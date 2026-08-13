"""Generate deterministic collaborative story-adventure pools for AliKa."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from charades_language import ACTIONS, LANGUAGES, SUBJECTS
from story_language import CATEGORY, OBJECTS, SETTINGS, TWISTS


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "games" / "story-adventure" / "cards"
BANDS = ("young", "mid", "teen", "senior")
SOURCE = "https://www.zygomatic-games.com/en/game/rorys-story-cubes/"


def _id(language: str, band: str, subject_index: int, kit_index: int) -> str:
    raw = f"story-adventure-v1:{language}:{band}:{subject_index}:{kit_index}".encode()
    return "sto_" + hashlib.sha256(raw).hexdigest()[:20]


def generate() -> None:
    for language in LANGUAGES:
        subjects = SUBJECTS[language]
        settings, objects, twists = SETTINGS[language], OBJECTS[language], TWISTS[language]
        if len(subjects) != 25 or not all(len(items) == 8 for items in (settings, objects, twists)):
            raise ValueError(f"{language}: expected 25 characters and eight-part story kits")
        for band in BANDS:
            missions = ACTIONS[band][language]
            if len(missions) != 8:
                raise ValueError(f"{language}/{band}: expected 8 missions")
            rows = []
            for subject_index, character in enumerate(subjects):
                local = subject_index >= 20
                for kit_index in range(8):
                    rows.append({
                        "card_id": _id(language, band, subject_index, kit_index),
                        "character": character,
                        "setting": settings[kit_index],
                        "object": objects[(kit_index + subject_index) % 8],
                        "mission": missions[(kit_index + subject_index * 3) % 8],
                        "twist": twists[(kit_index + subject_index * 5) % 8],
                        "category": CATEGORY[language][1 if local else 0],
                        "difficulty": BANDS.index(band) + 1,
                        "source": {"title": "Official open-ended storytelling game", "url": SOURCE},
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
