#!/usr/bin/env python3
"""Append release batch 03: 94 ICT and 6 Religion/Culture questions.

All cases are authored from lesson-note concepts.  Only note records are read.
The six DKAB records are distributed across the batch cognitive mix rather
than being placed into a single question type.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from build_unique_question_banks import ROOT
from author_grade6_bilisim_batch01 import LABELS_OUTPUT, OUTPUT, rotate


BTY_SOURCE = ROOT / "turkiye/6-sinif/bilisim-teknolojileri/bilisim-teknolojileri-tum.jsonl"
DKAB_SOURCE = ROOT / "turkiye/6-sinif/din-kulturu/din-kulturu-tum.jsonl"


# note, scenario, evidence, concept, action, inference, 3 misconceptions, rationale
BTY_CASES = [
    ("tr-g06-bty-note-001", "Parktaki çöp kutuları doluluk oranını ölçüp temizlik merkezine iletiyor.", "Merkez yalnız dolan kutular için rota oluşturuyor; bağlantısı kesilen kutunun değeri güncellenmiyor.", "Sensörlü kutuların ölçümü ağ üzerinden merkeze aktarması nesnelerin interneti kullanımına örnektir.", "Yalnız doluluk verisini gönderip konum erişimini görevli hesaplarla sınırlamak uygun tasarımdır.", "Bağlantı kesilince değerin güncellenmemesi, kararın uzaktan gelen sensör verisine bağlı olduğunu gösterir.", ["Otomatik rota oluşturan her araç sanal gerçeklik gözlüğüdür.", "Sensör ölçümü ağa aktarılmadığında da merkez güncel değeri kendiliğinden bilir.", "Kutunun konumunu herkese açık yayımlamak sistemin çalışması için zorunludur."], "Nesnelerin internetinde fiziksel algılama, ağ bağlantısı ve veriye dayalı işlem bir zincir oluşturur; veri erişimi gereksinimle sınırlandırılır."),
    ("tr-g06-bty-note-002", "Bir hastane uzaktan muayene kabinlerini kırsal bölgelerde denemeyi planlıyor.", "Deneme yolculuk süresini azaltıyor; zayıf bağlantıda görüntü donuyor ve bazı kullanıcılar kabini tek başına kullanamıyor.", "Geleceğin sağlık teknolojisi yararının yanında bağlantı eşitsizliği, erişilebilirlik ve mahremiyet yönleriyle değerlendirilmelidir.", "Kabinleri destek görevlisi ve çevrim dışı acil planıyla pilot bölgede sınamak dengeli uygulamadır.", "Süre kazanımı gerçek olsa da donma ve kullanım güçlüğü giderilmeden hizmet herkes için güvenilir değildir.", ["Uzaktan hizmet yeni olduğu için yüz yüze desteğe hiçbir koşulda ihtiyaç bırakmaz.", "Bağlantı sorunu sağlık kararlarının güvenilirliğini etkilemez.", "Kullanıcıların erişilebilirlik gereksinimlerini sormak teknolojik ilerlemeyi yavaşlattığı için gereksizdir."], "Teknoloji öngörüsü yalnız olanağı değil, farklı kullanıcıların gerçek koşullarında oluşabilecek risk ve destek gereksinimini de kapsar."),
    ("tr-g06-bty-note-003", "Bir mağaza ürün fiyatına yüzde 10 indirim uygulayan tablo hazırlıyor ve indirim oranını E1 hücresinde tutuyor.", "C2 hücresindeki indirim formülü aşağı kopyalandığında mutlak E1 başvurusu sabit kalıyor.", "Dolar işaretli mutlak başvuru, formül başka hücrelere kopyalansa da indirim oranının E1'den alınmasını sağlar.", "Oranı tek hücrede tutup ürün formülünde mutlak E1 başvurusunu kullanmak doğru uygulamadır.", "Kopyalanan satırlarda E1'in değişmemesi, mutlak başvurunun ortak oranı koruduğunu gösterir.", ["Mutlak E1 yazımı hücreyi formül dışında bırakır ve indirimi sıfırlar.", "Formül aşağı kopyalanınca bütün başvuruların sabit kalması zorunludur.", "İndirim oranını her satıra elle farklı yazmak tutarlılığı otomatik garanti eder."], "Göreli başvuru satırla değişen veriyi, mutlak başvuru ortak sabiti temsil eder; formülün kopyalanacağı yön buna göre planlanır."),
    ("tr-g06-bty-note-004", "Bir ortalama formülü boş hücre sayısını payda olarak kullanınca #SAYI/0! benzeri bölme hatası veriyor.", "Veri girilen satırda sonuç oluşuyor, hiç kayıt olmayan satırda payda sıfır kalıyor.", "Sıfıra bölme hatası, formülün paydasının veri olmayan durumda sıfır olmasından kaynaklanır.", "Paydayı oluşturan hücreleri ve boş durum kuralını denetleyip veri yoksa açıklayıcı sonuç göstermek gerekir.", "Hatanın yalnız boş satırda oluşması, sorunun dosyanın tamamında değil sıfır payda koşulunda olduğunu gösterir.", ["Bölme hatasını gidermek için bütün sayıları metne çevirmek gerekir.", "Paydanın sıfır olması bölme sonucunu değiştirmez.", "Hata iletisini gizlemek formülün matematiksel sorununu kendiliğinden düzeltir."], "Tablolama hatası, hangi girdide oluştuğu yeniden üretilerek ve formülün ara değerleri incelenerek kaynağına kadar daraltılır."),
    ("tr-g06-bty-note-005", "Turnuva kayıt tablosunda okul numarası sütununa harf ve yinelenen numaralar giriliyor.", "Yalnız sayı kabul eden doğrulama ve yinelenenleri işaretleyen kural açılınca üç hatalı kayıt bulunuyor.", "Veri doğrulama, alanın beklenen tür ve aralığına uymayan girişleri daha başta azaltır.", "Okul numarasına sayı ve benzersizlik denetimi uygulayıp bulunan hataları asıl listeden doğrulamak gerekir.", "Kurallar açılınca sorunların görünmesi, önceki tablonun giriş kısıtlarından yoksun olduğunu gösterir.", ["Okul numarası alanında her türlü metni kabul etmek kayıt eşleştirmeyi kolaylaştırır.", "Yinelenen numaraları rastgele silmek hangi öğrencinin doğru olduğunu kanıtlar.", "Veri doğrulama yalnız hücre rengini değiştirir; giriş kalitesini etkilemez."], "Alan kuralları veri toplamadan önce tanımlanır; otomatik işaretlenen kayıtlar güvenilir kaynağa dönülerek düzeltilir."),
    ("tr-g06-bty-note-006", "Okul servisi gecikmeleri duraklara göre filtrelenip özetleniyor.", "A durağında 12 kaydın 9'u yağmurlu günlerde, B durağında gecikmeler hava durumuna göre değişmiyor.", "Yağmur ile gecikme ilişkisi A durağında görülür; aynı sonucun bütün duraklara genellenmesi desteklenmez.", "Durak ve hava durumunu ayrı sütunlarda filtreleyip oranları durak bazında karşılaştırmak uygun analizdir.", "B durağındaki farklı örüntü, tek durağın sonucunun tüm güzergâha taşınamayacağını gösterir.", ["A durağındaki örüntü bütün şehirde yağmurun aynı gecikmeyi oluşturduğunu kanıtlar.", "Filtrelenen satırları yok sayıp yalnız toplam kayıt sayısına bakmak ilişkiyi açıklar.", "İki kategori karşılaştırılırken durak bilgisi gereksizdir."], "Bulgular alt gruplara göre değişebilir; filtre ve oranlar doğru payda ile yorumlanır, kapsam dışına taşırılmaz."),
    ("tr-g06-bty-note-007", "Tiyatro kaydında oyuncuların bazı cümleleri çok düşük, alkışlar ise aşırı yüksek duyuluyor.", "Seviye ölçer alkışta kırmızı bölgeye ulaşıyor; normalizasyon sonrası konuşma anlaşılır ve tepe değerleri sınırda kalıyor.", "Ses seviyesi düzenlemesi, aşırı tepeleri kırpmadan konuşma ile yüksek bölümler arasında dinlenebilir denge kurmalıdır.", "Özgün dosyayı koruyup bölümleri ölçerek seviyeyi ayarlamak ve taşma olup olmadığını dinlemek gerekir.", "Kırmızı tepelerin kaybolup konuşmanın korunması, seviye işleminin bozulmayı azalttığını gösterir.", ["Bütün bölümleri en yüksek seviyeye çıkarmak her kaydı bozulmadan eşitler.", "Kırmızı seviye göstergesi sesin mutlaka daha kaliteli olduğunu belirtir.", "Konuşmayı anlaşılır yapmak için alkış bölümünü tümüyle silmek zorunludur."], "Seviye ayarı hedef sesi korur, dijital taşmayı önler ve sonuç ölçümle birlikte kulakla denetlenir."),
    ("tr-g06-bty-note-008", "Bir masal podcastinde anlatıcı, karakter sesleri ve ortam efektleri ayrı kanallarda bulunuyor.", "Ejderha efekti anlatıcının önemli cümlesini örtüyor; efekt iki saniye erkene alınınca anlam açık kalıyor.", "Ses kurgusunda efektin zamanlaması ve seviyesi anlatının anlaşılmasını desteklemeli, konuşmayı örtmemelidir.", "Efekti ilgili olaydan hemen önce ve daha düşük düzeyde kullanıp geçişi ön izlemek gerekir.", "Zamanlama değişince cümlenin anlaşılması, sorunun kaydın içeriğinden çok kanal yerleşiminde olduğunu gösterir.", ["Efekt ne kadar yüksekse dinleyici masalı o kadar doğru anlar.", "Farklı ses kanallarının zaman çizelgesindeki yeri anlatımı etkilemez.", "Konuşmayı örten efekti düzeltmek için bütün anlatıcı kaydını silmek gerekir."], "Çok kanallı kurguda her öğenin zamanı, seviyesi ve anlatıdaki görevi birlikte düzenlenir."),
    ("tr-g06-bty-note-009", "Dil öğrenme kaydında her sözcükten sonra kısa tekrar boşluğu bırakılacak.", "İlk dosyada boşluklar değişken; işaretleyicilerle düzenlenince her sözcük sonrası üç saniye oluyor.", "Tutarlı aralıklar hedef kullanıcının tekrar yapmasını kolaylaştırır ve kurgu işaretleyicileri zamanlamayı denetlenebilir kılar.", "Sözcük sınırlarını işaretleyip eşit tekrar aralıkları eklemek, sonra tüm kaydı gerçek hızda dinlemek gerekir.", "Aralıklar eşitlenince öğrencilerin zamanında tekrar edebilmesi, düzenlemenin kullanım amacına uyduğunu gösterir.", ["Rastgele boşluk süreleri öğrenme kaydını daha öngörülebilir yapar.", "Sessizlik bölümleri ses ürünü sayılmaz ve zaman çizelgesinde düzenlenemez.", "Yalnız dosya adını değiştirmek aralık sürelerini eşitler."], "Ses ürünü geliştirme, içerik kadar hedeflenen dinleme davranışına uygun süre ve yapı tasarımını da içerir."),
    ("tr-g06-bty-note-010", "İşaret dili videosuna konuşmayı açıklayan altyazı ekleniyor.", "İlk altyazılar konuşmadan iki saniye sonra geliyor; zaman kodları düzeltilince metin ilgili hareketle eşleşiyor.", "Altyazı zamanlaması konuşma ve görüntüyle eşleşmeli, okunabilecek süre boyunca ekranda kalmalıdır.", "Zaman kodlarını cümle başlangıç ve bitişlerine göre ayarlayıp farklı hızlarda ön izleme yapmak uygundur.", "Düzeltme sonrası metin ile hareketin eşleşmesi, sorunun altyazı içeriğinden değil zamanlamadan kaynaklandığını gösterir.", ["Altyazının konuşmadan sonra gelmesi anlamı her zaman güçlendirir.", "Bütün altyazıları videonun ilk karesinde göstermek erişilebilirliği artırır.", "Zaman kodu yalnız yazı rengini belirler."], "Erişilebilir video düzenlemesinde metnin doğruluğu, okunabilirliği ve zaman eşleşmesi birlikte sınanır."),
    ("tr-g06-bty-note-011", "Bir deney videosu hızlı kesmeler yüzünden ölçüm adımlarını göstermeden sonuca atlıyor.", "Kesme süreleri uzatılıp ölçüm ekranı eklendiğinde izleyiciler işlemi doğru sırada anlatabiliyor.", "Kurgu temposu hedef kitleye gerekli kanıtı görme süresi vermeli; hız bilgi kaybına yol açmamalıdır.", "Ölçüm anlarını koruyup gereksiz beklemeleri kısaltmak ve izleyici testi yapmak doğru yaklaşımdır.", "İzleyicinin sırayı düzeltmesi, ölçüm karelerinin anlatı için gerekli olduğunu gösterir.", ["En hızlı kesme her öğretici videoyu daha anlaşılır yapar.", "Sonuç gösteriliyorsa ölçüm kanıtını videoda tutmak gereksizdir.", "Kurgu temposu hedef kitle ve içerik karmaşıklığından bağımsızdır."], "Video kurgusu süreyi azaltırken neden-sonuç ve kanıt zincirini korur; tempo izleyicinin anlayabileceği düzeyde seçilir."),
    ("tr-g06-bty-note-012", "Spor videosu 60 kare/saniye çekiliyor fakat okul sitesi yalnız 30 kare/saniye istiyor.", "30 kare/saniyelik çıktı yarı boyuta yaklaşıyor ve normal hızdaki hareket akıcı kalıyor.", "Kare hızı hedef platform ve hareket gereksinimine göre seçilir; daha yüksek değer her zaman zorunlu değildir.", "Kaynak projeyi koruyup site profiline uygun kare hızında çıktı almak ve hareketi kontrol etmek gerekir.", "Daha küçük çıktı akıcılığı koruyorsa 60 kare/saniye bu kullanım için gerekli değildir.", ["Kare hızı dosya boyutunu ve hareket görünümünü hiç etkilemez.", "30 kare/saniyeye dönüştürmek videonun sesini zorunlu olarak siler.", "En yüksek kare hızı bütün platformlarda tek doğru seçimdir."], "Dışa aktarma ayarı hedef platform, hareket türü, kalite ve dosya boyutunun dengesiyle belirlenir."),
    ("tr-g06-bty-note-013", "Bir öğrenci 'mikroplastik etkisi' araştırmasında yalnız reklam bağlantılarına tıklıyor.", "Arama terimine site:.edu.tr ve rapor eklenince üniversite raporları bulunuyor; reklam sayfaları ürün satıyor fakat kaynak vermiyor.", "Arama sorgusunu kaynak türü ve anahtar kavramlarla daraltmak güvenilir bilgiye ulaşmayı kolaylaştırır.", "Kurum raporlarını tarih ve kaynakçayla karşılaştırıp reklâm içeriğini kanıt olarak kullanmamak gerekir.", "Kaynaklı raporların daraltılmış sorguyla bulunması, arama sözcüğü seçiminin sonuç kalitesini etkilediğini gösterir.", ["Reklam etiketi taşıyan ilk sonuç bilimsel olarak en güvenilir kaynaktır.", "Arama sorgusuna bağlam eklemek sonuçların doğruluğunu azaltır.", "Bir sayfanın ürün satması sunduğu bütün iddiaları kanıtlar."], "Amaçlı aramada sorgu geliştirilir; yazarlık, kurum, tarih, kaynakça ve çıkar ilişkisi sonuç değerlendirmesine katılır."),
    ("tr-g06-bty-note-014", "Robotik takımında sabit bilgisayarlar kabloyla, hareketli tabletler kablosuz ağa bağlanıyor.", "Kablolu bilgisayarda gecikme düşük; tabletler hareket edebiliyor fakat uzak köşede sinyal zayıflıyor.", "Kablolu ve kablosuz bağlantıların güçlü yönleri kullanımın hareketlilik ve kararlılık gereksinimine göre değişir.", "Sabit denetim bilgisayarında kablo, hareketli tabletlerde kapsaması ölçülmüş kablosuz bağlantı kullanmak uygundur.", "Farklı sonuçlar tek bir bağlantı türünün her görev için üstün olmadığını gösterir.", ["Kablosuz bağlantı her mesafede aynı sinyal gücünü garanti eder.", "Kablolu bağlantı yalnız hareketli aygıtlar için tasarlanmıştır.", "Bağlantı seçerken hareketlilik ve gecikme ölçütleri dikkate alınmaz."], "İletişim teknolojisi fiziksel ortam, menzil, hareketlilik, hız ve güvenlik gereksinimine göre sınıflandırılıp seçilir."),
    ("tr-g06-bty-note-015", "Bir öğrenci büyük video dosyasını yerel ağdaki dört bilgisayara aynı anda gönderiyor.", "Aktarım sırasında herkesin hızı düşüyor; gönderimler sıraya alınınca bağlantı daha kararlı oluyor.", "Ağın bant genişliği paylaşılan bir kaynaktır; eş zamanlı büyük aktarımlar her kullanıcıya kalan kapasiteyi azaltabilir.", "Büyük aktarımları uygun saate veya sıraya planlamak ve gereksiz kopyaları önlemek doğru ağ yönetimidir.", "Sıralı aktarımda kararlılığın artması, dar boğazın tek bilgisayardan çok ortak kapasiteyle ilişkili olduğunu gösterir.", ["Aynı anda daha çok büyük dosya göndermek her kullanıcının hızını artırır.", "Bant genişliği ağdaki etkin kullanıcı sayısından etkilenmez.", "Aktarım yavaşsa tüm dosyaları tekrar tekrar başlatmak kapasite sorununu çözer."], "Ağ performansı trafik miktarı ve ortak kaynak paylaşımıyla değerlendirilir; planlama ve ölçümle iyileştirilir."),
    ("tr-g06-bty-note-016", "Bir hesap doğru parola girilse bile yeni bir cihazdan oturum açma kodu istiyor.", "Saldırgan parolayı öğrenmiş ancak kullanıcının doğrulama uygulamasındaki kod olmadan hesaba giremiyor.", "Çok adımlı doğrulama, parola ele geçirilse bile ikinci kanıtla yetkisiz erişimi zorlaştırır.", "Giriş denemesini reddedip parolayı değiştirmek, açık oturumları kapatmak ve kurtarma yöntemlerini kontrol etmek gerekir.", "İkinci kodun saldırıyı durdurması, tek paroladan bağımsız ek güvenlik katmanının etkisini gösterir.", ["İkinci doğrulama kodunu isteyen herkese göndermek hesabı korur.", "Parola sızdıysa çok adımlı doğrulamanın hiçbir etkisi olamaz.", "Şüpheli girişten sonra aynı parolayı başka hesaplarda kullanmaya devam etmek güvenlidir."], "Hesap güvenliğinde benzersiz parola, ikinci doğrulama, oturum denetimi ve olay sonrası değişiklik birlikte uygulanır."),
    ("tr-g06-bty-note-017", "Bir öğrenci internet yazısının üç paragrafını ödevine aynen alıp yalnız bağlantıyı sona ekliyor.", "Benzerlik kontrolü paragrafları birebir işaretliyor; öğretmen alıntı işareti ve özgün açıklama bulunmadığını görüyor.", "Kaynakça yazmak, aynen alınan metni alıntı olarak belirtme ve özgün katkı sunma sorumluluğunu ortadan kaldırmaz.", "Kısa gerekli bölümü açık alıntı ve kaynakla göstermek, geri kalanını anlayarak özgün biçimde açıklamak gerekir.", "Birebir eşleşme ve alıntı işaretinin yokluğu, bağlantı verilse bile metnin uygun kullanılmadığını gösterir.", ["Bağlantı sona yazılınca sınırsız metin kendi cümlemiz sayılır.", "Sözcüklerin yerini az değiştirmek telif ve akademik dürüstlük sorununu kesin çözer.", "Ödev eğitim amaçlı olduğu için kaynak belirtmek hiçbir zaman gerekmez."], "Telif ve akademik dürüstlükte izin, ölçülü kullanım, açık alıntı, kaynak ve öğrencinin kendi düşünsel katkısı birlikte aranır."),
    ("tr-g06-bty-note-018", "Bir fener uygulaması rehbere ve mikrofona erişim istiyor.", "Erişimler reddedildiğinde fener yine çalışıyor; uygulama mağazası açıklaması bu verilerin neden gerektiğini söylemiyor.", "Uygulamanın temel işleviyle ilgisiz izin talepleri veri azaltma ve mahremiyet açısından reddedilmelidir.", "Gereksiz izinleri kapatıp uygulamayı güvenilir kaynaktan güncellemek veya daha az izin isteyen alternatifi seçmek gerekir.", "Fenerin izinler olmadan çalışması, rehber ve mikrofon verisinin temel işlev için zorunlu olmadığını gösterir.", ["Uygulama mağazada bulunduğu için istediği bütün izinler zorunlu ve güvenlidir.", "Fener yakmak için rehberdeki bütün kişilerin yüklenmesi gerekir.", "Bir kez verilen uygulama izinleri sonradan incelenemez veya kapatılamaz."], "Dijital güvenlikte izin, uygulamanın açık işleviyle orantılı olmalı ve kullanıcı erişimleri düzenli denetlemelidir."),
    ("tr-g06-bty-note-019", "Kod kulübü ücretsiz bir programı okul bilgisayarlarına kurmak istiyor.", "Program ücretsiz indiriliyor fakat lisansı değiştirme, kopyalama ve toplu kurulum hakkını sınırlandırıyor.", "Ücretsiz fiyat, yazılımın özgür veya açık kaynak olduğu anlamına gelmez; kullanım haklarını lisans belirler.", "Toplu kurulum iznini lisans metninden doğrulamak, uygun değilse izin almak veya uyumlu lisanslı alternatif seçmek gerekir.", "Hakların sınırlandırılması, fiyat sıfır olsa bile yazılımın koşulsuz yeniden dağıtılamayacağını gösterir.", ["Ücretsiz indirilen yazılımın lisans koşulu olamaz.", "Kaynak kodu kapalıysa programı istediğimiz kadar kopyalamak zorunlu olarak serbesttir.", "Lisans yalnız program simgesinin rengini belirler."], "Yazılım seçiminde fiyat, kaynak kodu erişimi ve çalıştırma-kopyalama-değiştirme-dağıtma hakları birbirinden ayrılır."),
    ("tr-g06-bty-note-020", "Yüz ifadesi modeli için sınıf arkadaşlarının fotoğrafları izin formu olmadan ortak klasöre yükleniyor.", "Bazı öğrenciler fotoğraflarının silinmesini istiyor; klasör bağlantısına okul dışından da erişilebiliyor.", "Yüz görüntüsü kişisel veridir; açık amaç, bilgilendirilmiş izin, güvenli saklama ve silme hakkı gözetilmelidir.", "İzinsiz toplamayı durdurup erişimi kapatmak, kayıtları silmek ve gönüllü izinli veriyle yeniden planlamak gerekir.", "Dış erişim ve silme talebi, veri yönetiminin hem güvenlik hem rıza yönünden yetersiz olduğunu gösterir.", ["Model eğitimi amacı kişisel veri için otomatik ve sınırsız izin verir.", "Ortak bağlantı ne kadar çok kişiye açılırsa yüz verisi o kadar güvenli olur.", "Fotoğraf bir kez yüklenince sahibinin silme talebi dikkate alınmaz."], "Yapay zekâ verisi teknik girdi olmanın yanında kişisel hak taşır; en az veri, amaç sınırlaması, izin ve güvenli silme uygulanır."),
    ("tr-g06-bty-note-021", "Bir üretken yapay zekâ okul tarihi için iki kitap adı ve yazar öneriyor.", "Kütüphane kataloğunda kitaplardan biri yok, diğerinin yazarı farklı; araç kesin konuşuyor fakat kaynak vermiyor.", "Üretken yapay zekâ gerçeğe benzer fakat uydurma kaynak üretebilir; her eser bilgisi gerçek katalogdan doğrulanmalıdır.", "Kitapları kütüphane ve yayıncı kataloglarında arayıp doğrulanmayan kaynağı ödevden çıkarmak gerekir.", "Katalog uyuşmazlığı, akıcı yanıtın bibliyografik doğruluğu garanti etmediğini gösterir.", ["Kitap adı ayrıntılıysa katalogda bulunmasa da gerçek kabul edilir.", "Aynı yapay zekâya tekrar sormak bağımsız kaynak doğrulamasıdır.", "Yanlış yazar adını kaynakçada kullanmak ödevin güvenilirliğini artırır."], "Yapay zekâ çıktıları özellikle ad, tarih, alıntı ve kaynaklarda birincil veya yetkili kataloglarla doğrulanır."),
    ("tr-g06-bty-note-022", "Burs öneri modeli geçmiş veride yalnız yüksek gelirli bölgelerden öğrenci örnekleriyle eğitiliyor.", "Genel doğruluk yüksek görünürken düşük gelirli bölge testinde başarılı adayların çoğu kaçırılıyor.", "Genel başarı, alt gruplardaki dengesiz hatayı gizleyebilir; temsil ve grup bazlı değerlendirme gerekir.", "Veriyi hedef grupları temsil edecek biçimde dengeleyip hata oranlarını grup bazında incelemek gerekir.", "Hatanın belirli bölgede yoğunlaşması, modelin bütün kullanıcılar için eşit güvenilir olmadığını gösterir.", ["Genel doğruluk yüksekse hiçbir alt grubun sonucuna bakılmaz.", "Az temsil edilen grubu testten çıkarmak adalet sorununu çözer.", "Geçmiş verideki her örüntü değiştirilmeden gelecekte uygulanmalıdır."], "Model kalitesi yalnız toplam doğruluk değil, veri temsili, alt grup hata oranları ve kararın insan üzerindeki etkisiyle değerlendirilir."),
    ("tr-g06-bty-note-023", "Bir oyunda 'başla' iletisi gelince üç karakterin aynı anda hareket etmesi isteniyor.", "Yalnız bir karakterde ileti alındığında bloğu var; diğer ikisi hareketsiz kalıyor.", "Yayın iletisi bütün karakterlere ulaşsa da yalnız ilgili olayı dinleyen kod yığınları çalışır.", "Her karaktere aynı iletiyi alan olay bloğu ekleyip kendi hareket komutlarını bu bloğun altına bağlamak gerekir.", "İletiyi dinleyen tek karakterin hareket etmesi, yayının değil alıcı olay bloklarının eksik olduğunu gösterir.", ["Yayın iletisi gönderilince olay bloğu olmayan karakterler de rastgele hareket eder.", "Karakterleri eş zamanlı başlatmak için her birine farklı ve ilgisiz tuş atamak zorunludur.", "Olay blokları yalnız kostüm rengini değiştirir, kodu başlatmaz."], "Blok tabanlı programda iletiler bileşenleri eşgüdümler; gönderen ve dinleyen olayların doğru adı paylaşması gerekir."),
    ("tr-g06-bty-note-024", "Bir ekip akıllı sera projesini tek parça uzun blok yığınıyla yazıyor ve hata yerini bulamıyor.", "Sulama, ekran ve alarm ayrı özel bloklara bölününce her bölüm bağımsız test ediliyor ve alarm hatası hızla bulunuyor.", "Büyük problemi küçük görev ve özel bloklara ayırmak geliştirme, test ve yeniden kullanımı kolaylaştırır.", "Gereksinimleri sulama, gösterim ve alarm alt görevlerine ayırıp her biri için test yazmak gerekir.", "Ayrıştırma sonrası hatanın alarm bölümüne daralması, modüler tasarımın hata ayıklamayı kolaylaştırdığını gösterir.", ["Bütün komutları tek yığında tutmak hatanın yerini her zaman daha açık yapar.", "Özel bloklar yalnız kodu uzatır ve yeniden kullanılamaz.", "Problemi parçalara ayırmak görevler arası ilişki kurmayı imkânsızlaştırır."], "Yazılım süreci ayrıştırma, açık arayüz, küçük test ve bütünleştirme adımlarıyla karmaşıklığı yönetir."),
    ("tr-g06-bty-note-025", "Bir proje kameradan yüz ifadesi okuyup öğrencinin duygusunu kesin olarak sınıfa ilan ediyor.", "Aynı öğrenci için ışık değişince farklı etiket geliyor; öğrenci etiketin yanlış ve rahatsız edici olduğunu söylüyor.", "Yüz ifadesi modeli duyguyu kesin bilemez; belirsizlik, bağlam, mahremiyet ve kullanıcı onayı tasarımda korunmalıdır.", "Kesin ilanı kaldırıp gönüllü kullanıma geçmek, düşük güveni belirtmek ve hassas sonucu başkalarıyla paylaşmamak gerekir.", "Işıkla değişen etiket ve kullanıcı itirazı, çıktının kesin kişisel gerçek olarak sunulamayacağını gösterir.", ["Model bir etiket verdiğinde kişinin kendi açıklaması geçersiz olur.", "Hassas tahmini sınıfa duyurmak doğruluğu artırır.", "Işık koşulu görüntü modelinin sonucunu hiçbir zaman etkilemez."], "Yapay zekâ destekli ürün, teknik belirsizliği gizlemez; hassas çıkarımlarda rıza, zarar vermeme ve kullanıcı denetimini önceler."),
]


DKAB_CASES = [
    ("tr-g06-dkab-note-001", "Bir öğrenci peygamberlerin yalnız geleceği haber vermek için gönderildiğini söylüyor.", "Konu anlatımında peygamberlerin vahyi insanlara açıklayıp örnek oldukları belirtiliyor.", "Peygamberler Allah'tan aldıkları vahyi insanlara bildirir, açıklar ve yaşayışlarıyla örnek olur.", "Peygamberlerin mesajı ile örnek davranışlarını birlikte incelemek doğru yaklaşımdır.", "Bilgilendirme ve örnekliğin birlikte verilmesi, görevin tek bir haber türüyle sınırlandırılamayacağını gösterir.", ["Peygamberlerin görevi yalnız bilinmeyen gelecek olaylarını söylemektir.", "İlahi mesajın insan davranışıyla hiçbir ilişkisi yoktur.", "Peygamberler vahyi açıklamadan yalnız kendileri için saklamıştır."], "Peygamberlik görevi tebliğ, açıklama ve örnek olma boyutlarıyla ele alınır; tarihsel veya siyasi işlevler hakkında kanıtsız mutlaklık kurulmaz."),
    ("tr-g06-dkab-note-002", "Bir sınıf vahyin insanlara gönderiliş amacını tartışıyor.", "Öğrenciler doğruyu yanlıştan ayırma, sorumluluğu hatırlama ve iyi davranışa yönelme örnekleri veriyor.", "Vahiy insanlara inanç, ibadet ve ahlak alanında rehberlik ederek doğruyu bulmalarına yardım eder.", "Bir davranışı değerlendirirken vahyin rehberlik ve sorumluluk ilkelerini birlikte kullanmak gerekir.", "Verilen örneklerin ortak yönü, vahyin insanın tercihlerini iyiliğe yönelten rehber oluşudur.", ["Vahyin amacı insanın düşünmesini ve sorumluluk almasını engellemektir.", "Vahiy yalnız geçmiş olayların tarihini ezberletmek için gönderilmiştir.", "İlahi rehberlik günlük davranış ve ahlakla ilişkilendirilemez."], "Vahyin amacı, insanın iradesini yok etmek değil doğru bilgi ve değerlerle bilinçli seçim yapmasına rehberlik etmektir."),
    ("tr-g06-dkab-note-003", "Bir öğrenci bütün ilahi kitapların farklı temel inançlar öğrettiğini ileri sürüyor.", "Ders notunda tevhid, iyilik ve sorumluluk çağrısının ilahi mesajların ortak yönü olduğu açıklanıyor.", "İlahi kitaplar farklı zaman ve toplumlara gönderilse de Allah'ın birliği ve iyi davranışa yönelme gibi temel ilkelerde ortak mesaj taşır.", "Kitapları karşılaştırırken gönderildikleri bağlamla ortak temel ilkeleri birbirinden ayırmak gerekir.", "Ortak tevhid ve ahlak vurgusu, farklı bağlamların bütünüyle çelişkili mesaj anlamına gelmediğini gösterir.", ["İlahi kitapların hiçbir ortak mesajı bulunmaz.", "Farklı toplumlara gönderilmek Allah'ın birliği ilkesini değiştirir.", "İlahi kitap inancı yalnız kitap adlarını ezberlemekten ibarettir."], "Karşılaştırma, ortak inanç-ahlak ilkeleri ile tarihsel bağlam ve uygulama ayrıntılarını karıştırmadan yapılır."),
    ("tr-g06-dkab-note-004", "Bir öğrenci Felak suresini yalnız gece okunabilecek bir metin olarak tanımlıyor.", "Surenin anlamında yaratılmışların, karanlığın ve haset edenin şerrinden Allah'a sığınma ifadeleri yer alıyor.", "Felak suresi, insanın karşılaşabileceği kötülüklerden Allah'a sığınmasını öğreten bir duadır; yalnız belirli bir saate indirgenmez.", "Sureyi anlamıyla okuyup korku karşısında tedbir alırken Allah'a sığınma bilincini korumak gerekir.", "Birden çok kötülük türünün anılması, mesajın yalnız gece vaktine ait olmadığını gösterir.", ["Felak suresinin anlamında hiçbir sığınma ifadesi yoktur.", "Sure yalnız gündüz okunursa anlamlıdır ve başka zamanda okunamaz.", "Allah'a sığınmak insanın gerekli tedbirleri tamamen bırakması demektir."], "Sure anlamı bağlamından okunur; dua ve sığınma bilinci sorumlu davranış ve tedbirle çeliştirilmez."),
    ("tr-g06-dkab-note-005", "Bir öğrenci Ramazan'ı yalnız aç kalınan bir ay olarak anlatıyor.", "Konu anlatımında Kur'an, oruç, paylaşma, sabır ve ibadet bilinci birlikte ele alınıyor.", "Ramazan, Kur'an ayı ve oruç ibadetiyle birlikte paylaşma, sabır ve kulluk bilincinin güçlendiği bir dönemdir.", "Ramazan etkinliğinde ibadet bilgisini ihtiyaç sahipleriyle dayanışma ve güzel davranışlarla birlikte planlamak gerekir.", "Çok yönlü örnekler, Ramazan'ın yalnız bedensel açlıkla açıklanamayacağını gösterir.", ["Ramazan'ın Kur'an ve ibadet bilinciyle hiçbir ilişkisi yoktur.", "Oruç yalnız yemek saatini değiştiren bir alışkanlıktır.", "Paylaşma ve sabır Ramazan'ın anlamına dâhil değildir."], "Ramazan ve oruç, şekil şartlarının yanında niyet, öz denetim, paylaşma ve ahlaki gelişim boyutlarıyla anlaşılır."),
    ("tr-g06-dkab-note-006", "Bir öğrenci oruçluyken kırıcı konuşmanın ibadetle ilgisi olmadığını savunuyor.", "Ders örneğinde orucun yalnız yeme içmeden uzak durmak değil davranışları da iyileştirmek olduğu vurgulanıyor.", "Oruç, belirli süre yeme içmeden uzak durmanın yanında dili ve davranışları kötülükten koruma bilinci kazandırır.", "Tartışmada kırıcı sözü bırakıp özür dilemek ve öz denetimi sürdürmek orucun amacına uygun davranıştır.", "Ahlaki davranış vurgusu, ibadetin kişinin söz ve tutumlarından bağımsız olmadığını gösterir.", ["Oruçluyken başkasını incitmek ibadetin anlamını hiçbir biçimde etkilemez.", "Oruç yalnız susuz kalma süresini ölçen bir yarışmadır.", "Öz denetim ve güzel sözün oruçla bağlantısı kurulamaz."], "İbadetin biçimsel yönü ile ahlaki amacı birlikte ele alınır; sağlık ve dinî uygulama ayrıntılarında yetkili kaynaklara başvurulur."),
    ("tr-g06-dkab-note-007", "Bir öğrenci orucun insanı yalnız güçsüz bıraktığını, irade ve sabırla hiçbir ilişkisi olmadığını söylüyor.", "Konu anlatımında kişinin isteğini ertelemesi, sabırlı davranması ve ihtiyaç sahiplerini anlaması orucun kazanımları arasında gösteriliyor.", "Oruç, kişinin iradesini ve sabrını geliştirmesine, empati ve şükür bilinci kazanmasına katkı sağlayabilir.", "Gün içinde sabırlı ve saygılı davranıp ihtiyaç sahiplerine duyarlı olmak bu kazanımları hayata yansıtır.", "İstek erteleme ve empati örnekleri, orucun yalnız bedensel güçsüzlük olarak açıklanamayacağını gösterir.", ["Oruç irade, sabır ve empati gelişimini hiçbir biçimde destekleyemez.", "İsteği ertelemek öz denetim değil sorumsuzluk göstergesidir.", "İhtiyaç sahiplerini anlamak orucun toplumsal yönüyle ilişkisizdir."], "Orucun kazanımları fiziksel deneyimin bilinçli öz denetim, sabır, şükür ve dayanışma davranışlarına dönüşmesiyle değerlendirilir."),
]


DIN_POSITIONS = {7: 0, 22: 1, 31: 2, 50: 6, 54: 3, 68: 4, 96: 5}
MODE_SEQUENCE = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
LEVEL_SEQUENCE = [1] * 15 + [2] * 10 + [1] * 5 + [2] * 15 + [3] * 15 + [3] * 10 + [4] * 10 + [5] * 5 + [3] * 5 + [4] * 10


def read_notes_only(path: Path) -> dict[str, dict[str, Any]]:
    notes: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("type") == "note":
            notes[str(row.get("id"))] = row
    return notes


def make_table(qid: str, scenario: str, evidence: str, labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.alt"
    labels[h1], labels[h2] = "İncelenen öğe", "Kanıt kaydı"
    labels[alt] = "Bir durum ile gözlenen veya metinden çıkarılan kanıtı iki satırda veren tablo; doğru değerlendirme açıklanmamıştır."
    return {"kind": "table", "headerKeys": [h1, h2], "rows": [[{"v": "Durum"}, {"v": scenario}], [{"v": "Kanıt"}, {"v": evidence}]], "altTextKey": alt}


def make_question(local: int, case: tuple[Any, ...], mode: str, level: int,
                  note: dict[str, Any], labels: dict[str, str], subject: str,
                  *, batch_number: int = 3, number_base: int = 200) -> dict[str, Any]:
    note_id, scenario, evidence, concept, action, inference, wrongs, rationale = case
    number = number_base + local
    if subject.startswith("Din"):
        slug = "dkab"
    elif subject == "Fen Bilimleri":
        slug = "fen"
    else:
        slug = "bty"
    qid = f"tr-g06-bank-{slug}-b{batch_number:02d}-q{local:03d}"
    correct_position = (local - 1) % 4
    topic = str(note["title"]).replace("İ", "i").replace("I", "ı").lower()
    if subject.startswith("Din"):
        for source, target in (
            ("hz. muhammed", "Hz. Muhammed"), ("allah", "Allah"),
            ("ramazan", "Ramazan"), ("kur’an", "Kur’an"),
            ("kur'an", "Kur'an"), ("felak suresi", "Felak suresi"),
            ("fil suresi", "Fil suresi"),
        ):
            topic = topic.replace(source, target)
    variant5 = (local - 1) % 5
    if mode == "comprehension":
        correct, figure = concept, None
        template_id = f"g6-b{batch_number:02d}-concept-v{variant5 + 1}"
        stems = (
            f"{scenario} Bu durumu doğru kavram ilişkisiyle açıklayan ifade hangisidir?",
            f"{scenario} Bu örnekte {topic} bakımından ayırt edici temel bilgi hangi seçenekte verilmiştir?",
            f"{scenario} Konu anlatımının sınırlarını aşmadan kurulabilecek yargı hangisidir?",
            f"{scenario} Verilen örneği amaç ve işlev bakımından doğru sınıflandıran açıklama hangisidir?",
            f"{scenario} Bu olayda hangi temel ilke kavram yanılgısını önler?",
        )
        stem = stems[variant5]
        explanation = f"{rationale} Bu nedenle doğru seçenek, örneğin ayırt edici yönünü konu kapsamı içinde açıklar."
    elif mode == "application":
        combined = 51 <= local <= 60
        template_id = f"g6-b{batch_number:02d}-{'act-check' if combined else 'act'}-v{variant5 + 1}"
        figure = None
        if combined:
            correct = f"{action} Sonuç, başlangıçta belirlenen ölçüt ve elde edilen kanıtla yeniden değerlendirilmelidir."
            stem = f"{scenario} Uygulamada “{evidence}” kaydediliyor. Hem doğru eylemi hem sonuç denetimini içeren plan hangisidir?"
            explanation = f"{rationale} Doğru plan, konuya uygun davranışı seçer ve sonucunu somut kanıtla yeniden sınar."
        else:
            correct = action
            stems = (
                f"{scenario} Bu durumda uygulanabilir ve sorumlu yaklaşım hangisidir?",
                f"{scenario} {topic} bilgisi davranış veya tasarım kararına dönüştürülecektir. Hangi adım seçilmelidir?",
                f"{scenario} Dört öneriden hangisi hem amaca hem konu ölçütlerine uygundur?",
                f"{scenario} Sorunu gereksiz risk veya yanlış genelleme oluşturmadan ele alan işlem hangisidir?",
                f"{scenario} Bağlamdaki gereksinimler birlikte düşünüldüğünde hangi karar verilmelidir?",
            )
            stem = stems[variant5]
            explanation = f"{rationale} Doğru seçenek, temel bilgiyi bu yeni durumda uygulanabilir ve gerekçeli bir karara dönüştürür."
    elif mode == "analysis":
        correct = inference
        template_id = f"g6-b{batch_number:02d}-evidence-v{variant5 + 1}"
        analysis_context = {
            3: "yeni vaka", 4: "birinci bağımsız kanıt çalışması",
            5: "karşılaştırmalı ikinci kanıt çalışması",
        }.get(batch_number, f"{batch_number}. kanıt çalışması")
        stems = (
            f"Aşağıdaki tabloda {topic} hakkında {analysis_context} kapsamında bir durum ve kanıt verilmiştir. Hangi çıkarım iki kaydı birlikte açıklar?",
            f"Aşağıdaki tabloda yer alan {analysis_context} kanıtı {topic} kapsamında inceleniyor. Hangi sonuç bilgi sınırını aşmaz?",
            f"Aşağıdaki tabloda {topic} bağlamındaki durum ile gözlem {analysis_context} için eşleştirilmiştir. Hangi yorum doğrudan desteklenir?",
            f"Aşağıdaki tabloda {topic} için {analysis_context} sırasında neden ve sonuç ilişkisini denetleyecek iki kayıt vardır. Hangi değerlendirme ilişkiyi doğru kurar?",
            f"Aşağıdaki tabloda sunulan {analysis_context} kanıtına göre {topic} hakkında kısa bir rapor yazılacaktır. Hangi cümle yalnız verilen kanıta dayanır?",
        )
        stem = stems[variant5]
        explanation = f"{rationale} Tablodaki iki kayıt doğru çıkarımı destekler; daha geniş seçenekler kanıtın kapsamını aşar."
        figure = make_table(qid, scenario, evidence, labels)
    else:
        variant3 = (local - 1) % 3
        mistaken = wrongs[(local - 1) % 3]
        correct = f"Bu öğrenci görüşü şöyle düzeltilmelidir: {concept}"
        template_id = f"g6-b{batch_number:02d}-error-v{variant3 + 1}"
        stems = (
            f"Bir öğrenci “{mistaken}” diyor. Bu somut yanılgıyı konu anlatımına göre düzelten seçenek hangisidir?",
            f"Bir öğrenci {topic} konusunda “{mistaken}” sonucuna ulaşıyor. Hatalı kararı gerekçesiyle düzelten ifade hangisidir?",
            f"Bir öğrencinin çözümünde “{mistaken}” iddiası vardır. Gözden kaçırılan temel ölçütü geri kuran seçenek hangisidir?",
        )
        stem, figure = stems[variant3], None
        explanation = f"{rationale} Öğrencinin görüşü temel ölçütlerden birini dışarıda bıraktığı için doğru seçenek kavramı açıkça yeniden kurar."

    choices = rotate(correct, list(wrongs), correct_position)
    reason_map = {
        correct: f"Doğru gerekçe: {rationale} Seçenek amaç, bağlam ve kanıtı birlikte değerlendirir.",
        wrongs[0]: f"Tek boyuta indirgeme: {wrongs[0]} ifadesi konunun gerekli yönlerinden birini yok sayar ve eksik sonuç kurar.",
        wrongs[1]: f"Koşulsuz genelleme: {wrongs[1]} ifadesi sınırlı bir özelliği bütün durumlara taşıyarak kanıt sınırını aşar.",
        wrongs[2]: f"Kavram karışıklığı: {wrongs[2]} ifadesi amaç, görev, izin veya davranış ölçütünü yanlış bir sonuçla eşleştirir.",
    }
    visual_need = ({"level": "required", "role": "evidence", "rationale": "Durum ve kanıt yalnız tabloda bulunduğu için çözüm görsele bağlıdır.", "acceptableKinds": ["table"], "evidenceDimensions": ["durum", "kanıt"]} if figure else {"level": "none", "role": "none", "rationale": "Gerekli bağlam ve bilgi soru metninde eksiksiz verilmiştir.", "acceptableKinds": [], "evidenceDimensions": []})
    objective = str((note.get("objectives") or [note.get("objective")])[0])
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": number,
        "subject": subject, "grade": 6, "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — {batch_number}. özgün üretim partisi",
        "objective": objective, "objectiveId": objective, "noteId": note_id, "noteKey": note_id,
        "question": stem, "choices": choices, "correct": correct_position, "correctIndex": correct_position,
        "correctOption": choices[correct_position], "distractorWhy": [reason_map[x] for x in choices],
        "explanation": explanation, "level": level,
        "difficultyReason": f"Düzey {level}; {topic} bilgisini yeni bağlamda {mode} göreviyle kullanıp seçenekleri gerekçeleriyle ayırmayı gerektirir.",
        "questionType": mode, "familyId": f"tr-g06-bank-{slug}-b{batch_number:02d}-family-{local:03d}", "authoringTemplateId": template_id,
        "objectiveSource": note.get("objectiveSource"), "objectiveEvidenceId": note.get("objectiveEvidenceId"), "sourceRefs": note.get("sourceRefs") or [],
        "visualRequirement": "required" if figure else "none", "visualNeed": visual_need, "figure": figure,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    bty_notes, dkab_notes = read_notes_only(BTY_SOURCE), read_notes_only(DKAB_SOURCE)
    existing = [json.loads(x) for x in OUTPUT.read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(existing) != 200 or any(row.get("subject") != "Bilişim Teknolojileri ve Yazılım" for row in existing):
        raise RuntimeError("validated batches 01 and 02 must be regenerated before batch 03")
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    rows, bty_cursor = [], 0
    for local, (mode, level) in enumerate(zip(MODE_SEQUENCE, LEVEL_SEQUENCE), 1):
        if local in DIN_POSITIONS:
            case = DKAB_CASES[DIN_POSITIONS[local]]
            note, subject = dkab_notes[case[0]], "Din Kültürü ve Ahlak Bilgisi"
        else:
            case = BTY_CASES[bty_cursor % len(BTY_CASES)]
            bty_cursor += 1
            note, subject = bty_notes[case[0]], "Bilişim Teknolojileri ve Yazılım"
        rows.append(make_question(local, case, mode, level, note, labels, subject))
    if bty_cursor != 93:
        raise AssertionError(bty_cursor)
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + rows) + "\n", encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"batch": 3, "questions": 100, "ict": 93, "religion": 7, "total": 300, "labels": len(labels), "sourceQuestionReads": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
