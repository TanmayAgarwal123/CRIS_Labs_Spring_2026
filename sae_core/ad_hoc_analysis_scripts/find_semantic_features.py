"""
Advanced Feature Discovery for Domain-Specific Concepts
Finds semantic/scientific features rather than syntactic ones
"""

import numpy as np
from pathlib import Path
from collections import Counter
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sae_core.full_analysis import ActivationDatabase
from transformer_lens import HookedTransformer


class SemanticFeatureDiscovery:
    """Find semantically interesting features using multiple strategies"""
    
    def __init__(self, activation_db: ActivationDatabase, model: HookedTransformer):
        self.db = activation_db
        self.model = model
        
        # Common stopwords and syntactic tokens to filter
        self.stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'it', 'its', 'he', 'she', 'they', 'we',
            'i', 'you', 'me', 'him', 'her', 'them', 'us'
        }
        
        # HTML/formatting tokens
        self.formatting_patterns = [
            r'^\s*$',  # Only whitespace
            r'^[^\w\s]+$',  # Only punctuation
            r'^\d+$',  # Only numbers
            r'colspan|rowspan|class|style|div|span',  # HTML
        ]
    
    def is_stopword_or_formatting(self, token_str: str) -> bool:
        """Check if token is a stopword or formatting token"""
        token_clean = token_str.strip().lower()
        
        # Check stopwords
        if token_clean in self.stopwords:
            return True
        
        # Check formatting patterns
        for pattern in self.formatting_patterns:
            if re.search(pattern, token_str, re.IGNORECASE):
                return True
        
        # Single character (except meaningful ones)
        if len(token_clean) == 1 and token_clean not in {'q', 'e', 'c', 'h', 'n'}:
            return True
        
        return False
    
    def compute_token_specificity(self, token_str: str) -> float:
        """
        Estimate how domain-specific a token is
        Higher scores = more specific/rare
        """
        token_clean = token_str.strip().lower()
        
        # Length bonus (longer tokens tend to be more specific)
        length_score = min(len(token_clean) / 20.0, 1.0)
        
        # Capital letters (proper nouns, physics notation)
        has_capitals = any(c.isupper() for c in token_str.strip())
        capital_score = 0.3 if has_capitals else 0.0
        
        # Contains numbers or Greek letters (physics notation)
        has_numbers = bool(re.search(r'\d', token_str))
        number_score = 0.2 if has_numbers else 0.0
        
        # Domain-specific keywords (physics-related)
        physics_keywords = [
            'quantum', 'energy', 'momentum', 'force', 'mass', 'velocity',
            'acceleration', 'wave', 'particle', 'field', 'charge', 'magnetic',
            'electric', 'thermal', 'entropy', 'photon', 'electron', 'atom',
            'nuclear', 'radiation', 'equation', 'theorem', 'law', 'principle',
            'relativity', 'mechanics', 'dynamics', 'static', 'kinetic',
            'potential', 'conservation', 'symmetry', 'invariant', 'vector',
            'tensor', 'scalar', 'matrix', 'operator', 'hamiltonian', 'lagrangian'
        ]
        
        domain_score = 0.0
        for keyword in physics_keywords:
            if keyword in token_clean:
                domain_score = 0.5
                break
        
        return length_score + capital_score + number_score + domain_score
    
    def score_feature_by_specificity(self, feature_idx: int) -> dict:
        """
        Score a feature by how specific/semantic its activations are
        """
        activations = self.db.get_feature_activations(feature_idx, top_k=100)
        
        if len(activations) == 0:
            return None
        
        # Analyze tokens this feature fires on
        token_strs = []
        activation_values = []
        stopword_count = 0
        
        for token_idx, act_val in activations:
            token_str = self.db.token_metadata[token_idx].token_str
            token_strs.append(token_str)
            activation_values.append(act_val)
            
            if self.is_stopword_or_formatting(token_str):
                stopword_count += 1
        
        stopword_ratio = stopword_count / len(activations)
        
        # Skip if mostly stopwords
        if stopword_ratio > 0.5:
            return None
        
        # Compute average token specificity
        specificities = [self.compute_token_specificity(t) for t in token_strs]
        avg_specificity = np.mean(specificities)
        
        # Compute activation statistics
        mean_activation = np.mean(activation_values)
        max_activation = np.max(activation_values)
        activation_variance = np.var(activation_values)
        
        # Frequency (penalize too common)
        frequency = len(activations)
        frequency_penalty = 1.0 / (1.0 + np.log(frequency / 1000.0)) if frequency > 1000 else 1.0
        
        # Combined score
        score = (
            avg_specificity * 100 +  # Specificity is most important
            mean_activation * 10 +    # Higher activations
            max_activation * 5 +      # Peak activation matters
            activation_variance * 2   # Prefer features with varying strength
        ) * frequency_penalty * (1 - stopword_ratio)
        
        return {
            'feature_idx': feature_idx,
            'score': score,
            'avg_specificity': avg_specificity,
            'stopword_ratio': stopword_ratio,
            'mean_activation': mean_activation,
            'max_activation': max_activation,
            'frequency': frequency,
            'top_tokens': token_strs[:10]
        }
    
    def find_multi_token_features(self, feature_idx: int, context_size: int = 3) -> list:
        """
        Find features that activate on multi-token patterns (concepts)
        """
        activations = self.db.get_feature_activations(feature_idx, top_k=50)
        
        patterns = []
        for token_idx, act_val in activations:
            context = self.db.get_token_context(token_idx, self.model, context_size=context_size)
            
            # Extract window around target token
            tokens = context['context_tokens']
            target_pos = context_size  # Target is in middle
            
            if len(tokens) >= 2:
                window = tokens[max(0, target_pos-2):min(len(tokens), target_pos+3)]
                pattern = ' '.join(window)
                patterns.append((pattern, act_val))
        
        return patterns
    
    def discover_semantic_features(
        self,
        min_frequency: int = 100,
        max_frequency: int = 50000,
        top_k: int = 100,
        verbose: bool = True
    ) -> list:
        """
        Main discovery method - finds semantically interesting features
        """
        print("Discovering semantic features...")
        print(f"  Scanning {self.db.activation_matrix.shape[1]} features...")
        
        feature_scores = []
        
        for feature_idx in range(self.db.activation_matrix.shape[1]):
            if verbose and feature_idx % 500 == 0:
                print(f"  Progress: {feature_idx}/{self.db.activation_matrix.shape[1]}")
            
            # Get basic frequency
            activations = self.db.get_feature_activations(feature_idx, top_k=10)
            
            if len(activations) == 0:
                continue
            
            # Frequency filter
            freq = self.db.feature_metadata['activation_counts'][feature_idx]
            if freq < min_frequency or freq > max_frequency:
                continue
            
            # Compute semantic score
            score_info = self.score_feature_by_specificity(feature_idx)
            
            if score_info is not None and score_info['stopword_ratio'] < 0.3:
                feature_scores.append(score_info)
        
        # Sort by score
        feature_scores.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"\n✓ Found {len(feature_scores)} semantic features")
        print(f"  (Filtered out {self.db.activation_matrix.shape[1] - len(feature_scores)} features)")
        
        return feature_scores[:top_k]
    
    def find_concept_clusters(self, feature_scores: list, cooccurrence_matrix: np.ndarray = None) -> dict:
        """
        Group features into semantic clusters using co-occurrence
        """
        if cooccurrence_matrix is None:
            print("Warning: No co-occurrence matrix provided, skipping clustering")
            return {}
        
        print("\nFinding concept clusters...")
        
        # Extract feature indices
        feature_indices = [f['feature_idx'] for f in feature_scores[:50]]
        
        # Build similarity graph
        clusters = {}
        visited = set()
        
        for i, feat_i in enumerate(feature_indices):
            if feat_i in visited:
                continue
            
            # Find highly co-occurring features
            cluster = [feat_i]
            visited.add(feat_i)
            
            for feat_j in feature_indices[i+1:]:
                if feat_j in visited:
                    continue
                
                cooccur = cooccurrence_matrix[feat_i, feat_j]
                
                if cooccur > 0.3:  # Threshold for clustering
                    cluster.append(feat_j)
                    visited.add(feat_j)
            
            if len(cluster) > 1:
                clusters[f"cluster_{len(clusters)}"] = cluster
        
        print(f"✓ Found {len(clusters)} concept clusters")
        
        return clusters


