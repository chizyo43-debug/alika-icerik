#!/usr/bin/env python3
"""Author 63 Grade 5 Turkish paired tasks (grade rows 1638-1700)."""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from typing import Any

from build_unique_question_banks import ROOT
import author_grade5_social_segment01 as shared


SOURCE = ROOT / "turkiye/5-sinif/turkce/turkce-tum.jsonl"
OUTPUT = ROOT / "authoring/question-bank-blueprints/grade-5.jsonl"
LABELS_OUTPUT = ROOT / "authoring/question-bank-blueprints/grade-5-labels.json"


FULL_MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
FULL_LEVELS = (
    [1] * 15 + [2] * 10 +
    [1] * 5 + [2] * 15 + [3] * 15 +
    [3] * 10 + [4] * 10 + [5] * 5 +
    [3] * 5 + [4] * 10
)
MODES = FULL_MODES[37:]
LEVELS = FULL_LEVELS[37:]
NOTE_IDS = [
    "tr-g05-tur-td-5-1-n01", "tr-g05-tur-td-5-5-n01", "tr-g05-tur-td-5-7-n01",
    "tr-g05-tur-td-5-10-n01", "tr-g05-tur-td-5-22-n01", "tr-g05-tur-to-5-5-n01",
    "tr-g05-tur-to-5-6-n01", "tr-g05-tur-to-5-8-n01", "tr-g05-tur-to-5-13-n01",
    "tr-g05-tur-to-5-14-n01", "tr-g05-tur-to-5-15-n01", "tr-g05-tur-to-5-24-n01",
    "tr-g05-tur-tk-5-1-n01", "tr-g05-tur-tk-5-3-n01", "tr-g05-tur-tk-5-5-n01",
    "tr-g05-tur-tk-5-9-n01", "tr-g05-tur-tk-5-23-n01", "tr-g05-tur-ty-5-1-n01",
    "tr-g05-tur-ty-5-3-n01", "tr-g05-tur-ty-5-20-n01", "tr-g05-tur-ty-5-21-n01",
    "tr-g05-tur-to-5-21-n01",
]


