# -*- coding: utf-8 -*-
"""A3 parti 5 — MAT.5.2.3 ve MAT.5.2.4 ailelerinin yeniden üretimi.

Önceki hâl:
  5-2-3 (21 soru): beş kalıp dörder kez tekrarlanıyordu — sonraki terim,
    eksik terim, kural, şekil örüntüsü, kuralı bozan terim. Notun ayrıca
    anlattığı azalan örüntü, çarpan örüntüsü, adım numarasından terime
    geçiş ve "kural bütün terimleri açıklamalıdır" ilkesi hiç sorulmuyordu.
    Şekil örüntüsü soruları da yalnız toplam parçayı soruyordu; notun
    açıkça ayırdığı "bir adımda eklenen yeni parça sayısı" kavramı hiç
    ölçülmüyordu.
  5-2-4 (21 soru): 21/21 soru "Girdi #: önce # ile çarp, sonra # ekle.
    Algoritmanın çıktısı kaçtır?" kalıbındaydı. Notun anlattığı koşullu
    ("eğer") adım, tekrar, ters işlemle kontrol, akış gösterimi, girdi-çıktı
    tablosundan kural çıkarma ve adım sırasının sonucu değiştirmesi hiç
    sorulmuyordu.

Sayısal sorularda doğru cevap da çeldiriciler de Python'da hesaplanır;
çeldirici, adlandırılmış yanılgının kendi ifadesinin değeridir.

choices + correct + distractorWhy + hints + explanation tek birimde üretildi
(AUTHORING_RULES.md §1 atomiklik ilkesi).
"""

KAYNAK = "https://tymm.meb.gov.tr/upload/program/2024programmat5678Onayli.pdf"


# ---------------------------------------------------------------------------
# MAT.5.2.3 — note.03 "Örüntü kuralını bulma"
# ---------------------------------------------------------------------------

