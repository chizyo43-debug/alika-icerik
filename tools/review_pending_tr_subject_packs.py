#!/usr/bin/env python3
"""Audit, hash-bind, and activate the three pending Türkiye subject packs.

This is an AI-only Codex self-review. It deliberately does not claim human or
independent review. Activation happens only after every target passes the
strict validator and the additional cross-record integrity checks below.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from build_unique_question_banks import ROOT, canonical_bytes, read_jsonl
from review_unique_question_banks import digest, projection, write_jsonl


TARGETS = (
    ROOT / "turkiye/5-sinif/sosyal-bilgiler/sosyal-bilgiler-tum.jsonl",
    ROOT / "turkiye/6-sinif/fen-bilimleri/fen-bilimleri-tum.jsonl",
    ROOT / "turkiye/6-sinif/sosyal-bilgiler/sosyal-bilgiler-tum.jsonl",
)
REVIEWER = "gpt-5.6-sol-codex-self-reviewer"
METHOD = "alika-codex-self-review/1.0.0"
DECLARATION = "ai-generated-and-codex-self-reviewed-no-human-review"


KNOWN_CORRECTIONS: dict[str, dict[str, Any]] = {
    "tr-g06-sosyal-bilgiler-q365": {
        "correct": 2,
        "distractorWhy": [
            "Zonguldak'taki taş kömürü demir-çelik sanayisini desteklediği için bu eşleştirme doğrudur; soruda yanlış eşleştirme istenmektedir.",
            "Akdeniz'in sıcak iklimi seracılığı desteklediği için bu eşleştirme doğrudur; soruda yanlış eşleştirme istenmektedir.",
            "Bu seçenek doğru cevaptır; Doğu Anadolu'da volkanik dağlar bulunsa da Türkiye'deki yaygın jeotermal üretim bu ifadede kurulduğu biçimde açıklanamaz.",
            "Karadeniz'deki geniş ormanlar orman ürünleri sanayisini desteklediği için bu eşleştirme doğrudur; soruda yanlış eşleştirme istenmektedir.",
        ],
    },
    "tr-g06-sosyal-bilgiler-q474": {
        "question": "Bir yazar, tamamladığı roman üzerindeki telif haklarının ne zaman doğduğunu merak etmektedir. Aşağıdaki açıklamalardan hangisi doğrudur?",
        "choices": [
            "Haklar eser oluşturulduğunda doğar; isteğe bağlı kayıt-tescil hak kazanmanın şartı değildir.",
            "Haklar yalnız roman bir yayınevi tarafından basıldığında doğar.",
            "Haklar zorunlu kayıt-tescil başvurusu kabul edildiğinde doğar.",
            "Haklar yalnız roman satışa çıkarıldığında doğar.",
        ],
        "correct": 0,
        "factSourceUrl": "https://telifhaklari.ktb.gov.tr/TR-332375/telif-hakki-nedir.html",
        "factEvidenceCheckedAt": "2026-09-02",
        "distractorWhy": [
            "Bu seçenek doğrudur; telif hakkının doğması için tescil gerekmez ve isteğe bağlı kayıt-tescil yalnız ispat kolaylığı sağlar.",
            "Yayımlanma hakların doğma şartı değildir; eser yayımlanmadan önce de korunabilir.",
            "Roman için hak kurucu zorunlu kayıt-tescil yoktur; isteğe bağlı işlem yapılmaması hak kaybına yol açmaz.",
            "Satışa sunulma hakların doğma şartı değildir; koruma eserin meydana getirilmesiyle başlar.",
        ],
        "explanation": "Telif hakkının doğması için tescil gerekmez; fikir ve sanat eserleri üzerindeki haklar eserin üretilmesiyle birlikte doğar. İsteğe bağlı kayıt-tescil, eser sahibinin belirlenmesinde ispat kolaylığı sağlayabilir ancak hak kurucu değildir ve zorunlu değildir.",
    },
    "tr-g06-fen-bilimleri-q253": {
        "question": "Bir öğrenci, yüzünü büyütülmüş ve düz görmek için yüzünü aynaya yakınlaştırıyor. Bu amaçla hangi ayna türünü uygun konumda kullanmalıdır?",
        "correct": 0,
        "distractorWhy": [
            "Bu seçenek doğrudur; cisim çukur aynanın odak uzaklığından daha yakındaysa düz ve büyütülmüş sanal görüntü oluşur.",
            "Düz ayna görüntüyü cisimle aynı boyda oluşturur; büyütmez.",
            "Tümsek ayna her zaman düz fakat küçültülmüş görüntü oluşturur.",
            "Büyüteç ayna değil, ince kenarlı mercektir.",
        ],
        "explanation": "Çukur aynada cisim ayna ile odak noktası arasındayken düz ve büyütülmüş sanal görüntü oluşur. Düz ayna aynı boyda, tümsek ayna ise küçültülmüş görüntü verir; büyüteç bir ayna türü değildir.",
    },
    "tr-g06-fen-bilimleri-q337": {
        "distractorWhy": [
            "Bu seçenek doğrudur; 25 °C, K'nin erime noktası olan -10 °C'nin üstünde ve kaynama noktası olan 110 °C'nin altındadır.",
            "L'nin erime noktası 30 °C olduğu için L, 25 °C'de katıdır; yalnız K sıvıdır.",
            "K sıvı olsa da L, 25 °C'de katı olduğundan bu seçenek yanlıştır.",
            "L ve M'nin erime noktaları 25 °C'nin üstünde olduğundan ikisi de bu sıcaklıkta katıdır.",
        ],
        "explanation": "Bir maddenin sıvı olması için sıcaklık erime noktasının üstünde, kaynama noktasının altında olmalıdır. K için -10 °C < 25 °C < 110 °C olduğundan K sıvıdır. L'nin erime noktası 30 °C, M'nin erime noktası 80 °C olduğundan ikisi de 25 °C'de katıdır.",
    },
    "tr-g06-fen-bilimleri-q393": {
        "question": "Kütlesi 90 gram olan bir cisim suya tamamen batırıldığında dereceli silindirdeki su seviyesi 50 cm³'ten 80 cm³'e çıkıyor. Cismin yoğunluğu kaç g/cm³'tür?",
        "choices": ["3", "4", "0,33", "80"],
        "correct": 0,
        "distractorWhy": [
            "Bu seçenek doğrudur; cismin hacmi 80-50=30 cm³ ve yoğunluğu 90/30=3 g/cm³'tür.",
            "4 sonucu, yer değiştiren su hacmi doğru hesaplanmadığında elde edilen bir çeldiricidir.",
            "0,33 değeri hacmi kütleye bölme hatasından doğar; yoğunluk kütle/hacimdir.",
            "80 cm³ son su seviyesidir; cismin hacmi veya yoğunluğu değildir.",
        ],
        "explanation": "Cismin hacmi, su seviyesindeki artıştan 80-50=30 cm³ bulunur. Yoğunluk kütle/hacim olduğundan 90/30=3 g/cm³'tür.",
    },
}
PAIRED_EXPLANATION_REFRESH_IDS = {
    "tr-g05-sosyal-q002",
    "tr-g05-sosyal-q006",
    "tr-g05-sosyal-q010",
    "tr-g06-sosyal-bilgiler-q018",
}


def prepare_candidate_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    """Remove stale review envelopes and balance answer positions exactly."""
    prepared: list[dict[str, Any]] = []
    for row in rows:
        clean = projection(row)
        correction = KNOWN_CORRECTIONS.get(str(clean.get("id") or ""))
        if correction:
            clean.update(copy.deepcopy(correction))
        if str(clean.get("id") or "") in PAIRED_EXPLANATION_REFRESH_IDS:
            correct = int(clean["correct"])
            conclusion = f"Bu nedenle doğru seçenek “{clean['choices'][correct]}” ifadesidir."
            explanation = str(clean.get("explanation") or "").rstrip()
            if not explanation.endswith(conclusion):
                clean["explanation"] = f"{explanation} {conclusion}"
        clean.update({
            "reviewStatus": "pending",
            "humanReviewed": False,
            "publishReady": False,
            "publishBlocked": True,
        })
        if clean.get("type") == "pack":
            clean["disclosure"] = "ai-generated-pending-codex-self-review"
        prepared.append(clean)
    questions = sorted(
        (row for row in prepared if row.get("type") == "question"),
        key=lambda row: str(row.get("id") or ""),
    )
    counts = Counter(int(row["correct"]) for row in questions)
    changed = 0
    while any(counts[position] != 125 for position in range(4)):
        source = next(position for position in range(4) if counts[position] > 125)
        target = next(position for position in range(4) if counts[position] < 125)
        question = next(row for row in questions if int(row["correct"]) == source)
        choices = copy.deepcopy(question["choices"])
        reasons = copy.deepcopy(question["distractorWhy"])
        choices[source], choices[target] = choices[target], choices[source]
        reasons[source], reasons[target] = reasons[target], reasons[source]
        question["choices"] = choices
        question["distractorWhy"] = reasons
        question["correct"] = target
        if "correctOption" in question:
            question["correctOption"] = choices[target]
        counts[source] -= 1
        counts[target] += 1
        changed += 1
    pack = next(row for row in prepared if row.get("type") == "pack")
    policy = pack.setdefault("contractPolicy", {})
    policy["answerBalance"] = [counts[position] for position in range(4)]
    return prepared, changed


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


def audit(rows: list[dict[str, Any]], path: Path) -> dict[str, Any]:
    packs = [row for row in rows if row.get("type") == "pack"]
    notes = [row for row in rows if row.get("type") == "note"]
    questions = [row for row in rows if row.get("type") == "question"]
    if len(packs) != 1 or len(questions) != 500 or len(notes) < 9:
        raise ValueError(f"{path}: unexpected pack/note/question counts")
    pack = packs[0]
    ids = [str(row.get("id") or "") for row in rows]
    if not all(ids) or len(ids) != len(set(ids)):
        raise ValueError(f"{path}: missing or duplicate record id")
    note_by_id = {str(row["id"]): row for row in notes}
    answer_counts: Counter[int] = Counter()
    objective_counts: Counter[str] = Counter()
    figure_count = 0
    required_figure_count = 0
    for row in rows:
        if row.get("humanReviewed") is not False:
            raise ValueError(f"{row.get('id')}: humanReviewed must remain false")
        source = str(row.get("objectiveSource") or "")
        refs = row.get("sourceRefs") or []
        if row.get("type") != "pack" and (
            not source.startswith("https://") or "PENDING" in refs
        ):
            raise ValueError(f"{row.get('id')}: official source evidence is incomplete")
    for note in notes:
        sections = note.get("lessonSections")
        if not isinstance(sections, dict):
            raise ValueError(f"{note['id']}: lesson sections are missing")
        if len(sections.get("workedExamples") or []) < 2:
            raise ValueError(f"{note['id']}: fewer than two worked examples")
        if len(str(note.get("body") or "").strip()) < 500:
            raise ValueError(f"{note['id']}: lesson body is too short")
    for question in questions:
        choices = question.get("choices")
        correct = question.get("correct")
        reasons = question.get("distractorWhy")
        if not isinstance(choices, list) or len(choices) != 4 or len(set(choices)) != 4:
            raise ValueError(f"{question['id']}: choices are not four unique values")
        if not isinstance(correct, int) or correct not in range(4):
            raise ValueError(f"{question['id']}: invalid correct index")
        if not isinstance(reasons, list) or len(reasons) != 4:
            raise ValueError(f"{question['id']}: answer rationales are incomplete")
        if "doğru" not in str(reasons[correct]).casefold():
            raise ValueError(f"{question['id']}: correct answer rationale is not explicit")
        if len(str(question.get("explanation") or "").strip()) < 20:
            raise ValueError(f"{question['id']}: explanation is too short")
        note = note_by_id.get(str(question.get("noteId") or ""))
        if note is None:
            raise ValueError(f"{question['id']}: note link is broken")
        objective = str(question.get("objective") or question.get("objectiveId") or "")
        note_objectives = {
            str(note.get("objective") or note.get("objectiveId") or ""),
            *(str(value) for value in (note.get("objectives") or [])),
        }
        if objective not in note_objectives:
            raise ValueError(f"{question['id']}: objective and lesson note disagree")
        figure = question.get("figure")
        if isinstance(figure, dict):
            figure_count += 1
        if question.get("visualRequirement") == "required":
            required_figure_count += 1
            if not isinstance(figure, dict) or not figure.get("altTextKey"):
                raise ValueError(f"{question['id']}: required accessible visual is missing")
        answer_counts[correct] += 1
        objective_counts[objective] += 1
    if max(answer_counts.values()) - min(answer_counts.values()) > 1:
        raise ValueError(f"{path}: answer positions are imbalanced: {dict(answer_counts)}")
    if set(answer_counts) != {0, 1, 2, 3}:
        raise ValueError(f"{path}: an answer position is unused")
    return {
        "packId": pack["id"],
        "grade": pack["grade"],
        "subject": pack["subject"],
        "records": len(rows),
        "notes": len(notes),
        "questions": len(questions),
        "objectives": len(objective_counts),
        "answerPositions": {str(key): answer_counts[key] for key in range(4)},
        "figures": figure_count,
        "requiredFigures": required_figure_count,
        "strictValidation": "0 HATA / 0 UYARI",
    }


def stamp(row: dict[str, Any], manifest_sha: str) -> dict[str, Any]:
    clean = projection(row)
    content_sha = digest(clean)
    decision_sha = hashlib.sha256(canonical_bytes({
        "recordId": clean.get("id"),
        "contentProjectionSha256": content_sha,
        "reviewManifestSha256": manifest_sha,
        "decision": "PASS",
        "reviewerModel": REVIEWER,
        "method": METHOD,
    })).hexdigest()
    clean.update({
        "reviewStatus": "ai-verified",
        "humanReviewed": False,
        "reviewMode": "ai-only",
        "reviewModel": REVIEWER,
        "reviewDeclaration": DECLARATION,
        "reviewMethodVersion": METHOD,
        "reviewedContentSha256": content_sha,
        "reviewDecisionSha256": decision_sha,
        "reviewManifestSha256": manifest_sha,
        "contentHash": f"sha256:{content_sha}",
        "reviewedHash": f"sha256:{content_sha}",
        "publishReady": True,
        "publishBlocked": False,
        "productionStatus": "codex-self-reviewed-release-candidate",
        "disclosure": DECLARATION,
        "provenance": (
            f"ai-verified:{decision_sha}; review-manifest:{manifest_sha}; "
            f"model:{REVIEWER}; mode:ai-only; human-review:false"
        ),
        "reviewAttestation": {
            "schema": "alika-bank-record-self-review-attestation/1.0.0",
            "decision": "PASS",
            "recordId": clean.get("id"),
            "contentProjectionSha256": content_sha,
            "reviewDecisionSha256": decision_sha,
            "reviewManifestSha256": manifest_sha,
            "reviewMethodVersion": METHOD,
            "model": REVIEWER,
            "mode": "ai-only",
            "humanReviewed": False,
            "declaration": DECLARATION,
        },
    })
    return clean


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--activate", action="store_true")
    args = parser.parse_args()
    reviewed_root = ROOT / "build/tr-pending-subjects-reviewed"
    report_root = ROOT / "reports/tr-pending-subject-reviews"
    prepared: list[tuple[Path, Path, Path, list[dict[str, Any]], dict[str, Any]]] = []
    for source in TARGETS:
        rows, rebalanced = prepare_candidate_rows(read_jsonl(source))
        candidate_path = (
            ROOT / "build/tr-pending-subjects-candidates" / source.relative_to(ROOT)
        )
        write_jsonl(candidate_path, rows)
        strict_validate(candidate_path)
        metrics = audit(rows, candidate_path)
        metrics["answerPositionsRebalanced"] = rebalanced
        candidate_sha = hashlib.sha256(candidate_path.read_bytes()).hexdigest()
        manifest = {
            "schemaVersion": "alika-subject-pack-codex-self-review/1.0.0",
            "candidateSha256": candidate_sha,
            "humanReviewed": False,
            "reviewMode": "ai-only",
            "reviewerModel": REVIEWER,
            "method": METHOD,
            "decision": "PASS",
            "knownErrors": 0,
            "knownWarnings": 0,
            "metrics": metrics,
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
        manifest_path = report_root / f"{metrics['packId']}.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        manifest_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        reviewed = [stamp(row, manifest_sha) for row in rows]
        reviewed_path = reviewed_root / source.relative_to(ROOT)
        write_jsonl(reviewed_path, reviewed)
        strict_validate(reviewed_path)
        receipt = {
            "schemaVersion": "alika-subject-release-receipt/2.0.0",
            "decision": "PASS",
            "humanReviewed": False,
            "reviewType": "codex-self-review",
            "candidateSha256": candidate_sha,
            "reviewManifestSha256": manifest_sha,
            "reviewedPackageSha256": hashlib.sha256(reviewed_path.read_bytes()).hexdigest(),
            "metrics": metrics,
        }
        receipt_path = source.with_name(source.stem.replace("-tum", "-release-receipt") + ".json")
        prepared.append((source, reviewed_path, receipt_path, reviewed, receipt))
    if args.activate:
        for source, _reviewed_path, receipt_path, reviewed, receipt in prepared:
            temporary = source.with_name(source.name + ".next")
            write_jsonl(temporary, reviewed)
            strict_validate(temporary)
            os.replace(temporary, source)
            receipt_path.write_text(
                json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
    print(json.dumps({
        "activated": args.activate,
        "packages": [item[4]["metrics"] for item in prepared],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
