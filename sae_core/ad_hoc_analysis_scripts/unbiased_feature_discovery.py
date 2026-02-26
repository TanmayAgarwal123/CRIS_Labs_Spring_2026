"""
Unbiased feature discovery - remove manual physics keyword boosting
Tests if physics features emerge organically without biasing the scoring
"""

import numpy as np
from pathlib import Path
import re

from sae_core.full_analysis import ActivationDatabase
from transformer_lens import HookedTransformer


def unbiased_feature_scoring(
    activation_db_path: str,
    model_name: str = "qwen3-0.6b",
    output_dir: str = 'unbiased_discovery'
):
    """
    Discover interesting features WITHOUT manually boosting physics terms
    
    Scoring based only on:
    1. Token length (longer = more specific)
    2. Frequency (mid-range is good)
    3. Activation strength variance
    4. NOT stopwords/formatting
    
    NO manual physics keyword boosting!
    """
    
    print("="*80)
    print("UNBIASED FEATURE DISCOVERY")
    print("="*80)
    print("\nRemoving manual physics keyword bias...")
    print("Scoring based ONLY on statistical properties\n")
    
    # Load data
    print("Loading activation database...")
    db = ActivationDatabase.load(activation_db_path)
    
    print("Loading model...")
    model = HookedTransformer.from_pretrained(model_name)
    
    # Stopwords to filter
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
        'that', 'these', 'those', 'it', 'its', 'he', 'she', 'they', 'we'
    }
    
    # Formatting patterns to filter
    formatting_patterns = [
        r'^\s*$',  # Only whitespace
        r'^[^\w\s]+$',  # Only punctuation
        r'^\d+$',  # Only numbers
        r'colspan|rowspan|td|tr|class|style|div|span',  # HTML
        r'<\|.*?\|>',  # Special tokens
        r'^(Figure|FIG|URE|IVES|ARNING|credit)$',  # Textbook formatting
    ]
    
    print("Scanning features with unbiased scoring...")
    feature_scores = []
    
    for feature_idx in range(db.activation_matrix.shape[1]):
        if feature_idx % 1000 == 0:
            print(f"  Progress: {feature_idx}/{db.activation_matrix.shape[1]}")
        
        # Get activations
        activations = db.get_feature_activations(feature_idx, top_k=100)
        
        if len(activations) == 0:
            continue
        
        freq = db.feature_metadata['activation_counts'][feature_idx]
        
        # Frequency filter: not too rare, not too common
        if freq < 100 or freq > 20000:
            continue
        
        # Analyze tokens
        token_strs = []
        activation_values = []
        stopword_count = 0
        formatting_count = 0
        
        for token_idx, act_val in activations:
            token_str = db.token_metadata[token_idx].token_str
            token_strs.append(token_str)
            activation_values.append(act_val)
            
            token_clean = token_str.strip().lower()
            
            # Check stopwords
            if token_clean in stopwords:
                stopword_count += 1
            
            # Check formatting
            is_formatting = any(re.search(pattern, token_str, re.IGNORECASE) 
                              for pattern in formatting_patterns)
            if is_formatting:
                formatting_count += 1
        
        stopword_ratio = stopword_count / len(activations)
        formatting_ratio = formatting_count / len(activations)
        
        # Skip if mostly stopwords or formatting
        if stopword_ratio > 0.3 or formatting_ratio > 0.3:
            continue
        
        # UNBIASED SCORING (no physics keyword boost!)
        
        # 1. Token length (longer = more specific)
        avg_length = np.mean([len(t.strip()) for t in token_strs])
        length_score = min(avg_length / 15.0, 1.0)  # Normalize
        
        # 2. Activation statistics
        mean_activation = np.mean(activation_values)
        max_activation = np.max(activation_values)
        activation_variance = np.var(activation_values)
        
        # 3. Frequency penalty (prefer mid-range)
        frequency_penalty = 1.0 / (1.0 + np.log(freq / 1000.0)) if freq > 1000 else 1.0
        
        # COMBINED SCORE (purely statistical, no domain bias)
        score = (
            length_score * 50 +           # Token specificity
            mean_activation * 10 +         # Activation strength
            max_activation * 5 +           # Peak activation
            activation_variance * 2        # Activation diversity
        ) * frequency_penalty * (1 - stopword_ratio) * (1 - formatting_ratio)
        
        feature_scores.append({
            'feature_idx': feature_idx,
            'score': score,
            'frequency': freq,
            'mean_activation': mean_activation,
            'max_activation': max_activation,
            'avg_length': avg_length,
            'stopword_ratio': stopword_ratio,
            'top_tokens': token_strs[:10]
        })
    
    # Sort by score
    feature_scores.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\n✓ Found {len(feature_scores)} features passing filters")
    
    # Analyze: what emerged organically?
    print("\n" + "="*80)
    print("TOP 30 FEATURES (Unbiased Discovery)")
    print("="*80 + "\n")
    
    # Manual physics keywords (for comparison only)
    physics_keywords = {
        'force', 'mass', 'velocity', 'acceleration', 'momentum', 'energy',
        'kinetic', 'potential', 'friction', 'gravity', 'newton', 'vector',
        'magnitude', 'displacement', 'angular', 'torque', 'work', 'power',
        'quantum', 'wave', 'particle', 'field', 'charge'
    }
    
    physics_count = 0
    
    for i, feat_info in enumerate(feature_scores[:30], 1):
        # Check if any top tokens are physics terms
        is_physics = any(
            any(keyword in token.lower() for keyword in physics_keywords)
            for token in feat_info['top_tokens']
        )
        
        if is_physics:
            physics_count += 1
            marker = "🔬"
        else:
            marker = "  "
        
        print(f"{marker} {i:2d}. Feature {feat_info['feature_idx']:4d} | "
              f"Score: {feat_info['score']:.2e} | "
              f"Freq: {feat_info['frequency']:6d}")
        print(f"      Top tokens: {', '.join(feat_info['top_tokens'][:5])}")
        
        # Show example
        activations = db.get_feature_activations(feat_info['feature_idx'], top_k=1)
        if activations:
            token_idx, act_val = activations[0]
            context = db.get_token_context(token_idx, model, context_size=8)
            print(f"      Example: ...{context['context'][:70]}...")
        print()
    
    # Summary
    print("="*80)
    print("UNBIASED DISCOVERY RESULTS:")
    print("="*80 + "\n")
    
    physics_pct = physics_count / 30 * 100
    print(f"Physics-related features in top 30: {physics_count}/30 ({physics_pct:.1f}%)")
    print()
    
    if physics_pct > 50:
        print("✅ VALIDATION PASSED!")
        print("   Physics concepts emerged organically without manual boosting.")
        print("   This suggests the SAE genuinely learned domain-specific features.")
    elif physics_pct > 30:
        print("⚠️  PARTIAL VALIDATION")
        print("   Some physics concepts emerged, but also many non-physics terms.")
        print("   The scoring may need refinement.")
    else:
        print("❌ CONCERN RAISED")
        print("   Few physics concepts emerged without manual boosting.")
        print("   The original bias may have been artificially finding physics terms.")
    
    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    report_path = output_path / 'unbiased_discovery_report.txt'
    with open(report_path, 'w') as f:
        f.write("UNBIASED FEATURE DISCOVERY REPORT\n")
        f.write("="*80 + "\n\n")
        f.write("Scoring method: Statistical properties ONLY (no physics keyword boost)\n\n")
        f.write("Top 50 Features:\n")
        f.write("-"*80 + "\n\n")
        
        for i, feat_info in enumerate(feature_scores[:50], 1):
            is_physics = any(
                any(keyword in token.lower() for keyword in physics_keywords)
                for token in feat_info['top_tokens']
            )
            
            f.write(f"{i:3d}. Feature {feat_info['feature_idx']:4d} ")
            f.write(f"{'[PHYSICS]' if is_physics else '[OTHER]  '}\n")
            f.write(f"     Score: {feat_info['score']:.2e} | ")
            f.write(f"Freq: {feat_info['frequency']:6d} | ")
            f.write(f"Mean Act: {feat_info['mean_activation']:.3f}\n")
            f.write(f"     Tokens: {', '.join(feat_info['top_tokens'][:5])}\n\n")
    
    print(f"\n✓ Saved detailed report to {report_path}")
    
    return feature_scores


if __name__ == "__main__":
    ACTIVATION_DB_PATH = 'analysis/activation_database/activation_db_20251104_210231.pkl'
    MODEL_NAME = "qwen3-0.6b"
    OUTPUT_DIR = 'unbiased_discovery'
    
    features = unbiased_feature_scoring(
        activation_db_path=ACTIVATION_DB_PATH,
        model_name=MODEL_NAME,
        output_dir=OUTPUT_DIR
    )
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print(f"\nCheck {OUTPUT_DIR}/ for results")