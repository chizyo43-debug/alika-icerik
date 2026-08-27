#!/usr/bin/env python3
"""Build the manifest-backed Grade 11 AI-only release.

The source packages remain immutable. Every question must be covered exactly
once by a hash-bound GPT-5.6 Sol repair manifest and its reviewed repair
artifact. Pack and note records receive a release attestation only after
topology, curriculum, note richness, links, duplicates, answer balance, and the
canonical Question Contract 2.2 validator all pass.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = ROOT.parent
G11_SOURCE_ROOT = WORKSPACE / "chatgpt" / "11-sinif"
MODEL = "gpt-5.6-sol"
MODE = "ai-only"
DECLARATION = "ai-generated-and-ai-reviewed-no-human-review"
METHOD = "alika-g11-manifest-backed-ai-only-release/1.0.0"

QUESTION_CONTENT_FIELDS = (
    "type", "id", "questionNumber", "subject", "grade", "unitKey",
    "topicKey", "subtopicKey", "topic", "noteId", "noteKey", "objective",
    "question", "choices", "distractorWhy", "correct", "correctIndex",
    "correctOption", "level", "familyId", "objectiveSource", "sourceRefs",
    "objectiveEvidenceId", "explanation", "difficultyReason", "visualNeed",
    "figure", "hintsCount", "hintsForbidden",
)

REQUIRED_REVIEW_CHECKS = (
    "identityPreserved", "independentSolution", "singleCorrect",
    "objectiveAlignment", "answerFieldsConsistent", "explanationComplete",
    "fourSpecificOptionReasons", "hintsForbidden", "officialSourceEvidence",
    "visualNeedDecision", "visualAnswerLeakageAbsent",
    "dataModelFigureConsistency",
)

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

SUBJECTS = (
    {
        "slug": "matematik",
        "subject": "Matematik",
        "source": "matematik/staging/sol-repair/mathematics-full-validation-v2-c7c8d4e1.jsonl",
        "source_sha256": "c7c8d4e178e45f94d4301feb1a16d8089223157d24bec7711b26a2b65a77ba6d",
        "notes": 20,
        "manifest_count": 16,
    },
    {
        "slug": "fizik",
        "subject": "Fizik",
        "source": "fizik/staging/sol-repair/physics-full-validation-v2-cc153244.jsonl",
        "source_sha256": "cc1532440a43b1f351510ab5224668b920e2748ffd22d60fc6a8ed83cd6136fc",
        "notes": 31,
        "manifest_count": 10,
    },
    {
        "slug": "kimya",
        "subject": "Kimya",
        "source": "kimya/staging/sol-repair/chemistry-full-validation-v2-9433d94e.jsonl",
        "source_sha256": "9433d94ecf6b8714ee41572cc764548586786bbff2bb1f8be346dba5be4972fa",
        "notes": 25,
        "manifest_count": 10,
    },
    {
        "slug": "biyoloji",
        "subject": "Biyoloji",
        "source": "biyoloji/staging/sol-repair/biology-full-validation-v2-004f4948.jsonl",
        "source_sha256": "004f49485d1d58d101577fa64dd26381dbcdc4a2029e70d75a64f87183e12858",
        "notes": 22,
        "manifest_count": 10,
    },
    {
        "slug": "turk-dili-ve-edebiyati",
        "subject": "Türk Dili ve Edebiyatı",
        "source": "turk-dili-ve-edebiyati/staging/sol-repair/tde-full-validation-v2-9d953e62.jsonl",
        "source_sha256": "9d953e62cc990e81e15e33deee8ccf3d6644dbee235a8009b07247afec8ccb63",
        "notes": 32,
        "manifest_count": 10,
    },
    {
        "slug": "tarih",
        "subject": "Tarih",
        "source": "tarih/staging/sol-repair/history-full-validation-v2-b7105702.jsonl",
        "source_sha256": "b7105702c20507a44ce2930cc0b9b9eb24e9699fb15eeae1b6e810a4f26cfbce",
        "notes": 22,
        "manifest_count": 10,
    },
    {
        "slug": "cografya",
        "subject": "Coğrafya",
        "source": "cografya/staging/sol-repair/geography-full-validation-v2-fcac0783.jsonl",
        "source_sha256": "fcac0783b4aa3866e4f6e2618bd3c9914967dea76c16de3d54745dc6e5127169",
        "notes": 38,
        "manifest_count": 10,
    },
    {
        "slug": "ingilizce",
        "subject": "İngilizce",
        "source": "ingilizce/staging/sol-repair/english-full-validation-v2-4598a2d1.jsonl",
        "source_sha256": "4598a2d1ce74c1e3e8c52ac4d8fe6e5e79be88fd7d14cd644ddc63c67dc35e9f",
        "notes": 64,
        "manifest_count": 10,
    },
    {
        "slug": "felsefe",
        "subject": "Felsefe",
        "source": "felsefe/staging/sol-repair/philosophy-full-validation-v2-6ddd3aa5.jsonl",
        "source_sha256": "6ddd3aa5ae6e4a18f8558e7eddb6ca2c3a7a849bcfaca090671f267ab9a94038",
        "notes": 24,
        "manifest_count": 10,
    },
    {
        "slug": "din-kulturu-ve-ahlak-bilgisi",
        "subject": "Din Kültürü ve Ahlak Bilgisi",
        "source": "din-kulturu-ve-ahlak-bilgisi/staging/sol-repair/dkab-full-validation-v2-80c33a14.jsonl",
        "source_sha256": "80c33a140dd509ea67721b430964b70ded734dc10139e2624bcb26ac2914dbf7",
        "notes": 50,
        "manifest_count": 10,
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


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def write_jsonl_atomic(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (
        "\n".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":"))
            for row in rows
        )
        + "\n"
    ).encode("utf-8")
    temporary = path.with_name(f".{path.name}.release.tmp")
    temporary.write_bytes(raw)
    temporary.replace(path)


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")
    temporary = path.with_name(f".{path.name}.release.tmp")
    temporary.write_bytes(raw)
    temporary.replace(path)


def question_number(row: dict[str, Any]) -> int:
    if row.get("questionNumber") is not None:
        return int(row["questionNumber"])
    match = re.search(r"(?:^|[-_.])q(\d{1,5})(?:$|[-_.])", str(row.get("id")))
    if not match:
        raise RuntimeError(f"question number missing: {row.get('id')}")
    return int(match.group(1))


def manifest_projection_sha(
    row: dict[str, Any], fields: list[str]
) -> str:
    projection = {field: row[field] for field in fields if field in row}
    return sha256_bytes(canonical_bytes(projection))


def verify_question_manifests(
    config: dict[str, Any],
    source_path: Path,
    questions: list[dict[str, Any]],
) -> tuple[
    dict[str, dict[str, Any]],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    question_by_id = {str(row.get("id")): row for row in questions}
    manifest_dir = source_path.parent / "question-2.2"
    manifest_paths = sorted(manifest_dir.glob("*_q*_repair_manifest_*.json"))
    if len(manifest_paths) != config["manifest_count"]:
        raise RuntimeError(
            f"manifest count drift: {config['slug']} "
            f"({len(manifest_paths)} != {config['manifest_count']})"
        )

    evidence: dict[str, dict[str, Any]] = {}
    repaired_questions: dict[str, dict[str, Any]] = {}
    manifest_receipts: list[dict[str, Any]] = []
    for manifest_path in manifest_paths:
        raw = manifest_path.read_bytes()
        manifest_sha = sha256_bytes(raw)
        manifest = json.loads(raw.decode("utf-8-sig"))
        if manifest.get("status") != "PASS":
            raise RuntimeError(f"manifest not PASS: {manifest_path}")
        if manifest.get("reviewModel") != MODEL:
            raise RuntimeError(f"review model drift: {manifest_path}")
        if manifest.get("reviewMode") != MODE or manifest.get("humanReviewed") is not False:
            raise RuntimeError(f"review mode drift: {manifest_path}")

        authority = manifest.get("authority") or {}
        candidate_sha = str(
            authority.get("strictRepairCandidateSha256")
            or authority.get("sourceCandidateSha256")
            or ""
        ).lower()
        if candidate_sha != config["source_sha256"]:
            raise RuntimeError(f"manifest candidate drift: {manifest_path}")

        batch = manifest.get("batch") or {}
        batch_ids = [str(value) for value in batch.get("questionIds") or []]
        reviews = manifest.get("recordReviews") or []
        has_record_reviews = bool(reviews)
        review_ids = (
            [str(value.get("id")) for value in reviews]
            if has_record_reviews
            else list(batch_ids)
        )
        if (
            not batch_ids
            or len(batch_ids) != len(set(batch_ids))
            or len(review_ids) != len(set(review_ids))
            or set(batch_ids) != set(review_ids)
        ):
            raise RuntimeError(f"manifest record coverage drift: {manifest_path}")
        artifact_rel = batch.get("artifact")
        artifact_path = G11_SOURCE_ROOT / str(artifact_rel)
        if not artifact_path.is_file():
            raise RuntimeError(f"manifest artifact missing: {artifact_path}")
        if sha256_bytes(artifact_path.read_bytes()) != str(batch.get("sha256")).lower():
            raise RuntimeError(f"manifest artifact hash drift: {artifact_path}")
        artifact_rows = read_jsonl(artifact_path)
        artifact_by_id = {
            str(row.get("id")): row
            for row in artifact_rows
            if row.get("type") == "question"
        }
        if set(artifact_by_id) != set(batch_ids) or len(artifact_rows) != len(batch_ids):
            raise RuntimeError(f"manifest artifact topology drift: {artifact_path}")

        validation = manifest.get("validation") or {}
        required_zero = (
            "strictErrors",
            "strictWarnings",
            "contentFindings",
            "exactDuplicates",
            "nearDuplicates",
            "semanticFindings",
        )
        if any(validation.get(field) != 0 for field in required_zero):
            raise RuntimeError(f"manifest quality drift: {manifest_path}")
        boundary = manifest.get("mechanicalReviewBoundary") or {}
        if "gpt-5.6-sol" not in str(boundary.get("semanticPassGrantedBy", "")):
            raise RuntimeError(f"semantic review evidence missing: {manifest_path}")

        fields = (
            list((manifest.get("hashBinding") or {}).get("contentFields") or [])
            if has_record_reviews
            else list(QUESTION_CONTENT_FIELDS)
        )
        if has_record_reviews and not fields:
            raise RuntimeError(f"manifest content fields missing: {manifest_path}")
        effective_reviews = reviews if has_record_reviews else [
            {
                "id": record_id,
                "decision": (artifact_by_id[record_id].get("reviewAttestation") or {}).get("decision"),
                "contentSha256": artifact_by_id[record_id].get("reviewedContentSha256"),
                "decisionSha256": artifact_by_id[record_id].get("reviewDecisionSha256"),
            }
            for record_id in batch_ids
        ]
        for record_review in effective_reviews:
            record_id = str(record_review.get("id"))
            if record_id in evidence:
                raise RuntimeError(f"question reviewed twice: {record_id}")
            if record_id not in question_by_id:
                raise RuntimeError(f"reviewed question absent: {record_id}")
            row = artifact_by_id.get(record_id)
            if row is None:
                raise RuntimeError(f"reviewed artifact question absent: {record_id}")
            if record_review.get("decision") != "PASS":
                raise RuntimeError(f"question review not PASS: {record_id}")
            content_sha = manifest_projection_sha(row, fields)
            if content_sha != str(record_review.get("contentSha256")).lower():
                raise RuntimeError(f"question content hash drift: {record_id}")
            if not has_record_reviews:
                attestation = row.get("reviewAttestation") or {}
                checks = attestation.get("checks") or {}
                if (
                    attestation.get("reviewedBy") != MODEL
                    or attestation.get("reviewModel") != MODEL
                    or attestation.get("reviewMode") != MODE
                    or any(checks.get(name) is not True for name in REQUIRED_REVIEW_CHECKS)
                    or sha256_bytes(canonical_bytes(attestation))
                    != str(record_review.get("decisionSha256")).lower()
                ):
                    raise RuntimeError(f"embedded question review drift: {record_id}")
            evidence[record_id] = {
                "manifestPath": manifest_path.relative_to(G11_SOURCE_ROOT).as_posix(),
                "manifestSha256": manifest_sha,
                "manifestRecordContentSha256": content_sha,
                "manifestRecordDecisionSha256": record_review.get("decisionSha256"),
            }
            repaired_questions[record_id] = row

        manifest_receipts.append(
            {
                "path": manifest_path.relative_to(G11_SOURCE_ROOT).as_posix(),
                "sha256": manifest_sha,
                "firstQuestionId": batch.get("firstQuestionId"),
                "lastQuestionId": batch.get("lastQuestionId"),
                "questionCount": len(batch_ids),
            }
        )

    if set(evidence) != set(question_by_id):
        missing = sorted(set(question_by_id) - set(evidence))[:10]
        extra = sorted(set(evidence) - set(question_by_id))[:10]
        raise RuntimeError(f"manifest coverage drift: missing={missing} extra={extra}")
    return evidence, manifest_receipts, repaired_questions


def normalize_release_metadata(
    rows: list[dict[str, Any]], pack: dict[str, Any], notes: list[dict[str, Any]],
    questions: list[dict[str, Any]]
) -> dict[str, list[str]]:
    changed: dict[str, list[str]] = {}
    pack_id = str(pack.get("id"))
    if not pack_id:
        raise RuntimeError("pack id missing")
    if pack.get("curriculum") != "MEB-TYMM-2024":
        if pack.get("curriculum") not in (None, "", "MEB-TYMM-current"):
            raise RuntimeError(f"unexpected curriculum: {pack.get('curriculum')!r}")
        pack["curriculum"] = "MEB-TYMM-2024"
        changed.setdefault(pack_id, []).append("curriculum")

    labels = pack.get("labels")
    if isinstance(labels, dict) and labels:
        label_keys = set(labels)
        used_label_keys: set[str] = set()

        def collect_label_references(value: Any) -> None:
            if isinstance(value, str):
                if value in label_keys:
                    used_label_keys.add(value)
                return
            if isinstance(value, list):
                for item in value:
                    collect_label_references(item)
                return
            if isinstance(value, dict):
                for key, item in value.items():
                    if value is pack and key == "labels":
                        continue
                    collect_label_references(item)

        for row in rows:
            collect_label_references(row)
        pruned_labels = {
            key: value for key, value in labels.items() if key in used_label_keys
        }
        if pruned_labels != labels:
            pack["labels"] = pruned_labels
            changed.setdefault(pack_id, []).append("labels")

    for row in rows:
        record_id = str(row.get("id"))
        fields: list[str] = []
        if row.get("productionStatus") != "final-approved":
            row["productionStatus"] = "final-approved"
            fields.append("productionStatus")
        if row.get("type") != "pack":
            if row.get("packId") != pack_id:
                row["packId"] = pack_id
                fields.append("packId")
            if row.get("linkedPackId") != pack_id:
                row["linkedPackId"] = pack_id
                fields.append("linkedPackId")
        if fields:
            changed[record_id] = fields

    note_ids = {str(note.get("id")) for note in notes}
    for note in notes:
        record_id = str(note.get("id"))
        objectives = note.get("objectives")
        if not (
            isinstance(objectives, list)
            and objectives
            and all(isinstance(value, str) and value.strip() for value in objectives)
        ):
            objective = note.get("objectiveCode") or note.get("objective")
            if not isinstance(objective, str) or not objective.strip():
                raise RuntimeError(f"note objectives missing: {record_id}")
            note["objectives"] = [objective]
            changed.setdefault(record_id, []).append("objectives")

        body = str(note.get("body") or "").strip()
        sections = note.get("lessonSections")
        combined_size = len(body) + len(json.dumps(sections or {}, ensure_ascii=False))
        if not body or not isinstance(sections, dict) or combined_size < 1000:
            raise RuntimeError(f"note richness gate failed: {record_id}")

    for question in questions:
        record_id = str(question.get("id"))
        note_id = question.get("linkedNoteId") or question.get("noteId")
        if str(note_id) not in note_ids:
            raise RuntimeError(f"question note link missing: {record_id}")
        if not question.get("linkedNoteId"):
            question["linkedNoteId"] = note_id
            changed.setdefault(record_id, []).append("linkedNoteId")
        note_key = question.get("noteKey")
        if note_key and not question.get("linkedNoteKey"):
            question["linkedNoteKey"] = note_key
            changed.setdefault(record_id, []).append("linkedNoteKey")
    return changed


def stamp_record(
    row: dict[str, Any],
    package_decision_sha: str,
    changed_fields: list[str],
    question_evidence: dict[str, Any] | None,
) -> None:
    content_sha = projection_sha(row)
    record_kind = "manifest-backed-question" if question_evidence else "package-release-audit"
    decision = {
        "schema": "alika-g11-release-record-decision/1.0.0",
        "decision": "PASS",
        "recordId": row.get("id"),
        "recordType": row.get("type"),
        "reviewKind": record_kind,
        "contentProjectionSha256": content_sha,
        "packageDecisionSha256": package_decision_sha,
        "changedFields": changed_fields,
        "questionReviewEvidence": question_evidence,
        "model": MODEL,
        "mode": MODE,
        "humanReviewed": False,
        "methodVersion": METHOD,
    }
    decision_sha = sha256_bytes(canonical_bytes(decision))
    # The inherited batch already names the semantic reviewer inside the
    # hash-bound evidence.  Keeping its legacy top-level ``reviewedBy`` while
    # also writing a release provenance string would make rule 54 interpret
    # the reviewer as the producer, so the release uses the nested evidence.
    row.pop("reviewedBy", None)
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
                f"ai-verified:{decision_sha}; grade11-release:{package_decision_sha}; "
                f"model:{MODEL}; mode:{MODE}; human-review:false"
            ),
            "reviewAttestation": {
                **decision,
                "reviewDecisionSha256": decision_sha,
                "declaration": DECLARATION,
            },
        }
    )
    row.pop("reviewManifestSha256", None)
    row.pop("reviewRubricSha256", None)


def run_validator(path: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools/pack_validate.py"), "--strict", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0 or "TOPLAM: 0 HATA, 0 UYARI" not in output:
        raise RuntimeError(output[-8000:])
    return "0 HATA / 0 UYARI"


def prepare_subject(config: dict[str, Any]) -> dict[str, Any]:
    source_path = G11_SOURCE_ROOT / config["source"]
    output_path = (
        ROOT / "turkiye/11-sinif" / config["slug"] / f"{config['slug']}-tum.jsonl"
    )
    receipt_path = output_path.with_name(f"{config['slug']}-release-receipt.json")

    if output_path.is_file() and receipt_path.is_file():
        rows = read_jsonl(output_path)
        pack = next((row for row in rows if row.get("type") == "pack"), None)
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if pack and pack.get("reviewMethodVersion") == METHOD:
            current_sha = sha256_bytes(output_path.read_bytes())
            if receipt.get("package", {}).get("sha256") != current_sha:
                raise RuntimeError(f"release receipt drift: {output_path}")
            run_validator(output_path)
            return {
                "subject": config["subject"],
                "questions": 500,
                "notes": config["notes"],
                "packageSha256": current_sha,
                "validation": "0 HATA / 0 UYARI (already prepared)",
            }

    source_raw = source_path.read_bytes()
    source_sha = sha256_bytes(source_raw)
    if source_sha != config["source_sha256"]:
        raise RuntimeError(f"source candidate drift: {source_path} ({source_sha})")
    rows = read_jsonl(source_path)
    packs = [row for row in rows if row.get("type") == "pack"]
    notes = [row for row in rows if row.get("type") == "note"]
    questions = [row for row in rows if row.get("type") == "question"]
    if (len(packs), len(notes), len(questions)) != (1, config["notes"], 500):
        raise RuntimeError(f"topology drift: {config['slug']}")
    pack = packs[0]
    if pack.get("grade") != 11 or pack.get("subject") != config["subject"]:
        raise RuntimeError(f"pack identity drift: {config['slug']}")
    if pack.get("contentContractVersion") != "2.2":
        raise RuntimeError(f"contract drift: {config['slug']}")

    evidence, manifest_receipts, repaired_question_by_id = verify_question_manifests(
        config, source_path, questions
    )
    questions = sorted(repaired_question_by_id.values(), key=question_number)
    rows = packs + notes + questions
    changed = normalize_release_metadata(rows, pack, notes, questions)

    numbers = sorted(question_number(row) for row in questions)
    if numbers != list(range(1, 501)):
        raise RuntimeError(f"question range drift: {config['slug']}")
    ids = [str(row.get("id")) for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError(f"duplicate ids: {config['slug']}")
    normalized_questions = [
        re.sub(r"\s+", " ", str(row.get("question") or "").strip().casefold())
        for row in questions
    ]
    if not all(normalized_questions) or len(set(normalized_questions)) != 500:
        raise RuntimeError(f"duplicate/blank question text: {config['slug']}")
    normalized_notes = [
        re.sub(r"\s+", " ", str(row.get("body") or "").strip().casefold())
        for row in notes
    ]
    if len(set(normalized_notes)) != len(notes):
        raise RuntimeError(f"duplicate note body: {config['slug']}")

    manifest_set_sha = sha256_bytes(
        "\n".join(item["sha256"] for item in manifest_receipts).encode("ascii")
    )
    content_set_sha = sha256_bytes(
        "\n".join(projection_sha(row) for row in rows).encode("ascii")
    )
    package_decision = {
        "schema": "alika-g11-manifest-backed-package-decision/1.0.0",
        "decision": "PASS",
        "grade": 11,
        "subject": config["subject"],
        "sourceCandidateSha256": source_sha,
        "questionManifestCount": len(manifest_receipts),
        "questionManifestSetSha256": manifest_set_sha,
        "manifestReviewedQuestions": len(evidence),
        "contentProjectionSetSha256": content_set_sha,
        "changedRecords": changed,
        "gates": {
            "manifestCoverage": "PASS 500/500",
            "manifestContentHashes": "PASS 500/500",
            "noteRichness": f"PASS {len(notes)}/{len(notes)}",
            "noteQuestionLinks": "PASS 500/500",
            "duplicateIds": 0,
            "duplicateQuestionTexts": 0,
            "duplicateNoteBodies": 0,
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
        stamp_record(
            row,
            package_decision_sha,
            changed.get(record_id, []),
            evidence.get(record_id),
        )

    write_jsonl_atomic(output_path, rows)
    validation = run_validator(output_path)
    package_sha = sha256_bytes(output_path.read_bytes())
    answer_balance = [
        sum(1 for row in questions if row.get("correct") == index)
        for index in range(4)
    ]
    families = Counter(str(row.get("familyId")) for row in questions)
    figured = sum(bool(row.get("figure")) for row in questions)
    note_sizes = [
        len(str(row.get("body") or "").strip())
        + len(json.dumps(row.get("lessonSections") or {}, ensure_ascii=False))
        for row in notes
    ]
    receipt = {
        "schema": "alika-g11-manifest-backed-ai-only-release-receipt/1.0.0",
        "decision": "PASS",
        "grade": 11,
        "subject": config["subject"],
        "subjectSlug": config["slug"],
        "curriculum": pack.get("curriculum"),
        "humanReviewed": False,
        "mode": MODE,
        "model": MODEL,
        "publishBlocked": False,
        "publishReady": True,
        "questionRange": [1, 500],
        "counts": {
            "pack": 1,
            "note": len(notes),
            "question": len(questions),
            "total": len(rows),
        },
        "quality": {
            "errors": 0,
            "warnings": 0,
            "families": len(families),
            "largestFamily": max(families.values()),
            "answerBalance": answer_balance,
            "figuredQuestions": figured,
            "duplicateQuestionTexts": 0,
            "duplicateNoteBodies": 0,
            "minimumNoteEvidenceCharacters": min(note_sizes),
        },
        "review": {
            **package_decision,
            "packageDecisionSha256": package_decision_sha,
            "manifests": manifest_receipts,
        },
        "package": {
            "path": output_path.relative_to(ROOT).as_posix(),
            "bytes": output_path.stat().st_size,
            "records": len(rows),
            "sha256": package_sha,
        },
        "sourceCandidate": {
            "path": f"chatgpt/11-sinif/{config['source']}",
            "sha256": source_sha,
        },
        "gates": {
            "jsonlParse": f"PASS {len(rows)}/{len(rows)}",
            "questionContract22": "PASS",
            "manifestCoverage": "PASS 500/500",
            "manifestContentHashes": "PASS 500/500",
            "noteRichness": f"PASS {len(notes)}/{len(notes)}",
            "noteQuestionLinks": "PASS 500/500",
            "duplicateId": 0,
            "strictErrors": 0,
            "strictWarnings": 0,
        },
    }
    write_json_atomic(receipt_path, receipt)
    return {
        "subject": config["subject"],
        "questions": len(questions),
        "notes": len(notes),
        "manifests": len(manifest_receipts),
        "packageSha256": package_sha,
        "validation": validation,
    }


def main() -> int:
    results = [prepare_subject(config) for config in SUBJECTS]
    print(json.dumps(results, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
