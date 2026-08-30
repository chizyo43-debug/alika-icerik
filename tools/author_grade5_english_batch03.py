#!/usr/bin/env python3
"""Author 100 Grade 5 English editing-feedback questions (grade rows 601-700)."""
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

# These are instructional settings, not cosmetic names.  Each setting changes
# why the learner edits the two records and therefore keeps repeated language
# functions from becoming the same question skeleton.
WORKFLOWS = [
    ("Bir dinleme günlüğünde kaynak ayrıntıları ile öğrencinin tuttuğu notlar karşılaştırılıyor.", "dinleme günlüğü"),
    ("Okul duyuru panosuna asılmadan önce iki İngilizce bilgi kartı kaynak kayıtlarla karşılaştırılıyor.", "duyuru panosu"),
    ("Haftalık ders çizelgesindeki iki kayıt, öğrencinin İngilizce aktarım cümleleriyle denetleniyor.", "çizelge denetimi"),
    ("Akran değerlendirmesinde iki taslağın kişi, yer, zaman ve iletişim amacı ayrı ayrı inceleniyor.", "akran geri bildirimi"),
    ("Dijital sınıf posterindeki iki İngilizce bölüm, yayımlanmadan önce özgün iletilerle karşılaştırılıyor.", "poster düzeltmesi"),
    ("Ödev kontrol listesinde öğrencinin iki kaynak için yazdığı sonuçların kanıta dayanıp dayanmadığı sınanıyor.", "ödev kontrolü"),
    ("Kulüp bilgi formundaki iki İngilizce kayıt, yanlış yönlendirme oluşturmaması için kaynakla doğrulanıyor.", "kulüp formu"),
    ("Diyalog provasında iki konuşma kartının bağlama uygun karşılık verip vermediği değerlendiriliyor.", "diyalog provası"),
    ("Sınıf bilgi köşesindeki iki kısa metin, ana düşünce ve ayrıntı korunarak yeniden düzenleniyor.", "bilgi köşesi"),
    ("Gezi planı dosyasındaki iki İngilizce notta zaman, yer ve amaç bilgilerinin değişip değişmediği aranıyor.", "gezi planı"),
    ("Günlük rutin çizelgesine aktarılmış iki cümlede sıklık ve zaman ifadeleri kaynaklarla eşleştiriliyor.", "rutin çizelgesi"),
    ("Menü ve sipariş kartlarındaki iki İngilizce ifade, tercih bildirme işlevine göre gözden geçiriliyor.", "sipariş kartı"),
    ("Fen gözlem panosuna yazılan iki İngilizce sonuç, kaynak canlı veya uzay bilgileriyle karşılaştırılıyor.", "gözlem panosu"),
]


def paired_items(local: int) -> tuple[tuple[Any, ...], tuple[Any, ...]]:
    """Select two different language functions from one thematic unit."""
    unit = (local - 1) % 8
    variant = (local - 1) // 8
    group = base.ITEMS[unit * 3:unit * 3 + 3]
    # Traverse every ordered pair before returning to the same pairing.  The
    # accompanying workflow and draft state then make later cycles distinct.
    first_index, second_index = ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1))[variant % 6]
    return group[first_index], group[second_index]


def draft_for(item: tuple[Any, ...], variant: int, offset: int) -> str:
    """Create a plausible student draft; some drafts are already correct."""
    if (variant + offset) % 4 == 0:
        return str(item[3])
    wrongs = item[4]
    return str(wrongs[(variant + offset) % 3])


