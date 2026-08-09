# Türkiye 6. Sınıf — 2.000 Soruluk Banka Hazırlık Raporu

Tarih: 9 Ağustos 2026

Karar: **AI-only yayına hazır**

İnsan incelemesi: **Yok**

## Sonuç

`turkiye/6-sinif/soru-bankasi/6-sinif-tum-dersler-2000-soru.jsonl`, yedi
AI-only doğrulanmış 6. sınıf ders paketinden deterministik olarak oluşturulan
ortak seçkidir. Yeni yazılmış 2.000 soru değildir; kaynak 3.500 sorudan beş
ana ders için 380'er, Bilişim ile Din Kültürü için 50'şer kayıt seçer.

| Ölçüt | Sonuç |
|---|---:|
| Konu anlatımı | 168 |
| Soru | 2.000 |
| Matematik / Fen / Türkçe / İngilizce / Sosyal | 380'er |
| Bilişim Teknolojileri ve Yazılım | 50 |
| Din Kültürü ve Ahlak Bilgisi | 50 |
| Soru ailesi | 632 |
| Doğru cevap konumları | 500 / 500 / 500 / 500 |
| Görselli soru | 1.418 |
| Resmî kaynak belgesi | 7 |
| Kesin kaynak kanıtı bulunan not + soru | 2.168 / 2.168 |
| Geçerli konu anlatımı bağlantısı | 2.000 / 2.000 |
| `hints` alanı | 0 |
| Depo validatorü | 0 hata / 0 uyarı |
| Kalite skoru | 99,87 |
| Üretim profili validatorü | 0 bulgu |

## Ders dağılımı ve görseller

| Ders | Soru | Görselli soru |
|---|---:|---:|
| Matematik | 380 | 164 |
| Fen Bilimleri | 380 | 327 |
| Türkçe | 380 | 173 |
| İngilizce | 380 | 298 |
| Sosyal Bilgiler | 380 | 369 |
| Bilişim Teknolojileri ve Yazılım | 50 | 48 |
| Din Kültürü ve Ahlak Bilgisi | 50 | 39 |

Seçim görselli sorulara öncelik verir; seçilen hiçbir sorunun görseli
çıkarılmaz. Bilişim ve Din için 50'şer soruluk kota nedeniyle bu iki kaynak
paketteki bütün görsellerin ortak bankaya alınması mümkün değildir. Paket
birleştirilirken her görsele açık öğrenci yönergesi eklenir ve dersler arasında
çakışabilen görsel metin anahtarları paket kimliğiyle ad alanına alınır.

## Seçim ve kalite güvenceleri

- Her konu anlatımı ve kazanım en az bir seçili soruyla bağlı kalır.
- Beş ana derste kaynak soru ailelerinin tamamı korunur; düşük kotalı Bilişim
  ve Din derslerinde kazanım kapsamı korunurken en geniş aile çeşitliliği
  seçilir.
- Aynı dört seçenekten oluşan kümelerin bağımsız soru ailelerine yayılması ve
  sürekli yanlış dolgu seçenekler deterministik takaslarla azaltılır.
- Kısa/jenerik çeldirici gerekçeleri, doğru çözüm ölçütüne bağlanır; açıklamada
  cevabı harfle ele veren son cümleler kaldırılır.
- Her doğru cevap konumu toplamda tam 500 kez kullanılır.
- Paket başlığındaki `sourcePackages`, yedi kaynak dosyanın yolu ve SHA-256
  özetini taşır.
- Bütün kayıtlar `ai-verified`; `publishBlocked=false`; insan incelemesi yoktur.

## Tekrarlanabilir komutlar

```text
python tools/build_grade6_question_bank.py --write
python tools/finalize_ai_release.py soru-bankasi-6
python tools/pack_validate.py turkiye/6-sinif/soru-bankasi/6-sinif-tum-dersler-2000-soru.jsonl
python tools/pack_validate.py --skor turkiye/6-sinif/soru-bankasi --json reports/grade6_question_bank_quality.json
python -m pytest tests/ -q
```
