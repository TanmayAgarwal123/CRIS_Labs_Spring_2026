import torch
import torch.nn.functional as F
from pathlib import Path
from typing import Dict, List

from transformer_lens import HookedTransformer

from sae_core.sae_base import SAE
from sae_core.pretrained import load_pretrained
from sae_core.sae_train import WindowedTextDataset, pad_collate
from sae_core.training import compute_kl_divergence
from sae_core.data_processing.textbook_process import load_processed_data


def load_model(model_name: str, device: str, dtype: torch.dtype):
    return HookedTransformer.from_pretrained(
        model_name,
        device=device,
        dtype=str(dtype).replace("torch.", ""),
        trust_remote_code=True,
        torch_dtype=dtype,
    )


def prepare_batch(texts: List[str], tokenizer, max_length: int, batch_size: int, device: torch.device):
    dataset = WindowedTextDataset(
        texts=texts,
        tokenizer=tokenizer,
        max_length=max_length,
        prepend_bos=True,
    )
    pad_token_id = tokenizer.pad_token_id or tokenizer.eos_token_id
    samples = [dataset[i] for i in range(batch_size)]
    batch = pad_collate(samples, pad_token_id)
    return batch.to(device), pad_token_id


def evaluate_sae_on_batch(
    model: HookedTransformer,
    sae: SAE,
    batch: torch.Tensor,
    pad_token_id: int,
) -> Dict[str, float]:
    sae.eval()
    hook_layer = int(sae.cfg.hook_layer)
    mse_layers = list(range(hook_layer + 1, model.cfg.n_layers))
    cache_names = [sae.cfg.hook_spec, "logits"] + [f"blocks.{layer}.hook_resid_post" for layer in mse_layers]

    with torch.no_grad():
        logits_clean, cache_clean = model.run_with_cache(
            batch, names_filter=lambda name: name in cache_names
        )
        activations = cache_clean[sae.cfg.hook_spec]
        batch_size, seq_len, d_model = activations.shape

        activations_flat = activations.reshape(-1, d_model)
        tokens_flat = batch.reshape(-1)
        non_pad = tokens_flat != pad_token_id
        activations_real = activations_flat[non_pad]

        x_recon, features = sae.forward(activations_real)
        recon_loss = F.mse_loss(activations_real.to(x_recon.dtype), x_recon).item()
        sparsity = (features > 0).float().sum(dim=1).mean().item()

        x_recon_full = activations_flat.clone()
        x_recon_full[non_pad] = x_recon.to(activations_real.dtype)
        x_recon_reshaped = x_recon_full.reshape(batch_size, seq_len, -1)

        def intervention_hook(acts, hook):
            return x_recon_reshaped

        with model.hooks(fwd_hooks=[(sae.cfg.hook_spec, intervention_hook)]):
            logits_intervened, cache_intervened = model.run_with_cache(
                batch, names_filter=lambda name: name in cache_names
            )

    layer_mse = {}
    for layer in mse_layers:
        clean = cache_clean[f"blocks.{layer}.hook_resid_post"].to(torch.float32)
        intervened = cache_intervened[f"blocks.{layer}.hook_resid_post"].to(torch.float32)
        layer_mse[layer] = F.mse_loss(intervened, clean).item()

    kl = compute_kl_divergence(logits_clean, logits_intervened).item()

    return {
        "recon_mse": recon_loss,
        "sparsity": sparsity,
        "logit_kl": kl,
        "avg_block_mse": sum(layer_mse.values()) / len(layer_mse),
        "max_block_mse": max(layer_mse.values()),
        "min_block_mse": min(layer_mse.values()),
        "layer_mse": layer_mse,
    }


def load_sae(path: Path, device: str) -> SAE:
    sae, _ = load_pretrained(str(path), device=device, load_history=True)
    return sae


if __name__ == "__main__":
    MODEL_NAME = "Qwen/Qwen3-0.6B"
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    TORCH_DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32
    TORCH_DEVICE = torch.device(DEVICE)

    texts = load_processed_data("sae_core/data/processed_data/processed_physics_all.json")
    model = load_model(MODEL_NAME, DEVICE, TORCH_DTYPE)

    batch, pad_id = prepare_batch(
        texts[:32],
        model.tokenizer,
        max_length=128,
        batch_size=8,
        device=TORCH_DEVICE,
    )

    base_path = Path("sae_core/checkpoints/qwen3_06B_layer9_exp4_smoke_test_false/best_model.pt")
    block_path = Path("sae_core/checkpoints/qwen3_06B_layer9_exp4_smoke_test_true/best_model.pt")

    sae_base = load_sae(base_path, DEVICE)
    sae_block = load_sae(block_path, DEVICE)

    base_metrics = evaluate_sae_on_batch(model, sae_base, batch, pad_id)
    block_metrics = evaluate_sae_on_batch(model, sae_block, batch, pad_id)

    def summarize(name: str, metrics: Dict[str, float]):
        print(f"\n{name} metrics:")
        print(f"  recon_mse: {metrics['recon_mse']:.4f}")
        print(f"  sparsity: {metrics['sparsity']:.2f}")
        print(f"  logit_kl: {metrics['logit_kl']:.4f}")
        print(f"  avg_block_mse: {metrics['avg_block_mse']:.4f}")
        print(f"  min_block_mse: {metrics['min_block_mse']:.4f}")
        print(f"  max_block_mse: {metrics['max_block_mse']:.4f}")

    summarize("Baseline SAE", base_metrics)
    summarize("Block-MSE SAE", block_metrics)
