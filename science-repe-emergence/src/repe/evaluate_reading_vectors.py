"""Phase 9 — Evaluate per-layer LAT vectors on test + paraphrase activations.

For every (dataset, layer):
  - score_pos = pos_hidden[i, L, :] @ v[L]
  - score_neg = neg_hidden[i, L, :] @ v[L]
  - pairwise accuracy = mean(score_pos > score_neg)
  - AUC of binary classifier (label 1 for positives, 0 for negatives, score = h @ v)
  - margin    = mean(score_pos - score_neg)

Bootstrap 95% CIs computed by resampling pair indices with replacement
N_boot times. Best layer is the layer with the highest bootstrap-mean
accuracy on the test set; paraphrase accuracy is reported at that same
best layer.

Writes one JSON file per dataset to --output (a directory):
  {model_short}_{dataset}.json
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import roc_auc_score


def per_layer_scores(blob, indices, layer, vec):
    """Return (pos_scores, neg_scores) numpy arrays for the dataset slice."""
    pos = blob["pos_hidden"][indices, layer, :].float().numpy()
    neg = blob["neg_hidden"][indices, layer, :].float().numpy()
    v = vec.numpy() if isinstance(vec, torch.Tensor) else vec
    return pos @ v, neg @ v


def metrics(pos_scores, neg_scores):
    pos_scores = np.asarray(pos_scores)
    neg_scores = np.asarray(neg_scores)
    acc = float(np.mean(pos_scores > neg_scores))
    margin = float(np.mean(pos_scores - neg_scores))
    y = np.concatenate([np.ones_like(pos_scores), np.zeros_like(neg_scores)])
    s = np.concatenate([pos_scores, neg_scores])
    try:
        auc = float(roc_auc_score(y, s))
    except ValueError:
        auc = float("nan")
    return acc, auc, margin


def bootstrap(pos, neg, n_boot, rng):
    n = len(pos)
    accs, aucs, margins = [], [], []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        a, u, m = metrics(pos[idx], neg[idx])
        accs.append(a)
        aucs.append(u)
        margins.append(m)
    def summarize(vals):
        v = np.asarray(vals, dtype=np.float64)
        v = v[~np.isnan(v)]
        if len(v) == 0:
            return float("nan"), float("nan"), float("nan")
        return float(v.mean()), float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))
    return summarize(accs), summarize(aucs), summarize(margins)


def eval_one(blob, dataset, vec_blob, n_boot, rng):
    """Evaluate one dataset's LAT vectors against one activation blob."""
    indices = [i for i, ds in enumerate(blob["datasets"]) if ds == dataset]
    if not indices:
        return None
    vectors = vec_blob["vectors"]      # [n_layers, hidden]
    n_layers = vectors.shape[0]
    per_layer = []
    for L in range(n_layers):
        pos_s, neg_s = per_layer_scores(blob, indices, L, vectors[L])
        acc, auc, margin = metrics(pos_s, neg_s)
        (acc_m, acc_lo, acc_hi), (auc_m, auc_lo, auc_hi), (mg_m, mg_lo, mg_hi) = bootstrap(
            pos_s, neg_s, n_boot, rng
        )
        per_layer.append({
            "layer": L,
            "accuracy": acc,
            "accuracy_mean": acc_m, "accuracy_ci_lo": acc_lo, "accuracy_ci_hi": acc_hi,
            "auc": auc,
            "auc_mean": auc_m, "auc_ci_lo": auc_lo, "auc_ci_hi": auc_hi,
            "margin": margin,
            "margin_mean": mg_m, "margin_ci_lo": mg_lo, "margin_ci_hi": mg_hi,
        })
    return {"dataset": dataset, "n_pairs": len(indices), "per_layer": per_layer}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vectors", required=True,
                    help="directory of *_lat.pt files from Phase 8")
    ap.add_argument("--test", required=True, help="test.pt activations")
    ap.add_argument("--paraphrase", default=None,
                    help="paraphrase_test.pt activations (optional)")
    ap.add_argument("--output", required=True, help="output directory for JSON files")
    ap.add_argument("--n_boot", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    test = torch.load(args.test, map_location="cpu", weights_only=False)
    para = (torch.load(args.paraphrase, map_location="cpu", weights_only=False)
            if args.paraphrase and Path(args.paraphrase).exists() else None)
    print(f"test.pt: {len(test['pair_ids'])} pairs")
    if para is not None:
        print(f"paraphrase.pt: {len(para['pair_ids'])} pairs")

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(args.seed)

    vec_files = sorted(Path(args.vectors).glob("*_lat.pt"))
    if not vec_files:
        raise SystemExit(f"no *_lat.pt files in {args.vectors}")

    for vf in vec_files:
        vec_blob = torch.load(vf, map_location="cpu", weights_only=False)
        dataset = vec_blob["dataset"]
        model_short = (vec_blob.get("model_name") or "model").split("/")[-1]
        print(f"\n[{dataset}]")

        test_eval = eval_one(test, dataset, vec_blob, args.n_boot, rng)
        if test_eval is None:
            print(f"  no test pairs for dataset {dataset}; skipping")
            continue

        # best layer = highest bootstrap-mean accuracy
        best = max(test_eval["per_layer"], key=lambda r: r["accuracy_mean"])
        best_layer = best["layer"]

        result = {
            "model_name": vec_blob.get("model_name"),
            "model_short": model_short,
            "dataset": dataset,
            "n_test_pairs": test_eval["n_pairs"],
            "per_layer": test_eval["per_layer"],
            "best_layer": best_layer,
            "accuracy_mean": best["accuracy_mean"],
            "accuracy_ci_lo": best["accuracy_ci_lo"],
            "accuracy_ci_hi": best["accuracy_ci_hi"],
            "auc_mean": best["auc_mean"],
            "auc_ci_lo": best["auc_ci_lo"],
            "auc_ci_hi": best["auc_ci_hi"],
            "margin_mean": best["margin_mean"],
            "margin_ci_lo": best["margin_ci_lo"],
            "margin_ci_hi": best["margin_ci_hi"],
            "n_boot": args.n_boot,
            "flipped_layers": vec_blob.get("flipped_layers", []),
            "pca_explained_variance": vec_blob.get("pca_explained_variance", []),
        }

        if para is not None:
            para_eval = eval_one(para, dataset, vec_blob, args.n_boot, rng)
            if para_eval is not None and best_layer < len(para_eval["per_layer"]):
                pb = para_eval["per_layer"][best_layer]
                result["n_paraphrase_pairs"] = para_eval["n_pairs"]
                result["paraphrase_accuracy_mean"] = pb["accuracy_mean"]
                result["paraphrase_accuracy_ci_lo"] = pb["accuracy_ci_lo"]
                result["paraphrase_accuracy_ci_hi"] = pb["accuracy_ci_hi"]
                result["paraphrase_auc_mean"] = pb["auc_mean"]
                result["paraphrase_per_layer"] = para_eval["per_layer"]

        out_file = out_dir / f"{dataset}_eval.json"
        with out_file.open("w") as fh:
            json.dump(result, fh, indent=2)
        print(f"  best layer = {best_layer}  "
              f"acc {result['accuracy_mean']:.3f} "
              f"[{result['accuracy_ci_lo']:.3f}, {result['accuracy_ci_hi']:.3f}]  "
              f"AUC {result['auc_mean']:.3f}")
        if "paraphrase_accuracy_mean" in result:
            print(f"  paraphrase acc {result['paraphrase_accuracy_mean']:.3f}")
        print(f"  -> {out_file}")


if __name__ == "__main__":
    main()
