"""Build deterministic data-only AliKa Name–City packages."""
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
from name_city_language import (ALPHABETS, CATEGORIES, CATEGORY_IDS, CULTURE_FOCUS,
                                INITIAL_MODES)
from generate_name_city_games import EVENTS, PROFILES


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = ROOT / "games" / "name-city"
ROUNDS = GAME_ROOT / "rounds"
CATALOG = GAME_ROOT / "catalog.json"
LANGUAGES = tuple(ALPHABETS)
BANDS = {"young": (5, 7), "mid": (8, 11), "teen": (12, 14), "senior": (15, 18)}
PER_POOL = 200
NAMES = {
    "tr": "İsim Şehir", "en": "Name & City", "de": "Stadt, Land & Wort",
    "es": "Nombre y Ciudad", "fr": "Prénom et Ville", "pt": "Nome e Cidade",
    "ru": "Имя и город", "ja": "ことばカテゴリー", "ko": "초성 카테고리",
}
SUBJECTS = {
    "tr": "Kelime ve genel kültür", "en": "Words and general knowledge",
    "de": "Wörter und Allgemeinwissen", "es": "Palabras y cultura general",
    "fr": "Mots et culture générale", "pt": "Palavras e conhecimentos gerais",
    "ru": "Слова и общие знания", "ja": "ことばと一般知識", "ko": "낱말과 상식",
}
RUNTIME_FIELDS = ("round_id", "initial", "initial_mode", "category_ids", "categories",
                  "culture_focus", "seconds", "special_event", "difficulty")
CREATED_AT = "2026-08-14T00:00:00Z"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class NameCityBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = ROUNDS / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise NameCityBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PER_POOL:
        raise NameCityBuildError(f"{language}/{band}: expected {PER_POOL} rounds, got {len(rows)}")
    expected_labels = dict(zip(CATEGORY_IDS, CATEGORIES[language], strict=True))
    profile = PROFILES[band]
    ids, signatures = set(), set()
    for index, row in enumerate(rows, 1):
        ids_in_round, labels = row.get("category_ids"), row.get("categories")
        round_id = row.get("round_id")
        signature = (row.get("initial"), tuple(ids_in_round or ()), row.get("special_event"))
        valid_labels = (isinstance(ids_in_round, list) and isinstance(labels, list)
                        and labels == [expected_labels.get(item) for item in ids_in_round])
        source, tags = row.get("source"), row.get("culture_tags")
        if (not isinstance(round_id, str) or not ID_RE.fullmatch(round_id) or round_id in ids
                or row.get("initial") not in ALPHABETS[language]
                or row.get("initial_mode") != INITIAL_MODES[language]
                or not valid_labels or len(ids_in_round) != profile["category_count"]
                or len(set(ids_in_round)) != len(ids_in_round)
                or not {"person", "city"} <= set(ids_in_round)
                or any(item not in CATEGORY_IDS[:profile["available"]] for item in ids_in_round)
                or row.get("culture_focus") not in CULTURE_FOCUS[language]
                or row.get("seconds") != profile["seconds"]
                or row.get("special_event") not in EVENTS
                or row.get("difficulty") != tuple(BANDS).index(band) + 1
                or signature in signatures
                or not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://")
                or not isinstance(tags, list) or f"culture:{language}" not in tags
                or row.get("review_status") != "ai-draft"):
            raise NameCityBuildError(f"{language}/{band}:{index}: invalid round")
        ids.add(round_id)
        signatures.add(signature)
    if {row["special_event"] for row in rows} != set(EVENTS):
        raise NameCityBuildError(f"{language}/{band}: all special events required")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    rounds = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    extras = visual_payloads("name-city", band)
    extras["data/gameplay.json"] = gameplay_config("name-city", band)
    manifest = {
        "schema_version": 1,
        "game_id": str(uuid.uuid5(uuid.NAMESPACE_URL, f"https://alika.tr/games/name-city/v1/{language}/{band}")),
        "game_version": 1, "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PER_POOL} tur",
        "game_type": "name_city", "min_app_version": "1.1.24",
        "min_players": 2, "max_players": 12, "age_min": age_min, "age_max": age_max,
        "subject": SUBJECTS[language], "topic": f"{age_min}–{age_max}", "language": language,
        "license": "CC-BY-NC-4.0", "author": "AliKa Atölye",
        "assets": ([{"path": "data/rounds.json", "sha256": hashlib.sha256(rounds).hexdigest(),
                     "asset_type": "rounds", "size_bytes": len(rounds)}] + asset_records(extras)),
        "total_size_bytes": len(rounds) + sum(map(len, extras.values())), "created_at": CREATED_AT,
    }
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_STORED) as archive:
        for name, payload in (("manifest.json", _json_bytes(manifest)),
                              ("data/rounds.json", rounds), *extras.items()):
            info = zipfile.ZipInfo(name, ZIP_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, payload, compress_type=zipfile.ZIP_STORED)
    return output.getvalue(), manifest


def build(*, check: bool) -> None:
    outputs, entries = {}, []
    for language in LANGUAGES:
        for band in BANDS:
            payload, manifest = _package(language, band, _load_pool(language, band))
            relative = Path("games") / "name-city" / "dist" / language / f"{band}.alika-game"
            outputs[ROOT / relative] = payload
            entries.append({"path": relative.as_posix(), "sha256": hashlib.sha256(payload).hexdigest(),
                            "size_bytes": len(payload), "round_count": PER_POOL,
                            "game_id": manifest["game_id"], "game_version": 1,
                            "language": language, "age_min": manifest["age_min"],
                            "age_max": manifest["age_max"], "name": manifest["name"]})
    outputs[CATALOG] = _json_bytes({"schema_version": 1, "generated_at": CREATED_AT,
                                    "review_status": "ai-draft", "human_approved": False,
                                    "games": entries})
    if check:
        stale = [path.relative_to(ROOT).as_posix() for path, data in outputs.items()
                 if not path.is_file() or path.read_bytes() != data]
        if stale:
            raise NameCityBuildError("generated files are stale: " + ", ".join(stale))
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
    except NameCityBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
