#!/usr/bin/env python3
"""Append six audited Grade 7 Turkish batches (600 questions) from notes only."""
from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
import re
from typing import Any

from author_grade6_mixed_batch03 import LEVEL_SEQUENCE, make_question, read_notes_only
from author_grade7_dkab_batch01 import LABELS_OUTPUT, OUTPUT


SOURCE = Path("turkiye/7-sinif/turkce/turkce-tum.jsonl")
MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15


CONTEXTS = {
    1: [
        ("Tohum Günlüğü", "Zeynep aynı tür üç tohumu eş saksılara ekti. Yalnız ışık sürelerini değiştirdi; boyları haftada iki kez ölçüp günlüğüne yazdı. Dördüncü hafta, daha uzun ışık alan saksının daha hızlı büyüdüğünü fakat tek denemenin bütün bitkiler için yeterli olmayacağını belirtti."),
        ("Bisiklet Onarım Atölyesi", "Mahalle atölyesinde usta, gevşek zinciri hemen değiştirmek yerine önce temizledi ve gerginliğini ayarladı. Kısa deneme sürüşünde sorun çözülünce öğrencilere 'Parçayı atmadan önce nedeni araştırın.' dedi."),
        ("Yeni Bir Dil Öğrenmek", "Mert her gün uzun kelime listeleri ezberliyordu; ancak konuşurken sözcükleri hatırlayamıyordu. Daha sonra kelimeleri kısa diyaloglarda kullandı, yanlışlarını kaydetti ve haftalık hedefini buna göre değiştirdi."),
        ("Gökyüzü Gözlem Defteri", "Duru bir ay boyunca Ay'ı aynı saatte gözledi. Çizimlerini tarihlendirdi, bulutlu günleri ayrıca işaretledi ve şeklin düzenli değişimini fark etti. Gözleyemediği günleri tahminle doldurmadı."),
    ],
    2: [
        ("Cephedeki Mektup", "Mektupta asker, köyündeki ailesini özlediğini anlatırken görev arkadaşlarının dayanışmasını da yazıyordu. Tarih ve yer bilgisi bulunan belge, kişisel duygu ile dönemin koşullarını aynı sayfada buluşturuyordu."),
        ("Eski Köprünün Kitabesi", "Restorasyon ekibi kitabeyi temizlemeden önce yüksek çözünürlüklü fotoğraf çekti, harfleri uzmanlarla karşılaştırdı ve okunamayan bölümleri boş bıraktı. Tahmin edilen kelimeleri kesin bilgi gibi yazmadı."),
        ("Köy Okulunun Arşivi", "1928 tarihli yoklama defterinde öğrenci adları ve devam günleri vardı. Araştırmacı, tek defterin bütün bölgedeki eğitim durumunu göstermeyeceğini belirterek başka okul kayıtlarını da aradı."),
        ("Anıttaki Sessizlik", "Tören sona erdiğinde meydanda kısa bir sessizlik oldu. Çocuklar, taş duvardaki isimleri okudu; rehber, her ismin ayrı bir yaşam öyküsüne açıldığını söyledi."),
    ],
    3: [
        ("Apartman Toplantısı", "Toplantıda herkes otopark sorununu konuşuyor ama kimse birbirini dinlemiyordu. Yönetici söz sırası oluşturdu, ortak noktaları tahtaya yazdı ve iki öneriyi maliyet ile güvenlik ölçütlerine göre oylattı."),
        ("Sınıf Mesaj Grubu", "Bir öğrenci, arkadaşının kısa mesajını öfkeli bir cevap sanıp hemen karşılık verdi. Sonra ses tonunun yazıda görünmediğini fark etti, ne demek istediğini sordu ve yanlış anlamayı düzeltti."),
        ("Kayıp Cüzdan", "Ece, durakta bulduğu cüzdanı sosyal medyada açık adresle paylaşmak yerine belediyenin kayıp eşya birimine teslim etti. Teslim tutanağını aldı ve yalnız gerekli bilgiyi paylaştı."),
        ("Sessiz Kütüphane", "Kütüphanede grup çalışması yapan öğrenciler çevredekileri rahatsız ediyordu. Görevli onları susturmakla yetinmedi; konuşma odasının boş saatlerini gösterdi ve ortak bir kullanım planı hazırlamalarını istedi."),
    ],
    4: [
        ("Ebru Teknesi", "Sanatçı suyun üzerine üç renk bıraktı, bizle ince çizgiler oluşturdu ve kâğıdı tek hareketle yüzeye yatırdı. Aynı desenin yeniden yapılabileceğini ama birebir kopyalanamayacağını açıkladı."),
        ("Çini Atölyesi", "Usta, lale motifinin çevresine dengeli boşluklar bıraktı. Öğrenciler yalnız rengi değil tekrar, simetri ve kompozisyonu da inceledi; her motifin dönemi hakkında kaynak notu ekledi."),
        ("Bağlamanın Sesi", "Müzisyen aynı ezgiyi önce yavaş, sonra hareketli çaldı. Nota dizisi büyük ölçüde değişmediği hâlde vurgu ve tempo, dinleyicide farklı duygular uyandırdı."),
        ("Gölge Oyunu", "Perde arkasındaki tasvir ışığa yaklaştıkça büyüdü. Oynatıcı, mizahın yalnız sözlerden değil hareket, duraklama ve seyirciyle kurulan ilişkiden doğduğunu gösterdi."),
    ],
    5: [
        ("Gezici Kütüphane", "Otobüs kütüphane ayda iki kez dağ köylerine gidiyordu. Görevli, ödünç alınan kitap sayısının arttığını ancak yaş gruplarına göre tür çeşitliliğinin hâlâ yetersiz olduğunu raporladı."),
        ("Kitap Kulübü", "Kulüp üyeleri aynı romanı okudu fakat farklı bölümleri önemli buldu. Her üye yorumunu metinden bir cümleyle destekledi; başkasının görüşünü değiştirmek yerine gerekçeleri karşılaştırdı."),
        ("Dijital Okuma", "Arda ekrandaki uzun metinde sürekli bağlantılara tıklayınca ana düşünceyi kaçırdı. Bildirimleri kapattı, bölüm başlıklarını not etti ve yalnız amacıyla ilgili bağlantıları açtı."),
        ("Mahalle Kitaplığı", "Boş dükkân raflarla donatıldı; kitap bağışları konu ve yaş düzeyine göre sınıflandırıldı. Gönüllüler, çok eski veya eksik sayfalı kitapları yalnız sayı artsın diye rafa koymadı."),
    ],
    6: [
        ("Okul Temsilcisi Seçimi", "Adaylara eşit konuşma süresi verildi, oylar gizli kullanıldı ve sayım öğrencilerin önünde yapıldı. İtirazların yazılı alınacağı tarih önceden duyuruldu."),
        ("Erişilebilir Park", "Yeni park planında rampa vardı fakat oyun panoları çok yüksekteydi. Tasarım ekibi farklı kullanıcılarla deneme yaptı; yükseklikleri değiştirdi ve sesli yönlendirme ekledi."),
        ("Temiz Dere Başvurusu", "Mahalleli, deredeki kirliliği yalnız fotoğrafla bildirmedi. Aynı noktalardan tarihli gözlem tuttu, yetkili kuruma dilekçe verdi ve başvuru numarasıyla sonucu izledi."),
        ("Kişisel Veri Afişi", "Afiş, güçlü parola önerirken kimlik numarası ve konum gibi bilgilerin izinsiz paylaşılmamasını vurguluyordu. Kaynak bölümünde resmî rehbere bağlantı ve güncelleme tarihi bulunuyordu."),
    ],
}

