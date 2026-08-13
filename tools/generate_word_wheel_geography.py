"""Generate localized country/capital word-wheel pools from frozen facts."""
from __future__ import annotations

import json
import random
from typing import Any

from build_word_wheel_games import BANDS, LANGUAGES, PUZZLES_PER_POOL, ROOT
from generate_trivia_geography import FOCUS, _age_ordered, _prepare
from trivia_language import (
    CONTESTED_CAPITALS, CONTINENT_NAMES, SAME_NAME_CAPITALS, TEMPLATES,
    country_forms,
)


DATA_PATH = ROOT / "games" / "trivia" / "data" / "wikidata_countries.json"
CATEGORIES = {
    "tr": ("Ülke", "Başkent"), "en": ("Country", "Capital"),
    "de": ("Land", "Hauptstadt"), "es": ("País", "Capital"),
    "fr": ("Pays", "Capitale"), "pt": ("País", "Capital"),
    "ru": ("Страна", "Столица"), "ja": ("国", "首都"), "ko": ("나라", "수도"),
}
CONTINENT_CLUES = {
    "tr": "Bu ülke {continent} kıtasındadır.",
    "en": "This country is in {continent}.",
    "de": "Dieses Land liegt in {continent}.",
    "es": "Este país está en {continent}.",
    "fr": "Ce pays se trouve en {continent}.",
    "pt": "Este país fica na região: {continent}.",
    "ru": "Эта страна находится на континенте {continent}.",
    "ja": "この国がある大陸は{continent}です。",
    "ko": "이 나라는 {continent}에 있습니다.",
}


def _key(value: str) -> str:
    return " ".join(value.casefold().split())


def generate(snapshot: dict[str, list[dict[str, str]]]) -> None:
    prepared = _prepare(snapshot)
    for language in LANGUAGES:
        for band in BANDS:
            rng = random.Random(f"alika-word-wheel-v1:{language}:{band}")
            ordered = _age_ordered(prepared[language], FOCUS[language], band, rng)
            eligible = [
                item for item in ordered
                if item["iso2"] not in CONTESTED_CAPITALS
                and item["iso2"] not in SAME_NAME_CAPITALS
                and item["country"].casefold() != item["capital"].casefold()
                and len(item["continents"]) == 1
            ]
            used: set[str] = set()
            specs: list[tuple[str, dict[str, Any]]] = []
            for kind in ("country", "capital"):
                for item in eligible:
                    answer = item["country"] if kind == "country" else item["capital"]
                    forms = country_forms(language, item["iso2"], item["country"])
                    continent = CONTINENT_NAMES[language][item["continents"][0]]
                    context = {**forms, "capital": item["capital"], "continent": continent}
                    clue = (CONTINENT_CLUES[language].format(**context) if kind == "country"
                            else TEMPLATES[language]["capital"].format(**context))
                    if _key(answer) in used or _key(answer) in _key(clue):
                        continue
                    specs.append((kind, item))
                    used.add(_key(answer))
                    if sum(current_kind == kind for current_kind, _ in specs) == 100:
                        break
            if len(specs) != PUZZLES_PER_POOL:
                raise ValueError(f"not enough unique word puzzles for {language}/{band}: {len(specs)}")
            rng.shuffle(specs)

            rows = []
            local = set(FOCUS[language])
            for number, (kind, item) in enumerate(specs, 1):
                forms = country_forms(language, item["iso2"], item["country"])
                continent = CONTINENT_NAMES[language][item["continents"][0]]
                context = {**forms, "capital": item["capital"], "continent": continent}
                answer = item["country"] if kind == "country" else item["capital"]
                clue = (CONTINENT_CLUES[language].format(**context) if kind == "country"
                        else TEMPLATES[language]["capital"].format(**context))
                rows.append({
                    "puzzle_id": f"wheel-{language}-{band}-{number:03d}",
                    "answer": answer,
                    "category": CATEGORIES[language][0 if kind == "country" else 1],
                    "clue": clue,
                    "explanation": TEMPLATES[language]["capital_explanation"].format(**context),
                    "source": {"title": f"Wikidata {item['country_qid']}",
                               "url": f"https://www.wikidata.org/wiki/{item['country_qid']}"},
                    "culture_tags": ([f"culture:{language}", item["iso2"]]
                                     if item["iso2"] in local else ["global"]),
                    "review_status": "ai-draft",
                })
            path = ROOT / "games" / "word-wheel" / "words" / language / f"{band}.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
                encoding="utf-8",
            )


def main() -> int:
    generate(json.loads(DATA_PATH.read_text(encoding="utf-8")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
