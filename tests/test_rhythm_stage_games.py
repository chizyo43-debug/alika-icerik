from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_rhythm_stage_games", ROOT / "tools" / "build_rhythm_stage_games.py"
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_current_rhythms():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "rhythm-stage" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["challenge_count"] for item in catalog["games"]) == 7200


def test_packages_include_patterns_rules_visuals_and_match_catalog():
    catalog = json.loads((ROOT / "games" / "rhythm-stage" / "catalog.json").read_text(encoding="utf-8"))
    for item in catalog["games"]:
        path = ROOT / item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
        with zipfile.ZipFile(path) as archive:
            assert set(archive.namelist()) == {
                "manifest.json", "data/challenges.json", "data/gameplay.json",
                "visual/game_art.webp", "visual/theme.json",
            }
            manifest = json.loads(archive.read("manifest.json"))
            challenges = json.loads(archive.read("data/challenges.json"))
            gameplay = json.loads(archive.read("data/gameplay.json"))
            theme = json.loads(archive.read("visual/theme.json"))
        assert manifest["game_type"] == "rhythm_stage"
        assert len(challenges) == 200
        assert all(set(challenge) == set(builder.RUNTIME_FIELDS) for challenge in challenges)
        assert all(len(challenge["pattern"]) == challenge["steps_per_bar"] * challenge["bars"]
                   for challenge in challenges)
        assert gameplay["modes"] == ["echo_repeat", "family_relay", "duo_sync", "missing_beat"]
        assert gameplay["safety"]["microphone_required"] is False
        assert gameplay["safety"]["mute_visual_mode"] is True
        assert gameplay["timing"]["calibration_available"] is True
        assert len(gameplay["events"]) == 5
        assert theme["accessibility"]["color_only_feedback"] is False


def test_every_pool_is_unique_local_balanced_and_age_aware():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert len({(*row["pattern"], row["tempo_bpm"]) for row in rows}) == 200
            assert sum(f"culture:{language}" in row["culture_tags"] for row in rows) == 200
            assert len({(row["stage"], row["primary_instrument"], row["secondary_instrument"])
                        for row in rows}) == 5
            assert {row["special_event"] for row in rows} == builder.EVENTS
    young = json.loads(builder.gameplay_config("rhythm-stage", "young"))
    senior = json.loads(builder.gameplay_config("rhythm-stage", "senior"))
    assert young["round"]["practice_replays"] == 3
    assert young["round"]["speed_increase_percent"] == 0
    assert senior["round"]["practice_replays"] == 2
    assert senior["round"]["speed_increase_percent"] == 5
    assert all(len(row["pattern"]) == 8 for row in builder._load_pool("tr", "young"))
    assert all(len(row["pattern"]) == 24 for row in builder._load_pool("tr", "senior"))


def test_wrong_pool_size_fails_openly(monkeypatch):
    monkeypatch.setattr(builder, "PER_POOL", 201)
    with pytest.raises(builder.RhythmStageBuildError, match="expected 201 challenges"):
        builder._load_pool("tr", "young")


def test_broken_pattern_is_rejected(monkeypatch):
    rows = builder._load_pool("tr", "young")
    broken = [dict(row) for row in rows]
    broken[0] = {**broken[0], "pattern": [0] * 8}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.RhythmStageBuildError, match="invalid rhythm challenge"):
        builder._load_pool("tr", "young")


def test_malformed_timing_is_rejected_cleanly(monkeypatch):
    rows = builder._load_pool("tr", "young")
    broken = [dict(row) for row in rows]
    broken[0] = {**broken[0], "tempo_bpm": "fast", "bars": None}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.RhythmStageBuildError, match="invalid rhythm challenge"):
        builder._load_pool("tr", "young")