def feedback_options(
    first: tuple[Any, ...], second: tuple[Any, ...], variant: int, workflow_label: str
) -> tuple[list[str], list[str]]:
    correct_a, wrong_a = str(first[3]), first[4]
    correct_b, wrong_b = str(second[3]), second[4]
    bad_a = str(wrong_a[(variant + 1) % 3])
    bad_b = str(wrong_b[(variant + 2) % 3])
    other_a = str(wrong_a[(variant + 2) % 3])
    other_b = str(wrong_b[variant % 3])
    choices = [
        f"{workflow_label} kaydı: I'i '{correct_a}', II'yi '{correct_b}' biçiminde düzenle.",
        f"{workflow_label} kaydı: I'i '{bad_a}', II'yi '{correct_b}' biçiminde düzenle.",
        f"{workflow_label} kaydı: I'i '{correct_a}', II'yi '{bad_b}' biçiminde düzenle.",
        f"{workflow_label} kaydı: I'i '{other_a}', II'yi '{other_b}' biçiminde düzenle.",
    ]
    reasons = [
        f"Doğru çift düzeltme: I için {first[5]} II için {second[5]}",
        f"I. kartta bilgi değiştirme yanılgısı: İlk öneri kaynak iletideki kişi, yer, zaman ya da amacı korumaz. I için {first[5]}",
        f"II. kartta dil işlevi yanılgısı: İkinci öneri kaynak iletinin istediği karşılığı vermez. II için {second[5]}",
        f"İki kartta dayanaksız düzeltme yanılgısı: Önerilerin ikisi de kendi kaynağındaki kanıtı değiştirir. I için {first[5]} II için {second[5]}",
    ]
    return choices, reasons


def rotate(values: list[str], reasons: list[str], target: int) -> tuple[list[str], list[str]]:
    return (
        [*values[1:1 + target], values[0], *values[1 + target:]],
        [*reasons[1:1 + target], reasons[0], *reasons[1 + target:]],
    )


def diagram(
    qid: str,
    first: tuple[Any, ...],
    second: tuple[Any, ...],
    draft_a: str,
    draft_b: str,
    labels: dict[str, str],
) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    keys = {
        "source-a": f"{prefix}.source-a",
        "draft-a": f"{prefix}.draft-a",
        "source-b": f"{prefix}.source-b",
        "draft-b": f"{prefix}.draft-b",
        "alt": f"{prefix}.alt",
    }
    labels[keys["source-a"]] = f"I. kaynak: {first[1]}"
    labels[keys["draft-a"]] = f"I. öğrenci taslağı: {draft_a}"
    labels[keys["source-b"]] = f"II. kaynak: {second[1]}"
    labels[keys["draft-b"]] = f"II. öğrenci taslağı: {draft_b}"
    labels[keys["alt"]] = (
        "İki İngilizce kaynak ileti ile bunlara bağlı iki öğrenci taslağını oklarla gösteren "
        "diyagram; doğruluk veya doğru düzeltme işaretlenmemiştir."
    )
    return {
        "kind": "diagram",
        "direction": "horizontal",
        "altTextKey": keys["alt"],
        "nodes": [
            {"id": "source-a", "labelKey": keys["source-a"], "shape": "rect", "x": 8, "y": 18},
            {"id": "draft-a", "labelKey": keys["draft-a"], "shape": "rect", "x": 57, "y": 18},
            {"id": "source-b", "labelKey": keys["source-b"], "shape": "rect", "x": 8, "y": 72},
            {"id": "draft-b", "labelKey": keys["draft-b"], "shape": "rect", "x": 57, "y": 72},
        ],
        "edges": [
            {"from": "source-a", "to": "draft-a", "directed": True, "style": "solid"},
            {"from": "source-b", "to": "draft-b", "directed": True, "style": "solid"},
        ],
    }


