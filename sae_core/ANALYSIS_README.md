# SAE Analysis Guide

This guide is the analysis-focused companion to `sae_core/model_training/README.md`.

Use this file if you already trained an SAE (or downloaded one) and want to:

- run quick post-training checks
- run the full corpus activation analysis pipeline
- inspect feature summaries / matrices
- use the exploratory notebook `interp_analysis.ipynb`

For training, use `sae_core/model_training/README.md`.

## What this covers

Analysis entrypoints in `sae_core/`:

- `analysis_short_rerun.py`: quick script (sparsity, dead features, ablation)
- `run_analysis.py`: comprehensive pipeline (activation DB + matrices + metrics + reports)
- `full_analysis.py`: `SAEAnalyzer` implementation used by both
- `interp_analysis.ipynb`: exploratory notebook for feature interpretation and matrix diagnostics

## 1) Prerequisites (what you need before analysis)

You need:

- a base model ID (example: `Qwen/Qwen3-0.6B`)
- a trained/exported SAE directory (contains `weights.pt`, `config.json`, `history.json`)
- the hook layer and hook name used for training
- a dataset JSON (`list[str]`) to analyze on

Important:

- `sae_path` should point to the **exported SAE directory**, not a raw checkpoint typo.
- The base model + hook layer + hook name must match how the SAE was trained.

### Recover hook info from a saved SAE

From `SAELens/`:

```bash
python -m json.tool sae_core/pretrained_models/<run_name>/config.json
```

Look for:

- `hook_layer`
- `hook_name`
- `hook_spec`

Use these exact values in analysis.

## 2) Quick analysis (fast sanity check)

Use `analysis_short_rerun.py` when you want a quick read on a trained SAE before running the heavier pipeline.

It currently runs:

- sparsity metrics
- dead-feature detection
- ablation study

It does **not** build the corpus activation database.

### Step A: Edit the script constants

Open `sae_core/analysis_short_rerun.py` and update:

- `MODEL_NAME`
- `SAE_PATH`
- the `layer` passed to `SAEAnalyzer(...)`
- dataset path in `load_processed_data(...)` (if needed)

### Step B: Run it

From `SAELens/`:

```bash
python sae_core/analysis_short_rerun.py
```

This prints metrics to the console only.

## 3) Comprehensive analysis (includes corpus token activations)

Use `run_analysis.py` for the full end-to-end analysis workflow. This is the path that performs the corpus-wide token activation pass after training.

The script:

1. loads model + SAE + dataset
2. builds an activation database over the corpus (`collect_all_activations`)
3. computes feature similarity matrix
4. computes feature co-occurrence matrix
5. runs metrics (sparsity, dead features, reconstruction, ablation)
6. writes plots, JSON results, and a human-readable summary

### Option A: Edit constants in `run_analysis.py`

Open `sae_core/run_analysis.py` and update the values in the `__main__` block:

- `MODEL_NAME`
- `SAE_PATH`
- `LAYER`
- `HOOK_NAME`
- `DATA_PATH`
- `BATCH_SIZE`
- `ANALYSIS_DIR`

Then run:

```bash
python sae_core/run_analysis.py
```

### Option B (recommended): Call `run_comprehensive_analysis(...)` directly

This avoids editing the file every time.

From `SAELens/`:

```bash
python - <<'PY'
from sae_core.run_analysis import run_comprehensive_analysis

run_comprehensive_analysis(
    model_name="Qwen/Qwen3-0.6B",
    sae_path="sae_core/pretrained_models/<run_name>",
    layer=13,  # replace with your hook layer
    hook_name="hook_resid_post",
    data_path="sae_core/data/processed_data/processed_textbooks_all.json",
    batch_size=8,
    analysis_dir="analysis/<run_name>"
)
PY
```

## 4) Outputs from the comprehensive pipeline

`run_analysis.py` creates an analysis output directory (your `analysis_dir`) with subfolders:

- `activation_database/`
- `matrices/`
- `plots/`
- `results/`

Typical outputs:

