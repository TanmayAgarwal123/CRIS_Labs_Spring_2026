"""Generate Source B contrast-pair datasets via OpenAI.

MVP pass: no textbook concept extraction yet — uses built-in concept seeds.
Supports 4 dataset types (the 3 from AGENTS.md MVP plus math_formal_reasoning,
which is in scope per user override even though no math textbook exists).

CLI:
  python -m src.data.generate_contrast_pairs --dataset mechanistic_explanation_vs_surface --n 55
"""

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


SCIENCE_CONCEPTS = [
    # physics
    {"domain": "physics", "concept": "conservation_of_momentum",
     "anchors": ["momentum", "isolated", "force"]},
    {"domain": "physics", "concept": "newtons_third_law",
     "anchors": ["force", "equal", "opposite"]},
    {"domain": "physics", "concept": "inertia",
     "anchors": ["mass", "motion", "force"]},
    {"domain": "physics", "concept": "conservation_of_energy",
     "anchors": ["energy", "kinetic", "potential"]},
    {"domain": "physics", "concept": "buoyancy",
     "anchors": ["fluid", "displaced", "weight"]},
    {"domain": "physics", "concept": "wave_interference",
     "anchors": ["wave", "amplitude", "phase"]},
    {"domain": "physics", "concept": "gravitational_acceleration",
     "anchors": ["gravity", "mass", "acceleration"]},
    # chemistry
    {"domain": "chemistry", "concept": "le_chatelier_principle",
     "anchors": ["equilibrium", "stress", "shift"]},
    {"domain": "chemistry", "concept": "endothermic_reaction",
     "anchors": ["heat", "absorbed", "products"]},
    {"domain": "chemistry", "concept": "ph_and_acidity",
     "anchors": ["hydrogen", "concentration", "pH"]},
    {"domain": "chemistry", "concept": "catalysts",
     "anchors": ["activation", "energy", "reaction"]},
    {"domain": "chemistry", "concept": "ionic_bond",
     "anchors": ["electron", "transfer", "ion"]},
    {"domain": "chemistry", "concept": "entropy",
     "anchors": ["disorder", "system", "energy"]},
    # biology
    {"domain": "biology", "concept": "natural_selection",
     "anchors": ["variation", "fitness", "population"]},
    {"domain": "biology", "concept": "diffusion",
     "anchors": ["concentration", "molecules", "gradient"]},
    {"domain": "biology", "concept": "osmosis",
     "anchors": ["water", "membrane", "concentration"]},
    {"domain": "biology", "concept": "enzyme_function",
     "anchors": ["substrate", "active site", "reaction"]},
    {"domain": "biology", "concept": "photosynthesis",
     "anchors": ["light", "carbon", "energy"]},
    {"domain": "biology", "concept": "dna_replication",
     "anchors": ["strand", "template", "base"]},
    {"domain": "biology", "concept": "mitosis",
     "anchors": ["chromosome", "cell", "division"]},
]

MATH_CONCEPTS = [
    {"domain": "mathematics", "concept": "division_by_zero",
     "anchors": ["division", "zero", "undefined"]},
    {"domain": "mathematics", "concept": "proof_by_example",
     "anchors": ["proof", "example", "statement"]},
    {"domain": "mathematics", "concept": "limit_of_function",
     "anchors": ["limit", "function", "approach"]},
    {"domain": "mathematics", "concept": "derivative_meaning",
     "anchors": ["derivative", "function", "change"]},
    {"domain": "mathematics", "concept": "chain_rule",
     "anchors": ["derivative", "composition", "function"]},
    {"domain": "mathematics", "concept": "pythagorean_theorem",
     "anchors": ["triangle", "hypotenuse", "right"]},
    {"domain": "mathematics", "concept": "modular_arithmetic",
     "anchors": ["modular", "remainder", "integer"]},
    {"domain": "mathematics", "concept": "function_inverse",
     "anchors": ["inverse", "function", "domain"]},
    {"domain": "mathematics", "concept": "inequality_multiply_negative",
     "anchors": ["inequality", "negative", "sign"]},
    {"domain": "mathematics", "concept": "logarithm_of_product",
     "anchors": ["logarithm", "product", "sum"]},
    {"domain": "mathematics", "concept": "set_complement",
     "anchors": ["set", "element", "complement"]},
    {"domain": "mathematics", "concept": "probability_independence",
     "anchors": ["probability", "event", "independent"]},
    {"domain": "mathematics", "concept": "quadratic_discriminant",
     "anchors": ["quadratic", "discriminant", "root"]},
    {"domain": "mathematics", "concept": "linear_function",
     "anchors": ["linear", "function", "additive"]},
    {"domain": "mathematics", "concept": "counting_combinations",
     "anchors": ["combination", "order", "select"]},
]


