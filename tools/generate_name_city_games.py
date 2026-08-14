"""Generate deterministic localized Name–City rounds."""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

from name_city_language import (ALPHABETS, CATEGORIES, CATEGORY_IDS, CULTURE_FOCUS,
                                INITIAL_MODES)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "games" / "name-city" / "rounds"
LANGUAGES = tuple(ALPHABETS)
BANDS = ("young", "mid", "teen", "senior")
PROFILES = {
    "young": {"category_count": 5, "seconds": 150, "available": 7},
    "mid": {"category_count": 6, "seconds": 120, "available": 9},
    "teen": {"category_count": 7, "seconds": 90, "available": 12},
    "senior": {"category_count": 8, "seconds": 75, "available": 12},
}
EVENTS = ("golden_letter", "category_swap", "family_consult", "double_category", "lightning_round")
SOURCE = {"title": "Hasbro Scattergories official rules", "url": "https://instructions.hasbro.com/en-us/instruction/the-game-of-scattergories"}


def _id(language: str, band: str, index: int) -> str:
    raw = f"alika-name-city-v1:{language}:{band}:{index}".encode()
    return "nct_" + hashlib.sha256(raw).hexdigest()[:20]


def generate() -> None:
    for language in LANGUAGES:
        labels = dict(zip(CATEGORY_IDS, CATEGORIES[language], strict=True))
        alphabet = ALPHABETS[language]
        for band in BANDS:
            profile = PROFILES[band]
            rows, signatures = [], set()
            for index in range(200):
                attempt = 0
                while True:
                    rng = random.Random(f"alika-name-city-v1:{language}:{band}:{index}:{attempt}")
                    initial = alphabet[(index + rng.randrange(len(alphabet))) % len(alphabet)]
                    optional = list(CATEGORY_IDS[2:profile["available"]])
                    chosen = ["person", "city"] + rng.sample(optional, profile["category_count"] - 2)
                    rng.shuffle(chosen)
                    event = EVENTS[(index + rng.randrange(len(EVENTS))) % len(EVENTS)]
                    signature = (initial, tuple(chosen), event)
                    if signature not in signatures:
                        signatures.add(signature)
                        break
                    attempt += 1
                rows.append({
                    "round_id": _id(language, band, index),
                    "initial": initial,
                    "initial_mode": INITIAL_MODES[language],
                    "category_ids": chosen,
                    "categories": [labels[item] for item in chosen],
                    "culture_focus": CULTURE_FOCUS[language][index % 5],
                    "seconds": profile["seconds"],
                    "special_event": event,
                    "difficulty": BANDS.index(band) + 1,
                    "source": SOURCE,
                    "culture_tags": [f"culture:{language}"],
                    "review_status": "ai-draft",
                })
            path = OUT / language / f"{band}.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True,
                                               separators=(",", ":")) + "\n" for row in rows),
                            encoding="utf-8", newline="\n")


if __name__ == "__main__":
    generate()
