#!/usr/bin/env python3
"""Author 100 computed Grade 5 mathematics questions (grade rows 901-1000)."""
from __future__ import annotations

from fractions import Fraction
import json
from typing import Any

import author_grade5_math_segment01 as base


def number_with_copula(value: int) -> str:
    """Write an integer with the Turkish copular suffix used after digits."""
    absolute = abs(value)
    ones_suffix = {0: "dır", 1: "dir", 2: "dir", 3: "tür", 4: "tür",
                   5: "tir", 6: "dır", 7: "dir", 8: "dir", 9: "dur"}
    tens_suffix = {1: "dur", 2: "dir", 3: "dur", 4: "tır", 5: "dir",
                   6: "tır", 7: "tir", 8: "dir", 9: "dır"}
    if absolute % 10:
        suffix = ones_suffix[absolute % 10]
    elif (absolute // 10) % 10:
        suffix = tens_suffix[(absolute // 10) % 10]
    elif (absolute // 100) % 10:
        suffix = "dür"  # yüz
    elif absolute % 1_000_000:
        suffix = "dir"  # bin
    else:
        suffix = "dur"  # milyon
    return f"{value}'{suffix}"


MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
LEVELS = (
    [1] * 15 + [2] * 10 +
    [1] * 5 + [2] * 15 + [3] * 15 +
    [3] * 10 + [4] * 10 + [5] * 5 +
    [3] * 5 + [4] * 10
)
NOTE_IDS = [
    "tr.g05.mat.5.1.1.note.01", "tr.g05.mat.5.1.1.note.02", "tr.g05.mat.5.1.1.note.03",
    "tr.g05.mat.5.1.2.note.01", "tr.g05.mat.5.1.2.note.02", "tr.g05.mat.5.1.3.note.01",
    "tr.g05.mat.5.1.4.note.01", "tr.g05.mat.5.1.4.note.02", "tr.g05.mat.5.1.4.note.03",
    "tr.g05.mat.5.2.note.01", "tr.g05.mat.5.2.note.02", "tr.g05.mat.5.2.note.03",
    "tr.g05.mat.5.2.note.04", "tr.g05.mat.5.3.note.01", "tr.g05.mat.5.3.note.02",
    "tr.g05.mat.5.3.note.03", "tr.g05.mat.5.3.note.04", "tr.g05.mat.5.3.note.05",
    "tr.g05.mat.5.4.note.01", "tr.g05.mat.5.4.note.02", "tr.g05.mat.5.4.note.03",
    "tr.g05.mat.5.5.note.01", "tr.g05.mat.5.6.note.01",
]
CONTEXTS = [
    "matematik günlüğü", "akran çözüm kartı", "ölçme istasyonu", "sınıf proje dosyası",
    "çözüm karşılaştırma panosu", "kavram denetim çizelgesi", "uygulama atölyesi",
]


def fmt_int(value: int) -> str:
    return f"{value:,}".replace(",", " ")


def case_data(index: int, variant: int) -> tuple[str, str, list[str], str]:
    v = variant % 5
    if index == 0:
        number, digit, place, value = [
            (708_040_315, 8, "milyonlar", 8_000_000), (420_706_081, 7, "yüz binler", 700_000),
            (905_032_640, 3, "on binler", 30_000), (160_408_027, 4, "yüz binler", 400_000),
            (804_090_152, 9, "on binler", 90_000),
        ][v]
        statement = f"{fmt_int(number)} sayısındaki {digit} rakamının basamak adı ve değeri aranıyor."
        correct = f"Basamak çözümlemesi: {place} basamağı ve {fmt_int(value)}"
        wrongs = [f"Rakam değeriyle karıştırma: {place} basamağı ve {digit}", f"Komşu basamağa kaydırma: binler basamağı ve {fmt_int(value // 10)}", "Sıfırlı bölüğü yok sayma: rakamın basamak değeri olmadığı sonucu"]
        explanation = f"Sayı sağdan üçerli bölüklere ayrıldığında {digit}, {place} basamağında bulunur ve {fmt_int(value)} değerini taşır."
    elif index == 1:
        number, reading = [
            (63_005_208, "altmış üç milyon beş bin iki yüz sekiz"),
            (407_090_014, "dört yüz yedi milyon doksan bin on dört"),
            (81_300_006, "seksen bir milyon üç yüz bin altı"),
            (506_004_070, "beş yüz altı milyon dört bin yetmiş"),
            (92_040_301, "doksan iki milyon kırk bin üç yüz bir"),
        ][v]
        statement = f"{fmt_int(number)} sayısının bölükleri korunarak okunması isteniyor."
        correct = f"Bölükleri doğru okuma: {reading}"
        wrongs = ["Sıfırları basamak gibi okuma: sıfır yüzlü ve sıfır onlu bir ifade", "Binler ile birleri yer değiştirme: son bölüğü binler diye okuyan ifade", "Milyonlar bölüğünü yüz binlere kaydırma: ilk bölüğü eksik okuyan ifade"]
        explanation = f"Üçlü bölükler soldan sağa milyonlar, binler ve birler diye okunur; doğru okunuş {reading} biçimindedir."
    elif index == 2:
        words, number = [
            ("yedi yüz iki milyon on beş bin kırk", 702_015_040),
            ("doksan milyon üç yüz sekiz bin altı", 90_308_006),
            ("beş yüz on milyon yedi bin iki yüz", 510_007_200),
            ("iki yüz dört milyon altmış bin dokuz", 204_060_009),
            ("sekiz yüz milyon dokuz yüz bin yetmiş üç", 800_900_073),
        ][v]
        statement = f"'{words}' okunuşu rakamlarla yazılacaktır."
        correct = f"Üç basamaklı bölükleri koruma: {fmt_int(number)}"
        wrongs = [f"Eksik basamağı kapatmama: {str(number).replace('0', '', 1)}", "Binler bölüğünü birler bölüğüne taşıma: bölük sırası değişmiş sayı", "Okunmayan sıfırları sona ekleme: basamak sayısı değişmiş sayı"]
        explanation = f"Her bölük üç basamakla yazılıp eksik yerler sıfırla doldurulduğunda {fmt_int(number)} elde edilir."
    elif index == 3:
        groups, each, used, noun = [(14, 36, 128, "rozet"), (18, 27, 95, "kitap"), (22, 24, 173, "fidan"), (16, 45, 218, "bilet"), (25, 32, 187, "kalem")][v]
        total, result = groups * each, groups * each - used
        statement = f"Her birinde {each} {noun} bulunan {groups} grup hazırlanıyor; {used} {noun} kullanılıyor. Kalan miktar soruluyor."
        correct = f"Önce toplamı kurup eksiltme: {groups} × {each} - {used} = {result} {noun}"
        wrongs = [f"Bütün verileri toplama: {groups} + {each} + {used} işlemi", f"Gruplamayı atlayıp çıkarma: {each} - {used} işlemi", f"Kullanılanı grup sayısıyla çarpma: {used} × {groups} işlemi"]
        explanation = f"Eş grupların toplamı {groups} × {each} = {total}, kalan ise {total} - {used} = {result} {noun} olur."
    elif index == 4:
        a, b, ra, rb = [(612, 39, 600, 40), (487, 21, 500, 20), (796, 51, 800, 50), (304, 68, 300, 70), (903, 29, 900, 30)][v]
        exact, estimate = a * b, ra * rb
        statement = f"{a} × {b} için {ra} × {rb} = {fmt_int(estimate)} tahmini ile kesin sonuç karşılaştırılıyor."
        correct = f"Yakınlık denetimi: Kesin sonuç {fmt_int(exact)} olup {fmt_int(estimate)} tahminiyle tutarlıdır."
        wrongs = [f"Tahmini kesin sonuç sanma: Sonucu doğrudan {fmt_int(estimate)} kabul etme", "Yaklaşık sonuç farklı diye reddetme: tahmin ile kesin sonucun eşit olmasını isteme", f"Basamak çarpımını eksik yapma: kesin sonucu {fmt_int(exact - a)} sanma"]
        explanation = f"Dağılma ile {a} × {b} = {fmt_int(exact)} bulunur; tahmin yalnız sonucun büyüklük bakımından makul olduğunu sınar."
    elif index == 5:
        whole, numerator, denominator = [(3, 2, 5), (2, 5, 6), (4, 3, 8), (1, 7, 10), (5, 1, 4)][v]
        improper = whole * denominator + numerator
        statement = f"{whole} tam {numerator}/{denominator} gösterimi bileşik kesre dönüştürülüyor."
        correct = f"Bütünleri eş parçalara çevirme: ({whole} × {denominator} + {numerator})/{denominator} = {improper}/{denominator}"
        wrongs = [f"Tam kısmı paya ekleme: {whole + numerator}/{denominator}", f"Paydayı da değiştirme: {improper}/{denominator + whole}", f"Fazladan payı atma: {whole * denominator}/{denominator}"]
        explanation = f"Her bütün {denominator} eş parça içerir; {whole} bütün ve {numerator} parça toplam {improper} tane {denominator}'de bir eder."
    elif index == 6:
        a, b, d = [(5, 8, 13), (7, 11, 15), (4, 9, 12), (13, 17, 20), (6, 14, 19)][v]
        statement = f"{a}/{d} ve {b}/{d} kesirleri aynı büyüklükte bütünler üzerinde karşılaştırılıyor."
        correct = f"Eş payda kuralı: {b}/{d} > {a}/{d}; daha çok eş parça daha büyük miktardır."
        wrongs = [f"Küçük payı büyük sanma: {a}/{d} > {b}/{d}", "Paydalar eşit diye eşit sayma: iki kesri aynı kabul etme", "Pay ile paydayı toplama: karşılaştırmayı yeni bir kesre dönüştürme"]
        explanation = f"Her iki bütün {d} eş parçaya ayrılmıştır; {b} parça {a} parçadan fazla olduğu için {b}/{d} büyüktür."
    elif index == 7:
        a, b, c, d = [(3, 5, 4, 7), (5, 6, 7, 9), (4, 9, 5, 12), (7, 10, 11, 15), (5, 8, 8, 13)][v]
        left, right = Fraction(a, b), Fraction(c, d)
        sign = ">" if left > right else "<" if left < right else "="
        common = b * d
        statement = f"{a}/{b} ile {c}/{d} ortak payda kullanılarak karşılaştırılıyor."
        correct = f"Denk kesir kanıtı: {a*d}/{common} {sign} {c*b}/{common}; dolayısıyla {a}/{b} {sign} {c}/{d}."
        wrongs = ["Yalnız payları karşılaştırma: paydaların parça büyüklüğünü yok sayma", "Pay ve paydayı çapraz toplama: iki yeni ilişkisiz kesir üretme", "Paydalar farklı diye karşılaştırmayı imkânsız sayma: denk kesir kurmama"]
        explanation = f"Paydalar {common} ortak paydasında eşitlendiğinde paylar {a*d} ve {c*b} olur; bu kanıt {sign} ilişkisini verir."
    elif index == 8:
        numerator, denominator = [(7, 20), (13, 25), (3, 5), (9, 20), (17, 50)][v]
        percent = numerator * 100 // denominator
        decimal = f"0,{percent:02d}".rstrip("0")
        statement = f"{numerator}/{denominator} kesri ondalık ve yüzde gösterimine çevriliyor."
        correct = f"Değeri koruyan dönüşüm: {numerator}/{denominator} = {percent}/100 = {decimal} = %{percent}"
        wrongs = [f"Payı doğrudan yüzde sanma: %{numerator}", f"Virgül basamağını kaydırma: 0,0{percent}", "Yalnız paydayı yüz yapma: payı aynı bırakıp değeri değiştirme"]
        explanation = f"Kesir paydası 100 olacak biçimde genişletildiğinde {percent}/100 elde edilir; bu da {decimal} ve %{percent} demektir."
    elif index == 9:
        a, b, c = [(58, 27, 60), (74, 19, 80), (46, 38, 50), (67, 25, 70), (39, 44, 40)][v]
        box = a + b - c
        statement = f"{a} + {b} = {c} + □ eşitliğinde kutu değeri ve denge ilkesi aranıyor."
        correct = f"İki tarafı eşitleme: □ = {box}; her iki taraf {a+b} eder."
        wrongs = [f"İlk değişimi yok sayma: kutuya {b} yazma", f"Farkı ters yönde taşıma: kutuya {b + abs(c-a)} yazma", f"Tarafları birleştirme: kutuya {a+b+c} yazma"]
        explanation = f"Sol taraf {number_with_copula(a+b)}; sağ tarafın aynı değeri vermesi için {c} + {box} = {a+b} olmalıdır."
    elif index == 10:
        a, b, c = [(24, 7, 5), (19, 8, 6), (32, 9, 4), (15, 12, 3), (27, 6, 8)][v]
        result = a + b * c
        statement = f"{a} + {b} × {c} işlemi parantezsiz olarak hesaplanıyor."
        correct = f"Çarpma önceliği: {b} × {c} önce yapılır ve sonuç {result} olur."
        wrongs = [f"Soldan sağa koşulsuz ilerleme: ({a} + {b}) × {c} işlemi", f"İlk ve son sayıyı çarpma: {a} × {c} + {b} işlemi", "İşaretleri tek işlem sayma: toplama ile çarpmayı aynı adımda birleştirme"]
        explanation = f"Parantez olmadığında çarpma önce yapılır: {b} × {c} = {b*c}, ardından {a} eklenerek {result} bulunur."
    elif index == 11:
        start, step = [(8, 7), (12, 5), (3, 9), (21, 4), (6, 11)][v]
        terms = [start + step * i for i in range(5)]
        sixth = start + step * 5
        statement = f"{', '.join(map(str, terms))}, ... örüntüsünün kuralı ve altıncı terimi aranıyor."
        correct = f"Sabit farkı sürdürme: Her adımda {step} eklenir; altıncı terim {sixth} olur."
        wrongs = [f"Son farkı iki katına çıkarma: altıncı terimi {terms[-1] + 2*step} alma", "Terimleri çarparak ilerleme: toplamsal kuralı çarpımsal sanma", "Başlangıç terimini adım sayısı sanma: örüntünün artışını değiştirme"]
        explanation = f"Ardışık her iki terim arasındaki fark {number_with_copula(step)}; beş kez artışla {start} + 5 × {step} = {sixth} elde edilir."
    elif index == 12:
        divisor, quotient = [(28, 34), (36, 27), (24, 43), (32, 29), (18, 56)][v]
        dividend = divisor * quotient
        statement = f"{dividend} ÷ {divisor} işleminin bölümünü çarpma ile doğrulamak gerekiyor."
        correct = f"Ters işlem doğrulaması: Bölüm {quotient}; çünkü {divisor} × {quotient} = {dividend}."
        wrongs = [f"Eksik bölüm basamağı: {quotient-2} sonucunda durma", f"Böleni bölüme ekleme: {quotient + divisor} sonucunu seçme", f"Ara çarpımı bölüm sanma: {divisor * (quotient-1)} değerini sonuç yazma"]
        explanation = f"Bölme sonucu bölenle çarpıldığında bölüneni vermelidir; {divisor} × {quotient} = {dividend} eşitliği sonucu kanıtlar."
    elif index == 13:
        task, correct, wrongs = [
            ("Bir doğru parçasının uzunluğunu ölçüp aynısını başka yerde işaretlemek", "Araç planı: Cetvelle ölç, pergelle uzunluğu taşı.", ["Yalnız açıölçer kullanma: uzunluğu derece sanma", "Pergel açıklığını taşıma sırasında değiştirme: eşitliği bozma", "Cetvelin fiziksel ucundan başlama: sıfır çizgisini yok sayma"]),
            ("Verilen noktadan 75 derecelik bir açı oluşturmak", "Araç planı: Açıölçerin merkezini köşeye, sıfır çizgisini kola yerleştir.", ["Pergelle derece okuma: uzunluk aracını açı aracı sanma", "Açıölçeri kolun ortasına koyma: köşeyi merkez almama", "Cetvelle ışın uzunluğunu 75 birim yapma: açı ile uzunluğu karıştırma"]),
            ("Bir doğru parçasının orta dikmesini çizmek", "Araç planı: Eş açıklıklı pergel yaylarını iki uçtan çizip kesişimleri cetvelle birleştir.", ["Pergel açıklığını iki uçta değiştirme: eşit uzaklığı bozma", "Yalnız orta noktayı gözle seçme: dikliği ve eşitliği ölçmeme", "Açıölçerle rastgele bir dik çizme: orta noktayı kurmama"]),
            ("5 cm uzunluğunda bir doğru parçası çizmek", "Araç planı: Cetvelin 0 çizgisinden başlayıp 5 cm işaretine ulaş.", ["Cetvelin dış kenarından başlama: ölçüm başlangıcını kaydırma", "Pergelle 5 derecelik yay çizme: birimleri karıştırma", "Açıölçerin düz kenarını ölçeksiz kullanma: uzunluğu denetlememe"]),
            ("Bir merkeze 4 cm uzaklıktaki noktaların kümesini çizmek", "Araç planı: Pergeli 4 cm açıp sivri ucu merkezde sabit tutarak çember çiz.", ["Cetvelle yalnız dört nokta işaretleme: tüm noktalar kümesini oluşturmama", "Pergel merkezini çizerken kaydırma: ortak uzaklığı bozma", "Açıölçerle 4 derecelik açı çizme: uzaklık ile açıyı karıştırma"]),
        ][v]
        statement = f"Geometrik görev: {task}. Koşulları koruyan araç sırası aranıyor."
        explanation = f"Görevdeki uzunluk, eşit uzaklık veya açı koşulu uygun aracın sabit başlangıç ve ölçme özelliğiyle kurulmalıdır. {correct}"
    elif index == 14:
        degree = [35, 90, 128, 179, 62][v]
        kind = "dar" if degree < 90 else "dik" if degree == 90 else "geniş" if degree < 180 else "doğru"
        statement = f"Ölçüsü {degree} derece olan açı ölçülüp türüyle eşleştiriliyor."
        correct = f"Ölçü aralığına göre sınıflandırma: {degree} derece {kind} açıdır."
        wrongs = ["Görünüşe göre sınıflandırma: ölçüyü kullanmadan açı türü seçme", "Işın uzunluğuna göre sınıflandırma: kol boyunu açı ölçüsü sanma", "İç ve dış ölçeği karıştırma: tamamlayan dereceyi doğrudan seçme"]
        explanation = f"Açı türü ışın uzunluğuna değil derece ölçüsüne bağlıdır; {degree} derece, {kind} açı aralığındadır."
    elif index == 15:
        situation, relation = [
            ("İki doğru kesişiyor ve oluşan açılardan biri 90 derecedir", "Doğrular diktir; dört açı da 90 derecedir."),
            ("Aynı düzlemdeki iki doğru hiçbir noktada kesişmiyor", "Doğrular paraleldir; aralarındaki uzaklık sabittir."),
            ("İki doğru tek noktada 90 dereceden farklı açılarla buluşuyor", "Doğrular kesişendir fakat dik değildir."),
            ("Bir doğru, paralel iki doğruyu ayrı noktalarda kesiyor", "Üçüncü doğru kesendir; paralellik yalnız ilk iki doğru arasındadır."),
            ("Bir yatay ve bir düşey doğru aynı noktadan geçiyor", "Doğrular diktir ve kesişme noktasında dik açılar oluşur."),
        ][v]
        statement = f"Doğru ilişkisi gözlemi: {situation}. Uygun geometrik sonuç aranıyor."
        correct = f"Tanıma dayalı ilişki: {relation}"
        wrongs = ["Kesişmeyi paralellik sanma: ortak noktayı yok sayma", "Dikliği yalnız çizimin yönüne bağlama: açı ölçüsünü denetlememe", "Her kesişen doğruyu dik sanma: 90 derece koşulunu aramama"]
        explanation = f"Paralellik ortak nokta olmamasına, diklik ise kesişme açısının 90 derece olmasına göre belirlenir. {relation}"
    elif index == 16:
        sides, name = [(5, "beşgen"), (6, "altıgen"), (7, "yedigen"), (8, "sekizgen"), (4, "dörtgen")][v]
        statement = f"Kapalı bir şeklin {sides} doğru parçası kenarı ve {sides} köşesi vardır. Şekil sınıflandırılıyor."
        correct = f"Kenar sayısına göre adlandırma: Bu şekil bir {name}dir."
        wrongs = ["Köşe sayısını bir eksiltme: açık şekil gibi adlandırma", "Kenar uzunluklarına bakma: çokgen adını eşitlik koşuluna bağlama", "Eğri sınırı doğru parçası sayma: çokgen tanımını bozma"]
        explanation = f"Çokgenler doğru parçası kenarlarının sayısına göre adlandırılır; {sides} kenarlı kapalı şeklin adı {name}dir."
    elif index == 17:
        a, b, c = [(5, 7, 9), (6, 8, 13), (4, 6, 11), (7, 7, 12), (3, 5, 7)][v]
        possible = a + b > c and a + c > b and b + c > a
        statement = f"Pergelle {a} cm, {b} cm ve {c} cm kenarlı bir üçgen kurulmak isteniyor."
        if possible:
            correct = "Yayların kesişmesiyle kurulum mümkündür: Her iki kısa kenarın toplamı üçüncü kenardan büyüktür."
        else:
            correct = "Yaylar kesişmediği için kurulum mümkün değildir: İki kısa kenarın toplamı üçüncü kenardan büyük değildir."
        wrongs = ["Yalnız en uzun kenara bakma: diğer iki uzunluğun toplamını denetlememe", "Pergel açıklığını çizim sırasında değiştirme: verilen kenarları korumama", "Her üç pozitif uzunluğun üçgen kurduğunu sanma: kesişme koşulunu yok sayma"]
        explanation = f"Üçgen kurulması için her iki kenarın toplamı üçüncüden büyük olmalıdır; {a}, {b}, {c} uzunlukları bu koşula göre değerlendirilir."
    elif index == 18:
        perimeter, long_side = [(74, 22), (86, 27), (58, 19), (92, 31), (66, 20)][v]
        short = perimeter // 2 - long_side
        statement = f"Çevresi {perimeter} cm, uzun kenarı {long_side} cm olan dikdörtgenin kısa kenarı bulunuyor."
        correct = f"Yarı çevre yöntemi: {perimeter} ÷ 2 - {long_side} = {short} cm"
        wrongs = [f"Tek kenarı çevreden çıkarma: {perimeter - long_side} cm", f"Dikdörtgeni kare sanma: {perimeter / 4:g} cm", f"İki uzun kenarı çıkarıp ikiye bölmeme: {perimeter - 2*long_side} cm"]
        explanation = f"Bir uzun ve bir kısa kenarın toplamı {perimeter//2} cm'dir; {long_side} çıkarılınca kısa kenar {short} cm olur."
    elif index == 19:
        width, height = [(13, 8), (17, 6), (12, 9), (15, 7), (14, 11)][v]
        area = width * height
        statement = f"{width} cm ile {height} cm kenarlı dikdörtgen birim karelerle kaplanıyor. Alanı aranıyor."
        correct = f"Satır-sütun çarpımı: {width} × {height} = {area} cm²"
        wrongs = [f"Kenarları toplama: {width + height} cm²", f"Çevreyi alan sanma: {2*(width+height)} cm²", f"Kenar farkını kullanma: {abs(width-height)} cm²"]
        explanation = f"Her satırda {width} ve toplam {height} satır olduğundan {width} × {height} = {area} birim kare bulunur."
    elif index == 20:
        w1, h1, w2, h2 = [(12, 6, 10, 8), (14, 5, 9, 8), (11, 7, 13, 6), (16, 4, 10, 7), (9, 9, 15, 5)][v]
        a1, a2 = w1*h1, w2*h2
        p1, p2 = 2*(w1+h1), 2*(w2+h2)
        statement = f"A dikdörtgeni {w1}×{h1}, B dikdörtgeni {w2}×{h2} cm ölçülerindedir; alan ve çevre birlikte karşılaştırılıyor."
        correct = f"İki ölçütü ayrı hesaplama: Alanlar {a1} ve {a2} cm²; çevreler {p1} ve {p2} cm'dir."
        wrongs = ["Alan ile çevreyi aynı birimle karşılaştırma: cm ve cm² farkını yok sayma", "Yalnız kenar toplamlarına bakma: alan için çarpımı kullanmama", "Aynı çevrenin aynı alan verdiğini varsayma: kenar dağılımını incelememe"]
        explanation = f"Alan kenarların çarpımı, çevre kenarların toplamının iki katıdır; ayrı hesaplar A için {a1}/{p1}, B için {a2}/{p2} sonuçlarını verir."
    elif index == 21:
        counts = [(9, 14, 7, 10), (12, 8, 15, 5), (6, 13, 11, 9), (16, 7, 10, 12), (8, 17, 6, 11)][v]
        total, maximum, minimum = sum(counts), max(counts), min(counts)
        statement = f"Bir ankette dört kategorinin sıklıkları sırasıyla {counts[0]}, {counts[1]}, {counts[2]}, {counts[3]} verilmiştir. Toplam ve açıklık yorumlanıyor."
        correct = f"Veriye dayalı özet: Toplam {total}, en yüksek-en düşük farkı {maximum-minimum} kişidir."
        wrongs = ["Yalnız en yüksek sütunu toplam sanma: öteki kategorileri dışlama", "Kategori adlarını sayısal veri sanma: sıklıklar yerine kategori sayısını kullanma", "Örneklemden topluma kesin genelleme yapma: araştırma kapsamını aşma"]
        explanation = f"Sıklıkların toplamı {number_with_copula(total)}; en yüksek {maximum} ile en düşük {minimum} arasındaki fark {maximum-minimum} olur ve yorum yalnız ankete katılan grupla sınırlıdır."
    else:
        red, blue, green = [(3, 5, 2), (4, 3, 5), (2, 7, 3), (6, 2, 4), (5, 6, 1)][v]
        total = red + blue + green
        target = Fraction(blue, total)
        statement = f"Bir torbada {red} kırmızı, {blue} mavi ve {green} yeşil eş büyüklükte top vardır; mavi çekme olasılığı aranıyor."
        correct = f"İstenen/bütün sonuç oranı: {blue}/{total} = {target.numerator}/{target.denominator}"
        wrongs = [f"Yalnız istenenleri paydaya yazma: {blue}/{blue}", f"İstenmeyenleri pay sayma: {red+green}/{total}", f"Pay ile paydayı ters kurma: {total}/{blue}"]
        explanation = f"Tek çekilişte {total} eş olasılıklı top vardır ve bunların {blue} tanesi mavidir; olasılık {blue}/{total} olur."
    return statement, correct, list(wrongs), explanation


def table(qid: str, statement: str, labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.alt"
    labels[h1], labels[h2] = "İncelenen kayıt", "Çözüm görevi"
    labels[alt] = "Bir matematiksel veri kaydı ile bu kayda uygulanacak çözüm görevini gösteren tablo; doğru sonuç belirtilmemiştir."
    return {
        "kind": "table", "headerKeys": [h1, h2], "altTextKey": alt,
        "rows": [[{"v": statement}, {"v": "Verileri konu kuralıyla çözümle ve sonucu denetle."}]],
    }


def make(local: int, occurrence: int, note_map: dict[str, dict[str, Any]], labels: dict[str, str]) -> dict[str, Any]:
    global_number = 900 + local
    index = (local - 1) % len(NOTE_IDS)
    note = note_map[NOTE_IDS[index]]
    objectives = [str(value) for value in note.get("objectives") or [""]]
    objective = objectives[occurrence % len(objectives)]
    statement, correct_text, wrongs, explanation = case_data(index, occurrence)
    mode, level = MODES[local - 1], LEVELS[local - 1]
    context = CONTEXTS[(local + occurrence) % len(CONTEXTS)]
    correct = (global_number - 1) % 4
    raw_choices = [correct_text, *wrongs]
    raw_reasons = [
        f"Doğru matematiksel model: {explanation}",
        f"İlişkiyi eksik kurma yanılgısı: İlk yanlış strateji verilen niceliklerin veya geometrik koşulların tümünü kullanmaz. {explanation}",
        f"Kural ve temsil yanılgısı: İkinci yanlış strateji konu anlatımındaki işlem, birim ya da sınıflandırma kuralını değiştirir. {explanation}",
        f"Dayanaksız genelleme yanılgısı: Üçüncü yanlış stratejinin sonucu verilen kayıt veya ters işlemle doğrulanamaz. {explanation}",
    ]
    choices, distractor_why = base.rotate(raw_choices, raw_reasons, correct)
    qid = f"tr-g05-bank-mat-b02-q{local:03d}"
    if mode == "comprehension":
        stem = f"{context.capitalize()} içinde kavramın anlamı denetleniyor. {statement} İlişkiyi doğru açıklayan seçenek hangisidir?"
        fig = None
    elif mode == "application":
        stem = f"{context.capitalize()} uygulamasında şu problem çözülüyor: {statement} Verileri doğru yönteme aktaran işlem veya sonuç hangisidir?"
        fig = None
    elif mode == "analysis":
        stem = (
            f"Aşağıdaki tabloyu inceleyiniz. {context.capitalize()} tablosunda '{note['title']}' konusuna ait bir veri kaydı vardır. "
            "Kaydı bağlı konu kuralına göre çözümleyip bağımsız olarak doğrulayan seçenek hangisidir?"
        )
        fig = table(qid, statement, labels)
    else:
        stem = f"{context.capitalize()} sırasında bir öğrenci '{wrongs[0]}' sonucunu savunuyor. {statement} Yanılgıyı düzelten kanıt hangisidir?"
        fig = None
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "Çözümlenecek matematiksel veri ve görev yalnız tabloda birlikte verilmiştir.",
        "acceptableKinds": ["table"], "evidenceDimensions": ["veri", "çözüm görevi", "doğrulama"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "Çözüm için gereken bütün nicelikler ve koşullar soru metninde verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "Matematik", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — {mode}",
        "objective": objective, "objectiveId": objective,
        "noteId": note.get("id"), "noteKey": note.get("id"),
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct],
        "distractorWhy": distractor_why,
        "explanation": f"Çözüm, bağlı konu anlatımındaki kural ve ters denetimle kurulmuştur. {explanation}",
        "level": level,
        "difficultyReason": f"Düzey {level}; matematiksel veriyi {mode} biçiminde modele dönüştürmeyi, doğru işlemi yürütmeyi ve sonucu gerekçeyle sınamayı gerektirir.",
        "questionType": mode, "familyId": f"tr-g05-bank-mat-family-{global_number:03d}",
        "objectiveSource": note.get("objectiveSource"),
        "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [], "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    existing = [json.loads(line) for line in base.OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 900:
        raise RuntimeError("the first 900 grade questions must be regenerated before math batch 02")
    labels = json.loads(base.LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = base.notes()
    occurrences = [0] * len(NOTE_IDS)
    rows = []
    for local in range(1, 101):
        index = (local - 1) % len(NOTE_IDS)
        rows.append(make(local, occurrences[index], note_map, labels))
        occurrences[index] += 1
    base.OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    base.LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"mathQuestions": 100, "mathTotal": 115, "gradeTotal": 1000}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
