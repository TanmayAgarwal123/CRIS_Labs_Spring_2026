import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from dataclasses import dataclass
from typing import Tuple, Dict, Any, Optional, List
import json
from pathlib import Path
from contextlib import contextmanager
from transformer_lens.hook_points import HookedRootModule, HookPoint

from sae_core.sae_config import SAEConfig


class SAE(nn.Module):
    """Base Sparse Autoencoder"""
    
    def __init__(self, cfg: SAEConfig):
        super().__init__()
        self.cfg = cfg
        self.dtype = cfg.torch_dtype
        self.device = torch.device(cfg.device)
        self.use_error_term = cfg.use_error_term
        self.hook_spec = cfg.hook_spec
        
        self.initialize_weights()

        self.hook_sae_input = HookPoint()       # Input to SAE
        self.hook_sae_acts_pre = HookPoint()    # Before activation fn
        self.hook_sae_acts_post = HookPoint()   # After activation fn (features)
        self.hook_sae_output = HookPoint()      # Final output
        self.hook_sae_recons = HookPoint()      # Reconstruction
        if self.use_error_term:
            self.hook_sae_error = HookPoint()

    def get_hook_spec(self):
        return self.hook_spec
        

    def initialize_weights(self):
        """Initialize encoder and decoder weights"""
        # at some point should add mapping for init method
        W_enc_mat = torch.empty(self.cfg.d_in, self.cfg.d_sae, dtype=self.dtype, device=self.device)
        nn.init.kaiming_normal_(W_enc_mat)
        self.W_enc = nn.Parameter(W_enc_mat)

        self.b_enc = nn.Parameter(torch.zeros(self.cfg.d_sae, dtype=self.dtype, device=self.device))
        
        W_dec_mat = self.W_enc.data.T.clone().detach().contiguous() # clone matrix from encoder weights
        self.W_dec = nn.Parameter(W_dec_mat)

        self.b_dec = nn.Parameter(torch.zeros(self.cfg.d_in, dtype=self.dtype, device=self.device))
        

    def encode(self, x: Tensor) -> Tensor:
        """Encode input to sparse features"""
        # x: [..., d_in] -> [..., d_sae]
        pre_acts = x @ self.W_enc + self.b_enc
        pre_acts = self.hook_sae_acts_pre(pre_acts)
        return torch.relu(pre_acts)  # perhaps create mapping for different act fns?
    

    def decode(self, features: Tensor) -> Tensor:
        """Decode features back to input space"""
        # features: [..., d_sae] -> [..., d_in]
        return features @ self.W_dec + self.b_dec
    

    def forward(self, x: Tensor) -> Tuple[Tensor, Tensor]:
        """Forward pass returning reconstruction and features"""
        x = x.to(self.dtype)
        x = self.hook_sae_input(x)

        features = self.encode(x)
        features = self.hook_sae_acts_post(features)

        x_recon = self.decode(features)
        x_recon = self.hook_sae_recons(x_recon)

        output = self.hook_sae_output(x_recon)

        return output, features
    

    def normalize_decoder(self):
        """Normalize decoder rows to unit norm"""
        with torch.no_grad():
            # W_dec shape = (d_sae, d_in)
            norms = torch.norm(self.W_dec, dim=1, keepdim=True) # shape (d_sae,1)
            self.W_dec.data = self.W_dec.data / (norms + 1e-8)


    def training_forward(self, x: Tensor) -> Dict[str, Tensor]:
        """Forward pass for training, returns losses"""
        x_recon, features = self.forward(x)
        
        # Layer Reconstruction loss (MSE)
        recon_loss = F.mse_loss(x, x_recon)
        
        # Sparsity loss
        l1_loss = features.abs().mean()
        
        # Total layer loss
        # total_loss = recon_loss + self.cfg.l1_coefficient * l1_loss
        
        return {
            # "loss": total_loss,
            "recon_loss": recon_loss,
            "l1_loss": l1_loss,
            "features": features,
            "x_recon": x_recon,
        }
    
    def save(self, path: str, history: Optional[Dict[str, List[float]]] = None):
        """Save model weights and config"""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save weights
        torch.save(self.state_dict(), path / "weights.pt")
        
        # Save config
        with open(path / "config.json", "w") as f:
            json.dump(self.cfg.to_dict(), f)

        # Save history if provided
        if history is not None:
            with open(path / "history.json", "w") as f:
                json.dump(history, f, indent=2)
    
    @classmethod
    def load(cls, path: str, device: str = "cpu", load_history: bool = False):
        """Load model from disk, optionally with training history"""
        path = Path(path)
        
        # Load config
        with open(path / "config.json", "r") as f:
            config_dict = json.load(f)
        config_dict["device"] = device
        cfg = SAEConfig.from_dict(config_dict)
        
        # Create model
        model = cls(cfg)
        
        # Load weights
        state_dict = torch.load(path / "weights.pt", map_location=device)
        model.load_state_dict(state_dict)
        
        # Optionally load history
        history = None
        if load_history and (path / "history.json").exists():
            with open(path / "history.json", "r") as f:
                history = json.load(f)
        
        if load_history:
            return model, history
        return model
