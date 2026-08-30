#!/usr/bin/env python3
"""Strict pre-release audit for partial or complete authored bank blueprints."""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from build_unique_question_banks import (
    ROOT, combined, difficulty_schedule, discover, load_authored_blueprints,
    load_authored_labels, mix_schedule, normalized, objective_of, token_shingles,
)
from pack_validate import figur_atfi_var, figur_kontrol, figur_zorunlu_kazanim


def numeric_copula_suffix(value: int) -> str:
    absolute = abs(value)
    ones = {0: "dır", 1: "dir", 2: "dir", 3: "tür", 4: "tür",
            5: "tir", 6: "dır", 7: "dir", 8: "dir", 9: "dur"}
    tens = {1: "dur", 2: "dir", 3: "dur", 4: "tır", 5: "dir",
            6: "tır", 7: "tir", 8: "dir", 9: "dır"}
    if absolute % 10:
        return ones[absolute % 10]
    if (absolute // 10) % 10:
        return tens[(absolute // 10) % 10]
    if (absolute // 100) % 10:
        return "dür"
    if absolute % 1_000_000:
        return "dir"
    return "dur"


def label_references(value: Any, field: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key.endswith("Key") and isinstance(child, str):
                found.add(child)
            elif key.endswith("Keys") and isinstance(child, list):
                found.update(str(item) for item in child if isinstance(item, str))
            else:
                found.update(label_references(child, key))
    elif isinstance(value, list):
        for child in value:
            found.update(label_references(child, field))
    return found


def audit(grade: int) -> dict[str, Any]:
    questions = load_authored_blueprints(grade)
    labels = load_authored_labels(grade)
    subjects = discover(grade)
    subject_by_name = {subject.subject: subject for subject in subjects}
    notes: dict[str, dict[str, Any]] = {}
    source_by_objective: dict[str, list[tuple[str, str, set[tuple[str, ...]]]]] = defaultdict(list)
    for subject in subjects:
        for note in subject.notes:
            notes[str(note.get("id"))] = note
        for source in subject.questions:
            full = combined(source)
            source_by_objective[objective_of(source)].append(
                (str(source.get("id")), full, token_shingles(full))
            )

    errors: list[str] = []
    warnings: list[str] = []
    if "i\u0307" in json.dumps(labels, ensure_ascii=False):
        errors.append("görsel etiketlerinde Türkçe küçük i üzerinde birleşik nokta artefaktı var")
    seen_ids: set[str] = set()
    seen_texts: set[str] = set()
    seen_full: set[str] = set()
    generated_by_objective: dict[str, list[tuple[str, str, set[tuple[str, ...]]]]] = defaultdict(list)
    skeletons: Counter[str] = Counter()
    visual_coverage: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    near_source = 0
    near_internal = 0

    for position, question in enumerate(questions, 1):
        qid = str(question.get("id") or "")
        subject_name = str(question.get("subject") or "")
        note_id = str(question.get("noteId") or "")
        objective = objective_of(question)
        choices = question.get("choices") or []
        correct = question.get("correct")
        text = normalized(question.get("question"))
        full = combined(question)
        if not qid.startswith(f"tr-g{grade:02d}-bank-"):
            errors.append(f"{qid or position}: banka kapsamlı kimlik öneki yok")
        if qid in seen_ids:
            errors.append(f"{qid}: yinelenen kimlik")
        if text in seen_texts:
            errors.append(f"{qid}: yinelenen soru metni")
        if full in seen_full:
            errors.append(f"{qid}: yinelenen soru+seçenek içeriği")
        seen_ids.add(qid); seen_texts.add(text); seen_full.add(full)
        skeletons[text] += 1
        if subject_name not in subject_by_name:
            errors.append(f"{qid}: tanımsız ders {subject_name!r}")
        note = notes.get(note_id)
        if note is None:
            errors.append(f"{qid}: bağlı not bulunamadı {note_id!r}")
        else:
            note_objectives = {str(value) for value in note.get("objectives") or [note.get("objective")]}
            if objective not in note_objectives:
                errors.append(f"{qid}: kazanım bağlı notla uyuşmuyor")
            for field in ("unitKey", "topicKey", "subtopicKey", "objectiveSource", "objectiveEvidenceId"):
                if question.get(field) != note.get(field):
                    errors.append(f"{qid}: {field} bağlı notla uyuşmuyor")
        if len(choices) != 4 or len({normalized(value) for value in choices}) != 4:
            errors.append(f"{qid}: dört benzersiz seçenek yok")
        if not isinstance(correct, int) or correct not in range(4):
            errors.append(f"{qid}: doğru indeks geçersiz")
        elif question.get("correctOption") != choices[correct]:
            errors.append(f"{qid}: doğru indeks/seçenek atomik değil")
        reasons = question.get("distractorWhy") or []
        if len(reasons) != 4 or any(len(str(reason)) < 45 or ":" not in str(reason) for reason in reasons):
            errors.append(f"{qid}: yanılgı adı taşıyan dört ayrıntılı gerekçe yok")
        if len(str(question.get("explanation") or "")) < 80:
            errors.append(f"{qid}: çözüm açıklaması yetersiz")
        if len(str(question.get("difficultyReason") or "")) < 45:
            errors.append(f"{qid}: zorluk gerekçesi yetersiz")
        figure = question.get("figure")
        visual = question.get("visualNeed") or {}
        visual_coverage[objective][1] += 1
        visual_coverage[objective][0] += int(bool(figure))
        if "i\u0307" in json.dumps(question, ensure_ascii=False):
            errors.append(f"{qid}: Türkçe küçük i üzerinde birleşik nokta artefaktı var")
        if subject_name == "Fen Bilimleri":
            science_text = " ".join(
                [str(question.get("question") or ""), *map(str, choices)]
            )
            if re.search(r"\.\s+durum(?:una|unu|u|udur)\b", science_text, re.I):
                errors.append(f"{qid}: nokta sonrasında bozuk 'durum' cümle bağlantısı var")
            if re.search(r"(?:\d\s+n\b|\bn['’](?:luk|lik|un|in))", science_text):
                errors.append(f"{qid}: newton birim simgesi küçük n yazılmış")
            if re.search(
                r"\b(?:dünya|ay|güneş)['’](?:da|de|dan|den|ın|in|a|e)\b",
                science_text,
            ):
                errors.append(f"{qid}: gök cismi özel adı küçük harfle yazılmış")
        if subject_name == "Matematik":
            math_text = json.dumps(question, ensure_ascii=False)
            for match in re.finditer(
                r"(?<![/.,])\b(\d(?:[\d ]*\d)?)['’](dır|dir|dur|dür|tır|tir|tur|tür)\b",
                math_text,
            ):
                value = int(match.group(1).replace(" ", ""))
                expected = numeric_copula_suffix(value)
                if match.group(2) != expected:
                    errors.append(
                        f"{qid}: {match.group(0)!r} ek uyumu yanlış; "
                        f"{value}'{expected} olmalı"
                    )
                    break
        if visual.get("level") == "required" and not figure:
            errors.append(f"{qid}: zorunlu görsel eksik")
        if figure and not figur_atfi_var(
            str(question.get("question") or ""), "tr", "question", False
        ):
            errors.append(f"{qid}: görsel var ancak soru metni ona açıkça atıf yapmıyor")
        if not figure and figur_atfi_var(
            str(question.get("question") or ""), "tr", "question", True
        ):
            errors.append(f"{qid}: soru görsele atıf yapıyor ancak figure boş")
        if figure:
            for message in figur_kontrol(figure, "2.0"):
                errors.append(f"{qid}: figure {message}")
            missing_labels = sorted(label_references(figure) - set(labels))
            if missing_labels:
                errors.append(f"{qid}: eksik görsel etiketleri {missing_labels[:4]}")
            alt = str(labels.get(figure.get("altTextKey"), "")) if isinstance(figure, dict) else ""
            if not alt:
                errors.append(f"{qid}: erişilebilir alt metin eksik")
            elif isinstance(correct, int) and correct in range(len(choices)):
                correct_norm = normalized(choices[correct])
                if len(correct_norm) > 20 and correct_norm in normalized(alt):
                    errors.append(f"{qid}: alt metin doğru cevabı sızdırıyor")
        shingles = token_shingles(full)
        for candidate_id, candidate, candidate_shingles in source_by_objective.get(objective, []):
            union = shingles | candidate_shingles
            if union and len(shingles & candidate_shingles) / len(union) >= 0.62:
                if SequenceMatcher(None, full, candidate, autojunk=False).ratio() > 0.88:
                    near_source += 1
                    errors.append(f"{qid}: kaynak soruya yakın kopya {candidate_id}")
                    break
        for candidate_id, candidate, candidate_shingles in generated_by_objective[objective]:
            union = shingles | candidate_shingles
            if union and len(shingles & candidate_shingles) / len(union) >= 0.62:
                if SequenceMatcher(None, full, candidate, autojunk=False).ratio() > 0.88:
                    near_internal += 1
                    errors.append(f"{qid}: banka içi yakın kopya {candidate_id}")
                    break
        generated_by_objective[objective].append((qid, full, shingles))

    for objective, (figured, total) in sorted(visual_coverage.items()):
        if figur_zorunlu_kazanim(objective):
            target = max(1, math.ceil(0.30 * total))
            if figured < target:
                errors.append(
                    f"{objective}: görsel-zorunlu kazanım kapsamı {figured}/{total}; "
                    f"en az {target}/{total} olmalı"
                )

    for batch_start in range(0, len(questions) - len(questions) % 100, 100):
        batch = questions[batch_start:batch_start + 100]
        expected_levels = Counter(difficulty_schedule(grade)[:100])
        expected_modes = Counter(mix_schedule(grade)[:100])
        if Counter(row.get("correct") for row in batch) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
            errors.append(f"parti {batch_start // 100 + 1}: cevap dengesi 25/25/25/25 değil")
        # Every 100-row authoring batch follows the exact grade-level ratios.
        ratios = ({1: 20, 2: 25, 3: 30, 4: 20, 5: 5} if grade <= 7 else
                  {1: 15, 2: 25, 3: 30, 4: 20, 5: 10} if grade <= 10 else
                  {1: 10, 2: 20, 3: 30, 4: 25, 5: 15})
        if Counter(row.get("level") for row in batch) != Counter(ratios):
            errors.append(f"parti {batch_start // 100 + 1}: zorluk dağılımı yanlış")
        if Counter(row.get("questionType") for row in batch) != Counter(
            {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
        ):
            errors.append(f"parti {batch_start // 100 + 1}: soru türü dağılımı yanlış")
        del expected_levels, expected_modes

    diversity = len(skeletons) / max(1, len(questions))
    largest = max(skeletons.values(), default=0) / max(1, len(questions))
    if questions and diversity < 0.60:
        errors.append(f"iskelet çeşitliliği %{diversity * 100:.1f}; en az %60 olmalı")
    if questions and largest > 0.10:
        errors.append(f"en büyük soru iskeleti %{largest * 100:.1f}; en çok %10 olmalı")
    return {
        "schemaVersion": "alika-question-bank-blueprint-audit/1.0.0",
        "grade": grade, "questions": len(questions),
        "subjects": dict(sorted(Counter(str(row.get("subject")) for row in questions).items())),
        "objectives": len({objective_of(row) for row in questions}),
        "figures": sum(bool(row.get("figure")) for row in questions),
        "answerPositions": dict(sorted(Counter(row.get("correct") for row in questions).items())),
        "difficulty": dict(sorted(Counter(row.get("level") for row in questions).items())),
        "questionTypes": dict(sorted(Counter(row.get("questionType") for row in questions).items())),
        "skeletonDiversity": round(diversity, 4), "largestSkeletonShare": round(largest, 4),
        "nearSourceAbove088": near_source, "nearInternalAbove088": near_internal,
        "errors": errors, "warnings": warnings,
        "status": "PASS" if not errors and not warnings else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grade", type=int, required=True, choices=range(5, 13))
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    report = audit(args.grade)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
