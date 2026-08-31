#!/usr/bin/env python3
"""Append 100 independently authored Grade 6 science questions (batch 08)."""
from __future__ import annotations

from collections import Counter
import json

from author_grade6_bilisim_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade6_fen_batch07 import make_record, task
from author_grade6_mixed_batch03 import read_notes_only
from author_grade6_mixed_batch06 import FEN_SOURCE


def animal_tasks():
    n = "tr-g06-fen-bilimleri-note-011"
    return [
        task(n, "application", "Kelebeğin yaşam döngüsü kartları yumurta, tırtıl, pupa ve ergin olarak verilmiştir. Kartlar hangi sıraya konmalıdır?",
             "Yumurta → tırtıl → pupa → ergin", ["Tırtıl → yumurta → ergin → pupa", "Ergin → pupa → yumurta → tırtıl", "Pupa → ergin → tırtıl → yumurta"],
             "Kelebek tam başkalaşım geçirir; yumurtadan larva, ardından pupa ve ergin evreleri gelir."),
        task(n, "analysis", "K ve L canlılarının gelişimi karşılaştırılıyor. K yavrusunu doğurup sütle besliyor; L yumurtadan çıkıp belirgin başkalaşım geçiriyor. Hangi yorum uygundur?",
             "K bir memeli, L başkalaşım geçiren bir hayvan olabilir.", ["K kesinlikle yumurtlayan bir sürüngendir.", "L doğrudan küçük bir ergin olarak doğmuştur.", "İki canlıda da gelişim evresi bulunmaz."],
             "Doğum ve sütle besleme memeli; yumurta ile belirgin biçim değişimi başkalaşım kanıtıdır."),
        task(n, "application", "Yumurtlayan hayvanlar ile başkalaşım geçiren hayvanları ayıracak bir sınıflandırmada hangi ölçüt kullanılmalıdır?",
             "Yumurtlama ile başkalaşım farklı özelliklerdir; her yumurtlayan hayvan belirgin başkalaşım geçirmez.", ["Yumurtlayan hiçbir hayvan gelişmez.", "Başkalaşım yalnız memelilerde görülür.", "Yumurtlama, doğurarak çoğalma ile aynı olaydır."],
             "Kuş ve sürüngenler yumurtlayabilir ancak kurbağa veya kelebekteki gibi belirgin başkalaşım göstermeyebilir."),
        task(n, "comprehension", "Hayvanlarda büyüme ile gelişme arasındaki doğru ayrım hangisidir?",
             "Büyüme boyut ve kütle artışı, gelişme yapı ve işlevlerin olgunlaşmasıdır.", ["İkisi yalnız vücut renginin değişmesidir.", "Gelişme yalnız besin tüketmektir.", "Büyüme hiçbir ölçümle izlenemez."],
             "Büyüme nicel artış, gelişme ise canlıdaki nitel ve işlevsel değişimleri kapsar."),
    ]


def human_reproduction_tasks():
    n = "tr-g06-fen-bilimleri-note-012"
    return [
        task(n, "comprehension", "İnsanda yumurta hücresini üreten yapı ile embriyonun geliştiği organ hangi seçenekte doğru eşleştirilmiştir?",
             "Yumurtalık – rahim", ["Rahim – yumurtalık", "Yumurta kanalı – testis", "Testis – sperm kanalı"],
             "Yumurta hücresi yumurtalıkta oluşur; döllenmiş hücre rahme ulaşıp gelişimini sürdürür."),
        task(n, "analysis", "Bir akışta sperm ve yumurta hücresinin birleşmesi, ardından oluşan hücrenin rahme ilerlemesi gösteriliyor. Boş kutuya hangi kavram yazılmalıdır?",
             "Döllenme sonucu zigot oluşumu", ["Büyüme sonucu sperm oluşumu", "Rahimde yumurta üretimi", "Akciğerde embriyo gelişimi"],
             "Üreme hücrelerinin birleşmesi döllenmedir ve ilk hücre zigot adını alır."),
        task(n, "application", "Döllenme yeri ve embriyonun temel gelişim ortamı modele doğru yerleştirilecektir. Hangi eşleştirme kullanılmalıdır?",
             "Döllenme genellikle yumurta kanalında gerçekleşir; embriyonun temel gelişim ortamı rahimdir.", ["Yumurta hücresi rahimde üretilir.", "Sperm hücresi yumurtalıkta oluşur.", "Rahim ile yumurta kanalının görevleri aynıdır."],
             "Yumurta kanalı döllenme ve taşınma, rahim ise tutunma ve gelişimle ilişkilidir."),
    ]


def nervous_system_tasks():
    n = "tr-g06-fen-bilimleri-note-013"
    return [
        task(n, "comprehension", "Merkezî sinir sistemini oluşturan iki temel yapı hangisidir?", "Beyin ve omurilik",
             ["Duyu organları ve kaslar", "Kalp ve akciğer", "Hormonlar ve bezler"], "Beyin ve omurilik merkezî sinir sisteminin temel bölümleridir."),
        task(n, "application", "El sıcak bir yüzeye değdiğinde hızla çekiliyor. Bu hızlı yanıtın ilk düzenlendiği merkez hangisidir?", "Omurilik",
             ["Mide", "Böbrek", "Akciğer"], "Refleks yayı, tehlikeli uyarana hızlı yanıt için omurilikte düzenlenebilir."),
        task(n, "analysis", "Uyarı deriden omuriliğe ulaşıyor, omurilikten kasa yanıt gidiyor; acı daha sonra bilinçli algılanıyor. Hangi sıra uygundur?",
             "Duyu siniri → omurilik → motor sinir → kas; bilgi ayrıca beyne iletilir.",
             ["Kas → mide → duyu siniri → beyin", "Beyin → deri → omurilik olmadan kas", "Motor sinir → duyu siniri → akciğer"],
             "Refleks yayı duyu ve motor sinirleri omurilik üzerinden bağlar; bilinçli algı için beyin de bilgi alır."),
        task(n, "application", "Omurilik modeline refleks görevinin yanında hangi işlev eklenmelidir?",
             "Omurilik refleks merkezi olmasının yanında beyin ile çevresel yapılar arasında iletime katılır.",
             ["Omurilik sindirim enzimi üretir.", "Beyin bütün sinirlerden bağımsızdır.", "Çevresel sinirler yalnız kemiklerden oluşur."],
             "Omurilik hem hızlı refleks yanıtlarında hem sinirsel iletimin ana yolunda görev yapar."),
        task(n, "application", "Bir öğrenci kitabı okuyup anlamlandırırken hangi yapı öncelikle değerlendirme ve karar sürecine katılır?", "Beyin",
             ["Omurilik tek başına", "Mide", "Kemik iliği"], "Görsel bilginin işlenmesi, anlamlandırma ve bilinçli karar beynin görevleri arasındadır."),
        task(n, "analysis", "Duyu siniri zarar gören bir bölgede kaslar sağlamdır ancak dokunma bilgisi merkeze ulaşmıyor. Hangi çıkarım uygundur?",
             "Uyarının merkezî sinir sistemine taşınması aksayabilir.",
             ["Kaslar otomatik olarak kemik olur.", "Beyin artık bütün görevlerini kaybeder.", "Duyu siniri yalnız hormon salgılar."],
             "Duyu sinirleri reseptörlerden gelen uyarıları merkezî sinir sistemine taşır; çıkarım ilgili bölgeyle sınırlıdır."),
        task(n, "comprehension", "Çevresel sinir sisteminin temel işlevi hangisidir?",
             "Merkezî sinir sistemi ile organlar arasında uyarı ve yanıt iletmek",
             ["Kanın pıhtılaşmasını tek başına sağlamak", "Besinleri sindirmek", "Kemik üretmek"],
             "Çevresel sinirler duyu ve motor iletilerle merkez ile vücut arasında bağlantı kurar."),
        task(n, "error-analysis", "Bir öğrenci “Reflekste beyin hiçbir zaman bilgi almaz.” diyor. En doğru düzeltme hangisidir?",
             "Hızlı yanıt omurilikte düzenlenebilir; uyarı bilgisi bilinçli algı için beyne de iletilebilir.",
             ["Refleks yalnız beyinde başlar ve omuriliğe uğramaz.", "Refleks sırasında sinirler çalışmaz.", "Kas yanıtı uyarıdan önce oluşur."],
             "Refleksin hızlı olması beynin olaydan hiç haberdar olmadığı anlamına gelmez."),
        task(n, "application", "Bir sinir sistemi modelinde oklar yalnız merkezden kasa gidiyor. Modeli tamamlamak için hangi yol eklenmelidir?",
             "Duyu alıcısından merkezî sinir sistemine gelen iletim yolu",
             ["Kastan doğrudan mideye sindirim yolu", "Kemikten akciğere hormon yolu", "Bütün okları kaldırma"],
             "Sinirsel düzenleme duyu girişini ve motor çıkışı birlikte gösteren çift yönlü bilgi akışını içerir."),
    ]


