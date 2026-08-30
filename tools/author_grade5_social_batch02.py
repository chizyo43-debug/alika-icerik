#!/usr/bin/env python3
"""Author 100 paired Grade 5 social studies questions (grade rows 1301-1400)."""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from typing import Any

import author_grade5_social_segment01 as base


MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
LEVELS = (
    [1] * 15 + [2] * 10 +
    [1] * 5 + [2] * 15 + [3] * 15 +
    [3] * 10 + [4] * 10 + [5] * 5 +
    [3] * 5 + [4] * 10
)
NOTE_IDS = [
    "tr-g05-sosyal-sb-5-1-1-note", "tr-g05-sosyal-sb-5-1-2-note", "tr-g05-sosyal-sb-5-1-3-note",
    "tr-g05-sosyal-sb-5-2-1-note", "tr-g05-sosyal-sb-5-2-2-note", "tr-g05-sosyal-sb-5-2-3-note",
    "tr-g05-sosyal-sb-5-2-4-note", "tr-g05-sosyal-sb-5-3-1-note", "tr-g05-sosyal-sb-5-3-2-note",
    "tr-g05-sosyal-sb-5-3-3-note", "tr-g05-sosyal-sb-5-4-1-note", "tr-g05-sosyal-sb-5-4-2-note",
    "tr-g05-sosyal-sb-5-4-3-note", "tr-g05-sosyal-sb-5-4-4-note", "tr-g05-sosyal-sb-5-5-1-note",
    "tr-g05-sosyal-sb-5-5-2-note", "tr-g05-sosyal-sb-5-5-3-note", "tr-g05-sosyal-sb-5-6-1-note",
    "tr-g05-sosyal-sb-5-6-2-note",
]
EXTRA_CASES = [
    (
        "Mahalledeki kırık sokak lambası için öğrenci doğrudan hastaneye başvurmayı planlıyor. Sorun ile kurum eşleştirmesi denetleniyor.",
        "Yetki alanına göre başvuru: Sokak aydınlatması belediyenin veya ilgili elektrik dağıtım biriminin bildirim kanalına iletilmelidir.",
        ["Sağlık hizmetiyle karıştırma: Hastanenin sokak lambasını onarmasını isteme", "Kurum kullanmama: Tehlikeyi bildirmeden yalnız arkadaşlarla konuşma", "Yetkisiz müdahale: Elektrik tesisatını uzman olmadan açıp onarma"],
        "Sorunlarda kurumun görev alanı araştırılır; kamusal aydınlatma için yerel yönetim veya yetkili dağıtım birimine güvenli ve kanıta dayalı bildirim yapılır.",
    ),
    (
        "Okulda açık bırakılan musluklar ve tek yüzü kullanılıp atılan kâğıtlar gözleniyor. Bir öğrenci kaynakların sınırsız olduğunu savunuyor.",
        "Sürdürülebilir kullanım planı: Kaçaklar bildirilmeli, musluklar kapatılmalı, kâğıdın iki yüzü kullanılmalı ve tüketim düzenli izlenmelidir.",
        ["Tüketimi görünmez sayma: Kaynakların yenilendiği için hiç tükenmeyeceğini savunma", "Sorunu başka yere taşıma: Tasarrufu yalnız evde gerekli sayma", "Tek kullanımı artırma: Daha çok tüketimin kaynakları koruduğunu ileri sürme"],
        "Kaynakların verimli kullanımı ihtiyacı karşılamayı sürdürürken israfı azaltır; ölçme, önleme, yeniden kullanma ve ortak sorumluluk birlikte uygulanır.",
    ),
    (
        "Aylık 2 400 TL bütçesi olan aile önce 1 500 TL kira, 500 TL gıda ve 250 TL ulaşımı planlıyor; öğrenci kalan para hesaplanmadan pahalı bir oyun almak istiyor.",
        "İhtiyaç öncelikli bütçe: Zorunlu giderler 2 250 TL'dir; kalan 150 TL görülmeden isteğe yönelik harcama kararı verilmemelidir.",
        ["İstekleri ihtiyaç sayma: Oyunu kiradan önce bütçeye yerleştirme", "Geliri yok sayma: Bütün ürünleri borçla almayı bütçe planı kabul etme", "Giderleri ayrı tutmama: Kalanı hesaplamadan tek bir fiyatı yeterli sayma"],
        "Bütçede gelir ve zorunlu giderler listelenir, ihtiyaçlar öncelenir ve kalan tutar hesaplanır; istekler ancak kaynak yeterliyse değerlendirilir.",
    ),
    (
        "Bir ilde verimli ova, sulama ağı ve gıda işleme tesisi bulunuyor. Öğrenci ekonomik faaliyeti yalnız ilin nüfusuna bakarak belirliyor.",
        "Kanıtları birlikte kullanma: Ova ve sulama tarımsal üretimi, işleme tesisi de tarıma bağlı sanayiyi destekleyen göstergelerdir.",
        ["Tek ölçüte indirgeme: Nüfusu tek başına ekonomik faaliyet kabul etme", "Doğal koşulu yok sayma: Toprak ve suyun üretimle ilgisiz olduğunu savunma", "Her ile genelleme: Bütün illerde aynı ürün ve faaliyetin zorunlu olduğunu söyleme"],
        "Ekonomik faaliyetler doğal kaynak, iklim, yer şekli, ulaşım, iş gücü ve pazar gibi birden çok etkene göre kanıtlarla açıklanır.",
    ),
    (
        "Çevrim içi sağlık randevusu zaman kazandırıyor; fakat bağlantısı olmayan kişiler hizmete erişmekte zorlanıyor. Öğrenci teknolojinin yalnız olumlu etkisi olduğunu söylüyor.",
        "Çok yönlü etki değerlendirmesi: Teknoloji erişimi hızlandırabilir; dijital eşitsizlik, güvenlik ve erişilebilirlik sorunları için de önlem gerekir.",
        ["Tek yönlü iyimserlik: Her kullanıcının aynı cihaza ve bağlantıya sahip olduğunu varsayma", "Tek yönlü kötümserlik: Yararı görmeden teknolojiyi bütünüyle reddetme", "Neden-sonuç karışıklığı: Erişim sorununu sağlık hizmetinin gereksiz olduğuna kanıt sayma"],
        "Teknolojik gelişmelerin toplum hayatındaki etkileri yarar, risk ve farklı grupların erişim koşulları birlikte ele alınarak değerlendirilir.",
    ),
    (
        "Öğrenci bilinmeyen bir oyun bağlantısına kişisel bilgilerini yazıyor ve uzun süre ara vermeden ekran kullanıyor. Bilinçli kullanım planı aranıyor.",
        "Güvenli ve dengeli kullanım: Bağlantı doğrulanmalı, kişisel bilgi paylaşılmamalı, güçlü parola kullanılmalı ve ekran süresinde düzenli ara verilmelidir.",
        ["Kaynağı sorgulamama: Her bağlantıyı güvenli kabul edip bilgi paylaşma", "Parola güvenliğini bozma: Aynı kolay parolayı herkese söyleme", "Sağlığı yok sayma: Duruş, süre ve uyku üzerindeki etkileri önemsiz sayma"],
        "Bilinçli teknoloji kullanımı bilgi güvenliği, kaynak doğrulama, zaman yönetimi, ergonomi ve çevrim içi davranış sorumluluğunu birlikte içerir.",
    ),
]
CONTEXTS = [
    "sınıf meclisi dosyası", "yerel çevre incelemesi", "tarihsel kanıt atölyesi",
    "vatandaşlık uygulaması", "kaynak ve bütçe günlüğü", "teknoloji etki panosu",
    "toplumsal karar kartı", "araştırma sonuç çizelgesi",
]


