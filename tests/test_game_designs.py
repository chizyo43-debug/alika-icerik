from __future__ import annotations

import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT / "tools"))
import game_visuals
from gameplay_designs import gameplay_config
from word_wheel_design import LABELS, wheel_config


def test_every_current_game_has_rich_age_aware_play_and_visual_design():
    games = ("trivia", "memory", "who-is-it", "taboo", "liar")
    bands = ("young", "mid", "teen", "senior")
    for game in games:
        for band in bands:
            gameplay = json.loads(gameplay_config(game, band))
            visuals = game_visuals.visual_payloads(game, band)
            theme = json.loads(visuals["visual/theme.json"])
            assert len(gameplay["modes"]) >= 3
            assert len(gameplay["events"]) >= 3
            assert gameplay["principles"]["no_real_money"] is True
            assert theme["accessibility"]["color_only_feedback"] is False
            assert len(visuals["visual/game_art.webp"]) < 300_000


def test_word_wheel_has_local_labels_and_24_fair_equal_segments():
    assert set(LABELS) == {"tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko"}
    for language in LABELS:
        config = json.loads(wheel_config(language, "mid"))
        assert len(config["segments"]) == config["segment_count"] == 24
        assert config["fairness"]["equal_slice_angles"] is True
        assert config["fairness"]["result_committed_before_animation"] is True
        assert all(segment["label"] for segment in config["segments"])


def test_missing_visual_asset_fails_openly(monkeypatch, tmp_path):
    monkeypatch.setattr(game_visuals, "ROOT", tmp_path)
    with pytest.raises(ValueError, match="missing visual asset"):
        game_visuals.visual_payloads("trivia", "young")
