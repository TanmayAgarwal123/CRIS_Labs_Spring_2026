### Architecture

***sae_config.py***
    * `d_in: int` --> This is an integer value representing the input dimension to the SAE. This will typically be the dimension of the output of the last layer in the LLM before we pass it to the SAE
    * `d_sae: int` --> This is an integer value representing the hidden dimension of the SAE. The input dimension will be projected into this higher dimensional space, where we will then enforce a sparsity penalty so that only the strongest features fire. Features correspond to the columns of the decoder weight matrix, while the rows of the encoder weight matrix correspond to which features should be used to minimize reconstruction loss.
    * `l1_coefficient: float` --> this is the sparsity penalty. In the vanilla SAE, this corresponds to the weight we apply to the sparsity that we then add to the loss, so higher sparsity penalty penalizes high weights more. This is irrelevant in the BatchTopKSAE, as we are using a discrete `k` to cutoff the number of features being used.
    * `dtype: str = "float32"` --> this is the data type used within the SAE
    * `device: str = "cuda" if torch.cuda.is_available() else "cpu"` --> This is the device used, hopefully it's cuda, but you can run on cpu if you really need to
    * `use_error_term: bool = False` --> honestly I think this is useless in the current pipeline. I'm pretty sure it doesn't get used anywhere. I initially added it because the SAELens library included it, but I can't for the life of me even remember what it was for
    * `hook_layer: str = "14"` --> This is the string representation of the hook layer, which we've defaulted to 14, but it doesn't really matter
    * `hook_name: str = "mlp_out"` --> This is the string representation of the hook name, which we've defaulted to mlp_out, but now that I'm looking at it I don't even think this should be the default. In fact, the default should probably be something like layer 9 and hook residual post or something
    * `hook_spec: str = f"blocks.{hook_layer}.{hook_name}"` --> This is just the full hook representation in string format, as we'll need this to call certain parts of the cache for the hooked transformers we are using - they take this particular string format
    * `top_k: Optional[int] = None` --> Optional parameter if we happen to be using TopK SAEs, or BatchTopKSAEs, specifices the top k features to take
    * `top_k_aux: Optional[int] = None` --> Optional parameter for the top k auxiliary loss, if it isn't specified but the top_k parameter is, it is defaulted to the max(1, top_k // 2). It determines the topk we use for the auxiliary loss, when looking at how many of the dead features to use. 
    * `n_batches_to_dead: int = 200` --> parameter determining how many batches a feature would need to have not fired for in order for us to consider that feature ``dead'', and have to use the auxiliary loss to revive it
    * `aux_penalty: float = 1/32` --> This is just the penalty we use to multiply the aux loss, which is the MSE of the residual and the reconstructed input using the dead features. A higher aux penalty means we induce the model to spend more effort trying to revive dead features to use for unexplained parts of the input. 
    * `def __post_init__(self)` --> function that ensures that if the `top_k_aux` parameter isn't specified, but the `top_k` is, we just default the aux top k to either 1 or half of the normal topk value
    * `def torch_dtype(self)` --> function that makes sure the typing is ok with the pytorch dtypes - if it's already torch.dtype, we keep it that way, and if it's given as a string, we return the pytorched version of the string, and if it's something else we just do `torch.float32`
    * `def to_dict(self)` --> just creates a dictionary of all of the config attributes
    * `def from_dict(cls, config_dict: dict)` --> takes in the config dictionary and fills the SAEConfig class with all of the values from the dictionary

