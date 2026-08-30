#!/usr/bin/env python3
"""Author 13 Grade 5 social studies error-analysis questions (grade rows 1288-1300)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from build_unique_question_banks import ROOT
import author_grade5_math_segment01 as shared


SOURCE = ROOT / "turkiye/5-sinif/sosyal-bilgiler/sosyal-bilgiler-tum.jsonl"
OUTPUT = ROOT / "authoring/question-bank-blueprints/grade-5.jsonl"
LABELS_OUTPUT = ROOT / "authoring/question-bank-blueprints/grade-5-labels.json"


# note id, question, correct correction, three misconception choices, explanation
ITEMS = [
    (
        "tr-g05-sosyal-sb-5-1-1-note",
        "Sınıf temsilcisi seçilen bir öğrenci, 'Bu rol bana istediğim kararı tek başıma verme hakkı verir; arkadaşlarımı dinlemek zorunda değilim.' diyor. Hak, rol ve sorumluluk ilişkisini düzelten ifade hangisidir?",
        "Temsilci görüşleri iletme rolünü üstlenir; katılım hakkını kullanırken sınıfı dinleme ve ortak karara uyma sorumluluğu taşır.",
        ["Rol sahibi olmak bütün kurallardan muaf olmak demektir.", "Haklar yalnız yetişkinlere, sorumluluklar yalnız öğrencilere aittir.", "Sınıf temsilcisinin tek görevi kendi isteğini yönetime bildirmektir."],
        "Bir gruptaki rol belirli görevler getirir; hakların kullanımı başkalarının haklarına saygı ve sorumlulukların yerine getirilmesiyle birlikte düşünülür.",
    ),
    (
        "tr-g05-sosyal-sb-5-1-2-note",
        "Bir öğrenci farklı bir yöreye ait bayram geleneğini 'Bizimkine benzemediği için yanlıştır.' diye değerlendiriyor. Birlikte yaşama kültürüne uygun düzeltme hangisidir?",
        "Gelenek, ortaya çıktığı kültürel bağlam öğrenilerek incelenmeli; farklılık üstünlük ya da yanlışlık ölçütü yapılmamalıdır.",
        ["Bütün yöreler aynı geleneği uygulamaya zorlanmalıdır.", "Kültürel farklılıklar konuşulmamalı ve görünmez sayılmalıdır.", "Yalnız çoğunluğun geleneği kültürel değer kabul edilmelidir."],
        "Kültürel çeşitliliğe saygı, farklı uygulamaları kendi bağlamında tanımayı ve önyargı yerine karşılıklı anlayış kurmayı gerektirir.",
    ),
    (
        "tr-g05-sosyal-sb-5-1-3-note",
        "Sel sonrası yardım toplamak isteyen grup, ihtiyaç listesi almadan rastgele ürün göndermeyi planlıyor. Dayanışmayı etkili kılacak düzeltme hangisidir?",
        "Yetkili kurumların güncel ihtiyaç listesi doğrulanmalı, yardımlar güvenli biçimde sınıflandırılıp koordinasyonla ulaştırılmalıdır.",
        ["En çok görünen ürün, ihtiyaç olup olmadığına bakılmadan gönderilmelidir.", "Yardım yalnız bireysel yapılmalı, kurumlarla bilgi paylaşılmamalıdır.", "Dayanışma için afet bölgesine izinsiz gitmek yeterlidir."],
        "Yardımlaşma iyi niyetin yanında gerçek ihtiyacı belirleme, kaynak israfını önleme ve güvenli dağıtım için kurumlarla eşgüdüm gerektirir.",
    ),
    (
        "tr-g05-sosyal-sb-5-2-1-note",
        "Bir öğrenci 'Bir ilin kuzeyde olması değişmez, hangi yere göre konuşulduğu önemli değildir.' diyor. Göreceli konum kavramını düzelten ifade hangisidir?",
        "Kuzey, güney, yakınlık ve ulaşım bağlantıları seçilen referans yere göre ifade edilir; bu yüzden hangi yere göre konum verildiği belirtilmelidir.",
        ["Göreceli konum yalnız enlem ve boylam sayılarından oluşur.", "Bir ilin göreceli konumu yalnız yüz ölçümüyle belirlenir.", "Komşu iller ve ulaşım yolları konum açıklamasında kullanılamaz."],
        "Göreceli konum bir yerin çevresindeki deniz, il, yol, yer şekli ve başka merkezlere göre nerede bulunduğunu açıklar; referans değişince ifade de değişebilir.",
    ),
    (
        "tr-g05-sosyal-sb-5-2-2-note",
        "Bir sulak alanın bir bölümü yapılaşmaya açıldıktan sonra kuş sayısı azalıyor ve şiddetli yağışta su baskını artıyor. Öğrenci 'Çevre yalnız doğal nedenlerle değişir; yapılaşmanın etkisi yoktur.' diyor. Doğru çıkarım hangisidir?",
        "Beşerî yapılaşma yaşam alanını ve su tutma kapasitesini azaltmış olabilir; değişim doğal ve beşerî etkenlerin birlikte incelenmesini gerektirir.",
        ["Kuş sayısındaki azalma yapılaşmanın çevreyle ilgisiz olduğunu kanıtlar.", "Her su baskınının tek nedeni kuşların başka yere göç etmesidir.", "Doğal çevredeki değişim insanların yaşamını ve ekonomik faaliyetleri etkilemez."],
        "Sulak alanlar canlılara yaşam alanı sağlar ve suyu tutar; arazi kullanımındaki değişikliklerin canlı çeşitliliği ve taşkın riski üzerindeki etkisi kanıtlarla karşılaştırılmalıdır.",
    ),
    (
        "tr-g05-sosyal-sb-5-2-3-note",
        "Deprem planında bir öğrenci 'Sarsıntı sırasında pencereye koşarım, sonra asansörle inerim.' yazıyor. Afet zararını azaltan doğru düzeltme hangisidir?",
        "Önceden eşyalar sabitlenmeli; sarsıntıda çök-kapan-tutun uygulanmalı, sarsıntı bitince güvenli çıkış ve toplanma planı izlenmelidir.",
        ["Sarsıntı sırasında merdivene koşmak her binada en güvenli davranıştır.", "Hazırlık yalnız deprem olduktan sonra yapılmalıdır.", "Toplanma alanı yerine binanın camlı girişinde beklenmelidir."],
        "Afet yönetimi risk azaltma, hazırlık, doğru davranış ve iyileşme aşamalarını içerir; pencere, asansör ve kontrolsüz hareket ek tehlike oluşturabilir.",
    ),
    (
        "tr-g05-sosyal-sb-5-2-4-note",
        "Bir öğrenci kara komşularını Türkiye'ye göre konumlandırırken 'İran batıda, Bulgaristan güneyde, Suriye kuzeydedir.' diyor. Üç yön hatasını düzelten seçenek hangisidir?",
        "İran doğuda, Bulgaristan kuzeybatıda, Suriye güneyde yer alan kara komşularıdır.",
        ["İran kuzeybatıda, Bulgaristan doğuda, Suriye batıda yer alır.", "Üç ülke de Türkiye'nin yalnız kuzeyinde yer alır.", "Kara komşularının yönü haritadan belirlenemez; yalnız nüfusla açıklanır."],
        "Türkiye taban haritasında ülke sınırlarına göre İran doğuda, Bulgaristan kuzeybatıda ve Suriye güneyde bulunur; yönler harita kanıtıyla belirlenir.",
    ),
    (
        "tr-g05-sosyal-sb-5-3-1-note",
        "Bir öğrenci tarihî taş köprüyü somut olmayan, kuşaktan kuşağa aktarılan halk ezgisini ise somut miras sayıyor. Sınıflandırmayı düzelten ifade hangisidir?",
        "Taş köprü fiziksel varlığı olan somut; halk ezgisi bilgi ve icrayla aktarılan somut olmayan ortak mirastır.",
        ["Yalnız müzede sergilenen nesneler somut miras olabilir.", "Yazıya geçirilmiş her gelenek otomatik olarak somut mirasa dönüşür.", "Ortak miras yalnız günümüzde kullanılan yeni yapılardan oluşur."],
        "Somut miras görülebilen ve dokunulabilen yapı, alan ve nesneleri; somut olmayan miras ise sözlü anlatım, müzik, tören, bilgi ve becerileri kapsar.",
    ),
    (
        "tr-g05-sosyal-sb-5-3-2-note",
        "Bir yerleşimde bitki tohumları, tahıl depoları, öğütme taşları ve birbirine bitişik kalıcı evler bulunuyor. Öğrenci 'Bu kanıtlar yalnız göçebe avcılığı gösterir.' diyor. Doğru tarihsel çıkarım hangisidir?",
        "Kanıtlar üretim, depolama ve kalıcı konutlar nedeniyle yerleşik tarım yaşamını destekler; sonuç buluntularla sınırlı kurulmalıdır.",
        ["Öğütme taşı insanların hiç bitki tüketmediğini gösterir.", "Kalıcı evler yerleşimde sosyal ilişki bulunmadığını kanıtlar.", "Tek bir buluntu bütün Anadolu'daki yaşamın aynı olduğunu kesinleştirir."],
        "Arkeolojik buluntular birlikte yorumlanır; tohum, depo ve öğütme araçları üretim-beslenme ilişkisini, kalıcı yapılar ise yerleşik yaşamı destekleyen kanıtlardır.",
    ),
    (
        "tr-g05-sosyal-sb-5-3-3-note",
        "Öğrenci 'Çivi yazısını Lidyalılar, madeni parayı Sümerler geliştirdi.' biçiminde bir katkı eşleştirmesi yapıyor. Ders içeriğine uygun düzeltme hangisidir?",
        "Çivi yazısı Mezopotamya'da Sümerlerle, madeni paranın kullanımı Anadolu'da Lidyalılarla ilişkilendirilir.",
        ["Her iki gelişme de yalnız Hititlere aittir.", "Yazı ve para toplumların iletişim ve ticaretini etkilememiştir.", "Medeniyet katkıları yer ve zaman kanıtı olmadan rastgele eşleştirilebilir."],
        "Medeniyetlerin katkıları kaynak, yer ve dönem bilgisiyle eşleştirilir; Sümerlerin yazısı kayıt tutmayı, Lidyalıların para kullanımı değişimi ve ticareti kolaylaştırmıştır.",
    ),
    (
        "tr-g05-sosyal-sb-5-4-1-note",
        "Bir öğrenci 'Çoğunluk bir karar aldıysa azınlığın temel haklarını dikkate almak gerekmez.' diyor. Demokrasi ve cumhuriyet anlayışına uygun düzeltme hangisidir?",
        "Çoğunlukla karar alınabilir; ancak hukuk, temel haklar, eşitlik ve azınlığın görüşünü ifade edebilmesi demokratik düzen içinde korunur.",
        ["Demokrasi yalnız seçim günü oy kullanmaktan ibarettir.", "Cumhuriyette yöneticiler halka karşı sorumlu değildir.", "Farklı görüşlerin açıklanması ortak karar süreçlerini her zaman bozar."],
        "Demokratik yönetimde katılım ve çoğunluk ilkesi hukuk devleti, temel haklar, çoğulculuk ve hesap verebilirlikle birlikte işler.",
    ),
    (
        "tr-g05-sosyal-sb-5-4-2-note",
        "Mahalle parkındaki kırık oyun aracını gören öğrenci 'Etkin vatandaş yalnız şikâyet eder; çözüm için kuruma bilgi vermesi gerekmez.' diyor. Doğru vatandaşlık davranışı hangisidir?",
        "Tehlike güvenli biçimde belgelenip belediyenin ilgili birimine bildirilebilir; süreç izlenirken ortak alanı koruma sorumluluğu sürdürülür.",
        ["Oyun aracı uzmanlık olmadan öğrenci tarafından sökülmelidir.", "Kamusal sorunlar yalnız başkalarını etkilediği için görmezden gelinmelidir.", "Kurumlara başvurmak yerine doğrulanmamış bilgi sosyal medyada yayılmalıdır."],
        "Etkin vatandaş sorunları hak ve sorumluluk çerçevesinde fark eder, uygun kuruma kanıta dayalı başvuru yapar ve güvenli, yasal katılım yollarını kullanır.",
    ),
    (
        "tr-g05-sosyal-sb-5-4-3-note",
        "Bir öğrenci 'Düşüncemi açıklama hakkım varsa başka birinin özel bilgisini izinsiz paylaşabilirim.' diyor. Hak-sorumluluk dengesini düzelten seçenek hangisidir?",
        "İfade özgürlüğü başkalarının özel hayatı, onuru ve güvenliğiyle birlikte korunur; kişisel bilgi izinsiz paylaşılmamalıdır.",
        ["Temel haklar yalnız kişi tek başınayken geçerlidir.", "Özel hayatın korunması ifade özgürlüğünü bütünüyle ortadan kaldırır.", "Bir bilgi çevrim içi görülmüşse kaynağı ve izni araştırılmadan yayılabilir."],
        "Temel haklar birbirini yok etmeden birlikte korunur; bir hakkı kullanmak başkasının hakkını ihlal etme yetkisi vermez ve sorumlu davranış gerektirir.",
    ),
]


def notes() -> dict[str, dict[str, Any]]:
    rows = [json.loads(line) for line in SOURCE.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    return {str(row.get("id")): row for row in rows if row.get("type") == "note"}


def neighbour_map(qid: str, labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    alt = f"{prefix}.alt"
    labels[alt] = "Türkiye çevresinde sekiz kara komşusunun konumlarını etiketlerle gösteren harita; doğru seçenek işaretlenmemiştir."
    marker_data = [
        ("Yunanistan", 5, 40), ("Bulgaristan", 19, 15), ("Gürcistan", 76, 17), ("Ermenistan", 86, 33),
        ("Azerbaycan (Nahçıvan)", 91, 43), ("İran", 97, 55), ("Irak", 83, 77), ("Suriye", 56, 86),
    ]
    markers = []
    for index, (name, x, y) in enumerate(marker_data, 1):
        key = f"{prefix}.country{index}"
        labels[key] = name
        markers.append({"x": x, "y": y, "labelKey": key})
    return {"kind": "map", "base": "turkiye", "markers": markers, "altTextKey": alt}


def make(local: int, entry: tuple[Any, ...], note_map: dict[str, dict[str, Any]], labels: dict[str, str]) -> dict[str, Any]:
    note_id, stem, correct_text, wrongs, explanation = entry
    note = note_map[note_id]
    objective = str((note.get("objectives") or [""])[0])
    global_number = 1287 + local
    correct = (global_number - 1) % 4
    raw_choices = [correct_text, *wrongs]
    raw_reasons = [
        f"Doğru kanıta dayalı düzeltme: {explanation}",
        f"Tek ölçüte indirgeme yanılgısı: Bu seçenek sosyal olayı bağlam, hak, yer veya zaman kanıtlarının yalnız biriyle açıklar. {explanation}",
        f"Neden-sonuç yanılgısı: Bu seçenek verilen gözlemden desteklenmeyen ya da ters yönde bir sonuç çıkarır. {explanation}",
        f"Kapsamı aşan genelleme yanılgısı: Bu seçenek sınırlı bilgiyi bütün kişi, yer veya dönemlere kesin biçimde yayar. {explanation}",
    ]
    choices, distractor_why = shared.rotate(raw_choices, raw_reasons, correct)
    qid = f"tr-g05-bank-sos-s01-q{local:03d}"
    fig = neighbour_map(qid, labels) if local == 7 else None
    if fig:
        stem = f"Aşağıdaki haritayı inceleyiniz. Türkiye haritasındaki komşu ülke konumları değerlendiriliyor. {stem}"
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "Kara komşularının Türkiye'ye göre yönleri yalnız harita üzerindeki konumlarıyla gösterilir.",
        "acceptableKinds": ["map"], "evidenceDimensions": ["ülke", "sınır yönü", "Türkiye'ye göre konum"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "Sosyal durum, öğrenci iddiası ve değerlendirme için gereken kanıtlar soru metninde verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    level = 3 if local <= 3 else 4
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "Sosyal Bilgiler", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — hata analizi",
        "objective": objective, "objectiveId": objective,
        "noteId": note_id, "noteKey": note_id,
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct],
        "distractorWhy": distractor_why,
        "explanation": f"İddia, bağlı konu anlatımındaki kavramlar ve verilen kanıtlar birlikte kullanılarak sınanır. {explanation}",
        "level": level,
        "difficultyReason": f"Düzey {level}; öğrencinin sosyal bilgi iddiasındaki kavram veya kanıt hatasını bulmayı, bağlam sınırını korumayı ve gerekçeli düzeltme yapmayı gerektirir.",
        "questionType": "error-analysis", "familyId": f"tr-g05-bank-sos-family-{global_number:03d}",
        "objectiveSource": note.get("objectiveSource"),
        "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [], "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1287:
        raise RuntimeError("the first 1287 grade questions must be regenerated before social segment 01")
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = notes()
    rows = [make(local, entry, note_map, labels) for local, entry in enumerate(ITEMS, 1)]
    OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"socialQuestions": 13, "socialTotal": 13, "gradeTotal": 1300}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
