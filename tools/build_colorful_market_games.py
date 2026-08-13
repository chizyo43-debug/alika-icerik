"""Build deterministic data-only AliKa Colorful Market packages."""
from __future__ import annotations

import argparse
import hashlib
import io
import itertools
import json
import re
import sys
import uuid
import zipfile
from pathlib import Path
from typing import Any


TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
from game_visuals import asset_records, visual_payloads
from gameplay_designs import gameplay_config


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = ROOT / "games" / "colorful-market"
PUZZLES = GAME_ROOT / "puzzles"
CATALOG = GAME_ROOT / "catalog.json"
LANGUAGES = ("tr", "en", "de", "es", "fr", "pt", "ru", "ja", "ko")
BANDS = {"young": (5, 7), "mid": (8, 11), "teen": (12, 14), "senior": (15, 18)}
PROFILE = {
    "young": {"offers": 6, "basket": 2, "required": 1, "discount": 0},
    "mid": {"offers": 7, "basket": 3, "required": 1, "discount": 1},
    "teen": {"offers": 8, "basket": 3, "required": 2, "discount": 2},
    "senior": {"offers": 9, "basket": 4, "required": 3, "discount": 3},
}
EVENTS = {"golden_coupon", "market_rush", "bonus_basket", "price_freeze", "sharing_round"}
CATEGORIES = {"food", "school", "daily", "nature", "play"}
PER_POOL = 200
NAMES = {
    "tr": "Renkli Pazar", "en": "Colorful Market", "de": "Bunter Markt",
    "es": "Mercado de colores", "fr": "Marché coloré", "pt": "Mercado colorido",
    "ru": "Красочный рынок", "ja": "カラフル市場", "ko": "알록달록 시장",
}
SUBJECTS = {
    "tr": "Bütçe ve planlama", "en": "Budgeting and planning",
    "de": "Budget und Planung", "es": "Presupuesto y planificación",
    "fr": "Budget et planification", "pt": "Orçamento e planejamento",
    "ru": "Бюджет и планирование", "ja": "予算と計画", "ko": "예산과 계획",
}
RUNTIME_FIELDS = ("puzzle_id", "offers", "basket_size", "budget", "required_categories",
                  "coupon", "solution_basket", "special_event", "market", "difficulty")
