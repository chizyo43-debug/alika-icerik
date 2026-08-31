#!/usr/bin/env python3
"""Append the final 100 Grade 6 Turkish questions (batch 20)."""
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


def voice_tasks():
    n = "tr-g06-turkce-note-020"
    return rows(n, [
        ("comprehension", "Konuşma hızının etkili olması neye bağlıdır?", "Dinleyicinin takip edebileceği ve içeriğin gerektirdiği bir tempoya", "Her zaman çok hızlı olmaya", "Bütün cümleleri aynı sürede söylemeye", "Yalnız konuşmacının nefesine", "Uygun hız anlaşılabilirlik, vurgu ve amaçla birlikte ayarlanır."),
        ("comprehension", "Tonlama hangi bilgiyi iletebilir?", "Cümlenin duygu, tutum ve iletişim amacını", "Yalnız sözcük sayısını", "Metnin yazı tipini", "Konuşmacının boyunu", "Ses perdesindeki değişimler anlam ve duygu ayrımlarını destekler."),
        ("comprehension", "Doğru nefes kullanımı konuşmaya nasıl katkı sağlar?", "Cümleleri uygun yerlerde kesmeden ve sesi zorlamadan söylemeye", "Her sözcükte nefesi tutmaya", "Konuşmayı sürekli hızlandırmaya", "Vurguyu tamamen kaldırmaya", "Planlı nefes sesin sürekliliğini ve anlaşılabilirliği korur."),
        ("application", "Büyük salonda mikrofonsuz konuşan öğrencinin sesi arkaya ulaşmıyor. Ne yapmalıdır?", "Sesi bağırmadan destekli çıkarıp yüzünü dinleyiciye dönmeli ve uygun araç istemelidir.", "Sürekli fısıldamalıdır.", "Sözcük sonlarını yutmalıdır.", "Konuşma hızını iki katına çıkarmalıdır.", "İşitilebilirlik nefes desteği, yön ve ortam aracının birlikte düzenlenmesini gerektirir."),
        ("application", "Bir uyarı cümlesindeki en önemli güvenlik sözü nasıl belirginleştirilir?", "Sözü anlamlı vurgu ve kısa duraklamayla öne çıkararak", "Bütün cümleyi aynı tonda okuyarak", "Önemli sözü daha hızlı geçerek", "Cümlenin ortasını atlayarak", "Seçici vurgu dinleyicinin kritik bilgiye dikkatini çeker."),
        ("application", "Öğrenci uzun cümlede nefesi yetmediği için son kelimeleri anlaşılmaz söylüyor. Hangi çalışma uygundur?", "Anlam gruplarını işaretleyip uygun duraklarda nefes alarak prova yapmak", "Cümleyi tek nefeste hızla söylemek", "Son kelimeleri atlamak", "Nefes almadan ses yükseltmek", "Anlamlı duraklar hem nefes hem söz dizimi bütünlüğü sağlar."),
        ("analysis", "Konuşmacı heyecanlı bölümde hızlanıyor ancak dinleyici ayrıntıları kaçırıyor. En uygun uyarlama hangisidir?", "Heyecanı tonla korurken kritik bilgide hızı azaltıp duraklamak", "Daha da hızlanmak", "Bütün konuşmayı tekdüze yapmak", "Kritik bilgiyi çıkarmak", "Duygusal enerji ile anlaşılırlık dengelenebilir."),
        ("analysis", "Aynı cümle farklı vurgu yerleriyle iki anlam oluşturuyor. Bu neyi gösterir?", "Vurgunun cümlede bilgi odağını değiştirebildiğini", "Sözcüklerin anlamının yok olduğunu", "Sesin anlamla ilgisiz olduğunu", "Her vurgunun yanlış olduğunu", "Öne çıkarılan öğe dinleyicinin hangi karşıtlığı algılayacağını belirler."),
        ("error-analysis", "Bir öğrenci “Etkili ses kullanmak sürekli yüksek sesle konuşmaktır.” diyor. Hangi düzeltme doğrudur?", "Ses yüksekliği ortam ve anlama göre değiştirilmeli; hız, ton, vurgu ve nefesle dengelenmelidir.", "Yüksek ses her zaman ikna eder.", "Fısıltı bütün konuşmalar için uygundur.", "Tonlama gereksizdir.", "Etkililik tek bir ses özelliğinin sürekli kullanılmasına dayanmaz."),
    ])


