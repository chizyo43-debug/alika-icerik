# AliKa İçerik Deposu — Başlangıç Kalite Raporu (BASELINE)

**Tarih:** 2026-07-31  
**Depo:** chizyo43-debug/alika-icerik  
**Kapsam:** Türkiye 5. sınıf — Matematik, Fen Bilimleri, Türkçe

---

## 1. Genel İstatistikler

| Metrik | Değer |
|--------|-------|
| JSONL dosyası | 28 |
| Paket (pack satırı) | 28 (21 benzersiz) |
| Not (note satırı) | 252 (189 benzersiz) |
| Soru (question satırı) | 2.523 (1.893 benzersiz) |
| Toplam satır | 2.803 |
| Toplam boyut | 2,44 MB |

## 2. Kritik Bulgular

### 2.1 Fen Bilimleri Duplikasyonu (KRİTİK)

Fen Bilimleri'nde her ünite **iki kez** mevcut:
- `u1.jsonl`–`u7.jsonl`: Zenginleştirilmiş notlar (ort. 1.064 karakter)
- Açıklayıcı adlı dosyalar: Kısa notlar (ort. 471 karakter)

**Sorular birebir aynı** (90/90 ortak). Fark yalnızca not gövdelerinde.
Aynı pack ID'leri kullanılıyor → 693 duplike satır kimliği.

**Karar:** u1-u7 (zengin) içerik kanonik kabul edilecek, açıklayıcı dosya adlarıyla birleştirilecek.

### 2.2 Doğru Cevap Konumu (KRİTİK)

| Konum | Sayı | Oran |
|-------|------|------|
| A (index 0) | 2.519 | %99,8 |
| B (index 1) | 1 | %0,0 |
| C (index 2) | 1 | %0,0 |
| D (index 3) | 2 | %0,1 |

**Tüm sorularda doğru cevap A şıkkında.** Ölçme sistemi geçersiz.

### 2.3 Kazanım (Objective) Eksikliği (KRİTİK)

- `objective` boş: 2.523 / 2.523 (%100)
- `objectiveSource` boş: 2.523 / 2.523 (%100)

Hiçbir soru MEB kazanım koduna bağlı değil.

### 2.4 İpucu-Cevap Sızıntısı (YÜKSEK)

1.063 soruda (%42) ipuçları doğru cevap metnini içeriyor.

### 2.5 Görsel/Şekil Yetersizliği (YÜKSEK)

- Şekilli soru: 20 / 2.523 (%0,8)
- Tüm şekiller Matematik'te (kesir, sayı doğrusu)
- Fen ve Türkçe'de sıfır şekil

## 3. Ders Bazında Kalite Profili

### 3.1 Matematik (7 paket, 63 not, 633 soru)

| Metrik | Değer |
|--------|-------|
| Doğru A oranı | %99,7 |
| Seviye dağılımı | L1: %28,6 / L2: %43,1 / L3: %28,3 |
| Şekilli soru | 20 |
| objective boş | %100 |
| Türkçe karakter | Var (doğru) |
| Yer tutucu | 0 |

**Güçlü yönler:** Aritmetik doğrulama yapılabilir, açıklamalar çözüm yöntemi içeriyor, çeldiriciler öğrenci hatalarına dayalı.

**Zayıf yönler:** Cevap konumu, objective eksik, şekil yetersiz, bazı sorular çok benzer.

### 3.2 Fen Bilimleri (14 dosya → 7 benzersiz paket, 126→63 not, 1260→630 soru)

| Metrik | Değer |
|--------|-------|
| Doğru A oranı | %99,8 |
| Seviye dağılımı | L1: %28,1 / L2: %41,4 / L3: %30,5 |
| Şekilli soru | 0 |
| objective boş | %100 |
| Türkçe karakter | Var (doğru) |
| Duplikasyon | 7 paket × 2 |

**Güçlü yönler:** Zenginleştirilmiş notlar detaylı, bilimsel içerik genel olarak doğru.

**Zayıf yönler:** Duplikasyon, cevap konumu, şekil yok, objective yok, ezbere dayalı soru oranı yüksek.

### 3.3 Türkçe (7 paket, 63 not, 630 soru)

| Metrik | Değer |
|--------|-------|
| Doğru A oranı | %100,0 |
| Seviye dağılımı | L1: %29,8 / L2: %41,0 / L3: %29,2 |
| Şekilli soru | 0 |
| objective boş | %100 |
| Türkçe karakter | YOK (604/630 soru ASCII transliterasyon) |
| Yer tutucu | 34 ("yazim farki", "farkli ornek") |

**Güçlü yönler:** Konu kapsamı geniş, notlar yapılandırılmış.

**Zayıf yönler:** Türkçe karakter yok (en kritik), yer tutucular, cevap konumu, tüm sorular A.

## 4. Şema Eksiklikleri

Mevcut pakette bulunmayan alanlar:
- `schemaVersion`
- `source` / `provenance`
- `prerequisites`
- `objectives` (paket düzeyinde)
- `coverage` matrix
- `difficultyReason` (soru düzeyinde)
- `tags`
- `reviewStatus`

## 5. Öncelik Sıralaması

| # | Sorun | Önem | Etki |
|---|-------|------|------|
| 1 | Cevap konumu %99,8 A | KRİTİK | Ölçme geçersiz |
| 2 | Fen duplikasyonu (7 paket ×2) | KRİTİK | Depo bütünlüğü |
| 3 | objective/objectiveSource %100 boş | KRİTİK | Müfredat izlenebilirliği yok |
| 4 | Türkçe karakter yok (604 soru) | KRİTİK | Dil kalitesi |
| 5 | İpucu-cevap sızıntısı (1.063) | YÜKSEK | Ölçme gücü |
| 6 | Yer tutucular (34) | YÜKSEK | Yayınlanamaz |
| 7 | Şekil yetersizliği (%0,8) | YÜKSEK | Öğretim kapasitesi |
| 8 | Şema V2 eksik | ORTA | Sürdürülebilirlik |
| 9 | difficultyReason yok | ORTA | Zorluk kalibrasyonu |
| 10 | reviewStatus yok | ORTA | İnsan denetimi |

## 6. Kanonik Sayılar (Duplikasyon Sonrası Hedef)

| Ders | Paket | Not | Soru |
|------|-------|-----|------|
| Matematik | 7 | 63 | 633 |
| Fen Bilimleri | 7 | 63 | 630 |
| Türkçe | 7 | 63 | 630 |
| **Toplam** | **21** | **189** | **1.893** |
