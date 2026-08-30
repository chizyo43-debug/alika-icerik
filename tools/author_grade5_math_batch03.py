#!/usr/bin/env python3
"""Author 100 two-problem Grade 5 mathematics questions (grade rows 1001-1100)."""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from typing import Any

import author_grade5_math_segment01 as base
import author_grade5_math_batch02 as prior


MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
LEVELS = (
    [1] * 15 + [2] * 10 +
    [1] * 5 + [2] * 15 + [3] * 15 +
    [3] * 10 + [4] * 10 + [5] * 5 +
    [3] * 5 + [4] * 10
)
CONTEXTS = [
    "iki istasyonlu matematik turu", "akran çözüm karşılaştırması", "konular arası tekrar kartı",
    "matematiksel kanıt dosyası", "çift görevli uygulama", "öz değerlendirme çizelgesi",
    "iki aşamalı sınıf etkinliği", "çözüm yöntemleri panosu",
]


def pairs() -> list[tuple[int, int]]:
    values = sorted(
        combinations(range(len(prior.NOTE_IDS)), 2),
        key=lambda value: sha256(("-".join(map(str, value)) + "-alika-mat-b03").encode()).hexdigest(),
    )[:100]
    if len(values) != 100 or len(set(values)) != 100:
        raise RuntimeError("100 unique mathematics pairs could not be scheduled")
    return values


def raw_options(
    first: tuple[str, str, list[str], str],
    second: tuple[str, str, list[str], str],
    variant: int,
) -> tuple[list[str], list[str]]:
    _, correct_a, wrong_a, explanation_a = first
    _, correct_b, wrong_b, explanation_b = second
    bad_a = wrong_a[variant % 3]
    bad_b = wrong_b[(variant + 1) % 3]
    other_a = wrong_a[(variant + 2) % 3]
    other_b = wrong_b[variant % 3]
    choices = [
        f"I. görev — {correct_a} || II. görev — {correct_b}",
        f"I. görev — {bad_a} || II. görev — {correct_b}",
        f"I. görev — {correct_a} || II. görev — {bad_b}",
        f"I. görev — {other_a} || II. görev — {other_b}",
    ]
    reasons = [
        f"Doğru iki-model denetimi: I için {explanation_a} II için {explanation_b}",
        f"Birinci görevde ilişki yanılgısı: I. çözüm konu kuralını bozarken II. çözüm doğrudur. {explanation_a}",
        f"İkinci görevde işlem yanılgısı: I. çözüm doğru olsa da II. sonuç verilerle doğrulanamaz. {explanation_b}",
        f"Çifte model yanılgısı: Her iki çözüm de kendi problemindeki koşul, işlem sırası veya birimi değiştirir. {explanation_a} {explanation_b}",
    ]
    return choices, reasons


def table(
    qid: str,
    first_title: str,
    second_title: str,
    first_statement: str,
    second_statement: str,
    labels: dict[str, str],
) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, h3, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.h3", f"{prefix}.alt"
    labels[h1], labels[h2], labels[h3] = "Görev", "Konu", "Matematiksel veri"
    labels[alt] = "Farklı iki matematik konusuna ait I ve II veri kayıtlarını gösteren tablo; doğru çözüm belirtilmemiştir."
    return {
        "kind": "table", "headerKeys": [h1, h2, h3], "altTextKey": alt,
        "rows": [
            [{"v": "I"}, {"v": first_title}, {"v": first_statement}],
            [{"v": "II"}, {"v": second_title}, {"v": second_statement}],
        ],
    }


