import torch
import torch.nn as nn
from torch import Tensor
from dataclasses import dataclass
from typing import Tuple, Dict, Any
import json
from pathlib import Path

from sae_core.utils.mapping import DTYPE_MAP

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
            "hook_spec": self.hook_spec
        }
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> "SAEConfig":
        if "dtype" in config_dict and isinstance(config_dict["dtype"], torch.dtype):
            config_dict["dtype"] = str(config_dict["dtype"]).replace("torch.", "")
        return cls(**config_dict)