CONTEXT_DECISIONS = {
    "Tohum Günlüğü": "ölçümlerin düzenli tutulması güçlü kanıttır; tek denemenin bütün bitkilere genellenmemesi ise açık sınırdır",
    "Bisiklet Onarım Atölyesi": "parçayı atmadan önce temizleme ve ayar yapma, nedeni araştıran aşamalı çözümü somutlaştırır",
    "Yeni Bir Dil Öğrenmek": "ezberden bağlamlı kullanıma geçiş ile yanlış günlüğü, öğrenme stratejisinin kanıtla uyarlanmasını gösterir",
    "Gökyüzü Gözlem Defteri": "bulutlu günleri ayrı işaretlemek ve boşlukları uydurmamak, gözlem ile tahmini birbirinden ayırır",
    "Cephedeki Mektup": "tarih ve yer künyesi kişisel duygunun hangi dönem koşulunda yazıldığını doğrulayan bağlam sağlar",
    "Eski Köprünün Kitabesi": "okunamayan bölümü boş bırakmak, uzman karşılaştırması tamamlanmadan tahmini kesin bilgiye dönüştürmez",
    "Köy Okulunun Arşivi": "tek yoklama defteri yerel kanıt sunar fakat bütün bölgenin eğitim durumunu tek başına temsil etmez",
    "Anıttaki Sessizlik": "duvardaki isimler ortak belleği görünür kılarken her ismin ayrı yaşam öyküsü olduğu vurgulanır",
    "Apartman Toplantısı": "söz sırası ve ortak ölçüt tablosu, kişisel çatışmayı izlenebilir karar sürecine dönüştürür",
    "Sınıf Mesaj Grubu": "yazıda ses tonunun görünmemesi, tepki vermeden önce niyeti açıklığa kavuşturma gereğini doğurur",
    "Kayıp Cüzdan": "açık adres paylaşmamak ve teslim tutanağı almak, yardım ile kişisel veri sorumluluğunu dengeler",
    "Sessiz Kütüphane": "konuşma odasının saatlerini kullanmak, yalnız yasak koymadan ortak kullanım sorununa uygulanabilir çözüm üretir",
    "Ebru Teknesi": "aynı tekniğin her baskıda benzersiz iz bırakması, süreç benzerliği ile ürün özdeşliğini ayırır",
    "Çini Atölyesi": "renk yanında tekrar, simetri, kompozisyon ve kaynak notu kullanmak sanat ürününü çok ölçütlü inceler",
    "Bağlamanın Sesi": "nota dizisi büyük ölçüde sabitken tempo ve vurgu değişimi, ses kullanımının duyguya etkisini gösterir",
    "Gölge Oyunu": "ışığa uzaklık, hareket, duraklama ve seyirci ilişkisi birlikte anlam üreten çoklu anlatım ögeleridir",
    "Gezici Kütüphane": "ödünç sayısındaki artış erişimi gösterirken tür çeşitliliği eksikliği hizmet kalitesinin ayrı ölçütüdür",
    "Kitap Kulübü": "farklı yorumların metinden cümlelerle desteklenmesi, görüş ayrılığını kanıta dayalı karşılaştırmaya dönüştürür",
    "Dijital Okuma": "bildirimleri kapatmak ve yalnız amaçla ilgili bağlantıları açmak, dikkat dağınıklığına hedefli strateji sunar",
    "Mahalle Kitaplığı": "bağışları konu ve düzeye göre ayırmak, raf sayısını nitelik ve kullanılabilirliğin önüne geçirmez",
    "Okul Temsilcisi Seçimi": "eşit süre, gizli oy, açık sayım ve önceden duyurulan itiraz yolu demokratik süreci birlikte kurar",
    "Erişilebilir Park": "rampanın tek başına yetmemesi ve kullanıcı denemesi, erişilebilirliği farklı ihtiyaçlarla sınar",
    "Temiz Dere Başvurusu": "tarihli gözlem ile başvuru numarası, çevre sorununu kanıt ve izleme basamaklarına bağlar",
    "Kişisel Veri Afişi": "resmî kaynak ve güncelleme tarihi, güvenlik önerisinin kaynağını ve güncelliğini denetlenebilir kılar",
}

