import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor

from sae_core.sae_config import SAEConfig


class SAE(nn.Module):
    """Base Sparse Autoencoder."""

    def __init__(self, cfg: SAEConfig):
        super().__init__()
        self.cfg = cfg
        self.dtype = cfg.torch_dtype
        self.device = torch.device(cfg.device)
        self.hook_spec = cfg.hook_spec
        self._last_dense_acts: Optional[Tensor] = None
        self.register_buffer(
            "ever_fired",
            torch.zeros(self.cfg.d_sae, dtype=torch.bool, device=self.device),
        )

        self.initialize_weights()

    def get_hook_spec(self) -> str:
        return self.hook_spec

    def initialize_weights(self):
        """Initialize encoder and decoder weights."""
        W_enc_mat = torch.empty(
            self.cfg.d_in,
            self.cfg.d_sae,
            dtype=self.dtype,
            device=self.device,
        )
        nn.init.kaiming_uniform_(W_enc_mat)
        self.W_enc = nn.Parameter(W_enc_mat)

        self.b_enc = nn.Parameter(torch.zeros(self.cfg.d_sae, dtype=self.dtype, device=self.device))

        W_dec_mat = self.W_enc.data.T.clone().detach().contiguous()
        self.W_dec = nn.Parameter(W_dec_mat)

        self.b_dec = nn.Parameter(torch.zeros(self.cfg.d_in, dtype=self.dtype, device=self.device))

    def encode(self, x: Tensor) -> Tensor:
        """Encode input to sparse features."""
        x = x.to(self.dtype)
        pre_acts = x @ self.W_enc + self.b_enc
        return torch.relu(pre_acts)

    def decode(self, features: Tensor) -> Tensor:
        """Decode features back to input space."""
        return features @ self.W_dec + self.b_dec

    def forward(self, x: Tensor) -> Tuple[Tensor, Tensor]:
        """Forward pass returning reconstruction and features."""
        x = x.to(self.dtype)
        x = x - self.b_dec

        features = self.encode(x)
        x_recon = self.decode(features)
        self._last_dense_acts = features

        return x_recon, features

    def normalize_decoder(self):
        """Normalize decoder rows to unit norm."""
        with torch.no_grad():
            norms = torch.norm(self.W_dec, dim=1, keepdim=True)
            self.W_dec.data = self.W_dec.data / (norms + 1e-8)

    def training_forward(self, x: Tensor) -> Dict[str, Tensor]:
        """Forward pass for training, returns losses."""
        x_recon, features = self.forward(x)

        recon_loss = F.mse_loss(x, x_recon)
        l1_loss = features.abs().mean()

        return {
            "recon_loss": recon_loss,
            "l1_loss": l1_loss,
            "features": features,
            "x_recon": x_recon,
        }

    def update_inactive_features(self, features: Tensor) -> None:
        """Track which features have ever fired; subclasses can extend."""
        fired = (features.detach().sum(dim=0) > 0)
        if hasattr(self, "ever_fired"):
            self.ever_fired |= fired

    def count_dead_features(self) -> int:
        """Number of features that have never fired during training so far."""
        if not hasattr(self, "ever_fired"):
            return 0
        return int((~self.ever_fired).sum().item())

    def dead_feature_percentage(self) -> float:
        if self.cfg.d_sae == 0:
            return 0.0
        return 100 * self.count_dead_features() / self.cfg.d_sae

    def get_auxiliary_loss(self, x: Tensor, x_recon: Tensor) -> Optional[Tensor]:
        """Hook for subclasses that add additional training losses."""
        return None

    def project_decoder_gradients(self) -> None:
        """Hook for subclasses to modify decoder gradients before optimizer.step()."""
        return None

    def save(self, path: str, history: Optional[Dict[str, List[float]]] = None):
        """Save model weights and config."""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        torch.save(self.state_dict(), path / "weights.pt")

        with open(path / "config.json", "w") as f:
            json.dump(self.cfg.to_dict(), f)

        if history is not None:
            with open(path / "history.json", "w") as f:
                json.dump(history, f, indent=2)

    @classmethod
    def load(cls, path: str, device: str = "cpu", load_history: bool = False):
        """Load model from disk, optionally with training history."""
        path = Path(path)

        with open(path / "config.json", "r") as f:
            config_dict = json.load(f)
        config_dict["device"] = device
        cfg = SAEConfig.from_dict(config_dict)

        model = cls(cfg)

        state_dict = torch.load(path / "weights.pt", map_location=device)
        model.load_state_dict(state_dict, strict=False)

        history = None
        if load_history and (path / "history.json").exists():
            with open(path / "history.json", "r") as f:
                history = json.load(f)

        if load_history:
            return model, history
        return model


