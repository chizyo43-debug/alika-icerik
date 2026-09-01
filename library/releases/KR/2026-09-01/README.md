# Kore 2026-09-01 yayımlama paketi

Bu dizin AliKa uygulamasına doğrudan içe aktarılabilen Kore güvenli-kapsam
yayımını taşır: 94 ders ZIP'i, 47.000 soru, 2.162 konu anlatımı, 9.400 soru
ailesi, 48.743/48.743 zorunlu görsel, 135 yerel WAV, 675 soru-ses bağı ve 225
yerel konuşma-kayıt sorusu.

`release-catalog.json` bütün ZIP ve kaynak karmalarını; `release-audit.json` son
kabul sonucunu taşır. Kanıt gerektiren 289 müfredat hedefi paket dışındadır ve
`withheldObjectives` olarak listelenir; bu yüzden yayımlanan güvenli kapsam
`publishable=true`, tüm müfredat kapsamı ise `fullCurriculumCoverage=false`tır.

Kayıtların `reviewStatus=pending` ve `humanReviewed=false` değerleri korunur.
Codex öz-denetimi yalnız paket/yayım metadata katmanındadır. Ortaokul 7-9
yerleşimi AliKa öğrenme sırasıdır; ulusal olarak sınıfa özgülük iddiası değildir.
Lise seçmelileri öğrenci veya okul ders seçimine bağlanmalıdır.

Yeniden üretim ve kabul:

```powershell
python library/tools/build_kr_publish_release.py
python -m pytest library/tests/test_kr_publish_release.py -q
```
