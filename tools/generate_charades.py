"""Generate deterministic creative charades pools for all AliKa languages."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from charades_language import ACTIONS, CATEGORY, LANGUAGES, SUBJECTS


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "games" / "charades" / "cards"
BANDS = ("young", "mid", "teen", "senior")
SOURCE = "https://instructions.hasbro.com/en-us/instruction/guesstures-game"


def _id(language: str, band: str, subject_index: int, action_index: int) -> str:
    raw = f"charades-v1:{language}:{band}:{subject_index}:{action_index}".encode()
    return "cha_" + hashlib.sha256(raw).hexdigest()[:20]


def generate() -> None:
    for language in LANGUAGES:
        subjects = SUBJECTS[language]
        if len(subjects) != 25:
            raise ValueError(f"{language}: expected 25 subjects")
        for band in BANDS:
            actions = ACTIONS[band][language]
            if len(actions) != 8:
                raise ValueError(f"{language}/{band}: expected 8 actions")
            rows = []
            for subject_index, subject in enumerate(subjects):
                local = subject_index >= 20
                for action_index, action in enumerate(actions):
                    rows.append({
                        "card_id": _id(language, band, subject_index, action_index),
                        "prompt": f"{subject} — {action}",
                        "category": CATEGORY[language][1 if local else 0],
                        "difficulty": BANDS.index(band) + 1,
                        "source": {"title": "Official high-speed charades rules", "url": SOURCE},
                        "culture_tags": [f"culture:{language}"] if local else ["culture:universal"],
                        "review_status": "ai-draft",
                    })
            path = OUT / language / f"{band}.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":")) + "\n" for row in rows)
            path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    argparse.ArgumentParser().parse_args()
    generate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
