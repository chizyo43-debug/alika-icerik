from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from collections import Counter
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_word_hunt_games", ROOT / "tools" / "build_word_hunt_games.py"
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_current_puzzles():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "word-hunt" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["puzzle_count"] for item in catalog["games"]) == 7200


def test_packages_include_racks_rules_visuals_and_match_catalog():
    catalog = json.loads((ROOT / "games" / "word-hunt" / "catalog.json").read_text(encoding="utf-8"))
    for item in catalog["games"]:
        path = ROOT / item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
        with zipfile.ZipFile(path) as archive:
            assert set(archive.namelist()) == {
                "manifest.json", "data/puzzles.json", "data/gameplay.json",
                "visual/game_art.webp", "visual/theme.json",
            }
            manifest = json.loads(archive.read("manifest.json"))
            puzzles = json.loads(archive.read("data/puzzles.json"))
            gameplay = json.loads(archive.read("data/gameplay.json"))
            theme = json.loads(archive.read("visual/theme.json"))
        assert manifest["game_type"] == "word_hunt"
        assert len(puzzles) == 200
        assert all(set(puzzle) == set(builder.RUNTIME_FIELDS) for puzzle in puzzles)
        assert all(Counter(puzzle["answer_letters"]) <= Counter(puzzle["rack"])
                   for puzzle in puzzles)
        assert gameplay["modes"] == ["clue_hunt", "quick_10", "family_team", "letter_duel"]
        assert gameplay["rack"]["accented_letters_preserved"] is True
        assert gameplay["safety"]["no_public_spelling_shame"] is True
        assert len(gameplay["events"]) == 5
        assert theme["accessibility"]["color_only_feedback"] is False


def test_each_pool_has_local_words_and_age_rules_really_change():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert sum(f"culture:{language}" in row["culture_tags"] for row in rows) >= 30
    young = json.loads(builder.gameplay_config("word-hunt", "young"))
    senior = json.loads(builder.gameplay_config("word-hunt", "senior"))
    assert young["round"]["seconds"] == 120
    assert young["round"]["first_letter_hint"] is True
    assert senior["round"]["seconds"] == 45
    assert senior["rack"]["decoy_letters"] == 3


def test_wrong_pool_size_fails_openly(monkeypatch):
    monkeypatch.setattr(builder, "PER_POOL", 201)
    with pytest.raises(builder.WordHuntBuildError, match="expected 201 puzzles"):
        builder._load_pool("tr", "young")
