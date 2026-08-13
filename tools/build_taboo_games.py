"""Build deterministic data-only AliKa Taboo packages."""
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
GAME_ROOT = ROOT / "games" / "taboo"
CARDS = GAME_ROOT / "cards"
DIST = GAME_ROOT / "dist"
CATALOG = GAME_ROOT / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {"young": (5, 7), "mid": (8, 11), "teen": (12, 14), "senior": (15, 18)}
PER_POOL = 200
NAMES = {"tr": "Tabu", "en": "Taboo", "de": "Tabu", "es": "Tabú", "fr": "Tabou",
         "pt": "Tabu", "ru": "Табу", "ja": "タブー", "ko": "금지어 게임"}
RUNTIME_FIELDS = ("card_id", "target", "forbidden", "category", "explanation")
CREATED_AT = "2026-08-13T00:00:00Z"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class TabooBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _key(value: str) -> str:
    return " ".join(value.casefold().split())


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = CARDS / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TabooBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PER_POOL:
        raise TabooBuildError(f"{language}/{band}: expected {PER_POOL} cards, got {len(rows)}")
    ids: set[str] = set()
    targets: set[str] = set()
    for index, row in enumerate(rows, 1):
        card_id = str(row.get("card_id") or "")
        target = row.get("target")
        forbidden = row.get("forbidden")
        normalized = _key(target) if isinstance(target, str) else ""
        source = row.get("source")
        valid_forbidden = (isinstance(forbidden, list) and len(forbidden) == 4
                           and all(isinstance(value, str) and value.strip() and len(value) <= 100
                                   for value in forbidden)
                           and len({_key(value) for value in forbidden}) == 4
                           and normalized not in {_key(value) for value in forbidden})
        if (not ID_RE.fullmatch(card_id) or card_id in ids
                or not isinstance(target, str) or not 1 <= len(target.strip()) <= 100
                or normalized in targets or not valid_forbidden
                or not isinstance(row.get("category"), str) or not row["category"].strip()
                or not isinstance(row.get("explanation"), str)
                or not isinstance(source, dict)
                or not str(source.get("url", "")).startswith("https://www.wikidata.org/wiki/Q")
                or row.get("review_status") != "ai-draft"):
            raise TabooBuildError(f"{language}/{band}:{index}: invalid card")
        ids.add(card_id)
        targets.add(normalized)
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    cards = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    visuals = visual_payloads("taboo", band)
    extras = {**visuals, "data/gameplay.json": gameplay_config("taboo", band)}
    manifest = {
        "schema_version": 1,
        "game_id": str(uuid.uuid5(uuid.NAMESPACE_URL,
                                  f"https://alika.tr/games/taboo/v1/{language}/{band}")),
        "game_version": 1, "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PER_POOL} kart",
        "game_type": "taboo", "min_app_version": "1.1.24",
        "min_players": 2, "max_players": 8, "age_min": age_min, "age_max": age_max,
        "subject": "General Knowledge", "topic": f"{age_min}–{age_max}", "language": language,
        "license": "CC-BY-4.0", "author": "AliKa Atölye",
        "assets": ([{"path": "data/cards.json", "sha256": hashlib.sha256(cards).hexdigest(),
                     "asset_type": "cards", "size_bytes": len(cards)}]
                   + asset_records(extras)),
        "total_size_bytes": len(cards) + sum(map(len, extras.values())), "created_at": CREATED_AT,
    }
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_STORED) as archive:
        entries = (("manifest.json", _json_bytes(manifest)), ("data/cards.json", cards),
                   *extras.items())
        for name, payload in entries:
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
            relative = Path("games") / "taboo" / "dist" / language / f"{band}.alika-game"
            outputs[ROOT / relative] = payload
            entries.append({"path": relative.as_posix(), "sha256": hashlib.sha256(payload).hexdigest(),
                            "size_bytes": len(payload), "card_count": len(rows),
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
            raise TabooBuildError("generated files are stale: " + ", ".join(stale))
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
    except TabooBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
