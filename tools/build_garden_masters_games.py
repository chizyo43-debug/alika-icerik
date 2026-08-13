"""Build deterministic data-only AliKa Garden Masters packages."""
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
GAME_ROOT = ROOT / "games" / "garden-masters"
MISSIONS = GAME_ROOT / "missions"
CATALOG = GAME_ROOT / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {"young": (5, 7), "mid": (8, 11), "teen": (12, 14), "senior": (15, 18)}
PROFILE = {
    "young": {"size": 3, "plants": 4, "turns": 10},
    "mid": {"size": 4, "plants": 6, "turns": 12},
    "teen": {"size": 5, "plants": 8, "turns": 14},
    "senior": {"size": 6, "plants": 10, "turns": 16},
}
EVENTS = {"gentle_rain", "golden_bee", "compost_boost", "shade_cloud", "wind_breeze"}
KINDS = {"fruiting", "herb", "flower", "leafy", "root"}
SOILS = {"loam", "sand", "clay"}
PER_POOL = 200
NAMES = {
    "tr": "Bahçe Ustaları", "en": "Garden Masters", "de": "Gartenmeister",
    "es": "Maestros del jardín", "fr": "Maîtres du jardin", "pt": "Mestres do jardim",
    "ru": "Мастера сада", "ja": "ガーデンマスター", "ko": "정원의 달인",
}
SUBJECTS = {
    "tr": "Bahçe planlama ve ekosistem", "en": "Garden planning and ecosystems",
    "de": "Gartenplanung und Ökosysteme", "es": "Planificación del jardín y ecosistemas",
    "fr": "Planification du jardin et écosystèmes", "pt": "Planejamento do jardim e ecossistemas",
    "ru": "Планирование сада и экосистемы", "ja": "庭づくりと生態系", "ko": "정원 계획과 생태계",
}
RUNTIME_FIELDS = ("mission_id", "board_size", "cells", "plants", "solution",
                  "water_budget", "turn_limit", "target_score", "special_event",
                  "event_cells", "garden", "garden_style", "difficulty")
