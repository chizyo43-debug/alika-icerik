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
        "charades": {
            "modes": ["classic_team", "quick_5", "family_coop", "spotlight_chain"],
            "round": {"seconds": 90 if young else 60, "cards_per_turn": 5,
                      "pass_tokens": 3 if young else 2, "sound_allowed": False,
                      "speaking_allowed": False, "mouth_spelling_allowed": False},
            "bonuses": {"difficulty_points": [1, 2, 3, 4], "streak_starts_at": 3,
                        "streak_bonus": 1, "cooperative_target": 12 if young else 16},
            "events": ["double_card", "freeze_pose", "reverse_actor", "silent_relay",
                       "custom_family_card"],
            "safety": {"skip_without_explanation": True, "no_mocking_prompts": True,
                       "physical_contact_required": False},
        },
        "draw-guess": {
            "modes": ["classic_team", "quick_5", "all_draw", "family_coop"],
            "round": {"seconds": 120 if young else 60, "cards_per_turn": 5,
                      "pass_tokens": 3 if young else 2, "letters_allowed": False,
                      "numbers_allowed": False, "speaking_allowed": False},
            "canvas": {"colors": 8, "brush_sizes": 3, "undo_count": 5 if young else 3,
                       "clear_canvas": True, "shape_hint": young},
            "bonuses": {"difficulty_points": [1, 2, 3, 4], "streak_starts_at": 3,
                        "streak_bonus": 1, "cooperative_target": 12 if young else 16},
            "events": ["one_line", "one_color", "helper_stroke", "speed_round",
                       "all_draw_same_clue"],
            "safety": {"skip_without_explanation": True, "no_mocking_drawings": True,
                       "eyes_closed_required": False, "unsafe_grip_required": False},
        },
        "story-adventure": {
            "modes": ["solo_story", "family_chain", "quick_60", "hidden_twist"],
            "round": {"seconds": 120 if young else 60, "sentences_per_turn": 2 if young else 1,
                      "required_elements": 3 if young else 5, "cards_per_game": 5,
                      "pass_tokens": 3 if young else 2},
            "story_structure": {"steps": ["beginning", "challenge", "surprise", "solution", "ending"],
                                "previous_sentence_visible": True, "ending_choice": True},
            "bonuses": {"use_every_element": 2, "connect_previous_turn": 1,
                        "creative_ending": 1, "cooperative_target": 10 if young else 14},
            "events": ["new_character", "reverse_ending", "sound_effect",
                       "forbidden_word", "happy_ending"],
            "safety": {"skip_without_explanation": True, "no_mocking_stories": True,
                       "personal_disclosure_required": False, "frightening_twists_for_young": False},
        },
    }
    base.update(designs[game])
    return _json_bytes(base)
