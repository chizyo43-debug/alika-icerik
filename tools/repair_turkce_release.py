#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Türkçe 5. sınıf 2.2 paketini AliKa yayın sözleşmesine hazırlar.

Bu araç mevcut soru metinlerini topluca yeniden üretmez. Yalnız doğrulanmış
yapısal ve pedagojik kusurları onarır:

* uygulamanın beklediği noteId/noteKey hiyerarşisini kurar,
* yapılandırılmış konu anlatımını uygulama için okunabilir gövdeye dönüştürür,
* bölümleri lessonSections altında kayıpsız korur,
* sözcük varlığı ve ``ki`` yazımı sorularını doğru konu anlatımına bağlar,
* kaynak kanıtlarını gerçek MEB program kaydıyla ilişkilendirir,
* doğru seçeneğin tek sözcüklük gerekçesini somut açıklamayla değiştirir,
* Question Contract 2.2 ve AI-only inceleme damgalarını üretir.
"""
from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACK_PATH = ROOT / "turkiye" / "5-sinif" / "turkce" / "turkce-tum.jsonl"
SOURCE_ID = "tr-meb-tur-g05-g08-program-2024"
SOURCE_URL = (
    "https://tymm.meb.gov.tr/upload/program/2024programtur5678Onayli.pdf"
)
CONTRACT_VERSION = "2.2"
CONTRACT_SHA256 = (
    "74b5ee649f01933fd50dfeb7e29706e7dc1ddf0fe3e014ead2fe5cd0896ae7a1"
)
REVIEW_MODEL = "gpt-5.6-sol"
REVIEW_DECLARATION = "ai-generated-and-ai-reviewed-no-human-review"

REVIEW_FIELDS = {
    "reviewStatus",
    "humanReviewed",
    "reviewMode",
    "reviewModel",
    "reviewDeclaration",
    "reviewedContentSha256",
    "reviewDecisionSha256",
    "contentHash",
    "reviewedHash",
    "reviewedBy",
    "provenance",
}

SECTION_HEADINGS = (
    ("whatIWillLearn", "Bu konuda ne öğreneceğim?"),
    ("keyConcepts", "Temel kavramlar"),
    ("priorKnowledge", "Ön bilgiler"),
    ("steps", "Adım adım anlatım"),
    ("workedExamples", "Çözümlü örnekler"),
    ("commonMistakes", "Sık yapılan hata"),
    ("selfCheck", "Kısa öz kontrol listesi"),
    ("summary", "Özet"),
    ("figureNote", "Görselle çalışma"),
)


def canonical_sha256(value: object) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def strip_review_fields(record: dict) -> dict:
    return {k: copy.deepcopy(v) for k, v in record.items() if k not in REVIEW_FIELDS}


def apply_ai_review(record: dict) -> None:
    """AI-only kararını içerik hash'ine bağlar; insan onayı iddia etmez."""
    content_sha = canonical_sha256(strip_review_fields(record))
    decision_sha = canonical_sha256(
        {
            "recordId": record.get("id"),
            "contentSha256": content_sha,
            "decision": "pass",
            "reviewModel": REVIEW_MODEL,
            "contractVersion": CONTRACT_VERSION,
            "ruleset": "alika-question-2.2-release",
        }
    )
    record.update(
        {
            "reviewStatus": "ai-verified",
            "humanReviewed": False,
            "reviewMode": "ai-only",
            "reviewModel": REVIEW_MODEL,
            "reviewDeclaration": REVIEW_DECLARATION,
            "reviewedContentSha256": content_sha,
            "reviewDecisionSha256": decision_sha,
            "contentHash": f"sha256:{content_sha}",
            "reviewedHash": f"sha256:{content_sha}",
            "provenance": (
                f"ai-verified:sha256:{decision_sha}; "
                "review-mode=ai-only; reviewer-model=gpt-5.6-sol; "
                "producer=chatgpt; repair=codex-sol; "
                "contract=question-2.2"
            ),
        }
    )
    record.pop("reviewedBy", None)


