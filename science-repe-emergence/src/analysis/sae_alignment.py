"""Phase 12 — SAE Bridge: cosine alignment between LAT vectors and SAE features.

For each (SAE, LAT dataset) combination, computes the cosine of the LAT
vector against every SAE decoder row, saves the full spectrum (.npy), the
top-k features (.json), a spectrum plot (.png), and a btop128-vs-btop256
"split" comparison.

Downloads SAE artifacts from a HuggingFace repo. Decoder weight names vary
across SAE codebases, so we look for the most common keys ("W_dec",
"decoder.weight", "decoder", "dec"); the script will print what it finds.

CLI:
  python -m src.analysis.sae_alignment \\
      --lat_vectors outputs/vectors/qwen3_1p7b \\
      --sae_repo CRISMechInterp/Qwen3_SAEs \\
      --sae_subfolders qwen3_1p7b_middle_btop128_exp4 qwen3_1p7b_middle_btop256_exp4 \\
      --sae_layer_hint hook_resid_post \\
      --top_k 20 \\
      --output_dir outputs/sae_alignment/qwen3_1p7b
"""

import argparse
import json
import math
import os
from pathlib import Path

import numpy as np
import torch

from huggingface_hub import hf_hub_download, list_repo_files
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Candidate decoder weight keys (in priority order).
DECODER_KEYS = [
    "W_dec", "decoder.weight", "decoder", "dec",
    "W_d", "decoder_weight",
]


def _try_load_weights(local_path):
    """Load a weights file. Supports .safetensors and torch state-dicts."""
    if local_path.endswith(".safetensors"):
        from safetensors.torch import load_file
        return load_file(local_path)
    return torch.load(local_path, map_location="cpu", weights_only=False)


def load_sae_decoder(repo, subfolder, hf_token):
    """Return (decoder_rows[n_features, d_model] (L2-normalized), config_dict).

    Auto-detects decoder orientation by comparing to d_model from config.json
    if present.
    """
    files = list_repo_files(repo, token=hf_token)
    in_sub = [f for f in files if f.startswith(subfolder + "/")]
    if not in_sub:
        raise SystemExit(f"no files under {repo}/{subfolder}")

    # config (optional)
    config = {}
    cfg_files = [f for f in in_sub if f.endswith("config.json")]
    if cfg_files:
        cfg_path = hf_hub_download(repo, cfg_files[0], token=hf_token)
        try:
            config = json.load(open(cfg_path))
        except Exception:
            pass

    # weights
    weight_candidates = [
        f for f in in_sub
        if f.endswith(".safetensors") or f.endswith(".pt") or f.endswith(".bin")
    ]
    if not weight_candidates:
        raise SystemExit(f"no weight files under {repo}/{subfolder}")
    # Prefer something named 'weights' or 'model'; otherwise take the first.
    weight_candidates.sort(key=lambda x: (
        0 if "weights" in x.lower() or "model" in x.lower() else 1, x
    ))
    weights_path = hf_hub_download(repo, weight_candidates[0], token=hf_token)
    state = _try_load_weights(weights_path)

    # Find decoder tensor
    decoder = None
    decoder_key = None
    state_keys = list(state.keys()) if hasattr(state, "keys") else []
    for k in DECODER_KEYS:
        if k in state:
            decoder = state[k]
            decoder_key = k
            break
    if decoder is None:
        # try any key containing 'dec'
        for k in state_keys:
            if "dec" in k.lower():
                decoder = state[k]
                decoder_key = k
                break
    if decoder is None:
        raise SystemExit(
            f"could not find a decoder tensor in {weights_path}; "
            f"keys: {state_keys[:20]}"
        )

    decoder = decoder.float()
    d_model = config.get("d_model") or config.get("hidden_size") \
        or config.get("act_size") or config.get("d_in")

    # Orient as [n_features, d_model]
    if d_model is not None:
        if decoder.shape[1] != d_model and decoder.shape[0] == d_model:
            decoder = decoder.T
    # L2-normalize rows
    norms = decoder.norm(dim=1, keepdim=True).clamp_min(1e-12)
    decoder = decoder / norms

    print(f"  loaded {weight_candidates[0]} (key={decoder_key!r}); "
          f"decoder shape after orientation = {tuple(decoder.shape)}")
    return decoder.numpy(), config


def pick_lat_layer(lat_blob, hint):
    """Pick the layer of the LAT vector to align against the SAE.

    The SAE is trained at a specific transformer layer (e.g. the middle
    layer). We pick the LAT vector at the layer with the highest PCA
    explained variance, OR the middle layer if explained-variance info is
    absent. The user can override via SAE config if needed.
    """
    expl = lat_blob.get("pca_explained_variance")
    if expl:
        # Bias towards middle layers (typical SAE residual stream hook).
        n = len(expl)
        mid = n // 2
        # weight = expl_var minus distance penalty from middle
        scores = [e - 0.001 * abs(i - mid) for i, e in enumerate(expl)]
        return int(np.argmax(scores))
    return lat_blob["vectors"].shape[0] // 2


def random_baseline_threshold(d_model, n_features):
    """Expected number of random unit vectors with |cos| > 0.10 in d_model dims.
    Used as a sanity overlay on the spectrum plot.
    """
    sigma = 1.0 / math.sqrt(d_model)
    # under Gaussian approx: P(|cos|>0.10) ~ 2 * (1 - Phi(0.10/sigma))
    from math import erf, sqrt
    z = 0.10 / sigma
    p = 2.0 * (1.0 - 0.5 * (1.0 + erf(z / sqrt(2.0))))
    return n_features * p


