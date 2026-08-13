"""Generate reviewable country-capital memory pools from the frozen snapshot.

The generator is offline: it reuses the same committed Wikidata snapshot and
language rules as the trivia catalogue. Runtime packages are built separately
and contain none of the review metadata in these JSONL files.
"""
from __future__ import annotations

import json
import random
from typing import Any

from build_memory_games import BANDS, LANGUAGES, PAIRS, ROOT
from generate_trivia_geography import FOCUS, _age_ordered, _prepare
from trivia_language import (
    CONTESTED_CAPITALS,
    SAME_NAME_CAPITALS,
    TEMPLATES,
    country_forms,
)


DATA_PATH = ROOT / "games" / "trivia" / "data" / "wikidata_countries.json"
CATEGORIES = {
    "tr": "Ülke ve başkent", "en": "Country and capital",
    "de": "Land und Hauptstadt", "es": "País y capital",
    "fr": "Pays et capitale", "pt": "País e capital",
    "ru": "Страна и столица", "ja": "国と首都", "ko": "나라와 수도",
}


def generate(snapshot: dict[str, list[dict[str, str]]]) -> None:
    prepared = _prepare(snapshot)
    for language in LANGUAGES:
        base = prepared[language]
        for band in BANDS:
            rng = random.Random(f"alika-memory-v1:{language}:{band}")
            ordered = _age_ordered(base, FOCUS[language], band, rng)
            eligible = [
                item for item in ordered
                if item["iso2"] not in CONTESTED_CAPITALS
                and item["iso2"] not in SAME_NAME_CAPITALS
                and item["country"].casefold() != item["capital"].casefold()
            ]
            selected = eligible[:PAIRS]
            if len(selected) != PAIRS:
                raise ValueError(f"not enough memory pairs for {language}/{band}")

            culture = set(FOCUS[language])
            rows: list[dict[str, Any]] = []
            for number, item in enumerate(selected, 1):
                context = {
                    **country_forms(language, item["iso2"], item["country"]),
                    "capital": item["capital"],
                }
                rows.append({
                    "pair_id": f"mem-{language}-{band}-{number:03d}",
                    "left": item["country"],
                    "right": item["capital"],
                    "category": CATEGORIES[language],
                    "explanation": TEMPLATES[language]["capital_explanation"].format(**context),
                    "source": {
                        "title": f"Wikidata {item['country_qid']}",
                        "url": f"https://www.wikidata.org/wiki/{item['country_qid']}",
                    },
                    "culture_tags": (
                        [f"culture:{language}", item["iso2"]]
                        if item["iso2"] in culture else ["global"]
                    ),
                    "review_status": "ai-draft",
                })

            path = ROOT / "games" / "memory" / "pairs" / language / f"{band}.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
                encoding="utf-8",
            )


def main() -> int:
    snapshot = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    generate(snapshot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
