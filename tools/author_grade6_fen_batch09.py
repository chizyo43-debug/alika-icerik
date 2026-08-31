#!/usr/bin/env python3
"""Append 100 independently authored Grade 6 science questions (batch 09)."""
from __future__ import annotations

from collections import Counter
import json

from author_grade6_bilisim_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade6_fen_batch07 import make_record, task
from author_grade6_mixed_batch03 import read_notes_only
from author_grade6_mixed_batch06 import FEN_SOURCE


def phase_tasks():
    n = "tr-g06-fen-bilimleri-note-025"
    return [
        task(n, "application", "Erime noktası 30°C, kaynama noktası 90°C olan saf madde 60°C'de hangi hâldedir?", "Sıvı",
             ["Katı", "Gaz", "Aynı anda yalnız katı ve gaz"], "60°C erime noktasının üstünde, kaynama noktasının altındadır."),
        task(n, "analysis", "Saf madde soğutulurken sıcaklık 42°C'de bir süre sabit kalıyor ve sıvı-katı birlikte görülüyor. Bu değer neyi gösterir?", "Donma noktasını",
             ["Kaynama noktasını", "Yoğunluğu", "Kütleyi"], "Soğuma sırasında sıvı ve katının birlikte bulunduğu sabit sıcaklık donma noktasıdır."),
        task(n, "comprehension", "Saf bir maddenin erime ve donma noktaları aynı basınçta nasıl ilişkilidir?", "Aynı sıcaklık değerindedir.",
             ["Erime noktası her zaman iki katıdır.", "Birbirleriyle ilgisizdir.", "Donma noktası her zaman 0°C'dir."], "Aynı madde ve basınçta katı-sıvı geçişinin iki yönü aynı sıcaklıkta gerçekleşir."),
        task(n, "error-analysis", "Bir öğrenci “Kaynama sırasında sıcaklık sabitse madde enerji almıyordur.” diyor. Hangi düzeltme doğrudur?",
             "Enerji alınır; bu enerji sıcaklığı artırmak yerine hâl değişiminde kullanılır.", ["Kaynama sırasında enerji bütünüyle yok olur.", "Sıcaklık sabitken tanecikler hareket etmez.", "Kaynama yalnız katılarda görülür."], "Hâl değişimi sırasında aktarılan enerji tanecikler arası etkileşimi değiştirmeye gider."),
        task(n, "application", "Bilinmeyen saf sıvının kaynama noktasını belirlerken hangi ölçüm planı uygundur?",
             "Basıncı sabit tutup güvenli ısıtma sırasında sıcaklığı düzenli aralıklarla kaydetmek", ["Termometre kullanmadan yalnız renge bakmak", "Basıncı sürekli değiştirip tek değer yazmak", "Sıvıya çıplak elle dokunmak"], "Kaynama noktası sıcaklık-zaman kaydı ve sabit basınç koşuluyla belirlenir; deney güvenli araçlarla yapılır."),
        task(n, "analysis", "A ve B saf maddeleri aynı basınçta sırasıyla 78°C ve 100°C'de kaynıyor. Hangi sonuç doğrudan desteklenir?",
             "Bu koşulda B'nin kaynama noktası A'dan yüksektir.", ["B kesinlikle A'dan daha yoğundur.", "A ve B aynı maddedir.", "Her basınçta bu değerler değişmeden kalır."], "Veri yalnız verilen basınçtaki kaynama noktalarını karşılaştırır; başka özellikleri kanıtlamaz."),
        task(n, "comprehension", "Bir sıvının kaynama noktasını belirleyen temel koşullar hangileridir?",
             "Madde türü ve ortam basıncı", ["Yalnız sıvının rengi", "Kabın üzerindeki etiket", "Sıvının bulunduğu odanın adı"], "Kaynama noktası madde türüne ve basınca bağlıdır; 100°C normal basınçta su için bilinen değerdir."),
        task(n, "comprehension", "Saf maddelerin erime ve kaynama noktalarının ayırt edici özellik olmasının anlamı nedir?",
             "Aynı basınçta maddeyi tanımaya yardımcı olan karakteristik değerler olmaları", ["Her madde için aynı değerde olmaları", "Madde miktarı arttıkça zorunlu değişmeleri", "Yalnız kabın rengine bağlı olmaları"], "Hâl değişim noktaları uygun koşullarda madde türüne özgü karşılaştırma bilgisi verir."),
    ]


def density_calculation_tasks():
    n = "tr-g06-fen-bilimleri-note-026"
    return [
        task(n, "application", "Kütlesi 96 g, hacmi 32 cm³ olan cismin yoğunluğu kaç g/cm³'tür?", "3 g/cm³", ["0,33 g/cm³", "64 g/cm³", "128 g/cm³"], "d=m/V=96/32=3 g/cm³."),
        task(n, "application", "Yoğunluğu 2 g/cm³, hacmi 45 cm³ olan örneğin kütlesi kaç gramdır?", "90 g", ["22,5 g", "43 g", "47 g"], "m=d×V=2×45=90 g."),
        task(n, "application", "Yoğunluğu 2,5 g/cm³ ve kütlesi 150 g olan cismin hacmi kaç cm³'tür?", "60 cm³", ["375 cm³", "147,5 cm³", "152,5 cm³"], "V=m/d=150/2,5=60 cm³."),
        task(n, "application", "Terazide 78 g ölçülen taş, dereceli kaptaki su düzeyini 20 mL'den 50 mL'ye çıkarıyor. Taşın yoğunluğu kaç g/cm³'tür?",
             "2,6 g/cm³", ["0,38 g/cm³", "1,56 g/cm³", "3,9 g/cm³"], "Taşın hacmi 50−20=30 cm³ olur; yoğunluk d=78/30=2,6 g/cm³'tür."),
        task(n, "comprehension", "Yoğunluğun g/cm³ birimi hangi oranı ifade eder?", "Bir santimetreküp hacimdeki gram cinsinden kütleyi",
             ["Bir gramdaki santimetreyi", "Toplam hacim ile zamanı", "Sıcaklık başına kuvveti"], "Yoğunluk birim hacim başına kütledir."),
        task(n, "analysis", "Aynı maddeden K örneği 40 g/20 cm³, L örneği 100 g/50 cm³ ölçülüyor. Hangi sonuç uygundur?",
             "İkisinin yoğunluğu da 2 g/cm³'tür.", ["K'nin yoğunluğu 20, L'nin 50 g/cm³'tür.", "L daha çok madde içerdiği için yoğunluğu zorunlu farklıdır.", "K ve L'nin oranları karşılaştırılamaz."], "Her iki kütle/hacim oranı 2'dir; aynı koşuldaki aynı madde için uyumludur."),
        task(n, "application", "Düzensiz taşın yoğunluğu ölçülecek. Hacim nasıl güvenli ve uygun biçimde bulunabilir?",
             "Taşın suya batırılmasıyla oluşan hacim artışını dereceli kapta ölçerek", ["Yalnız taşın rengini gözleyerek", "Taşı kırıp parçaların adını sayarak", "Kütleyi hacim kabul ederek"], "Tam batan ve suyla tepkime vermeyen düzensiz cismin hacmi yer değiştiren sıvı hacmiyle bulunabilir."),
        task(n, "application", "Bir raporda 120 g ve 40 cm³ verilerinden yoğunluk 3 bulunuyor. Sonuç bilimsel birimiyle nasıl yazılmalıdır?",
             "Sonuç 3 g/cm³ olarak yazılmalıdır.", ["Sonuç 3 cm olmalıdır.", "Birim 3 g olmalıdır.", "Yoğunlukta birim kullanılamaz."], "Kütle gram, hacim santimetreküp olduğunda oran birimi g/cm³'tür."),
    ]


