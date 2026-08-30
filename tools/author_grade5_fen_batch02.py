#!/usr/bin/env python3
"""Author Grade 5 science bank batch 02 (questions 101–200)."""
from __future__ import annotations

import json

import author_grade5_fen_batch01 as common


KNOWLEDGE = [
    ("tr-g05-fen-fb-5-1-1-1", "Güneş Dünya'dan çok daha büyük olduğu hâlde çok uzakta bulunduğu için gökyüzünde küçük görünür.",
     ["Güneş gerçekte Dünya'dan küçüktür; bu nedenle küçük görünür.", "Bir cismin görünür büyüklüğü uzaklığından hiç etkilenmez.", "Güneş her gün gerçek çapını değiştirdiği için bazen küçük görünür."],
     "Aynı büyüklükte iki topun biri yakına, diğeri uzağa yerleştirilerek Güneş'in görünüşü modelleniyor.",
     "Uzaktaki top görüş alanında daha küçük yer kaplıyor; büyüklüğü değişmediği hâlde görünüşü değişiyor.",
     "Görünür büyüklük gerçek büyüklüğün yanında gözlemciye uzaklığa da bağlıdır; Güneş çok büyük ve çok uzaktır."),
    ("tr-g05-fen-fb-5-1-2-1", "Ay hem kendi ekseni çevresinde döner hem Dünya çevresinde dolanır; bu hareketlerin süreleri yakın olduğu için Dünya'dan çoğunlukla aynı yüzü görülür.",
     ["Ay kendi ekseni çevresinde hiç dönmediği için aynı yüzünü gösterir.", "Ay yalnız Güneş çevresinde dolanır, Dünya ile birlikte hareket etmez.", "Ay'ın Dünya'ya bakan yüzü her gece rastgele değişir."],
     "Bir modelde Ay küresi Dünya çevresinde dolanırken üzerindeki işaret sürekli Dünya'ya dönük tutuluyor.",
     "İşaretin Dünya'ya dönük kalması için Ay küresi dolanırken kendi ekseni çevresinde de dönüyor.",
     "Ay'ın dönme ve Dünya çevresinde dolanma sürelerinin yakınlığı, aynı yüzün görülmesini açıklar."),
    ("tr-g05-fen-fb-5-1-2-2", "Ana evreler yaklaşık birer hafta arayla görülür ve yeni aydan sonra ilk dördün, dolunay ve son dördün sırası izlenir.",
     ["Dolunaydan hemen sonra yeni ay ve ardından ilk dördün görülür.", "Ana evrelerin tümü aynı gece art arda tamamlanır.", "Ay evrelerinin sırası her ay rastgele değişir."],
     "Bir takvimde yeni ay birinci gün, ilk dördün sekizinci gün ve dolunay on beşinci gün olarak işaretleniyor.",
     "Tarihler ana evreler arasında yaklaşık yedi günlük aralık bulunduğunu gösteriyor.",
     "Ay'ın ana evreleri düzenli bir döngü izler; ara evrelerle birlikte döngü yaklaşık dört haftada tamamlanır."),
    ("tr-g05-fen-fb-5-1-3-1", "Güneş-Dünya-Ay modelinde büyüklük ve uzaklıkların gerçek oranlarda gösterilememesi modelin bir sınırlılığıdır.",
     ["Bir model gerçeğin bütün özelliklerini eksiksiz ve aynı ölçekte göstermek zorundadır.", "Kürelerin renkleri doğruysa hareket merkezlerinin yanlış olması önemli değildir.", "Modelde uzaklıklar rastgele seçilse de gerçek oranları gösterdiği söylenebilir."],
     "Masa üzerindeki modelde Güneş ve Dünya küreleri birbirine çok yakın, Ay küresi ise Dünya kadar büyük yapılmış.",
     "Model hareketleri gösterebilir ancak küre büyüklükleri ve aralarındaki uzaklıklar gerçek oranları temsil etmiyor.",
     "Bilimsel model belirli özellikleri açıklamak için sadeleştirilir; hangi yönlerinin gerçeği temsil etmediği belirtilmelidir."),
    ("tr-g05-fen-fb-5-2-1-1", "Dinamometre ölçeğinde iki sayı arasındaki eşit bölmeler sayılarak her bölmenin newton değeri bulunur.",
     ["Ölçekte ara bölmelerin değeri her zaman 1 N kabul edilir.", "Bölme değeri bulunurken büyük değerden küçük değer çıkarılmaz.", "Gösterge hangi çizgide olursa olsun yalnız en büyük ölçek değeri okunur."],
     "0 N ile 10 N arasında beş eşit aralık bulunan dinamometrede gösterge üçüncü aralıkta duruyor.",
     "Her aralık 2 N'dur; üçüncü aralık 6 N değerini gösterir.",
     "Ölçek aralığı, iki numaralı değer farkının aradaki eşit aralık sayısına bölünmesiyle hesaplanır."),
    ("tr-g05-fen-fb-5-2-1-2", "Bir dinamometre ölçüm sınırından büyük kuvvetle zorlanırsa yayı kalıcı olarak uzayabilir ve ölçüm güvenilirliğini kaybeder.",
     ["Ölçüm sınırı aşılırsa dinamometre daha duyarlı hâle gelir.", "Yayın kalıcı uzaması sonraki ölçümlerin doğruluğunu etkilemez.", "Her dinamometre büyüklüğü ne olursa olsun sınırsız kuvvet ölçer."],
     "En fazla 10 N ölçen dinamometreye 16 N'luk yük asılıyor ve yük çıkarılınca gösterge sıfıra dönmüyor.",
     "Sıfır noktasındaki kayma, yayın esneklik sınırının aşılmış olabileceğini gösteriyor.",
     "Araç seçilirken kuvvet beklenen ölçüm aralığında olmalı; ölçüm sınırı güvenlik ve doğruluk için korunmalıdır."),
    ("tr-g05-fen-fb-5-2-2-1", "Ağırlık, gök cisminin cisme uyguladığı çekim kuvvetidir ve dinamometreyle newton cinsinden ölçülür.",
     ["Ağırlık cismin içerdiği madde miktarıdır ve eşit kollu teraziyle ölçülür.", "Bir cismin ağırlığı bulunduğu gök cisminin çekiminden bağımsızdır.", "Ağırlığın birimi kilogram, kütlenin birimi newtondur."],
     "Bir astronot aynı örnek taşı Dünya'da ve Ay'da dinamometreye asıyor.",
     "Ay'daki gösterge daha küçük değer verirken taşın madde miktarı değişmiyor.",
     "Çekim kuvveti değiştiğinde ağırlık değişir; kütle ise cisimden madde eklenmedikçe veya çıkarılmadıkça aynı kalır."),
    ("tr-g05-fen-fb-5-2-3-1", "Yürüme, yazı yazma ve fren yapma gibi birçok iş için sürtünme gereklidir; sürtünme her zaman zararlı değildir.",
     ["Sürtünme yalnız makineleri aşındırdığı için bütün durumlarda zararlıdır.", "Yürürken yer ile ayak arasında sürtünme olmasa da ileri hareket değişmez.", "Fren balatasındaki sürtünme aracın durma mesafesini uzatmak için kullanılır."],
     "Buzlu zeminde yürümek zorlaşırken pürüzlü zeminde ayak geriye kaymadan ilerliyor.",
     "Pürüzlü zeminin ayağa uyguladığı sürtünme, ayağın zemini itmesine karşılık ileri hareketi mümkün kılıyor.",
     "Sürtünmenin yararlı ya da zararlı oluşu kullanım amacına bağlıdır; gerektiği yerde kontrol edilir."),
    ("tr-g05-fen-fb-5-2-3-2", "Hava ve su da hareket eden cisimlere sürtünme uygular; akıcı biçimler bu direnci azaltabilir.",
     ["Sürtünme yalnız iki katı yüzey birbirine değdiğinde oluşur.", "Paraşütün geniş yüzeyi hava direncini azaltıp düşmeyi hızlandırır.", "Suda sivri ve düzgün biçim hareket direncini her zaman artırır."],
     "Aynı kütlede düz ve buruşturulmuş iki kâğıt aynı yükseklikten bırakılıyor.",
     "Düz kâğıt daha büyük yüzeyle havayı ittiği için daha yavaş düşüyor.",
     "Gazlar ve sıvılar akışkan sürtünmesi oluşturur; yüzey alanı ve biçim bu direnci etkiler."),
    ("tr-g05-fen-fb-5-3-1-1", "Çekirdek hücresel faaliyetleri yönetir, hücre zarı madde alışverişini düzenler, sitoplazma yaşamsal olayların gerçekleştiği ortamdır.",
     ["Hücre zarı yalnız hücreye renk verir ve hiçbir madde geçirmez.", "Çekirdek besin üretmek için yalnız bitki hücresinde bulunan yeşil yapıdır.", "Sitoplazma hücrenin dışında bulunan sert ve cansız kabuktur."],
     "Bir hücre modelinde yönetim merkezi, seçici sınır ve jel benzeri iç ortam ayrı renklerle gösteriliyor.",
     "Yönetim merkezi çekirdeği, seçici sınır hücre zarını, iç ortam sitoplazmayı temsil ediyor.",
     "Temel hücre yapıları farklı görevleri birlikte yürütür; yapı ile görev doğru eşleştirilmelidir."),
    ("tr-g05-fen-fb-5-3-1-2", "Mide bir organdır, sindirim sistemi bir organ sistemidir ve insan bir organizmadır.",
     ["Mide tek bir hücre, sindirim sistemi ise bir dokudur.", "İnsan yalnız bir organ sisteminden oluşan bir organdır.", "Organ sistemleri birleşerek doku, dokular birleşerek hücre oluşturur."],
     "Bir şemada mide, bağırsak ve diğer sindirim organları birlikte çalışan bir grup olarak gösteriliyor.",
     "Birden fazla organın ortak görev için çalışması organ sistemi düzeyini gösteriyor.",
     "Yapı düzeyi örnekleri sınıflandırılırken parçanın büyüklüğünden çok örgütlenme ve görev ilişkisi kullanılır."),
    ("tr-g05-fen-fb-5-3-2-1", "Oynamaz eklemler çok az ya da hiç hareket etmezken oynar eklemler geniş hareket sağlar; eklem türü göreve uygundur.",
     ["Kafatası kemikleri geniş hareket sağlayan oynar eklemlerle bağlıdır.", "Diz eklemi hiç hareket etmeyen oynamaz eklemdir.", "Vücuttaki bütün kemik bağlantıları aynı miktarda hareket eder."],
     "Kafatası kemikleri beyni sağlam biçimde korurken diz bükülüp açılabiliyor.",
     "Koruma gereken yerde hareket az, yürüme gereken dizde hareket fazladır.",
     "Eklemler kemiklerin bağlantı yeridir; hareket miktarları bulundukları bölgenin görevine göre değişir."),
    ("tr-g05-fen-fb-5-3-2-2", "Egzersiz öncesi ısınma, hareketleri doğru teknikle yapma ve dinlenme kas yaralanması riskini azaltır.",
     ["Yoğun egzersize aniden başlamak kasları yaralanmaya karşı hazırlar.", "Ağrıya rağmen aynı hareketi sürdürmek iyileşmeyi hızlandırır.", "Dinlenme ve uygun su tüketiminin kas sağlığıyla ilişkisi yoktur."],
     "Spor kulübünde bir grup ısınma yaparken diğer grup doğrudan en ağır çalışmaya başlıyor.",
     "Isınan grupta hareket açıklığı kademeli artıyor ve zorlanma şikâyeti daha az görülüyor.",
     "Kas sağlığı için yük kademeli artırılır; keskin ağrı ve yaralanmada etkinlik durdurulup yardım alınır."),
    ("tr-g05-fen-fb-5-4-1-1", "Bir ışık demetinin sisli ortamda düz bir çizgi gibi görülmesi, ışığın doğrusal yayılmasına günlük yaşam kanıtıdır.",
     ["Sis ışığı kaynaktan bağımsız olarak kıvrımlı yollara zorlar.", "Düz görülen ışık yolu ışığın yalnız sis tarafından üretildiğini kanıtlar.", "Işık demetinin yönü kaynağın konumuyla ilişkili değildir."],
     "Sahnede sis varken projektörden çıkan ışık huzmesi kaynaktan zemine uzanan düz bir yol olarak görülüyor.",
     "Havadaki küçük damlacıklar doğrusal yol üzerindeki ışığı görünür kılıyor.",
     "Işık homojen ortamda doğrusal ilerler; ortam parçacıkları ışık yolunu gözlemlemeyi kolaylaştırabilir."),
    ("tr-g05-fen-fb-5-4-2-1", "Bir maddenin saydamlığı kalınlık ve yapısına göre değişebilir; sınıflandırma gözlenen ışık geçişine dayanmalıdır.",
     ["Aynı maddeden yapılan her kalınlıktaki parça ışığı kesinlikle aynı miktarda geçirir.", "Bir maddenin adı biliniyorsa ışık deneyi yapmadan her örneği aynı sınıfa koymak yeterlidir.", "Işık geçişini karşılaştırırken kaynak uzaklığını ve kalınlığı değiştirmek adil deneydir."],
     "İnce ve kalın iki renkli plastik levha aynı el feneriyle deneniyor.",
     "İnce levhanın arkasında daha fazla, kalın levhanın arkasında daha az ışık ölçülüyor.",
     "Işık geçirme durumu madde yapısı ve örneğin kalınlığı gibi koşullarla birlikte değerlendirilir."),
    ("tr-g05-fen-fb-5-4-3-1", "Işık kaynağına yaklaştırılan opak cismin ekrandaki tam gölgesi genellikle büyür; ekrana yaklaştırıldığında küçülür.",
     ["Opak cismin yeri değişse de gölge büyüklüğü hiçbir zaman değişmez.", "Cisim ışık kaynağına yaklaştıkça ekrandaki gölge her zaman küçülür.", "Gölge büyüklüğü yalnız cismin renginden etkilenir."],
     "El feneri ve ekran sabitken top önce ışık kaynağına, sonra ekrana yaklaştırılıyor.",
     "Kaynağa yakın konumda daha büyük, ekrana yakın konumda daha küçük tam gölge ölçülüyor.",
     "Doğrusal yayılan ışınların oluşturduğu gölge, kaynak-cisim-ekran uzaklıklarına bağlıdır."),
    ("tr-g05-fen-fb-5-5-1-1", "Katıda tanecikler düzenli ve yakın, sıvıda yakın fakat hareketli, gazda ise daha uzak ve serbest hareketlidir.",
     ["Gaz tanecikleri katı taneciklerinden daha sıkı ve düzenli dizilir.", "Sıvı tanecikleri sabit konumlarında yalnız titreşir ve yer değiştiremez.", "Katı, sıvı ve gaz taneciklerinin aralık ve hareketleri tamamen aynıdır."],
     "Üç kutu modelinden birinde tanecikler düzenli-sık, birinde düzensiz-yakın, diğerinde seyrek gösteriliyor.",
     "Modeller sırasıyla katı, sıvı ve gaz hâllerinin tanecik düzenini temsil ediyor.",
     "Maddenin hâli değişirken tanecik türü değil, taneciklerin düzeni, aralığı ve hareketi değişir."),
    ("tr-g05-fen-fb-5-5-2-1", "Eşit sıcaklıktaki farklı miktarda maddelerin sıcaklıkları aynı olsa da içerdiği toplam enerji miktarları farklı olabilir.",
     ["Sıcaklıkları eşit olan bütün maddelerin miktarı ve toplam enerjisi kesinlikle aynıdır.", "Madde miktarı arttığında termometrenin gösterdiği sıcaklık kendiliğinden artar.", "Bir kabın sıcaklığı yalnız kabın hacmini gösterir."],
     "20 °C'deki bir bardak su ile 20 °C'deki büyük kova su karşılaştırılıyor.",
     "Termometreler aynı değeri gösterirken kovada çok daha fazla su bulunuyor.",
     "Sıcaklık taneciklerin ortalama hareketiyle ilişkili ölçüdür; madde miktarı ayrı bir değişkendir."),
    ("tr-g05-fen-fb-5-5-2-2", "Isı yalıtımı, sıcak ve soğuk maddeler arasındaki enerji aktarım hızını azaltır; aktarım yönünü tersine çevirmez.",
     ["Yalıtım ısıyı soğuktan sıcağa kendiliğinden pompalayan bir kaynaktır.", "Yalıtılmış kapta hiçbir koşulda ısı alışverişi olmaz.", "Yalıtım malzemesi sıcaklık farkını anında artırır."],
     "Aynı sıcak çorba biri yalıtımlı, biri metal iki kaba konuyor.",
     "Yalıtımlı kaptaki çorbanın sıcaklığı aynı sürede daha az azalıyor.",
     "Yalıtım ısı aktarımını yavaşlatır; sıcak madde yine çevreye enerji verir fakat daha uzun sürede soğur."),
    ("tr-g05-fen-fb-5-5-3-1", "Buharlaşma sıvının yüzeyinde farklı sıcaklıklarda gerçekleşebilir; kaynama ise sıvının her yerinde belirli koşullarda görülür.",
     ["Buharlaşma yalnız sıvı kaynama sıcaklığına ulaştığında başlar.", "Kaynama yalnız sıvının yüzeyinde sessizce gerçekleşir.", "Islak çamaşırın oda sıcaklığında kuruması donma olayıdır."],
     "Oda sıcaklığındaki ıslak bez zamanla kururken ocaktaki suda her yerde kabarcıklar oluşuyor.",
     "Bezde yüzeyden buharlaşma, sudaki yaygın kabarcıklarda kaynama gözleniyor.",
     "Buharlaşma ve kaynama sıvıdan gaza geçiştir ancak gerçekleşme biçimleri ve koşulları farklıdır."),
    ("tr-g05-fen-fb-5-5-4-1", "Tencere gövdesinde iletken metal, sapında ise ısıyı yavaş ileten malzeme kullanılması kullanım amacına uygundur.",
     ["Tencere sapı en iyi ısı ileten metalden yapılırsa güvenlik artar.", "Tencere gövdesi ısıyı hiç iletmeyen malzemeden yapılırsa yemek daha hızlı ısınır.", "Malzeme seçerken ısı iletkenliği kullanım amacıyla ilişkilendirilmez."],
     "Tasarımcı yemeğin hızlı ısınmasını, sapın ise elle güvenli tutulmasını istiyor.",
     "Metal gövde ısıyı yemeğe aktarırken yalıtkan sap ele ulaşan ısıyı azaltıyor.",
     "Bir üründe farklı parçalar farklı görevler üstlenebilir; malzeme özelliği parçanın görevine göre seçilir."),
    ("tr-g05-fen-fb-5-5-4-2", "Bir yalıtım deneyinde kap, su miktarı, başlangıç sıcaklığı ve süre sabit tutulup yalnız yalıtım malzemesi değiştirilmelidir.",
     ["Yalıtım malzemesiyle birlikte su miktarını da değiştirmek adil karşılaştırmadır.", "Başlangıç sıcaklıkları farklı kapların son sıcaklıklarını doğrudan karşılaştırmak yeterlidir.", "Deneyde ölçüm süresini her kap için rastgele seçmek sonucu güvenilir yapar."],
     "Pamuk, yün ve köpükle sarılan üç özdeş kapta yalıtım başarısı karşılaştırılacak.",
     "Tüm kaplarda eşit su, eşit başlangıç sıcaklığı ve eşit bekleme süresi kullanılıyor.",
     "Kontrollü deneyde bağımsız değişken yalıtım malzemesi, bağımlı değişken sıcaklık değişimidir."),
    ("tr-g05-fen-fb-5-6-1-1", "Devre sembolleri çizimin yönü değişse de elemanın türünü korur; önemli olan sembol ve bağlantı ilişkisidir.",
     ["Pil sembolü kâğıtta döndürülünce ampul sembolüne dönüşür.", "Şemadaki kablo çizgilerinin uzunluğu gerçek kabloyla bire bir aynı olmalıdır.", "Sembolün sayfadaki rengi devre elemanının görevini tek başına belirler."],
     "Aynı devre biri yatay, diğeri dik yerleşimli iki şemayla gösteriliyor.",
     "Sembollerin yönleri farklı olsa da pil, anahtar ve ampul arasındaki bağlantılar aynı kalıyor.",
     "Devre şeması fiziksel yerleşimi ölçekli çizmek yerine eleman türünü ve bağlantı düzenini aktarır."),
    ("tr-g05-fen-fb-5-6-1-2", "Çalışmayan basit devrede pilin yönü, ampulün temas noktaları, kablo bağlantıları ve anahtarın durumu sistemli biçimde kontrol edilmelidir.",
     ["Ampul yanmıyorsa hiçbir bağlantıya bakmadan yalnız pili boyamak gerekir.", "Açık anahtar devreyi tamamladığı için ilk kontrol onu açık bırakmaktır.", "Kablolardan biri bağlı değilse devre yine kapalı yol oluşturur."],
     "Yeni kurulan devrede sağlam pil ve ampul olmasına rağmen ampul yanmıyor.",
     "Kontrolde kablonun ampulün metal temas noktasına değmediği bulunuyor.",
     "Arıza aramada elemanlar ve bağlantılar sırayla kontrol edilir; kapalı iletken yol sağlanmadan ampul yanmaz."),
    ("tr-g05-fen-fb-5-6-2-1", "Ampul parlaklığı deneyinde değiştirilen değişken pil sayısıysa ampul sayısı ve ampul türü sabit tutulmalıdır.",
     ["Pil sayısının etkisini ölçerken her denemede ampul sayısı da değiştirilmelidir.", "Kontrol edilen değişkenler deney sonucunu etkilemeyeceği için sabit tutulmaz.", "Parlaklık gözlemi yapılmadan yalnız devre çiziminin güzelliği karşılaştırılır."],
     "Bir öğrenci bir ve iki pilli devrelerin parlaklığını karşılaştırmak istiyor.",
     "İki devrede de aynı tür tek ampul ve aynı bağlantı düzeni kullanılıyor; yalnız pil sayısı değişiyor.",
     "Tek değişkenli deney, gözlenen parlaklık farkını değiştirilen pil sayısıyla ilişkilendirmeyi sağlar."),
    ("tr-g05-fen-fb-5-7-1-1", "Atık yağ, pil, ilaç ve elektronik parçalar lavaboya veya normal çöpe değil, uygun toplama noktalarına verilmelidir.",
     ["Kullanılmış kızartma yağı suyla karıştırılıp lavaboya dökülmelidir.", "Atık piller metal içermediği için bahçeye bırakılabilir.", "Son kullanma tarihi geçmiş ilaçlar gıda atığı kutusuna atılmalıdır."],
     "Evde atık yağ, bitmiş pil ve bozuk telefon birikiyor.",
     "Belediyenin ayrı yağ, pil ve elektronik atık toplama noktaları bulunduğu belirleniyor.",
     "Tehlikeli atıkların ayrı toplanması su, toprak ve canlıların zararlı maddelere maruz kalmasını azaltır."),
    ("tr-g05-fen-fb-5-7-1-2", "Bir ürünün onarılması veya başka amaçla yeniden kullanılması, yeni ürün ve atık gereksinimini azaltabilir.",
     ["Küçük arızası olan her ürün doğrudan atılmalı ve yenisi alınmalıdır.", "Yeniden kullanım ile geri dönüşüm tamamen aynı işlemdir; ikisinde de ürün ham maddeye parçalanır.", "Onarım kaynak ve enerji kullanımını her koşulda artırdığı için yapılmamalıdır."],
     "Fermuarı bozulan çanta onarılıyor, boş kavanozlar saklama kabı olarak kullanılıyor.",
     "İki uygulamada da ürünler ham madde işlemine girmeden kullanımda kalıyor.",
     "Yeniden kullanım ürünün ömrünü uzatır; geri dönüşüm ise atığı işleyerek yeni ham madde elde eder."),
    ("tr-g05-fen-fb-5-7-1-3", "Atık planının başarısı, oluşan atık miktarı ve doğru ayrılan atık oranı gibi ölçülebilir verilerle izlenmelidir.",
     ["Atık yönetimi planı uygulanınca sonuç ölçmeye gerek yoktur.", "Başarı yalnız kutuların renginin beğenilmesiyle belirlenir.", "Toplam atık artıp doğru ayırma azalırsa plan kesinlikle başarılıdır."],
     "Okul plan öncesi ve sonrası haftalık çöp kütlesini ve doğru ayrılan ambalajları kaydediyor.",
     "Toplam çöp azalırken doğru ayrılan ambalaj oranı yükseliyor.",
     "Ölçülebilir göstergeler planın etkisini kanıtlar ve hangi adımın düzeltilmesi gerektiğini gösterir."),
]


def main() -> int:
    common.NOTE_BY_ID = common.read_notes()
    missing = sorted({entry[0] for entry in KNOWLEDGE} - set(common.NOTE_BY_ID))
    if missing or len(KNOWLEDGE) != 28:
        raise RuntimeError(f"knowledge/note coverage error: missing={missing} count={len(KNOWLEDGE)}")
    existing = [json.loads(line) for line in common.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 100 or any("-b01-" not in str(row.get("id")) for row in existing):
        raise RuntimeError("batch 01 must be regenerated before batch 02")
    labels = json.loads(common.LABELS_OUTPUT.read_text(encoding="utf-8"))
    rows = []
    for local in range(1, 101):
        global_number = 100 + local
        rows.append(common.make_question(
            global_number, KNOWLEDGE[(local - 1) % len(KNOWLEDGE)],
            common.MODE_SEQUENCE[local - 1], common.LEVEL_SEQUENCE[local - 1], labels,
            batch=2, local_number=local, knowledge_count=len(KNOWLEDGE),
        ))
    common.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    common.LABELS_OUTPUT.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({"questions": len(rows), "total": len(existing) + len(rows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
