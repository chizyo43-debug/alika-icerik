"""Generate deterministic, solvable Route Masters maze missions."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import deque
from pathlib import Path

from route_masters_language import THEMES


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "games" / "route-masters" / "missions"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = ("young", "mid", "teen", "senior")
SIZE = {"young": 5, "mid": 6, "teen": 7, "senior": 8}
ROTATABLE = {"young": 1, "mid": 2, "teen": 3, "senior": 4}
ALLOWANCE = {"young": 8, "mid": 6, "teen": 4, "senior": 2}
SOURCE = "https://www.smartgames.eu/uk/play-learn"
DIRS = ((0, -1, 1, 4), (1, 0, 2, 8), (0, 1, 4, 1), (-1, 0, 8, 2))


def _mission_id(language: str, band: str, number: int) -> str:
    raw = f"route-masters-v1:{language}:{band}:{number}".encode()
    return "rou_" + hashlib.sha256(raw).hexdigest()[:20]


def _maze(size: int, rng: random.Random, start: int) -> list[int]:
    openings = [0] * (size * size)
    visited = {start}
    stack = [start]
    while stack:
        current = stack[-1]
        x, y = current % size, current // size
        choices = []
        for dx, dy, bit, opposite in DIRS:
            nx, ny = x + dx, y + dy
            target = ny * size + nx
            if 0 <= nx < size and 0 <= ny < size and target not in visited:
                choices.append((target, bit, opposite))
        if not choices:
            stack.pop()
            continue
        target, bit, opposite = rng.choice(choices)
        openings[current] |= bit
        openings[target] |= opposite
        visited.add(target)
        stack.append(target)
    return openings


def _path_to_farthest(openings: list[int], size: int, start: int) -> tuple[list[int], int]:
    queue = deque([start])
    parent = {start: -1}
    distance = {start: 0}
    while queue:
        cell = queue.popleft()
        x, y = cell % size, cell // size
        for dx, dy, bit, _ in DIRS:
            if not openings[cell] & bit:
                continue
            nxt = (y + dy) * size + (x + dx)
            if nxt not in parent:
                parent[nxt] = cell
                distance[nxt] = distance[cell] + 1
                queue.append(nxt)
    goal = max(distance, key=lambda cell: (distance[cell], cell))
    path = []
    cell = goal
    while cell != -1:
        path.append(cell)
        cell = parent[cell]
    path.reverse()
    return path, distance[goal]


def _specials(band: str, path: list[int], openings: list[int], rng: random.Random) -> list[dict]:
    specials: list[dict] = [{"type": "bonus_star", "position": path[len(path) // 2]}]
    if band != "young":
        specials.extend([
            {"type": "key", "position": path[max(1, len(path) // 3)]},
            {"type": "gate", "position": path[min(len(path) - 2, 2 * len(path) // 3)]},
        ])
    if band in ("teen", "senior"):
        off_path = [cell for cell in range(len(openings)) if cell not in set(path)]
        if off_path:
            specials.append({"type": "energy_orb", "position": rng.choice(off_path)})
    if band == "senior":
        off_path = [cell for cell in range(len(openings))
                    if cell not in set(path) and cell not in {item["position"] for item in specials}]
        for cell in rng.sample(off_path, min(2, len(off_path))):
            specials.append({"type": "trap", "position": cell})
    return specials


def generate() -> None:
    for language in LANGUAGES:
        if len(THEMES[language]) != 5:
            raise ValueError(f"{language}: expected five cultural themes")
        for band in BANDS:
            size = SIZE[band]
            rows = []
            seen: set[tuple[int, ...]] = set()
            for number in range(200):
                corners = (0, size - 1, size * (size - 1), size * size - 1)
                start = corners[number % len(corners)]
                for attempt in range(100):
                    rng = random.Random(
                        f"alika-route-masters-v1:{language}:{band}:{number}:{attempt}"
                    )
                    openings = _maze(size, rng, start)
                    signature = tuple(openings)
                    if signature not in seen:
                        break
                else:
                    raise ValueError(f"{language}/{band}:{number + 1}: unique maze unavailable")
                seen.add(signature)
                path, optimal_moves = _path_to_farthest(openings, size, start)
                candidates = path[1:-1]
                count = ROTATABLE[band]
                if len(candidates) < count:
                    raise ValueError(f"{language}/{band}:{number + 1}: route too short")
                positions = sorted(rng.sample(candidates, count))
                rotatable = [{"position": position, "start_rotation": rng.choice((1, 2, 3)),
                              "solution_rotation": 0} for position in positions]
                rotation_moves = sum(min(item["start_rotation"], 4 - item["start_rotation"])
                                     for item in rotatable)
                theme = THEMES[language][number // 40]
                rows.append({
                    "mission_id": _mission_id(language, band, number + 1),
                    "board_size": size,
                    "openings": openings,
                    "start": start,
                    "goal": path[-1],
                    "rotatable_tiles": rotatable,
                    "specials": _specials(band, path, openings, rng),
                    "optimal_moves": optimal_moves,
                    "optimal_actions": optimal_moves + rotation_moves,
                    "move_limit": optimal_moves + rotation_moves + ALLOWANCE[band],
                    "hero": theme["hero"],
                    "setting": theme["setting"],
                    "treasure": theme["treasure"],
                    "difficulty": BANDS.index(band) + 1,
                    "source": {"title": "Official progressive logic-game principles", "url": SOURCE},
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
