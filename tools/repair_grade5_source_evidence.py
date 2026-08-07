#!/usr/bin/env python3
"""Repair Grade 5 official-source evidence without regenerating questions."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRADE5 = ROOT / "turkiye" / "5-sinif"

SOCIAL = GRADE5 / "sosyal-bilgiler" / "sosyal-bilgiler-tum.jsonl"
TURKISH = GRADE5 / "turkce" / "turkce-tum.jsonl"
MATH = GRADE5 / "matematik" / "matematik-tum.jsonl"
ENGLISH = GRADE5 / "ingilizce" / "ingilizce-tum.jsonl"

SOCIAL_SOURCE_ID = "tr-meb-sosyal-g04-g07-program-2024"
SOCIAL_URL = (
    "https://mufredat.meb.gov.tr/Dosyalar/"
    "202582516728345-sosyal%20bilgiler.pdf"
)
SOCIAL_SHA256 = (
    "122139E66C7255234C61A703E5A3B2E7E49C40679AF8869AD7B0A43CE6674B13"
)
SOCIAL_PAGES = {
    **{f"SB.5.1.{n}": 37 for n in range(1, 4)},
    **{f"SB.5.2.{n}": 42 for n in range(1, 5)},
    **{f"SB.5.3.{n}": 47 for n in range(1, 4)},
    **{f"SB.5.4.{n}": 52 for n in range(1, 5)},
    **{f"SB.5.5.{n}": 57 for n in range(1, 4)},
    **{f"SB.5.6.{n}": 61 for n in range(1, 3)},
}

TURKISH_SOURCE_ID = "tr-meb-tur-g05-g08-program-2024"
TURKISH_SHA256 = (
    "A5308C3C433FC4A5C5CE486DA4A22379EEAC630789C0F37C2987BEC8AF70EA85"
)
TURKISH_PAGES = {
    "T.D.5.1.": 36,
    "T.D.5.5.": 37,
    "T.D.5.7.": 37,
    "T.D.5.10.": 38,
    "T.D.5.22.": 40,
    "T.O.5.5.": 43,
    "T.O.5.6.": 43,
    "T.O.5.8.": 44,
    "T.O.5.13.": 45,
    "T.O.5.14.": 45,
    "T.O.5.15.": 45,
    "T.O.5.21.": 46,
    "T.O.5.24.": 47,
    "T.K.5.1.": 49,
    "T.K.5.3.": 49,
    "T.K.5.5.": 50,
    "T.K.5.9.": 51,
    "T.K.5.23.": 54,
    "T.Y.5.1.": 56,
    "T.Y.5.3.": 56,
    "T.Y.5.20.": 59,
    "T.Y.5.21.": 59,
}

MATH_SOURCE_ID = "tr-meb-mat-g05-g08-program-2024"
MATH_PAGES = {
    "MAT.5.1.1": 14,
    "MAT.5.1.2": 21,
    "MAT.5.1.3": 27,
    "MAT.5.1.4": 27,
    "MAT.5.2.1": 32,
    "MAT.5.2.2": 32,
    "MAT.5.2.3": 32,
    "MAT.5.2.4": 32,
    "MAT.5.3.1": 39,
    "MAT.5.3.2": 39,
    "MAT.5.3.3": 39,
    "MAT.5.3.4": 39,
    "MAT.5.3.5": 39,
    "MAT.5.3.6": 39,
    "MAT.5.3.7": 39,
    "MAT.5.4.1": 48,
    "MAT.5.4.2": 48,
    "MAT.5.4.3": 48,
    "MAT.5.4.4": 48,
    "MAT.5.5.1": 53,
    "MAT.5.5.2": 53,
    "MAT.5.6.1": 59,
    "MAT.5.6.2": 59,
}

ENGLISH_SOURCE_ID = "tr-meb-ingilizce-g02-g08-program-2025"
ENGLISH_URL = "https://tymm.meb.gov.tr/upload/program/ingilizce-programi-1-tegm.pdf"

TURKISH_EXPLANATIONS = {
    "tr-g05-tur-q407": {
        "explanation": (
            "Lale, menekşe ve papatya bitki adlarıdır; üçü de çiçek türü "
            "olduğu için ortak kavram alanları çiçek adlarıdır."
        ),
        "correctWhy": (
            "Doğru seçenektir; lale, menekşe ve papatya farklı çiçek "
            "türlerini adlandırır."
        ),
    },
    "tr-g05-tur-q425": {
        "explanation": (
            "Sevinç, kaygı ve şaşkınlık kişinin hissedebildiği durumları "
            "adlandırır; bu nedenle duygu bildiren sözcükler başlığında "
            "toplanır."
        ),
        "correctWhy": (
            "Doğru seçenektir; üç sözcük de bir kişinin hissedebileceği "
            "duyguları adlandırır."
        ),
    },
    "tr-g05-tur-q443": {
        "explanation": (
            "Çınar, meşe ve ardıç farklı ağaç türlerinin adlarıdır; bu nedenle "
            "ortak kavram alanları ağaçlardır."
        ),
        "correctWhy": (
            "Doğru seçenektir; çınar, meşe ve ardıç farklı ağaç türlerini "
            "adlandırır."
        ),
    },
}


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "\n".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":"))
            for row in rows
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def source(pack: dict, source_id: str) -> dict:
    matches = [
        item
        for item in pack.get("sources") or []
        if item.get("sourceId") == source_id
    ]
    if len(matches) != 1:
        raise ValueError(f"{pack.get('id')}: kaynak bulunamadı: {source_id}")
    return matches[0]


def record_objectives(record: dict) -> list[str]:
    values = record.get("objectives") or [record.get("objective")]
    return [str(value) for value in values if value]


def repair_social(rows: list[dict]) -> None:
    pack = rows[0]
    item = source(pack, SOCIAL_SOURCE_ID)
    item["downloadUrl"] = SOCIAL_URL
    item["sha256"] = SOCIAL_SHA256
    item["pageCount"] = 116
    for record in rows[1:]:
        if record.get("type") not in {"note", "question"}:
            continue
        objectives = record_objectives(record)
        pages = {SOCIAL_PAGES[objective] for objective in objectives}
        if len(pages) != 1:
            raise ValueError(f"{record.get('id')}: tek sosyal sayfası bulunamadı")
        page = pages.pop()
        record["objectiveSource"] = SOCIAL_URL
        record["objectiveEvidenceId"] = (
            f"{SOCIAL_SOURCE_ID}:pdf-page-{page}"
        )
        record["sourceRefs"] = [SOCIAL_SOURCE_ID]


def repair_turkish(rows: list[dict]) -> None:
    pack = rows[0]
    item = source(pack, TURKISH_SOURCE_ID)
    item["sha256"] = TURKISH_SHA256
    item["pageCount"] = 272
    url = item["downloadUrl"]
    for record in rows[1:]:
        if record.get("type") not in {"note", "question"}:
            continue
        objectives = record_objectives(record)
        pages = {TURKISH_PAGES[objective] for objective in objectives}
        if len(pages) != 1:
            raise ValueError(f"{record.get('id')}: tek Türkçe sayfası bulunamadı")
        page = pages.pop()
        record["objectiveSource"] = url
        record["objectiveEvidenceId"] = (
            f"{TURKISH_SOURCE_ID}:pdf-page-{page}"
        )
        record["sourceRefs"] = [TURKISH_SOURCE_ID]
        replacement = TURKISH_EXPLANATIONS.get(record.get("id"))
        if replacement:
            record["explanation"] = replacement["explanation"]
            record["distractorWhy"][record["correct"]] = replacement["correctWhy"]


def repair_math(rows: list[dict]) -> None:
    pack = rows[0]
    item = source(pack, MATH_SOURCE_ID)
    url = item["downloadUrl"]
    for record in rows[1:]:
        if record.get("type") not in {"note", "question"}:
            continue
        objectives = record_objectives(record)
        pages = {MATH_PAGES[objective] for objective in objectives}
        if len(pages) != 1:
            raise ValueError(f"{record.get('id')}: tek Matematik sayfası bulunamadı")
        page = pages.pop()
        record["objectiveSource"] = url
        record["objectiveEvidenceId"] = f"{MATH_SOURCE_ID}:pdf-page-{page}"
        record["sourceRefs"] = [MATH_SOURCE_ID]


def repair_english(rows: list[dict]) -> None:
    pack = rows[0]
    source(pack, ENGLISH_SOURCE_ID)
    for record in rows[1:]:
        if record.get("type") not in {"note", "question"}:
            continue
        evidence = str(record.get("objectiveEvidenceId") or "")
        if not evidence.startswith(f"{ENGLISH_SOURCE_ID}#p"):
            raise ValueError(f"{record.get('id')}: İngilizce sayfa çapası bozuk")
        record["objectiveSource"] = ENGLISH_URL


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    jobs = (
        (SOCIAL, repair_social),
        (TURKISH, repair_turkish),
        (MATH, repair_math),
        (ENGLISH, repair_english),
    )
    for path, repair in jobs:
        rows = read_jsonl(path)
        repair(rows)
        if args.write:
            write_jsonl(path, rows)
        print(f"{path.relative_to(ROOT)}: {len(rows)} kayıt")
    if not args.write:
        print("(dosyaları yazmak için --write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
