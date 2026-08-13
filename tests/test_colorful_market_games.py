from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_colorful_market_games", ROOT / "tools" / "build_colorful_market_games.py"
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_unique_budget_puzzles():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "colorful-market" / "catalog.json")
                         .read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["puzzle_count"] for item in catalog["games"]) == 7200


def test_packages_include_budget_rules_visuals_and_match_catalog():
    catalog = json.loads((ROOT / "games" / "colorful-market" / "catalog.json")
                         .read_text(encoding="utf-8"))
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
        assert manifest["game_type"] == "budget_market"
        assert len(puzzles) == 200
        assert all(set(puzzle) == set(builder.RUNTIME_FIELDS) for puzzle in puzzles)
        assert gameplay["budgeting"]["fictional_star_tokens"] is True
        assert gameplay["safety"]["no_real_money"] is True
        assert gameplay["safety"]["no_brand_ads"] is True


def test_every_pool_is_local_single_solution_and_age_aware():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert sum(f"culture:{language}" in row["culture_tags"] for row in rows) == 200
            assert len({row["market"] for row in rows}) == 5
            assert {row["special_event"] for row in rows} == builder.EVENTS
            assert all(len(builder._solutions(row, builder.PROFILE[band])) == 1 for row in rows)
    young = json.loads(builder.gameplay_config("colorful-market", "young"))
    senior = json.loads(builder.gameplay_config("colorful-market", "senior"))
    assert young["round"]["basket_size"] == 2
    assert senior["round"]["basket_size"] == 4


def test_wrong_pool_size_fails_openly(monkeypatch):
    monkeypatch.setattr(builder, "PER_POOL", 201)
    with pytest.raises(builder.ColorfulMarketBuildError, match="expected 201 puzzles"):
        builder._load_pool("tr", "young")


def test_second_valid_basket_is_rejected(monkeypatch):
    rows = builder._load_pool("tr", "young")
    broken = [dict(row) for row in rows]
    offers = [dict(item) for item in broken[0]["offers"]]
    solution_prices = [item["price"] for item in offers
                       if item["product_id"] in broken[0]["solution_basket"]]
    outsiders = [item for item in offers if item["product_id"] not in broken[0]["solution_basket"]]
    outsiders[0]["price"], outsiders[1]["price"] = solution_prices
    outsiders[0]["category"] = broken[0]["required_categories"][0]
    broken[0] = {**broken[0], "offers": offers}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.ColorfulMarketBuildError, match="invalid market puzzle"):
        builder._load_pool("tr", "young")


def test_invalid_coupon_is_rejected_cleanly(monkeypatch):
    rows = builder._load_pool("tr", "mid")
    broken = [dict(row) for row in rows]
    broken[0] = {**broken[0], "coupon": {**broken[0]["coupon"], "discount": 9}}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.ColorfulMarketBuildError, match="invalid market puzzle"):
        builder._load_pool("tr", "mid")
