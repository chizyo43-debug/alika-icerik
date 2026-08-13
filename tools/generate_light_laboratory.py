"""Generate deterministic, solvable Light Laboratory puzzles."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

from light_laboratory_language import THEMES


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "games" / "light-laboratory" / "puzzles"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = ("young", "mid", "teen", "senior")
EVENTS = ("golden_mirror", "energy_orb", "frozen_mirror", "portal_pair", "spectrum_burst")
COLORS = ("red", "green", "blue")
DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
PROFILES = {
    "young": {"size": 5, "length": 6, "rotatable": 1, "filters": 0, "allowance": 4},
    "mid": {"size": 6, "length": 10, "rotatable": 2, "filters": 1, "allowance": 3},
    "teen": {"size": 7, "length": 14, "rotatable": 3, "filters": 2, "allowance": 2},
    "senior": {"size": 8, "length": 18, "rotatable": 4, "filters": 3, "allowance": 1},
}
SOURCE = "https://www.exploratorium.edu/sites/default/files/files/Tinkering%20Studio%20Light%20and%20Shadow%20Starter%20Cards_English.pdf"


def _id(language: str, band: str, number: int) -> str:
    raw = f"light-laboratory-v1:{language}:{band}:{number}".encode()
    return "lig_" + hashlib.sha256(raw).hexdigest()[:20]


def _direction(first: int, second: int, size: int) -> int:
    ax, ay, bx, by = first % size, first // size, second % size, second // size
    delta = (bx - ax, by - ay)
    return DIRS.index(delta)


def _orientation(incoming: int, outgoing: int) -> int:
    slash = {(0, 1), (1, 0), (2, 3), (3, 2)}
    if (incoming, outgoing) in slash:
        return 0
    if (incoming, outgoing) in {(0, 3), (3, 0), (2, 1), (1, 2)}:
        return 1
    raise ValueError("invalid mirror turn")


def _path(size: int, length: int, minimum_turns: int, minimum_straights: int,
          rng: random.Random) -> list[int]:
    for _ in range(1000):
        start = rng.randrange(size) * size
        cells = [start]
        direction = 1
        while len(cells) < length:
            choices = []
            for candidate_direction in (direction, (direction - 1) % 4, (direction + 1) % 4):
                dx, dy = DIRS[candidate_direction]
                x, y = cells[-1] % size + dx, cells[-1] // size + dy
                nxt = y * size + x
                if 0 <= x < size and 0 <= y < size and nxt not in cells:
                    choices.append((candidate_direction, nxt))
            if not choices:
                break
            direction, nxt = rng.choice(choices)
            cells.append(nxt)
        turns = sum(_direction(cells[i - 1], cells[i], size) !=
                    _direction(cells[i], cells[i + 1], size) for i in range(1, len(cells) - 1))
        straights = max(0, len(cells) - 2 - turns)
        if len(cells) == length and turns >= minimum_turns and straights >= minimum_straights:
            return cells
    raise ValueError("unique light path unavailable")


def generate() -> None:
    for language in LANGUAGES:
        if len(THEMES[language]) != 5:
            raise ValueError(f"{language}: expected five local science themes")
        for band in BANDS:
            profile = PROFILES[band]
            rows = []
            seen: set[tuple[int, ...]] = set()
            for number in range(200):
                for attempt in range(100):
                    rng = random.Random(f"alika-light-lab-v1:{language}:{band}:{number}:{attempt}")
                    path = _path(profile["size"], profile["length"], profile["rotatable"],
                                 profile["filters"], rng)
                    signature = tuple(path)
                    if signature not in seen:
                        break
                else:
                    raise ValueError(f"{language}/{band}:{number + 1}: unique path unavailable")
                seen.add(signature)
                turns = []
                for index in range(1, len(path) - 1):
                    incoming = _direction(path[index - 1], path[index], profile["size"])
                    outgoing = _direction(path[index], path[index + 1], profile["size"])
                    if incoming != outgoing:
                        turns.append((index, _orientation(incoming, outgoing)))
                chosen_turns = sorted(rng.sample(turns, profile["rotatable"]), key=lambda item: item[0])
                chosen_indices = {item[0] for item in chosen_turns}
                color = rng.choice(COLORS)
                elements = []
                for index, orientation in turns:
                    rotatable = index in chosen_indices
                    elements.append({"type": "mirror", "cell": path[index],
                                     "rotatable": rotatable, "solution_orientation": orientation,
                                     "start_orientation": 1 - orientation if rotatable else orientation})
                straight = [index for index in range(1, len(path) - 1)
                            if index not in {item[0] for item in turns}]
                for index in rng.sample(straight, profile["filters"]):
                    elements.append({"type": "filter", "cell": path[index],
                                     "color": color, "rotatable": False})
                event = EVENTS[number % len(EVENTS)]
                event_cells = sorted(rng.sample(path[1:-1], 2))
                theme = THEMES[language][number // 40]
                rows.append({
                    "puzzle_id": _id(language, band, number + 1),
                    "board_size": profile["size"], "emitter_cell": path[0],
                    "emitter_direction": _direction(path[0], path[1], profile["size"]),
                    "emitter_color": color, "target_cell": path[-1], "target_color": color,
                    "solution_path": path, "elements": sorted(elements, key=lambda item: item["cell"]),
                    "energy_budget": len(path) + profile["allowance"],
                    "rotation_limit": profile["rotatable"] + profile["allowance"],
                    "special_event": event, "event_cells": event_cells,
                    "laboratory": theme["laboratory"], "artifact": theme["artifact"],
                    "difficulty": BANDS.index(band) + 1,
                    "source": {"title": "Official hands-on light and reflection principles", "url": SOURCE},
                    "culture_tags": [f"culture:{language}"], "review_status": "ai-draft",
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