def speaking_vocabulary_tasks():
    n = "tr-g06-turkce-note-021"
    return rows(n, [
        ("comprehension", "Konuşmada zengin söz varlığı neyi sağlar?", "Düşünceyi daha kesin, çeşitli ve bağlama uygun ifade etmeyi", "Her cümleyi uzatmayı", "Yabancı sözcükleri zorunlu kullanmayı", "Aynı sözü sürekli tekrarlamayı", "Sözcük çeşitliliği amaçla uyumlu olduğunda anlatım gücünü artırır."),
        ("comprehension", "Sözcük seçiminde dinleyici neden dikkate alınır?", "Terim ve açıklama düzeyini anlaşılır kılmak için", "Doğru bilgiyi değiştirmek için", "Kaynakları kaldırmak için", "Konuyu gizlemek için", "Aynı kavram farklı ön bilgi düzeylerinde farklı açıklama gerektirebilir."),
        ("comprehension", "Gereksiz sözcük tekrarını azaltmanın yolu hangisidir?", "Bağlama uygun zamir, eş veya yakın anlamlı ifadeler kullanmak", "Her cümleyi aynı sözcükle başlatmak", "Ana kavramı tamamen silmek", "Rastgele sözcük eklemek", "Çeşitlilik anlam bağını koruyarak tekrarı azaltır."),
        ("application", "'Güzel bir proje yaptık, güzel sonuçlar aldık.' cümlesi nasıl geliştirilir?", "Nitelikli bir proje hazırladık, yararlı sonuçlar elde ettik.", "Güzel güzel proje sonuç güzel.", "Proje yaptık sonuç.", "Aynı cümle değişmeden tekrarlanmalıdır.", "Daha özel sıfat ve fiiller anlamı belirginleştirir."),
        ("application", "Uzman olmayan dinleyiciye 'biyolojik çeşitlilik' terimi nasıl sunulmalıdır?", "Terimi koruyup canlı türleri ve yaşam ortamlarındaki çeşitlilik diye kısa açıklamak", "Terimi açıklamadan art arda kullanmak", "Yanlış bir günlük sözle değiştirmek", "Konuyu atlamak", "Doğru terim ile anlaşılır açıklama birlikte kullanılabilir."),
        ("application", "Bir tartışmada 'kötü' yerine sorunu açıkça belirten hangi ifade daha uygundur?", "Uygulanması pahalı ve erişimi sınırlı", "Hiç iyi değil", "Berbat bir şey", "Ben sevmiyorum, o kadar", "Ölçüt belirten dil görüşü gerekçelendirir."),
        ("application", "Konuşmacı yeni öğrendiği 'sürdürülebilir' sözünü kullanacaktır. Hangi cümle uygundur?", "Kaynağı tüketmeden uzun süre devam edebilen sürdürülebilir bir plan geliştirdik.", "Sürdürülebilir çok mavi bir sestir.", "Bugün sürdürülebilir koştum.", "Her plan yalnız sözcük yazılınca sürdürülebilir olur.", "Cümle kavramın süreklilik ve kaynak dengesi anlamını doğru taşır."),
        ("analysis", "Konuşmada çok sayıda teknik terim var, ancak tanım ve örnek yok. Dinleyici üzerindeki olası etki nedir?", "İçerik doğru olsa bile anlaşılabilirlik azalabilir.", "Terim sayısı anlamayı otomatik artırır.", "Örnekler her zaman gereksizdir.", "Dinleyici düzeyi önemli değildir.", "Terim yoğunluğu ön bilgiyle dengelenmelidir."),
        ("analysis", "İki sözcük yakın anlamlı ancak biri küçümseyici çağrışım taşıyor. Konuşmacı ne yapmalıdır?", "Amaç ve saygılı tonla uyuşan sözcüğü seçmelidir.", "Her zaman küçümseyici olanı kullanmalıdır.", "Çağrışımı yok saymalıdır.", "İki sözcüğü rastgele değiştirmelidir.", "Sözcükler sözlük anlamının yanında değerlendirme tonu taşır."),
        ("analysis", "Konuşmacı aynı düşünceyi atasözüyle destekliyor fakat atasözü bağlama uymuyor. Sorun nedir?", "Kalıplaşmış söz düşünceyi süslese de anlam ilişkisi kurulmamıştır.", "Her atasözü her konuya uyar.", "Atasözü kanıt yerine geçer.", "Bağlam konuşmada önemsizdir.", "Söz varlığı unsuru yalnız yerinde kullanıldığında anlatımı zenginleştirir."),
        ("error-analysis", "Bir öğrenci “Zengin konuşma için anlamını bilmediğim uzun sözcükleri kullanmalıyım.” diyor. Hangi düzeltme doğrudur?", "Anlamı bilinen, amaç ve dinleyiciye uygun sözcükler seçilmelidir.", "Uzunluk doğruluğu kanıtlar.", "Anlam önemli değildir.", "Yabancı sözcük her zaman üstündür.", "Söz varlığı gösteriş değil doğru ve etkili anlatım aracıdır."),
    ])


def speaking_reflection_tasks():
    n = "tr-g06-turkce-note-022"
    return rows(n, [
        ("comprehension", "Konuşma sonrası öz yansıtma hangi soruyla başlayabilir?", "Amacımı dinleyiciye açık ve kanıtlı biçimde aktarabildim mi?", "Mikrofonun markası neydi?", "Kaç sandalye vardı?", "Konuşmam en uzun muydu?", "Öz değerlendirme amaç ve performans kanıtına odaklanır."),
        ("comprehension", "Konuşma kaydı neden yararlı bir öz değerlendirme aracıdır?", "Hız, duraklama, tekrar ve ses özelliklerini sonradan somut biçimde inceletir.", "Dinleyiciyi gereksiz kılar.", "Bütün hataları otomatik düzeltir.", "İçeriğin doğruluğunu tek başına kanıtlar.", "Kayıt gözden kaçan performans ayrıntılarını yeniden dinleme olanağı verir."),
        ("comprehension", "Akran geri bildirimi nasıl kullanılmalıdır?", "Somut ölçütlerle karşılaştırılıp uygun geliştirme adımına dönüştürülerek", "Her yorum sorgusuz kabul edilerek", "Yalnız övgüler seçilerek", "Konuşmacının kendi kanıtı yok sayılarak", "Geri bildirim ölçüt ve öz gözlemle birlikte değerlendirilir."),
        ("application", "Öğrenci sunumda süreyi iki dakika aşıyor. Sonraki prova hedefi hangisidir?", "Düşük öncelikli iki ayrıntıyı çıkarıp her bölümü zamanlayarak süreye uymak", "Daha hızlı ve anlaşılmaz konuşmak", "Sonucu kaldırmak", "Süreyi ölçmemek", "İçerik budama ve bölüm süreleri soruna doğrudan çözüm getirir."),
        ("application", "Dinleyiciler örnekleri anlıyor fakat ana mesajı söyleyemiyor. Öğrenci neyi değiştirmelidir?", "Ana mesajı giriş ve sonuçta açıkça ifade edip örnekleri ona bağlamalıdır.", "Daha çok ilgisiz örnek eklemelidir.", "Ana mesajı gizlemelidir.", "Sonuç bölümünü kaldırmalıdır.", "Örneklerin hangi düşünceyi desteklediği görünür olmalıdır."),
        ("application", "Konuşmacı göz teması kurarken planını unutuyor. Hangi deneme uygundur?", "Tam metin yerine kısa anahtar kartlarla bölümler arasında bakış geçişi çalışmak", "Gözlerini sürekli kapatmak", "Bütün metni ekrandan okumak", "Planı kaldırmak", "Anahtar kart doğal aktarım ile yapısal desteği dengeler."),
        ("application", "Ses kaydında cümle sonlarının duyulmadığı fark ediliyor. Uygun hedef hangisidir?", "Cümle sonlarını tamamlayıp üç örnek cümlede anlaşılabilirliği yeniden kaydetmek", "Bütün konuşmayı bağırarak yapmak", "Daha hızlı konuşmak", "Son sözcükleri atlamak", "Ölçülebilir hedef belirlenen sesletim sorununa yönelir."),
        ("analysis", "İki sunum arasında başarı arttı ancak ikinci dinleyici grubu konuya daha hâkimdi. Sonuç nasıl yorumlanır?", "Gelişim olasıdır; konuşmacı etkisini görmek için benzer dinleyici grubuyla da deneme gerekir.", "Başarı kesin yalnız konuşmacıdan kaynaklanır.", "Dinleyici ön bilgisi önemsizdir.", "İlk sunum kaydı silinmelidir.", "Karşılaştırmada dinleyici farkı sonucu etkileyen değişkendir."),
        ("analysis", "Konuşmacı yalnız hatalarına odaklanıp işe yarayan yöntemleri kaydetmiyor. Ne kaybeder?", "Başarılı stratejileri sürdürme ve başka konuşmalara aktarma fırsatını", "Hata bulma becerisini", "Konuşma süresini", "Kaynak listesini", "Öz yansıtma güçlü yönleri de kanıtla belirlemelidir."),
        ("analysis", "Akran 'çok hızlı', konuşmacı 'normal' diyor. En güçlü çözüm hangisidir?", "Kaydı süre ve anlaşılabilirlik ölçütleriyle inceleyip belirli bölümlerdeki hızı karşılaştırmak", "İki görüşten rastgele birini seçmek", "Geri bildirimi yok saymak", "Konuşmayı tekrar dinlememek", "Somut ölçüm öz algı ile dış geri bildirimi uzlaştırır."),
        ("error-analysis", "Bir öğrenci “Konuşma bittikten sonra değiştirilecek bir şey kalmaz.” diyor. Hangi düzeltme doğrudur?", "Sonraki konuşmalar için kayıt ve geri bildirimden gelişim hedefi çıkarılabilir.", "Her konuşma tek seferliktir.", "Deneyim aktarılmaz.", "Öz değerlendirme yalnız not vermektir.", "Yansıtma gelecekteki planı iyileştirir."),
    ])


