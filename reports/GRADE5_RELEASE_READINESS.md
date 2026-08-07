# Türkiye 5. Sınıf Yayın Hazırlık Raporu

**Tarih:** 7 Ağustos 2026

**Karar:** Yayına hazır

**İnceleme modeli:** Codex Sol, AI-only

**Beyan:** İçerik yapay zekâ tarafından üretilmiş ve yapay zekâ tarafından
incelenmiştir; insan onayı yoktur.

## Sonuç

Türkiye 5. sınıfın beş ders paketi Question Contract 2.2 ve AliKa veri
sözleşmesiyle uyumludur. Paketlerin tamamı 0 hata, 0 uyarı ve en az 99 kalite
puanıyla geçmiştir. Her soru geçerli bir konu anlatımına bağlıdır; `hints`
alanı yoktur.

| Ders | Not | Soru | Aile | Cevap dağılımı | Not görseli | Soru görseli | Skor |
|---|---:|---:|---:|---|---:|---:|---:|
| Matematik | 23 | 500 | 115 | 125 / 125 / 125 / 125 | 23 | 116 | 99,25 |
| Fen Bilimleri | 28 | 500 | 140 | 125 / 125 / 125 / 125 | 28 | 160 | 99,61 |
| Türkçe | 22 | 500 | 118 | 125 / 125 / 125 / 125 | 22 | 0 | 100,00 |
| İngilizce | 24 | 500 | 83 | 125 / 125 / 125 / 125 | 24 | 100 | 100,00 |
| Sosyal Bilgiler | 19 | 500 | 109 | 125 / 125 / 125 / 125 | 19 | 101 | 100,00 |
| **Toplam** | **116** | **2.500** | — | — | **116** | **477** | — |

Türkçe soru görseli sayısının sıfır olması bilinçli ders politikasıdır.
Türkçede süs amaçlı görsel yerine metin becerisi korunmuş, 22 konu
anlatımının tamamına anlamlı öğretim görseli eklenmiştir.

## Tamamlanan onarımlar

- İngilizce 518 sorudan, kazanım ve aile kapsamını koruyan 500 soruluk nihai
  pakete indirildi; `ENG.5.8.L4` kapsamındaki 18 yeni soru korundu.
- İngilizcedeki kalıp çözüm açıklamaları somut dil bilgisi veya bağlam
  gerekçelerine dönüştürüldü; soru ile çelişen zaman, yer, etkinlik ve gezi
  sırası gerekçeleri düzeltildi.
- Sosyal Bilgiler tam paket olarak eklendi. Görsele aktarılırken soru kökünde
  kalan kanıt satırları tabloya geri taşındı ve erişilebilir alternatif
  metinler yenilendi.
- Yerleşim yeri belgesinin e-Devlet/Nüfus ve Vatandaşlık İşleri üzerinden
  alınabilmesi güncel resmî uygulamayla hizalandı.
- Deprem tehlikesi ile risk kavramı ayrıldı; arkeolojik bulgulardan özel
  mülkiyet hakkında kesin sonuç çıkaran ve çocukları etiketleyebilecek
  ifadeler yumuşatıldı.
- Kalite puanı, doğrulayıcının gerçek kabul eşikleriyle aynı ölçeğe getirildi;
  ham ölçümler raporda ayrıca korunmaktadır.

## Doğrulama kanıtı

- `python tools/pack_validate.py turkiye/5-sinif --skor`
  - 5/5 paket geçti.
  - Her pakette 0 hata ve 0 uyarı.
- `ALIKA_APP_REPO=<uygulama> python -m pytest tests -q`
  - 105 test geçti.
  - Gerçek AliKa Windows içe aktarıcısıyla 5 paket, 116 not ve 2.500 soru
    geçici veritabanına kayıpsız alındı.
  - Yeniden içe aktarma kimlikleri çoğaltmadan aynı içeriği buldu.
- Android görsel sözleşmesi ve kitaplık içe aktarma birim testleri geçti.
- Değişen İngilizce ve Sosyal Bilgiler paketlerinde her kazanımdan bir kayıt
  seçen 43 soruluk bağımsız AI örneklemi
  `reports/GRADE5_AI_REVIEW_SAMPLE.md` içinde saklanmıştır.

## Yayın kuralı

Paketler yalnız `ai-verified` durumundadır. Hiçbir kayıt `human-reviewed`
veya insan onaylı olarak sunulmaz. İçerik ve inceleme hash'leri kayda
bağlıdır; sonraki bir değişiklik mevcut inceleme kararını geçersiz kılar ve
yeniden doğrulama gerektirir.
