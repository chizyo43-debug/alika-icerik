#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MAT.5.3.5 ve MAT.5.3.6'da kalıp tekrarını figür-öncelikli sorularla değiştirir.

İki kusur aynı kayıtlarda buluşuyor:

  * Kalıp tekrarı (§11.9): "Bir düzlem şeklinin çokgen olması için…" dört kez,
    "Eşkenar üçgen ile kare için ortak özellik…" dört kez, "Çokgenlerin kenar
    ve köşe sayılarıyla ilgili…" üç kez yazılmış. Bunlar tek soru.
  * Figür açığı (kural 42): iki kazanımda 0/21 figür.

figure_spec 1.2.0 `shape/polygon` için `sides` alanını getirdiği için artık
çokgen sadık biçimde çizilebiliyor ve iki kusur tek işlemde kapanıyor.

FİGÜR CEVABI VERMEZ, VERİ VERİR. Ayrım şudur: figürden kenar sayısını SAYMAK
sorunun verisidir; aranan değer hâlâ hesaplanmalı ya da bilinmelidir.
Bu yüzden "kaç köşesi vardır?" biçimindeki yedi soruya figür EKLENMEDİ —
orada çocuk şekli sayar ve soru biter. Ölçme değil, resme bakma olur.

Doğru cevap konumu her kayıtta KORUNUR: paket dağılımı 125/125/125/125 ve
soru değiştirirken onu bozmak, düzeltilmiş bir ölçütü sessizce geri almaktır.

Kullanım:
    python tools/regen_mat_5_3_5_5_3_6.py            # yalnız rapor
    python tools/regen_mat_5_3_5_5_3_6.py --yaz
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "matematik" / "matematik-tum.jsonl"

AD = {3: "üçgen", 4: "dörtgen", 5: "beşgen", 6: "altıgen",
      7: "yedigen", 8: "sekizgen", 9: "dokuzgen", 10: "ongen"}


def yeni(kok, kenar, siklar, dogru_metin, gerekceler, aciklama, zorluk):
    """Tek bir figür-öncelikli soru tanımı."""
    return {"kok": kok, "kenar": kenar, "siklar": siklar,
            "dogru": dogru_metin, "gerekce": gerekceler,
            "aciklama": aciklama, "zorluk": zorluk}


