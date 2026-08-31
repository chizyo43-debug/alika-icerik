#!/usr/bin/env python3
"""Append 45 mathematics and 55 social studies questions for Grade 6 batch 15."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

from author_grade6_bilisim_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade6_english_batch11 import rows
from author_grade6_english_math_batch12 import MATH_SOURCE
from author_grade6_fen_batch07 import task
from author_grade6_fen_english_batch10 import make_record
from author_grade6_mixed_batch03 import read_notes_only

SOCIAL_SOURCE = Path("turkiye/6-sinif/sosyal-bilgiler/sosyal-bilgiler-tum.jsonl")


def vrows(note: str, values: list[tuple[str, str, str, str, str, str, str, str | None]]):
    result = []
    for mode, stem, correct, w1, w2, w3, explanation, visual in values:
        item = task(note, mode, stem, correct, [w1, w2, w3], explanation,
                    figure_kind=(visual.split(":", 1)[0] if visual else None))
        if visual:
            item["visual_payload"] = visual
        result.append(item)
    return result


def statistics_bias_tasks():
    n = "tr-g06-matematik-note-023"
    return vrows(n, [
        ("comprehension", "Bir yorumun veriyle desteklenip desteklenmediğini incelerken ilk karşılaştırma ne olmalıdır?", "Yorumdaki iddia ile ilgili gözlenen değerler", "Grafiğin renkleri ile başlığı", "Araştırmacının kişisel tercihi ile sonuç", "En büyük sayı ile örneklem adı", "İddianın gerektirdiği ölçüt doğrudan veriyle sınanır.", None),
        ("comprehension", "Bir kategorinin 'en çok tercih edilen' olması ne demektir?", "Sıklığının diğer kategorilerden yüksek olması", "Toplamın mutlaka yarısından fazla olması", "İlk sırada yazılmış olması", "Sıklığının toplamla eşit olması", "En çok ifadesi kategoriler arası sıklık karşılaştırmasıdır.", None),
        ("comprehension", "Örneklem yanlılığı hangi durumda oluşabilir?", "Hedef topluluğun yalnız tek özellikteki küçük bir bölümünden veri alındığında", "Farklı gruplardan dengeli veri alındığında", "Soru tarafsız yazıldığında", "Eksik kayıtlar açıkça belirtildiğinde", "Tek yönlü seçim hedef topluluğun çeşitliliğini yansıtmayabilir.", None),
        ("comprehension", "Dikey ekseni sıfırdan başlatmayan bir sütun grafiği hangi riski taşır?", "Küçük farkları olduğundan büyük gösterebilir.", "Bütün değerleri otomatik olarak eşitler.", "Kategori adlarını sayıya dönüştürür.", "Örneklem büyüklüğünü artırır.", "Kesilmiş eksen görsel yükseklik farkını abartabilir.", None),
        ("comprehension", "Nedensellik iddiası için yalnız iki değişkenin birlikte değişmesi neden yeterli değildir?", "Başka etkenler de iki değişkeni etkiliyor olabilir.", "İki değişken hiçbir zaman ölçülemez.", "Birlikte değişim her zaman rastlantıdır.", "Nedensellik yalnız kategori adlarıyla kanıtlanır.", "İlişki gözlemi tek başına alternatif açıklamaları dışlamaz.", None),
        ("comprehension", "Bir araştırma raporunda örneklem büyüklüğünün verilmesi neyi değerlendirmeye yardım eder?", "Sonucun dayandığı gözlem kapsamını", "Her katılımcının adını", "Grafiğin rengini", "Doğru cevabın konumunu", "Kaç gözlemin kullanıldığı sonucun kapsamını anlamaya yardım eder.", None),
        ("comprehension", "Seçici raporlama ne demektir?", "Yalnız istenen sonucu destekleyen bulguları sunmak", "Bütün bulguları kaynaklarıyla göstermek", "Veriyi iki kez kontrol etmek", "Kişisel bilgileri gizlemek", "Bazı sonuçları gizlemek dağılımın bütününü çarpıtır.", None),
        ("comprehension", "Bir grafikte eşit aralıklı sayılar neden eşit görsel aralıklarla gösterilmelidir?", "Ölçeğin karşılaştırmaları çarpıtmaması için", "Sütun sayısını azaltmak için", "Her değeri en büyük göstermek için", "Kategori adlarını kaldırmak için", "Tutarlı ölçek sayısal farkların doğru algılanmasını sağlar.", None),
        ("application", "Bir sınıfta kulüp tercihleri bilim 11, spor 9, müzik 7'dir. 'Bilim en çok seçilmiştir.' yorumu nasıl değerlendirilir?", "Desteklenir; 11 diğer sıklıklardan büyüktür.", "Desteklenmez; 11 toplamın yarısından azdır.", "Desteklenmez; müzik son sıradadır.", "Karar verilemez; kategori verisi karşılaştırılamaz.", "En çok için yarıdan fazla koşulu değil en yüksek sıklık aranır.", "table:Bilim|11;Spor|9;Müzik|7"),
        ("application", "24 öğrenciden 10'u servisle geliyor. 'Servis kullananlar sınıfın yarısından azdır.' yorumu hangisidir?", "Doğrudur; 10, 12'den küçüktür.", "Yanlıştır; 10, 24'ten büyüktür.", "Doğrudur; 10 öğrencinin tamamıdır.", "Karşılaştırma için öğrenci sayısı kullanılamaz.", "24'ün yarısı 12 ve 10<12'dir.", None),
        ("application", "Bir ankette A seçeneği 18, B seçeneği 17 oy alıyor. Grafiğin ekseni 16'dan başlatılırsa hangi açıklama rapora eklenmelidir?", "Kesilmiş eksenin bir oy farkını görsel olarak büyüttüğü belirtilmelidir.", "A'nın B'nin on sekiz katı olduğu yazılmalıdır.", "B verisi rapordan çıkarılmalıdır.", "Eksen başlangıcı sonuçla ilgisizdir.", "Gerçek fark yalnız bir oydur; görsel oran bunu aşırı gösterebilir.", "chart:18,17"),
        ("application", "Okul yemeği memnuniyeti yalnız yemek kulübü üyelerine soruluyor. Daha güvenilir plan hangisidir?", "Farklı sınıf ve tercih gruplarından öğrencilere aynı tarafsız soruyu yöneltmek", "Yalnız en memnun üyeleri seçmek", "Cevap vermeyenleri memnun saymak", "Soruyu 'Yemekler harika değil mi?' biçiminde sormak", "Çeşitli gruplardan dengeli seçim ve tarafsız soru yanlılığı azaltır.", None),
        ("application", "Bir rapor 'tablet kullanan öğrencilerin notu daha yüksek, o hâlde tablet tek başına başarıyı artırır' diyor. Uygun düzeltme hangisidir?", "Gözlenen ilişkiyi belirtip çalışma süresi ve destek gibi başka etkenleri incelemek gerekir.", "İlişki nedenselliği kesin kanıtlar.", "Not verileri tamamen silinmelidir.", "Yalnız tablet markası nedendir.", "Birlikte değişim alternatif nedenleri dışlamaz.", None),
        ("application", "İki sınıfın etkinlik tercihleri birleştirilecektir: tiyatro 8+11, spor 12+9, müzik 10+7. En yüksek toplam hangisidir?", "Spor, 21", "Tiyatro, 19", "Müzik, 17", "Tiyatro, 8", "Birleşik sıklıklar 19, 21 ve 17'dir.", "table:Tiyatro|8|11;Spor|12|9;Müzik|10|7"),
        ("application", "Bir haber 'ankete katılan 40 kişinin 26'sı bisiklet yolunu destekledi' diyor. Hangi ifade veriye sadıktır?", "Katılımcıların 26'sı desteklemiştir; bütün kent için genelleme örnekleme bağlıdır.", "Kentteki herkes desteklemiştir.", "Destek oranı kesinlikle gelecekte değişmez.", "Katılmayanlar karşı çıkmıştır.", "Bulguyu 40 katılımcıyla sınırlamak verinin kapsamını korur.", None),
        ("application", "Bir sütun grafiğinde 0, 10, 20, 30 etiketleri eşit aralıkta yer almalıdır. Hangi düzenleme doğrudur?", "Her 10 birimlik artışı aynı dikey uzaklıkla göstermek", "20 ile 30 arasını iki kat geniş çizmek", "Sıfır etiketini gizlemek", "En yüksek sütunu resimle büyütmek", "Eşit sayısal aralıklar ortak ölçek gerektirir.", None),
        ("application", "Bir araştırmada 100 yanıtın 12'si boş bırakılmıştır. Raporlama nasıl yapılmalıdır?", "Geçerli yanıt sayısı ve 12 eksik yanıt açıkça belirtilmelidir.", "Boş yanıtların tümü istenen seçeneğe eklenmelidir.", "Eksik kayıtlar gizlenmelidir.", "Toplam örneklem 112 yazılmalıdır.", "Eksiklik miktarı yorumun paydasını ve güvenilirliğini etkileyebilir.", None),
        ("application", "Bir mağaza yalnız sabah müşterilerinin bekleme süresini ölçüp 'gün boyu bekleme az' diyor. En uygun yeni veri toplama planı hangisidir?", "Sabah, öğle ve akşam farklı zaman dilimlerinden ölçüm almak", "Sabah ölçümlerini çoğaltıp diğer saatleri yok saymak", "En kısa süreleri seçmek", "Süre yerine müşteri adlarını toplamak", "Günün farklı yoğunluklarını kapsamak genellemeyi güçlendirir.", None),
        ("application", "Bir raporda 6-A ortalaması 72, 6-B ortalaması 74'tür. '6-B'deki her öğrenci daha başarılıdır' cümlesi nasıl düzeltilmelidir?", "6-B'nin ortalaması iki puan yüksektir; bireysel değerler ayrıca incelenmelidir.", "6-B'deki bütün değerler 74'tür.", "Ortalama bireysel sıralamayı kesin verir.", "İki sınıfın dağılımları aynıdır.", "Grup ortalaması her birey hakkında hüküm kurdurmaz.", None),
        ("analysis", "A grubunda 50 kişinin 30'u, B grubunda 20 kişinin 14'ü bir öneriyi destekliyor. Hangi karşılaştırma doğrudur?", "B'nin destek oranı %70, A'nın %60'tır; B'nin oranı daha yüksektir.", "A'nın sayısı büyük olduğu için oranı da yüksektir.", "İki oran eşittir.", "B'nin oranı %14'tür.", "Farklı grup büyüklüklerinde ham sayılar yerine oranlar karşılaştırılır.", "table:A|30|50;B|14|20"),
        ("analysis", "Bir grafik satışın 100'den 105'e çıktığını gösteriyor ve 'satış beş kat arttı' başlığını kullanıyor. Sorun nedir?", "Artış 5 birim ve %5'tir; beş kat iddiası veriyi çarpıtır.", "105, 100'den küçüktür.", "Yüzde değişim hesaplanamaz.", "Başlık her durumda doğrudur.", "Kat artışı ile mutlak ve yüzdelik artış karıştırılmıştır.", None),
        ("analysis", "Bir ankete internet erişimi olanlar çevrim içi katılabiliyor; erişimi olmayanlar dışarıda kalıyor. Hangi yanlılık olasıdır?", "Kapsama yanlılığı", "Ölçü birimi dönüşümü", "Açı ölçme hatası", "Rastgele sayı üretimi", "Katılım yolu hedef topluluğun bir bölümünü sistematik olarak dışlıyor.", None),
        ("analysis", "İki rapor aynı veriyi kullanıyor. Biri bütün 60 gözlemi, diğeri yalnız en yüksek 10 gözlemi sunuyor. Hangisi daha güvenilir karşılaştırma sağlar?", "Bütün 60 gözlemi ve seçim ölçütünü açıklayan rapor", "Yalnız yüksek 10 değeri sunan rapor", "Kaynağı vermeyen rapor", "Sonucu baştan ilan eden rapor", "Tam veri dağılımı seçici raporlama riskini azaltır.", None),
        ("analysis", "Bir sınıfta ortalama okuma süresi uç bir değer çıkarılınca 28'den 22 dakikaya düşüyor. Hangi sonuç çıkar?", "Uç değer ortalamayı yukarı çekmiştir; silinmeden önce doğruluğu kontrol edilmelidir.", "Uç değer kesinlikle hatalıdır.", "Ortanca da mutlaka altı azalır.", "Bütün öğrenciler 22 dakika okumuştur.", "Ortalama uç değerlerden etkilenir; kaydın geçerliliği ayrıca sınanır.", None),
        ("analysis", "Başarı anketinin sorusu 'Daha iyi olan yeni sistemi destekliyor musunuz?' biçimindedir. Neden sorunludur?", "'Daha iyi' sözü cevabı olumluya yönlendirir.", "Soru çok kısa olduğu için", "Evet-hayır cevabı veri üretmediği için", "Yeni sistem sözcüğü sayı olmadığı için", "Değer yargısı içeren ifade tarafsızlığı bozar.", None),
        ("analysis", "Bir rapor %80 memnuniyet veriyor ancak yalnız 5 kişi yanıtlamıştır. Hangi ek bilgi özellikle önemlidir?", "Örneklemin nasıl seçildiği ve yalnız dört kişinin memnun olduğu", "Grafiğin yazı tipi", "Katılımcıların adları", "Sonucun yuvarlak sayı olması", "Yüksek yüzde küçük ve seçimi belirsiz örneklemde dikkatle yorumlanır.", None),
        ("analysis", "Bir çizgi grafiği kategorik meyve tercihlerini ardışık noktalarla birleştiriyor. Hangi değişiklik daha uygundur?", "Bağımsız kategorilerin sıklıklarını sütun grafiğiyle göstermek", "Noktalar arasına daha çok eğri eklemek", "Meyve adlarını sayıya çevirmek", "Y eksenini kaldırmak", "Kategoriler sürekli sıra oluşturmadığı için bağlantılı çizgi yanıltıcı olabilir.", None),
        ("error-analysis", "Bir öğrenci “En çok seçilen kategori toplamın yarısından fazla olmalıdır.” diyor. Hangi düzeltme doğrudur?", "En çok için diğer her kategoriden yüksek sıklık yeterlidir; salt çoğunluk ayrı bir koşuldur.", "En çok her zaman toplamla eşittir.", "Kategori sıklıkları karşılaştırılamaz.", "En küçük kategori en çok sayılır.", "Tepe kategori ile yarıdan fazla olma kavramları farklıdır.", None),
        ("error-analysis", "Bir öğrenci “Grafiğin ekseni 90'dan başlasa da 94 ile 96 arasındaki fark dört kat görünüyorsa sorun yoktur.” diyor. Hangi düzeltme gerekir?", "Kesilmiş eksen farkı büyütebilir; ölçek açıkça belirtilmeli ve yorum gerçek iki birim farka dayanmalıdır.", "Görsel yükseklik sayısal farkın kendisidir.", "Eksen değerleri okunmamalıdır.", "94 ile 96 eşittir.", "Yorum, görsel alan yerine eksen değerlerini kullanmalıdır.", None),
        ("error-analysis", "Bir öğrenci “Ankete yanıt vermeyenlerin hepsi karşı çıkmıştır.” diyor. Hangi değerlendirme doğrudur?", "Yanıt vermeyenlerin görüşü bilinmez; veri olmadan bir kategoriye atanamazlar.", "Boş yanıt her zaman hayırdır.", "Eksik yanıt sonuçları güçlendirir.", "Yanıt vermeyenler örnekleme eklenmemelidir.", "Eksik gözleme varsayımla değer vermek yanlılık oluşturur.", None),
        ("error-analysis", "Bir öğrenci “İki değişken birlikte arttıysa biri ötekine kesin neden olmuştur.” diyor. Hangi düzeltme gerekir?", "İlişki nedenselliği tek başına kanıtlamaz; üçüncü etkenler ve araştırma düzeni incelenmelidir.", "Birlikte değişen ölçüler ilişkisizdir.", "Neden yalnız büyük sayı olabilir.", "Nedensellik grafik rengiyle belirlenir.", "Alternatif açıklamalar dışlanmadan kesin neden söylenemez.", None),
        ("error-analysis", "Bir öğrenci “Farklı büyüklükte iki grubu yalnız destekleyen kişi sayısıyla karşılaştırırım.” diyor. Doğru yöntem hangisidir?", "Her grupta destekleyenlerin toplam gruba oranını karşılaştırmak", "Yalnız daha büyük grubu seçmek", "Paydaları yok saymak", "İki ham sayıyı toplamak", "Oranlar grup büyüklüğü farkını hesaba katar.", None),
    ])


def probability_tasks():
    n = "tr-g06-matematik-note-024"
    return vrows(n, [
        ("comprehension", "Deneysel olasılık nasıl hesaplanır?", "Olayın gerçekleşme sayısı toplam deneme sayısına bölünür.", "Toplam deneme gerçekleşme sayısına bölünür.", "Gerçekleşmeme sayısı ikiyle çarpılır.", "Yalnız son deneme kullanılır.", "Göreli sıklık gerçekleşme/toplam oranıdır.", None),
        ("comprehension", "Deneme sayısı arttıkça göreli sıklık için genel beklenti hangisidir?", "Uzun dönemde daha kararlı bir değerin çevresinde toplanması", "Her zaman tam 1 olması", "Sürekli sıfıra düşmesi", "Sonucun kesin sırayla tekrar etmesi", "Daha çok gözlem rastgele dalgalanmanın göreli etkisini azaltabilir.", None),
        ("comprehension", "Deneysel olasılığın 0 ile 1 arasında olması neyi gösterir?", "Gerçekleşme sayısının toplam denemeyi aşamayacağını", "Her olayın yarı yarıya olduğunu", "Deneme sayısının sıfır olduğunu", "Olayın kesin gerçekleşeceğini", "0≤başarı sayısı≤toplam deneme olduğundan oran bu aralıktadır.", None),
        ("application", "Bir döndürme deneyinde mavi 24 kez, diğer renkler 36 kez gelmiştir. Mavinin deneysel olasılığı nedir?", "24/60 = 0,4", "36/60 = 0,6", "24/36", "60/24", "Toplam deneme 24+36=60; mavi göreli sıklığı 24/60'tır.", "table:Mavi|24;Diğer|36"),
        ("application", "Bir para 80 kez atıldığında yazı 46 kez gelmiştir. Tura gelmesinin deneysel olasılığı kaçtır?", "34/80", "46/80", "34/46", "80/34", "Tura sayısı 80−46=34, oran 34/80'dir.", "table:Yazı|46;Tura|34"),
        ("application", "Bir olay 50 denemenin 18'inde gerçekleşmiştir. Aynı koşullardaki 200 deneme için yaklaşık kaç gerçekleşme beklenir?", "72", "18", "50", "128", "18/50 oranı 200'e uygulanır: 200×18/50=72.", None),
        ("application", "Aynı olay A deneyinde 12/30, B deneyinde 18/45 oranında gözleniyor. Hangi sonuç doğrudur?", "İki deneyin göreli sıklıkları eşittir.", "A daha büyüktür.", "B daha büyüktür.", "Paydalar farklı olduğu için karşılaştırılamaz.", "Her iki oran da 2/5'tir.", "table:A|12|30;B|18|45"),
        ("application", "Bir torbadan geri koymalı 100 çekişte kırmızı 37 kez gelmiştir. 50 yeni çekiş için en uygun tahmin hangisidir?", "Yaklaşık 18 veya 19 kırmızı", "Kesin 37 kırmızı", "Kesin 50 kırmızı", "Hiç kırmızı gelmez", "37/100×50=18,5 yaklaşık bir beklentidir, garanti değildir.", None),
        ("analysis", "Bir olay ilk 20 denemede 14, sonraki 80 denemede 36 kez gerçekleşiyor. Birleşik deneysel olasılık nedir?", "50/100 = 0,5", "14/20 = 0,7", "36/80 = 0,45", "50/80", "Gerçekleşmeler ve denemeler birlikte toplanır: 50/100.", "table:İlk|14|20;Sonraki|36|80"),
        ("analysis", "İki öğrenci aynı olayı inceliyor: Ece 8/10, Can 72/100 buluyor. Hangisinin tahmini genellikle daha kararlı kabul edilir?", "Can'ınki; daha çok denemeye dayanır.", "Ece'ninki; oranı daha büyüktür.", "İkisi de kesin gerçek olasılıktır.", "Deneme sayısı kararlılığı etkilemez.", "Daha geniş deney, rastgele tekil dalgalanmalardan daha az etkilenir.", None),
        ("analysis", "Bir olayın göreli sıklıkları 20, 100 ve 500 denemede 0,60; 0,53; 0,51'dir. Hangi yorum uygundur?", "Deneme sayısı arttıkça değer yaklaşık 0,5 çevresinde kararlılaşmaktadır.", "Olasılık her denemede kesin 0,60'tır.", "Değerler karşılaştırılamaz.", "500 denemelik sonuç en az bilgi içerir.", "Daha büyük deneylerde oranların 0,5'e yaklaşması kararlılık işaretidir.", "table:20|0,60;100|0,53;500|0,51"),
        ("error-analysis", "Bir öğrenci “26 başarı, 54 başarısızlık varsa olasılık 26/54'tür.” diyor. Hangi düzeltme doğrudur?", "Toplam 80 deneme vardır; deneysel olasılık 26/80'dir.", "Payda yalnız başarısızlık sayısıdır.", "Olasılık 54/26'dır.", "Başarı sayısı kullanılmaz.", "Payda bütün denemeleri içermelidir.", None),
        ("error-analysis", "Bir öğrenci “İlk 50 çekişte mavi 18 geldiyse sonraki 50'de kesin 18 gelir.” diyor. Hangi düzeltme gerekir?", "18 yaklaşık tahmindir; rastgelelik nedeniyle yeni sonuç farklı olabilir.", "Yeni deneyde kesin 32 mavi gelir.", "Deneysel olasılık geleceği belirler.", "Geri koyma sonuçları sıralı yapar.", "Göreli sıklık beklenti sağlar, kesin sayı vermez.", None),
    ])


def roles_rights_tasks():
    n = "tr-g06-sosyal-bilgiler-note-001"
    return vrows(n, [
        ("comprehension", "Bir kişinin ailede çocuk, okulda öğrenci, takımda kaptan olması neyi gösterir?", "Aynı kişinin farklı gruplarda farklı roller üstlenebildiğini", "Her insanın yalnız tek rolü olduğunu", "Rollerin yalnız doğuştan geldiğini", "Hakların rolü ortadan kaldırdığını", "Gruplar değiştikçe kişiden beklenen davranış ve görevler değişebilir.", None),
        ("comprehension", "Hak ile sorumluluk arasındaki ilişki hangisidir?", "Haklardan yararlanırken başkalarının haklarını gözeten görevler de vardır.", "Her hak yalnız bir kişiye aittir.", "Sorumluluklar hakları tamamen kaldırır.", "Hak ve sorumluluk birbirinden bütünüyle bağımsızdır.", "Toplumsal yaşamda hak kullanımı ortak kurallara ve sorumluluklara bağlıdır.", None),
        ("comprehension", "Zaman içinde değişebilen role örnek hangisidir?", "Öğrencinin sınıf temsilcisi seçilmesi", "Bir kişinin doğduğu ülke", "İnsanın yaşama hakkı", "Çocuğun insan olması", "Temsilcilik seçimle kazanılan ve süresi değişebilen bir roldür.", None),
        ("comprehension", "Bir gruba üyelikte rol neyi ifade eder?", "Grup içinde kişiden beklenen davranış ve görevleri", "Kişinin bütün özel bilgilerini", "Yalnız fiziksel görünüşünü", "Değişmeyen tek kimliğini", "Rol, belirli toplumsal bağlamdaki beklentiler bütünüdür.", None),
        ("application", "Sınıf kitaplığından kitap alma hakkını kullanan öğrencinin uygun sorumluluğu hangisidir?", "Kitabı zamanında ve zarar vermeden geri getirmek", "Kitabı istediği kadar saklamak", "Başkasının kaydını silmek", "Kitapları izinsiz eve götürmek", "Ortak kaynaktan yararlanma hakkı, kaynağı koruma ve iade sorumluluğuyla dengelenir.", None),
        ("application", "Takım kaptanı seçilen Eylül'ün rolünde hangi değişim beklenir?", "Kendi oyununa ek olarak iletişim ve takım düzenine katkı sorumluluğu üstlenmesi", "Bütün takım arkadaşlarının haklarını kaldırması", "Kurallara uymaktan muaf olması", "Takımın tek oyuncusu hâline gelmesi", "Yeni rol ek koordinasyon görevi getirir, diğer üyelerin haklarını kaldırmaz.", None),
        ("application", "Bir öğrenci okul meclisinde görüş bildirme hakkını kullanacaktır. En uygun davranış hangisidir?", "Gerekçesini açıklayıp başkalarını dinlemek", "Konuşanları susturmak", "Doğrulanmamış suçlamalar yapmak", "Oylama sonucunu zorla değiştirmek", "Katılım hakkı saygılı iletişim ve ortak kurallarla kullanılır.", None),
        ("application", "Evde alışveriş listesine katkı sunan çocuğun hem hakkını hem sorumluluğunu gösteren seçenek hangisidir?", "İhtiyacını söylemek ve aile bütçesini gözetmek", "Bütün kararları tek başına vermek", "Diğer aile üyelerini dinlememek", "İstediği ürünü gizlice almak", "Görüş bildirme hakkı ortak kaynakları dikkate alma sorumluluğuyla birlikte işler.", None),
        ("application", "Bir kulüpte görev dağılımı değiştiğinde eski sekreter yeni etkinlik sorumlusu oluyor. Bu durum nasıl açıklanır?", "Grup içindeki rolü zamanla değişmiştir.", "Temel hakları sona ermiştir.", "Artık hiçbir gruba ait değildir.", "Roller hiçbir koşulda değişmez.", "Görev değişikliği grup üyeliği sürerken rol beklentisini değiştirebilir.", "table:Önce|Sekreter;Sonra|Etkinlik sorumlusu"),
        ("analysis", "Mert hem öğrenci hem kardeştir. Ders saatinde ödevini, evde küçük kardeşinin güvenliğini gözetiyor. Hangi çıkarım uygundur?", "Rolleri farklı bağlamlarda farklı sorumluluklar doğurur.", "İki rol birbiriyle mutlaka çatışır.", "Kardeş rolü eğitim hakkını kaldırır.", "Öğrenci rolü evde de tek roldür.", "Aynı kişi bağlama göre birden çok rolü dengeler.", None),
        ("analysis", "Bir öğrenci 'oyun alanını kullanma hakkım var' diyerek sırayı bozuyor. Hangi değerlendirme doğrudur?", "Hakkını kullanırken diğer öğrencilerin eşit yararlanma hakkını ihlal etmektedir.", "Hak sahibi olmak bütün kuralları kaldırır.", "Sıra yalnız sorumluluğu olmayanlar içindir.", "Oyun hakkı yalnız ilk gelene aittir.", "Haklar başkalarının aynı hakkıyla ve ortak düzenle sınırlanır.", None),
        ("analysis", "Bir görev gönüllü alınmış olsa bile tamamlanmadığında grup çalışması aksıyor. Bu durum neyi gösterir?", "Üstlenilen rolün başkalarını etkileyen sorumlulukları bulunduğunu", "Gönüllü görevlerin sorumluluk doğurmadığını", "Grubun yalnız liderden oluştuğunu", "Hakların görevle ilişkisi olmadığını", "Rol beklentisinin yerine getirilmesi ortak sonuca katkı sağlar.", None),
        ("error-analysis", "Bir öğrenci “Rolüm değişirse temel haklarım da yok olur.” diyor. Hangi düzeltme doğrudur?", "Roller değişebilir; temel haklar insan olmaktan kaynaklanır ve rol değişimiyle ortadan kalkmaz.", "Her yeni rol bütün eski hakları siler.", "Haklar yalnız yöneticilere aittir.", "Rol ile hak aynı kavramdır.", "Toplumsal rol ile evrensel temel haklar farklı düzlemlerdedir.", None),
        ("error-analysis", "Bir öğrenci “Sorumluluk yalnız yetişkinlerin görevidir.” diyor. Hangi değerlendirme uygundur?", "Çocukların yaşına ve rollerine uygun okul, aile ve çevre sorumlulukları vardır.", "Çocukların hiçbir ortak görevi yoktur.", "Sorumluluk hak kullanımını yasaklar.", "Yalnız ücretli işler sorumluluktur.", "Sorumluluklar yaşa ve role göre farklılaşır ama çocuklukta da bulunur.", None),
    ])


def culture_unity_tasks():
    n = "tr-g06-sosyal-bilgiler-note-002"
    return vrows(n, [
        ("comprehension", "Ortak dil, tarih ve geleneklerin toplumsal birliğe katkısı hangisidir?", "Aidiyet ve ortak hafıza oluşturmaya yardım etmeleri", "Bütün bireysel farklılıkları yok etmeleri", "Yalnız ekonomik kazanç sağlamaları", "Toplumu iletişimsiz bırakmaları", "Paylaşılan kültürel unsurlar ortak kimlik ve iletişim zemini sağlar.", None),
        ("comprehension", "Kültürel miras neyi kapsar?", "Geçmişten devralınan somut ve somut olmayan değerleri", "Yalnız yeni üretilen teknolojiyi", "Sadece kişisel eşyaları", "Hiç değişmeyen tek bir davranışı", "Yapılar, eserler, anlatılar, müzik ve gelenekler kültürel mirasa dâhildir.", None),
        ("comprehension", "Millî bayramların ortaklaşa kutlanması hangi işlevi güçlendirebilir?", "Ortak tarih bilinci ve dayanışmayı", "Bireylerin birbirinden kopmasını", "Yerel kültürlerin yasaklanmasını", "Geçmişin unutulmasını", "Ortak anma ve kutlamalar paylaşılan değerleri görünür kılar.", None),
        ("application", "Mahallede farklı yörelerden halk oyunları festivali düzenleniyor. Birliği güçlendiren yaklaşım hangisidir?", "Her oyunun kaynağını tanıtıp bütün gruplara eşit katılım alanı açmak", "Yalnız tek yörenin oyununu doğru saymak", "Diğer gelenekleri küçümsemek", "Katılımcıları kökenine göre ayırmak", "Çeşitliliği tanıma ve eşit katılım ortak aidiyeti güçlendirir.", None),
        ("application", "Tarihî bir çeşmenin korunması için en uygun çalışma hangisidir?", "Uzman görüşüyle belgeleme, bakım ve bilinçlendirme yapmak", "Kitabesini silip yeni yazı yazmak", "Taşlarını hatıra olarak dağıtmak", "Yapıyı kayıtsız biçimde boyamak", "Kültürel varlık özgün özellikleri belgelenerek korunur.", None),
        ("application", "Bir sınıf ortak yemek kültürünü araştırıyor. Güvenilir yöntem hangisidir?", "Farklı ailelerden sözlü tarih görüşmeleri yapıp kaynakları karşılaştırmak", "Tek bir sosyal medya paylaşımını bütün ülkeye genellemek", "Yalnız kendi ailesini doğru kabul etmek", "Kaynak belirtmeden tarif kopyalamak", "Çeşitli tanıklıkları karşılaştırmak kültürel çeşitliliği daha iyi yansıtır.", None),
        ("application", "Yerel bir türkünün okul etkinliğinde kullanılması için hangi yaklaşım saygılıdır?", "Kaynağını ve yöresini belirtip uygun biçimde icra etmek", "Eseri anonim sanıp sahipliğini gizlemek", "Sözlerini alay amacıyla değiştirmek", "Yörenin adını kaldırmak", "Kaynak ve bağlamı belirtmek kültürel emeğe saygı gösterir.", None),
        ("application", "Afet sonrası farklı şehirlerden insanların ortak yardım kampanyasına katılması hangi değeri örnekler?", "Dayanışma", "Ayrımcılık", "Kayıtsızlık", "Yalıtılmışlık", "Ortak ihtiyaç için gönüllü ve düzenli katkı toplumsal dayanışmadır.", None),
        ("analysis", "Bir kentte hem geleneksel el sanatları hem çağdaş tasarımlar sergileniyor. Hangi yorum uygundur?", "Kültür geçmişten beslenirken yeni üretimlerle değişip zenginleşebilir.", "Kültür yalnız geçmişte kalır.", "Yeni tasarım kültürel mirası otomatik olarak yok eder.", "İki tür eser birlikte bulunamaz.", "Kültür süreklilik ve değişimi aynı anda taşıyabilir.", None),
        ("analysis", "Ortak bir bayram farklı bölgelerde değişik yemeklerle kutlanıyor. Bu durum neyi gösterir?", "Ortak değerlerin yerel çeşitlilikle birlikte yaşatılabildiğini", "Bölgelerin hiçbir ortak değeri olmadığını", "Yalnız bir kutlama biçiminin millî olduğunu", "Çeşitliliğin birliği mutlaka bozduğunu", "Ortak anlam farklı yerel uygulamalarla ifade edilebilir.", None),
        ("analysis", "Bir proje yalnız çoğunluk kültürünü gösterip küçük grupların katkılarını dışlıyor. Birlik açısından temel sorun nedir?", "Kapsayıcılık eksikliği bazı bireylerin aidiyetini zayıflatabilir.", "Çok kaynak kullanılması", "Ortak tarih anlatılması", "Etkinliğin okulda yapılması", "Birlik, farklı katkıların görünür ve saygın olmasını gerektirir.", None),
        ("analysis", "İki kuşak aynı geleneği farklı biçimde uyguluyor fakat temel anlamı koruyor. Hangi çıkarım desteklenir?", "Kültürel aktarım uyarlanarak sürebilir.", "Gelenek bütünüyle sona ermiştir.", "Kültür değişemez.", "Kuşaklar arasında iletişim yoktur.", "Biçim değişikliği temel değerin aktarılmasına engel olmayabilir.", None),
        ("error-analysis", "Bir öğrenci “Toplumsal birlik için herkesin bütün kültürel özellikleri aynı olmalıdır.” diyor. Hangi düzeltme doğrudur?", "Birlik ortak değerlerle güçlenebilir; kültürel çeşitlilik saygıyla birlikte var olabilir.", "Farklılıklar mutlaka kaldırılmalıdır.", "Birlik yalnız tek yemekle sağlanır.", "Yerel kültür ortak aidiyeti engeller.", "Birlik aynılık değil, ortak zeminde kapsayıcı dayanışmadır.", None),
        ("error-analysis", "Bir öğrenci “Kültürel mirası korumak onu hiç kullanmamak demektir.” diyor. Hangi değerlendirme uygundur?", "Koruma, uygun kullanım, bakım, belgeleme ve gelecek kuşaklara aktarmayı birlikte kapsar.", "Bütün eserler kapatılmalıdır.", "Miras yalnız fotoğrafla korunur.", "Kullanılan her gelenek yok olur.", "Sürdürülebilir yaşatma kontrollü kullanım ve korumayı dengeler.", None),
    ])


def social_problem_tasks():
    n = "tr-g06-sosyal-bilgiler-note-003"
    return vrows(n, [
        ("comprehension", "Toplumsal sorunu tanımlarken hangi bilgi gereklidir?", "Sorundan kimlerin, nerede ve nasıl etkilendiği", "Yalnız kişisel söylenti", "Çözüm seçilmeden önce suçlu ilanı", "Sorunun görmezden gelinmesi", "Kapsam ve etki belirlenmeden uygun çözüm değerlendirilemez.", None),
        ("comprehension", "Müzakere neyi gerektirir?", "Farklı görüşleri gerekçeleriyle dinleyip ortak seçenekleri değerlendirmeyi", "Yalnız en yüksek sesin karar vermesini", "Kanıtları dışlamayı", "Karşı tarafı susturmayı", "Müzakere karşılıklı dinleme, gerekçelendirme ve uzlaşma arayışıdır.", None),
        ("comprehension", "Bir çözüm önerisi değerlendirilirken hangi ölçüt birlikte kullanılmalıdır?", "Uygulanabilirlik, adalet ve beklenen etki", "Yalnız sloganın uzunluğu", "Öneriyi sunanın yaşı", "Sosyal medyadaki beğeni rengi", "İyi çözüm kaynakları, hakları ve sonuçları birlikte gözetir.", None),
        ("comprehension", "Sorunun nedenleri ile belirtileri arasındaki fark nedir?", "Nedenler sorunu doğuran etkenler, belirtiler gözlenen sonuçlardır.", "İkisi her zaman aynı sözcüktür.", "Belirti çözümün kendisidir.", "Neden yalnız sonuçtan sonra oluşur.", "Kalıcı çözüm için görünür sonuçların arkasındaki etkenler incelenir.", None),
        ("application", "Okul girişinde bisikletler geçişi engelliyor. İlk uygun adım hangisidir?", "Yoğun saatleri ve kullanıcı ihtiyaçlarını gözleyip sorunun kapsamını belirlemek", "Bütün bisikletleri habersiz kaldırmak", "Bisiklete gelenleri suçlamak", "Geçiş sorununu yok saymak", "Veri toplama sorunun boyutunu ve paydaşlarını açıklar.", None),
        ("application", "Mahalle parkında gürültü şikâyeti için kapsayıcı toplantı nasıl düzenlenir?", "Çocuklar, çevre sakinleri ve yetkililere eşit söz hakkı verip zaman ve kullanım verilerini paylaşmak", "Yalnız tek şikâyetçiyi dinlemek", "Çocukları toplantıdan dışlamak", "Kanıt sunmayı yasaklamak", "Bütün paydaşların görüşü ve ortak veri dengeli çözüm sağlar.", None),
        ("application", "Su israfını azaltma önerilerinden hangisi ölçülebilir?", "Kaçakları onarıp aylık tüketimi önceki dönemle karşılaştırmak", "Herkese daha dikkatli olun demek", "Sayaçları kaldırmak", "Tüketim verisini gizlemek", "Somut müdahale ve önce-sonra ölçümü etkinin değerlendirilmesini sağlar.", None),
        ("application", "Bir çözüm tekerlekli sandalye kullananların erişimini azaltıyorsa ne yapılmalıdır?", "Erişilebilirlik etkisi incelenip öneri bütün kullanıcıların hakkını koruyacak biçimde değiştirilmelidir.", "Azınlıkta oldukları için etki yok sayılmalıdır.", "Yalnız maliyet dikkate alınmalıdır.", "Sorun çözülmüş sayılmalıdır.", "Çözüm bir sorunu giderirken yeni hak ihlali üretmemelidir.", None),
        ("analysis", "Çöp sorunu için A önerisi daha çok kutu, B önerisi atık eğitimi sunuyor. Veriler kutuların dolduğunu ve yanlış ayrıştırma yapıldığını gösteriyor. En güçlü plan hangisidir?", "Kutu kapasitesiyle birlikte ayrıştırma eğitimini birleştirmek", "Yalnız afiş asmak", "Bütün kutuları kaldırmak", "Verileri kullanmadan kura çekmek", "İki farklı neden birlikte bulunduğundan birleşik müdahale uygundur.", None),
        ("analysis", "Bir öneri ucuz fakat sorundan etkilenenlerin yarısına ulaşmıyor; diğeri biraz pahalı ve herkese erişiyor. Hangi ek değerlendirme önemlidir?", "Bütçeyle birlikte kapsayıcılık ve uzun dönem etkisi", "Yalnız önerinin adı", "Sunumun rengi", "Öneriyi kimin önce söylediği", "Maliyet tek ölçüt değildir; adalet ve etki de tartılmalıdır.", None),
        ("analysis", "Toplantıda çoğunluk hemen karar vermek, azınlık güvenlik riskini incelemek istiyor. Demokratik yaklaşım hangisidir?", "Risk kanıtlarını dinleyip gerekirse öneriyi güvenli hâle getirdikten sonra karar vermek", "Azınlığın sözünü kesmek", "Oylamayı gizlemek", "Kanıtı çoğunluk sayısıyla geçersiz saymak", "Çoğunluk kararı temel hak ve güvenlik gerekçelerini yok saymamalıdır.", None),
        ("analysis", "Bir pilot uygulama beklenen sonucu vermedi. En uygun sonraki adım hangisidir?", "Sonuçları inceleyip varsayımları ve uygulama adımlarını değiştirerek yeniden denemek", "Başarılı ilan etmek", "Ölçümleri silmek", "Aynı yöntemi neden aramadan sonsuza dek sürdürmek", "Çözüm süreci kanıta göre gözden geçirilebilir.", None),
        ("error-analysis", "Bir öğrenci “Toplumsal sorunda ilk akla gelen çözüm mutlaka en iyisidir.” diyor. Hangi düzeltme doğrudur?", "Birden çok seçenek etki, hak, maliyet ve uygulanabilirlik açısından karşılaştırılmalıdır.", "İlk fikir kanıt gerektirmez.", "Yalnız pahalı çözüm iyidir.", "Müzakere zaman kaybıdır.", "Alternatifleri ölçütlerle değerlendirmek beklenmeyen zararları azaltır.", None),
        ("error-analysis", "Bir öğrenci “Çoğunluk kabul ederse çözüm hiç kimsenin hakkını ihlal edemez.” diyor. Hangi değerlendirme uygundur?", "Çoğunluk kararı da temel haklar ve eşitlik açısından denetlenmelidir.", "Çoğunluk bütün hakları kaldırır.", "Azınlıkların görüşü veri değildir.", "Oylama yapılınca sonuçlar incelenmez.", "Demokratik karar yalnız sayı değil hak güvencesi de içerir.", None),
    ])


def location_tasks():
    n = "tr-g06-sosyal-bilgiler-note-004"
    return vrows(n, [
        ("comprehension", "Mutlak konum hangi bilgilerle belirlenir?", "Enlem ve boylam dereceleriyle", "Komşu ülkeler ve ulaşım yollarıyla", "Nüfus ve ekonomiyle", "Dağların adlarıyla", "Koordinat sistemi yeryüzündeki mutlak konumu verir.", "coordinate"),
        ("comprehension", "Göreceli konum neyi açıklar?", "Bir yerin çevresindeki doğal ve beşerî unsurlara göre yerini", "Yalnız enlem derecesini", "Yalnız boylam derecesini", "Değişmeyen tek koordinatı", "Denizler, komşular ve yollar göreceli konum ilişkileridir.", None),
        ("comprehension", "Ekvator'a paralel uzanan hayalî çemberlere ne denir?", "Paralel", "Meridyen", "Kutup", "Ölçek", "Paraleller enlem değerlerini belirler.", "coordinate"),
        ("application", "40° kuzey, 30° doğu koordinatları hangi yarımküreleri gösterir?", "Kuzey ve Doğu yarımküreleri", "Güney ve Batı yarımküreleri", "Kuzey ve Batı yarımküreleri", "Güney ve Doğu yarımküreleri", "Kuzey enlemi Ekvator'un, doğu boylamı başlangıç meridyeninin doğusundadır.", "coordinate"),
        ("application", "Türkiye'nin üç tarafının denizlerle çevrili olması hangi konum türüne örnektir?", "Göreceli konum", "Mutlak konum", "Yalnız enlem", "Yalnız boylam", "Denizlere göre yer, çevresel bir ilişkidir.", None),
        ("application", "İki nokta aynı meridyen üzerindeyse hangi değerleri aynıdır?", "Boylamları", "Enlemleri", "Yükseltileri", "Denize uzaklıkları", "Meridyenler aynı boylam değerindeki noktaları birleştirir.", "coordinate"),
        ("application", "Bir ülkenin Asya ile Avrupa arasındaki ulaşım yolları üzerinde bulunması hangi sonucu destekler?", "Kıtalar arası ulaşım ve ticaret etkileşiminin önem kazanmasını", "Bütün iklimlerin aynı olmasını", "Koordinatlarının değişmesini", "Denizlerin ortadan kalkmasını", "Göreceli konum ulaşım ve ekonomik bağlantıları etkileyebilir.", None),
        ("application", "Atlas kullanırken 36°–42° kuzey ifadesi neyi gösterir?", "Ülkenin kuzey yarımküredeki enlem aralığını", "Doğu-batı boylam aralığını", "Yükselti basamaklarını", "Nüfus dağılımını", "Kuzey dereceleri enlem konumunu belirtir.", "table:Enlem|36°–42° Kuzey;Boylam|26°–45° Doğu"),
        ("analysis", "A noktası 38°K 27°D, B noktası 41°K 27°D'dir. Hangisi daha kuzeydedir?", "B noktası", "A noktası", "İkisi aynı enlemdedir.", "Boylam bilinmeden söylenemez.", "Kuzey enlem derecesi daha büyük olan B, Ekvator'dan daha kuzeydedir.", "coordinate"),
        ("analysis", "Bir limanın koordinatları değişmezken yeni demir yolu açılıyor. Hangi konum özelliği değişmiştir?", "Göreceli ulaşım konumu", "Mutlak enlem ve boylam", "Bulunduğu yarımküre", "Ekvator'a açısal uzaklığı", "Yeni bağlantı çevresel ilişkiyi değiştirir, koordinatı değiştirmez.", None),
        ("analysis", "Türkiye'nin orta kuşakta olması ile mevsimlerin belirgin yaşanması arasında hangi bağ kurulabilir?", "Mutlak enlem konumu iklim ve mevsim özelliklerini etkiler.", "Göreceli konum enlemi yok eder.", "Boylam tek başına sıcaklığı belirler.", "Kıtaların adı mevsimleri oluşturur.", "Güneş ışınlarının geliş açısı enleme göre değişir.", None),
        ("error-analysis", "Bir öğrenci “Komşu ülkeler bir yerin mutlak konumunu gösterir.” diyor. Hangi düzeltme doğrudur?", "Komşular göreceli konumu; enlem ve boylam mutlak konumu gösterir.", "Komşular enlem derecesidir.", "Mutlak konum yalnız nüfustur.", "Göreceli konum koordinatla sınırlıdır.", "İlişkisel çevre bilgisi ile koordinat bilgisi ayrılmalıdır.", None),
        ("error-analysis", "Bir öğrenci “Aynı paraleldeki bütün yerlerin boylamı da aynıdır.” diyor. Hangi değerlendirme doğrudur?", "Aynı paralelde enlem aynıdır; boylamlar farklı olabilir.", "Paralel boylamı sabitler.", "Enlem ve boylam her zaman eşittir.", "Paraleller kutupları birleştirir.", "Paraleller doğu-batı yönünde uzanır ve birçok meridyeni keser.", "coordinate"),
    ])


TASK_BUILDERS = [statistics_bias_tasks, probability_tasks, roles_rights_tasks,
                 culture_unity_tasks, social_problem_tasks, location_tasks]


def _label(labels: dict[str, str], qid: str, suffix: str, value: str) -> str:
    key = f"figure.{qid}.{suffix}"
    labels[key] = value
    return key


def table_figure(qid: str, labels: dict[str, str], payload: str) -> dict[str, Any]:
    raw_rows = [segment.split("|") for segment in payload.split(":", 1)[1].split(";")]
    width = max(len(row) for row in raw_rows)
    headers = [_label(labels, qid, f"h{i}", value)
               for i, value in enumerate(["Grup", "Gerçekleşme / değer", "Toplam"][:width])]
    rows_out = []
    for raw in raw_rows:
        cells = raw + ["—"] * (width - len(raw))
        rows_out.append([{"v": value} for value in cells])
    alt = _label(labels, qid, "alt", "Soruda karşılaştırılan grup, sıklık ve toplam değerlerini satırlar hâlinde gösteren tablo; yorum veya doğru cevap verilmemiştir.")
    return {"kind": "table", "headerKeys": headers, "rows": rows_out, "altTextKey": alt}


def chart_figure(qid: str, labels: dict[str, str], payload: str) -> dict[str, Any]:
    values = [float(value.replace(",", ".")) for value in payload.split(":", 1)[1].split(",")]
    category_keys = [_label(labels, qid, f"c{i}", f"Grup {chr(65+i)}") for i in range(len(values))]
    x = _label(labels, qid, "x", "Gruplar")
    y = _label(labels, qid, "y", "Gözlenen değer")
    alt = _label(labels, qid, "alt", "Ortak sıfır tabanından yükselen iki sütunda gözlenen değerleri gösteren grafik; yorum veya doğru cevap belirtilmemiştir.")
    return {"kind": "chart", "style": "bar", "categoryKeys": category_keys,
            "values": values, "axisKeys": {"x": x, "y": y}, "altTextKey": alt}


def coordinate_figure(qid: str, labels: dict[str, str]) -> dict[str, Any]:
    local = int(qid.rsplit("q", 1)[1])
    points = []
    if local == 94:
        points = [[30, 40]]
    elif local in {96, 99}:
        points = [[27, 38], [27, 41]] if local == 99 else [[30, 36], [30, 42]]
    point_labels = {}
    for index, name in enumerate("AB"[:len(points)]):
        point_labels[str(index)] = _label(labels, qid, f"p{index}", name)
    alt = _label(labels, qid, "alt", "Enlem ve boylam eksenleri üzerinde soruda verilen noktaları gösteren sınır içermeyen koordinat şeması.")
    figure: dict[str, Any] = {"kind": "coordinate", "xRange": [20, 50], "yRange": [30, 50],
                              "points": points, "altTextKey": alt}
    if point_labels:
        figure["labels"] = point_labels
    return figure


def apply_visual(row: dict[str, Any], item: dict[str, Any], labels: dict[str, str]) -> None:
    payload = item.get("visual_payload")
    if not payload:
        return
    qid = str(row["id"])
    kind = payload.split(":", 1)[0]
    if kind == "table":
        figure = table_figure(qid, labels, payload)
        word = "tabloyu"
    elif kind == "chart":
        figure = chart_figure(qid, labels, payload)
        word = "grafiği"
    elif kind == "coordinate":
        figure = coordinate_figure(qid, labels)
        word = "görseli"
    else:
        raise AssertionError(f"unsupported visual payload: {payload}")
    row["figure"] = figure
    row["question"] = f"Aşağıdaki {word} inceleyiniz. {row['question']}"
    row["visualRequirement"] = "required"
    row["visualNeed"] = {"level": "required", "role": "evidence",
                         "rationale": "Soru, nicel veya konumsal ilişkileri yapılandırılmış görsel kanıtla karşılaştırmayı gerektirir.",
                         "acceptableKinds": [figure["kind"]],
                         "evidenceDimensions": ["değer veya koordinat", "karşılaştırma veya konum"]}


def verify_math_facts() -> None:
    assert 10 < 24 / 2 and 18 + 17 == 35 and [8 + 11, 12 + 9, 10 + 7] == [19, 21, 17]
    assert 30 / 50 == .6 and 14 / 20 == .7 and abs(105 / 100 - 1 - .05) < 1e-12
    assert 24 / 60 == .4 and 80 - 46 == 34 and 200 * 18 / 50 == 72
    assert 12 / 30 == 18 / 45 == .4 and 50 * 37 / 100 == 18.5
    assert (14 + 36) / (20 + 80) == .5 and 26 / (26 + 54) == 26 / 80


def main() -> int:
    verify_math_facts()
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1400:
        raise RuntimeError("validated first fourteen batches must exist before batch 15")
    math_notes = read_notes_only(MATH_SOURCE)
    social_notes = read_notes_only(SOCIAL_SOURCE)
    notes = {**math_notes, **social_notes}
    tasks = [item for builder in TASK_BUILDERS for item in builder()]
    if len(tasks) != 100:
        raise AssertionError(f"batch 15 must contain 100 tasks, got {len(tasks)}")
    expected_modes = {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
    if Counter(item["mode"] for item in tasks) != expected_modes:
        raise AssertionError(Counter(item["mode"] for item in tasks))
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    rows_out = []
    for local, item in enumerate(tasks, 1):
        row = make_record(local, item, notes[item["note"]], batch=15, number_base=1400)
        apply_visual(row, item, labels)
        rows_out.append(row)
    if Counter(row["subject"] for row in rows_out) != Counter({"Matematik": 45, "Sosyal Bilgiler": 55}):
        raise AssertionError(Counter(row["subject"] for row in rows_out))
    if Counter(row["correctIndex"] for row in rows_out) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer positions are not exactly balanced")
    if sum(bool(row.get("figure")) for row in rows_out) != 17:
        raise AssertionError("batch 15 must contain exactly 17 required figures")
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":"))
                                 for row in existing + rows_out) + "\n", encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
    print(json.dumps({"batch": 15, "questions": 100, "mathematics": 45,
                      "socialStudies": 55, "figures": 17, "total": 1500,
                      "modes": dict(Counter(item["mode"] for item in tasks)),
                      "sourceQuestionReads": 0, "figureSpec": "1.3.0"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
