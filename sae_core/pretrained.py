from pathlib import Path
from typing import Optional, Union, Tuple, Dict, Any
from sae_core.sae_base import SAE

# TO DO: Save a dictionary of saved models in json, update each time we save a model, load json file 
PRETRAINED_SAES = {
    'gpt2.blocks.5.hook_mlp_out.sae': 'pretrained_models/gpt2.blocks.5.hook_mlp_out.sae',
    'broken_qwen3_06B.blocks.14.hook_mlp_out.sae': 'pretrained_models/broken_qwen3_06B.blocks.14.hook_mlp_out.sae',
    'qwen3_06B.blocks.14.hook_mlp_out.sae': 'pretrained_models/qwen3_06B.blocks.14.hook_mlp_out.sae'
}

def list_pretrained():
    """List available pre-trained SAEs"""
    return list(PRETRAINED_SAES.keys())

def load_pretrained(name: str, device: str = "cpu", load_history: bool=False) -> Union[SAE, Tuple[SAE, Dict[str, Any]]]:
    """
    Load a pre-trained SAE by name.
    
    Args:
        name: Name from PRETRAINED_SAES registry
        device: Device to load model on
        
    Returns:
        Loaded SAE model
    """
    if name not in PRETRAINED_SAES:
        available = ", ".join(PRETRAINED_SAES.keys())
        raise ValueError(f"Unknown model '{name}'. Available: {available}")
    
    path = PRETRAINED_SAES[name]
    
    # Handle both relative and absolute paths
    if not Path(path).is_absolute():
        # Assume relative to this file's directory
        path = Path(__file__).parent / path
    
    return SAE.load(path, device=device, load_history=load_history)