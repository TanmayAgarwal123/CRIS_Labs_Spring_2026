***Core Training Architecture Overview***
## Data Flow
    * Raw Text -> WindowedTextDataset -> DataLoader -> Model Forward Pass -> SAE Training -> Checkpoints/Model Save

## File Structure & Responsibilities
*Core SAE Components*
    * `sae_config.py`: Configuration dataclass for SAE architecture
        * Defines: d_in, d_sae, l1_coefficient, hook specs, etc.
    * `sae_base.py`: SAE imlementations
        * `SAE`: Base vanilla SAE
        * `BatchTopKSAE`: Batch Top-K SAE variant
    * `train_config.py`: SAE training configuration 
        * Learning rates, loss coefficients, end-to-end training flags, etc.

*Training Components*
    * `training.py`: Core training loop
        * `train_sae()`: Main training function
        * `compute_kl_divergence()`: KL divergence loss between clean/intervened logits
    * `sae_train.py`: High level training wrapper
        * `WindowedTextDataset`: Efficient tokenization and windowing class
        * `SAETrainer`: Class to orchestrate training process

*Execution Scripts*
    * `Qwen_sae_training.py`: Main training entry point
        * Model loading, config setup, training execution

## Key Concepts to Better Understand
1. Dead Features Issue
    * Some SAE features never activate during training
        * Wastes SAE capacity, reduces interpretability
    * **BatchTopKSAE Solution:** Auxiliary loss to revive dead features
2. All changes to pipeline I still don't understand completely
    * WindowedTextDataset
    * padding token + masking
    * KL divergence 
    * train + val split
    * Overall BatchTopKSAE math/implementation

## Current State Questions to Answer
*Architecture Questions*
    * Why did I choose expansion factor 4? Why not 8, 16, etc.?
    * Why BatchTopKSAE over vanilla SAE?
    * What's the relationship between top_k and top_k_aux?
    * Why remove encoder bias in BatchTopKSAE?
*Training Questions*
    * Why these specific loss weights?
    * What does activation_batch_size do exactly?
    * What's the correct KL divergence direction?
*Data Questions*
    * What the hell is WindowedTextDataset and why do we use it?
    * How many tokens in training set?
    * What's the distribution of text lengths?
    * Why max_text_length = 256?
    * Is validation split size appropriate?