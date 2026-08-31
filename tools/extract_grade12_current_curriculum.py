#!/usr/bin/env python3
"""Extract the 2026-2027 active Grade 12 registry from official MEB PDFs."""
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
OUTPUT = ROOT / "curriculum/tr-grade12-current-2018.json"
SOURCES: dict[str, dict[str, Any]] = {
    "Biyoloji": {"slug": "biyoloji", "sourceId": "tr-meb-biyoloji-g09-g12-program-2018", "url": "https://mufredat.meb.gov.tr/Dosyalar/20182215535566-Biyoloji%20d%C3%B6p.pdf", "pages": (29, 33), "pattern": r"12\.\d+\.\d+\.\d+"},
    "Coğrafya": {"slug": "cografya", "sourceId": "tr-meb-cografya-g09-g12-program-2018", "url": "https://mufredat.meb.gov.tr/Dosyalar/2018120203724482-Cografya%20dop%20pdf.pdf", "pages": (31, 35), "pattern": r"12\.\d+\.\d+"},
    "Din Kültürü ve Ahlak Bilgisi": {"slug": "dkab", "sourceId": "tr-meb-dkab-g09-g12-program-2018", "url": "https://mufredat.meb.gov.tr/Dosyalar/20221229134742302-DKAB_(9-12.%20S%C4%B1n%C4%B1f)_DOP_%202018.pdf", "pages": (37, 42), "pattern": r"12\s*[\.,]\s*\d+\s*\.\s*\d+"},
    "Fizik": {"slug": "fizik", "sourceId": "tr-meb-fizik-g09-g12-program-2018", "url": "https://mufredat.meb.gov.tr/Dosyalar/201812103112910-orta%C3%B6%C4%9Fretim_fizik_son.pdf", "pages": (36, 43), "pattern": r"12\.\d+\.\d+\.\d+"},
    "İngilizce": {"slug": "ingilizce", "sourceId": "tr-meb-ingilizce-g09-g12-program-2018", "url": "https://mufredat.meb.gov.tr/Dosyalar/201812020472656-OGM%20INGILIZCE%20PRG%2020.012018.pdf", "pages": (56, 65), "pattern": r"E12\.\d+\.(?:L|SI|SP|R|W)\d+"},
    "Kimya": {"slug": "kimya", "sourceId": "tr-meb-kimya-g09-g12-program-2018", "url": "https://mufredat.meb.gov.tr/Dosyalar/201812102955190-19.01.2018%20Kimya%20Dersi%20%C3%96%C4%9Fretim%20Program%C4%B1.pdf", "pages": (34, 39), "pattern": r"12\.\d+\.\d+\.\d+"},
    "Matematik": {"slug": "matematik", "sourceId": "tr-meb-matematik-g09-g12-program-2018", "url": "https://mufredat.meb.gov.tr/Dosyalar/201821102727101-OGM%20MATEMAT%C4%B0K%20PRG%2020.01.2018.pdf", "pages": (37, 41), "pattern": r"12\.\d+\.\d+\.\d+"},
    "Türk Dili ve Edebiyatı": {"slug": "tde", "sourceId": "tr-meb-tde-g09-g12-program-2018", "url": "https://mufredat.meb.gov.tr/Dosyalar/20221229132522794-T%C3%BCrk%20Dili%20ve%20Edebiyat%C4%B1%20Dersi%20%C3%96%C4%9Fretim%20Program%C4%B1.pdf", "manual": True},
    "T.C. İnkılap Tarihi ve Atatürkçülük": {"slug": "inkilap", "sourceId": "tr-meb-inkilap-g12-program-2018", "url": "https://mufredat.meb.gov.tr/Dosyalar/20221229131923491-T.C.%20%C4%B0nk%C4%B1lap%20Tarihi%20ve%20Atat%C3%BCrk%C3%A7%C3%BCl%C3%BCk%20Dersi%20%C3%96%C4%9Fretim%20Program%C4%B1.pdf", "pages": (21, 28), "pattern": r"[1-8]\.\d+", "codePrefix": "İTA.12."},
    "Mantık": {"slug": "mantik", "sourceId": "tr-meb-mantik-program-2009", "url": "https://mufredat.meb.gov.tr/Dosyalar/2019930144322531-Mant%C4%B1k%20Dersi%20%C3%96%C4%9Fretim%20Program%C4%B1.pdf", "numbered": (21, 32, 53), "prefix": "MAN.12"},
    "Psikoloji": {"slug": "psikoloji", "sourceId": "tr-meb-psikoloji-program-2011", "url": "https://mufredat.meb.gov.tr/Dosyalar/201993014469656-Psikoloji%20Dersi%20%C3%96%C4%9Fretim%20Program%C4%B1nda%20De%C4%9Fi%C5%9Fiklik%20Yap%C4%B1lams%C4%B114.02.11.pdf", "numbered": (13, 32, 59), "prefix": "PSK.12"},
    "Sosyoloji": {"slug": "sosyoloji", "sourceId": "tr-meb-sosyoloji-program-2009", "url": "https://mufredat.meb.gov.tr/Dosyalar/2019930144835783-Sosyoloji%20Dersi%20%C3%96%C4%9Fretim%20Program%C4%B1.pdf", "numbered": (20, 39, 60), "prefix": "SOS.12"},
}

