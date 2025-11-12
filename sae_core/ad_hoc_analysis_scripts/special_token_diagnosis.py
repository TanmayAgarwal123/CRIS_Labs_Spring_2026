"""
Special Token Analysis - The REAL polysemanticity check
Special tokens (BOS, EOS, padding, etc.) are often the worst offenders
"""

import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from sae_core.full_analysis import ActivationDatabase
import re


class SpecialTokenAnalyzer:
    """Comprehensive special token analysis for SAEs"""
    
    def __init__(self, activation_db: ActivationDatabase):
        self.db = activation_db
        
        # Comprehensive special token patterns
        self.special_token_patterns = {
            'bos_eos': [
                r'<\|im_start\|>',
                r'<\|im_end\|>',
                r'<\|endoftext\|>',
                r'<s>',
                r'</s>',
                r'<eos>',
                r'<bos>',
                r'<\|begin_of_text\|>',
                r'<\|end_of_text\|>',
            ],
            'padding': [
                r'<pad>',
                r'<\|pad\|>',
                r'\[PAD\]',
            ],
            'whitespace': [
                r'^\s+$',  # Only whitespace
                r'^\\n+$',  # Only newlines
                r'^\\t+$',  # Only tabs
            ],
            'punctuation_only': [
                r'^[.,;:!?\-\'"(){}[\]]+$',  # Only punctuation
            ],
            'html_xml': [
                r'</?[a-z]+[^>]*>',  # HTML/XML tags
                r'&[a-z]+;',  # HTML entities
            ],
            'special_markers': [
                r'^\[.*\]$',  # [MASK], [UNK], etc.
                r'^<.*>$',  # <special>
                r'^\{.*\}$',  # {special}
            ]
        }
    
    def classify_token(self, token_str: str) -> str:
        """Classify a token as special or normal"""
        token = token_str.strip()
        
        # Check each category
        for category, patterns in self.special_token_patterns.items():
            for pattern in patterns:
                if re.search(pattern, token, re.IGNORECASE):
                    return category
        
        # Additional heuristics
        if len(token) == 0:
            return 'empty'
        
        if token.startswith('▁') or token.startswith('Ġ'):
            return 'normal'  # Tokenizer prefix, but the token itself is normal
        
        return 'normal'
    
    def analyze_token_distribution(self, sample_size: int = 10000):
        """Analyze distribution of token types in corpus"""
        
        print("Analyzing token type distribution in corpus...")
        
        n_tokens = len(self.db.token_metadata)
        sample_size = min(sample_size, n_tokens)
        sample_indices = np.random.choice(n_tokens, sample_size, replace=False)
        
        category_counts = Counter()
        token_examples = defaultdict(list)
        
        for idx in sample_indices:
            token_str = self.db.token_metadata[idx].token_str
            category = self.classify_token(token_str)
            category_counts[category] += 1
            
            if len(token_examples[category]) < 10:
                token_examples[category].append(token_str)
        
        print("\nToken Distribution in Corpus:")
        print("-" * 80)
        for category, count in category_counts.most_common():
            pct = count / sample_size * 100
            examples = token_examples[category][:5]
            print(f"{category:20s}: {count:6d} ({pct:5.2f}%) | Examples: {examples}")
        
        return category_counts, token_examples
    
    def analyze_feature_special_token_usage(self):
        """For each feature, determine what % of activations are special tokens"""
        
        print("\nAnalyzing features for special token dependency...")
        
        n_features = self.db.activation_matrix.shape[1]
        feature_stats = []
        
        for feature_idx in range(n_features):
            if feature_idx % 500 == 0:
                print(f"  Progress: {feature_idx}/{n_features}")
            
            activations = self.db.get_feature_activations(feature_idx, top_k=None)
            
            if len(activations) == 0:
                continue
            
            # Classify each activation
            category_counts = Counter()
            token_type_counts = Counter()  # Changed from defaultdict to Counter!
            
            for token_idx, act_val in activations:
                token_str = self.db.token_metadata[token_idx].token_str
                category = self.classify_token(token_str)
                category_counts[category] += 1
                token_type_counts[token_str] += 1
            
            total = len(activations)
            special_count = sum(count for cat, count in category_counts.items() if cat != 'normal')
            special_ratio = special_count / total if total > 0 else 0
            
            # Token diversity
            unique_tokens = len(token_type_counts)
            
            # Fix: Handle case where token_type_counts might be empty
            if len(token_type_counts) > 0:
                most_common_token, most_common_count = token_type_counts.most_common(1)[0]
                most_common_ratio = most_common_count / total
            else:
                most_common_token = ""
                most_common_count = 0
                most_common_ratio = 0.0
            
            # Entropy for diversity
            if unique_tokens > 0:
                token_probs = np.array(list(token_type_counts.values())) / total
                entropy = -np.sum(token_probs * np.log(token_probs + 1e-10))
                max_entropy = np.log(unique_tokens)
                normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
            else:
                normalized_entropy = 0.0
            
            feature_stats.append({
                'feature_idx': feature_idx,
                'total_activations': total,
                'special_ratio': special_ratio,
                'category_breakdown': dict(category_counts),
                'unique_tokens': unique_tokens,
                'diversity': normalized_entropy,
                'most_common_token': most_common_token,
                'most_common_ratio': most_common_ratio,
                'most_common_category': self.classify_token(most_common_token) if most_common_token else 'unknown'
            })
        
        return feature_stats
    
    def categorize_features(self, feature_stats):
        """Categorize features by their special token usage"""
        
        categories = {
            'special_only': [],      # >95% special tokens
            'special_heavy': [],     # 70-95% special tokens
            'special_moderate': [],  # 30-70% special tokens
            'mostly_normal': [],     # 10-30% special tokens
            'normal_only': [],       # <10% special tokens
        }
        
        for feat in feature_stats:
            ratio = feat['special_ratio']
            
            if ratio > 0.95:
                categories['special_only'].append(feat)
            elif ratio > 0.70:
                categories['special_heavy'].append(feat)
            elif ratio > 0.30:
                categories['special_moderate'].append(feat)
            elif ratio > 0.10:
                categories['mostly_normal'].append(feat)
            else:
                categories['normal_only'].append(feat)
        
        return categories
    
    def print_summary(self, feature_stats, categories):
        """Print comprehensive summary"""
        
        n_total = len(feature_stats)
        
        print("\n" + "="*80)
        print("SPECIAL TOKEN ANALYSIS SUMMARY")
        print("="*80 + "\n")
        
        print(f"Total active features: {n_total}\n")
        
        print("FEATURE CATEGORIZATION:")
        print("-"*80)
        for cat_name, features in categories.items():
            count = len(features)
            pct = count / n_total * 100 if n_total > 0 else 0
            print(f"{cat_name:20s}: {count:5d} ({pct:5.1f}%)")
        
        print("\n" + "="*80)
        print("CRITICAL ASSESSMENT")
        print("="*80 + "\n")
        
        special_problematic = len(categories['special_only']) + len(categories['special_heavy'])
        pct_problematic = special_problematic / n_total * 100
        
        if pct_problematic > 30:
            print("🚨 CRITICAL ISSUE: >30% of features dominated by special tokens!")
            print("   → SAE is wasting capacity on special tokens")
            print("   → RECOMMENDATION: Retrain with special token masking/filtering")
        elif pct_problematic > 10:
            print("⚠️  MODERATE CONCERN: 10-30% features are special-token heavy")
            print("   → Some wasted capacity, but not catastrophic")
            print("   → CONSIDER: Light filtering or accept as-is")
        else:
            print("✅ GOOD: <10% of features are special-token heavy")
            print("   → Minimal capacity waste")
            print("   → SAE is learning meaningful content features")
        
        print(f"\nSpecific breakdown:")
        print(f"  • Completely useless (>95% special): {len(categories['special_only'])} ({len(categories['special_only'])/n_total*100:.1f}%)")
        print(f"  • Mostly useless (70-95% special):   {len(categories['special_heavy'])} ({len(categories['special_heavy'])/n_total*100:.1f}%)")
        print(f"  • Useful features (<30% special):    {len(categories['mostly_normal']) + len(categories['normal_only'])} ({(len(categories['mostly_normal']) + len(categories['normal_only']))/n_total*100:.1f}%)")
    
    def identify_worst_offenders(self, feature_stats, top_k=30):
        """Identify features that are most dominated by special tokens"""
        
        sorted_features = sorted(feature_stats, key=lambda x: x['special_ratio'], reverse=True)
        
        print("\n" + "="*80)
        print(f"TOP {top_k} WORST OFFENDERS (most special-token dependent)")
        print("="*80 + "\n")
        
        for i, feat in enumerate(sorted_features[:top_k], 1):
            print(f"{i:2d}. Feature {feat['feature_idx']:5d}")
            print(f"    Special token ratio: {feat['special_ratio']*100:5.1f}%")
            print(f"    Most common: '{feat['most_common_token'][:50]}' ({feat['most_common_ratio']*100:.1f}%)")
            print(f"    Category breakdown: {feat['category_breakdown']}")
            print(f"    Total activations: {feat['total_activations']}")
            print()
    
    def create_visualizations(self, feature_stats, categories, output_dir):
        """Create comprehensive visualizations"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Extract data
        special_ratios = np.array([f['special_ratio'] for f in feature_stats])
        diversities = np.array([f['diversity'] for f in feature_stats])
        total_acts = np.array([f['total_activations'] for f in feature_stats])
        
        # Create figure
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Distribution of special token ratios
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.hist(special_ratios, bins=50, alpha=0.7, edgecolor='black', color='coral')
        ax1.axvline(0.30, color='orange', linestyle='--', linewidth=2, label='30% threshold')
        ax1.axvline(0.70, color='red', linestyle='--', linewidth=2, label='70% threshold')
        ax1.set_xlabel('Special Token Ratio', fontsize=12)
        ax1.set_ylabel('Number of Features', fontsize=12)
        ax1.set_title('Distribution of Special Token Dependency Across Features', fontsize=14)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Category pie chart
        ax2 = fig.add_subplot(gs[0, 2])
        cat_sizes = [len(features) for features in categories.values()]
        cat_labels = [f"{name}\n({size})" for name, size in zip(categories.keys(), cat_sizes)]
        colors_pie = ['darkred', 'red', 'orange', 'lightgreen', 'darkgreen']
        ax2.pie(cat_sizes, labels=cat_labels, colors=colors_pie, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Feature Categories', fontsize=12)
        
        # 3. Scatter: special ratio vs diversity
        ax3 = fig.add_subplot(gs[1, :2])
        scatter = ax3.scatter(special_ratios, diversities, 
                            c=np.log10(total_acts + 1), 
                            alpha=0.4, s=20, cmap='viridis')
        ax3.axvline(0.30, color='orange', linestyle='--', alpha=0.5)
        ax3.axvline(0.70, color='red', linestyle='--', alpha=0.5)
        ax3.axhline(0.5, color='blue', linestyle='--', alpha=0.5)
        ax3.set_xlabel('Special Token Ratio', fontsize=12)
        ax3.set_ylabel('Token Diversity', fontsize=12)
        ax3.set_title('Feature Characterization: Special Tokens vs Diversity', fontsize=14)
        plt.colorbar(scatter, ax=ax3, label='log10(Total Activations)')
        ax3.grid(True, alpha=0.3)
        
        # Add quadrant labels
        ax3.text(0.85, 0.8, 'Special\n+ Diverse', ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='orange', alpha=0.3), fontsize=9)
        ax3.text(0.15, 0.8, 'Normal\n+ Diverse\n(GOOD)', ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='green', alpha=0.3), fontsize=9)
        ax3.text(0.85, 0.2, 'Special\nMonosemantic\n(BAD)', ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='red', alpha=0.3), fontsize=9)
        ax3.text(0.15, 0.2, 'Normal\nMonosemantic', ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3), fontsize=9)
        
        # 4. Histogram of special ratios for special-heavy features only
        ax4 = fig.add_subplot(gs[1, 2])
        special_heavy_ratios = [f['special_ratio'] for f in feature_stats if f['special_ratio'] > 0.3]
        if special_heavy_ratios:
            ax4.hist(special_heavy_ratios, bins=30, alpha=0.7, edgecolor='black', color='red')
            ax4.set_xlabel('Special Token Ratio', fontsize=10)
            ax4.set_ylabel('Count', fontsize=10)
            ax4.set_title('Zoomed: Special-Heavy Features (>30%)', fontsize=11)
            ax4.grid(True, alpha=0.3)
        
        # 5. Breakdown by special token type (for special-heavy features)
        ax5 = fig.add_subplot(gs[2, :])
        
        # Aggregate category breakdowns
        type_totals = Counter()
        for feat in feature_stats:
            if feat['special_ratio'] > 0.3:  # Only special-heavy
                for cat, count in feat['category_breakdown'].items():
                    if cat != 'normal':
                        type_totals[cat] += count
        
        if type_totals:
            types = list(type_totals.keys())
            counts = list(type_totals.values())
            bars = ax5.barh(types, counts, alpha=0.7, edgecolor='black')
            
            # Color bars
            colors_types = plt.cm.Reds(np.linspace(0.4, 0.9, len(types)))
            for bar, color in zip(bars, colors_types):
                bar.set_color(color)
            
            ax5.set_xlabel('Total Activations on Special Tokens', fontsize=12)
            ax5.set_title('Breakdown of Special Token Types (for special-heavy features)', fontsize=14)
            ax5.grid(True, alpha=0.3, axis='x')
        
        plt.savefig(output_path / 'special_token_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✓ Saved visualization to {output_path / 'special_token_analysis.png'}")
    
    def save_detailed_report(self, feature_stats, categories, output_dir):
        """Save comprehensive text report"""
        
        output_path = Path(output_dir)
        report_path = output_path / 'special_token_report.txt'
        
        with open(report_path, 'w') as f:
            f.write("SPECIAL TOKEN ANALYSIS - DETAILED REPORT\n")
            f.write("="*80 + "\n\n")
            
            n_total = len(feature_stats)
            f.write(f"Total features analyzed: {n_total}\n\n")
            
            # Category breakdown
            f.write("FEATURE CATEGORIES:\n")
            f.write("-"*80 + "\n\n")
            for cat_name, features in categories.items():
                count = len(features)
                pct = count / n_total * 100
                f.write(f"{cat_name:20s}: {count:5d} ({pct:5.1f}%)\n")
            
            # Worst offenders
            f.write("\n\nWORST OFFENDERS (Top 50 special-token dependent features):\n")
            f.write("="*80 + "\n\n")
            
            sorted_features = sorted(feature_stats, key=lambda x: x['special_ratio'], reverse=True)
            
            for i, feat in enumerate(sorted_features[:50], 1):
                f.write(f"{i:2d}. Feature {feat['feature_idx']:5d}\n")
                f.write(f"    Special ratio: {feat['special_ratio']*100:5.1f}%\n")
                f.write(f"    Most common: '{feat['most_common_token'][:60]}'\n")
                f.write(f"    Category: {feat['most_common_category']}\n")
                f.write(f"    Breakdown: {feat['category_breakdown']}\n")
                f.write(f"    Diversity: {feat['diversity']:.3f}\n")
                f.write(f"    Total activations: {feat['total_activations']}\n\n")
        
        print(f"✓ Saved detailed report to {report_path}")


def run_special_token_analysis(
    activation_db_path: str,
    output_dir: str = 'special_token_analysis'
):
    """Main analysis function"""
    
    print("="*80)
    print("COMPREHENSIVE SPECIAL TOKEN ANALYSIS")
    print("="*80 + "\n")
    
    # Load database
    print("Loading activation database...")
    db = ActivationDatabase.load(activation_db_path)
    
    # Initialize analyzer
    analyzer = SpecialTokenAnalyzer(db)
    
    # 1. Analyze token distribution in corpus
    print("\n" + "="*80)
    print("STEP 1: Token Distribution in Corpus")
    print("="*80)
    token_dist, token_examples = analyzer.analyze_token_distribution(sample_size=20000)
    
    # 2. Analyze features
    print("\n" + "="*80)
    print("STEP 2: Feature-Level Analysis")
    print("="*80)
    feature_stats = analyzer.analyze_feature_special_token_usage()
    
    # 3. Categorize features
    categories = analyzer.categorize_features(feature_stats)
    
    # 4. Print summary
    analyzer.print_summary(feature_stats, categories)
    
    # 5. Identify worst offenders
    analyzer.identify_worst_offenders(feature_stats, top_k=30)
    
    # 6. Create visualizations
    print("\nCreating visualizations...")
    analyzer.create_visualizations(feature_stats, categories, output_dir)
    
    # 7. Save detailed report
    print("\nSaving detailed report...")
    analyzer.save_detailed_report(feature_stats, categories, output_dir)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print(f"\nResults saved to: {output_dir}/")
    
    return feature_stats, categories, token_dist


if __name__ == "__main__":
    ACTIVATION_DB_PATH = 'analysis_reborn_final/activation_database/activation_db_20251111_231938.pkl'
    OUTPUT_DIR = 'special_token_analysis'
    
    feature_stats, categories, token_dist = run_special_token_analysis(
        activation_db_path=ACTIVATION_DB_PATH,
        output_dir=OUTPUT_DIR
    )
    
    print("\n✓ Check special_token_analysis/ for detailed results")
