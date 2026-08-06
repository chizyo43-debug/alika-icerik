# AliKa İçerik Üretim Sözleşmesi

> **Sözleşme sürümü.** Yayımlanmış dört paket **2.0**'dır. Yeni üretim
> **Question Contract 2.2** ile yapılır: `hints` yoktur, hiyerarşi anahtarları
> (`unitKey` → `topicKey` → `subtopicKey` → `noteKey`) zorunludur, dolu her
> figür `altTextKey` taşır ve üretici kendi çıktısını `ai-verified`
> damgalayamaz. Ayrıntı §13.
>
> Kanonik şema **AliKa uygulama deposundadır**: `shared/question-2.2.schema.json`
> ve `shared/figure_spec.json`. Bu depoya kopyalanmaz — iki kopya, birinde
> güncellenip diğerinde unutulan bir sözleşme demektir. `tools/pack_validate.py`
> kuralları kendi kodunda uygular ve iki sürümü paketin `schemaVersion`
> alanına göre ayırır.

Bu belge **üretici modele** yöneliktir. Kuralları tanımlamaz — onlar
`SCHEMA_V2.md` ve `.claude/skills/alika-icerik/SKILL.md` içindedir. Burada
yalnız **bu depoda gerçekten yapılmış hatalar**, nedenleri ve tekrar etmemesi
için uyulacak üretim disiplini vardır.

Üretim yapmadan önce oku. Ürettikten sonra `python tools/pack_validate.py
--skor <paket>` ile kendini denetle.

---

## 0. Tek cümlelik özet

Bir soruyu oluşturan alanlar **birlikte doğrudur ya da birlikte yanlıştır**.
Hiçbirini tek başına düzenleme, hiçbirini tek başına "iyileştirme".

---

## 1. Atomiklik ilkesi (en önemli madde)

`choices`, `correct`, `distractorWhy`, `hints`, `explanation` **tek üretim
birimidir**. Biri değişiyorsa hepsi birlikte yeniden üretilir.

### Ne olmuştu

`d133631` commit'i "dolgu çeldiricileri temizle" göreviyle 31 sorunun
`choices` alanını değiştirdi, `distractorWhy`'a dokunmadı:

```jsonc
// tr.g05.mat.5-3-1.q001 — BOZUK HÂL
"choices": ["şablon", "hesap makinesi ve gönye", "kalemtraş", "cetvel ve pergel"],
"distractorWhy": [
  "Açıölçer açı ölçer; eş uzaklıktaki yayları oluşturamaz.",   // ← şık artık "şablon"
  "Hesap makinesi geometrik çizgi çizmez; orta nokta için ...",
  "Silgi çizim aracı değildir ve uzunluk aktaramaz.",          // ← şık artık "kalemtraş"
  "doğru"
]
```

Çocuk "şablon"u seçiyor, ekranda "Açıölçer açı ölçer" yazıyor. 21 soruda
30 gerekçe bu durumdaydı.

Aynı commit 5 kesir sorusunda çeldiricileri eş anlamlılarla değiştirdi.
Kutuya yazılınca ortaya çıkan cümleler:

```
2/3 daha düşüktür 3/5      ← eski: "küçüktür" (geçerli ve teşhis edici)
5/8 daha hafiftir  7/12    ← kesirde ağırlık yok
3/4 daha dardır    2/3     ← kesirde genişlik yok
```

### Kural

- Bir alanı düzeltmek için diğerlerini okumadan dokunma.
- Bir metriği düşürmek için kelime değiştirme; sorunun **tamamını** yeniden üret.
- CI'daki `tools/check_paired_edit.py` bunu PR'da durdurur. Denetimi susturmak
  için `--revert-of` kullanma; o yalnız bilinen tutarlı bir hâle **birebir**
  dönüşü doğrular.

---

## 2. Metrik avcılığı yasağı

Bir ölçütü sayısal olarak iyileştirip içeriği kötüleştirmek ihlaldir.
Bu depoda iki kez oldu.

**Örnek 1 — kozmetik çeşitlendirme.** İngilizce v2'de `difficultyReason`
benzersizliği 185/500'den 512/518'e çıktı. Sayı üçe katlandı ama üretilen şey
soru kökünün gerekçenin içine yapıştırılmasıydı:

```
"Öğrencinin “<soru kökü aynen>” görevi için <kökten kopyalanan 3 sözcük>
 kanıtlarını kullanarak seçenekleri karşılaştırmasını gerektirir."
```