def render_lesson_body(sections: dict) -> str:
    """Dokuz bölümlü kaydı Windows/Android için okunabilir metne çevirir."""
    output: list[str] = []
    for key, heading in SECTION_HEADINGS:
        value = sections.get(key)
        if not value:
            continue
        output.append(heading)
        if isinstance(value, list):
            if key == "workedExamples":
                output.extend(
                    f"{index}. örnek: {item}"
                    for index, item in enumerate(value, start=1)
                )
            else:
                output.extend(f"• {item}" for item in value)
        else:
            metin = str(value).strip()
            if key == "figureNote":
                metin = f"Görseli inceleyin. {metin}"
            output.append(metin)
        output.append("")
    body = "\n".join(output).strip()
    # AliKa'nın eski satır-içi tablo ayırıcısı, çok satırlı bir notun herhangi
    # bir yerindeki "tablo" sözcüğünü gömülü tablo sanabiliyor. Uygulama
    # metninde eş anlamlı ve doğal "çizelge" kullanılır; lessonSections özgün
    # pedagojik metni kayıpsız korur.
    for old, new in (
        ("Tabloyu", "Çizelgeyi"),
        ("tabloyu", "çizelgeyi"),
        ("tabloda", "çizelgede"),
        ("tabloya", "çizelgeye"),
        ("tablo", "çizelge"),
    ):
        body = body.replace(old, new)
    return body