CREATED_AT = "2026-08-14T00:00:00Z"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{2,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class GardenMastersBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def _neighbors(position: int, size: int) -> set[int]:
    x, y = position % size, position // size
    return {ny * size + nx for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
            if 0 <= nx < size and 0 <= ny < size}


def _score(plants: list[dict], cells: list[dict], placements: list[dict], size: int,
           event: str, event_cells: list[int]) -> int | None:
    try:
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
    except (KeyError, TypeError, IndexError):
        return None


def _valid_layout(row: dict[str, Any], profile: dict[str, int]) -> bool:
    size, cells, plants, solution = (row.get("board_size"), row.get("cells"),
                                     row.get("plants"), row.get("solution"))
    if (size != profile["size"] or not isinstance(cells, list) or len(cells) != size * size
            or not isinstance(plants, list) or len(plants) != profile["plants"]
            or not isinstance(solution, list) or len(solution) != len(plants)):
        return False
    if any(not isinstance(cell, dict) or cell.get("cell") != index
           or cell.get("sun") not in (1, 2, 3) or cell.get("moisture") not in (1, 2, 3)
           or cell.get("soil") not in SOILS for index, cell in enumerate(cells)):
        return False
    ids: set[str] = set()
    for plant in plants:
        plant_id = plant.get("plant_id") if isinstance(plant, dict) else None
        if (not isinstance(plant_id, str) or not ID_RE.fullmatch(plant_id) or plant_id in ids
                or not isinstance(plant.get("name"), str) or not plant["name"].strip()
                or plant.get("kind") not in KINDS or plant.get("sun_need") not in (1, 2, 3)
                or plant.get("moisture_need") not in (1, 2, 3)
                or plant.get("water_cost") not in (1, 2, 3)
                or not isinstance(plant.get("harvest_points"), int)
                or not 1 <= plant["harvest_points"] <= 5
                or not isinstance(plant.get("pollinator_friendly"), bool)):
            return False
        ids.add(plant_id)
    placed_ids, positions = set(), set()
    for placement in solution:
        if not isinstance(placement, dict):
            return False
        plant_id, cell = placement.get("plant_id"), placement.get("cell")
        if (plant_id not in ids or plant_id in placed_ids or not isinstance(cell, int)
                or not 0 <= cell < size * size or cell in positions):
            return False
        placed_ids.add(plant_id)
        positions.add(cell)
    return placed_ids == ids


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = MISSIONS / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GardenMastersBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PER_POOL:
        raise GardenMastersBuildError(f"{language}/{band}: expected {PER_POOL} missions, got {len(rows)}")
    ids: set[str] = set()
    signatures: set[str] = set()
    cultural = 0
    profile = PROFILE[band]
    expected_difficulty = tuple(BANDS).index(band) + 1
    for index, row in enumerate(rows, 1):
        mission_id = row.get("mission_id")
        source, tags = row.get("source"), row.get("culture_tags")
        signature = json.dumps({"cells": row.get("cells"), "plants": row.get("plants"),
                                "solution": row.get("solution")}, sort_keys=True,
                               ensure_ascii=False, separators=(",", ":"))
        calculated = (_score(row.get("plants"), row.get("cells"), row.get("solution"),
                             row.get("board_size"), row.get("special_event"), row.get("event_cells"))
                      if _valid_layout(row, profile) and isinstance(row.get("event_cells"), list) else None)
        if (not isinstance(mission_id, str) or not ID_RE.fullmatch(mission_id) or mission_id in ids
                or signature in signatures or not _valid_layout(row, profile)
                or row.get("turn_limit") != profile["turns"]
                or not isinstance(row.get("water_budget"), int)
                or row["water_budget"] < sum(plant["water_cost"] for plant in row["plants"])
                or row.get("special_event") not in EVENTS
                or not isinstance(row.get("event_cells"), list) or not row["event_cells"]
                or len(set(row["event_cells"])) != len(row["event_cells"])
                or any(not isinstance(cell, int) or not 0 <= cell < profile["size"] ** 2
                       for cell in row["event_cells"])
                or calculated is None or row.get("target_score") != calculated
                or any(not isinstance(row.get(field), str) or not row[field].strip()
                       for field in ("garden", "garden_style"))
                or row.get("difficulty") != expected_difficulty
                or not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://")
                or not isinstance(tags, list) or row.get("review_status") != "ai-draft"):
            raise GardenMastersBuildError(f"{language}/{band}:{index}: invalid garden mission")
        cultural += any(str(tag).startswith(f"culture:{language}") for tag in tags)
        ids.add(mission_id)
        signatures.add(signature)
    if cultural != PER_POOL or {row["special_event"] for row in rows} != EVENTS:
        raise GardenMastersBuildError(f"{language}/{band}: cultural or event coverage is incomplete")
    if len({(row["garden"], row["garden_style"]) for row in rows}) != 5:
        raise GardenMastersBuildError(f"{language}/{band}: expected five cultural garden kits")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    missions = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    extras = visual_payloads("garden-masters", band)
    extras["data/gameplay.json"] = gameplay_config("garden-masters", band)
    manifest = {
        "schema_version": 1,
        "game_id": str(uuid.uuid5(uuid.NAMESPACE_URL,
                                  f"https://alika.tr/games/garden-masters/v1/{language}/{band}")),
        "game_version": 1, "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PER_POOL} bahçe görevi",
        "game_type": "garden_masters", "min_app_version": "1.1.24",
        "min_players": 1, "max_players": 8, "age_min": age_min, "age_max": age_max,
        "subject": SUBJECTS[language], "topic": f"{age_min}–{age_max}", "language": language,
        "license": "CC-BY-NC-4.0", "author": "AliKa Atölye",
        "assets": ([{"path": "data/missions.json", "sha256": hashlib.sha256(missions).hexdigest(),
                     "asset_type": "missions", "size_bytes": len(missions)}] + asset_records(extras)),
        "total_size_bytes": len(missions) + sum(map(len, extras.values())), "created_at": CREATED_AT,
    }
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_STORED) as archive:
        for name, payload in (("manifest.json", _json_bytes(manifest)),
                              ("data/missions.json", missions), *extras.items()):
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
            relative = Path("games") / "garden-masters" / "dist" / language / f"{band}.alika-game"
            outputs[ROOT / relative] = payload
            entries.append({"path": relative.as_posix(), "sha256": hashlib.sha256(payload).hexdigest(),
                            "size_bytes": len(payload), "mission_count": len(rows),
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
            raise GardenMastersBuildError("generated files are stale: " + ", ".join(stale))
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
    except GardenMastersBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
