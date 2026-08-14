from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_family_escape_games", ROOT / "tools" / "build_family_escape_games.py"
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_single_solution_mysteries():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "family-escape-night" / "catalog.json")
                         .read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["puzzle_count"] for item in catalog["games"]) == 7200


def test_packages_include_cooperative_rules_visuals_and_match_catalog():
    catalog = json.loads((ROOT / "games" / "family-escape-night" / "catalog.json")
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
        assert manifest["game_type"] == "family_escape"
        assert len(puzzles) == 200
        assert all(set(puzzle) == set(builder.RUNTIME_FIELDS) for puzzle in puzzles)
        assert gameplay["cooperation"]["shared_team_goal"] is True
        assert gameplay["round"]["timer_default_on"] is False
        assert gameplay["safety"]["no_player_elimination"] is True


def test_every_pool_is_local_unique_solvable_and_age_aware():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert sum(f"culture:{language}" in row["culture_tags"] for row in rows) == 200
            assert len({(row["room"], row["treasure"]) for row in rows}) == 5
            assert {row["special_event"] for row in rows} == builder.EVENTS
            assert all(len(builder._solutions(row, builder.PROFILE[band])) == 1 for row in rows)
    young = json.loads(builder.gameplay_config("family-escape-night", "young"))
    senior = json.loads(builder.gameplay_config("family-escape-night", "senior"))
    assert young["round"]["symbol_count"] == 3
    assert young["round"]["hint_tokens"] == 4
    assert senior["round"]["symbol_count"] == 6


def test_wrong_pool_size_fails_openly(monkeypatch):
    monkeypatch.setattr(builder, "PER_POOL", 201)
    with pytest.raises(builder.FamilyEscapeBuildError, match="expected 201 puzzles"):
        builder._load_pool("tr", "young")


def test_ambiguous_clue_set_is_rejected(monkeypatch):
    rows = builder._load_pool("tr", "young")
    broken = [dict(row) for row in rows]
    symbol = broken[0]["solution_code"][0]
    clues = [{"type": "position", "symbol": symbol, "position": 0},
             {"type": "before", "first": symbol, "second": broken[0]["solution_code"][1]},
             {"type": "before", "first": symbol, "second": broken[0]["solution_code"][2]}]
    broken[0] = {**broken[0], "clues": clues}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.FamilyEscapeBuildError, match="invalid escape mystery"):
        builder._load_pool("tr", "young")


def test_invalid_symbol_reference_is_rejected_cleanly(monkeypatch):
    rows = builder._load_pool("tr", "mid")
    broken = [dict(row) for row in rows]
    clues = [dict(clue) for clue in broken[0]["clues"]]
    reference = next(key for key in clues[0] if key not in {"type", "position", "distance"})
    clues[0][reference] = "unknown"
    broken[0] = {**broken[0], "clues": clues}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.FamilyEscapeBuildError, match="invalid escape mystery"):
        builder._load_pool("tr", "mid")