def writing_process_tasks():
    n = "tr-g06-turkce-note-023"
    return rows(n, [
        ("comprehension", "Planlı yazma sürecinin temel aşamaları hangileridir?", "Hazırlık, taslak oluşturma, gözden geçirme, düzeltme ve paylaşma", "Yalnız başlık yazma", "Doğrudan yayımlama", "Sadece yazım denetimi", "Yazı düşüncenin geliştirilip yeniden düzenlendiği aşamalı bir süreçtir."),
        ("comprehension", "Yazma öncesi amaç belirlemek neyi yönlendirir?", "İçerik, tür, ton ve kanıt seçimini", "Yalnız kâğıt boyutunu", "Sözcük sayısını rastgele artırmayı", "Kaynakları kaldırmayı", "İletişim amacı yazının bütün temel kararlarını etkiler."),
        ("comprehension", "Taslak neden son metin olarak görülmemelidir?", "Düşünce ve anlatımın geri bildirimle geliştirileceği ilk düzen olduğu için", "Taslakta cümle bulunmadığı için", "Taslak yalnız başlıktır.", "Taslak değiştirilemez.", "İlk yazım keşif ve örgütleme içerir; düzeltmeye açıktır."),
        ("application", "Öğrenci okul bahçesi için öneri yazacaktır. Hazırlıkta ne toplamalıdır?", "Sorun gözlemleri, kullanıcı görüşleri ve uygulanabilir çözüm bilgisi", "Yalnız kişisel beğenisini", "Konuyla ilgisiz alıntılar", "Kaynağı belirsiz sayılar", "Öneri gerçek gereksinim ve kanıtla temellendirilir."),
        ("application", "Taslakta aynı düşünce üç paragrafta tekrarlanıyor. Gözden geçirmede ne yapılmalıdır?", "Tekrarlar birleştirilip her paragrafa ayrı bir işlev verilmelidir.", "Tekrar sayısı artırılmalıdır.", "Bütün paragraflar silinmelidir.", "Başlık değiştirilip metin bırakılmalıdır.", "Paragraf işlevleri metnin ilerlemesini sağlar."),
        ("application", "Yazının sonucu yeni ve açıklanmamış bir fikir içeriyor. Nasıl düzeltilir?", "Yeni fikir gelişme bölümünde açıklanmalı ya da sonuçtan çıkarılmalıdır.", "Sonuca daha çok yeni fikir eklenmelidir.", "Giriş silinmelidir.", "Kaynaklar kaldırılmalıdır.", "Sonuç önceki düşünceleri bağlar; açıklanmamış sav başlatmaz."),
        ("application", "Akran geri bildirimi 'örnek yetersiz' diyor. Yazarın uygun adımı hangisidir?", "İddianın hangi bölümünde kanıt eksik olduğunu bulup ilgili örneği eklemek", "Her paragrafa rastgele örnek koymak", "Geri bildirimi aynen metne yazmak", "Ana düşünceyi değiştirmeden hiçbir şey yapmamak", "Geri bildirim somut metin gereksinimine çevrilmelidir."),
        ("analysis", "Bir yazı dil bilgisi bakımından doğru ancak düşünceler dağınık. Hangi aşama önceliklidir?", "Paragraf sırası ve düşünce bağlantılarını yeniden düzenleme", "Yalnız noktalama düzeltme", "Sözcükleri uzatma", "Metni hemen yayımlama", "Büyük yapısal sorunlar yüzey düzeltmelerinden önce ele alınır."),
        ("analysis", "Yazar her cümleyi yazarken kusursuzlaştırmaya çalıştığı için taslak ilerlemiyor. Hangi yöntem uygundur?", "Önce düşünce akışını tamamlayıp düzeltmeyi ayrı turda yapmak", "Her sözcükte uzun süre beklemek", "Taslak aşamasını kaldırmak", "Yazmayı bırakmak", "Üretim ve düzeltme odaklarını ayırmak ilerlemeyi kolaylaştırır."),
        ("analysis", "İki geri bildirim çelişiyor: biri ayrıntı ekle, diğeri kısalt diyor. Yazar ne yapmalıdır?", "Amaç ve hedef okura göre hangi bölümün gerekli olduğunu kanıtla değerlendirmelidir.", "İki öneriyi de düşünmeden uygulamalıdır.", "Rastgele birini seçmelidir.", "Metni silmelidir.", "Geri bildirim kararını metnin amacı belirler."),
        ("error-analysis", "Bir öğrenci “İlk taslak bittiyse yazı tamamdır.” diyor. Hangi düzeltme doğrudur?", "İçerik, yapı, dil ve yazım ayrı gözden geçirme turlarında iyileştirilmelidir.", "Taslak değiştirilemez.", "Düzeltme yalnız kötü yazarlara gerekir.", "Paylaşma aşaması ilk sıradadır.", "Nitelikli yazı çoğunlukla yeniden yazmayla oluşur."),
    ])


