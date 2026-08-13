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

## Bu Kim? v1

`who-is-it` kataloğu dokuz dil ve dört yaş bandında 36 paket sunar. Her pakette
sistemin tur başında otomatik seçtiği 200 kaynaklı kişi vardır; toplam 7.200
oyun girdisi bulunur. Kişinin adı çözülene kadar ortak ekrana çıkmaz. İpuçları
sırayla açılır ve erken doğru tahmin daha yüksek puan getirir.

```powershell
python tools/fetch_who_is_it_wikidata.py
python tools/generate_who_is_it.py
python tools/build_who_is_it_games.py
python tools/build_who_is_it_games.py --check
python -m pytest tests/test_who_is_it_games.py -q
```

## Tabu v1

`taboo` kataloğu dokuz dil ve dört yaş bandında 36 indirilebilir paket sunar.
Her pakette 200 kart, her kartta bir hedef ve dört yasak kelime vardır; toplam
7.200 kart bulunur. Sistem uygun havuzdan kartı otomatik seçer. Kaynak bağlantıları
denetim dosyalarında kalır, çocuk cihazına giden pakete eklenmez.

```powershell
python tools/generate_taboo_geography.py
python tools/build_taboo_games.py
python tools/build_taboo_games.py --check
python -m pytest tests/test_taboo_games.py -q
```

## Yalancı v1

`liar` kataloğu dokuz dil ve dört yaş bandında 36 indirilebilir paket sunar.
Her pakette 200 kart vardır. Bir kartta üç cümleden ikisi doğru, biri yanlıştır;
oyuncular yalanı seçer ve cevap açılınca doğru bilgi gösterilir. Toplam 7.200
kartın kaynak bağlantıları yalnız denetim kayıtlarında tutulur.

```powershell
python tools/generate_liar_geography.py
python tools/build_liar_games.py
python tools/build_liar_games.py --check
python -m pytest tests/test_liar_games.py -q
```

## Sessiz Sinema v1

`charades` kataloğu dokuz dil ve dört yaş bandında 36 indirilebilir paket sunar.
Her pakette 200 hareket kartı vardır; toplam 7.200 kart bulunur. Kartların 40'ı
doğrudan ilgili dilin kültüründen gelen karakter veya meslekleri kullanır. Oyun;
klasik takım, beş kartlık hızlı tur, ortak aile ve oyuncu zinciri seçeneklerini,
ayrıca yaşa göre güvenli pas ve süre ayarlarını taşır.

```powershell
python tools/generate_charades.py
python tools/build_charades_games.py
python tools/build_charades_games.py --check
python -m pytest tests/test_charades_games.py -q
```

## Çiz ve Bil v1

`draw-guess` kataloğu dokuz dil ve dört yaş bandında 36 indirilebilir paket sunar.
Her pakette 200 çizim sahnesi, toplamda 7.200 kart bulunur. Her havuzdaki 40 kart
ilgili dilin kültürel karakter ve uğraşlarını kullanır. Küçük yaş grubunda şekil
ipucu ve iki kat süre; diğer gruplarda artan zorluk, seri bonusu ve özel çizim
turları vardır.

```powershell
python tools/generate_draw_guess.py
python tools/build_draw_guess_games.py
python tools/build_draw_guess_games.py --check
python -m pytest tests/test_draw_guess_games.py -q
```

## Hikâye Macerası v1

`story-adventure` kataloğu dokuz dil ve dört yaş bandında 36 indirilebilir paket
sunar. Her pakette sistemin otomatik birleştirdiği 200 macera kartı, toplamda 7.200
kart bulunur. Her kart bir kahraman, mekân, eşya, görev ve sürpriz taşır; havuzdaki
40 kart ilgili dilin kültürel karakterlerini kullanır. Tek anlatıcı, aile zinciri,
60 saniyelik hızlı oyun ve sürprizi sonradan açılan oyun seçenekleri bulunur.

```powershell
python tools/generate_story_adventure.py
python tools/build_story_adventure_games.py
python tools/build_story_adventure_games.py --check
python -m pytest tests/test_story_adventure_games.py -q
```

## Kelime Avı v1

`word-hunt` kataloğu dokuz dil ve dört yaş bandında 36 indirilebilir paket sunar.
Her pakette 200 karışık harf bulmacası, toplamda 7.200 bulmaca bulunur. Sistem
istenen sayıda bulmacayı havuzdan otomatik seçer. Küçük yaşta ilk harf ipucu ve
daha uzun süre; büyük yaşlarda artan yanıltıcı harfler bulunur. Her dilin kendine
özgü harfleri ve kültürel kelimeleri değiştirilmeden korunur.

```powershell
python tools/generate_word_hunt.py
python tools/build_word_hunt_games.py
python tools/build_word_hunt_games.py --check
python -m pytest tests/test_word_hunt_games.py -q
```
