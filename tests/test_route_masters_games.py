from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_route_masters_games", ROOT / "tools" / "build_route_masters_games.py"
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_solvable_missions():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "route-masters" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["mission_count"] for item in catalog["games"]) == 7200


def test_packages_include_boards_rules_visuals_and_match_catalog():
    catalog = json.loads((ROOT / "games" / "route-masters" / "catalog.json").read_text(encoding="utf-8"))
    for item in catalog["games"]:
        path = ROOT / item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
        with zipfile.ZipFile(path) as archive:
            assert set(archive.namelist()) == {
                "manifest.json", "data/missions.json", "data/gameplay.json",
                "visual/game_art.webp", "visual/theme.json",
            }
            manifest = json.loads(archive.read("manifest.json"))
            missions = json.loads(archive.read("data/missions.json"))
            gameplay = json.loads(archive.read("data/gameplay.json"))
            theme = json.loads(archive.read("visual/theme.json"))
        assert manifest["game_type"] == "route_masters"
        assert len(missions) == 200
        assert all(set(mission) == set(builder.RUNTIME_FIELDS) for mission in missions)
        assert all(builder._distance(mission["openings"], mission["board_size"],
                                     mission["start"], mission["goal"]) == mission["optimal_moves"]
                   for mission in missions)
        assert all(mission["move_limit"] >= mission["optimal_actions"] for mission in missions)
        assert gameplay["modes"] == ["solo_path", "family_coop", "treasure_race", "program_route"]
        assert gameplay["safety"]["no_player_elimination"] is True
        assert len(gameplay["events"]) == 5
        assert theme["accessibility"]["color_only_feedback"] is False


def test_every_pool_is_unique_local_and_age_rules_really_change():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert len({tuple(row["openings"]) for row in rows}) == 200
            assert sum(f"culture:{language}" in row["culture_tags"] for row in rows) == 200
            assert len({(row["hero"], row["setting"], row["treasure"]) for row in rows}) == 5
    young = json.loads(builder.gameplay_config("route-masters", "young"))
    senior = json.loads(builder.gameplay_config("route-masters", "senior"))
    assert young["round"]["board_size"] == 5
    assert young["round"]["path_preview"] is True
    assert senior["round"]["board_size"] == 8
    assert senior["round"]["rotatable_tiles"] == 4


def test_wrong_pool_size_fails_openly(monkeypatch):
    monkeypatch.setattr(builder, "PER_POOL", 201)
    with pytest.raises(builder.RouteMastersBuildError, match="expected 201 missions"):
        builder._load_pool("tr", "young")


def test_broken_corridor_is_rejected(monkeypatch):
    rows = builder._load_pool("tr", "young")
    broken = [dict(row) for row in rows]
    broken[0] = {**broken[0], "openings": [0] * 25}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.RouteMastersBuildError, match="invalid mission"):
        builder._load_pool("tr", "young")
