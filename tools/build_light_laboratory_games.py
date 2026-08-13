"""Build deterministic data-only AliKa Light Laboratory packages."""
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
GAME_ROOT = ROOT / "games" / "light-laboratory"
PUZZLES = GAME_ROOT / "puzzles"
CATALOG = GAME_ROOT / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {"young": (5, 7), "mid": (8, 11), "teen": (12, 14), "senior": (15, 18)}
PROFILE = {
    "young": {"size": 5, "length": 6, "rotatable": 1, "filters": 0},
    "mid": {"size": 6, "length": 10, "rotatable": 2, "filters": 1},
    "teen": {"size": 7, "length": 14, "rotatable": 3, "filters": 2},
    "senior": {"size": 8, "length": 18, "rotatable": 4, "filters": 3},
}
EVENTS = {"golden_mirror", "energy_orb", "frozen_mirror", "portal_pair", "spectrum_burst"}
COLORS = {"red", "green", "blue"}
DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
PER_POOL = 200
NAMES = {
    "tr": "Işık Laboratuvarı", "en": "Light Laboratory", "de": "Lichtlabor",
    "es": "Laboratorio de luz", "fr": "Laboratoire de lumière", "pt": "Laboratório de luz",
    "ru": "Лаборатория света", "ja": "光の研究室", "ko": "빛 실험실",
}
SUBJECTS = {
    "tr": "Işık ve optik", "en": "Light and optics", "de": "Licht und Optik",
    "es": "Luz y óptica", "fr": "Lumière et optique", "pt": "Luz e óptica",
    "ru": "Свет и оптика", "ja": "光と光学", "ko": "빛과 광학",
}
RUNTIME_FIELDS = ("puzzle_id", "board_size", "emitter_cell", "emitter_direction",
                  "emitter_color", "target_cell", "target_color", "solution_path",
                  "elements", "energy_budget", "rotation_limit", "special_event",
                  "event_cells", "laboratory", "artifact", "difficulty")
CREATED_AT = "2026-08-14T00:00:00Z"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{2,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class LightLaboratoryBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def _direction(first: int, second: int, size: int) -> int | None:
    ax, ay, bx, by = first % size, first // size, second % size, second // size
    delta = (bx - ax, by - ay)
    return DIRS.index(delta) if delta in DIRS else None


def _orientation(incoming: int, outgoing: int) -> int | None:
    if (incoming, outgoing) in {(0, 1), (1, 0), (2, 3), (3, 2)}:
        return 0
    if (incoming, outgoing) in {(0, 3), (3, 0), (2, 1), (1, 2)}:
        return 1
    return None


def _trace_valid(row: dict[str, Any], profile: dict[str, int]) -> bool:
    size, path, elements = row.get("board_size"), row.get("solution_path"), row.get("elements")
    if (size != profile["size"] or not isinstance(path, list) or len(path) != profile["length"]
            or len(set(path)) != len(path) or not isinstance(elements, list)
            or any(not isinstance(cell, int) or not 0 <= cell < size * size for cell in path)):
        return False
    directions = [_direction(path[index], path[index + 1], size) for index in range(len(path) - 1)]
    if any(direction is None for direction in directions):
        return False
    if (row.get("emitter_cell") != path[0] or row.get("target_cell") != path[-1]
            or row.get("emitter_direction") != directions[0]
            or row.get("emitter_color") not in COLORS
            or row.get("target_color") != row.get("emitter_color")):
        return False
    by_cell: dict[int, dict[str, Any]] = {}
    rotatable = filters = 0
    for element in elements:
        if not isinstance(element, dict) or not isinstance(element.get("cell"), int):
            return False
        cell = element["cell"]
        if cell in by_cell or cell not in path[1:-1]:
            return False
        if element.get("type") == "mirror":
            index = path.index(cell)
            expected = _orientation(directions[index - 1], directions[index])
            if (expected is None or element.get("solution_orientation") != expected
                    or element.get("start_orientation") not in (0, 1)
                    or not isinstance(element.get("rotatable"), bool)):
                return False
            if element["rotatable"]:
                rotatable += 1
                if element["start_orientation"] == expected:
                    return False
            elif element["start_orientation"] != expected:
                return False
        elif element.get("type") == "filter":
            index = path.index(cell)
            if (directions[index - 1] != directions[index] or element.get("rotatable") is not False
                    or element.get("color") != row.get("emitter_color")):
                return False
            filters += 1
        else:
            return False
        by_cell[cell] = element
    for index in range(1, len(path) - 1):
        if directions[index - 1] != directions[index]:
            if path[index] not in by_cell or by_cell[path[index]].get("type") != "mirror":
                return False
    return rotatable == profile["rotatable"] and filters == profile["filters"]


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = PUZZLES / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LightLaboratoryBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PER_POOL:
        raise LightLaboratoryBuildError(f"{language}/{band}: expected {PER_POOL} puzzles, got {len(rows)}")
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
                or path_key in paths or not _trace_valid(row, profile)
                or not isinstance(row.get("energy_budget"), int)
                or row["energy_budget"] < profile["length"]
                or not isinstance(row.get("rotation_limit"), int)
                or row["rotation_limit"] < profile["rotatable"]
                or row.get("special_event") not in EVENTS
                or not isinstance(row.get("event_cells"), list) or len(row["event_cells"]) != 2
                or len(set(row["event_cells"])) != 2
                or any(cell not in solution_path[1:-1] for cell in row["event_cells"])
                or any(not isinstance(row.get(field), str) or not row[field].strip()
                       for field in ("laboratory", "artifact"))
                or row.get("difficulty") != expected_difficulty
                or not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://")
                or not isinstance(tags, list) or row.get("review_status") != "ai-draft"):
            raise LightLaboratoryBuildError(f"{language}/{band}:{index}: invalid light puzzle")
        cultural += any(str(tag).startswith(f"culture:{language}") for tag in tags)
        ids.add(puzzle_id)
        paths.add(path_key)
    if cultural != PER_POOL or {row["special_event"] for row in rows} != EVENTS:
        raise LightLaboratoryBuildError(f"{language}/{band}: cultural or event coverage is incomplete")
    if len({(row["laboratory"], row["artifact"]) for row in rows}) != 5:
        raise LightLaboratoryBuildError(f"{language}/{band}: expected five cultural laboratory themes")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    puzzles = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    extras = visual_payloads("light-laboratory", band)
    extras["data/gameplay.json"] = gameplay_config("light-laboratory", band)
    manifest = {
        "schema_version": 1,
        "game_id": str(uuid.uuid5(uuid.NAMESPACE_URL,
                                  f"https://alika.tr/games/light-laboratory/v1/{language}/{band}")),
        "game_version": 1, "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PER_POOL} ışık bulmacası",
        "game_type": "light_laboratory", "min_app_version": "1.1.24",
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
            relative = Path("games") / "light-laboratory" / "dist" / language / f"{band}.alika-game"
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
            raise LightLaboratoryBuildError("generated files are stale: " + ", ".join(stale))
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
    except LightLaboratoryBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
