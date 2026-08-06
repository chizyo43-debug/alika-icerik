# AliKa İçerik Şemaları — 2.2 Güncel, 2.0 Geriye Uyumlu

**Güncel üretim sürümü:** 2.2
**Eski paket sürümü:** 2.0 (yalnız geriye uyumluluk)
**Durum:** Tüm yeni ve onarılan paketlerde 2.2 zorunlu
**Uyumluluk:** v1 paketleri `schemaVersion` alanı yoksa v1 kabul edilir.

---

## 0. Güncel Question Contract 2.2

Kanonik şema AliKa uygulama deposundaki
`shared/question-2.2.schema.json`, görsel sözleşmesi ise
`shared/figure_spec.json` dosyasıdır. Bu depodaki `tools/pack_validate.py`
aynı yayın kapılarını uygular.

2.2 için bağlayıcı farklar:

- `hints` alanı yoktur; boş dizi olarak bile yazılması HATA'dır.
- Hiyerarşi `unitKey → topicKey → subtopicKey → noteKey` biçimindedir.
- Notta `id = noteId = noteKey`; soruda `noteId = noteKey` olmalıdır.
- Her soru bir `familyId` taşır; paket en az 80 aile içerir ve bir ailede en
  fazla 8 soru bulunur.
- Dolu her görsel anlamlı bir `altTextKey` taşır.
- Her soru geçerli bir konu anlatımına bağlıdır. `explanation` yalnız o
  sorunun çözümüdür; konu anlatımının yerine geçmez.
- `ai-verified`, yalnız ayrı AI son denetimi ve geçerli içerik/karar hash'leri
  ile kullanılabilir. İnsan onayı yapılmadığı açıkça belirtilir.
- `pack.contractPolicy`, `contentContractVersion`,
  `contentContractHash` ve `visualPolicy` yayın öncesinde zorunludur.

Aşağıdaki 2.0 alan açıklamaları, mevcut eski İngilizce paketinin içe
aktarılabilmesi için korunmuştur; yeni üretime örnek değildir.

---

## 1. Pack (Paket) Satırı — Eski 2.0 Referansı

```json
{
  "type": "pack",
  "schemaVersion": "2.0",
  "id": "tr.meb.g05.mat.t4",
  "version": 3,
  "lang": "tr",
  "country": "TR",
  "curriculum": "MEB-TYMM-2025",
  "subject": "Matematik",
  "grade": 5,
  "theme": "Sayılar ve Nicelikler (2): Kesirler",
  "license": "CC-BY-NC-4.0",
  "labels": {},
  "source": "alika-atolye-v2",
  "provenance": "machine-generated:qwen3-4b:2026-07:human-pending",
  "prerequisites": ["tr.meb.g05.mat.t2"],
  "objectives": ["M.5.1.4.1", "M.5.1.4.2"],
  "coverage": {
    "M.5.1.4.1": {"notes": ["n001","n002"], "questions": 20},
    "M.5.1.4.2": {"notes": ["n003","n004"], "questions": 20}
  }
}
```

