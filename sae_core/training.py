import math
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

from sae_core.sae_base import SAE, BatchTopKSAE
from sae_core.train_config import TrainingConfig

LOG_PROB_MIN = -60.0  # clamp value to avoid log(0) issues

def train_sae(
    sae: BatchTopKSAE,
    model: HookedTransformer,
    data_loader: DataLoader,
    config: TrainingConfig,
    checkpoint_dir: Optional[Path] = None,
    checkpoint_freq: int = 5,
    save_best: bool = True,
    val_loader: Optional[DataLoader] = None,
) -> Dict[str, List[float]]:

    model.eval()

    # Checkpointing
    if checkpoint_dir is not None:
        checkpoint_dir = Path(checkpoint_dir)
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        print(f"Checkpointing enabled: saving to {checkpoint_dir}")
    best_recon_loss = float('inf')

    # Freeze model parameters - they won't be needing gradient updates
    for param in model.parameters():
        param.requires_grad = False

    optimizer = torch.optim.Adam(sae.parameters(), lr=config.lr)

    hook_spec = sae.cfg.hook_spec
    hook_layer = sae.cfg.hook_layer

    if config.block_mse_layers is None:
        mse_layers = list(range(int(hook_layer) + 1, model.cfg.n_layers))
    else:
        mse_layers = config.block_mse_layers

    metric_keys = [
        "loss",
        "recon_loss",
        "l1_loss",
        "sparsity",
        "recon_contribution",
        "l1_contribution",
        "aux_loss",
    ]

    cache_names = [hook_spec]
    if config.use_block_mse:
        metric_keys.extend(["block_mse_contribution", "total_post_layer_mse"])
        cache_names.extend([f"blocks.{layer}.hook_resid_post" for layer in mse_layers])
        for layer in mse_layers:
            metric_keys.append(f"{layer}_mse")

    if config.use_logit_kl:
        metric_keys.extend(["logit_kl", "kl_contribution"])
        cache_names.append("logits")

    history = {k: [] for k in metric_keys}
    history["dead_features"] = []
    history["dead_feature_percentage"] = []
    if val_loader is not None:
        for key in metric_keys:
            history[f"val_{key}"] = []

    pad_token_id = model.tokenizer.pad_token_id
    if pad_token_id is None:
        pad_token_id = model.tokenizer.eos_token_id
    if pad_token_id is None:
        raise ValueError("Tokenizer must provide a pad_token_id or eos_token_id for masking")

    def forward_batch(batch: torch.Tensor):
        with torch.no_grad():
            logits_clean, cache_clean = model.run_with_cache(
                batch, names_filter=lambda name: name in cache_names
            )
            activations = cache_clean[hook_spec]

            batch_size, seq_len, d_model = activations.shape
            activations_flat = activations.reshape(-1, d_model) # [B*S, d_model]
            tokens_flat = batch.reshape(-1)
            non_pad = tokens_flat != pad_token_id
            activations_real = activations_flat[non_pad]    # Get rid of all padding tokens, now [N_real, d_model]
            if activations_real.numel() == 0:
                return None

        def sae_forward_on_real_activations(real_acts: torch.Tensor):
            if config.activation_batch_size is not None and config.activation_batch_size > 0:
                x_chunks = []
                f_chunks = []
                for start in range(0, real_acts.shape[0], config.activation_batch_size):
                    end = start + config.activation_batch_size
                    x_c, f_c = sae.forward(real_acts[start:end])
                    x_chunks.append(x_c)
                    f_chunks.append(f_c)
                x_full = torch.cat(x_chunks, dim=0)
                f_full = torch.cat(f_chunks, dim=0)
                sae._last_dense_acts = f_full
                return x_full, f_full
            x_recon_full, f_full = sae.forward(real_acts)
            sae._last_dense_acts = f_full
            return x_recon_full, f_full

        x_recon, features = sae_forward_on_real_activations(activations_real)
        recon_loss = F.mse_loss(activations_real.to(x_recon.dtype), x_recon)
        x_recon = x_recon.to(activations_real.dtype)
        l1_loss = features.abs().mean()

        recon_contribution = config.reconstruction_loss_weight * recon_loss
        l1_contribution = config.l1_coefficient * l1_loss
        loss = recon_contribution + l1_contribution

        aux_loss_value = 0.0
        aux_loss = sae.get_auxiliary_loss(activations_real, x_recon)
        if aux_loss is not None:
            loss = loss + aux_loss
            aux_loss_value = aux_loss.item()

        sparsity_value = (features > 0).float().sum(dim=1).mean().item()

        block_mse_contribution = 0.0
        total_post_layer_mse = 0.0
        per_layer_mse: Dict[int, float] = {layer: 0.0 for layer in mse_layers}
        kl_value = 0.0
        kl_contribution_value = 0.0

        x_recon_full = None
        logits_intervened = None
        cache_intervened = None
        if config.use_end_to_end:
            x_recon_full = activations_flat.clone()     # [B*S, d_model]
            x_recon_full[non_pad] = x_recon     # overwrite non-pad rows with sae reconstruction
            x_recon_reshaped = x_recon_full.reshape(batch_size, seq_len, -1)

            def intervention_hook(acts, hook):
                return x_recon_reshaped

            with model.hooks(fwd_hooks=[(hook_spec, intervention_hook)]):
                logits_intervened, cache_intervened = model.run_with_cache(
                    batch, names_filter=lambda name: name in cache_names
                )

            if config.use_block_mse:
                for layer in mse_layers:
                    clean_post = cache_clean[f"blocks.{layer}.hook_resid_post"].to(torch.float32)
                    intervened_post = cache_intervened[f"blocks.{layer}.hook_resid_post"].to(torch.float32)
                    layer_mse = F.mse_loss(intervened_post, clean_post)
                    layer_mse_contribution = config.block_mse_weight * layer_mse
                    loss += layer_mse_contribution
                    block_mse_contribution += layer_mse_contribution.item()
                    mse_value = layer_mse.item()
                    per_layer_mse[layer] = mse_value
                    total_post_layer_mse += mse_value

            if config.use_logit_kl:
                attn_mask = (batch != pad_token_id)
                kl_div = compute_kl_divergence(
                    logits_intervened,
                    logits_clean,
                    mask=attn_mask,
                )
                kl_contribution = config.logit_kl_weight * kl_div
                loss += kl_contribution
                kl_value = kl_div.item()
                kl_contribution_value = kl_contribution.item()

        stats = {
            "loss": loss.item(),
            "recon_loss": recon_loss.item(),
            "l1_loss": l1_loss.item(),
            "sparsity": sparsity_value,
            "recon_contribution": recon_contribution.item(),
            "l1_contribution": l1_contribution.item(),
            "aux_loss": aux_loss_value,
        }

        if config.use_block_mse:
            stats["block_mse_contribution"] = block_mse_contribution
            stats["total_post_layer_mse"] = total_post_layer_mse
            for layer in mse_layers:
                stats[f"{layer}_mse"] = per_layer_mse[layer]

        if config.use_logit_kl:
            stats["logit_kl"] = kl_value
            stats["kl_contribution"] = kl_contribution_value

        return loss, stats, features

    def evaluate(loader: DataLoader):
        eval_metrics = {k: 0.0 for k in metric_keys}
        total_batches = 0
        sae.eval()
        with torch.no_grad():
            for batch in loader:
                batch = batch.to(sae.device)
                result = forward_batch(batch)
                if result is None:
                    continue
                _, batch_stats, _ = result
                for key in metric_keys:
                    eval_metrics[key] += batch_stats[key]
                total_batches += 1
        sae.train()
        return eval_metrics, total_batches

    for epoch in range(config.num_epochs):
        epoch_metrics = {k: 0.0 for k in metric_keys}
        num_batches = 0

        pbar = tqdm(data_loader, desc=f"Epoch {epoch+1}/{config.num_epochs}")
        for i, batch in enumerate(pbar):
            batch = batch.to(sae.device)
            optimizer.zero_grad()

            result = forward_batch(batch)
            if result is None:
                continue
            loss, batch_stats, features = result

            if not torch.isfinite(loss):
                print("Encountered non-finite loss; skipping batch to keep training stable.")
                continue
            if any(not math.isfinite(v) for v in batch_stats.values()):
                print("Encountered non-finite training stats; skipping batch to keep training stable.")
                continue
            if not torch.isfinite(features).all():
                print("Encountered non-finite SAE activations; skipping batch to keep training stable.")
                continue

            loss.backward()
            sae.project_decoder_gradients()
            optimizer.step()
            sae.normalize_decoder()

            sae.update_inactive_features(features)

            for key in metric_keys:
                epoch_metrics[key] += batch_stats[key]
            num_batches += 1

            if i % config.log_freq == 0:
                pbar_dict = {
                    "loss": f"{batch_stats['loss']:.4f}",
                    "recon": f"{batch_stats['recon_contribution']:.4f}",
                    "l1": f"{batch_stats['l1_contribution']:.4f}",
                }
                if config.use_block_mse:
                    pbar_dict["block_mse"] = f"{batch_stats['block_mse_contribution']:.4f}"
                if config.use_logit_kl:
                    pbar_dict["kl"] = f"{batch_stats['kl_contribution']:.4f}"
                pbar.set_postfix(pbar_dict)

        if num_batches == 0:
            raise RuntimeError("Training loader produced zero usable batches.")

        dead_features = sae.count_dead_features()
        dead_feature_pct = sae.dead_feature_percentage()

        for key in metric_keys:
            history[key].append(epoch_metrics[key] / num_batches)
        history["dead_features"].append(dead_features)
        history["dead_feature_percentage"].append(dead_feature_pct)

        print(f"\nEpoch {epoch+1} Summary:")
        print(f"    loss: {history['loss'][-1]:.4f}")
        print(f"      └─ recon_contribution: {history['recon_contribution'][-1]:.4f}")
        print(f"      └─ l1_contribution: {history['l1_contribution'][-1]:.4f}")
        if config.use_block_mse:
            print(f"      └─ block_mse_contribution: {history['block_mse_contribution'][-1]:.4f}")
        if config.use_logit_kl:
            print(f"      └─ kl_contribution: {history['kl_contribution'][-1]:.4f}")
        print(f"    sparsity: {history['sparsity'][-1]:.4f}")
        print(f"    aux_loss: {history['aux_loss'][-1]:.4f}")
        print(f"    dead features: {dead_features}/{sae.cfg.d_sae} ({dead_feature_pct:.2f}%)")

        if val_loader is not None:
            val_metrics, val_batches = evaluate(val_loader)
            if val_batches == 0:
                raise RuntimeError("Validation loader produced zero usable batches.")
            for key in metric_keys:
                history[f"val_{key}"].append(val_metrics[key] / val_batches)
            print("    Validation:")
            print(f"        loss: {history['val_loss'][-1]:.4f}")
            print(f"          └─ recon_contribution: {history['val_recon_contribution'][-1]:.4f}")
            print(f"          └─ l1_contribution: {history['val_l1_contribution'][-1]:.4f}")
            if config.use_block_mse:
                print(f"          └─ block_mse_contribution: {history['val_block_mse_contribution'][-1]:.4f}")
            if config.use_logit_kl:
                print(f"          └─ kl_contribution: {history['val_kl_contribution'][-1]:.4f}")
            print(f"        sparsity: {history['val_sparsity'][-1]:.4f}")
            print(f"        aux_loss: {history['val_aux_loss'][-1]:.4f}")

        if checkpoint_dir is not None:
            if (epoch + 1) % checkpoint_freq == 0:
                checkpoint_path = checkpoint_dir / f"checkpoint_epoch{epoch+1}.pt"
                sae.save(str(checkpoint_path), history=history)
                print(f"    Saved checkpoint to {checkpoint_path}")

            if save_best and history['recon_loss'][-1] < best_recon_loss:
                best_recon_loss = history['recon_loss'][-1]
                best_model_path = checkpoint_dir / "best_model.pt"
                sae.save(str(best_model_path), history=history)
                print(f"    New best model (recon_loss: {best_recon_loss:.4f}) Saved to {best_model_path}")

    return history


