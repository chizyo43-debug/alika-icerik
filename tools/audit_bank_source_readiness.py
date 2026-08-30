#!/usr/bin/env python3
"""Profile lesson-note and semantic-input readiness for unique bank authoring."""
from __future__ import annotations

import json
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

from build_unique_question_banks import (
    ROOT, discover, load_authored_blueprints, subject_quotas,
)


REQUIRED_SECTIONS = {
    "whatIWillLearn", "keyConcepts", "priorKnowledge", "steps", "workedExamples",
    "commonMistakes", "selfCheck", "summary", "figureNote",
}
GENERIC_TEMPLATE_MARKERS = (
    "temel kavramları ayırmak, aralarındaki ilişkiyi güvenilir kanıtla kurmak",
    "çalışma kaydı",
    "bağlam dizisi",
)

SECTION_MINIMUMS = {
    "whatIWillLearn": 30,
    "priorKnowledge": 30,
    "keyConcepts": 200,
    "steps": 25,
    "commonMistakes": 100,
    "summary": 30,
}


def note_failures(note: dict[str, Any]) -> list[str]:
    failures = []
    body = str(note.get("body") or "")
    sections = note.get("lessonSections")
    if len(body) < 800:
        failures.append("body_short")
    if not isinstance(sections, dict) or not REQUIRED_SECTIONS <= set(sections):
        failures.append("sections_missing")
        return failures
    examples = sections.get("workedExamples")
    if not isinstance(examples, list) or len(examples) < 2 or any(len(str(value)) < 120 for value in examples[:2]):
        failures.append("worked_examples_insufficient")
    for key, minimum in SECTION_MINIMUMS.items():
        if len(str(sections.get(key) or "").strip()) < minimum:
            failures.append(f"section_{key}_insufficient")
    if note.get("figure") is not None and len(str(sections.get("figureNote") or "").strip()) < 40:
        failures.append("section_figureNote_insufficient")
    self_check = sections.get("selfCheck")
    if not isinstance(self_check, list) or len(self_check) < 3:
        failures.append("self_check_insufficient")
    # A single ordinary phrase such as “amaç, yöntem, kanıt ve sonuç” is not
    # evidence of templated prose.  Require multiple high-specificity template
    # markers so rich, subject-specific notes do not receive false alarms.
    marker_body = unicodedata.normalize("NFKC", body).casefold()
    marker_hits = sum(
        unicodedata.normalize("NFKC", marker).casefold() in marker_body
        for marker in GENERIC_TEMPLATE_MARKERS
    )
    if marker_hits >= 2:
        failures.append("generic_template_language")
    if not note.get("objectiveSource") or not note.get("objectiveEvidenceId"):
        failures.append("meb_anchor_missing")
    return failures


def audit_grade(grade: int, activation: dict[str, Any]) -> dict[str, Any]:
    subjects = discover(grade)
    quotas = subject_quotas(subjects)
    authored_counts = Counter(
        str(row.get("subject") or "") for row in load_authored_blueprints(grade)
    )
    subject_results = []
    grade_failures = []
    for subject in subjects:
        failure_counts: Counter[str] = Counter()
        failed_notes = []
        for note in subject.notes:
            failures = note_failures(note)
            failure_counts.update(failures)
            if failures:
                failed_notes.append({"id": note.get("id"), "failures": failures})
        authored = authored_counts.get(subject.subject, 0)
        shortage = max(0, quotas[subject.subject] - authored)
        if shortage:
            grade_failures.append(f"{subject.subject}:independent_authoring_shortage")
        if failed_notes:
            grade_failures.append(f"{subject.subject}:note_quality")
        subject_results.append({
            "subject": subject.subject,
            "sourcePath": subject.path.relative_to(ROOT).as_posix(),
            "quota": quotas[subject.subject],
            "canonicalObjectives": len(subject.by_objective),
            "notes": len(subject.notes),
            "questions": len(subject.questions),
            "sourceQuestionsReservedForCopyDetection": len(subject.questions),
            "independentlyAuthoredQuestions": authored,
            "newAuthoringMinimum": shortage,
            "failedNoteCount": len(failed_notes),
            "failureCounts": dict(sorted(failure_counts.items())),
            "failedNotes": failed_notes,
        })
    activation_entry = activation["grades"][str(grade)]
    if activation_entry["repositorySourceStatus"] != "eligible":
        grade_failures.append("curriculum_not_active")
    return {
        "grade": grade,
        "curriculum": activation_entry,
        "subjectQuotas": quotas,
        "subjects": subject_results,
        "status": "READY" if not grade_failures else "BLOCKED",
        "blockingFindings": sorted(set(grade_failures)),
    }


def main() -> int:
    activation = json.loads((ROOT / "curriculum" / "tr-2026-2027-activation.json").read_text(encoding="utf-8"))
    grades = [audit_grade(grade, activation) for grade in range(5, 13)]
    report = {
        "schemaVersion": "alika-bank-source-readiness/1.1.0",
        "intendedUse": "5–12. sınıf 2.000 özgün soruluk aktif banka üretimi",
        "grain": "sınıf/ders/not/kazanım ve bağımsız yazılmış tam soru kaydı",
        "schoolYear": "2026-2027",
        "summary": {
            "readyGrades": [item["grade"] for item in grades if item["status"] == "READY"],
            "blockedGrades": [item["grade"] for item in grades if item["status"] == "BLOCKED"],
        },
        "grades": grades,
    }
    target = ROOT / "reports" / "question-bank-source-readiness.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
