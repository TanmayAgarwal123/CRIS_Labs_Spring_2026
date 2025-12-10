# Pipeline Scaling Changes

This document summarizes the internal changes made to keep the SAE pipeline
transparent while making it practical to scale to more layers and larger Qwen3
models. Everything is still configured via regular Python constants so you can
inspect and tweak behaviour without going through a CLI.

## 1. Streaming token windows for training (`sae_core/sae_train.py`)

- `WindowedTextDataset` now streams random windows from each raw text instead of
  pre-tokenizing and truncating everything up front. Each `__getitem__` call
  runs the HuggingFace tokenizer and, if the sequence is longer than
  `TrainingConfig.max_text_length`, samples a random contiguous window of that
  length. This keeps memory flat and exposes different parts of long documents
  across epochs.
- `pad_collate` handles padding inside the `DataLoader`, using the tokenizer's
  PAD id when available (or EOS as a fallback). There is no hidden batching
  logic—everything lives in `sae_train.py` so you can see exactly how padding
  works.
- `TrainingConfig` gained `num_dataloader_workers`, `pin_memory`, and
  `persistent_workers` knobs. They default to the original single-worker
  behaviour but can be bumped when you want asynchronous data loading.

## 2. Model loading & precision control (`sae_core/model_training/Qwen_sae_training.py`)

- The script now exposes a `MODEL_LOAD_CONFIG` dictionary next to
  `MODEL_NAME`. You can set `device`, `dtype`, `n_devices`, and any
  HuggingFace-specific kwargs (e.g., `device_map`, `load_in_4bit` or
  `torch_dtype`). `HookedTransformer.from_pretrained` receives these exact
  values so you can shard or quantize larger checkpoints without digging into
  the trainer internals.
- All other hyperparameters remain hard-coded in the script, so scaling to a new
  layer/model is as simple as editing this file.

## 3. Analysis pipeline scalability (`sae_core/full_analysis.py`)

- **Activation collection:** instead of storing every `(row, col, value)` tuple
  in Python lists, the collector now builds CSR arrays (`indptr`, `indices`,
  `data`) on the fly. This reduces memory overhead and keeps token order intact.
- **Similarity & co-occurrence:** both matrices are now computed chunk by chunk
  and stored directly to on-disk `.npy` memmaps via `numpy.lib.format.open_memmap`.
  You still get full square matrices for downstream tooling, but the peak RAM
  usage scales with `chunk_size × n_features` rather than `n_features²`.
    - `compute_feature_similarity(..., chunk_size=1024)` handles cosine/dot and
      negative Euclidean metrics by multiplying the decoder weights in slices.
    - `compute_feature_cooccurrence(..., chunk_size=512)` turns the activation
      database into a binary `csr_matrix` once, then multiplies blocks to obtain
      correlation, Jaccard, or PMI scores.
- Both methods print where the resulting `.npy` file lives, so you can inspect
  or memory-map it later without recomputation. All existing plotting utilities
  work transparently because `numpy.memmap` behaves like an `ndarray`.

## 4. Training loop integration (`sae_core/training.py`)

- The training loop itself did not need structural changes; it automatically
  consumes the variable-length batches emitted by the new dataset thanks to the
  existing PAD masking logic. Any adjustments to batch size or gradient budget
  can continue to be made via `TrainingConfig` inside your training script.

With these changes the pipeline remains explicit (all knobs are plain Python
constants), but you avoid the obvious bottlenecks that would make larger runs
impractical.