***train_config.py***
    * `class Training Config` --> @dataclass for setting up the config for training the SAE
        * `num_epochs: int = 10` --> Just the number of epochs we train for, i.e. how many times do we iterate through our entire training dataset
        * `batch_size: int = 32` --> the batch size for our input text into the model and SAE
        * `lr: float = 1e-3` --> the learning rate we use for updating our parameters
        * `l1_coefficient: float = 0.01` --> this is the penalty weight we use for our sparsity loss, which only matters for the vanilla SAE, not the topk SAE
        * `num_dataloader_workers: int = 0` --> Number of workers for the PyTorch DataLoader
        * `persistent_workers: bool = False` --> If True, doesn't kill DataLoader object on each epoch
        * `pin_memory: bool = False` --> Pins memory for faster, asynchronous transfers to GPU 
        * `use_end_to_end: bool = True` --> This determines whether we use the end-to-end loss, which can include the block_mse losses for each layer after the target layer, and then also the KL-divergence of the output logits
        * `reconstruction_loss_weight: float = 1` --> This is the weight penalty applied to the target layer's reconstruction mse loss
        * `use_block_mse: bool = False` --> this determines whether we use the block_mse losses for each layer after the target layer, and we default to False because it doesn't seem to make that much of a difference, and greatly increases runtime when we do use it
        * `block_mse_weight: float = 0.1` --> penalty weight applied to each block_mse loss if we choose to use it
        * `block_mse_layers: Optional[List[int]] = None` --> Optional parameter to list out the specific layers we want to do block_mse loss at
        * `use_logit_kl: bool = True` --> Determines whether we include the resulting KL divergence on the logits as part of our loss
        * `logit_kl_weight: float = 0.1` --> penalty weight applied to KL divergence loss
        * `log_freq: int = 100` --> how often we log the losses and other metrics when iterating over the batches in our dataloader
        * `activation_batch_size: int = 16` --> For memory purposes, chunks the activations even further to make sure we can successfully do the sae forward pass on the activations
        * `max_text_length: int = 256` --> This is the maximum text length that we use in our windowed dataset creation. Basically this is just the maximum length of a window that we tokenize
        * `def __post_init__(self)` --> ensures that if we are doing end_to_end loss, then at least one of block_mse or kl_div loss is being used, otherwise we would run into an error in the training phase
    
