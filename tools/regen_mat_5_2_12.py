# -*- coding: utf-8 -*-
"""A3 parti 4 — MAT.5.2.1 ve MAT.5.2.2 ailelerinin yeniden üretimi.

Önceki hâl:
  5-2-1 (22 soru): iki kalıp dönüşümlü tekrarlanıyordu — 11 kez
    "# + # = # + □ eşitliğinde kutuya hangi sayı yazılmalıdır?" ve 11 kez
    "# × (# + #) işleminin dağılma özelliğine göre sonucu kaçtır?".
    Not dört özellik anlatıyor (eşitliğin korunumu, değişme, birleşme,
    dağılma) ama sorular yalnız ikisine değiyordu; birleşme özelliği ve
    eşitliğin korunumu hiç ölçülmüyordu.
  5-2-2 (21 soru): 21/21 "# + # × # işleminin sonucu kaçtır?". Notun
    anlattığı parantez, bölme, soldan sağa kuralı ve "çarpma her zaman
    bölmeden önce değildir" uyarısı hiç sorulmuyordu.

Yeni hâl: her iki ailede de notun anlattığı bütün alt konular kapsandı.
Sayısal sorularda doğru cevap da çeldiriciler de Python'da hesaplanır:
çeldirici, adlandırılmış yanılgının kendi ifadesinden çıkar (örneğin
"soldan sağa yapmış" çeldiricisi (51+3)*4 ifadesinin değeridir). Böylece
gerekçedeki iddia makineyle doğrulanabilir kalır.

choices + correct + distractorWhy + hints + explanation tek birimde üretildi
(AUTHORING_RULES.md §1 atomiklik ilkesi).
"""

KAYNAK = "https://tymm.meb.gov.tr/upload/program/2024programmat5678Onayli.pdf"


def S(x):
    """Sayıyı şık metnine çevirir."""
    return str(x)


# ---------------------------------------------------------------------------
# MAT.5.2.1 — note.01 "Eşitliğin korunumu, değişme, birleşme ve dağılma"
# ---------------------------------------------------------------------------
# sayisal(...) : doğru değer + (değer, gerekçe) çiftleri
# sozel(...)   : şıkların tamamı metin