def writing_strategy_tasks():
    n = "tr-g06-turkce-note-024"
    return rows(n, [
        ("comprehension", "Serbest yazma tekniği hangi amaçla kullanılabilir?", "Kısa sürede düşünce üretip yazma engelini aşmak", "Son metni düzeltmesiz yayımlamak", "Kaynakları gizlemek", "Her cümleyi aynı kalıpta kurmak", "Serbest yazma ilk fikir üretimine odaklanır; sonra düzenleme gerekir."),
        ("comprehension", "Kavram haritası yazmaya nasıl yardımcı olur?", "Ana fikir ve alt düşünceler arasındaki bağlantıları görselleştirir.", "Noktalama işaretlerini otomatik seçer.", "Kaynak doğruluğunu tek başına kanıtlar.", "Metni yazarsız oluşturur.", "İlişki haritası içerik örgütlemesini destekler."),
        ("comprehension", "Karşılaştırmalı yazıda hangi yapı önemlidir?", "İki konuyu ortak ölçütler üzerinden değerlendirmek", "Her konu için farklı ve ilgisiz ölçüt kullanmak", "Yalnız birini anlatmak", "Sonucu kanıtsız vermek", "Ortak ölçüt adil ve izlenebilir karşılaştırma sağlar."),
        ("application", "Öğrenci bir olay öyküsü yazacaktır. Hangi plan uygundur?", "Kişi, amaç, çatışma, dönüm noktası ve sonuç sırası", "Yalnız sıfat listesi", "Kaynakça düzeni", "Tanım ve madde işaretleri", "Öyküleme olay gelişimi ve değişim gerektirir."),
        ("application", "Bir işlemi öğreten metin için hangi yöntem seçilmelidir?", "Numaralı aşamalar, gerekli araçlar ve güvenlik uyarıları", "Zaman sırası olmayan anılar", "Yalnız benzetmeler", "Sonucu gizleyen şiir", "Yönerge açık sıra ve uygulanabilir ayrıntı gerektirir."),
        ("application", "Tartışmacı yazıda karşı görüş nasıl kullanılmalıdır?", "Adil biçimde sunulup kanıtla yanıtlanmalıdır.", "Çarpıtılıp küçümsenmelidir.", "Tamamen gizlenmelidir.", "Kaynak gösterilmeden reddedilmelidir.", "Karşı görüşe gerekçeli yanıt savı güçlendirir."),
        ("application", "Fikir üretmekte zorlanan öğrenci hangi iki tekniği sıralı kullanabilir?", "Beyin fırtınasıyla seçenek üretip ölçütlerle eleme", "İlk fikri seçip araştırmayı bırakma", "Yalnız yazım denetimi yapma", "Başlığı kopyalama", "Üretim ve seçim farklı bilişsel aşamalardır."),
        ("analysis", "Öğrenci açıklayıcı metinde yoğun öyküleme kullanıyor ve kavramın tanımı belirsiz kalıyor. Ne yapılmalıdır?", "Öykü örnek olarak korunup tanım ve neden-sonuç açıklaması güçlendirilmelidir.", "Bütün açıklamalar kaldırılmalıdır.", "Daha çok karakter eklenmelidir.", "Kavram hiç adlandırılmamalıdır.", "Teknik yazının baskın amacına hizmet etmelidir."),
        ("analysis", "Bir metin problem-çözüm düzeninde başlıyor fakat sonuçta karşılaştırmaya geçiyor. Hangi kontrol gerekir?", "Seçilen yapının baştan sona ana amaca hizmet edip etmediği", "Yalnız sözcük sayısı", "Yazı tipi", "Paragraf renginin aynı olması", "Yapısal tutarlılık okurun düşünce akışını izlemesini sağlar."),
        ("analysis", "Aynı yazıda günlük biçimi ve resmî rapor dili karışıyor. Ne belirlenmelidir?", "Hedef tür, okur ve amaç için baskın anlatım yöntemi", "Her paragrafta yeni tür", "Yalnız başlık uzunluğu", "Kaynakların kaldırılması", "Türsel seçim ton ve yapı bütünlüğü sağlar."),
        ("error-analysis", "Bir öğrenci “Bir yazma tekniği seçince metin boyunca başka teknik kullanamam.” diyor. Hangi düzeltme doğrudur?", "Baskın tekniği desteklemek için amaca uygun başka teknikler kullanılabilir.", "Teknikler hiçbir zaman birleşmez.", "Örnek vermek yapıyı bozar.", "Amaç teknik seçimini etkilemez.", "Açıklama içinde örnek veya öykü gibi destekler yer alabilir."),
    ])


