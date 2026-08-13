"""Generate deterministic, solvable Balance Workshop construction challenges."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

from balance_workshop_language import KITS


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "games" / "balance-workshop" / "challenges"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = ("young", "mid", "teen", "senior")
EVENTS = ("golden_anchor", "wind_gust", "moving_platform", "magnetic_lock", "earthquake_wave")
STRUCTURES = ("tower", "bridge", "balance_beam", "arch", "cantilever")
PROFILES = {
    "young": {"pieces": 5, "base": 8.0, "tilt": 10.0, "stability": 3,
              "wind": 0.4, "motion": 0.05, "shake": 0.04, "friction": 0.82},
    "mid": {"pieces": 7, "base": 7.0, "tilt": 8.0, "stability": 4,
            "wind": 0.8, "motion": 0.12, "shake": 0.08, "friction": 0.74},
    "teen": {"pieces": 9, "base": 6.0, "tilt": 6.0, "stability": 5,
             "wind": 1.2, "motion": 0.20, "shake": 0.13, "friction": 0.66},
    "senior": {"pieces": 11, "base": 5.2, "tilt": 4.0, "stability": 6,
               "wind": 1.6, "motion": 0.30, "shake": 0.18, "friction": 0.58},
}
SHAPES = {
    "young": ("beam", "arch", "triangle"),
    "mid": ("beam", "arch", "triangle", "cylinder"),
    "teen": ("beam", "arch", "triangle", "cylinder", "counterweight"),
    "senior": ("beam", "arch", "triangle", "cylinder", "counterweight", "wedge"),
}
SOURCE = "https://assets.education.lego.com/_/downloads/LearnToLearn_Curriculum_2.0_en-US.pdf"


def _challenge_id(language: str, band: str, number: int) -> str:
    raw = f"balance-workshop-v1:{language}:{band}:{number}".encode()
    return "bal_" + hashlib.sha256(raw).hexdigest()[:20]


def _piece(pair: int, side: str, shape: str, width: float, height: float,
           mass: float, friction: float, feature: str) -> dict:
    return {"piece_id": f"p{pair}{side}", "shape": shape, "width": width,
            "height": height, "mass": mass, "friction": friction, "feature": feature}


def _layout(language: str, band: str, number: int) -> tuple[list[dict], list[dict]]:
    profile = PROFILES[band]
    rng = random.Random(f"alika-balance-workshop-v1:{language}:{band}:{number}")
    pair_count = (profile["pieces"] - 1) // 2
    pieces: list[dict] = []
    solution: list[dict] = []
    for pair in range(pair_count):
        shape = rng.choice(SHAPES[band])
        width = round(rng.uniform(1.8, 2.35), 2)
        height = round(rng.uniform(0.72, 1.12), 2)
        mass = round(rng.uniform(1.0, 2.8), 2)
        x = round(max(profile["base"] * 0.08,
                      profile["base"] * (0.22 - pair * 0.02)), 2)
        y = round(pair * 1.18 + height / 2, 3)
        feature = "fragile" if band in ("teen", "senior") and pair == 1 else "normal"
        left = _piece(pair, "l", shape, width, height, mass, profile["friction"], feature)
        right = _piece(pair, "r", shape, width, height, mass, profile["friction"], feature)
        pieces.extend((left, right))
        solution.extend((
            {"piece_id": left["piece_id"], "x": -x, "y": y, "rotation": 0},
            {"piece_id": right["piece_id"], "x": x, "y": y, "rotation": 0},
        ))
    center_height = round(rng.uniform(0.8, 1.2), 2)
    center_feature = "golden" if EVENTS[number % len(EVENTS)] == "golden_anchor" else "normal"
    center = {"piece_id": "pc", "shape": rng.choice(("beam", "arch", "triangle")),
              "width": round(rng.uniform(1.7, 2.2), 2), "height": center_height,
              "mass": round(rng.uniform(1.2, 2.6), 2), "friction": profile["friction"],
              "feature": center_feature}
    pieces.append(center)
    solution.append({"piece_id": "pc", "x": 0.0,
                     "y": round(pair_count * 1.18 + center_height / 2, 3), "rotation": 0})
    rng.shuffle(pieces)
    return pieces, solution


def generate() -> None:
    for language in LANGUAGES:
        if len(KITS[language]) != 5:
            raise ValueError(f"{language}: expected five cultural workshop kits")
        for band in BANDS:
            profile = PROFILES[band]
            rows = []
            seen: set[str] = set()
            for number in range(200):
                pieces, solution = _layout(language, band, number)
                signature = hashlib.sha256(json.dumps(
                    {"pieces": pieces, "solution": solution}, sort_keys=True
                ).encode()).hexdigest()
                if signature in seen:
                    raise ValueError(f"{language}/{band}:{number + 1}: duplicate construction")
                seen.add(signature)
                event = EVENTS[number % len(EVENTS)]
                kit = KITS[language][number // 40]
                by_id = {piece["piece_id"]: piece for piece in pieces}
                target_height = round(max(
                    slot["y"] + by_id[slot["piece_id"]]["height"] / 2 for slot in solution
                ), 2)
                rows.append({
                    "challenge_id": _challenge_id(language, band, number + 1),
                    "construction_type": STRUCTURES[(number // 5) % len(STRUCTURES)],
                    "base_width": profile["base"],
                    "pieces": pieces,
                    "solution": solution,
                    "target_height": target_height,
                    "stability_seconds": profile["stability"],
                    "max_tilt_degrees": profile["tilt"],
                    "wind_strength": profile["wind"] if event == "wind_gust" else 0.0,
                    "platform_motion": profile["motion"] if event == "moving_platform" else 0.0,
                    "shake_strength": profile["shake"] if event == "earthquake_wave" else 0.0,
                    "gravity": 9.8,
                    "special_event": event,
                    "workshop": kit["workshop"],
                    "material": kit["material"],
                    "ornament": kit["ornament"],
                    "difficulty": BANDS.index(band) + 1,
                    "source": {"title": "Official structure, stability and weight activity", "url": SOURCE},
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