CHANNEL_ACTIONS = {
    "Dinleme/İzleme": "işitsel ve görsel kaydı amaçlı biçimde izleme",
    "Konuşma": "sözlü üretimi dinleyiciye göre planlama",
    "Okuma": "yazılı kayıttaki kanıtları amaçlı biçimde okuma",
    "Yazma": "yazılı üretimi yapı ve okur etkisine göre düzenleme",
}


def theme_number(note: dict[str, Any]) -> int:
    match = re.search(r"tema-(\d+)", str(note.get("unitKey")))
    if not match:
        raise ValueError(note["id"])
    return int(match.group(1))


def profile(title: str, passage: str) -> tuple[str, str, str, list[str], str]:
    low = title.casefold()
    if "materyal seçimini" in low:
        return ("Materyal; amaç, düzey, güvenilir kaynak ve erişilebilirlik ölçütlerini birlikte karşılamalıdır.", "Başlık ve görünüme göre değil amaçla ilgili içerik, kaynak künyesi ve sunum niteliğine göre seçim yapılmalıdır.", "Metindeki kaynak ve kapsam işaretleri, yalnız ilgi çekici olmanın yeterli olmadığını gösterir.", ["En renkli materyal her amaç için en güvenilir kaynaktır.", "Kaynak ve hedef kitle materyal seçimini etkilemez.", "Tek bir başlık içeriğin doğruluğunu kesin kanıtlar."], "Materyal seçimi amaçla ilgili, güvenilir, düzeye uygun ve kullanılabilir kaynak karşılaştırmasına dayanır.")
    if "strateji" in low or "yöntem" in low:
        return ("Strateji; amaç, metin türü ve karşılaşılan güçlüğe göre seçilip süreçte değiştirilebilir.", "Ön izleme, not alma, soru sorma, yeniden okuma veya dinleme seçeneklerinden göreve uygun olanı kullanmak gerekir.", "Amaçla uyumlu stratejinin eksik bilgiyi görünür kılması, tek yöntemin her durumda yeterli olmadığını gösterir.", ["Aynı strateji her metin ve amaçta değiştirilmeden kullanılmalıdır.", "Anlama güçlüğü oluştuğunda strateji değiştirmek başarısızlıktır.", "Not alma, soru sorma ve yeniden inceleme amaçla ilişkisizdir."], "Strateji seçimi görevin gerektirdiği bilgiye ve öz izleme sonucuna göre yapılır.")
    if "öz yansıtma" in low or "kendini uyarlayabilme" in low:
        return ("Öz yansıtma; güçlü yönü, somut güçlüğü, kullanılan kanıtı ve uygulanabilir sonraki adımı belirler.", "Genel beğeni cümlesi yerine neyin anlaşıldığını, nerede zorlanıldığını ve hangi stratejinin değişeceğini yazmak gerekir.", "Belirli bir güçlüğe karşı belirli bir sonraki adım seçilmesi, yansıtmanın performansı geliştirmeye dönük olduğunu gösterir.", ["Çalışmayı bitirmek hiçbir iyileştirme gerekmeyeceğini kanıtlar.", "Öz yansıtmada kanıt ve sonraki adım bulunması gerekmez.", "Yalnız 'güzeldi' demek bütün süreci ayrıntılı değerlendirir."], "Yansıtma, gözlenebilir performans kanıtı ile gerçekçi iyileştirme kararını bağlar.")
    if "anlamını bilmediği" in low or "söz varlığını geliştirmeye" in low:
        return ("Bilinmeyen sözün anlamı yakın cümle, karşıtlık, örnek, kök-ek ve metnin bütünü gibi ipuçlarıyla tahmin edilir.", "Sözcüğü çevreleyen ifadeleri inceleyip tahmini sözlük veya yeni bir bağlamla doğrulamak gerekir.", "Sözcüğün olay içindeki işlevi, ilk akla gelen ilgisiz anlam yerine bağlama uygun anlamı destekler.", ["Bilinmeyen sözcüğün anlamı yalnız harf sayısından bulunur.", "İlk tahmin metinle çelişse de değiştirilemez.", "Bağlam ve sözlük doğrulaması söz varlığı gelişimini engeller."], "Söz varlığı çözümlemesi bağlamdan tahmin ve güvenilir doğrulamayı birlikte içerir.")
    if "yüzey anlam" in low:
        return ("Yüzey anlam; metinde açıkça verilen kişi, yer, zaman, olay ve bilgi ilişkilerinden oluşur.", "Yanıtı metinde doğrudan bulunan ayrıntılarla sınırlayıp yorum ile açık bilgiyi ayırmak gerekir.", "Tarihli ve açık eylem kayıtları, metinde söylenmeyen niyetleri kesinleştirmeden yüzey anlamı kurar.", ["Metinde açıkça verilmeyen her niyet yüzey anlamın parçasıdır.", "Kişi, zaman ve olay ayrıntıları yüzey anlamı belirlemez.", "Okurun kişisel deneyimi metindeki açık bilgiyi değiştirebilir."], "Yüzey anlam metnin açık göstergelerine dayanır; çıkarım ayrı bir işlem olarak tutulur.")
    if "bölümlerini" in low or "yapılandırabilme" in low or "içerik ve yapıya" in low:
        return ("Metin veya konuşma; amaca uygun giriş, geliştirme ve sonuç bölümlerinde tutarlı bir akış kurar.", "Ana düşünceyi girişte belirginleştirip kanıt ve örnekleri geliştirmede, sonucu ve çağrıyı kapanışta düzenlemek gerekir.", "Bilginin girişten kanıta ve sonuca ilerlemesi, rastgele sıralamaya göre anlamı daha izlenebilir kılar.", ["Sonuç cümlesi girişten önce verilince her metin daha açık olur.", "Bölümler arasında konu ve bağlantı bulunması gerekmez.", "Örnekler ana düşünceyle ilişkilendirilmeden sıralanmalıdır."], "Yapı seçimi amaç, metin türü, ana düşünce ve bağlantıların düzenli ilerleyişine dayanır.")
    if "önemli bilgileri" in low or "anahtar kelimeleri" in low:
        return ("Önemli bilgi ve anahtar kelime, metnin konusunu ve ana düşüncesini taşıyan tekrar veya ilişki örüntülerinden belirlenir.", "Ayrıntıları ana düşünceye katkılarına göre ayırıp metnin kavram ağını taşıyan sınırlı sayıda sözcük seçmek gerekir.", "Kaynak, amaç ve sonuçla bağlantılı ifadeler ana düşünceyi taşırken dekoratif ayrıntılar ikincil kalır.", ["Metindeki bütün sözcükler eşit ölçüde anahtar kelimedir.", "En uzun sözcük her zaman en önemli bilgiyi gösterir.", "Ana düşünceyle ilişki kurmak bilgi seçiminde gereksizdir."], "Bilgi seçimi metin yapısı, ana düşünce ve kavramlar arası bağla gerekçelendirilir.")
    if "düşünceyi geliştirme" in low:
        return ("Tanımlama, örneklendirme, karşılaştırma, tanık gösterme ve sayısal veriler düşünceyi farklı yollarla geliştirir.", "İddiaya uygun geliştirme yolunu seçip örnek veya verinin kaynağını ve iddiayla bağını açıkça kurmak gerekir.", "Somut örnek ve ölçülü verinin iddiayı açıklaması, ilgisiz ayrıntının kanıt sayılamayacağını gösterir.", ["Her kişisel görüş sayısal veri olarak adlandırılır.", "Örnek, açıklanan düşünceyle ilgisiz olsa da kanıttır.", "Karşılaştırmada ortak ölçüt kullanmak gereksizdir."], "Düşünceyi geliştirme yolu, iddianın ne tür açıklama veya kanıta ihtiyaç duyduğuna göre seçilir.")
    if "söz sanat" in low:
        return ("Söz sanatı; sözcüklerin bağlamdaki ilişkisiyle benzetme, kişileştirme, konuşturma veya abartma etkisi kurar.", "İfadeyi gerçek anlam, benzetilen özellik ve insana özgü eylem bakımından çözümlemek gerekir.", "İnsan özelliğinin insan dışı bir varlığa aktarılması kişileştirme kanıtı oluşturur; yalnız şiirsel ses yeterli değildir.", ["Her mecazlı ifade aynı anda bütün söz sanatlarını içerir.", "Kişileştirme için insan dışı varlığa insan özelliği verilmez.", "Söz sanatı metindeki sözcük ilişkilerinden bağımsız belirlenir."], "Söz sanatı adı, metindeki dilsel kanıt ve kurduğu anlam etkisiyle eşleştirilir.")
    if "ikna etme" in low:
        return ("İkna tekniği; kanıt, uzman görüşü, duygu, tekrar veya sosyal onay gibi araçların hedef kitleyi nasıl yönlendirdiğiyle belirlenir.", "İddia, dayanak, hedef kitle ve kullanılan duygusal ya da mantıksal tekniği ayrı ayrı incelemek gerekir.", "Kaynaklı veri ile yalnız korku uyandıran sözün farklı işlevi, bütün ikna yollarının eş değer kanıt olmadığını gösterir.", ["Duygusal ifade her durumda doğruluğu kanıtlar.", "Uzman adı verilmesi kaynağı kontrol etmeyi gereksiz kılar.", "İkna tekniği ile hedef kitle arasında ilişki yoktur."], "İkna çözümlemesi mesajın tekniğini, kanıt kalitesini ve hedef kitle üzerindeki etkisini ayırır.")
    if "medya" in low or "çoklu ortam" in low or "görselle" in low:
        return ("Metin, görsel, ses ve grafik aynı iletiyi desteklemeli; kaynak, ölçek, başlık ve kurgu tercihleri anlamı etkiler.", "Aşağıdaki şemadaki ögeleri amaç, kaynak, veri uyumu ve hedef kitle ölçütleriyle birlikte incelemek gerekir.", "Şemadaki kaynaklı metin ile ölçülü gösterimin aynı eğilimi taşıması, çoklu ortam ögelerinin birbirini desteklediğini gösterir.", ["Görsel çekici olduğunda metin ve kaynakla çelişmesi önemsizdir.", "Grafikte ölçek ve kaynak bilgisi anlamı hiçbir zaman etkilemez.", "Çoklu ortamda her öge birbirinden bağımsız ve amaçsız seçilir."], "Çoklu ortam anlamı, ögeler arası uyum ve sunum tercihlerinin eleştirel çözümlemesiyle belirlenir.")
    if "tahmin" in low:
        return ("Tahmin başlık, görsel, önceki bölüm ve ön bilgiden hareketle kurulur; yeni kanıt geldiğinde güncellenir.", "Tahmini kesin gerçek saymadan dayandığı ipucunu belirtmek ve metin ilerledikçe doğrulamak gerekir.", "Yeni ayrıntının ilk tahmini değiştirmesi, tahminin kanıta açık geçici bir düşünme aracı olduğunu gösterir.", ["Tahmin bir kez yapıldıktan sonra metinle çelişse de değişmez.", "Başlık ve önceki bilgiler tahmin kurmada kullanılamaz.", "Kanıtsız her olasılık metnin kesin sonucu sayılır."], "Tahmin, açık ipucuna dayanır ve sonraki bilgiyle doğrulanıp uyarlanır.")
    if "basit çıkarım" in low or "üst düzey çıkarım" in low or "derin anlam" in low:
        return ("Çıkarım, metindeki birden çok ipucunu ön bilgiyle ilişkilendirir; çıkarımın kapsamı kanıtı aşmaz.", "Kişi davranışı, neden-sonuç, ton ve tekrar eden ayrıntıları birleştirip alternatif açıklamaları elemek gerekir.", "Birden çok bağımsız ipucunun aynı yorumu desteklemesi, tek sözcüğe dayalı kesin yargıdan daha güçlüdür.", ["Metinde tek sözcük görmek bütün gizli nedenleri kesinleştirir.", "Çıkarım için metinsel kanıt göstermek gerekmez.", "Okurun istediği her yorum metinle eşit ölçüde desteklenir."], "Derin anlam, metinsel ipuçları arasında gerekçeli bağ kurularak ve belirsizlik korunarak belirlenir.")
    if "sınıflandır" in low:
        return ("Sınıflandırma, ortak ve ayırt edici özelliklere dayanan açık, tutarlı ve amaca uygun ölçüt gerektirir.", "Ögeleri önce aynı ölçütle inceleyip her grubun nedenini ve sınırda kalan örneği açıklamak gerekir.", "Aynı ölçüte göre oluşan grupların yeniden uygulanabilmesi, rastgele adlandırmadan daha güvenilir sınıflandırma sağlar.", ["Her öge için farklı ölçüt kullanmak tutarlı sınıflandırmadır.", "Grupların ortak özelliğini açıklamak gereksizdir.", "Bir öge görünüşüne göre aynı anda çelişkili gruplara konmalıdır."], "Sınıflandırma ölçütü bütün ögelere eşit uygulanır ve grup özellikleriyle gerekçelendirilir.")
    if "karşılaştır" in low:
        return ("Karşılaştırma aynı ölçüt üzerinden benzerlik ve farklılığı kanıtlarıyla birlikte gösterir.", "İki unsur için ortak amaç, yapı, dil veya sonuç ölçütü seçip her yargıyı metinden örnekle desteklemek gerekir.", "Aynı ölçütte farklı sonuçların görünmesi, yalnız bir unsuru betimlemenin karşılaştırma olmadığını gösterir.", ["İki unsur farklı ölçütlerle anlatılırsa karşılaştırma tamamlanır.", "Yalnız benzerlik yazmak bütün farkları da açıklar.", "Karşılaştırmada metinsel kanıt ve ortak ölçüt gerekmez."], "Geçerli karşılaştırma, eş ölçüt ve iki tarafa ait doğrulanabilir kanıt kullanır.")
    if "özet" in low:
        return ("Özet, ana düşünce ve temel gelişmeleri özgün sırayla, ayrıntı ve kişisel yorumdan arındırarak aktarır.", "Metnin yapı ve anahtar kelimelerinden yararlanıp tekrar, örnek ve süsleyici ayrıntıları elemek gerekir.", "Kişi, temel sorun ve sonuç ilişkisinin korunması; uzun ayrıntı listesinden daha kapsayıcı bir özet oluşturur.", ["Özet metindeki her cümleyi aynı uzunlukta tekrarlar.", "Özete metinde bulunmayan kişisel yargılar eklenmelidir.", "Ana düşünce çıkarılıp yalnız ayrıntılar sıralanır."], "Özetleme, metnin anlam omurgasını kısaltırken olay ve düşünce ilişkisini korur.")
    if "hikâye unsurlarını" in low:
        return ("Öyküleyici metin kişi, olay, yer, zaman, çatışma ve çözüm ilişkisiyle yapılandırılır.", "Unsurları ayrı ayrı belirleyip olayın başlangıç, düğüm ve çözümündeki işlevlerini ilişkilendirmek gerekir.", "Kişinin amacı ile karşılaştığı engelin olay akışını yönlendirmesi, dekoratif betimlemeden farklı bir hikâye unsurudur.", ["Metinde adı geçen her nesne ana karakterdir.", "Yer ve zaman olayın anlamını hiçbir zaman etkilemez.", "Çatışma ile çözüm aynı işlevi taşır."], "Hikâye unsurları ad listesi olarak değil olay örgüsündeki işlevleriyle çözümlenir.")
    if "yorum" in low or "değerlendir" in low or "eleştir" in low:
        return ("Yorum anlamı açıklar; değerlendirme ölçüte göre değer biçer; eleştiri güçlü ve geliştirilecek yönleri kanıtla tartışır.", "Yargının türünü belirleyip açık ölçüt, metinsel kanıt ve uygulanabilir gerekçe kullanmak gerekir.", "Metinden örnek ve ölçüt içeren yargı, kişiye yönelik gerekçesiz beğeni veya saldırıdan ayrılır.", ["Kişisel beğeni tek başına ayrıntılı kanıta dayalı eleştiridir.", "Değerlendirmede ölçüt ve örnek kullanmak gereksizdir.", "Eleştiri yalnız olumsuz söz söylemekten oluşur."], "Yorum, değerlendirme ve eleştiri amaçlarına uygun kanıt ve saygılı gerekçeyle ifade edilir.")
    if "probleme çözüm" in low or "problem çözüm" in low:
        return ("Problem çözümü; sorunu, nedenleri, etkilenenleri, seçenekleri ve başarı göstergesini kanıtla ilişkilendirir.", "Sorunu açıkça tanımlayıp birden çok çözümü uygulanabilirlik ve etki ölçütleriyle karşılaştırmak gerekir.", "Çözüm sonrasında aynı göstergenin izlenmesi, ilk fikri kanıtsız uygulamaktan daha güvenilir sonuç verir.", ["Aklımıza gelen ilk çözüm her durumda en iyi çözümdür.", "Sorunun nedenini ve etkilenenleri belirlemek gereksizdir.", "Çözüm uygulandıktan sonra sonuç izlenmemelidir."], "Problem çözme süreci tanım, kanıt, seçenek, uygulama ve izleme basamaklarını kapsar.")
    if "yazım kuralları" in low or "noktalama" in low:
        return ("Yazım ve noktalama, sözcüklerin biçimini ve cümleler arasındaki anlam ilişkisini okura açık gösterir.", "Cümleyi büyük harf, özel ad, birleşik-ayrı yazım ve noktalama işlevleri bakımından bütünüyle denetlemek gerekir.", "Virgülün ara sözü, iki noktanın açıklamayı ve noktanın tamamlanan yargıyı belirtmesi anlam akışını netleştirir.", ["Noktalama yalnız metnin görünüşünü değiştirir, anlamı etkilemez.", "Özel adlar ve cümle başlangıçları küçük harfle yazılmalıdır.", "Her duraklama yerine aynı noktalama işareti kullanılabilir."], "Yazım ve noktalama seçimi kural kadar cümlede kurduğu anlam ve yapı ilişkisiyle doğrulanır.")
    if "sesini" in low or "beden dilini" in low or "sunum" in low or "geçiş ve bağlantı" in low:
        return ("Sözlü sunumda ses, vurgu, durak, beden dili, mekân ve geçiş ifadeleri amaç ve dinleyiciyle uyumlu olmalıdır.", "Ana noktaları belirleyip sesi anlam birimlerine göre kullanmak, görsel ve hareketi içeriği destekleyecek ölçüde seçmek gerekir.", "Vurgu ile geçişin düşünce değişimini görünür kılması, sürekli yüksek ses ve rastgele hareketten daha anlaşılırdır.", ["Sürekli yüksek ses kullanmak bütün konuşmaları etkili yapar.", "Beden dili konuşmanın içeriğiyle çelişse de anlam değişmez.", "Geçiş ifadeleri düşünceler arasındaki ilişkiyi kurmaz."], "Sözlü anlatım ögeleri gösteriş için değil anlam, dinleyici ve mekân gereksinimi için düzenlenir.")
    if "konuşma" in low:
        return ("Konuşma; amaç, dinleyici, içerik, süre, söz sırası ve geri bildirim kararlarının yönetildiği bir süreçtir.", "Ana düşünceyi ve desteklerini planlayıp dinleyicinin tepkisine göre açıklama, örnek veya konuşma hızını uyarlamak gerekir.", "Açık amaç ve düzenli kanıtın dinleyici sorularını karşılaması, hazırlığın ezberden ibaret olmadığını gösterir.", ["Konuşmada amaç ve dinleyici belirlemek gereksizdir.", "Hazırlıksız konuşma hiçbir düzen veya kanıt gerektirmez.", "Geri bildirim konuşma sürecini geliştiremez."], "Konuşma yönetimi hazırlık, üretim, etkileşim ve öz değerlendirme kararlarını birlikte içerir.")
    if "yaz" in low:
        return ("Yazma; amaç ve hedef kitleye göre planlama, taslak, gözden geçirme, düzenleme ve paylaşma aşamalarını içerir.", "Ana düşünceyi, yapıyı ve kanıtı planlayıp taslağı içerik, dil ve okur etkisi bakımından yeniden düzenlemek gerekir.", "Taslak ile son metin arasındaki gerekçeli değişiklikler, yazmanın tek seferlik bir ürün olmadığını gösterir.", ["İlk taslak her zaman yayıma hazır son metindir.", "Hedef kitle ve amaç sözcük seçimini etkilemez.", "Gözden geçirmede yalnız yazı tipi değiştirilir."], "Yazma süreci içerik, yapı, dil ve geri bildirime dayalı geliştirme adımlarını kapsar.")
    return ("Dil becerisi; amaç, bağlam, metin kanıtı ve hedef kitle arasındaki ilişkinin bilinçli yönetilmesini gerektirir.", "Verilen metindeki açık kanıtları belirleyip görevin istediği dil eylemini bu kanıtlarla gerçekleştirmek gerekir.", "Metin kanıtı ile seçilen eylemin uyumu, rastgele veya yalnız kişisel beğeniye dayalı karardan daha güçlüdür.", ["Dil görevi metin ve amaçtan bağımsız rastgele yapılabilir.", "Kanıt göstermek ve hedef kitleyi düşünmek gereksizdir.", "İlk karar yeni bilgi geldiğinde hiçbir zaman değiştirilemez."], "Dil becerisi kararı amaç, kaynak, kanıt ve öz denetimle gerekçelendirilir.")


