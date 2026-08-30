#!/usr/bin/env python3
"""Author Grade 5 science bank batch 01 (100 independent questions).

The records are written from curriculum concepts and lesson-note anchors. They
do not read or transform lesson-package questions.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from build_unique_question_banks import ROOT


SOURCE = ROOT / "turkiye/5-sinif/fen-bilimleri/fen-bilimleri-tum.jsonl"
OUTPUT = ROOT / "authoring/question-bank-blueprints/grade-5.jsonl"
LABELS_OUTPUT = ROOT / "authoring/question-bank-blueprints/grade-5-labels.json"


# note id, correct scientific conclusion, three misconceptions, scenario,
# observable evidence, explanation
KNOWLEDGE = [
    ("tr-g05-fen-fb-5-1-1-1", "Güneş, çok sıcak gazlardan oluşan küresel bir yıldızdır ve kendi ekseni çevresinde döner.",
     ["Güneş katı yüzeyli bir gezegendir ve dönmez.", "Güneş ışığını Dünya'dan yansıtan bir uydudur.", "Güneş yalnız çevresindeki gezegenlerin yansıttığı ışıkla görünür."],
     "Bir gözlemevinde Güneş lekelerinin günler içinde disk üzerinde yer değiştirdiği kaydediliyor.",
     "Lekelerin doğudan batıya düzenli yer değiştirmesi, Güneş'in dönme hareketine kanıt sağlar.",
     "Güneş bir yıldızdır; çok sıcak gazlardan oluşur, ışık ve ısı yayar, kendi ekseni çevresinde döner."),
    ("tr-g05-fen-fb-5-1-2-1", "Ay kendi ışığını üretmez; Güneş'ten aldığı ışığı yansıtır ve yüzeyinde kraterler bulunur.",
     ["Ay parlak göründüğünde kendi ürettiği ışığı yayar.", "Ay'ın yüzeyi tamamen düz ve kratersizdir.", "Ay bir yıldız olduğu için Dünya'dan daha büyüktür."],
     "Bir öğrenci Ay'ın karanlık bölümünün ışık saçmadığını, aydınlık bölümünün Güneş'e dönük olduğunu gözlüyor.",
     "Aydınlık kısmın Güneş'in konumuna göre değişmesi, görülen ışığın yansıyan Güneş ışığı olduğunu gösterir.",
     "Ay doğal uydudur; kendi ışığı yoktur, Güneş ışığını yansıtır ve çarpma kraterleri taşır."),
    ("tr-g05-fen-fb-5-1-2-2", "Ay'ın evreleri, Güneş'in aydınlattığı yarısının Dünya'dan görülen bölümünün değişmesiyle oluşur.",
     ["Ay'ın evreleri Dünya'nın Ay'a her hafta farklı renkte ışık göndermesiyle oluşur.", "Ay evre değiştirirken gerçek büyüklüğü küçülüp büyür.", "Ay'ın evreleri bulutların Ay'ın parçalarını kalıcı olarak örtmesidir."],
     "Dört hafta boyunca aynı saatte çekilen Ay fotoğraflarında aydınlık bölümün biçimi düzenli değişiyor.",
     "Fotoğraflardaki döngü yeni ay, ilk dördün, dolunay ve son dördün sırasıyla tekrar ediyor.",
     "Ay'ın yarısı her zaman Güneş tarafından aydınlatılır; Dünya'dan görülen aydınlık pay evreyi belirler."),
    ("tr-g05-fen-fb-5-1-3-1", "Bir modelde Dünya Güneş çevresinde, Ay Dünya çevresinde dolanırken üçü de kendi ekseni çevresinde döner.",
     ["Modelde Güneş Dünya çevresinde, Dünya da Ay çevresinde dolanmalıdır.", "Ay yalnız kendi ekseninde döner; Dünya çevresinde dolanmaz.", "Dünya ve Ay hareketsizdir; yalnız Güneş onların çevresinde dolaşır."],
     "Üç küreyle kurulacak modelde öğrenciler dönme ve dolanma hareketlerini oklarla gösterecek.",
     "Büyük yörünge Dünya'nın Güneş çevresindeki, küçük yörünge Ay'ın Dünya çevresindeki dolanmasını temsil eder.",
     "Güneş-Dünya-Ay modelinde gök cisimlerinin büyüklükleri ve hareket merkezleri doğru temsil edilmelidir."),
    ("tr-g05-fen-fb-5-2-1-1", "Kuvvet dinamometreyle ölçülür ve birimi newtondur.",
     ["Kuvvet termometreyle ölçülür ve birimi derecedir.", "Kuvvet eşit kollu teraziyle ölçülür ve birimi kilogramdır.", "Kuvvet dereceli silindirle ölçülür ve birimi litredir."],
     "Bir yaylı ölçüm aracına asılan cisim göstergede 6 değerini gösteriyor.",
     "Araç dinamometredir; ölçek değeri 6 N olarak okunur.",
     "Dinamometrede yayın uzaması kuvvetin büyüklüğünü gösterir; sonuç newton (N) ile yazılır."),
    ("tr-g05-fen-fb-5-2-1-2", "Dinamometrenin ölçüm aralığı ve duyarlılığı kullanılan yayın özelliklerine bağlıdır.",
     ["Her yay, kalınlığı ve uzunluğu ne olursa olsun aynı aralığı ölçer.", "Yayın uzaması kuvvetten etkilenmez; yalnız renginden etkilenir.", "Dinamometrede ölçek gerekmez çünkü kuvvet gözle tam belirlenir."],
     "İki dinamometreden birinde ince, diğerinde kalın yay kullanılarak eşit kuvvet uygulanıyor.",
     "İnce yay daha fazla uzarken kalın yay daha az uzuyor; ölçekler buna göre ayrı kalibre edilmelidir.",
     "Yayın cinsi, kalınlığı ve uzunluğu uzamayı etkiler; tasarımda ölçüm sınırı aşılmamalıdır."),
    ("tr-g05-fen-fb-5-2-2-1", "Kütle madde miktarıdır ve değişmez; ağırlık gök cisminin çekimine bağlı bir kuvvettir.",
     ["Kütle ve ağırlık her yerde aynı birimle ölçülen aynı büyüklüktür.", "Ay'a gidildiğinde cismin kütlesi azalır, ağırlığı değişmez.", "Ağırlık eşit kollu teraziyle kilogram cinsinden ölçülür."],
     "Aynı kaya Dünya'da ve Ay'da ölçülüyor; eşit kollu terazi sonucu aynı, dinamometre sonucu farklı çıkıyor.",
     "Madde miktarı değişmediği için kütle aynı kalır; Ay'ın çekimi daha küçük olduğundan ağırlık azalır.",
     "Kütle kilogramla, ağırlık newtonla ifade edilir; ağırlık bulunduğu yerdeki çekime göre değişir."),
    ("tr-g05-fen-fb-5-2-3-1", "Sürtünme kuvveti harekete zıt yönde etki eder; hareketi yavaşlatabilir, ısı ve aşınma oluşturabilir.",
     ["Sürtünme her zaman hareket yönünde etki ederek cismi hızlandırır.", "Sürtünmenin hareket ve yüzey sıcaklığı üzerinde hiçbir etkisi yoktur.", "Sürtünme yalnız sıvılarda görülür, katı yüzeylerde oluşmaz."],
     "Aynı oyuncak araba pürüzlü ve düzgün zeminde eşit hızla bırakılıyor.",
     "Araba pürüzlü zeminde daha kısa mesafede duruyor ve tekerlekleri daha çok ısınıyor.",
     "Pürüzlü yüzeyde sürtünme genellikle daha büyüktür; mekanik enerjinin bir bölümü ısıya dönüşür."),
    ("tr-g05-fen-fb-5-2-3-2", "Gerektiğinde yüzeyi pürüzlendirmek sürtünmeyi artırır; yağlamak veya tekerlek kullanmak sürtünmeyi azaltır.",
     ["Ayakkabı tabanını düzleştirmek kaymayı önlemek için sürtünmeyi artırır.", "Bisiklet zincirini yağlamak sürtünmeyi artırıp hareketi zorlaştırır.", "Kış lastiğindeki derin kanallar yol tutuşunu azaltmak için yapılır."],
     "Bir okul rampası yağmurda kayganlaşıyor, bir kapının menteşesi ise zor hareket ediyor.",
     "Rampaya kaymaz şerit eklemek tutunmayı artırır; menteşeyi uygun yağla yağlamak hareketi kolaylaştırır.",
     "Sürtünme amaca göre artırılır veya azaltılır; tek bir yöntem her durumda doğru değildir."),
    ("tr-g05-fen-fb-5-3-1-1", "Bitki hücresinde hücre zarı, sitoplazma ve çekirdeğe ek olarak hücre duvarı ve kloroplast bulunabilir.",
     ["Hayvan hücresinde hücre duvarı ve kloroplast, bitki hücresinde yalnız çekirdek bulunur.", "Bitki ve hayvan hücrelerinin hiçbir ortak yapısı yoktur.", "Kloroplast bütün hayvan hücrelerinde besin üretir."],
     "Mikroskop görüntülerinden birinde köşeli sınırlar ve yeşil yapılar, diğerinde esnek sınırlar görülüyor.",
     "Köşeli sınır hücre duvarına, yeşil yapılar kloroplasta işaret ederek bitki hücresini ayırt eder.",
     "İki hücre tipi temel yapıları paylaşır; hücre duvarı ve kloroplast bitki hücresi için ayırt edicidir."),
    ("tr-g05-fen-fb-5-3-1-2", "Canlılarda yapı düzeyi hücre, doku, organ, sistem ve organizma sırasıyla ilerler.",
     ["Canlıların yapı sırası organ, hücre, sistem, doku ve organizmadır.", "Bir doku farklı sistemlerin birleşmesiyle oluşur.", "Organizma yalnız tek bir hücre parçasından oluşur."],
     "Kas hücreleri bir araya gelerek kas dokusunu, dokular da kalp gibi bir organı oluşturuyor.",
     "Benzer hücrelerden doku, farklı dokulardan organ, birlikte çalışan organlardan sistem oluşur.",
     "Küçük yapı birimleri düzenli biçimde birleşerek daha karmaşık canlılık düzeylerini oluşturur."),
    ("tr-g05-fen-fb-5-3-2-1", "Destek ve hareket sistemi kemik, eklem ve kasların birlikte çalışmasıyla vücudu destekler ve hareket sağlar.",
     ["Hareketi yalnız kemikler sağlar; kas ve eklemlerin görevi yoktur.", "Eklemler kasları sindirerek enerji üretir.", "Kaslar iskeletle bağlantı kurmadan kemikleri uzaktan hareket ettirir."],
     "Bir öğrenci dirseğini bükerken üst kol kaslarından birinin kısalıp diğerinin gevşediğini gözlüyor.",
     "Kasların kemiklere bağlı çalışması ve dirsek ekleminin hareket noktası olması kolun bükülmesini sağlar.",
     "İskelet destek ve koruma sağlar; eklemler hareket alanı, kaslar çekme kuvveti oluşturur."),
    ("tr-g05-fen-fb-5-3-2-2", "Dengeli beslenme, uygun egzersiz, doğru duruş ve güvenli yük taşıma destek-hareket sistemi sağlığını korur.",
     ["Ağır çantayı sürekli tek omuzda taşımak omurga sağlığını korur.", "Isınmadan yoğun egzersize başlamak kas yaralanması riskini azaltır.", "Kemik sağlığı için hareketten kaçınıp yalnız şekerli içecek tüketmek gerekir."],
     "Bir öğrencinin çantası vücut ağırlığına göre ağır ve masa başındaki duruşu sürekli eğik.",
     "Çantayı hafifletmek, iki askıyı kullanmak ve çalışma yüksekliğini düzeltmek riski azaltır.",
     "Kas ve kemik sağlığı düzenli davranışlarla korunur; ağrı veya yaralanmada yetişkin ve sağlık uzmanına başvurulur."),
    ("tr-g05-fen-fb-5-4-1-1", "Işık homojen bir ortamda doğrusal yollar boyunca yayılır.",
     ["Işık kaynaktan çıktıktan sonra engel olmadan rastgele kıvrılarak ilerler.", "Işık yalnız karanlıkta doğrusal, aydınlıkta dairesel yayılır.", "Işık bir kaynaktan çıkamaz; cisimler ışığı kendiliğinden görür."],
     "Üç delikli kart arka arkaya diziliyor; mum yalnız delikler aynı doğrultudayken görülüyor.",
     "Deliklerden biri yana kaydırıldığında ışık göze ulaşmıyor; bu sonuç doğrusal yayılmayı destekliyor.",
     "Işının doğrusal ilerlemesi, hizalanmış delik deneyinde ve gölge oluşumunda gözlenebilir."),
    ("tr-g05-fen-fb-5-4-2-1", "Saydam maddeler ışığın çoğunu, yarı saydam maddeler bir bölümünü geçirir; opak maddeler ışığı geçirmez.",
     ["Buzlu cam bütün ışığı geçirir ve görüntüyü saydam cam kadar net gösterir.", "Tahta levha ışığın çoğunu geçirdiği için saydamdır.", "Saydam, yarı saydam ve opak maddeler ışığı aynı miktarda geçirir."],
     "El feneri cam, yağlı kâğıt ve tahta levhaya ayrı ayrı tutuluyor.",
     "Cam arkasında parlak ve net, yağlı kâğıt arkasında zayıf, tahta arkasında ışık görülmüyor.",
     "Maddeler ışığı geçirme miktarına göre saydam, yarı saydam ve opak olarak sınıflandırılır."),
    ("tr-g05-fen-fb-5-4-3-1", "Tam gölge, opak bir cismin ışık kaynağından gelen ışığı engellemesiyle oluşur.",
     ["Tam gölge saydam cismin bütün ışığı geçirmesiyle oluşur.", "Gölge oluşması için ışık kaynağına gerek yoktur.", "Opak cisim kaldırıldığında aynı yerde tam gölge büyüyerek kalır."],
     "Bir top, el feneri ile beyaz ekran arasına yerleştiriliyor.",
     "Top ışığı geçirmediği için ekranda ışık alamayan koyu bir bölge oluşuyor.",
     "Işık kaynağı, opak cisim ve ekranın konumları tam gölgenin yerini ve büyüklüğünü etkiler."),
    ("tr-g05-fen-fb-5-5-1-1", "Maddeler taneciklerden oluşur; tanecikler arasında boşluk bulunur ve tanecikler hareketlidir.",
     ["Madde kesintisiz tek parçadır ve hiçbir taneciği yoktur.", "Tanecikler arasında hiç boşluk bulunmaz ve bütün hâllerde hareketsizdir.", "Yalnız katılar taneciklidir; sıvı ve gazların taneciği yoktur."],
     "Bir damla mürekkep karıştırılmadan suyun her yanına zamanla dağılıyor.",
     "Mürekkep taneciklerinin su tanecikleri arasındaki boşluklarda hareket etmesi yayılmayı açıklar.",
     "Katı, sıvı ve gazların tümü taneciklidir; tanecik düzeni, aralığı ve hareketi hâle göre değişir."),
    ("tr-g05-fen-fb-5-5-2-1", "Sıcaklık termometreyle ölçülen bir değerdir; ısı ise sıcaklık farkı nedeniyle aktarılan enerjidir.",
     ["Isı ve sıcaklık aynı büyüklüktür ve ikisi de termometreyle derece olarak ölçülür.", "Sıcaklık maddeler arasında akan bir enerji türüdür.", "Isı alışverişi için sıcaklık farkı bulunmamalıdır."],
     "Biri küçük, biri büyük iki kap su aynı sıcaklıkta ölçülüyor fakat ısıtılmaları için farklı enerji gerekiyor.",
     "Termometreler aynı sıcaklığı gösterse de madde miktarları farklı olduğundan aktarılan enerji miktarı farklı olabilir.",
     "Sıcaklık ve ısı ilişkili fakat farklı kavramlardır; sıcaklık farkı ısı aktarımını yönlendirir."),
    ("tr-g05-fen-fb-5-5-2-2", "Isı, sıcaklığı yüksek maddeden sıcaklığı düşük maddeye aktarılır ve dengeye yaklaşılır.",
     ["Isı her zaman soğuk maddeden sıcak maddeye kendiliğinden akar.", "Temas eden farklı sıcaklıktaki maddeler sıcaklıklarını hiç değiştirmez.", "Isı alışverişinde iki maddenin de sıcaklığı sınırsız yükselir."],
     "Sıcak metal kaşık oda sıcaklığındaki suya bırakılıyor.",
     "Kaşık soğurken su ısınıyor; bir süre sonra sıcaklıkları birbirine yaklaşıyor.",
     "Net ısı aktarımı sıcaktan soğuğa olur ve sıcaklık farkı azaldıkça termal dengeye yaklaşılır."),
    ("tr-g05-fen-fb-5-5-3-1", "Erime katıdan sıvıya, donma sıvıdan katıya; buharlaşma sıvıdan gaza, yoğuşma gazdan sıvıya geçiştir.",
     ["Erime sıvının gaza, donma gazın sıvıya dönüşmesidir.", "Yoğuşma katının doğrudan sıvıya dönüşmesidir.", "Buharlaşma yalnız suyun donarak katılaşmasıdır."],
     "Soğuk şişenin dışında su damlaları oluşurken tabaktaki buz zamanla suya dönüşüyor.",
     "Şişedeki damlalar havadaki su buharının yoğuşması, buzun suya dönüşmesi erimedir.",
     "Hâl değişimlerini adlandırırken başlangıç ve son hâl birlikte dikkate alınmalıdır."),
    ("tr-g05-fen-fb-5-5-4-1", "Metaller genellikle ısıyı iyi iletir; tahta ve plastik gibi maddeler ısıyı daha yavaş iletir.",
     ["Tahta kaşık ısıyı metal kaşıktan her zaman daha hızlı iletir.", "Bütün maddeler ısıyı aynı hızda iletir.", "Isı iletkenliği maddenin cinsinden bağımsızdır."],
     "Eşit uzunluktaki metal ve tahta çubukların bir ucu sıcak suya daldırılıyor.",
     "Metal çubuğun diğer ucu daha kısa sürede ısınıyor.",
     "Isı iletim hızı maddenin cinsine bağlıdır; bu özellik kullanım amacına göre malzeme seçiminde kullanılır."),
    ("tr-g05-fen-fb-5-5-4-2", "Isı yalıtımında ısıyı yavaş ileten malzemeler ve aralarında hapsolmuş hava katmanları kullanılır.",
     ["Bina yalıtımında yalnız çok iyi ısı ileten kalın metal levhalar kullanılmalıdır.", "Yalıtım, iç ve dış ortam arasındaki ısı aktarımını hızlandırmayı amaçlar.", "Çift cam arasındaki hava boşluğu yalıtımı azaltmak için bırakılır."],
     "İki özdeş kaptan biri yünle sarılıyor, diğeri açık bırakılıyor; ikisine de sıcak su konuyor.",
     "Yünle sarılı kaptaki su aynı sürede daha az soğuyor.",
     "Yalıtım ısı aktarımını tamamen yok etmez, yavaşlatır; enerji tasarrufu ve konfor sağlar."),
    ("tr-g05-fen-fb-5-6-1-1", "Devre şemalarında pil, ampul, anahtar ve bağlantı kablosu herkesçe aynı anlaşılan standart sembollerle gösterilir.",
     ["Devre elemanları her çizimde rastgele resimlerle gösterilmelidir.", "Standart semboller yalnız kablonun rengini belirtir, elemanı belirtmez.", "Bir devre şemasında pil ve ampul aynı sembolle gösterilir."],
     "İki öğrenci farklı ülkelerde aynı elektrik devresi şemasını okuyor.",
     "Standart semboller sayesinde iki öğrenci de elemanları ve bağlantıları aynı biçimde belirliyor.",
     "Semboller devrenin fiziksel görünüşünü değil, eleman türünü ve elektriksel bağlantıyı açıkça gösterir."),
    ("tr-g05-fen-fb-5-6-1-2", "Ampulün yanması için devre elemanları iletken kablolarla kapalı bir yol oluşturacak biçimde bağlanmalıdır.",
     ["Ampulün yanması için anahtar açık ve devre yolu kesik olmalıdır.", "Kablonun yalnız ampulün camına değmesi kapalı devre kurar.", "Pil devreden çıkarıldığında ampul aynı parlaklıkta yanmaya devam eder."],
     "Pil, anahtar ve ampul bağlıyken anahtar kapatıldığında ampul yanıyor; anahtar açıldığında sönüyor.",
     "Kapalı anahtar akım için kesintisiz yol oluşturur; açık anahtar yolu keser.",
     "Çalışan basit devrede enerji kaynağı, alıcı ve bağlantılar kapalı bir iletim yolu oluşturur."),
    ("tr-g05-fen-fb-5-6-2-1", "Özdeş ampullerle kurulan devrede pil sayısı artarsa parlaklık artabilir; aynı pil sayısında ampul sayısı artarsa parlaklık azalabilir.",
     ["Pil sayısı artsa da ampul parlaklığı hiçbir koşulda değişmez.", "Aynı devrede ampul sayısı arttıkça her ampul kesinlikle daha parlak yanar.", "Parlaklığı karşılaştırırken aynı anda pil ve ampul sayısını değiştirmek tek değişkenli deneydir."],
     "Bir grup özdeş ampul ve pillerle, her denemede yalnız bir değişkeni değiştirerek parlaklığı karşılaştırıyor.",
     "İki pilli tek ampul, bir pilli tek ampulden daha parlak; bir pilli iki ampulün her biri daha sönük gözleniyor.",
     "Adil deneyde yalnız pil ya da ampul sayısı değiştirilir, diğer koşullar sabit tutulur."),
    ("tr-g05-fen-fb-5-7-1-1", "Evsel atıklar kâğıt, cam, metal, plastik, organik ve tehlikeli türlerine göre ayrı toplanmalıdır.",
     ["Atık pil ile sebze kabuğu aynı organik atık kutusuna atılmalıdır.", "Cam şişe, yemek artığı ve elektronik atık ayrılmadan tek kutuda toplanmalıdır.", "Tehlikeli evsel atıklar toprağa gömülürse güvenli biçimde yok olur."],
     "Okulda atık pil, muz kabuğu, cam kavanoz ve gazete için ayrı kutular hazırlanıyor.",
     "Her atığın uygun kutuya ayrılması geri kazanımı kolaylaştırır ve tehlikeli maddelerin çevreye karışmasını önler.",
     "Kaynağında ayırma, atık yönetiminin ilk uygulama adımlarındandır; pil ve elektronik atık özel toplama noktalarına gider."),
    ("tr-g05-fen-fb-5-7-1-2", "Geri dönüşüm ham madde ve enerji kullanımını azaltabilir; ancak önce tüketimi azaltma ve yeniden kullanım düşünülmelidir.",
     ["Geri dönüşüm sınırsız tüketimin çevreye hiçbir etkisi olmayacağını garanti eder.", "Kullanılabilir bir ürünü hemen atmak kaynak tasarrufunun en etkili yoludur.", "Geri dönüştürülebilir maddeleri kirli organik atıklarla karıştırmak geri kazanımı kolaylaştırır."],
     "Bir sınıf tek kullanımlık şişe tüketimini azaltıp matara kullanıyor ve kalan şişeleri ayrı topluyor.",
     "Matara kullanımı atık oluşumunu önler; ayrı toplama ise oluşan atığın geri dönüşümünü kolaylaştırır.",
     "Kaynakları korumada azaltma ve yeniden kullanım çoğu zaman geri dönüşümden önce gelir."),
    ("tr-g05-fen-fb-5-7-1-3", "Atık yönetiminde önleme, azaltma, yeniden kullanım, geri dönüşüm ve güvenli bertaraf sırası gözetilir.",
     ["Atık yönetiminin ilk adımı bütün ürünleri kullandıktan hemen sonra çöpe atmaktır.", "Yeniden kullanılabilecek ürünleri yakmak kaynakları korur.", "Atıkları türüne bakmadan doğaya bırakmak güvenli bertaraftır."],
     "Bir okul şenliği için tabak seçimi, artan yiyecekler ve ambalajlar hakkında plan hazırlanıyor.",
     "Yıkanabilir tabak seçmek atığı önler; uygun artıkları değerlendirmek ve ambalajı ayırmak sonraki basamaklardır.",
     "İyi atık planı yalnız çöp kutusunu değil, satın alma öncesinden güvenli son işleme kadar bütün süreci kapsar."),
]


MODE_COUNTS = (("comprehension", 25), ("application", 35), ("analysis", 25), ("error-analysis", 15))
MODE_SEQUENCE = [mode for mode, count in MODE_COUNTS for _ in range(count)]
# Difficulty is coupled to the actual cognitive mode, not assigned as a label
# after the fact. Totals remain exactly 20/25/30/20/5.
LEVEL_SEQUENCE = (
    [1] * 15 + [2] * 10 +                         # comprehension (25)
    [1] * 5 + [2] * 15 + [3] * 15 +              # application (35)
    [3] * 10 + [4] * 10 + [5] * 5 +              # analysis (25)
    [3] * 5 + [4] * 10                            # error analysis (15)
)
OPENERS = (
    "Bir bilim günlüğünde bu konu için doğru bilgi aranıyor.",
    "Sınıf tartışmasında kanıta dayalı bir sonuca ulaşılacak.",
    "Öğrenci, gözlemini konu anlatımındaki bilgiyle karşılaştırıyor.",
    "Bir araştırma grubunun kararını bilimsel gerekçeyle sınaması gerekiyor.",
    "Günlük yaşam durumunun hangi bilimsel ilkeyle açıklandığı inceleniyor.",
)


def read_notes() -> dict[str, dict[str, Any]]:
    rows = [json.loads(line) for line in SOURCE.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    return {str(row.get("id")): row for row in rows if row.get("type") == "note"}


def rotate(values: list[Any], correct_position: int) -> list[Any]:
    correct, wrongs = values[0], values[1:]
    return [*wrongs[:correct_position], correct, *wrongs[correct_position:]]


def make_figure(qid: str, context: str, evidence: str, labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.alt"
    labels[h1] = "İnceleme bölümü"
    labels[h2] = "Kayıt"
    labels[alt] = "Bir durum ile bu duruma ait gözlem kanıtını iki satırda veren tablo; sonuç veya doğru cevap işareti içermez."
    return {
        "kind": "table",
        "headerKeys": [h1, h2],
        "rows": [[{"v": "Durum"}, {"v": context}], [{"v": "Gözlem"}, {"v": evidence}]],
        "altTextKey": alt,
    }


def make_question(number: int, entry: tuple[Any, ...], mode: str, level: int,
                  labels: dict[str, str], *, batch: int = 1,
                  local_number: int | None = None, knowledge_count: int | None = None) -> dict[str, Any]:
    note_id, fact, wrongs, context, evidence, explanation = entry
    notes = NOTE_BY_ID
    note = notes[note_id]
    objective = str((note.get("objectives") or [""])[0])
    local = local_number if local_number is not None else number
    entry_count = knowledge_count if knowledge_count is not None else len(KNOWLEDGE)
    qid = f"tr-g05-bank-fen-b{batch:02d}-q{local:03d}"
    correct_position = (number - 1) % 4
    claims = [fact, *wrongs]
    choices = rotate(claims, correct_position)
    reasons_by_claim = {
        fact: f"Doğru bilimsel ilişki: {explanation}",
        wrongs[0]: f"Kavram karışıklığı: Bu ifade ölçülen ya da gözlenen özelliği yanlış bir araç, yapı veya süreçle eşleştirir. {explanation}",
        wrongs[1]: f"Aşırı genelleme: Bu ifade kanıtın desteklemediği bir sonucu bütün durumlara yayar. {explanation}",
        wrongs[2]: f"Neden-sonuç yanılgısı: Bu ifade olayın yönünü veya oluşma nedenini ters kurar. {explanation}",
    }
    opener = OPENERS[(local - 1) % len(OPENERS)]
    if mode == "comprehension":
        stem = (
            f"{opener} Başlangıç durumu şöyledir: {context} "
            f"{note['title']} hakkında aşağıdaki ifadelerden hangisi bilimsel olarak doğrudur?"
        )
        figure = None
    elif mode == "application":
        application_variant = (local - 1) // entry_count
        if application_variant >= 2:
            stem = (
                f"Bir ekip şu durumu açıklayan bir uygulama kartı hazırlıyor: {context} "
                f"Kartta gözlem olarak “{evidence}” yazıyor. Durum, gözlem ve bilimsel bilgi birlikte "
                f"denetlendiğinde kartın sonuç bölümüne hangi ifade yazılmalıdır?"
            )
        elif application_variant == 1:
            stem = (
                f"{context} Araştırma kaydında ayrıca şu kanıt yer alıyor: {evidence} "
                f"Bu kanıtla sınırlı kalındığında öğrencinin uygulama kararını hangi sonuç destekler?"
            )
        else:
            stem = f"{context} {opener} Bu durumda hangi bilimsel değerlendirme kullanılmalıdır?"
        figure = None
    elif mode == "analysis":
        stem = (
            f"Aşağıdaki tabloda şu incelemenin ayrıntıları verilmiştir: {context} "
            f"{note['title']} konusundaki tablo kanıtını en doğru açıklayan sonuç hangisidir?"
        )
        figure = make_figure(qid, context, evidence, labels)
    else:
        mistaken = wrongs[(local - 1) % 3]
        stem = f"Bir öğrenci {note['title']} konusunda “{mistaken}” sonucuna ulaşıyor. Konu anlatımındaki bilimsel bilgiler kullanıldığında bu yanılgıyı düzelten ifade hangisidir?"
        figure = None
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "Durum ve gözlem yalnız tabloda verildiği için sonuç tablo kanıtına bağlıdır.",
        "acceptableKinds": ["table"], "evidenceDimensions": ["durum", "gözlem"],
    } if figure else {
        "level": "none", "role": "none",
        "rationale": "Sorunun çözümü için gerekli durum ve kavramlar metinde eksiksiz verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    row = {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": number,
        "subject": "Fen Bilimleri", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — {mode}",
        "objective": objective, "objectiveId": objective,
        "noteId": note_id, "noteKey": note_id,
        "question": stem, "choices": choices, "correct": correct_position,
        "correctIndex": correct_position, "correctOption": choices[correct_position],
        "distractorWhy": [reasons_by_claim[choice] for choice in choices],
        "explanation": f"{explanation} Verilen durumda doğru seçenek bu ilişkiyi korur.",
        "level": level,
        "difficultyReason": f"Düzey {level}; {note['title']} bilgisini {mode} biçiminde kullanıp dört bilimsel iddiayı gerekçeleriyle ayırmayı gerektirir.",
        "questionType": mode, "familyId": f"tr-g05-bank-fen-family-{number:03d}",
        "objectiveSource": note.get("objectiveSource"),
        "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [],
        "visualNeed": visual_need, "figure": figure,
        "hintsCount": 0, "hintsForbidden": True,
    }
    return row


def main() -> int:
    global NOTE_BY_ID
    NOTE_BY_ID = read_notes()
    missing = sorted({entry[0] for entry in KNOWLEDGE} - set(NOTE_BY_ID))
    if missing or len(KNOWLEDGE) != 28:
        raise RuntimeError(f"knowledge/note coverage error: missing={missing} count={len(KNOWLEDGE)}")
    labels: dict[str, str] = {}
    rows = [
        make_question(number, KNOWLEDGE[(number - 1) % len(KNOWLEDGE)], MODE_SEQUENCE[number - 1],
                      LEVEL_SEQUENCE[number - 1], labels)
        for number in range(1, 101)
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n",
                      encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
    print(json.dumps({"questions": len(rows), "labels": len(labels), "output": str(OUTPUT)}, ensure_ascii=False))
    return 0


NOTE_BY_ID: dict[str, dict[str, Any]] = {}


if __name__ == "__main__":
    raise SystemExit(main())
