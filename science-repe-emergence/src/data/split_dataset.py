"""Split validated Source B contrast pairs into train/val/test (and a
paraphrased held-out set).

70/15/15 stratified by (dataset, domain). Pair stays in one split
(splitting by row, not by positive/negative).

Then build data/processed/paraphrase_test.jsonl: pick --n_paraphrase_per_dataset
test pairs per dataset (default 10), paraphrase both positive and negative
via gpt-4.1-mini, retry up to 3x to make the paraphrase pass the same
length-ratio / banned-token / shared-anchor / TF-IDF checks. Skip pairs that
never produce a valid paraphrase.

CLI:
  python -m src.data.split_dataset \\
      --input_dir data/generated \\
      --output_dir data/processed \\
      --train 0.70 --val 0.15 --test 0.15 \\
      --n_paraphrase_per_dataset 10
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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BANNED = [
    "correct", "incorrect", "wrong", "misconception", "false", "true",
    "actually", "in fact", "no,", "yes,",
]


def stratified_split(pairs, ratios, seed):
    """Per-(dataset, domain) bucket, shuffle, split 70/15/15.

    The remainder after rounding goes to test, which is the most defensible
    place to lose precision (test set tolerates +/-1 better than train)."""
    train_r, val_r, _ = ratios
    rng = random.Random(seed)

    buckets = defaultdict(list)
    for p in pairs:
        buckets[(p["dataset"], p["domain"])].append(p)

    train, val, test = [], [], []
    for key in sorted(buckets):
        group = buckets[key]
        rng.shuffle(group)
        n = len(group)
        n_train = int(round(n * train_r))
        n_val = int(round(n * val_r))
        # cap n_val so test gets at least one if n >= 3
        if n_train + n_val >= n and n >= 3:
            n_val = max(0, n - n_train - 1)
        train.extend(group[:n_train])
        val.extend(group[n_train:n_train + n_val])
        test.extend(group[n_train + n_val:])
    return train, val, test


def validate_paraphrase(pos, neg, anchors, vectorizer):
    reasons = []
    pn, nn = len(pos.split()), len(neg.split())
    if pn < 4 or nn < 4:
        reasons.append("too short")
    elif abs(pn - nn) / max(pn, nn) > 0.20:
        reasons.append(f"length ratio {pn}/{nn}")
    text = (pos + " " + neg).lower()
    for w in BANNED:
        if w in text:
            reasons.append(f"banned token: {w!r}")
            break
    pl, nl = pos.lower(), neg.lower()
    pos_hits = sum(1 for a in anchors if a.lower() in pl)
    neg_hits = sum(1 for a in anchors if a.lower() in nl)
    if pos_hits < 2:
        reasons.append(f"positive has {pos_hits} anchors")
    if neg_hits < 2:
        reasons.append(f"negative has {neg_hits} anchors")
    vecs = vectorizer.transform([pos, neg])
    sim = float(cosine_similarity(vecs[0], vecs[1])[0][0])
    if sim > 0.85:
        reasons.append(f"pos/neg TF-IDF cosine {sim:.3f} > 0.85")
    return reasons


PARAPHRASE_PROMPT = """Paraphrase the following two scientific statements while preserving their EXACT meaning.
The paraphrases will become a held-out test set for representation engineering, so they must rephrase the original ideas in different words while keeping which side is correct vs which side reflects a misconception.

Hard constraints:
  1. Preserve meaning exactly. Do not flip which side is the misconception.
  2. Both statements must still discuss the same concept.
  3. Whitespace-token lengths within +/- 20% of each other.
  4. Each side must contain at least 2 of these anchor terms: {anchors}.
  5. Neither may contain any of: "correct", "incorrect", "wrong", "misconception", "false", "true", "actually", "in fact", "no,", "yes,".
  6. Use noticeably different wording from the originals (not just a few-word swap).

Original positive: {positive}
Original negative: {negative}

