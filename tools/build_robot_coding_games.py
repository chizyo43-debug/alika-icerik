"""Build deterministic data-only AliKa Robot Coding Arena packages."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import uuid
import zipfile
from pathlib import Path
from typing import Any


TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
from game_visuals import asset_records, visual_payloads
from gameplay_designs import gameplay_config


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = ROOT / "games" / "robot-coding-arena"
PUZZLES = GAME_ROOT / "puzzles"
CATALOG = GAME_ROOT / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {"young": (5, 7), "mid": (8, 11), "teen": (12, 14), "senior": (15, 18)}
PROFILE = {
    "young": {"size": 5, "length": 6, "loops": 0, "conditions": 0, "obstacles": 3},
    "mid": {"size": 6, "length": 9, "loops": 1, "conditions": 0, "obstacles": 5},
    "teen": {"size": 7, "length": 13, "loops": 2, "conditions": 1, "obstacles": 7},
    "senior": {"size": 8, "length": 17, "loops": 3, "conditions": 2, "obstacles": 10},
}
EVENTS = {"turbo_lane", "magnetic_storm", "golden_battery", "portal_pair", "debug_glitch"}
COLORS = {"cyan", "violet", "coral"}
DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
PER_POOL = 200
NAMES = {
    "tr": "Robot Kodlama Arenası", "en": "Robot Coding Arena", "de": "Roboter-Code-Arena",
    "es": "Arena de programación robótica", "fr": "Arène de programmation robotique",
    "pt": "Arena de programação robótica", "ru": "Арена программирования роботов",
    "ja": "ロボット・コーディング・アリーナ", "ko": "로봇 코딩 아레나",
}
SUBJECTS = {
    "tr": "Kodlama ve algoritma", "en": "Coding and algorithms",
    "de": "Programmieren und Algorithmen", "es": "Programación y algoritmos",
    "fr": "Programmation et algorithmes", "pt": "Programação e algoritmos",
    "ru": "Программирование и алгоритмы", "ja": "プログラミングとアルゴリズム",
    "ko": "코딩과 알고리즘",
}
RUNTIME_FIELDS = ("puzzle_id", "board_size", "start_cell", "start_direction", "target_cell",
                  "solution_path", "solution_program", "obstacles", "sensor_gates",
                  "optimal_blocks", "command_budget", "special_event", "event_cells",
                  "arena", "mission_item", "difficulty")
CREATED_AT = "2026-08-14T00:00:00Z"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{2,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class RobotCodingBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def _move(cell: int, direction: int, size: int) -> int | None:
    x, y = cell % size, cell // size
    dx, dy = DIRS[direction]
    x, y = x + dx, y + dy
    return y * size + x if 0 <= x < size and 0 <= y < size else None


def _run_program(row: dict[str, Any], profile: dict[str, int]) -> tuple[list[int], int, int] | None:
    size = row.get("board_size")
    program = row.get("solution_program")
    obstacles = row.get("obstacles")
    gates = row.get("sensor_gates")
    if (size != profile["size"] or not isinstance(program, list) or not program
            or not isinstance(obstacles, list) or not isinstance(gates, list)):
        return None
    if (len(obstacles) != profile["obstacles"] or len(set(obstacles)) != len(obstacles)
            or any(not isinstance(cell, int) or not 0 <= cell < size * size for cell in obstacles)):
        return None
    gate_map = {}
    for gate in gates:
        if (not isinstance(gate, dict) or set(gate) != {"cell", "color"}
                or not isinstance(gate.get("cell"), int) or gate.get("color") not in COLORS
                or gate["cell"] in gate_map or not 0 <= gate["cell"] < size * size):
            return None
        gate_map[gate["cell"]] = gate["color"]
    cell = row.get("start_cell")
    direction = row.get("start_direction")
    if not isinstance(cell, int) or not 0 <= cell < size * size or direction not in range(4):
        return None
    route = [cell]
    loop_count = condition_count = 0

    def execute(blocks: list[dict[str, Any]], *, nested: bool = False) -> bool:
        nonlocal cell, direction, loop_count, condition_count
        for block in blocks:
            if not isinstance(block, dict) or not isinstance(block.get("op"), str):
                return False
            op = block["op"]
            if op == "forward" and set(block) == {"op"}:
                nxt = _move(cell, direction, size)
                if nxt is None or nxt in obstacles:
                    return False
                cell = nxt
                route.append(cell)
            elif op in {"turn_left", "turn_right"} and set(block) == {"op"}:
                direction = (direction + (1 if op == "turn_right" else -1)) % 4
            elif op == "repeat" and not nested:
                if (set(block) != {"op", "count", "body"} or not isinstance(block["count"], int)
                        or not 2 <= block["count"] <= size
                        or block["body"] != [{"op": "forward"}]):
                    return False
                loop_count += 1
                for _ in range(block["count"]):
                    if not execute(block["body"], nested=True):
                        return False
            elif op == "if_tile" and not nested:
                if (set(block) != {"op", "tile", "then"} or block.get("tile") not in COLORS
                        or block.get("then") != [{"op": "forward"}]):
                    return False
                nxt = _move(cell, direction, size)
                if nxt is None or gate_map.get(nxt) != block["tile"]:
                    return False
                condition_count += 1
                if not execute(block["then"], nested=True):
                    return False
            else:
                return False
        return True

    if not execute(program):
        return None
    return route, loop_count, condition_count


def _program_valid(row: dict[str, Any], profile: dict[str, int]) -> bool:
    result = _run_program(row, profile)
    path = row.get("solution_path")
    if (result is None or not isinstance(path, list) or len(path) != profile["length"]
            or len(set(path)) != len(path) or result[0] != path
            or row.get("target_cell") != path[-1] or row.get("start_cell") != path[0]
            or result[1] != profile["loops"] or result[2] != profile["conditions"]):
        return False
    obstacles = row["obstacles"]
    gates = row["sensor_gates"]
    if (any(cell in path for cell in obstacles) or len(gates) != profile["conditions"]
            or any(gate["cell"] not in path[1:-1] for gate in gates)
            or not isinstance(row.get("optimal_blocks"), int)
            or row["optimal_blocks"] != len(row["solution_program"])
            or not isinstance(row.get("command_budget"), int)
            or row["command_budget"] < row["optimal_blocks"]):
        return False
    return True


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = PUZZLES / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RobotCodingBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PER_POOL:
        raise RobotCodingBuildError(f"{language}/{band}: expected {PER_POOL} puzzles, got {len(rows)}")
    ids: set[str] = set()
    paths: set[tuple[int, ...]] = set()
    cultural = 0
    profile = PROFILE[band]
    expected_difficulty = tuple(BANDS).index(band) + 1
    for index, row in enumerate(rows, 1):
        puzzle_id = row.get("puzzle_id")
        solution_path = row.get("solution_path")
        path_key = tuple(solution_path) if isinstance(solution_path, list) else ()
        source, tags = row.get("source"), row.get("culture_tags")
        if (not isinstance(puzzle_id, str) or not ID_RE.fullmatch(puzzle_id) or puzzle_id in ids
                or path_key in paths or not _program_valid(row, profile)
                or row.get("special_event") not in EVENTS
                or not isinstance(row.get("event_cells"), list) or len(row["event_cells"]) != 2
                or len(set(row["event_cells"])) != 2
                or any(cell not in solution_path[1:-1] for cell in row["event_cells"])
                or any(not isinstance(row.get(field), str) or not row[field].strip()
                       for field in ("arena", "mission_item"))
                or row.get("difficulty") != expected_difficulty
                or not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://")
                or not isinstance(tags, list) or row.get("review_status") != "ai-draft"):
            raise RobotCodingBuildError(f"{language}/{band}:{index}: invalid robot program")
        cultural += any(str(tag).startswith(f"culture:{language}") for tag in tags)
        ids.add(puzzle_id)
        paths.add(path_key)
    if cultural != PER_POOL or {row["special_event"] for row in rows} != EVENTS:
        raise RobotCodingBuildError(f"{language}/{band}: cultural or event coverage is incomplete")
    if len({(row["arena"], row["mission_item"]) for row in rows}) != 5:
        raise RobotCodingBuildError(f"{language}/{band}: expected five cultural mission themes")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    puzzles = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    extras = visual_payloads("robot-coding-arena", band)
    extras["data/gameplay.json"] = gameplay_config("robot-coding-arena", band)
    manifest = {
        "schema_version": 1,
        "game_id": str(uuid.uuid5(uuid.NAMESPACE_URL,
                                  f"https://alika.tr/games/robot-coding-arena/v1/{language}/{band}")),
        "game_version": 1, "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PER_POOL} kodlama görevi",
        "game_type": "robot_coding", "min_app_version": "1.1.24",
        "min_players": 1, "max_players": 8, "age_min": age_min, "age_max": age_max,
        "subject": SUBJECTS[language], "topic": f"{age_min}–{age_max}", "language": language,
        "license": "CC-BY-NC-4.0", "author": "AliKa Atölye",
        "assets": ([{"path": "data/puzzles.json", "sha256": hashlib.sha256(puzzles).hexdigest(),
                     "asset_type": "puzzles", "size_bytes": len(puzzles)}] + asset_records(extras)),
        "total_size_bytes": len(puzzles) + sum(map(len, extras.values())), "created_at": CREATED_AT,
    }
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_STORED) as archive:
        for name, payload in (("manifest.json", _json_bytes(manifest)),
                              ("data/puzzles.json", puzzles), *extras.items()):
            info = zipfile.ZipInfo(name, ZIP_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, payload, compress_type=zipfile.ZIP_STORED)
    return output.getvalue(), manifest


def build(*, check: bool) -> None:
    outputs: dict[Path, bytes] = {}
    entries = []
    for language in LANGUAGES:
        for band in BANDS:
            rows = _load_pool(language, band)
            payload, manifest = _package(language, band, rows)
            relative = Path("games") / "robot-coding-arena" / "dist" / language / f"{band}.alika-game"
            outputs[ROOT / relative] = payload
            entries.append({"path": relative.as_posix(), "sha256": hashlib.sha256(payload).hexdigest(),
                            "size_bytes": len(payload), "puzzle_count": len(rows),
                            "game_id": manifest["game_id"], "game_version": 1,
                            "language": language, "age_min": manifest["age_min"],
                            "age_max": manifest["age_max"], "name": manifest["name"]})
    outputs[CATALOG] = _json_bytes({"schema_version": 1, "generated_at": CREATED_AT,
                                    "review_status": "ai-draft", "human_approved": False,
                                    "games": entries})
    if check:
        stale = [path.relative_to(ROOT).as_posix() for path, data in outputs.items()
                 if not path.is_file() or (path.read_bytes().replace(b"\r\n", b"\n") != data
                                           if path.suffix == ".json" else path.read_bytes() != data)]
        if stale:
            raise RobotCodingBuildError("generated files are stale: " + ", ".join(stale))
        return
    for path, data in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        build(check=args.check)
    except RobotCodingBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