def case_data(index: int) -> tuple[str, str, list[str], str]:
    if index < 13:
        _, statement, correct, wrongs, explanation = base.ITEMS[index]
        return statement, correct, list(wrongs), explanation
    return EXTRA_CASES[index - 13]


def pair_set() -> list[tuple[int, int]]:
    values = sorted(
        combinations(range(len(NOTE_IDS)), 2),
        key=lambda value: sha256(("-".join(map(str, value)) + "-alika-social-b02").encode()).hexdigest(),
    )[:100]
    if len(values) != 100 or len(set(values)) != 100:
        raise RuntimeError("100 unique social studies pairs could not be scheduled")
    return values


def table(qid: str, titles: list[str], cases: list[tuple[str, str, list[str], str]], labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, h3, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.h3", f"{prefix}.alt"
    labels[h1], labels[h2], labels[h3] = "Kayıt", "Konu", "İncelenen durum"
    labels[alt] = "İki sosyal bilgiler konusuna ait I ve II durum kayıtlarını gösteren tablo; doğru yorum belirtilmemiştir."
    return {
        "kind": "table", "headerKeys": [h1, h2, h3], "altTextKey": alt,
        "rows": [[{"v": label}, {"v": title}, {"v": case[0]}] for label, title, case in zip(("I", "II"), titles, cases)],
    }


def make(
    local: int,
    selected: tuple[int, int],
    note_map: dict[str, dict[str, Any]],
    labels: dict[str, str],
    *,
    global_base: int = 1300,
    batch_id: str = "b02",
) -> dict[str, Any]:
    global_number = global_base + local
    first_index, second_index = selected
    cases = [case_data(first_index), case_data(second_index)]
    notes = [note_map[NOTE_IDS[first_index]], note_map[NOTE_IDS[second_index]]]
    objectives = [str((note.get("objectives") or [""])[0]) for note in notes]
    variant = (local - 1) // 8
    correct_values = [case[1] for case in cases]
    wrong_a = cases[0][2][variant % 3]
    wrong_b = cases[1][2][(variant + 1) % 3]
    raw_choices = [
        f"I — {correct_values[0]} || II — {correct_values[1]}",
        f"I — {wrong_a} || II — {correct_values[1]}",
        f"I — {correct_values[0]} || II — {wrong_b}",
        f"I — {cases[0][2][(variant + 2) % 3]} || II — {cases[1][2][variant % 3]}",
    ]
    raw_reasons = [
        f"Doğru iki-kanıt yorumu: I için {cases[0][3]} II için {cases[1][3]}",
        f"Birinci kayıtta bağlam yanılgısı: I. yorum kanıt veya hak-sorumluluk bağını bozarken II doğrudur. {cases[0][3]}",
        f"İkinci kayıtta neden-sonuç yanılgısı: I doğru olsa da II. yorum verilen durumdan çıkarılamaz. {cases[1][3]}",
        f"Çifte genelleme yanılgısı: Her iki yorum da kendi durumunun yer, zaman, kapsam ya da kurum sınırını aşar. {cases[0][3]} {cases[1][3]}",
    ]
    correct = (global_number - 1) % 4
    choices, distractor_why = base.shared.rotate(raw_choices, raw_reasons, correct)
    mode, level = MODES[local - 1], LEVELS[local - 1]
    context = CONTEXTS[(local - 1) % len(CONTEXTS)]
    qid = f"tr-g05-bank-sos-{batch_id}-q{local:03d}"
    titles = [str(note["title"]) for note in notes]
    if mode == "comprehension":
        stem = f"Bir {context} içinde iki durum okunuyor. I: {cases[0][0]} II: {cases[1][0]} İki temel kavramı da kanıta uygun yorumlayan seçenek hangisidir?"
        fig = None
    elif mode == "application":
        stem = f"{context.capitalize()} için iki ayrı durum değerlendirilecektir. I: {cases[0][0]} II: {cases[1][0]} Her duruma uygun karar veya eylem çiftini veren seçenek hangisidir?"
        fig = None
    elif mode == "analysis":
        stem = (
            f"Aşağıdaki tabloda {titles[0].casefold()} ile {titles[1].casefold()} konularından iki durum vardır. "
            "Her kaydı kendi kanıt ve kapsamıyla çözümleyen seçenek hangisidir?"
        )
        fig = table(qid, titles, cases, labels)
    else:
        stem = f"{context.capitalize()} sırasında öğrenci I için '{wrong_a}', II için '{wrong_b}' diyor. I. durum {cases[0][0]} II. durum {cases[1][0]} İki yanılgıyı da düzelten yorum çifti hangisidir?"
        fig = None
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "İki sosyal durum ve bağlı konu başlıkları yalnız tabloda birlikte gösterilir.",
        "acceptableKinds": ["table"], "evidenceDimensions": ["kayıt", "konu", "durum kanıtı"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "İki sosyal durumun değerlendirilmesi için gereken bütün kanıtlar metinde verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    note = notes[0]
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "Sosyal Bilgiler", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — iki durum {mode}",
        "objective": objectives[0], "objectiveId": objectives[0], "integratedObjectives": objectives,
        "noteId": note.get("id"), "noteKey": note.get("id"),
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct], "distractorWhy": distractor_why,
        "explanation": f"I. kayıt için {cases[0][3]} II. kayıt için {cases[1][3]} Yorumlar kendi kanıt ve kapsamlarında doğrulanır.",
        "level": level,
        "difficultyReason": f"Düzey {level}; iki sosyal bilgiler konusundaki kanıtları {mode} biçiminde ayrı değerlendirip sonuçları tek kararda birleştirmeyi gerektirir.",
        "questionType": mode, "familyId": f"tr-g05-bank-sos-family-{global_number:03d}",
        "objectiveSource": note.get("objectiveSource"), "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [], "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    existing = [json.loads(line) for line in base.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1300:
        raise RuntimeError("the first 1300 grade questions must be regenerated before social batch 02")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    rows = [make(local, selected, note_map, labels) for local, selected in enumerate(pair_set(), 1)]
    base.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    base.LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"socialQuestions": 100, "socialTotal": 113, "gradeTotal": 1400}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
