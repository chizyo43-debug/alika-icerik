#!/usr/bin/env python3
"""Append Grade 6 batch 06: 32 DKAB and 68 science questions.

The batch closes the canonical DKAB quota and starts science from a 36-note
case library.  It reads lesson notes only; source questions are never used as
authoring input.  Figure Spec 1.3 diagrams are used where spatial evidence is
the task, charts for numerical trends, and tables for textual evidence.
"""
from __future__ import annotations

import json
from typing import Any

from author_grade6_bilisim_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade6_dkab_batch04 import CASES as DKAB_A
from author_grade6_dkab_batch05 import CASES as DKAB_B
from author_grade6_fen_case_library import FEN_CASES
from author_grade6_mixed_batch03 import (
    DKAB_SOURCE, LEVEL_SEQUENCE, MODE_SEQUENCE, make_question, read_notes_only,
)
from build_unique_question_banks import ROOT


FEN_SOURCE = ROOT / "turkiye/6-sinif/fen-bilimleri/fen-bilimleri-tum.jsonl"
DKAB_POSITIONS = set(range(1, 11)) | set(range(26, 38)) | set(range(86, 96))


def derived_dkab_case(case: tuple[Any, ...], variant: int, mode: str) -> tuple[Any, ...]:
    """Turn an existing note-grounded case into a genuinely new reasoning task."""
    note_id, scenario, evidence, concept, action, inference, wrongs, rationale = case
    wrong0, wrong1, wrong2 = wrongs
    if variant == 0:
        new_scenario = (
            "Bir öğrenci kurulu, konu hakkında hazırlanan değerlendirme ölçütünü "
            "bir vaka ile kaynak kaydını karşılaştırarak sınamak istiyor."
        )
        new_evidence = (
            f"Birinci kayıt şunu bildiriyor: {evidence} İkinci kayıttaki “{wrong0}” "
            "yorumu ise bu bilgiyle açıkça çelişiyor."
        )
        new_concept = f"Vaka ile kaynak kaydının birlikte koruduğu kavram sınırı şudur: {concept}"
        new_action = f"Ölçütü düzeltirken çelişen iddiayı çıkarıp şu adımı uygulamak gerekir: {action}"
        new_inference = f"Bağımsız kayıtlar karşılaştırıldığında şu sonuç desteklenir: {inference}"
    elif variant == 1:
        new_scenario = (
            f"Sınıf, “{scenario}” vakasının dayandığı ilkeyi farklı bir karar kartına "
            "aktarırken gerekçeyi yeniden kuruyor."
        )
        new_evidence = (
            f"Kartta {evidence} bilgisi yer alıyor; ancak önerilen “{wrong1}” sonucu "
            "bu bilginin izin verdiği kapsamı aşıyor."
        )
        new_concept = f"Aktarımda korunması gereken temel ilişki şudur: {concept}"
        new_action = f"Yeni kararı kanıtla uyumlu hâle getiren uygulama şudur: {action}"
        new_inference = f"Vaka yeni bağlama taşındığında kanıtın desteklediği sınır şudur: {inference}"
    elif variant == 2:
        new_scenario = (
            "Bir akran incelemesinde aynı konu için biri kaynaklı, biri yalnız varsayıma "
            "dayanan iki açıklama karşılaştırılıyor."
        )
        new_evidence = (
            f"Kaynaklı açıklama “{evidence}” bilgisini veriyor. Varsayıma dayanan kartta "
            f"ise “{wrong2}” yazıyor."
        )
        new_concept = f"Kaynaklı açıklamayla uyumlu kavramsal düzeltme şudur: {concept}"
        new_action = f"İnceleme sonucunda varsayımı elemek ve şu kanıtlı işlemi seçmek gerekir: {action}"
        new_inference = f"Kaynak ile varsayım arasındaki ayrım şu çıkarımı destekler: {inference}"
    else:
        new_scenario = (
            "Bir öz kontrol formu, verilen kararı hem konu bilgisi hem de olası sonucu "
            "bakımından denetlemeyi istiyor."
        )
        new_evidence = (
            f"Formdaki dayanak “{evidence}” biçimindedir. Buna rağmen “{wrong0}” "
            "genellemesi yapılırsa dayanak ile karar birbirinden kopuyor."
        )
        new_concept = f"Öz kontrolde yeniden kurulması gereken bilgi şudur: {concept}"
        new_action = f"Karar ve sonucu birlikte doğrulayan sorumlu adım şudur: {action}"
        new_inference = f"Dayanakla karar yeniden eşleştirildiğinde şu yorum geçerli kalır: {inference}"

    if mode in {"comprehension", "application"}:
        if variant != 1:
            new_scenario += f" İncelenen vaka şöyledir: {scenario}"
        new_scenario += f" İncelemede dayanak olarak şu bilgi kullanılıyor: {evidence}"
    new_wrongs = [
        f"Değerlendirme ölçütü şu ilkeye dayanmalıdır: {wrong0}",
        f"Yeni bağlama aktarılacak yorum şudur: {wrong1}",
        f"Kaynak karşılaştırmasının desteklediği sonuç şudur: {wrong2}",
    ]
    new_rationale = (
        f"{rationale} Bu yeni bağlamda iddia, bağımsız dayanak ve uygulanabilir "
        "sonuç birbirine karşı denetlenir."
    )
    return (
        note_id, new_scenario, new_evidence, new_concept, new_action,
        new_inference, new_wrongs, new_rationale,
    )


