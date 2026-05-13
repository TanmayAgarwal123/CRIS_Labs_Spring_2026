"""Phase 3 — Build Source A vgel-style truncation pairs.

Reads the suffix bank and writes one JSONL row per
(suffix x truncation_level x dataset_type). Loads the Qwen3-1.7B-Base and
Qwen3-4B-Base tokenizers, asserts they are identical, and uses a single
tokenizer for all truncation. (No model weights are downloaded.)

Verifies suffix_identical by asserting the truncated suffix is the suffix
of both positive_prompt and negative_prompt.

CLI:
  python -m src.data.generate_source_a_pairs \\
      --input data/repe_suffixes/science_suffix_bank.jsonl \\
      --output data/repe_suffixes/source_a_pairs.jsonl \\
      --truncation_levels 8
"""

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from transformers import AutoTokenizer


TEMPLATES = {
    "science_persona":
        "Consider the following scientific text, interpreted by someone "
        "with {persona}.\n\n{suffix}",
    "mechanistic_persona":
        "The following scientific text is being interpreted by someone "
        "with {persona}.\n\n{suffix}",
}

PERSONA_LABELS = {
    "concept_correct_vs_misconception": {
        "template": "science_persona",
        "positive": "a precise and accurate understanding of this scientific concept",
        "negative": "a common misconception about this scientific concept",
    },
    "mechanistic_explanation_vs_surface": {
        "template": "mechanistic_persona",
        "positive": "a deep understanding of the underlying causal mechanism",
        "negative": "a shallow, surface-level pattern-matching understanding",
    },
    "counterfactual_reasoning": {
        "template": "mechanistic_persona",
        "positive": "careful reasoning about how changing one variable affects the system",
        "negative": "incorrectly applying a memorized rule without adjusting for the changed condition",
    },
}


def load_qwen_tokenizer():
    """Load Qwen3-1.7B + 4B tokenizers and verify they match."""
    print("loading Qwen3-1.7B-Base tokenizer...")
    tok_1p7b = AutoTokenizer.from_pretrained("Qwen/Qwen3-1.7B-Base")
    print("loading Qwen3-4B-Base tokenizer...")
    tok_4b = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B-Base")

    assert tok_1p7b.vocab_size == tok_4b.vocab_size, (
        f"Tokenizers differ: 1.7B vocab={tok_1p7b.vocab_size}, "
        f"4B vocab={tok_4b.vocab_size}. Generate separate pair files per model."
    )
    # deeper check: token IDs must match for a few representative strings
    for probe in [
        "The chain rule states that the derivative of a composition equals "
        "the derivative of the outer evaluated at the inner times the "
        "derivative of the inner.",
        "When two carts collide on a frictionless track, the forces they "
        "exert on each other are equal in magnitude and opposite in direction.",
        "In an isolated system, the total momentum remains constant.",
    ]:
        a = tok_1p7b(probe, add_special_tokens=False).input_ids
        b = tok_4b(probe, add_special_tokens=False).input_ids
        assert a == b, "tokenizer probe mismatch"

    print(f"tokenizer vocab size: {tok_1p7b.vocab_size} "
          "— confirmed identical for 1.7B and 4B")
    return tok_1p7b


def truncation_lengths(max_len, n_levels):
    """n_levels evenly-spaced lengths from 20% to 95% of max_len."""
    if n_levels < 2:
        return [max(1, int(max_len * 0.5))]
    fracs = [0.20 + (0.95 - 0.20) * i / (n_levels - 1) for i in range(n_levels)]
    lengths = [max(1, int(max_len * f)) for f in fracs]
    return sorted(set(lengths))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input",
        default="data/repe_suffixes/science_suffix_bank.jsonl",
    )
    ap.add_argument(
        "--output",
        default="data/repe_suffixes/source_a_pairs.jsonl",
    )
    ap.add_argument("--truncation_levels", type=int, default=8)
    ap.add_argument("--min_tokens", type=int, default=10,
                    help="skip suffix if it has fewer than this many tokens")
    ap.add_argument("--drop_last_n", type=int, default=5)
    args = ap.parse_args()

    load_dotenv(".env")  # picks up HF_TOKEN if present
    if os.environ.get("HF_TOKEN"):
        os.environ.setdefault("HUGGING_FACE_HUB_TOKEN", os.environ["HF_TOKEN"])

    tokenizer = load_qwen_tokenizer()

    suffixes = [json.loads(l) for l in open(args.input)]
    print(f"loaded {len(suffixes)} suffixes")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    n_pairs = 0
    by_dataset = {k: 0 for k in PERSONA_LABELS}
    by_domain = {}
    skipped_short = 0

    with out.open("w") as fh:
        for s in suffixes:
            tokens = tokenizer.tokenize(s["text"])
            if len(tokens) <= args.min_tokens:
                skipped_short += 1
                continue
            max_len = len(tokens) - args.drop_last_n
            if max_len < 1:
                skipped_short += 1
                continue
            lengths = truncation_lengths(max_len, args.truncation_levels)

            for length in lengths:
                truncated = tokenizer.convert_tokens_to_string(tokens[:length])
                # token-list -> string round-trip can leave a leading space
                # depending on the tokenizer; templates end with the suffix
                # verbatim, so we keep `truncated` as-is for the suffix
                # equality check.
                trunc_tok_count = length

                for dataset_name, spec in PERSONA_LABELS.items():
                    template = TEMPLATES[spec["template"]]
                    pos_prompt = template.format(
                        persona=spec["positive"], suffix=truncated
                    )
                    neg_prompt = template.format(
                        persona=spec["negative"], suffix=truncated
                    )
                    # invariant: suffix appears verbatim at the END of both
                    if not (pos_prompt.endswith(truncated)
                            and neg_prompt.endswith(truncated)):
                        raise RuntimeError(
                            f"suffix not at end of prompt for "
                            f"suffix_id={s['suffix_id']} length={length}"
                        )

                    entry = {
                        "pair_id": (
                            f"source_a_{s['suffix_id']}_{dataset_name}_"
                            f"trunc{length:03d}"
                        ),
                        "source": "vgel_textbook_suffix",
                        "dataset": dataset_name,
                        "domain": s["domain"],
                        "suffix_id": s["suffix_id"],
                        "suffix": truncated,
                        "suffix_identical": True,
                        "positive_persona": spec["positive"],
                        "negative_persona": spec["negative"],
                        "positive_prompt": pos_prompt,
                        "negative_prompt": neg_prompt,
                        "approx_token_count": trunc_tok_count,
                    }
                    fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
                    n_pairs += 1
                    by_dataset[dataset_name] += 1
                    by_domain[s["domain"]] = by_domain.get(s["domain"], 0) + 1

    print()
    print(f"wrote {n_pairs} pairs -> {out}")
    print(f"skipped {skipped_short} suffixes (too short)")
    print("by dataset:")
    for k, v in by_dataset.items():
        print(f"  {k}: {v}")
    print("by domain:")
    for k, v in sorted(by_domain.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
