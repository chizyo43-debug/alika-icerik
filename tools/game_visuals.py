"""Shared visual themes and downloadable presentation assets for AliKa games."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

GAME_STYLES: dict[str, dict[str, Any]] = {
    "trivia": {
        "accent": "#14D9FF", "accent_2": "#FF4FD8", "highlight": "#FFD447",
        "correct": "#39E58C", "wrong": "#FF5470", "card": "#17224D",
    },
    "memory": {
        "accent": "#8B5CFF", "accent_2": "#23D5E8", "highlight": "#FFCF5A",
        "correct": "#3CE6A0", "wrong": "#FF6B81", "card": "#25205A",
    },
    "word-wheel": {
        "accent": "#00D7FF", "accent_2": "#FF3DBB", "highlight": "#FFE04B",
        "correct": "#38E895", "wrong": "#FF526D", "card": "#152756",
    },
    "who-is-it": {
        "accent": "#4FD8FF", "accent_2": "#FFB84A", "highlight": "#F4ED65",
        "correct": "#3BE39B", "wrong": "#FF607D", "card": "#19305D",
    },
    "taboo": {
        "accent": "#FF536E", "accent_2": "#8E5CFF", "highlight": "#FFD554",
        "correct": "#35E7A1", "wrong": "#FF405F", "card": "#381B55",
    },
    "liar": {
        "accent": "#A968FF", "accent_2": "#20D9D2", "highlight": "#FFD34E",
        "correct": "#3BE8A0", "wrong": "#FF4D70", "card": "#231C52",
    },
    "charades": {
        "accent": "#00D5FF", "accent_2": "#FF4DB8", "highlight": "#FFD34A",
        "correct": "#38E69A", "wrong": "#FF5A72", "card": "#202158",
    },
    "draw-guess": {
        "accent": "#18CFFF", "accent_2": "#FF4AAB", "highlight": "#FFC83D",
        "correct": "#31E59A", "wrong": "#FF536F", "card": "#1A2458",
    },
    "story-adventure": {
        "accent": "#16D8FF", "accent_2": "#F34DFF", "highlight": "#FFCB45",
        "correct": "#3AE8A2", "wrong": "#FF5876", "card": "#24205C",
    },
    "word-hunt": {
        "accent": "#15D8FF", "accent_2": "#FF4DC8", "highlight": "#FFD052",
        "correct": "#37E69B", "wrong": "#FF5874", "card": "#18295C",
    },
    "route-masters": {
        "accent": "#12D9F4", "accent_2": "#A84DFF", "highlight": "#FFD24A",
        "correct": "#38E79B", "wrong": "#FF5B73", "card": "#15345B",
    },
    "rhythm-stage": {
        "accent": "#18D9FF", "accent_2": "#FF45C8", "highlight": "#FFD24F",
        "correct": "#39E99D", "wrong": "#FF5878", "card": "#24215C",
    },
    "balance-workshop": {
        "accent": "#19D9FF", "accent_2": "#FF5A75", "highlight": "#FFD34F",
        "correct": "#39E89C", "wrong": "#FF526E", "card": "#1D2858",
    },
    "garden-masters": {
        "accent": "#19D9FF", "accent_2": "#68E35D", "highlight": "#FFD44F",
        "correct": "#35E99A", "wrong": "#FF5A72", "card": "#173A55",
    },
    "light-laboratory": {
        "accent": "#18D9FF", "accent_2": "#B85CFF", "highlight": "#FFD34D",
        "correct": "#3AE99D", "wrong": "#FF5775", "card": "#172654",
    },
    "robot-coding-arena": {
        "accent": "#16D9FF", "accent_2": "#A95CFF", "highlight": "#FFD23F",
        "correct": "#58E65D", "wrong": "#FF5B70", "card": "#172758",
    },
    "colorful-market": {
        "accent": "#22D4CE", "accent_2": "#FF7186", "highlight": "#FFD34E",
        "correct": "#60DF6A", "wrong": "#FF5B70", "card": "#283065",
    },
    "family-escape-night": {
        "accent": "#20D8EA", "accent_2": "#A95BFF", "highlight": "#FFD044",
        "correct": "#55E092", "wrong": "#FF6178", "card": "#252052",
    },
}


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def visual_payloads(game: str, band: str) -> dict[str, bytes]:
    """Return the shared art plus an age-adjusted in-game theme."""
    style = GAME_STYLES[game]
    art_path = ROOT / "games" / "visuals" / game / "game_art.webp"
    try:
        art = art_path.read_bytes()
    except OSError as exc:
        raise ValueError(f"missing visual asset: {art_path.relative_to(ROOT)}") from exc
    if not art.startswith(b"RIFF") or len(art) > 300_000:
        raise ValueError(f"invalid or oversized visual asset: {art_path.relative_to(ROOT)}")

    age_tone = {
        "young": {"motion": "playful", "glow": 0.92, "density": "low"},
        "mid": {"motion": "energetic", "glow": 0.82, "density": "medium"},
        "teen": {"motion": "dynamic", "glow": 0.72, "density": "medium"},
        "senior": {"motion": "confident", "glow": 0.62, "density": "high"},
    }[band]
    theme = {
        "schema_version": 1,
        "art": {"background": "visual/game_art.webp", "overlay_opacity": 0.22},
        "palette": {"background": "#08122F", "text": "#FFFFFF", **style},
        "cards": {"corner_radius": 22, "border_width": 2, "glow": age_tone["glow"],
                  "press_scale": 0.97, "reveal_ms": 320},
        "feedback": {"correct_burst": True, "wrong_shake": True,
                     "streak_confetti": 3, "score_pop_ms": 520},
        "motion": {"tone": age_tone["motion"], "content_density": age_tone["density"],
                   "reduce_motion_supported": True},
        "accessibility": {"minimum_contrast": "AA", "color_only_feedback": False,
                          "large_touch_targets": True},
    }
    return {"visual/game_art.webp": art, "visual/theme.json": _json_bytes(theme)}


def asset_records(payloads: dict[str, bytes]) -> list[dict[str, Any]]:
    """Create manifest records for visual or configuration payloads."""
    records = []
    for path, payload in payloads.items():
        asset_type = "image" if path.endswith(".webp") else "config"
        records.append({"path": path, "sha256": hashlib.sha256(payload).hexdigest(),
                        "asset_type": asset_type, "size_bytes": len(payload)})
    return records
