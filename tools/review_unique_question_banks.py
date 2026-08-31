#!/usr/bin/env python3
"""Verify, attest and optionally activate a pending unique question bank.

This command cannot invent an AI review.  It requires a separate manifest with
one hash-bound PASS decision per 100-question batch, reruns deterministic gates,
then stamps the immutable content projection.  Activation uses ``os.replace``
only after the repository strict validator reports zero errors and warnings.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from build_unique_question_banks import (
    BATCH, METHOD, REVIEW_FIELDS, ROOT, TARGET, canonical_bytes, discover,
    objective_of, read_jsonl, validate_candidate,
)
from validate_audio_assets import validate as validate_audio_assets


REVIEW_METHOD = "alika-hash-bound-independent-ai-review/2.0.0"
DECLARATION = "ai-generated-and-independently-ai-reviewed-no-human-review"


def projection(row: dict[str, Any]) -> dict[str, Any]:
    return {key: copy.deepcopy(value) for key, value in row.items() if key not in REVIEW_FIELDS}


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def batch_digest(questions: list[dict[str, Any]]) -> str:
    return hashlib.sha256(b"\n".join(canonical_bytes(projection(row)) for row in questions) + b"\n").hexdigest()


def verify_external_manifest(
    manifest: dict[str, Any], questions: list[dict[str, Any]], candidate_sha: str,
    supporting_rows: list[dict[str, Any]] | None = None,
) -> None:
    if manifest.get("schemaVersion") != "alika-independent-ai-batch-review/2.0.0":
        raise ValueError("review manifest schema mismatch")
    if manifest.get("candidateSha256") != candidate_sha:
        raise ValueError("review manifest is not bound to this candidate")
    if manifest.get("humanReviewed") is not False or manifest.get("reviewMode") != "ai-only":
        raise ValueError("review mode mismatch")
    reviewer = str(manifest.get("reviewerModel") or "")
    producer = str(manifest.get("producer") or "")
    if not reviewer or reviewer == producer:
        raise ValueError("independent reviewer identity missing")
    batches = manifest.get("batches")
    if not isinstance(batches, list) or len(batches) != TARGET // BATCH:
        raise ValueError("exactly twenty batch decisions are required")
    for index in range(TARGET // BATCH):
        batch = batches[index]
        selected = questions[index * BATCH:(index + 1) * BATCH]
        expected_ids = [row["id"] for row in selected]
        if (
            batch.get("batch") != index + 1
            or batch.get("decision") != "PASS"
            or batch.get("questionIds") != expected_ids
            or batch.get("contentProjectionSha256") != batch_digest(selected)
            or batch.get("knownErrors") != 0
            or batch.get("knownWarnings") != 0
        ):
            raise ValueError(f"batch {index + 1}: incomplete or stale AI decision")
    supporting = manifest.get("supportingRecords")
    if not isinstance(supporting, list):
        raise ValueError("supporting record decisions are required")
    expected_supporting = list(supporting_rows or [])
    if len(supporting) != len(expected_supporting):
        raise ValueError("supporting record decision count mismatch")
    for index, row in enumerate(expected_supporting):
        decision = supporting[index]
        if (
            decision.get("recordId") != row.get("id")
            or decision.get("decision") != "PASS"
            or decision.get("contentProjectionSha256") != digest(projection(row))
            or decision.get("knownErrors") != 0
            or decision.get("knownWarnings") != 0
        ):
            raise ValueError(f"supporting record {row.get('id')}: incomplete or stale AI decision")


def stamp(row: dict[str, Any], manifest_sha: str, reviewer: str) -> dict[str, Any]:
    clean = projection(row)
    content_sha = digest(clean)
    decision_sha = digest({
        "recordId": clean.get("id"), "contentProjectionSha256": content_sha,
        "reviewManifestSha256": manifest_sha, "decision": "PASS",
        "reviewerModel": reviewer, "method": REVIEW_METHOD,
    })
    clean.update({
        "reviewStatus": "ai-verified", "humanReviewed": False,
        "reviewMode": "ai-only", "reviewModel": reviewer,
        "reviewDeclaration": DECLARATION, "reviewMethodVersion": REVIEW_METHOD,
        "reviewedContentSha256": content_sha,
        "reviewDecisionSha256": decision_sha,
        "reviewManifestSha256": manifest_sha,
        "contentHash": f"sha256:{content_sha}", "reviewedHash": f"sha256:{content_sha}",
        "publishReady": True, "publishBlocked": False,
        "productionStatus": "reviewed-release-candidate",
        "disclosure": DECLARATION,
        "provenance": (
            f"ai-verified:{decision_sha}; review-manifest:{manifest_sha}; "
            f"model:{reviewer}; mode:ai-only; human-review:false"
        ),
        "reviewAttestation": {
            "schema": "alika-bank-record-review-attestation/2.0.0",
            "decision": "PASS", "recordId": clean.get("id"),
            "contentProjectionSha256": content_sha,
            "reviewDecisionSha256": decision_sha,
            "reviewManifestSha256": manifest_sha,
            "reviewMethodVersion": REVIEW_METHOD,
            "model": reviewer, "mode": "ai-only", "humanReviewed": False,
            "declaration": DECLARATION,
        },
    })
    return clean


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n",
        encoding="utf-8", newline="\n",
    )


def strict_validate(path: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "pack_validate.py"), "--strict", str(path)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode or "TOPLAM: 0 HATA, 0 UYARI" not in output:
        raise RuntimeError(output[-12000:])
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grade", type=int, required=True, choices=range(5, 13))
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--activate", action="store_true")
    args = parser.parse_args()
    pending_path = ROOT / "build" / "question-banks" / f"grade-{args.grade}" / "pending" / f"{args.grade}-sinif-tum-dersler-2000-soru.pending.jsonl"
    rows = read_jsonl(pending_path)
    questions = [row for row in rows if row.get("type") == "question"]
    supporting_rows = [row for row in rows if row.get("type") != "question"]
    candidate_sha = hashlib.sha256(pending_path.read_bytes()).hexdigest()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
    verify_external_manifest(manifest, questions, candidate_sha, supporting_rows)
    subjects = discover(args.grade)
    metrics = validate_candidate(rows, [q for subject in subjects for q in subject.questions], args.grade)
    audio_policy = rows[0].get("audioPolicy") if isinstance(rows[0].get("audioPolicy"), dict) else None
    audio_report = None
    pending_audio_manifest = pending_path.parent / "audio-assets.json"
    if audio_policy is not None:
        if hashlib.sha256(pending_audio_manifest.read_bytes()).hexdigest() != audio_policy.get("manifestSha256"):
            raise ValueError("audio manifest is not bound to the candidate pack")
        audio_report = validate_audio_assets(
            pending_path, pending_audio_manifest, allow_runtime_pending=False,
        )
        if audio_report["status"] != "PASS":
            raise ValueError(f"audio validation failed: {audio_report['errors'][:12]}")
    manifest_sha = hashlib.sha256(args.manifest.read_bytes()).hexdigest()
    reviewer = manifest["reviewerModel"]
    reviewed = [stamp(row, manifest_sha, reviewer) for row in rows]
    release_dir = ROOT / "build" / "question-banks" / f"grade-{args.grade}" / "reviewed"
    candidate = release_dir / f"{args.grade}-sinif-tum-dersler-2000-soru.reviewed.jsonl"
    write_jsonl(candidate, reviewed)
    if audio_policy is not None:
        shutil.copy2(pending_audio_manifest, release_dir / "audio-assets.json")
        reviewed_assets = release_dir / "assets" / "audio"
        reviewed_assets.mkdir(parents=True, exist_ok=True)
        for source in sorted((pending_path.parent / "assets" / "audio").glob("*.wav")):
            shutil.copy2(source, reviewed_assets / source.name)
    strict_output = strict_validate(candidate)
    android_bundle = None
    if audio_policy is not None:
        bundle_path = release_dir / f"{args.grade}-sinif-tum-dersler-2000-soru.alika.zip"
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "build_audio_class_bundle.py"),
                "--package", str(candidate),
                "--audio-manifest", str(release_dir / "audio-assets.json"),
                "--output", str(bundle_path),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode:
            raise RuntimeError((result.stdout or "") + (result.stderr or ""))
        android_bundle = json.loads(result.stdout.strip().splitlines()[-1])
    receipt = {
        "schemaVersion": "alika-question-bank-release-receipt/2.0.0",
        "grade": args.grade, "decision": "PASS", "humanReviewed": False,
        "candidateSha256": candidate_sha, "reviewManifestSha256": manifest_sha,
        "reviewedPackageSha256": hashlib.sha256(candidate.read_bytes()).hexdigest(),
        "builder": METHOD, "reviewMethod": REVIEW_METHOD, "metrics": metrics,
        "strictValidation": "0 HATA / 0 UYARI",
        **({"audioValidation": audio_report} if audio_report is not None else {}),
        **({"androidClassBundle": android_bundle} if android_bundle is not None else {}),
    }
    receipt_path = release_dir / f"grade-{args.grade}-release-receipt.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    if args.activate:
        target_dir = ROOT / "turkiye" / f"{args.grade}-sinif" / "soru-bankasi"
        target = target_dir / f"{args.grade}-sinif-tum-dersler-2000-soru.jsonl"
        target_receipt = target_dir / f"{args.grade}-sinif-tum-dersler-2000-soru-release-receipt.json"
        temporary = target.with_suffix(".jsonl.next")
        write_jsonl(temporary, reviewed)
        strict_validate(temporary)
        if audio_policy is not None:
            active_assets = target_dir / "assets" / "audio"
            active_assets.mkdir(parents=True, exist_ok=True)
            for source in sorted((release_dir / "assets" / "audio").glob("*.wav")):
                shutil.copy2(source, active_assets / source.name)
            audio_manifest_next = target_dir / "audio-assets.json.next"
            shutil.copy2(release_dir / "audio-assets.json", audio_manifest_next)
            os.replace(audio_manifest_next, target_dir / "audio-assets.json")
            bundle_source = release_dir / f"{args.grade}-sinif-tum-dersler-2000-soru.alika.zip"
            bundle_next = target_dir / f"{args.grade}-sinif-tum-dersler-2000-soru.alika.zip.next"
            shutil.copy2(bundle_source, bundle_next)
            os.replace(
                bundle_next,
                target_dir / f"{args.grade}-sinif-tum-dersler-2000-soru.alika.zip",
            )
        os.replace(temporary, target)
        target_receipt.write_text(receipt_path.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    print(json.dumps({"candidate": str(candidate), "receipt": str(receipt_path), "activated": args.activate, "strict": strict_output.splitlines()[-1:]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
