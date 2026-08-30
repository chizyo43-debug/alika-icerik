#!/usr/bin/env python3
"""Finish the Grade 5 bank with 100 unique triple Turkish questions (rows 1901-2000)."""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json

import author_grade5_turkish_segment01 as base
import author_grade5_turkish_batch03 as prior


def triple_set() -> list[tuple[int, int, int]]:
    ordered = sorted(
        combinations(range(len(base.NOTE_IDS)), 3),
        key=lambda value: sha256(("-".join(map(str, value)) + "-alika-tur-b03-triple").encode()).hexdigest(),
    )
    values = ordered[32:132]
    if len(values) != 100 or set(values) & set(prior.triple_set()):
        raise RuntimeError("Turkish batch 04 triple set is invalid")
    # Sorted triples strand the final spelling/semantic objectives in a
    # secondary-only position.  Rotate two records for each into the primary
    # note slot; the combination itself and all three tasks remain unchanged.
    primary_counts = {20: 0, 21: 0}
    oriented: list[tuple[int, int, int]] = []
    for value in values:
        target = next((index for index in (21, 20) if index in value and primary_counts[index] < 2), None)
        if target is None:
            oriented.append(value)
        else:
            oriented.append((target, *(index for index in value if index != target)))
            primary_counts[target] += 1
    if min(primary_counts.values()) < 2:
        raise RuntimeError("late Turkish objectives could not be scheduled as primary twice")
    return oriented


def main() -> int:
    existing = [json.loads(line) for line in base.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1900:
        raise RuntimeError("the first 1900 grade questions must be regenerated before Turkish batch 04")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    rows = [
        prior.triple_make(local, selected, note_map, labels, global_base=1900, batch_id="b04")
        for local, selected in enumerate(triple_set(), 1)
    ]
    base.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    base.LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"turkishQuestions": 100, "turkishTotal": 363, "gradeTotal": 2000}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
