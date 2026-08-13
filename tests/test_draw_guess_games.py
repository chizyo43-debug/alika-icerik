from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_draw_guess_games", ROOT / "tools" / "build_draw_guess_games.py"
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_current_cards():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "draw-guess" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["card_count"] for item in catalog["games"]) == 7200


def test_packages_include_canvas_rules_visuals_and_match_catalog():
    catalog = json.loads((ROOT / "games" / "draw-guess" / "catalog.json").read_text(encoding="utf-8"))
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
        assert manifest["game_type"] == "draw_guess"
        assert len(cards) == 200
        assert all(set(card) == set(builder.RUNTIME_FIELDS) for card in cards)
        assert all(card["draw_tip"] for card in cards)
        assert gameplay["modes"] == ["classic_team", "quick_5", "all_draw", "family_coop"]
        assert gameplay["round"]["letters_allowed"] is False
        assert gameplay["round"]["numbers_allowed"] is False
        assert gameplay["safety"]["unsafe_grip_required"] is False
        assert len(gameplay["events"]) == 5
        assert theme["accessibility"]["color_only_feedback"] is False


def test_each_pool_has_40_local_cards_and_age_rules_really_change():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert sum(f"culture:{language}" in row["culture_tags"] for row in rows) == 40
    young = json.loads(builder.gameplay_config("draw-guess", "young"))
    teen = json.loads(builder.gameplay_config("draw-guess", "teen"))
    assert young["round"]["seconds"] == 120
    assert young["canvas"]["shape_hint"] is True
    assert teen["round"]["seconds"] == 60
    assert teen["canvas"]["shape_hint"] is False


def test_wrong_pool_size_fails_openly(monkeypatch):
    monkeypatch.setattr(builder, "PER_POOL", 201)
    with pytest.raises(builder.DrawGuessBuildError, match="expected 201 cards"):
        builder._load_pool("tr", "young")
