"""Phase 1 — Extract textbook chunks from preprocessed JSON files.

Reads three JSON inputs (flat list of strings) and writes a single JSON list
of normalized, deduplicated, length-filtered chunks to
data/extracted/textbook_text.json.

CLI:
  python -m src.data.extract_textbook_text \\
      --json_inputs \\
        data/preprocessed/processed_textbook_physics.json \\
        data/preprocessed/processed_textbook_chemistry.json \\
        data/preprocessed/processed_textbook_biology.json \\
      --output data/extracted/textbook_text.json
"""

import argparse
import hashlib
import json
from pathlib import Path


def normalize(s: str) -> str:
    """Collapse all whitespace runs to single spaces and strip."""
    return " ".join(s.split())


def domain_from_filename(path: str) -> str:
    name = Path(path).name.lower()
    if "phys" in name:
        return "physics"
    if "chem" in name:
        return "chemistry"
    if "bio" in name:
        return "biology"
    raise ValueError(f"cannot infer domain from filename: {path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json_inputs", nargs="+", required=True)
    ap.add_argument("--output", default="data/extracted/textbook_text.json")
    ap.add_argument("--min_chars", type=int, default=80)
    args = ap.parse_args()

    seen = set()
    chunks = []
    counts = {}

    for path in args.json_inputs:
        domain = domain_from_filename(path)
        counts.setdefault(domain, {"raw": 0, "kept": 0, "short": 0, "dup": 0})
        data = json.load(open(path))
        if not isinstance(data, list):
            raise ValueError(f"{path} is not a JSON list")

        for raw in data:
            counts[domain]["raw"] += 1
            if not isinstance(raw, str):
                # spec is flat list of strings; non-string entries are skipped
                counts[domain]["short"] += 1
                continue
            text = normalize(raw)
            if len(text) < args.min_chars:
                counts[domain]["short"] += 1
                continue
            h = hashlib.md5(text.encode("utf-8")).hexdigest()
            if h in seen:
                counts[domain]["dup"] += 1
                continue
            seen.add(h)
            idx = counts[domain]["kept"]
            counts[domain]["kept"] += 1
            chunks.append({
                "chunk_id": f"{domain}_{idx:06d}",
                "domain": domain,
                "source_file": Path(path).name,
                "chapter_or_section": "unknown",
                "text": text,
                "char_count": len(text),
                "approx_token_count": int(len(text.split()) * 1.3),
            })

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        json.dump(chunks, f, ensure_ascii=False)

    print(f"wrote {len(chunks)} chunks -> {out}")
    for d, c in counts.items():
        print(f"  {d}: raw={c['raw']} kept={c['kept']} "
              f"dropped_short={c['short']} deduped={c['dup']}")


if __name__ == "__main__":
    main()
