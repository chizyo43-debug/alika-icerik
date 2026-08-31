#!/usr/bin/env python3
"""Append 100 independently authored Grade 6 Turkish questions (batch 19)."""
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


def prediction_tasks():
    n = "tr-g06-turkce-note-011"
    return rows(n, [
        ("comprehension", "Okuma sırasında tahminin işlevi nedir?", "Okurun ipuçlarından beklenti kurup yeni bilgilerle bunu sınaması", "Metnin sonunu kesinleştirmesi", "Yazarı gereksiz kılması", "Bütün ayrıntıları atlaması", "Tahmin dikkat ve merakı yönlendirir, kanıta göre güncellenir."),
        ("comprehension", "Tahmin ile rastgele varsayım arasındaki fark hangisidir?", "Tahmin başlık, görsel ve metinsel ipuçlarına dayanır.", "Tahmin hiçbir kanıt gerektirmez.", "Rastgele varsayım her zaman doğrudur.", "İkisi kesin sonuçtur.", "Sınanabilir bir tahmin metinden gelen dayanak içerir."),
        ("application", "Başlığı 'Kaybolan Tohumlar', görseli kurumuş tarla olan metin için uygun tahmin hangisidir?", "Tohum çeşitliliğinin azalması ve bunun tarıma etkisi ele alınabilir.", "Bir uzay aracının yapımı anlatılır.", "Yalnız futbol kuralları sıralanır.", "Metinde kesinlikle şiir vardır.", "Başlık ve görsel tarım ile çeşitlilik sorununa işaret eder."),
        ("application", "İlk paragrafta karakter yağmur bulutlarını izleyip kovaları hazırlıyor. Sonraki olay için en güçlü tahmin hangisidir?", "Yağmur suyunu biriktirmeye çalışacaktır.", "Denizde yüzmeye gidecektir.", "Kovaları çöpe atacaktır.", "Bulutlarla ilgili hiçbir şey olmayacaktır.", "Hazırlık eylemi yağmur suyunu toplama beklentisini destekler."),
        ("application", "Metnin ortasında yeni kanıt ilk tahminle çelişiyor. Okur ne yapmalıdır?", "Tahminini yeni kanıta göre değiştirmelidir.", "İlk tahmini metinden üstün saymalıdır.", "Çelişen cümleyi yok saymalıdır.", "Okumayı bırakmalıdır.", "Tahmin esnek olmalı ve kanıta göre yeniden kurulmalıdır."),
        ("application", "Bir bilgilendirici metinde alt başlıklar 'Sorun', 'Nedenler', 'Çözüm Denemeleri'dir. Son bölüm için hangi tahmin uygundur?", "Denemelerin sonuçları veya öneriler sunulabilir.", "Yeni bir masal kahramanı tanıtılır.", "Konu açıklamasız değişir.", "Yalnız kaynakça kaldırılır.", "Metnin açıklayıcı düzeni çözüm değerlendirmesine doğru ilerler."),
        ("analysis", "İki tahminden biri yalnız başlığa, diğeri başlıkla ilk paragraftaki kanıta dayanıyor. Hangisi daha güçlüdür?", "Birden çok uyumlu ipucu kullanan ikinci tahmin", "Yalnız başlığa dayanan ilk tahmin", "İkisi de kanıtsızdır.", "Tahminler karşılaştırılamaz.", "Bağımsız ipuçlarının birleşmesi tahminin dayanağını güçlendirir."),
        ("analysis", "Okur 'kahraman yarışmayı kazanır' tahminini yapıyor; metin kahramanın sakatlandığını ve arkadaşına yardım ettiğini gösteriyor. Nasıl güncellenmelidir?", "Sonucun kazanmak yerine dayanışma ve fedakârlığa yönelebileceği düşünülmelidir.", "İlk tahmin kesin sürdürülmelidir.", "Yeni olay metin dışıdır.", "Arkadaş karakteri yok sayılmalıdır.", "Olay örgüsündeki dönüm noktası beklentiyi değiştirir."),
        ("error-analysis", "Bir öğrenci “Tahminim yanlış çıktıysa okuma başarısızdır.” diyor. Hangi düzeltme doğrudur?", "Yanlış tahmin de yeni kanıtı fark edip düşünceyi güncelleme fırsatı verir.", "Tahmin yalnız doğruysa yapılır.", "Metin tahmine uymalıdır.", "Tahmin değiştirmek yasaktır.", "Amaç sonucu bilmek değil anlama sürecini kanıtla yönetmektir."),
        ("error-analysis", "Bir öğrenci “Metni bitirdikten sonra söylenen sonuç tahmindir.” diyor. Hangi değerlendirme gerekir?", "Sonuç bilindikten sonraki ifade tahmin değil, özet veya değerlendirmedir.", "Her özet tahmindir.", "Tahmin yalnız sona yazılır.", "Okuma öncesi ipucu kullanılmaz.", "Tahmin belirsizlik varken ileriye dönük kurulur."),
    ])