A23 = [
    dict(
        level=1,
        question="14, 25, 36, 47, … sayı örüntüsünün sonraki terimi kaçtır?",
        dogru=47 + 11,
        celdiriciler=[
            (47 + 10, "Ardışık terimler arasındaki artışı 11 yerine 10 almış."),
            (47 + 11 + 11, "İki adım birden ilerlemiş; soru yalnız bir sonraki terimi istiyor."),
            (36, "Bir önceki terimi yazmış."),
        ],
        explanation="Ardışık terimler arasındaki fark her adımda 11'dir: 25 − 14 = 11, 36 − 25 = 11, "
                    "47 − 36 = 11. Sonraki terim 47 + 11 = 58 olur.",
        difficultyReason="2 adım; ön bilgi: ardışık terimler arasındaki sabit farkın bulunması; çeldiriciler yakın (artışı bir eksik alma); beceri: örüntü kuralı bulma",
        hints=[
            "Ardışık terimler arasındaki farkları tek tek hesapla.",
            "Bulduğun farkların birbirine eşit olup olmadığına bak.",
            "Fark her adımda aynıysa kuralın sabit artan olduğunu söyle.",
            "Bu farkı son terime eklemeyi dene.",
            "Tam çözüm: fark her adımda 11'dir; 47 + 11 = 58 bulunur.",
        ],
    ),
    dict(
        level=2,
        question="23, 27, □, 35, 39 örüntüsünde kutuya hangi sayı gelmelidir?",
        dogru=27 + 4,
        celdiriciler=[
            (27 + 3, "Artış miktarını 4 yerine 3 almış."),
            ((27 + 39) // 2, "27 ile 39'un tam ortasını almış; oysa kutu 27'den yalnız bir adım sonradır."),
            (27 + 2, "Artışı iki adıma bölmüş: 4 ÷ 2 = 2 eklemiş."),
        ],
        explanation="Bilinen terimler arasındaki fark 4'tür: 27 − 23 = 4 ve 39 − 35 = 4. "
                    "Kutu 27'den bir adım sonra geldiğine göre 27 + 4 = 31 olur.",
        difficultyReason="2 adım; ön bilgi: örüntünün ortasındaki eksik terimin komşu terimlerden bulunması; çeldiriciler yakın (ortalama alma); beceri: örüntü tamamlama",
        hints=[
            "Kutunun iki yanındaki bilinen terimleri işaretle.",
            "Yan yana duran bilinen terimler arasındaki farkı hesapla.",
            "Kutunun soldaki terimden kaç adım sonra geldiğini say.",
            "Farkı o terime bir kez eklemeyi dene.",
            "Tam çözüm: fark 4'tür ve kutu 27'den bir adım sonradır; 27 + 4 = 31 bulunur.",
        ],
    ),
    dict(
        level=2,
        question="22, 32, 42, 52, 62 örüntüsünün kuralı hangisidir?",
        choices=[
            "Her terim bir öncekine 10 eklenerek bulunur.",
            "Her terim bir öncekinin 2 katıdır.",
            "Her terim bir öncekine 20 eklenerek bulunur.",
            "Her terim 10 ile çarpılıp 2 eklenerek bulunur.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "İki katı kuralı 22'den sonra 44 verirdi; oysa ikinci terim 32'dir.",
            "Yirmi eklense ikinci terim 42 olurdu; terimler arasındaki fark bunun yarısıdır.",
            "Bu kural 22'den sonra 222 verirdi; örüntüdeki artış çarpma ile değil toplama ile oluşur.",
        ],
        explanation="Ardışık terimlerin farkı her adımda 10'dur: 32 − 22 = 10, 42 − 32 = 10. "
                    "Kural, her terime 10 eklenmesidir.",
        difficultyReason="2 adım; ön bilgi: sabit artan kuralın ifade edilmesi; çeldiriciler yakın (çarpan kuralı ya da iki katı artış önerme); beceri: kural ifade etme",
        hints=[
            "Ardışık terimler arasındaki farkları hesapla.",
            "Farkların sabit olup olmadığına karar ver.",
            "Her seçenekteki kuralı ilk terime uygulayıp ikinci terimi tahmin et.",
            "Tahmini örüntüdeki gerçek ikinci terimle karşılaştır.",
            "Tam çözüm: fark her adımda 10'dur; kural her terime 10 eklenmesidir.",
        ],
    ),
    dict(
        level=3,
        question="Bir şekil örüntüsünde toplam parça sayıları ilk dört adımda sırasıyla 20, 31, 42 ve 53'tür. Beşinci adımda toplam kaç parça olur?",
        dogru=53 + 11,
        celdiriciler=[
            (11, "Her adımda eklenen yeni parça sayısını yazmış; soru toplam parça sayısını istiyor."),
            (53 + 10, "Adımlar arasındaki artışı 11 yerine 10 almış."),
            (53 + 11 + 11, "İki adım birden ilerlemiş; beşinci değil altıncı adımı hesaplamış."),
        ],
        explanation="Adımlar arasındaki artış sabittir: 31 − 20 = 11, 42 − 31 = 11, 53 − 42 = 11. "
                    "Beşinci adımdaki toplam parça sayısı 53 + 11 = 64 olur.",
        difficultyReason="3 adım; ön bilgi: şekil örüntüsünde toplam parça sayısının sabit artması; çeldiriciler yakın (eklenen parçayı toplam sanma); beceri: örüntü kuralı bulma",
        hints=[
            "Ardışık adımlardaki toplam parça sayıları arasındaki farkları hesapla.",
            "Farkların her adımda aynı olup olmadığına bak.",
            "Sorunun toplam parçayı mı yoksa eklenen parçayı mı istediğini kontrol et.",
            "Son bilinen adıma artış miktarını eklemeyi dene.",
            "Tam çözüm: her adımda 11 parça eklenir; beşinci adımda 53 + 11 = 64 parça olur.",
        ],
    ),
    dict(
        level=3,
        question="Toplam parça sayıları 20, 31, 42 ve 53 olan bir şekil örüntüsünde her adımda kaç yeni parça eklenmektedir?",
        dogru=11,
        celdiriciler=[
            (53, "Son adımdaki toplam parça sayısını yazmış; soru bir adımda eklenen parçayı istiyor."),
            (20, "İlk adımdaki toplam parça sayısını yazmış."),
            (53 - 20, "İlk ve son adım arasındaki toplam artışı yazmış; bu artış üç adıma dağılır."),
        ],
        explanation="Bir adımda eklenen yeni parça sayısı, ardışık iki adımın farkıdır: 31 − 20 = 11. "
                    "Toplam parça sayısı ile bir adımda eklenen parça sayısı farklı kavramlardır.",
        difficultyReason="3 adım; ön bilgi: toplam parça ile eklenen parça kavramlarının ayrımı; çeldiriciler yakın (toplamı ya da genel artışı yanıt sanma); beceri: kavram ayırt etme",
        hints=[
            "Sorunun toplam parçayı mı yoksa her adımda eklenen parçayı mı istediğini işaretle.",
            "Ardışık iki adımın parça sayılarını yan yana yaz.",
            "Bu iki sayının farkını al.",
            "Aynı farkın diğer adımlarda da çıkıp çıkmadığını kontrol et.",
            "Tam çözüm: ardışık adımların farkı 11'dir; her adımda 11 yeni parça eklenir.",
        ],
    ),
    dict(
        level=1,
        question="25, 28, 31, 34, … sayı örüntüsünün sonraki terimi kaçtır?",
        dogru=34 + 3,
        celdiriciler=[
            (34 + 4, "Ardışık terimler arasındaki artışı 3 yerine 4 almış."),
            (34 + 3 + 3, "İki adım birden ilerlemiş."),
            (31, "Bir önceki terimi yazmış."),
        ],
        explanation="Ardışık terimlerin farkı 3'tür: 28 − 25 = 3, 31 − 28 = 3, 34 − 31 = 3. "
                    "Sonraki terim 34 + 3 = 37 olur.",
        difficultyReason="2 adım; ön bilgi: sabit artan örüntüde bir sonraki terim; çeldiriciler yakın (artışı bir fazla alma); beceri: örüntü kuralı bulma",
        hints=[
            "Terimleri alt alta yazıp aralarındaki farkları hesapla.",
            "Farkların eşit olup olmadığına bak.",
            "Sabit farkı belirle.",
            "Bu farkı son terime bir kez eklemeyi dene.",
            "Tam çözüm: fark her adımda 3'tür; 34 + 3 = 37 bulunur.",
        ],
    ),
    dict(
        level=2,
        question="11, 19, □, 35, 43 örüntüsünde kutuya hangi sayı gelmelidir?",
        dogru=19 + 8,
        celdiriciler=[
            (19 + 6, "Artışı 8 yerine 6 almış."),
            (19 + 16, "İki adım birden ilerlemiş; 35 sayısı zaten dizide yazılıdır."),
            (19 + 4, "Artışı iki adıma bölmüş: 8 ÷ 2 = 4 eklemiş."),
        ],
        explanation="Bilinen terimler arasındaki fark 8'dir: 19 − 11 = 8 ve 43 − 35 = 8. "
                    "Kutu 19'dan bir adım sonra geldiğine göre 19 + 8 = 27 olur.",
        difficultyReason="2 adım; ön bilgi: eksik terimin sabit farktan bulunması; çeldiriciler yakın (artışı yanlış alma); beceri: örüntü tamamlama",
        hints=[
            "Yan yana duran bilinen terimlerin farkını hesapla.",
            "Aynı farkın dizinin diğer ucunda da geçerli olup olmadığını kontrol et.",
            "Kutunun soldaki bilinen terimden kaç adım sonra geldiğini say.",
            "Farkı o terime ekleyip sonucu sağdaki terimle sına.",
            "Tam çözüm: fark 8'dir; 19 + 8 = 27 bulunur ve 27 + 8 = 35 ile dizi tutarlı çıkar.",
        ],
    ),
    dict(
        level=2,
        question="7, 15, 23, 31, 39 örüntüsünün kuralı hangisidir?",
        choices=[
            "Her terim bir öncekine 7 eklenerek bulunur.",
            "Her terim bir öncekine 8 eklenerek bulunur.",
            "Her terim bir öncekinin 2 katından 1 eksiktir.",
            "Her terim adım numarasının 8 katıdır.",
        ],
        correct=1,
        distractorWhy=[
            "İlk terimin kendisini artış miktarı sanmış; 7 eklense ikinci terim 14 olurdu.",
            "doğru",
            "Bu kural ilk iki terimi açıklar (2 × 7 − 1 = 13 bile değil) ama üçüncü terimden itibaren tutmaz.",
            "Bu kural birinci adımda 8 verirdi; oysa ilk terim 7'dir.",
        ],
        explanation="Ardışık terimlerin farkı her adımda 8'dir: 15 − 7 = 8, 23 − 15 = 8, 31 − 23 = 8. "
                    "Kural, her terime 8 eklenmesidir.",
        difficultyReason="2 adım; ön bilgi: sabit artan kuralın ifade edilmesi ve bütün terimlerle sınanması; çeldiriciler yakın (ilk terimi artış sanma); beceri: kural ifade etme",
        hints=[
            "Ardışık terimler arasındaki farkları hesapla.",
            "Her seçenekteki kuralı ilk terime uygulayıp ikinci terimi tahmin et.",
            "Tahminin örüntüdeki gerçek terimle uyuşup uyuşmadığına bak.",
            "Yalnız ilk terimi açıklayan kuralları ele.",
            "Tam çözüm: fark her adımda 8'dir; kural her terime 8 eklenmesidir.",
        ],
    ),
    dict(
        level=3,
        question="Her adımda 5 eklenmesi gereken 5, 10, 15, 22, 25 dizisinde kuralı bozan terim hangisidir?",
        dogru=22,
        celdiriciler=[
            (15, "Kurala uyan son terimi işaretlemiş; 15 − 10 = 5 olduğu için bu terim doğrudur."),
            (25, "Dizinin son terimini seçmiş; oysa kural bir önceki adımda bozulmuştur."),
            (10, "İkinci terimi işaretlemiş; 10 − 5 = 5 olduğu için bu terim de kurala uygundur."),
        ],
        explanation="Ardışık farklar sırasıyla 5, 5, 7 ve 3'tür. Kural gereği dördüncü terim 15 + 5 = 20 "
                    "olmalıydı; dizide 22 yazıldığı için kuralı bozan terim 22'dir.",
        difficultyReason="3 adım; ön bilgi: verilen kuralla dizinin adım adım sınanması; çeldiriciler yakın (kurala uyan terimleri seçme); beceri: hata bulma",
        hints=[
            "Soruda kuralın ne olduğunun verildiğini fark et.",
            "Ardışık terimler arasındaki farkları baştan sona tek tek hesapla.",
            "Hangi farkın 5'ten farklı çıktığını işaretle.",
            "O farkın hangi terimde ortaya çıktığına karar ver.",
            "Tam çözüm: farklar 5, 5, 7, 3'tür. Dördüncü terim 15 + 5 = 20 olmalıydı; dizideki 22 kuralı bozar.",
        ],
    ),
    dict(
        level=4,
        question="48, 42, 36, 30, … örüntüsünün sonraki terimi kaçtır?",
        dogru=30 - 6,
        celdiriciler=[
            (30 - 4, "Azalış miktarını 6 yerine 4 almış."),
            (36, "Bir önceki terimi yazmış."),
            (30 - 6 - 6, "İki adım birden gerilemiş."),
        ],
        explanation="Terimler her adımda 6 azalmaktadır: 48 − 42 = 6, 42 − 36 = 6, 36 − 30 = 6. "
                    "Sonraki terim 30 − 6 = 24 olur.",
        difficultyReason="3 adım; ön bilgi: sabit azalan örüntünün fark hesabı; çeldiriciler yakın (azalışı yanlış alma); beceri: örüntü kuralı bulma",
        hints=[
            "Terimlerin büyüyüp mü küçüldüğüne mi baktığını belirle.",
            "Ardışık terimler arasındaki farkları hesapla.",
            "Farkın her adımda aynı olup olmadığına bak.",
            "Bu farkı son terimden çıkarmayı dene.",
            "Tam çözüm: her adımda 6 azalır; 30 − 6 = 24 bulunur.",
        ],
    ),
    dict(
        level=4,
        question="3, 6, 12, 24, … örüntüsünün sonraki terimi kaçtır?",
        dogru=24 * 2,
        celdiriciler=[
            (24 + 6, "Örüntüyü sabit artan sanıp ilk farkı eklemiş: 24 + 6."),
            (24 + 12, "Son iki terim arasındaki farkı sabit sanıp eklemiş: 24 + 12."),
            (24 * 2 * 2, "İki adım birden ilerlemiş."),
        ],
        explanation="Bu örüntüde fark sabit değildir; her terim bir öncekinin 2 katıdır: "
                    "6 = 3 × 2, 12 = 6 × 2, 24 = 12 × 2. Sonraki terim 24 × 2 = 48 olur.",
        difficultyReason="4 adım; ön bilgi: çarpan örüntüsünün sabit artan örüntüden ayırt edilmesi; çeldiriciler yakın (sabit fark varsayma); beceri: kural türü belirleme",
        hints=[
            "Önce ardışık terimler arasındaki farkları hesapla.",
            "Farkların sabit olup olmadığını kontrol et.",
            "Fark sabit değilse terimler arasında bölme ilişkisi olup olmadığına bak.",
            "Her terimi bir öncekine bölmeyi dene.",
            "Tam çözüm: her terim bir öncekinin 2 katıdır; 24 × 2 = 48 bulunur.",
        ],
    ),
    dict(
        level=4,
        question="İlk terimi 4 olan ve her adımda 7 artan bir örüntünün 10. terimi kaçtır?",
        dogru=4 + 9 * 7,
        celdiriciler=[
            (4 + 10 * 7, "Artışı 10 kez uygulamış; oysa ilk terim zaten 1. adımdır ve 10. terime 9 adımda ulaşılır."),
            (10 * 7, "İlk terimi hiç hesaba katmamış; yalnız 10 × 7 çarpımını yazmış."),
            (4 + 7, "Yalnız bir adım ilerlemiş; 11 sayısı 2. terimdir."),
        ],
        explanation="İlk terim 1. adımdır; 10. terime ulaşmak için 9 kez artış uygulanır: "
                    "4 + 9 × 7 = 4 + 63 = 67.",
        difficultyReason="4 adım; ön bilgi: adım sayısı ile artış sayısı arasındaki bir fark; çeldiriciler çok yakın (bir fazla artış uygulama); beceri: genelleme; hesaplama",
        hints=[
            "İlk terimin kaçıncı adıma karşılık geldiğini söyle.",
            "10. terime ulaşmak için kaç kez artış uygulanacağını say.",
            "Bu sayıyı artış miktarıyla çarp.",
            "Çıkan sonucu ilk terime eklemeyi dene.",
            "Tam çözüm: 10. terime 9 adımda ulaşılır; 4 + 9 × 7 = 4 + 63 = 67 bulunur.",
        ],
    ),
    dict(
        level=5,
        question="İlk terimi 6 olan ve her adımda 5 artan bir örüntüde 41 sayısı kaçıncı terimdir?",
        dogru=(41 - 6) // 5 + 1,
        celdiriciler=[
            ((41 - 6) // 5, "Kaç adım ilerlendiğini bulup orada durmuş; ilk terimin 1. adım olduğunu eklememiş."),
            ((41 - 6) // 5 + 2, "Bir adım fazla saymış."),
            (41 - 6, "Yalnız iki terim arasındaki farkı yazmış; bu sayı adım numarası değildir."),
        ],
        explanation="İlk terimden 41'e kadar artış 41 − 6 = 35'tir. Her adımda 5 artıldığına göre "
                    "35 ÷ 5 = 7 adım ilerlenmiştir. İlk terim 1. adım olduğu için 41 sayısı 7 + 1 = 8. terimdir.",
        difficultyReason="5 adım; ön bilgi: adım sayısı ile terim numarası arasındaki bir fark; çeldiriciler çok yakın (ara sonucu yanıt sanma); beceri: akıl yürütme; hesaplama",
        hints=[
            "İlk terim ile aranan terim arasındaki toplam artışı hesapla.",
            "Bu artışın kaç adımda oluştuğunu bul.",
            "İlk terimin kaçıncı adım olduğunu hatırla.",
            "Adım sayısına ilk terimi de katmayı dene.",
            "Tam çözüm: 41 − 6 = 35, 35 ÷ 5 = 7 adım eder; ilk terim 1. adım olduğundan 41 sayısı 8. terimdir.",
        ],
    ),
    dict(
        level=4,
        question="Bir örüntünün ilk üç terimi 2, 4 ve 8'dir. Aşağıdaki kurallardan hangisi bu üç terimin hepsini birden açıklar?",
        choices=[
            "Her terime 2 eklenir.",
            "Her terime adım numarası kadar eklenir.",
            "Her terim bir öncekinin karesidir.",
            "Her terim bir öncekinin 2 katıdır.",
        ],
        correct=3,
        distractorWhy=[
            "Bu kural ilk iki terimi açıklar ama üçüncü terimi 6 verir; oysa örüntüde 8 yazılıdır.",
            "Bu kural ikinci terimi 3 verir; ilk iki terimi bile açıklamaz.",
            "Bu kural ilk iki terimi açıklar ama üçüncü terimi 16 verir; oysa örüntüde 8 yazılıdır.",
            "doğru",
        ],
        explanation="Bir kural, verilen terimlerin yalnız bir kısmını değil hepsini açıklamalıdır. "
                    "İki katı kuralı 2 → 4 → 8 dizisinin üç terimini de verir; diğer kurallar üçüncü "
                    "terimde tutmaz.",
        difficultyReason="4 adım; ön bilgi: kuralın bütün terimlerle sınanması gerektiği; çeldiriciler çok yakın (ikisi de ilk iki terimi açıklıyor); beceri: kural sınama; akıl yürütme",
        hints=[
            "Bir kuralın kaç terimi açıklaması gerektiğini düşün.",
            "Her seçeneği ilk terime uygulayıp ikinci terimi tahmin et.",
            "İkinci terimi tutturan seçeneklerde üçüncü terimi de tahmin et.",
            "Üçüncü terimde tutmayan kuralları ele.",
            "Tam çözüm: 2 × 2 = 4 ve 4 × 2 = 8 olduğundan iki katı kuralı üç terimi de açıklar; diğerleri üçüncü terimde tutmaz.",
        ],
    ),
    dict(
        level=3,
        question="Bir örüntünün adım ve terim tablosu şöyledir: 1. adım 9, 2. adım 14, 3. adım 19, 4. adım 24. Altıncı adımdaki terim kaçtır?",
        dogru=9 + 5 * 5,
        celdiriciler=[
            (9 + 4 * 5, "Beşinci adımda durmuş; 29 sayısı altıncı adımın değil beşinci adımın terimidir."),
            (9 + 6 * 5, "Bir adım fazla ilerlemiş; artışı altı kez uygulamış."),
            (5, "Adımlar arasındaki artış miktarını yazmış; soru terimin kendisini istiyor."),
        ],
        explanation="Terimler her adımda 5 artmaktadır. 1. adımdan 6. adıma 5 adım ilerlenir: "
                    "9 + 5 × 5 = 9 + 25 = 34.",
        difficultyReason="3 adım; ön bilgi: adım tablosundan sabit artışın okunması ve ileri adıma taşınması; çeldiriciler yakın (bir eksik ya da bir fazla adım); beceri: örüntü genelleme",
        hints=[
            "Tablodaki ardışık terimlerin farkını hesapla.",
            "Dördüncü adımdan altıncı adıma kaç adım olduğunu say.",
            "Ya da birinci adımdan altıncı adıma kaç adım olduğunu say.",
            "Adım sayısını artışla çarpıp başlangıç terimine eklemeyi dene.",
            "Tam çözüm: artış 5'tir; 1. adımdan 6. adıma 5 adım vardır ve 9 + 5 × 5 = 34 bulunur.",
        ],
    ),
    dict(
        level=1,
        question="18, 29, 40, 51, … sayı örüntüsünün sonraki terimi kaçtır?",
        dogru=51 + 11,
        celdiriciler=[
            (51 + 9, "Ardışık terimler arasındaki artışı 11 yerine 9 almış."),
            (40, "Bir önceki terimi yazmış."),
            (51 + 11 + 11, "İki adım birden ilerlemiş."),
        ],
        explanation="Ardışık terimlerin farkı 11'dir: 29 − 18 = 11, 40 − 29 = 11, 51 − 40 = 11. "
                    "Sonraki terim 51 + 11 = 62 olur.",
        difficultyReason="2 adım; ön bilgi: sabit artan örüntüde bir sonraki terim; çeldiriciler yakın (artışı yanlış alma); beceri: örüntü kuralı bulma",
        hints=[
            "Terimler arasındaki farkları tek tek hesapla.",
            "Farkların eşit olduğunu doğrula.",
            "Sabit artış miktarını belirle.",
            "Bu miktarı son terime eklemeyi dene.",
            "Tam çözüm: fark her adımda 11'dir; 51 + 11 = 62 bulunur.",
        ],
    ),
    dict(
        level=2,
        question="29, 32, □, 38, 41 örüntüsünde kutuya hangi sayı gelmelidir?",
        dogru=32 + 3,
        celdiriciler=[
            (32 + 2, "Artışı 3 yerine 2 almış."),
            (32 + 6, "İki adım birden ilerlemiş; 38 zaten dizide yazılıdır."),
            (32 + 1, "Terimlerin birer birer arttığını sanmış."),
        ],
        explanation="Bilinen terimlerin farkı 3'tür: 32 − 29 = 3 ve 41 − 38 = 3. "
                    "Kutu 32'den bir adım sonra geldiğine göre 32 + 3 = 35 olur.",
        difficultyReason="2 adım; ön bilgi: eksik terimin komşu terimlerden bulunması; çeldiriciler yakın (adım sayısını şaşırma); beceri: örüntü tamamlama",
        hints=[
            "Kutunun iki yanındaki bilinen terimleri işaretle.",
            "Yan yana duran bilinen terimlerin farkını hesapla.",
            "Kutunun kaç adım sonra geldiğini say.",
            "Bulduğun sayıyı sağdaki terimle sınayarak doğrula.",
            "Tam çözüm: fark 3'tür; 32 + 3 = 35 bulunur ve 35 + 3 = 38 ile dizi tutarlı çıkar.",
        ],
    ),
    dict(
        level=2,
        question="23, 30, 37, 44, 51 örüntüsünün kuralı hangisidir?",
        choices=[
            "Her terim bir öncekine 6 eklenerek bulunur.",
            "Her terim adım numarasının 7 katıdır.",
            "Her terim bir öncekine 7 eklenerek bulunur.",
            "Her terim bir öncekinin 2 katından 16 eksiktir.",
        ],
        correct=2,
        distractorWhy=[
            "Altı eklense ikinci terim 29 olurdu; oysa örüntüde 30 yazılıdır.",
            "Bu kural birinci adımda 7 verirdi; oysa ilk terim 23'tür.",
            "doğru",
            "Bu kural ilk adımda 30 verir ama ikinci adımda 44 verir; üçüncü terimde tutmaz.",
        ],
        explanation="Ardışık terimlerin farkı her adımda 7'dir: 30 − 23 = 7, 37 − 30 = 7, 44 − 37 = 7. "
                    "Kural, her terime 7 eklenmesidir.",
        difficultyReason="2 adım; ön bilgi: sabit artan kuralın bütün terimlerle sınanması; çeldiriciler yakın (yakın artış değerleri); beceri: kural ifade etme",
        hints=[
            "Ardışık terimler arasındaki farkları hesapla.",
            "Farkların sabit olup olmadığını kontrol et.",
            "Her seçenekteki kuralı ilk terime uygulayıp ikinci terimi tahmin et.",
            "Tahmini gerçek ikinci terimle karşılaştır.",
            "Tam çözüm: fark her adımda 7'dir; kural her terime 7 eklenmesidir.",
        ],
    ),
    dict(
        level=3,
        question="Bir şekil örüntüsünde toplam parça sayıları 19, 25, 31 ve 37'dir. Altıncı adımda toplam kaç parça olur?",
        dogru=37 + 2 * 6,
        celdiriciler=[
            (37 + 6, "Beşinci adımda durmuş; 43 sayısı altıncı adımın değil beşinci adımın parça sayısıdır."),
            (6, "Her adımda eklenen yeni parça sayısını yazmış; soru toplam parçayı istiyor."),
            (37 + 3 * 6, "Bir adım fazla ilerlemiş; artışı üç kez uygulamış."),
        ],
        explanation="Her adımda 6 parça eklenir: 25 − 19 = 6, 31 − 25 = 6, 37 − 31 = 6. "
                    "Dördüncü adımdan altıncı adıma iki adım vardır: 37 + 2 × 6 = 37 + 12 = 49.",
        difficultyReason="3 adım; ön bilgi: sabit artışın birden çok adım ileriye taşınması; çeldiriciler yakın (bir eksik ya da bir fazla adım); beceri: örüntü genelleme",
        hints=[
            "Ardışık adımlar arasındaki artışı hesapla.",
            "Verilen son adımın kaçıncı adım olduğunu belirle.",
            "Oradan altıncı adıma kaç adım kaldığını say.",
            "Adım sayısını artışla çarpıp son bilinen değere eklemeyi dene.",
            "Tam çözüm: artış 6'dır ve dördüncü adımdan altıncı adıma iki adım vardır; 37 + 2 × 6 = 49 bulunur.",
        ],
    ),
    dict(
        level=4,
        question="Bir öğrenci 3, 6, 9, 12 örüntüsü için “her terim bir öncekinin 2 katıdır” kuralını söylemiştir. Bu kural neden yanlıştır?",
        choices=[
            "Örüntülerde çarpma içeren kural kullanılamaz.",
            "Yalnız ilk iki terimi açıklar; üçüncü terimi 12, dördüncüyü 24 verir ve örüntüye uymaz.",
            "Kural doğrudur; öğrenci yalnız kuralı eksik yazmıştır.",
            "Örüntüde yeterince terim verilmediği için hiçbir kural bulunamaz.",
        ],
        correct=1,
        distractorWhy=[
            "Çarpma içeren kurallar örüntülerde kullanılabilir; sorun kuralın türünde değil, terimleri açıklamamasındadır.",
            "doğru",
            "Kural üçüncü terimden itibaren tutmadığı için doğru sayılamaz; eksiklik yazımda değil kuralın kendisindedir.",
            "Dört terim bir kuralı sınamak için yeterlidir; nitekim her terime 3 eklendiği görülebilir.",
        ],
        explanation="Bir kural, verilen bütün terimleri açıklamalıdır. İki katı kuralı 3'ten sonra 6 verir "
                    "ve ilk iki terimi tutturur; ancak üçüncü terimi 12 verir, oysa örüntüde 9 yazılıdır. "
                    "Doğru kural her terime 3 eklenmesidir.",
        difficultyReason="4 adım; ön bilgi: kuralın bütün terimlerle sınanması ilkesi; çeldiriciler yakın (kuralı kısmen doğru sayma); beceri: hata teşhisi; akıl yürütme",
        hints=[
            "Öğrencinin söylediği kuralı ilk terime uygula ve ikinci terimi bul.",
            "Aynı kuralı bir kez daha uygulayıp üçüncü terimi bul.",
            "Bulduğun terimi örüntüdeki gerçek terimle karşılaştır.",
            "Bir kuralın kaç terimi açıklaması gerektiğine karar ver.",
            "Tam çözüm: iki katı kuralı ilk iki terimi tutturur ama üçüncü terimi 12 verir; örüntüde 9 yazılı olduğu için kural yanlıştır. Doğru kural her terime 3 eklenmesidir.",
        ],
    ),
    dict(
        level=5,
        question="5, 11, 17, 23, … örüntüsünde 23'ten sonra gelen iki terim sırasıyla hangileridir?",
        choices=[
            "29 ve 34",
            "28 ve 33",
            "29 ve 35",
            "30 ve 37",
        ],
        correct=2,
        distractorWhy=[
            "İlk adımda 6, ikinci adımda 5 eklemiş; artış her adımda aynı kalmalıdır.",
            "Artışı 6 yerine 5 almış.",
            "doğru",
            "Artışı 6 yerine 7 almış.",
        ],
        explanation="Ardışık terimlerin farkı 6'dır: 11 − 5 = 6, 17 − 11 = 6, 23 − 17 = 6. "
                    "Sonraki iki terim 23 + 6 = 29 ve 29 + 6 = 35 olur.",
        difficultyReason="5 adım; ön bilgi: sabit artışın iki adım ileriye taşınması; çeldiriciler çok yakın (artışı bir birim şaşırma ya da adımda değiştirme); beceri: örüntü genelleme",
        hints=[
            "Ardışık terimler arasındaki farkları hesapla ve sabit olduğunu doğrula.",
            "Bu farkı son terime bir kez ekle.",
            "Çıkan sayıya aynı farkı bir kez daha ekle.",
            "Seçeneklerde iki terim arasındaki farkın da aynı kalıp kalmadığını kontrol et.",
            "Tam çözüm: fark 6'dır; 23 + 6 = 29 ve 29 + 6 = 35 bulunur.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# MAT.5.2.4 — note.04 "Aritmetik işlem algoritmalarını yorumlama"
# ---------------------------------------------------------------------------

A24 = [
    dict(
        level=1,
        question="Girdi 12: önce 4 ile çarp, sonra 4 ekle. Algoritmanın çıktısı kaçtır?",
        dogru=12 * 4 + 4,
        celdiriciler=[
            ((12 + 4) * 4, "Adımları ters sırada uygulamış: önce eklemiş, sonra çarpmış."),
            (12 * 4, "İkinci adımı yapmamış; yalnız çarpma sonucunu yazmış."),
            (12 + 4 + 4, "Çarpma yerine toplama yapmış."),
        ],
        explanation="Adımlar sırayla uygulanır: 12 × 4 = 48; bu sonuç ikinci adımın girdisi olur ve "
                    "48 + 4 = 52 bulunur.",
        difficultyReason="2 adım; ön bilgi: her adımın çıktısının sonraki adımın girdisi olması; çeldiriciler yakın (adım sırasını değiştirme); beceri: algoritma izleme",
        hints=[
            "Algoritmanın kaç adımdan oluştuğunu say.",
            "Birinci adımı girdiye uygula ve sonucu yaz.",
            "Bu sonucun ikinci adımın girdisi olduğunu hatırla.",
            "İkinci adımı bu yeni sayıya uygula.",
            "Tam çözüm: 12 × 4 = 48 bulunur, ardından 48 + 4 = 52 elde edilir.",
        ],
    ),
    dict(
        level=2,
        question="A algoritması girdiye önce 5 ekler, sonra 3 ile çarpar. B algoritması girdiyi önce 3 ile çarpar, sonra 5 ekler. Girdi 6 için iki algoritma karşılaştırıldığında ne söylenir?",
        choices=[
            "A'nın çıktısı 33, B'nin çıktısı 23'tür; adımların sırası sonucu değiştirir.",
            "İkisinin de çıktısı 33'tür; aynı sayılar kullanıldığı için sonuç aynıdır.",
            "A'nın çıktısı 23, B'nin çıktısı 33'tür; sıra sonucu ters çevirir.",
            "İkisinin de çıktısı 23'tür; çarpma her durumda önce yapılır.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "B algoritmasında çarpma önce yapıldığı için çıktısı 23 olur; iki sonuç aynı değildir.",
            "Sonuçlar ters eşleştirilmiş: toplamayı önce yapan A daha büyük çıktı verir.",
            "A algoritmasında toplama önce yapılır; adımların sırasını algoritma belirler, işlem önceliği değil.",
        ],
        explanation="A: (6 + 5) × 3 = 11 × 3 = 33. B: 6 × 3 + 5 = 18 + 5 = 23. "
                    "Aynı sayılar kullanılsa bile adımların sırası değiştiğinde farklı bir algoritma ve "
                    "farklı bir sonuç oluşur.",
        difficultyReason="3 adım; ön bilgi: adım sırasının algoritmayı ve sonucu değiştirmesi; çeldiriciler yakın (sonuçları ters eşleştirme); beceri: algoritma izleme; karşılaştırma",
        hints=[
            "İki algoritmayı ayrı ayrı, adım adım izle.",
            "A'da hangi işlemin önce geldiğini belirleyip çıktıyı hesapla.",
            "B'de hangi işlemin önce geldiğini belirleyip çıktıyı hesapla.",
            "İki çıktıyı karşılaştırıp sıranın etkili olup olmadığına karar ver.",
            "Tam çözüm: A için (6 + 5) × 3 = 33, B için 6 × 3 + 5 = 23 bulunur; adım sırası sonucu değiştirir.",
        ],
    ),
    dict(
        level=3,
        question="Bir algoritma girdiyi 3 ile çarpıp sonuca 6 ekliyor. Çıktı 36 ise girdi kaçtır?",
        dogru=(36 - 6) // 3,
        celdiriciler=[
            (36 - 6, "Yalnız ekleme adımını geri almış; çarpmayı geri almamış."),
            (36 // 3 - 6, "Adımları ters sırada geri almış: önce 3'e bölüp sonra 6 çıkarmış."),
            ((36 + 6) // 3, "Geri alırken çıkarma yerine toplama yapmış."),
        ],
        explanation="Girdiyi bulmak için adımlar ters sırada ve ters işlemlerle geri alınır: "
                    "önce 36 − 6 = 30, sonra 30 ÷ 3 = 10.",
        difficultyReason="4 adım; ön bilgi: ters işlemle geriye çalışma ve adımların ters sırada geri alınması; çeldiriciler yakın (sırayı ya da işlemi şaşırma); beceri: akıl yürütme; hesaplama",
        hints=[
            "Algoritmanın adımlarını sırayla yaz.",
            "Geriye giderken hangi adımdan başlanacağını düşün.",
            "Her adımın ters işlemini belirle: toplamanın tersi çıkarma, çarpmanın tersi bölme.",
            "Ters işlemleri son adımdan başlayarak uygula.",
            "Tam çözüm: 36 − 6 = 30 bulunur, ardından 30 ÷ 3 = 10 elde edilir; girdi 10'dur.",
        ],
    ),
    dict(
        level=3,
        question="Bir algoritma şöyledir: sayı tek ise 3 ile çarp ve 1 ekle; çift ise 2'ye böl. Girdi 7 için çıktı kaçtır?",
        dogru=3 * 7 + 1,
        celdiriciler=[
            (3 * 7, "Koşulun seçtiği yolu doğru bulmuş ama ikinci adımı yapmamış."),
            ((7 + 1) * 3, "Yolun adımlarını ters sırada uygulamış: önce 1 eklemiş, sonra çarpmış."),
            (7 + 1, "Çarpma adımını atlamış; yalnız 1 eklemiş."),
        ],
        explanation="7 tek sayıdır, bu yüzden tek sayılar için tanımlanan yol izlenir: "
                    "3 × 7 = 21 ve 21 + 1 = 22. Koşullu algoritmada iki yol birden uygulanmaz.",
        difficultyReason="3 adım; ön bilgi: koşullu adımda yalnız bir yolun izlenmesi; çeldiriciler yakın (yolun adımlarını atlama ya da ters uygulama); beceri: algoritma izleme",
        hints=[
            "Önce girdinin koşulu sağlayıp sağlamadığını kontrol et.",
            "Koşulun sonucuna göre hangi yolun izleneceğine karar ver.",
            "Yalnız o yoldaki adımları sırayla uygula.",
            "Diğer yolu hiç uygulamadığını doğrula.",
            "Tam çözüm: 7 tek olduğu için tek yolu izlenir; 3 × 7 = 21 ve 21 + 1 = 22 bulunur.",
        ],
    ),
    dict(
        level=4,
        question="Bir algoritma şöyledir: sayı 20'den küçükse 3 ile çarp, değilse 5 çıkar. Girdi 20 için çıktı kaçtır?",
        dogru=20 - 5,
        celdiriciler=[
            (20 * 3, "Koşulu yanlış okumuş; 20 sayısı 20'den küçük olmadığı için çarpma yolu seçilmez."),
            (20 + 5, "Doğru yolu seçmiş ama çıkarma yerine toplama yapmış."),
            (20 * 3 - 5, "İki yolu birden uygulamış; koşullu algoritmada yalnız bir yol izlenir."),
        ],
        explanation="20 sayısı 20'den küçük değildir, bu yüzden koşul sağlanmaz ve ikinci yol izlenir: "
                    "20 − 5 = 15.",
        difficultyReason="4 adım; ön bilgi: eşitlik durumunda 'küçüktür' koşulunun sağlanmaması; çeldiriciler çok yakın (sınır değerde koşulu yanlış okuma); beceri: koşul değerlendirme",
        hints=[
            "Koşulun tam olarak ne dediğini kelimesi kelimesine oku.",
            "Girdinin koşulu sağlayıp sağlamadığına karar ver; sınır değere dikkat et.",
            "Koşul sağlanmıyorsa hangi yolun izleneceğini belirle.",
            "Yalnız o yoldaki işlemi uygula.",
            "Tam çözüm: 20 sayısı 20'den küçük olmadığı için koşul sağlanmaz; ikinci yol izlenir ve 20 − 5 = 15 bulunur.",
        ],
    ),
    dict(
        level=2,
        question="Girdi 9: önce 2 ile çarp, sonra 6 ekle, sonra 3'e böl. Algoritmanın çıktısı kaçtır?",
        dogru=(9 * 2 + 6) // 3,
        celdiriciler=[
            (9 * 2 + 6 // 3, "Son adımı yalnız en son eklenen sayıya uygulamış; bölme, o ana kadarki sonuca uygulanır."),
            ((9 + 6) * 2 // 3, "Adımların sırasını değiştirmiş: önce toplama yapmış."),
            (9 * 2 + 6, "Üçüncü adımı hiç yapmamış."),
        ],
        explanation="Her adımın çıktısı sonraki adımın girdisidir: 9 × 2 = 18, 18 + 6 = 24, 24 ÷ 3 = 8.",
        difficultyReason="3 adım; ön bilgi: üç adımlı algoritmada her adımın bir öncekinin sonucuna uygulanması; çeldiriciler yakın (adımı yanlış sayıya uygulama); beceri: algoritma izleme",
        hints=[
            "Algoritmanın üç adımdan oluştuğunu fark et.",
            "Birinci adımı uygulayıp ara sonucu yaz.",
            "İkinci adımı bu ara sonuca uygula.",
            "Üçüncü adımı, ikinci adımdan çıkan sayının tamamına uygula.",
            "Tam çözüm: 9 × 2 = 18, 18 + 6 = 24, 24 ÷ 3 = 8 bulunur.",
        ],
    ),
    dict(
        level=3,
        question="Bir öğrenci “girdi 8: önce 5 ekle, sonra 4 ile çarp” algoritmasının çıktısını 37 bulmuştur. Öğrencinin hatası nedir?",
        choices=[
            "Adımları ters sırada uygulamıştır; önce toplama yapılmalı ve çıktı 52 olmalıdır.",
            "Çarpma yerine bölme yapmıştır; çıktı 7 olmalıdır.",
            "İkinci adımı atlamıştır; çıktı 13 olmalıdır.",
            "Girdiyi yanlış almıştır; bulduğu 37 sonucu doğrudur.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Algoritmada bölme adımı yoktur; işlem türünü değiştirmek hatanın kaynağı değildir.",
            "Öğrenci ikinci adımı yapmıştır; 37 sayısı 8 × 4 = 32 sonucuna 5 eklenmesiyle çıkmıştır.",
            "Girdi soruda açıkça verilmiştir; ayrıca doğru sıra izlendiğinde 37 sonucu elde edilmez.",
        ],
        explanation="Algoritma önce toplamayı gerektirir: (8 + 5) × 4 = 13 × 4 = 52. Öğrenci ise önce "
                    "çarpıp sonra eklemiş, yani 8 × 4 + 5 = 37 bulmuştur.",
        difficultyReason="4 adım; ön bilgi: adım sırasının sonucu değiştirmesi ve öğrenci yolunun geri çözülmesi; çeldiriciler yakın (başka bir hata türü önerme); beceri: hata teşhisi",
        hints=[
            "Algoritmayı doğru sırayla uygulayıp kendi sonucunu bul.",
            "Öğrencinin bulduğu sayıya hangi adımlarla ulaşılabileceğini dene.",
            "İki yolu yan yana yazıp nerede ayrıldıklarına bak.",
            "Ayrılmanın adım sırasından mı işlem türünden mi kaynaklandığına karar ver.",
            "Tam çözüm: doğru sıra (8 + 5) × 4 = 52 verir. Öğrenci 8 × 4 + 5 = 37 yaparak adımları ters sırada uygulamıştır.",
        ],
    ),
    dict(
        level=4,
        question="Bir algoritmada girdi 3 iken çıktı 11, girdi 5 iken çıktı 17, girdi 8 iken çıktı 26 olmaktadır. Algoritmanın kuralı hangisidir?",
        choices=[
            "Girdiye 8 ekle.",
            "Girdiyi 3 ile çarp, sonra 2 ekle.",
            "Girdiyi 2 ile çarp, sonra 5 ekle.",
            "Girdiyi 4 ile çarp, sonra 1 çıkar.",
        ],
        correct=1,
        distractorWhy=[
            "Bu kural ilk satırı açıklar ama girdi 5 için 13 verir; oysa tabloda 17 yazılıdır.",
            "doğru",
            "Bu kural ilk satırı açıklar ama girdi 5 için 15 verir; oysa tabloda 17 yazılıdır.",
            "Bu kural ilk satırı açıklar ama girdi 5 için 19 verir; oysa tabloda 17 yazılıdır.",
        ],
        explanation="Bir kural, tablodaki bütün satırları açıklamalıdır. “3 ile çarp, 2 ekle” kuralı "
                    "3 → 11, 5 → 17 ve 8 → 26 satırlarının üçünü de verir; diğer üç kural yalnız ilk "
                    "satırı tutturur.",
        difficultyReason="4 adım; ön bilgi: kuralın bütün girdi-çıktı çiftleriyle sınanması; çeldiriciler çok yakın (üçü de ilk satırı açıklıyor); beceri: kural sınama; akıl yürütme",
        hints=[
            "Tablodaki üç satırı ayrı ayrı ele al.",
            "Her seçenekteki kuralı ilk girdiye uygulayıp çıktıyı tahmin et.",
            "İlk satırı tutturan seçeneklerde ikinci satırı da dene.",
            "Bütün satırları açıklamayan kuralları ele.",
            "Tam çözüm: 3 × 3 + 2 = 11, 5 × 3 + 2 = 17 ve 8 × 3 + 2 = 26'dır; yalnız bu kural üç satırı da açıklar.",
        ],
    ),
    dict(
        level=5,
        question="Bir algoritmanın çıktısını doğrulamanın en güvenilir yolu nedir?",
        choices=[
            "Aynı adımları bir kez daha aynı sırada uygulamak.",
            "Çıktının tek mi çift mi olduğuna bakmak.",
            "Adımları ters işlemlerle geriye doğru uygulayıp girdiye ulaşmak.",
            "Girdiyi büyütüp çıktının da büyüdüğünü görmek.",
        ],
        correct=2,
        distractorWhy=[
            "Aynı yol tekrarlandığında aynı hata da tekrarlanır; bu yöntem yanlışı ortaya çıkarmaz.",
            "Tek-çift kontrolü kaba bir işarettir; doğru büyüklükteki yanlış bir sonucu yakalamaz.",
            "doğru",
            "Çıktının büyümesi kuralın yönünü gösterir ama sayının doğruluğunu kanıtlamaz.",
        ],
        explanation="Aritmetik bir algoritmayı kontrol etmenin en güçlü yolu ters işlemlerle geriye "
                    "gitmektir: çıktıdan başlanıp her adım ters işlemiyle geri alınır. Başlangıçtaki "
                    "girdiye ulaşılıyorsa çıktı doğrudur.",
        difficultyReason="3 adım; ön bilgi: ters işlemle doğrulamanın diğer kontrol yollarından üstünlüğü; çeldiriciler yakın (kısmi kontrol yolları); beceri: yöntem değerlendirme",
        hints=[
            "Bir hatayı yakalamak için aynı yolu tekrarlamanın yeterli olup olmadığını düşün.",
            "Her işlemin bir ters işlemi olduğunu hatırla.",
            "Çıktıdan başlayıp geriye gidersen nereye ulaşman gerektiğini söyle.",
            "Yalnız bir özelliğe bakan kontrol yollarının ne kadar güvenilir olduğunu değerlendir.",
            "Tam çözüm: adımlar ters işlemlerle geriye alınır; başlangıç girdisine ulaşılıyorsa çıktı doğrulanmış olur.",
        ],
    ),
    dict(
        level=1,
        question="Girdi 15: önce 2 ile çarp, sonra 6 ekle. Algoritmanın çıktısı kaçtır?",
        dogru=15 * 2 + 6,
        celdiriciler=[
            ((15 + 6) * 2, "Adımları ters sırada uygulamış: önce eklemiş, sonra çarpmış."),
            (15 * 2, "İkinci adımı yapmamış."),
            (15 + 2 + 6, "Çarpma yerine toplama yapmış."),
        ],
        explanation="Adımlar sırayla uygulanır: 15 × 2 = 30 ve 30 + 6 = 36.",
        difficultyReason="2 adım; ön bilgi: iki adımlı algoritmanın sırayla izlenmesi; çeldiriciler yakın (sıra değiştirme); beceri: algoritma izleme",
        hints=[
            "Algoritmanın adımlarını sırayla numaralandır.",
            "Birinci adımı girdiye uygula.",
            "Çıkan sonucu ikinci adımın girdisi olarak kullan.",
            "İkinci adımı uygulayıp çıktıyı yaz.",
            "Tam çözüm: 15 × 2 = 30 bulunur, ardından 30 + 6 = 36 elde edilir.",
        ],
    ),
    dict(
        level=2,
        question="Bir akış şemasındaki oklar sırasıyla “girdiyi al → 7 ile çarp → 10 çıkar → çıktıyı yaz” adımlarını göstermektedir. Girdi 6 için çıktı kaçtır?",
        dogru=6 * 7 - 10,
        celdiriciler=[
            (6 * 7, "Çıkarma adımını atlayıp doğrudan çıktıya geçmiş."),
            (6 * 7 + 10, "Çıkarma yerine toplama yapmış."),
            (6 + 7 - 10 + 10, "Çarpma yerine toplama yapmış ve çıkarma adımını da uygulamamış."),
        ],
        explanation="Oklar adımların sırasını gösterir: 6 × 7 = 42, ardından 42 − 10 = 32. "
                    "“Çıktıyı yaz” bir işlem değil, sonucun bildirilmesidir.",
        difficultyReason="2 adım; ön bilgi: akış gösteriminde okların adım sırasını belirtmesi; çeldiriciler yakın (adım atlama); beceri: akış okuma; hesaplama",
        hints=[
            "Okların hangi yönde okunduğunu belirle.",
            "İşlem içeren adımları, bilgi veren adımlardan ayır.",
            "Birinci işlem adımını girdiye uygula.",
            "Sonucu ikinci işlem adımına taşı.",
            "Tam çözüm: 6 × 7 = 42 bulunur, ardından 42 − 10 = 32 elde edilir.",
        ],
    ),
    dict(
        level=4,
        question="A algoritması girdiyi 2 ile çarpıp 6 ekler. B algoritması girdiye 3 ekleyip 2 ile çarpar. Girdi 4 için bu iki algoritma karşılaştırıldığında ne söylenir?",
        choices=[
            "İkisinin de çıktısı 14'tür; 2 × (girdi + 3) ile 2 × girdi + 6 ifadeleri dağılma özelliğine göre eşittir.",
            "İkisinin de çıktısı 14'tür ama bu yalnız 4 girdisine özgü bir rastlantıdır.",
            "A'nın çıktısı 14, B'nin çıktısı 11'dir; adımların sırası sonucu değiştirir.",
            "A'nın çıktısı 8, B'nin çıktısı 14'tür; A'da ikinci adım sonucu değiştirmez.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Dağılma özelliği gereği iki ifade her girdi için eşittir; eşitlik bu girdiye özgü bir rastlantı değildir.",
            "B algoritmasında önce toplama yapılır ve sonuç 2 × 7 = 14 olur; iki çıktı eşittir.",
            "A algoritmasında ikinci adımda 6 eklenir ve sonuç 14 olur; bu adım atlanamaz.",
        ],
        explanation="A: 4 × 2 + 6 = 8 + 6 = 14. B: (4 + 3) × 2 = 7 × 2 = 14. Adım sıraları farklı olsa da "
                    "2 × (girdi + 3) ifadesi dağılma özelliğiyle 2 × girdi + 6 hâline geldiği için iki "
                    "algoritma her girdi için aynı çıktıyı verir.",
        difficultyReason="5 adım; ön bilgi: farklı adım sıralarının dağılma özelliği sayesinde denk olabilmesi; çeldiriciler çok yakın (eşitliği rastlantı sayma); beceri: akıl yürütme; genelleme",
        hints=[
            "İki algoritmayı verilen girdi için ayrı ayrı hesapla.",
            "Çıktıların eşit çıkıp çıkmadığına bak.",
            "Eşitse bunun her girdi için geçerli olup olmadığını sorgula.",
            "B'nin adımlarını bir çarpım ifadesi gibi yazıp parantezi açmayı dene.",
            "Tam çözüm: A için 4 × 2 + 6 = 14, B için (4 + 3) × 2 = 14 bulunur. Parantez açılınca 2 × girdi + 6 elde edildiği için eşitlik her girdi için geçerlidir.",
        ],
    ),
    dict(
        level=4,
        question="Bir algoritma girdiyi 5 ile çarpıp sonuçtan 3 çıkarıyor. Çıktı 47 ise girdi kaçtır?",
        dogru=(47 + 3) // 5,
        celdiriciler=[
            (47 + 3, "Yalnız çıkarma adımını geri almış; bölmeyi yapmamış."),
            (47 * 5 - 3, "Geriye gitmek yerine algoritmayı çıktıya bir kez daha uygulamış."),
            (47 - 3, "Geri alırken çıkarmanın tersini almamış; 3'ü bir kez daha çıkarmış."),
        ],
        explanation="Adımlar ters sırada ve ters işlemlerle geri alınır: önce 47 + 3 = 50, "
                    "sonra 50 ÷ 5 = 10. Girdi 10'dur.",
        difficultyReason="4 adım; ön bilgi: ters işlemle geriye çalışma; çeldiriciler yakın (ara sonucu yanıt sanma, ters işlemi şaşırma); beceri: akıl yürütme; hesaplama",
        hints=[
            "Algoritmanın adımlarını sırayla yazıp son adımı işaretle.",
            "Geriye giderken son adımdan başlanacağını hatırla.",
            "Çıkarmanın tersinin ne olduğunu belirle.",
            "İkinci olarak çarpmanın tersini uygula.",
            "Tam çözüm: 47 + 3 = 50 bulunur, ardından 50 ÷ 5 = 10 elde edilir.",
        ],
    ),
    dict(
        level=2,
        question="Girdi 7: önce 6 ile çarp, sonra 13 ekle. Algoritmanın çıktısı kaçtır?",
        dogru=7 * 6 + 13,
        celdiriciler=[
            ((7 + 13) * 6, "Adımları ters sırada uygulamış: önce eklemiş, sonra çarpmış."),
            (7 * 6, "İkinci adımı yapmamış."),
            (7 + 6 + 13, "Çarpma yerine toplama yapmış."),
        ],
        explanation="Adımlar sırayla uygulanır: 7 × 6 = 42 ve 42 + 13 = 55.",
        difficultyReason="2 adım; ön bilgi: iki adımlı algoritmanın sırayla izlenmesi; çeldiriciler yakın (sıra değiştirme); beceri: algoritma izleme",
        hints=[
            "Adımları sırayla numaralandır.",
            "Birinci adımı girdiye uygula.",
            "Ara sonucu bir kenara yaz.",
            "İkinci adımı bu ara sonuca uygula.",
            "Tam çözüm: 7 × 6 = 42 bulunur, ardından 42 + 13 = 55 elde edilir.",
        ],
    ),
    dict(
        level=5,
        question="Bir algoritma “sayıyı 2 ile çarp” adımını 3 kez tekrarlamaktadır. Girdi 5 için çıktı kaçtır?",
        dogru=5 * 2 * 2 * 2,
        celdiriciler=[
            (5 * 2 * 3, "Tekrar sayısını çarpan sanmış: 5 × 2 × 3."),
            (5 * 2, "Adımı yalnız bir kez uygulamış."),
            (5 + 2 + 2 + 2, "Çarpma yerine toplama yapmış."),
        ],
        explanation="Adım her tekrarda bir önceki sonuca uygulanır: 5 × 2 = 10, 10 × 2 = 20, 20 × 2 = 40.",
        difficultyReason="4 adım; ön bilgi: tekrarlanan adımın her seferinde bir önceki sonuca uygulanması; çeldiriciler yakın (tekrar sayısını çarpan sanma); beceri: algoritma izleme",
        hints=[
            "Adımın kaç kez tekrarlanacağını belirle.",
            "İlk tekrarı girdiye uygula ve sonucu yaz.",
            "İkinci tekrarı bu yeni sonuca uygula.",
            "Üçüncü tekrarı da bir önceki sonuca uygulamayı unutma.",
            "Tam çözüm: 5 × 2 = 10, 10 × 2 = 20, 20 × 2 = 40 bulunur.",
        ],
    ),
    dict(
        level=3,
        question="Bir algoritma şöyledir: sayı 10'dan büyükse 10 çıkar, değilse 10 ekle. Girdi 10 için çıktı kaçtır?",
        dogru=10 + 10,
        celdiriciler=[
            (10 - 10, "Koşulu “büyük veya eşit” diye okumuş; 10 sayısı 10'dan büyük değildir."),
            (10, "Koşul sağlanmadığı için hiçbir adımın uygulanmadığını sanmış; oysa ikinci yol izlenir."),
            (10 * 10, "Ekleme yerine çarpma yapmış."),
        ],
        explanation="10 sayısı 10'dan büyük değildir, bu yüzden koşul sağlanmaz ve ikinci yol izlenir: "
                    "10 + 10 = 20.",
        difficultyReason="3 adım; ön bilgi: sınır değerde 'büyüktür' koşulunun sağlanmaması ve koşul sağlanmadığında ikinci yolun izlenmesi; çeldiriciler çok yakın (sınır değer yorumu); beceri: koşul değerlendirme",
        hints=[
            "Koşulda “büyüktür” mü “büyük veya eşittir” mi yazdığına dikkat et.",
            "Girdinin koşulu sağlayıp sağlamadığına karar ver.",
            "Koşul sağlanmadığında algoritmanın durup durmadığını düşün.",
            "İzlenecek yolu belirleyip işlemi uygula.",
            "Tam çözüm: 10 sayısı 10'dan büyük olmadığı için koşul sağlanmaz; ikinci yol izlenir ve 10 + 10 = 20 bulunur.",
        ],
    ),
    dict(
        level=4,
        question="Bir öğrenci “girdi 24: önce 4'e böl, sonra 2 ile çarp” algoritmasının çıktısını 3 bulmuştur. Öğrencinin hatası nedir?",
        choices=[
            "Bölme adımını atlamıştır; çıktı 48 olmalıdır.",
            "İkinci adımı atlamıştır; çıktı 6 olmalıdır.",
            "İkinci adımdaki çarpmayı bölenin içine katmıştır; çıktı 12 olmalıdır.",
            "Girdiyi 4 ile çarpmalıydı; çıktı 192 olmalıdır.",
        ],
        correct=2,
        distractorWhy=[
            "Öğrenci bölme adımını yapmıştır; hata bölmenin atlanmasında değil, bölenin genişletilmesindedir.",
            "İkinci adım atlansaydı sonuç 6 çıkardı; oysa öğrenci 3 bulmuştur.",
            "doğru",
            "Algoritmada çarpma ikinci adımdadır; girdinin 4 ile çarpılması istenmemektedir.",
        ],
        explanation="Adımlar sırayla uygulanır: 24 ÷ 4 = 6, ardından 6 × 2 = 12. Öğrenci ise 2'yi bölenin "
                    "içine katıp 24 ÷ (4 × 2) = 3 hesaplamıştır.",
        difficultyReason="4 adım; ön bilgi: art arda gelen bölme ve çarpmanın ayrı adımlar olması; çeldiriciler yakın (başka bir hata türü önerme); beceri: hata teşhisi",
        hints=[
            "Algoritmayı adım adım doğru uygulayıp kendi sonucunu bul.",
            "Öğrencinin bulduğu 3 sayısına hangi işlemle ulaşılabileceğini dene.",
            "İki yolu karşılaştırıp 2 sayısının nerede kullanıldığına bak.",
            "İkinci adımın ayrı bir işlem mi yoksa bölenin parçası mı olduğuna karar ver.",
            "Tam çözüm: doğru yol 24 ÷ 4 = 6 ve 6 × 2 = 12'dir. Öğrenci 24 ÷ (4 × 2) = 3 yaparak çarpmayı bölenin içine katmıştır.",
        ],
    ),
    dict(
        level=1,
        question="Girdi 20: önce 5 ile çarp, sonra 4 ekle. Algoritmanın çıktısı kaçtır?",
        dogru=20 * 5 + 4,
        celdiriciler=[
            ((20 + 4) * 5, "Adımları ters sırada uygulamış: önce eklemiş, sonra çarpmış."),
            (20 * 5, "İkinci adımı yapmamış."),
            (20 + 5 + 4, "Çarpma yerine toplama yapmış."),
        ],
        explanation="Adımlar sırayla uygulanır: 20 × 5 = 100 ve 100 + 4 = 104.",
        difficultyReason="2 adım; ön bilgi: iki adımlı algoritmanın sırayla izlenmesi; çeldiriciler yakın (sıra değiştirme); beceri: algoritma izleme",
        hints=[
            "Adımları sırayla numaralandır.",
            "Birinci adımı girdiye uygula.",
            "Ara sonucu yaz.",
            "İkinci adımı ara sonuca uygula.",
            "Tam çözüm: 20 × 5 = 100 bulunur, ardından 100 + 4 = 104 elde edilir.",
        ],
    ),
    dict(
        level=5,
        question="Girdisi 6 iken çıktısı 20 olan algoritma aşağıdakilerden hangisidir?",
        choices=[
            "önce 2 ekle, sonra 3 ile çarp",
            "önce 4 ile çarp, sonra 2 çıkar",
            "önce 2 ile çarp, sonra 6 ekle",
            "önce 3 ile çarp, sonra 2 ekle",
        ],
        correct=3,
        distractorWhy=[
            "Bu algoritma (6 + 2) × 3 = 24 verir; istenen çıktıdan büyüktür.",
            "Bu algoritma 6 × 4 − 2 = 22 verir; istenen çıktıdan büyüktür.",
            "Bu algoritma 6 × 2 + 6 = 18 verir; istenen çıktıdan küçüktür.",
            "doğru",
        ],
        explanation="Seçenekler tek tek denenir: 6 × 3 + 2 = 18 + 2 = 20 olduğundan istenen algoritma "
                    "girdiyi 3 ile çarpıp 2 ekleyendir.",
        difficultyReason="5 adım; ön bilgi: verilen girdi-çıktı çiftine uyan algoritmanın seçilmesi; çeldiriciler çok yakın (dördü de aynı sayılarla kurulmuş); beceri: deneme; algoritma izleme",
        hints=[
            "Her seçeneğin bir algoritma tanımladığını fark et.",
            "İlk seçeneği verilen girdiye uygulayıp çıktısını hesapla.",
            "Aynı işlemi diğer seçenekler için de yap.",
            "Bulduğun çıktıları istenen sayıyla karşılaştır.",
            "Tam çözüm: 6 × 3 + 2 = 20 olduğundan aranan algoritma budur; diğerleri sırasıyla 24, 22 ve 18 verir.",
        ],
    ),
    dict(
        level=2,
        question="Bir algoritma girdiyi 7 ile çarpıp 2 çıkarıyor. Girdiler 4, 6 ve 9 iken çıktılar sırasıyla hangileridir?",
        choices=[
            "26, 40 ve 61",
            "26, 42 ve 63",
            "28, 42 ve 63",
            "30, 44 ve 65",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "İlk çıktıyı doğru bulmuş ama sonraki iki girdide çıkarma adımını atlamış.",
            "Üç girdide de yalnız çarpma yapmış; çıkarma adımını hiç uygulamamış.",
            "Çıkarma yerine toplama yapmış.",
        ],
        explanation="Algoritma her girdiye aynı iki adımı uygular: 4 × 7 − 2 = 26, 6 × 7 − 2 = 40, "
                    "9 × 7 − 2 = 61.",
        difficultyReason="3 adım; ön bilgi: aynı algoritmanın birden çok girdiye uygulanması; çeldiriciler yakın (bazı satırlarda adım atlama); beceri: algoritma izleme; hesaplama",
        hints=[
            "Algoritmanın adımlarını bir kez netçe yaz.",
            "İlk girdiye iki adımı da uygula.",
            "Aynı iki adımı ikinci girdiye uygula.",
            "Üçüncü girdide de her iki adımı uyguladığından emin ol.",
            "Tam çözüm: 4 × 7 − 2 = 26, 6 × 7 − 2 = 40 ve 9 × 7 − 2 = 61 bulunur.",
        ],
    ),
    dict(
        level=3,
        question="Bir algoritmanın adımları şöyledir: 1) girdiyi 3 ile çarp, 2) sonuca 12 ekle, 3) sonucu 3'e böl. Girdi 5 için çıktı kaçtır?",
        dogru=(5 * 3 + 12) // 3,
        celdiriciler=[
            (5 * 3 + 12 // 3, "Üçüncü adımı yalnız eklenen sayıya uygulamış; bölme, ikinci adımdan çıkan sonuca uygulanır."),
            (5 * 3 + 12, "Üçüncü adımı hiç yapmamış."),
            ((5 + 12) * 3 // 3, "Adımların sırasını değiştirmiş: önce toplama yapmış."),
        ],
        explanation="Numaralı yönerge sırayla izlenir: 5 × 3 = 15, 15 + 12 = 27, 27 ÷ 3 = 9.",
        difficultyReason="3 adım; ön bilgi: numaralı yönergede her adımın bir önceki sonucun tamamına uygulanması; çeldiriciler yakın (adımı yanlış sayıya uygulama); beceri: algoritma izleme",
        hints=[
            "Yönergedeki adımların numaralandırıldığını fark et.",
            "Birinci adımı girdiye uygula.",
            "İkinci adımı birinci adımdan çıkan sayıya uygula.",
            "Üçüncü adımı, ikinci adımdan çıkan sayının tamamına uygula.",
            "Tam çözüm: 5 × 3 = 15, 15 + 12 = 27, 27 ÷ 3 = 9 bulunur.",
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
    """Sayısal soruyu şık listesine çevirir; değerler Python'da hesaplanmıştır."""
    if "choices" in s:
        return list(s["choices"]), int(s["correct"]), list(s["distractorWhy"])
    degerler = [s["dogru"]] + [d for d, _ in s["celdiriciler"]]
    assert len(set(degerler)) == 4, f"{s['question']}: şık değerleri benzersiz değil: {degerler}"
    assert all(v >= 0 for v in degerler), f"{s['question']}: negatif şık: {degerler}"
    return [str(v) for v in degerler], 0, ["doğru"] + [g for _, g in s["celdiriciler"]]


AILELER = [
    ("tr.g05.mat.5-2-3", "MAT.5.2.3", "tr.g05.mat.5.2.note.03", "Örüntü kuralını bulma", A23),
    ("tr.g05.mat.5-2-4", "MAT.5.2.4", "tr.g05.mat.5.2.note.04",
     "Aritmetik işlem algoritmalarını yorumlama", A24),
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