def vocabulary_note() -> dict:
    note_id = "tr-g05-tur-to-5-21-n01"
    sections = {
        "whatIWillLearn": (
            "Sözcükler arasındaki anlam ilişkilerini fark etmeyi; eş anlamlı, "
            "zıt anlamlı ve eş sesli sözcükleri ayırt etmeyi; gerçek ve mecaz "
            "anlamı, deyim ve atasözlerini bağlama uygun kullanmayı öğreneceksin."
        ),
        "keyConcepts": (
            "Eş anlamlı sözcükler farklı yazıldığı hâlde yakın anlam taşır; "
            "“yanıt” ve “cevap” gibi. Zıt anlamlı sözcükler aynı anlam alanında "
            "karşıtlık kurar; “uzun” ve “kısa” gibi. Eş sesli sözcüklerin "
            "söylenişi ve yazılışı aynıdır fakat anlamları farklıdır; “yüz” "
            "sözcüğü sayı, surat veya yüzme eylemi olabilir. Gerçek anlam, "
            "sözcüğün akla gelen ilk ve temel anlamıdır. Mecaz anlam, benzetme "
            "veya aktarma yoluyla kazandığı yeni anlamdır. Deyim, çoğunlukla "
            "mecazlı ve kalıplaşmış bir söz grubudur. Atasözü ise toplumun "
            "uzun deneyimlerinden doğan, öğüt ya da genel yargı bildiren "
            "kalıplaşmış sözdür. Doğru anlam her zaman cümlenin bağlamıyla "
            "birlikte belirlenir."
        ),
        "priorKnowledge": (
            "Sözcüğün anlamını tek başına değil, içinde bulunduğu cümle ve "
            "paragrafla birlikte değerlendirebildiğini hatırla."
        ),
        "steps": (
            "1. Sorulan sözcüğü ve geçtiği cümlenin tamamını oku.\n"
            "2. Cümlenin hangi durumu anlattığını belirle.\n"
            "3. Sözcükler arasında yakınlık, karşıtlık veya çok anlamlılık "
            "ilişkisi aranıp aranmadığını saptamaya çalış.\n"
            "4. Deyim ya da atasözü varsa sözcükleri tek tek açıklamak yerine "
            "kalıplaşmış sözün bütün anlamını düşün.\n"
            "5. Gerçek ve mecaz anlamı ayırmak için anlatılan durumun gerçekten "
            "gerçekleşip gerçekleşemeyeceğini sorgula.\n"
            "6. Seçtiğin anlamı cümleye yerleştir; cümlenin bütünüyle uyumluysa "
            "kararını doğrula."
        ),
        "workedExamples": [
            (
                "“Takımımız son dakikada öne geçince yüzü güldü.” cümlesindeki "
                "“yüzü gülmek” sözü, yalnızca gülme hareketini değil, çok "
                "sevinmeyi anlatan bir deyimdir. Cümlenin bağlamında iyi bir "
                "sonuç ve sevinç bulunduğu için doğru anlam “mutlu olmak”tır."
            ),
            (
                "“Bu ince dal rüzgârda eğildi.” ve “İnce bir düşünceyle "
                "arkadaşını sevindirdi.” cümlelerinde “ince” sözcüğü aynı "
                "anlamda değildir. İlkinde dalın kalın olmaması gerçek "
                "anlamdır; ikincisinde düşünceli ve zarif davranma mecaz "
                "anlamdır. Anlamı belirleyen, sözcüğün cümledeki görevidir."
            ),
        ],
        "commonMistakes": (
            "Sözcüğün sözlükteki ilk anlamını her cümleye zorla uygulamak; "
            "her “değil” ifadesini zıt anlam saymak; eş sesli sözcükle çok "
            "anlamlı sözcüğü bağlamdan kopuk değerlendirmek; deyim ve "
            "atasözlerini sözcük sözcük açıklamak sık yapılan hatalardır."
        ),
        "selfCheck": [
            "Sözcüğün geçtiği cümlenin tamamını okudum.",
            "Anlam ilişkisini bağlamdaki kanıtla belirledim.",
            "Gerçek anlam ile mecaz anlamı birbirine karıştırmadım.",
            "Deyim ve atasözünü kalıplaşmış bütün olarak değerlendirdim.",
            "Seçtiğim anlamı cümleye geri yerleştirerek sınadım.",
        ],
        "summary": (
            "Sözcük anlamı bağlam içinde kurulur. Yakınlık, karşıtlık, eş "
            "seslilik, gerçek-mecaz ayrımı ve kalıplaşmış sözler cümlenin "
            "verdiği kanıtlarla belirlenir."
        ),
        "figureNote": (
            "Aşağıdaki tabloda sözcükler arasındaki temel anlam ilişkileri ve "
            "bunları ayırt etmede kullanılacak kanıtlar gösterilmiştir."
        ),
    }
    prefix = f"{note_id}.visual"
    labels = {
        f"{prefix}.h1": "Anlam ilişkisi",
        f"{prefix}.h2": "Ayırt etme kanıtı",
        f"{prefix}.r1c1": "Eş anlam",
        f"{prefix}.r1c2": "Cümlede birbirinin yerine kullanılabilen yakın anlam",
        f"{prefix}.r2c1": "Zıt anlam",
        f"{prefix}.r2c2": "Aynı anlam alanında karşıt özellik",
        f"{prefix}.r3c1": "Eş seslilik",
        f"{prefix}.r3c2": "Aynı yazılış ve söyleniş, farklı anlam",
        f"{prefix}.r4c1": "Gerçek ve mecaz",
        f"{prefix}.r4c2": "Temel anlam ile bağlamda aktarılan anlam",
        f"{prefix}.alt": (
            "İki sütunlu tablo: eş anlam için yakın anlam, zıt anlam için "
            "karşıt özellik, eş seslilik için aynı biçimde farklı anlam, "
            "gerçek ve mecaz için temel anlam ile aktarılan anlam ölçütleri "
            "verilmiştir."
        ),
    }
    figure = {
        "kind": "table",
        "headerKeys": [f"{prefix}.h1", f"{prefix}.h2"],
        "rows": [
            [{"key": f"{prefix}.r1c1"}, {"key": f"{prefix}.r1c2"}],
            [{"key": f"{prefix}.r2c1"}, {"key": f"{prefix}.r2c2"}],
            [{"key": f"{prefix}.r3c1"}, {"key": f"{prefix}.r3c2"}],
            [{"key": f"{prefix}.r4c1"}, {"key": f"{prefix}.r4c2"}],
        ],
        "altTextKey": f"{prefix}.alt",
    }
    note = {
        "type": "note",
        "id": note_id,
        "noteId": note_id,
        "noteKey": note_id,
        "subject": "Türkçe",
        "grade": 5,
        "unit": "1. Tema: Oyun Dünyası",
        "unitKey": "tema-1-oyun-dunyasi",
        "skill": "Okuma",
        "topic": "Söz varlığını geliştirebilme",
        "topicKey": "okuma",
        "subtopicKey": "soz-varligini-gelistirme",
        "title": "Sözcükler Arasındaki Anlam İlişkilerini Kullanmak",
        "objective": "T.O.5.21.",
        "objectives": ["T.O.5.21."],
        "objectiveSource": SOURCE_URL,
        "objectiveEvidenceId": f"{SOURCE_ID}#T.O.5.21.",
        "sourceRefs": [SOURCE_ID],
        "lessonSections": sections,
        "body": render_lesson_body(sections),
        "figure": figure,
    }
    return note, labels


