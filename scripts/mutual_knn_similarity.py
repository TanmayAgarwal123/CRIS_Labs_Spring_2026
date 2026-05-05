#!/usr/bin/env python3
"""
Compute mutual k-nearest-neighbor representational similarity between two language models.

Definition (Platonic-style mutual kNN):
For each datapoint i, let N_a(i) and N_b(i) be its k nearest neighbors in models A and B.
The score is mean_i |N_a(i) ∩ N_b(i)| / k.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Sequence, Tuple

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mutual kNN similarity for two language model representation spaces."
    )
    parser.add_argument(
        "--corpus-path",
        type=Path,
        required=True,
        help="Path to a UTF-8 text corpus.",
    )
    parser.add_argument(
        "--model-a",
        type=str,
        required=True,
        help="HF model id/path for model A.",
    )
    parser.add_argument(
        "--model-b",
        type=str,
        required=True,
        help="HF model id/path for model B.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=100,
        help="Chunk size in tokens for datapoints.",
    )
    parser.add_argument(
        "--chunk-stride",
        type=int,
        default=None,
        help="Stride in tokens between chunk starts. Defaults to chunk-size (non-overlapping).",
    )
    parser.add_argument(
        "--chunk-tokenizer",
        type=str,
        default=None,
        help="Tokenizer used for corpus chunking. Defaults to model A tokenizer.",
    )
    parser.add_argument(
        "--max-chunks",
        type=int,
        default=512,
        help="Maximum number of chunks to evaluate.",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=10,
        help="Neighborhood size.",
    )
    parser.add_argument(
        "--layer-a",
        type=int,
        default=-1,
        help="Layer index for model A hidden states (Python indexing; -1 is final layer).",
    )
    parser.add_argument(
        "--layer-b",
        type=int,
        default=-1,
        help="Layer index for model B hidden states (Python indexing; -1 is final layer).",
    )
    parser.add_argument(
        "--pooling",
        choices=["mean", "last"],
        default="mean",
        help="Token pooling strategy for per-chunk embeddings.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=16,
        help="Batch size for model forward passes.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        help="Device: auto, cpu, cuda, cuda:0, ...",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="Optional path to save a JSON results file.",
    )
    return parser.parse_args()


def pick_device(device_arg: str) -> torch.device:
    if device_arg == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(device_arg)


def read_corpus(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Corpus file not found: {path}")
    return path.read_text(encoding="utf-8")


def build_text_chunks(
    corpus_text: str,
    tokenizer_name: str,
    chunk_size: int,
    chunk_stride: int | None,
    max_chunks: int | None,
) -> List[str]:
    if chunk_size < 2:
        raise ValueError("chunk_size must be at least 2.")
    stride = chunk_size if chunk_stride is None else chunk_stride
    if stride <= 0:
        raise ValueError("chunk_stride must be positive.")

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, use_fast=True)
    ids = tokenizer(corpus_text, add_special_tokens=False)["input_ids"]
    if len(ids) < chunk_size:
        raise ValueError(
            f"Corpus too short after tokenization ({len(ids)} tokens) for chunk_size={chunk_size}."
        )

    chunks: List[str] = []
    for start in range(0, len(ids) - chunk_size + 1, stride):
        slice_ids = ids[start : start + chunk_size]
        text = tokenizer.decode(
            slice_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )
        chunks.append(text)
        if max_chunks is not None and len(chunks) >= max_chunks:
            break
    return chunks


def _prepare_tokenizer_for_padding(tokenizer: AutoTokenizer) -> AutoTokenizer:
    if tokenizer.pad_token is None:
        if tokenizer.eos_token is not None:
            tokenizer.pad_token = tokenizer.eos_token
        else:
            tokenizer.add_special_tokens({"pad_token": "[PAD]"})
    return tokenizer


def _pool_hidden(
    hidden: torch.Tensor,
    attention_mask: torch.Tensor,
    pooling: str,
) -> torch.Tensor:
    mask = attention_mask.to(hidden.dtype)
    if pooling == "mean":
        denom = mask.sum(dim=1, keepdim=True).clamp_min(1.0)
        return (hidden * mask.unsqueeze(-1)).sum(dim=1) / denom
    if pooling == "last":
        lengths = attention_mask.sum(dim=1).clamp_min(1) - 1
        batch_ix = torch.arange(hidden.size(0), device=hidden.device)
        return hidden[batch_ix, lengths]
    raise ValueError(f"Unsupported pooling: {pooling}")


@torch.no_grad()
def embed_texts(
    texts: Sequence[str],
    model_name: str,
    layer_index: int,
    pooling: str,
    batch_size: int,
    device: torch.device,
) -> np.ndarray:
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    tokenizer = _prepare_tokenizer_for_padding(tokenizer)
    model = AutoModel.from_pretrained(model_name)
    model.eval()
    model.to(device)

    outputs_all: List[np.ndarray] = []
    for i in range(0, len(texts), batch_size):
        batch = list(texts[i : i + batch_size])
        encoded = tokenizer(
            batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )
        encoded = {k: v.to(device) for k, v in encoded.items()}
        out = model(**encoded, output_hidden_states=True, return_dict=True)
        hidden_states = out.hidden_states
        if hidden_states is None:
            raise RuntimeError(f"Model {model_name} did not return hidden_states.")
        if not (-len(hidden_states) <= layer_index < len(hidden_states)):
            raise IndexError(
                f"layer index {layer_index} out of range for {model_name} with {len(hidden_states)} hidden-state tensors."
            )
        hidden = hidden_states[layer_index]
        pooled = _pool_hidden(hidden, encoded["attention_mask"], pooling)
        outputs_all.append(pooled.detach().cpu().to(torch.float32).numpy())

    return np.concatenate(outputs_all, axis=0)


def l2_normalize(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    norms = np.maximum(norms, eps)
    return x / norms


def knn_indices(embeddings: np.ndarray, k: int) -> np.ndarray:
    n = embeddings.shape[0]
    if n < 2:
        raise ValueError("Need at least 2 datapoints to compute nearest neighbors.")
    if k < 1 or k >= n:
        raise ValueError(f"k must satisfy 1 <= k < n_datapoints. Got k={k}, n={n}.")

    x = l2_normalize(embeddings)
    sim = x @ x.T
    np.fill_diagonal(sim, -np.inf)

    idx = np.argpartition(sim, kth=sim.shape[1] - k, axis=1)[:, -k:]
    row_ids = np.arange(n)[:, None]
    idx_vals = sim[row_ids, idx]
    order = np.argsort(-idx_vals, axis=1)
    idx_sorted = idx[row_ids, order]
    return idx_sorted


def mutual_knn_score(neighbors_a: np.ndarray, neighbors_b: np.ndarray) -> Tuple[float, np.ndarray]:
    if neighbors_a.shape != neighbors_b.shape:
        raise ValueError(
            f"Neighbor shapes must match, got {neighbors_a.shape} vs {neighbors_b.shape}."
        )
    n, k = neighbors_a.shape
    overlaps = np.empty(n, dtype=np.float32)
    for i in range(n):
        set_a = set(neighbors_a[i].tolist())
        set_b = set(neighbors_b[i].tolist())
        overlaps[i] = len(set_a.intersection(set_b)) / float(k)
    return float(overlaps.mean()), overlaps


def main() -> None:
    args = parse_args()
    device = pick_device(args.device)

    chunk_tokenizer = args.chunk_tokenizer or args.model_a
    corpus_text = read_corpus(args.corpus_path)
    chunks = build_text_chunks(
        corpus_text=corpus_text,
        tokenizer_name=chunk_tokenizer,
        chunk_size=args.chunk_size,
        chunk_stride=args.chunk_stride,
        max_chunks=args.max_chunks,
    )

    if len(chunks) <= args.k:
        raise ValueError(
            f"Need more chunks than k. Got {len(chunks)} chunks with k={args.k}. "
            "Increase corpus size or reduce k."
        )

    emb_a = embed_texts(
        texts=chunks,
        model_name=args.model_a,
        layer_index=args.layer_a,
        pooling=args.pooling,
        batch_size=args.batch_size,
        device=device,
    )
    emb_b = embed_texts(
        texts=chunks,
        model_name=args.model_b,
        layer_index=args.layer_b,
        pooling=args.pooling,
        batch_size=args.batch_size,
        device=device,
    )

    neigh_a = knn_indices(emb_a, args.k)
    neigh_b = knn_indices(emb_b, args.k)
    score, per_point_overlap = mutual_knn_score(neigh_a, neigh_b)

    results = {
        "metric": "mutual_knn_overlap",
        "definition": "mean_i |N_a(i) ∩ N_b(i)| / k",
        "model_a": args.model_a,
        "model_b": args.model_b,
        "layer_a": args.layer_a,
        "layer_b": args.layer_b,
        "pooling": args.pooling,
        "k": args.k,
        "n_chunks": len(chunks),
        "chunk_size_tokens": args.chunk_size,
        "chunk_stride_tokens": args.chunk_stride if args.chunk_stride is not None else args.chunk_size,
        "chunk_tokenizer": chunk_tokenizer,
        "device": str(device),
        "score": score,
        "per_point_overlap_mean": float(per_point_overlap.mean()),
        "per_point_overlap_std": float(per_point_overlap.std(ddof=0)),
    }

    print(json.dumps(results, indent=2))
    if args.output_json is not None:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote results JSON: {args.output_json}")


if __name__ == "__main__":
    main()
