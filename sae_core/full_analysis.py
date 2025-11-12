import torch
import torch.nn as nn
from transformer_lens import HookedTransformer
import numpy as np
from typing import List, Dict, Tuple, Optional
from tqdm import tqdm
import heapq
from scipy import sparse
from dataclasses import dataclass
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

from sae_core.pretrained import load_pretrained


@dataclass
class TokenMetadata:
    """Metadata for each token in the corpus"""
    global_idx: int     # Global index across the entire corpus
    text_idx: int       # Which textbook in the dataset
    position: int       # Position within textbook
    token_id: int       # token Id
    token_str: str      # String representation of token


class ActivationDatabase:
    """
    Stores activation data for entire corpus

    Structure:
    - activation_matrix: Sparse matrix [n_tokens x n_features]
    - token_metadata: List of TokenMetadata for each token
    - feature_metadata: Dictionary with feature statistics
    """

    def __init__(
        self,
        activation_matrix: sparse.csr_matrix,   # compressed sparse row matrix for memory efficiency
        token_metadata: List[TokenMetadata],
        feature_metadata: Dict[str, any]
    ):
        self.activation_matrix = activation_matrix
        self.token_metadata = token_metadata
        self.feature_metadata = feature_metadata

        # build reverse indices for fast lookup for feature -> token
        self.build_indices()

    def build_indices(self):
        """Build reverse lookup structures"""
        # Feature -> list of token indices where the feature activated
        self.feature_to_tokens = {}
        
        print("Building feature activation index")
        # Get non-zero entries
        rows, cols = self.activation_matrix.nonzero()

        for token_idx, feature_idx in tqdm(
            zip(rows, cols),
            total=len(rows),
            desc="Indexing"
        ):
            if feature_idx not in self.feature_to_tokens:
                self.feature_to_tokens[feature_idx] = []
            self.feature_to_tokens[feature_idx].append(token_idx)

    def get_feature_activations(
            self,
            feature_idx: int,
            top_k: Optional[int] = None 
    )-> List[Tuple[int, float]]:
        """
        Get all tokens where a feature activated
        Returns a list of (token_idx, activation_value) tuples, sorted by activation
        """
        if feature_idx not in self.feature_to_tokens:   # feature never fired
            return []
        
        token_indices = self.feature_to_tokens[feature_idx]
        activations = []

        for token_idx in token_indices:
            act_value = self.activation_matrix[token_idx, feature_idx]
            activations.append((token_idx, act_value))

        activations.sort(key=lambda x: x[1], reverse=True)

        if top_k is not None:
            activations = activations[:top_k]

        return activations
    
    def get_token_activations(
            self,
            token_idx: int,
            threshold: float = 0.0
    ) -> List[Tuple[int, float]]:
        """
        Get all features that activated for a specific token
        Returns a list of (feature_idx, activation_value) tuples, also sorted by activation
        """
        token_activations = self.activation_matrix[token_idx].toarray()[0]

        active_features = []
        for feature_idx, act_value in enumerate(token_activations):
            if act_value > threshold:
                active_features.append((feature_idx, act_value))

        active_features.sort(key=lambda x: x[1], reverse=True)

        return active_features
    
    def get_token_context(
            self, 
            token_idx: int,
            model: HookedTransformer,
            context_size: int = 10
    ) -> Dict[str, any]:
        """
        Get contextual information about a token
        Returns a dictionary with token string, position, surrouding context, etc.
        """
        metadata = self.token_metadata[token_idx]

        # Find neighboring tokens in the same text
        text_tokens = [
            t for t in self.token_metadata if t.text_idx == metadata.text_idx
        ]

        # Get context window
        start_pos = max(0, metadata.position - context_size)
        end_pos = min(len(text_tokens), metadata.position + context_size + 1)
        
        context_tokens = text_tokens[start_pos:end_pos]
        context_str = " ".join([t.token_str for t in context_tokens])

        return {
            'global_idx': metadata.global_idx,
            'text_idx': metadata.text_idx,
            'position': metadata.position,
            'token': metadata.token_str,
            'token_id': metadata.token_id,
            'context': context_str,
            'context_tokens': [t.token_str for t in context_tokens]
        }
    
    def save(self, path: str):
        """Save activation DB to disk"""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            'activation_matrix': self.activation_matrix,
            'token_metadata': self.token_metadata,
            'feature_metadata': self.feature_metadata
        }

        with open(path, 'wb') as f:
            pickle.dump(data, f)

        print(f"Saved activation DB to {path}")

    @staticmethod
    def load(path:str) -> 'ActivationDatabase':
        """Load activation database"""
        with open(path, 'rb') as f:
            data = pickle.load(f)

        db = ActivationDatabase(
            activation_matrix=data['activation_matrix'],
            token_metadata=data['token_metadata'],
            feature_metadata=data['feature_metadata']
        )

        print(f"Loaded activation DB from {path}")
        print(f" {len(db.token_metadata)} tokens, {db.activation_matrix.shape[1]} features")

        return db
    


