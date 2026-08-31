#!/usr/bin/env python3
"""Append 100 source-critical Grade 7 Social Studies questions, batch 14."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

from author_grade6_mixed_batch03 import LEVEL_SEQUENCE, make_question, read_notes_only
from author_grade7_dkab_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade7_math_social_batch13 import SOCIAL_CASES


SOURCE = Path("turkiye/7-sinif/sosyal-bilgiler/sosyal-bilgiler-tum.jsonl")
MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
LENSES = (
    "kaynağın amacı ve hedef kitlesi", "birincil ve ikincil kaynak ayrımı",
    "zaman içindeki değişim", "farklı toplumsal grupların deneyimi",
    "iddia-kanıt uyumu", "uygulanabilir çözüm ve izleme",
)


def derive(base: tuple[Any, ...], occurrence: int) -> tuple[Any, ...]:
    note, scenario, evidence, concept, action, inference, wrongs, rationale = base
    lens = LENSES[occurrence % len(LENSES)]
    return (
        note,
        f"Bir araştırma kurulu {lens} bakımından yeni ve karşılaştırmalı bir dosya açıyor. Dosyadaki toplumsal durum şudur: {scenario}",
        f"Birinci kaynak şu bulguyu bildiriyor: {evidence} İkinci kaynak aynı olayın kapsamını, tarihini ve temsil ettiği grubu açıklayan bağımsız bir künye sunuyor.",
        f"{concept} Bu görevde {lens}, olgu ile yorumun ve sınırlı örnek ile genel iddianın ayrılmasını sağlar.",
        f"{action} Sonra iki kaynağın uzlaştığı ve ayrıldığı noktalar yazılmalı, öneri için izlenebilir bir gösterge belirlenmelidir.",
        f"{inference} İkinci kaynağın kapsam bilgisi bu çıkarımı {lens} sınırında destekler; dosyada olmayan dönem veya gruplara genellenemez.",
        [
            f"{wrongs[0]} {lens.capitalize()} incelenmeden tek kaynak bütün toplumu temsil eder.",
            f"{wrongs[1]} İki kaynak çeliştiğinde tarih ve kapsam bilgisi karşılaştırılmaz.",
            f"{wrongs[2]} Olgu ile yorumun ayrılması toplumsal araştırma için gereksizdir.",
        ],
        f"{rationale} Karşılaştırmalı dosyada {lens}; kaynak, bağlam, iddia ve öneri arasındaki bağı şeffaflaştırır.",
    )


def transform(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace("tr-g06-bank-bty-b14", "tr-g07-bank-sosyal-bilgiler-b14").replace("tr.g06.bank.bty.b14", "tr.g07.bank.sosyal-bilgiler.b14")
    if isinstance(value, list): return [transform(x) for x in value]
    if isinstance(value, dict): return {k: transform(v) for k, v in value.items()}
    return value


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1300:
        raise RuntimeError(f"batch 14 expects 1300 records, found {len(existing)}")
    notes = read_notes_only(SOURCE)
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    occurrences: Counter[str] = Counter()
    rows = []
    for local, mode in enumerate(MODES, 1):
        base = SOCIAL_CASES[(local + 7) % len(SOCIAL_CASES)]
        occurrence = occurrences[base[0]]
        occurrences[base[0]] += 1
        case = derive(base, occurrence)
        note = dict(notes[case[0]])
        note["title"] = f"{note['title']} — {LENSES[occurrence % len(LENSES)]}"
        row = make_question(local, case, mode, LEVEL_SEQUENCE[local - 1], note, labels, "Sosyal Bilgiler", batch_number=14, number_base=1300)
        row = transform(row)
        row["grade"] = 7
        row["title"] = f"{note['title']} — 14. özgün üretim partisi"
        rows.append(row)
    if Counter(row["correctIndex"] for row in rows) != Counter({0: 25, 1: 25, 2: 25, 3: 25}): raise AssertionError("answer balance")
    labels = {transform(key): transform(value) for key, value in labels.items()}
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + rows) + "\n", encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"grade": 7, "batch": 14, "questions": 100, "socialStudies": 100, "total": 1400, "figures": sum(bool(row.get("figure")) for row in rows), "sourceQuestionReads": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__": raise SystemExit(main())
