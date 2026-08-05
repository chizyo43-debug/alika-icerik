# -*- coding: utf-8 -*-
"""A3 parti 2 — MAT.5.5.1 'Kategorik veri' ailesinin yeniden üretimi.

Önceki hâl: 21 sorunun tamamı "Bir kulüp anketinde kitap: X, spor: Y,
müzik: Z, resim: W" kökünü paylaşıyordu; yalnız sayılar değişiyordu.
Beş alt soru tipi (en çok / en az / toplam / fark / iki kategori) dönüşümlü
tekrarlanmış, 9 soruda seçenek kümesi birebir aynı olmuştu
('kitap','müzik','resim','spor'). 2., 3. ve 4. ipuçları 21 sorunun
hepsinde aynı iki cümleydi.

Yeni hâl: notun (tr.g05.mat.5.5.note.01) altı öğretim adımını kapsayan
21 farklı soru tipi — araştırma sorusu tasarımı, kategori tanımı çakışması,
çetele okuma, sıklık toplamı denetimi, eksik kategori, fark, oran, kategori
birleştirme, grafik ölçeği, eksen, grafik türü seçimi, örneklem sınırı,
yorum kapsamı. Her sorunun bağlamı ayrı; çeldiriciler adlandırılmış bir
kavram yanılgısına bağlı.

choices + correct + distractorWhy + hints + explanation tek birimde üretildi
(AUTHORING_RULES.md §1 atomiklik ilkesi).
"""

KAYNAK = "https://tymm.meb.gov.tr/upload/program/2024programmat5678Onayli.pdf"

