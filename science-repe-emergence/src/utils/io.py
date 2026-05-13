"""I/O helpers: JSON / JSONL with utf-8 + parent-dir creation."""

import json
from pathlib import Path


def load_jsonl(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path, rows):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def load_json(path):
    with open(path) as f:
        return json.load(f)


def write_json(path, obj, indent=None):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)
