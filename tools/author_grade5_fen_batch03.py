#!/usr/bin/env python3
"""Author Grade 5 science batch 03 as two-evidence reasoning questions."""
from __future__ import annotations

import json
from typing import Any

import author_grade5_fen_batch01 as b1
import author_grade5_fen_batch02 as b2


COMBO_CHOICES = [
    "Yalnız I numaralı sonuç desteklenir.",
    "Yalnız II numaralı sonuç desteklenir.",
    "I ve II numaralı sonuçların ikisi de desteklenir.",
    "I ve II numaralı sonuçların hiçbiri desteklenmez.",
]


def figure(qid: str, first: tuple[Any, ...], second: tuple[Any, ...],
           claim_i: str, claim_ii: str, labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.alt"
    labels[h1] = "Kanıt kartı"
    labels[h2] = "İçerik"
    labels[alt] = "İki araştırmanın durum, gözlem ve öğrenci sonucu satırlarını gösteren tablo; sonuçların doğruluğu işaretlenmemiştir."
    return {
        "kind": "table", "headerKeys": [h1, h2], "altTextKey": alt,
        "rows": [
            [{"v": "I — Durum"}, {"v": first[3]}],
            [{"v": "I — Gözlem"}, {"v": first[4]}],
            [{"v": "I — Sonuç"}, {"v": claim_i}],
            [{"v": "II — Durum"}, {"v": second[3]}],
            [{"v": "II — Gözlem"}, {"v": second[4]}],
            [{"v": "II — Sonuç"}, {"v": claim_ii}],
        ],
    }


def make(local: int, labels: dict[str, str]) -> dict[str, Any]:
    global_number = 200 + local
    first = b1.KNOWLEDGE[(local - 1) % len(b1.KNOWLEDGE)]
    second = b2.KNOWLEDGE[(local - 1) % len(b2.KNOWLEDGE)]
    note_id, fact_i, wrong_i = first[0], first[1], first[2]
    fact_ii, wrong_ii = second[1], second[2]
    note = b1.NOTE_BY_ID[note_id]
    objective = str((note.get("objectives") or [""])[0])
    mode = b1.MODE_SEQUENCE[local - 1]
    level = b1.LEVEL_SEQUENCE[local - 1]
    correct = (global_number - 1) % 4
    truth_i = correct in (0, 2)
    truth_ii = correct in (1, 2)
    claim_i = fact_i if truth_i else wrong_i[(local - 1) % 3]
    claim_ii = fact_ii if truth_ii else wrong_ii[(local + 1) % 3]
    qid = f"tr-g05-bank-fen-b03-q{local:03d}"
    if mode == "comprehension":
        stem = (
            f"{note['title']} konusunda iki bilgi kartı hazırlanıyor. I. kartta “{claim_i}”, "
            f"II. kartta “{claim_ii}” yazıyor. Konu anlatımına göre hangi değerlendirme doğrudur?"
        )
        fig = None
    elif mode == "application":
        if local >= 54:
            stem = (
                f"Bir denetim formunda I. kanıt “{first[4]}”, II. kanıt “{second[4]}” olarak kaydediliyor. "
                f"Forma I için “{claim_i}”, II için “{claim_ii}” sonuçları ekleniyor. Her sonuç yalnız kendi "
                "kanıt ve bilimsel ilkesiyle sınandığında hangi değerlendirme yapılmalıdır?"
            )
        else:
            stem = (
                f"Birinci uygulamada {first[3]} İkinci uygulamada {second[3]} "
                f"Öğrenciler sırasıyla “{claim_i}” ve “{claim_ii}” sonuçlarını yazıyor. "
                "Gözlem koşulları ve bilimsel bilgiler birlikte kullanıldığında hangi değerlendirme yapılmalıdır?"
            )
        fig = None
    elif mode == "analysis":
        stem = (
            f"Aşağıdaki tabloda {note['title']} ile ilgili iki ayrı araştırmanın kanıt zinciri verilmiştir. "
            f"I. zincir şu duruma dayanır: {first[3]} II. zincir ise şu duruma dayanır: "
            f"{second[3]} Hangi değerlendirme doğrudur?"
        )
        fig = figure(qid, first, second, claim_i, claim_ii, labels)
    else:
        stem = (
            f"Bir öğrenci {note['title']} konusunda iki sonuç yazıyor: I. “{claim_i}” II. “{claim_ii}” "
            "Her sonuç kendi bilimsel anlamıyla denetlendiğinde öğrencinin hata durumunu hangi seçenek doğru gösterir?"
        )
        fig = None
    actual = (truth_i, truth_ii)
    combinations = ((True, False), (False, True), (True, True), (False, False))
    reasons = []
    for index, proposed in enumerate(combinations):
        if proposed == actual:
            reasons.append(
                f"Doğru kanıt değerlendirmesi: I. sonuç {'desteklenir' if truth_i else 'desteklenmez'}, "
                f"II. sonuç {'desteklenir' if truth_ii else 'desteklenmez'}; iki kanıt ayrı ayrı sınanmıştır."
            )
        else:
            errors = []
            if proposed[0] != truth_i:
                errors.append("I. kanıtı ters yorumlar")
            if proposed[1] != truth_ii:
                errors.append("II. kanıtı ters yorumlar")
            reasons.append(
                f"Çift-kanıt yanılgısı: Bu seçenek {' ve '.join(errors)}; iki sonucun doğruluğu birbirinden bağımsız denetlenmelidir."
            )
    explanation = (
        f"I. kayıt için temel bilgi şudur: {first[5]} II. kayıt için temel bilgi şudur: {second[5]} "
        f"Buna göre doğru değerlendirme “{COMBO_CHOICES[correct]}” olur."
    )
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "İki durum, iki gözlem ve iki öğrenci sonucu yalnız tabloda birlikte verilir.",
        "acceptableKinds": ["table"], "evidenceDimensions": ["durum", "gözlem", "sonuç"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "İki iddia ve gerekli bağlam soru metninde eksiksiz verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "Fen Bilimleri", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — iki kanıtlı {mode}",
        "objective": objective, "objectiveId": objective,
        "noteId": note_id, "noteKey": note_id,
        "question": stem, "choices": list(COMBO_CHOICES), "correct": correct,
        "correctIndex": correct, "correctOption": COMBO_CHOICES[correct],
        "distractorWhy": reasons, "explanation": explanation,
        "level": level,
        "difficultyReason": f"Düzey {level}; iki bağımsız kanıt zincirini ayrı doğrulayıp sonuçları {mode} biçiminde birleştirmeyi gerektirir.",
        "questionType": mode, "familyId": f"tr-g05-bank-fen-family-{global_number:03d}",
        "objectiveSource": note.get("objectiveSource"),
        "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [],
        "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    b1.NOTE_BY_ID = b1.read_notes()
    existing = [json.loads(line) for line in b1.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 200 or any(f"-b{1 if i < 100 else 2:02d}-" not in str(row.get("id")) for i, row in enumerate(existing)):
        raise RuntimeError("batches 01 and 02 must be regenerated before batch 03")
    labels = json.loads(b1.LABELS_OUTPUT.read_text(encoding="utf-8"))
    rows = [make(local, labels) for local in range(1, 101)]
    b1.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    b1.LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                                encoding="utf-8", newline="\n")
    print(json.dumps({"questions": 100, "total": 300}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
