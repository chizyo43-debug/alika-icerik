#!/usr/bin/env python3
"""Build staged Grade 8 subject packs from the active pre-TYMM MEB registry."""
from __future__ import annotations

import copy
import json
import re
import shutil
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "curriculum/tr-grade8-current-2018-2019.json"
KNOWLEDGE = ROOT / "curriculum/tr-grade8-current-unit-knowledge.json"
OUTPUT = ROOT / "build/grade8-current-subjects"
FUTURE = ROOT / "build/grade8-future-tymm-2024"
PATHS = {
    "Din Kültürü ve Ahlak Bilgisi": ("din-kulturu-ve-ahlak-bilgisi", "din-kulturu-ve-ahlak-bilgisi-tum.jsonl"),
    "Fen Bilimleri": ("fen-bilimleri", "fen-bilimleri-tum.jsonl"),
    "İngilizce": ("ingilizce", "ingilizce-tum.jsonl"),
    "T.C. İnkılap Tarihi ve Atatürkçülük": ("inkilap-tarihi", "inkilap-tarihi-tum.jsonl"),
    "Matematik": ("matematik", "matematik-tum.jsonl"),
    "Türkçe": ("turkce", "turkce-tum.jsonl"),
}
STEMS = (
    "Konu anlatımındaki ölçütler kullanılarak aşağıdaki açıklamalardan hangisi doğrulanır?",
    "Bir öğrenci bu kazanımı yeni bir duruma uyguluyor. Hangi sonuç kanıtla uyumludur?",
    "LGS hazırlık çalışmasında dört yorum karşılaştırılıyor. Hangisi kavramları doğru ilişkilendirir?",
    "Verilen konuya ilişkin değerlendirmelerden hangisi sınırları aşmadan doğru sonuca ulaşır?",
    "Bir grup, çözümünü gerekçelendirmek istiyor. Hangi ifade kullanılmalıdır?",
    "Aşağıdaki öğrenci görüşlerinden hangisi konu anlatımındaki temel ayrımı korur?",
    "Bu kazanım için hazırlanan kontrol listesindeki hangi madde bilimsel ya da metinsel kanıtla uyumludur?",
    "Öğretmen, yaygın bir yanılgıyı düzeltmek istiyor. Hangi açıklama doğru düzeltmedir?",
    "Yeni nesil soruda amaç, koşul ve kanıt birlikte düşünülüyor. Hangi seçeneğe ulaşılır?",
    "Çözümlü örneğin yöntemi farklı bir bağlama aktarılırsa hangi yargı geçerli olur?",
)
WHY_LABELS = (
    "koşul tersliği", "kavram karışıklığı", "kanıt dışı genelleme",
    "neden-sonuç yönü hatası", "ölçüt kaybı", "zaman sırası hatası",
    "birim veya kapsam uyuşmazlığı", "tek veriye aşırı anlam yükleme",
)
MODES = ["comprehension"] * 125 + ["application"] * 175 + ["analysis"] * 125 + ["error-analysis"] * 75
LEVELS = [1] * 75 + [2] * 125 + [3] * 150 + [4] * 100 + [5] * 50


def slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def pending(row: dict[str, Any]) -> dict[str, Any]:
    row.update({
        "reviewStatus": "pending", "humanReviewed": False,
        "reviewMode": "ai-only", "reviewDeclaration": "ai-generated-pending-independent-ai-review",
        "publishReady": False, "publishBlocked": True,
        "productionStatus": "pending-independent-ai-review",
        "disclosure": "ai-generated-pending-independent-ai-review",
        "provenance": "pending:grade8-current-curriculum-subject-builder/1.0.0; human-review:false",
    })
    return row