def analyze_semantic_features(
    activation_db_path: str,
    model_name: str = "qwen3-0.6b",
    cooccurrence_path: str = None,
    output_dir: str = 'analysis_semantic'
):
    """
    Run semantic feature discovery
    """
    
    print("="*80)
    print("SEMANTIC FEATURE DISCOVERY")
    print("="*80)
    
    # Load data
    print(f"\nLoading activation database...")
    db = ActivationDatabase.load(activation_db_path)
    
    print(f"Loading model...")
    model = HookedTransformer.from_pretrained(model_name)
    
    # Initialize discovery
    discovery = SemanticFeatureDiscovery(db, model)
    
    # Find semantic features
    semantic_features = discovery.discover_semantic_features(
        min_frequency=100,     # At least 100 activations
        max_frequency=20000,   # But not too common
        top_k=100,
        verbose=True
    )
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save results
    results_path = output_path / 'semantic_features.txt'
    with open(results_path, 'w') as f:
        f.write("SEMANTIC FEATURE DISCOVERY\n")
        f.write("="*80 + "\n\n")
        f.write(f"Found {len(semantic_features)} semantic features\n\n")
        f.write("Top Features (by semantic specificity):\n")
        f.write("-"*80 + "\n\n")
        
        for i, feat_info in enumerate(semantic_features[:50], 1):
            f.write(f"{i:3d}. Feature {feat_info['feature_idx']:4d}\n")
            f.write(f"     Score: {feat_info['score']:.2e} | ")
            f.write(f"Specificity: {feat_info['avg_specificity']:.3f} | ")
            f.write(f"Freq: {feat_info['frequency']:6d}\n")
            f.write(f"     Max Act: {feat_info['max_activation']:.3f} | ")
            f.write(f"Mean Act: {feat_info['mean_activation']:.3f} | ")
            f.write(f"Stopwords: {feat_info['stopword_ratio']*100:.1f}%\n")
            f.write(f"     Top tokens: {', '.join(feat_info['top_tokens'][:5])}\n")
            
            # Get example contexts
            activations = db.get_feature_activations(feat_info['feature_idx'], top_k=3)
            for token_idx, act_val in activations:
                context = db.get_token_context(token_idx, model, context_size=8)
                f.write(f"       → {context['context'][:100]}...\n")
            f.write("\n")
    
    print(f"\n✓ Saved semantic features to: {results_path}")
    
    # Print top 20 to console
    print("\n" + "="*80)
    print("TOP 20 SEMANTIC FEATURES")
    print("="*80 + "\n")
    
    for i, feat_info in enumerate(semantic_features[:20], 1):
        print(f"{i:2d}. Feature {feat_info['feature_idx']:4d} | "
              f"Score: {feat_info['score']:.2e} | "
              f"Specificity: {feat_info['avg_specificity']:.2f}")
        print(f"    Top tokens: {', '.join(feat_info['top_tokens'][:5])}")
        
        # Show best example
        activations = db.get_feature_activations(feat_info['feature_idx'], top_k=1)
        if activations:
            token_idx, act_val = activations[0]
            context = db.get_token_context(token_idx, model, context_size=8)
            print(f"    Example: ...{context['context'][:80]}...")
        print()
    
    # Try clustering if co-occurrence available
    if cooccurrence_path and Path(cooccurrence_path).exists():
        print("\nLoading co-occurrence matrix for clustering...")
        cooccurrence = np.load(cooccurrence_path)
        
        clusters = discovery.find_concept_clusters(semantic_features, cooccurrence)
        
        if clusters:
            clusters_path = output_path / 'concept_clusters.txt'
            with open(clusters_path, 'w') as f:
                f.write("CONCEPT CLUSTERS\n")
                f.write("="*80 + "\n\n")
                
                for cluster_name, feature_ids in clusters.items():
                    f.write(f"\n{cluster_name.upper()}: Features {feature_ids}\n")
                    f.write("-"*80 + "\n")
                    
                    for feat_idx in feature_ids:
                        # Find in semantic_features
                        feat_info = next((f for f in semantic_features if f['feature_idx'] == feat_idx), None)
                        if feat_info:
                            f.write(f"  Feature {feat_idx}: {', '.join(feat_info['top_tokens'][:3])}\n")
                    f.write("\n")
            
            print(f"✓ Saved concept clusters to: {clusters_path}")
    
    print("\n" + "="*80)
    print("DISCOVERY COMPLETE")
    print("="*80)
    
    return semantic_features


if __name__ == "__main__":
    # Configuration
    ACTIVATION_DB_PATH = 'analysis/activation_database/activation_db_20251104_210231.pkl'
    MODEL_NAME = "qwen3-0.6b"
    COOCCURRENCE_PATH = 'analysis/matrices/feature_cooccurrence_20251104_210231.npy'
    OUTPUT_DIR = 'analysis_semantic'
    
    # Run discovery
    semantic_features = analyze_semantic_features(
        activation_db_path=ACTIVATION_DB_PATH,
        model_name=MODEL_NAME,
        cooccurrence_path=COOCCURRENCE_PATH,
        output_dir=OUTPUT_DIR
    )
    
    print(f"\n✓ Check {OUTPUT_DIR}/ for detailed results")