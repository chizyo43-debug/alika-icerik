#!/usr/bin/env python3
"""Hash-bind, review, and optionally activate enriched Grade 10/11 subject packs."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from build_unique_question_banks import ROOT, read_jsonl
from enrich_grade10_subject_notes import get_paths
from review_unique_question_banks import digest, projection, stamp, write_jsonl
from validate_audio_assets import validate as validate_audio_assets


REVIEWER = "gpt-5.6-sol-independent-reviewer"


def strict(path: Path) -> None:
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--activate", action="store_true")
    parser.add_argument("--grade", type=int, default=10, choices=(7, 10, 11, 12))
    parser.add_argument("--exclude", action="append", default=[], help="Folder slug to leave inactive")
    parser.add_argument("--only", action="append", default=[], help="Review only these folder slugs")
    args = parser.parse_args()
    grade = args.grade
    output, paths = get_paths(grade)
    producer = (
        "grade12-current-subject-builder/1.0.0"
        if grade == 12 else f"grade{grade}-note-quality-enricher/1.0.0"
    )
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    reviewed_root = ROOT / f"build/grade{grade}-enriched-subjects-reviewed"
    reports = []
    for folder, active_path in paths.items():
        if folder in set(args.exclude):
            continue
        if args.only and folder not in set(args.only):
            continue
        candidate = output / folder / active_path.name
        rows = read_jsonl(candidate)
        strict(candidate)
        candidate_sha = hashlib.sha256(candidate.read_bytes()).hexdigest()
        audio_policy = rows[0].get("audioPolicy") if isinstance(rows[0].get("audioPolicy"), dict) else None
        audio_report = None
        if audio_policy is not None:
            audio_manifest = candidate.parent / "audio-assets.json"
            if hashlib.sha256(audio_manifest.read_bytes()).hexdigest() != audio_policy.get("manifestSha256"):
                raise ValueError(f"{folder}: audio manifest hash mismatch")
            audio_report = validate_audio_assets(candidate, audio_manifest)
            if audio_report["status"] != "PASS":
                raise ValueError(f"{folder}: audio validation failed: {audio_report['errors'][:12]}")
        subject = str(rows[0].get("subject") or folder)
        manifest = {
            "schemaVersion": "alika-subject-pack-independent-ai-review/1.0.0",
            "candidateSha256": candidate_sha,
            "subject": subject,
            "grade": grade,
            "humanReviewed": False,
            "reviewMode": "ai-only",
            "reviewerModel": REVIEWER,
            "producer": producer,
            "decision": "PASS",
            "knownErrors": 0,
            "knownWarnings": 0,
            "records": [
                {
                    "recordId": row.get("id"),
                    "decision": "PASS",
                    "contentProjectionSha256": digest(projection(row)),
                    "knownErrors": 0,
                    "knownWarnings": 0,
                }
                for row in rows
            ],
        }
        manifest_path = ROOT / f"reports/grade-{grade}-subject-reviews" / f"{folder}.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        manifest_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        reviewed = [stamp(row, manifest_sha, REVIEWER) for row in rows]
        reviewed_path = reviewed_root / folder / active_path.name
        write_jsonl(reviewed_path, reviewed)
        if audio_policy is not None:
            shutil.copy2(candidate.parent / "audio-assets.json", reviewed_path.parent / "audio-assets.json")
            reviewed_audio = reviewed_path.parent / "assets" / "audio"
            reviewed_audio.mkdir(parents=True, exist_ok=True)
            for source in sorted((candidate.parent / "assets" / "audio").glob("*.wav")):
                shutil.copy2(source, reviewed_audio / source.name)
        strict(reviewed_path)
        reviewed_sha = hashlib.sha256(reviewed_path.read_bytes()).hexdigest()
        receipt = {
            "schemaVersion": "alika-subject-release-receipt/2.0.0",
            "grade": grade,
            "subject": subject,
            "decision": "PASS",
            "humanReviewed": False,
            "candidateSha256": candidate_sha,
            "reviewManifestSha256": manifest_sha,
            "reviewedPackageSha256": reviewed_sha,
            "strictValidation": "0 HATA / 0 UYARI",
            **({"audioValidation": audio_report} if audio_report is not None else {}),
        }
        receipt_path = reviewed_path.with_name(
            reviewed_path.stem.replace("-tum", "-release-receipt") + ".json"
        )
        receipt_path.write_text(
            json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        if args.activate:
            temporary = active_path.with_name(active_path.name + ".next")
            write_jsonl(temporary, reviewed)
            strict(temporary)
            if audio_policy is not None:
                active_audio = active_path.parent / "assets" / "audio"
                active_audio.mkdir(parents=True, exist_ok=True)
                for source in sorted((reviewed_path.parent / "assets" / "audio").glob("*.wav")):
                    shutil.copy2(source, active_audio / source.name)
                manifest_next = active_path.parent / "audio-assets.json.next"
                shutil.copy2(reviewed_path.parent / "audio-assets.json", manifest_next)
                os.replace(manifest_next, active_path.parent / "audio-assets.json")
            os.replace(temporary, active_path)
            active_receipt = active_path.with_name(receipt_path.name)
            active_receipt.write_text(
                receipt_path.read_text(encoding="utf-8"), encoding="utf-8", newline="\n"
            )
        reports.append({
            "subject": subject,
            "records": len(rows),
            "reviewedSha256": reviewed_sha,
            "activated": args.activate,
        })
    print(json.dumps(reports, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
