import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from torch.utils.data import DataLoader, Dataset
from dataclasses import dataclass
from typing import Tuple, Dict, Any, List, Optional, Callable
import json
from pathlib import Path
from tqdm import tqdm
from transformer_lens import HookedTransformer

from sae_core.sae_base import SAE
from sae_core.standard_sae import StandardSAE
from sae_core.train_config import TrainingConfig

def train_sae(
    sae: SAE,
    model: HookedTransformer,
    data_loader: DataLoader,
    config: TrainingConfig
) -> Dict[str, List[float]]:
    """
    SAE training function that should work with any SAE variant
    
    Returns:
        History dictionary with loss curves
    """
    # Freeze model parameters - they won't be needing gradient updates
    for param in model.parameters():
        param.requires_grad = False

    optimizer = torch.optim.Adam(sae.parameters(), lr=config.lr) # add mapping at some point

    hook_spec = sae.cfg.hook_spec
    hook_layer = sae.cfg.hook_layer
    hook_name = sae.cfg.hook_name

    if config.block_mse_layers is None:
        mse_layers = list(range(int(hook_layer)+1, model.cfg.n_layers)) # proceeding layers
    else:
        mse_layers = config.block_mse_layers
    
    history = {"loss": [], "recon_loss": [], "l1_loss": [], "sparsity": [],
               "recon_contribution": [], "l1_contribution": []}
    cache_names = [hook_spec]
    if config.use_block_mse:
        history['total_post_layer_mse'] = []
        history['block_mse_contribution'] = []
        cache_names.extend([f"blocks.{layer}.hook_resid_post" for layer in mse_layers])
        for layer in mse_layers:
            history[f"{layer}_mse"] = []

    kl_div = None
    if config.use_logit_kl:
        history["logit_kl"] = []
        history["kl_contribution"] = []
        cache_names.append("logits")
    
    for epoch in range(config.num_epochs):
        epoch_metrics = {k:0 for k in history.keys()}
        num_batches = 0
        
        pbar = tqdm(data_loader, desc=f"Epoch {epoch+1}/{config.num_epochs}")
        for i, batch in enumerate(pbar):
            batch = batch.to(sae.device)
            optimizer.zero_grad()

            # Clean model activations
            with torch.no_grad():
                logits_clean, cache_clean = model.run_with_cache(
                     batch,
                    names_filter=lambda name: name in cache_names
                )
                activations = cache_clean[hook_spec]
                
                # Reshape if needed:
                batch_size, seq_len = batch.shape[:2]
                activations = activations.flatten(0,1) if len(activations.shape) == 3 else activations.flatten(0,2)

            x_recon, features = sae.forward(activations)

            recon_loss = F.mse_loss(activations, x_recon)
            l1_loss = features.abs().mean()

            recon_contribution = config.reconstruction_loss_weight * recon_loss
            l1_contribution = config.l1_coefficient * l1_loss
            loss = recon_contribution + l1_contribution

            # Calculate sparsity:
            epoch_metrics['sparsity'] += (features > 0).float().sum(dim=1).mean().item()
            epoch_metrics['recon_contribution'] += recon_contribution.item()
            epoch_metrics['l1_contribution'] += l1_contribution.item()

            block_mse_contribution = 0.0
            if config.use_end_to_end:
                x_recon_reshaped = x_recon.reshape(batch_size, seq_len, -1)     # might be redundant

                def intervention_hook(acts, hook):
                    return x_recon_reshaped
                
                with model.hooks(fwd_hooks=[(hook_spec, intervention_hook)]):
                    logits_intervened, cache_intervened = model.run_with_cache(
                        batch,
                        names_filter=lambda name: name in cache_names
                    )

                if config.use_block_mse:
                    for layer in mse_layers:
                        layer_mse = F.mse_loss(
                            cache_intervened[f"blocks.{layer}.hook_resid_post"],
                            cache_clean[f"blocks.{layer}.hook_resid_post"]
                        )   # calculate mse between model output and modified output (from sae)
                        layer_mse_contribution = config.block_mse_weight * layer_mse
                        loss += layer_mse_contribution
                        block_mse_contribution += layer_mse_contribution.item()
                        epoch_metrics[f'{layer}_mse'] += layer_mse.item()
                        epoch_metrics['total_post_layer_mse'] += layer_mse.item()

                    epoch_metrics['block_mse_contribution'] += block_mse_contribution

                if config.use_logit_kl:
                    kl_div = compute_kl_divergence(
                        logits_intervened,
                        logits_clean
                    )
                    kl_contribution = config.logit_kl_weight * kl_div
                    loss += kl_contribution
                    epoch_metrics['logit_kl'] += kl_div.item()
                    epoch_metrics['kl_contribution'] += kl_contribution.item()
            
            # Backward pass
            loss.backward()
            optimizer.step()
            sae.normalize_decoder()
            
            # Track metrics
            epoch_metrics['loss'] += loss.item()
            epoch_metrics['recon_loss'] += recon_loss.item()
            epoch_metrics['l1_loss'] += l1_loss.item()
            num_batches += 1

            if i % config.log_freq == 0:
                pbar_dict = {
                    "loss": f"{loss.item():.4f}",
                    "recon": f"{recon_contribution.item():.4f}",
                    "l1": f"{l1_contribution.item():.4f}"
                }
                if config.use_block_mse:
                    pbar_dict['block_mse'] = f"{block_mse_contribution:.4f}"
                if config.use_logit_kl:
                    pbar_dict['kl'] = f"{kl_contribution.item():.4f}"
                pbar.set_postfix(pbar_dict)
        
        for k in history.keys():
            history[k].append(epoch_metrics[k] / num_batches)

        print(f"\nEpoch {epoch+1} Summary:")
        print(f"    loss: {history['loss'][-1]:.4f}")
        print(f"      └─ recon_contribution: {history['recon_contribution'][-1]:.4f}")
        print(f"      └─ l1_contribution: {history['l1_contribution'][-1]:.4f}")
        if config.use_block_mse:
            print(f"      └─ block_mse_contribution: {history['block_mse_contribution'][-1]:.4f}")
        if config.use_logit_kl:
            print(f"      └─ kl_contribution: {history['kl_contribution'][-1]:.4f}")
        print(f"    sparsity: {history['sparsity'][-1]:.4f}")
    
    return history


def compute_kl_divergence(
    logits_original: torch.Tensor,
    logits_reconstructed: torch.Tensor,
    temperature: float = 1.0
) -> torch.Tensor:
    """
    Compute KL divergence between two logit distributions
    
    Args:
        logits_original: Original model logits [batch, seq, vocab]
        logits_reconstructed: Logits from model with SAE intervention [batch, seq, vocab]
        temperature: Temperature for softmax (default 1.0)
    
    Returns:
        KL divergence (scalar)
    """
    log_probs_original = F.log_softmax(logits_original / temperature, dim=-1)
    log_probs_reconstructed = F.log_softmax(logits_reconstructed / temperature, dim=-1)

    kl_div = F.kl_div(log_probs_reconstructed, log_probs_original, reduction='batchmean',log_target=True)
    
    return kl_div