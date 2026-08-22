# Bilgi Yarışması v2 — karma genel kültür hazırlık raporu

> Durum: Otomatik kalite kapılarından geçen, indirilebilir veri paketleri.
> İnsan onayı yayın için beklenmez; katalog kaydı, içeriğin AI destekli
> üretildiğini açıkça korur.

## Kapsam

- 9 dil: `tr`, `en`, `de`, `es`, `fr`, `pt`, `ru`, `ja`, `ko`
- 4 yaş bandı: 5–7, 8–11, 12–14, 15–18
- 36 paket, paket başına 200, toplam 7.200 soru
- Her 200 soruda tam olarak:
  - 40 coğrafya
  - 60 insanlar ve kültür (tarih, sanat, edebiyat, bilim ve spor kişileri)
  - 50 matematik ve mantık
  - 50 bilim, doğa ve teknoloji
- Aynı konu ailesi arka arkaya gelmez. Soru sırası her havuzda konular
  arasında geçiş yapar.
- Her dilde en az 40 kültür-yerel soru vardır. Kişi ve ülke seçimleri dilin
  kültür çevresine göre değiştiği için dokuz dil aynı havuzun çevirisi değildir.

## Kaynaklar

- Ülke, başkent ve kıta olguları: dondurulmuş çok dilli Wikidata anık görüntüsü.
- Tarihî ve güncel olmayan kişi bilgileri: AliKa'nın dondurulmuş çok dilli
  Wikidata kişi anık görüntüsü.
- Matematik ve mantık: yaş bandına göre belirlenimci işlemler; Khan Academy
  matematik kaynağına bağlanır.
- Elementler: IUPAC periyodik tablosu.
- Gezegenler: NASA Solar System Exploration.
- SI birimleri: BIPM SI Brochure.
- Temel bilim/doğa soruları: Smithsonian Science Education Center.

Uygulama ve normal paketleme sırasında internet kullanılmaz. Her soru HTTPS
kaynak bağı taşır; kaynaklar üretim zamanında dondurulmuş veriden okunur.

## Otomatik kalite kapıları

- Her havuz tam 200 soru ve dört benzersiz şık taşır.
- Soru kimlikleri ve soru metinleri havuz içinde benzersizdir.
- Doğru şık konumları 50/50/50/50 dengelidir.
- Coğrafya oranı %20 ile sınırlıdır; başkent–ülke–kıta soruları artık oyunun
  tamamını oluşturmaz.
- Konu dağılımı ve kültür kotası 36 havuzun tamamında test edilir.
- Üreteç çalıştırıldığında kaydedilmiş 7.200 soruyu bayt düzeyinde yeniden
  oluşturur.
- 36 arşiv veri-only `.alika-game` biçimindedir; katalog SHA-256 ve boyutlarını
  kaydeder.
- İçerik sürümü `2` yapıldı; kurulu eski coğrafya paketleri güncelleme olarak
  algılanabilir.

## Açık sınır

Kişi açıklamaları dondurulmuş Wikidata etiketlerinden gelir. Otomatik testler
cevabın soruda görünmesini ve yinelenen soruları engeller; ancak bazı meslek
adları günlük dilde beklenenden daha özel olabilir. Bu durum paketin teknik
yayınını durdurmaz ve sonraki içerik sürümlerinde sadeleştirilebilir.
