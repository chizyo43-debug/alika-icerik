"""Build deterministic data-only AliKa story-adventure packages."""
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
GAME_ROOT = ROOT / "games" / "story-adventure"
CARDS = GAME_ROOT / "cards"
CATALOG = GAME_ROOT / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {"young": (5, 7), "mid": (8, 11), "teen": (12, 14), "senior": (15, 18)}
PER_POOL = 200
NAMES = {
    "tr": "Hikâye Macerası", "en": "Story Adventure", "de": "Geschichtenabenteuer",
    "es": "Aventura de historias", "fr": "Aventure à raconter", "pt": "Aventura de histórias",
    "ru": "Приключение-история", "ja": "物語アドベンチャー", "ko": "이야기 모험",
}
SUBJECTS = {
    "tr": "Yaratıcı anlatım", "en": "Creative storytelling", "de": "Kreatives Erzählen",
    "es": "Narración creativa", "fr": "Récit créatif", "pt": "Narrativa criativa",
    "ru": "Творческое повествование", "ja": "創作物語", "ko": "창의적 이야기",
}
RUNTIME_FIELDS = ("card_id", "character", "setting", "object", "mission", "twist",
                  "category", "difficulty")
CREATED_AT = "2026-08-14T00:00:00Z"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class StoryAdventureBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = CARDS / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StoryAdventureBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PER_POOL:
        raise StoryAdventureBuildError(f"{language}/{band}: expected {PER_POOL} cards, got {len(rows)}")
    ids: set[str] = set()
    combinations: set[tuple[str, ...]] = set()
    cultural = 0
    expected_difficulty = tuple(BANDS).index(band) + 1
    text_fields = ("character", "setting", "object", "mission", "twist", "category")
    for index, row in enumerate(rows, 1):
        card_id = row.get("card_id")
        source = row.get("source")
        tags = row.get("culture_tags")
        combo = tuple(" ".join(str(row.get(field, "")).casefold().split()) for field in text_fields[:-1])
        if (not isinstance(card_id, str) or not ID_RE.fullmatch(card_id) or card_id in ids
                or any(not isinstance(row.get(field), str) or not row[field].strip()
                       or len(row[field]) > 180 for field in text_fields)
                or combo in combinations or row.get("difficulty") != expected_difficulty
                or not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://")
                or not isinstance(tags, list) or row.get("review_status") != "ai-draft"):
            raise StoryAdventureBuildError(f"{language}/{band}:{index}: invalid card")
        cultural += any(str(tag).startswith(f"culture:{language}") for tag in tags)
        ids.add(card_id)
        combinations.add(combo)
    if cultural < 40:
        raise StoryAdventureBuildError(f"{language}/{band}: at least 40 culture-local cards required")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    cards = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    extras = visual_payloads("story-adventure", band)
    extras["data/gameplay.json"] = gameplay_config("story-adventure", band)
    manifest = {
        "schema_version": 1,
        "game_id": str(uuid.uuid5(uuid.NAMESPACE_URL,
                                  f"https://alika.tr/games/story-adventure/v1/{language}/{band}")),
        "game_version": 1, "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PER_POOL} kart",
        "game_type": "story_adventure", "min_app_version": "1.1.24",
        "min_players": 1, "max_players": 12, "age_min": age_min, "age_max": age_max,
        "subject": SUBJECTS[language], "topic": f"{age_min}–{age_max}", "language": language,
        "license": "CC-BY-NC-4.0", "author": "AliKa Atölye",
        "assets": ([{"path": "data/cards.json", "sha256": hashlib.sha256(cards).hexdigest(),
                     "asset_type": "cards", "size_bytes": len(cards)}] + asset_records(extras)),
        "total_size_bytes": len(cards) + sum(map(len, extras.values())), "created_at": CREATED_AT,
    }
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_STORED) as archive:
        for name, payload in (("manifest.json", _json_bytes(manifest)),
                              ("data/cards.json", cards), *extras.items()):
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
            relative = Path("games") / "story-adventure" / "dist" / language / f"{band}.alika-game"
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
            raise StoryAdventureBuildError("generated files are stale: " + ", ".join(stale))
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
    except StoryAdventureBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
