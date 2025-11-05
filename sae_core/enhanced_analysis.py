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

from sae_core.pretrained import load_pretrained


@dataclass
class TokenMetadata:
    """Metadata for each token in the corpus"""
    global_idx: int          # Global index across entire corpus
    text_idx: int            # Which text in the dataset
    position: int            # Position within that text
    token_id: int           # Actual token ID
    token_str: str          # String representation


class ActivationDatabase:
    """
    Stores comprehensive activation data for the entire corpus
    
    Structure:
    - activation_matrix: Sparse [n_tokens x n_features] matrix
    - token_metadata: List of TokenMetadata for each token
    - feature_metadata: Dictionary with feature statistics
    """
    
    def __init__(
        self,
        activation_matrix: sparse.csr_matrix,
        token_metadata: List[TokenMetadata],
        feature_metadata: Dict[str, any]
    ):
        self.activation_matrix = activation_matrix
        self.token_metadata = token_metadata
        self.feature_metadata = feature_metadata
        
        # Build reverse indices for fast lookup
        self._build_indices()
    
    def _build_indices(self):
        """Build reverse lookup structures"""
        # Feature -> list of token indices where it activated
        self.feature_to_tokens = {}
        
        print("Building feature activation index...")
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
    ) -> List[Tuple[int, float]]:
        """
        Get all tokens where a feature activated
        
        Returns:
            List of (token_idx, activation_value) tuples, sorted by activation
        """
        if feature_idx not in self.feature_to_tokens:
            return []
        
        token_indices = self.feature_to_tokens[feature_idx]
        activations = []
        
        for token_idx in token_indices:
            act_val = self.activation_matrix[token_idx, feature_idx]
            activations.append((token_idx, act_val))
        
        # Sort by activation value (descending)
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
        
        Returns:
            List of (feature_idx, activation_value) tuples
        """
        token_activations = self.activation_matrix[token_idx].toarray()[0]
        
        active_features = []
        for feature_idx, act_val in enumerate(token_activations):
            if act_val > threshold:
                active_features.append((feature_idx, act_val))
        
        # Sort by activation value (descending)
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
        
        Returns:
            Dictionary with token string, position, surrounding context, etc.
        """
        metadata = self.token_metadata[token_idx]
        
        # Find neighboring tokens in the same text
        text_tokens = [
            t for t in self.token_metadata 
            if t.text_idx == metadata.text_idx
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
        """Save activation database to disk"""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'activation_matrix': self.activation_matrix,
            'token_metadata': self.token_metadata,
            'feature_metadata': self.feature_metadata
        }
        
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"✓ Saved activation database to {path}")
    
    @staticmethod
    def load(path: str) -> 'ActivationDatabase':
        """Load activation database from disk"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        db = ActivationDatabase(
            activation_matrix=data['activation_matrix'],
            token_metadata=data['token_metadata'],
            feature_metadata=data['feature_metadata']
        )
        
        print(f"✓ Loaded activation database from {path}")
        print(f"  {len(db.token_metadata)} tokens, {db.activation_matrix.shape[1]} features")
        
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
        """
        Args:
            model: HookedTransformer (e.g., qwen3-0.6b, gpt2-small)
            sae_path: Path to trained SAE weights
            layer: Layer number SAE is trained on
            hook_name: Hook point name (e.g., 'hook_mlp_out', 'hook_resid_post')
            dataset: List of text samples for analysis
        """
        self.model = model
        self.dataset = dataset
        self.layer = layer
        self.hook_name = hook_name
        self.hook_point = f"blocks.{layer}.{hook_name}"
        
        # Activation database (will be populated by collect_all_activations)
        self.activation_db: Optional[ActivationDatabase] = None
        
        # Feature similarity matrix (will be computed by compute_feature_similarity)
        self.feature_similarity: Optional[np.ndarray] = None
        
        # Validate dataset
        if not dataset or len(dataset) == 0:
            raise ValueError("Dataset cannot be empty!")
        
        # Filter out empty strings
        self.dataset = [text for text in dataset if text and len(text.strip()) > 0]
        if len(self.dataset) == 0:
            raise ValueError("Dataset contains only empty strings!")
        
        # Load SAE and move to correct device
        self.sae = load_pretrained(sae_path)
        self.device = next(self.model.parameters()).device
        self.sae = self.sae.to(self.device)
        self.sae.eval()  # Set to eval mode
        
        print(f"✓ Loaded SAE from {sae_path}")
        print(f"✓ Model and SAE on device: {self.device}")
        print(f"✓ Hook point: {self.hook_point}")
        print(f"✓ SAE dimensions: {self.sae.cfg.d_in} → {self.sae.cfg.d_sae}")
        print(f"✓ Dataset: {len(self.dataset)} texts")
    
    def _reset_model_state(self):
        """Clear all hooks and GPU cache"""
        self.model.reset_hooks()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    def collect_all_activations(
        self,
        texts: Optional[List[str]] = None,
        batch_size: int = 8,
        activation_threshold: float = 0.0,
        save_path: Optional[str] = None
    ) -> ActivationDatabase:
        """
        Process entire corpus and build comprehensive activation database
        
        Args:
            texts: Texts to process (defaults to self.dataset)
            batch_size: Batch size for processing
            activation_threshold: Only store activations above this value (for sparsity)
            save_path: Optional path to save the database
        
        Returns:
            ActivationDatabase with full activation matrix and token metadata
        """
        if texts is None:
            texts = self.dataset
        
        # Validate texts
        texts = [t for t in texts if t and len(t.strip()) > 0]
        if len(texts) == 0:
            raise ValueError("No valid texts to process!")
        
        self._reset_model_state()
        
        # Storage for building the database
        all_activations = []  # List of (row, col, value) tuples for sparse matrix
        token_metadata = []
        global_token_idx = 0
        
        # Feature statistics
        feature_activation_counts = torch.zeros(self.sae.cfg.d_sae)
        feature_total_activation = torch.zeros(self.sae.cfg.d_sae)
        
        print(f"\nCollecting activations from {len(texts)} texts...")
        print(f"This will build a comprehensive activation database.\n")
        
        for text_idx in tqdm(range(0, len(texts), batch_size), desc="Processing"):
            batch_texts = texts[text_idx:text_idx+batch_size]
            
            try:
                tokens = self.model.to_tokens(batch_texts, prepend_bos=True)
                tokens = tokens.to(self.device)
                
                if tokens.numel() == 0:
                    continue
                
            except Exception as e:
                print(f"Warning: Failed to tokenize batch {text_idx//batch_size}: {e}")
                continue
            
            with torch.no_grad():
                try:
                    # Get activations at hook point
                    _, cache = self.model.run_with_cache(
                        tokens,
                        names_filter=lambda name: name == self.hook_point
                    )
                    acts = cache[self.hook_point]
                    
                    # Encode with SAE
                    for batch_idx in range(acts.shape[0]):
                        text_global_idx = text_idx + batch_idx
                        
                        for pos in range(acts.shape[1]):
                            # Get features for this token
                            token_acts = acts[batch_idx, pos, :]
                            features = self.sae.encode(token_acts.unsqueeze(0))[0]
                            
                            # Get token string
                            token_id = tokens[batch_idx, pos].item()
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
                            
                            # Store activations (sparse format)
                            active_features = (features > activation_threshold).nonzero(as_tuple=True)[0]
                            
                            for feature_idx in active_features:
                                feature_idx_int = feature_idx.item()
                                activation_value = features[feature_idx].item()
                                
                                # Add to sparse matrix data
                                all_activations.append((
                                    global_token_idx,
                                    feature_idx_int,
                                    activation_value
                                ))
                                
                                # Update statistics
                                feature_activation_counts[feature_idx_int] += 1
                                feature_total_activation[feature_idx_int] += activation_value
                            
                            global_token_idx += 1
                    
                except Exception as e:
                    print(f"Warning: Error processing batch {text_idx//batch_size}: {e}")
                    continue
            
            self._reset_model_state()
        
        print(f"\n✓ Processed {global_token_idx} tokens")
        print(f"✓ Collected {len(all_activations)} non-zero activations")
        
        # Build sparse matrix
        print("\nBuilding sparse activation matrix...")
        rows, cols, values = zip(*all_activations) if all_activations else ([], [], [])
        
        activation_matrix = sparse.csr_matrix(
            (values, (rows, cols)),
            shape=(global_token_idx, self.sae.cfg.d_sae)
        )
        
        # Compute feature metadata
        feature_metadata = {
            'n_features': self.sae.cfg.d_sae,
            'n_tokens': global_token_idx,
            'activation_counts': feature_activation_counts.tolist(),
            'total_activations': feature_total_activation.tolist(),
            'mean_activation': (feature_total_activation / (feature_activation_counts + 1e-8)).tolist(),
            'sparsity': 1.0 - (len(all_activations) / (global_token_idx * self.sae.cfg.d_sae))
        }
        
        print(f"✓ Matrix shape: {activation_matrix.shape}")
        print(f"✓ Sparsity: {feature_metadata['sparsity']*100:.2f}% (zeros)")
        
        # Create database
        self.activation_db = ActivationDatabase(
            activation_matrix=activation_matrix,
            token_metadata=token_metadata,
            feature_metadata=feature_metadata
        )
        
        # Save if requested
        if save_path is not None:
            self.activation_db.save(save_path)
        
        return self.activation_db
    
    def load_activation_database(self, path: str):
        """Load a previously saved activation database"""
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
        
        Args:
            save_path: Optional path to save similarity matrix
            similarity_metric: 'cosine', 'dot', or 'euclidean'
        
        Returns:
            Similarity matrix [n_features x n_features]
        """
        print(f"\nComputing feature similarity using {similarity_metric} metric...")
        
        # Get decoder weights [d_sae × d_in]
        decoder = self.sae.W_dec.detach().cpu()
        n_features = decoder.shape[0]
        
        if similarity_metric == 'cosine':
            # Normalize each feature's decoder
            decoder_normalized = decoder / (decoder.norm(dim=1, keepdim=True) + 1e-8)
            
            # Compute pairwise cosine similarity
            similarity = decoder_normalized @ decoder_normalized.T
            
        elif similarity_metric == 'dot':
            # Raw dot product
            similarity = decoder @ decoder.T
            
        elif similarity_metric == 'euclidean':
            # Negative euclidean distance (so higher = more similar)
            # Using efficient matrix operations
            decoder_sq = (decoder ** 2).sum(dim=1, keepdim=True)
            distances = decoder_sq + decoder_sq.T - 2 * (decoder @ decoder.T)
            similarity = -torch.sqrt(torch.clamp(distances, min=0))
            
        else:
            raise ValueError(f"Unknown similarity metric: {similarity_metric}")
        
        self.feature_similarity = similarity.numpy()
        
        print(f"✓ Computed {n_features} × {n_features} similarity matrix")
        print(f"  Mean similarity: {self.feature_similarity.mean():.4f}")
        print(f"  Std similarity: {self.feature_similarity.std():.4f}")
        
        # Save if requested
        if save_path is not None:
            np.save(save_path, self.feature_similarity)
            print(f"✓ Saved similarity matrix to {save_path}")
        
        return self.feature_similarity
    
    def find_similar_features(
        self,
        feature_idx: int,
        top_k: int = 10,
        exclude_self: bool = True
    ) -> List[Tuple[int, float]]:
        """
        Find features most similar to a given feature
        
        Args:
            feature_idx: Index of query feature
            top_k: Number of similar features to return
            exclude_self: Whether to exclude the feature itself
        
        Returns:
            List of (feature_idx, similarity_score) tuples
        """
        if self.feature_similarity is None:
            raise ValueError("Must call compute_feature_similarity() first!")
        
        similarities = self.feature_similarity[feature_idx]
        
        # Get top-k indices
        if exclude_self:
            # Set self-similarity to -inf so it's not selected
            similarities = similarities.copy()
            similarities[feature_idx] = -np.inf
        
        top_indices = np.argsort(similarities)[-top_k:][::-1]
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
        Comprehensive analysis of a single feature:
        - Max activating examples with context
        - Similar features by decoder
        
        Requires: activation_db and feature_similarity to be computed
        """
        if self.activation_db is None:
            raise ValueError("Must call collect_all_activations() first!")
        if self.feature_similarity is None:
            raise ValueError("Must call compute_feature_similarity() first!")
        
        print(f"\n{'='*60}")
        print(f"Feature {feature_idx} Analysis")
        print(f"{'='*60}\n")
        
        # Get activation statistics
        activation_freq = self.activation_db.feature_metadata['activation_counts'][feature_idx]
        mean_activation = self.activation_db.feature_metadata['mean_activation'][feature_idx]
        
        print(f"Activation Statistics:")
        print(f"  Frequency: {activation_freq} tokens ({activation_freq/self.activation_db.feature_metadata['n_tokens']*100:.2f}%)")
        print(f"  Mean activation: {mean_activation:.4f}")
        
        # Get max activating examples
        print(f"\nTop {top_k} Activating Examples:")
        print("-" * 60)
        
        activations = self.activation_db.get_feature_activations(feature_idx, top_k=top_k)
        
        for i, (token_idx, act_val) in enumerate(activations, 1):
            context = self.activation_db.get_token_context(
                token_idx, 
                self.model, 
                context_size=context_size
            )
            
            print(f"\n{i}. Activation: {act_val:.4f}")
            print(f"   Token: '{context['token']}'")
            print(f"   Context: {context['context']}")
        
        # Find similar features
        print(f"\n\nMost Similar Features (by decoder):")
        print("-" * 60)
        
        similar_features = self.find_similar_features(feature_idx, top_k=5)
        
        for i, (sim_feature_idx, similarity) in enumerate(similar_features, 1):
            # Get example activation for this similar feature
            sim_activations = self.activation_db.get_feature_activations(sim_feature_idx, top_k=1)
            
            print(f"\n{i}. Feature {sim_feature_idx} (similarity: {similarity:.4f})")
            
            if sim_activations:
                token_idx, act_val = sim_activations[0]
                context = self.activation_db.get_token_context(token_idx, self.model, context_size=5)
                print(f"   Example: '{context['token']}' in context: {context['context']}")
        
        print(f"\n{'='*60}\n")

    # [Keep all the existing methods from the original class below]
    
    def compute_sparsity_metrics(
        self, 
        texts: Optional[List[str]] = None, 
        batch_size: int = 8
    ) -> Tuple[Dict[str, float], List[float]]:
        """
        Compute L0 (number of active features) and L1 (sum of activations) statistics
        
        Returns:
            metrics: Dictionary with L0/L1 mean and std
            feature_freq: List of activation frequencies for each feature
        """
        if texts is None:
            texts = self.dataset
        
        # Validate texts
        texts = [t for t in texts if t and len(t.strip()) > 0]
        if len(texts) == 0:
            raise ValueError("No valid texts to process!")
        
        self._reset_model_state()
        
        # Running statistics
        l0_sum = 0.0
        l0_sq_sum = 0.0
        l1_sum = 0.0
        l1_sq_sum = 0.0
        feature_counts = torch.zeros(self.sae.cfg.d_sae, device='cpu')
        n_tokens_total = 0
        
        print(f"Computing sparsity metrics on {len(texts)} texts...")
        
        for i in tqdm(range(0, len(texts), batch_size), desc="Sparsity"):
            batch_texts = texts[i:i+batch_size]
            
            try:
                tokens = self.model.to_tokens(batch_texts, prepend_bos=True)
                tokens = tokens.to(self.device)
                
                # Check if we got valid tokens
                if tokens.numel() == 0:
                    print(f"Warning: Batch {i//batch_size} produced no tokens, skipping...")
                    continue
                
            except Exception as e:
                print(f"Warning: Failed to tokenize batch {i//batch_size}: {e}")
                continue
            
            with torch.no_grad():
                try:
                    # Get activations at hook point
                    _, cache = self.model.run_with_cache(
                        tokens,
                        names_filter=lambda name: name == self.hook_point
                    )
                    acts = cache[self.hook_point]
                    
                    # Flatten batch and sequence dimensions
                    acts_flat = acts.reshape(-1, acts.shape[-1])
                    
                    # Skip if no activations
                    if acts_flat.shape[0] == 0:
                        continue
                    
                    # Encode with SAE
                    features = self.sae.encode(acts_flat)
                    
                    # Compute L0 (number of active features per token)
                    l0_per_token = (features > 0).float().sum(dim=1)
                    l0_sum += l0_per_token.sum().item()
                    l0_sq_sum += (l0_per_token ** 2).sum().item()
                    
                    # Compute L1 (sum of activations per token)
                    l1_per_token = features.abs().sum(dim=1)
                    l1_sum += l1_per_token.sum().item()
                    l1_sq_sum += (l1_per_token ** 2).sum().item()
                    
                    # Track feature activation frequency
                    feature_active = (features > 0).float().sum(dim=0).cpu()
                    feature_counts += feature_active
                    
                    n_tokens_total += acts_flat.shape[0]
                    
                except Exception as e:
                    print(f"Warning: Error processing batch {i//batch_size}: {e}")
                    continue
            
            self._reset_model_state()
        
        # Check if we processed any tokens
        if n_tokens_total == 0:
            raise RuntimeError(
                "Failed to process any tokens! Check that:\n"
                "1. Your texts are not empty\n"
                "2. The tokenizer is working correctly\n"
                "3. The hook point exists in the model"
            )
        
        # Compute final statistics
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
        
        print(f"\n✓ Sparsity Results:")
        print(f"  L0: {l0_mean:.2f} ± {l0_std:.2f} features/token")
        print(f"  L1: {l1_mean:.4f} ± {l1_std:.4f}")
        print(f"  Tokens processed: {n_tokens_total}")
        
        return metrics, feature_freq
    
    def find_dead_features(
        self, 
        feature_freq: List[float], 
        threshold: float = 0.001
    ) -> Dict[str, any]:
        """
        Identify features that rarely or never activate
        
        Args:
            feature_freq: List of activation frequencies (from compute_sparsity_metrics)
            threshold: Frequency below which a feature is considered "dead"
        
        Returns:
            Dictionary with dead feature statistics
        """
        feature_freq_tensor = torch.tensor(feature_freq)
        dead_mask = feature_freq_tensor < threshold
        
        n_dead = int(dead_mask.sum().item())
        pct_dead = 100 * dead_mask.float().mean().item()
        dead_indices = dead_mask.nonzero(as_tuple=True)[0].tolist()
        
        print(f"\n✓ Dead Features (threshold={threshold}):")
        print(f"  {n_dead}/{len(feature_freq)} ({pct_dead:.1f}%) dead features")
        
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
        Measure how well SAE reconstructs the original activations
        
        Returns:
            Dictionary with MSE, explained variance, cosine similarity, etc.
        """
        if texts is None:
            texts = self.dataset
        
        # Validate texts
        texts = [t for t in texts if t and len(t.strip()) > 0]
        if len(texts) == 0:
            raise ValueError("No valid texts to process!")
        
        self._reset_model_state()
        
        # Running statistics
        mse_sum = 0.0
        original_var_sum = 0.0
        residual_var_sum = 0.0
        cos_sim_sum = 0.0
        n_tokens_total = 0
        
        print(f"Computing reconstruction metrics on {len(texts)} texts...")
        
        for i in tqdm(range(0, len(texts), batch_size), desc="Reconstruction"):
            batch_texts = texts[i:i+batch_size]
            
            try:
                tokens = self.model.to_tokens(batch_texts, prepend_bos=True)
                tokens = tokens.to(self.device)
                
                if tokens.numel() == 0:
                    continue
                    
            except Exception as e:
                print(f"Warning: Failed to tokenize batch {i//batch_size}: {e}")
                continue
            
            with torch.no_grad():
                try:
                    # Get original activations
                    _, cache = self.model.run_with_cache(
                        tokens,
                        names_filter=lambda name: name == self.hook_point
                    )
                    acts = cache[self.hook_point]
                    acts_flat = acts.reshape(-1, acts.shape[-1])
                    
                    if acts_flat.shape[0] == 0:
                        continue
                    
                    # SAE reconstruction
                    x_recon, features = self.sae(acts_flat)
                    
                    # Compute residual
                    residual = acts_flat - x_recon
                    
                    # MSE loss
                    mse = (residual ** 2).mean().item()
                    mse_sum += mse * acts_flat.shape[0]
                    
                    # Variance (for explained variance calculation)
                    original_var_sum += acts_flat.var().item() * acts_flat.shape[0]
                    residual_var_sum += residual.var().item() * acts_flat.shape[0]
                    
                    # Cosine similarity
                    cos_sim = torch.nn.functional.cosine_similarity(
                        acts_flat, x_recon, dim=1
                    ).mean().item()
                    cos_sim_sum += cos_sim * acts_flat.shape[0]
                    
                    n_tokens_total += acts_flat.shape[0]
                    
                except Exception as e:
                    print(f"Warning: Error processing batch {i//batch_size}: {e}")
                    continue
            
            self._reset_model_state()
        
        if n_tokens_total == 0:
            raise RuntimeError("Failed to process any tokens!")
        
        # Compute averages
        mse_avg = mse_sum / n_tokens_total
        original_var_avg = original_var_sum / n_tokens_total
        residual_var_avg = residual_var_sum / n_tokens_total
        cos_sim_avg = cos_sim_sum / n_tokens_total
        
        # Explained variance: 1 - (Var(residual) / Var(original))
        explained_var = 1.0 - (residual_var_avg / original_var_avg) if original_var_avg > 0 else 0.0
        
        metrics = {
            'mse': mse_avg,
            'explained_variance': explained_var,
            'cosine_similarity': cos_sim_avg,
            'original_std': np.sqrt(original_var_avg),
            'residual_std': np.sqrt(residual_var_avg),
            'n_tokens': n_tokens_total
        }
        
        print(f"\n✓ Reconstruction Results:")
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
        Compare model performance under three conditions:
        1. Baseline: Original model (no intervention)
        2. Zero ablation: Replace activations with zeros
        3. SAE reconstruction: Replace activations with SAE output
        
        Returns:
            Dictionary with loss for each condition and loss recovered metric
        """
        if texts is None:
            texts = self.dataset
        
        # Validate texts
        texts = [t for t in texts if t and len(t.strip()) > 0]
        if len(texts) == 0:
            raise ValueError("No valid texts to process!")
        
        self._reset_model_state()
        
        # Get padding token for loss computation
        pad_token_id = self.model.tokenizer.pad_token_id
        if pad_token_id is None:
            pad_token_id = self.model.tokenizer.eos_token_id
        
        loss_baseline_sum = 0.0
        loss_zero_sum = 0.0
        loss_sae_sum = 0.0
        n_batches = 0
        
        print(f"Running ablation study on {len(texts)} texts...")
        
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
                    # 1. BASELINE: Original model (no intervention)
                    self._reset_model_state()
                    logits_baseline = self.model(tokens)
                    loss_baseline = self._compute_ce_loss(logits_baseline, tokens, pad_token_id)
                    
                    # 2. ZERO ABLATION: Replace with zeros
                    self._reset_model_state()
                    def zero_hook(acts, hook):
                        return torch.zeros_like(acts)
                    
                    logits_zero = self.model.run_with_hooks(
                        tokens,
                        fwd_hooks=[(self.hook_point, zero_hook)],
                        reset_hooks_end=True
                    )
                    loss_zero = self._compute_ce_loss(logits_zero, tokens, pad_token_id)
                    
                    # 3. SAE RECONSTRUCTION: Replace with SAE output
                    self._reset_model_state()
                    def sae_hook(acts, hook):
                        x_recon, _ = self.sae(acts)
                        return x_recon
                    
                    logits_sae = self.model.run_with_hooks(
                        tokens,
                        fwd_hooks=[(self.hook_point, sae_hook)],
                        reset_hooks_end=True
                    )
                    loss_sae = self._compute_ce_loss(logits_sae, tokens, pad_token_id)
                    
                    # Accumulate losses
                    loss_baseline_sum += loss_baseline.item()
                    loss_zero_sum += loss_zero.item()
                    loss_sae_sum += loss_sae.item()
                    n_batches += 1
                    
                    # Sanity check: baseline should have lowest loss
                    if loss_baseline.item() > loss_zero.item():
                        print(f"\n⚠️ WARNING: Baseline loss > Zero ablation loss!")
                        print(f"   This suggests the hook point may be incorrect.")
                    
                except Exception as e:
                    print(f"Warning: Error processing batch {i//batch_size}: {e}")
                    continue
            
            self._reset_model_state()
        
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
            print("\n⚠️ WARNING: Zero ablation did not increase loss!")
        
        metrics = {
            'baseline_loss': loss_baseline_avg,
            'zero_ablation_loss': loss_zero_avg,
            'sae_reconstruction_loss': loss_sae_avg,
            'loss_recovered': loss_recovered,
            'n_batches': n_batches
        }
        
        print(f"\n✓ Ablation Study Results:")
        print(f"  Baseline Loss:      {loss_baseline_avg:.4f}")
        print(f"  Zero Ablation:      {loss_zero_avg:.4f} (+{loss_increase_zero:.4f})")
        print(f"  SAE Reconstruction: {loss_sae_avg:.4f} (+{loss_increase_sae:.4f})")
        print(f"  Loss Recovered:     {loss_recovered*100:.2f}%")
        print(f"  Batches processed:  {n_batches}")
        
        return metrics
    
    def _compute_ce_loss(
        self, 
        logits: torch.Tensor, 
        tokens: torch.Tensor, 
        pad_token_id: int
    ) -> torch.Tensor:
        """Compute cross-entropy loss for next-token prediction"""
        # Shift logits and tokens for next-token prediction
        logits = logits[:, :-1, :]  # Remove last token
        targets = tokens[:, 1:]      # Remove first token (BOS)
        
        # Flatten for loss computation
        logits_flat = logits.reshape(-1, logits.shape[-1])
        targets_flat = targets.reshape(-1)
        
        # Compute cross-entropy (ignore padding tokens)
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
        texts: Optional[List[str]] = None,
        top_k: int = 10,
        batch_size: int = 8,
        context_size: int = 10
    ) -> List[Dict[str, any]]:
        """
        Find tokens/contexts that most strongly activate a specific feature
        
        Args:
            feature_idx: Index of the feature to analyze
            texts: Texts to search through
            top_k: Number of top examples to return
            batch_size: Batch size for processing
            context_size: Number of tokens before/after to show (total window = 2*context_size+1)
        
        Returns:
            List of dictionaries with 'text', 'activation', 'position' for each example
        """
        if texts is None:
            texts = self.dataset
        
        # Validate texts
        texts = [t for t in texts if t and len(t.strip()) > 0]
        if len(texts) == 0:
            raise ValueError("No valid texts to process!")
        
        self._reset_model_state()
        
        # Use min-heap to efficiently track top-k
        top_examples = []  # Heap of (activation, counter, example_dict)
        counter = 0  # Unique counter to break ties
        
        print(f"Finding max activating examples for feature {feature_idx}...")
        
        for i in tqdm(range(0, len(texts), batch_size), desc="Max Act"):
            batch_texts = texts[i:i+batch_size]
            
            try:
                tokens = self.model.to_tokens(batch_texts, prepend_bos=True)
                tokens = tokens.to(self.device)
                
                if tokens.numel() == 0:
                    continue
                    
            except Exception as e:
                print(f"Warning: Failed to tokenize batch {i//batch_size}: {e}")
                continue
            
            with torch.no_grad():
                try:
                    # Get activations
                    _, cache = self.model.run_with_cache(
                        tokens,
                        names_filter=lambda name: name == self.hook_point
                    )
                    acts = cache[self.hook_point]
                    acts_flat = acts.reshape(-1, acts.shape[-1])
                    
                    if acts_flat.shape[0] == 0:
                        continue
                    
                    # Encode with SAE
                    features = self.sae.encode(acts_flat)
                    feature_acts = features[:, feature_idx]
                    
                    # Get top activations from this batch
                    top_vals, top_indices = feature_acts.topk(
                        min(top_k * 2, len(feature_acts))
                    )
                    
                    for val, idx in zip(top_vals, top_indices):
                        # Convert flat index to batch and sequence position
                        batch_idx = idx // tokens.shape[1]
                        seq_idx = idx % tokens.shape[1]
                        
                        # Extract context
                        context_start = max(0, seq_idx - context_size)
                        context_end = min(tokens.shape[1], seq_idx + context_size + 1)
                        context_tokens = tokens[batch_idx, context_start:context_end]
                        
                        # Get text representation
                        context_text = self.model.to_string(context_tokens)
                        
                        # Highlight the specific token
                        target_token = self.model.to_string(tokens[batch_idx, seq_idx])
                        
                        example = {
                            'text': context_text,
                            'target_token': target_token,
                            'activation': val.item(),
                            'position': seq_idx.item(),
                            'batch_idx': i + batch_idx.item()
                        }
                        
                        # Maintain top-k using heap with counter for tie-breaking
                        if len(top_examples) < top_k:
                            heapq.heappush(top_examples, (val.item(), counter, example))
                            counter += 1
                        elif val.item() > top_examples[0][0]:
                            heapq.heapreplace(top_examples, (val.item(), counter, example))
                            counter += 1
                
                except Exception as e:
                    print(f"Warning: Error processing batch {i//batch_size}: {e}")
                    continue
            
            self._reset_model_state()
        
        if len(top_examples) == 0:
            print(f"⚠️ WARNING: No activations found for feature {feature_idx}")
            return []
        
        # Sort by activation (descending)
        top_examples.sort(reverse=True, key=lambda x: x[0])
        result = [ex[2] for ex in top_examples]
        
        print(f"\n✓ Found top {len(result)} activating examples for feature {feature_idx}")
        print(f"  Max activation: {result[0]['activation']:.4f}")
        print(f"  Min activation (in top-k): {result[-1]['activation']:.4f}")
        
        return result
    
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
        
        print(f"\n{'='*60}")
        print(f"Running Full SAE Analysis")
        print(f"{'='*60}\n")
        
        results = {}
        
        # 1. Sparsity metrics
        print(f"\n[1/4] Computing Sparsity Metrics...")
        sparsity_metrics, feature_freq = self.compute_sparsity_metrics(
            texts, batch_size
        )
        results['sparsity'] = sparsity_metrics
        results['feature_freq'] = feature_freq
        
        # 2. Dead features
        print(f"\n[2/4] Identifying Dead Features...")
        dead_features = self.find_dead_features(feature_freq)
        results['dead_features'] = dead_features
        
        # 3. Reconstruction quality
        print(f"\n[3/4] Computing Reconstruction Metrics...")
        recon_metrics = self.compute_reconstruction_metrics(texts, batch_size)
        results['reconstruction'] = recon_metrics
        
        # 4. Ablation study
        print(f"\n[4/4] Running Ablation Study...")
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
            
            print(f"\n✓ Results saved to {save_path}")
        
        print(f"Analysis Complete!")
        
        return results