def writing_content_structure_tasks():
    n = "tr-g06-turkce-note-025"
    return rows(n, [
        ("comprehension", "Paragrafın ana düşüncesi neyi sağlar?", "Cümlelerin hangi ortak noktayı geliştireceğini", "Her cümlenin bağımsız konuya geçmesini", "Yalnız başlığın uzunluğunu", "Noktalama sayısını", "Paragraf bütünlüğü merkezi düşünce çevresinde kurulur."),
        ("comprehension", "Bağdaşıklık hangi araçlarla güçlenir?", "Gönderimler, bağlaçlar ve uygun sözcük tekrarlarıyla", "Rastgele zaman değişimleriyle", "İlgisiz cümlelerle", "Her cümlede yeni kişiyle", "Dilsel bağlar cümlelerin birbirine nasıl tutunduğunu gösterir."),
        ("comprehension", "Giriş ile sonuç arasındaki ilişki nasıl olmalıdır?", "Girişte kurulan amaç ve sorular sonuçta karşılanmalıdır.", "Sonuç bütünüyle yeni konu açmalıdır.", "Giriş sonuçla ilgisiz olmalıdır.", "İki bölüm aynı cümleyi tekrarlamalıdır.", "Metinsel kapanış başlangıçtaki yönü tamamlar."),
        ("application", "Paragrafta dört cümle kent ulaşımını, biri evcil hayvan bakımını anlatıyor. Ne yapılmalıdır?", "Evcil hayvan cümlesi çıkarılmalı veya ilgili başka paragrafa taşınmalıdır.", "Ulaşım cümleleri silinmelidir.", "Bütün cümleler aynı paragrafta kalmalıdır.", "Başlık evcil hayvan yapılmalıdır.", "İlgisiz cümle paragrafın konu bütünlüğünü bozar."),
        ("application", "'Bu nedenle' bağlacı hangi durumda uygundur?", "Önceki cümledeki nedenin sonucunu verirken", "Karşıt düşünceye geçerken", "Örnek listesine başlarken", "Zamanı belirsizleştirirken", "Bağlaç neden-sonuç ilişkisini açıklar."),
        ("application", "Bir raporda bulgu ve yorum birbirine karışmış. Nasıl düzenlenir?", "Ölçülen sonuçlar ayrı, bu sonuçlara dayalı çıkarımlar ayrı sunulur.", "Bütün sayılar kaldırılır.", "Yorumlar bulgu diye yazılır.", "Kaynaklar gizlenir.", "Bilgi türlerini ayırmak raporun denetlenmesini kolaylaştırır."),
        ("application", "Öyküde karakterin kararı için hiçbir hazırlık yok. Hangi içerik eklenmelidir?", "Kararı açıklayan önceki olay, amaç veya iç çatışma", "İlgisiz mekân listesi", "Yeni başlıklar", "Sonuçtan sonra rastgele kişi", "Nedensel hazırlık karakter eylemini inandırıcı kılar."),
        ("analysis", "Metin her paragrafta aynı ana düşünceyi farklı sözlerle tekrarlıyor. Hangi yapısal değişiklik gerekir?", "Her paragrafa savı ilerleten ayrı alt düşünce ve kanıt verilmelidir.", "Tekrarlar artırılmalıdır.", "Paragraflar rastgele sıralanmalıdır.", "Ana düşünce kaldırılmalıdır.", "Metin ilerleme göstermeli, yalnız döngüsel tekrar yapmamalıdır."),
        ("analysis", "Bağlaçlar dil bilgisel olarak doğru fakat düşünceler arasında gerçek ilişki yok. Bu neyi gösterir?", "Yüzeysel bağdaşıklığın tek başına anlamsal tutarlılık sağlamadığını", "Bağlaç varsa metin mutlaka tutarlıdır.", "Anlam ilişkisi gereksizdir.", "Her bağlaç aynı işlevdedir.", "Dilsel işaret ile düşünsel bağlantı uyumlu olmalıdır."),
        ("analysis", "Sonuç paragrafı ana savı tekrar ediyor fakat kanıtların önemini açıklamıyor. Nasıl geliştirilir?", "Temel bulguların savı neden desteklediği birleştirilerek gösterilir.", "Yeni kanıtsız sav eklenir.", "Gelişme bölümü aynen kopyalanır.", "Sonuç kaldırılır.", "Sentez, tekrarın ötesinde kanıtların ortak anlamını kurar."),
        ("error-analysis", "Bir öğrenci “Her paragrafın konusu farklı olursa metin daha zengin olur.” diyor. Hangi düzeltme doğrudur?", "Alt konular farklılaşabilir ancak hepsi ortak amaç ve ana düşünceye bağlanmalıdır.", "Paragraflar ilişkisiz olmalıdır.", "Ana düşünce metni sınırlar.", "Geçişler gereksizdir.", "Zenginlik konu dağınıklığı değil örgütlü ayrıntıdır."),
    ])


