# LGS 2024–2026 Soru Analizi ve 2027 Tahmin Çerçevesi

> **Hazırlanma:** 12 Ekim 2026 · **Kapsam:** 2024, 2025 ve 2026 LGS merkezî sınavının 270 sorusu
> (her yıl 90 soru) · **Kazanım kaynağı:** MEB 2018–2019 8. sınıf öğretim programları
> (`curriculum/tr-grade8-current-2018-2019.json`)
>
> **Makine okunur çıktılar**
> - `authoring/lgs-2027/lgs-2024-2026-soru-envanteri.json`: 270 sorunun envanteri. Her kayıtta soru no, ünite/blok, kazanım kodu, kısa özet, biçim, cevap, güven düzeyi ve kaynak var.
> - `authoring/lgs-2027/lgs-2027-tahmin-plani.json`: Envanterden türetilen 2027 tahmin planı. Ünite, kazanım ve görev kotalarını, soru tipi ve zorluk karmasını içerir.
> - `tools/build_lgs_2027_plan.py`: Planı yeniden üretir. `--check` planın güncel olup olmadığını denetler, `--tables` ve `--appendix` bu rapordaki tabloları basar.

## 0. Yöntem ve güven düzeyi

- **Birincil kaynak resmî kitapçıklardır.** MEB'in yayımladığı 2024, 2025 ve 2026 sözel ve sayısal kitapçıkları (EBA/ÖDSGM PDF'leri) soru soru incelendi.
- **PDF'ler doğrudan indirilemedi.** Çalışma ortamının ağ politikası `meb.gov.tr` ve `eba.gov.tr` alan adlarını engelliyor. Bu yüzden kitapçıklar, arama motorunun bu PDF'lerden çıkardığı dizin metni üzerinden okundu.
  - Her sorgu 4–5 ardışık soruyu kapsadı.
  - Soru numaraları cevap anahtarı, hesapla öz-doğrulama ve ikinci okuma ile kontrol edildi.
  - Kitapçıkların bağlantıları envanterin `exams.*.booklets` alanında.
- **Soru metinleri kopyalanmadı.** Envanterdeki `summary` alanı yalnızca kısa bir açıklamadır. Bankada LGS soruları birebir kullanılmamalıdır; aynı beceriyi ölçen özgün sorular yazılmalıdır.
- **2026 sayısal B kitapçığına göre numaralandı.** A kitapçığının metni dizinde bulunamadı. Kitapçıklar arasında soru sırası farklıdır. Konu dağılımı ve soru tipi analizi bundan etkilenmez.
- **Cevap anahtarlarının kaynağı:**
  - Sayısal anahtarlar kitapçıkların anahtar sayfası metninden okundu.
  - Sözel anahtarlar üçüncü taraf bir kaynaktan (dilbilgisi.net) alındı. Kitapçık okumalarıyla tutarlılar; tek çelişki 2025 Türkçe 16. sorudur (B/C).
  - Hepsi resmî PDF ile bir kez daha doğrulanmalıdır.

**Güven ölçeği**
- **high:** kitapçık metni artı ikinci okuma, anahtar/hesap tutarlılığı ya da resmî MEB belgesi.
- **medium:** kitapçık metninde konu açık, numara tek okumayla belirlendi.
- **low:** parça metin ya da analist çıkarımı.
- **unknown:** içerik bulunamadı.

| Ders | 2024 (high/medium/low/unknown) | 2025 | 2026 |
|---|---|---|---|
| Türkçe | 6/8/6/0 | 0/11/9/0 | 2/10/6/2 |
| Matematik | 7/10/3/0 | 4/10/6/0 | 2/10/6/2 |
| Fen Bilimleri | 2/14/4/0 | 1/17/2/0 | 0/16/4/0 |
| T.C. İnkılap Tarihi ve Atatürkçülük | 0/5/2/3 | 0/5/4/1 | 1/5/4/0 |
| Din Kültürü ve Ahlak Bilgisi | 1/4/4/1 | 0/2/7/1 | 0/8/1/1 |
| İngilizce | 0/8/2/0 | 2/7/1/0 | 2/8/0/0 |

Toplam 270 soru: high 30, medium 158, low 71, unknown 11. İçeriği tanımlanan soru: 259.

## 1. Yönetici özeti

1. **Biçim üç yıldır sabit.**
   - Sınavda 90 soru var, her soruda 4 seçenek.
   - Sözel oturum: Türkçe 20, İnkılap 10, Din 10, İngilizce 10 soru; 75 dakika, soru başına yaklaşık 90 saniye.
   - Sayısal oturum: Matematik 20, Fen 20 soru; 80 dakika, soru başına yaklaşık 120 saniye.
   - Türkçe, Matematik ve Fen ×4; diğer üç ders ×1 ağırlıklı.
   - Net = doğru − yanlış/3.
2. **Kapsam yalnızca 8. sınıf programı, ama programın tamamı.**
   - 2020 ve 2023'te yalnız 1. dönem konuları sorulmuştu. 2024–2026'da kılavuzlar "8. sınıf öğretim programlarındaki kazanımlar" diyor ve ay sınırı koymuyor.
   - Kanıt olarak, ikinci dönemin son üniteleri her yıl soruldu: Matematikte Geometrik Cisimler, Fende Elektrik, İngilizcede Science ünitesi.
   - Buna karşın üç yılda hiç gözlenmeyenler var: İnkılap'ta 7. ünite (Atatürk'ün Ölümü ve Sonrası), İngilizcede 10. ünite (Natural Forces).
3. **2027 aynı programla yapılacak.**
   - 2026-2027'de 8. sınıf TYMM öncesi programla okutuluyor. 2027 adayları 5–8. sınıfların tamamını eski programla okudu.
   - MEB'e göre yeni müfredata uyumlu soru modeli 2028'de başlayacak. Bakan Tekin de "sınav sistemi değil, sorular değişecek" dedi.
   - Bu nedenle 2027 LGS'nin 2024–2026 ile aynı kapsam ve tarzda olması beklenir.
4. **En zor test her yıl Matematik.**
   - Resmî ortalama madde güçlüğü (p) 0,33 → 0,28 → 0,28.
   - Türkçe 2025'te belirgin biçimde zorlaştı (0,42), 2026'da toparlandı (0,47).
   - Din (0,57 → 0,63) ve İnkılap (0,47 → 0,53) her yıl biraz kolaylaştı.
   - İngilizce p = 0,44 ile ikinci en zor test ve en ayırt edici test (D = 0,69).
5. **Ölçme kalitesi yüksek ama kusursuz değil.**
   - Bütün testlerde ayırt edicilik 0,40'ın üzerinde, güvenirlik 0,72–0,88.
   - 2024 Fen 13. soru, program dışı kavram (tork, eylemsizlik momenti) gerektirdiği için mahkeme kararıyla iptal edildi.
   - 2025 Matematik 15. sorusu belirsizlik gerekçesiyle tartışıldı; MEB itirazı reddetti.
6. **Fen'in ünite dağılımı neredeyse sabit.** Madde ve Endüstri 5, Enerji Dönüşümleri 4, DNA 3–4, Elektrik 2–3, Basınç 2, Basit Makineler 2, Mevsimler 1. 2024 ve 2025'te test ünite blokları hâlinde dizildi.
7. **Matematik her yıl aynı omurgayı izliyor.**
   - Doğrusal Denklemler ve eğim 3–4, Kareköklü İfadeler 2–3, Üslü 2, Cebirsel 2, Üçgenler 2; kalan yedi ünite 1'er soru.
   - Soruların %75–90'ı şekil, tablo ya da grafik içeriyor; yaklaşık yarısı gerçek yaşam bağlamıyla açılıyor.
   - Her yıl 3–5 çok kazanımlı seçici soru var.
8. **Türkçede ağırlık paragraf ve sözel mantıkta.**
   - Paragraf/okuduğunu anlama 5–8, sözel mantık/görsel/grafik 3–4, cümlede anlam 2–3 soru.
   - Dil bilgisi 2–3 soru, testin sonunda.
   - Yazım ve noktalama her yıl birer soru.
   - 2025–2026'da edebî/yazar odaklı metinler arttı.
   - Dönüşümlü dil bilgisi konularından fiilimsi 2025–2026'da gözlenmedi; 2027 için güçlü aday.
9. **İnkılap ve Din kaynak/metin yorumuna dayanıyor.**
   - İnkılap'ta her madde bir kaynakla (hatıra, roman kesiti, parti programı, tablo, Atatürk sözü) açılıyor ve "ulaşılabilir yargı / ilke / temel esas" soruluyor.
   - Din'de ayet/sure yorumu, siyer örnek olayı, kavram ayrımı ve öncüllü yargılar öne çıkıyor.
10. **İngilizce okuma temelli ve kökler İngilizce.**
    - En sık biçim: 3–4 kişinin kısa metni → "Who…? / Which two…?".
    - Olumsuz kök (NOT/cannot) sık; ayrı dilbilgisi sorusu yok.
11. **Güncel 8. sınıf matematik verisi LGS tarzından farklı.**
    - Güncel veride soru kökleri ortalama 18 sözcük, %52,5'i görselli ve görevler eşit ağırlıklı (her biri 50 soru).
    - LGS bağlamlı, çok adımlı ve görsel ağırlıklı; görevlere dağılımı da eşit değil.
    - 2027 bankası bu veri üzerine ayrı bir "LGS katmanı" olarak kurulmalı (§5, §6).

## 2. Sınavın yapısı, kapsamı ve 2027 görünümü

### 2.1 Yapı

| | Sözel oturum | Sayısal oturum |
|---|---|---|
| Testler | Türkçe 20, T.C. İnkılap Tarihi ve Atatürkçülük 10, Din Kültürü ve Ahlak Bilgisi 10, Yabancı Dil 10 | Matematik 20, Fen Bilimleri 20 |
| Soru / süre | 50 soru / 75 dk (≈90 sn/soru) | 40 soru / 80 dk (≈120 sn/soru) |
| Ağırlık | Türkçe ×4; diğerleri ×1 | Matematik ×4, Fen ×4 |

- **Puanlama:** Net = doğru − yanlış/3.
- **Ölçek:** Alt test puanları standart puana çevrilip ağırlıklandırılır ve 100–500 ölçeğine taşınır.
- **Kitapçık türleri:** 2026'da A, B, C ve D kitapçıkları vardı; soru sırası kitapçıklar arasında farklıdır.

| Yıl | Tarih | Başvuru | Katılım | Tam puan (500) | Sonuç |
|---|---|---|---|---|---|
| 2024 | 2 Haziran 2024 (Pazar) | 1.038.544 | 992.906 (%95,61) | 352 | 28 Haziran 2024 |
| 2025 | 15 Haziran 2025 (Pazar) | 1.010.916 | 963.142 (%95,27) | 719 | 11 Temmuz 2025 |
| 2026 | 13 Haziran 2026 (Cumartesi)¹ | 1.022.658 | 994.358 (%97,23) | 452 | 10 Temmuz 2026 |

¹ Kılavuzda tarih 14 Haziran Pazardı. Aynı gün oynanacak Dünya Kupası maçı nedeniyle sınav bir gün öne alındı.

### 2.2 Kapsam: hangi sınıflar?

| Sınav | Resmî kapsam |
|---|---|
| 2020 | Yalnız 1. dönem müfredatı (salgın) |
| 2021 | Talim ve Terbiye Kurulunun daraltılmış konu-kazanım listesi |
| 2023 | Yalnız 1. dönem konuları (deprem) |
| 2024 | Ders kitaplarındaki konu, kazanım, etkinlik ve sorular; ay sınırı yok |
| 2025 | "8'inci sınıf öğretim programlarındaki kazanımlar esas alınacak"; ay sınırı yok |
| 2026 | "Her alan için 8'inci sınıf öğretim programlarında belirlenen kazanımlar"; ay sınırı yok |

- **Resmî kapsam yalnızca 8. sınıftır.** Soru bazında bakıldığında da 2024–2026'da sorulan her madde 8. sınıf kazanımına bağlanıyor.
  - MEB'in 2025 analizine göre soruların tamamı ücretsiz dağıtılan 8. sınıf ders kitaplarıyla örtüşüyor.
  - 2024'te iptal edilen Fen sorusu, program dışı kavram gerektirdiği için iptal edildi. Bu, sınırın yargı yoluyla da korunduğunu gösteriyor.
- **Sorular 5–7. sınıf bilgisini örtük olarak kullanıyor.** Bu bilgi önkoşul olarak varsayılıyor.

| Ders | Sık kullanılan önceki sınıf bilgisi (analist çıkarımı) |
|---|---|
| Matematik | Alan ve çevre (5–6); prizma hacmi (6); daire alanı ve π (7); oran-orantı ve yüzde (7); denklem kurma (7); tam sayılar (7); veri ve grafik okuma (5–7); çokgen ve açı bilgisi (5–7) |
| Fen Bilimleri | Dünya'nın hareketleri (5); dengelenmiş kuvvet ve sürat (6); yoğunluk (6); iletken-yalıtkan (6); kütle-ağırlık (7); hücre ve bölünme (7); atom, element, saf madde (7); canlılar ve çevre (5–7) |
| Türkçe | Sarmal okuma becerileri (5–7); sözcük türleri (6); fiil ve ek fiil (7); deyim-atasözü ve söz sanatları; yazım ve noktalama (1–8, birikimli) |
| İnkılap | 7. sınıf Sosyal Bilgiler'deki Osmanlı–Avrupa ilişkileri (dolaylı) |
| Din | Önceki sınıflardaki siyer bilgisi ve temel kavramlar (dolaylı) |
| İngilizce | 5–7. sınıf kelime ve yapıları: present continuous, past simple, karşılaştırma, tercih ifadeleri |

### 2.3 2027 için resmî görünüm (12.10.2026)

- **Program:** 2026-2027'de 8. sınıf 2018-2019 programıyla okutuluyor; TYMM 5–7. sınıflarda.
  - 2027 adayları 5. sınıfı 2023-24'te, 6. sınıfı 2024-25'te, 7. sınıfı 2025-26'da okudu. Hepsi eski programdaydı.
  - Kaynak: `curriculum/tr-2026-2027-activation.json`.
- **Yeni soru modeli:** MEB'e göre yeni müfredata uyumlu soru modeli LGS'de ve YKS'de 2028'de başlayacak. Bakan Tekin: "sınav sistemi değil, sorular değişecek."
- **Kontenjan:** Bakan Tekin, sınavla öğrenci alan okulların sayısı ve kontenjanının kademeli olarak azaltılacağını söyledi. Takvim ve oran açıklanmadı.
- **Henüz açıklanmayanlar:**
  - 2027 sınav tarihi ve 2027 kılavuzu. Kılavuz geçen yıl Mart ayında yayımlanmıştı.
  - 2026-2027 örnek soru seti. Önceki iki yılda ilk set 18 Kasım ve 30 Kasım/1 Aralık'ta çıktı.
