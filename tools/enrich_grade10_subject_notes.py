#!/usr/bin/env python3
"""Stage Grade 10/11 subject packs with quality-complete, ID-preserving notes."""
from __future__ import annotations

import copy
import argparse
import json
import sys

from audit_bank_source_readiness import note_failures
from build_unique_question_banks import ROOT, read_jsonl
from enrich_grade9_subject_notes import enrich_note
from review_unique_question_banks import projection, write_jsonl


def get_paths(grade: int) -> tuple[object, dict]:
    output = (
        ROOT / "build/grade12-current-subjects"
        if grade == 12 else ROOT / f"build/grade{grade}-enriched-subjects"
    )
    paths = {
        path.parent.name: path
        for path in sorted((ROOT / f"turkiye/{grade}-sinif").glob("*/*-tum.jsonl"))
        if path.parent.name != "soru-bankasi"
    }
    return output, paths


def pending(row: dict, grade: int) -> dict:
    clean = projection(row)
    clean.update({
        "reviewStatus": "pending",
        "humanReviewed": False,
        "reviewMode": "ai-only",
        "reviewDeclaration": "ai-generated-pending-independent-ai-review",
        "publishReady": False,
        "publishBlocked": True,
        "productionStatus": "pending-independent-ai-review",
        "disclosure": "ai-generated-pending-independent-ai-review",
        "provenance": f"pending:grade{grade}-note-quality-enricher/1.0.0; human-review:false",
    })
    return clean


def normalize_note_identity(row: dict) -> dict:
    """Fill importer-required note identity fields without changing stable IDs."""
    note = copy.deepcopy(row)
    objectives = [str(value) for value in (note.get("objectives") or []) if value]
    objective = str(note.get("objective") or note.get("objectiveId") or "").strip()
    if not objective and objectives:
        objective = objectives[0]
    if objective and not objectives:
        objectives = [objective]
    objective_text = note.get("objectiveText")
    if isinstance(objective_text, list):
        objective_text = next((str(value).strip() for value in objective_text if str(value).strip()), "")
    title = str(note.get("title") or note.get("topic") or objective_text or objective).strip()
    topic = str(note.get("topic") or title).strip()
    note_id = str(note.get("id") or note.get("noteId") or note.get("noteKey") or "").strip()
    note["title"] = title
    note["topic"] = topic
    note["objective"] = objective
    note["objectives"] = objectives
    note["noteId"] = note_id
    note["noteKey"] = note_id
    return note


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grade", type=int, default=10, choices=(7, 10, 11, 12))
    args = parser.parse_args()
    grade = args.grade
    output, paths = get_paths(grade)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = []
    for folder, source in paths.items():
        rows = read_jsonl(source)
        staged = []
        changed = 0
        for row in rows:
            current = row
            if row.get("type") == "note":
                current = normalize_note_identity(row)
                if note_failures(current):
                    current = enrich_note(current)
                changed += int(current != row)
            elif row.get("type") == "pack":
                current = copy.deepcopy(row)
                version = current.get("version")
                current["version"] = version + 1 if isinstance(version, int) else "2"
            staged.append(pending(current, grade))
        target = output / folder / source.name
        write_jsonl(target, staged)
        report.append({
            "subject": rows[0].get("subject"),
            "records": len(rows),
            "notesChanged": changed,
            "candidate": str(target),
        })
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