def endocrine_tasks():
    n = "tr-g06-fen-bilimleri-note-014"
    return [
        task(n, "comprehension", "İç salgı bezlerinin ürettiği ve kanla hedef yapılara taşınan kimyasal habercilere ne ad verilir?", "Hormon",
             ["Enzim", "Alyuvar", "Duyu siniri"], "Hormonlar iç salgı bezlerinden kana verilir ve hedef hücrelerin çalışmasını düzenler."),
        task(n, "application", "Ani tehlike sırasında kalp atımı ve solunumun hızlanmasına katkı sağlayan bez hangisidir?", "Böbreküstü bezi",
             ["Tükürük bezi", "Ter bezi", "Gözyaşı bezi"], "Böbreküstü bezinden salgılanan hormonlar vücudu kısa süreli strese hazırlamaya yardım eder."),
        task(n, "analysis", "Yemekten sonra yükselen kan şekerinin zamanla normal aralığa yaklaşması hangi düzenleyici ilişkiyi destekler?",
             "Pankreas hormonlarının kan şekeri dengesine katkısını",
             ["Akciğerin kemik uzatmasını", "Midenin sinir üretmesini", "Tiroit bezinin doğrudan ışık algılamasını"],
             "Pankreasın hormonları kan şekeri düzeyinin düzenlenmesinde rol alır; tek ölçüm kişisel tanı koydurmaz."),
        task(n, "comprehension", "Büyüme hormonu salgılanmasını ve bazı başka bezleri etkileyen bez hangisidir?", "Hipofiz bezi",
             ["Tükürük bezi", "Yağ bezi", "Ter bezi"], "Hipofiz, büyüme hormonu ve başka iç salgı bezlerini etkileyen hormonlar üretir."),
        task(n, "analysis", "Hipofizden çıkan uyarıcı hormonun tiroit bezinin çalışmasını etkilediği model neyi gösterir?",
             "İç salgı bezlerinin birbirleriyle ilişkili çalışabildiğini",
             ["Bütün bezlerin birbirinden tamamen bağımsız olduğunu", "Hormonların yalnız sindirimde görev yaptığını", "Sinirlerin hormon yerine kan hücresi ürettiğini"],
             "Bir bezin hormonu başka bir bezin etkinliğini düzenleyebilir; sistemler ilişki içinde çalışır."),
        task(n, "error-analysis", "Bir öğrenci “Hormonlar sinir uyarısı kadar anlık başlar ve her zaman hemen biter.” diyor. Hangi düzeltme uygundur?",
             "Hormon etkileri genellikle sinirsel iletime göre daha yavaş başlayabilir ve daha uzun sürebilir.",
             ["Hormonların vücutta hiçbir etkisi yoktur.", "Sinirsel iletim yalnız kanla gerçekleşir.", "Bütün hormonlar aynı organda üretilir."],
             "Sinirsel ve hormonal düzenleme hız ve etki süresi bakımından farklılaşabilir."),
        task(n, "application", "Bir modelde hormon, onu üreten bezden hedef organa nasıl gösterilmelidir?",
             "Bezden kana, kandan uygun hedef hücrelere yönelen bir ileti olarak",
             ["Bezden kemiğe rastgele sıçrayan ışık olarak", "Yalnız deri yüzeyinde kalan boya olarak", "Hedefi olmayan ve hiçbir yere ulaşmayan madde olarak"],
             "Hormonlar kana salgılanır ve yalnız uygun alıcılara sahip hedeflerde etki oluşturur."),
        task(n, "comprehension", "Tiroit hormonlarının genel olarak ilişkili olduğu süreç hangisidir?",
             "Metabolizma hızının düzenlenmesi",
             ["Görüntünün retinada oluşması", "Kemiklerin eklemle bağlanması", "Akciğerde oksijenin rengine karar verme"],
             "Tiroit hormonları vücudun enerji kullanımı ve metabolik hızının düzenlenmesine katkı sağlar."),
        task(n, "error-analysis", "Bir öğrenci “Her belirti tek bir bezin hastalığını kesin gösterir.” diyor. Bilimsel ve güvenli düzeltme hangisidir?",
             "Benzer belirtilerin farklı nedenleri olabilir; tanı uzman değerlendirmesi ve uygun ölçümler gerektirir.",
             ["Belirti görülünce arkadaş ilacı kullanılmalıdır.", "Tek internet yorumu kesin tanıdır.", "İç salgı sistemi sağlıkla ilişkili değildir."],
             "Ders bilgisi işlevleri açıklar; kişisel tanı ve tedavi kararı vermez."),
        task(n, "analysis", "Koşu başlarken sinirsel yanıtın hızlı, hormonal etkinin daha yavaş ve uzun sürdüğü ölçülüyor. Hangi sonuç uygundur?",
             "Sinir ve iç salgı sistemleri farklı zaman özellikleriyle birlikte düzenleme yapabilir.",
             ["İki sistem birbirini hiçbir zaman etkilemez.", "Hormonlar yalnız kemiklerde bulunur.", "Hız farkı sistemlerden birinin gereksiz olduğunu kanıtlar."],
             "Vücut düzenlemesi hızlı sinirsel iletim ile daha uzun etkili hormonal yanıtın eşgüdümünü içerebilir."),
    ]