def reading_context_vocabulary_tasks():
    n = "tr-g06-turkce-note-012"
    return rows(n, [
        ("comprehension", "Metinde bilinmeyen sözcüğün anlamını tahmin ederken hangi ipuçları birlikte kullanılabilir?", "Tanım, örnek, karşıtlık ve neden-sonuç ifadeleri", "Yalnız harf sayısı", "Sayfa rengi ve punto", "Kitabın fiyatı", "Yazar anlamı çevredeki farklı ilişkilerle sezdirir."),
        ("comprehension", "'Aksine' sözcüğü çevresindeki anlam için ne tür ipucu verir?", "Karşıtlık", "Örnekleme", "Zaman sırası", "Tanım", "'Aksine' önceki düşüncenin tersini bildiren bölüme geçiş yapar."),
        ("comprehension", "Sözlükte birden çok anlam varsa hangisi seçilmelidir?", "Cümlenin konusu ve dil bilgisel yapısıyla uyuşan anlam", "Her zaman ilk anlam", "En uzun açıklama", "Rastgele bir anlam", "Çok anlamlı sözcüklerde bağlam doğru sözlük anlamını belirler."),
        ("application", "'Toprak suya doymuştu; bir damla daha ememeyecek kadar suyla doluydu.' cümlesinde 'doymuş' ne demektir?", "Alabileceği en yüksek su miktarına ulaşmış", "Acıkmış", "Rengini kaybetmiş", "Sertleşip taş olmuş", "İkinci bölüm sözcüğü açıklayan tanım ipucu verir."),
        ("application", "'Çocuk çekingen değildi; aksine tanımadığı kişilerle kolayca konuşuyordu.' cümlesinde 'çekingen' hangi anlamdadır?", "İletişim kurmaktan kaçınan", "Çok konuşkan", "Öfkeli", "Dalgın", "'Aksine' sonrası davranış ilk sıfatın karşıtını gösterir."),
        ("application", "'İşler sekteye uğradı; malzeme gelmeyince çalışma geçici olarak durdu.' ifadesinde 'sekteye uğramak' ne demektir?", "Kesintiye uğramak", "Hızlanmak", "Başarıyla tamamlanmak", "Gizlice başlamak", "Neden-sonuç bölümü çalışmanın durduğunu açıklar."),
        ("application", "'Yazar yalın bir dil kullanmış; karmaşık ve süslü anlatımdan kaçınmış.' cümlesinde 'yalın' ne demektir?", "Sade", "Eksik", "Kaba", "Bilimsel", "Karşılaştırılan 'karmaşık ve süslü' sözleri sade anlamını destekler."),
        ("analysis", "'Koyu' sözcüğü 'koyu renk', 'koyu sohbet' ve 'koyu taraftar' kullanımlarında neden farklı anlam taşır?", "Birlikte kullanıldığı sözcükler fiziksel yoğunluk, samimiyet ve güçlü bağlılık anlamlarını seçtirir.", "Sözcük her yerde yalnız renk demektir.", "Son iki kullanım yanlıştır.", "Bağlam anlamı etkilemez.", "Eş dizimler çok anlamlı sözcüğün hangi anlamda olduğunu belirler."),
        ("analysis", "Öğrenci 'yüz vermek' ifadesini 'yüzünü göstermek' diye açıklıyor. Cümlede 'Ona çok yüz verince kuralları önemsemedi.' yazıyor. Doğru çözümleme hangisidir?", "Gereğinden fazla hoş görülü davranmak", "Fotoğrafını göstermek", "Yönünü çevirmek", "Birini tanımamak", "Sonuçta kuralların önemsenmemesi aşırı hoşgörü anlamını destekler."),
        ("error-analysis", "Bir öğrenci “Sözcüğün kökünü biliyorsam bağlama bakmam gerekmez.” diyor. Hangi düzeltme doğrudur?", "Kök ipucu yararlı olabilir; ekler, çok anlamlılık ve cümle bağlamı da kontrol edilmelidir.", "Kök her kullanımın tam anlamıdır.", "Ekler anlamı değiştirmez.", "Cümle sözcüğe bilgi vermez.", "Biçimsel çözümleme anlam tahmininin yalnız bir parçasıdır."),
        ("error-analysis", "Bir öğrenci “Tahminimi doğrulamak için cümleyi tekrar okumak gereksizdir.” diyor. Hangi değerlendirme gerekir?", "Tahmini cümleye yerleştirip anlam bütünlüğünü sınamak önemli bir kontroldür.", "İlk çağrışım her zaman doğrudur.", "Bağlam yalnız ilk okumada kullanılır.", "Sözlük ve metin karşılaştırılmaz.", "Yerine koyma testi tahminin bağlama uyup uymadığını gösterir."),
    ])


