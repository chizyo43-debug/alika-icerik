"""Original, family-friendly AliKa studio wheel configuration."""
from __future__ import annotations

import json
from typing import Any


LABELS = {
    "tr": {"double": "2 KAT", "jackpot": "YILDIZ HAZİNESİ", "free_letter": "HARF HEDİYESİ",
           "shield": "KALKAN", "extra_turn": "EK TUR", "spin_again": "YİNE ÇEVİR",
           "mystery": "SÜRPRİZ", "lose_turn": "SIRA GEÇER", "half": "YARI PUAN",
           "bankrupt": "TUR PUANI SİLİNİR"},
    "en": {"double": "DOUBLE", "jackpot": "STAR JACKPOT", "free_letter": "FREE LETTER",
           "shield": "SHIELD", "extra_turn": "EXTRA TURN", "spin_again": "SPIN AGAIN",
           "mystery": "MYSTERY", "lose_turn": "SKIP TURN", "half": "HALF SCORE",
           "bankrupt": "ROUND POINTS LOST"},
    "de": {"double": "DOPPELT", "jackpot": "STERN-JACKPOT", "free_letter": "FREIBUCHSTABE",
           "shield": "SCHILD", "extra_turn": "EXTRARUNDE", "spin_again": "NOCHMAL DREHEN",
           "mystery": "ÜBERRASCHUNG", "lose_turn": "ZUG VERFÄLLT", "half": "HALBE PUNKTE",
           "bankrupt": "RUNDENPUNKTE WEG"},
    "es": {"double": "DOBLE", "jackpot": "BOTE ESTRELLA", "free_letter": "LETRA GRATIS",
           "shield": "ESCUDO", "extra_turn": "TURNO EXTRA", "spin_again": "GIRA OTRA VEZ",
           "mystery": "SORPRESA", "lose_turn": "PIERDE TURNO", "half": "MEDIA PUNTUACIÓN",
           "bankrupt": "PIERDE PUNTOS DE RONDA"},
    "fr": {"double": "DOUBLE", "jackpot": "JACKPOT ÉTOILE", "free_letter": "LETTRE OFFERTE",
           "shield": "BOUCLIER", "extra_turn": "TOUR EN PLUS", "spin_again": "RETOURNE",
           "mystery": "SURPRISE", "lose_turn": "TOUR PASSÉ", "half": "MOITIÉ DES POINTS",
           "bankrupt": "POINTS DE MANCHE PERDUS"},
    "pt": {"double": "DOBRO", "jackpot": "JACKPOT ESTRELA", "free_letter": "LETRA GRÁTIS",
           "shield": "ESCUDO", "extra_turn": "TURNO EXTRA", "spin_again": "GIRE DE NOVO",
           "mystery": "SURPRESA", "lose_turn": "PERDE A VEZ", "half": "METADE DOS PONTOS",
           "bankrupt": "PERDE PONTOS DA RODADA"},
    "ru": {"double": "УДВОЕНИЕ", "jackpot": "ЗВЁЗДНЫЙ ДЖЕКПОТ", "free_letter": "БУКВА В ПОДАРОК",
           "shield": "ЩИТ", "extra_turn": "ЕЩЁ ХОД", "spin_again": "КРУТИ ЕЩЁ",
           "mystery": "СЮРПРИЗ", "lose_turn": "ПРОПУСК ХОДА", "half": "ПОЛОВИНА ОЧКОВ",
           "bankrupt": "ОЧКИ РАУНДА СГОРАЮТ"},
    "ja": {"double": "2倍", "jackpot": "スタージャックポット", "free_letter": "文字プレゼント",
           "shield": "シールド", "extra_turn": "もう1回", "spin_again": "もう一度回す",
           "mystery": "サプライズ", "lose_turn": "1回休み", "half": "ポイント半分",
           "bankrupt": "ラウンド得点消失"},
    "ko": {"double": "2배", "jackpot": "별 잭팟", "free_letter": "글자 선물",
           "shield": "방패", "extra_turn": "추가 차례", "spin_again": "한 번 더 돌리기",
           "mystery": "깜짝 칸", "lose_turn": "차례 넘김", "half": "점수 절반",
           "bankrupt": "라운드 점수 삭제"},
}

COLORS = {
    "points": ["#00C8FF", "#6D5DFF", "#FF4EB8", "#FF8A3D", "#15D69C", "#F6CB3D"],
    "bonus": "#FFE14D", "safe": "#32E0A1", "risk": "#FF5876", "mystery": "#A565FF",
}


def _segment(identifier: str, kind: str, *, value: int | None = None,
             label: str | None = None, color: str) -> dict[str, Any]:
    result: dict[str, Any] = {"id": identifier, "kind": kind, "color": color}
    if value is not None:
        result["value"] = value
    result["label"] = label or str(value)
    return result


def wheel_config(language: str, band: str) -> bytes:
    labels = LABELS[language]
    values = [100, 150, 200, 250, 300, 400, 150, 200, 250, 300, 500, 200]
    segments = [_segment(f"points_{i + 1}", "points", value=value,
                         color=COLORS["points"][i % len(COLORS["points"])])
                for i, value in enumerate(values)]
    special = [
        ("double", "multiplier", 2, COLORS["bonus"]),
        ("jackpot", "jackpot", None, COLORS["bonus"]),
        ("free_letter", "free_letter", None, COLORS["safe"]),
        ("shield", "shield", None, COLORS["safe"]),
        ("extra_turn", "extra_turn", None, COLORS["safe"]),
        ("spin_again", "spin_again", None, COLORS["safe"]),
        ("mystery", "mystery", None, COLORS["mystery"]),
        ("lose_turn", "lose_turn", None, COLORS["risk"]),
        ("half", "half_round_score", None, COLORS["risk"]),
        ("bankrupt", "reset_round_score", None, "#1B1B2F"),
    ]
    for identifier, kind, value, color in special:
        segments.append(_segment(identifier, kind, value=value, label=labels[identifier], color=color))
    # Two ordinary wedges keep the wheel at a TV-studio-like 24 equal slices.
    segments.extend([
        _segment("points_13", "points", value=350, color="#00C8FF"),
        _segment("points_14", "points", value=450, color="#FF4EB8"),
    ])

    young = band == "young"
    rules = {
        "schema_version": 1, "design": "alika_studio_wheel", "segment_count": 24,
        "segments": segments,
        "scoring": {"letter_points": "wedge_value_x_revealed_count", "vowels_cost": 100,
                    "jackpot_seed": 500, "jackpot_add_per_miss": 50,
                    "bankrupt_scope": "current_round_only", "match_score_is_protected": True},
        "age_profile": {"band": band, "gentle_mode": young,
                        "bankrupt_becomes_lose_turn": young,
                        "starting_shields": 1 if young else 0,
                        "hint_after_misses": 2 if young else 3},
        "round": {"recommended_puzzles": 5, "solve_any_time": True,
                  "wrong_solve_ends_turn": True, "max_seconds": 150},
        "motion": {"minimum_turns": 4, "maximum_turns": 7, "duration_ms": 4200,
                   "deceleration": "ease_out_quint", "pointer_tick": True,
                   "reduced_motion_duration_ms": 700},
        "fairness": {"equal_slice_angles": True, "server_or_host_selects_result": True,
                     "result_committed_before_animation": True, "no_real_money": True},
    }
    return (json.dumps(rules, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")
