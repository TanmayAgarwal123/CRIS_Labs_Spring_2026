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
    # hook_point: str,
    data_loader: DataLoader,
    config: TrainingConfig
) -> Dict[str, List[float]]:
    """
    SAE training function that should work with any SAE variant
    
    Returns:
        History dictionary with loss curves
    """
    optimizer = torch.optim.Adam(sae.parameters(), lr=config.lr) # add mapping at some point

    hook_spec = sae.cfg.hook_spec

    # Find layer number
    layer_num = int(hook_spec.split('.')[1])

    if config.block_mse_layers is None:
        mse_layers = list(range(layer_num+1, model.cfg.n_layers)) # proceeding layers
    else:
        mse_layers = config.block_mse_layers
    
    history = {"loss": [], "recon_loss": [], "l1_loss": [], "sparsity": []}
    cache_names = [hook_spec]
    if config.use_block_mse:
        history['total_post_layer_mse'] = []
        cache_names.extend([f"blocks.{layer}.hook_resid_post" for layer in mse_layers])
        for layer in mse_layers:
            history[f"{layer}_mse"] = []
    if config.use_logit_kl:
        history["logit_kl"] = []
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
            
            # SAE Forward pass            
            outputs = sae.training_forward(activations)
            #Split outputs
            recon_loss = outputs["recon_loss"]
            l1_loss = outputs["l1_loss"]
            loss = outputs["loss"]
            x_recon = outputs["x_recon"]    # shape [batch_size,seq_len,d_in]
            sae_act = outputs["features"]   # shape [batch_size,seq_len,d_sae]

            # Calculate sparsity:
            epoch_metrics['sparsity'] = (sae_act > 0).float().mean().item()

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
                        loss += layer_mse
                        epoch_metrics[f'{layer}_mse'] += layer_mse.item()
                        epoch_metrics['total_post_layer_mse'] += layer_mse.item()

                if config.use_logit_kl:
                    kl_div = compute_kl_divergence(
                        logits_intervened,
                        logits_clean
                    )
                    loss += config.logit_kl_weight * kl_div
                    epoch_metrics['logit_kl'] += kl_div.item()
            
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
                pbar_dict = {"loss": f"{loss.item():.4f}"}
                if config.use_block_mse:
                    pbar_dict = {"total_post_layer_mse": f"{epoch_metrics['total_post_layer_mse']:.4f}"}
                if config.use_logit_kl:
                    pbar_dict = {"kl_div": f"{kl_div.item():.4f}"}
                pbar.set_postfix(pbar_dict)
        
        for k in history.keys():
            history[k].append(epoch_metrics[k] / num_batches)

        print(f"\nEpoch {epoch+1} Summary:")
        for k, v in history.items():
            print(f"    {k}: {v[-1]:.4f}")
    
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