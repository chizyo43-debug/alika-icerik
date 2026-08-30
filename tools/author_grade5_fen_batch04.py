#!/usr/bin/env python3
"""Author Grade 5 science batch 04 with paired-evidence decision tasks."""
from __future__ import annotations

import json
from typing import Any

import author_grade5_fen_batch01 as b1
import author_grade5_fen_batch02 as b2


def pair_options(first: tuple[Any, ...], second: tuple[Any, ...], variant: int) -> tuple[list[str], list[str]]:
    fact_a, wrong_a = first[1], first[2]
    fact_b, wrong_b = second[1], second[2]
    pairs = [
        (fact_a, fact_b),
        (wrong_a[variant % 3], fact_b),
        (fact_a, wrong_b[(variant + 1) % 3]),
        (wrong_a[(variant + 2) % 3], wrong_b[variant % 3]),
    ]
    if variant % 2:
        options = [f"I. sonuç: {a} II. sonuç: {b}" for a, b in pairs]
    else:
        options = [f"İlk kaydı “{a}” ilkesiyle; ikinci kaydı “{b}” ilkesiyle açıklamak." for a, b in pairs]
    reasons = [
        f"Doğru iki-kayıt kararı: İlk kayıt için {first[5]} İkinci kayıt için {second[5]}",
        f"Birinci-kayıt yanılgısı: İlk açıklama bilimsel ilkeyi bozarken ikinci açıklama doğrudur. İlk kayıt için {first[5]}",
        f"İkinci-kayıt yanılgısı: İlk açıklama doğru olsa da ikinci açıklama gözlemle uyuşmaz. İkinci kayıt için {second[5]}",
        f"Çifte yanılgı: Her iki açıklama da kendi gözlem zinciriyle çelişir. Doğru ilkeler sırasıyla şunlardır: {first[5]} {second[5]}",
    ]
    return options, reasons


def diagram(qid: str, first: tuple[Any, ...], second: tuple[Any, ...], labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    alt = f"{prefix}.alt"
    labels[alt] = "İki bağımsız araştırmada durumdan gözleme ilerleyen iki paralel kanıt zinciri; doğru sonuç gösterilmez."
    nodes = []
    for node_id, x, y, value in (
        ("i-durum", 8, 18, first[3]), ("i-gozlem", 55, 18, first[4]),
        ("ii-durum", 8, 70, second[3]), ("ii-gozlem", 55, 70, second[4]),
    ):
        key = f"{prefix}.{node_id}"
        labels[key] = value
        nodes.append({"id": node_id, "labelKey": key, "shape": "rect", "x": x, "y": y})
    return {
        "kind": "diagram", "direction": "horizontal", "altTextKey": alt,
        "nodes": nodes,
        "edges": [
            {"from": "i-durum", "to": "i-gozlem", "directed": True, "style": "solid"},
            {"from": "ii-durum", "to": "ii-gozlem", "directed": True, "style": "solid"},
        ],
    }


def rotate(values: list[Any], reasons: list[str], target: int) -> tuple[list[Any], list[str]]:
    correct_value, correct_reason = values[0], reasons[0]
    wrong_values, wrong_reasons = values[1:], reasons[1:]
    return (
        [*wrong_values[:target], correct_value, *wrong_values[target:]],
        [*wrong_reasons[:target], correct_reason, *wrong_reasons[target:]],
    )


def make(local: int, labels: dict[str, str]) -> dict[str, Any]:
    global_number = 300 + local
    index = (local - 1) % len(b1.KNOWLEDGE)
    first, second = b1.KNOWLEDGE[index], b2.KNOWLEDGE[index]
    note_id = first[0]
    note = b1.NOTE_BY_ID[note_id]
    objective = str((note.get("objectives") or [""])[0])
    mode, level = b1.MODE_SEQUENCE[local - 1], b1.LEVEL_SEQUENCE[local - 1]
    correct = (global_number - 1) % 4
    variant = (local - 1) // len(b1.KNOWLEDGE)
    raw_options, raw_reasons = pair_options(first, second, variant)
    choices, reasons = rotate(raw_options, raw_reasons, correct)
    qid = f"tr-g05-bank-fen-b04-q{local:03d}"
    if mode == "comprehension":
        stem = (
            f"{note['title']} için iki bilgi özeti karşılaştırılıyor. İlk özet şu duruma aittir: {first[3]} "
            f"İkinci özet ise şu duruma aittir: {second[3]} İki özeti de bilimsel "
            "olarak doğru tamamlayan seçenek hangisidir?"
        )
        fig = None
    elif mode == "application":
        if local >= 54:
            stem = (
                f"Bir uygulama formunda ilk gözlem “{first[4]}”, ikinci gözlem “{second[4]}” olarak "
                f"kaydediliyor. {note['title']} bilgisi iki kayda ayrı ayrı uygulandığında hangi karar çifti seçilmelidir?"
            )
        else:
            stem = (
                f"Bir ekip iki durumda karar verecek: I. {first[3]} II. {second[3]} "
                f"{note['title']} bilgisi her duruma doğru uygulandığında hangi karar çifti oluşur?"
            )
        fig = None
    elif mode == "analysis":
        stem = (
            f"Aşağıdaki diyagramda {note['title']} konusunda iki paralel durum-gözlem zinciri gösterilmiştir. "
            f"Birinci zincirin odağı “{first[3]}”, ikinci zincirin odağı ise "
            f"“{second[3]}” durumudur. İki zinciri birlikte doğru yorumlayan seçenek hangisidir?"
        )
        fig = diagram(qid, first, second, labels)
    else:
        mistaken_a = first[2][local % 3]
        mistaken_b = second[2][(local + 1) % 3]
        stem = (
            f"Öğrenci ilk kayıt için “{mistaken_a}”, ikinci kayıt için “{mistaken_b}” diyor. "
            f"{note['title']} açısından iki yanılgıyı da düzelten karar çifti hangisidir?"
        )
        fig = None
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "İki bağımsız durum-gözlem zincirinin bağlantıları yalnız diyagramda gösterilir.",
        "acceptableKinds": ["diagram"], "evidenceDimensions": ["durum", "gözlem", "bağlantı"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "İki durum ve karar için gerekli bilgiler soru metninde verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "Fen Bilimleri", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — karar çifti {mode}",
        "objective": objective, "objectiveId": objective,
        "noteId": note_id, "noteKey": note_id,
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct],
        "distractorWhy": reasons,
        "explanation": f"İlk kayıt için {first[5]} İkinci kayıt için {second[5]} Bu iki doğrulama birlikte doğru seçeneği verir.",
        "level": level,
        "difficultyReason": f"Düzey {level}; iki farklı kanıt zincirine aynı kazanımın farklı alt bilgilerini {mode} biçiminde uygulamayı gerektirir.",
        "questionType": mode, "familyId": f"tr-g05-bank-fen-family-{global_number:03d}",
        "objectiveSource": note.get("objectiveSource"), "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [], "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    b1.NOTE_BY_ID = b1.read_notes()
    existing = [json.loads(line) for line in b1.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 300:
        raise RuntimeError("batches 01–03 must be regenerated before batch 04")
    labels = json.loads(b1.LABELS_OUTPUT.read_text(encoding="utf-8"))
    rows = [make(local, labels) for local in range(1, 101)]
    b1.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    b1.LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                                encoding="utf-8", newline="\n")
    print(json.dumps({"questions": 100, "total": 400}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