def puberty_tasks():
    n = "tr-g06-fen-bilimleri-note-015"
    return [
        task(n, "comprehension", "Ergenlik dönemindeki değişimlerle ilgili hangi ifade bilimseldir?",
             "Değişimlerin başlama zamanı ve hızı kişiden kişiye farklılık gösterebilir.",
             ["Bütün bireylerde aynı gün ve aynı hızda başlar.", "Yalnız dış görünüş değişir, duygular etkilenmez.", "Her farklılık bir sağlık sorunu olduğunu kesin gösterir."],
             "Ergenlik doğal bir gelişim sürecidir ve bireysel zamanlama farklılıkları olağandır."),
        task(n, "application", "Arkadaşının fiziksel değişimlerinin kendisinden farklı olduğunu gören öğrenci nasıl davranmalıdır?",
             "Karşılaştırma ve alaydan kaçınıp bireysel gelişim farklılıklarına saygı göstermelidir.",
             ["Farklılığı kusur olarak yaymalıdır.", "Kesin tanı koymalıdır.", "Kişisel bilgileri izinsiz paylaşmalıdır."],
             "Bireysel gelişim farklılıkları saygı, mahremiyet ve güvenilir yetişkin desteğiyle ele alınır."),
        task(n, "comprehension", "Aşağıdakilerden hangisi ergenlikte görülebilen ruhsal değişime örnektir?",
             "Duyguların daha hızlı değişebilmesi", ["Kemik uzunluğunun artması", "Terlemenin artması", "Vücut kıllarının belirginleşmesi"],
             "Duygu değişkenliği ruhsal; diğer seçenekler bedensel değişim örnekleridir."),
        task(n, "analysis", "Bir öğrenci son aylarda hem boyunun uzadığını hem de duygularının daha değişken olduğunu belirtiyor. Hangi sınıflandırma uygundur?",
             "Boy uzaması bedensel, duygu değişkenliği ruhsal değişimdir.",
             ["İkisi de yalnız toplumsal değişimdir.", "Boy uzaması ruhsal, duygu değişimi bedenseldir.", "Hiçbiri gelişimle ilişkili değildir."],
             "Ergenlikte bedensel ve ruhsal değişimler bir arada görülebilir; iki tür birbirine karıştırılmaz."),
        task(n, "error-analysis", "Bir öğrenci “Ergenlikte herkes aynı fiziksel değişimi aynı hızla yaşar.” diyor. Hangi düzeltme doğrudur?",
             "Ortak değişimler bulunsa da zamanlama ve hız bireyler arasında değişebilir.",
             ["Ergenlikte hiçbir ortak değişim yoktur.", "Yalnız arkadaşların yorumu gelişimi belirler.", "Farklı hız her zaman hastalık demektir."],
             "Biyolojik gelişim genel örüntüler taşır ancak bireysel farklılıklar doğaldır."),
        task(n, "application", "Ergenlikle ilgili güvenilir bilgiye ihtiyaç duyan öğrenci öncelikle hangi kaynağa yönelmelidir?",
             "Ailesi, okul sağlık/rehberlik birimi veya yetkin sağlık uzmanı gibi güvenilir yetişkinlere",
             ["Kimliği belirsiz sosyal medya yorumuna", "Arkadaşının reçeteli ilacına", "Alay amacıyla oluşturulan söylentiye"],
             "Kişisel gelişim ve sağlık bilgisi güvenilir yetişkin ve uzman kaynaklardan alınır."),
        task(n, "comprehension", "Ergenlikte öz bakımın önemini doğru açıklayan ifade hangisidir?",
             "Terleme ve cilt değişimleri artabileceği için düzenli temizlik ve uygun bakım yararlıdır.",
             ["Temizlik alışkanlıkları gelişimle ilgisizdir.", "Her cilt değişimi için rastgele ilaç kullanılmalıdır.", "Kişisel bakım yalnız başkaları istediğinde yapılmalıdır."],
             "Düzenli ve güvenli öz bakım bedensel değişimlere uyum sağlamaya yardımcı olur."),
        task(n, "analysis", "Bir çizelgede dört öğrencinin boy uzama miktarları farklıdır; hepsinin genel sağlık izlemi normaldir. En uygun sonuç hangisidir?",
             "Boy uzama hızları bireysel olarak farklı olabilir.",
             ["En az uzayan öğrenci kesinlikle hastadır.", "Bütün değerlerin aynı olması gerekir.", "Boy uzaması ergenlikle ilişkili değildir."],
             "Tek büyüme ölçümü tanı koydurmaz; normal gelişimde bireysel hız farklılıkları görülebilir."),
        task(n, "error-analysis", "Bir öğrenci “Ruhsal değişimler gerçek değildir; ergenlik yalnız boy uzamasıdır.” diyor. Hangi düzeltme uygundur?",
             "Ergenlik bedensel değişimlerin yanında duygu, düşünce ve sosyal ilişkilerde değişimler de içerebilir.",
             ["Ergenlikte boy hiç uzamaz.", "Duygular yalnız dışarıdan öğretilir ve gelişimle ilgisizdir.", "Ruhsal değişimler herkes için aynı biçimde olur."],
             "Gelişim biyolojik, ruhsal ve sosyal boyutları birlikte kapsar."),
        task(n, "application", "Bir arkadaş bedensel değişimi nedeniyle rahatsız edici yorumlara maruz kalıyor. En uygun davranış hangisidir?",
             "Yorumları durdurmak, arkadaşın mahremiyetine saygı göstermek ve gerektiğinde güvenilir yetişkinden destek istemek",
             ["Yorumları daha çok kişiye yaymak", "Arkadaşın fotoğrafını izinsiz paylaşmak", "Durumu eğlence olarak sürdürmek"],
             "Akran ilişkilerinde saygı ve mahremiyet korunur; zorbalık güvenilir yetişkin desteğiyle ele alınır."),
        task(n, "application", "Bir kaynak 'ergenlikteki bütün duygular sorun belirtisidir' diyor ancak bilimsel kaynaklar duygu değişkenliğinin doğal olabileceğini belirtiyor. Bilgi kartı nasıl düzeltilmelidir?",
             "İlk kaynak aşırı genelleme yapmıştır; süreklilik ve işlev kaybı gibi durumlarda uzman desteği ayrıca değerlendirilir.",
             ["Her duygu değişimi için tanı konmalıdır.", "Bilimsel kaynaklar karşılaştırılmamalıdır.", "Duygular sağlıkla hiçbir zaman ilişkili değildir."],
             "Doğal değişim ile destek gerektiren durumlar kesin genellemeyle değil, güvenilir değerlendirmeyle ayrılır."),
        task(n, "comprehension", "Ergenlik döneminde sağlıklı gelişimi destekleyen alışkanlıklar hangisidir?",
             "Dengeli beslenme, düzenli uyku, hareket ve güvenilir destek",
             ["Sürekli uykusuz kalma ve öğün atlama", "Başkasının ilacını kullanma", "Soruları gizleyip yanlış bilgiye güvenme"],
             "Temel yaşam alışkanlıkları ve güvenilir sosyal destek gelişim sağlığını korumaya yardımcı olur."),
    ]