def compute_kl_divergence(
    logits_intervened: torch.Tensor,
    logits_clean: torch.Tensor,
    temperature: float = 1.0,
    mask: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    """
    Compute KL divergence KL(P_intervened || P_clean). Optionally mask out pad tokens.
    Args:
        logits_intervened: Logits from model with SAE intervention [batch, seq, vocab]
        logits_clean: Original model logits [batch, seq, vocab]
        temperature: Temperature for softmax (default 1.0)
        mask: Optional bool mask [batch, seq] where True means keep token
    """
    logits_intervened = logits_intervened.to(torch.float32)
    logits_clean = logits_clean.to(torch.float32)

    log_probs_intervened = F.log_softmax(logits_intervened / temperature, dim=-1)
    log_probs_clean = F.log_softmax(logits_clean / temperature, dim=-1)

    log_probs_intervened = torch.clamp(torch.nan_to_num(log_probs_intervened), min=LOG_PROB_MIN, max=0.0)
    log_probs_clean = torch.clamp(torch.nan_to_num(log_probs_clean), min=LOG_PROB_MIN, max=0.0)

    if mask is None:
        return F.kl_div(
            log_probs_clean,       # input (p)
            log_probs_intervened, # target(q)
            reduction="batchmean",
            log_target=True,
        )

    # reduction='none' to apply mask, then average over unmasked tokens
    per_token = F.kl_div(
        log_probs_clean,
        log_probs_intervened,
        reduction="none",
        log_target=True,
    ).sum(dim=-1)
    mask_f = mask.to(per_token.dtype)
    masked_sum = (per_token * mask_f).sum()
    denom = mask_f.sum().clamp_min(1.0)
    return masked_sum / denom