class SAEAnalyzer:
    """Analyze trained SAE performance and feature interpretability"""

    def __init__(
        self,
        model: HookedTransformer,
        sae_path: str,
        layer: int,
        hook_name: str,
        dataset: List[str]
    ):
        self.model = model
        self.dataset = dataset
        self.layer = layer
        self.hook_name = hook_name
        self.hook_point = f"blocks.{layer}.{hook_name}"

        self.activation_db: Optional[ActivationDatabase] = None
        self.feature_similarity: Optional[np.ndarray] = None

        # Validate dataset
        if not dataset or len(dataset) == 0:
            raise ValueError("Dataset is empty :(")
        
        # Filter out empty strings from dataset
        self.dataset = [text for text in dataset if text and len(text.strip()) > 0]
        if len(self.dataset) == 0:
            raise ValueError("Dataset contained only empty strings :(")
        
        # Load SAE
        self.sae = load_pretrained(sae_path)
        self.device = next(self.model.parameters()).device
        self.sae = self.sae.to(self.device)
        self.sae.eval()

        print(f"Loaded SAE from {sae_path}")
        print(f"Model and SAE on device: {self.device}")
        print(f"Hook point: {self.hook_point}")
        print(f"SAE Dim: {self.sae.cfg.d_in} -> {self.sae.cfg.d_sae}")
        print(f"Dataset: {len(self.dataset)} texts")

    def reset_model_state(self):
        """Clear all hooks and GPU cache"""
        self.model.reset_hooks()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    def collect_all_activations(
        self,
        texts: Optional[List[str]] = None,
        batch_size: int = 8,
        activation_threshold: float = 0.0,
        save_path: Optional[str] = None,
    ) -> ActivationDatabase:
        """
        Process entire corpus and build activation DB
        Returns activation DB with full activation matrix and token metadata
        """
        if texts is None:
            texts = self.dataset

        # Validate texts
        texts = [t for t in texts if t and len(t.strip()) > 0]
        if len(texts) == 0:
            raise ValueError("No valid texts to process :(")
        
        self.reset_model_state()

        all_activations = []
        token_metadata = []
        global_token_idx = 0

        # Track padding tokens
        padding_tokens_skipped = 0
        pad_token_id = self.model.tokenizer.pad_token_id
        print(f"Pad token ID: {pad_token_id}")

        # Feature statistics
        feature_activation_counts = torch.zeros(self.sae.cfg.d_sae)
        feature_total_activation = torch.zeros(self.sae.cfg.d_sae)

        print(f"Collecting activations from {len(texts)} texts")

        for text_idx in tqdm(range(0, len(texts), batch_size), desc="Processing"):
            batch_texts = texts[text_idx: text_idx+batch_size]

            try:
                tokens = self.model.to_tokens(batch_texts, prepend_bos=True)
                tokens = tokens.to(self.device) # [batch_size, seq_len]

                if tokens.numel() == 0:  # skip token if it's an empty tensor
                    print(f"Empty batch at idx: {text_idx}")
                    continue

            except Exception as e:
                print(f"Failed to tokenize batch {text_idx//batch_size}: {e}")
                continue

            with torch.no_grad():
                try:
                    # Get hook point activations
                    logits, cache = self.model.run_with_cache(
                        tokens, 
                        names_filter=lambda name: name == self.hook_point
                    )
                    acts = cache[self.hook_point]   # [batch_size, seq_len, model_layer_dim]

                    # Encode with SAE
                    for batch_idx in range(acts.shape[0]):
                        text_global_idx = text_idx + batch_idx

                        for pos in range(acts.shape[1]):
                            # Get token ID 
                            token_id = tokens[batch_idx, pos].item()
                            
                            # Skip padding tokens (critical fix for Qwen)
                            if token_id == pad_token_id:
                                padding_tokens_skipped += 1
                                continue
                            
                            # Get features for this token
                            token_acts = acts[batch_idx, pos, :]
                            features = self.sae.encode(token_acts.unsqueeze(0))[0]

                            # Get token string
                            token_str = self.model.to_string(tokens[batch_idx, pos])

                            # Store metadata
                            metadata = TokenMetadata(
                                global_idx=global_token_idx,
                                text_idx=text_global_idx,
                                position=pos,
                                token_id=token_id,
                                token_str=token_str
                            )
                            token_metadata.append(metadata)

                            # Store activations
                            active_features = (features > activation_threshold).nonzero(as_tuple=True)[0]

                            for feature_idx in active_features:
                                feature_idx_int = feature_idx.item()
                                activation_value = features[feature_idx].item()

                                all_activations.append((
                                    global_token_idx,
                                    feature_idx_int,
                                    activation_value
                                ))

                                feature_activation_counts[feature_idx_int] += 1
                                feature_total_activation[feature_idx_int] += activation_value

                            global_token_idx += 1

                except Exception as e:
                    print(f"Error processing batch {text_idx//batch_size}: {e}")
                    continue

            self.reset_model_state()

        print(f"Processed {global_token_idx} tokens")
        print(f"Padding tokens skipped: {padding_tokens_skipped}")
        print(f"Collected {len(all_activations)} non-zero activations")

        rows, cols, values = zip(*all_activations) if all_activations else ([],[],[])

        activation_matrix = sparse.csr_matrix(
            (values, (rows, cols)),
            shape = (global_token_idx, self.sae.cfg.d_sae)
        )

        feature_metadata = {
            'n_features': self.sae.cfg.d_sae,
            'n_tokens': global_token_idx,
            'activation_counts': feature_activation_counts.tolist(),
            'total_activations': feature_total_activation.tolist(),
            'mean_activation': (feature_total_activation / (feature_activation_counts + 1e-8)).tolist(),
            'sparsity': 1.0 - (len(all_activations) / (global_token_idx * self.sae.cfg.d_sae))
        }

        print(f"Matrix shape: {activation_matrix.shape}")
        print(f"Sparsity: {feature_metadata['sparsity']*100:.2f}% (zeros)")

        self.activation_db = ActivationDatabase(
            activation_matrix=activation_matrix,
            token_metadata=token_metadata,
            feature_metadata=feature_metadata
        )

        if save_path is not None:
            self.activation_db.save(save_path)

        return self.activation_db
    
    def load_activation_database(self, path:str):
        """Load a previously saved activation DB"""
        self.activation_db = ActivationDatabase.load(path)
        return self.activation_db
    
    def compute_feature_similarity(
        self,
        save_path: Optional[str] = None,
        similarity_metric: str = 'cosine'
    ) -> np.ndarray:
        """
        Compute pairwise similarity between SAE features based on decoder weights
        Features with similar decoder directions should represent similar concepts
        Returns a similarity matrix [n_features x n_features]
        """
        print(f"Compution feature similarity using {similarity_metric}")

        # Get decoder weights [d_sae, d_in]
        decoder = self.sae.W_dec.detach().cpu()
        n_features = decoder.shape[0]

        if similarity_metric == 'cosine':
            # Normalize each feature's decoder
            decoder_normalized = decoder / (decoder.norm(dim=1, keepdim=True) + 1e-8)

            # Compute pairwise cos similarity
            similarity = decoder_normalized @ decoder_normalized.T

        elif similarity_metric == 'dot':
            similarity = decoder @ decoder.T

        elif similarity_metric == 'euclidean':
            # We'll do negative euclidean distance so higher is more similar
            decoder_sq = (decoder **2).sum(dim=1, keepdim=True)
            distances = decoder_sq + decoder_sq.T - 2*(decoder @ decoder.T)
            similarity = -torch.sqrt(torch.clamp(distances, min=0))

        else:
            raise ValueError(f"Unknown similarity metric: {similarity_metric}")
        
        self.feature_similarity = similarity.numpy()

        print(f"Computed {n_features}x{n_features} similarity matrix")

        if save_path is not None:
            np.save(save_path, self.feature_similarity)
            print(f"Saved similarity matrix to {save_path}")

        return self.feature_similarity
    
    def find_similar_features(
        self,
        feature_idx: int,
        top_k: int = 10,
        exclude_self : bool = True
    ) -> List[Tuple[int, float]]:
        """
        Find features most similar to a given feature
        Returns list of (feature_idx, similarity_score) tuples
        """
        if self.feature_similarity is None:
            raise ValueError("Must call compute_feature_similarity() first")
        
        similarities = self.feature_similarity[feature_idx]

        # Get top k indices
        if exclude_self:
            similarities = similarities.copy()
            similarities[feature_idx] = -np.inf

        top_indices = np.argsort(similarities)[-top_k:][::-1]   # ascending, so take last k, then reverse order
        top_similarities = similarities[top_indices]

        results = list(zip(top_indices.tolist(), top_similarities.tolist()))

        return results
    
    def analyze_feature_with_context(
        self,
        feature_idx: int,
        top_k: int = 10,
        context_size: int = 10
    ):
        """
        Analysis of a single feature:
        - max activating examples with context
        - similar features by decoder
        """
        if self.activation_db is None:
            raise ValueError("Must collection activations into db first")
        if self.feature_similarity is None:
            raise ValueError("Must compute feature similarities first")
        
        print(f"Feature {feature_idx} Analysis")
        activation_freq = self.activation_db.feature_metadata['activation_counts'][feature_idx]
        mean_activation = self.activation_db.feature_metadata['mean_activation'][feature_idx]

        print(f"Frequency: {activation_freq} tokens ({activation_freq/self.activation_db.feature_metadata['n_tokens']*100:.2f}%)")
        print(f"Mean activation: {mean_activation:.4f}")

        # Get max activating examples
        activations = self.activation_db.get_feature_activations(feature_idx, top_k=top_k)

        for i, (token_idx, act_val) in enumerate(activations, 1):
            context = self.activation_db.get_token_context(
                token_idx,
                self.model,
                context_size=context_size
            )
            print(f"\n{i}. Activation: {act_val:.4f}")
            print(f"Token: '{context['token']}'")
            print(f"Context: {context['context']}")

        similar_features = self.find_similar_features(feature_idx, top_k=5)

        for i, (sim_feature_idx, similarity) in enumerate(similar_features, 1):
            sim_activations = self.activation_db.get_feature_activations(sim_feature_idx, top_k=1)
            print(f"\n{i}. Feature {sim_feature_idx} (similarity: {similarity:.4f})")

            if sim_activations:
                token_idx, act_val = sim_activations[0]
                context = self.activation_db.get_token_context(token_idx, self.model, context_size=5)
                print(f" Example: '{context['token']}' in context: {context['context']}")

    def compute_sparsity_metrics(
        self,
        texts: Optional[List[str]] = None,
        batch_size: int = 8
    ) -> Tuple[Dict[str, float], List[float]]:
        """
        Compute L0 (number of activate features) and L1 (sum of activations)
        Return dictionary with L0/L1 mean and std, return list of activation frequencies for each feature
        """
        if texts is None:
            texts = self.dataset
        
        # Validate texts
        texts = [t for t in texts if t and len(t.strip()) > 0]
        if len(texts) == 0:
            raise ValueError("No valid texts to process :(")
        
        self.reset_model_state()

        pad_token_id = self.model.tokenizer.pad_token_id

        # Running stats
        l0_sum = 0.0
        l0_sq_sum = 0.0
        l1_sum = 0.0
        l1_sq_sum = 0.0
        feature_counts = torch.zeros(self.sae.cfg.d_sae, device='cpu')
        n_tokens_total = 0

        for i in tqdm(range(0, len(texts), batch_size), desc="Sparsity"):
            batch_texts = texts[i:i+batch_size]

            try:
                tokens = self.model.to_tokens(batch_texts, prepend_bos=True)
                tokens = tokens.to(self.device)

                if tokens.numel() == 0:
                    print(f"Warning: Batch {i//batch_size} produced no tokens, skipping...")
                    continue

            except Exception as e:
                print(f"Warning: Failed to tokenize batch {i//batch_size}: {e}")
                continue

            with torch.no_grad():
                try:
                    logits, cache = self.model.run_with_cache(
                        tokens,
                        names_filter=lambda name: name == self.hook_point
                    )
                    acts = cache[self.hook_point]

                    # Flatten batch and sequence dimensions
                    acts_flat = acts.reshape(-1, acts.shape[-1])
                    tokens_flat = tokens.reshape(-1)
                    non_padding_mask = tokens_flat != pad_token_id
                    acts_flat = acts_flat[non_padding_mask]

                    # Skip if no activations
                    if acts_flat.shape[0] == 0:
                        continue

                    features = self.sae.encode(acts_flat)

                    l0_per_token = (features > 0).float().sum(dim=1)
                    l0_sum += l0_per_token.sum().item()
                    l0_sq_sum += (l0_per_token **2).sum().item()

                    l1_per_token = features.abs().sum(dim=1)
                    l1_sum += l1_per_token.sum().item()
                    l1_sq_sum += (l1_per_token ** 2).sum().item()

                    feature_active = (features > 0).float().sum(dim=0).cpu()
                    feature_counts += feature_active

                    n_tokens_total += acts_flat.shape[0]

                except Exception as e:
                    print(f"Warning: Error processing batch {i//batch_size}: {e}")
                    continue

            self.reset_model_state()

        if n_tokens_total == 0:
            raise RuntimeError("Failed to process any tokens")
        
        l0_mean = l0_sum / n_tokens_total
        l0_var = (l0_sq_sum / n_tokens_total) - (l0_mean ** 2)
        l0_std = np.sqrt(max(0, l0_var))

        l1_mean = l1_sum / n_tokens_total
        l1_var = (l1_sq_sum / n_tokens_total) - (l1_mean ** 2)
        l1_std = np.sqrt(max(0, l1_var))

        feature_freq = (feature_counts / n_tokens_total).tolist()

        metrics = {
            'l0_mean': l0_mean,
            'l0_std': l0_std,
            'l1_mean': l1_mean,
            'l1_std': l1_std,
            'n_features': self.sae.cfg.d_sae,
            'n_tokens': n_tokens_total
        }

        print(f"\n Sparsity Results:")
        print(f"  L0: {l0_mean:.2f} ± {l0_std:.2f} features/token")
        print(f"  L1: {l1_mean:.4f} ± {l1_std:.4f}")
        print(f"  Tokens processed: {n_tokens_total}")

        return metrics, feature_freq


    def find_dead_features(
        self,
        feature_freq: List[float],
        threshold: float = 0.0
    ) -> Dict[str, any]:
        """
        Identify features that rarely or never activate
        Returns dictionary with dead feature stats
        """
        feature_freq_tensor = torch.tensor(feature_freq)
        dead_mask = feature_freq_tensor < threshold

        n_dead = int(dead_mask.sum().item())
        pct_dead = 100 * dead_mask.float().mean().item()
        dead_indices = dead_mask.nonzero(as_tuple=True)[0].tolist()

        print(f"Dead feature threshold: {threshold}")
        print(f" {n_dead}/{len(feature_freq)} ({pct_dead:.1f}%) dead features")

        return {
            'n_dead': n_dead,
            'pct_dead': pct_dead,
            'dead_indices': dead_indices,
            'threshold': threshold
        }
    
    def compute_reconstruction_metrics(
        self,
        texts: Optional[List[str]] = None,
        batch_size: int = 8
    ) -> Dict[str, float]:
        """
        Measure how well SAE reconstructs original activations
        Returns dictionary with MSE, explained variance, cos similarity, etc.
        """
        if texts is None:
            texts = self.dataset
        
        # Validate texts
        texts = [t for t in texts if t and len(t.strip()) > 0]
        if len(texts) == 0:
            raise ValueError("No valid texts to process!")
        
        self.reset_model_state()

        pad_token_id = self.model.tokenizer.pad_token_id

        # Running stats
        mse_sum = 0.0
        original_var_sum = 0.0
        residual_var_sum = 0.0
        cos_sim_sum = 0.0
        n_tokens_total = 0

        for i in tqdm(range(0, len(texts), batch_size), desc='Reconstruction'):
            batch_texts = texts[i: i+batch_size]

            try:
                tokens = self.model.to_tokens(batch_texts, prepend_bos=True)
                tokens = tokens.to(self.device)

                if tokens.numel() == 0:
                    print(f"Warning: Batch {i//batch_size} produced no tokens, skipping...")
                    continue

            except Exception as e:
                print(f"Warning: Failed to tokenize batch {i//batch_size}: {e}")
                continue

            with torch.no_grad():
                try:
                    logits, cache = self.model.run_with_cache(
                        tokens,
                        names_filter=lambda name: name == self.hook_point
                    )
                    acts = cache[self.hook_point]
                    acts_flat = acts.reshape(-1, acts.shape[-1])
                    tokens_flat = tokens.reshape(-1)
                    non_padding_mask = tokens_flat != pad_token_id
                    acts_flat = acts_flat[non_padding_mask]
                    
                    if acts_flat.shape[0] == 0:
                        continue

                    # SAE reconstruction
                    x_recon, features = self.sae(acts_flat)

                    residual = acts_flat - x_recon
                    mse = (residual **2).mean().item()
                    mse_sum += mse * acts_flat.shape[0]

                    original_var_sum += acts_flat.var().item() * acts_flat.shape[0]
                    residual_var_sum += residual.var().item() * acts_flat.shape[0]

                    cos_sim = torch.nn.functional.cosine_similarity(
                        acts_flat, x_recon, dim=1
                    ).mean().item()
                    cos_sim_sum += cos_sim * acts_flat.shape[0]

                    n_tokens_total += acts_flat.shape[0]

                except Exception as e:
                    print(f"Warning: Error processing batch {i//batch_size}: {e}")
                    continue
            
            self.reset_model_state()
        
        if n_tokens_total == 0:
            raise RuntimeError("Failed to process any tokens")
        
        mse_avg = mse_sum / n_tokens_total
        original_var_avg = original_var_sum / n_tokens_total
        residual_var_avg = residual_var_sum / n_tokens_total
        cos_sim_avg = cos_sim_sum / n_tokens_total

        explained_var = 1.0 - (residual_var_avg / original_var_avg) if original_var_avg > 0 else 0.0

        metrics = {
            'mse': mse_avg,
            'explained_variance': explained_var,
            'cosine_similarity': cos_sim_avg,
            'original_std': np.sqrt(original_var_avg),
            'residual_std': np.sqrt(residual_var_avg),
            'n_tokens': n_tokens_total
        }

        print(f"\nReconstruction Results:")
        print(f"  MSE: {mse_avg:.6f}")
        print(f"  Explained Variance: {explained_var:.4f} ({explained_var*100:.2f}%)")
        print(f"  Cosine Similarity: {cos_sim_avg:.4f}")
        print(f"  Tokens processed: {n_tokens_total}")

        return metrics


    def ablation_study(
        self,
        texts: Optional[List[str]] = None,
        batch_size: int = 4
    ) -> Dict[str, float]:
        """
        Compare model performance under baseline, zero ablation, and sae reconstruction
        Returns dictionary with loss for each condition and recovered loss
        """
        if texts is None:
            texts = self.dataset
        
        # Validate texts
        texts = [t for t in texts if t and len(t.strip()) > 0]
        if len(texts) == 0:
            raise ValueError("No valid texts to process!")
        
        self.reset_model_state()

        # Get padding token for loss computation
        pad_token_id = self.model.tokenizer.pad_token_id
        if pad_token_id is None:
            pad_token_id = self.model.tokenizer.eos_token_id

        loss_baseline_sum = 0.0
        loss_zero_sum = 0.0
        loss_sae_sum = 0.0
        n_batches = 0

        for i in tqdm(range(0, len(texts), batch_size), desc="Ablation"):
            batch_texts = texts[i:i+batch_size]
            
            try:
                tokens = self.model.to_tokens(batch_texts, prepend_bos=True)
                tokens = tokens.to(self.device)
                
                if tokens.numel() == 0 or tokens.shape[1] < 2:
                    continue
                    
            except Exception as e:
                print(f"Warning: Failed to tokenize batch {i//batch_size}: {e}")
                continue
            
            with torch.no_grad():
                try:
                    # 1. Baseline: Original model (no intervention)
                    self.reset_model_state()
                    logits_baseline = self.model(tokens)
                    loss_baseline = self.compute_ce_loss(logits_baseline, tokens, pad_token_id)
                    
                    # 2. Zero ablation: Replace with zeros
                    self.reset_model_state()
                    def zero_hook(acts, hook):
                        return torch.zeros_like(acts)
                    
                    logits_zero = self.model.run_with_hooks(
                        tokens,
                        fwd_hooks=[(self.hook_point, zero_hook)],
                        reset_hooks_end=True
                    )
                    loss_zero = self.compute_ce_loss(logits_zero, tokens, pad_token_id)
                    
                    # 3. SAE reconstruction: Replace with SAE output
                    self.reset_model_state()
                    def sae_hook(acts, hook):
                        x_recon, features = self.sae(acts)
                        return x_recon
                    
                    logits_sae = self.model.run_with_hooks(
                        tokens,
                        fwd_hooks=[(self.hook_point, sae_hook)],
                        reset_hooks_end=True
                    )
                    loss_sae = self.compute_ce_loss(logits_sae, tokens, pad_token_id)
                    
                    # Accumulate losses
                    loss_baseline_sum += loss_baseline.item()
                    loss_zero_sum += loss_zero.item()
                    loss_sae_sum += loss_sae.item()
                    n_batches += 1
                    
                    # Sanity check: baseline should have lowest loss
                    if loss_baseline.item() > loss_zero.item():
                        print(f"\nWARNING: Baseline loss > Zero ablation loss!")
                    
                except Exception as e:
                    print(f"Warning: Error processing batch {i//batch_size}: {e}")
                    continue
            
            self.reset_model_state()
        
        if n_batches == 0:
            raise RuntimeError("Failed to process any batches!")
        
        # Compute averages
        loss_baseline_avg = loss_baseline_sum / n_batches
        loss_zero_avg = loss_zero_sum / n_batches
        loss_sae_avg = loss_sae_sum / n_batches
        
        # Calculate "loss recovered"
        loss_increase_zero = loss_zero_avg - loss_baseline_avg
        loss_increase_sae = loss_sae_avg - loss_baseline_avg
        
        if loss_increase_zero > 0:
            loss_recovered = 1.0 - (loss_increase_sae / loss_increase_zero)
        else:
            loss_recovered = float('nan')
            print("\nWARNING: Zero ablation did not increase loss!")
        
        metrics = {
            'baseline_loss': loss_baseline_avg,
            'zero_ablation_loss': loss_zero_avg,
            'sae_reconstruction_loss': loss_sae_avg,
            'loss_recovered': loss_recovered,
            'n_batches': n_batches
        }
        
        print(f"\nAblation Study Results:")
        print(f"  Baseline Loss:      {loss_baseline_avg:.4f}")
        print(f"  Zero Ablation:      {loss_zero_avg:.4f} (+{loss_increase_zero:.4f})")
        print(f"  SAE Reconstruction: {loss_sae_avg:.4f} (+{loss_increase_sae:.4f})")
        print(f"  Loss Recovered:     {loss_recovered*100:.2f}%")
        print(f"  Batches processed:  {n_batches}")
        
        return metrics
    

    def compute_ce_loss(
        self,
        logits: torch.Tensor,
        tokens: torch.Tensor,
        pad_token_id: int
    ) -> torch.Tensor:
        """Compute cross entropy loss for next-token prediction"""
        # Shift logits and tokens for next-token prediction
        logits = logits[:, :-1, :]  # Remove last token
        targets = tokens[:, 1:] # Remove first token (BOS)

        # Flatten for loss computation
        logits_flat = logits.reshape(-1, logits.shape[-1])
        targets_flat = targets.reshape(-1)

        loss = torch.nn.functional.cross_entropy(
            logits_flat,
            targets_flat,
            ignore_index=pad_token_id,
            reduction='mean'
        )

        return loss
    
    def find_max_activating_examples(
    self,
    feature_idx: int,
    top_k: int = 10,
    context_size: int = 10
) -> List[Dict[str, any]]:
        """
        Find tokens/contexts that most strongly activate a feature.
        Uses pre-computed activation database if available.
        """
        if self.activation_db is None:
            raise ValueError(
                "Activation database not found. "
                "Run collect_all_activations() first"
            )
        
        # Get top-k activations (already sorted!)
        activations = self.activation_db.get_feature_activations(feature_idx, top_k=top_k)
        
        if len(activations) == 0:
            print(f"WARNING: No activations found for feature {feature_idx}")
            return []
        
        # Build results with context
        results = []
        for token_idx, activation_value in activations:
            context_info = self.activation_db.get_token_context(
                token_idx,
                self.model,
                context_size=context_size
            )
            
            results.append({
                'text': context_info['context'],
                'target_token': context_info['token'],
                'activation': activation_value,
                'position': context_info['position'],
                'batch_idx': context_info['text_idx']
            })
        
        print(f"\nFound top {len(results)} activating examples for feature {feature_idx}")
        print(f"  Max activation: {results[0]['activation']:.4f}")
        if len(results) > 0:
            print(f"  Min activation (in top-k): {results[-1]['activation']:.4f}")
        
        return results
    
    def compute_feature_cooccurrence(
    self,
    min_activation: float = 0.0,
    method: str = 'correlation',
    save_path: Optional[str] = None,
    chunk_size: int = 1000
) -> np.ndarray:
        """
        Compute feature co-occurrence matrix
        
        Args:
            min_activation: Threshold for considering a feature "active"
            method: 'correlation', 'jaccard', or 'pmi' (pointwise mutual information)
            save_path: Optional path to save the co-occurrence matrix
            chunk_size: Process features in chunks to manage memory
            
        Returns:
            Co-occurrence matrix [n_features x n_features]
        """
        if self.activation_db is None:
            raise ValueError("Must collect activations into db first")
        
        print(f"Computing feature co-occurrence using {method}")
        
        n_features = self.activation_db.activation_matrix.shape[1]
        n_tokens = self.activation_db.activation_matrix.shape[0]
        
        # Binarize the activation matrix (feature active or not)
        binary_matrix = (self.activation_db.activation_matrix > min_activation).astype(np.float32)
        
        if method == 'correlation':
            # Pearson correlation between feature activation patterns
            # For memory efficiency, compute in chunks
            print("Computing correlation matrix...")
            cooccurrence = np.zeros((n_features, n_features), dtype=np.float32)
            
            for i in tqdm(range(0, n_features, chunk_size), desc="Correlation chunks"):
                end_i = min(i + chunk_size, n_features)
                chunk = binary_matrix[:, i:end_i].toarray()
                
                # Compute correlation with all features
                for j in range(0, n_features, chunk_size):
                    end_j = min(j + chunk_size, n_features)
                    chunk_j = binary_matrix[:, j:end_j].toarray()
                    
                    # Compute correlation
                    cooccurrence[i:end_i, j:end_j] = np.corrcoef(
                        chunk.T, chunk_j.T
                    )[:chunk.shape[1], chunk.shape[1]:]
            
            # Handle NaNs (features that never activate)
            cooccurrence = np.nan_to_num(cooccurrence, nan=0.0)
            
        elif method == 'jaccard':
            # Jaccard similarity: |A ∩ B| / |A ∪ B|
            print("Computing Jaccard similarity...")
            cooccurrence = np.zeros((n_features, n_features), dtype=np.float32)
            
            for i in tqdm(range(n_features), desc="Jaccard similarity"):
                feature_i = binary_matrix[:, i].toarray().ravel()
                
                for j in range(i, n_features):
                    feature_j = binary_matrix[:, j].toarray().ravel()
                    
                    intersection = np.sum(feature_i * feature_j)
                    union = np.sum(np.maximum(feature_i, feature_j))
                    
                    if union > 0:
                        jaccard = intersection / union
                        cooccurrence[i, j] = jaccard
                        cooccurrence[j, i] = jaccard
        
        elif method == 'pmi':
            # Pointwise Mutual Information
            print("Computing PMI...")
            cooccurrence = np.zeros((n_features, n_features), dtype=np.float32)
            
            # Compute P(feature_i)
            p_features = np.array(binary_matrix.sum(axis=0)).ravel() / n_tokens
            
            for i in tqdm(range(n_features), desc="PMI"):
                feature_i = binary_matrix[:, i].toarray().ravel()
                
                for j in range(i, n_features):
                    feature_j = binary_matrix[:, j].toarray().ravel()
                    
                    # P(i and j)
                    p_ij = np.sum(feature_i * feature_j) / n_tokens
                    
                    if p_ij > 0 and p_features[i] > 0 and p_features[j] > 0:
                        pmi = np.log(p_ij / (p_features[i] * p_features[j]))
                        cooccurrence[i, j] = pmi
                        cooccurrence[j, i] = pmi
        
        else:
            raise ValueError(f"Unknown method: {method}")
        
        print(f"Computed {n_features}x{n_features} co-occurrence matrix")
        
        if save_path is not None:
            np.save(save_path, cooccurrence)
            print(f"Saved co-occurrence matrix to {save_path}")
        
        self.feature_cooccurrence = cooccurrence
        return cooccurrence


    def find_coactivating_features(
        self,
        feature_idx: int,
        top_k: int = 10,
        exclude_self: bool = True,
        min_cooccurrence: float = 0.0
    ) -> List[Tuple[int, float]]:
        """
        Find features that frequently co-activate with a given feature
        
        Returns:
            List of (feature_idx, cooccurrence_score) tuples
        """
        if not hasattr(self, 'feature_cooccurrence') or self.feature_cooccurrence is None:
            raise ValueError("Must call compute_feature_cooccurrence() first")
        
        cooccurrence = self.feature_cooccurrence[feature_idx]
        
        if exclude_self:
            cooccurrence = cooccurrence.copy()
            cooccurrence[feature_idx] = -np.inf
        
        # Filter by minimum co-occurrence
        valid_indices = np.where(cooccurrence > min_cooccurrence)[0]
        valid_scores = cooccurrence[valid_indices]
        
        # Get top k
        if len(valid_indices) > top_k:
            top_k_local_indices = np.argsort(valid_scores)[-top_k:][::-1]
            top_indices = valid_indices[top_k_local_indices]
            top_scores = valid_scores[top_k_local_indices]
        else:
            sorted_order = np.argsort(valid_scores)[::-1]
            top_indices = valid_indices[sorted_order]
            top_scores = valid_scores[sorted_order]
        
        return list(zip(top_indices.tolist(), top_scores.tolist()))


    def analyze_feature_clusters(
        self,
        feature_idx: int,
        top_k: int = 5,
        context_size: int = 10
    ):
        """
        Analyze a feature along with its co-activating features
        Shows examples where these features activate together
        """
        if self.activation_db is None:
            raise ValueError("Must collect activations into db first")
        if not hasattr(self, 'feature_cooccurrence') or self.feature_cooccurrence is None:
            raise ValueError("Must call compute_feature_cooccurrence() first")
        
        print(f"\n=== Feature Cluster Analysis for Feature {feature_idx} ===")
        
        # Get co-activating features
        coactivating = self.find_coactivating_features(feature_idx, top_k=top_k)
        
        print(f"\nTop {len(coactivating)} co-activating features:")
        for i, (feat_idx, score) in enumerate(coactivating, 1):
            freq = self.activation_db.feature_metadata['activation_counts'][feat_idx]
            print(f"{i}. Feature {feat_idx}: co-occurrence={score:.4f}, freq={freq}")
        
        # Find examples where multiple features activate together
        print(f"\nExamples where feature {feature_idx} co-activates with others:")
        
        # Get tokens where target feature activates
        activations = self.activation_db.get_feature_activations(feature_idx, top_k=20)
        
        for token_idx, act_val in activations[:10]:
            # Get all features active at this token
            token_features = self.activation_db.get_token_activations(token_idx, threshold=0.0)
            
            # Check which co-activating features are present
            coactivating_ids = {f[0] for f in coactivating}
            present_coactivations = [
                (f_idx, f_val) for f_idx, f_val in token_features 
                if f_idx in coactivating_ids
            ]
            
            if present_coactivations:
                context = self.activation_db.get_token_context(
                    token_idx, self.model, context_size=context_size
                )
                print(f"\n  Token: '{context['token']}' (activation: {act_val:.4f})")
                print(f"  Context: {context['context']}")
                print(f"  Co-active features: {[(f, round(v, 3)) for f, v in present_coactivations[:3]]}")

    def run_full_analysis(
        self,
        texts: Optional[List[str]] = None,
        batch_size: int = 8,
        save_path: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Run complete analysis suite and optionally save results
        
        Returns:
            Dictionary containing all analysis results
        """
        if texts is None:
            texts = self.dataset
        
        print(f"Running Full SAE Analysis")
        
        results = {}
        
        # 1. Sparsity metrics
        print(f"\nComputing Sparsity Metrics...")
        sparsity_metrics, feature_freq = self.compute_sparsity_metrics(
            texts, batch_size
        )
        results['sparsity'] = sparsity_metrics
        results['feature_freq'] = feature_freq
        
        # 2. Dead features
        print(f"\nIdentifying Dead Features...")
        dead_features = self.find_dead_features(feature_freq)
        results['dead_features'] = dead_features
        
        # 3. Reconstruction quality
        print(f"\nComputing Reconstruction Metrics...")
        recon_metrics = self.compute_reconstruction_metrics(texts, batch_size)
        results['reconstruction'] = recon_metrics
        
        # 4. Ablation study
        print(f"\nRunning Ablation Study...")
        ablation_metrics = self.ablation_study(texts, batch_size=4)
        results['ablation'] = ablation_metrics
        
        # Save if requested
        if save_path is not None:
            import json
            from pathlib import Path
            
            save_path = Path(save_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to JSON-serializable format
            results_json = {
                'sparsity': results['sparsity'],
                'dead_features': {
                    k: v for k, v in results['dead_features'].items()
                    if k != 'dead_indices'  # Can be very long
                },
                'reconstruction': results['reconstruction'],
                'ablation': results['ablation']
            }
            
            with open(save_path, 'w') as f:
                json.dump(results_json, f, indent=2)
            
            print(f"\nResults saved to {save_path}")
        
        print(f"Analysis Complete!")
        
        return results
    
    def plot_activation_distribution(
        self,
        feature_idx: int,
        save_path: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 6)
    ):
        """
        Plot the distribution of activation values for a specific feature
        """
        if self.activation_db is None:
            raise ValueError("Must collect activations into db first")
        
        activations = self.activation_db.get_feature_activations(feature_idx)
        
        if len(activations) == 0:
            print(f"Feature {feature_idx} never activated")
            return
        
        activation_values = [act_val for _, act_val in activations]
        
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Histogram
        axes[0].hist(activation_values, bins=50, alpha=0.7, edgecolor='black')
        axes[0].set_xlabel('Activation Value')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title(f'Feature {feature_idx} Activation Distribution')
        axes[0].grid(True, alpha=0.3)
        
        # Box plot
        axes[1].boxplot(activation_values, vert=True)
        axes[1].set_ylabel('Activation Value')
        axes[1].set_title(f'Feature {feature_idx} Activation Statistics')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved plot to {save_path}")
        
        plt.show()


    def plot_feature_similarity_heatmap(
        self,
        feature_indices: Optional[List[int]] = None,
        top_k: int = 50,
        save_path: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 10),
        cmap: str = 'RdBu_r'
    ):
        """
        Plot heatmap of feature similarity matrix
        
        Args:
            feature_indices: Specific features to plot, or None for top-k most active
            top_k: Number of features to plot if feature_indices is None
        """
        if self.feature_similarity is None:
            raise ValueError("Must call compute_feature_similarity() first")
        
        # Select features to plot
        if feature_indices is None:
            # Use top-k most frequently activating features
            if self.activation_db is None:
                feature_indices = list(range(min(top_k, self.feature_similarity.shape[0])))
            else:
                freq = self.activation_db.feature_metadata['activation_counts']
                feature_indices = np.argsort(freq)[-top_k:].tolist()
        
        # Extract submatrix
        similarity_subset = self.feature_similarity[np.ix_(feature_indices, feature_indices)]
        
        # Plot
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.heatmap(
            similarity_subset,
            xticklabels=feature_indices,
            yticklabels=feature_indices,
            cmap=cmap,
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"label": "Similarity"},
            ax=ax
        )
        
        ax.set_title(f'Feature Similarity Heatmap (Top {len(feature_indices)} Features)')
        ax.set_xlabel('Feature Index')
        ax.set_ylabel('Feature Index')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved heatmap to {save_path}")
        
        plt.show()


    def plot_cooccurrence_heatmap(
        self,
        feature_indices: Optional[List[int]] = None,
        top_k: int = 50,
        save_path: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 10)
    ):
        """
        Plot heatmap of feature co-occurrence matrix
        """
        if not hasattr(self, 'feature_cooccurrence') or self.feature_cooccurrence is None:
            raise ValueError("Must call compute_feature_cooccurrence() first")
        
        # Select features
        if feature_indices is None:
            if self.activation_db is None:
                feature_indices = list(range(min(top_k, self.feature_cooccurrence.shape[0])))
            else:
                freq = self.activation_db.feature_metadata['activation_counts']
                feature_indices = np.argsort(freq)[-top_k:].tolist()
        
        # Extract submatrix
        cooccurrence_subset = self.feature_cooccurrence[np.ix_(feature_indices, feature_indices)]
        
        # Plot
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.heatmap(
            cooccurrence_subset,
            xticklabels=feature_indices,
            yticklabels=feature_indices,
            cmap='YlOrRd',
            square=True,
            linewidths=0.5,
            cbar_kws={"label": "Co-occurrence Score"},
            ax=ax
        )
        
        ax.set_title(f'Feature Co-occurrence Heatmap (Top {len(feature_indices)} Features)')
        ax.set_xlabel('Feature Index')
        ax.set_ylabel('Feature Index')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved heatmap to {save_path}")
        
        plt.show()


    def plot_sparsity_distribution(
        self,
        metrics: Dict[str, float],
        feature_freq: List[float],
        save_path: Optional[str] = None,
        figsize: Tuple[int, int] = (15, 5)
    ):
        """
        Visualize sparsity metrics and feature frequency distribution
        """
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        
        # 1. Feature frequency distribution
        axes[0].hist(feature_freq, bins=50, alpha=0.7, edgecolor='black')
        axes[0].set_xlabel('Activation Frequency')
        axes[0].set_ylabel('Number of Features')
        axes[0].set_title('Feature Activation Frequency Distribution')
        axes[0].set_yscale('log')
        axes[0].grid(True, alpha=0.3)
        
        # 2. L0 summary
        l0_data = [metrics['l0_mean']]
        axes[1].bar(['L0'], l0_data, alpha=0.7, color='skyblue', edgecolor='black')
        axes[1].errorbar(['L0'], l0_data, yerr=[metrics['l0_std']], 
                        fmt='none', color='black', capsize=5)
        axes[1].set_ylabel('Features per Token')
        axes[1].set_title(f"L0: {metrics['l0_mean']:.2f} ± {metrics['l0_std']:.2f}")
        axes[1].grid(True, alpha=0.3, axis='y')
        
        # 3. Dead features
        active_features = np.sum(np.array(feature_freq) > 0.001)
        dead_features = len(feature_freq) - active_features
        
        axes[2].pie(
            [active_features, dead_features],
            labels=['Active', 'Dead'],
            autopct='%1.1f%%',
            colors=['lightgreen', 'lightcoral'],
            startangle=90
        )
        axes[2].set_title(f'Feature Usage\n(threshold=0.0)')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved plot to {save_path}")
        
        plt.show()


    def plot_reconstruction_quality(
        self,
        metrics: Dict[str, float],
        save_path: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 4)
    ):
        """
        Visualize reconstruction quality metrics
        """
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        
        # 1. MSE
        axes[0].bar(['MSE'], [metrics['mse']], alpha=0.7, color='salmon', edgecolor='black')
        axes[0].set_ylabel('Mean Squared Error')
        axes[0].set_title(f"Reconstruction MSE\n{metrics['mse']:.6f}")
        axes[0].grid(True, alpha=0.3, axis='y')
        
        # 2. Explained Variance
        axes[1].barh(['Original\nVariance', 'Residual\nVariance'], 
                    [1.0, 1.0 - metrics['explained_variance']],
                    alpha=0.7, color=['skyblue', 'lightcoral'], edgecolor='black')
        axes[1].set_xlabel('Proportion of Variance')
        axes[1].set_title(f"Explained Variance: {metrics['explained_variance']*100:.2f}%")
        axes[1].grid(True, alpha=0.3, axis='x')
        
        # 3. Cosine Similarity
        angles = np.linspace(0, 2*np.pi, 100)
        cos_sim = metrics['cosine_similarity']
        
        ax = plt.subplot(133, projection='polar')
        ax.fill_between(angles, 0, cos_sim, alpha=0.3, color='green')
        ax.plot(angles, [cos_sim]*len(angles), color='green', linewidth=2)
        ax.set_ylim(0, 1)
        ax.set_title(f"Cosine Similarity\n{cos_sim:.4f}", pad=20)
        ax.set_rticks([0.25, 0.5, 0.75, 1.0])
        ax.grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved plot to {save_path}")
        
        plt.show()


    def create_feature_dashboard(
        self,
        feature_idx: int,
        save_path: Optional[str] = None,
        figsize: Tuple[int, int] = (16, 10)
    ):
        """
        Create a comprehensive dashboard for a single feature showing:
        - Activation distribution
        - Top activating examples
        - Similar features
        - Co-activating features
        """
        if self.activation_db is None:
            raise ValueError("Must collect activations first")
        
        fig = plt.figure(figsize=figsize)
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 1. Feature stats
        ax1 = fig.add_subplot(gs[0, :])
        ax1.axis('off')
        
        freq = self.activation_db.feature_metadata['activation_counts'][feature_idx]
        mean_act = self.activation_db.feature_metadata['mean_activation'][feature_idx]
        pct = freq / self.activation_db.feature_metadata['n_tokens'] * 100
        
        stats_text = f"""
        Feature {feature_idx} Overview
        
        Activation Frequency: {freq:,} tokens ({pct:.2f}%)
        Mean Activation: {mean_act:.4f}
        """
        ax1.text(0.5, 0.5, stats_text, ha='center', va='center', 
                fontsize=14, family='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # 2. Activation distribution
        ax2 = fig.add_subplot(gs[1, 0])
        activations = self.activation_db.get_feature_activations(feature_idx)
        if activations:
            activation_values = [act_val for _, act_val in activations]
            ax2.hist(activation_values, bins=30, alpha=0.7, edgecolor='black')
            ax2.set_xlabel('Activation Value')
            ax2.set_ylabel('Count')
            ax2.set_title('Activation Distribution')
            ax2.grid(True, alpha=0.3)
        
        # 3. Top examples
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.axis('off')
        
        top_examples = []
        for token_idx, act_val in activations[:5]:
            context = self.activation_db.get_token_context(token_idx, self.model, context_size=5)
            top_examples.append(f"'{context['token']}' ({act_val:.3f})")
        
        examples_text = "Top Activating Tokens:\n\n" + "\n".join(top_examples)
        ax3.text(0.1, 0.9, examples_text, ha='left', va='top',
                fontsize=10, family='monospace',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        
        # 4. Similar features (if available)
        if self.feature_similarity is not None:
            ax4 = fig.add_subplot(gs[2, 0])
            similar = self.find_similar_features(feature_idx, top_k=10)
            if similar:
                feat_ids, similarities = zip(*similar)
                ax4.barh(range(len(feat_ids)), similarities, alpha=0.7, edgecolor='black')
                ax4.set_yticks(range(len(feat_ids)))
                ax4.set_yticklabels([f"F{f}" for f in feat_ids])
                ax4.set_xlabel('Similarity Score')
                ax4.set_title('Most Similar Features')
                ax4.grid(True, alpha=0.3, axis='x')
        
        # 5. Co-activating features (if available)
        if hasattr(self, 'feature_cooccurrence') and self.feature_cooccurrence is not None:
            ax5 = fig.add_subplot(gs[2, 1])
            coactivating = self.find_coactivating_features(feature_idx, top_k=10)
            if coactivating:
                feat_ids, scores = zip(*coactivating)
                ax5.barh(range(len(feat_ids)), scores, alpha=0.7, 
                        edgecolor='black', color='orange')
                ax5.set_yticks(range(len(feat_ids)))
                ax5.set_yticklabels([f"F{f}" for f in feat_ids])
                ax5.set_xlabel('Co-occurrence Score')
                ax5.set_title('Co-activating Features')
                ax5.grid(True, alpha=0.3, axis='x')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved dashboard to {save_path}")
        
        plt.show()