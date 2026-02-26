# SAE Training + Tracking Guide

This guide is the practical, end-to-end workflow for training Sparse Autoencoders (SAEs) in this repo and tracking runs with Weights & Biases (W&B).

Use this to understand:

- preparing the training dataset
- running a single SAE training job
- running the Qwen3 batch pipeline
- monitoring progress in W&B (without uploading every checkpoint)
- exporting final models and uploading them to Hugging Face

Note: the top-level `SAELens/README.md` is marked out of date. For training, use this file.

## What lives in this folder

- `single_sae_training.py`: flexible single-run entrypoint (any supported model, configurable hook layer, `batch_topk` or standard SAE).
- `Qwen3_all_sae_training.py`: batch pipeline that trains one BatchTopK SAE per selected Qwen3 model.
- `eval_sae_minibatch.py`: ad hoc minibatch evaluation script.
- `wandb_utils.py`: shared W&B helpers used by the training scripts.

## How the training pipeline works (high level)

1. Load processed text data from JSON (`list[str]`).
2. Split into train/validation sets.
3. Load the base transformer (TransformerLens `HookedTransformer`).
4. Choose a hook location (`blocks.<layer>.<hook_name>`).
5. Build an SAE + training config.
6. Train with checkpointing and validation (training uses random-crop windows; validation uses deterministic windows).
7. Track epoch metrics in W&B (optional).
8. Reload the best checkpoint (if available) and export the final SAE directory.
9. Upload final exported SAE to Hugging Face (optional but you should do this).

By design, W&B tracking logs metrics and (optionally) the final exported SAE artifact only.
Training now samples random crops from cached tokenized texts to reduce boundary-aligned "position-0" features.

## Repo map (training-relevant files)

- `sae_core/model_training/single_sae_training.py`: CLI args, model loading, run orchestration.
- `sae_core/model_training/Qwen3_all_sae_training.py`: multi-model Qwen3 orchestration.
- `sae_core/sae_train.py`: dataset windowing + dataloader setup + trainer wrapper.
- `sae_core/training.py`: core optimization loop, metrics, validation, checkpointing, W&B epoch logging.
- `sae_core/sae_base.py`: SAE modules and save/load format (`weights.pt`, `config.json`, `history.json`).
- `sae_core/data_processing/textbook_process.py`: builds the default processed training dataset.

## 1) Choose and verify your Python environment

You can use either a local `venv` or a Conda environment.

### Option A: `venv` (project-local)

From the repository root (`SAELens`):

```bash
python -m venv .venv
source .venv/bin/activate
```

### Option B: Conda

List envs:

```bash
conda info --envs
```

Activate one:

```bash
conda activate sae_lab_project
```

Important: Conda envs are activated with `conda activate <name>`, not `source .<env>/bin/activate`.

### Verify what environment you are actually using

Run these before installing or logging into services:

```bash
echo $CONDA_DEFAULT_ENV
echo $VIRTUAL_ENV
which python
python -c "import sys; print(sys.executable)"
python -m pip -V
```

This avoids the common issue where `wandb` is installed/logged in on a different interpreter than the one used for training.

## 2) Install dependencies

From the repository root (`SAELens`):

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### W&B login compatibility note (important)

If `wandb login` fails with an error like:

- `API key must be 40 characters long, yours was ...`

then your active environment is using an older `wandb` version that rejects newer API keys.

Upgrade in the same environment you will train in:

```bash
python -m pip install --upgrade "wandb>=0.22.3"
```

Verify:

```bash
python -c "import wandb; print(wandb.__version__)"
```

## 3) Optional service logins (W&B + Hugging Face)

### W&B (for run tracking)

Log in using the active Python interpreter:

```bash
python -m wandb login
```

Optional environment defaults:

```bash
export WANDB_PROJECT="sae-training"
export WANDB_ENTITY="<your_wandb_team_or_username>"
```

Offline mode (store locally, sync later):

```bash
export WANDB_MODE=offline
```

### Hugging Face (for final model uploads)

