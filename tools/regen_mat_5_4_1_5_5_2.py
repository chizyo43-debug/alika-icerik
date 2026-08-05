# -*- coding: utf-8 -*-
"""A3 parti 7 — MAT.5.4.1 ve MAT.5.5.2 ailelerinin yeniden üretimi.

Kural 39'un (dolgu çeldirici) on ihlalinin sekizi bu iki aileden geçiyordu:
'20 cm'×7, '12 cm'×6, '48 cm'×5, '26 cm'×4, '16 cm'×4, '11 cm'×4,
'Öğrencinin sonucu doğrudur'×4, 'Sonuçlar ülkedeki bütün öğrencileri kesin
olarak gösterir.'×5, 'Katılımcı sayısı yalnız en büyük sıklığa eşittir.'×4,
'Bütün kategorilerin sıklıkları eşittir.'×4.

Sebep ikisinde de aynı: beş kalıbın beşer kez tekrarı. 5-5-2'de q003, q008,
q013 ve q018 aslında tek bir soruydu; yalnız kök cümlesi yeniden ifade
edilmişti ("hangi uyarı doğrudur / geçerlidir / doğru kabul edilir / her zaman
doğrudur"). Aynı dört çeldirici dört kez dolaştığı için kalıbı fark eden
öğrenci bunları eleyebiliyordu.

5-4-1 yeni kapsamı, notun (tr.g05.mat.5.4.note.01) anlattığı bütün noktaları
içerir: çevre formülü, yarı çevre, çevre ve bir kenardan diğer kenar, kare
özel durumu, "yalnız çevre verilince tek dikdörtgen belirlenemez" ilkesi ve
ikinci koşulun (kenar farkı, kat ilişkisi) gerekliliği.

5-5-2 yeni kapsamı 5-5-1 ile çakışmayacak biçimde yorumlama ve eleştiriye
odaklanır: ölçekli sütun, kesilmiş eksen, "en yüksek sütun çoğunluk demek
değildir", veriden çıkarılamayan sonuç, yanıltıcı sunum, iki grafiği
karşılaştırma.

choices + correct + distractorWhy + hints + explanation tek birimde üretildi
(AUTHORING_RULES.md §1 atomiklik ilkesi).
"""

KAYNAK = "https://tymm.meb.gov.tr/upload/program/2024programmat5678Onayli.pdf"

# ---------------------------------------------------------------------------
# MAT.5.4.1 — note.01 "Çevresi verilen dikdörtgenin kenarlarını bulma"
# ---------------------------------------------------------------------------

