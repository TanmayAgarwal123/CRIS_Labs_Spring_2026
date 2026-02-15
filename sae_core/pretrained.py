import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Type, Union

from huggingface_hub import snapshot_download

from sae_core.sae_base import SAE, BatchTopKSAE

HF_REPO_ID = "Sardean/saelens-models"

PRETRAINED_SAES = {
    # Deprecated SAEs:
    'gpt2.blocks.5.hook_mlp_out.sae': 'gpt2.blocks.5.hook_mlp_out.sae',
    'broken_qwen3_06B.blocks.14.hook_mlp_out.sae': 'broken_qwen3_06B.blocks.14.hook_mlp_out.sae',
    'qwen3_06B.blocks.14.hook_mlp_out.sae': 'qwen3_06B.blocks.14.hook_mlp_out.sae',
    'qwen3_06B.blocks.14.hook_mlp_out.sae.sparsity1': 'qwen3_06B.blocks.14.hook_mlp_out.sae.sparsity1',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity2.0': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity2.0',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity40.mse0.001.kl0.01': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity40.mse0.001.kl0.01',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity0.1.mse0.1.kl0.1': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity0.1.mse0.1.kl0.1',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity1.mse0.01.kl0.1': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity1.mse0.01.kl0.1',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity1.mse0.1.kl0.1': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity1.mse0.1.kl0.1',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity2.mse0.01.kl0.1': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity2.mse0.01.kl0.1',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity20.mse0.001.kl0.01': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity20.mse0.001.kl0.01',
    # Newer SAEs:
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity40.mse0.001.kl0.01.physics10': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity40.mse0.001.kl0.01.physics10',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity40.mse0.001.kl0.01.physics10.exp8': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity40.mse0.001.kl0.01.physics10.exp8',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity60.mse0.001.kl0.01.physics10.exp8': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity60.mse0.001.kl0.01.physics10.exp8',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity200.mse0.001.kl0.01.physics.exp4': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity200.mse0.001.kl0.01.physics.exp4',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity100.mse0.001.kl0.01.physics.exp4': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity100.mse0.001.kl0.01.physics.exp4',
    #BatchTopK SAEs:
    'Qwen_Qwen3-0.6B.blocks.9.hook_resid_post.btop256sae.all_science.exp4' : 'Qwen_Qwen3-0.6B.blocks.9.hook_resid_post.btop256sae.all_science.exp4',
    'Qwen_Qwen3-0.6B.blocks.9.hook_resid_post.btop128sae.all_science.exp4' : 'Qwen_Qwen3-0.6B.blocks.9.hook_resid_post.btop128sae.all_science.exp4'
}


def list_pretrained():
    """List available pre-trained SAEs."""
    return list(PRETRAINED_SAES.keys())


def _resolve_sae_type(path: Path) -> Type[SAE]:
    """Infer which SAE class to instantiate from the saved config."""
    with open(path / "config.json", "r") as f:
        cfg = json.load(f)

    # BatchTopK checkpoints always store top_k.
    if cfg.get("top_k") is not None:
        return BatchTopKSAE
    return SAE


def _load_from_path(
    path: Path,
    device: str,
    load_history: bool,
) -> Union[SAE, Tuple[SAE, Dict[str, Any]]]:
    sae_type = _resolve_sae_type(path)
    return sae_type.load(path, device=device, load_history=load_history)


def load_pretrained(
    name_or_path: str,
    device: str = "cpu",
    load_history: bool = False,
    use_local: bool = False
) -> Union[SAE, Tuple[SAE, Dict[str, Any]]]:
    """
    Load a pre-trained SAE by name (from HF) or a local path.

    - If `name_or_path` is a directory, load directly from disk.
    - Otherwise, look up the name in PRETRAINED_SAES and download from Hugging Face if needed.
    """
    path = Path(name_or_path)
    if path.exists():
        return _load_from_path(path, device=device, load_history=load_history)

    if name_or_path not in PRETRAINED_SAES:
        available = ", ".join(sorted(PRETRAINED_SAES.keys()))
        raise ValueError(f"Unknown model '{name_or_path}'. Available: {available}")

    model_folder = PRETRAINED_SAES[name_or_path]

    if use_local:
        local_path = Path(__file__).parent / "pretrained_models" / model_folder
        if local_path.exists():
            return _load_from_path(local_path, device=device, load_history=load_history)

    model_dir = snapshot_download(
        repo_id=HF_REPO_ID,
        allow_patterns=f"{model_folder}/*",
    )
    full_path = Path(model_dir) / model_folder
    return _load_from_path(full_path, device=device, load_history=load_history)