- **İzlenecekler:**
  - MEB örnek soruları (Kasım 2026'dan itibaren).
  - MEBİ denemeleri. 2025 Türkçe soruları örnek sorulara, 2026 Türkçe soruları MEBİ denemelerine benzetildi.
  - Mart 2027 kılavuzundaki kapsam cümlesi.

## 3. Zorluk ve ölçme kalitesi

Resmî madde istatistikleri:
- p = ortalama madde güçlüğü (doğru cevap oranı); yükseldikçe test kolaylaşır.
- D = ayırt edicilik.
- r = güvenirlik.

| Test | 2024 p | 2025 p | 2026 p | 2026 D | 2026 r |
|---|---|---|---|---|---|
| Türkçe | 0,48 | 0,42 | 0,47 | 0,48 | 0,82 |
| Matematik | 0,33 | 0,28 | 0,28 | 0,52 | 0,86 |
| Fen Bilimleri | 0,43 | 0,44 | 0,45 | 0,54 | 0,87 |
| T.C. İnkılap Tarihi ve Atatürkçülük | 0,47 | 0,49 | 0,53 | 0,60 | 0,81 |
| Din Kültürü ve Ahlak Bilgisi | 0,57 | 0,59 | 0,63 | 0,53 | 0,72 |
| İngilizce | 0,52 | 0,44* | 0,44 | 0,69 | 0,88 |

**Tabloyla ilgili notlar:**
- 2024 değerleri "yapılma ortalaması / soru sayısı" olarak türetildi (ör. Türkçe 9,63/20).
- 2025 ve 2026 değerleri ÖDSGM raporlarından alındı. *2025 İngilizce değeri türetilmiştir.
- 2024'te Matematik ve Fen için D = 0,53 ve r = 0,87 bildirildi. 2025'te Matematik D = 0,56, r = 0,88; Fen D = 0,53, r = 0,87.

**Yorum**
- **Matematik:** Seçiciliğin asıl kaynağı. Uzmanlara göre 2024'te 6 kolay, 9 orta ve 5 zor soru vardı. Zor sorular birden çok kazanımı birleştiriyordu (eğim + Pisagor + denklem; hacim + denklem + karekök; EBOB-EKOK + eşitsizlik).
- **Türkçe:** 2025 testi eğitimcilerce "LGS tarihinin en zor Türkçe testi" olarak değerlendirildi. Nedenleri edebî ve mecaz yoğun metinler ile çok yakın çeldiricilerdi.
- **İngilizce:** Uzmanlar 2026 testini "kolay" buldu, ama resmî veriye göre ikinci en zor ve en ayırt edici test. Banka resmî veriye göre ayarlanmalı.
- **Tam puan sayısı:** 352 → 719 → 452. Rekor 2025'te, bütün testler zor değerlendirilmesine rağmen geldi. Tam puan, üst dilimde ayrıştırmanın zayıf kalabildiğini gösteriyor; seçici soruların payı kritik.

**Kalite sorunlarından çıkan dersler**

| Olay | Ders |
|---|---|
| 2024 Fen 13 (makara-tahta düzeneği) mahkeme kararıyla iptal edildi | Bilirkişiye göre çözüm tork, ivme ve eylemsizlik momenti gerektiriyordu. Basit makine sorularında moment/tork hesabı kurulmamalı; "ip ve makara ağırlıkları önemsiz, sürtünme yok" varsayımları yazılmalı. |
| 2024 Türkçe 1 ("bırakmak" çok anlamlılık), Matematik 20 ve Fen 15 için dava açıldı | Çok anlamlılık sorularında tek bir anlam açıkça doğru olmalı. Hiçbiri için iptal kararı bulunamadı. |
| 2025 Matematik 15 (logo üzerinde A–B uzaklığı, Pisagor) | "En kısa" ve yol koşulu belirtilmediği için birden çok seçeneğin savunulabileceği öne sürüldü. Uzaklık sorularında yol/ölçü koşulu açık yazılmalı. |

## 4. Ders bazında analiz

Tablolar envanterden üretilmiştir.
- **2027 beklenen:** 2024–2026 payları ağırlıklandırılarak (2024: 0,25, 2025: 0,35, 2026: 0,40) bulunan beklenen soru sayısı; parantez içi ondalık değerdir.
- **Banka kotası:** 2.000 soruluk tahmin bankasındaki pay.

### 4.1 Türkçe

| Ünite / blok | 2024 | 2025 | 2026 | Ağırlıklı pay | 2027 beklenen | Banka kotası |
|---|---|---|---|---|---|---|
| Sözcük ve söz öbeğinde anlam (deyim, atasözü) | 3 | 2 | 0 | %7,2 | **1** (1,4) | 32 |
| Cümlede anlam (cümle birleştirme dahil) | 3 | 2 | 3 | %13,9 | **3** (2,8) | 61 |
| Paragraf ve okuduğunu anlama | 5 | 8 | 8 | %38,0 | **8** (7,6) | 167 |
| Sözel mantık, görsel, tablo ve grafik okuma | 4 | 3 | 3 | %16,9 | **3** (3,4) | 75 |
| Dil bilgisi (fiilimsi, öge, çatı, cümle türü, anlatım bozukluğu) | 3 | 3 | 2 | %13,4 | **3** (2,7) | 59 |
| Yazım kuralları | 1 | 1 | 1 | %5,2 | **1** (1,0) | 23 |
| Noktalama işaretleri | 1 | 0 | 1 | %3,5 | **1** (0,7) | 15 |
| Söz sanatları | 0 | 1 | 0 | %1,8 | **0** (0,3) | 13 |
| *ünitesi belirsiz* | 0 | 0 | 2 | – | – | – |

**Soru türleri**
- **Testin sırası:**
  - Başta (1–6): kısa sözcük, söz öbeği ve cümle anlamı soruları. Kökler: "anlamca en yakın", "kesin olarak çıkarılabilecek yargı", "koşul anlamı", "boşluklara sırasıyla getirilecek ifadeler".
  - Ortada: paragraf, görsel ve grafik soruları.
  - Sonda: dil bilgisi, yazım ve noktalama. 2026 örneği: 17 yazım, 18 noktalama, 19 yer tamlayıcısı, 20 nesnesine göre çatı.
- **Her yıl 1 grafik ve 1–2 görsel/sözel mantık maddesi var:**
  - 2024: iki tablodan sütun grafiğine geçiş (rüzgâr türbinleri), yan flütte parmak-tuş görseli.
  - 2025: beyaz eşya satış grafiği, silindirli kilit görseli.
  - 2026: kıtalara göre orman alanı grafiği, yelkenli teknenin yelken sistemi, ölçüte uyan laboratuvar kuralları afişi.
- **Kural/açıklama verip uygulatan maddeler:**
  - 2024: üç koşullu ödev seçimi, tutarlılık açıklaması.
  - 2025: arka kapak yazısı ölçütü.
  - 2026: kuralların nitelikleri ve afiş.
- **Olumsuz kökler sık:** ulaşılamaz, örnek olamaz, yoktur, kullanılmamıştır, yanlıştır, söylenemez. 2024'te en az 6 madde.
- **Ortak metne bağlı ikili soru:** 2025'te dokunmatik ekran metnine bağlı bir yazım sorusu ve bir üç nokta (noktalama) sorusu.
- **Dönüşümlü dil bilgisi:**

| Konu | 2024 | 2025 | 2026 |
|---|---|---|---|
| Fiilimsi | ✓ | – | – |
| Cümle türleri | ✓ | ✓ (yeri belirsiz) | – |
| Fiilde çatı | – | ✓ (yeri belirsiz) | ✓ |
| Cümlenin ögeleri | – | anlatım bozukluğuna gömülü | ✓ |
| Anlatım bozukluğu | ✓ | ✓ | – |
| Söz sanatları | – | ✓ | – |

**Metin seçimi**
- 2024'te gündelik yaşam ve kültür metinleri ağırlıktaydı: sosyal medya, mahalle kedileri, çocuk oyunları.
- 2025–2026'da edebî/yazar odaklı metinler arttı: Cahit Zarifoğlu, Behçet Necatigil, Cemil Meriç, Reşat Nuri Güntekin.

**Kalite ve zorluk**
- p değerleri 0,48 → 0,42 → 0,47.
- 2025'teki düşüş mecaz yoğun metinlere ve yakın çeldiricilere bağlandı.
- 2026'da "anlam" soruları en zor bulundu.

**2027 beklentisi**
- Paragraf 7–8, sözel mantık/görsel 3–4, cümlede anlam 2–3, sözcük anlamı 1–2, dil bilgisi 2–3, yazım 1, noktalama 1 soru.
- Dil bilgisinde fiilimsi güçlü aday; cümle türleri ve anlatım bozukluğu da aday. Plandaki tahmin bonusu bu üç kazanıma verildi.

**Türkçe için 2.000'lik bankadaki pay:** 445 soru, hedef ortalama p ≈ 0,45

| Soru tipi | Pay | Kota |
|---|---|---|
| Uzun paragraf (edebî/bilgilendirici) | %35 | 156 |
| Numaralanmış cümle/parça | %20 | 89 |
| Görsel, grafik, tablo, şema | %15 | 67 |
| Kısa cümle/sözcük anlamı | %15 | 67 |
| Kural/açıklama verip uygulama | %10 | 44 |
| Ortak metinli ikili soru | %5 | 22 |

Zorluk karması (1 = en kolay, 5 = en zor): 1. seviye %5 (22) · 2. seviye %20 (89) · 3. seviye %40 (178) · 4. seviye %25 (111) · 5. seviye %10 (45)

**Kaçınılacaklar:** Birden çok anlamı savunulabilen çok anlamlılık maddeleri (2024 1. soru için dava açıldı). Dinleme/izleme ve konuşma kazanımlarını doğrudan ölçmeye çalışmak (kâğıt-kalem biçiminde ölçülmüyor). Ses bilgisi gibi 8. sınıf programında yer almayan konular.

### 4.2 Matematik

| Ünite / blok | 2024 | 2025 | 2026 | Ağırlıklı pay | 2027 beklenen | Banka kotası |
|---|---|---|---|---|---|---|
| Çarpanlar ve Katlar | 1 | 1 | 0 | %3,0 | **1** (0,6) | 13 |
| Üslü İfadeler | 2 | 2 | 2 | %10,7 | **2** (2,1) | 48 |
| Kareköklü İfadeler | 3 | 3 | 2 | %13,7 | **3** (2,7) | 61 |
| Veri Analizi | 1 | 1 | 1 | %5,3 | **1** (1,1) | 24 |
| Basit Olayların Olma Olasılığı | 1 | 1 | 1 | %5,3 | **1** (1,1) | 24 |
| Cebirsel İfadeler ve Özdeşlikler | 2 | 2 | 2 | %10,7 | **2** (2,1) | 48 |
| Doğrusal Denklemler (eğim dahil) | 4 | 3 | 3 | %17,3 | **4** (3,5) | 77 |
| Eşitsizlikler | 1 | 2 | 1 | %7,1 | **1** (1,4) | 31 |
| Üçgenler (Pisagor dahil) | 2 | 2 | 2 | %10,7 | **2** (2,1) | 47 |
| Dönüşüm Geometrisi | 1 | 1 | 1 | %5,3 | **1** (1,1) | 24 |
| Eşlik ve Benzerlik | 1 | 1 | 1 | %5,3 | **1** (1,1) | 24 |
| Geometrik Cisimler | 1 | 1 | 1 | %5,3 | **1** (1,1) | 24 |
| *ünitesi belirsiz* | 0 | 0 | 3 | – | – | – |

*2026 sayısal B kitapçığına göre. Ünitesi belirlenemeyen 3 soru için üçüncü taraf dağılımlar Kareköklü 3 ve Cebirsel 3 gösteriyor.*

**Soru türleri (kitapçık okumasından)**

| Biçim | 2024 | 2025 | 2026 (B) |
|---|---|---|---|
| Şekil, tablo ya da grafik içeren | 17/20 | 18/20 | 15/20 |
| Gerçek yaşam bağlamıyla açılan | 9 | 9 | 9 |
| Tablo, grafik, koordinat | 4 | 4 | 3 |
| Çok kazanımlı / çok adımlı | 5 | 4 | 3 |
| Olumsuz kök ("olamaz") | 1 | 1 | 1 |

- **Testin başında 2–3 kısa doğrudan soru var.** Örnekler: irrasyonel sayı seçimi, √363 − √75 − √27 işlemi, eşitsizliği sağlayan en büyük tam sayı, tam kare seçimi.
- **Her yıl tekrar eden kurgular:**
  - Özdeşlik alan modelleri: ötelenen kartonlar (2024), (2y + 3x)² gelir tablosu (2025), dört sarı dikdörtgen ve küp blok (2026).
  - Bağlam içinde eğim: çekmeceler (2024), köşegen eğimi ve yol-zaman grafiği (2025), tahterevalli (2026).
  - Kareli zeminde dönüşüm ve benzerlik.
  - Her yıl bir silindir sorusu: hacim → yanal alan → birleşik cismin yüzey alanı.
  - "En az / en fazla" kısıtlı sayma: bilyeler, gömlek satışı, yumurta kolisi.
  - Kareköklü uzunluklu bağlamlar: televizyon ses kuralı, oyuncak tren yolları.
- **Formül verilmez.** Alan, çevre, hacim ve Pisagor önceki sınıf bilgisiyle kullanılır. π = 3 alınır ve sayılar temiz çıkar.

**Kalite ve zorluk**
- p = 0,33 → 0,28 → 0,28 ile en zor test.
- Seçicilik çok kazanımlı maddelerden geliyor.
- 2025 15. soru, ölçü koşulunun belirsizliği nedeniyle tartışıldı.

**2027 beklentisi**
- Doğrusal Denklemler ve eğim 3–4, Kareköklü 3, Üslü 2, Cebirsel 2, Üçgenler 2, Eşitsizlik 1–2; diğer üniteler 1'er soru.
- Bir silindir, bir dönüşüm ve bir veri sorusu neredeyse kesin.

**Matematik için 2.000'lik bankadaki pay:** 445 soru, hedef ortalama p ≈ 0,32

| Soru tipi | Pay | Kota |
|---|---|---|
| Şekil/model tabanlı | %38 | 169 |
| Gerçek yaşam problemi | %22 | 98 |
| Tablo, grafik, koordinat | %13 | 58 |
| Kısa doğrudan işlem/kavram | %12 | 53 |
| Çok kazanımlı seçici | %10 | 45 |
| Kural/tanım verip uygulama | %5 | 22 |

Zorluk karması (1 = en kolay, 5 = en zor): 1. seviye %5 (22) · 2. seviye %15 (67) · 3. seviye %35 (156) · 4. seviye %30 (133) · 5. seviye %15 (67)

**Kaçınılacaklar:** Yolu ya da "en kısa" koşulu belirtilmemiş uzaklık soruları (2025 15. soru itirazı). Program dışı içerik (ikinci dereceden denklem, trigonometri, ispat). Hesap makinesi gerektiren büyük sayılar; 80 dakikada 40 soru için soru başına ~2 dakika vardır.

### 4.3 Fen Bilimleri

| Ünite / blok | 2024 | 2025 | 2026 | Ağırlıklı pay | 2027 beklenen | Banka kotası |
|---|---|---|---|---|---|---|
| Mevsimler ve İklim | 1 | 1 | 1 | %5,0 | **1** (1,0) | 22 |
| DNA ve Genetik Kod | 4 | 3 | 3 | %16,2 | **3** (3,2) | 72 |
| Basınç | 2 | 2 | 2 | %10,0 | **2** (2,0) | 45 |
| Madde ve Endüstri | 5 | 5 | 5 | %25,0 | **5** (5,0) | 111 |
| Basit Makineler | 2 | 2 | 2 | %10,0 | **2** (2,0) | 44 |
| Enerji Dönüşümleri ve Çevre Bilimi | 4 | 4 | 4 | %20,0 | **4** (4,0) | 89 |
| Elektrik Yükleri ve Elektrik Enerjisi | 2 | 3 | 3 | %13,8 | **3** (2,8) | 61 |

**Soru türleri**
- **Görsel:** Her yıl 17–19 soruda görsel var.
- **Deney/etkinlik düzeneği:** Her yıl 10–11 soru. Değişken kontrolü, hipotez testi ve gözlem-çıkarım istiyor.
- **Öncüllü (I-II-III):** Her yıl 3–4 soru.
- **Kökler:** "kesinlikle doğrudur", "hangileri belirlenebilir", "hangi değişkenin etkisi test edilmektedir".
- **Sıralama:** 2024 ve 2025 A kitapçıklarında test ünite blokları hâlinde dizildi; Madde ve Endüstri 16–20. sorulardı. 2026 B kitapçığında sıra karışık.
- **Tekrar eden kurgular:**
  - Eş yükseltideki şehirlerin sıcaklık verilerinden mevsim ve yarım küre çıkarımı (2024, 2025, 2026).
  - Bezelye tek karakter çaprazlaması: boy → tohum rengi → çiçek rengi.
  - Madde döngüsü şeması: azot, azot, karbon.
  - Işık rengi–fotosentez deneyi.
  - Yüklü çubuklarla elektriklenme ve topraklama.
  - Katı ve sıvı basıncı deneyi.
  - Ayraç ve pH renk tablosu.
  - Isı ve hâl değişimi deneyi.
  - Periyodik tablo kesiti.
  - Makara, eğik düzlem, çıkrık ve kaldıraç düzenekleri.

**Kalite ve zorluk**
- p = 0,43 → 0,44 → 0,45; D = 0,53–0,54; r = 0,87.
- 2024'te 13. soru iptal edildi (bkz. §3).

**2027 beklentisi**
- Madde ve Endüstri 5, Enerji Dönüşümleri ve Çevre Bilimi 4, DNA ve Genetik Kod 3–4, Elektrik 2–3, Basınç 2, Basit Makineler 2, Mevsimler 1.

**Fen Bilimleri için 2.000'lik bankadaki pay:** 444 soru, hedef ortalama p ≈ 0,45

| Soru tipi | Pay | Kota |
|---|---|---|
| Deney düzeneği ve değişken | %35 | 155 |
| Model, şema, döngü | %18 | 80 |
| Günlük yaşam/teknoloji (öncüllü) | %17 | 76 |
| Tablo/grafik yorumlama | %15 | 67 |
| Düzenek/mekanizma | %10 | 44 |
| Çaprazlama problemi | %5 | 22 |

Zorluk karması (1 = en kolay, 5 = en zor): 1. seviye %5 (22) · 2. seviye %20 (89) · 3. seviye %40 (178) · 4. seviye %25 (111) · 5. seviye %10 (44)

**Kaçınılacaklar:** Basit makine sorularında tork, moment, ivme veya eylemsizlik momenti gerektiren kurgular (2024 13. soru mahkemece iptal edildi). Program dışı nicel hesaplar (formüllü basınç hesabı yerine nitel karşılaştırma). Değişkenleri belirsiz bırakılmış deney düzenekleri.

### 4.4 T.C. İnkılap Tarihi ve Atatürkçülük

| Ünite / blok | 2024 | 2025 | 2026 | Ağırlıklı pay | 2027 beklenen | Banka kotası |
|---|---|---|---|---|---|---|
| Bir Kahraman Doğuyor | 0 | 1 | 1 | %7,9 | **1** (0,8) | 17 |
| Millî Uyanış: Bağımsızlık Yolunda Atılan Adımlar | 2 | 3 | 3 | %30,8 | **3** (3,1) | 66 |
| Millî Bir Destan: Ya İstiklal Ya Ölüm! | 3 | 1 | 2 | %22,6 | **2** (2,3) | 49 |
| Atatürkçülük ve Çağdaşlaşan Türkiye | 2 | 2 | 2 | %22,9 | **2** (2,3) | 49 |
| Demokratikleşme Çabaları | 0 | 1 | 1 | %7,9 | **1** (0,8) | 17 |
| Atatürk Dönemi Türk Dış Politikası | 0 | 1 | 1 | %7,9 | **1** (0,8) | 17 |
| Atatürk'ün Ölümü ve Sonrası | 0 | 0 | 0 | %0,0 | **0** (0,0) | 7 |
| *ünitesi belirsiz* | 3 | 1 | 0 | – | – | – |

**Soru türleri**
- **Her madde bir kaynakla açılıyor:**
  - Bilgi metni ve Atatürk sözü.
  - Hatıra: Kâzım Karabekir.
  - Roman kesiti: Kemal Tahir.
  - Parti programı: Serbest Cumhuriyet Fırkası.
  - Tablo: Atatürk dönemi demokratikleşme adımları; Londra Konferansı–Kars sınırı durum-sonuç tablosu.
- **Kökler:**
  - "Bu bilgilere göre hangisine ulaşılabilir?"
  - "Hangi ilkenin / temel esasın önemini vurgular?"
  - Neden-sonuç ilişkisi.
- **Saf ezber sorusu gözlenmedi.**
- **Atatürk ilkeleri ve temel esaslar her yıl 2 ya da daha fazla soruda kullanılıyor (İTA.8.4.1, İTA.8.4.9):**
  - 2024: inkılapçılık esasları ve laiklik.
  - 2025: inkılapçılık ve millîlik.
  - 2026: Sümerbank ile devletçilik ve halkçılık.
- **Sıra kronolojik değil.** 2025'te ilke soruları testin başındaydı.
- **Geç dönem üniteleri soruluyor.** Demokratikleşme (Ünite 5) ve dış politika (Ünite 6) 2025 ve 2026'da 1'er soru aldı: Musul sorunu (2025), barışçı dış politika (2026). Ünite 7 gözlenmedi.

**Kalite ve zorluk**
- p = 0,47 → 0,49 → 0,53.
- 2026'da ayırt edicilik 0,60 ile üç yılın en yükseği.

**2027 beklentisi**
- Ünite 2 (Millî Uyanış) 3, Ünite 3 ve Ünite 4 ikişer, Ünite 1, 5 ve 6 birer soru.
- Ünite 7 için bankada az sayıda soru tutulmalı.

**T.C. İnkılap Tarihi ve Atatürkçülük için 2.000'lik bankadaki pay:** 222 soru, hedef ortalama p ≈ 0,5

| Soru tipi | Pay | Kota |
|---|---|---|
| Kaynak metinden çıkarım | %45 | 100 |
| Atatürk sözü → ilke/temel esas | %25 | 56 |
| Neden-sonuç ilişkilendirme | %10 | 22 |
| Tablo, şema, zaman çizelgesi | %10 | 22 |
| Edebî metin/sanata yansıma | %5 | 11 |
| Olumsuz kök ile eleme | %5 | 11 |

Zorluk karması (1 = en kolay, 5 = en zor): 1. seviye %5 (11) · 2. seviye %25 (56) · 3. seviye %40 (89) · 4. seviye %25 (55) · 5. seviye %5 (11)

**Kaçınılacaklar:** Tarih/ad ezberine dayalı bilgi soruları (2024-2026'da gözlenmedi). Ünite 7'ye aşırı ağırlık (2024-2026 kitapçıklarında gözlenmedi).

### 4.5 Din Kültürü ve Ahlak Bilgisi

| Ünite / blok | 2024 | 2025 | 2026 | Ağırlıklı pay | 2027 beklenen | Banka kotası |
|---|---|---|---|---|---|---|
| Kader İnancı | 2 | 5 | 1 | %29,4 | **3** (2,9) | 66 |
| Zekât ve Sadaka | 2 | 2 | 3 | %26,7 | **3** (2,7) | 59 |
| Din ve Hayat | 2 | 0 | 2 | %14,4 | **1** (1,4) | 32 |
| Hz. Muhammed'in Örnekliği | 2 | 2 | 2 | %22,2 | **2** (2,2) | 49 |
| Kur'an-ı Kerim ve Özellikleri | 1 | 0 | 1 | %7,2 | **1** (0,7) | 16 |
| *ünitesi belirsiz* | 1 | 1 | 1 | – | – | – |

**Soru türleri**
- **Ünite sonu sure ve peygamber kazanımları soruluyor:**
  - Maûn suresi (2024).
  - Âyetü'l-Kürsî hakkında numaralı bilgiler (2026).
  - Hz. Musa, Hz. Şuayb ve Hz. Yusuf eşleştirme tablosu (2024).
- **Siyer örnek olayları:**
  - Hicret: Abdullah bin Ureykıt, olumsuz kökle "çıkarılamaz" (2024).
  - İbrahim'in vefatı ve Güneş tutulması (2024).
  - İstişare olayları (2025).
  - Mekke'nin fethinde af (2026).
- **Kavram ayrımları:**
  - Kader-kaza tanımları (2025).
  - Tevekkül: millî futbolcunun gol sevinci örneği (2025).
  - Zekâtın şartları ve verilebilecek yakınlar (2025, 2026).
  - Takrirî sünnet (2026).
- **Öncüllü (I-II-III/IV) sorular:** Her yıl 2–3 tane.

**Kalite ve zorluk**
- En kolay test: p = 0,57 → 0,59 → 0,63.
- 2026 güvenirliği (0,72) testler arasında en düşük.
- Uzmanlar 2026 dağılımı konusunda ayrıştı: bir kısmına göre Kader ve Zekât ağırlıklı, bir kısmına göre dengeli.

**2027 beklentisi**
- Kader 2–3, Zekât ve Sadaka 2–3, Hz. Muhammed'in Örnekliği 2, Din ve Hayat 1–2, Kur'an-ı Kerim 1 soru.
- Bankada bütün sure ve peygamber kazanımları temsil edilmeli: 8.1.5, 8.1.6, 8.2.4, 8.2.5, 8.3.3, 8.3.4, 8.4.9, 8.5.4.

**Din Kültürü ve Ahlak Bilgisi için 2.000'lik bankadaki pay:** 222 soru, hedef ortalama p ≈ 0,6

| Soru tipi | Pay | Kota |
|---|---|---|
| Ayet, hadis, sure yorumu | %30 | 67 |
| Örnek olay (siyer) | %25 | 56 |
| Kavram bilgisi uygulama | %20 | 44 |
| Öncüllü numaralı yargılar | %15 | 33 |
| Metinde vurgulanan düşünce | %10 | 22 |

Zorluk karması (1 = en kolay, 5 = en zor): 1. seviye %10 (22) · 2. seviye %30 (67) · 3. seviye %40 (89) · 4. seviye %15 (33) · 5. seviye %5 (11)

**Kaçınılacaklar:** Mezhep/fıkıh ayrıntısına giren, program dışı hüküm soruları. Tek bir yoruma kapalı olmayan ahlaki ikilemler.

### 4.6 İngilizce

| Ünite / blok | 2024 | 2025 | 2026 | Ağırlıklı pay | 2027 beklenen | Banka kotası |
|---|---|---|---|---|---|---|
| Friendship | 2 | 2 | 1 | %16,6 | **1** (1,7) | 36 |
| Teen Life | 0 | 1 | 1 | %7,5 | **1** (0,8) | 16 |
| In the Kitchen | 1 | 1 | 1 | %10,3 | **1** (1,0) | 22 |
| On the Phone | 1 | 1 | 1 | %10,3 | **1** (1,0) | 22 |
| The Internet | 1 | 0 | 1 | %6,8 | **1** (0,7) | 15 |
| Adventures | 1 | 1 | 1 | %10,3 | **1** (1,0) | 22 |
| Tourism | 1 | 2 | 2 | %17,8 | **2** (1,8) | 38 |
| Chores | 1 | 1 | 1 | %10,3 | **1** (1,0) | 22 |
| Science | 1 | 1 | 1 | %10,3 | **1** (1,0) | 22 |
| Natural Forces | 0 | 0 | 0 | %0,0 | **0** (0,0) | 7 |
| *ünitesi belirsiz* | 1 | 0 | 0 | – | – | – |

**Soru türleri**
- **Dil:** Kökler İngilizce.
- **Ünite dağılımı:** Her ünite yaklaşık bir kez soruluyor. Tourism 2025 ve 2026'da ikişer, Friendship 2024 ve 2025'te ikişer soru aldı.
- **En sık biçim:** 3–4 kişinin kısa görüş, mesaj ya da diyaloğu üzerine "Who…?" veya "Which two…?". Örnekler: İstanbul hakkında görüşler, macera sporları, hafta sonu planları.
- **Diğer biçimler:**
  - Diyalog tamamlama ve "cannot be the answer" türü soru-cevap eşleme.
  - Ölçüte uyan davetiye kartı.
  - Tablo, ilan, afiş ve blog tablosu okuma.
  - İşlev tanıma: aynı işlevi gören telefon cümleleri (2026; uzmanlara göre en dikkat çekici madde).
  - Kelime sınıflama: pişirme yöntemi ve mutfak araçları (2025).
- **Olumsuz kök:** NOT, cannot, none sık. 2025'te en az 5 soru.
- **Dilbilgisi:** Ayrı dilbilgisi sorusu yok. Present continuous ile past ayrımı, tercih ve zorunluluk ifadeleri bağlam içinde ölçülüyor.
- **Ünite 10:** Natural Forces üç yılda hiç gözlenmedi.

**Kalite ve zorluk**
- p = 0,52 → 0,44 → 0,44.
- 2026'da ayırt edicilik 0,69, güvenirlik 0,88; ikisi de testler arasında en yüksek.

**2027 beklentisi**
- Ünite 1–9'dan birer soru; Tourism ya da Friendship'ten ikinci bir soru.
- Natural Forces için bankada az sayıda soru tutulmalı.

**İngilizce için 2.000'lik bankadaki pay:** 222 soru, hedef ortalama p ≈ 0,45

| Soru tipi | Pay | Kota |
|---|---|---|
| 3–4 kişilik kısa metin → kişi seçme | %35 | 78 |
| Diyalog tamamlama/soru-cevap | %20 | 45 |
| Tablo, ilan, afiş okuma | %15 | 33 |
| Okuma parçası (çıkarım, başlık) | %15 | 33 |
| İşlev/kelime sınıflama | %10 | 22 |
| Davetiye/mesaj ölçütü | %5 | 11 |

Zorluk karması (1 = en kolay, 5 = en zor): 1. seviye %5 (11) · 2. seviye %25 (56) · 3. seviye %40 (89) · 4. seviye %25 (55) · 5. seviye %5 (11)

**Kaçınılacaklar:** Ünite 10 Natural Forces'a aşırı ağırlık (2024-2026'da gözlenmedi). Yalnız dilbilgisi kuralını soran bağlamsız maddeler.

## 5. Güncel 8. sınıf matematik verisiyle karşılaştırma

Kullanıcının paylaştığı güncel örnek veri incelendi (`8-sinif-matematik-oyun-ornek.zip`: dört paket, 1.400 soru, 28 görev, 274 yanılgı kaydı).
- Kazanım kodları MEB 2018 programıyla bire bir aynı.
- Görev → kazanım eşlemesi plana aktarıldı (`subjects.Matematik.taskMap`).

| Ölçüt | Güncel veri | LGS 2024–2026 (matematik) |
|---|---|---|
| Görev ağırlığı | 28 görevin her biri 50 soru (eşit) | Eşit değil: Doğrusal Denklemler/eğim 3–4, Kareköklü 2–3; yedi ünite 1'er soru |
| Kök uzunluğu | Ortalama 18 sözcük; %1,3'ü ≥ 40 sözcük | Soruların yaklaşık yarısı çok cümleli gerçek yaşam bağlamıyla açılıyor |
| Görsel | %52,5 (735/1.400) | %75–90 (her yıl 15–18/20) |
| Çok kazanımlı soru | Görev odaklı, tek kazanım | Her yıl 3–5 seçici çok kazanımlı soru |
| Öncüllü / olumsuz kök | 7 / 19 soru (%0,5 / %1,4) | Öncüllü yok; olumsuz kök yaklaşık 1/20 |
| Zorluk (1–5) | %20 / 30 / 30 / 16 / 4 | Resmî p ≈ 0,28–0,33 (en zor test) → 3–5. seviye ağırlıklı karma |
| Çeldirici | Yanılgı anahtarlı (%69,5 dolu) | Hesaplanmış, adlandırılabilir hatalar |
| Şekil türü | 204 koordinat ve 1 açı şekli oyunca desteklenmiyor | Eğim ve doğrusal grafik soruları koordinat düzlemi kullanıyor |

**Değerlendirme**
- Güncel veri, kazanım öğretimi ve oyun için iyi bir temel. Yanılgı kataloğu da LGS tarzı çeldirici üretimi için doğrudan kullanılabilir.
- Ancak LGS'yi yansıtmıyor: kökler kısa, ağırlıklar eşit ve zorluk düşük.

**2027 bankası için öneriler**
1. **Katman.** Mevcut görev yapısını koruyun ve üzerine "LGS 2027" katmanı ekleyin. Katmanın kotaları planın `taskQuotas` alanındadır (aşağıdaki tablo).
2. **Bağlam.** LGS tarzı maddelerde 2–5 cümlelik bağlam ve gerekli şekil, tablo ya da grafik kullanın. Yalnızca işlem soran maddeler formun yaklaşık %10–15'i olmalı.
3. **Çok kazanımlı maddeler.** Matematik bankasının %10'u çok kazanımlı seçici maddelerden oluşmalı. Önerilen eşleşmeler: eğim + Pisagor, silindir + denklem, benzerlik + Pisagor, EBOB-EKOK + eşitsizlik, daire grafiği + bölünebilme.
4. **Şekil türleri.** Oyunun koordinat ve açı şekillerini desteklemesi gerekiyor. Destek gelene kadar bu soruları diagram olarak çizin; eğim ve doğrusal grafik soruları LGS'de her yıl var.
5. **Fen.** `curriculum/tr-grade8-current-unit-knowledge.json` dosyasındaki F.8.5 bilgi kartında "moment dengesi kuvvet ile dik uzaklığın çarpımına dayanır" ifadesi var. 2024 iptal kararıyla çeliştiği için banka üretiminde kullanılmamalı.

| Görev | Konu | Güncel veri | 2027 LGS katmanı kotası |
|---|---|---|---|
| M8-T01 | Pozitif tam sayıların çarpanları ve asal çarpan gösterimi | 50 | 4 |
| M8-T02 | EBOB, EKOK ve aralarında asal sayılar | 50 | 9 |
| M8-T03 | Tam sayı kuvvetleri ve üslü ifadelerin kuralları | 50 | 25 |
| M8-T04 | 10 sayısının kuvvetleri ve bilimsel gösterim | 50 | 23 |
| M8-T05 | Kareköklü sayıların büyüklüğü ve eşdeğer gösterimi | 50 | 22 |
| M8-T06 | Kareköklü ifadelerle işlemler ve doğal sayı çarpanları | 50 | 26 |
| M8-T07 | Ondalık karekökler ve gerçek sayılar | 50 | 13 |
| M8-T08 | Üç veri grubuna kadar çizgi ve sütun grafikleri | 50 | 14 |
| M8-T09 | Sütun, daire ve çizgi grafikleri arasında dönüşüm | 50 | 10 |
| M8-T10 | Olası durumlar ve eşit şans | 50 | 10 |
| M8-T11 | Basit olayların olasılığı ve tümleyen | 50 | 14 |
| M8-T12 | Cebirsel ifadeler ve çarpma modelleri | 50 | 31 |
| M8-T13 | Özdeşlik modelleri ve çarpanlara ayırma | 50 | 17 |
| M8-T14 | Rasyonel katsayılı birinci derece denklemler | 50 | 32 |
| M8-T15 | Koordinat sistemi ve sıralı ikililer | 50 | 5 |
| M8-T16 | Doğrusal ilişkilerin tablo, denklem ve grafikleri | 50 | 20 |
| M8-T17 | Eğim ve doğrusal gösterimler | 50 | 20 |
| M8-T18 | Eşitsizlik cümleleri ve sayı doğrusu | 50 | 18 |
| M8-T19 | En çok iki işlemli eşitsizliklerin çözümü | 50 | 13 |
| M8-T20 | Üçgenin yardımcı elemanları ve çizim koşulları | 50 | 6 |
| M8-T21 | Üçgende kenar ve açı ilişkileri | 50 | 22 |
| M8-T22 | Pisagor bağıntısı ve dik üçgen problemleri | 50 | 19 |
| M8-T23 | Eş ve benzer çokgenlerin ilişkileri | 50 | 24 |
| M8-T24 | Öteleme ve görüntü ilişkileri | 50 | 5 |
| M8-T25 | Yansıma ve iki adımlı dönüşüm görüntüleri | 50 | 19 |
| M8-T26 | Dik prizma ve silindirin elemanları ve açınımları | 50 | 7 |
| M8-T27 | Dik dairesel silindirin yüzey alanı ve hacmi | 50 | 14 |
| M8-T28 | Dik piramit ve koninin elemanları ve açınımları | 50 | 3 |
| **Toplam** | | **1.400** | **445** |

## 6. 2027 tahmin modeli ve soru bankası planı

**Yöntem** (`tools/build_lgs_2027_plan.py`):
1. **Ünite payları.** Her yıl, ünitesi belirlenen sorular içindeki ünite payı hesaplanır. Bu paylar 2024: 0,25, 2025: 0,35, 2026: 0,40 ağırlıklarıyla ortalanır.
2. **Sınav formu.** Ağırlıklı pay × soru sayısı = "2027 beklenen". Tam sayıya en büyük kalan yöntemiyle çevrilir.
3. **Banka kotası.** Ders kotaları sınavdaki soru sayısıyla orantılıdır. 2.000 soruda Türkçe 445, Matematik 445, Fen 444, İnkılap 222, Din 222, İngilizce 222.
   - Hiç gözlenmeyen ama programda olan ünitelere en az %3 pay verilir: İnkılap Ünite 7, İngilizce Natural Forces.
4. **Kazanım kotası.** Ünite içinde kazanım ağırlığı = test edilebilirlik × (1 + 2 × birincil gözlem + 1 × ikincil gözlem + tahmin bonusu).
   - Test edilebilirlik çarpanları: dinleme/konuşma ve üretime dayalı yazma kazanımları "none" (0); kısmen ölçülebilenler "partial" (0,3).
   - Tahmin bonusu dönüşümlü konular için verilir: fiilimsi +2, cümle türleri +1, anlatım bozukluğu +1.
5. **Görev kotası (Matematik).** Kazanım kotaları güncel verideki 28 göreve aktarılır.

| Ders | 2027 için beklenen form (ünite: soru) |
|---|---|
| Türkçe (20) | Sözcük ve söz öbeğinde anlam 1 · Cümlede anlam 3 · Paragraf ve okuduğunu anlama 8 · Sözel mantık, görsel, tablo ve grafik okuma 3 · Dil bilgisi 3 · Yazım kuralları 1 · Noktalama işaretleri 1 |
| Matematik (20) | Çarpanlar ve Katlar 1 · Üslü İfadeler 2 · Kareköklü İfadeler 3 · Veri Analizi 1 · Basit Olayların Olma Olasılığı 1 · Cebirsel İfadeler ve Özdeşlikler 2 · Doğrusal Denklemler 4 · Eşitsizlikler 1 · Üçgenler 2 · Dönüşüm Geometrisi 1 · Eşlik ve Benzerlik 1 · Geometrik Cisimler 1 |
| Fen Bilimleri (20) | Mevsimler ve İklim 1 · DNA ve Genetik Kod 3 · Basınç 2 · Madde ve Endüstri 5 · Basit Makineler 2 · Enerji Dönüşümleri ve Çevre Bilimi 4 · Elektrik Yükleri ve Elektrik Enerjisi 3 |
| T.C. İnkılap Tarihi ve Atatürkçülük (10) | Bir Kahraman Doğuyor 1 · Millî Uyanış 3 · Millî Bir Destan 2 · Atatürkçülük ve Çağdaşlaşan Türkiye 2 · Demokratikleşme Çabaları 1 · Atatürk Dönemi Türk Dış Politikası 1 |
| Din Kültürü ve Ahlak Bilgisi (10) | Kader İnancı 3 · Zekât ve Sadaka 3 · Din ve Hayat 1 · Hz. Muhammed'in Örnekliği 2 · Kur'an-ı Kerim ve Özellikleri 1 |
| İngilizce (10) | Friendship 1 · Teen Life 1 · In the Kitchen 1 · On the Phone 1 · The Internet 1 · Adventures 1 · Tourism 2 · Chores 1 · Science 1 |

**Soru yazım ilkeleri (bütün dersler)**
1. **Özgünlük.** LGS sorusu kopyalanmaz. Aynı kazanım, aynı beceri ve aynı biçimde yeni bir bağlam yazılır.
2. **Etiketler.** Her soru envanterdeki gibi ünite/blok, kazanım, biçim, zorluk (1–5) ve yanılgı anahtarlı çeldirici gerekçesi taşır.
3. **Kalıp çeşitliliği.** Aynı kurgu aynı ünitede en fazla birkaç kez kullanılır; bağlam, sayı ve görsel değiştirilir (`AUTHORING_RULES.md` §4).
4. **Belirsizlik denetimi.** "En kısa", "ip ağırlığı önemsiz", "sürtünme yok", "tek anlam" gibi koşullar açıkça yazılır (§3'teki olaylar).
5. **Doğrulama.** Üretilen paketler `tools/pack_validate.py` ile denetlenir. Doğru cevap konumları dengelenir.

## 7. Belirsizlikler ve doğrulama planı

**Düşük güvenli ya da eksik alanlar**
- 2026 sayısal A numaralandırması ve A cevap anahtarı.
- İçeriği bulunamayan 11 soru:
  - İnkılap 2024: 1, 7, 8; 2025: 5.
  - Din 2024: 3; 2025: 7; 2026: 6.
  - Türkçe 2026: 5, 15.
  - Matematik 2026 (B kitapçığı): 1, 10.
- İçeriği bilinen ama ünitesi belirlenemeyen 2 soru: Matematik 2026 (B kitapçığı) 14 ('Bizim Çocuklar' afişi) ve İngilizce 2024 4 (kurs seçimi tablosu).
- Türkçe paragraf sorularının çoğunda kök görülemedi.
- 2025 Din'de Kader ünitesi 5 soru görünüyor; bunların bir kısmı düşük güvenli.
- 2025 Türkçe 16'nın cevabı B mi C mi, çelişkili.

**Ağ izni verildiğinde**
1. Envanterdeki `exams.*.booklets` PDF'lerini indirin.
2. Metni `pdftotext` ile çıkarın ve her kaydı numara, konu ve cevap açısından doğrulayın. Önce düşük güvenli kayıtlar.
3. Envanteri güncelleyip `python tools/build_lgs_2027_plan.py` çalıştırın.

**2027'ye kadar izlenecekler**
- MEB örnek soruları ve MEBİ denemeleri (Kasım 2026 →).
- 2027 kılavuzu (Mart 2027): kapsam cümlesi, tarih, süreler.
- Ünite 7 / Natural Forces gibi gözlenmeyen konular örnek sorularda belirirse plandaki taban paylar artırılmalı.

## 8. Başlıca kaynaklar

**Kitapçıklar** (ÖDSGM/EBA)
- 2024: https://cdn.eba.gov.tr/yardimcikaynaklar/2024/06/lgs/2024sozel.pdf · https://cdn.eba.gov.tr/yardimcikaynaklar/2024/06/lgs/2024sayisal.pdf
- 2025: https://cdn.eba.gov.tr/yardimcikaynaklar/2025/06/lgs/2025sozel.pdf · https://cdn.eba.gov.tr/yardimcikaynaklar/2025/06/lgss/2025sayisal.pdf
- 2026: https://cdn.eba.gov.tr/yardimcikaynaklar/2026/06/trlgs/a_2026_sozel.pdf · https://cdn.eba.gov.tr/yardimcikaynaklar/2026/06/trlgs/b_2026_sayisal.pdf

**Resmî istatistik ve raporlar**
- 2024 sonuçları: https://www.meb.gov.tr/lgs-kapsamindaki-merkezi-sinav-sonuclari-aciklandi/haber/34178/tr
- 2025 özet rapor: https://cdn.eba.gov.tr/yardimcikaynaklar/2025/07/LGS2025MerkeziSinavOzetRapor.pdf
- 2025 istatistikleri: https://odsgm.meb.gov.tr/meb_iys_dosyalar/2025_07/16205446_2025lgsistatistikleri.pdf
- 2026 raporu: https://www.meb.gov.tr/2026-lgs-kapsaminda-merkezi-sinav-raporu-yayimlandi/haber/41333/tr

**Kapsam**
- 2026 kılavuzu: https://www.meb.gov.tr/meb_iys_dosyalar/2026_04/03170012_LGS_Basvuru_ve_Uygulama_Kilavuzu_2026_.pdf
- 2025 kılavuzu: https://www.meb.gov.tr/2025-lgs-kapsamindaki-merkezi-sinav-icin-basvuru-ve-uygulama-kilavuzu-yayimlandi/haber/36648/tr
- 2023 kapsam kararı: https://www.meb.gov.tr/2023-lgsde-8-sinifin-yksde-12-sinifin-ikinci-donem-konulari-sinav-kapsamina-dhil-olmayacak/haber/29003/tr

**Ders kitabı uyumu (2025)**
- https://www.meb.gov.tr/lgs-sinav-sorularinin-temel-kaynagi-ucretsiz-dagitilan-ders-kitaplari-oldu/haber/38347/tr

**2028 soru modeli**
- https://www.meb.gov.tr/yks-ve-lgsde-yeni-mufredata-uyumlu-soru-modeli-2028de-hayata-gececek/haber/39265/tr
- https://www.pervinkaplan.com/detay/bakan-tekin-sinav-sistemi-degil-sorular-degisecek/33756

**İptal ve itiraz**
- https://www.hurriyet.com.tr/egitim/lgsde-tartisilan-soru-iptal-edildi-42529957
- https://www.pervinkaplan.com/detay/2025-lgs-tartisilan-matematik-sorusuna-meb-ne-yanit-verdi/31523

Soru bazındaki kaynaklar envanterdeki `sources` alanlarındadır.

## Ek A. Soru soru envanter (A kitapçığı; 2026 sayısal B kitapçığı)

Özetler kısaltılmıştır. Tam kayıt, kazanım ve kaynaklar için envanter JSON'una bakın.

### Türkçe

**2024 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | Sözcük ve söz öbeğinde anlam (deyim, atasözü) | T.8.3.5 | 'Bırakmak' fiilinin farklı cümlelerdeki anlamları (ör. bir işi bırakıp başka biriyle ilgilenmek); çok anlamlılık. | A | medium |
| 2 | Sözcük ve söz öbeğinde anlam (deyim, atasözü) | T.8.3.6 | Seçeneklerdeki kısa metinlerden hangisinde ayraç içinde verilen deyimin anlattığı duruma uygun bir durum bulunduğu soruluyor. | C | high |
| 3 | Cümlede anlam (cümle birleştirme dahil) | T.8.3.25 | Bir parçadaki numaralanmış cümlelerden hangisinde koşul anlamı bulunduğu soruluyor. | D | high |
| 4 | Dil bilgisi (fiilimsi, öge, çatı, cümle türü, anlatım bozukluğu) | T.8.3.8 | Seçenek cümlelerden hangisinde anlatım bozukluğu bulunmadığı soruluyor. | C | high |
| 5 | Cümlede anlam (cümle birleştirme dahil) | T.8.4.15 | Verilen cümlelerin anlam bütünlüğü bozulmadan doğru biçimde birleştirildiği seçenek soruluyor. | A | high |
| 6 | Cümlede anlam (cümle birleştirme dahil) | T.8.3.21 | Zamanı içinde çok fırsat barındıran, fırsatı da içinde çok zaman barındıran şey olarak tanımlayan cümleye anlamca en yakın ifade. | D | high |
| 7 | Paragraf ve okuduğunu anlama | T.8.3.17 | Sosyal medyayı insanların değil, sosyal medyanın insanları kullandığı düşüncesini işleyen eleştirel paragraf; kök görülmedi. | C | low |
| 8 | Sözel mantık, görsel, tablo ve grafik okuma | T.8.3.25 | Öğretmenin ilkbahar için verdiği ödev etkinliklerinden gözlem, uygulama ve tasarı gerçekleştirme koşullarının üçünü birden karşılayanı bulma. | B | medium |
| 9 | Paragraf ve okuduğunu anlama | T.8.3.17 | Bir şiirin ana düşüncesi (seçeneklerde geçmişe takılmadan yaşamak, şimdinin değeri, hüzünlü anılardan uzak durmak gibi temalar). | A | medium |
| 10 | Paragraf ve okuduğunu anlama | T.8.3.25 | paragraf – geleneksel mahalle yaşamında kedilerin yeri; hangi yargıya ULAŞILAMAZ | C | medium |
| 11 | Sözcük ve söz öbeğinde anlam (deyim, atasözü) | T.8.3.5 | altı çizili ifadenin anlamı – toplumun '…mış gibi yapanlar topluluğu'na dönüşmesi (sosyal medya); hangisi buna ÖRNEK OLAMAZ | B | medium |
| 12 | Paragraf ve okuduğunu anlama | T.8.3.25 | Bir metinde bilgi, durum ve olaylar arasında mantıksal tutarlılık bulunmamasının anlatım kusuru sayıldığını açıklayan bilgi; buna göre değerlendirme (kök tam görülmedi). | D | low |
| 13 | Paragraf ve okuduğunu anlama | T.8.3.25 | Dilin milleti millet yapan temel unsurlardan biri olduğu ve korunması gerektiği açıklaması; 'Bu açıklamaya göre…' kökü. | A | low |
| 14 | Dil bilgisi (fiilimsi, öge, çatı, cümle türü, anlatım bozukluğu) | T.8.3.9 | 'Ebe' içeren bir çocuk oyununun anlatıldığı parçada numaralanmış sözcüklerden (I–IV) hangisinin fiilimsi olmadığı. | A | low |
| 15 | Sözel mantık, görsel, tablo ve grafik okuma | T.8.3.32 | Rüzgâr türbinleri bağlamı: Tablo 1 rüzgâr türlerini hızlarına göre (hafiften tam fırtınaya) sıralıyor; Tablo 2'deki saat aralıklarına göre üretilen elektriği doğru gösteren sütun grafiği. | B | high |
| 16 | Sözel mantık, görsel, tablo ve grafik okuma | T.8.3.27 | Yan flütte notaların hangi parmakla hangi kapağa basılarak çalındığını gösteren görsel ve bilgi; kök görülmedi. | C | medium |
| 17 | Yazım kuralları | T.8.4.16 | Konya'nın Hadim ilçesinin Türkiye'de kirazın en geç hasat edildiği yerlerden biri olduğu ve buradaki bir kiraz çeşidinin uzak pazarlara gönderildiği bilgisi; kök görülmedi. | B | low |
| 18 | Noktalama işaretleri | T.8.4.16 | Şehirler ve öne çıkan kişiler üzerine parçada virgülün hangi işlevinde kullanılmadığı. | D | medium |
| 19 | Sözel mantık, görsel, tablo ve grafik okuma | T.8.3.35 | 'İlkbahar, Yaz, Sonbahar, Kış' oyununun kuralları (oyunculardan biri hakem seçilir…); kök görülmedi – kurallara dayalı sözel mantık maddesi olması muhtemel. | D | low |
| 20 | Dil bilgisi (fiilimsi, öge, çatı, cümle türü, anlatım bozukluğu) | T.8.4.19 | Anadolu kültürünü Türkiye Yüzyılı'nın temel dayanağı olarak niteleyen cümlenin türüyle ilgili yanlış ifade. | C | medium |

**2025 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | Paragraf ve okuduğunu anlama | T.8.3.21 | Hiç tanımadığımız hâlde ilk bakışta kendini belli eden insanlar üzerine kısa metin; kök görülmedi. | B | medium |
| 2 | Sözcük ve söz öbeğinde anlam (deyim, atasözü) | T.8.3.5 | Dostlara karşı tutumu anlatan metinde boşluklara düşüncenin akışına göre sırasıyla getirilecek ifadeler (ikili sıfat/söz öbeği seçenekleri, ör. 'pes etmemiş – koruyucu'). | A | medium |
| 3 | Cümlede anlam (cümle birleştirme dahil) | T.8.3.25 | Bir sanatçının 'birçok türde yazdım ama kendimi en iyi şiirle ifade ettim' anlamındaki sözünden kesin olarak çıkarılabilecek yargı. | C | medium |
| 4 | Cümlede anlam (cümle birleştirme dahil) | T.8.3.21 | Yabancı kültür ögelerini birebir kopyalamak yerine millî değerlerle yorumlayıp yeni ürünler ortaya koymaya çağıran cümlede anlatılmak istenen düşünce. | D | medium |
| 5 | Dil bilgisi (fiilimsi, öge, çatı, cümle türü, anlatım bozukluğu) | T.8.3.8 | Nesne eksikliğinden kaynaklanan anlatım bozukluğu (seçenek cümleleri deneme türü/yazarı üzerine; birinde eskimiş düşünceler-paslı çiviler benzetmesi). | C | medium |
| 6 | Paragraf ve okuduğunu anlama | T.8.3.25 | Düşüncelerini özgürce dile getiren deneme yazarı üzerine metin; '- - - -' ile boş bırakılan yere getirilecek cümle. | D | low |
| 7 | Söz sanatları | T.8.3.7 | Hangi seçenekteki dizelerde söz sanatı kullanılmadığı (dizelerden biri damların göğe bakmaktan usanmasıyla kişileştirme içeriyor). | B | medium |
| 8 | Paragraf ve okuduğunu anlama | T.8.3.18 | Sözcükleri büyüteç gibi kullanan ve İstanbul adalarından birini anlatan bir yazar üzerine metin; vurgulanan yazar özelliği (seçenekler: tarafsızlık, kararlılık, fedakârlık, alçak gönüllülük). | D | medium |
| 9 | Paragraf ve okuduğunu anlama | T.8.3.25 | İyi bir arka kapak yazısının kitabın içeriğiyle uyumlu olması ölçütü; seçeneklerdeki kitap tanıtım yazılarından uygun olanı. | C | medium |
| 10 | Sözcük ve söz öbeğinde anlam (deyim, atasözü) | T.8.3.5 | Büyük şairler hakkında yazılan eleştiri kitaplarındaki abartılı övgüler üzerine metin; altı çizili ifadenin anlamı (kesin değil). | A | low |
| 11 | Paragraf ve okuduğunu anlama | T.8.3.20 | Kapağı işlemeli köstekli saatini sık sık çıkaran Tarık'ın anlatıldığı öyküleyici parça; kök görülmedi (karakter/duygu çıkarımı olabilir). | D | low |
| 12 | Paragraf ve okuduğunu anlama | T.8.3.17 | 'Okumanın rastgele ve bilinçsizce yapılması' üzerine paragraf; kök görülmedi. | C | low |
| 13 | Yazım kuralları | T.8.4.16 | Otomobillerde dokunmatik ekran kullanımı ve kullanılabilirlik testleri metni: (a) numaralanmış cümlelerden hangisinde yazım yanlışı olmadığı, (b) numaralanmış yerlerden hangisine üç nokta getirileceği – aynı metne bağlı iki soru. | D | medium |
| 14 | Sözel mantık, görsel, tablo ve grafik okuma | T.8.3.32 | Grafik: bir ülkede beyaz eşya satışlarının iç pazar, ihracat ve toplam hacmi (2018–2023). | A | medium |
| 15 | Sözel mantık, görsel, tablo ve grafik okuma | T.8.3.32 | Bir ailenin yumurta üretimi, tüketimi ve satışına ilişkin bilgilerle tablo/sözel mantık maddesi (aday; kilit görseli 16. soru). | A | low |
| 16 | Sözel mantık, görsel, tablo ve grafik okuma | T.8.3.27 | Silindirli kilit sistemi ve anahtar görseli; anahtar çevrildiğinde açılabilir durumda olan kilit görseli. | B | medium |
| 17 | Dil bilgisi (fiilimsi, öge, çatı, cümle türü, anlatım bozukluğu) | T.8.4.20 | Cemil Meriç'in Türk kültürüne katkıları ve 38 yaşında görme yetisini kaybetmesi üzerine numaralanmış cümleler; kök görülmedi (dil bilgisi sorusu olabilir). | C | low |
| 18 | Paragraf ve okuduğunu anlama | T.8.3.17 | Akdeniz bitki örtüsü (keçiboynuzu, badem ağaçları) üzerine paragraf; kök görülmedi. | B | low |
| 19 | Paragraf ve okuduğunu anlama | T.8.3.17 | Türk eğitim tarihinin Türkistan bozkırlarından Anadolu'ya uzanan gelişimi üzerine paragraf; kök görülmedi. | A | low |
| 20 | Dil bilgisi (fiilimsi, öge, çatı, cümle türü, anlatım bozukluğu) | T.8.4.19 | Anadolu'nun bitki çeşitliliği açısından dünyanın en zengin bölgelerinden biri olduğunu anlatan numaralanmış cümleler; kök görülmedi. | B | low |

**2026 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | Cümlede anlam (cümle birleştirme dahil) | T.8.3.21 | Cahit Zarifoğlu üzerine kısa metin: yazılarının bütünü okununca yaşadığı dönemden bugünü okur gibi olunduğu (zamanı aşan gözlem) anlatılıyor; metindeki bir cümleye anlamca en yakın ifade ya da yazarın bakışına ilişkin anlam sor… | A | medium |
| 2 | Paragraf ve okuduğunu anlama | T.8.3.25 | Sözün, zamanı gelince muhatabını bulacağı düşüncesini işleyen metin; metne göre söylenemeyecek yargı (seçeneklerden biri sözü 'adressiz mektup' sayma fikri üzerine). | B | medium |
| 3 | Cümlede anlam (cümle birleştirme dahil) | T.8.3.25 | Bir yazarın çağdaşı/meslektaşı yazarlarla karşılaştırılarak anlatıldığı parça; parçadan çıkarım. | D | low |
| 4 | Cümlede anlam (cümle birleştirme dahil) | T.8.3.21 | Bir aydını tanımanın en iyi yolunun onun hangi tarihsel ve toplumsal zeminden seslendiğini belirlemek olduğunu söyleyen cümleye anlamca en yakın ifade (seçenekler düşünür-çağ-tarihsel/toplumsal atmosfer ilişkisi üzerine). | A | medium |
| 5 | — | — | — | D | unknown |
| 6 | Paragraf ve okuduğunu anlama | T.8.3.17 | Sosyal medyanın gerçeği çarpıttığı ve insanlar arasında sahte bir yakınlık yanılsaması yarattığı anlatılan paragraf (çağın parlak aynası benzetmesi); kök görülmedi. | C | medium |
| 7 | Sözel mantık, görsel, tablo ve grafik okuma | T.8.3.27 | Kuralların nitelikleri (toplumsal değerlere dayanma, davranışı yönlendirme, olumlu ve nesnel ifade, kuralın amacının belirtilmesi) anlatılıyor; seçeneklerdeki 'Laboratuvar Kuralları' afişlerinden bu ölçütlere uyanı bulma. | A | high |
| 8 | Paragraf ve okuduğunu anlama | T.8.3.25 | Behçet Necatigil ve şiirle geçen hayatı / bir şair ile kitapçı üzerine anlatı; anlatıcının duyguları ya da metinden çıkarım. | D | medium |
| 9 | Paragraf ve okuduğunu anlama | T.8.3.11 | Duyusal imgeler içeren betimleyici metin; seçeneklerde 'tanımlama, karşılaştırma, niteleyici sözcük kullanma' gibi anlatım teknikleri. | A | low |
| 10 | Paragraf ve okuduğunu anlama | T.8.3.25 | Yaşamda karşılaşılan sorunlar ve çözüm arayışı üzerine metin; metne göre hangi davranışın bir çözüm yolu örneği olamayacağı. | B | low |
| 11 | Paragraf ve okuduğunu anlama | T.8.3.20 | Odasını temizleyip kitaplığını düzenlemeye başlayan bir kişinin anlatıldığı öyküleyici parça; kök görülmedi. | D | low |
| 12 | Paragraf ve okuduğunu anlama | T.8.3.17 | XX. yüzyıl öncesinde insanların ihtiyacı kadar üretip tükettiğini, sonra tüketim alışkanlıklarının değiştiğini anlatan paragraf; kök görülmedi. | C | low |
| 13 | Paragraf ve okuduğunu anlama | T.8.3.11 | Şiirsel, betimleyici kısa metin (hafif rüzgâr, belli belirsiz bulutlar); kök görülmedi. | A | low |
| 14 | Sözel mantık, görsel, tablo ve grafik okuma | T.8.3.32 | Grafik: kıtalara göre orman alanlarındaki değişim (1990–2000, 2000–2010, 2010–2020); seçeneklerde Okyanusya, Avrupa, Kuzey Amerika karşılaştırmaları. | C | medium |
| 15 | — | — | — | D | unknown |
| 16 | Sözel mantık, görsel, tablo ve grafik okuma | T.8.3.27 | Görsel: yelkenli teknenin yelken sistemi ve tam açık hâli; verilen bilgiye göre teknenin hangi durumdan dolayı zarar gördüğü soruluyor. | C | high |
| 17 | Yazım kuralları | T.8.4.16 | 'İnsan yaş aldıkça…' diye başlayan, bölümleri I–IV ile numaralanmış metinde hangi bölümde yazım yanlışı bulunmadığı. | B | medium |
| 18 | Noktalama işaretleri | T.8.4.16 | Bir metinde ayraçla boş bırakılan yerlere (ör. bir yazar adından sonra) hangi noktalama işaretlerinin geleceği; metin Reşat Nuri Güntekin ile Muhsin Ertuğrul ilişkisi üzerine. | D | medium |
| 19 | Dil bilgisi (fiilimsi, öge, çatı, cümle türü, anlatım bozukluğu) | T.8.4.18 | Gümüşhane'den başlayan bir yolculuğu anlatan parçada numaralanmış cümlelerden hangisinde yer tamlayıcısı (dolaylı tümleç) bulunduğu. | C | medium |
| 20 | Dil bilgisi (fiilimsi, öge, çatı, cümle türü, anlatım bozukluğu) | T.8.4.20 | Kervansarayları anlatan bir belgesel metninde numaralanmış cümlelerdeki fiillerden hangisinin nesnesine göre farklı çatıda olduğu (geçişli/geçişsiz). | B | medium |

### Matematik

**2024 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | Cebirsel İfadeler ve Özdeşlikler | M.8.2.1.1 | Kenar uzunluğu (x+2) cm olan karenin çevresini veren cebirsel ifade (seçenekler x+8 / 4x+2 / 4x+4 / 4x+8). | D | high |
| 2 | Üslü İfadeler | M.8.1.2.5 | Bilimsel gösterim sorusu; seçenekler 3,5·10^7, 2,1·10^10 biçiminde. Kök metni çıkarılamadı. | B | medium |
| 3 | Kareköklü İfadeler | M.8.1.3.8 | Verilen kareköklü sayılardan hangisinin irrasyonel olduğu (seçenekler √14, √1,2?, √1,44, √12 benzeri; kök işaretleri metinde düşmüş). | A | high |
| 4 | Kareköklü İfadeler | M.8.1.3.5 | √363 − √75 − √27 işleminin sonucu (seçenekler 2√3…5√3). | B | high |
| 5 | Veri Analizi | M.8.4.1.1 | Bir müzeyi günün farklı saatlerinde ziyaret eden kişi sayılarını gösteren sütun grafiğine dayalı yorum sorusu. | B | high |
| 6 | Dönüşüm Geometrisi | M.8.3.2.2 | Eskimiş kısımları tamir edilecek dikdörtgen kilim kareli zeminde simetri doğrusuyla modelleniyor; simetriyle tamamlanınca beyaz bölgelerin alamayacağı desen soruluyor. | D | medium |
| 7 | Cebirsel İfadeler ve Özdeşlikler | M.8.2.1.2 | Kenarı 3x cm olan beyaz ve mavi kare kartonlar çakıştırılıp beyaz olan 1 cm yukarı ve 1 cm sola öteleniyor; görünen mavi bölgenin alanını veren cebirsel ifade isteniyor. | A | medium |
| 8 | Doğrusal Denklemler (eğim dahil) | M.8.2.2.1 | Gülsüm'ün kırmızı, yeşil ve mavi kalemlerinin uzunlukları arasındaki ilişkiler şekilde (2,8 cm ve 5,2 cm farklarla) veriliyor; birer kalem uç uca 56,1 cm iken kırmızı kalemin uzunluğu soruluyor. | A | medium |
| 9 | Eşitsizlikler | M.8.2.3.3 | Bir mağazada bir günde satılan pantolon (240 TL) ve gömlek (180 TL) sayıları tabloda; günlük gelir 12 000 TL'den az ise satılabilecek en fazla gömlek sayısı (38–41). | B | medium |
| 10 | Doğrusal Denklemler (eğim dahil) | M.8.2.2.5 | Bahçe ilaçlamada depoda kalan ilaç miktarı–zaman doğrusal grafiği; bahçe 5 saatte ilaçlanıyor; başlangıçtaki ilaç miktarı (L) soruluyor. | B | medium |
| 11 | Kareköklü İfadeler | M.8.1.3.2 | Televizyonun ses seviyesi ile ses göstergesi arasında verilen kural: sayı tam kare ise karekökü, değilse kareköküne en yakın doğal sayı gösteriliyor; kuralın uygulanması. | C | high |
| 12 | Üçgenler (Pisagor dahil) | M.8.3.1.3 | Bir öğrenci üçgenin kenar ve açıları arasındaki ilişkiyi pergelle inceliyor; üç farklı merkezli çember yayı çiziliyor. | D | medium |
| 13 | Doğrusal Denklemler (eğim dahil) | M.8.2.2.1 | 800 m'lik doğrusal parkurda A'dan B'ye gidip A'ya dönmek 1 tur; Efe 2. turda bir noktada duruyor ve A'ya uzaklığına ilişkin bir koşul veriliyor; konumla ilgili ölçü soruluyor. | A | low |
| 14 | Geometrik Cisimler | M.8.3.4.4 | Hacimleri 12 000 cm³ olan üç dik dairesel silindir parçadan oluşan 70 cm yükseklikte tabure; en üstteki parçanın yarıçapının ortadakine oranı (π=3). | D | high |
| 15 | Üslü İfadeler | M.8.1.2.2 | Kenarları 2^5 cm ve 2^6 cm olan 10 özdeş mavi dikdörtgenle oluşturulan ABCD dikdörtgeni içindeki sarı bölgenin çevresi. | C | medium |
| 16 | Çarpanlar ve Katlar | M.8.1.1.2 | Kütlesi 4 g olan mavi ve 28 g olan sarı bilyeler; toplam kütle 700 g'dan fazla olacak biçimde koşullar altında en az toplam bilye sayısı (uzmanların 'bilye sorusu'). | C | medium |
| 17 | Doğrusal Denklemler (eğim dahil) | M.8.2.2.6 | Ön yüz alanı 135 cm² olan 5 özdeş dikdörtgen çekmecenin dizilişinde CB'nin eğimi 4/3; A ile B arası uzaklık (36/45/48/54). | D | high |
| 18 | Eşlik ve Benzerlik | M.8.3.3.2 | Kareli zeminde KLMN karesi; A'dan başlayan yolla AKB üçgeni, ardından buna benzer üçgen oluşturan ikinci yol; en az toplam yol uzunluğu (15/18/20/25). | C | medium |
| 19 | Basit Olayların Olma Olasılığı | M.8.5.1.5 | 1–9 sayılarının yazıldığı 3×3 tabloda bazı kutucuklar mavi kartlarla kapatılmış; verilen koşullara göre II. satırdaki kapalı sayıların toplamı (17/12/11/3). | B | low |
| 20 | Üçgenler (Pisagor dahil) | M.8.3.1.5 | Uzunluğu 7 birim, genişliği 2 birim olan dikdörtgen biçimli bir yol modeli; /EA/ ile başlayan bir uzunluk soruluyor (metnin devamı okunamadı). | C | low |

**2025 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | Kareköklü İfadeler | M.8.1.3.4 | Kenar uzunluğu kareköklü bir ifade olarak verilen eşkenar üçgenin çevresi (metinde kök işareti düşmüş; '8 cm' okundu). | D | high |
| 2 | Üslü İfadeler | M.8.1.2.2 | Her birinin alanı 36 cm² olan altı eşkenar üçgenden oluşan düzgün altıgenin alanı; seçenekler 6'nın kuvvetleri biçiminde. | C | medium |
| 3 | Eşitsizlikler | M.8.2.3.3 | 11x − 17 ≤ 16 türünde birinci dereceden eşitsizliği sağlayan en büyük tam sayı (eşitsizlik sembolü metinde düşmüş). | C | high |
| 4 | Kareköklü İfadeler | M.8.1.3.5 | Kareli zeminde alanı 300 cm² olan dikdörtgen üzerinde KLMN ve PRST karelerinin çevrelerinin karşılaştırılması (OCR bozuk). | B | low |
| 5 | Dönüşüm Geometrisi | M.8.3.2.2 | Birim karelerden oluşan küp açınımı bağlamında yansıma (simetri doğrusuna göre görüntü) sorusu. | A | medium |
| 6 | Cebirsel İfadeler ve Özdeşlikler | M.8.2.1.1 | Dikdörtgen biçimli mavi ve kare biçimli sarı levhalarla oluşturulan şeklin çevresini veren cebirsel ifade. | D | medium |
| 7 | Eşitsizlikler | M.8.2.3.1 | Üç uçağın gösteri uçuşunda bir noktanın yüksekliğinin alabileceği değer aralığını gösteren eşitsizlik. | A | medium |
| 8 | Doğrusal Denklemler (eğim dahil) | M.8.2.2.1 | Turşucuda eşit ölçekli özdeş bardaklarda turşu suyu, havuç suyu ve acı sos oranlarıyla az ve çok acılı içecekler; 4 bardak az acılı + 1 bardak çok acılı içecekte toplam turşu suyu toplam acı sostan 400 mL fazla → bardağın hacmi. | B | medium |
| 9 | Doğrusal Denklemler (eğim dahil) | M.8.2.2.6 | Koordinat düzleminde 8 eş kareden oluşan dikdörtgenin köşegenlerinden birinin eğimi olamayacak değer. | D | medium |
| 10 | Cebirsel İfadeler ve Özdeşlikler | M.8.2.1.3 | Beyaz eşya satış tablosu; satışlardan elde edilen toplam gelir (2y + 3x)² TL; bir bulaşık makinesinin satış fiyatını veren cebirsel ifade (3x / 2y / 6y / 9x). | D | medium |
| 11 | Çarpanlar ve Katlar | M.8.1.1.2 | Kütleleri gram cinsinden doğal sayı olan 5 özdeş A cisminin toplam kütlesiyle ilgili koşullardan bir A'nın kütlesi (30/24/21/18). | B | low |
| 12 | Doğrusal Denklemler (eğim dahil) | M.8.2.2.6 | İki aracın yol–zaman ilişkisini gösteren doğrusal grafik; II. aracın I. araçtan kaç saat sonra harekete başladığı (1 / 1,8 / 2 / 2,3). | C | high |
| 13 | Eşlik ve Benzerlik | M.8.3.3.2 | Kareli zeminde [AD] ile [CF] B noktasında kesişiyor; /AB/ uzunluğu soruluyor. | C | low |
| 14 | Üslü İfadeler | M.8.1.2.2 | 1024 L'lik gübre deposu, her biri dakikada 2² L püskürten 24 memeli makine; 8 dakikada 48 dekar gübreleniyor; kalan gübreyle kaç dekar daha gübrelenebileceği. | B | medium |
| 15 | Üçgenler (Pisagor dahil) | M.8.3.1.5 | 8 cm uzunluğundaki dikdörtgen kâğıt üç parçaya kesilerek oluşturulan logo (Şekil II) üzerinde A ve B köşeleri arasındaki uzaklık — Pisagor. | B | high |
| 16 | Üçgenler (Pisagor dahil) | M.8.3.1.2 | Uzunlukları doğal sayı olan, en kısası n birim dört çubuktan hangileri uç uca birleştirilerek üçgen oluşturulabileceği. | D | medium |
| 17 | Basit Olayların Olma Olasılığı | M.8.5.1.5 | Yalnızca elma, erik ve ayva ağaçlarının bulunduğu, toplam 60 ağaçlık bahçe (soru kökü okunamadı). | A | low |
| 18 | Kareköklü İfadeler | M.8.1.3.7 | Mavi ve beyaz bölgeli özdeş iki dikdörtgen kâğıt mavi bölgeler çakışacak biçimde birleştiriliyor; uzun kenar 10,24 dm; beyaz bölgenin uzun kenarı (0,5 / 0,8 / 1 / 1,2). | C | low |
| 19 | Geometrik Cisimler | M.8.3.4.3 | Taban yarıçapı (okunan: 1 cm) ve yanal alanı 108 cm² olan ahşap silindir tabanlarına paralel kesilerek üç silindire ayrılıyor (Şekil I–II); kök kesik. | B | medium |
| 20 | Veri Analizi | M.8.4.1.1 | A, B, C, D vagonlu trende iki istasyondaki yolcular; iki istasyonda kadın yolcu toplamları eşit; I. istasyondaki en az erkek yolcu sayısı (204/170/153/136 — hepsi 17'nin katı). | A | low |

**2026 (B kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | — | — | — | D | unknown |
| 2 | Cebirsel İfadeler ve Özdeşlikler | M.8.2.1.3 | ABCD karesi dört özdeş sarı dikdörtgen, alanı 4y² cm² yeşil kare ve 4x² cm² mavi kareden oluşuyor; bir sarı dikdörtgenin alanını veren ifade (6xy/4xy/2xy/xy). | C | high |
| 3 | Kareköklü İfadeler | M.8.1.3.1 | Seçeneklerden hangisinin tam kare pozitif tam sayı olduğu (okunan seçenekler 3/9/18/27; kök işaretleri düşmüş olabilir). | B | medium |
| 4 | Dönüşüm Geometrisi | M.8.3.2.2 | Kareli zeminde mavi karenin d doğrusuna göre yansımasının hangi numaralı (I–IV) kareye düştüğü. | B | medium |
| 5 | Eşitsizlikler | M.8.2.3.1 | Lunaparkta oyuncaklara biniş için boy kurallarını veren tabela bağlamlı soru (eşitsizlik olması muhtemel). | A | low |
| 6 | Basit Olayların Olma Olasılığı | M.8.5.1.5 | Peynir ve patates katmanlı tepsiden kesilen kare dilimlerden rastgele seçilen birinin yalnız peynirli olma olasılığı. | B | medium |
| 7 | Cebirsel İfadeler ve Özdeşlikler | M.8.2.1.2 | Ayrıtı (2x+5) cm olan küp biçimli ahşap bloktan 5 cm yükseklikte kare prizma kesilip parçalar yeniden dizildiğinde sarı bölgenin alanını veren cebirsel ifade. | D | medium |
| 8 | Üslü İfadeler | M.8.1.2.4 | Yalnızca seçenekleri (10'un kuvvetleri) okunabilen soru; kök metni yok. | D | low |
| 9 | Doğrusal Denklemler (eğim dahil) | M.8.2.2.1 | 5 m uzunluğundaki otomobil ve 45 m uzunluğundaki kamyon düz yolda hareket ediyor; kamyon 24 m yol aldığında otomobilin aldığı yol (kesirli seçenekler). | C | low |
| 10 | — | — | — | B | unknown |
| 11 | Kareköklü İfadeler | M.8.1.3.4 | Uzunluğu 4√2 m olan K yolu ve 2√6 m olan L yolu; tam şarjlı oyuncak tren L'de 6 tam turda şarjı bitiriyor; K yolunda kaçıncı turda biteceği. | D | medium |
| 12 | Eşlik ve Benzerlik | M.8.3.3.2 | 12 cm × 16 cm dikdörtgen kâğıtta AD üzerinde E; [BE] ve [BD] çizilerek BAE ~ BCD benzer üçgenleri ve EBD üçgeni; EBD'nin çevresi (42/45/46/48). | A | high |
| 13 | Doğrusal Denklemler (eğim dahil) | M.8.2.2.6 | 260 cm çubuğun orta noktasına 120 cm'lik dik destek konarak yapılan tahterevalli; [AB]'nin son konumdaki eğiminin alamayacağı değer. | C | medium |
| 14 | — | — | Millî takımı desteklemek için hazırlanan afişin her satırına 'Bizim Çocuklar' yazılmış; seçenekler harf (Ç/u/o/z); kökün devamı okunamadı. | A | low |
| 15 | Doğrusal Denklemler (eğim dahil) | M.8.2.2.1 | Doğrusal yolda aynı anda birbirine doğru sabit süratle giden A ve B araçlarının C noktasında karşılaşması; A'nın başlangıçta C'ye uzaklığı (970/720/680/630). | D | medium |
| 16 | Üslü İfadeler | M.8.1.2.5 | Bir çiftçinin 1 m²'lik çerçeveyle başak sayarak buğday verimini tahmin etmesi bağlamlı soru. | A | low |
| 17 | Üçgenler (Pisagor dahil) | M.8.3.1.2 | Kenarı 8 cm olan eşkenar üçgen [AK] boyunca kesilerek kenar uzunlukları tam sayı olan iki üçgen elde ediliyor. | C | medium |
| 18 | Veri Analizi | M.8.4.1.2 | Tavuk çiftliğinde günlük yumurta üretiminin küçük/orta/büyük boylara göre dağılımı daire grafiğinde; ayrılan yumurtalarla en az kaç kolinin imha edileceği. | B | medium |
| 19 | Geometrik Cisimler | M.8.3.4.3 | Dik dairesel silindirlerden oluşan birleşik cismin toplam yüzey alanı (π = 3; 1296/1248/1200/1152). | C | medium |
| 20 | Üçgenler (Pisagor dahil) | M.8.3.1.2 | Uzunlukları tam sayı olan üç çubuğun (koşullara göre) alabileceği farklı toplam uzunluk sayısı (8/11/13/16). | B | low |

### Fen Bilimleri

**2024 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | DNA ve Genetik Kod | F.8.2.1.1 | Hücredeki kalıtım materyalini oluşturan yapılardan (DNA, gen, kromozom, organik baz) hangisinin modellerde doğru işaretlendiği. | B | medium |
| 2 | DNA ve Genetik Kod | F.8.2.2.2 | Bezelye bitkilerinde boy uzunluğu karakteriyle ilgili kalıtım sorusu (metin kesik). | D | medium |
| 3 | DNA ve Genetik Kod | F.8.2.5.1 | Bir memeli hayvanın (P) klonlanmasıyla ilgili soru (metin kesik). | D | medium |
| 4 | DNA ve Genetik Kod | F.8.2.3.1 | Kürk renginin melanin pigmentinin üretilmesine bağlı olduğu türde enzimi üretilemeyen mutasyon; verilen bilgilerle hangi işlemlerin/çıkarımların yapılabileceği (I-II-III). | A | high |
| 5 | Enerji Dönüşümleri ve Çevre Bilimi | F.8.6.1.1 | Kara ekosisteminde aynı besin zincirindeki K, L, M, N türlerinden M'deki biyolojik birikimin diğerlerinden az olması bilgisinden çıkarım. | B | medium |
| 6 | Enerji Dönüşümleri ve Çevre Bilimi | F.8.6.2.2 | Sarı ışıkla aydınlatılan bir su bitkisinde belirli sürede üretilen glikoz miktarıyla fotosentez hızının ölçüldüğü deney. | C | low |
| 7 | Enerji Dönüşümleri ve Çevre Bilimi | F.8.6.3.1 | Atmosferdeki azotun canlılar tarafından kullanılmasıyla ilgili soru (azot döngüsü). | D | medium |
| 8 | Enerji Dönüşümleri ve Çevre Bilimi | F.8.6.3.3 | Sera etkisinin artışına bağlı küresel ısınma ve iklim değişikliğinin olumsuz etkileri. | A | low |
| 9 | Mevsimler ve İklim | F.8.1.1.1 | Eş yükseltideki iki şehrin sıcaklık değerlerinden mevsim/yarım küre çıkarımı; I-II-III yargıları. | C | medium |
| 10 | Basınç | F.8.3.1.1 | Katı cisimlerin zemine uyguladığı basıncı etkileyen değişkenlerle ilgili deney/gözlem sorusu. | D | medium |
| 11 | Basınç | F.8.3.1.2 | Sıvı basıncıyla ilgili hipotezlerin test edilmesi. | B | medium |
| 12 | Basit Makineler | F.8.5.1.1 | Duvara bağlı bir tahta üzerinde yürüyen öğrenci düzeneği (tahtayı tutan ip/destek kuvveti ile ilgili olması muhtemel). | A | low |
| 13 | Basit Makineler | F.8.5.1.1 | Eşit bölmeli tahtanın tavana ve tahtaya bağlı makaralarla işçilerce yatay dengede tutulması; ip kuvvetinin tahtanın ağırlığıyla karşılaştırılması ('kesinlikle doğru' yargıları). | C | high |
| 14 | Elektrik Yükleri ve Elektrik Enerjisi | F.8.7.1.3 | İki aşamalı elektriklenme etkinliği (yük etkileşimi/elektriklenme çeşitleri). | A | medium |
| 15 | Elektrik Yükleri ve Elektrik Enerjisi | F.8.7.3.1 | Güneş paneli temizleme sistemi bağlamlı soru (enerji dönüşümü veya tasarım). | C | low |
| 16 | Madde ve Endüstri | F.8.4.1.1 | Periyodik tablodaki elementlerle ilgili soru (grup/periyot, metal-ametal-yarı metal). | D | medium |
| 17 | Madde ve Endüstri | F.8.4.3.1 | Kimyasal tepkime deneyiyle ilgili soru. | B | medium |
| 18 | Madde ve Endüstri | F.8.4.4.5 | Asit ve bazlarla yapılan bir deney; I-II-III yargılarından hangilerinin doğru olduğu. | A | medium |
| 19 | Madde ve Endüstri | F.8.4.5.1 | Bir maddenin sıcaklık değişimini etkileyen faktörlerle ilgili soru (ısı-sıcaklık). | B | medium |
| 20 | Madde ve Endüstri | F.8.4.5.3 | Saf bir katının 30 dakika ısıtıldığı K, L, M düzenekleri; ısınma/hal değişimi karşılaştırması. | C | medium |

**2025 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | DNA ve Genetik Kod | F.8.2.1.3 | Kendini eşlemeye başlayan DNA molekülünde eşlemenin tamamlandığı ve tamamlanmadığı bölgeler modelde gösteriliyor; yeni zincirlerin nükleotid dizilimiyle ilgili yargılar. | A | medium |
| 2 | DNA ve Genetik Kod | F.8.2.2.2 | Bezelyelerde tohum rengi karakterinin kalıtımı (tek karakter çaprazlaması). | C | medium |
| 3 | DNA ve Genetik Kod | F.8.2.2.2 | Soya fasulyesinde bakla tüy yoğunluğu ile ilgili soru (kalıtım/çevre etkisi bağlamı). | D | low |
| 4 | Enerji Dönüşümleri ve Çevre Bilimi | F.8.6.1.1 | Sucul bir ekosistemdeki besin ağı; öğrencinin bu besin ağından yararlanarak destekleyemeyeceği hipotez. | C | medium |
| 5 | Enerji Dönüşümleri ve Çevre Bilimi | F.8.6.2.2 | Oda sıcaklığında kapalı cam kapta bitkiyle fotosentez deneyi; 24 saat sonra CO₂ ve O₂ miktarları ile toplam biyokütle değişimine ilişkin I-II-III yargıları. | B | medium |
| 6 | Enerji Dönüşümleri ve Çevre Bilimi | F.8.6.3.1 | Azot döngüsü şeması (ayrıştırıcılar, baklagil köklerindeki azot bağlayıcı bakteriler); şemaya göre doğru ifade. | D | medium |
| 7 | Enerji Dönüşümleri ve Çevre Bilimi | F.8.6.3.3 | Bir bölgedeki kirlilik araştırması; 1970–2010 yılları arasında birim hacim havadaki karbondioksit miktarı grafiği (küresel iklim değişikliği). | A | medium |
| 8 | Basınç | F.8.3.1.2 | Sıvı yoğunluğunun sıvı basıncına etkisini test eden basınç ölçerli deney; seçeneklerde 2. düzeneğin sıvı cinsi, hacmi ve basınç ölçer konumu (değişken kontrolü). | D | medium |
| 9 | Basınç | F.8.3.1.1 | İçinden çubuk geçirilmiş sünger; çubuğa halkalar ve perde asılıyor; süngerde oluşan izler (katı basıncı). | B | medium |
| 10 | Mevsimler ve İklim | F.8.1.1.1 | Eş yükseltideki K ve L şehirlerinin uzun yıllar aylık ortalama sıcaklıkları tablosu; yarım küre/mevsim çıkarımı. | C | high |
| 11 | Basit Makineler | F.8.5.1.1 | Sürtünmesiz 1. ve 2. eğik düzlemde kutuların iplerle uygulanan en küçük kuvvetlerle sabit hızla çıkarılması; kuvvetlerin karşılaştırılması (önceki okumada çıkrık da geçiyordu). | C | medium |
| 12 | Basit Makineler | F.8.5.1.1 | Bir öğrencinin ağırlığı önemsenmeyen özdeş kasnaklarla kurduğu düzenek (kasnak/makara sistemi). | B | medium |
| 13 | Elektrik Yükleri ve Elektrik Enerjisi | F.8.7.1.1 | Elektriklenme ve elektriksel etkileşimlerden yararlanılarak kirli havanın temizlenmesi (elektrostatik filtre) bağlamı. | A | medium |
| 14 | Elektrik Yükleri ve Elektrik Enerjisi | F.8.7.1.2 | Elektriksel yük durumları bilinmeyen küçük ve hafif K, L, M plastik parçaların yüklü çubuklarla incelenmesi; yük etkileşimi yargıları. | D | medium |
| 15 | Elektrik Yükleri ve Elektrik Enerjisi | F.8.7.3.2 | Elektrik enerjisinin hareket, ısı ve ışık enerjisine dönüşümü; bir öğrencinin bu dönüşümleri gösteren modelleri. | A | medium |
| 16 | Madde ve Endüstri | F.8.4.1.2 | Periyodik sistemde elementlerin yerleşimi/sınıflandırılması (önceki okuma: grup numarası büyük olan yarı metal; grup no, periyot no, sınıf, atom no karşılaştırması). | C | medium |
| 17 | Madde ve Endüstri | F.8.4.2.1 | Boş deney tüpüne konan katı iyotun ısıtılıp soğutulması deneyi (süblimleşme–kırağılaşma; fiziksel/kimyasal değişim ayrımı). | B | medium |
| 18 | Madde ve Endüstri | F.8.4.4.3 | Metil oranj, fenolftalein ve timol mavisi ayraçlarının asit ve bazdaki renk tablosu; renksiz üç çözeltinin asit/baz olarak belirlenmesi. | C | medium |
| 19 | Madde ve Endüstri | F.8.4.5.1 | İki özdeş kaba sıcaklığı ve kütlesi belirtilen maddeler konarak yapılan ısı–sıcaklık deneyi (kökün yalnız başı okundu). | A | medium |
| 20 | Madde ve Endüstri | F.8.4.5.3 | Maddelerin hâl değişimiyle ilgili deney (ısınma/hâl değişimi). | D | low |

**2026 (B kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | Enerji Dönüşümleri ve Çevre Bilimi | F.8.6.1.1 | Bir ekosistemdeki canlılar arasındaki (beslenme) ilişkiler. | B | medium |
| 2 | Enerji Dönüşümleri ve Çevre Bilimi | F.8.6.3.1 | Doğadaki karbon döngüsü. | C | medium |
| 3 | Enerji Dönüşümleri ve Çevre Bilimi | F.8.6.2.2 | İpliksi alglerde ışık renginin fotosenteze etkisini inceleyen deney; yeşil ışıkla ilgili sonuç. | A | medium |
| 4 | DNA ve Genetik Kod | F.8.2.2.2 | Bezelyede çiçek rengi kalıtımıyla ilgili iki çaprazlama. | A | medium |
| 5 | Enerji Dönüşümleri ve Çevre Bilimi | F.8.6.4.1 | Kaynakların korunması ve enerji tasarrufu. | B | low |
| 6 | DNA ve Genetik Kod | F.8.2.1.1 | Nükleotidin yapı birimlerinin (şeker, fosfat, organik baz) sembollerle eşleştirilmesi; seçeneklerde fosfat, adenin, şeker, guanin. | D | medium |
| 7 | DNA ve Genetik Kod | F.8.2.3.2 | Hava ve su ortamındaki yaprakları farklı olan su bitkisi ve öğrencinin etiketli yaprak modeli (modifikasyon). | C | medium |
| 8 | Elektrik Yükleri ve Elektrik Enerjisi | F.8.7.2.2 | Yanıcı madde içeren veya elektrik yüklü ortamdaki metal kapların topraklanması gereken uygulamalar (I-II-III). | C | medium |
| 9 | Mevsimler ve İklim | F.8.1.1.1 | Dünya üzerinde eş yükseltideki P, R ve S şehirleri (mevsim/iklim çıkarımı; kök kesik). | D | medium |
| 10 | Elektrik Yükleri ve Elektrik Enerjisi | F.8.7.1.3 | Nötr iletken K ve L kürelerinin yüklü çubuklarla etki/dokunma yoluyla yüklenmesi. | A | low |
| 11 | Basınç | F.8.3.1.2 | Sıvı basıncıyla ilgili etkinlikte alt ve üst kısımları eşit bölmeli tel kafes ve balon (Şekil I); üç yargının değerlendirilmesi. | C | medium |
| 12 | Basit Makineler | F.8.5.1.1 | Çamura batan traktörü çıkarmak için ağırlığı önemsenmeyen ip ve özdeş halkalarla kurulan düzenek (makara/palanga benzeri kuvvet kazancı). | B | low |
| 13 | Basit Makineler | F.8.5.1.2 | Ağırlığı önemsenmeyen levha, tutma kolu ve tekerleklerle kutu taşıma aracı tasarımı (kaldıraç ilkesi). | A | medium |
| 14 | Elektrik Yükleri ve Elektrik Enerjisi | F.8.7.1.3 | Bir öğrencinin elektriksel yükü nötr olan iletken K ve L kürelerini yüklemek için yüklü çubuklarla yaptığı işlemler. | D | medium |
| 15 | Basınç | F.8.3.1.1 | Katı basıncı: küp biçimli K ve L cisimlerinin zemine uyguladığı basınç; seçenekler kuvvetin yönü ve büyüklüğü tablosu. | B | medium |
| 16 | Madde ve Endüstri | F.8.4.4.4 | Bitki özütünden hazırlanan ayracın çözeltilerde turuncu/sarı/kırmızı renk vermesine göre K, L, M çözeltilerinin pH karşılaştırması (seçenekler tablo). | C | medium |
| 17 | Madde ve Endüstri | F.8.4.5.1 | Sıcak su torbalarının verdiği ısı (maddenin cinsi/kütlesi/sıcaklık değişimi ile ısı ilişkisi). | A | medium |
| 18 | Madde ve Endüstri | F.8.4.2.1 | Mavi renkli çözeltiye konan çinko çubukta gözlenen değişim (kimyasal değişim/tepkime). | B | medium |
| 19 | Madde ve Endüstri | F.8.4.5.1 | İki kaptaki suyun ısıtıcıyla ısıtılması ve süreler; kütle, başlangıç sıcaklığı ve alınan ısı miktarıyla ilgili I–III yargıları. | B | medium |
| 20 | Madde ve Endüstri | F.8.4.5.2 | Özdeş iki cam kaptaki saf suların ısıtılmasıyla ilgili deney (19. soruyla örtüşüyor olabilir). | D | low |

### T.C. İnkılap Tarihi ve Atatürkçülük

**2024 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | — | — | — | A | unknown |
| 2 | Millî Bir Destan: Ya İstiklal Ya Ölüm! | İTA.8.3.1 | Londra Konferansı'na davet ve Kars-Ardahan-Artvin-Batum sınırlarıyla ilgili gelişmelerin durum-sonuç tablosu; yanlış eşleşme/ifade. | B | low |
| 3 | Millî Uyanış: Bağımsızlık Yolunda Atılan Adımlar | İTA.8.2.3 | Paris Barış Konferansı'nda bazı halkların yönetimi ve kaynaklarının 'gelişmiş' milletlere emanet edilmesi kararı; doğrudan ilişkili kavram (manda). | A | medium |
| 4 | Millî Uyanış: Bağımsızlık Yolunda Atılan Adımlar | İTA.8.2.2 | Birinci Dünya Savaşı sırasında Osmanlı topraklarının paylaşımına ilişkin gizli anlaşmalar (Rusya'nın paylaşım teklifi, İngiltere-Fransa ekonomik çıkarları); kök görülmedi. | D | low |
| 5 | Atatürkçülük ve Çağdaşlaşan Türkiye | İTA.8.4.9 | Atatürk inkılapçılığının sürekli yenilenmeyi öngördüğünü anlatan metin; dayandığı temel esaslar (millî birlik ve beraberlik, bağımsızlık ve özgürlük vb.). | C | medium |
| 6 | Millî Bir Destan: Ya İstiklal Ya Ölüm! | İTA.8.3.3 | Atatürk'ün, ülkenin elleri bağlıyken ordunun görevini yaptığını ve şimdi ilim ve irfan sahiplerinin vatanı hür ve mutlu kılmaya çağrıldığını söyleyen sözü; bu sözle anlatılmak istenen (eğitimin/ilmin yeni mücadele alanı olması). | D | medium |
| 7 | — | — | — | B | unknown |
| 8 | — | — | — | C | unknown |
| 9 | Millî Bir Destan: Ya İstiklal Ya Ölüm! | İTA.8.3.5 | Sakarya Zaferi'nden sonraki gelişmeler (düşman ordularının durumu) üzerine metin; kök görülmedi. | A | medium |
| 10 | Atatürkçülük ve Çağdaşlaşan Türkiye | İTA.8.4.1 | Laiklik ilkesi ve din-vicdan hürriyeti üzerine metin; kök görülmedi. | B | medium |

**2025 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | Atatürkçülük ve Çağdaşlaşan Türkiye | İTA.8.4.1 | Atatürk'ün gelişmiş dünya uygarlığına yetişme zorunluluğunu anlatan ('artık duramayız' anlamındaki) sözü; hangi ilkenin önemini vurguladığı (seçenekler: Halkçılık, Milliyetçilik, İnkılapçılık, Cumhuriyetçilik). | C | medium |
| 2 | Atatürkçülük ve Çağdaşlaşan Türkiye | İTA.8.4.9 | Atatürk'ün bir milletin başka bir milletin taklitçisi olamayacağını, ilerlemenin kendi öz kaynaklarından çıkarılması gerektiğini anlatan sözü; vurgulanan değer (seçenekler: Millîlik, Eşitlik, Özgürlük, Barışçılık). | A | medium |
| 3 | Bir Kahraman Doğuyor | İTA.8.1.1 | Balkan Savaşları: Birinci Balkan Savaşı'nın ardından Doğu Trakya'nın Bulgar egemenliğine girmesi ve Osmanlı'nın Balkan devletleri arasındaki anlaşmazlıktan yararlanması (Edirne'nin geri alınması); kök görülmedi. | D | low |
| 4 | Millî Uyanış: Bağımsızlık Yolunda Atılan Adımlar | İTA.8.2.2 | 'Türk Milletinin Varoluş Destanı: Çanakkale' başlıklı metin; kök görülmedi. | B | low |
| 5 | — | — | — | A | unknown |
| 6 | Millî Uyanış: Bağımsızlık Yolunda Atılan Adımlar | İTA.8.2.5 | Amasya Genelgesi'nden Erzurum ve Sivas kongrelerine uzanan süreci anlatan metin; Atatürk ilke ve inkılaplarını oluşturan temel esaslardan hangisinin vurgulandığı (bağımsızlık ve özgürlük; millî tarih bilinci vb.). | D | low |
| 7 | Millî Uyanış: Bağımsızlık Yolunda Atılan Adımlar | İTA.8.2.2 | Birinci Dünya Savaşı'nda Mustafa Kemal'in komuta ettiği Suriye-Filistin Cephesi ile ilgili metin; kök görülmedi. | C | low |
| 8 | Millî Bir Destan: Ya İstiklal Ya Ölüm! | İTA.8.3.2 | Sakarya Savaşı'nın kazanılmasının dış dünyadaki (siyasi/diplomatik) etkilerine ilişkin alıntı; kök görülmedi. | B | medium |
| 9 | Demokratikleşme Çabaları | İTA.8.5.1 | Atatürk dönemi demokratikleşme adımlarını gösteren tablo (kurulan partiler, mecliste temsil, çok partili hayat denemeleri, meclis hükümeti sistemi); 'bu tabloya göre hangisi söylenebilir'. | B | medium |
| 10 | Atatürk Dönemi Türk Dış Politikası | İTA.8.6.2 | Musul Sorunu, Milletler Cemiyeti süreci ve Irak'ın durumu; 'bu bilgilere göre hangisine ulaşılabilir' (diplomasiyle çözüm vb.). | D | medium |

**2026 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | Bir Kahraman Doğuyor | İTA.8.1.4 | İtalya'nın Trablusgarp harekâtı öncesinde büyük devletlerin tutumunu yokladığı ve Almanya ile İngiltere'nin karşı çıkmayacağını anladığı anlatılıyor; bu bilgiden ulaşılabilecek yargı soruluyor (seçenekler doğrulanamadı). | B | high |
| 2 | Millî Uyanış: Bağımsızlık Yolunda Atılan Adımlar | İTA.8.2.1 | Kâzım Karabekir'in, İttihat ve Terakki yönetiminin İngiltere ve Fransa'dan güvence alamayınca Almanya'ya yöneldiğini anlatan açıklaması; neden-sonuç ilişkisi. | D | medium |
| 3 | Millî Uyanış: Bağımsızlık Yolunda Atılan Adımlar | İTA.8.2.5 | Millî Mücadele hazırlık dönemi (Mustafa Kemal'in çalışmaları) – içerik ayrıntısı bulunamadı. | C | low |
| 4 | Millî Uyanış: Bağımsızlık Yolunda Atılan Adımlar | İTA.8.2.7 | TBMM'ye karşı ayaklanmalar ve alınan tedbirler (aday) – içerik ayrıntısı bulunamadı. | A | low |
| 5 | Millî Bir Destan: Ya İstiklal Ya Ölüm! | İTA.8.3.2 | Batı Cephesi: I. İnönü, II. İnönü, Kütahya-Eskişehir, Sakarya ve Büyük Taarruz muharebeleri / Mustafa Kemal'in Millî Mücadele cephelerine ilişkin değerlendirmesi. | C | low |
| 6 | Millî Bir Destan: Ya İstiklal Ya Ölüm! | İTA.8.3.7 | Kemal Tahir'in 'Esir Şehrin İnsanları' romanından kesit: Mondros sonrası işgal altındaki İstanbul; edebî metinden tarihî çıkarım. | A | low |
| 7 | Atatürkçülük ve Çağdaşlaşan Türkiye | İTA.8.4.6 | 3 Haziran 1933'te kurulan Sümerbank (fabrikalarda kreş, okul, sağlık hizmetleri) ile ilişkilendirilebilecek Atatürk ilkeleri. | B | medium |
| 8 | Atatürkçülük ve Çağdaşlaşan Türkiye | İTA.8.4.5 | Atatürk'ün aileye ilişkin sözleri; sözlerden ulaşılabilecek yargılar. | D | medium |
| 9 | Demokratikleşme Çabaları | İTA.8.5.1 | 12 Ağustos 1930'da Fethi Okyar başkanlığında kurulan Serbest Cumhuriyet Fırkası (program: laik cumhuriyete bağlılık, ekonomide liberalizm); bilgilere göre doğru yargı (ör. mecliste temsil). | B | medium |
| 10 | Atatürk Dönemi Türk Dış Politikası | İTA.8.6.1 | Lozan sonrası Atatürk döneminin barışçı dış politikası üzerine metin; kök görülmedi. | C | medium |

### Din Kültürü ve Ahlak Bilgisi

**2024 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | Hz. Muhammed'in Örnekliği | 8.4.4 | 'Sebat' kavramı (kararlılık, devamlılık, çaba) üzerine madde; kök görülmedi. | C | low |
| 2 | Zekât ve Sadaka | 8.2.5 | Maûn suresi: hesap gününü yalanlayanların tutumu ve yoksula yardım sorumluluğu; numaralı yargılardan hangilerine ulaşılabileceği (yalnız varlıklılara mı, her birey için mi, manevi yardımı da kapsar mı). | B | low |
| 3 | — | — | — | A | unknown |
| 4 | Zekât ve Sadaka | 8.2.4 | Peygamberler tablosu (ör. Medyen halkına gönderilen peygamber); Hz. Musa, Hz. Şuayb ve Hz. Yusuf'un I-II-III ile eşleştirilmesi. | B | low |
| 5 | Din ve Hayat | 8.3.1 | Camilerin yalnız ibadet yeri olmayıp kültür ve sosyalleşme mekânı olduğu. | C | high |
| 6 | Kader İnancı | 8.1.1 | Evrendeki yasaların nitelikleriyle ilgili numaralı ifadeler (zamana/mekâna göre değişir mi, gözlenebilir olgulara dayanır mı, genellenebilir mi). | C | medium |
| 7 | Din ve Hayat | 8.3.2 | İslam'a göre her çocuğun günahsız doğduğu bilgisinden insan haklarına (zarar veren davranışların yasaklanması, yaşama hakkı) ilişkin çıkarımlar. | B | medium |
| 8 | Hz. Muhammed'in Örnekliği | 8.4.4 | Hz. Muhammed'in Abdullah bin Ureykıt kılavuzluğunda Medine'ye hicreti; olaydan çıkarılamayacak özellik (cesaret-kararlılık, tedbirlilik, uzmandan yararlanma, merhamet). | D | medium |
| 9 | Kader İnancı | 8.1.1 | Hz. Peygamber'in oğlu İbrahim'in vefat ettiği gün gerçekleşen Güneş tutulması ve Peygamber'in iki olay arasında ilişki olmadığını açıklaması; asıl anlatılmak istenen (evrenin yasaları/tevhid). | B | medium |
| 10 | Kur'an-ı Kerim ve Özellikleri | 8.5.2 | Ahiret inancına değinen bir ayet; seçeneklerden biri hesap günü hakkında bilgi verdiği (Kur'an'ın ana konuları). | A | low |

**2025 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | Kader İnancı | 8.1.3 | Kendisine minnet beklentisi ve kibir sorulan bir hayırseverin kendini 'aşçının elindeki kepçe' gibi gördüğünü söylemesi (verilen rızkın asıl sahibi Allah'tır); kader-kaza kavramlarına ilişkin numaralı ifadeler (birinde kaza-kad… | C | medium |
| 2 | Kader İnancı | 8.1.3 | Kader ve kaza konulu ikinci madde (kök/seçenek ayrıştırılamadı). | D | low |
| 3 | Kader İnancı | 8.1.2 | Kur'an'a göre yeryüzünün insanın hizmetine sunulduğu ve insanın yeryüzündeki düzene uygun yaşaması gerektiği; seçeneklerde zorluklarla başa çıkma, huzur, sorumluluk. | B | low |
| 4 | Kader İnancı | 8.1.3 | Bir millî futbolcunun gol sevincinde elini kalbine koyup parmağıyla göğü işaret etmesi; çaba gösterip Allah'a güvenme (tevekkül). | B | medium |
| 5 | Zekât ve Sadaka | 8.2.2 | Zekât konulu madde (5 ve 6 zekât). | A | low |
| 6 | Zekât ve Sadaka | 8.2.2 | Zekâtla ilgili numaralı ifadeler (toprak ürünlerinde bir yıl şartı aranmaması, gelir getiren mal, temel ihtiyaç malları, bakmakla yükümlü olunan yakınlara zekât verilmemesi); hangilerinin doğru olduğu. | D | low |
| 7 | — | — | — | B | unknown |
| 8 | Hz. Muhammed'in Örnekliği | 8.4.3 | Hz. Peygamber'in hayatından numaralı olaylar (I: Kureyş'i Safa tepesine davet edip peygamberliğini duyurması; Taif halkıyla ilgili bir olay; namaza çağırma yöntemi için sahabenin görüşünü alması vb.); hangilerinin istişareye ve… | C | low |
| 9 | Kader İnancı | 8.1.1 | Allah'ın gece ile gündüzü, Güneş ile Ay'ı bir ölçü/hesapla düzenlediğini bildiren ayet; evrendeki düzen ve yasalar; kök görülmedi. | A | low |
| 10 | Hz. Muhammed'in Örnekliği | 8.4.8 | Hz. Peygamber'in en hayırlı insanın kim olduğunu soran birine verdiği cevap ve selamlaşmanın önemine ilişkin hadis; kök görülmedi. | A | low |

**2026 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | Hz. Muhammed'in Örnekliği | 8.4.7 | İmam Gazali'nin Hz. Muhammed'i örnek almasına ilişkin metin; vurgulanan husus (seçenekler: Kur'an'ın anlaşılması, Müslümanların birliği, İslam'ın temel kaynakları, Peygamber ahlakının benimsenmesi). | D | medium |
| 2 | Kader İnancı | 8.1.6 | Âyetü'l-Kürsî hakkında numaralanmış dört bilgi (Allah'ın birliği ve hâkimiyeti; hangi surede yer aldığı – Yusuf suresi çeldirici; vakit namazlarından sonra okunması vb.); hangilerinin doğru olduğu. | C | medium |
| 3 | Din ve Hayat | 8.3.2 | İslam'ın evliliği kadın ve erkeğin sevgi ve dayanışma içinde hayatlarını birleştirdiği bir kurum olarak görmesi; Kur'an'da eşlerin birbirine huzur kaynağı olması; kök görülmedi. | A | medium |
| 4 | Zekât ve Sadaka | 8.2.2 | Zekât verilebilecek yakınların doğru belirlendiği seçenek. | A | medium |
| 5 | Hz. Muhammed'in Örnekliği | 8.4.2 | Hz. Muhammed'in Mekke'nin fethinde Kureyşlilere tutumu (af), Enfâl 25. ayetten alıntı; numaralı yargılardan hangilerine ulaşılabileceği (Yalnız I / Yalnız II / I ve III / II ve III). | C | medium |
| 6 | — | — | — | B | unknown |
| 7 | Din ve Hayat | 8.3.1 | Abdestin arınmanın bir adımı olduğu, yalnız suyla temizlenmenin yetmediği; abdestin manevi arınma/erdemli davranış kazandırma yönü (seçenekler: beden temizliği, sağlıklı yaşam, namazın şartı, manevi arınma). | D | medium |
| 8 | Kur'an-ı Kerim ve Özellikleri | 8.5.1 | Hz. Peygamber'in davranışlarından hangisinin takrirî sünnet örneği olduğu (ör. kendisinin tercih etmediği bir yiyeceği yiyen sahabeye ses çıkarmaması). | C | medium |
| 9 | Zekât ve Sadaka | 8.2.2 | Peygamber'in temel ihtiyaç fazlası mallardan zekât alması üzerine metin; metinden ULAŞILAMAYACAK bilgi (seçenekler: bir yıl geçme şartı, âlimlerin katkısı, zekâtın sünnetle belirlenmesi, zekât malında şartlar). | A | medium |
| 10 | Zekât ve Sadaka | 8.2.3 | Hz. Peygamber'in nisap/altın değeri üzerinden bir düzen kurmasıyla öncelikle neyi amaçladığı (seçenekler: ekonomik denge, sosyal birlik ve adalet, Medine'yi dinin merkezi yapma, şehri dış tehditlere karşı koruma). | B | low |

### İngilizce

**2024 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | The Internet | E8.5.R1 | Sandra's and Mark's opinions about the internet (useful vs not); what Mark would say. | B | medium |
| 2 | Chores | E8.8.R1 | Jane talks about her responsibility at home; complete the blank (she likes being in the kitchen). | D | medium |
| 3 | Tourism | E8.7.R1 | Unclear; an option mentions that a tour takes place in summer. | A | low |
| 4 | — | — | Kübra's options for an English course (days, times, fees); which course she should choose. | D | low |
| 5 | On the Phone | E8.4.SI1 | Phone call between Max and a secretary with blanks; which option fits none of the blanks. | C | medium |
| 6 | Adventures | E8.6.R1 | Anthony will do an extreme sport on Sunday whose main equipment is a parachute; which sport. | B | medium |
| 7 | In the Kitchen | E8.3.SI1 | Four cooking-course students ask the teacher about making a cake; which cannot be the teacher's answer. | A | medium |
| 8 | Friendship | E8.1.L1 | Friends discuss a school party (one thinks City Park is not suitable); who talks about the party's location. | C | medium |
| 9 | Friendship | E8.1.R2 | Mr. White asks students to prepare an invitation card with place, time and type of event; which card includes all. | C | medium |
| 10 | Science | E8.9.SI2 | Matthew asks Emily about the most important invention of the last century (what, why, inventor); which cannot be Emily's answer. | D | medium |

**2025 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | Friendship | E8.1.R1 | Four people's opinions about their friends; who says something positive about their friend. | A | medium |
| 2 | Teen Life | E8.2.R1 | Clara buys books for friends (Robert, Lisa, Mary, Jack) according to their interests; which book will she NOT buy. | C | medium |
| 3 | Chores | E8.8.R1 | School-rules poster (keep the classroom tidy, be quiet while the teacher is talking, return library books); which option does NOT fit the blank. | D | medium |
| 4 | In the Kitchen | E8.3.R2 | Words grouped as cooking methods vs kitchen utensils; which two words should change places. | B | medium |
| 5 | On the Phone | E8.4.L2 | Four phone conversations (Mr Brown, Mr Jordan, Mr Logan, Mr Miller); who is definitely NOT available. | C | medium |
| 6 | Science | E8.9.R2 | Three short texts about Prof. Gazi Yaşargil (born 1925, Diyarbakır; family, education, achievements); which heading is NOT covered (hobbies). | A | high |
| 7 | Friendship | E8.1.R2 | Messages about invitations to Susan; who did NOT invite Susan to an event (options Carol, Jason, Liz, Mandy). | C | medium |
| 8 | Adventures | E8.6.R1 | Mike has written a new book about extreme sports; four online comments about it are given; stem not seen. | D | medium |
| 9 | Tourism | E8.7.R1 | Four short texts about places (Colosseum, Adrasan, Taj Mahal, Rize); which question is answered in all four texts (e.g., where it is). | D | high |
| 10 | Tourism | E8.7.R1 | A map/itinerary of a 'Cycling Tour – August 2025'; stem not seen (route/stop details). | B | low |

**2026 (A kitapçığı)**

| No | Ünite/blok | Kazanım | Soru özeti | Cevap | Güven |
|---|---|---|---|---|---|
| 1 | Friendship | E8.1.R1 | Miss June asks students to write a paragraph about their relationship with someone; which option paragraph mentions only positive things (shared hobbies, trust and respect, support). | D | medium |
| 2 | Teen Life | E8.2.R1 | Four teens describe weekend activities and likes/dislikes; who will join an activity they do not like. | C | medium |
| 3 | In the Kitchen | E8.3.R1 | Tina bakes a cake; friend Jessica's feedback on ingredients (likes apple and honey, too much lemon, add chocolate next time); stem not seen. | A | medium |
| 4 | On the Phone | E8.4.L2 | Three sentences from a phone call share one function; identify it (asking the caller to wait / hold on). | D | high |
| 5 | Tourism | E8.7.R1 | Three people's comments about a tour they joined; which statement is true according to the comments. | B | medium |
| 6 | Adventures | E8.6.R1 | Four friends describe free-time activities; which two are interested in extreme sports. | B | medium |
| 7 | Science | E8.9.R1 | Four short dialogue excerpts; which pair is doing an experiment right now (present continuous clues vs. past scientific discovery distractor). | D | high |
| 8 | Chores | E8.8.R1 | Lily hosts a birthday party; afterwards she vacuums, washes dishes, does laundry and takes out the rubbish; which picture shows a chore she did NOT do. | A | medium |
| 9 | Tourism | E8.7.R1 | Four people's opinions about Istanbul; who says something positive about the city. | C | medium |
| 10 | The Internet | E8.5.R2 | Table of four friends' video blogs (content, follower numbers); which statement is NOT correct. | B | medium |

