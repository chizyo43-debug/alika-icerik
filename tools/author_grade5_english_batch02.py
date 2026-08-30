#!/usr/bin/env python3
"""Author 100 integrated Grade 5 English questions (grade rows 501–600)."""
from __future__ import annotations

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


def paired_items(local: int) -> tuple[tuple[Any, ...], tuple[Any, ...]]:
    unit = (local - 1) % 8
    variant = (local - 1) // 8
    group = base.ITEMS[unit * 3:unit * 3 + 3]
    first_index = variant % 3
    second_index = (first_index + 1 + (variant // 3) % 2) % 3
    if second_index == first_index:
        second_index = (first_index + 1) % 3
    return group[first_index], group[second_index]


def raw_options(first: tuple[Any, ...], second: tuple[Any, ...], variant: int) -> tuple[list[str], list[str]]:
    correct_a, wrong_a = first[3], first[4]
    correct_b, wrong_b = second[3], second[4]
    pairs = [
        (correct_a, correct_b),
        (wrong_a[variant % 3], correct_b),
        (correct_a, wrong_b[(variant + 1) % 3]),
        (wrong_a[(variant + 2) % 3], wrong_b[variant % 3]),
    ]
    options = [f"I → {a} | II → {b}" for a, b in pairs]
    reasons = [
        f"Doğru iki-ileti çözümü: I için {first[5]} II için {second[5]}",
        f"İlk ileti yanılgısı: I. eşleştirme kişi, yer, zaman veya dil işlevini değiştirir; II doğrudur. I için {first[5]}",
        f"İkinci ileti yanılgısı: I doğru çözülse de II. eşleştirme verilen iletiden çıkarılamaz. II için {second[5]}",
        f"Çifte ileti yanılgısı: Her iki eşleştirme de kendi ileti kanıtını veya dil işlevini bozar. I için {first[5]} II için {second[5]}",
    ]
    return options, reasons


def rotate(values: list[str], reasons: list[str], target: int) -> tuple[list[str], list[str]]:
    return (
        [*values[1:1 + target], values[0], *values[1 + target:]],
        [*reasons[1:1 + target], reasons[0], *reasons[1 + target:]],
    )


def table(qid: str, first: tuple[Any, ...], second: tuple[Any, ...], labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.alt"
    labels[h1], labels[h2] = "İleti", "Dinleme/okuma kaydı"
    labels[alt] = "I ve II olarak adlandırılan iki İngilizce iletiyi gösteren tablo; doğru yorum işaretlenmemiştir."
    return {
        "kind": "table", "headerKeys": [h1, h2], "altTextKey": alt,
        "rows": [[{"v": "I"}, {"v": first[1]}], [{"v": "II"}, {"v": second[1]}]],
    }


def make(local: int, note_map: dict[str, dict[str, Any]], labels: dict[str, str]) -> dict[str, Any]:
    global_number = 500 + local
    first, second = paired_items(local)
    note = note_map[first[0]]
    secondary_note = note_map[second[0]]
    objective = str((note.get("objectives") or [""])[0])
    secondary_objective = str((secondary_note.get("objectives") or [""])[0])
    variant = (local - 1) // 8
    options, reasons = raw_options(first, second, variant)
    correct = (global_number - 1) % 4
    choices, distractor_why = rotate(options, reasons, correct)
    mode, level = MODES[local - 1], LEVELS[local - 1]
    qid = f"tr-g05-bank-eng-b02-q{local:03d}"
    if mode == "comprehension":
        stem = (
            f"İki ileti okunuyor. I: “{first[1]}” II: “{second[1]}” "
            f"I için görev “{first[2]}”, II için görev “{second[2]}” biçimindedir. İki görevi de doğru çözen seçenek hangisidir?"
        )
        fig = None
    elif mode == "application":
        if local >= 50:
            stem = (
                f"Bir öğrenci I. ileti için “{first[1]}”, II. ileti için “{second[1]}” notlarını alıyor. "
                "Notları iki ayrı iletişim kartına doğru uygulamak için hangi çözüm çifti seçilmelidir?"
            )
        else:
            stem = (
                f"I. durumda şu İngilizce ileti kullanılıyor: “{first[1]}” II. durumda ise “{second[1]}” "
                "iletisi kullanılıyor. Her duruma uygun anlam veya karşılığı veren çözüm çifti hangisidir?"
            )
        fig = None
    elif mode == "analysis":
        stem = (
            f"Aşağıdaki tabloda iki İngilizce ileti verilmiştir. I. ileti için {first[2].casefold()} "
            f"II. ileti için {second[2].casefold()} İki çözümleme sonucunu birlikte doğru veren seçenek hangisidir?"
        )
        fig = table(qid, first, second, labels)
    else:
        mistaken_a = first[4][variant % 3]
        mistaken_b = second[4][(variant + 1) % 3]
        stem = (
            f"Öğrenci I. ileti için “{mistaken_a}”, II. ileti için “{mistaken_b}” sonucunu yazıyor. "
            "İki bilgi veya dil işlevi yanılgısını da düzelten çözüm çifti hangisidir?"
        )
        fig = None
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "Çözümlenecek iki İngilizce ileti yalnız tabloda birlikte gösterilir.",
        "acceptableKinds": ["table"], "evidenceDimensions": ["I. ileti", "II. ileti"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "İki ileti ve istenen görevler soru metninde eksiksiz verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "İngilizce", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — bütünleşik {mode}",
        "objective": objective, "objectiveId": objective,
        "integratedObjectives": [objective, secondary_objective],
        "noteId": note.get("id"), "noteKey": note.get("id"),
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct],
        "distractorWhy": distractor_why,
        "explanation": f"I. ileti için {first[5]} II. ileti için {second[5]} İki sonuç birlikte doğru seçeneği oluşturur.",
        "level": level,
        "difficultyReason": f"Düzey {level}; iki İngilizce iletiyi birbirine karıştırmadan {mode} biçiminde çözmeyi ve sonuçları tek seçimde birleştirmeyi gerektirir.",
        "questionType": mode, "familyId": f"tr-g05-bank-eng-family-{global_number:03d}",
        "objectiveSource": note.get("objectiveSource"), "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [], "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    existing = [json.loads(line) for line in base.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 500:
        raise RuntimeError("the first 500 grade questions must be regenerated before English batch 02")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    rows = [make(local, note_map, labels) for local in range(1, 101)]
    base.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    base.LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                                  encoding="utf-8", newline="\n")
    print(json.dumps({"englishQuestions": 100, "englishTotal": 130, "gradeTotal": 600}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
