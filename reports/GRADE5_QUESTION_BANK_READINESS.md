# Türkiye 5. Sınıf — 2.000 Soruluk Banka Hazırlık Raporu

Tarih: 7 Ağustos 2026

Karar: **AI-only yayın adayı**

İnsan incelemesi: **Yok**

## Sonuç

`turkiye/5-sinif/soru-bankasi/5-sinif-tum-dersler-2000-soru.jsonl`,
beş doğrulanmış ders paketinden deterministik olarak oluşturulan ortak seçkidir.
Yeni yazılmış 2.000 soru değildir; kaynak 2.500 sorudan ders başına 400 kayıt
seçer ve kaynak kaydın kararlı kimliğini, içeriğini ve AI inceleme hash'ini
değiştirmeden korur.

| Ölçüt | Sonuç |
|---|---:|
| Konu anlatımı | 116 |
| Soru | 2.000 |
| Ders başına soru | 400 |
| Soru ailesi | 565 |
| Aile başına üst sınır | 8 |
| Doğru cevap konumları | 500 / 500 / 500 / 500 |
| Görselli soru | 477 |
| Validator | 0 hata / 0 uyarı |
| Kalite skoru | 99,78 |

## Görsel güvencesi

Kaynak paketlerdeki bütün görselli sorular korunmuştur:

| Ders | Kaynak | Ortak bankada |
|---|---:|---:|
| Matematik | 116 | 116 |
| Fen Bilimleri | 160 | 160 |
| Türkçe | 0 | 0 |
| İngilizce | 100 | 100 |
| Sosyal Bilgiler | 101 | 101 |

Tablo, grafik, şekil, akış veya devreye atıf yapan soru geçerli `figure`
olmadan doğrulamadan geçemez. Her görseldeki `altTextKey` ve diğer metin
anahtarları paket `labels` sözlüğünde çözülür. Seçim motoru yalnız görselsiz
soruları eleyebilir.

## Seçim güvenceleri

- Her ders ve her doğru cevap konumu için tam 100 soru seçilir.
- Hiçbir konu anlatımı, kazanım veya soru ailesi seçki dışında kalmaz.
- Bir kaynak seçeneğin doğru örneğini kaldırarak onu sürekli yanlış dolguya
  dönüştüren seçimlere izin verilmez.
- Çok dersli derlemede kapalı seçenek havuzu ders bazında ölçülür.
- `hints` alanı yasaktır; her soru geçerli `noteId`/`noteKey` bağı taşır.
- Derleme yeniden çalıştırıldığında aynı kaynaklarla aynı seçki oluşur.

## AliKa uyumluluğu

Windows gerçek içe aktarıcısı ile temiz veritabanında sınandı:

- 1 ortak koleksiyon,
- 116 konu anlatımı,
- 2.000 soru,
- ders başına 400 soru,
- 477 kayıpsız görsel,
- bütün sorularda konu anlatımı bağlantısı,
- ikinci içe aktarmada kopya oluşturmadan aynı paketin etkinleştirilmesi.

Ortak paket 2.117 JSONL satırıdır. AliKa Windows ve Android güvenlik sınırı,
2.000 soruya ek olarak paket başlığı ve bağlı notları kabul edecek şekilde
2.500 satıra yükseltilmiştir; dosya boyutu ve satır başına boyut kontrolleri
korunmuştur.

## Tekrarlanabilir komutlar

```text
python tools/build_grade5_question_bank.py --write
python tools/finalize_ai_release.py soru-bankasi
python tools/pack_validate.py turkiye/5-sinif/soru-bankasi/5-sinif-tum-dersler-2000-soru.jsonl --skor
python -m pytest -q
```
