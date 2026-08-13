"""Generate deterministic, localized word-hunt puzzles from reviewed word pools."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "games" / "word-wheel" / "words"
OUT = ROOT / "games" / "word-hunt" / "puzzles"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = ("young", "mid", "teen", "senior")
BASE_DECOYS = {"young": 0, "mid": 1, "teen": 2, "senior": 3}


def _tile(language: str, char: str) -> str:
    if language == "tr":
        return {"i": "İ", "ı": "I"}.get(char, char.upper())
    if char == "ß":
        return "ẞ"
    return char.upper()


def _answer_tiles(language: str, answer: str) -> list[str]:
    return [_tile(language, char) for char in answer if char.isalnum()]


def _id(language: str, band: str, source_id: str) -> str:
    raw = f"word-hunt-v1:{language}:{band}:{source_id}".encode()
    return "hun_" + hashlib.sha256(raw).hexdigest()[:20]


def generate() -> None:
    for language in LANGUAGES:
        for band in BANDS:
            source_path = SOURCE_ROOT / language / f"{band}.jsonl"
            source_rows = [json.loads(line) for line in source_path.read_text(encoding="utf-8").splitlines()
                           if line.strip()]
            alphabet = sorted({tile for row in source_rows
                               for tile in _answer_tiles(language, row["answer"])})
            if len(source_rows) != 200 or len(alphabet) < 8:
                raise ValueError(f"{language}/{band}: incomplete source word pool")
            rows = []
            for index, source in enumerate(source_rows):
                answer_tiles = _answer_tiles(language, source["answer"])
                if not answer_tiles:
                    raise ValueError(f"{language}/{band}:{index + 1}: answer has no tiles")
                rng = random.Random(f"alika-word-hunt-v1:{language}:{band}:{source['puzzle_id']}")
                decoy_count = max(BASE_DECOYS[band], 3 - len(answer_tiles))
                decoys = [rng.choice(alphabet) for _ in range(decoy_count)]
                rack = answer_tiles + decoys
                if len(rack) > 1:
                    for _ in range(4):
                        rng.shuffle(rack)
                        if rack != answer_tiles + decoys:
                            break
                bonus_index = int(hashlib.sha256(source["answer"].encode()).hexdigest()[:8], 16)
                rows.append({
                    "puzzle_id": _id(language, band, source["puzzle_id"]),
                    "answer": source["answer"],
                    "answer_letters": "".join(answer_tiles),
                    "rack": rack,
                    "category": source["category"],
                    "clue": source["clue"],
                    "bonus_letter": answer_tiles[bonus_index % len(answer_tiles)],
                    "difficulty": BANDS.index(band) + 1,
                    "source": source["source"],
                    "culture_tags": source["culture_tags"],
                    "review_status": "ai-draft",
                })
            path = OUT / language / f"{band}.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True,
                                               separators=(",", ":")) + "\n" for row in rows),
                            encoding="utf-8", newline="\n")


def main() -> int:
    argparse.ArgumentParser().parse_args()
    generate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
