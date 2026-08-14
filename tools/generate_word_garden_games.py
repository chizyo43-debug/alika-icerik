"""Generate child-safe hangman-style Word Garden puzzles from reviewed word pools."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "games" / "word-wheel" / "words"
OUT = ROOT / "games" / "word-garden" / "puzzles"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = ("young", "mid", "teen", "senior")
MISSES = {"young": 10, "mid": 8, "teen": 7, "senior": 6}
HINTS = {"young": 3, "mid": 2, "teen": 1, "senior": 1}
EVENTS = ("golden_letter", "bee_hint", "rainbow_bloom", "extra_petal", "family_whisper")


def _tile(language: str, char: str) -> str:
    if language == "tr":
        return {"i": "İ", "ı": "I"}.get(char, char.upper())
    if char == "ß":
        return "ẞ"
    return char.upper()


def answer_tiles(language: str, answer: str) -> list[str]:
    return [_tile(language, char) for char in answer if char.isalnum()]


def answer_pattern(answer: str) -> str:
    return "".join("_" if char.isalnum() else char for char in answer)


def _id(language: str, band: str, source_id: str) -> str:
    raw = f"alika-word-garden-v1:{language}:{band}:{source_id}".encode()
    return "wgd_" + hashlib.sha256(raw).hexdigest()[:20]


def generate() -> None:
    for language in LANGUAGES:
        for band in BANDS:
            source_path = SOURCE_ROOT / language / f"{band}.jsonl"
            source_rows = [json.loads(line) for line in source_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            if len(source_rows) != 200:
                raise ValueError(f"{language}/{band}: expected 200 source words")
            rows = []
            for index, source in enumerate(source_rows):
                tiles = answer_tiles(language, source["answer"])
                if not tiles:
                    raise ValueError(f"{language}/{band}:{index + 1}: answer has no letters")
                event_index = int(hashlib.sha256(source["puzzle_id"].encode()).hexdigest()[:8], 16)
                rows.append({
                    "puzzle_id": _id(language, band, source["puzzle_id"]),
                    "answer": source["answer"],
                    "letters": tiles,
                    "pattern": answer_pattern(source["answer"]),
                    "category": source["category"],
                    "clue": source["clue"],
                    "max_misses": MISSES[band],
                    "hint_tokens": HINTS[band],
                    "special_event": EVENTS[event_index % len(EVENTS)],
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


if __name__ == "__main__":
    generate()
