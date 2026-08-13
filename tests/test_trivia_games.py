from __future__ import annotations

import importlib.util
import json
import os
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_trivia_games", ROOT / "tools" / "build_trivia_games.py"
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_language_age_pools_build_and_generated_files_are_current():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "trivia" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["review_status"] == "ai-draft"
    assert catalog["human_approved"] is False
    assert len(catalog["games"]) == 36
    assert sum(item["question_count"] for item in catalog["games"]) == 7200
    assert {(item["language"], item["age_min"], item["age_max"]) for item in catalog["games"]} == {
        (language, ages[0], ages[1])
        for language in builder.LANGUAGES
        for ages in builder.BANDS.values()
    }


def test_archives_are_data_only_and_match_catalog():
    catalog = json.loads((ROOT / "games" / "trivia" / "catalog.json").read_text(encoding="utf-8"))
    for item in catalog["games"]:
        path = ROOT / item["path"]
        with zipfile.ZipFile(path) as archive:
            assert set(archive.namelist()) == {
                "manifest.json", "data/questions.json", "visual/game_art.webp",
                "visual/theme.json", "data/gameplay.json",
            }
            assert all(info.compress_type == zipfile.ZIP_STORED for info in archive.infolist())
            assert all(info.create_system == 3 for info in archive.infolist())
            manifest = json.loads(archive.read("manifest.json"))
            questions = json.loads(archive.read("data/questions.json"))
            theme = json.loads(archive.read("visual/theme.json"))
            gameplay = json.loads(archive.read("data/gameplay.json"))
        assert manifest["game_type"] == "quiz_race"
        assert manifest["language"] == item["language"]
        assert manifest["age_min"] == item["age_min"]
        assert manifest["age_max"] == item["age_max"]
        assert len(questions) == 200
        assert all(set(question) == set(builder.QUESTION_FIELDS) for question in questions)
        assert theme["feedback"]["correct_burst"] is True
        assert theme["motion"]["reduce_motion_supported"] is True
        assert gameplay["modes"] == ["classic", "quick_5", "family_team"]
        assert len(gameplay["events"]) >= 4


def test_archives_round_trip_through_real_alika_reader_when_available(monkeypatch):
    raw = os.environ.get("ALIKA_APP_REPO", "").strip()
    if not raw:
        import pytest
        pytest.skip("ALIKA_APP_REPO verilmedi; gerçek oyun okuyucu kapısı atlandı.")
    windows = Path(raw).resolve() / "windows"
    if not (windows / "library" / "game_package.py").is_file():
        raise AssertionError(f"AliKa Windows kaynak yolu geçersiz: {windows}")
    monkeypatch.syspath_prepend(str(windows))
    sys.modules.pop("library", None)
    from library.game_package import game_questions, read_game_package_file

    paths = sorted((ROOT / "games" / "trivia" / "dist").rglob("*.alika-game"))
    assert len(paths) == 36
    for path in paths:
        package = read_game_package_file(path)
        assert len(game_questions(package)) == 200
