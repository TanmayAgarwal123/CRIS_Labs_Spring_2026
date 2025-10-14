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
from sae_core.training import train_sae

# NOTE: NOT CURRENTLY USING IN IMPLEMENTATION, SAELENS USES THIS SO MIGHT BE USEFUL LATER

# Class that collects activations on a forward pass (lower level storage in memory)
class ActivationBuffer:
    """Stores activations from a TransformerLens model"""
    
    def __init__(self, hook_spec: str, max_size: int = 5000000):
        """
        Args:
            hook_spec: Hook specification e.g. "blocks.6.hook_mlp_out"
            max_size: Maximum activation vectors to store
        """
        self.hook_spec = hook_spec  # should include layer and hook name
        self.max_size = max_size
        self.activations = [] 
        self.current_size = 0
        
    def hook_fn(self, activations: torch.Tensor, hook):
        """Generic hook function"""
        # Reshape activations:
        if len(activations.shape) == 4:  # [batch, seq, heads, d_head]
            batch, seq_len, n_heads, d_head = activations.shape
            acts = activations.reshape(batch * seq_len, n_heads * d_head)
        elif len(activations.shape) == 3:  # [batch, seq, d_model]
            batch, seq_len, d_model = activations.shape
            acts = activations.reshape(batch * seq_len, d_model)
        else:
            raise ValueError(f"Unexpected activation shape: {activations.shape}")
        
        acts = acts.detach().cpu()
        
        # Add activations to buffer:
        if self.current_size + acts.shape[0] <= self.max_size:
            self.activations.append(acts)
            self.current_size += acts.shape[0]
        else:
            print("Warning! Activation storage full, didn't add vectors to collection")
        
        return activations
    
    def get_activations(self) -> torch.Tensor:
        if not self.activations:
            raise ValueError("No activations collected")
        return torch.cat(self.activations, dim=0)
    
    def clear(self):
        self.activations = []
        self.current_size = 0


class ActivationDataset(Dataset):
    """Dataset wrapper for activations"""
    
    def __init__(self, activations: torch.Tensor):
        self.activations = activations 
    
    def __len__(self):
        return len(self.activations)
    
    def __getitem__(self, idx):
        return self.activations[idx]


class ActivationCollector:
    """Collects activations from a TransformerLens model"""
    
    def __init__(self, model: HookedTransformer, hook_spec: str, device: str = "cuda"):
        """
        Args:
            model: Any TransformerLens model
            hook_spec: Hook point like "blocks.6.hook_mlp_out"
        """
        self.model = model
        self.hook_spec = hook_spec
        self.device = device
        self.buffer = ActivationBuffer(hook_spec)
        
        # Determine activation dimension
        if "hook_z" in hook_spec:
            self.d_activation = model.cfg.n_heads * model.cfg.d_head    # I wonder if I'll need a separate model.cfg class
        else:
            self.d_activation = model.cfg.d_model
    
    def collect(
        self, 
        texts: List[str], 
        batch_size: int = 16,
        max_length: int = 128
    ) -> torch.Tensor:
        """Collect activations from texts"""
        print(f"Collecting activations from {self.hook_spec}...")
        self.buffer.clear()
        
        for i in tqdm(range(0, len(texts), batch_size)):    # tqdm to show progress bar
            batch_texts = texts[i:i+batch_size]     # Create batch
            tokens = self.model.to_tokens(batch_texts)     # tokenize batch using built-in TFLens fn
            
            # Temporarily attach the buffer's hook fn to specified layer:
            with self.model.hooks([(self.hook_spec, self.buffer.hook_fn)]):     # model.hooks gets pre-defined hook points from TFLens
                _ = self.model(tokens)  # pass tokens through foward pass, buffer.hook_fun gets called and stores activations each time layer activates
        
        activations = self.buffer.get_activations()     # Retrieve all collected activations concatenated into tensor
        print(f"Collected {activations.shape[0]} vectors of dimension {activations.shape[1]}")
        return activations



# print("Went all the way through!")