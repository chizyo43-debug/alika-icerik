"""Generate deterministic Family Escape Night symbol-code mysteries."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from pathlib import Path

from family_escape_language import THEMES


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "games" / "family-escape-night" / "puzzles"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = ("young", "mid", "teen", "senior")
SYMBOLS = ("star", "diamond", "clover", "drop", "moon", "sun")
EVENTS = ("secret_drawer", "golden_hint", "key_rain", "echo_clue", "moving_portrait")
PROFILES = {
    "young": {"symbols": 3, "clues": 3, "hints": 4, "types": {"position", "before", "adjacent"}},
    "mid": {"symbols": 4, "clues": 4, "hints": 3, "types": {"position", "before", "adjacent", "not_position"}},
    "teen": {"symbols": 5, "clues": 5, "hints": 2, "types": {"position", "before", "adjacent", "not_position", "distance"}},
    "senior": {"symbols": 6, "clues": 6, "hints": 2, "types": {"position", "before", "adjacent", "not_position", "distance", "between"}},
}
SOURCE = "https://www.thamesandkosmos.com/manuals/full/694043_EXIT_HoR_Manual.pdf"


def _id(language: str, band: str, number: int) -> str:
    raw = f"family-escape-night-v1:{language}:{band}:{number}".encode()
    return "esc_" + hashlib.sha256(raw).hexdigest()[:20]


def _matches(code: tuple[str, ...], clue: dict) -> bool:
    positions = {symbol: index for index, symbol in enumerate(code)}
    kind = clue["type"]
    if kind == "position":
        return positions[clue["symbol"]] == clue["position"]
    if kind == "not_position":
        return positions[clue["symbol"]] != clue["position"]
    if kind == "before":
        return positions[clue["first"]] < positions[clue["second"]]
    if kind == "adjacent":
        return abs(positions[clue["first"]] - positions[clue["second"]]) == 1
    if kind == "distance":
        return abs(positions[clue["first"]] - positions[clue["second"]]) == clue["distance"]
    if kind == "between":
        left, middle, right = positions[clue["left"]], positions[clue["middle"]], positions[clue["right"]]
        return min(left, right) < middle < max(left, right)
    return False


def _candidate_clues(solution: tuple[str, ...], allowed: set[str]) -> list[dict]:
    clues = []
    n = len(solution)
    for index, symbol in enumerate(solution):
        if "position" in allowed:
            clues.append({"type": "position", "symbol": symbol, "position": index})
        if "not_position" in allowed:
            clues.extend({"type": "not_position", "symbol": symbol, "position": wrong}
                         for wrong in range(n) if wrong != index)
    for first_index, second_index in itertools.combinations(range(n), 2):
        first, second = solution[first_index], solution[second_index]
        if "before" in allowed:
            clues.append({"type": "before", "first": first, "second": second})
        if "adjacent" in allowed and second_index - first_index == 1:
            clues.append({"type": "adjacent", "first": first, "second": second})
        if "distance" in allowed:
            clues.append({"type": "distance", "first": first, "second": second,
                          "distance": second_index - first_index})
    if "between" in allowed:
        for left_index, middle_index, right_index in itertools.combinations(range(n), 3):
            clues.append({"type": "between", "left": solution[left_index],
                          "middle": solution[middle_index], "right": solution[right_index]})
    return clues


def _make_clues(solution: tuple[str, ...], profile: dict, rng: random.Random):
    # A complete before-chain fixes one and only one ordering. The final clue is
    # redundant by design, but introduces the age-specific visual clue types.
    chosen = [{"type": "before", "first": solution[index], "second": solution[index + 1]}
              for index in range(len(solution) - 1)]
    extras = [clue for clue in _candidate_clues(solution, profile["types"])
              if clue not in chosen and clue["type"] != "before"]
    if not extras:
        return None
    chosen.append(rng.choice(extras))
    rng.shuffle(chosen)
    return chosen


def generate() -> None:
    for language in LANGUAGES:
        if len(THEMES[language]) != 5:
            raise ValueError(f"{language}: expected five local escape themes")
        for band in BANDS:
            profile = PROFILES[band]
            rows = []
            seen = set()
            for number in range(200):
                for attempt in range(1000):
                    rng = random.Random(f"alika-family-escape-v1:{language}:{band}:{number}:{attempt}")
                    symbols = tuple(rng.sample(SYMBOLS, profile["symbols"]))
                    solution = tuple(rng.sample(symbols, len(symbols)))
                    clues = _make_clues(solution, profile, rng)
                    signature = (symbols, json.dumps(clues, sort_keys=True)) if clues else None
                    if clues and signature not in seen:
                        break
                else:
                    raise ValueError(f"{language}/{band}:{number + 1}: unique mystery unavailable")
                seen.add(signature)
                room, treasure = THEMES[language][number // 40]
                rows.append({
                    "puzzle_id": _id(language, band, number + 1), "symbols": list(symbols),
                    "clues": clues, "solution_code": list(solution),
                    "hint_tokens": profile["hints"], "role_count": 4,
                    "special_event": EVENTS[number % len(EVENTS)],
                    "room": room, "treasure": treasure,
                    "difficulty": BANDS.index(band) + 1,
                    "source": {"title": "EXIT House of Riddles cooperative rulebook", "url": SOURCE},
                    "culture_tags": [f"culture:{language}"], "review_status": "ai-draft",
                })
            output = OUT / language / f"{band}.jsonl"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True,
                                                 separators=(",", ":")) + "\n" for row in rows),
                              encoding="utf-8", newline="\n")


def main() -> int:
    argparse.ArgumentParser().parse_args()
    generate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
