from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_light_laboratory_games", ROOT / "tools" / "build_light_laboratory_games.py"
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_solvable_puzzles():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "light-laboratory" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["puzzle_count"] for item in catalog["games"]) == 7200


def test_packages_include_optics_rules_visuals_and_match_catalog():
    catalog = json.loads((ROOT / "games" / "light-laboratory" / "catalog.json").read_text(encoding="utf-8"))
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
        assert manifest["game_type"] == "light_laboratory"
        assert len(puzzles) == 200
        assert all(set(puzzle) == set(builder.RUNTIME_FIELDS) for puzzle in puzzles)
        assert gameplay["modes"] == ["beam_builder", "family_coop", "duo_circuit", "spectrum_challenge"]
        assert gameplay["optics"]["safe_enclosed_beams"] is True
        assert gameplay["safety"]["no_real_laser_instruction"] is True
        assert theme["accessibility"]["color_only_feedback"] is False


def test_every_pool_is_unique_local_traced_and_age_aware():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert len({tuple(row["solution_path"]) for row in rows}) == 200
            assert sum(f"culture:{language}" in row["culture_tags"] for row in rows) == 200
            assert len({(row["laboratory"], row["artifact"]) for row in rows}) == 5
            assert {row["special_event"] for row in rows} == builder.EVENTS
            assert all(builder._trace_valid(row, builder.PROFILE[band]) for row in rows)
    young = json.loads(builder.gameplay_config("light-laboratory", "young"))
    senior = json.loads(builder.gameplay_config("light-laboratory", "senior"))
    assert young["round"]["board_size"] == 5
    assert young["round"]["beam_preview"] is True
    assert senior["round"]["board_size"] == 8
    assert senior["round"]["rotatable_mirrors"] == 4


def test_wrong_pool_size_fails_openly(monkeypatch):
    monkeypatch.setattr(builder, "PER_POOL", 201)
    with pytest.raises(builder.LightLaboratoryBuildError, match="expected 201 puzzles"):
        builder._load_pool("tr", "young")


def test_broken_light_path_is_rejected(monkeypatch):
    rows = builder._load_pool("tr", "young")
    broken = [dict(row) for row in rows]
    path = list(broken[0]["solution_path"])
    path[2] = path[-1]
    broken[0] = {**broken[0], "solution_path": path}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.LightLaboratoryBuildError, match="invalid light puzzle"):
        builder._load_pool("tr", "young")


def test_wrong_filter_color_is_rejected_cleanly(monkeypatch):
    rows = builder._load_pool("tr", "mid")
    broken = [dict(row) for row in rows]
    elements = [dict(element) for element in broken[0]["elements"]]
    filter_element = next(element for element in elements if element["type"] == "filter")
    filter_element["color"] = next(color for color in builder.COLORS
                                   if color != broken[0]["emitter_color"])
    broken[0] = {**broken[0], "elements": elements}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.LightLaboratoryBuildError, match="invalid light puzzle"):
        builder._load_pool("tr", "mid")
