"""Freeze multilingual Wikidata geography facts and generate 36 review pools.

This is an authoring tool, not a CI/network dependency. Generated JSONL and the
normalized fact snapshot are committed; normal package builds are offline.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from build_trivia_games import BANDS, LANGUAGES, QUESTIONS, ROOT, SUBJECTS
from trivia_language import (
    CONTESTED_CAPITALS,
    CONTINENT_ALIASES,
    CONTINENT_NAMES,
    RU_CONTINENT_PREPOSITIONAL,
    SAME_NAME_CAPITALS,
    TEMPLATES,
    country_forms,
    display_capital,
    display_name,
)


DATA_PATH = ROOT / "games" / "trivia" / "data" / "wikidata_countries.json"
ENDPOINT = "https://query.wikidata.org/sparql"
QUERY = """
SELECT DISTINCT ?country ?countryLabel ?iso2 ?capital ?capitalLabel ?continent ?continentLabel WHERE {
  ?country wdt:P31 wd:Q3624078;
           wdt:P297 ?iso2;
           wdt:P36 ?capital;
           wdt:P30 ?continent.
  FILTER NOT EXISTS { ?country wdt:P576 ?dissolved. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language \"%s,en\". }
}
ORDER BY ?iso2 ?capitalLabel ?continentLabel
"""

FOCUS = {
    "tr": "TR AZ KZ KG UZ TM CY GR BG GE AM IR IQ SY RO BA AL MK RS XK".split(),
    "en": "GB US CA AU NZ IE ZA IN SG JM TT BS BB BZ GY NG GH KE UG PK".split(),
    "de": "DE AT CH LI LU BE NL DK PL CZ SK HU SI HR IT FR SE NO RO EE".split(),
    "es": "ES MX AR CO PE CL VE EC BO PY UY GT HN SV NI CR PA CU DO GQ".split(),
    "fr": "FR BE CH CA LU MC SN CI ML NE BF BJ TG GA CM CD CG MG HT DJ".split(),
    "pt": "PT BR AO MZ CV GW ST TL GQ ES UY AR ZA NA BW ZM ZW MW MG IN".split(),
    "ru": "RU BY KZ KG AM AZ GE UZ TJ TM MD LV LT EE MN RS BG SK FI CZ".split(),
    "ja": "JP KR CN MN TW PH VN TH MY SG ID BN KH LA MM IN NP BT LK AU".split(),
    "ko": "KR JP CN MN TW PH VN TH MY SG ID BN KH LA MM IN NP BT LK AU".split(),
}

# 5–7 bandında çok küçük/az bilinen devletler yerine çocuğun harita,
# spor, masal, yemek ve gündelik haber bağlamında karşılaşma olasılığı
# yüksek ülkeler öncelenir. Diğer bantlar daha geniş küresel havuzu kullanır.
MAJOR = """
TR US GB CA MX BR AR CL CO PE FR DE ES IT PT NL BE CH AT SE NO DK FI PL CZ
GR RO BG UA RU IE IS AU NZ JP KR CN IN ID PH VN TH MY SG PK BD IR IQ SA AE
IL EG MA DZ TN ZA NG KE ET GH TZ CD SD SN CI CM AO MZ MG KZ UZ AZ GE AM
MN NP LK AF JO LB SY QA KW OM YE CU DO JM CR PA GT BO PY UY VE EC
""".split()

TOPICS = {
    "tr": "Dünya ve kültür", "en": "World and culture", "de": "Welt und Kultur",
    "es": "Mundo y cultura", "fr": "Monde et culture", "pt": "Mundo e cultura",
    "ru": "Мир и культура", "ja": "世界と文化", "ko": "세계와 문화",
}


def _qid(uri: str) -> str:
    return uri.rsplit("/", 1)[-1]


def fetch() -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for language in LANGUAGES:
        params = urllib.parse.urlencode({"query": QUERY % language, "format": "json"}).encode()
        request = urllib.request.Request(
            ENDPOINT,
            data=params,
            headers={
                "Accept": "application/sparql-results+json",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "AliKaContentAuthoring/1.0 (https://github.com/chizyo43-debug/alika-icerik)",
            },
        )
        payload = None
        for attempt in range(4):
            try:
                with urllib.request.urlopen(request, timeout=90) as response:
                    payload = json.load(response)
                break
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
                if attempt == 3:
                    raise
                time.sleep(2 ** attempt)
        assert payload is not None
        grouped: dict[str, dict[str, Any]] = {}
        for binding in payload["results"]["bindings"]:
            iso = binding["iso2"]["value"].upper()
            country = binding["countryLabel"]["value"]
            capital = binding["capitalLabel"]["value"]
            continent = binding["continentLabel"]["value"]
            if any(re.fullmatch(r"Q\d+", value) for value in (country, capital, continent)):
                continue
            group = grouped.setdefault(iso, {
                "iso2": iso,
                "country_qid": _qid(binding["country"]["value"]),
                "country": country,
                "capitals": set(),
                "continents": set(),
            })
            group["capitals"].add(capital)
            group["continents"].add(continent)
        normalized = []
        for group in grouped.values():
            if len(group["capitals"]) != 1:
                continue
            normalized.append({
                "iso2": group["iso2"],
                "country_qid": group["country_qid"],
                "country": group["country"],
                "capital": next(iter(group["capitals"])),
                "continents": sorted(group["continents"]),
            })
        result[language] = sorted(normalized, key=lambda item: item["iso2"])
        time.sleep(0.5)
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def _options(correct: str, candidates: list[str], rng: random.Random, position: int) -> tuple[list[str], int]:
    pool = sorted({value for value in candidates if value and value != correct})
    wrong = rng.sample(pool, 3)
    choices = wrong[:]
    choices.insert(position, correct)
    return choices, position


def _ordered(items: list[dict[str, str]], focus: list[str], rng: random.Random) -> list[dict[str, str]]:
    by_iso = {item["iso2"]: item for item in items}
    local = [by_iso[iso] for iso in focus if iso in by_iso]
    rest = [item for item in items if item["iso2"] not in set(focus)]
    rng.shuffle(local)
    rng.shuffle(rest)
    return local + rest


def _age_ordered(
        items: list[dict[str, str]], focus: list[str], band: str,
        rng: random.Random) -> list[dict[str, str]]:
    if band != "young":
        return _ordered(items, focus, rng)
    by_iso = {item["iso2"]: item for item in items}
    preferred_codes = list(dict.fromkeys(focus + MAJOR))
    preferred = [by_iso[iso] for iso in preferred_codes if iso in by_iso]
    rest = [item for item in items if item["iso2"] not in set(preferred_codes)]
    # Kültürel ilk blok sabit kalır; küresel tanıdık blok ve kuyruk
    # deterministik olarak karışır, böylece diller aynı havuza dönüşmez.
    local_count = sum(iso in by_iso for iso in focus)
    local, global_preferred = preferred[:local_count], preferred[local_count:]
    rng.shuffle(local)
    rng.shuffle(global_preferred)
    rng.shuffle(rest)
    return local + global_preferred + rest


def _prepare(snapshot: dict[str, list[dict[str, str]]]) -> dict[str, list[dict[str, Any]]]:
    """Ham etiketi görünen ada indirger, kıtaları altı kanona eşler.

    Anık görüntü dokunulmadan kalır: sürüm izlenebilirliği kaynakta,
    okunabilirlik burada. Kıta eşlemesi olmayan etiket (Avrasya) düşer.
    """
    prepared: dict[str, list[dict[str, Any]]] = {}
    for language in LANGUAGES:
        rows = []
        for item in snapshot[language]:
            iso = item["iso2"]
            rows.append({
                "iso2": iso,
                "country_qid": item["country_qid"],
                "country": display_name(language, iso, item["country"]),
                "capital": display_capital(language, iso, item["capital"]),
                "continents": sorted({CONTINENT_ALIASES[label]
                                      for label in item["continents"]
                                      if label in CONTINENT_ALIASES}),
            })
        prepared[language] = rows
    return prepared


def _specs(ordered: list[dict[str, Any]], focus: list[str]) -> list[tuple[str, dict[str, Any]]]:
    """Havuzun 100 başkent + 60 ülke + 40 kıta sorusunu seçer.

    Başkent ve ülke yönü aynı ülkeyi paylaşırsa bir soru diğerinin cevabını
    verir. Paylaşım yalnız kültür-yerel ülkelerde bırakılır: paket başına en
    az 40 yerel soru kapısı (bkz. `build_trivia_games._load_pool`) yalnız 20
    yerel ülkeden besleniyor, çift yön olmadan kota dolmuyor. Küresel
    ülkelerin tamamı tek yönde sorulur; çift soru 60'tan 20'ye iner.

    Adı başkentiyle aynı veya doğrudan şehir türevi olan devletler (Monako,
    Lüksemburg, Cibuti, Vatikan) iki yönde de cevabı ele verir; kıta sorusuna
    ve çeldirici havuzuna girerler, başkent/ülke sorusuna girmezler.
    """
    local = set(focus)
    ready = [item for item in ordered
             if item["iso2"] not in CONTESTED_CAPITALS
             and item["iso2"] not in SAME_NAME_CAPITALS
             and item["country"] != item["capital"]]
    capitals = ready[:100]
    asked = {item["iso2"] for item in capitals}
    countries = ([item for item in capitals if item["iso2"] in local]
                 + [item for item in ready if item["iso2"] not in asked])[:60]
    continents = [item for item in ordered if len(item["continents"]) == 1][:40]
    if len(capitals) < 100 or len(countries) < 60 or len(continents) < 40:
        raise ValueError("not enough country facts for a 200-question pool")
    return ([("capital", item) for item in capitals]
            + [("country", item) for item in countries]
            + [("continent", item) for item in continents])


def generate(snapshot: dict[str, list[dict[str, str]]]) -> None:
    prepared = _prepare(snapshot)
    for language in LANGUAGES:
        base = prepared[language]
        if len(base) < 160:
            raise ValueError(f"not enough country facts for {language}: {len(base)}")
        continent_names = CONTINENT_NAMES[language]
        template = TEMPLATES[language]
        for band in BANDS:
            rng = random.Random(f"alika-trivia-v1:{language}:{band}")
            ordered = _age_ordered(base, FOCUS[language], band, rng)
            # Older bands receive closer distractors from the same continent.
            hard = band in {"teen", "senior"}
            rows: list[dict[str, Any]] = []
            culture_set = set(FOCUS[language])
            for number, (kind, item) in enumerate(_specs(ordered, FOCUS[language]), 1):
                key = item["continents"][0] if item["continents"] else None
                continent = continent_names[key] if key else ""
                same_continent = [other for other in base if key in other["continents"]]
                candidates = same_continent if hard and len(same_continent) >= 4 else base
                if kind == "capital":
                    answer = item["capital"]
                    values = [other["capital"] for other in candidates
                              if other["iso2"] not in CONTESTED_CAPITALS]
                elif kind == "country":
                    answer = item["country"]
                    values = [other["country"] for other in candidates]
                else:
                    answer = continent
                    values = list(continent_names.values())
                choices, correct = _options(answer, values, rng, (number - 1) % 4)
                context = {
                    **country_forms(language, item["iso2"], item["country"]),
                    "capital": item["capital"],
                    "continent": continent,
                    "continent_prep": RU_CONTINENT_PREPOSITIONAL.get(continent, continent),
                }
                row = {
                    "question_id": f"gk-{language}-{band}-{number:03d}",
                    "question": template[kind].format(**context),
                    "choices": choices,
                    "correct": correct,
                    "subject": SUBJECTS[language],
                    "topic": TOPICS[language],
                    "explanation": template[f"{kind}_explanation"].format(**context),
                    "source": {
                        "title": f"Wikidata {item['country_qid']}",
                        "url": f"https://www.wikidata.org/wiki/{item['country_qid']}",
                    },
                    "culture_tags": ([f"culture:{language}", item["iso2"]]
                                     if item["iso2"] in culture_set else ["global"]),
                    "review_status": "ai-draft",
                }
                rows.append(row)
            path = QUESTIONS / language / f"{band}.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
                encoding="utf-8",
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    snapshot = fetch() if args.refresh or not DATA_PATH.is_file() else json.loads(
        DATA_PATH.read_text(encoding="utf-8")
    )
    generate(snapshot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
