# -*- coding: utf-8 -*-
"""A3 parti 3 — MAT.5.1.1 'Çok basamaklı doğal sayılar' ailesinin yeniden üretimi.

Önceki hâl: 25 sorunun 25'i de "### ### ### doğal sayısının doğru okunuşu
hangisidir?" kökünü paylaşıyordu; yalnız sayı değişiyordu. Beş ipucunun beşi
de 25 soruda birebir aynıydı. distractorWhy üç kalıptan ibaretti
("1.000 değerindeki basamak değişikliği…"). Ayrıca noteId üç not arasında
q001→note.01, q002→note.02, q003→note.03 diye mekanik olarak dönüyordu;
soruların hepsi okuma sorusu olduğu için üçte ikisi konusunu anlatmayan bir
nota bağlıydı (SKILL.md: soruyu yalnız konusu gerçekten o notta anlatılan
nota bağla).

Yeni hâl: üç notun üçünü de gerçekten kapsayan 25 soru —
  A (note.01 Bölükler ve basamaklar): basamak değeri, basamak adı, sayı
     değeri farkı, çözümleme, bölük yapısı, bölükten sayıya, kat ilişkisi
  B (note.02 Doğal sayıları okuma): okuma, sıfır bölük kuralı, "bir bin"
     tuzağı, bölük içi sıfırlar
  C (note.03 Okunuştan sayıya geçme): sözden rakama, söylenmeyen bölüğün
     000 ile tamamlanması, yazım hatası teşhisi

Okunuşlar elle yazılmadı: aşağıdaki oku() işleviyle üretildi. Çeldiriciler de
belirtilen basamağı değiştirilmiş sayının AYNI işlevden geçirilmiş okunuşudur;
böylece hem doğru cevap hem çeldirici Türkçe okuma kuralına uygun kalır ve
gerekçe hangi basamağın değiştiğini kesin olarak söyleyebilir.

choices + correct + distractorWhy + hints + explanation tek birimde üretildi
(AUTHORING_RULES.md §1 atomiklik ilkesi).
"""

KAYNAK = "https://tymm.meb.gov.tr/upload/program/2024programmat5678Onayli.pdf"

_BIRLER = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
_ONLAR = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş",
          "seksen", "doksan"]


def oku3(x: int) -> str:
    """Üç basamaklı bir bölüğü okur. 100 → 'yüz' (bir yüz değil)."""
    if x == 0:
        return ""
    parca = []
    yuz, kalan = divmod(x, 100)
    if yuz == 1:
        parca.append("yüz")
    elif yuz > 1:
        parca.append(f"{_BIRLER[yuz]} yüz")
    on, bir = divmod(kalan, 10)
    if on:
        parca.append(_ONLAR[on])
    if bir:
        parca.append(_BIRLER[bir])
    return " ".join(parca)


def oku(n: int) -> str:
    """Doğal sayının Türkçe okunuşu (0 ≤ n < 1 000 000 000).

    Kurallar: tamamı sıfır olan bölük hiç okunmaz; binler bölüğü 1 ise
    'bir bin' değil yalnız 'bin' denir; birler bölüğüne bölük adı eklenmez.
    """
    if n == 0:
        return "sıfır"
    milyon, kalan = divmod(n, 1_000_000)
    bin_, birler = divmod(kalan, 1000)
    parca = []
    if milyon:
        parca.append(f"{oku3(milyon)} milyon")
    if bin_ == 1:
        parca.append("bin")
    elif bin_:
        parca.append(f"{oku3(bin_)} bin")
    if birler:
        parca.append(oku3(birler))
    return " ".join(parca)


def yaz(n: int) -> str:
    """Sayıyı bölüklere ayırarak yazar: 40891723 → '40 891 723'."""
    return f"{n:,}".replace(",", " ")


def degistir(n: int, konum: int, yeni_rakam: int) -> int:
    """n sayısının `konum` basamağındaki rakamı değiştirir."""
    eski = n // 10 ** konum % 10
    return n + (yeni_rakam - eski) * 10 ** konum


# ---------------------------------------------------------------------------
# A grubu — note.01 "Bölükler ve basamaklar"
# ---------------------------------------------------------------------------