def writing_vocabulary_tasks():
    n = "tr-g06-turkce-note-026"
    return rows(n, [
        ("comprehension", "Yazıda söz varlığını zengin kullanmak ne demektir?", "Amaca ve bağlama uygun, anlamı belirginleştiren çeşitli sözler seçmek", "Her cümleye bilinmeyen sözcük eklemek", "Aynı deyimi sürekli tekrarlamak", "Metni gereksiz yere uzatmak", "Zenginlik, gösterişten çok doğru ve etkili sözcük seçimine dayanır."),
        ("comprehension", "Bir deyimin yazıya katkı sağlaması için hangi koşul gereklidir?", "Anlamının anlatılan durumla örtüşmesi", "Mümkün olduğunca uzun olması", "Her paragrafta kullanılması", "Sözcüklerinin değiştirilmesi", "Deyimler kalıplaşmıştır ve ancak bağlama uygun kullanıldığında anlatımı güçlendirir."),
        ("application", "'Bahçe güzeldi.' cümlesini gözleme dayalı ve canlı anlatan seçenek hangisidir?", "Yağmur damlalarıyla parlayan laleler bahçeye canlılık katıyordu.", "Bahçe çok çok güzeldi.", "Bahçe güzellik bakımından güzeldi.", "Bahçede bir şeyler vardı.", "Somut ayrıntı ve güçlü fiil okurun zihninde belirgin bir görüntü oluşturur."),
        ("application", "Bir raporda 'çok kötü hava' yerine ölçülebilir hangi ifade kullanılmalıdır?", "Görüş uzaklığını azaltan yoğun sis", "Felaket bir hava", "İnanılmaz kötü hava", "Bence hoş olmayan hava", "Nesnel yazıda genel yargı yerine gözlenebilir özellik belirtilir."),
        ("application", "'Arkadaşım bana yardım etti.' cümlesinde dayanışmayı vurgulayan uygun deyim hangisidir?", "Arkadaşım zor günümde bana omuz verdi.", "Arkadaşım kulağının üstüne yattı.", "Arkadaşım baltayı taşa vurdu.", "Arkadaşım ağzından baklayı çıkardı.", "Omuz vermek, destek olmak anlamıyla bağlama uygundur."),
        ("application", "Yazar 'sakin' sözcüğünü art arda üç kez kullanmıştır. En uygun düzeltme hangisidir?", "Anlama göre 'dingin' ve 'telaşsız' gibi yakın anlamlı sözlerle tekrarları azaltmak", "Sakin sözcüğünün her tekrarını büyük harfle yazmak", "Bütün cümleleri silmek", "Anlamı farklı rastgele sıfatlar eklemek", "Yakın anlamlı sözcükler bağlam denetlenerek kullanılmalıdır."),
        ("analysis", "'Soğuk oda' ile 'soğuk tavır' ifadelerindeki 'soğuk' sözcükleri nasıl ayrılır?", "İlkinde duyuyla algılanan gerçek, ikincide ilgisizliği anlatan mecaz anlam vardır.", "İkisi de yalnız soyut anlamdadır.", "İkisi de aynı varlığı adlandırır.", "İkinci kullanım anlamsızdır.", "Bağlam aynı sözcüğün gerçek ve mecaz kullanımını belirler."),
        ("analysis", "Bir çocuk öyküsünde çok eski ve açıklanmamış sözcükler olay akışını kesiyor. Yazarın en uygun kararı nedir?", "Gerekli olanları bağlamla açıklayıp diğerlerini hedef okura uygun sözlerle değiştirmek", "Bütün eski sözcükleri korumak", "Olayları çıkarmak", "Sözlükteki en uzun karşılıkları seçmek", "Sözcük seçimi tür, amaç ve okurun ön bilgisiyle dengelenir."),
        ("error-analysis", "Bir öğrenci “Eş anlamlı sözcükleri her bağlamda birbirinin yerine kullanabilirim.” diyor. Hata nedir?", "Yakın anlamlı sözlerin çağrışım ve kullanım alanları farklı olabilir.", "Eş anlamlıların yazılışı aynıdır.", "Bağlam sözcük anlamını etkilemez.", "Bütün sözcükler zıt anlamlıdır.", "Sözcük seçerken cümledeki anlam ve ton sınanmalıdır."),
        ("error-analysis", "Bir öğrenci “Ayağını yorganına göre uzat sözü hızlı koşmamızı öğütler.” diyor. Yanlış nasıl düzeltilir?", "Atasözü harcamaları imkânlara göre ayarlamayı öğütler.", "Atasözü spor yapmayı öğütler.", "Yorganın boyunu ölçmeyi anlatır.", "Sözün hiçbir mecaz anlamı yoktur.", "Kalıplaşmış söz gerçek anlamdaki eylemle değil aktardığı öğütle yorumlanır."),
        ("error-analysis", "Bir öğrenci “Yazıyı etkileyici yapmak için her cümlede farklı mecaz kullanmalıyım.” diyor. Ne yapmalıdır?", "Ana düşünceye hizmet etmeyen mecazları çıkarıp az ve yerinde kullanmalıdır.", "Daha fazla mecaz eklemelidir.", "Ana düşünceyi tamamen kaldırmalıdır.", "Mecazların anlamını rastgele değiştirmelidir.", "Söz sanatlarının yoğunluğu anlamın açıklığını bozmamalıdır."),
    ])