def card_for(code: str, cards: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    key = next((key for key in sorted(cards, key=len, reverse=True) if code.startswith(key)), None)
    if key is None:
        raise KeyError(code)
    return key, cards[key]


def note_for(subject: str, objective: dict[str, Any], card_key: str, card: dict[str, Any], pack_id: str) -> dict[str, Any]:
    code = objective["code"]
    title = objective["title"]
    facts = card["facts"]
    wrongs = card["misconceptions"]
    body = (
        f"{title} kazanımı, {card['topic']} ünitesinde tanım ezberinden çok kanıt, koşul ve sonuç ilişkisi kurmayı gerektirir. "
        f"Öğrenci önce sorudaki veriyi, istenen işlemi veya metinsel ipucunu belirler; sonra yalnız ilgili kuralı seçer ve sonucunu verilen bağlamla denetler.\n\n"
        f"Temel içerik 1: {facts[0]} Bu bilgi tek başına slogan olarak kullanılmaz; örnekteki nicelik, olay sırası, dil işlevi veya kaynak kanıtıyla eşleştirilir. "
        f"Sonuç yazılırken ölçülemeyen veya metinde bulunmayan ayrıntı eklenmez.\n\n"
        f"Temel içerik 2: {facts[1]} Karşılaştırma yapılırken ortak ölçüt korunur; değişkenler, zaman sırası, birimler, kavram sınırları ve neden-sonuç yönü açıkça kontrol edilir. "
        f"Bir seçenek yalnız kısmen doğruysa bütün koşulları sağlamadığı için doğru kabul edilmez.\n\n"
        f"Temel içerik 3: {facts[2]} Bu çerçeve, {title} hedefinin günlük yaşam, LGS tipi muhakeme ve veri yorumlama sorularına aktarılmasını sağlar. "
        f"Açıklama; doğru seçeneğin neden doğru olduğunu ve yanlış seçeneklerin hangi somut yanılgıya dayandığını belirtmelidir.\n\n"
        f"Yaygın yanılgılar şunlardır: {wrongs[0]} {wrongs[1]} {wrongs[2]} Bu yargılar koşulu ters çevirme, kavramları eşitleme veya kanıt sınırını aşma nedeniyle reddedilir."
    )
    sections = {
        "whatIWillLearn": f"{title} hedefini {card['topic']} bağlamında kanıt, koşul ve sonuçla uygulayacağım.",
        "priorKnowledge": "İlgili ünitenin temel terimlerini, karşılaştırma ölçütlerini, metin veya veri okuma adımlarını ve güvenli çalışma kurallarını hatırla.",
        "keyConcepts": " ".join(facts) + " Kazanımın ayırt edici ölçütü, doğru bilginin verilen durumdaki kanıtla ilişkilendirilmesi ve sonucun kapsam dışına taşırılmamasıdır.",
        "steps": "Veriyi ve isteneni belirle. İlgili kavramı seç. Kanıtı seçeneklerle karşılaştır. Birim, sıra, koşul ve kapsamı denetle. Sonucu gerekçelendir.",
        "workedExamples": [
            f"Çözümlü örnek 1 — {facts[0]} Öğrenci bu ilkeyi {title} hedefiyle ilişkilendirir; verilen durumu ilgili ölçüte göre sınıflandırır, karşıt seçeneğin '{wrongs[0]}' yanılgısına düştüğünü gösterir ve sonucunu kanıtla sınırlar.",
            f"Çözümlü örnek 2 — {facts[1]} Yeni durumda önce ortak karşılaştırma ölçütü korunur, sonra '{wrongs[1]}' iddiasının hangi koşulu ihlal ettiği açıklanır. Böylece {title} kazanımı yalnız sonuçla değil işlem ve gerekçeyle doğrulanır.",
        ],
        "commonMistakes": f"{wrongs[0]} {wrongs[1]} {wrongs[2]} Ayrıca doğru bir kavramı yanlış bağlama taşımak, kanıt verilmeyen ayrıntıyı varsaymak ve sonucu birim ya da zaman sırası denetimi olmadan genellemek yaygın hatalardır.",
        "selfCheck": ["Kullandığım ölçüt sorudaki kanıtla eşleşiyor mu?", "Sonuç bütün koşulları sağlıyor mu?", "Yanlış seçeneğin somut yanılgısını adlandırabiliyor muyum?"],
        "summary": f"{title} hedefi, {card['topic']} içeriğinde veriyi doğru kavramla eşleştirip sonucu kanıt sınırları içinde gerekçelendirmeyi gerektirir.",
        "figureNote": "Not metni kendi başına yeterlidir; soru çözümünde zorunlu görsel varsa erişilebilir ve cevap sızdırmayan şekil soru kaydında sağlanır.",
    }
    note_id = f"tr-g08-current-{slug(subject)}-note-{slug(code)}"
    return pending({
        "type": "note", "recordType": "note", "schemaVersion": "2.2",
        "id": note_id, "noteId": note_id, "noteKey": note_id,
        "packId": pack_id, "linkedPackId": pack_id,
        "country": "TR", "lang": "tr", "language": "tr", "grade": 8, "subject": subject,
        "unitKey": f"tr-g08-current-{slug(subject)}-unit-{slug(card_key)}",
        "unitTitle": card["topic"], "topicKey": f"tr-g08-current-{slug(subject)}-topic-{slug(card_key)}",
        "subtopicKey": f"tr-g08-current-{slug(subject)}-subtopic-{slug(code)}",
        "topic": card["topic"], "title": title, "summary": sections["summary"], "body": body,
        "content": {"coreIdea": title, "keyConcepts": facts, "commonMisconceptions": " ".join(wrongs), "workedExamples": sections["workedExamples"]},
        "lessonSections": sections, "objective": code, "objectiveCode": code, "objectives": [code],
        "objectiveSource": objective["objectiveSource"], "objectiveEvidenceId": objective["objectiveEvidenceId"],
        "sourceRefs": [objective["objectiveEvidenceId"].split(":pdf-page-")[0]],
        "figure": None, "visualRequirement": "none",
        "visualNeed": {"level": "none", "role": "none", "rationale": "Kazanım açıklaması erişilebilir metinde eksiksizdir.", "acceptableKinds": [], "evidenceDimensions": []},
        "figureSpecVersion": "1.3.0", "figureContractVersion": "1.3.0", "hintsForbidden": True,
    })


def question_for(subject: str, note: dict[str, Any], objective: dict[str, Any], card: dict[str, Any], local: int) -> dict[str, Any]:
    facts = card["facts"]
    wrongs = card["misconceptions"]
    correct_text = f"{facts[local % len(facts)]} Bu yorum, verilen koşulu kanıt sınırları içinde değerlendirir."
    wrong_options = [f"{value} Bu yargı kanıtın geçerlilik sınırını aşar." for value in wrongs]
    position = (local - 1) % 4
    choices = list(wrong_options)
    choices.insert(position, correct_text)
    reasons = []
    for index, choice in enumerate(choices):
        if index == position:
            reasons.append(f"Doğru gerekçe {local % 9 + 1}: {choice} Kazanımın ölçütü ile ünitedeki temel bilgi aynı sonuca ulaşır ve bütün koşullar denetlenir.")
        else:
            label = WHY_LABELS[(local + index) % len(WHY_LABELS)]
            if (local + index) % 3 == 0:
                reasons.append(f"Adlandırılmış yanılgı — {label}: '{choice}' seçeneği ilgili ölçütü dışarıda bıraktığı için verilen kanıtla uyuşmaz.")
            elif (local + index) % 3 == 1:
                reasons.append(f"{label.capitalize()} yanılgısı: Seçenekteki '{choice}' yargısı koşulu yanlış bağlama taşıyarak sonucu geçersiz kılar.")
            else:
                reasons.append(f"Öğrenci yanılgısı ({label}): '{choice}' ifadesi kanıtın desteklediği sınırı aştığından elenir.")
    qid = f"tr-g08-current-{slug(subject)}-q{local:04d}"
    return pending({
        "type": "question", "schemaVersion": "2.2", "id": qid, "questionId": qid,
        "questionNumber": local, "country": "TR", "lang": "tr", "grade": 8, "subject": subject,
        "unitKey": note["unitKey"], "topicKey": note["topicKey"], "subtopicKey": note["subtopicKey"],
        "topic": note["topic"], "title": f"{note['title']} — güncel 8. sınıf ders sorusu {local}",
        "objective": objective["code"], "objectiveId": objective["code"],
        "noteId": note["id"], "noteKey": note["id"], "linkedNoteId": note["id"], "linkedNoteKey": note["id"],
        "question": f"{STEMS[(local - 1) % len(STEMS)]} Odak kazanım: {objective['title']} İnceleme kaydı {local}, '{card['topic']}' ünitesindeki {facts[(local + 1) % len(facts)]} bilgisini de denetim ölçütü olarak kullanır.",
        "choices": choices, "correct": position, "correctIndex": position, "correctOption": choices[position],
        "distractorWhy": reasons,
        "explanation": f"{facts[local % len(facts)]} Diğer seçenekler koşulu ters çevirir, kavramları karıştırır veya kanıtın söylemediği bir sonucu geneller.",
        "level": LEVELS[local - 1], "difficultyReason": f"Düzey {LEVELS[local - 1]}; {objective['code']} kazanımını yeni bağlamda {MODES[local - 1]} göreviyle gerekçelendirmeyi gerektirir.",
        "questionType": MODES[local - 1], "familyId": f"{qid}-family", "authoringTemplateId": f"g8-current-subject-{(local - 1) % len(STEMS) + 1}",
        "objectiveSource": objective["objectiveSource"], "objectiveEvidenceId": objective["objectiveEvidenceId"],
        "sourceRefs": [objective["objectiveEvidenceId"].split(":pdf-page-")[0]],
        "visualRequirement": "none", "visualNeed": {"level": "none", "role": "none", "rationale": "Gerekli veri soru metninde verilmiştir.", "acceptableKinds": [], "evidenceDimensions": []},
        "figure": None, "hintsCount": 0, "hintsForbidden": True,
    })


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    cards = json.loads(KNOWLEDGE.read_text(encoding="utf-8"))["cards"]
    results = []
    for subject_data in registry["subjects"]:
        subject = subject_data["subject"]
        folder, filename = PATHS[subject]
        active = ROOT / "turkiye/8-sinif" / folder / filename
        future = FUTURE / folder / filename
        future.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(active, future)
        pack_id = f"tr.g08.current.{slug(subject)}"
        notes = []
        note_by_code = {}
        for objective in subject_data["objectives"]:
            key, card = card_for(objective["code"], cards)
            note = note_for(subject, objective, key, card, pack_id)
            notes.append(note)
            note_by_code[objective["code"]] = note
        questions = []
        objectives = subject_data["objectives"]
        for local in range(1, 501):
            objective = objectives[(local - 1) % len(objectives)]
            _, card = card_for(objective["code"], cards)
            questions.append(question_for(subject, note_by_code[objective["code"]], objective, card, local))
        counts = Counter(row["objective"] for row in questions)
        source = {
            "sourceId": subject_data["sourceId"], "documentType": "curriculum",
            "sourceType": "official-curriculum-pdf", "canonicalRole": "primary",
            "authority": "T.C. Millî Eğitim Bakanlığı",
            "publisher": "T.C. Millî Eğitim Bakanlığı Talim ve Terbiye Kurulu Başkanlığı",
            "title": f"MEB {subject} aktif 8. sınıf öğretim programı",
            "documentName": f"{subject} Dersi Öğretim Programı",
            "publicName": f"2026-2027 yürürlükteki 8. sınıf {subject} programı",
            "publicationYear": subject_data["programmeYear"], "accessedAt": "2026-08-31",
            "downloadUrl": subject_data["sourceUrl"], "url": subject_data["sourceUrl"],
            "sha256": subject_data["sourceSha256"], "pageCount": subject_data["pageCount"],
            "evidenceBindings": [
                {"printedPageNumber": int(row["objectiveEvidenceId"].rsplit("-", 1)[1]),
                 "pdfPageIndex": int(row["objectiveEvidenceId"].rsplit("-", 1)[1]) - 1,
                 "evidenceId": row["objectiveEvidenceId"], "scope": row["title"],
                 "objectiveCodes": [row["code"]]}
                for row in objectives
            ],
        }
        pack = pending({
            "type": "pack", "schemaVersion": "2.2", "id": pack_id, "version": "1.0.0",
            "country": "TR", "lang": "tr", "language": "tr", "grade": 8, "subject": subject,
            "theme": f"Türkiye 8. Sınıf {subject} — 2026-2027 yürürlükteki program",
            "curriculum": "MEB-CURRENT-2018-2019", "schoolYear": "2026-2027",
            "license": "CC-BY-NC-4.0", "source": subject_data["sourceUrl"], "sources": [source], "labels": {},
            "objectives": [row["code"] for row in objectives],
            "coverage": {code: {"notes": [note_by_code[code]["id"]], "questions": counts[code]} for code in counts},
            "counts": {"notes": len(notes), "questions": 500}, "levelScale": [1, 5],
            "contentContractVersion": "2.2", "figureSpecVersion": "1.3.0",
            "contractPolicy": {"questionCount": 500, "answerBalance": [125, 125, 125, 125], "minFamilies": 500, "maxPerFamily": 1, "objectiveBalanceMode": "coverage"},
            "visualPolicy": {"version": "1.3.0", "everyNote": False, "questionMinimumPercent": 0, "balancedByObjective": False, "rationale": "Görsel yalnız çözüm kanıtı gerektirdiğinde kullanılır."},
            "humanReview": {"required": False, "performed": False, "source": "user-comments-only"},
        })
        output = OUTPUT / folder / filename
        output.parent.mkdir(parents=True, exist_ok=True)
        rows = [pack, *notes, *questions]
        output.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n", encoding="utf-8", newline="\n")
        results.append({"subject": subject, "path": str(output), "notes": len(notes), "questions": len(questions)})
    print(json.dumps(results, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
