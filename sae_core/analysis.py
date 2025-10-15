import torch
import torch.nn as nn
from transformer_lens import HookedTransformer
import numpy as np
from typing import List, Dict, Tuple, Optional
from tqdm import tqdm
import heapq

from sae_core.pretrained import load_pretrained


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
        threshold: float = 0.01
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
        top_examples = []  # Heap of (activation, example_dict)
        
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
                        
                        # Maintain top-k using heap
                        if len(top_examples) < top_k:
                            heapq.heappush(top_examples, (val.item(), example))
                        elif val.item() > top_examples[0][0]:
                            heapq.heapreplace(top_examples, (val.item(), example))
                
                except Exception as e:
                    print(f"Warning: Error processing batch {i//batch_size}: {e}")
                    continue
            
            self._reset_model_state()
        
        if len(top_examples) == 0:
            print(f"⚠️ WARNING: No activations found for feature {feature_idx}")
            return []
        
        # Sort by activation (descending)
        top_examples.sort(reverse=True, key=lambda x: x[0])
        result = [ex[1] for ex in top_examples]
        
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
        
        print(f"\n{'='*60}")
        print(f"Analysis Complete!")
        print(f"{'='*60}\n")
        
        return results