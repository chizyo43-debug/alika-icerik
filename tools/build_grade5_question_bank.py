#!/usr/bin/env python3
"""Build the curated Türkiye Grade 5 all-subject 2,000-question bank.

The bank is an aggregate, not 2,000 newly authored questions. It selects 400
already AI-verified questions from each of the five release packages. Every
existing visual question is retained; removals are limited to non-visual
questions and preserve every note, objective, and family.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRADE5 = ROOT / "turkiye" / "5-sinif"
OUTPUT = GRADE5 / "soru-bankasi" / "5-sinif-tum-dersler-2000-soru.jsonl"
CONTRACT_HASH = (
    "sha256:74b5ee649f01933fd50dfeb7e29706e7dc1ddf0fe3e014ead2fe5cd0896ae7a1"
)
TARGET_PER_SUBJECT = 400
TARGET_PER_POSITION = 100
SUBJECTS = (
    ("Matematik", GRADE5 / "matematik" / "matematik-tum.jsonl"),
    (
        "Fen Bilimleri",
        GRADE5 / "fen-bilimleri" / "fen-bilimleri-tum.jsonl",
    ),
    ("Türkçe", GRADE5 / "turkce" / "turkce-tum.jsonl"),
    ("İngilizce", GRADE5 / "ingilizce" / "ingilizce-tum.jsonl"),
    (
        "Sosyal Bilgiler",
        GRADE5 / "sosyal-bilgiler" / "sosyal-bilgiler-tum.jsonl",
    ),
)
REVIEW_FIELDS = {
    "reviewStatus",
    "humanReviewed",
    "reviewMode",
    "reviewModel",
    "reviewDeclaration",
    "reviewedContentSha256",
    "reviewDecisionSha256",
    "contentHash",
    "reviewedHash",
    "reviewedBy",
    "provenance",
}


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":"))
            for row in rows
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def canonical_sha256(value: object) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def assert_verified(record: dict) -> None:
    content = {
        key: copy.deepcopy(value)
        for key, value in record.items()
        if key not in REVIEW_FIELDS
    }
    digest = canonical_sha256(content)
    expected = f"sha256:{digest}"
    if (
        record.get("reviewStatus") != "ai-verified"
        or record.get("humanReviewed") is not False
        or record.get("reviewDeclaration")
        != "ai-generated-and-ai-reviewed-no-human-review"
        or record.get("contentHash") != expected
        or record.get("reviewedHash") != expected
        or record.get("reviewedContentSha256") != digest
    ):
        raise ValueError(f"{record.get('id')}: güncel AI inceleme damgası yok")


def stable_rank(subject: str, question: dict) -> str:
    return hashlib.sha256(
        f"grade5-bank-v1\0{subject}\0{question['id']}".encode("utf-8")
    ).hexdigest()


def normalize_option(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return re.sub(r"\s+", " ", text).strip(" \t\r\n.,;:!?\"'()[]{}")


def select_subject(
    subject: str, notes: list[dict], questions: list[dict]
) -> list[dict]:
    if len(questions) != 500:
        raise ValueError(f"{subject}: 500 kaynak soru bekleniyor")
    if Counter(question["correct"] for question in questions) != {
        0: 125,
        1: 125,
        2: 125,
        3: 125,
    }:
        raise ValueError(f"{subject}: kaynak cevap dağılımı 125'er değil")

    note_counts = Counter(question["noteId"] for question in questions)
    objective_counts = Counter(question["objective"] for question in questions)
    family_counts = Counter(question["familyId"] for question in questions)
    option_counts: Counter[str] = Counter()
    option_families: dict[str, set[str]] = defaultdict(set)
    for question in questions:
        for option in question["choices"]:
            normalized = normalize_option(option)
            option_counts[normalized] += 1
            option_families[normalized].add(question["familyId"])
    shared_options = {
        option
        for option, count in option_counts.items()
        if count >= 4 and len(option_families[option]) >= 2
    }
    # Derleme, kaynak pakette doğru cevap olarak bulunan ortak bir seçeneğin
    # bütün doğru örneklerini yanlışlıkla eleyip onu "sürekli yanlış dolgu"ya
    # dönüştürmemeli.
    protected_correct = {
        question["id"]
        for question in questions
        if normalize_option(question["choices"][question["correct"]])
        in shared_options
    }
    removed: set[str] = set()

    for position in range(4):
        candidates = sorted(
            (
                question
                for question in questions
                if (
                    question["correct"] == position
                    and not question.get("figure")
                    and question["id"] not in protected_correct
                )
            ),
            key=lambda question: (
                -note_counts[question["noteId"]],
                -objective_counts[question["objective"]],
                -family_counts[question["familyId"]],
                stable_rank(subject, question),
            ),
        )
        for question in candidates:
            if sum(
                1
                for item in questions
                if item["correct"] == position and item["id"] in removed
            ) >= 25:
                break
            note_id = question["noteId"]
            objective = question["objective"]
            family = question["familyId"]
            if (
                note_counts[note_id] <= 1
                or objective_counts[objective] <= 1
                or family_counts[family] <= 1
            ):
                continue
            removed.add(question["id"])
            note_counts[note_id] -= 1
            objective_counts[objective] -= 1
            family_counts[family] -= 1

    selected = [
        copy.deepcopy(question)
        for question in questions
        if question["id"] not in removed
    ]
    if len(selected) != TARGET_PER_SUBJECT:
        raise ValueError(
            f"{subject}: 400 soru seçilemedi, bulunan {len(selected)}"
        )
    if Counter(question["correct"] for question in selected) != {
        0: TARGET_PER_POSITION,
        1: TARGET_PER_POSITION,
        2: TARGET_PER_POSITION,
        3: TARGET_PER_POSITION,
    }:
        raise ValueError(f"{subject}: cevap konumları 100'er değil")
    if any(question.get("figure") and question["id"] in removed for question in questions):
        raise AssertionError(f"{subject}: görselli soru çıkarıldı")
    selected_notes = {question["noteId"] for question in selected}
    if selected_notes != {note["id"] for note in notes}:
        missing = sorted({note["id"] for note in notes} - selected_notes)
        raise ValueError(f"{subject}: sorusuz kalan notlar: {missing}")
    if {question["objective"] for question in selected} != {
        question["objective"] for question in questions
    }:
        raise ValueError(f"{subject}: kazanım kapsamı kayboldu")
    if {question["familyId"] for question in selected} != {
        question["familyId"] for question in questions
    }:
        raise ValueError(f"{subject}: aile kapsamı kayboldu")
    return selected


def referenced_label_keys(value: object) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for name, child in value.items():
            if (
                isinstance(child, str)
                and (name == "key" or name.endswith("Key"))
            ):
                found.add(child)
            elif name.endswith("Keys") and isinstance(child, (list, dict)):
                if isinstance(child, list):
                    found.update(
                        item for item in child if isinstance(item, str)
                    )
                else:
                    found.update(
                        item for item in child.values()
                        if isinstance(item, str)
                    )
            found.update(referenced_label_keys(child))
    elif isinstance(value, list):
        for child in value:
            found.update(referenced_label_keys(child))
    return found


def build() -> tuple[list[dict], dict]:
    all_notes: list[dict] = []
    all_questions: list[dict] = []
    all_labels: dict[str, str] = {}
    all_sources: dict[str, dict] = {}
    source_packages = []
    visual_by_subject: dict[str, dict[str, int]] = {}

    for subject, path in SUBJECTS:
        rows = read_jsonl(path)
        pack = next(row for row in rows if row.get("type") == "pack")
        notes = [row for row in rows if row.get("type") == "note"]
        questions = [row for row in rows if row.get("type") == "question"]
        if pack.get("reviewStatus") != "ai-verified":
            raise ValueError(f"{subject}: kaynak paket AI doğrulanmış değil")
        for record in notes + questions:
            assert_verified(record)
        selected = select_subject(subject, notes, questions)
        all_notes.extend(copy.deepcopy(notes))
        all_questions.extend(selected)
        source_packages.append(
            {
                "id": pack["id"],
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "questions": len(selected),
            }
        )
        visual_by_subject[subject] = {
            "source": sum(bool(question.get("figure")) for question in questions),
            "selected": sum(bool(question.get("figure")) for question in selected),
        }
        for key, value in (pack.get("labels") or {}).items():
            previous = all_labels.get(key)
            if previous is not None and previous != value:
                raise ValueError(f"labels çakışması: {key}")
            all_labels[key] = value
        for item in pack.get("sources") or []:
            source_id = item.get("sourceId")
            if not source_id:
                raise ValueError(f"{subject}: sourceId boş")
            normalized_item = copy.deepcopy(item)
            # ``reused`` yalnız kaynak paketin kendi üretim geçmişini anlatır;
            # aynı resmî belgenin kimliği veya doğrulama kanıtı değildir.
            normalized_item.pop("reused", None)
            previous = all_sources.get(source_id)
            if previous is not None and previous != normalized_item:
                raise ValueError(f"kaynak tanımı çakışması: {source_id}")
            all_sources[source_id] = normalized_item

    if len({note["id"] for note in all_notes}) != len(all_notes):
        raise ValueError("Dersler arasında not kimliği çakışıyor")
    if len({question["id"] for question in all_questions}) != len(all_questions):
        raise ValueError("Dersler arasında soru kimliği çakışıyor")

    note_ids_by_objective: defaultdict[str, set[str]] = defaultdict(set)
    for note in all_notes:
        for objective in note.get("objectives") or [note.get("objective")]:
            if objective:
                note_ids_by_objective[str(objective)].add(note["id"])
    question_counts = Counter(
        str(question["objective"]) for question in all_questions
    )
    linked_notes: defaultdict[str, set[str]] = defaultdict(set)
    for question in all_questions:
        linked_notes[str(question["objective"])].add(question["noteId"])
    coverage = {
        objective: {
            "notes": sorted(
                linked_notes[objective] or note_ids_by_objective[objective]
            ),
            "questions": question_counts[objective],
        }
        for objective in sorted(question_counts)
    }

    used_labels: set[str] = set()
    for record in all_notes + all_questions:
        used_labels.update(referenced_label_keys(record.get("figure")))
    labels = {
        key: all_labels[key]
        for key in sorted(used_labels)
        if key in all_labels
    }
    subject_counts = dict(
        sorted(Counter(question["subject"] for question in all_questions).items())
    )
    answer_balance = [
        sum(question["correct"] == position for question in all_questions)
        for position in range(4)
    ]
    figure_count = sum(bool(question.get("figure")) for question in all_questions)
    families = {question["familyId"] for question in all_questions}
    pack = {
        "type": "pack",
        "schemaVersion": "2.2",
        "id": "tr.g05.tum-dersler.soru-bankasi",
        "version": 1,
        "lang": "tr",
        "country": "TR",
        "curriculum": "MEB-TYMM-2024+2025",
        "curricula": ["MEB-TYMM-2024", "MEB-TYMM-2025"],
        "subject": "Tüm Dersler",
        "grade": 5,
        "theme": "Türkiye 5. Sınıf — 2.000 Soruluk Tüm Dersler Soru Bankası",
        "license": "CC-BY-NC-4.0",
        "source": "alika-grade5-ai-verified-course-packs",
        "sources": [all_sources[key] for key in sorted(all_sources)],
        "sourcePackages": source_packages,
        "selectionPolicy": {
            "version": "grade5-bank-v1",
            "mode": "curated-aggregate",
            "perSubject": TARGET_PER_SUBJECT,
            "perAnswerPositionPerSubject": TARGET_PER_POSITION,
            "preserveAllFigures": True,
            "preserveEveryNoteObjectiveAndFamily": True,
        },
        "labels": labels,
        "objectives": sorted(question_counts),
        "coverage": coverage,
        "counts": {"notes": len(all_notes), "questions": len(all_questions)},
        "levelScale": [1, 5],
        "contentContractVersion": "2.2",
        "contentContractHash": CONTRACT_HASH,
        "visualPolicy": {
            "version": "1.0",
            "everyNote": True,
            "questionMinimumPercent": 0,
            "balancedByObjective": False,
            "preserveAllSourceFigures": True,
            "bySubject": visual_by_subject,
            "rationale": (
                "Kaynak paketlerdeki 477 görselli sorunun tamamı korunur. "
                "Tablo, grafik, şekil, akış veya devre gerektiren sorular "
                "görselsiz derlenmez."
            ),
        },
        "contractPolicy": {
            "questionCount": 2000,
            "perSubjectQuestionCount": subject_counts,
            "idScopeMode": "multi-subject",
            "minFamilies": len(families),
            "maxPerFamily": 8,
            "answerBalance": answer_balance,
            "minFiguredQuestions": figure_count,
            "everyNoteHasFigure": True,
            "objectiveBalanceMode": "coverage",
        },
        "reviewStatus": "pending",
        "humanReviewed": False,
        "publishBlocked": True,
        "disclosure": "ai-generated-and-ai-reviewed-no-human-review",
        "provenance": (
            "machine-compiled:codex-sol:2026-08; "
            "sources=grade5-ai-verified; review=pending"
        ),
    }
    rows = [
        pack,
        *sorted(all_notes, key=lambda row: (row["subject"], row["id"])),
        *sorted(all_questions, key=lambda row: (row["subject"], row["id"])),
    ]
    summary = {
        "notes": len(all_notes),
        "questions": len(all_questions),
        "subjects": subject_counts,
        "answers": answer_balance,
        "families": len(families),
        "figures": figure_count,
        "visualBySubject": visual_by_subject,
    }
    return rows, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    rows, summary = build()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.write:
        write_jsonl(OUTPUT, rows)
        print(OUTPUT.relative_to(ROOT).as_posix())
    else:
        print("(dosyayı yazmak için --write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