def spelling_punctuation_tasks():
    n = "tr-g06-turkce-note-027"
    return rows(n, [
        ("comprehension", "Nokta hangi temel görevde kullanılır?", "Tamamlanmış cümlenin sonunda", "Her soru cümlesinin başında", "Alıntının iki yanında", "Sıralı sözcüklerin arasında", "Nokta, yargısı tamamlanan cümleyi kapatır."),
        ("comprehension", "Özel adlara getirilen çekim ekleri nasıl yazılır?", "Kesme işaretiyle ayrılır.", "Her zaman bitişik ve küçük harfle yazılır.", "Kısa çizgiyle ayrılır.", "Parantez içine alınır.", "Kişi ve yer gibi özel adlara gelen çekim eklerinde kesme kullanılır."),
        ("application", "Hangi cümlede virgül sıralanan eş görevli sözleri doğru ayırmıştır?", "Çantama defter, kalem, cetvel ve silgi koydum.", "Dolaba, kitap kalem ve boya yerleştirdim.", "Masada silgi kalem, makas ve kâğıt vardı.", "Sepete elma armut üzüm ve, incir koyduk.", "Virgül, bağlaçtan önceki sıralı adları birbirinden ayırır."),
        ("application", "Hangi yazım doğrudur?", "Ankara'ya yarın sabah gideceğiz.", "Ankaraya bu akşam yola çıkacağız.", "istanbul'a hafta sonu varacağız.", "İzmir-e trenle gideceğiz.", "Şehir adı büyük harfle başlar ve çekim eki kesmeyle ayrılır."),
        ("application", "Birinin sözünü aynen aktarmadan önce iki noktanın doğru kullanıldığı cümle hangisidir?", "Öğretmen şöyle dedi: Yarın erken gelin.", "Müdür şu uyarıyı yaptı, Koridorda koşmayın.", "Antrenör sordu? Hazır mısınız.", "Başkan konuştu; çünkü Toplantı başladı.", "Açıklama veya örnek niteliğindeki aktarımdan önce iki nokta kullanılabilir."),
        ("application", "Doğrudan soru bildiren ve doğru noktalanan cümle hangisidir?", "Toplantı saat kaçta başlayacak?", "Servisin ne zaman geleceğini merak ettim?", "Bana neden geciktiğini anlattı!", "Yarın kimin nöbetçi olduğunu biliyorum:", "Doğrudan soru bildiren cümlenin sonuna soru işareti konur; dolaylı soru cümlesi soru işareti almaz."),
        ("analysis", "'Pazardan elma armut muz aldık.' cümlesinde anlamı izlenir kılmak için ne yapılmalıdır?", "Elma ve armuttan sonra virgül getirilmelidir.", "Pazardan sonra soru işareti getirilmelidir.", "Muz sözcüğü büyük harfle yazılmalıdır.", "Cümlenin sonuna iki nokta getirilmelidir.", "Eş görevli sıralı adlar virgülle ayrılır; cümle noktayla biter."),
        ("analysis", "'Eyvah, anahtarımı içeride unuttum?' cümlesinde hangi değişiklik uygundur?", "Cümle güçlü duygu bildirdiği için son işaret ünlem olmalıdır.", "Virgül kaldırılıp iki nokta konmalıdır.", "Anahtarımı büyük harfle yazılmalıdır.", "Soru işaretiyle birlikte nokta eklenmelidir.", "Cümle bilgi istemiyor; şaşkınlık ve kaygı bildiriyor."),
        ("analysis", "'29 ekim Cumhuriyet Bayramı'nı kutladık.' cümlesinde hangi iki düzeltme gerekir?", "'Ekim' büyük harfle başlamalı ve bayram adına gelen ek doğru kesmeyle ayrılmalıdır.", "Yalnız 29 yazıyla yazılmalıdır.", "Cumhuriyet küçük harfle başlamalıdır.", "Bayramı sözcüğünden sonra soru işareti gelmelidir.", "Belirli tarihlerin ay adı ve resmî bayram adları büyük harfle yazılır."),
        ("error-analysis", "Bir öğrenci “Konuşurken durduğum her yere virgül koyarım.” diyor. Hangi ilke bu yanlışı düzeltir?", "Virgül yalnız nefese göre değil cümledeki görev ve anlam ilişkisine göre konur.", "Her iki sözcükten sonra virgül konur.", "Virgül yalnız uzun cümlede kullanılır.", "Virgül bütün noktalama işaretlerinin yerine geçer.", "Noktalama konuşma nefesini değil yazılı yapıyı ve anlamı gösterir."),
        ("error-analysis", "Bir öğrenci “Türkiye Büyük Millet Meclisi'ne yazımında kesme doğrudur.” diyor. Sorun nedir?", "Kısaltılmadan yazılan kurum adına gelen ek kesmeyle ayrılmamalıdır.", "Türkiye küçük harfle başlamalıdır.", "Büyük sözcüğü çıkarılmalıdır.", "Ek kısa çizgiyle ayrılmalıdır.", "Kurum ve kuruluş adlarına gelen ekler ad açık yazıldığında kesmeyle ayrılmaz."),
    ])


