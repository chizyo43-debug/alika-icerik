from __future__ import annotations

import importlib.util
import json
import os
import sys
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_memory_games", ROOT / "tools" / "build_memory_games.py")
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_language_age_pools_build_and_generated_files_are_current():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "memory" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["review_status"] == "ai-draft"
    assert catalog["human_approved"] is False
    assert len(catalog["games"]) == 36
    assert sum(item["pair_count"] for item in catalog["games"]) == 3600


def test_archives_are_data_only_and_match_catalog():
    catalog = json.loads((ROOT / "games" / "memory" / "catalog.json").read_text(encoding="utf-8"))
    for item in catalog["games"]:
        with zipfile.ZipFile(ROOT / item["path"]) as archive:
            assert set(archive.namelist()) == {
                "manifest.json", "data/cards.json", "visual/game_art.webp",
                "visual/theme.json", "data/gameplay.json",
            }
            assert all(info.compress_type == zipfile.ZIP_STORED for info in archive.infolist())
            assert all(info.create_system == 3 for info in archive.infolist())
            manifest = json.loads(archive.read("manifest.json"))
            cards = json.loads(archive.read("data/cards.json"))
        assert manifest["game_type"] == "memory_cards"
        assert manifest["language"] == item["language"]
        assert len(cards) == builder.PAIRS
        assert all(set(card) == set(builder.RUNTIME_FIELDS) for card in cards)


def test_each_language_has_four_distinct_age_pools():
    for language in builder.LANGUAGES:
        pools = []
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            pools.append(frozenset((row["left"], row["right"]) for row in rows))
        assert len(set(pools)) == len(builder.BANDS)


def test_archives_round_trip_through_real_alika_reader_when_available(monkeypatch):
    raw = os.environ.get("ALIKA_APP_REPO", "").strip()
    if not raw:
        pytest.skip("ALIKA_APP_REPO verilmedi; gerçek oyun okuyucu kapısı atlandı.")
    windows = Path(raw).resolve() / "windows"
    if not (windows / "library" / "game_package.py").is_file():
        raise AssertionError(f"AliKa Windows kaynak yolu geçersiz: {windows}")
    monkeypatch.syspath_prepend(str(windows))
    sys.modules.pop("library", None)
    from library.game_package import game_cards, read_game_package_file

    paths = sorted((ROOT / "games" / "memory" / "dist").rglob("*.alika-game"))
    assert len(paths) == 36
    for path in paths:
        package = read_game_package_file(path)
        assert len(game_cards(package)) == builder.PAIRS