# task text, correct response, three misconceptions, explanation
CASES = [
    (
        "Amaç, 'mendil kapmaca' oyununun kurallarını doğru öğrenmektir. Aday materyaller kaynak göstermeyen kısa reklam, yalnız müzik içeren klip ve kültür kurumunun anlatımlı uygulama videosudur.",
        "Amaca ve kaynağa uygun seçim: Kuralları adım adım gösteren, kaynağı belli uygulama videosunu kullanmak.",
        ["Görsel çekiciliği yeterli sayma: Kuralları anlatmayan müzik klibini seçmek", "Reklamı bilgi kaynağı sanma: Ürünü öven kısa tanıtımı seçmek", "Kaynak denetimini atlama: İlk karşılaşılan videoyu doğrulamadan kullanmak"],
        "Dinleme-izleme materyali amaç, içerik yeterliliği, yaşa uygunluk ve güvenilir kaynak ölçütleriyle seçilir; yalnız çekicilik bilgi doğruluğunu göstermez.",
    ),
    (
        "Sesli duyuru şöyledir: 'Kukla atölyesi cumartesi saat onda kütüphanede başlayacak; katılımcılar makas getirecek.' Açık bilgiler belirleniyor.",
        "Duyuruda açıkça verilenler: Cumartesi, saat on, kütüphane ve makas getirme koşulu.",
        ["Metinde olmayan ayrıntıyı ekleme: Atölyenin pazar günü bahçede olduğunu söylemek", "Bir bilgiyi değiştirme: Başlangıç saatini öğleden sonra kabul etmek", "Çıkarımı açık bilgi sanma: Katılımcıların kuklayı eve götüreceğini kesinleştirmek"],
        "Açık bilgi, duyuruda doğrudan söylenen yer, zaman ve hazırlık ayrıntılarıdır; metinde bulunmayan sonuçlar kesin bilgi diye sunulamaz.",
    ),
    (
        "Kayda önce fermuar sesi, sonra yağmurun cama vuruşu ve 'Şemsiyeni unutma.' cümlesi geliyor. Konuşmacının hazırlığına ilişkin çıkarım aranıyor.",
        "Ses ve söz ipuçlarını birleştirme: Dışarıda yağış olduğu için yağmurluk veya çanta hazırlanıyor olabilir.",
        ["Tek sesi kesin kanıt sayma: Fermuar duyulduğu için valizle uzun yolculuğu kesinleştirmek", "Sözlü ipucunu yok sayma: Havanın güneşli olduğunu savunmak", "İlgisiz çıkarım yapma: Konuşmacının yemek pişirdiğini söylemek"],
        "Çıkarım birden çok ipucunun desteklediği olası sonuçtur; fermuar, yağmur ve şemsiye uyarısı yağışa uygun hazırlığı destekler fakat ayrıntıyı kesinleştirmez.",
    ),
    (
        "İlk konuşmacı bisiklette kask kullanımını, ikinci konuşmacı gece görünür olmak için reflektörü anlatıyor; ikisi de güvenli sürüş kurallarına uyulmasını istiyor.",
        "Ortak ve farklı yönleri ayırma: Ortak amaç güvenliktir; verilen güvenlik önlemleri kask ve reflektör olarak farklıdır.",
        ["Tek ayrıntıyı ortak sayma: İki konuşmanın da yalnız kaskı anlattığını söylemek", "Amaçları ters yorumlama: Birinin güvenliği gereksiz bulduğunu savunmak", "Karşılaştırma yapmama: Yalnız ilk konuşmayı özetleyip ikinciyi dışlamak"],
        "İki konuşma karşılaştırılırken ortak amaç ile her metne özgü destekleyici ayrıntılar ayrı sütunlarda belirlenir.",
    ),
    (
        "Bir içecek reklamı 'Bunu içen herkes gün boyu en güçlü olur.' diyor; araştırma, uzman görüşü veya içerik bilgisi göstermiyor.",
        "Medya iletisini sorgulama: 'Herkes' ve 'en güçlü' iddiaları kanıtsız genellemedir; kaynak ve içerik bilgisi aranmalıdır.",
        ["Sloganı kanıt sayma: Tekrarlandığı için iddiayı doğru kabul etmek", "Görseli bilimsel veri sanma: Renkli görüntünün etkiyi kanıtladığını söylemek", "Reklam amacını yok sayma: Mesajın satış yapmaya çalışmadığını savunmak"],
        "Medya mesajında amaç, hedef kitle, kanıt, kaynak ve abartılı dil birlikte incelenir; slogan doğrulanabilir bilgi yerine geçmez.",
    ),
    (
        "'Duru, arkadaşının uyarısını kulak ardı etmedi ve yola çıkmadan haritayı yeniden inceledi.' cümlesinde 'kulak ardı etmedi' sözünün anlamı aranıyor.",
        "Bağlama dayalı anlam: Uyarıyı önemseyip dikkate aldı.",
        ["Sözcükleri gerçek anlamda birleştirme: Uyarıyı kulağının arkasına koydu", "Olumsuzluğu atlama: Uyarıyı önemsemedi", "İlgisiz anlam seçme: Uyarıyı yüksek sesle söyledi"],
        "Deyimin anlamı sonraki eylemle sınanır; haritayı yeniden incelemesi, uyarıyı dikkate aldığını gösterir.",
    ),
    (
        "Yazılı duyuru şöyledir: 'Park temizliği pazar günü saat dokuzda doğu kapısında başlayacak. Eldivenler belediyece verilecektir.' Doğrudan bilgiler seçiliyor.",
        "Metinde açıkça verilenler: Pazar günü, saat dokuz, doğu kapısı ve eldivenlerin belediyece sağlanması.",
        ["Yer bilgisini değiştirme: Batı kapısını başlangıç noktası yapmak", "Metinde olmayan amacı ekleme: Katılanlara ödül verileceğini söylemek", "Zamanı genelleme: Etkinliğin her pazar yapılacağını kesinleştirmek"],
        "Açık bilgi metindeki cümlelerden doğrudan bulunur; tek etkinliğin zamanı, yeri ve sağlanan araçlar değiştirilmeden aktarılır.",
    ),
    (
        "Öykü kişisi odadan çıkarken ışığı kapatıyor, diş fırçalarken musluğu açık bırakmıyor ve kullanılmayan kâğıtları ayırıyor.",
        "Davranışlardan çıkarım: Kişi kaynakları verimli kullanmaya önem vermektedir.",
        ["Tek davranışı abartma: Kişinin hiç elektrik kullanmadığını söylemek", "Ters çıkarım yapma: Kaynak israfını önemsediğini reddetmek", "Metin dışına çıkma: Kişinin mesleğini kesinleştirmek"],
        "Çıkarım, birden çok davranışın ortak yönüne dayanır; ışık, su ve kâğıtla ilgili eylemler tasarruf tutumunu destekler.",
    ),
    (
        "İki cümle inceleniyor: 'İlçe kütüphanesinde 12 400 kitap vardır.' ve 'Bu, ülkenin en güzel kütüphanesidir.'",
        "Bilgi-görüş ayrımı: Kitap sayısı doğrulanabilir olgudur; 'en güzel' kişisel değerlendirmedir.",
        ["Her iki cümleyi görüş sayma: Sayısal verinin doğrulanabilirliğini yok sayma", "Her iki cümleyi bilgi sayma: Beğeniyi ölçülmüş veri kabul etme", "Yazılı olanı otomatik bilgi sayma: Kaynak ve ölçüt aramama"],
        "Olgusal bilgi gözlem veya kayıtla doğrulanabilir; kişisel görüş beğeni ve değerlendirme bildirir, herkes için aynı olmak zorunda değildir.",
    ),
    (
        "Öyküde Ece okul bahçesinde uçurtmasını kaybediyor, rüzgâr kesilmeden önce arkadaşlarıyla arıyor ve uçurtmayı ağacın dalında buluyor.",
        "Öykü unsurlarını eşleştirme: Kişi Ece, yer okul bahçesi, sorun kayıp uçurtma, çözüm arkadaşlarla arayıp dalda bulmadır.",
        ["Sorunla çözümü karıştırma: Ağacı kayıp olayının nedeni sayma", "Yeri değiştirme: Olayı evin mutfağında geçmiş kabul etme", "Metinde olmayan kişi ekleme: Öğretmenin uçurtmayı getirdiğini söyleme"],
        "Öykü kişisi, yer, zaman, sorun ve çözüm metindeki olay akışından ayrı ayrı belirlenir; bulunma anı sorunun çözümüdür.",
    ),
    (
        "Metin önce gerekli malzemeleri listeliyor, ardından 'karıştır, dinlendir, şekil ver' gibi sıralı emir cümleleri kullanıyor.",
        "Tür işaretlerine göre tanıma: Malzeme ve işlem sırası içeren öğretici tarif/yönerge metnidir.",
        ["Öykü sanma: Emir kiplerini olay örgüsü kabul etmek", "Şiir sanma: Satırların kısa olmasını tek ölçüt yapmak", "Haber sanma: Yer ve tarih bilgisi olmadan güncel olay aktardığını söylemek"],
        "Metin türü biçimden tek başına değil amaç, yapı ve dil işaretlerinden tanınır; malzeme listesi ve sıralı eylemler yönergeyi gösterir.",
    ),
    (
        "Çevrim içi haberde çarpıcı bir başlık ve eski bir fotoğraf vardır; yazar, tarih ve veri kaynağı belirtilmemiştir.",
        "Eleştirel okuma planı: Tarih, yazar, özgün fotoğraf bağlamı ve güvenilir ikinci kaynaklar doğrulanmadan paylaşmamak.",
        ["Başlığı yeterli kanıt sayma: Metni okumadan paylaşmak", "Fotoğrafı zamansız gerçek sayma: Nerede ve ne zaman çekildiğini araştırmamak", "Beğeni sayısını doğruluk ölçütü yapmak: Çok paylaşılanı otomatik doğru kabul etmek"],
        "Medya metni başlık, görsel, tarih, yazar, amaç ve kaynaklar bakımından sorgulanır; eski veya bağlamsız görsel yanıltıcı olabilir.",
    ),
    (
        "Sınıf tartışmasında konuşmacı cümlesini bitirmeden araya giren ve karşı görüşü tekrar etmeden yanıtlayan öğrenci için uygun düzeltme aranıyor.",
        "Konuşma sırasını koruma: Sözün bitmesini beklemek, duyulan görüşü doğru anladığını gösterip kendi gerekçesini sakin biçimde sunmak.",
        ["Sesi yükseltme: Haklı görünmek için konuşanın sözünü kesmek", "Konudan kaçma: Karşı görüş yerine kişiyi eleştirmek", "Dinlemeyi bırakma: Yalnız kendi cümlesini tekrarlamak"],
        "Uygun konuşma göz teması, söz sırası, etkin dinleme, konuya bağlılık ve saygılı gerekçe gerektirir.",
    ),
    (
        "Amaç, okul yönetimini kâğıt geri dönüşüm kutuları yerleştirmeye ikna eden iki dakikalık konuşma hazırlamaktır.",
        "Amaca uygun içerik: Sorunu kısa veriyle açıklamak, uygulanabilir kutu planı önermek ve beklenen yararı gerekçelendirmek.",
        ["İlgisiz anı anlatma: Tatil deneyimini konuşmanın merkezine koymak", "Yalnız slogan kullanma: Sorun ve çözüm kanıtı vermemek", "Hedef kitleyi yok sayma: Yönetimin uygulayamayacağı belirsiz istekler sıralamak"],
        "Konuşma içeriği amaç, süre ve hedef kitleye göre seçilir; ikna için sorun, kanıt, uygulanabilir öneri ve sonuç bağı kurulur.",
    ),
    (
        "İki grup bahçeyi aynı saatte kullanmak istiyor. Bir öğrenci öteki grubun gerekçesini sormadan 'Biz önce geldik, konu kapandı.' diyor.",
        "Uzlaşma adımı: Her grubun ihtiyacını açık sorularla dinlemek, ortak ölçüt belirlemek ve zamanı adil biçimde paylaşan plan kurmak.",
        ["Tek taraflı karar: Yalnız güçlü grubun isteğini uygulamak", "Sorunu erteleme: Hiç konuşmadan iki grubun da bahçeyi kullanmamasını istemek", "Kişiye yönelme: Gerekçe yerine grup üyelerini suçlamak"],
        "Uzlaşma soru sorma, etkin dinleme, ortak ve farklı ihtiyaçları belirleme ve tarafların kabul edebileceği çözüm üretme sürecidir.",
    ),
    (
        "'Bu kitabı sen mi getirdin?' cümlesinde farklı sözcüklerin vurgulanmasıyla sorulan bilgi değişiyor.",
        "Vurguyu anlama bağlama: 'sen' vurgusu kişiyi, 'bu' vurgusu hangi kitabı, 'getirdin' vurgusu eylemi öne çıkarır.",
        ["Vurguyu yalnız ses yüksekliği sanma: Anlam odağının değişmediğini söylemek", "Her sözcüğü aynı şiddette söyleme: Sorulan bilgiyi belirsiz bırakmak", "Soru tonunu yok sayma: Cümleyi kesin bildiri gibi okumak"],
        "Ses tonu, vurgu ve durak konuşmanın anlam odağını ve tutumunu taşır; vurgu yeri değişince yanıt beklenen öge de değişebilir.",
    ),
    (
        "Arkadaşının başarısını kutlayan konuşmacı donuk sesle 'Ne güzel, çok sevindim.' diyor ve yüzünü çeviriyor.",
        "Sözlü ve sözsüz uyum: İçten sevinç için sıcak ton, uygun yüz ifadesi ve arkadaşına yönelme sözlerle tutarlı olmalıdır.",
        ["Yalnız sözcükleri yeterli sayma: Ses ve beden dilinin etkisini yok sayma", "Duyguyu abartma: Kutlama yerine bağırarak konuşmayı seçme", "Ters tutum gösterme: Alaycı tonun aynı anlamı verdiğini savunma"],
        "Duygu ve tutum sözcüklerin yanında ses tonu, vurgu, yüz ifadesi ve beden yönelimiyle aktarılır; kanalların uyumu anlamı güçlendirir.",
    ),
    (
        "Öğrenci araştırma yazısını konu belirlemeden doğrudan temize çekiyor; kaynakları sonradan ekleyip hiç gözden geçirmemeyi planlıyor.",
        "Yazma sürecini yönetme: Amaç ve konu belirle, bilgi topla, planla, taslak yaz, içerik-dil düzeltmesi yap ve son biçimi yayımla.",
        ["Taslağı son ürün sayma: İlk yazımı kontrol etmeden teslim etmek", "Kaynağı sona bırakma: Bilgiyi nereden aldığını kaydetmemek", "Yalnız yazımı düzeltme: İçerik, düzen ve hedef kitleyi hiç gözden geçirmemek"],
        "Yazma doğrusal tek hamle değil; planlama, taslak, gözden geçirme, düzenleme ve paylaşma aşamalarının gerektiğinde yinelendiği bir süreçtir.",
    ),
    (
        "Paragrafın amacı okul bahçesinde gölgelik gereksinimini açıklamaktır; taslakta konu cümlesi, yaz tatili anısı ve ilgisiz yemek listesi peş peşe verilmiştir.",
        "Paragraf bütünlüğü: Gereksinimi belirten konu cümlesini sıcaklık/gölge verileri ve uygulanabilir sonuç cümlesiyle desteklemek.",
        ["İlgisiz ayrıntıları artırma: Yemek listesini paragrafın çoğuna yaymak", "Konu cümlesini kaldırma: Okurun ana düşünceyi tahmin etmesini istemek", "Desteksiz sonuç yazma: Kanıt vermeden yalnız 'Gölgelik şarttır.' demek"],
        "Amaca uygun paragraf tek ana düşünce çevresinde konu cümlesi, ilgili destekleyici ayrıntılar ve düşünceyi tamamlayan sonuçla kurulur.",
    ),
    (
        "Taslak şöyledir: 'Bisiklet çevre dostudur. Bazı yollar güvenli değildir. ___ güvenli bisiklet yolları artırılmalıdır.' Uygun geçiş aranıyor.",
        "Neden-sonuç geçişi: 'Bu nedenle' ifadesi sorunla öneri arasındaki sonucu kurar.",
        ["Karşıtlık bağını yanlış kurma: 'Oysa' ile öneriyi nedenin tersi gibi sunmak", "Sıralama sözü kullanma: 'İlk olarak' deyip önceki neden-sonuç bağını koparmak", "İlgisiz ekleme yapma: 'Örneğin' deyip sonuç yerine yeni konu başlatmak"],
        "Geçiş ifadesi cümleler arasındaki anlam ilişkisine göre seçilir; güvenli olmayan yollar önerinin nedenidir, öneri bu nedenle sonuçtur.",
    ),
    (
        "Oyun yönergesi taslağı şöyledir: 'çocuklar iki gruba ayrılır ali Başlama çizgisini gösterir sonra oyun başlar' Yazım ve noktalama düzeltiliyor.",
        "Cümle ve özel ad düzeni: 'Çocuklar iki gruba ayrılır. Ali başlama çizgisini gösterir, sonra oyun başlar.'",
        ["Bütün sözcükleri büyük harfle yazma: Cümle ve özel ad ayrımını yok saymak", "Noktalamasız bırakma: İşlem sırasındaki cümle sınırlarını göstermemek", "Özel adı küçük yazma: 'ali' biçimini koruyup yalnız virgül eklemek"],
        "Cümle büyük harfle başlar ve uygun noktayla biter; kişi adı büyük harfle yazılır, sıralı eylemler virgül veya ayrı cümlelerle açıklaştırılır.",
    ),
    (
        "'Konuklar salona girdi, ev sahibi misafirleri karşıladı.' ve 'Cimri adamın cömert kardeşi yardım etti.' cümlelerindeki anlam ilişkileri aranıyor.",
        "Sözcük ilişkilerini ayırma: 'Konuk-misafir' eş anlamlı, 'cimri-cömert' karşıt anlamlıdır.",
        ["Bütününü karşıt sayma: Konuk ile misafiri zıt anlamlı kabul etmek", "Ses benzerliğini ölçüt yapma: Anlam yerine harf sayısını karşılaştırmak", "Bağlamı yok sayma: Cimri ile cömerti eş anlamlı saymak"],
        "Eş anlamlı sözcükler aynı veya yakın kavramı, karşıt anlamlılar zıt özellikleri karşılar; cümle bağlamı ilişkiyi doğrular.",
    ),
]


