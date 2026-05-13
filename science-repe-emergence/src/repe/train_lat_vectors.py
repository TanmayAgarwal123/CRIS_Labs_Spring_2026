"""Phase 8 — Train per-layer LAT vectors via PCA on diff activations.

For each dataset:
  - load combined diffs from train.pt (Source A + Source B, same dataset)
  - per layer: PCA(n_components=1), normalize, sign-flip if val diffs
    on average score negative
  - save one .pt per dataset

Saved blob:
  {
    "model_name":         str,
    "dataset":            str,
    "source_setting":     "combined",
    "vectors":            Tensor[n_layers, hidden_dim],   (fp32)
    "pca_explained_variance": list[float],
    "flipped_layers":     list[int],
    "n_train_pairs":      int,
    "n_val_pairs":        int,
    "metadata":           dict,
  }

CLI:
  python -m src.repe.train_lat_vectors \\
      --activations outputs/activations/qwen3_1p7b/train.pt \\
      --val         outputs/activations/qwen3_1p7b/val.pt \\
      --output      outputs/vectors/qwen3_1p7b \\
      --pca_components 1 \\
      --normalize
"""

import argparse
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
from sklearn.decomposition import PCA
from tqdm.auto import tqdm


def diffs_from(blob, indices=None):
    """diff[i] = pos[i] - neg[i] at every layer, optionally restricted to indices."""
    pos = blob["pos_hidden"].float()
    neg = blob["neg_hidden"].float()
    if indices is not None:
        pos = pos[indices]
        neg = neg[indices]
    return pos - neg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--activations", required=True, help="train.pt")
    ap.add_argument("--val", default=None,
                    help="val.pt; if provided, used to sign-correct each LAT layer")
    ap.add_argument("--output", required=True, help="output directory")
    ap.add_argument("--pca_components", type=int, default=1)
    ap.add_argument("--normalize", action="store_true")
    args = ap.parse_args()

    train = torch.load(args.activations, map_location="cpu", weights_only=False)
    print(f"train.pt: {len(train['pair_ids'])} pairs, "
          f"{train['n_layers']} layers, hidden={train['hidden_dim']}")

    val = None
    if args.val and Path(args.val).exists():
        val = torch.load(args.val, map_location="cpu", weights_only=False)
        print(f"val.pt:   {len(val['pair_ids'])} pairs (for sign-correction)")

    # Group train indices by dataset (source A + B combined)
    train_by_ds = defaultdict(list)
    for i, ds in enumerate(train["datasets"]):
        train_by_ds[ds].append(i)

    val_by_ds = defaultdict(list)
    if val is not None:
        for i, ds in enumerate(val["datasets"]):
            val_by_ds[ds].append(i)

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    n_layers = train["n_layers"]
    hidden_dim = train["hidden_dim"]

    for dataset in sorted(train_by_ds):
        idx = train_by_ds[dataset]
        d_train = diffs_from(train, idx).numpy()    # [n, layers, hidden]
        n = d_train.shape[0]
        print(f"\n[{dataset}] training on {n} diff vectors")

        v_idx = val_by_ds.get(dataset, [])
        d_val = diffs_from(val, v_idx).numpy() if val is not None and v_idx else None

        vectors = np.zeros((n_layers, hidden_dim), dtype=np.float32)
        expl_var = []
        flipped = []

        for L in tqdm(range(n_layers), desc="layers"):
            X = d_train[:, L, :]            # [n, hidden]
            pca = PCA(n_components=args.pca_components)
            pca.fit(X)
            v = pca.components_[0].astype(np.float32)
            if args.normalize:
                norm = np.linalg.norm(v)
                if norm > 0:
                    v = v / norm

            # sign-correct: positive diff (pos - neg) should project +ve on val
            if d_val is not None and len(d_val) > 0:
                proj = d_val[:, L, :] @ v
                if proj.mean() < 0:
                    v = -v
                    flipped.append(L)

            vectors[L] = v
            expl_var.append(float(pca.explained_variance_ratio_[0]))

        blob = {
            "model_name": train.get("model_name"),
            "dataset": dataset,
            "source_setting": "combined",
            "vectors": torch.from_numpy(vectors),
            "pca_explained_variance": expl_var,
            "flipped_layers": flipped,
            "n_train_pairs": int(n),
            "n_val_pairs": int(len(v_idx)),
            "metadata": {
                "normalize": bool(args.normalize),
                "pca_components": int(args.pca_components),
                "hidden_dim": int(hidden_dim),
                "n_layers": int(n_layers),
            },
        }
        out_file = out_dir / f"{dataset}_lat.pt"
        torch.save(blob, out_file)
        print(f"  -> {out_file}  "
              f"(mean expl_var={np.mean(expl_var):.4f}, "
              f"flipped {len(flipped)}/{n_layers} layers)")


if __name__ == "__main__":
    main()