def system_health_tasks():
    n = "tr-g06-fen-bilimleri-note-016"
    return [
        task(n, "comprehension", "Denetleyici ve düzenleyici sistemlerin sağlığını destekleyen temel alışkanlık hangisidir?",
             "Yeterli ve düzenli uyku", ["Her gece uykuyu ertelemek", "Sınırsız enerji içeceği tüketmek", "Reçeteli ilacı paylaşmak"],
             "Uyku, sinirsel ve hormonal düzenleme ile öğrenme süreçlerini destekler."),
        task(n, "application", "Sınav haftasında uykusuzluk yaşayan öğrenci için en güvenli ilk plan hangisidir?",
             "Uyku düzeni kurmak, dengeli beslenmek ve sorun sürerse ailesiyle sağlık uzmanına danışmak",
             ["Arkadaşının ilacını denemek", "Daha çok enerji içeceği içmek", "Bir hafta hiç uyumadan çalışmak"],
             "Yaşam düzeni güvenli ilk basamaktır; süren sağlık sorunu akran önerisiyle değil uzman desteğiyle değerlendirilir."),
        task(n, "analysis", "Bir haftalık kayıtta düzenli uyuyan öğrencilerin dikkat testinde daha tutarlı sonuç aldığı görülüyor. Hangi yorum kanıt sınırını korur?",
             "Bu grupta düzenli uyku ile dikkat tutarlılığı arasında ilişki görülmüştür; başka etkenler de incelenmelidir.",
             ["Uyku tek başına bütün başarıyı kesin belirler.", "Bir haftalık kayıt bütün öğrenciler için değişmez kanundur.", "Dikkat ile uyku arasında hiçbir ilişki araştırılamaz."],
             "Gözlem ilişkiyi destekler ancak tek başına kesin nedensellik ve sınırsız genelleme kurmaz."),
        task(n, "error-analysis", "Bir öğrenci “Arkadaşımda işe yarayan reçeteli ilaç bende de güvenlidir.” diyor. Hangi düzeltme doğrudur?",
             "İlaçlar kişiye ve duruma göre değerlendirilir; yalnız uygun yetişkin ve sağlık uzmanı yönlendirmesiyle kullanılmalıdır.",
             ["Doz bilgisi olmadan ilaç paylaşmak güvenlidir.", "Reçeteli ilaçlar herkeste aynı etkiyi yapar.", "Belirti benzerliği kesin tanı koydurur."],
             "İlaç paylaşımı ciddi risk taşır; öğrenciye kişisel tedavi önerisi verilmez."),
        task(n, "application", "Güvenilir sağlık bilgisi araştırılırken hangi ölçüt kullanılmalıdır?",
             "Yetkin kurum/yazar, güncel tarih, kaynak ve uzmanlık bilgisi kontrol edilmelidir.",
             ["En çok beğeni alan yorum doğru sayılmalıdır.", "Kaynağı belirsiz video tek kanıt yapılmalıdır.", "Ürün reklamı bilimsel araştırma yerine kullanılmalıdır."],
             "Kaynak güvenilirliği yazarlık, kurum, güncellik ve kanıtla değerlendirilir."),
        task(n, "comprehension", "Düzenli fiziksel etkinliğin sistem sağlığına olası katkısı hangisidir?",
             "Uyku, stres yönetimi ve genel vücut düzeninin desteklenmesi",
             ["Sinir sisteminin bütünüyle kapanması", "Hormonların tamamen yok olması", "Her sağlık sorununu tek başına kesin iyileştirmesi"],
             "Uygun hareket sağlığı destekler ancak tek başına bütün sorunların tedavisi değildir."),
        task(n, "analysis", "İki kaynak enerji içecekleri için çelişkili iddialar sunuyor. Biri ürün reklamı, diğeri kamu sağlık kurumunun çocuklara yönelik açıklaması. Hangisi önceliklidir?",
             "Çıkar çatışması daha düşük ve uzman kanıtına dayalı kamu sağlık kurumu açıklaması",
             ["Ürünü satan reklam; çünkü daha renkli hazırlanmıştır.", "Kaynağı olmayan kullanıcı yorumu", "İçeriği okumadan ilk çıkan sonuç"],
             "Sağlık kararında kaynak amacı, uzmanlık ve kanıt niteliği birlikte değerlendirilir."),
        task(n, "error-analysis", "Bir öğrenci “Baş ağrısının nedeni kesinlikle tek bir iç salgı bezidir.” diyor. Bilimsel düzeltme hangisidir?",
             "Baş ağrısının farklı nedenleri olabilir; tek belirtiden bez veya hastalık tanısı konamaz.",
             ["Her baş ağrısında aynı ilaç kullanılmalıdır.", "Belirtiler uzman değerlendirmesi gerektirmez.", "İç salgı sistemi baş ağrısıyla kesinlikle ilişkisizdir."],
             "Ders içeriği işlevleri açıklar; belirtiye dayalı kişisel tanı koymaz."),
        task(n, "application", "Uzun süre ekran kullanan öğrenci çalışma düzenini nasıl iyileştirebilir?",
             "Düzenli mola, uygun duruş, yeterli uyku ve günlük hareket planlayabilir.",
             ["Ekranı bütün gece aralıksız kullanabilir.", "Uyku yerine kafeinli içecek seçebilir.", "Göz yorgunluğunu görmezden gelebilir."],
             "Dengeli çalışma ve dinlenme alışkanlıkları sinir sistemi sağlığını destekler."),
        task(n, "comprehension", "Sinir sistemi sağlığını korumada kask ve emniyet kemerinin işlevi nedir?",
             "Baş, beyin ve omurilik yaralanması riskini azaltmaya yardımcı olmak",
             ["Hormon üretimini durdurmak", "Bütün kazaları kesinlikle önlemek", "Kasları sinire dönüştürmek"],
             "Koruyucu ekipman darbelerin etkisini azaltır; riski sıfırladığı iddia edilmez."),
        task(n, "analysis", "Bir öğrenci uyku süresini artırınca derste dikkati yükseliyor; aynı dönemde çalışma planını da değiştiriyor. Hangi sonuç uygundur?",
             "İyileşmede uyku ve çalışma planının katkıları ayrı karşılaştırma olmadan kesin ayrıştırılamaz.",
             ["Yalnız uyku kesin tek nedendir.", "Çalışma planı hiçbir zaman etkili olamaz.", "İki değişken birlikte değiştiğinde neden kesinleşir."],
             "Birden fazla koşul değiştiğinde tek nedenli çıkarım için kontrollü ek veri gerekir."),
        task(n, "application", "Kaygı ve uyku sorunu günlük işlevleri uzun süre etkileyen öğrenci ne yapmalıdır?",
             "Güvendiği yetişkinle konuşup uygun sağlık veya rehberlik uzmanından destek istemelidir.",
             ["Sorunu gizleyip rastgele takviye kullanmalıdır.", "Arkadaşının reçetesini almalıdır.", "Uzman desteğini gereksiz saymalıdır."],
             "Süren ve işlevi etkileyen sorunlarda güvenilir yetişkin ve uzman desteği güvenli yaklaşımdır."),
    ]


