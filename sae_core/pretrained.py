from pathlib import Path
from typing import Optional, Union, Tuple, Dict, Any
from sae_core.sae_base import SAE
from huggingface_hub import hf_hub_download, snapshot_download
import os

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
    # New SAEs:
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity40.mse0.001.kl0.01.physics10': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity40.mse0.001.kl0.01.physics10',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity40.mse0.001.kl0.01.physics10.exp8': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity40.mse0.001.kl0.01.physics10.exp8',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity60.mse0.001.kl0.01.physics10.exp8': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity60.mse0.001.kl0.01.physics10.exp8',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity200.mse0.001.kl0.01.physics.exp4': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity200.mse0.001.kl0.01.physics.exp4',
    'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity100.mse0.001.kl0.01.physics.exp4': 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity100.mse0.001.kl0.01.physics.exp4'
}

def list_pretrained():
    """List available pre-trained SAEs"""
    return list(PRETRAINED_SAES.keys())

def load_pretrained(name: str, device: str = "cpu", load_history: bool = False, use_local: bool = False) -> Union[SAE, Tuple[SAE, Dict[str, Any]]]:
    """
    Load a pre-trained SAE by name from Hugging Face.
    
    Args:
        name: Name from PRETRAINED_SAES registry
        device: Device to load model on
        load_history: Whether to load training history
        use_local: If True, try to load from local pretrained_models/ folder first
        
    Returns:
        Loaded SAE model (and optionally training history)
    """
    if name not in PRETRAINED_SAES:
        available = ", ".join(PRETRAINED_SAES.keys())
        raise ValueError(f"Unknown model '{name}'. Available: {available}")
    
    model_folder = PRETRAINED_SAES[name]
    
    # Option to use local files (for development)
    if use_local:
        local_path = Path(__file__).parent / "pretrained_models" / model_folder
        if local_path.exists():
            return SAE.load(local_path, device=device, load_history=load_history)
    
    # Download entire model folder from Hugging Face (includes weights, config, history, etc.)
    # This automatically caches to ~/.cache/huggingface/hub/
    model_dir = snapshot_download(
        repo_id=HF_REPO_ID,
        allow_patterns=f"{model_folder}/*",  # Only download this specific model folder
        cache_dir=None,  # Uses default cache location
    )
    
    # The downloaded folder structure mirrors HF, so we need to append the model_folder name
    full_path = Path(model_dir) / model_folder
    
    return SAE.load(full_path, device=device, load_history=load_history)