def _label(labels: dict[str, str], qid: str, suffix: str, text: str) -> str:
    key = f"{qid.replace('-', '.')}.{suffix}"
    labels[key] = text
    return key


def _eclipse_figure(qid: str, labels: dict[str, str], lunar: bool) -> dict[str, Any]:
    sun = _label(labels, qid, "sun", "Güneş")
    earth = _label(labels, qid, "earth", "Dünya")
    moon = _label(labels, qid, "moon", "Ay")
    alt = _label(
        labels, qid, "alt",
        "Güneş, Dünya ve Ay'ın aynı doğrultudaki konumlarını ve gölge bölgesini gösteren ölçeksiz model.",
    )
    if lunar:
        bodies = [
            {"type": "circle", "style": "sun", "x": 12, "y": 30, "r": 9, "labelKey": sun},
            {"type": "circle", "style": "earth", "x": 49, "y": 30, "r": 7, "labelKey": earth},
            {"type": "circle", "style": "moon", "x": 83, "y": 30, "r": 4, "labelKey": moon},
        ]
        shadow = {"type": "polygon", "style": "shadow", "points": [[52, 25], [88, 20], [88, 40], [52, 35]], "fill": "muted"}
    else:
        bodies = [
            {"type": "circle", "style": "sun", "x": 12, "y": 30, "r": 9, "labelKey": sun},
            {"type": "circle", "style": "moon", "x": 49, "y": 30, "r": 4, "labelKey": moon},
            {"type": "circle", "style": "earth", "x": 83, "y": 30, "r": 7, "labelKey": earth},
        ]
        shadow = {"type": "polygon", "style": "shadow", "points": [[49, 27], [84, 24], [84, 36], [49, 33]], "fill": "muted"}
    return {
        "kind": "diagram", "viewBox": [0, 0, 100, 60],
        "elements": [
            {"type": "line", "style": "ray", "x1": 20, "y1": 20, "x2": 90, "y2": 20, "stroke": "gold"},
            {"type": "line", "style": "ray", "x1": 20, "y1": 40, "x2": 90, "y2": 40, "stroke": "gold"},
            shadow, *bodies,
        ],
        "altTextKey": alt, "notToScale": True,
    }


def _force_figure(qid: str, labels: dict[str, str]) -> dict[str, Any]:
    east = _label(labels, qid, "east", "Doğu yönü: 12 N")
    west = _label(labels, qid, "west", "Batı yönü: 7 N")
    box = _label(labels, qid, "box", "Kutu")
    alt = _label(labels, qid, "alt", "Bir kutuya zıt yönlerde uygulanan iki kuvvet oku; bileşke açıklanmamıştır.")
    return {
        "kind": "diagram", "viewBox": [0, 0, 100, 60],
        "elements": [
            {"type": "rect", "style": "block", "x": 42, "y": 22, "w": 16, "h": 16, "fill": "surface", "labelKey": box},
            {"type": "line", "style": "force", "x1": 58, "y1": 26, "x2": 88, "y2": 26, "stroke": "blue", "labelKey": east},
            {"type": "line", "style": "force", "x1": 42, "y1": 34, "x2": 20, "y2": 34, "stroke": "orange", "labelKey": west},
        ],
        "altTextKey": alt, "notToScale": True,
    }


