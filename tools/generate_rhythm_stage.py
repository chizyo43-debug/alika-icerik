"""Generate deterministic original rhythm challenges for AliKa."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

from rhythm_stage_language import KITS


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "games" / "rhythm-stage" / "challenges"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = ("young", "mid", "teen", "senior")
EVENTS = ("golden_beat", "time_freeze", "echo_round", "missing_beat", "tempo_lift")
PROFILES = {
    "young": {"steps": 8, "bars": 1, "hits": (3, 5), "secondary": (0, 0),
              "simultaneous": 0, "tempo": (72, 92), "tolerance": 180, "swing": (0,)},
    "mid": {"steps": 8, "bars": 2, "hits": (6, 9), "secondary": (1, 2),
            "simultaneous": 0, "tempo": (84, 110), "tolerance": 140, "swing": (0,)},
    "teen": {"steps": 8, "bars": 2, "hits": (8, 12), "secondary": (2, 4),
             "simultaneous": 1, "tempo": (96, 128), "tolerance": 110, "swing": (0, 8)},
    "senior": {"steps": 8, "bars": 3, "hits": (12, 17), "secondary": (4, 7),
               "simultaneous": 2, "tempo": (108, 148), "tolerance": 90, "swing": (0, 8, 12)},
}
SOURCE = "https://musiclab.chromeexperiments.com/Rhythm/"


def _id(language: str, band: str, number: int) -> str:
    raw = f"rhythm-stage-v1:{language}:{band}:{number}".encode()
    return "rhy_" + hashlib.sha256(raw).hexdigest()[:20]


def _pattern(language: str, band: str, number: int, seen: set[tuple[int, ...]]) -> tuple[list[int], random.Random, int]:
    profile = PROFILES[band]
    length = profile["steps"] * profile["bars"]
    for attempt in range(100):
        rng = random.Random(f"alika-rhythm-stage-v1:{language}:{band}:{number}:{attempt}")
        hit_count = rng.randint(*profile["hits"])
        positions = sorted(rng.sample(range(length), hit_count))
        if 0 not in positions:
            positions[0] = 0
            positions = sorted(set(positions))
            while len(positions) < hit_count:
                positions.append(rng.choice([p for p in range(length) if p not in positions]))
                positions.sort()
        pattern = [0] * length
        for position in positions:
            pattern[position] = 1
        secondary_count = min(rng.randint(*profile["secondary"]), len(positions))
        for position in rng.sample(positions, secondary_count):
            pattern[position] = 2
        for position in rng.sample(positions, min(profile["simultaneous"], len(positions))):
            pattern[position] = 3
        tempo_min, tempo_max = profile["tempo"]
        tempo = rng.randrange(tempo_min, tempo_max + 1, 2)
        signature = (*pattern, tempo)
        if signature not in seen:
            seen.add(signature)
            return pattern, rng, tempo
    raise ValueError(f"{language}/{band}:{number + 1}: unique rhythm unavailable")


def generate() -> None:
    for language in LANGUAGES:
        if len(KITS[language]) != 5:
            raise ValueError(f"{language}: expected five cultural rhythm kits")
        for band in BANDS:
            profile = PROFILES[band]
            rows = []
            seen: set[tuple[int, ...]] = set()
            for number in range(200):
                pattern, rng, tempo = _pattern(language, band, number, seen)
                kit = KITS[language][number // 40]
                hit_positions = [index for index, value in enumerate(pattern) if value]
                accent_count = {"young": 1, "mid": 1, "teen": 2, "senior": 3}[band]
                accents = sorted(rng.sample(hit_positions, min(accent_count, len(hit_positions))))
                rows.append({
                    "challenge_id": _id(language, band, number + 1),
                    "tempo_bpm": tempo,
                    "steps_per_bar": profile["steps"],
                    "bars": profile["bars"],
                    "pattern": pattern,
                    "accent_steps": accents,
                    "swing_percent": rng.choice(profile["swing"]),
                    "tolerance_ms": profile["tolerance"],
                    "primary_instrument": kit["primary"],
                    "primary_sound": kit["primary_sound"],
                    "secondary_instrument": kit["secondary"],
                    "secondary_sound": kit["secondary_sound"],
                    "stage": kit["stage"],
                    "special_event": EVENTS[number % len(EVENTS)],
                    "difficulty": BANDS.index(band) + 1,
                    "source": {"title": "Interactive rhythm-learning principles", "url": SOURCE},
                    "culture_tags": [f"culture:{language}"],
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
