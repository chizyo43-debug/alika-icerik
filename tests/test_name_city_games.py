from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_name_city_games", ROOT / "tools" / "build_name_city_games.py")
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_catalog_has_36_downloads_and_7200_rounds():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "name-city" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert len(catalog["games"]) == 36
    assert sum(item["round_count"] for item in catalog["games"]) == 7200


def test_packages_have_local_rounds_rich_visuals_and_family_rules():
    catalog = json.loads((ROOT / "games" / "name-city" / "catalog.json").read_text(encoding="utf-8"))
    for item in catalog["games"]:
        path = ROOT / item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
        with zipfile.ZipFile(path) as archive:
            assert set(archive.namelist()) == {"manifest.json", "data/rounds.json",
                                               "data/gameplay.json", "visual/game_art.webp",
                                               "visual/theme.json"}
            manifest = json.loads(archive.read("manifest.json"))
            rounds = json.loads(archive.read("data/rounds.json"))
            gameplay = json.loads(archive.read("data/gameplay.json"))
            theme = json.loads(archive.read("visual/theme.json"))
        assert manifest["game_type"] == "name_city"
        assert len(rounds) == 200
        assert all(set(row) == set(builder.RUNTIME_FIELDS) for row in rounds)
        assert gameplay["scoring"]["family_vote_for_disputed_answer"] is True
        assert gameplay["safety"]["no_personal_data_entry"] is True
        assert len(gameplay["events"]) == 5
        assert theme["accessibility"]["color_only_feedback"] is False


def test_every_language_uses_its_own_initial_system_and_age_profile():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert all(row["initial"] in builder.ALPHABETS[language] for row in rows)
            assert all(row["initial_mode"] == builder.INITIAL_MODES[language] for row in rows)
            assert all({"person", "city"} <= set(row["category_ids"]) for row in rows)
            assert {row["special_event"] for row in rows} == set(builder.EVENTS)
    assert len(builder._load_pool("tr", "young")[0]["categories"]) == 5
    assert len(builder._load_pool("tr", "senior")[0]["categories"]) == 8
    assert builder.INITIAL_MODES["ja"] == "kana_row"
    assert builder.INITIAL_MODES["ko"] == "choseong"


def test_wrong_pool_size_fails_openly(monkeypatch):
    monkeypatch.setattr(builder, "PER_POOL", 201)
    with pytest.raises(builder.NameCityBuildError, match="expected 201 rounds"):
        builder._load_pool("tr", "young")
