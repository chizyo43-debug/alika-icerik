"""Build deterministic data-only AliKa Rhythm Stage packages."""
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
GAME_ROOT = ROOT / "games" / "rhythm-stage"
CHALLENGES = GAME_ROOT / "challenges"
CATALOG = GAME_ROOT / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {"young": (5, 7), "mid": (8, 11), "teen": (12, 14), "senior": (15, 18)}
PROFILE = {
    "young": {"length": 8, "tempo": (72, 92), "tolerance": 180, "secondary": False},
    "mid": {"length": 16, "tempo": (84, 110), "tolerance": 140, "secondary": True},
    "teen": {"length": 16, "tempo": (96, 128), "tolerance": 110, "secondary": True},
    "senior": {"length": 24, "tempo": (108, 148), "tolerance": 90, "secondary": True},
}
SOUNDS = {"hand_drum", "frame_drum", "wood_click", "bass_drum", "bell", "snare",
          "metal_bell", "shaker", "clap"}
EVENTS = {"golden_beat", "time_freeze", "echo_round", "missing_beat", "tempo_lift"}
PER_POOL = 200
NAMES = {
    "tr": "Ritim Sahnesi", "en": "Rhythm Stage", "de": "Rhythmusbühne",
    "es": "Escenario rítmico", "fr": "Scène rythmique", "pt": "Palco do ritmo",
    "ru": "Сцена ритма", "ja": "リズムステージ", "ko": "리듬 무대",
}
SUBJECTS = {
    "tr": "Ritim ve zamanlama", "en": "Rhythm and timing", "de": "Rhythmus und Timing",
    "es": "Ritmo y coordinación", "fr": "Rythme et coordination", "pt": "Ritmo e coordenação",
    "ru": "Ритм и координация", "ja": "リズムとタイミング", "ko": "리듬과 타이밍",
}
RUNTIME_FIELDS = ("challenge_id", "tempo_bpm", "steps_per_bar", "bars", "pattern",
                  "accent_steps", "swing_percent", "tolerance_ms", "primary_instrument",
                  "primary_sound", "secondary_instrument", "secondary_sound", "stage",
                  "special_event", "difficulty")
CREATED_AT = "2026-08-14T00:00:00Z"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,80}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class RhythmStageBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = CHALLENGES / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RhythmStageBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PER_POOL:
        raise RhythmStageBuildError(f"{language}/{band}: expected {PER_POOL} challenges, got {len(rows)}")
    ids: set[str] = set()
    signatures: set[tuple[Any, ...]] = set()
    cultures = 0
    expected_difficulty = tuple(BANDS).index(band) + 1
    profile = PROFILE[band]
    for index, row in enumerate(rows, 1):
        challenge_id = row.get("challenge_id")
        pattern = row.get("pattern")
        accents = row.get("accent_steps")
        tempo = row.get("tempo_bpm")
        source, tags = row.get("source"), row.get("culture_tags")
        signature = ((*pattern, tempo) if isinstance(pattern, list) and isinstance(tempo, int) else ())
        if (not isinstance(challenge_id, str) or not ID_RE.fullmatch(challenge_id) or challenge_id in ids
                or not isinstance(pattern, list) or len(pattern) != profile["length"]
                or any(value not in (0, 1, 2, 3) for value in pattern) or sum(value > 0 for value in pattern) < 3
                or pattern[0] == 0 or signature in signatures
                or not isinstance(tempo, int)
                or not profile["tempo"][0] <= tempo <= profile["tempo"][1] or tempo % 2
                or row.get("steps_per_bar") != 8
                or not isinstance(row.get("bars"), int)
                or row["bars"] * row["steps_per_bar"] != len(pattern)
                or not isinstance(accents, list) or not accents
                or len(set(accents)) != len(accents)
                or any(not isinstance(step, int) or not 0 <= step < len(pattern) or pattern[step] == 0
                       for step in accents)
                or row.get("swing_percent") not in (0, 8, 12)
                or row.get("tolerance_ms") != profile["tolerance"]
                or (not profile["secondary"] and any(value in (2, 3) for value in pattern))
                or (profile["secondary"] and not any(value in (2, 3) for value in pattern))
                or row.get("primary_sound") not in SOUNDS or row.get("secondary_sound") not in SOUNDS
                or any(not isinstance(row.get(field), str) or not row[field].strip()
                       for field in ("primary_instrument", "secondary_instrument", "stage"))
                or row.get("special_event") not in EVENTS or row.get("difficulty") != expected_difficulty
                or not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://")
                or not isinstance(tags, list) or row.get("review_status") != "ai-draft"):
            raise RhythmStageBuildError(f"{language}/{band}:{index}: invalid rhythm challenge")
        cultures += any(str(tag).startswith(f"culture:{language}") for tag in tags)
        ids.add(challenge_id)
        signatures.add(signature)
    if cultures != PER_POOL or {row["special_event"] for row in rows} != EVENTS:
        raise RhythmStageBuildError(f"{language}/{band}: cultural or event coverage is incomplete")
    if len({(row["stage"], row["primary_instrument"], row["secondary_instrument"])
            for row in rows}) != 5:
        raise RhythmStageBuildError(f"{language}/{band}: expected five cultural rhythm kits")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    challenges = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    extras = visual_payloads("rhythm-stage", band)
    extras["data/gameplay.json"] = gameplay_config("rhythm-stage", band)
    manifest = {
        "schema_version": 1,
        "game_id": str(uuid.uuid5(uuid.NAMESPACE_URL,
                                  f"https://alika.tr/games/rhythm-stage/v1/{language}/{band}")),
        "game_version": 1, "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PER_POOL} ritim",
        "game_type": "rhythm_stage", "min_app_version": "1.1.24",
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
            relative = Path("games") / "rhythm-stage" / "dist" / language / f"{band}.alika-game"
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
            raise RhythmStageBuildError("generated files are stale: " + ", ".join(stale))
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
    except RhythmStageBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