TDE: tuple[tuple[int, str, str], ...] = (
    (57, "TDE.12.1.1", "Edebiyat ile düşünce akımları ve felsefe arasındaki ilişkiyi değerlendirir"),
    (57, "TDE.12.1.2", "Edebiyat ile psikoloji ve psikiyatri arasındaki ilişkiyi değerlendirir"),
    (57, "TDE.12.1.3", "Dilin tarihî süreçte değişimini etkileyen sebepleri açıklar"),
    (57, "TDE.12.1.4", "Türkçenin ilk örneklerden günümüze önemli sözlüklerini tanır"),
    (57, "TDE.12.1.5", "Toplumsal değişme ve teknolojinin dile etkisi hakkında yazı ve sunum hazırlar"),
    (58, "TDE.12.2.1", "1960 sonrası Cumhuriyet Dönemi hikâyelerini anlatım teknikleri bakımından çözümler"),
    (58, "TDE.12.2.2", "Küçürek hikâyenin özelliklerini örnek metinlerde belirler"),
    (58, "TDE.12.2.3", "Hikâye tekniklerini kullanarak özgün hikâye yazar ve dramatize eder"),
    (59, "TDE.12.3.1", "Cumhuriyet Dönemi şiir anlayışlarını metinlerden hareketle ayırt eder"),
    (59, "TDE.12.3.2", "Şiirde tema, yapı, dil, ahenk ve edebî anlayış ilişkisini çözümler"),
    (59, "TDE.12.3.3", "Bir şiiri çözümleyip dönem ve sanatçı bağlamında sözlü olarak sunar"),
    (60, "TDE.12.4.1", "Cumhuriyet Dönemi Türk romanını dönem ve anlayış özellikleriyle değerlendirir"),
    (60, "TDE.12.4.2", "Türk dünyası ve dünya edebiyatı romanlarını yapı ve tema bakımından karşılaştırır"),
    (60, "TDE.12.4.3", "Bir roman hakkında kanıta dayalı tanıtma ve değerlendirme yazısı yazar"),
    (61, "TDE.12.5.1", "1950 sonrası Türk tiyatrosunun farklı anlayışlarını metinlerden ayırt eder"),
    (61, "TDE.12.5.2", "Tiyatro metnini tür özelliklerini koruyarak radyo tiyatrosuna dönüştürür"),
    (61, "TDE.12.5.3", "Radyo tiyatrosunu bilişim araçlarıyla seslendirip sunar"),
    (62, "TDE.12.6.1", "Dünya ve Cumhuriyet Dönemi denemelerini tür özellikleri bakımından çözümler"),
    (62, "TDE.12.6.2", "Özgün bir deneme yazar, gözden geçirir ve sözlü olarak sunar"),
    (63, "TDE.12.7.1", "Türk edebiyatının farklı dönemlerindeki söylev örneklerini karşılaştırır"),
    (63, "TDE.12.7.2", "Söylevde amaç, hedef kitle, kanıt ve hitabet özelliklerini çözümler"),
    (63, "TDE.12.7.3", "Güncel bir konuda söylev metni yazar ve etkili biçimde sunar"),
)


def clean(value: str) -> str:
    value = value.replace("\u00ad", "").replace("\uf048", " ").replace("\uf094", " ").replace("\uf020", " ")
    value = re.sub(r"(?<=\w)-\s+(?=\w)", "", value)
    return re.sub(r"\s+", " ", value).strip(" .;:-")


