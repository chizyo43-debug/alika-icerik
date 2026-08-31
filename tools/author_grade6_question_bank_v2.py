#!/usr/bin/env python3
"""Author grade-6 bank items from distinct lesson-note knowledge cards.

Unlike the retired worked-example repeater, this producer consumes a different
fact, definition, worked rule, or bilingual example for every question.  It
never reads lesson question rows.  Visuals in this stage are evidence tables;
geographic and scientific visual families are added only through the common
Figure Spec routing pipeline after their data contract is complete.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from author_grade6_question_bank import (
    AUTHORING_ROOT, GRADE_ROOT, LABEL_PATH, QUESTION_PATH, SUBJECT_QUOTAS,
    allocate, batch_schedule, clean, read_pack_and_notes,
)


STOP = {
    "acaba", "adım", "ayrıca", "başlamadan", "belirle", "bilgiler", "bilgiyi",
    "bir", "biz", "bölümde", "bölüm", "burada", "bütün", "cevap", "çözüm",
    "doğru", "edecek", "ederek", "edilir", "gerekir", "göre", "hangi", "için",
    "ilgili", "ilişkiyi", "kadar", "kavramlar", "kendi", "konu", "konuda",
    "konusunu", "kontrol", "kullanarak", "öğrenci", "öğrenece", "örnek", "önce",
    "olarak", "olan", "olduğunu", "şekilde", "seçenek", "sonra", "sonuç",
    "temel", "verilen", "yalnız", "yapılan", "yerine",
}
GENERIC_LABELS = re.compile(
    r"(?i)^(?:örnek|çözüm|amaç|materyal|cevap|diyalog|adım|soru|özet|etkinlik)\b"
)
GENERIC_SENTENCE = re.compile(
    r"(?i)öğrenece|kendi cümlelerimle|doğru seçenek ile|bu bölüme başlamadan|"
    r"önce soruda verilen|seçenekleri tek tek|konu anlatımındaki ilke|öz kontrol"
)


@dataclass(frozen=True)
class Card:
    kind: str
    evidence: str
    answer: str
    alternatives: tuple[str, ...]
    explanation: str


def literal(value: str) -> str:
    return re.sub(r"[^\w]+", " ", value.casefold()).strip()


def strip_markdown(value: str) -> str:
    value = re.sub(r"(?m)^#{1,6}\s*", "", value)
    value = re.sub(r"\*\*|`", "", value)
    value = re.sub(r"(?m)^\s*[-*]\s*", "", value)
    return re.sub(r"\s+", " ", value).strip()


def definitions(body: str) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    pattern = re.compile(
        r"(?m)^\s*(?:[-*]|\d+[.)])?\s*\*\*([^*\n:]{2,80}):?\*\*\s*"
        r"(?:[:\-]\s*)?([^\n]{3,500})"
    )
    for label, description in pattern.findall(body):
        label, description = clean(label), clean(description)
        if (GENERIC_LABELS.search(label) or len(label.split()) > 9
                or not 3 <= len(description) <= 420):
            continue
        pair = (label, description)
        if pair not in result:
            result.append(pair)
    return result


def english_examples(body: str) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for english, turkish in re.findall(
        r"(?m)^\s*\d+\.\s+([A-Z][^\n(]{4,180})\s*\(([^)\n]{3,180})\)", body
    ):
        pair = (clean(english).rstrip("."), clean(turkish).rstrip("."))
        if pair not in result:
            result.append(pair)
    return result


def sentences(body: str) -> list[str]:
    text = strip_markdown(body)
    result: list[str] = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        sentence = sentence.strip()
        if (not 48 <= len(sentence) <= 320 or "?" in sentence
                or GENERIC_SENTENCE.search(sentence)):
            continue
        if literal(sentence) not in {literal(old) for old in result}:
            result.append(sentence)
    return result


def stem(value: str) -> str:
    value = value.casefold()
    for suffix in ("leriniz", "larınız", "lerinin", "larının", "lerden", "lardan",
                   "lerin", "ların", "leri", "ları", "ler", "lar", "nin", "nın",
                   "nun", "nün", "in", "ın", "un", "ün", "i", "ı", "u", "ü"):
        if len(value) - len(suffix) >= 4 and value.endswith(suffix):
            return value[:-len(suffix)]
    return value


def glossary(body: str, title: str, definition_rows: list[tuple[str, str]]) -> list[str]:
    text = strip_markdown(body)
    counts = Counter(
        word.casefold() for word in re.findall(
            r"[A-Za-zÇĞİÖŞÜçğıöşü][A-Za-zÇĞİÖŞÜçğıöşü'’\-]{3,}", text
        ) if word.casefold() not in STOP
    )
    candidates = [label for label, _ in definition_rows]
    candidates.extend(re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü]{4,}", title))
    candidates.extend(word for word, count in counts.most_common() if count >= 2)
    result: list[str] = []
    seen_stems: set[str] = set()
    for value in candidates:
        value = clean(value)
        key = stem(value)
        if (not 4 <= len(value) <= 48 or key in STOP or key in seen_stems
                or GENERIC_LABELS.search(value)):
            continue
        seen_stems.add(key)
        result.append(value)
    return result


def build_cards(note: dict[str, Any]) -> list[Card]:
    body = str(note.get("body") or "")
    definition_rows = definitions(body)
    terms = glossary(body, str(note.get("title") or ""), definition_rows)
    cards: list[Card] = []

    definition_terms = [label for label, _ in definition_rows]
    for label, description in definition_rows:
        alternatives = [term for term in definition_terms if stem(term) != stem(label)]
        alternatives.extend(term for term in terms if stem(term) != stem(label))
        alternatives = list(dict.fromkeys(alternatives))
        if len(alternatives) >= 3:
            cards.append(Card("definition", description, label, tuple(alternatives),
                              f"{label}: {description}"))

    if str(note.get("subject")) == "İngilizce":
        bilingual = english_examples(body)
        english_values = [english for english, _ in bilingual]
        for english, turkish in bilingual:
            alternatives = [value for value in english_values if literal(value) != literal(english)]
            if len(alternatives) >= 3:
                cards.append(Card("translation", turkish, english, tuple(alternatives),
                                  f"‘{english}’ ifadesinin Türkçe anlamı ‘{turkish}’ biçimindedir."))

    for sentence in sentences(body):
        hits = [term for term in terms if re.search(rf"(?i)\b{re.escape(term)}\b", sentence)]
        hits.sort(key=lambda value: (len(value.split()), len(value)), reverse=True)
        chosen = next((value for value in hits if len(value) >= 4), None)
        if not chosen:
            continue
        alternatives = [
            value for value in terms
            if stem(value) != stem(chosen) and abs(len(value.split()) - len(chosen.split())) <= 1
        ]
        if len(alternatives) < 3:
            continue
        evidence = re.sub(rf"(?i)\b{re.escape(chosen)}\b", "____", sentence)
        if evidence == sentence:
            continue
        cards.append(Card("cloze", evidence, chosen, tuple(alternatives), sentence))

    unique: list[Card] = []
    seen: set[tuple[str, str]] = set()
    for card in cards:
        key = (literal(card.answer), literal(card.explanation))
        if key not in seen:
            seen.add(key)
            unique.append(card)
    return unique


def evidence_table(qid: str, evidence: str, labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2 = f"{prefix}.h1", f"{prefix}.h2"
    r1, r2 = f"{prefix}.r1", f"{prefix}.r2"
    e1, e2 = f"{prefix}.e1", f"{prefix}.e2"
    alt = f"{prefix}.alt"
    labels.update({
        h1: "Bilgi kartı", h2: "Tamamlanacak bölüm", r1: "Kanıt", r2: "Eksik kavram",
        e1: evidence, e2: "?",
        alt: "Bir konu cümlesindeki kanıtı ve tamamlanacak kavram alanını gösteren iki satırlı tablo; doğru seçenek işaretlenmemiştir.",
    })
    return {"kind": "table", "headerKeys": [h1, h2],
            "rows": [[{"key": r1}, {"key": e1}], [{"key": r2}, {"key": e2}]],
            "altTextKey": alt}


def make_question(note: dict[str, Any], card: Card, number: int, local: int,
                  mode: str, level: int, correct: int, labels: dict[str, str]) -> dict[str, Any]:
    qid = f"tr-g06-bank-q{number:04d}"
    distractors = list(card.alternatives)
    distractors.sort(key=lambda value: hashlib.sha256(f"{qid}:{value}".encode()).hexdigest())
    wrongs = distractors[:3]
    choices = wrongs.copy(); choices.insert(correct, card.answer)
    mistaken = wrongs[local % 3]
    if card.kind == "translation":
        core = f"Which sentence means “{card.evidence}” in English?"
    else:
        core = f"Aşağıdaki bilgi kartındaki boşluğu doğru tamamlayan kavram hangisidir? {card.evidence}"
    if mode == "application":
        core = ("Bir öğrenci konu anlatımındaki bilgiyi yeni bir sınıflandırma kartına aktarıyor. " + core)
    elif mode == "analysis":
        core = ("Bilgi kartındaki tanım, ilişki ve bağlam birlikte çözümlenecektir. " + core)
    elif mode == "error-analysis":
        core = (f"Bir öğrenci boşluğa “{mistaken}” yazmıştır. Bu yanlış yanıtı düzelten seçenek hangisidir? "
                f"Karttaki kanıt: {card.evidence}")
    use_figure = mode == "analysis" or local % 4 == 0
    figure = evidence_table(qid, card.evidence, labels) if use_figure else None
    if figure:
        core = "Aşağıdaki tabloyu inceleyiniz. " + core
    reasons = []
    wrong_index = 0
    for index, choice in enumerate(choices):
        if index == correct:
            reasons.append(f"Doğru kavram ilişkisi: {card.explanation}")
        else:
            reasons.append(
                f"Kavram değiştirme yanılgısı: ‘{choice}’ karttaki tanım veya ilişkiyi karşılamaz; "
                f"doğru ilişki {card.explanation}"
            )
            wrong_index += 1
    objective = str(note.get("objective") or note.get("objectiveId"))
    visual = ({"level": "required", "role": "evidence",
               "rationale": "Kanıt cümlesi ve eksik kavram alanı yalnız tabloda birlikte sunulur.",
               "acceptableKinds": ["table"], "evidenceDimensions": ["kanıt", "kavram"]}
              if figure else {"level": "none", "role": "none",
               "rationale": "Gerekli tanım ve ilişki soru metninde eksiksizdir.",
               "acceptableKinds": [], "evidenceDimensions": []})
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": number,
        "subject": note.get("subject"), "grade": 6, "unitKey": note.get("unitKey"),
        "topicKey": note.get("topicKey"), "subtopicKey": note.get("subtopicKey"),
        "topic": note.get("topic"), "title": f"{note.get('title')} — {mode}",
        "objective": objective, "objectiveId": objective, "noteId": note.get("id"),
        "noteKey": note.get("id"), "question": core, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct], "distractorWhy": reasons,
        "explanation": card.explanation.rstrip(".!?…") + ".",
        "level": level,
        "difficultyReason": (f"Düzey {level}; öğrenci {note.get('title')} bağlamındaki özgün bilgi kartında "
                             f"tanım, kanıt ve kavram eşleşmesini {mode} biçiminde kurar."),
        "questionType": mode, "familyId": f"tr-g06-bank-family-{number:04d}",
        "objectiveSource": note.get("objectiveSource"),
        "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": list(note.get("sourceRefs") or []), "visualNeed": visual, "figure": figure,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    subject_data: dict[str, list[dict[str, Any]]] = {}
    for path in sorted(GRADE_ROOT.glob("*/*-tum.jsonl")):
        if path.parent.name == "soru-bankasi":
            continue
        pack, notes = read_pack_and_notes(path)
        subject_data[str(pack["subject"])] = notes
    if set(subject_data) != set(SUBJECT_QUOTAS):
        raise ValueError("6. sınıf ders kapsamı eksik")

    labels: dict[str, str] = {}
    questions: list[dict[str, Any]] = []
    number = 0
    for subject, quota in SUBJECT_QUOTAS.items():
        notes = subject_data[subject]
        allocations = allocate(quota, notes)
        for note in notes:
            needed = allocations[str(note["id"])]
            cards = build_cards(note)
            if len(cards) < needed:
                raise ValueError(f"{note['id']}: {len(cards)}/{needed} benzersiz bilgi kartı")
            selected = sorted(
                cards,
                key=lambda card: hashlib.sha256(
                    f"{note['id']}:{card.kind}:{card.evidence}:{card.answer}".encode()
                ).hexdigest(),
            )[:needed]
            for local, card in enumerate(selected):
                number += 1
                batch = (number - 1) // 100
                offset = (number - 1) % 100
                modes = batch_schedule(batch, [("comprehension", 25), ("application", 35),
                                                ("analysis", 25), ("error-analysis", 15)], "g6-v2-mode")
                levels = batch_schedule(batch, [(1, 20), (2, 25), (3, 30), (4, 20), (5, 5)], "g6-v2-level")
                answers = batch_schedule(batch, [(0, 25), (1, 25), (2, 25), (3, 25)], "g6-v2-answer")
                questions.append(make_question(note, card, number, local, modes[offset],
                                               levels[offset], answers[offset], labels))
    if number != 2000:
        raise AssertionError(number)
    AUTHORING_ROOT.mkdir(parents=True, exist_ok=True)
    QUESTION_PATH.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":"))
                                       for row in questions) + "\n", encoding="utf-8", newline="\n")
    LABEL_PATH.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                          encoding="utf-8", newline="\n")
    print(json.dumps({"grade": 6, "questions": len(questions), "labels": len(labels),
                      "status": "PENDING_REVIEW", "sourceQuestionRecordsRead": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
