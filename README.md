# AliKa içerik deposu

AliKa uygulamasının ders içeriği: Türkiye ortaokul **5–8. sınıf** soru bankaları ve konu anlatımları (2026–2027 öğretim yılı),
**LGS 2027 deneme** paketi, **LGS 2028 hazırlık (7. sınıf)** paketleri, **ilkokul (6–10 yaş) görsel etkinlik** paketi ve
AliKa TV oyun paketleri.
Diğer ülkeler ve eski Türkiye verisi bu sürümde kaldırıldı; geçmiş sürümler git geçmişinde durur.

## Düzen

```
turkiye/<N>-sinif/<ders-klasörü>/<paket>.jsonl   ders paketleri (Question/Note 2.2, JSON Lines)
turkiye/8-sinif/lgs-2027/lgs-2027-<ders>.jsonl    LGS 2027 deneme paketi (6 ders, deneme formları)
turkiye/7-sinif/lgs-2028/lgs-2028-<ders>.jsonl    LGS 2028 hazırlık deneme paketi, 7. sınıf (6 ders, 5 form)
turkiye/7-sinif/lgs-2028-unite-setleri/…           LGS 2028 hazırlık ünite setleri, 7. sınıf (6 ders, 43 ünite)
ilkokul/gorsel-etkinlikler/<paket>.jsonl          ilkokul görsel etkinlik paketi (dilden bağımsız, visualChoice v3)
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

LGS 2028 hazırlık (7. sınıf, TYMM; İngilizce 2018 programı) iki parçadır:
- Deneme paketi `tr.g07.<ders>.lgs2028`: `assessment.exam: lgs-2028-hazirlik`, `examOnly`; 5 form × 90 soru. Uygulama formu
  çocuğun işlediği konulara göre kısaltır (`calendar`). 45 ünite notu yalnız ebeveyn panelinin LGS kartında görünür.
- Ünite setleri `tr.g07.<ders>.lgs2028u`: `assessment` yok, her soruda `lgsSet` bloğu (ünite, set sırası, `requires`);
  konu adı «Ünite setleri — <ünite>». 327 soru, 43 not; notlar Ders Arşivi'nde ünite altında görünür. Setler deneme
  paketinin `calendar`'ıyla açılır, bu yüzden deneme paketi de kurulmalıdır.
- AliKa Windows 1.2.15 ve sonrasını gerektirir (iki öbekli TYMM kodları ve `lgsSet`). Android'de bu kurallar bir sonraki
  Play sürümüyle gelir; o zamana kadar Android bu paketleri reddeder.
- İnceleme: `ai-verified`, insan incelemesi yapılmadı. Bağlam temelli sorular MEB Bağlam Temelli Çoktan Seçmeli Soru
  Yazım Kılavuzu'na göre yazıldı; LGS sorusu değildir.

Ders paketi başına en çok 500 soru; bir ders birden çok pakete (dönem/ünite) bölünür.

## İlkokul görsel etkinlikler

`ilkokul/gorsel-etkinlikler/ilkokul-gorsel-renkli-6-10.jsonl`: 6–10 yaş (ilkokul, ortaokul öncesi) için renkli
şekil kartlarıyla 600 görsel soru. Dört tür vardır: benzerlik (325), «Sıradaki ne?» (100), «Farklı olanı bul» (100)
ve «Tabloyu tamamla» (75). Sorular 24 ailede B1–B6 basamaklarına dizilidir. Metin, okuma ya da ses gerektirmez
(`lang: zxx`); kartlar renk körü dostu Okabe-Ito tonlarıyla çizilir.

- Ders paketi değildir: Question/Note 2.2 kuralları (`pack_validate`) uygulanmaz. Kalite kapısı her sorunun yapısını
  uygulamanın visualChoice sözleşmesiyle (`dogrulayici/windows/visual_choice.py`) denetler; bu pakette bilinen bulgu
  yoktur. Sözleşme doğru şıkkın kendisini yeniden hesaplamaz; o denetim üretim tarafında yapılır (aşağıda).
- Uygulamaya paket olarak içe aktarılır. visualChoice v3 kartları AliKa Windows 1.2.12 ve sonrası ile alika main
  764bea29 sonrası Android sürümlerini gerektirir. 500'ü aşan tek dosyayı eski Android sürümleri kısaltıyordu; yeni
  sürümler dosya başına 2.000 soruya kadar alır.
- İnceleme durumu: `reviewStatus: pending`, `humanReviewed: false`. Yaş yerleşimi editoryaldir, çocuklarla henüz
  denenmedi (`agePlacement: editorial-not-child-validated`). Doğru şıklar üreticide kuraldan hesaplanır ve üretim
  tarafındaki ayrı bir doğrulayıcı her sorunun kaydındaki `semanticCase`'ten yeniden hesaplayarak denetler (o araç bu
  depoda değildir).
- Açık işler (paket başlığında `publishable: false` bu yüzden duruyor): v3 destekli Android sürümünün yayımlanması,
  Windows'ta kartların gerçek ekran denetimi, ödül akışının cihazda kabulü, çocuk denemesi (4x4 kartlar dahil).
  Paketin Android'de içe aktarımı ve çizimi bir test telefonunda denendi (600/600).
- Lisans: depodaki öteki içerik paketleri gibi CC BY-NC 4.0 (bu paketin başlığında `license` alanı yoktur).

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
