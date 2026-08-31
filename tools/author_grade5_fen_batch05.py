#!/usr/bin/env python3
"""Author the final 70 Grade 5 science questions (401–470)."""
from __future__ import annotations

import json
from typing import Any

import author_grade5_fen_batch01 as b1
import author_grade5_fen_batch02 as b2


MODES = ["comprehension"] * 18 + ["application"] * 24 + ["analysis"] * 18 + ["error-analysis"] * 10
LEVELS = (
    [1] * 10 + [2] * 8 +
    [1] * 4 + [2] * 10 + [3] * 10 +
    [3] * 8 + [4] * 7 + [5] * 3 +
    [3] * 3 + [4] * 7
)


def evidence_options(first: tuple[Any, ...], second: tuple[Any, ...], variant: int) -> tuple[list[str], list[str]]:
    options = [
        f"İddia: {first[1]} Kanıt: {first[4]}",
        f"İddia: {first[2][variant % 3]} Kanıt: {first[4]}",
        f"İddia: {second[1]} Kanıt: {first[4]}",
        f"İddia: {second[2][(variant + 1) % 3]} Kanıt: {second[4]}",
    ]
    reasons = [
        f"Doğru iddia–kanıt bağı: Gözlem ilk iddiayı doğrudan destekler. {first[5]}",
        f"Kavram yanılgısı: Kanıt gerçek olsa da ona bağlanan iddia bilimsel olarak yanlıştır. {first[5]}",
        f"Kanıt aktarımı yanılgısı: İkinci iddia doğru olabilir ancak burada verilen birinci kanıt bu iddiayı sınamaz. {second[5]}",
        f"Çifte uyumsuzluk: İkinci kaydın gözlemi, yanlış kurulmuş iddiayı desteklemez. {second[5]}",
    ]
    return options, reasons


def rotate(values: list[str], reasons: list[str], target: int) -> tuple[list[str], list[str]]:
    return (
        [*values[1:1 + target], values[0], *values[1 + target:]],
        [*reasons[1:1 + target], reasons[0], *reasons[1 + target:]],
    )


def experiment(qid: str, note: dict[str, Any], context: str, evidence: str,
               labels: dict[str, str]) -> dict[str, Any] | None:
    unit = str(note.get("unitKey") or "")
    prefix = qid.replace("-", ".")
    alt = f"{prefix}.alt"
    evidence_key = f"{prefix}.evidence"
    labels[evidence_key] = evidence
    # Kapalı araç kataloğu yalnız bu anahtar açma-kapama düzeneklerini eksiksiz
    # temsil edebiliyor. Malzeme, kaşık, yün, delikli kart veya devre sembolü
    # isteyen bağlamlar yanıltıcı yaklaşık aparatlarla çizilmez; aşağıdaki
    # diagram() yolu durum ve gözlem kanıtını doğrudan gösterir.
    if unit == "fb-5-6" and "anahtar" in context.casefold() and any(
        marker in context.casefold() for marker in ("kapatıldığında", "açıldığında")
    ):
        labels[alt] = (
            "Bir pil, anahtar ve lambanın kapalı devre oluşturacak biçimde "
            "kablolarla bağlandığı düzenek; anahtarın açık ve kapalı durumu "
            "karşılaştırılır, doğru seçenek işaretlenmez."
        )
        labels[f"{prefix}.battery"] = "Pil"
        labels[f"{prefix}.switch"] = "Anahtar"
        labels[f"{prefix}.lamp"] = "Ampul"
        return {
            "kind": "diagram", "direction": "horizontal", "altTextKey": alt,
            "nodes": [
                {"id": "battery", "labelKey": f"{prefix}.battery", "shape": "rect", "x": 10, "y": 45},
                {"id": "switch", "labelKey": f"{prefix}.switch", "shape": "rect", "x": 42, "y": 45},
                {"id": "lamp", "labelKey": f"{prefix}.lamp", "shape": "circle", "x": 74, "y": 45},
            ],
            "edges": [
                {"from": "battery", "to": "switch", "directed": False, "style": "solid"},
                {"from": "switch", "to": "lamp", "directed": False, "style": "solid"},
                {"from": "lamp", "to": "battery", "directed": False, "style": "solid"},
            ],
        }
    return None


