"""Phase 2 — Curate Source A suffix bank from extracted textbook chunks.

Reads data/extracted/textbook_text.json, applies a strict filter for
self-contained scientific content, scores survivors for ranking, and writes
data/repe_suffixes/science_suffix_bank.jsonl.

Quality matters more than quantity here: a vgel-style suffix has to be
something the model can plausibly continue under either a positive or
negative reasoning persona. Fragments, references to unseen
figures/tables/equations, anaphoric starts ("It / This / That ..."),
pedagogical scaffolding ("First we draw...", "Notice that..."), URLs, and
inline citations all break that contract and are filtered out.

After the heuristic filter, an optional LLM judge (gpt-4.1-mini) gives each
survivor a final keep/drop. The judge is on by default; pass
--no_llm_judge to skip it.

CLI:
  python -m src.data.build_repe_suffix_bank \\
      --input data/extracted/textbook_text.json \\
      --output data/repe_suffixes/science_suffix_bank.jsonl \\
      --max_per_domain 120
"""

import argparse
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


DOMAIN_TERMS = {
    "physics": [
        "force", "energy", "mass", "momentum", "velocity", "acceleration",
        "wave", "field", "pressure", "current", "voltage", "charge",
        "particle", "atom", "frequency", "amplitude", "gravity", "friction",
        "kinetic", "potential", "magnetic", "electric", "resistance",
        "thermal", "heat", "temperature", "conservation", "inertia",
    ],
    "chemistry": [
        "reaction", "molecule", "atom", "bond", "electron", "proton",
        "compound", "element", "acid", "base", "solution", "concentration",
        "equilibrium", "catalyst", "oxidation", "reduction", "isotope",
        "ion", "mole", "polar", "covalent", "ionic", "neutron", "orbital",
        "ph", "enthalpy", "entropy",
    ],
    "biology": [
        "cell", "protein", "enzyme", "dna", "rna", "membrane", "gene",
        "tissue", "organism", "selection", "evolution", "species",
        "mitosis", "meiosis", "photosynthesis", "respiration", "homeostasis",
        "nucleus", "ribosome", "mitochondria", "diffusion", "osmosis",
        "transcription", "translation", "chromosome", "phospholipid",
    ],
}

VERB_HINTS = [
    " is ", " are ", " was ", " were ", " has ", " have ", " had ",
    " can ", " will ", " do ", " does ", " did ", " be ", " been ",
    " causes ", " produces ", " increases ", " decreases ", " becomes ",
    " forms ", " creates ", " requires ", " depends ", " results ",
    " leads ", " contains ", " consists ", " happens ", " occurs ",
    " moves ", " makes ", " gives ", " provides ", " shows ",
    " acts ", " exerts ", " emits ", " absorbs ", " carries ",
]

CAUSAL_TOKENS = [
    "because", "therefore", "depends on", "causes", "results in",
    "leads to", "due to", "as a result", "occurs when", "happens when",
    "when ", "if ",
]


# Hard-filter substring lists. ALL are matched against the lowercased text.
META_REFERENCES = [
    "figure ", "table ", "fig.", "tbl.", "eq.", "equation ",
    "section ", "chapter ", "appendix ", "page ",
    "shown above", "shown below", "shown in figure", "shown in table",
    "see figure", "see table", "see also", "see appendix",
    "described in", "discussed previously", "as illustrated",
    "as discussed", "as shown",
    "we will see", "we shall see", "in the next", "in the previous",
    "later in", "earlier in",
]

PEDAGOGICAL_REFERENCES = [
    "this site", "this section", "this book", "this textbook",
    "this chapter", "this lab", "this course", "this video",
    "you can ", "you will ", "you may ", "you should ",
    "we draw ", "we assign ", "we calculate ", "we will ", "we shall ",
    "we can see", "we know that", "as we see",
]

URL_PATTERNS = ["http://", "https://", "www."]

ANAPHORIC_PREFIXES = (
    "it ", "this ", "that ", "these ", "those ", "such ",
    "there ", "here ",
    "however,", "therefore,", "thus,", "hence,",
    "moreover,", "furthermore,", "also,",
)

INSTRUCTIONAL_PREFIXES = (
    "note that", "notice that", "recall that", "remember that",
    "keep in mind",
    "first we ", "first, we ", "next we ", "next, we ", "now we ",
)

NUM_LIST_RE = re.compile(r"^\d+\.\s")
LETTER_LIST_RE = re.compile(r"^\(?[a-z]\)\s|^\[\d+\]")
LONE_CAP_RE = re.compile(r"^[A-Z]\.\s")