def visual_figure(qid: str, labels: dict[str, str], theme: int, variant: int) -> dict[str, Any]:
    base = qid.replace("-", ".")
    left, right, alt = f"{base}.left", f"{base}.right", f"{base}.alt"
    labels[left] = ("Kaynağı ve tarihi belirtilen kısa açıklama" if variant % 2 == 0 else "Ana düşünceyi taşıyan metin bölümü")
    labels[right] = ("Aynı eğilimi ölçülü biçimde gösteren veri ögesi" if variant % 2 == 0 else "Metni tamamlayan kaynaklı görsel öge")
    labels[alt] = f"Tema {theme} bağlamında metin ögesi ile onu destekleyen görsel veri ögesi arasındaki ilişkiyi gösteren şema."
    return {"kind": "diagram", "viewBox": [0, 0, 100, 60], "elements": [
        {"type": "rect", "style": "plain", "x": 5, "y": 14, "w": 38, "h": 32, "fill": "surface", "stroke": "ink", "labelKey": left},
        {"type": "line", "style": "plain", "x1": 44, "y1": 30, "x2": 56, "y2": 30, "stroke": "blue"},
        {"type": "rect", "style": "plain", "x": 57, "y": 14, "w": 38, "h": 32, "fill": "surface", "stroke": "ink", "labelKey": right},
    ], "altTextKey": alt, "notToScale": True}


