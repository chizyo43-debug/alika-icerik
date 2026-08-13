"""Generate localized geography Taboo cards from frozen Wikidata facts."""
from __future__ import annotations

import json
import random

from generate_trivia_geography import FOCUS, _age_ordered, _prepare
from trivia_language import (
    CONTESTED_CAPITALS, CONTINENT_NAMES, SAME_NAME_CAPITALS, TEMPLATES,
    country_forms,
)


from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "games" / "trivia" / "data" / "wikidata_countries.json"
OUT = ROOT / "games" / "taboo" / "cards"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = ("young", "mid", "teen", "senior")
PER_POOL = 200
CATEGORIES = {
    "tr": ("Ülke", "Başkent"), "en": ("Country", "Capital"),
    "de": ("Land", "Hauptstadt"), "es": ("País", "Capital"),
    "fr": ("Pays", "Capitale"), "pt": ("País", "Capital"),
    "ru": ("Страна", "Столица"), "ja": ("国", "首都"), "ko": ("나라", "수도"),
}
GENERIC = {
    "tr": {"flag": "bayrak", "map": "harita", "city": "şehir", "government": "yönetim"},
    "en": {"flag": "flag", "map": "map", "city": "city", "government": "government"},
    "de": {"flag": "Flagge", "map": "Karte", "city": "Stadt", "government": "Regierung"},
    "es": {"flag": "bandera", "map": "mapa", "city": "ciudad", "government": "gobierno"},
    "fr": {"flag": "drapeau", "map": "carte", "city": "ville", "government": "gouvernement"},
    "pt": {"flag": "bandeira", "map": "mapa", "city": "cidade", "government": "governo"},
    "ru": {"flag": "флаг", "map": "карта", "city": "город", "government": "правительство"},
    "ja": {"flag": "国旗", "map": "地図", "city": "都市", "government": "政府"},
    "ko": {"flag": "국기", "map": "지도", "city": "도시", "government": "정부"},
}


def _key(value: str) -> str:
    return " ".join(value.casefold().split())


def generate(snapshot: dict[str, list[dict[str, str]]]) -> None:
    prepared = _prepare(snapshot)
    for language in LANGUAGES:
        for band in BANDS:
            rng = random.Random(f"alika-taboo-v1:{language}:{band}")
            ordered = _age_ordered(prepared[language], FOCUS[language], band, rng)
            eligible = [
                item for item in ordered
                if item["iso2"] not in CONTESTED_CAPITALS
                and item["iso2"] not in SAME_NAME_CAPITALS
                and item["country"].casefold() != item["capital"].casefold()
                and len(item["continents"]) == 1
            ]
            specs: list[tuple[str, dict]] = []
            used: set[str] = set()
            for kind in ("country", "capital"):
                for item in eligible:
                    target = item[kind]
                    if _key(target) in used:
                        continue
                    specs.append((kind, item))
                    used.add(_key(target))
                    if sum(current == kind for current, _ in specs) == 100:
                        break
            if len(specs) != PER_POOL:
                raise ValueError(f"not enough unique Taboo cards for {language}/{band}: {len(specs)}")
            rng.shuffle(specs)
            rows = []
            local = set(FOCUS[language])
            for number, (kind, item) in enumerate(specs, 1):
                continent = CONTINENT_NAMES[language][item["continents"][0]]
                generic = GENERIC[language]
                if kind == "country":
                    target = item["country"]
                    forbidden = [item["capital"], continent, generic["flag"], generic["map"]]
                    category = CATEGORIES[language][0]
                else:
                    target = item["capital"]
                    forbidden = [item["country"], continent, generic["city"], generic["government"]]
                    category = CATEGORIES[language][1]
                if len({_key(value) for value in forbidden}) != 4 or _key(target) in {
                    _key(value) for value in forbidden
                }:
                    raise ValueError(f"invalid forbidden terms for {language}/{band}/{item['iso2']}")
                forms = country_forms(language, item["iso2"], item["country"])
                explanation = TEMPLATES[language]["capital_explanation"].format(
                    **forms, capital=item["capital"], continent=continent,
                )
                rows.append({
                    "card_id": f"taboo-{language}-{band}-{number:03d}",
                    "target": target, "forbidden": forbidden, "category": category,
                    "explanation": explanation,
                    "source": {"title": f"Wikidata {item['country_qid']}",
                               "url": f"https://www.wikidata.org/wiki/{item['country_qid']}"},
                    "culture_tags": ([f"culture:{language}", item["iso2"]]
                                     if item["iso2"] in local else ["global"]),
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