If you want to upload trained SAEs:

```bash
python -m pip install huggingface_hub
huggingface-cli login
export SAE_HF_REPO_ID="<your_username>/Qwen3_SAEs"
```

## 4) Prepare training data

The default training data file used by both scripts is:

- `sae_core/data/processed_data/processed_textbooks_all.json`

This should be a JSON file containing a `list[str]`.

### Build the default dataset (textbook chapters)

The processing script reads Markdown chapter files from:

- `sae_core/data/raw_data/physics_chapters/*.md`
- `sae_core/data/raw_data/chemistry_chapters/*.md`
- `sae_core/data/raw_data/biology_chapters/*.md`

Then writes:

- `sae_core/data/processed_data/processed_textbooks_all.json`

Run:

```bash
python sae_core/data_processing/textbook_process.py
```

### Use your own dataset instead

If you already have a JSON list of strings, point the training scripts at it:

```bash
python sae_core/model_training/single_sae_training.py \
  --data-path path/to/your_dataset.json
```

## 5) Quick smoke test (recommended before long runs)

Run a short training job first to verify:

- model download/loading works
- dataset path is valid
- W&B logging appears
- checkpoints and final export are written

Example (small/fast-ish validation run):

```bash
python sae_core/model_training/single_sae_training.py \
  --num-epochs 1 \
  --batch-size 2 \
  --activation-batch-size 8 \
  --max-text-length 128 \
  --log-freq 10 \
  --wandb \
  --wandb-project sae-training \
  --run-name smoke_test_sae
```

Apple Silicon tip: use `--device mps` if autodetection does not pick it.

CUDA-only memory tip: `--load-in-4bit` can reduce memory pressure, but depends on your environment/tooling.

## 6) Train a single SAE (recommended default workflow)

Default run (Qwen3-0.6B, auto-selected middle layer, BatchTopK SAE):

```bash
python sae_core/model_training/single_sae_training.py
```

See all options:

```bash
python sae_core/model_training/single_sae_training.py --help
```

### Common single-run examples

Train on a different model:

```bash
python sae_core/model_training/single_sae_training.py \
  --model-name google/gemma-2-2b
```

Train on a fixed layer instead of auto-middle:

```bash
python sae_core/model_training/single_sae_training.py \
  --model-name Qwen/Qwen3-1.7B \
  --hook-layer 12 \
  --hook-name hook_resid_post
```

Train a standard SAE instead of BatchTopK:

```bash
python sae_core/model_training/single_sae_training.py \
  --sae-type standard \
  --sparsity-penalty 0.01
```

Lower memory pressure:

```bash
python sae_core/model_training/single_sae_training.py \
  --batch-size 2 \
  --activation-batch-size 8 \
  --max-text-length 256
```

Custom run naming:

```bash
python sae_core/model_training/single_sae_training.py \
  --run-name qwen3_1p7b_layer12_btop128_exp4_test
```

### Single-run W&B tracking

Enable W&B logging:

```bash
python sae_core/model_training/single_sae_training.py \
  --wandb \
  --wandb-project sae-training
```

Add tags and notes:

```bash
python sae_core/model_training/single_sae_training.py \
  --wandb \
  --wandb-project sae-training \
  --wandb-tags qwen3 baseline exp4 \
  --wandb-notes "Middle-layer BatchTopK SAE baseline"
```

Offline W&B logging:

```bash
python sae_core/model_training/single_sae_training.py \
  --wandb \
  --wandb-mode offline
```

Log only the final exported SAE as a W&B artifact (no checkpoints):

```bash
python sae_core/model_training/single_sae_training.py \
  --wandb \
  --wandb-log-final-artifact
```

### Single-run Hugging Face upload

Upload the final exported SAE to Hugging Face:

```bash
python sae_core/model_training/single_sae_training.py \
  --upload-to-hf
```

You can combine HF + W&B:

```bash
python sae_core/model_training/single_sae_training.py \
  --wandb \
  --wandb-project sae-training \
  --upload-to-hf
```