def alignment_spectrum_plot(cos, out_path, title, d_model):
    abs_cos = np.abs(cos)
    sorted_desc = -np.sort(-abs_cos)
    n = len(sorted_desc)
    # random baseline: sigma = 1/sqrt(d_model); plot sigma and 3*sigma lines
    sigma = 1.0 / math.sqrt(d_model)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(sorted_desc, lw=1)
    ax.axhline(sigma, color="grey", ls="--", lw=0.8, label=f"random sigma ~ {sigma:.3f}")
    ax.axhline(3 * sigma, color="red", ls="--", lw=0.8, label=f"3*sigma ~ {3*sigma:.3f}")
    ax.axhline(0.10, color="orange", ls=":", lw=0.8, label="|cos|=0.10")
    ax.set_xlabel("SAE feature index (sorted by |cos|)")
    ax.set_ylabel("|cosine(LAT, decoder_row)|")
    ax.set_title(title)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


def top_features(cos, k):
    abs_cos = np.abs(cos)
    order = np.argsort(-abs_cos)[:k]
    return [
        {
            "rank": int(r),
            "feature_idx": int(idx),
            "cos": float(cos[idx]),
            "abs_cos": float(abs_cos[idx]),
            "sign": int(np.sign(cos[idx])),
        }
        for r, idx in enumerate(order, start=1)
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat_vectors", required=True,
                    help="directory of *_lat.pt files (one model)")
    ap.add_argument("--sae_repo", required=True)
    ap.add_argument("--sae_subfolders", nargs="+", required=True)
    ap.add_argument("--sae_layer_hint", default="hook_resid_post")
    ap.add_argument("--top_k", type=int, default=20)
    ap.add_argument("--output_dir", required=True)
    args = ap.parse_args()

    hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    lat_files = sorted(Path(args.lat_vectors).glob("*_lat.pt"))
    if not lat_files:
        raise SystemExit(f"no LAT vector files in {args.lat_vectors}")

    # Load all SAE decoders up front (per subfolder).
    decoders = {}
    for sub in args.sae_subfolders:
        short = sub.split("_")[-2] if "_" in sub else sub  # e.g. "btop128"
        # robust short-name: pull the "btop128"/"btop256" segment
        short = "btop128" if "btop128" in sub else (
                "btop256" if "btop256" in sub else sub)
        print(f"\nloading SAE {sub} as {short!r}")
        dec, cfg = load_sae_decoder(args.sae_repo, sub, hf_token)
        decoders[short] = {"decoder": dec, "config": cfg, "subfolder": sub}

    # Per-LAT cosines, top features, plot
    all_cos = {}   # {short: {dataset: cos_array}}
    all_top = {}   # {short: {dataset: top_features_list}}
    for short, sae in decoders.items():
        d_model = sae["decoder"].shape[1]
        per_dataset_cos = {}
        per_dataset_top = {}
        sub_out = out_dir / short
        sub_out.mkdir(parents=True, exist_ok=True)
        for lf in lat_files:
            blob = torch.load(lf, map_location="cpu", weights_only=False)
            dataset = blob["dataset"]
            v = blob["vectors"]                       # [n_layers, hidden]
            if v.shape[1] != d_model:
                print(f"  [{dataset}] LAT hidden_dim={v.shape[1]} != SAE d_model={d_model}; skipping")
                continue
            layer = pick_lat_layer(blob, args.sae_layer_hint)
            lat_vec = v[layer].float().numpy()
            lat_vec = lat_vec / (np.linalg.norm(lat_vec) + 1e-12)
            cos = sae["decoder"] @ lat_vec            # [n_features]
            per_dataset_cos[dataset] = cos
            np.save(sub_out / f"{dataset}_cos.npy", cos)
            top = top_features(cos, args.top_k)
            per_dataset_top[dataset] = top
            with (sub_out / f"{dataset}_top_features.json").open("w") as f:
                json.dump({
                    "dataset": dataset,
                    "sae_short": short,
                    "sae_subfolder": sae["subfolder"],
                    "lat_layer": int(layer),
                    "d_model": int(d_model),
                    "n_features": int(sae["decoder"].shape[0]),
                    "top_k": args.top_k,
                    "top": top,
                }, f, indent=2)
            alignment_spectrum_plot(
                cos,
                sub_out / f"{dataset}_spectrum.png",
                title=f"{short} | {dataset} | LAT layer {layer}",
                d_model=d_model,
            )
            n_above = int(np.sum(np.abs(cos) > 0.10))
            n_random_above = random_baseline_threshold(d_model, len(cos))
            print(f"  [{short}|{dataset}] layer={layer} "
                  f"|cos|>0.10: {n_above}  (random baseline ~ {n_random_above:.1f})")
        all_cos[short] = per_dataset_cos
        all_top[short] = per_dataset_top

    # btop128 vs btop256 split analysis
    if "btop128" in all_top and "btop256" in all_top:
        splits = {}
        for ds in set(all_top["btop128"]) & set(all_top["btop256"]):
            top128 = all_top["btop128"][ds]
            top256 = all_top["btop256"][ds]
            splits[ds] = {
                "btop128_top": top128[:args.top_k],
                "btop256_top": top256[:args.top_k],
                "n_btop128_top_k": len(top128),
                "n_btop256_top_k": len(top256),
                "btop256_max_abs_cos": max(t["abs_cos"] for t in top256) if top256 else None,
                "btop128_max_abs_cos": max(t["abs_cos"] for t in top128) if top128 else None,
            }
        with (out_dir / "btop128_vs_btop256_splits.json").open("w") as f:
            json.dump(splits, f, indent=2)
        print(f"\nwrote {out_dir / 'btop128_vs_btop256_splits.json'}")


if __name__ == "__main__":
    main()
