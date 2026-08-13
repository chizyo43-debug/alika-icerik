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