def reflection_tasks():
    n = "tr-g06-fen-bilimleri-note-017"
    return [
        task(n, "comprehension", "Pürüzsüz bir yüzeyde paralel gelen ışınların düzenli yönlerde yansımasına ne ad verilir?",
             "Düzgün yansıma", ["Dağınık yansıma", "Tam soğurulma", "Işığın yok olması"], "Düz ve pürüzsüz yüzeyler ışınların düzenli yönlerde yansımasını sağlar."),
        task(n, "analysis", "Aynı ışık parlak metal ve mat duvara tutuluyor. Metalde net görüntü, duvarda farklı yönlere dağılmış ışık görülüyor. Hangi yorum doğrudur?",
             "Metal düzgün, duvar dağınık yansıma oluşturmuştur.", ["Duvar ışığı hiç yansıtmamıştır.", "İki yüzey aynı yansımayı oluşturmuştur.", "Metal yalnız ışığı soğurmuştur."],
             "Net görüntü düzenli yönlü, dağılma ise pürüzlü yüzeyde farklı yönlü yansımayla ilişkilidir."),
        task(n, "error-analysis", "Bir öğrenci “Dağınık yansımada ışık hiç yansımaz.” diyor. Hangi düzeltme doğrudur?",
             "Işık yansır ancak yüzey pürüzleri nedeniyle birçok yöne dağılır.", ["Işık yalnız pürüzlü yüzeyde yok olur.", "Dağınık yansımada gelme açısı bulunmaz.", "Pürüzlü yüzeyler bütün ışığı geçirir."],
             "Dağınık sözcüğü yansımanın yokluğunu değil, yönlerin çeşitlenmesini anlatır."),
        task(n, "application", "Bir projektör perdesinin sınıfın farklı yerlerinden görülmesi isteniyor. Hangi yüzey özelliği yararlıdır?",
             "Işığı farklı yönlere yansıtan mat yüzey", ["Yalnız tek yöne güçlü yansıtan ayna yüzeyi", "Işığı bütünüyle geçiren saydam yüzey", "Hiç ışık almayan yüzey"],
             "Mat yüzeydeki dağınık yansıma görüntünün geniş açıdan görülmesini kolaylaştırır."),
        task(n, "analysis", "Buruşturulmuş folyo açılıp tamamen düzleştirildiğinde yansıyan ışığın dağılımı nasıl değişebilir?",
             "Yüzey düzgünleştikçe yansıma daha düzenli hâle gelebilir.", ["Işık yansıması bütünüyle sona erer.", "Dağılım zorunlu olarak artar.", "Yüzey şekli yansımayı hiçbir zaman etkilemez."],
             "Yüzey normallerinin daha düzenli olması yansıyan ışınların yönlerini de düzenler."),
        task(n, "comprehension", "Düzgün ve dağınık yansımanın ikisinde de geçerli temel ilke hangisidir?",
             "Her küçük yüzey bölgesinde gelme ve yansıma açıları normale göre eşittir.", ["Pürüzlü yüzey ışığı yok eder.", "Yansıma açısı her zaman sıfırdır.", "Normal yalnız aynalarda çizilebilir."],
             "Pürüzlülük yerel normallerin yönünü değiştirir; yansıma kuralı her bölgede geçerlidir."),
    ]


def mirror_tasks():
    n = "tr-g06-fen-bilimleri-note-019"
    return [
        task(n, "application", "Dar bir mağaza koridorunda geniş görüş alanı elde etmek için hangi ayna seçilmelidir?", "Tümsek ayna",
             ["Düz ayna", "Çukur ayna", "Işığı geçiren cam"], "Tümsek ayna daha geniş alanı küçük ve düz görüntüyle gösterebilir."),
        task(n, "comprehension", "Düz aynada oluşan görüntünün genel özelliği hangisidir?", "Düz, sanal ve cisimle aynı boyda olması",
             ["Her zaman ters ve çok büyük olması", "Aynanın önünde gerçek görüntü olması", "Cisim uzaklığından bağımsız yok olması"], "Düz ayna sanal, düz ve eş boylu görüntü oluşturur."),
        task(n, "application", "Yüz odak uzaklığından daha yakındayken büyütülmüş ve düz görüntü verecek bakım aynası seçilecektir. Ayna türü hangisidir?", "Çukur ayna",
             ["Tümsek ayna", "Düz ayna", "Saydam levha"], "Çukur ayna, cisim odak ile ayna arasındayken sanal, düz ve büyütülmüş görüntü oluşturabilir."),
        task(n, "application", "Araç yan aynası için tümsek ayna seçilirken hangi gerekçe kullanılmalıdır?",
             "Tümsek ayna görüntüyü küçültür ancak geniş görüş alanı sağladığı için kullanılır.", ["Tümsek ayna her zaman ters gerçek görüntü verir.", "Yan aynada görüş alanı önemsizdir.", "Tümsek ayna ışığı hiç yansıtmaz."], "Araç aynasında tercih nedeni büyütme değil, geniş alanı görebilmektir."),
        task(n, "application", "Güneş ışığını küçük bir bölgede toplamak isteyen deney düzeneğinde hangi ayna kullanılabilir?", "Çukur ayna",
             ["Tümsek ayna", "Düz ayna", "Mat karton"], "Çukur ayna, eksene paralel ışınları odak yakınında toplayabilir; deney güvenli gözetimle yapılmalıdır."),
        task(n, "analysis", "Aynı cisim tümsek aynada küçük ve düz, düz aynada eş boylu görülüyor. Hangi çıkarım doğrudur?",
             "Ayna yüzeyinin biçimi görüntü boyutunu ve görüş alanını etkiler.", ["Bütün aynalar aynı görüntüyü verir.", "Cisim aynaya bakınca fiziksel olarak küçülür.", "Düz ayna her zaman büyütür."], "İki aynadaki farklı görüntü özellikleri yansıtıcı yüzey biçiminden kaynaklanır."),
        task(n, "comprehension", "Tümsek aynanın görüntüsü için hangisi genellikle doğrudur?", "Düz, sanal ve cisimden küçük olması",
             ["Ters, gerçek ve cisimden büyük olması", "Her uzaklıkta cisimle aynı boyda olması", "Hiç görüntü oluşturmaması"], "Tümsek aynada sanal, düz ve küçültülmüş görüntü oluşur."),
        task(n, "error-analysis", "Bir öğrenci “Çukur ayna her cisim uzaklığında aynı tür görüntü verir.” diyor. Hangi düzeltme gerekir?",
             "Çukur aynada görüntünün türü ve boyutu cismin odakla ilişkili uzaklığına göre değişir.", ["Çukur ayna hiçbir zaman görüntü oluşturmaz.", "Cisim uzaklığı yalnız düz aynayı etkiler.", "Odak kavramı aynalarla ilişkili değildir."], "Çukur ayna yakın cisimde sanal-büyük, daha uzakta gerçek ve farklı boylarda görüntü verebilir."),
        task(n, "application", "Periskopun basit modelinde görüntü yönünü değiştirmek için hangi ayna türü uygun biçimde kullanılabilir?", "Düz aynalar",
             ["Yalnız tümsek aynalar", "Yalnız çukur aynalar", "Mat yüzeyler"], "Düz aynalar ışığın yönünü belirli açılarla değiştirerek basit periskop modeli oluşturabilir."),
    ]