Tırnaklı alan ve kökten kopyalanan sözcükler maskelenince geriye 193 iskelet
kalıyordu, 512 değil. Doğrulayıcının kural 37'si artık tam olarak bunu ölçer:
**imza yığılması**, ham benzersizlik değil.

**Örnek 2 — dolgu değişimi.** `d133631`'de 105 dolgu çeldiriciden yalnız 2'si
gerçekten kalktı; `yalnız açıölçer` yerine `makas`, `yalnız silgi` yerine
`kalemtraş` geldi. Dolgu sayısı 105 → 103. Buna karşılık şık↔gerekçe
uyumsuzluğu 380 → 409 **kötüleşti**.

### Kural

Bir düzeltmenin kabul ölçütü tek bir sayı değildir. Şunları birlikte göster:
skor tablosu, `check_paired_edit` çıktısı ve `tools/review_sample.py` ile
alınan %5 örneklemin insan okuması.

---

## 3. Çeldirici üretim reçetesi

Her yanlış şık **adlandırılmış bir kavram yanılgısına** karşılık gelir ve
`distractorWhy` o yanılgıyı söyler.

**İyi (matematik paketinden, gerçek):**

```
"Toplama yapmış: 90 + 27 = 117."
"Paydaya tüm toplar yerine yalnız mavi topları yazmış."
"Son 14 ekleme adımını atlamış: 14 × 2 = 28."
"Dik açı yerine doğru açıdan çıkarmış: 180 − 27 = 153."
```

