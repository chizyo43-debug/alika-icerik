"""Generate deterministic, executable Robot Coding Arena puzzles."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

from robot_coding_language import THEMES


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "games" / "robot-coding-arena" / "puzzles"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = ("young", "mid", "teen", "senior")
EVENTS = ("turbo_lane", "magnetic_storm", "golden_battery", "portal_pair", "debug_glitch")
COLORS = ("cyan", "violet", "coral")
DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
PROFILES = {
    "young": {"size": 5, "length": 6, "loops": 0, "conditions": 0, "obstacles": 3, "allowance": 4},
    "mid": {"size": 6, "length": 9, "loops": 1, "conditions": 0, "obstacles": 5, "allowance": 3},
    "teen": {"size": 7, "length": 13, "loops": 2, "conditions": 1, "obstacles": 7, "allowance": 2},
    "senior": {"size": 8, "length": 17, "loops": 3, "conditions": 2, "obstacles": 10, "allowance": 1},
}
SOURCE = "https://code.org/curriculum/course2/6/Teacher"


def _id(language: str, band: str, number: int) -> str:
    raw = f"robot-coding-arena-v1:{language}:{band}:{number}".encode()
    return "rob_" + hashlib.sha256(raw).hexdigest()[:20]


def _direction(first: int, second: int, size: int) -> int:
    ax, ay, bx, by = first % size, first // size, second % size, second // size
    return DIRS.index((bx - ax, by - ay))


def _path(size: int, length: int, rng: random.Random) -> list[int]:
    for _ in range(2000):
        cells = [rng.randrange(size) * size]
        direction = 1
        while len(cells) < length:
            choices = []
            for candidate in (direction, (direction - 1) % 4, (direction + 1) % 4):
                dx, dy = DIRS[candidate]
                x, y = cells[-1] % size + dx, cells[-1] // size + dy
                nxt = y * size + x
                if 0 <= x < size and 0 <= y < size and nxt not in cells:
                    choices.append((candidate, nxt))
            if not choices:
                break
            direction, nxt = rng.choice(choices)
            cells.append(nxt)
        if len(cells) == length:
            return cells
    raise ValueError("robot route unavailable")


def _segments(path: list[int], size: int) -> list[tuple[int, int, int]]:
    directions = [_direction(path[index], path[index + 1], size)
                  for index in range(len(path) - 1)]
    result = []
    start = 0
    for index in range(1, len(directions) + 1):
        if index == len(directions) or directions[index] != directions[start]:
            result.append((start, index, directions[start]))
            start = index
    return result


def _compile(path: list[int], profile: dict[str, int], rng: random.Random):
    segments = _segments(path, profile["size"])
    repeatable = [index for index, (start, end, _) in enumerate(segments) if end - start >= 2]
    if len(repeatable) < profile["loops"]:
        return None
    loop_segments = set(rng.sample(repeatable, profile["loops"]))
    condition_moves = [move for segment_index, (start, end, _) in enumerate(segments)
                       if segment_index not in loop_segments
                       for move in range(start, end) if move < len(path) - 2]
    if len(condition_moves) < profile["conditions"]:
        return None
    chosen_conditions = set(rng.sample(condition_moves, profile["conditions"]))
    condition_colors = {move: rng.choice(COLORS) for move in chosen_conditions}
    program = []
    gates = []
    previous_direction = segments[0][2]
    for segment_index, (start, end, direction) in enumerate(segments):
        if segment_index:
            turn = (direction - previous_direction) % 4
            if turn not in (1, 3):
                return None
            program.append({"op": "turn_right" if turn == 1 else "turn_left"})
        if segment_index in loop_segments:
            program.append({"op": "repeat", "count": end - start,
                            "body": [{"op": "forward"}]})
        else:
            for move in range(start, end):
                if move in chosen_conditions:
                    color = condition_colors[move]
                    program.append({"op": "if_tile", "tile": color,
                                    "then": [{"op": "forward"}]})
                    gates.append({"cell": path[move + 1], "color": color})
                else:
                    program.append({"op": "forward"})
        previous_direction = direction
    return program, gates, segments[0][2]


def generate() -> None:
    for language in LANGUAGES:
        if len(THEMES[language]) != 5:
            raise ValueError(f"{language}: expected five local coding themes")
        for band in BANDS:
            profile = PROFILES[band]
            rows = []
            seen: set[tuple[int, ...]] = set()
            for number in range(200):
                for attempt in range(500):
                    rng = random.Random(f"alika-robot-code-v1:{language}:{band}:{number}:{attempt}")
                    path = _path(profile["size"], profile["length"], rng)
                    compiled = _compile(path, profile, rng)
                    if tuple(path) not in seen and compiled is not None:
                        break
                else:
                    raise ValueError(f"{language}/{band}:{number + 1}: unique program unavailable")
                seen.add(tuple(path))
                program, gates, start_direction = compiled
                free_cells = [cell for cell in range(profile["size"] ** 2) if cell not in path]
                obstacles = sorted(rng.sample(free_cells, profile["obstacles"]))
                theme = THEMES[language][number // 40]
                rows.append({
                    "puzzle_id": _id(language, band, number + 1),
                    "board_size": profile["size"], "start_cell": path[0],
                    "start_direction": start_direction, "target_cell": path[-1],
                    "solution_path": path, "solution_program": program,
                    "obstacles": obstacles, "sensor_gates": gates,
                    "optimal_blocks": len(program),
                    "command_budget": len(program) + profile["allowance"],
                    "special_event": EVENTS[number % len(EVENTS)],
                    "event_cells": sorted(rng.sample(path[1:-1], 2)),
                    "arena": theme["arena"], "mission_item": theme["mission_item"],
                    "difficulty": BANDS.index(band) + 1,
                    "source": {"title": "Code.org Maze: sequencing and loops", "url": SOURCE},
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