def absorption_tasks():
    n = "tr-g06-fen-bilimleri-note-020"
    return [
        task(n, "analysis", "Özdeş siyah ve beyaz kutular aynı lambadan eşit süre ışık alıyor. Siyah kutunun sıcaklığı 9°C, beyazın 4°C artıyor. Hangi sonuç uygundur?",
             "Bu düzende siyah yüzey daha fazla ışık enerjisi soğurmuş olabilir.", ["Beyaz yüzey kesinlikle daha fazla soğurmuştur.", "Renk ile sıcaklık artışı arasında hiçbir ilişki araştırılamaz.", "Siyah kutu ışığı bütünüyle yansıtmıştır."], "Eşit koşullarda daha büyük sıcaklık artışı daha fazla soğurulmayı destekler; sonuç düzenekle sınırlıdır."),
        task(n, "application", "Rengin ışık soğurulmasına etkisini sınamak için hangi değişkenler sabit tutulmalıdır?",
             "Malzeme, yüzey alanı, ışık gücü, uzaklık, süre ve başlangıç sıcaklığı", ["Renkle birlikte malzeme ve lamba gücü de değiştirilmelidir.", "Yalnız kutuların adı aynı olmalıdır.", "Başlangıç sıcaklığı ölçülmemelidir."], "Yalnız renk değişirse sıcaklık farkı renk-soğurma ilişkisiyle yorumlanabilir."),
        task(n, "error-analysis", "Bir öğrenci “Siyah yüzey bütün ışığı yüzde yüz soğurur.” diyor. Hangi düzeltme doğrudur?",
             "Siyah yüzey görünür ışığın büyük bölümünü soğurabilir; 'tamamı' sonucu ölçüm olmadan kurulamaz.", ["Siyah yüzey hiçbir ışığı soğurmaz.", "Beyaz ve siyah her koşulda aynı davranır.", "Soğurulma yalnız ses dalgalarında görülür."], "Renk eğilimi mutlak ve ölçümsüz bir yüzdeye dönüştürülmemelidir."),
        task(n, "comprehension", "Işığın bir madde tarafından soğurulması enerji bakımından hangi sonuca katkı sağlayabilir?",
             "Maddenin iç enerjisinin ve sıcaklığının artmasına", ["Maddenin zorunlu olarak görünmez olmasına", "Bütün enerjinin yok olmasına", "Kütlenin anında sıfırlanmasına"], "Soğurulan ışık enerjisi maddenin iç enerjisine aktarılıp ısınmaya katkı verebilir."),
    ]


def white_light_tasks():
    n = "tr-g06-fen-bilimleri-note-021"
    return [
        task(n, "analysis", "Aşağıdaki şemada beyaz ışığın prizmadan geçişi gösteriliyor. Ekrandaki renk şeridi hangi çıkarımı destekler?",
             "Beyaz ışık farklı renk bileşenlerinden oluşur.", ["Prizma renkleri yoktan üretir.", "Beyaz ışık yalnız kırmızıdır.", "Ekran kendi kendine renk üretmiştir."], "Farklı renklerin farklı miktarda kırılıp ayrılması beyaz ışığın bileşik yapısını gösterir.", figure_kind="prism"),
        task(n, "comprehension", "Görünür ışık tayfında kırmızıdan mora uzanan renklerin kaynağı hangisidir?",
             "Beyaz ışığın farklı renk bileşenleri", ["Prizmanın boyası", "Karanlığın ürettiği renkler", "Yalnız ekranın yüzeyi"], "Prizma var olan renk bileşenlerini farklı kırılma miktarlarıyla ayırır."),
        task(n, "application", "Prizma deneyinde renk şeridini daha açık gözlemek için hangi düzenleme uygundur?",
             "Dar beyaz ışık demetini prizmaya yöneltip ortam ışığını azaltmak ve ekranı hizalamak", ["Prizmayı ışık yolundan çıkarmak", "Bütün odayı çok parlak aydınlatmak", "Ekranı ışığın ters yönüne saklamak"], "Dar demet, uygun hizalama ve düşük ortam ışığı ayrışan renkleri görünür kılar."),
        task(n, "error-analysis", "Bir öğrenci “Prizma beyaz ışığa sonradan renk ekler.” diyor. Hangi düzeltme doğrudur?",
             "Prizma beyaz ışığın içindeki renkleri farklı miktarda kırarak ayırır.", ["Prizma ışığı bütünüyle yok eder.", "Beyaz ışıkta hiçbir renk bileşeni yoktur.", "Renkler yalnız karanlıkta oluşur."], "Ayrışma yeni renk üretimi değil, bileşenlerin farklı yönlere sapmasıdır."),
        task(n, "analysis", "Renkli dilimleri bulunan bir disk hızla döndüğünde beyaza yakın görünmektedir. Bu gözlem neyi destekler?",
             "Farklı ışık renklerinin uygun birleşiminin beyaza yakın algı oluşturabileceğini", ["Beyaz ışığın tek renk olduğunu", "Renklerin dönme sırasında yok olduğunu", "Diskin kütlesinin azaldığını"], "Hızlı dönüşte göz farklı renk uyarılarını birleştirir; bu, beyaz ışığın bileşim fikriyle uyumludur."),
    ]