Return ONLY valid JSON in this exact shape, no prose:
{{"positive": "...", "negative": "..."}}
"""


def paraphrase_one(client, model, pair):
    prompt = PARAPHRASE_PROMPT.format(
        anchors=", ".join(pair["shared_anchors"]),
        positive=pair["positive"],
        negative=pair["negative"],
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        response_format={"type": "json_object"},
    )
    obj = json.loads(resp.choices[0].message.content)
    return obj.get("positive", "").strip(), obj.get("negative", "").strip()


def paraphrase_with_retries(client, model, pair, vectorizer, max_retries):
    """Try up to max_retries times to produce a paraphrase that validates."""
    last_reasons = ["no attempts succeeded"]
    for attempt in range(1, max_retries + 1):
        try:
            p_pos, p_neg = paraphrase_one(client, model, pair)
        except Exception as e:
            last_reasons = [f"api error: {e}"]
            continue
        reasons = validate_paraphrase(
            p_pos, p_neg, pair["shared_anchors"], vectorizer
        )
        if not reasons:
            return True, p_pos, p_neg, attempt, []
        last_reasons = reasons
    return False, None, None, max_retries, last_reasons


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_dir", default="data/generated")
    ap.add_argument("--output_dir", default="data/processed")
    ap.add_argument("--train", type=float, default=0.70)
    ap.add_argument("--val", type=float, default=0.15)
    ap.add_argument("--test", type=float, default=0.15)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--n_paraphrase_per_dataset", type=int, default=10)
    ap.add_argument("--paraphrase_model", default="gpt-4.1-mini")
    ap.add_argument("--max_paraphrase_retries", type=int, default=3)
    ap.add_argument("--paraphrase_concurrency", type=int, default=10)
    args = ap.parse_args()

    files = sorted(Path(args.input_dir).glob("*.jsonl"))
    all_pairs = []
    for f in files:
        for line in open(f):
            all_pairs.append(json.loads(line))

    print(f"loaded {len(all_pairs)} pairs from {len(files)} files")
    by_dataset = defaultdict(int)
    for p in all_pairs:
        by_dataset[p["dataset"]] += 1
    for d in sorted(by_dataset):
        print(f"  {d}: {by_dataset[d]}")

    # 1) Stratified split
    train, val, test = stratified_split(
        all_pairs, (args.train, args.val, args.test), args.seed
    )
    for p in train:
        p["split"] = "train"
    for p in val:
        p["split"] = "val"
    for p in test:
        p["split"] = "test"

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for split_name, pairs in [("train", train), ("val", val), ("test", test)]:
        path = out / f"{split_name}.jsonl"
        with path.open("w") as f:
            for p in pairs:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
        print(f"wrote {len(pairs)} -> {path}")

    # per-split per-dataset table
    counts = {
        "train": defaultdict(int),
        "val": defaultdict(int),
        "test": defaultdict(int),
    }
    for split_name, pairs in [("train", train), ("val", val), ("test", test)]:
        for p in pairs:
            counts[split_name][p["dataset"]] += 1
    datasets = sorted({p["dataset"] for p in all_pairs})

    print(f"\nper-split per-dataset:")
    print(f"  {'dataset':<42} {'train':>6} {'val':>6} {'test':>6}")
    for ds in datasets:
        print(f"  {ds:<42} "
              f"{counts['train'][ds]:>6} {counts['val'][ds]:>6} "
              f"{counts['test'][ds]:>6}")

    flagged = [ds for ds in datasets if counts['train'][ds] < 30]
    if flagged:
        print(f"\n  CONCERN: <30 training pairs (LAT may be unstable): {flagged}")
    else:
        print(f"\n  OK: all datasets have >=30 training pairs.")

    # 2) Paraphrase test set
    print(f"\n--- generating paraphrase_test "
          f"({args.n_paraphrase_per_dataset} per dataset) ---")

    # build TF-IDF vectorizer over all texts so the IDF is comparable
    all_texts = []
    for p in all_pairs:
        all_texts.append(p["positive"])
        all_texts.append(p["negative"])
    vectorizer = TfidfVectorizer(stop_words="english").fit(all_texts)

    rng = random.Random(args.seed + 1)
    test_by_dataset = defaultdict(list)
    for p in test:
        test_by_dataset[p["dataset"]].append(p)

    load_dotenv(".env")
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    # pick candidates per dataset (not necessarily contiguous; we may need
    # to skip past pairs that all retries fail on, so pull more than N)
    paraphrase_pairs = []
    skipped = []

    def go(orig):
        ok, pp, pn, attempts, reasons = paraphrase_with_retries(
            client, args.paraphrase_model, orig, vectorizer,
            args.max_paraphrase_retries,
        )
        return orig, ok, pp, pn, attempts, reasons

    for ds in datasets:
        candidates = list(test_by_dataset[ds])
        rng.shuffle(candidates)
        target = min(args.n_paraphrase_per_dataset, len(candidates))
        if target < args.n_paraphrase_per_dataset:
            print(f"  WARN: {ds} test set has only {len(candidates)} pairs; "
                  f"requesting {target}")

        # try a pool 1.5x the target so failures don't starve the count
        pool = candidates[:max(target, int(target * 1.5) + 2)]
        kept_for_ds = 0

        with ThreadPoolExecutor(
            max_workers=args.paraphrase_concurrency
        ) as ex:
            futures = [ex.submit(go, p) for p in pool]
            for fut in as_completed(futures):
                orig, ok, pp, pn, attempts, reasons = fut.result()
                if kept_for_ds >= target:
                    continue  # already filled the quota
                if ok:
                    paraphrase_pairs.append({
                        **orig,
                        "pair_id": orig["pair_id"] + "_para",
                        "positive": pp,
                        "negative": pn,
                        "split": "paraphrase_test",
                        "notes": (
                            (orig.get("notes") or "")
                            + f" | paraphrased from {orig['pair_id']} "
                              f"in {attempts} attempt(s)"
                        ).strip(" |"),
                    })
                    kept_for_ds += 1
                else:
                    skipped.append({
                        "orig_pair_id": orig["pair_id"],
                        "dataset": orig["dataset"],
                        "reasons": reasons,
                    })

        print(f"  {ds}: kept {kept_for_ds}/{target}")

    para_path = out / "paraphrase_test.jsonl"
    with para_path.open("w") as f:
        for p in paraphrase_pairs:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    print(f"\nwrote {len(paraphrase_pairs)} paraphrase pairs -> {para_path}")
    if skipped:
        print(f"  skipped {len(skipped)} pairs whose paraphrases never validated")


if __name__ == "__main__":
    main()