# Değiştirilecek soru kimliği → yeni içerik.
YENILER = {
"tr.g05.mat.5-3-5.q003": yeni(
 "Verilen şekle göre, çizilen çokgenin adı nedir?", 7,
 ["Yedigen", "Altıgen", "Sekizgen", "Beşgen"], "Yedigen",
 {"Altıgen": "Bir kenarı saymayı atlamış: altıgenin altı kenarı vardır.",
  "Sekizgen": "Bir kenarı iki kez saymış: sekizgenin sekiz kenarı vardır.",
  "Beşgen": "Köşeleri değil kenarları saymış ama iki kenarı birleşik "
            "görmüş; beşgenin beş kenarı vardır."},
 "Şekildeki kapalı kırık çizgi yedi doğru parçasından oluşur; yedi kenarlı "
 "çokgene yedigen denir.",
 "Tek adımlı görünür ama sayma dikkat ister: şeklin kenarları eşit "
 "uzunlukta olduğu için birini atlamak kolaydır ve çeldiriciler bir eksik "
 "ile bir fazla saymadır."),

"tr.g05.mat.5-3-5.q008": yeni(
 "Verilen şekle göre, bu çokgene bir kenar daha eklenirse yeni şeklin adı "
 "ne olur?", 5,
 ["Altıgen", "Beşgen", "Dörtgen", "Yedigen"], "Altıgen",
 {"Beşgen": "Şeklin şu anki adını yazmış; eklenen kenarı hesaba katmamış.",
  "Dörtgen": "Kenar eklemek yerine çıkarmış: bir kenar azalsa dörtgen olurdu.",
  "Yedigen": "Bir yerine iki kenar eklemiş."},
 "Şekilde beş kenar vardır; bir kenar eklenince altı kenarlı çokgen, yani "
 "altıgen oluşur.",
 "İki adım gerekir: önce şekildeki kenar sayısını saymak, sonra bir "
 "artırıp yeni adı bulmak. Çeldiriciler saymayı doğru yapıp adımı "
 "atlayan ve yönü ters uygulayan öğrencidir."),

"tr.g05.mat.5-3-5.q013": yeni(
 "Verilen şekle göre, çizilen çokgenin kenar sayısı bir üçgenin kenar "
 "sayısından kaç fazladır?", 6,
 ["3", "6", "9", "2"], "3",
 {"6": "Çokgenin kenar sayısını yazmış; karşılaştırmayı yapmamış.",
  "9": "Çıkarma yerine toplama yapmış: 6 + 3 = 9.",
  "2": "Üçgenin kenar sayısını dört sanmış: 6 − 4 = 2."},
 "Şekildeki çokgenin altı kenarı vardır; üçgenin üç kenarı olduğuna göre "
 "fark 6 − 3 = 3'tür.",
 "İki adım gerekir: şekilden kenar sayısını okumak ve üçgenin kenar "
 "sayısıyla farkını almak. Çeldiriciler işlemi atlayan, yanlış işlem seçen "
 "ve ön bilgiyi yanlış hatırlayan öğrencidir."),

"tr.g05.mat.5-3-5.q018": yeni(
 "Verilen şekle göre, çizilen çokgenin bütün kenarları 4 santimetre ise "
 "çevresi kaç santimetredir?", 5,
 ["20", "9", "16", "25"], "20",
 {"9": "Kenar sayısı ile kenar uzunluğunu toplamış: 5 + 4 = 9.",
  "16": "Bir kenarı saymayı atlamış: 4 × 4 = 16.",
  "25": "Kenar uzunluğu yerine kenar sayısını kullanmış: 5 × 5 = 25."},
 "Şekilde beş kenar vardır ve her biri 4 santimetredir; çevre "
 "5 × 4 = 20 santimetredir.",
 "İki adım gerekir: şekilden kenar sayısını saymak ve kenar uzunluğuyla "
 "çarpmak. Çeldiriciler toplama ile çarpmayı karıştıran, bir kenarı atlayan "
 "ve iki sayıyı birbirinin yerine koyan öğrencidir."),

"tr.g05.mat.5-3-6.q003": yeni(
 "Verilen şekle göre, çizilen düzgün çokgenin bütün kenarları 5 santimetre "
 "ise çevresi kaç santimetredir?", 6,
 ["30", "11", "25", "36"], "30",
 {"11": "Kenar sayısı ile kenar uzunluğunu toplamış: 6 + 5 = 11.",
  "25": "Bir kenarı saymayı atlamış: 5 × 5 = 25.",
  "36": "Kenar uzunluğu yerine kenar sayısını kullanmış: 6 × 6 = 36."},
 "Şekilde altı kenar vardır ve her biri 5 santimetredir; çevre "
 "6 × 5 = 30 santimetredir.",
 "İki adım gerekir: şekilden kenar sayısını okumak ve kenar uzunluğuyla "
 "çarpmak. Çeldiriciler işlemi karıştıran, eksik sayan ve iki niceliği "
 "birbirinin yerine koyan öğrencidir."),

"tr.g05.mat.5-3-6.q008": yeni(
 "Verilen şekle göre, çizilen düzgün çokgenin çevresi 36 santimetre ise bir "
 "kenarı kaç santimetredir?", 9,
 ["4", "9", "27", "45"], "4",
 {"9": "Kenar sayısını cevap olarak yazmış; bölme işlemini yapmamış.",
  "27": "Bölme yerine çıkarma yapmış: 36 − 9 = 27.",
  "45": "Bölme yerine toplama yapmış: 36 + 9 = 45."},
 "Şekilde dokuz kenar vardır ve düzgün çokgende kenarlar eşittir; "
 "36 ÷ 9 = 4 santimetre.",
 "İki adım gerekir: şekilden kenar sayısını saymak ve çevreyi bu sayıya "
 "bölmek. Çeldiriciler bölmeyi atlayan ve yanlış işlem seçen öğrencidir; "
 "üçü de şekilden okunan 9 sayısını kullandığı için birbirine yakındır."),

"tr.g05.mat.5-3-6.q013": yeni(
 "Verilen şekle göre, çizilen çokgenin kenar sayısı ile köşe sayısının "
 "toplamı kaçtır?", 8,
 ["16", "8", "15", "64"], "16",
 {"8": "Yalnız kenar sayısını yazmış; köşe sayısını eklememiş.",
  "15": "Köşe sayısını kenar sayısından bir eksik sanmış: 8 + 7 = 15.",
  "64": "Toplama yerine çarpma yapmış: 8 × 8 = 64."},
 "Çokgende kenar sayısı ile köşe sayısı eşittir; şekilde sekiz kenar "
 "olduğuna göre toplam 8 + 8 = 16'dır.",
 "İki adım gerekir: şekilden kenar sayısını okumak ve kenar ile köşe "
 "sayısının eşit olduğu bilgisini kullanmak. Çeldiriciler bu eşitliği "
 "bilmeyen ve işlemi karıştıran öğrencidir."),

"tr.g05.mat.5-3-6.q005": yeni(
 "Verilen şekle göre, çizilen düzgün çokgenin bir kenarı 7 santimetre ise "
 "çevresi kaç santimetredir?", 4,
 ["28", "11", "21", "49"], "28",
 {"11": "Kenar sayısı ile kenar uzunluğunu toplamış: 4 + 7 = 11.",
  "21": "Bir kenarı saymayı atlamış: 3 × 7 = 21.",
  "49": "Kenar uzunluğu yerine kenar sayısını kullanmış: 7 × 7 = 49."},
 "Şekilde dört kenar vardır ve her biri 7 santimetredir; çevre "
 "4 × 7 = 28 santimetredir.",
 "İki adım gerekir: şekilden kenar sayısını saymak ve kenar uzunluğuyla "
 "çarpmak. Çeldiriciler toplama-çarpma karışıklığı, eksik sayma ve iki "
 "niceliği yer değiştirme yanılgılarını temsil eder."),

"tr.g05.mat.5-3-6.q010": yeni(
 "Verilen şekle göre, kenarları eşit uzunlukta olan bu düzgün çokgenin adı "
 "nedir?", 10,
 ["Ongen", "Dokuzgen", "Sekizgen", "Yedigen"], "Ongen",
 {"Dokuzgen": "Bir kenarı saymayı atlamış: dokuzgenin dokuz kenarı vardır.",
  "Sekizgen": "İki kenarı saymayı atlamış: sekizgenin sekiz kenarı vardır.",
  "Yedigen": "Kenarları ikişerli gruplayarak saymış; yedigenin yedi kenarı "
             "vardır."},
 "Şekildeki kapalı kırık çizgi on doğru parçasından oluşur; on kenarlı "
 "çokgene ongen denir.",
 "Kenar sayısı arttıkça sayma hatası olasılığı da artar; çeldiriciler bir, "
 "iki ve üç eksik saymayı temsil eder, bu yüzden birbirine yakındır."),
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
    eksik = [kid for kid in YENILER if kid not in indeks]
    if eksik:
        print(f"bulunamayan kimlik: {eksik}")
        return 1

    degisen = 0
    for kid, y in YENILER.items():
        q = indeks[kid]
        dogru_konum = q["correct"]          # dağılım korunur

        siklar = list(y["siklar"])
        assert len(set(siklar)) == 4, f"{kid}: şık tekrarı"
        assert y["dogru"] in siklar, f"{kid}: doğru şık listede yok"

        # Doğru şıkkı özgün konumuna taşı, gerekçeleri şıklarla birlikte diz.
        siklar.remove(y["dogru"])
        sirali = siklar[:dogru_konum] + [y["dogru"]] + siklar[dogru_konum:]
        gerekceler = []
        for i, s in enumerate(sirali):
            if i == dogru_konum:
                gerekceler.append(f"Doğru; {y['aciklama'][0].lower()}"
                                  f"{y['aciklama'][1:]}")
            else:
                assert s in y["gerekce"], f"{kid}: {s!r} için gerekçe yok"
                gerekceler.append(y["gerekce"][s])
        assert len(gerekceler) == 4

        kenar = y["kenar"]
        alt = (f"Kenarları eşit uzunlukta, {kenar} kenarlı kapalı bir çokgen.")
        ozet = hashlib.sha256(alt.encode("utf-8")).hexdigest()[:12]
        anahtar = f"{kid}.visual.{ozet}"
        etiketler[anahtar] = alt

        q["question"] = y["kok"]
        q["choices"] = sirali
        q["correct"] = dogru_konum
        q["distractorWhy"] = gerekceler
        q["explanation"] = y["aciklama"]
        q["difficultyReason"] = y["zorluk"]
        q["figure"] = {"kind": "shape", "type": "polygon", "sides": kenar,
                       "altTextKey": anahtar}
        q["reviewStatus"] = "pending"
        q["humanReviewed"] = False
        q["provenance"] = ("machine-generated:claude-opus-5:2026-08:"
                           "5-3-5-5-3-6-figur-oncelikli-yeniden-uretim")
        degisen += 1

    paket["labels"] = etiketler
    sorular = [k for k in kayitlar if k.get("type") == "question"]
    paket["contractPolicy"]["minFiguredQuestions"] = sum(
        1 for q in sorular if q.get("figure"))

    dagilim = [0, 0, 0, 0]
    for q in sorular:
        dagilim[q["correct"]] += 1
    print(f"  yeniden üretilen soru  {degisen}")
    print(f"  cevap dağılımı         {dagilim}")
    if dagilim != [125, 125, 125, 125]:
        print("UYARI: dağılım bozuldu")
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
