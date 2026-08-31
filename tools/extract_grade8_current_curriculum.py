#!/usr/bin/env python3
"""Extract the active 2026–2027 Grade 8 objective registry from official MEB PDFs."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "curriculum/tr-grade8-current-2018-2019.json"
SOURCES = {
    "Fen Bilimleri": {
        "slug": "fen",
        "url": "https://mufredat.meb.gov.tr/Dosyalar/201812312311937-FEN%20B%C4%B0L%C4%B0MLER%C4%B0%20%C3%96%C4%9ERET%C4%B0M%20PROGRAMI2018.pdf",
        "sourceId": "tr-meb-fen-g03-g08-program-2018",
        "pattern": r"F\.8\.\d+\.\d+\.\d+",
    },
    "Matematik": {
        "slug": "matematik",
        "url": "https://mufredat.meb.gov.tr/Dosyalar/201813017165445-MATEMAT%C4%B0K%20%C3%96%C4%9ERET%C4%B0M%20PROGRAMI%202018v.pdf",
        "sourceId": "tr-meb-matematik-g01-g08-program-2018",
        "pattern": r"M\.8\.\d+\.\d+\.\d+",
        "titleOverrides": {
            "M.8.1.2.2": "Üslü ifadelerle ilgili temel kuralları anlar, birbirine denk ifadeler oluşturur",
            "M.8.1.2.5": "Çok büyük ve çok küçük sayıları bilimsel gösterimle ifade eder ve karşılaştırır",
        },
    },
    "Türkçe": {
        "slug": "turkce",
        "url": "https://mufredat.meb.gov.tr/Dosyalar/20195716392253-02-T%C3%BCrk%C3%A7e%20%C3%96%C4%9Fretim%20Program%C4%B1%202019.pdf",
        "sourceId": "tr-meb-turkce-g01-g08-program-2019",
        "pattern": r"T\.8\.\d+\.\d+",
    },
    "İngilizce": {
        "slug": "ingilizce",
        "url": "https://mufredat.meb.gov.tr/Dosyalar/201812411191321-%C4%B0NG%C4%B0L%C4%B0ZCE%20%C3%96%C4%9ERET%C4%B0M%20PROGRAMI%20Klas%C3%B6r%C3%BC.pdf",
        "sourceId": "tr-meb-ingilizce-g02-g08-program-2018",
        "pattern": r"E8\.\d+\.(?:L|SI|SP|R|W)\d+",
        "pageRange": [85, 94],
    },
    "Din Kültürü ve Ahlak Bilgisi": {
        "slug": "dkab",
        "url": "https://mufredat.meb.gov.tr/Dosyalar/20221229134650712-DKAB_(4-8.%20S%C4%B1n%C4%B1f)_DOP_%202018.pdf",
        "sourceId": "tr-meb-dkab-g04-g08-program-2018",
        "pattern": r"8\.\d+\.\d+",
        # pypdf keeps the official text but inserts word-internal spaces and
        # the generic sentence cutter mistakes ``Hz.`` for the end of the
        # learning outcome.  Keep these evidence-checked repairs beside the
        # source declaration so a rerun cannot silently recreate truncated
        # curriculum records.
        "titleOverrides": {
            "8.1.5": "Hz. Musa’nın (a.s.) hayatını ana hatlarıyla tanır",
            "8.1.6": "Ayet el-Kürsi'yi okur, anlamını söyler",
            "8.2.4": "Hz. Şuayb’in (a.s.) hayatını ana hatlarıyla tanır",
            "8.3.2": "İslam dininin can, nesil, akıl, mal ve din emniyetiyle ilgili ortaya koyduğu ilke ve hedefleri analiz eder",
            "8.3.3": "Hz. Yusuf’un (a.s.) örnek hayatından ilkeler çıkarır",
            "8.4.1": "Hz. Muhammed’in (s.a.v.) doğruluğu ve güvenilir kişiliği ile peygamberlerin özellikleri arasında ilişki kurar",
            "8.4.2": "Hz. Muhammed’in (s.a.v.) merhametli ve affedici oluşunu davranışlarında yansıtmaya özen gösterir",
            "8.4.3": "Hz. Muhammed’in (s.a.v.) istişareye verdiği önemi ortaya koyan örnek olaylardan hareketle gündelik hayatla ilgili çıkarımlarda bulunur",
            "8.4.4": "Hz. Muhammed’in (s.a.v.) cesaret ve kararlılığını örnek olaylarla açıklar",
            "8.4.5": "Hz. Muhammed’in (s.a.v.) hakkı gözetmedeki hassasiyetine örnekler verir",
            "8.4.6": "Hz. Muhammed’in (s.a.v.) insanlara verdiği değeri örneklerle açıklar",
            "8.4.7": "Hz. Muhammed’in (s.a.v.) örnek davranışlarının toplumsal hayattaki önemini değerlendirir",
            "8.4.8": "Hz. Muhammed’in (s.a.v.) hikmetli söz ve davranışlarıyla insanları iyiye ve güzele yönlendirdiğini fark eder",
            "8.5.4": "Hz. Nuh’un (a.s.) tevhide davetini özetler",
        },
    },
    "T.C. İnkılap Tarihi ve Atatürkçülük": {
        "slug": "inkilap",
        "url": "https://mufredat.meb.gov.tr/Dosyalar/201812104016155-%C4%B0NKILAP%20TAR%C4%B0H%C4%B0%20VE%20ATAT%C3%9CRK%C3%87%C3%9CL%C3%9CK%20%C3%96%C4%9ERET%C4%B0M%20PROGRAMI.pdf",
        "sourceId": "tr-meb-inkilap-g08-program-2018",
        "pattern": r"İTA\.8\.\d+\.\d+",
        "titleOverrides": {
            "İTA.8.2.8": "Mustafa Kemal’in ve Türk milletinin Sevr Antlaşması’na karşı tepkilerini değerlendirir",
        },
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(text: str) -> str:
    text = text.replace("\u00ad", "").replace("\u0002", "")
    text = re.sub(r"(?<=\w)-\s+(?=\w)", "", text)
    return re.sub(r"\s+", " ", text).strip(" .")


def objective_title(block: str) -> str:
    block = clean(block)
    stop_markers = (
        " a) ", " b) ", " c) ", " ç) ", " d) ", " e) ",
        " Konu ile ilgili", " Kazanım kapsamında", " Bu kazanım",
        " Temel düzeyde", " Uygulamalarda", " Açıklamalar",
        " Contexts ", " Tasks/Activities ", " Assignments ",
    )
    positions = [block.find(marker) for marker in stop_markers if block.find(marker) > 0]
    if positions:
        block = block[:min(positions)]
    block = re.split(r"\s+[a-eç]\.(?=\s+[A-ZÇĞİÖŞÜ])", block, maxsplit=1)[0]
    block = re.split(r"\s*[•]\s*", block, maxsplit=1)[0]
    # The learning-outcome sentence itself is the canonical title; retain
    # abbreviations such as s.a.v. by cutting only at a sentence boundary that
    # is followed by a new capitalized explanatory sentence.
    match = re.search(r"\.(?=\s+[A-ZÇĞİÖŞÜ])", block)
    if match:
        block = block[:match.start()]
    return clean(block)


def page_entries(text: str, pattern: str) -> list[tuple[str, str]]:
    regex = re.compile(
        rf"(?<![\w.])({pattern})\s*\.\s*(.+?)(?=(?<![\w.])(?:{pattern})\s*\.|\Z)",
        re.DOTALL,
    )
    return [(match.group(1), objective_title(match.group(2))) for match in regex.finditer(text)]


def extract_subject(pdf: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    reader = PdfReader(pdf)
    page_range = config.get("pageRange")
    objectives: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, page in enumerate(reader.pages):
        page_number = index + 1
        if page_range and not (page_range[0] <= page_number <= page_range[1]):
            continue
        text = page.extract_text() or ""
        for code, title in page_entries(text, config["pattern"]):
            if code in seen or not title:
                continue
            seen.add(code)
            title = config.get("titleOverrides", {}).get(code, title)
            # Some programme PDFs expose the printed footer page number as
            # part of the final outcome block (for example ``... eder. 6``).
            title = re.sub(r"\.\s*\d+$", "", title).strip()
            if title == "Hz" or "�" in title or re.search(r"\.\s*\d+$", title):
                raise ValueError(f"{config['sourceId']}:{code}: corrupt objective title {title!r}")
            objectives.append({
                "code": code,
                "title": title,
                "objectiveSource": config["url"],
                "objectiveEvidenceId": f"{config['sourceId']}:pdf-page-{page_number}",
            })
    return objectives


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args.source_dir.mkdir(parents=True, exist_ok=True)
    subjects = []
    for subject, config in SOURCES.items():
        path = args.source_dir / f"{config['slug']}.pdf"
        if not path.exists():
            if not args.download:
                raise FileNotFoundError(path)
            urllib.request.urlretrieve(config["url"], path)
        objectives = extract_subject(path, config)
        if not objectives:
            raise ValueError(f"{subject}: no Grade 8 objectives extracted")
        subjects.append({
            "subject": subject,
            "programmeFamily": "pre-TYMM-current",
            "programmeYear": 2019 if subject == "Türkçe" else 2018,
            "sourceId": config["sourceId"],
            "sourceUrl": config["url"],
            "sourceSha256": sha256(path),
            "pageCount": len(PdfReader(path).pages),
            "objectives": objectives,
        })
    registry = {
        "schemaVersion": "alika-tr-current-curriculum/1.0.0",
        "country": "TR",
        "grade": 8,
        "schoolYear": "2026-2027",
        "programmeFamily": "pre-TYMM-current",
        "authority": "T.C. Millî Eğitim Bakanlığı",
        "activationEvidence": [
            "https://tymm.meb.gov.tr/taslak-cerceve-planlari",
            "https://antalyaodm.meb.gov.tr/www/yillik-cerceve-planlar-ve-ogretim-programlari/icerik/49/tr",
        ],
        "subjects": subjects,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(registry, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"output": str(args.output), "counts": {s["subject"]: len(s["objectives"]) for s in subjects}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