A41 = [
    dict(
        level=1,
        question="Çevresi 56 cm olan bir dikdörtgenin bir kenarı 23 cm'dir. Diğer kenarı kaç santimetredir?",
        birim="cm",
        dogru=56 // 2 - 23,
        celdiriciler=[
            (56 - 23, "Çevreyi 2'ye bölmeden bilinen kenarı çıkarmış: 56 − 23."),
            (56 // 2, "Yarı çevreyi bulup orada durmuş; bilinen kenarı çıkarmamış."),
            (2 * (56 // 2 - 23), "Bulduğu kenarı ikiyle çarpmış; kenar çevrede iki kez sayılsa da uzunluğu tekildir."),
        ],
        explanation="Çevre 2 × (a + b) olduğuna göre yarı çevre bir uzun ve bir kısa kenarın "
                    "toplamıdır: 56 ÷ 2 = 28. Bilinen kenar çıkarılır: 28 − 23 = 5 cm.",
        difficultyReason="2 adım; ön bilgi: yarı çevrenin iki komşu kenarın toplamı olması; çeldiriciler yakın (bölmeyi atlama); beceri: hesaplama",
        hints=[
            "Dikdörtgende kaç kenar bulunduğunu ve kaçının eşit olduğunu hatırla.",
            "Çevrenin yarısının hangi iki kenarı kapsadığını düşün.",
            "Çevreyi ikiye bölerek yarı çevreyi bul.",
            "Bilinen kenarı yarı çevreden çıkarmayı dene.",
            "Tam çözüm: yarı çevre 56 ÷ 2 = 28'dir; 28 − 23 = 5 cm bulunur.",
        ],
    ),
    dict(
        level=2,
        question="Kenarları 7 cm ve 3 cm olan bir dikdörtgenin yarı çevresi kaç santimetredir?",
        birim="cm",
        dogru=7 + 3,
        celdiriciler=[
            (2 * (7 + 3), "Yarı çevre yerine çevrenin tamamını hesaplamış."),
            (7 * 3, "Kenarları toplamak yerine çarpmış."),
            (7 - 3, "Kenarları toplamak yerine farklarını almış."),
        ],
        explanation="Yarı çevre, bir uzun ve bir kısa kenarın toplamıdır: 7 + 3 = 10 cm. "
                    "Çevrenin tamamı bunun iki katı, yani 20 cm olur.",
        difficultyReason="1 adım; ön bilgi: yarı çevre tanımı; çeldiriciler yakın (tam çevreyi yanıt sanma); beceri: kavram uygulama",
        hints=[
            "Yarı çevrenin kaç kenarı kapsadığını söyle.",
            "Dikdörtgende hangi kenarların eşit olduğunu hatırla.",
            "Birbirine komşu iki kenarı seç.",
            "Bu iki kenarı toplamayı dene.",
            "Tam çözüm: yarı çevre bir uzun ve bir kısa kenarın toplamıdır: 7 + 3 = 10 cm.",
        ],
    ),
    dict(
        level=2,
        question="Çevresi 40 cm olan bir karenin bir kenarı kaç santimetredir?",
        birim="cm",
        dogru=40 // 4,
        celdiriciler=[
            (40 // 2, "Karenin çevresini dikdörtgen gibi ikiye bölmüş; karede dört kenar da eşittir."),
            (40 - 4, "Çevreden kenar sayısını çıkarmış."),
            (40 * 4, "Bölme yerine çarpma yapmış."),
        ],
        explanation="Karede dört kenar da eşittir, bu yüzden çevre kenarın 4 katıdır. "
                    "Kenar 40 ÷ 4 = 10 cm bulunur.",
        difficultyReason="1 adım; ön bilgi: karede dört kenarın eşitliği; çeldiriciler yakın (dikdörtgen kuralını uygulama); beceri: hesaplama",
        hints=[
            "Karenin kaç kenarı olduğunu ve bunların eşit olup olmadığını söyle.",
            "Çevrenin kenar cinsinden nasıl yazıldığını düşün.",
            "Dikdörtgen için kullandığın yarı çevre yolunun karede geçerli olup olmadığını sorgula.",
            "Çevreyi kenar sayısına bölmeyi dene.",
            "Tam çözüm: karede çevre kenarın 4 katıdır; 40 ÷ 4 = 10 cm bulunur.",
        ],
    ),
    dict(
        level=3,
        question="Bir öğrenci kenarları 16 cm ve 5 cm olan dikdörtgenin çevresini 44 cm bulmuştur. Bu sonuç için ne söylenebilir?",
        choices=[
            "Doğrudur; çevre 2 × (16 + 5) = 42 cm'dir.",
            "Yanlıştır; öğrenci bir kenarı fazladan saymıştır, çevre 42 cm olmalıdır.",
            "Yanlıştır; çevre iki kenarın çarpımıdır, 80 cm olmalıdır.",
            "Yanlıştır; çevre yarı çevreye eşittir, 21 cm olmalıdır.",
        ],
        correct=1,
        distractorWhy=[
            "Bu seçenek sonucu doğru sayarken kendi içinde 42 değerini veriyor; 44 ile 42 aynı sayı değildir.",
            "doğru",
            "Çevre kenarların çarpımı değil toplamıdır; çarpım alan hesabına aittir.",
            "Yarı çevre çevrenin yarısıdır; çevrenin kendisi bunun iki katıdır.",
        ],
        explanation="Çevre 2 × (16 + 5) = 2 × 21 = 42 cm'dir. Öğrencinin bulduğu 44 sayısı 2 cm "
                    "fazladır; bir kenar uzunluğu fazladan sayılmıştır.",
        difficultyReason="3 adım; ön bilgi: çevre formülünün uygulanması ve sonucun sınanması; çeldiriciler yakın (çevre ile alanı ya da yarı çevreyi karıştırma); beceri: hata teşhisi",
        hints=[
            "Çevreyi kendin hesaplayıp bir kenara yaz.",
            "Bulduğun değeri öğrencinin sonucuyla karşılaştır.",
            "Aradaki farkı hesapla.",
            "Bu farkın hangi hatadan gelebileceğini düşün.",
            "Tam çözüm: 2 × (16 + 5) = 42 cm'dir; öğrencinin bulduğu 44 sayısı 2 cm fazladır.",
        ],
    ),
    dict(
        level=4,
        question="Yalnız çevresi 30 cm olduğu bilinen bir dikdörtgenin kenarları için ne söylenebilir?",
        choices=[
            "Kenarlar tek bir biçimde belirlenir; her ikisi de 7,5 cm'dir.",
            "Kenarlar belirlenemez; toplamı 15 cm olan farklı kenar çiftleri bulunabilir.",
            "Kenarlar belirlenemez; çevreden hiçbir bilgi çıkarılamaz.",
            "Kenarlar tek bir biçimde belirlenir; uzun kenar 20 cm, kısa kenar 10 cm'dir.",
        ],
        correct=1,
        distractorWhy=[
            "Bu, kenarların eşit olduğu özel durumdur ve o şekil bir karedir; dikdörtgen için tek olasılık değildir.",
            "doğru",
            "Çevreden bilgi çıkarılabilir: yarı çevre 15 cm'dir ve kenarların toplamı bu değerdir.",
            "Bu iki kenarın toplamı 30 cm'dir; oysa yarı çevre 15 cm olmalıdır.",
        ],
        explanation="Çevre 30 cm ise yarı çevre 15 cm'dir; kenarların toplamı 15 cm olmak zorundadır "
                    "ama bu toplamı veren birden çok kenar çifti vardır (14 ve 1; 12 ve 3; 9 ve 6 gibi). "
                    "Kenarları belirlemek için ikinci bir koşul gerekir.",
        difficultyReason="4 adım; ön bilgi: yalnız çevrenin dikdörtgeni tek başına belirlememesi; çeldiriciler yakın (özel durumu genel sanma); beceri: akıl yürütme",
        hints=[
            "Çevreden hangi bilgiyi kesin olarak çıkarabileceğini yaz.",
            "Bu bilgiyi sağlayan birkaç kenar çifti dene.",
            "Bulduğun çiftlerin sayısına bak: bir tane mi, birden çok mu?",
            "Tek bir dikdörtgene ulaşmak için başka ne bilinmesi gerektiğini düşün.",
            "Tam çözüm: yarı çevre 15 cm'dir ve bu toplamı veren birçok kenar çifti bulunur; kenarları belirlemek için ikinci bir koşul gerekir.",
        ],
    ),
    dict(
        level=1,
        question="Çevresi 38 cm olan bir dikdörtgenin bir kenarı 15 cm'dir. Diğer kenarı kaç santimetredir?",
        birim="cm",
        dogru=38 // 2 - 15,
        celdiriciler=[
            (38 - 15, "Çevreyi 2'ye bölmeden bilinen kenarı çıkarmış."),
            (38 // 2, "Yarı çevreyi bulup orada durmuş."),
            (2 * (38 // 2 - 15), "Bulduğu kenarı bir de ikiyle çarpmış; kenar tekil bir uzunluktur."),
        ],
        explanation="Yarı çevre 38 ÷ 2 = 19 cm'dir. Bilinen kenar çıkarılır: 19 − 15 = 4 cm.",
        difficultyReason="2 adım; ön bilgi: çevre ve bir kenardan diğer kenarın bulunması; çeldiriciler yakın (bölmeyi atlama, ara sonucu yanıt sanma); beceri: hesaplama",
        hints=[
            "Çevrenin kaç kenarı kapsadığını hatırla.",
            "Yarı çevrenin hangi iki kenara karşılık geldiğini düşün.",
            "Yarı çevreyi hesapla.",
            "Bilinen kenarı yarı çevreden çıkar.",
            "Tam çözüm: 38 ÷ 2 = 19 ve 19 − 15 = 4 cm bulunur.",
        ],
    ),
    dict(
        level=3,
        question="Çevresi 46 cm olan bir dikdörtgen için aşağıdaki kenar çiftlerinden hangisi mümkündür?",
        choices=[
            "14 cm ve 9 cm",
            "24 cm ve 22 cm",
            "30 cm ve 16 cm",
            "13 cm ve 8 cm",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Bu çiftin toplamı 46 cm'dir; oysa yarı çevre 23 cm olmalıdır, 46 cm çevrenin kendisidir.",
            "Bu çiftin toplamı 46 cm'dir; kenarlar yarı çevreye göre seçilmelidir.",
            "Bu çiftin toplamı 21 cm'dir; yarı çevre 23 cm olmalıdır.",
        ],
        explanation="Yarı çevre 46 ÷ 2 = 23 cm'dir; kenar çiftinin toplamı 23 olmalıdır. "
                    "14 + 9 = 23 olduğundan bu çift mümkündür.",
        difficultyReason="3 adım; ön bilgi: kenar çiftinin toplamının yarı çevreye eşit olması; çeldiriciler yakın (toplamı çevreye eşitleme); beceri: seçenek eleme; hesaplama",
        hints=[
            "Önce yarı çevreyi hesapla.",
            "Bir kenar çiftinin toplamının hangi değere eşit olması gerektiğini yaz.",
            "Her seçenekteki iki kenarı topla.",
            "Toplamı yarı çevreye eşit olan çifti seç.",
            "Tam çözüm: yarı çevre 23 cm'dir; 14 + 9 = 23 olduğundan bu çift mümkündür.",
        ],
    ),
    dict(
        level=4,
        question="Çevresi 34 cm olan bir dikdörtgende uzun kenar kısa kenardan 3 cm fazladır. Kısa kenar kaç santimetredir?",
        birim="cm",
        dogru=(34 // 2 - 3) // 2,
        celdiriciler=[
            (34 // 2 - 3, "Yarı çevreden farkı çıkarıp orada durmuş; kalan değer iki kısa kenara aittir."),
            ((34 // 2 - 3) // 2 + 3, "Kısa kenarı bulduktan sonra uzun kenarı yazmış."),
            (34 // 2, "Yarı çevreyi kısa kenar sanmış."),
        ],
        explanation="Yarı çevre 34 ÷ 2 = 17 cm'dir ve bir kısa ile bir uzun kenarın toplamıdır. "
                    "Uzun kenar 3 cm fazla olduğuna göre farkı çıkarınca 17 − 3 = 14 kalır; bu değer "
                    "iki kısa kenara eşittir. Kısa kenar 14 ÷ 2 = 7 cm'dir.",
        difficultyReason="5 adım; ön bilgi: yarı çevre ve kenar farkının birlikte kullanılması; çeldiriciler yakın (ara sonucu ya da diğer kenarı yanıt sanma); beceri: model kurma; hesaplama",
        hints=[
            "Yarı çevrenin hangi iki kenarın toplamı olduğunu yaz.",
            "İki kenar arasındaki farkın verildiğini fark et.",
            "Yarı çevreden farkı çıkarınca elde kalan değerin neye karşılık geldiğini düşün.",
            "Kalan değerin kaç eşit parçaya ayrılacağına karar ver.",
            "Tam çözüm: yarı çevre 17'dir; 17 − 3 = 14 iki kısa kenara aittir ve kısa kenar 14 ÷ 2 = 7 cm bulunur.",
        ],
    ),
    dict(
        level=4,
        question="Çevresi 36 cm olan bir dikdörtgende uzun kenar kısa kenarın 2 katıdır. Uzun kenar kaç santimetredir?",
        birim="cm",
        dogru=2 * (36 // 2 // 3),
        celdiriciler=[
            (36 // 2 // 3, "Kısa kenarı bulup orada durmuş; soru uzun kenarı istiyor."),
            (36 // 2, "Yarı çevreyi uzun kenar sanmış."),
            (36 // 2 // 2, "Yarı çevreyi iki eşit parçaya bölmüş; paylar 1 ve 2 olduğu için toplam 3 pay vardır."),
        ],
        explanation="Yarı çevre 36 ÷ 2 = 18 cm'dir. Kısa kenara 1 pay dersek uzun kenara 2 pay düşer; "
                    "toplam 3 pay 18 cm eder. Bir pay 18 ÷ 3 = 6 cm olduğundan uzun kenar 2 × 6 = 12 cm'dir.",
        difficultyReason="5 adım; ön bilgi: yarı çevrenin pay düşünmeyle bölünmesi; çeldiriciler yakın (ara sonucu ya da yanlış bölmeyi yanıt sanma); beceri: model kurma; hesaplama",
        hints=[
            "Önce yarı çevreyi bul.",
            "Kısa kenara 1 pay dersen uzun kenara kaç pay düşeceğini yaz.",
            "Toplam kaç pay olduğunu hesapla.",
            "Bir payın değerini bulup sorulan kenarı yaz.",
            "Tam çözüm: yarı çevre 18'dir, toplam 3 pay eder; bir pay 6 cm olduğundan uzun kenar 2 × 6 = 12 cm'dir.",
        ],
    ),
    dict(
        level=2,
        question="Çevresi 24 cm olan bir karenin bir kenarı kaç santimetredir?",
        birim="cm",
        dogru=24 // 4,
        celdiriciler=[
            (24 // 2, "Karede de yarı çevre yolunu kullanmış; karede dört kenar eşit olduğu için çevre dörde bölünür."),
            (24 // 3, "Çevreyi üçe bölmüş; karenin dört kenarı vardır."),
            (24 - 4, "Çevreden kenar sayısını çıkarmış."),
        ],
        explanation="Karede çevre kenarın 4 katıdır: kenar 24 ÷ 4 = 6 cm.",
        difficultyReason="1 adım; ön bilgi: karenin çevre formülü; çeldiriciler yakın (yanlış bölen seçme); beceri: hesaplama",
        hints=[
            "Karenin kenar sayısını yaz.",
            "Kenarların hepsinin eşit olup olmadığını söyle.",
            "Çevrenin kenar cinsinden kaç katı olduğunu belirle.",
            "Çevreyi bu sayıya bölmeyi dene.",
            "Tam çözüm: karede çevre kenarın 4 katıdır; 24 ÷ 4 = 6 cm bulunur.",
        ],
    ),
    dict(
        level=3,
        question="Bir dikdörtgenin kısa kenarı 4 cm uzatılırsa çevresi kaç santimetre artar?",
        birim="cm",
        dogru=8,
        celdiriciler=[
            (4, "Uzatmayı bir kez saymış; dikdörtgende karşılıklı iki kenar birden uzar."),
            (16, "Uzatmayı dört kenara birden uygulamış; yalnız karşılıklı iki kenar değişir."),
            (2, "Uzatmanın yarısını almış."),
        ],
        explanation="Dikdörtgende karşılıklı kenarlar eşittir; kısa kenar uzatılınca iki kenar birden "
                    "uzar. Çevre artışı 2 × 4 = 8 cm olur.",
        difficultyReason="3 adım; ön bilgi: dikdörtgende karşılıklı kenarların birlikte değişmesi; çeldiriciler yakın (artışı bir ya da dört kez sayma); beceri: akıl yürütme",
        hints=[
            "Dikdörtgende kaç kenarın kısa kenar olduğunu say.",
            "Bir kenar uzatılınca eşiti olan kenara ne olduğunu düşün.",
            "Çevrenin kaç kenardan oluştuğunu hatırla.",
            "Uzatmanın kaç kez çevreye eklendiğini belirle.",
            "Tam çözüm: iki kısa kenar birden uzadığından çevre 2 × 4 = 8 cm artar.",
        ],
    ),
    dict(
        level=5,
        question="Kenar uzunlukları santimetre cinsinden tam sayı olan ve çevresi 20 cm olan kaç farklı dikdörtgen çizilebilir? (Kenarları yer değiştirmiş olanlar aynı sayılır.)",
        birim="",
        dogru=5,
        celdiriciler=[
            (10, "Yarı çevreyi doğrudan yanıt yazmış; her kenar çifti için ayrı bir dikdörtgen sayılmaz."),
            (9, "Kenar çiftlerini yer değiştirmiş hâlleriyle birlikte saymış."),
            (4, "Kenarları eşit olan durumu (kare) saymamış; kare de bir dikdörtgendir."),
        ],
        explanation="Yarı çevre 20 ÷ 2 = 10 cm'dir; iki kenarın toplamı 10 olmalıdır. Tam sayı çiftler "
                    "1+9, 2+8, 3+7, 4+6 ve 5+5'tir. Yer değiştirmiş hâller aynı sayıldığından 5 farklı "
                    "dikdörtgen çizilebilir; bunlardan 5+5 olanı karedir.",
        difficultyReason="5 adım; ön bilgi: yarı çevreyi veren tam sayı çiftlerinin sistemli sayılması ve karenin de dikdörtgen olması; çeldiriciler çok yakın (sıralı sayma, kareyi dışlama); beceri: sistemli sayma; akıl yürütme",
        hints=[
            "Önce iki kenarın toplamının kaç olması gerektiğini bul.",
            "Bu toplamı veren tam sayı çiftlerini küçükten başlayarak sırayla yaz.",
            "Yer değiştirmiş çiftleri tekrar saymadığından emin ol.",
            "Kenarları eşit olan durumun da bir dikdörtgen sayılıp sayılmayacağına karar ver.",
            "Tam çözüm: toplamı 10 olan çiftler 1+9, 2+8, 3+7, 4+6 ve 5+5'tir; 5 farklı dikdörtgen çizilebilir.",
        ],
    ),
    dict(
        level=1,
        question="Çevresi 26 cm olan bir dikdörtgenin bir kenarı 10 cm'dir. Diğer kenarı kaç santimetredir?",
        birim="cm",
        dogru=26 // 2 - 10,
        celdiriciler=[
            (26 - 10, "Çevreyi 2'ye bölmeden bilinen kenarı çıkarmış."),
            (26 // 2, "Yarı çevreyi bulup orada durmuş."),
            (10, "Verilen kenarı yeniden yazmış; dikdörtgende komşu kenarlar eşit olmak zorunda değildir."),
        ],
        explanation="Yarı çevre 26 ÷ 2 = 13 cm'dir; bilinen kenar çıkarılır: 13 − 10 = 3 cm.",
        difficultyReason="2 adım; ön bilgi: çevre ve bir kenardan diğerinin bulunması; çeldiriciler yakın (bölmeyi atlama); beceri: hesaplama",
        hints=[
            "Çevrenin iki uzun ve iki kısa kenarı kapsadığını hatırla.",
            "Yarı çevreyi hesapla.",
            "Yarı çevrenin hangi iki kenara ait olduğunu söyle.",
            "Bilinen kenarı yarı çevreden çıkar.",
            "Tam çözüm: 26 ÷ 2 = 13 ve 13 − 10 = 3 cm bulunur.",
        ],
    ),
    dict(
        level=2,
        question="Dikdörtgenin çevresini veren ifade aşağıdakilerden hangisidir?",
        choices=[
            "a × b",
            "a + b",
            "2 × (a + b)",
            "4 × a",
        ],
        correct=2,
        distractorWhy=[
            "Bu ifade iki kenarın çarpımıdır ve alan hesabına aittir; çevre bir uzunluktur.",
            "Bu ifade yalnız yarı çevreyi verir; çevre bunun iki katıdır.",
            "doğru",
            "Bu ifade karenin çevresidir; dikdörtgende kenarlar iki farklı uzunluktadır.",
        ],
        explanation="Dikdörtgende karşılıklı kenarlar eşittir: çevre a + b + a + b, yani "
                    "2 × (a + b) olur.",
        difficultyReason="2 adım; ön bilgi: çevre formülünün türetilmesi; çeldiriciler yakın (alan, yarı çevre ve kare formülü); beceri: formül tanıma",
        hints=[
            "Dikdörtgenin kaç kenarı olduğunu ve kaçının eşit olduğunu yaz.",
            "Bütün kenarları tek tek toplayarak bir ifade kur.",
            "Kurduğun ifadeyi kısaltmayı dene.",
            "Alan ile çevrenin farklı büyüklükler olduğunu göz önüne al.",
            "Tam çözüm: kenarlar a + b + a + b biçiminde toplanır ve bu 2 × (a + b) olarak yazılır.",
        ],
    ),
    dict(
        level=3,
        question="Bir dikdörtgen ile bir karenin çevreleri eşittir. Dikdörtgenin kenarları 11 cm ve 5 cm ise karenin bir kenarı kaç santimetredir?",
        birim="cm",
        dogru=2 * (11 + 5) // 4,
        celdiriciler=[
            (11 + 5, "Yarı çevreyi karenin kenarı sanmış."),
            (2 * (11 + 5), "Çevrenin tamamını karenin kenarı sanmış."),
            (11, "Dikdörtgenin uzun kenarını yazmış; çevreleri eşit olan şekillerin kenarları eşit olmak zorunda değildir."),
        ],
        explanation="Dikdörtgenin çevresi 2 × (11 + 5) = 32 cm'dir. Karenin çevresi de 32 cm "
                    "olduğuna göre bir kenarı 32 ÷ 4 = 8 cm'dir.",
        difficultyReason="4 adım; ön bilgi: iki şeklin çevresini ortak bir değer üzerinden bağlama; çeldiriciler yakın (ara sonucu kenar sanma); beceri: model kurma; hesaplama",
        hints=[
            "Önce dikdörtgenin çevresini hesapla.",
            "Bu değerin karenin çevresine eşit olduğunu yaz.",
            "Karede çevrenin kenar cinsinden kaç katı olduğunu hatırla.",
            "Çevreyi kenar sayısına bölmeyi dene.",
            "Tam çözüm: dikdörtgenin çevresi 2 × 16 = 32 cm'dir; karenin kenarı 32 ÷ 4 = 8 cm bulunur.",
        ],
    ),
    dict(
        level=4,
        question="Bir bahçenin çevresine tel çekilecektir. Bahçe dikdörtgen biçiminde olup uzun kenarı 18 m, kısa kenarı 12 m'dir. Kapı için 3 m'lik bir açıklık bırakılacağına göre kaç metre tel gerekir?",
        birim="m",
        dogru=2 * (18 + 12) - 3,
        celdiriciler=[
            (2 * (18 + 12), "Kapı açıklığını düşmemiş; tel bahçenin tamamını değil, kapı dışındaki kısmı çevreler."),
            (18 + 12 - 3, "Yarı çevreden kapıyı çıkarmış; tel bütün çevre boyunca çekilir."),
            (2 * (18 + 12) + 3, "Kapı açıklığını çıkarmak yerine eklemiş."),
        ],
        explanation="Bahçenin çevresi 2 × (18 + 12) = 60 m'dir. Kapı için 3 m açık bırakıldığından "
                    "60 − 3 = 57 m tel gerekir.",
        difficultyReason="4 adım; ön bilgi: gerçek durumda çevre hesabı ve açıklığın düşülmesi; çeldiriciler yakın (açıklığı atlama ya da ekleme); beceri: model kurma; hesaplama",
        hints=[
            "Önce bahçenin çevresini hesapla.",
            "Telin çevrenin tamamına mı çekileceğine bak.",
            "Kapı açıklığının tele ihtiyaç doğurup doğurmadığını düşün.",
            "Açıklığı çevreden çıkarmayı dene.",
            "Tam çözüm: çevre 2 × 30 = 60 m'dir; kapı için 60 − 3 = 57 m tel gerekir.",
        ],
    ),
    dict(
        level=2,
        question="Kenarları 8 cm ve 6 cm olan bir dikdörtgenin yarı çevresi kaç santimetredir?",
        birim="cm",
        dogru=8 + 6,
        celdiriciler=[
            (2 * (8 + 6), "Çevrenin tamamını hesaplamış; soru yarı çevreyi istiyor."),
            (8 * 6, "Kenarları toplamak yerine çarpmış; çarpım alana aittir."),
            ((8 + 6) // 2, "Yarı çevreyi bir kez daha ikiye bölmüş."),
        ],
        explanation="Yarı çevre bir uzun ve bir kısa kenarın toplamıdır: 8 + 6 = 14 cm.",
        difficultyReason="1 adım; ön bilgi: yarı çevre tanımı; çeldiriciler yakın (çevre, alan ya da fazladan bölme); beceri: kavram uygulama",
        hints=[
            "Yarı çevrenin kaç kenarı kapsadığını söyle.",
            "Komşu iki kenarı seç.",
            "Bu iki kenarı topla.",
            "Sonucu bir daha bölmen gerekip gerekmediğini kontrol et.",
            "Tam çözüm: yarı çevre 8 + 6 = 14 cm'dir.",
        ],
    ),
    dict(
        level=5,
        question="Çevresi 60 cm olan bir dikdörtgenin uzun kenarı kısa kenarının 4 katıdır. Kısa kenar kaç santimetredir?",
        birim="cm",
        dogru=60 // 2 // 5,
        celdiriciler=[
            (4 * (60 // 2 // 5), "Uzun kenarı yazmış; soru kısa kenarı istiyor."),
            (60 // 5, "Pay bölüşümünü çevre üzerinden yapmış; paylar yarı çevreye dağıtılır."),
            (60 // 2 // 4, "Toplam payı 4 saymış; kısa kenarın 1 payı da toplama katılmalıdır."),
        ],
        explanation="Yarı çevre 60 ÷ 2 = 30 cm'dir. Kısa kenara 1 pay dersek uzun kenara 4 pay düşer; "
                    "toplam 5 pay 30 cm eder. Bir pay 30 ÷ 5 = 6 cm olduğundan kısa kenar 6 cm'dir.",
        difficultyReason="5 adım; ön bilgi: yarı çevrenin pay düşünmeyle bölünmesi; çeldiriciler yakın (uzun kenarı ya da yanlış payı yanıt sanma); beceri: model kurma; hesaplama",
        hints=[
            "Önce yarı çevreyi bul.",
            "Kısa kenara 1 pay dersen uzun kenara kaç pay düşeceğini yaz.",
            "Toplam kaç pay olduğunu hesapla.",
            "Yarı çevreyi toplam pay sayısına bölmeyi dene.",
            "Tam çözüm: yarı çevre 22 cm ve toplam 5 paydır; kısa kenar 22 ÷ 5 ile bulunur.",
        ],
    ),
    dict(
        level=3,
        question="Çevresi 30 cm olan bir dikdörtgenin bir kenarı 12 cm'dir. Diğer kenarı kaç santimetredir?",
        birim="cm",
        dogru=30 // 2 - 12,
        celdiriciler=[
            (30 - 12, "Çevreyi 2'ye bölmeden bilinen kenarı çıkarmış."),
            (30 // 2, "Yarı çevreyi bulup orada durmuş."),
            (12 - 30 // 2 + 12, "Çıkarma işlemini ters yönde yapıp sonucu düzeltmeye çalışmış."),
        ],
        explanation="Yarı çevre 30 ÷ 2 = 15 cm'dir; bilinen kenar çıkarılır: 15 − 12 = 3 cm.",
        difficultyReason="2 adım; ön bilgi: yarı çevreden bilinen kenarın çıkarılması; çeldiriciler yakın (bölmeyi atlama); beceri: hesaplama",
        hints=[
            "Çevreyi ikiye bölerek yarı çevreyi bul.",
            "Yarı çevrenin hangi iki kenarı kapsadığını yaz.",
            "Bilinen kenarı işaretle.",
            "Yarı çevreden bilinen kenarı çıkar.",
            "Tam çözüm: 30 ÷ 2 = 15 ve 15 − 12 = 3 cm bulunur.",
        ],
    ),
    dict(
        level=4,
        question="İki dikdörtgenin çevreleri eşittir. Birincinin kenarları 9 cm ve 7 cm, ikincinin bir kenarı 13 cm'dir. İkinci dikdörtgenin diğer kenarı kaç santimetredir?",
        birim="cm",
        dogru=(9 + 7) - 13,
        celdiriciler=[
            (2 * (9 + 7) - 13, "Yarı çevre yerine çevrenin tamamından bilinen kenarı çıkarmış."),
            (9 + 7, "Birinci dikdörtgenin yarı çevresini doğrudan yanıt yazmış."),
            (13 - 9, "Bilinen kenarları birbirinden çıkarmış; iki şekli bağlayan büyüklük çevredir."),
        ],
        explanation="Birinci dikdörtgenin yarı çevresi 9 + 7 = 16 cm'dir. Çevreler eşit olduğuna göre "
                    "ikinci dikdörtgenin de yarı çevresi 16 cm'dir; diğer kenar 16 − 13 = 3 cm bulunur.",
        difficultyReason="4 adım; ön bilgi: iki şeklin yarı çevre üzerinden bağlanması; çeldiriciler yakın (yarı çevre ile çevreyi karıştırma); beceri: model kurma; hesaplama",
        hints=[
            "Birinci dikdörtgenin yarı çevresini hesapla.",
            "Çevreler eşitse yarı çevrelerin de eşit olup olmayacağını düşün.",
            "İkinci dikdörtgenin yarı çevresini yaz.",
            "Bilinen kenarı bu değerden çıkar.",
            "Tam çözüm: yarı çevre 9 + 7 = 16 cm'dir; ikinci dikdörtgende 16 − 13 = 3 cm bulunur.",
        ],
    ),
    dict(
        level=1,
        question="Çevre hangi büyüklüğü ifade eder?",
        choices=[
            "Şeklin kapladığı yüzeyi",
            "Şeklin sınırını oluşturan kenar uzunluklarının toplamını",
            "Şeklin en uzun kenarını",
            "Şeklin köşe sayısını",
        ],
        correct=1,
        distractorWhy=[
            "Kaplanan yüzey alan kavramıdır; alan kare birimlerle, çevre uzunluk birimiyle ölçülür.",
            "doğru",
            "En uzun kenar tek bir uzunluktur; çevre bütün kenarların toplamıdır.",
            "Köşe sayısı bir sayımdır; çevre ise ölçülen bir uzunluktur.",
        ],
        explanation="Çevre, kapalı bir şeklin sınırını oluşturan bütün kenar uzunluklarının toplamıdır "
                    "ve uzunluk birimiyle (cm, m) ölçülür.",
        difficultyReason="1 adım; ön bilgi: çevre tanımı ve alandan ayrılması; çeldiriciler yakın (alan ve kenar kavramlarıyla karıştırma); beceri: kavram bilgisi",
        hints=[
            "Bir şeklin etrafından yürüdüğünü düşün; kat ettiğin yol neye karşılık gelir?",
            "Çevrenin hangi birimle ölçüldüğünü hatırla.",
            "Yüzey ölçüsünün ayrı bir kavram olduğunu göz önüne al.",
            "Sayım ile ölçüm arasındaki farkı düşün.",
            "Tam çözüm: çevre, şeklin sınırındaki bütün kenar uzunluklarının toplamıdır.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# MAT.5.5.2 — note.01, veri yorumlama ve grafik eleştirisi
# ---------------------------------------------------------------------------

A52 = [
    dict(
        level=1,
        question="Bir sütun grafiğinde her birim 2 öğrenciyi göstermektedir. Müzik sütunu 15 birim yüksekliğinde olduğuna göre müziği kaç öğrenci seçmiştir?",
        birim="öğrenci",
        dogru=15 * 2,
        celdiriciler=[
            (15, "Birim sayısını doğrudan öğrenci sayısı sanmış; ölçeği kullanmamış."),
            (15 // 2 + 15 % 2, "Çarpmak yerine bölmüş; her birim birden çok öğrenciyi gösterir."),
            (15 + 2, "Ölçeği çarpan değil eklenecek sayı sanmış."),
        ],
        explanation="Her birim 2 öğrenciyi gösterdiğine göre sütun yüksekliği ölçekle çarpılır: "
                    "15 × 2 = 30 öğrenci.",
        difficultyReason="2 adım; ön bilgi: sütun grafiğinde ölçeğin uygulanması; çeldiriciler yakın (ölçeği atlama ya da ters uygulama); beceri: grafik okuma",
        hints=[
            "Grafikteki bir birimin kaç kişiye karşılık geldiğini yaz.",
            "Sütunun kaç birim yüksekliğinde olduğunu işaretle.",
            "Bu iki sayının hangi işlemle birleşeceğine karar ver.",
            "Sonucun birim sayısından büyük mü küçük mü çıkması gerektiğini düşün.",
            "Tam çözüm: her birim 2 öğrenci olduğundan 15 × 2 = 30 öğrenci bulunur.",
        ],
    ),
    dict(
        level=3,
        question="Bir sütun grafiğinde sıklık ekseni 0'dan değil 40'tan başlatılmıştır. Bu seçim okuyucuyu nasıl yanıltır?",
        choices=[
            "Sütunlar arasındaki farklar olduğundan büyük görünür.",
            "Sütunlar arasındaki farklar olduğundan küçük görünür.",
            "Sütunların sırası değişir.",
            "Kategori adları okunamaz hâle gelir.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Eksenin kesilmesi farkları küçültmez; tam tersine sütunların alt kısmı görünmediği için farklar abartılır.",
            "Eksenin nereden başladığı kategorilerin sırasını etkilemez.",
            "Kategori adları yatay eksende yazılıdır; sıklık ekseninin başlangıcı bu adları etkilemez.",
        ],
        explanation="Sıklık ekseni 0'dan başlamazsa sütunların ortak alt kısmı görünmez. Örneğin 42 ile "
                    "46 sıklıkları, eksen 40'tan başlatıldığında 2 birim ile 6 birim olarak çizilir ve "
                    "aradaki küçük fark üç katmış gibi görünür.",
        difficultyReason="4 adım; ön bilgi: kesilmiş eksenin görsel etkisi; çeldiriciler yakın (etkinin yönünü ters okuma); beceri: eleştirel değerlendirme",
        hints=[
            "Eksen 0'dan başlasaydı sütunların ne kadarının çizileceğini düşün.",
            "Eksen 40'tan başlayınca sütunların hangi kısmının kaybolduğunu belirle.",
            "İki yakın sıklık seçip her iki durumda sütun yüksekliklerini karşılaştır.",
            "Farkların büyüyüp mü küçüldüğüne karar ver.",
            "Tam çözüm: alt kısım kesildiği için 42 ile 46 arasındaki fark 2 birime karşı 6 birim gibi görünür; farklar abartılmış olur.",
        ],
    ),
    dict(
        level=4,
        question="Bir sınıfta 30 öğrenciye en sevdiği spor sorulmuş; futbol 12, basketbol 9, voleybol 5, yüzme 4 yanıtı alınmıştır. “Sınıfın çoğunluğu futbolu seviyor” yorumu için ne söylenebilir?",
        choices=[
            "Doğrudur; futbol en yüksek sıklığa sahiptir.",
            "Yanlıştır; çoğunluk için 15'ten fazla kişi gerekir, futbolu 12 kişi seçmiştir.",
            "Yanlıştır; çoğunluk her zaman en düşük sıklıktır.",
            "Belirlenemez; sıklıklar toplanmadan yorum yapılamaz.",
        ],
        correct=1,
        distractorWhy=[
            "En yüksek sıklığa sahip olmak çoğunluk olmak demek değildir; çoğunluk yarıdan fazlasını gerektirir.",
            "doğru",
            "Çoğunluk en düşük sıklık değildir; yarıdan fazla olma koşuludur.",
            "Sıklıklar soruda verilmiştir ve toplamları 30'dur; yorum için yeterli bilgi vardır.",
        ],
        explanation="Çoğunluk, toplamın yarısından fazlası demektir: 30 ÷ 2 = 15, yani 15'ten fazla "
                    "kişi gerekir. Futbolu 12 kişi seçmiştir; bu sayı en yüksek sıklıktır ama çoğunluk "
                    "değildir.",
        difficultyReason="4 adım; ön bilgi: en yüksek sıklık ile çoğunluğun farkı; çeldiriciler yakın (en yüksek olanı çoğunluk sayma); beceri: akıl yürütme",
        hints=[
            "Çoğunluk sözcüğünün ne anlama geldiğini kendi sözlerinle söyle.",
            "Sınıf mevcudunun yarısını hesapla.",
            "Futbolu seçen sayıyı bu değerle karşılaştır.",
            "En yüksek sıklığa sahip olmakla çoğunluk olmanın aynı şey olup olmadığına karar ver.",
            "Tam çözüm: çoğunluk için 15'ten fazla kişi gerekir; futbolu seçen 12 kişi en yüksek sıklıktır ama çoğunluk değildir.",
        ],
    ),
    dict(
        level=2,
        question="Bir sütun grafiğinde sütunlardan biri diğerlerinden çok daha geniş çizilmiştir. Bu durum neden kusurdur?",
        choices=[
            "Genişlik farkı o kategoriyi olduğundan önemli gösterir; sütunlar aynı genişlikte olmalıdır.",
            "Geniş sütun daha az yer kapladığı için okunması zorlaşır.",
            "Genişlik farkı sıklıkları otomatik olarak değiştirir.",
            "Sütun genişliği kategori sayısını belirler.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Geniş sütun daha çok yer kaplar; kusur yerden değil, dikkati orantısız çekmesinden kaynaklanır.",
            "Genişlik sıklıkları değiştirmez; sıklığı gösteren yüksekliktir. Kusur görsel yanıltmadır.",
            "Kategori sayısı veriden gelir; sütun genişliğiyle belirlenmez.",
        ],
        explanation="Sütun grafiğinde sıklığı gösteren büyüklük yüksekliktir. Bütün sütunlar aynı "
                    "genişlikte olmalıdır; farklı genişlik, o kategoriyi göze daha büyük gösterir ve "
                    "karşılaştırmayı yanıltır.",
        difficultyReason="3 adım; ön bilgi: sütun grafiğinde sıklığı yalnız yüksekliğin taşıması; çeldiriciler yakın (genişliği sıklıkla ilişkilendirme); beceri: eleştirel değerlendirme",
        hints=[
            "Sütun grafiğinde sıklığı hangi büyüklüğün gösterdiğini söyle.",
            "Genişliğin sıklıkla bir ilgisi olup olmadığını düşün.",
            "Geniş bir sütunun göze nasıl göründüğünü canlandır.",
            "Bu görünümün karşılaştırmayı etkileyip etkilemediğine karar ver.",
            "Tam çözüm: sıklığı yükseklik gösterir; farklı genişlik o kategoriyi olduğundan önemli gösterdiği için bütün sütunlar aynı genişlikte olmalıdır.",
        ],
    ),
    dict(
        level=5,
        question="Bir sınıfta yapılan kulüp anketinde spor kulübü birinci çıkmıştır. Aşağıdaki sonuçlardan hangisi bu veriden ÇIKARILAMAZ?",
        choices=[
            "Bu sınıfta spor kulübünü seçen sayı diğer kulüplerden fazladır.",
            "Bu sınıfta spor kulübü en çok tercih edilen kulüptür.",
            "Bu sınıftaki öğrencilerin spor kulübüne yazılma sırası diğerlerinden öncedir.",
            "Bu sınıfta en az bir öğrenci spor kulübünü seçmiştir.",
        ],
        correct=2,
        distractorWhy=[
            "Birinci çıkmak zaten bu demektir; sonuç doğrudan veriden okunur.",
            "Bu ifade birinci çıkmanın başka sözcüklerle söylenmiş hâlidir.",
            "doğru",
            "Birinci çıkan bir kategorinin sıklığı sıfır olamaz; en az bir seçim yapılmıştır.",
        ],
        explanation="Anket yalnız tercihleri ölçer. Yazılma sırası, zamanı ya da nedeni hakkında veri "
                    "toplanmamıştır; bu yüzden sıralamaya dair bir sonuç bu veriden çıkarılamaz.",
        difficultyReason="5 adım; ön bilgi: veriden çıkarılabilecek sonuçların ölçülen değişkenle sınırlı olması; çeldiriciler çok yakın (üçü de doğrudan okunabilen sonuçlar); beceri: akıl yürütme",
        hints=[
            "Ankette hangi sorunun sorulduğunu ve neyin ölçüldüğünü yaz.",
            "Her seçeneğin hangi bilgiyi iddia ettiğini belirle.",
            "Bu bilgilerden hangilerinin doğrudan sıklıklardan okunabildiğine bak.",
            "Ölçülmemiş bir özellik hakkında iddia kuran seçeneği ara.",
            "Tam çözüm: anket yalnız tercihi ölçmüştür; yazılma sırası ölçülmediği için bu sonuç veriden çıkarılamaz.",
        ],
    ),
    dict(
        level=2,
        question="Bir sütun grafiğinde her birim 4 kitabı göstermektedir. Bir sütun 7 birim yüksekliğinde olduğuna göre o kategoride kaç kitap vardır?",
        birim="kitap",
        dogru=7 * 4,
        celdiriciler=[
            (7, "Birim sayısını doğrudan kitap sayısı sanmış; ölçeği uygulamamış."),
            (7 + 4, "Ölçeği çarpan değil eklenecek sayı sanmış."),
            (4, "Ölçeğin kendisini yanıt yazmış."),
        ],
        explanation="Sütun yüksekliği ölçekle çarpılır: 7 × 4 = 28 kitap.",
        difficultyReason="2 adım; ön bilgi: ölçekli sütun grafiğinin okunması; çeldiriciler yakın (ölçeği atlama); beceri: grafik okuma",
        hints=[
            "Bir birimin kaç kitaba karşılık geldiğini yaz.",
            "Sütunun kaç birim olduğunu işaretle.",
            "İki sayıyı hangi işlemle birleştireceğine karar ver.",
            "Sonucun birim sayısından büyük çıkması gerektiğini kontrol et.",
            "Tam çözüm: 7 × 4 = 28 kitap bulunur.",
        ],
    ),
    dict(
        level=3,
        question="İki farklı sınıfta aynı anket yapılmıştır. A sınıfında 30, B sınıfında 20 öğrenci vardır ve iki sınıfta da müziği 10 öğrenci seçmiştir. Bu iki sonuç nasıl karşılaştırılmalıdır?",
        choices=[
            "İki sınıfta müziğe olan ilgi tam olarak aynıdır; sayılar eşittir.",
            "Sayılar eşit olsa da oranlar farklıdır: A sınıfında 10/30, B sınıfında 10/20.",
            "A sınıfında ilgi daha yüksektir; sınıf mevcudu daha büyüktür.",
            "Karşılaştırma yapılamaz; farklı sınıfların verileri birlikte değerlendirilemez.",
        ],
        correct=1,
        distractorWhy=[
            "Sayıların eşit olması ilginin eşit olduğunu göstermez; grup büyüklükleri farklıdır.",
            "doğru",
            "Sınıf mevcudunun büyük olması ilgiyi artırmaz; aynı sayı daha kalabalık bir grupta daha küçük bir orana karşılık gelir.",
            "Farklı büyüklükteki gruplar oran üzerinden karşılaştırılabilir; karşılaştırma mümkündür.",
        ],
        explanation="Grup büyüklükleri farklı olduğunda ham sayılar yanıltıcıdır. A sınıfında oran "
                    "10/30, yani üçte bir; B sınıfında 10/20, yani yarımdır. B sınıfında müziğe ilgi "
                    "oransal olarak daha yüksektir.",
        difficultyReason="4 adım; ön bilgi: farklı büyüklükteki grupların oran üzerinden karşılaştırılması; çeldiriciler yakın (ham sayıyı doğrudan karşılaştırma); beceri: akıl yürütme",
        hints=[
            "İki sınıfın mevcutlarını yan yana yaz.",
            "Müziği seçen sayıların eşit olduğunu fark et.",
            "Aynı sayının farklı büyüklükteki gruplarda ne anlama geldiğini düşün.",
            "Her sınıf için bir oran kurmayı dene.",
            "Tam çözüm: oranlar 10/30 ve 10/20'dir; sayılar eşit olsa da B sınıfındaki oran daha büyüktür.",
        ],
    ),
    dict(
        level=4,
        question="Bir gazete “Öğrencilerin yarısından fazlası spor kulübünü seçti” başlığını atmıştır. Haberin içinde anketin yalnız spor salonunda bulunan öğrencilere yapıldığı yazmaktadır. Bu haberin temel kusuru nedir?",
        choices=[
            "Başlıkta yüzde yerine kesir kullanılmıştır.",
            "Katılımcılar bütün öğrencileri temsil etmemektedir; sonuç yalnız spor salonundaki gruba aittir.",
            "Anket sonuçları grafikle gösterilmemiştir.",
            "Kulüp sayısı haberde belirtilmemiştir.",
        ],
        correct=1,
        distractorWhy=[
            "Kesir ya da yüzde kullanmak bir kusur değildir; ikisi de aynı miktarı gösterebilir.",
            "doğru",
            "Grafik eksikliği sunumla ilgilidir; buradaki kusur sonucun kimler için geçerli olduğuyla ilgilidir.",
            "Kulüp sayısı ek bilgidir; başlığın yanıltıcılığı katılımcı grubundan kaynaklanır.",
        ],
        explanation="Veri yalnız spor salonundaki öğrencilerden toplanmıştır; bu grup zaten spora "
                    "ilgili öğrencilerden oluşur. Sonuç bütün öğrencilere genellenemez; yorum "
                    "araştırmaya katılan grupla sınırlı tutulmalıdır.",
        difficultyReason="4 adım; ön bilgi: katılımcı grubunun sonucu sınırlaması; çeldiriciler yakın (kusuru sunumda arama); beceri: eleştirel değerlendirme",
        hints=[
            "Başlığın kimler hakkında bir iddia kurduğunu belirle.",
            "Verinin gerçekte kimlerden toplandığını yaz.",
            "İki grubu karşılaştır: biri diğerini kapsıyor mu?",
            "Toplanma yerinin sonucu etkileyip etkilemediğini düşün.",
            "Tam çözüm: veri yalnız spor salonundaki öğrencilerden toplanmıştır; bu grup bütün öğrencileri temsil etmediği için başlık yanıltıcıdır.",
        ],
    ),
    dict(
        level=1,
        question="Sütun grafiğinde bir kategorinin sıklığı neyle gösterilir?",
        choices=[
            "Sütunun rengiyle",
            "Sütunun yüksekliğiyle",
            "Sütunun genişliğiyle",
            "Sütunun eksendeki sırasıyla",
        ],
        correct=1,
        distractorWhy=[
            "Renk yalnız kategorileri ayırt etmeye yarar; bir sayı taşımaz.",
            "doğru",
            "Genişlik bütün sütunlarda aynı olmalıdır; sıklığı taşımaz.",
            "Sıra kategorilerin diziliş düzenidir; sıklıkla ilgisi yoktur.",
        ],
        explanation="Sütun grafiğinde sıklığı yükseklik gösterir. Genişlik bütün sütunlarda eşit "
                    "tutulur; renk ve sıra ise sayısal bir bilgi taşımaz.",
        difficultyReason="1 adım; ön bilgi: sütun grafiğinde sıklığı yalnız yüksekliğin taşıması; çeldiriciler yakın (grafiğin diğer görsel özellikleri); beceri: temsil okuma",
        hints=[
            "Sütun grafiğinde hangi özelliğin sayıya bağlı olarak değiştiğini düşün.",
            "İki kategori aynı sıklığa sahipse sütunlarının neyi aynı olur?",
            "Renk değiştirmenin sıklığı değiştirip değiştirmediğini sorgula.",
            "Genişliğin bütün sütunlarda neden eşit tutulduğunu hatırla.",
            "Tam çözüm: sıklığı sütunun yüksekliği gösterir; renk, genişlik ve sıra sayısal bilgi taşımaz.",
        ],
    ),
    dict(
        level=3,
        question="Bir sütun grafiğinde başlık yazılmamıştır. Bu eksiklik neye yol açar?",
        choices=[
            "Sütunların yükseklikleri okunamaz.",
            "Verinin hangi araştırmaya ait olduğu anlaşılmaz.",
            "Kategoriler arasındaki sıralama bozulur.",
            "Sıklıkların toplamı değişir.",
        ],
        correct=1,
        distractorWhy=[
            "Yükseklikler sıklık ekseninden okunmaya devam eder; başlık bu okumayı engellemez.",
            "doğru",
            "Sıralama kategorilerin dizilişiyle ilgilidir; başlıkla değişmez.",
            "Başlık sayıları etkilemez; sıklıklar veriden gelir.",
        ],
        explanation="Başlık, grafiğin hangi araştırma sorusuna ait olduğunu ve verinin kimlerden "
                    "toplandığını bildirir. Başlıksız bir grafikte sayılar okunabilir ama neyi "
                    "anlattıkları belirsiz kalır.",
        difficultyReason="2 adım; ön bilgi: grafik başlığının görevi; çeldiriciler yakın (eksikliği okunabilirlikle karıştırma); beceri: temsil okuma",
        hints=[
            "Başlığın grafikte hangi bilgiyi taşıdığını söyle.",
            "Başlık olmadan sütun yüksekliklerinin okunup okunamayacağını düşün.",
            "Sayılar okunabiliyorsa geriye hangi bilginin eksik kaldığını belirle.",
            "Başlığın sayıları değiştirip değiştirmediğini sorgula.",
            "Tam çözüm: sayılar yine okunur ama verinin hangi araştırmaya ait olduğu anlaşılmaz.",
        ],
    ),
    dict(
        level=5,
        question="Bir sınıfta 25 öğrenciye anket yapılmış, sıklıklar 9, 7, 6 ve 3 olarak kaydedilmiştir. Bu tabloya bakan bir öğrenci “Katılımcı sayısı 9'dur” demiştir. Bu yorumun hatası nedir?",
        choices=[
            "En büyük sıklığı katılımcı sayısı sanmıştır; katılımcı sayısı bütün sıklıkların toplamıdır.",
            "En küçük sıklığı katılımcı sayısı sanmıştır; doğrusu 3 olmalıdır.",
            "Katılımcı sayısı kategori sayısına eşittir; doğrusu 4 olmalıdır.",
            "Hata yoktur; en büyük sıklık her zaman katılımcı sayısını verir.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Öğrenci en küçük değil en büyük sıklığı yazmıştır; ayrıca en küçük sıklık da katılımcı sayısını vermez.",
            "Kategori sayısı kaç seçenek sunulduğunu gösterir; katılımcı sayısıyla ilgisi yoktur.",
            "En büyük sıklık yalnız bir kategoriye aittir; bütün katılımcıları kapsamaz.",
        ],
        explanation="Katılımcı sayısı bütün sıklıkların toplamıdır: 9 + 7 + 6 + 3 = 25. Bu sayı "
                    "soruda verilen 25 katılımcıyla tutarlıdır. Öğrenci ise yalnız en büyük sıklığı "
                    "yazmıştır.",
        difficultyReason="4 adım; ön bilgi: katılımcı sayısının sıklıkların toplamına eşit olması; çeldiriciler yakın (başka bir tek sayıyı katılımcı sanma); beceri: hata teşhisi",
        hints=[
            "Tablodaki dört sayıyı topla.",
            "Bulduğun toplamı soruda verilen katılımcı sayısıyla karşılaştır.",
            "Öğrencinin yazdığı sayının tabloda nereye karşılık geldiğini bul.",
            "Tek bir kategorinin sıklığının bütün katılımcıları kapsayıp kapsamadığına karar ver.",
            "Tam çözüm: 9 + 7 + 6 + 3 = 25'tir; öğrenci yalnız en büyük sıklığı katılımcı sayısı sanmıştır.",
        ],
    ),
    dict(
        level=2,
        question="Bir sütun grafiğinde her birim 5 kişiyi göstermektedir. Bir kategoriyi 45 kişi seçtiğine göre o kategorinin sütunu kaç birim yüksekliğinde olmalıdır?",
        birim="birim",
        dogru=45 // 5,
        celdiriciler=[
            (45, "Kişi sayısını doğrudan birim sayısı sanmış; ölçeği uygulamamış."),
            (45 * 5, "Bölme yerine çarpma yapmış; kişi sayısından birime geçerken ölçeğe bölünür."),
            (45 - 5, "Ölçeği çıkarılacak sayı sanmış."),
        ],
        explanation="Kişi sayısından birim sayısına geçilirken ölçeğe bölünür: 45 ÷ 5 = 9 birim.",
        difficultyReason="2 adım; ön bilgi: ölçeğin ters yönde uygulanması; çeldiriciler yakın (işlem yönünü ters çevirme); beceri: grafik kurma",
        hints=[
            "Bir birimin kaç kişiye karşılık geldiğini yaz.",
            "Elinde kişi sayısı mı yoksa birim sayısı mı olduğunu belirle.",
            "Kişi sayısından birime geçerken hangi işlemin gerektiğini düşün.",
            "Sonucun kişi sayısından küçük çıkması gerektiğini kontrol et.",
            "Tam çözüm: 45 ÷ 5 = 9 olduğundan sütun 9 birim yüksekliğinde çizilir.",
        ],
    ),
    dict(
        level=4,
        question="Bir okulda aynı anket iki kez yapılmıştır: eylül ayında ve mayıs ayında. Sonuçlar farklı çıkmıştır. Bu farkın en makul açıklaması hangisidir?",
        choices=[
            "Ölçüm hatası vardır; aynı anket her zaman aynı sonucu vermelidir.",
            "Tercihler zaman içinde değişebilir; iki sonuç iki farklı zamana aittir.",
            "İkinci anket geçersizdir; yalnız ilk sonuç kullanılmalıdır.",
            "Sıklıkların toplamı değiştiği için karşılaştırma yapılamaz.",
        ],
        correct=1,
        distractorWhy=[
            "Aynı anketin farklı zamanlarda farklı sonuç vermesi hata değildir; tercihler sabit değildir.",
            "doğru",
            "Sonradan yapılan anket geçersiz sayılmaz; her ölçüm kendi zamanı için geçerlidir.",
            "Katılımcı sayısı değişmediyse toplam da değişmez; ayrıca toplam değişse bile oranla karşılaştırma yapılabilir.",
        ],
        explanation="Bir anket, yapıldığı andaki durumu ölçer. Aradan geçen zamanda tercihler "
                    "değişebileceği için iki farklı sonuç birbiriyle çelişmez; her biri kendi "
                    "zamanına ait bir ölçümdür.",
        difficultyReason="4 adım; ön bilgi: ölçümün yapıldığı ana ait olması; çeldiriciler yakın (farkı hata sayma); beceri: eleştirel değerlendirme",
        hints=[
            "Bir anketin hangi ana ait bilgi verdiğini düşün.",
            "İki anketin arasında ne kadar zaman geçtiğini fark et.",
            "Tercihlerin bu sürede değişip değişemeyeceğini sorgula.",
            "Farklı sonuçların birbiriyle çelişip çelişmediğine karar ver.",
            "Tam çözüm: her anket yapıldığı andaki durumu ölçer; aradan geçen sürede tercihler değişebileceği için iki sonuç çelişmez.",
        ],
    ),
    dict(
        level=3,
        question="Bir sütun grafiğinde iki kategorinin sütunları eşit yüksekliktedir ama sıklıkları farklıdır. Bunun en olası nedeni nedir?",
        choices=[
            "Ölçek eşit aralıklarla ilerlememektedir.",
            "Kategori adları yanlış yazılmıştır.",
            "Sütunlar farklı renkte çizilmiştir.",
            "Grafiğe başlık konmamıştır.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Kategori adları sütunların yüksekliğini belirlemez; ad yanlış olsa da yükseklik sıklığa bağlıdır.",
            "Renk sayısal bir bilgi taşımaz; yükseklikleri etkilemez.",
            "Başlık grafiğin neyi anlattığını bildirir; sütun yüksekliklerini belirlemez.",
        ],
        explanation="Sütun yüksekliği sıklığa ölçek üzerinden bağlanır. Ölçek eşit aralıklarla "
                    "ilerlemezse farklı sıklıklar aynı yüksekliğe düşebilir; bu yüzden ölçekteki "
                    "aralıklar eşit tutulmalıdır.",
        difficultyReason="3 adım; ön bilgi: yükseklik ile sıklık arasındaki bağın ölçek üzerinden kurulması; çeldiriciler yakın (grafiğin sayısal olmayan öğeleri); beceri: eleştirel değerlendirme",
        hints=[
            "Sütun yüksekliğinin sıklığa nasıl bağlandığını düşün.",
            "Bu bağı kuran öğenin ne olduğunu söyle.",
            "Ölçek aralıkları eşit olmazsa ne olacağını canlandır.",
            "Sayısal bilgi taşımayan öğeleri ele.",
            "Tam çözüm: yükseklik sıklığa ölçek üzerinden bağlanır; ölçek eşit aralıklı değilse farklı sıklıklar aynı yüksekliğe düşebilir.",
        ],
    ),
    dict(
        level=5,
        question="Bir anket sonucunda “katılımcıların %60'ı A seçeneğini seçti” denmektedir. Ankete 5 kişi katılmıştır. Bu sunumun kusuru nedir?",
        choices=[
            "Yüzde hesabı yanlıştır; 5 kişiyle yüzde hesaplanamaz.",
            "Çok küçük bir gruptan elde edilen sonuç yüzdeyle sunularak olduğundan güvenilir gösterilmiştir.",
            "Yüzde yerine kesir kullanılmalıydı; başka bir kusur yoktur.",
            "A seçeneğinin adı belirtilmemiştir.",
        ],
        correct=1,
        distractorWhy=[
            "Yüzde hesabı yapılabilir: 5 kişinin 3'ü %60 eder. Kusur hesapta değil sunumdadır.",
            "doğru",
            "Kesir kullanmak da aynı sayıyı verirdi; asıl sorun grup büyüklüğünün gizlenmesidir.",
            "Seçeneğin adı ek bilgidir; sunumun yanıltıcılığı katılımcı sayısından kaynaklanır.",
        ],
        explanation="5 kişiden 3'ü %60 eder ve hesap doğrudur. Ancak yüzde ifadesi büyük bir grup "
                    "izlenimi verir; tek bir kişinin farklı yanıt vermesi oranı %20 değiştirirdi. "
                    "Küçük gruplarda sonuç, katılımcı sayısıyla birlikte sunulmalıdır.",
        difficultyReason="5 adım; ön bilgi: küçük örneklemde yüzde sunumunun yanıltıcılığı; çeldiriciler yakın (kusuru hesapta ya da biçimde arama); beceri: eleştirel değerlendirme; akıl yürütme",
        hints=[
            "Verilen yüzdenin kaç kişiye karşılık geldiğini hesapla.",
            "Hesabın doğru olup olmadığını kontrol et.",
            "Bir kişinin yanıtı değişseydi yüzdenin ne kadar değişeceğini bul.",
            "Yüzde ifadesinin okuyucuda nasıl bir grup büyüklüğü izlenimi bıraktığını düşün.",
            "Tam çözüm: 5 kişinin 3'ü %60 eder ve hesap doğrudur; ancak tek bir yanıt oranı %20 değiştireceği için sonuç katılımcı sayısıyla birlikte sunulmalıdır.",
        ],
    ),
    dict(
        level=1,
        question="Bir sıklık tablosunda kategorilerin sıklıkları 6, 4, 7 ve 3'tür. Ankete kaç kişi katılmıştır?",
        birim="kişi",
        dogru=6 + 4 + 7 + 3,
        celdiriciler=[
            (7, "En büyük sıklığı katılımcı sayısı sanmış."),
            (4, "Kategori sayısını katılımcı sayısı sanmış."),
            (6 + 4, "Yalnız ilk iki kategoriyi toplamış; kalan iki kategoriyi eklememiş."),
        ],
        explanation="Katılımcı sayısı bütün sıklıkların toplamına eşittir: 6 + 4 + 7 + 3 = 20 kişi.",
        difficultyReason="1 adım; ön bilgi: sıklıklar toplamının katılımcı sayısına eşitliği; çeldiriciler yakın (tek bir sıklığı ya da kategori sayısını yanıt sanma); beceri: tablo okuma",
        hints=[
            "Her kategorinin sıklığının ne anlama geldiğini söyle.",
            "Bir katılımcının kaç kategoriye sayıldığını düşün.",
            "Bütün sıklıkları alt alta yaz.",
            "Bu sayıları toplamayı dene.",
            "Tam çözüm: 6 + 4 + 7 + 3 = 20 olduğundan ankete 20 kişi katılmıştır.",
        ],
    ),
    dict(
        level=3,
        question="Bir sütun grafiğinde sıklık ekseninde yalnız 0, 5, 10, 15 değerleri işaretlidir. Bir sütun 5 ile 10 arasının tam ortasında bitmektedir. Bu sütunun sıklığı yaklaşık kaçtır?",
        birim="",
        dogru=7,
        celdiriciler=[
            (5, "Sütunun altındaki işareti okumuş; sütun o çizginin üzerinde bitiyor."),
            (10, "Sütunun üstündeki işareti okumuş; sütun o çizgiye ulaşmıyor."),
            (15, "En üstteki işareti yazmış; sütun bu değere çok uzaktır."),
        ],
        explanation="İşaretler arasındaki aralık 5 birimdir. Sütun 5 ile 10 arasının ortasında "
                    "bittiğine göre sıklık yaklaşık 5 + 5 ÷ 2, yani 7 ile 8 arasındadır; en yakın "
                    "tam değer 7'dir.",
        difficultyReason="3 adım; ön bilgi: işaretler arası değerin ara değer okumayla tahmin edilmesi; çeldiriciler yakın (komşu işaretleri okuma); beceri: grafik okuma",
        hints=[
            "Eksendeki işaretler arasındaki aralığın kaç birim olduğunu bul.",
            "Sütunun hangi iki işaret arasında bittiğini belirle.",
            "Sütunun bu aralığın neresinde durduğuna bak.",
            "Aralığın yarısını alt işarete eklemeyi dene.",
            "Tam çözüm: aralık 5 birimdir; sütun ortada bittiğine göre sıklık 5 ile 10 arasının ortasındadır ve yaklaşık 7'dir.",
        ],
    ),
    dict(
        level=4,
        question="Bir sınıfta yapılan ankette resim kulübünü 8, müzik kulübünü 8 öğrenci seçmiştir. Grafikte resim sütunu müzik sütunundan yüksek çizilmiştir. Bu grafikle ilgili ne söylenebilir?",
        choices=[
            "Grafik doğrudur; sütunların yüksekliği çizim tercihine bağlıdır.",
            "Grafik yanlıştır; eşit sıklıklar eşit yükseklikte çizilmelidir.",
            "Grafik doğrudur; resim kulübü alfabetik olarak önce geldiği için daha yüksek çizilir.",
            "Grafik yanlıştır; eşit sıklıklar tek bir sütunda birleştirilmelidir.",
        ],
        correct=1,
        distractorWhy=[
            "Yükseklik çizim tercihi değildir; sıklığı temsil eder ve veriye bağlıdır.",
            "doğru",
            "Alfabetik sıra sütunların dizilişini etkileyebilir ama yüksekliğini belirlemez.",
            "Kategoriler ayrı tutulur; eşit sıklıklı olmaları onları birleştirmeyi gerektirmez.",
        ],
        explanation="Sütun yüksekliği sıklığı temsil eder. İki kategorinin sıklığı eşitse sütunları "
                    "da eşit yükseklikte çizilmelidir; aksi hâlde grafik veriyi yanlış gösterir.",
        difficultyReason="3 adım; ön bilgi: yüksekliğin sıklığa bağlı olması; çeldiriciler yakın (yüksekliği çizim tercihi ya da sıralamayla ilişkilendirme); beceri: eleştirel değerlendirme",
        hints=[
            "İki kategorinin sıklıklarını karşılaştır.",
            "Sütun yüksekliğinin neye bağlı olduğunu hatırla.",
            "Sıklıklar eşitse yüksekliklerin nasıl olması gerektiğini söyle.",
            "Çizim tercihinin veriyi değiştirip değiştiremeyeceğine karar ver.",
            "Tam çözüm: iki kategorinin sıklığı 8'er olduğuna göre sütunlar eşit yükseklikte çizilmelidir; grafik yanlıştır.",
        ],
    ),
    dict(
        level=2,
        question="Bir sıklık tablosunda kategoriler ve sıklıklar yazılıdır. Bu tablodan doğrudan okunabilecek bilgi hangisidir?",
        choices=[
            "Her kategoriyi kaç kişinin seçtiği",
            "Katılımcıların bu seçimi neden yaptığı",
            "Katılımcıların yaş ortalaması",
            "Anketin hangi tarihte yapıldığı",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Seçimin nedeni ayrı bir soruyla ölçülür; sıklık tablosu neden bilgisi taşımaz.",
            "Yaş bilgisi toplanmadıysa tabloda bulunmaz; sıklıklar yalnız kategori seçimlerini gösterir.",
            "Tarih tablonun başlığında ya da açıklamasında yer alabilir ama sıklıklardan okunamaz.",
        ],
        explanation="Sıklık tablosu her kategoriye düşen gözlem sayısını gösterir. Neden, yaş ya da "
                    "tarih gibi bilgiler ancak ayrıca toplanmışsa bilinebilir.",
        difficultyReason="2 adım; ön bilgi: tablodan okunabilecek bilginin ölçülen değişkenle sınırlı olması; çeldiriciler yakın (ölçülmemiş bilgiler); beceri: tablo okuma",
        hints=[
            "Sıklık tablosunda hangi iki bilginin sütunlar hâlinde yazıldığını söyle.",
            "Bu sütunlardan doğrudan ne okunabileceğini belirle.",
            "Ölçülmemiş bir özelliğin tabloda bulunup bulunamayacağını düşün.",
            "Ek bilgi gerektiren seçenekleri ele.",
            "Tam çözüm: tablo kategori ve sıklık taşır; doğrudan okunabilecek bilgi her kategoriyi kaç kişinin seçtiğidir.",
        ],
    ),
    dict(
        level=5,
        question="Bir sütun grafiğinde toplam 24 kişilik bir sınıfın verileri gösterilmektedir. Sütunların yükseklikleri 10, 8, 5 ve 4 olarak okunmaktadır. Bu grafikle ilgili hangi sonuca varılır?",
        choices=[
            "Grafik tutarlıdır; sıklıkların toplamı sınıf mevcuduna eşittir.",
            "Grafik tutarsızdır; sıklıkların toplamı 27 olup sınıf mevcudunu aşmaktadır.",
            "Grafik tutarsızdır; sıklıkların toplamı 24'ten küçüktür.",
            "Grafik tutarlıdır; sıklıkların toplamının mevcutla ilgisi yoktur.",
        ],
        correct=1,
        distractorWhy=[
            "Sıklıkların toplamı 27'dir ve 24'e eşit değildir; grafik tutarlı sayılamaz.",
            "doğru",
            "Toplam 27'dir ve 24'ten küçük değil büyüktür.",
            "Her katılımcı bir kez sayıldığı için sıklıkların toplamı katılımcı sayısına eşit olmalıdır.",
        ],
        explanation="Sıklıkların toplamı 10 + 8 + 5 + 4 = 27'dir. Her öğrenci yalnız bir kategori "
                    "seçebildiğine göre toplam 24'ü aşamaz; ya bir okuma hatası vardır ya da bazı "
                    "öğrenciler birden çok kez sayılmıştır.",
        difficultyReason="5 adım; ön bilgi: sıklıklar toplamının katılımcı sayısını aşamaması; çeldiriciler yakın (yönü ters okuma, ilişkiyi yok sayma); beceri: tutarlılık denetimi; akıl yürütme",
        hints=[
            "Grafikten okunan dört sıklığı topla.",
            "Bulduğun toplamı sınıf mevcuduyla karşılaştır.",
            "Bir öğrencinin kaç kategoriye sayılabileceğini düşün.",
            "Toplamın mevcudu aşmasının ne anlama geldiğine karar ver.",
            "Tam çözüm: 10 + 8 + 5 + 4 = 27 > 24'tür; her öğrenci bir kez sayıldığına göre grafik tutarsızdır.",
        ],
    ),
]


A52.append(dict(
    level=3,
    question="Bir sütun grafiğinde en büyük sıklık 48'dir. Her birim 1 kişiyi gösterecek biçimde çizilirse grafik çok uzayacaktır. Bu durumda ne yapılmalıdır?",
    choices=[
        "En büyük sıklık grafikten çıkarılmalıdır.",
        "Sıklıklar yuvarlanarak küçültülmelidir.",
        "Her birim birden çok kişiyi gösterecek bir ölçek seçilmeli ve bu ölçek grafikte belirtilmelidir.",
        "Sütunlar daha dar çizilmelidir.",
    ],
    correct=2,
    distractorWhy=[
        "Bir kategoriyi çıkarmak veriyi eksik gösterir; grafiğin boyu uğruna veri atılamaz.",
        "Yuvarlama sıklıkları değiştirir ve grafik gerçek veriyi göstermez.",
        "doğru",
        "Sütun genişliği grafiğin yüksekliğini değiştirmez; sorun dikey eksenin uzunluğundadır.",
    ],
    explanation="Ölçek, gereken duyarlılığa göre seçilir. Her birim örneğin 5 kişiyi gösterirse "
                "48 sıklığı yaklaşık 10 birimle çizilir ve grafik okunur boyutta kalır. Seçilen "
                "ölçeğin grafikte belirtilmesi zorunludur; belirtilmezse yükseklikler yanlış okunur.",
    difficultyReason="3 adım; ön bilgi: ölçek seçiminin veriyi değiştirmeden gösterimi düzenlemesi; çeldiriciler yakın (veriyi değiştiren çözümler önerme); beceri: grafik kurma",
    hints=[
        "Grafiğin neden uzadığını belirle: sayılar mı büyük, ölçek mi küçük?",
        "Veriyi değiştirmeden gösterimi değiştirmenin bir yolu olup olmadığını düşün.",
        "Bir birimin kaç kişiyi gösterebileceğini sorgula.",
        "Ölçeği değiştirirsen okuyucunun bunu nasıl bileceğini düşün.",
        "Tam çözüm: her birim birden çok kişiyi gösterecek bir ölçek seçilir ve bu ölçek grafikte yazılır; veri değişmeden grafik okunur boyutta kalır.",
    ],
))


def _dondur(secenekler, gerekceler, kaynak, hedef):
    """Şıkları döngüsel kaydırarak doğru cevabı hedef konuma taşır.

    Döndürme choices ve distractorWhy'a AYNI anda uygulanır; ikisini ayrı
    işlemek d133631'deki hatanın ta kendisidir (AUTHORING_RULES.md §1).
    """
    kaydir = (kaynak - hedef) % len(secenekler)
    yeni_s = secenekler[kaydir:] + secenekler[:kaydir]
    yeni_g = gerekceler[kaydir:] + gerekceler[:kaydir]
    assert yeni_s[hedef] == secenekler[kaynak]
    assert yeni_g[hedef] == gerekceler[kaynak] == "doğru"
    return yeni_s, yeni_g


def _cozumle(s):
    if "choices" in s:
        return list(s["choices"]), int(s["correct"]), list(s["distractorWhy"])
    degerler = [s["dogru"]] + [d for d, _ in s["celdiriciler"]]
    assert len(set(degerler)) == 4, f"{s['question']}: şık değerleri benzersiz değil: {degerler}"
    assert all(v >= 0 for v in degerler), f"{s['question']}: negatif şık: {degerler}"
    birim = s.get("birim", "")
    ek = f" {birim}" if birim else ""
    return [str(v) + ek for v in degerler], 0, ["doğru"] + [g for _, g in s["celdiriciler"]]


AILELER = [
    ("tr.g05.mat.5-4-1", "MAT.5.4.1", "tr.g05.mat.5.4.note.01",
     "Çevre ve dikdörtgenin kenarları", A41),
    ("tr.g05.mat.5-5-2", "MAT.5.5.2", "tr.g05.mat.5.5.note.01",
     "Veriyi yorumlama ve grafik eleştirisi", A52),
]


def uret():
    kayitlar = []
    for onek, kazanim, note_id, topic, sorular in AILELER:
        for i, s in enumerate(sorular, start=1):
            secenekler, kaynak, gerekceler = _cozumle(s)
            hedef = (i - 1) % 4
            secenekler, gerekceler = _dondur(secenekler, gerekceler, kaynak, hedef)
            kayitlar.append({
                "type": "question",
                "id": f"{onek}.q{i:03d}",
                "subject": "Matematik",
                "topic": topic,
                "noteId": note_id,
                "objective": kazanim,
                "objectiveSource": KAYNAK,
                "level": s["level"],
                "question": s["question"],
                "choices": secenekler,
                "correct": hedef,
                "distractorWhy": gerekceler,
                "explanation": s["explanation"],
                "difficultyReason": s["difficultyReason"],
                "figure": None,
                "hints": s["hints"],
                "provenance": "machine-generated:claude-opus-5:2026-08:a3-celdirici-yeniden-uretim:human-pending",
                "reviewStatus": "pending",
                "correctIndex": hedef,
            })
    return kayitlar