def _ray_figure(qid: str, labels: dict[str, str]) -> dict[str, Any]:
    mirror = _label(labels, qid, "mirror", "Ayna")
    normal = _label(labels, qid, "normal", "Normal")
    incoming = _label(labels, qid, "incoming", "Gelen ışın: 35°")
    reflected = _label(labels, qid, "reflected", "Yansıyan ışın: 35°")
    alt = _label(labels, qid, "alt", "Ayna, yüzey normali ve normalin iki yanında yer alan iki ışın.")
    return {
        "kind": "diagram", "viewBox": [0, 0, 100, 60],
        "elements": [
            {"type": "line", "style": "plain", "x1": 12, "y1": 45, "x2": 88, "y2": 45, "stroke": "ink", "labelKey": mirror},
            {"type": "line", "style": "plain", "x1": 50, "y1": 8, "x2": 50, "y2": 52, "stroke": "muted", "labelKey": normal},
            {"type": "line", "style": "ray", "x1": 20, "y1": 15, "x2": 50, "y2": 45, "stroke": "blue", "labelKey": incoming},
            {"type": "line", "style": "ray", "x1": 50, "y1": 45, "x2": 80, "y2": 15, "stroke": "orange", "labelKey": reflected},
        ],
        "altTextKey": alt, "notToScale": True,
    }


def _prism_figure(qid: str, labels: dict[str, str]) -> dict[str, Any]:
    white = _label(labels, qid, "white", "Beyaz ışık")
    prism = _label(labels, qid, "prism", "Prizma")
    screen = _label(labels, qid, "screen", "Ekran")
    alt = _label(labels, qid, "alt", "Beyaz ışığın üçgen prizmadan geçip ekranda farklı yönlere ayrıldığı düzenek.")
    return {
        "kind": "diagram", "viewBox": [0, 0, 100, 60],
        "elements": [
            {"type": "line", "style": "ray", "x1": 8, "y1": 30, "x2": 40, "y2": 30, "stroke": "ink", "labelKey": white},
            {"type": "polygon", "style": "plain", "points": [[40, 12], [40, 48], [62, 30]], "fill": "surface", "stroke": "purple", "labelKey": prism},
            {"type": "line", "style": "ray", "x1": 62, "y1": 30, "x2": 90, "y2": 16, "stroke": "danger"},
            {"type": "line", "style": "ray", "x1": 62, "y1": 30, "x2": 90, "y2": 25, "stroke": "orange"},
            {"type": "line", "style": "ray", "x1": 62, "y1": 30, "x2": 90, "y2": 35, "stroke": "blue"},
            {"type": "line", "style": "ray", "x1": 62, "y1": 30, "x2": 90, "y2": 44, "stroke": "purple"},
            {"type": "rect", "style": "plain", "x": 91, "y": 10, "w": 3, "h": 40, "fill": "white", "stroke": "ink", "labelKey": screen},
        ],
        "altTextKey": alt, "notToScale": True,
    }


def _heating_chart(qid: str, labels: dict[str, str]) -> dict[str, Any]:
    cats = [_label(labels, qid, f"t{i}", f"{i * 2}. dakika") for i in range(6)]
    x_key = _label(labels, qid, "x", "Süre")
    y_key = _label(labels, qid, "y", "Sıcaklık (°C)")
    alt = _label(labels, qid, "alt", "Sıcaklığın önce arttığı, bir süre 80 derecede sabit kaldığı ve sonra yeniden arttığı çizgi grafik.")
    return {
        "kind": "chart", "style": "line", "categoryKeys": cats,
        "values": [20, 50, 80, 80, 80, 95], "axisKeys": {"x": x_key, "y": y_key},
        "altTextKey": alt,
    }


