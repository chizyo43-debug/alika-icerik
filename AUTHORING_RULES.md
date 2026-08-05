# AliKa İçerik Üretim Sözleşmesi

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
| Çeldirici, aynı konudaki başka sorunun doğru cevabı | %15 altı | 41 |
| Gerekçe iskeleti yığılması | %20 altı | 37 |

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
