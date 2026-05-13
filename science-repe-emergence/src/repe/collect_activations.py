"""Phase 7 — Collect last-token hidden states for Source A + Source B.

Reads:
  - --source_b_dataset path/to/*.jsonl     (train/val/test/paraphrase rows)
  - --source_a_pairs   path/to/*.jsonl     (Phase 3 pre-templated vgel pairs)

For each pair runs ONE forward per side (positive, negative) with
output_hidden_states=True under torch.no_grad(), grabs the last-token hidden
state at every transformer block (drops the embedding layer), and saves
both pos and neg activations stacked.

Save format (one .pt per split):
  {
    "model_name":  str,
    "pos_hidden":  Tensor[n_pairs, n_layers, hidden]    (bf16)
    "neg_hidden":  Tensor[n_pairs, n_layers, hidden]    (bf16)
    "pair_ids":    list[str],
    "datasets":    list[str],
    "sources":     list[str],   # "source_a_vgel" or "source_b_gpt"
    "n_layers":    int,
    "hidden_dim":  int,
  }

CLI:
  python -m src.repe.collect_activations \\
      --model Qwen/Qwen3-1.7B-Base \\
      --source_b_dataset data/processed/train.jsonl \\
      --source_a_pairs   data/repe_suffixes/source_a_pairs.jsonl \\
      --output outputs/activations/qwen3_1p7b/train.pt \\
      --batch_size 1 \\
      --dtype bfloat16
"""

import argparse
import json
import os
from pathlib import Path

import torch
from tqdm.auto import tqdm

from src.repe.model_loader import load_model_and_tokenizer
from src.repe.prompt_templates import wrap_neutral
from src.utils.io import load_jsonl


def build_entries(source_b_dataset, source_a_pairs):
    """Return list of (pair_id, dataset, source, positive_prompt, negative_prompt)."""
    entries = []
    if source_b_dataset:
        for row in load_jsonl(source_b_dataset):
            entries.append((
                row["pair_id"],
                row["dataset"],
                "source_b_gpt",
                wrap_neutral(row["positive"]),
                wrap_neutral(row["negative"]),
            ))
    if source_a_pairs:
        for row in load_jsonl(source_a_pairs):
            entries.append((
                row["pair_id"],
                row["dataset"],
                "source_a_vgel",
                row["positive_prompt"],
                row["negative_prompt"],
            ))
    return entries


@torch.no_grad()
def forward_last_token(model, tokenizer, prompts, max_length, device):
    """Run a single batched forward pass, return last-token hidden states per
    transformer block (excluding the embedding layer).

    Returns: Tensor[batch, n_blocks, hidden] in the model's dtype.
    """
    enc = tokenizer(
        prompts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=max_length,
    ).to(device)
    out = model(**enc, output_hidden_states=True, use_cache=False)
    # outputs.hidden_states: tuple of length n_blocks+1
    #   index 0  = embedding layer output
    #   index i  = post-transformer-block-(i-1) hidden states (for i >= 1)
    # We use indices [1:] so vectors[i] is the post-block-i hidden state,
    # matching the hook semantics in control_model.py.
    block_states = out.hidden_states[1:]
    # Left-padded so the real final token is at position -1 for every row.
    # Shape per layer: [batch, seq, hidden] -> take [-1] -> [batch, hidden]
    stacked = torch.stack(
        [h[:, -1, :] for h in block_states], dim=1
    )  # [batch, n_blocks, hidden]
    return stacked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--source_b_dataset", default=None)
    ap.add_argument("--source_a_pairs", default=None)
    ap.add_argument("--output", required=True)
    ap.add_argument("--batch_size", type=int, default=1)
    ap.add_argument("--dtype", default="bfloat16")
    ap.add_argument("--max_length", type=int, default=512)
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    out = Path(args.output)
    if out.exists() and not args.overwrite:
        print(f"{out} exists; pass --overwrite to regenerate. skipping.")
        return
    out.parent.mkdir(parents=True, exist_ok=True)

    entries = build_entries(args.source_b_dataset, args.source_a_pairs)
    if not entries:
        raise SystemExit("no entries — pass --source_b_dataset or --source_a_pairs")
    print(f"loaded {len(entries)} entries "
          f"(source_b={sum(1 for e in entries if e[2]=='source_b_gpt')}, "
          f"source_a={sum(1 for e in entries if e[2]=='source_a_vgel')})")

    print(f"loading {args.model} (dtype={args.dtype})")
    model, tokenizer = load_model_and_tokenizer(args.model, dtype=args.dtype)
    device = next(model.parameters()).device

    pair_ids, datasets, sources = [], [], []
    pos_chunks, neg_chunks = [], []

    bs = max(1, args.batch_size)
    for i in tqdm(range(0, len(entries), bs), desc="forward"):
        batch = entries[i:i + bs]
        pos_prompts = [b[3] for b in batch]
        neg_prompts = [b[4] for b in batch]

        pos_h = forward_last_token(
            model, tokenizer, pos_prompts, args.max_length, device
        ).to(torch.bfloat16).cpu()
        neg_h = forward_last_token(
            model, tokenizer, neg_prompts, args.max_length, device
        ).to(torch.bfloat16).cpu()

        pos_chunks.append(pos_h)
        neg_chunks.append(neg_h)
        for b in batch:
            pair_ids.append(b[0])
            datasets.append(b[1])
            sources.append(b[2])

    pos_hidden = torch.cat(pos_chunks, dim=0)
    neg_hidden = torch.cat(neg_chunks, dim=0)
    n_layers = pos_hidden.shape[1]
    hidden_dim = pos_hidden.shape[2]

    blob = {
        "model_name": args.model,
        "pos_hidden": pos_hidden,
        "neg_hidden": neg_hidden,
        "pair_ids": pair_ids,
        "datasets": datasets,
        "sources": sources,
        "n_layers": n_layers,
        "hidden_dim": hidden_dim,
    }
    torch.save(blob, out)
    size_mb = out.stat().st_size / 1e6
    print(f"\nwrote {len(pair_ids)} pairs x {n_layers} layers x {hidden_dim} dim "
          f"-> {out} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