def density_comparison_tasks():
    n = "tr-g06-fen-bilimleri-note-027"
    return [
        task(n, "comprehension", "Eşit hacimli K ve L sıvılarının kütleleri 36 g ve 52 g'dır. Hangisinin yoğunluğu büyüktür?", "L'nin",
             ["K'nin", "İkisi kesinlikle eşittir.", "Hacimler eşitken yoğunluk karşılaştırılamaz."], "Eşit hacimde daha büyük kütle daha büyük yoğunluk demektir."),
        task(n, "application", "K: 24 g/12 cm³, L: 45 g/15 cm³, M: 28 g/14 cm³. En yoğun madde hangisidir?", "L",
             ["K", "M", "Üçü eşit"], "Yoğunluklar K=2, L=3, M=2 g/cm³'tür."),
        task(n, "comprehension", "İki örneğin yalnız kütleleri biliniyorsa yoğunluklarını kesin karşılaştırmak neden mümkün değildir?",
             "Yoğunluk için kütlenin hacme oranı da bilinmelidir.", ["Yoğunluk yalnız örneğin adına bağlıdır.", "Kütle yoğunluk hesabında hiç kullanılmaz.", "Bütün maddelerin yoğunluğu aynıdır."], "Büyük örnek daha ağır olabilir; yoğunluk karşılaştırması m/V oranına dayanır."),
        task(n, "comprehension", "Yoğunlukları karşılaştırılan iki örnekte birimlerin aynı olması neden önemlidir?",
             "Oranların aynı ölçü temelinde anlamlı karşılaştırılmasını sağlar.", ["Birimler farklı olunca yoğunluk otomatik eşit olur.", "Birim yalnız renk belirtir.", "Dönüşüm yapmak sonucu her zaman sıfırlar."], "Kütle ve hacim birimleri uyumlu dönüştürülmeden sayısal oranlar doğrudan karşılaştırılamaz."),
    ]


