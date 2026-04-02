#!/bin/bash
#SBATCH --job-name=sae_llm_labels
#SBATCH --output=logs/llm_labeler_%j.out
#SBATCH --error=logs/llm_labeler_%j.err
#SBATCH --time=4:00:00
#SBATCH --ntasks=1
# No GPU needed — this is purely API calls
# Adjust partition as needed:
#SBATCH --partition=cpu

# ---------------------------------------------------------------------------
# Configuration — edit these before submitting
# ---------------------------------------------------------------------------

REPO_ROOT=/scratch/hewittlab/dc3349/SAELens
CONDA_ENV=research

# Path to your feature summaries JSONL (relative to REPO_ROOT)
ANALYSIS_DIR=Qwen_Qwen3-0.6B.blocks.9.hook_resid_post.btop128sae.all_science.exp4.analysis
FEATURE_SUMMARIES=${REPO_ROOT}/${ANALYSIS_DIR}/results/feature_summaries_20251213_151033.jsonl

# Output location
OUTPUT=${REPO_ROOT}/${ANALYSIS_DIR}/results/feature_labels_llm.jsonl

# LLM settings
MODEL=gpt-4o-mini          # or gpt-4o, etc.
TOP_K_EXAMPLES=10           # examples shown to LLM per feature
MIN_EXAMPLES=5              # skip dead/rare features
REQUESTS_PER_MINUTE=500     # stay under OpenAI tier rate limit

# API key — set in your environment or replace with a secrets path
# export OPENAI_API_KEY=sk-...  # do NOT hardcode here

# ---------------------------------------------------------------------------

set -euo pipefail

# Create log dir if it doesn't exist
mkdir -p ${REPO_ROOT}/sae_core/logs

echo "Job ID: ${SLURM_JOB_ID}"
echo "Node: $(hostname)"
echo "Start: $(date)"
echo "Feature summaries: ${FEATURE_SUMMARIES}"
echo "Output: ${OUTPUT}"
echo "Model: ${MODEL}"

# Activate conda env
source $(conda info --base)/etc/profile.d/conda.sh
conda activate ${CONDA_ENV}

# Install openai if not already present (safe to re-run)
pip install -q openai

# Check API key is set
if [ -z "${OPENAI_API_KEY:-}" ]; then
    echo "ERROR: OPENAI_API_KEY is not set. Export it before submitting."
    exit 1
fi

cd ${REPO_ROOT}

python sae_core/llm_feature_labeler.py \
    --feature_summaries "${FEATURE_SUMMARIES}" \
    --output "${OUTPUT}" \
    --model "${MODEL}" \
    --top_k_examples ${TOP_K_EXAMPLES} \
    --min_examples ${MIN_EXAMPLES} \
    --requests_per_minute ${REQUESTS_PER_MINUTE}

echo "End: $(date)"
