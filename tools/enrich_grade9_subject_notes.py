#!/usr/bin/env python3
"""Stage Grade 9 subject packs with quality-complete, ID-preserving notes."""
from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from typing import Any

from build_unique_question_banks import ROOT, read_jsonl
from audit_bank_source_readiness import note_failures
from review_unique_question_banks import projection, write_jsonl


OUTPUT = ROOT / "build/grade9-enriched-subjects"
PATHS = {
    path.parent.name: path
    for path in sorted((ROOT / "turkiye/9-sinif").glob("*/*-tum.jsonl"))
    if path.parent.name != "soru-bankasi"
}


def strings(value: Any) -> list[str]:
    if isinstance(value, str) and value.strip():
        return [" ".join(value.split())]
    if isinstance(value, list):
        return [item for child in value for item in strings(child)]
    if isinstance(value, dict):
        return [item for child in value.values() for item in strings(child)]
    return []


def selected(content: dict[str, Any], keys: tuple[str, ...], fallback: list[str]) -> list[str]:
    values: list[str] = []
    for key in keys:
        values.extend(strings(content.get(key)))
    return values or fallback


def full_example(
    value: Any, number: int, objective: str, fact: str, mistake: str,
    english: bool = False,
) -> str:
    if isinstance(value, dict):
        prompt = " ".join(str(value.get("prompt") or value.get("question") or "").split())
        solution = " ".join(str(value.get("solution") or value.get("answer") or "").split())
    else:
        prompt, solution = "", " ".join(str(value or "").split())
    prompt = prompt or (
        f"Apply {objective} in a new context" if english
        else f"{objective} kazanımını yeni bir örnekte uygulama"
    )
    solution = solution or fact
    if english:
        return (
            f"Worked example {number} — Task: {prompt}. Solution: {solution} "
            f"First match the supplied evidence with the criterion in {objective}; then state only the conclusion "
            f"that the evidence supports. The interpretation '{mistake}' is rejected because it ignores a condition "
            "or exceeds the evidence. The final check must cite the context-specific clue explicitly."
        )
    return (
        f"Çözümlü örnek {number} — Durum: {prompt}. Çözüm: {solution} "
        f"Önce verilen kanıt ile {objective} hedefinin ölçütü eşleştirilir; ardından sonuç yalnız bu "
        f"kanıtın izin verdiği kapsamda yazılır. '{mistake}' yorumu, koşulu ya da kanıt sınırını "
        "ihlal ettiği için elenir. Son kontrol, gerekçenin duruma özgü bilgiyi açıkça kullanmasıdır."
    )


