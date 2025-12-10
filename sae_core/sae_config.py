import torch
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class SAEConfig:
    """Config class for SAE"""
    d_in: int       # input dimension
    d_sae: int      # SAE dimension
    l1_coefficient: float = 1  # sparsity penalty
    dtype: str = "float32" 
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    use_error_term: bool = False
    hook_layer: str = "14"
    hook_name: str = "mlp_out"
    hook_spec: str = f"blocks.{hook_layer}.{hook_name}"
    top_k: Optional[int] = None
    top_k_aux: Optional[int] = None
    n_batches_to_dead: int = 200
    aux_penalty: float = 1 / 32

    def __post_init__(self):
        """Keep backwards-compatible aliases and sensible defaults."""
        if self.top_k_aux is None and self.top_k is not None:
            self.top_k_aux = max(1, self.top_k // 2)

    @property
    def torch_dtype(self) -> torch.dtype:
        if isinstance(self.dtype, torch.dtype):
            return self.dtype
        if isinstance(self.dtype, str):
            return getattr(torch, self.dtype)
        return torch.float32
    
    def to_dict(self) -> dict:
        return {
            "d_in": self.d_in,
            "d_sae": self.d_sae,
            "l1_coefficient": self.l1_coefficient,
            "dtype": str(self.dtype).replace("torch.", "") if isinstance(self.dtype, torch.dtype) else self.dtype,
            "device": self.device,
            "use_error_term": self.use_error_term,
            "hook_layer": self.hook_layer,
            "hook_name": self.hook_name,
            "hook_spec": self.hook_spec,
            "topk": self.topk,
            "top_k": self.top_k,
            "top_k_aux": self.top_k_aux,
            "n_batches_to_dead": self.n_batches_to_dead,
            "aux_penalty": self.aux_penalty,
        }
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> "SAEConfig":
        if "dtype" in config_dict and isinstance(config_dict["dtype"], torch.dtype):
            config_dict["dtype"] = str(config_dict["dtype"]).replace("torch.", "")
        return cls(**config_dict)
