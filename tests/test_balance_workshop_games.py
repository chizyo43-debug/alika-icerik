from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_balance_workshop_games", ROOT / "tools" / "build_balance_workshop_games.py"
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_all_languages_and_age_groups_have_200_balanced_challenges():
    builder.build(check=True)
    catalog = json.loads((ROOT / "games" / "balance-workshop" / "catalog.json").read_text(encoding="utf-8"))
    assert catalog["human_approved"] is False
    assert catalog["review_status"] == "ai-draft"
    assert len(catalog["games"]) == 36
    assert sum(item["challenge_count"] for item in catalog["games"]) == 7200


def test_packages_include_constructions_rules_visuals_and_match_catalog():
    catalog = json.loads((ROOT / "games" / "balance-workshop" / "catalog.json").read_text(encoding="utf-8"))
    for item in catalog["games"]:
        path = ROOT / item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
        with zipfile.ZipFile(path) as archive:
            assert set(archive.namelist()) == {
                "manifest.json", "data/challenges.json", "data/gameplay.json",
                "visual/game_art.webp", "visual/theme.json",
            }
            manifest = json.loads(archive.read("manifest.json"))
            challenges = json.loads(archive.read("data/challenges.json"))
            gameplay = json.loads(archive.read("data/gameplay.json"))
            theme = json.loads(archive.read("visual/theme.json"))
        assert manifest["game_type"] == "balance_workshop"
        assert len(challenges) == 200
        assert all(set(challenge) == set(builder.RUNTIME_FIELDS) for challenge in challenges)
        assert gameplay["modes"] == ["free_build", "family_coop", "turn_by_turn", "blueprint_challenge"]
        assert gameplay["physics"]["center_of_mass_line"] is True
        assert gameplay["safety"]["no_player_elimination"] is True
        assert theme["accessibility"]["color_only_feedback"] is False


def test_every_pool_is_unique_local_balanced_and_age_aware():
    for language in builder.LANGUAGES:
        for band in builder.BANDS:
            rows = builder._load_pool(language, band)
            assert len({json.dumps((row["pieces"], row["solution"]), sort_keys=True) for row in rows}) == 200
            assert sum(f"culture:{language}" in row["culture_tags"] for row in rows) == 200
            assert len({(row["workshop"], row["material"], row["ornament"]) for row in rows}) == 5
            assert {row["special_event"] for row in rows} == builder.EVENTS
            assert {row["construction_type"] for row in rows} == builder.STRUCTURES
            assert all(builder._valid_geometry(row, builder.PROFILE[band]) for row in rows)
    young = json.loads(builder.gameplay_config("balance-workshop", "young"))
    senior = json.loads(builder.gameplay_config("balance-workshop", "senior"))
    assert young["round"]["piece_count"] == 5
    assert young["round"]["placement_seconds"] == 0
    assert senior["round"]["piece_count"] == 11
    assert senior["physics"]["snap_assist"] is False


def test_wrong_pool_size_fails_openly(monkeypatch):
    monkeypatch.setattr(builder, "PER_POOL", 201)
    with pytest.raises(builder.BalanceWorkshopBuildError, match="expected 201 challenges"):
        builder._load_pool("tr", "young")


def test_unbalanced_solution_is_rejected(monkeypatch):
    rows = builder._load_pool("tr", "young")
    broken = [dict(row) for row in rows]
    bad_solution = [dict(slot) for slot in broken[0]["solution"]]
    bad_solution[0]["x"] = 3.8
    broken[0] = {**broken[0], "solution": bad_solution}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.BalanceWorkshopBuildError, match="invalid construction"):
        builder._load_pool("tr", "young")


def test_malformed_piece_is_rejected_cleanly(monkeypatch):
    rows = builder._load_pool("tr", "young")
    broken = [dict(row) for row in rows]
    bad_pieces = [dict(piece) for piece in broken[0]["pieces"]]
    bad_pieces[0]["mass"] = "heavy"
    broken[0] = {**broken[0], "pieces": bad_pieces}
    monkeypatch.setattr(builder.Path, "read_text", lambda *_args, **_kwargs:
                        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in broken))
    with pytest.raises(builder.BalanceWorkshopBuildError, match="invalid construction"):
        builder._load_pool("tr", "young")
