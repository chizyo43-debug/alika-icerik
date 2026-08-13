"""Refresh the frozen Who Is It source snapshot from Wikimedia APIs."""
from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "games" / "who-is-it" / "data" / "wikidata_people.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
PEOPLE_PAGES = ("Wikipedia:Vital articles/Level 4/People",)
USER_AGENT = "AliKaContentBuilder/1.0 (https://github.com/chizyo43-debug/alika-icerik)"


def _get(base: str, params: dict[str, str]) -> dict:
    url = base + "?" + urlencode(params)
    last: Exception | None = None
    for attempt in range(4):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=45) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            last = exc
            if attempt < 3:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Wikimedia request failed: {url}") from last


def _batches(values: list[str], size: int = 50):
    for start in range(0, len(values), size):
        yield values[start:start + size]


def _year(claims: dict, property_id: str) -> int | None:
    for claim in claims.get(property_id, []):
        value = claim.get("mainsnak", {}).get("datavalue", {}).get("value")
        if isinstance(value, dict):
            raw = value.get("time", "")
            if isinstance(raw, str) and len(raw) >= 5:
                try:
                    return int(raw[1:5]) * (-1 if raw.startswith("-") else 1)
                except ValueError:
                    continue
    return None


def _claim_ids(claims: dict, property_id: str) -> list[str]:
    values = []
    for claim in claims.get(property_id, []):
        value = claim.get("mainsnak", {}).get("datavalue", {}).get("value")
        if isinstance(value, dict) and isinstance(value.get("id"), str):
            values.append(value["id"])
    return values


def fetch() -> dict:
    wikipedia = "https://en.wikipedia.org/w/api.php"
    wikidata = "https://www.wikidata.org/w/api.php"
    titles: set[str] = set()
    for page in PEOPLE_PAGES:
        parsed = _get(wikipedia, {
            "action": "parse", "page": page, "prop": "links",
            "format": "json", "formatversion": "2",
        })
        titles.update(
            link["title"] for link in parsed.get("parse", {}).get("links", [])
            if link.get("ns") == 0 and isinstance(link.get("title"), str)
        )

    qids: set[str] = set()
    for batch in _batches(sorted(titles)):
        result = _get(wikipedia, {
            "action": "query", "prop": "pageprops", "redirects": "1",
            "titles": "|".join(batch), "format": "json", "formatversion": "2",
        })
        for page in result.get("query", {}).get("pages", []):
            qid = page.get("pageprops", {}).get("wikibase_item")
            if isinstance(qid, str):
                qids.add(qid)

    raw_people: dict[str, dict] = {}
    related_ids: set[str] = set()
    for batch in _batches(sorted(qids)):
        result = _get(wikidata, {
            "action": "wbgetentities", "ids": "|".join(batch),
            "props": "labels|descriptions|claims|sitelinks",
            "languages": "|".join(LANGUAGES), "format": "json",
        })
        for qid, entity in result.get("entities", {}).items():
            claims = entity.get("claims", {})
            occupations = _claim_ids(claims, "P106")
            citizenships = _claim_ids(claims, "P27")
            related_ids.update(occupations)
            related_ids.update(citizenships)
            raw_people[qid] = {
                "qid": qid,
                "birth_year": _year(claims, "P569"),
                "death_year": _year(claims, "P570"),
                "occupation_qids": occupations,
                "citizenship_qids": citizenships,
                "sitelink_count": len(entity.get("sitelinks", {})),
                "labels": {lang: entity.get("labels", {}).get(lang, {}).get("value", "")
                           for lang in LANGUAGES},
                "descriptions": {
                    lang: entity.get("descriptions", {}).get(lang, {}).get("value", "")
                    for lang in LANGUAGES
                },
            }

    related_labels: dict[str, dict[str, str]] = {}
    for batch in _batches(sorted(related_ids)):
        result = _get(wikidata, {
            "action": "wbgetentities", "ids": "|".join(batch), "props": "labels",
            "languages": "|".join(LANGUAGES), "format": "json",
        })
        for qid, entity in result.get("entities", {}).items():
            related_labels[qid] = {
                lang: entity.get("labels", {}).get(lang, {}).get("value", "")
                for lang in LANGUAGES
            }

    people = []
    for person in raw_people.values():
        if not person["birth_year"] or not person["death_year"]:
            continue
        occupation_qids = person.pop("occupation_qids")
        person["occupations"] = {
            lang: [related_labels[qid][lang] for qid in occupation_qids
                   if related_labels.get(qid, {}).get(lang)]
            for lang in LANGUAGES
        }
        person["citizenships"] = {
            lang: [related_labels[qid][lang] for qid in person["citizenship_qids"]
                   if related_labels.get(qid, {}).get(lang)]
            for lang in LANGUAGES
        }
        people.append(person)
    people.sort(key=lambda row: (-row["sitelink_count"], row["qid"]))
    return {
        "schema_version": 1,
        "source": "English Wikipedia Vital articles Level 4 and Wikidata",
        "source_urls": [
            "https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level_4/People",
            "https://www.wikidata.org/",
        ],
        "people": people,
    }


def main() -> int:
    snapshot = fetch()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    counts = {
        lang: sum(bool(row["labels"][lang] and row["descriptions"][lang])
                  for row in snapshot["people"])
        for lang in LANGUAGES
    }
    print(json.dumps({"people": len(snapshot["people"]), "localized": counts}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
