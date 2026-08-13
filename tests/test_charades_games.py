from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_charades_games", ROOT / "tools" / "build_charades_games.py"
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_current_cards():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "charades" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["card_count"] for item in catalog["games"]) == 7200


def test_packages_include_rich_gameplay_and_visuals_and_match_catalog():
    catalog = json.loads((ROOT / "games" / "charades" / "catalog.json").read_text(encoding="utf-8"))
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
        assert manifest["game_type"] == "charades"
        assert len(cards) == 200
        assert all(set(card) == set(builder.RUNTIME_FIELDS) for card in cards)
        assert all("—" in card["prompt"] for card in cards)
        assert gameplay["modes"] == ["classic_team", "quick_5", "family_coop", "spotlight_chain"]
        assert gameplay["round"]["speaking_allowed"] is False
        assert len(gameplay["events"]) == 5
        assert theme["feedback"]["streak_confetti"] == 3


def test_each_age_pool_is_distinct_and_has_40_culture_local_cards():
    for language in builder.LANGUAGES:
        pools = []
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            pools.append(frozenset(row["prompt"] for row in rows))
            assert sum(f"culture:{language}" in row["culture_tags"] for row in rows) == 40
        assert len(set(pools)) == 4


def test_wrong_pool_size_fails_openly(monkeypatch):
    monkeypatch.setattr(builder, "PER_POOL", 201)
    with pytest.raises(builder.CharadesBuildError, match="expected 201 cards"):
        builder._load_pool("tr", "young")