class BatchTopKSAE(SAE):
    def __init__(self, cfg: SAEConfig):
        super().__init__(cfg)
        if self.cfg.top_k is None:
            raise ValueError("BatchTopKSAE requires cfg.top_k to be set.")
        if self.cfg.top_k_aux is None:
            raise ValueError("BatchTopKSAE requires cfg.top_k_aux to be set.")

        self.top_k = int(self.cfg.top_k)
        self.top_k_aux = int(self.cfg.top_k_aux)
        self.register_buffer(
            "num_batches_not_active",
            torch.zeros(self.cfg.d_sae, dtype=torch.float32, device=self.device),
        )

    def encode(self, x: Tensor) -> Tensor:
        x = x.to(self.dtype)
        pre_acts = x @ self.W_enc
        return torch.relu(pre_acts)

    def forward(self, x: Tensor) -> Tuple[Tensor, Tensor]:
        x = x.to(self.dtype)
        x_cent = x - self.b_dec # center the x

        dense_acts = self.encode(x_cent) # get dense activations
        added_seq_dim = False
        if dense_acts.ndim == 2:
            dense_acts = dense_acts.unsqueeze(1)
            added_seq_dim = True
        self._last_dense_acts = dense_acts  # to save for later

        # Flatten all activations into a single batch dimension
        orig_shape = dense_acts.shape   # [batch, seq_len, d_sae]
        flat_acts = dense_acts.reshape(-1)     # [batch, seq_len, d_sae] --> [batch*seq_len*d_sae]

        B, S, d_sae = orig_shape
        N = B*S

        # Global Batch Top-K:
        k_total = min(N*self.top_k, flat_acts.numel())
        values, indices = torch.topk(flat_acts, k_total, dim=0)

        # sparse activations
        sparse_flat = torch.zeros_like(flat_acts)
        sparse_flat[indices] = values

        sparse_acts = sparse_flat.view(orig_shape)

        x_recon = self.decode(sparse_acts)
        if added_seq_dim:
            x_recon = x_recon.squeeze(1)
            sparse_acts = sparse_acts.squeeze(1)
        return x_recon, sparse_acts

    def update_inactive_features(self, features: Tensor) -> None:
        if not hasattr(self, "num_batches_not_active"):
            return
        with torch.no_grad():
            fired = (features.detach().sum(dim=0) > 0)
            if hasattr(self, "ever_fired"):
                self.ever_fired |= fired
            self.num_batches_not_active += (~fired).float()
            self.num_batches_not_active[fired] = 0.0

    def get_auxiliary_loss(self, x: Tensor, x_recon: Tensor) -> Optional[Tensor]:
        acts = self._last_dense_acts
        if acts is None:
            return None
        if acts.ndim == 2:
            acts = acts.unsqueeze(1)

        # calculate how many of the features were considered dead by our threshold
        dead_mask = self.num_batches_not_active >= self.cfg.n_batches_to_dead   # boolean vector of length d_sae
        dead_count = dead_mask.sum().item()
        if dead_count == 0:
            return None

        # Get only the features that are dead
        acts_dead = acts[:,:, dead_mask]    # [B, S, d_dead]
        if acts_dead.numel() == 0:
            return None
        
        orig_shape = acts_dead.shape
        B, S, d_dead = orig_shape
        
        k_aux = min(self.top_k_aux, d_dead)
        if k_aux <= 0:
            return None
        
        N = B*S
        flat_acts_dead = acts_dead.view(-1) # [N * d_dead]

        # Global aux TopK over dead features
        k_aux_total = min(N*k_aux, flat_acts_dead.numel())
        values, indices = torch.topk(flat_acts_dead, k_aux_total, dim=0)

        sparse_flat = torch.zeros_like(flat_acts_dead)   
        sparse_flat[indices] = values
        sparse_acts = sparse_flat.view(orig_shape)  # [B, S, d_dead]

        # Get the dead features from the decoder matrix iteself
        decoder_slice = self.W_dec[dead_mask]   # [d_dead, d_in]
        x_recon_aux = sparse_acts @ decoder_slice + self.b_dec  # [B, S, d_in]
        if x.ndim == 2:
            x = x.unsqueeze(1)
        if x_recon.ndim == 2:
            x_recon = x_recon.unsqueeze(1)
        residual = (x - x_recon).to(torch.float32)  # the residual is what the SAE failed to explain

        # "Point" dead features at unexplained information
        aux_loss = self.cfg.aux_penalty * (x_recon_aux.to(torch.float32) - residual).pow(2).mean()
        return aux_loss.to(self.dtype)

    def normalize_decoder(self):
        super().normalize_decoder()

    def project_decoder_gradients(self) -> None:
        if self.W_dec.grad is None:
            return
        with torch.no_grad():
            norms = torch.norm(self.W_dec.detach(), dim=1, keepdim=True) + 1e-8
            w_normed = self.W_dec / norms   # row-wise unit vectors, each row vector points in same direction as W_dec, [d_sae, d_in]
            grad_proj = (self.W_dec.grad * w_normed).sum(dim=1, keepdim=True) * w_normed    # column vector [d_sae, 1] of scalar projection coefficients pointing in direction of w_normed
            self.W_dec.grad -= grad_proj