def reading_surface_tasks():
    n = "tr-g06-turkce-note-013"
    return rows(n, [
        ("comprehension", "Metnin yüzey anlamını belirlerken hangi sorular temel bilgi sağlar?", "Kim, ne, nerede, ne zaman ve nasıl", "Yazar neyi gizledi", "Başka neler olabilirdi", "Okur ne hissediyor", "Doğrudan verilen olay ve durum bilgileri temel sorularla belirlenir."),
        ("comprehension", "Gönderim yapan 'bu, o, burada' gibi sözleri anlamak için ne yapılır?", "Önceki ve sonraki cümlelerde işaret ettikleri varlık bulunur.", "Sözler metinden çıkarılır.", "Her biri yazarı gösterir.", "Yalnız sözlüğe bakılır.", "Gönderim öğesi bağlamdaki bir varlık veya düşünceye bağlanır."),
        ("comprehension", "Bir metinde olayların zamanını belirleyen açık ipucu hangisidir?", "'Ertesi sabah' ifadesi", "'Belki' sözcüğü", "Bir benzetme", "Başlıktaki sıfat", "Zaman zarfı olayın kronolojik konumunu açıkça verir."),
        ("application", "'Defne paketi kütüphaneciye bıraktı. O, paketi öğleden sonra müdüre iletti.' cümlesinde 'O' kimdir?", "Kütüphaneci", "Defne", "Müdür", "Paket", "İletme eylemini yapan en yakın uygun kişi kütüphanecidir."),
        ("application", "'Yarış 14 Mayıs'ta başlayacak, kayıtlar ise 10 Mayıs'ta kapanacak.' Metne göre önce hangisi olur?", "Kayıtların kapanması", "Yarışın başlaması", "İki olay aynı anda olur.", "Tarih verilmemiştir.", "10 Mayıs, 14 Mayıs'tan öncedir."),
        ("application", "'Otobüs arızalanınca ekip yürüyerek köye ulaştı.' cümlesinde köye nasıl ulaşılmıştır?", "Yürüyerek", "Otobüsle", "Trenle", "Bisikletle", "Ulaşma biçimi cümlede açıkça belirtilmiştir."),
        ("application", "'Sergi pazartesi hariç her gün 10.00–17.00 arasında açıktır.' Salı günü 16.30'da ziyaret mümkün müdür?", "Evet, açık saat aralığındadır.", "Hayır, yalnız pazartesi açıktır.", "Hayır, 16.00'da kapanır.", "Saat bilgisi yoktur.", "Salı hariç tutulan gün değildir ve 16.30 kapanıştan öncedir."),
        ("analysis", "Özet 'Selin kitabı satın aldı' diyor; metinde 'Selin kitabı ödünç aldı' yazıyor. Yüzey anlam hatası nedir?", "Mülkiyet değişimi eklenmiş, ödünç alma satın alma gibi aktarılmıştır.", "Karakter adı değiştirilmiştir.", "Kitap metinde yoktur.", "Zaman bilgisi eklenmiştir.", "İki eylemin hukuki ve günlük anlamı farklıdır."),
        ("analysis", "'Kapı açılınca içeride kimse görünmedi.' cümlesinden 'oda boştur' sonucu kesin midir?", "Hayır; görünmeyen bir yerde kişi bulunabilir, cümle yalnız görünmediğini söyler.", "Evet; görünmemek yok olmak demektir.", "Evet; kapı açılmıştır.", "Oda sözcüğü geçmediği için kapı yoktur.", "Yüzey bilgi ile olası çıkarım ayrılmalıdır."),
        ("analysis", "Bir olay özeti doğru kişileri içeriyor fakat iki olayın sırasını ters veriyor. Neden yüzey anlamı bozar?", "Neden-sonuç veya olay gelişimi farklılaşabilir.", "Kişiler doğruysa sıra önemsizdir.", "Özetlerde zaman kullanılmaz.", "Ters sıra metni kısaltır.", "Kronoloji açık olay örgüsünün bir parçasıdır."),
        ("error-analysis", "Bir öğrenci “Metinde açıkça söylenmeyen ama mümkün olan her şey yüzey anlamdır.” diyor. Hangi düzeltme doğrudur?", "Yüzey anlam doğrudan verilen bilgidir; olasılıklar çıkarım olarak ayrı belirtilir.", "Mümkün olan her olay metinde vardır.", "Çıkarım ile bilgi aynı şeydir.", "Metin kanıtı gerekmez.", "Açıklık derecesi bilgi türünü belirler."),
    ])


def reading_keywords_tasks():
    n = "tr-g06-turkce-note-014"
    return rows(n, [
        ("comprehension", "Anahtar kelime seçiminin metni özetlemeye katkısı nedir?", "Temel kavramları görünür kılarak ana düşüncenin iskeletini kurması", "Bütün cümleleri kopyalatması", "Ayrıntıları ana düşünce yapması", "Yalnız bağlaçları toplaması", "Kavramsal merkezler özette hangi bilgilerin korunacağını gösterir."),
        ("comprehension", "Bir sözcüğün başlıkta ve alt başlıklarda yer alması neyin ipucu olabilir?", "Metnin temel kavramlarından biri olduğunun", "Her zaman önemsiz olduğunun", "Yalnız yazım örneği olduğunun", "Metinle ilgisizliğinin", "Metin yapısında öne çıkarılan sözcükler konu örgüsünü gösterebilir."),
        ("comprehension", "Anahtar kelimeler arasında ilişki kurarken hangi soru yararlıdır?", "Bu kavramlar birbirini nasıl açıklar veya etkiler?", "Hangisi daha uzun yazılır?", "Kaç harfleri vardır?", "Hangi satırda önce görünür?", "Anlam ilişkisi kavram ağını kurar."),
        ("application", "'Kent Bahçeleri' metni üretim, dayanışma, boş alan ve sağlıklı beslenmeyi açıklıyor. Uygun anahtar grup hangisidir?", "kent bahçesi–üretim–dayanışma–beslenme", "yazar–sayfa–paragraf–nokta", "bugün–çok–ve–fakat", "şehir–kalem–masa–ses", "Seçilen sözcükler metnin konusu ve yararlarını kapsar."),
        ("application", "Bir metinde 'erozyon' bir kez tanımlanıyor, sonraki paragraflar neden ve önlemleri açıklıyor. Sözcük anahtar mıdır?", "Evet; bütün açıklamaları örgütleyen temel sorunun adıdır.", "Hayır; yalnız bir kez yazılmıştır.", "Yalnız çok tekrarlanan bağlaçlar anahtardır.", "Tanımlanan sözcük anahtar olamaz.", "Kavramsal merkez sıklıktan bağımsız biçimde metni örgütleyebilir."),
        ("application", "'Uyku, dikkat ve öğrenme' ilişkisini anlatan metinde kavram haritasının merkezine ne yazılmalıdır?", "uyku ve öğrenme ilişkisi", "metnin yayıncısı", "sayfa numarası", "örnek öğrencinin adı", "Merkez metnin bütün alt kavramlarını kapsamalıdır."),
        ("application", "Anahtar listesinde 'iklim, yağış, sıcaklık, bitki örtüsü, sandalye' vardır. Hangisi çıkarılmalıdır?", "sandalye", "iklim", "yağış", "bitki örtüsü", "Sandalye diğer doğal sistem kavramlarıyla ilişki kurmaz."),
        ("analysis", "İki metin de 'enerji' sözcüğünü kullanıyor; biri beslenme, diğeri elektrik üretimi hakkında. Anahtar kelimeler nasıl farklılaştırılır?", "Her metinde enerjiyi çevreleyen besin-metabolizma ve kaynak-elektrik kavramlarıyla", "İki liste yalnız 'enerji' olmalıdır.", "Bağlamlar yok sayılmalıdır.", "Metin başlıkları silinmelidir.", "Aynı sözcüğün kavramsal alanı metnin konusuna göre değişir."),
        ("analysis", "Öğrencinin seçtiği anahtarlar yalnız örnekleri, arkadaşınınkiler ana kavram ve nedenleri içeriyor. Hangisi özete daha iyi temel olur?", "Ana kavram ve nedenleri içeren liste", "Yalnız örnekleri içeren liste", "İki liste de metinle ilgisizdir.", "Anahtar kelime özeti etkilemez.", "Örnekler destekleyicidir; ana düşünceyi kuran kavramlar önceliklidir."),
        ("analysis", "Bir anahtar sözcük listesi metnin sonundaki çözüm bölümünü temsil etmiyor. Hangi ekleme ölçütü kullanılmalıdır?", "Çözümün temel eylem ve hedefini gösteren kavramlar eklenmelidir.", "Rastgele yeni sıfatlar eklenmelidir.", "İlk bölüm sözcükleri tekrarlanmalıdır.", "Çözüm bölümü yok sayılmalıdır.", "Dengeli liste metnin bütün yapısal bölümlerini kapsar."),
        ("error-analysis", "Bir öğrenci “Özel ad olan her sözcük anahtar kelimedir.” diyor. Hangi düzeltme doğrudur?", "Özel ad ancak metnin temel bilgi örgüsünde önemliyse anahtar seçilir.", "Her kişi adı ana düşüncedir.", "Anahtar kelime yalnız özel addır.", "Metnin konusu önemli değildir.", "Sözcük türü değil anlam merkeziliği belirleyicidir."),
    ])


