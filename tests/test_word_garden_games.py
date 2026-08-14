from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_word_garden_games", ROOT / "tools" / "build_word_garden_games.py")
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_catalog_has_36_downloads_and_7200_words():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "word-garden" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert len(catalog["games"]) == 36
    assert sum(item["puzzle_count"] for item in catalog["games"]) == 7200


def test_packages_use_word_garden_instead_of_hanging_visuals():
    catalog = json.loads((ROOT / "games" / "word-garden" / "catalog.json").read_text(encoding="utf-8"))
    for item in catalog["games"]:
        path = ROOT / item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
        with zipfile.ZipFile(path) as archive:
            assert set(archive.namelist()) == {"manifest.json", "data/puzzles.json",
                                               "data/gameplay.json", "visual/game_art.webp",
                                               "visual/theme.json"}
            manifest = json.loads(archive.read("manifest.json"))
            puzzles = json.loads(archive.read("data/puzzles.json"))
            gameplay = json.loads(archive.read("data/gameplay.json"))
        assert manifest["game_type"] == "hangman"
        assert len(puzzles) == 200
        assert all(set(row) == set(builder.RUNTIME_FIELDS) for row in puzzles)
        assert gameplay["garden"]["gallows_visual"] is False
        assert gameplay["safety"]["no_gallows"] is True
        assert gameplay["safety"]["no_injury_or_death"] is True
        assert len(gameplay["events"]) == 5


def test_words_patterns_culture_and_age_rules_are_valid():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert sum(f"culture:{language}" in row["culture_tags"] for row in rows) >= 30
            assert all(row["letters"] == builder.answer_tiles(language, row["answer"]) for row in rows)
            assert all(row["pattern"] == builder.answer_pattern(row["answer"]) for row in rows)
            assert {row["special_event"] for row in rows} == set(builder.EVENTS)
    assert builder._load_pool("tr", "young")[0]["max_misses"] == 10
    assert builder._load_pool("tr", "senior")[0]["max_misses"] == 6


def test_wrong_pool_size_fails_openly(monkeypatch):
    monkeypatch.setattr(builder, "PER_POOL", 201)
    with pytest.raises(builder.WordGardenBuildError, match="expected 201 puzzles"):
        builder._load_pool("tr", "young")
