"""Build deterministic, data-only AliKa memory-card packages."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import uuid
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "games" / "memory"
PAIRS_DIR = MEMORY / "pairs"
DIST = MEMORY / "dist"
CATALOG = MEMORY / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {
    "young": (5, 7),
    "mid": (8, 11),
    "teen": (12, 14),
    "senior": (15, 18),
}
PAIRS = 100
NAMES = {
    "tr": "Ülke–Başkent Hafızası", "en": "Country–Capital Memory",
    "de": "Länder–Hauptstädte-Memory", "es": "Memoria de países y capitales",
    "fr": "Mémoire des pays et capitales", "pt": "Memória de países e capitais",
    "ru": "Память: страны и столицы", "ja": "国と首都の神経衰弱", "ko": "나라와 수도 기억 게임",
}
SUBJECTS = {
    "tr": "Genel Kültür", "en": "General Knowledge", "de": "Allgemeinwissen",
    "es": "Cultura general", "fr": "Culture générale", "pt": "Conhecimentos gerais",
    "ru": "Общие знания", "ja": "一般知識", "ko": "상식",
}
PAIR_LABELS = {
    "tr": "çift", "en": "pairs", "de": "Paare", "es": "parejas",
    "fr": "paires", "pt": "pares", "ru": "пар", "ja": "組", "ko": "쌍",
}
CREATED_AT = "2026-08-13T00:00:00Z"
RUNTIME_FIELDS = ("pair_id", "left", "right", "category", "explanation")
ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class MemoryBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = PAIRS_DIR / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MemoryBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PAIRS:
        raise MemoryBuildError(f"{language}/{band}: expected {PAIRS} pairs, got {len(rows)}")

    ids: set[str] = set()
    lefts: set[str] = set()
    rights: set[str] = set()
    cultural = 0
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise MemoryBuildError(f"{language}/{band}:{index}: row must be an object")
        missing = set(RUNTIME_FIELDS) - set(row)
        if missing:
            raise MemoryBuildError(f"{language}/{band}:{index}: missing {sorted(missing)}")
        pair_id = row["pair_id"]
        if not isinstance(pair_id, str) or not ID_RE.fullmatch(pair_id) or pair_id in ids:
            raise MemoryBuildError(f"{language}/{band}:{index}: invalid/duplicate pair_id")
        values = [row[field] for field in RUNTIME_FIELDS[1:]]
        if any(not isinstance(value, str) or not value.strip() for value in values):
            raise MemoryBuildError(f"{language}/{band}:{index}: card text must be non-empty strings")
        left = " ".join(row["left"].casefold().split())
        right = " ".join(row["right"].casefold().split())
        if left == right or left in lefts or right in rights:
            raise MemoryBuildError(f"{language}/{band}:{index}: duplicate or self-revealing pair")
        source = row.get("source")
        if not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://"):
            raise MemoryBuildError(f"{language}/{band}:{index}: HTTPS source is required")
        tags = row.get("culture_tags")
        if not isinstance(tags, list):
            raise MemoryBuildError(f"{language}/{band}:{index}: culture_tags must be a list")
        cultural += any(str(tag).startswith(f"culture:{language}") for tag in tags)
        ids.add(pair_id)
        lefts.add(left)
        rights.add(right)
    if cultural < 15:
        raise MemoryBuildError(f"{language}/{band}: at least 15 culture-local pairs required")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    cards = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    game_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"https://alika.tr/games/memory/v1/{language}/{band}"))
    manifest = {
        "schema_version": 1,
        "game_id": game_id,
        "game_version": 1,
        "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PAIRS} {PAIR_LABELS[language]}",
        "game_type": "memory_cards",
        "min_app_version": "1.1.24",
        "min_players": 1,
        "max_players": 8,
        "age_min": age_min,
        "age_max": age_max,
        "subject": SUBJECTS[language],
        "topic": f"{age_min}–{age_max}",
        "language": language,
        "license": "CC-BY-NC-4.0",
        "author": "AliKa Atölye",
        "assets": [{
            "path": "data/cards.json",
            "sha256": hashlib.sha256(cards).hexdigest(),
            "asset_type": "cards",
            "size_bytes": len(cards),
        }],
        "total_size_bytes": len(cards),
        "created_at": CREATED_AT,
    }
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_STORED) as archive:
        for name, payload in (("manifest.json", _json_bytes(manifest)), ("data/cards.json", cards)):
            info = zipfile.ZipInfo(name, ZIP_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, payload, compress_type=zipfile.ZIP_STORED)
    return output.getvalue(), manifest


def build(*, check: bool) -> None:
    entries: list[dict[str, Any]] = []
    outputs: dict[Path, bytes] = {}
    for language in LANGUAGES:
        for band in BANDS:
            rows = _load_pool(language, band)
            payload, manifest = _package(language, band, rows)
            relative = Path("games") / "memory" / "dist" / language / f"{band}.alika-game"
            outputs[ROOT / relative] = payload
            entries.append({
                "path": relative.as_posix(), "sha256": hashlib.sha256(payload).hexdigest(),
                "size_bytes": len(payload), "pair_count": len(rows),
                "game_id": manifest["game_id"], "game_version": manifest["game_version"],
                "language": language, "age_min": manifest["age_min"],
                "age_max": manifest["age_max"], "name": manifest["name"],
            })
    outputs[CATALOG] = _json_bytes({
        "schema_version": 1, "generated_at": CREATED_AT,
        "review_status": "ai-draft", "human_approved": False, "games": entries,
    })
    if check:
        stale = [path.relative_to(ROOT).as_posix() for path, data in outputs.items()
                 if not path.is_file() or (
                     path.read_bytes().replace(b"\r\n", b"\n") != data
                     if path.suffix == ".json" else path.read_bytes() != data
                 )]
        if stale:
            raise MemoryBuildError("generated files are stale: " + ", ".join(stale))
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
    except MemoryBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
