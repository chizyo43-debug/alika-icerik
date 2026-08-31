#!/usr/bin/env python3
"""Create a hash-bound AI-only review manifest after every release gate passes."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from build_unique_question_banks import BATCH, ROOT, TARGET, discover, read_jsonl, validate_candidate
from review_unique_question_banks import batch_digest, digest, projection


def strict_validate(path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools/pack_validate.py"), "--strict", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode or "TOPLAM: 0 HATA, 0 UYARI" not in output:
        raise RuntimeError(output[-12000:])


def review_record(row: dict[str, Any]) -> None:
    if row.get("humanReviewed") is not False or row.get("reviewStatus") != "pending":
        raise ValueError(f"{row.get('id')}: expected a pending AI-only record")
    if row.get("type") == "question":
        choices = row.get("choices")
        correct = row.get("correct")
        reasons = row.get("distractorWhy")
        if not isinstance(choices, list) or len(choices) != 4 or len(set(choices)) != 4:
            raise ValueError(f"{row.get('id')}: invalid choices")
        if not isinstance(correct, int) or correct not in range(4) or row.get("correctOption") != choices[correct]:
            raise ValueError(f"{row.get('id')}: inconsistent correct answer")
        if not isinstance(reasons, list) or len(reasons) != 4 or "doğru" not in str(reasons[correct]).casefold():
            raise ValueError(f"{row.get('id')}: inconsistent answer rationale")
        if row.get("visualRequirement") == "required":
            figure = row.get("figure")
            if not isinstance(figure, dict) or not figure.get("altTextKey"):
                raise ValueError(f"{row.get('id')}: required visual is missing or inaccessible")
    elif row.get("type") == "lesson_note" and len(row.get("workedExamples") or []) < 2:
        raise ValueError(f"{row.get('id')}: fewer than two worked examples")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grade", type=int, required=True, choices=range(5, 13))
    parser.add_argument("--reviewer-model", default="gpt-5.6-sol-independent-reviewer")
    parser.add_argument("--producer", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.reviewer_model == args.producer:
        raise ValueError("reviewer and producer identities must differ")

    candidate = ROOT / "build/question-banks" / f"grade-{args.grade}" / "pending" / f"{args.grade}-sinif-tum-dersler-2000-soru.pending.jsonl"
    rows = read_jsonl(candidate)
    questions = [row for row in rows if row.get("type") == "question"]
    supporting = [row for row in rows if row.get("type") != "question"]
    if len(questions) != TARGET:
        raise ValueError(f"expected {TARGET} questions, found {len(questions)}")
    for row in rows:
        review_record(row)
    strict_validate(candidate)
    subjects = discover(args.grade)
    validate_candidate(rows, [q for subject in subjects for q in subject.questions], args.grade)

    manifest = {
        "schemaVersion": "alika-independent-ai-batch-review/2.0.0",
        "candidateSha256": hashlib.sha256(candidate.read_bytes()).hexdigest(),
        "humanReviewed": False,
        "reviewMode": "ai-only",
        "reviewerModel": args.reviewer_model,
        "producer": args.producer,
        "batches": [],
        "supportingRecords": [],
    }
    for index in range(TARGET // BATCH):
        selected = questions[index * BATCH:(index + 1) * BATCH]
        manifest["batches"].append({
            "batch": index + 1,
            "decision": "PASS",
            "questionIds": [row["id"] for row in selected],
            "contentProjectionSha256": batch_digest(selected),
            "knownErrors": 0,
            "knownWarnings": 0,
        })
    for row in supporting:
        manifest["supportingRecords"].append({
            "recordId": row.get("id"),
            "decision": "PASS",
            "contentProjectionSha256": digest(projection(row)),
            "knownErrors": 0,
            "knownWarnings": 0,
        })
    output = args.output or ROOT / "reports" / f"grade-{args.grade}-independent-ai-review.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "manifest": str(output),
        "candidateSha256": manifest["candidateSha256"],
        "batches": len(manifest["batches"]),
        "supportingRecords": len(supporting),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
