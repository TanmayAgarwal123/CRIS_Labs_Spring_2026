import torch
import torch.nn as nn
from transformer_lens import HookedTransformer
import numpy as np
from typing import List, Dict, Tuple, Optional
from tqdm import tqdm

from sae_core.pretrained import load_pretrained


class SAEAnalyzer:
    def __init__(self, model, sae_path, dataset):
        """
        Args:
            model: HookedTransformer (e.g., gpt2-small)
            sae_path: Path to trained SAE
            dataset: List of text samples
        """
        self.model = model
        self.dataset = dataset

        self.sae = load_pretrained(sae_path)
        self.device = next(self.model.parameters()).device
        self.sae = self.sae.to(self.device)
        print(f"Model and SAE on device: {self.device}")

        # TODO: Need to fix config for SAE to include layer and hook_name
        self.layer = sae_path[-19:-17]  # THIS IS NOT SUSTAINABLE
        self.hook_name = sae_path[-16:-4]   # THIS IS NOT SUSTAINABLE
        self.hook_point = f"blocks.{self.layer}.{self.hook_name}"

    def compute_sparsity_metrics(self, texts, batch_size=8):
        """Compute L0, L1, and feature activation statistics - STREAMING VERSION"""
        # Clear any existing hooks
        self.model.reset_hooks(including_permanent=True)
        
        l0_sum = 0
        l0_sq_sum = 0
        l1_sum = 0
        l1_sq_sum = 0
        feature_sum = None
        n_tokens_total = 0
        
        print(f"Processing {len(texts)} texts in batches of {batch_size}...")
        
        for i in tqdm(range(0, len(texts), batch_size)):
            batch = texts[i:i+batch_size]
            tokens = self.model.to_tokens(batch)
            
            # Run model and cache activations
            with torch.no_grad():
                _, cache = self.model.run_with_cache(tokens)
                acts = cache[self.hook_point]
                
                # Flatten
                acts_flat = acts.reshape(-1, acts.shape[-1])
                
                # Get SAE feature activations
                features = self.sae.encode(acts_flat)
                
                # Compute metrics for this batch
                l0_per_token = (features != 0).float().sum(dim=1)
                l1_per_token = features.abs().sum(dim=1)
                
                # Accumulate statistics
                l0_sum += l0_per_token.sum().item()
                l0_sq_sum += (l0_per_token ** 2).sum().item()
                l1_sum += l1_per_token.sum().item()
                l1_sq_sum += (l1_per_token ** 2).sum().item()
                
                # Feature frequency (accumulate on CPU to save GPU memory)
                if feature_sum is None:
                    feature_sum = (features != 0).float().sum(dim=0).cpu()
                else:
                    feature_sum += (features != 0).float().sum(dim=0).cpu()
                
                n_tokens_total += features.shape[0]
                
                # Clear cache and hooks immediately
                del cache, acts, acts_flat, features, l0_per_token, l1_per_token
                self.model.reset_hooks(including_permanent=True)
                torch.cuda.empty_cache()
        
        # Compute final statistics
        l0_mean = l0_sum / n_tokens_total
        l0_var = (l0_sq_sum / n_tokens_total) - (l0_mean ** 2)
        l0_std = np.sqrt(max(0, l0_var))
        
        l1_mean = l1_sum / n_tokens_total
        l1_var = (l1_sq_sum / n_tokens_total) - (l1_mean ** 2)
        l1_std = np.sqrt(max(0, l1_var))
        
        feature_freq = (feature_sum / n_tokens_total).tolist()
        
        results = {
            'l0_mean': l0_mean,
            'l0_std': l0_std,
            'l1_mean': l1_mean,
            'l1_std': l1_std,
            'feature_freq': feature_freq,
            'n_features': len(feature_freq),
            'n_tokens': n_tokens_total
        }
        
        return results
    
    def find_dead_features(self, feature_freq_list, threshold=0.005):
        """Identify features that rarely activate - uses precomputed frequencies"""
        feature_freq = torch.tensor(feature_freq_list)
        dead_features = (feature_freq < threshold)
        
        return {
            'n_dead': int(dead_features.sum().item()),
            'pct_dead': 100 * dead_features.float().mean().item(),
            'dead_indices': dead_features.nonzero().squeeze().tolist(),
            'activation_freq': feature_freq_list
        }
    
    def compute_layer_reconstruction_metrics(self, texts, batch_size=8):
        """Measure reconstruction quality - STREAMING VERSION"""
        # Clear any existing hooks
        self.model.reset_hooks(including_permanent=True)
        
        mse_sum = 0
        var_sum = 0
        res_var_sum = 0
        cos_sim_sum = 0
        recon_error_sum = 0
        n_tokens_total = 0
        
        print(f"Computing reconstruction metrics...")
        
        for i in tqdm(range(0, len(texts), batch_size)):
            batch = texts[i:i+batch_size]
            tokens = self.model.to_tokens(batch)
            
            with torch.no_grad():
                _, cache = self.model.run_with_cache(tokens)
                acts = cache[self.hook_point]
                acts_flat = acts.reshape(-1, acts.shape[-1])
                
                # SAE reconstruction
                sae_output = self.sae(acts_flat)
                reconstructed = sae_output[0]
                
                # Compute metrics
                mse = torch.nn.functional.mse_loss(reconstructed, acts_flat, reduction='sum')
                residual = acts_flat - reconstructed
                
                mse_sum += mse.item()
                var_sum += acts_flat.var(dim=0).sum().item()
                res_var_sum += residual.var(dim=0).sum().item()
                
                cos_sim = torch.nn.functional.cosine_similarity(
                    acts_flat, reconstructed, dim=1
                )
                cos_sim_sum += cos_sim.sum().item()
                
                recon_error = torch.norm(residual, dim=1).sum().item()
                recon_error_sum += recon_error
                
                n_tokens_total += acts_flat.shape[0]
                
                # Clear memory and hooks
                del cache, acts, acts_flat, sae_output, reconstructed, residual
                self.model.reset_hooks(including_permanent=True)
                torch.cuda.empty_cache()
        
        return {
            'mse_loss': mse_sum / n_tokens_total,
            'explained_variance': 1 - (res_var_sum / var_sum),
            'cosine_similarity': cos_sim_sum / n_tokens_total,
            'reconstruction_error': recon_error_sum / n_tokens_total
        }
    
    def ablation_study(self, texts, metric='loss', batch_size=4):
        """
        Compare model performance with:
        1. Original activations (baseline)
        2. Zero ablation
        3. SAE reconstruction
        """
        # CRITICAL: Clear all hooks at the start
        self.model.reset_hooks(including_permanent=True)
        print(f"Cleared hooks. Active hooks: {len(self.model.hook_dict)}")
        
        loss_orig_sum = 0
        loss_zero_sum = 0
        loss_sae_sum = 0
        n_batches = 0
        
        print(f"Running ablation study...")
        
        for i in tqdm(range(0, len(texts), batch_size)):
            batch = texts[i:i+batch_size]
            tokens = self.model.to_tokens(batch)
            
            # CRITICAL: Reset hooks before each condition
            self.model.reset_hooks(including_permanent=True)
            
            # 1. Baseline (original) - NO HOOKS
            with torch.no_grad():
                logits_orig = self.model(tokens)
                loss_orig = self.cross_entropy_loss(logits_orig, tokens)
            
            # CRITICAL: Clear any cached state between runs
            self.model.reset_hooks(including_permanent=True)
            torch.cuda.empty_cache()
            
            # 2. Zero ablation
            def zero_ablation_hook(acts, hook):
                return torch.zeros_like(acts)
            
            with torch.no_grad():
                logits_zero = self.model.run_with_hooks(
                    tokens,
                    fwd_hooks=[(self.hook_point, zero_ablation_hook)],
                    reset_hooks_end=True  # Ensure hooks are cleared
                )
                loss_zero = self.cross_entropy_loss(logits_zero, tokens)
            
            # CRITICAL: Clear hooks and cache
            self.model.reset_hooks(including_permanent=True)
            torch.cuda.empty_cache()
            
            # 3. SAE reconstruction  
            def sae_hook(acts, hook):
                with torch.no_grad():
                    sae_output = self.sae(acts)
                    reconstructed = sae_output[0]
                return reconstructed
            
            with torch.no_grad():
                logits_sae = self.model.run_with_hooks(
                    tokens,
                    fwd_hooks=[(self.hook_point, sae_hook)],
                    reset_hooks_end=True  # Ensure hooks are cleared
                )
                loss_sae = self.cross_entropy_loss(logits_sae, tokens)
            
            # CRITICAL: Clear hooks after each batch
            self.model.reset_hooks(including_permanent=True)
            
            # Sanity check: baseline should be best
            if loss_orig.item() > loss_zero.item():
                print(f"\n⚠️  WARNING batch {i//batch_size}: Baseline ({loss_orig.item():.4f}) > Zero ablation ({loss_zero.item():.4f})")
            
            loss_orig_sum += loss_orig.item()
            loss_zero_sum += loss_zero.item()
            loss_sae_sum += loss_sae.item()
            n_batches += 1
            
            # Clear memory
            del logits_orig, logits_zero, logits_sae, tokens
            torch.cuda.empty_cache()
        
        # Compute averages and loss recovered
        avg_results = {
            'baseline_loss': loss_orig_sum / n_batches,
            'zero_ablation_loss': loss_zero_sum / n_batches,
            'sae_reconstruction_loss': loss_sae_sum / n_batches,
        }
        
        # Loss recovered: what fraction of harm from zero ablation is recovered by SAE?
        loss_increase_zero = avg_results['zero_ablation_loss'] - avg_results['baseline_loss']
        loss_increase_sae = avg_results['sae_reconstruction_loss'] - avg_results['baseline_loss']
        
        if loss_increase_zero > 0:
            avg_results['loss_recovered'] = 1 - (loss_increase_sae / loss_increase_zero)
        else:
            # If zero ablation doesn't increase loss, something is very wrong
            avg_results['loss_recovered'] = float('nan')
            print("\n⚠️  WARNING: Zero ablation did not increase loss! Check your hook point.")
        
        return avg_results
    
    def cross_entropy_loss(self, logits, tokens):
        """Cross-entropy loss for next token prediction (ignoring padding tokens)"""
        # Get the padding token ID
        pad_token_id = self.model.tokenizer.pad_token_id
        if pad_token_id is None:
            # If no explicit pad token, use eos_token as padding
            pad_token_id = self.model.tokenizer.eos_token_id
        
        log_probs = torch.nn.functional.log_softmax(logits[:, :-1], dim=-1)
        targets = tokens[:, 1:]
        
        # Create mask for non-padding tokens
        mask = (targets != pad_token_id)
        
        # Compute loss only on non-padding tokens
        log_probs_flat = log_probs.reshape(-1, log_probs.shape[-1])
        targets_flat = targets.reshape(-1)
        
        # Use ignore_index to skip padding tokens
        return torch.nn.functional.nll_loss(
            log_probs_flat,
            targets_flat,
            ignore_index=pad_token_id
        )
    
    def find_max_activating_examples(self, texts, feature_idx, top_k=10, batch_size=8):
        """Find tokens that most activate a specific feature - MEMORY EFFICIENT"""
        # Clear any existing hooks
        self.model.reset_hooks(including_permanent=True)
        
        # Use a min-heap to keep only top-k examples
        import heapq
        top_examples = []  # Will store (activation, context_dict) tuples
        
        print(f"Finding max activating examples for feature {feature_idx}...")
        
        for i in tqdm(range(0, len(texts), batch_size)):
            batch = texts[i:i+batch_size]
            tokens = self.model.to_tokens(batch)
            
            with torch.no_grad():
                _, cache = self.model.run_with_cache(tokens)
                acts = cache[self.hook_point]
                acts_flat = acts.reshape(-1, acts.shape[-1])
                
                features = self.sae.encode(acts_flat)
                feature_acts = features[:, feature_idx]
                
                # Get top activations from this batch
                top_vals, top_indices = feature_acts.topk(min(top_k * 2, len(feature_acts)))
                
                for val, idx in zip(top_vals, top_indices):
                    batch_idx = idx // tokens.shape[1]
                    seq_idx = idx % tokens.shape[1]
                    
                    context_start = max(0, seq_idx - 5)
                    context_end = min(tokens.shape[1], seq_idx + 6)
                    context_tokens = tokens[batch_idx, context_start:context_end]
                    context_text = self.model.to_string(context_tokens)
                    
                    context_dict = {
                        'text': context_text,
                        'activation': val.item(),
                        'position': seq_idx.item()
                    }
                    
                    # Use heap to maintain top-k
                    if len(top_examples) < top_k:
                        heapq.heappush(top_examples, (val.item(), context_dict))
                    elif val.item() > top_examples[0][0]:
                        heapq.heapreplace(top_examples, (val.item(), context_dict))
                
                # Clear memory and hooks
                del cache, acts, acts_flat, features
                self.model.reset_hooks(including_permanent=True)
                torch.cuda.empty_cache()
        
        # Sort by activation (descending)
        top_examples.sort(reverse=True, key=lambda x: x[0])
        return [ex[1] for ex in top_examples]