def make_case(note: dict[str, Any], variant: int) -> tuple[Any, ...]:
    theme = theme_number(note)
    heading, passage = CONTEXTS[theme][variant % 4]
    concept, action, inference, wrongs, rationale = profile(str(note["title"]), passage)
    visual = "görselle" in str(note["title"]).casefold() or "çoklu ortam" in str(note["title"]).casefold()
    scenario = (f"Aşağıdaki şemayla birlikte '{heading}' başlıklı özgün içerik inceleniyor. Metin kaydı şöyledir: {passage}" if visual else f"'{heading}' başlıklı özgün metin/dinleme kaydı şöyledir: {passage}")
    evidence = f"Kayıtta başlık, olay veya düşünce akışı ve kaynak sınırı birlikte veriliyor; görev özellikle '{note['title']}' becerisine odaklanıyor."
    return note["id"], scenario, evidence, concept, action, inference, wrongs, rationale


def transform(value: Any, batch: int) -> Any:
    if isinstance(value, str):
        return value.replace(f"tr-g06-bank-bty-b{batch:02d}", f"tr-g07-bank-turkce-b{batch:02d}").replace(f"tr.g06.bank.bty.b{batch:02d}", f"tr.g07.bank.turkce.b{batch:02d}")
    if isinstance(value, list): return [transform(x, batch) for x in value]
    if isinstance(value, dict): return {k: transform(v, batch) for k, v in value.items()}
    return value


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1400:
        raise RuntimeError(f"batches 15–20 expect 1400 records, found {len(existing)}")
    notes = list(read_notes_only(SOURCE).values())
    if len(notes) != 152:
        raise RuntimeError(f"expected 152 notes, found {len(notes)}")
    assignments = (notes + notes + notes + notes[:144])[:600]
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    seen: defaultdict[str, int] = defaultdict(int)
    rows = []
    for offset, note in enumerate(assignments):
        batch = 15 + offset // 100
        local = offset % 100 + 1
        mode = MODES[local - 1]
        variant = seen[note["id"]]
        seen[note["id"]] += 1
        case = make_case(note, variant)
        row = make_question(local, case, mode, LEVEL_SEQUENCE[local - 1], note, labels, "Türkçe", batch_number=batch, number_base=(batch - 1) * 100)
        row = transform(row, batch)
        row["grade"] = 7
        row["title"] = f"{note['title']} — {batch}. özgün üretim partisi"
        theme = theme_number(note)
        heading, passage = CONTEXTS[theme][variant % 4]
        channel = str(note.get("topic") or "Türkçe")
        channel_action = CHANNEL_ACTIONS.get(channel, "Türkçe dil eylemini kanıtla gerçekleştirme")
        concrete_decision = CONTEXT_DECISIONS[heading]
        skill_anchor = f"özel beceri odağı {str(note['title']).casefold()}; kanal eylemi {channel_action}"
        evidence_anchor = (
            f"Bu görevde '{heading}' kaydındaki kanıt, {channel} alanında "
            f"{str(note['title']).casefold()} hedefi için kullanılmaktadır."
        )
        row["question"] = row["question"].rstrip() + " " + evidence_anchor
        if passage not in row["question"]:
            row["question"] += f" Metin kanıtı: {passage}"
        correct_index = int(row["correctIndex"])
        contextual_correct = (
            str(row["choices"][correct_index]).rstrip() +
            f" Somut bağlam kararı: {concrete_decision}. Bu seçimde {skill_anchor}."
        )
        row["choices"][correct_index] = contextual_correct
        row["correctOption"] = contextual_correct
        row["distractorWhy"][correct_index] = (
            str(row["distractorWhy"][correct_index]).rstrip() +
            f" Bağlamsal doğrulama: '{heading}' kaydı ve {note['title']} hedefi aynı seçenekte karşılanır."
        )
        row["explanation"] = (
            str(row["explanation"]).rstrip() +
            f" '{heading}' kaydının açık ayrıntıları, {channel} alanındaki {note['title']} becerisinin "
            f"hangi kanıtla uygulandığını somutlaştırır. {skill_anchor.capitalize()}. "
            f"Kayıt için belirleyici çözümleme şudur: {concrete_decision}. Bağlam kaydı şöyledir: {passage}"
        )
        is_visual = "görselle" in str(note["title"]).casefold() or "çoklu ortam" in str(note["title"]).casefold()
        if is_visual:
            qid = row["id"]
            row["figure"] = visual_figure(qid, labels, theme_number(note), variant)
            row["visualRequirement"] = "required"
            row["visualNeed"] = {"level": "required", "role": "evidence", "rationale": "Metin ve görsel öge arasındaki anlam ilişkisi yalnız yapılandırılmış şemada gösterilmektedir.", "acceptableKinds": ["diagram"], "evidenceDimensions": ["metin ögesi", "görsel öge", "kaynak uyumu"]}
            row["question"] = row["question"].replace("Aşağıdaki tabloda", "Aşağıdaki şemada")
            row["question"] = "Aşağıdaki şemada verilen kanıtı kullanınız. " + row["question"]
        rows.append(row)
    for batch in range(15, 21):
        part = rows[(batch - 15) * 100:(batch - 14) * 100]
        if Counter(row["correctIndex"] for row in part) != Counter({0: 25, 1: 25, 2: 25, 3: 25}): raise AssertionError(f"batch {batch} answer balance")
        if Counter(row["questionType"] for row in part) != Counter({"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}): raise AssertionError(f"batch {batch} mode balance")
    # Convert labels emitted by generic qids for each Turkish batch.
    fixed_labels = {}
    for key, value in labels.items():
        new_key, new_value = key, value
        for batch in range(15, 21):
            new_key, new_value = transform(new_key, batch), transform(new_value, batch)
        fixed_labels[new_key] = new_value
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + rows) + "\n", encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(fixed_labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"grade": 7, "batches": "15-20", "questions": 600, "turkish": 600, "total": 2000, "objectives": len({(n.get('objectives') or [n.get('objective')])[0] for n in notes}), "figures": sum(bool(row.get("figure")) for row in rows), "sourceQuestionReads": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__": raise SystemExit(main())