***sae_base.py***
    * `class SAE(nn.Module)` --> base class for the SAE
        * `def __init__(self, cfg: SAEConfig)` --> initialize the SAE
            * `self.cfg` --> takes in the SAEConfig class and uses that as the configuration
                * `self.dtype`
                * `self.device`
                * `self.use_error_term`
                * `self.hook_spec`
            * `self._last_dense_acts: Optional[Tensor] = None` --> keeps track of the most recent dense activation before any transformations
            * `self.register_buffer` --> Adds a buffer called "ever_fired" which is a zeros vector of boolean values of size d_sae, basically to keep track of which features in the SAE never fire
            * `self.initialize_weights()` --> calls the initialize weights method to initialize the parameters
        * `def get_hook_spec(self)` --> just returns the string of the hook_spec
        * `def initialize_weights(self)` --> Initializes the encoder and decoder weights and biases
            * `W_enc` --> Encoder matrix of size [d_in, d_sae], initialized using kaiming_uniform
            * `b_enc` --> Encoder bias, vector of length [d_sae], initialized as all zeros vector
            * `W_dec` --> Decoder matrix of size [d_sae, d_in], initialized as the transpose of the encoder matrix
            * `b_dec` --> decoder bias, vector of length [d_in], initialized as all zeros vector
        * `def encode(self, x: Tensor)` --> Encodes the model activations into the sae feature spase, to then be sparsified afterwards
            * matrix multiplies the x input tensor by `W_enc`, then addes `b_enc`, then takes the relu
        * `def decode(self, features: Tensor)` --> decodes the encoded features back into the input space so they can be passed along back to the model pipeline
            * matrix multiples the features by `W_dec`, then adds the `b_dec`
        * `def forward(self, x: Tensor)` --> forward pass taking in the model activations, returning both the reconstructed output and the encoded features
            * First centers the x input be subtracting the `b_dec` (Anthropic does this in their papers), then gets features by calling the `encode` function, then gets `x_recon` by calling the `decode` function on the features, then stores the features as the last dense activations, and returns `x_recon, features`
        * `def normalize_decoder(self)` --> Normalizes the rows of the decoder matrix to unit norm, using `torch.norm` on the 1st dimension (columns), then divides `W_dec` by its norm
        * `def training_forward(self, x: Tensor)` --> Forward pass specifically for training, returns dictionary of losses. First calls the forward function, then computes reconstruction loss for target layer by doing `F.mse_loss` on the x input and the reconstructed x from the forward pass. Then calculates the sparsity loss, by taking the absolute value of the features and then finding its mean, then return a dictionary with the recon loss, the l1 sparsity loss, the features, and the reconstructed x.
        * `def update_inactive_features(self, features: Tensor)` --> tracks which features have ever fired by collapsing the features matrix by rows so that we only have 1 row corresponding to all features, then we see which ones are > 0, and then we update the `self.ever_fired` attribute vector by doing a bitwise OR with the new boolean vector
        * `def count_dead_features(self)` --> basically just does a bitwise NOT operator on the `self.ever_fired` vector and sums the result to see how many features have never fired during training
        * `def dead_feature_percentage(self)` --> just uses the counts calculated in the method above and divides by the total number of features, `d_sae`, and finds the percentage
        * `def save(self, path:str, history: Optional[Dict[str, List[float]]] = None)` --> saves the model weights and config file. Creates a `weights.pt` filepath, and saves the SAE class' state_dict, dumps the config dictionary into a `config.json` file, and then dumps the history of losses into a `history.json` file
        * `def load(cls, path:str, device:str = "cpu", load_history: bool = False)` --> Loades the model from the cpu, optional parameter to load the training history as well. Basically just dumps the config json contents into a dictionary, then uses the `SAEConfig.from_dict` method to load the dictionary. Then defines the model based on the model class specified and the config just created, loads the weights into the model's state_dict, and then loads the history as a dictionary from the json file
    * `class BatchTopKSAE(SAE)` --> Class for the BatchTopKSAE, takes as parent the default SAE class
        * `def __init__(self, cfg: SAEConfig)` --> first ensures that the relevant parameters are set to use batchTopKSAE
            * sets a new buffer for `"num_batches_not_active"` as a zeros vector for all features (d_sae)
        * `def encode(self, x: Tensor)` --> encodes the model activations, similar to the vanilla SAE, but we don't include `b_enc`
        * `def forward(self, x: Tensor)` --> forward pass, first centers x input by subtracting `b_dec`, then encodes the input, saves this as the last_dense_acts. Then we flatten the encoded activations, then reshaping them by collapsing everything into a 1D tensor, doing batch*seq_len*d_sae, and then we do `torch.topk` on this flattened vector over the 0th dimension, getting the top k values and their indices for the batch. Then we create a new vector corresponding to the sparse version of the encoded activations, by making it an all zeros vector, and then using indexing to set all the indices corresponding to the topk values in the batch to their values, leaving everything else as 0. Then we reshape the sparse encoded activations back into the original shape of [batch, seq_len, d_sae], and pass that along to the decoder method to get the reconstructed activations.
    * `def update_inactive_features(self, features: Tensor)` --> Updates the attributes for active/inactive features
        * we essentially find which features have fired in this batch/iteration, doing a bitwise OR on the `self.ever_fired` vector, and then adding to the `self.num_batches_not_active` vector the bitwise NOT operation on the `fired` vector, adding 1 to the count if the feature didn't fire in that batch. We then set the indices of those that HAVE fired to 0, resetting if it fired this batch. The `self.num_batches_not_active` is just an active counter of how many batches it has been since that feature has last fired.
    * `def get_auxiliary_loss(self, x:Tensor, x_recon:Tensor)` --> Calculates the auxiliary loss for batchtopksae
        * we first calculate how many of the features have been dead as determined by our "deadness" threshold, then retrive only the features we consider dead from our encoded activations. We then do another separate top_k_aux on these dead features, same as the forward pass. We then calculate the residual from the original input and the original x_recon, and then try to get our dead features to compensate for the reconstruction residual we do have
    * `project_decoder_gradients(self)` --> function to remove gradients that would stretch or shrink the magnitude of the decoder features, so model only updates the direction of the features rather than their scale - similar to normalizing the decoder

### Training

