"""Generate localized two-truths-and-a-lie cards from frozen Wikidata facts."""
from __future__ import annotations

import json
import random
from pathlib import Path

from generate_trivia_geography import FOCUS, _age_ordered, _prepare
from trivia_language import (
    CONTESTED_CAPITALS, CONTINENT_NAMES, SAME_NAME_CAPITALS, TEMPLATES,
    RU_CONTINENT_PREPOSITIONAL, country_forms,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "games" / "trivia" / "data" / "wikidata_countries.json"
OUT = ROOT / "games" / "liar" / "cards"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = ("young", "mid", "teen", "senior")
PER_POOL = 200
CATEGORIES = {
    "tr": "Dünya", "en": "World", "de": "Welt", "es": "Mundo",
    "fr": "Monde", "pt": "Mundo", "ru": "Мир", "ja": "世界", "ko": "세계",
}


def _statement(language: str, item: dict, kind: str, *, capital: str | None = None) -> str:
    forms = country_forms(language, item["iso2"], item["country"])
    continent = CONTINENT_NAMES[language][item["continents"][0]]
    context = {
        **forms,
        "capital": capital if capital is not None else item["capital"],
        "continent": continent,
        "continent_prep": RU_CONTINENT_PREPOSITIONAL.get(continent, continent),
    }
    return TEMPLATES[language][f"{kind}_explanation"].format(**context)


def _pick_distinct(eligible: list[dict], indexes: list[int]) -> list[dict]:
    picked: list[dict] = []
    used: set[str] = set()
    for raw_index in indexes:
        index = raw_index % len(eligible)
        while eligible[index]["iso2"] in used:
            index = (index + 1) % len(eligible)
        picked.append(eligible[index])
        used.add(eligible[index]["iso2"])
    return picked


def generate(snapshot: dict[str, list[dict[str, str]]]) -> None:
    prepared = _prepare(snapshot)
    for language in LANGUAGES:
        for band in BANDS:
            rng = random.Random(f"alika-liar-v1:{language}:{band}")
            ordered = _age_ordered(prepared[language], FOCUS[language], band, rng)
            eligible = [
                item for item in ordered
                if item["iso2"] not in CONTESTED_CAPITALS
                and item["iso2"] not in SAME_NAME_CAPITALS
                and item["country"].casefold() != item["capital"].casefold()
                and len(item["continents"]) == 1
            ]
            if len(eligible) < 100:
                raise ValueError(f"not enough geography facts for {language}/{band}")
            rows = []
            signatures: set[tuple[str, ...]] = set()
            for number in range(PER_POOL):
                cycle = number // len(eligible)
                a, b, c, wrong = _pick_distinct(eligible, [
                    number, number * 7 + 13 + cycle, number * 11 + 29 + cycle * 2,
                    number * 17 + 47 + cycle * 3,
                ])
                statements = [
                    _statement(language, a, "capital"),
                    _statement(language, b, "continent"),
                    _statement(language, c, "capital", capital=wrong["capital"]),
                ]
                signature = tuple(statements)
                if signature in signatures:
                    raise ValueError(f"duplicate liar card for {language}/{band}/{number + 1}")
                signatures.add(signature)
                lie_text = statements[2]
                rng.shuffle(statements)
                lie_index = statements.index(lie_text)
                correction = _statement(language, c, "capital")
                qids = {item["country_qid"] for item in (a, b, c, wrong)}
                rows.append({
                    "card_id": f"liar-{language}-{band}-{number + 1:03d}",
                    "statements": statements,
                    "lie_index": lie_index,
                    "category": CATEGORIES[language],
                    "explanation": correction,
                    "sources": [{"title": f"Wikidata {qid}",
                                 "url": f"https://www.wikidata.org/wiki/{qid}"}
                                for qid in sorted(qids)],
                    "review_status": "ai-draft",
                })
            path = OUT / language / f"{band}.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
                encoding="utf-8",
            )


if __name__ == "__main__":
    generate(json.loads(DATA_PATH.read_text(encoding="utf-8")))