def reading_word_wealth_tasks():
    n = "tr-g06-turkce-note-015"
    return rows(n, [
        ("comprehension", "Metinden söz varlığı geliştirirken sözcük ailesi oluşturmak ne sağlar?", "Ortak kökten türeyen anlam ve görev ilişkilerini görmeyi", "Bütün sözcükleri eş anlamlı saymayı", "Kökü metinden silmeyi", "Yalnız hece saymayı", "Kök ve ek ilişkisi yeni sözcükleri anlamayı kolaylaştırır."),
        ("comprehension", "Deyimin anlamı neden tek tek sözcüklerden her zaman çıkarılamaz?", "Kalıplaşmış bütünün mecaz veya özel bir anlam taşıması nedeniyle", "Deyimlerde sözcük bulunmadığı için", "Her deyim yabancı dil olduğu için", "Sözcükler yazılmadığı için", "Kalıplaşmış ifade parçalarının toplamından farklı anlam kurabilir."),
        ("application", "'Gözden geçirmek' ifadesi 'raporu son kez gözden geçirdi' cümlesinde ne demektir?", "İnceleyip kontrol etmek", "Raporu gözünün önünden geçirmek", "Raporu saklamak", "Yalnız başlığı okumak", "Nesne olarak rapor ve son kez sözü kontrol anlamını destekler."),
        ("application", "Metinde 'üretken' sözcüğünü öğrenen öğrenci hangi sözcük ailesini kurabilir?", "üretmek–üretim–üretici–üretken", "ürün–tüketmek–kalem–masa", "üretmek–uyumak–koşmak–bakmak", "üretken–mavi–dün–fakat", "Ortak 'üret-' kökü anlam ilişkisini korur."),
        ("application", "'Kararlı' sözcüğünü 'inatçı' ile karşılaştırırken hangi ayrım uygundur?", "Kararlı hedefte tutarlı, inatçı ise gerekçeye rağmen değişmemekte olumsuz çağrışım taşıyabilir.", "İki sözcük her bağlamda aynıdır.", "Kararlı yalnız fiziksel nesnedir.", "İnatçı her zaman olumlu bir övgüdür.", "Yakın anlamlı sözlerin ton ve değerlendirme farkı vardır."),
        ("application", "Bir metindeki 'kulağına küpe olmak' deyimini öğrenci nasıl etkinleştirir?", "Dersi unutmamayı anlatan yeni ve uygun bir cümlede kullanarak", "Sözcükleri gerçek takı olarak çizerek", "Deyimi her cümleye ekleyerek", "Anlamını kontrol etmeden değiştirerek", "Yeni bağlamda doğru kullanım kalıcı ve işlevsel öğrenme sağlar."),
        ("analysis", "'Ağır' sözcüğü 'ağır çanta', 'ağır ceza' ve 'ağır konuşma'da nasıl çözülür?", "Fiziksel ağırlık, ciddi yaptırım ve kırıcı/sert söyleyiş anlamlarına göre", "Üçünde de kilogram anlamıyla", "Yalnız ceza kullanımında anlamlıdır.", "Sözcük her yerde aynıdır.", "Birlikte kullanılan adlar uygun anlamı belirler."),
        ("analysis", "Öğrenci metindeki yeni sözcükleri alfabetik yazıyor fakat kullanamıyor. Hangi çalışma eksiktir?", "Anlam, bağlam, örnek ve anlam ilişkileriyle etkin kullanım", "Alfabe sırası", "Sayfa numarası", "Sözcük sayısı", "Listeleme tek başına üretici söz varlığı oluşturmaz."),
        ("analysis", "Bir yazar aynı kavram için her cümlede farklı yakın anlamlı söz kullanıyor. Bunun etkisi ne olabilir?", "Tekrarı azaltırken anlam tonlarını zenginleştirebilir; bağlam uyumu denetlenmelidir.", "Metni otomatik olarak yanlış yapar.", "Bütün sözcükleri eş anlamlı yapar.", "Ana düşünceyi zorunlu kaldırır.", "Çeşitlilik ancak sözcükler bağlama uygun seçildiğinde yararlıdır."),
        ("error-analysis", "Bir öğrenci “Deyimi oluşturan sözcüklerden birini eş anlamlısıyla değiştirsem anlam aynı kalır.” diyor. Hangi düzeltme doğrudur?", "Deyimler kalıplaşmıştır; sözcük değişikliği kullanımı bozabilir.", "Her deyim serbestçe değişir.", "Deyimler yalnız gerçek anlamdadır.", "Kalıplaşma önemli değildir.", "Deyimin biçimi toplumsal kullanımda yerleşmiştir."),
        ("error-analysis", "Bir öğrenci “Yeni öğrendiğim sözcüğü çok kullanırsam her bağlama uyar.” diyor. Hangi değerlendirme gerekir?", "Sözcük anlam, ton ve eş dizim bakımından uygun olduğu yerde kullanılmalıdır.", "Sıklık bütün hataları düzeltir.", "Bağlam sözcük seçimini etkilemez.", "Her sözcük her adla birleşir.", "Yerindelik, kullanım sayısından daha önemlidir."),
    ])