SORULAR = [
    dict(
        level=1,
        question="Bir sınıfta yapılacak araştırmada kategorik veri toplayan soru aşağıdakilerden hangisidir?",
        choices=[
            "Boyun kaç santimetre?",
            "Okula hangi araçla geliyorsun?",
            "Kaç kardeşin var?",
            "Günde kaç saat ders çalışıyorsun?",
        ],
        correct=1,
        distractorWhy=[
            "Boy santimetreyle ölçülen sayısal bir büyüklüktür; kişileri tür ya da tercihe göre gruplamaz.",
            "doğru",
            "Kardeş sayısı sayılarak bulunan sayısal bir veridir; yanıt bir grup adı değildir.",
            "Çalışma süresi saatle ölçülür; yanıtlar bir ölçü değeridir, kategori değildir.",
        ],
        explanation="Kategorik veri kişileri tür, tercih ya da özellik bakımından gruplandırır. "
                    "Okula hangi araçla geliyorsun sorusunun yanıtları servis, yürüyerek, bisiklet gibi "
                    "kategorilerdir; diğer üç soru sayısal büyüklük ister.",
        difficultyReason="1 adım; ön bilgi: kategorik ile sayısal değişken ayrımı; çeldiriciler tek yönlü (hepsi sayısal); beceri: tanım uygulama",
        hints=[
            "Kategorik verinin yanıtı bir sayı mı yoksa bir grup adı mı olur, onu hatırla.",
            "Her seçeneği tek tek al ve yanıtının hangi türde çıkacağını söyle.",
            "Yanıtı santimetre, saat ya da adet ile ifade edilen soruları ele.",
            "Geriye kalan soruda yanıtların birer taşıt adı olacağını fark et.",
            "Tam çözüm: boy, kardeş sayısı ve çalışma süresi sayısal ölçülerdir. Okula hangi araçla geliyorsun sorusu servis, yürüyerek, bisiklet gibi gruplar verdiği için kategorik veri toplar.",
        ],
    ),
    dict(
        level=2,
        question="Bir anket 'Hangi tür film seversin?' sorusuna komedi, çizgi film, korku, animasyon seçeneklerini koymuştur. Bu seçenek listesinin temel sorunu nedir?",
        choices=[
            "Seçenek sayısı çift olmamalıdır.",
            "Çizgi film ile animasyon aynı yanıtı iki kategoriye böler.",
            "Seçenekler alfabetik sıraya konmamıştır.",
            "Korku seçeneği listeye en sona yazılmalıdır.",
        ],
        correct=1,
        distractorWhy=[
            "Seçenek sayısının tek ya da çift olması sayımı etkilemez; kategori listesinde böyle bir koşul yoktur.",
            "doğru",
            "Alfabetik sıra yalnız okumayı kolaylaştırır; kategorilerin birbirinden ayrı olmasıyla ilgisi yoktur.",
            "Seçeneklerin yazılma sırası sıklıkları değiştirmez; sorun sıralamada değildir.",
        ],
        explanation="Kategoriler birbiriyle çakışmamalıdır: her yanıt yalnız bir kategoriye girebilmelidir. "
                    "Bir çizgi film aynı zamanda animasyondur; aynı filmi seven iki öğrenci farklı seçenekleri "
                    "işaretleyebileceği için sıklıklar bölünür ve tablo yanıltıcı olur.",
        difficultyReason="2 adım; ön bilgi: kategorilerin ayrık ve kapsayıcı olması koşulu; çeldiriciler biçimsel kusurlar öne sürüyor; beceri: eleştirel değerlendirme",
        hints=[
            "İyi bir kategori listesinde her yanıtın kaç seçeneğe girebileceğini düşün.",
            "Seçenek adlarını ikişer ikişer karşılaştır: hangisi diğerinin yerine de kullanılabilir?",
            "Bir öğrencinin sevdiği filmi iki farklı seçeneğe yazabilmesi tabloyu nasıl etkiler?",
            "Aynı anlama gelen iki seçeneğin sıklığı böldüğünü göz önüne al.",
            "Tam çözüm: çizgi film ile animasyon aynı türü adlandırır. Aynı yanıt iki kategoriye dağıldığı için sıklıklar bölünür; kategoriler birbirinden ayrık olmalıdır.",
        ],
    ),
    dict(
        level=1,
        question="Çetele işaretiyle sayım yapılırken beşinci işaret nasıl konur?",
        choices=[
            "Daha kalın çizilir.",
            "Ayrı bir satıra yazılır.",
            "İlk dördünün üzerini çizecek biçimde konur.",
            "Rakamla 5 yazılır.",
        ],
        correct=2,
        distractorWhy=[
            "Çizginin kalınlığı sayıma bilgi katmaz; işaretler tek tek sayıldığı için beşli grup yine görünmez.",
            "Yeni satıra geçmek beşli grubu göstermez; sayan kişi yine baştan tek tek saymak zorunda kalır.",
            "doğru",
            "Sayım sırasında rakama geçilirse çetelenin amacı olan hızlı ve hatasız sayma ortadan kalkar.",
        ],
        explanation="Çetelede beşinci işaret ilk dördünün üzerini çizerek beşli bir grup oluşturur. "
                    "Böylece sayarken beşer beşer ilerlenir ve tek tek sayma hatası azalır.",
        difficultyReason="1 adım; ön bilgi: çetele işaretinin beşli gruplama kuralı; çeldiriciler yakın (hepsi işaretin biçimini değiştiriyor); beceri: kural hatırlama",
        hints=[
            "Çetelenin sayımı kolaylaştırmak için ne yaptığını hatırla.",
            "Beşli gruplar hâlinde saymanın tek tek saymaya göre üstünlüğünü düşün.",
            "Bir işaretin diğer dördüyle nasıl bir grup oluşturabileceğini göz önüne getir.",
            "İşaretin yönünü değiştirmenin gruplama sağlayıp sağlamadığını sorgula.",
            "Tam çözüm: beşinci işaret ilk dördünün üzerine çapraz çizilir. Ortaya çıkan beşli demet sayesinde toplam beşer beşer sayılır.",
        ],
    ),
    dict(
        level=2,
        question="Bir sınıfta göz rengi sayılmıştır. Kahverengi için 2 tam beşli demet ve 2 tek çetele işareti bulunmaktadır. Kahverengi gözlü kaç öğrenci vardır?",
        choices=[
            "10",
            "22",
            "12",
            "7",
        ],
        correct=2,
        distractorWhy=[
            "Yalnız beşli demetleri saymış: 2 × 5 = 10; artan iki tek işareti eklememiş.",
            "Her beşli demeti on kabul etmiş: 10 + 10 + 2 = 22.",
            "doğru",
            "Bir beşli demeti saymayı unutmuş: 5 + 2 = 7.",
        ],
        explanation="Her demet 5 işaret taşır: 2 × 5 = 10. Artan 2 tek işaret eklenir: 10 + 2 = 12.",
        difficultyReason="2 adım; ön bilgi: çetele demetinin beş işaret olduğu; çeldiriciler yakın (demet değeri ve artan işaret hataları); beceri: hesaplama",
        hints=[
            "Bir çetele demetinin kaç işaretten oluştuğunu belirle.",
            "Demetlerin taşıdığı toplam işaret sayısını hesapla.",
            "Demetlerin dışında kalan tek işaretleri ayrıca say.",
            "İki sonucu topladığında sayımın tamamını elde edeceğini düşün.",
            "Tam çözüm: 2 demet 2 × 5 = 10 işaret eder; artan 2 tek işaret eklenince 10 + 2 = 12 öğrenci bulunur.",
        ],
    ),
    dict(
        level=3,
        question="Bir öğretmen 28 öğrenciyle anket yaptığını belirtiyor. Sıklık tablosunda kategoriler için 9, 7, 6 ve 4 yazılıdır. Bu tablo için ne söylenebilir?",
        choices=[
            "Sıklıkların toplamı 26 olduğundan iki öğrencinin yanıtı tabloya işlenmemiştir.",
            "Tablo doğrudur; sıklıkların toplamı katılımcı sayısına eşittir.",
            "Sıklıklar 28'i aştığından iki yanıt iki kez sayılmıştır.",
            "Katılımcı sayısı kategori sayısına tam bölünmediği için tablo geçersizdir.",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Sıklıkların toplamı 26'dır; bu sayı bildirilen 28 katılımcıya eşit olmadığı için tablo eksiktir.",
            "Toplam 28'in üstünde değil altındadır; fazla sayım değil eksik kayıt söz konusudur.",
            "Kategorilere düşen sayıların eşit olması gerekmez; tablonun geçerliliği toplamla ölçülür.",
        ],
        explanation="Sıklıkların toplamı katılımcı sayısına eşit olmalıdır: 9 + 7 + 6 + 4 = 26. "
                    "Bildirilen katılımcı 28 olduğuna göre 28 − 26 = 2 yanıt tabloya geçirilmemiştir.",
        difficultyReason="3 adım; ön bilgi: sıklık toplamının katılımcı sayısına eşitliği; çeldiriciler yakın (eksik yerine fazla sayım yorumu); beceri: hesaplama; akıl yürütme",
        hints=[
            "Sıklık tablosunda toplam sayının neye eşit olması gerektiğini hatırla.",
            "Tablodaki dört sayıyı topla.",
            "Bulduğun toplamı öğretmenin bildirdiği katılımcı sayısıyla karşılaştır.",
            "İki sayı arasındaki farkın ne anlama geldiğini düşün: eksik mi, fazla mı?",
            "Tam çözüm: 9 + 7 + 6 + 4 = 26 < 28. Aradaki 2 fark, iki öğrencinin yanıtının tabloya işlenmediğini gösterir.",
        ],
    ),
    dict(
        level=2,
        question="Bir okulda 40 öğrenciye en sevdiği mevsim sorulmuştur: ilkbahar 11, yaz 15, sonbahar 6 yanıtı alınmıştır. Kış diyen kaç öğrenci vardır?",
        choices=[
            "32",
            "8",
            "4",
            "10",
        ],
        correct=1,
        distractorWhy=[
            "Verilen üç sıklığın toplamını yazmış; bu sayı katılımcıların tamamı değil, kış dışında kalanlardır.",
            "doğru",
            "En büyük ile en küçük sıklığın farkını almış: 15 − 11 = 4.",
            "Katılımcı sayısını kategori sayısına bölerek her mevsime eşit sıklık düştüğünü varsaymış: 40 ÷ 4 = 10.",
        ],
        explanation="Sıklıkların toplamı katılımcı sayısına eşittir. Bilinen üç kategori 11 + 15 + 6 = 32 eder; "
                    "kış için 40 − 32 = 8 öğrenci kalır.",
        difficultyReason="2 adım; ön bilgi: sıklık toplamı ile katılımcı sayısı ilişkisi; çeldiriciler yakın (ara toplamı yanıt sanma); beceri: hesaplama",
        hints=[
            "Dört kategorinin sıklıkları toplandığında hangi sayının çıkması gerektiğini belirle.",
            "Verilen üç sıklığı topla.",
            "Bulduğun toplamı katılımcı sayısından çıkarmayı dene.",
            "Çıkan farkın hangi kategoriye ait olduğunu kontrol et.",
            "Tam çözüm: 11 + 15 + 6 = 32; kış diyen öğrenci sayısı 40 − 32 = 8'dir.",
        ],
    ),
    dict(
        level=2,
        question="Bir kütüphane kaydına göre macera 24, bilim kurgu 17, şiir 9, biyografi 13 kitap ödünç alınmıştır. Macera türü biyografiden kaç kitap fazla ödünç alınmıştır?",
        choices=[
            "37",
            "7",
            "11",
            "24",
        ],
        correct=2,
        distractorWhy=[
            "Fark yerine iki sıklığı toplamış: 24 + 13 = 37.",
            "Macerayı biyografi yerine bilim kurguyla karşılaştırmış: 24 − 17 = 7.",
            "doğru",
            "Yalnız macera türünün sıklığını yazmış; karşılaştırma işlemini yapmamış.",
        ],
        explanation="'Kaç fazla' sorusu çıkarma gerektirir: 24 − 13 = 11 kitap.",
        difficultyReason="2 adım; ön bilgi: 'kaç fazla' ifadesinin çıkarma işlemine karşılık gelmesi; çeldiriciler yakın (yanlış kategori eşleştirme); beceri: hesaplama",
        hints=[
            "'Kaç fazla' ifadesinin hangi işlemi gerektirdiğini belirle.",
            "Soruda karşılaştırılan iki türün adını tek tek işaretle.",
            "Bu iki türe ait sıklıkları tablodan ayır.",
            "Büyük sayıdan küçük sayıyı çıkarmayı dene.",
            "Tam çözüm: macera 24, biyografi 13 kitaptır; fark 24 − 13 = 11'dir.",
        ],
    ),
    dict(
        level=1,
        question="Bir sınıfta en sevilen ders sorulmuştur: görsel sanatlar 4, beden eğitimi 17, müzik 9, fen bilimleri 11. En çok sevilen ders hangisidir?",
        choices=[
            "fen bilimleri",
            "müzik",
            "beden eğitimi",
            "görsel sanatlar",
        ],
        correct=2,
        distractorWhy=[
            "Fen bilimleri 11 kişiyle ikinci sıradadır; 17'nin altındadır.",
            "Müzik 9 kişi almıştır; listedeki en büyük sayı bu değildir.",
            "doğru",
            "Görsel sanatlar 4 kişiyle listenin en küçük sıklığına sahiptir.",
        ],
        explanation="Sıklıklar karşılaştırıldığında en büyük sayı 17'dir; bu sayı beden eğitimi dersine aittir.",
        difficultyReason="1 adım; ön bilgi: sıklıkların büyüklük karşılaştırması; çeldiriciler belirgin (sıklıklar birbirinden uzak); beceri: seçenek eleme",
        hints=[
            "'En çok' ifadesinin sıklıkların hangisini işaret ettiğini düşün.",
            "Dört sayıyı yan yana yazarak karşılaştırmayı kolaylaştır.",
            "Küçük sayılara ait dersleri sırayla ele.",
            "Geriye kalan en büyük sayının hangi derse ait olduğuna bak.",
            "Tam çözüm: 4, 17, 9 ve 11 sayıları içinde en büyüğü 17'dir; bu sıklık beden eğitimi dersine aittir.",
        ],
    ),
    dict(
        level=1,
        question="Bir okulda geri dönüşüm kutularına atılan malzemeler sayılmıştır: kâğıt 26, plastik 19, cam 7, metal 12. En az toplanan malzeme hangisidir?",
        choices=[
            "metal",
            "cam",
            "plastik",
            "kâğıt",
        ],
        correct=1,
        distractorWhy=[
            "Metal 12 kayıtla üçüncü sıradadır; daha küçük bir sıklık vardır.",
            "doğru",
            "Plastik 19 kayıtla ikinci en büyük sıklığa sahiptir.",
            "Kâğıt 26 kayıtla en çok toplanan malzemedir; soru en azı istiyor.",
        ],
        explanation="Sıklıklar 26, 19, 7 ve 12'dir. En küçük sayı 7 olduğundan en az toplanan malzeme camdır.",
        difficultyReason="1 adım; ön bilgi: sıklık sıralaması; çeldiriciler yakın (en çok ile en az karıştırma); beceri: seçenek eleme",
        hints=[
            "Soruda en büyük mü en küçük mü sıklığın istendiğini işaretle.",
            "Dört sayıyı küçükten büyüğe sıralamayı dene.",
            "Sıralamanın başındaki sayıya odaklan.",
            "O sayının hangi malzemeye ait olduğunu tablodan bul.",
            "Tam çözüm: 7 < 12 < 19 < 26 sıralamasında en küçük sıklık 7'dir ve cam malzemesine aittir.",
        ],
    ),
    dict(
        level=3,
        question="Bir sınıfta 24 öğrencinin sevdiği içecek sayılmıştır: süt 5, ayran 13, meyve suyu 6. Aşağıdaki yorumlardan hangisi bu verilerle doğrulanır?",
        choices=[
            "Süt seçenler sınıfın dörtte birinden fazladır.",
            "Meyve suyu seçenler ayran seçenlerin tam yarısıdır.",
            "Süt ile meyve suyu seçenler birlikte ayran seçenlerden fazladır.",
            "Ayran seçenler sınıfın yarısından fazladır.",
        ],
        correct=3,
        distractorWhy=[
            "Sınıfın dörtte biri 24 ÷ 4 = 6 kişidir; süt seçen 5 kişi bu sayının altında kalır.",
            "Ayran seçenlerin yarısı 13 ÷ 2 = 6,5'tir; meyve suyu sıklığı olan 6 buna eşit değildir.",
            "Süt ile meyve suyu birlikte 5 + 6 = 11 kişidir; bu sayı 13'ten küçüktür.",
            "doğru",
        ],
        explanation="Sınıfın yarısı 24 ÷ 2 = 12 kişidir. Ayran seçen 13 kişi bu sayıdan fazla olduğundan "
                    "yalnız ayranla ilgili yorum verilerle doğrulanır.",
        difficultyReason="3 adım; ön bilgi: bir sayının yarısı ve dörtte birini bulma; çeldiriciler yakın (her biri ayrı bir kesir karşılaştırması); beceri: hesaplama; akıl yürütme",
        hints=[
            "Her yorumu ayrı bir hesap gibi ele al ve tek tek dene.",
            "Sınıf mevcudunun yarısını ve dörtte birini önceden hesapla.",
            "Bulduğun bu iki sayıyı tablodaki sıklıklarla karşılaştır.",
            "Yanlış çıkan yorumları elediğinde geriye kaç tane kaldığına bak.",
            "Tam çözüm: yarım 12, dörtte bir 6'dır. Süt 5 < 6, meyve suyu 6 ≠ 6,5, süt+meyve suyu 11 < 13. Ayran 13 > 12 olduğundan ayran seçenler sınıfın yarısından fazladır.",
        ],
    ),
    dict(
        level=3,
        question="40 kişilik bir grupta 10 kişi evcil hayvan olarak kuş seçmiştir. Kuş seçenlerin oranı yüzde kaçtır?",
        choices=[
            "10",
            "25",
            "40",
            "4",
        ],
        correct=1,
        distractorWhy=[
            "Kişi sayısını doğrudan yüzde olarak yazmış; oran hesabı yapmamış.",
            "doğru",
            "Grubun büyüklüğünü yüzde değeri sanmış.",
            "Grup mevcudunu kuş seçen sayısına bölüp bölümü yüzde olarak yazmış: 40 ÷ 10 = 4.",
        ],
        explanation="Oran, parçanın bütüne bölünmesiyle bulunur: 10 ÷ 40 = 1/4. Bu kesir yüzde olarak "
                    "1/4 × 100 = %25'e karşılık gelir.",
        difficultyReason="3 adım; ön bilgi: parça-bütün oranı ve yüzdeye çevirme; çeldiriciler yakın (bölme yönünü ters çevirme); beceri: hesaplama",
        hints=[
            "Oran hesabında hangi sayının parça, hangisinin bütün olduğunu belirle.",
            "Parçayı bütüne bölerek bir kesir yaz.",
            "Yazdığın kesri sadeleştir.",
            "Sadeleşen kesri yüzdeye çevirmek için 100 ile çarpmayı dene.",
            "Tam çözüm: 10 ÷ 40 = 1/4; 1/4 × 100 = 25 olduğundan oran %25'tir.",
        ],
    ),
    dict(
        level=4,
        question="Ulaşım anketinde servis 14, yürüyerek 8, bisiklet 5, otobüs 3 öğrenci sayılmıştır. Yürüyerek ve bisiklet kategorileri 'kendi imkânıyla' adı altında birleştirilirse en büyük sıklık kaç olur?",
        choices=[
            "13",
            "19",
            "14",
            "8",
        ],
        correct=2,
        distractorWhy=[
            "Birleştirilen kategorinin sıklığını yazmış: 8 + 5 = 13; oysa bu sayı servisin 14'ünden küçüktür.",
            "Birleştirmeye servisi de katmış: 14 + 5 = 19.",
            "doğru",
            "Birleştirmeyi hiç yapmadan yalnız yürüyerek sıklığını almış.",
        ],
        explanation="Birleştirme sonrası kategoriler servis 14, kendi imkânıyla 8 + 5 = 13, otobüs 3 olur. "
                    "Bu üç sayının en büyüğü 14'tür.",
        difficultyReason="4 adım; ön bilgi: kategori birleştirmenin sıklıkları topladığı; çeldiriciler yakın (birleşik sıklığı doğrudan yanıt sanma); beceri: hesaplama; akıl yürütme",
        hints=[
            "Kategori birleştirmenin sıklıklara ne yaptığını düşün.",
            "Birleştirilecek iki kategorinin sıklıklarını topla.",
            "Birleştirmeden etkilenmeyen kategorileri de yeni tabloya yaz.",
            "Yeni tablodaki bütün sıklıkları karşılaştır; en büyüğü ara.",
            "Tam çözüm: birleşik kategori 8 + 5 = 13 olur. Yeni tablo 14, 13 ve 3 sıklıklarını içerdiğinden en büyük sıklık 14'tür.",
        ],
    ),
    dict(
        level=4,
        question="Bir kantin kaydında poğaça 18, simit 22, sandviç 12, tost 15 adet satılmıştır. Satış sayıları küçükten büyüğe hangi seçenekte doğru sıralanmıştır?",
        choices=[
            "simit, poğaça, tost, sandviç",
            "sandviç, tost, poğaça, simit",
            "sandviç, poğaça, tost, simit",
            "tost, sandviç, poğaça, simit",
        ],
        correct=1,
        distractorWhy=[
            "Sıralamayı büyükten küçüğe yapmış; soruda küçükten büyüğe isteniyor.",
            "doğru",
            "18 ile 15'in yerini değiştirmiş; poğaça tosttan önce yazılamaz.",
            "12 ile 15'in yerini değiştirmiş; sıralamanın başına daha büyük sayı gelmiş.",
        ],
        explanation="Satış sayıları 12, 15, 18 ve 22'dir. Küçükten büyüğe sıralandığında sandviç, tost, "
                    "poğaça, simit dizilişi elde edilir.",
        difficultyReason="3 adım; ön bilgi: doğal sayı sıralaması; çeldiriciler yakın (yön hatası ve tek yer değiştirme); beceri: sıralama",
        hints=[
            "Soruda sıralamanın hangi yönde istendiğini işaretle.",
            "Dört satış sayısını yalnız rakam olarak alt alta yaz.",
            "Bu sayıları küçükten büyüğe diz.",
            "Her sayının yanına ait olduğu ürünün adını yeniden yerleştir.",
            "Tam çözüm: 12 < 15 < 18 < 22 sıralaması sandviç, tost, poğaça, simit dizilişini verir.",
        ],
    ),
    dict(
        level=2,
        question="Kategorilerin sıklıklarını yan yana karşılaştırmak için en uygun gösterim hangisidir?",
        choices=[
            "çizgi grafiği",
            "sayı doğrusu",
            "çetele işaretleri",
            "sütun grafiği",
        ],
        correct=3,
        distractorWhy=[
            "Çizgi grafiği zaman içindeki değişimi gösterir; kategoriler arasında böyle bir sıra bulunmaz.",
            "Sayı doğrusu tek bir sayının yerini gösterir; birden çok grubu yan yana koyamaz.",
            "Çetele sayım aşamasında tutulur; işaretler görsel bir karşılaştırma sağlamaz.",
            "doğru",
        ],
        explanation="Sütun grafiğinde kategoriler bir eksende, sıklıklar diğer eksende yer alır. "
                    "Aynı genişlikteki sütunların yükseklikleri doğrudan karşılaştırılabilir.",
        difficultyReason="2 adım; ön bilgi: gösterim türlerinin kullanım amacı; çeldiriciler yakın (hepsi geçerli birer matematiksel gösterim); beceri: uygun temsil seçme",
        hints=[
            "Karşılaştırmanın kategoriler arasında mı zaman içinde mi yapıldığını belirle.",
            "Her gösterimin hangi tür veriyi anlatmak için kullanıldığını hatırla.",
            "Zaman değişimi için kullanılan gösterimi ele.",
            "Tek bir sayıyı gösteren ve yalnız sayım için tutulan gösterimleri de ele.",
            "Tam çözüm: kategorilerin sıklıkları sütun grafiğinde yan yana çizilir; sütun yükseklikleri doğrudan karşılaştırılabildiği için en uygun gösterim budur.",
        ],
    ),
    dict(
        level=3,
        question="Bir öğrenci sütun grafiği çizerken sıklık eksenini 0, 2, 5, 6, 10 diye işaretlemiştir. Bu grafiğin en önemli kusuru nedir?",
        choices=[
            "Kategori sayısı yetersizdir.",
            "Sütunlar renklendirilmemiştir.",
            "Ölçek aralıkları eşit değildir.",
            "Grafiğe başlık yazılmamıştır.",
        ],
        correct=2,
        distractorWhy=[
            "Kaç kategori bulunduğu soruda bildirilmemiştir; anlatılan kusur kategorilerle ilgili değildir.",
            "Renklendirme biçimsel bir tercihtir; sütun yüksekliklerinin okunmasını değiştirmez.",
            "doğru",
            "Başlık eksikliği ayrı bir eksiklik olurdu; burada anlatılan kusur eksen işaretlerinin arasındadır.",
        ],
        explanation="Sütun grafiğinde ölçek eşit aralıklarla ilerlemelidir. 0, 2, 5, 6, 10 dizisinde aralıklar "
                    "sırasıyla 2, 3, 1 ve 4 olduğundan eşit yükseklikteki iki sütun farklı sıklıkları temsil eder "
                    "ve karşılaştırma yanıltıcı olur.",
        difficultyReason="3 adım; ön bilgi: sütun grafiğinde eşit ölçek koşulu; çeldiriciler biçimsel eksiklikler öne sürüyor; beceri: eleştirel değerlendirme",
        hints=[
            "Sütun grafiğinde eksen işaretlerinin nasıl ilerlemesi gerektiğini hatırla.",
            "Verilen sayı dizisinde ardışık işaretler arasındaki farkları tek tek hesapla.",
            "Bulduğun farkların birbirine eşit olup olmadığına bak.",
            "Farklar eşit değilse aynı yükseklikteki iki sütunun ne anlatacağını düşün.",
            "Tam çözüm: 0, 2, 5, 6, 10 dizisinde farklar 2, 3, 1 ve 4'tür. Ölçek aralıkları eşit olmadığı için sütun yükseklikleri sıklıklarla orantılı çıkmaz.",
        ],
    ),
    dict(
        level=3,
        question="Bir sütun grafiğinde yatay eksende kategori adları yer alıyorsa dikey eksende ne bulunmalıdır?",
        choices=[
            "sıklık ölçeği",
            "kategori adlarının tekrarı",
            "katılımcıların adları",
            "araştırma sorusunun metni",
        ],
        correct=0,
        distractorWhy=[
            "doğru",
            "Kategori adları zaten yatay eksende yazılmıştır; iki eksende aynı bilgi tekrarlanmaz.",
            "Grafik tek tek kişileri değil, her gruba düşen sayıyı gösterir; kişi adları eksene yazılmaz.",
            "Araştırma sorusu grafiğin başlığında yer alır; eksende bir ölçek bulunması gerekir.",
        ],
        explanation="Sütun grafiğinin iki ekseni farklı bilgi taşır: biri kategorileri, diğeri her kategoriye "
                    "düşen sıklığı gösteren ölçeği içerir. Kategoriler yataydaysa dikey eksen sıklık ölçeğidir.",
        difficultyReason="2 adım; ön bilgi: sütun grafiğinde eksenlerin görevi; çeldiriciler yakın (grafiğin diğer öğeleriyle karıştırma); beceri: temsil okuma",
        hints=[
            "Sütun grafiğinin iki ekseninin farklı bilgiler taşıdığını hatırla.",
            "Bir sütunun yüksekliğinin neyi anlattığını düşün.",
            "Kategorilerin hangi eksende yazıldığı soruda verilmiş; diğerine ne kalır?",
            "Grafiğin başlığına yazılan bilgiyi eksenden ayır.",
            "Tam çözüm: kategoriler yatay eksende olduğuna göre dikey eksen sütun yüksekliklerini okumaya yarayan sıklık ölçeğini taşır.",
        ],
    ),
    dict(
        level=3,
        question="Okulun tamamının en sevdiği oyunu öğrenmek isteyen bir öğrenci soruyu yalnız kendi takım arkadaşlarına sormuştur. Bu yöntemin temel hatası nedir?",
        choices=[
            "Soruda kategori sayısı fazladır.",
            "Yanıtlar çetele yerine tabloya yazılmıştır.",
            "Aynı soru katılımcılara iki kez sorulmamıştır.",
            "Katılımcılar okulun tamamını temsil etmemektedir.",
        ],
        correct=3,
        distractorWhy=[
            "Kaç seçenek sunulduğu soruda belirtilmemiştir; anlatılan kusur seçenek listesiyle ilgili değildir.",
            "Verinin tabloya yazılması geçerli bir kayıt biçimidir; sayım yöntemi hatalı değildir.",
            "Aynı soruyu tekrarlamak veriyi doğrulamaz; sorun sorunun kaç kez sorulduğunda değildir.",
            "doğru",
        ],
        explanation="Araştırma sorusu kimlerin inceleneceğini belirler. Okulun tamamı hakkında sonuç çıkarmak "
                    "için katılımcıların okuldaki bütün öğrencileri yansıtması gerekir; tek bir takımdan toplanan "
                    "veri bu kapsamı karşılamaz.",
        difficultyReason="3 adım; ön bilgi: araştırma sorusunun kapsamı ile katılımcı grubunun uyumu; çeldiriciler biçimsel ayrıntılara yöneliyor; beceri: akıl yürütme",
        hints=[
            "Öğrencinin hangi grup hakkında sonuç çıkarmak istediğini belirle.",
            "Soruyu gerçekte kimlere sorduğunu işaretle.",
            "Bu iki grubu birbiriyle karşılaştır: biri diğerini kapsıyor mu?",
            "Yalnız bir takımdan toplanan yanıtların okulun geneli için ne söyleyebileceğini düşün.",
            "Tam çözüm: sonuç okulun tamamı için isteniyor ama veri tek bir takımdan toplanmıştır. Katılımcı grubu araştırmanın kapsamını yansıtmadığı için yöntem hatalıdır.",
        ],
    ),
    dict(
        level=4,
        question="Bir sınıftaki 25 öğrenciye en sevdiği spor sorulmuş ve en yüksek sıklık basketbolda çıkmıştır. Aşağıdaki yorumlardan hangisi bu veriyle desteklenir?",
        choices=[
            "Ülkedeki bütün öğrenciler en çok basketbolu sever.",
            "Bu sınıfta basketbolu seçen öğrenci sayısı diğer sporları seçenlerden fazladır.",
            "Okuldaki her sınıfta aynı spor birinci sıradadır.",
            "Basketbol diğer sporlardan daha faydalı bir spordur.",
        ],
        correct=1,
        distractorWhy=[
            "Yirmi beş kişilik tek bir sınıftan toplanan veri ülke geneline genellenemez.",
            "doğru",
            "Veri yalnız bir sınıftan toplanmıştır; diğer sınıflar hakkında bilgi vermez.",
            "Tercih sıklığı bir sporun yararını ölçmez; toplanan veri fayda hakkında bilgi içermez.",
        ],
        explanation="Yorumlar yalnız toplanan verinin kapsamıyla sınırlı tutulmalıdır. Veri bu sınıftaki "
                    "tercihleri gösterdiği için sonuç da bu sınıf hakkında kurulmalıdır.",
        difficultyReason="4 adım; ön bilgi: veri yorumunun katılımcı grubuyla sınırlı olması; çeldiriciler yakın (üçü de aşırı genelleme ya da veri dışı yargı); beceri: akıl yürütme",
        hints=[
            "Verinin kimlerden toplandığını tek cümleyle söyle.",
            "Her yorumun kim hakkında bir iddia kurduğunu ayrı ayrı belirle.",
            "Katılımcı grubunun dışına çıkan yorumları ele.",
            "Tercih sayısının ölçemeyeceği bir yargı kalıp kalmadığını kontrol et.",
            "Tam çözüm: veri yalnız bu sınıftan toplanmıştır. Ülke geneline ya da diğer sınıflara uzanan yorumlar ile yararlılık yargısı veriyle desteklenmez; geçerli yorum bu sınıftaki sıklık karşılaştırmasıdır.",
        ],
    ),
    dict(
        level=4,
        question="Bir sayımda üç kategori için sırasıyla 3 tam çetele demeti; 1 tam demet ile 4 tek işaret; 2 tek işaret kaydedilmiştir. Toplam kaç gözlem vardır?",
        choices=[
            "20",
            "26",
            "10",
            "24",
        ],
        correct=1,
        distractorWhy=[
            "Yalnız tam demetleri saymış: 3 × 5 + 5 = 20; artan tek işaretleri eklememiş.",
            "doğru",
            "Her tam demeti bir gözlem saymış: 3 + 1 + 4 + 2 = 10.",
            "Üçüncü kategorideki 2 gözlemi toplama katmamış: 15 + 9 = 24.",
        ],
        explanation="Birinci kategori 3 × 5 = 15, ikinci kategori 5 + 4 = 9, üçüncü kategori 2 gözlem içerir. "
                    "Toplam 15 + 9 + 2 = 26'dır.",
        difficultyReason="4 adım; ön bilgi: demet değeri ve artan işaretlerin ayrı sayılması; çeldiriciler yakın (demet ile tek işaret karışması); beceri: hesaplama",
        hints=[
            "Bir tam demetin kaç gözleme karşılık geldiğini belirle.",
            "Her kategoriyi ayrı ayrı ele al ve demetlerin toplamını hesapla.",
            "Demetlerin dışında kalan tek işaretleri her kategoriye ekle.",
            "Üç kategoriden çıkan sonuçları alt alta yazıp topla.",
            "Tam çözüm: 3 × 5 = 15; 5 + 4 = 9; 2. Üçünün toplamı 15 + 9 + 2 = 26 gözlemdir.",
        ],
    ),
    dict(
        level=5,
        question="Bir sınıfta 30 öğrenciye en sevdiği renk sorulmuştur. Mavi diyenler kırmızı diyenlerin iki katıdır, yeşil diyenler 6 kişidir ve başka renk seçilmemiştir. Mavi diyen kaç öğrenci vardır?",
        choices=[
            "8",
            "24",
            "16",
            "12",
        ],
        correct=2,
        distractorWhy=[
            "Kırmızı diyenlerin sayısını bulup orada durmuş; soru mavi diyenleri istiyor.",
            "Mavi ile kırmızı diyenlerin toplamını yazmış: 30 − 6 = 24.",
            "doğru",
            "Kalan 24 kişiyi iki eşit gruba bölmüş; oysa mavi grubu kırmızının iki katıdır.",
        ],
        explanation="Yeşil dışındaki öğrenciler 30 − 6 = 24 kişidir. Kırmızı diyenlere 1 pay, mavi diyenlere "
                    "2 pay düşer; toplam 3 pay 24 kişiye karşılık gelir. Bir pay 24 ÷ 3 = 8 kişi olduğundan "
                    "mavi diyenler 2 × 8 = 16 kişidir.",
        difficultyReason="5 adım; ön bilgi: pay düşünmeyle iki katı olan grupları ayırma; çeldiriciler yakın (ara sonucu ya da toplamı yanıt sanma); beceri: hesaplama; akıl yürütme; model kurma",
        hints=[
            "Sıklığı bilinen kategoriyi toplamdan ayırmayı dene.",
            "Geriye kalan iki kategorinin toplam kaç kişi olduğunu bul.",
            "Kırmızı diyenlere 1 pay dersen mavi diyenlere kaç pay düşeceğini yaz.",
            "Toplam kaç pay olduğunu bulup bir payın değerini hesapla.",
            "Tam çözüm: 30 − 6 = 24 kişi kalır. Toplam 3 pay 24 kişiyi verdiğinden bir pay 8'dir; mavi diyenler 2 × 8 = 16 kişidir.",
        ],
    ),
    dict(
        level=5,
        question="Bir markette bir günlük meyve satışı şöyledir: elma 30, armut 15, muz 30, kiraz 15 kilogram. Elma ile muz satışı, toplam satışın kaçta kaçıdır?",
        choices=[
            "1/2",
            "2/3",
            "1/3",
            "5/6",
        ],
        correct=1,
        distractorWhy=[
            "Dört kategoriden ikisi seçildiği için oranı kategori sayısına göre yazmış; oran satış miktarlarından hesaplanır.",
            "doğru",
            "Birleştirilen iki kategoriden yalnız birini hesaba katmış: 30/90 = 1/3.",
            "Yalnız kiraz satışını toplamdan çıkarmış: 75/90 = 5/6.",
        ],
        explanation="Toplam satış 30 + 15 + 30 + 15 = 90 kilogramdır. Elma ile muz birlikte 30 + 30 = 60 "
                    "kilogram eder. Oran 60/90 olur ve sadeleştirildiğinde 2/3 bulunur.",
        difficultyReason="5 adım; ön bilgi: parça-bütün oranı ve kesir sadeleştirme; çeldiriciler yakın (eksik parça ya da kategori sayısına göre oran); beceri: hesaplama; akıl yürütme",
        hints=[
            "Oranın paydasına hangi sayının yazılacağını belirle.",
            "Dört kategorinin satışını toplayarak bütünü bul.",
            "Sorulan iki kategorinin satışını ayrıca topla.",
            "Parçayı bütünün üzerine yazıp kesri sadeleştir.",
            "Tam çözüm: toplam 90, istenen parça 30 + 30 = 60'tır. 60/90 kesri sadeleştirildiğinde 2/3 elde edilir.",
        ],
    ),
]