def ice_water_tasks():
    n = "tr-g06-fen-bilimleri-note-028"
    return [
        task(n, "comprehension", "Buzun sıvı su üzerinde kalmasının temel nedeni hangisidir?", "Buzun yoğunluğunun sıvı sudan düşük olması",
             ["Buzun sudan daha yoğun olması", "Buzun kütlesinin her zaman sıfır olması", "Suyun buzu aşağı itmemesi"], "Su donarken yapısı daha fazla hacim kaplar; aynı kütlede yoğunluğu azalır."),
        task(n, "analysis", "Eşit kütlede buz 110 cm³, sıvı su 100 cm³ hacim kaplıyor. Hangi sonuç desteklenir?", "Buzun yoğunluğu sıvı sudan daha küçüktür.",
             ["Buz daha yoğundur.", "Hacim yoğunlukla ilişkisizdir.", "İkisinin yoğunluğu zorunlu eşittir."], "Eşit kütlede daha büyük hacim daha küçük m/V oranı demektir."),
        task(n, "application", "Bir göl modelinde kış koşulu gösterilecektir. Buz ve sıvı su nasıl yerleştirilmelidir?", "Buz üstte, sıvı su altta",
             ["Buz dipte, sıvı su üstte", "İkisi yalnız havada", "Buz bütün gölü alttan başlayarak doldurmuş"], "Daha az yoğun buz yüzer ve yüzey tabakası oluşturur."),
        task(n, "comprehension", "Yüzeydeki buz tabakasının alttaki suya etkisi hangisidir?", "Dış ortamla ısı alışverişini yavaşlatmaya yardımcı olması",
             ["Alttaki suyu anında kaynatması", "Isı kaybını zorunlu olarak hızlandırması", "Suyun yoğunluğunu sıfırlaması"], "Buz tabakası tam bir yalıtım olmasa da alttaki suyun hızlı soğumasını azaltabilir."),
        task(n, "comprehension", "Buzun göl yüzeyinde kalmasını sağlayan yoğunluk ilişkisi hangisidir?",
             "Buzun yoğunluğu sıvı suyun yoğunluğundan küçüktür.", ["Buzun yoğunluğu sonsuzdur.", "Buz sıvı sudan daha yoğundur.", "Buz ile suyun yoğunluğu her koşulda sıfırdır."], "Düşük yoğunluklu buz sıvı su üzerinde yüzer."),
        task(n, "analysis", "Bir gölette yüzey donmuş, dipte 4°C civarında sıvı su ölçülmüştür. Hangi çıkarım uygundur?", "Yüzeyden donma altta sıvı yaşam ortamının sürmesine katkı sağlamıştır.",
             ["Göl bütünüyle dipten donmuştur.", "Dipte su bulunması buzun battığını gösterir.", "Sıcaklık canlı yaşamıyla hiçbir zaman ilişkili değildir."], "Suyun yoğunluk davranışı ve yüzey buzunun ısı geçişini yavaşlatması dipte sıvı su kalmasını destekler."),
        task(n, "application", "Buz ve su yoğunluğunu karşılaştıran güvenli deneyde hangi ölçümler gerekir?", "Her örneğin kütlesi ve hacmi",
             ["Yalnız renkleri", "Yalnız kapların adı", "Sadece ortamın saati"], "Yoğunluk m/V olduğundan iki hâlin kütle ve hacim verileri aynı birimle ölçülmelidir."),
        task(n, "comprehension", "Yüzeydeki buz tabakasının alttaki suyun ısı kaybına etkisi nasıl açıklanır?",
             "Isı kaybını azaltabilir ancak tamamen durdurmaz.", ["Isı kaybını her zaman sonsuz artırır.", "Isı aktarımını yalnız yazın mümkün kılar.", "Buz ile su arasındaki enerji aktarımını kesinlikle sıfırlar."], "Yalıtım etkisi görecelidir; enerji aktarımı daha yavaş da olsa sürebilir."),
        task(n, "analysis", "Aynı hacimde buz ve su örnekleri tartıldığında su daha ağır geliyor. Hangi sonuç desteklenir?", "Sıvı suyun yoğunluğu buzunkinden büyüktür.",
             ["Buz daha yoğundur.", "Eşit hacim yoğunluk karşılaştırmasına izin vermez.", "Kütle farkı yalnız renk farkıdır."], "Eşit hacimde daha büyük kütle daha büyük yoğunluğu gösterir."),
        task(n, "application", "Bir animasyon, gölün kışın neden tamamen donmadığını açıklayacak. Hangi olay sırası kullanılmalıdır?",
             "Yüzey suyu soğur → yüzeyde buz oluşur → buz yüzer → alttaki ısı kaybı yavaşlar",
             ["Dip suyu donar → buz çöker → bütün göl anında donar", "Buz batar → yüzey kaynar → canlılar donar", "Su ısınır → yoğunluk yok olur → buz buharlaşır"], "Olay zinciri yoğunluk farkını, yüzey buzunu ve ısı aktarımını birlikte açıklar."),
        task(n, "comprehension", "Su donduğunda aynı kütle için hacmin artması yoğunluğu nasıl etkiler?", "Yoğunluğu azaltır.",
             ["Yoğunluğu artırır.", "Yoğunluğu her durumda değiştirmez.", "Kütleyi iki katına çıkarır."], "d=m/V bağıntısında kütle sabitken hacim artarsa yoğunluk azalır."),
        task(n, "analysis", "Kütlesi 90 g olan buz 100 cm³ hacim kaplıyor. Yoğunluğu kaç g/cm³'tür?", "0,9 g/cm³",
             ["1,1 g/cm³", "10 g/cm³", "190 g/cm³"], "d=90/100=0,9 g/cm³'tür; bu değer yaklaşık 1 g/cm³ sudan küçüktür."),
        task(n, "application", "Buzun yüzdüğünü gösteren tanecik modelinde hangi özellik vurgulanmalıdır?", "Katı yapıdaki taneciklerin aynı kütlede daha geniş hacme yayılması",
             ["Buzda hiç tanecik bulunmaması", "Buz taneciklerinin kütlesinin yok olması", "Sıvı su taneciklerinin tamamen hareketsiz olması"], "Model doğrudan fotoğraf değildir; düşük yoğunluğu daha açık yapı ile temsil eder."),
        task(n, "application", "Kapalı bir kaptaki su donarken kütlesi yaklaşık korunup hacmi artıyor. Bu değişim buzun yüzmesini nasıl açıklar?",
             "Hacim artışı yoğunluğu düşürür; buz sıvı su üzerinde kalır.", ["Donma bütün maddeyi yok eder.", "Kütle korununca yoğunluk zorunlu artar.", "Hacim yoğunluk hesabında kullanılmaz."], "Buzun yüzmesi kütle kazanımından değil, aynı kütlede daha büyük hacimden kaynaklanır."),
        task(n, "analysis", "Bir modelde buz parçası suyun yarısında asılı gösterilmiş, yüzeyde değil. Gözlem kaydı ise buzun yüzdüğünü söylüyor. Hangi değerlendirme uygundur?",
             "Model yoğunluk ilişkisini doğru temsil etmediği için güncellenmelidir.", ["Gözlem modelle çeliştiği için yok sayılmalıdır.", "Buzun konumu modelde önemsizdir.", "Model yalnız rengi değişince düzelir."], "Bilimsel model güvenilir gözlemle uyumlu olmalı ve buzun yüzeyde kalmasını göstermelidir."),
        task(n, "comprehension", "Buz tabakasının su canlıları için yararı hangi koşulla sınırlıdır?", "Altta sıvı su ve yaşam için uygun başka koşulların da bulunmasıyla",
             ["Buzun tek başına bütün canlıları kesin korumasıyla", "Suyun tamamen donmasıyla", "Oksijen ve besin koşullarının önemsiz olmasıyla"], "Buzun yalıtım etkisi önemlidir ancak yaşam yalnız tek faktöre bağlı değildir."),
        task(n, "application", "Bir göletin kış gözleminde hangi veri seti yoğunluk etkisini incelemeye en çok yardım eder?", "Derinliğe göre su sıcaklığı, buz konumu ve sıvı kalan tabaka kalınlığı",
             ["Yalnız göletin adı", "Sadece kıyıdaki ağaç sayısı", "Bir günün tek fotoğrafı"], "Konum, sıcaklık ve hâl verileri yüzeyden donma modelini sınamaya yarar."),
        task(n, "analysis", "Buz tabakası kalınlaşırken alttaki suyun hâlâ sıvı kaldığı ölçülüyor. Hangi sonuç kanıt sınırını korur?", "Buz tabakası bu gözlem döneminde alttaki suyun hızlı donmasını azaltmış olabilir.",
             ["Buz her koşulda bütün gölü sonsuza kadar sıvı tutar.", "Buz tabakası alttaki suyu ısıtmıştır.", "Tek gözlem dünyadaki bütün göller için kesin yasadır."], "Veri olası yalıtım etkisini destekler; süre, derinlik ve çevre koşulları da önemlidir."),
        task(n, "application", "Bir gölün yüzeyden donmasını açıklayan modele yoğunluk bilgisi nasıl eklenmelidir?",
             "Daha düşük yoğunluklu buzun yüzeyde kaldığı gösterilmelidir.", ["Yoğunluk yalnız gazlar için yazılmalıdır.", "Buzun dipte biriktiği gösterilmelidir.", "Sıvı ve katı hâller zorunlu eşit yoğunlukta çizilmelidir."], "Hâller arasındaki yoğunluk farkı buzun konumunu ve ısı alışverişi düzenini etkiler."),
        task(n, "application", "Buz ve su örnekleri için grafik çizilecek. Aynı kütlede yatay eksene hacim konursa hangi nokta daha sağda olmalıdır?", "Buz noktası",
             ["Su noktası", "İki nokta zorunlu üst üste", "Kütle bilinmeden ikisi de çizilemez"], "Aynı kütlede buz daha büyük hacim kaplar; bu yüzden hacim ekseninde daha sağdadır."),
        task(n, "comprehension", "Bir şişe ağzına kadar suyla doldurulup dondurulduğunda şişe şekil değiştiriyor. Bu gözlem hangi özellikle ilişkilidir?", "Suyun donarken hacminin artmasıyla",
             ["Suyun kütlesinin yok olmasıyla", "Buzun sıvı sudan daha yoğun olmasıyla", "Donmanın yalnız renk değiştirmesiyle"], "Donarken oluşan açık yapı hacim artışına ve kapta basınca yol açabilir."),
        task(n, "comprehension", "4°C civarındaki sıvı suyun göl tabanına yönelmesi hangi özellikle açıklanır?", "Sıvı suyun bu sıcaklık çevresinde yüksek yoğunluğa sahip olmasıyla",
             ["4°C'de suyun gaza dönüşmesiyle", "Buzun dipte erimesiyle", "Yoğunluğun sıcaklıktan hiç etkilenmemesiyle"], "Tatlı su yaklaşık 4°C'de en yüksek yoğunluğa ulaşır ve daha aşağıda bulunabilir."),
        task(n, "analysis", "Yüzey suyu 0°C'ye yaklaşırken dipte 4°C ölçülüyor. Hangi katmanlaşma yorumu uygundur?", "Daha yoğun 4°C su altta, daha soğuk su ve buz üstte bulunabilir.",
             ["En soğuk su her zaman en yoğundur.", "Buz mutlaka dipte bulunur.", "Sıcaklık ile yoğunluk arasında hiçbir ilişki yoktur."], "Suyun olağan dışı yoğunluk davranışı kış katmanlaşmasını açıklar."),
        task(n, "error-analysis", "Bir öğrenci “Su soğudukça her sıcaklıkta kesintisiz biçimde daha yoğun olur.” diyor. Hangi düzeltme doğrudur?",
             "Tatlı su yaklaşık 4°C'ye kadar yoğunlaşır; daha fazla soğuyup donarken yoğunluğu azalır.", ["Su sıcaklıktan hiç etkilenmez.", "Su 100°C'de en yoğundur.", "Buz sıvı sudan daha yoğundur."], "Suyun 4°C çevresindeki maksimum yoğunluğu basit doğrusal genellemeyi geçersiz kılar."),
        task(n, "application", "Bir eğitim posteri buzun canlılara etkisini gösterecek. Hangi başlık kanıta uygundur?", "Yüzen buz, alttaki sıvı yaşam alanının korunmasına katkı sağlar",
             ["Buz bütün canlıları tek başına kesin kurtarır", "Batan buz gölü dipten dondurur", "Yoğunluk canlı yaşamıyla ilişkisizdir"], "Başlık bilimsel mekanizmayı belirtir ancak sonucu mutlaklaştırmaz."),
        task(n, "analysis", "İki göle ait kayıtta sığ göl tamamen, derin göl yalnız yüzeyden donuyor. Hangi yorum uygundur?", "Yoğunluk mekanizmasına ek olarak derinlik ve çevre koşulları donma sonucunu etkileyebilir.",
             ["Yoğunluk bilgisi bütünüyle yanlıştır.", "Bütün göller aynı sürede donmalıdır.", "Derinlik ısı alışverişini hiçbir zaman etkilemez."], "Aynı temel mekanizma farklı derinlik ve hava koşullarında farklı sonuçlar verebilir."),
        task(n, "application", "Su altındaki sıcaklığı ölçmek için öğrenci buz yüzeyine çıkmadan nasıl güvenli veri toplayabilir?", "Yetişkin gözetiminde kıyıdan kullanılan uygun sensör ve güvenli ölçüm düzeniyle",
             ["İnce buz üzerinde tek başına yürüyerek", "Buzu çıplak elle kırıp suya girerek", "Ölçüm yapmadan değer uydurarak"], "Buzlu su ortamı risklidir; veri güvenli ekipman ve yetişkin gözetimiyle toplanır."),
        task(n, "comprehension", "Yoğunluk farkı olmasaydı ve buz suya batsaydı göl modeli için hangi öngörü yapılabilirdi?", "Buz dipte birikerek yüzeydeki yalıtıcı tabakanın oluşmasını zorlaştırabilirdi.",
             ["Yüzey yalıtımı kesinlikle artardı.", "Göl her zaman kaynardı.", "Buzun konumu hiçbir sonucu etkilemezdi."], "Karşıt model, yüzen buzun yüzey tabakası oluşturmasının önemini görünür kılar."),
        task(n, "analysis", "Bir deneyde buz eridikçe aynı su kütlesinin kapladığı hacim azalıyor. Hangi çıkarım desteklenir?", "Sıvı su bu koşulda buzdan daha yoğundur.",
             ["Erime kütleyi yok etmiştir.", "Buz daha küçük hacim kaplamıştır.", "Yoğunluk hacimle ilişkisizdir."], "Kütle korunurken hacmin azalması m/V oranının sıvı hâlde büyüdüğünü gösterir."),
        task(n, "error-analysis", "Bir öğrenci “Buzun üstte olması yalnız rüzgârın onu kaldırmasıyla açıklanır.” diyor. Hangi düzeltme uygundur?", "Rüzgâr olmasa da buzun suya göre düşük yoğunluğu yüzmesini sağlar.",
             ["Rüzgâr bütün maddelerin yoğunluğunu sıfırlar.", "Buz yalnız hava içinde yüzer.", "Sıvıların kaldırma etkisi yoktur."], "Yüzme temel olarak yoğunluk ve kaldırma ilişkisiyle açıklanır; rüzgâr zorunlu neden değildir."),
        task(n, "application", "Bir modelde su ve buz eşit hacimli kutularla gösterilecek. Yoğunluğu doğru temsil etmek için ne yapılmalıdır?", "Su kutusunda buz kutusuna göre daha büyük kütle gösterilmelidir.",
             ["Buz kutusunda daha küçük hacimde daha büyük kütle gösterilmelidir.", "İki kutunun kütle bilgisi gizlenmelidir.", "Yalnız kutu renkleri değiştirilmelidir."], "Eşit hacimde sıvı suyun kütlesi daha büyük olduğundan yoğunluğu daha yüksektir."),
    ]