def apply_science_visual(
    row: dict[str, Any], labels: dict[str, str], case_index: int, task_context: str = "",
) -> None:
    """Replace the generic evidence table only when a stronger semantic visual exists."""
    if row.get("questionType") != "analysis":
        return
    qid = str(row["id"])
    figure: dict[str, Any] | None = None
    noun = "şemada"
    if case_index == 2:
        figure = _eclipse_figure(qid, labels, lunar=False)
    elif case_index == 3:
        figure = _eclipse_figure(qid, labels, lunar=True)
    elif case_index == 4:
        figure = _force_figure(qid, labels)
    elif case_index == 17:
        figure = _ray_figure(qid, labels)
    elif case_index == 20:
        figure = _prism_figure(qid, labels)
    elif case_index == 24:
        figure, noun = _heating_chart(qid, labels), "grafikte"
    if figure is None:
        return
    row["figure"] = figure
    # Several notes share a broad topic; the note title keeps each visual task
    # identifiable without copying the evidence out of the figure.
    topic = {
        2: "Güneş tutulması modeli",
        3: "Ay tutulması modeli",
        4: "zıt yönlü kuvvetler",
        17: "yansıma açıları",
        20: "beyaz ışığın prizmada ayrılması",
        24: "saf maddenin ısınma eğrisi",
    }.get(case_index, str(row.get("title") or row.get("topic") or "fen olayı").split(" — ", 1)[0])
    row["question"] = (
        f"Aşağıdaki {noun} {topic} konusuna ait ölçüm veya konum kanıtı verilmiştir. "
        + (f"İncelemede {task_context} ölçütleri birlikte kullanılacaktır. " if task_context else "")
        + "Hangi çıkarım görseldeki kanıtla ve konu anlatımıyla birlikte desteklenir?"
    )
    kind = str(figure["kind"])
    row["visualNeed"] = {
        "level": "required", "role": "evidence",
        "rationale": "Çözüm için gereken uzamsal veya sayısal kanıt yalnız yapılandırılmış görselde yer alır.",
        "acceptableKinds": [kind], "evidenceDimensions": ["konum" if kind == "diagram" else "süre", "ölçüm"],
    }
    row["visualRequirement"] = "required"
    row["explanation"] = str(row["explanation"]).replace(
        "Tablodaki iki kayıt", "Görseldeki yapılandırılmış kanıt"
    )


def main() -> int:
    dkab_notes = read_notes_only(DKAB_SOURCE)
    fen_notes = read_notes_only(FEN_SOURCE)
    existing = [json.loads(x) for x in OUTPUT.read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(existing) != 500:
        raise RuntimeError("validated first five batches must exist before batch 06")
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    dkab_cases = [
        (source[index], (2 * index + source_no) % 4)
        for index in range(16)
        for source_no, source in enumerate((DKAB_A, DKAB_B))
    ]
    rows: list[dict[str, Any]] = []
    dkab_cursor = fen_cursor = 0
    for local, (mode, level) in enumerate(zip(MODE_SEQUENCE, LEVEL_SEQUENCE), 1):
        if local in DKAB_POSITIONS:
            source_case, variant = dkab_cases[dkab_cursor]
            case = derived_dkab_case(source_case, variant, mode)
            dkab_cursor += 1
            row = make_question(
                local, case, mode, level, dkab_notes[case[0]], labels,
                "Din Kültürü ve Ahlak Bilgisi", batch_number=6, number_base=500,
            )
        else:
            case_index = fen_cursor % len(FEN_CASES)
            case = FEN_CASES[case_index]
            fen_cursor += 1
            row = make_question(
                local, case, mode, level, fen_notes[case[0]], labels,
                "Fen Bilimleri", batch_number=6, number_base=500,
            )
            apply_science_visual(row, labels, case_index)
        rows.append(row)
    if (dkab_cursor, fen_cursor) != (32, 68):
        raise AssertionError((dkab_cursor, fen_cursor))
    if {row["correctIndex"] for row in rows} != {0, 1, 2, 3}:
        raise AssertionError("answer positions were not rotated")
    OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + rows) + "\n",
        encoding="utf-8", newline="\n",
    )
    LABELS_OUTPUT.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({
        "batch": 6, "questions": 100, "religion": 32, "science": 68,
        "total": 600, "labels": len(labels), "sourceQuestionReads": 0,
        "figureSpec": "1.3.0",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
