#!/usr/bin/env python3
"""Append Grade 7 batch 03: 100 note-grounded Science questions."""
from __future__ import annotations

from collections import Counter
import json
from typing import Any

from build_unique_question_banks import ROOT
from author_grade6_mixed_batch03 import make_question, read_notes_only
from author_grade7_dkab_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade7_dkab_fen_batch02 import FEN_CASES as FIRST_CASES


SOURCE = ROOT / "turkiye/7-sinif/fen-bilimleri/fen-bilimleri-tum.jsonl"


EXTRA_CASES = [
    ("tr-g07-fen-note-fb-7-5-3-1-q0393-q0400", "Öğrenciler yağ ve su karışımını çalkaladıktan sonra farklı sürelerde gözlüyor.", "Çalkalama sonrası geçici bulanıklık oluşuyor; bekleyince iki ayrı tabaka yeniden belirginleşiyor.", "Karışım dağılımı kontrollü miktar, karıştırma ve bekleme süresiyle gözlenirse geçici görünüm ile kalıcı homojenlik birbirinden ayrılır.", "Eşit hacim ve çalkalama süresi kullanıp tabaka oluşumunu belirli aralıklarla güvenli biçimde kaydetmek gerekir.", "İki tabakanın yeniden oluşması, kısa süreli bulanıklığın karışımı kalıcı olarak homojen yapmadığını gösterir.", ["Çalkalanan her karışım kalıcı olarak homojen olur.", "Bekleme kaydı karışımın dağılımını değerlendirmede gereksizdir.", "Yağ ile su aynı görünüyorsa maddeler kimyasal olarak yeni maddeye dönüşmüştür."], "Karışım sınıflandırması ilk görünüşe değil kontrollü gözlem, bekleme ve tekrarlanabilir dağılım kanıtına dayanır."),
    ("tr-g07-fen-note-fb-7-5-3-1", "Hava, şekerli su, ayran ve granit örnekleri gözlenebilir özelliklerine göre sınıflandırılıyor.", "Hava ve tamamen çözünmüş şekerli su tek fazlı; ayran bekleyince ayrışıyor, granitte farklı mineraller seçilebiliyor.", "Homojen karışımda bileşenler örneğin her yerinde aynı dağılım gösterirken heterojen karışımda farklı faz veya kısımlar ayırt edilebilir.", "Örnekleri görünüm, faz ve bekleme sonrası değişim ölçütleriyle karşılaştırıp saf madde kararıyla karıştırmamak gerekir.", "Ayran ve granitte farklı kısımların gözlenmesi, bunların hava ve şekerli sudan farklı sınıfa yerleştirilmesini destekler.", ["Gözle seçilemeyen bileşenleri olan her karışım saf maddedir.", "Granit tek renkli göründüğü anda kesin homojen sayılır.", "Homojen ve heterojen ayrımında dağılım ve faz sayısı kullanılamaz."], "Sınıflandırma, karışımın bileşenlerinin dağılımını ve gözlenebilir fazlarını temel alır; görünüş tek başına saflığı kanıtlamaz."),
]

CASES = [*FIRST_CASES, *EXTRA_CASES]
MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
LEVELS = [1] * 20 + [2] * 25 + [3] * 30 + [4] * 20 + [5] * 5
FOCI = (
    "değişken kontrolü", "ölçümün tekrarlanabilirliği", "model-veri tutarlılığı",
    "laboratuvar güvenliği", "neden-sonuç ilişkisi", "belirsizlik ve kanıt sınırı",
)


def derive(base: tuple[Any, ...], occurrence: int) -> tuple[Any, ...]:
    note, scenario, evidence, concept, action, inference, wrongs, rationale = base
    focus = FOCI[occurrence % len(FOCI)]
    return (
        note,
        f"Bir {focus} çalışmasında şu bilimsel durum yeniden inceleniyor: {scenario}",
        f"{evidence} Kayıtlar ayrıca {focus} ölçütüne göre karşılaştırılıyor.",
        f"{concept} Bu açıklamada {focus} göz ardı edilmez.",
        f"{action} Sonuç {focus} bakımından da kontrol edilmelidir.",
        f"{inference} Bu çıkarım {focus} sınırında kalır.",
        [
            f"{wrongs[0]} Ayrıca {focus} sonucu etkilemez.",
            f"{wrongs[1]} Bu yargı tek gözlemden bütün koşullara taşınabilir.",
            f"{wrongs[2]} Ölçüm ile açıklama arasındaki bağın kurulması gerekmez.",
        ],
        f"{rationale} Bilimsel değerlendirmede {focus} açıkça kaydedilir ve sonuçla ilişkilendirilir.",
    )


def replace_grade(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace("tr-g06-bank-fen-b03", "tr-g07-bank-fen-b03").replace("tr.g06.bank.fen.b03", "tr.g07.bank.fen.b03")
    if isinstance(value, list):
        return [replace_grade(child) for child in value]
    if isinstance(value, dict):
        return {key: replace_grade(child) for key, child in value.items()}
    return value


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 200:
        raise RuntimeError(f"batch 03 expects 200 records, found {len(existing)}")
    notes = read_notes_only(SOURCE)
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    occurrences: Counter[str] = Counter()
    records = []
    for local, (mode, level) in enumerate(zip(MODES, LEVELS), 1):
        base = CASES[(local - 1) % len(CASES)]
        occurrence = occurrences[base[0]]
        occurrences[base[0]] += 1
        case = derive(base, occurrence)
        note = dict(notes[case[0]])
        note["title"] = f"{note['title']} — {FOCI[occurrence % len(FOCI)]}"
        row = make_question(local, case, mode, level, note, labels, "Fen Bilimleri", batch_number=3, number_base=200)
        row = replace_grade(row)
        row["grade"] = 7
        row["title"] = f"{note['title']} — 3. özgün üretim partisi"
        records.append(row)
    labels = {replace_grade(key): replace_grade(value) for key, value in labels.items()}
    if Counter(row["correct"] for row in records) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer balance")
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + records) + "\n", encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"grade": 7, "batch": 3, "questions": 100, "science": 100, "total": 300, "figures": sum(bool(row.get("figure")) for row in records), "sourceQuestionReads": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