def reading_reflection_tasks():
    n = "tr-g06-turkce-note-016"
    return rows(n, [
        ("comprehension", "Okuma öz değerlendirmesinde hangi kanıt kullanılabilir?", "Özetin metindeki ana düşünce ve kanıtlarla uyumu", "Yalnız okunan sayfa sayısı", "Kitabın kapak rengi", "Masanın konumu", "Ürün ile kaynak metin karşılaştırması anlama düzeyini gösterir."),
        ("comprehension", "Okuma hızını değerlendirirken neden anlama da ölçülmelidir?", "Hız artarken anlam kaybı olup olmadığını görmek için", "Anlama yalnız yazmada önemlidir.", "Hız tek başına her şeyi gösterir.", "Metin türü önemsizdir.", "Etkili okuma hız ve anlama dengesidir."),
        ("application", "Öğrenci bilim metninde ana düşünceyi buluyor fakat grafik açıklamalarını kaçırıyor. Sonraki hedefi ne olmalıdır?", "Metin ile grafik başlığı ve verileri arasında en az iki ilişki kurmak", "Daha hızlı sayfa çevirmek", "Grafikleri tamamen atlamak", "Yalnız sonuç paragrafını okumak", "Hedef saptanan çoklu temsil eksikliğine doğrudan yönelir."),
        ("application", "Okur bilmediği sözcüklerde sürekli sözlüğe gidip akışı kaybediyor. Hangi deneme planı uygundur?", "Önce bağlamdan tahmin edip kritik sözcükleri bölüm sonunda doğrulamak", "Sözlüğü tamamen bırakmak", "Her sözcükte uzun ara vermek", "Bilinmeyenleri metinden silmek", "Seçici ve ertelenmiş doğrulama akıcılıkla doğruluğu dengeler."),
        ("application", "Öğrenci olay sırasını iyi, karakter amaçlarını zayıf anlıyor. Hangi stratejiyi eklemelidir?", "Karakterin kararlarını ve bunların gerekçelerini iki sütunda izlemek", "Yalnız tarihleri işaretlemek", "Metni sesli ama amaçsız okumak", "Karakter adlarını silmek", "Karar-gerekçe eşleştirmesi motivasyon çözümlemesini destekler."),
        ("application", "Bir öğrenci önceki hedefini iki hafta boyunca karşılıyor. Nasıl uyarlamalıdır?", "Benzer beceriyi daha karmaşık metinde veya daha az destekle denemelidir.", "Hedefi değiştirmeden sonsuza dek sürdürmelidir.", "Başarı kaydını silmelidir.", "Okumayı bırakmalıdır.", "Kademeli güçlük gelişimi sürdürür."),
        ("analysis", "Öğrenci yöntem değiştirdikten sonra başarısı arttı, fakat ikinci metin çok daha kolaydı. Hangi sonuç uygundur?", "Yöntemin etkisini ayırmak için benzer zorluktaki metinlerle yeniden denemek gerekir.", "Yeni yöntem kesin daha iyidir.", "Metin zorluğu sonucu etkilemez.", "Tek karşılaştırma yeterlidir.", "Adil değerlendirme diğer değişkenleri olabildiğince sabit tutar."),
        ("analysis", "Okur 'metni anladım' diyor ancak özetinde ana düşünce yok. Hangi kanıt daha güvenilirdir?", "Özet ve sorulara verilen gerekçeli cevaplar", "Okurun genel hissi", "Okuma süresinin kısa olması", "Metnin kolay görünmesi", "Somut performans öz algıyı doğrular veya düzeltir."),
        ("analysis", "Bir okuma günlüğü yalnız hataları içeriyor. Nasıl geliştirilmelidir?", "İşe yarayan strateji, kanıt, güçlük ve sonraki adımı birlikte kaydetmelidir.", "Daha çok hata eklemelidir.", "Başarıları yok saymalıdır.", "Plan bölümünü kaldırmalıdır.", "Dengeli yansıtma güçlü yönleri sürdürürken gelişim alanını hedefler."),
        ("error-analysis", "Bir öğrenci “Öz değerlendirmede kendime puan vermem yeterlidir.” diyor. Hangi düzeltme doğrudur?", "Puanın hangi metinsel ve performans kanıtına dayandığı açıklanmalı, gelişim adımı belirlenmelidir.", "Kanıt puanı gereksiz yapar.", "Sonraki hedef yazılmaz.", "Puan her zaman tam olmalıdır.", "Sayısal sonuç tek başına neden ve çözüm göstermez."),
        ("error-analysis", "Bir öğrenci “Anlamadığım metin her zaman kötü yazılmıştır.” diyor. Hangi değerlendirme gerekir?", "Metin özelliğiyle birlikte ön bilgi, sözcük bilgisi ve kullanılan strateji de incelenmelidir.", "Okurun süreci hiç etkili değildir.", "Her zor metin yanlıştır.", "Strateji değiştirmek gereksizdir.", "Anlama güçlüğünün birden çok kaynağı olabilir."),
    ])


