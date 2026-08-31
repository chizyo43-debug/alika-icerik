#!/usr/bin/env python3
"""Author the active-curriculum Grade 8 bank independently from lesson questions."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from build_grade8_current_subject_candidates import WHY_LABELS, card_for, slug
from build_unique_question_banks import ROOT, largest_remainder


REGISTRY = ROOT / "curriculum/tr-grade8-current-2018-2019.json"
KNOWLEDGE = ROOT / "curriculum/tr-grade8-current-unit-knowledge.json"
OUTPUT = ROOT / "authoring/question-bank-blueprints/grade-8.jsonl"
LABELS = ROOT / "authoring/question-bank-blueprints/grade-8-labels.json"
# Each independently inspectable 100-question batch must carry the target
# ratios itself; a globally shuffled 2,000-row schedule can satisfy the total
# while leaving individual review batches skewed.
MODE_SCHEDULE = (
    ["comprehension"] * 25
    + ["application"] * 35
    + ["analysis"] * 25
    + ["error-analysis"] * 15
) * 20
LEVEL_SCHEDULE = ([1] * 15 + [2] * 25 + [3] * 30 + [4] * 20 + [5] * 10) * 20
STEMS = {
    "comprehension": (
        "Kısa konu kartındaki temel ayrımı doğru kuran açıklama hangisidir?",
        "Aşağıdaki yargılardan hangisi kavramın ayırt edici özelliğini korur?",
        "Bir öğrenci tanım ile örneği eşleştiriyor. Hangi eşleştirme savunulabilir?",
        "Verilen bağlamda temel bilgiyi çarpıtmadan aktaran seçenek hangisidir?",
    ),
    "application": (
        "Öğrenci bu bilgiyi yeni bir duruma uyguladığında hangi sonuca ulaşmalıdır?",
        "Günlük yaşam bağlamında aynı ölçüt kullanılırsa hangi açıklama geçerli olur?",
        "Çözümlü örneğin yöntemi aşağıdaki duruma aktarıldığında hangi seçenek seçilir?",
        "Amaç, koşul ve kanıt birlikte değerlendirildiğinde hangi uygulama doğrudur?",
    ),
    "analysis": (
        "Kanıt tablosundaki iki kayıt birlikte yorumlandığında hangi sonuca ulaşılır?",
        "Tablodaki gözlem ve ölçüt arasındaki ilişkiyi doğru çözümleyen seçenek hangisidir?",
        "Sunulan verilerden çıkarılabilecek en kapsamlı ve kanıtla sınırlı yargı hangisidir?",
        "İki kanıt satırı karşılaştırıldığında hangi açıklama desteklenir?",
    ),
    "error-analysis": (
        "Bir öğrencinin hatalı genellemesini gerekçesiyle düzelten seçenek hangisidir?",
        "Çözümdeki kavram yanılgısını belirleyip doğru ölçütü geri kuran ifade hangisidir?",
        "Aşağıdaki seçeneklerden hangisi hatanın nedenini göstererek doğru sonucu verir?",
        "Öğrenci görüşündeki kanıt sınırı ihlalini düzelten açıklama hangisidir?",
    ),
}
CASE_VARIANTS = (
    "Öğrenci önce kavramları sınıflandırıp ardından yalnız doğrudan desteklenen sonucu işaretlemektedir.",
    "Çalışma grubu iki karşı örnek aramış, genellemenin geçerli olduğu koşulları ayrıca kaydetmiştir.",
    "Deneme çözümünde amaç, kullanılan yöntem ve ulaşılan sonuç ayrı sütunlarda karşılaştırılmıştır.",
    "Öğretmen bir yanlış örneği düzelttikten sonra aynı ölçütün yeni bağlamda korunmasını istemiştir.",
    "Araştırma ekibi kaynak, gözlem ve çıkarımı birbirine karıştırmadan üç aşamalı bir kontrol yapmıştır.",
    "Öğrenci çözümünü birim, zaman sırası ve kavram sınırı bakımından yeniden denetlemiştir.",
    "Akran değerlendirmesinde her seçenek için destekleyen kanıt ve çürüten karşı kanıt birlikte yazılmıştır.",
    "Yeni nesil etkinlikte önce verilenler işaretlenmiş, sonra gereksiz bilgiler elenip sonuç gerekçelendirilmiştir.",
    "Kavram haritasında neden, süreç ve sonuç oklarla ayrılmış; ters yöndeki bağlantılar sorgulanmıştır.",
    "Öz değerlendirme formunda öğrenciden kuralı söylemesi değil, hangi koşulda kullanılacağını kanıtlaması istenmiştir.",
)
ENGLISH_CASE_VARIANTS = (
    "The learner classifies the language evidence before selecting only the directly supported conclusion.",
    "The group tests two counterexamples and records the exact condition under which the statement remains valid.",
    "The review separates purpose, language form and communicative result in three explicit steps.",
    "After correcting one misconception, the teacher asks learners to preserve the same criterion in a new context.",
    "The team distinguishes source detail, observation and inference before making a language decision.",
    "The learner checks time reference, word meaning and discourse purpose before confirming the answer.",
    "Peer reviewers write one supporting detail and one refuting detail for every option.",
    "The task marks the given information first, removes irrelevant details and then justifies the final choice.",
    "A concept map separates cause, process and result and challenges links that point in the wrong direction.",
    "The self-check asks not only for the rule but also for evidence showing when that rule applies.",
)
ENGLISH_STEMS = {
    "comprehension": "Which option preserves the key meaning and language function in the source?",
    "application": "Which response applies the target language to this new situation accurately?",
    "analysis": "Study the table below. Which conclusion is fully supported by both rows?",
    "error-analysis": "Which option identifies the misconception and restores the correct language choice?",
}


def table_figure(qid: str, objective: str, card: dict[str, Any], labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.alt"
    labels[h1] = "Kayıt"
    labels[h2] = "Kanıt"
    labels[alt] = f"{objective} kazanımı için iki kanıt kaydını gösteren tablo; doğru cevabı açıklamaz."
    return {
        "kind": "table", "headerKeys": [h1, h2],
        "rows": [[{"v": "I"}, {"v": card["facts"][0]}], [{"v": "II"}, {"v": card["facts"][1]}]],
        "altTextKey": alt,
    }


def build_question(index: int, subject: str, objective: dict[str, Any], card: dict[str, Any], labels: dict[str, str], occurrence: int) -> dict[str, Any]:
    mode = MODE_SCHEDULE[index - 1]
    level = LEVEL_SCHEDULE[index - 1]
    local_variant = (index - 1) % 12
    fact = card["facts"][(index + local_variant) % len(card["facts"])]
    misconception = card["misconceptions"][(index + 1) % len(card["misconceptions"])]
    stem = STEMS[mode][local_variant % 4]
    if mode == "error-analysis":
        stem = f"Bir öğrenci '{misconception}' diyor. {stem}"
    case_text = CASE_VARIANTS[occurrence % len(CASE_VARIANTS)]
    if subject == "İngilizce":
        case_text = ENGLISH_CASE_VARIANTS[occurrence % len(ENGLISH_CASE_VARIANTS)]
        stem = ENGLISH_STEMS[mode]
        if mode == "error-analysis":
            stem = f"A learner claims, '{misconception}' {stem}"
    context = (
        f"Bağlam: {card['topic']}. İnceleme ölçütü {objective['title']} hedefidir. "
        f"{case_text} "
        f"Çalışma kaydında {card['facts'][(index + occurrence + 1) % len(card['facts'])]} bilgisi ayrıca doğrulanmıştır."
    )
    if subject == "İngilizce":
        context = f"Context: {card['topic']}. Target outcome: {objective['title']} {case_text} The record also confirms that {card['facts'][(index + occurrence + 1) % len(card['facts'])]}"
        correct = f"For this outcome, {fact} The conclusion stays within the evidence because the review process is: {case_text}"
        wrongs = [f"For this outcome, {wrong} This conflicts with the evidence and ignores that {case_text}" for wrong in card["misconceptions"]]
    else:
        correct = f"{objective['title']} hedefinde {fact} Sonuç bu kanıtla sınırlıdır; inceleme süreci şöyle yürütülür: {case_text}"
        wrongs = [f"{objective['title']} hedefinde {wrong} Bu yorum kanıtla çelişir ve şu denetimi yok sayar: {case_text}" for wrong in card["misconceptions"]]
    position = (index - 1) % 4
    choices = list(wrongs)
    choices.insert(position, correct)
    reasons = []
    for option_index, choice in enumerate(choices):
        if option_index == position:
            reasons.append(f"Doğru çözüm {local_variant + 1}: '{choice}' ifadesi hem ünite bilgisini hem de kazanımın kanıt sınırını birlikte korur.")
        else:
            label = WHY_LABELS[(index + option_index) % len(WHY_LABELS)]
            forms = (
                f"Adlandırılmış yanılgı — {label}: '{choice}' seçeneği verilen koşullardan birini dışarıda bırakır.",
                f"{label.capitalize()} yanılgısı: Seçenekteki '{choice}' yargısı kanıtın desteklemediği bir sonucu ekler.",
                f"Öğrenci yanılgısı ({label}): '{choice}' ifadesi kavram ile bağlam arasındaki ilişkiyi ters kurar.",
            )
            reasons.append(forms[(index + option_index) % len(forms)])
    qid = f"tr-g08-bank-{slug(subject)}-q{index:04d}"
    needs_figure = mode == "analysis"
    figure = table_figure(qid, objective["code"], card, labels) if needs_figure else None
    note_id = f"tr-g08-current-{slug(subject)}-note-{slug(objective['code'])}"
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": index,
        "subject": subject, "grade": 8,
        "unitKey": f"tr-g08-current-{slug(subject)}-unit-{slug(next(key for key in sorted(CARDS, key=len, reverse=True) if objective['code'].startswith(key)))}",
        "topicKey": f"tr-g08-current-{slug(subject)}-topic-{slug(next(key for key in sorted(CARDS, key=len, reverse=True) if objective['code'].startswith(key)))}",
        "subtopicKey": f"tr-g08-current-{slug(subject)}-subtopic-{slug(objective['code'])}",
        "topic": card["topic"], "title": f"{objective['title']} — özgün 8. sınıf banka sorusu {index}",
        "objective": objective["code"], "objectiveId": objective["code"],
        "noteId": note_id, "noteKey": note_id,
        "question": f"{context} {'Şekildeki tabloyu inceleyiniz. ' if mode == 'analysis' and subject != 'İngilizce' else ''}{stem}", "choices": choices,
        "correct": position, "correctIndex": position, "correctOption": choices[position],
        "distractorWhy": reasons,
        "explanation": (f"{objective['title']} hedefi için {fact} {case_text} Çözümde amaç, kanıt ve kapsam birlikte denetlenir; diğer seçenekler somut bir koşulu ters çevirir veya kanıtsız genelleme yapar." if subject != "İngilizce" else f"For {objective['title']}, {fact} {case_text} The solution checks purpose, evidence and scope; the other options reverse a condition or add an unsupported inference."),
        "level": level, "difficultyReason": f"Düzey {level}; {objective['code']} bilgisini {mode} görevinde yeni kanıtla ilişkilendirip üç adlandırılmış yanılgıyı ayırmayı gerektirir.",
        "questionType": mode, "familyId": f"{qid}-family",
        "authoringTemplateId": f"g8-current-{mode}-{local_variant + 1}-case-{occurrence + 1}",
        "objectiveSource": objective["objectiveSource"], "objectiveEvidenceId": objective["objectiveEvidenceId"],
        "sourceRefs": [objective["objectiveEvidenceId"].split(":pdf-page-")[0]],
        "visualRequirement": "required" if needs_figure else "none",
        "visualNeed": {
            "level": "required" if needs_figure else "none",
            "role": "evidence" if needs_figure else "none",
            "rationale": "İki kanıt satırını karşılaştırmak çözümün ayrılmaz parçasıdır." if needs_figure else "Gerekli bağlam metinde eksiksiz verilmiştir.",
            "acceptableKinds": ["table"] if needs_figure else [],
            "evidenceDimensions": ["comparison", "relationship"] if needs_figure else [],
        },
        "figure": figure, "hintsCount": 0, "hintsForbidden": True,
        "reviewStatus": "pending", "humanReviewed": False, "reviewMode": "ai-only",
        "reviewDeclaration": "ai-generated-pending-independent-ai-review",
        "disclosure": "ai-generated-pending-independent-ai-review",
        "publishReady": False, "publishBlocked": True,
        "provenance": "pending:grade8-current-independent-bank-author/1.0.0; human-review:false",
    }


def main() -> int:
    global CARDS
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    CARDS = json.loads(KNOWLEDGE.read_text(encoding="utf-8"))["cards"]
    weights = {row["subject"]: len(row["objectives"]) for row in registry["subjects"]}
    minimums = {key: max(100, 2 * value) for key, value in weights.items()}
    quotas = largest_remainder(2000, weights, minimums, {key: 600 for key in weights})
    rows = []
    labels: dict[str, str] = {}
    global_index = 1
    for subject_data in registry["subjects"]:
        subject = subject_data["subject"]
        objectives = subject_data["objectives"]
        for local in range(quotas[subject]):
            objective = objectives[local % len(objectives)]
            _, card = card_for(objective["code"], CARDS)
            rows.append(build_question(global_index, subject, objective, card, labels, local // len(objectives)))
            global_index += 1
    if global_index != 2001:
        raise ValueError(global_index)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n", encoding="utf-8", newline="\n")
    LABELS.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "questions": len(rows), "labels": len(labels), "quotas": quotas,
        "answers": list(Counter(row["correct"] for row in rows).values()),
        "figures": sum(bool(row["figure"]) for row in rows),
        "mix": dict(Counter(row["questionType"] for row in rows)),
        "levels": dict(Counter(row["level"] for row in rows)),
    }, ensure_ascii=False))
    return 0


CARDS: dict[str, Any] = {}


if __name__ == "__main__":
    raise SystemExit(main())
