"""Validate Source B contrast-pair JSONL files.

For each pair:
  - positive/negative whitespace-token length ratio within +/-20%
  - >= 2 shared anchor terms (from `shared_anchors`) appear in BOTH texts
  - neither side contains banned giveaway tokens
  - positive vs negative TF-IDF cosine < 0.85 (not near-duplicates)

Drops are written to outputs/runs/dataset_generation_drops.jsonl with a
`reasons` field. Passing pairs overwrite the original JSONL in --input_dir.

CLI:
  python -m src.data.validate_dataset \\
      --input_dir data/generated \\
      --drops outputs/runs/dataset_generation_drops.jsonl
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BANNED = [
    "correct", "incorrect", "wrong", "misconception", "false", "true",
    "actually", "in fact", "no,", "yes,",
]
LENGTH_RATIO_MAX = 0.20
MIN_SHARED_ANCHORS = 2
TFIDF_DUP_MAX = 0.85


def check_length_ratio(pos, neg):
    pn, nn = len(pos.split()), len(neg.split())
    if pn == 0 or nn == 0:
        return "empty side"
    if abs(pn - nn) / max(pn, nn) > LENGTH_RATIO_MAX:
        return f"length ratio {pn}/{nn}"
    return None


def check_banned(pos, neg):
    text = (pos + " " + neg).lower()
    for w in BANNED:
        if w in text:
            return f"banned token: {w!r}"
    return None


def check_anchors(pos, neg, anchors):
    if not anchors or len(anchors) < MIN_SHARED_ANCHORS:
        return f"only {len(anchors or [])} anchor(s) defined"
    pl, nl = pos.lower(), neg.lower()
    pos_hits = sum(1 for a in anchors if a.lower() in pl)
    neg_hits = sum(1 for a in anchors if a.lower() in nl)
    if pos_hits < MIN_SHARED_ANCHORS:
        return f"positive has {pos_hits} anchors"
    if neg_hits < MIN_SHARED_ANCHORS:
        return f"negative has {neg_hits} anchors"
    return None


def check_pair_duplicate(pos, neg, vectorizer):
    vecs = vectorizer.transform([pos, neg])
    sim = float(cosine_similarity(vecs[0], vecs[1])[0][0])
    if sim > TFIDF_DUP_MAX:
        return f"pos/neg TF-IDF cosine {sim:.3f} > {TFIDF_DUP_MAX}"
    return None


def validate_pair(pair, vectorizer):
    """Return list of failure reasons. Empty list = pair passes."""
    p, n = pair["positive"], pair["negative"]
    anchors = pair.get("shared_anchors", [])
    reasons = []
    for fn in (
        lambda: check_length_ratio(p, n),
        lambda: check_banned(p, n),
        lambda: check_anchors(p, n, anchors),
        lambda: check_pair_duplicate(p, n, vectorizer),
    ):
        r = fn()
        if r:
            reasons.append(r)
    return reasons


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_dir", default="data/generated")
    ap.add_argument(
        "--drops",
        default="outputs/runs/dataset_generation_drops.jsonl",
    )
    args = ap.parse_args()

    files = sorted(Path(args.input_dir).glob("*.jsonl"))
    if not files:
        raise SystemExit(f"no JSONL files found in {args.input_dir}")
    print(f"validating {len(files)} files: {[f.name for f in files]}")

    # Build a single TF-IDF vectorizer over all texts so the IDF is stable
    file_pairs = {}
    all_texts = []
    for f in files:
        pairs = [json.loads(l) for l in open(f)]
        file_pairs[f] = pairs
        for p in pairs:
            all_texts.append(p["positive"])
            all_texts.append(p["negative"])
    print(f"loaded {sum(len(p) for p in file_pairs.values())} pairs total")

    vectorizer = TfidfVectorizer(stop_words="english").fit(all_texts)

    drops_path = Path(args.drops)
    drops_path.parent.mkdir(parents=True, exist_ok=True)

    total_kept = 0
    total_dropped = 0
    drops_by_reason = defaultdict(int)
    per_file = {}

    with drops_path.open("w") as drops_f:
        for f in files:
            pairs = file_pairs[f]
            kept, dropped = [], []
            for p in pairs:
                reasons = validate_pair(p, vectorizer)
                if reasons:
                    dropped.append(p)
                    drops_f.write(json.dumps(
                        {**p, "reasons": reasons}, ensure_ascii=False
                    ) + "\n")
                    for r in reasons:
                        # bucket reasons by leading phrase
                        key = r.split(":")[0].split(" ")[0:2]
                        drops_by_reason[" ".join(key)] += 1
                else:
                    kept.append(p)

            # overwrite the source file with passing pairs only
            with f.open("w") as out:
                for p in kept:
                    out.write(json.dumps(p, ensure_ascii=False) + "\n")

            per_file[f.name] = (len(kept), len(dropped))
            total_kept += len(kept)
            total_dropped += len(dropped)

    print(f"\nresults:")
    for name, (kept, dropped) in per_file.items():
        print(f"  {name:<46} kept={kept:>3} dropped={dropped:>3}")
    print(f"  {'TOTAL':<46} kept={total_kept:>3} dropped={total_dropped:>3}")
    if drops_by_reason:
        print(f"\ndrop reasons:")
        for r, n in sorted(drops_by_reason.items(), key=lambda x: -x[1]):
            print(f"  {r}: {n}")
    print(f"\ndrops -> {drops_path}")


if __name__ == "__main__":
    main()
