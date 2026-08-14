"""Build deterministic child-safe hangman-style AliKa Word Garden packages."""
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
from generate_word_garden_games import EVENTS, HINTS, MISSES, answer_pattern, answer_tiles


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = ROOT / "games" / "word-garden"
PUZZLES = GAME_ROOT / "puzzles"
CATALOG = GAME_ROOT / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {"young": (5, 7), "mid": (8, 11), "teen": (12, 14), "senior": (15, 18)}
PER_POOL = 200
NAMES = {
    "tr": "Adam Asmaca · Kelime Bahçesi", "en": "Word Guess · Word Garden",
    "de": "Wörter raten · Wortgarten", "es": "Ahorcado · Jardín de palabras",
    "fr": "Le Pendu · Jardin des mots", "pt": "Forca · Jardim de palavras",
    "ru": "Виселица · Сад слов", "ja": "ことば当て · ことばの庭", "ko": "단어 맞히기 · 단어 정원",
}
SUBJECTS = {
    "tr": "Kelime bilgisi", "en": "Vocabulary", "de": "Wortschatz",
    "es": "Vocabulario", "fr": "Vocabulaire", "pt": "Vocabulário",
    "ru": "Словарный запас", "ja": "語彙", "ko": "어휘",
}
RUNTIME_FIELDS = ("puzzle_id", "answer", "letters", "pattern", "category", "clue",
                  "max_misses", "hint_tokens", "special_event", "difficulty")
CREATED_AT = "2026-08-14T00:00:00Z"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class WordGardenBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = PUZZLES / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WordGardenBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PER_POOL:
        raise WordGardenBuildError(f"{language}/{band}: expected {PER_POOL} puzzles, got {len(rows)}")
    ids, answers, cultural = set(), set(), 0
    for index, row in enumerate(rows, 1):
        puzzle_id, answer = row.get("puzzle_id"), row.get("answer")
        normalized = " ".join(answer.casefold().split()) if isinstance(answer, str) else ""
        source, tags = row.get("source"), row.get("culture_tags")
        if (not isinstance(puzzle_id, str) or not ID_RE.fullmatch(puzzle_id) or puzzle_id in ids
                or not isinstance(answer, str) or not answer.strip() or normalized in answers
                or row.get("letters") != answer_tiles(language, answer)
                or row.get("pattern") != answer_pattern(answer)
                or not isinstance(row.get("category"), str) or not row["category"].strip()
                or not isinstance(row.get("clue"), str) or not row["clue"].strip()
                or row.get("max_misses") != MISSES[band]
                or row.get("hint_tokens") != HINTS[band]
                or row.get("special_event") not in EVENTS
                or row.get("difficulty") != tuple(BANDS).index(band) + 1
                or not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://")
                or not isinstance(tags, list) or row.get("review_status") != "ai-draft"):
            raise WordGardenBuildError(f"{language}/{band}:{index}: invalid puzzle")
        cultural += f"culture:{language}" in tags
        ids.add(puzzle_id)
        answers.add(normalized)
    if cultural < 30:
        raise WordGardenBuildError(f"{language}/{band}: at least 30 culture-local words required")
    if {row["special_event"] for row in rows} != set(EVENTS):
        raise WordGardenBuildError(f"{language}/{band}: all special events required")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    puzzles = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    extras = visual_payloads("word-garden", band)
    extras["data/gameplay.json"] = gameplay_config("word-garden", band)
    manifest = {
        "schema_version": 1,
        "game_id": str(uuid.uuid5(uuid.NAMESPACE_URL, f"https://alika.tr/games/word-garden/v1/{language}/{band}")),
        "game_version": 1, "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PER_POOL} kelime",
        "game_type": "hangman", "min_app_version": "1.1.24",
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
    outputs, entries = {}, []
    for language in LANGUAGES:
        for band in BANDS:
            payload, manifest = _package(language, band, _load_pool(language, band))
            relative = Path("games") / "word-garden" / "dist" / language / f"{band}.alika-game"
            outputs[ROOT / relative] = payload
            entries.append({"path": relative.as_posix(), "sha256": hashlib.sha256(payload).hexdigest(),
                            "size_bytes": len(payload), "puzzle_count": PER_POOL,
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
            raise WordGardenBuildError("generated files are stale: " + ", ".join(stale))
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
    except WordGardenBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
