#!/usr/bin/env python3
"""Migrate the remaining Grade 5 English and Social Studies packs to 2.2.

The migration preserves educational wording unless a concrete contract defect
requires a change. It removes legacy hints, adds the stable hierarchy, builds
lesson sections from the existing long-form notes, supplies meaningful note
flows, converts context-rich questions into accessible evidence tables, and
balances correct-answer positions without separating choices from rationales.

English keeps all 18 ENG.5.8.L4 transfer questions. Exactly 18 older questions
are removed with a deterministic selection that retains every family and
objective and removes the required 5/6/4/3 answer-position surplus.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_HASH = (
    "sha256:74b5ee649f01933fd50dfeb7e29706e7dc1ddf0fe3e014ead2fe5cd0896ae7a1"
)
STAMP_FIELDS = (
    "reviewMode",
    "reviewModel",
    "reviewDeclaration",
    "reviewedContentSha256",
    "reviewDecisionSha256",
    "contentHash",
    "reviewedHash",
    "reviewedBy",
)
SECTION_NAMES = (
    "whatIWillLearn",
    "priorKnowledge",
    "keyConcepts",
    "steps",
    "workedExamples",
    "commonMistakes",
    "selfCheck",
    "summary",
    "figureNote",
)
PROMPT_VARIANTS = (
    "Aşağıdaki tabloyu inceleyin.",
    "Aşağıdaki tabloyu inceleyin. Kanıtları birlikte değerlendirin.",
    "Aşağıdaki tabloyu inceleyin. Bilgileri karşılaştırın.",
    "Aşağıdaki tabloyu inceleyin. Açık kanıtlardan yararlanın.",
    "Aşağıdaki tabloyu inceleyin. Verilen ayrıntıları ilişkilendirin.",
    "Aşağıdaki tabloyu inceleyin. Kararınızı tablodaki kanıtlara dayandırın.",
    "Aşağıdaki tabloyu inceleyin. Bütün kanıtları hesaba katın.",
    "Aşağıdaki tabloyu inceleyin. Bilgilerin tümünü birlikte düşünün.",
    "Aşağıdaki tabloyu inceleyin. Kanıtlar arasındaki ilişkiyi belirleyin.",
    "Aşağıdaki tabloyu inceleyin. Önce açık bilgileri ayırın.",
    "Aşağıdaki tabloyu inceleyin. Sonucu bütün verilere dayandırın.",
    "Aşağıdaki tabloyu inceleyin. Ayrıntıları tek tek kontrol edin.",
)
LEGACY_ENGLISH_LABELS = {
    "fig.activity": "Etkinlik",
    "fig.day": "Gün",
    "fig.place": "Yer",
    "fig.item": "Hazırlık",
    "fig.weather": "Hava",
}


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def slug(value: object, limit: int = 54) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    replacements = str.maketrans(
        {"ı": "i", "İ": "i", "ş": "s", "Ş": "s", "ğ": "g", "Ğ": "g"}
    )
    text = text.translate(replacements).casefold()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:limit].rstrip("-") or "konu"


def normalized(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).casefold()
    text = re.sub(r"\d+", "#", text)
    text = re.sub(r"[^\w\s#]", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def label_key(record_id: str, role: str, text: str) -> str:
    digest = hashlib.sha256(f"{role}\0{text}".encode("utf-8")).hexdigest()[:12]
    return f"{record_id}.visual.{digest}"


def add_label(labels: dict, record_id: str, role: str, text: str) -> str:
    key = label_key(record_id, role, text)
    labels[key] = text
    return key


def sentences(text: str) -> list[str]:
    # Avoid splitting common English abbreviations in the source questions.
    protected = (
        str(text or "")
        .replace("P.E.", "P§E§")
        .replace("Mr.", "Mr§")
        .replace("Mrs.", "Mrs§")
    )
    parts = [
        part.replace("§", ".").strip()
        for part in re.split(r"(?<=[.!?])\s+", protected)
        if part.strip()
    ]
    return parts


def paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]


def extract_named_sections(body: str) -> dict[str, str]:
    headings = (
        "Kavramlar",
        "Adım adım öğrenelim",
        "Dil yapısı ve kelimeler",
        "Çözümlü örnek 1",
        "Çözümlü örnek 2",
        "Sık yapılan hata",
        "Öz kontrol",
        "Özet",
        "Görselle çalışma",
    )
    found: list[tuple[int, str, int]] = []
    for heading in headings:
        match = re.search(
            rf"(?im)^\s*(?:#+\s*)?{re.escape(heading)}\s*$", body
        )
        if match:
            found.append((match.start(), heading, match.end()))
    found.sort()
    result: dict[str, str] = {}
    for index, (start, heading, content_start) in enumerate(found):
        end = found[index + 1][0] if index + 1 < len(found) else len(body)
        result[heading] = body[content_start:end].strip()
    return result


def extract_keyword_block(body: str, keywords: tuple[str, ...]) -> str:
    lines = body.splitlines()
    start = None
    for index, line in enumerate(lines):
        clean = line.strip().casefold()
        if clean and any(keyword in clean for keyword in keywords):
            start = index + 1
            break
    if start is None:
        return ""
    collected: list[str] = []
    for line in lines[start:]:
        clean = line.strip()
        if (
            collected
            and len(clean) < 110
            and re.match(r"^(?:\d+[.)]\s*)?[A-ZÇĞİÖŞÜ]", clean)
            and any(
                marker in clean.casefold()
                for marker in (
                    "ön bilgi",
                    "temel kavram",
                    "adım",
                    "örnek",
                    "sık yapılan",
                    "yanılgı",
                    "öz kontrol",
                    "özet",
                )
            )
        ):
            break
        if clean:
            collected.append(clean)
    return "\n".join(collected).strip()


def self_check_items(text: str) -> list[str]:
    candidates = re.findall(
        r"(?:^|\n)\s*(?:\d+[.)]|[-•])\s*(.{15,}?[?!.])(?=\s*(?:\n|$))",
        text,
        flags=re.M,
    )
    if len(candidates) < 3:
        candidates = [
            item.strip()
            for item in sentences(text)
            if len(item.strip()) >= 25
        ]
    return candidates[:8]


def worked_examples(body: str, named: dict[str, str]) -> list[str]:
    examples = [
        named.get("Çözümlü örnek 1", ""),
        named.get("Çözümlü örnek 2", ""),
    ]
    examples = [item for item in examples if item]
    if len(examples) < 2:
        blocks = [
            block
            for block in paragraphs(body)
            if "örnek" in block.casefold() and len(block) >= 80
        ]
        for block in blocks:
            if block not in examples:
                examples.append(block)
            if len(examples) == 2:
                break
    if len(examples) < 2:
        long_parts = [item for item in sentences(body) if len(item) >= 100]
        examples.extend(long_parts[: 2 - len(examples)])
    if len(examples) < 2:
        raise ValueError("Konu anlatımında iki örnek çıkarılamadı.")
    return examples[:2]


def lesson_sections(note: dict, subject: str) -> dict:
    body = str(note.get("body") or "")
    named = extract_named_sections(body)
    body_sentences = [item for item in sentences(body) if len(item) >= 30]
    if len(body_sentences) < 5:
        raise ValueError(f"{note.get('id')}: konu anlatımı çok kısa")

    key_concepts = (
        named.get("Kavramlar")
        or extract_keyword_block(body, ("temel kavram",))
        or "\n".join(body_sentences[:4])
    )
    steps = (
        named.get("Adım adım öğrenelim")
        or extract_keyword_block(body, ("adım adım", "yöntem", "nasıl"))
        or "\n".join(body_sentences[2:8])
    )
    mistakes = (
        named.get("Sık yapılan hata")
        or extract_keyword_block(body, ("sık yapılan", "yanılgı"))
        or body_sentences[-3]
    )
    check_source = (
        named.get("Öz kontrol")
        or extract_keyword_block(body, ("öz kontrol",))
        or "\n".join(body_sentences[-8:])
    )
    checks = self_check_items(check_source)
    if len(checks) < 3:
        checks = [
            f"{note.get('title') or note.get('topic')} konusunun temel kavramlarını açıklayabiliyorum.",
            "Bir örnekteki açık bilgi ile yaptığım yorumu birbirinden ayırabiliyorum.",
            "Sonucumu konu anlatımındaki kural veya kanıtla kontrol edebiliyorum.",
        ]

    intro = body_sentences[0]
    prior = body_sentences[1]
    summary = (
        named.get("Özet")
        or extract_keyword_block(body, ("kısa özet", "sonuç"))
        or " ".join(body_sentences[-2:])
    )
    figure_note = (
        f"Aşağıdaki şemayı inceleyin. Şema, "
        f"{note.get('title') or note.get('topic')} konusunda kanıttan sonuca "
        "giderken izlenecek adımları düzenler."
    )
    return {
        "whatIWillLearn": intro,
        "priorKnowledge": prior,
        "keyConcepts": key_concepts,
        "steps": steps,
        "workedExamples": worked_examples(body, named),
        "commonMistakes": mistakes,
        "selfCheck": checks,
        "summary": summary,
        "figureNote": figure_note,
    }


def note_figure(note: dict, labels: dict) -> dict:
    step_text = note["lessonSections"]["steps"]
    candidates = [
        re.sub(r"^\d+[.)]\s*", "", line.strip())
        for line in step_text.splitlines()
        if len(line.strip()) >= 20
    ]
    if len(candidates) < 4:
        candidates = sentences(step_text)
    candidates = [item[:170] for item in candidates if len(item) >= 20][:4]
    while len(candidates) < 4:
        fallbacks = (
            "Kavramı ve sorunun amacını belirle.",
            "Açık bilgileri veya dil ipuçlarını düzenle.",
            "Seçenekleri kanıtlarla tek tek karşılaştır.",
            "Sonucu konu kuralıyla yeniden doğrula.",
        )
        candidates.append(fallbacks[len(candidates)])
    nodes = []
    for index, text in enumerate(candidates, 1):
        nodes.append(
            {
                "id": f"a{index}",
                "labelKey": add_label(
                    labels, note["id"], f"step-{index}", text
                ),
            }
        )
    alt = " → ".join(candidates)
    return {
        "kind": "flow",
        "nodes": nodes,
        "edges": [
            {"from": f"a{index}", "to": f"a{index + 1}"}
            for index in range(1, len(nodes))
        ],
        "direction": "down",
        "altTextKey": add_label(labels, note["id"], "alt", alt),
    }


def hierarchy(subject: str, objective: str, note: dict) -> dict:
    if subject == "english":
        match = re.match(r"ENG\.5\.(\d+)\.([A-Z]\d+)$", objective)
        if not match:
            raise ValueError(f"İngilizce kazanımı tanınmadı: {objective}")
        unit, strand = match.groups()
        unit_key = f"eng-5-{unit}"
        topic_key = f"{unit_key}-{strand.casefold()}"
    else:
        match = re.match(r"SB\.5\.(\d+)\.(\d+)$", objective)
        if not match:
            raise ValueError(f"Sosyal Bilgiler kazanımı tanınmadı: {objective}")
        unit, outcome = match.groups()
        unit_key = f"sb-5-{unit}"
        topic_key = f"{unit_key}-{outcome}"
    return {
        "unitKey": unit_key,
        "topicKey": topic_key,
        "subtopicKey": slug(note.get("title") or note.get("topic")),
    }


def clear_review_stamp(record: dict, producer: str) -> None:
    for field in STAMP_FIELDS:
        record.pop(field, None)
    record["reviewStatus"] = "pending"
    record["humanReviewed"] = False
    record["provenance"] = (
        f"machine-migrated:{producer}:2026-08; "
        "contract=question-2.2; review=pending"
    )


def question_figure_candidates(questions: list[dict]) -> list[dict]:
    ranked = []
    for question in questions:
        if question.get("figure"):
            continue
        parts = sentences(str(question.get("question") or ""))
        if len(parts) < 2 or "?" not in parts[-1]:
            continue
        evidence = parts[:-1]
        if not (45 <= sum(map(len, evidence)) <= 700):
            continue
        ranked.append(
            (
                -min(len(evidence), 5),
                sum(map(len, evidence)),
                str(question.get("id")),
                question,
            )
        )
    return [entry[-1] for entry in sorted(ranked)]


def set_context_figure(
    question: dict,
    labels: dict,
    evidence: list[str],
    task: str,
    variant: int,
) -> None:
    record_id = question["id"]
    header_order = add_label(labels, record_id, "header-order", "Sıra")
    header_evidence = add_label(labels, record_id, "header-evidence", "Kanıt")
    rows = []
    for index, item in enumerate(evidence, 1):
        order_key = add_label(labels, record_id, f"order-{index}", str(index))
        evidence_key = add_label(
            labels, record_id, f"evidence-{index}", item
        )
        rows.append([{"key": order_key}, {"key": evidence_key}])
    alt = " ".join(
        f"{index}. kanıt: {item}" for index, item in enumerate(evidence, 1)
    )
    question["figure"] = {
        "kind": "table",
        "headerKeys": [header_order, header_evidence],
        "rows": rows,
        "altTextKey": add_label(labels, record_id, "alt", alt),
    }
    question["question"] = (
        f"{PROMPT_VARIANTS[variant % len(PROMPT_VARIANTS)]} {task}"
    )


def move_context_to_figure(question: dict, labels: dict, variant: int) -> None:
    parts = sentences(str(question["question"]))
    set_context_figure(question, labels, parts[:-1], parts[-1], variant)


def normalize_figure_references(
    questions: list[dict], labels: dict
) -> None:
    """Keep every visual explicit and every generated question stem distinct."""
    seen: set[str] = set()
    for ordinal, question in enumerate(
        sorted(questions, key=lambda row: row["id"])
    ):
        figure = question.get("figure")
        if not figure:
            continue
        text = str(question.get("question") or "").strip()
        if figure.get("kind") == "table":
            parts = sentences(text)
            task = parts[-1] if parts else text
            # Existing generated tables use the canonical Sıra/Kanıt headers.
            header_values = [
                labels.get(key, "") for key in figure.get("headerKeys", [])
            ]
            if len(figure.get("headerKeys", [])) == 2 and (
                header_values == ["Sıra", "Kanıt"]
                or not any(header_values)
            ):
                labels[figure["headerKeys"][0]] = "Sıra"
                labels[figure["headerKeys"][1]] = "Kanıt"
                header_values = ["Sıra", "Kanıt"]
            generated = header_values == ["Sıra", "Kanıt"]
            if generated:
                candidate_index = ordinal
                while True:
                    prefix = PROMPT_VARIANTS[
                        candidate_index % len(PROMPT_VARIANTS)
                    ]
                    candidate = f"{prefix} {task}"
                    signature = normalized(candidate)
                    if signature not in seen:
                        text = candidate
                        break
                    candidate_index += 1
            elif not re.search(
                r"\btabloyu\s+(?:dikkatle\s+)?(?:incele|kullan)",
                text,
                flags=re.I,
            ):
                text = f"Aşağıdaki tabloyu inceleyin. {text}"
        elif not re.search(
            r"\b(?:şekli|grafiği|görseli|diyagramı|şemayı)\s+"
            r"(?:incele|kullan|yorumla)",
            text,
            flags=re.I,
        ):
            noun = "şemayı" if figure.get("kind") == "flow" else "görseli"
            text = f"Aşağıdaki {noun} inceleyin. {text}"
        question["question"] = text
        seen.add(normalized(text))


def repair_split_visual_evidence(
    questions: list[dict], labels: dict
) -> None:
    """Move a final evidence line left in the stem back into its table.

    Legacy questions sometimes separate the final evidence item from the
    actual task with a newline instead of sentence punctuation. The original
    sentence splitter therefore treated both as the task. A visual question
    must keep all evidence in the figure and only the answerable instruction
    in the stem.
    """
    for question in questions:
        figure = question.get("figure")
        text = str(question.get("question") or "")
        if (
            not isinstance(figure, dict)
            or figure.get("kind") != "table"
        ):
            continue
        header_values = [
            labels.get(key, "") for key in figure.get("headerKeys", [])
        ]
        if header_values != ["Sıra", "Kanıt"]:
            continue

        prompt = max(
            (item for item in PROMPT_VARIANTS if text.startswith(item)),
            key=len,
            default=None,
        )
        if prompt is None:
            continue

        # A previous migration could have matched the shortest common prompt
        # and accidentally copied the remaining instruction into the table.
        prompt_suffixes = sorted(
            {
                item.removeprefix(PROMPT_VARIANTS[0]).strip()
                for item in PROMPT_VARIANTS
                if item != PROMPT_VARIANTS[0]
            },
            key=len,
            reverse=True,
        )
        for row in figure.get("rows") or []:
            if len(row) < 2:
                continue
            evidence_key = row[1].get("key")
            value = str(labels.get(evidence_key, ""))
            for suffix in prompt_suffixes:
                if value.startswith(suffix):
                    labels[evidence_key] = value[len(suffix) :].strip()
                    break

        remainder = text[len(prompt) :].strip()
        lines = [line.strip() for line in remainder.splitlines() if line.strip()]
        if len(lines) >= 2 and "?" in lines[-1]:
            task = lines[-1]
            dangling = " ".join(lines[:-1]).strip()
            if dangling and dangling.strip("| \t"):
                row_number = len(figure.get("rows") or []) + 1
                order_key = add_label(
                    labels,
                    question["id"],
                    f"order-{row_number}",
                    str(row_number),
                )
                evidence_key = add_label(
                    labels,
                    question["id"],
                    f"evidence-{row_number}",
                    dangling,
                )
                figure.setdefault("rows", []).append(
                    [{"key": order_key}, {"key": evidence_key}]
                )
            question["question"] = f"{prompt} {task}"

        evidence_values = []
        for row in figure.get("rows") or []:
            if len(row) < 2:
                continue
            value = labels.get(row[1].get("key"), "")
            if value:
                evidence_values.append(value)
        alt = " ".join(
            f"{index}. kanıt: {value}"
            for index, value in enumerate(evidence_values, 1)
        )
        figure["altTextKey"] = add_label(
            labels, question["id"], "alt-repaired", alt
        )


def repair_english_language_quality(questions: list[dict]) -> None:
    """Keep solution evidence aligned with the actual English question."""
    special_reasons = {
        "tr.g05.ingilizce.q242": (
            "“Millie is writing her diary now.” doğrudur; “now” devam eden "
            "eylemi gösterdiği için “is writing” şimdiki zaman yapısı "
            "kullanılmalıdır."
        ),
        "tr.g05.ingilizce.q314": (
            "“Mahallede bir yerin varlığı sorulur.” doğrudur; "
            "“Is there ...?” kalıbı, belirli bir yerin çevrede bulunup "
            "bulunmadığını sorar."
        ),
    }
    special_difficulty = {
        "tr.g05.ingilizce.q242": (
            "2 adım gerektirir: “now” zaman ipucunun şimdiki zamanı "
            "gösterdiği belirlenir, ardından özneye uygun “is + fiil-ing” "
            "yapısı seçilir. Ön bilgi olarak şimdiki zaman yapısı gerekir. "
            "Çeldiriciler geniş zaman ve hatalı fiil biçimlerini kullanır."
        ),
        "tr.g05.ingilizce.q314": (
            "2 adım gerektirir: “Is there ...?” yapısının varlık sorguladığı "
            "belirlenir ve “near the square” yer ayrıntısı korunur. Ön bilgi "
            "olarak tekil varlık sorusu yapısı gerekir. "
            "Çeldiriciler cümlenin soru işlevini veya yer bilgisini değiştirir."
        ),
        "tr.g05.ingilizce.q376": (
            "2 adım gerektirir: duyurudaki stands, dishes from different countries ve world "
            "cuisines kanıtlarını birleştirerek etkinliğin temel amacını "
            "özetlemek gerekir. Ön bilgi olarak etkinlik duyurusunda ana fikir "
            "bulma becerisi gerekir. Çeldiriciler etkinliğin yerini, türünü "
            "veya sunulan deneyimi değiştirir."
        ),
        "tr.g05.ingilizce.q481": (
            "2 adım gerektirir: gezi programındaki gün sırası izlenir ve "
            "“final day” bilgisi son durakla eşleştirilir. Ön bilgi olarak "
            "sıralama ve zaman ifadeleri gerekir. Çeldiriciler önceki "
            "günlerdeki yerleri son günle karıştırır."
        ),
    }
    for question in questions:
        for field in ("explanation", "difficultyReason"):
            value = question.get(field)
            if isinstance(value, str):
                question[field] = re.sub(
                    r"(?<![A-Za-zÇĞİÖŞÜçğıöşü])ngilizce\b",
                    "İngilizce",
                    value,
                )
        reasons = question.get("distractorWhy") or []
        question["distractorWhy"] = [
            re.sub(
                r"(?<![A-Za-zÇĞİÖŞÜçğıöşü])ngilizce\b",
                "İngilizce",
                str(reason),
            )
            for reason in reasons
        ]

        if question["id"] in special_difficulty:
            question["difficultyReason"] = special_difficulty[question["id"]]

        explanation = str(question.get("explanation") or "").strip()
        if question["id"] in special_reasons:
            explanation = special_reasons[question["id"]]
        elif "ipuçları birlikte değerlendirilir" in explanation:
            match = re.search(
                r"Ön bilgi olarak şu ölçüt gerekir:\s*(.+?)\s+Çeldiriciler",
                str(question.get("difficultyReason") or ""),
            )
            if match:
                answer = str(question["choices"][question["correct"]])
                explanation = f"“{answer}” doğrudur; {match.group(1).strip()}"
        question["explanation"] = explanation

        correct = question["correct"]
        if explanation:
            answer = str(question["choices"][correct])
            question["distractorWhy"][correct] = (
                f"Doğru; “{answer}” seçeneği sorudaki kanıtla uyumludur. "
                f"{explanation}"
            )

        text = str(question.get("question") or "")
        text = text.replace(
            "Aşağıdaki tabloyu inceleyin. Aşağıdaki tabloya göre",
            "Aşağıdaki tabloyu inceleyin. Tabloya göre",
        )
        question["question"] = text


def repair_social_current_facts(questions: list[dict]) -> None:
    """Replace obsolete claims and overstatements with current, cautious facts."""
    by_id = {question["id"]: question for question in questions}

    residence = by_id["tr-g05-sosyal-q367"]
    residence.update(
        {
            "title": "Yerleşim Yeri Belgesini Çevrim İçi Alma",
            "question": (
                "Yılmaz ailesi barkodlu yerleşim yeri (ikametgâh) belgesini "
                "evden almak istemektedir. Aşağıdaki resmî hizmetlerden "
                "hangisini kullanmalıdır?"
            ),
            "choices": [
                "Belediyenin etkinlik sayfası",
                "Okulun öğrenci bilgi sistemi",
                "e-Devlet Kapısı",
                "Vergi dairesinin ödeme sayfası",
            ],
            "correct": 2,
            "difficultyReason": (
                "Belgeyi düzenleyen resmî dijital hizmeti, başka kamu "
                "kurumlarının çevrim içi hizmetlerinden ayırt etmeyi gerektirir."
            ),
            "explanation": (
                "Yerleşim yeri ve diğer adres belgesi, Nüfus ve Vatandaşlık "
                "İşleri Genel Müdürlüğünün e-Devlet Kapısı hizmetinden "
                "barkodlu olarak oluşturulabilir."
            ),
            "distractorWhy": [
                "Belediye etkinlik sayfası yerleşim yeri belgesi oluşturmaz.",
                "Okulun öğrenci sistemi yalnız eğitim kayıtlarıyla ilgilidir.",
                (
                    "Doğru; e-Devlet Kapısı'ndaki Nüfus ve Vatandaşlık İşleri "
                    "hizmeti barkodlu yerleşim yeri belgesi oluşturur."
                ),
                "Vergi dairesinin ödeme sayfası adres belgesi oluşturmaz.",
            ],
        }
    )

    neighbourhood = by_id["tr-g05-sosyal-q371"]
    neighbourhood.update(
        {
            "title": "Mahalle Dayanışması İçin Muhtara Başvuru",
            "question": (
                "Aşağıdaki durumlardan hangisinde mahalle muhtarına başvurmak "
                "en uygun ilk adımlardan biridir?"
            ),
            "choices": [
                "Pasaport başvurusu yapmak",
                "Trafik kazası için olay yeri tutanağı hazırlatmak",
                (
                    "Mahalledeki ihtiyaç sahipleri için dayanışma çalışmasını "
                    "yerel olarak koordine etmek"
                ),
                "Gelir vergisi borcunu ödemek",
            ],
            "correct": 2,
            "difficultyReason": (
                "Muhtarın mahalle düzeyindeki iletişim ve koordinasyon rolünü "
                "başka kurumların resmî görevlerinden ayırt etmeyi gerektirir."
            ),
            "explanation": (
                "Muhtar, mahalle halkını ve yerel ihtiyaçları yakından tanıyan "
                "bir kamu görevlisidir. Mahalle dayanışmasının ilgili kurumlar "
                "ve gönüllülerle koordine edilmesinde uygun bir başvuru noktasıdır."
            ),
            "distractorWhy": [
                "Pasaport işlemleri nüfus müdürlüklerinde yürütülür.",
                "Trafik kazası tutanağı muhtarlığın görevi değildir.",
                (
                    "Doğru; muhtar mahalle ihtiyaçlarının belirlenmesi ve yerel "
                    "dayanışmanın koordinasyonunda uygun bir başvuru noktasıdır."
                ),
                "Vergi ödemeleri vergi idaresinin hizmetleri üzerinden yapılır.",
            ],
        }
    )

    hazard = by_id["tr-g05-sosyal-q148"]
    hazard["question"] = hazard["question"].replace(
        "ilinin yüksek riskli bölgede olduğunu",
        "ilinde deprem tehlikesinin yüksek olduğunu",
    )
    hazard["explanation"] = (
        "AFAD'ın deprem tehlike haritası, bir yerde deprem yer hareketlerinin "
        "ne ölçüde güçlü olabileceğine ilişkin tehlike bilgisini gösterir; "
        "tek başına bina dayanıklılığını veya oluşacak zararı göstermez. "
        "Tehlikenin yüksek olması, hazırlık ve farkındalık çalışmalarının "
        "önemini artırır."
    )
    hazard["distractorWhy"][hazard["correct"]] = (
        "Doğru; yüksek deprem tehlikesi hazırlık ve farkındalık "
        "çalışmalarını önemli hâle getirir."
    )

    catalhoyuk = by_id["tr-g05-sosyal-q230"]
    catalhoyuk["explanation"] = (
        "Evlerin benzer büyüklükte ve düzende olması ile saray gibi belirgin "
        "ayrıcalık yapılarının bulunmaması, görünür statü farklarının sınırlı "
        "olabileceğini düşündürür. Bulgular daha eşitlikçi bir yaşam yorumunu "
        "destekler; ancak tek başına özel mülkiyetin bulunmadığını kanıtlamaz."
    )
    catalhoyuk["distractorWhy"][catalhoyuk["correct"]] = (
        "Doğru; benzer evler ve belirgin ayrıcalık yapılarının bulunmaması, "
        "statü farklarının sınırlı olabileceğine işaret eder."
    )

    technology = by_id["tr-g05-sosyal-q477"]
    technology["explanation"] = (
        "Bilgisayar oyunlarına gereğinden fazla zaman ayırmak; ders, uyku, "
        "hareket ve yüz yüze iletişim için ayrılan zamanı azaltabilir. Diğer "
        "seçenekler teknolojinin sağlık, eğitim ve güvenlik alanındaki olumlu "
        "kullanımlarına örnektir."
    )
    technology["distractorWhy"][technology["correct"]] = (
        "Doğru; aşırı oyun süresi günlük sorumluluklar, hareket ve sosyal "
        "iletişim için ayrılan zamanı azaltabilir."
    )


def repair_missing_inline_figure(
    question: dict, labels: dict, variant: int
) -> bool:
    """Turn an inline 'Verilen ...:' datum into the table it promises."""
    if question.get("figure"):
        return False
    text = str(question.get("question") or "")
    match = re.search(r"\s+(Verilen\s+[^:]{2,40}:\s*.+)$", text, flags=re.I)
    if "aşağıdaki tabloda" not in text.casefold() or not match:
        return False
    task = text[: match.start()].strip()
    task = re.sub(
        r"^Aşağıdaki tabloda\s+", "Tabloda ", task, flags=re.I
    )
    set_context_figure(
        question, labels, [match.group(1).strip()], task, variant
    )
    return True


def choose_english_removals(questions: list[dict]) -> set[str]:
    legacy = [q for q in questions if not q["id"].endswith(tuple(
        f"{number:03d}" for number in range(501, 519)
    ))]
    if len(legacy) != 500:
        raise ValueError("İngilizce eski 500 soru bloğu belirlenemedi.")
    required_by_correct = {0: 5, 1: 6, 2: 4, 3: 3}
    family_counts = Counter(q["familyId"] for q in questions)
    objective_counts = Counter(q["objective"] for q in questions)
    signatures = Counter(normalized(q["question"]) for q in questions)
    choice_use = Counter(
        tuple(sorted(normalized(choice) for choice in q["choices"]))
        for q in questions
    )

    ranked: list[tuple[tuple[int, int, int, str], dict]] = []
    for q in legacy:
        removable = (
            family_counts[q["familyId"]] > 1
            and objective_counts[q["objective"]] > 2
        )
        if not removable:
            continue
        score = (
            signatures[normalized(q["question"])] - 1,
            choice_use[
                tuple(sorted(normalized(choice) for choice in q["choices"]))
            ]
            - 1,
            family_counts[q["familyId"]],
            q["id"],
        )
        ranked.append((score, q))
    ranked.sort(reverse=True, key=lambda item: item[0])

    selected: set[str] = set()
    selected_families = Counter()
    selected_objectives = Counter()
    remaining = dict(required_by_correct)
    for _score, q in ranked:
        position = q["correct"]
        if remaining.get(position, 0) <= 0:
            continue
        if family_counts[q["familyId"]] - selected_families[q["familyId"]] <= 1:
            continue
        if objective_counts[q["objective"]] - selected_objectives[q["objective"]] <= 2:
            continue
        selected.add(q["id"])
        selected_families[q["familyId"]] += 1
        selected_objectives[q["objective"]] += 1
        remaining[position] -= 1
        if not any(remaining.values()):
            break
    if any(remaining.values()) or len(selected) != 18:
        raise ValueError(f"İngilizce 18 soru seçilemedi: kalan={remaining}")
    return selected


def rotate_choices(question: dict, target: int) -> None:
    source = question["correct"]
    if source == target:
        return
    shift = (target - source) % 4
    choices = list(question["choices"])
    reasons = list(question["distractorWhy"])
    question["choices"] = [choices[(index - shift) % 4] for index in range(4)]
    question["distractorWhy"] = [
        reasons[(index - shift) % 4] for index in range(4)
    ]
    question["correct"] = target


def balance_answers(questions: list[dict]) -> None:
    target = [125, 125, 125, 125]
    counts = Counter(q["correct"] for q in questions)
    excess = [
        position
        for position in range(4)
        for _ in range(max(0, counts[position] - target[position]))
    ]
    missing = [
        position
        for position in range(4)
        for _ in range(max(0, target[position] - counts[position]))
    ]
    if len(excess) != len(missing):
        raise ValueError(f"Cevap dağılımı dengelenemiyor: {counts}")
    used = set()
    for source, destination in zip(excess, missing):
        question = next(
            q
            for q in sorted(questions, key=lambda row: row["id"], reverse=True)
            if q["correct"] == source and q["id"] not in used
        )
        rotate_choices(question, destination)
        used.add(question["id"])


def coverage(questions: list[dict], notes: list[dict]) -> dict:
    note_by_objective: dict[str, list[str]] = defaultdict(list)
    for note in notes:
        for objective in note.get("objectives") or [note.get("objective")]:
            if objective and note["id"] not in note_by_objective[objective]:
                note_by_objective[objective].append(note["id"])
    counts = Counter(q["objective"] for q in questions)
    return {
        objective: {
            "notes": note_by_objective[objective],
            "questions": counts[objective],
        }
        for objective in sorted(counts)
    }


def migrate(path: Path, subject: str, *, write: bool) -> dict:
    rows = read_jsonl(path)
    pack = next(row for row in rows if row.get("type") == "pack")
    notes = [row for row in rows if row.get("type") == "note"]
    questions = [row for row in rows if row.get("type") == "question"]

    removed: set[str] = set()
    if subject == "english":
        if len(questions) == 518:
            removed = choose_english_removals(questions)
            rows = [
                row
                for row in rows
                if row.get("type") != "question" or row["id"] not in removed
            ]
            questions = [row for row in questions if row["id"] not in removed]
        elif len(questions) != 500:
            raise ValueError(
                f"İngilizce geçişi 518 veya 500 soru bekliyor: "
                f"{len(questions)}"
            )
    if len(questions) != 500:
        raise ValueError(f"{subject}: 500 soru bekleniyor, bulunan {len(questions)}")

    labels = dict(pack.get("labels") or {})
    if subject == "english":
        for key, value in LEGACY_ENGLISH_LABELS.items():
            labels.setdefault(key, value)
    note_by_id = {note["id"]: note for note in notes}
    producer = "chatgpt-pro;repair=codex-sol"
    for note in notes:
        objective = str(
            note.get("objective")
            or (note.get("objectives") or [""])[0]
        )
        note["objectives"] = list(dict.fromkeys(
            note.get("objectives") or [objective]
        ))
        note["noteId"] = note["id"]
        note["noteKey"] = note["id"]
        note.update(hierarchy(subject, objective, note))
        note["lessonSections"] = lesson_sections(note, subject)
        note["figure"] = note_figure(note, labels)
        figure_note = note["lessonSections"]["figureNote"]
        body = str(note.get("body") or "").rstrip()
        if not re.search(
            r"\bşemayı\s+(?:incele|kullan|yorumla)", body, flags=re.I
        ):
            note["body"] = f"{body}\n\nGörselle çalışma\n{figure_note}"
        note["sourceRefs"] = list(note.get("sourceRefs") or [])
        clear_review_stamp(note, producer)

    for question in questions:
        question.pop("hints", None)
        note = note_by_id.get(question.get("noteId"))
        if note is None:
            raise ValueError(f"{question['id']}: noteId bulunamadı")
        question["noteKey"] = question["noteId"]
        question.update(hierarchy(subject, question["objective"], note))
        question["sourceRefs"] = list(question.get("sourceRefs") or [])
        if not question["sourceRefs"]:
            raise ValueError(f"{question['id']}: sourceRefs boş")
        correct = question["correct"]
        if "doğru" not in str(question["distractorWhy"][correct]).casefold():
            question["distractorWhy"][correct] = (
                "Doğru; " + str(question["distractorWhy"][correct]).strip()
            )
        clear_review_stamp(question, producer)

    balance_answers(questions)
    for index, question in enumerate(questions):
        repair_missing_inline_figure(question, labels, index)
    already_figured = sum(bool(q.get("figure")) for q in questions)
    needed = max(0, 100 - already_figured)
    candidates = question_figure_candidates(questions)
    if len(candidates) < needed:
        raise ValueError(
            f"{subject}: {needed} yeni görsel için yalnız "
            f"{len(candidates)} güvenli bağlam sorusu bulundu"
        )
    for index, question in enumerate(candidates[:needed]):
        move_context_to_figure(question, labels, index)
    normalize_figure_references(questions, labels)
    repair_split_visual_evidence(questions, labels)
    if subject == "english":
        repair_english_language_quality(questions)
    elif subject == "social":
        repair_social_current_facts(questions)

    if subject == "social":
        replacements = {
            "tr-g05-sosyal-q372": (
                "İl Millî Eğitim Müdürlüğü",
                "İl Millî Eğitim Müdürlüğü okul ve eğitim hizmetleriyle "
                "ilgilenir; park aydınlatması belediyenin yerel hizmetidir.",
            ),
            "tr-g05-sosyal-q374": (
                "Belediye Başkanlığı",
                "Belediye Başkanlığı yerel hizmetleri yürütür; okul disiplin "
                "başvurusunun ikinci basamağı ilçe millî eğitim müdürlüğüdür.",
            ),
            "tr-g05-sosyal-q381": (
                "Nüfus Müdürlüğü",
                "Nüfus Müdürlüğü kimlik ve nüfus işlemlerini yürütür; mahalle "
                "parkındaki bakım sorununun ilk başvuru yeri değildir.",
            ),
        }
        for question in questions:
            replacement = replacements.get(question["id"])
            if not replacement:
                continue
            try:
                position = [
                    str(choice).casefold()
                    for choice in question["choices"]
                ].index("valilik")
            except ValueError:
                continue
            question["choices"][position] = replacement[0]
            question["distractorWhy"][position] = replacement[1]

    pack["schemaVersion"] = "2.2"
    pack["contentContractVersion"] = "2.2"
    pack["contentContractHash"] = CONTRACT_HASH
    pack["version"] = max(int(pack.get("version") or 0), 2)
    used_label_keys: set[str] = set()
    for record in [*notes, *questions]:
        figure = record.get("figure")
        if not isinstance(figure, dict):
            continue
        stack: list[object] = [figure]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                for key, item in value.items():
                    if (
                        (key == "key" or key.endswith("Key"))
                        and isinstance(item, str)
                    ):
                        used_label_keys.add(item)
                    stack.append(item)
            elif isinstance(value, list):
                stack.extend(value)
            elif isinstance(value, str) and value in labels:
                used_label_keys.add(value)
    pack["labels"] = {
        key: labels[key] for key in sorted(used_label_keys) if key in labels
    }
    pack["coverage"] = coverage(questions, notes)
    pack["objectives"] = sorted(pack["coverage"])
    pack["counts"] = {"notes": len(notes), "questions": len(questions)}
    pack["disclosure"] = "ai-generated-and-ai-reviewed-no-human-review"
    pack["publishBlocked"] = False
    pack["reviewStatus"] = "pending"
    pack["humanReviewed"] = False
    for field in STAMP_FIELDS:
        pack.pop(field, None)
    pack["provenance"] = (
        "machine-migrated:codex-sol:2026-08; "
        "contract=question-2.2; review=pending"
    )
    pack["visualPolicy"] = {
        "version": "1.0",
        "everyNote": True,
        "questionMinimumPercent": 20,
        "balancedByObjective": True,
        "rationale": (
            "Görseller yalnız bağlamdaki kanıtları düzenlediğinde kullanılır; "
            "soru metni görseldeki veriye açıkça bağlanır."
        ),
    }
    pack["contractPolicy"] = {
        "questionCount": 500,
        "minFamilies": 80,
        "maxPerFamily": 8,
        "answerBalance": [125, 125, 125, 125],
        "minFiguredQuestions": 100,
        "everyNoteHasFigure": True,
        "objectiveBalanceMode": "coverage",
    }

    # Remove the malformed legacy key while retaining its value if present.
    if subject == "social":
        for row in rows:
            if "sourceCitation\n" in row:
                row.setdefault("sourceCitation", row.pop("sourceCitation\n"))

    result = {
        "subject": subject,
        "notes": len(notes),
        "questions": len(questions),
        "families": len({q["familyId"] for q in questions}),
        "answerBalance": [
            sum(q["correct"] == position for q in questions)
            for position in range(4)
        ],
        "noteFigures": sum(bool(n.get("figure")) for n in notes),
        "questionFigures": sum(bool(q.get("figure")) for q in questions),
        "removed": sorted(removed),
    }
    if result["families"] < 80:
        raise ValueError(f"{subject}: aile sayısı 80 altında")
    if max(Counter(q["familyId"] for q in questions).values()) > 8:
        raise ValueError(f"{subject}: aile tavanı aşıldı")
    if result["answerBalance"] != [125, 125, 125, 125]:
        raise ValueError(f"{subject}: cevap dağılımı bozuk")
    if write:
        write_jsonl(path, rows)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    targets = (
        (
            ROOT
            / "turkiye"
            / "5-sinif"
            / "ingilizce"
            / "ingilizce-tum.jsonl",
            "english",
        ),
        (
            ROOT
            / "turkiye"
            / "5-sinif"
            / "sosyal-bilgiler"
            / "sosyal-bilgiler-tum.jsonl",
            "social",
        ),
    )
    for path, subject in targets:
        print(json.dumps(
            migrate(path, subject, write=args.write),
            ensure_ascii=False,
            indent=2,
        ))
    if not args.write:
        print("(dosyaları yazmak için --write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
