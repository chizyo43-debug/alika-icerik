from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_garden_masters_games", ROOT / "tools" / "build_garden_masters_games.py"
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_solvable_missions():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "garden-masters" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["mission_count"] for item in catalog["games"]) == 7200


def test_packages_include_gardens_rules_visuals_and_match_catalog():
    catalog = json.loads((ROOT / "games" / "garden-masters" / "catalog.json").read_text(encoding="utf-8"))
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
        assert manifest["game_type"] == "garden_masters"
        assert len(missions) == 200
        assert all(set(mission) == set(builder.RUNTIME_FIELDS) for mission in missions)
        assert gameplay["modes"] == ["garden_builder", "family_coop", "harvest_race", "weather_challenge"]
        assert gameplay["safety"]["no_pesticides"] is True
        assert gameplay["safety"]["no_player_elimination"] is True
        assert theme["accessibility"]["color_only_feedback"] is False


def test_every_pool_is_unique_local_solvable_and_age_aware():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert len({json.dumps((row["cells"], row["plants"], row["solution"]),
                                   sort_keys=True) for row in rows}) == 200
            assert sum(f"culture:{language}" in row["culture_tags"] for row in rows) == 200
            assert len({(row["garden"], row["garden_style"]) for row in rows}) == 5
            assert {row["special_event"] for row in rows} == builder.EVENTS
            assert all(builder._score(row["plants"], row["cells"], row["solution"],
                                      row["board_size"], row["special_event"],
                                      row["event_cells"]) == row["target_score"] for row in rows)
    young = json.loads(builder.gameplay_config("garden-masters", "young"))
    senior = json.loads(builder.gameplay_config("garden-masters", "senior"))
    assert young["round"]["board_size"] == 3
    assert young["round"]["solution_preview"] is True
    assert senior["round"]["board_size"] == 6
    assert senior["round"]["plant_count"] == 10


def test_wrong_pool_size_fails_openly(monkeypatch):
    monkeypatch.setattr(builder, "PER_POOL", 201)
    with pytest.raises(builder.GardenMastersBuildError, match="expected 201 missions"):
        builder._load_pool("tr", "young")


def test_unsuitable_solution_is_rejected(monkeypatch):
    rows = builder._load_pool("tr", "young")
    broken = [dict(row) for row in rows]
    cells = [dict(cell) for cell in broken[0]["cells"]]
    solution_cell = broken[0]["solution"][0]["cell"]
    cells[solution_cell]["sun"] = 1 if cells[solution_cell]["sun"] != 1 else 3
    broken[0] = {**broken[0], "cells": cells}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.GardenMastersBuildError, match="invalid garden mission"):
        builder._load_pool("tr", "young")


def test_malformed_plant_is_rejected_cleanly(monkeypatch):
    rows = builder._load_pool("tr", "young")
    broken = [dict(row) for row in rows]
    plants = [dict(plant) for plant in broken[0]["plants"]]
    plants[0]["water_cost"] = "many"
    broken[0] = {**broken[0], "plants": plants}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.GardenMastersBuildError, match="invalid garden mission"):
        builder._load_pool("tr", "young")
