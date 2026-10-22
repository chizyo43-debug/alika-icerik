# AliKa oyun paketleri

Bu dizin AliKa'nın yalnız veri taşıyan `.alika-game` paketlerini barındırır.
Paketler kod, eklenti, dış URL veya çalıştırılabilir dosya içermez.

AliKa TV'de dört oyun vardır. Işık Hızı Rallisi ile Uzay İstasyonu uygulamanın
içinde gelir ve paket gerektirmez; aşağıdaki iki oyun bu depodan indirilir.
Eski oyun paketleri 2026-10-21'de kaldırıldı; geçmişleri Git'te durur.

Kapaklar (`games/visuals/<oyun>/game_art.webp`, 960×540, yazısız) AliKa TV'nin uzay
görünümündedir ve TV ana menüsündeki oyun kartı amblemleriyle aynı çizimden üretilir
(uygulama deposunda `TvGameCoverArtTest`, 2026-10-22). Paket teması da aynı paleti taşır.

## Çarkıfelek v1

`word-wheel` kataloğu dokuz dil ve dört yaş bandında 36 paket sunar. Her pakette
sistemin tur başında otomatik seçtiği tam 200 kelime bulmacası vardır; toplam
7.200 bulmaca bulunur. Ortak ekrana cevap değil, yalnız kategori, ipucu ve kapalı
harf tahtası gider.

```powershell
python tools/generate_word_wheel_geography.py  # kaynak: games/word-wheel/data
python tools/build_word_wheel_games.py
python tools/build_word_wheel_games.py --check
python -m pytest tests/test_word_wheel_games.py -q
```

## İsim Şehir v1

`name-city` kataloğu dokuz dil ve dört yaş bandında 36 indirilebilir paket sunar.
Her pakette 200 harf–kategori turu, toplamda 7.200 tur vardır. İsim ve şehir her
turda korunur; yaş büyüdükçe kategori sayısı artar ve süre kısalır. Japonca kana
satırlarını, Korece ise ilk ses işaretlerini kullanır. Ortak cevaplar elenir,
tartışmalı cevaplar aile oylamasıyla çözülür.

```powershell
python tools/generate_name_city_games.py
python tools/build_name_city_games.py
python tools/build_name_city_games.py --check
python -m pytest tests/test_name_city_games.py -q
```