def speaking_process_tasks():
    n = "tr-g06-turkce-note-017"
    return rows(n, [
        ("comprehension", "Konuşma sürecini planlamanın ilk adımı nedir?", "Amaç, dinleyici ve temel mesajı belirlemek", "Bütün cümleleri ezberlemek", "Yalnız süreyi doldurmak", "Soruları yasaklamak", "İçerik ve sunum kararları amaç ile dinleyiciye göre verilir."),
        ("comprehension", "Konuşmada giriş bölümünün işlevi hangisidir?", "Konuyu ve amacı tanıtıp dinleyicinin dikkatini hazırlamak", "Bütün ayrıntıları tekrarlamak", "Kaynakları gizlemek", "Sonucu açıklamadan bitirmek", "Giriş dinleyiciye yön ve bağlam verir."),
        ("comprehension", "Konuşma provaları neyi değerlendirmeye yardım eder?", "Süre, akış, anlaşılabilirlik ve ses kullanımını", "Yalnız kıyafeti", "Dinleyicinin notunu", "Salonun yaşını", "Prova sunum öncesi düzeltilebilir performans kanıtı sağlar."),
        ("application", "Üç dakikalık tanıtım konuşması hazırlayan öğrenci ne yapmalıdır?", "Bir ana mesaj seçip giriş-gelişme-sonuç için süre dağıtmalıdır.", "Beş ayrı konu eklemelidir.", "Girişi iki dakika sürdürmelidir.", "Sonucu kaldırmalıdır.", "Kısa sürede içerik önceliği ve zaman planı gerekir."),
        ("application", "Konuşmacı ana başlıktan sık sık uzaklaşıyor. Hangi araç yardımcı olur?", "Anahtar sözcüklerden oluşan kısa konuşma planı", "Tam metni ekrandan hızlı okumak", "Yeni konular eklemek", "Süreyi yok saymak", "Anahtar plan düşünce akışını korurken doğal konuşmayı destekler."),
        ("application", "Soru-cevap bölümünde cevabı bilmeyen konuşmacı nasıl davranmalıdır?", "Bilmediğini açıkça belirtip güvenilir kaynaktan kontrol edeceğini söylemelidir.", "Uydurma bilgi vermelidir.", "Soruyu soranı küçümsemelidir.", "Konuyu aniden kapatmalıdır.", "Dürüstlük ve doğrulama konuşmanın güvenilirliğini korur."),
        ("application", "Dinleyiciler kavramı anlamadığını belli ediyor. Konuşmacı ne yapmalıdır?", "Kavramı kısa örnekle yeniden açıklayıp anlayışı kontrol etmelidir.", "Aynı cümleyi daha hızlı söylemelidir.", "Dinleyiciyi suçlamalıdır.", "Konuyu açıklamadan geçmelidir.", "Geri bildirime göre açıklama biçimi uyarlanır."),
        ("analysis", "Konuşma bilgili fakat ana fikir sona kadar belirsiz kalıyor. Temel sorun nedir?", "İçerik hiyerarşisi ve geçişler planlanmamıştır.", "Kaynak sayısı fazladır.", "Konuşma çok yavaştır.", "Dinleyici bulunmamaktadır.", "Bilgi seçimi kadar düşüncelerin örgütlenmesi de anlaşılabilirliği belirler."),
        ("analysis", "Bir öğrenci metni ezberleyince küçük bir unutma anında bütünüyle duruyor. Daha dayanıklı yöntem hangisidir?", "Anahtar fikir ve geçişlere dayalı planla anlamı kendi cümleleriyle aktarmak", "Daha uzun metni ezberlemek", "Göz temasını kaldırmak", "Hiç prova yapmamak", "Kavramsal plan sözcük unutulsa da akışı sürdürür."),
        ("analysis", "Konuşmacı süreyi aştığı için sonuç bölümüne ulaşamıyor. Hangi prova verisi kullanılmalıdır?", "Her bölümün gerçek süresi ölçülüp düşük öncelikli ayrıntılar çıkarılmalıdır.", "Yalnız toplam sözcük sayısı artırılmalıdır.", "Giriş uzatılmalıdır.", "Saat kullanılmamalıdır.", "Bölüm bazlı süre kaydı içerik budamasını yönlendirir."),
        ("error-analysis", "Bir öğrenci “İyi konuşma, yazılı metni hiç durmadan okumaktır.” diyor. Hangi düzeltme doğrudur?", "İyi konuşma amaçlı plan, doğal aktarım, dinleyici etkileşimi ve uygun ses kullanımını gerektirir.", "Göz teması gereksizdir.", "Dinleyici konuşmayı etkilemez.", "Hızlı okumak tek ölçüttür.", "Konuşma yazılı metni seslendirmekten daha geniş bir iletişim sürecidir."),
    ])


