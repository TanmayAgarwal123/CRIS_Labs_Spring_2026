import torch
import torch.nn as nn
from transformer_lens import HookedTransformer
import numpy as np
from typing import List, Dict, Tuple, Optional
from tqdm import tqdm
import heapq

from sae_core.pretrained import load_pretrained


class SAEAnalyzer:
    """Analyze trained SAE performance and feature interpretability"""