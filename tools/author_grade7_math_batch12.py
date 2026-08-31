#!/usr/bin/env python3
"""Append Grade 7 Mathematics batch 12 with independent validation tasks."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

from author_grade6_mixed_batch03 import LEVEL_SEQUENCE, make_question, read_notes_only
from author_grade7_dkab_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade7_math_batch11 import CASES


SOURCE = Path("turkiye/7-sinif/matematik/matematik-tum.jsonl")
MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
LENSES = (
    ("ters işlem denetimi", "sonuçtan başlangıç verisine dönülerek aynı ilişkinin elde edilmesi"),
    ("alternatif temsil denetimi", "tablo, sözel ifade veya cebirsel gösterimin aynı değeri vermesi"),
    ("birim ve sınır denetimi", "birim ile mümkün değer aralığının sonuçla tutarlı kalması"),
    ("karşı örnek denetimi", "iddianın kapsamı dışındaki bir durumun genellemeyi bozup bozmadığının sınanması"),
)


def derive(base: tuple[Any, ...], occurrence: int) -> tuple[Any, ...]:
    note, scenario, evidence, concept, action, inference, wrongs, rationale = base
    lens, check = LENSES[occurrence % len(LENSES)]
    return (
        note,
        f"Bir matematik doğrulama kurulu {lens} kullanarak yeni bir rapor hazırlıyor. Başlangıç modeli şudur: {scenario} Kurul, ilk sonucu doğrudan kabul etmeyip ikinci bir temsil istemektedir.",
        f"İlk kayıtta şu bulgu vardır: {evidence} Bağımsız kontrol kaydı ise {check} koşulunu taşıyor ve iki kaydın aynı niceliği açıklaması bekleniyor.",
        f"{concept} Ayrıca {lens}, işlemin yalnız sonucunu değil temsil ile anlam arasındaki eşdeğerliği denetler.",
        f"{action} Ardından {check} gösterilmeli ve iki yoldan elde edilen sonuçlar karşılaştırılmalıdır.",
        f"{inference} Bu çıkarım, {lens} sonucunda iki bağımsız temsilin aynı ilişkiyi vermesiyle güçlenir; rapor yalnız denetlenen koşullarla sınırlıdır.",
        [
            f"{wrongs[0]} Üstelik {lens} yapılmadan da her temsilin aynı sonucu vereceği varsayılabilir.",
            f"{wrongs[1]} İkinci kayıt ilk kayıtla çelişse bile sonuç değiştirilemez.",
            f"{wrongs[2]} {check.capitalize()} matematiksel doğrulamada hiçbir bilgi sağlamaz.",
        ],
        f"{rationale} Bu yeni görevde {lens}; işlem, temsil, birim ve sonuç arasındaki bağı görünür kılar. {check.capitalize()} sağlanmadan kesinlik iddiası kurulmaz.",
    )


def transform(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace("tr-g06-bank-bty-b12", "tr-g07-bank-matematik-b12").replace("tr.g06.bank.bty.b12", "tr.g07.bank.matematik.b12")
    if isinstance(value, list):
        return [transform(child) for child in value]
    if isinstance(value, dict):
        return {key: transform(child) for key, child in value.items()}
    return value


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1100:
        raise RuntimeError(f"batch 12 expects 1100 records, found {len(existing)}")
    notes = read_notes_only(SOURCE)
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    occurrences: Counter[str] = Counter()
    rows = []
    for local, mode in enumerate(MODES, 1):
        base = CASES[(local + 9) % len(CASES)]
        occurrence = occurrences[base[0]]
        occurrences[base[0]] += 1
        case = derive(base, occurrence)
        note = dict(notes[case[0]])
        note["title"] = f"{note['title']} — {LENSES[occurrence % len(LENSES)][0]}"
        row = make_question(local, case, mode, LEVEL_SEQUENCE[local - 1], note, labels, "Matematik", batch_number=12, number_base=1100)
        row = transform(row)
        row["grade"] = 7
        row["title"] = f"{note['title']} — 12. özgün üretim partisi"
        rows.append(row)
    if Counter(row["correctIndex"] for row in rows) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer balance")
    labels = {transform(key): transform(value) for key, value in labels.items()}
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + rows) + "\n", encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"grade": 7, "batch": 12, "questions": 100, "mathematics": 100, "total": 1200, "figures": sum(bool(row.get("figure")) for row in rows), "sourceQuestionReads": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