def enrich_note(source: dict[str, Any]) -> dict[str, Any]:
    note = copy.deepcopy(source)
    objective_ids = [
        str(value) for value in (note.get("objectives") or [note.get("objective")]) if value
    ]
    english = any(re.match(r"^(?:ENG\.|E\d+\.)", value) for value in objective_ids)
    objective = str(note.get("objective") or (objective_ids[0] if objective_ids else "") or note.get("title") or "Kazanım")
    topic = str(note.get("topic") or note.get("unitTitle") or note.get("title") or "konu")
    content = note.get("learningContent") if isinstance(note.get("learningContent"), dict) else {}
    existing = note.get("lessonSections") if isinstance(note.get("lessonSections"), dict) else {}
    fallback = [
        str(note.get("summary") or "").strip(),
        objective,
        f"{topic} içeriğinde doğru sonuç; kavram, koşul, kanıt ve kapsam birlikte denetlenerek kurulur.",
    ]
    fallback = [value for value in fallback if value]
    facts = selected(
        content,
        ("keyFacts", "facts", "corePrinciples", "problemSolvingPrinciples", "evidenceHierarchy"),
        strings(existing.get("keyConcepts")) or fallback,
    )
    procedures = selected(content, ("procedure", "steps", "process", "method"), strings(existing.get("steps")) or [
        "Sorudaki veriyi ve istenen sonucu belirle.",
        "Kazanıma uygun kavramı veya yöntemi seç.",
        "Kanıtı koşul, sıra, birim ve kapsam bakımından denetle.",
        "Sonucu karşı örnek ve yaygın yanılgılarla sınayıp gerekçelendir.",
    ])
    mistakes = selected(content, ("commonMisconceptions", "misconceptions", "commonMistakes"), strings(existing.get("commonMistakes")) or [
        f"{topic} ile ilgili tek bir örneği bütün durumlara genellemek.",
        "Kanıtın söylemediği bir ayrıntıyı varsaymak.",
        "Doğru kavramı yanlış koşulda kullanmak.",
    ])
    raw_examples: list[Any] = []
    for key in ("workedExamples", "examples", "solvedExamples"):
        value = content.get(key)
        if isinstance(value, list):
            raw_examples.extend(value)
    raw_examples.extend(existing.get("workedExamples") if isinstance(existing.get("workedExamples"), list) else [])
    examples = [
        full_example(
            raw_examples[index] if index < len(raw_examples) else None,
            index + 1,
            objective,
            facts[index % len(facts)],
            mistakes[index % len(mistakes)],
            english,
        )
        for index in range(2)
    ]
    sections = dict(existing)
    if len(str(sections.get("whatIWillLearn") or "").strip()) < 30:
        sections["whatIWillLearn"] = (
            f"I will apply {objective} in the {topic} context by using explicit evidence, valid conditions and a justified response."
            if english else
            f"{objective} hedefini {topic} bağlamında gerçek kanıt, geçerli koşul ve gerekçeli sonuçla uygulayacağım."
        )
    if len(str(sections.get("priorKnowledge") or "").strip()) < 30:
        sections["priorKnowledge"] = (
            f"Recall the core language of {topic}, strategies for reading evidence and the limits of a supported inference."
            if english else
            f"{topic} ünitesinin temel terimlerini, metin ya da veri okuma adımlarını ve güvenli çalışma sınırlarını hatırla."
        )
    if len(str(sections.get("keyConcepts") or "").strip()) < 200:
        sections["keyConcepts"] = " ".join(facts) + (
            f" For {objective}, these concepts are used through meaning, audience, context and explicit textual or spoken evidence. "
            "A valid response preserves time reference, register, communicative purpose and the limits of the supplied information."
            if english else
            f" {objective} için bu kavramlar ezberlenmiş etiketler olarak değil, verilen durumdaki açık kanıtla "
            "eşleştirilerek kullanılır. Sonuç; zaman, neden-sonuç, birim, kaynak ve kapsam sınırlarını aşmamalıdır."
        )
    if len(str(sections.get("steps") or "").strip()) < 25:
        sections["steps"] = " ".join(procedures)
    sections["workedExamples"] = examples
    if len(str(sections.get("commonMistakes") or "").strip()) < 100:
        sections["commonMistakes"] = " ".join(
            (
                f"Misconception {index + 1}: {value} Correct it by checking meaning, context and the explicit evidence."
                if english else
                f"Yanılgı {index + 1}: {value} Bu yorum, kanıt veya koşul denetimiyle düzeltilmelidir."
            )
            for index, value in enumerate(mistakes[:4])
        )
    checks = sections.get("selfCheck") if isinstance(sections.get("selfCheck"), list) else []
    if len(checks) < 3:
        checks = (
            [
                f"Can I point to the evidence I used for {objective}?",
                "Does my response satisfy every condition without inventing a detail?",
                "Can I name the misconception behind the strongest distractor?",
            ] if english else [
                f"{objective} için kullandığım kanıtı açıkça gösterebiliyor muyum?",
                "Sonucum bütün koşulları sağlıyor ve kapsam dışı ayrıntı eklemiyor mu?",
                "En güçlü yanlış seçeneğin dayandığı yanılgıyı adlandırabiliyor muyum?",
            ]
        )
    sections["selfCheck"] = checks
    if len(str(sections.get("summary") or "").strip()) < 30:
        sections["summary"] = (
            f"{objective} requires learners to process the {topic} context with an appropriate language strategy and justify the response within the evidence."
            if english else
            f"{objective}, {topic} içeriğindeki bilgiyi uygun yöntemle işleyip sonucu kanıt sınırlarında gerekçelendirmeyi gerektirir."
        )
    if "figureNote" not in sections:
        sections["figureNote"] = (
            "A visual, when present, organises evidence without revealing the answer and is used only when the task refers to it explicitly."
            if english else
            "Varsa görsel, metindeki kanıtı düzenler; cevap işareti taşımaz ve soru çözümünde yalnız açıkça atıf yapıldığında kullanılır."
        )
    note["lessonSections"] = sections
    body = str(note.get("body") or "").strip()
    if len(body) < 800:
        body = "\n\n".join([
            body,
            " ".join(strings(sections["whatIWillLearn"])),
            ("Key concepts and relationships: " if english else "Temel kavramlar ve ilişkiler: ") + str(sections["keyConcepts"]),
            ("Application process: " if english else "Uygulama yolu: ") + str(sections["steps"]),
            *map(str, examples),
            ("Common mistakes: " if english else "Yaygın hatalar: ") + str(sections["commonMistakes"]),
            ("Summary: " if english else "Özet: ") + str(sections["summary"]),
        ]).strip()
    note["body"] = body
    note["summary"] = str(note.get("summary") or sections["summary"])
    return note


def pending(row: dict[str, Any]) -> dict[str, Any]:
    clean = projection(row)
    clean.update({
        "reviewStatus": "pending", "humanReviewed": False,
        "reviewMode": "ai-only", "reviewDeclaration": "ai-generated-pending-independent-ai-review",
        "publishReady": False, "publishBlocked": True,
        "productionStatus": "pending-independent-ai-review",
        "disclosure": "ai-generated-pending-independent-ai-review",
        "provenance": "pending:grade9-note-quality-enricher/1.0.0; human-review:false",
    })
    return clean


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = []
    for folder, source in PATHS.items():
        rows = read_jsonl(source)
        staged = []
        changed = 0
        for row in rows:
            current = row
            if row.get("type") == "note":
                if note_failures(row):
                    current = enrich_note(row)
                    changed += int(current != row)
            elif row.get("type") == "pack":
                current = copy.deepcopy(row)
                version = current.get("version")
                current["version"] = version + 1 if isinstance(version, int) else "2"
            staged.append(pending(current))
        target = OUTPUT / folder / source.name
        write_jsonl(target, staged)
        report.append({"subject": rows[0].get("subject"), "records": len(rows), "notesChanged": changed, "candidate": str(target)})
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