def density_model_tasks():
    n = "tr-g06-fen-bilimleri-note-029"
    return [
        task(n, "application", "Eşit hacimli iki kutudan yoğunluğu büyük olanı tanecik modeliyle göstermek için hangi tasarım uygundur?", "Aynı hacimde daha fazla toplam kütle temsil eden tanecikler kullanmak",
             ["Yalnız kutunun rengini koyulaştırmak", "Daha az kütleyi daha büyük yoğunluk diye etiketlemek", "Hacimleri farklı yapıp karşılaştırma ölçütünü gizlemek"], "Yoğunluk modeli eşit hacimdeki kütle farkını görünür kılmalıdır."),
        task(n, "analysis", "Bir model K için 60 g/30 cm³, L için 90 g/30 cm³ değerlerini gösteriyor. Hangi madde daha yoğundur?", "L",
             ["K", "İkisi eşit", "Modelden hesaplanamaz"], "K=2, L=3 g/cm³ olduğundan L daha yoğundur."),
        task(n, "comprehension", "Bilimsel yoğunluk modelinin gerçek maddeyle ilişkisi nasıl açıklanmalıdır?", "Kütle-hacim ilişkisini temsil eden, sınırlılıkları belirtilmiş bir gösterimdir.",
             ["Maddenin taneciklerinin bire bir fotoğrafıdır.", "Yalnız süs amacı taşır.", "Modeldeki her tanecik gerçek boyuttadır."], "Model, görünmeyen ilişkiyi sadeleştirir; gerçek boyut ve sayı iddiası taşımaz."),
        task(n, "error-analysis", "Bir öğrenci “Daha çok tanecik çizilen kutunun hacmi de mutlaka daha büyüktür.” diyor. Hangi düzeltme doğrudur?", "Kutular eşit hacimliyse daha çok kütle daha büyük yoğunluğu temsil edebilir.",
             ["Tanecik sayısı hiçbir modeli etkilemez.", "Yoğunluk yalnız kutu alanıdır.", "Eşit hacimde kütle karşılaştırılamaz."], "Modelde dış hacim sabit tutulup içerik kütlesi değiştirilebilir."),
        task(n, "application", "Yeni ölçüm modeldeki yoğunluk değerinin yanlış olduğunu gösteriyor. Ne yapılmalıdır?", "Modelin kütle-hacim verileri ve gösterimi yeni kanıta göre güncellenmelidir.",
             ["Yeni ölçüm yok sayılmalıdır.", "Yalnız modelin adı değiştirilmelidir.", "Model değişmez gerçek kabul edilmelidir."], "Bilimsel model güvenilir veriye göre gözden geçirilip geliştirilebilir."),
        task(n, "analysis", "İki farklı büyüklükteki aynı madde örneğinin modellerinde m/V oranı eşit çıkıyor. Hangi çıkarım uygundur?", "Model, yoğunluğun örnek miktarından bağımsız madde özelliği olmasını destekler.",
             ["Büyük örneğin yoğunluğu zorunlu daha büyüktür.", "Kütle ve hacim oranı anlamsızdır.", "Örnekler kesinlikle farklı maddelerdir."], "Aynı koşulda aynı maddenin yoğunluk oranı örnek miktarı değişse de sabit kalabilir."),
    ]