# Per-dataset registry. Each entry defines:
#   - reasoning_type: label baked into every output row
#   - concepts: which seed list to cycle through
#   - positive_desc / negative_desc: what positive vs negative should be
#   - examples: optional few-shot pairs spliced into the prompt
DATASETS = {
    "concept_correct_vs_misconception": {
        "reasoning_type": "conceptual",
        "concepts": SCIENCE_CONCEPTS,
        "positive_desc": (
            "a correct, conceptually accurate, mechanistic statement of the concept"
        ),
        "negative_desc": (
            "a plausible misconception about the SAME concept — the kind of "
            "answer a confused student would give. It must NOT be obviously stupid"
        ),
        "examples": [],
    },
    "mechanistic_explanation_vs_surface": {
        "reasoning_type": "mechanistic",
        "concepts": SCIENCE_CONCEPTS,
        "positive_desc": (
            "an explanation that names the underlying causal mechanism — what is "
            "actually happening at the level of forces, particles, molecules, or "
            "processes — and shows the causal chain"
        ),
        "negative_desc": (
            "an explanation that restates the phenomenon in different words, "
            "names the right vocabulary, or gives a circular / keyword-matching "
            "answer that does NOT explain the mechanism. It must sound plausible"
        ),
        "examples": [
            {
                "domain": "chemistry", "concept": "catalysts and activation energy",
                "positive": (
                    "A catalyst increases reaction rate by providing a pathway with "
                    "lower activation energy, so a larger fraction of molecular "
                    "collisions can form products at the same temperature."
                ),
                "negative": (
                    "A catalyst increases reaction rate because it is a substance "
                    "related to the reaction, so the reaction happens faster when "
                    "the catalyst is present."
                ),
            }
        ],
    },
    "counterfactual_reasoning": {
        "reasoning_type": "counterfactual",
        "concepts": SCIENCE_CONCEPTS,
        "positive_desc": (
            "an answer that correctly tracks an intervention. Phrase it in the "
            "shape 'If <variable changes>, then <outcome> because <mechanism>' "
            "where the mechanism is the actual causal reason"
        ),
        "negative_desc": (
            "an answer that applies the original rule unchanged, ignores the "
            "changed variable, or invokes a memorized phrase that does not "
            "account for the intervention. Use the SAME 'If X, then Y because Z' "
            "shape so the surface form parallels the positive"
        ),
        "examples": [
            {
                "domain": "biology", "concept": "osmosis",
                "positive": (
                    "If the solution outside a cell becomes more concentrated, "
                    "water tends to leave the cell because the water potential is "
                    "lower outside than inside."
                ),
                "negative": (
                    "If the solution outside a cell becomes more concentrated, "
                    "water tends to enter the cell because cells always take in "
                    "water when surrounded by more solute."
                ),
            }
        ],
    },
    "math_formal_reasoning": {
        "reasoning_type": "formal",
        "concepts": MATH_CONCEPTS,
        "positive_desc": (
            "a valid mathematical inference or proof step — the conclusion "
            "follows from the premises by a correct rule, with the rule named "
            "or implied"
        ),
        "negative_desc": (
            "a plausible but invalid mathematical inference — for example, "
            "implicit division by zero, claiming a converse that doesn't hold, "
            "applying a property out of its valid scope, generalizing from a few "
            "examples to all integers, or confusing a function with its inverse. "
            "It must look like the kind of step a student might actually write"
        ),
        "examples": [],
    },
}


