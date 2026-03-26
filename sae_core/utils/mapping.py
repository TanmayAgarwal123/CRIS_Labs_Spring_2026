import torch

DTYPE_MAP = {
    "float32": torch.float32,
    "float64": torch.float64,
    "float16": torch.float16,
    "bfloat16": torch.bfloat16,
    "torch.float32": torch.float32,
    "torch.float64": torch.float64,
    "torch.float16": torch.float16,
    "torch.bfloat16": torch.bfloat16,
}

ACT_FN_MAP = {
    "relu": torch.nn.ReLU(),
    "gelu": torch.nn.GELU(),
    "glu": torch.nn.GLU()
}