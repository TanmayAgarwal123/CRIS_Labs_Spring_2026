"""
Automated SAE feature labeling using an OpenAI-compatible LLM.

For each feature in a feature_summaries JSONL, sends the top activating
examples (token + context) to an LLM and asks for a short interpretive label.

Supports resuming interrupted runs — already-labeled features are skipped.

Usage:
    python llm_feature_labeler.py \
        --feature_summaries path/to/feature_summaries.jsonl \
        --output path/to/feature_labels.jsonl \
        --model gpt-4o-mini \
        --top_k_examples 10 \
        --min_examples 5 \
        --max_features 3464  # set to limit for testing
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from openai import OpenAI

# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are an expert in mechanistic interpretability of language models.
You are analyzing features learned by a Sparse Autoencoder (SAE) trained on
a science textbook corpus. Each feature activates strongly on specific tokens
in context.

For each feature, you will be shown its top activating examples. Each example
shows the token that triggered the activation (in [brackets]) and the surrounding
context.

Your task is to classify each feature using ONLY evidence visible in the examples.
Do not rely on intuition — base every field on what you can directly observe.

Respond ONLY with a JSON object in this exact format:
{
  "label": "<short label, 2-6 words>",
  "description": "<one sentence: what token/context pattern triggers this feature>",
  "category": "<see categories below>",
  "monosemantic": <true or false>,
  "interpretability_score": <integer 1-5>,
  "knowledge_domain": "<see domains below>",
  "abstraction_level": "<surface | lexical | conceptual>"
}

--- CATEGORY ---
Look at the bracketed tokens across all examples. Pick the best match:
- specific_token: the same single common word appears in ≥80% of examples (e.g. "of", "the")
- morpheme: different words but they share a common suffix/prefix/stem (e.g. "-tion", "un-")
- syntax: different tokens but they all play the same grammatical role (e.g. always the verb, always a clause opener)
- domain_term: tokens are content words from a specific scientific domain
- positional: activation correlates with token position (e.g. always near position 0, or always at end)
- numeric: tokens are digits, decimals, or units of measurement
- punctuation: tokens are punctuation or whitespace characters
- polysemantic: no single pattern unifies the examples
- unclear: you genuinely cannot determine a pattern from the given examples

--- MONOSEMANTIC ---
Set to true ONLY if a single pattern explains ≥80% of the examples.
Set to false if two or more distinct patterns are needed to explain the examples.

--- INTERPRETABILITY SCORE (1-5) ---
Base this on how consistently the examples follow a single identifiable rule:
- 5: Every example fits one clear rule. Zero ambiguity.
- 4: ~80-90% of examples fit one rule; 1-2 outliers.
- 3: A pattern exists but ~20-30% of examples don't clearly fit it.
- 2: A vague family resemblance, but you cannot state the rule precisely.
- 1: No discernible rule. Examples appear random or contradictory.

--- KNOWLEDGE DOMAIN ---
Look at the content of the contexts (not just the triggering token). Pick the most specific match:
- chemistry: chemical reactions, elements, compounds, molecular structure
- biology: organisms, cells, anatomy, ecology, genetics, physiology
- physics: forces, energy, motion, waves, electricity, thermodynamics
- mathematics: numbers, proofs, equations, geometry, algebra
- general_science: cross-domain scientific language (e.g. "experiment", "hypothesis", units)
- syntax: grammatical/structural words with no domain content (connectives, articles, auxiliaries)
- morphology: word-part patterns with no domain content
- discourse: text structure (headings, citations, numbered lists, section markers)
- other: a clear pattern outside the above domains
- unclear: contexts are too mixed or sparse to determine

--- ABSTRACTION LEVEL ---
- surface: the pattern is a specific character, punctuation mark, or high-frequency function word — no semantic content needed to identify it
- lexical: the pattern requires recognizing a specific word, morpheme, or named token — word-level knowledge
- conceptual: the pattern requires understanding a scientific concept or semantic relationship — goes beyond individual tokens
"""


def format_examples(feature: dict, top_k: int) -> str:
    examples = feature.get("top_examples", [])[:top_k]
    if not examples:
        return "(no examples available)"

    lines = []
    for i, ex in enumerate(examples, 1):
        token = ex.get("token", "?")
        activation = ex.get("activation", 0.0)
        context = ex.get("context", "").strip()

        # Highlight the token in context if it appears
        if token in context:
            highlighted = context.replace(token, f"[{token}]", 1)
        else:
            highlighted = f"[{token}] ... {context}"

        lines.append(f"  {i}. activation={activation:.3f}  \"{highlighted}\"")

    return "\n".join(lines)


def build_user_message(feature: dict, top_k: int) -> str:
    fid = feature["feature"]
    freq = feature.get("activation_frequency", "?")
    mean_act = feature.get("mean_activation", "?")
    n_ex = len(feature.get("top_examples", []))

    header = (
        f"Feature ID: {fid}\n"
        f"Activation frequency: {freq}  Mean activation: {mean_act:.4f}\n"
        f"Number of stored examples: {n_ex}\n\n"
        f"Top {min(top_k, n_ex)} activating examples:\n"
    )
    return header + format_examples(feature, top_k)


# ---------------------------------------------------------------------------
# OpenAI call with retry
# ---------------------------------------------------------------------------

