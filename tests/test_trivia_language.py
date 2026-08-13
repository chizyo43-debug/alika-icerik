from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import generate_trivia_geography as generator  # noqa: E402
from trivia_language import (  # noqa: E402
    CONTESTED_CAPITALS,
    CONTINENT_ALIASES,
    CONTINENT_NAMES,
    SAME_NAME_CAPITALS,
    country_forms,
    display_capital,
    display_name,
)


@pytest.mark.parametrize(
    ("language", "iso2", "name", "field", "expected"),
    [
        ("tr", "IR", "İran", "gen", "İran'ın"),
        ("tr", "NP", "Nepal", "gen", "Nepal'in"),
        ("tr", "TR", "Türkiye", "gen", "Türkiye'nin"),
        ("en", "NL", "Netherlands", "of", "the Netherlands"),
        ("de", "CH", "Schweiz", "of", "der Schweiz"),
        ("de", "GB", "Vereinigtes Königreich", "of", "des Vereinigten Königreichs"),
        ("fr", "NL", "Pays-Bas", "of", "des Pays-Bas"),
        ("es", "GB", "Reino Unido", "of", "del Reino Unido"),
        ("pt", "BR", "Brasil", "subj", "o Brasil"),
        ("pt", "CM", "Camarões", "of", "dos Camarões"),
        ("ru", "PG", "Папуа — Новая Гвинея", "gen", "Папуа — Новой Гвинеи"),
        ("ko", "KR", "대한민국", "topic", "은"),
        ("ko", "MM", "미얀마", "topic", "는"),
    ],
)
def test_country_forms_cover_reviewed_language_rules(language, iso2, name, field, expected):
    assert country_forms(language, iso2, name)[field] == expected


def test_reviewed_display_overrides_remove_long_and_administrative_names():
    assert display_name("tr", "NL", "Hollanda Krallığı") == "Hollanda"
    assert display_name("es", "NL", "Reino de los Países Bajos") == "Países Bajos"
    assert display_capital("ja", "CN", "北京市") == "北京"
    assert display_capital("ko", "KR", "서울특별시") == "서울"


def test_continent_aliases_use_six_canonical_values_without_eurasia():
    assert set(CONTINENT_ALIASES.values()) == set(next(iter(CONTINENT_NAMES.values())))
    assert "Avrasya" not in CONTINENT_ALIASES
    assert "Eurasia" not in CONTINENT_ALIASES
    assert "Евразия" not in CONTINENT_ALIASES


def test_geography_generator_matches_committed_pools(monkeypatch, tmp_path):
    snapshot = json.loads(generator.DATA_PATH.read_text(encoding="utf-8"))
    monkeypatch.setattr(generator, "QUESTIONS", tmp_path)
    generator.generate(snapshot)
    for language in generator.LANGUAGES:
        for band in generator.BANDS:
            expected = ROOT / "games" / "trivia" / "questions" / language / f"{band}.jsonl"
            assert (tmp_path / language / f"{band}.jsonl").read_bytes() == expected.read_bytes()


def test_generated_pools_exclude_sensitive_and_self_revealing_capitals():
    snapshot = json.loads(generator.DATA_PATH.read_text(encoding="utf-8"))
    excluded = CONTESTED_CAPITALS | SAME_NAME_CAPITALS
    for language in generator.LANGUAGES:
        qids = {
            item["iso2"]: item["country_qid"]
            for item in snapshot[language]
            if item["iso2"] in excluded
        }
        excluded_urls = {f"https://www.wikidata.org/wiki/{qid}" for qid in qids.values()}
        canonical_continents = set(CONTINENT_NAMES[language].values())
        for band in generator.BANDS:
            path = ROOT / "games" / "trivia" / "questions" / language / f"{band}.jsonl"
            rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            assert not ({row["source"]["url"] for row in rows[:160]} & excluded_urls)
            assert {
                choice for row in rows[160:] for choice in row["choices"]
            } <= canonical_continents


def test_reverse_pairs_are_local_only_and_within_documented_range():
    for language in generator.LANGUAGES:
        for band in generator.BANDS:
            path = ROOT / "games" / "trivia" / "questions" / language / f"{band}.jsonl"
            rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            capital_sources = {row["source"]["url"] for row in rows[:100]}
            inverse_rows = {
                row["source"]["url"]: row for row in rows[100:160]
                if row["source"]["url"] in capital_sources
            }
            assert 17 <= len(inverse_rows) <= 20
            assert all(
                f"culture:{language}" in row["culture_tags"]
                for row in inverse_rows.values()
            )
