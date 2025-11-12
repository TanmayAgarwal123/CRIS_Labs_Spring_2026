"""
Check if stopwords are activating disproportionately many features
"""

import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict

import sys
sys.path.append('/Users/deancasey/Documents/Columbia/CRIS Lab/SAELens')

from sae_core.full_analysis import ActivationDatabase


def analyze_token_polysemanticity(
    activation_db_path: str,
    output_dir: str = 'polysemanticity_analysis'
):
    """
    Analyze how many features activate for different types of tokens
    """
    
    print("="*80)
    print("STOPWORD POLYSEMANTICITY ANALYSIS")
    print("="*80)
    
    # Load data
    print("\nLoading activation database...")
    db = ActivationDatabase.load(activation_db_path)
    
    # Define token categories
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'was', 'are', 'it', 'that', 'this'
    }
    
    physics_terms = {
        'force', 'mass', 'velocity', 'acceleration', 'momentum', 'energy',
        'kinetic', 'potential', 'friction', 'gravity', 'newton', 'vector',
        'magnitude', 'displacement', 'angular', 'torque', 'work', 'power'
    }
    
    # Collect L0 (number of active features) for each token type
    stopword_l0 = []
    physics_l0 = []
    other_l0 = []
    
    # Sample tokens (don't need all 891K - sample 10K for speed)
    print("\nAnalyzing L0 (active features) per token...")
    sample_size = min(10000, len(db.token_metadata))
    sample_indices = np.random.choice(len(db.token_metadata), sample_size, replace=False)
    
    for token_idx in sample_indices:
        token_str = db.token_metadata[token_idx].token_str.strip().lower()
        
        # Get active features for this token
        active_features = db.get_token_activations(token_idx, threshold=0.0)
        l0 = len(active_features)
        
        # Categorize
        if token_str in stopwords:
            stopword_l0.append(l0)
        elif token_str in physics_terms:
            physics_l0.append(l0)
        else:
            other_l0.append(l0)
    
    # Compute statistics
    print(f"\n{'='*80}")
    print("RESULTS: L0 (Active Features) by Token Type")
    print(f"{'='*80}\n")
    
    if stopword_l0:
        print(f"STOPWORDS (n={len(stopword_l0)}):")
        print(f"  Mean L0: {np.mean(stopword_l0):.2f} ± {np.std(stopword_l0):.2f}")
        print(f"  Median L0: {np.median(stopword_l0):.1f}")
        print(f"  Range: [{np.min(stopword_l0)}, {np.max(stopword_l0)}]")
        print()
    
    if physics_l0:
        print(f"PHYSICS TERMS (n={len(physics_l0)}):")
        print(f"  Mean L0: {np.mean(physics_l0):.2f} ± {np.std(physics_l0):.2f}")
        print(f"  Median L0: {np.median(physics_l0):.1f}")
        print(f"  Range: [{np.min(physics_l0)}, {np.max(physics_l0)}]")
        print()
    
    if other_l0:
        print(f"OTHER TOKENS (n={len(other_l0)}):")
        print(f"  Mean L0: {np.mean(other_l0):.2f} ± {np.std(other_l0):.2f}")
        print(f"  Median L0: {np.median(other_l0):.1f}")
        print(f"  Range: [{np.min(other_l0)}, {np.max(other_l0)}]")
        print()
    
    # INTERPRETATION
    print(f"{'='*80}")
    print("INTERPRETATION:")
    print(f"{'='*80}\n")
    
    if stopword_l0 and other_l0:
        ratio = np.mean(stopword_l0) / np.mean(other_l0)
        
        if ratio > 1.5:
            print("⚠️  WARNING: Stopwords activate 50%+ MORE features than average!")
            print("    This suggests the SAE is densely encoding common words.")
            print("    → PROBLEM: Features are not sparse/interpretable")
        elif ratio > 1.2:
            print("⚠️  CAUTION: Stopwords activate slightly more features than average.")
            print("    This might be expected (stopwords appear in many contexts)")
            print("    → Check if this matches your sparsity target")
        else:
            print("✅ GOOD: Stopwords don't activate disproportionately many features!")
            print("    This suggests sparse, meaningful feature learning.")
            print("    → SAE is working as intended")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Box plots
    data_to_plot = []
    labels = []
    
    if stopword_l0:
        data_to_plot.append(stopword_l0)
        labels.append('Stopwords')
    if physics_l0:
        data_to_plot.append(physics_l0)
        labels.append('Physics Terms')
    if other_l0:
        data_to_plot.append(other_l0)
        labels.append('Other Tokens')
    
    axes[0].boxplot(data_to_plot, labels=labels)
    axes[0].set_ylabel('L0 (Active Features)', fontsize=12)
    axes[0].set_title('Feature Activation Count by Token Type', fontsize=14)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Histograms
    if stopword_l0:
        axes[1].hist(stopword_l0, bins=30, alpha=0.5, label='Stopwords', edgecolor='black')
    if physics_l0:
        axes[1].hist(physics_l0, bins=30, alpha=0.5, label='Physics Terms', edgecolor='black')
    if other_l0:
        axes[1].hist(other_l0, bins=30, alpha=0.5, label='Other', edgecolor='black')
    
    axes[1].set_xlabel('L0 (Active Features)', fontsize=12)
    axes[1].set_ylabel('Frequency', fontsize=12)
    axes[1].set_title('Distribution of Active Features', fontsize=14)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_path / 'token_polysemanticity.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n✓ Saved visualization to {output_path / 'token_polysemanticity.png'}")
    
    # Detailed breakdown: which features activate on stopwords?
    print("\n" + "="*80)
    print("DETAILED ANALYSIS: Which features activate on stopwords?")
    print("="*80 + "\n")
    
    # Pick the most common stopwords and analyze them
    common_stopwords = ['the', 'a', 'of', 'and', 'in']
    
    for stopword in common_stopwords:
        # Find all occurrences of this stopword
        stopword_token_indices = [
            i for i, meta in enumerate(db.token_metadata)
            if meta.token_str.strip().lower() == stopword
        ]
        
        if not stopword_token_indices:
            continue
        
        # Sample up to 100 occurrences
        sample_stopword_indices = stopword_token_indices[:100]
        
        # Get all features that activate
        feature_activation_counts = defaultdict(int)
        
        for token_idx in sample_stopword_indices:
            active_features = db.get_token_activations(token_idx, threshold=0.0)
            for feat_idx, _ in active_features:
                feature_activation_counts[feat_idx] += 1
        
        # Sort by frequency
        sorted_features = sorted(feature_activation_counts.items(), key=lambda x: x[1], reverse=True)
        
        print(f"Token: '{stopword}' (analyzed {len(sample_stopword_indices)} occurrences)")
        print(f"  Total unique features activated: {len(feature_activation_counts)}")
        print(f"  Top 5 most frequently activated features:")
        for feat_idx, count in sorted_features[:5]:
            pct = count / len(sample_stopword_indices) * 100
            print(f"    Feature {feat_idx}: {count}/{len(sample_stopword_indices)} ({pct:.1f}%)")
        print()
    
    # Save detailed report
    report_path = output_path / 'polysemanticity_report.txt'
    with open(report_path, 'w') as f:
        f.write("STOPWORD POLYSEMANTICITY ANALYSIS\n")
        f.write("="*80 + "\n\n")
        
        f.write("SUMMARY STATISTICS:\n")
        f.write("-"*80 + "\n\n")
        
        if stopword_l0:
            f.write(f"Stopwords: {np.mean(stopword_l0):.2f} ± {np.std(stopword_l0):.2f} features\n")
        if physics_l0:
            f.write(f"Physics terms: {np.mean(physics_l0):.2f} ± {np.std(physics_l0):.2f} features\n")
        if other_l0:
            f.write(f"Other tokens: {np.mean(other_l0):.2f} ± {np.std(other_l0):.2f} features\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("INTERPRETATION:\n")
        f.write("="*80 + "\n\n")
        
        if stopword_l0 and other_l0:
            ratio = np.mean(stopword_l0) / np.mean(other_l0)
            f.write(f"Stopword/Other ratio: {ratio:.2f}\n\n")
            
            if ratio > 1.5:
                f.write("WARNING: Stopwords are activating many more features than expected.\n")
                f.write("This suggests the SAE may not be learning sparse, interpretable features.\n")
            else:
                f.write("GOOD: Stopwords don't show excessive polysemanticity.\n")
                f.write("The SAE appears to be learning sparse features appropriately.\n")
    
    print(f"✓ Saved detailed report to {report_path}")
    
    return {
        'stopword_l0': stopword_l0,
        'physics_l0': physics_l0,
        'other_l0': other_l0
    }


if __name__ == "__main__":
    ACTIVATION_DB_PATH = 'analysis/activation_database/activation_db_20251104_210231.pkl'
    OUTPUT_DIR = 'polysemanticity_analysis'
    
    results = analyze_token_polysemanticity(
        activation_db_path=ACTIVATION_DB_PATH,
        output_dir=OUTPUT_DIR
    )
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print(f"\nCheck {OUTPUT_DIR}/ for results")