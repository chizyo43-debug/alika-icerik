from __future__ import annotations

import importlib.util
import json
import os
import sys
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_who_is_it_games", ROOT / "tools" / "build_who_is_it_games.py",
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_people():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "who-is-it" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["identity_count"] for item in catalog["games"]) == 7200


def test_packages_are_data_only_and_hide_answers_from_clues():
    catalog = json.loads((ROOT / "games" / "who-is-it" / "catalog.json").read_text(encoding="utf-8"))
    for item in catalog["games"]:
        with zipfile.ZipFile(ROOT / item["path"]) as archive:
            assert set(archive.namelist()) == {
                "manifest.json", "data/identities.json", "visual/game_art.webp",
                "visual/theme.json", "data/gameplay.json",
            }
            manifest = json.loads(archive.read("manifest.json"))
            identities = json.loads(archive.read("data/identities.json"))
        assert manifest["game_type"] == "who_is_it"
        assert len(identities) == 200
        assert all(set(row) == set(builder.RUNTIME_FIELDS) for row in identities)
        assert all(len(row["clues"]) == 4 for row in identities)
        assert all(builder._key(row["answer"]) not in builder._key(clue)
                   for row in identities for clue in row["clues"])


def test_each_language_has_four_distinct_age_pools():
    for language in builder.LANGUAGES:
        pools = [frozenset(row["answer"] for row in builder._load_pool(language, band))
                 for band in builder.BANDS]
        assert len(set(pools)) == 4


def test_every_source_is_traceable_to_wikidata():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            assert all(row["source"]["url"].startswith("https://www.wikidata.org/wiki/Q")
                       for row in builder._load_pool(language, band))


def test_packages_round_trip_through_real_alika_reader(monkeypatch):
    raw = os.environ.get("ALIKA_APP_REPO", "").strip()
    if not raw:
        pytest.skip("ALIKA_APP_REPO verilmedi; gerçek oyun okuyucu kapısı atlandı.")
    windows = Path(raw).resolve() / "windows"
    monkeypatch.syspath_prepend(str(windows))
    sys.modules.pop("library", None)
    from library.game_package import game_identities, read_game_package_file

    paths = sorted((ROOT / "games" / "who-is-it" / "dist").rglob("*.alika-game"))
    assert len(paths) == 36
    for path in paths:
        package = read_game_package_file(path)
        assert len(game_identities(package)) == 200
