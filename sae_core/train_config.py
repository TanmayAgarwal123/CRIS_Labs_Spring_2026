import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from tqdm import tqdm
from transformer_lens import HookedTransformer

from sae_core.sae_base import SAE


@dataclass
class TrainingConfig:
    """Configuration for SAE training"""
    num_epochs: int = 10
    batch_size: int = 32
    lr: float = 1e-3
    l1_coefficient: float = 0.01
    num_dataloader_workers: int = 0
    pin_memory: bool = False
    persistent_workers: bool = False
    
    use_end_to_end: bool = True
    reconstruction_loss_weight: float = 1  # Weight for local reconstruction
    
    use_block_mse: bool = False
    block_mse_weight: float = 0.1     # Might have to turn this into a list if want layer-specific weights
    block_mse_layers: Optional[List[int]] = None  # Which blocks to compute MSE at
    
    use_logit_kl: bool = True
    logit_kl_weight: float = 0.1
    
    log_freq: int = 100

    early_stopping_patience: Optional[int] = None  # epochs without val_loss improvement before stopping
    early_stopping_min_delta: float = 0.0          # required improvement over best val_loss

    activation_batch_size: int = 16
    max_text_length: int = 256
    
    def __post_init__(self):
        """Validate config"""
        if self.use_end_to_end and not (self.use_block_mse or self.use_logit_kl):
            raise ValueError("If use_end_to_end=True, must enable at least one downstream loss")