def title_after(text: str, end: int) -> str:
    tail = text[end:].lstrip(" .,:;-\n")
    terminal = re.search(
        r"\b(?:açıklar|analiz eder|ayırt eder|belirler|değerlendirir|fark eder|"
        r"geliştirir|görür|ifade eder|ilişki kurar|kavrar|karşılaştırır|öğrenir|"
        r"özetler|örnekler verir|sınıflandırır|sembolleştirir|sorgular|tanır|"
        r"tanımlar|tartışır|tespit eder|uygular|yorumlar|yararlanır|bilir|"
        r"bulunur|yapar|çözer|çıkarır|gösterir|dönüştürür|hazırlar|sunar)\s*\.",
        tail,
        flags=re.IGNORECASE,
    )
    title = tail[:terminal.end() - 1] if terminal else re.split(r"[.!?](?:\s|$)", tail, maxsplit=1)[0]
    return clean(title)


def coded(reader: PdfReader, config: dict[str, Any]) -> list[dict[str, Any]]:
    start, end = config["pages"]
    found: list[dict[str, Any]] = []
    seen: set[str] = set()
    regex = re.compile(rf"(?<![\w.])({config['pattern']})\s*\.?")
    for page_number in range(start, end + 1):
        text = reader.pages[page_number - 1].extract_text() or ""
        matches = list(regex.finditer(text))
        for index, match in enumerate(matches):
            compact_code = re.sub(r"\s+", "", match.group(1)).replace("12,", "12.")
            code = config.get("codePrefix", "") + compact_code
            if code in seen:
                continue
            segment_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            title = title_after(text[match.end():segment_end], 0)
            if len(title) < 8 or "ÜNİTE, KAZANIM" in title:
                continue
            seen.add(code)
            found.append({"code": code, "title": title, "page": page_number})
    return found


def numbered(reader: PdfReader, config: dict[str, Any]) -> list[dict[str, Any]]:
    start, end, expected = config["numbered"]
    chunks: list[str] = []
    boundaries: list[tuple[int, int]] = []
    cursor = 0
    for page_number in range(start, end + 1):
        text = reader.pages[page_number - 1].extract_text() or ""
        chunks.append(text)
        boundaries.append((cursor, page_number))
        cursor += len(text) + 1
    merged = "\n".join(chunks)
    output = []
    cursor = 0
    for number in range(1, expected + 1):
        match = re.search(rf"(?<![\d.]){number}\s*\.(?!\d)\s*", merged[cursor:])
        if not match:
            raise ValueError(f"{config['sourceId']}: missing numbered outcome {number}")
        absolute_end = cursor + match.end()
        next_match = (
            re.search(rf"(?<![\d.]){number + 1}\s*\.(?!\d)\s*", merged[absolute_end:])
            if number < expected else None
        )
        segment_end = absolute_end + next_match.start() if next_match else len(merged)
        segment = merged[absolute_end:segment_end].lstrip(" .,:;-\n")
        title = clean(re.split(r"[.!?](?:\s|$)", segment, maxsplit=1)[0])
        if not 8 <= len(title) <= 240:
            raise ValueError(f"{config['sourceId']}:{number}: corrupt title {title!r}")
        page = max(page_number for offset, page_number in boundaries if offset <= absolute_end)
        output.append({"code": f"{config['prefix']}.{number}", "title": title, "page": page})
        cursor = absolute_end
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
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
        reader = PdfReader(path)
        if config.get("manual"):
            objectives = [{"code": code, "title": title, "page": page} for page, code, title in TDE]
        elif config.get("numbered"):
            objectives = numbered(reader, config)
        else:
            objectives = coded(reader, config)
        if not objectives:
            raise ValueError(f"{subject}: no objectives")
        for row in objectives:
            row["objectiveSource"] = config["url"]
            row["objectiveEvidenceId"] = f"{config['sourceId']}:pdf-page-{row.pop('page')}"
        subjects.append({
            "subject": subject,
            "programmeFamily": "pre-TYMM-current",
            "programmeYear": 2018,
            "sourceId": config["sourceId"],
            "sourceUrl": config["url"],
            "sourceSha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "pageCount": len(reader.pages),
            "objectives": objectives,
        })
    payload = {
        "schemaVersion": "alika-tr-current-curriculum/1.0.0",
        "country": "TR", "grade": 12, "schoolYear": "2026-2027",
        "programmeFamily": "pre-TYMM-current", "authority": "T.C. Millî Eğitim Bakanlığı",
        "activationEvidence": [
            "https://tymm.meb.gov.tr/taslak-cerceve-planlari",
            "https://antalyaodm.meb.gov.tr/www/yillik-cerceve-planlar-ve-ogretim-programlari/icerik/49",
        ],
        "subjects": subjects,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"output": str(args.output), "counts": {s["subject"]: len(s["objectives"]) for s in subjects}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
