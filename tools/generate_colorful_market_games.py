"""Generate deterministic Colorful Market budget puzzles with one valid basket."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from pathlib import Path

from colorful_market_language import CATALOGS, MARKETS


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "games" / "colorful-market" / "puzzles"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = ("young", "mid", "teen", "senior")
EVENTS = ("golden_coupon", "market_rush", "bonus_basket", "price_freeze", "sharing_round")
PROFILES = {
    "young": {"offers": 6, "basket": 2, "required": 1, "discount": 0, "max_price": 7},
    "mid": {"offers": 7, "basket": 3, "required": 1, "discount": 1, "max_price": 10},
    "teen": {"offers": 8, "basket": 3, "required": 2, "discount": 2, "max_price": 13},
    "senior": {"offers": 9, "basket": 4, "required": 3, "discount": 3, "max_price": 16},
}
SOURCE = "https://www.consumerfinance.gov/consumer-tools/educator-tools/youth-financial-education/teach/activities/budgeting-needs-and-wants/"


def _id(language: str, band: str, number: int) -> str:
    raw = f"colorful-market-v1:{language}:{band}:{number}".encode()
    return "mar_" + hashlib.sha256(raw).hexdigest()[:20]


def _valid_combinations(offers, basket_size, required, coupon):
    valid = []
    for combo in itertools.combinations(offers, basket_size):
        ids = {item["product_id"] for item in combo}
        categories = {item["category"] for item in combo}
        if not set(required) <= categories:
            continue
        if coupon and coupon["product_id"] not in ids:
            continue
        total = sum(item["price"] for item in combo) - (coupon["discount"] if coupon else 0)
        valid.append((tuple(sorted(ids)), total))
    return valid


def generate() -> None:
    for language in LANGUAGES:
        catalog = CATALOGS[language]
        if len(catalog) != 12 or len(MARKETS[language]) != 5:
            raise ValueError(f"{language}: incomplete local market catalog")
        for band in BANDS:
            profile = PROFILES[band]
            rows = []
            signatures = set()
            for number in range(200):
                for attempt in range(2000):
                    rng = random.Random(f"alika-market-v1:{language}:{band}:{number}:{attempt}")
                    selected = rng.sample(list(enumerate(catalog)), profile["offers"])
                    offers = [{"product_id": f"p{index:02d}", "name": item[0],
                               "category": item[1], "price": rng.randint(1, profile["max_price"])}
                              for index, item in selected]
                    solution = rng.sample(offers, profile["basket"])
                    categories = sorted({item["category"] for item in solution})
                    if len(categories) < profile["required"]:
                        continue
                    required = sorted(rng.sample(categories, profile["required"]))
                    coupon = None
                    if profile["discount"]:
                        coupon_item = rng.choice(solution)
                        coupon = {"product_id": coupon_item["product_id"],
                                  "discount": profile["discount"]}
                    budget = sum(item["price"] for item in solution) - profile["discount"]
                    combinations = _valid_combinations(offers, profile["basket"], required, coupon)
                    matches = [ids for ids, total in combinations if total == budget]
                    signature = tuple(sorted((item["product_id"], item["price"]) for item in offers))
                    if len(matches) == 1 and set(matches[0]) == {item["product_id"] for item in solution} \
                            and signature not in signatures and budget > 0:
                        break
                else:
                    raise ValueError(f"{language}/{band}:{number + 1}: unique basket unavailable")
                signatures.add(signature)
                rows.append({
                    "puzzle_id": _id(language, band, number + 1),
                    "offers": sorted(offers, key=lambda item: item["product_id"]),
                    "basket_size": profile["basket"], "budget": budget,
                    "required_categories": required, "coupon": coupon,
                    "solution_basket": sorted(item["product_id"] for item in solution),
                    "special_event": EVENTS[number % len(EVENTS)],
                    "market": MARKETS[language][number // 40],
                    "difficulty": BANDS.index(band) + 1,
                    "source": {"title": "CFPB Budgeting for needs and wants", "url": SOURCE},
                    "culture_tags": [f"culture:{language}"], "review_status": "ai-draft",
                })
            output = OUT / language / f"{band}.jsonl"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True,
                                                 separators=(",", ":")) + "\n" for row in rows),
                              encoding="utf-8", newline="\n")


def main() -> int:
    argparse.ArgumentParser().parse_args()
    generate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
