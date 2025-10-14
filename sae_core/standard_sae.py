import torch
import torch.nn as nn
from torch import Tensor
from dataclasses import dataclass
from typing import Tuple, Dict, Any
import json
from pathlib import Path

from sae_core.sae_base import SAE


# Need to work on this more
class StandardSAE(SAE):
    """Standard SAE with tied weights and decoder norm constraint"""
    
    def initialize_weights(self):
        """Initialize with decoder norm = 1 and tied weights"""
        super().initialize_weights()
        
        # Normalize decoder columns to unit norm
        with torch.no_grad():
            self.W_dec.data = self.W_dec.data / self.W_dec.norm(dim=1, keepdim=True)
            # Scale encoder accordingly 
            self.W_enc.data = self.W_dec.T.clone()
    
    # Add normalizations at some point:
    # @torch.no_grad()
    # def constrain_decoder_norms(self):
    #     """Constrain decoder norms to 1 (call after each gradient step)"""
    #     self.W_dec.data = self.W_dec.data / self.W_dec.norm(dim=1, keepdim=True).clamp(min=1e-8)