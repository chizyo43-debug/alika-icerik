"""Build deterministic, data-only AliKa trivia packages from reviewable JSONL."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import uuid
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRIVIA = ROOT / "games" / "trivia"
QUESTIONS = TRIVIA / "questions"
DIST = TRIVIA / "dist"
CATALOG = TRIVIA / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {
    "young": (5, 7),
    "mid": (8, 11),
    "teen": (12, 14),
    "senior": (15, 18),
}
NAMES = {
    "tr": "Bilgi Yarışması",
    "en": "General Knowledge Challenge",
    "de": "Wissensquiz",
    "es": "Concurso de cultura general",
    "fr": "Quiz de culture générale",
    "pt": "Desafio de conhecimentos gerais",
    "ru": "Викторина общих знаний",
    "ja": "一般知識クイズ",
    "ko": "상식 퀴즈",
}
SUBJECTS = {
    "tr": "Genel Kültür", "en": "General Knowledge", "de": "Allgemeinwissen",
    "es": "Cultura general", "fr": "Culture générale", "pt": "Conhecimentos gerais",
    "ru": "Общие знания", "ja": "一般知識", "ko": "상식",
}
CREATED_AT = "2026-08-13T00:00:00Z"
QUESTION_FIELDS = (
    "question_id", "question", "choices", "correct", "subject", "topic", "explanation",
)
ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class TriviaBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = QUESTIONS / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TriviaBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != 200:
        raise TriviaBuildError(f"{language}/{band}: expected 200 questions, got {len(rows)}")
    seen_ids: set[str] = set()
    seen_text: set[str] = set()
    answers = Counter()
    cultural = 0
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise TriviaBuildError(f"{language}/{band}:{index}: row must be an object")
        missing = set(QUESTION_FIELDS) - set(row)
        if missing:
            raise TriviaBuildError(f"{language}/{band}:{index}: missing {sorted(missing)}")
        question_id = row["question_id"]
        question = row["question"]
        choices = row["choices"]
        correct = row["correct"]
        if (not isinstance(question_id, str) or not ID_RE.fullmatch(question_id)
                or question_id in seen_ids):
            raise TriviaBuildError(f"{language}/{band}:{index}: invalid/duplicate question_id")
        normalized = " ".join(str(question).casefold().split())
        if not normalized or normalized in seen_text:
            raise TriviaBuildError(f"{language}/{band}:{index}: blank/duplicate question")
        if (not isinstance(choices, list) or len(choices) != 4
                or any(not isinstance(choice, str) or not choice.strip() for choice in choices)
                or len({choice.strip().casefold() for choice in choices}) != 4):
            raise TriviaBuildError(f"{language}/{band}:{index}: choices must be four unique strings")
        if isinstance(correct, bool) or not isinstance(correct, int) or correct not in range(4):
            raise TriviaBuildError(f"{language}/{band}:{index}: invalid correct index")
        source = row.get("source")
        if not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://"):
            raise TriviaBuildError(f"{language}/{band}:{index}: HTTPS source is required")
        tags = row.get("culture_tags")
        if not isinstance(tags, list):
            raise TriviaBuildError(f"{language}/{band}:{index}: culture_tags must be a list")
        cultural += any(str(tag).startswith(f"culture:{language}") for tag in tags)
        seen_ids.add(question_id)
        seen_text.add(normalized)
        answers[correct] += 1
    if cultural < 40:
        raise TriviaBuildError(f"{language}/{band}: at least 40 culture-local questions required")
    if max(answers.values()) - min(answers.values()) > 2:
        raise TriviaBuildError(f"{language}/{band}: correct-answer positions are imbalanced")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    runtime_rows = [{key: row[key] for key in QUESTION_FIELDS} for row in rows]
    questions = _json_bytes(runtime_rows)
    game_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"https://alika.tr/games/trivia/v1/{language}/{band}"))
    manifest = {
        "schema_version": 1,
        "game_id": game_id,
        "game_version": 1,
        "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · 200",
        "game_type": "quiz_race",
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
            "path": "data/questions.json",
            "sha256": hashlib.sha256(questions).hexdigest(),
            "asset_type": "questions",
            "size_bytes": len(questions),
        }],
        "total_size_bytes": len(questions),
        "created_at": CREATED_AT,
    }
    output = io.BytesIO()
    # Stored entries keep the package bytes identical across Python/zlib builds.
    with zipfile.ZipFile(output, "w", zipfile.ZIP_STORED) as archive:
        for name, payload in (
            ("manifest.json", _json_bytes(manifest)),
            ("data/questions.json", questions),
        ):
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
            relative = Path("games") / "trivia" / "dist" / language / f"{band}.alika-game"
            outputs[ROOT / relative] = payload
            entries.append({
                "path": relative.as_posix(),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "size_bytes": len(payload),
                "question_count": len(rows),
                "game_id": manifest["game_id"],
                "game_version": manifest["game_version"],
                "language": language,
                "age_min": manifest["age_min"],
                "age_max": manifest["age_max"],
                "name": manifest["name"],
            })
    catalog = _json_bytes({
        "schema_version": 1,
        "generated_at": CREATED_AT,
        "review_status": "ai-draft",
        "human_approved": False,
        "games": entries,
    })
    outputs[CATALOG] = catalog
    if check:
        mismatches = [path.relative_to(ROOT).as_posix() for path, data in outputs.items()
                      if not path.is_file() or (
                          path.read_bytes().replace(b"\r\n", b"\n") != data
                          if path.suffix == ".json" else path.read_bytes() != data
                      )]
        if mismatches:
            raise TriviaBuildError("generated files are stale: " + ", ".join(mismatches))
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
    except TriviaBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
