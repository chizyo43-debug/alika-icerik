#!/usr/bin/env python3
"""Append Grade 6 ICT bank batch 02: 100 new note-grounded questions.

The case library is independent from batch 01 and reads only lesson-note
records.  It never loads lesson questions.
"""
from __future__ import annotations

import json
from typing import Any

from author_grade6_bilisim_batch01 import (
    LABELS_OUTPUT, OUTPUT, read_notes_only, rotate,
)


# note id, new scenario, observable evidence, contextual concept, action,
# inference, three misconceptions, explanation
CASES = [
    ("tr-g06-bty-note-001",
     "Bir spor salonundaki bileklikler nabız ölçümünü yakındaki istasyona gönderiyor; istasyon antrenman yoğunluğu için uyarı üretiyor.",
     "Bileklik çevrim dışıyken yalnız ölçüm saklıyor, ağa bağlanınca kayıtları aktarıyor ve ortak ekranda güncelliyor.",
     "Bu sistemde algılayıcı verisinin ağ üzerinden başka bir aygıta aktarılması nesnelerin interneti işlevine örnektir.",
     "Bileklik verisini yalnız izin verilen hesapla paylaşmak ve uyarıyı ölçüm sınırlarına göre üretmek amaca uygun tasarımdır.",
     "Aktarımın bağlantı kurulunca başlaması, bileklik ile istasyonun veri alışverişi yapan bağlı cihazlar olduğunu destekler.",
     ["Nabız sayısının ekranda görünmesi, görüntünün gerçek ortama bindirildiğini ve sistemin artırılmış gerçeklik olduğunu kanıtlar.", "Ağ bağlantısı kesilince veri saklayan aygıt bilişim teknolojisi sayılamaz.", "Bir uyarı üreten bütün sistemler girdiye bakmadan insan bilincine sahip yapay zekâ kabul edilir."],
     "Bağlı teknoloji; algılama, veri aktarımı ve işleme zinciriyle tanınır, yalnız ekranın görünüşü veya ürün adıyla sınıflandırılmaz."),
    ("tr-g06-bty-note-002",
     "İlçe kütüphanesi, kitapları raflar arasında taşıyacak robotları gelecek yıl kullanmayı düşünüyor.",
     "Denemede çalışanların ağır yükü azalıyor; ancak dar koridorda çocukları algılama ve iş kaybı kaygıları raporlanıyor.",
     "Geleceğe dönük bir bilişim çözümü, verim artışıyla birlikte güvenlik ve çalışanların değişen görevleri açısından değerlendirilmelidir.",
     "Robotları önce sınırlı alanda güvenlik testine almak ve çalışanlara yeni görevler için eğitim vermek dengeli geçiş sağlar.",
     "Yük taşıma süresinin azalması tek başına yeterli değildir; çocuk algılama kusuru çözülmeden yaygın kullanım güvenli sayılamaz.",
     ["Robot bir işi hızlandırıyorsa güvenlik denemesine ihtiyaç kalmaz.", "Yeni teknoloji geldiğinde çalışanların bilgi ve deneyinin hiçbir değeri kalmaz.", "Gelecek hakkında yapılan ilk tahmin kesin gerçekleşeceği için farklı olasılıklar incelenmez."],
     "Teknolojik gelecek senaryoları yarar, risk, erişilebilirlik ve yeni beceri gereksinimlerini birlikte ele alan kanıta dayalı kararlardır."),
    ("tr-g06-bty-note-003",
     "Bir öğretmen sınav puanlarını B2:B21 aralığına yazıp sınıf ortalamasını hesaplamak istiyor.",
     "B22 hücresindeki =ORTALAMA(B2:B21) formülü bir puan değiştirildiğinde yeni ortalamayı otomatik gösteriyor.",
     "Aralık kullanan formül, belirtilen hücrelerdeki sayısal değerleri hesaplamaya katar ve girdiler değiştiğinde sonucu yeniler.",
     "Ortalama hücresine =ORTALAMA(B2:B21) yazıp puan sütununu sayısal biçimde tutmak tekrar hesaplamayı önler.",
     "B7 değişince yalnız sonuç hücresinin yenilenmesi, ortalamanın sabit metin değil hücre başvurulu formül olduğunu gösterir.",
     ["ORTALAMA işlevi yalnız en büyük puanı bulur ve diğer hücreleri yok sayar.", "Formülün başındaki eşittir işaretini silmek hesaplamanın daha hızlı yenilenmesini sağlar.", "B2:B21 gösterimi iki hücreyi böler; aradaki hücreleri kapsamaz."],
     "Tablolama formüllerinde işlevin amacı, aralığın kapsamı ve veri türü doğru kurulursa sonuç değişen kayıtlara bağlı olarak güncellenir."),
    ("tr-g06-bty-note-004",
     "Bir çalışma sayfasında bazı tarihlerin yerinde #### işaretleri görülüyor, diğer hesaplamalar doğru çalışıyor.",
     "Sütun genişletildiğinde tarihler eksiksiz görünüyor ve hücre değerleri değişmiyor.",
     "#### görünümü bu durumda verinin silindiğini değil, sütunun biçimlendirilmiş değeri gösterecek kadar geniş olmadığını belirtir.",
     "Önce sütunu genişletip değerin görünmesini denemek, veriyi silmeden sorunun görüntüleme kaynaklı olup olmadığını sınar.",
     "Genişlik değişince değerlerin ortaya çıkması, sorunun formülde değil hücre görünümünde olduğunu kanıtlar.",
     ["#### işareti bulunan her hücrede bilgisayar virüsü vardır.", "İşaretleri düzeltmenin tek yolu çalışma kitabındaki bütün tarihleri silmektir.", "Sütun genişliği yalnız hücre rengini etkiler; görüntülenen değeri etkilemez."],
     "Hata çözümünde belirti doğru yorumlanır; veri, formül ve görünüm olasılıkları küçük denemelerle birbirinden ayrılır."),
    ("tr-g06-bty-note-005",
     "Gezi kayıtlarında doğum tarihleri 04/05/2014, 5 Mayıs 2014 ve 2014-05-05 gibi farklı biçimlerde tutuluyor.",
     "Tarihler tek biçime dönüştürülünce yaş grubuna göre sıralama doğru çalışıyor; iki eksik tarih boş bırakılıp açıklanıyor.",
     "Aynı veri türünün farklı gösterimleri analizden önce standartlaştırılmalı, eksik değerler uydurma bilgiyle doldurulmamalıdır.",
     "Tarih sütununa veri doğrulama ve ortak tarih biçimi uygulayıp eksik kayıtları kaynağından doğrulamak doğru düzenlemedir.",
     "Sıralamanın standartlaştırmadan sonra düzelmesi, önceki hücrelerin bir bölümünün tarih yerine metin olarak algılandığını gösterir.",
     ["Eksik doğum tarihlerini herkes için aynı rastgele günle doldurmak veri kalitesini yükseltir.", "Tarihlerin farklı biçimde yazılması sıralama ve hesaplamayı hiçbir zaman etkilemez.", "Her bilgiyi tek bir hücrede birleştirmek veri doğrulamayı kolaylaştırır."],
     "Temiz veri; anlamı belli sütunlar, tutarlı tür ve biçimler, doğrulanmış değerler ve açıkça yönetilen eksiklikler gerektirir."),
    ("tr-g06-bty-note-006",
     "Bir kulüp, altı haftalık toplantılara katılan öğrenci sayısını çizgi grafiğiyle gösteriyor.",
     "Katılım 18, 21, 19, 24, 27 ve 26 olarak değişiyor; son iki haftada afiş çalışması yapılmış fakat başka etken kaydı yok.",
     "Grafik genel artışı gösterir; ancak afişin artışa tek başına neden olduğunu kanıtlamak için ek karşılaştırma gerekir.",
     "Haftalık değişimi çizgi grafiğiyle sunup afiş etkisini ayrı veri veya karşılaştırma grubuyla sınamak uygun analizdir.",
     "Dördüncü haftadan sonra katılım yüksek olsa da eş zamanlı başka değişkenler bilinmediğinden kesin neden kurulamaz.",
     ["Son değer ilk değerden büyükse aradaki bütün haftalarda kesintisiz artış vardır.", "Afiş ile artış aynı dönemde görüldüğü için afiş tek ve kesin nedendir.", "Çizgi grafiğinde eksen başlığı olmasa da değerlerin anlamı ve birimi kesin anlaşılır."],
     "Grafik örüntüyü görünür kılar; nedensellik için yalnız zaman birlikteliği değil, uygun karşılaştırma ve yeterli kanıt aranır."),
    ("tr-g06-bty-note-007",
     "Doğa kulübü, sabah kuş seslerini kaydederken uzaktan geçen araçların gürültüsünü de kayda alıyor.",
     "Gürültü profili kısa sessiz bölümden örneklenince araç uğultusu azalıyor, kuş ötüşlerinin dalga biçimi korunuyor.",
     "Gürültü azaltma, istenmeyen sürekli sesi düşürürken hedef sesin anlaşılabilirliğini koruyacak ölçüde uygulanmalıdır.",
     "Özgün kaydın kopyasını saklayıp kısa gürültü örneğiyle ölçülü azaltma yapmak ve sonucu kulaklıkla karşılaştırmak uygundur.",
     "Kuş sesleri bozulmadan uğultunun azalması, efektin hedef kaydı tümüyle silmeden işe yaradığını gösterir.",
     ["Gürültü bulunan kayıtta bütün frekansları en yüksek oranda silmek hedef sesi kesin korur.", "Ses dalga biçimini görmeden rastgele kesmek yalnız istenmeyen bölümleri kaldırır.", "Düzenleme bittikten sonra dinleme yapmak gereksizdir; ekrandaki renk kaliteyi kanıtlar."],
     "Ses düzenlemede geri alınabilir çalışma, ölçülü işlem ve önce-sonra dinleme testi birlikte kullanılır."),
    ("tr-g06-bty-note-008",
     "Okul podcastinde iki konuk konuşması, sunucu geçişleri ve kapanış müziği kullanılacak.",
     "İlk taslak 11 dakika sürüyor; hedef süre 6 dakika ve ikinci konuk aynı bilgiyi üç kez yineliyor.",
     "Kurgu, ana mesajı koruyarak yinelemeleri kısaltmalı ve bölümler arasında dinleyiciye yön veren geçişler kurmalıdır.",
     "Yinelenen bölümleri kesip her konuğa bir ana fikir ayırmak ve geçiş cümlelerini zaman çizelgesine yerleştirmek uygundur.",
     "Hedef süre aşılırken aynı bilginin yinelenmesi, içeriğin amaç ve süreye göre yeniden seçilmesi gerektiğini gösterir.",
     ["Hedef süreyi tutturmak için bütün konuk konuşmalarını hızlandırıp anlaşılmaz yapmak gerekir.", "Geçiş cümlelerini kaldırmak farklı bölümlerin ilişkisini daha açık hâle getirir.", "Kurgu sırasında ana mesaj yerine yalnız dosya boyutuna bakmak yeterlidir."],
     "Kurgu planı, içerik önceliği ve süreyi dengeler; kesme işlemi anlam bütünlüğünü bozmayacak biçimde yapılır."),
    ("tr-g06-bty-note-009",
     "Görme desteği için hazırlanan ders anlatımı okul sitesinde düşük bağlantı hızında da dinlenecek.",
     "Kayıpsız çıktı 180 MB iken konuşma için uygun sıkıştırılmış çıktı 18 MB ve dinleme testinde sözcükler anlaşılır kalıyor.",
     "Hedef kullanım konuşma dinlemekse anlaşılabilirliği koruyan daha küçük ve yaygın biçim erişimi kolaylaştırabilir.",
     "İki çıktı biçimini dosya boyutu, uyumluluk ve anlaşılabilirlikle karşılaştırıp hedefe uygun olanı yayımlamak gerekir.",
     "On kat küçük dosyanın konuşmayı anlaşılır tutması, amaç için kayıpsız büyük dosyanın zorunlu olmadığını gösterir.",
     ["En büyük dosya her zaman en erişilebilir ses ürünüdür.", "Sıkıştırılmış bir ses dosyası hiçbir aygıtta açılamaz.", "Ses ürünü seçerken hedef kitlenin bağlantı ve aygıt koşulları dikkate alınmaz."],
     "Ses çıktısı, teknik olarak en büyük değer yerine kullanıcı gereksinimi, yeterli kalite, boyut ve uyumluluk dengesiyle seçilir."),
    ("tr-g06-bty-note-010",
     "Bir ekip stop-motion deney videosunda 240 fotoğrafı zaman çizelgesine aktarıyor.",
     "Bazı kareler iki kez eklenmiş, başlık görüntünün önemli bölümünü kapatıyor ve ön izleme kısa süreli sıçrıyor.",
     "Yinelenen kareler kaldırılmalı, süreler dengelenmeli ve başlık içeriği örtmeyecek güvenli alana taşınmalıdır.",
     "Zaman çizelgesinde yinelenen kareleri bulup silmek, başlığı yeniden konumlandırmak ve ön izlemeyi tekrar izlemek doğru adımdır.",
     "Sıçramanın yinelenen kareler kaldırılınca bitmesi, sorunun çekimden değil kurgu sırasından kaynaklandığını destekler.",
     ["Sıçramayı gidermek için bütün karelere farklı ve yoğun efektler eklemek gerekir.", "Başlık ana görüntüyü kapatıyorsa yazı boyutunu daha da büyütmek anlaşılabilirliği artırır.", "Ön izleme hatası görüldüğünde zaman çizelgesini kontrol etmeden dışa aktarmak sorunu çözer."],
     "Video düzenleme, zaman çizelgesindeki her öğenin süre, sıra ve görünürlük bakımından amaca hizmet etmesini gerektirir."),
    ("tr-g06-bty-note-011",
     "Geri dönüşüm videosunda atığın bulunması, türünün okunması ve doğru kutuya bırakılması farklı günlerde çekiliyor.",
     "Taslakta kutuya bırakma önce, etiket okuma sonra geliyor; el ve nesne konumu iki kesme arasında aniden değişiyor.",
     "Anlatı sırası ve görsel süreklilik birlikte bozulduğu için çekimler işlem sırasına konmalı ve uyumlu kesmeler seçilmelidir.",
     "Önce bulma, sonra etiketi okuma, en son ayırma planını kurup ardışık çekimlerde konum tutarlılığını denetlemek gerekir.",
     "İzleyicinin işlemi ters anlaması ve nesnenin sıçraması, hem olay örgüsü hem devamlılık hatası bulunduğunu gösterir.",
     ["Sahneleri çekim tarihine göre sıralamak her zaman anlatının doğru sırasını verir.", "Nesnenin kesme arasında yer değiştirmesi videoyu daha gerçekçi yapar.", "Süreklilik yalnız ses seviyesidir; görüntü konumuyla ilişkili değildir."],
     "Kurgu, neden-sonuç sırasını ve ardışık görüntülerdeki yön, konum, hareket devamlılığını koruyarak anlaşılır hikâye kurar."),
    ("tr-g06-bty-note-012",
     "Bir röportaj videosu okul sitesine ve sınıf projektörüne ayrı çıktılarla hazırlanıyor.",
     "Site sürümü küçük ekranda akıcı; projektör sürümünde yazılar bulanık, ses ise iki sürümde de eş zamanlı.",
     "Farklı gösterim ortamları için çözünürlük ve bit hızı ayrı seçilebilir; bulanık yazı projektör çıktısının görüntü ayarını artırmayı gerektirir.",
     "Kaynak projeyi koruyup site ve projektör için iki hedef profil oluşturmak, her çıktıyı gerçek aygıtta sınamak uygundur.",
     "Ses iki sürümde de doğruyken yalnız büyük ekranda yazı bozuluyorsa sorun ses kurgusundan çok görüntü çözünürlüğüyle ilişkilidir.",
     ["Tek çıktı dosyası bütün ekran ve bağlantı koşullarında zorunlu olarak en iyi sonucu verir.", "Projektörde yazı bulanıksa ses dosyasını büyütmek görüntüyü keskinleştirir.", "Dışa aktarım profilinin çözünürlük ve bit hızıyla ilişkisi yoktur."],
     "Video tesliminde hedef aygıt ve bağlantı koşulu belirlenir; uygun profil seçilir ve son dosya kendi kullanım ortamında doğrulanır."),
    ("tr-g06-bty-note-013",
     "Bir mesaj, 'yarın bütün okullar tatil' iddiasını kaynak göstermeden sınıf grubunda yayıyor.",
     "Valilik ve okulun resmî kanallarında duyuru yok; mesajın görseli geçen yıla ait ve tarih bölümü kesilmiş.",
     "Kaynağı ve tarihi doğrulanmayan mesaj paylaşılmamalı; güncel bilgi yetkili kurumun resmî kanalından kontrol edilmelidir.",
     "Mesajı iletmeden önce görselin tarihini ve resmî duyuruları karşılaştırıp yanlışsa grubu düzeltmek amaca uygun kullanımdır.",
     "Güncel resmî duyuru bulunmaması ve eski görsel, iddianın güvenilir kanıt taşımadığını gösterir.",
     ["Çok kişi paylaştığı için mesajın doğruluğu ayrıca kontrol edilmez.", "Görselde kurum logosu görünmesi tarihin güncel olduğunu kesin kanıtlar.", "Yanlış bilgi olasılığında en hızlı davranış mesajı daha fazla gruba iletmektir."],
     "İnternet bilgisinde kaynak, tarih, bağlam ve bağımsız doğrulama aranır; yaygınlık doğruluğun kanıtı değildir."),
    ("tr-g06-bty-note-014",
     "Kütüphane kartı kapıya birkaç santimetre yaklaştırılınca kimliği okuyucuya iletiyor; uzaktan bağlantı kurmuyor.",
     "Kart yakınken işlem bir saniyede tamamlanıyor, on santimetre uzaklaştırılınca okuyucu yanıt vermiyor.",
     "Çok kısa menzil ve küçük kimlik verisi, yakın alan iletişimine uygun bir kullanım özelliğidir.",
     "Kapı kimliği için kısa menzilli temassız bağlantı kullanıp uzun mesafeli veri aktarımını ayrı ağ üzerinden yürütmek uygundur.",
     "Mesafe birkaç santimetreyi aşınca iletişimin kesilmesi, teknolojinin geniş alan ağı için tasarlanmadığını gösterir.",
     ["Birkaç santimetrede çalışan kart iletişimi kıtalar arası mobil ağdır.", "Kısa menzil her durumda daha çok enerji tüketip daha az güvenlik sağlar.", "İletişim teknolojileri kapsama uzaklığına göre sınıflandırılamaz."],
     "Bağlantı türü menzil, veri miktarı, hareketlilik, enerji ve güvenlik gereksinimleri birlikte incelenerek seçilir."),
    ("tr-g06-bty-note-015",
     "Sınıf içi yerel ağda dosya sunucusu, yazıcı ve internet bağlantısı ortak kullanılıyor.",
     "Yazıcı çalışırken yalnız bir bilgisayar sunucuyu göremiyor; aynı bilgisayarın ağ adresi diğerleriyle çakışıyor.",
     "Tek aygıttaki adres çakışması yerel bağlantıyı bozabilir; ağın tümü kesik olmadığı için sorun o aygıtın yapılandırmasında aranmalıdır.",
     "Çakışan ağ adresini otomatik veya benzersiz olacak biçimde düzeltip sunucu erişimini yeniden test etmek uygun adımdır.",
     "Diğer aygıtların sunucuya ulaşması, ortak sunucunun ve ana bağlantının çalıştığını; hatanın tek istemciyle sınırlı olduğunu gösterir.",
     ["Bir bilgisayar bağlanamıyorsa bütün okulun internet kablosu kesin kopmuştur.", "Aynı ağdaki iki aygıta aynı adresi vermek iletişimi daha hızlı yapar.", "Yazıcının çalışması yerel ağdaki bütün ayarların her aygıtta doğru olduğunu kanıtlar."],
     "Ağ sorunları kapsamına göre daraltılır; çalışan bileşenler kanıt olarak kullanılır ve istemci, bağlantı, adresleme sırasıyla sınanır."),
    ("tr-g06-bty-note-016",
     "Bir bilgisayar açıldığında dosyaların uzantıları değişmiş ve ödeme isteyen bir ekran görünmüş.",
     "Haricî diskte önceki güne ait çevrim dışı yedek var; işletim sistemi uzun süredir güncellenmemiş.",
     "Belirtiler fidye yazılımı olasılığını gösterir; aygıt ağdan ayrılmalı, yetişkine/uzmana bildirilmeli ve temiz yedek kontrollü kullanılmalıdır.",
     "Aygıtı ağdan ayırıp olayı sorumlu kişiye bildirmek, sistemi güvenli ortamda temizlemek ve doğrulanmış yedeği geri yüklemek uygundur.",
     "Çevrim dışı yedeğin etkilenmemesi, düzenli ve bağlantısı kesilen yedeklemenin zararı azaltan ayrı bir savunma katmanı olduğunu gösterir.",
     ["Ödeme ekranındaki bağlantıya tıklamak dosyaların güvenli biçimde döneceğini garanti eder.", "Bulaşmış bilgisayarı ağda açık tutmak diğer aygıtları korur.", "Güncelleme ve yedekleme zararlı yazılımlarla ilişkili değildir."],
     "Olay müdahalesi yayılmayı durdurma, uzman desteği, güvenli temizleme ve doğrulanmış yedekten kurtarma adımlarını içerir; riskli ödeme önermez."),
    ("tr-g06-bty-note-017",
     "Öğrenciler tanıtım videosuna popüler bir şarkının tamamını arka plan olarak eklemek istiyor.",
     "Şarkı sayfası 'tüm hakları saklıdır' diyor; okulun lisanslı müzik arşivinde benzer, atıfla kullanılabilen bir parça bulunuyor.",
     "Eserin okul projesinde kullanılması otomatik izin değildir; lisans koşulu uygun alternatif seçilip gerekli atıf yapılmalıdır.",
     "Tüm hakları saklı şarkı yerine kullanım izni açık parçayı seçmek ve belirtilen eser sahibi bilgisini videoya eklemek gerekir.",
     "İkinci parçanın lisansı eğitim videosuna ve atıfla paylaşıma izin verdiği için belgelenebilir yasal seçenek odur.",
     ["Video para kazandırmadığı için her şarkının tamamı izinsiz kullanılabilir.", "Şarkının adını değiştirmek telif hakkını ortadan kaldırır.", "Atıf yazmak, lisansın açıkça yasakladığı her kullanımı serbest bırakır."],
     "Telifli içerikte amaç kadar lisansın verdiği haklar, kullanım kapsamı ve atıf koşulu denetlenir; uygun alternatif seçimi etik çözüm olabilir."),
    ("tr-g06-bty-note-018",
     "Bir öğrenci hakkında alaycı bir video sınıf grubunda tekrar tekrar paylaşılıyor.",
     "Hedef öğrenci rahatsız olduğunu söylüyor; mesajların tarih ve kullanıcı bilgileri görülebiliyor.",
     "Tekrarlanan incitici paylaşım siber zorbalıktır; karşılık vererek yaymak yerine kanıt korunup güvenilir yetişkin ve platforma bildirilmelidir.",
     "Mesajların ekran görüntüsünü güvenli saklayıp paylaşımı durdurmak, engelleme-bildirme araçlarını ve yetişkin desteğini kullanmak gerekir.",
     "İçeriğin yinelenmesi ve hedef kişinin zarar görmesi, olayın sıradan şakadan öte müdahale gerektiren siber zorbalık olduğunu gösterir.",
     ["Rahatsız edici videoyu daha çok kişiye göndermek kanıtı korumanın en güvenli yoludur.", "Çevrim içi olduğu için incitici paylaşımın gerçek etkisi olmaz.", "Hedef öğrenci tek başına karşılık vermeli ve hiçbir yetişkine haber vermemelidir."],
     "Siber zorbalıkta güvenlik, yayılımı durdurma, kanıtı değiştirmeden saklama, engelleme ve güvenilir destek alma önceliklidir."),
    ("tr-g06-bty-note-019",
     "Bir ekip, üzerinde CC BY-SA yazan bir çizimi değiştirerek ders oyununun kapağında kullanacak.",
     "Lisans metni eser sahibinin belirtilmesini ve uyarlamanın aynı lisansla paylaşılmasını istiyor.",
     "CC BY-SA uyarlamaya izin verir; ancak atıf ve aynı lisansla paylaşma koşulları yerine getirilmelidir.",
     "Eser sahibini ve lisansı belirtip değiştirilen kapağı aynı lisans koşuluyla yayımlamak uygun kullanımdır.",
     "Uyarlama izni koşullu olduğundan yalnız isim yazmak yetmez; yeni ürünün paylaşım lisansı da uyumlu olmalıdır.",
     ["CC BY-SA, eser sahibinin adını silmeyi ve tüm hakları kapatmayı gerektirir.", "Aynı lisans koşulu yalnız dosyanın rengini belirler; yeniden paylaşımı etkilemez.", "Creative Commons işareti bulunan bütün eserler koşulsuz kamu malıdır."],
     "Lisans sembolleri belirli izin ve yükümlülükleri birlikte taşır; kullanıcı değişiklik, atıf ve paylaşım koşullarını ayrı ayrı uygular."),
    ("tr-g06-bty-note-020",
     "Sesli komut modeli için yalnız yetişkinlerin sessiz odada söylediği kayıtlar toplanıyor; ürün çocukların gürültülü sınıfında kullanılacak.",
     "Model yetişkin denemelerinde başarılı, çocuk seslerinde ve sınıf uğultusunda komutları sıkça karıştırıyor.",
     "Eğitim verisi hedef kullanıcı ve ortamı temsil etmediği için model başarısı gerçek kullanım koşullarına genellenemez.",
     "İzinli çocuk sesi örneklerini farklı ortam gürültüleriyle dengeli toplamak ve kişisel kayıtları güvenli yönetmek gerekir.",
     "Hatanın çocuk ve gürültü koşullarında yoğunlaşması, veri dağılımının hedef kullanımı kapsamadığını gösterir.",
     ["Sessiz odadaki yetişkin kayıtları bütün yaş ve ortamları eksiksiz temsil eder.", "Daha çok aynı yetişkin sesini eklemek çocuk seslerindeki yanlılığı kesin çözer.", "Ses verisi kişisel veri sayılamayacağı için izin ve saklama kuralı gerekmez."],
     "Yapay zekâ girdileri hedef nüfusu, ortam çeşitliliğini ve etik veri kurallarını kapsamalı; başarı ilgili koşullarda ayrı ölçülmelidir."),
    ("tr-g06-bty-note-021",
     "Bir yapay zekâ aracı, okul bahçesindeki bitkinin zehirli olduğunu kesin bir dille söylüyor.",
     "Araç kaynak vermiyor; iki botanik kaynağı aynı fotoğrafla kesin tür belirlenemeyeceğini ve bitkiye dokunulmamasını öneriyor.",
     "Kaynak göstermeyen yapay zekâ çıktısı sağlık ve güvenlik kararında tek kanıt olamaz; uzman ve güvenilir kaynak doğrulaması gerekir.",
     "Bitkiye dokunmadan yetişkine haber vermek, birden çok güvenilir kaynağı ve gerekirse uzman görüşünü kullanmak doğru yaklaşımdır.",
     "Bağımsız kaynakların fotoğraf sınırını belirtmesi, aracın kesinlik düzeyinin kanıtla desteklenmediğini gösterir.",
     ["Yapay zekâ kesin konuştuğu için bitkiyi tatmak güvenli doğrulama yöntemidir.", "Kaynak göstermeyen yanıt, akıcı yazıldığı için uzman görüşünden üstündür.", "Aynı soruyu araca tekrar sormak bağımsız kaynak doğrulaması sayılır."],
     "Yapay zekâ çıktısı risk düzeyine uygun dikkatle değerlendirilir; belirsizlik saklanmaz ve fiziksel güvenlik için yetkin kişiye başvurulur."),
    ("tr-g06-bty-note-022",
     "Atık türü modeli kâğıt, plastik ve metal görüntüleriyle eğitiliyor; testte metali sıkça plastik sanıyor.",
     "Hata tablosunda 30 metal örneğinin 12'si plastik, yalnız 2 kâğıt örneği yanlış sınıflandırılmış.",
     "Toplam doğruluk tek başına yetmez; hata dağılımı metal sınıfının yeterince öğrenilmediğini gösterir.",
     "Metal örneklerinin çeşitliliğini ve etiketlerini inceleyip modeli ayrı test kümesiyle yeniden değerlendirmek gerekir.",
     "Yanlışların metalde yoğunlaşması, iyileştirme önceliğinin bu sınıfın verisi ve ayırt edici özellikleri olduğunu gösterir.",
     ["Kâğıt sınıfı iyi olduğu için model bütün sınıflarda eşit derecede başarılıdır.", "Test hatalarını eğitim verisine ekleyip aynı veride ölçmek bağımsız başarıyı korur.", "Yanlış sınıflanan metal örneklerini silmek modelin gerçek dünyadaki sorununu çözer."],
     "Model değerlendirmesi sınıf bazlı hata örüntülerini, bağımsız testi ve veri kalitesini birlikte kullanarak hedefli iyileştirme yapar."),
    ("tr-g06-bty-note-023",
     "Bir blok programında karakter, boşluk tuşuna basılınca on kez zıplayacak; puan yalnız engel aşılırsa artacak.",
     "Kodda on tekrar döngüsü var fakat puan artırma bloğu döngünün dışında ve koşulsuz çalışıyor.",
     "Puanın her denemede artması, puan bloğunun engel koşulunun içine taşınması gerektiğini gösterir.",
     "Engel algılama koşulunu döngü içinde sınayıp puanı yalnız koşul doğru olduğunda artırmak uygundur.",
     "Zıplama sayısı doğruyken puan hatalıysa döngü sayacından çok koşul ve değişken bloğunun konumu incelenmelidir.",
     ["Puanı düzeltmek için tekrar sayısını rastgele artırmak gerekir.", "Koşul bloğunun içinde veya dışında olmak komutun ne zaman çalışacağını etkilemez.", "Değişken değeri yalnız kostüm değiştirerek saklanabilir."],
     "Blokların yuvalanma yeri yürütme kapsamını belirler; olay, döngü, koşul ve değişken beklenen davranışa göre izlenir."),
    ("tr-g06-bty-note-024",
     "Bir kelime oyununda doğru harf girildiğinde ilerleme bekleniyor; Türkçe karakterlerde program yanıtı yanlış sayıyor.",
     "Küçük İngilizce harfler geçiyor, 'ş' ve 'ğ' içeren örnekler kalıyor; karşılaştırma bloğu yalnız sınırlı karakter listesi kullanıyor.",
     "Hatanın belirli Türkçe karakterlerde yinelenmesi, karşılaştırma ve normalleştirme adımında eksik durum bulunduğunu gösterir.",
     "Türkçe karakterleri kapsayan testler ekleyip karşılaştırma kuralını düzeltmek, sonra eski ve yeni testleri birlikte çalıştırmak gerekir.",
     "Başarılı ve başarısız girdilerin karakter türüne göre ayrılması, hatayı kullanıcı girişini işleyen bloklara daraltır.",
     ["Bir test geçtiği için program bütün alfabelerde doğru çalışır.", "Türkçe karakter hatasını gidermek için oyunun bütün görsellerini silmek gerekir.", "Başarısız örnekleri test listesinden çıkarmak yazılımı düzeltir."],
     "Hata ayıklama, örüntüyü yeniden üretir, nedeni küçük bir adıma daraltır ve düzeltmenin eski işlevleri bozmadığını regresyon testiyle denetler."),
    ("tr-g06-bty-note-025",
     "Blok tabanlı erişilebilirlik projesi sınıftaki sesleri tanıyıp işitme güçlüğü olan kullanıcıya görsel uyarı verecek.",
     "Model zil sesinde yüzde 92, alkışta yüzde 88, konuşmada yüzde 54 güven gösteriyor; proje her sonuçta aynı kırmızı uyarıyı yakıyor.",
     "Model çıktısı güven ve ses türüyle birlikte koşullara bağlanmalı; düşük güvenli konuşma sonucu kesin tehlike gibi gösterilmemelidir.",
     "Her ses türü için anlaşılır görsel belirlemek, düşük güven durumunda 'ses anlaşılamadı' uyarısı vermek ve kullanıcıyla test yapmak uygundur.",
     "Güven düzeyleri farklıyken tek renk kullanılması, model çıktısının blok kararlarına anlamlı biçimde dönüştürülmediğini gösterir.",
     ["Yapay zekâ bloğu eklendiğinde güven puanı ve kullanıcı geri bildirimi gereksiz olur.", "Bütün sesleri aynı uyarıyla göstermek erişilebilirliği her durumda artırır.", "Sınıf seslerini süresiz saklamak, kullanıcı izni olmadan da zorunlu geliştirme adımıdır."],
     "Yapay zekâ destekli üründe model sonucu, belirsizlik, kullanıcı ihtiyacı ve mahremiyet koşulları blok mantığına açıkça yansıtılır."),
]


