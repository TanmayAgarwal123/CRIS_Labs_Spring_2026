"""Phase 10 — Coefficient sweep over control prompts.

For each LAT vector file under --vectors (one per Source B dataset), and
for each prompt in --prompts (a YAML file), generate one continuation per
coefficient in --coefficients. Steering hooks are installed at the four
middle/late control layers (45/55/65/75%).

Output: one JSONL per vector dataset under --output:
  outputs/generations/<model_short>/<dataset>.jsonl
Each row:
  {
    prompt_id, domain, concept, prompt, vector_dataset, model,
    coefficient, control_layers, generation, decode_config
  }
"""

import argparse
import json
from pathlib import Path

import torch
import yaml
from tqdm.auto import tqdm

from src.repe.control_model import (
    default_control_layers,
    install_control_hooks,
    remove_hooks,
)
from src.repe.model_loader import load_model_and_tokenizer


def parse_coeffs(s):
    """Accept '1,2,3' or '1.0 2.0 3.0' (post-split) values."""
    if isinstance(s, list):
        return [float(x) for x in s]
    parts = [p for p in s.replace(",", " ").split() if p]
    return [float(p) for p in parts]


@torch.no_grad()
def generate_one(model, tokenizer, prompt, max_new_tokens, do_sample,
                 temperature, top_p, repetition_penalty):
    enc = tokenizer(prompt, return_tensors="pt").to(model.device)
    kwargs = dict(
        **enc,
        max_new_tokens=max_new_tokens,
        do_sample=do_sample,
        repetition_penalty=repetition_penalty,
        pad_token_id=tokenizer.pad_token_id,
        use_cache=True,
    )
    if do_sample:
        kwargs["temperature"] = temperature
        kwargs["top_p"] = top_p
    out_ids = model.generate(**kwargs)
    new_tokens = out_ids[0, enc.input_ids.shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--vectors", required=True,
                    help="directory of *_lat.pt from Phase 8")
    ap.add_argument("--prompts", required=True, help="YAML of control prompts")
    ap.add_argument("--coefficients", default="-2.0,-1.0,0.0,1.0,2.0")
    ap.add_argument("--layers", default="middle_late",
                    choices=["middle_late"],
                    help="layer-selection strategy; 'middle_late' = 45/55/65/75%%")
    ap.add_argument("--max_new_tokens", type=int, default=160)
    ap.add_argument("--repetition_penalty", type=float, default=1.1)
    ap.add_argument("--do_sample", action="store_true")
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--top_p", type=float, default=0.9)
    ap.add_argument("--dtype", default="bfloat16")
    ap.add_argument("--output", required=True, help="output directory")
    ap.add_argument("--datasets", nargs="*", default=None,
                    help="optional dataset filter (default: all vector files)")
    args = ap.parse_args()

    with open(args.prompts) as f:
        prompts_cfg = yaml.safe_load(f)
    prompts = prompts_cfg.get("prompts") or prompts_cfg
    print(f"loaded {len(prompts)} prompts")

    coeffs = parse_coeffs(args.coefficients)
    print(f"coefficients: {coeffs}")

    vec_files = sorted(Path(args.vectors).glob("*_lat.pt"))
    if args.datasets:
        vec_files = [v for v in vec_files
                     if any(v.name.startswith(d + "_") for d in args.datasets)]
    if not vec_files:
        raise SystemExit(f"no LAT vector files in {args.vectors}")

    print(f"loading {args.model} (dtype={args.dtype})")
    model, tokenizer = load_model_and_tokenizer(args.model, dtype=args.dtype)
    n_blocks = len(model.model.layers)
    print(f"model has {n_blocks} transformer blocks")

    control_layers = default_control_layers(n_blocks)
    print(f"control layers ({args.layers}): {control_layers}")

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    decode_cfg = {
        "max_new_tokens": args.max_new_tokens,
        "do_sample": args.do_sample,
        "temperature": args.temperature if args.do_sample else None,
        "top_p": args.top_p if args.do_sample else None,
        "repetition_penalty": args.repetition_penalty,
    }

    for vf in vec_files:
        blob = torch.load(vf, map_location="cpu", weights_only=False)
        dataset = blob["dataset"]
        vectors = blob["vectors"].float()
        n_v_layers = vectors.shape[0]
        if n_v_layers != n_blocks:
            print(f"  WARN: vectors have {n_v_layers} layers but model has "
                  f"{n_blocks} blocks; using the first {n_blocks} layers")
        rows = []
        print(f"\n[{dataset}]  prompts={len(prompts)}  coeffs={len(coeffs)}  "
              f"-> {len(prompts) * len(coeffs)} generations")
        for prm in tqdm(prompts, desc="prompts"):
            for c in coeffs:
                handles = install_control_hooks(
                    model, vectors[:n_blocks], control_layers, c
                )
                try:
                    text = generate_one(
                        model, tokenizer, prm["prompt"],
                        args.max_new_tokens, args.do_sample,
                        args.temperature, args.top_p, args.repetition_penalty,
                    )
                finally:
                    remove_hooks(handles)
                rows.append({
                    "prompt_id": prm["id"],
                    "domain": prm.get("domain"),
                    "concept": prm.get("concept"),
                    "prompt": prm["prompt"],
                    "vector_dataset": dataset,
                    "model": args.model,
                    "coefficient": c,
                    "control_layers": control_layers,
                    "generation": text,
                    "decode_config": decode_cfg,
                })
        out_file = out_dir / f"{dataset}.jsonl"
        with out_file.open("w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"  wrote {len(rows)} -> {out_file}")


if __name__ == "__main__":
    main()