**Kötü (İngilizce v1'den, gerçek):**

```
"“a rubber” seçeneği, soru kökündeki anlamla veya sınıf eşyaları ve proje
 malzemeleri yapısıyla uyuşmadığı için yanlıştır."
```

İkincisi 2000 metnin 791'inde aynen geçiyordu. Öğrenci neden yanıldığını
öğrenmiyor.

### Sayısal kısıtlar

| Kısıt | Eşik | Kural |
|---|---|---|
| Bir şık pakette ≥4 kez geçip hiçbir soruda doğru olmamalı | 0 örnek | 39 |
| Aynı 4'lü seçenek kümesi birden çok soruda | %5 altı | 39 |
| Çeldirici, **başka bir kazanımdaki** sorunun doğru cevabı | %15 altı | 41 |
| Gerekçe iskeleti yığılması | %20 altı | 37 |

**Kural 41 aynı kazanım içindeki paylaşımı kusur saymaz.** Bu bilerek böyle:
sıklık zarfları (`always/usually/often/sometimes/rarely/never`) ya da bir
ünitenin giysi sözcükleri **kapalı bir kümedir**. Altı zarfı ölçen altı soruda
her çeldirici zorunlu olarak başka bir sorunun cevabıdır; kümenin dışına
çıkmak soruyu kolaylaştırır. Ölçtüğün şeyi bozarak metrik düşürme.

Ölçüt **kazanım dışından ödünç** almadır: bir çarpma sorusunun çeldiricisi
bir alan sorusunun cevabıysa öğrenci konuyu değil paketi öğrenir.

**Neden önemli:** `There is/are` ailesinde çeldiriciler `There am` ve `It are`
idi. İkisi de hiçbir soruda doğru değildi; öğrenci kalıbı görünce eliyor,
gerçek seçim `is`/`are` arasına iniyor. Şans %25 değil %50 oluyor —
ölçme geçersizleşiyor.

---

## 4. Soru kalıbı çeşitliliği

Aynı gövde imzası (sayılar ve özel adlar maskelenmiş hâli) pakette **%10'u**
aşmamalı; genel çeşitlilik **%60'ın** altına düşmemeli (kural 40).

Matematikte 500 sorunun arkasında 166 kalıp vardı: 25 soru "### ### ###
doğal sayısının doğru okunuşu hangisidir?", 21 soru "# + # × # işleminin
sonucu kaçtır?". Öğrenci ikinci sorudan sonra kalıbı ezberliyor.

Aynı kazanımı ölçerken temsili değiştir: sözel problem, model/şekil, tablo
okuma, ters yönde sorma (cevaptan soruya), hata bulma.

---

## 5. İpucu merdiveni

`hints` **tam 5 dolu basamak**. İlk dördü doğru şıkkın metnini vermez
(kural 18, HATA). Beşinci basamak tam çözüm verebilir — bu şartname gereği
serbesttir.

Ama 5. basamak tek cümleye yığılmamalı: kural 38, 4. veya 5. ipucunun
paketin %70'inde aynı olmasını uyarı sayar. İngilizce'de 511/518 farklı,
Türkçe'de 25/500 — ikincisi sınırda.

**Not:** Fen ve Türkçe'de 5. ipucunun cevabı vermesi bir kural ihlali
değildi; erken kalite raporlarında öyle sayılmıştı. Ölçüm yaparken
şartnamenin ne dediğini kontrol et, kendi beklentini kural sanma.

---

## 6. Şekil

Görsel gerektiren kazanımlarda soruların en az %30'unda `figure` olmalı
(kural 42). Bugün matematik geometri (13 kazanım) ve fen (18 kazanım)
tamamen metinden — 2.018 sorunun yalnız 5'inde şekil var.

Şekil kataloğu ve SVG beyaz listesi tek kaynaktan gelir:
`shared/figure_spec.json` (ana AliKa deposu) ve `tools/pack_validate.py`
içindeki `KATALOG`. Üçüncü bir tanım açma. İzinli `kind`:

```
numberline · fraction · shape · angle · grid · coordinate · chart · table · flow · circuit
```

### 6.1 Figür de atomik üretilir

`figure` ile soru kökündeki **şekle atıf** aynı üretim biriminin parçasıdır
(§1'in şekil hâli). A4 birinci partide 49 figür eklendi, köke dokunulmadı;
doğrulayıcı 49 uyarı verdi: *"figure dolu ama metin ondan bahsetmiyor"*.
Metnin anmadığı figür süstür — çocuk ona bakmayı bilmez.

### 6.2 Figür kökte yazılı olanı gösterir, fazlasını değil

Metinde bulunmayan bir bilgiyi — özellikle **aranan değeri** — figüre koymak
soruyu çözer. Ölçme biter, resim bakma başlar.

Belirsizse üretme, atla:

- Kökte iki derece geçiyorsa hangisinin çizildiği belli değildir.
- İki dikdörtgen karşılaştırılıyorsa tek ızgara yanıltır.

A4'te bu iki durum atlandığı için 5-3-3'te 21 sorunun 13'ü figür aldı; kalan
8'i elle üretilecek. Eksik kapsama, yanlış figürden iyidir.

---

## 7. Kazanım dengesi

Kazanım başına soru sayısı, en çok ile en az arasında **6 kattan** fazla
açılmamalı (kural 45). Türkçe'de `T.O.5.5.` 83 soru alırken üç kazanım 1'er
soru alıyor; oran 83.

---

## 8. Kaynak ve izlenebilirlik

`objectiveSource` gezinilebilir bir açılış sayfası değil, **belge çapası**
olmalı — program PDF'i veya sayfa/bölüm çapası (kural 43).

- İyi: `https://tymm.meb.gov.tr/upload/program/2024programmat5678Onayli.pdf`
- Kötü: `https://tymm.meb.gov.tr/ogretim-programlari/ders/ingilizce-dersi-temel-egitim`

Kazanım kodunu uydurma. Kod ile program sürümü tutarlı olmalı: paket
`MEB-TYMM-2024` diyorsa kodlar 2024 programının kodları olmalı. Türkçe pakette
kodlar eski biçimde (`T.O.5.5.`) — bu eşleme **insan tarafından** program
belgesinden çıkarılır, tahmin edilmez.

---

## 9. Üretim sonrası öz denetim

```bash
python tools/pack_validate.py <paket.jsonl>
```

```bash
python tools/pack_validate.py --skor turkiye/5-sinif --json reports/quality_score.json
```

Kural numarası → ne yapılacağı:

| Kural | Seviye | Düzeltme |
|---|---|---|
| 12, 13 | HATA | Şık tekrarı/aynı sayı — şıkları yeniden üret |
| 15 | HATA | Aritmetik tutmuyor — anahtarı ve açıklamayı birlikte düzelt |
| 17, 18 | HATA | 5 dolu ipucu; ilk dördü cevabı vermez |
| 19 | HATA | `distractorWhy` uzunluğu = şık sayısı; doğru indekste "doğru" |
| 32, 37 | HATA | `difficultyReason` kısa veya tek iskelete yığılmış |
| 39 | UYARI | Dolgu çeldirici / tekrarlı seçenek kümesi |
| 40 | UYARI | Soru kalıbı yığılması veya düşük çeşitlilik |
| 41 | UYARI | Çeldirici geri dönüşümü |
| 42 | UYARI | Görsel gerektiren kazanımda şekil yok |
| 43 | UYARI | `objectiveSource` belge çapası değil |
| 45 | UYARI | Kazanım yükü dengesiz |

`tests/quality_baseline.json` bilinen borcu tutar. **HATA her zaman 0
olmalıdır.** UYARI sayısı ve skor bu tabandan kötüleşemez; bir kusur
düzeltildiğinde taban aşağı çekilir, asla yukarı.

Tabanın tek istisnası, içeriği doğru yapan bir onarımın metriği düşürmesidir
(A1'de matematik 72.76 → 72.39). Böyle bir durumda gerekçesi taban dosyasına
yazılır.

İkinci ve daha ince istisna: **ölçüm düzeltmesi**. Kural 41 kazanım üzerinden
ölçülmeye başlayınca matematik 80.77 → 79.63'e, uyarı 3 → 4'e çıktı. İçerik
kötüleşmedi; düzeltilmiş ölçüt onun zaten var olan kusurunu maskelemeyi
bıraktı. Burada doğru davranış tabanı yukarı çekip **neden** yazmaktır.
Yanlış davranış kuralı gevşetip tabanı korumaktır — ölçüyü küçültmek borcu
kapatmaz.

---

## 10. Çalışılmayan yollar

- Metni ASCII'ye çevirme. Türkçe karakter zorunlu (`ş ğ ı ö ü ç İ`).
- LaTeX. Kesir `3/8`, üs Unicode (`m²`).
- Serbest HTML veya çalıştırılabilir kod.
- "Yukarıdaki metne göre" deyip metni gövdeye gömmemek. Bağlam soruyla
  birlikte gelir (İngilizce `q197`–`q203` bu hatayı yapmıştı).
- Müfredat içeriğini soran soru. Ölçülen şey derstir, program belgesi değil
  (İngilizce `q489`: *"Which group belongs to the curriculum content for…"*).
- Anlamsız doğru cevap. İngilizce `q203`'ün anahtarı
  *"he is playing golf with a guitar"* idi.

---

## 11. Yeniden üretimde yakalanan hata sınıfları (A3/A4)

251 matematik sorusu sekiz partide yeniden üretildi. Aşağıdakilerin **hepsi
üretici modelin kendi yeni çıktısında** çıktı, eski içerikte değil. Yani bu
kusurlar §1–§10'u okumakla kapanmıyor; ayrıca aranmaları gerekiyor.

Doğrulayıcı bunların çoğunu yakalar, ama **yazmadan önce** aranmalı: bir parti
uygulanıp geri alınmaktansa üretim sırasında durdurulmalı.

### 11.1 Çeldirici doğru cevaba çarpıyor

En sık hata. Beş ayrı partide çıktı:

```
5 × ((18 − 6) ÷ 4)        → "önce çarp" sapması da 15 veriyordu
11, 19, □, 35, 43         → aritmetik ortalama 27 = aranan terim
sıklıklar 6, 4, 7, 3      → iki farklı okuma yanılgısı aynı sayıya çıkıyor
çevresi 56 cm             → kısa kenar sapması doğru çevreyi üretiyordu
```

Çeldiriciyi **hesaplayarak** üret, yazarak değil; sonra dört değerin
gerçekten farklı olduğunu doğrula. Sapma ifadesi ile doğru ifade farklı
olduğu hâlde sonuçları eşit çıkabilir — bu gözle görülmez.

### 11.2 Uydurulmuş sapma ifadesi

`7 × 8 − 20 ÷ 20` sorusunda bir çeldiricinin gerekçesi şu ifadeye
dayandırılmıştı:

```
7 * (8 - 20 // 20) * 0 + 7 * 8
```

Böyle bir öğrenci yanılgısı yok. Bu ifade, **istenen sayıyı üretmek için
geriye doğru** kurulmuştu. Gerekçe makine tarafından doğrulanabilir olsun
diye ifadeyi sayıya uydurmak, gerekçeyi doğru değil yalnız tutarlı yapar.

Doğrusu: önce yanılgıyı adlandır (*"bölmeyi çarpmadan önce yapmış"*), sonra
o yanılgının ifadesini yaz, çıkan sayıyı çeldirici yap. Sayı önce
seçilirse ifade uydurulur. Bu soru tamamen değiştirildi (`84 ÷ 7 − 5`).

### 11.3 Sorunun kendisi aritmetik olarak imkânsız

> Çevresi 44 cm olan dikdörtgende uzun kenar kısa kenarın 4 katıdır.

Yarı çevre 22, kısa kenar 22/5 — tam sayı değil. Üstelik buna
uydurma bir açıklama yazılmıştı. Kök sayıları **çözülerek** doğrulanmalı;
"makul görünüyor" yetmez. (Çevre 60 yapıldı.)

### 11.4 Negatif ya da anlamsız çeldirici

`45 ÷ 9 + 7 × 3 − 8` sorusunda bir sapma negatif sayı üretiyordu. 5. sınıf
öğrencisi negatif sayıyı bilmez; şıkkı görünce eler, ölçme bozulur (§3'teki
`There am` ile aynı kusur). Sapma **inanılır** olmalı.

### 11.5 Farklı gösterim, aynı değer (kural 13)

```
9/20  ile  0,45      → aynı sayı, ikisi de doğru
0,07  ile  7/100     → aynı sayı
```

Kesir ile ondalık aynı soruda şık olarak bulunuyorsa eşitlik elle kontrol
edilmeli. Çözüm ya değeri değiştirmek (`9/25`) ya da şıkları cümleye
çevirmektir.

### 11.6 Tahmin sorusunda kökün kendisi hesaplanabiliyor (kural 15)

> **4.812 + 3.196** işleminin sonucu yaklaşık kaçtır?

Doğrulayıcı kökteki ifadeyi **tam** hesaplar, 8.008 bulur, yuvarlanmış
anahtarla çelişir. Tahmin sorusunda işlemi sembolle yazma:
*"4.812 ile 3.196 sayılarının toplamı yaklaşık kaçtır?"*

### 11.7 Konuma bağlı açıklama

Bir açıklama *"dördüncü yorum"* diyordu. Şıklar döndürülünce dördüncü yorum
başka bir şey oldu. `explanation` ve `distractorWhy` **şıkkın metnine**
atıf yapar, sırasına değil.

### 11.8 Doğru cevap konumu dağılmıyor

İkinci partide doğru cevap dağılımı **2 / 9 / 7 / 3** çıktı. Model
"doğruyu ikinci sıraya koy" eğilimi taşıyor; öğrenci bunu fark eder.

Çözüm, üretimden sonra belirlenimci döndürme (`_dondur`) — ve döndürme
`choices` ile `distractorWhy`'a **aynı anda** uygulanır, yoksa §1'deki
d133631 hatası yeniden üretilir. İşlem `assert` ile korunmalı.

### 11.9 Kalıp tekrarını "yeni soru" sanma

`MAT.5.5.2`'de q003 / q008 / q013 / q018 tek soruydu; yalnız kök cümlesi
dört kez yeniden yazılmıştı. Aynı dört çeldiricinin pakette dolaşmasının
(kural 39) sebebi buydu. Kalıp sayarken **ölçülen yanılgıyı** say, cümleyi
değil.

Aynı ailede `noteId` atamaları notlar arasında mekanik olarak dönüyordu:
soru bir konuyu ölçerken bambaşka konudaki nota bağlanıyordu. `noteId`
içerikten gelir, sıradan değil.

### 11.10 Türkçe metin işlerken

- `.lower()` Türkçe için **yanlıştır**: `I → ı`, `İ → i` elle yapılır.
  Soru köküne önek eklerken ilk harf küçültülüyorsa bu tuzağa düşülür.
- `.` binlik, `,` ondalık ayracıdır. Doğrulayıcıda bu yüzden gerçek bir hata
  vardı: `4.812` ondalık 4,812 sanılıyordu. Binlik noktaları ondalık
  virgülden **önce** atılmalı; sonra atılırsa `1,234 → 1.234` üç basamaklı
  binlik grubuna benzeyip yanlışlıkla silinir.

### 11.11 Metrik avcılığı yine denendi

Yeni üretilen içerikte `karşılaştırılamaz` dört kez çeldirici olarak geçti
ve kural 39'a takıldı. Aynı anlamı farklı sözcüklerle yazmak uyarıyı
susturacaktı — §2 gereği yapılmadı; yerine gerçek yanılgı ifade eden
çeldiriciler kondu (*"1 sayısı asal olduğu için ikisi eşittir"*).

**Bir uyarıyı susturmak için kelime değiştirmek her zaman ihlaldir**, kusuru
üreten sen olsan bile.

---

## 12. Parti uygulanmadan önce çalıştırılacak ön denetim

Doğrulayıcı paketin tamamını denetler; bu liste **yazmadan önce** parti
içinde koşar. §11'in her maddesi buradaki bir satıra karşılık gelir.

| # | Denetim | Yakaladığı |
|---|---|---|
| 1 | `len(set(dört değer)) == 4` | 11.1 |
| 2 | Her çeldirici bir ifadeden **hesaplanmış** mı | 11.2 |
| 3 | Kök sayıları çözülüp tam sonuç veriyor mu | 11.3 |
| 4 | Hiçbir şık negatif / sınıf düzeyi dışı değil | 11.4 |
| 5 | Kesir ↔ ondalık eşitliği yok | 11.5 |
| 6 | Tahmin sorusunda kökte açık işlem yok | 11.6 |
| 7 | Gerekçe/açıklama sıra sözcüğü içermiyor | 11.7 |
| 8 | Doğru cevap konumları dengeli döndürülmüş | 11.8 |
| 9 | `len(distractorWhy) == len(choices)`, `"doğru"` doğru indekste | §1 |
| 10 | İlk dört ipucu doğru şıkkın metnini içermiyor | §5 |
| 11 | Ölçülen yanılgılar parti içinde benzersiz | 11.9 |
| 12 | `noteId` sorunun konusuyla uyuşuyor | 11.9 |

Bu denetimlerin **hepsi** A3 partilerinde en az bir gerçek kusur yakaladı.
Hiçbiri süs değil.

---

## 13. Question Contract 2.2

2.0 paketleri olduğu gibi geçerlidir; doğrulayıcı iki sürümü paketin
`schemaVersion` alanına göre ayırır. Yeni ve onarılan paketler 2.2'dir.

### Neyi değiştirdi

| Konu | 2.0 | 2.2 |
|---|---|---|
| `hints` | tam 5 dolu basamak (kural 17, HATA) | **alan yok** (kural 56, HATA) |
| Hiyerarşi | `topic` + `objective` | `unitKey`→`topicKey`→`subtopicKey`→`noteKey` (47) |
| Aile | yok | `familyId` zorunlu, ≥80 aile, ≤8 soru (49, 50) |
| Figür alt metni | yok | dolu figürde `altTextKey` zorunlu (kural 4) |
| Damga | `reviewStatus` serbest | üretici kendini damgalayamaz (54) |
| Kabul hedefi | rapor metninde | `pack.contractPolicy` içinde, ölçülenle karşılaştırılır (52, 53) |

`hints` **boş dizi olarak bile** yazılmaz. Boş dizi "bu alan var, doldurulmayı
bekliyor" der; 2.2'de alan yoktur.

### İki sürüm neden tek dosyada

`hints` kuralları birbirini iptal ediyor: 2.0 beş ipucu yoksa HATA verir,
2.2 ipucu **varsa** HATA verir. Sürüm kapısı kırılırsa yayımlanmış dört paket
sessizce 500'er HATA üretir. `tests/test_contract_22.py` bunu bekçiliyor —
kapıyı test etmeden kurala dokunma.

### Skor: S1 yer değiştirir

2.2'de ipucu olmadığı için "ilk dört ipucunda sızıntı yok" ölçütü her zaman
1.0 döner ve skoru sahte biçimde şişirirdi. Aynı ağırlık (0.20) **gerekçe
özgüllüğüne** verilir: jenerik olmayan `distractorWhy` oranı. Sözleşmenin asıl
derdi zaten budur.

### Kaynağı bilinmeyen kazanım

`objectiveSource` uydurulmaz. Bilinmiyorsa üçü birlikte `PENDING` olur ve
`pack.publishBlocked: true` yazılır (kural 55). Yarısı dolu bir kaynak,
uydurulmuş kaynaktan daha tehlikelidir: doğrulanmış görünür.

Türkçe paketinde kazanım kodları 2019 biçimindedir (`T.O.5.5.`) ama paket
`MEB-TYMM-2024` diyor. Bu eşleme program belgesinden **insan eliyle** çıkarılır;
o zamana kadar paket teknik olarak tam, yayına kapalıdır.