def speaking_technique_tasks():
    n = "tr-g06-turkce-note-018"
    return rows(n, [
        ("comprehension", "Hazırlıklı konuşma hangi özelliği taşır?", "İçerik ve sunumun önceden planlanmasını", "Hiç düşünmeden başlamayı", "Kaynak kullanmamayı", "Dinleyiciyi yok saymayı", "Hazırlık araştırma, düzenleme ve prova içerir."),
        ("comprehension", "Tartışmada kullanılan temel iletişim tekniği hangisidir?", "İddiayı gerekçeyle sunup karşı görüşü dikkatle dinlemek", "Karşı tarafın sözünü kesmek", "Kişisel saldırı yapmak", "Kanıtları gizlemek", "Tartışma düşünce ve kanıtların saygılı karşılaştırılmasıdır."),
        ("comprehension", "Betimleyici konuşmada hangi ögeler etkilidir?", "Duyusal ayrıntı ve düzenli gözlem", "Yalnız sayısal işlem", "Kaynağı belirsiz hüküm", "Konudan bağımsız liste", "Betimleme dinleyicinin zihninde varlık veya ortam canlandırır."),
        ("application", "Bir deneyin nasıl yapıldığını anlatacak öğrenci hangi tekniği seçmelidir?", "Basamaklı açıklama ve gösterip yaptırma", "Serbest çağrışım", "Yalnız öyküleme", "Konuyla ilgisiz tartışma", "İşlem öğretimi sıra, araç ve güvenlik açıklaması gerektirir."),
        ("application", "Bir gezi anısını ilgi çekici anlatmak için hangi teknik uygundur?", "Olayları zaman sırasıyla öyküleyip seçilmiş ayrıntılar kullanmak", "Bütün olayları rastgele dizmek", "Yalnız tanım okumak", "Sonucu başta söyleyip ayrıntıları silmek", "Öyküleme olay, kişi, yer ve zaman akışı kurar."),
        ("application", "İki çözümün üstün ve zayıf yönlerini sunmak için hangi yöntem uygundur?", "Ölçütlere göre karşılaştırmalı konuşma", "Tek taraflı övgü", "Kaynakları saklama", "Sorunu değiştirme", "Ortak ölçütler adil karşılaştırma sağlar."),
        ("application", "Hazırlıksız kısa konuşmada düşünceleri düzenlemek için ne yapılabilir?", "Kısa bir giriş, iki temel nokta ve sonuç düzeni kurulabilir.", "Aklına gelen her konu eklenebilir.", "Sonuç kullanılmayabilir.", "Süre yok sayılabilir.", "Basit iskelet kısa sürede bütünlük sağlar."),
        ("analysis", "Konuşmacı tartışmada çok kanıt sunuyor fakat karşı görüşü yanlış aktarıyor. Hangi sorun vardır?", "Karşı görüşü adil temsil etmediği için değerlendirme güvenilir değildir.", "Kanıt kullanmak yanlıştır.", "Tartışmada karşı görüş bulunmaz.", "Yalnız ses tonu önemlidir.", "Eleştiri önce görüşü doğru anlamayı gerektirir."),
        ("analysis", "Bir tanıtım konuşması yalnız betimleme yapıyor, ürünün nasıl kullanılacağını açıklamıyor. Hangi teknik eklenmelidir?", "İşlem basamaklarını gösteren açıklayıcı anlatım", "Daha çok sıfat", "Yeni bir öykü", "Konuyla ilgisiz soru", "Kullanım amacı aşamalı açıklama gerektirir."),
        ("analysis", "Dinleyici uzmanlardan oluşuyorsa aynı konu için teknik nasıl uyarlanabilir?", "Temel tanımlar kısaltılıp kanıt ve yöntem ayrıntısı artırılabilir.", "Bütün kavramlar çocuklaştırılmalıdır.", "Kaynaklar kaldırılmalıdır.", "Dinleyici düzeyi önemsizdir.", "Teknik ve ayrıntı düzeyi ön bilgiye göre değişir."),
        ("error-analysis", "Bir öğrenci “Her konuşmada tek teknik kullanmak zorunludur.” diyor. Hangi düzeltme doğrudur?", "Amaç gerektiriyorsa açıklama, öyküleme, betimleme ve tartışma teknikleri birlikte kullanılabilir.", "Teknikler birbiriyle birleşemez.", "Konuşmanın amacı teknik seçimini etkilemez.", "Yalnız öyküleme geçerlidir.", "Bir konuşma farklı bölümlerde farklı işlevler taşıyabilir."),
    ])


