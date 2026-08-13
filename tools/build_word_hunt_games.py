"""Build deterministic data-only AliKa word-hunt packages."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import uuid
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any


TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
from game_visuals import asset_records, visual_payloads
from gameplay_designs import gameplay_config


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = ROOT / "games" / "word-hunt"
PUZZLES = GAME_ROOT / "puzzles"
CATALOG = GAME_ROOT / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {"young": (5, 7), "mid": (8, 11), "teen": (12, 14), "senior": (15, 18)}
PER_POOL = 200
NAMES = {
    "tr": "Kelime Avı", "en": "Word Hunt", "de": "Wortjagd",
    "es": "Caza de palabras", "fr": "Chasse aux mots", "pt": "Caça-palavras",
    "ru": "Охота за словами", "ja": "ことばハント", "ko": "낱말 사냥",
}
SUBJECTS = {
    "tr": "Kelime bilgisi", "en": "Vocabulary", "de": "Wortschatz",
    "es": "Vocabulario", "fr": "Vocabulaire", "pt": "Vocabulário",
    "ru": "Словарный запас", "ja": "語彙", "ko": "어휘",
}
RUNTIME_FIELDS = ("puzzle_id", "answer", "answer_letters", "rack", "category", "clue",
                  "bonus_letter", "difficulty")
CREATED_AT = "2026-08-14T00:00:00Z"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class WordHuntBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = PUZZLES / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WordHuntBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PER_POOL:
        raise WordHuntBuildError(f"{language}/{band}: expected {PER_POOL} puzzles, got {len(rows)}")
    ids: set[str] = set()
    answers: set[str] = set()
    cultural = 0
    expected_difficulty = tuple(BANDS).index(band) + 1
    minimum_decoys = {"young": 0, "mid": 1, "teen": 2, "senior": 3}[band]
    for index, row in enumerate(rows, 1):
        puzzle_id, answer = row.get("puzzle_id"), row.get("answer")
        answer_letters, rack = row.get("answer_letters"), row.get("rack")
        normalized = " ".join(answer.casefold().split()) if isinstance(answer, str) else ""
        source, tags = row.get("source"), row.get("culture_tags")
        if (not isinstance(puzzle_id, str) or not ID_RE.fullmatch(puzzle_id) or puzzle_id in ids
                or not isinstance(answer, str) or not answer.strip() or normalized in answers
                or not isinstance(answer_letters, str) or not answer_letters
                or not isinstance(rack, list) or any(not isinstance(tile, str) or not tile for tile in rack)
                or not (Counter(answer_letters) <= Counter(rack))
                or len(rack) - len(answer_letters) < minimum_decoys
                or not isinstance(row.get("category"), str) or not row["category"].strip()
                or not isinstance(row.get("clue"), str) or not row["clue"].strip()
                or not isinstance(row.get("bonus_letter"), str)
                or row["bonus_letter"] not in answer_letters
                or row.get("difficulty") != expected_difficulty
                or not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://")
                or not isinstance(tags, list) or row.get("review_status") != "ai-draft"):
            raise WordHuntBuildError(f"{language}/{band}:{index}: invalid puzzle")
        cultural += any(str(tag).startswith(f"culture:{language}") for tag in tags)
        ids.add(puzzle_id)
        answers.add(normalized)
    if cultural < 30:
        raise WordHuntBuildError(f"{language}/{band}: at least 30 culture-local puzzles required")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    puzzles = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    extras = visual_payloads("word-hunt", band)
    extras["data/gameplay.json"] = gameplay_config("word-hunt", band)
    manifest = {
        "schema_version": 1,
        "game_id": str(uuid.uuid5(uuid.NAMESPACE_URL,
                                  f"https://alika.tr/games/word-hunt/v1/{language}/{band}")),
        "game_version": 1, "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PER_POOL} bulmaca",
        "game_type": "word_hunt", "min_app_version": "1.1.24",
        "min_players": 1, "max_players": 12, "age_min": age_min, "age_max": age_max,
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
            relative = Path("games") / "word-hunt" / "dist" / language / f"{band}.alika-game"
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
            raise WordHuntBuildError("generated files are stale: " + ", ".join(stale))
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
    except WordHuntBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
