# AliKa oyun paketleri

Bu dizin AliKa'nın yalnız veri taşıyan `.alika-game` paketlerini barındırır.
Paketler kod, eklenti, dış URL veya çalıştırılabilir dosya içermez.

## Bilgi Yarışması v1

`trivia` kataloğu dört AliKa yaş bandını ve dokuz uygulama dilini kapsar:

- `young`: 5–7
- `mid`: 8–11
- `teen`: 12–14
- `senior`: 15–18
- Diller: `tr`, `en`, `de`, `es`, `fr`, `pt`, `ru`, `ja`, `ko`

Her dil/yaş bileşimi tam 200 soruluk ayrı bir havuzdur. Kaynak JSONL
dosyaları `games/trivia/questions`, indirilebilir deterministik arşivler
`games/trivia/dist` altındadır. `catalog.json` her paketin SHA-256 karmasını,
yaş aralığını, dilini ve soru sayısını listeler.

Kaynak kayıtlardaki `source` ve `culture_tags` denetim bilgisidir; çocuk
cihazına giden pakete yalnız AliKa'nın beyaz listedeki soru alanları yazılır.
Katalog insan kültürel incelemesi tamamlanana kadar `ai-draft` durumundadır.

```powershell
python tools/build_trivia_games.py
python tools/build_trivia_games.py --check
python -m pytest tests/test_trivia_games.py -q
```

## Ülke–Başkent Hafızası v1

`memory` kataloğu da aynı dokuz dil ve dört yaş bandında 36 ayrı paket sunar.
Her pakette, oyun başında seçilen 2–12 çiftlik turu besleyen 100 ülke–başkent
çifti vardır. Kaynak JSONL dosyaları `games/memory/pairs`, deterministik ve
yalnız veri taşıyan arşivler `games/memory/dist` altındadır.

Kaynak kayıtlar izlenebilirlik için HTTPS Wikidata bağlantısı ve kültür etiketi
taşır; çalışma zamanı paketine yalnız `pair_id`, `left`, `right`, `category` ve
`explanation` alanları girer. Katalog insan onayı gerektirmeyen AI-only yayın
akışında `ai-draft` ve `human_approved: false` olarak açıkça işaretlenir.

```powershell
python tools/generate_memory_geography.py
python tools/build_memory_games.py
python tools/build_memory_games.py --check
python -m pytest tests/test_memory_games.py -q
```

## Çarkıfelek v1

`word-wheel` kataloğu dokuz dil ve dört yaş bandında 36 paket sunar. Her pakette
sistemin tur başında otomatik seçtiği tam 200 kelime bulmacası vardır; toplam
7.200 bulmaca bulunur. Ortak ekrana cevap değil, yalnız kategori, ipucu ve kapalı
harf tahtası gider.

```powershell
python tools/generate_word_wheel_geography.py
python tools/build_word_wheel_games.py
python tools/build_word_wheel_games.py --check
python -m pytest tests/test_word_wheel_games.py -q
```
