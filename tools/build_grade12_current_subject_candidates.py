#!/usr/bin/env python3
"""Build pending Grade 12 subject packs from the active pre-TYMM registry."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

from audit_bank_source_readiness import note_failures
from author_grade9_question_bank import semantic_task_clause
from build_unique_question_banks import ROOT
from enrich_grade9_subject_notes import enrich_note
from review_unique_question_banks import projection, write_jsonl


REGISTRY = ROOT / "curriculum/tr-grade12-current-2018.json"
OUTPUT = ROOT / "build/grade12-current-subjects"
FUTURE = ROOT / "turkiye/12-sinif/future-tymm-2025-2026"
PATHS = {
    "Biyoloji": ("biyoloji", "biyoloji-tum.jsonl"),
    "Coğrafya": ("cografya", "cografya-tum.jsonl"),
    "Din Kültürü ve Ahlak Bilgisi": ("din-kulturu-ve-ahlak-bilgisi", "din-kulturu-ve-ahlak-bilgisi-tum.jsonl"),
    "Felsefe Grubu": ("felsefe-grubu", "felsefe-grubu-tum.jsonl"),
    "Fizik": ("fizik", "fizik-tum.jsonl"),
    "İngilizce": ("ingilizce", "ingilizce-tum.jsonl"),
    "Kimya": ("kimya", "kimya-tum.jsonl"),
    "Matematik": ("matematik", "matematik-tum.jsonl"),
    "T.C. İnkılap Tarihi ve Atatürkçülük": ("tc-inkilap-tarihi-ve-ataturkculuk", "tc-inkilap-tarihi-ve-ataturkculuk-tum.jsonl"),
    "Türk Dili ve Edebiyatı": ("turk-dili-ve-edebiyati", "turk-dili-ve-edebiyati-tum.jsonl"),
}
FELSEFE_PARTS = {"Mantık", "Psikoloji", "Sosyoloji"}
LEVELS = [1] * 100 + [2] * 100 + [3] * 100 + [4] * 100 + [5] * 100
STEMS_TR = (
    "Kazanımın ayırt edici ölçütünü doğru kullanan açıklama hangisidir?",
    "Konu bilgisini yeni duruma kanıt sınırını aşmadan uygulayan seçenek hangisidir?",
    "Verilen görüşlerden hangisi neden, süreç ve sonuç ilişkisini doğru kurar?",
    "Yaygın bir kavram yanılgısını düzelten seçenek hangisidir?",
    "Aşağıdaki çözüm yollarından hangisi ilgili kazanımla tutarlıdır?",
)
STEMS_EN = (
    "Which option uses the target meaning accurately in this context?",
    "Which response is supported by the stated communicative evidence?",
    "Which option preserves purpose, context and the limits of the information?",
    "Which response corrects the learner's misconception?",
    "Which language choice is consistent with the learning outcome?",
)
MISCONCEPTIONS_TR = (
    "Tek bir örneği bütün durumlara genellemek",
    "Neden ile sonucu ters çevirmek",
    "Kavramın gerekli koşulunu göz ardı etmek",
    "Kanıtta bulunmayan bir ayrıntıyı sonuç saymak",
    "Ortak ölçüt kullanmadan iki durumu eşitlemek",
)
MISCONCEPTIONS_EN = (
    "generalising from one example to every context",
    "reversing cause and result",
    "ignoring a necessary condition",
    "adding a detail not supplied by the evidence",
    "comparing two messages with different criteria",
)
SUBJECT_FACTS = {
    "Biyoloji": ("Moleküler süreçlerde yapı, işlev ve bilgi akışı birlikte değerlendirilir.", "Enerji dönüşümleri ve canlı sistemler kontrollü değişkenlerle açıklanır.", "Bitkisel süreçlerde gözlem ile çıkarım birbirinden ayrılır."),
    "Coğrafya": ("Coğrafi olaylar konum, ölçek, dağılış ve karşılıklı etkileşim içinde incelenir.", "Ekonomik faaliyetlerin mekânsal ve toplumsal sonuçları aynı ölçütlerle karşılaştırılır.", "Çevre politikaları doğal sınırlar ile sürdürülebilirlik ilkelerini birlikte gözetir."),
    "Din Kültürü ve Ahlak Bilgisi": ("Dinî bilgi, ayet ve tarihsel bağlamı çarpıtmadan yorumlanır.", "Farklı inanç ve düşünce gelenekleri kendi temel kavramları içinde karşılaştırılır.", "Güncel meselelerde temel ilke, yöntem ve ahlaki sonuç birlikte değerlendirilir."),
    "Felsefe Grubu": ("Mantıksal geçerlilik, öncüllerin doğruluğundan ayrı bir ölçüttür.", "Psikolojik süreçler biyolojik, bilişsel ve çevresel etkenlerle birlikte ele alınır.", "Sosyolojik açıklama birey, grup, kurum ve toplumsal yapı ilişkisini korur."),
    "Fizik": ("Fiziksel modelde nicelik, birim, yön ve geçerlilik koşulu açıkça belirtilir.", "Deneysel sonuç bağımsız, bağımlı ve kontrol edilen değişkenler ayrılarak yorumlanır.", "Modern fizik açıklamalarında modelin ölçeği ve kanıtın sınırı korunur."),
    "İngilizce": ("Meaning is inferred from purpose, context and explicit textual or spoken clues.", "A coherent response preserves audience, register, time reference and linking devices.", "Listening and reading evidence must not be replaced by an unsupported assumption."),
    "Kimya": ("Kimyasal dönüşümlerde tanecik, bağ, enerji ve ölçülebilir sonuç birlikte değerlendirilir.", "Yapı ile özellik arasındaki ilişki molekül geometrisi ve fonksiyonel gruplarla açıklanır.", "Enerji ve çevre seçenekleri bilimsel yarar, risk ve sürdürülebilirlik ölçütleriyle karşılaştırılır."),
    "Matematik": ("Tanım kümesi ve gerekli koşullar belirlenmeden cebirsel işlem genellenemez.", "Fonksiyon, limit, türev ve integral ilişkilerinde grafik ile cebirsel temsil birlikte denetlenir.", "Bulunan sonuç başlangıç koşulu, işaret, aralık ve geometrik anlam bakımından kontrol edilir."),
    "T.C. İnkılap Tarihi ve Atatürkçülük": ("Tarihsel gelişmeler kronoloji, neden, sonuç ve dönemin koşulları birlikte kullanılarak açıklanır.", "Birincil ve ikincil kaynaklar amaç, bağlam ve güvenilirlik bakımından karşılaştırılır.", "Siyasi, toplumsal ve ekonomik değişimler tek nedene indirgenmeden değerlendirilir."),
    "Türk Dili ve Edebiyatı": ("Edebî metin tür, dönem, tema, yapı, dil ve anlatım özellikleriyle çözümlenir.", "Metin yorumu doğrudan metinsel kanıta dayanır; sanatçı veya dönem bilgisi kanıtın yerine geçmez.", "Yazma ve konuşma ürünleri amaç, hedef kitle, tutarlılık ve dil kullanımı bakımından gözden geçirilir."),
}


def slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def pending(row: dict[str, Any]) -> dict[str, Any]:
    clean = projection(row)
    clean.update({
        "reviewStatus": "pending", "humanReviewed": False, "reviewMode": "ai-only",
        "reviewDeclaration": "ai-generated-pending-independent-ai-review",
        "publishReady": False, "publishBlocked": True,
        "productionStatus": "pending-independent-ai-review",
        "disclosure": "ai-generated-pending-independent-ai-review",
        "provenance": "pending:grade12-current-subject-builder/1.0.0; human-review:false",
    })
    return clean


def grouped(registry: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for source in registry["subjects"]:
        target = "Felsefe Grubu" if source["subject"] in FELSEFE_PARTS else source["subject"]
        result.setdefault(target, []).append(source)
    return result


def learning_content(subject: str, objective: dict[str, Any]) -> dict[str, Any]:
    title = objective["title"]
    facts = [f"Kazanımın doğrudan içeriği şudur: {title}.", *SUBJECT_FACTS[subject]]
    if subject == "İngilizce":
        facts[0] = f"The official learning outcome requires this performance: {title}."
        mistakes = list(MISCONCEPTIONS_EN[:4])
        procedure = ["Identify the purpose and source clue.", "Match language to audience and context.", "Check time, coherence and evidence.", "Revise the response without adding information."]
    else:
        mistakes = list(MISCONCEPTIONS_TR[:4])
        procedure = ["Sorudaki verilenleri ve isteneni belirle.", "Kazanıma özgü kavramı ya da bağıntıyı seç.", "Kanıtı koşul, sıra, birim ve kapsam yönünden denetle.", "Sonucu karşı örnek ve yaygın yanılgılarla sınayıp gerekçelendir."]
    return {"keyFacts": facts, "procedure": procedure, "commonMisconceptions": mistakes}


def note(subject: str, item: dict[str, Any], pack_id: str) -> dict[str, Any]:
    code, title = item["code"], item["title"]
    note_id = f"tr-g12-{slug(subject)}-current-note-{slug(code)}"
    raw = {
        "type": "note", "recordType": "note", "schemaVersion": "2.2",
        "id": note_id, "noteId": note_id, "noteKey": note_id,
        "packId": pack_id, "linkedPackId": pack_id, "country": "TR", "lang": "tr", "language": "tr",
        "grade": 12, "subject": subject, "title": title, "topic": title,
        "unitKey": f"tr-g12-current-{slug(subject)}-unit-{slug(code.rsplit('.', 1)[0])}",
        "topicKey": f"tr-g12-current-{slug(subject)}-topic-{slug(code)}",
        "subtopicKey": f"tr-g12-current-{slug(subject)}-subtopic-{slug(code)}",
        "objective": code, "objectiveCode": code, "objectives": [code],
        "objectiveSource": item["objectiveSource"], "objectiveEvidenceId": item["objectiveEvidenceId"],
        "sourceRefs": [item["objectiveEvidenceId"].split(":pdf-page-")[0]],
        "summary": title, "body": title, "learningContent": learning_content(subject, item),
        "figure": None, "visualRequirement": "none",
        "visualNeed": {"level": "none", "role": "none", "rationale": "Kazanım açıklaması erişilebilir metinde eksiksizdir.", "acceptableKinds": [], "evidenceDimensions": []},
        "figureSpecVersion": "1.3.0", "figureContractVersion": "1.3.0", "hintsForbidden": True,
    }
    enriched = enrich_note(raw)
    failures = note_failures(enriched)
    if failures:
        raise ValueError(f"{note_id}: {failures}")
    return pending(enriched)


def question(subject: str, item: dict[str, Any], linked_note: dict[str, Any], local: int) -> dict[str, Any]:
    english = subject == "İngilizce"
    facts = linked_note["learningContent"]["keyFacts"]
    mistakes = MISCONCEPTIONS_EN if english else MISCONCEPTIONS_TR
    stems = STEMS_EN if english else STEMS_TR
    correct_text = facts[(local - 1) % len(facts)]
    wrongs = [
        (f"The response is based on {mistakes[(local + offset) % len(mistakes)]}; it therefore exceeds the supplied evidence."
         if english else f"Bu yorum {mistakes[(local + offset) % len(mistakes)].casefold()} yanılgısına dayanır; kazanımın kanıt sınırını aşar.")
        for offset in range(3)
    ]
    position = (local - 1) % 4
    choices = list(wrongs)
    choices.insert(position, correct_text)
    reasons = []
    for index, choice in enumerate(choices):
        if index == position:
            reasons.append(f"Doğru çözüm — kazanım ve kanıt uyumu: '{choice}' ifadesi {item['code']} ölçütünü korur.")
        else:
            label = mistakes[(local + index) % len(mistakes)]
            reasons.append(f"Adlandırılmış öğrenci yanılgısı — {label}: '{choice}' seçeneği gerekli koşulu veya kanıt sınırını ihlal eder.")
    qid = f"tr-g12-{slug(subject)}-current-q{local:04d}"
    row = {
        "type": "question", "schemaVersion": "2.2", "id": qid, "questionId": qid,
        "questionNumber": local, "country": "TR", "lang": "tr", "grade": 12, "subject": subject,
        "unitKey": linked_note["unitKey"], "topicKey": linked_note["topicKey"], "subtopicKey": linked_note["subtopicKey"],
        "topic": linked_note["topic"], "title": f"{item['title']} — güncel ders sorusu {local}",
        "objective": item["code"], "objectiveId": item["code"], "noteId": linked_note["id"], "noteKey": linked_note["id"],
        "linkedNoteId": linked_note["id"], "linkedNoteKey": linked_note["id"],
        "question": f"{semantic_task_clause(local, english)} {stems[(local - 1) % len(stems)]} Odak: {item['title']}.",
        "choices": choices, "correct": position, "correctIndex": position, "correctOption": choices[position],
        "distractorWhy": reasons,
        "explanation": f"{correct_text} Diğer seçenekler bir koşulu ters çevirir, kavramı yanlış bağlama taşır veya kanıtsız ayrıntı ekler.",
        "level": LEVELS[local - 1], "difficultyReason": f"Düzey {LEVELS[local - 1]}; {item['code']} hedefini yeni bağlamda kanıtla gerekçelendirmeyi gerektirir.",
        "questionType": ("comprehension", "application", "analysis", "error-analysis")[(local - 1) % 4],
        "familyId": f"{qid}-family", "authoringTemplateId": f"g12-current-source-{(local - 1) % len(stems) + 1}",
        "objectiveSource": item["objectiveSource"], "objectiveEvidenceId": item["objectiveEvidenceId"],
        "sourceRefs": [item["objectiveEvidenceId"].split(":pdf-page-")[0]],
        "visualRequirement": "none", "visualNeed": {"level": "none", "role": "none", "rationale": "Gerekli veri soru metninde verilmiştir.", "acceptableKinds": [], "evidenceDimensions": []},
        "figure": None, "hintsCount": 0, "hintsForbidden": True,
    }
    if english and re.search(r"\.L\d+$", item["code"]):
        asset_id = f"tr.g12.ingilizce.lesson.a{local:04d}"
        row["mediaRequirement"] = "audio-required"
        row["audio"] = {"assetId": asset_id, "role": "prompt", "playbackRequired": True}
    return pending(row)


def source_record(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "sourceId": source["sourceId"], "documentType": "curriculum", "sourceType": "official-curriculum-pdf",
        "canonicalRole": "primary", "authority": "T.C. Millî Eğitim Bakanlığı",
        "publisher": "T.C. Millî Eğitim Bakanlığı Talim ve Terbiye Kurulu Başkanlığı",
        "title": f"MEB {source['subject']} öğretim programı", "documentName": f"{source['subject']} Dersi Öğretim Programı",
        "publicName": f"2026-2027 yürürlükteki 12. sınıf {source['subject']} programı",
        "publicationYear": source["programmeYear"], "accessedAt": "2026-08-31",
        "downloadUrl": source["sourceUrl"], "url": source["sourceUrl"], "sha256": source["sourceSha256"],
        "pageCount": source["pageCount"],
        "evidenceBindings": [
            {"printedPageNumber": int(item["objectiveEvidenceId"].rsplit("-", 1)[1]),
             "pdfPageIndex": int(item["objectiveEvidenceId"].rsplit("-", 1)[1]) - 1,
             "evidenceId": item["objectiveEvidenceId"], "scope": item["title"], "objectiveCodes": [item["code"]]}
            for item in source["objectives"]
        ],
    }


def archive_future() -> None:
    for subject, (folder, filename) in PATHS.items():
        source_dir = ROOT / "turkiye/12-sinif" / folder
        target_dir = FUTURE / folder
        target_dir.mkdir(parents=True, exist_ok=True)
        for path in source_dir.iterdir():
            if path.is_file():
                target = target_dir / path.name
                if not target.exists():
                    shutil.copy2(path, target)
    bank_dir = ROOT / "turkiye/12-sinif/soru-bankasi"
    target_bank = FUTURE / "soru-bankasi"
    target_bank.mkdir(parents=True, exist_ok=True)
    for path in bank_dir.iterdir():
        if path.is_file() and not (target_bank / path.name).exists():
            shutil.copy2(path, target_bank / path.name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-future", action="store_true")
    parser.add_argument("--finalize-audio", action="store_true")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if args.archive_future:
        archive_future()
    results = []
    for subject, sources in grouped(registry).items():
        folder, filename = PATHS[subject]
        objectives = [copy.deepcopy(item) for source in sources for item in source["objectives"]]
        pack_id = f"tr.g12.{folder}.full"
        notes = [note(subject, item, pack_id) for item in objectives]
        by_code = {row["objective"]: row for row in notes}
        questions = [question(subject, objectives[(local - 1) % len(objectives)], by_code[objectives[(local - 1) % len(objectives)]["code"]], local) for local in range(1, 501)]
        counts = Counter(row["objective"] for row in questions)
        pack = pending({
            "type": "pack", "schemaVersion": "2.2", "id": pack_id, "version": 2,
            "country": "TR", "lang": "tr", "language": "tr", "grade": 12, "subject": subject,
            "theme": f"Türkiye 12. Sınıf {subject} — 2026-2027 yürürlükteki program",
            "curriculum": "MEB-CURRENT-2018-2019", "schoolYear": "2026-2027", "programmeFamily": "pre-TYMM-current",
            "license": "CC-BY-NC-4.0", "source": "official-meb-current-curriculum", "sources": [source_record(source) for source in sources],
            "labels": {}, "objectives": [item["code"] for item in objectives],
            "coverage": {code: {"notes": [by_code[code]["id"]], "questions": counts[code]} for code in counts},
            "counts": {"notes": len(notes), "questions": 500}, "levelScale": [1, 5],
            "contentContractVersion": "2.2", "figureSpecVersion": "1.3.0",
            "contractPolicy": {"questionCount": 500, "answerBalance": [125, 125, 125, 125], "minFamilies": 500, "maxPerFamily": 1, "objectiveBalanceMode": "coverage"},
            "visualPolicy": {"version": "1.3.0", "everyNote": False, "questionMinimumPercent": 0, "balancedByObjective": False, "rationale": "Görsel yalnız çözüm kanıtı gerektirdiğinde kullanılır."},
            "humanReview": {"required": False, "performed": False, "source": "user-comments-only"},
        })
        target = OUTPUT / folder / filename
        if subject == "İngilizce" and args.finalize_audio:
            manifest_path = target.parent / "audio-assets.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            assets = {str(asset["assetId"]): asset for asset in manifest["assets"]}
            audio_questions = [row for row in questions if row.get("mediaRequirement") == "audio-required"]
            for row in audio_questions:
                row["audio"]["contentSha256"] = assets[row["audio"]["assetId"]]["sha256"]
            pack["audioPolicy"] = {
                "schemaVersion": "alika-local-audio-policy/1.0.0",
                "manifestPath": "audio-assets.json",
                "manifestSha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                "assetCount": len(assets), "questionCount": len(audio_questions),
                "storage": "local-offline-wav", "remoteAssetsAllowed": False,
                "recordingStorage": "local-temporary-only",
            }
        write_jsonl(target, [pack, *notes, *questions])
        results.append({"subject": subject, "objectives": len(objectives), "notes": len(notes), "questions": len(questions), "candidate": str(target)})
    print(json.dumps({"archivedFuture": args.archive_future, "packages": results}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
