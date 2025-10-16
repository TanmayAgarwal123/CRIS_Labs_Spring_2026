import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from transformer_lens import HookedTransformer
# from transformer_lens.utils import get_act_name
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
from sae_core.training import TrainingConfig

from sae_core.data_processing.textbook_process import load_processed_data


# Qwen3 Models: 0.6B, 1.7B, 4B, 8B, 14B
qwen3_06b = HookedTransformer.from_pretrained("qwen3-0.6b")

sae_expansion = 4
sparsity_penalty = 40
recon_weight = 1.0
mse_penalty = 0.001
kl_penalty = 0.01

text_list = load_processed_data('sae_core/data/processed_data/processed_chem_text.json')

hook_layer = '12'
hook_name = 'hook_resid_post'
hook_spec = f'blocks.{hook_layer}.{hook_name}'

QWEN3_SAE_Config = SAEConfig(
    d_in = qwen3_06b.cfg.d_model,
    d_sae = sae_expansion * qwen3_06b.cfg.d_model,
    l1_coefficient = sparsity_penalty,
    dtype = str(qwen3_06b.cfg.dtype).replace("torch.", ""),
    device = "cuda",
    use_error_term = False,
    hook_layer = hook_layer,
    hook_name = hook_name,
    hook_spec = hook_spec
)
print(f'Model dim: {QWEN3_SAE_Config.d_in}, SAE dim: {QWEN3_SAE_Config.d_sae}')

QWEN3_SAE_TRAIN_Config = TrainingConfig(
    num_epochs=15,
    batch_size=8,
    lr=1e-3,
    l1_coefficient=QWEN3_SAE_Config.l1_coefficient,
    use_end_to_end=True,
    reconstruction_loss_weight=recon_weight,
    use_block_mse=True,
    block_mse_weight=mse_penalty,
    use_logit_kl= True,
    logit_kl_weight=kl_penalty,
    log_freq=100,
    activation_batch_size=8,
    max_text_length=64
)

QWEN3_SAE_Trainer = SAETrainer(
    qwen3_06b,
    sae_class=SAE,
    sae_config=QWEN3_SAE_Config,
    train_config=QWEN3_SAE_TRAIN_Config,
    device=QWEN3_SAE_Config.device
)

print("Starting SAE training:")

history = QWEN3_SAE_Trainer.train(texts=text_list[:512])

QWEN3_SAE = QWEN3_SAE_Trainer.sae

# Save model:
model_path = f'sae_core/pretrained_models/qwen3_06B.{QWEN3_SAE_Trainer.hook_spec}.sae.sparsity{sparsity_penalty}.mse{mse_penalty}.kl{kl_penalty}'
QWEN3_SAE.save(model_path, history=history)

print("Finished running! Model and history saved")