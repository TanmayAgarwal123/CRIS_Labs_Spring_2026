"""Phase 13 — Cross-model scaling plots and per-(model, dataset) bootstrap CI tables.

Reads every JSON written by Phase 9 evaluate_reading_vectors. The eval
files already carry per-layer bootstrap CIs and an identified best layer;
this script:

  - lays out a layerwise accuracy curve per (model, dataset)
  - lays out the headline scaling plot (best-layer accuracy vs model size,
    log-x, error bars from bootstrap CIs, chance line at 0.5)
  - emits one bootstrap-summary JSON per (model, dataset) for tables in
    the report

Model size is parsed from the model_short field (e.g. "qwen3_1p7b" ->
1.7e9). Unknown shorthands fall back to a categorical x-axis.

CLI:
  python -m src.analysis.plot_scaling_trends \\
      --evaluations_dir outputs/evaluations \\
      --output_dir      outputs/plots \\
      --n_boot          1000
"""

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def parse_model_size(short):
    """qwen3_0p6b -> 0.6e9, qwen3_1p7b -> 1.7e9, qwen3_4b -> 4e9, ..."""
    if not short:
        return None
    s = short.lower()
    m = re.search(r"(\d+)p(\d+)b", s)
    if m:
        whole, frac = m.groups()
        return float(f"{whole}.{frac}") * 1e9
    m = re.search(r"(\d+)b", s)
    if m:
        return float(m.group(1)) * 1e9
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--evaluations_dir", required=True)
    ap.add_argument("--output_dir", required=True)
    ap.add_argument("--n_boot", type=int, default=1000)
    args = ap.parse_args()

    eval_root = Path(args.evaluations_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # find every eval json (one per dataset per model). They live under
    # outputs/evaluations/<model_short>/<dataset>_eval.json
    eval_files = sorted(eval_root.rglob("*_eval.json"))
    if not eval_files:
        raise SystemExit(f"no *_eval.json files under {eval_root}")
    print(f"found {len(eval_files)} eval files")

    # Group by (model, dataset)
    by_model_dataset = {}
    for f in eval_files:
        d = json.load(open(f))
        key = (d.get("model_short") or f.parent.name, d["dataset"])
        by_model_dataset[key] = d

    # Per (model, dataset) bootstrap-summary JSON (already in the eval file
    # but we re-emit a flat one for the report).
    boot_dir = eval_root
    for (model, dataset), d in by_model_dataset.items():
        out = {
            "model": model,
            "dataset": dataset,
            "best_layer": d["best_layer"],
            "accuracy_mean": d["accuracy_mean"],
            "accuracy_ci_lo": d["accuracy_ci_lo"],
            "accuracy_ci_hi": d["accuracy_ci_hi"],
            "auc_mean": d.get("auc_mean"),
            "auc_ci_lo": d.get("auc_ci_lo"),
            "auc_ci_hi": d.get("auc_ci_hi"),
            "margin_mean": d.get("margin_mean"),
            "margin_ci_lo": d.get("margin_ci_lo"),
            "margin_ci_hi": d.get("margin_ci_hi"),
            "n_pairs": d.get("n_test_pairs"),
            "n_boot": d.get("n_boot", args.n_boot),
            "paraphrase_accuracy_mean": d.get("paraphrase_accuracy_mean"),
            "paraphrase_accuracy_ci_lo": d.get("paraphrase_accuracy_ci_lo"),
            "paraphrase_accuracy_ci_hi": d.get("paraphrase_accuracy_ci_hi"),
        }
        boot_path = boot_dir / f"{model}_{dataset}_bootstrap.json"
        with boot_path.open("w") as f:
            json.dump(out, f, indent=2)

    # Layerwise plot per (model, dataset)
    for (model, dataset), d in by_model_dataset.items():
        layers = [r["layer"] for r in d["per_layer"]]
        acc_m = [r["accuracy_mean"] for r in d["per_layer"]]
        lo = [r["accuracy_ci_lo"] for r in d["per_layer"]]
        hi = [r["accuracy_ci_hi"] for r in d["per_layer"]]
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.fill_between(layers, lo, hi, alpha=0.3, label="95% CI")
        ax.plot(layers, acc_m, lw=1.5, label="bootstrap mean")
        ax.axhline(0.5, color="grey", ls="--", lw=0.8, label="chance")
        ax.set_xlabel("layer (transformer block index)")
        ax.set_ylabel("pairwise accuracy")
        ax.set_title(f"{model} | {dataset}")
        ax.set_ylim(0.0, 1.05)
        ax.legend(fontsize=8)
        fig.tight_layout()
        out_p = out_dir / f"layerwise_{model}_{dataset}.png"
        fig.savefig(out_p, dpi=140)
        plt.close(fig)

    # Headline scaling plot: best-layer accuracy vs model size
    by_dataset = defaultdict(list)
    for (model, dataset), d in by_model_dataset.items():
        size = parse_model_size(model)
        by_dataset[dataset].append({
            "model": model,
            "size": size,
            "acc": d["accuracy_mean"],
            "lo": d["accuracy_ci_lo"],
            "hi": d["accuracy_ci_hi"],
        })

    fig, ax = plt.subplots(figsize=(7, 4.5))
    has_size = any(any(r["size"] is not None for r in v) for v in by_dataset.values())
    for dataset, rows in by_dataset.items():
        rows = sorted(rows, key=lambda r: (r["size"] or 0))
        if has_size:
            xs = [r["size"] for r in rows if r["size"] is not None]
            ys = [r["acc"] for r in rows if r["size"] is not None]
            errs_lo = [r["acc"] - r["lo"] for r in rows if r["size"] is not None]
            errs_hi = [r["hi"] - r["acc"] for r in rows if r["size"] is not None]
            ax.errorbar(xs, ys, yerr=[errs_lo, errs_hi], marker="o",
                        capsize=4, lw=1.5, label=dataset)
        else:
            ax.plot([r["model"] for r in rows],
                    [r["acc"] for r in rows], marker="o", label=dataset)
    if has_size:
        ax.set_xscale("log")
        ax.set_xlabel("model size (parameters, log scale)")
    else:
        ax.set_xlabel("model")
    ax.set_ylabel("best-layer pairwise accuracy")
    ax.axhline(0.5, color="grey", ls="--", lw=0.8, label="chance")
    ax.set_ylim(0.0, 1.05)
    ax.set_title("Reading-vector accuracy vs model scale")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    out_p = out_dir / "scaling_best_layer_accuracy.png"
    fig.savefig(out_p, dpi=140)
    plt.close(fig)

    print(f"wrote layerwise plots and {out_p.name} -> {out_dir}")


if __name__ == "__main__":
    main()
