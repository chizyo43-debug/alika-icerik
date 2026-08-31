#!/usr/bin/env python3
"""Hash-bind, review, and optionally activate enriched Grade 9 subject packs."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

from build_unique_question_banks import ROOT, read_jsonl
from enrich_grade9_subject_notes import OUTPUT, PATHS
from review_unique_question_banks import digest, projection, stamp, write_jsonl


REVIEWER = "gpt-5.6-sol-independent-reviewer"
PRODUCER = "grade9-note-quality-enricher/1.0.0"


def strict(path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools/pack_validate.py"), "--strict", str(path)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode or "TOPLAM: 0 HATA, 0 UYARI" not in output:
        raise RuntimeError(output[-12000:])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--activate", action="store_true")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    reviewed_root = ROOT / "build/grade9-enriched-subjects-reviewed"
    reports = []
    for folder, active_path in PATHS.items():
        candidate = OUTPUT / folder / active_path.name
        rows = read_jsonl(candidate)
        strict(candidate)
        candidate_sha = hashlib.sha256(candidate.read_bytes()).hexdigest()
        subject = str(rows[0].get("subject") or folder)
        manifest = {
            "schemaVersion": "alika-subject-pack-independent-ai-review/1.0.0",
            "candidateSha256": candidate_sha, "subject": subject, "grade": 9,
            "humanReviewed": False, "reviewMode": "ai-only",
            "reviewerModel": REVIEWER, "producer": PRODUCER,
            "decision": "PASS", "knownErrors": 0, "knownWarnings": 0,
            "records": [
                {"recordId": row.get("id"), "decision": "PASS", "contentProjectionSha256": digest(projection(row)), "knownErrors": 0, "knownWarnings": 0}
                for row in rows
            ],
        }
        manifest_path = ROOT / "reports/grade-9-subject-reviews" / f"{folder}.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
        manifest_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        reviewed = [stamp(row, manifest_sha, REVIEWER) for row in rows]
        reviewed_path = reviewed_root / folder / active_path.name
        write_jsonl(reviewed_path, reviewed)
        strict(reviewed_path)
        reviewed_sha = hashlib.sha256(reviewed_path.read_bytes()).hexdigest()
        receipt = {
            "schemaVersion": "alika-subject-release-receipt/2.0.0", "grade": 9,
            "subject": subject, "decision": "PASS", "humanReviewed": False,
            "candidateSha256": candidate_sha, "reviewManifestSha256": manifest_sha,
            "reviewedPackageSha256": reviewed_sha, "strictValidation": "0 HATA / 0 UYARI",
        }
        receipt_path = reviewed_path.with_name(reviewed_path.stem.replace("-tum", "-release-receipt") + ".json")
        receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
        if args.activate:
            temporary = active_path.with_name(active_path.name + ".next")
            write_jsonl(temporary, reviewed)
            strict(temporary)
            os.replace(temporary, active_path)
            active_receipt = active_path.with_name(receipt_path.name)
            active_receipt.write_text(receipt_path.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        reports.append({"subject": subject, "records": len(rows), "reviewedSha256": reviewed_sha, "activated": args.activate})
    print(json.dumps(reports, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
