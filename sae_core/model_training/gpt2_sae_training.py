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
import re
import requests

from sae_core.sae_base import SAE
from sae_core.sae_config import SAEConfig
from sae_core.standard_sae import StandardSAE
from sae_core.training import train_sae
from sae_core.sae_train import SAETrainer

from SAELens.sae_core.data_processing.textbook_process import load_processed_data


gpt2_small = HookedTransformer.from_pretrained("gpt2-small")

sae_expansion = 4

text_list = load_processed_data('sae_core/data/processed_data/processed_chem_text.json')


GPT2_SAE_Config = SAEConfig(
    d_in = gpt2_small.cfg.d_model,
    d_sae = sae_expansion * gpt2_small.cfg.d_model,
    l1_coefficient = 0.01,
    dtype = gpt2_small.cfg.dtype,
    device = "cuda" # should be able to use cpu if needed
)
print(f'Model dim: {GPT2_SAE_Config.d_in}, SAE dim: {GPT2_SAE_Config.d_sae}')


# TO DO: Build TrainConfig
GPT2_SAE_Trainer = SAETrainer(
    gpt2_small,
    hook_spec = 'blocks.5.hook_mlp_out',
    sae_class = SAE,
    sae_expansion = sae_expansion,
    device = GPT2_SAE_Config.device
)

print("Starting SAE training:")

history = GPT2_SAE_Trainer.collect_and_train(
    texts=text_list[:1000],
    num_epochs=10,
    batch_size=32,
    lr=1e-3,
    l1_coefficient=GPT2_SAE_Config.l1_coefficient,
    max_text_length=56,
    activation_batch_size=16
)

GPT2_SAE = GPT2_SAE_Trainer.sae

# Save model:
model_path = f'sae_core/pretrained_models/gpt2.{GPT2_SAE_Trainer.hook_spec}.sae'
GPT2_SAE.save(model_path)

# GPT2_SAE_Trainer.intervene()