BANNED = [
    "correct", "incorrect", "wrong", "misconception", "false", "true",
    "actually", "in fact", "no,", "yes,",
]


PROMPT = """You are generating one contrast pair for a representation engineering
experiment that probes a language model's representation of scientific or
mathematical reasoning.

Dataset: {dataset}
Concept: {concept}
Domain: {domain}
Anchor terms (use at least 2 of these in BOTH the positive and negative): {anchors}

Produce ONE pair:
  - positive: {positive_desc} (1-3 sentences).
  - negative: {negative_desc} (1-3 sentences).

Hard constraints (your output will be rejected if any are violated):
  1. positive and negative discuss the same concept.
  2. positive and negative whitespace-token lengths within +-20%.
  3. each side contains at least 2 of the listed anchor terms.
  4. neither contains any of these tokens: "correct", "incorrect", "wrong",
     "misconception", "false", "true", "actually", "in fact", "no,", "yes,".
     Avoid hedging ("it might be that", "some people think").
  5. match register: do NOT make the positive longer or more formal by default.
  6. negative must be plausible — not silly or self-contradicting.
  7. original — do not copy or closely paraphrase textbook sentences.
{examples_block}
Return ONLY valid JSON in this exact shape, with no prose before or after:
{{"positive": "...", "negative": "..."}}
"""


def whitespace_tokens(s):
    return len(s.split())


def validate(positive, negative, anchors):
    reasons = []
    pn, nn = whitespace_tokens(positive), whitespace_tokens(negative)
    if pn < 4 or nn < 4:
        reasons.append("too short")
    elif abs(pn - nn) / max(pn, nn) > 0.20:
        reasons.append(f"length ratio {pn}/{nn}")

    text = (positive + " " + negative).lower()
    for w in BANNED:
        if w in text:
            reasons.append(f"banned token: {w!r}")
            break

    pos_lower, neg_lower = positive.lower(), negative.lower()
    pos_hits = sum(1 for a in anchors if a.lower() in pos_lower)
    neg_hits = sum(1 for a in anchors if a.lower() in neg_lower)
    if pos_hits < 2:
        reasons.append(f"positive has {pos_hits} anchors")
    if neg_hits < 2:
        reasons.append(f"negative has {neg_hits} anchors")

    return reasons


def render_examples(examples):
    if not examples:
        return ""
    lines = ["", "Reference examples (do NOT copy verbatim — match the style):"]
    for ex in examples:
        lines.append("")
        lines.append(f"  domain: {ex['domain']}")
        lines.append(f"  concept: {ex['concept']}")
        lines.append(f"  positive: {ex['positive']}")
        lines.append(f"  negative: {ex['negative']}")
    lines.append("")
    return "\n".join(lines)


