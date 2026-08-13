from __future__ import annotations

import importlib.util
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_liar_games", ROOT / "tools" / "build_liar_games.py")
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_cards():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "liar" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["card_count"] for item in catalog["games"]) == 7200


def test_packages_are_data_only_with_two_truths_and_one_lie_contract():
    catalog = json.loads((ROOT / "games" / "liar" / "catalog.json").read_text(encoding="utf-8"))
    for item in catalog["games"]:
        with zipfile.ZipFile(ROOT / item["path"]) as archive:
            assert set(archive.namelist()) == {"manifest.json", "data/cards.json"}
            manifest = json.loads(archive.read("manifest.json"))
            cards = json.loads(archive.read("data/cards.json"))
        assert manifest["game_type"] == "liar"
        assert len(cards) == 200
        assert all(set(card) == set(builder.RUNTIME_FIELDS) for card in cards)
        assert all(len(card["statements"]) == 3 and len(set(card["statements"])) == 3 for card in cards)
        assert all(card["lie_index"] in (0, 1, 2) for card in cards)


def test_each_language_has_four_distinct_age_pools():
    for language in builder.LANGUAGES:
        pools = [frozenset(tuple(card["statements"]) for card in builder._load_pool(language, band))
                 for band in builder.BANDS]
        assert len(set(pools)) == 4


def test_sources_stay_in_review_rows_and_russian_continents_are_inflected():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert all(row["sources"] and all(
                source["url"].startswith("https://www.wikidata.org/wiki/Q")
                for source in row["sources"]
            ) for row in rows)
    russian = [statement for band in builder.BANDS for row in builder._load_pool("ru", band)
               for statement in row["statements"]]
    assert not any(f" в {continent}." in statement for continent in (
        "Азия", "Европа", "Африка", "Океания", "Антарктида",
    ) for statement in russian)