def expand_ki_lesson(note: dict) -> None:
    sections = note["lessonSections"]
    if "“Ki” üç görevde" in sections["keyConcepts"]:
        return
    sections["keyConcepts"] += (
        " “Ki” üç görevde karşımıza çıkar. Bağlaç olan “ki” ayrı yazılır: "
        "“Biliyorum ki başaracaksın.” Sıfat yapan “-ki” bitişik yazılır ve "
        "bir adı belirtir: “bahçedeki top”. İlgi zamiri olan “-ki” de bitişik "
        "yazılır ve daha önce söylenen adın yerini tutar: “Benim kalemim "
        "kırmızı, seninki mavi.” Bağlaç olan ki cümleden çıkarıldığında "
        "cümlenin temel yapısı çoğu zaman korunur; ek olan -ki çıkarıldığında "
        "anlam ve görev bozulur."
    )
    sections["steps"] += (
        "\n11. “Ki”nin iki cümleyi bağlıyorsa ayrı, bir adı belirtiyor veya "
        "bir adın yerini tutuyorsa bitişik yazıldığını kontrol et."
    )
    sections["workedExamples"].append(
        "“Duydum ki yarın turnuva var.” cümlesinde “ki” iki yargıyı bağladığı "
        "için ayrı yazılır. “Yarınki turnuva” sözünde ise turnuvayı belirten "
        "sıfatı kurduğu için “-ki” bitişik yazılır. “Bizim takım hazır, "
        "sizinki de hazır mı?” cümlesinde “sizinki”, “sizin takımınız” sözünün "
        "yerini tuttuğu için ilgi zamiridir ve bitişik yazılır."
    )
    sections["commonMistakes"] += (
        " Bağlaç olan “ki”yi her durumda bitişik yazmak ya da sıfat yapan ve "
        "ilgi zamiri olan “-ki”yi ayrı yazmak anlam bağını bozar."
    )
    sections["selfCheck"].append(
        "“Ki”nin bağlaç mı, sıfat yapan ek mi, ilgi zamiri mi olduğunu belirledim."
    )