***training.py***
    * `def train_sae()` --> main training loop function
        * `sae: BatchTopKSAE` --> SAE class
        * `model: HookedTransformer` --> LLM from HookedTransformer librayr
        * `data_loader: DataLoader` --> PyTorch DataLoader object, most likely from the WindowedTextDataset
        * `config: TrainingConfig` --> TrainingConfig object to determine traning hyperparameters
        * `checkpoint_dir: Optional[Path] = None` --> directory filepath for where to save the checkpoints
        * `checkpoint_freq: int = 5` --> how frequently we want to save a checkpoint of the model
        * `save_best: bool = True` --> whether we want to save the best model over all checkpoints
        * `val_loader: Optional[DataLoader] = None` --> dataloader for the validation set, if we choose to use it
        * First we set the model into evaluation mode and freeze all the model parameters by setting their `requires_grad` param to False. We define the optimizer as the Adam optimizer, and set the learning rate from the training config. We set the hook specification, and define the the block_mse layers we want to track. We then setup the metrics, which include the various losses we want to track. We then setup a list of layer names to track when we collect the model activations in the cache, and create a history dictionary to track all of the metrics throughout each epoch. We define the `pad_token_id` from the model's tokenizer, and thus complete our setup for training
        * `def forward_batch(batch: torch.Tensor)` --> forward pass of a batch where we collect model activations from the LLM
            * we use `model.run_with_cache` on the batch with a filter from the cache names to ensure we only get the activations for the layers we want, and get the logits and the activations from the LLM. We then flatten the activations so that they go from [batch_size, seq_len, d_model] to [batch_size*seq_len, d_model], and then flatten the tokens as well into a 1D vector. We then find which parts of the flattened token vector are NOT padding tokens, and set or activations to only those elements, so we get rid of all padding activations, with our activations now of size [N_real, d_model]
            * `def sae_forward_on_real_activations(real_acts: torch.Tensor)` --> foward pass of the activations through the sae
                * if we happen to be using a specific activation batch size, this is where that appears. We chunk the activations and the features into tensors of length `activation_batch_size`, and then concatenate all chunked activations/features into a full tensor each, returning that
                * if we aren't using activation batches, then we just send the activations directly from the model into the sae forward pass and return the outputs
            * After we have gotten the sae activations, we get the reconstruction loss by doing the MSE between the original model activations with the sae activations, and also get the l1 sparsity loss from the features. Then we get the total loss from the layer by applying the penalty weights and summing the losses. Next we find the auxiliary loss between the real activations and the sae activations (which is similar to the reconstruction loss, but it just has a different penalty applied)
            * Then we find the sparsity of the batch by looking at the mean of how many features are > 0 
            * If we are using end-to-end loss, we define some new vectors, as we need to be able to send the reconstructed sae output back into the model instead of the model's previous layer. But since the sae activations are of a smaller length (because we only encoded the non-padding tokens), we need to make sure the shapes align, so we clone the original clean model activations, and then overwrite only the rows that were non-padding with the sae's reconstruction
            * We then define the hook which replaces the model activations with the sae reconstruction
            * if we're doing block_mse, we compare the activations from the clean input with the activations from the intervened sae input, and compre the MSE for each layer we want to look at
            * If we're doing KL divergence, we use an attention mask for all non padding tokens, and compute the KL divergence between the intervened and the clean logits
            * We then store all of the losses in a dictionary, and return the total loss, the stats dictionary, and the sae features
        * `def evaluate(loader: DataLoader)` --> evaluation function to evaluate the SAE on the validation dataset
            * We basically just iterate over the validation set, running the forward training pass through the SAE and collecting the loss statistics and filling up an evaluation dictionary with the statistics, returning the metrics and the number of batches processed
        * After defining the training and evaluation functions, we finally actually iterate over our dataloader for however many epochs we specified in the config, zero_gradding the optimizer, getting the results from the training forward pass on each batch, calling `loss.backward()` to get gradients, calling `sae.project_decoder_gradients()` to ensure `W_dec` isn't being scaled, just rotated, then we do `optimizer.step()` to apply the backwards gradient updates, and then we normalize the decoder again just in case. Then we call `sae.update_inactive_features` to keep track of any dead features
        * We then do a bunch of bookkeeping, keeping track of all the metrics and printing out the highlights
    * `def compute_kl_divergence` --> computes the kl divergence of the resulting logits
        * `logits_intervened: torch.Tensor` --> logits of the model that had the sae activation intervention
        * `logits_clean: torch.Tensor` --> logits of the clean model
        * `temperature: float = 1.0` --> stochasticity of the softmax we apply to the logits before computing kl divergence
        * `mask: Optional[torch.Tensor] = None` --> mask to only look at the non-padding tokens
        * This function takes the softmax of each of the logits, and then just does the built-in torch `F.kl_div` function to find KL(P_intervened || P_clean), which should induce the sae to not have the intervened model's logits stray to far from the clean logits. 

