# -*- coding: utf-8 -*-
"""A3 parti 6 — MAT.5.1.2 ve MAT.5.1.3 ailelerinin yeniden üretimi.

Önceki hâl:
  5.1.2 (25 soru): beş kalıp beşer kez tekrarlanıyordu (kitap kampanyası,
    geri dönüşüm hedefi, koli-defter, fidan paylaştırma, kütüphane kutuları).
    Ailenin iki notu var ama noteId aralarında mekanik olarak dönüyordu ve
    note.02'nin konusu (tahmin, yuvarlama, uyumlu sayılar, ters işlemle
    kontrol) 25 sorunun hiçbirinde sorulmuyordu — hepsi düz hesaptı.
  5.1.3 (25 soru): beş kalıp beşer kez tekrarlanıyordu (şişe-ondalık,
    yüz kare-yüzde, parkur-bileşik, kilogram-tam sayılı, anket-üçlü gösterim).
    Notun anlattığı basit/bileşik kesir ayrımı, pay-payda tanımı, paydası
    10 veya 100'e denk hâle getirilebilen kesirler, gösterimler arası
    karşılaştırma ve "dönüşüm miktarı değiştirmez" ilkesi hiç sorulmuyordu.

Sayısal sorularda doğru cevap da çeldiriciler de Python'da hesaplanır;
çeldirici, adlandırılmış yanılgının kendi ifadesinin değeridir.

choices + correct + distractorWhy + hints + explanation tek birimde üretildi
(AUTHORING_RULES.md §1 atomiklik ilkesi).
"""

KAYNAK = "https://tymm.meb.gov.tr/upload/program/2024programmat5678Onayli.pdf"


def T(n: int) -> str:
    """Türkçe binlik ayracıyla yazar: 18067 → '18.067'."""
    return f"{n:,}".replace(",", ".")


# ---------------------------------------------------------------------------
# MAT.5.1.2 — note.01 "Problemi matematiksel işleme dönüştürme" (13 soru)
# ---------------------------------------------------------------------------