# Doğru cevap konumu tek bir şıkta yığılmasın diye dönüşümlü hedef dizi.
# Döndürme choices ve distractorWhy'a AYNI anda uygulanır; ikisini ayrı
# işlemek d133631'deki hatanın ta kendisidir (AUTHORING_RULES.md §1).
HEDEF_KONUM = [i % 4 for i in range(len(SORULAR))]


def _dondur(secenekler, gerekceler, kaynak, hedef):
    """Şıkları döngüsel kaydırarak doğru cevabı hedef konuma taşır."""
    kaydir = (kaynak - hedef) % len(secenekler)
    yeni_s = secenekler[kaydir:] + secenekler[:kaydir]
    yeni_g = gerekceler[kaydir:] + gerekceler[:kaydir]
    assert yeni_s[hedef] == secenekler[kaynak]
    assert yeni_g[hedef] == gerekceler[kaynak] == "doğru"
    return yeni_s, yeni_g


def uret():
    kayitlar = []
    for i, s in enumerate(SORULAR, start=1):
        s = dict(s)
        hedef = HEDEF_KONUM[i - 1]
        s["choices"], s["distractorWhy"] = _dondur(
            s["choices"], s["distractorWhy"], s["correct"], hedef)
        s["correct"] = hedef
        q = {
            "type": "question",
            "id": f"tr.g05.mat.5-5-1.q{i:03d}",
            "subject": "Matematik",
            "topic": "Kategorik veri analizi",
            "noteId": "tr.g05.mat.5.5.note.01",
            "objective": "MAT.5.5.1",
            "objectiveSource": KAYNAK,
            "level": s["level"],
            "question": s["question"],
            "choices": s["choices"],
            "correct": s["correct"],
            "distractorWhy": s["distractorWhy"],
            "explanation": s["explanation"],
            "difficultyReason": s["difficultyReason"],
            "figure": None,
            "hints": s["hints"],
            "provenance": "machine-generated:claude-opus-5:2026-08:a3-celdirici-yeniden-uretim:human-pending",
            "reviewStatus": "pending",
            "correctIndex": s["correct"],
        }
        kayitlar.append(q)
    return kayitlar
