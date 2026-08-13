from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_robot_coding_games", ROOT / "tools" / "build_robot_coding_games.py"
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_executable_programs():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "robot-coding-arena" / "catalog.json")
                         .read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["puzzle_count"] for item in catalog["games"]) == 7200


def test_packages_include_program_rules_visuals_and_match_catalog():
    catalog = json.loads((ROOT / "games" / "robot-coding-arena" / "catalog.json")
                         .read_text(encoding="utf-8"))
    for item in catalog["games"]:
        path = ROOT / item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
        with zipfile.ZipFile(path) as archive:
            assert set(archive.namelist()) == {
                "manifest.json", "data/puzzles.json", "data/gameplay.json",
                "visual/game_art.webp", "visual/theme.json",
            }
            manifest = json.loads(archive.read("manifest.json"))
            puzzles = json.loads(archive.read("data/puzzles.json"))
            gameplay = json.loads(archive.read("data/gameplay.json"))
            theme = json.loads(archive.read("visual/theme.json"))
        assert manifest["game_type"] == "robot_coding"
        assert len(puzzles) == 200
        assert all(set(puzzle) == set(builder.RUNTIME_FIELDS) for puzzle in puzzles)
        assert gameplay["modes"] == ["code_mission", "family_debug", "duo_program",
                                     "efficiency_challenge"]
        assert gameplay["coding"]["step_by_step_run"] is True
        assert gameplay["safety"]["mistakes_are_reversible"] is True
        assert theme["accessibility"]["color_only_feedback"] is False


def test_every_pool_is_unique_local_executable_and_age_aware():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert len({tuple(row["solution_path"]) for row in rows}) == 200
            assert sum(f"culture:{language}" in row["culture_tags"] for row in rows) == 200
            assert len({(row["arena"], row["mission_item"]) for row in rows}) == 5
            assert {row["special_event"] for row in rows} == builder.EVENTS
            assert all(builder._program_valid(row, builder.PROFILE[band]) for row in rows)
    young = json.loads(builder.gameplay_config("robot-coding-arena", "young"))
    senior = json.loads(builder.gameplay_config("robot-coding-arena", "senior"))
    assert young["round"]["board_size"] == 5
    assert young["round"]["loop_blocks"] == 0
    assert senior["round"]["board_size"] == 8
    assert senior["round"]["condition_blocks"] == 2


def test_wrong_pool_size_fails_openly(monkeypatch):
    monkeypatch.setattr(builder, "PER_POOL", 201)
    with pytest.raises(builder.RobotCodingBuildError, match="expected 201 puzzles"):
        builder._load_pool("tr", "young")


def test_program_that_hits_an_obstacle_is_rejected(monkeypatch):
    rows = builder._load_pool("tr", "young")
    broken = [dict(row) for row in rows]
    broken[0] = {**broken[0], "obstacles": [broken[0]["solution_path"][1],
                                             *broken[0]["obstacles"][1:]]}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.RobotCodingBuildError, match="invalid robot program"):
        builder._load_pool("tr", "young")


def test_wrong_condition_color_is_rejected_cleanly(monkeypatch):
    rows = builder._load_pool("tr", "teen")
    broken = [dict(row) for row in rows]
    gates = [dict(gate) for gate in broken[0]["sensor_gates"]]
    gates[0]["color"] = next(color for color in builder.COLORS if color != gates[0]["color"])
    broken[0] = {**broken[0], "sensor_gates": gates}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.RobotCodingBuildError, match="invalid robot program"):
        builder._load_pool("tr", "teen")