CREATED_AT = "2026-08-14T00:00:00Z"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{2,80}$")
PRODUCT_RE = re.compile(r"^p\d{2}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class ColorfulMarketBuildError(ValueError):
    pass


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def _solutions(row: dict[str, Any], profile: dict[str, int]) -> list[tuple[str, ...]] | None:
    offers = row.get("offers")
    required = row.get("required_categories")
    coupon = row.get("coupon")
    budget = row.get("budget")
    if (not isinstance(offers, list) or len(offers) != profile["offers"]
            or not isinstance(required, list) or len(required) != profile["required"]
            or len(set(required)) != len(required) or not set(required) <= CATEGORIES
            or not isinstance(budget, int) or budget <= 0):
        return None
    ids = set()
    for item in offers:
        if (not isinstance(item, dict) or set(item) != {"product_id", "name", "category", "price"}
                or not isinstance(item.get("product_id"), str)
                or not PRODUCT_RE.fullmatch(item["product_id"]) or item["product_id"] in ids
                or not isinstance(item.get("name"), str) or not item["name"].strip()
                or item.get("category") not in CATEGORIES
                or not isinstance(item.get("price"), int) or not 1 <= item["price"] <= 20):
            return None
        ids.add(item["product_id"])
    if profile["discount"] == 0:
        if coupon is not None:
            return None
    elif (not isinstance(coupon, dict) or set(coupon) != {"product_id", "discount"}
          or coupon.get("product_id") not in ids or coupon.get("discount") != profile["discount"]):
        return None
    matches = []
    for combo in itertools.combinations(offers, profile["basket"]):
        combo_ids = {item["product_id"] for item in combo}
        if not set(required) <= {item["category"] for item in combo}:
            continue
        if coupon and coupon["product_id"] not in combo_ids:
            continue
        total = sum(item["price"] for item in combo) - (coupon["discount"] if coupon else 0)
        if total == budget:
            matches.append(tuple(sorted(combo_ids)))
    return matches


def _puzzle_valid(row: dict[str, Any], profile: dict[str, int]) -> bool:
    matches = _solutions(row, profile)
    solution = row.get("solution_basket")
    return (matches is not None and len(matches) == 1
            and isinstance(solution, list) and len(solution) == profile["basket"]
            and len(set(solution)) == len(solution) and tuple(sorted(solution)) == matches[0]
            and row.get("basket_size") == profile["basket"])


def _load_pool(language: str, band: str) -> list[dict[str, Any]]:
    path = PUZZLES / language / f"{band}.jsonl"
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ColorfulMarketBuildError(f"invalid source pool: {path.relative_to(ROOT)}") from exc
    if len(rows) != PER_POOL:
        raise ColorfulMarketBuildError(f"{language}/{band}: expected {PER_POOL} puzzles, got {len(rows)}")
    ids = set()
    signatures = set()
    profile = PROFILE[band]
    expected_difficulty = tuple(BANDS).index(band) + 1
    cultural = 0
    for index, row in enumerate(rows, 1):
        puzzle_id = row.get("puzzle_id")
        offers = row.get("offers")
        signature = tuple(sorted((item.get("product_id"), item.get("price")) for item in offers)) \
            if isinstance(offers, list) and all(isinstance(item, dict) for item in offers) else ()
        source, tags = row.get("source"), row.get("culture_tags")
        if (not isinstance(puzzle_id, str) or not ID_RE.fullmatch(puzzle_id) or puzzle_id in ids
                or signature in signatures or not _puzzle_valid(row, profile)
                or row.get("special_event") not in EVENTS
                or not isinstance(row.get("market"), str) or not row["market"].strip()
                or row.get("difficulty") != expected_difficulty
                or not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://")
                or not isinstance(tags, list) or row.get("review_status") != "ai-draft"):
            raise ColorfulMarketBuildError(f"{language}/{band}:{index}: invalid market puzzle")
        cultural += any(str(tag).startswith(f"culture:{language}") for tag in tags)
        ids.add(puzzle_id)
        signatures.add(signature)
    if cultural != PER_POOL or {row["special_event"] for row in rows} != EVENTS:
        raise ColorfulMarketBuildError(f"{language}/{band}: cultural or event coverage is incomplete")
    if len({row["market"] for row in rows}) != 5:
        raise ColorfulMarketBuildError(f"{language}/{band}: expected five local markets")
    return rows


def _package(language: str, band: str, rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    age_min, age_max = BANDS[band]
    puzzles = _json_bytes([{field: row[field] for field in RUNTIME_FIELDS} for row in rows])
    extras = visual_payloads("colorful-market", band)
    extras["data/gameplay.json"] = gameplay_config("colorful-market", band)
    manifest = {
        "schema_version": 1,
        "game_id": str(uuid.uuid5(uuid.NAMESPACE_URL,
                                  f"https://alika.tr/games/colorful-market/v1/{language}/{band}")),
        "game_version": 1, "name": f"{NAMES[language]} · {age_min}–{age_max}",
        "description": f"{language.upper()} · {age_min}–{age_max} · {PER_POOL} bütçe görevi",
        "game_type": "budget_market", "min_app_version": "1.1.24",
        "min_players": 1, "max_players": 8, "age_min": age_min, "age_max": age_max,
        "subject": SUBJECTS[language], "topic": f"{age_min}–{age_max}", "language": language,
        "license": "CC-BY-NC-4.0", "author": "AliKa Atölye",
        "assets": ([{"path": "data/puzzles.json", "sha256": hashlib.sha256(puzzles).hexdigest(),
                     "asset_type": "puzzles", "size_bytes": len(puzzles)}] + asset_records(extras)),
        "total_size_bytes": len(puzzles) + sum(map(len, extras.values())), "created_at": CREATED_AT,
    }
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_STORED) as archive:
        for name, payload in (("manifest.json", _json_bytes(manifest)),
                              ("data/puzzles.json", puzzles), *extras.items()):
            info = zipfile.ZipInfo(name, ZIP_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, payload, compress_type=zipfile.ZIP_STORED)
    return output.getvalue(), manifest


def build(*, check: bool) -> None:
    outputs: dict[Path, bytes] = {}
    entries = []
    for language in LANGUAGES:
        for band in BANDS:
            rows = _load_pool(language, band)
            payload, manifest = _package(language, band, rows)
            relative = Path("games") / "colorful-market" / "dist" / language / f"{band}.alika-game"
            outputs[ROOT / relative] = payload
            entries.append({"path": relative.as_posix(), "sha256": hashlib.sha256(payload).hexdigest(),
                            "size_bytes": len(payload), "puzzle_count": len(rows),
                            "game_id": manifest["game_id"], "game_version": 1,
                            "language": language, "age_min": manifest["age_min"],
                            "age_max": manifest["age_max"], "name": manifest["name"]})
    outputs[CATALOG] = _json_bytes({"schema_version": 1, "generated_at": CREATED_AT,
                                    "review_status": "ai-draft", "human_approved": False,
                                    "games": entries})
    if check:
        stale = [path.relative_to(ROOT).as_posix() for path, data in outputs.items()
                 if not path.is_file() or (path.read_bytes().replace(b"\r\n", b"\n") != data
                                           if path.suffix == ".json" else path.read_bytes() != data)]
        if stale:
            raise ColorfulMarketBuildError("generated files are stale: " + ", ".join(stale))
        return
    for path, data in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        build(check=args.check)
    except ColorfulMarketBuildError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
