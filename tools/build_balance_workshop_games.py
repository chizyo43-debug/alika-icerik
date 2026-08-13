"""Build deterministic data-only AliKa Balance Workshop packages."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
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
GAME_ROOT = ROOT / "games" / "balance-workshop"
CHALLENGES = GAME_ROOT / "challenges"
CATALOG = GAME_ROOT / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {"young": (5, 7), "mid": (8, 11), "teen": (12, 14), "senior": (15, 18)}
PROFILE = {
    "young": {"pieces": 5, "base": 8.0, "tilt": 10.0, "stability": 3},
    "mid": {"pieces": 7, "base": 7.0, "tilt": 8.0, "stability": 4},
    "teen": {"pieces": 9, "base": 6.0, "tilt": 6.0, "stability": 5},
    "senior": {"pieces": 11, "base": 5.2, "tilt": 4.0, "stability": 6},
}
SHAPES = {"beam", "arch", "triangle", "cylinder", "counterweight", "wedge"}
FEATURES = {"normal", "fragile", "golden", "magnetic"}
EVENTS = {"golden_anchor", "wind_gust", "moving_platform", "magnetic_lock", "earthquake_wave"}
STRUCTURES = {"tower", "bridge", "balance_beam", "arch", "cantilever"}
PER_POOL = 200
NAMES = {
    "tr": "Denge Atölyesi", "en": "Balance Workshop", "de": "Balance-Werkstatt",
    "es": "Taller de equilibrio", "fr": "Atelier d'équilibre", "pt": "Oficina do equilíbrio",
    "ru": "Мастерская равновесия", "ja": "バランス工房", "ko": "균형 공방",
}
SUBJECTS = {
    "tr": "Denge ve yapı tasarımı", "en": "Balance and structural design",
    "de": "Gleichgewicht und Konstruktion", "es": "Equilibrio y diseño estructural",
    "fr": "Équilibre et construction", "pt": "Equilíbrio e construção",
    "ru": "Равновесие и конструирование", "ja": "バランスと構造設計", "ko": "균형과 구조 설계",
}
RUNTIME_FIELDS = (
    "challenge_id", "construction_type", "base_width", "pieces", "solution",
    "target_height", "stability_seconds", "max_tilt_degrees", "wind_strength",
    "platform_motion", "shake_strength", "gravity", "special_event", "workshop",
    "material", "ornament", "difficulty",
)
CREATED_AT = "2026-08-14T00:00:00Z"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{2,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class BalanceWorkshopBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def _valid_number(value: Any, minimum: float, maximum: float) -> bool:
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and minimum <= value <= maximum)


def _valid_geometry(row: dict[str, Any], profile: dict[str, Any]) -> bool:
    pieces, solution = row.get("pieces"), row.get("solution")
    if not isinstance(pieces, list) or len(pieces) != profile["pieces"]:
        return False
    if not isinstance(solution, list) or len(solution) != len(pieces):
        return False
    piece_ids: set[str] = set()
    by_id: dict[str, dict[str, Any]] = {}
    for piece in pieces:
        if not isinstance(piece, dict):
            return False
        piece_id = piece.get("piece_id")
        if (not isinstance(piece_id, str) or not ID_RE.fullmatch(piece_id)
                or piece_id in piece_ids or piece.get("shape") not in SHAPES
                or piece.get("feature") not in FEATURES
                or not _valid_number(piece.get("width"), 0.5, 3.0)
                or not _valid_number(piece.get("height"), 0.4, 2.0)
                or not _valid_number(piece.get("mass"), 0.2, 5.0)
                or not _valid_number(piece.get("friction"), 0.3, 1.0)):
            return False
        piece_ids.add(piece_id)
        by_id[piece_id] = piece
    used: set[str] = set()
    weighted_x = total_mass = 0.0
    top = 0.0
    base_width = row.get("base_width")
    if not _valid_number(base_width, 3.0, 10.0):
        return False
    for slot in solution:
        if not isinstance(slot, dict):
            return False
        piece_id = slot.get("piece_id")
        x, y = slot.get("x"), slot.get("y")
        if (piece_id not in by_id or piece_id in used
                or not _valid_number(x, -10.0, 10.0) or not _valid_number(y, 0.0, 20.0)
                or slot.get("rotation") not in (0, 90, 180, 270)):
            return False
        piece = by_id[piece_id]
        if y < piece["height"] / 2 or abs(x) + piece["width"] / 2 > base_width / 2:
            return False
        weighted_x += piece["mass"] * x
        total_mass += piece["mass"]
        top = max(top, y + piece["height"] / 2)
        used.add(piece_id)
    return (used == piece_ids and abs(weighted_x / total_mass) <= 0.01
            and abs(round(top, 2) - row.get("target_height", -1)) <= 0.01)


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = CHALLENGES / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BalanceWorkshopBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PER_POOL:
        raise BalanceWorkshopBuildError(
            f"{language}/{band}: expected {PER_POOL} challenges, got {len(rows)}"
        )
    ids: set[str] = set()
    signatures: set[str] = set()
    cultural = 0
    profile = PROFILE[band]
    expected_difficulty = tuple(BANDS).index(band) + 1
    for index, row in enumerate(rows, 1):
        challenge_id = row.get("challenge_id")
        source, tags = row.get("source"), row.get("culture_tags")
        signature = json.dumps({"pieces": row.get("pieces"), "solution": row.get("solution")},
                               sort_keys=True, separators=(",", ":"))
        if (not isinstance(challenge_id, str) or not ID_RE.fullmatch(challenge_id)
                or challenge_id in ids or signature in signatures
                or not _valid_geometry(row, profile)
                or row.get("construction_type") not in STRUCTURES
                or row.get("base_width") != profile["base"]
                or row.get("stability_seconds") != profile["stability"]
                or row.get("max_tilt_degrees") != profile["tilt"]
                or not _valid_number(row.get("wind_strength"), 0.0, 2.0)
                or not _valid_number(row.get("platform_motion"), 0.0, 0.5)
                or not _valid_number(row.get("shake_strength"), 0.0, 0.3)
                or row.get("gravity") != 9.8 or row.get("special_event") not in EVENTS
                or any(not isinstance(row.get(field), str) or not row[field].strip()
                       for field in ("workshop", "material", "ornament"))
                or row.get("difficulty") != expected_difficulty
                or not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://")
                or not isinstance(tags, list) or row.get("review_status") != "ai-draft"):
            raise BalanceWorkshopBuildError(f"{language}/{band}:{index}: invalid construction")
        cultural += any(str(tag).startswith(f"culture:{language}") for tag in tags)
        ids.add(challenge_id)
        signatures.add(signature)
    if (cultural != PER_POOL or {row["special_event"] for row in rows} != EVENTS
            or {row["construction_type"] for row in rows} != STRUCTURES):
        raise BalanceWorkshopBuildError(f"{language}/{band}: coverage is incomplete")
    if len({(row["workshop"], row["material"], row["ornament"]) for row in rows}) != 5:
        raise BalanceWorkshopBuildError(f"{language}/{band}: expected five cultural workshop kits")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    challenges = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    extras = visual_payloads("balance-workshop", band)
    extras["data/gameplay.json"] = gameplay_config("balance-workshop", band)
    manifest = {
        "schema_version": 1,
        "game_id": str(uuid.uuid5(uuid.NAMESPACE_URL,
                                  f"https://alika.tr/games/balance-workshop/v1/{language}/{band}")),
        "game_version": 1, "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PER_POOL} yapı görevi",
        "game_type": "balance_workshop", "min_app_version": "1.1.24",
        "min_players": 1, "max_players": 8, "age_min": age_min, "age_max": age_max,
        "subject": SUBJECTS[language], "topic": f"{age_min}–{age_max}", "language": language,
        "license": "CC-BY-NC-4.0", "author": "AliKa Atölye",
        "assets": ([{"path": "data/challenges.json", "sha256": hashlib.sha256(challenges).hexdigest(),
                     "asset_type": "challenges", "size_bytes": len(challenges)}] + asset_records(extras)),
        "total_size_bytes": len(challenges) + sum(map(len, extras.values())), "created_at": CREATED_AT,
    }
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_STORED) as archive:
        for name, payload in (("manifest.json", _json_bytes(manifest)),
                              ("data/challenges.json", challenges), *extras.items()):
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
            relative = Path("games") / "balance-workshop" / "dist" / language / f"{band}.alika-game"
            outputs[ROOT / relative] = payload
            entries.append({"path": relative.as_posix(), "sha256": hashlib.sha256(payload).hexdigest(),
                            "size_bytes": len(payload), "challenge_count": len(rows),
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
            raise BalanceWorkshopBuildError("generated files are stale: " + ", ".join(stale))
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
    except BalanceWorkshopBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
