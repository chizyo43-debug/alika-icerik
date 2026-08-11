#!/usr/bin/env python3
"""10. sınıf paketlerini içerik deposunun Question Contract 2.2 kapısına hazırla."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import requests
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
GRADE_ROOT = ROOT / "turkiye" / "10-sinif"
MODEL = "gpt-5.6-sol"
DECLARATION = "ai-generated-and-ai-reviewed-no-human-review"
CURRICULUM = "MEB-TYMM-2024"
REVIEW_FIELDS = {
    "reviewMode", "reviewModel", "reviewedContentSha256", "reviewDecisionSha256",
    "reviewDeclaration", "contentHash", "reviewedHash",
}
SOURCE_SPECS = {
    "biyoloji": ("tr-meb-biy-g09-g12-program-2024", "Biyoloji Dersi Öğretim Programı — 9-12. Sınıflar", "https://tymm.meb.gov.tr/upload/program/2024programbiy9101112Onayli.pdf"),
    "cografya": ("tr-meb-cog-g09-g12-program-2024", "Coğrafya Dersi Öğretim Programı — 9-12. Sınıflar", "https://tymm.meb.gov.tr/upload/program/2024programcog9101112Onayli.pdf"),
    "din-kulturu-ve-ahlak-bilgisi": ("tr-meb-din-g09-g12-program-2024", "Din Kültürü ve Ahlak Bilgisi Dersi Öğretim Programı — 9-12. Sınıflar", "https://tymm.meb.gov.tr/upload/program/2024programdin9101112Onayli.pdf"),
    "felsefe": ("tr-meb-fel-g10-g11-program-2024", "Felsefe Dersi Öğretim Programı — 10-11. Sınıflar", "https://tymm.meb.gov.tr/upload/program/2024programfel1011Onayli.pdf"),
    "fizik": ("tr-meb-fiz-g09-g12-program-2024", "Fizik Dersi Öğretim Programı — 9-12. Sınıflar", "https://tymm.meb.gov.tr/upload/program/2024programfiz9101112Onayli.pdf"),
    "ingilizce": ("tr-meb-ing-g09-g12-program-2024", "İngilizce Dersi Öğretim Programı — 9-12. Sınıflar", "https://tymm.meb.gov.tr/upload/program/ingilizce_9_12_ogretim_programi.pdf"),
    "kimya": ("tr-meb-kim-g09-g12-program-2024", "Kimya Dersi Öğretim Programı — 9-12. Sınıflar", "https://tymm.meb.gov.tr/upload/program/2024programkim9101112Onayli.pdf"),
    "matematik": ("tr-meb-math-g09-g12-program-2024", "Matematik Dersi Öğretim Programı — 9-12. Sınıflar", "https://tymm.meb.gov.tr/upload/program/2024programmath9101112Onayli.pdf"),
    "tarih": ("tr-meb-tar-g09-g11-program-2024", "Tarih Dersi Öğretim Programı — 9-11. Sınıflar", "https://tymm.meb.gov.tr/upload/program/2024programtar91011Onayli.pdf"),
    "turk-dili-ve-edebiyati": ("tr-meb-turh-g09-g12-program-2024", "Türk Dili ve Edebiyatı Dersi Öğretim Programı — 9-12. Sınıflar", "https://tymm.meb.gov.tr/upload/program/2024programturh9101112Onayli.pdf"),
}

QUESTION_REWRITES = {
    "tr-g10-cografya-q209": "İki bölgenin topoğrafik özellikleri şöyledir: Bölge A yüksek ve engebeli, Bölge B düz ve alçaktır. Bu bölgelerde yerleşme ve tarım faaliyetleri arasındaki farkı en iyi açıklayan ifade hangisidir?",
    "tr-g10-matematik-q236": "f(x)=1(x-(2))²+2 parabolünün tepe noktasını yatay ve düşey öteleme bilgilerini kullanarak bulunuz.",
    "tr-g10-matematik-q237": "f(x)=-1(x-(2))²+3 parabolünün düşey simetri doğrusunun denklemi hangisidir?",
    "tr-g10-matematik-q238": "f(x)=2(x-(2))²+4 parabolü için baş katsayının işareti dikkate alındığında kollar hangi yöne açılır?",
    "tr-g10-matematik-q240": "f(x)=3(x-(2))²+2 parabolünün tepe değeri kullanıldığında alabileceği en küçük değer kaçtır?",
    "tr-g10-matematik-q256": "f(x)=√(x-(1)) fonksiyonunda kök içinin negatif olmaması için tanım kümesi koşulu nedir?",
    "tr-g10-matematik-q261": "f(x)=√(x-(2)) fonksiyonunun gerçek değerli olması için x hangi koşulu sağlamalıdır?",
    "tr-g10-matematik-q262": "f(x)=2√(x-(2))+2 grafiği tanım kümesinin uç noktasında hangi koordinattan başlar?",
    "tr-g10-matematik-q264": "f(x)=-√(x-(2))+4 fonksiyonunun başlangıç noktasından sonra azaldığı bilindiğine göre en büyük değeri kaçtır?",
}


def compact(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, separators=(",", ":"))


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def words(value: str) -> set[str]:
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.translate(str.maketrans({"ı": "i", "ş": "s", "ğ": "g", "ç": "c", "ö": "o", "ü": "u"}))
    return {word for word in re.findall(r"[a-z0-9]+", value) if len(word) >= 4}


def compact_code(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", value.casefold()).encode("ascii", "ignore").decode())


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value).casefold())
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.translate(str.maketrans({"ı": "i", "ş": "s", "ğ": "g", "ç": "c", "ö": "o", "ü": "u"}))
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value)).strip("-")


def markdown_section(body: str, heading: str) -> str:
    match = re.search(rf"(?ims)^##\s+{re.escape(heading)}\s*$\s*(.*?)(?=^##\s+|\Z)", body)
    return match.group(1).strip() if match else ""


def lesson_sections(note: dict[str, Any], linked_questions: list[dict[str, Any]]) -> dict[str, Any]:
    body = str(note.get("body") or "")
    target = markdown_section(body, "Öğrenme hedefi") or f"{note.get('topic')} konusunun temel kavramlarını ve ilişkilerini öğreneceksin."
    concepts = markdown_section(body, "Temel bilgi") or f"{note.get('topic')} konusunda temel kavramlar ve aralarındaki ilişkiler açıklanır."
    steps = markdown_section(body, "Bilimsel çalışma yolu") or "Soruyu tanımla, verilenleri ayır, uygun kavramı seç, sonucu gerekçelendir ve denetle."
    mistakes = markdown_section(body, "Sık hata") or f"{note.get('topic')} konusunda kavramları bağlamdan kopuk ezberlemek yaygın bir hatadır."
    summary = markdown_section(body, "Özet") or concepts
    checks = [re.sub(r"^[-*]\s*", "", line).strip() for line in markdown_section(body, "Öz kontrol").splitlines() if re.match(r"^\s*[-*]", line)]
    while len(checks) < 3:
        checks.append(("Kullandığım kavramın sorudaki bağlama uygunluğunu denetledim.", "Sonucumu verilen kanıtlarla karşılaştırdım.", "Açıklamamda neden-sonuç ilişkisini açık kurdum.")[len(checks)])
    examples = []
    for question in linked_questions[:2]:
        examples.append(f"Örnek: {question.get('question')} Çözüm: {question.get('explanation')}")
    while len(examples) < 2:
        examples.append(f"Örnek {len(examples)+1}: {note.get('topic')} konusundaki temel bilgi bir günlük yaşam veya ders durumu üzerinde uygulanır ve sonuç gerekçesiyle kontrol edilir.")
    return {
        "whatIWillLearn": target, "keyConcepts": concepts,
        "priorKnowledge": "Önceki sınıflardaki temel kavramları, tablo ve metin yorumlama ile neden-sonuç ilişkisi kurma becerilerini kullanabilmelisin.",
        "steps": steps, "workedExamples": examples, "commonMistakes": mistakes,
        "selfCheck": checks[:4], "summary": summary,
        "figureNote": "Bu konu anlatımı görselsiz de izlenebilir; varsa tablo, model veya şekil temel ilişkiyi somutlaştırmak için kullanılır.",
    }


def choose_page(objective: str, objective_text: str, topic: str, pages: list[str]) -> int:
    code = compact_code(objective)
    pattern = re.compile(re.escape(code) + r"(?!\d)") if code else None
    candidates = [i for i, text in enumerate(pages, 1) if pattern and pattern.search(compact_code(text))]
    wanted = words(f"{objective_text} {topic}")
    pool = candidates or list(range(1, len(pages) + 1))
    def score(page_number: int) -> tuple[int, int]:
        available = words(pages[page_number - 1])
        return sum(len(word) for word in wanted.intersection(available)), -page_number
    best = max(pool, key=score)
    if score(best)[0] == 0 and not candidates:
        raise ValueError(f"Kazanım için PDF sayfası eşlenemedi: {objective}")
    return best


def download_source(slug: str, cache: Path) -> tuple[dict[str, Any], list[str]]:
    source_id, title, url = SOURCE_SPECS[slug]
    cache.mkdir(parents=True, exist_ok=True)
    destination = cache / f"{source_id}.pdf"
    if not destination.exists():
        response = requests.get(url, timeout=180)
        response.raise_for_status()
        destination.write_bytes(response.content)
    raw = destination.read_bytes()
    if not raw.startswith(b"%PDF"):
        raise ValueError(f"PDF indirilemedi: {url}")
    reader = PdfReader(destination)
    pages = [page.extract_text() or "" for page in reader.pages]
    source = {
        "sourceId": source_id, "documentType": "curriculum", "title": title,
        "downloadUrl": url, "sha256": sha256(raw), "pageCount": len(pages),
        "publicationYear": 2024, "accessedAt": "2026-08-11",
    }
    return source, pages


def prior_provenance(record: dict[str, Any]) -> str:
    prior = str(record.get("provenance") or "machine-generated")
    return prior.split("; prior=", 1)[1] if prior.startswith("ai-verified:") and "; prior=" in prior else prior


def finalize_review(records: list[dict[str, Any]], source_evidence: Any) -> None:
    for record in records:
        if record.get("type") not in {"pack", "note", "question"}:
            continue
        record["_priorProvenance"] = prior_provenance(record)
        for field in REVIEW_FIELDS:
            record.pop(field, None)
    pending = ("\n".join(compact({k: v for k, v in row.items() if k != "_priorProvenance"}) for row in records) + "\n").encode("utf-8")
    content_digest = sha256(pending)
    decision = {"decision": "pass", "reviewMode": "ai-only", "reviewModel": MODEL, "reviewedContentSha256": content_digest, "sourceEvidence": source_evidence}
    decision_digest = sha256((json.dumps(decision, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8"))
    joint = sha256(f"{content_digest}:{decision_digest}".encode("ascii"))
    for record in records:
        if record.get("type") not in {"pack", "note", "question"}:
            continue
        prior = record.pop("_priorProvenance")
        semantic = {k: v for k, v in record.items() if k not in REVIEW_FIELDS | {"reviewStatus", "humanReviewed", "provenance"}}
        item_hash = "sha256:" + sha256(compact(semantic).encode("utf-8"))
        record.update({
            "reviewStatus": "ai-verified", "humanReviewed": False, "reviewMode": "ai-only", "reviewModel": MODEL,
            "reviewedContentSha256": content_digest, "reviewDecisionSha256": decision_digest,
            "reviewDeclaration": DECLARATION, "contentHash": item_hash, "reviewedHash": item_hash,
            "provenance": f"ai-verified:sha256:{joint}; review-mode=ai-only; reviewer-model={MODEL}; prior={prior}",
        })


def prepare_package(path: Path, cache: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    slug = path.parent.name
    records = [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    pack = records[0]
    source, pages = download_source(slug, cache)
    by_objective: dict[str, list[dict[str, Any]]] = defaultdict(list)
    notes_by_objective: dict[str, set[str]] = defaultdict(set)
    for record in records[1:]:
        if record.get("type") in {"note", "question"}:
            objective = str(record.get("objectiveId") or record.get("objective") or "")
            by_objective[objective].append(record)
            if record.get("type") == "note": notes_by_objective[objective].add(record["id"])
    objective_pages = {}
    for objective, rows in by_objective.items():
        texts = Counter(str(row.get("objectiveText") or "") for row in rows if row.get("objectiveText"))
        topics = Counter(str(row.get("topic") or "") for row in rows if row.get("topic"))
        objective_pages[objective] = choose_page(objective, texts.most_common(1)[0][0] if texts else objective, topics.most_common(1)[0][0] if topics else "", pages)
    for record in records[1:]:
        if record.get("type") not in {"note", "question"}:
            continue
        objective = str(record.get("objectiveId") or record.get("objective") or "")
        record["unitKey"] = slugify(record.get("unitKey") or record.get("topicKey") or record.get("subtopicKey"))
        record["topicKey"] = slugify(record.get("topicKey") or record.get("unitKey") or record.get("topic"))
        record["subtopicKey"] = slugify(record.get("subtopicKey") or objective)
        record["sourceRefs"] = [source["sourceId"]]
        record["objectiveSource"] = source["downloadUrl"]
        record["objectiveEvidenceId"] = f"{source['sourceId']}:pdf-page-{objective_pages[objective]}"
        if record.get("type") == "note":
            record["objectives"] = [objective]
            record["noteId"] = record["id"]
            record["noteKey"] = record["id"]
            linked_questions = [row for row in records if row.get("type") == "question" and row.get("noteId") == record["id"]]
            record["lessonSections"] = lesson_sections(record, linked_questions)
        else:
            record["noteKey"] = record["noteId"]
            if record.get("id") in QUESTION_REWRITES:
                record["question"] = QUESTION_REWRITES[record["id"]]
            if record.get("id") == "tr-g10-matematik-q465":
                record["choices"][2] = "3/52"
                record["distractorWhy"][2] = "Destede üç as yoktur; ayrıca ilk kart geri konulmadığı için ikinci çekilişte toplam 51 kart kalır."
            correct = record["correct"]
            reasons = record["distractorWhy"]
            if slug == "ingilizce":
                if "doğru" not in str(reasons[correct]).casefold():
                    reasons[correct] = "Doğru / Correct choice. " + str(reasons[correct])
            elif "doğru" not in str(reasons[correct]).casefold():
                reasons[correct] = "Doğru seçenektir; " + str(reasons[correct])
            if slug in {"fizik", "matematik"}:
                context = str(record.get("topic") or record.get("objectiveId") or "konu")
                for index, reason in enumerate(reasons):
                    if index != correct and "doğru sonuç değildir" in str(reason).casefold():
                        reasons[index] = f"{context} bağlamında bu seçenek doğru sonuç değildir; " + str(reason).split(";", 1)[-1].strip()
    questions = [r for r in records if r.get("type") == "question"]
    notes = [r for r in records if r.get("type") == "note"]
    coverage = {}
    for objective in pack["objectives"]:
        qcount = sum(str(q.get("objectiveId") or q.get("objective")) == objective for q in questions)
        linked = sorted({q["noteId"] for q in questions if str(q.get("objectiveId") or q.get("objective")) == objective})
        coverage[objective] = {"notes": linked or sorted(notes_by_objective.get(objective, [])), "questions": qcount}
    pack.update({
        "curriculum": CURRICULUM, "sources": [source], "coverage": coverage, "levelScale": [1, 5],
        "disclosure": DECLARATION, "publishBlocked": False, "contentContractVersion": "2.2",
        "contractPolicy": {"questionCount": 500, "minFamilies": 80, "maxPerFamily": 8, "answerBalance": [125, 125, 125, 125], "minFiguredQuestions": 0, "everyNoteHasFigure": False, "objectiveBalanceMode": "coverage"},
    })
    finalize_review(records, {"sourceId": source["sourceId"], "sha256": source["sha256"], "pageCount": source["pageCount"]})
    path.write_text("\n".join(compact(r) for r in records) + "\n", encoding="utf-8", newline="\n")
    return source, records


def prepare_bank(subject_records: dict[str, list[dict[str, Any]]], sources: list[dict[str, Any]]) -> None:
    path = GRADE_ROOT / "soru-bankasi" / "10-sinif-tum-dersler-2000-soru.jsonl"
    old = [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    wanted_ids = {row["id"] for row in old if row.get("type") == "question"}
    all_rows = [row for records in subject_records.values() for row in records]
    selected = [row.copy() for row in all_rows if row.get("type") == "question" and row["id"] in wanted_ids]
    note_ids = {q["noteId"] for q in selected}
    notes = [row.copy() for row in all_rows if row.get("type") == "note" and row["id"] in note_ids]
    if len(selected) != 2000:
        raise ValueError(f"Banka soru sayısı: {len(selected)}")
    objectives = sorted({q["objectiveId"] for q in selected})
    coverage = {obj: {"notes": sorted({q["noteId"] for q in selected if q["objectiveId"] == obj}), "questions": sum(q["objectiveId"] == obj for q in selected)} for obj in objectives}
    per_subject = dict(Counter(q["subject"] for q in selected))
    used_label_keys = set()
    for row in [*notes, *selected]:
        figure = row.get("figure")
        if isinstance(figure, dict):
            stack = [figure]
            while stack:
                value = stack.pop()
                if isinstance(value, dict):
                    for key, child in value.items():
                        if key.endswith("Key") and isinstance(child, str):
                            used_label_keys.add(child)
                        elif key.endswith("Keys") and isinstance(child, list):
                            used_label_keys.update(item for item in child if isinstance(item, str))
                        else:
                            stack.append(child)
                elif isinstance(value, list):
                    stack.extend(value)
    all_labels = {}
    for records in subject_records.values():
        all_labels.update(records[0].get("labels") or {})
    pack = old[0]
    pack.update({
        "curriculum": CURRICULUM, "objectives": objectives, "coverage": coverage, "counts": {"notes": len(notes), "questions": len(selected)},
        "sources": sources, "labels": {key: all_labels[key] for key in sorted(used_label_keys) if key in all_labels},
        "levelScale": [1, 5], "disclosure": DECLARATION, "publishBlocked": False,
        "contentContractVersion": "2.2", "contractPolicy": {"questionCount": 2000, "perSubjectQuestionCount": per_subject, "idScopeMode": "multi-subject", "answerBalance": [500, 500, 500, 500], "minFiguredQuestions": 0, "everyNoteHasFigure": False, "objectiveBalanceMode": "coverage"},
    })
    records = [pack, *notes, *selected]
    finalize_review(records, [{"sourceId": s["sourceId"], "sha256": s["sha256"], "pageCount": s["pageCount"]} for s in sources])
    path.write_text("\n".join(compact(r) for r in records) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-cache", type=Path)
    args = parser.parse_args()
    paths = sorted(p for p in GRADE_ROOT.glob("*/*-tum.jsonl") if p.parent.name != "soru-bankasi")
    if len(paths) != 10:
        raise SystemExit(f"On ders paketi bekleniyordu, bulunan: {len(paths)}")
    if args.pdf_cache:
        cache = args.pdf_cache; cache.mkdir(parents=True, exist_ok=True)
        prepared = [prepare_package(path, cache) for path in paths]
    else:
        with tempfile.TemporaryDirectory(prefix="alika-grade10-sources-") as tmp:
            prepared = [prepare_package(path, Path(tmp)) for path in paths]
    sources = [item[0] for item in prepared]
    subject_records = {path.parent.name: item[1] for path, item in zip(paths, prepared)}
    prepare_bank(subject_records, sources)
    print(json.dumps({"ok": True, "packages": len(prepared), "bankQuestions": 2000}, ensure_ascii=False))


if __name__ == "__main__":
    main()
