import os
from pathlib import Path
import json
import numpy as np
from datetime import datetime

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for remote servers
import matplotlib.pyplot as plt
import seaborn as sns

from sae_core.full_analysis import SAEAnalyzer
from sae_core.pretrained import load_pretrained
from sae_core.data_processing.textbook_process import load_processed_data
from transformer_lens import HookedTransformer

def create_analysis_directories(base_path: str = 'analysis'):
    """Create organized directory structure for analysis outputs"""
    base = Path(base_path)
    dirs = {
        'base': base,
        'activation_db': base / 'activation_database',
        'matrices': base / 'matrices',
        'plots': base / 'plots',
        'results': base / 'results',
        'dashboards': base / 'plots' / 'dashboards'
    }
    
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return dirs


def run_comprehensive_analysis(
    model_name: str = "qwen3-0.6b",
    sae_path: str = None,
    layer: int = 12,
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
    
    # ========================================
    # 1. LOAD MODEL, SAE, AND DATA
    # ========================================
    print("\n[1/9] Loading model, SAE, and data...")
    
    model = HookedTransformer.from_pretrained(model_name)
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
    
    # ========================================
    # 2. INITIALIZE ANALYZER
    # ========================================
    print("\n[2/9] Initializing SAE Analyzer...")
    
    analyzer = SAEAnalyzer(
        model=model,
        sae_path=sae_path,
        layer=layer,
        hook_name=hook_name,
        dataset=texts
    )
    print("✓ Analyzer initialized")
    
    # ========================================
    # 3. COLLECT ACTIVATIONS
    # ========================================
    print("\n[3/9] Collecting activations across corpus...")
    print("This may take a while depending on corpus size...")
    
    activation_db_path = dirs['activation_db'] / f'activation_db_{timestamp}.pkl'
    analyzer.collect_all_activations(
        batch_size=batch_size,
        save_path=str(activation_db_path)
    )
    print(f"✓ Saved activation database to: {activation_db_path}")
    
    # ========================================
    # 4. COMPUTE FEATURE SIMILARITY
    # ========================================
    print("\n[4/9] Computing feature similarity matrix...")
    
    similarity_path = dirs['matrices'] / f'feature_similarity_{timestamp}.npy'
    analyzer.compute_feature_similarity(
        similarity_metric='cosine',
        save_path=str(similarity_path)
    )
    print(f"✓ Saved similarity matrix to: {similarity_path}")
    
    # ========================================
    # 5. COMPUTE FEATURE CO-OCCURRENCE
    # ========================================
    print("\n[5/9] Computing feature co-occurrence matrix...")
    print("This may take a while for large feature sets...")
    
    cooccurrence_path = dirs['matrices'] / f'feature_cooccurrence_{timestamp}.npy'
    analyzer.compute_feature_cooccurrence(
        method='correlation',
        save_path=str(cooccurrence_path),
        chunk_size=1000  # Adjust based on available memory
    )
    print(f"✓ Saved co-occurrence matrix to: {cooccurrence_path}")
    
    # ========================================
    # 6. RUN FULL METRICS ANALYSIS
    # ========================================
    print("\n[6/9] Running full metrics analysis...")
    
    results_path = dirs['results'] / f'analysis_results_{timestamp}.json'
    results = analyzer.run_full_analysis(
        batch_size=batch_size,
        save_path=str(results_path)
    )
    print(f"✓ Saved results to: {results_path}")
    
    # ========================================
    # 7. CREATE OVERVIEW VISUALIZATIONS
    # ========================================
    print("\n[7/9] Creating overview visualizations...")
    
    # Sparsity distribution
    analyzer.plot_sparsity_distribution(
        results['sparsity'],
        results['feature_freq'],
        save_path=str(dirs['plots'] / 'sparsity_overview.png')
    )
    plt.close('all')  # Close all figures
    print("✓ Created sparsity distribution plot")
    
    # Reconstruction quality
    analyzer.plot_reconstruction_quality(
        results['reconstruction'],
        save_path=str(dirs['plots'] / 'reconstruction_quality.png')
    )
    plt.close('all')
    print("✓ Created reconstruction quality plot")
    
    # Feature similarity heatmap
    analyzer.plot_feature_similarity_heatmap(
        top_k=50,
        save_path=str(dirs['plots'] / 'similarity_heatmap.png')
    )
    plt.close('all')
    print("✓ Created feature similarity heatmap")
    
    # Feature co-occurrence heatmap
    analyzer.plot_cooccurrence_heatmap(
        top_k=50,
        save_path=str(dirs['plots'] / 'cooccurrence_heatmap.png')
    )
    plt.close('all')
    print("✓ Created feature co-occurrence heatmap")
    
    # ========================================
    # 8. ANALYZE TOP FEATURES
    # ========================================
    print("\n[8/9] Analyzing top features individually...")
    
    # Get top 10 most active features
    feature_counts = np.array(results['feature_freq'])
    top_feature_indices = np.argsort(feature_counts)[-10:][::-1]
    
    feature_analysis_dir = dirs['dashboards']
    
    for rank, feature_idx in enumerate(top_feature_indices, 1):
        print(f"  Analyzing feature {feature_idx} (rank {rank})...")
        
        try:
            # Create comprehensive dashboard
            analyzer.create_feature_dashboard(
                feature_idx=feature_idx,
                save_path=str(feature_analysis_dir / f'feature_{feature_idx}_dashboard.png')
            )
            plt.close('all')
            
            # Individual activation distribution
            analyzer.plot_activation_distribution(
                feature_idx=feature_idx,
                save_path=str(feature_analysis_dir / f'feature_{feature_idx}_distribution.png')
            )
            plt.close('all')
        except Exception as e:
            print(f"  WARNING: Failed to analyze feature {feature_idx}: {e}")
            continue
    
    print(f"✓ Created {len(top_feature_indices)} feature dashboards")
    
    # ========================================
    # 9. GENERATE SUMMARY REPORT
    # ========================================
    print("\n[9/9] Generating summary report...")
    
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
            'results': str(results_path.relative_to(dirs['base']))
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

## Directory Structure
```
analysis/
├── SUMMARY_{timestamp}.json          # This summary
├── config_{timestamp}.json           # Run configuration
├── activation_database/              # Activation database
├── matrices/                         # Similarity & co-occurrence matrices
├── results/                          # Detailed analysis results
└── plots/                            # All visualizations
    ├── training_history.png
    ├── sparsity_overview.png
    ├── reconstruction_quality.png
    ├── similarity_heatmap.png
    ├── cooccurrence_heatmap.png
    └── dashboards/                   # Per-feature dashboards
        ├── feature_*_dashboard.png
        └── feature_*_distribution.png
```

## Top 10 Most Active Features
{', '.join(map(str, top_feature_indices.tolist()))}

See dashboards/ folder for detailed analysis of each feature.
"""
    
    readme_path = dirs['base'] / f'README_{timestamp}.md'
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✓ Saved summary to: {summary_path}")
    print(f"✓ Saved README to: {readme_path}")
    
    # ========================================
    # COMPLETION
    # ========================================
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


# ========================================
# MAIN EXECUTION
# ========================================
if __name__ == "__main__":
    
    # Configuration
    MODEL_NAME = "qwen3-0.6b"
    SAE_PATH = 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity100.mse0.001.kl0.01.physics.exp4'
    # SAE_PATH = 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity60.mse0.001.kl0.01.physics10.exp8'
    LAYER = 12
    HOOK_NAME = 'hook_resid_post'
    DATA_PATH = 'sae_core/data/processed_data/processed_physics_all.json'
    # DATA_PATH = 'sae_core/data/processed_data/processed_physics_10_ch.json'
    BATCH_SIZE = 16
    ANALYSIS_DIR = 'analysis_reborn_final'
    
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