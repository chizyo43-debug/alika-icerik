#!/usr/bin/env python3
"""Author the first 100 Grade 6 ICT bank questions from lesson notes only.

This authoring path deliberately reads only ``note`` records.  Lesson-package
questions are neither loaded nor transformed; the strict audit owns source-copy
detection after authoring.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from build_unique_question_banks import ROOT


SOURCE = ROOT / "turkiye/6-sinif/bilisim-teknolojileri/bilisim-teknolojileri-tum.jsonl"
OUTPUT = ROOT / "authoring/question-bank-blueprints/grade-6.jsonl"
LABELS_OUTPUT = ROOT / "authoring/question-bank-blueprints/grade-6-labels.json"


# note id, principle, responsible application, evidence-based inference,
# three plausible misconceptions, independent scenario, observable evidence,
# topic-specific rationale
KNOWLEDGE = [
    ("tr-g06-bty-note-001",
     "Yapay zekâ örüntülerden sonuç üretir; nesnelerin interneti ise sensörlü cihazların ağ üzerinden veri alışverişi yapmasını sağlar.",
     "Seradaki nem sensörlerini ağa bağlayıp ölçümlere göre sulama uyarısı üretmek, nesnelerin internetini amacına uygun kullanır.",
     "Sensör verisinin uzaktan izlenebilmesi, cihazların ağda veri paylaşan bir sistem oluşturduğunu gösterir.",
     ["Kamerada sanal nesne görünmeyen her uygulama artırılmış gerçekliktir.", "İnternete bağlanan her cihaz insan gibi düşünen bağımsız bir yapay zekâdır.", "Bir teknolojinin adı, hangi veriyi işlediğine ve hangi ihtiyacı karşıladığına bakılmadan belirlenebilir."],
     "Okul serasında nem ölçen küçük aygıtlar değerleri öğretmenin tabletine düzenli olarak gönderiyor.",
     "Tablet, üç saksının nem değerlerini aynı anda gösteriyor ve düşük değer için uyarı veriyor.",
     "Teknolojiyi sınıflandırırken görünen aygıttan çok veri toplama, bağlantı ve işleme işlevleri birlikte incelenir."),
    ("tr-g06-bty-note-002",
     "Gelecekteki bilişim çözümleri değerlendirilirken sağladığı yarar kadar erişilebilirlik, mahremiyet, güvenlik ve mesleklere etkisi de düşünülmelidir.",
     "Otonom servis aracı denenmeden önce farklı kullanıcılar için güvenlik senaryoları ve kişisel veri kuralları belirlenmelidir.",
     "Yeni sistem zamanı azaltırken kişisel konumları gereksiz topluyorsa yenilik yararlı olsa da tasarımın iyileştirilmesi gerekir.",
     ["Yeni olan her teknoloji kendiliğinden güvenli ve herkes için erişilebilirdir.", "Bir sistem hızlı çalışıyorsa kişisel veri toplamasının sınırı önemli değildir.", "Teknolojik değişime uyum yalnız yeni aygıt satın almakla sağlanır; yeni beceri öğrenmek gerekmez."],
     "Bir belediye, yolcuları durağa taşıyan sürücüsüz küçük araçları okul bölgesinde denemeyi planlıyor.",
     "Deneme raporu süreyi kısaltıyor; ancak tekerlekli sandalye erişimi ve konum kayıtlarının saklama süresi açıklanmıyor.",
     "Gelecek öngörüsü kesin tahmin değildir; olası yarar ve riskler kanıta, etik ilkelere ve kullanıcı gereksinimlerine göre tartılır."),
    ("tr-g06-bty-note-003",
     "Tablolama programında hücreler veri saklar; formüller eşittir işaretiyle başlar ve hücre başvuruları değişen verilerle sonucu günceller.",
     "Haftalık gider toplamını elle yazmak yerine =TOPLA(B2:B8) formülünü kullanmak hesaplamayı yeniden kullanılabilir kılar.",
     "B2:B8 değerlerinden biri değişince toplamın da değişmesi, hücre başvurulu formülün çalıştığını gösterir.",
     ["Formül yazılan hücreye eşittir işareti koymak işlemi metne dönüştürür.", "Bir toplamı hesaplamak için bütün değerleri her değişiklikte yeniden elle yazmak en güvenilir yöntemdir.", "Grafik oluşturmak verileri hücrelere düzenli girmeden de doğru sonuç üretir."],
     "Sınıf temsilcisi yedi günlük kantin harcamasını bir çalışma sayfasında izliyor.",
     "Bir günlük tutar düzeltildiğinde formül hücresindeki haftalık toplam otomatik olarak değişiyor.",
     "Hücre başvuruları ve işlevler, veriyi düzenli tutar ve girdiler değiştiğinde hesaplamayı otomatik yeniler."),
    ("tr-g06-bty-note-004",
     "Tablolama sorununu çözerken önce beklenen sonuç, veri türü, hücre başvurusu ve hata iletisi ayrı ayrı kontrol edilmelidir.",
     "#DEĞER! hatasında formülün kullandığı hücrelerde sayı yerine metin bulunup bulunmadığını incelemek uygun ilk adımdır.",
     "Sayısal sütundaki tek metin girdisi düzeltilince formül çalışıyorsa sorunun kaynağı veri türü uyumsuzluğudur.",
     ["Bir formül hata verdiğinde nedeni incelemeden bütün çalışma sayfasını silmek gerekir.", "Her hata iletisi internet bağlantısının kesildiğini gösterir.", "Yanlış sonuç veren formülü renk değiştirerek düzeltmek mümkündür; başvuruları kontrol etmek gerekmez."],
     "Kulüp bütçesi sayfasında toplam hücresi #DEĞER! uyarısı gösteriyor.",
     "Gider sütunundaki bir hücreye 250 yerine 'iki yüz elli' yazıldığı görülüyor.",
     "Sorun belirleme; belirtinin kaynağını veri, formül ve başvuru düzeyinde sınamayı, sonra küçük ve geri alınabilir düzeltme yapmayı gerektirir."),
    ("tr-g06-bty-note-005",
     "Veri tablosunda her sütun tek bir özelliği, her satır tek bir kaydı temsil etmeli; başlıklar ve veri biçimleri tutarlı olmalıdır.",
     "Anket yanıtlarını ad, sınıf ve tercih için ayrı sütunlara yerleştirip aynı yazım biçimini kullanmak temiz bir veri kümesi oluşturur.",
     "Aynı tercihin farklı yazımları tek biçime getirildiğinde kategori sayısının azalması, önceki veride tutarsızlık olduğunu gösterir.",
     ["Bir hücreye ad, sınıf ve tercih bilgisini birlikte yazmak filtrelemeyi kolaylaştırır.", "Boş hücreleri rastgele sıfırla doldurmak eksik veri sorununu her zaman çözer.", "Başlıksız sütunlar kullanmak verinin anlamını daha açık hâle getirir."],
     "Okul kulübü seçimleri çevrim içi formdan çalışma sayfasına aktarılıyor.",
     "Robotik tercihi tabloda 'Robotik', 'robotik ' ve 'ROB.' biçimlerinde üç ayrı kategori olarak görünüyor.",
     "Düzenli veri toplama; açık alan adları, tutarlı biçimler, gerekli doğrulama ve eksik değerlerin anlamlı biçimde ele alınmasına dayanır."),
    ("tr-g06-bty-note-006",
     "Tablolama verisinden bulgu çıkarırken uygun hesaplama ve grafik seçilmeli; yorum yalnız gösterilen veri aralığıyla sınırlı tutulmalıdır.",
     "Aylara göre kitap sayısını karşılaştırmak için sütun grafiği ve toplam için uygun bir toplama formülü kullanmak amaca uygundur.",
     "Nisan değeri en yüksek olsa da yalnız dört aylık kayıt bulunması, yılın tamamı için kesin sonuç kurulamayacağını gösterir.",
     ["Grafikte en yüksek sütunu görmek, veri kapsamı ne olursa olsun gelecek yılın sonucunu kesinleştirir.", "Kategorileri karşılaştırmak için eksen ve ölçeği belirtilmemiş herhangi bir grafik yeterlidir.", "Ortalama hesaplamak yerine en büyük değeri bütün kayıtların ortak değeri saymak doğrudur."],
     "Kütüphane, ocak-nisan arasında ödünç verilen kitap sayılarını bir tabloda topluyor.",
     "Sütun grafiğinde nisan 420 ile en yüksek, şubat 260 ile en düşük değeri taşıyor; başka ay verisi bulunmuyor.",
     "Bulgular, doğru seçilmiş temsil ve hesaplamaya dayanmalı; kaydın kapsamadığı dönemlere taşan genellemelerden kaçınılmalıdır."),
    ("tr-g06-bty-note-007",
     "Ses düzenleme programları kaydı kesme, gürültüyü azaltma, seviyeyi ayarlama ve uygun biçimde dışa aktarma işlemlerini sağlar.",
     "Konuşma kaydının sessiz başlangıcını kesip ses düzeyini dengelerken özgün dosyanın bir kopyasını korumak güvenli bir iş akışıdır.",
     "Dalga biçimindeki aşırı yüksek tepelerin azaltılması ve konuşmanın anlaşılır kalması, seviye düzenlemesinin amaca ulaştığını gösterir.",
     ["Gürültüyü azaltmak için bütün konuşma bölümlerini silmek gerekir.", "Düzenlenen projeyi yalnız programın proje biçiminde saklamak her oynatıcıda dinlenmesini garanti eder.", "Başkasına ait müziği kaynak ve izin denetimi yapmadan eklemek etik bir düzenleme adımıdır."],
     "Öğrenciler okul radyosu için rüzgâr sesi bulunan bir röportaj kaydını düzenliyor.",
     "Ön izleme sonunda konuşma anlaşılır, ses tepeleri taşmıyor ve dışa aktarılan dosya hedef aygıtta açılıyor.",
     "İyi ses düzenleme, anlaşılabilirliği artırırken içeriği bozmaz; özgün kayıt, telif ve uygun çıktı biçimi korunur."),
    ("tr-g06-bty-note-008",
     "Ses kurgusunda amaç ve hedef kitle belirlendikten sonra bölümler anlamlı sıraya konur; geçişler ve ses seviyeleri bütünlük sağlayacak biçimde ayarlanır.",
     "Üç dakikalık podcast için giriş, ana anlatım ve kapanışı zaman çizelgesinde planlayıp müziği konuşmadan daha düşük seviyede tutmak uygundur.",
     "Kapanışın girişten önce duyulması ve müziğin konuşmayı örtmesi, kurgu sırası ile seviye dengesinin yeniden düzenlenmesi gerektiğini gösterir.",
     ["Ses parçalarını rastgele sıraya koymak dinleyicinin konuyu daha kolay izlemesini sağlar.", "Arka plan müziğini konuşmadan daha yüksek yapmak her durumda anlaşılırlığı artırır.", "Kurgu planı hazırlamak yalnız dosya adını seçmek demektir; süre ve geçişler önemli değildir."],
     "Bir ekip, müze gezisini anlatan kısa bir podcast için dört kayıt ve bir müzik parçası hazırlıyor.",
     "İlk denemede sonuç bölümü başta, tanıtım sonda kalıyor ve müzik anlatıcının sesini bastırıyor.",
     "Kurgu; içerik sırası, süre, geçiş ve ses dengesi kararlarının dinleme amacıyla birlikte planlanmasıdır."),
    ("tr-g06-bty-note-009",
     "Ses ürünü geliştirmede kayıt ortamı, örnekleme ve dosya biçimi hedef kullanıma göre seçilir; düzenleme sonrası farklı aygıtlarda test yapılır.",
     "İnternet için hazırlanan konuşmayı sessiz ortamda kaydedip yaygın bir biçimde dışa aktarmak ve kulaklıkla denetlemek uygun süreçtir.",
     "Bilgisayarda açılan dosyanın okul tabletinde açılmaması, içerikten önce çıktı biçimi ve uyumluluğun kontrol edilmesini gerektirir.",
     ["Kayıt bozuksa aynı dosyanın adını değiştirmek ses kalitesini kendiliğinden düzeltir.", "En büyük dosya boyutu her kullanım için en iyi ve en uyumlu ses anlamına gelir.", "Ürünü dışa aktarmadan yalnız proje dosyasını paylaşmak dinleyicinin her aygıtta açmasını sağlar."],
     "Bir öğrenci masal kaydını sınıf sitesinde telefon ve tabletlerden dinletmek istiyor.",
     "Ön izleme temizken ilk çıktı yalnız düzenleme yapılan bilgisayarda açılıyor; ikinci yaygın biçim iki aygıtta da oynuyor.",
     "Ses geliştirme, kayıt kalitesinin yanında çıktı biçimi, dosya boyutu, uyumluluk ve son kullanıcı testini de kapsar."),
    ("tr-g06-bty-note-010",
     "Video düzenleme programında ham görüntüler içe aktarılır, zaman çizelgesinde kesilip sıralanır, ses ve başlık eklenir, sonra hedefe uygun dışa aktarılır.",
     "Deney videosunda başarısız tekrarları kesip açıklama başlıklarını ilgili görüntünün üzerine yerleştirmek anlatımı güçlendirir.",
     "Başlık deney görüntüsünden sonra geliyorsa izleyici adımı zamanında anlayamaz; zaman çizelgesindeki yerleşim düzeltilmelidir.",
     ["Ham görüntüyü hiç izlememek, gereksiz bölümlerin yayında kalmasını önler.", "Geçiş ve efekt sayısını artırmak içeriğin doğruluğunu kendiliğinden yükseltir.", "Dışa aktarma ayarını hedef ekranı düşünmeden seçmek her aygıtta aynı sonucu garanti eder."],
     "Fen kulübü, su filtresi yapımını gösteren iki dakikalık öğretici video hazırlıyor.",
     "İlk kurguda uzun bekleme anları kalıyor ve 'çakıl ekle' başlığı ilgili görüntü bittikten sonra görünüyor.",
     "Video düzenleme kararları gösterişe değil, anlatım amacı, zamanlama, anlaşılabilirlik ve hedef aygıt gereksinimine hizmet etmelidir."),
    ("tr-g06-bty-note-011",
     "Video kurgusu, planlanan mesajı kurmak için çekimleri seçme, sıralama ve sürelerini ayarlama işlemidir; süreklilik izleyicinin olayı izlemesini sağlar.",
     "Bir fidan dikme videosunda çukur açma, fidanı yerleştirme ve sulama çekimlerini işlem sırasına göre dizmek doğru kurgudur.",
     "Sulama görüntüsü çukur açmadan önce geliyorsa olay örgüsündeki neden-sonuç sırası bozulmuştur.",
     ["Çekimleri dosya adına göre rastgele sıralamak olayın anlaşılmasını kolaylaştırır.", "Aynı görüntüyü amaç olmadan sürekli yinelemek videonun iletisini güçlendirir.", "Kurgu planında hedef kitleyi ve süreyi düşünmek gereksizdir; yalnız efekt seçimi önemlidir."],
     "Çevre kulübü, bahçeye fidan dikme aşamalarını farklı açılardan çekiyor.",
     "Taslak videoda sulama sahnesi önce, çukur açma sahnesi sonra geliyor ve izleyiciler sırayı karıştırıyor.",
     "Kurgu sırası, anlatılan sürecin mantığı ve hedef kitlenin izlemesi gereken bilgi akışıyla uyumlu olmalıdır."),
    ("tr-g06-bty-note-012",
     "Video ürünü planlama, çekim, kurgu, telif denetimi, uygun çözünürlük ve codec ile dışa aktarma ve son test aşamalarından geçer.",
     "Okul ekranı için videoyu hedef çözünürlükte dışa aktarıp görüntü-ses eşleşmesini son dosyada denetlemek gerekir.",
     "Yüksek çözünürlüklü dosya takılarak oynarken daha dengeli ayar akıcı çalışıyorsa çıktı seçimi hedef donanıma göre yapılmalıdır.",
     ["Codec yalnız videonun dosya adıdır ve oynatma uyumluluğunu etkilemez.", "En yüksek çözünürlük her ekranda en akıcı oynatmayı koşulsuz garanti eder.", "Dışa aktarılan dosyayı izlemeye gerek yoktur; proje ön izlemesi son ürünle her zaman aynıdır."],
     "Tarih kulübü videosu sınıftaki eski bir etkileşimli tahtada gösterilecek.",
     "İlk çıktı yüksek boyutu nedeniyle takılıyor; hedef ayara göre dışa aktarılan ikinci dosya akıcı ve sesi eş zamanlı oynatıyor.",
     "Son ürün kalitesi yalnız ham çekime değil, hedef ortamla uyumlu teknik ayarlar ve dışa aktarım sonrası kontrole bağlıdır."),
    ("tr-g06-bty-note-013",
     "İnternet amaca uygun kullanılırken güvenilir kaynak seçilir, kişisel bilgiler korunur, süre yönetilir ve çevrim içi davranışlarda etik kurallara uyulur.",
     "Ödev araştırmasında kurum ve uzman kaynaklarını karşılaştırıp kaynakçayı yazmak, bilinmeyen bağlantıları açmamak doğru yaklaşımdır.",
     "Aynı iddia yalnız reklâm içeren anonim sayfada geçiyor, resmî kaynaklarda doğrulanmıyorsa bilgi güvenilir kabul edilmemelidir.",
     ["Arama sonucunda ilk sırada görünen her sayfa doğrulanmış bilgi içerir.", "Kişisel adresi herkese açık paylaşmak eğitim amaçlı internet kullanımının zorunlu parçasıdır.", "Kaynak göstermeden metni aynen kopyalamak hızlı olduğu için etik kabul edilir."],
     "Bir öğrenci enerji tasarrufu ödevi için üç internet sayfası buluyor ve bir sayfa ev adresini isteyen ödüllü anket açıyor.",
     "İki sayfada yazar ve kurum bilgisi bulunuyor; anonim sayfa kaynak göstermiyor ve kişisel bilgi istiyor.",
     "Amaçlı internet kullanımı, bilgi doğrulama ile mahremiyet ve telif sorumluluğunu aynı anda gözetir."),
    ("tr-g06-bty-note-014",
     "İletişim teknolojileri kapsama alanı, bağlantı ortamı, hız, enerji tüketimi ve kullanım amacına göre sınıflandırılır.",
     "Yakındaki iki sensörün az veri göndermesi için kısa menzilli düşük enerjili bağlantı seçmek gereksinime uygundur.",
     "Bağlantı yalnız aynı odada çalışıp uzaklaşınca kesiliyorsa kısa menzilli bir iletişim teknolojisi kullanıldığı çıkarılabilir.",
     ["Bluetooth, Wi-Fi ve mobil ağ aynı kapsama ve kullanım özelliklerine sahiptir.", "Kablolu bağlantılar her zaman hareketli aygıtlar için en uygun çözümdür.", "İletişim aracını seçerken mesafe, veri miktarı ve güvenlik gereksinimi dikkate alınmaz."],
     "Müze rozetleri ziyaretçinin telefonuna yalnız sergi salonundayken küçük bilgi paketleri gönderiyor.",
     "Telefon salondan çıkınca bağlantı sona eriyor; aktarım az enerji kullanıyor ve kısa mesafede gerçekleşiyor.",
     "Teknoloji sınıflandırması yalnız adına değil, kablolu-kablosuz oluşuna, kapsamasına ve taşıdığı veri gereksinimine dayanır."),
    ("tr-g06-bty-note-015",
     "Bilgisayar ağı, cihazların belirli kurallarla veri ve kaynak paylaşmasını sağlar; güvenli bağlantıda yetkilendirme ve şifreleme önemlidir.",
     "Okul yazıcısını yalnız yetkili hesaplara açıp kablosuz ağı güçlü parola ve güncel şifreleme ile korumak uygun yapılandırmadır.",
     "Ağa bağlanan herkes yazdırabiliyorsa ve yönetim ekranı varsayılan paroladaysa kaynak paylaşımı erişim denetiminden yoksundur.",
     ["Ağa bağlanan her kullanıcı bütün dosya ve aygıtlara sınırsız erişmelidir.", "Varsayılan yönetici parolasını değiştirmemek ağı daha kolay yönetildiği için güvenli yapar.", "Ağ güvenliği yalnız kablonun uzunluğuna bağlıdır; kullanıcı izinleri etkili değildir."],
     "Bir okul laboratuvarında bilgisayarlar ortak yazıcıyı ve dosya klasörünü ağ üzerinden kullanıyor.",
     "Misafir hesabı yönetim klasörünü açabiliyor ve yönlendirici hâlâ üretici parolasıyla çalışıyor.",
     "Kaynak paylaşımı ağın yararıdır; ancak en az yetki, güçlü kimlik doğrulama ve güncel koruma olmadan paylaşım güvenli değildir."),
    ("tr-g06-bty-note-016",
     "Siber güvenlik tek bir araç değil; güçlü benzersiz parola, çok adımlı doğrulama, güncelleme, yedekleme ve dikkatli kullanıcı davranışının birlikte yönetimidir.",
     "Hesap için benzersiz parola ve iki adımlı doğrulama kullanıp kurtarma kodlarını güvenli yerde saklamak riski azaltır.",
     "Güncel olmayan aygıtta aynı parola birçok hesapta kullanılıyorsa virüs programı bulunsa bile savunma katmanları yetersizdir.",
     ["Aynı güçlü parolayı bütün hesaplarda kullanmak parola yönetiminin en güvenli yoludur.", "Güncellemeleri sürekli ertelemek bilinen güvenlik açıklarını kapatır.", "Yedekleme yalnız dosya silindikten sonra yapılır; önceden planlanmasına gerek yoktur."],
     "Bir öğrenci tüm hesaplarında aynı parolayı kullanıyor, telefon güncellemelerini erteliyor ve yalnız antivirüse güveniyor.",
     "Bir oyun sitesindeki parola sızıntısından sonra aynı parola kullanılan e-posta hesabına da giriş denemesi yapılıyor.",
     "Katmanlı güvenlikte bir önlem başarısız olsa bile diğer önlemler hesabı ve veriyi korumaya devam eder."),
    ("tr-g06-bty-note-017",
     "Telif hakkı eser sahibinin haklarını korur; bir eseri kullanmak için lisans ve izin koşulları incelenmeli, gerektiğinde kaynak gösterilmelidir.",
     "Sunumda kullanılacak fotoğrafın lisansını kontrol edip izin verilen biçimde eser sahibini belirtmek etik kullanımdır.",
     "Fotoğraf internette ücretsiz görüntülense bile yeniden kullanım izni belirtilmiyorsa kopyalanabileceği sonucu çıkarılamaz.",
     ["İnternette görülebilen bütün eserler telifsizdir ve istenen biçimde değiştirilebilir.", "Eser sahibinin adını silmek içeriği kendi çalışmamız hâline getirir.", "Kaynak yazmak, lisansın yasakladığı ticari kullanımı kendiliğinden serbest bırakır."],
     "Bir ekip, okul afişi için bir fotoğraf sitesinde beğendiği görseli indirmek istiyor.",
     "Sayfa fotoğrafçının adını gösteriyor fakat yeniden kullanım lisansı veya indirme izni belirtmiyor.",
     "Erişilebilir olmak kullanım hakkı vermekle aynı değildir; lisans koşulu, izin ve atıf gereği ayrı ayrı doğrulanır."),
    ("tr-g06-bty-note-018",
     "Kimlik avı ve zararlı içeriklerde gönderen, adres, acil işlem baskısı ve bağlantı hedefi kontrol edilmeli; şüpheli ileti yetişkine veya kuruma bildirilmelidir.",
     "Kargo mesajındaki kısaltılmış bağlantıya dokunmadan resmî uygulamadan gönderiyi kontrol etmek güvenli davranıştır.",
     "Mesaj gerçek kurum adını kullansa da alan adı farklı ve parola istiyorsa kimlik avı riski yüksektir.",
     ["Mesajda kurum logosu bulunması bağlantının kesinlikle güvenli olduğunu kanıtlar.", "Acil uyarı veren bağlantıya hızlıca parola girmek hesabın kapanmasını önler.", "Siber zorbalık içeren mesajları kanıt saklamadan karşı tarafa yaymak en doğru çözümdür."],
     "Bir telefona 'Paketiniz bekliyor, on dakika içinde giriş yapın' yazılı bir mesaj geliyor.",
     "Bağlantının alan adı kargo şirketinden farklı ve açılan sayfa e-posta parolası istiyor.",
     "Güvenli kullanıcı acele baskısına kapılmaz; bağlantı yerine resmî kanalı kullanır, bilgi paylaşmaz ve olayı bildirir."),
    ("tr-g06-bty-note-019",
     "Yazılım ve içerik lisansı; çalıştırma, kopyalama, değiştirme ve paylaşma haklarının hangilerinin verildiğini belirler.",
     "Bir görseli değiştirmeden önce lisansın uyarlamaya izin verip vermediğini ve atıf koşulunu okumak gerekir.",
     "Kaynak kodunun görülebilmesi, lisans değiştirme ve dağıtma hakkı vermiyorsa ürünün otomatik olarak özgür yazılım sayılamayacağını gösterir.",
     ["Ücretsiz indirilen her yazılımın kaynak kodu değiştirilebilir ve yeniden satılabilir.", "Tescilli yazılımın lisans sözleşmesi kullanıcı haklarını belirlemez.", "Kamu malı ile atıf gerektiren açık lisans tamamen aynı kullanım koşullarına sahiptir."],
     "Kod kulübü, internette kaynak kodu görünen bir aracı değiştirip kendi sitesinde yayımlamak istiyor.",
     "Depoda kod var; ancak lisans dosyası değiştirme ve yeniden dağıtma izni vermiyor.",
     "Lisans türü fiyatla veya dosyaya erişimle değil, hak sahibinin açıkça verdiği kullanım izinleriyle belirlenir."),
    ("tr-g06-bty-note-020",
     "Yapay zekâ girdileri amaca uygun, yeterli, doğru ve temsil edici olmalı; kişisel veri toplamada izin ve veri azaltma ilkesi gözetilmelidir.",
     "Bitki modelini farklı ışık ve açılardan dengeli örneklerle eğitip kişi görüntülerini gereksiz yere toplamamak uygun veri tasarımıdır.",
     "Yalnız aydınlık ortam fotoğraflarıyla eğitilen model gölgede hata yapıyorsa eğitim verisi kullanım koşullarını temsil etmiyor demektir.",
     ["Daha çok veri toplamak, verinin hatalı veya izinsiz olmasına bakılmadan modeli her zaman iyileştirir.", "Bir sınıfı hiç örneklemeyen veri kümesi bütün sınıfları eşit öğrenmiş sayılır.", "Kişisel veriler yapay zekâ girdisi olunca izin ve güvenlik kuralları uygulanmaz."],
     "Öğrenciler yaprak türlerini ayıran basit bir model için okul bahçesinde fotoğraf topluyor.",
     "Verilerin çoğu tek türden ve güneşli havada çekilmiş; gölgeli görüntülerde doğruluk belirgin biçimde düşüyor.",
     "Model çıktısının sınırları girdi verisinin kapsamı ve kalitesiyle ilişkilidir; etik toplama da teknik başarı kadar gereklidir."),
    ("tr-g06-bty-note-021",
     "Yapay zekâ aracı çıktısı kesin doğru kabul edilmez; amaç açık yazılır, kişisel veri paylaşılmaz ve sonuç güvenilir kaynaklarla doğrulanır.",
     "Özetleme aracına kimlik bilgisi içermeyen metin verip çıkan bilgileri asıl kaynakla karşılaştırmak sorumlu kullanımdır.",
     "Araç aynı soruya çelişkili iki tarih veriyorsa akıcı yazması güvenilirliğe yetmez ve kaynak doğrulaması gerekir.",
     ["Yapay zekâ kendinden emin bir cümle kurduğunda kaynak göstermese de sonuç kesin doğrudur.", "Daha ayrıntılı yanıt almak için arkadaşların özel bilgilerini araca yüklemek uygundur.", "Üretilen metni kontrol etmeden kendi çalışması gibi teslim etmek etik kullanım örneğidir."],
     "Bir öğrenci tarih ödevindeki uzun metni yapay zekâ aracıyla özetliyor.",
     "Araç aynı olay için iki farklı tarih yazıyor ve hiçbir kaynak belirtmiyor.",
     "Yapay zekâ yardımcı araçtır; kullanıcı mahremiyet, doğruluk, telif ve kendi öğrenme sorumluluğunu devredemez."),
    ("tr-g06-bty-note-022",
     "Basit yapay zekâ modeli için problem tanımlanır, etiketli veri hazırlanır, eğitim yapılır ve daha önce görmediği test verisiyle başarı ölçülür.",
     "Kedi-köpek modelinde eğitimden ayrılan dengeli fotoğrafları test için kullanmak gerçek genelleme başarısını ölçer.",
     "Eğitim görüntülerinde çok yüksek, yeni görüntülerde düşük başarı görülmesi modelin örnekleri ezberlemiş olabileceğini gösterir.",
     ["Modeli eğittiğimiz aynı örneklerle test etmek yeni durum başarısını güvenilir biçimde ölçer.", "Yanlış etiketleri artırmak modelin sınıfları daha iyi ayırmasını sağlar.", "Yalnız doğruluk yüzdesine bakmak, hangi sınıfta hata yapıldığını incelemeyi gereksiz kılar."],
     "Bir grup iki hayvanı ayıran görüntü modeli kuruyor ve bütün fotoğrafları eğitimde kullanıyor.",
     "Model eğitim fotoğraflarında yüzde 99 başarılı; yeni çekimlerde özellikle karanlık görüntüleri sıkça karıştırıyor.",
     "Eğitim ve test verisinin ayrılması, veri dengesi ve hata örneklerinin incelenmesi modelin gerçekten öğrenip öğrenmediğini gösterir."),
    ("tr-g06-bty-note-023",
     "Blok tabanlı programlamada olaylar kodu başlatır, döngüler yinelemeyi, koşullar karar vermeyi, değişkenler ise değişen bilgiyi saklamayı sağlar.",
     "Karakter her tıklandığında puanı bir artırmak için tıklama olayı altında puan değişkenini artıran blok kullanmak uygundur.",
     "Puan ekranda hep sıfır kalıyorsa hareket bloğundan önce değişkenin artırılıp artırılmadığı ve olay bağlantısı kontrol edilmelidir.",
     ["Bir değişken yalnız karakterin rengini değiştirir; sayı veya metin saklayamaz.", "Koşul bloğu içindeki komutlar koşula bakılmadan her zaman çalışır.", "Başlatma olayı bulunmayan blok yığını proje açılır açılmaz kendiliğinden yürütülür."],
     "Bir oyunda yıldız tıklanınca kayboluyor fakat puan göstergesi değişmiyor.",
     "Kodda tıklama olayı ve gizlenme bloğu var; puan değişkenini artıran blok bulunmuyor.",
     "Bileşenin görevi ile istenen davranış eşleştirilerek eksik olay, veri veya kontrol bloğu belirlenir."),
    ("tr-g06-bty-note-024",
     "Yazılım geliştirme; problemi anlama, gereksinimleri belirleme, algoritma tasarlama, kodlama, test etme ve hatayı düzeltme döngüsüdür.",
     "Labirent oyununda önce başarı ölçütlerini yazıp küçük adımlarla kodlamak ve her adımı örneklerle test etmek süreci yönetir.",
     "Karakter yalnız sağ kenarda takılıyorsa bu sınır durumunu yeniden üreten test, hatanın ilgili koşulda aranmasını sağlar.",
     ["Problemi tanımlamadan doğrudan rastgele blok eklemek geliştirme süresini her zaman kısaltır.", "Bir program ilk denemede açılıyorsa farklı girdilerle test edilmesine gerek yoktur.", "Hata bulununca çalışan bütün kodu silmek, hatanın kaynağını ayırmaktan daha güvenlidir."],
     "Bir ekip, ok tuşlarıyla hareket eden karakteri hedefe ulaştıran oyun geliştiriyor.",
     "Normal konumlarda hareket doğru; karakter sağ sınıra geldiğinde tuşa basınca ekran dışında kalıyor.",
     "Süreç yönetimi, ölçülebilir gereksinim ve sınır durumlarını içeren testlerle hatayı küçük bir kod bölümüne kadar daraltır."),
    ("tr-g06-bty-note-025",
     "Yapay zekâ destekli blok projesinde amaç, veri/algılayıcı girdisi, model çıktısı ve blokların bu çıktıya vereceği tepki birlikte tasarlanır ve test edilir.",
     "Geri dönüşüm oyununda görüntü modelinin güven puanı yeterliyse ilgili kutu animasyonunu çalıştırmak, düşükse kullanıcıdan yeniden görüntü istemek uygundur.",
     "Model düşük ışıkta plastik şişeyi karıştırıyorsa yalnız blok sırasını değiştirmek yetmez; veri ve güven eşiği de incelenmelidir.",
     ["Yapay zekâ modeli projeye eklenince olay ve koşul bloklarına ihtiyaç kalmaz.", "Modelin ilk tahminini güven puanına bakmadan her durumda doğru kabul etmek gerekir.", "Kullanıcı görüntülerini izin almadan kalıcı saklamak ürünün teknik başarısı için zorunludur."],
     "Öğrenciler kameradaki atığı tanıyıp doğru geri dönüşüm kutusunu gösteren blok tabanlı oyun yapıyor.",
     "Aydınlıkta doğru çalışan model düşük ışıkta güven puanı düşmesine rağmen oyun kesin bir kutu gösteriyor.",
     "Çalışan ürün, model sınırlarını koşul bloklarıyla yönetir; veri etiği, kullanıcı uyarısı ve farklı koşullarda test tasarımın parçasıdır."),
]


MODE_SEQUENCE = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
LEVEL_SEQUENCE = (
    [1] * 15 + [2] * 10
    + [1] * 5 + [2] * 15 + [3] * 15
    + [3] * 10 + [4] * 10 + [5] * 5
    + [3] * 5 + [4] * 10
)
MODE_LABELS = {
    "comprehension": "kavramı ayırt etme",
    "application": "bilgiyi yeni durumda uygulama",
    "analysis": "durum ve kanıtı birlikte çözümleme",
    "error-analysis": "somut yanılgıyı gerekçeyle düzeltme",
}


def read_notes_only() -> dict[str, dict[str, Any]]:
    notes: dict[str, dict[str, Any]] = {}
    for line in SOURCE.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("type") == "note":
            notes[str(row.get("id"))] = row
    return notes


def rotate(correct: str, wrongs: list[str], position: int) -> list[str]:
    result = list(wrongs)
    result.insert(position, correct)
    return result


def make_table(qid: str, scenario: str, evidence: str, labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.alt"
    labels[h1] = "İnceleme öğesi"
    labels[h2] = "Kayıt"
    labels[alt] = "Bir bilişim uygulamasının durumu ve gözlenen sonucu iki satırda gösteren tablo; doğru seçenek belirtilmemiştir."
    return {
        "kind": "table",
        "headerKeys": [h1, h2],
        "rows": [[{"v": "Durum"}, {"v": scenario}], [{"v": "Gözlem"}, {"v": evidence}]],
        "altTextKey": alt,
    }


def make_question(number: int, entry: tuple[Any, ...], mode: str, level: int,
                  notes: dict[str, dict[str, Any]], labels: dict[str, str]) -> dict[str, Any]:
    note_id, principle, application, inference, wrongs, scenario, evidence, rationale = entry
    note = notes[note_id]
    objective = str((note.get("objectives") or [note.get("objective")])[0])
    qid = f"tr-g06-bank-bty-b01-q{number:03d}"
    correct_position = (number - 1) % 4
    topic_phrase = str(note["title"]).replace("İ", "i").replace("I", "ı").lower()
    if mode == "comprehension":
        variant = (number - 1) % 5
        template_id = f"g6-bty-comprehension-v{variant + 1}"
        correct = principle
        stems = (
            f"{scenario} Bu örneği {topic_phrase} konusundaki temel işlevle açıklayan ifade hangisidir?",
            f"{scenario} Olayı doğru sınıflandırmak için {topic_phrase} kapsamında hangi ayrım kullanılmalıdır?",
            f"{scenario} Bu durumla ilgili hangi iddia, kavramın geçerlilik sınırını aşmadan kurulmuştur?",
            f"{scenario} Gözlenen bilişim işlevinin yanlış bir teknolojiyle karıştırılmasını hangi bilgi önler?",
            f"{scenario} Durumun araç, veri ve amaç ilişkisini doğru kuran temel ilke hangisidir?",
        )
        stem = stems[variant]
        explanation = f"{rationale} Bu nedenle örnekteki temel işlev doğru ifadede sınırlarıyla açıklanmıştır."
        figure = None
    elif mode == "application":
        second_application = 51 <= number <= 60
        variant = (number - 1) % 5
        phase = "apply-test" if second_application else "apply"
        template_id = f"g6-bty-{phase}-v{variant + 1}"
        if second_application:
            correct = f"{application} Uygulamanın başarısı, beklenen sonuçla gözlem kaydı karşılaştırılarak sınanmalıdır."
            stems = (
                f"{scenario} İlk denemede “{evidence}” kaydediliyor. Ekip {topic_phrase} için uygulama ve doğrulama adımını birlikte seçecek. Hangi plan uygundur?",
                f"{scenario} Pilot uygulamanın gözlemi şöyledir: {evidence} Bu aşamada {topic_phrase} ölçütlerine göre hem eylem hem başarı kontrolü içeren karar hangisidir?",
                f"{scenario} Ekip bir çözüm uygulayıp şu kaydı alıyor: {evidence} Kararın işe yaradığını da sınayan seçenek hangisidir?",
                f"{scenario} Tasarım günlüğünde “{evidence}” yazıyor. {topic_phrase} bilgisini uygulama-test döngüsüne dönüştüren plan hangisidir?",
                f"{scenario} Deneme sonucu “{evidence}” olarak raporlanıyor. Eylemi seçen ve beklenen sonuçla karşılaştıran yaklaşım hangisidir?",
            )
            stem = stems[variant]
            explanation = (
                f"{rationale} İkinci uygulama, yalnız işlemi seçmekle kalmaz; beklenen sonuç ile gerçek gözlemi "
                "karşılaştırarak kararın işe yarayıp yaramadığını da denetler."
            )
        else:
            correct = application
            stems = (
                f"{scenario} Ekip ürünü amacına uygun geliştirecek; {topic_phrase} bilgisini doğrudan uygulayan karar hangisidir?",
                f"{scenario} Kullanıcı gereksinimi ve güvenlik birlikte gözetilecektir. İlk uygulanabilir adım hangisidir?",
                f"{scenario} Tasarım ekibi dört çözüm önerisini değerlendiriyor. Durumdaki gereksinime en uygun öneri hangisidir?",
                f"{scenario} Çalışma planına {topic_phrase} için doğru bir işlem eklenecektir. Hangi işlem seçilmelidir?",
                f"{scenario} Ekip, araç seçimini amaç ve kanıtla eşleştirmek istiyor. Hangi karar bu eşleşmeyi kurar?",
            )
            stem = stems[variant]
            explanation = f"{rationale} Bu uygulama kararı, senaryodaki gereksinimi doğrudan karşılar ve doğrulanabilir bir adım önerir."
        figure = None
    elif mode == "analysis":
        variant = (number - 1) % 5
        template_id = f"g6-bty-analysis-v{variant + 1}"
        correct = inference
        stems = (
            f"Aşağıdaki tabloda {topic_phrase} kapsamında bir durum ile gözlem eşleştiriliyor. İki kayıt birlikte değerlendirildiğinde hangi çıkarıma ulaşılır?",
            f"Aşağıdaki tablodaki durum ve gözlem, {topic_phrase} ölçütleriyle incelenecektir. Hangi yorum kanıtın sınırını aşmaz?",
            f"Aşağıdaki tabloda bir inceleme ekibinin iki kaydı yer alıyor. {topic_phrase} açısından hangi sonuç doğrudan gözlemle desteklenir?",
            f"Aşağıdaki tabloda iki satırlı kayıt verilmiştir. {topic_phrase} konusunda neden ile sonucu doğru ayıran değerlendirme hangisidir?",
            f"Aşağıdaki tabloda sunulan kanıta dayanarak kısa bir rapor yazılacaktır. {topic_phrase} için hangi rapor cümlesi kanıt sınırında kalır?",
        )
        stem = stems[variant]
        explanation = f"{rationale} Tablodaki durum ile gözlem arasındaki bağ, doğru çıkarımın kapsamını belirler."
        figure = make_table(qid, scenario, evidence, labels)
    else:
        variant = (number - 1) % 3
        template_id = f"g6-bty-error-analysis-v{variant + 1}"
        mistaken = wrongs[(number - 1) % 3]
        correct = f"Öğrencinin çıkarımı düzeltilmelidir: {principle}"
        stems = (
            f"Bir öğrenci {topic_phrase} konusunu tartışırken “{mistaken}” diyor. Bu hatalı yorumu konu anlatımına dayanarak düzelten seçenek hangisidir?",
            f"Bir öğrenci “{mistaken}” kararını savunuyor. {topic_phrase} ölçütlerinden hangisi kullanılarak bu yanılgı doğru biçimde giderilir?",
            f"Bir öğrencinin çalışma kâğıdında hatalı sonuç “{mistaken}” biçiminde yazılmıştır. Hatanın kaynağını düzelten değerlendirme hangisidir?",
        )
        stem = stems[variant]
        explanation = f"{rationale} Öğrencinin yanılgısı ölçütlerden birini yok saydığı için doğru düzeltme temel ilkeyi açıkça geri kurar."
        figure = None

    mode_wrongs = list(wrongs)
    choices = rotate(correct, mode_wrongs, correct_position)
    reason_by_choice = {
        correct: f"Doğru gerekçe: {rationale} Seçenek, verilen bağlam için gerekli ölçütleri birlikte kullanır.",
        mode_wrongs[0]: f"Eksik ölçüt yanılgısı: {wrongs[0]} ifadesi karar için gerekli veri, işlev veya güvenlik koşulunu dışarıda bırakır.",
        mode_wrongs[1]: f"Aşırı genelleme yanılgısı: {wrongs[1]} ifadesi tek bir özelliği bütün durumlara taşıyarak kanıt sınırını aşar.",
        mode_wrongs[2]: f"Amaç-araç karışıklığı: {wrongs[2]} ifadesi kullanılan aracı, çözülmesi gereken gereksinim veya süreçle yanlış eşleştirir.",
    }
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "Durum ve gözlem yalnız tabloda verildiği için çıkarım görsel kanıta bağlıdır.",
        "acceptableKinds": ["table"], "evidenceDimensions": ["durum", "gözlem"],
    } if figure else {
        "level": "none", "role": "none",
        "rationale": "Çözüm için gereken bağlam ve kavramlar soru metninde eksiksiz verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": number,
        "subject": "Bilişim Teknolojileri ve Yazılım", "grade": 6,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — {MODE_LABELS[mode]}",
        "objective": objective, "objectiveId": objective,
        "noteId": note_id, "noteKey": note_id,
        "question": stem, "choices": choices, "correct": correct_position,
        "correctIndex": correct_position, "correctOption": choices[correct_position],
        "distractorWhy": [reason_by_choice[choice] for choice in choices],
        "explanation": explanation, "level": level,
        "difficultyReason": (
            f"Düzey {level}; {MODE_LABELS[mode]} sırasında senaryodaki {note['title']} ölçütlerini "
            "ayırt edip gerekçeli bir karar vermeyi gerektirir."
        ),
        "questionType": mode, "familyId": f"tr-g06-bank-bty-family-{number:03d}",
        "authoringTemplateId": template_id,
        "objectiveSource": note.get("objectiveSource"),
        "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [],
        "visualRequirement": "required" if figure else "none",
        "visualNeed": visual_need, "figure": figure,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    notes = read_notes_only()
    missing = sorted({entry[0] for entry in KNOWLEDGE} - set(notes))
    if missing or len(KNOWLEDGE) != 25:
        raise RuntimeError(f"knowledge/note coverage error: missing={missing} count={len(KNOWLEDGE)}")
    labels: dict[str, str] = {}
    rows = [
        make_question(number, KNOWLEDGE[(number - 1) % 25], MODE_SEQUENCE[number - 1],
                      LEVEL_SEQUENCE[number - 1], notes, labels)
        for number in range(1, 101)
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n",
        encoding="utf-8", newline="\n",
    )
    LABELS_OUTPUT.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({"questions": len(rows), "labels": len(labels), "sourceQuestionReads": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