### Data Pipeline

***sae_train.py***
    * `class WindowedTextDataset(Dataset)` --> Creates a dataset of tokenized text so we don't have to re-tokenize each training epoch
        * `def __init__(self, texts: List[str], tokenizer, max_length: int, prepend_bos: bool = False)`
            * takes in list of text strings, checks to see if it is empty
            * sets the bos token from the tokenizer, calls the `self._build_windows()` method to create the windowed dataset
        * `def __len__(self)` --> returns the length of the windowed dataset (`self.windows`)
        * `def _tokenize(self, text: str)` --> tokenizes a string of text
            * takes `self.tokenizer` from the model tokenizer , returns pytorch tensors without padding, without trunction, and without special tokens, corresponding to the token ids
            * if we want to prepend the bos token, we concatenate 1 bos token to the beginning of the encoded tokenized tensor, otherwise we return the tokenized tensor as is
        * `def _build_windows(self)` --> Tokenize the input strings in the list, add these tensors to a list that we can turn into a full dataset
            * create a list that will take in tensors
            * iterate over all strings in the input text list, tokenize the strings, append them to window, ensure they are <= the max length
        * `def __getitem__(self, idx: int)` --> return the tokens vector from the given argument index from the window
    * `def pad_collate(batch: List[torch.Tensor], pad_token_id: int)` --> pads tokenized tensors in a batch to ensure we can pass the tokenized batch as 1 nice block
        * we first find the max length of all the tokenized vectors in the batch, then we pad all of the vectors in the batch to this max length
            * we do this by creating a matrix of size (batch_len, max_len), filling it with all padding tokens
            * then we iterate over each row in the batch (corresponding to a sequence of tokens), and fill the matrix with the token ids
    * `class SAETrainer`
        * `def __init__(self, mdoel: HookedTransformer, sae_class: SAE, sae_config: SAEConfig, train_config: TrainingConfig, device: str="cuda" if torch.cuda.is_available() else "cpu())`
            * set all the necessary parameters, mostly using the config files
        * `def train(self, texts: List[str], checkpoint_dir: Optional[str] = None, checkpoint_freq: int=5, save_best: bool = True, val_texts: Optional[List[str]] = None)`
            * first we set the `pad_token_id` to the tokenizers pad token id
            * we define the dataset as the `WindowedTextDataset` of the texts
            * we set the persistent workers parameter for better GPU usage efficiency
            * we then create a DataLoader object using the dataset, shuffling the data, collating each batch using the `pad_collate` function from earlier
                * we do the same if we have a validation dataset as well
            * Then we just call the `train_sae` function from `training.py` 

    

### Analysis Pipeline

