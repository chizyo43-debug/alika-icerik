#!/usr/bin/env python3
"""Author 100 additional Grade 5 social studies questions (grade rows 1401-1500)."""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from typing import Any

import author_grade5_social_segment01 as base
import author_grade5_social_batch02 as prior


def remaining_pairs() -> list[tuple[int, int]]:
    ordered = sorted(
        combinations(range(len(prior.NOTE_IDS)), 2),
        key=lambda value: sha256(("-".join(map(str, value)) + "-alika-social-b02").encode()).hexdigest(),
    )
    values = ordered[100:]
    if len(values) != 71 or set(values) & set(prior.pair_set()):
        raise RuntimeError("remaining social studies pairs are invalid")
    return values


def triples() -> list[tuple[int, int, int]]:
    values = sorted(
        combinations(range(len(prior.NOTE_IDS)), 3),
        key=lambda value: sha256(("-".join(map(str, value)) + "-alika-social-b03").encode()).hexdigest(),
    )[:29]
    if len(values) != 29 or len(set(values)) != 29:
        raise RuntimeError("social studies triple set is invalid")
    return values


def triple_table(
    qid: str,
    titles: list[str],
    cases: list[tuple[str, str, list[str], str]],
    labels: dict[str, str],
) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, h3, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.h3", f"{prefix}.alt"
    labels[h1], labels[h2], labels[h3] = "Kayıt", "Konu", "Sosyal durum"
    labels[alt] = "Üç sosyal bilgiler konusuna ait I, II ve III durum kayıtlarını gösteren tablo; doğru yorumlar işaretlenmemiştir."
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
    global_base: int = 1400,
    batch_id: str = "b03",
) -> dict[str, Any]:
    global_number = global_base + local
    variant = (local - 1) // 8
    cases = [prior.case_data(index) for index in selected]
    notes = [note_map[prior.NOTE_IDS[index]] for index in selected]
    objectives = [str((note.get("objectives") or [""])[0]) for note in notes]
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
        "Doğru üç-kanıt yorumu: " + " ".join(case[3] for case in cases),
        f"Birinci durumda bağlam yanılgısı: I. yorum kanıt sınırını aşar; II ve III doğrudur. {cases[0][3]}",
        f"İkinci durumda neden-sonuç yanılgısı: II. yorum durumdan çıkarılamaz; I ve III doğrudur. {cases[1][3]}",
        f"Üçüncü durumda kurum veya kapsam yanılgısı: III. yorum uygun değildir; I ve II doğrudur. {cases[2][3]}",
    ]
    correct = (global_number - 1) % 4
    choices, distractor_why = base.shared.rotate(raw_choices, raw_reasons, correct)
    mode, level = prior.MODES[local - 1], prior.LEVELS[local - 1]
    qid = f"tr-g05-bank-sos-{batch_id}-q{local:03d}"
    titles = [str(note["title"]) for note in notes]
    if mode == "comprehension":
        stem = (
            "Üç sosyal durumun temel kavramları karşılaştırılıyor. "
            + " ".join(f"{label}: {case[0]}" for label, case in zip(("I", "II", "III"), cases))
            + " Her durumu kendi kanıtıyla doğru yorumlayan sonuç dizisi hangisidir?"
        )
        fig = None
    elif mode == "application":
        stem = (
            "Bir sınıf uygulamasında üç duruma ayrı karar veya eylem planı hazırlanacaktır. "
            + " ".join(f"{label}: {case[0]}" for label, case in zip(("I", "II", "III"), cases))
            + " Üç duruma da uygun uygulama dizisi hangisidir?"
        )
        fig = None
    elif mode == "analysis":
        stem = (
            f"Aşağıdaki tabloda {titles[0].casefold()}, {titles[1].casefold()} ve {titles[2].casefold()} "
            "konularından üç durum vardır. Her kaydı kendi kanıt ve kapsamıyla çözümleyip üç doğru yorumu veren seçenek hangisidir?"
        )
        fig = triple_table(qid, titles, cases, labels)
    else:
        stem = (
            "Bir öğrenci üç durum için şu sonuçları yazıyor: "
            + " ".join(f"{label}: {wrong}" for label, wrong in zip(("I", "II", "III"), wrong_values))
            + " Durumlar "
            + " ".join(f"{label}: {case[0]}" for label, case in zip(("I", "II", "III"), cases))
            + " biçimindedir. Üç yanılgıyı da düzelten yorum dizisi hangisidir?"
        )
        fig = None
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "Üç sosyal durum ve bağlı konu başlıkları yalnız tabloda birlikte gösterilir.",
        "acceptableKinds": ["table"], "evidenceDimensions": ["kayıt", "konu", "durum kanıtı"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "Üç durumun iddiaları ve değerlendirme kanıtları soru metninde verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    note = notes[0]
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "Sosyal Bilgiler", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — üç durum {mode}",
        "objective": objectives[0], "objectiveId": objectives[0], "integratedObjectives": objectives,
        "noteId": note.get("id"), "noteKey": note.get("id"),
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct], "distractorWhy": distractor_why,
        "explanation": " ".join(f"{label}. kayıt için {case[3]}" for label, case in zip(("I", "II", "III"), cases)),
        "level": level,
        "difficultyReason": f"Düzey {level}; üç sosyal bilgiler durumunu {mode} biçiminde ayrı kanıtlarla değerlendirip sonuçları tek seçimde birleştirmeyi gerektirir.",
        "questionType": mode, "familyId": f"tr-g05-bank-sos-family-{global_number:03d}",
        "objectiveSource": note.get("objectiveSource"), "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [], "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    existing = [json.loads(line) for line in base.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1400:
        raise RuntimeError("the first 1400 grade questions must be regenerated before social batch 03")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    rows = [
        prior.make(local, selected, note_map, labels, global_base=1400, batch_id="b03")
        for local, selected in enumerate(remaining_pairs(), 1)
    ]
    rows.extend(triple_make(local, selected, note_map, labels) for local, selected in enumerate(triples(), 72))
    if len(rows) != 100:
        raise RuntimeError("social batch 03 must contain exactly 100 questions")
    base.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    base.LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"socialQuestions": 100, "socialTotal": 213, "gradeTotal": 1500}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