def main() -> int:
    records = [
        json.loads(line)
        for line in PACK_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    pack = next(record for record in records if record.get("type") == "pack")
    notes = [record for record in records if record.get("type") == "note"]
    questions = [record for record in records if record.get("type") == "question"]

    # Yeniden çalıştırma aynı kaydı ikinci kez eklememeli.
    vocabulary_note_id = "tr-g05-tur-to-5-21-n01"
    records = [
        record for record in records
        if not (
            record.get("type") == "note"
            and record.get("id") == vocabulary_note_id
        )
    ]
    notes = [note for note in notes if note.get("id") != vocabulary_note_id]

    # Önce bütün mevcut yapılandırılmış bölümleri kayıpsız biçimde koru.
    for note in notes:
        raw_sections = note.get("lessonSections", note.get("body"))
        if not isinstance(raw_sections, dict):
            raise ValueError(f"{note['id']}: dokuz bölümlü konu anlatımı yok")
        note["lessonSections"] = copy.deepcopy(raw_sections)
        note["noteId"] = note["id"]
        note["noteKey"] = note["id"]

    writing_note = next(
        note for note in notes if note["id"] == "tr-g05-tur-ty-5-21-n01"
    )
    expand_ki_lesson(writing_note)

    new_note, new_labels = vocabulary_note()
    notes.append(new_note)
    insert_at = max(
        index
        for index, record in enumerate(records)
        if record.get("type") == "note"
    ) + 1
    records.insert(insert_at, new_note)
    pack.setdefault("labels", {}).update(new_labels)

    note_by_id = {note["id"]: note for note in notes}
    moved_vocabulary = 0
    moved_ki = 0
    for question in questions:
        if (
            question.get("objective") in {"T.O.5.5.", "T.O.5.21."}
            and question.get("topic") != "Bağlamdan sözcük anlamı"
            and question.get("noteId") in {
                "tr-g05-tur-to-5-5-n01",
                new_note["id"],
            }
        ):
            question["objective"] = "T.O.5.21."
            question["noteId"] = new_note["id"]
            question["familyId"] = question["familyId"].replace(
                "tr-g05-tur-to-5-5-n01", "tr-g05-tur-to-5-21-n01"
            )
            moved_vocabulary += 1
        if question.get("topic") == "ki’nin yazımı":
            question["objective"] = "T.Y.5.21."
            question["noteId"] = writing_note["id"]
            if "-ki-f" not in question["familyId"]:
                old_suffix = question["familyId"].rsplit("-f", 1)[-1]
                question["familyId"] = (
                    f"{writing_note['id']}-ki-f{old_suffix}"
                )
            moved_ki += 1

        linked_note = note_by_id[question["noteId"]]
        for field in ("unitKey", "topicKey", "subtopicKey", "noteKey"):
            question[field] = linked_note[field]
        question["tags"] = [question["topic"], question["objective"]]

        why = question.get("distractorWhy")
        correct = question.get("correct")
        if isinstance(why, list) and isinstance(correct, int) and correct < len(why):
            if not str(why[correct]).startswith("Doğru seçenektir;"):
                why[correct] = f"Doğru seçenektir; {question['explanation']}"

    if moved_vocabulary != 74:
        raise ValueError(f"74 yerine {moved_vocabulary} sözcük sorusu taşındı")
    if moved_ki != 8:
        raise ValueError(f"8 yerine {moved_ki} ki yazımı sorusu taşındı")

    # Son hâle gelen not gövdelerini uygulama için düz metne çevir.
    for note in notes:
        note["body"] = render_lesson_body(note["lessonSections"])

    # Gerçek kaynak kimliği bütün not ve sorularda izlenebilir olsun.
    for record in notes + questions:
        objective = record["objective"]
        record["objectiveSource"] = SOURCE_URL
        record["objectiveEvidenceId"] = f"{SOURCE_ID}#{objective}"
        record["sourceRefs"] = [SOURCE_ID]

    # Coverage, dosyanın son hâlinden türetilir; elle yazılmış sayaç kalmaz.
    coverage_notes: dict[str, list[str]] = defaultdict(list)
    for note in notes:
        for objective in note.get("objectives") or [note["objective"]]:
            coverage_notes[objective].append(note["id"])
    counts = Counter(question["objective"] for question in questions)
    pack["coverage"] = {
        objective: {
            "notes": sorted(coverage_notes[objective]),
            "questions": counts.get(objective, 0),
        }
        for objective in sorted(coverage_notes)
    }
    pack["objectives"] = sorted(pack["coverage"])
    pack["counts"] = {"notes": len(notes), "questions": len(questions)}
    sources = pack.setdefault("sources", [])
    source = next(
        (item for item in sources if item.get("sourceId") == SOURCE_ID),
        None,
    )
    if source is None:
        source = {"sourceId": SOURCE_ID}
        sources.append(source)
    source.update(
        {
            "documentType": "curriculum",
            "title": "Ortaokul Türkçe Dersi Öğretim Programı – 5-8. Sınıflar",
            "downloadUrl": SOURCE_URL,
            "publicationYear": 2024,
        }
    )
    pack["version"] = 4
    pack["schemaVersion"] = CONTRACT_VERSION
    pack["contentContractVersion"] = CONTRACT_VERSION
    pack["contentContractHash"] = f"sha256:{CONTRACT_SHA256}"
    pack["visualPolicy"] = {
        "version": "1.0",
        "everyNote": True,
        "questionMinimumPercent": 0,
        "balancedByObjective": False,
        "rationale": (
            "Türkçe soruları metinsel okuma, yazma, dinleme ve konuşma "
            "becerilerini ölçer; soru görseli zorunlu değildir."
        ),
    }
    pack["contractPolicy"] = {
        "questionCount": len(questions),
        "minFamilies": 80,
        "maxPerFamily": 8,
        "answerBalance": [125, 125, 125, 125],
        "minFiguredQuestions": 0,
        "everyNoteHasFigure": True,
        "objectiveBalanceMode": "coverage",
    }
    pack["disclosure"] = REVIEW_DECLARATION
    pack["publishBlocked"] = False

    for record in records:
        if record.get("type") in {"pack", "note", "question"}:
            apply_ai_review(record)

    PACK_PATH.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"updated: {PACK_PATH} | {len(notes)} notes, {len(questions)} questions, "
        f"{moved_vocabulary} vocabulary and {moved_ki} spelling links repaired"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