def conductivity_tasks():
    n = "tr-g06-fen-bilimleri-note-030"
    return [
        task(n, "comprehension", "Basit devrede ampulün yanmasına izin veren maddeler nasıl sınıflandırılır?", "Elektrik iletkeni",
             ["Elektrik yalıtkanı", "Işık kaynağı", "Isı ölçer"], "Devre tamamlandığında akım geçiren madde iletkendir."),
        task(n, "application", "Bakır tel, plastik çubuk, grafit uç ve cam güvenli düşük gerilim devresinde sınanıyor. Ampulün bakır ve grafitte yanması neyi gösterir?", "Bakır ve grafitin bu düzende iletken davrandığını",
             ["Plastik ve camın güçlü iletken olduğunu", "Grafitin metal olmadığı için iletemeyeceğini", "Ampulün madde türünden bağımsız yandığını"], "Akımın geçmesi bakır ve grafitin iletkenliğini gösterir; grafit metal olmadan da iletebilir."),
        task(n, "analysis", "Aynı pil ve ampulde K maddesiyle ışık yanıyor, L ile yanmıyor. Hangi çıkarım kanıt sınırını korur?", "K bu düzende iletken, L yalıtkan davranmıştır.",
             ["K dünyadaki en iyi iletkendir.", "L her koşulda hiçbir elektrik etkisi göstermez.", "Pil ve bağlantılar kontrol edilmeden kesin madde yasası kurulabilir."], "Sonuç verilen düzenek ve bağlantıların doğruluğu koşuluyla sınıflandırma sağlar."),
        task(n, "error-analysis", "Bir öğrenci “Metal olmayan maddeler hiçbir zaman elektrik iletemez.” diyor. Hangi düzeltme doğrudur?", "Grafit gibi metal olmayan bazı maddeler elektrik iletebilir.",
             ["Bütün metaller yalıtkandır.", "Plastik her zaman iyi iletkendir.", "Madde cinsi ile iletkenlik ilişkisizdir."], "Metal olma ile iletkenlik güçlü ilişkili olsa da tek ve istisnasız ölçüt değildir."),
        task(n, "application", "Bir maddenin iletkenliğini sınıfta güvenli biçimde sınamak için hangi kaynak kullanılmalıdır?", "Düşük gerilimli pil ve uygun basit devre",
             ["Doğrudan şehir prizi", "Çıplak kablolu yüksek gerilim", "Islak elle priz bağlantısı"], "Öğrenci deneyinde güvenli düşük gerilim kullanılır; ev priziyle deney yapılmaz."),
        task(n, "analysis", "Test maddesi iletken olduğu hâlde ampul yanmıyor. Hangi kontrol önce yapılmalıdır?", "Pilin, ampulün ve bağlantıların kapalı devre oluşturup oluşturmadığı",
             ["Maddenin rengi", "Masanın yüksekliği", "Öğrencinin adı"], "Negatif sonuç maddeye bağlanmadan önce devrenin diğer bileşenleri doğrulanır."),
        task(n, "comprehension", "Elektrik kablosunda metal çekirdek ile plastik kaplamanın görevleri hangi seçenekte doğrudur?", "Metal iletir, plastik kullanıcıyı akımdan yalıtmaya yardımcı olur.",
             ["Plastik iletir, metal yalıtır.", "İkisi de yalnız süstür.", "Metal akımı tamamen durdurur."], "Kablo tasarımı iletken çekirdek ve yalıtkan dış kaplamayı birlikte kullanır."),
        task(n, "error-analysis", "Bir öğrenci “Ampul yanmadıysa test maddesi kesinlikle yalıtkandır; devreyi kontrol etmeye gerek yoktur.” diyor. Hangi düzeltme gerekir?", "Bağlantı, pil ve ampul doğrulanmadan yalnız madde hakkında kesin sonuç kurulamaz.",
             ["Ampul yanmaması maddenin kesin süper iletken olduğunu gösterir.", "Devre bileşenleri sonucu etkilemez.", "Tekrar ölçümü bilimsel değildir."], "Deneyde ölçüm sisteminin çalışması ve tek değişken koşulu önce kontrol edilir."),
    ]


def resistance_tasks():
    n = "tr-g06-fen-bilimleri-note-031"
    return [
        task(n, "analysis", "Aynı maddeden eş kalınlıkta 20 cm ve 40 cm teller aynı devrede sınanıyor. Uzun telde ampul daha sönük. Hangi sonuç uygundur?", "Tel uzadıkça direnç artmış olabilir.",
             ["Tel uzadıkça direnç kesinlikle azalmıştır.", "Uzunluk parlaklığı hiçbir zaman etkilemez.", "Kısa telin maddesi kendiliğinden değişmiştir."], "Madde ve kesit sabitken daha uzun iletken yol daha büyük dirençle uyumludur."),
        task(n, "application", "Tel kalınlığının ampul parlaklığına etkisi araştırılacak. Hangi değişkenler sabit tutulmalıdır?", "Tel cinsi, tel uzunluğu, pil ve ampul",
             ["Kalınlıkla birlikte tel cinsi de değiştirilmelidir.", "Bütün devreler farklı pillerle kurulmalıdır.", "Uzunluk her ölçümde rastgele seçilmelidir."], "Yalnız kesit alanı değişirse etkisi ayrıştırılabilir."),
        task(n, "error-analysis", "Bir öğrenci “Aynı cins tel uzadıkça direnç azalır ve ampul daha parlak yanar.” diyor. Hangi düzeltme doğrudur?", "Aynı kesitte tel uzadıkça direnç artar ve parlaklık azalabilir.",
             ["Uzunluk direnci hiçbir zaman etkilemez.", "Uzun tel akımı sınırsız artırır.", "Ampul parlaklığı devre akımıyla ilişkisizdir."], "Daha uzun iletken yol yüklerin hareketine daha fazla karşı koyar."),
    ]


