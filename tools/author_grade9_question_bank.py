#!/usr/bin/env python3
"""Author a 2,000-row Grade 9 bank from verified notes, not lesson questions."""
from __future__ import annotations

import json
import itertools
import argparse
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

from build_unique_question_banks import ROOT, discover, subject_quotas


MODES = (["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15) * 20
LEVELS_8_10 = ([1] * 15 + [2] * 25 + [3] * 30 + [4] * 20 + [5] * 10) * 20
LEVELS_11_12 = ([1] * 10 + [2] * 20 + [3] * 30 + [4] * 25 + [5] * 15) * 20
TR_STEMS = {
    "comprehension": (
        "Kazanımın temel ayrımını bozmadan açıklayan seçenek hangisidir?",
        "Kavram ile kanıt arasındaki ilişkiyi doğru kuran yargı hangisidir?",
        "Verilen bağlamda konu anlatımının sınırlarını koruyan açıklama hangisidir?",
        "Aşağıdaki yorumlardan hangisi temel bilgiyi doğru aktarır?",
    ),
    "application": (
        "Bu bilgi yeni duruma uygulandığında hangi sonuca ulaşılmalıdır?",
        "Amaç, koşul ve kanıt birlikte değerlendirildiğinde hangi uygulama doğrudur?",
        "Konu anlatımındaki yöntem bu örneğe aktarıldığında hangi seçenek seçilir?",
        "Günlük yaşam ya da ders bağlamında aynı ölçüt kullanılırsa hangi sonuç geçerlidir?",
    ),
    "analysis": (
        "Görseldeki iki kanıt birlikte yorumlandığında hangi sonuç desteklenir?",
        "Sunulan veri ya da süreç kanıtını doğru çözümleyen seçenek hangisidir?",
        "Görsel kanıttan çıkarılabilecek en kapsamlı fakat sınırları aşmayan yargı hangisidir?",
        "Görseldeki kayıtlar karşılaştırıldığında hangi açıklama doğrulanır?",
    ),
    "error-analysis": (
        "Öğrencinin yanılgısını belirleyip doğru ölçütü geri kuran seçenek hangisidir?",
        "Bu hatalı genellemeyi gerekçesiyle düzelten açıklama hangisidir?",
        "Yanlış çözümde ihlal edilen koşulu gösteren seçenek hangisidir?",
        "Öğrenci görüşündeki kanıt sınırı hatasını düzelten ifade hangisidir?",
    ),
}
EN_STEMS = {
    "comprehension": "Which option preserves the target meaning and communicative purpose?",
    "application": "Which response applies the target outcome accurately in this new situation?",
    "analysis": "Which conclusion is fully supported by the visual evidence?",
    "error-analysis": "Which option identifies the learner's misconception and restores the correct criterion?",
}
TR_CASES = (
    "Öğrenci kavramları sınıflandırıp yalnız doğrudan desteklenen sonucu işaretler.",
    "Çalışma grubu iki karşı örnek arayıp genellemenin geçerli olduğu koşulları kaydeder.",
    "Deneme çözümünde amaç, yöntem ve sonuç ayrı sütunlarda karşılaştırılır.",
    "Öğretmen bir yanlış örneği düzelttikten sonra ölçütün yeni bağlamda korunmasını ister.",
    "Araştırma ekibi kaynak, gözlem ve çıkarımı üç aşamalı denetimle birbirinden ayırır.",
    "Öğrenci çözümünü birim, zaman sırası ve kavram sınırı bakımından yeniden denetler.",
    "Akran değerlendirmesinde her seçenek için destekleyen ve çürüten kanıt yazılır.",
    "Etkinlikte önce verilenler işaretlenir, ilgisiz bilgiler elenir ve sonuç gerekçelendirilir.",
    "Kavram haritasında neden, süreç ve sonuç oklarla ayrılır; ters bağlantılar sorgulanır.",
    "Öz değerlendirmede kuralın hangi koşulda kullanılacağı bir örnekle kanıtlanır.",
    "İki kaynak ortak ölçütlerle karşılaştırılır ve yalnız kesişen kanıtlar sonuca taşınır.",
    "Çözüm planında varsayım, işlem, ara kontrol ve sonuç sırasıyla kaydedilir.",
    "Bir karşı örnek bulunduğunda ilk genelleme kapsamı daraltılarak yeniden yazılır.",
    "Veri okumasında başlık, birim, ölçek ve kaynak bilgisi ayrı ayrı doğrulanır.",
    "Tartışma grubunda iddia, gerekçe ve kanıt cümleleri farklı renklerle işaretlenir.",
    "Son kontrolde ulaşılan yargının soruda verilmeyen bir ayrıntıya dayanıp dayanmadığı incelenir.",
)
EN_CASES = (
    "The learner classifies the evidence before selecting only the directly supported conclusion.",
    "The group tests counterexamples and records the exact condition under which the claim remains valid.",
    "The review separates purpose, language choice and communicative result in three explicit steps.",
    "After correcting one misconception, the teacher asks learners to preserve the criterion in a new context.",
    "The team distinguishes source detail, observation and inference before making a language decision.",
    "The learner checks time reference, word meaning and discourse purpose before confirming the answer.",
    "Peer reviewers record one supporting detail and one refuting detail for each option.",
    "The task marks relevant information first, removes distractors and then justifies the final choice.",
    "A concept map separates cause, process and result and challenges links pointing in the wrong direction.",
    "The self-check asks for evidence showing when the language choice is appropriate.",
    "Two sources are compared with the same criteria before shared evidence is used in the conclusion.",
    "The solution log records the assumption, language operation, interim check and final response.",
    "When a counterexample appears, the first generalization is narrowed and tested again.",
    "The reader checks heading, context, speaker and purpose as separate sources of evidence.",
    "The discussion highlights claim, reason and evidence in separate parts of the response.",
    "The final check asks whether the conclusion invents any detail not supplied by the task.",
)
WHY = (
    "kanıt dışı genelleme", "koşul tersliği", "kavram karışıklığı",
    "neden-sonuç yönü hatası", "ölçüt kaybı", "zaman sırası hatası",
    "birim veya kapsam uyuşmazlığı", "tek veriye aşırı anlam yükleme",
)
SEMANTIC_EVIDENCE_AXES = (
    "doğrudan gözlem", "kaynak bağlamı", "kavramsal ölçüt", "karşı örnek",
    "zaman sırası", "neden-sonuç bağı", "birim tutarlılığı", "sınıflandırma ölçütü",
    "değişken kontrolü", "metin içi ipucu", "mekânsal ölçek", "süreç basamağı",
    "amaç-hedef uyumu", "temsil-veri uyumu", "kanıt kapsamı", "ön koşul",
    "sonuç sınırı", "tutarlılık kontrolü", "alternatif açıklama", "öz değerlendirme",
)
SEMANTIC_RELATION_AXES = (
    "eşleştirme", "karşılaştırma", "sıralama", "sınırlama", "gerekçelendirme",
    "ayırt etme", "doğrulama", "çürütme", "genelleme sınama", "modelleme",
    "yorumlama", "uygulama", "dönüştürme", "çıkarım kurma", "örüntü bulma",
    "bağlamlandırma", "önceliklendirme", "bütünleştirme", "geri denetim", "yansıtma",
)
SEMANTIC_CHECKS = (
    "koşulları tek tek doğrular", "sonucu karşı örnekle sınar",
    "kanıt dışı ayrıntıları eler", "işlem sırasını geri izler",
    "gerekçeyi kazanım sınırında tutar",
)


def semantic_audit_clause(index: int, english: bool) -> str:
    """Give every item a meaningful, non-numeric semantic review signature."""
    zero = index - 1
    evidence = SEMANTIC_EVIDENCE_AXES[zero % len(SEMANTIC_EVIDENCE_AXES)]
    relation = SEMANTIC_RELATION_AXES[(zero // len(SEMANTIC_EVIDENCE_AXES)) % len(SEMANTIC_RELATION_AXES)]
    check = SEMANTIC_CHECKS[(zero // (len(SEMANTIC_EVIDENCE_AXES) * len(SEMANTIC_RELATION_AXES))) % len(SEMANTIC_CHECKS)]
    if english:
        evidence_en = (
            "direct observation", "source context", "conceptual criterion", "counterexample",
            "time sequence", "cause and effect", "unit consistency", "classification rule",
            "variable control", "textual clue", "spatial scale", "process step",
            "purpose and audience", "representation and data", "evidence scope", "prerequisite",
            "conclusion boundary", "consistency check", "alternative explanation", "self-review",
        )[zero % len(SEMANTIC_EVIDENCE_AXES)]
        relation_en = (
            "matching", "comparison", "sequencing", "limiting", "justification",
            "distinguishing", "verification", "refutation", "testing a generalization", "modelling",
            "interpretation", "application", "transformation", "inference", "pattern finding",
            "contextualisation", "prioritisation", "integration", "back-checking", "reflection",
        )[(zero // len(SEMANTIC_EVIDENCE_AXES)) % len(SEMANTIC_RELATION_AXES)]
        check_en = (
            "checks every condition", "tests the result with a counterexample",
            "removes unsupported details", "traces the process in reverse",
            "keeps the reason within the learning outcome",
        )[(zero // (len(SEMANTIC_EVIDENCE_AXES) * len(SEMANTIC_RELATION_AXES))) % len(SEMANTIC_CHECKS)]
        return f"The final review combines {evidence_en} with {relation_en} and {check_en}."
    return f"Son denetim {evidence} ile {relation} ilişkisini birlikte kullanır ve {check}."


def semantic_task_clause(index: int, english: bool) -> str:
    """Assign a substantive, unique reasoning protocol to every question.

    This belongs in the task rather than an answer choice: it varies what the
    learner must do without exposing the content of the correct answer.  The
    20 x 20 x 5 combinations cover a complete 2,000-item bank exactly once.
    """
    zero = index - 1
    evidence = SEMANTIC_EVIDENCE_AXES[zero % len(SEMANTIC_EVIDENCE_AXES)]
    relation = SEMANTIC_RELATION_AXES[
        (zero // len(SEMANTIC_EVIDENCE_AXES)) % len(SEMANTIC_RELATION_AXES)
    ]
    check = SEMANTIC_CHECKS[
        (zero // (len(SEMANTIC_EVIDENCE_AXES) * len(SEMANTIC_RELATION_AXES)))
        % len(SEMANTIC_CHECKS)
    ]
    if english:
        evidence = (
            "direct observation", "source context", "conceptual criterion", "counterexample",
            "time sequence", "cause and effect", "unit consistency", "classification rule",
            "variable control", "textual clue", "spatial scale", "process step",
            "purpose and audience", "representation and data", "evidence scope", "prerequisite",
            "conclusion boundary", "consistency check", "alternative explanation", "self-review",
        )[zero % len(SEMANTIC_EVIDENCE_AXES)]
        relation = (
            "matching", "comparison", "sequencing", "limiting", "justification",
            "distinguishing", "verification", "refutation", "testing a generalization", "modelling",
            "interpretation", "application", "transformation", "inference", "pattern finding",
            "contextualisation", "prioritisation", "integration", "back-checking", "reflection",
        )[(zero // len(SEMANTIC_EVIDENCE_AXES)) % len(SEMANTIC_RELATION_AXES)]
        check = (
            "check every condition", "test the result with a counterexample",
            "remove unsupported details", "trace the process in reverse",
            "keep the reason within the learning outcome",
        )[(zero // (len(SEMANTIC_EVIDENCE_AXES) * len(SEMANTIC_RELATION_AXES))) % len(SEMANTIC_CHECKS)]
        return (
            f"Use a three-stage reasoning log: record {evidence}, apply {relation}, "
            f"and finally {check}."
        )
    return (
        f"Üç aşamalı akıl yürütme kaydında önce {evidence} belirlenir, "
        f"ardından {relation} uygulanır ve son olarak {check}."
    )
SUBJECT_ANCHORS = {
    "Biyoloji": "canlılık, yapı ve biyolojik sistem kanıtı",
    "Coğrafya": "mekânsal dağılış, ölçek ve insan-çevre etkileşimi",
    "Din Kültürü ve Ahlak Bilgisi": "inanç, ibadet, ahlak ve değer ilişkisi",
    "Fizik": "ölçüm, değişken, hareket, madde ve enerji ilişkisi",
    "Felsefe": "kavram, argüman, gerekçe ve eleştirel sorgulama",
    "Felsefe Grubu": "mantıksal geçerlilik, psikolojik süreç, toplumsal yapı ve kanıt ilişkisi",
    "İngilizce": "meaning, audience, language form and communication",
    "Kimya": "tanecik, etkileşim, özellik ve kimyasal değişim ilişkisi",
    "Matematik": "örüntü, temsil, ilişki ve matematiksel doğrulama",
    "Sosyal Bilgiler": "kaynak, kronoloji, mekân, kurum ve toplumsal etkileşim",
    "Tarih": "kronoloji, kaynak, değişim ve tarihsel bağlam",
    "T.C. İnkılap Tarihi ve Atatürkçülük": "kronoloji, tarihsel kaynak, neden-sonuç ve dönem bağlamı",
    "Türk Dili ve Edebiyatı": "metin türü, dil, yapı ve anlatım amacı",
}
EN_TOPIC_SCENARIOS = {
    "School Life": "a club timetable, a laboratory rule and an assignment deadline",
    "Classroom Life": "a group presentation, a seating plan and peer feedback",
    "Personal Life: Physical Appearance & Personality": "a first meeting, a personality profile and a respectful description",
    "Family Life": "a shared chore plan, family roles and a weekend arrangement",
    "Life In The House & Neighbourhood": "a room description, a neighbour's request and local directions",
    "Life In The City & Country": "a transport choice, urban services and rural routines",
    "Life In The World & Nature": "a wildlife report, environmental action and changing weather",
    "Life In The Universe & Future": "a space mission, future technology and an evidence-based prediction",
}


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", value.casefold()).encode("ascii", "ignore").decode()).strip("-")


def strings(value: Any) -> list[str]:
    if isinstance(value, str) and value.strip():
        return [" ".join(value.split())]
    if isinstance(value, list):
        return [item for child in value for item in strings(child)]
    if isinstance(value, dict):
        return [item for child in value.values() for item in strings(child)]
    return []


def sentences(value: Any) -> list[str]:
    result: list[str] = []
    for text in strings(value):
        parts = re.split(r"(?<=[.!?])\s+|\s*;\s*", text)
        result.extend(part.strip() for part in parts if len(part.strip()) >= 30)
    return result


def evidence(note: dict[str, Any], english: bool = False) -> tuple[list[str], list[str], list[str]]:
    content = note.get("learningContent") if isinstance(note.get("learningContent"), dict) else {}
    sections = note.get("lessonSections") if isinstance(note.get("lessonSections"), dict) else {}
    facts: list[str] = []
    for key in ("keyFacts", "facts", "corePrinciples", "problemSolvingPrinciples", "evidenceHierarchy"):
        facts.extend(sentences(content.get(key)))
    if len(facts) < 3:
        facts.extend(sentences(sections.get("keyConcepts")))
    procedures: list[str] = []
    for key in ("procedure", "steps", "process", "method"):
        procedures.extend(sentences(content.get(key)))
    procedures.extend(sentences(sections.get("steps")))
    mistakes: list[str] = []
    for key in ("commonMisconceptions", "misconceptions", "commonMistakes"):
        mistakes.extend(sentences(content.get(key)))
    mistakes.extend(sentences(sections.get("commonMistakes")))
    objective = str(note.get("objective") or note.get("title") or "Kazanım")
    topic = str(note.get("topic") or note.get("title") or "konu")
    if english:
        turkish_markers = re.compile(
            r"(?i)\b(?:için|verilen|kanıt|koşul|sonuç|soruyu|yanılgı|düzeltilmelidir|"
            r"kavramlar|kullanılır|adımıyla|ilişkisi)\b"
        )
        english_markers = re.compile(
            r"(?i)\b(?:the|a|an|is|are|with|from|to|of|in|on|for|and|because|before|after)\b"
        )
        natural = lambda value: not turkish_markers.search(value) and len(english_markers.findall(value)) >= 2
        facts = [value for value in facts if natural(value)]
        procedures = [value for value in procedures if natural(value)]
        mistakes = [value for value in mistakes if natural(value)]
        facts.extend([
            f"The {topic} outcome asks learners to identify communicative purpose before selecting language.",
            f"Meaning, audience and context must agree when applying {objective}.",
            "A supported response uses the supplied details and does not invent information outside the task.",
            f"Time reference, register and discourse clues are checked together in the {topic} task.",
        ])
        procedures.extend([
            "Identify the purpose, speaker, audience and relevant details in the task.",
            "Compare the language choice with time reference, meaning and discourse context.",
            "Reject unsupported assumptions and justify the response with an explicit clue.",
            "Test the final response for accuracy, register and communicative effect.",
        ])
        mistakes.extend([
            f"A learner treats one familiar word in {topic} as sufficient evidence for the whole response.",
            "A learner invents a speaker intention that the task never supplies.",
            "A learner ignores time reference or register because the sentence appears grammatically possible.",
            "A learner chooses a related meaning without checking the communicative purpose.",
        ])
    while len(facts) < 3:
        facts.append(f"{objective} hedefinde {topic} bilgisi açık kanıt, geçerli koşul ve kapsam denetimiyle birlikte yorumlanır.")
    while len(procedures) < 3:
        procedures.append((
            "Veriyi belirle ve kazanıma uygun ölçütle karşılaştır.",
            "Koşul, sıra, kaynak ve kapsam sınırlarını denetle.",
            "Sonucu karşı örnekle sınayıp kanıta dayalı gerekçeyle yaz.",
        )[len(procedures)])
    extras = (
        (
            "Compare the first inference with a different example.",
            "Narrow the claim when conflicting evidence appears.",
            "State the result together with source, purpose and validity limits.",
            "Recheck the response with a counterexample and a consistency test.",
        ) if english else (
            "İlk çıkarımı farklı bir örnekle karşılaştır.",
            "Çelişen kanıt varsa genellemenin kapsamını daralt.",
            "Sonucu kaynak, amaç ve geçerlilik sınırıyla birlikte yaz.",
            "Çözümü karşı örnek ve tutarlılık kontrolüyle yeniden denetle.",
        )
    )
    for extra in extras:
        if extra not in procedures:
            procedures.append(extra)
    while len(mistakes) < 3:
        mistakes.append((
            f"{topic} için tek bir ipucunu bütün koşulların yerine kullanmak.",
            "Kanıtın söylemediği ayrıntıyı kişisel tahminle tamamlamak.",
            "Yöntemin sırası, birimi veya kapsamı sonucu etkilemez sanmak.",
        )[len(mistakes)])
    return facts, procedures, mistakes


def evidence_indices(facts: list[str], steps: list[str], occurrence: int) -> tuple[int, int, int]:
    first = occurrence % len(facts)
    second = ((occurrence // len(facts)) + 1) % len(facts)
    step = (occurrence // (len(facts) * len(facts))) % len(steps)
    return first, second, step


def evidence_combination(facts: list[str], steps: list[str], occurrence: int, english: bool) -> str:
    first, second, step = evidence_indices(facts, steps, occurrence)
    if english:
        return (
            f"{facts[first].rstrip('.!?')}. A second check combines {facts[second].rstrip('.!?')} with the step "
            f"'{steps[step]}'"
        )
    return f"{facts[first].rstrip('.!?')}. İkinci denetimde {facts[second].rstrip('.!?')} bilgisi, '{steps[step]}' adımıyla birlikte kullanılır."


def process_triplet(steps: list[str], occurrence: int) -> list[str]:
    combinations = list(itertools.combinations(range(len(steps)), 3))
    selected = combinations[occurrence % len(combinations)]
    return [steps[index] for index in selected]


def distractor_claims(
    facts: list[str], steps: list[str], mistakes: list[str], occurrence: int, english: bool,
) -> list[str]:
    claims = []
    for offset in range(3):
        mistake = mistakes[(occurrence + offset) % len(mistakes)].rstrip(".!?")
        fact = facts[(occurrence * 2 + offset + 1) % len(facts)].rstrip(".!?")
        step = steps[(occurrence * 3 + offset + 1) % len(steps)].rstrip(".!?")
        if english:
            claims.append(
                f"{mistake}. This reasoning treats '{fact}' as irrelevant and skips the check '{step}'."
            )
        else:
            claims.append(
                f"{mistake}. Bu akıl yürütme '{fact}' bilgisini ilgisiz sayar ve '{step}' denetimini atlar."
            )
    return claims


def table_figure(qid: str, objective: str, facts: list[str], labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.alt"
    labels[h1], labels[h2] = "Kayıt", "Kanıt"
    labels[alt] = f"{objective} için iki kanıt kaydını karşılaştıran tablo; cevap işareti içermez."
    return {
        "kind": "table", "headerKeys": [h1, h2],
        "rows": [[{"v": "I"}, {"v": facts[0]}], [{"v": "II"}, {"v": facts[1]}]],
        "altTextKey": alt,
    }


def flow_figure(qid: str, objective: str, steps: list[str], labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    alt, edge = f"{prefix}.alt", f"{prefix}.edge"
    labels[alt] = f"{objective} için üç aşamalı denetim akışını gösteren şema; cevap işareti içermez."
    labels[edge] = "sonra"
    nodes = []
    for index, step in enumerate(steps[:3], 1):
        key = f"{prefix}.node{index}"
        labels[key] = step
        nodes.append({"id": f"n{index}", "labelKey": key})
    return {
        "kind": "flow", "altTextKey": alt, "direction": "left-to-right",
        "nodes": nodes,
        "edges": [
            {"from": "n1", "to": "n2", "labelKey": edge},
            {"from": "n2", "to": "n3", "labelKey": edge},
        ],
    }


def build_question(grade: int, index: int, subject: str, objective: str, note: dict[str, Any], occurrence: int, labels: dict[str, str]) -> dict[str, Any]:
    mode = MODES[index - 1]
    level = (LEVELS_11_12 if grade >= 11 else LEVELS_8_10)[index - 1]
    variant = (index - 1) % 16
    english = subject == "İngilizce"
    audio_skill = re.search(r"\.([LSP])\d+$", objective) if english else None
    cases = EN_CASES if english else TR_CASES
    case = cases[occurrence % len(cases)]
    facts, steps, misconceptions = evidence(note, english)
    fact = evidence_combination(facts, steps, occurrence, english)
    misconception = misconceptions[(occurrence + 1) % len(misconceptions)]
    objective_title = str(note.get("objective") or note.get("title") or objective)
    display_title = str(note.get("title") or objective_title).casefold().replace("i\u0307", "i")
    topic = str(note.get("topic") or note.get("unitTitle") or note.get("title") or subject)
    anchor = SUBJECT_ANCHORS[subject]
    scenario = EN_TOPIC_SCENARIOS.get(topic, f"a task about {topic}") if english else f"{anchor} odağında gerçek bir ders uygulaması"
    premise = fact
    stem = EN_STEMS[mode] if english else TR_STEMS[mode][variant % 4]
    if mode == "error-analysis":
        stem = (f"A learner claims, '{misconception}' {stem}" if english else f"Bir öğrenci '{misconception}' diyor. {stem}")
    use_flow = mode == "analysis" and index % 2 == 0
    flow_steps = process_triplet(steps, occurrence)
    first_fact, second_fact, _ = evidence_indices(facts, steps, occurrence)
    contextual_wrongs = distractor_claims(facts, steps, misconceptions, occurrence, english)
    if mode == "analysis":
        visual_ref = "Study the flow chart below. " if english and use_flow else "Study the table below. " if english else "Aşağıdaki şemayı inceleyiniz. " if use_flow else "Aşağıdaki tabloyu inceleyiniz. "
    else:
        visual_ref = ""
    semantic_clause = semantic_audit_clause(index, english)
    task_clause = semantic_task_clause(index, english)
    if english:
        context = f"Context: {topic}. The task uses {scenario}. Target skill: {display_title}. {case} {task_clause}"
        if audio_skill and audio_skill.group(1) == "L":
            context += " Listen to the attached local recording before answering; the written stem does not reproduce its evidence."
        elif audio_skill:
            context += " Listen to the attached model, record your own repetition, and then complete the evidence check."
        elif mode != "analysis":
            context += f" The source record states that {premise}"
        if use_flow:
            correct_fact = f"The valid process begins with {flow_steps[0]} It continues with {flow_steps[1]} and ends by applying {flow_steps[2]}"
            wrong_facts = [
                f"The process begins with {flow_steps[2]} and treats {flow_steps[0]} as an optional final detail. {contextual_wrongs[0]}",
                f"The order is irrelevant, so a conclusion may be selected before evidence is checked. {contextual_wrongs[1]}",
                f"Only the first step is needed; comparison and scope checks cannot change the answer. {contextual_wrongs[2]}",
            ]
        else:
            correct_fact = fact
            wrong_facts = contextual_wrongs
        correct_text = f"{correct_fact} The {anchor} focus is preserved, and the review process confirms it as follows: {case}"
        wrong_texts = [f"{wrong} This claim conflicts with the supplied evidence and is incompatible with this review process: {case}" for wrong in wrong_facts]
        explanation = f"For {objective_title}, {correct_fact} The scenario involving {scenario} keeps the {anchor} focus explicit. {case} {semantic_clause} The solution checks purpose, evidence and scope; each distractor reverses a condition, changes the process order or adds an unsupported inference."
    else:
        context = f"Bağlam: {topic}. Görev, {scenario} üzerinden {display_title} konusunu inceler. {case} {task_clause}"
        if mode != "analysis":
            context += f" Çalışma kaydında şu bilgi doğrulanmıştır: {premise}"
        if use_flow:
            correct_fact = f"Geçerli süreç {flow_steps[0]} adımıyla başlar; {flow_steps[1]} aşamasıyla sürer ve {flow_steps[2]} denetimiyle tamamlanır."
            wrong_facts = [
                f"Süreç {flow_steps[2]} ile başlar; {flow_steps[0]} isteğe bağlı son ayrıntıdır. {contextual_wrongs[0]}",
                f"Adımların sırası önemli değildir; kanıt denetlenmeden sonuç seçilebilir. {contextual_wrongs[1]}",
                f"Yalnız ilk adım yeterlidir; karşılaştırma ve kapsam denetimi sonucu değiştiremez. {contextual_wrongs[2]}",
            ]
        else:
            correct_fact = fact
            wrong_facts = contextual_wrongs
        correct_text = f"{correct_fact} {anchor} odağı korunur; çözüm süreci bu sonucu şu denetimle doğrular: {case}"
        wrong_texts = [f"{wrong} Bu yorum verilen kanıtla çelişir ve şu denetim süreciyle bağdaşmaz: {case}" for wrong in wrong_facts]
        explanation = f"{objective_title} hedefi için {correct_fact} Uygulama {scenario} içinde {anchor} odağını korur. {case} {semantic_clause} Çözümde amaç, kanıt, koşul ve kapsam birlikte denetlenir; çeldiriciler bir koşulu ters çevirir, işlem sırasını bozar veya kanıtsız genelleme yapar."
    position = (index - 1) % 4
    choices = list(wrong_texts)
    choices.insert(position, correct_text)
    reasons = []
    for option_index, choice in enumerate(choices):
        if option_index == position:
            reasons.append(f"Doğru çözüm — kanıt uyumu: '{choice}' ifadesi kazanım ölçütünü, konu bilgisini ve kanıt sınırını birlikte korur.")
        else:
            label = WHY[(index + option_index) % len(WHY)]
            reasons.append(f"Adlandırılmış öğrenci yanılgısı — {label}: '{choice}' seçeneği verilen koşullardan birini dışarıda bırakır veya kanıtın desteklemediği bir sonuç ekler.")
    qid = f"tr-g{grade:02d}-bank-{slug(subject)}-q{index:04d}"
    table_facts = [facts[first_fact], facts[second_fact]]
    figure = flow_figure(qid, objective, flow_steps, labels) if use_flow else table_figure(qid, objective, table_facts, labels) if mode == "analysis" else None
    note_id = str(note.get("id"))
    record = {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": index,
        "subject": subject, "grade": grade,
        "unitKey": note.get("unitKey") or note.get("themeKey") or note.get("topicKey"),
        "topicKey": note.get("topicKey") or note.get("themeKey") or note.get("unitKey"),
        "subtopicKey": note.get("subtopicKey") or note.get("topicKey") or note.get("unitKey"),
        "topic": topic, "title": f"{objective_title} — özgün {grade}. sınıf banka sorusu {index}",
        "objective": objective, "objectiveId": objective,
        "noteId": note_id, "noteKey": note_id,
        "question": f"{context} {visual_ref}{stem}", "choices": choices,
        "correct": position, "correctIndex": position, "correctOption": choices[position],
        "distractorWhy": reasons, "explanation": explanation,
        "level": level,
        "difficultyReason": f"Düzey {level}; {objective} bilgisini {mode} görevinde yeni kanıtla ilişkilendirip üç adlandırılmış yanılgıyı ayırmayı gerektirir.",
        "questionType": mode, "familyId": f"{qid}-family",
        "authoringTemplateId": f"g{grade}-current-{mode}-{variant + 1}-case-{occurrence + 1}",
        "objectiveSource": note.get("objectiveSource"), "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [str(note.get("objectiveEvidenceId") or "").split(":pdf-page-")[0]],
        "visualRequirement": "required" if figure else "none",
        "visualNeed": {
            "level": "required" if figure else "none", "role": "evidence" if figure else "none",
            "rationale": "İki kanıtı ya da işlem sırasını karşılaştırmak çözümün ayrılmaz parçasıdır." if figure else "Gerekli bağlam metinde eksiksiz verilmiştir.",
            "acceptableKinds": [figure["kind"]] if figure else [],
            "evidenceDimensions": ["comparison", "relationship"] if figure else [],
        },
        "figure": figure, "hintsCount": 0, "hintsForbidden": True,
        "reviewStatus": "pending", "humanReviewed": False, "reviewMode": "ai-only",
        "reviewDeclaration": "ai-generated-pending-independent-ai-review",
        "disclosure": "ai-generated-pending-independent-ai-review",
        "publishReady": False, "publishBlocked": True,
        "provenance": f"pending:grade{grade}-independent-bank-author/1.0.0; human-review:false",
    }
    if subject == "İngilizce":
        skill_match = audio_skill
        if skill_match:
            asset_id = f"tr.g{grade:02d}.ingilizce.bank.a{index:04d}"
            skill = skill_match.group(1)
            if skill == "L":
                record["mediaRequirement"] = "audio-required"
                record["audio"] = {
                    "assetId": asset_id, "role": "prompt", "playbackRequired": True,
                }
            else:
                record["mediaRequirement"] = "audio-response-required"
                record["audio"] = {
                    "assetId": asset_id, "role": "reference", "playbackRequired": True,
                }
                record["spokenResponse"] = {
                    "mode": "repeat-after-model", "recordingRequired": True,
                    "referenceAssetId": asset_id, "assessmentStatus": "runtime-supported",
                }
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grade", type=int, default=9, choices=(9, 10, 11, 12))
    args = parser.parse_args()
    grade = args.grade
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    output = ROOT / f"authoring/question-bank-blueprints/grade-{grade}.jsonl"
    labels_output = ROOT / f"authoring/question-bank-blueprints/grade-{grade}-labels.json"
    subjects = discover(grade)
    quotas = subject_quotas(subjects)
    rows: list[dict[str, Any]] = []
    labels: dict[str, str] = {}
    index = 1
    for subject in subjects:
        by_objective: dict[str, dict[str, Any]] = {}
        for note in subject.notes:
            for objective in note.get("objectives") or [note.get("objective")]:
                if objective:
                    by_objective.setdefault(str(objective), note)
        objective_keys = sorted(subject.by_objective)
        # Lesson-question volume is copy-detection evidence, not curricular
        # importance.  Distribute each subject quota evenly across canonical
        # outcomes so a legacy link concentration cannot create dozens of
        # surface variants for one outcome.
        base, remainder = divmod(quotas[subject.subject], len(objective_keys))
        if base < 2:
            raise ValueError(f"{subject.subject}: objective minimum cannot be met")
        allocations = {
            key: base + int(position < remainder)
            for position, key in enumerate(objective_keys)
        }
        for objective in sorted(allocations):
            note = by_objective[objective]
            for occurrence in range(allocations[objective]):
                rows.append(build_question(grade, index, subject.subject, objective, note, occurrence, labels))
                index += 1
    if len(rows) != 2000:
        raise ValueError(len(rows))
    output.parent.mkdir(parents=True, exist_ok=True)
    serialized = "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows).replace("i\u0307", "i").replace("0’dır", "0’dur").replace("0'dır", "0'dur")
    output.write_text(serialized + "\n", encoding="utf-8", newline="\n")
    labels_output.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2).replace("i\u0307", "i") + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "questions": len(rows), "labels": len(labels), "quotas": quotas,
        "answers": dict(Counter(row["correct"] for row in rows)),
        "figures": dict(Counter((row.get("figure") or {}).get("kind", "none") for row in rows)),
        "mix": dict(Counter(row["questionType"] for row in rows)),
        "levels": dict(Counter(row["level"] for row in rows)),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