def object_color_tasks():
    n = "tr-g06-fen-bilimleri-note-022"
    return [
        task(n, "comprehension", "Beyaz bir cismin beyaz ışıkta beyaz görünmesinin temel nedeni hangisidir?",
             "Görünür renklerin büyük bölümünü yansıtması", ["Bütün renkleri soğurması", "Kendi kırmızı ışığını üretmesi", "Işığı bütünüyle yok etmesi"], "Beyaz yüzey görünür bileşenlerin çoğunu yansıttığı için beyaz algılanır."),
        task(n, "comprehension", "Siyah bir cismin beyaz ışıkta koyu görünmesi hangi davranışla açıklanır?",
             "Gelen görünür ışığın büyük bölümünü soğurması", ["Bütün renkleri güçlü yansıtması", "Yalnız beyaz ışık üretmesi", "Işıkla hiçbir etkileşim kurmaması"], "Yansıyan ışık az olduğunda cisim siyaha yakın görünür."),
        task(n, "analysis", "Kırmızı bir top kırmızı ışıkta parlak, mavi ışıkta çok koyu görünüyor. Hangi çıkarım uygundur?",
             "Top kırmızı ışığı yansıtır; mavi ışığı büyük ölçüde soğurur.", ["Top mavi ışığı kırmızıya dönüştürür.", "Top bütün renkleri eşit yansıtır.", "Aydınlatma rengi görünümü etkilemez."], "Görünen renk, gelen ışığın bileşimi ile cismin yansıtma özelliğinin ortak sonucudur."),
        task(n, "application", "Yeşil bir yaprağın yeşil görünmesini sağlayan temel ışık davranışı hangisidir?",
             "Yeşil bileşeni diğerlerine göre daha çok yansıtması", ["Yeşil ışığı bütünüyle soğurması", "Kendi Güneş ışığını üretmesi", "Bütün renkleri eşit yok etmesi"], "Yaprak beyaz ışığın yeşil bileşenini daha fazla yansıttığı için yeşil algılanır."),
        task(n, "error-analysis", "Bir öğrenci “Cismin görünen rengi aydınlatma değişse de her zaman aynıdır.” diyor. Hangi düzeltme doğrudur?",
             "Görünen renk, cisim özelliğiyle birlikte üzerine düşen ışığın renklerine de bağlıdır.", ["Cisim rengi yalnız adına bağlıdır.", "Aydınlatma yalnız cismin kütlesini değiştirir.", "Karanlıkta bütün cisimler kendi renginde parlak görünür."], "Yansıtılabilecek renk ortam ışığında yoksa cisim farklı veya koyu görünebilir."),
        task(n, "analysis", "Mavi bir kumaş beyaz ışıkta mavi, yalnız kırmızı ışık altında siyaha yakın görünüyor. En uygun açıklama hangisidir?",
             "Kumaş mavi bileşeni yansıtır; kırmızı ışığı yeterince yansıtmadığı için koyu görünür.", ["Kumaş kırmızı ışığı maviye dönüştürür.", "Kırmızı ışık altında mavi bileşen daha çok bulunur.", "Kumaşın rengi ışıkla ilişkisizdir."], "Kırmızı aydınlatmada yansıtacağı mavi bileşen bulunmaz."),
        task(n, "application", "Renk görünümünde yalnız ışık kaynağının etkisini sınamak için hangi plan uygundur?",
             "Aynı cismi ve ortamı koruyup yalnız aydınlatma rengini değiştirmek", ["Her ışıkta farklı cisim kullanmak", "Cisim ve ışık rengini birlikte değiştirmek", "Gözlem sonuçlarını kaydetmemek"], "Tek değişken ışık rengi olduğunda görünüm farkı aydınlatmayla ilişkilendirilebilir."),
        task(n, "error-analysis", "Bir öğrenci “Kırmızı elma mavi ışığı kırmızıya çevirir.” diyor. Hangi düzeltme uygundur?",
             "Elma kırmızı ışığı yansıtır; yalnız mavi ışıkta yansıtacağı kırmızı bileşen olmadığından koyu görünebilir.", ["Elma bütün ışıkları kırmızı ışığa dönüştürür.", "Mavi ışıkta ortamda kırmızı bileşen zorunlu olarak vardır.", "Cisimler ışığı hiç soğurmaz."], "Cisim renk üretip dönüştürmez; mevcut bileşenleri farklı oranlarda yansıtır ve soğurur."),
        task(n, "application", "Karanlık kutudaki bir cismin rengini gözleyebilmek için düzenek nasıl tamamlanmalıdır?",
             "Cisme ışık düşmesi ve yansıyan ışığın göze ulaşması", ["Cismin mutlaka ısınması", "Işık olmadan cismin kendi rengini göze göndermesi", "Yalnız cismin adının bilinmesi"], "Görme, kaynaktan gelen ışığın cisimle etkileşip göze ulaşmasına bağlıdır."),
        task(n, "analysis", "Sarı bir cisim, sarı bileşen içermeyen tek renkli ışık altında koyu görünüyor. Hangi sonuç kanıt sınırını korur?",
             "Cismin yansıtacağı uygun ışık bileşeni ortamda bulunmadığı için koyu görünmüş olabilir.", ["Cisim kalıcı olarak siyaha dönüşmüştür.", "Tek gözlem cismin kimyasal yapısının bozulduğunu kanıtlar.", "Aydınlatma rengi görünümü etkilemez."], "Gözlem görünür renk ilişkisini destekler; cismin kalıcı yapısal değişimini kanıtlamaz."),
    ]


def solar_energy_tasks():
    n = "tr-g06-fen-bilimleri-note-023"
    return [
        task(n, "comprehension", "Fotovoltaik panelin temel enerji dönüşümü hangisidir?", "Işık enerjisinden elektrik enerjisine",
             ["Kömür enerjisinden ışığa", "Elektrikten Güneş ışığına", "Ses enerjisinden nükleer enerjiye"], "Fotovoltaik hücreler gelen Güneş ışığından elektrik üretir."),
        task(n, "application", "Bir bina yalnız kullanım suyunu Güneş ile ısıtmak istiyor. Hangi teknoloji doğrudan uygundur?", "Güneş kolektörü",
             ["Rüzgâr türbini", "Kömür sobası", "Dizel jeneratör"], "Isıl kolektör Güneş ışınımını suya aktarılan ısı enerjisine dönüştürür."),
        task(n, "analysis", "Çatıdaki A sistemi elektrik sayacına, B sistemi sıcak su deposuna bağlıdır. Hangi eşleştirme uygundur?",
             "A fotovoltaik panel, B güneş kolektörüdür.", ["A güneş kolektörü, B rüzgâr türbinidir.", "İkisi de yalnız kömür yakar.", "B fotovoltaik paneldir ve yalnız ses üretir."], "Çıkış türleri sistemlerin enerji dönüşümünü ayırt eder."),
        task(n, "error-analysis", "Bir öğrenci “Her Güneş enerjisi düzeneği yalnız elektrik üretir.” diyor. Hangi düzeltme doğrudur?",
             "Güneş enerjisi fotovoltaik sistemle elektriğe, ısıl kolektörle ısıya dönüştürülebilir.", ["Güneş enerjisi hiçbir teknolojiyle kullanılamaz.", "Bütün sistemler yalnız sıcak su üretir.", "Dönüşüm türü kullanım amacından bağımsızdır."], "Aynı kaynak farklı teknolojilerde farklı enerji türlerine dönüştürülebilir."),
        task(n, "application", "Okul çatısındaki panel gölgede düşük üretim yapıyor. İlk iyileştirme hangisidir?",
             "Gölge durumunu ve panel yönelimini inceleyip güvenli biçimde uygun konuma almak", ["Paneli kapalı bir bodruma taşımak", "Üretimi ölçmeden panel sayısını rastgele azaltmak", "Güneş ışığını engelleyen örtü eklemek"], "Panel üretimi gelen ışık miktarı ve yönelimden etkilenir; çatı müdahalesi yetkili kişilerce yapılır."),
        task(n, "application", "İki tasarımdan biri enerji üretimini, diğeri panelin üretim ve kullanım ömrü sonu etkilerini de değerlendiriyor. Sürdürülebilirlik incelemesi için hangisi seçilmelidir?",
             "Yaşam döngüsü etkilerini de değerlendiren tasarım", ["Yalnız ilk gün üretimine bakan tasarım", "Hiç ölçüm yapmayan tasarım", "Gölge ve bakım koşullarını yok sayan tasarım"], "Yenilenebilir sistemler enerji kazancı yanında malzeme, bakım ve geri dönüşüm yönleriyle değerlendirilir."),
    ]


