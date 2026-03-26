import json
import pickle
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
from numpy.lib.format import open_memmap
from scipy import sparse
from tqdm import tqdm
from transformer_lens import HookedTransformer

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
        feature_metadata: Dict[str, Any]
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
    ) -> Dict[str, Any]:
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
        self.pad_token_id = self._resolve_pad_token_id()

    def reset_model_state(self):
        """Clear all hooks and GPU cache"""
        self.model.reset_hooks()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def _resolve_pad_token_id(self) -> int:
        token_id = self.model.tokenizer.pad_token_id
        if token_id is None:
            token_id = self.model.tokenizer.eos_token_id
        if token_id is None:
            raise ValueError("Tokenizer must provide a pad_token_id or eos_token_id")
        return token_id

    def _prepare_square_matrix(self, n_features: int, save_path: Optional[str], filename_prefix: str):
        """Allocate on-disk storage for large NxN matrices."""
        if save_path is None:
            tmp_dir = Path(tempfile.mkdtemp())
            save_path = tmp_dir / f"{filename_prefix}.npy"
        else:
            save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        matrix = open_memmap(save_path, mode='w+', dtype=np.float32, shape=(n_features, n_features))
        return matrix, save_path

    def _encode_sparse_features(self, acts: torch.Tensor) -> torch.Tensor:
        """
        Encode activations using the SAE, returning the sparse feature activations
        in the same way the SAE is used during forward passes.
        """
        sae_dtype = getattr(self.sae, "dtype", acts.dtype)
        x = acts.to(sae_dtype)
        if hasattr(self.sae, "b_dec"):
            x = x - self.sae.b_dec

        dense = self.sae.encode(x)

        # BatchTopKSAE-style sparsification
        if hasattr(self.sae, "top_k") and self.sae.top_k is not None:
            added_seq_dim = False
            if dense.ndim == 2:
                dense = dense.unsqueeze(1)
                added_seq_dim = True

            orig_shape = dense.shape  # [B, S, d_sae]
            flat = dense.reshape(-1)

            n_tokens = orig_shape[0] * orig_shape[1]
            k_total = min(n_tokens * int(self.sae.top_k), flat.numel())

            sparse_flat = torch.zeros_like(flat)
            if k_total > 0:
                values, indices = torch.topk(flat, k_total, dim=0)
                sparse_flat[indices] = values
            sparse = sparse_flat.view(orig_shape)
            if added_seq_dim:
                sparse = sparse.squeeze(1)
        else:
            sparse = dense

        return sparse.to(torch.float32)
    
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

        token_metadata = []
        global_token_idx = 0
        csr_indices: List[int] = []
        csr_data: List[float] = []
        csr_indptr = [0]

        # Track padding tokens
        padding_tokens_skipped = 0
        pad_token_id = self.pad_token_id
        print(f"Pad token ID: {pad_token_id}")

        # Feature statistics
        feature_activation_counts = torch.zeros(self.sae.cfg.d_sae, dtype=torch.int64)
        feature_total_activation = torch.zeros(self.sae.cfg.d_sae, dtype=torch.float64)
        ever_fired_mask = torch.zeros(self.sae.cfg.d_sae, dtype=torch.bool)

        print(f"Collecting activations from {len(texts)} texts")

        for text_idx in tqdm(range(0, len(texts), batch_size), desc="Processing"):
            batch_texts = texts[text_idx: text_idx+batch_size]

            try:
                tokens = self.model.to_tokens(batch_texts, prepend_bos=False)
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

                    batch_size, seq_len, _ = acts.shape
                    acts_flat = acts.reshape(-1, acts.shape[-1])
                    tokens_flat = tokens.reshape(-1)
                    pad_mask = tokens_flat == pad_token_id
                    padding_tokens_skipped += pad_mask.sum().item()
                    non_pad_mask = ~pad_mask

                    if non_pad_mask.sum().item() == 0:
                        continue

                    valid_tokens = tokens_flat[non_pad_mask]
                    valid_acts = acts_flat[non_pad_mask]
                    features = self._encode_sparse_features(valid_acts)
                    features_cpu = features.detach().cpu()
                    valid_tokens_cpu = valid_tokens.detach().cpu()

                    batch_active_mask = features_cpu > activation_threshold
                    feature_activation_counts += batch_active_mask.sum(dim=0).to(feature_activation_counts.dtype)
                    feature_total_activation += (features_cpu * batch_active_mask).sum(dim=0).to(feature_total_activation.dtype)
                    ever_fired_mask |= batch_active_mask.any(dim=0)

                    valid_indices = non_pad_mask.nonzero(as_tuple=False).squeeze(-1)

                    for local_idx, flat_idx in enumerate(valid_indices.tolist()):
                        batch_idx = flat_idx // seq_len
                        pos = flat_idx % seq_len
                        text_global_idx = text_idx + batch_idx

                        token_value = valid_tokens_cpu[local_idx].item()
                        if token_value == pad_token_id:
                            padding_tokens_skipped += 1
                            continue

                        token_tensor = tokens[batch_idx, pos].detach().cpu()
                        token_str = self.model.to_string(token_tensor)

                        metadata = TokenMetadata(
                            global_idx=global_token_idx,
                            text_idx=text_global_idx,
                            position=pos,
                            token_id=int(token_value),
                            token_str=token_str
                        )
                        token_metadata.append(metadata)

                        active_features = batch_active_mask[local_idx].nonzero(as_tuple=True)[0]
                        if active_features.numel() > 0:
                            active_values = features_cpu[local_idx, active_features]
                            csr_indices.extend(active_features.tolist())
                            csr_data.extend(active_values.tolist())
                        csr_indptr.append(len(csr_indices))

                        global_token_idx += 1

                except Exception as e:
                    print(f"Error processing batch {text_idx//batch_size}: {e}")
                    continue

            self.reset_model_state()

        print(f"Processed {global_token_idx} tokens")
        print(f"Padding tokens skipped: {padding_tokens_skipped}")
        non_zero_acts = len(csr_data)
        print(f"Collected {non_zero_acts} non-zero activations")

        if global_token_idx == 0:
            raise RuntimeError("No valid tokens collected for activation DB")

        activation_matrix = sparse.csr_matrix(
            (
                np.array(csr_data, dtype=np.float32),
                np.array(csr_indices, dtype=np.int32),
                np.array(csr_indptr, dtype=np.int64),
            ),
            shape=(global_token_idx, self.sae.cfg.d_sae)
        )

        mean_activation = torch.zeros_like(feature_total_activation, dtype=torch.float64)
        nonzero_mask = feature_activation_counts > 0
        mean_activation[nonzero_mask] = feature_total_activation[nonzero_mask] / feature_activation_counts[nonzero_mask].clamp(min=1)

        feature_metadata = {
            'n_features': self.sae.cfg.d_sae,
            'n_tokens': global_token_idx,
            'activation_counts': feature_activation_counts.tolist(),
            'total_activations': feature_total_activation.tolist(),
            'mean_activation': mean_activation.tolist(),
            'sparsity': 1.0 - (non_zero_acts / (global_token_idx * self.sae.cfg.d_sae)),
            'ever_fired': ever_fired_mask.tolist(),
            'activation_threshold': activation_threshold
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
        similarity_metric: str = 'cosine',
        chunk_size: int = 1024
    ) -> np.ndarray:
        """
        Compute pairwise similarity between SAE features based on decoder weights
        without materializing the full matrix in memory.
        """
        print(f"Computing feature similarity using {similarity_metric} (chunk_size={chunk_size})")

        decoder = self.sae.W_dec.detach().float().cpu()
        n_features = decoder.shape[0]

        if similarity_metric == 'cosine':
            decoder = decoder / (decoder.norm(dim=1, keepdim=True) + 1e-8)
        elif similarity_metric == 'euclidean':
            decoder_norm_sq = (decoder ** 2).sum(dim=1, keepdim=True)
        elif similarity_metric != 'dot':
            raise ValueError(f"Unknown similarity metric: {similarity_metric}")

        storage, storage_path = self._prepare_square_matrix(
            n_features,
            save_path,
            filename_prefix='feature_similarity'
        )

        decoder_t = decoder.T.contiguous()
        iterator = range(0, n_features, chunk_size)
        iterator = tqdm(iterator, desc="Similarity chunks") if n_features > chunk_size else iterator

        for start in iterator:
            end = min(start + chunk_size, n_features)
            block = decoder[start:end]
            if similarity_metric in ('cosine', 'dot'):
                sims = block @ decoder_t
            else:  # euclidean
                block_sq = decoder_norm_sq[start:end]
                distances = block_sq + decoder_norm_sq.T - 2 * (block @ decoder_t)
                sims = -torch.sqrt(torch.clamp(distances, min=0.0))
            storage[start:end, :] = sims.numpy()

        storage.flush()
        print(f"Computed {n_features}x{n_features} similarity matrix")
        print(f"Similarity matrix stored at {storage_path}")

        self.feature_similarity = storage
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

        pad_token_id = self.pad_token_id

        # Running stats
        l0_sum = 0.0
        l0_sq_sum = 0.0
        l1_sum = 0.0
        l1_sq_sum = 0.0
        feature_counts = torch.zeros(self.sae.cfg.d_sae, device='cpu', dtype=torch.float64)
        ever_fired = torch.zeros(self.sae.cfg.d_sae, device='cpu', dtype=torch.bool)
        n_tokens_total = 0

        for i in tqdm(range(0, len(texts), batch_size), desc="Sparsity"):
            batch_texts = texts[i:i+batch_size]

            try:
                tokens = self.model.to_tokens(batch_texts, prepend_bos=False)
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

                    features = self._encode_sparse_features(acts_flat)
                    active_mask = features > 0

                    l0_per_token = active_mask.sum(dim=1).to(torch.float64)
                    l0_sum += l0_per_token.sum().item()
                    l0_sq_sum += (l0_per_token ** 2).sum().item()

                    l1_per_token = features.abs().sum(dim=1).to(torch.float64)
                    l1_sum += l1_per_token.sum().item()
                    l1_sq_sum += (l1_per_token ** 2).sum().item()

                    feature_active = active_mask.sum(dim=0).cpu().to(torch.float64)
                    feature_counts += feature_active
                    ever_fired |= active_mask.any(dim=0).cpu()

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
        self.feature_activation_mask = ever_fired

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
        threshold: float = 0.0,
        use_training_metric: bool = False
    ) -> Dict[str, Any]:
        """
        Identify features that rarely or never activate
        Returns dictionary with dead feature stats
        """
        if use_training_metric:
            if hasattr(self, "feature_activation_mask"):
                dead_mask = ~self.feature_activation_mask
            elif self.activation_db is not None and 'ever_fired' in self.activation_db.feature_metadata:
                dead_mask = ~torch.tensor(self.activation_db.feature_metadata['ever_fired'], dtype=torch.bool)
            else:
                dead_mask = torch.tensor(feature_freq) < threshold
        else:
            dead_mask = torch.tensor(feature_freq) < threshold

        n_dead = int(dead_mask.sum().item())
        pct_dead = 100 * (n_dead / len(feature_freq) if len(feature_freq) else 0.0)
        dead_indices = dead_mask.nonzero(as_tuple=True)[0].tolist()

        print(f"Dead feature threshold: {threshold}")
        print(f" {n_dead}/{len(feature_freq)} ({pct_dead:.1f}%) dead features")

        return {
            'n_dead': n_dead,
            'pct_dead': pct_dead,
            'dead_indices': dead_indices,
            'threshold': threshold,
            'use_training_metric': use_training_metric
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

        pad_token_id = self.pad_token_id

        # Running stats
        mse_sum = 0.0
        original_var_sum = 0.0
        residual_var_sum = 0.0
        cos_sim_sum = 0.0
        n_tokens_total = 0

        for i in tqdm(range(0, len(texts), batch_size), desc='Reconstruction'):
            batch_texts = texts[i: i+batch_size]

            try:
                tokens = self.model.to_tokens(batch_texts, prepend_bos=False)
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
                    x_recon, _ = self.sae(acts_flat)
                    acts_metrics = acts_flat.to(torch.float32)
                    x_recon = x_recon.to(torch.float32)

                    residual = acts_metrics - x_recon
                    mse = (residual **2).mean().item()
                    mse_sum += mse * acts_metrics.shape[0]

                    original_var_sum += acts_metrics.var().item() * acts_metrics.shape[0]
                    residual_var_sum += residual.var().item() * acts_metrics.shape[0]

                    cos_sim = torch.nn.functional.cosine_similarity(
                        acts_metrics, x_recon, dim=1
                    ).mean().item()
                    cos_sim_sum += cos_sim * acts_metrics.shape[0]

                    n_tokens_total += acts_metrics.shape[0]

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
        pad_token_id = self.pad_token_id

        loss_baseline_sum = 0.0
        loss_zero_sum = 0.0
        loss_sae_sum = 0.0
        n_batches = 0

        for i in tqdm(range(0, len(texts), batch_size), desc="Ablation"):
            batch_texts = texts[i:i+batch_size]
            
            try:
                tokens = self.model.to_tokens(batch_texts, prepend_bos=False)
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
                        x_recon, _ = self.sae(acts)
                        return x_recon.to(dtype=acts.dtype)
                    
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
    ) -> List[Dict[str, Any]]:
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
        chunk_size: int = 512
    ) -> np.ndarray:
        """Compute feature co-occurrence matrix in chunks to limit memory usage."""
        if self.activation_db is None:
            raise ValueError("Must collect activations into db first")

        print(f"Computing feature co-occurrence using {method} (chunk_size={chunk_size})")

        activation_matrix = self.activation_db.activation_matrix.copy().astype(np.float32)
        n_tokens, n_features = activation_matrix.shape

        if min_activation > 0:
            mask = activation_matrix.data > min_activation
            activation_matrix.data = mask.astype(np.float32)
            activation_matrix.eliminate_zeros()
        else:
            activation_matrix.data = np.ones_like(activation_matrix.data, dtype=np.float32)

        feature_counts = np.asarray(activation_matrix.sum(axis=0)).ravel()
        probs = feature_counts / max(n_tokens, 1)
        denom_all = np.sqrt(np.clip(probs * (1 - probs), 1e-12, None))

        storage, storage_path = self._prepare_square_matrix(
            n_features,
            save_path,
            filename_prefix='feature_cooccurrence'
        )

        iterator = range(0, n_features, chunk_size)
        iterator = tqdm(iterator, desc="Cooccurrence chunks") if n_features > chunk_size else iterator

        for start in iterator:
            end = min(start + chunk_size, n_features)
            chunk = activation_matrix[:, start:end]
            joint_counts = chunk.transpose().dot(activation_matrix).toarray()

            if method == 'correlation':
                joint = joint_counts / max(n_tokens, 1)
                numer = joint - probs[start:end][:, None] * probs[None, :]
                denom = denom_all[start:end][:, None] * denom_all[None, :]
                block = np.divide(numer, denom + 1e-8, out=np.zeros_like(numer), where=denom > 0)
            elif method == 'jaccard':
                unions = (
                    feature_counts[start:end][:, None] + feature_counts[None, :] - joint_counts
                )
                block = np.divide(
                    joint_counts,
                    unions,
                    out=np.zeros_like(joint_counts),
                    where=unions > 0
                )
            elif method == 'pmi':
                joint = joint_counts / max(n_tokens, 1)
                denom = probs[start:end][:, None] * probs[None, :]
                ratio = np.divide(
                    joint,
                    denom + 1e-12,
                    out=np.zeros_like(joint),
                    where=denom > 0
                )
                block = np.log(np.clip(ratio, 1e-12, None))
            else:
                raise ValueError(f"Unknown method: {method}")

            storage[start:end, :] = block.astype(np.float32)

        storage.flush()
        print(f"Computed {n_features}x{n_features} co-occurrence matrix")
        print(f"Co-occurrence matrix stored at {storage_path}")

        self.feature_cooccurrence = storage
        return self.feature_cooccurrence


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

    def generate_feature_summaries(
        self,
        save_path: str,
        top_k: int = 25,
        context_size: int = 10,
        min_activation: float = 0.0,
        max_features: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Create JSONL feature summaries with top activating examples for each feature.
        """
        if self.activation_db is None:
            raise ValueError("Must collect activations into db first")

        n_features = self.activation_db.activation_matrix.shape[1]
        activation_counts = self.activation_db.feature_metadata.get('activation_counts', [0] * n_features)
        mean_activation = self.activation_db.feature_metadata.get('mean_activation', [0.0] * n_features)

        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        summaries = []
        with open(save_path, "w") as f:
            iterator = range(n_features)
            iterator = tqdm(iterator, desc="Feature summaries") if n_features > 100 else iterator
            for feature_idx in iterator:
                freq = activation_counts[feature_idx]
                if freq <= 0:
                    continue

                activations = self.activation_db.get_feature_activations(feature_idx, top_k=top_k)
                if min_activation > 0:
                    activations = [(t_idx, val) for t_idx, val in activations if val >= min_activation]
                if len(activations) == 0:
                    continue

                examples = []
                for token_idx, act_val in activations[:top_k]:
                    context = self.activation_db.get_token_context(
                        token_idx,
                        self.model,
                        context_size=context_size
                    )
                    examples.append({
                        'token': context['token'],
                        'activation': float(act_val),
                        'context': context['context'],
                        'position': context['position'],
                        'text_idx': context['text_idx'],
                        'global_idx': context['global_idx']
                    })

                summary = {
                    'feature': feature_idx,
                    'activation_frequency': float(freq),
                    'mean_activation': float(mean_activation[feature_idx]),
                    'top_examples': examples
                }
                f.write(json.dumps(summary) + "\n")
                summaries.append(summary)

                if max_features is not None and len(summaries) >= max_features:
                    break

        print(f"Saved feature summaries for {len(summaries)} features to {save_path}")
        return summaries

    def run_full_analysis(
        self,
        texts: Optional[List[str]] = None,
        batch_size: int = 8,
        save_path: Optional[str] = None,
        feature_summary_path: Optional[str] = None,
        feature_summary_top_k: int = 25,
        use_training_dead_metric: bool = False
    ) -> Dict[str, Any]:
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
        dead_features = self.find_dead_features(
            feature_freq,
            use_training_metric=use_training_dead_metric
        )
        results['dead_features'] = dead_features
        
        # 3. Reconstruction quality
        print(f"\nComputing Reconstruction Metrics...")
        recon_metrics = self.compute_reconstruction_metrics(texts, batch_size)
        results['reconstruction'] = recon_metrics
        
        # 4. Ablation study
        print(f"\nRunning Ablation Study...")
        ablation_metrics = self.ablation_study(texts, batch_size=4)
        results['ablation'] = ablation_metrics

        # 5. Optional feature summaries (requires activation DB)
        if feature_summary_path is not None:
            if self.activation_db is None:
                raise ValueError("Activation DB required to generate feature summaries. Run collect_all_activations first.")
            self.generate_feature_summaries(
                feature_summary_path,
                top_k=feature_summary_top_k
            )
            results['feature_summaries'] = feature_summary_path
        
        # Save if requested
        if save_path is not None:
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
            if 'feature_summaries' in results:
                results_json['feature_summaries'] = results['feature_summaries']
            
            with open(save_path, 'w') as f:
                json.dump(results_json, f, indent=2)
            
            print(f"\nResults saved to {save_path}")
        
        print(f"Analysis Complete!")
        
        return results
