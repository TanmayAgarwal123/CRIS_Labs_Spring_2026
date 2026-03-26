from pathlib import Path
import json
import numpy as np
from datetime import datetime

import torch
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for remote servers
import matplotlib.pyplot as plt

from sae_core.full_analysis import SAEAnalyzer
from sae_core.pretrained import load_pretrained
from sae_core.data_processing.textbook_process import load_processed_data
from transformer_lens import HookedTransformer


def get_compute_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


DEVICE = get_compute_device()
TORCH_DTYPE = torch.float16 if DEVICE in {"cuda", "mps"} else torch.float32
DTYPE_STR = str(TORCH_DTYPE).replace("torch.", "")
NUM_DEVICES = torch.cuda.device_count() if DEVICE == "cuda" else 1

FROM_PRETRAINED_KWARGS = {
    "trust_remote_code": True,
    "torch_dtype": TORCH_DTYPE,
}
if NUM_DEVICES > 1:
    FROM_PRETRAINED_KWARGS["device_map"] = "auto"

def create_analysis_directories(base_path: str = 'analysis'):
    """Create organized directory structure for analysis outputs"""
    base = Path(base_path)
    dirs = {
        'base': base,
        'activation_db': base / 'activation_database',
        'matrices': base / 'matrices',
        'plots': base / 'plots',
        'results': base / 'results'
    }
    
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return dirs