def diagram(qid: str, context: str, evidence: str, labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    alt, ckey, ekey = f"{prefix}.alt", f"{prefix}.context", f"{prefix}.evidence"
    labels[alt] = "İncelenen durumdan gözlem kanıtına giden iki düğümlü akış; doğru iddia gösterilmez."
    labels[ckey], labels[ekey] = context, evidence
    return {
        "kind": "diagram", "direction": "horizontal", "altTextKey": alt,
        "nodes": [
            {"id": "context", "labelKey": ckey, "shape": "rect", "x": 10, "y": 42},
            {"id": "evidence", "labelKey": ekey, "shape": "rect", "x": 58, "y": 42},
        ],
        "edges": [{"from": "context", "to": "evidence", "directed": True, "style": "solid"}],
    }


def make(local: int, labels: dict[str, str]) -> dict[str, Any]:
    global_number = 400 + local
    index = (local * 5 + 3) % len(b1.KNOWLEDGE)
    first, second = b1.KNOWLEDGE[index], b2.KNOWLEDGE[index]
    note_id = first[0]
    note = b1.NOTE_BY_ID[note_id]
    objective = str((note.get("objectives") or [""])[0])
    mode, level = MODES[local - 1], LEVELS[local - 1]
    correct = (global_number - 1) % 4
    raw_choices, raw_reasons = evidence_options(first, second, local)
    choices, reasons = rotate(raw_choices, raw_reasons, correct)
    qid = f"tr-g05-bank-fen-b05-q{local:03d}"
    if mode == "comprehension":
        stem = (
            f"{note['title']} konusunda bir iddianın bilimsel kanıtla desteklenmesi isteniyor. "
            f"İncelenen durum şudur: {first[3]} Hangi iddia–kanıt çifti kendi içinde tutarlıdır?"
        )
        fig = None
    elif mode == "application":
        stem = (
            f"Bir öğrenci şu durumu çözüm kartına aktaracak: {first[3]} Başka bir kayıt da şu "
            f"durumu içeriyor: {second[3]} {note['title']} bilgisi uygulandığında hangi kart "
            "iddiasını gerçekten kendi kanıtıyla eşleştirir?"
        )
        fig = None
    elif mode == "analysis":
        fig = experiment(qid, note, first[3], first[4], labels) or diagram(qid, first[3], first[4], labels)
        kind_name = "deney düzeneği" if fig["kind"] == "experiment" else "kanıt diyagramı"
        visual_instruction = (
            "Aşağıdaki deney düzeneğini inceleyiniz."
            if fig["kind"] == "experiment"
            else "Aşağıdaki diyagramı inceleyiniz."
        )
        stem = (
            f"{visual_instruction} {kind_name.capitalize()}, {note['title']} konusunda “{first[3]}” "
            "durumundan elde edilen gözlemi gösterir. Düzeneği veya diyagramı doğru yorumlayan iddia–kanıt çifti hangisidir?"
        )
    else:
        mistaken = raw_choices[1 + local % 3]
        stem = (
            f"Bir öğrenci {note['title']} için şu eşleştirmeyi yapıyor: “{mistaken}” "
            "Bu eşleştirmedeki yanılgıyı gideren ve kanıtı doğru iddiaya bağlayan seçenek hangisidir?"
        )
        fig = None
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "Araç yerleşimi veya durum-gözlem bağlantısı yalnız görselde gösterilir.",
        "acceptableKinds": [fig["kind"]], "evidenceDimensions": ["düzenek", "gözlem"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "Gerekli durum ve iddia–kanıt çiftleri metinde verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "Fen Bilimleri", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — iddia ve kanıt {mode}",
        "objective": objective, "objectiveId": objective, "noteId": note_id, "noteKey": note_id,
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct],
        "distractorWhy": reasons,
        "explanation": f"Doğru eşleştirmede iddia ile gözlem aynı ilişkiyi anlatır. {first[5]}",
        "level": level,
        "difficultyReason": f"Düzey {level}; iddia ile gözlemi birbirinden ayırıp aralarındaki kanıt bağını {mode} düzeyinde sınamayı gerektirir.",
        "questionType": mode, "familyId": f"tr-g05-bank-fen-family-{global_number:03d}",
        "objectiveSource": note.get("objectiveSource"), "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [], "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    b1.NOTE_BY_ID = b1.read_notes()
    existing = [json.loads(line) for line in b1.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 400:
        raise RuntimeError("batches 01–04 must be regenerated before the final science segment")
    labels = json.loads(b1.LABELS_OUTPUT.read_text(encoding="utf-8"))
    rows = [make(local, labels) for local in range(1, 71)]
    b1.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    b1.LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                                encoding="utf-8", newline="\n")
    print(json.dumps({"questions": 70, "scienceTotal": 470, "gradeTotal": 470}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
