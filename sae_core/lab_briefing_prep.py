"""
Utility script to summarize the latest SAE analysis run and
surface physics-heavy features for quick presentation prep.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np
from transformer_lens import HookedTransformer

from sae_core.full_analysis import ActivationDatabase, SAEAnalyzer
from sae_core.data_processing.textbook_process import load_processed_data
from sae_core.ad_hoc_analysis_scripts.special_token_diagnosis import (
    SpecialTokenAnalyzer,
)


PHYSICS_KEYWORDS: Sequence[str] = [
    "newton",
    "force",
    "energy",
    "kinetic",
    "potential",
    "mass",
    "momentum",
    "velocity",
    "speed",
    "accelerat",
    "gravity",
    "gravit",
    "field",
    "electric",
    "charge",
    "current",
    "voltage",
    "resistance",
    "magnet",
    "flux",
    "coulomb",
    "gauss",
    "planck",
    "boltzmann",
    "photon",
    "wave",
    "frequency",
    "lambda",
    "omega",
    "ampere",
    "joule",
    "watt",
    "pascal",
    "pressure",
    "density",
    "torque",
    "rotation",
    "angular",
    "thermo",
    "temperature",
    "kelvin",
    "equation",
    "vector",
    "scalar",
    "circuit",
    "power",
    "work",
    "impulse",
    "resonance",
]

PHYSICS_UNITS = {
    "kg",
    "hz",
    "pa",
    "ohm",
    "omega",
    "m/s",
    "m∙s⁻¹",
    "m·s⁻¹",
    "m^2",
    "mv",
    "kv",
    "ma",
    "mev",
    "gev",
    "tev",
    "ev",
    "nm",
    "μm",
}


@dataclass
class FeatureContext:
    feature_idx: int
    physics_hits: List[Dict[str, object]]
    activation_frequency: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prep physics-heavy SAE features for lab briefing."
    )
    parser.add_argument(
        "--analysis-dir",
        type=Path,
        default=Path("analysis_reborn_final"),
        help="Directory containing SUMMARY/config and activation DB outputs.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Where to store markdown/JSON outputs (defaults to <analysis-dir>/lab_briefing).",
    )
    parser.add_argument(
        "--num-features",
        type=int,
        default=5,
        help="How many physics-heavy features to surface.",
    )
    parser.add_argument(
        "--scan-top-tokens",
        type=int,
        default=400,
        help="Number of top activations per feature to scan for physics tokens.",
    )
    parser.add_argument(
        "--min-physics-hits",
        type=int,
        default=3,
        help="Minimum keyword hits required before accepting a feature.",
    )
    parser.add_argument(
        "--contexts-per-feature",
        type=int,
        default=5,
        help="Maximum number of contexts to store per accepted feature.",
    )
    parser.add_argument(
        "--context-size",
        type=int,
        default=10,
        help="Context window (tokens) when displaying top activations.",
    )
    parser.add_argument(
        "--skip-dashboards",
        action="store_true",
        help="If set, do not regenerate feature dashboards.",
    )
    return parser.parse_args()


def find_latest_summary(analysis_dir: Path) -> Path:
    summaries = sorted(analysis_dir.glob("SUMMARY_*.json"))
    if not summaries:
        raise FileNotFoundError(f"No SUMMARY_* files found in {analysis_dir}")
    return summaries[-1]


def load_json(path: Path) -> Dict:
    with open(path, "r") as f:
        return json.load(f)


def write_json(path: Path, payload: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)


def normalize_token(token_str: str) -> str:
    return token_str.replace("▁", "").replace("Ġ", "").strip()


def token_is_physics(token_str: str) -> bool:
    normalized = normalize_token(token_str)
    lower_norm = normalized.lower()
    if len(lower_norm) >= 2 and lower_norm in PHYSICS_UNITS:
        return True
    return any(keyword in lower_norm for keyword in PHYSICS_KEYWORDS)


def gather_physics_features(
    db: ActivationDatabase,
    model: Optional[HookedTransformer],
    candidate_indices: Sequence[int],
    desired: int,
    scan_top_tokens: int,
    min_hits: int,
    max_hits: int,
    context_size: int,
) -> List[FeatureContext]:
    selected: List[FeatureContext] = []

    for feature_idx in candidate_indices:
        activations = db.get_feature_activations(feature_idx, top_k=scan_top_tokens)
        if not activations:
            continue

        physics_hits: List[Dict[str, object]] = []
        seen_tokens = set()

        for token_idx, act_val in activations:
            token_str = db.token_metadata[token_idx].token_str
            if not token_is_physics(token_str):
                continue

            if token_idx in seen_tokens:
                continue

            context = db.get_token_context(
                token_idx=token_idx, model=model, context_size=context_size
            )

            physics_hits.append(
                {
                    "token_idx": int(token_idx),
                    "token": normalize_token(token_str),
                    "activation": float(act_val),
                    "context": context["context"],
                    "text_idx": int(context["text_idx"]),
                    "position": int(context["position"]),
                }
            )
            seen_tokens.add(token_idx)

            if len(physics_hits) >= max_hits:
                break

        if len(physics_hits) >= min_hits:
            freq = db.feature_metadata["activation_counts"][feature_idx]
            selected.append(
                FeatureContext(
                    feature_idx=int(feature_idx),
                    physics_hits=physics_hits,
                    activation_frequency=int(freq),
                )
            )

        if len(selected) >= desired:
            break

    return selected


def summarize_special_tokens(
    analyzer: SpecialTokenAnalyzer,
    feature_indices: Sequence[int],
) -> Dict[int, Dict[str, object]]:
    stats: Dict[int, Dict[str, object]] = {}

    for feature_idx in feature_indices:
        activations = analyzer.db.get_feature_activations(feature_idx)
        if not activations:
            stats[feature_idx] = {
                "total_activations": 0,
                "special_ratio": 0.0,
                "category_breakdown": {},
            }
            continue

        category_counts: Counter[str] = Counter()
        token_type_counts: Counter[str] = Counter()

        for token_idx, _ in activations:
            token_str = analyzer.db.token_metadata[token_idx].token_str
            category = analyzer.classify_token(token_str)
            category_counts[category] += 1
            token_type_counts[token_str] += 1

        total = len(activations)
        special_count = total - category_counts.get("normal", 0)
        most_common_token, most_common_count = (
            token_type_counts.most_common(1)[0]
            if token_type_counts
            else ("", 0)
        )

        stats[feature_idx] = {
            "total_activations": total,
            "special_ratio": special_count / total if total else 0.0,
            "category_breakdown": dict(category_counts),
            "unique_tokens": len(token_type_counts),
            "most_common_token": normalize_token(most_common_token),
            "most_common_ratio": most_common_count / total if total else 0.0,
        }

    return stats


def build_markdown_report(
    summary: Dict,
    feature_contexts: List[FeatureContext],
    special_stats: Dict[int, Dict[str, object]],
) -> str:
    lines: List[str] = []
    lines.append(f"# Lab Briefing Snapshot ({summary['timestamp']})")
    lines.append("")
    lines.append("## Headline Metrics")
    lines.append(
        f"- Sparsity (L0): {summary['sparsity']['l0_mean']:.2f} ± {summary['sparsity']['l0_std']:.2f}"
    )
    lines.append(
        f"- Dead Features: {summary['dead_features']['n_dead']} "
        f"({summary['dead_features']['pct_dead']:.2f}%)"
    )
    lines.append(
        f"- Reconstruction: MSE {summary['reconstruction']['mse']:.4f}, "
        f"Explained Var {summary['reconstruction']['explained_variance']*100:.2f}%, "
        f"Cos Sim {summary['reconstruction']['cosine_similarity']:.3f}"
    )
    lines.append(
        f"- Loss Recovered (Ablation): {summary['ablation']['loss_recovered']*100:.2f}%"
    )
    lines.append("")
    lines.append("## Physics-Leaning Features")

    if not feature_contexts:
        lines.append("_No features met the physics keyword threshold._")
        return "\n".join(lines)

    for ctx in feature_contexts:
        stats = special_stats.get(ctx.feature_idx, {})
        special_pct = stats.get("special_ratio", 0.0) * 100
        lines.append(
            f"### Feature {ctx.feature_idx} "
            f"(activations: {ctx.activation_frequency:,}, special tokens: {special_pct:.2f}%)"
        )

        for hit in ctx.physics_hits:
            lines.append(
                f"- `{hit['token']}` @ text {hit['text_idx']} pos {hit['position']} "
                f"(act={hit['activation']:.3f}): {hit['context']}"
            )

        lines.append("")

    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    analysis_dir = args.analysis_dir
    analysis_dir.mkdir(parents=True, exist_ok=True)

    output_dir = args.output_dir or (analysis_dir / "lab_briefing")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_path = find_latest_summary(analysis_dir)
    summary = load_json(summary_path)
    timestamp = summary["timestamp"]

    config_path = analysis_dir / f"config_{timestamp}.json"
    config = load_json(config_path)

    activation_db_path = analysis_dir / summary["files"]["activation_db"]
    similarity_path = analysis_dir / summary["files"]["similarity_matrix"]
    cooccurrence_path = analysis_dir / summary["files"]["cooccurrence_matrix"]

    print(f"Loading activation DB from {activation_db_path} ...")
    activation_db = ActivationDatabase.load(str(activation_db_path))

    candidate_order = np.argsort(
        np.array(activation_db.feature_metadata["activation_counts"])
    )[::-1]

    contexts_per_feature = max(args.contexts_per_feature, args.min_physics_hits)

    physics_features = gather_physics_features(
        db=activation_db,
        model=None,
        candidate_indices=candidate_order,
        desired=args.num_features,
        scan_top_tokens=args.scan_top_tokens,
        min_hits=args.min_physics_hits,
        max_hits=contexts_per_feature,
        context_size=args.context_size,
    )

    if not physics_features:
        print(
            "WARNING: No features met the physics threshold. "
            "Consider relaxing --min-physics-hits or increasing --scan-top-tokens."
        )

    special_token_analyzer = SpecialTokenAnalyzer(activation_db)
    special_stats = summarize_special_tokens(
        special_token_analyzer,
        feature_indices=[fc.feature_idx for fc in physics_features],
    )

    report_text = build_markdown_report(summary, physics_features, special_stats)
    markdown_path = output_dir / f"lab_briefing_{timestamp}.md"
    markdown_path.write_text(report_text)
    print(f"Wrote markdown summary to {markdown_path}")

    feature_payload = {
        "timestamp": timestamp,
        "features": [
            {
                "feature_idx": ctx.feature_idx,
                "activation_frequency": ctx.activation_frequency,
                "physics_hits": ctx.physics_hits,
                "special_token_stats": special_stats.get(ctx.feature_idx, {}),
            }
            for ctx in physics_features
        ],
    }
    write_json(output_dir / f"physics_feature_contexts_{timestamp}.json", feature_payload)

    if physics_features and not args.skip_dashboards:
        print(f"Loading model {summary['model']} for dashboard regeneration ...")
        model = HookedTransformer.from_pretrained(summary["model"])
        texts = load_processed_data(config["data_path"])

        analyzer = SAEAnalyzer(
            model=model,
            sae_path=summary["sae_path"],
            layer=summary["layer"],
            hook_name=summary["hook_name"],
            dataset=texts,
        )
        analyzer.activation_db = activation_db
        analyzer.feature_similarity = np.load(similarity_path)
        analyzer.feature_cooccurrence = np.load(cooccurrence_path)

        dashboard_dir = output_dir / "dashboards"
        dashboard_dir.mkdir(parents=True, exist_ok=True)
        for ctx in physics_features:
            save_path = dashboard_dir / f"feature_{ctx.feature_idx}_dashboard.png"
            print(f"Regenerating dashboard for feature {ctx.feature_idx} ...")
            analyzer.create_feature_dashboard(
                feature_idx=ctx.feature_idx,
                save_path=str(save_path),
            )

    print("Done.")


if __name__ == "__main__":
    main()