A = [
    dict(
        level=1,
        question="48 273 561 sayısında 7 rakamının basamak değeri kaçtır?",
        choices=["70 000", "7 000", "700 000", "7"],
        correct=0,
        distractorWhy=[
            "doğru",
            "7 rakamını bir sağdaki binler basamağında sanmış.",
            "7 rakamını bir soldaki yüz binler basamağında sanmış.",
            "Rakamın kendi değerini yazmış; basamak değeri bulunduğu yere göre değişir.",
        ],
        explanation="48 273 561 sayısında 7 rakamı on binler basamağındadır. "
                    "Basamak değeri 7 × 10 000 = 70 000'dir.",
        difficultyReason="2 adım; ön bilgi: basamak adları ve basamak değerinin tanımı; çeldiriciler yakın (komşu basamaklar); beceri: basamak çözümleme",
        hints=[
            "Sayıyı sağdan başlayarak üçerli bölüklere ayır.",
            "Aranan rakamın sağdan kaçıncı basamakta olduğunu say.",
            "O basamağın adını belirle: birler, onlar, yüzler, binler…",
            "Rakamı, basamağın değeriyle çarpmayı dene.",
            "Tam çözüm: 7 rakamı sağdan beşinci, yani on binler basamağındadır; 7 × 10 000 = 70 000 eder.",
        ],
    ),
    dict(
        level=1,
        question="215 806 934 sayısında 8 rakamı hangi basamaktadır?",
        choices=["yüz binler", "on binler", "yüzler", "binler"],
        correct=0,
        distractorWhy=[
            "doğru",
            "Sağdan sayarken bir basamak eksik saymış.",
            "Rakamın bulunduğu bölüğü değil, bölük içindeki sırasını basamak adı sanmış.",
            "8 rakamını binler bölüğünün en sağındaki basamakta sanmış.",
        ],
        explanation="215 806 934 sayısı 215 | 806 | 934 biçiminde bölüklere ayrılır. "
                    "8 rakamı binler bölüğünün en solundadır ve bu basamağın adı yüz binlerdir.",
        difficultyReason="2 adım; ön bilgi: bölük yapısı ve basamak adlarının sırası; çeldiriciler yakın (aynı bölüğün diğer basamakları); beceri: basamak adlandırma",
        hints=[
            "Sayıyı sağdan üçerli gruplara ayırıp bölük sınırlarını çiz.",
            "Aranan rakamın hangi bölükte kaldığını belirle.",
            "Her bölüğün kendi içinde birler, onlar, yüzler basamaklarını taşıdığını hatırla.",
            "Bölük adı ile bölük içindeki basamağı birleştirmeyi dene.",
            "Tam çözüm: 8 rakamı binler bölüğünün yüzler basamağındadır; bu basamağın adı yüz binlerdir.",
        ],
    ),
    dict(
        level=2,
        question="94 620 sayısında 6 rakamının basamak değeri ile sayı değeri arasındaki fark kaçtır?",
        choices=["600", "594", "606", "6"],
        correct=1,
        distractorWhy=[
            "Yalnız basamak değerini yazmış; çıkarma işlemini yapmamış.",
            "doğru",
            "Fark yerine iki değeri toplamış: 600 + 6 = 606.",
            "Yalnız sayı değerini yazmış; basamak değerini hesaba katmamış.",
        ],
        explanation="6 rakamı yüzler basamağındadır: basamak değeri 600, sayı değeri 6'dır. "
                    "Fark 600 − 6 = 594 olur.",
        difficultyReason="3 adım; ön bilgi: basamak değeri ile sayı değeri ayrımı; çeldiriciler yakın (ara değerleri yanıt sanma); beceri: hesaplama",
        hints=[
            "Sayı değeri ile basamak değerinin farklı şeyler olduğunu hatırla.",
            "6 rakamının hangi basamakta olduğunu belirle.",
            "Bu basamağa göre 6'nın basamak değerini yaz.",
            "İki değeri alt alta yazıp büyükten küçüğü çıkarmayı dene.",
            "Tam çözüm: basamak değeri 600, sayı değeri 6'dır; 600 − 6 = 594.",
        ],
    ),
    dict(
        level=3,
        question="70 508 sayısının çözümlenmiş biçimi hangisidir?",
        choices=[
            "7 × 10 000 + 5 × 100 + 8 × 1",
            "7 × 1 000 + 5 × 100 + 8 × 1",
            "7 × 10 000 + 5 × 1 000 + 8 × 1",
            "7 × 10 000 + 5 × 100 + 8 × 10",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "7 rakamını on binler yerine binler basamağında saymış.",
            "5 rakamını yüzler yerine binler basamağında saymış.",
            "8 rakamını birler yerine onlar basamağında saymış.",
        ],
        explanation="Çözümleme, sayıyı sıfır olmayan basamak değerlerinin toplamı biçiminde yazmaktır. "
                    "70 508 sayısında 7 on binler, 5 yüzler, 8 birler basamağındadır: "
                    "7 × 10 000 + 5 × 100 + 8 × 1.",
        difficultyReason="3 adım; ön bilgi: çözümlemenin sıfır olmayan basamak değerleri toplamı olduğu; çeldiriciler yakın (tek basamak kaydırma); beceri: basamak çözümleme",
        hints=[
            "Çözümlemenin hangi toplamı gösterdiğini hatırla.",
            "Sayıdaki sıfır olan basamakları işaretle; bunlar toplama yazılmaz.",
            "Sıfır olmayan her rakamın basamak adını tek tek belirle.",
            "Her rakamı kendi basamağının değeriyle çarpmayı dene.",
            "Tam çözüm: 7 on binler, 5 yüzler, 8 birler basamağındadır; çözümleme 7 × 10 000 + 5 × 100 + 8 × 1 biçiminde yazılır.",
        ],
    ),
    dict(
        level=3,
        question="9 000 000 + 40 000 + 300 + 2 toplamı hangi sayıya eşittir?",
        choices=["9 400 302", "9 040 320", "9 043 002", "9 040 302"],
        correct=3,
        distractorWhy=[
            "40 000'i yüz binler basamağına yazmış.",
            "2'yi birler yerine onlar basamağına yazmış.",
            "300'ü yüzler yerine binler basamağına yazmış.",
            "doğru",
        ],
        explanation="Her terim kendi basamağına yerleştirilir: 9 milyonlar, 4 on binler, 3 yüzler, "
                    "2 birler basamağına yazılır. Boş kalan basamaklar sıfırla tamamlanınca 9 040 302 elde edilir.",
        difficultyReason="4 adım; ön bilgi: çözümlemeden sayıya geçiş ve boş basamakların sıfırla tamamlanması; çeldiriciler yakın (tek terim kaydırma); beceri: basamak yerleştirme",
        hints=[
            "Toplamdaki her terimin hangi basamağa ait olduğunu belirle.",
            "Dokuz basamaklık boş bir sıra çizip terimleri yerlerine yaz.",
            "Hiç terim gelmeyen basamakları işaretle.",
            "Bu boş basamakları sıfırla doldurmayı dene.",
            "Tam çözüm: 9 milyonlar, 4 on binler, 3 yüzler, 2 birler basamağına gelir; boşluklar sıfırlanınca sayı 9 040 302 olur.",
        ],
    ),
    dict(
        level=2,
        question="512 073 486 sayısı sağdan üçerli ayrıldığında kaç bölük oluşur ve en soldaki bölüğün adı nedir?",
        choices=[
            "3 bölük; en soldaki binler bölüğüdür",
            "9 bölük; en soldaki milyonlar bölüğüdür",
            "3 bölük; en soldaki milyonlar bölüğüdür",
            "2 bölük; en soldaki milyonlar bölüğüdür",
        ],
        correct=2,
        distractorWhy=[
            "Bölük adlarını sağdan sola sayarken bir sıra eksik ilerlemiş.",
            "Basamak sayısını bölük sayısı sanmış; her bölük üç basamak taşır.",
            "doğru",
            "Birler bölüğünü saymamış; sağdan ilk grup da bir bölüktür.",
        ],
        explanation="512 073 486 sayısı sağdan üçerli ayrılınca 512 | 073 | 486 olur; üç grup oluşur. "
                    "Bölükler sağdan sola birler, binler ve milyonlar diye adlandırıldığından en soldaki "
                    "grup milyonlar bölüğüdür.",
        difficultyReason="3 adım; ön bilgi: bölüğe ayırma ve bölük adlarının sağdan sola sırası; çeldiriciler yakın (basamak ile bölük karıştırma); beceri: bölük çözümleme",
        hints=[
            "Ayırmaya sayının hangi ucundan başlanacağını hatırla.",
            "Üçerli grupları oluşturup kaç grup çıktığını say.",
            "Grupları sağdan sola adlandırmaya başla.",
            "En sağdaki grubun adını söyledikten sonra sola doğru ilerle.",
            "Tam çözüm: 512 | 073 | 486 ayrımı üç grup verir; sağdan sola birler, binler, milyonlar denince en soldaki grup milyonlar bölüğü olur.",
        ],
    ),
    dict(
        level=3,
        question="40 891 723 sayısının binler bölüğündeki üç basamaklı sayı kaçtır?",
        choices=["40", "891", "723", "917"],
        correct=1,
        distractorWhy=[
            "Milyonlar bölüğünü yazmış; bu bölük sayının en solundadır.",
            "doğru",
            "Birler bölüğünü yazmış; bu bölük sayının en sağındadır.",
            "Bölüklere sağdan değil soldan ayırmış: 408 | 917 | 23.",
        ],
        explanation="Bölüklere ayırma sağdan başlar: 40 | 891 | 723. Sağdan ikinci grup binler bölüğü "
                    "olduğuna göre aranan sayı 891'dir.",
        difficultyReason="3 adım; ön bilgi: bölüğe ayırmanın sağdan başladığı; çeldiriciler yakın (komşu bölükler ve soldan ayırma); beceri: bölük okuma",
        hints=[
            "Bölüklere ayırırken hangi uçtan başlandığını hatırla.",
            "Sayıyı üçerli gruplara ayırıp aralarına boşluk koy.",
            "Grupları sağdan sola adlandır.",
            "Binler adını verdiğin grubu işaretle.",
            "Tam çözüm: sağdan ayırma 40 | 891 | 723 verir; sağdan ikinci grup binler bölüğüdür ve 891'dir.",
        ],
    ),
    dict(
        level=4,
        question="Bir doğal sayının milyonlar bölüğü 27, binler bölüğü 400, birler bölüğü 65'tir. Bu sayı kaçtır?",
        choices=["274 065", "27 400 650", "27 465", "27 400 065"],
        correct=3,
        distractorWhy=[
            "Binler bölüğündeki sıfırları yazmayıp bölükleri yan yana getirmiş.",
            "Birler bölüğünü 650 yazmış; 65 sayısı bölüğün sağına yaslanmalıdır.",
            "Bölük değerlerini boş basamakları doldurmadan art arda yazmış.",
            "doğru",
        ],
        explanation="Soldaki ilk bölük olduğu gibi yazılır, sonraki bölükler üç basamağa tamamlanır: "
                    "milyonlar 27, binler 400, birler 065. Sayı 27 400 065 olur.",
        difficultyReason="4 adım; ön bilgi: en soldaki bölük dışındaki bölüklerin üç basamağa tamamlanması; çeldiriciler yakın (sıfır tamamlamayı atlama); beceri: bölükten sayıya geçiş",
        hints=[
            "Sayının kaç bölükten oluşacağını belirle.",
            "En soldaki bölüğün kaç basamaklı olabileceğini düşün.",
            "Diğer bölüklerin kaç basamak tutması gerektiğini hatırla.",
            "Üç basamağa ulaşmayan bölükleri soldan sıfırla tamamlamayı dene.",
            "Tam çözüm: 27 | 400 | 065 dizilişi elde edilir; birler bölüğü 65 olduğu için 065 biçiminde tamamlanır ve sayı 27 400 065 olur.",
        ],
    ),
    dict(
        level=4,
        question="63 000 sayısında 6 rakamının basamak değeri, 3 rakamının basamak değerinin kaç katıdır?",
        choices=["2", "200", "20", "10"],
        correct=2,
        distractorWhy=[
            "Basamak değerleri yerine rakamları bölmüş: 6 ÷ 3 = 2.",
            "Bölme sonucuna fazladan bir sıfır eklemiş.",
            "doğru",
            "İki basamak arasındaki uzaklığa bakıp 10 demiş; oranı hesaplamamış.",
        ],
        explanation="6 rakamı on binler basamağındadır: basamak değeri 60 000. 3 rakamı binler "
                    "basamağındadır: basamak değeri 3 000. Oran 60 000 ÷ 3 000 = 20'dir.",
        difficultyReason="4 adım; ön bilgi: basamak değeri hesabı ve iki değerin oranı; çeldiriciler yakın (rakamların kendi değerini kullanma); beceri: hesaplama; akıl yürütme",
        hints=[
            "'Kaç katıdır' sorusunun hangi işlemi gerektirdiğini belirle.",
            "Her iki rakamın basamak adını ayrı ayrı bul.",
            "İki rakamın basamak değerlerini yaz.",
            "Büyük değeri küçük değere bölmeyi dene.",
            "Tam çözüm: basamak değerleri 60 000 ve 3 000'dir; 60 000 ÷ 3 000 = 20 olduğundan 20 katıdır.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# B grubu — note.02 "Doğal sayıları okuma"
# ---------------------------------------------------------------------------
# okunus(...) tipinde soru: doğru cevap da çeldiriciler de oku() işlevinden
# üretilir. sapma = (basamak konumu, yeni rakam, gerekçe cümlesi)

B_OKUNUS = [
    dict(level=1, sayi=14_552_829,
         sapmalar=[(3, 3, "Binler basamağındaki 2 rakamını 3 sanmış; sayı 14 553 829 olarak okunmuş."),
                   (5, 6, "Yüz binler basamağındaki 5 rakamını 6 sanmış; sayı 14 652 829 olarak okunmuş."),
                   (1, 3, "Onlar basamağındaki 2 rakamını 3 sanmış; sayı 14 552 839 olarak okunmuş.")],
         difficultyReason="2 adım; ön bilgi: bölüğe ayırma ve bölük adlarının söylenme sırası; çeldiriciler çok yakın (tek basamak farkı); beceri: seçenek eleme"),
    dict(level=2, sayi=305_000_476,
         sapmalar=[(3, 1, "Binler bölüğünü boş bırakmayıp 1 yazmış; sayı 305 001 476 olarak okunmuş."),
                   (8, 4, "Yüz milyonlar basamağındaki 3 rakamını 4 sanmış; sayı 405 000 476 olarak okunmuş."),
                   (2, 5, "Yüzler basamağındaki 4 rakamını 5 sanmış; sayı 305 000 576 olarak okunmuş.")],
         difficultyReason="3 adım; ön bilgi: tamamı sıfır olan bölüğün hiç okunmaması; çeldiriciler çok yakın; beceri: kural uygulama; seçenek eleme"),
    dict(level=3, sayi=84_001_250,
         sapmalar=[(3, 2, "Binler bölüğünü 2 sanmış; sayı 84 002 250 olarak okunmuş."),
                   (1, 6, "Onlar basamağındaki 5 rakamını 6 sanmış; sayı 84 001 260 olarak okunmuş."),
                   (6, 5, "Milyonlar basamağındaki 4 rakamını 5 sanmış; sayı 85 001 250 olarak okunmuş.")],
         difficultyReason="3 adım; ön bilgi: binler bölüğü 1 iken 'bir bin' değil 'bin' denmesi; çeldiriciler çok yakın; beceri: kural uygulama"),
    dict(level=2, sayi=720_045_003,
         sapmalar=[(4, 5, "On binler basamağındaki 4 rakamını 5 sanmış; sayı 720 055 003 olarak okunmuş."),
                   (7, 3, "On milyonlar basamağındaki 2 rakamını 3 sanmış; sayı 730 045 003 olarak okunmuş."),
                   (0, 5, "Birler basamağındaki 3 rakamını 5 sanmış; sayı 720 045 005 olarak okunmuş.")],
         difficultyReason="3 adım; ön bilgi: bölük içindeki sıfırların tek tek söylenmemesi; çeldiriciler çok yakın; beceri: seçenek eleme"),
    dict(level=4, sayi=600_000_018,
         sapmalar=[(1, 8, "Onlar basamağındaki 1 rakamını 8 sanmış; sayı 600 000 088 olarak okunmuş."),
                   (8, 5, "Yüz milyonlar basamağındaki 6 rakamını 5 sanmış; sayı 500 000 018 olarak okunmuş."),
                   (3, 2, "Binler bölüğünü boş bırakmayıp 2 yazmış; sayı 600 002 018 olarak okunmuş.")],
         difficultyReason="4 adım; ön bilgi: art arda iki boş bölüğün okunmaması; çeldiriciler çok yakın; beceri: kural uygulama; seçenek eleme"),
    dict(level=5, sayi=9_090_909,
         sapmalar=[(4, 8, "On binler basamağındaki 9 rakamını 8 sanmış; sayı 9 080 909 olarak okunmuş."),
                   (2, 8, "Yüzler basamağındaki 9 rakamını 8 sanmış; sayı 9 090 809 olarak okunmuş."),
                   (6, 8, "Milyonlar basamağındaki 9 rakamını 8 sanmış; sayı 8 090 909 olarak okunmuş.")],
         difficultyReason="4 adım; ön bilgi: sıfırla dolu basamakların atlanarak okunması; çeldiriciler çok yakın (aynı ses örüntüsü); beceri: dikkatli okuma; seçenek eleme"),
]

B_KURAL = [
    dict(
        level=4,
        question="Bir doğal sayının binler bölüğündeki üç rakamın üçü de sıfırsa bu bölük okunurken ne yapılır?",
        choices=[
            "Bölük hiç okunmaz; yazımda üç sıfırla yerini korur.",
            "Bölük 'sıfır bin' diye okunur.",
            "Bölük okunmaz ve yazımdan da çıkarılır.",
            "Bölük yalnız 'bin' diye okunur.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Sıfırlar okunuşta söylenmez; böyle bir bölük adı Türkçe okuma kuralında yoktur.",
            "Bölük yazımdan çıkarılırsa soldaki rakamlar sağa kayar ve sayının değeri değişir.",
            "Bin sözcüğü ancak o bölükte sıfırdan farklı bir değer varken söylenir.",
        ],
        explanation="Tamamı sıfır olan bir bölük okunmaz; ancak yazımda üç sıfırla yerini korumak "
                    "zorundadır. Sıfırlar söylenmediği hâlde diğer rakamların doğru basamakta kalmasını sağlar.",
        difficultyReason="2 adım; ön bilgi: boş bölüğün okunmaması ile yazımda yer tutması arasındaki ayrım; çeldiriciler yakın (okuma ile yazımı karıştırma); beceri: kural ayırt etme",
        hints=[
            "Okuma ile yazmanın iki ayrı işlem olduğunu aklında tut.",
            "Boş bir bölüğün söylenip söylenmediğini hatırla.",
            "O bölüğün sıfırları yazımdan silinirse diğer rakamlara ne olur, dene.",
            "Sayının değerini koruyan yazımın hangisi olduğuna karar ver.",
            "Tam çözüm: boş bölük söylenmez ama yazımda üç sıfırla durur; sıfırlar silinirse soldaki rakamlar sağa kayacağı için sayının değeri bozulur.",
        ],
    ),
    dict(
        level=5,
        question="Aşağıdaki okunuşlardan hangisi Türkçe sayı okuma kuralına aykırıdır?",
        choices=[
            "iki bin yüz elli",
            "bir milyon yüz elli",
            "bir bin yüz elli",
            "yüz bin elli",
        ],
        correct=2,
        distractorWhy=[
            "Binler bölüğü 2 olduğu için sayı bölük adıyla birlikte söylenir; kurala uygundur.",
            "Milyonlar bölüğü 1 iken 'bir milyon' denir; bu bölükte kısaltma yapılmaz.",
            "doğru",
            "Binler bölüğü 100 olduğu için 'yüz bin' denir; kurala uygundur.",
        ],
        explanation="Türkçede binler bölüğü 1 olduğunda 'bir bin' denmez, yalnız 'bin' denir. "
                    "Bu kısaltma yalnız bin sözcüğüne özgüdür; milyon için 'bir milyon' söylenir.",
        difficultyReason="4 adım; ön bilgi: 'bir bin' kısaltmasının yalnız binler bölüğüne özgü olması; çeldiriciler çok yakın (üçü de geçerli okunuş); beceri: kural ayırt etme; akıl yürütme",
        hints=[
            "Bölük adlarının önüne hangi durumlarda sayı söylendiğini hatırla.",
            "Seçenekleri bölük bölük ayırarak hangi bölüğün kaç olduğunu belirle.",
            "Bölüğü 1 olan seçenekleri bir kenara ayır.",
            "Bu seçeneklerden hangisinde kısaltma yapılması gerektiğini düşün.",
            "Tam çözüm: binler bölüğü 1 iken yalnız 'bin' denir. Bu yüzden 'bir bin yüz elli' kurala aykırıdır; doğrusu 'bin yüz elli'dir.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# C grubu — note.03 "Okunuştan sayıya geçme"
# ---------------------------------------------------------------------------

C = [
    dict(
        level=2,
        question="“kırk beş bin yedi” sayısı rakamlarla nasıl yazılır?",
        choices=["45 700", "450 007", "45 007", "4 507"],
        correct=2,
        distractorWhy=[
            "Yedi sayısını birler yerine yüzler basamağına yazmış.",
            "Binler bölüğünü üç basamakla sınırlamayıp fazladan bir sıfır eklemiş.",
            "doğru",
            "Birler bölüğünü üç basamağa tamamlamamış; bölük 007 olmalıdır.",
        ],
        explanation="Bin sözcüğü bölük sınırını gösterir: binler bölüğü 45, birler bölüğü 7'dir. "
                    "Birler bölüğü üç basamağa tamamlanınca 007 olur ve sayı 45 007 diye yazılır.",
        difficultyReason="3 adım; ön bilgi: bin sözcüğünün bölük sınırı olması ve bölüğün üç basamağa tamamlanması; çeldiriciler yakın (sıfır sayısını şaşırma); beceri: sözden sayıya geçiş",
        hints=[
            "Okunuşta bölük sınırını gösteren sözcüğü bul.",
            "Bu sözcüğün önündeki ve arkasındaki bölümleri ayır.",
            "Her bölümün hangi bölüğe ait olduğunu yaz.",
            "En soldaki bölük dışındaki bölükleri üç basamağa tamamlamayı dene.",
            "Tam çözüm: binler bölüğü 45, birler bölüğü 007'dir; yan yana yazılınca sayı 45 007 olur.",
        ],
    ),
    dict(
        level=3,
        question="“üç milyon iki yüz bin altmış” sayısı rakamlarla nasıl yazılır?",
        choices=["3 020 060", "3 200 060", "3 200 600", "3 000 260"],
        correct=1,
        distractorWhy=[
            "İki yüz sayısını binler bölüğünün yüzler basamağı yerine onlar basamağına yazmış.",
            "doğru",
            "Altmış sayısını birler bölüğünün onlar basamağı yerine yüzler basamağına yazmış.",
            "Bin sözcüğünün önündeki iki yüzü binler bölüğüne yazmayıp birler bölüğüne taşımış.",
        ],
        explanation="Milyon ve bin sözcükleri iki bölük sınırı gösterir: milyonlar 3, binler 200, "
                    "birler 060. Bölükler yan yana yazılınca sayı 3 200 060 olur.",
        difficultyReason="4 adım; ön bilgi: iki bölük sınırının aynı anda kullanılması; çeldiriciler yakın (bölük içinde basamak kaydırma); beceri: sözden sayıya geçiş",
        hints=[
            "Okunuşta kaç tane bölük adı geçtiğini say.",
            "Bu adları ayırıcı kabul edip ifadeyi parçalara böl.",
            "Her parçanın hangi bölüğe karşılık geldiğini yaz.",
            "Soldaki ilk bölük dışındaki bölükleri üç basamağa tamamlamayı dene.",
            "Tam çözüm: milyonlar 3, binler 200, birler 060 olur; yan yana yazılınca sayı 3 200 060 elde edilir.",
        ],
    ),
    dict(
        level=3,
        question="“sekiz milyon dokuz” sayısı rakamlarla nasıl yazılır?",
        choices=["8 009 000", "89", "8 000 009", "8 000 900"],
        correct=2,
        distractorWhy=[
            "Dokuz sayısını birler bölüğü yerine binler bölüğüne yazmış.",
            "Milyon sözcüğünü yok sayıp söylenen rakamları yan yana getirmiş.",
            "doğru",
            "Dokuz sayısını birler basamağı yerine yüzler basamağına yazmış.",
        ],
        explanation="Okunuşta bin sözcüğü geçmediğine göre binler bölüğü söylenmemiştir ve 000 yazılır. "
                    "Milyonlar 8, binler 000, birler 009 olur; sayı 8 000 009 biçiminde yazılır.",
        difficultyReason="4 adım; ön bilgi: söylenmeyen bölüğün 000 ile tamamlanması; çeldiriciler yakın (boş bölüğü atlama); beceri: sözden sayıya geçiş; akıl yürütme",
        hints=[
            "Okunuşta hangi bölük adlarının geçtiğini işaretle.",
            "Geçmeyen bir bölük adı olup olmadığını kontrol et.",
            "Söylenmeyen bölüğün yazımda ne olacağını hatırla.",
            "Üç bölüğü soldan sağa sırayla yazmayı dene.",
            "Tam çözüm: bin sözcüğü söylenmediği için binler bölüğü 000'dır; milyonlar 8, birler 009 olunca sayı 8 000 009 olur.",
        ],
    ),
    dict(
        level=4,
        question="“yetmiş milyon beş yüz bin” sayısı rakamlarla nasıl yazılır?",
        choices=["70 500 000", "70 005 000", "7 500 000", "70 500"],
        correct=0,
        distractorWhy=[
            "doğru",
            "Beş yüz yerine yalnız beşi yazmış; binler bölüğü 500 olmalıydı.",
            "Yetmiş sayısını on milyonlar yerine milyonlar basamağına yazmış.",
            "Sonda söylenmeyen birler bölüğünü 000 ile tamamlamamış.",
        ],
        explanation="Milyonlar 70, binler 500'dür. Birler bölüğü söylenmediği için 000 yazılır ve "
                    "sayı 70 500 000 olur.",
        difficultyReason="4 adım; ön bilgi: sonda söylenmeyen birler bölüğünün 000 ile tamamlanması; çeldiriciler yakın (bölük atlama ve basamak kaydırma); beceri: sözden sayıya geçiş",
        hints=[
            "Okunuşun sonunda hangi bölüğün hiç söylenmediğini fark et.",
            "Söylenen iki bölüğü ayrı ayrı yaz.",
            "Söylenmeyen bölüğün kaç basamak tutacağını belirle.",
            "Üç bölüğü soldan sağa yan yana getirmeyi dene.",
            "Tam çözüm: milyonlar 70, binler 500, birler 000'dır; sayı 70 500 000 biçiminde yazılır.",
        ],
    ),
    dict(
        level=4,
        question="“iki yüz bin otuz dört” sayısı rakamlarla nasıl yazılır?",
        choices=["200 340", "2 000 034", "20 034", "200 034"],
        correct=3,
        distractorWhy=[
            "Otuz dört sayısını birler bölüğünün sağına değil soluna yaslamış.",
            "İki yüz bin ifadesini iki milyon gibi okuyup fazladan bir bölük açmış.",
            "Binler bölüğünü üç basamağa tamamlamamış; bölük 200 olmalıdır.",
            "doğru",
        ],
        explanation="Bin sözcüğünün önündeki iki yüz binler bölüğünün değeridir: 200. Birler bölüğü "
                    "34 olduğu için 034 biçiminde tamamlanır ve sayı 200 034 olur.",
        difficultyReason="4 adım; ön bilgi: bölüğün sağa yaslanarak üç basamağa tamamlanması; çeldiriciler yakın (yaslama yönü ve fazla bölük); beceri: sözden sayıya geçiş",
        hints=[
            "Bin sözcüğünün önündeki bölümün hangi bölüğe ait olduğunu belirle.",
            "Bin sözcüğünden sonra söylenen sayıyı ayrı yaz.",
            "İki basamaklı kalan bölüğü üç basamağa tamamlamayı dene.",
            "Tamamlarken sıfırın sağa mı sola mı ekleneceğine karar ver.",
            "Tam çözüm: binler bölüğü 200, birler bölüğü 034'tür; sayı 200 034 olarak yazılır.",
        ],
    ),
    dict(
        level=5,
        question="“altı milyon on beş bin doksan” sayısı rakamlarla nasıl yazılır?",
        choices=["6 150 090", "6 015 090", "6 015 900", "6 015 009"],
        correct=1,
        distractorWhy=[
            "On beş sayısını binler bölüğünün sağına değil soluna yaslamış.",
            "doğru",
            "Doksan sayısını birler bölüğünün onlar basamağı yerine yüzler basamağına yazmış.",
            "Doksan sayısını onlar basamağı yerine birler basamağına yazmış.",
        ],
        explanation="Milyonlar 6, binler 15, birler 90'dır. İki basamaklı bölükler üç basamağa "
                    "tamamlanınca 015 ve 090 olur; sayı 6 015 090 biçiminde yazılır.",
        difficultyReason="5 adım; ön bilgi: iki bölüğün birden sağa yaslanarak tamamlanması; çeldiriciler çok yakın (aynı rakamlar farklı basamaklarda); beceri: sözden sayıya geçiş; dikkatli yazım",
        hints=[
            "Okunuştaki iki bölük adını ayırıcı kabul edip ifadeyi üçe böl.",
            "Her parçanın sayı karşılığını ayrı ayrı yaz.",
            "İki basamakta kalan bölükleri işaretle.",
            "Bu bölükleri üç basamağa tamamlarken sıfırı hangi yana ekleyeceğine karar ver.",
            "Tam çözüm: bölükler 6, 015 ve 090 olur; yan yana yazılınca sayı 6 015 090 elde edilir.",
        ],
    ),
    dict(
        level=3,
        question="“yedi milyon dört yüz” okunuşu rakamlarla yazılırken binler bölüğüne ne yazılır?",
        choices=["400", "000", "7", "Binler bölüğü boş bırakılır"],
        correct=1,
        distractorWhy=[
            "Dört yüz sayısını binler bölüğüne yazmış; bin sözcüğü söylenmediği için bu sayı birler bölüğüne aittir.",
            "doğru",
            "Milyonlar bölüğünün değerini binler bölüğüne taşımış.",
            "Bölüğü boş bırakırsa soldaki rakamlar sağa kayar ve sayının değeri değişir.",
        ],
        explanation="Okunuşta bin sözcüğü geçmediğine göre binler bölüğünün değeri sıfırdır. "
                    "Bu bölük üç sıfırla yazılır ve sayı 7 000 400 olur.",
        difficultyReason="3 adım; ön bilgi: söylenmeyen bölüğün 000 ile yazılması; çeldiriciler yakın (bölüğü boş bırakma ya da komşu bölüğün değerini taşıma); beceri: kural uygulama",
        hints=[
            "Okunuşta hangi bölük adlarının söylendiğini işaretle.",
            "Söylenmeyen bölüğün değerinin kaç olduğunu düşün.",
            "Bu değerin kaç basamakla yazılacağını belirle.",
            "Bölüğü hiç yazmazsan diğer rakamlara ne olacağını dene.",
            "Tam çözüm: bin sözcüğü söylenmediği için binler bölüğü sıfırdır ve 000 biçiminde yazılır; sayı 7 000 400 olur.",
        ],
    ),
    dict(
        level=5,
        question="Bir öğrenci “kırk milyon iki yüz bin beş” sayısını 40 200 500 diye yazmıştır. Öğrencinin hatası nedir?",
        choices=[
            "Milyonlar bölüğünü 40 yerine 4 yazmıştır.",
            "Binler bölüğünü 200 yerine 002 yazmıştır.",
            "Beş sayısını birler basamağı yerine yüzler basamağına yazmıştır.",
            "Bin sözcüğünden sonra fazladan bir bölük açmıştır.",
        ],
        correct=2,
        distractorWhy=[
            "Yazdığı sayının milyonlar bölüğü zaten 40'tır; bu bölükte hata yoktur.",
            "Yazdığı sayının binler bölüğü 200'dür; bu bölük okunuşa uygundur.",
            "doğru",
            "Yazdığı sayı üç bölükten oluşuyor; fazladan bir bölük açılmamıştır.",
        ],
        explanation="Doğru yazım 40 200 005'tir. Öğrenci birler bölüğünü 005 yerine 500 yazarak "
                    "beş sayısını yüzler basamağına koymuştur; bölük sağa yaslanmalıydı.",
        difficultyReason="5 adım; ön bilgi: yazımı yeniden okuyarak denetleme ve bölüğün sağa yaslanması; çeldiriciler yakın (hatasız bölükleri hatalı gösterme); beceri: hata teşhisi; akıl yürütme",
        hints=[
            "Öğrencinin yazdığı sayıyı bölüklere ayırıp yeniden oku.",
            "Kendi okuduğunla soruda verilen okunuşu karşılaştır.",
            "İki okunuşun hangi bölükte ayrıldığını bul.",
            "O bölükteki sayının hangi basamakta durması gerektiğini düşün.",
            "Tam çözüm: 40 200 500 sayısı kırk milyon iki yüz bin beş yüz diye okunur. Birler bölüğü 005 olmalıydı; beş sayısı birler basamağına yazılmadığı için sayı 40 200 005 yerine 40 200 500 çıkmıştır.",
        ],
    ),
]


def _okunus_sorusu(t):
    """Okunuş sorusunu oku() işlevinden üretir; çeldiriciler de aynı işlevden."""
    n = t["sayi"]
    dogru = oku(n)
    secenekler = [dogru]
    gerekceler = ["doğru"]
    for konum, yeni, neden in t["sapmalar"]:
        bozuk = degistir(n, konum, yeni)
        assert bozuk != n, f"{n}: sapma sayıyı değiştirmedi"
        secenekler.append(oku(bozuk))
        gerekceler.append(neden)
    assert len(set(secenekler)) == 4, f"{n}: okunuşlar benzersiz değil"
    return dict(
        level=t["level"],
        question=f"{yaz(n)} doğal sayısının okunuşu hangisidir?",
        choices=secenekler,
        correct=0,
        distractorWhy=gerekceler,
        explanation=f"{yaz(n)} sayısı sağdan üçerli bölüklere ayrılır. Her bölük kendi içinde "
                    f"okunup bölük adı eklenince “{dogru}” elde edilir.",
        difficultyReason=t["difficultyReason"],
        hints=[
            "Sayıyı sağdan başlayarak üçerli bölüklere ayır.",
            "Bölükleri sağdan sola birler, binler, milyonlar diye adlandır.",
            "En soldaki bölükten başlayarak her bölüğü kendi içinde oku.",
            "Seçenekleri bölük bölük karşılaştır; ayrıldıkları basamağı bul.",
            f"Tam çözüm: bölükler sırayla okunup adları eklenince sayının okunuşu “{dogru}” olur.",
        ],
    )


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


def uret():
    ham = []
    for s in A:
        ham.append((s, "tr.g05.mat.5.1.1.note.01", "Bölükler ve basamaklar"))
    for t in B_OKUNUS:
        ham.append((_okunus_sorusu(t), "tr.g05.mat.5.1.1.note.02", "Doğal sayıları okuma"))
    for s in B_KURAL:
        ham.append((s, "tr.g05.mat.5.1.1.note.02", "Doğal sayıları okuma"))
    for s in C:
        ham.append((s, "tr.g05.mat.5.1.1.note.03", "Okunuştan sayıya geçme"))

    kayitlar = []
    for i, (s, note_id, topic) in enumerate(ham, start=1):
        s = dict(s)
        hedef = (i - 1) % 4
        s["choices"], s["distractorWhy"] = _dondur(
            list(s["choices"]), list(s["distractorWhy"]), s["correct"], hedef)
        kayitlar.append({
            "type": "question",
            "id": f"tr.g05.mat.5.1.1.q{i:03d}",
            "subject": "Matematik",
            "topic": topic,
            "noteId": note_id,
            "objective": "MAT.5.1.1",
            "objectiveSource": KAYNAK,
            "level": s["level"],
            "question": s["question"],
            "choices": s["choices"],
            "correct": hedef,
            "distractorWhy": s["distractorWhy"],
            "explanation": s["explanation"],
            "difficultyReason": s["difficultyReason"],
            "figure": None,
            "hints": s["hints"],
            "provenance": "machine-generated:claude-opus-5:2026-08:a3-celdirici-yeniden-uretim:human-pending",
            "reviewStatus": "pending",
            "correctIndex": hedef,
        })
    return kayitlar
