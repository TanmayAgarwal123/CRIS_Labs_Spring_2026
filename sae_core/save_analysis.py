import json
import pickle
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class SAEResultsSaver:
    """Save and load SAE analysis results"""
    
    def __init__(self, base_dir: str = "./sae_results"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True, parents=True)
    
    def save_analysis(
        self, 
        sparsity_results: Dict,
        dead_features: Dict,
        reconstruction: Dict,
        ablation: Dict,
        run_name: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Save all analysis results to disk
        
        Args:
            sparsity_results: Output from compute_sparsity_metrics()
            dead_features: Output from find_dead_features()
            reconstruction: Output from compute_layer_reconstruction_metrics()
            ablation: Output from ablation_study()
            run_name: Optional name for this run (default: timestamp)
            metadata: Optional dict with model info, config, etc.
        
        Returns:
            Path to saved results directory
        """
        # Create run directory
        if run_name is None:
            run_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        run_dir = self.base_dir / run_name
        run_dir.mkdir(exist_ok=True, parents=True)
        
        # 1. Save main metrics (JSON - human readable)
        metrics = {
            'sparsity': {
                'l0_mean': sparsity_results['l0_mean'],
                'l0_std': sparsity_results['l0_std'],
                'l1_mean': sparsity_results['l1_mean'],
                'l1_std': sparsity_results['l1_std'],
                'n_features': sparsity_results['n_features'],
                'n_tokens': sparsity_results['n_tokens']
            },
            'dead_features': {
                'n_dead': dead_features['n_dead'],
                'pct_dead': dead_features['pct_dead'],
                'dead_indices': dead_features['dead_indices']
            },
            'reconstruction': reconstruction,
            'ablation': ablation,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        
        with open(run_dir / 'metrics.json', 'w') as f:
            json.dump(metrics, f, indent=2)
        
        # 2. Save large arrays separately (NumPy - efficient)
        # Feature frequencies
        feature_freq = np.array(sparsity_results['feature_freq'])
        np.save(run_dir / 'feature_frequencies.npy', feature_freq)
        
        # Activation frequencies
        activation_freq = np.array(dead_features['activation_freq'])
        np.save(run_dir / 'activation_frequencies.npy', activation_freq)
        
        # 3. Create summary report (text file)
        self._save_summary_report(run_dir, metrics)
        
        print(f"✓ Results saved to: {run_dir}")
        print(f"  - metrics.json: Main results")
        print(f"  - feature_frequencies.npy: Feature activation frequencies")
        print(f"  - summary.txt: Human-readable report")
        
        return run_dir
    
    def _save_summary_report(self, run_dir: Path, metrics: Dict):
        """Generate a human-readable summary report"""
        with open(run_dir / 'summary.txt', 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("SAE ANALYSIS SUMMARY\n")
            f.write("=" * 60 + "\n\n")
            
            if metrics['metadata']:
                f.write("METADATA\n")
                f.write("-" * 60 + "\n")
                for key, val in metrics['metadata'].items():
                    f.write(f"{key}: {val}\n")
                f.write("\n")
            
            f.write("SPARSITY METRICS\n")
            f.write("-" * 60 + "\n")
            s = metrics['sparsity']
            f.write(f"L0 Mean (Active Features): {s['l0_mean']:.2f}\n")
            f.write(f"L0 Std: {s['l0_std']:.2f}\n")
            f.write(f"L1 Mean: {s['l1_mean']:.2f}\n")
            f.write(f"L1 Std: {s['l1_std']:.2f}\n")
            f.write(f"Total Features: {s['n_features']}\n")
            f.write(f"Tokens Analyzed: {s['n_tokens']}\n\n")
            
            f.write("DEAD FEATURES\n")
            f.write("-" * 60 + "\n")
            d = metrics['dead_features']
            f.write(f"Dead Features: {d['n_dead']} ({d['pct_dead']:.1f}%)\n\n")
            
            f.write("RECONSTRUCTION QUALITY\n")
            f.write("-" * 60 + "\n")
            r = metrics['reconstruction']
            f.write(f"MSE Loss: {r['mse_loss']:.6f}\n")
            f.write(f"Explained Variance: {r['explained_variance']:.4f}\n")
            f.write(f"Cosine Similarity: {r['cosine_similarity']:.4f}\n")
            f.write(f"Reconstruction Error: {r['reconstruction_error']:.6f}\n\n")
            
            f.write("ABLATION STUDY\n")
            f.write("-" * 60 + "\n")
            a = metrics['ablation']
            f.write(f"Baseline Loss: {a['baseline_loss']:.4f}\n")
            f.write(f"Zero Ablation Loss: {a['zero_ablation_loss']:.4f}\n")
            f.write(f"SAE Reconstruction Loss: {a['sae_reconstruction_loss']:.4f}\n")
            f.write(f"Loss Recovered: {a['loss_recovered']:.4f} ({a['loss_recovered']*100:.1f}%)\n\n")
            
            f.write("=" * 60 + "\n")
            f.write(f"Generated: {metrics['timestamp']}\n")
    
    def save_feature_examples(
        self, 
        feature_idx: int,
        examples: list,
        run_name: str
    ):
        """
        Save max activating examples for a specific feature
        
        Args:
            feature_idx: Feature index
            examples: List of example dicts from find_max_activating_examples()
            run_name: Name of the run (must match existing run)
        """
        run_dir = self.base_dir / run_name
        
        # Create examples subdirectory
        examples_dir = run_dir / "feature_examples"
        examples_dir.mkdir(exist_ok=True)
        
        # Save as JSON
        with open(examples_dir / f"feature_{feature_idx}.json", 'w') as f:
            json.dump({
                'feature_idx': feature_idx,
                'examples': examples,
                'n_examples': len(examples)
            }, f, indent=2)
        
        # Also save as readable text
        with open(examples_dir / f"feature_{feature_idx}.txt", 'w') as f:
            f.write(f"Max Activating Examples for Feature {feature_idx}\n")
            f.write("=" * 60 + "\n\n")
            for i, ex in enumerate(examples, 1):
                f.write(f"{i}. Activation: {ex['activation']:.4f}\n")
                f.write(f"   Position: {ex['position']}\n")
                f.write(f"   Text: {ex['text']}\n\n")
        
        print(f"✓ Feature {feature_idx} examples saved to: {examples_dir}")
    
    def load_analysis(self, run_name: str) -> Dict[str, Any]:
        """
        Load saved analysis results
        
        Args:
            run_name: Name of the run to load
        
        Returns:
            Dictionary with all results
        """
        run_dir = self.base_dir / run_name
        
        if not run_dir.exists():
            raise FileNotFoundError(f"Run '{run_name}' not found in {self.base_dir}")
        
        # Load metrics
        with open(run_dir / 'metrics.json', 'r') as f:
            metrics = json.load(f)
        
        # Load arrays
        feature_freq = np.load(run_dir / 'feature_frequencies.npy')
        activation_freq = np.load(run_dir / 'activation_frequencies.npy')
        
        results = {
            'metrics': metrics,
            'feature_frequencies': feature_freq,
            'activation_frequencies': activation_freq,
            'run_name': run_name,
            'run_dir': str(run_dir)
        }
        
        print(f"✓ Loaded results from: {run_dir}")
        
        return results
    
    def load_feature_examples(self, run_name: str, feature_idx: int) -> Dict:
        """Load saved feature examples"""
        run_dir = self.base_dir / run_name
        examples_file = run_dir / "feature_examples" / f"feature_{feature_idx}.json"
        
        if not examples_file.exists():
            raise FileNotFoundError(f"Examples for feature {feature_idx} not found")
        
        with open(examples_file, 'r') as f:
            return json.load(f)
    
    def list_runs(self) -> list:
        """List all saved runs"""
        runs = []
        for run_dir in self.base_dir.iterdir():
            if run_dir.is_dir() and (run_dir / 'metrics.json').exists():
                runs.append(run_dir.name)
        return sorted(runs)
    
    def compare_runs(self, run_names: list) -> Dict:
        """Compare metrics across multiple runs"""
        comparison = {
            'runs': [],
            'sparsity': {'l0_mean': [], 'l0_std': []},
            'dead_features': {'n_dead': [], 'pct_dead': []},
            'reconstruction': {'mse_loss': [], 'explained_variance': []},
            'ablation': {'loss_recovered': []}
        }
        
        for run_name in run_names:
            results = self.load_analysis(run_name)
            metrics = results['metrics']
            
            comparison['runs'].append(run_name)
            comparison['sparsity']['l0_mean'].append(metrics['sparsity']['l0_mean'])
            comparison['sparsity']['l0_std'].append(metrics['sparsity']['l0_std'])
            comparison['dead_features']['n_dead'].append(metrics['dead_features']['n_dead'])
            comparison['dead_features']['pct_dead'].append(metrics['dead_features']['pct_dead'])
            comparison['reconstruction']['mse_loss'].append(metrics['reconstruction']['mse_loss'])
            comparison['reconstruction']['explained_variance'].append(metrics['reconstruction']['explained_variance'])
            comparison['ablation']['loss_recovered'].append(metrics['ablation']['loss_recovered'])
        
        return comparison


# Helper function for quick saving
def save_sae_analysis(
    sparsity_results,
    dead_features,
    reconstruction,
    ablation,
    run_name=None,
    base_dir="./sae_results",
    **metadata
):
    """Quick save function"""
    saver = SAEResultsSaver(base_dir)
    return saver.save_analysis(
        sparsity_results,
        dead_features,
        reconstruction,
        ablation,
        run_name,
        metadata
    )


# Helper function for quick loading
def load_sae_analysis(run_name, base_dir="./sae_results"):
    """Quick load function"""
    saver = SAEResultsSaver(base_dir)
    return saver.load_analysis(run_name)