def notes() -> dict[str, dict[str, Any]]:
    rows = [json.loads(line) for line in SOURCE.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    return {str(row.get("id")): row for row in rows if row.get("type") == "note"}


def balanced_pairs() -> list[tuple[int, int]]:
    available = list(combinations(range(len(NOTE_IDS)), 2))
    counts = [0] * len(NOTE_IDS)
    selected: list[tuple[int, int]] = []

    def digest(value: tuple[int, int]) -> str:
        return sha256(("-".join(map(str, value)) + "-alika-tur-s01").encode()).hexdigest()

    for _ in range(63):
        pair = min(
            (value for value in available if value not in selected),
            key=lambda value: (max(counts[value[0]], counts[value[1]]), counts[value[0]] + counts[value[1]], digest(value)),
        )
        selected.append(pair)
        counts[pair[0]] += 1
        counts[pair[1]] += 1
    if min(counts) < 5 or max(counts) > 6 or len(set(selected)) != 63:
        raise RuntimeError("Turkish topic-pair schedule is not balanced")
    return selected


def table(qid: str, titles: list[str], cases: list[tuple[str, str, list[str], str]], labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, h3, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.h3", f"{prefix}.alt"
    labels[h1], labels[h2], labels[h3] = "Görev", "Dil becerisi", "Metin veya ileti"
    labels[alt] = "İki Türkçe dil becerisine ait I ve II metin/ileti görevlerini gösteren tablo; doğru yanıtlar belirtilmemiştir."
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
    global_base: int = 1637,
    batch_id: str = "s01",
    schedule_offset: int = 37,
) -> dict[str, Any]:
    global_number = global_base + local
    first_index, second_index = selected
    cases = [CASES[first_index], CASES[second_index]]
    notes_for_task = [note_map[NOTE_IDS[first_index]], note_map[NOTE_IDS[second_index]]]
    objectives = [str((note.get("objectives") or [""])[0]) for note in notes_for_task]
    variant = (local - 1) // 7
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
        f"Doğru iki-beceri çözümü: I için {cases[0][3]} II için {cases[1][3]}",
        f"Birinci görevde metin kanıtı yanılgısı: I. yanıt açık bilgi, bağlam veya iletişim amacını bozarken II doğrudur. {cases[0][3]}",
        f"İkinci görevde dil işlevi yanılgısı: I doğru olsa da II. yanıt görev ve metin ilişkisini kuramaz. {cases[1][3]}",
        f"Çifte bağlam yanılgısı: Her iki yanıt da kendi metnindeki amaç, yapı, söz veya kanıt sınırını değiştirir. {cases[0][3]} {cases[1][3]}",
    ]
    correct = (global_number - 1) % 4
    choices, distractor_why = shared.shared.rotate(raw_choices, raw_reasons, correct)
    mode = FULL_MODES[schedule_offset + local - 1]
    level = FULL_LEVELS[schedule_offset + local - 1]
    qid = f"tr-g05-bank-tur-{batch_id}-q{local:03d}"
    titles = [str(note["title"]) for note in notes_for_task]
    if mode == "comprehension":
        stem = f"İki Türkçe görevinin temel anlamı karşılaştırılıyor. I: {cases[0][0]} II: {cases[1][0]} İki metin veya iletiyi de doğru yorumlayan yanıt çifti hangisidir?"
        fig = None
    elif mode == "application":
        stem = f"İki Türkçe görevi ayrı ayrı uygulanacaktır. I: {cases[0][0]} II: {cases[1][0]} Her iki görevi de amacına uygun tamamlayan yanıt çifti hangisidir?"
        fig = None
    elif mode == "analysis":
        stem = f"Aşağıdaki tabloda {titles[0].casefold()} ile {titles[1].casefold()} becerilerine ait iki kayıt vardır. Metin ve ileti kanıtlarını çözümleyip iki doğru yanıtı veren seçenek hangisidir?"
        fig = table(qid, titles, cases, labels)
    else:
        stem = f"Bir öğrenci I için '{wrong_a}', II için '{wrong_b}' yanıtını veriyor. I. görev {cases[0][0]} II. görev {cases[1][0]} İki dil yanılgısını da düzelten yanıt çifti hangisidir?"
        fig = None
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "İki metin/ileti görevi ve bağlı dil becerileri yalnız tabloda birlikte gösterilir.",
        "acceptableKinds": ["table"], "evidenceDimensions": ["görev", "dil becerisi", "metin veya ileti"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "İki Türkçe görevinin metinleri ve değerlendirme koşulları soru metninde verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    note = notes_for_task[0]
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "Türkçe", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — iki beceri {mode}",
        "objective": objectives[0], "objectiveId": objectives[0], "integratedObjectives": objectives,
        "noteId": note.get("id"), "noteKey": note.get("id"),
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct], "distractorWhy": distractor_why,
        "explanation": f"I. görev için {cases[0][3]} II. görev için {cases[1][3]} Her yanıt kendi metin ve ileti kanıtıyla doğrulanır.",
        "level": level,
        "difficultyReason": f"Düzey {level}; iki Türkçe becerisini {mode} biçiminde ayrı metin kanıtlarına uygulayıp yanıtları tek seçimde birleştirmeyi gerektirir.",
        "questionType": mode, "familyId": f"tr-g05-bank-tur-family-{global_number:03d}",
        "objectiveSource": note.get("objectiveSource"), "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [], "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1637:
        raise RuntimeError("the first 1637 grade questions must be regenerated before Turkish segment 01")
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = notes()
    rows = [make(local, selected, note_map, labels) for local, selected in enumerate(balanced_pairs(), 1)]
    OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"turkishQuestions": 63, "turkishTotal": 63, "gradeTotal": 1700}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