def run_comprehensive_analysis(
    model_name: str = "qwen3-0.6b",
    sae_path: str = None,
    layer: int = 9,
    hook_name: str = 'hook_resid_post',
    data_path: str = None,
    batch_size: int = 16,
    analysis_dir: str = 'analysis'
):
    """
    Run complete SAE analysis pipeline with all visualizations
    
    Args:
        model_name: HuggingFace model name
        sae_path: Path to pretrained SAE
        layer: Layer number for hook
        hook_name: Name of hook point
        data_path: Path to processed data JSON
        batch_size: Batch size for processing
        analysis_dir: Base directory for saving outputs
    """
    
    # Create timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n{'='*80}")
    print(f"Starting Comprehensive SAE Analysis - {timestamp}")
    print(f"Running in REMOTE SERVER MODE (no display)")
    print(f"{'='*80}\n")
    
    # Create directory structure
    print("Setting up directory structure...")
    dirs = create_analysis_directories(analysis_dir)
    
    # Save run configuration
    config = {
        'timestamp': timestamp,
        'model_name': model_name,
        'sae_path': sae_path,
        'layer': layer,
        'hook_name': hook_name,
        'data_path': data_path,
        'batch_size': batch_size
    }
    
    with open(dirs['base'] / f'config_{timestamp}.json', 'w') as f:
        json.dump(config, f, indent=2)
    

    # 1. LOAD MODEL, SAE, AND DATA

    print("\n[1/7] Loading model, SAE, and data...")
    
    model = HookedTransformer.from_pretrained(
        model_name,
        device=DEVICE,
        dtype=DTYPE_STR,
        n_devices=max(1, NUM_DEVICES),
        **FROM_PRETRAINED_KWARGS,
    )
    print(f"✓ Loaded model: {model_name}")
    
    sae, history = load_pretrained(sae_path, load_history=True)
    print(f"✓ Loaded SAE from: {sae_path}")
    
    # Save training history
    if history:
        print("\nTraining History Summary:")
        print(f"  Final Loss: {history['loss'][-1]:.4f}")
        print(f"  Final Recon Loss: {history['recon_loss'][-1]:.4f}")
        print(f"  Final L1 Loss: {history['l1_loss'][-1]:.4f}")
        print(f"  Final Sparsity (L0): {history['sparsity'][-1]:.2f}")
        
        # Plot training curves
        fig, axes = plt.subplots(1, 4, figsize=(15, 4))
        
        axes[0].plot(history['loss'])
        axes[0].set_title('Total Loss')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Loss')
        axes[0].grid(True, alpha=0.3)
        
        axes[1].plot(history['recon_loss'])
        axes[1].set_title('Reconstruction Loss')
        axes[1].set_xlabel('Epoch')
        axes[1].grid(True, alpha=0.3)
        
        axes[2].plot(history['l1_loss'])
        axes[2].set_title('L1 Loss')
        axes[2].set_xlabel('Epoch')
        axes[2].grid(True, alpha=0.3)
        
        axes[3].plot(history['sparsity'])
        axes[3].set_title('Sparsity (L0)')
        axes[3].set_xlabel('Epoch')
        axes[3].set_ylabel('Active Features')
        axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(dirs['plots'] / 'training_history.png', dpi=300, bbox_inches='tight')
        plt.close()  # Important: close figure to free memory
        print(f"✓ Saved training history plot")
    
    texts = load_processed_data(data_path)
    print(f"✓ Loaded {len(texts)} texts from: {data_path}")
    

    # 2. INITIALIZE ANALYZER

    print("\n[2/7] Initializing SAE Analyzer...")
    
    analyzer = SAEAnalyzer(
        model=model,
        sae_path=sae_path,
        layer=layer,
        hook_name=hook_name,
        dataset=texts
    )
    print("✓ Analyzer initialized")
    

    # 3. COLLECT ACTIVATIONS

    print("\n[3/7] Collecting activations across corpus...")
    print("This may take a while depending on corpus size...")
    
    activation_db_path = dirs['activation_db'] / f'activation_db_{timestamp}.pkl'
    analyzer.collect_all_activations(
        batch_size=batch_size,
        save_path=str(activation_db_path)
    )
    print(f"✓ Saved activation database to: {activation_db_path}")
    

    # 4. COMPUTE FEATURE SIMILARITY

    print("\n[4/7] Computing feature similarity matrix...")
    
    similarity_path = dirs['matrices'] / f'feature_similarity_{timestamp}.npy'
    analyzer.compute_feature_similarity(
        similarity_metric='cosine',
        save_path=str(similarity_path)
    )
    print(f"✓ Saved similarity matrix to: {similarity_path}")
    

    # 5. COMPUTE FEATURE CO-OCCURRENCE

    print("\n[5/7] Computing feature co-occurrence matrix...")
    print("This may take a while for large feature sets...")
    
    cooccurrence_path = dirs['matrices'] / f'feature_cooccurrence_{timestamp}.npy'
    analyzer.compute_feature_cooccurrence(
        method='correlation',
        save_path=str(cooccurrence_path),
        chunk_size=1000  # Adjust based on available memory
    )
    print(f"✓ Saved co-occurrence matrix to: {cooccurrence_path}")
    

    # 6. RUN FULL METRICS ANALYSIS

    print("\n[6/7] Running full metrics analysis...")
    
    feature_summary_path = dirs['results'] / f'feature_summaries_{timestamp}.jsonl'
    results_path = dirs['results'] / f'analysis_results_{timestamp}.json'
    results = analyzer.run_full_analysis(
        batch_size=batch_size,
        save_path=str(results_path),
        feature_summary_path=str(feature_summary_path),
        feature_summary_top_k=25,
        use_training_dead_metric=True,
    )
    print(f"✓ Saved results to: {results_path}")
    print(f"✓ Saved feature summaries to: {feature_summary_path}")
    

    # 7. GENERATE SUMMARY REPORT

    print("\n[7/7] Generating summary report...")
    
    feature_counts = np.array(results['feature_freq'])
    top_feature_indices = np.argsort(feature_counts)[-10:][::-1]
    
    summary = {
        'timestamp': timestamp,
        'model': model_name,
        'sae_path': sae_path,
        'layer': layer,
        'hook_name': hook_name,
        'dataset_size': len(texts),
        'n_tokens_processed': results['sparsity']['n_tokens'],
        'n_features': results['sparsity']['n_features'],
        'sparsity': {
            'l0_mean': results['sparsity']['l0_mean'],
            'l0_std': results['sparsity']['l0_std'],
            'l1_mean': results['sparsity']['l1_mean'],
            'l1_std': results['sparsity']['l1_std']
        },
        'dead_features': {
            'n_dead': results['dead_features']['n_dead'],
            'pct_dead': results['dead_features']['pct_dead']
        },
        'reconstruction': {
            'mse': results['reconstruction']['mse'],
            'explained_variance': results['reconstruction']['explained_variance'],
            'cosine_similarity': results['reconstruction']['cosine_similarity']
        },
        'ablation': {
            'baseline_loss': results['ablation']['baseline_loss'],
            'zero_ablation_loss': results['ablation']['zero_ablation_loss'],
            'sae_reconstruction_loss': results['ablation']['sae_reconstruction_loss'],
            'loss_recovered': results['ablation']['loss_recovered']
        },
        'top_features': top_feature_indices.tolist(),
        'files': {
            'activation_db': str(activation_db_path.relative_to(dirs['base'])),
            'similarity_matrix': str(similarity_path.relative_to(dirs['base'])),
            'cooccurrence_matrix': str(cooccurrence_path.relative_to(dirs['base'])),
            'results': str(results_path.relative_to(dirs['base'])),
            'feature_summaries': str(feature_summary_path.relative_to(dirs['base']))
        }
    }
    
    summary_path = dirs['base'] / f'SUMMARY_{timestamp}.json'
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Create human-readable summary
    readme_content = f"""
# SAE Analysis Report
Generated: {timestamp}

## Configuration
- Model: {model_name}
- SAE Path: {sae_path}
- Layer: {layer}
- Hook: {hook_name}
- Dataset: {len(texts)} texts

## Key Results

### Sparsity Metrics
- L0 (features/token): {results['sparsity']['l0_mean']:.2f} ± {results['sparsity']['l0_std']:.2f}
- L1: {results['sparsity']['l1_mean']:.4f} ± {results['sparsity']['l1_std']:.4f}
- Tokens processed: {results['sparsity']['n_tokens']:,}

### Dead Features
- Number: {results['dead_features']['n_dead']} / {results['sparsity']['n_features']}
- Percentage: {results['dead_features']['pct_dead']:.1f}%

### Reconstruction Quality
- MSE: {results['reconstruction']['mse']:.6f}
- Explained Variance: {results['reconstruction']['explained_variance']:.4f} ({results['reconstruction']['explained_variance']*100:.2f}%)
- Cosine Similarity: {results['reconstruction']['cosine_similarity']:.4f}

### Ablation Study
- Baseline Loss: {results['ablation']['baseline_loss']:.4f}
- Zero Ablation Loss: {results['ablation']['zero_ablation_loss']:.4f}
- SAE Reconstruction Loss: {results['ablation']['sae_reconstruction_loss']:.4f}
- Loss Recovered: {results['ablation']['loss_recovered']*100:.2f}%

## Top 10 Most Active Features
{', '.join(map(str, top_feature_indices.tolist()))}

See results/{feature_summary_path.name} for per-feature activation contexts.
"""
    
    readme_path = dirs['base'] / f'README_{timestamp}.md'
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✓ Saved summary to: {summary_path}")
    print(f"✓ Saved README to: {readme_path}")
    
    
    # COMPLETION
    
    print(f"\n{'='*80}")
    print(f"Analysis Complete!")
    print(f"{'='*80}")
    print(f"\nAll outputs saved to: {dirs['base']}")
    print(f"View summary: {readme_path}")
    print(f"\nKey Metrics:")
    print(f"  • Sparsity (L0): {results['sparsity']['l0_mean']:.2f} features/token")
    print(f"  • Dead Features: {results['dead_features']['pct_dead']:.1f}%")
    print(f"  • Reconstruction Quality: {results['reconstruction']['explained_variance']*100:.2f}% variance explained")
    print(f"  • Loss Recovered: {results['ablation']['loss_recovered']*100:.2f}%")
    print(f"\n{'='*80}\n")
    
    return analyzer, results, summary


# MAIN EXECUTION
if __name__ == "__main__":
    
    # Configuration
    MODEL_NAME = "qwen3-0.6b"
    SAE_PATH = 'Qwen_Qwen3-0.6B.blocks.9.hook_resid_post.btop128sae.all_science.exp4'
    LAYER = 9
    HOOK_NAME = 'hook_resid_post'
    DATA_PATH = 'sae_core/data/processed_data/processed_textbooks_all.json'
    BATCH_SIZE = 16
    ANALYSIS_DIR = f'{SAE_PATH}.analysis'
    
    try:
        # Run analysis
        analyzer, results, summary = run_comprehensive_analysis(
            model_name=MODEL_NAME,
            sae_path=SAE_PATH,
            layer=LAYER,
            hook_name=HOOK_NAME,
            data_path=DATA_PATH,
            batch_size=BATCH_SIZE,
            analysis_dir=ANALYSIS_DIR
        )
        
        print("✓ Analysis completed successfully!")
        print("Check the analysis/ folder for all outputs.")
        
    except Exception as e:
        print(f"\n❌ ERROR: Analysis failed with exception:")
        print(f"{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
