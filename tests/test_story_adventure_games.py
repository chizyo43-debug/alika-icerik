from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_story_adventure_games", ROOT / "tools" / "build_story_adventure_games.py"
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_current_cards():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "story-adventure" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["card_count"] for item in catalog["games"]) == 7200


def test_packages_include_story_rules_visuals_and_match_catalog():
    catalog = json.loads((ROOT / "games" / "story-adventure" / "catalog.json").read_text(encoding="utf-8"))
    for item in catalog["games"]:
        path = ROOT / item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
        with zipfile.ZipFile(path) as archive:
            assert set(archive.namelist()) == {
                "manifest.json", "data/cards.json", "data/gameplay.json",
                "visual/game_art.webp", "visual/theme.json",
            }
            manifest = json.loads(archive.read("manifest.json"))
            cards = json.loads(archive.read("data/cards.json"))
            gameplay = json.loads(archive.read("data/gameplay.json"))
            theme = json.loads(archive.read("visual/theme.json"))
        assert manifest["game_type"] == "story_adventure"
        assert len(cards) == 200
        assert all(set(card) == set(builder.RUNTIME_FIELDS) for card in cards)
        assert all(all(card[field] for field in ("character", "setting", "object", "mission", "twist"))
                   for card in cards)
        assert gameplay["modes"] == ["solo_story", "family_chain", "quick_60", "hidden_twist"]
        assert gameplay["story_structure"]["ending_choice"] is True
        assert gameplay["safety"]["personal_disclosure_required"] is False
        assert len(gameplay["events"]) == 5
        assert theme["accessibility"]["color_only_feedback"] is False


def test_each_pool_has_40_local_cards_and_age_rules_really_change():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert sum(f"culture:{language}" in row["culture_tags"] for row in rows) == 40
    young = json.loads(builder.gameplay_config("story-adventure", "young"))
    teen = json.loads(builder.gameplay_config("story-adventure", "teen"))
    assert young["round"]["seconds"] == 120
    assert young["round"]["required_elements"] == 3
    assert teen["round"]["seconds"] == 60
    assert teen["round"]["required_elements"] == 5


def test_wrong_pool_size_fails_openly(monkeypatch):
    monkeypatch.setattr(builder, "PER_POOL", 201)
    with pytest.raises(builder.StoryAdventureBuildError, match="expected 201 cards"):
        builder._load_pool("tr", "young")