## 7) Train all Qwen3 SAEs (batch pipeline)

This script trains one BatchTopK SAE per selected Qwen3 model and uses conservative per-model memory defaults.

Default:

```bash
python sae_core/model_training/Qwen3_all_sae_training.py
```

Limit to selected models:

```bash
python sae_core/model_training/Qwen3_all_sae_training.py \
  --models Qwen/Qwen3-0.6B Qwen/Qwen3-1.7B
```

### Batch pipeline W&B tracking (one run per model)

Enable W&B for all models in the batch run:

```bash
python sae_core/model_training/Qwen3_all_sae_training.py \
  --wandb \
  --wandb-project sae-training
```

Group all per-model runs together in W&B:

```bash
python sae_core/model_training/Qwen3_all_sae_training.py \
  --wandb \
  --wandb-project sae-training \
  --wandb-group qwen3_sae_batch_feb25
```

Log final exported SAE artifacts to W&B (still no checkpoints):

```bash
python sae_core/model_training/Qwen3_all_sae_training.py \
  --wandb \
  --wandb-log-final-artifact
```

### Batch pipeline Hugging Face upload

Upload each final exported SAE after it is saved:

```bash
python sae_core/model_training/Qwen3_all_sae_training.py \
  --upload-to-hf
```

## 8) What gets logged (console, local files, W&B)

### Console output (live)

You will see:

- dataset/model loading messages
- selected hook and SAE dimensions
- `tqdm` batch progress bars
- epoch summaries
- validation summaries (if enabled)
- checkpoint saves / best-model updates

`--log-freq` controls how often the progress bar postfix is updated during an epoch.

### Local metric history (always saved)

Training history is saved into `history.json` in:

- the final exported SAE directory
- checkpoint directories (when checkpoints are written)

Common metrics include:

- `loss`
- `recon_loss`
- `l1_loss`
- `sparsity`
- `recon_contribution`
- `l1_contribution`
- `aux_loss`
- `dead_features`
- `dead_feature_percentage`
- `val_*` versions when validation is enabled

If enabled, additional metrics are also tracked:

- `logit_kl`, `kl_contribution`
- `block_mse_contribution`, `total_post_layer_mse`, and per-layer MSE values

### W&B metrics (epoch aggregates)

When `--wandb` is enabled, the training loop logs epoch-level aggregates such as:

- `train/loss`
- `train/recon_loss`
- `train/l1_loss`
- `train/sparsity`
- `train/dead_features`
- `train/dead_feature_percentage`
- `val/loss` and other `val/*` metrics (if validation is enabled)

The scripts also write final run summary fields (status, final losses, local model path, etc.) to the W&B run summary.

## 9) Output locations and saved artifacts

### Final exported SAE (canonical output)

- Single-run script: `sae_core/pretrained_models/<run_name>/`
- Qwen3 batch script: `sae_core/pretrained_models/<auto_generated_run_name>/`

Each exported SAE directory contains:

- `weights.pt`
- `config.json`
- `history.json`

### Checkpoints (local only by default)

- Single-run script: `sae_core/checkpoints/<run_name>/`
- Qwen3 batch script: `sae_core/checkpoints/<model_id>_layer<layer>_exp<expansion>/`

The trainer periodically saves checkpoints and a best checkpoint:

- `checkpoint_epoch<N>.pt/`
- `best_model.pt/`

Important: these are directories (not single files), even though they end in `.pt`.

After training, the scripts try to reload `best_model.pt/` and export that as the final SAE.

## 10) Most important CLI knobs (quick reference)

### Model + hook selection

- `--model-name`
- `--hook-layer` (0-indexed; omit to auto-pick middle layer)
- `--middle-layer-strategy` (`lower` or `upper`)
- `--hook-name` (default `hook_resid_post`)

### SAE architecture

Single-run script:

- `--sae-type` (`batch_topk` or `standard`)
- `--sae-expansion`
- `--sparsity-penalty`
- `--topk`
- `--topk-aux`

Qwen3 batch script:

- BatchTopK SAE only
- `--sae-expansion`
- `--topk`
- `--sparsity-penalty`

### Training / memory

- `--num-epochs`
- `--batch-size`
- `--activation-batch-size`
- `--max-text-length`
- `--lr`
- `--log-freq`
- `--checkpoint-freq`
- `--load-in-4bit` (environment-dependent)

### End-to-end losses (single-run script)

- `--use-end-to-end` / `--no-use-end-to-end`
- `--use-logit-kl` / `--no-use-logit-kl`
- `--use-block-mse` / `--no-use-block-mse`
- `--logit-kl-weight`
- `--block-mse-weight`

Constraint: if `--use-end-to-end` is enabled, at least one of `--use-logit-kl` or `--use-block-mse` must be enabled.

### Tracking + model publishing

- `--wandb`
- `--wandb-project`
- `--wandb-entity`
- `--wandb-mode` (`online`, `offline`, `disabled`)
- `--wandb-group`
- `--wandb-tags`
- `--wandb-notes`
- `--wandb-log-final-artifact` (final export only; no checkpoint uploads)
- `--upload-to-hf`
- `--hf-repo-id`
- `--hf-private`

## 11) Troubleshooting

### W&B login fails with "API key must be 40 characters long"

Your active environment has an older `wandb` version.

Fix in the same environment you train in:

```bash
python -m pip install --upgrade "wandb>=0.22.3"
python -m wandb login
```

### `wandb` command uses the wrong Python environment

Check what is active:

```bash
which python
which wandb
python -c "import sys, wandb; print(sys.executable); print(wandb.__version__)"
```

Prefer:

```bash
python -m wandb login
```

instead of plain `wandb login`, because it guarantees the CLI runs in the active interpreter.

### `source .envXYZ/bin/activate` fails for a Conda env

That path style is for `venv`, not Conda.

Use:

```bash
conda activate <env_name>
```

### Out-of-memory (OOM)

Reduce memory pressure with one or more of:

- `--batch-size`
- `--activation-batch-size`
- `--max-text-length`
- `--num-epochs` (for smoke tests only)

On compatible CUDA setups, `--load-in-4bit` may also help.

### Hook layer errors / wrong layer index

- `hook_layer` is 0-indexed.
- If omitted, the script chooses the middle layer with `--middle-layer-strategy`.

### `batch_topk` config errors

For `--sae-type batch_topk`, `--topk` must be greater than 0.

### Validation behavior

- Validation uses `--val-fraction` (default `0.1`).
- Validation metrics are only logged if a non-empty validation split exists.

## 12) Suggested first run sequence (copy/paste)

From `SAELens/`:

```bash
# 1) Activate your env (choose one)
source .venv/bin/activate
# or: conda activate sae_lab_project

# 2) Install deps
python -m pip install -r requirements.txt
python -m pip install --upgrade "wandb>=0.22.3"

# 3) Login (optional but recommended for tracking)
python -m wandb login

# 4) Build dataset (if not already present)
python sae_core/data_processing/textbook_process.py

# 5) Smoke test + W&B tracking
python sae_core/model_training/single_sae_training.py \
  --num-epochs 1 \
  --batch-size 2 \
  --activation-batch-size 8 \
  --max-text-length 128 \
  --wandb \
  --wandb-project sae-training \
  --run-name smoke_test_sae

# 6) Real run (example)
python sae_core/model_training/single_sae_training.py \
  --model-name Qwen/Qwen3-0.6B \
  --sae-type batch_topk \
  --topk 128 \
  --sae-expansion 4 \
  --wandb \
  --wandb-project sae-training \
  --upload-to-hf
```

## 13) What to read next (if you want deeper understanding)

- `sae_core/training.py`: exact loss terms, metrics, validation, checkpointing.
- `sae_core/sae_base.py`: SAE and BatchTopKSAE implementation details.
- `sae_core/train_config.py`: training config fields and validation.
- `sae_core/model_training/single_sae_training.py`: all CLI knobs and default values.
