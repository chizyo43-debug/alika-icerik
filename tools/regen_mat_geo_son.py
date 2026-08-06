#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometri ailelerinin son partisi: figür açığı + dolgu çeldirici birlikte.

İki uyarı aynı kayıtlarda buluşuyor, bu yüzden tek işlemde kapanır:

  * kural 42 — altı kazanımda figür oranı %30'un altında
  * kural 39 — altı ölçü değeri ('20 cm' ×7, '16 cm' ×6 …) pakette dolaşıyor
    ve hiçbir soruda doğru değil; öğrenci kalıbı görüp eliyor, şans %25'ten
    yukarı çıkıyor ve ölçme geçersizleşiyor

Yeniden üretilen her soruda çeldirici, adlandırılmış bir yanılgının kendi
hesabından çıkar; sayı önce seçilip ifade ona uydurulmaz (§11.2).

Doğru cevap konumu korunur: paket dağılımı 125/125/125/125.

Kullanım:
    python tools/regen_mat_geo_son.py            # yalnız rapor
    python tools/regen_mat_geo_son.py --yaz
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "matematik" / "matematik-tum.jsonl"


def S(kok, fig, alt, siklar, dogru, gerekce, aciklama, zorluk):
    return dict(kok=kok, fig=fig, alt=alt, siklar=siklar, dogru=dogru,
                gerekce=gerekce, aciklama=aciklama, zorluk=zorluk)


def acik(d):
    return {"kind": "angle", "degrees": d}


def dikd(w, h):
    return {"kind": "shape", "type": "rect", "dims": {"w": w, "h": h}}


def cokgen(n):
    return {"kind": "shape", "type": "polygon", "sides": n}


def izgara(c, r):
    return {"kind": "grid", "cols": c, "rows": r}


def grafik(adlar, degerler):
    return {"kind": "chart", "style": "bar", "categoryKeys": adlar,
            "values": degerler}


