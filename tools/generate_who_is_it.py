"""Generate localized Who Is It pools from the frozen Wikimedia snapshot."""
from __future__ import annotations

import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "games" / "who-is-it" / "data" / "wikidata_people.json"
OUT = ROOT / "games" / "who-is-it" / "identities"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = ("young", "mid", "teen", "senior")
PER_POOL = 200
BAND_OFFSETS = {"young": 0, "mid": 150, "teen": 300, "senior": 450}
FOCUS = {
    "tr": {"Q43", "Q12560"},
    "en": {"Q30", "Q145", "Q16", "Q408"},
    "de": {"Q183", "Q40", "Q39"},
    "es": {"Q29", "Q96", "Q414"},
    "fr": {"Q142", "Q31", "Q16"},
    "pt": {"Q45", "Q155"},
    "ru": {"Q159", "Q15180"},
    "ja": {"Q17"},
    "ko": {"Q884"},
}
TEMPLATES = {
    "tr": {
        "born": "{year} yılında doğdum.", "died": "{year} yılında hayatımı kaybettim.",
        "role": "{country} ile bağlantılıyım; çalışma alanlarımdan biri {occupation}.",
        "description": "Kaynaklarda şöyle tanımlanırım: {description}.",
    },
    "en": {
        "born": "I was born in {year}.", "died": "I died in {year}.",
        "role": "I am associated with {country}; one of my fields was {occupation}.",
        "description": "I am described as {description}.",
    },
    "de": {
        "born": "Ich wurde {year} geboren.", "died": "Ich starb {year}.",
        "role": "Ich bin mit {country} verbunden; eines meiner Gebiete war {occupation}.",
        "description": "Ich werde so beschrieben: {description}.",
    },
    "es": {
        "born": "Nací en {year}.", "died": "Fallecí en {year}.",
        "role": "Tengo relación con {country}; uno de mis campos fue {occupation}.",
        "description": "Se me describe así: {description}.",
    },
    "fr": {
        "born": "Je suis né(e) en {year}.", "died": "Je suis décédé(e) en {year}.",
        "role": "Je suis lié(e) à {country} ; l’un de mes domaines était {occupation}.",
        "description": "Je suis décrit(e) ainsi : {description}.",
    },
    "pt": {
        "born": "Nasci em {year}.", "died": "Faleci em {year}.",
        "role": "Tenho ligação com {country}; uma das minhas áreas foi {occupation}.",
        "description": "Sou descrito(a) assim: {description}.",
    },
    "ru": {
        "born": "Я родился или родилась в {year} году.", "died": "Я умер или умерла в {year} году.",
        "role": "Я связан или связана с {country}; одна из моих сфер — {occupation}.",
        "description": "В источниках меня описывают так: {description}.",
    },
    "ja": {
        "born": "{year}年に生まれました。", "died": "{year}年に亡くなりました。",
        "role": "{country}にゆかりがあり、分野の一つは{occupation}です。",
        "description": "資料では次のように紹介されています：{description}。",
    },
    "ko": {
        "born": "{year}년에 태어났습니다.", "died": "{year}년에 세상을 떠났습니다.",
        "role": "{country}와 관련이 있으며 활동 분야 중 하나는 {occupation}입니다.",
        "description": "자료에는 다음과 같이 소개됩니다: {description}.",
    },
}
YOUNG_BLOCKED = (
    "serial killer", "pornographic", "criminal", "dictator", "nazi", "terrorist",
    "murderer", "adult film", "war criminal",
)


def _key(value: str) -> str:
    return " ".join(value.casefold().split())


def _eligible(person: dict, language: str, band: str) -> bool:
    answer = person["labels"].get(language, "").strip()
    description = person["descriptions"].get(language, "").strip()
    occupations = person["occupations"].get(language, [])
    citizenships = person["citizenships"].get(language, [])
    if not answer or not description or not occupations or not citizenships:
        return False
    if len(answer) > 100 or len(description) > 220 or _key(answer) in _key(description):
        return False
    if band == "young" and any(word in person["descriptions"].get("en", "").casefold()
                                for word in YOUNG_BLOCKED):
        return False
    return True


def _select(people: list[dict], language: str, band: str) -> list[dict]:
    eligible = [person for person in people if _eligible(person, language, band)]
    eligible.sort(key=lambda row: (-row["sitelink_count"], row["qid"]))
    offset = BAND_OFFSETS[band]
    rotated = eligible[offset:] + eligible[:offset]
    local = [row for row in rotated if FOCUS[language].intersection(row["citizenship_qids"])]
    selected = local[:30]
    selected_qids = {row["qid"] for row in selected}
    selected.extend(row for row in rotated if row["qid"] not in selected_qids)
    selected = selected[:PER_POOL]
    if len(selected) != PER_POOL:
        raise ValueError(f"not enough localized people for {language}/{band}: {len(selected)}")
    return selected


def generate() -> None:
    snapshot = json.loads(DATA.read_text(encoding="utf-8"))
    people = snapshot["people"]
    for language in LANGUAGES:
        for band in BANDS:
            selected = _select(people, language, band)
            rng = random.Random(f"alika-who-is-it-v1:{language}:{band}")
            rng.shuffle(selected)
            rows = []
            for number, person in enumerate(selected, 1):
                answer = person["labels"][language].strip()
                occupation = person["occupations"][language][0].strip()
                country = person["citizenships"][language][0].strip()
                description = person["descriptions"][language].strip().rstrip(".。")
                template = TEMPLATES[language]
                clues = [
                    template["died"].format(year=person["death_year"]),
                    template["born"].format(year=person["birth_year"]),
                    template["role"].format(country=country, occupation=occupation),
                    template["description"].format(description=description),
                ]
                if any(_key(answer) in _key(clue) for clue in clues):
                    raise ValueError(f"answer leaked in clue: {language}/{band}/{person['qid']}")
                rows.append({
                    "identity_id": f"who-{language}-{band}-{number:03d}",
                    "answer": answer,
                    "category": occupation,
                    "clues": clues,
                    "explanation": f"{answer}: {description}.",
                    "source": {
                        "title": f"Wikidata {person['qid']}",
                        "url": f"https://www.wikidata.org/wiki/{person['qid']}",
                    },
                    "culture_tags": ([f"culture:{language}"]
                                     if FOCUS[language].intersection(person["citizenship_qids"])
                                     else ["global"]),
                    "review_status": "ai-draft",
                })
            path = OUT / language / f"{band}.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
                encoding="utf-8",
            )


if __name__ == "__main__":
    generate()