A12_NOT1 = [
    dict(
        level=1,
        question="Bir okulun kitap kampanyasında ilk hafta 5.034, ikinci hafta 1.195 kitap toplanmıştır. İki haftada toplam kaç kitap toplanmıştır?",
        birim="kitap",
        dogru=5034 + 1195,
        celdiriciler=[
            (5034 - 1195, "Birleştirme yerine fark almış; iki hafta bir araya geldiği için toplama gerekir."),
            (5034, "Yalnız ilk haftanın sayısını yazmış."),
            (5034 + 1195 - 100, "Toplarken onlar basamağından gelen eldeyi yüzler basamağına eklememiş."),
        ],
        explanation="İki haftanın miktarları bir araya geldiği için toplama yapılır: 5.034 + 1.195 = 6.229.",
        difficultyReason="1 adım; ön bilgi: birleştirme durumunun toplama ile modellenmesi; çeldiriciler yakın (elde hatası); beceri: model kurma",
        hints=[
            "Problemde iki miktarın bir araya mı geldiğini yoksa birinin diğerinden mi çıktığını belirle.",
            "Verilenleri ve istenen miktarı ayrı ayrı yaz.",
            "Duruma uyan işlemi seç.",
            "Toplarken basamakları alt alta hizala ve eldeleri işaretle.",
            "Tam çözüm: iki hafta birleştiği için toplama yapılır; 5.034 + 1.195 = 6.229 kitap bulunur.",
        ],
    ),
    dict(
        level=2,
        question="Bir geri dönüşüm projesinin hedefi 12.357 kapak toplamaktır. Şimdiye kadar 2.073 kapak toplandığına göre hedefe ulaşmak için kaç kapak daha gerekir?",
        birim="kapak",
        dogru=12357 - 2073,
        celdiriciler=[
            (12357 + 2073, "Eksik kalan miktarı bulmak yerine iki sayıyı toplamış."),
            (12357, "Hedefin tamamını yazmış; toplanmış olanları düşmemiş."),
            (2073, "Şimdiye kadar toplananı yazmış; soru kalanı istiyor."),
        ],
        explanation="Hedeften toplanan çıkarılır: 12.357 − 2.073 = 10.284 kapak daha gerekir.",
        difficultyReason="2 adım; ön bilgi: hedefe kalan miktarın çıkarma ile bulunması; çeldiriciler yakın (verilenleri doğrudan yanıt sanma); beceri: model kurma",
        hints=[
            "Hedefin mi yoksa toplananın mı daha büyük olduğunu belirle.",
            "Sorunun hangi miktarı istediğini kendi sözlerinle söyle.",
            "Eksilme durumunun hangi işlemle anlatıldığını hatırla.",
            "Büyük sayıdan küçüğü çıkarmayı dene.",
            "Tam çözüm: 12.357 − 2.073 = 10.284 kapak daha gerekir.",
        ],
    ),
    dict(
        level=2,
        question="Bir yardım merkezine 84 koli gönderilmiştir. Her kolide 117 defter olduğuna göre toplam kaç defter gönderilmiştir?",
        birim="defter",
        dogru=84 * 117,
        celdiriciler=[
            (84 + 117, "Eş büyüklükteki grupların toplamı yerine iki sayıyı toplamış."),
            (84 * 100, "Yalnız 84 × 100 kısmi çarpımını yazmış; 84 × 17 kısmını eklememiş."),
            (84 * 17, "Yalnız 84 × 17 kısmi çarpımını yazmış; 84 × 100 kısmını eklememiş."),
        ],
        explanation="Eş büyüklükte 84 grup vardır ve her grup 117 defter içerir: 84 × 117 = 9.828 defter.",
        difficultyReason="2 adım; ön bilgi: eş grupların toplamının çarpma ile modellenmesi; çeldiriciler yakın (kısmi çarpımda durma); beceri: model kurma; hesaplama",
        hints=[
            "Kaç grup olduğunu ve her grupta kaç nesne bulunduğunu ayrı ayrı yaz.",
            "Grupların hepsi eşit büyüklükte mi, kontrol et.",
            "Eş grupların toplamının hangi işlemle bulunduğunu hatırla.",
            "Çarpmayı kısmi çarpımlara ayırıp hepsini topladığından emin ol.",
            "Tam çözüm: 84 × 117 = 84 × 100 + 84 × 17 = 8.400 + 1.428 = 9.828 defter bulunur.",
        ],
    ),
    dict(
        level=3,
        question="Bir şenlikte 6.720 fidan 40 sınıfa eşit olarak paylaştırılmaktadır. Her sınıfa kaç fidan düşer?",
        birim="fidan",
        dogru=6720 // 40,
        celdiriciler=[
            (6720 - 40, "Eşit paylaştırma yerine çıkarma yapmış."),
            (6720 + 40, "Eşit paylaştırma yerine toplama yapmış."),
            (6720 // 4, "Bölerken 40'ın sonundaki sıfırı hesaba katmamış: 6.720 ÷ 4."),
        ],
        explanation="Bir miktar eşit paylaştırıldığı için bölme yapılır: 6.720 ÷ 40 = 168 fidan.",
        difficultyReason="2 adım; ön bilgi: eşit paylaştırmanın bölme ile modellenmesi; çeldiriciler yakın (bölende sıfırı atlama); beceri: model kurma; hesaplama",
        hints=[
            "Toplam miktarın kaç eşit parçaya ayrıldığını belirle.",
            "Eşit paylaştırmanın hangi işlemle anlatıldığını hatırla.",
            "Bölenin kaç basamaklı olduğuna dikkat et.",
            "Bölme işlemini basamak basamak yap.",
            "Tam çözüm: 6.720 ÷ 40 = 168 olduğundan her sınıfa 168 fidan düşer.",
        ],
    ),
    dict(
        level=3,
        question="Bir depoda 984 kalem vardır. Her kutuya 24 kalem konulacaktır. Kaç kutu doldurulur?",
        birim="kutu",
        dogru=984 // 24,
        celdiriciler=[
            (984 + 24, "Toplam içinde kaç grup bulunduğunu ararken toplama yapmış."),
            (984 - 24, "Yalnız bir kutuluk kalemi çıkarmış; kaç kutu dolduğunu bulmamış."),
            (984 * 24, "Toplam kalem sayısını bir kez daha çarpmış; oysa toplam zaten verilmiştir."),
        ],
        explanation="Bir miktarın içinde kaç eşit grup bulunduğu sorulduğu için bölme yapılır: "
                    "984 ÷ 24 = 41 kutu.",
        difficultyReason="2 adım; ön bilgi: 'içinde kaç grup var' durumunun da bölme ile modellenmesi; çeldiriciler yakın (işlem türünü şaşırma); beceri: model kurma",
        hints=[
            "Toplam miktarın mı yoksa grup sayısının mı verildiğini belirle.",
            "Her grupta kaç nesne olduğunu işaretle.",
            "Toplamın içinde kaç grup bulunduğunu bulmak için hangi işlem gerektiğini düşün.",
            "Bölme işlemini yapıp sonucu kutu sayısı olarak yorumla.",
            "Tam çözüm: 984 ÷ 24 = 41 olduğundan 41 kutu doldurulur.",
        ],
    ),
    dict(
        level=4,
        question="Bir kütüphanede 6.667 kitap vardır. Kütüphaneye, her birinde 152 kitap bulunan 75 kutu daha getirilmektedir. Son durumda kütüphanede toplam kaç kitap olur?",
        birim="kitap",
        dogru=6667 + 75 * 152,
        celdiriciler=[
            (75 * 152, "Başlangıçtaki kitapları eklememiş; yalnız yeni gelenleri yazmış."),
            (6667 + 75, "Her kutudaki kitap sayısını kullanmamış; yalnız kutu sayısını eklemiş."),
            (6667 + 152, "Yalnız bir kutuyu eklemiş; kutu sayısını hesaba katmamış."),
        ],
        explanation="Önce yeni gelen kitaplar bulunur: 75 × 152 = 11.400. Sonra başlangıç miktarına "
                    "eklenir: 6.667 + 11.400 = 18.067 kitap.",
        difficultyReason="3 adım; ön bilgi: çok adımlı problemde bir işlemin sonucunun sonraki adıma girmesi; çeldiriciler yakın (bir adımı atlama); beceri: model kurma; hesaplama",
        hints=[
            "Problemin tek adımda mı yoksa birden çok adımda mı çözüldüğünü belirle.",
            "Önce yeni gelen kitapların sayısını bulmayı dene.",
            "Bu ara sonucu bir kenara yaz.",
            "Ara sonucu başlangıçtaki miktarla birleştir.",
            "Tam çözüm: 75 × 152 = 11.400 bulunur, ardından 6.667 + 11.400 = 18.067 kitap elde edilir.",
        ],
    ),
    dict(
        level=4,
        question="Bir fırında gün başında 3.500 ekmek vardır. Sabah 1.250, öğleden sonra 1.870 ekmek satılmıştır. Akşam kaç ekmek kalmıştır?",
        birim="ekmek",
        dogru=3500 - 1250 - 1870,
        celdiriciler=[
            (1250 + 1870, "Yalnız satılan ekmekleri toplamış; kalanı hesaplamamış."),
            (3500 - 1250, "Yalnız sabah satışını düşmüş; öğleden sonrayı hesaba katmamış."),
            (3500 - 1870, "Yalnız öğleden sonraki satışı düşmüş; sabahı hesaba katmamış."),
        ],
        explanation="Önce satılan toplam bulunur: 1.250 + 1.870 = 3.120. Sonra başlangıçtan düşülür: "
                    "3.500 − 3.120 = 380 ekmek kalır.",
        difficultyReason="3 adım; ön bilgi: iki eksilmenin art arda uygulanması; çeldiriciler yakın (bir eksilmeyi atlama); beceri: model kurma; hesaplama",
        hints=[
            "Kaç kez satış yapıldığını say.",
            "Satışların hepsini bir araya getirmeyi dene.",
            "Bulduğun toplamı başlangıçtaki miktarla karşılaştır.",
            "Eksilme durumunun hangi işlemle anlatıldığını hatırla.",
            "Tam çözüm: 1.250 + 1.870 = 3.120 satılmıştır; 3.500 − 3.120 = 380 ekmek kalır.",
        ],
    ),
    dict(
        level=2,
        question="Bir şehirde bir yılda 34.560 fidan, komşu şehirde 28.905 fidan dikilmiştir. Birinci şehirde kaç fidan fazla dikilmiştir?",
        birim="fidan",
        dogru=34560 - 28905,
        celdiriciler=[
            (34560 + 28905, "Fark yerine iki sayıyı toplamış."),
            (34560 - 28905 - 100, "Çıkarma sırasında yüzler basamağında ödünç almayı atlamış."),
            (34560, "Yalnız birinci şehrin sayısını yazmış; karşılaştırma yapmamış."),
        ],
        explanation="İki miktar arasındaki fark çıkarma ile bulunur: 34.560 − 28.905 = 5.655 fidan.",
        difficultyReason="2 adım; ön bilgi: karşılaştırma farkının çıkarma ile modellenmesi; çeldiriciler yakın (ödünç alma hatası); beceri: model kurma; hesaplama",
        hints=[
            "İki miktarın karşılaştırıldığını fark et.",
            "Hangi sayının daha büyük olduğunu belirle.",
            "Fark sorusunun hangi işlemi gerektirdiğini hatırla.",
            "Çıkarma yaparken ödünç almayı gereken basamaklarda uygula.",
            "Tam çözüm: 34.560 − 28.905 = 5.655 fidan fazla dikilmiştir.",
        ],
    ),
    dict(
        level=4,
        question="Bir gezi için 218 öğrenci taşınacaktır. Her otobüse en çok 40 öğrenci binebildiğine göre en az kaç otobüs gerekir?",
        birim="otobüs",
        dogru=6,
        celdiriciler=[
            (5, "Bölümde durmuş; artan 18 öğrenci için bir otobüs daha gerektiğini hesaba katmamış."),
            (18, "Bölmenin kalanını yanıt olarak yazmış."),
            (7, "Artan öğrenciler için iki otobüs daha saymış; oysa 18 öğrenci tek otobüse sığar."),
        ],
        explanation="218 ÷ 40 işleminde bölüm 5, kalan 18'dir. Artan 18 öğrencinin de taşınması "
                    "gerektiği için bir otobüs daha eklenir: en az 6 otobüs gerekir.",
        difficultyReason="4 adım; ön bilgi: kalanlı bölmenin sonucunun probleme göre yukarı yuvarlanması; çeldiriciler çok yakın (bölümde durma, kalanı yanıt sanma); beceri: sonucu yorumlama",
        hints=[
            "Önce bölme işlemini yapıp bölümü ve kalanı ayrı ayrı yaz.",
            "Kalanın ne anlama geldiğini kendi sözlerinle söyle.",
            "Artan öğrencilerin taşınıp taşınmayacağına karar ver.",
            "Gerekirse bölüme bir ekleyip eklemeyeceğini düşün.",
            "Tam çözüm: 218 ÷ 40 = 5 kalan 18'dir. Artan 18 öğrenci için bir otobüs daha gerektiğinden en az 6 otobüs gerekir.",
        ],
    ),
    dict(
        level=4,
        question="Bir manavda 155 elma vardır. Her poşete 12 elma konularak yalnız tam dolu poşetler hazırlanacaktır. Kaç tam dolu poşet hazırlanır?",
        birim="poşet",
        dogru=155 // 12,
        celdiriciler=[
            (155 // 12 + 1, "Artan 11 elma için bir poşet daha saymış; oysa soru yalnız tam dolu poşetleri istiyor."),
            (155 % 12, "Bölmenin kalanını yanıt olarak yazmış."),
            (155 - 12, "Bölme yerine çıkarma yapmış; yalnız bir poşetlik elmayı düşmüş."),
        ],
        explanation="155 ÷ 12 işleminde bölüm 12, kalan 11'dir. Artan 11 elma bir poşeti tam "
                    "dolduramadığı için 12 tam dolu poşet hazırlanır.",
        difficultyReason="4 adım; ön bilgi: kalanlı bölmede kalanın probleme göre atılması; çeldiriciler çok yakın (yukarı yuvarlama, kalanı yanıt sanma); beceri: sonucu yorumlama",
        hints=[
            "Bölme işlemini yapıp bölümü ve kalanı yaz.",
            "Sorunun tam dolu poşetleri mi yoksa kullanılan bütün poşetleri mi istediğine bak.",
            "Artan elmaların bir poşeti doldurup doldurmadığına karar ver.",
            "Kalanı yanıta katıp katmayacağını belirle.",
            "Tam çözüm: 155 ÷ 12 = 12 kalan 11'dir. Artan 11 elma poşeti dolduramadığından 12 tam dolu poşet hazırlanır.",
        ],
    ),
    dict(
        level=3,
        question="Bir pastaneye gelen 96 pasta 8 rafa eşit olarak yerleştirilmiştir. “Her rafta kaç pasta vardır?” sorusunu çözmek için hangi işlem yapılmalıdır?",
        choices=["96 ÷ 8", "96 × 8", "96 − 8", "96 + 8"],
        correct=0,
        distractorWhy=[
            "doğru",
            "“Her” sözcüğünü görünce çarpmaya yönelmiş; oysa burada verilen toplam eşit paylaştırılıyor.",
            "Problemde eksilme durumu yoktur; raflara yerleştirmek pasta sayısını azaltmaz.",
            "Problemde birleştirme durumu yoktur; toplam pasta sayısı zaten verilmiştir.",
        ],
        explanation="İşlem seçimi tek bir sözcüğe değil, miktarların birbirine nasıl bağlandığına "
                    "dayanır. Burada verilen toplam eşit parçalara ayrıldığı için bölme yapılır: "
                    "96 ÷ 8 = 12 pasta.",
        difficultyReason="3 adım; ön bilgi: işlem seçiminin anahtar sözcüğe değil ilişkiye dayanması; çeldiriciler yakın (sözcükten yola çıkan seçimler); beceri: model kurma",
        hints=[
            "Problemde hangi miktarın verildiğini, hangisinin istendiğini ayır.",
            "Toplam pasta sayısının bilinip bilinmediğine bak.",
            "Toplam biliniyorsa eşit paylaştırmanın hangi işlemle yapıldığını hatırla.",
            "Bir sözcüğe bakarak değil, miktarların ilişkisine bakarak karar ver.",
            "Tam çözüm: toplam verilmiş ve eşit paylaştırılmıştır; bu yüzden 96 ÷ 8 işlemi yapılır.",
        ],
    ),
    dict(
        level=5,
        question="Aşağıdaki iki problemde de “toplam” sözcüğü geçmektedir. I. 4 kutuda toplam 48 kalem vardır; bir kutuda kaç kalem vardır? II. Bir kutuda 12 kalem vardır; 4 kutuda toplam kaç kalem vardır? Bu iki problem sırasıyla hangi işlemlerle çözülür?",
        choices=[
            "I için bölme, II için çarpma",
            "İkisi için de çarpma",
            "İkisi için de bölme",
            "I için çarpma, II için bölme",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "I. problemde toplam zaten verilmiştir; verilen toplamı bir kez daha çarpmak anlamsız olur.",
            "II. problemde toplam verilmemiş, bulunması istenmiştir; bölme yapılacak bir toplam yoktur.",
            "İşlemler ters eşleştirilmiş: toplamın verildiği problemde bölme, arandığı problemde çarpma gerekir.",
        ],
        explanation="Aynı sözcük farklı ilişkilerde kullanılabilir. I. problemde toplam verilmiş ve eşit "
                    "paylaştırma istenmiştir: 48 ÷ 4 = 12. II. problemde eş grupların toplamı aranmıştır: "
                    "12 × 4 = 48. İşlem seçimi sözcüğe değil ilişkiye dayanır.",
        difficultyReason="5 adım; ön bilgi: aynı anahtar sözcüğün farklı ilişkilerde farklı işlem gerektirmesi; çeldiriciler çok yakın (iki problemi aynı sayma); beceri: model kurma; akıl yürütme",
        hints=[
            "İki problemi ayrı ayrı oku ve her birinde neyin verildiğini yaz.",
            "Hangi problemde toplamın verildiğini, hangisinde arandığını işaretle.",
            "Toplamın verildiği problemde ne yapılması gerektiğini düşün.",
            "Toplamın arandığı problemde hangi işlemin gerektiğini belirle.",
            "Tam çözüm: I'de toplam verilmiş ve paylaştırılmıştır (48 ÷ 4 = 12); II'de eş grupların toplamı aranmıştır (12 × 4 = 48).",
        ],
    ),
    dict(
        level=1,
        question="“Bir depoda 720 kg un vardı, bunun 285 kg'ı kullanıldı. Kaç kilogram un kalmıştır?” probleminde istenen nedir?",
        choices=[
            "Kalan un miktarı",
            "Depodaki başlangıç un miktarı",
            "Kullanılan un miktarı",
            "Depoya sonradan eklenen un miktarı",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Başlangıç miktarı problemde verilmiştir; verilen bir miktar istenen olamaz.",
            "Kullanılan miktar da problemde verilmiştir; bulunması gereken bu değildir.",
            "Problemde depoya un eklendiğine dair bir bilgi yoktur.",
        ],
        explanation="Verilenler problemde bilinen sayılardır: 720 kg başlangıç ve 285 kg kullanılan. "
                    "İstenen ise bulunması gereken miktardır; burada bu, kalan un miktarıdır.",
        difficultyReason="1 adım; ön bilgi: verilen ile istenen ayrımı; çeldiriciler yakın (verilenleri istenen sanma); beceri: problem çözümleme",
        hints=[
            "Problemdeki sayıları tek tek işaretle.",
            "Bu sayıların soruda mı yoksa metinde mi geçtiğine bak.",
            "Soru cümlesinin hangi miktarı sorduğunu bul.",
            "Metinde zaten yazılı olan miktarların istenen olamayacağını düşün.",
            "Tam çözüm: 720 kg ve 285 kg verilenlerdir; soru cümlesi kalan un miktarını sorduğu için istenen budur.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# MAT.5.1.2 — note.02 "Çözümü tahmin etme ve kontrol etme" (12 soru)
# ---------------------------------------------------------------------------

A12_NOT2 = [
    dict(
        level=2,
        question="4.812 ile 3.196 sayılarının toplamı en yakın bine yuvarlanarak tahmin edilirse hangi sonuç bulunur?",
        birim="",
        dogru=5000 + 3000,
        celdiriciler=[
            (4000 + 3000, "İki sayıyı da aşağı yuvarlamış; 4.812 sayısı 5.000'e daha yakındır."),
            (5000 + 4000, "İki sayıyı da yukarı yuvarlamış; 3.196 sayısı 3.000'e daha yakındır."),
            (4812 + 3196, "Kesin sonucu yazmış; soru tahmini istiyor."),
        ],
        explanation="Her sayı en yakın bine yuvarlanır: 4.812 → 5.000 ve 3.196 → 3.000. "
                    "Tahmin 5.000 + 3.000 = 8.000 olur.",
        difficultyReason="2 adım; ön bilgi: en yakın bine yuvarlamada yüzler basamağına bakılması; çeldiriciler yakın (yuvarlama yönünü şaşırma); beceri: tahmin",
        hints=[
            "Bine yuvarlarken hangi basamağa bakılacağını hatırla.",
            "Her sayıyı ayrı ayrı yuvarla.",
            "Yuvarladığın sayıların hangi bine daha yakın olduğunu kontrol et.",
            "Yuvarlanmış sayıları topla.",
            "Tam çözüm: 4.812 → 5.000, 3.196 → 3.000; tahmin 5.000 + 3.000 = 8.000 olur.",
        ],
    ),
    dict(
        level=2,
        question="587 ile 342 sayılarının toplamı en yakın yüze yuvarlanarak tahmin edilirse hangi sonuç bulunur?",
        birim="",
        dogru=600 + 300,
        celdiriciler=[
            (500 + 300, "İki sayıyı da aşağı yuvarlamış; 587 sayısı 600'e daha yakındır."),
            (600 + 400, "İki sayıyı da yukarı yuvarlamış; 342 sayısı 300'e daha yakındır."),
            (587 + 342, "Kesin sonucu yazmış; soru tahmini istiyor."),
        ],
        explanation="Her sayı en yakın yüze yuvarlanır: 587 → 600 ve 342 → 300. "
                    "Tahmin 600 + 300 = 900 olur.",
        difficultyReason="2 adım; ön bilgi: en yakın yüze yuvarlamada onlar basamağına bakılması; çeldiriciler yakın (yuvarlama yönünü şaşırma); beceri: tahmin",
        hints=[
            "Yüze yuvarlarken hangi basamağa bakılacağını belirle.",
            "587 sayısının hangi yüze daha yakın olduğunu söyle.",
            "342 sayısı için aynı kontrolü yap.",
            "Yuvarlanmış iki sayıyı topla.",
            "Tam çözüm: 587 → 600, 342 → 300; tahmin 600 + 300 = 900 olur.",
        ],
    ),
    dict(
        level=4,
        question="3.187 ÷ 41 bölümünü zihinden tahmin etmek için hangi uyumlu sayı çifti seçilmelidir?",
        choices=["3.200 ÷ 40", "3.000 ÷ 50", "3.187 ÷ 40", "3.200 ÷ 41"],
        correct=0,
        distractorWhy=[
            "doğru",
            "41 sayısı 50'ye değil 40'a yakındır; ayrıca 3.000 ÷ 50 zihinden kolay olsa da gerçek işlemden uzaklaşır.",
            "Yalnız böleni yuvarlamış; bölünen zihinden kolay bir sayı olmadığı için tahmin kolaylaşmaz.",
            "Yalnız bölüneni yuvarlamış; 41'e bölmek zihinden kolay değildir.",
        ],
        explanation="Uyumlu sayılar, birbirine göre zihinden kolay işlem yapılmasını sağlayan yakın "
                    "sayılardır. 3.187 → 3.200 ve 41 → 40 seçilirse 3.200 ÷ 40 = 80 zihinden bulunur.",
        difficultyReason="4 adım; ön bilgi: uyumlu sayıların birbirine göre seçilmesi; çeldiriciler yakın (yalnız bir sayıyı yuvarlama); beceri: tahmin stratejisi",
        hints=[
            "Uyumlu sayıların ne demek olduğunu hatırla: birbirine göre kolay işlem verirler.",
            "Böleni en yakın onluğa yuvarlamayı dene.",
            "Bölüneni, bu yeni bölene tam bölünecek yakın bir sayıya yuvarla.",
            "Seçtiğin çiftin zihinden gerçekten kolay olup olmadığını sına.",
            "Tam çözüm: 3.187 → 3.200 ve 41 → 40 seçilir; 3.200 ÷ 40 = 80 zihinden bulunur.",
        ],
    ),
    dict(
        level=3,
        question="Bir öğrenci 39 × 21 çarpımını 819 bulmuştur. Tahminle kontrol edildiğinde ne söylenebilir?",
        choices=[
            "Tahmin 800 civarındadır; 819 sonucu makuldür.",
            "Tahmin 600 civarındadır; bulunan sonuç çok büyüktür.",
            "Tahmin 800 civarındadır ama tahmin ile kesin sonuç eşit olmadığı için işlem yanlıştır.",
            "Çarpma işlemlerinde tahmin kullanılamaz; kontrol yapılamaz.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "40 × 20 = 800 olduğundan tahmin 600 değildir; bulunan sonuç tahminle uyumludur.",
            "Tahmin ile kesin sonucun eşit olması gerekmez; önemli olan aralarında açıklanamayacak kadar büyük fark bulunmamasıdır.",
            "Tahmin çarpma işlemlerinde de kullanılır; yuvarlanmış çarpanlarla yaklaşık sonuç bulunabilir.",
        ],
        explanation="Çarpanlar en yakın onluğa yuvarlanır: 39 → 40 ve 21 → 20. Tahmin 40 × 20 = 800'dür. "
                    "Bulunan 819 sonucu bu tahmine yakın olduğu için makuldür.",
        difficultyReason="3 adım; ön bilgi: tahminin amacının kesin sonucu vermek değil makullüğü sınamak olması; çeldiriciler yakın (tahminden eşitlik bekleme); beceri: kontrol etme",
        hints=[
            "Çarpanları en yakın onluğa yuvarla.",
            "Yuvarlanmış çarpanlarla tahmini hesapla.",
            "Tahmin ile öğrencinin bulduğu sonucu karşılaştır.",
            "Aradaki farkın açıklanabilir büyüklükte olup olmadığına karar ver.",
            "Tam çözüm: 40 × 20 = 800 tahmini bulunur; 819 sonucu bu tahmine yakın olduğundan makuldür.",
        ],
    ),
    dict(
        level=3,
        question="Bir öğrenci 936 ÷ 12 = 78 sonucunu bulmuştur. Bu sonucu kontrol etmenin en doğrudan yolu nedir?",
        choices=[
            "78 × 12 çarpımının 936 verip vermediğine bakmak",
            "936 + 12 toplamının 78'e yakın olup olmadığına bakmak",
            "Aynı bölme işlemini bir kez daha aynı yolla yapmak",
            "78 sayısının 936'dan küçük olduğunu görmek",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Toplama, bölmenin ters işlemi değildir; bu karşılaştırma sonucun doğruluğu hakkında bilgi vermez.",
            "Aynı yol tekrarlandığında aynı hata da tekrarlanır; bu yöntem yanlışı ortaya çıkarmaz.",
            "Bölümün bölünenden küçük olması beklenen bir durumdur; bu gözlem sonucun doğru olduğunu göstermez.",
        ],
        explanation="Bölmenin ters işlemi çarpmadır. Bölüm ile bölen çarpıldığında bölünen elde "
                    "ediliyorsa sonuç doğrulanmış olur: 78 × 12 = 936.",
        difficultyReason="2 adım; ön bilgi: ters işlemle kontrol; çeldiriciler yakın (kısmi ya da geçersiz kontrol yolları); beceri: kontrol etme",
        hints=[
            "Bölme işleminin ters işleminin ne olduğunu hatırla.",
            "Elindeki bölüm ve böleni yan yana yaz.",
            "Bu iki sayıyı çarptığında hangi sayıyı bulman gerektiğini söyle.",
            "Aynı yolu tekrarlamanın hatayı yakalayıp yakalamayacağını düşün.",
            "Tam çözüm: bölmenin tersi çarpmadır; 78 × 12 = 936 çıkıyorsa sonuç doğrudur.",
        ],
    ),
    dict(
        level=4,
        question="Bir çiftlikte 48 kasa vardır ve her kasada 96 yumurta bulunmaktadır. Toplam yumurta sayısı için en makul tahmin hangisidir?",
        choices=["5.000 civarı", "500 civarı", "50.000 civarı", "150 civarı"],
        correct=0,
        distractorWhy=[
            "doğru",
            "Bir basamak eksik tahmin etmiş; 50 × 100 çarpımı üç basamaklı bir sayı vermez.",
            "Bir basamak fazla tahmin etmiş; 50 × 100 çarpımı beş basamaklı bir sayı vermez.",
            "Çarpma yerine toplama ile tahmin etmiş: 50 + 100.",
        ],
        explanation="Çarpanlar kolay sayılara yuvarlanır: 48 → 50 ve 96 → 100. "
                    "Tahmin 50 × 100 = 5.000 olur.",
        difficultyReason="3 adım; ön bilgi: çarpma tahmininde basamak büyüklüğünün korunması; çeldiriciler yakın (basamak kaydırma); beceri: tahmin",
        hints=[
            "İki çarpanı da zihinden kolay sayılara yuvarla.",
            "Yuvarlanmış sayıları çarp.",
            "Çıkan sonucun kaç basamaklı olduğunu kontrol et.",
            "Tahminin gerçek çarpımın büyüklük sırasına uyup uymadığına bak.",
            "Tam çözüm: 48 → 50 ve 96 → 100 alınır; tahmin 50 × 100 = 5.000 olur.",
        ],
    ),
    dict(
        level=5,
        question="128.640 kişilik bir etkinlikteki katılımcı sayısı için “yaklaşık 129 bin kişi” denmiştir. Bu tahminde sayı hangi basamağa yuvarlanmıştır?",
        choices=["en yakın bine", "en yakın yüze", "en yakın on bine", "en yakın yüz bine"],
        correct=0,
        distractorWhy=[
            "doğru",
            "En yakın yüze yuvarlansaydı 128.600 elde edilirdi; bu sayı “129 bin” diye ifade edilmez.",
            "En yakın on bine yuvarlansaydı 130.000 elde edilirdi.",
            "En yakın yüz bine yuvarlansaydı 100.000 elde edilirdi.",
        ],
        explanation="128.640 sayısı en yakın bine yuvarlanınca 129.000 olur; bu da “yaklaşık 129 bin” "
                    "biçiminde ifade edilir. Yuvarlanacak basamak, gereken duyarlılığa göre seçilir.",
        difficultyReason="4 adım; ön bilgi: yuvarlanan basamağın sonuçtan geri okunması; çeldiriciler yakın (her biri başka bir basamağa yuvarlama); beceri: tahmin; akıl yürütme",
        hints=[
            "Sayıyı her seçenekteki basamağa ayrı ayrı yuvarla.",
            "Her yuvarlamanın sonucunu yaz.",
            "Bu sonuçları soruda verilen ifadeyle karşılaştır.",
            "Hangi yuvarlamanın verilen ifadeyi tam karşıladığına karar ver.",
            "Tam çözüm: 128.640 en yakın bine yuvarlanınca 129.000 olur ve bu “yaklaşık 129 bin” diye ifade edilir.",
        ],
    ),
    dict(
        level=4,
        question="Bir öğrenci 6.120 ÷ 6 işleminin sonucunu 102 bulmuştur. Tahmin bu sonuç hakkında ne söyler?",
        choices=[
            "Tahmin 1.000 civarıdır; 102 sonucu çok küçüktür, işlemde basamak hatası vardır.",
            "Tahmin 100 civarıdır; bulunan sonuç makuldür.",
            "Tahmin 600 civarıdır; bulunan sonuç biraz küçüktür.",
            "Bölme işleminde tahmin kullanılamaz; sonuç hakkında bir şey söylenemez.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "6.000 ÷ 6 = 1.000 olduğundan tahmin 100 değildir; bulunan sonuç tahminin onda biri kadardır.",
            "6.000 ÷ 6 işlemi 600 vermez; bölen 6 olduğu için sonuç dört basamaklıdır.",
            "Bölme işleminde de yuvarlanmış sayılarla tahmin yapılabilir; nitekim bu tahmin hatayı ortaya çıkarır.",
        ],
        explanation="Bölünen kolay bir sayıya yuvarlanır: 6.120 → 6.000. Tahmin 6.000 ÷ 6 = 1.000'dir. "
                    "Bulunan 102 sonucu bu tahminden on kat küçüktür; aradaki fark açıklanamayacak kadar "
                    "büyük olduğu için işlem yeniden yapılmalıdır. Doğru sonuç 1.020'dir.",
        difficultyReason="4 adım; ön bilgi: tahmin ile kesin sonuç arasındaki büyük farkın hata işareti olması; çeldiriciler yakın (tahmini yanlış hesaplama); beceri: kontrol etme; akıl yürütme",
        hints=[
            "Bölüneni zihinden kolay bir sayıya yuvarla.",
            "Yuvarlanmış sayıyla bölmeyi yap ve tahmini yaz.",
            "Tahmin ile öğrencinin bulduğu sonucu karşılaştır.",
            "Aradaki farkın açıklanabilir olup olmadığına karar ver.",
            "Tam çözüm: 6.000 ÷ 6 = 1.000 tahmini bulunur; 102 sonucu bundan on kat küçük olduğu için işlemde basamak hatası vardır ve doğru sonuç 1.020'dir.",
        ],
    ),
    dict(
        level=2,
        question="78 ile 52 sayılarının çarpımı, çarpanlar en yakın onluğa yuvarlanarak tahmin edilirse hangi sonuç bulunur?",
        birim="",
        dogru=80 * 50,
        celdiriciler=[
            (70 * 50, "78 sayısını aşağı yuvarlamış; 78 sayısı 80'e daha yakındır."),
            (78 * 52, "Kesin sonucu yazmış; soru tahmini istiyor."),
            (80 * 60, "52 sayısını yukarı yuvarlamış; 52 sayısı 50'ye daha yakındır."),
        ],
        explanation="Çarpanlar en yakın onluğa yuvarlanır: 78 → 80 ve 52 → 50. "
                    "Tahmin 80 × 50 = 4.000 olur.",
        difficultyReason="2 adım; ön bilgi: onluğa yuvarlamada birler basamağına bakılması; çeldiriciler yakın (yuvarlama yönünü şaşırma); beceri: tahmin",
        hints=[
            "Onluğa yuvarlarken hangi basamağa bakılacağını hatırla.",
            "78 sayısını yuvarla ve hangi onluğa daha yakın olduğunu doğrula.",
            "52 sayısı için aynı kontrolü yap.",
            "Yuvarlanmış çarpanları çarp.",
            "Tam çözüm: 78 → 80 ve 52 → 50; tahmin 80 × 50 = 4.000 olur.",
        ],
    ),
    dict(
        level=3,
        question="Bir problemde 12 kutuda kaç kalem bulunduğu sorulmuş, öğrenci yanıtını “48 kutu” diye yazmıştır. Bu yanıttaki en açık kusur nedir?",
        choices=[
            "İstenen kalem sayısıdır ama yanıt kutu birimiyle yazılmıştır.",
            "Yanıttaki sayı çok küçüktür.",
            "Bölme yerine çarpma yapılmıştır.",
            "Yanıt bir tam sayı olmamalıdır.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Sayının büyüklüğü hakkında karar vermek için kalem sayısı bilinmelidir; verilen bilgide böyle bir dayanak yoktur.",
            "Hangi işlemin yapıldığı yanıttan anlaşılmamaktadır; görünen kusur işlemde değil birimdedir.",
            "Kalem sayısı sayılabilir bir miktardır; tam sayı olması beklenen bir sonuçtur.",
        ],
        explanation="Kontrol yollarından biri de birim incelemesidir. Soru kalem sayısını istediği hâlde "
                    "yanıt kutu birimiyle yazılmıştır; birim uyuşmadığı için yanıt sorulan miktarı "
                    "karşılamamaktadır.",
        difficultyReason="3 adım; ön bilgi: birim incelemesinin bir kontrol yolu olması; çeldiriciler yakın (kusuru sayıda ya da işlemde arama); beceri: kontrol etme",
        hints=[
            "Sorunun hangi birimde bir yanıt beklediğini belirle.",
            "Öğrencinin yazdığı yanıtın birimine bak.",
            "İki birimi karşılaştır.",
            "Birim uyuşmuyorsa yanıtın sorulan miktarı karşılayıp karşılamadığına karar ver.",
            "Tam çözüm: soru kalem sayısını istemektedir ama yanıt kutu birimiyle yazılmıştır; birim uyuşmazlığı en açık kusurdur.",
        ],
    ),
    dict(
        level=1,
        question="Bir işlemi yapmadan önce tahmin etmenin amacı nedir?",
        choices=[
            "Sonucun makul bir aralıkta olup olmadığını görmek",
            "Kesin sonucu hesaplamadan bulmak",
            "İşlemi yapmaktan kurtulmak",
            "Sayıları küçültüp problemi kolaylaştırmak",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Tahmin yaklaşık bir değer verir; kesin sonuç ancak gerçek sayılarla yapılan işlemden çıkar.",
            "Tahmin işlemin yerini almaz; işlemden önce ya da sonra bir denetim aracıdır.",
            "Yuvarlama yalnız tahmin için yapılır; problemin sayıları değişmez ve kesin sonuç yine gerçek sayılarla bulunur.",
        ],
        explanation="Tahminin amacı cevabı rastgele söylemek ya da işlemin yerini almak değildir; "
                    "sonucun makul bir aralıkta olup olmadığını görmektir.",
        difficultyReason="1 adım; ön bilgi: tahminin amacı; çeldiriciler yakın (tahmini kesin sonucun yerine koyma); beceri: kavram bilgisi",
        hints=[
            "Tahminin kesin sonucu verip vermediğini düşün.",
            "Bir tahmin yanlış çıkarsa işlemin yapılmasına gerek kalıp kalmadığını sorgula.",
            "Tahminin işlemden önce mi sonra mı işe yaradığını değerlendir.",
            "Yuvarlamanın problemin sayılarını gerçekten değiştirip değiştirmediğine karar ver.",
            "Tam çözüm: tahmin, kesin sonucun yerini almaz; sonucun makul bir aralıkta olup olmadığını görmeye yarar.",
        ],
    ),
    dict(
        level=5,
        question="3.940 + 2.080 toplamı için iki öğrenci farklı tahmin yapmıştır: A en yakın bine yuvarlayıp 6.000, B en yakın yüze yuvarlayıp 6.000 bulmuştur. Kesin sonuç 6.020'dir. Bu durum için ne söylenebilir?",
        choices=[
            "İki tahmin de kesin sonuca yakındır; yüze yuvarlama genelde daha duyarlıdır ama bu örnekte aynı sonucu vermiştir.",
            "Yalnız A doğru tahmin yapmıştır; bine yuvarlama her zaman daha güvenilirdir.",
            "Tahminler kesin sonuca eşit olmadığı için ikisi de yanlıştır.",
            "Yüze yuvarlama her zaman bine yuvarlamayla aynı sonucu verir.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Bine yuvarlama daha kaba bir tahmin verir; güvenilirliği artıran şey basamağın büyüklüğü değil, gereken duyarlılığa uygun seçilmesidir.",
            "Tahminin kesin sonuca eşit olması beklenmez; önemli olan aralarında açıklanamayacak kadar büyük fark bulunmamasıdır.",
            "İki yuvarlama çoğu sayıda farklı sonuç verir; burada aynı çıkması bu sayılara özgüdür.",
        ],
        explanation="A: 4.000 + 2.000 = 6.000. B: 3.900 + 2.100 = 6.000. İki tahmin de kesin sonuç olan "
                    "6.020'ye yakındır. Yuvarlanacak basamak gereken duyarlılığa göre seçilir; daha küçük "
                    "basamağa yuvarlamak genelde daha duyarlı bir tahmin verir, ancak bu örnekte iki yol "
                    "aynı sonuca çıkmıştır.",
        difficultyReason="5 adım; ön bilgi: yuvarlama basamağının duyarlılıkla ilişkisi ve tahminden eşitlik beklenmemesi; çeldiriciler çok yakın (her biri bir aşırı genelleme); beceri: akıl yürütme; kontrol etme",
        hints=[
            "İki öğrencinin yuvarlamalarını ayrı ayrı yapıp tahminlerini doğrula.",
            "İki tahmini kesin sonuçla karşılaştır.",
            "Bir tahminin kesin sonuca eşit olmasının gerekip gerekmediğini düşün.",
            "İki yuvarlamanın her sayıda aynı sonucu verip vermeyeceğini sorgula.",
            "Tam çözüm: A için 4.000 + 2.000 = 6.000, B için 3.900 + 2.100 = 6.000 bulunur. İkisi de 6.020'ye yakındır; küçük basamağa yuvarlama genelde daha duyarlıdır ama burada iki yol aynı sonucu vermiştir.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# MAT.5.1.3 — note.01 "Kesir, tam sayılı kesir, ondalık ve yüzde" (25 soru)
# ---------------------------------------------------------------------------

A13 = [
    dict(
        level=1,
        question="Bir şişenin 3/10'u su ile doludur. Bu miktarın ondalık gösterimi hangisidir?",
        choices=["0,3", "0,03", "3,0", "0,10"],
        correct=0,
        distractorWhy=[
            "doğru",
            "Paydayı 100 kabul etmiş; onda birler virgülden sonraki ilk basamakta gösterilir.",
            "Payı tam sayı gibi yazmış; oysa kesir bir bütünden küçüktür.",
            "Payı değil paydayı virgülden sonra yazmış.",
        ],
        explanation="Paydası 10 olan kesirde pay, virgülden sonraki ilk basamağa yazılır: 3/10 = 0,3.",
        difficultyReason="1 adım; ön bilgi: onda birler basamağının virgülden sonraki ilk basamak olması; çeldiriciler yakın (basamak kaydırma); beceri: gösterim dönüştürme",
        hints=[
            "Kesrin paydasının kaç olduğuna bak.",
            "Virgülden sonraki ilk basamağın adını hatırla.",
            "Payın hangi basamağa yazılacağına karar ver.",
            "Yazdığın sayının bir bütünden küçük olup olmadığını kontrol et.",
            "Tam çözüm: payda 10 olduğu için pay onda birler basamağına yazılır ve 3/10 = 0,3 elde edilir.",
        ],
    ),
    dict(
        level=2,
        question="Bir ipin 47/100'ü boyanmıştır. Boyalı kısmın ondalık gösterimi hangisidir?",
        choices=["4,7", "0,47", "0,047", "47,0"],
        correct=1,
        distractorWhy=[
            "Virgülü bir basamak sağa kaydırmış; payda 100 iken virgülden sonra iki basamak bulunur.",
            "doğru",
            "Paydayı 1000 kabul etmiş; iki basamak yerine üç basamak yazmış.",
            "Payı tam sayı gibi yazmış; oysa kesir bir bütünden küçüktür.",
        ],
        explanation="Paydası 100 olan kesirde virgülden sonra iki basamak bulunur: 47/100 = 0,47.",
        difficultyReason="2 adım; ön bilgi: yüzde birler basamağının virgülden sonraki ikinci basamak olması; çeldiriciler yakın (virgül kaydırma); beceri: gösterim dönüştürme",
        hints=[
            "Paydanın kaç olduğunu belirle.",
            "Payda 100 iken virgülden sonra kaç basamak bulunacağını hatırla.",
            "Payı bu basamaklara yerleştir.",
            "Sayının bir bütünden küçük olduğunu doğrula.",
            "Tam çözüm: payda 100 olduğundan virgülden sonra iki basamak yazılır ve 47/100 = 0,47 olur.",
        ],
    ),
    dict(
        level=1,
        question="Yüz eş kareye ayrılmış bir kartın 28 karesi boyanmıştır. Boyalı kısmın yüzde gösterimi hangisidir?",
        choices=["%2,8", "%72", "%28", "%0,28"],
        correct=2,
        distractorWhy=[
            "Virgülü bir basamak sola kaydırmış; boyalı kare sayısı doğrudan yüzde değeridir.",
            "Boyalı değil boyasız kısmı hesaplamış: 100 − 28.",
            "doğru",
            "Ondalık gösterimi yüzde işaretiyle birlikte yazmış; iki gösterim bir arada kullanılmaz.",
        ],
        explanation="Yüzde gösterimi bütünü 100 eş parça kabul eder. Kart zaten 100 eş kareye "
                    "ayrıldığından boyalı kare sayısı doğrudan yüzde değeridir: %28.",
        difficultyReason="1 adım; ön bilgi: yüzde gösteriminin bütünü 100 eş parça kabul etmesi; çeldiriciler yakın (tümleyeni alma, virgül kaydırma); beceri: gösterim dönüştürme",
        hints=[
            "Kartın kaç eş parçaya ayrıldığını söyle.",
            "Yüzde gösteriminin bütünü kaç parça kabul ettiğini hatırla.",
            "İki sayının aynı olup olmadığına bak.",
            "Sorunun boyalı mı boyasız kısmı mı istediğini kontrol et.",
            "Tam çözüm: kart 100 eş kareye ayrıldığı için boyalı 28 kare doğrudan %28'e karşılık gelir.",
        ],
    ),
    dict(
        level=2,
        question="%35 hangi kesre eşittir?",
        choices=["35/10", "100/35", "35/100", "3,5/100"],
        correct=2,
        distractorWhy=[
            "Paydayı 10 yazmış; yüzde gösteriminde bütün 100 eş parçadır.",
            "Pay ile paydanın yerini değiştirmiş.",
            "doğru",
            "Payı ondalık biçimde yazmış; yüzde değeri doğrudan pay olarak kullanılır.",
        ],
        explanation="Yüzde gösterimi bütünü 100 eş parça kabul eder; yüzde değeri pay, 100 ise "
                    "payda olur: %35 = 35/100.",
        difficultyReason="2 adım; ön bilgi: yüzde ile paydası 100 olan kesrin denkliği; çeldiriciler yakın (payda hatası, ters çevirme); beceri: gösterim dönüştürme",
        hints=[
            "Yüzde gösteriminde bütünün kaça bölündüğünü hatırla.",
            "Bu sayının kesrin neresine yazılacağını belirle.",
            "Yüzde değerinin kesrin neresine yazılacağını belirle.",
            "Kurduğun kesrin bir bütünden küçük olup olmadığını kontrol et.",
            "Tam çözüm: bütün 100 eş parçadır; %35 gösterimi 35/100 kesrine eşittir.",
        ],
    ),
    dict(
        level=2,
        question="0,6 sayısının yüzde gösterimi hangisidir?",
        choices=["%6", "%60", "%0,6", "%600"],
        correct=1,
        distractorWhy=[
            "Ondalık sayıdaki rakamı doğrudan yüzde değeri sanmış; 0,6 sayısı 6/10'dur ve payda 100'e çevrilmelidir.",
            "doğru",
            "Ondalık gösterimi yüzde işaretiyle birlikte yazmış; iki gösterim bir arada kullanılmaz.",
            "Paydayı 100'e çevirirken bir basamak fazla kaydırmış.",
        ],
        explanation="0,6 sayısı 6/10 kesrine eşittir. Pay ve payda 10 ile genişletilirse 60/100 elde "
                    "edilir; bu da %60 demektir.",
        difficultyReason="3 adım; ön bilgi: ondalık gösterimden yüzdeye geçerken paydanın 100'e denk hâle getirilmesi; çeldiriciler yakın (basamak kaydırma); beceri: gösterim dönüştürme",
        hints=[
            "Ondalık sayıyı önce kesir biçiminde yaz.",
            "Bu kesrin paydasının kaç olduğunu belirle.",
            "Paydayı 100 yapmak için pay ve paydayı kaçla genişteceğini bul.",
            "Yeni payı yüzde değeri olarak oku.",
            "Tam çözüm: 0,6 = 6/10 = 60/100 olduğundan yüzde gösterimi %60'tır.",
        ],
    ),
    dict(
        level=3,
        question="2 3/4 tam sayılı kesrinin bileşik kesir gösterimi hangisidir?",
        choices=["5/4", "8/4", "11/4", "6/4"],
        correct=2,
        distractorWhy=[
            "Tam kısmı pay ile toplamış: 2 + 3 = 5; paydayla çarpmayı yapmamış.",
            "Yalnız tam kısmı kesre çevirmiş: 2 × 4 = 8; payı eklememiş.",
            "doğru",
            "Tam kısmı payla çarpmış: 2 × 3 = 6; paydayı hesaba katmamış.",
        ],
        explanation="Tam sayılı kesirde tam kısım payda ile çarpılır ve paya eklenir: "
                    "2 × 4 + 3 = 11. Payda değişmez: 11/4.",
        difficultyReason="3 adım; ön bilgi: tam sayılı kesirden bileşik kesre geçiş kuralı; çeldiriciler yakın (adımlardan birini atlama); beceri: gösterim dönüştürme",
        hints=[
            "Tam sayılı kesrin tam kısmını ve kesir kısmını ayrı ayrı işaretle.",
            "Bir bütünün kaç parçaya ayrıldığını belirle.",
            "Tam kısımdaki bütünlerin kaç parça ettiğini hesapla.",
            "Bulduğun parça sayısına kesir kısmındaki payı eklemeyi dene.",
            "Tam çözüm: 2 bütün 2 × 4 = 8 parça eder; 3 parça eklenince 11/4 elde edilir.",
        ],
    ),
    dict(
        level=3,
        question="17/5 bileşik kesrinin tam sayılı kesir gösterimi hangisidir?",
        choices=["2 3/5", "3 5/2", "3 2/17", "3 2/5"],
        correct=3,
        distractorWhy=[
            "Bölüm ile kalanın yerini değiştirmiş; 17 ÷ 5 işleminde bölüm 3, kalan 2'dir.",
            "Kalan ile paydanın yerini değiştirmiş; tam sayılı kesirde kesir kısmı basit kesir olmalıdır.",
            "Paydaya kesrin paydasını değil ilk payı yazmış; dönüşümde payda değişmez.",
            "doğru",
        ],
        explanation="Pay paydaya bölünür: 17 ÷ 5 = 3 kalan 2. Bölüm tam kısım, kalan yeni pay olur "
                    "ve payda değişmez: 3 2/5.",
        difficultyReason="3 adım; ön bilgi: bileşik kesirden tam sayılı kesre geçişte bölüm ve kalanın görevleri; çeldiriciler yakın (bölüm-kalan-payda karıştırma); beceri: gösterim dönüştürme",
        hints=[
            "Payı paydaya bölmeyi dene.",
            "Bölme işleminin bölümünü ve kalanını ayrı ayrı yaz.",
            "Bölümün tam sayılı kesirde nereye yazılacağını belirle.",
            "Kalanın ve paydanın yerlerini kontrol et.",
            "Tam çözüm: 17 ÷ 5 = 3 kalan 2'dir; tam kısım 3, pay 2, payda 5 olur ve sonuç 3 2/5'tir.",
        ],
    ),
    dict(
        level=2,
        question="Aşağıdaki kesirlerden hangisi bileşik kesirdir?",
        choices=["3/8", "7/4", "2/5", "4/9"],
        correct=1,
        distractorWhy=[
            "3 sayısı 8'den küçük olduğu için bu kesir bir bütünden küçüktür; basit kesirdir.",
            "doğru",
            "2 sayısı 5'ten küçük olduğu için bu kesir bir bütünden küçüktür; basit kesirdir.",
            "4 sayısı 9'dan küçük olduğu için bu kesir bir bütünden küçüktür; basit kesirdir.",
        ],
        explanation="Payı paydasına eşit ya da paydasından büyük olan kesir bileşik kesirdir. "
                    "Yalnız 7/4 kesrinde pay paydadan büyüktür.",
        difficultyReason="2 adım; ön bilgi: basit ve bileşik kesir tanımları; çeldiriciler yakın (üçü de basit kesir); beceri: sınıflandırma",
        hints=[
            "Basit kesir ile bileşik kesrin tanımlarını yan yana hatırla.",
            "Her seçenekte payı ve paydayı karşılaştır.",
            "Payı paydasından küçük olan kesirleri ele.",
            "Geriye kalan kesrin payı ile paydasını bir kez daha karşılaştır.",
            "Tam çözüm: bileşik kesirde pay paydadan küçük değildir; yalnız 7/4 bu koşulu sağlar.",
        ],
    ),
    dict(
        level=1,
        question="5/8 kesrinde 8 sayısı neyi gösterir?",
        choices=[
            "Kaç parçanın alındığını",
            "Bütünün kaç katı alındığını",
            "Bütünün kaç eş parçaya ayrıldığını",
            "Kesrin ondalık karşılığını",
        ],
        correct=2,
        distractorWhy=[
            "Alınan parça sayısını kesir çizgisinin üstündeki pay gösterir; burada bu sayı 5'tir.",
            "Kesir bütünün katını değil, bütünün eş parçalarından alınan miktarı gösterir.",
            "doğru",
            "Ondalık karşılık ayrı bir gösterimdir; payda bu değeri doğrudan vermez.",
        ],
        explanation="Kesir çizgisinin altındaki payda, bütünün kaç eş parçaya ayrıldığını belirtir. "
                    "Üstteki pay ise bu parçalardan kaç tanesinin alındığını gösterir.",
        difficultyReason="1 adım; ön bilgi: pay ve payda tanımları; çeldiriciler yakın (payla paydayı karıştırma); beceri: kavram bilgisi",
        hints=[
            "Kesir çizgisinin altındaki ve üstündeki sayıların adlarını söyle.",
            "Bir bütünün önce ne yapıldığını düşün: bölünüyor mu, alınıyor mu?",
            "Bölme işini hangi sayının anlattığına karar ver.",
            "Alınan parça sayısını hangi sayının gösterdiğini kontrol et.",
            "Tam çözüm: kesir çizgisinin altındaki payda bütünün kaç eş parçaya ayrıldığını gösterir; 5/8 kesrinde bu sayı 8'dir.",
        ],
    ),
    dict(
        level=3,
        question="1/4 miktarının ondalık ve yüzde gösterimleri sırasıyla hangileridir?",
        choices=["0,14 ve %14", "0,25 ve %2,5", "0,25 ve %25", "0,4 ve %40"],
        correct=2,
        distractorWhy=[
            "Pay ile paydayı yan yana yazmış; kesir bir bölme işlemi anlatır.",
            "Ondalık gösterimi doğru bulmuş ama yüzdeye çevirirken virgülü bir basamak sola kaydırmış.",
            "doğru",
            "Paydayı pay sanıp 4/10 kesrine çevirmiş.",
        ],
        explanation="1/4 kesri 25/100 kesrine denktir. Buradan ondalık gösterim 0,25, yüzde gösterim "
                    "%25 olarak yazılır. Üç gösterim de aynı miktarı anlatır.",
        difficultyReason="3 adım; ön bilgi: paydası 100'e denk hâle getirilebilen kesirlerin üç gösterimi; çeldiriciler yakın (virgül kaydırma, pay-payda karıştırma); beceri: gösterim dönüştürme",
        hints=[
            "Paydayı 100 yapmak için pay ve paydayı kaçla genişleteceğini bul.",
            "Yeni kesri yaz.",
            "Bu kesrin ondalık karşılığını yaz.",
            "Aynı kesrin yüzde karşılığını yaz ve iki gösterimi karşılaştır.",
            "Tam çözüm: 1/4 = 25/100 olduğundan ondalık gösterim 0,25, yüzde gösterim %25'tir.",
        ],
    ),
    dict(
        level=4,
        question="3/20 kesrinin yüzde gösterimi hangisidir?",
        choices=["%3", "%15", "%20", "%30"],
        correct=1,
        distractorWhy=[
            "Payı doğrudan yüzde değeri sanmış; paydayı 100'e çevirmeden yüzde yazılamaz.",
            "doğru",
            "Paydayı yüzde değeri olarak yazmış.",
            "Paydayı 100 yapmak için 5 ile genişletmesi gerekirken 10 ile genişletmiş.",
        ],
        explanation="Paydayı 100 yapmak için pay ve payda 5 ile genişletilir: 3/20 = 15/100. "
                    "Bu da %15 demektir.",
        difficultyReason="4 adım; ön bilgi: paydası 100'e denk hâle getirilebilen kesirlerde genişletme çarpanının bulunması; çeldiriciler yakın (payı ya da paydayı doğrudan yüzde sanma); beceri: gösterim dönüştürme",
        hints=[
            "Yüzde gösterimi için paydanın kaç olması gerektiğini hatırla.",
            "Mevcut paydayı bu sayıya çevirmek için kaçla çarpman gerektiğini bul.",
            "Aynı sayıyla payı da çarp.",
            "Yeni payı yüzde değeri olarak oku.",
            "Tam çözüm: 20 × 5 = 100 olduğundan pay da 5 ile çarpılır: 3 × 5 = 15. Sonuç 15/100, yani %15'tir.",
        ],
    ),
    dict(
        level=3,
        question="2/5 kesrinin ondalık gösterimi hangisidir?",
        choices=["0,2", "0,4", "0,25", "2,5"],
        correct=1,
        distractorWhy=[
            "Payı doğrudan onda birler basamağına yazmış; paydayı 10'a çevirmemiş.",
            "doğru",
            "Paydası 4 olan bir kesirle karıştırmış; 0,25 sayısı 1/4 kesrine karşılık gelir.",
            "Pay ile paydayı yan yana yazmış; kesir bir bölme işlemi anlatır.",
        ],
        explanation="Paydayı 10 yapmak için pay ve payda 2 ile genişletilir: 2/5 = 4/10 = 0,4.",
        difficultyReason="3 adım; ön bilgi: paydası 10'a denk hâle getirilebilen kesirlerin ondalığa çevrilmesi; çeldiriciler yakın (payı doğrudan yazma); beceri: gösterim dönüştürme",
        hints=[
            "Ondalık gösterime geçmek için paydanın kaç olması gerektiğini düşün.",
            "Mevcut paydayı bu sayıya çevirecek çarpanı bul.",
            "Aynı çarpanı paya da uygula.",
            "Yeni payı virgülden sonraki ilk basamağa yaz.",
            "Tam çözüm: 5 × 2 = 10 olduğundan pay da 2 ile çarpılır: 2/5 = 4/10 = 0,4.",
        ],
    ),
    dict(
        level=4,
        question="0,7 ile 3/4 sayılarından hangisi büyüktür?",
        choices=[
            "0,7 büyüktür; 7 sayısı 3'ten büyüktür.",
            "İkisi eşittir.",
            "Karşılaştırılamaz; biri ondalık, diğeri kesirdir.",
            "3/4 büyüktür; 3/4 = 0,75 ve 0,75 > 0,7'dir.",
        ],
        correct=3,
        distractorWhy=[
            "Payları doğrudan karşılaştırmış; iki sayı aynı gösterime çevrilmeden payları karşılaştırılamaz.",
            "3/4 = 0,75 iken 0,7 farklı bir değerdir; iki sayı eşit değildir.",
            "Gösterimler farklı olsa da miktarlar aynı biçime çevrilerek karşılaştırılabilir.",
            "doğru",
        ],
        explanation="Karşılaştırma için iki sayı aynı gösterime çevrilir: 3/4 = 75/100 = 0,75. "
                    "0,75 > 0,7 olduğundan 3/4 daha büyüktür.",
        difficultyReason="4 adım; ön bilgi: farklı gösterimlerin ortak biçime çevrilerek karşılaştırılması; çeldiriciler yakın (payları doğrudan karşılaştırma); beceri: karşılaştırma",
        hints=[
            "İki sayının farklı gösterimlerde yazıldığını fark et.",
            "Karşılaştırma yapabilmek için ikisini aynı gösterime çevirmeyi düşün.",
            "Kesri ondalığa çevir.",
            "İki ondalık sayıyı basamak basamak karşılaştır.",
            "Tam çözüm: 3/4 = 0,75'tir ve 0,75 > 0,7 olduğundan 3/4 daha büyüktür.",
        ],
    ),
    dict(
        level=4,
        question="%40 ile 2/5 miktarları için ne söylenebilir?",
        choices=[
            "İkisi de aynı miktarı gösterir; 2/5 = 40/100 = %40'tır.",
            "%40 daha büyüktür; yüzde gösterimi her zaman daha büyük bir miktar anlatır.",
            "2/5 daha büyüktür; kesirler yüzdelerden büyüktür.",
            "Karşılaştırma yapılamaz; biri yüzde, diğeri kesirdir.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Gösterim biçimi miktarın büyüklüğünü belirlemez; yüzde yalnız başka bir yazım biçimidir.",
            "Kesirlerin yüzdelerden büyük olduğu diye bir kural yoktur; iki gösterim aynı miktarı anlatabilir.",
            "İki gösterim ortak biçime çevrilerek karşılaştırılabilir; nitekim burada eşit çıkarlar.",
        ],
        explanation="2/5 kesri pay ve payda 20 ile genişletilerek 40/100 hâline gelir; bu da %40 demektir. "
                    "Gösterim değişse de miktar değişmez.",
        difficultyReason="4 adım; ön bilgi: dönüşümün miktarı değiştirmemesi; çeldiriciler yakın (gösterim biçimine göre büyüklük varsayma); beceri: karşılaştırma; kavram bilgisi",
        hints=[
            "İki miktarı aynı gösterime çevirmeyi dene.",
            "Kesrin paydasını 100 yapacak çarpanı bul.",
            "Aynı çarpanı paya da uygula.",
            "Elde ettiğin kesri yüzde biçiminde oku ve verilen yüzdeyle karşılaştır.",
            "Tam çözüm: 2/5 = 40/100 = %40'tır; iki gösterim aynı miktarı anlatır.",
        ],
    ),
    dict(
        level=2,
        question="0,36 sayısında 6 rakamı hangi basamaktadır?",
        choices=["onda birler", "yüzde birler", "birler", "onlar"],
        correct=1,
        distractorWhy=[
            "Onda birler virgülden sonraki ilk basamaktır; orada 3 rakamı bulunur.",
            "doğru",
            "Birler basamağı virgülün solundadır; orada 0 rakamı bulunur.",
            "Onlar basamağı virgülün solunda, birlerin de solundadır; bu sayıda dolu değildir.",
        ],
        explanation="Ondalık gösterimde virgülün sağındaki ilk basamak onda birler, ikinci basamak "
                    "yüzde birlerdir. 0,36 sayısında 6 rakamı ikinci basamakta olduğu için yüzde "
                    "birler basamağındadır.",
        difficultyReason="2 adım; ön bilgi: virgülün sağındaki basamak adları; çeldiriciler yakın (komşu basamaklar); beceri: basamak adlandırma",
        hints=[
            "Virgülün sağındaki basamakları sırayla adlandır.",
            "Aranan rakamın virgülden sonra kaçıncı sırada olduğunu say.",
            "O sıranın adını yaz.",
            "Virgülün solundaki basamaklarla karıştırmadığını kontrol et.",
            "Tam çözüm: virgülden sonraki ilk basamak onda birler, ikinci basamak yüzde birlerdir; 6 rakamı ikinci sırada olduğu için yüzde birler basamağındadır.",
        ],
    ),
    dict(
        level=2,
        question="Yüzde gösteriminde bütün kaç eş parça kabul edilir?",
        choices=["10", "1000", "100", "Kesrin paydası kadar"],
        correct=2,
        distractorWhy=[
            "Bütünün 10 eş parçaya ayrılması onda birleri verir; yüzde gösterimi bundan farklıdır.",
            "Bütünün 1000 eş parçaya ayrılması binde birleri verir.",
            "doğru",
            "Yüzde gösteriminde payda her zaman aynıdır; kesirden kesire değişmez.",
        ],
        explanation="Yüzde gösterimi bütünü her zaman 100 eş parça kabul eder. Bu yüzden %35, "
                    "35/100 ve 0,35 aynı miktarı anlatır.",
        difficultyReason="1 adım; ön bilgi: yüzde gösteriminin tanımı; çeldiriciler yakın (başka payda değerleri); beceri: kavram bilgisi",
        hints=[
            "Yüzde sözcüğünün kendisinin hangi sayıyı çağrıştırdığını düşün.",
            "%35 gösteriminin hangi kesre eşit olduğunu hatırla.",
            "O kesrin paydasını yaz.",
            "Bu paydanın kesirden kesire değişip değişmediğini sorgula.",
            "Tam çözüm: yüzde gösteriminde bütün her zaman 100 eş parça kabul edilir.",
        ],
    ),
    dict(
        level=5,
        question="0,45 · 2/5 · %48 · 9/25 miktarlarından hangisi en büyüktür?",
        choices=["0,45", "2/5", "%48", "9/25"],
        correct=2,
        distractorWhy=[
            "0,45 sayısı %48 gösterimine karşılık gelen 0,48'den küçüktür.",
            "2/5 = 40/100 = 0,40 olduğundan 0,48'den küçüktür.",
            "doğru",
            "9/25 = 36/100 = 0,36 olduğundan listenin en küçük miktarıdır.",
        ],
        explanation="Karşılaştırma için hepsi ondalık gösterime çevrilir: 0,45; 2/5 = 0,40; "
                    "%48 = 0,48; 9/25 = 0,36. En büyük değer 0,48 olduğundan %48 en büyüktür.",
        difficultyReason="5 adım; ön bilgi: dört farklı gösterimin ortak biçime çevrilmesi; çeldiriciler çok yakın (üçü 0,36-0,45 aralığında); beceri: karşılaştırma; gösterim dönüştürme",
        hints=[
            "Dört miktarın farklı gösterimlerde yazıldığını fark et.",
            "Hepsini aynı gösterime çevirmeye karar ver.",
            "Her kesri ve yüzdeyi ondalık biçime çevir.",
            "Dört ondalık sayıyı basamak basamak karşılaştır.",
            "Tam çözüm: 0,45; 0,40; 0,48 ve 0,45 elde edilir; en büyük değer 0,48 olduğundan %48 en büyüktür.",
        ],
    ),
    dict(
        level=3,
        question="Payı paydasına eşit olan bir kesir hangi sayıya eşittir?",
        choices=["0", "1", "Paydanın kendisine", "Payın yarısına"],
        correct=1,
        distractorWhy=[
            "Payı sıfır olan kesir sıfıra eşittir; pay ile payda eşitken durum farklıdır.",
            "doğru",
            "Kesir bir bölme işlemi anlatır; eşit iki sayının bölümü paydayı vermez.",
            "Payın yarısı ayrı bir sayıdır; eşit pay ve payda bu değeri vermez.",
        ],
        explanation="Kesir, bütünün eş parçalarından kaç tanesinin alındığını gösterir. Pay paydaya "
                    "eşitse bütünün bütün parçaları alınmış demektir; bu da bir tam bütün, yani 1 eder.",
        difficultyReason="3 adım; ön bilgi: kesrin bölme anlamı ve tam bütün kavramı; çeldiriciler yakın (sıfır ya da payda ile karıştırma); beceri: kavram bilgisi",
        hints=[
            "Bir bütünün kaç eş parçaya ayrıldığını paydanın gösterdiğini hatırla.",
            "Bu parçaların hepsi alınırsa elde kaç bütün kaldığını düşün.",
            "Örnek olarak 4/4 kesrini bir daireyle canlandır.",
            "Kesrin bir bölme işlemi anlattığını da göz önüne al.",
            "Tam çözüm: pay paydaya eşitse bütünün bütün parçaları alınmıştır; kesir 1'e eşittir.",
        ],
    ),
    dict(
        level=2,
        question="3 1/5 tam sayılı kesrinde 3 sayısı neyi gösterir?",
        choices=[
            "Kaç tam bütün bulunduğunu",
            "Bütünün kaç eş parçaya ayrıldığını",
            "Alınan parça sayısını",
            "Kesrin ondalık karşılığını",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Bütünün kaç eş parçaya ayrıldığını payda gösterir; burada bu sayı 5'tir.",
            "Alınan parça sayısını pay gösterir; burada bu sayı 1'dir.",
            "Ondalık karşılık ayrı bir gösterimdir; tam kısım bu değeri doğrudan vermez.",
        ],
        explanation="Tam sayılı kesir, bir tam sayı ile bir basit kesrin birlikte yazılmasıdır. "
                    "Baştaki sayı kaç tam bütün bulunduğunu gösterir; kalan kesir ise bir bütünden "
                    "küçük olan parçayı anlatır.",
        difficultyReason="2 adım; ön bilgi: tam sayılı kesrin yapısı; çeldiriciler yakın (pay ve payda görevleriyle karıştırma); beceri: kavram bilgisi",
        hints=[
            "Tam sayılı kesrin kaç parçadan oluştuğunu söyle.",
            "Kesir çizgisinin üstündeki ve altındaki sayıların görevlerini hatırla.",
            "Geriye kalan sayının hangi görevi üstlendiğini düşün.",
            "Bu sayının bir bütünden küçük mü büyük mü bir miktarı anlattığını kontrol et.",
            "Tam çözüm: baştaki 3 sayısı kaç tam bütün bulunduğunu gösterir; 1/5 ise bir bütünden küçük olan parçadır.",
        ],
    ),
    dict(
        level=3,
        question="Yüz eş kareye ayrılmış bir kartın 7 karesi boyanmıştır. Boyalı kısım için aşağıdakilerden hangisi YANLIŞTIR?",
        choices=[
            "Boyalı kısım 7/100'dür.",
            "Boyalı kısmın ondalık gösterimi 0,7'dir.",
            "Boyalı kısmın yüzde gösterimi %7'dir.",
            "Boyalı olmayan kısım 93 karedir.",
        ],
        correct=1,
        distractorWhy=[
            "Kart 100 eş kareye ayrıldığı ve 7 karesi boyandığı için bu ifade doğrudur.",
            "doğru",
            "Bütün 100 eş parça kabul edildiğinde boyalı kısım bu yüzdeye karşılık gelir; ifade doğrudur.",
            "Toplam 100 kareden 7'si boyalı olduğuna göre 100 − 7 = 93 kare boyasızdır; ifade doğrudur.",
        ],
        explanation="Boyalı kısım 7/100'dür; ondalık gösterimi 0,07, yüzde gösterimi %7'dir. "
                    "0,7 sayısı ise 70/100'e karşılık gelir ve boyalı kısmın on katıdır.",
        difficultyReason="3 adım; ön bilgi: paydası 100 olan kesrin ondalık gösteriminde iki basamak bulunması; çeldiriciler yakın (üçü de doğru gösterim); beceri: gösterim dönüştürme; hata bulma",
        hints=[
            "Boyalı kısmı önce kesir biçiminde yaz.",
            "Bu kesrin ondalık karşılığını hesapla; virgülden sonra kaç basamak olmalı?",
            "Yüzde karşılığını da yaz.",
            "Seçenekleri bulduğun üç gösterimle karşılaştır ve uymayanı ara.",
            "Tam çözüm: boyalı kısım 7/100 = 0,07 = %7'dir. 0,7 sayısı 70/100 demektir ve bu gösterim yanlıştır.",
        ],
    ),
    dict(
        level=4,
        question="Bir kesri ondalık gösterime çevirmenin amacı nedir?",
        choices=[
            "Miktarı büyütmek",
            "Aynı miktarı başka bir biçimde göstermek",
            "Miktarı küçültmek",
            "Paydayı yok edip yeni bir sayı elde etmek",
        ],
        correct=1,
        distractorWhy=[
            "Dönüşüm miktarı değiştirmez; 1/2 ile 0,5 aynı büyüklüğü anlatır.",
            "doğru",
            "Dönüşüm miktarı küçültmez; yalnız yazım biçimi değişir.",
            "Ondalık gösterimde payda yok olmaz; virgülün sağındaki basamaklar paydanın yerini tutar.",
        ],
        explanation="Gösterim dönüşümlerinin amacı miktarı değiştirmek değil, aynı değeri başka bir "
                    "biçimde yazmaktır. Kesir, ondalık ve yüzde aynı miktarın üç ayrı gösterimidir.",
        difficultyReason="3 adım; ön bilgi: dönüşümün miktarı korumasi ilkesi; çeldiriciler yakın (dönüşümü bir işlem sanma); beceri: kavram bilgisi",
        hints=[
            "1/2 kesrini ondalık biçimde yaz.",
            "İki gösterimin aynı büyüklüğü anlatıp anlatmadığını düşün.",
            "Dönüşümün sayıyı büyütüp küçülttüğünü sorgula.",
            "Ondalık gösterimde paydanın gerçekten yok olup olmadığına karar ver.",
            "Tam çözüm: 1/2 = 0,5'tir ve iki gösterim aynı miktarı anlatır; dönüşümün amacı miktarı değil yazım biçimini değiştirmektir.",
        ],
    ),
    dict(
        level=1,
        question="1/2 miktarının yüzde gösterimi hangisidir?",
        choices=["%12", "%2", "%50", "%1"],
        correct=2,
        distractorWhy=[
            "Pay ile paydayı yan yana yazmış; kesir bir bölme işlemi anlatır.",
            "Paydayı yüzde değeri olarak yazmış.",
            "doğru",
            "Payı yüzde değeri olarak yazmış; paydayı 100'e çevirmemiş.",
        ],
        explanation="Paydayı 100 yapmak için pay ve payda 50 ile genişletilir: 1/2 = 50/100 = %50.",
        difficultyReason="2 adım; ön bilgi: paydası 100'e denk hâle getirme; çeldiriciler yakın (pay ya da paydayı doğrudan yüzde sanma); beceri: gösterim dönüştürme",
        hints=[
            "Yüzde gösteriminde paydanın kaç olması gerektiğini hatırla.",
            "Mevcut paydayı 100 yapacak çarpanı bul.",
            "Aynı çarpanı paya da uygula.",
            "Yeni payı yüzde değeri olarak oku.",
            "Tam çözüm: 2 × 50 = 100 olduğundan pay da 50 ile çarpılır: 1/2 = 50/100 = %50.",
        ],
    ),
    dict(
        level=4,
        question="Bir öğrenci 3/10 kesrinin yüzde gösterimini %3 diye yazmıştır. Öğrencinin hatası nedir?",
        choices=[
            "Paydayı 100'e çevirmeden payı doğrudan yüzde olarak yazmıştır; doğrusu %30'dur.",
            "Payı 100 ile çarpmalıydı; doğrusu %300'dür.",
            "Yüzde gösterimi yalnız paydası 100 olan kesirlerde kullanılır; bu kesir çevrilemez.",
            "Hata yoktur; 3/10 kesri %3'e eşittir.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Payın 100 ile çarpılması gerekmez; payda 100'e çevrilirken pay aynı çarpanla genişletilir.",
            "Paydası 10 olan kesirler de 100'e denk hâle getirilebilir; dönüşüm mümkündür.",
            "3/10 kesri 30/100'e denktir; %3 gösterimi 3/100 demektir ve on kat küçüktür.",
        ],
        explanation="Paydayı 100 yapmak için pay ve payda 10 ile genişletilir: 3/10 = 30/100 = %30. "
                    "Öğrenci paydayı çevirmeden payı doğrudan yüzde değeri olarak yazmıştır.",
        difficultyReason="4 adım; ön bilgi: yüzdeye çevirirken pay ve paydanın aynı çarpanla genişletilmesi; çeldiriciler yakın (aşırı ya da eksik genişletme); beceri: hata teşhisi",
        hints=[
            "Kesri kendin yüzdeye çevirip sonucu bul.",
            "Paydayı 100 yapmak için hangi çarpanı kullandığını yaz.",
            "Aynı çarpanı paya uygulayıp uygulamadığını kontrol et.",
            "Kendi sonucunla öğrencinin yazdığını karşılaştır.",
            "Tam çözüm: 3/10 = 30/100 = %30'dur. Öğrenci paydayı çevirmeden payı yüzde değeri saymıştır.",
        ],
    ),
    dict(
        level=4,
        question="Bir öğrenci 1 1/2 tam sayılı kesrini bileşik kesir olarak 11/2 diye yazmıştır. Öğrencinin hatası nedir?",
        choices=[
            "Paydayı da değiştirmeliydi; doğrusu 11/4'tür.",
            "Hata yoktur; 1 1/2 kesri 11/2'ye eşittir.",
            "Tam kısmı paydayla toplamalıydı; doğrusu 1/3'tür.",
            "Tam kısmı payın soluna yazıp rakamları birleştirmiştir; doğru bileşik kesir 3/2'dir.",
        ],
        correct=3,
        distractorWhy=[
            "Bileşik kesre çevirirken payda değişmez; yalnız pay yeniden hesaplanır.",
            "11/2 kesri 5 1/2 miktarına karşılık gelir; verilen miktardan çok büyüktür.",
            "Tam kısım paydayla toplanmaz; paydayla çarpılıp paya eklenir.",
            "doğru",
        ],
        explanation="Tam kısım payda ile çarpılıp paya eklenir: 1 × 2 + 1 = 3; payda değişmez. "
                    "Doğru bileşik kesir 3/2'dir. Öğrenci ise iki rakamı yan yana yazarak 11 elde etmiştir; "
                    "bu sayı 11/2, yani 5 1/2 demektir.",
        difficultyReason="4 adım; ön bilgi: tam sayılı kesirden bileşik kesre geçişte rakam birleştirmenin geçersizliği; çeldiriciler yakın (payda değiştirme, toplama önerme); beceri: hata teşhisi",
        hints=[
            "Dönüşümü kendin yapıp doğru bileşik kesri bul.",
            "Tam kısımla paydayı hangi işlemle birleştirdiğini yaz.",
            "Paydanın değişip değişmediğini kontrol et.",
            "Öğrencinin yazdığı kesri tam sayılı biçime geri çevirip ne elde ettiğine bak.",
            "Tam çözüm: 1 × 2 + 1 = 3 olduğundan doğru bileşik kesir 3/2'dir. Öğrencinin yazdığı 11/2 ise 5 1/2 demektir.",
        ],
    ),
    dict(
        level=5,
        question="0,5 · 2/5 · %45 miktarları küçükten büyüğe nasıl sıralanır?",
        choices=[
            "%45 < 2/5 < 0,5",
            "2/5 < %45 < 0,5",
            "0,5 < 2/5 < %45",
            "2/5 < 0,5 < %45",
        ],
        correct=1,
        distractorWhy=[
            "2/5 = 0,40 ve %45 = 0,45 olduğundan bu iki miktarın sırası ters yazılmış.",
            "doğru",
            "0,5 sayısı üç miktarın en büyüğüdür; sıralamanın başına yazılamaz.",
            "%45 = 0,45 olduğundan 0,5'ten küçüktür; sıralamanın sonuna yazılamaz.",
        ],
        explanation="Üç miktar da ondalık gösterime çevrilir: 0,5; 2/5 = 0,40; %45 = 0,45. "
                    "Küçükten büyüğe sıralama 0,40 < 0,45 < 0,50, yani 2/5 < %45 < 0,5 olur.",
        difficultyReason="5 adım; ön bilgi: üç farklı gösterimin ortak biçime çevrilip sıralanması; çeldiriciler çok yakın (ikili sıraları değiştirme); beceri: karşılaştırma; sıralama",
        hints=[
            "Üç miktarın farklı gösterimlerde yazıldığını fark et.",
            "Hepsini ondalık gösterime çevir.",
            "Üç ondalık sayıyı küçükten büyüğe diz.",
            "Her sayının yanına asıl gösterimini geri yaz.",
            "Tam çözüm: 0,5; 0,40 ve 0,45 elde edilir; sıralama 2/5 < %45 < 0,5 olur.",
        ],
    ),
]


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
    return [T(v) + ek for v in degerler], 0, ["doğru"] + [g for _, g in s["celdiriciler"]]


AILELER = [
    ("tr.g05.mat.5.1.2", "MAT.5.1.2",
     [("tr.g05.mat.5.1.2.note.01", "Problemi matematiksel işleme dönüştürme", A12_NOT1),
      ("tr.g05.mat.5.1.2.note.02", "Çözümü tahmin etme ve kontrol etme", A12_NOT2)]),
    ("tr.g05.mat.5.1.3", "MAT.5.1.3",
     [("tr.g05.mat.5.1.3.note.01",
       "Kesir, ondalık ve yüzde gösterimleri", A13)]),
]


def uret():
    kayitlar = []
    for onek, kazanim, gruplar in AILELER:
        i = 0
        for note_id, topic, sorular in gruplar:
            for s in sorular:
                i += 1
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
