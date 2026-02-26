"""
Generate dashboards for the most interesting physics features
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import json

from sae_core.full_analysis import SAEAnalyzer, ActivationDatabase
from transformer_lens import HookedTransformer
from sae_core.data_processing.textbook_process import load_processed_data
import numpy as np


def create_physics_dashboards(
    activation_db_path: str,
    model_name: str = "qwen3-0.6b",
    sae_path: str = None,
    layer: int = 12,
    hook_name: str = 'hook_resid_post',
    data_path: str = None,
    similarity_path: str = None,
    cooccurrence_path: str = None,
    output_dir: str = 'physics_features'
):
    """
    Create comprehensive dashboards for physics-related features
    """
    
    print("="*80)
    print("PHYSICS FEATURE ANALYSIS")
    print("="*80)
    
    # Top physics features from semantic discovery (hand-curated)
    physics_features = {
        7428: 'acceleration',
        3634: 'force',
        5988: 'velocity',
        830: 'mass',
        5736: 'magnitude',
        5673: 'Newton',
        5499: 'momentum',
        908: 'vector',
        7633: 'kinetic',
        2516: 'angular',
        6321: 'displacement',
        841: 'drag',
        3944: 'normal_force',
        4908: 'potential',
        6158: 'kinetic_energy',
        4503: 'equation',
        3984: 'horizontal',
        5236: 'direction',
        5185: 'friction',
        4035: 'constant',
        6331: 'law',
        5764: 'change',
    }
    
    print(f"\nAnalyzing {len(physics_features)} physics features...")
    
    # Load data
    print("\nLoading activation database...")
    db = ActivationDatabase.load(activation_db_path)
    
    print("Loading model...")
    model = HookedTransformer.from_pretrained(model_name)
    
    print("Loading dataset...")
    texts = load_processed_data(data_path)
    
    # Initialize analyzer
    print("Initializing analyzer...")
    analyzer = SAEAnalyzer(
        model=model,
        sae_path=sae_path,
        layer=layer,
        hook_name=hook_name,
        dataset=texts
    )
    analyzer.activation_db = db
    
    # Load pre-computed matrices
    if similarity_path:
        print(f"Loading similarity matrix...")
        analyzer.feature_similarity = np.load(similarity_path)
    
    if cooccurrence_path:
        print(f"Loading co-occurrence matrix...")
        analyzer.feature_cooccurrence = np.load(cooccurrence_path)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    dashboards_path = output_path / 'dashboards'
    dashboards_path.mkdir(exist_ok=True)
    
    # Create summary document
    summary = {
        'physics_features': {},
        'feature_relationships': {}
    }
    
    # Generate dashboards
    print("\nCreating feature dashboards...")
    for feature_idx, concept_name in physics_features.items():
        print(f"  {concept_name} (Feature {feature_idx})...")
        
        try:
            # Create dashboard
            analyzer.create_feature_dashboard(
                feature_idx=feature_idx,
                save_path=str(dashboards_path / f'{concept_name}_feature_{feature_idx}_dashboard.png')
            )
            plt.close('all')
            
            # Get feature statistics
            activations = db.get_feature_activations(feature_idx, top_k=10)
            freq = db.feature_metadata['activation_counts'][feature_idx]
            mean_act = db.feature_metadata['mean_activation'][feature_idx]
            
            # Get top examples
            examples = []
            for token_idx, act_val in activations[:5]:
                context = db.get_token_context(token_idx, model, context_size=10)
                examples.append({
                    'token': context['token'],
                    'activation': float(act_val),
                    'context': context['context']
                })
            
            summary['physics_features'][concept_name] = {
                'feature_idx': feature_idx,
                'frequency': int(freq),
                'mean_activation': float(mean_act),
                'top_examples': examples
            }
            
            # Find related physics features
            if analyzer.feature_similarity is not None:
                similar = analyzer.find_similar_features(feature_idx, top_k=5)
                related = []
                for sim_feat, sim_score in similar:
                    if sim_feat in physics_features:
                        related.append({
                            'feature': physics_features[sim_feat],
                            'feature_idx': sim_feat,
                            'similarity': float(sim_score)
                        })
                
                if related:
                    summary['feature_relationships'][concept_name] = related
            
        except Exception as e:
            print(f"    WARNING: Failed to analyze {concept_name}: {e}")
    
    # Save summary
    summary_path = output_path / 'physics_features_summary.json'
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n✓ Saved summary to: {summary_path}")
    
    # Create human-readable report
    report_path = output_path / 'PHYSICS_FEATURES_REPORT.md'
    with open(report_path, 'w') as f:
        f.write("# Physics Features Analysis Report\n\n")
        f.write(f"Analyzed {len(physics_features)} physics-related features from SAE\n\n")
        f.write("---\n\n")
        
        for concept_name, info in summary['physics_features'].items():
            f.write(f"## {concept_name.upper()}\n\n")
            f.write(f"**Feature Index:** {info['feature_idx']}\n\n")
            f.write(f"**Frequency:** {info['frequency']:,} tokens ({info['frequency']/db.feature_metadata['n_tokens']*100:.2f}%)\n\n")
            f.write(f"**Mean Activation:** {info['mean_activation']:.3f}\n\n")
            f.write("**Top Examples:**\n\n")
            
            for i, ex in enumerate(info['top_examples'], 1):
                f.write(f"{i}. Token: `{ex['token']}` (activation: {ex['activation']:.2f})\n")
                f.write(f"   ```\n   {ex['context'][:120]}...\n   ```\n\n")
            
            # Related features
            if concept_name in summary['feature_relationships']:
                f.write("**Related Physics Features:**\n\n")
                for rel in summary['feature_relationships'][concept_name]:
                    f.write(f"- {rel['feature']} (similarity: {rel['similarity']:.3f})\n")
                f.write("\n")
            
            f.write("---\n\n")
    
    print(f"✓ Saved report to: {report_path}")
    
    # Create feature co-occurrence heatmap for physics features only
    if analyzer.feature_cooccurrence is not None:
        print("\nCreating physics feature co-occurrence heatmap...")
        
        physics_indices = list(physics_features.keys())
        physics_labels = [physics_features[idx] for idx in physics_indices]
        
        # Extract submatrix
        cooccur_subset = analyzer.feature_cooccurrence[np.ix_(physics_indices, physics_indices)]
        
        # Plot
        fig, ax = plt.subplots(figsize=(14, 12))
        
        import seaborn as sns
        sns.heatmap(
            cooccur_subset,
            xticklabels=physics_labels,
            yticklabels=physics_labels,
            cmap='YlOrRd',
            square=True,
            cbar_kws={"label": "Co-occurrence Score"},
            ax=ax,
            annot=False
        )
        
        ax.set_title('Physics Concept Co-occurrence', fontsize=16, pad=20)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        plt.savefig(output_path / 'physics_cooccurrence_heatmap.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Saved co-occurrence heatmap")
    
    # Create frequency comparison
    print("\nCreating feature frequency comparison...")
    
    feature_names = []
    frequencies = []
    mean_activations = []
    
    for concept_name in sorted(physics_features.keys()):
        concept_label = physics_features[concept_name]
        info = summary['physics_features'][concept_label]
        feature_names.append(concept_label)
        frequencies.append(info['frequency'])
        mean_activations.append(info['mean_activation'])
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Frequency plot
    bars1 = ax1.barh(feature_names, frequencies, alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Frequency (number of activations)', fontsize=12)
    ax1.set_title('Physics Feature Activation Frequency', fontsize=14, pad=15)
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Color bars by frequency
    colors = plt.cm.viridis(np.array(frequencies) / max(frequencies))
    for bar, color in zip(bars1, colors):
        bar.set_color(color)
    
    # Mean activation plot
    bars2 = ax2.barh(feature_names, mean_activations, alpha=0.7, edgecolor='black', color='coral')
    ax2.set_xlabel('Mean Activation Value', fontsize=12)
    ax2.set_title('Physics Feature Mean Activation Strength', fontsize=14, pad=15)
    ax2.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig(output_path / 'physics_feature_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved feature comparison plot")
    
    print("\n" + "="*80)
    print("PHYSICS FEATURE ANALYSIS COMPLETE")
    print("="*80)
    print(f"\nOutputs saved to: {output_path}/")
    print(f"  • Dashboards: {dashboards_path}/")
    print(f"  • Summary: {summary_path}")
    print(f"  • Report: {report_path}")
    print(f"  • Visualizations: {output_path}/*.png")
    
    return summary


if __name__ == "__main__":
    # Configuration
    ACTIVATION_DB_PATH = 'analysis/activation_database/activation_db_20251104_210231.pkl'
    MODEL_NAME = "qwen3-0.6b"
    SAE_PATH = 'qwen3_06B.blocks.12.hook_resid_post.sae.sparsity60.mse0.001.kl0.01.physics10.exp8'
    LAYER = 12
    HOOK_NAME = 'hook_resid_post'
    DATA_PATH = 'sae_core/data/processed_data/processed_physics_10_ch.json'
    SIMILARITY_PATH = 'analysis/matrices/feature_similarity_20251104_210231.npy'
    COOCCURRENCE_PATH = 'analysis/matrices/feature_cooccurrence_20251104_210231.npy'
    OUTPUT_DIR = 'physics_features'
    
    summary = create_physics_dashboards(
        activation_db_path=ACTIVATION_DB_PATH,
        model_name=MODEL_NAME,
        sae_path=SAE_PATH,
        layer=LAYER,
        hook_name=HOOK_NAME,
        data_path=DATA_PATH,
        similarity_path=SIMILARITY_PATH,
        cooccurrence_path=COOCCURRENCE_PATH,
        output_dir=OUTPUT_DIR
    )
    
    print("\n✓ Analysis complete! Check physics_features/ for results")