***full_analysis.py***
    * `class TokenMetadata` --> dataclass for storing metadata for each token in the corpus
        * `global_idx: int` --> Global index across the entire corpus
        * `text_idx: int` --> Which textbook in the dataset this token comes from
        * `position: int` --> position within the textbook
        * `token_id: int` --> token ID
        * `token_str: str` --> string representation of token
    * `class ActivationDatabase` --> Stores activation data for the entire corpus
        * `def __init__(self, activation_matrix: sparse.csr_matrix, token_metadata: List[TokenMetadata], feature_metadata: Dict[str, any])`
            * sets these attributes, and then calls the `build_indices()` function to build indices for fast lookup for feature --> token
        * ` def build_indices(self)` --> builds reverse lookup structures
            * we essentially want to be able to choose a specific feature, and get a list of token indices where the feature activated
            * we do this by building a dictionary `feature_to_tokens`, creating a lookup with features as the keys and a list of all tokens as the values
        * `def get_feature_activations(self, feature_idx: int, top_k: Optional[int] = None)`
            * This function gets all the tokens where a feature activated and returns a list of (token_idx, activation_value) tuples, sorted by activation value
            * This is per-feature, so for a given input feature, we find all tokens that fired for this feature, iterating over all tokens and appending a tuple of the (token_idx, act_value), where the activation value has been taken from the existing activation matrix, which is the sparse activation matrix
            * Then we sort the list of token activations, and return the max_results values if we want to just look at the most important activations
        * `def get_token_activations(self, token_idx: int, threshold: float = 0.0)` --> Gets all features that activated for a specific token
            * This is the opposite of the previous functions, and returns a list of (feature_idx, activation_value) tuples, also sorted by activation
            * First we extract the row from the sparse activation matrix corresponding to the target token index, convert it to an array, then iterate over all features in that row, and if the activation value of that feature is bigger than the threshold, we add that feature as a tuple to the list of active features, then sort again by activation value
        * `def get_token_context(self, token_idx: int, context_size: int = 10)` --> Get the surrounding context and other information about a token
            * This function creates a dictionary of the contextual information of a particular token, creating a string of the surrounding context as well
            * This function assumes the metadata class has already been defined and filled
        * `def save(self, path:str)` --> Save the activation database to disk
            * uses pickle to dump a dictionary of the activation matrix, the token metadata, and the feature metadata into a file
        * `def load(path:str)` --> loads the activation database class from a file
    * `class SAEAnalyzer` --> Analyzes the trained SAE performance and feature interpretability
        * `def __init__(self, model: HookedTransformer, sae_path:str, layer:int, hook_name: str, dataset: List[str])`
            * First we load the sae by calling the `load_pretrained` method and using the sae file itself, then we send all the model parameters to GPU, as well as the sae itself, and then set the sae into eval mode
        * `def reset_model_state(self)` --> clears all hooks and the GPU cache
            * calls `model.reset_hooks()`, which is a HookedTransformer method to clear all hooks
            * calls `torch.cuda.empty_cache()` to empty the cuda cache
        * `def _prepare_square_matrix(self, n_features:int, save_path: Optional[str], filename_prefix:str)` --> Allocates on-disk storage for large NxN matrices
            * basically just allocates some space for a square matrix so memory doesn't blow up
        * `def collect_all_activations(self, texts: Optional[List[str]] = None, batch_size: int = 8, activation_threshold: float = 0.0, save_path: Optional[str] = None)`
            * we basically iterate through the corpus, tokenizing it, sending it to the model hook, encoding the result with the SAE
            * we build a sparse [token x feature] matrix, tracking per-feature counts/means/sparsity
        * `def compute_feature_similarity` --> chunk-computes decoder-weight similarity (cosine/dot/euclidean) into a memmap
        * `def find_similar_features` --> Pulls top neighbors
        * `def compute_feature_cooccurence` --> builds a co-activation matrix (correlation/Jaccard/PMI) in chunks
        * `def find_coactivating_features` --> queries the co-activation matrix
        * `def analyze_feature_with_context` --> Prints top actiations with surrounding text and similar features
        * `def find_max_activating_examples` --> returns top contexts
        * `def analyze_feature_clusters` --> shows co-activating features and shared examples
        * `def compute_sparsity_metrics` --> computes L0/L1 per token and per-feature activation frequencies
        * `def find_dead_features` --> flags rarely firing features
        * `def compute_reconstruction_metrics` --> measures SAE MSE, explained variance, cosine simlarity on activations
        * `def compute_ce_loss` --> Helper function to compute cross entropy loss
        * `def ablation_study` --> compares baseline loss to zero-ablation and SAE-reconstruction hooks and reports loss recovered
        * `def run_full_analysis` --> runs sparsity, dead-features, reconstruction, ablation, and saves into JSON (optional)