- `activation_database/activation_db_<timestamp>.pkl`
- `matrices/feature_similarity_<timestamp>.npy`
- `matrices/feature_cooccurrence_<timestamp>.npy`
- `results/analysis_results_<timestamp>.json`
- `results/feature_summaries_<timestamp>.jsonl`
- `plots/training_history.png` (if training history exists)
- `SUMMARY_<timestamp>.json`
- `README_<timestamp>.md`

These outputs are what the notebook is intended to inspect.

## 5) Notebook workflow (`interp_analysis.ipynb`)

`interp_analysis.ipynb` is an exploratory interpretation notebook for:

- loading `feature_summaries_*.jsonl`
- plotting feature statistics
- loading and visualizing similarity / co-occurrence matrices
- inspecting clusters and co-activating features
- loading the saved activation DB for deeper diagnostics

### Important: the notebook is not parameterized yet

The notebook currently contains hard-coded example paths and timestamps from a prior run. You will need to edit the setup cells for your run.

In particular, update path cells that reference:

- `feature_summaries_*.jsonl`
- `.../matrices/feature_similarity_*.npy`
- `.../matrices/feature_cooccurrence_*.npy`
- `activation_database/activation_db_*.pkl`
- `sae_path` (if you load the SAE inside the notebook)

### Recommended order of operations

1. Run `run_analysis.py` (or `run_comprehensive_analysis(...)`) first.
2. Confirm your `analysis_dir` contains `results/`, `matrices/`, and `activation_database/`.
3. Open `interp_analysis.ipynb`.
4. Update the notebook path variables to point at your analysis outputs.
5. Run cells top-to-bottom (it is stateful and exploratory; later cells depend on earlier variables).

### Launching Jupyter

From `SAELens/`:

```bash
jupyter lab sae_core/interp_analysis.ipynb
```

or

```bash
jupyter notebook sae_core/interp_analysis.ipynb
```

If Jupyter is not installed in your environment:

```bash
python -m pip install jupyterlab
```

Some notebook cells also use packages like `seaborn`, `scikit-learn`, and `scipy`. Install missing packages in the same environment if needed.

## 6) Minimal end-to-end analysis flow (copy/paste)

From `SAELens/`:

```bash
# 1) Quick sanity check (edit constants in script first)
python sae_core/analysis_short_rerun.py

# 2) Comprehensive analysis (writes activation DB + matrices + summaries)
python - <<'PY'
from sae_core.run_analysis import run_comprehensive_analysis

run_comprehensive_analysis(
    model_name="Qwen/Qwen3-0.6B",
    sae_path="sae_core/pretrained_models/<run_name>",
    layer=13,
    hook_name="hook_resid_post",
    data_path="sae_core/data/processed_data/processed_textbooks_all.json",
    batch_size=8,
    analysis_dir="analysis/<run_name>"
)
PY

# 3) Open notebook for interpretation (edit path cells to your outputs)
jupyter lab sae_core/interp_analysis.ipynb
```

## 7) Resource notes (important)

### Activation DB collection can be heavy

`collect_all_activations(...)` processes the entire corpus through the base model and stores sparse SAE activations for every token. This can be expensive in:

- GPU time (model forward passes)
- CPU time (sparse matrix construction / indexing)
- RAM (token metadata + indices)
- disk (activation DB pickle + matrices)

If you only need a quick quality check, run `analysis_short_rerun.py` first.

### Matrix steps scale with `d_sae`

Similarity and co-occurrence are `d_sae x d_sae` matrices. Larger SAEs make these steps slower and larger on disk.

If needed:

- reduce `batch_size`
- skip the full pipeline and call only the `SAEAnalyzer` methods you need
- use the notebook only after generating the necessary outputs

## 8) Common analysis issues

### Wrong `sae_path`

Point `sae_path` to the exported SAE directory (with `weights.pt`, `config.json`, `history.json`).

### Hook mismatch (layer / hook name)

Analysis must use the same base model + layer + hook used during training.

### Notebook path errors

The notebook contains hard-coded example paths. Update all path variables in the setup/loading cells to your run’s timestamps and directory names.

### Slow notebook cells

Some cells load large matrices / activation DBs and do clustering or diagnostics. That is expected for larger SAEs.
