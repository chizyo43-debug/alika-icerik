"""Build deterministic, data-only AliKa word-wheel packages."""
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
from word_wheel_design import wheel_config


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = ROOT / "games" / "word-wheel"
WORDS = GAME_ROOT / "words"
DIST = GAME_ROOT / "dist"
CATALOG = GAME_ROOT / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {"young": (5, 7), "mid": (8, 11), "teen": (12, 14), "senior": (15, 18)}
PUZZLES_PER_POOL = 200
NAMES = {
    "tr": "Çarkıfelek", "en": "Word Wheel", "de": "Glücksrad",
    "es": "Ruleta de palabras", "fr": "Roue des mots", "pt": "Roda das palavras",
    "ru": "Колесо слов", "ja": "ことばのルーレット", "ko": "낱말 돌림판",
}
SUBJECTS = {
    "tr": "Genel Kültür", "en": "General Knowledge", "de": "Allgemeinwissen",
    "es": "Cultura general", "fr": "Culture générale", "pt": "Conhecimentos gerais",
    "ru": "Общие знания", "ja": "一般知識", "ko": "상식",
}
WORD_LABELS = {"tr": "kelime", "en": "words", "de": "Wörter", "es": "palabras",
               "fr": "mots", "pt": "palavras", "ru": "слов", "ja": "語", "ko": "개 낱말"}
RUNTIME_FIELDS = ("puzzle_id", "answer", "category", "clue", "explanation")
CREATED_AT = "2026-08-25T00:00:00Z"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class WordWheelBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _key(value: str) -> str:
    return " ".join(value.casefold().split())


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = WORDS / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WordWheelBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PUZZLES_PER_POOL:
        raise WordWheelBuildError(f"{language}/{band}: expected {PUZZLES_PER_POOL} words, got {len(rows)}")
    ids: set[str] = set()
    answers: set[str] = set()
    cultural = 0
    categories: set[str] = set()
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict) or set(RUNTIME_FIELDS) - set(row):
            raise WordWheelBuildError(f"{language}/{band}:{index}: invalid row")
        puzzle_id = row["puzzle_id"]
        answer = row["answer"]
        category = row["category"]
        clue = row["clue"]
        explanation = row["explanation"]
        normalized = _key(answer) if isinstance(answer, str) else ""
        if (not isinstance(puzzle_id, str) or not ID_RE.fullmatch(puzzle_id) or puzzle_id in ids
                or not isinstance(answer, str) or not 1 <= len(answer.strip()) <= 80
                or not any(char.isalnum() for char in answer) or normalized in answers
                or not isinstance(category, str) or not category.strip() or len(category) > 128
                or not isinstance(clue, str) or not clue.strip() or len(clue) > 300
                or normalized in _key(clue)
                or not isinstance(explanation, str) or len(explanation) > 1000):
            raise WordWheelBuildError(f"{language}/{band}:{index}: invalid or answer-revealing puzzle")
        source = row.get("source")
        tags = row.get("culture_tags")
        if not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://"):
            raise WordWheelBuildError(f"{language}/{band}:{index}: HTTPS source is required")
        if not isinstance(tags, list):
            raise WordWheelBuildError(f"{language}/{band}:{index}: culture_tags must be a list")
        cultural += any(str(tag).startswith(f"culture:{language}") for tag in tags)
        categories.add(category.strip())
        ids.add(puzzle_id)
        answers.add(normalized)
    if cultural < 30:
        raise WordWheelBuildError(f"{language}/{band}: at least 30 culture-local words required")
    if len(categories) < 7:
        raise WordWheelBuildError(f"{language}/{band}: at least 7 mixed categories required")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    words = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    extras = visual_payloads("word-wheel", band)
    extras["data/wheel.json"] = wheel_config(language, band)
    manifest = {
        "schema_version": 1,
        "game_id": str(uuid.uuid5(uuid.NAMESPACE_URL,
                                  f"https://alika.tr/games/word-wheel/v1/{language}/{band}")),
        "game_version": 2, "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PUZZLES_PER_POOL} {WORD_LABELS[language]}",
        "game_type": "word_wheel", "min_app_version": "1.1.24",
        "min_players": 1, "max_players": 8, "age_min": age_min, "age_max": age_max,
        "subject": SUBJECTS[language], "topic": f"{age_min}–{age_max}", "language": language,
        "license": "CC-BY-NC-4.0", "author": "AliKa Atölye",
        "assets": ([{"path": "data/words.json", "sha256": hashlib.sha256(words).hexdigest(),
                     "asset_type": "words", "size_bytes": len(words)}]
                   + asset_records(extras)),
        "total_size_bytes": len(words) + sum(map(len, extras.values())), "created_at": CREATED_AT,
    }
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_STORED) as archive:
        entries = (("manifest.json", _json_bytes(manifest)), ("data/words.json", words),
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
            relative = Path("games") / "word-wheel" / "dist" / language / f"{band}.alika-game"
            outputs[ROOT / relative] = payload
            entries.append({"path": relative.as_posix(), "sha256": hashlib.sha256(payload).hexdigest(),
                            "size_bytes": len(payload), "word_count": len(rows),
                            "game_id": manifest["game_id"], "game_version": manifest["game_version"],
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
            raise WordWheelBuildError("generated files are stale: " + ", ".join(stale))
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
    except WordWheelBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
