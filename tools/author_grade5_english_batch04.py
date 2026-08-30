#!/usr/bin/env python3
"""Author 100 cumulative Grade 5 English questions (grade rows 701-800)."""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from typing import Any

import author_grade5_english_segment01 as base


MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
LEVELS = (
    [1] * 15 + [2] * 10 +
    [1] * 5 + [2] * 15 + [3] * 15 +
    [3] * 10 + [4] * 10 + [5] * 5 +
    [3] * 5 + [4] * 10
)
CONTEXTS = [
    "dönem sonu dil dosyası", "okul gazetesi İngilizce köşesi", "akran okuma atölyesi",
    "sınıf içi dinleme istasyonu", "İngilizce ürün dosyası", "duyuru ve bilgi kartı seti",
    "günlük yaşam iletişim panosu", "tematik proje dosyası", "konuşma provası kayıtları",
    "okuma kanıtı çizelgesi",
]


def triples() -> list[tuple[int, int, int]]:
    values = sorted(
        combinations(range(24), 3),
        key=lambda value: sha256(("-".join(map(str, value)) + "-alika-eng-b04").encode()).hexdigest(),
    )[:100]
    if len(values) != 100 or len(set(values)) != 100:
        raise RuntimeError("100 unique English triples could not be scheduled")
    return values


def rotate(values: list[str], reasons: list[str], target: int) -> tuple[list[str], list[str]]:
    return (
        [*values[1:1 + target], values[0], *values[1 + target:]],
        [*reasons[1:1 + target], reasons[0], *reasons[1 + target:]],
    )


def options(items: list[tuple[Any, ...]], variant: int) -> tuple[list[str], list[str]]:
    correct = [str(item[3]) for item in items]
    wrong = [str(item[4][(variant + index) % 3]) for index, item in enumerate(items)]

    def line(values: list[str]) -> str:
        return f"I: {values[0]} || II: {values[1]} || III: {values[2]}"

    values = [
        line(correct),
        line([wrong[0], correct[1], correct[2]]),
        line([correct[0], wrong[1], correct[2]]),
        line([correct[0], correct[1], wrong[2]]),
    ]
    reasons = [
        "Üçlü kanıt doğrulaması: Her kayıt kendi kaynak iletisindeki anlamı ve dil işlevini korur. "
        + " ".join(str(item[5]) for item in items),
        f"I. kayıtta ayrıntı değiştirme yanılgısı: İlk sonuç kaynağı bozarken II ve III doğrudur. {items[0][5]}",
        f"II. kayıtta iletişim işlevi yanılgısı: İkinci sonuç istenen göreve uygun değildir; I ve III doğrudur. {items[1][5]}",
        f"III. kayıtta dayanaksız çıkarım yanılgısı: Son sonuç kaynakta bulunmayan bir bilgi ekler; I ve II doğrudur. {items[2][5]}",
    ]
    return values, reasons


def table(qid: str, items: list[tuple[Any, ...]], labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, h3, alt = (f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.h3", f"{prefix}.alt")
    labels[h1], labels[h2], labels[h3] = "Kayıt", "İngilizce kaynak ileti", "Düzenleme görevi"
    labels[alt] = (
        "I, II ve III olarak adlandırılmış üç İngilizce kaynak ileti ile her birinin düzenleme görevini "
        "gösteren tablo; doğru sonuçlar belirtilmemiştir."
    )
    return {
        "kind": "table", "headerKeys": [h1, h2, h3], "altTextKey": alt,
        "rows": [
            [{"v": label}, {"v": item[1]}, {"v": item[2]}]
            for label, item in zip(("I", "II", "III"), items)
        ],
    }


def make(
    local: int,
    selected: tuple[int, int, int],
    note_map: dict[str, dict[str, Any]],
    labels: dict[str, str],
) -> dict[str, Any]:
    global_number = 700 + local
    items = [base.ITEMS[index] for index in selected]
    notes = [note_map[item[0]] for item in items]
    objectives = [str((note.get("objectives") or [""])[0]) for note in notes]
    variant = (local - 1) // 8
    raw_choices, raw_reasons = options(items, variant)
    correct = (global_number - 1) % 4
    choices, distractor_why = rotate(raw_choices, raw_reasons, correct)
    mode, level = MODES[local - 1], LEVELS[local - 1]
    context = CONTEXTS[(local - 1) % len(CONTEXTS)]
    qid = f"tr-g05-bank-eng-b04-q{local:03d}"

    sources = " ".join(
        f"{label}. kaynak: '{item[1]}' Görev: {item[2]}"
        for label, item in zip(("I", "II", "III"), items)
    )
    if mode == "comprehension":
        stem = (
            f"Bir {context} için üç kayıt okunuyor. {sources} "
            "Üç kaydın da açık bilgisini ve iletişim amacını koruyan sonuç dizisi hangisidir?"
        )
        fig = None
    elif mode == "application":
        stem = (
            f"Öğrenci {context} hazırlarken şu üç kaynağı ayrı kartlara aktaracaktır: {sources} "
            "Kartların hiçbirinde kişi, yer, zaman, eylem veya dil işlevi değişmemesi için hangi üçlü seçilmelidir?"
        )
        fig = None
    elif mode == "analysis":
        stem = (
            f"Aşağıdaki tabloyu inceleyiniz. {context.capitalize()} tablosunda üç kaynak ve bunlara ait görevler verilmiştir. "
            f"Görev odakları sırasıyla I için '{items[0][2]}', II için '{items[1][2]}' ve "
            f"III için '{items[2][2]}' biçimindedir. "
            "Her satırı kendi kanıtıyla çözümleyip üç doğru sonucu birlikte veren seçenek hangisidir?"
        )
        fig = table(qid, items, labels)
    else:
        mistaken = [str(item[4][(variant + index) % 3]) for index, item in enumerate(items)]
        stem = (
            f"{context.capitalize()} denetiminde öğrenci sırasıyla '{mistaken[0]}', '{mistaken[1]}' ve "
            f"'{mistaken[2]}' yazmıştır. Kaynaklar şunlardır: {sources} "
            "Her kayıttaki yanılgıyı ayrı denetleyerek üç doğru düzeltmeyi veren seçenek hangisidir?"
        )
        fig = None

    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "Üç kaynak ileti ile bunların görev eşleşmeleri yalnız tabloda birlikte gösterilir.",
        "acceptableKinds": ["table"],
        "evidenceDimensions": ["kaynak ileti", "düzenleme görevi", "kayıt sırası"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "Üç kaynak ileti ve görevleri soru metninde eksiksiz verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    note = notes[0]
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "İngilizce", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — üçlü kanıt {mode}",
        "objective": objectives[0], "objectiveId": objectives[0],
        "integratedObjectives": objectives,
        "noteId": note.get("id"), "noteKey": note.get("id"),
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct],
        "distractorWhy": distractor_why,
        "explanation": (
            "Üç kaynak birbirinden bağımsız doğrulanır. "
            + " ".join(f"{label} için {item[5]}" for label, item in zip(("I", "II", "III"), items))
        ),
        "level": level,
        "difficultyReason": (
            f"Düzey {level}; üç farklı İngilizce kaydı {mode} biçiminde çözüp sonuçları birbirine "
            "karıştırmadan tek seçimde birleştirmeyi gerektirir."
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
    if len(existing) != 700:
        raise RuntimeError("the first 700 grade questions must be regenerated before English batch 04")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    rows = [make(local, selected, note_map, labels) for local, selected in enumerate(triples(), 1)]
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
    print(json.dumps({"englishQuestions": 100, "englishTotal": 330, "gradeTotal": 800}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
