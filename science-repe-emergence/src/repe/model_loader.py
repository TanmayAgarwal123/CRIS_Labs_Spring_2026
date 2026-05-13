"""Load a Qwen3 base model + tokenizer with bf16 (or fp16) and device_map='auto'.

Sets model.eval() and a pad token (Qwen3 doesn't set one by default but
batched activation collection needs one).
"""

import os

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


_DTYPE_MAP = {
    "bfloat16": torch.bfloat16,
    "bf16": torch.bfloat16,
    "float16": torch.float16,
    "fp16": torch.float16,
    "float32": torch.float32,
    "fp32": torch.float32,
}


def load_model_and_tokenizer(
    model_name: str,
    dtype: str = "bfloat16",
    device_map: str = "auto",
):
    torch_dtype = _DTYPE_MAP[dtype]
    hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")

    tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
    # Qwen3 base ships without a pad token; pad with eos for batched inference.
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
    # Left padding makes "last token" trivially position [-1] across the batch.
    tokenizer.padding_side = "left"

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch_dtype,
        device_map=device_map,
        token=hf_token,
    )
    model.eval()

    return model, tokenizer
