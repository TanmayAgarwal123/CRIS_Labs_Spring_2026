# SAE Core

A comprehensive Sparse Autoencoder (SAE) implementation for analyzing transformer language models.

## Overview

This repository contains tools for training and analyzing Sparse Autoencoders on transformer models to understand their internal representations. SAEs learn sparse, interpretable features from model activations, enabling mechanistic interpretability research.

## Features

- **SAE Training**: Train SAEs on various transformer models (GPT-2, Qwen3)
- **Comprehensive Analysis**: Evaluate SAE performance with sparsity metrics, reconstruction quality, and ablation studies
- **Data Processing**: Tools for processing and preparing text data for training
- **Pretrained Models**: Pre-trained SAEs for immediate analysis
- **Flexible Configuration**: Configurable training parameters and model architectures

## Project Structure

```
sae_core/
├── sae_base.py              # Core SAE implementation
├── sae_config.py            # SAE configuration classes
├── training.py              # Training utilities
├── analysis.py              # SAE analysis tools
├── model_training/          # Model-specific training scripts
│   ├── gpt2_sae_training.py
│   └── Qwen_sae_training.py
├── data_processing/         # Text data processing utilities
├── pretrained_models/       # Pre-trained SAE models
└── utils/                   # Utility functions
```

## Quick Start

### Training an SAE

```python
from sae_core.sae_base import SAE
from sae_core.sae_config import SAEConfig
from sae_core.sae_train import SAETrainer

# Configure SAE
config = SAEConfig(
    d_in=768,           # Model dimension
    d_sae=3072,         # SAE dimension (4x expansion)
    l1_coefficient=0.01 # Sparsity penalty
)

# Train SAE
trainer = SAETrainer(model, sae_class=SAE, sae_config=config)
history = trainer.train(texts=your_text_data)
```

### Analyzing an SAE

```python
from sae_core.analysis import SAEAnalyzer

# Load analyzer
analyzer = SAEAnalyzer(
    model=your_model,
    sae_path="path/to/pretrained/sae",
    layer=12,
    hook_name="hook_resid_post",
    dataset=your_text_data
)

# Run full analysis
results = analyzer.run_full_analysis()
```

## Key Components

- **SAE**: Base sparse autoencoder implementation with encoder/decoder architecture
- **SAEAnalyzer**: Comprehensive analysis suite including sparsity metrics, reconstruction quality, and ablation studies
- **SAETrainer**: Training pipeline with support for end-to-end training and multiple loss functions
- **Data Processing**: Utilities for processing text data from various sources

## Pretrained Models

The repository includes several pre-trained SAEs:
- GPT-2 models trained on different layers
- Qwen3-0.6B models with various sparsity configurations
- Models trained on chemistry textbook data

## Requirements

- PyTorch
- TransformerLens
- NumPy
- tqdm

