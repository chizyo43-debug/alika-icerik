# LGS 2027 Tahmin Bankası: Üretim Talimatı

Bu klasör, LGS 2024–2026 analizinden türetilen 2027 tahmin bankasının üretim
girdilerini içerir. Bu talimat, bankayı üretecek yerel ajan içindir.

## 1. Dosyalar

| Dosya | Görevi |
|---|---|
| `authoring/lgs-2027/lgs-2027-tahmin-plani.json` | Üretim kotaları; kotalar için tek doğruluk kaynağı. |
| `authoring/lgs-2027/lgs-2024-2026-soru-envanteri.json` | 270 LGS sorusunun özeti, kazanımı, biçimi ve cevabı. Yalnızca tarz referansıdır. |
| `reports/LGS_2024_2026_SORU_ANALIZI.md` | Analiz raporu. Özellikle §4 (ders bazında soru türleri), §5 (güncel veriyle karşılaştırma) ve §6 (yazım ilkeleri). |
| `curriculum/tr-grade8-current-2018-2019.json` | 8. sınıf kazanım kodları ve başlıkları (MEB-CURRENT-2018-2019). |
| `tools/build_lgs_2027_plan.py`, `tests/test_lgs_2027_plan.py` | Planı envanterden yeniden üretir ve doğrular. |

Paketi depo köküne açarken `curriculum/` dosyasının yerel sürümünüzün üzerine
yazmadığından emin olun. Aynı dosya depoda zaten var; özeti `MANIFEST.sha256`
içindedir.

## 2. Ne üretilecek

- **Hacim ve dağılım:** 2.000 özgün soru (varsayılan). Türkçe 445, Matematik 445, Fen Bilimleri 444; İnkılap, Din ve İngilizce 222'şer soru.
- **Soru yapısı:** Her soruda 4 seçenek ve tek doğru cevap bulunur. Her soru MEB-CURRENT-2018-2019 kazanım kodu ve 1–5 zorluk seviyesi taşır.
- **Biçim:** Deponuzdaki güncel 8. sınıf paketleriyle aynı: Question Contract 2.2, `AUTHORING_RULES.md`, `SCHEMA_V2.md`.
  - Güncel matematik örneğindeki alanlar korunur: `familyId`, `unitKey`, `topicKey`, `subtopicKey`, `noteId`, `objective`, `level`, `difficultyReason`, `choices`, `correct`, `distractorWhy`, `explanation`, `figure`, `tags`, `taskId`, `distractorKeys`, `lessonAnchor`.
- **Önerilen paketleme:**
  - Ders başına bir LGS paketi (ör. `tr.g08.lgs2027.matematik`).
  - İsteğe bağlı olarak 90 soruluk deneme formları (§7).

## 3. Planı okuma

`subjects.<Ders>` altında şu alanlar var:

