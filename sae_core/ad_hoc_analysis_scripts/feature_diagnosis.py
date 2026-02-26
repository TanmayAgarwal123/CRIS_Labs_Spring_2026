"""
Answer: Do features redundantly represent the same stopwords?
"""

import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from collections import defaultdict
from sae_core.full_analysis import ActivationDatabase

def analyze_feature_token_specificity(
    activation_db_path: str,
    output_dir: str = 'feature_specificity_analysis'
):
    """
    For EACH feature, determine:
    1. What % of its activations are stopwords?
    2. How diverse are the tokens it fires on?
    3. Is it redundant with other features?
    """
    
    print("="*80)
    print("FEATURE-LEVEL TOKEN SPECIFICITY ANALYSIS")
    print("="*80)
    
    # Load data
    print("\nLoading activation database...")
    db = ActivationDatabase.load(activation_db_path)
    
    # Define token categories
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'was', 'are', 'it', 'that', 'this',
        'be', 'been', 'being', 'have', 'has', 'had'
    }
    
    n_features = db.activation_matrix.shape[1]
    
    # Analyze each feature
    print(f"\nAnalyzing {n_features} features...")
    
    feature_stats = []
    
    for feature_idx in range(n_features):
        if feature_idx % 500 == 0:
            print(f"  Progress: {feature_idx}/{n_features}")
        
        # Get all activations
        activations = db.get_feature_activations(feature_idx, top_k=None)
        
        if len(activations) == 0:
            continue  # Dead feature
        
        # Count token types
        stopword_count = 0
        token_counts = defaultdict(int)
        
        for token_idx, act_val in activations:
            token_str = db.token_metadata[token_idx].token_str.strip().lower()
            token_counts[token_str] += 1
            
            if token_str in stopwords:
                stopword_count += 1
        
        # Compute statistics
        total_activations = len(activations)
        stopword_ratio = stopword_count / total_activations
        unique_tokens = len(token_counts)
        
        # Token diversity (entropy-based)
        token_probs = np.array(list(token_counts.values())) / total_activations
        entropy = -np.sum(token_probs * np.log(token_probs + 1e-10))
        max_entropy = np.log(unique_tokens) if unique_tokens > 0 else 1
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        # Most common token
        most_common_token = max(token_counts.items(), key=lambda x: x[1])
        most_common_ratio = most_common_token[1] / total_activations
        
        feature_stats.append({
            'feature_idx': feature_idx,
            'total_activations': total_activations,
            'stopword_ratio': stopword_ratio,
            'unique_tokens': unique_tokens,
            'diversity': normalized_entropy,
            'most_common_token': most_common_token[0],
            'most_common_ratio': most_common_ratio
        })
    
    # Convert to arrays for analysis
    stopword_ratios = np.array([f['stopword_ratio'] for f in feature_stats])
    diversities = np.array([f['diversity'] for f in feature_stats])
    most_common_ratios = np.array([f['most_common_ratio'] for f in feature_stats])
    
    # Classification
    stopword_heavy = stopword_ratios > 0.7  # >70% stopwords
    monosemantic = most_common_ratios > 0.8  # >80% one token
    diverse = diversities > 0.5  # Good diversity
    
    print("\n" + "="*80)
    print("RESULTS: Feature Categorization")
    print("="*80 + "\n")
    
    n_total = len(feature_stats)
    
    print(f"Total active features analyzed: {n_total}\n")
    
    print("STOPWORD FEATURES (>70% activations on stopwords):")
    print(f"  Count: {np.sum(stopword_heavy)} ({np.sum(stopword_heavy)/n_total*100:.1f}%)")
    
    print("\nMONOSEMANTIC FEATURES (>80% activations on single token):")
    print(f"  Count: {np.sum(monosemantic)} ({np.sum(monosemantic)/n_total*100:.1f}%)")
    
    print("\nDIVERSE FEATURES (high token diversity):")
    print(f"  Count: {np.sum(diverse)} ({np.sum(diverse)/n_total*100:.1f}%)")
    
    print("\nPOLYSEMANTIC FEATURES (diverse but NOT stopword-heavy):")
    polysemantic = diverse & ~stopword_heavy
    print(f"  Count: {np.sum(polysemantic)} ({np.sum(polysemantic)/n_total*100:.1f}%)")
    
    print("\n" + "="*80)
    print("KEY INSIGHT: Are all features learning stopwords?")
    print("="*80 + "\n")
    
    if np.sum(stopword_heavy) > n_total * 0.5:
        print("⚠️  CRITICAL PROBLEM: >50% of features primarily learn stopwords!")
        print("    → SAE has systemic redundancy issue")
        print("    → Recommendation: Retrain with higher sparsity penalty")
    elif np.sum(stopword_heavy) > n_total * 0.3:
        print("⚠️  MODERATE CONCERN: 30-50% of features focus on stopwords")
        print("    → Some redundancy, but not catastrophic")
        print("    → Consider mild hyperparameter adjustment")
    else:
        print("✅ GOOD: <30% of features are stopword-heavy")
        print("    → SAE has reasonable specialization")
        print("    → The high L0 for stopwords is expected (many contexts)")
    
    # Create visualizations
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Plot 1: Stopword ratio distribution
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    axes[0, 0].hist(stopword_ratios, bins=50, alpha=0.7, edgecolor='black')
    axes[0, 0].axvline(0.7, color='red', linestyle='--', label='70% threshold')
    axes[0, 0].set_xlabel('Stopword Ratio')
    axes[0, 0].set_ylabel('Number of Features')
    axes[0, 0].set_title('Distribution of Stopword Ratios Across Features')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Token diversity
    axes[0, 1].hist(diversities, bins=50, alpha=0.7, edgecolor='black', color='green')
    axes[0, 1].set_xlabel('Token Diversity (normalized entropy)')
    axes[0, 1].set_ylabel('Number of Features')
    axes[0, 1].set_title('Feature Token Diversity')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Scatter - diversity vs stopword ratio
    scatter = axes[1, 0].scatter(stopword_ratios, diversities, 
                                 alpha=0.3, s=10, c=most_common_ratios,
                                 cmap='viridis')
    axes[1, 0].set_xlabel('Stopword Ratio')
    axes[1, 0].set_ylabel('Token Diversity')
    axes[1, 0].set_title('Feature Characterization')
    axes[1, 0].axvline(0.7, color='red', linestyle='--', alpha=0.5)
    axes[1, 0].axhline(0.5, color='blue', linestyle='--', alpha=0.5)
    plt.colorbar(scatter, ax=axes[1, 0], label='Most Common Token Ratio')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Annotate regions
    axes[1, 0].text(0.85, 0.7, 'Stopword\nHeavy', ha='center', 
                   bbox=dict(boxstyle='round', facecolor='red', alpha=0.3))
    axes[1, 0].text(0.3, 0.7, 'Polysemantic\n(Good)', ha='center',
                   bbox=dict(boxstyle='round', facecolor='green', alpha=0.3))
    axes[1, 0].text(0.3, 0.2, 'Monosemantic\n(Good)', ha='center',
                   bbox=dict(boxstyle='round', facecolor='blue', alpha=0.3))
    
    # Plot 4: Feature category pie chart
    categories = [
        np.sum(monosemantic & ~stopword_heavy),  # Good monosemantic
        np.sum(polysemantic),  # Good polysemantic
        np.sum(stopword_heavy),  # Bad
        n_total - np.sum(monosemantic | polysemantic | stopword_heavy)  # Other
    ]
    labels = [
        f'Monosemantic\n({categories[0]}, {categories[0]/n_total*100:.1f}%)',
        f'Polysemantic\n({categories[1]}, {categories[1]/n_total*100:.1f}%)',
        f'Stopword-Heavy\n({categories[2]}, {categories[2]/n_total*100:.1f}%)',
        f'Other\n({categories[3]}, {categories[3]/n_total*100:.1f}%)'
    ]
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightgray']
    
    axes[1, 1].pie(categories, labels=labels, colors=colors, autopct='',
                   startangle=90)
    axes[1, 1].set_title('Feature Quality Distribution')
    
    plt.tight_layout()
    plt.savefig(output_path / 'feature_specificity_analysis.png', dpi=300)
    plt.close()
    
    print(f"\n✓ Saved visualization to {output_path / 'feature_specificity_analysis.png'}")
    
    # Save detailed report
    report_path = output_path / 'feature_specificity_report.txt'
    with open(report_path, 'w') as f:
        f.write("FEATURE-LEVEL TOKEN SPECIFICITY ANALYSIS\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Total features analyzed: {n_total}\n\n")
        
        f.write("FEATURE CATEGORIES:\n")
        f.write("-"*80 + "\n\n")
        f.write(f"Stopword-heavy (>70%):    {np.sum(stopword_heavy):4d} ({np.sum(stopword_heavy)/n_total*100:5.1f}%)\n")
        f.write(f"Monosemantic (>80% one):  {np.sum(monosemantic):4d} ({np.sum(monosemantic)/n_total*100:5.1f}%)\n")
        f.write(f"Diverse (high entropy):    {np.sum(diverse):4d} ({np.sum(diverse)/n_total*100:5.1f}%)\n")
        f.write(f"Good polysemantic:        {np.sum(polysemantic):4d} ({np.sum(polysemantic)/n_total*100:5.1f}%)\n\n")
        
        f.write("WORST OFFENDERS (most stopword-heavy features):\n")
        f.write("-"*80 + "\n\n")
        
        # Sort by stopword ratio
        sorted_stats = sorted(feature_stats, key=lambda x: x['stopword_ratio'], reverse=True)
        
        for i, feat in enumerate(sorted_stats[:20], 1):
            f.write(f"{i:2d}. Feature {feat['feature_idx']:4d}\n")
            f.write(f"    Stopword ratio: {feat['stopword_ratio']*100:5.1f}%\n")
            f.write(f"    Most common: '{feat['most_common_token']}' ({feat['most_common_ratio']*100:.1f}%)\n")
            f.write(f"    Unique tokens: {feat['unique_tokens']}\n")
            f.write(f"    Diversity: {feat['diversity']:.3f}\n\n")
        
        f.write("\nBEST FEATURES (diverse, not stopword-heavy):\n")
        f.write("-"*80 + "\n\n")
        
        # Sort by diversity, filter out stopword-heavy
        good_features = [f for f in feature_stats if f['stopword_ratio'] < 0.3]
        sorted_good = sorted(good_features, key=lambda x: x['diversity'], reverse=True)
        
        for i, feat in enumerate(sorted_good[:20], 1):
            f.write(f"{i:2d}. Feature {feat['feature_idx']:4d}\n")
            f.write(f"    Stopword ratio: {feat['stopword_ratio']*100:5.1f}%\n")
            f.write(f"    Diversity: {feat['diversity']:.3f}\n")
            f.write(f"    Unique tokens: {feat['unique_tokens']}\n")
            f.write(f"    Total activations: {feat['total_activations']}\n\n")
    
    print(f"✓ Saved report to {report_path}")
    
    return feature_stats, {
        'n_total': n_total,
        'n_stopword_heavy': np.sum(stopword_heavy),
        'n_monosemantic': np.sum(monosemantic),
        'n_diverse': np.sum(diverse),
        'n_polysemantic_good': np.sum(polysemantic)
    }


if __name__ == "__main__":
    ACTIVATION_DB_PATH = 'deprecated_analysis/analysis/activation_database/activation_db_20251104_210231.pkl'
    OUTPUT_DIR = 'feature_specificity_analysis'
    
    feature_stats, summary = analyze_feature_token_specificity(
        activation_db_path=ACTIVATION_DB_PATH,
        output_dir=OUTPUT_DIR
    )
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)