### Alanlar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `schemaVersion` | string | **EVET** | `"2.0"` — doğrulayıcı desteklemiyorsa HATA |
| `id` | string | EVET | Paket kimliği (v1'den aynı) |
| `version` | int | EVET | Artan sürüm numarası |
| `lang` | string | EVET | ISO 639-1 dil kodu |
| `country` | string | EVET | ISO 3166-1 ülke kodu |
| `curriculum` | string | EVET | Müfredat tanımlayıcısı |
| `subject` | string | EVET | Ders adı |
| `grade` | int | EVET | Sınıf düzeyi |
| `theme` | string | EVET | Tema/ünite adı |
| `license` | string | EVET | SPDX lisans tanımlayıcısı |
| `labels` | object | EVET | i18n etiketleri (şekil anahtarları) |
| `source` | string | **EVET (v2)** | İçerik kaynağı |
| `provenance` | string | **EVET (v2)** | Üretim zinciri izi |
| `prerequisites` | string[] | HAYIR | Ön koşul paket ID'leri |
| `objectives` | string[] | **EVET (v2)** | MEB kazanım kodları |
| `coverage` | object | HAYIR | Kazanım → not/soru eşlemesi |

### Provenance Formatı

```
<üretim-yöntemi>:<model>:<tarih>:<denetim-durumu>
```

Örnekler:
- `machine-generated:qwen3-4b:2026-07:human-pending`
- `machine-generated:qwen3-4b:2026-07:human-reviewed:2026-08`
- `human-authored:editor:2026-07:verified`

### Kurallar

- `schemaVersion` boş veya `"2.0"` değilse → doğrulayıcı HATA verir
- `objectives` boş dizi olamaz (en az 1 kazanım kodu)
- `provenance` içinde `human-reviewed` veya `verified` yoksa paket `"reviewed"` olarak işaretlenemez
- `source` alanı `"unknown"` olamaz

---

## 2. Note (Not) Satırı

```json
{
  "type": "note",
  "id": "tr.meb.g05.mat.t4.n001",
  "subject": "Matematik",
  "topic": "Kesir Kavramı",
  "title": "Kesir Kavramı",
  "body": "## Kesir Kavramı\n\n...",
  "figure": null,
  "objectives": ["M.5.1.4.1"],
  "band": 2
}
```

### Yeni Alanlar (v2)

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `objectives` | string[] | HAYIR | Bu notun karşıladığı kazanımlar |
| `band` | int | HAYIR | Yaş/anlatım bandı (1-4) |

---

## 3. Question (Soru) Satırı

```json
{
  "type": "question",
  "id": "tr.meb.g05.mat.t4.q001",
  "subject": "Matematik",
  "topic": "Kesir Kavramı",
  "noteId": "tr.meb.g05.mat.t4.n001",
  "objective": "M.5.1.4.1",
  "objectiveSource": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_matematik.pdf",
  "level": 2,
  "difficultyReason": "2 adım: payda eşitleme + toplama; soyut kesir işlemi; çeldiriciler yakın",
  "question": "3/8 + 2/8 işleminin sonucu kaçtır?",
  "choices": ["5/8", "5/16", "6/8", "1/2"],
  "correct": 0,
  "distractorWhy": ["doğru; paylar toplanır payda aynı kalır", "1 paydalar toplanmış; payda sabit kalmalı", "0 paylar çarpılmış; toplama yapılmalı", "0 sadeleştirme hatası; 5/8 zaten sade"],
  "explanation": "Paydalar eşit (8) → payları topla: 3+2=5, payda aynı: 5/8.",
  "figure": null,
  "hints": ["Paydalar eşit mi?", "Eşitse payları topla.", "Payda değişmez.", "3+2=5.", "Sonuç: 5/8."],
  "tags": ["kesir", "toplama", "eşit-payda"],
  "reviewStatus": "pending",
  "provenance": "machine-generated:qwen3-4b:2026-07:human-pending"
}
```

### Alanlar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `id` | string | EVET | Tekil kimlik |
| `objective` | string | **EVET (v2)** | MEB kazanım kodu |
| `objectiveSource` | string | **EVET (v2)** | Resmî kaynak URL |
| `level` | int | EVET | Zorluk (1-5) |
| `difficultyReason` | string | **EVET (v2)** | Zorluk gerekçesi |
| `question` | string | EVET | Soru metni |
| `choices` | string[] | EVET | 4 seçenek |
| `correct` | int | EVET | Doğru indeks (0-3) |
| `distractorWhy` | string[] | EVET | Her seçenek için gerekçe |
| `explanation` | string | EVET | Çözüm açıklaması |
| `figure` | object/null | EVET | Şekil tanımı |
| `hints` | string[] | Yalnız 2.0 | Eski paketlerde 5 kademeli ipucu; 2.2'de yasak |
| `tags` | string[] | HAYIR | Konu etiketleri |
| `reviewStatus` | string | **EVET (v2)** | `pending`/`reviewed`/`rejected` |
| `provenance` | string | **EVET (v2)** | Üretim izi |

### Kurallar

- `objective` boş olamaz (v2)
- `objectiveSource` geçerli URL olmalı (http/https)
- `difficultyReason` en az 20 karakter
- `reviewStatus` yalnızca `pending`, `reviewed`, `ai-verified`, `rejected` olabilir
- `reviewStatus: "reviewed"` için `provenance` içinde `human-reviewed` bulunmalı
- Serbest HTML veya çalıştırılabilir kod yasak
- Tüm çıktı UTF-8

---

## 4. difficultyReason Ölçütleri

En az şu özelliklerden 2'sini içermeli:

- Çözüm adımı sayısı
- İşlem yükü
- Gerekli ön bilgiler
- Metin uzunluğu
- Soyutlama seviyesi
- Çeldirici yakınlığı
- Şekil/tablo yorumlama gereksinimi
- Transfer/muhakeme gereksinimi

Örnek: `"3 adım (eşitleme + toplama + sadeleştirme); ön bilgi: EKOK; çeldiriciler yakın (payda hatası)"`

---

## 5. Migrasyon Stratejisi

1. Mevcut v1 paketlere `schemaVersion: "2.0"` ekle
2. `source: "alika-atolye-v1-migrated"` ekle
3. `provenance: "machine-generated:qwen3-4b:2026-07:human-pending"` ekle
4. `reviewStatus: "pending"` ekle
5. `objective` ve `objectiveSource` — MEB kazanım eşlemesi yapılana kadar `"PENDING"` placeholder
6. `difficultyReason` — otomatik üretim (level + topic bazlı şablon)
7. `tags` — topic'ten otomatik türetme

### Geçiş Kuralları

- `objective: "PENDING"` → doğrulayıcı UYARI (HATA değil) verir
- `objectiveSource: "PENDING"` → doğrulayıcı UYARI verir
- Migrasyon sonrası `version` +1 artar
- Content hash değişir (deterministik sıralama gerekli)

---

## 6. Doğrulayıcı Genişletmeleri

Yeni kurallar (v2):

| Kural | Seviye | Açıklama |
|-------|--------|----------|
| 27 | HATA | `schemaVersion` eksik veya desteklenmiyor |
| 28 | HATA | `source` boş veya "unknown" |
| 29 | HATA | `provenance` format hatası |
| 30 | UYARI | `objective` boş veya "PENDING" |
| 31 | UYARI | `objectiveSource` boş veya geçersiz URL |
| 32 | HATA | `difficultyReason` 20 karakterden kısa |
| 33 | HATA | `reviewStatus` geçersiz değer |
| 34 | HATA | `reviewStatus: reviewed` ama provenance'da human-reviewed yok |
| 35 | UYARI | Doğru cevap konumu pakette %35'i aşıyor |
| 36 | HATA | `distractorWhy` uzun görünmesine rağmen öğrencinin somut hatasını adlandırmayan şablon içeriyor |
| 37 | HATA | `difficultyReason` soru kökünü uzatan jenerik şablon içeriyor |
| 38 | UYARI | Yalnız 2.0: 4. veya 5. ipucu paket sorularının en az %70'inde aynı |
| 39 | RAPOR/UYARI | Tekrarlı seçenek kümeleri ve sürekli yanlış seçenekler raporlanır; yalnız açıkça bozuk dil biçimlerinin 4+ kez dolgu olarak kullanılması uyarı verir |