def passes_filter(chunk):
    text = chunk["text"]
    cc = chunk["char_count"]
    tok = chunk["approx_token_count"]

    if not (100 <= cc <= 400):
        return False
    if not (20 <= tok <= 80):
        return False
    if not text.rstrip().endswith((".", "?", "!")):
        return False
    if text.startswith("#"):
        return False

    low = text.lower()

    if NUM_LIST_RE.match(text) or LETTER_LIST_RE.match(text):
        return False
    if LONE_CAP_RE.match(text):
        return False

    if any(p in low for p in URL_PATTERNS):
        return False
    if any(m in low for m in META_REFERENCES):
        return False
    if any(p in low for p in PEDAGOGICAL_REFERENCES):
        return False
    if any(low.startswith(p) for p in ANAPHORIC_PREFIXES):
        return False
    if any(low.startswith(p) for p in INSTRUCTIONAL_PREFIXES):
        return False

    padded = " " + low + " "
    if not any(t in padded for t in DOMAIN_TERMS.get(chunk["domain"], [])):
        return False
    if not any(v in padded for v in VERB_HINTS):
        return False

    return True


def score(chunk):
    """Rank survivors. All hard criteria already satisfied."""
    text = chunk["text"]
    tok = chunk["approx_token_count"]
    s = 0.0
    if 25 <= tok <= 50:
        s += 0.30
    elif 20 <= tok <= 70:
        s += 0.15
    padded = " " + text.lower() + " "
    s += min(0.30, 0.10 * sum(1 for v in VERB_HINTS if v in padded))
    s += min(0.30, 0.10 * sum(1 for t in DOMAIN_TERMS.get(chunk["domain"], [])
                              if t in padded))
    if any(c in padded for c in CAUSAL_TOKENS):
        s += 0.10
    return min(s, 1.0)


def why(chunk):
    bits = []
    text = chunk["text"]
    tok = chunk["approx_token_count"]
    if 25 <= tok <= 50:
        bits.append("token-band")
    padded = " " + text.lower() + " "
    if any(v in padded for v in VERB_HINTS):
        bits.append("verb")
    if any(t in padded for t in DOMAIN_TERMS.get(chunk["domain"], [])):
        bits.append("technical-term")
    if any(c in padded for c in CAUSAL_TOKENS):
        bits.append("causal")
    return ", ".join(bits) or "default"


JUDGE_PROMPT = """You are filtering candidate text passages for a representation
engineering experiment on scientific reasoning. A KEEP-able passage is:
  - a self-contained scientific statement (no anaphoric "it/this/that"
    referring to outside context)
  - about a specific scientific concept, mechanism, or relationship
  - grammatically clean and free of OCR artifacts
  - free of references to figures/tables/equations the reader cannot see
  - free of pedagogical scaffolding ("we will...", "first we draw...",
    "you can see...", "in this chapter")
  - the kind of passage a model could naturally continue under either a
    "deep mechanistic" or a "surface misconception" persona

A REJECT-able passage is fragmentary, a header/caption, a worked-example
walkthrough, a meta description of the textbook, or has obvious OCR garbage.

Domain: {domain}

Passage:
{text}

Reply with valid JSON only:
{{"keep": true|false, "reason": "<one short phrase>"}}
"""


def llm_judge_one(client, model, chunk):
    prompt = JUDGE_PROMPT.format(domain=chunk["domain"], text=chunk["text"])
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=60,
        response_format={"type": "json_object"},
    )
    obj = json.loads(resp.choices[0].message.content)
    return bool(obj.get("keep")), obj.get("reason", "")