def rheostat_tasks():
    n = "tr-g06-fen-bilimleri-note-032"
    return [
        task(n, "comprehension", "Reostanın basit devredeki temel işlevi hangisidir?", "Devreye giren direnç teli uzunluğunu değiştirerek akımı ayarlamak",
             ["Pilin kimyasal türünü değiştirmek", "Ampulü ışık kaynağı olmaktan çıkarmak", "Devredeki bütün direnci sıfırlamak"], "Reosta ayarlanabilir dirençtir ve akım/parlaklık kontrolünde kullanılır."),
        task(n, "analysis", "Reostada devreye katılan tel yolu uzatıldığında ampermetre değeri azalıyor. Hangi çıkarım uygundur?", "Etkin direnç artmıştır.",
             ["Etkin direnç azalmıştır.", "Akım ile direnç ilişkisizdir.", "Pil gerilimi zorunlu iki kat olmuştur."], "Diğer koşullar sabitken daha uzun direnç yolu akımı azaltır."),
        task(n, "application", "Ampulü daha sönük yapmak isteyen öğrenci reostayı nasıl ayarlamalıdır?", "Devreye giren etkin direnç teli uzunluğunu artırmalıdır.",
             ["Etkin direnci sıfıra yaklaştırmalıdır.", "Reostayı devreden çıkarıp kabloyla kısa devre yapmalıdır.", "Pili ters çevirmenin parlaklığı kesin artıracağını varsaymalıdır."], "Seri devrede direnç artışı akımı ve parlaklığı azaltabilir."),
        task(n, "error-analysis", "Bir öğrenci “Sürgü sağa giderse ampul her devrede kesin parlaklaşır.” diyor. Hangi düzeltme doğrudur?", "Sonuç, reostanın hangi uçlarının bağlı olduğuna ve etkin tel yolunun nasıl değiştiğine bağlıdır.",
             ["Sürgü konumu hiçbir devreyi etkilemez.", "Sağ yön elektriksel birimdir.", "Reostada bağlantı uçları gösterilmemelidir."], "Fiziksel yön tek başına yeterli değildir; akım yolu izlenmelidir."),
        task(n, "application", "Reosta etkisini adil karşılaştırmak için hangi bileşenler aynı tutulmalıdır?", "Pil, ampul, bağlantı biçimi ve ölçüm aracı",
             ["Her denemede farklı pil ve ampul", "Reostayla birlikte bütün telleri değiştirmek", "Akımı ölçmeden yalnız tahmin yazmak"], "Yalnız reosta ayarı değişirse parlaklık ve akım farkı onunla ilişkilendirilebilir."),
        task(n, "analysis", "Etkin direnç 4 Ω'dan 9 Ω'a çıkarılırken aynı devrede ampul parlaklığı azalıyor. Hangi ilişki desteklenir?", "Direnç arttıkça akım ve parlaklık azalmıştır.",
             ["Direnç arttıkça akım artmıştır.", "Parlaklık yalnız ampul rengine bağlıdır.", "Direnç değişimi ölçüme yansımamıştır."], "Aynı kaynakta daha büyük toplam direnç daha küçük akımla uyumludur."),
        task(n, "comprehension", "Reostanın sürgüsü neyi fiziksel olarak değiştirir?", "Devreye katılan direnç telinin etkin uzunluğunu",
             ["Elektronların kütlesini", "Pilin içindeki madde türünü", "Ampulün cam rengini"], "Sürgü bağlantı noktasını değiştirerek akımın geçtiği direnç teli bölümünü ayarlar."),
        task(n, "error-analysis", "Bir öğrenci “Reosta yalnız devreyi açıp kapatan anahtardır.” diyor. Hangi düzeltme uygundur?", "Reosta akımı kademeli ayarlayan değişken dirençtir; anahtarla aynı görevde değildir.",
             ["Reosta yalnız pil üretir.", "Anahtar direnci sürekli ayarlar.", "İki eleman devreyi hiçbir biçimde etkilemez."], "Anahtar devreyi açıp kapatırken reosta etkin direnci değiştirir."),
    ]


