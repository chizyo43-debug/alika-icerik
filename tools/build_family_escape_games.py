"""Build deterministic data-only AliKa Family Escape Night packages."""
from __future__ import annotations

import argparse
import hashlib
import io
import itertools
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
GAME_ROOT = ROOT / "games" / "family-escape-night"
PUZZLES = GAME_ROOT / "puzzles"
CATALOG = GAME_ROOT / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {"young": (5, 7), "mid": (8, 11), "teen": (12, 14), "senior": (15, 18)}
PROFILE = {
    "young": {"symbols": 3, "clues": 3, "hints": 4,
              "types": {"position", "before", "adjacent"}},
    "mid": {"symbols": 4, "clues": 4, "hints": 3,
            "types": {"position", "before", "adjacent", "not_position"}},
    "teen": {"symbols": 5, "clues": 5, "hints": 2,
             "types": {"position", "before", "adjacent", "not_position", "distance"}},
    "senior": {"symbols": 6, "clues": 6, "hints": 2,
               "types": {"position", "before", "adjacent", "not_position", "distance", "between"}},
}
SYMBOLS = {"star", "diamond", "clover", "drop", "moon", "sun"}
EVENTS = {"secret_drawer", "golden_hint", "key_rain", "echo_clue", "moving_portrait"}
PER_POOL = 200
NAMES = {
    "tr": "Aile Kaçış Gecesi", "en": "Family Escape Night", "de": "Familien-Rätselnacht",
    "es": "Noche de escape familiar", "fr": "Soirée d'évasion en famille",
    "pt": "Noite de fuga em família", "ru": "Семейный вечер загадок",
    "ja": "ファミリー脱出ナイト", "ko": "가족 탈출의 밤",
}
SUBJECTS = {
    "tr": "İş birliği ve mantık", "en": "Cooperation and logic",
    "de": "Zusammenarbeit und Logik", "es": "Cooperación y lógica",
    "fr": "Coopération et logique", "pt": "Cooperação e lógica",
    "ru": "Сотрудничество и логика", "ja": "協力と論理", "ko": "협동과 논리",
}
RUNTIME_FIELDS = ("puzzle_id", "symbols", "clues", "solution_code", "hint_tokens",
                  "role_count", "special_event", "room", "treasure", "difficulty")
CREATED_AT = "2026-08-14T00:00:00Z"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{2,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class FamilyEscapeBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def _clue_valid(clue: Any, symbols: set[str], profile: dict[str, Any]) -> bool:
    if not isinstance(clue, dict) or clue.get("type") not in profile["types"]:
        return False
    kind = clue["type"]
    expected = {
        "position": {"type", "symbol", "position"},
        "not_position": {"type", "symbol", "position"},
        "before": {"type", "first", "second"},
        "adjacent": {"type", "first", "second"},
        "distance": {"type", "first", "second", "distance"},
        "between": {"type", "left", "middle", "right"},
    }[kind]
    if set(clue) != expected:
        return False
    referenced = [value for key, value in clue.items()
                  if key not in {"type", "position", "distance"}]
    if any(value not in symbols for value in referenced) or len(set(referenced)) != len(referenced):
        return False
    if "position" in clue and (not isinstance(clue["position"], int)
                               or not 0 <= clue["position"] < profile["symbols"]):
        return False
    if "distance" in clue and (not isinstance(clue["distance"], int)
                               or not 1 <= clue["distance"] < profile["symbols"]):
        return False
    return True


def _matches(code: tuple[str, ...], clue: dict[str, Any]) -> bool:
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


def _solutions(row: dict[str, Any], profile: dict[str, Any]) -> list[tuple[str, ...]] | None:
    symbols, clues = row.get("symbols"), row.get("clues")
    if (not isinstance(symbols, list) or len(symbols) != profile["symbols"]
            or len(set(symbols)) != len(symbols) or not set(symbols) <= SYMBOLS
            or not isinstance(clues, list) or len(clues) != profile["clues"]
            or len({json.dumps(clue, sort_keys=True) for clue in clues}) != len(clues)
            or not all(_clue_valid(clue, set(symbols), profile) for clue in clues)):
        return None
    return [code for code in itertools.permutations(symbols)
            if all(_matches(code, clue) for clue in clues)]


def _puzzle_valid(row: dict[str, Any], profile: dict[str, Any]) -> bool:
    matches = _solutions(row, profile)
    solution = row.get("solution_code")
    return (matches is not None and len(matches) == 1 and isinstance(solution, list)
            and tuple(solution) == matches[0] and set(solution) == set(row["symbols"])
            and row.get("hint_tokens") == profile["hints"] and row.get("role_count") == 4)


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = PUZZLES / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FamilyEscapeBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PER_POOL:
        raise FamilyEscapeBuildError(f"{language}/{band}: expected {PER_POOL} puzzles, got {len(rows)}")
    ids, signatures = set(), set()
    profile = PROFILE[band]
    cultural = 0
    for index, row in enumerate(rows, 1):
        puzzle_id = row.get("puzzle_id")
        signature = (tuple(row.get("symbols", [])), json.dumps(row.get("clues"), sort_keys=True))
        source, tags = row.get("source"), row.get("culture_tags")
        if (not isinstance(puzzle_id, str) or not ID_RE.fullmatch(puzzle_id) or puzzle_id in ids
                or signature in signatures or not _puzzle_valid(row, profile)
                or row.get("special_event") not in EVENTS
                or any(not isinstance(row.get(field), str) or not row[field].strip()
                       for field in ("room", "treasure"))
                or row.get("difficulty") != tuple(BANDS).index(band) + 1
                or not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://")
                or not isinstance(tags, list) or row.get("review_status") != "ai-draft"):
            raise FamilyEscapeBuildError(f"{language}/{band}:{index}: invalid escape mystery")
        cultural += any(str(tag).startswith(f"culture:{language}") for tag in tags)
        ids.add(puzzle_id)
        signatures.add(signature)
    if cultural != PER_POOL or {row["special_event"] for row in rows} != EVENTS:
        raise FamilyEscapeBuildError(f"{language}/{band}: cultural or event coverage is incomplete")
    if len({(row["room"], row["treasure"]) for row in rows}) != 5:
        raise FamilyEscapeBuildError(f"{language}/{band}: expected five local escape rooms")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    puzzles = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    extras = visual_payloads("family-escape-night", band)
    extras["data/gameplay.json"] = gameplay_config("family-escape-night", band)
    manifest = {
        "schema_version": 1,
        "game_id": str(uuid.uuid5(uuid.NAMESPACE_URL,
                                  f"https://alika.tr/games/family-escape-night/v1/{language}/{band}")),
        "game_version": 1, "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PER_POOL} ortak kaçış macerası",
        "game_type": "family_escape", "min_app_version": "1.1.24",
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
            relative = Path("games") / "family-escape-night" / "dist" / language / f"{band}.alika-game"
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
            raise FamilyEscapeBuildError("generated files are stale: " + ", ".join(stale))
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
    except FamilyEscapeBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
