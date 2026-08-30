#!/usr/bin/env python3
"""Author 100 unused-pair Grade 5 Turkish questions (grade rows 1701-1800)."""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json

import author_grade5_turkish_segment01 as base


def pair_set() -> list[tuple[int, int]]:
    excluded = set(base.balanced_pairs())
    available = [value for value in combinations(range(len(base.NOTE_IDS)), 2) if value not in excluded]
    counts = [0] * len(base.NOTE_IDS)
    selected: list[tuple[int, int]] = []

    def digest(value: tuple[int, int]) -> str:
        return sha256(("-".join(map(str, value)) + "-alika-tur-b02").encode()).hexdigest()

    for _ in range(100):
        pair = min(
            (value for value in available if value not in selected),
            key=lambda value: (max(counts[value[0]], counts[value[1]]), counts[value[0]] + counts[value[1]], digest(value)),
        )
        selected.append(pair)
        counts[pair[0]] += 1
        counts[pair[1]] += 1
    if len(set(selected)) != 100 or set(selected) & excluded:
        raise RuntimeError("Turkish batch 02 pair set is invalid")
    return selected


def main() -> int:
    existing = [json.loads(line) for line in base.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1700:
        raise RuntimeError("the first 1700 grade questions must be regenerated before Turkish batch 02")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    rows = [
        base.make(local, selected, note_map, labels, global_base=1700, batch_id="b02", schedule_offset=0)
        for local, selected in enumerate(pair_set(), 1)
    ]
    base.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    base.LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"turkishQuestions": 100, "turkishTotal": 163, "gradeTotal": 1800}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