def generate_one(client, model, dataset_name, spec, seed):
    prompt = PROMPT.format(
        dataset=dataset_name,
        concept=seed["concept"],
        domain=seed["domain"],
        anchors=", ".join(seed["anchors"]),
        positive_desc=spec["positive_desc"],
        negative_desc=spec["negative_desc"],
        examples_block=render_examples(spec["examples"]),
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        response_format={"type": "json_object"},
    )
    obj = json.loads(resp.choices[0].message.content)
    return obj.get("positive", "").strip(), obj.get("negative", "").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=sorted(DATASETS.keys()))
    ap.add_argument("--n", type=int, default=55)
    ap.add_argument("--model", default="gpt-4.1-mini")
    ap.add_argument("--output_dir", default="data/generated")
    ap.add_argument("--drops_dir", default="outputs/runs")
    ap.add_argument("--max_attempts_factor", type=float, default=3.0)
    ap.add_argument("--overwrite", action="store_true",
                    help="regenerate from scratch even if output JSONL exists")
    ap.add_argument("--append", action="store_true",
                    help="if output exists, top it up to --n by generating "
                         "only the missing pairs (preserves existing rows)")
    args = ap.parse_args()

    spec = DATASETS[args.dataset]
    out_path = Path(args.output_dir) / f"{args.dataset}.jsonl"
    drops_path = Path(args.drops_dir) / f"{args.dataset}_drops.jsonl"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    drops_path.parent.mkdir(parents=True, exist_ok=True)

    pairs, drops = [], []
    seq_per_concept = {c["concept"]: 0 for c in spec["concepts"]}

    # Decide what to do with an existing file.
    if out_path.exists() and not args.overwrite:
        if args.append:
            existing = [json.loads(l) for l in open(out_path)]
            pairs.extend(existing)
            # seed per-concept seq counter from existing pair_ids
            for seed in spec["concepts"]:
                prefix = f"{seed['domain']}_{seed['concept']}_"
                seq_per_concept[seed["concept"]] = sum(
                    1 for p in existing if p["pair_id"].startswith(prefix)
                )
            if len(pairs) >= args.n:
                print(f"{out_path} already has {len(pairs)} pairs >= "
                      f"target {args.n}; nothing to do.")
                return
            print(f"loaded {len(existing)} existing pairs; "
                  f"topping up to {args.n}.")
        else:
            print(f"{out_path} exists; pass --overwrite or --append. skipping.")
            return

    load_dotenv(".env")
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    needed = args.n - len(pairs)
    max_attempts = int(needed * args.max_attempts_factor) + len(spec["concepts"])
    attempt = 0

    while len(pairs) < args.n and attempt < max_attempts:
        seed = spec["concepts"][attempt % len(spec["concepts"])]
        attempt += 1
        try:
            positive, negative = generate_one(
                client, args.model, args.dataset, spec, seed
            )
        except Exception as e:
            drops.append({"concept": seed["concept"], "reason": f"api: {e}"})
            print(f"[{args.dataset}][{attempt:3d}] api error on "
                  f"{seed['concept']}: {e}")
            continue

        reasons = validate(positive, negative, seed["anchors"])
        if reasons:
            drops.append({
                "concept": seed["concept"],
                "reasons": reasons,
                "positive": positive,
                "negative": negative,
            })
            print(f"[{args.dataset}][{attempt:3d}] DROP {seed['concept']}: "
                  f"{reasons}")
            continue

        seq_per_concept[seed["concept"]] += 1
        pid = (f"{seed['domain']}_{seed['concept']}_"
               f"{seq_per_concept[seed['concept']]:03d}")
        pairs.append({
            "pair_id": pid,
            "source": "gpt_generated_contrast",
            "dataset": args.dataset,
            "domain": seed["domain"],
            "textbook": seed["domain"],
            "chapter_or_section": "unknown",
            "concept": seed["concept"],
            "positive": positive,
            "negative": negative,
            "positive_label": 1,
            "negative_label": 0,
            "reasoning_type": spec["reasoning_type"],
            "difficulty": "intro",
            "shared_anchors": seed["anchors"],
            "notes": "",
        })
        print(f"[{args.dataset}][{attempt:3d}] kept {pid} "
              f"({len(pairs)}/{args.n})")

    # `pairs` already includes the existing rows in append mode, so write
    # the full set with "w" either way. Drops are only the NEW failures, so
    # append them to any prior drop log when running in --append mode.
    drops_mode = "a" if args.append and drops_path.exists() else "w"
    with out_path.open("w") as f:
        for p in pairs:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    with drops_path.open(drops_mode) as f:
        for d in drops:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    print()
    print(f"[{args.dataset}] wrote {len(pairs)} pairs -> {out_path}")
    print(f"[{args.dataset}] dropped {len(drops)} -> {drops_path}")


if __name__ == "__main__":
    main()
