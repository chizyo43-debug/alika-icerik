# AliKa içerik deposu

AliKa uygulamasının ders içeriği: Türkiye ortaokul **5–8. sınıf** soru bankaları ve konu anlatımları (2026–2027 öğretim yılı),
**LGS 2027 deneme** paketi ve AliKa TV oyun paketleri.
Diğer ülkeler ve eski Türkiye verisi bu sürümde kaldırıldı; geçmiş sürümler git geçmişinde durur.

## Düzen

```
turkiye/<N>-sinif/<ders-klasörü>/<paket>.jsonl   ders paketleri (Question/Note 2.2, JSON Lines)
turkiye/8-sinif/lgs-2027/lgs-2027-<ders>.jsonl    LGS 2027 deneme paketi (6 ders, deneme formları)
KATALOG.json                                      paket listesi, soru sayıları, sha256
dogrulayici/                                      uygulamanın doğrulayıcısı (alika main kopyası) + kalite kapısı
games/                                            AliKa TV oyun paketleri (Çarkıfelek, İsim Şehir), bkz. games/README.md
tools/, tests/                                    oyun paketi üreticileri ve testleri
.github/workflows/icerik.yml                      CI: kalite kapısı + oyun paketleri güncel mi
```

Ders klasörleri: `turkce`, `matematik`, `fen-bilimleri`, `sosyal-bilgiler` (5–7), `inkilap-tarihi` (8), `ingilizce`,
`din-kulturu-ve-ahlak-bilgisi` (5, 7, 8), `din-kulturu` (6), `bilisim-teknolojileri` (5–6), `teknoloji-ve-tasarim` (7–8).

LGS paketi ders paketlerinden ayrıdır: kimlikler `tr.g08.<ders>.lgs2027`, başlıkta `assessment.kind: lgs-deneme`
(`examOnly`); uygulama bu soruları yalnız LGS deneme bölümünde kullanır. Yeni deneme formları aynı paketin bir üst sürümüyle gelir.

Paket başına en çok 500 soru; bir ders birden çok pakete (dönem/ünite) bölünür.

## Program

- 5., 6. ve 7. sınıf: Türkiye Yüzyılı Maarif Modeli (TYMM) programları.
- 8. sınıf ve 7. sınıf İngilizce: 2018/2019 programları (2026–2027'de yürürlükte); yeni program yürürlüğe girince güncellenecek.
- Her soruda `objective` (öğrenme çıktısı kodu), `topic`, `topicKey`, `unitKey`, `noteId`, `level` bulunur.

## Gösterim

Sorular MEB sınav biçimine göre yazılır (kök kalın, kökteki olumsuz sözcük altı çizili, bağlam ayrı `context` alanında,
öncüller I. II. III.). Metin işaretleri AMI biçimindedir (`__altı çizili__`); bunu kullanan paketlerin başlığında
`"textMarkup": "alika-ami/1"` vardır. Şekiller AliKa Figure Spec'e (`dogrulayici/shared/figure_spec.json`) uyar.
Bu özellikler AliKa Android 0.3.11 / Windows (alika main 2026-10-17) ve sonrasını gerektirir.

## Yeni içerik eklemek

1. Paketi `turkiye/<N>-sinif/<ders-klasörü>/` altına `.jsonl` olarak koyun (ya da mevcut paketi güncelleyin).
   **Mevcut paketin içeriği değişiyorsa başlıktaki `version` bir artırılır**: uygulama, kurulu paketin yerine ancak
   daha yüksek sürümü kurar («sürüm N, kurulu sürüm N değerinden yeni değil» hatası).
2. Doğrulayın: `python dogrulayici/tools/pack_validate.py turkiye/<N>-sinif/<ders>/<paket>.jsonl` → **0 HATA** olmalı.
3. Kataloğu yenileyin: `python dogrulayici/kontrol.py --katalog-yaz`.
4. Kalite kapısını çalıştırın: `python dogrulayici/kontrol.py` (CI aynı komutu çalıştırır).

Kalite kapısı yeni HATA'ya izin vermez. `dogrulayici/bilinen-bulgular.json` uygulama ekibine raporlanmış yanlış alarmları
tutar (ör. Türkçe yazım öğreten sorulardaki «13.00» saat yazımı, İngilizce metindeki saat); doğrulayıcı düzeldikçe bu liste kısalır.
Listeye yalnız onaylı yanlış alarm eklenir (`--temel-yaz`).

## Doğrulayıcı

`dogrulayici/` uygulama deposundaki doğrulayıcının birebir kopyasıdır (kaynak commit `dogrulayici/KAYNAK.txt`).
Elle değiştirilmez; uygulama tarafında güncellenince yeniden kopyalanır.

## İnceleme durumu

İçerik yapay zekâ ile üretildi ve yapay zekâ ile incelendi. Her kaydın durumu kendi alanlarındadır: `reviewStatus`
(`ai-verified`), `reviewedContentSha256` (incelenen içeriğin hash'i), `reviewDecisionSha256` ve `provenance` (karar belgesinin hash'i).
Damga inceleyen modeli adlandırmaz. İnsan incelemesi yapılmadı (`humanReviewed: false`).

## Lisans

İçerik paketleri CC BY-NC 4.0 (paket başlığındaki `license` alanı).
