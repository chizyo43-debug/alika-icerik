#!/usr/bin/env python3
"""Finish Grade 6 social studies (84) and start Turkish (16) in batch 17."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

from author_grade6_bilisim_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade6_fen_batch07 import task
from author_grade6_fen_english_batch10 import make_record
from author_grade6_mixed_batch03 import read_notes_only

SOCIAL_SOURCE = Path("turkiye/6-sinif/sosyal-bilgiler/sosyal-bilgiler-tum.jsonl")
TURKISH_SOURCE = Path("turkiye/6-sinif/turkce/turkce-tum.jsonl")


def vrows(note: str, values: list[tuple[str, str, str, str, str, str, str, str | None]]):
    result = []
    for mode, stem, correct, w1, w2, w3, explanation, visual in values:
        item = task(note, mode, stem, correct, [w1, w2, w3], explanation,
                    figure_kind=(visual.split(":", 1)[0] if visual else None))
        if visual:
            item["visual_payload"] = visual
        result.append(item)
    return result


def remaining_rights_tasks():
    n = "tr-g06-sosyal-bilgiler-note-012"
    return vrows(n, [
        ("comprehension", "Çocukların eğitim hakkı hangi toplumsal sonuca katkı sağlar?", "Bilgi ve becerilerini geliştirerek topluma katılmalarına", "Diğer hakların kaldırılmasına", "Yalnız sınav sayısının artmasına", "Çocukların karar süreçlerinden dışlanmasına", "Eğitim bireyin gelişimini ve toplumsal katılımını destekler.", None),
        ("application", "Bir kamu hizmetinde işitme engelli birey için işaret dili desteği sağlanması hangi ilkeyi uygular?", "Hizmete eşit erişim", "Keyfî ayrımcılık", "Bilgi gizleme", "Mülkiyet devri", "Uygun destek, farklı gereksinimlere rağmen eşit yararlanmayı sağlar.", None),
        ("analysis", "Bir hak ihlali iddiasında yalnız söylenti yerine belge ve başvuru yolları kullanılması neden önemlidir?", "İddianın doğrulanmasını ve hukuki çözüm aranmasını sağlar.", "Hak aramayı engeller.", "Söylentiyi kesin kanıt yapar.", "Yetkili kurumları gereksiz kılar.", "Kanıt ve usul, uyuşmazlığın adil incelenmesine yardım eder.", "flow:İhlal iddiası>Kanıtları koruma>Yetkili başvuru>İnceleme ve çözüm"),
        ("error-analysis", "Bir öğrenci “Haklar yalnız çoğunlukta olanlara aittir.” diyor. Hangi düzeltme doğrudur?", "Temel haklar çoğunluk-azınlık ayrımı olmadan herkes içindir.", "Azınlıkların yalnız sorumluluğu vardır.", "Çoğunluk hakları dilediğinde kaldırabilir.", "Haklar oy sayısıyla kazanılır.", "Evrensellik ve eşitlik temel hakların ortak niteliğidir.", None),
    ])


def digital_citizenship_tasks():
    n = "tr-g06-sosyal-bilgiler-note-013"
    return vrows(n, [
        ("comprehension", "E-devlet hizmetlerinin vatandaşlık açısından olumlu yönü hangisidir?", "Bazı kamu hizmetlerine zaman ve yerden bağımsız erişimi kolaylaştırması", "Bütün kişisel verileri herkese açması", "Yüz yüze hizmetleri yasaklaması", "Dijital okuryazarlığı gereksiz kılması", "Çevrim içi erişim işlem süresi ve uzaklık engelini azaltabilir.", None),
        ("comprehension", "Dijital uçurum neyi ifade eder?", "Cihaz, bağlantı ve dijital becerilere erişimdeki eşitsizliği", "İnternetteki bütün içerikleri", "Yalnız ekran boyutunu", "Elektronik imzayı", "Eşit olmayan erişim dijital haklardan yararlanmayı farklılaştırır.", None),
        ("comprehension", "Kişisel veri hangisidir?", "Bir kişiyi doğrudan veya dolaylı belirleyebilen bilgi", "Herkese açık hava sıcaklığı", "Anonim toplam öğrenci sayısı", "Ülkenin yüzölçümü", "Ad, konum, fotoğraf ve kimlik numarası kişiye bağlanabilen verilerdir.", None),
        ("application", "Bir kamu sitesi işlem için gereksiz biçimde rehberdeki tüm kişileri istiyor. Kullanıcı ne yapmalıdır?", "İznin amacını sorgulayıp yalnız gerekli veriye izin vermeli ve resmî kanaldan doğrulamalıdır.", "Bütün izinleri düşünmeden açmalıdır.", "Parolasını mesajla göndermelidir.", "Uygulamanın adını kaynak saymalıdır.", "Veri minimizasyonu hizmet için gereken kadar veri paylaşmayı gerektirir.", None),
        ("application", "Çevrim içi dilekçe verecek vatandaşın güvenli adımı hangisidir?", "Resmî alan adını ve güvenli bağlantıyı kontrol etmek", "Arama sonucundaki ilk reklama kimlik bilgisi girmek", "Tek kullanımlık kodu paylaşmak", "Ortak bilgisayarda oturumu açık bırakmak", "Adres ve bağlantı doğrulaması kimlik avı riskini azaltır.", None),
        ("application", "İnternet erişimi olmayan yurttaşların da bir hizmetten yararlanması için hangi düzenleme kapsayıcıdır?", "Yüz yüze veya telefon desteği gibi alternatif kanalları sürdürmek", "Hizmeti yalnız uygulamaya taşımak", "Dijital becerisi olmayanları dışlamak", "Başvuru süresini gizlemek", "Çoklu erişim kanalı dijital uçurumun etkisini azaltır.", None),
        ("application", "Bir belediye açık veri yayımlayacaktır. Hangi uygulama hakları dengeler?", "Kamu yararlı veriyi anonimleştirip kişisel bilgileri korumak", "Ad ve adresleri açıkça yayımlamak", "Bütün veriyi gizlemek", "Veri kaynağını belirtmemek", "Şeffaflık, kişisel verilerin korunmasıyla birlikte uygulanmalıdır.", "flow:Kamu verisi>Kişisel veri kontrolü>Anonimleştirme>Açık ve güvenli paylaşım"),
        ("application", "Çevrim içi toplantıda görüş bildiren öğrencinin dijital vatandaşlık sorumluluğu hangisidir?", "Saygılı dil kullanmak ve doğrulanmış bilgi paylaşmak", "Başkalarının hesabıyla yazmak", "Kişisel saldırı yapmak", "Toplantı bağlantısını herkese yaymak", "Katılım hakkı güvenlik ve başkalarının haklarına saygıyla kullanılır.", None),
        ("analysis", "Bir hizmet yalnız akıllı telefonun son modelinde çalışıyor. Hangi hak sorunu doğabilir?", "Cihazı uygun olmayanların kamu hizmetine eşit erişimi azalabilir.", "Herkes aynı telefona sahiptir.", "Hizmet otomatik olarak daha adildir.", "Donanım erişimi vatandaşlıkla ilgisizdir.", "Teknik tasarım bazı grupları dışlayabilir.", "table:Tasarım|Yalnız yeni telefon;Etkilenen|Eski cihaz kullananlar;Risk|Eşitsiz erişim"),
        ("analysis", "Dijital platform yanlış bilgiyi hızla yayıyor fakat düzeltme daha az kişiye ulaşıyor. Hangi önlem uygundur?", "Kaynak doğrulama, düzeltmeyi görünür kılma ve medya okuryazarlığı", "Yanlış içeriği tekrar tekrar paylaşma", "Bütün eleştirileri kaldırma", "Kaynağı gizleme", "Teknik ve eğitsel önlemler yanlış bilginin demokratik katılıma zararını azaltabilir.", None),
        ("analysis", "Bir kurum algoritmayla başvuruları sıralıyor ancak ölçütleri açıklamıyor. Hangi ilke önem kazanır?", "Şeffaflık, denetlenebilirlik ve ayrımcılık kontrolü", "Gizlilik bahanesiyle hiçbir denetim yapmamak", "Algoritmayı her zaman yanılmaz saymak", "Başvuranların itiraz hakkını kaldırmak", "Otomatik kararlar açıklanabilir ve itiraza açık olmalıdır.", None),
        ("error-analysis", "Bir öğrenci “Dijital hizmet varsa herkes eşit biçimde erişiyor demektir.” diyor. Hangi düzeltme gerekir?", "Bağlantı, cihaz, erişilebilirlik ve beceri farkları gerçek erişimi değiştirebilir.", "İnternet bütün eşitsizlikleri kaldırır.", "Yalnız hizmetin varlığı yeterlidir.", "Erişilebilir tasarım gereksizdir.", "Kâğıt üzerindeki erişim ile fiilî yararlanma aynı olmayabilir.", None),
        ("error-analysis", "Bir öğrenci “Şeffaflık için bütün vatandaş verileri açık yayımlanmalıdır.” diyor. Hangi değerlendirme doğrudur?", "Şeffaflık kamu kararlarını açıklamayı gerektirir; kişisel veriler korunmalı ve gerekirse anonimleştirilmelidir.", "Özel hayat şeffaflığa engeldir.", "Kimlik numarası kamu verisidir.", "Anonimleştirme veriyi değersiz yapar.", "Kamu bilgisine erişim ile özel hayatın korunması dengelenir.", None),
    ])


def resources_economy_tasks():
    n = "tr-g06-sosyal-bilgiler-note-014"
    return vrows(n, [
        ("comprehension", "Yenilenebilir doğal kaynağa örnek hangisidir?", "Güneş enerjisi", "Petrol", "Taş kömürü", "Doğal gaz", "Güneş enerjisi insan ömrü ölçeğinde sürekli yenilenir.", None),
        ("comprehension", "Madenin bulunduğu yerde çıkarılmasını belirleyen temel özellik nedir?", "Jeolojik oluşum ve rezervin ekonomik işletilebilirliği", "Yalnız nüfus adı", "Sokak sayısı", "Okul takvimi", "Maden yatakları jeolojik koşullara bağlıdır; işletme maliyeti de önem taşır.", None),
        ("comprehension", "Doğal kaynakların sürdürülebilir kullanımı neyi amaçlar?", "Bugünkü gereksinimleri karşılarken gelecek kuşakların olanaklarını korumayı", "Kaynağı en kısa sürede tüketmeyi", "Çevresel maliyeti gizlemeyi", "Yalnız ilk yıl gelirini artırmayı", "Sürdürülebilirlik ekonomik, çevresel ve toplumsal sürekliliği dengeler.", None),
        ("comprehension", "Su kaynakları hangi ekonomik faaliyetleri doğrudan destekleyebilir?", "Tarım, enerji, sanayi ve turizm", "Yalnız uzay araştırması", "Sadece posta hizmeti", "Hiçbir üretim alanı", "Su pek çok üretim sürecinin ve yaşamın temel girdisidir.", None),
        ("application", "Rüzgârın düzenli ve güçlü estiği bir kıyı sırtında hangi yatırım değerlendirilebilir?", "Rüzgâr enerji santrali", "Petrol kuyusu", "Taş kömürü galerisi", "Çeltik tarlası", "Rüzgâr rejimi uygun alanlarda elektrik üretimi için kullanılabilir.", None),
        ("application", "Orman ürünleri işleyen tesis için sürdürülebilir hammadde planı hangisidir?", "Kesim kadar yenileme, sertifikalı kaynak ve habitat koruması", "Bütün ağaçları aynı yıl kesmek", "Kaçak üretimi artırmak", "Yangın riskini yok saymak", "Yenileme ve izlenebilirlik kaynağın sürekliliğini destekler.", "flow:Orman kaynağı>Planlı kesim>Yenileme ve koruma>Sürdürülebilir üretim"),
        ("application", "Jeotermal kaynak kullanılan bir bölgede hangi iki fayda sağlanabilir?", "Isıtma ve elektrik üretimi", "Deniz seviyesini düşürme ve yağışı durdurma", "Kömür oluşturma ve petrol artırma", "Toprağı bütünüyle kurutma", "Sıcak yer altı akışkanları enerji ve ısı sağlayabilir.", None),
        ("application", "Bir maden işletmesi kapanış planı hazırlıyor. Hangisi gereklidir?", "Atık güvenliği, alanın rehabilitasyonu ve su izleme", "Çukuru açık bırakmak", "Bütün kayıtları silmek", "Yerel halkı bilgilendirmemek", "Faaliyet sonrası çevresel riskler onarım ve izlem gerektirir.", None),
        ("application", "Kurak bölgede tarımsal üretimi sürdürmek için hangi uygulama uygundur?", "Suya uygun ürün ve verimli sulama yöntemi seçmek", "Suyu sınırsız kabul etmek", "Buharlaşmayı artırmak", "Yer altı suyunu ölçmeden çekmek", "Ürün deseni ve sulama verimliliği sınırlı suya uyum sağlar.", None),
        ("analysis", "Bir bölgede güneş enerjisi yatırımı istihdam sağlıyor fakat tarım alanlarıyla çakışıyor. Hangi çözüm dengelidir?", "Arazi uygunluk analiziyle düşük verimli veya çatı alanlarını önceliklendirmek", "Tarımı tamamen kaldırmak", "Enerji ihtiyacını yok saymak", "Arazi etkisini ölçmemek", "Yer seçimi enerji yararı ile arazi kullanımını birlikte gözetir.", "table:Yarar|Temiz enerji ve iş;Çatışma|Tarım alanı;Çözüm|Uygun yer seçimi"),
        ("analysis", "Maden fiyatı yükselince üretim artıyor, fakat su kirliliği maliyeti hesaba katılmıyor. Hangi ekonomik sorun vardır?", "Çevresel dış maliyet karar fiyatına yansıtılmamıştır.", "Rezerv kendiliğinden yenilenmiştir.", "Kirlilik ekonomik değildir.", "Fiyat bütün etkileri otomatik kapsar.", "Topluma yüklenen zarar üreticinin maliyet hesabı dışında kalabilir.", None),
        ("analysis", "Aynı akarsu hem sulama hem enerji için kullanılıyor. Kurak yılda hangi yaklaşım gerekir?", "Ekosistem ve içme suyu gereksinimleriyle birlikte öncelik ve paylaşım planı yapmak", "Bütün suyu tek faaliyete vermek", "Akış verisini gizlemek", "Kullanıcıları görüştürmemek", "Çok amaçlı kaynaklar kuraklıkta paydaş ve ekosistem dengesiyle yönetilir.", None),
        ("error-analysis", "Bir öğrenci “Yenilenebilir kaynak hiç tükenmez, bu yüzden sınırsız kullanılabilir.” diyor. Hangi düzeltme doğrudur?", "Kaynak akışı yenilense de alan, ekosistem, teknoloji ve kullanım hızı sınırlar oluşturur.", "Yenilenebilir kaynakların etkisi yoktur.", "Her yere aynı tesis kurulabilir.", "Talep hiçbir zaman artmaz.", "Yenilenebilirlik sorumsuz ve sınırsız kullanım anlamına gelmez.", None),
        ("error-analysis", "Bir öğrenci “Doğal kaynak bulunduğu yerde ekonomi otomatik olarak gelişir.” diyor. Hangi değerlendirme gerekir?", "Teknoloji, sermaye, ulaşım, yönetim ve çevresel koşullar kaynağın ekonomik katkısını belirler.", "Rezerv tek başına refahı garanti eder.", "Ulaşımın maliyetle ilgisi yoktur.", "Kaynak yönetimi önemsizdir.", "Kaynak potansiyeli uygun kurum ve altyapıyla değere dönüşür.", None),
    ])


def professions_tasks():
    n = "tr-g06-sosyal-bilgiler-note-015"
    return vrows(n, [
        ("comprehension", "Mesleklerin ortaya çıkmasında hangi etken önemlidir?", "Toplumun gereksinimleri, kaynaklar ve teknoloji", "Yalnız meslek adının uzunluğu", "Sadece kişisel ün", "Coğrafyanın hiçbir etkisi olmaması", "Üretim biçimleri ve gereksinimler iş bölümünü şekillendirir.", None),
        ("comprehension", "Geleceğin mesleklerine hazırlanırken aktarılabilir beceri hangisidir?", "Problem çözme ve öğrenmeyi sürdürme", "Tek bir aracı ezberleyip değişime kapanma", "İş birliğinden kaçınma", "Kaynak doğrulamama", "Teknolojiler değişse de öğrenme, iletişim ve problem çözme birçok alanda kullanılır.", None),
        ("comprehension", "Bir meslek için gereken yeterlilik neyi ifade eder?", "İşi güvenli ve etkili yapmak için bilgi, beceri ve tutumları", "Yalnız iş yerinin adresini", "Sadece kıyafetin rengini", "Mesleğin popülerliğini", "Yeterlilik işin görevlerini yerine getirebilme kapasitesidir.", None),
        ("application", "Tarım teknolojileri gelişen bölgede hangi yeni uzmanlık gereksinimi artabilir?", "Hassas tarım veri analistliği", "Buzul rehberliği", "Denizaltı madenciliği", "El yazması kopyacılığı", "Sensör ve uydu verileri tarımsal kararlar için yeni uzmanlık oluşturur.", None),
        ("application", "Bir öğrenci sağlık teknolojilerine ilgi duyuyor. Kariyer araştırmasında hangi adım uygundur?", "Mesleğin görevlerini, eğitim yolunu, etik sorumluluklarını ve çalışma ortamını incelemek", "Yalnız maaş söylentisine bakmak", "Tek videoyu bütün meslek saymak", "Gerekli becerileri yok saymak", "Çok boyutlu araştırma bilinçli seçim sağlar.", "flow:İlgi alanı>Meslek araştırması>Gerekli eğitim ve beceri>Deneyim ve karar"),
        ("application", "Turizm kentinde yabancı dil ve dijital rezervasyon becerilerinin birlikte aranması neyi gösterir?", "Meslek yeterliliklerinin ekonomik faaliyet ve teknolojiyle değişebildiğini", "Turizmin iletişim gerektirmediğini", "Dijital araçların bütün insan becerisini kaldırdığını", "Mesleklerin değişmez olduğunu", "Sektörün dönüşümü yeni beceri bileşimleri gerektirir.", None),
        ("application", "Bir mesleği deneyimlemek isteyen öğrenci için güvenli yöntem hangisidir?", "Uzman gözetiminde iş yeri gözlemi veya okul projesi yapmak", "Tehlikeli ekipmanı izinsiz kullanmak", "Kimlik bilgilerini bilinmeyen siteye vermek", "Meslek hakkında kaynak kullanmamak", "Gözetimli deneyim gerçek görevleri güvenli biçimde tanıtır.", None),
        ("error-analysis", "Bir öğrenci “Otomasyon bazı rutin işleri azaltıyorsa çalışanlara yeni beceri eğitimi vermek gereksizdir.” diyor. Hangi düzeltme doğrudur?", "Yeniden beceri kazandırma ve yaşam boyu öğrenme desteği yeni görevlere geçişi kolaylaştırır.", "Eğitim bütünüyle durdurulmalıdır.", "Teknoloji kullanımı çalışanlardan gizlenmelidir.", "Değişim hakkında bilgi verilmemelidir.", "Dönüşen görevler güncel bilgi ve beceri edinmeyi gerektirir.", None),
        ("analysis", "Aynı meslek farklı bölgelerde farklı araçlar kullanıyor. Hangi sonuç çıkar?", "Temel amaç benzerken uygulama coğrafya ve teknolojiye uyarlanabilir.", "Meslek bütünüyle farklıdır.", "Araç seçimi hiçbir koşuldan etkilenmez.", "Bütün çalışanlar aynı ortamda bulunur.", "İşin yöntemi yerel gereksinim ve imkânlara göre değişebilir.", "table:Sabit|Mesleğin temel amacı;Değişen|Araç ve çalışma ortamı;Etken|Coğrafya ve teknoloji"),
        ("analysis", "Yapay zekâ bir uzmana öneri sunuyor fakat son karar insan tarafından veriliyor. Hangi beceri önem kazanır?", "Öneriyi eleştirel değerlendirme ve etik sorumluluk", "Her çıktıyı sorgusuz kabul etme", "Alan bilgisini bırakma", "Kararın kaynağını gizleme", "Araç çıktısı bağlam ve sonuç bakımından uzman denetimi gerektirir.", None),
        ("analysis", "Bir bölgede yenilenebilir enerji yatırımları artıyor. Meslek eğitimi nasıl uyarlanmalıdır?", "Elektrik, bakım, çevre ve iş güvenliği becerileri sektör verileriyle planlanmalıdır.", "Eski program hiç incelenmemelidir.", "Yalnız meslek adları değiştirilmelidir.", "İş güvenliği kaldırılmalıdır.", "Eğitim gerçek iş gereksinimleriyle ve güvenlikle eşleştirilir.", None),
        ("analysis", "Bir meslek yüksek gelirli fakat kişinin ilgi ve değerleriyle uyuşmuyor. Dengeli seçim nasıl yapılır?", "Gelirle birlikte ilgi, yetenek, eğitim, çalışma koşulu ve toplumsal etki değerlendirilir.", "Yalnız gelir seçimi belirler.", "İlgi ve beceri önemsizdir.", "Meslek araştırması gereksizdir.", "Kariyer kararı çok ölçütlüdür.", None),
        ("error-analysis", "Bir öğrenci “Gelecekte bütün meslekleri robotlar yapacak, insan becerisine gerek kalmayacak.” diyor. Hangi düzeltme doğrudur?", "Bazı görevler otomatikleşebilir; yeni görevler ve insanın yaratıcılık, iletişim ve etik karar becerileri önemini sürdürebilir.", "Her meslek aynı anda yok olur.", "Teknoloji yeni iş oluşturamaz.", "İnsan denetimi hiçbir alanda gerekmez.", "Teknolojik değişim görevleri dönüştürür; sonucu meslek bazında incelemek gerekir.", None),
    ])


def product_project_tasks():
    n = "tr-g06-sosyal-bilgiler-note-016"
    return vrows(n, [
        ("comprehension", "Ürün geliştirme sürecinde ihtiyaç analizi neden yapılır?", "Çözülecek gerçek sorunu ve hedef kullanıcıyı belirlemek için", "Reklamı üründen önce kesinleştirmek için", "Bütün rakipleri kopyalamak için", "Maliyeti gizlemek için", "İhtiyaç doğru tanımlanmazsa tasarım kullanıcının sorununu çözmeyebilir.", None),
        ("comprehension", "Prototip ne işe yarar?", "Ürünün erken örneğini deneyip eksikleri görmeye", "Seri üretimi kanıtsız başlatmaya", "Markayı otomatik tescil etmeye", "Bütçeyi kaldırmaya", "Prototip düşük maliyetle test ve düzeltme olanağı verir.", None),
        ("comprehension", "Yatırım bütçesi hangi bilgileri içermelidir?", "Beklenen gelir, gider, kaynak ve riskleri", "Yalnız ürünün rengini", "Sadece sloganı", "Kaynağı belirsiz tahminleri", "Mali plan kaynak gereksinimini ve sürdürülebilirliği gösterir.", None),
        ("application", "Öğrenciler su tasarruflu saksı tasarlıyor. İlk güvenilir veri hangisidir?", "Kullanıcıların sulama sorunları ve mevcut su tüketimi", "Logonun rengi", "Sosyal medyada rastgele beğeni", "Rakibin ürün adını kopyalama", "Sorun ve başlangıç ölçümü tasarım hedefini belirler.", "flow:İhtiyacı belirle>Tasarım>Prototip testi>İyileştirme"),
        ("application", "Prototip kullanıcı testinde kapağın zor açıldığı görülüyor. Uygun adım hangisidir?", "Geri bildirimi kaydedip mekanizmayı yeniden tasarlamak ve tekrar test etmek", "Kullanıcıyı suçlamak", "Sorunu rapordan silmek", "Seri üretime hemen geçmek", "Yinelemeli tasarım kanıta göre düzeltme gerektirir.", None),
        ("application", "Bir ürünün maliyeti 80 TL, hedef satış fiyatı 110 TL'dir. Diğer giderler hesaba katılmadan birim brüt fark kaç TL'dir?", "30 TL", "190 TL", "80 TL", "110 TL", "110−80=30 TL; bunun net kâr olmadığı ayrıca belirtilmelidir.", None),
        ("application", "Hedef kitlesi çocuklar olan ürün reklamında hangi yaklaşım etiktir?", "Yaşa uygun, doğrulanabilir bilgi verip yanıltıcı korku ve baskı kullanmamak", "Gerçek dışı kesin sonuç vaat etmek", "Gizli ücretleri saklamak", "Çocuğun kişisel verisini izinsiz toplamak", "Çocuklara yönelik pazarlama açık ve koruyucu olmalıdır.", None),
        ("application", "Yatırımcıya sunumda hangi kanıt daha değerlidir?", "Doğrulanmış ihtiyaç, test sonuçları, maliyet ve risk planı", "Yalnız büyük yazılı slogan", "Kaynağı olmayan pazar sayısı", "Rakibi küçümseyen iddia", "Karar verici ürünün sorunu çözdüğünü ve planın uygulanabilir olduğunu görmek ister.", "table:İhtiyaç|Kullanıcı verisi;Çözüm|Test sonucu;Yatırım|Maliyet ve risk"),
        ("analysis", "İki prototipten A ucuz fakat çabuk bozuluyor; B pahalı ve onarılabilir. Hangi değerlendirme gerekir?", "Satın alma fiyatıyla birlikte ömür, bakım, kullanıcı güvenliği ve atık etkisi", "Yalnız ilk fiyat", "Yalnız renk", "Dayanıklılığı yok saymak", "Toplam yaşam döngüsü maliyeti tek fiyat etiketinden geniştir.", None),
        ("analysis", "Anket ürüne yüksek ilgi gösteriyor fakat katılımcılar yalnız tasarım kulübü üyeleri. Hangi risk vardır?", "Örneklem hedef pazarın tamamını temsil etmeyebilir.", "İlgi kesin satış garantisidir.", "Kulüp üyeleri bütün nüfustur.", "Anket sonuçları test edilemez.", "Yakın ilgi grubu talebi olduğundan yüksek gösterebilir.", None),
        ("analysis", "Satış arttı fakat iade oranı da yükseldi. Hangi sonraki adım uygundur?", "İade nedenlerini ürün kalitesi ve beklenti uyumuyla birlikte incelemek", "Yalnız satış sayısını başarı kabul etmek", "İadeleri kayıttan silmek", "Müşteri geri bildirimini kapatmak", "Satış hacmi ve memnuniyet göstergeleri birlikte değerlendirilir.", None),
        ("analysis", "Ürün fikri iyi fakat ham madde yalnız uzak ve riskli tek tedarikçiden geliyor. Yatırım planında ne yapılmalıdır?", "Tedarik riski, alternatif malzeme ve stok planı oluşturmak", "Riski gizlemek", "Tek kaynağı sonsuz kabul etmek", "Maliyeti hesaplamamak", "Tedarik sürekliliği üretim ve maliyet için kritik risktir.", None),
        ("error-analysis", "Bir öğrenci “Prototip başarılıysa kullanıcı testi gereksizdir.” diyor. Hangi düzeltme doğrudur?", "Tasarımcının değerlendirmesi yeterli değildir; gerçek kullanıcı testi kullanım sorunlarını gösterebilir.", "Prototip her zaman kusursuzdur.", "Kullanıcı görüşü ürünü bozar.", "Test yalnız satıştan sonra yapılır.", "Erken kullanıcı kanıtı pahalı hataları seri üretimden önce bulur.", None),
        ("error-analysis", "Bir öğrenci “Satış fiyatı maliyetten yüksekse proje kesin kârlıdır.” diyor. Hangi değerlendirme gerekir?", "Pazarlama, dağıtım, vergi, iade ve sabit giderler de hesaplanmadan net kâr bilinmez.", "Birim fark bütün giderleri kapsar.", "Gelir hesaplamaya gerek yoktur.", "Kârlılık yalnız sloganla ölçülür.", "Toplam gelir ve toplam maliyet birlikte değerlendirilmelidir.", None),
    ])


def transport_communication_tasks():
    n = "tr-g06-sosyal-bilgiler-note-017"
    return vrows(n, [
        ("comprehension", "Ulaşım teknolojilerinin kültürel etkileşime etkisi hangisidir?", "İnsan ve ürün hareketini hızlandırarak karşılaşmaları artırması", "Bütün kültürel farkları anında yok etmesi", "İletişimi gereksiz kılması", "Yalnız yerel üretimi durdurması", "Daha erişilebilir yolculuk farklı toplumların temasını artırabilir.", None),
        ("comprehension", "İletişim teknolojilerinin kültürel değişimdeki rolü nedir?", "Bilgi ve kültürel ürünlerin geniş kitlelere hızla ulaşmasını sağlamak", "Mesafeyi fiziksel olarak kaldırmak", "Her içeriği güvenilir yapmak", "Kültür üretimini sona erdirmek", "Dijital ağlar içerik dolaşımını hızlandırır fakat doğruluk ve temsil denetimi gerekir.", None),
        ("comprehension", "Kültürel etkileşim neyi ifade eder?", "Toplumların temas yoluyla birbirinden unsur öğrenmesi ve uyarlaması", "Bir kültürün diğerini zorunlu olarak yok etmesi", "Hiçbir değişimin yaşanmaması", "Yalnız ticari fiyat değişimini", "Etkileşim alışveriş, yorumlama ve yeni biçimler doğurabilir.", None),
        ("application", "Hızlı tren hattı açılan iki kent arasında hangi kültürel sonuç beklenebilir?", "Ziyaret, etkinlik ve öğrenci değişiminin kolaylaşması", "Kentlerin bütün geleneklerinin aynılaşması", "İnternetin kapanması", "Yerel kültürün otomatik yok olması", "Seyahat süresinin azalması karşılıklı katılımı artırabilir.", None),
        ("application", "Çevrim içi müze sergisinin erişimini artırmak için hangi özellik uygundur?", "Çok dilli açıklama, altyazı ve kaynak bilgisi", "Yalnız yüksek hızlı cihazda çalışma", "Eser bağlamını kaldırma", "Telif bilgisini gizleme", "Dil ve erişilebilirlik desteği daha çok kişinin güvenli biçimde yararlanmasını sağlar.", None),
        ("application", "Bir geleneksel dans videosu başka ülkede yeniden yorumlanıyor. Saygılı paylaşım nasıl olur?", "Kaynağı belirtip yeni yorum ile özgün bağlamı ayırmak", "Dansı kendi buluşu gibi sunmak", "Topluluğun adını silmek", "Yanlış bilgi eklemek", "Atıf kültürel emeği tanır ve dönüşümün kaynağını görünür kılar.", None),
        ("application", "Turistik uçuşların arttığı adada kültürel ve çevresel baskı oluşuyor. Hangi plan dengelidir?", "Taşıma kapasitesi, yerel katılım ve koruma kurallarıyla ziyaretçi yönetimi", "Sınırsız ziyaretçi kabulü", "Yerel halkı karar dışı bırakmak", "Koruma verisini gizlemek", "Ulaşım kolaylığı sürdürülebilir ziyaret yönetimiyle dengelenmelidir.", "flow:Ulaşım kolaylığı>Ziyaretçi artışı>Kültürel-çevresel baskı>Katılımcı yönetim"),
        ("application", "Uzak köyde internet bağlantısı kuruluyor. Kültürel yarar hangisi olabilir?", "Yerel üreticilerin ürün ve hikâyelerini geniş kitlelere ulaştırması", "Yerel dilin zorunlu olarak bitmesi", "Bütün yüz yüze iletişimin sona ermesi", "Yanlış bilginin imkânsızlaşması", "Bağlantı yerel üretimin tanıtımına yeni kanal sağlayabilir.", None),
        ("analysis", "Aynı müzik türü farklı ülkelerde yerel çalgılarla icra ediliyor. Hangi sonuç çıkar?", "Kültürel ürünler dolaşırken yerel unsurlarla yeniden yorumlanabilir.", "Bütün icralar özdeş olmak zorundadır.", "Yerel çalgı etkileşimi engeller.", "Müzik ulaşım ve iletişimden etkilenmez.", "Kültür aktarımı kopyalamadan çok uyarlama da içerebilir.", "table:Dolaşan unsur|Müzik türü;Yerel katkı|Çalgılar;Sonuç|Yeni yorum"),
        ("analysis", "Sosyal medya akımı yerel el sanatına talebi artırıyor fakat seri taklitler de çoğalıyor. Dengeli yorum hangisidir?", "Görünürlük ekonomik fırsat yaratırken özgünlük ve emek hakları için koruma gerekir.", "Akım yalnız zarar verir.", "Taklitler ustalara her zaman yarar sağlar.", "Kaynak belirtmek gereksizdir.", "Dijital yayılım aynı anda fırsat ve koruma sorunu üretebilir.", None),
        ("analysis", "Yeni kara yolu gençlerin kente erişimini artırırken köyde bazı geleneksel işler azalıyor. Bu durum neyi gösterir?", "Ulaşım değişiminin ekonomik ve kültürel sonuçlarının birlikte ortaya çıkabildiğini", "Yolun yalnız olumlu sonucu olduğunu", "Mesleklerin kültürle ilişkisiz olduğunu", "Köy-kent etkileşiminin azaldığını", "Hareketlilik fırsatlarla birlikte yaşam biçimini dönüştürebilir.", None),
        ("error-analysis", "Bir öğrenci “İletişim hızlandıysa paylaşılan her kültürel bilgi doğrudur.” diyor. Hangi düzeltme gerekir?", "Hız doğruluk garantisi değildir; kaynak, bağlam ve temsil denetlenmelidir.", "Çok paylaşılan içerik kanıttır.", "Kaynak kontrolü iletişimi engeller.", "Dijital içerik yanlış olamaz.", "Yayılma hızı ile bilgi kalitesi farklı ölçütlerdir.", None),
        ("error-analysis", "Bir öğrenci “Kültürel etkileşim yalnız bir tarafın diğerini taklit etmesidir.” diyor. Hangi değerlendirme doğrudur?", "Etkileşim karşılıklı alışveriş, seçme ve yerel uyarlama süreçlerini içerebilir.", "Etkileşim her zaman tek yönlüdür.", "Uyarlama kültürel değildir.", "Toplumlar temas kuramaz.", "Kültürler temas sırasında hem alır hem dönüştürür hem de katkı sunar.", None),
    ])


def intellectual_property_tasks():
    n = "tr-g06-sosyal-bilgiler-note-018"
    return vrows(n, [
        ("comprehension", "Telif hakkı temel olarak neyi korur?", "Edebiyat, sanat ve benzeri özgün eserlerdeki yaratıcı emeği", "Bir ürünün yalnız satış fiyatını", "Her doğal fikri süresiz olarak", "Şirketin vergi kaydını", "Telif somutlaşmış özgün eser üzerindeki hakları düzenler.", None),
        ("comprehension", "Patent hangi tür yeniliği korumaya yöneliktir?", "Yeni, buluş basamağı içeren ve uygulanabilir teknik buluşu", "Her sloganı", "Yalnız şirket adını", "Bir kitabın cümlelerini", "Patent teknik çözüm niteliğindeki buluşlara süreli koruma sağlayabilir.", None),
        ("comprehension", "Marka neyi ayırt etmeye yarar?", "Bir işletmenin mal veya hizmetlerini diğerlerinden", "Bir romanın bütün içeriğini", "Doğal kaynağın yerini", "Bilimsel gerçeği", "Ad, logo veya işaret ticari kaynak ayrımı sağlar.", None),
        ("application", "Bir öğrenci internetten bulduğu fotoğrafı sunumda kullanacaktır. İlk yapması gereken nedir?", "Lisansı ve kullanım iznini kontrol edip gerekli atfı vermek", "Fotoğrafı kendi çekmiş gibi göstermek", "Filigranı silmek", "Kaynağı gizlemek", "Çevrim içi erişim eserin serbest kullanımda olduğu anlamına gelmez.", None),
        ("application", "Yeni bir kilit mekanizması geliştiren tasarımcı hangi korumayı araştırmalıdır?", "Patent veya faydalı model", "Yalnız telif", "Coğrafi işaret", "Alan adı", "Teknik işleyişe sahip yenilik sınai hak korumasına konu olabilir.", None),
        ("application", "Bir işletme ürünlerini ayırt eden adı ve logoyu korumak istiyor. Uygun işlem hangisidir?", "Marka tescili", "Roman telifi", "Buluş patenti", "Nüfus kaydı", "Ticari ad ve işaret marka tesciliyle korunabilir.", None),
        ("application", "Açık lisanslı müzik kullanırken hangi kurala uyulmalıdır?", "Lisansta belirtilen atıf, paylaşım ve ticari kullanım koşullarına", "Kaynağı her zaman silmeye", "Eseri sınırsız sahiplenmeye", "Lisans metnini yok saymaya", "Açık lisans ücretsiz erişim sağlayabilir fakat koşullar bağlayıcıdır.", None),
        ("analysis", "Bir fikir henüz yalnız zihindedir, somut teknik çözüm veya eser hâline gelmemiştir. Hangi yorum uygundur?", "Soyut fikir ile korunabilir eser veya buluş aynı değildir; somutlaştırma ve koşullar incelenmelidir.", "Her düşünce otomatik patentlidir.", "Fikir başkasına anlatılınca telif kesin doğar.", "Koruma türleri arasında fark yoktur.", "Fikrî haklar belirli koruma konuları ve şartlara bağlanır.", None),
        ("analysis", "Bir şirket rakibinin logosuna çok benzeyen işaret kullanıyor. Hangi risk vardır?", "Tüketicide karıştırılma ve marka hakkı ihlali", "Patent süresinin uzaması", "Eserin kamu malı olması", "Coğrafi uzaklığın artması", "Benzer işaretler ticari kaynak konusunda yanılgı doğurabilir.", "table:Korunan|Ayırt edici logo;Davranış|Çok benzer işaret;Risk|Karıştırılma"),
        ("analysis", "Patent süresi bittikten sonra buluş bilgisinin kullanılabilmesi hangi dengeyi gösterir?", "Buluş sahibine süreli teşvik ile toplumun bilgiye uzun dönem erişimi arasındaki dengeyi", "Korumanın sonsuz olduğunu", "Buluşun hiç açıklanmadığını", "Telif ile markanın aynı olduğunu", "Patent sistemi açıklama karşılığında sınırlı süreli tekel sağlar.", None),
        ("analysis", "Bir video hem özgün müzik hem şirket logosu hem yeni cihaz tasarımı içeriyor. Hangi sonuç çıkar?", "Farklı unsurlar telif, marka ve patent gibi farklı korumalara konu olabilir.", "Tek bir hak bütün unsurları aynı biçimde korur.", "Logo telifle teknik buluş olur.", "Cihaz tasarımı yalnız marka sayılır.", "Koruma konusu unsurun niteliğine göre belirlenir.", "flow:Özgün müzik>Telif;Logo>Marka;Teknik cihaz>Patent araştırması"),
        ("error-analysis", "Bir öğrenci “İnternette gördüğüm her içerik sahipsizdir.” diyor. Hangi düzeltme doğrudur?", "Çevrim içi içerik de telif ve lisans koşullarına tabi olabilir; kaynak ve izin kontrol edilmelidir.", "İndirmek sahiplik verir.", "Arama motoru bütün hakları kaldırır.", "Kaynak belirtmek gereksizdir.", "Erişilebilirlik ile kullanım hakkı aynı şey değildir.", None),
        ("error-analysis", "Bir öğrenci “Patent, marka ve telif aynı şeyi korur.” diyor. Hangi değerlendirme doğrudur?", "Patent teknik buluşu, marka ayırt edici işareti, telif özgün eseri korur.", "Üçü yalnız şirket adını korur.", "Telif teknik mekanizmayı tescil eder.", "Marka romanın bütün metnini korur.", "Koruma türleri farklı fikrî ürün ve işlevlere yöneliktir.", None),
    ])


def listening_material_tasks():
    n = "tr-g06-turkce-note-001"
    return vrows(n, [
        ("comprehension", "Dinleme/izleme materyali seçerken amaç neden belirlenmelidir?", "İçeriğin, sürenin ve sunum biçiminin gereksinime uygunluğunu değerlendirmek için", "Yalnız kapağın rengini seçmek için", "Bütün materyalleri aynı saymak için", "Kaynak bilgisini yok saymak için", "Amaç, seçimin hangi ölçütlerle yapılacağını belirler.", None),
        ("comprehension", "Güvenilir bir bilgilendirici videoda hangi özellik aranır?", "Kaynakların belirtilmesi ve iddiaların doğrulanabilir olması", "Başlığın yalnız büyük harfle yazılması", "Çok paylaşılmış olması", "Konuşmacının hızlı konuşması", "Kaynak ve kanıt, içeriğin denetlenebilmesini sağlar.", None),
        ("comprehension", "Dinleyicinin düzeyine uygunluk neyi ifade eder?", "Dil, kavram yoğunluğu ve ön bilgilerin dinleyiciye uygun olmasını", "İçeriğin mümkün olduğunca uzun olmasını", "Bütün terimlerin açıklamasız verilmesini", "Yalnız eğlenceli olmasını", "Anlaşılabilirlik hedef kitlenin dil ve bilgi düzeyiyle ilişkilidir.", None),
        ("comprehension", "Bir materyalin güncelliği özellikle hangi konuda önemlidir?", "Hızla değişen bilimsel ve kamusal bilgilerde", "Tarihî bir şiirin özgün metninde", "Masalın kahraman adında", "Müziğin ritminde", "Değişen bilgiler eski kayıtlarda geçerliliğini yitirebilir.", None),
        ("comprehension", "Altyazı ve sesli betimleme hangi ölçüte katkı sağlar?", "Erişilebilirliğe", "Kaynağın gizlenmesine", "İçeriğin kısaltılmasına", "Telifin kaldırılmasına", "Farklı duyusal gereksinimler için alternatif sunum erişimi artırır.", None),
        ("application", "Öğrenci deprem çantası hazırlamayı öğrenecek. Hangi materyal en uygundur?", "Güncel resmî kurum videosu ve kontrol listesi", "Kaynağı belirsiz eski reklam", "Kurgusal korku filmi", "Yorumlarda dolaşan söylenti", "Güvenlik amacı güncel ve yetkili kaynak gerektirir.", None),
        ("application", "Bir şiirin vurgu ve tonlamasını incelemek isteyen öğrenci ne seçmelidir?", "Nitelikli bir sesli şiir dinletisi ve metnin yazılı kopyası", "Yalnız sessiz fotoğraf albümü", "Şiirle ilgisiz haber", "Sadece sözlük maddesi", "Ses kaydı işitsel özellikleri, metin ise sözcük ve dizeleri karşılaştırmayı sağlar.", None),
        ("application", "On dakikalık hazırlık süresinde bir konunun temelini öğrenmek için hangi seçim uygundur?", "Süresi belli, bölüm başlıkları açık ve kısa bir açıklayıcı kayıt", "İki saatlik kaynaksız yayın", "Konuyla ilgisiz video dizisi", "Süresi belirtilmeyen canlı yayın", "Zaman sınırı ve temel öğrenme amacı kısa, yapılandırılmış materyali gerektirir.", "table:Amaç|Temel bilgi;Süre|10 dakika;Uygun materyal|Kısa ve bölümlü açıklama"),
        ("application", "İşitme güçlüğü yaşayan öğrenci belgesel izleyecek. Hangi sürüm seçilmelidir?", "Doğru zamanlanmış altyazılı ve okunabilir metin destekli sürüm", "Altyazısız ve düşük sesli sürüm", "Görüntüsü olmayan kayıt", "Metni kapatılmış sürüm", "Altyazı konuşma ve önemli ses bilgisini erişilebilir kılar.", None),
        ("application", "Aynı konuda biri uzman röportajı, diğeri reklam olan iki kayıt var. Araştırma amacı için hangisi seçilmelidir?", "Uzmanın kimliği ve kanıtları doğrulanabilen röportaj", "Ürünü öven kaynak göstermeyen reklam", "Daha renkli olan kayıt", "Daha çok ünlem kullanan kayıt", "Araştırma materyali uzmanlık, kanıt ve amaç bakımından değerlendirilir.", None),
        ("application", "Bir öğrenci hızlı konuşulan kaydı anlamakta zorlanıyor. Materyal seçimini nasıl uyarlamalıdır?", "Oynatma hızı ayarlanabilen, duraklatılabilen ve bölümlemeli sürümü seçmelidir.", "Daha da hızlı sürümü açmalıdır.", "Aynı kaydı not almadan sürdürmelidir.", "Konuyla ilgisiz kısa videoya geçmelidir.", "Kontrol edilebilir oynatma ve bölümleme bilişsel yükü azaltır.", None),
        ("analysis", "Video A güncel ve kaynaklı ancak ileri düzey; Video B anlaşılır fakat beş yıl önceki değişmiş verileri içeriyor. En iyi çözüm hangisidir?", "A'nın uygun bölümlerini açıklayıcı destekle kullanıp güncel veriyi korumak", "B'yi güncelliğini kontrol etmeden kullanmak", "İki videoyu da yalnız görüntü kalitesine göre seçmek", "Kaynak ve düzeyi aynı ölçüt saymak", "Amaç güncel bilgi ise doğruluk korunur; düzey desteğiyle erişilebilirlik artırılır.", "table:Video A|Güncel-kaynaklı-ileri;Video B|Anlaşılır-eski;Karar|Güncel içeriğe destek"),
        ("analysis", "Bir podcast ilgi çekici öyküler anlatıyor fakat kaynak vermiyor; resmî kayıt daha sade ve belgelidir. Bilgi toplama amacı için hangi değerlendirme doğrudur?", "Resmî kayıt ana kaynak olmalı; podcast iddiaları doğrulanırsa yardımcı örnek olabilir.", "İlgi çekicilik doğruluk için yeterlidir.", "Kaynaklı kayıt gereksizdir.", "Podcastteki her öykü kanıttır.", "Materyalin çekiciliği ile güvenilirliği ayrı ölçütlerdir.", None),
        ("analysis", "Bir öğrenci her amaç için yalnız kısa video seçiyor. Hangi durumda bu seçim yetersiz kalabilir?", "Karmaşık bir tartışmada farklı görüş ve kanıtların ayrıntılı incelenmesi gerektiğinde", "Tek bir terimin telaffuzunu dinlerken", "Kısa duyuruya bakarken", "Bir ses efektini tanırken", "Materyal uzunluğu amaç ve içeriğin derinliğiyle uyumlu olmalıdır.", None),
        ("error-analysis", "Bir öğrenci “En çok izlenen video en güvenilir videodur.” diyor. Hangi düzeltme doğrudur?", "İzlenme sayısı popülerliği gösterir; güvenilirlik kaynak, uzmanlık ve kanıtla değerlendirilir.", "Popülerlik her iddiayı kanıtlar.", "Kaynak kontrolü yalnız az izlenen içerikte yapılır.", "Başlık güvenilirliği belirler.", "Nicel izlenme göstergesi bilgi kalitesinin doğrudan ölçüsü değildir.", None),
        ("error-analysis", "Bir öğrenci “Materyal eğlenceliyse amaca uygunluk ve erişilebilirlik önemli değildir.” diyor. Hangi değerlendirme gerekir?", "İlgi çekicilik yararlı olabilir; amaç, doğruluk, düzey ve erişilebilirlik birlikte değerlendirilmelidir.", "Eğlence bütün öğrenme ölçütlerini kaldırır.", "Amaç yalnız süreyi belirler.", "Erişilebilirlik içerikle ilgisizdir.", "İyi seçim birden çok ölçüt arasında denge kurar.", None),
    ])


TASK_BUILDERS = [remaining_rights_tasks, digital_citizenship_tasks, resources_economy_tasks,
                 professions_tasks, product_project_tasks, transport_communication_tasks,
                 intellectual_property_tasks, listening_material_tasks]


def _label(labels: dict[str, str], qid: str, suffix: str, value: str) -> str:
    key = f"figure.{qid}.{suffix}"
    labels[key] = value
    return key


def table_figure(qid: str, labels: dict[str, str], payload: str) -> dict[str, Any]:
    raw_rows = [segment.split("|") for segment in payload.split(":", 1)[1].split(";")]
    width = max(len(row) for row in raw_rows)
    headers = [_label(labels, qid, f"h{i}", f"Alan {i+1}") for i in range(width)]
    rows_out = [[{"v": value} for value in row + ["—"] * (width - len(row))] for row in raw_rows]
    alt = _label(labels, qid, "alt", "Sorudaki ölçüt ve kanıtları karşılaştıran tablo; doğru yanıt belirtilmemiştir.")
    return {"kind": "table", "headerKeys": headers, "rows": rows_out, "altTextKey": alt}


def flow_figure(qid: str, labels: dict[str, str], payload: str) -> dict[str, Any]:
    chunks = payload.split(":", 1)[1].split(";")
    if any(">" in chunk for chunk in chunks):
        chains = [chunk.split(">") for chunk in chunks]
    else:
        chains = [chunks]
    names = []
    for chain in chains:
        for name in chain:
            if name not in names:
                names.append(name)
    nodes = [{"id": f"n{i}", "labelKey": _label(labels, qid, f"n{i}", name)} for i, name in enumerate(names)]
    ids = {name: f"n{i}" for i, name in enumerate(names)}
    edges = []
    for chain in chains:
        for left, right in zip(chain, chain[1:]):
            edges.append({"from": ids[left], "to": ids[right]})
    alt = _label(labels, qid, "alt", "Sorudaki süreç veya koruma ilişkilerini düğümlerle gösteren akış şeması; doğru seçenek açıklanmamıştır.")
    return {"kind": "flow", "nodes": nodes, "edges": edges, "altTextKey": alt}


def apply_visual(row: dict[str, Any], item: dict[str, Any], labels: dict[str, str]) -> None:
    payload = item.get("visual_payload")
    if not payload:
        return
    qid = str(row["id"])
    kind = payload.split(":", 1)[0]
    if kind == "table":
        figure = table_figure(qid, labels, payload)
    elif kind == "flow":
        figure = flow_figure(qid, labels, payload)
    else:
        raise AssertionError(payload)
    row["figure"] = figure
    row["question"] = f"Aşağıdaki görseli inceleyiniz. Görseldeki verileri kullanarak cevaplayınız. {row['question']}"
    row["visualRequirement"] = "required"
    row["visualNeed"] = {"level": "required", "role": "evidence",
                         "rationale": "Karşılaştırma veya süreç ilişkisi yapılandırılmış görsel kanıt üzerinden okunur.",
                         "acceptableKinds": [figure["kind"]],
                         "evidenceDimensions": ["ölçüt veya unsur", "süreç veya sonuç"]}


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1600:
        raise RuntimeError("validated first sixteen batches must exist before batch 17")
    notes = {**read_notes_only(SOCIAL_SOURCE), **read_notes_only(TURKISH_SOURCE)}
    tasks = [item for builder in TASK_BUILDERS for item in builder()]
    if len(tasks) != 100:
        raise AssertionError(f"batch 17 must contain 100 tasks, got {len(tasks)}")
    expected_modes = {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
    if Counter(item["mode"] for item in tasks) != expected_modes:
        raise AssertionError(Counter(item["mode"] for item in tasks))
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    rows_out = []
    for local, item in enumerate(tasks, 1):
        row = make_record(local, item, notes[item["note"]], batch=17, number_base=1600)
        apply_visual(row, item, labels)
        rows_out.append(row)
    expected_subjects = Counter({"Sosyal Bilgiler": 84, "Türkçe": 16})
    if Counter(row["subject"] for row in rows_out) != expected_subjects:
        raise AssertionError(Counter(row["subject"] for row in rows_out))
    if Counter(row["correctIndex"] for row in rows_out) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer positions are not exactly balanced")
    figure_count = sum(bool(row.get("figure")) for row in rows_out)
    expected_figures = sum(bool(item.get("visual_payload")) for item in tasks)
    if figure_count != expected_figures:
        raise AssertionError((figure_count, expected_figures))
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":"))
                                 for row in existing + rows_out) + "\n", encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
    print(json.dumps({"batch": 17, "questions": 100, "socialStudies": 84, "turkish": 16,
                      "figures": figure_count, "total": 1700,
                      "modes": dict(Counter(item["mode"] for item in tasks)),
                      "sourceQuestionReads": 0, "figureSpec": "1.3.0"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
