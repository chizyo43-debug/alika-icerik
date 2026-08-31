#!/usr/bin/env python3
"""Build non-copying, note-linked 2,000-question banks for grades 5–12.

The builder is deliberately unable to publish.  It writes a pending candidate
in 100-question batches; ``review_unique_question_banks.py`` owns the separate,
hash-bound release decision. Subject questions are used only for curriculum
grounding and copy detection; complete bank questions come from independent
authoring records.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import shutil
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
AUTHORING_DIR = ROOT / "authoring" / "question-bank-blueprints"
TARGET = 2_000
BATCH = 100
SUBJECT_MIN = 100
SUBJECT_MAX = 600
CONTRACT_HASH = "sha256:74b5ee649f01933fd50dfeb7e29706e7dc1ddf0fe3e014ead2fe5cd0896ae7a1"
METHOD = "alika-note-grounded-unique-bank-builder/2.0.0"
CURRENT_CURRICULUM_BLOCKS: dict[int, str] = {}
REVIEW_FIELDS = {
    "aiReviewStatus", "aiVerification", "aiVerified", "approvalGranted",
    "approvalStatus", "approvedBy", "attestation", "contentHash", "disclosure",
    "humanReviewed", "provenance", "publishBlocked", "publishReady", "publishable",
    "review", "reviewAttestation", "reviewDecisionSha256", "reviewDeclaration",
    "reviewManifestSha256", "reviewMethodVersion", "reviewMode", "reviewModel",
    "reviewRubricSha256", "reviewStatus", "reviewSummary", "reviewedBy",
    "reviewedContentSha256", "reviewedHash", "verifiedBy", "workflowState",
    "productionStatus",
}
MIX_RATIOS = {
    "comprehension": 0.25,
    "application": 0.35,
    "analysis": 0.25,
    "error-analysis": 0.15,
}
DIFFICULTY_RATIOS = {
    "5-7": (0.20, 0.25, 0.30, 0.20, 0.05),
    "8-10": (0.15, 0.25, 0.30, 0.20, 0.10),
    "11-12": (0.10, 0.20, 0.30, 0.25, 0.15),
}
STEM_OPENERS = (
    "Kazanım kartını dikkatle inceleyen bir öğrenci şu problemi çözüyor",
    "Ders sonundaki öz değerlendirmede aşağıdaki durum ele alınıyor",
    "Konu anlatımındaki kavramlar yeni bir durumda sınanıyor",
    "Bir çalışma grubunda aşağıdaki problem için gerekçeli yanıt aranıyor",
    "Öğrenci, öğrendiği bilgiyi aşağıdaki bağlama aktarmak istiyor",
    "Sınıf içi tartışmada aşağıdaki soruya kanıta dayalı yanıt veriliyor",
    "Kavram yanılgılarını ayırmak için aşağıdaki durum değerlendiriliyor",
    "Çözümlü örnekten sonra benzer olmayan şu durum inceleniyor",
    "Bir deneme oturumunda aşağıdaki problem adım adım çözümleniyor",
    "Öğrenme günlüğünde aşağıdaki soruya uygun sonuç aranıyor",
    "İki farklı çözüm yolu karşılaştırılırken şu problem kullanılıyor",
    "Konuya özgü ölçütler kullanılarak aşağıdaki durum yorumlanıyor",
)
REASONING_LENSES = (
    "kavram ile örnek arasındaki bağ", "verilen koşulların tümü", "neden-sonuç ilişkisi",
    "gözlem ile çıkarım ayrımı", "tanımın ayırt edici özelliği", "işlem sırasının gerekçesi",
    "kanıtın desteklediği sonuç", "genellemenin geçerlilik sınırı", "temsil ile gerçek durum ilişkisi",
    "karşı örnek olasılığı", "birim ve nicelik uyumu", "metindeki bağlam ipuçları",
    "zaman ve sıra ilişkisi", "sınıflandırma ölçütü", "değişkenler arasındaki ilişki",
    "ifadenin amaç ve hedefe uygunluğu",
)


@dataclass
class SubjectData:
    path: Path
    pack: dict[str, Any]
    notes: list[dict[str, Any]]
    questions: list[dict[str, Any]]
    by_objective: dict[str, list[dict[str, Any]]]

    @property
    def subject(self) -> str:
        return str(self.pack["subject"])


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def load_authored_blueprints(grade: int) -> list[dict[str, Any]]:
    """Load independently authored questions; never derive them from lesson questions."""
    path = AUTHORING_DIR / f"grade-{grade}.jsonl"
    if not path.exists():
        return []
    rows = read_jsonl(path)
    if any(row.get("type") != "question" for row in rows):
        raise ValueError(f"{path}: only complete question records are allowed")
    ids = [str(row.get("id") or "") for row in rows]
    if any(not value for value in ids) or len(set(ids)) != len(ids):
        raise ValueError(f"{path}: question ids must be present and unique")
    return rows


def load_authored_labels(grade: int) -> dict[str, Any]:
    path = AUTHORING_DIR / f"grade-{grade}-labels.json"
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: label file must be a JSON object")
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def combined_curriculum(subjects: list[SubjectData]) -> str:
    """Return the validator-supported curriculum id for a mixed-subject bank."""
    values = {str(subject.pack.get("curriculum") or "").strip() for subject in subjects}
    if "" in values:
        raise ValueError("subject pack curriculum is missing")
    if len(values) == 1:
        return next(iter(values))
    years: set[str] = set()
    for value in values:
        if not value.startswith("MEB-TYMM-"):
            raise ValueError(f"unsupported mixed curriculum set: {sorted(values)}")
        years.update(re.findall(r"20\d{2}", value))
    if not years:
        raise ValueError(f"curriculum year missing: {sorted(values)}")
    return "MEB-TYMM-" + "+".join(sorted(years))


def pending(row: dict[str, Any]) -> dict[str, Any]:
    clean = {key: copy.deepcopy(value) for key, value in row.items() if key not in REVIEW_FIELDS}
    clean.update({
        "reviewStatus": "pending",
        "humanReviewed": False,
        "reviewMode": "ai-only",
        "reviewDeclaration": "ai-generated-pending-independent-ai-review",
        "disclosure": "ai-generated-pending-independent-ai-review",
        "publishReady": False,
        "publishBlocked": True,
        "provenance": f"pending:{METHOD}; human-review:false",
    })
    return clean


def objective_of(question: dict[str, Any]) -> str:
    # ``objective`` is display text in several legacy lesson packages, while
    # ``objectiveId`` remains the canonical curriculum code.  Prefer the ID so
    # prose descriptions cannot inflate the quota universe as fake outcomes.
    value = question.get("objectiveId") or question.get("objective")
    if not isinstance(value, str) or not value.strip() or value == "PENDING":
        raise ValueError(f"{question.get('id')}: canonical objective missing")
    return value.strip()


def usable_source_question(question: dict[str, Any]) -> bool:
    choices = question.get("choices")
    correct = question.get("correct")
    return (
        isinstance(choices, list) and len(choices) == 4
        and isinstance(correct, int) and correct in range(4)
        and len({normalized(choice) for choice in choices}) == 4
        and bool(safe_text(question.get("question")))
        and bool(question.get("objectiveSource"))
        and bool(question.get("objectiveEvidenceId"))
    )


def discover(grade: int) -> list[SubjectData]:
    grade_dir = ROOT / "turkiye" / f"{grade}-sinif"
    result: list[SubjectData] = []
    for path in sorted(grade_dir.glob("*/*-tum.jsonl")):
        if path.parent.name == "soru-bankasi":
            continue
        rows = read_jsonl(path)
        packs = [row for row in rows if row.get("type") == "pack"]
        notes = [row for row in rows if row.get("type") == "note"]
        raw_questions = [row for row in rows if row.get("type", "question") == "question"]
        if len(packs) != 1 or not notes or not raw_questions:
            raise ValueError(f"invalid subject topology: {path}")
        note_objectives: dict[str, list[str]] = {
            str(note.get("id")): [
                str(value) for value in (note.get("objectives") or [note.get("objective")])
                if value
            ]
            for note in notes
            if note.get("id")
        }
        questions: list[dict[str, Any]] = []
        for source in raw_questions:
            question = dict(source)
            linked = note_objectives.get(str(question.get("noteId") or ""), [])
            # Some legacy TYMM packs display the full outcome sentence in the
            # question while the linked note carries its canonical code.  The
            # bank pipeline groups source evidence by the canonical curriculum
            # identifier; a one-outcome note is an unambiguous alias bridge.
            if len(linked) == 1:
                question["objective"] = linked[0]
                question["objectiveId"] = linked[0]
            questions.append(question)
        by_objective: dict[str, list[dict[str, Any]]] = defaultdict(list)
        seen_semantic_inputs: set[str] = set()
        accepted_semantics: dict[str, list[tuple[str, set[tuple[str, ...]]]]] = defaultdict(list)
        for question in questions:
            if not usable_source_question(question):
                continue
            signature = combined(question)
            if signature in seen_semantic_inputs:
                continue
            objective = objective_of(question)
            signature_shingles = token_shingles(signature)
            if any(
                (signature_shingles | old_shingles)
                and len(signature_shingles & old_shingles) / len(signature_shingles | old_shingles) >= 0.62
                and SequenceMatcher(None, signature, old, autojunk=False).ratio() > 0.88
                for old, old_shingles in accepted_semantics[objective]
            ):
                continue
            seen_semantic_inputs.add(signature)
            accepted_semantics[objective].append((signature, signature_shingles))
            by_objective[objective].append(question)
        # Canonical objective coverage comes from the note/curriculum records,
        # never from the availability of lesson questions.  Source questions
        # are copy-detection evidence only; an objective with zero usable
        # source questions must still receive its bank minimum.
        for note in notes:
            for objective in note.get("objectives") or [note.get("objective")]:
                if objective:
                    by_objective.setdefault(str(objective), [])
        if not by_objective:
            raise ValueError(f"no usable semantic inputs: {path}")
        result.append(SubjectData(path, packs[0], notes, questions, dict(by_objective)))
    if not result:
        raise ValueError(f"grade {grade}: no subject packs")
    return result


def largest_remainder(
    total: int,
    weights: dict[str, int],
    minimums: dict[str, int],
    maximums: dict[str, int],
) -> dict[str, int]:
    allocation = dict(minimums)
    if sum(allocation.values()) > total:
        raise ValueError("minimum quotas exceed total")
    while sum(allocation.values()) < total:
        remaining = total - sum(allocation.values())
        eligible = [key for key in weights if allocation[key] < maximums[key]]
        if not eligible:
            raise ValueError("quota caps prevent allocation")
        weight_sum = sum(max(1, weights[key]) for key in eligible)
        exact = {key: remaining * max(1, weights[key]) / weight_sum for key in eligible}
        grants = {
            key: min(maximums[key] - allocation[key], int(math.floor(exact[key])))
            for key in eligible
        }
        if not any(grants.values()):
            key = max(
                eligible,
                key=lambda item: (exact[item] - math.floor(exact[item]), weights[item], item),
            )
            grants[key] = 1
        for key, grant in grants.items():
            allocation[key] += min(grant, total - sum(allocation.values()))
            if sum(allocation.values()) == total:
                break
    return allocation


def subject_quotas(subjects: list[SubjectData]) -> dict[str, int]:
    weights = {item.subject: len(item.by_objective) for item in subjects}
    minimums = {
        item.subject: max(SUBJECT_MIN, 2 * len(item.by_objective)) for item in subjects
    }
    if any(value > SUBJECT_MAX for value in minimums.values()):
        raise ValueError(f"objective minimum exceeds subject cap: {minimums}")
    maximums = {item.subject: SUBJECT_MAX for item in subjects}
    return largest_remainder(TARGET, weights, minimums, maximums)


def objective_quotas(subject: SubjectData, total: int) -> dict[str, int]:
    weights = {key: max(1, len(value)) for key, value in subject.by_objective.items()}
    minimums = {key: 2 for key in weights}
    maximums = {key: total for key in weights}
    return largest_remainder(total, weights, minimums, maximums)


def exact_schedule(count: int, ratios: Iterable[float], values: Iterable[Any], seed: str) -> list[Any]:
    ratio_list, value_list = list(ratios), list(values)
    raw = [count * ratio for ratio in ratio_list]
    amounts = [int(math.floor(value)) for value in raw]
    for index in sorted(range(len(raw)), key=lambda i: raw[i] - amounts[i], reverse=True)[:count - sum(amounts)]:
        amounts[index] += 1
    schedule = [value for value, amount in zip(value_list, amounts) for _ in range(amount)]
    decorated = [
        (hashlib.sha256(f"{seed}\0{index}\0{value}".encode("utf-8")).hexdigest(), value)
        for index, value in enumerate(schedule)
    ]
    return [value for _, value in sorted(decorated)]


def difficulty_schedule(grade: int) -> list[int]:
    group = "5-7" if grade <= 7 else "8-10" if grade <= 10 else "11-12"
    ratios = DIFFICULTY_RATIOS[group]
    values = [level for level, ratio in enumerate(ratios, 1) for _ in range(round(TARGET * ratio))]
    if len(values) != TARGET:
        raise AssertionError("difficulty ratios must be exact at 2,000")
    decorated = [
        (hashlib.sha256(f"g{grade}-difficulty-{index}-{value}".encode()).hexdigest(), value)
        for index, value in enumerate(values)
    ]
    return [value for _, value in sorted(decorated)]


def mix_schedule(grade: int) -> list[str]:
    values = [mode for mode, ratio in MIX_RATIOS.items() for _ in range(round(TARGET * ratio))]
    if len(values) != TARGET:
        raise AssertionError("mix ratios must be exact at 2,000")
    decorated = [(hashlib.sha256(f"g{grade}-mix-{i}-{value}".encode()).hexdigest(), value) for i, value in enumerate(values)]
    return [value for _, value in sorted(decorated)]


def normalized(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value or ""))
    text = re.sub(r"\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]{2,}\b", "<ad>", text)
    text = re.sub(r"\d+(?:[.,]\d+)?", "<sayi>", text.casefold())
    text = re.sub(r"[^\w<>]+", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def literal_normalized(value: Any) -> str:
    """Normalize literal option content without similarity-only name/number masking."""
    text = unicodedata.normalize("NFKC", str(value or "")).casefold()
    text = re.sub(r"[^\w]+", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def combined(question: dict[str, Any]) -> str:
    return normalized(" ".join([str(question.get("question", "")), *map(str, question.get("choices", []))]))


def token_shingles(text: str, size: int = 3) -> set[tuple[str, ...]]:
    tokens = text.split()
    return {tuple(tokens[index:index + size]) for index in range(max(1, len(tokens) - size + 1))}


def rotate_semantic(correct_text: str, wrongs: list[str], target: int) -> list[str]:
    ordered = list(wrongs)
    ordered.insert(target, correct_text)
    return ordered


def safe_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def labels_used_by_figures(rows: Iterable[dict[str, Any]], labels: dict[str, Any]) -> set[str]:
    """Collect label keys actually referenced by structured figures."""
    used: set[str] = set()

    def visit(value: Any, field: str = "") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if (key == "key" or key.endswith("Key")) and isinstance(child, str) and child in labels:
                    used.add(child)
                elif key.endswith("Keys") and isinstance(child, list):
                    used.update(item for item in child if isinstance(item, str) and item in labels)
                elif key in {"labels", "sideLabels", "axisKeys", "labelKeys"} and isinstance(child, dict):
                    used.update(item for item in child.values() if isinstance(item, str) and item in labels)
                else:
                    visit(child, key)
        elif isinstance(value, list):
            for child in value:
                visit(child, field)

    for row in rows:
        figure = row.get("figure")
        if isinstance(figure, dict):
            visit(figure)
    return used


def make_table_figure(
    question_id: str,
    context: str,
    statements: list[str],
    labels: dict[str, Any],
) -> dict[str, Any]:
    prefix = question_id.replace("-", ".")
    alt = f"{prefix}.figure.alt"
    head_a, head_b = f"{prefix}.figure.h1", f"{prefix}.figure.h2"
    labels[alt] = "Bir problem durumu ile A, B, C ve D değerlendirme kartlarını içeren tablo; doğru cevap işareti bulunmaz."
    labels[head_a] = "Kart"
    labels[head_b] = "Değerlendirme"
    context_key = f"{prefix}.figure.context"
    context_value_key = f"{prefix}.figure.context.value"
    labels[context_key] = "Problem"
    labels[context_value_key] = context
    rows = [[{"key": context_key}, {"key": context_value_key}]]
    for index, statement in enumerate(statements):
        row_key = f"{prefix}.figure.row{index + 1}"
        statement_key = f"{prefix}.figure.statement{index + 1}"
        labels[row_key] = "ABCD"[index]
        labels[statement_key] = statement
        rows.append([{"key": row_key}, {"key": statement_key}])
    return {
        "kind": "table",
        "headerKeys": [head_a, head_b],
        "rows": rows,
        "altTextKey": alt,
    }


def build_question(
    *, source: dict[str, Any], note: dict[str, Any], grade: int, number: int,
    mode: str, level: int, correct_position: int, labels: dict[str, Any], variant: int,
) -> dict[str, Any]:
    source_choices = [safe_text(value) for value in source.get("choices", [])]
    source_correct = source.get("correct")
    if len(source_choices) != 4 or not isinstance(source_correct, int) or source_correct not in range(4):
        raise ValueError(f"{source.get('id')}: invalid source answer")
    if len({normalized(choice) for choice in source_choices}) != 4:
        raise ValueError(f"{source.get('id')}: repeated source choice")
    correct = source_choices[source_correct]
    wrongs = [choice for index, choice in enumerate(source_choices) if index != source_correct]
    topic = safe_text(source.get("topic") or note.get("topic") or note.get("title"))
    original = safe_text(source.get("question"))
    opener = STEM_OPENERS[(number + grade) % len(STEM_OPENERS)]
    lens = REASONING_LENSES[int(hashlib.sha256(
        f"{source.get('id')}\0{number}".encode("utf-8")
    ).hexdigest(), 16) % len(REASONING_LENSES)]
    opener = f"{opener}; çözümde özellikle {lens} denetleniyor"
    question_id = f"tr-g{grade:02d}-bank-q{number:04d}"
    statements = rotate_semantic(correct, wrongs, correct_position)
    figure = make_table_figure(question_id, original, statements, labels)
    mistaken = wrongs[number % 3]
    focus = " ".join(original.split()[:14]).rstrip(".,;:!?")
    contrast = f"{focus}; {wrongs[0]} / {wrongs[1]} karşılaştırması"
    choice_patterns = (
        "{letter} kartını {lens} ölçütüyle, {contrast} bağlamında savunmak",
        "{contrast} için {lens} denetiminden sonra {letter} kartını sonuç kaydına geçirmek",
        "{contrast} bağlamında problem koşullarını koruyan seçenek olarak {letter} kartını işaretlemek",
        "{contrast} incelendikten sonra gerekçeli karar basamağında {letter} kartını geçerli saymak",
    )
    choice_texts = [choice_patterns[variant % len(choice_patterns)].format(letter=letter, lens=lens, contrast=contrast) for letter in "ABCD"]
    semantic_correct = choice_texts[correct_position]
    semantic_wrongs = [value for index, value in enumerate(choice_texts) if index != correct_position]
    visual_need = {
        "level": "required", "role": "evidence",
        "rationale": "Problem ve değerlendirilecek yargılar yalnız tabloda verildiği için tablo çözümün zorunlu kanıtıdır.",
        "acceptableKinds": ["table"],
        "evidenceDimensions": ["problem", "kart", "değerlendirme"],
    }
    if mode == "comprehension":
        stem = (
            f"{opener}. Aşağıdaki tabloda verilen problem ve dört karttan hangisi, "
            f"“{topic}” konu anlatımındaki temel bilgiyi doğru yansıtır?"
        )
    elif mode == "application":
        stem = (
            f"{opener}. Aşağıdaki tablodaki problem, “{topic}” bilgisi yeni duruma "
            "uygulanarak çözülecektir. Hangi çözüm kartı seçilmelidir?"
        )
    elif mode == "error-analysis":
        stem = (
            f"{opener}. Öğrenci tablodaki “{mistaken}” yargısını seçiyor. “{topic}” "
            "kazanımına göre hangi kart bu yanılgının yerine kullanılmalıdır?"
        )
    else:
        stem = (
            f"{opener}. Aşağıdaki tablodaki problem ve değerlendirme kartları birlikte "
            f"çözümlendiğinde, “{topic}” açısından hangi kart desteklenir?"
        )
    stem += f" İncelemede “{focus}” ipucu ile “{mistaken}” önerisi birlikte denetlenmelidir."
    if variant:
        variant_guidance = (
            "Önce problemdeki koşullar ayrıştırılmalı, ardından her kart aynı ölçütle sınanmalıdır.",
            "Karar, yalnız konu başlığına değil tabloda verilen özel duruma dayandırılmalıdır.",
            "Sonuç yazılmadan önce yanlış seçeneklerin hangi koşulla çeliştiği ayrı ayrı kontrol edilmelidir.",
        )
        stem += " " + variant_guidance[(variant - 1) % len(variant_guidance)]
    choices = rotate_semantic(semantic_correct, semantic_wrongs, correct_position)
    misconceptions = (
        "Kavramı tersine çevirme", "Bağlam koşulunu atlama", "Kanıtı yanlış genelleme"
    )
    distractor_why = []
    wrong_index = 0
    for index, choice in enumerate(choices):
        if index == correct_position:
            distractor_why.append(
                f"Doğru; bu seçenek {topic} kazanımındaki doğru sonucu ve verilen bağlamı birlikte korur."
            )
        else:
            distractor_why.append(
                f"{misconceptions[wrong_index % len(misconceptions)]}: “{choice}” seçeneği, "
                f"{topic} için verilen koşullardan en az birini yanlış yorumlar."
            )
            wrong_index += 1
    explanation = safe_text(source.get("explanation"))
    if not explanation:
        explanation = f"Doğru sonuç “{correct}” ifadesidir."
    result = {
        "type": "question",
        "id": question_id,
        "questionNumber": number,
        "subject": source.get("subject") or note.get("subject"),
        "grade": grade,
        "unitKey": source.get("unitKey") or note.get("unitKey"),
        "topicKey": source.get("topicKey") or note.get("topicKey"),
        "subtopicKey": source.get("subtopicKey") or note.get("subtopicKey"),
        "topic": topic,
        "noteId": note.get("noteId") or note.get("id"),
        "noteKey": note.get("noteKey") or note.get("id"),
        "objective": objective_of(source),
        "question": stem,
        "choices": choices,
        "correct": correct_position,
        "correctIndex": correct_position,
        "correctOption": choices[correct_position],
        "distractorWhy": distractor_why,
        "explanation": (
            f"{explanation} Bu nedenle doğru değerlendirme {choices[correct_position]!r} olur; "
            "diğer seçenekler belirtilen öğrenci yanılgılarını temsil eder."
        ),
        "level": level,
        "difficultyReason": (
            f"Düzey {level}; {topic} bilgisini yeni bağlama aktarmayı, dört özgül seçeneği "
            f"karşılaştırmayı ve {mode} türünde gerekçeli karar vermeyi gerektirir."
        ),
        "questionType": mode,
        "familyId": f"tr-g{grade:02d}-bank-family-{number:04d}",
        "objectiveSource": source.get("objectiveSource") or note.get("objectiveSource"),
        "objectiveEvidenceId": source.get("objectiveEvidenceId") or note.get("objectiveEvidenceId"),
        "sourceRefs": copy.deepcopy(source.get("sourceRefs") or note.get("sourceRefs") or []),
        "visualNeed": visual_need,
        "figure": figure,
        "hintsCount": 0,
        "hintsForbidden": True,
        "linkedNoteId": note.get("noteId") or note.get("id"),
        "linkedNoteKey": note.get("noteKey") or note.get("id"),
        "sourceQuestionSemanticRef": f"sha256:{sha256({'id': source.get('id'), 'objective': objective_of(source)})}",
    }
    return pending(result)


def select_note(subject: SubjectData, question: dict[str, Any]) -> dict[str, Any]:
    note_id = question.get("noteId") or question.get("linkedNoteId")
    for note in subject.notes:
        if note_id in {note.get("id"), note.get("noteId"), note.get("noteKey")}:
            return note
    objective = objective_of(question)
    for note in subject.notes:
        objectives = note.get("objectives") or [note.get("objective")]
        if objective in objectives:
            return note
    raise ValueError(f"{question.get('id')}: linked note missing")


def validate_candidate(
    rows: list[dict[str, Any]], source_questions: list[dict[str, Any]], grade: int
) -> dict[str, Any]:
    notes = [row for row in rows if row.get("type") == "note"]
    questions = [row for row in rows if row.get("type") == "question"]
    if len(questions) != TARGET:
        raise ValueError(f"question count {len(questions)} != {TARGET}")
    if Counter(question["correct"] for question in questions) != Counter({0: 500, 1: 500, 2: 500, 3: 500}):
        raise ValueError("answer positions are not 500/500/500/500")
    if Counter(question.get("level") for question in questions) != Counter(difficulty_schedule(grade)):
        raise ValueError("difficulty distribution does not match the grade policy")
    if Counter(question.get("questionType") for question in questions) != Counter(mix_schedule(grade)):
        raise ValueError("question-type distribution does not match the 25/35/25/15 policy")
    note_ids = {str(note.get("id")) for note in notes}
    source_ids = {str(question.get("id")) for question in source_questions}
    seen_ids, seen_texts, seen_full = set(), set(), set()
    source_texts = {normalized(q.get("question")) for q in source_questions}
    source_full_by_objective: dict[str, list[tuple[str, str, set[tuple[str, ...]]]]] = defaultdict(list)
    for question in source_questions:
        full = combined(question)
        source_full_by_objective[objective_of(question)].append((str(question.get("id")), full, token_shingles(full)))
    generated_by_objective: dict[str, list[tuple[str, str, set[tuple[str, ...]]]]] = defaultdict(list)
    near = []
    for question in questions:
        qid = str(question.get("id"))
        text, full = normalized(question.get("question")), combined(question)
        if qid in seen_ids or qid in source_ids:
            raise ValueError(f"duplicate/source id: {qid}")
        if text in seen_texts or text in source_texts:
            raise ValueError(f"duplicate/source text: {qid}")
        if full in seen_full:
            raise ValueError(f"duplicate question+choices: {qid}")
        seen_ids.add(qid); seen_texts.add(text); seen_full.add(full)
        choices = question.get("choices") or []
        correct = question.get("correct")
        if len(choices) != 4 or len({literal_normalized(choice) for choice in choices}) != 4:
            raise ValueError(f"{qid}: choices are not four unique values")
        if correct not in range(4) or question.get("correctOption") != choices[correct]:
            raise ValueError(f"{qid}: atomic answer mismatch")
        if len(question.get("distractorWhy") or []) != 4:
            raise ValueError(f"{qid}: distractorWhy mismatch")
        if str(question.get("noteId")) not in note_ids or question.get("noteKey") != question.get("noteId"):
            raise ValueError(f"{qid}: note link mismatch")
        if not question.get("objectiveSource") or not question.get("objectiveEvidenceId"):
            raise ValueError(f"{qid}: MEB evidence anchor missing")
        visual = question.get("visualNeed") or {}
        if visual.get("level") == "required" and not question.get("figure"):
            raise ValueError(f"{qid}: required figure missing")
        objective = objective_of(question)
        q_shingles = token_shingles(full)
        comparisons = source_full_by_objective[objective] + generated_by_objective[objective]
        for candidate_id, candidate, candidate_shingles in comparisons:
            union = q_shingles | candidate_shingles
            if union and len(q_shingles & candidate_shingles) / len(union) < 0.62:
                continue
            ratio = SequenceMatcher(None, full, candidate, autojunk=False).ratio()
            if ratio > 0.88:
                near.append((qid, candidate_id, round(ratio, 4)))
                break
        generated_by_objective[objective].append((qid, full, q_shingles))
    if near:
        raise ValueError(f"near-copy threshold exceeded: {near[:10]}")
    objective_counts = Counter(objective_of(question) for question in questions)
    if min(objective_counts.values()) < 2:
        raise ValueError("canonical objective minimum is below two")
    return {
        "grade": grade,
        "questions": len(questions),
        "notes": len(notes),
        "answerBalance": [500, 500, 500, 500],
        "difficulty": dict(sorted(Counter(q["level"] for q in questions).items())),
        "mix": dict(sorted(Counter(q["questionType"] for q in questions).items())),
        "visualQuestions": sum(bool(q.get("figure")) for q in questions),
        "objectives": len(objective_counts),
        "exactSourceIdOverlap": 0,
        "exactSourceTextOverlap": 0,
        "nearCopyAbove088": 0,
    }


def build_grade(grade: int, *, allow_blocked: bool = False) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if grade in CURRENT_CURRICULUM_BLOCKS and not allow_blocked:
        raise RuntimeError(CURRENT_CURRICULUM_BLOCKS[grade])
    subjects = discover(grade)
    quotas = subject_quotas(subjects)
    blueprints = load_authored_blueprints(grade)
    blueprint_counts = Counter(str(row.get("subject") or "") for row in blueprints)
    readiness_blockers = []
    for subject in subjects:
        authored = blueprint_counts.get(subject.subject, 0)
        if authored != quotas[subject.subject]:
            readiness_blockers.append(
                f"{subject.subject}: {authored}/{quotas[subject.subject]} bağımsız yazılmış tam soru hazır"
            )
        deficient_notes = 0
        for note in subject.notes:
            sections = note.get("lessonSections")
            examples = sections.get("workedExamples") if isinstance(sections, dict) else None
            if not isinstance(examples, list) or len(examples) < 2 or any(len(str(value)) < 120 for value in examples[:2]):
                deficient_notes += 1
        if deficient_notes:
            readiness_blockers.append(
                f"{subject.subject}: {deficient_notes} notta iki kazanıma özgü çözümlü örnek eksik"
            )
    unexpected_subjects = sorted(set(blueprint_counts) - {subject.subject for subject in subjects})
    if unexpected_subjects:
        readiness_blockers.append(f"tanımsız ders adları: {', '.join(unexpected_subjects)}")
    if len(blueprints) != TARGET:
        readiness_blockers.append(f"toplam bağımsız yazılmış soru: {len(blueprints)}/{TARGET}")
    if readiness_blockers:
        raise RuntimeError("kaynak hazırlık kapısı: " + "; ".join(readiness_blockers))
    old_path = ROOT / "turkiye" / f"{grade}-sinif" / "soru-bankasi" / f"{grade}-sinif-tum-dersler-2000-soru.jsonl"
    old_pack = read_jsonl(old_path)[0] if old_path.exists() else {}
    labels: dict[str, Any] = load_authored_labels(grade)
    sources: dict[str, dict[str, Any]] = {}
    source_packages = []
    notes_by_id: dict[str, dict[str, Any]] = {}
    subjects_by_name = {subject.subject: subject for subject in subjects}
    for subject in subjects:
        labels.update(copy.deepcopy(subject.pack.get("labels") or {}))
        for source in subject.pack.get("sources") or []:
            key = source.get("sourceId") or sha256(source)
            sources[str(key)] = copy.deepcopy(source)
        source_packages.append({
            "id": subject.pack.get("id"),
            "path": subject.path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(subject.path),
            "hashScope": "raw-file-sha256",
            "questionsUsedAsSemanticInputs": 0,
            "usedFor": "curriculum-grounding-note-linking-and-copy-detection-only",
        })
    questions = []
    ordered_blueprints = sorted(
        blueprints,
        key=lambda row: (int(row.get("questionNumber") or TARGET + 1), str(row.get("id"))),
    )
    for index, authored in enumerate(ordered_blueprints, 1):
        subject = subjects_by_name[str(authored.get("subject"))]
        note = select_note(subject, authored)
        note_id = str(note.get("id"))
        notes_by_id.setdefault(note_id, pending(note))
        question = copy.deepcopy(authored)
        if not str(question.get("id") or "").startswith(f"tr-g{grade:02d}-bank-"):
            raise ValueError(f"{question.get('id')}: bank-scoped id prefix is required")
        question["questionNumber"] = index
        question["grade"] = grade
        question["noteId"] = note_id
        question["noteKey"] = note_id
        question["linkedNoteId"] = note_id
        question["linkedNoteKey"] = note_id
        questions.append(pending(question))
    audio_policy: dict[str, Any] | None = None
    if any(str(question.get("mediaRequirement") or "").startswith("audio") for question in questions):
        audio_root = ROOT / "build" / "audio-authoring" / f"grade-{grade}"
        audio_manifest_path = audio_root / "audio-assets.json"
        if not audio_manifest_path.is_file():
            raise RuntimeError(f"grade {grade}: audio-assets.json missing")
        audio_manifest = json.loads(audio_manifest_path.read_text(encoding="utf-8"))
        assets = audio_manifest.get("assets") if isinstance(audio_manifest.get("assets"), list) else []
        by_id = {str(asset.get("assetId") or ""): asset for asset in assets}
        audio_questions = 0
        for question in questions:
            requirement = str(question.get("mediaRequirement") or "")
            if not requirement.startswith("audio"):
                continue
            audio_questions += 1
            audio = question.get("audio") if isinstance(question.get("audio"), dict) else {}
            asset_id = str(audio.get("assetId") or "")
            asset = by_id.get(asset_id)
            if asset is None:
                raise RuntimeError(f"{question.get('id')}: unresolved audio asset {asset_id}")
            audio["contentSha256"] = str(asset.get("sha256") or "")
            question["audio"] = audio
        if audio_questions != len(by_id) or int(audio_manifest.get("assetCount") or -1) != len(by_id):
            raise RuntimeError(
                f"grade {grade}: audio coverage mismatch questions={audio_questions} assets={len(by_id)}"
            )
        audio_policy = {
            "schemaVersion": "alika-local-audio-policy/1.0.0",
            "manifestPath": "audio-assets.json",
            "manifestSha256": file_sha256(audio_manifest_path),
            "assetCount": len(by_id),
            "questionCount": audio_questions,
            "storage": "local-offline-wav",
            "remoteAssetsAllowed": False,
            "recordingStorage": "local-temporary-only",
        }
    coverage_notes: dict[str, set[str]] = defaultdict(set)
    coverage_counts: Counter[str] = Counter()
    for question in questions:
        objective = objective_of(question)
        coverage_counts[objective] += 1
        coverage_notes[objective].add(str(question["noteId"]))
    coverage = {
        objective: {
            "notes": sorted(coverage_notes[objective]),
            "questions": coverage_counts[objective],
        }
        for objective in sorted(coverage_counts)
    }
    supporting_rows = [*notes_by_id.values(), *questions]
    used_label_keys = labels_used_by_figures(supporting_rows, labels)
    labels = {key: labels[key] for key in sorted(used_label_keys)}
    pack = pending({
        "type": "pack",
        "schemaVersion": "2.2",
        "id": old_pack.get("id") or f"tr.g{grade:02d}.tum-dersler.soru-bankasi",
        "version": (int(old_pack.get("version", 1)) + 1) if str(old_pack.get("version", 1)).isdigit() else "2.0.0",
        "lang": "tr", "country": "TR",
        "curriculum": combined_curriculum(subjects),
        "subject": "Tüm Dersler", "grade": grade,
        "theme": f"Türkiye {grade}. Sınıf — 2.000 Özgün Soruluk Tüm Dersler Soru Bankası",
        "license": "CC-BY-NC-4.0",
        "source": "independently-authored-blueprints-grounded-in-canonical-subject-packs",
        "sources": list(sources.values()),
        "sourcePackages": source_packages,
        "labels": labels,
        "visualPolicy": {
            "version": "1.3.0", "everyNote": False,
            "questionMinimumPercent": 0, "balancedByObjective": False,
            "rationale": "Görsel yalnız çözüm kanıtı gerektirdiğinde zorunludur; dekoratif kota uygulanmaz.",
        },
        "objectives": sorted(coverage),
        "counts": {"notes": len(notes_by_id), "questions": TARGET},
        "coverage": coverage,
        "levelScale": [1, 5],
        "contentContractVersion": "2.2", "contentContractHash": CONTRACT_HASH,
        "figureSpecVersion": "1.3.0",
        "contractPolicy": {
            "questionCount": TARGET, "minFamilies": TARGET, "maxPerFamily": 1,
            "idScopeMode": "multi-subject",
            "answerBalance": [500, 500, 500, 500],
            "minFiguredQuestions": 0, "everyNoteHasFigure": False,
            "objectiveBalanceMode": "coverage",
        },
        "generationPolicy": {
            "version": METHOD, "batchSize": BATCH,
            "sourceQuestionReuse": "forbidden",
            "authoringInput": f"authoring/question-bank-blueprints/grade-{grade}.jsonl",
            "subjectMinimum": SUBJECT_MIN, "subjectMaximum": SUBJECT_MAX,
            "canonicalObjectiveMinimum": 2,
            "subjectQuotas": quotas,
            "mix": MIX_RATIOS,
        },
        **({"audioPolicy": audio_policy} if audio_policy is not None else {}),
    })
    rows = [pack, *notes_by_id.values(), *questions]
    metrics = validate_candidate(rows, [q for s in subjects for q in s.questions], grade)
    metrics["subjectQuotas"] = quotas
    metrics["audioQuestions"] = sum(
        str(question.get("mediaRequirement") or "").startswith("audio")
        for question in questions
    )
    metrics["contentProjectionSha256"] = hashlib.sha256(
        b"\n".join(canonical_bytes(row) for row in rows) + b"\n"
    ).hexdigest()
    return rows, metrics


def write_batches(grade: int, rows: list[dict[str, Any]], metrics: dict[str, Any]) -> Path:
    target_dir = ROOT / "build" / "question-banks" / f"grade-{grade}" / "pending"
    target_dir.mkdir(parents=True, exist_ok=True)
    if rows[0].get("audioPolicy"):
        source_root = ROOT / "build" / "audio-authoring" / f"grade-{grade}"
        shutil.copy2(source_root / "audio-assets.json", target_dir / "audio-assets.json")
        source_assets = source_root / "assets" / "audio"
        target_assets = target_dir / "assets" / "audio"
        target_assets.mkdir(parents=True, exist_ok=True)
        for source in sorted(source_assets.glob("*.wav")):
            shutil.copy2(source, target_assets / source.name)
    pack = rows[0]
    notes = [row for row in rows if row.get("type") == "note"]
    questions = [row for row in rows if row.get("type") == "question"]
    for batch_index in range(0, TARGET, BATCH):
        batch_rows = [pack, *notes, *questions[batch_index:batch_index + BATCH]]
        path = target_dir / f"batch-{batch_index // BATCH + 1:02d}.jsonl"
        path.write_text(
            "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in batch_rows) + "\n",
            encoding="utf-8", newline="\n",
        )
    candidate = target_dir / f"{grade}-sinif-tum-dersler-2000-soru.pending.jsonl"
    candidate.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n",
        encoding="utf-8", newline="\n",
    )
    # External review binds to the immutable bytes on disk, not to the
    # separately useful canonical content projection.  Reporting the latter
    # as candidateSha256 made a correct external manifest look stale.
    metrics["candidateSha256"] = hashlib.sha256(candidate.read_bytes()).hexdigest()
    (target_dir / "candidate-metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    return candidate


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--grade", type=int, choices=range(5, 13), action="append")
    parser.add_argument("--allow-blocked-curriculum", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    grades = args.grade or list(range(5, 13))
    for grade in grades:
        try:
            rows, metrics = build_grade(grade, allow_blocked=args.allow_blocked_curriculum)
        except RuntimeError as exc:
            print(json.dumps({"grade": grade, "status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False))
            return 2
        path = write_batches(grade, rows, metrics)
        print(json.dumps({"grade": grade, "status": "PENDING_REVIEW", "candidate": str(path), **metrics}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