| Alan | Anlamı |
|---|---|
| `bankQuota` | Dersin banka kotası |
| `units[].predictedPerExam` | 2027 sınav formunda bu üniteden beklenen soru sayısı |
| `units[].bankQuota` | Ünitenin banka kotası |
| `units[].kazanimlar[].bankQuota` | Bu kazanımdan üretilecek soru sayısı |
| `units[].kazanimlar[].levelSplit` | Bu kazanımın 1–5 seviye dağılımı; toplamları dersin `difficultyMix` kotasını verir |
| `units[].kazanimlar[].taskId` | Matematik: güncel verideki görev (M8-T01…T28) |
| `units[].kazanimlar[].testability` | `none` ise soru üretilmez (kota 0) |
| `taskQuotas` | Matematik: görev başına toplam kota |
| `itemTypeMix` | Ders genelinde soru tipi kotaları (§4'teki uygunluk tablosuna göre dağıtın) |
| `styleRules`, `avoid` | Uyulacak üslup kuralları ve kaçınılacaklar |
| `targetMeanP` | Hedef ortalama doğru oranı |

Seviye tanımı (öneri):

| Seviye | Beklenen doğru oranı | Tanım |
|---|---|---|
| 1 | > %80 | Tek adım, doğrudan bilgi ya da işlem |
| 2 | %60–80 | Tek kazanım, kısa bağlam |
| 3 | %40–60 | Bağlam + iki adım ya da görsel/tablo yorumu |
| 4 | %25–40 | Uzun bağlam, çok adım, yakın çeldiriciler |
| 5 | < %25 | Çok kazanımlı seçici soru ya da yeni kural/durum uygulaması |

## 4. Soru tipi ile ünite uygunluğu

`itemTypeMix` ders geneli içindir. Tipleri ünitelere aşağıdaki uygunluğa göre dağıtın.

**Türkçe**

| Blok | Uygun tipler |
|---|---|
| Paragraf | `uzun-paragraf-edebi-bilgilendirici`, `kural-aciklama-verip-uygulama`, `ortak-metinli-ikili-soru` |
| Sözel mantık / görsel | `gorsel-grafik-tablo-sema`, `kural-aciklama-verip-uygulama` |
| Sözcük ve cümle anlamı | `kisa-cumle-sozcuk-anlami`, `numarali-cumle-parca` |
| Dil bilgisi, yazım, noktalama | `numarali-cumle-parca`, `ortak-metinli-ikili-soru` |
| Söz sanatları | `kisa-cumle-sozcuk-anlami` (dizeler), `uzun-paragraf-edebi-bilgilendirici` |

**Matematik**
- Bütün tipler bütün ünitelere uyar.
- `tablo-grafik-koordinat` özellikle Veri Analizi, Doğrusal Denklemler, Eşitsizlikler ve Olasılık için.
- `cok-kazanimli-secici` için örnek eşleşmeler: eğim + Pisagor, silindir + denklem, benzerlik + Pisagor, EBOB-EKOK + eşitsizlik, daire grafiği + bölünebilme.

**Fen Bilimleri**

| Tip | Uygun üniteler |
|---|---|
| `deney-duzenegi-degisken` | Basınç; Madde ve Endüstri (ısı, hâl değişimi, asit-baz); Enerji Dönüşümleri (fotosentez); Elektrik; Mevsimler (veri) |
| `model-sema-dongu` | DNA (model, eşlenme); Enerji (madde döngüleri, besin ağı); Madde ve Endüstri (periyodik tablo) |
| `caprazlama-problemi` | DNA ve Genetik Kod (F.8.2.2.2, F.8.2.2.3) |
| `duzenek-mekanizma` | Basit Makineler, Basınç |
| `tablo-grafik-yorumlama` | Mevsimler; Madde ve Endüstri (pH, ısınma grafiği); Enerji (CO₂ ve iklim verisi) |
| `gunluk-yasam-teknoloji-oncullu` | Elektrik (topraklama, santraller); Enerji (kaynak tasarrufu); Madde ve Endüstri (temizlik maddeleri) |

**İnkılap, Din, İngilizce:** Tipler bütün ünitelere uyar.

## 5. Yazım kuralları

1. **Özgünlük.**
   - LGS sorusu, metni ya da sayı kurgusu kopyalanmaz. Envanterdeki özetler yalnızca tarz referansıdır.
   - Türkçe metinler özgün yazılır; gerçek yazarlara ait metinlerden uzun alıntı yapılmaz.
2. **Tek doğru cevap.**
   - Ajan her soruyu bağımsız olarak yeniden çözer.
   - İkinci bir seçenek savunulabiliyorsa soru yeniden yazılır.
3. **Çeldiriciler.**
   - Çeldiriciler adlandırılmış yanılgılardan hesaplanır. Matematikte `yanilgilar.jsonl` anahtarları `distractorKeys` alanına yazılır.
   - Doğru şık uzunluk, ayrıntı ya da kalıp bir ifadeyle kendini ele vermez.
4. **Koşullar açık yazılır.** Örnek: "sürtünmeler önemsiz", "en kısa yol", "π = 3", "ip ve makara ağırlıkları önemsiz".
5. **Program sınırı.**
   - Yalnızca 8. sınıf kazanımları ve 5–7. sınıf önkoşulları kullanılır.
   - Yasak konular: tork/moment hesabı, trigonometri, ikinci dereceden denklem. 2024 Fen 13. soru tork gerektirdiği için iptal edildi.
6. **Görseller.**
   - Kök, görsele açıkça atıf yapar; dolu her görselde `altTextKey` bulunur.
   - Oyunun desteklediği türler: diagram, table, numberline, fraction, grid, chart.
   - Koordinat ve açı şekilleri oyunda desteklenmiyor; bunlar diagram olarak çizilir.
7. **Olumsuz kök.** Kökteki olumsuzluk sözcüğü ("değildir", "ulaşılamaz", "NOT") vurgulanır.
8. **Cevap konumu.** Doğru cevaplar A, B, C ve D arasında dengeli dağıtılır.
9. **Ders üslubu.** Ders bazında üslup için plandaki `styleRules`'a, kaçınılacaklar için `avoid`'e uyulur.

## 6. Etiketleme

| Alan | Değer |
|---|---|
| `objective` | Plandaki `kazanimlar[].code` |
| `level` | `levelSplit`'ten |
| `taskId` | Matematik için plandaki `taskId` |
| `tags` | `["lgs-2027", "lgs-unite:<ünite anahtarı>", "lgs-tip:<itemTypeMix anahtarı>"]` |
| `reviewStatus` / `publishBlocked` | `"pending"` / `true`. Ayrı AI-only denetim ve doğrulayıcı geçişine kadar böyle kalır. |

## 7. Üretim akışı

1. **Parti sırası.** Ders → ünite → kazanım sırasıyla, 10–25 soruluk partiler hâlinde üretin.
2. **Parti adımları.**
   - Kotayı ve `levelSplit`'i plandan alın, soru tiplerini §4'e göre dağıtın.
   - Soruları yazın.
   - Her soruyu bağımsız çözün ve çeldiricileri denetleyin.
   - `tools/pack_validate.py` ile doğrulayın, gerekiyorsa düzeltin.
3. **Ders sonu sayımı.** Ders paketi bitince ünite, kazanım, seviye ve soru tipi sayılarını plandakilerle karşılaştırın.
4. **Deneme formları (isteğe bağlı).** 90 soruluk formları raporun §6'sındaki "2027 için beklenen form" dağılımıyla kurun.

## 8. Komutlar

```bash
python tools/build_lgs_2027_plan.py --check       # plan envanterle güncel mi
python -m pytest tests/test_lgs_2027_plan.py -q   # envanter ve plan tutarlılığı
python tools/pack_validate.py --strict <paket.jsonl>
```

Banka büyüklüğünü değiştirmek için `python tools/build_lgs_2027_plan.py --bank-size 3000`
kullanılır. Bu komut plan dosyasının üzerine yazar.

## 9. Bilinen belirsizlikler

- **Envanterin güvenilirliği.** 270 sorunun 11'inin içeriği bulunamadı, 71'i düşük güvenli.
- **2026 sayısal numaralandırması.** 2026 Matematik ve Fen kayıtları B kitapçığı numarasıyla verildi.
- **Resmî PDF'lerle doğrulama.** Ağ erişimi olan ortamda resmî kitapçıklarla doğrulama yapılabilir.
  - Bağlantılar envanterin `exams.<yıl>.booklets` alanında.
  - Doğrulamadan sonra envanteri güncelleyip planı yeniden üretin.