def make(local: int, note_map: dict[str, dict[str, Any]], labels: dict[str, str]) -> dict[str, Any]:
    global_number = 600 + local
    variant = (local - 1) // 8
    first, second = paired_items(local)
    workflow_intro, workflow_label = WORKFLOWS[variant]
    draft_a = draft_for(first, variant, 0)
    draft_b = draft_for(second, variant, 2)
    note, secondary_note = note_map[first[0]], note_map[second[0]]
    objective = str((note.get("objectives") or [""])[0])
    secondary_objective = str((secondary_note.get("objectives") or [""])[0])
    options, reasons = feedback_options(first, second, variant, workflow_label)
    correct = (global_number - 1) % 4
    choices, distractor_why = rotate(options, reasons, correct)
    mode, level = MODES[local - 1], LEVELS[local - 1]
    qid = f"tr-g05-bank-eng-b03-q{local:03d}"

    if mode == "comprehension":
        stem = (
            f"{workflow_intro} I. kaynak ileti '{first[1]}', öğrenci taslağı '{draft_a}' biçimindedir. "
            f"II. kaynak ileti '{second[1]}', öğrenci taslağı '{draft_b}' biçimindedir. "
            "Kaynakların anlamını ve iletişim işlevini koruyan geri bildirim hangisidir?"
        )
        fig = None
    elif mode == "application":
        stem = (
            f"{workflow_intro} I. kartın kaynağı '{first[1]}', taslağı '{draft_a}'; "
            f"II. kartın kaynağı '{second[1]}', taslağı '{draft_b}' olarak verilmiştir. "
            "Öğrenci iki kartı da doğru hâle getirmek için hangi düzenleme yönergesini uygulamalıdır?"
        )
        fig = None
    elif mode == "analysis":
        stem = (
            f"{workflow_intro} Diyagramdaki I. kayıt için görev '{first[2]}', II. kayıt için görev '{second[2]}' biçimindedir. "
            "Kaynak-taslak bağlantılarını çözümleyerek her iki kaydı da doğru düzelten geri bildirim hangisidir?"
        )
        fig = diagram(qid, first, second, draft_a, draft_b, labels)
    else:
        stem = (
            f"{workflow_intro} Öğrenci I. kaynak '{first[1]}' için '{draft_a}', II. kaynak '{second[1]}' için "
            f"'{draft_b}' yazmıştır. Bilgi değiştirme ile dil işlevi yanılgılarını ayrı ayrı kontrol edip "
            "iki kart için de kanıta dayalı düzeltme veren seçenek hangisidir?"
        )
        fig = None

    visual_need = ({
        "level": "required",
        "role": "evidence",
        "rationale": "İki kaynak ileti ile öğrenci taslakları arasındaki bağlantılar yalnız diyagramda gösterilir.",
        "acceptableKinds": ["diagram"],
        "evidenceDimensions": ["kaynak ileti", "öğrenci taslağı", "bağlantı"],
    } if fig else {
        "level": "none",
        "role": "none",
        "rationale": "Kaynak iletiler ve öğrenci taslakları soru metninde eksiksiz verilmiştir.",
        "acceptableKinds": [],
        "evidenceDimensions": [],
    })
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "İngilizce", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — taslak düzeltme {mode}",
        "objective": objective, "objectiveId": objective,
        "integratedObjectives": [objective, secondary_objective],
        "noteId": note.get("id"), "noteKey": note.get("id"),
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct],
        "distractorWhy": distractor_why,
        "explanation": (
            f"I. kayıt için {first[5]} II. kayıt için {second[5]} "
            "Geri bildirim iki kaynakta da kişi, yer, zaman, eylem ve iletişim işlevini korumalıdır."
        ),
        "level": level,
        "difficultyReason": (
            f"Düzey {level}; iki İngilizce kaynak ile öğrenci taslaklarını {mode} biçiminde karşılaştırıp "
            "iki bağımsız düzeltmeyi tek kararda birleştirmeyi gerektirir."
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
    if len(existing) != 600:
        raise RuntimeError("the first 600 grade questions must be regenerated before English batch 03")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    rows = [make(local, note_map, labels) for local in range(1, 101)]
    base.OUTPUT.write_text(
        "\n".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":"))
            for row in [*existing, *rows]
        ) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    base.LABELS_OUTPUT.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"englishQuestions": 100, "englishTotal": 230, "gradeTotal": 700}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
