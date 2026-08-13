# Bilgi Yarışması v1 — yayın hazırlık raporu

> Durum: **AI-only taslak; insan kültürel onayı yok.** Bu paketler teknik
> inceleme ve AliKa uyumluluk testi için hazırdır; insan onayı tamamlanmadan
> “final onaylı” etiketi alamaz.

## Kapsam

- 9 dil: `tr`, `en`, `de`, `es`, `fr`, `pt`, `ru`, `ja`, `ko`
- 4 yaş bandı: 5–7, 8–11, 12–14, 15–18
- 36 ayrı paket, paket başına 200, toplam 7.200 soru
- Her havuzda 54–58 dil-kültür çevresine öncelikli soru; kalanı küresel
  dünya/kültür coğrafyası
- 5–7 bandında tanınırlığı yüksek ülkeler öncelikli; 12–18
  bantlarında aynı kıtadan daha yakın çeldiriciler kullanılır

## Kaynak ve sınırlar

- Olgular Wikidata'nın çok dilli ülke, başkent ve kıta kayıtlarından
  yazar zamanında donduruldu; uygulama ve CI ağa çıkmaz.
- Ham kaynak anık görüntüsü `games/trivia/data/wikidata_countries.json`;
  her soru ayrıca ilgili Wikidata varlığına HTTPS kaynak bağı taşır.
- Güncel lider, nüfus, fiyat ve benzeri hızla eskiyen olgular üretilmez.
- Birden fazla başkenti olan devletler havuzdan çıkarılır; birden fazla
  kıtada gösterilen devletlerden kıta sorusu üretilmez.
- Wikidata etiketi doğrudan cümleye girmez. `tools/trivia_language.py`
  etiketi görünen ada indirir (resmî uzun ad, idari ek, bozuk etiket) ve
  cümlenin istediği çekimli/edatlı biçimi üretir. Anık görüntü ham kalır.
- Kıta etiketleri altı kanona eşlenir. Wikidata'nın dile göre değişen
  bölümlemesi (`Okyanusya` ↔ `Ada Okyanusyası`, `Океания` ↔ `Австралия и
  Океания`) aynı soruda iki savunulabilir doğru üretiyordu. Avrasya bir kıta
  adı olarak sorulmaz ve çeldirici havuzunda yer almaz.
- Başkenti geçişte/yerelleştirilmemiş ya da siyasi olarak tartışmalı
  devletlerden (Ekvator Ginesi, İsrail) başkent ve ülke sorusu üretilmez;
  kıta sorusuna girerler. Ekvator Ginesi için Ciudad de la Paz'ın başkent
  ilanı ve bir yıllık kurum taşıma süresi [2 Ocak 2026 tarihli resmî
  karara](https://www.guineaecuatorialpress.com/index.php/noticias/decreto_ley_por_el_que_se_declara_la_ciudad_de_la_paz_djibloho_capital_de_la_republica_de_guinea_ecuatorial)
  dayanır. Adı başkentiyle aynı veya doğrudan şehir türevi olan devletler
  (Monako, Lüksemburg, Cibuti, Vatikan) de cevabı ele verdiği için bu iki
  yönün dışındadır.
- V1 genel kültürünün odağı dünya ve kültürel coğrafyadır. Sanat,
  bilim, spor ve edebiyat kategorileri ayrı kaynak/insan inceleme dalgasıdır.

## Otomatik kapılar

- Her havuz tam 200 soru ve dört benzersiz şık taşır.
- Soru kimlikleri, metinler ve şıklar havuz içinde benzersizdir.
- Doğru şık konumu her havuzda dengelidir.
- Ham `Q...` varlık kimliği, bozuk Unicode ve cevabı anmayan açıklama yoktur.
- Arşivler deterministiktir; `catalog.json` SHA-256 ve boyutları kaydeder.
- 36/36 arşiv AliKa `windows/library/game_package.py` gerçek okuyucusunda
  kabul edilmiş, her birinden 200 soru geri okunmuştur.

## Bilinen borç

- Başkent ve ülke yönü, kültür-yerel ülkelerde hâlâ aynı havuzda
  eşleşiyor: havuz başına 17–20 soru, bir başka sorunun cevabını veriyor.
  Kasıtlı: paket başına ≥40 yerel soru kapısı yalnız 20 yerel ülkeden
  besleniyor, çift yön kaldırılırsa kota dolmuyor. Küresel ülkelerin
  tamamı tek yönde soruluyor; eşleşme 60'tan 17–20'ye indi. Kalıcı çözüm
  yerel havuzu genişletmek ya da dördüncü bir soru türü eklemektir.
- Havuz hâlâ üç cümle kalıbından üretiliyor (100 başkent + 60 ülke +
  40 kıta). Kalıp çeşitliliği v2'nin konusudur.

## İnsan inceleme kapısı

Her dil için ana dili o dil olan veya o dilde ileri yetkin bir inceleyici,
dört havuzun en az %10 belirlenimci örneklemini okuyacak; yanlış olgu,
doğal olmayan dil, yaşa uygunsuzluk ve hassas kültürel ifade sıfır olmadan
`human_approved` değeri `true` yapılmayacaktır.
