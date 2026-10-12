#!/usr/bin/env python3
"""Derive the LGS 2027 prediction plan from the 2024–2026 question inventory.

The inventory (`authoring/lgs-2027/lgs-2024-2026-soru-envanteri.json`) is the
hand-curated source of truth: one record per exam question with its unit,
kazanım code and evidence level. This tool turns it into a deterministic plan
(`authoring/lgs-2027/lgs-2027-tahmin-plani.json`):

* unit shares per subject, weighted towards recent exams,
* the expected question count per unit on a 2027 exam form,
* bank quotas per subject, unit and kazanım (and per math task id),
* the curated item-type, difficulty and style profile of each subject.

`--check` fails when the committed plan is out of date. `--tables` and
`--appendix` print the unit and per-question tables used in
`reports/LGS_2024_2026_SORU_ANALIZI.md`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "authoring" / "lgs-2027" / "lgs-2024-2026-soru-envanteri.json"
PLAN = ROOT / "authoring" / "lgs-2027" / "lgs-2027-tahmin-plani.json"
REGISTRY = ROOT / "curriculum" / "tr-grade8-current-2018-2019.json"

PLAN_SCHEMA = "alika-lgs-plan/1.0.0"
INVENTORY_SCHEMA = "alika-lgs-inventory/1.0.0"
YEARS = ("2024", "2025", "2026")
CONFIDENCE = ("high", "medium", "low", "unknown")
TESTABILITY_FACTOR = {"core": 1.0, "partial": 0.3, "none": 0.0}


class PlanError(Exception):
    pass


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def largest_remainder(weights: dict[str, float], total: int) -> dict[str, int]:
    """Split `total` into integers proportional to `weights`.

    Ties are broken by key order so the result is deterministic.
    """
    positive = {key: value for key, value in weights.items() if value > 0}
    result = {key: 0 for key in weights}
    if total <= 0 or not positive:
        return result
    scale = total / sum(positive.values())
    exact = {key: value * scale for key, value in positive.items()}
    for key, value in exact.items():
        result[key] = int(value)
    remaining = total - sum(result.values())
    order = sorted(exact, key=lambda key: (-(exact[key] - int(exact[key])), list(weights).index(key)))
    for key in order[:remaining]:
        result[key] += 1
    return result


def registry_codes(registry: dict[str, Any]) -> dict[str, dict[str, str]]:
    return {
        subject["subject"]: {item["code"]: item["title"] for item in subject["objectives"]}
        for subject in registry["subjects"]
    }


def unit_kazanimlar(unit: dict[str, Any], codes: dict[str, str]) -> list[str]:
    """Kazanım codes of a unit: an explicit list or every code under its prefixes."""
    if unit.get("kazanimlar"):
        return list(unit["kazanimlar"])
    prefixes = tuple(prefix.rstrip(".") + "." for prefix in unit.get("codePrefixes", []))
    return [code for code in codes if code.startswith(prefixes)]


def validate(inventory: dict[str, Any], codes_by_subject: dict[str, dict[str, str]]) -> None:
    if inventory.get("schemaVersion") != INVENTORY_SCHEMA:
        raise PlanError(f"inventory schemaVersion must be {INVENTORY_SCHEMA}")
    subjects = inventory["subjects"]
    seen: set[tuple[Any, ...]] = set()
    per_form: Counter[tuple[str, str, str]] = Counter()
    for question in inventory["questions"]:
        subject = question["subject"]
        if subject not in subjects:
            raise PlanError(f"unknown subject: {subject}")
        definition = subjects[subject]
        year = str(question["year"])
        if year not in YEARS:
            raise PlanError(f"unknown year: {year}")
        booklet = question.get("booklet")
        expected_booklet = definition.get("bookletByYear", {}).get(year, "A")
        if booklet != expected_booklet:
            raise PlanError(f"{year} {subject} q{question.get('qNo')}: booklet {booklet} != {expected_booklet}")
        number = question.get("qNo")
        if not isinstance(number, int) or not 1 <= number <= definition["questionsPerExam"]:
            raise PlanError(f"{year} {subject}: invalid qNo {number}")
        key = (year, subject, booklet, number)
        if key in seen:
            raise PlanError(f"duplicate question {key}")
        seen.add(key)
        per_form[(year, subject, booklet)] += 1
        unit_keys = {unit["key"] for unit in definition["units"]}
        if question.get("unit") is not None and question["unit"] not in unit_keys:
            raise PlanError(f"{key}: unknown unit {question['unit']}")
        codes = codes_by_subject[definition["registrySubject"]]
        for code in [question.get("kazanim"), *question.get("kazanimSecondary", [])]:
            if code is not None and code not in codes:
                raise PlanError(f"{key}: kazanım {code} is not in the registry")
        if question.get("confidence") not in CONFIDENCE:
            raise PlanError(f"{key}: invalid confidence {question.get('confidence')}")
        if question.get("answer") not in (None, "A", "B", "C", "D"):
            raise PlanError(f"{key}: invalid answer {question.get('answer')}")
    for (year, subject, booklet), count in per_form.items():
        if count != subjects[subject]["questionsPerExam"]:
            raise PlanError(f"{year} {subject} {booklet}: {count} records, expected {subjects[subject]['questionsPerExam']}")


def unit_observations(inventory: dict[str, Any], subject: str) -> tuple[dict[str, dict[str, int]], dict[str, int]]:
    counts: dict[str, dict[str, int]] = {year: Counter() for year in YEARS}
    unknown = {year: 0 for year in YEARS}
    for question in inventory["questions"]:
        if question["subject"] != subject:
            continue
        year = str(question["year"])
        if question.get("unit") is None:
            unknown[year] += 1
        else:
            counts[year][question["unit"]] += 1
    return {year: dict(value) for year, value in counts.items()}, unknown


def kazanim_observations(inventory: dict[str, Any], subject: str) -> tuple[Counter[str], Counter[str]]:
    """Primary and secondary kazanım hits of a subject across 2024–2026."""
    primary: Counter[str] = Counter()
    secondary: Counter[str] = Counter()
    for question in inventory["questions"]:
        if question["subject"] != subject:
            continue
        if question.get("kazanim"):
            primary[question["kazanim"]] += 1
        for code in question.get("kazanimSecondary", []):
            secondary[code] += 1
    return primary, secondary


def build_subject(inventory: dict[str, Any], subject: str, quota: int,
                  codes_by_subject: dict[str, dict[str, str]]) -> dict[str, Any]:
    definition = inventory["subjects"][subject]
    method = inventory["planMethod"]
    year_weights = {year: float(method["yearWeights"][year]) for year in YEARS}
    per_exam = definition["questionsPerExam"]
    codes = codes_by_subject[definition["registrySubject"]]
    counts, unknown = unit_observations(inventory, subject)
    units = definition["units"]

    shares: dict[str, float] = {}
    for unit in units:
        weighted, weight_sum = 0.0, 0.0
        for year in YEARS:
            known = sum(counts[year].values())
            if known:
                weighted += year_weights[year] * counts[year].get(unit["key"], 0) / known
                weight_sum += year_weights[year]
        shares[unit["key"]] = weighted / weight_sum if weight_sum else 0.0

    expected = {key: share * per_exam for key, share in shares.items()}
    predicted = largest_remainder(expected, per_exam)
    floor = float(method["unitFloorShare"])
    bank_weights = {
        unit["key"]: max(shares[unit["key"]], floor if unit.get("inScope", True) else 0.0)
        for unit in units
    }
    unit_quota = largest_remainder(bank_weights, quota)

    primary_hits, secondary_hits = kazanim_observations(inventory, subject)
    testability = definition.get("kazanimTestability", {})
    adjustments = {item["code"]: float(item["bonus"]) for item in definition.get("predictionAdjustments", [])}
    task_map = definition.get("taskMap", {})
    code_to_task = {code: task for task, info in task_map.items() for code in info["objectives"]}
    primary_weight = float(method["kazanimPrimaryWeight"])
    secondary_weight = float(method["kazanimSecondaryWeight"])

    unit_rows = []
    task_quota: Counter[str] = Counter()
    for unit in units:
        kazanimlar = unit_kazanimlar(unit, codes)
        weights = {}
        for code in kazanimlar:
            factor = TESTABILITY_FACTOR[testability.get(code, "core")]
            evidence = primary_weight * primary_hits.get(code, 0) + secondary_weight * secondary_hits.get(code, 0)
            weights[code] = factor * (1.0 + evidence + adjustments.get(code, 0.0))
        allocation = largest_remainder(weights, unit_quota[unit["key"]])
        rows = []
        for code in kazanimlar:
            row = {
                "code": code,
                "title": codes[code],
                "observedPrimary": primary_hits.get(code, 0),
                "observedSecondary": secondary_hits.get(code, 0),
                "testability": testability.get(code, "core"),
                "bankQuota": allocation[code],
            }
            if code in adjustments:
                row["predictionBonus"] = adjustments[code]
            if code in code_to_task:
                row["taskId"] = code_to_task[code]
                task_quota[code_to_task[code]] += allocation[code]
            rows.append(row)
        observed_years = [counts[year].get(unit["key"], 0) for year in YEARS]
        unit_rows.append({
            "key": unit["key"],
            "name": unit["name"],
            "observed": {year: counts[year].get(unit["key"], 0) for year in YEARS},
            "observedRange": [min(observed_years), max(observed_years)],
            "weightedShare": round(shares[unit["key"]], 4),
            "expectedPerExam": round(expected[unit["key"]], 2),
            "predictedPerExam": predicted[unit["key"]],
            "bankQuota": unit_quota[unit["key"]],
            "kazanimlar": rows,
        })

    profile = definition["styleProfile"]
    result: dict[str, Any] = {
        "registrySubject": definition["registrySubject"],
        "questionsPerExam": per_exam,
        "scoreWeight": definition["scoreWeight"],
        "session": definition["session"],
        "unknownUnitPerYear": unknown,
        "bankQuota": quota,
        "units": unit_rows,
        "itemTypeMix": _mix(profile["itemTypeMix"], quota),
        "difficultyMix": _mix(profile["difficultyMix"], quota),
        "targetMeanP": profile["targetMeanP"],
        "styleRules": profile["styleRules"],
        "avoid": profile["avoid"],
    }
    if task_map:
        result["taskQuotas"] = {task: task_quota.get(task, 0) for task in task_map}
    return result


def _mix(shares: dict[str, float], quota: int) -> list[dict[str, Any]]:
    total = sum(shares.values())
    if abs(total - 1.0) > 1e-6:
        raise PlanError(f"mix shares must sum to 1.0, got {total}")
    counts = largest_remainder(shares, quota)
    return [{"key": key, "share": share, "bankQuota": counts[key]} for key, share in shares.items()]


def build_plan(inventory: dict[str, Any], registry: dict[str, Any], bank_size: int | None = None) -> dict[str, Any]:
    codes_by_subject = registry_codes(registry)
    validate(inventory, codes_by_subject)
    method = inventory["planMethod"]
    size = int(bank_size or method["bankSize"])
    subjects = inventory["subjects"]
    total_per_exam = sum(definition["questionsPerExam"] for definition in subjects.values())
    quotas = largest_remainder({name: definition["questionsPerExam"] / total_per_exam for name, definition in subjects.items()}, size)
    return {
        "schemaVersion": PLAN_SCHEMA,
        "title": "LGS 2027 tahmin planı (2024–2026 soru envanterinden türetilmiştir)",
        "targetExam": "LGS 2027 merkezî sınavı",
        "curriculum": inventory["curriculum"],
        "derivedFrom": {
            "inventory": str(INVENTORY.relative_to(ROOT)),
            "inventorySha256": None,
            "registry": str(REGISTRY.relative_to(ROOT)),
        },
        "method": method,
        "bankSize": size,
        "examForm": {name: definition["questionsPerExam"] for name, definition in subjects.items()},
        "subjects": {name: build_subject(inventory, name, quotas[name], codes_by_subject) for name in subjects},
    }


def render(plan: dict[str, Any], inventory_path: Path) -> str:
    plan = dict(plan)
    plan["derivedFrom"] = dict(plan["derivedFrom"], inventorySha256=_sha256(inventory_path))
    return json.dumps(plan, ensure_ascii=False, indent=2) + "\n"


def tables(plan: dict[str, Any]) -> str:
    lines = []
    for name, subject in plan["subjects"].items():
        lines.append(f"### {name}\n")
        lines.append("| Ünite / blok | 2024 | 2025 | 2026 | Ağırlıklı pay | 2027 beklenen | Banka kotası |")
        lines.append("|---|---|---|---|---|---|---|")
        for unit in subject["units"]:
            observed = unit["observed"]
            lines.append(
                f"| {unit['name']} | {observed['2024']} | {observed['2025']} | {observed['2026']} | "
                f"%{unit['weightedShare'] * 100:.1f} | {unit['predictedPerExam']} ({unit['expectedPerExam']:.1f}) | {unit['bankQuota']} |"
            )
        unknown = subject["unknownUnitPerYear"]
        if any(unknown.values()):
            lines.append(f"| *ünitesi belirsiz* | {unknown['2024']} | {unknown['2025']} | {unknown['2026']} | – | – | – |")
        lines.append("")
    return "\n".join(lines)


FORMAT_MARKERS = {
    "görsel": None,
    "günlük yaşam bağlamı": ("günlük yaşam", "bağlam"),
    "öncüllü": ("öncüllü", "numaralı", "numaralanmış"),
    "olumsuz kök": ("olumsuz",),
    "deney/düzenek": ("deney", "düzenek"),
    "tablo/grafik": ("tablo", "grafik", "koordinat"),
    "çok kazanımlı": ("çok kazanımlı", "çok adımlı"),
    "kural/açıklama verip uygulama": ("kural", "açıklama verip", "tanım verip"),
}


def _has(question: dict[str, Any], words: tuple[str, ...] | None) -> bool:
    if words is None:
        visual = str(question.get("visual") or "").lower()
        return bool(visual) and not visual.startswith(("none", "yok"))
    text = " ".join([*question.get("format", []), str(question.get("visual") or "")]).lower()
    return any(word in text for word in words)


def appendix(inventory: dict[str, Any]) -> str:
    """Per-subject format counts and per-question reference tables."""
    lines = []
    for subject, definition in inventory["subjects"].items():
        units = {unit["key"]: unit["name"] for unit in definition["units"]}
        questions = [q for q in inventory["questions"] if q["subject"] == subject]
        lines.append(f"### {subject}\n")
        lines.append("| Özellik | " + " | ".join(YEARS) + " |")
        lines.append("|---|" + "---|" * len(YEARS))
        for label, words in FORMAT_MARKERS.items():
            row = [sum(1 for q in questions if str(q["year"]) == year and _has(q, words)) for year in YEARS]
            lines.append(f"| {label} | " + " | ".join(str(value) for value in row) + " |")
        lines.append("")
        for year in YEARS:
            year_questions = sorted((q for q in questions if str(q["year"]) == year), key=lambda q: q["qNo"])
            booklet = year_questions[0]["booklet"] if year_questions else "A"
            lines.append(f"**{year} ({booklet} kitapçığı)**\n")
            lines.append("| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |")
            lines.append("|---|---|---|---|---|---|")
            for q in year_questions:
                summary = (q.get("summary") or "—").replace("|", "/").replace("\n", " ")
                if len(summary) > 230:
                    summary = summary[:227].rstrip() + "…"
                lines.append(
                    f"| {q['qNo']} | {units.get(q.get('unit'), '—')} | {q.get('kazanim') or '—'} | {summary} | "
                    f"{q.get('answer') or '—'} | {q['confidence']} |"
                )
            lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if the committed plan is stale")
    parser.add_argument("--tables", action="store_true", help="print markdown unit tables")
    parser.add_argument("--appendix", action="store_true", help="print per-question reference tables")
    parser.add_argument("--bank-size", type=int, default=None)
    args = parser.parse_args()
    inventory = _load(INVENTORY)
    try:
        plan = build_plan(inventory, _load(REGISTRY), args.bank_size)
    except PlanError as exc:
        parser.error(str(exc))
    text = render(plan, INVENTORY)
    if args.tables:
        print(tables(plan))
        return 0
    if args.appendix:
        print(appendix(inventory))
        return 0
    if args.check:
        if not PLAN.exists() or PLAN.read_text(encoding="utf-8") != text:
            print(f"{PLAN.relative_to(ROOT)} is stale; run tools/build_lgs_2027_plan.py", file=sys.stderr)
            return 1
        return 0
    PLAN.parent.mkdir(parents=True, exist_ok=True)
    PLAN.write_text(text, encoding="utf-8")
    print(f"wrote {PLAN.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
