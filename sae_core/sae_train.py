import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from transformer_lens import HookedTransformer
from transformer_lens.utils import get_act_name
import numpy as np
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import json
from dataclasses import dataclass
from tqdm import tqdm

from sae_core.sae_base import SAE
from sae_core.sae_config import SAEConfig
from sae_core.standard_sae import StandardSAE
from sae_core.training import train_sae, compute_kl_divergence
from sae_core.activation_collection import ActivationBuffer, ActivationCollector, ActivationDataset
from sae_core.train_config import TrainingConfig


class SAETrainer:    
    def __init__(
        self,
        model: HookedTransformer,
        sae_class: SAE,
        sae_config: SAEConfig,
        train_config: TrainingConfig,
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        """
        Args:
            model: TransformerLens model (GPT-2, Qwen3, etc.)
            hook_spec: Hook point like "blocks.6.hook_mlp_out"
            sae_class: Which SAE variant to use
            sae_expansion: Hidden dimension multiplier
        """
        self.model = model
        self.hook_spec = sae_config.hook_spec
        self.device = device

        self.sae_cfg = sae_config
        self.train_cfg = train_config
        
        self.sae = sae_class(self.sae_cfg)
        
    def train(self, texts:List[str]):
        # Tokenize
        tokens = [
            self.model.to_tokens(t, prepend_bos=True)[0, : self.train_cfg.max_text_length]
            for t in texts
        ]

        print(f"Token dtype: {tokens[0].dtype}")
        print(f"Sample tokens: {tokens[0][:10]}")

        def collate_fn(batch_indices):
            indices = [idx[0].item() if isinstance(idx, tuple) else idx for idx in batch_indices]
            batch_tokens = [tokens[i] for i in indices]
            max_len = max(len(t) for t in batch_tokens)
            padded = torch.stack([
                torch.nn.functional.pad(t, (0, max_len - len(t)), value=int(self.model.tokenizer.pad_token_id))
                for t in batch_tokens
            ])
            padded = padded.long()
        
            # Debugging
            # print(f"Batch dtype after collate: {padded.dtype}, shape: {padded.shape}")
            
            return padded
        
        dataset = torch.utils.data.TensorDataset(torch.arange(len(tokens)))

        loader = DataLoader(dataset, batch_size = self.train_cfg.batch_size, shuffle=True, collate_fn=collate_fn)

        return train_sae(self.sae, self.model, loader, self.train_cfg)
    
print("all the way through")