#!/usr/bin/env python3
"""Append 100 independently authored Grade 6 Turkish questions (batch 18)."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

from author_grade6_bilisim_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade6_fen_batch07 import task
from author_grade6_fen_english_batch10 import make_record
from author_grade6_mixed_batch03 import read_notes_only

TURKISH_SOURCE = Path("turkiye/6-sinif/turkce/turkce-tum.jsonl")


def rows(note: str, values):
    return [task(note, mode, stem, correct, [w1, w2, w3], explanation)
            for mode, stem, correct, w1, w2, w3, explanation in values]


def listening_strategy_tasks():
    n = "tr-g06-turkce-note-002"
    return rows(n, [
        ("comprehension", "Bir konuşmanın ana düşüncesini bulmak isteyen dinleyici için uygun strateji hangisidir?", "Tekrarlanan düşünceleri ve konuşmanın sonuç bölümünü izlemek", "Her sözcüğü ayrı ayrı yazmak", "Yalnız ilk cümleyi dinlemek", "Konuşmacının kıyafetine odaklanmak", "Ana düşünceyi belirlemede vurgu, tekrar ve sonuç ifadeleri yol gösterir."),
        ("comprehension", "Not alarak dinlemenin temel amacı nedir?", "Önemli bilgileri seçip düzenli biçimde kaydetmek", "Konuşmanın tamamını sözcüğü sözcüğüne yazmak", "Dinlemeyi bırakıp yalnız yazmak", "Her ayrıntıyı eşit önemde görmek", "Etkili not, anahtar bilgi ve ilişkileri kısa biçimde kaydeder."),
        ("comprehension", "Tahmin ederek dinleme stratejisinde dinleyici ne yapar?", "Başlık ve önceki bilgilerden sonraki içeriğe ilişkin beklenti kurup bunu sınar.", "Konuşmayı dinlemeden sonucu doğru sayar.", "Bilmediği her sözcüğü atlar.", "Yalnız ses yüksekliğini ölçer.", "Tahmin geçici bir beklentidir ve yeni bilgiyle doğrulanır ya da değiştirilir."),
        ("application", "Bir bilim söyleşisinde neden-sonuç ilişkilerini izleyecek öğrenci nasıl not almalıdır?", "Nedenleri ve sonuçları oklarla bağlayan kısa bir şema kurmalıdır.", "Konuşmacının her duraklamasını yazmalıdır.", "Yalnız tarihleri daire içine almalıdır.", "Not almadan sonunda hatırlamaya çalışmalıdır.", "İlişki odaklı şema, neden ile sonucu görünür kılar."),
        ("application", "Öğretmen deney yönergesini bir kez okuyacaktır. Öğrenci hangi stratejiyi kullanmalıdır?", "İşlem basamaklarını sıra numarasıyla kaydetmek", "Yalnız son basamağı yazmak", "Araç adlarını önemsememek", "Yönerge bitmeden uygulamaya başlamak", "Sıralı not, yönergedeki işlem düzeninin korunmasını sağlar."),
        ("application", "Bir öykü dinlerken karakterlerin değişimini incelemek için hangi yöntem uygundur?", "Başlangıç ve sonuçtaki davranışları karşılaştıran iki sütunlu not tutmak", "Yalnız mekân adlarını yazmak", "Her cümledeki harfleri saymak", "Sonunu dinlemeden karar vermek", "Karşılaştırmalı not karakter gelişimini kanıtlarla izletir."),
        ("analysis", "Öğrenci bir tartışmada yalnız kendi görüşünü destekleyen cümleleri not ediyor. Bu stratejinin sorunu nedir?", "Karşıt gerekçeleri dışlayarak tartışmayı yanlı değerlendirmesine yol açması", "Notlarının çok kısa olması", "Konuşmacı adlarını yazması", "Kâğıdı ikiye bölmesi", "Tartışmayı anlamak için farklı iddia ve kanıtlar birlikte kaydedilmelidir."),
        ("analysis", "Bir dinleyici her bilinmeyen sözcükte kaydı durduruyor ve bütünlüğü kaçırıyor. En uygun uyarlama hangisidir?", "Önce bağlamdan geçici anlam kurup kritik sözcükleri sonradan doğrulamak", "Bütün sözcükleri yok saymak", "Kaydı baştan sona sürekli durdurmak", "Yalnız sözlüğü dinlemek", "Akışı koruyup seçici doğrulama yapmak anlama ile sözcük öğrenimini dengeler."),
        ("analysis", "Aynı öğrenci haber bülteninde ayrıntılı not, şiir dinletisinde ise duygu ve imgeleri işaretliyor. Bu neyi gösterir?", "Stratejisini metnin türü ve dinleme amacına göre değiştirdiğini", "Tutarsız dinlediğini", "Şiirde ana düşünce olmadığını", "Haberde duygu bulunmadığını", "Dinleme yöntemi her materyalde aynı olmak zorunda değildir."),
        ("error-analysis", "Bir öğrenci “Etkili dinleme için konuşulan her şeyi eksiksiz yazmalıyım.” diyor. Hangi düzeltme doğrudur?", "Anahtar fikirleri seçmek ve ilişkileri kısa notlarla göstermek daha etkilidir.", "Not almak dinlemeyi tamamen bırakmaktır.", "Yalnız ilk cümle yazılmalıdır.", "Her sözcük aynı önemdedir.", "Sözcüğü sözcüğüne yazma çabası anlamayı ve seçmeyi zorlaştırabilir."),
        ("error-analysis", "Bir öğrenci “Başlığa bakarak yaptığım tahmin kesin doğrudur.” diyor. Hangi değerlendirme gerekir?", "Tahmin dinleme sırasında yeni kanıtlarla sınanmalı ve gerekirse değiştirilmelidir.", "Başlık bütün ayrıntıları kanıtlar.", "Tahmin değiştirilemez.", "Yeni bilgi tahmini etkilemez.", "Tahmin bir anlama aracı, kesin hüküm değildir."),
    ])


def listening_vocabulary_inference_tasks():
    n = "tr-g06-turkce-note-003"
    return rows(n, [
        ("comprehension", "Dinlerken bilinmeyen bir sözcüğün anlamını tahmin etmede en güçlü ipucu hangisidir?", "Sözcüğün çevresindeki cümlelerin kurduğu bağlam", "Sözcüğün kaç harfli olduğu", "Konuşmanın dosya adı", "Dinleyicinin rastgele seçimi", "Bağlam, sözcüğün olay ve düşünce içindeki işlevini gösterir."),
        ("comprehension", "'Yani, başka bir deyişle' ifadeleri bilinmeyen sözcük için ne sağlayabilir?", "Açıklama veya yeniden ifade ipucu", "Karşıtlık ipucu", "Zaman sırası ipucu", "Ses efekti", "Yeniden ifade eden bölüm önceki kavramı daha anlaşılır biçimde açıklar."),
        ("comprehension", "Bir anlam tahmini ne zaman doğrulanmalıdır?", "Bağlamla uyuşmadığında veya sözcük kritik bilgi taşıdığında", "Hiçbir zaman", "Yalnız sözcük tanıdıksa", "Sadece konuşma çok kısaysa", "Sözlük ya da güvenilir kaynak, önemli ve belirsiz tahminleri denetler."),
        ("application", "'Kuraklık nedeniyle gölet çekildi; kıyıda önceden su altında kalan taşlar görünür oldu.' cümlesinde 'çekildi' ne demektir?", "Suyu azalıp geriledi", "Fotoğrafı çekildi", "Bir yere davet edildi", "Hızla genişledi", "Taşların görünmesi su seviyesinin gerilediğini gösterir."),
        ("application", "'Mert öneriye temkinli yaklaştı; hemen kabul etmek yerine kanıt istedi.' cümlesinde 'temkinli' hangi anlamdadır?", "Dikkatli ve ölçülü", "Öfkeli ve saldırgan", "Neşeli ve aceleci", "İlgisiz ve uykulu", "Hemen kabul etmeme ve kanıt isteme dikkatli davranışı açıklar."),
        ("application", "Konuşmacı 'Bu bitki endemiktir, yani yalnız bu bölgede doğal olarak yaşar.' diyor. 'Endemik' ne demektir?", "Belirli bir bölgeye özgü", "Her kıtada yaygın", "İnsan eliyle plastikten yapılmış", "Hiç yaşamayan", "'Yani' sonrasındaki açıklama sözcüğün anlamını doğrudan verir."),
        ("application", "'Toplantı verimli geçti; kısa sürede üç uygulanabilir karar alındı.' cümlesinde 'verimli' için uygun tahmin hangisidir?", "Yararlı sonuç üreten", "Uzun ve sonuçsuz", "Gürültülü", "Katılımcısız", "Uygulanabilir kararların alınması olumlu sonuç üretildiğini gösterir."),
        ("analysis", "'İnce' sözcüğü bir kayıtta önce 'ince ip', sonra 'ince bir alay' biçiminde kullanılıyor. Hangi sonuç çıkar?", "Sözcüğün anlamı bağlama göre somut kalınlıktan sezilmesi güç alaya değişmiştir.", "İki kullanım kesin aynıdır.", "İkinci kullanım anlamsızdır.", "Sözcük yalnız ip için kullanılabilir.", "Çok anlamlı sözcüklerde çevredeki ifadeler uygun anlamı seçtirir."),
        ("analysis", "Öğrenci 'donuk bakış' ifadesindeki 'donuk'u yalnız 'buz tutmuş' olarak yorumluyor. Neyi gözden kaçırmıştır?", "İnsan bakışı bağlamında canlılık ve ifade taşımama anlamını", "Sözcüğün hece sayısını", "Konuşmacının yaşını", "Kayıt süresini", "Mecaz anlam, fiziksel donma anlamının bağlama uyarlanmasıyla oluşur."),
        ("error-analysis", "Bir öğrenci “Bilinmeyen sözcüğün anlamı, kulağıma benzeyen ilk sözcüktür.” diyor. Hangi düzeltme doğrudur?", "Ses benzerliği tek başına yetmez; cümle, konu ve açıklama ipuçları birlikte kullanılmalıdır.", "Her benzer ses aynı anlamdır.", "Bağlam sözcük anlamını etkilemez.", "Tahmin için cümleyi dinlemeye gerek yoktur.", "Anlam tahmini biçimsel benzerlikten çok kullanım bağlamına dayanır."),
        ("error-analysis", "Bir öğrenci “Tahminimi sözlükte farklı görünce sözlük yanlıştır.” diyor. Hangi değerlendirme gerekir?", "Bağlama uygun sözlük anlamı incelenmeli, tahmin kanıta göre düzeltilmelidir.", "İlk tahmin her zaman doğrudur.", "Sözlük yalnız yazım için kullanılır.", "Bağlam ile kaynak karşılaştırılmaz.", "Doğrulama, öğrenenin geçici tahminini yeniden değerlendirmesini sağlar."),
    ])


def listening_surface_meaning_tasks():
    n = "tr-g06-turkce-note-004"
    return rows(n, [
        ("comprehension", "Bir dinleme metninin yüzey anlamı neyi kapsar?", "Açıkça söylenen kişi, olay, yer, zaman ve bilgileri", "Yalnız gizli iletileri", "Dinleyicinin metinden bağımsız görüşünü", "Söylenmeyen bütün olasılıkları", "Yüzey anlam doğrudan ifade edilen bilgilerin anlaşılmasıdır."),
        ("comprehension", "Olay sırasını belirlemek için hangi sözler yol gösterir?", "Önce, ardından, sonunda", "Belki, sanırım, keşke", "Güzel, büyük, mavi", "Çünkü, ama, fakat", "Zaman ve sıra belirten ifadeler olayların dizilişini gösterir."),
        ("comprehension", "Bir duyuruda 'kim, ne zaman, nerede' soruları neyi belirlemeye yardım eder?", "Açık temel bilgileri", "Mecazların tümünü", "Konuşmacının gizli niyetini", "Metnin yazılmamış sonunu", "Duyurunun katılımcı, zaman ve yer bilgileri doğrudan yüzey anlamdır."),
        ("application", "'Servis çarşamba günü saat dokuzda okul bahçesinden kalkacak.' cümlesine göre kalkış yeri neresidir?", "Okul bahçesi", "Servis durağı", "Spor salonu", "Kent meydanı", "Cümlede yer açıkça okul bahçesi olarak verilmiştir."),
        ("application", "'Ece önce fideleri suladı, sonra kuruyan yaprakları temizledi.' cümlesinde ikinci işlem hangisidir?", "Kuruyan yaprakları temizlemek", "Fideleri sulamak", "Toprak satın almak", "Bahçeden ayrılmak", "'Sonra' sözcüğü ikinci eylemi belirtir."),
        ("application", "Bir haberde 'Köprü bakım nedeniyle iki gün araç trafiğine kapalı kalacak.' deniyor. Kapanma nedeni nedir?", "Bakım çalışması", "Yağış", "Yeni yol açılması", "Yarış", "Neden 'bakım nedeniyle' ifadesiyle doğrudan açıklanmıştır."),
        ("application", "'Toplantıya yalnız proje temsilcileri katılacaktır.' duyurusuna göre kimler katılabilir?", "Proje temsilcileri", "Okuldaki herkes", "Yalnız veliler", "Bütün ziyaretçiler", "'Yalnız' sınırlaması katılımcı grubunu açıkça belirler."),
        ("analysis", "Bir öğrenci duyurudaki 'başvurular cuma sona erer' bilgisini 'etkinlik cuma yapılır' diye aktarıyor. Hatası nedir?", "Başvuru son tarihi ile etkinlik tarihini karıştırmıştır.", "Cuma gününü yanlış duymuştur.", "Yer bilgisini eklemiştir.", "Katılımcı sayısını azaltmıştır.", "Metin yalnız başvuru süresinin bitişini söylemektedir."),
        ("analysis", "Öyküde 'Ali anahtarı masaya bıraktı; Zeynep daha sonra anahtarı aldı.' deniyor. 'Ali anahtarı Zeynep'e verdi' özeti neden uygun değildir?", "Doğrudan verme eylemi söylenmemiş, iki ayrı eylem birleştirilmiştir.", "Anahtar sözcüğü geçmemiştir.", "Zeynep anahtarı almamıştır.", "Masa belirtilmemiştir.", "Yüzey anlamda metinde açıkça bulunmayan aracılık eklenmemelidir."),
        ("error-analysis", "Bir öğrenci “Yüzey anlamı belirlerken kendi tahminimi metindeki bilgi gibi yazabilirim.” diyor. Hangi düzeltme doğrudur?", "Açık bilgi ile çıkarım ayrı tutulmalı; yüzey anlam yalnız söylenene dayanmalıdır.", "Her tahmin metin bilgisidir.", "Metindeki ayrıntılar gereksizdir.", "Çıkarım her zaman yüzey anlamdır.", "Dinleyici eklediği düşünceyi konuşmacının sözü gibi sunmamalıdır."),
        ("error-analysis", "Bir öğrenci “Olayları hatırladığım sıraya göre yazmam yeterli.” diyor. Hangi değerlendirme gerekir?", "Sıra belirten ifadeler ve eylemlerin metindeki dizilişi kontrol edilmelidir.", "Hatırlanan sıra metinden daha güvenilirdir.", "Önce ve sonra aynı anlamdadır.", "Olay sırası yüzey anlamla ilgili değildir.", "Kronoloji metinsel işaretlerle doğrulanır."),
    ])


def listening_keywords_tasks():
    n = "tr-g06-turkce-note-005"
    return rows(n, [
        ("comprehension", "Bilgilendirici bir dinleme metninde anahtar kelime neyi taşır?", "Metnin konusu ve ana düşüncesiyle doğrudan ilgili temel kavramı", "Her cümledeki ilk sözcüğü", "Yalnız özel adları", "En uzun sözcüğü", "Anahtar kelimeler metnin temel bilgi ağını temsil eder."),
        ("comprehension", "Bir sözcüğün sık tekrarlanması anahtar kelime olması için tek başına yeterli midir?", "Hayır; metnin temel düşüncesiyle ilişkisi de bulunmalıdır.", "Evet; en sık sözcük her zaman anahtardır.", "Yalnız bağlaçlar anahtar olur.", "Tekrarın hiçbir önemi yoktur.", "Sıklık bir ipucudur ancak anlam merkeziliğiyle birlikte değerlendirilir."),
        ("comprehension", "Anahtar kelimelerle kavram haritası kurmak neyi kolaylaştırır?", "Temel kavramlar arasındaki ilişkileri görmeyi", "Metni sözcüğü sözcüğüne ezberlemeyi", "Bütün ayrıntıları eşitlemeyi", "Kaynağı kaldırmayı", "Kavram haritası seçilen temel bilgileri bağlantılarıyla düzenler."),
        ("application", "Geri dönüşümün atık, ayrıştırma, yeniden kullanım ve enerji tasarrufu yönlerini anlatan kayıtta uygun anahtar kelime grubu hangisidir?", "atık–ayrıştırma–yeniden kullanım–enerji", "mikrofon–salon–konuşmacı–süre", "güzel–büyük–bugün–çok", "önce–fakat–ve–ile", "Seçilen kavramlar metnin bilgi içeriğini doğrudan temsil eder."),
        ("application", "Bir kayıt göçmen kuşların rota, beslenme ve iklimle ilişkisini anlatıyor. Hangi sözcük anahtar olmaya en az uygundur?", "stüdyo", "göç", "rota", "iklim", "Stüdyo kaydın üretim ortamı olabilir fakat konu ağının parçası değildir."),
        ("application", "Dinleyici uzun bir konuşmadan anahtar kelime çıkaracaktır. Hangi yöntem uygundur?", "Bölüm başlıklarını, tekrarları ve açıklanan temel kavramları birlikte izlemek", "Her sözcüğü eşit sayıda yazmak", "Yalnız kapanış müziğini not etmek", "Konudan bağımsız sıfatları seçmek", "Yapı ve anlam ipuçları temel kavramları belirlemeyi kolaylaştırır."),
        ("application", "'Su döngüsü' kaydında buharlaşma, yoğuşma ve yağış açıklanıyor. Üst kavram hangisidir?", "su döngüsü", "mikrofon", "hava durumu sunucusu", "örnek sayısı", "Üç süreç su döngüsü üst başlığı altında ilişkilidir."),
        ("analysis", "İki öğrenci aynı kayıttan sözcük seçiyor. Biri 'orman, biyoçeşitlilik, habitat', diğeri 'bugün, ayrıca, gerçekten' diyor. İlk grup neden daha uygundur?", "Metnin kavramsal içeriğini temsil eder; ikinci grup genel kullanım sözleridir.", "İlk sözcükler daha uzundur.", "İkinci grup yanlış telaffuz edilmiştir.", "Bağlaçlar hiçbir metinde bulunmaz.", "Anahtarlık sözcük türünden çok konu merkeziliğine dayanır."),
        ("analysis", "Bir sözcük yalnız tek kez geçiyor fakat kayıt boyunca açıklanan sorunun adı. Anahtar sayılabilir mi?", "Evet; sıklığı az olsa da ana düşünceyi örgütlüyorsa anahtar olabilir.", "Hayır; en az üç tekrar zorunludur.", "Yalnız ilk cümledeyse olabilir.", "Tek geçen sözcüğün anlamı olmaz.", "Merkezilik, salt tekrar sayısından daha belirleyici olabilir."),
        ("analysis", "Anahtar kelime listesi metnin yalnız ilk bölümünü temsil ediyor. Nasıl iyileştirilir?", "Her bölümden temel kavramlar seçilip ortak ana düşünceyle ilişkilendirilir.", "İlk bölümdeki liste uzatılır.", "Son bölümler dinlenmez.", "Yalnız tarih sayıları eklenir.", "Bütün metni temsil eden liste bölüm dengesi gerektirir."),
        ("error-analysis", "Bir öğrenci “Metinde en çok geçen 've' sözcüğü anahtar kelimedir.” diyor. Hangi düzeltme doğrudur?", "Sıklık yetmez; 've' düşünceleri bağlar fakat konunun temel kavramını taşımaz.", "Her bağlaç ana düşüncedir.", "Anahtar kelime yalnız en kısa sözcüktür.", "Konu ile ilişki aranmaz.", "İşlev sözcükleri sık olabilir ancak içerik merkezi olmayabilir."),
    ])


def listening_word_wealth_tasks():
    n = "tr-g06-turkce-note-006"
    return rows(n, [
        ("comprehension", "Söz varlığını geliştirmek yalnız yeni sözcük ezberlemek midir?", "Hayır; sözcüğün anlamını, ilişkilerini ve uygun kullanımını öğrenmeyi de içerir.", "Evet; kullanım önemli değildir.", "Yalnız yazılışını bilmek yeterlidir.", "Sözcükler bağlamdan bağımsızdır.", "Etkin söz varlığı anlamı bağlama uygun kullanabilmeyi gerektirir."),
        ("comprehension", "Eş anlamlı sözcükleri karşılaştırmak hangi beceriyi geliştirir?", "Bağlama göre ince anlam ve kullanım seçimini", "Bütün sözcükleri aynı kabul etmeyi", "Cümle kurmayı bırakmayı", "Yalnız hece saymayı", "Yakın anlamlı sözler her bağlamda birbirinin yerine geçmeyebilir."),
        ("comprehension", "Bir sözcüğün çağrışım alanını çıkarmak ne demektir?", "Sözcüğün ilişkilendiği kavram ve duyguları belirlemek", "Yalnız sözlükteki ilk anlamı kopyalamak", "Harflerini alfabetik dizmek", "Sözcüğü metinden silmek", "Çağrışımlar sözcüğün zihinde kurduğu anlam ağını gösterir."),
        ("application", "Dinlemede 'özenli' sözcüğü 'işini dikkatle ve titizlikle yapan' diye açıklanıyor. Öğrenci nasıl pekiştirebilir?", "Sözcüğü yeni bir uygun cümlede kullanıp 'dikkatli' ile anlam farkını tartışarak", "Yalnız üç kez tekrarlayarak", "Açıklamayı silerek", "İlgisiz bir sözcükle değiştirerek", "Yeni bağlam ve karşılaştırma sözcüğün etkin kullanımını güçlendirir."),
        ("application", "'Kök' sözcüğü bitki ve dil bilgisi bağlamlarında geçiyor. Hangi çalışma uygundur?", "İki anlamı ayrı örneklerle gösteren anlam haritası oluşturmak", "Bir anlamı yanlış saymak", "Sözcüğü yalnız bitki için kullanmak", "İki cümleyi dinlememek", "Çok anlamlılık bağlama göre farklı kavramsal kullanımları içerir."),
        ("application", "Bir kayıtta 'tasarruf' sözcüğü sık kullanılıyor. Öğrenci söz varlığı defterine ne yazmalıdır?", "Bağlamdaki anlam, örnek cümle ve ilişkili 'israf' karşıtlığını", "Yalnız sözcüğün harf sayısını", "Konuşmacının adını", "Dosya boyutunu", "Anlam, örnek ve anlam ilişkisi kalıcı öğrenmeyi destekler."),
        ("application", "'İncelemek' yerine her cümlede 'bakmak' kullanan öğrenci anlatımını nasıl zenginleştirir?", "Araştırmak, gözden geçirmek, çözümlemek gibi bağlama uygun seçenekleri ayırt ederek", "Her fiili bakmak yaparak", "Fiilleri cümleden çıkararak", "Sözcükleri rastgele değiştirerek", "Amaç ve bağlama göre daha özel fiiller anlatım kesinliğini artırır."),
        ("analysis", "'Sert' sözcüğü 'sert kaya' ve 'sert eleştiri' içinde geçiyor. Hangi çözümleme doğrudur?", "İlkinde fiziksel katılık, ikincide kırıcı veya ağır tutum anlamı vardır.", "İki kullanım da yalnız taş anlamındadır.", "İkinci kullanım anlamsızdır.", "Sözcük tek anlamlıdır.", "Somut nitelik mecaz yoluyla iletişim tutumunu anlatabilir."),
        ("analysis", "Öğrenci yeni öğrendiği sözcüğü her cümlede kullanıyor ve bazı cümleler bozuluyor. Sorun nedir?", "Sözcüğün bağlam, ton ve birlikte kullanıldığı sözleri gözetmemesi", "Sözcüğü hatırlaması", "Cümle kurması", "Sözlük kullanması", "Söz varlığı zenginliği çok kullanmak değil yerinde kullanmaktır."),
        ("analysis", "İki yakın anlamlı sözcükten biri resmî, diğeri günlük tonda. Seçim neye göre yapılmalıdır?", "Konuşmanın amacı, dinleyici ve bağlamına göre", "Yalnız sözcüğün uzunluğuna göre", "Rastgele", "Her zaman resmî olan seçilerek", "Üslup uygunluğu anlam kadar iletişim durumuna bağlıdır."),
        ("error-analysis", "Bir öğrenci “Sözlükte ilk yazan anlamı her cümlede kullanırım.” diyor. Hangi düzeltme doğrudur?", "Sözcüğün cümledeki bağlamına uyan anlamı seçmek gerekir.", "İlk anlam bütün kullanımları açıklar.", "Cümle anlam seçiminde etkisizdir.", "Çok anlamlı sözcük yoktur.", "Sözlük maddesindeki anlamlar kullanım bağlamına göre ayrılır."),
    ])


def listening_reflection_tasks():
    n = "tr-g06-turkce-note-007"
    return rows(n, [
        ("comprehension", "Dinleme sonrası öz yansıtma neyi amaçlar?", "Kullanılan yöntemin işe yarayıp yaramadığını değerlendirip sonraki dinlemeyi geliştirmeyi", "Yalnız doğru cevap sayısını yazmayı", "Konuşmacıyı değerlendirmeyi", "Materyali değiştirmeden tekrar etmeyi", "Öz yansıtma kişinin kendi süreç ve stratejisine odaklanır."),
        ("comprehension", "Dinleme hedefiyle sonuç arasındaki farkı belirlemek neden önemlidir?", "Eksik kalan beceri ve bilginin nerede oluştuğunu anlamaya yardım eder.", "Hedefi gereksiz kılar.", "Her sonucu başarılı gösterir.", "Yalnız materyalin süresini ölçer.", "Hedef-sonuç karşılaştırması uyarlama için somut veri sağlar."),
        ("comprehension", "Bir sonraki dinleme için ölçülebilir hedef hangisidir?", "Dört ana bilgiden en az üçünü doğru not etmek", "Daha iyi dinlemek", "Hiç hata yapmamak", "Konuşmayı sevmek", "Ölçülebilir hedef gözlenebilir performans ölçütü içerir."),
        ("application", "Öğrenci olay sırasını karıştırdığını fark ediyor. Sonraki dinlemede ne yapmalıdır?", "Önce-sonra-sonunda işaretlerini ayrı bir zaman çizgisine kaydetmelidir.", "Not almayı tamamen bırakmalıdır.", "Yalnız karakter adlarını yazmalıdır.", "Kaydı daha hızlı oynatmalıdır.", "Soruna yönelik sıra çizelgesi kronolojiyi destekler."),
        ("application", "Dinleme notlarında çok ayrıntı, az ana fikir bulunan öğrenci hangi uyarlamayı yapmalıdır?", "Her bölüm için tek ana düşünce ve iki destekleyici ayrıntı sınırı koymalıdır.", "Daha çok ayrıntı yazmalıdır.", "Bütün başlıkları kaldırmalıdır.", "Sözcüğü sözcüğüne yazmalıdır.", "Seçim ölçütü ana bilgi ile ayrıntı dengesini kurar."),
        ("application", "Öğrenci bilinmeyen sözcükler yüzünden akışı kaçırıyor. Deneme planı hangisidir?", "Sözcüğü kısa işaretleyip dinleme bitince bağlam ve sözlükle kontrol etmek", "Her sözcükte uzun araştırma yapmak", "Bilinmeyenleri yok saymak", "Kaydı kapatmak", "Ertelenmiş doğrulama akışı korurken öğrenmeyi sürdürür."),
        ("application", "Bir öğrenci podcastte başarılı, görüntülü yönergede başarısızdır. Ne yapmalıdır?", "Görsel ve işitsel bilgiyi eşleştirme biçimini ayrıca inceleyip stratejisini uyarlamalıdır.", "Bütün materyallerde aynı yöntemle devam etmelidir.", "Yalnız podcast dinlemelidir.", "Başarısızlığı ölçmemelidir.", "Materyal türü farklı dikkat ve not düzeni gerektirebilir."),
        ("analysis", "Öğrenci 'not aldım ama anlamadım' diyor. Öz yansıtma için hangi soru daha yararlıdır?", "Notlarım ana fikirleri mi, yoksa bağlantısız ayrıntıları mı içeriyor?", "Kaç sayfa kullandım?", "Kalemimin rengi neydi?", "Konuşmacı kaç kez durdu?", "Notların niteliğini incelemek anlamama sorununa doğrudan kanıt sağlar."),
        ("analysis", "İki denemede strateji değişmiş fakat materyal zorlukları da farklıdır. Sonuç nasıl değerlendirilmelidir?", "Strateji etkisini anlamak için benzer zorluktaki materyallerle yeniden karşılaştırma yapılmalıdır.", "İkinci strateji kesin üstündür.", "Materyal farkı önemsizdir.", "Tek deneme kalıcı kanıttır.", "Birden çok değişken sonucu etkilediğinde adil karşılaştırma gerekir."),
        ("analysis", "Öğrenci hedefini sürekli kolayca aşıyor. Bir sonraki adım ne olmalıdır?", "Hedefi daha derin çıkarım veya daha az destek gerektirecek biçimde kademeli zorlaştırmak", "Aynı kolay hedefi sonsuza dek sürdürmek", "Başarıyı yok saymak", "Dinlemeyi bırakmak", "Uyarlama yalnız eksikleri değil gelişimi de dikkate alır."),
        ("error-analysis", "Bir öğrenci “Öz değerlendirme, kendime yalnız 'iyiydim' demektir.” diyor. Hangi düzeltme doğrudur?", "Somut hedef, kanıt, güçlü yön ve geliştirme adımı birlikte belirtilmelidir.", "Genel övgü yeterlidir.", "Kanıt gereksizdir.", "Sonraki plan yazılmaz.", "İşe yarar yansıtma gözleme dayalı ve eyleme dönüktür."),
    ])


def reading_material_tasks():
    n = "tr-g06-turkce-note-008"
    return rows(n, [
        ("comprehension", "Okuma materyali seçerken amaçla uyum ne demektir?", "Metnin türü, kapsamı ve zorluğunun okuma gereksinimini karşılaması", "Yalnız kapağın beğenilmesi", "Her amaç için aynı metnin kullanılması", "Kaynağın yok sayılması", "Araştırma, zevk ve yönerge okuması farklı materyal özellikleri gerektirir."),
        ("comprehension", "Bir internet metninin güvenilirliğini değerlendirmede hangi bilgi önemlidir?", "Yazar, kurum, yayın tarihi ve kullanılan kaynaklar", "Sayfadaki renk sayısı", "Metnin ilk sırada çıkması", "Reklam sayısının çokluğu", "Kaynak kimliği ve kanıt metnin denetlenmesini sağlar."),
        ("application", "Öğrenci güneş enerjisiyle ilgili güncel istatistik arıyor. Hangi materyali seçmelidir?", "Tarihi ve veri kaynağı belli güncel kurum raporunu", "Yılı belirtilmeyen kişisel yorumu", "Kurgusal roman bölümünü", "Kaynağı silinmiş görseli", "İstatistik amacı güncel ve izlenebilir veri gerektirir."),
        ("application", "Bir romanın olay örgüsünü inceleyecek öğrenci için hangi sürüm uygundur?", "Eksiksiz metin ve bölüm yapısı korunmuş güvenilir baskı", "Yalnız arka kapak özeti", "Konuyla ilgili tek yorum", "Sayfaları eksik tarama", "Olay örgüsü bütün metnin sırası ve bölümleri üzerinden incelenir."),
        ("application", "Düşük görme yaşayan öğrenci için erişilebilir okuma materyali hangisidir?", "Yazı boyutu ayarlanabilen ve ekran okuyucuyla uyumlu dijital metin", "Yakınlaştırılamayan bulanık tarama", "Alternatif metinsiz görsel sayfa", "Küçük puntolu düşük kontrast baskı", "Uyarlanabilir sunum metne bağımsız erişimi artırır."),
        ("application", "On dakikada bir işlemin basamaklarını bulmak isteyen öğrenci ne seçmelidir?", "Başlıkları ve numaralı adımları açık kısa yönerge", "Uzun tarihçe yazısı", "İşlemle ilgisiz şiir", "Kaynağı belirsiz reklam", "Hızlı başvuru amacı taranabilir ve sıralı metin gerektirir."),
        ("analysis", "Kaynak A uzman yazarlı fakat 12 yıl eski; Kaynak B güncel fakat yazar ve veri kaynağı belirsiz. En iyi yaklaşım hangisidir?", "Güncel ve uzman kaynak arayıp A'nın değişmeyen temel bilgilerini ayrıca doğrulamak", "B'yi yalnız güncel diye seçmek", "A'yı yalnız uzman adıyla bütünüyle güncel saymak", "İki kaynağı da sorgulamadan birleştirmek", "Güncellik ve güvenilirlik birlikte aranmalıdır."),
        ("analysis", "Öğrenci her konuda yalnız ansiklopedi kullanıyor. Bu seçim ne zaman yetersizdir?", "Yeni gelişmeler veya farklı görüşlerin güncel kanıtlarla incelenmesi gerektiğinde", "Kavramın genel tanımını ararken", "Tarihî bir adın yazımını kontrol ederken", "Temel başvuru bilgisi ararken", "Tek materyal türü bütün amaç ve güncellik gereksinimlerini karşılamaz."),
        ("analysis", "Bir metin yaş düzeyine uygun fakat konuyu aşırı basitleştirip önemli kanıtları çıkarmış. Nasıl değerlendirilir?", "Anlaşılabilirlik olumlu olsa da içerik yeterliliği için daha kapsamlı destek gerekir.", "Kolay olduğu için tek başına yeterlidir.", "Kanıtlar gereksizdir.", "Düzey uygunluğu doğruluğu otomatik sağlar.", "Materyal seçimi düzey kadar kapsam ve doğruluğu da gözetir."),
        ("error-analysis", "Bir öğrenci “Arama motorunda ilk çıkan metin en güvenilir olandır.” diyor. Hangi düzeltme doğrudur?", "Sıralama güvenilirlik kanıtı değildir; yazar, kurum, tarih ve kaynaklar incelenmelidir.", "İlk sonuç her zaman bilimsel rapordur.", "Kaynak bilgisi gereksizdir.", "Reklamlar uzman incelemesidir.", "Arama sırası birçok etkene bağlıdır ve içerik doğruluğunu garanti etmez."),
        ("error-analysis", "Bir öğrenci “Kısa metin her okuma amacı için daha iyidir.” diyor. Hangi değerlendirme gerekir?", "Uygun uzunluk amaç, zaman ve gereken ayrıntı düzeyine göre değişir.", "Uzun metin bilgi içermez.", "Araştırmada ayrıntı gerekmez.", "Metin uzunluğu tek kalite ölçütüdür.", "Kısa başvuru ile derin inceleme farklı kapsam gerektirir."),
    ])


def fluent_reading_tasks():
    n = "tr-g06-turkce-note-009"
    return rows(n, [
        ("comprehension", "Akıcı okumanın temel bileşenleri hangileridir?", "Doğruluk, uygun hız ve anlamlı vurgu-tonlama", "Yalnız çok hızlı okuma", "Her sözcükte durma", "Metni anlamadan seslendirme", "Akıcılık hızla birlikte doğruluk ve anlamı yansıtan seslendirmeyi içerir."),
        ("comprehension", "Sessiz okumada akıcılık nasıl gözlenebilir?", "Metni uygun sürede anlayıp geri dönüşleri amaca göre yönetebilme", "Sesin yüksekliğiyle", "Her satırı parmakla izlemekle", "Yalnız sayfa sayısıyla", "Sessiz akıcılık hız ve anlama dengesine dayanır."),
        ("application", "Öğrenci noktada durmadan, virgülde uzun bekleyerek okuyor. Hangi çalışma uygundur?", "Noktalama işaretlerine göre duraklama yerlerini işaretleyip örnek okuma yapmak", "Bütün işaretleri silmek", "Daha hızlı okumak", "Her sözcükten sonra durmak", "Duraklama işaretin cümledeki işlevine göre ayarlanır."),
        ("application", "Bir diyalogu tekdüze okuyan öğrenci nasıl geliştirebilir?", "Konuşan kişileri, duyguyu ve soru-ünlem işaretlerini tonlamaya yansıtabilir.", "Bütün cümleleri aynı tonda okuyabilir.", "Karakter adlarını atlayabilir.", "Yalnız son sözcüğü yükseltebilir.", "Diyalogdaki konuşmacı ve duygu seslendirmeyi yönlendirir."),
        ("application", "Uzun sözcüklerde sık hata yapan öğrenci için uygun alıştırma hangisidir?", "Sözcükleri anlamlı hece ve eklerine ayırıp yavaş doğru okuduktan sonra bütünleştirmek", "Sözcükleri tahmin ederek atlamak", "Metni daha hızlı okumak", "Yalnız kısa sözcükleri okumak", "Doğru çözümleme hızdan önce biçim doğruluğunu kurar."),
        ("application", "Öğrenci hızlı okuyor fakat ana düşünceyi açıklayamıyor. Ne yapmalıdır?", "Hızı biraz azaltıp bölüm sonlarında kısa anlam kontrolü yapmalıdır.", "Hızı daha da artırmalıdır.", "Anlama sorularını kaldırmalıdır.", "Yalnız süreyi kaydetmelidir.", "Akıcı okuma anlamayı koruyan uygun hızı gerektirir."),
        ("analysis", "Bir öğrenci dakikada daha çok sözcük okuyor fakat hata sayısı iki katına çıkıyor. Bu gelişme sayılır mı?", "Hayır; hız artışı doğruluk ve anlam kaybıyla birlikte değerlendirilmelidir.", "Evet; tek ölçüt hızdır.", "Hatalar akıcılıkla ilgisizdir.", "Anlama ölçülmez.", "Akıcılık bileşenleri birlikte gelişmelidir."),
        ("analysis", "Şiirde yavaş, haberde daha düzenli hızlı okuyan öğrenci için hangi yorum uygundur?", "Hızını metin türü ve anlam gereksinimine göre ayarlamıştır.", "Şiiri yanlış okumuştur.", "Her metin aynı hızda okunmalıdır.", "Haberde tonlama gerekmez.", "Uygun hız tür, amaç ve söz dizimine göre değişebilir."),
        ("analysis", "Kayıt dinleyen öğrenci kendi okumasında tümce sonlarını yuttuğunu fark ediyor. En güçlü geri bildirim kanıtı hangisidir?", "Kendi ses kaydıyla örnek okumayı belirli cümlelerde karşılaştırmak", "Yalnız arkadaşının 'iyi' demesi", "Kitabın sayfa sayısı", "Okuma süresini gizlemek", "Somut kayıt karşılaştırması hata yerlerini gösterir."),
        ("error-analysis", "Bir öğrenci “Akıcı okumak mümkün olan en yüksek hızda okumaktır.” diyor. Hangi düzeltme doğrudur?", "Akıcılık doğru, anlaşılır ve metne uygun hızda okumaktır.", "Hız dışındaki ölçütler gereksizdir.", "Duraklama akıcılığı bozar.", "Anlam yalnız sessiz okumada önemlidir.", "Aşırı hız hata ve anlam kaybına yol açabilir."),
        ("error-analysis", "Bir öğrenci “Sessiz okumada geri dönmek her zaman hatadır.” diyor. Hangi değerlendirme gerekir?", "Zor bir bilgi veya belirsiz bağlantı için amaçlı geri dönüş anlamayı destekleyebilir.", "Her satır üç kez okunmalıdır.", "Geri dönüş yalnız sesli okumada olur.", "Anlama kontrolü gereksizdir.", "Sorun amaçsız sık geri dönüşlerdir; bilinçli kontrol farklıdır."),
    ])


def reading_strategy_tasks():
    n = "tr-g06-turkce-note-010"
    return rows(n, [
        ("comprehension", "Göz atarak okuma hangi amaçla kullanılır?", "Metnin yapısı ve genel konusu hakkında hızlı ön bilgi edinmek", "Her ayrıntıyı ezberlemek", "Yalnız noktalama saymak", "Metni baştan sona seslendirmek", "Başlık, alt başlık ve görseller genel yapı hakkında ön izleme sağlar."),
        ("comprehension", "Soru sorarak okuma stratejisinin katkısı nedir?", "Okurun amacını canlı tutup kanıt aramasını sağlaması", "Metindeki bütün cevapları önceden bilmesi", "Okuma hızını her zaman artırması", "Yazarı gereksiz kılması", "Sorular dikkat ve anlam kontrolünü yönlendirir."),
        ("application", "Bir kılavuzdan yalnız parola değiştirme adımını arayan kişi hangi yöntemi kullanmalıdır?", "Anahtar sözcükle tarayarak okuma", "Bütün kılavuzu edebî okuma", "Her sayfayı ezberleme", "Yalnız kapağa bakma", "Belirli bilgi arama tarama stratejisine uygundur."),
        ("application", "Bir makalenin savını değerlendirecek öğrenci ne yapmalıdır?", "İddia, kanıt, karşı görüş ve sonucu işaretleyerek eleştirel okumalıdır.", "Yalnız ilk cümleyi kabul etmelidir.", "Kaynakları atlamalıdır.", "Bilmediği her kavramı yok saymalıdır.", "Sav değerlendirmesi argümanın bileşenlerini incelemeyi gerektirir."),
        ("application", "Sınav öncesi uzun bir bölümü yeniden çalışacak öğrenci için hangi yöntem uygundur?", "Önce başlıkları gözden geçirip sonra önemli bölümleri özetleyerek okumak", "Metni amaçsız hızla geçmek", "Yalnız son paragrafı okumak", "Notlarla metni karşılaştırmamak", "Ön izleme ve özetleme bilgiyi düzenli biçimde yeniden kurar."),
        ("application", "Bir öykünün atmosferini anlamak isteyen okur neye odaklanmalıdır?", "Mekân, betimleme, duygu çağrıştıran sözler ve olayların tonuna", "Yalnız sayfa numarasına", "Sadece karakter adlarının uzunluğuna", "Yayın tarihine", "Atmosfer dil, mekân ve olay sunumunun birlikte etkisidir."),
        ("analysis", "Öğrenci her metinde altını çok fazla çizdiği için önemli yerleri seçemiyor. Ne yapmalıdır?", "Okuma amacına göre sınırlı ölçüt belirleyip yalnız iddia ve temel kanıtları işaretlemelidir.", "Daha fazla yeri çizmelidir.", "Bütün metni boyamalıdır.", "Alt başlıkları silmelidir.", "Seçici işaretleme bilgi önceliğini görünür kılar."),
        ("analysis", "Bir okuyucu tarama yöntemiyle şiirin duygusal katmanını anlamaya çalışıyor. Neden yetersiz kalabilir?", "Tarama belirli bilgiyi bulur; şiir için yavaş ve yorumlayıcı okuma gerekebilir.", "Şiirde sözcük bulunmaz.", "Tarama yalnız roman içindir.", "Duygu okuma yöntemiyle ilgisizdir.", "Strateji metnin türü ve amaçla eşleşmelidir."),
        ("analysis", "İki kaynak çeliştiğinde okur hangi stratejiyle ilerlemelidir?", "Kaynakların kanıtlarını, tarihini ve uzmanlığını karşılaştırıp ek doğrulama aramalıdır.", "İlk okuduğunu kesin kabul etmelidir.", "İki metni de yok saymalıdır.", "Daha kısa olanı seçmelidir.", "Çelişki eleştirel karşılaştırma ve kaynak denetimi gerektirir."),
        ("error-analysis", "Bir öğrenci “Hızlı göz atma her metni tam anlamak için yeterlidir.” diyor. Hangi düzeltme doğrudur?", "Göz atma genel yapı verir; ayrıntılı ve eleştirel amaçlar için derin okuma gerekir.", "Başlık bütün kanıtları içerir.", "Ayrıntılar hiçbir zaman önemli değildir.", "Derin okuma yalnız sözlük içindir.", "Ön izleme ile tam çözümleme farklı amaçlara hizmet eder."),
        ("error-analysis", "Bir öğrenci “Okuma stratejimi metin boyunca değiştirmemeliyim.” diyor. Hangi değerlendirme gerekir?", "Anlama güçlüğü veya amaç değiştiğinde strateji uyarlanabilir.", "Tek strateji bütün sorunları çözer.", "Okur kendi sürecini izlememelidir.", "Yeniden okuma her zaman yanlıştır.", "Etkili okur kullandığı yöntemi sonuçlara göre düzenler."),
    ])


def prediction_intro_task():
    return rows("tr-g06-turkce-note-011", [
        ("comprehension", "Okuma öncesi tahmin oluştururken hangi unsurlar kullanılabilir?", "Başlık, görsel, tür ve önceki bilgiler", "Yalnız sayfa numarası", "Metni okumadan kesin hüküm", "Yazarın adındaki harf sayısı", "Metin çevresindeki ipuçları konu ve olay hakkında sınanabilir beklenti kurdurur."),
    ])


TASK_BUILDERS = [listening_strategy_tasks, listening_vocabulary_inference_tasks,
                 listening_surface_meaning_tasks, listening_keywords_tasks,
                 listening_word_wealth_tasks, listening_reflection_tasks,
                 reading_material_tasks, fluent_reading_tasks, reading_strategy_tasks,
                 prediction_intro_task]


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1700:
        raise RuntimeError("validated first seventeen batches must exist before batch 18")
    notes = read_notes_only(TURKISH_SOURCE)
    tasks = [item for builder in TASK_BUILDERS for item in builder()]
    if len(tasks) != 100:
        raise AssertionError(f"batch 18 must contain 100 tasks, got {len(tasks)}")
    expected_modes = {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
    if Counter(item["mode"] for item in tasks) != expected_modes:
        raise AssertionError(Counter(item["mode"] for item in tasks))
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    rows_out = [make_record(local, item, notes[item["note"]], batch=18, number_base=1700)
                for local, item in enumerate(tasks, 1)]
    if Counter(row["subject"] for row in rows_out) != Counter({"Türkçe": 100}):
        raise AssertionError(Counter(row["subject"] for row in rows_out))
    if Counter(row["correctIndex"] for row in rows_out) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer positions are not exactly balanced")
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":"))
                                 for row in existing + rows_out) + "\n", encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
    print(json.dumps({"batch": 18, "questions": 100, "turkish": 100, "figures": 0,
                      "total": 1800, "modes": dict(Counter(item["mode"] for item in tasks)),
                      "sourceQuestionReads": 0, "figureSpec": "1.3.0"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
