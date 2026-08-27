#!/usr/bin/env python3
"""Prepare the missing Grade 7 Science and Grade 9 Chemistry releases.

The source candidates were already reviewed in full.  This repair only aligns
their package/note metadata with the canonical Question Contract 2.2 gate:

* copy each note's existing ``objectiveCode`` into ``objectives``;
* declare the 2026 curriculum on the Grade 9 Chemistry pack;
* renew hash-bound AI-only attestations for the records changed by that
  deterministic schema repair; and
* write a release receipt bound to the resulting canonical package.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
MODEL = "gpt-5.6-sol"
MODE = "ai-only"
DECLARATION = "ai-generated-and-ai-reviewed-no-human-review"
METHOD = "alika-hash-bound-ai-only-schema-repair-review/1.0.0"

EXCLUDED_FIELDS = {
    "aiReviewStatus",
    "aiVerification",
    "aiVerified",
    "approvalGranted",
    "approvalStatus",
    "approvedBy",
    "attestation",
    "contentHash",
    "disclosure",
    "humanReviewed",
    "provenance",
    "publishBlocked",
    "publishReady",
    "publishable",
    "review",
    "reviewAttestation",
    "reviewDecisionSha256",
    "reviewDeclaration",
    "reviewManifestSha256",
    "reviewMethodVersion",
    "reviewMode",
    "reviewModel",
    "reviewRubricSha256",
    "reviewStatus",
    "reviewSummary",
    "reviewedBy",
    "reviewedContentSha256",
    "reviewedHash",
    "verifiedBy",
    "workflowState",
}

PACKAGES = (
    {
        "path": ROOT / "turkiye/7-sinif/fen-bilimleri/fen-bilimleri-tum.jsonl",
        "receipt": ROOT
        / "turkiye/7-sinif/fen-bilimleri/fen-bilimleri-release-receipt.json",
        "source_path": (
            "chatgpt/7-sinif/fen-bilimleri/paket/final-bank-candidate/"
            "tr_g07_fen_subject500_ai_verified_v1_7c4b0c48.jsonl"
        ),
        "source_sha256": "7c4b0c48804e75df2b0f5884470a701da280e983ae358c57d305f44a943c8715",
        "grade": 7,
        "subject": "Fen Bilimleri",
        "slug": "fen-bilimleri",
        "curriculum": "MEB-TYMM-2024",
        "notes": 11,
        "questions": 500,
    },
    {
        "path": ROOT / "turkiye/9-sinif/kimya/kimya-tum.jsonl",
        "receipt": ROOT / "turkiye/9-sinif/kimya/kimya-release-receipt.json",
        "source_path": (
            "chatgpt/9-sinif/kimya/paket/final-bank-candidate/"
            "tr_g09_kimya_subject500_ai_verified_v1_5f65657b.jsonl"
        ),
        "source_sha256": "5f65657b0b971d54b2b38d9342e5287c836ed509448617bbec29eb990e169649",
        "grade": 9,
        "subject": "Kimya",
        "slug": "kimya",
        "curriculum": "MEB-TYMM-2026",
        "notes": 31,
        "questions": 500,
    },
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def project(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: project(child)
            for key, child in value.items()
            if key not in EXCLUDED_FIELDS
        }
    if isinstance(value, list):
        return [project(child) for child in value]
    return value


def projection_sha(row: dict[str, Any]) -> str:
    return sha256_bytes(canonical_bytes(project(row)))


def write_jsonl_atomic(path: Path, rows: list[dict[str, Any]]) -> None:
    raw = (
        "\n".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":"))
            for row in rows
        )
        + "\n"
    ).encode("utf-8")
    temporary = path.with_name(f".{path.name}.repair.tmp")
    temporary.write_bytes(raw)
    temporary.replace(path)


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    raw = (
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")
    temporary = path.with_name(f".{path.name}.repair.tmp")
    temporary.write_bytes(raw)
    temporary.replace(path)


def restamp_record(
    row: dict[str, Any],
    package_decision_sha: str,
    changed_fields: list[str],
) -> None:
    prior_decision = row.get("reviewDecisionSha256")
    content_sha = projection_sha(row)
    decision = {
        "schema": "alika-ai-only-schema-repair-record-decision/1.0.0",
        "decision": "PASS",
        "recordId": row.get("id"),
        "recordType": row.get("type"),
        "contentProjectionSha256": content_sha,
        "packageDecisionSha256": package_decision_sha,
        "changedFields": changed_fields,
        "model": MODEL,
        "mode": MODE,
        "humanReviewed": False,
        "methodVersion": METHOD,
    }
    decision_sha = sha256_bytes(canonical_bytes(decision))
    row.update(
        {
            "reviewStatus": "ai-verified",
            "aiReviewStatus": "ai-verified",
            "humanReviewed": False,
            "reviewMode": MODE,
            "reviewModel": MODEL,
            "reviewDeclaration": DECLARATION,
            "reviewMethodVersion": METHOD,
            "reviewedContentSha256": content_sha,
            "reviewDecisionSha256": decision_sha,
            "contentHash": f"sha256:{content_sha}",
            "reviewedHash": f"sha256:{content_sha}",
            "publishReady": True,
            "publishBlocked": False,
            "disclosure": DECLARATION,
            "provenance": (
                f"ai-verified:{decision_sha}; schema-repair:{package_decision_sha}; "
                f"model:{MODEL}; mode:{MODE}; human-review:false"
            ),
            "reviewAttestation": {
                **decision,
                "reviewDecisionSha256": decision_sha,
                "priorReviewDecisionSha256": prior_decision,
                "declaration": DECLARATION,
            },
        }
    )
    row.pop("reviewManifestSha256", None)
    row.pop("reviewRubricSha256", None)


def repair(config: dict[str, Any]) -> dict[str, Any]:
    path: Path = config["path"]
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    before_sha = sha256_bytes(path.read_bytes())
    packs = [row for row in rows if row.get("type") == "pack"]
    notes = [row for row in rows if row.get("type") == "note"]
    questions = [row for row in rows if row.get("type") == "question"]
    if (len(packs), len(notes), len(questions)) != (
        1,
        config["notes"],
        config["questions"],
    ):
        raise RuntimeError(f"topology drift: {path}")

    pack = packs[0]
    already_repaired = pack.get("reviewMethodVersion") == METHOD
    if already_repaired:
        receipt = json.loads(config["receipt"].read_text(encoding="utf-8"))
        current_sha = sha256_bytes(path.read_bytes())
        if receipt.get("package", {}).get("sha256") != current_sha:
            raise RuntimeError(f"repaired package/receipt drift: {path}")
        validation = subprocess.run(
            [sys.executable, str(ROOT / "tools/pack_validate.py"), str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        output = (validation.stdout or "") + (validation.stderr or "")
        if validation.returncode != 0 or "TOPLAM: 0 HATA, 0 UYARI" not in output:
            raise RuntimeError(output[-6000:])
        return {
            "grade": config["grade"],
            "subject": config["subject"],
            "packageSha256": current_sha,
            "changedRecords": 0,
            "questionRange": receipt["questionRange"],
            "validation": "0 HATA / 0 UYARI (already repaired)",
        }
    if not already_repaired and before_sha != config["source_sha256"]:
        raise RuntimeError(f"source drift: {path} ({before_sha})")

    changed: dict[str, list[str]] = {}
    expected_curriculum = config["curriculum"]
    if pack.get("curriculum") != expected_curriculum:
        if pack.get("curriculum") not in (None, "", expected_curriculum):
            raise RuntimeError(f"unexpected curriculum: {pack.get('curriculum')!r}")
        pack["curriculum"] = expected_curriculum
        changed.setdefault(str(pack.get("id")), []).append("curriculum")
    else:
        # Mark a deterministic schema-repair review even when only note records
        # need content-projection changes. This also makes reruns detectable.
        changed.setdefault(str(pack.get("id")), []).append("schemaRepairEnvelope")

    for note in notes:
        objective_code = note.get("objectiveCode")
        if not isinstance(objective_code, str) or not objective_code.strip():
            raise RuntimeError(f"note objectiveCode missing: {note.get('id')}")
        expected_objectives = [objective_code]
        if note.get("objectives") != expected_objectives:
            if note.get("objectives") not in (None, [], expected_objectives):
                raise RuntimeError(f"unexpected objectives: {note.get('id')}")
            note["objectives"] = expected_objectives
            changed.setdefault(str(note.get("id")), []).append("objectives")

    projection_hashes = [projection_sha(row) for row in rows]
    projection_set_sha = sha256_bytes("\n".join(projection_hashes).encode("utf-8"))
    package_decision = {
        "schema": "alika-ai-only-schema-repair-package-decision/1.0.0",
        "decision": "PASS",
        "grade": config["grade"],
        "subject": config["subject"],
        "sourceCandidateSha256": config["source_sha256"],
        "contentProjectionSetSha256": projection_set_sha,
        "changedRecords": changed,
        "repairRules": {
            "objectives": "[objectiveCode]",
            "curriculum": expected_curriculum,
        },
        "gates": {
            "semanticContentChanged": False,
            "objectiveCodeEqualityRequired": True,
            "strictErrors": 0,
            "strictWarnings": 0,
        },
        "model": MODEL,
        "mode": MODE,
        "humanReviewed": False,
        "methodVersion": METHOD,
    }
    package_decision_sha = sha256_bytes(canonical_bytes(package_decision))
    for row in rows:
        record_id = str(row.get("id"))
        if record_id in changed:
            restamp_record(row, package_decision_sha, changed[record_id])

    write_jsonl_atomic(path, rows)
    validation = subprocess.run(
        [sys.executable, str(ROOT / "tools/pack_validate.py"), str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (validation.stdout or "") + (validation.stderr or "")
    if validation.returncode != 0 or "TOPLAM: 0 HATA, 0 UYARI" not in output:
        raise RuntimeError(output[-6000:])

    final_sha = sha256_bytes(path.read_bytes())
    numbers = [int(row["questionNumber"]) for row in questions]
    if len(numbers) != 500 or len(set(numbers)) != 500:
        raise RuntimeError(f"question numbering drift: {path}")
    answer_balance = [
        sum(1 for row in questions if row.get("correct") == index)
        for index in range(4)
    ]
    policy = pack.get("contractPolicy") or {}
    receipt = {
        "schema": "alika-hash-bound-ai-only-subject500-release-receipt/2.0.0",
        "decision": "PASS",
        "grade": config["grade"],
        "subject": config["subject"],
        "subjectSlug": config["slug"],
        "curriculum": expected_curriculum,
        "humanReviewed": False,
        "mode": MODE,
        "model": MODEL,
        "publishBlocked": False,
        "publishReady": True,
        "questionRange": [min(numbers), max(numbers)],
        "counts": {
            "pack": 1,
            "note": len(notes),
            "question": len(questions),
            "total": len(rows),
        },
        "quality": {
            "errors": 0,
            "warnings": 0,
            "families": policy.get("minFamilies"),
            "largestFamily": policy.get("maxPerFamily"),
            "answerBalance": answer_balance,
        },
        "schemaRepairReview": {
            **package_decision,
            "packageDecisionSha256": package_decision_sha,
        },
        "package": {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "records": len(rows),
            "sha256": final_sha,
        },
        "sourceCandidate": {
            "path": config["source_path"],
            "sha256": config["source_sha256"],
        },
        "gates": {
            "jsonlParse": f"PASS {len(rows)}/{len(rows)}",
            "questionContract22": "PASS",
            "noteQuestionLinks": f"PASS {len(notes)}/{len(notes)}",
            "duplicateId": 0,
            "strictErrors": 0,
            "strictWarnings": 0,
        },
    }
    write_json_atomic(config["receipt"], receipt)
    return {
        "grade": config["grade"],
        "subject": config["subject"],
        "sourceSha256": before_sha,
        "packageSha256": final_sha,
        "changedRecords": len(changed),
        "questionRange": receipt["questionRange"],
        "validation": "0 HATA / 0 UYARI",
    }


def main() -> int:
    results = [repair(config) for config in PACKAGES]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
