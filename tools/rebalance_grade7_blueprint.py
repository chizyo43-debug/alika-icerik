#!/usr/bin/env python3
"""Repair Grade 7 authored quotas after canonical source-note changes."""
from __future__ import annotations

import json
import sys
from collections import Counter

from author_grade9_question_bank import build_question
from build_unique_question_banks import AUTHORING_DIR, discover, subject_quotas


GRADE = 7
BLUEPRINT = AUTHORING_DIR / "grade-7.jsonl"
LABELS = AUTHORING_DIR / "grade-7-labels.json"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    rows = [json.loads(line) for line in BLUEPRINT.read_text(encoding="utf-8").splitlines() if line.strip()]
    labels = json.loads(LABELS.read_text(encoding="utf-8")) if LABELS.exists() else {}
    subjects = {item.subject: item for item in discover(GRADE)}
    quotas = subject_quotas(list(subjects.values()))
    current = Counter(str(row.get("subject") or "") for row in rows)
    deficits = {subject: quotas[subject] - current[subject] for subject in quotas if quotas[subject] > current[subject]}
    excesses = {subject: current[subject] - quotas[subject] for subject in quotas if current[subject] > quotas[subject]}
    if sum(deficits.values()) != sum(excesses.values()):
        raise ValueError({"deficits": deficits, "excesses": excesses})

    replacements: list[tuple[int, str]] = []
    used_positions: set[int] = set()
    target_subjects = [subject for subject, count in sorted(deficits.items()) for _ in range(count)]
    for answer_position, target_subject in enumerate(target_subjects):
        source_subject = next(subject for subject, count in excesses.items() if count > 0)
        candidates = [
            (index, row) for index, row in enumerate(rows)
            if row.get("subject") == source_subject
            and int(row.get("correct", -1)) == answer_position % 4
            and index not in used_positions
        ]
        if not candidates:
            raise ValueError(f"{source_subject}: no replaceable answer position {answer_position % 4}")
        index, _ = candidates[-1]
        replacements.append((index, target_subject))
        used_positions.add(index)
        excesses[source_subject] -= 1

    objective_counts = Counter((str(row.get("subject") or ""), str(row.get("objective") or "")) for row in rows)
    for index, target_subject in replacements:
        subject = subjects[target_subject]
        note_by_objective = {}
        for note in subject.notes:
            for objective in note.get("objectives") or [note.get("objective")]:
                if objective:
                    note_by_objective.setdefault(str(objective), note)
        objective = min(sorted(subject.by_objective), key=lambda value: (objective_counts[(target_subject, value)], value))
        note = note_by_objective[objective]
        question_number = int(rows[index].get("questionNumber") or index + 1)
        occurrence = objective_counts[(target_subject, objective)]
        replacement = build_question(GRADE, question_number, target_subject, objective, note, occurrence, labels)
        if replacement["correct"] != rows[index]["correct"]:
            raise ValueError(f"answer balance changed at {question_number}")
        replacement["level"] = rows[index]["level"]
        replacement["difficultyReason"] = (
            f"Düzey {replacement['level']}; {objective} bilgisini yeni kanıtla ilişkilendirip "
            "üç adlandırılmış yanılgıyı ayırmayı gerektirir."
        )
        rows[index] = replacement
        objective_counts[(target_subject, objective)] += 1

    final_counts = Counter(str(row.get("subject") or "") for row in rows)
    # A previous interrupted run may have written the four replacements before
    # this level-preservation guard existed.  Normalize only this tool's rows.
    for row in rows:
        if str(row.get("authoringTemplateId") or "").startswith("g7-current-") and int(row.get("questionNumber") or 0) in range(397, 401):
            row["level"] = 4
            row["difficultyReason"] = (
                f"Düzey 4; {row.get('objective')} bilgisini yeni kanıtla ilişkilendirip "
                "üç adlandırılmış yanılgıyı ayırmayı gerektirir."
            )
    if final_counts != Counter(quotas):
        raise ValueError({"actual": final_counts, "expected": quotas})
    if Counter(int(row["correct"]) for row in rows) != Counter({0: 500, 1: 500, 2: 500, 3: 500}):
        raise ValueError("answer balance changed")
    BLUEPRINT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n",
        encoding="utf-8", newline="\n",
    )
    LABELS.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"replacements": len(replacements), "quotas": quotas, "answers": dict(Counter(row["correct"] for row in rows))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
