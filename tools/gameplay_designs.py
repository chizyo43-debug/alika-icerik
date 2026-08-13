"""Researched, age-aware play variants shared by downloadable game packages."""
from __future__ import annotations

import json
from typing import Any


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def gameplay_config(game: str, band: str) -> bytes:
    young = band == "young"
    base: dict[str, Any] = {
        "schema_version": 1,
        "age_profile": band,
        "principles": {
            "short_turns": True, "player_choice": True, "comeback_possible": True,
            "no_real_money": True, "no_humiliation": True,
            "reduced_motion_supported": True,
        },
    }
    designs: dict[str, dict[str, Any]] = {
        "trivia": {
            "modes": ["classic", "quick_5", "family_team"],
            "round": {"default_questions": 10, "answer_seconds": 20 if young else 15,
                      "category_choice_every": 3},
            "bonuses": {"streak_starts_at": 3, "streak_bonus": 50,
                        "hint_tokens": 2 if young else 1,
                        "second_chance": young},
            "events": ["double_score_question", "team_consult", "category_choice",
                       "fast_finish_bonus"],
        },
        "memory": {
            "modes": ["classic", "reaction", "solo_time", "cooperative"],
            "board": {"visible_pairs": {"young": 8, "mid": 12, "teen": 16, "senior": 20}[band],
                      "preview_seconds": 4 if young else 2},
            "bonuses": {"match_grants_extra_turn": True, "combo_after_matches": 2,
                        "hint_tokens": 2 if young else 1},
            "events": ["shuffle_two_unmatched", "peek_one", "golden_pair"],
        },
        "who-is-it": {
            "modes": ["progressive_clues", "yes_no_duel", "team_detective"],
            "round": {"question_limit": 12 if young else 10, "clue_count": 4,
                      "wrong_guess_ends_round": not young},
            "bonuses": {"early_guess_multiplier": [4, 3, 2, 1],
                        "safe_guess_token": 1 if young else 0},
            "events": ["extra_clue", "remove_two_options", "one_question_free"],
        },
        "taboo": {
            "modes": ["classic", "one_guesser", "all_play", "cooperative"],
            "round": {"seconds": 75 if young else 60, "pass_tokens": 3 if young else 2,
                      "forbidden_word_penalty": 0 if young else 1},
            "events": ["double_point_card", "one_guesser", "silent_gesture_forbidden",
                       "team_rescue"],
            "safety": {"no_mocking_cards": True, "skip_without_explanation": True},
        },
        "liar": {
            "modes": ["spot_the_lie", "team_detectives", "host_challenge"],
            "round": {"vote_seconds": 25 if young else 18, "explanation_reveal": True,
                      "private_vote": True},
            "bonuses": {"streak_starts_at": 2, "reason_bonus": True,
                        "second_vote": young},
            "events": ["double_detective", "ask_for_clue", "team_consult",
                       "swap_one_statement"],
            "safety": {"facts_not_personal_accusations": True, "no_player_is_called_liar": True},
        },
    }
    base.update(designs[game])
    return _json_bytes(base)
