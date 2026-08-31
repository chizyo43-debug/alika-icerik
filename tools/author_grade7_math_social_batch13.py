#!/usr/bin/env python3
"""Append Grade 7 batch 13: 9 Mathematics and 91 Social Studies items."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re
from typing import Any

from author_grade6_mixed_batch03 import LEVEL_SEQUENCE, make_question, read_notes_only
from author_grade7_dkab_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade7_math_batch11 import CASES as MATH_BASES


MATH_SOURCE = Path("turkiye/7-sinif/matematik/matematik-tum.jsonl")
SOCIAL_SOURCE = Path("turkiye/7-sinif/sosyal-bilgiler/sosyal-bilgiler-tum.jsonl")
MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
MATH_POSITIONS = {1, 2, 26, 27, 28, 61, 62, 86, 87}
FOCI = ("kaynak karşılaştırması", "neden-sonuç zinciri", "hak ve sorumluluk dengesi", "kanıtın temsil gücü", "zaman ve bağlam sınırı", "çoklu bakış açısı")


SOCIAL_CASES = [
    ("tr-g07-sosyal-note-sb-7-1-1", "Bir öğrenci meclisi toplantısında aynı anda konuşma, kişiye yönelik eleştiri ve belirsiz görev dağılımı nedeniyle karar alınamıyor.", "İkinci toplantıda söz sırası, etkin dinleme, ben dili, açık görev ve geri bildirim ilkeleri uygulanınca ortak karar kayda geçiyor.", "Etkili iletişim yalnız konuşmak değil; dinleme, empati, açık ifade, uygun kanal ve geri bildirimle ortak anlam kurmaktır.", "Sorunu kişiden ayırıp söz hakkını eşit dağıtan, mesajı açıklığa kavuşturan ve kararı geri bildirimle doğrulayan süreç kurulmalıdır.", "İkinci toplantıdaki ilerleme, iletişim ilkelerinin grup kararını ve çatışma çözümünü desteklediğini gösterir.", ["Etkili iletişimde yalnız en yüksek sesle konuşan kişi karar verir.", "Geri bildirim mesajın anlaşılıp anlaşılmadığını belirlemede gereksizdir.", "Kişiye saldırmak sorun davranışını açıklamaktan daha yapıcıdır."], "İletişim süreci kaynak, alıcı, mesaj, kanal ve geri bildirim ilişkisiyle; saygı ve sorumluluk temelinde değerlendirilir."),
    ("tr-g07-sosyal-note-sb-7-1-2", "Okulun bilim sergisi üst katta yapılıyor; asansör çalışmıyor, yönergeler küçük puntolu ve işitme desteği bulunmuyor.", "Erişilebilir rota, büyük puntolu ve sesli içerik, işaret dili desteği ile ayarlanabilir masa önerileri ihtiyaç temelli olarak listeleniyor.", "Fırsat eşitliği herkese aynı aracı vermek değil, katılımı engelleyen koşulları makul düzenlemelerle gidermektir.", "Özel gereksinimli bireylerin görüşünü alıp fiziksel, iletişimsel ve dijital engelleri belirleyerek uygulanabilir düzenleme yapılmalıdır.", "Farklı desteklerin aynı etkinliğe bağımsız katılımı artırması, eşitlik ile hakkaniyetin birlikte düşünülmesi gerektiğini gösterir.", ["Herkese aynı küçük puntolu metni vermek fırsat eşitliğini kesin sağlar.", "Erişilebilirlik yalnız bina girişindeki rampadan ibarettir.", "Düzenleme yapılırken ilgili bireyin görüşünü almak gereksizdir."], "Erişilebilirlik kararı varsayıma değil ihtiyaç, katılım hakkı ve ilgili bireyin deneyimine dayanır."),
    ("tr-g07-sosyal-note-sb-7-1-3", "Bir doğal afet sonrasında farklı şehirlerden insanlar yardım kampanyasına katılıyor, doğrulanmış ihtiyaç listeleri izleniyor ve kamu kurumlarıyla koordinasyon kuruluyor.", "Gönüllüler ayni yardımı gelişigüzel göndermek yerine resmî duyurulara göre sınıflandırıyor; yanlış bilgi içeren paylaşımlar düzeltiliyor.", "Millî meseleler karşısındaki toplumsal tutum dayanışma, sorumluluk, doğru bilgi ve kurumlarla eşgüdüm içinde incelenebilir.", "Yardım davranışını ihtiyaç kanıtı, güvenilir duyuru, güvenlik ve adil dağıtım ölçütleriyle planlamak gerekir.", "Koordineli ve doğrulanmış yardımın daha düzenli ulaşması, dayanışmanın yalnız iyi niyet değil sorumlu örgütlenme gerektirdiğini gösterir.", ["Afet sırasında kaynağı belirsiz her paylaşım hemen yayılmalıdır.", "Dayanışma kamu kurumları ve yerel ihtiyaçlarla koordinasyonu dışlar.", "Yardımın kime ve nasıl ulaştığını izlemek gereksizdir."], "Toplumsal dayanışma örnekleri genellemeci övgü yerine somut davranış, kaynak ve sonuç üzerinden yorumlanır."),
    ("tr-g07-sosyal-note-sb-7-2-1", "Bir mahallede çevrim içi alışveriş, uzaktan çalışma ve farklı ülkelerden kültürel içerik tüketimi on yılda yaygınlaşıyor.", "Yeni iş ve erişim fırsatları artarken yerel dükkân rekabeti, kişisel veri güvenliği ve kültürel tek tipleşme tartışmaları da kaydediliyor.", "Küreselleşme ekonomik, teknolojik ve kültürel bağlantıları artırır; etkileri tek yönlü değil fırsat ve riskleri birlikte içerir.", "Değişimi zaman içinde, farklı toplumsal gruplar ve en az iki etki alanı bakımından karşılaştırmak gerekir.", "Aynı süreçte erişim artışı ve yerel rekabet baskısının görülmesi, küreselleşmenin yalnız olumlu ya da yalnız olumsuz açıklanamayacağını gösterir.", ["Küreselleşme bütün toplumlarda aynı sonucu aynı hızla doğurur.", "Dijital bağlantıların ekonomi ve kültürle hiçbir ilişkisi yoktur.", "Tek bir kişinin deneyimi bütün toplum için kesin kanıttır."], "Küresel değişim çok boyutlu veri, zaman ve farklı grupların deneyimleriyle yorumlanır."),
    ("tr-g07-sosyal-note-sb-7-2-2", "Bölgesel bir deprem sonrası arama-kurtarma, geçici barınma ve sağlık desteği için uluslararası iş birliği gerekiyor.", "Türkiye'nin kamu kurumları, yardım kuruluşları ve uluslararası mekanizmalarla uzman ekip, sahra hastanesi ve lojistik destek sağlayabildiği örnekleniyor.", "Bölgesel ve küresel sorunlarda ülkelerin rolü diplomasi, insani yardım, teknik kapasite ve uluslararası iş birliği boyutlarıyla ele alınır.", "Sorunun türüne uygun kurum, uzmanlık ve yardım biçimini kaynaklı biçimde eşleştirip etkisini izlemek gerekir.", "Farklı kapasite türlerinin aynı insani amaç için eşgüdümü, rolün yalnız tek bir yardım kalemine indirgenemeyeceğini gösterir.", ["Küresel sorunlar hiçbir ülkenin iş birliği yapmasını gerektirmez.", "İnsani yardımda yerel ihtiyaç ve koordinasyon önemsizdir.", "Bir ülkenin rolü yalnız yaptığı açıklamaların sayısıyla ölçülür."], "Ülke rolü güncel sloganlarla değil kurum, eylem, iş birliği ve doğrulanabilir sonuçlarla özetlenir."),
    ("tr-g07-sosyal-note-sb-7-3-1", "Osmanlı Devleti'nin farklı dönemlerde uyguladığı iskân, tımar, hoşgörü, ticaret yolu güvenliği ve merkezî yönetim politikaları ilişki haritasına aktarılıyor.", "Politikaların fethedilen bölgelerde güvenlik, üretim, vergi düzeni ve yönetim sürekliliğiyle farklı biçimlerde bağlantı kurduğu görülüyor.", "Osmanlı'nın genişlemesi askerî başarı kadar yönetim, ekonomi, iskân ve yerel düzen politikalarının birlikte etkisiyle sorgulanır.", "Her politikayı uygulandığı dönem, amaç, araç ve kısa-uzun vadeli sonuçlarıyla kaynaklardan karşılaştırmak gerekir.", "Birden çok politikanın farklı işlevler üstlenmesi, cihan devleti sürecinin tek savaşa veya tek nedene bağlanamayacağını gösterir.", ["Osmanlı'nın büyümesinde yönetim ve ekonomi politikalarının hiçbir etkisi yoktur.", "Her politika bütün yüzyıllarda aynı biçimde uygulanmıştır.", "Tek bir zafer sonraki bütün gelişmeleri tek başına açıklar."], "Tarihsel açıklama çok nedenli, kronolojik ve kaynakların sınırını gözeten biçimde kurulur."),
    ("tr-g07-sosyal-note-sb-7-3-2", "Yeni askerî teknolojiler, ticaret yollarındaki değişim ve Avrupa'daki kurumlaşma karşısında Osmanlı'nın yenilik girişimleri inceleniyor.", "Matbaa, askerî ve eğitim kurumları, elçilikler ve idari düzenlemeler farklı dönem ve ihtiyaçlarla eşleştiriliyor.", "Osmanlı yenilikleri değişen güç dengelerine verilen, dönemlere göre amaç ve kapsamı farklılaşan cevaplar olarak yorumlanır.", "Yeniliğin nedenini, uygulama alanını, karşılaşılan güçlüğü ve sonucunu kronolojik kaynaklarla ayrı ayrı belirlemek gerekir.", "Farklı alanlarda yenilik yapılması, değişimin yalnız askerî bir başlıkla açıklanamayacağını gösterir.", ["Bütün yenilikler aynı padişah döneminde ve aynı nedenle yapılmıştır.", "Dış gelişmelerin Osmanlı yenilikleriyle hiçbir ilişkisi yoktur.", "Bir yenilik ilan edildiği anda bütün sorunları kalıcı çözer."], "Neden-sonuç ilişkisi anakronizmden kaçınarak dönem, kurum ve sonuç kanıtlarıyla kurulur."),
    ("tr-g07-sosyal-note-sb-7-3-3", "Öğrenciler bir Osmanlı şehrini mimari, vakıf, eğitim, sanat ve gündelik yaşam unsurlarıyla tanıtan dijital sergi hazırlıyor.", "Her görselin kaynağı, yapının işlevi, dönemi ve günümüzdeki korunma durumu künyeye ekleniyor; doğrulanmamış atıflar çıkarılıyor.", "Kültür ve medeniyet ürünü kaynaklı, bağlamlı, telif ve kültürel miras duyarlılığı taşıyan biçimde paylaşılmalıdır.", "Ürünün amacını ve hedef kitlesini belirleyip farklı unsurları güvenilir kaynak ve doğru künye ile ilişkilendirmek gerekir.", "Kaynak ve işlev bilgisinin sergiyi anlaşılır kılması, görsel süslemenin tek başına tarihsel ürün oluşturmadığını gösterir.", ["Kaynağı belirsiz her görsel tarihsel kanıt olarak kullanılabilir.", "Bir kültürü yalnız tek yapı ve tek dönem temsil eder.", "Telif, künye ve korunma bilgisi paylaşım kalitesini etkilemez."], "Tarihsel ürün içerik doğruluğu, kaynak şeffaflığı, temsil çeşitliliği ve etik paylaşım ölçütleriyle değerlendirilir."),
    ("tr-g07-sosyal-note-sb-7-4-1", "Bir vatandaşlık kartında Türkiye Cumhuriyeti'nin demokratik, laik ve sosyal bir hukuk devleti olma nitelikleri örnek durumlarla eşleştiriliyor.", "Seçim ve katılım demokratik; din ve vicdan özgürlüğü laik; sosyal destek sosyal devlet; işlemlerin hukuka bağlılığı hukuk devleti niteliğiyle ilişkilendiriliyor.", "Cumhuriyetin temel nitelikleri birbirini tamamlar ve somut kurum, hak, özgürlük ve sorumluluk örnekleriyle açıklanır.", "Bir örneği yalnız anahtar kelimeye değil hangi hak, kurum ve hukuk ilişkisini gösterdiğine göre sınıflandırmak gerekir.", "Farklı örneklerin ayrı niteliklerle ilişkilendirilmesi, kavramların aynı anlamda kullanılmadığını gösterir.", ["Hukuk devleti yöneticilerin hukukla bağlı olmadığı anlamına gelir.", "Laiklik din ve vicdan özgürlüğünü ortadan kaldırır.", "Sosyal devlet yalnız seçimlerin yapılmasını açıklar."], "Temel nitelikler Anayasa'daki anlamlarıyla ve hak temelli somut örneklerle özetlenir."),
    ("tr-g07-sosyal-note-sb-7-4-2", "Bir kamu hizmeti talebinin belediye, valilik, bakanlık ve yargı birimleri arasındaki yeri inceleniyor.", "Yerel ortak ihtiyaçlar belediye; ilde merkezî idare valilik; politika ve yürütme bakanlık; uyuşmazlıkların hukuki denetimi bağımsız yargı ile eşleştiriliyor.", "Devletin yönetim yapısı yasama, yürütme, yargı ile merkezî ve yerel yönetimlerin görev ve ilişkileri üzerinden çözümlenir.", "Sorunun niteliğine göre yetkili kurumu belirleyip kurumların görev sınırlarını ve denetim yollarını karıştırmamak gerekir.", "Aynı talebin farklı aşamalarda farklı kurumları ilgilendirmesi, yönetim yapısının tek bir makamdan oluşmadığını gösterir.", ["Belediye bütün ülkede kanun yapan yasama organıdır.", "Yargının görevi yürütme adına günlük kamu hizmeti sunmaktır.", "Merkezî ve yerel yönetim arasında hiçbir görev ayrımı yoktur."], "Yönetim şeması kurum adından çok anayasal işlev, yetki ve denetim ilişkisiyle okunur."),
    ("tr-g07-sosyal-note-sb-7-4-3", "Türkiye'de demokratik katılımın gelişimi seçim, çok partili hayat, kadınların siyasal hakları ve sivil toplum örnekleriyle zaman çizelgesinde inceleniyor.", "Her gelişme katılım, eşitlik, çoğulculuk ve hukukun üstünlüğü ilkelerinden biri veya birkaçıyla ilişkilendiriliyor.", "Demokrasi gelişimi tek olay değil, hakların ve katılım kanallarının zaman içinde genişlemesi ve kurumlaşmasıdır.", "Olayları kronolojik sıraya koyup hangi demokratik ilkeyi nasıl etkilediğini kaynakla açıklamak gerekir.", "Farklı gelişmelerin ayrı ilkeleri güçlendirmesi, demokrasinin yalnız sandık gününe indirgenemeyeceğini gösterir.", ["Demokrasi yalnız çoğunluğun hiçbir sınır olmadan karar vermesidir.", "Hakların genişlemesi ile demokratik gelişim arasında ilişki yoktur.", "Kronoloji ve tarihsel bağlam demokratik gelişimi yorumlamada gereksizdir."], "Demokratik gelişim, kurumlar kadar hak, katılım, çoğulculuk ve hukuk ilkeleriyle yorumlanır."),
    ("tr-g07-sosyal-note-sb-7-4-4", "Bir okul temsilci seçiminde adaylara eşit tanıtım süresi verilmiyor, oy gizliliği korunmuyor ve itiraz yolu açıklanmıyor.", "Sorunlar eşit yarışma, özgür tercih, gizli oy, şeffaf sayım ve etkili itiraz ölçütleriyle sınıflandırılıyor.", "Demokratik uygulamadaki sorunlar yalnız sonuçla değil sürecin özgürlük, eşitlik, şeffaflık ve hesap verebilirlik ilkelerine uygunluğuyla belirlenir.", "Her soruna ilgili demokratik ilkeyi geri kuran uygulanabilir çözüm ve denetim adımı önermek gerekir.", "Bir aday kazansa bile süreç ilkeleri ihlal ediliyorsa uygulamanın demokratik niteliği zedelenir.", ["Seçimin yapılmış olması bütün süreç sorunlarını kendiliğinden giderir.", "Gizli oy ve şeffaf sayım birbirine gereksiz iki uygulamadır.", "İtiraz hakkı demokratik süreçte hesap verebilirliği azaltır."], "Demokratik sorun çözümü ilke, süreç, kanıt ve başvuru yollarını birlikte ele alır."),
    ("tr-g07-sosyal-note-sb-7-5-1", "Bir bölgede sulama altyapısı, demiryolu bağlantısı, mesleki eğitim ve sağlık yatırımları birlikte planlanıyor.", "Üretim kapasitesi, pazara erişim, nitelikli iş gücü ve yaşam kalitesinde beklenen değişimler neden-sonuç ağına yerleştiriliyor.", "Millî kalkınma hamleleri ekonomik büyüme yanında beşerî, sosyal, bölgesel ve çevresel sonuçlarıyla yorumlanır.", "Yatırımın başlangıç ihtiyacını, doğrudan ve dolaylı etkilerini, zamanını ve sürdürülebilirlik göstergelerini ayırmak gerekir.", "Bir yatırım paketinin birden çok alanı etkilemesi, kalkınmanın yalnız gelir artışı olarak ölçülemeyeceğini gösterir.", ["Kalkınma yalnız bina sayısının artmasıdır.", "Her yatırım bütün bölgelerde aynı sonucu verir.", "Çevresel ve sosyal etkiler kalkınma değerlendirmesine katılmaz."], "Kalkınma ilişkisi çok boyutlu gösterge, bölgesel ihtiyaç ve uzun vadeli sonuçlarla değerlendirilir."),
    ("tr-g07-sosyal-note-sb-7-5-2", "Yerel meyve üreticileri hasat döneminde ürün kaybı yaşıyor; soğuk zincir ve dağıtım merkezi seçenekleri inceleniyor.", "Depolama kaybı azalınca pazara ulaşan miktarın arttığı, düzenli dağıtımın fiyat dalgalanmasını sınırlayabildiği fakat enerji maliyeti oluşturduğu kaydediliyor.", "Üretim, dağıtım ve tüketim birbirine bağlıdır; bir halkadaki verim, maliyet veya erişim değişimi diğer halkaları etkiler.", "Çözümü üretici geliri, kayıp oranı, tüketici erişimi, maliyet ve çevresel etki göstergeleriyle karşılaştırmak gerekir.", "Kayıp azalmasıyla arzın artması, dağıtım altyapısının üretim sonucunu ve tüketici erişimini birlikte etkilediğini gösterir.", ["Dağıtım koşulları üretim ve tüketimi hiçbir zaman etkilemez.", "Ürün miktarı artınca maliyet ve çevresel etki mutlaka sıfır olur.", "Ekonomik gelişmişlik yalnız tüketim miktarıyla ölçülür."], "Ekonomik döngü ilişkisi veri, maliyet, erişim ve sürdürülebilirlik boyutlarıyla çözümlenir."),
    ("tr-g07-sosyal-note-sb-7-6-1", "Otonom ulaşım, yapay zekâ destekli sağlık ve uzaktan çalışma teknolojilerinin 2040 kent yaşamına etkileri için senaryo çalışması yapılıyor.", "Her teknoloji için olası yarar, risk, etkilenen grup, gerekli beceri ve etik-hukuki düzenleme ayrı sütunlarda değerlendiriliyor.", "Gelecek öngörüsü kesin kehanet değil; mevcut eğilim, kanıt, varsayım ve alternatif senaryolara dayalı gerekçeli çıkarımdır.", "Eğilimi kaynakla belirleyip en az iki senaryo kurmak, fırsat ve riskleri farklı gruplar açısından değerlendirmek gerekir.", "Aynı teknolojinin erişim kolaylığı ve eşitsizlik riski doğurabilmesi, tek yönlü gelecek tahmininin yetersiz olduğunu gösterir.", ["Teknolojik gelişme bütün toplumsal sorunları kendiliğinden çözer.", "Gelecek hakkında öngörü için mevcut kanıt ve varsayım gerekmez.", "Bir teknolojinin etkisi bütün gruplar için zorunlu olarak aynıdır."], "Öngörü, belirsizliği açıklar; veri ve varsayımı birbirinden ayırarak alternatif sonuçları tartışır."),
    ("tr-g07-sosyal-note-sb-7-6-2", "Göç üzerine üç örnek metin nüfus dağılımını, bireysel uyumu ve geçmiş dönem göçlerini farklı sorularla inceliyor.", "Coğrafya mekânsal dağılıma, sosyoloji toplumsal ilişkilere, tarih zaman içindeki değişime odaklanıyor; ortak konu farklı yöntemlerle ele alınıyor.", "Sosyal bilimler insan ve toplumu farklı soru, ölçek, kaynak ve yöntemlerle inceler; alanlar gerektiğinde birlikte çalışabilir.", "Metnin sorduğu soruyu, kullandığı kanıtı ve analiz ölçeğini belirleyerek ilgili sosyal bilim alanını gerekçelendirmek gerekir.", "Aynı göç konusunun üç farklı odakla incelenmesi, alan ayrımının yalnız konu adına bakılarak yapılamayacağını gösterir.", ["Bir konu yalnız tek sosyal bilim alanınca incelenebilir.", "Sosyal bilim alanını belirlemede araştırma sorusu ve yöntem önemsizdir.", "Tarih yalnız geleceği, coğrafya yalnız bireysel duyguyu inceler."], "Alan genellemesi metindeki amaç, kaynak, zaman ve mekân odağına dayanır."),
    ("tr-g07-sosyal-note-sb-7-6-3", "Mahalle parkında akşam kullanımının azalması problemi bilimsel sorgulamayla inceleniyor.", "Aydınlatma ölçümü, farklı saatlerde kullanıcı sayımı, yaş gruplarıyla gönüllü görüşme ve güvenlik kayıtları etik izinlerle karşılaştırılıyor.", "Toplumsal problem sorgulaması açık soru, çoklu veri, etik toplama, analiz, sınırlılık ve kanıta dayalı öneri basamaklarını içerir.", "Problemi peşin hüküm kurmadan tanımlayıp nicel ve nitel veriyi aynı zaman ve yer sınırında toplamak gerekir.", "Birden çok kaynağın benzer saat ve noktaları göstermesi, önerinin yalnız kişisel izlenime göre kurulmasından daha güçlü kanıt sağlar.", ["İlk tahmin kanıt toplamadan kesin sonuç kabul edilmelidir.", "İnsanlarla ilgili veri toplanırken gönüllülük ve gizlilik gereksizdir.", "Tek bir gözlem bütün mevsimler için genellenebilir."], "Bilimsel sorgulama şeffaf yöntem, etik, kanıt çeşitliliği ve sınırlılık bildirimiyle yürütülür."),
]


def derive_social(base: tuple[Any, ...], occurrence: int) -> tuple[Any, ...]:
    note, scenario, evidence, concept, action, inference, wrongs, rationale = base
    focus = FOCI[occurrence % len(FOCI)]
    return (
        note,
        f"{scenario} Bu yeni değerlendirmede {focus} özellikle izleniyor.",
        f"{evidence} Kayıt ayrıca {focus} ölçütüne göre ikinci bir ekipçe doğrulanıyor.",
        f"{concept} {focus.capitalize()} bu kavramın bağlam dışına taşınmasını önler.",
        f"{action} Son karar {focus} bakımından gerekçelendirilip kaynağıyla kayda geçirilmelidir.",
        f"{inference} Bu çıkarım yalnız {focus} ve verilen kayıtların desteklediği sınırda geçerlidir.",
        [f"{wrongs[0]} {focus.capitalize()} sonucu değiştirmez.", f"{wrongs[1]} Tek örnek bütün dönem ve gruplara taşınabilir.", f"{wrongs[2]} Kaynak ile yorum arasındaki bağın açıklanması gerekmez."],
        f"{rationale} {focus.capitalize()} sayesinde olgu, yorum ve öneri birbirine karıştırılmaz.",
    )


def derive_math(base: tuple[Any, ...], occurrence: int) -> tuple[Any, ...]:
    note, scenario, evidence, concept, action, inference, wrongs, rationale = base
    return (note,
            f"Bir tasarım ekibi verilen matematiksel modeli farklı bir karar problemi için seçiyor: {scenario}",
            f"Model seçim kaydı şu kanıtı içeriyor: {evidence} Ekip ayrıca sonucun gerçek durumdaki anlamını ayrı satırda doğruluyor.",
            f"{concept} Bir model, yalnız işlem verdiği için değil sorulan niceliği ve koşulları temsil ettiği için uygundur.",
            f"{action} Sonucu ikinci bir temsil veya ters işlemle denetleyip modelin kullanım sınırını yazmak gerekir.",
            f"{inference} Bu sonuç, işlem ile bağlam aynı niceliği gösterdiği sürece seçilen modeli destekler.",
            [f"{wrongs[0]} Modelin bağlama uygunluğu incelenmez.", f"{wrongs[1]} Her matematiksel bağıntı bu probleme aynı sonucu verir.", f"{wrongs[2]} Birim ve sonuç aralığı model seçimini etkilemez."],
            f"{rationale} Tasarım kararı işlem, temsil, birim ve bağlamın birlikte doğrulanmasına dayanır.")


def transform(value: Any, subject: str) -> Any:
    if isinstance(value, str):
        slug = "matematik" if subject == "Matematik" else "sosyal-bilgiler"
        return value.replace("tr-g06-bank-bty-b13", f"tr-g07-bank-{slug}-b13").replace("tr.g06.bank.bty.b13", f"tr.g07.bank.{slug}.b13")
    if isinstance(value, list): return [transform(x, subject) for x in value]
    if isinstance(value, dict): return {k: transform(v, subject) for k, v in value.items()}
    return value


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1200:
        raise RuntimeError(f"batch 13 expects 1200 records, found {len(existing)}")
    math_notes, social_notes = read_notes_only(MATH_SOURCE), read_notes_only(SOCIAL_SOURCE)
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    social_occurrences: Counter[str] = Counter()
    math_index = social_index = 0
    rows = []
    for local, mode in enumerate(MODES, 1):
        if local in MATH_POSITIONS:
            base = MATH_BASES[math_index]
            math_index += 1
            case = derive_math(base, 0)
            note, subject = math_notes[case[0]], "Matematik"
        else:
            base = SOCIAL_CASES[social_index % len(SOCIAL_CASES)]
            social_index += 1
            occurrence = social_occurrences[base[0]]
            social_occurrences[base[0]] += 1
            case = derive_social(base, occurrence)
            note, subject = social_notes[case[0]], "Sosyal Bilgiler"
        row = make_question(local, case, mode, LEVEL_SEQUENCE[local - 1], note, labels, subject, batch_number=13, number_base=1200)
        row = transform(row, subject)
        row["grade"] = 7
        row["title"] = f"{note['title']} — 13. özgün üretim partisi"
        if subject == "Matematik":
            row["question"] += " Bu görevde ayrıca ikinci temsil ile ters işlemin aynı matematiksel kararı verip vermediği sorgulanmaktadır."
        rows.append(row)
    if Counter(row["subject"] for row in rows) != Counter({"Matematik": 9, "Sosyal Bilgiler": 91}): raise AssertionError(Counter(row["subject"] for row in rows))
    if Counter(row["correctIndex"] for row in rows) != Counter({0: 25, 1: 25, 2: 25, 3: 25}): raise AssertionError("answer balance")
    fixed_labels = {}
    for key, value in labels.items():
        match = re.search(r"\.b13\.q(\d{3})\.", key)
        label_subject = "Matematik" if match and int(match.group(1)) in MATH_POSITIONS else "Sosyal Bilgiler"
        fixed_labels[transform(key, label_subject)] = transform(value, label_subject)
    labels = fixed_labels
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + rows) + "\n", encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"grade": 7, "batch": 13, "questions": 100, "mathematics": 9, "socialStudies": 91, "total": 1300, "figures": sum(bool(row.get("figure")) for row in rows), "sourceQuestionReads": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__": raise SystemExit(main())
