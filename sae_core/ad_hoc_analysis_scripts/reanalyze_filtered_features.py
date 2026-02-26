"""
Re-analyze SAE features while filtering out special tokens
Uses existing activation database - NO rerun needed!
"""

import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sae_core.full_analysis import SAEAnalyzer, ActivationDatabase
from transformer_lens import HookedTransformer


def filter_special_token_features(
    activation_db: ActivationDatabase,
    model: HookedTransformer,
    special_tokens: list = None,
    max_special_token_ratio: float = 0.3
):
    """
    Find features that don't primarily activate on special tokens
    
    Args:
        activation_db: Your activation database
        model: The language model (for token vocab)
        special_tokens: List of special token strings to filter
        max_special_token_ratio: Max fraction of activations that can be special tokens
    
    Returns:
        List of (feature_idx, score) for interesting features
    """
    
    if special_tokens is None:
        # Common special tokens for Qwen models
        special_tokens = [
            '<|im_end|>',
            '<|endoftext|>',
            '<|im_start|>',
            '<pad>',
            '<eos>',
            '<bos>',
            '</s>',
            '<s>',
        ]
    
    print(f"Filtering features that activate primarily on: {special_tokens}")
    
    n_features = activation_db.activation_matrix.shape[1]
    feature_scores = []
    
    for feature_idx in range(n_features):
        # Get all activations for this feature
        activations = activation_db.get_feature_activations(feature_idx)
        
        if len(activations) == 0:
            continue  # Dead feature
        
        # Count how many are on special tokens
        special_count = 0
        total_count = len(activations)
        
        for token_idx, _ in activations:
            token_str = activation_db.token_metadata[token_idx].token_str
            
            # Check if it's a special token
            if any(special in token_str for special in special_tokens):
                special_count += 1
        
        special_ratio = special_count / total_count
        
        # Only keep features where special tokens are minority
        if special_ratio < max_special_token_ratio:
            # Score by frequency and diversity
            activation_values = [act for _, act in activations]
            mean_activation = np.mean(activation_values)
            activation_variance = np.var(activation_values)
            
            # Combined score: frequency * mean_activation * (1 - special_ratio)
            score = total_count * mean_activation * (1 - special_ratio) * (1 + activation_variance)
            
            feature_scores.append((feature_idx, score, special_ratio, total_count))
    
    # Sort by score
    feature_scores.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nFound {len(feature_scores)} features with <{max_special_token_ratio*100:.0f}% special tokens")
    print(f"(Filtered out {n_features - len(feature_scores)} features)")
    
    return feature_scores


