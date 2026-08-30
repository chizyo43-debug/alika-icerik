#!/usr/bin/env python3
"""Finish the Grade 5 social studies quota with 37 questions (grade rows 1601-1637)."""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json

import author_grade5_social_segment01 as base
import author_grade5_social_batch02 as data
import author_grade5_social_batch03 as authored


def triple_set() -> list[tuple[int, int, int]]:
    ordered = sorted(
        combinations(range(len(data.NOTE_IDS)), 3),
        key=lambda value: sha256(("-".join(map(str, value)) + "-alika-social-b03").encode()).hexdigest(),
    )
    values = ordered[129:166]
    if len(values) != 37:
        raise RuntimeError("social quota tail must contain 37 unique triples")
    # A sorted combination always makes late-index topics secondary.  Rotate
    # two records for each technology objective into the primary note slot so
    # the bank measures every canonical objective directly at least twice.
    primary_counts = {17: 0, 18: 0}
    oriented: list[tuple[int, int, int]] = []
    for value in values:
        target = next((index for index in (18, 17) if index in value and primary_counts[index] < 2), None)
        if target is None:
            oriented.append(value)
        else:
            oriented.append((target, *(index for index in value if index != target)))
            primary_counts[target] += 1
    if min(primary_counts.values()) < 2:
        raise RuntimeError("technology objectives could not be scheduled as primary twice")
    return oriented


def main() -> int:
    existing = [json.loads(line) for line in base.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1600:
        raise RuntimeError("the first 1600 grade questions must be regenerated before social batch 05")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    rows = [
        authored.triple_make(local, selected, note_map, labels, global_base=1600, batch_id="b05")
        for local, selected in enumerate(triple_set(), 1)
    ]
    base.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    base.LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"socialQuestions": 37, "socialTotal": 350, "gradeTotal": 1637}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