def make(
    local: int,
    selected: tuple[int, int],
    note_map: dict[str, dict[str, Any]],
    labels: dict[str, str],
    *,
    global_base: int = 1000,
    batch_id: str = "b03",
) -> dict[str, Any]:
    global_number = global_base + local
    first_index, second_index = selected
    variant = (local - 1) // 8
    first = prior.case_data(first_index, variant)
    second = prior.case_data(second_index, variant + 2)
    first_note = note_map[prior.NOTE_IDS[first_index]]
    second_note = note_map[prior.NOTE_IDS[second_index]]
    first_objectives = [str(value) for value in first_note.get("objectives") or [""]]
    second_objectives = [str(value) for value in second_note.get("objectives") or [""]]
    objective = first_objectives[variant % len(first_objectives)]
    secondary_objective = second_objectives[(variant + 1) % len(second_objectives)]
    raw_choices, raw_reasons = raw_options(first, second, variant)
    correct = (global_number - 1) % 4
    choices, distractor_why = base.rotate(raw_choices, raw_reasons, correct)
    mode, level = MODES[local - 1], LEVELS[local - 1]
    context = CONTEXTS[(local - 1) % len(CONTEXTS)]
    qid = f"tr-g05-bank-mat-{batch_id}-q{local:03d}"

    if mode == "comprehension":
        stem = (
            f"Bir {context} içinde iki bağımsız kayıt okunuyor. I: {first[0]} II: {second[0]} "
            "Her kaydın temel kavramını doğru yorumlayan çözüm çifti hangisidir?"
        )
        fig = None
    elif mode == "application":
        stem = (
            f"{context.capitalize()} için iki problem ayrı ayrı uygulanacaktır. I: {first[0]} II: {second[0]} "
            "Verileri doğru matematiksel modele dönüştürüp iki sonucu da doğrulayan çift hangisidir?"
        )
        fig = None
    elif mode == "analysis":
        stem = (
            f"Aşağıdaki tabloda '{first_note['title']}' ve '{second_note['title']}' konularına ait iki veri kaydı vardır. "
            "Kayıtları birbirine karıştırmadan çözümleyip iki doğru sonucu veren seçenek hangisidir?"
        )
        fig = table(qid, str(first_note["title"]), str(second_note["title"]), first[0], second[0], labels)
    else:
        stem = (
            f"{context.capitalize()} sırasında öğrenci I için '{first[2][variant % 3]}', II için "
            f"'{second[2][(variant + 1) % 3]}' yazıyor. I. veri {first[0]} II. veri {second[0]} "
            "İki yanılgıyı da düzelten kanıt çifti hangisidir?"
        )
        fig = None

    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "İki bağımsız matematiksel veri kaydı ve konu eşleşmeleri yalnız tabloda gösterilir.",
        "acceptableKinds": ["table"], "evidenceDimensions": ["görev", "konu", "matematiksel veri"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "İki problemin bütün verileri ve çözüm koşulları soru metninde verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "Matematik", "grade": 5,
        "unitKey": first_note.get("unitKey"), "topicKey": first_note.get("topicKey"),
        "subtopicKey": first_note.get("subtopicKey"), "topic": first_note.get("topic"),
        "title": f"{first_note['title']} — iki görev {mode}",
        "objective": objective, "objectiveId": objective,
        "integratedObjectives": [objective, secondary_objective],
        "noteId": first_note.get("id"), "noteKey": first_note.get("id"),
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct],
        "distractorWhy": distractor_why,
        "explanation": f"I. kayıt için {first[3]} II. kayıt için {second[3]} İki sonuç kendi verisiyle ayrı ayrı denetlenir.",
        "level": level,
        "difficultyReason": f"Düzey {level}; iki farklı matematik konusundaki veriyi {mode} biçiminde ayrı modellere dönüştürüp sonuçları tek kararda birleştirmeyi gerektirir.",
        "questionType": mode, "familyId": f"tr-g05-bank-mat-family-{global_number:03d}",
        "objectiveSource": first_note.get("objectiveSource"),
        "objectiveEvidenceId": first_note.get("objectiveEvidenceId"),
        "sourceRefs": first_note.get("sourceRefs") or [], "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    existing = [json.loads(line) for line in base.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1000:
        raise RuntimeError("the first 1000 grade questions must be regenerated before math batch 03")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    rows = [make(local, selected, note_map, labels) for local, selected in enumerate(pairs(), 1)]
    base.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    base.LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"mathQuestions": 100, "mathTotal": 215, "gradeTotal": 1100}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