A21 = [
    dict(
        level=1,
        question="17 + 9 = 9 + □ eşitliğinde kutuya hangi sayı yazılmalıdır?",
        dogru=17,
        celdiriciler=[
            (17 + 9, "İki tarafı toplayıp sonucu kutuya yazmış; eşitlik işareti “sonuç geliyor” demek değildir."),
            (9, "Kutunun karşısındaki sayıyı yeniden yazmış; yer değiştiren sayı 17'dir."),
            (17 - 9, "İki sayının farkını almış: 17 − 9 = 8."),
        ],
        explanation="Toplamada değişme özelliği vardır: sayıların yeri değişse de toplam aynı kalır. "
                    "Sol tarafta 17 ile 9 toplanmıştır; sağ tarafta 9 zaten yazılı olduğuna göre kutuya 17 gelir.",
        difficultyReason="1 adım; ön bilgi: toplamada değişme özelliği; çeldiriciler yakın (eşitliği sonuç sanma); beceri: özellik tanıma",
        hints=[
            "Eşitlik işaretinin iki tarafın aynı değeri taşıdığını bildirdiğini hatırla.",
            "Eşitliğin iki tarafında hangi sayıların ortak olduğuna bak.",
            "Sol taraftaki sayılardan hangisinin sağ tarafta henüz yazılmadığını bul.",
            "Toplamada sayıların yerinin değişmesinin sonucu değiştirip değiştirmediğini düşün.",
            "Tam çözüm: sol tarafta 17 ve 9 vardır, sağ tarafta 9 yazılıdır. Değişme özelliği gereği kutuya 17 gelir ve iki taraf da 26 eder.",
        ],
    ),
    dict(
        level=1,
        question="6 × 13 = □ × 6 eşitliğinde kutuya hangi sayı gelmelidir?",
        dogru=13,
        celdiriciler=[
            (6 * 13, "Çarpımın sonucunu kutuya yazmış; eşitliğin sağ tarafı henüz çarpılmamış bir ifadedir."),
            (6, "Kutunun karşısındaki sayıyı yeniden yazmış; yer değiştiren çarpan 13'tür."),
            (13 - 6, "İki çarpanın farkını almış: 13 − 6 = 7."),
        ],
        explanation="Çarpmada da değişme özelliği vardır: çarpanların yeri değişse de çarpım aynı kalır. "
                    "6 × 13 ile 13 × 6 eşit olduğundan kutuya 13 yazılır.",
        difficultyReason="1 adım; ön bilgi: çarpmada değişme özelliği; çeldiriciler yakın (çarpımı yanıt sanma); beceri: özellik tanıma",
        hints=[
            "Çarpmada çarpanların yerinin değişmesinin sonucu etkileyip etkilemediğini hatırla.",
            "Eşitliğin iki tarafındaki ortak çarpanı işaretle.",
            "Sol tarafta olup sağ tarafta yazılmayan çarpanı bul.",
            "Kutuya yazacağın sayının bir çarpan mı yoksa bir çarpım mı olduğuna karar ver.",
            "Tam çözüm: 6 × 13 ile 13 × 6 aynı değeri verir; sağ tarafta 6 yazılı olduğuna göre kutuya 13 gelir.",
        ],
    ),
    dict(
        level=2,
        question="(38 + 25) + 15 toplamını zihinden kolay hesaplamak için hangi gruplama seçilir?",
        choices=["38 + (25 + 15)", "(38 + 25) × 15", "38 × (25 + 15)", "(38 − 25) + 15"],
        correct=0,
        distractorWhy=[
            "doğru",
            "Toplama işlemini çarpmaya çevirmiş; gruplama işlemin türünü değiştiremez.",
            "Parantezin dışındaki toplamayı çarpmaya çevirmiş; birleşme özelliği yalnız gruplamayı değiştirir.",
            "Toplamayı çıkarmaya çevirmiş; çıkarmada birleşme özelliği zaten yoktur.",
        ],
        explanation="Toplamada birleşme özelliği, üç sayının farklı biçimde gruplanabileceğini söyler. "
                    "25 + 15 = 40 kolay bir toplam olduğu için 38 + (25 + 15) = 38 + 40 = 78 zihinden yapılabilir.",
        difficultyReason="2 adım; ön bilgi: toplamada birleşme özelliğinin işlemi değil gruplamayı değiştirmesi; çeldiriciler yakın (işlem türünü değiştirme); beceri: özellik seçme",
        hints=[
            "Birleşme özelliğinin neyi değiştirmeye izin verdiğini hatırla: işlemi mi, gruplamayı mı?",
            "Seçeneklerdeki işlem işaretlerini soruyla karşılaştır.",
            "İşlem türünü değiştiren seçenekleri ele.",
            "Kalan seçenekte parantez içindeki toplamın kolay bir sayı verip vermediğine bak.",
            "Tam çözüm: birleşme özelliği yalnız gruplamayı değiştirir. 38 + (25 + 15) yazılınca parantez içi 40 olur ve toplam 78 diye kolayca bulunur.",
        ],
    ),
    dict(
        level=2,
        question="25 × 7 × 4 çarpımını zihinden kolay hesaplamak için hangi gruplama seçilir?",
        choices=["(25 × 7) + 4", "(25 × 4) × 7", "(25 + 4) × 7", "25 × (7 + 4)"],
        correct=1,
        distractorWhy=[
            "Son çarpmayı toplamaya çevirmiş; gruplama işlemin türünü değiştiremez.",
            "doğru",
            "İlk çarpmayı toplamaya çevirmiş; birleşme özelliği yalnız parantezin yerini değiştirir.",
            "Parantez içindeki çarpmayı toplamaya çevirmiş; sonuç 25 × 11 olur ve ilk ifadeye eşit değildir.",
        ],
        explanation="Çarpmada birleşme özelliği çarpanların farklı gruplanmasına izin verir. "
                    "25 × 4 = 100 kolay bir çarpım olduğundan (25 × 4) × 7 = 100 × 7 = 700 zihinden yapılabilir.",
        difficultyReason="2 adım; ön bilgi: çarpmada birleşme özelliği ve kolay çarpan eşleştirme; çeldiriciler yakın (işlem türünü değiştirme); beceri: özellik seçme",
        hints=[
            "Üç çarpandan hangi ikisinin çarpımının yuvarlak bir sayı verdiğini ara.",
            "Birleşme özelliğinin işlem işaretini değiştirmediğini hatırla.",
            "İçinde toplama işareti bulunan seçenekleri ele.",
            "Kalan seçenekte parantez içinin kaç ettiğine bak.",
            "Tam çözüm: 25 × 4 = 100 olduğundan (25 × 4) × 7 = 100 × 7 = 700 zihinden bulunur.",
        ],
    ),
    dict(
        level=2,
        question="5 × (48 + 4) işleminin sonucu dağılma özelliği kullanılarak kaç bulunur?",
        dogru=5 * (48 + 4),
        celdiriciler=[
            (5 * 48 + 4, "Yalnız ilk terimi çarpmış, ikinci terimi olduğu gibi eklemiş: 5 × 48 + 4."),
            (5 * 48, "Parantez içindeki ikinci terimi hiç kullanmamış: yalnız 5 × 48 hesaplanmış."),
            (5 + 48 * 4, "Çarpanı parantezin ilk terimiyle toplayıp ikinci terimle çarpmış: 5 + 48 × 4."),
        ],
        explanation="Dağılma özelliğinde çarpan, parantez içindeki her terimle ayrı ayrı çarpılır: "
                    "5 × 48 + 5 × 4 = 240 + 20 = 260.",
        difficultyReason="2 adım; ön bilgi: çarpmanın toplama üzerine dağılması; çeldiriciler yakın (ikinci terimi çarpmayı unutma); beceri: hesaplama",
        hints=[
            "Dağılma özelliğinde çarpanın kaç terimle çarpılacağını hatırla.",
            "Parantez içindeki terimleri tek tek işaretle.",
            "Çarpanı her terimin üzerine ayrı ayrı dağıt.",
            "Elde ettiğin iki çarpımı toplamayı dene.",
            "Tam çözüm: 5 × 48 = 240 ve 5 × 4 = 20 bulunur; toplam 240 + 20 = 260 eder.",
        ],
    ),
    dict(
        level=3,
        question="8 × (50 − 3) işleminin sonucu dağılma özelliği kullanılarak kaç bulunur?",
        dogru=8 * (50 - 3),
        celdiriciler=[
            (8 * 50 - 3, "Yalnız ilk terimi çarpmış, 3'ü olduğu gibi çıkarmış: 8 × 50 − 3."),
            (8 * 50 + 8 * 3, "Çıkarma yerine toplama dağıtmış: 8 × 50 + 8 × 3."),
            (8 * 50, "Parantezin ikinci terimini hiç kullanmamış: yalnız 8 × 50 hesaplanmış."),
        ],
        explanation="Çarpma, çıkarma üzerine de dağılır ve işaret korunur: "
                    "8 × 50 − 8 × 3 = 400 − 24 = 376.",
        difficultyReason="3 adım; ön bilgi: çarpmanın çıkarma üzerine dağılması ve işaretin korunması; çeldiriciler yakın (işaret değiştirme); beceri: hesaplama",
        hints=[
            "Dağılma özelliğinin yalnız toplamada mı geçerli olduğunu düşün.",
            "Parantez içindeki işlem işaretini not et.",
            "Çarpanı iki terimin de üzerine dağıt.",
            "Dağıtırken parantez içindeki işaretin aynen korunduğunu kontrol et.",
            "Tam çözüm: 8 × 50 = 400 ve 8 × 3 = 24 bulunur; çıkarma korunduğu için sonuç 400 − 24 = 376 olur.",
        ],
    ),
    dict(
        level=3,
        question="7 × 26 + 7 × 14 işleminin sonucu kaçtır?",
        dogru=7 * 26 + 7 * 14,
        celdiriciler=[
            (7 * 26, "Yalnız ilk çarpımı yazmış; ikinci çarpımı toplamaya katmamış."),
            (26 + 14, "Ortak çarpan 7'yi hiç kullanmamış; yalnız 26 + 14 toplamını yazmış."),
            (7 * 26 * 14, "İki çarpımı toplamak yerine hepsini birbiriyle çarpmış."),
        ],
        explanation="İki çarpımda ortak çarpan 7'dir; dağılma özelliği ters yönde kullanılır: "
                    "7 × 26 + 7 × 14 = 7 × (26 + 14) = 7 × 40 = 280.",
        difficultyReason="3 adım; ön bilgi: dağılma özelliğinin ters yönde (ortak çarpan parantezine alma) kullanımı; çeldiriciler yakın (ortak çarpanı düşürme); beceri: hesaplama; akıl yürütme",
        hints=[
            "İki çarpımda ortak olan sayıyı bul.",
            "Bu ortak sayıyı parantezin önüne almayı dene.",
            "Parantez içinde hangi iki sayının kalacağını yaz.",
            "Parantez içini toplayıp ortak çarpanla çarpmayı dene.",
            "Tam çözüm: ortak çarpan 7'dir; 7 × (26 + 14) = 7 × 40 = 280 bulunur.",
        ],
    ),
    dict(
        level=4,
        question="Bir öğrenci 6 × (30 + 4) işlemini 6 × 30 + 4 = 184 diye hesaplamıştır. Öğrencinin hatası nedir?",
        choices=[
            "Çarpanı parantezdeki ikinci terimle çarpmamıştır; işlemin sonucu 204 olmalıdır.",
            "Parantez içini önce toplamalıydı; dağılma özelliği kullanılamaz.",
            "Çarpanı yalnız ikinci terime dağıtmalıydı; sonuç 24 olmalıdır.",
            "Çarpma yerine toplama yapmalıydı; sonuç 40 olmalıdır.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Dağılma özelliği bu işlemde kullanılabilir; parantez içini toplamak da aynı sonucu verir, ikisi de geçerlidir.",
            "Dağılma özelliğinde çarpan terimlerden yalnız birine değil, hepsine dağıtılır.",
            "İşlemde çarpma vardır; işlem türünü değiştirmek sonucu bulmanın yolu değildir.",
        ],
        explanation="Dağılma özelliğinde çarpan parantez içindeki her terimle çarpılır: "
                    "6 × 30 + 6 × 4 = 180 + 24 = 204. Öğrenci 4'ü çarpmadan eklediği için 184 bulmuştur. "
                    "Parantez içi önce toplanarak 6 × 34 = 204 biçiminde de hesaplanabilirdi.",
        difficultyReason="4 adım; ön bilgi: dağılma özelliğinin bütün terimlere uygulanması; çeldiriciler yakın (geçerli yolu hatalı gösterme); beceri: hata teşhisi",
        hints=[
            "Öğrencinin yazdığı adımı kendi başına hesapla ve sonucu doğrula.",
            "Aynı işlemi parantez içini önce toplayarak hesapla.",
            "İki sonucu karşılaştır; hangisinin doğru olduğuna karar ver.",
            "Öğrencinin adımında hangi sayının çarpılmadan kaldığını bul.",
            "Tam çözüm: doğru dağıtım 6 × 30 + 6 × 4 = 180 + 24 = 204'tür. Öğrenci 4'ü çarpanla çarpmadan eklediği için 184 bulmuştur.",
        ],
    ),
    dict(
        level=2,
        question="Aşağıdaki eşitliklerden hangisi yanlıştır?",
        choices=[
            "18 + 5 = 5 + 18",
            "18 × 5 = 5 × 18",
            "18 − 5 = 5 − 18",
            "18 + 0 = 18",
        ],
        correct=2,
        distractorWhy=[
            "Toplamada değişme özelliği vardır; iki taraf da 23 eder.",
            "Çarpmada değişme özelliği vardır; iki taraf da 90 eder.",
            "doğru",
            "Bir sayıya sıfır eklemek onu değiştirmez; iki taraf da 18'dir.",
        ],
        explanation="Değişme özelliği toplama ve çarpmada geçerlidir, çıkarmada geçerli değildir. "
                    "18 − 5 = 13 iken 5 − 18 aynı değeri vermez; bu yüzden üçüncü eşitlik yanlıştır.",
        difficultyReason="2 adım; ön bilgi: değişme özelliğinin hangi işlemlerde geçerli olduğu; çeldiriciler yakın (üçü de doğru eşitlik); beceri: özellik ayırt etme",
        hints=[
            "Değişme özelliğinin hangi işlemler için geçerli olduğunu hatırla.",
            "Her seçeneğin iki tarafını ayrı ayrı hesapla.",
            "İki tarafı eşit çıkan seçenekleri ele.",
            "Kalan seçenekte işlem işaretinin ne olduğuna bak.",
            "Tam çözüm: çıkarmada değişme özelliği yoktur. 18 − 5 = 13 iken 5 − 18 bu değeri vermez, bu yüzden 18 − 5 = 5 − 18 yanlıştır.",
        ],
    ),
    dict(
        level=3,
        question="(48 ÷ 6) ÷ 2 ile 48 ÷ (6 ÷ 2) işlemlerinin sonuçları için ne söylenebilir?",
        choices=[
            "İkisi de 4'tür; bölmede birleşme özelliği vardır.",
            "Birincisi 4, ikincisi 16'dır; bölmede birleşme özelliği yoktur.",
            "İkisi de 16'dır; gruplama sonucu değiştirmez.",
            "Birincisi 16, ikincisi 4'tür; parantez her zaman sonucu büyütür.",
        ],
        correct=1,
        distractorWhy=[
            "Birinci işlem 4 verir ama ikincisi aynı değeri vermez; bu yüzden birleşme özelliğinden söz edilemez.",
            "doğru",
            "İkinci işlem 16 verir ama birincisi 4'tür; iki sonuç eşit değildir.",
            "Sonuçlar ters sıralanmış; ayrıca parantez sonucu büyütmez, yalnız hangi işlemin önce yapılacağını belirler.",
        ],
        explanation="(48 ÷ 6) ÷ 2 = 8 ÷ 2 = 4 iken 48 ÷ (6 ÷ 2) = 48 ÷ 3 = 16'dır. "
                    "Gruplama değiştiğinde sonuç da değiştiği için bölmede birleşme özelliği yoktur.",
        difficultyReason="4 adım; ön bilgi: birleşme özelliğinin bölmede geçerli olmadığı; çeldiriciler yakın (doğru sayıları yanlış eşleştirme); beceri: hesaplama; akıl yürütme",
        hints=[
            "İki işlemi ayrı ayrı, parantezden başlayarak hesapla.",
            "Birinci işlemin sonucunu yaz.",
            "İkinci işlemin sonucunu yaz.",
            "İki sonucu karşılaştırıp gruplamanın sonucu değiştirip değiştirmediğine karar ver.",
            "Tam çözüm: (48 ÷ 6) ÷ 2 = 4, 48 ÷ (6 ÷ 2) = 16 bulunur. Sonuçlar farklı olduğundan bölmede birleşme özelliği yoktur.",
        ],
    ),
    dict(
        level=1,
        question="Dengede duran bir terazinin sol kefesine 7 gramlık bir ağırlık ekleniyor. Terazinin dengede kalması için ne yapılmalıdır?",
        choices=[
            "Sağ kefeye de 7 gram eklenmelidir.",
            "Sağ kefeden 7 gram alınmalıdır.",
            "Sol kefeden 7 gram geri alınıp sağ kefeye konmalıdır.",
            "Hiçbir şey yapılmasına gerek yoktur; terazi kendiliğinden dengelenir.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Bir kefeye eklenip diğerinden alınırsa iki kefe arasındaki fark iki katına çıkar ve denge daha da bozulur.",
            "Ağırlığı sol kefeden alıp sağa koymak eklemeyi geri almak değildir; sağ kefe bu kez ağır basar.",
            "Terazi kendiliğinden dengelenmez; denge ancak iki kefeye aynı işlem uygulanınca korunur.",
        ],
        explanation="Eşitliğin korunumu terazi ile aynı biçimde çalışır: bir kefeye eklenen miktar diğerine de "
                    "eklenirse denge bozulmaz. Sol kefeye 7 gram eklendiğine göre sağ kefeye de 7 gram eklenmelidir.",
        difficultyReason="1 adım; ön bilgi: eşitliğin korunumunun terazi modeliyle karşılığı; çeldiriciler yakın (dengeyi bozan işlemler); beceri: model uygulama",
        hints=[
            "Terazinin dengede olması iki kefe için ne anlama gelir, düşün.",
            "Yalnız bir kefeye ekleme yapılınca hangi kefenin ağır bastığını söyle.",
            "Dengeyi geri getirmek için diğer kefeye ne yapılması gerektiğini düşün.",
            "Ekleme yerine çıkarma yapılırsa farkın büyüyüp büyümediğini kontrol et.",
            "Tam çözüm: iki kefeye aynı miktar eklenirse denge korunur. Sol kefeye 7 gram eklendiği için sağ kefeye de 7 gram eklenmelidir.",
        ],
    ),
    dict(
        level=2,
        question="□ + 14 = 39 eşitliğinde kutuya hangi sayı gelmelidir?",
        dogru=39 - 14,
        celdiriciler=[
            (39 + 14, "İki sayıyı toplamış; oysa kutudaki sayı 14 ile toplanınca 39 etmelidir."),
            (39, "Eşitliğin sağ tarafını olduğu gibi kutuya yazmış; 14'ü hesaba katmamış."),
            (14, "Kutunun yanındaki sayıyı yeniden yazmış."),
        ],
        explanation="Eşitliğin iki tarafından aynı sayı çıkarılırsa eşitlik bozulmaz. "
                    "İki taraftan 14 çıkarılınca kutudaki sayı 39 − 14 = 25 olarak bulunur.",
        difficultyReason="2 adım; ön bilgi: eşitliğin iki tarafından aynı sayının çıkarılabilmesi; çeldiriciler yakın (ters işlem); beceri: bilinmeyen bulma",
        hints=[
            "Kutudaki sayının 14 ile toplanınca kaç etmesi gerektiğini söyle.",
            "Eşitliğin iki tarafına aynı işlemi uygulayabildiğini hatırla.",
            "Kutuyu yalnız bırakmak için iki taraftan hangi sayıyı çıkaracağını belirle.",
            "Çıkarma işlemini iki tarafta da yapmayı dene.",
            "Tam çözüm: iki taraftan 14 çıkarılır; kutu = 39 − 14 = 25 bulunur.",
        ],
    ),
    dict(
        level=3,
        question="Bir eşitliğin sol tarafı 3 ile çarpılmıştır. Eşitliğin bozulmaması için ne yapılmalıdır?",
        choices=[
            "Sağ taraf da 3 ile çarpılmalıdır.",
            "Sağ taraf 3'e bölünmelidir.",
            "Sağ tarafa 3 eklenmelidir.",
            "Sol taraf yeniden 3'e bölünmelidir; sağ tarafa dokunulmaz.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Bir taraf çarpılıp diğeri bölünürse iki taraf birbirinden daha da uzaklaşır.",
            "Toplama ile çarpma birbirinin yerini tutmaz; 3 eklemek 3 ile çarpmanın karşılığı değildir.",
            "Bu yol işlemi geri alır ve eşitliği eski hâline döndürür; istenen ise çarpılmış hâlin korunmasıdır.",
        ],
        explanation="Eşitliğin iki tarafı sıfırdan farklı aynı sayıyla çarpılırsa eşitlik bozulmaz. "
                    "Sol taraf 3 ile çarpıldığına göre sağ taraf da 3 ile çarpılmalıdır.",
        difficultyReason="3 adım; ön bilgi: eşitliğin iki tarafına aynı çarpma işleminin uygulanması; çeldiriciler yakın (ters işlem ya da farklı işlem önerme); beceri: kural uygulama",
        hints=[
            "Eşitliği bir terazi gibi düşün: bir kefeye yapılan işlem diğerine ne yapılmasını gerektirir?",
            "Yalnız bir tarafın çarpılması dengeyi hangi yöne bozar?",
            "Aynı işlemin iki tarafa da uygulanması gerektiğini hatırla.",
            "Çarpmanın yerine toplama koymanın denk olup olmadığını sorgula.",
            "Tam çözüm: iki taraf aynı sayıyla çarpılırsa eşitlik korunur; sol taraf 3 ile çarpıldığına göre sağ taraf da 3 ile çarpılmalıdır.",
        ],
    ),
    dict(
        level=4,
        question="35 × 12 = 35 × (10 + 2) = 35 × 10 + 35 × 2 dönüşümünde hangi özellik kullanılmıştır?",
        choices=[
            "toplamada birleşme özelliği",
            "çarpmada değişme özelliği",
            "çarpmanın toplama üzerine dağılma özelliği",
            "toplamada değişme özelliği",
        ],
        correct=2,
        distractorWhy=[
            "Birleşme özelliği yalnız gruplamayı değiştirir; burada 12 sayısı iki terime ayrılıp çarpan her ikisine dağıtılmıştır.",
            "Değişme özelliği çarpanların yerini değiştirir; burada çarpanların yeri değil, biri toplama açılmıştır.",
            "doğru",
            "Toplamada değişme özelliği terimlerin yerini değiştirir; burada 10 ile 2 yer değiştirmemiştir.",
        ],
        explanation="12 sayısı 10 + 2 biçiminde yazılmış, ardından 35 çarpanı parantez içindeki her terimle "
                    "ayrı ayrı çarpılmıştır. Bu, çarpmanın toplama üzerine dağılma özelliğidir.",
        difficultyReason="4 adım; ön bilgi: dört özelliğin birbirinden ayırt edilmesi; çeldiriciler çok yakın (hepsi geçerli birer özellik adı); beceri: özellik tanıma; akıl yürütme",
        hints=[
            "Dönüşümün her adımında neyin değiştiğini tek tek yaz.",
            "İlk adımda 12 sayısına ne yapıldığına bak.",
            "İkinci adımda 35 çarpanının kaç terimle çarpıldığını say.",
            "Yalnız gruplamayı ya da yalnız sırayı değiştiren özellikleri ele.",
            "Tam çözüm: 12 iki terime ayrılmış ve 35 her iki terimle çarpılmıştır; bu çarpmanın toplama üzerine dağılma özelliğidir.",
        ],
    ),
    dict(
        level=3,
        question="7 × 102 çarpımını zihinden yapmak için hangi ayrıştırma kullanılır?",
        choices=[
            "7 × 100 + 7 × 2",
            "7 × 100 + 2",
            "7 × 100 × 2",
            "7 + 100 × 2",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "İkinci terimi çarpmadan eklemiş; çarpan parantezdeki her terime dağıtılmalıdır.",
            "İki terimi toplamak yerine çarpmış; 102 sayısı 100 ile 2'nin toplamıdır, çarpımı değildir.",
            "Çarpanı ilk terimle toplamış; dağılma özelliğinde çarpan hiçbir terimle toplanmaz.",
        ],
        explanation="102 sayısı 100 + 2 biçiminde yazılır ve çarpan her iki terime dağıtılır: "
                    "7 × 100 + 7 × 2 = 700 + 14 = 714.",
        difficultyReason="3 adım; ön bilgi: zihinden hesapta sayıyı kolay terimlere ayırma ve dağılma; çeldiriciler yakın (terimi çarpmadan bırakma); beceri: hesaplama stratejisi",
        hints=[
            "102 sayısını zihinden kolay iki parçaya ayırmayı dene.",
            "Bu iki parçanın toplamla mı çarpımla mı birleştiğine karar ver.",
            "Çarpanı her iki parçaya ayrı ayrı dağıt.",
            "Ortaya çıkan iki çarpımı toplamayı dene.",
            "Tam çözüm: 102 = 100 + 2 yazılır; 7 × 100 + 7 × 2 = 700 + 14 = 714 bulunur.",
        ],
    ),
    dict(
        level=4,
        question="4 × (□ + 6) = 4 × 15 + 4 × 6 eşitliğinde kutuya hangi sayı gelmelidir?",
        dogru=15,
        celdiriciler=[
            (15 + 6, "Parantez içindeki iki terimi toplamış; kutuya yalnız dağıtılan ilk terim yazılır."),
            (4, "Parantezin önündeki çarpanı kutuya yazmış."),
            (6, "Parantezde zaten yazılı olan terimi yeniden yazmış."),
        ],
        explanation="Sağ tarafta 4 çarpanı 15 ve 6 terimlerine dağıtılmıştır. Dağıtımdan önceki hâl "
                    "4 × (15 + 6) olduğuna göre kutuya 15 gelir.",
        difficultyReason="4 adım; ön bilgi: dağılmanın ters yönde okunması; çeldiriciler yakın (parantez içini toplama ya da çarpanı yazma); beceri: akıl yürütme",
        hints=[
            "Eşitliğin sağ tarafının hangi işlemden elde edildiğini düşün.",
            "Sağ taraftaki iki çarpımda ortak olan sayıyı bul.",
            "Ortak çarpanı parantezin önüne alıp geri kalanları parantez içine yaz.",
            "Yazdığın ifadeyi soldaki ifadeyle karşılaştır.",
            "Tam çözüm: sağ taraf 4 × (15 + 6) ifadesinden çıkmıştır; sol tarafta 6 zaten yazılı olduğuna göre kutuya 15 gelir.",
        ],
    ),
    dict(
        level=2,
        question="Bir öğrenci defterine “8 + 5 = 13 + 2 = 15” yazmıştır. Bu yazımın hatası nedir?",
        choices=[
            "Toplama işlemleri yanlış hesaplanmıştır.",
            "Eşitlik işareti zincir hâlinde kullanılmış, aslında eşit olmayan ifadeler eşitlenmiştir.",
            "Eşitlik işareti yerine büyüktür işareti kullanılmalıydı.",
            "İşlemler soldan sağa değil sağdan sola yapılmalıydı.",
        ],
        correct=1,
        distractorWhy=[
            "Her toplama tek başına doğru hesaplanmıştır; hata hesapta değil, eşitliklerin bağlanmasındadır.",
            "doğru",
            "İfadeler arasında bir büyüklük karşılaştırması istenmemektedir; sorun eşitliğin yanlış yerde kurulmasıdır.",
            "İşlem yönü bu yazımdaki hatanın kaynağı değildir; her iki yönde de aynı toplamlar çıkar.",
        ],
        explanation="Eşitlik işareti iki tarafın aynı değeri taşıdığını bildirir. 8 + 5 = 13 doğrudur, "
                    "13 + 2 = 15 de doğrudur; ancak 13 ile 15 eşit olmadığı için bunlar tek bir zincirde "
                    "eşitlik işaretiyle bağlanamaz.",
        difficultyReason="3 adım; ön bilgi: eşitlik işaretinin denge anlamı, 'sonuç geliyor' anlamı taşımaması; çeldiriciler yakın (hatayı hesapta arama); beceri: hata teşhisi",
        hints=[
            "Eşitlik işaretinin ne bildirdiğini kendi sözlerinle söyle.",
            "Zincirdeki her eşitliği ayrı ayrı ele alıp hesapla.",
            "Zincirin başındaki ve sonundaki değerleri karşılaştır.",
            "Bu iki değer eşit değilse aralarına eşitlik işareti konup konamayacağına karar ver.",
            "Tam çözüm: 8 + 5 = 13, 13 + 2 = 15'tir. 13 ile 15 eşit olmadığından bu ifadeler tek bir eşitlik zincirinde bağlanamaz.",
        ],
    ),
    dict(
        level=5,
        question="24 + 36 = 36 + 24 ve (24 + 36) + 4 = 24 + (36 + 4) eşitlikleri sırasıyla hangi özellikleri gösterir?",
        choices=[
            "birleşme özelliği; değişme özelliği",
            "değişme özelliği; birleşme özelliği",
            "dağılma özelliği; birleşme özelliği",
            "değişme özelliği; dağılma özelliği",
        ],
        correct=1,
        distractorWhy=[
            "Özellikler ters sıralanmış: ilk eşitlikte terimlerin yeri, ikincisinde gruplaması değişmiştir.",
            "doğru",
            "İlk eşitlikte çarpma yoktur; dağılma özelliği bir çarpanın terimlere dağıtılmasıyla ilgilidir.",
            "İkinci eşitlikte çarpma yoktur; yalnız parantezin yeri değişmiştir.",
        ],
        explanation="Birinci eşitlikte terimlerin yeri değişmiştir: bu değişme özelliğidir. İkincisinde "
                    "terimlerin yeri aynı kalıp gruplama değişmiştir: bu da birleşme özelliğidir.",
        difficultyReason="5 adım; ön bilgi: değişme, birleşme ve dağılma özelliklerinin aynı anda ayırt edilmesi; çeldiriciler çok yakın (aynı adların farklı sıralanışı); beceri: özellik tanıma; akıl yürütme",
        hints=[
            "İki eşitliği ayrı ayrı incele; her birinde neyin değiştiğini yaz.",
            "Birinci eşitlikte sayıların yerinin mi gruplamasının mı değiştiğine bak.",
            "İkinci eşitlikte parantezin yerini izle.",
            "Çarpma bulunmayan bir eşitlikte dağılma özelliğinden söz edilip edilemeyeceğini düşün.",
            "Tam çözüm: ilk eşitlikte terimler yer değiştirmiştir (değişme), ikincisinde yalnız gruplama değişmiştir (birleşme).",
        ],
    ),
    dict(
        level=1,
        question="45 + 19 = □ + 45 eşitliğinde kutuya hangi sayı gelmelidir?",
        dogru=19,
        celdiriciler=[
            (45 + 19, "İki sayının toplamını kutuya yazmış; sağ tarafta toplama işlemi henüz yapılmamıştır."),
            (45, "Kutunun yanındaki sayıyı yeniden yazmış; yer değiştiren sayı 19'dur."),
            (45 - 19, "İki sayının farkını almış: 45 − 19 = 26."),
        ],
        explanation="Toplamada değişme özelliği gereği 45 + 19 ile 19 + 45 eşittir; kutuya 19 yazılır.",
        difficultyReason="1 adım; ön bilgi: toplamada değişme özelliği; çeldiriciler yakın (toplamı ya da farkı yazma); beceri: özellik tanıma",
        hints=[
            "Eşitliğin iki tarafında ortak olan sayıyı işaretle.",
            "Sol tarafta olup sağ tarafta henüz yazılmamış sayıyı bul.",
            "Toplamada terimlerin yer değiştirmesinin sonucu etkileyip etkilemediğini hatırla.",
            "Kutuya bir terim mi yoksa bir toplam mı yazılacağına karar ver.",
            "Tam çözüm: sağ tarafta 45 yazılı olduğuna göre kutuya 19 gelir; iki taraf da 64 eder.",
        ],
    ),
    dict(
        level=4,
        question="12 × 45 − 12 × 35 işleminin sonucu kaçtır?",
        dogru=12 * 45 - 12 * 35,
        celdiriciler=[
            (45 - 35, "Ortak çarpan 12'yi hiç kullanmamış; yalnız 45 − 35 farkını yazmış."),
            (12 * (45 + 35), "Parantez içindeki işlemi çıkarma yerine toplama yapmış."),
            (12 * 45, "İkinci çarpımı hiç çıkarmamış; yalnız 12 × 45 hesaplanmış."),
        ],
        explanation="İki çarpımda ortak çarpan 12'dir: 12 × 45 − 12 × 35 = 12 × (45 − 35) = 12 × 10 = 120.",
        difficultyReason="4 adım; ön bilgi: çıkarmada ortak çarpan parantezine alma; çeldiriciler yakın (ortak çarpanı düşürme ya da işareti değiştirme); beceri: hesaplama; akıl yürütme",
        hints=[
            "İki çarpımda ortak olan sayıyı bul.",
            "Ortak çarpanı parantezin önüne almayı dene.",
            "Parantez içinde hangi işlemin kalacağına karar ver.",
            "Parantez içini hesaplayıp ortak çarpanla çarp.",
            "Tam çözüm: 12 × (45 − 35) = 12 × 10 = 120 bulunur.",
        ],
    ),
    dict(
        level=5,
        question="Bir terazinin sol kefesinde eşit ağırlıkta 3 kutu ile 5 gramlık bir ağırlık, sağ kefesinde ise 20 gramlık bir ağırlık vardır ve terazi dengededir. Bir kutu kaç gramdır?",
        dogru=5,
        celdiriciler=[
            (20 - 5, "İki kefeden 5 gramı çıkarıp orada durmuş; kalan 15 gram üç kutuya aittir."),
            (20, "Sağ kefedeki ağırlığın tamamını tek kutuya vermiş."),
            (20 + 5, "İki kefedeki ağırlıkları toplamış; oysa terazi dengede olduğu için iki kefe eşittir."),
        ],
        explanation="Terazi dengede olduğuna göre iki kefe eşittir: 3 kutu + 5 = 20. İki kefeden 5 gram "
                    "çıkarılınca 3 kutu = 15 kalır; bir kutu 15 ÷ 3 = 5 gramdır.",
        difficultyReason="5 adım; ön bilgi: eşitliğin korunumuyla iki taraftan aynı miktarı çıkarma ve eşit parçalara bölme; çeldiriciler yakın (ara sonucu yanıt sanma); beceri: model kurma; hesaplama",
        hints=[
            "Terazinin dengede olmasının iki kefe için ne anlama geldiğini yaz.",
            "İki kefeyi bir eşitlik gibi düşünüp yan yana getir.",
            "Kutuları yalnız bırakmak için iki kefeden aynı anda ne çıkarabileceğini bul.",
            "Kalan ağırlığın kaç kutuya ait olduğunu belirleyip paylaştırmayı dene.",
            "Tam çözüm: 3 kutu + 5 = 20 eşitliğinde iki taraftan 5 çıkarılır, 3 kutu = 15 olur; bir kutu 15 ÷ 3 = 5 gramdır.",
        ],
    ),
    dict(
        level=5,
        question="(60 + 24) ÷ 6 işlemi için aşağıdakilerden hangisi doğrudur?",
        choices=[
            "60 ÷ 6 + 24 ÷ 6 = 14",
            "60 ÷ 6 + 24 = 34",
            "60 + 24 ÷ 6 = 64",
            "60 ÷ 6 × 24 ÷ 6 = 40",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Yalnız ilk terimi bölmüş, ikinci terimi olduğu gibi eklemiş; parantez içindeki her terim bölünmelidir.",
            "Parantezi yok sayıp işlem önceliğine göre hesaplamış; parantez toplamanın önce yapılmasını gerektirir.",
            "Terimler arasındaki toplamayı çarpmaya çevirmiş; bölme toplamayı çarpmaya dönüştürmez.",
        ],
        explanation="Bir toplamın bölümünde her terim ayrı ayrı bölünebilir: "
                    "(60 + 24) ÷ 6 = 60 ÷ 6 + 24 ÷ 6 = 10 + 4 = 14. Parantez içi önce toplanarak "
                    "84 ÷ 6 = 14 biçiminde de bulunur.",
        difficultyReason="5 adım; ön bilgi: bölmenin toplam üzerine terim terim uygulanabilmesi; çeldiriciler yakın (yalnız bir terimi bölme, parantezi yok sayma); beceri: hesaplama; akıl yürütme",
        hints=[
            "Önce parantez içini toplayıp bölerek sonucu bul; bu senin kontrol değerin olsun.",
            "Sonra her terimi ayrı ayrı bölmeyi dene.",
            "İki yoldan çıkan sonuçları karşılaştır.",
            "Seçenekleri hesaplayıp kontrol değerine eşit olanı ara.",
            "Tam çözüm: 84 ÷ 6 = 14'tür. Terim terim bölündüğünde de 60 ÷ 6 + 24 ÷ 6 = 10 + 4 = 14 çıkar.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# MAT.5.2.2 — note.02 "Doğal sayılarda işlem önceliği"
# ---------------------------------------------------------------------------

A22 = [
    dict(
        level=1,
        question="51 + 3 × 4 işleminin sonucu kaçtır?",
        dogru=51 + 3 * 4,
        celdiriciler=[
            ((51 + 3) * 4, "İşlemleri soldan sağa yapmış: önce 51 + 3, sonra 4 ile çarpmış."),
            (51 + 3 + 4, "Çarpma yerine toplama yapmış."),
            (51 * 3 + 4, "Çarpma ile toplamanın yerini değiştirmiş: 51 × 3 + 4."),
        ],
        explanation="Çarpma toplamadan önce yapılır: 3 × 4 = 12; ardından 51 + 12 = 63.",
        difficultyReason="2 adım; ön bilgi: çarpmanın toplamadan önce geldiği; çeldiriciler yakın (soldan sağa hesaplama); beceri: hesaplama",
        hints=[
            "İşlemde kaç farklı işlem türü bulunduğunu say.",
            "Bu işlemlerden hangisinin önce yapılması gerektiğini belirle.",
            "Öncelikli işlemi yapıp sonucu yerine yaz.",
            "Kalan işlemi son adımda uygula.",
            "Tam çözüm: önce 3 × 4 = 12 yapılır, sonra 51 + 12 = 63 bulunur.",
        ],
    ),
    dict(
        level=2,
        question="60 − 4 × 7 işleminin sonucu kaçtır?",
        dogru=60 - 4 * 7,
        celdiriciler=[
            ((60 - 4) * 7, "İşlemleri soldan sağa yapmış: önce 60 − 4, sonra 7 ile çarpmış."),
            (4 * 7, "Yalnız çarpımı yazmış; çıkarma adımını yapmamış."),
            (60 - 4 - 7, "Çarpma yerine ikinci bir çıkarma yapmış."),
        ],
        explanation="Çarpma çıkarmadan önce yapılır: 4 × 7 = 28; ardından 60 − 28 = 32.",
        difficultyReason="2 adım; ön bilgi: çarpmanın çıkarmadan önce geldiği; çeldiriciler yakın (soldan sağa hesaplama); beceri: hesaplama",
        hints=[
            "İşlemdeki çarpmayı ve çıkarmayı ayrı ayrı işaretle.",
            "Hangisinin önce yapılacağına karar ver.",
            "Çarpımı hesaplayıp ifadede yerine koy.",
            "Kalan çıkarmayı son adımda yap.",
            "Tam çözüm: önce 4 × 7 = 28 yapılır, sonra 60 − 28 = 32 bulunur.",
        ],
    ),
    dict(
        level=2,
        question="72 ÷ 8 + 4 işleminin sonucu kaçtır?",
        dogru=72 // 8 + 4,
        celdiriciler=[
            (72 // (8 + 4), "Toplamayı bölmeden önce yapmış: 72 ÷ (8 + 4)."),
            (72 // 8 * 4, "Toplama yerine çarpma yapmış: 72 ÷ 8 × 4."),
            (72 // 8, "Yalnız bölümü yazmış; toplama adımını yapmamış."),
        ],
        explanation="Bölme toplamadan önce yapılır: 72 ÷ 8 = 9; ardından 9 + 4 = 13.",
        difficultyReason="2 adım; ön bilgi: bölmenin toplamadan önce geldiği; çeldiriciler yakın (paranteze alma); beceri: hesaplama",
        hints=[
            "İşlemde parantez olmadığına dikkat et.",
            "Bölme ile toplamadan hangisinin öncelikli olduğunu hatırla.",
            "Bölme işlemini yapıp sonucunu yerine yaz.",
            "Kalan toplamayı son adımda uygula.",
            "Tam çözüm: önce 72 ÷ 8 = 9 yapılır, sonra 9 + 4 = 13 bulunur.",
        ],
    ),
    dict(
        level=2,
        question="(15 + 9) × 3 işleminin sonucu kaçtır?",
        dogru=(15 + 9) * 3,
        celdiriciler=[
            (15 + 9 * 3, "Parantezi yok sayıp çarpmayı önce yapmış: 15 + 9 × 3."),
            (15 * 3 + 9, "Çarpanı parantezin ikinci terimi yerine birinci terimiyle çarpıp kalanı eklemiş."),
            (15 + 9 + 3, "Çarpma yerine toplama yapmış."),
        ],
        explanation="Parantez önce yapılır: 15 + 9 = 24; ardından 24 × 3 = 72.",
        difficultyReason="2 adım; ön bilgi: parantezin en yüksek öncelikte olması; çeldiriciler yakın (parantezi yok sayma); beceri: hesaplama",
        hints=[
            "Parantezin işlem sırasında ne anlama geldiğini hatırla.",
            "Parantez içindeki işlemi ilk adımda yap.",
            "Bulduğun sayıyı parantezin yerine koy.",
            "Kalan çarpmayı son adımda uygula.",
            "Tam çözüm: parantez içi 15 + 9 = 24 eder; sonra 24 × 3 = 72 bulunur.",
        ],
    ),
    dict(
        level=3,
        question="36 ÷ 6 × 2 işleminin sonucu kaçtır?",
        dogru=36 // 6 * 2,
        celdiriciler=[
            (36 // (6 * 2), "Çarpmayı bölmeden önce yapmış; oysa aynı öncelikteki işlemler soldan sağa uygulanır."),
            (36 * 6 // 2, "Bölme ile çarpmanın yerini değiştirmiş: 36 × 6 ÷ 2."),
            (36 // 6, "Yalnız bölümü yazmış; çarpma adımını yapmamış."),
        ],
        explanation="Çarpma ile bölme aynı öncelik düzeyindedir; soldan sağa uygulanır: "
                    "önce 36 ÷ 6 = 6, sonra 6 × 2 = 12.",
        difficultyReason="3 adım; ön bilgi: çarpmanın bölmeden önce gelmediği, aynı düzeyde soldan sağa sıra; çeldiriciler çok yakın (çarpmayı öne alma); beceri: kural uygulama; hesaplama",
        hints=[
            "İşlemdeki iki işlemin öncelik düzeylerini karşılaştır.",
            "Aynı düzeydeki işlemlerde sırayı neyin belirlediğini hatırla.",
            "En soldaki işlemi ilk adımda yap.",
            "Çıkan sonucu kullanarak ikinci işlemi uygula.",
            "Tam çözüm: çarpma ile bölme aynı düzeydedir, soldan sağa gidilir: 36 ÷ 6 = 6, sonra 6 × 2 = 12.",
        ],
    ),
    dict(
        level=3,
        question="50 − 12 + 8 işleminin sonucu kaçtır?",
        dogru=50 - 12 + 8,
        celdiriciler=[
            (50 - (12 + 8), "Toplamayı çıkarmadan önce yapmış; oysa aynı öncelikteki işlemler soldan sağa uygulanır."),
            (50 + 12 - 8, "Çıkarma ile toplamanın yerini değiştirmiş."),
            (50 - 12, "Yalnız ilk çıkarmayı yapmış; toplama adımını atlamış."),
        ],
        explanation="Toplama ile çıkarma aynı öncelik düzeyindedir; soldan sağa uygulanır: "
                    "önce 50 − 12 = 38, sonra 38 + 8 = 46.",
        difficultyReason="3 adım; ön bilgi: toplamanın çıkarmadan önce gelmediği, aynı düzeyde soldan sağa sıra; çeldiriciler çok yakın (toplamayı öne alma); beceri: kural uygulama; hesaplama",
        hints=[
            "İşlemde parantez bulunup bulunmadığına bak.",
            "Toplama ile çıkarmanın öncelik düzeylerini karşılaştır.",
            "Aynı düzeydeki işlemlerde hangi yönde ilerlendiğini hatırla.",
            "En soldaki işlemden başlayarak adım adım ilerle.",
            "Tam çözüm: soldan sağa gidilir: 50 − 12 = 38, sonra 38 + 8 = 46 bulunur.",
        ],
    ),
    dict(
        level=3,
        question="4 × (7 + 5) − 10 işleminin sonucu kaçtır?",
        dogru=4 * (7 + 5) - 10,
        celdiriciler=[
            (4 * 7 + 5 - 10, "Parantezi yok sayıp çarpmayı yalnız ilk terime uygulamış."),
            (4 * (7 + 5), "Parantez ve çarpmayı doğru yapmış ama son çıkarma adımını atlamış."),
            (4 * (7 + 5 - 10), "Çıkarmayı da parantezin içine almış."),
        ],
        explanation="Önce parantez: 7 + 5 = 12. Sonra çarpma: 4 × 12 = 48. En son çıkarma: 48 − 10 = 38.",
        difficultyReason="3 adım; ön bilgi: parantez, çarpma ve çıkarmanın üç aşamalı sırası; çeldiriciler yakın (adım atlama ya da parantezi genişletme); beceri: hesaplama",
        hints=[
            "İşlemi üç aşamaya böl ve her aşamada yalnız bir işlem yap.",
            "Parantez içini ilk adımda hesapla.",
            "Çıkan sayıyı çarpanla çarp.",
            "Parantezin dışında kalan çıkarmayı en sona bırak.",
            "Tam çözüm: 7 + 5 = 12, 4 × 12 = 48, 48 − 10 = 38 bulunur.",
        ],
    ),
    dict(
        level=4,
        question="100 − 3 × (12 − 4) işleminin sonucu kaçtır?",
        dogru=100 - 3 * (12 - 4),
        celdiriciler=[
            ((100 - 3) * (12 - 4), "İşlemleri soldan sağa yapmış: önce 100 − 3, sonra parantezle çarpmış."),
            (100 - 3 * 12 - 4, "Parantezi kaldırırken ikinci terimin işaretini korumamış."),
            (12 - 4, "Yalnız parantez içini yazmış; kalan iki adımı yapmamış."),
        ],
        explanation="Önce parantez: 12 − 4 = 8. Sonra çarpma: 3 × 8 = 24. En son çıkarma: 100 − 24 = 76.",
        difficultyReason="4 adım; ön bilgi: parantez, çarpma ve çıkarmanın sırası; çeldiriciler yakın (soldan sağa hesaplama, işaret hatası); beceri: hesaplama",
        hints=[
            "İşlemde parantezin nerede olduğunu işaretle.",
            "Parantez içini hesaplayıp yerine tek bir sayı yaz.",
            "Geriye kalan ifadede hangi işlemin öncelikli olduğuna karar ver.",
            "Çarpımı bulduktan sonra çıkarmayı en sona bırak.",
            "Tam çözüm: 12 − 4 = 8, 3 × 8 = 24, 100 − 24 = 76 bulunur.",
        ],
    ),
    dict(
        level=2,
        question="18 + 6 ÷ 3 işleminde hangi işlem önce yapılmalıdır?",
        choices=[
            "toplama, çünkü soldaki işlem önce yapılır",
            "bölme, çünkü bölme toplamadan önceliklidir",
            "ikisi aynı anda yapılır",
            "toplama, çünkü toplama her zaman önceliklidir",
        ],
        correct=1,
        distractorWhy=[
            "Soldan sağa kuralı yalnız aynı öncelik düzeyindeki işlemler için geçerlidir; burada düzeyler farklıdır.",
            "doğru",
            "İşlemler tek tek sırayla yapılır; aynı anda yapılan iki işlem diye bir kural yoktur.",
            "Toplamanın önceliği yoktur; öncelik sırası parantez, çarpma-bölme, toplama-çıkarma biçimindedir.",
        ],
        explanation="İşlem önceliğinde çarpma ve bölme, toplama ve çıkarmadan önce gelir. "
                    "Bu işlemde önce 6 ÷ 3 = 2 yapılır, ardından 18 + 2 = 20 bulunur.",
        difficultyReason="2 adım; ön bilgi: öncelik düzeyleri ile soldan sağa kuralının hangi durumda geçerli olduğu; çeldiriciler yakın (soldan sağa kuralını genelleştirme); beceri: kural ayırt etme",
        hints=[
            "İşlem önceliği sırasını baştan sona kendi sözlerinle söyle.",
            "Bu işlemdeki iki işlemin hangi düzeyde olduğunu belirle.",
            "Düzeyler farklıysa soldan sağa kuralının geçerli olup olmadığını düşün.",
            "Öncelik düzeyi yüksek olan işlemi seç.",
            "Tam çözüm: bölme, toplamadan önceliklidir; bu yüzden önce 6 ÷ 3 yapılır ve sonuç 18 + 2 = 20 olur.",
        ],
    ),
    dict(
        level=4,
        question="Bir öğrenci 20 + 5 × 4 işleminin sonucunu 100 bulmuştur. Öğrencinin hatası nedir?",
        choices=[
            "Çarpmayı toplamadan önce yapmalıydı; sonuç 40 olmalıdır.",
            "Toplamayı çarpmadan önce yapmalıydı; sonuç 100 doğrudur.",
            "İşleme parantez eklemeliydi; sonuç 25 olmalıdır.",
            "Çarpma yerine bölme yapmalıydı; sonuç 21 olmalıdır.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Öğrencinin yaptığı zaten budur; toplamanın çarpmadan önce yapılması işlem önceliğine aykırıdır.",
            "İşlemde parantez yoktur ve eklenmesi de istenmemiştir; hata öncelik sırasındadır.",
            "İşlemde bölme geçmemektedir; işlem türünü değiştirmek hatanın düzeltilmesi değildir.",
        ],
        explanation="İşlem önceliğine göre çarpma önce yapılır: 5 × 4 = 20; ardından 20 + 20 = 40. "
                    "Öğrenci soldan sağa ilerleyip 20 + 5 = 25 bulmuş ve 25 × 4 = 100 diye devam etmiştir.",
        difficultyReason="4 adım; ön bilgi: soldan sağa hesaplamanın öncelik kuralını bozması; çeldiriciler yakın (hatayı doğru gösterme); beceri: hata teşhisi",
        hints=[
            "Öğrencinin 100 sonucuna hangi adımlarla ulaşmış olabileceğini yaz.",
            "İşlemi bir de öncelik kuralına göre hesapla.",
            "İki sonucu karşılaştır.",
            "Farkın hangi adımda ortaya çıktığını bul.",
            "Tam çözüm: doğru sıra önce 5 × 4 = 20, sonra 20 + 20 = 40'tır. Öğrenci soldan sağa gidip 20 + 5 = 25 ve 25 × 4 = 100 yapmıştır.",
        ],
    ),
    dict(
        level=4,
        question="9 + 6 × 2 işlemine parantez eklenerek sonucun 30 olması isteniyor. Parantez nereye konmalıdır?",
        choices=[
            "9 + (6 × 2)",
            "(9 + 6) × 2",
            "(9 + 6 × 2)",
            "9 + 6 × (2)",
        ],
        correct=1,
        distractorWhy=[
            "Bu parantez zaten öncelik sırasında yapılacak işlemi gösterir; sonuç değişmez ve 21 kalır.",
            "doğru",
            "İfadenin tamamını paranteze almak işlem sırasını değiştirmez; sonuç yine 21 olur.",
            "Tek bir sayıyı paranteze almak hiçbir işlemi öne almaz; sonuç 21 kalır.",
        ],
        explanation="Toplamanın önce yapılması için toplama paranteze alınır: (9 + 6) × 2 = 15 × 2 = 30. "
                    "Parantezsiz hâlde çarpma önce yapıldığı için sonuç 9 + 12 = 21'dir.",
        difficultyReason="4 adım; ön bilgi: parantezin işlem sırasını değiştirmek için kullanılması; çeldiriciler yakın (sonucu değiştirmeyen parantezler); beceri: akıl yürütme; hesaplama",
        hints=[
            "Önce parantezsiz hâlin sonucunu hesapla.",
            "İstenen sonuca ulaşmak için hangi işlemin öne alınması gerektiğini düşün.",
            "O işlemi paranteze almayı dene.",
            "Sonucu değiştirmeyen parantezleri ele.",
            "Tam çözüm: toplama öne alınmalıdır. (9 + 6) × 2 = 15 × 2 = 30 olur; parantezsiz hâl ise 21 verir.",
        ],
    ),
    dict(
        level=3,
        question="8 + 4 × 5 ile (8 + 4) × 5 işlemlerinin sonuçları için ne söylenebilir?",
        choices=[
            "İkisi de 60'tır; parantez sonucu değiştirmez.",
            "Birincisi 28, ikincisi 60'tır; parantez işlem sırasını değiştirir.",
            "İkisi de 28'dir; çarpma her durumda önce yapılır.",
            "Birincisi 60, ikincisi 28'dir; parantez çarpmayı sona atar.",
        ],
        correct=1,
        distractorWhy=[
            "Birinci işlemde parantez yoktur, çarpma önce yapılır ve sonuç 60 çıkmaz.",
            "doğru",
            "İkinci işlemde parantez toplamayı öne aldığı için çarpma her durumda önce yapılmaz.",
            "Sonuçlar ters eşleştirilmiş; ayrıca parantez çarpmayı sona atmaz, yalnız parantez içini öne alır.",
        ],
        explanation="8 + 4 × 5 işleminde çarpma önce yapılır: 8 + 20 = 28. (8 + 4) × 5 işleminde ise "
                    "parantez toplamayı öne alır: 12 × 5 = 60. Parantez işlem sırasını değiştirdiği için "
                    "sonuçlar farklıdır.",
        difficultyReason="3 adım; ön bilgi: parantezin sonucu değiştirebilmesi; çeldiriciler yakın (doğru sayıları yanlış eşleştirme); beceri: hesaplama; karşılaştırma",
        hints=[
            "İki işlemi ayrı ayrı hesapla; acele edip karşılaştırma yapma.",
            "Parantezsiz işlemde hangi işlemin önce geldiğini belirle.",
            "Parantezli işlemde parantez içini ilk adımda hesapla.",
            "İki sonucu yan yana yazıp karşılaştır.",
            "Tam çözüm: 8 + 4 × 5 = 8 + 20 = 28, (8 + 4) × 5 = 12 × 5 = 60'tır; parantez sırayı değiştirdiği için sonuçlar farklıdır.",
        ],
    ),
    dict(
        level=5,
        question="5 × ((18 − 6) ÷ 4) işleminin sonucu kaçtır?",
        dogru=5 * ((18 - 6) // 4),
        celdiriciler=[
            (5 * (18 - 6 // 4), "İç parantezi yok sayıp bölmeyi yalnız 6'ya uygulamış: 5 × (18 − 6 ÷ 4)."),
            ((5 * 18 - 6) // 4, "Çarpmayı parantezlerin önüne almış: (5 × 18 − 6) ÷ 4."),
            ((18 - 6) // 4, "İç işlemleri doğru yapmış ama 5 ile çarpma adımını atlamış."),
        ],
        explanation="İç parantezden başlanır: 18 − 6 = 12. Sonra dış parantez: 12 ÷ 4 = 3. "
                    "En son çarpma: 5 × 3 = 15.",
        difficultyReason="5 adım; ön bilgi: iç içe parantezlerde en içten dışa doğru ilerleme; çeldiriciler yakın (parantez atlama, adım atlama); beceri: hesaplama; sıralı işlem",
        hints=[
            "İç içe parantezlerde hangisinden başlanacağını hatırla.",
            "En içteki parantezi hesaplayıp yerine tek bir sayı yaz.",
            "Yeni oluşan parantezi hesapla.",
            "Parantezlerin tamamı bitince kalan çarpmayı yap.",
            "Tam çözüm: 18 − 6 = 12, 12 ÷ 4 = 3, 5 × 3 = 15 bulunur.",
        ],
    ),
    dict(
        level=5,
        question="45 ÷ 9 + 7 × 3 − 8 işleminin sonucu kaçtır?",
        dogru=45 // 9 + 7 * 3 - 8,
        celdiriciler=[
            ((45 // 9 + 7) * 3 - 8, "İşlemleri soldan sağa yapmış: bölmeden sonra toplayıp 3 ile çarpmış."),
            (45 // 9 + 7 * 3, "Bölme ve çarpmayı doğru yapmış ama son çıkarmayı atlamış."),
            (45 // 9 * 7 + 3 - 8, "Toplama işaretini çarpma sanmış: 45 ÷ 9 × 7 + 3 − 8."),
        ],
        explanation="Önce bölme ve çarpma soldan sağa: 45 ÷ 9 = 5 ve 7 × 3 = 21. "
                    "Sonra toplama ve çıkarma soldan sağa: 5 + 21 = 26, 26 − 8 = 18.",
        difficultyReason="5 adım; ön bilgi: iki öncelik düzeyinin dört işlemli bir ifadede birlikte uygulanması; çeldiriciler yakın (soldan sağa hesaplama, adım atlama); beceri: hesaplama; sıralı işlem",
        hints=[
            "İfadedeki bütün işlemleri türlerine göre iki gruba ayır.",
            "Öncelik düzeyi yüksek olan grubu soldan sağa hesapla.",
            "Bulduğun sonuçları ifadede yerlerine yaz.",
            "Kalan işlemleri de soldan sağa uygula.",
            "Tam çözüm: 45 ÷ 9 = 5 ve 7 × 3 = 21 bulunur; ardından 5 + 21 = 26 ve 26 − 8 = 18 elde edilir.",
        ],
    ),
    dict(
        level=2,
        question="84 ÷ 7 − 5 işleminin sonucu kaçtır?",
        dogru=84 // 7 - 5,
        celdiriciler=[
            (84 // (7 - 5), "Çıkarmayı bölmeden önce yapmış: 84 ÷ (7 − 5)."),
            (84 // 7, "Yalnız bölümü yazmış; çıkarma adımını yapmamış."),
            (84 // 7 + 5, "Çıkarma yerine toplama yapmış."),
        ],
        explanation="Bölme çıkarmadan önce yapılır: 84 ÷ 7 = 12; ardından 12 − 5 = 7.",
        difficultyReason="2 adım; ön bilgi: bölmenin çıkarmadan önce geldiği; çeldiriciler yakın (paranteze alma, adım atlama); beceri: hesaplama",
        hints=[
            "İşlemde parantez olmadığına dikkat et.",
            "Bölme ile çıkarmadan hangisinin öncelikli olduğunu belirle.",
            "Bölme işlemini yapıp sonucunu yerine yaz.",
            "Kalan çıkarmayı son adımda uygula.",
            "Tam çözüm: önce 84 ÷ 7 = 12 yapılır, sonra 12 − 5 = 7 bulunur.",
        ],
    ),
    dict(
        level=3,
        question="96 ÷ (4 × 3) işleminin sonucu kaçtır?",
        dogru=96 // (4 * 3),
        celdiriciler=[
            (96 // 4 * 3, "Parantezi yok sayıp soldan sağa ilerlemiş: 96 ÷ 4 × 3."),
            (4 * 3, "Yalnız parantez içini yazmış; bölme adımını yapmamış."),
            (96 // 4 + 3, "Parantez içindeki çarpmayı toplamaya çevirip soldan sağa hesaplamış."),
        ],
        explanation="Parantez içi önce yapılır: 4 × 3 = 12; ardından 96 ÷ 12 = 8.",
        difficultyReason="3 adım; ön bilgi: parantezin bölenin tamamını kapsaması; çeldiriciler yakın (parantezi yok sayma); beceri: hesaplama",
        hints=[
            "Parantezin bölme işleminde neyi kapsadığına dikkat et.",
            "Parantez içindeki çarpmayı ilk adımda yap.",
            "Bulduğun sayıyı bölen olarak yerine koy.",
            "Bölme işlemini son adımda uygula.",
            "Tam çözüm: parantez içi 4 × 3 = 12 eder; sonra 96 ÷ 12 = 8 bulunur.",
        ],
    ),
    dict(
        level=5,
        question="Aşağıdaki işlemlerden hangisinin sonucu 30'dur?",
        choices=[
            "4 × 5 + 10",
            "4 × (5 + 10)",
            "4 + 5 × 10",
            "(4 + 5) × 10",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Parantez toplamayı öne alır: 4 × 15 = 60 eder.",
            "Çarpma önce yapılır: 4 + 50 = 54 eder.",
            "Parantez toplamayı öne alır: 9 × 10 = 90 eder.",
        ],
        explanation="Aynı sayılarla kurulan bu dört ifade, işlem sırası farklı olduğu için farklı sonuçlar "
                    "verir. 4 × 5 + 10 işleminde çarpma önce yapılır: 20 + 10 = 30.",
        difficultyReason="5 adım; ön bilgi: aynı sayılarla kurulan ifadelerin sıraya göre farklı sonuç vermesi; çeldiriciler çok yakın (aynı sayılar, farklı parantez); beceri: hesaplama; seçenek eleme",
        hints=[
            "Dört seçenekte de aynı sayıların kullanıldığını fark et.",
            "Her seçeneği ayrı ayrı, öncelik kuralına göre hesapla.",
            "Parantezli seçeneklerde parantez içini ilk adımda yap.",
            "Bulduğun dört sonucu istenen sayıyla karşılaştır.",
            "Tam çözüm: 4 × 5 + 10 = 20 + 10 = 30'dur; diğerleri sırasıyla 60, 54 ve 90 verir.",
        ],
    ),
    dict(
        level=1,
        question="9 × 3 + 6 işleminin sonucu kaçtır?",
        dogru=9 * 3 + 6,
        celdiriciler=[
            (9 * (3 + 6), "Toplamayı çarpmadan önce yapmış: 9 × (3 + 6)."),
            (9 + 3 + 6, "Çarpma yerine toplama yapmış."),
            (9 * 3, "Yalnız çarpımı yazmış; toplama adımını yapmamış."),
        ],
        explanation="Çarpma toplamadan önce yapılır: 9 × 3 = 27; ardından 27 + 6 = 33.",
        difficultyReason="2 adım; ön bilgi: çarpmanın toplamadan önce geldiği; çeldiriciler yakın (toplamayı öne alma); beceri: hesaplama",
        hints=[
            "İşlemde parantez bulunup bulunmadığına bak.",
            "Çarpma ile toplamadan hangisinin öncelikli olduğunu hatırla.",
            "Çarpımı hesaplayıp yerine yaz.",
            "Kalan toplamayı son adımda uygula.",
            "Tam çözüm: önce 9 × 3 = 27 yapılır, sonra 27 + 6 = 33 bulunur.",
        ],
    ),
    dict(
        level=4,
        question="Bir defter 12 TL, bir kalem 4 TL'dir. 3 defter ve 2 kalem alan bir kişi kaç TL öder?",
        dogru=3 * 12 + 2 * 4,
        celdiriciler=[
            ((3 + 2) * (12 + 4), "Ürün sayılarını ve fiyatları ayrı ayrı toplayıp çarpmış: (3 + 2) × (12 + 4)."),
            (3 * 12, "Yalnız defterlerin tutarını hesaplamış; kalemleri toplama katmamış."),
            (12 + 4, "Birer defter ile birer kalemin fiyatını toplamış; adetleri hesaba katmamış."),
        ],
        explanation="Her ürün için adet ile fiyat çarpılır, sonra tutarlar toplanır: "
                    "3 × 12 + 2 × 4 = 36 + 8 = 44 TL.",
        difficultyReason="4 adım; ön bilgi: gerçek durumda çarpmanın toplamadan önce gelmesi; çeldiriciler yakın (adet ve fiyatları karıştırma); beceri: model kurma; hesaplama",
        hints=[
            "Her ürün türü için ayrı bir hesap yapman gerektiğini fark et.",
            "Defterlerin toplam tutarını bul.",
            "Kalemlerin toplam tutarını bul.",
            "İki tutarı toplamayı dene.",
            "Tam çözüm: defterler 3 × 12 = 36 TL, kalemler 2 × 4 = 8 TL tutar; toplam ödeme 36 + 8 = 44 TL'dir.",
        ],
    ),
    dict(
        level=2,
        question="İşlem önceliğine göre aşağıdakilerden hangisi doğrudur?",
        choices=[
            "Çarpma her zaman bölmeden önce yapılır.",
            "Toplama her zaman çıkarmadan önce yapılır.",
            "Önce parantez içi; sonra çarpma ile bölme soldan sağa; en son toplama ile çıkarma soldan sağa yapılır.",
            "Bütün işlemler her durumda soldan sağa yapılır.",
        ],
        correct=2,
        distractorWhy=[
            "Çarpma ile bölme aynı öncelik düzeyindedir; aralarındaki sırayı soldan sağa okuma belirler.",
            "Toplama ile çıkarma aynı öncelik düzeyindedir; aralarındaki sırayı soldan sağa okuma belirler.",
            "doğru",
            "Soldan sağa kuralı yalnız aynı öncelik düzeyindeki işlemler için geçerlidir; parantez ve çarpma bu kuralın önüne geçer.",
        ],
        explanation="İşlem önceliği üç aşamalıdır: önce parantez içi, sonra çarpma ile bölme soldan sağa, "
                    "en son toplama ile çıkarma soldan sağa. Çarpmanın bölmeden, toplamanın çıkarmadan "
                    "önce geldiği düşünülmemelidir.",
        difficultyReason="2 adım; ön bilgi: öncelik düzeylerinin sırası ve aynı düzeyde soldan sağa kuralı; çeldiriciler yakın (yaygın yanlış genellemeler); beceri: kural hatırlama",
        hints=[
            "Öncelik sırasında ilk basamağın ne olduğunu söyle.",
            "Çarpma ile bölmenin aynı düzeyde mi ayrı düzeyde mi olduğunu düşün.",
            "Aynı düzeydeki işlemlerde sırayı neyin belirlediğini hatırla.",
            "İçinde 'her zaman' geçen genellemeleri tek tek sına.",
            "Tam çözüm: sıra parantez içi, ardından çarpma-bölme soldan sağa, en son toplama-çıkarma soldan sağadır.",
        ],
    ),
    dict(
        level=5,
        question="120 ÷ (8 + 4) × 2 işleminin sonucu kaçtır?",
        dogru=120 // (8 + 4) * 2,
        celdiriciler=[
            (120 // ((8 + 4) * 2), "Çarpmayı bölmeden önce yapmış; oysa ikisi aynı düzeydedir ve soldan sağa gidilir."),
            (120 // 8 + 4 * 2, "Parantezi yok sayıp her işlemi ayrı hesaplamış."),
            (120 // (8 + 4), "Parantez ve bölmeyi doğru yapmış ama son çarpma adımını atlamış."),
        ],
        explanation="Önce parantez: 8 + 4 = 12. Sonra bölme ile çarpma aynı düzeyde olduğundan soldan sağa: "
                    "120 ÷ 12 = 10, ardından 10 × 2 = 20.",
        difficultyReason="5 adım; ön bilgi: parantezden sonra aynı düzeydeki bölme ve çarpmanın soldan sağa uygulanması; çeldiriciler çok yakın (çarpmayı öne alma); beceri: hesaplama; kural uygulama",
        hints=[
            "Parantez içini ilk adımda hesapla.",
            "Geriye kalan iki işlemin öncelik düzeylerini karşılaştır.",
            "Aynı düzeydeyseler hangi yönde ilerleneceğini hatırla.",
            "Soldaki işlemden başlayarak adım adım devam et.",
            "Tam çözüm: 8 + 4 = 12 bulunur; sonra soldan sağa 120 ÷ 12 = 10 ve 10 × 2 = 20 elde edilir.",
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
    secenekler = [S(v) for v in degerler]
    gerekceler = ["doğru"] + [g for _, g in s["celdiriciler"]]
    return secenekler, 0, gerekceler


AILELER = [
    ("tr.g05.mat.5-2-1", "MAT.5.2.1", "tr.g05.mat.5.2.note.01",
     "Eşitliğin korunumu ve işlem özellikleri", A21),
    ("tr.g05.mat.5-2-2", "MAT.5.2.2", "tr.g05.mat.5.2.note.02",
     "Doğal sayılarda işlem önceliği", A22),
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
