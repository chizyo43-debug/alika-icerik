#!/usr/bin/env python3
"""Finish the Grade 5 mathematics quota with 87 questions (grade rows 1201-1287)."""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from typing import Any

import author_grade5_math_segment01 as base
import author_grade5_math_batch02 as data
import author_grade5_math_batch03 as paired
import author_grade5_math_batch04 as second


def remaining_pairs() -> list[tuple[int, int]]:
    ordered = sorted(
        combinations(range(len(data.NOTE_IDS)), 2),
        key=lambda value: sha256(("-".join(map(str, value)) + "-alika-mat-b03").encode()).hexdigest(),
    )
    values = ordered[200:]
    if len(values) != 53 or set(values) & set(second.second_pair_set()):
        raise RuntimeError("remaining mathematics pair set is invalid")
    return values


def triple_set() -> list[tuple[int, int, int]]:
    values = sorted(
        combinations(range(len(data.NOTE_IDS)), 3),
        key=lambda value: sha256(("-".join(map(str, value)) + "-alika-mat-b05").encode()).hexdigest(),
    )[:34]
    if len(values) != 34 or len(set(values)) != 34:
        raise RuntimeError("mathematics triple set is invalid")
    return values


def triple_table(
    qid: str,
    titles: list[str],
    cases: list[tuple[str, str, list[str], str]],
    labels: dict[str, str],
) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, h3, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.h3", f"{prefix}.alt"
    labels[h1], labels[h2], labels[h3] = "Görev", "Konu anlatımı", "Veri kaydı"
    labels[alt] = "Üç farklı matematik konusuna ait I, II ve III veri kayıtlarını gösteren tablo; doğru çözümler belirtilmemiştir."
    return {
        "kind": "table", "headerKeys": [h1, h2, h3], "altTextKey": alt,
        "rows": [
            [{"v": label}, {"v": title}, {"v": case[0]}]
            for label, title, case in zip(("I", "II", "III"), titles, cases)
        ],
    }


def triple_make(
    local: int,
    selected: tuple[int, int, int],
    note_map: dict[str, dict[str, Any]],
    labels: dict[str, str],
) -> dict[str, Any]:
    global_number = 1200 + local
    variant = (local - 54) // 6
    cases = [data.case_data(index, variant + offset * 2) for offset, index in enumerate(selected)]
    notes = [note_map[data.NOTE_IDS[index]] for index in selected]
    objectives = [
        str((note.get("objectives") or [""])[variant % len(note.get("objectives") or [""])])
        for note in notes
    ]
    correct_values = [case[1] for case in cases]
    wrong_values = [case[2][(variant + index) % 3] for index, case in enumerate(cases)]

    def line(values: list[str]) -> str:
        return " || ".join(f"{label}. görev — {value}" for label, value in zip(("I", "II", "III"), values))

    raw_choices = [
        line(correct_values),
        line([wrong_values[0], correct_values[1], correct_values[2]]),
        line([correct_values[0], wrong_values[1], correct_values[2]]),
        line([correct_values[0], correct_values[1], wrong_values[2]]),
    ]
    raw_reasons = [
        "Doğru üç-model denetimi: " + " ".join(case[3] for case in cases),
        f"Birinci görevde kavram yanılgısı: I. çözüm konu kuralını değiştirir; II ve III doğrudur. {cases[0][3]}",
        f"İkinci görevde işlem yanılgısı: II. çözüm kendi verisiyle doğrulanamaz; I ve III doğrudur. {cases[1][3]}",
        f"Üçüncü görevde temsil yanılgısı: III. çözüm koşul veya birimi bozar; I ve II doğrudur. {cases[2][3]}",
    ]
    correct = (global_number - 1) % 4
    choices, distractor_why = base.rotate(raw_choices, raw_reasons, correct)
    mode, level = paired.MODES[local - 1], paired.LEVELS[local - 1]
    qid = f"tr-g05-bank-mat-b05-q{local:03d}"
    titles = [str(note["title"]) for note in notes]
    if mode == "application":
        stem = (
            "Bir konu tarama uygulamasında üç bağımsız problem çözülüyor. "
            + " ".join(f"{label}: {case[0]}" for label, case in zip(("I", "II", "III"), cases))
            + " Üç veriyi kendi matematiksel modeline doğru aktaran sonuç dizisi hangisidir?"
        )
        fig = None
    elif mode == "analysis":
        stem = (
            f"Aşağıdaki tabloda '{titles[0]}', '{titles[1]}' ve '{titles[2]}' konularından üç kayıt vardır. "
            "Her kaydı kendi kuralıyla çözümleyip üç doğru sonucu birlikte veren seçenek hangisidir?"
        )
        fig = triple_table(qid, titles, cases, labels)
    else:
        stem = (
            "Bir öğrenci üç problem için şu sonuçları yazıyor: "
            + " ".join(f"{label}: {wrong}" for label, wrong in zip(("I", "II", "III"), wrong_values))
            + " Veriler ise "
            + " ".join(f"{label}: {case[0]}" for label, case in zip(("I", "II", "III"), cases))
            + " biçimindedir. Üç yanılgıyı da düzelten sonuç dizisi hangisidir?"
        )
        fig = None
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "Üç bağımsız matematiksel veri kaydı ve konu eşleşmesi yalnız tabloda gösterilir.",
        "acceptableKinds": ["table"], "evidenceDimensions": ["görev", "konu", "veri kaydı"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "Üç problemin bütün verileri ve çözüm koşulları soru metninde verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    note = notes[0]
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "Matematik", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — üç görev {mode}",
        "objective": objectives[0], "objectiveId": objectives[0],
        "integratedObjectives": objectives,
        "noteId": note.get("id"), "noteKey": note.get("id"),
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct],
        "distractorWhy": distractor_why,
        "explanation": " ".join(f"{label}. kayıt için {case[3]}" for label, case in zip(("I", "II", "III"), cases)),
        "level": level,
        "difficultyReason": f"Düzey {level}; üç farklı matematik kaydını {mode} biçiminde bağımsız modelleyip sonuçları tek seçimde birleştirmeyi gerektirir.",
        "questionType": mode, "familyId": f"tr-g05-bank-mat-family-{global_number:03d}",
        "objectiveSource": note.get("objectiveSource"),
        "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [], "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    existing = [json.loads(line) for line in base.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1200:
        raise RuntimeError("the first 1200 grade questions must be regenerated before math batch 05")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    rows = [
        paired.make(local, selected, note_map, labels, global_base=1200, batch_id="b05")
        for local, selected in enumerate(remaining_pairs(), 1)
    ]
    rows.extend(
        triple_make(local, selected, note_map, labels)
        for local, selected in enumerate(triple_set(), 54)
    )
    if len(rows) != 87:
        raise RuntimeError("math quota tail must contain exactly 87 questions")
    base.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    base.LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"mathQuestions": 87, "mathTotal": 402, "gradeTotal": 1287}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