def expansion_tasks():
    n = "tr-g06-fen-bilimleri-note-024"
    return [
        task(n, "comprehension", "Maddelerin çoğu ısıtıldığında boyutlarında görülen değişim hangisidir?", "Genleşme",
             ["Büzülme", "Yoğunluğun zorunlu artması", "Kütlenin yok olması"], "Sıcaklık artışı taneciklerin ortalama hareketini artırır ve çoğu maddede boyut artışı görülür."),
        task(n, "application", "Metal kavanoz kapağı sıcak suyla ısıtıldığında neden daha kolay açılabilir?",
             "Metal kapak genleşerek kavanoz ağzına göre bir miktar genişleyebilir.", ["Kapak anında büzülür.", "Camın kütlesi sıfırlanır.", "Sıcak su metali yalıtkana dönüştürür."], "Metal ve camın genleşme davranışı farklı olabilir; kapak güvenli sıcaklıkta ısıtılır."),
        task(n, "analysis", "Yazın köprü birleşim boşluğu daralıyor, kışın genişliyor. Hangi çıkarım uygundur?",
             "Köprü parçaları sıcaklık artınca genleşip boşluğu daraltmaktadır.", ["Parçalar yazın büzülmektedir.", "Sıcaklık boyutu etkilememektedir.", "Boşluk yalnız rüzgâr nedeniyle değişir."], "Mevsimle tekrarlanan boşluk değişimi ısıl genleşme ve büzülmeyle uyumludur."),
        task(n, "application", "Köprü tasarımında genleşme boşluğu hangi amaçla kullanılmalıdır?",
             "Boşluk sıcaklıkla oluşan boyut değişimine yer vererek gerilme ve hasar riskini azaltır.", ["Boşluk sıcaklık etkisini artırmak için bırakılır.", "Metal hiç genleşmediği için boşluk süstür.", "Boşluk köprünün taşıma gücünü zorunlu olarak sıfırlar."], "Yapı tasarımında beklenen genleşme için pay bırakmak güvenliği destekler."),
        task(n, "application", "Elektrik tellerinin yazın sarkması dikkate alınarak montajda ne yapılmalıdır?",
             "Mevsimsel sıcaklık aralığına uygun hesaplanmış gerginlik payı bırakılmalıdır.", ["Tel her mevsim sonuna kadar gerilmelidir.", "Sıcaklık etkisi yok sayılmalıdır.", "Tel rastgele uzunlukta kesilmelidir."], "Genleşme ve büzülme öngörüsü güvenli mühendislik payıyla tasarıma katılır."),
        task(n, "analysis", "Eşit uzunluktaki X ve Y metalleri aynı miktarda ısıtıldığında X daha fazla uzuyor. Hangi sonuç desteklenir?",
             "Bu koşullarda X'in genleşme miktarı Y'den büyüktür.", ["Bütün metaller aynı oranda genleşir.", "Y kesinlikle daha çok ısınmıştır.", "X'in kütlesi yok olmuştur."], "Başlangıç boyu ve sıcaklık değişimi eşitken ölçülen uzama farkı madde türü etkisini destekler."),
        task(n, "comprehension", "Soğutulan bir metal çubukta genellikle hangi değişim beklenir?", "Büzülerek boyunun bir miktar kısalması",
             ["Sınırsız genleşmesi", "Kimyasal türünün zorunlu değişmesi", "Kütlesinin anında iki katına çıkması"], "Sıcaklık azaldığında çoğu metalde boyut küçülmesi görülür."),
        task(n, "error-analysis", "Bir öğrenci “Genleşmede maddenin kütlesi artar; bu yüzden boyu uzar.” diyor. Hangi düzeltme uygundur?",
             "Genleşme tanecik aralıklarının değişmesiyle ilgilidir; kapalı örneğin kütlesi zorunlu olarak artmaz.", ["Genleşmede bütün tanecikler yeni maddeye dönüşür.", "Boyut değişimi yalnız kütle eklenmesiyle olabilir.", "Isıtma tanecik hareketini etkilemez."], "Isıl genleşme madde miktarı eklemek değil, mevcut yapının boyut değişimidir."),
        task(n, "application", "Sıvılı termometrede sıcaklık artınca sıvı sütununun yükselmesi hangi ilkeye dayanır?",
             "Sıvının ısıl genleşmesine", ["Sıvının kütlesinin yok olmasına", "Camın ışık üretmesine", "Yer çekiminin tamamen kalkmasına"], "Termometre sıvısının hacmi sıcaklıkla değişir ve dar boruda seviye değişimi görünür olur."),
    ]


def phase_point_task():
    n = "tr-g06-fen-bilimleri-note-025"
    return [task(n, "analysis", "Saf bir madde ısıtılırken sıcaklık bir süre 65°C'de sabit kalıyor ve katı-sıvı birlikte gözleniyor. Bu sıcaklık neyi gösterir?",
                 "Verilen basınçta maddenin erime noktasını", ["Kaynama noktasının mutlaka 0°C olduğunu", "Maddenin artık enerji almadığını", "Yoğunluğunun 65 g/cm³ olduğunu"], "Hâl değişimi boyunca aktarılan enerji tanecik düzenini değiştirdiğinden sıcaklık sabit kalabilir; katı-sıvı birlikteliği erimeyi gösterir.")]


TASK_BUILDERS = [
    animal_tasks, human_reproduction_tasks, nervous_system_tasks, endocrine_tasks,
    puberty_tasks, system_health_tasks, reflection_tasks, mirror_tasks,
    absorption_tasks, white_light_tasks, object_color_tasks, solar_energy_tasks,
    expansion_tasks, phase_point_task,
]


def main() -> int:
    existing = [json.loads(x) for x in OUTPUT.read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(existing) != 700:
        raise RuntimeError("validated first seven batches must exist before batch 08")
    notes = read_notes_only(FEN_SOURCE)
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    tasks = [item for builder in TASK_BUILDERS for item in builder()]
    expected_modes = {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
    if len(tasks) != 100 or Counter(item["mode"] for item in tasks) != expected_modes:
        raise AssertionError((len(tasks), Counter(item["mode"] for item in tasks)))
    rows = [
        make_record(local, item, notes[item["note"]], labels, batch=8, number_base=700)
        for local, item in enumerate(tasks, 1)
    ]
    if Counter(row["correctIndex"] for row in rows) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer positions are not exactly balanced")
    OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + rows) + "\n",
        encoding="utf-8", newline="\n",
    )
    LABELS_OUTPUT.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({
        "batch": 8, "questions": 100, "science": 100, "total": 800,
        "modes": expected_modes, "labels": len(labels), "sourceQuestionReads": 0,
        "figureSpec": "1.3.0",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