def llm_judge(chunks, model, concurrency):
    """Parallel keep/drop pass. Returns list of (chunk, keep, reason)."""
    load_dotenv(".env")
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    results = [None] * len(chunks)

    def go(i):
        try:
            keep, reason = llm_judge_one(client, model, chunks[i])
            return i, keep, reason
        except Exception as e:
            return i, True, f"judge_error: {e}"  # default-keep on API failure

    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = [ex.submit(go, i) for i in range(len(chunks))]
        for n, fut in enumerate(as_completed(futures), 1):
            i, keep, reason = fut.result()
            results[i] = (chunks[i], keep, reason)
            if n % 50 == 0 or n == len(chunks):
                print(f"  judge {n}/{len(chunks)}")
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/extracted/textbook_text.json")
    ap.add_argument(
        "--output",
        default="data/repe_suffixes/science_suffix_bank.jsonl",
    )
    ap.add_argument("--max_per_domain", type=int, default=120)
    ap.add_argument("--min_quality_score", type=float, default=0.0,
                    help="floor for sending candidates to the judge; "
                         "0.0 means the judge sees every hard-pass chunk")
    ap.add_argument("--no_llm_judge", action="store_true",
                    help="skip the gpt-4.1-mini keep/drop pass")
    ap.add_argument("--judge_model", default="gpt-4.1-mini")
    ap.add_argument("--judge_concurrency", type=int, default=20)
    ap.add_argument("--judge_pool_factor", type=int, default=5,
                    help="run judge on top max_per_domain*factor candidates "
                         "per domain so that drops don't starve the bank")
    ap.add_argument("--drops_path",
                    default="outputs/runs/suffix_bank_drops.jsonl",
                    help="where to log judge drops for inspection")
    args = ap.parse_args()

    chunks = json.load(open(args.input))
    print(f"loaded {len(chunks)} chunks")

    # 1) Hard filter + score + per-domain ranking
    by_domain = {}
    for c in chunks:
        if passes_filter(c):
            by_domain.setdefault(c["domain"], []).append(c)

    candidates_per_domain = {}
    for domain, cs in by_domain.items():
        scored = sorted(((score(c), c) for c in cs), key=lambda x: -x[0])
        scored = [(s, c) for s, c in scored if s >= args.min_quality_score]
        # take a larger pool so the LLM judge can drop without starving
        pool = scored[:args.max_per_domain * args.judge_pool_factor]
        candidates_per_domain[domain] = pool
        print(f"  {domain}: {len(cs)} pass-hard, "
              f"{len(scored)} pass-score>={args.min_quality_score}, "
              f"pool={len(pool)} sent to judge")

    # 2) Optional LLM judge
    judge_results = {}
    if not args.no_llm_judge:
        all_pool = [c for pool in candidates_per_domain.values() for _, c in pool]
        print(f"\nrunning LLM judge on {len(all_pool)} candidates "
              f"(model={args.judge_model}, concurrency={args.judge_concurrency})")
        results = llm_judge(all_pool, args.judge_model, args.judge_concurrency)
        for c, keep, reason in results:
            judge_results[c["chunk_id"]] = (keep, reason)
        kept = sum(1 for k, _ in judge_results.values() if k)
        print(f"judge kept {kept} / {len(all_pool)}")

    # 3) Final pick: top max_per_domain after LLM filter
    selected = []
    counts = {}
    for domain, pool in candidates_per_domain.items():
        kept = []
        for sc, c in pool:
            if not args.no_llm_judge:
                keep, _ = judge_results.get(c["chunk_id"], (True, ""))
                if not keep:
                    continue
            kept.append((sc, c))
            if len(kept) >= args.max_per_domain:
                break
        counts[domain] = len(kept)
        for i, (sc, c) in enumerate(kept):
            entry = {
                "suffix_id": f"{domain}_suffix_{i:06d}",
                "domain": domain,
                "source_chunk_id": c["chunk_id"],
                "chapter_or_section": c.get("chapter_or_section", "unknown"),
                "text": c["text"],
                "approx_token_count": c["approx_token_count"],
                "quality_score": round(sc, 3),
                "why_selected": why(c),
            }
            if not args.no_llm_judge:
                _, reason = judge_results.get(c["chunk_id"], (True, "kept"))
                entry["judge_reason"] = reason
            selected.append(entry)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for s in selected:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    # Drops sidecar for inspection (judge-rejected candidates)
    if not args.no_llm_judge:
        drops_path = Path(args.drops_path)
        drops_path.parent.mkdir(parents=True, exist_ok=True)
        with drops_path.open("w") as f:
            for pool in candidates_per_domain.values():
                for sc, c in pool:
                    keep, reason = judge_results.get(c["chunk_id"], (True, ""))
                    if not keep:
                        f.write(json.dumps({
                            "chunk_id": c["chunk_id"],
                            "domain": c["domain"],
                            "score": round(sc, 3),
                            "judge_reason": reason,
                            "text": c["text"],
                        }, ensure_ascii=False) + "\n")
        print(f"logged judge drops -> {drops_path}")

    print(f"\nwrote {len(selected)} suffixes -> {out}")
    for d in sorted(counts):
        n = counts[d]
        mean_tok = (
            sum(s["approx_token_count"] for s in selected if s["domain"] == d)
            / max(n, 1)
        )
        flag = "  <-- BELOW TARGET" if n < args.max_per_domain else ""
        print(f"  {d}: kept={n} mean_tokens={mean_tok:.1f}{flag}")


if __name__ == "__main__":
    main()