def writing_reflection_tasks():
    n = "tr-g06-turkce-note-028"
    return rows(n, [
        ("comprehension", "Yazma sürecinde öz yansıtmanın amacı nedir?", "Yazarın kanıta dayalı güçlü ve gelişmesi gereken yönlerini belirlemesi", "Yalnız yazıya not vermesi", "Metni başkasına bırakması", "İlk taslağı değişmez kabul etmesi", "Öz yansıtma, sonraki düzenleme ve öğrenme kararlarını yönlendirir."),
        ("comprehension", "Bir geliştirme hedefinin ölçülebilir olması ne sağlar?", "Sonraki metinde ilerlemenin somut göstergelerle izlenmesini", "Bütün sorunların kendiliğinden çözülmesini", "Geri bildirimin gereksizleşmesini", "Metin türünün değişmesini", "Belirli davranış ve ölçütler ilerlemeyi görünür kılar."),
        ("comprehension", "Yazarın başarılı bulduğu bir yöntemi kaydetmesi neden önemlidir?", "Yöntemi benzer yazma görevlerine bilinçli biçimde aktarabilmesi için", "Her metni aynı yapmak için", "Düzeltmeyi bırakmak için", "Okur görüşünü yok saymak için", "Yansıtma yalnız hata değil işe yarayan stratejiler hakkında da bilgi üretir."),
        ("application", "Öğrenci öyküsünde zaman sırasının karıştığını fark ediyor. En uygun uyarlama hangisidir?", "Olay kartlarını kronolojik dizip gerekli geçiş sözleriyle taslağı yeniden kurmak", "Yalnız başlığı değiştirmek", "Yazım yanlışlarını düzeltip bırakmak", "Son paragrafı silmek", "Belirlenen yapısal soruna doğrudan süreç ve metin değişikliği yapılır."),
        ("application", "Öğretmen 'iddiaların kanıtsız' geri bildirimini veriyor. Öğrenci ne yapmalıdır?", "Her temel iddia için güvenilir bilgi veya örnek ekleyip bağlantısını açıklamak", "Daha kesin bir ton kullanmak", "Kaynakları çıkarmak", "Aynı iddiayı üç kez yazmak", "Kanıt eksikliği tekrar ya da tonla değil ilgili dayanakla giderilir."),
        ("application", "Öğrenci son üç yazısında uzun cümlelerin anlaşılmadığını görüyor. Hangi hedef uygundur?", "Bir sonraki taslakta her uzun cümleyi yargı ve bağlaç bakımından denetleyip gerekirse bölmek", "Bütün cümleleri üç sözcüğe indirmek", "Yalnız kısa sözcük kullanmak", "Okura danışmadan yayımlamak", "Hedef belirli soruna yönelik, uygulanabilir ve denetlenebilirdir."),
        ("application", "Akran değerlendirmesinde iki kişi sonucu belirsiz buluyor. Yazarın ilk adımı ne olmalıdır?", "Sonucun ana düşünceyi nasıl bağladığını ölçütle inceleyip gerekli yeniden yazmayı yapmak", "Yorumları sayıca az diye yok saymak", "Giriş bölümünü silmek", "Yeni bir konuya geçmek", "Tekrarlanan geri bildirim metin kanıtıyla sınanıp düzenlemeye dönüştürülür."),
        ("analysis", "Yazar 'metnim akıcı' diyor fakat nerede ve neden olduğunu gösteremiyor. Değerlendirmenin eksiği nedir?", "Yargıyı destekleyen cümle, geçiş veya okur geri bildirimi gibi kanıt yoktur.", "Metin mutlaka akıcı değildir.", "Öz değerlendirmede olumlu yön söylenemez.", "Akıcılık yalnız yazım kurallarıdır.", "Geçerli öz yansıtma genel izlenimi somut metin göstergesine bağlar."),
        ("analysis", "İlk taslakta betimleme zayıf, ikinci taslakta ayrıntı çok fazla olduğu için olay yavaşlıyor. Nasıl yorumlanmalıdır?", "Gelişim vardır ancak ayrıntıların olayın amacıyla dengelenmesi gerekir.", "İkinci taslak bütünüyle başarısızdır.", "Her ayrıntı korunmalıdır.", "İlk taslağa hiç bakılmamalıdır.", "Uyarlama bir sorunu çözerken yeni bir dengesizlik oluşturabilir; sonuç yeniden ölçülür."),
        ("analysis", "Yazar yalnız öğretmenin düzeltmelerini kopyalıyor, nedenlerini açıklayamıyor. Hangi beceri eksiktir?", "Geri bildirimi ilkeye dönüştürüp yeni durumlara uyarlama", "El yazısı hızı", "Başlık seçme", "Kaynak sıralama", "Öğrenme, düzeltmenin gerekçesini anlayıp bağımsız uygulamayı gerektirir."),
        ("error-analysis", "Bir öğrenci 'Öz değerlendirmede yalnız yanlışlar yazılır.' diyor. Hangi düzeltme doğrudur?", "Güçlü yönler, sorunlar, kanıtlar ve sonraki adımlar birlikte belirlenir.", "Yalnız yazım yanlışları sayılır.", "Başarılar değerlendirmeyi bozar.", "Sonraki hedefe gerek yoktur.", "Dengeli yansıtma korunacak ve geliştirilecek davranışları gösterir."),
        ("error-analysis", "Bir öğrenci “Çelişseler bile bütün geri bildirimleri metnime eklemeliyim.” diyor. Ne yapmalıdır?", "Yorumları amaç, tür ve hedef okur ölçütleriyle değerlendirip gerekçeli seçim yapmalıdır.", "Her yorumu mutlaka uygulamalıdır.", "Hiç geri bildirim almamalıdır.", "Metni rastgele kısaltmalıdır.", "Yazar geri bildirimin uygunluğunu denetleyen etkin karar vericidir."),
        ("error-analysis", "Bir öğrenci “Bir kez iyi not aldıysam aynı plan her konuya uyar.” diyor. Bu düşüncedeki hata nedir?", "Strateji yeni tür, amaç ve okura göre uyarlanmalıdır.", "Başarılı yöntemler hiçbir zaman tekrarlanmaz.", "Plan yalnız şiirde kullanılır.", "Konu yazma kararlarını etkilemez.", "Öz yansıtma başarıyı körü körüne kopyalamak değil koşullara göre aktarmaktır."),
        ("error-analysis", "Bir öğrenci “Düzeltme yaptım; önceki ve sonraki metni karşılaştırmam gerekmez.” diyor. Hangi eksik giderilmelidir?", "Değişikliğin hedeflenen sorunu çözüp çözmediği metin kanıtıyla kontrol edilmelidir.", "İlk taslak silinmelidir.", "Yalnız değişiklik sayısı yazılmalıdır.", "Her değişiklik başarılı kabul edilmelidir.", "Uyarlamanın etkisi karşılaştırma ve ölçütle doğrulanır."),
    ])


TASK_BUILDERS = [
    voice_tasks,
    speaking_vocabulary_tasks,
    speaking_reflection_tasks,
    writing_process_tasks,
    writing_strategy_tasks,
    writing_content_structure_tasks,
    writing_vocabulary_tasks,
    spelling_punctuation_tasks,
    writing_reflection_tasks,
]


def main():
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    if len(existing) == 2000 and all(str(row.get("id", "")).startswith("tr-g06-bank-turkce-b20-") for row in existing[-100:]):
        existing = existing[:1900]
    if len(existing) != 1900:
        raise SystemExit(f"batch 20 expects 1900 records or its own replaceable output, found {len(existing)}")
    notes = read_notes_only(TURKISH_SOURCE)
    tasks = [item for builder in TASK_BUILDERS for item in builder()]
    if len(tasks) != 100:
        raise AssertionError(f"expected 100 tasks, found {len(tasks)}")
    expected_modes = {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
    if Counter(item["mode"] for item in tasks) != expected_modes:
        raise AssertionError(Counter(item["mode"] for item in tasks))
    records = [make_record(local, item, notes[item["note"]], batch=20, number_base=1900)
               for local, item in enumerate(tasks, 1)]
    if Counter(record["subject"] for record in records) != {"Türkçe": 100}:
        raise AssertionError(Counter(record["subject"] for record in records))
    if Counter(record["correctIndex"] for record in records) != {0: 25, 1: 25, 2: 25, 3: 25}:
        raise AssertionError(Counter(record["correctIndex"] for record in records))
    if any(record.get("figure") is not None for record in records):
        raise AssertionError("batch 20 must not contain decorative figures")
    OUTPUT.write_text("\n".join(json.dumps(record, ensure_ascii=False, separators=(",", ":"))
                                  for record in existing + records) + "\n",
                      encoding="utf-8", newline="\n")
    print(json.dumps({"batch": 20, "added": len(records), "total": len(existing) + len(records), "subjects": dict(Counter(r["subject"] for r in records)), "modes": dict(Counter(item["mode"] for item in tasks))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