MODE_SEQUENCE = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
LEVEL_SEQUENCE = (
    [1] * 15 + [2] * 10
    + [1] * 5 + [2] * 15 + [3] * 15
    + [3] * 10 + [4] * 10 + [5] * 5
    + [3] * 5 + [4] * 10
)


def table(qid: str, scenario: str, evidence: str, labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.alt"
    labels[h1] = "Kanıt bölümü"
    labels[h2] = "İçerik"
    labels[alt] = "Bir bilişim vakasının bağlamını ve gözlenen sonucunu iki satırda sunan tablo; sonuç değerlendirmesi içermez."
    return {
        "kind": "table", "headerKeys": [h1, h2],
        "rows": [[{"v": "Vaka"}, {"v": scenario}], [{"v": "Gözlenen sonuç"}, {"v": evidence}]],
        "altTextKey": alt,
    }


def make_question(local: int, entry: tuple[Any, ...], mode: str, level: int,
                  notes: dict[str, dict[str, Any]], labels: dict[str, str]) -> dict[str, Any]:
    note_id, scenario, evidence, concept, action, inference, wrongs, rationale = entry
    note = notes[note_id]
    objective = str((note.get("objectives") or [note.get("objective")])[0])
    number = 100 + local
    qid = f"tr-g06-bank-bty-b02-q{local:03d}"
    correct_position = (local - 1) % 4
    topic = str(note["title"]).replace("İ", "i").replace("I", "ı").lower()
    if mode == "comprehension":
        variant = (local - 1) % 5
        template_id = f"g6-bty-b02-concept-v{variant + 1}"
        correct = concept
        stems = (
            f"{scenario} Bu yeni örneğin temel bilişim işlevini doğru açıklayan ifade hangisidir?",
            f"{scenario} {topic} bakımından durumun ayırt edici özelliği hangi seçenekte verilmiştir?",
            f"{scenario} Kavramın kapsamını aşmadan kurulabilecek sonuç hangisidir?",
            f"{scenario} Araç, veri ve amaç ilişkisini doğru sınıflandıran açıklama hangisidir?",
            f"{scenario} Bu olayda hangi temel bilgi bir kavram karışıklığını önler?",
        )
        stem = stems[variant]
        explanation = f"{rationale} Bu nedenle doğru ifade yeni vakadaki ayırt edici işlevi açıkça sınırlar."
        figure = None
    elif mode == "application":
        combined = 51 <= local <= 60
        variant = (local - 1) % 5
        template_id = f"g6-bty-b02-{'act-check' if combined else 'act'}-v{variant + 1}"
        if combined:
            correct = f"{action} Ardından gözlenen sonuç, belirlenen başarı ölçütüyle karşılaştırılmalıdır."
            stems = (
                f"{scenario} Deneme kaydı “{evidence}” diyor. Uygulama ve kontrolü birlikte içeren plan hangisidir?",
                f"{scenario} İlk sonuç şöyledir: {evidence} {topic} için kararı uygulayıp sınayan seçenek hangisidir?",
                f"{scenario} Ekip “{evidence}” gözlemini alıyor. Hem eylem hem doğrulama adımı hangi planda vardır?",
                f"{scenario} Pilot çalışmada “{evidence}” kaydediliyor. Çözümü ölçülebilir bir testle birleştiren karar hangisidir?",
                f"{scenario} Uygulamadan önce ve sonra karşılaştırma yapılacaktır. “{evidence}” kaydını da kullanan yaklaşım hangisidir?",
            )
            stem = stems[variant]
            explanation = f"{rationale} Doğru plan, eylemi seçmenin yanında gerçek sonucu önceden belirlenen ölçütle denetler."
        else:
            correct = action
            stems = (
                f"{scenario} Bu gereksinim için uygulanabilir ve sorumlu karar hangisidir?",
                f"{scenario} Ekip {topic} bilgisini tasarım kararına dönüştürecek. Hangi adım seçilmelidir?",
                f"{scenario} Dört öneriden hangisi hem amaca hem güvenilir çalışma ölçütüne uygundur?",
                f"{scenario} Sorunu gereksiz risk oluşturmadan çözen işlem hangisidir?",
                f"{scenario} Kullanıcı koşulları dikkate alındığında hangi uygulama kararı verilmelidir?",
            )
            stem = stems[variant]
            explanation = f"{rationale} Doğru karar, bu vakadaki gereksinimi uygulanabilir ve denetlenebilir bir adıma dönüştürür."
        figure = None
    elif mode == "analysis":
        variant = (local - 1) % 5
        template_id = f"g6-bty-b02-evidence-v{variant + 1}"
        correct = inference
        stems = (
            f"Aşağıdaki tabloda {topic} için yeni bir vaka ve gözlenen sonuç verilmiştir. Hangi çıkarım iki kaydı birlikte açıklar?",
            f"Aşağıdaki tabloda yer alan kanıt {topic} kapsamında incelenecektir. Hangi sonuç, verilen bilginin sınırını aşmaz?",
            f"Aşağıdaki tabloda bir uygulama ile sonucu eşleştirilmiştir. {topic} açısından hangi yorum desteklenir?",
            f"Aşağıdaki tabloda {topic} için neden ve sonuç ilişkisini denetleyecek iki kayıt vardır. Hangi değerlendirme bu ilişkiyi doğru kurar?",
            f"Aşağıdaki tabloda sunulan veriye göre {topic} hakkında bir rapor cümlesi seçilecektir. Yalnız kanıtla doğrulanan cümle hangisidir?",
        )
        stem = stems[variant]
        explanation = f"{rationale} Tablodaki gözlem, doğru çıkarımı desteklerken daha geniş ve kanıtsız yorumlara izin vermez."
        figure = table(qid, scenario, evidence, labels)
    else:
        variant = (local - 1) % 3
        template_id = f"g6-bty-b02-misconception-v{variant + 1}"
        mistaken = wrongs[(local - 1) % 3]
        correct = f"Doğru düzeltme şudur: {concept}"
        stems = (
            f"Bir öğrenci “{mistaken}” diyor; {topic} bilgisini kullanarak bu somut yanılgıyı düzelten seçenek hangisidir?",
            f"Bir öğrenci {topic} konusunda “{mistaken}” sonucunu yazıyor. Hatalı kararı gerekçesiyle düzelten ifade hangisidir?",
            f"Bir öğrencinin çözümünde “{mistaken}” iddiası vardır. İddianın gözden kaçırdığı temel ölçütü geri kuran seçenek hangisidir?",
        )
        stem = stems[variant]
        explanation = f"{rationale} Öğrencinin iddiası gerekli ölçütü dışarıda bıraktığından doğru seçenek kavramı yeni bağlam için yeniden kurar."
        figure = None

    choices = rotate(correct, list(wrongs), correct_position)
    reasons = {
        correct: f"Doğru gerekçe: {rationale} Seçenek vakadaki amaç, kanıt ve sınırı birlikte korur.",
        wrongs[0]: f"Tek belirti yanılgısı: {wrongs[0]} ifadesi bir görünümü bütün sürecin kanıtı sayarak gerekli ölçütleri atlar.",
        wrongs[1]: f"Koşulsuz genelleme: {wrongs[1]} ifadesi yalnız bazı durumlarda geçerli olabilecek yargıyı bütün örneklere taşır.",
        wrongs[2]: f"İşlev karışıklığı: {wrongs[2]} ifadesi araç, veri, izin veya test adımlarından birini yanlış görevle eşleştirir.",
    }
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "Vaka ve gözlenen sonuç yalnız tabloda sunulduğu için çıkarım tabloya bağlıdır.",
        "acceptableKinds": ["table"], "evidenceDimensions": ["vaka", "gözlenen sonuç"],
    } if figure else {
        "level": "none", "role": "none",
        "rationale": "Sorunun çözümünde kullanılacak bütün bilgi metin içinde verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": number,
        "subject": "Bilişim Teknolojileri ve Yazılım", "grade": 6,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — ikinci özgün vaka",
        "objective": objective, "objectiveId": objective,
        "noteId": note_id, "noteKey": note_id,
        "question": stem, "choices": choices, "correct": correct_position,
        "correctIndex": correct_position, "correctOption": choices[correct_position],
        "distractorWhy": [reasons[choice] for choice in choices],
        "explanation": explanation, "level": level,
        "difficultyReason": (
            f"Düzey {level}; {topic} bilgisini bağımsız ikinci vakadaki amaç, kanıt ve sınırlara göre "
            f"{mode} görevinde kullanmayı gerektirir."
        ),
        "questionType": mode, "familyId": f"tr-g06-bank-bty-b02-family-{local:03d}",
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
    missing = sorted({case[0] for case in CASES} - set(notes))
    if missing or len(CASES) != 25:
        raise RuntimeError(f"case/note coverage error: missing={missing} count={len(CASES)}")
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    expected_ids = [f"tr-g06-bank-bty-b01-q{i:03d}" for i in range(1, 101)]
    if [str(row.get("id")) for row in existing] != expected_ids:
        raise RuntimeError("batch 01 is missing or has changed; regenerate and validate it first")
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    rows = [
        make_question(local, CASES[(local - 1) % 25], MODE_SEQUENCE[local - 1],
                      LEVEL_SEQUENCE[local - 1], notes, labels)
        for local in range(1, 101)
    ]
    all_rows = existing + rows
    OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in all_rows) + "\n",
        encoding="utf-8", newline="\n",
    )
    LABELS_OUTPUT.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({"questions": len(rows), "total": len(all_rows), "labels": len(labels), "sourceQuestionReads": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
