"""Build deterministic data-only AliKa Route Masters packages."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import uuid
import zipfile
from collections import deque
from pathlib import Path
from typing import Any


TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
from game_visuals import asset_records, visual_payloads
from gameplay_designs import gameplay_config


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = ROOT / "games" / "route-masters"
MISSIONS = GAME_ROOT / "missions"
CATALOG = GAME_ROOT / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {"young": (5, 7), "mid": (8, 11), "teen": (12, 14), "senior": (15, 18)}
SIZE = {"young": 5, "mid": 6, "teen": 7, "senior": 8}
ROTATABLE = {"young": 1, "mid": 2, "teen": 3, "senior": 4}
PER_POOL = 200
NAMES = {
    "tr": "Rota Ustaları", "en": "Route Masters", "de": "Routenmeister",
    "es": "Maestros de la ruta", "fr": "Maîtres du parcours", "pt": "Mestres da rota",
    "ru": "Мастера маршрута", "ja": "ルートマスター", "ko": "경로의 달인",
}
SUBJECTS = {
    "tr": "Mantık ve yön bulma", "en": "Logic and navigation", "de": "Logik und Orientierung",
    "es": "Lógica y orientación", "fr": "Logique et orientation", "pt": "Lógica e orientação",
    "ru": "Логика и навигация", "ja": "論理と経路探索", "ko": "논리와 길 찾기",
}
RUNTIME_FIELDS = ("mission_id", "board_size", "openings", "start", "goal",
                  "rotatable_tiles", "specials", "optimal_moves", "optimal_actions",
                  "move_limit", "hero", "setting", "treasure", "difficulty")
CREATED_AT = "2026-08-14T00:00:00Z"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)
DIRS = ((0, -1, 1, 4), (1, 0, 2, 8), (0, 1, 4, 1), (-1, 0, 8, 2))


class RouteMastersBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def _distance(openings: list[int], size: int, start: int, goal: int) -> int | None:
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        cell, distance = queue.popleft()
        if cell == goal:
            return distance
        x, y = cell % size, cell // size
        for dx, dy, bit, opposite in DIRS:
            if not openings[cell] & bit:
                continue
            nx, ny = x + dx, y + dy
            if not (0 <= nx < size and 0 <= ny < size):
                return None
            nxt = ny * size + nx
            if not openings[nxt] & opposite:
                return None
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, distance + 1))
    return None


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = MISSIONS / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RouteMastersBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PER_POOL:
        raise RouteMastersBuildError(f"{language}/{band}: expected {PER_POOL} missions, got {len(rows)}")
    ids: set[str] = set()
    mazes: set[tuple[int, ...]] = set()
    cultural = 0
    expected_difficulty = tuple(BANDS).index(band) + 1
    for index, row in enumerate(rows, 1):
        mission_id = row.get("mission_id")
        size, openings = row.get("board_size"), row.get("openings")
        start, goal = row.get("start"), row.get("goal")
        rotatable, specials = row.get("rotatable_tiles"), row.get("specials")
        source, tags = row.get("source"), row.get("culture_tags")
        distance = (_distance(openings, size, start, goal)
                    if isinstance(size, int) and isinstance(openings, list)
                    and isinstance(start, int) and isinstance(goal, int) else None)
        maze_key = tuple(openings) if isinstance(openings, list) else ()
        valid_rotations = (isinstance(rotatable, list) and len(rotatable) == ROTATABLE[band]
                           and len({item.get("position") for item in rotatable
                                    if isinstance(item, dict)}) == len(rotatable)
                           and all(isinstance(item, dict)
                                   and isinstance(item.get("position"), int)
                                   and 0 <= item["position"] < size * size
                                   and item.get("start_rotation") in (1, 2, 3)
                                   and item.get("solution_rotation") == 0 for item in rotatable))
        if (not isinstance(mission_id, str) or not ID_RE.fullmatch(mission_id) or mission_id in ids
                or size != SIZE[band] or len(openings) != size * size
                or any(not isinstance(mask, int) or not 0 <= mask <= 15 for mask in openings)
                or maze_key in mazes or distance is None or distance != row.get("optimal_moves")
                or not valid_rotations or not isinstance(specials, list) or not specials
                or any(not isinstance(item, dict) or item.get("type") not in
                       {"bonus_star", "key", "gate", "energy_orb", "trap"}
                       or not isinstance(item.get("position"), int)
                       or not 0 <= item["position"] < size * size for item in specials)
                or not isinstance(row.get("optimal_actions"), int)
                or row["optimal_actions"] < distance or row.get("move_limit", 0) < row["optimal_actions"]
                or any(not isinstance(row.get(field), str) or not row[field].strip()
                       for field in ("hero", "setting", "treasure"))
                or row.get("difficulty") != expected_difficulty
                or not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://")
                or not isinstance(tags, list) or row.get("review_status") != "ai-draft"):
            raise RouteMastersBuildError(f"{language}/{band}:{index}: invalid mission")
        cultural += any(str(tag).startswith(f"culture:{language}") for tag in tags)
        ids.add(mission_id)
        mazes.add(maze_key)
    if cultural != PER_POOL:
        raise RouteMastersBuildError(f"{language}/{band}: all missions must be culture-local")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    missions = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    extras = visual_payloads("route-masters", band)
    extras["data/gameplay.json"] = gameplay_config("route-masters", band)
    manifest = {
        "schema_version": 1,
        "game_id": str(uuid.uuid5(uuid.NAMESPACE_URL,
                                  f"https://alika.tr/games/route-masters/v1/{language}/{band}")),
        "game_version": 1, "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PER_POOL} bölüm",
        "game_type": "route_masters", "min_app_version": "1.1.24",
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
            relative = Path("games") / "route-masters" / "dist" / language / f"{band}.alika-game"
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
            raise RouteMastersBuildError("generated files are stale: " + ", ".join(stale))
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
    except RouteMastersBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
