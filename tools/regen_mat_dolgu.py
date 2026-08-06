#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kural 39'un son dolgu değerlerini kapatır: '16 cm', '20 cm', '48 cm'.

Bu değerler DOLGU DEĞİLDİ. Üçü de gerçek bir yanılgının kendi hesabından
çıkıyordu: "yarı çevre yerine çevrenin tamamını hesaplamış: (7+3)×2 = 20",
"kenarları toplamak yerine çarpmış: 8×6 = 48". Değeri keyfî değiştirmek,
sayıyı önce seçip ifadeyi ona uydurmak olurdu — §11.2'de yasaklanan şey.

Kural 39 bir şıkkı yalnız pakette dört kereden çok geçip HİÇBİR soruda doğru
olmadığında işaretler; zararı öğrencinin "bu değer hiç doğru değil" diye
eleyebilmesidir. Doğru onarım değeri silmek değil, o değere pakette bir ev
bulmaktır.

İLK DENEMEDE YANLIŞ YAPTIM ve kaydı buraya bırakıyorum: '16 cm'yi doğru
yapmak için 5-4-1.q017'nin sayılarını değiştirdim, ama o sorunun cevabı
'14 cm' idi ve '14 cm' pakette dokuz kez çeldirici olarak geçiyordu. Bir
değeri kurtarırken başka bir değeri evsiz bıraktım ve uyarı yer değiştirdi.
Ders: değeri TAŞIMA, yeni ev AÇ.

Bu yüzden q017'ye dokunulmuyor. Üç ayrı soruya üç ev açılıyor:

  5-4-1.q002  yarı çevre 12 + 8            → '20 cm' doğru
  5-4-1.q011  kısa kenar 8 cm uzatılırsa   → '16 cm' doğru
  5-4-1.q003  bir kenarı 12 cm olan kare   → '48 cm' doğru
  5-4-2.q007  alan 288, bir kenar 12       → '24 cm' doğru

Bağış veren soru seçilirken cevabının pakette BAŞKA evi olmasına bakıldı:
5-4-2.q007'nin eski cevabı '10 cm' idi ve '10 cm' iki ayrı soruda daha doğru
cevap. Bunu gözetmeden ilk denememde 5-3-7.q013'ün cevabını 18'den 24'e
çevirmiştim ve '18 cm' evsiz kalıp uyarı yer değiştirmişti.

Doğru cevap konumu ve figürlü soru sayısı korunur.

Kullanım:
    python tools/regen_mat_dolgu.py --yaz
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "matematik" / "matematik-tum.jsonl"