def biodiversity_tasks():
    n = "tr-g06-fen-bilimleri-note-033"
    return [
        task(n, "comprehension", "Bir bölgenin biyoçeşitliliği araştırılırken hangi canlı grupları birlikte dikkate alınmalıdır?",
             "Bitkiler, hayvanlar ve bölgede yaşayan diğer canlı grupları",
             ["Yalnız göze çarpan büyük hayvanlar", "Sadece insanlar tarafından yetiştirilen bitkiler", "Yalnız aynı türün farklı yaştaki bireyleri"],
             "Biyoçeşitlilik değerlendirmesi tek bir canlı grubuna değil, bölgedeki farklı canlı türlerine dayanır."),
        task(n, "application", "Bir okul bahçesinin biyoçeşitliliğini mevsim boyunca araştırmak isteyen ekip için en uygun plan hangisidir?",
             "Aynı alanları belirli aralıklarla gözleyip farklı canlı gruplarını ortak kayıt ölçütleriyle saymak",
             ["Bir kez yalnız öğle saatinde tek ağacı gözlemek", "Her gözlemde alan ve sayım yöntemini değiştirmek", "Canlıları saymadan yalnız bahçenin güzel olduğunu yazmak"],
             "Düzenli zaman aralıkları ve değişmeyen ölçütler gözlemlerin karşılaştırılmasını sağlar."),
        task(n, "analysis", "K alanında 12 bitki, 7 kuş ve 9 böcek türü; L alanında 4 bitki, 3 kuş ve 2 böcek türü kaydediliyor. Hangi yorum veriye uygundur?",
             "İncelenen gruplar ve dönemde K alanında daha fazla tür çeşitliliği gözlenmiştir.",
             ["L alanında kesinlikle hiç biyoçeşitlilik yoktur.", "K alanındaki her türün birey sayısı daha fazladır.", "Bu sayımlar iki alanın bütün gelecek yıllarını kanıtlar."],
             "Veriler K'de daha çok tür kaydı gösterir; birey sayısı ve bütün zamanlar hakkında kesinlik sağlamaz."),
        task(n, "error-analysis", "Bir öğrenci “Bahçede çok sayıda serçe gördüm; o hâlde biyoçeşitlilik kesinlikle yüksektir.” diyor. Hangi düzeltme doğrudur?",
             "Tek türün birey sayısı yeterli değildir; farklı türler ve canlı grupları araştırılmalıdır.",
             ["Bir türün çok bireyi her zaman çok tür anlamına gelir.", "Biyoçeşitlilik için hiçbir gözlem gerekmez.", "Yalnız serçelerin rengi sayılmalıdır."],
             "Birey bolluğu ile tür çeşitliliği aynı ölçüt değildir."),
        task(n, "application", "İki sulak alanın biyoçeşitliliği karşılaştırılacak. Adil karşılaştırma için hangi koşul önemlidir?",
             "Benzer mevsim, alan büyüklüğü, süre ve gözlem yöntemini kullanmak",
             ["Bir alanı bir saat, diğerini yalnız bir dakika gözlemek", "Birinde bütün canlıları, diğerinde yalnız kuşları saymak", "Alanların adlarına göre sonuç vermek"],
             "Ortak ölçütler kullanılmadan kayıt farkının yöntemden mi alandan mı kaynaklandığı ayırt edilemez."),
        task(n, "analysis", "Bir çayırlıkta çiçek türleri azaldıktan sonra gözlenen tozlayıcı böcek türleri de azalıyor. Hangi çıkarım kanıt sınırını korur?",
             "Kayıtlar çiçek ve tozlayıcı çeşitliliğinin birlikte değişmiş olabileceğini gösterir; neden için ek araştırma gerekir.",
             ["Her çiçek türü azalması dünyadaki bütün böcekleri yok eder.", "İki kaydın değişmesi aralarında hiçbir ilişki olamayacağını kanıtlar.", "Böcek azalmasının tek nedeni kesinlikle hava sıcaklığıdır."],
             "Birlikte değişim ilişki olasılığını destekler ancak tek başına kesin neden belirlemez."),
        task(n, "comprehension", "Biyoçeşitliliğin doğal yaşam açısından önemli olmasının temel gerekçesi hangisidir?",
             "Canlıların beslenme, barınma ve diğer ekolojik ilişkilerle birbirine bağlı olması",
             ["Her canlının çevreden tamamen bağımsız yaşaması", "Yalnız insanların sevdiği türlerin görev taşıması", "Tür çeşitliliğinin canlı ilişkilerini hiç etkilememesi"],
             "Doğal yaşamda canlılar farklı roller ve ilişkilerle aynı sistemin parçalarıdır."),
        task(n, "error-analysis", "Bir öğrenci “Biyoçeşitlilik yalnız bir yerin güzel görünmesiyle ilgilidir.” diyor. Hangi düzeltme uygundur?",
             "Biyoçeşitlilik canlılar arası ilişkiler ve doğal yaşamın işleyişiyle de ilgilidir.",
             ["Biyoçeşitlilik yalnız boya renklerinin sayısıdır.", "Canlı türleri doğal yaşamda hiçbir görev üstlenmez.", "Bir alanın görünüşü bütün bilimsel ölçümlerin yerini alır."],
             "Estetik değer olabilir; ancak bilimsel önem canlı çeşitliliğini ve ekolojik ilişkileri de kapsar."),
        task(n, "application", "Bir göletteki biyoçeşitliliği izlemek için hangi kayıt kanıt bakımından en kullanışlıdır?",
             "Tarih, konum, gözlem süresi ve güvenilir tür tanımlarıyla yinelenen kayıtlar",
             ["Tarihsiz tek bir bulanık fotoğraf", "Tür adı vermeyen 'çok canlı vardı' cümlesi", "Gözlem yapılmadan hazırlanan tahmin listesi"],
             "İzlenebilir ve yinelenebilir kayıtlar farklı dönemlerin karşılaştırılmasına yardım eder."),
        task(n, "analysis", "Aynı korulukta ilk sayımda 18, ikinci sayımda 11 tür görülüyor. İkinci sayım yalnız beş dakika sürmüş, ilk sayım bir saat sürmüş. Hangi değerlendirme doğrudur?",
             "Süreler eşit olmadığı için tür sayısındaki fark doğrudan biyoçeşitlilik azalması diye yorumlanamaz.",
             ["Yedi türün kesin yok olduğu kanıtlanmıştır.", "Gözlem süresi tür kaydını hiçbir zaman etkilemez.", "Kısa sayım daha çok tür bulmayı zorunlu kılar."],
             "Örnekleme çabası farklı olduğunda gözlenen tür sayıları adil karşılaştırma oluşturmaz."),
        task(n, "comprehension", "Bir araştırmada gözlem ile yorum arasındaki fark hangisidir?",
             "Gözlem kaydedilen veridir; yorum bu veriye dayanarak kurulan açıklamadır.",
             ["Gözlem kanıtsız tahmin, yorum ölçüm aracıdır.", "İkisi her durumda aynı cümledir.", "Yorum yalnız canlıların adını saymaktır."],
             "Bilimsel değerlendirmede veri ile veriden çıkarılan sonuç ayrı tutulur."),
        task(n, "error-analysis", "Bir öğrenci “Tek bir kuş görmediğim için bu ormanda kuş türü yoktur.” diyor. Hangi düzeltme gerekir?",
             "Tek zamanlı gözlem yokluğu kanıtlamaz; farklı zaman ve noktalarda yinelenen gözlemler yapılmalıdır.",
             ["Bir canlı görülmediyse tür dünyadan yok olmuştur.", "Kuşları araştırmak için yalnız bitki saymak yeterlidir.", "Tek gözlem bütün mevsimleri temsil eder."],
             "Canlıların görülmesi saat, mevsim, hava ve örnekleme yönteminden etkilenebilir."),
    ]


