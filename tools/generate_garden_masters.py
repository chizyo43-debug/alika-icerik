"""Generate deterministic, solvable Garden Masters missions."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

from garden_masters_language import KITS, PLANTS


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "games" / "garden-masters" / "missions"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = ("young", "mid", "teen", "senior")
EVENTS = ("gentle_rain", "golden_bee", "compost_boost", "shade_cloud", "wind_breeze")
PROFILES = {
    "young": {"size": 3, "plants": 4, "allowance": 4, "turns": 10},
    "mid": {"size": 4, "plants": 6, "allowance": 3, "turns": 12},
    "teen": {"size": 5, "plants": 8, "allowance": 2, "turns": 14},
    "senior": {"size": 6, "plants": 10, "allowance": 1, "turns": 16},
}
SOURCE = "https://www.rhs.org.uk/education-learning/school-gardening/resources/getting-started/setting-up-a-school-garden"


def _id(language: str, band: str, number: int) -> str:
    raw = f"garden-masters-v1:{language}:{band}:{number}".encode()
    return "gar_" + hashlib.sha256(raw).hexdigest()[:20]


def _neighbors(position: int, size: int) -> set[int]:
    x, y = position % size, position // size
    return {ny * size + nx for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
            if 0 <= nx < size and 0 <= ny < size}


def score(plants: list[dict], cells: list[dict], placements: list[dict], size: int,
          event: str, event_cells: list[int]) -> int:
    by_id = {plant["plant_id"]: plant for plant in plants}
    occupied = {item["plant_id"]: item["cell"] for item in placements}
    total = 0
    for plant_id, cell_index in occupied.items():
        plant, cell = by_id[plant_id], cells[cell_index]
        if cell["sun"] == plant["sun_need"] and cell["moisture"] == plant["moisture_need"]:
            total += plant["harvest_points"]
        if plant["kind"] == "flower":
            total += sum(1 for other_id, other_cell in occupied.items()
                         if by_id[other_id]["kind"] == "fruiting"
                         and other_cell in _neighbors(cell_index, size))
    total += sum(2 for item in placements if item["cell"] in event_cells
                 and event in ("golden_bee", "compost_boost"))
    return total


def generate() -> None:
    for language in LANGUAGES:
        if len(KITS[language]) != 5 or len(PLANTS[language]) != 10:
            raise ValueError(f"{language}: incomplete local garden data")
        for band in BANDS:
            profile = PROFILES[band]
            rows = []
            seen: set[str] = set()
            for number in range(200):
                rng = random.Random(f"alika-garden-masters-v1:{language}:{band}:{number}")
                size = profile["size"]
                plant_specs = list(PLANTS[language])
                rng.shuffle(plant_specs)
                plant_specs = plant_specs[:profile["plants"]]
                plants = []
                for index, (name, kind, sun, moisture) in enumerate(plant_specs):
                    plants.append({"plant_id": f"p{index}", "name": name, "kind": kind,
                                   "sun_need": sun, "moisture_need": moisture,
                                   "water_cost": 1 if moisture == 1 else 2,
                                   "harvest_points": 2 + (kind in ("fruiting", "root")),
                                   "pollinator_friendly": kind == "flower"})
                cells = [{"cell": cell, "sun": rng.randint(1, 3),
                          "moisture": rng.randint(1, 3),
                          "soil": rng.choice(("loam", "sand", "clay"))}
                         for cell in range(size * size)]
                positions = rng.sample(range(size * size), len(plants))
                placements = []
                for plant, position in zip(plants, positions):
                    cells[position]["sun"] = plant["sun_need"]
                    cells[position]["moisture"] = plant["moisture_need"]
                    placements.append({"plant_id": plant["plant_id"], "cell": position})
                event = EVENTS[number % len(EVENTS)]
                event_cells = sorted(rng.sample(range(size * size), min(2, size)))
                target = score(plants, cells, placements, size, event, event_cells)
                kit = KITS[language][number // 40]
                signature = hashlib.sha256(json.dumps(
                    {"cells": cells, "plants": plants, "solution": placements},
                    sort_keys=True, ensure_ascii=False).encode()).hexdigest()
                if signature in seen:
                    raise ValueError(f"{language}/{band}:{number + 1}: duplicate garden")
                seen.add(signature)
                rows.append({
                    "mission_id": _id(language, band, number + 1),
                    "board_size": size, "cells": cells, "plants": plants,
                    "solution": placements,
                    "water_budget": sum(plant["water_cost"] for plant in plants) + profile["allowance"],
                    "turn_limit": profile["turns"], "target_score": target,
                    "special_event": event, "event_cells": event_cells,
                    "garden": kit["garden"], "garden_style": kit["style"],
                    "difficulty": BANDS.index(band) + 1,
                    "source": {"title": "Official school-garden planning principles", "url": SOURCE},
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
