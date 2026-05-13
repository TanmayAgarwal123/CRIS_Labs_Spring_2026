"""Phase 11 — LLM-judge evaluation of control generations.

Reads every JSONL under --input (one per vector dataset), scores each
generation via gpt-4.1-mini using the AGENTS.md rubric:

    scientific_correctness:  1-5
    mechanistic_depth:       1-5
    misconception_presence:  1-5   (1 = none, 5 = severe)
    clarity:                 1-5
    contains_major_error:    bool
    brief_reason:            str

Writes one consolidated JSON:
  {
    "model": str,                      # judge model
    "n_generations": int,
    "per_generation": [...],
    "by_coefficient": [
       {"coefficient": -2.0, "scientific_correctness": 2.5, ...}, ...
    ],
    "by_dataset": { "<vector_dataset>": {"coefficient": ...}, ... },
    "manual_audit_sample": [...]
  }

CLI:
  python -m src.analysis.evaluate_generations \\
      --input  outputs/generations/qwen3_1p7b \\
      --output outputs/evaluations/qwen3_1p7b/generation_scores.json \\
      --model  gpt-4.1-mini \\
      --sample_for_manual_audit 5
"""

import argparse
import json
import os
import random
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


JUDGE_PROMPT = """You are evaluating a model-generated scientific or mathematical
explanation.

Score the answer using the rubric below.

Prompt:
{prompt}

Generated answer:
{answer}

Rubric:
- scientific_correctness: integer 1-5 (1 = mostly wrong, 5 = fully correct)
- mechanistic_depth:      integer 1-5 (1 = only surface, 5 = clear causal mechanism)
- misconception_presence: integer 1-5 (1 = no misconception, 5 = severe misconception)
- clarity:                integer 1-5 (1 = incoherent, 5 = very clear)
- contains_major_error:   true or false
- brief_reason:           one short sentence

Return ONLY valid JSON, no prose:
{{"scientific_correctness": 1, "mechanistic_depth": 1, "misconception_presence": 1, "clarity": 1, "contains_major_error": false, "brief_reason": "..."}}
"""


def judge_one(client, model, row):
    p = JUDGE_PROMPT.format(prompt=row["prompt"], answer=row["generation"])
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": p}],
        temperature=0,
        max_tokens=200,
        response_format={"type": "json_object"},
    )
    obj = json.loads(resp.choices[0].message.content)
    return obj


def aggregate(rows, by_key):
    buckets = defaultdict(list)
    for r in rows:
        buckets[r[by_key]].append(r)
    summary = []
    for k in sorted(buckets):
        bucket = buckets[k]
        agg = {by_key: k, "n": len(bucket)}
        for field in ("scientific_correctness", "mechanistic_depth",
                      "misconception_presence", "clarity"):
            vals = [r["scores"][field] for r in bucket
                    if isinstance(r.get("scores"), dict) and field in r["scores"]]
            agg[field] = float(sum(vals) / len(vals)) if vals else None
        major_err = [r["scores"].get("contains_major_error")
                     for r in bucket if isinstance(r.get("scores"), dict)]
        agg["frac_major_error"] = (
            float(sum(bool(x) for x in major_err) / len(major_err))
            if major_err else None
        )
        summary.append(agg)
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True,
                    help="directory of generation JSONLs, OR a single JSONL")
    ap.add_argument("--output", required=True)
    ap.add_argument("--model", default="gpt-4.1-mini")
    ap.add_argument("--concurrency", type=int, default=10)
    ap.add_argument("--sample_for_manual_audit", type=int, default=0)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    inp = Path(args.input)
    if inp.is_dir():
        files = sorted(inp.glob("*.jsonl"))
    else:
        files = [inp]
    if not files:
        raise SystemExit(f"no JSONL in {args.input}")

    rows = []
    for f in files:
        for line in open(f):
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    print(f"loaded {len(rows)} generations from {len(files)} file(s)")

    load_dotenv(".env")
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def go(i):
        try:
            scores = judge_one(client, args.model, rows[i])
            return i, scores, None
        except Exception as e:
            return i, None, f"{type(e).__name__}: {e}"

    print(f"judging with {args.model} (concurrency={args.concurrency})")
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = [ex.submit(go, i) for i in range(len(rows))]
        for n, fut in enumerate(as_completed(futures), 1):
            i, scores, err = fut.result()
            if scores is not None:
                rows[i]["scores"] = scores
            else:
                rows[i]["judge_error"] = err
            if n % 25 == 0 or n == len(rows):
                print(f"  judge {n}/{len(rows)}")

    by_coef = aggregate(rows, "coefficient")
    by_ds = {}
    rows_per_ds = defaultdict(list)
    for r in rows:
        rows_per_ds[r.get("vector_dataset", "unknown")].append(r)
    for ds, rs in rows_per_ds.items():
        by_ds[ds] = aggregate(rs, "coefficient")

    audit = []
    if args.sample_for_manual_audit > 0:
        rng = random.Random(args.seed)
        audit = rng.sample(rows, min(args.sample_for_manual_audit, len(rows)))

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "judge_model": args.model,
        "n_generations": len(rows),
        "by_coefficient": by_coef,
        "by_dataset": by_ds,
        "manual_audit_sample": audit,
        "per_generation": rows,
    }
    with out_path.open("w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nwrote {out_path}")
    print("by coefficient:")
    for r in by_coef:
        print(f"  c={r['coefficient']:>5}  correctness={r['scientific_correctness']:.2f}  "
              f"mech_depth={r['mechanistic_depth']:.2f}  "
              f"misconception={r['misconception_presence']:.2f}  "
              f"clarity={r['clarity']:.2f}  frac_err={r['frac_major_error']:.2f}")


if __name__ == "__main__":
    main()
