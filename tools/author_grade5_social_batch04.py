#!/usr/bin/env python3
"""Author 100 three-topic social studies questions (grade rows 1501-1600)."""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json

import author_grade5_social_segment01 as base
import author_grade5_social_batch02 as data
import author_grade5_social_batch03 as prior


def triple_set() -> list[tuple[int, int, int]]:
    ordered = sorted(
        combinations(range(len(data.NOTE_IDS)), 3),
        key=lambda value: sha256(("-".join(map(str, value)) + "-alika-social-b03").encode()).hexdigest(),
    )
    values = ordered[29:129]
    if len(values) != 100 or set(values) & set(prior.triples()):
        raise RuntimeError("social batch 04 triple set is invalid")
    return values


def main() -> int:
    existing = [json.loads(line) for line in base.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1500:
        raise RuntimeError("the first 1500 grade questions must be regenerated before social batch 04")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    rows = [
        prior.triple_make(local, selected, note_map, labels, global_base=1500, batch_id="b04")
        for local, selected in enumerate(triple_set(), 1)
    ]
    base.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    base.LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"socialQuestions": 100, "socialTotal": 313, "gradeTotal": 1600}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