def call_llm(client: OpenAI, model: str, user_msg: str,
             max_retries: int = 5) -> dict:
    """Call the LLM and parse JSON response. Retries on rate-limit errors."""
    delay = 2.0
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.0,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            err = str(e)
            if "rate_limit" in err.lower() or "429" in err:
                print(f"  Rate limit hit, waiting {delay:.0f}s...", flush=True)
                time.sleep(delay)
                delay = min(delay * 2, 60)
            else:
                print(f"  API error (attempt {attempt+1}/{max_retries}): {e}", flush=True)
                if attempt == max_retries - 1:
                    raise
                time.sleep(delay)
    raise RuntimeError("Max retries exceeded")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_existing_labels(output_path: Path) -> set[int]:
    """Return set of feature IDs already written to output file."""
    done = set()
    if output_path.exists():
        with open(output_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        obj = json.loads(line)
                        done.add(obj["feature"])
                    except Exception:
                        pass
    return done


def main():
    parser = argparse.ArgumentParser(description="Label SAE features with an LLM")
    parser.add_argument(
        "--feature_summaries", required=True,
        help="Path to feature_summaries_<timestamp>.jsonl"
    )
    parser.add_argument(
        "--output", required=True,
        help="Path for output JSONL (labels are appended, enabling resume)"
    )
    parser.add_argument(
        "--model", default="gpt-4o-mini",
        help="OpenAI model to use (default: gpt-4o-mini)"
    )
    parser.add_argument(
        "--top_k_examples", type=int, default=10,
        help="Number of top examples to show per feature (default: 10)"
    )
    parser.add_argument(
        "--min_examples", type=int, default=5,
        help="Skip features with fewer than this many examples (default: 5)"
    )
    parser.add_argument(
        "--max_features", type=int, default=None,
        help="Stop after labeling this many features (useful for testing)"
    )
    parser.add_argument(
        "--requests_per_minute", type=int, default=500,
        help="Rate limit cap (default: 500 RPM)"
    )
    parser.add_argument(
        "--api_key_env", default="OPENAI_API_KEY",
        help="Env var containing the OpenAI API key (default: OPENAI_API_KEY)"
    )
    parser.add_argument(
        "--base_url", default=None,
        help="Optional custom base URL for OpenAI-compatible APIs"
    )
    args = parser.parse_args()

    # --- setup ---
    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        print(f"ERROR: environment variable {args.api_key_env} is not set.", file=sys.stderr)
        sys.exit(1)

    client_kwargs = {"api_key": api_key}
    if args.base_url:
        client_kwargs["base_url"] = args.base_url
    client = OpenAI(**client_kwargs)

    feature_path = Path(args.feature_summaries)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    min_interval = 60.0 / args.requests_per_minute  # seconds between requests

    # --- load features ---
    print(f"Loading features from {feature_path}", flush=True)
    features = []
    with open(feature_path) as f:
        for line in f:
            line = line.strip()
            if line:
                features.append(json.loads(line))
    print(f"Loaded {len(features)} features", flush=True)

    # --- resume support ---
    already_done = load_existing_labels(output_path)
    if already_done:
        print(f"Resuming: {len(already_done)} features already labeled, skipping them", flush=True)

    # --- filter ---
    to_process = [
        f for f in features
        if f["feature"] not in already_done
        and len(f.get("top_examples", [])) >= args.min_examples
    ]
    skipped_low_ex = len(features) - len(already_done) - len(to_process)
    print(
        f"Features to label: {len(to_process)}  "
        f"(skipped {skipped_low_ex} with <{args.min_examples} examples)",
        flush=True
    )

    if args.max_features is not None:
        to_process = to_process[:args.max_features]
        print(f"Capped at {args.max_features} features for this run", flush=True)

    # --- label ---
    labeled = 0
    errors = 0
    t_start = time.time()

    with open(output_path, "a") as out_f:
        for i, feature in enumerate(to_process):
            fid = feature["feature"]
            t_req = time.time()

            try:
                user_msg = build_user_message(feature, args.top_k_examples)
                result = call_llm(client, args.model, user_msg)
                record = {
                    "feature": fid,
                    "activation_frequency": feature.get("activation_frequency"),
                    "mean_activation": feature.get("mean_activation"),
                    "label": result.get("label", ""),
                    "description": result.get("description", ""),
                    "category": result.get("category", "unclear"),
                    "monosemantic": result.get("monosemantic", None),
                    "interpretability_score": result.get("interpretability_score", None),
                    "knowledge_domain": result.get("knowledge_domain", "unclear"),
                    "abstraction_level": result.get("abstraction_level", None),
                }
                out_f.write(json.dumps(record) + "\n")
                out_f.flush()
                labeled += 1

                elapsed = time.time() - t_start
                rate = labeled / elapsed * 60
                score = result.get("interpretability_score", "?")
                domain = result.get("knowledge_domain", "?")
                print(
                    f"[{i+1}/{len(to_process)}] feature={fid:5d}  "
                    f"score={score}  domain={domain:15s}  "
                    f"label=\"{result.get('label', '')}\"  "
                    f"({rate:.0f} feat/min)",
                    flush=True
                )
            except Exception as e:
                errors += 1
                print(f"  ERROR on feature {fid}: {e}", flush=True)
                record = {
                    "feature": fid,
                    "activation_frequency": feature.get("activation_frequency"),
                    "mean_activation": feature.get("mean_activation"),
                    "label": "ERROR",
                    "description": str(e),
                    "category": "unclear",
                    "monosemantic": None,
                    "interpretability_score": None,
                    "knowledge_domain": "unclear",
                    "abstraction_level": None,
                }
                out_f.write(json.dumps(record) + "\n")
                out_f.flush()

            # rate limiting
            elapsed_req = time.time() - t_req
            if elapsed_req < min_interval:
                time.sleep(min_interval - elapsed_req)

    total_time = time.time() - t_start
    print(
        f"\nDone. Labeled {labeled} features, {errors} errors, "
        f"in {total_time/60:.1f} min. Output: {output_path}",
        flush=True
    )


if __name__ == "__main__":
    main()
