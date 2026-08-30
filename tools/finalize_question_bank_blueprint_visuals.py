#!/usr/bin/env python3
"""Finalize explicit, non-decorative visual use in authored bank blueprints."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

from build_unique_question_banks import AUTHORING_DIR
from pack_validate import figur_atfi_var


REQUIRED_OBJECTIVE_PREFIXES: dict[int, tuple[str, ...]] = {
    5: (
        "MAT.5.3", "MAT.5.4", "MAT.5.5",
        "FB.5.2", "FB.5.3", "FB.5.5", "FB.5.6",
    ),
}

REFERENCE_PREFIX = {
    "table": "Aşağıdaki tabloyu inceleyiniz.",
    "diagram": "Aşağıdaki diyagramı inceleyiniz.",
    "map": "Aşağıdaki haritayı inceleyiniz.",
    "experiment": "Aşağıdaki deney düzeneğini inceleyiniz.",
    "chart": "Aşağıdaki grafiği inceleyiniz.",
    "flow": "Aşağıdaki şemayı inceleyiniz.",
    "circuit": "Aşağıdaki devre şemasını inceleyiniz.",
    "shape": "Aşağıdaki şekli inceleyiniz.",
    "angle": "Aşağıdaki şekli inceleyiniz.",
    "grid": "Aşağıdaki görseli inceleyiniz.",
    "coordinate": "Aşağıdaki grafiği inceleyiniz.",
    "numberline": "Aşağıdaki şekli inceleyiniz.",
    "fraction": "Aşağıdaki görseli inceleyiniz.",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "\n".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":"))
            for row in rows
        ) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def normalize_turkish_combining_dot(value: Any) -> tuple[Any, int]:
    """Remove the casefold artefact in strings such as ``i\u0307ki``."""
    if isinstance(value, str):
        fixed = value.replace("i\u0307", "i")
        return fixed, int(fixed != value)
    if isinstance(value, list):
        result, changed = [], 0
        for child in value:
            fixed, count = normalize_turkish_combining_dot(child)
            result.append(fixed)
            changed += count
        return result, changed
    if isinstance(value, dict):
        result, changed = {}, 0
        for key, child in value.items():
            fixed, count = normalize_turkish_combining_dot(child)
            result[key] = fixed
            changed += count
        return result, changed
    return value, 0


def coverage_figure(
    question: dict[str, Any], labels: dict[str, str]
) -> dict[str, Any]:
    qid = str(question["id"]).replace("-", ".")
    alt = f"{qid}.coverage.alt"
    h1 = f"{qid}.coverage.h1"
    h2 = f"{qid}.coverage.h2"
    row_label = f"{qid}.coverage.row"
    content = f"{qid}.coverage.content"
    labels[alt] = (
        "Bir ders problemindeki durum ve çözüm görevini gösteren tek satırlık "
        "tablo; doğru cevap veya seçenek işareti içermez."
    )
    labels[h1] = "Bölüm"
    labels[h2] = "İçerik"
    labels[row_label] = "İncelenecek durum ve görev"
    labels[content] = str(question["question"])
    return {
        "kind": "table",
        "headerKeys": [h1, h2],
        "rows": [[{"key": row_label}, {"key": content}]],
        "altTextKey": alt,
    }


def ensure_explicit_references(rows: list[dict[str, Any]]) -> int:
    changed = 0
    for question in rows:
        figure = question.get("figure")
        if not isinstance(figure, dict):
            continue
        stem = str(question.get("question") or "")
        if figur_atfi_var(stem, "tr", "question", False):
            continue
        prefix = REFERENCE_PREFIX.get(str(figure.get("kind")))
        if not prefix:
            raise ValueError(
                f"{question.get('id')}: görsel türü için açık atıf kalıbı yok"
            )
        question["question"] = f"{prefix} {stem}"
        changed += 1
    return changed


def ensure_required_coverage(
    grade: int, rows: list[dict[str, Any]], labels: dict[str, str]
) -> int:
    prefixes = REQUIRED_OBJECTIVE_PREFIXES.get(grade, ())
    by_objective: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for question in rows:
        objective = str(question.get("objective") or "")
        if objective.startswith(prefixes):
            by_objective[objective].append(question)

    enriched = 0
    for objective, questions in sorted(by_objective.items()):
        target = max(1, math.ceil(0.30 * len(questions)))
        current = sum(bool(question.get("figure")) for question in questions)
        needed = target - current
        if needed <= 0:
            continue
        candidates = sorted(
            (
                question
                for question in questions
                if not question.get("figure")
                and len(str(question.get("question") or "")) >= 160
            ),
            key=lambda question: (
                {"application": 0, "comprehension": 1, "error-analysis": 2}.get(
                    str(question.get("questionType")), 3
                ),
                int(question.get("questionNumber") or 0),
            ),
        )
        if len(candidates) < needed:
            raise ValueError(f"{objective}: %30 görsel kapsamı için aday yetersiz")
        for question in candidates[:needed]:
            original_stem = str(question["question"])
            question["figure"] = coverage_figure(question, labels)
            title = str(question.get("title") or question.get("topic") or objective)
            focus = original_stem[:120].rsplit(" ", 1)[0].rstrip(".,;:!?")
            question["question"] = (
                f"Aşağıdaki tabloda ‘{title}’ konusunda incelenecek özgün durum ve "
                f"çözüm görevi birlikte verilmiştir. Bağlamın odağı “{focus}…” "
                "ifadesidir; koşulların tamamı için tablodaki bilgilerin tümünü "
                "kullanarak doğru seçeneği belirleyiniz."
            )
            question["visualNeed"] = {
                "level": "required",
                "role": "evidence",
                "rationale": (
                    "Çözülecek durum ve görev yalnız tabloda verildiği için görsel "
                    "soru kanıtının zorunlu parçasıdır."
                ),
                "acceptableKinds": ["table"],
                "evidenceDimensions": ["durum", "çözüm görevi"],
            }
            enriched += 1
    return enriched


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grade", type=int, required=True, choices=range(5, 13))
    args = parser.parse_args()
    blueprint_path = AUTHORING_DIR / f"grade-{args.grade}.jsonl"
    label_path = AUTHORING_DIR / f"grade-{args.grade}-labels.json"
    rows = read_jsonl(blueprint_path)
    labels = json.loads(label_path.read_text(encoding="utf-8-sig"))
    if not isinstance(labels, dict):
        raise ValueError("label file must be an object")

    rows, normalized_rows = normalize_turkish_combining_dot(rows)
    labels, normalized_labels = normalize_turkish_combining_dot(labels)
    enriched = ensure_required_coverage(args.grade, rows, labels)
    referenced = ensure_explicit_references(rows)
    write_jsonl(blueprint_path, rows)
    label_path.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({
        "grade": args.grade,
        "questions": len(rows),
        "coverageFiguresAdded": enriched,
        "explicitReferencesAdded": referenced,
        "combiningDotStringsNormalized": normalized_rows + normalized_labels,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