def speaking_purpose_content_tasks():
    n = "tr-g06-turkce-note-019"
    return rows(n, [
        ("comprehension", "Konuşmada içerik seçimini belirleyen temel üçlü hangisidir?", "Amaç, konu ve dinleyici", "Salon, masa ve perde", "Süre, renk ve kıyafet", "Mikrofon, sandalye ve kapı", "İçerik iletişim amacına ve hedef kitleye göre sınırlandırılır."),
        ("comprehension", "Bilgilendirme amacıyla yapılan konuşmada hangi özellik önceliklidir?", "Doğru, açık ve düzenli bilgi", "Kanıtsız abartı", "Dinleyiciyi zorlamak", "Kaynağı gizlemek", "Bilgilendirme güvenilir içeriğin anlaşılır sunumunu gerektirir."),
        ("application", "Çocuklara su tasarrufunu anlatan konuşmada hangi içerik uygundur?", "Günlük yaşamdan uygulanabilir örnekler ve açık nedenler", "Yalnız teknik mevzuat maddeleri", "Karmaşık uzman hesapları", "Konuyla ilgisiz tarihçe", "Yaşa uygun somut örnekler davranışla bilgiyi bağlar."),
        ("application", "Bir öneri konuşmasında dinleyiciyi ikna etmek için ne kullanılmalıdır?", "Sorun, kanıt, uygulanabilir çözüm ve beklenen yarar", "Yalnız emir cümleleri", "Karşı görüşü küçümseme", "Kaynağı olmayan kesin vaat", "İkna, gerekçe ve uygulanabilirlik üzerine kurulmalıdır."),
        ("application", "Anma törenindeki konuşmada içerik nasıl seçilmelidir?", "Kişinin katkısını doğrulanmış örneklerle ve saygılı bir dille yansıtacak biçimde", "Doğrulanmamış söylentilerle", "Alaycı ve gündelik ifadelerle", "Konuyla ilgisiz reklamla", "Bağlam saygılı ton ve güvenilir anı bilgisi gerektirir."),
        ("analysis", "Bir konuşma amacını 'bilgilendirmek' diye belirtiyor fakat içeriğin çoğu ürün satın alma çağrısıdır. Sorun nedir?", "Açıklanan amaç ile gerçek içerik uyuşmamaktadır.", "Satın alma çağrısı her zaman bilgidir.", "Amaç içeriği etkilemez.", "Konuşma otomatik olarak tarafsızdır.", "İletişim niyeti içerik ve dil seçiminden anlaşılır."),
        ("analysis", "Aynı konu velilere ve öğrencilere anlatılacaktır. Hangi unsur değişebilir?", "Örnekler, terim açıklamaları ve eylem çağrısının düzeyi", "Temel gerçeklerin doğruluğu", "Kaynakların güvenilirliği", "Konunun kendisi", "Hedef kitle sunum biçimini değiştirir, doğruluğu değil."),
        ("analysis", "Konuşmacı çok ilginç ayrıntılar ekliyor fakat ana mesaj için süre kalmıyor. Hangi seçim yapılmalıdır?", "Amaçla doğrudan ilişkili içerik korunup düşük öncelikli ayrıntılar çıkarılmalıdır.", "Ana mesaj çıkarılmalıdır.", "Bütün ayrıntılar eşit tutulmalıdır.", "Süre sınırı yok sayılmalıdır.", "İçerik önceliği iletişim amacına göre belirlenir."),
        ("error-analysis", "Bir öğrenci “Dinleyici kim olursa olsun aynı örnek ve terimleri kullanırım.” diyor. Hangi düzeltme doğrudur?", "İçerik doğruluğu korunarak örnek ve açıklama düzeyi dinleyicinin ön bilgisine göre uyarlanmalıdır.", "Dinleyici içerik seçimini etkilemez.", "Uzman ve yeni başlayan aynı ön bilgiye sahiptir.", "Terimler hiçbir zaman açıklanmaz.", "Anlaşılabilirlik hedef kitleyi gözetir."),
        ("error-analysis", "Bir öğrenci “İkna etmek için kanıt yerine duyguyu abartmak yeterlidir.” diyor. Hangi değerlendirme gerekir?", "Duygusal bağ destekleyici olabilir; güvenilir kanıt ve mantıklı gerekçe temel olmalıdır.", "Abartı her iddiayı doğrular.", "Kanıt iknayı zayıflatır.", "Karşı görüş yok sayılmalıdır.", "Sorumlu ikna yanıltma yerine gerekçeli karar olanağı sağlar."),
        ("error-analysis", "Bir öğrenci “Konuşma amacı başta yazıldıysa içerikle uyumunu kontrol etmeye gerek yoktur.” diyor. Hangi düzeltme doğrudur?", "Her bölümün amaç ve ana mesaja hizmet edip etmediği konuşma boyunca denetlenmelidir.", "Amaç yazmak otomatik uyum sağlar.", "İçerik bağımsız seçilir.", "Sonuç bölümü amaç dışı olmalıdır.", "Planlanan amaç gerçek içerik seçimleriyle gerçekleştirilir."),
    ])


def voice_intro_tasks():
    return rows("tr-g06-turkce-note-020", [
        ("comprehension", "Konuşmada ses yüksekliği neye göre ayarlanmalıdır?", "Ortamın büyüklüğü, dinleyici uzaklığı ve iletişim amacına", "Yalnız konuşmacının isteğine", "Her zaman en yüksek düzeye", "Metindeki sözcük sayısına", "İşitilebilirlik ile rahatsız etmeme dengesi ortam ve dinleyiciye bağlıdır."),
        ("comprehension", "Vurgu konuşmada hangi işlevi görür?", "Önemli sözcük ve düşünceleri öne çıkarmayı", "Bütün sözcükleri eşitlemeyi", "Nefesi durdurmayı", "Konuyu değiştirmeyi", "Anlam odağı ses şiddeti, süre veya ton değişimiyle belirginleşir."),
    ])


TASK_BUILDERS = [prediction_tasks, reading_context_vocabulary_tasks, reading_surface_tasks,
                 reading_keywords_tasks, reading_word_wealth_tasks, reading_reflection_tasks,
                 speaking_process_tasks, speaking_technique_tasks,
                 speaking_purpose_content_tasks, voice_intro_tasks]


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1800:
        raise RuntimeError("validated first eighteen batches must exist before batch 19")
    notes = read_notes_only(TURKISH_SOURCE)
    tasks = [item for builder in TASK_BUILDERS for item in builder()]
    if len(tasks) != 100:
        raise AssertionError(f"batch 19 must contain 100 tasks, got {len(tasks)}")
    expected_modes = {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
    if Counter(item["mode"] for item in tasks) != expected_modes:
        raise AssertionError(Counter(item["mode"] for item in tasks))
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    rows_out = [make_record(local, item, notes[item["note"]], batch=19, number_base=1800)
                for local, item in enumerate(tasks, 1)]
    if Counter(row["correctIndex"] for row in rows_out) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer positions are not exactly balanced")
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":"))
                                 for row in existing + rows_out) + "\n", encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
    print(json.dumps({"batch": 19, "questions": 100, "turkish": 100, "figures": 0,
                      "total": 1900, "modes": dict(Counter(item["mode"] for item in tasks)),
                      "sourceQuestionReads": 0, "figureSpec": "1.3.0"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