def analyze_filtered_features(
    activation_db_path: str,
    model_name: str = "qwen3-0.6b",
    sae_path: str = None,
    layer: int = 12,
    hook_name: str = 'hook_resid_post',
    max_special_token_ratio: float = 0.3,
    top_k: int = 20,
    output_dir: str = 'analysis_filtered'
):
    """
    Re-analyze features with special token filtering
    """
    
    print("="*80)
    print("FILTERED FEATURE ANALYSIS")
    print("="*80)
    
    # Load existing activation database
    print(f"\nLoading activation database from: {activation_db_path}")
    activation_db = ActivationDatabase.load(activation_db_path)
    
    # Load model
    print(f"\nLoading model: {model_name}")
    model = HookedTransformer.from_pretrained(model_name)
    
    # Filter features
    print(f"\nFiltering features (max special token ratio: {max_special_token_ratio})...")
    feature_scores = filter_special_token_features(
        activation_db,
        model,
        max_special_token_ratio=max_special_token_ratio
    )
    
    if len(feature_scores) == 0:
        print("ERROR: No features passed the filter!")
        return
    
    # Print top features
    print(f"\nTop {min(top_k, len(feature_scores))} features (by filtered score):")
    print("-" * 80)
    for i, (feat_idx, score, special_ratio, count) in enumerate(feature_scores[:top_k], 1):
        print(f"{i:2d}. Feature {feat_idx:4d} | Score: {score:.2e} | "
              f"Count: {count:6d} | Special: {special_ratio*100:.1f}%")
        
        # Show example activations
        activations = activation_db.get_feature_activations(feat_idx, top_k=3)
        for token_idx, act_val in activations:
            token_str = activation_db.token_metadata[token_idx].token_str
            context = activation_db.get_token_context(token_idx, model, context_size=5)
            print(f"      '{token_str}' ({act_val:.3f}) in: ...{context['context'][:60]}...")
        print()
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    dashboards_path = output_path / 'dashboards'
    dashboards_path.mkdir(exist_ok=True)
    
    # Re-initialize analyzer with the database
    print(f"\nInitializing analyzer...")
    from sae_core.data_processing.textbook_process import load_processed_data
    texts = load_processed_data('sae_core/data/processed_data/processed_physics_10_ch.json')
    
    analyzer = SAEAnalyzer(
        model=model,
        sae_path=sae_path,
        layer=layer,
        hook_name=hook_name,
        dataset=texts
    )
    analyzer.activation_db = activation_db
    
    # Load pre-computed matrices if available
    base_analysis_dir = Path(activation_db_path).parent.parent
    
    # Try to load similarity matrix
    similarity_files = list(base_analysis_dir.glob('matrices/feature_similarity_*.npy'))
    if similarity_files:
        print(f"Loading similarity matrix: {similarity_files[0]}")
        analyzer.feature_similarity = np.load(similarity_files[0])
    
    # Try to load co-occurrence matrix  
    cooccurrence_files = list(base_analysis_dir.glob('matrices/feature_cooccurrence_*.npy'))
    if cooccurrence_files:
        print(f"Loading co-occurrence matrix: {cooccurrence_files[0]}")
        analyzer.feature_cooccurrence = np.load(cooccurrence_files[0])
    
    # Create dashboards for top filtered features
    print(f"\nCreating dashboards for top {min(10, len(feature_scores))} filtered features...")
    
    for rank, (feature_idx, score, special_ratio, count) in enumerate(feature_scores[:10], 1):
        print(f"  Creating dashboard for feature {feature_idx} (rank {rank})...")
        
        try:
            analyzer.create_feature_dashboard(
                feature_idx=feature_idx,
                save_path=str(dashboards_path / f'feature_{feature_idx}_dashboard.png')
            )
            plt.close('all')
            
            analyzer.plot_activation_distribution(
                feature_idx=feature_idx,
                save_path=str(dashboards_path / f'feature_{feature_idx}_distribution.png')
            )
            plt.close('all')
        except Exception as e:
            print(f"  WARNING: Failed to create dashboard: {e}")
    
    # Save filtered feature list
    filtered_features_path = output_path / 'filtered_features.txt'
    with open(filtered_features_path, 'w') as f:
        f.write("FILTERED FEATURE ANALYSIS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Max special token ratio: {max_special_token_ratio}\n")
        f.write(f"Features passing filter: {len(feature_scores)}\n\n")
        f.write("Top Features:\n")
        f.write("-" * 80 + "\n")
        
        for i, (feat_idx, score, special_ratio, count) in enumerate(feature_scores[:50], 1):
            f.write(f"{i:3d}. Feature {feat_idx:4d} | Score: {score:.2e} | "
                   f"Count: {count:6d} | Special: {special_ratio*100:.1f}%\n")
    
    print(f"\n✓ Saved filtered feature list to: {filtered_features_path}")
    print(f"✓ Saved dashboards to: {dashboards_path}")
    
    print("\n" + "="*80)
    print("FILTERED ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nOutputs saved to: {output_path}")
    print(f"Check {dashboards_path} for interesting feature visualizations")
    
    return feature_scores


if __name__ == "__main__":
    # Configuration - UPDATE THESE PATHS
    ACTIVATION_DB_PATH = 'analysis/activation_database/activation_db_20251104_210231.pkl'
    SAE_PATH = 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity60.mse0.001.kl0.01.physics10.exp8'
    MODEL_NAME = "qwen3-0.6b"
    LAYER = 12
    HOOK_NAME = 'hook_resid_post'

    print("Running filtered analysis")
    
    # Run filtered analysis
    feature_scores = analyze_filtered_features(
        activation_db_path=ACTIVATION_DB_PATH,
        model_name=MODEL_NAME,
        sae_path=SAE_PATH,
        layer=LAYER,
        hook_name=HOOK_NAME,
        max_special_token_ratio=0.3,  # Allow max 30% special tokens
        top_k=20,
        output_dir='analysis_filtered'
    )
    
    print("\n✓ Done! Check analysis_filtered/ for results")