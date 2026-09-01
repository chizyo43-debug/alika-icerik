# Japonya 2026-09-01 yayımlama paketi

Bu dizin AliKa uygulamasına doğrudan içe aktarılabilen Japonya güvenli-kapsam
yayımını taşır. `release-catalog.json` bütün ZIP ve kaynak karmalarını;
`release-audit.json` son kabul sonucunu taşır.

Konuşma performansını gerçekten ölçmeyen çoktan seçmeli İngilizce kayıtlar tam
performans kanıtı olarak yayımlanmaz. İlgili hedefler `withheldObjectives`
alanında açıkça tutulur. Kayıtların `reviewStatus=pending` ve
`humanReviewed=false` değerleri korunur; Codex öz-denetimi yalnız paket/yayım
metadata katmanındadır.

Yeniden üretim ve kabul:

```powershell
python library/tools/build_jp_publish_release.py
python -m pytest library/tests/test_jp_publish_release.py -q
```
