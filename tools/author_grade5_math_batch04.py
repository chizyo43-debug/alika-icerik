#!/usr/bin/env python3
"""Author 100 additional two-problem mathematics questions (grade rows 1101-1200)."""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json

import author_grade5_math_segment01 as base
import author_grade5_math_batch02 as data
import author_grade5_math_batch03 as paired


def second_pair_set() -> list[tuple[int, int]]:
    ordered = sorted(
        combinations(range(len(data.NOTE_IDS)), 2),
        key=lambda value: sha256(("-".join(map(str, value)) + "-alika-mat-b03").encode()).hexdigest(),
    )
    values = ordered[100:200]
    if len(values) != 100 or set(values) & set(ordered[:100]):
        raise RuntimeError("second mathematics pair set is incomplete or overlaps batch 03")
    return values


def main() -> int:
    existing = [json.loads(line) for line in base.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1100:
        raise RuntimeError("the first 1100 grade questions must be regenerated before math batch 04")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    rows = [
        paired.make(local, selected, note_map, labels, global_base=1100, batch_id="b04")
        for local, selected in enumerate(second_pair_set(), 1)
    ]
    base.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    base.LABELS_OUTPUT.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({"mathQuestions": 100, "mathTotal": 315, "gradeTotal": 1200}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
