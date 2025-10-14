import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from transformer_lens import HookedTransformer
from transformer_lens.utils import get_act_name
import numpy as np
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import json
from dataclasses import dataclass
from tqdm import tqdm
import re
import requests

from sae_core.sae_base import SAE
from sae_core.sae_config import SAEConfig
from sae_core.standard_sae import StandardSAE
from sae_core.training import train_sae
from sae_core.sae_train import SAETrainer

from sae_core.data_processing.textbook_process import load_and_process_textbook, save_processed_data
from sae_core.pretrained import load_pretrained, list_pretrained

from transformer_lens import HookedTransformer

from collections import defaultdict
import matplotlib.pyplot as plt


sae_file_path = list_pretrained()[0]

class SAEAnalyzer:
    def __init__(self, model, sae_path, dataset):
        """
        Args:
            model: HookedTransformer (e.g., gpt2-small)
            sae: Trained SAE
            dataset: List of text samples
        """
        self.model = model
        self.dataset = dataset

        self.sae = load_pretrained(sae_path)
        self.device = next(self.model.parameters()).device
        self.sae = self.sae.to(self.device)
        print(f"Model and SAE on device: {self.device}")

        # TO DO: Need to fix config for SAE to include layer and hook_name:
        self.layer = sae_path[-19:-17]  # THIS IS NOT SUSTAINABLE
        self.hook_name = sae_path[-16:-4]   # THIS IS NOT SUSTAINABLE
        self.hook_point = f"blocks.{self.layer}.{self.hook_name}"

    def get_activations(self, texts, batch_size=8):
        """Get original activations from the model"""
        all_acts = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            tokens = self.model.to_tokens(batch)
            
            # Run model and cache activations
            _, cache = self.model.run_with_cache(tokens)
            acts = cache[self.hook_point]

            acts_flat = acts.reshape(-1, acts.shape[-1])
            all_acts.append(acts_flat)

            # Save memory:
            del _
            del cache
            
        return torch.cat(all_acts, dim=0)
    
    def compute_sparsity_metrics(self, texts, batch_size=8):
        """Compute L0, L1, and feature activation statistics"""
        activations = self.get_activations(texts, batch_size)
        
        # Reshape: (batch, seq, d_model) -> (batch*seq, d_model)
        acts_flat = activations
        
        # Get SAE feature activations
        with torch.no_grad():
            features = self.sae.encode(acts_flat)  # (batch*seq, n_features)
        
        # L0: Number of active features (non-zero)
        l0_per_token = (features != 0).float().sum(dim=1)
        
        # L1: Sum of absolute values
        l1_per_token = features.abs().sum(dim=1)
        
        # Feature activation frequency
        feature_freq = (features != 0).float().mean(dim=0)
        
        results = {
            'l0_mean': l0_per_token.mean().item(),
            'l0_std': l0_per_token.std().item(),
            'l1_mean': l1_per_token.mean().item(),
            'l1_std': l1_per_token.std().item(),
            'feature_freq': feature_freq.detach().cpu().tolist(),
            'n_features': features.shape[1],
            'n_tokens': features.shape[0]
        }
        
        return results, features
    
    def find_dead_features(self, feature_activations, threshold=1e-8):
        """Identify features that rarely activate"""
        activation_freq = (feature_activations.abs() > threshold).float().mean(dim=0)
        dead_features = (activation_freq < 0.005)  # Boolean tensor, <0.5% activation
        
        return {
            'n_dead': int(dead_features.sum().item()),
            'pct_dead': 100 * dead_features.float().mean().item(),
            'dead_indices': dead_features.nonzero().squeeze().tolist(),
            'activation_freq': activation_freq.detach().cpu().tolist()
            }
    
    def compute_layer_reconstruction_metrics(self, texts, batch_size=8):
        """Measure reconstruction quality"""
        activations = self.get_activations(texts, batch_size)
        
        with torch.no_grad():
            # SAE returns (reconstruction, features)
            sae_output = self.sae(activations)
            reconstructed = sae_output[0]
        
        # MSE loss
        mse_loss = torch.nn.functional.mse_loss(reconstructed, activations)
        
        # Explained variance
        total_variance = activations.var()
        residual_variance = (activations - reconstructed).var()
        explained_var = 1 - (residual_variance / total_variance)
        
        # Cosine similarity
        cos_sim = torch.nn.functional.cosine_similarity(
            activations, reconstructed, dim=1
        ).mean()
        
        return {
            'mse_loss': mse_loss.item(),
            'explained_variance': explained_var.item(),
            'cosine_similarity': cos_sim.item(),
            'reconstruction_error': torch.norm(activations - reconstructed, dim=1).mean().item()
            }
    
    def ablation_study(self, texts, metric='loss', batch_size=4):
        """
        Compare model performance with:
        1. Original activations (baseline)
        2. Zero ablation
        3. SAE reconstruction
        
        Args:
            metric: 'loss'
        """
        results = {}
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            tokens = self.model.to_tokens(batch)
            
            # 1. Baseline (original)
            logits_orig = self.model(tokens)
            loss_orig = self.cross_entropy_loss(logits_orig, tokens)
            
            # 2. Zero ablation
            def zero_ablation_hook(acts, hook):
                return torch.zeros_like(acts)
            
            logits_zero = self.model.run_with_hooks(
                tokens,
                fwd_hooks=[(self.hook_point, zero_ablation_hook)]
            )
            loss_zero = self.cross_entropy_loss(logits_zero, tokens)
            
            # 3. SAE reconstruction
            def sae_hook(acts, hook):
                # original_shape = acts.shape
                # acts_flat = acts.reshape(-1, acts.shape[-1])
                with torch.no_grad():
                    sae_output = self.sae(acts)
                    reconstructed = sae_output[0]
                # print(f"Original acts norm: {acts.norm().item():.4f}")
                # print(f"Reconstructed norm: {reconstructed.norm().item():.4f}")
                # print(f"Difference norm: {(acts - reconstructed).norm().item():.4f}")
                return reconstructed
            
            logits_sae = self.model.run_with_hooks(
                tokens,
                fwd_hooks=[(self.hook_point, sae_hook)]
            )
            loss_sae = self.cross_entropy_loss(logits_sae, tokens)
            
            # Store results
            if 'loss_orig' not in results:
                results = {
                    'loss_orig': [],
                    'loss_zero': [],
                    'loss_sae': []
                }
            
            results['loss_orig'].append(loss_orig.item())
            results['loss_zero'].append(loss_zero.item())
            results['loss_sae'].append(loss_sae.item())
        
        # Compute averages and loss recovered
        avg_results = {
            'baseline_loss': np.mean(results['loss_orig']),
            'zero_ablation_loss': np.mean(results['loss_zero']),
            'sae_reconstruction_loss': np.mean(results['loss_sae']),
        }
        
        # Loss recovered: what fraction of harm from zero ablation is recovered by SAE?
        loss_increase_zero = avg_results['zero_ablation_loss'] - avg_results['baseline_loss']
        loss_increase_sae = avg_results['sae_reconstruction_loss'] - avg_results['baseline_loss']
        avg_results['loss_recovered'] = 1 - (loss_increase_sae / loss_increase_zero)
        
        return avg_results
    
    def cross_entropy_loss(self, logits, tokens):
        """Cross-entropy loss for next token prediction"""
        # Shift logits/tokens to align predictions with the targets:
        log_probs = torch.nn.functional.log_softmax(logits[:, :-1], dim=-1)
        targets = tokens[:, 1:]
        return torch.nn.functional.nll_loss(
            log_probs.reshape(-1, log_probs.shape[-1]),
            targets.reshape(-1)
        )
    
    def find_max_activating_examples(self, texts, feature_idx, top_k=10, batch_size=8):
        """Find tokens that most activate a specific feature"""
        max_acts = []
        max_contexts = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            tokens = self.model.to_tokens(batch)
            activations = self.get_activations(batch, batch_size=len(batch))
            acts_flat = activations.reshape(-1, activations.shape[-1])
            
            with torch.no_grad():
                features = self.sae.encode(acts_flat)
            
            feature_acts = features[:, feature_idx]
            
            # Get top activations
            top_vals, top_indices = feature_acts.topk(min(top_k, len(feature_acts)))
            
            for val, idx in zip(top_vals, top_indices):
                # Find token
                batch_idx = idx // tokens.shape[1]
                seq_idx = idx % tokens.shape[1]
                
                # Get surrounding context
                context_start = max(0, seq_idx - 5)
                context_end = min(tokens.shape[1], seq_idx + 6)
                context_tokens = tokens[batch_idx, context_start:context_end]
                context_text = self.model.to_string(context_tokens)
                
                max_acts.append(val.item())
                max_contexts.append({
                    'text': context_text,
                    'activation': val.item(),
                    'position': seq_idx.item()
                })
        
        # Sort by activation value
        sorted_contexts = sorted(max_contexts, key=lambda x: x['activation'], reverse=True)
        return sorted_contexts[:top_k]
    