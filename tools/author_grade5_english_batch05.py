#!/usr/bin/env python3
"""Finish the Grade 5 English quota with 85 four-source questions (rows 801-885)."""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from typing import Any

import author_grade5_english_segment01 as base
from author_grade5_english_batch04 import rotate


MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25
LEVELS = (
    [1] * 15 + [2] * 10 +
    [1] * 5 + [2] * 15 + [3] * 15 +
    [3] * 10 + [4] * 10 + [5] * 5
)
CONTEXTS = [
    "çoklu dinleme sınaması", "dört köşe okuma etkinliği", "sınıf İngilizce arşivi",
    "tematik ileti dosyası", "bağımsız kanıt kontrolü", "dil işlevleri sergisi",
    "kazanım öz değerlendirmesi", "kaynak-taslak karşılaştırması", "iletişim kartları atölyesi",
    "İngilizce düzeltmen masası", "dönem sonu ürün seçkisi",
]


def quartets() -> list[tuple[int, int, int, int]]:
    values = sorted(
        combinations(range(24), 4),
        key=lambda value: sha256(("-".join(map(str, value)) + "-alika-eng-b05").encode()).hexdigest(),
    )[:85]
    if len(values) != 85 or len(set(values)) != 85:
        raise RuntimeError("85 unique English quartets could not be scheduled")
    return values


def raw_options(items: list[tuple[Any, ...]], variant: int) -> tuple[list[str], list[str]]:
    correct = [str(item[3]) for item in items]
    wrong = [str(item[4][(variant + index) % 3]) for index, item in enumerate(items)]

    def line(values: list[str]) -> str:
        return " || ".join(f"{label}: {value}" for label, value in zip(("I", "II", "III", "IV"), values))

    choices = [
        line(correct),
        line([wrong[0], correct[1], correct[2], correct[3]]),
        line([correct[0], wrong[1], correct[2], correct[3]]),
        line([correct[0], correct[1], wrong[2], wrong[3]]),
    ]
    reasons = [
        "Dört kaynak da bağımsız doğrulanmıştır: " + " ".join(str(item[5]) for item in items),
        f"Ayrıntı değiştirme yanılgısı: I. kayıt kaynağı bozar; diğer üç kayıt doğrudur. {items[0][5]}",
        f"Dil işlevi yanılgısı: II. kayıt istenen iletişim görevini bozarken diğer üç kayıt doğrudur. {items[1][5]}",
        f"Kanıtsız çıkarım yanılgısı: III ve IV. kayıtlar kaynakta bulunmayan sonuçlar ekler. {items[2][5]} {items[3][5]}",
    ]
    return choices, reasons


def table(qid: str, items: list[tuple[Any, ...]], labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, h3, alt = (f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.h3", f"{prefix}.alt")
    labels[h1], labels[h2], labels[h3] = "Kayıt", "Kaynak ileti", "Kanıt görevi"
    labels[alt] = (
        "Dört İngilizce kaynak iletiyi ve her birinin kanıt görevini I-IV satırlarında gösteren tablo; "
        "doğru sonuçlar işaretlenmemiştir."
    )
    return {
        "kind": "table", "headerKeys": [h1, h2, h3], "altTextKey": alt,
        "rows": [
            [{"v": label}, {"v": item[1]}, {"v": item[2]}]
            for label, item in zip(("I", "II", "III", "IV"), items)
        ],
    }


def make(
    local: int,
    selected: tuple[int, int, int, int],
    note_map: dict[str, dict[str, Any]],
    labels: dict[str, str],
) -> dict[str, Any]:
    global_number = 800 + local
    items = [base.ITEMS[index] for index in selected]
    notes = [note_map[item[0]] for item in items]
    objectives = [str((note.get("objectives") or [""])[0]) for note in notes]
    mode, level = MODES[local - 1], LEVELS[local - 1]
    variant = (local - 1) // 7
    choices_raw, reasons_raw = raw_options(items, variant)
    correct = (global_number - 1) % 4
    choices, distractor_why = rotate(choices_raw, reasons_raw, correct)
    context = CONTEXTS[(local - 1) % len(CONTEXTS)]
    qid = f"tr-g05-bank-eng-b05-q{local:03d}"
    sources = " ".join(
        f"{label}. '{item[1]}' Görev: {item[2]}"
        for label, item in zip(("I", "II", "III", "IV"), items)
    )

    if mode == "comprehension":
        stem = (
            f"{context.capitalize()} kapsamında dört kısa kaynak okunuyor: {sources} "
            "Her kaydın açık bilgisini kendi göreviyle eşleştirerek dört doğru sonucu veren dizi hangisidir?"
        )
        fig = None
    elif mode == "application":
        stem = (
            f"Bir öğrenci {context} için şu dört kaynağı ayrı ürünlere dönüştürecektir: {sources} "
            "Kişi, yer, zaman, eylem ve iletişim işlevlerini değiştirmeden uygulanabilecek sonuç dizisi hangisidir?"
        )
        fig = None
    else:
        stem = (
            f"Aşağıdaki tabloyu inceleyiniz. {context.capitalize()} tablosunda dört bağımsız kaynak vardır. Görevler sırasıyla "
            f"'{items[0][2]}', '{items[1][2]}', '{items[2][2]}' ve '{items[3][2]}' biçimindedir. "
            "Her satırı kendi kanıtıyla çözümleyip dört doğru sonucu birlikte veren seçenek hangisidir?"
        )
        fig = table(qid, items, labels)

    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "Dört kaynak ileti ile görev eşleşmeleri yalnız tabloda düzenli olarak gösterilir.",
        "acceptableKinds": ["table"],
        "evidenceDimensions": ["kaynak ileti", "kanıt görevi", "kayıt sırası"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "Dört kaynak ileti ve görevleri soru metninde eksiksiz verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    note = notes[0]
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "İngilizce", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — dört kaynak {mode}",
        "objective": objectives[0], "objectiveId": objectives[0],
        "integratedObjectives": objectives,
        "noteId": note.get("id"), "noteKey": note.get("id"),
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct],
        "distractorWhy": distractor_why,
        "explanation": " ".join(
            f"{label} için {item[5]}" for label, item in zip(("I", "II", "III", "IV"), items)
        ),
        "level": level,
        "difficultyReason": (
            f"Düzey {level}; dört farklı İngilizce kaydı {mode} biçiminde bağımsız çözüp sonuçları tek "
            "seçimde birleştirmeyi gerektirir."
        ),
        "questionType": mode, "familyId": f"tr-g05-bank-eng-family-{global_number:03d}",
        "objectiveSource": note.get("objectiveSource"),
        "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [], "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    existing = [
        json.loads(line)
        for line in base.OUTPUT.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(existing) != 800:
        raise RuntimeError("the first 800 grade questions must be regenerated before English batch 05")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    rows = [make(local, selected, note_map, labels) for local, selected in enumerate(quartets(), 1)]
    base.OUTPUT.write_text(
        "\n".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":"))
            for row in [*existing, *rows]
        ) + "\n",
        encoding="utf-8", newline="\n",
    )
    base.LABELS_OUTPUT.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({"englishQuestions": 85, "englishTotal": 415, "gradeTotal": 885}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