YENILER = {
# ---- MAT.5.3.1 temel geometrik çizimler (+3) ----
"tr.g05.mat.5-3-1.q004": S(
 "Verilen şekle göre, açıölçerle ölçülen bu açıyı çizmek için açıölçer "
 "kaç dereceyi gösterecek biçimde işaretlenmelidir?",
 acik(65), "Ortak bir köşeden çıkan iki ışın; ikinci ışın yatay başlangıç "
 "ışınından 65 derece döndürülmüş olarak çizilmiştir.",
 ["65", "115", "25", "130"], "65",
 {"115": "Açının bütünlerini almış: 180 − 65 = 115.",
  "25": "Açının tümlerini almış: 90 − 65 = 25.",
  "130": "Ölçüyü iki katına çıkarmış: 65 × 2 = 130."},
 "Açıölçer köşeye yerleştirilir ve ışının geçtiği bölme okunur; şekildeki "
 "açı 65 derecedir, çizim de aynı bölmeden işaretlenir.",
 "Tek adımlı görünse de üç çeldirici birbirine yakın: tümler, bütünler ve "
 "iki kat alma yanılgıları aynı sayıdan türediği için ayırt etmek "
 "açıölçerin ne okuduğunu bilmeyi gerektirir."),

"tr.g05.mat.5-3-1.q009": S(
 "Verilen şekle göre, bu açının açıortayı çizilirse oluşan iki açıdan her "
 "biri kaç derece olur?",
 acik(80), "Ortak bir köşeden çıkan iki ışın; ikinci ışın yatay başlangıç "
 "ışınından 80 derece döndürülmüş olarak çizilmiştir.",
 ["40", "80", "160", "10"], "40",
 {"80": "Açıortayın açıyı ikiye böldüğünü gözden kaçırmış; ölçüyü aynen "
        "yazmış.",
  "160": "Bölme yerine çarpma yapmış: 80 × 2 = 160.",
  "10": "Tümlerini ikiye bölmüş: (90 − 80) ÷ 1 = 10."},
 "Açıortay açıyı iki eş parçaya böler; 80 ÷ 2 = 40 derece.",
 "İki adım gerekir: şekilden açı ölçüsünü okumak ve açıortayın açıyı iki eş "
 "parçaya böldüğünü uygulamak. Çeldiriciler adımı atlayan, işlemi ters "
 "çeviren ve yanlış ön bilgiyi kullanan öğrencidir."),

"tr.g05.mat.5-3-1.q014": S(
 "Verilen şekle göre, gönye kullanılarak çizilecek dik açı bu açıdan kaç "
 "derece büyüktür?",
 acik(55), "Ortak bir köşeden çıkan iki ışın; ikinci ışın yatay başlangıç "
 "ışınından 55 derece döndürülmüş olarak çizilmiştir.",
 ["35", "55", "125", "145"], "35",
 {"55": "Şekildeki açıyı cevap olarak yazmış; karşılaştırmayı yapmamış.",
  "125": "Dik açı yerine doğru açıdan çıkarmış: 180 − 55 = 125.",
  "145": "Toplama yapmış: 90 + 55 = 145."},
 "Gönyenin dik köşesi 90 derecedir; şekildeki açı 55 derece olduğuna göre "
 "fark 90 − 55 = 35 derecedir.",
 "İki adım gerekir: şekilden ölçüyü okumak ve dik açıyla farkını almak. "
 "Çeldiriciler işlemi atlayan, dik açı ile doğru açıyı karıştıran ve "
 "çıkarma yerine toplama yapan öğrencidir."),

# ---- MAT.5.3.5 çokgenleri tanıma (+3) ----
"tr.g05.mat.5-3-5.q004": S(
 "Verilen şekle göre, çizilen çokgenin köşe sayısı bir dörtgenin köşe "
 "sayısından kaç fazladır?",
 cokgen(9), "Kenarları eşit uzunlukta, dokuz kenarlı kapalı bir çokgen.",
 ["5", "9", "13", "4"], "5",
 {"9": "Çokgenin köşe sayısını yazmış; karşılaştırmayı yapmamış.",
  "13": "Çıkarma yerine toplama yapmış: 9 + 4 = 13.",
  "4": "Dörtgenin köşe sayısını yazmış; hangi sayıdan çıkarılacağını "
       "karıştırmış."},
 "Çokgende köşe sayısı kenar sayısına eşittir; şekildeki çokgenin dokuz "
 "köşesi, dörtgenin dört köşesi vardır: 9 − 4 = 5.",
 "Üç şey gerekir: şekilden kenar sayısını saymak, kenar ile köşe sayısının "
 "eşitliğini bilmek ve farkı almak. Çeldiriciler bu üç adımdan birini "
 "atlayan öğrenciyi temsil eder."),

"tr.g05.mat.5-3-5.q009": S(
 "Verilen şekle göre, kenarları eşit uzunlukta olan bu kapalı şeklin adı "
 "nedir?",
 cokgen(6), "Kenarları eşit uzunlukta, altı kenarlı kapalı bir çokgen.",
 ["Altıgen", "Beşgen", "Yedigen", "Dörtgen"], "Altıgen",
 {"Beşgen": "Bir kenarı saymayı atlamış: beşgenin beş kenarı vardır.",
  "Yedigen": "Bir kenarı iki kez saymış: yedigenin yedi kenarı vardır.",
  "Dörtgen": "Karşılıklı kenarları tek kenar sayarak eşleştirmiş."},
 "Şekildeki kapalı kırık çizgi altı doğru parçasından oluşur; altı kenarlı "
 "çokgene altıgen denir.",
 "Sayma dikkat ister çünkü kenarlar eşit uzunluktadır ve birini atlamak "
 "kolaydır; çeldiriciler bir eksik, bir fazla ve eşleştirerek sayma "
 "yanılgılarını temsil eder."),

"tr.g05.mat.5-3-5.q014": S(
 "Verilen şekle göre, çizilen çokgenin bütün kenarları 3 santimetre ise "
 "çevresi kaç santimetredir?",
 cokgen(7), "Kenarları eşit uzunlukta, yedi kenarlı kapalı bir çokgen.",
 ["21", "10", "18", "49"], "21",
 {"10": "Kenar sayısı ile kenar uzunluğunu toplamış: 7 + 3 = 10.",
  "18": "Bir kenarı saymayı atlamış: 6 × 3 = 18.",
  "49": "Kenar uzunluğu yerine kenar sayısını kullanmış: 7 × 7 = 49."},
 "Şekilde yedi kenar vardır ve her biri 3 santimetredir; çevre "
 "7 × 3 = 21 santimetredir.",
 "İki adım gerekir: şekilden kenar sayısını saymak ve kenar uzunluğuyla "
 "çarpmak. Çeldiriciler toplama-çarpma karışıklığı, eksik sayma ve iki "
 "niceliği yer değiştirme yanılgılarını temsil eder."),

# ---- MAT.5.3.6 çokgenlerin özellikleri (+2) ----
"tr.g05.mat.5-3-6.q017": S(
 "Verilen şekle göre, çizilen düzgün çokgenin çevresi 40 santimetre ise bir "
 "kenarı kaç santimetredir?",
 cokgen(8), "Kenarları eşit uzunlukta, sekiz kenarlı kapalı bir çokgen.",
 ["5", "8", "32", "48"], "5",
 {"8": "Kenar sayısını cevap olarak yazmış; bölme işlemini yapmamış.",
  "32": "Bölme yerine çıkarma yapmış: 40 − 8 = 32.",
  "48": "Bölme yerine toplama yapmış: 40 + 8 = 48."},
 "Şekilde sekiz kenar vardır ve düzgün çokgende kenarlar eşittir; "
 "40 ÷ 8 = 5 santimetre.",
 "İki adım gerekir: şekilden kenar sayısını saymak ve çevreyi bu sayıya "
 "bölmek. Üç çeldirici de şekilden okunan 8 sayısını kullandığı için "
 "birbirine yakındır ve işlem seçimini bilmeyi gerektirir."),

"tr.g05.mat.5-3-6.q012": S(
 "Verilen şekle göre, çizilen çokgene iki kenar daha eklenirse kenar sayısı "
 "kaç olur?",
 cokgen(5), "Kenarları eşit uzunlukta, beş kenarlı kapalı bir çokgen.",
 ["7", "5", "3", "10"], "7",
 {"5": "Şeklin şu anki kenar sayısını yazmış; eklemeyi yapmamış.",
  "3": "Eklemek yerine çıkarmış: 5 − 2 = 3.",
  "10": "Toplama yerine çarpma yapmış: 5 × 2 = 10."},
 "Şekilde beş kenar vardır; iki kenar eklenince 5 + 2 = 7 olur.",
 "İki adım gerekir: şekilden kenar sayısını okumak ve iki artırmak. "
 "Çeldiriciler adımı atlayan, yönü ters uygulayan ve işlemi karıştıran "
 "öğrenciyi temsil eder."),

# ---- MAT.5.3.7 çemberlerle üçgen inşası (+3) ----
"tr.g05.mat.5-3-7.q004": S(
 "Verilen şekle göre, eş açıklıklı iki çemberle oluşturulan bu eşkenar "
 "üçgenin çevresi kaç santimetredir?",
 {"kind": "shape", "type": "triangle", "dims": {"a": 9, "b": 9, "c": 9}},
 "Üç kenarı da 9 santimetre olan bir eşkenar üçgen.",
 ["27", "18", "81", "12"], "27",
 {"18": "Yalnız iki kenarı toplamış: 9 + 9 = 18.",
  "81": "Kenarları çarpmış: 9 × 9 = 81.",
  "12": "Kenar sayısı ile kenar uzunluğunu toplamış: 9 + 3 = 12."},
 "Eşkenar üçgenin üç kenarı da eşittir; çevre 3 × 9 = 27 santimetredir.",
 "İki adım gerekir: şekilden kenar uzunluğunu okumak ve eşkenar üçgende üç "
 "kenarın eşit olduğunu kullanmak. Çeldiriciler bir kenarı atlayan, işlemi "
 "karıştıran ve iki niceliği toplayan öğrenciyi temsil eder."),

"tr.g05.mat.5-3-7.q009": S(
 "Verilen şekle göre, eş açıklıklı iki çemberle oluşturulan bu üçgenin bir "
 "iç açısı kaç derecedir?",
 {"kind": "shape", "type": "triangle", "dims": {"a": 5, "b": 5, "c": 5}},
 "Üç kenarı da 5 santimetre olan bir eşkenar üçgen.",
 ["60", "90", "180", "45"], "60",
 {"90": "Her üçgende bir dik açı bulunduğunu sanmış.",
  "180": "Üç açının toplamını tek açı sanmış.",
  "45": "İç açılar toplamını dörde bölmüş: 180 ÷ 4 = 45."},
 "Şekildeki üçgenin üç kenarı eşittir, yani eşkenardır; eşkenar üçgende üç "
 "iç açı da eşit olduğundan her biri 180 ÷ 3 = 60 derecedir.",
 "İki adım gerekir: şekilden üçgenin eşkenar olduğunu görmek ve iç açılar "
 "toplamını üçe bölmek. Çeldiriciler üçgen türünü ayırt edemeyen ve "
 "toplamı tek açıyla karıştıran öğrenciyi temsil eder."),

"tr.g05.mat.5-3-7.q019": S(
 "Verilen şekle göre, eş açıklıklı iki çemberle oluşturulan bu eşkenar "
 "üçgenin iki kenarının toplamı kaç santimetredir?",
 {"kind": "shape", "type": "triangle", "dims": {"a": 8, "b": 8, "c": 8}},
 "Üç kenarı da 8 santimetre olan bir eşkenar üçgen.",
 ["16", "24", "8", "64"], "16",
 {"24": "Üç kenarı toplamış, yani çevreyi bulmuş: 3 × 8 = 24.",
  "8": "Tek kenarın uzunluğunu yazmış; ikinci kenarı eklememiş.",
  "64": "Toplama yerine çarpma yapmış: 8 × 8 = 64."},
 "Şekildeki üçgenin her kenarı 8 santimetredir; iki kenarın toplamı "
 "8 + 8 = 16 santimetredir.",
 "Tek adımlı görünse de çeldiriciler yakın: çevre ile iki kenarın toplamını "
 "karıştırmak ve tek kenarda kalmak, sorunun kaç kenar istediğini okumayı "
 "gerektirir."),

# ---- MAT.5.4.1 çevre ve dikdörtgenin kenarları (+2) ----
"tr.g05.mat.5-4-1.q010": S(
 "Verilen şekle göre, birim karelerden oluşan bu dikdörtgenin çevresi kaç "
 "birimdir?",
 izgara(7, 3), "Yedi sütun ve üç satırdan oluşan birim kare ızgarası; "
 "kareler eşit büyüklüktedir.",
 ["20", "21", "10", "14"], "20",
 {"21": "Çevre yerine alanı hesaplamış: 7 × 3 = 21.",
  "10": "Yalnız iki kenarı toplamış: 7 + 3 = 10.",
  "14": "Uzun kenarı iki kez almış ama kısa kenarları unutmuş: 7 × 2 = 14."},
 "Şekilde uzun kenar 7, kısa kenar 3 birimdir; çevre (7 + 3) × 2 = 20 "
 "birimdir.",
 "İki adım gerekir: şekilden kenar uzunluklarını saymak ve çevre bağıntısını "
 "uygulamak. Çeldiriciler alan ile çevreyi karıştıran, yarım çevrede kalan "
 "ve bir kenar çiftini unutan öğrenciyi temsil eder."),

"tr.g05.mat.5-4-1.q018": S(
 "Verilen şekle göre, birim karelerden oluşan bu dikdörtgenin uzun kenarı "
 "kısa kenarından kaç birim fazladır?",
 izgara(9, 4), "Dokuz sütun ve dört satırdan oluşan birim kare ızgarası; "
 "kareler eşit büyüklüktedir.",
 ["5", "13", "36", "26"], "5",
 {"13": "Çıkarma yerine toplama yapmış: 9 + 4 = 13.",
  "36": "Kenarları çarpmış, yani alanı bulmuş: 9 × 4 = 36.",
  "26": "Çevreyi hesaplamış: (9 + 4) × 2 = 26."},
 "Şekilde uzun kenar 9, kısa kenar 4 birimdir; fark 9 − 4 = 5 birimdir.",
 "İki adım gerekir: şekilden iki kenarı saymak ve farkı almak. Çeldiriciler "
 "işlemi karıştıran, alan hesaplayan ve çevre hesaplayan öğrenciyi temsil "
 "eder; üçü de aynı iki sayıdan türediği için birbirine yakındır."),

# ---- MAT.5.5.2 veriyi yorumlama (+5) ----
"tr.g05.mat.5-5-2.q004": S(
 "Verilen grafiğe göre, en çok seçilen etkinlik ile en az seçilen etkinlik "
 "arasındaki fark kaç öğrencidir?",
 grafik(["resim", "muzik", "spor", "tiyatro"], [12, 5, 9, 3]),
 "Sütun grafiği; kategoriler ve sıklıkları: resim 12, müzik 5, spor 9, "
 "tiyatro 3.",
 ["9", "12", "3", "15"], "9",
 {"12": "En çok seçilenin sıklığını yazmış; farkı almamış.",
  "3": "En az seçilenin sıklığını yazmış; farkı almamış.",
  "15": "Çıkarma yerine toplama yapmış: 12 + 3 = 15."},
 "Grafikte en yüksek sütun resim (12), en düşük sütun tiyatro (3); "
 "fark 12 − 3 = 9 öğrencidir.",
 "İki adım gerekir: grafikten en büyük ve en küçük değeri okumak ve farkı "
 "almak. Çeldiriciler tek değerde kalan ve işlemi karıştıran öğrenciyi "
 "temsil eder."),

"tr.g05.mat.5-5-2.q009": S(
 "Verilen grafiğe göre, araştırmaya katılan toplam öğrenci sayısı kaçtır?",
 grafik(["kitap", "film", "oyun"], [8, 6, 11]),
 "Sütun grafiği; kategoriler ve sıklıkları: kitap 8, film 6, oyun 11.",
 ["25", "11", "14", "3"], "25",
 {"11": "Yalnız en yüksek sütunu yazmış; diğerlerini eklememiş.",
  "14": "Bir sütunu toplamayı atlamış: 8 + 6 = 14.",
  "3": "Öğrenci sayısı yerine kategori sayısını yazmış."},
 "Toplam, bütün sütunların sıklıklarının toplamıdır: 8 + 6 + 11 = 25.",
 "Çok adımlı bir okuma: üç değeri grafikten ayrı ayrı okuyup toplamak "
 "gerekir. Çeldiriciler tek sütunda kalan, eksik toplayan ve kategori "
 "sayısını veri sayısı sanan öğrenciyi temsil eder."),

"tr.g05.mat.5-5-2.q014": S(
 "Verilen grafiğe göre, seçim sayısı 7'den fazla olan kaç kategori vardır?",
 grafik(["mavi", "yesil", "sari", "kirmizi"], [10, 4, 8, 6]),
 "Sütun grafiği; kategoriler ve sıklıkları: mavi 10, yeşil 4, sarı 8, "
 "kırmızı 6.",
 ["2", "4", "1", "18"], "2",
 {"4": "Bütün kategorileri saymış; koşulu uygulamamış.",
  "1": "Yalnız en yüksek sütunu saymış; 7'yi geçen ikinciyi atlamış.",
  "18": "Kategori saymak yerine sıklıkları toplamış: 10 + 8 = 18."},
 "Grafikte 7'den büyük olan sütunlar mavi (10) ve sarıdır (8); bu koşulu "
 "sağlayan iki kategori vardır.",
 "İki adım gerekir: her sütunun değerini okumak ve koşulu sağlayanları "
 "saymak. Çeldiriciler koşulu atlayan, eksik sayan ve sayma yerine toplama "
 "yapan öğrenciyi temsil eder."),

"tr.g05.mat.5-5-2.q019": S(
 "Verilen grafiğe göre, iki en düşük sütunun toplamı en yüksek sütundan kaç "
 "eksiktir?",
 grafik(["elma", "armut", "kiraz"], [14, 5, 4]),
 "Sütun grafiği; kategoriler ve sıklıkları: elma 14, armut 5, kiraz 4.",
 ["5", "9", "14", "23"], "5",
 {"9": "İki düşük sütunun toplamını yazmış; karşılaştırmayı yapmamış.",
  "14": "En yüksek sütunu yazmış; çıkarmayı yapmamış.",
  "23": "Üç sütunu toplamış: 14 + 5 + 4 = 23."},
 "İki düşük sütunun toplamı 5 + 4 = 9; en yüksek sütun 14 olduğuna göre "
 "fark 14 − 9 = 5'tir.",
 "Üç adım gerekir: grafikten üç değeri okumak, ikisini toplamak ve "
 "üçüncüden çıkarmak. Çeldiriciler adımlardan birinde duran öğrenciyi "
 "temsil eder ve bu yüzden birbirine yakındır."),

"tr.g05.mat.5-5-2.q020": S(
 "Verilen grafiğe göre, hangi kategori toplam seçimlerin yarısından "
 "fazlasını almıştır?",
 grafik(["yuzme", "kosu", "bisiklet"], [13, 6, 5]),
 "Sütun grafiği; kategoriler ve sıklıkları: yüzme 13, koşu 6, bisiklet 5.",
 ["Yüzme", "Koşu", "Bisiklet", "Hiçbiri"], "Yüzme",
 {"Koşu": "İkinci en yüksek sütunu seçmiş; yarıyla karşılaştırmamış.",
  "Bisiklet": "En düşük sütunu seçmiş.",
  "Hiçbiri": "Toplamı yanlış hesaplayıp hiçbir sütunun yarıyı geçmediğini "
             "sanmış."},
 "Toplam 13 + 6 + 5 = 24; yarısı 12'dir. Yalnız yüzme sütunu (13) 12'den "
 "büyüktür.",
 "Üç adım gerekir: bütün sütunları toplamak, yarısını bulmak ve her sütunu "
 "bu değerle karşılaştırmak. Çeldiriciler karşılaştırmayı atlayıp doğrudan "
 "sütun seçen öğrenciyi temsil eder."),
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

    for kid, y in YENILER.items():
        q = indeks[kid]
        konum = q["correct"]
        siklar = list(y["siklar"])
        assert len(set(siklar)) == 4, f"{kid}: şık tekrarı"
        assert y["dogru"] in siklar, f"{kid}: doğru şık yok"
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

        fig = dict(y["fig"])
        if fig["kind"] == "chart":
            kat = []
            for ad in fig["categoryKeys"]:
                a = (f"{kid}.visual."
                     f"{hashlib.sha256(ad.encode()).hexdigest()[:12]}")
                etiketler[a] = ad
                kat.append(a)
            fig["categoryKeys"] = kat
        ozet = hashlib.sha256(y["alt"].encode("utf-8")).hexdigest()[:12]
        anahtar = f"{kid}.visual.{ozet}"
        etiketler[anahtar] = y["alt"]
        fig["altTextKey"] = anahtar

        q.update(question=y["kok"], choices=sirali, correct=konum,
                 distractorWhy=gerekceler, explanation=y["aciklama"],
                 difficultyReason=y["zorluk"], figure=fig,
                 reviewStatus="pending", humanReviewed=False,
                 provenance="machine-generated:claude-opus-5:2026-08:"
                            "geo-son-parti-figur-oncelikli")

    paket["labels"] = etiketler
    sorular = [k for k in kayitlar if k.get("type") == "question"]
    paket["contractPolicy"]["minFiguredQuestions"] = sum(
        1 for q in sorular if q.get("figure"))
    dagilim = [0, 0, 0, 0]
    for q in sorular:
        dagilim[q["correct"]] += 1

    print(f"  yeniden üretilen soru  {len(YENILER)}")
    print(f"  figürlü soru           {paket['contractPolicy']['minFiguredQuestions']}")
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
