#!/usr/bin/env python3
"""Normalize Grade 7 English correct-option reason labels for strict validation."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = ROOT / "authoring/question-bank-blueprints/grade-7.jsonl"


def main() -> int:
    rows = [json.loads(line) for line in BLUEPRINT.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed = 0
    for row in rows:
        if row.get("subject") != "İngilizce":
            continue
        correct = row.get("correct")
        reasons = row.get("distractorWhy")
        if not isinstance(correct, int) or not isinstance(reasons, list) or correct >= len(reasons):
            raise ValueError(f"{row.get('id')}: invalid correct/distractorWhy structure")
        reason = str(reasons[correct])
        if reason.startswith("Correct reasoning:"):
            reasons[correct] = "Doğru / correct reasoning:" + reason.removeprefix("Correct reasoning:")
            changed += 1
        if "doğru" not in str(reasons[correct]).casefold():
            raise ValueError(f"{row.get('id')}: correct reason still lacks the canonical label")
    if changed != 600:
        raise ValueError(f"expected 600 English reason-label repairs, found {changed}")
    BLUEPRINT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"blueprint": str(BLUEPRINT), "changed": changed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