YENILER = {
"tr.g05.mat.5-4-1.q002": {
 "kok": "Verilen şekle göre, kenarları 12 cm ve 8 cm olan bir dikdörtgenin "
        "yarı çevresi kaç santimetredir?",
 "fig": {"kind": "shape", "type": "rect", "dims": {"w": 12, "h": 8}},
 "alt": "Uzun kenarı 12 birim, kısa kenarı 8 birim olan bir dikdörtgen.",
 "siklar": ["20 cm", "4 cm", "40 cm", "96 cm"],
 "dogru": "20 cm",
 "gerekce": {
   "4 cm": "Kenarları toplamak yerine farklarını almış: 12 − 8 = 4.",
   "40 cm": "Yarı çevre yerine çevrenin tamamını hesaplamış: "
            "(12 + 8) × 2 = 40.",
   "96 cm": "Kenarları toplamak yerine çarpmış; çarpım alana aittir: "
            "12 × 8 = 96."},
 "aciklama": "Yarı çevre, komşu iki kenarın toplamıdır: 12 + 8 = 20 "
             "santimetre.",
 "zorluk": "Tek adımlı bir toplama ama çeldiriciler dört işlemin dördünü de "
           "temsil ediyor; hangisinin yarı çevreye ait olduğunu bilmek "
           "gerekir.",
},
"tr.g05.mat.5-4-1.q011": {
 "kok": "Bir dikdörtgenin kısa kenarı 8 cm uzatılırsa çevresi kaç "
        "santimetre artar?",
 "fig": None,
 "alt": None,
 "siklar": ["16 cm", "32 cm", "8 cm", "4 cm"],
 "dogru": "16 cm",
 "gerekce": {
   "32 cm": "Uzatmayı dört kenara birden uygulamış: 8 × 4 = 32; oysa yalnız "
            "karşılıklı iki kenar değişir.",
   "8 cm": "Uzatmayı bir kez saymış; dikdörtgende karşılıklı iki kenar "
           "birden uzar.",
   "4 cm": "Uzatmanın yarısını almış: 8 ÷ 2 = 4."},
 "aciklama": "Kısa kenar uzatılınca karşılıklı iki kenar birden uzar; çevre "
             "artışı 8 × 2 = 16 santimetredir.",
 "zorluk": "Kaç kenarın değiştiğini görmeyi gerektirir; üç çeldirici de "
           "kenar sayısını yanlış alan (dört, bir ve yarım) öğrenciyi "
           "temsil ettiği için birbirine yakındır.",
},
"tr.g05.mat.5-4-2.q007": {
 "kok": "Alanı 288 cm² ve bir kenarı 12 cm olan dikdörtgenin diğer kenarı "
        "kaç santimetredir?",
 "fig": None,
 "alt": None,
 "siklar": ["24 cm", "276 cm", "300 cm", "12 cm"],
 "dogru": "24 cm",
 "gerekce": {
   "276 cm": "Bölme yerine çıkarma yapmış: 288 − 12 = 276.",
   "300 cm": "Bölme yerine toplama yapmış: 288 + 12 = 300.",
   "12 cm": "Verilen kenarı yeniden yazmış; dikdörtgende komşu kenarlar "
            "eşit olmak zorunda değildir."},
 "aciklama": "Dikdörtgenin alanı komşu iki kenarın çarpımıdır; diğer kenar "
             "288 ÷ 12 = 24 santimetredir.",
 "zorluk": "Alan bağıntısını ters yönde kullanmayı gerektirir: çarpım "
           "biliniyor, çarpanlardan biri aranıyor. Çeldiriciler bölme "
           "yerine toplama ve çıkarma yapan öğrenciyi temsil eder.",
},
"tr.g05.mat.5-4-1.q003": {
 "kok": "Verilen şekle göre, bir kenarı 12 cm olan karenin çevresi kaç "
        "santimetredir?",
 "fig": {"kind": "shape", "type": "square", "dims": {"a": 12}},
 "alt": "Dört kenarı da 12 birim olan bir kare.",
 "siklar": ["48 cm", "24 cm", "144 cm", "12 cm"],
 "dogru": "48 cm",
 "gerekce": {
   "24 cm": "Yalnız iki kenarı toplamış: 12 + 12 = 24; karede dört kenar "
            "vardır.",
   "144 cm": "Kenarları çarpmış, yani alanı bulmuş: 12 × 12 = 144.",
   "12 cm": "Bir kenarın uzunluğunu yazmış; çevre bütün kenarların "
            "toplamıdır."},
 "aciklama": "Karede dört kenar da eşittir; çevre 4 × 12 = 48 santimetredir.",
 "zorluk": "Tek adımlı bir çarpma ama çeldiriciler alan ile çevreyi, iki "
           "kenar ile dört kenarı ayırt etmeyi gerektiriyor.",
},
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaz", action="store_true")
    ns = ap.parse_args(argv)

    kayitlar = [json.loads(s) for s in
                PAKET.read_text(encoding="utf-8").splitlines() if s.strip()]
    paket = next(k for k in kayitlar if k.get("type") == "pack")
    etiketler = dict(paket.get("labels") or {})
    indeks = {k.get("id"): k for k in kayitlar}

    for kid, y in YENILER.items():
        if kid not in indeks:
            print(f"bulunamadı: {kid}")
            return 1
        q = indeks[kid]
        konum = q["correct"]
        siklar = list(y["siklar"])
        assert len(set(siklar)) == 4, f"{kid}: şık tekrarı"
        siklar.remove(y["dogru"])
        sirali = siklar[:konum] + [y["dogru"]] + siklar[konum:]
        gerekceler = []
        for i, s in enumerate(sirali):
            if i == konum:
                gerekceler.append(
                    f"Doğru; {y['aciklama'][0].lower()}{y['aciklama'][1:]}")
            else:
                assert s in y["gerekce"], f"{kid}: {s!r} gerekçesi yok"
                gerekceler.append(y["gerekce"][s])

        q.update(question=y["kok"], choices=sirali, correct=konum,
                 distractorWhy=gerekceler, explanation=y["aciklama"],
                 difficultyReason=y["zorluk"],
                 reviewStatus="pending", humanReviewed=False,
                 provenance="machine-generated:claude-opus-5:2026-08:"
                            "kural39-deger-evi")
        if y["fig"]:
            ozet = hashlib.sha256(y["alt"].encode("utf-8")).hexdigest()[:12]
            anahtar = f"{kid}.visual.{ozet}"
            etiketler[anahtar] = y["alt"]
            fig = dict(y["fig"])
            fig["altTextKey"] = anahtar
            q["figure"] = fig
        else:
            q["figure"] = None

    # Yetim etiket bırakma: figürü değişen sorunun eski alt metin anahtarı
    # artık kullanılmıyorsa sözlükten çıkar (kural 25 / kural 51).
    kullanilan = set()

    def gez(v, ad=""):
        if isinstance(v, dict):
            for k2, alt in v.items():
                if k2 == "key" and isinstance(alt, str):
                    kullanilan.add(alt)
                elif k2 in ("labels", "sideLabels", "axisKeys") and isinstance(alt, dict):
                    kullanilan.update(x for x in alt.values() if isinstance(x, str))
                else:
                    gez(alt, k2)
        elif isinstance(v, list):
            for x in v:
                gez(x, ad)
        elif isinstance(v, str) and (ad.endswith("Key") or ad.endswith("Keys")):
            kullanilan.add(v)

    for k in kayitlar:
        if k.get("type") != "pack":
            gez(k.get("figure"))
    yetim = sorted(set(etiketler) - kullanilan)
    for a in yetim:
        del etiketler[a]

    paket["labels"] = etiketler
    sorular = [k for k in kayitlar if k.get("type") == "question"]
    paket["contractPolicy"]["minFiguredQuestions"] = sum(
        1 for q in sorular if q.get("figure"))
    dagilim = [0, 0, 0, 0]
    for q in sorular:
        dagilim[q["correct"]] += 1
    print(f"  yeniden üretilen soru  {len(YENILER)}")
    print(f"  silinen yetim etiket   {len(yetim)}")
    print(f"  figürlü soru           {paket['contractPolicy']['minFiguredQuestions']}")
    print(f"  cevap dağılımı         {dagilim}")
    if dagilim != [125, 125, 125, 125]:
        return 1

    if not ns.yaz:
        print("(yazmak için --yaz)")
        return 0
    PAKET.write_text(
        "\n".join(json.dumps(k, ensure_ascii=False) for k in kayitlar) + "\n",
        encoding="utf-8", newline="\n")
    print(f"yazıldı: {PAKET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
