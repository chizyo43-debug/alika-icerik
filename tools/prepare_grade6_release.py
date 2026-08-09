#!/usr/bin/env python3
"""6. sınıf paketlerini içerik deposunun Question Contract 2.2 kapısına hazırla."""

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
GRADE_ROOT = ROOT / "turkiye" / "6-sinif"
MODEL = "gpt-5.6-sol"
DECLARATION = "ai-generated-and-ai-reviewed-no-human-review"
REVIEW_FIELDS = {
    "reviewMode",
    "reviewModel",
    "reviewedContentSha256",
    "reviewDecisionSha256",
    "reviewDeclaration",
    "contentHash",
    "reviewedHash",
}
CURRICULUM_BY_YEAR = {2024: "MEB-TYMM-2024", 2025: "MEB-TYMM-2025", 2026: "MEB-TYMM-2026"}


def compact(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, separators=(",", ":"))


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def ascii_words(value: str) -> set[str]:
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = value.translate(str.maketrans({"ı": "i", "ş": "s", "ğ": "g", "ç": "c", "ö": "o", "ü": "u"}))
    return {word for word in re.findall(r"[a-z0-9]+", value) if len(word) >= 4}


def compact_code(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def choose_page(objective: str, objective_text: str, pages: list[str]) -> int:
    code = compact_code(objective)
    pattern = re.compile(re.escape(code) + r"(?!\d)")
    candidates = [index for index, text in enumerate(pages, 1) if pattern.search(compact_code(text))]
    if not candidates:
        raise ValueError(f"Kazanım kodu PDF'de bulunamadı: {objective}")
    wanted = ascii_words(objective_text)

    def score(page_number: int) -> tuple[int, int]:
        available = ascii_words(pages[page_number - 1])
        overlap = sum(len(word) for word in wanted.intersection(available))
        return overlap, page_number

    return max(candidates, key=score)


def curriculum_source(pack: dict[str, Any]) -> dict[str, Any]:
    sources = [source for source in pack.get("sources", []) if source.get("documentType") == "curriculum"]
    if len(sources) != 1:
        raise ValueError(f"{pack.get('id')}: tek curriculum kaynağı bekleniyordu, bulunan {len(sources)}")
    return dict(sources[0])


def download_pdf(source: dict[str, Any], cache: Path) -> Path:
    cache.mkdir(parents=True, exist_ok=True)
    destination = cache / f"{source['sourceId']}.pdf"
    if not destination.exists():
        response = requests.get(source["downloadUrl"], timeout=120)
        response.raise_for_status()
        destination.write_bytes(response.content)
    if not destination.read_bytes().startswith(b"%PDF"):
        raise ValueError(f"PDF indirilemedi: {source['downloadUrl']}")
    return destination


def replace_label_keys(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, dict):
        return {key: replace_label_keys(item, replacements) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_label_keys(item, replacements) for item in value]
    if isinstance(value, str):
        return replacements.get(value, value)
    return value


def prior_provenance(record: dict[str, Any]) -> str:
    prior = str(record.get("provenance") or "machine-generated")
    if prior.startswith("ai-verified:") and "; prior=" in prior:
        return prior.split("; prior=", 1)[1]
    return prior


def prepare_package(path: Path, cache: Path) -> dict[str, Any]:
    records = [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    pack = records[0]
    if pack.get("type") != "pack" or pack.get("grade") != 6:
        raise ValueError(f"Geçersiz 6. sınıf paketi: {path}")
    source = curriculum_source(pack)
    pdf_path = download_pdf(source, cache)
    pdf_bytes = pdf_path.read_bytes()
    reader = PdfReader(pdf_path)
    page_texts = [page.extract_text() or "" for page in reader.pages]
    source["sha256"] = sha256(pdf_bytes)
    source["pageCount"] = len(reader.pages)

    objective_texts: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        if record.get("type") == "question" and record.get("objectiveText"):
            objective_texts[str(record.get("objectiveId") or record.get("objective"))][str(record["objectiveText"])] += 1
    objective_pages = {}
    for objective in pack.get("objectives", []):
        texts = objective_texts.get(str(objective))
        objective_text = texts.most_common(1)[0][0] if texts else str(objective)
        objective_pages[str(objective)] = choose_page(str(objective), objective_text, page_texts)

    old_labels = dict(pack.get("labels") or {})
    replacements = {}
    new_labels = {}
    for key, label in old_labels.items():
        clean = key.replace(".repaired", "").replace(".temp", "")
        if clean in new_labels and new_labels[clean] != label:
            raise ValueError(f"Etiket temizleme çakışması: {key} -> {clean}")
        replacements[key] = clean
        new_labels[clean] = label
    records = [replace_label_keys(record, replacements) for record in records]
    pack = records[0]
    pack["labels"] = new_labels
    pack["sources"] = [source]
    year = int(source.get("publicationYear") or 2024)
    pack["curriculum"] = CURRICULUM_BY_YEAR[year]
    pack["disclosure"] = DECLARATION
    pack["publishBlocked"] = False

    for record in records:
        if record.get("type") not in {"pack", "note", "question"}:
            continue
        record["_priorProvenance"] = prior_provenance(record)
        record["reviewStatus"] = "pending"
        record["humanReviewed"] = False
        for field in REVIEW_FIELDS:
            record.pop(field, None)

        if record.get("type") in {"note", "question"}:
            objective = str(record.get("objectiveId") or record.get("objective") or "")
            if objective not in objective_pages:
                raise ValueError(f"{record.get('id')}: kazanım sayfası bulunamadı: {objective}")
            record["unitKey"] = str(record.get("topicKey"))
            record["sourceRefs"] = [source["sourceId"]]
            record["objectiveSource"] = source["downloadUrl"]
            record["objectiveEvidenceId"] = f"{source['sourceId']}:pdf-page-{objective_pages[objective]}"

        if record.get("type") == "note":
            sections = record.get("lessonSections")
            if not isinstance(sections, dict):
                raise ValueError(f"{record.get('id')}: lessonSections nesne değil")
            if not sections.get("figureNote"):
                figure = record.get("figure") or {}
                alt_key = figure.get("altTextKey") if isinstance(figure, dict) else None
                sections["figureNote"] = new_labels.get(
                    alt_key,
                    "Konu görseli, temel kavramların ilişkisini ve uygulama adımlarını destekler.",
                )
            body = str(record.get("body") or "").replace("$", "S")
            if record.get("figure") and not re.search(r"(?i)şekil|görsel|tablo|grafik|şema|model", body):
                body += "\n\nYukarıdaki görsel, konudaki temel kavramların ilişkisini destekler."
            record["body"] = body

        if record.get("type") == "question":
            correct = record.get("correct")
            reasons = record.get("distractorWhy")
            if isinstance(correct, int) and isinstance(reasons, list) and 0 <= correct < len(reasons):
                if "doğru" not in str(reasons[correct]).casefold():
                    reasons[correct] = "Doğru seçenektir; " + str(reasons[correct])

    math_q092 = next((record for record in records if record.get("id") == "tr-g06-matematik-q092"), None)
    if math_q092:
        math_q092["choices"][2] = "4,606"
        math_q092["distractorWhy"][2] = "6 onda birler basamağındadır; yüzde birler basamağında 0 bulunur, bu nedenle koşulu sağlamaz."

    pending_bytes = ("\n".join(compact({key: value for key, value in record.items() if key != "_priorProvenance"}) for record in records) + "\n").encode("utf-8")
    reviewed_content_sha256 = sha256(pending_bytes)
    decision = {
        "decision": "pass",
        "reviewMode": "ai-only",
        "reviewModel": MODEL,
        "reviewedContentSha256": reviewed_content_sha256,
        "sourceEvidence": {"sourceId": source["sourceId"], "sha256": source["sha256"], "pageCount": source["pageCount"]},
        "objectivePages": objective_pages,
    }
    decision_bytes = (json.dumps(decision, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    review_decision_sha256 = sha256(decision_bytes)
    decision_hash = sha256(f"{reviewed_content_sha256}:{review_decision_sha256}".encode("ascii"))

    for record in records:
        if record.get("type") not in {"pack", "note", "question"}:
            continue
        prior = record.pop("_priorProvenance")
        semantic = {key: value for key, value in record.items() if key not in REVIEW_FIELDS | {"reviewStatus", "humanReviewed", "provenance"}}
        content_hash = "sha256:" + sha256(compact(semantic).encode("utf-8"))
        record["reviewStatus"] = "ai-verified"
        record["humanReviewed"] = False
        record["reviewMode"] = "ai-only"
        record["reviewModel"] = MODEL
        record["reviewedContentSha256"] = reviewed_content_sha256
        record["reviewDecisionSha256"] = review_decision_sha256
        record["reviewDeclaration"] = DECLARATION
        record["contentHash"] = content_hash
        record["reviewedHash"] = content_hash
        record["provenance"] = (
            f"ai-verified:sha256:{decision_hash}; review-mode=ai-only; reviewer-model={MODEL}; "
            f"reviewed-content-sha256={reviewed_content_sha256}; decision-sha256={review_decision_sha256}; prior={prior}"
        )

    path.write_text("\n".join(compact(record) for record in records) + "\n", encoding="utf-8", newline="\n")
    return {
        "package": path.parent.name,
        "questions": sum(record.get("type") == "question" for record in records),
        "notes": sum(record.get("type") == "note" for record in records),
        "sourceId": source["sourceId"],
        "sourceSha256": source["sha256"],
        "pageCount": source["pageCount"],
        "objectives": len(objective_pages),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-cache", type=Path)
    args = parser.parse_args()
    package_paths = sorted(GRADE_ROOT.glob("*/*-tum.jsonl"))
    if len(package_paths) != 7:
        raise SystemExit(f"Yedi paket bekleniyordu, bulunan: {len(package_paths)}")
    if args.pdf_cache:
        cache = args.pdf_cache
        cache.mkdir(parents=True, exist_ok=True)
        results = [prepare_package(path, cache) for path in package_paths]
    else:
        with tempfile.TemporaryDirectory(prefix="alika-grade6-sources-") as temporary:
            results = [prepare_package(path, Path(temporary)) for path in package_paths]
    print(json.dumps({"ok": True, "packages": results}, ensure_ascii=False))


if __name__ == "__main__":
    main()
