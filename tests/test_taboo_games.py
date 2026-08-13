from __future__ import annotations

import importlib.util
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_taboo_games", ROOT / "tools" / "build_taboo_games.py")
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_cards():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "taboo" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["card_count"] for item in catalog["games"]) == 7200


def test_packages_are_data_only_with_four_distinct_forbidden_terms():
    catalog = json.loads((ROOT / "games" / "taboo" / "catalog.json").read_text(encoding="utf-8"))
    for item in catalog["games"]:
        with zipfile.ZipFile(ROOT / item["path"]) as archive:
            assert set(archive.namelist()) == {
                "manifest.json", "data/cards.json", "visual/game_art.webp",
                "visual/theme.json", "data/gameplay.json",
            }
            manifest = json.loads(archive.read("manifest.json"))
            cards = json.loads(archive.read("data/cards.json"))
        assert manifest["game_type"] == "taboo"
        assert len(cards) == 200
        assert all(set(card) == set(builder.RUNTIME_FIELDS) for card in cards)
        assert all(len(card["forbidden"]) == 4 for card in cards)
        assert all(len({builder._key(value) for value in card["forbidden"]}) == 4 for card in cards)
        assert all(builder._key(card["target"]) not in {
            builder._key(value) for value in card["forbidden"]
        } for card in cards)


def test_each_language_has_four_distinct_age_pools():
    for language in builder.LANGUAGES:
        pools = [frozenset(card["target"] for card in builder._load_pool(language, band))
                 for band in builder.BANDS]
        assert len(set(pools)) == 4


def test_source_links_stay_in_review_data_not_runtime_package():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert all(row["source"]["url"].startswith("https://www.wikidata.org/wiki/Q") for row in rows)
    sample = ROOT / "games" / "taboo" / "dist" / "tr" / "young.alika-game"
    with zipfile.ZipFile(sample) as archive:
        cards = json.loads(archive.read("data/cards.json"))
    assert all("source" not in card and "culture_tags" not in card for card in cards)
