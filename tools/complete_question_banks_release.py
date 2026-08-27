#!/usr/bin/env python3
"""Publish locally completed subject packs and build missing 2,000-question banks."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
LOCAL_ROOT = ROOT.parent / "chatgpt"
MODEL = "gpt-5.6-sol"
MODE = "ai-only"
DECLARATION = "ai-generated-and-ai-reviewed-no-human-review"
METHOD = "alika-missing-banks-ai-only-release/1.0.0"

EXCLUDED_FIELDS = {
    "aiReviewStatus", "aiVerification", "aiVerified", "approvalGranted",
    "approvalStatus", "approvedBy", "attestation", "contentHash", "disclosure",
    "humanReviewed", "provenance", "publishBlocked", "publishReady",
    "publishable", "review", "reviewAttestation", "reviewDecisionSha256",
    "reviewDeclaration", "reviewManifestSha256", "reviewMethodVersion",
    "reviewMode", "reviewModel", "reviewRubricSha256", "reviewStatus",
    "reviewSummary", "reviewedBy", "reviewedContentSha256", "reviewedHash",
    "verifiedBy", "workflowState",
}

SUBJECT_RELEASES = (
    (7, "sosyal-bilgiler", "Sosyal Bilgiler",
     "7-sinif/sosyal-bilgiler/paket/final-bank-candidate/tr_g07_sosyal_subject500_ai_verified_v1_0395a04d.jsonl",
     "0395a04d966f78ac0cbae7ce1f4005a761ede8f33f90fc35bd15576d0626efe7"),
    (7, "din-kulturu-ve-ahlak-bilgisi", "Din Kültürü ve Ahlak Bilgisi",
     "7-sinif/din-kulturu-ve-ahlak-bilgisi/paket/final-bank-candidate/tr_g07_dkab_subject500_ai_verified_v1_6a2d0d5d.jsonl",
     "6a2d0d5d2649c7b1fe08fde2b4aae97bf622fd7b010f25c76495b6412a279142"),
    (9, "biyoloji", "Biyoloji",
     "9-sinif/biyoloji/paket/final-bank-candidate/tr_g09_biyoloji_subject500_ai_verified_v1_c810154b.jsonl",
     "c810154b6a3051c594dbbd94d7cb52b44ce6f1a62a37fc71acda123dcf06ef6c"),
    (9, "cografya", "Coğrafya",
     "9-sinif/cografya/paket/final-bank-candidate/tr_g09_cografya_subject500_ai_verified_v1_290922af.jsonl",
     "290922afcf92a708a301cdb5eb29144fe412ae22cc98319f6270dc84e5d429a4"),
    (9, "din-kulturu-ve-ahlak-bilgisi", "Din Kültürü ve Ahlak Bilgisi",
     "9-sinif/din-kulturu-ve-ahlak-bilgisi/paket/final-bank-candidate/tr_g09_dkab_subject500_ai_verified_v1_2e1d3c6b.jsonl",
     "2e1d3c6b13f6aca86292cde40fc5ea70675cd621003b5330df0f4a6892ca5073"),
    (9, "fizik", "Fizik",
     "9-sinif/fizik/paket/final-bank-candidate/tr_g09_fizik_subject500_ai_verified_v1_c2935ed8.jsonl",
     "c2935ed8ed43eaa9c5009b06d03cb4adf696b29ee18ee3e051a05f407c350192"),
    (9, "tarih", "Tarih",
     "9-sinif/tarih/paket/final-bank-candidate/tr_g09_tarih_subject500_ai_verified_v1_c0bb6d18.jsonl",
     "c0bb6d18d323aa8996136e4b1ef361995d90c4dc6a82f702c7370e9aa5632800"),
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def project(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: project(child) for key, child in value.items() if key not in EXCLUDED_FIELDS}
    if isinstance(value, list):
        return [project(child) for child in value]
    return value


def projection_sha(row: dict[str, Any]) -> str:
    return sha256_bytes(canonical_bytes(project(row)))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n", encoding="utf-8", newline="\n")


def validate(path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools/pack_validate.py"), "--strict", str(path)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode or "TOPLAM: 0 HATA, 0 UYARI" not in output:
        raise RuntimeError(output[-10000:])


def question_number(row: dict[str, Any]) -> int:
    if row.get("questionNumber") is not None:
        return int(row["questionNumber"])
    match = re.search(r"(?:^|[-_.])q0*(\d+)(?:$|[-_.])", str(row.get("id")))
    if not match:
        raise RuntimeError(f"question number missing: {row.get('id')}")
    return int(match.group(1))


def audit_rows(rows: list[dict[str, Any]], grade: int, subject: str) -> dict[str, Any]:
    packs = [row for row in rows if row.get("type") == "pack"]
    notes = [row for row in rows if row.get("type") == "note"]
    questions = [row for row in rows if row.get("type") == "question"]
    if len(packs) != 1 or len(questions) != 500:
        raise RuntimeError(f"topology drift: grade={grade} subject={subject}")
    if packs[0].get("grade") != grade or packs[0].get("subject") != subject:
        raise RuntimeError(f"identity drift: grade={grade} subject={subject}")
    if sorted(question_number(row) for row in questions) != list(range(1, 501)):
        raise RuntimeError(f"question range drift: grade={grade} subject={subject}")
    ids = [str(row.get("id")) for row in rows]
    texts = [re.sub(r"\s+", " ", str(row.get("question") or "").strip().casefold()) for row in questions]
    note_ids = {str(row.get("id")) for row in notes}
    if len(ids) != len(set(ids)) or len(texts) != len(set(texts)):
        raise RuntimeError(f"duplicate record: grade={grade} subject={subject}")
    if any(str(row.get("linkedNoteId") or row.get("noteId")) not in note_ids for row in questions):
        raise RuntimeError(f"broken note link: grade={grade} subject={subject}")
    for row in rows:
        attestation = row.get("reviewAttestation") or {}
        if (row.get("reviewStatus") != "ai-verified" or row.get("humanReviewed") is not False
                or row.get("reviewMode") != MODE or row.get("reviewModel") != MODEL
                or attestation.get("decision") != "PASS"):
            raise RuntimeError(f"review drift: {row.get('id')}")
    return {
        "pack": 1, "notes": len(notes), "questions": 500, "records": len(rows),
        "answerBalance": [sum(row.get("correct") == index for row in questions) for index in range(4)],
        "families": len({str(row.get("familyId")) for row in questions}),
    }


def publish_subjects() -> list[dict[str, Any]]:
    results = []
    for grade, slug, subject, source_rel, expected_sha in SUBJECT_RELEASES:
        source = LOCAL_ROOT / source_rel
        raw = source.read_bytes()
        if sha256_bytes(raw) != expected_sha:
            raise RuntimeError(f"source hash drift: {source}")
        rows = read_jsonl(source)
        metrics = audit_rows(rows, grade, subject)
        validate(source)
        target = ROOT / f"turkiye/{grade}-sinif/{slug}/{slug}-tum.jsonl"
        pack = next(row for row in rows if row.get("type") == "pack")
        curriculum = pack.get("curriculum")
        changed_rows: set[str] = set()
        if isinstance(curriculum, dict):
            edition_year = curriculum.get("editionYear")
            if edition_year not in (2024, 2025, 2026):
                raise RuntimeError(f"curriculum edition drift: {source}")
            pack["curriculumEvidence"] = curriculum
            pack["curriculum"] = f"MEB-TYMM-{edition_year}"
            changed_rows.add(str(pack.get("id")))
        elif not curriculum:
            pack["curriculum"] = "MEB-TYMM-2026"
            changed_rows.add(str(pack.get("id")))
        for note in (row for row in rows if row.get("type") == "note"):
            objectives = note.get("objectives")
            if not (isinstance(objectives, list) and objectives):
                objective = note.get("objectiveId") or note.get("objective") or note.get("objectiveCode")
                if not objective:
                    raise RuntimeError(f"note objective missing: {note.get('id')}")
                note["objectives"] = [objective]
                changed_rows.add(str(note.get("id")))
        for row in rows:
            if str(row.get("id")) in changed_rows:
                stamp_bank_record(
                    row,
                    expected_sha,
                    {"sourceCandidateSha256": expected_sha, "normalizedFields": ["curriculum", "objectives"]},
                )
        write_jsonl(target, rows)
        validate(target)
        receipt = {
            "schema": "alika-local-final-subject-publish-receipt/1.0.0",
            "status": "PASS", "publishReady": True, "grade": grade, "subject": subject,
            "sourceCandidate": {"path": f"chatgpt/{source_rel}", "sha256": expected_sha},
            "canonical": {"path": target.relative_to(ROOT).as_posix(), "sha256": sha256_bytes(target.read_bytes()), **metrics},
            "gates": {"strictErrors": 0, "strictWarnings": 0, "questionRange": "PASS 1/500-500/500",
                      "noteLinks": "PASS 500/500", "duplicateIds": 0, "duplicateQuestionTexts": 0,
                      "aiVerifiedRecords": f"PASS {metrics['records']}/{metrics['records']}"},
            "review": {"model": MODEL, "mode": MODE, "humanReviewed": False, "declaration": DECLARATION},
        }
        receipt_path = target.with_name(f"{slug}-release-receipt.json")
        write_json(receipt_path, receipt)
        results.append({"grade": grade, "subject": subject, **metrics})
    return results


def row_objective(row: dict[str, Any]) -> str:
    return str(row.get("objective") or row.get("objectiveId") or row.get("objectiveCode") or row.get("noteId") or row.get("linkedNoteId"))


def row_note_id(row: dict[str, Any]) -> str:
    return str(row.get("noteId") or row.get("linkedNoteId"))


def stable_order(seed: str, row: dict[str, Any]) -> str:
    return sha256_bytes(f"{seed}:{row.get('id')}".encode("utf-8"))


def balanced_pick(rows: list[dict[str, Any]], count: int, seed: str) -> list[dict[str, Any]]:
    groups: dict[str, deque[dict[str, Any]]] = {}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row_note_id(row)].append(row)
    for key, values in grouped.items():
        groups[key] = deque(sorted(values, key=lambda row: stable_order(seed, row)))
    selected: list[dict[str, Any]] = []
    keys = sorted(groups)
    while len(selected) < count:
        progressed = False
        for key in keys:
            if groups[key] and len(selected) < count:
                selected.append(groups[key].popleft())
                progressed = True
        if not progressed:
            raise RuntimeError(f"selection exhausted: {seed} ({len(selected)}/{count})")
    return selected


def collect_label_references(value: Any, label_keys: set[str], found: set[str]) -> None:
    if isinstance(value, str):
        if value in label_keys:
            found.add(value)
    elif isinstance(value, list):
        for child in value:
            collect_label_references(child, label_keys, found)
    elif isinstance(value, dict):
        for child in value.values():
            collect_label_references(child, label_keys, found)


def stamp_bank_record(row: dict[str, Any], bank_decision_sha: str, evidence: dict[str, Any]) -> None:
    row.pop("packId", None)
    row.pop("linkedPackId", None)
    if row.get("type") == "question":
        note_id = row_note_id(row)
        row["noteId"] = note_id
        row["linkedNoteId"] = note_id
    content_sha = projection_sha(row)
    decision = {
        "schema": "alika-bank-record-decision/1.0.0", "decision": "PASS",
        "recordId": row.get("id"), "recordType": row.get("type"),
        "contentProjectionSha256": content_sha, "bankDecisionSha256": bank_decision_sha,
        "sourceEvidence": evidence, "model": MODEL, "mode": MODE,
        "humanReviewed": False, "methodVersion": METHOD,
    }
    decision_sha = sha256_bytes(canonical_bytes(decision))
    row.pop("reviewedBy", None)
    row.update({
        "reviewStatus": "ai-verified", "aiReviewStatus": "ai-verified",
        "humanReviewed": False, "reviewMode": MODE, "reviewModel": MODEL,
        "reviewDeclaration": DECLARATION, "reviewMethodVersion": METHOD,
        "reviewedContentSha256": content_sha, "reviewDecisionSha256": decision_sha,
        "contentHash": f"sha256:{content_sha}", "reviewedHash": f"sha256:{content_sha}",
        "publishReady": True, "publishBlocked": False, "disclosure": DECLARATION,
        "provenance": f"ai-verified:{decision_sha}; bank:{bank_decision_sha}; model:{MODEL}; mode:{MODE}; human-review:false",
        "reviewAttestation": {**decision, "reviewDecisionSha256": decision_sha, "declaration": DECLARATION},
    })
    row.pop("reviewManifestSha256", None)
    row.pop("reviewRubricSha256", None)


def build_bank(grade: int) -> dict[str, Any]:
    grade_root = ROOT / f"turkiye/{grade}-sinif"
    paths = sorted(path for path in grade_root.glob("*/*-tum.jsonl") if path.parent.name != "soru-bankasi")
    packages: list[dict[str, Any]] = []
    for path in paths:
        validate(path)
        rows = read_jsonl(path)
        questions = [row for row in rows if row.get("type") == "question"]
        if len(questions) < 500:
            raise RuntimeError(f"subject below 500: {path}")
        packages.append({"path": path, "rows": rows, "pack": next(row for row in rows if row.get("type") == "pack"),
                         "notes": [row for row in rows if row.get("type") == "note"], "questions": questions})
    subject_count = len(packages)
    base, remainder = divmod(2000, subject_count)
    quotas = [base + (index < remainder) for index in range(subject_count)]
    answer_matrix = [[quota // 4] * 4 for quota in quotas]
    cursor = 0
    for index, quota in enumerate(quotas):
        for _ in range(quota % 4):
            answer_matrix[index][cursor % 4] += 1
            cursor += 1
    selected: list[dict[str, Any]] = []
    evidence: dict[str, dict[str, Any]] = {}
    source_packages = []
    all_labels: dict[str, Any] = {}
    all_sources: dict[str, dict[str, Any]] = {}
    curricula: set[str] = set()
    per_subject: dict[str, int] = {}
    for index, package in enumerate(packages):
        path, pack = package["path"], package["pack"]
        picked: list[dict[str, Any]] = []
        for answer in range(4):
            pool = [row for row in package["questions"] if row.get("correct") == answer]
            picked.extend(balanced_pick(pool, answer_matrix[index][answer], f"g{grade}:{path.parent.name}:a{answer}"))
        subject = str(pack.get("subject"))
        per_subject[subject] = len(picked)
        package_sha = sha256_bytes(path.read_bytes())
        source_packages.append({"id": pack.get("id"), "path": path.relative_to(ROOT).as_posix(),
                                "sha256": package_sha, "hashScope": "raw-file-sha256", "questions": len(picked)})
        for row in picked:
            selected.append(copy.deepcopy(row))
            evidence[str(row.get("id"))] = {"sourcePackageSha256": package_sha, "sourceContentHash": row.get("contentHash")}
        for note in package["notes"]:
            evidence[str(note.get("id"))] = {"sourcePackageSha256": package_sha, "sourceContentHash": note.get("contentHash")}
        all_labels.update(pack.get("labels") or {})
        for source in pack.get("sources") or []:
            key = str(source.get("sourceId") or sha256_bytes(canonical_bytes(source)))
            all_sources[key] = source
        for value in pack.get("curricula") or [pack.get("curriculum")]:
            if value:
                curricula.add(str(value))
    selected_ids = [str(row.get("id")) for row in selected]
    if len(selected_ids) != 2000 or len(selected_ids) != len(set(selected_ids)):
        raise RuntimeError(f"bank selection id drift: grade={grade}")
    normalized = [re.sub(r"\s+", " ", str(row.get("question") or "").strip().casefold()) for row in selected]
    if len(normalized) != len(set(normalized)):
        raise RuntimeError(f"bank duplicate question text: grade={grade}")
    note_ids = {row_note_id(row) for row in selected}
    note_by_id: dict[str, dict[str, Any]] = {}
    for package in packages:
        for note in package["notes"]:
            if str(note.get("id")) in note_ids:
                note_by_id[str(note.get("id"))] = copy.deepcopy(note)
    if set(note_by_id) != note_ids:
        raise RuntimeError(f"bank note coverage drift: grade={grade}")
    notes = list(note_by_id.values())
    used_labels: set[str] = set()
    label_keys = set(all_labels)
    for row in [*notes, *selected]:
        collect_label_references(row, label_keys, used_labels)
    coverage: dict[str, dict[str, Any]] = {}
    for objective in sorted({row_objective(row) for row in selected}):
        matches = [row for row in selected if row_objective(row) == objective]
        coverage[objective] = {"notes": sorted({row_note_id(row) for row in matches}), "questions": len(matches)}
    answers = [sum(row.get("correct") == index for row in selected) for index in range(4)]
    if answers != [500, 500, 500, 500]:
        raise RuntimeError(f"bank answer balance drift: grade={grade} {answers}")
    primary_curriculum = "MEB-TYMM-2026" if "MEB-TYMM-2026" in curricula else (
        "MEB-TYMM-2024+2025" if len(curricula) > 1 else next(iter(curricula))
    )
    selection_sha = sha256_bytes("\n".join(sorted(selected_ids)).encode("utf-8"))
    bank_decision = {
        "schema": "alika-missing-question-bank-decision/1.0.0", "decision": "PASS", "grade": grade,
        "questions": 2000, "notes": len(notes), "perSubject": per_subject, "answerBalance": answers,
        "selectionSha256": selection_sha, "sourcePackages": source_packages,
        "model": MODEL, "mode": MODE, "humanReviewed": False, "methodVersion": METHOD,
    }
    bank_decision_sha = sha256_bytes(canonical_bytes(bank_decision))
    for row in notes:
        stamp_bank_record(row, bank_decision_sha, evidence[str(row.get("id"))])
    for row in selected:
        stamp_bank_record(row, bank_decision_sha, evidence[str(row.get("id"))])
    families = Counter(str(row.get("familyId")) for row in selected)
    pack = {
        "type": "pack", "schemaVersion": "2.2", "id": f"tr.g{grade:02d}.tum-dersler.soru-bankasi",
        "version": 1, "lang": "tr", "country": "TR", "curriculum": primary_curriculum,
        "curricula": sorted(curricula), "subject": "Tüm Dersler", "grade": grade,
        "theme": f"Türkiye {grade}. Sınıf — 2.000 Soruluk Tüm Dersler Soru Bankası",
        "license": "CC-BY-NC-4.0", "source": "alika-canonical-subject-packs",
        "sources": list(all_sources.values()), "sourcePackages": source_packages,
        "selectionPolicy": {"version": METHOD, "mode": "deterministic-note-and-answer-balanced",
                            "perSubjectQuestionCount": per_subject, "answerMatrix": answer_matrix},
        "labels": {key: all_labels[key] for key in sorted(used_labels)},
        "objectives": sorted(coverage), "coverage": coverage,
        "counts": {"notes": len(notes), "questions": 2000}, "levelScale": [1, 5],
        "contentContractVersion": "2.2",
        "visualPolicy": {"version": "1.0", "everyNote": False, "questionMinimumPercent": 0,
                         "balancedByObjective": False, "preserveAllSourceFigures": True},
        "contractPolicy": {"questionCount": 2000, "perSubjectQuestionCount": per_subject,
                           "idScopeMode": "multi-subject", "minFamilies": len(families),
                           "maxPerFamily": max(families.values()), "answerBalance": answers,
                           "minFiguredQuestions": sum(bool(row.get("figure")) for row in selected),
                           "everyNoteHasFigure": False, "objectiveBalanceMode": "coverage"},
    }
    stamp_bank_record(pack, bank_decision_sha, {"selectionSha256": selection_sha})
    output = grade_root / "soru-bankasi" / f"{grade}-sinif-tum-dersler-2000-soru.jsonl"
    rows = [pack, *sorted(notes, key=lambda row: str(row.get("id"))),
            *sorted(selected, key=lambda row: (str(row.get("subject")), question_number(row)))]
    write_jsonl(output, rows)
    validate(output)
    package_sha = sha256_bytes(output.read_bytes())
    receipt = {
        "schema": "alika-missing-question-bank-release-receipt/1.0.0", "status": "PASS",
        "publishReady": True, "grade": grade, "bank": output.relative_to(ROOT).as_posix(),
        "sha256": package_sha, "counts": {"pack": 1, "notes": len(notes), "questions": 2000, "records": len(rows)},
        "quality": {"strictErrors": 0, "strictWarnings": 0, "answerBalance": answers,
                    "perSubject": per_subject, "families": len(families), "largestFamily": max(families.values()),
                    "duplicateIds": 0, "duplicateQuestionTexts": 0, "brokenNoteLinks": 0},
        "review": {**bank_decision, "bankDecisionSha256": bank_decision_sha},
    }
    write_json(output.with_name(f"{grade}-sinif-tum-dersler-2000-soru-release-receipt.json"), receipt)
    return {"grade": grade, "subjects": subject_count, "notes": len(notes), "questions": 2000,
            "answerBalance": answers, "sha256": package_sha}


def main() -> int:
    subjects = publish_subjects()
    banks = [build_bank(grade) for grade in (7, 8, 9, 11)]
    print(json.dumps({"subjects": subjects, "banks": banks}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
