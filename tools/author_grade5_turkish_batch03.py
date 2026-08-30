#!/usr/bin/env python3
"""Author 68 remaining-pair and 32 triple Turkish questions (grade rows 1801-1900)."""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from typing import Any

import author_grade5_turkish_segment01 as base
import author_grade5_turkish_batch02 as second


def remaining_pairs() -> list[tuple[int, int]]:
    excluded = set(base.balanced_pairs()) | set(second.pair_set())
    values = [value for value in combinations(range(len(base.NOTE_IDS)), 2) if value not in excluded]
    if len(values) != 68:
        raise RuntimeError("exactly 68 Turkish topic pairs must remain")
    return sorted(values, key=lambda value: sha256(("-".join(map(str, value)) + "-alika-tur-b03").encode()).hexdigest())


def triple_set() -> list[tuple[int, int, int]]:
    values = sorted(
        combinations(range(len(base.NOTE_IDS)), 3),
        key=lambda value: sha256(("-".join(map(str, value)) + "-alika-tur-b03-triple").encode()).hexdigest(),
    )[:32]
    if len(values) != 32 or len(set(values)) != 32:
        raise RuntimeError("Turkish batch 03 triple set is invalid")
    return values


def triple_table(qid: str, titles: list[str], cases: list[tuple[str, str, list[str], str]], labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, h3, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.h3", f"{prefix}.alt"
    labels[h1], labels[h2], labels[h3] = "Görev", "Türkçe becerisi", "Metin veya ileti"
    labels[alt] = "Üç Türkçe becerisine ait I, II ve III metin/ileti görevlerini gösteren tablo; doğru yanıtlar belirtilmemiştir."
    return {
        "kind": "table", "headerKeys": [h1, h2, h3], "altTextKey": alt,
        "rows": [[{"v": label}, {"v": title}, {"v": case[0]}] for label, title, case in zip(("I", "II", "III"), titles, cases)],
    }


def triple_make(
    local: int,
    selected: tuple[int, int, int],
    note_map: dict[str, dict[str, Any]],
    labels: dict[str, str],
    *,
    global_base: int = 1800,
    batch_id: str = "b03",
) -> dict[str, Any]:
    global_number = global_base + local
    variant = (local - 1) // 8
    cases = [base.CASES[index] for index in selected]
    notes_for_task = [note_map[base.NOTE_IDS[index]] for index in selected]
    objectives = [str((note.get("objectives") or [""])[0]) for note in notes_for_task]
    correct_values = [case[1] for case in cases]
    wrong_values = [case[2][(variant + index) % 3] for index, case in enumerate(cases)]

    def line(values: list[str]) -> str:
        return " || ".join(f"{label} — {value}" for label, value in zip(("I", "II", "III"), values))

    raw_choices = [
        line(correct_values),
        line([wrong_values[0], correct_values[1], correct_values[2]]),
        line([correct_values[0], wrong_values[1], correct_values[2]]),
        line([correct_values[0], correct_values[1], wrong_values[2]]),
    ]
    raw_reasons = [
        "Doğru üç-beceri çözümü: " + " ".join(case[3] for case in cases),
        f"Birinci görevde metin kanıtı yanılgısı: I. yanıt bağlam veya amacı bozar; II ve III doğrudur. {cases[0][3]}",
        f"İkinci görevde dil işlevi yanılgısı: II. yanıt kendi metniyle doğrulanamaz; I ve III doğrudur. {cases[1][3]}",
        f"Üçüncü görevde yapı yanılgısı: III. yanıt tür, konuşma veya yazma koşulunu değiştirir; I ve II doğrudur. {cases[2][3]}",
    ]
    correct = (global_number - 1) % 4
    choices, distractor_why = base.shared.shared.rotate(raw_choices, raw_reasons, correct)
    mode, level = base.FULL_MODES[local - 1], base.FULL_LEVELS[local - 1]
    qid = f"tr-g05-bank-tur-{batch_id}-q{local:03d}"
    titles = [str(note["title"]) for note in notes_for_task]
    if mode == "comprehension":
        stem = (
            "Üç Türkçe görevinin temel anlamları karşılaştırılıyor. "
            + " ".join(f"{label}: {case[0]}" for label, case in zip(("I", "II", "III"), cases))
            + " Üç metin veya iletiyi doğru yorumlayan yanıt dizisi hangisidir?"
        )
        fig = None
    elif mode == "application":
        stem = (
            "Üç Türkçe görevi ayrı ürün veya konuşmalarda uygulanacaktır. "
            + " ".join(f"{label}: {case[0]}" for label, case in zip(("I", "II", "III"), cases))
            + " Üç görevi de amacına uygun tamamlayan yanıt dizisi hangisidir?"
        )
        fig = None
    elif mode == "analysis":
        stem = (
            f"Aşağıdaki tabloda {titles[0].casefold()}, {titles[1].casefold()} ve {titles[2].casefold()} "
            "becerilerine ait üç kayıt vardır. Metin ve ileti kanıtlarını çözümleyip üç doğru yanıtı veren seçenek hangisidir?"
        )
        fig = triple_table(qid, titles, cases, labels)
    else:
        stem = (
            "Bir öğrenci üç görev için şu yanıtları veriyor: "
            + " ".join(f"{label}: {wrong}" for label, wrong in zip(("I", "II", "III"), wrong_values))
            + " Görevler "
            + " ".join(f"{label}: {case[0]}" for label, case in zip(("I", "II", "III"), cases))
            + " biçimindedir. Üç dil yanılgısını da düzelten yanıt dizisi hangisidir?"
        )
        fig = None
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "Üç metin/ileti görevi ve bağlı Türkçe becerileri yalnız tabloda birlikte gösterilir.",
        "acceptableKinds": ["table"], "evidenceDimensions": ["görev", "Türkçe becerisi", "metin veya ileti"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "Üç Türkçe görevinin metinleri ve değerlendirme koşulları soru metninde verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    note = notes_for_task[0]
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "Türkçe", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — üç beceri {mode}",
        "objective": objectives[0], "objectiveId": objectives[0], "integratedObjectives": objectives,
        "noteId": note.get("id"), "noteKey": note.get("id"),
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct], "distractorWhy": distractor_why,
        "explanation": " ".join(f"{label}. görev için {case[3]}" for label, case in zip(("I", "II", "III"), cases)),
        "level": level,
        "difficultyReason": f"Düzey {level}; üç Türkçe becerisini {mode} biçiminde ayrı metin kanıtlarına uygulayıp yanıtları tek seçimde birleştirmeyi gerektirir.",
        "questionType": mode, "familyId": f"tr-g05-bank-tur-family-{global_number:03d}",
        "objectiveSource": note.get("objectiveSource"), "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [], "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    existing = [json.loads(line) for line in base.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1800:
        raise RuntimeError("the first 1800 grade questions must be regenerated before Turkish batch 03")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    rows = [
        base.make(local, selected, note_map, labels, global_base=1800, batch_id="b03", schedule_offset=0)
        for local, selected in enumerate(remaining_pairs(), 1)
    ]
    rows.extend(triple_make(local, selected, note_map, labels) for local, selected in enumerate(triple_set(), 69))
    if len(rows) != 100:
        raise RuntimeError("Turkish batch 03 must contain exactly 100 questions")
    base.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    base.LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"turkishQuestions": 100, "turkishTotal": 263, "gradeTotal": 1900}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