def threat_tasks():
    n = "tr-g06-fen-bilimleri-note-034"
    return [
        task(n, "analysis", "Bir bölgede dört yılda kaydedilen tür sayıları 42, 38, 33 ve 27'dir. Eğilim sürerse hangi tahmin uygundur?",
             "Tür sayısı sonraki dönemde de azalabilir; bu kesin sonuç değil veriye dayalı tahmindir.",
             ["Sonraki yıl tür sayısı kesinlikle sıfır olacaktır.", "Sayılar düzenli olarak artmaktadır.", "Geçmiş veriler hiçbir tahmine katkı sağlamaz."],
             "Düzenli azalma geleceğe ilişkin dikkatli bir azalma öngörüsünü destekler."),
        task(n, "application", "Yeni yol yapımından önce ve sonra bir yaşam alanındaki tür değişimini araştırmak için hangi plan daha güçlüdür?",
             "Aynı yöntemle yol çevresini ve benzer bir kontrol alanını birden çok dönemde izlemek",
             ["Yalnız yol sonrası tek fotoğrafa bakmak", "Önce kuşları sonra yalnız bitkileri saymak", "Kontrol alanında hiç kayıt tutmamak"],
             "Önce-sonra ve kontrol alanı kayıtları zaman ile alan farklarını ayırmaya yardım eder."),
        task(n, "error-analysis", "Bir öğrenci “Bir gün tür sayısı düşük çıktı; alanın biyoçeşitliliği kesin olarak yok oluyor.” diyor. Hangi düzeltme doğrudur?",
             "Tek günlük kayıt yeterli değildir; aynı yöntemle farklı zamanlarda toplanan veriler incelenmelidir.",
             ["Tek sayı her zaman uzun dönem eğilimidir.", "Tür sayımı yerine yalnız hava tahmini kullanılmalıdır.", "Yeni veriler ilk yorumu hiçbir zaman değiştiremez."],
             "Eğilim belirlemek için karşılaştırılabilir ve tekrarlı gözlemler gerekir."),
        task(n, "application", "Akarsudaki kirlilik ile canlı çeşitliliği ilişkisi araştırılıyor. Hangi veri çifti en yararlıdır?",
             "Aynı tarihlerde ölçülen su kalitesi değerleri ile kaydedilen tür sayıları",
             ["Yalnız kıyıdaki taşların rengi", "Bir köyün nüfusu ile başka ülkenin kuş sayısı", "Tarihsiz tek tür listesi"],
             "Eş zamanlı çevre ve canlı verileri değişimlerin birlikte incelenmesini sağlar."),
        task(n, "analysis", "Bir sulak alanda su seviyesi düştükçe gözlenen su kuşu türleri azalıyor. Hangi yorum bilimsel olarak daha uygundur?",
             "Su seviyesi değişimi olası bir tehdit etkenidir; diğer koşullar da incelenmelidir.",
             ["Bütün kuş azalmasının tek nedeni kesinlikle su seviyesidir.", "Birlikte değişen veriler hiçbir araştırma sorusu oluşturamaz.", "Su kuşları yaşam alanından etkilenmez."],
             "Veri olası ilişkiyi gösterir; kesin neden için besin, kirlilik ve gözlem koşulları gibi etkenler de sınanır."),
        task(n, "comprehension", "Veriye dayalı tahmin ile kesin sonuç arasındaki fark hangisidir?",
             "Tahmin mevcut eğilime dayanır ve yeni verilerle değişebilir.",
             ["Tahmin geleceği değişmez biçimde kanıtlar.", "Kesin sonuç hiçbir kanıt gerektirmez.", "Tahminde veriye bakmak yasaktır."],
             "Bilimsel tahmin belirsizlik taşır ve yeni kanıta göre güncellenir."),
        task(n, "analysis", "Bir adada yabancı bir türün yayılışı 5, 18, 41 birey olarak artarken yerli bir tür 60, 47, 29 bireye düşüyor. Hangi sonuç desteklenir?",
             "İki değişimin ilişkili olabileceği araştırılmalıdır; tablo tek başına kesin neden kanıtlamaz.",
             ["Yabancı türün artışı yerli türü kesinlikle hiçbir biçimde etkilemez.", "İki türün birey sayısı da artmıştır.", "Üç dönemlik kayıt bütün adalar için değişmez yasa kurar."],
             "Karşıt eğilim olası etkileşimi düşündürür fakat neden-sonuç için ek kanıt gerekir."),
        task(n, "application", "Bir ormandaki tür azalmasına ilişkin tahminin güvenilirliğini artırmak için ne yapılmalıdır?",
             "Uzun süreli kayıtlar, habitat değişimi ve insan etkisi verileri birlikte incelenmelidir.",
             ["Yalnız tek bir söylenti yazılmalıdır.", "Azalmayla çelişen bütün ölçümler silinmelidir.", "Her yıl farklı ölçütle sayım yapılmalıdır."],
             "Birden fazla karşılaştırılabilir kanıt, eğilim ve olası nedenlerin değerlendirilmesini güçlendirir."),
        task(n, "error-analysis", "Bir öğrenci “Grafikte iki değer birlikte azalıyorsa birinin diğerine kesin neden olduğu kanıtlanır.” diyor. Hangi düzeltme uygundur?",
             "Birlikte değişim ilişki gösterebilir; neden-sonuç için kontrollü veya ek kanıt gerekir.",
             ["Grafikler hiçbir ilişki gösteremez.", "Azalan değerler her zaman ölçüm hatasıdır.", "Neden araştırılırken başka değişkenlere bakılmaz."],
             "Korelasyon tek başına nedensellik kanıtı değildir."),
        task(n, "application", "Tarım alanında tozlayıcı türlerinin azaldığı görülüyor. Hangi koruma kararı veriye en uygun biçimde eşlik eder?",
             "Pestisit kullanımı ve çiçekli habitat verilerini izleyip etkisi ölçülebilen önlemler denemek",
             ["Nedeni araştırmadan bütün canlıları alandan uzaklaştırmak", "Tür kayıtlarını durdurmak", "Tek çözümün kesin olduğunu ilan edip sonuç ölçmemek"],
             "Önlem, olası tehdit verileriyle ilişkilendirilmeli ve sonrasında etkisi yeniden ölçülmelidir."),
        task(n, "error-analysis", "Bir öğrenci “Geçen yılki tahmin değiştiyse bilimsel çalışma başarısızdır.” diyor. Hangi düzeltme doğrudur?",
             "Yeni veriler geldiğinde tahmini güncellemek bilimsel sürecin doğal bir parçasıdır.",
             ["Bilimsel tahminler yeni kanıttan etkilenmemelidir.", "İlk tahmin her koşulda kesin gerçektir.", "Yeni ölçümler eski verilerin tamamını yok eder."],
             "Tahminler eldeki kanıta bağlıdır ve daha iyi kanıtla yeniden değerlendirilir."),
    ]


def fuel_task():
    n = "tr-g06-fen-bilimleri-note-035"
    return [
        task(n, "application", "Yakıtla çalışan sobanın bulunduğu odada karbonmonoksit alarmı çalıyor ve bir kişi baş ağrısı hissediyor. En güvenli ilk davranış hangisidir?",
             "Herkesi temiz havaya çıkarıp acil yardım istemek ve yetkili kontrolü olmadan içeri dönmemek",
             ["Alarmı susturup uyumaya devam etmek", "Koku yoksa sobaya daha çok yakıt eklemek", "Kaynağı bulmak için odada tek başına uzun süre beklemek"],
             "Karbonmonoksit renksiz ve kokusuz olabilir; belirtilerde ortamdan uzaklaşmak ve acil yardım almak gerekir."),
    ]


TASK_BUILDERS = [
    phase_tasks, density_calculation_tasks, density_comparison_tasks,
    ice_water_tasks, density_model_tasks, conductivity_tasks,
    resistance_tasks, rheostat_tasks, biodiversity_tasks, threat_tasks,
    fuel_task,
]


def main() -> int:
    existing = [json.loads(x) for x in OUTPUT.read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(existing) != 800:
        raise RuntimeError("validated first eight batches must exist before batch 09")
    notes = read_notes_only(FEN_SOURCE)
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    tasks = [item for builder in TASK_BUILDERS for item in builder()]
    if len(tasks) != 100:
        raise AssertionError(f"batch 09 must contain 100 tasks, got {len(tasks)}")
    expected_modes = {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
    if Counter(item["mode"] for item in tasks) != expected_modes:
        raise AssertionError(Counter(item["mode"] for item in tasks))
    rows = [
        make_record(local, item, notes[item["note"]], labels, batch=9, number_base=800)
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
    print("appended grade 6 science batch 09: 100 questions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
