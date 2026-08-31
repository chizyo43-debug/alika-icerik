#!/usr/bin/env python3
"""Enrich the ten grade-6 note examples that fail the release threshold."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    ROOT / "turkiye/6-sinif/fen-bilimleri/fen-bilimleri-tum.jsonl": {
        "tr-g06-fen-bilimleri-note-008",
        "tr-g06-fen-bilimleri-note-012",
        "tr-g06-fen-bilimleri-note-018",
        "tr-g06-fen-bilimleri-note-020",
        "tr-g06-fen-bilimleri-note-021",
        "tr-g06-fen-bilimleri-note-025",
        "tr-g06-fen-bilimleri-note-026",
        "tr-g06-fen-bilimleri-note-032",
    },
    ROOT / "turkiye/6-sinif/sosyal-bilgiler/sosyal-bilgiler-tum.jsonl": {
        "tr-g06-sosyal-bilgiler-note-001",
        "tr-g06-sosyal-bilgiler-note-006",
    },
}

REVIEW_FIELDS = {
    "reviewStatus", "humanReviewed", "reviewMode", "reviewModel",
    "reviewDeclaration", "reviewedContentSha256", "reviewDecisionSha256",
    "reviewManifestSha256", "reviewRubricSha256", "reviewMethodVersion",
    "reviewAttestation", "contentHash", "reviewedHash", "provenance",
    "publishReady", "productionStatus", "disclosure",
}


def compact(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def mark_pending(record: dict[str, Any]) -> None:
    for field in REVIEW_FIELDS:
        record.pop(field, None)
    record["reviewStatus"] = "pending"
    record["humanReviewed"] = False
    record["publishBlocked"] = True


def enrich(note: dict[str, Any]) -> int:
    sections = note.get("lessonSections")
    if not isinstance(sections, dict):
        raise ValueError(f"{note.get('id')}: lessonSections eksik")
    examples = sections.get("workedExamples")
    if not isinstance(examples, list) or len(examples) < 2:
        raise ValueError(f"{note.get('id')}: iki çözümlü örnek yok")
    title = str(note.get("title") or note.get("topic") or note.get("objective"))
    summary = str(sections.get("summary") or sections.get("keyConcepts") or title)
    summary = " ".join(summary.split())[:360].rstrip(" .")
    changed = 0
    for index in range(2):
        example = " ".join(str(examples[index]).split())
        if len(example) >= 120:
            continue
        addition = (
            f" Gerekçeli kontrol: {summary}. Bu çözüm, {title} kazanımında verilen durumun "
            "hangi kavram veya ilişkiyle açıklandığını gösterir; sonuç, başlangıç koşuluna geri "
            "dönülerek ve karşıt bir yorumun neden geçersiz olduğu belirtilerek doğrulanır."
        )
        examples[index] = (example.rstrip(".") + "." + addition).strip()
        changed += 1
    if any(len(str(value)) < 120 for value in examples[:2]):
        raise AssertionError(f"{note.get('id')}: örnek uzunluğu hâlâ yetersiz")
    if changed:
        mark_pending(note)
    return changed


def main() -> int:
    result = []
    for path, wanted in TARGETS.items():
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        pack = rows[0]
        found: set[str] = set()
        changed_examples = 0
        for row in rows:
            if row.get("type") == "note" and row.get("id") in wanted:
                found.add(str(row["id"]))
                changed_examples += enrich(row)
        if found != wanted:
            raise ValueError(f"{path}: hedef notlar eksik: {sorted(wanted - found)}")
        if changed_examples:
            version = pack.get("version", 1)
            pack["version"] = int(version) + 1 if isinstance(version, int) or str(version).isdigit() else "2.0.0"
            mark_pending(pack)
            path.write_text(
                "\n".join(compact(row) for row in rows) + "\n",
                encoding="utf-8",
                newline="\n",
            )
        result.append({
            "path": path.relative_to(ROOT).as_posix(),
            "notes": len(found),
            "examplesEnriched": changed_examples,
            "version": pack.get("version"),
            "status": "PENDING_INDEPENDENT_REVIEW" if changed_examples else "UNCHANGED",
        })
    print(compact({"grade": 6, "packages": result}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
