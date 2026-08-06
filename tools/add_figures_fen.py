#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fen sorularına kökten okunabilen görsel ekler.

Kural 42, görsel temsil olmadan öğretilemeyen kazanım alanlarında (FB.5.2
kuvvet-hareket, FB.5.3 canlı yapısı, FB.5.5 madde, FB.5.6 ışık/devre) figür
oranını denetler. Fen paketinde hiç figür yoktu.

İKİ KURAL, ARAÇ TARAFINDAN ZORLANIR (AUTHORING_RULES §6.2):

  1. Figürdeki her sayı, soru kökünde ZATEN yazılı olmalı. ``kok_dogrula``
     bunu denetler; geçmiyorsa araç durur. Kökte olmayan bir veriyi figüre
     koymak, soruyu figürle çözdürmektir.
  2. Figür, ARANAN değeri vermemeli. ``cevap_sizmasin`` doğru şıkkın metnini
     figür etiketlerinde arar; bulursa durur. Ölçüm serisi taşıyan sorularda
     aranan satır bilinçli olarak "?" bırakılır.

Kök metnine atıf da AYNI işlemde eklenir (§6.1): metnin anmadığı figür susar
ve kural 3 haklı olarak uyarır.

Kullanım:
    python tools/add_figures_fen.py --yaz
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "fen-bilimleri" / "fen-bilimleri-tum.jsonl"

# Atıf kalıbı doğrulayıcının açık işaret listesine UYMALIDIR. "Verilen şemaya
# göre" bilerek sayılmaz: fen sorularında şema çoğu kez senaryonun içindeki bir
# nesnedir ("öğrenci bir devre şeması çizer, bu şemaya göre deney kurar") ve
# okura gösterilen figür değildir. Şema için açık konum belirten kalıp kullanılır.
ATIF = {"table": "Verilen tabloya göre, ",
        "chart": "Verilen grafiğe göre, ",
        "flow": "Aşağıdaki şemaya göre, ",
        "circuit": "Aşağıdaki şemaya göre, "}

# ---------------------------------------------------------------------------
# Soru → figür tanımı.
#   ("tablo", [başlık...], [[hücre...], ...])
#   ("grafik", stil, [kategori...], [değer...], (x, y))
#   ("devre", [eleman...], düzen)
# "?" hücresi: aranan değer bilinçli boş bırakılmıştır.
# ---------------------------------------------------------------------------
FIGURLER = {
# ---- FB.5.2.1.1 kuvvetin büyüklüğü ----
"tr-g05-fen-q0084": ("tablo", ["Dinamometre", "Ölçebildiği en büyük kuvvet"],
  [["Birinci", "10 N"], ["İkinci", "30 N"]]),
"tr-g05-fen-q0087": ("tablo", ["Özellik", "Değer"],
  [["Ölçebileceği en büyük değer", "6 N"],
   ["Uygulanan kuvvet", "6 N değerinden fazla"]]),
# q0089 figür ALMAZ: kökte okunan değer 4 N ve doğru cevap da '4 N'.
# Figür kökü tekrarlasa bile burada cevabı ekrana yazmış olur (§6.2).
"tr-g05-fen-q0093": ("tablo", ["Asılan yük", "Yayın uzaması"],
  [["3 N", "2 cm"], ["6 N", "?"]]),
"tr-g05-fen-q0094": ("tablo", ["Uygulanan kuvvet", "İbrenin yeri"],
  [["4 N", "Ölçeğin tam ortası"], ["8 N", "?"]]),
"tr-g05-fen-q0099": ("tablo", ["Özellik", "Değer"],
  [["Dinamometrenin ölçüm sınırı", "10 N"], ["Uygulanan kuvvet", "15 N"]]),
"tr-g05-fen-q0100": ("grafik", "line", ["2 N", "4 N", "6 N"], [1, 2, 3],
  ("Uygulanan kuvvet", "Esneme miktarı (cm)")),
# ---- FB.5.2.1.2 dinamometre tasarımı ----
"tr-g05-fen-q0101": ("tablo", ["Asılan bilye sayısı", "Yayın uzaması"],
  [["1", "Az"], ["2", "Daha çok"], ["3", "En çok"]]),
"tr-g05-fen-q0102": ("tablo", ["Asılan bilye", "Yayın uzaması"],
  [["1 bilye", "2 cm"], ["2 bilye", "4 cm"], ["3 bilye", "6 cm"],
   ["4 bilye", "?"]]),
"tr-g05-fen-q0103": ("tablo", ["Yay", "1 N asılınca uzama"],
  [["Yay A", "1 cm"], ["Yay B", "3 cm"]]),
"tr-g05-fen-q0107": ("tablo", ["Asılan kuvvet", "Yayın uzaması"],
  [["1 N", "2 cm"], ["2 N", "4 cm"], ["3 N", "6 cm"]]),
"tr-g05-fen-q0108": ("tablo", ["Yay", "Uygulanan kuvvet", "Gözlenen"],
  [["Kısa yay", "2 N", "Daha az uzadı"],
   ["Uzun yay", "2 N", "Daha çok uzadı"]]),
"tr-g05-fen-q0109": ("tablo", ["Yay seçeneği", "Uzunluk"],
  [["Birinci", "5 cm"], ["İkinci", "10 cm"], ["Üçüncü", "20 cm"]]),
"tr-g05-fen-q0112": ("tablo", ["Öğrenci", "Kullandığı yay"],
  [["Birinci", "Kısa ve kalın"], ["İkinci", "Uzun ve ince"]]),
"tr-g05-fen-q0114": ("tablo", ["Uygulanan kuvvet", "Çubuğun ilerlemesi"],
  [["1 N", "2 cm"], ["2 N", "4 cm"], ["3 N", "6 cm"], ["4 N", "?"]]),
"tr-g05-fen-q0117": ("tablo", ["Yay", "Asılan bilye"],
  [["Birinci yay", "1 bilye"], ["İkinci yay", "2 bilye"]]),
"tr-g05-fen-q0118": ("tablo", ["Yay", "Asılan kütle", "Ölçülen"],
  [["İnce yay", "50 gram", "Uzama miktarı"],
   ["Kalın yay", "50 gram", "Uzama miktarı"]]),
# ---- FB.5.2.2.1 kütle ve ağırlık ----
"tr-g05-fen-q0119": ("tablo", ["Ortam", "Paketin kütlesi"],
  [["Dünya", "2 kilogram"], ["Ay", "?"]]),
"tr-g05-fen-q0120": ("tablo", ["Ölçüm", "Kullanılan araç"],
  [["Birinci", "Eşit kollu terazi"], ["İkinci", "Dinamometre"]]),
"tr-g05-fen-q0123": ("tablo", ["Ortam", "Kitabın ağırlığı"],
  [["Dünya", "3 N"], ["Ay", "?"]]),
"tr-g05-fen-q0124": ("tablo", ["Özellik", "Değer"],
  [["Paket şekerin kütlesi", "1 kg"]]),
"tr-g05-fen-q0125": ("tablo", ["Ölçüm sırası", "Kullanılan araç"],
  [["Önce", "Eşit kollu terazi"], ["Sonra", "Dinamometre"]]),
"tr-g05-fen-q0126": ("tablo", ["Ortam", "Elmanın kütlesi"],
  [["Dünya", "200 gram"], ["Ay", "?"]]),
"tr-g05-fen-q0129": ("tablo", ["Büyüklük", "Dünya'da ölçülen"],
  [["Kütle", "3 kg"], ["Ağırlık", "30 N"]]),
"tr-g05-fen-q0130": ("tablo", ["Ambalaj bilgisi", "Yazan"],
  [["Un paketinin üzerinde", "2 kg"]]),
# q0133 figür ALMAZ: şıklar çıplak değer ('150 gram') ve doğru cevap Dünya'daki
# değerin aynısı; tabloya yazmak cevabı ekrana koymak olur (§6.2).
"tr-g05-fen-q0134": ("tablo", ["Ortam", "Cismin ağırlığı"],
  [["Dünya", "30 N"], ["Ay", "?"]]),
# ---- FB.5.2.3.1 sürtünme kuvvetinin etkileri ----
"tr-g05-fen-q0137": ("tablo", ["Deneme", "Zemin"],
  [["Birinci", "Düz tahta"], ["İkinci", "Halı kaplı"]]),
"tr-g05-fen-q0138": ("tablo", ["Rampa", "Yüzey durumu"],
  [["Birinci", "Yağ sürülmüş"], ["İkinci", "Kuru"], ["Üçüncü", "Zımparalı"]]),
"tr-g05-fen-q0139": ("tablo", ["Pistin yarısı", "Zemin"],
  [["Birinci yarı", "Düz asfalt"], ["İkinci yarı", "Kuru çimen"]]),
"tr-g05-fen-q0140": ("tablo", ["Ortam", "Yürüme yüzeyi"],
  [["Havuz", "Suyun içi"], ["Okul", "Koridor zemini"],
   ["Buz pisti", "Buz"]]),
"tr-g05-fen-q0141": ("tablo", ["Yüzey", "Gözlenen"],
  [["Pürüzlü karton", "Blok daha erken durdu"],
   ["Düz cam", "Blok daha geç durdu"]]),
"tr-g05-fen-q0142": ("tablo", ["Yol", "Gözlenen"],
  [["Çakıllı yol", "Birkaç adımda tökezledi"],
   ["Islak asfalt", "Kaydı"]]),
"tr-g05-fen-q0143": ("tablo", ["Kitap", "Altına yapıştırılan"],
  [["Birinci", "Lastik bant"], ["İkinci", "Düz karton şerit"]]),
"tr-g05-fen-q0145": ("tablo", ["Deney", "Yüzey"],
  [["Birinci", "Kuru halı"], ["İkinci", "Islak halı"],
   ["Üçüncü", "Kuru fayans"], ["Dördüncü", "Yağlı fayans"]]),
"tr-g05-fen-q0146": ("tablo", ["Zemin", "Gözlenen"],
  [["Tahta", "Araba daha uzağa gitti"], ["Halı", "Araba daha yakına gitti"]]),
"tr-g05-fen-q0147": ("tablo", ["Deneme", "Bloğun altındaki"],
  [["Birinci", "Pürüzsüz kâğıt"], ["İkinci", "İnce zımpara"],
   ["Üçüncü", "Kalın zımpara"]]),
"tr-g05-fen-q0151": ("tablo", ["Rampa yüzeyi", "Kaplama"],
  [["Bir yüzey", "Pürüzlü halı"], ["Öbür yüzey", "Düz kâğıt"]]),
"tr-g05-fen-q0152": ("tablo", ["Rampa", "Yüzeyi"],
  [["Birinci", "Kumlu"], ["İkinci", "Cilalı"]]),
"tr-g05-fen-q0153": ("tablo", ["Model paraşüt", "Biçimi"],
  [["Birinci", "Küçük ve kapalı"], ["İkinci", "Orta boy"],
   ["Üçüncü", "Büyük ve geniş"]]),
"tr-g05-fen-q0154": ("tablo", ["Deney", "Düzenek"],
  [["Birinci", "Blok yay üzerinden bırakıldı"],
   ["İkinci", "Aynı blok farklı zeminde"]]),
"tr-g05-fen-q0148": ("tablo", ["Deneme", "Ayakta olan"],
  [["Birinci", "Ayakkabı"], ["İkinci", "Çorap"]]),
# ---- FB.5.2.3.2 sürtünmeyi artırma ve azaltma ----
"tr-g05-fen-q0160": ("tablo", ["Yüzey", "Cinsi"],
  [["1", "Pürüzlü halı"], ["2", "Düz cam"], ["3", "Yağlı tabla"],
   ["4", "Çıkıntılı lastik örtü"]]),
"tr-g05-fen-q0164": ("grafik", "bar",
  ["Cam zemin", "Ahşap zemin", "Çakıl taşlı zemin"], [3, 5, 8],
  ("Zemin türü", "Harekete geçirmek için gereken kuvvet (N)")),
"tr-g05-fen-q0165": ("tablo", ["Zemin", "Durumu"],
  [["Düz asfalt yol", "Yağmurlu havada ıslak"],
   ["Yosun tutmuş kaldırım", "Yağmurlu havada ıslak"],
   ["Kuru beton", "Yağmurlu havada ıslak"]]),
"tr-g05-fen-q0170": ("tablo", ["Zemin", "Kaplaması"],
  [["1", "Düz beton"], ["2", "İnce çakıl"], ["3", "Yağlı naylon örtü"]]),
"tr-g05-fen-q0159": ("tablo", ["Düzenek", "İçeriği"],
  [["Birinci", "Bilim fuarı modeli bölümü"],
   ["İkinci", "Bilim fuarı modeli bölümü"],
   ["Üçüncü", "Bilim fuarı modeli bölümü"],
   ["Dördüncü", "Bilim fuarı modeli bölümü"]]),
# ---- FB.5.3.1.1 bitki ve hayvan hücreleri ----
"tr-g05-fen-q0175": ("tablo", ["Hücre", "Hücre duvarı", "Kloroplast"],
  [["Birinci", "Var", "Var"], ["İkinci", "Yok", "Yok"]]),
"tr-g05-fen-q0179": ("tablo", ["Hücre örneği", "Koful"],
  [["Birinci", "Belirgin büyük bir koful"],
   ["İkinci", "Birçok küçük koful"]]),
"tr-g05-fen-q0183": ("tablo", ["Hücre", "Koful", "Hücre duvarı"],
  [["Birinci", "Büyük ve tek", "Var"],
   ["İkinci", "Birçok küçük", "Yok"]]),
"tr-g05-fen-q0188": ("tablo", ["Hücre", "Koful", "Hücre duvarı"],
  [["Birinci", "Büyük ve belirgin", "Var"],
   ["İkinci", "Küçük", "Yok"]]),
"tr-g05-fen-q0191": ("tablo", ["Hücre", "Hücre duvarı ve kloroplast"],
  [["Birinci", "Görüldü"], ["İkinci", "Görülmedi"]]),
"tr-g05-fen-q0186": ("tablo", ["Yapı", "Gözlemde"],
  [["Hücre zarı", "Var"], ["Sitoplazma", "Var"], ["Çekirdek", "Var"],
   ["Hücre duvarı", "Yok"], ["Kloroplast", "Yok"]]),
# ---- FB.5.3.1.2 hücreden organizmaya ----
"tr-g05-fen-q0195": ("akis", ["Hücre", "?", "Organ", "Sistem", "Organizma"]),
"tr-g05-fen-q0197": ("akis",
  ["Hücre", "Doku", "Sistem", "Organ", "Organizma"]),
"tr-g05-fen-q0214": ("akis",
  ["Hücre", "Doku", "Organ", "Sistem", "Organizma"]),
"tr-g05-fen-q0207": ("akis", ["Doku", "Organ", "Sistem", "Organizma"]),
"tr-g05-fen-q0194": ("tablo", ["Birlikte çalışan yapı", "Örnek"],
  [["Kalp", "Yapı"], ["Damar", "Yapı"], ["Kan", "Yapı"]]),
"tr-g05-fen-q0198": ("tablo", ["Birlikte çalışan organ", "Görevi"],
  [["Mide", "Besinleri sindirmek"], ["Karaciğer", "Besinleri sindirmek"],
   ["Pankreas", "Besinleri sindirmek"]]),
"tr-g05-fen-q0205": ("tablo", ["Sistem", "Vücuttaki durumu"],
  [["Sindirim sistemi", "Bulunur"], ["Dolaşım sistemi", "Bulunur"],
   ["Sinir sistemi", "Bulunur"]]),
"tr-g05-fen-q0208": ("tablo", ["Mideyi oluşturan", "Türü"],
  [["Kas dokusu", "Doku"], ["Örtü dokusu", "Doku"]]),
"tr-g05-fen-q0213": ("tablo", ["Birlikte çalışan", "Yapı"],
  [["Kalp", "Bulunur"], ["Damar", "Bulunur"], ["Kan hücreleri", "Bulunur"]]),
# ---- FB.5.3.2.1 destek ve hareket sistemi ----
"tr-g05-fen-q0217": ("tablo", ["Listedeki yapı", "Sınıf"],
  [["Kafatası", "?"], ["Omurga", "?"], ["Pazı kası", "?"],
   ["Uyluk kası", "?"], ["Parmak eklemi", "?"]]),
"tr-g05-fen-q0224": ("tablo", ["Sıra", "Yapı"],
  [["1", "Pazı kemiği"], ["2", "Dirsek eklemi"], ["3", "Biseps kası"]]),
"tr-g05-fen-q0229": ("tablo", ["Eklem", "Gözlenen hareket"],
  [["Bilek", "Yukarı-aşağı ve ileri-geri"],
   ["Omuz", "Daire çizer gibi her yöne"]]),
"tr-g05-fen-q0230": ("tablo", ["Model malzemesi", "Neyi temsil ediyor"],
  [["Karton", "?"], ["İp", "?"], ["Bant", "?"]]),
"tr-g05-fen-q0234": ("tablo", ["Dokunulan yapı", "Hissedilen"],
  [["Birinci", "Sert doku"], ["İkinci", "Yumuşak ve hareket edebilen doku"]]),
"tr-g05-fen-q0221": ("tablo", ["Kemik türü", "Sınıflandırma ölçütü"],
  [["Uzun", "Şekil"], ["Kısa", "Şekil"], ["Yassı", "Şekil"],
   ["Düzensiz", "Şekil"]]),
"tr-g05-fen-q0225": ("tablo", ["Eklem türü", "Hareket yeteneği"],
  [["Oynar", "?"], ["Yarı oynar", "?"], ["Oynamaz", "?"]]),
# ---- FB.5.3.2.2 destek ve hareket sistemi sağlığı ----
"tr-g05-fen-q0254": ("tablo", ["Öğrenci", "Oturuşu"],
  [["Ali", "Kambur"], ["Selin", "Sırtı dik"],
   ["Merve", "Masaya yaslanıp öne eğik"], ["Can", "Bacakları uzatılmış"]]),
# q0249 figür ALMAZ: şıklar öğrenci adları ve tablonun ilk sütunu da adlar;
# doğru cevap ('Ayşe') figürde göründüğü an soru tabloya bakmakla çözülür.
"tr-g05-fen-q0237": ("tablo", ["Taşıma yöntemi", "Poşetin dağılımı"],
  [["Birinci", "Tek elde"], ["İkinci", "İki ele eşit"]]),
"tr-g05-fen-q0251": ("tablo", ["Taşıma biçimi", "Sırtın durumu"],
  [["Tek omuzda", "Ağrı başladı"], ["Önerilen", "?"]]),
# ---- FB.5.5.1.1 maddenin tanecikli yapısı ----
"tr-g05-fen-q0315": ("tablo", ["Kavanoz", "İçindeki", "Tanecikler arası boşluk"],
  [["Birinci", "Su", "?"], ["İkinci", "Buz", "Çok az"],
   ["Üçüncü", "Hava", "?"]]),
"tr-g05-fen-q0317": ("tablo", ["Kap", "İçindeki"],
  [["Birinci", "Su"], ["İkinci", "Buz"], ["Üçüncü", "Hava"]]),
"tr-g05-fen-q0320": ("tablo", ["Kap", "Eklenen gıda boyası"],
  [["Birinci", "Birkaç damla"], ["İkinci", "İki damla"],
   ["Üçüncü", "Üç damla"]]),
# q0323 ve q0321 figür ALMAZ: şıklar maddelerin kendi adları; tablonun ilk
# sütunu o adları taşıdığı an doğru cevap ekrandadır (§6.2).
"tr-g05-fen-q0313": ("tablo", ["Örnek", "Taneciklerin durumu"],
  [["Şişkin balonun içi", "Birbirine çok uzak"],
   ["Katı limon tozu", "?"]]),
# ---- FB.5.5.2.1 ısı ve sıcaklık ----
"tr-g05-fen-q0324": ("tablo", ["Ölçüm zamanı", "Hava sıcaklığı"],
  [["Sabah", "22 °C"], ["Öğleden sonra", "28 °C"]]),
"tr-g05-fen-q0325": ("tablo", ["Kap", "Su kütlesi", "Sıcaklık"],
  [["Birinci", "Eşit", "30 °C"], ["İkinci", "Eşit", "60 °C"]]),
"tr-g05-fen-q0327": ("tablo", ["Kap", "Suyun sıcaklığı"],
  [["Birinci", "20 °C"], ["İkinci", "60 °C"]]),
"tr-g05-fen-q0332": ("tablo", ["Tencere", "Su miktarı", "Sıcaklık"],
  [["Birinci", "1 litre", "Eşit"], ["İkinci", "2 litre", "Eşit"]]),
"tr-g05-fen-q0333": ("tablo", ["Bardak", "Su miktarı", "Sıcaklık"],
  [["Birinci", "Yarım bardak", "50 °C"],
   ["İkinci", "Tam bardak", "50 °C"]]),
"tr-g05-fen-q0338": ("tablo", ["Oda", "Termometrenin gösterdiği"],
  [["Birinci", "20 °C"], ["İkinci", "40 °C"]]),
"tr-g05-fen-q0339": ("tablo", ["Örnek", "Hacim", "Sıcaklık"],
  [["Birinci", "50 mL", "Aynı"], ["İkinci", "200 mL", "Aynı"]]),
"tr-g05-fen-q0329": ("tablo", ["Kap", "İçindeki su"],
  [["Tencere", "Ocakta kaynıyor"], ["Bardak", "Tencereden konuldu"]]),
# ---- FB.5.5.2.2 ısı alışverişi ----
"tr-g05-fen-q0340": ("tablo", ["Sıvı", "Miktar", "Başlangıç sıcaklığı"],
  [["Çay", "300 mL", "80 °C"], ["Su", "300 mL", "20 °C"],
   ["Karışım", "İkisi birlikte", "?"]]),
"tr-g05-fen-q0341": ("tablo", ["Sıvı", "Miktar", "Başlangıç sıcaklığı"],
  [["Sıcak çay", "80 mL", "60 °C"], ["Soğuk su", "80 mL", "20 °C"],
   ["Karışım", "İkisi birlikte", "?"]]),
"tr-g05-fen-q0342": ("tablo", ["Sıvı", "Miktar", "Başlangıç sıcaklığı"],
  [["Birinci su", "150 mL", "40 °C"], ["İkinci su", "150 mL", "10 °C"],
   ["Karışım", "İkisi birlikte", "?"]]),
"tr-g05-fen-q0345": ("tablo", ["Sıvı", "Miktar", "Başlangıç sıcaklığı"],
  [["Birinci su", "100 mL", "60 °C"], ["İkinci su", "200 mL", "30 °C"]]),
"tr-g05-fen-q0347": ("tablo", ["Sıvı", "Miktar", "Başlangıç sıcaklığı"],
  [["Sıcak çay", "200 mL", "60 °C"], ["Su", "300 mL", "20 °C"]]),
"tr-g05-fen-q0348": ("tablo", ["Sıvı", "Miktar", "Başlangıç sıcaklığı"],
  [["Çay", "100 mL", "80 °C"], ["Su", "100 mL", "20 °C"],
   ["Karışım", "İkisi birlikte", "?"]]),
"tr-g05-fen-q0350": ("tablo", ["Sıvı", "Miktar", "Başlangıç sıcaklığı"],
  [["Süt", "50 mL", "90 °C"], ["Su", "200 mL", "20 °C"]]),
"tr-g05-fen-q0351": ("tablo", ["Bardak", "Miktar", "Başlangıç sıcaklığı"],
  [["Birinci", "100 mL", "30 °C"], ["İkinci", "100 mL", "70 °C"]]),
"tr-g05-fen-q0352": ("tablo", ["Sıvı", "Miktar", "Başlangıç sıcaklığı"],
  [["Çorba", "200 mL", "80 °C"], ["Su", "100 mL", "20 °C"]]),
"tr-g05-fen-q0353": ("tablo", ["Kap", "Suyun sıcaklığı"],
  [["Birinci", "10 °C"], ["İkinci", "90 °C"]]),
"tr-g05-fen-q0354": ("tablo", ["Deneme", "Sıcak su", "Soğuk su"],
  [["Birinci", "50 mL, 60 °C", "50 mL, 40 °C"],
   ["İkinci", "50 mL, 60 °C", "25 mL, 40 °C"]]),
"tr-g05-fen-q0355": ("tablo", ["Deneme", "Soğuk su", "Sıcak su"],
  [["Birinci", "100 mL, 25 °C", "100 mL, 75 °C"],
   ["İkinci", "Daha çok soğuk su", "Aynı sıcak su"]]),
"tr-g05-fen-q0344": ("tablo", ["Su", "Kütle", "Başlangıç sıcaklığı"],
  [["Birinci", "50 g", "80 °C"], ["İkinci", "50 g", "20 °C"]]),
"tr-g05-fen-q0349": ("tablo", ["Sıvı", "Miktar", "Başlangıç sıcaklığı"],
  [["Çorba", "500 mL", "70 °C"], ["Su", "500 mL", "30 °C"]]),
# ---- FB.5.5.3.1 hâl değişimi ----
"tr-g05-fen-q0359": ("tablo", ["Kap", "Ağzı", "Birkaç gün sonra"],
  [["Birinci", "Açık", "?"], ["İkinci", "Kapalı", "?"]]),
"tr-g05-fen-q0364": ("tablo", ["Kap", "Su", "Bekleme"],
  [["Birinci", "100 mL, 80 °C", "10 dakika"],
   ["İkinci", "100 mL, 20 °C", "10 dakika"]]),
"tr-g05-fen-q0369": ("tablo", ["Bardak", "Durumu", "Üç saat sonra"],
  [["Birinci", "Açıkta", "Su azaldı"], ["İkinci", "Kapaklı", "?"]]),
"tr-g05-fen-q0370": ("tablo", ["Kap", "Odanın sıcaklığı", "Bekleme"],
  [["Birinci", "20 °C", "10 dakika"], ["İkinci", "30 °C", "10 dakika"]]),
"tr-g05-fen-q0365": ("tablo", ["Düzenek", "Gözlenen"],
  [["Birinci", "Isıtılan kaptaki suya geçirilen balon şişiyor"],
   ["İkinci", "Buzdolabından çıkan şişenin dışı terliyor"]]),
"tr-g05-fen-q0360": ("akis", ["Suyun yüzeyinden buhar çıkıyor",
  "Su fokurdayarak kaynıyor", "Çok miktarda buhar çıkıyor"]),
# ---- FB.5.5.4.1 ısı iletkenliği ----
"tr-g05-fen-q0372": ("tablo", ["Çubuk", "Isıtma süresi"],
  [["Tahta", "Aynı"], ["Demir", "Aynı"], ["Alüminyum", "Aynı"],
   ["Plastik", "Aynı"]]),
"tr-g05-fen-q0374": ("tablo", ["Çubuk", "Ucundaki mum", "Isıtma"],
  [["Metal kaşık", "Aynı büyüklükte", "Aynı"],
   ["Tahta çubuk", "Aynı büyüklükte", "Aynı"]]),
"tr-g05-fen-q0377": ("tablo", ["Çubuk", "Maddesi"],
  [["Birinci", "Bakır"], ["İkinci", "Alüminyum"], ["Üçüncü", "Tahta"],
   ["Dördüncü", "Plastik"]]),
"tr-g05-fen-q0381": ("tablo", ["Kaşık", "Birkaç saniye sonra ucu"],
  [["Metal", "Sıcak"], ["Tahta", "Ilık"]]),
"tr-g05-fen-q0383": ("tablo", ["Malzeme", "Sınıf"],
  [["Demir çubuk", "?"], ["Alüminyum tel", "?"], ["Tahta çubuk", "?"],
   ["Plastik cetvel", "?"], ["Cam bardak", "?"]]),
"tr-g05-fen-q0386": ("tablo", ["Batırılan", "Süre"],
  [["Tahta kaşık", "15 saniye"], ["Metal kaşık", "15 saniye"],
   ["Plastik kaşık", "15 saniye"], ["Taş parçası", "15 saniye"]]),
"tr-g05-fen-q0387": ("tablo", ["Araç", "Yapıldığı madde"],
  [["Tencere", "Metal"], ["Tencere kulpu", "Plastik"], ["Kazak", "Yün"],
   ["Sıcak su borusunun dış yüzeyi", "Köpük"]]),
"tr-g05-fen-q0380": ("tablo", ["Kap", "Dış yüzeyi", "Bekleme"],
  [["Birinci", "Kalın köpükle sarılı", "20 dakika"],
   ["İkinci", "Açık", "20 dakika"]]),
# ---- FB.5.5.4.2 ısı yalıtımı ----
"tr-g05-fen-q0388": ("tablo", ["Elde bulunan malzeme", "Türü"],
  [["Cam şişe", "Kap"], ["Strafor köpük", "Sarma malzemesi"],
   ["Alüminyum folyo", "Sarma malzemesi"],
   ["Yün kumaş", "Sarma malzemesi"]]),
"tr-g05-fen-q0391": ("tablo", ["Kutuya yapıştırılan", "Bekleme"],
  [["Cam", "10 dakika"], ["Tahta", "10 dakika"], ["Metal", "10 dakika"],
   ["Kumaş", "10 dakika"]]),
"tr-g05-fen-q0392": ("tablo", ["Bardak", "Dış yüzeyi"],
  [["Birinci", "Yalıtılmadan bırakıldı"],
   ["İkinci", "Eşit kalınlıkta pamukla sarıldı"]]),
"tr-g05-fen-q0396": ("tablo", ["Bardak", "Dış yüzeyi"],
  [["Birinci", "Açık"], ["İkinci", "İnce alüminyum folyo"],
   ["Üçüncü", "Yün kumaş"]]),
"tr-g05-fen-q0401": ("tablo", ["Kullanılabilecek malzeme", "Türü"],
  [["Yün kumaş parçası", "Kumaş"], ["İnce alüminyum folyo", "Metal"],
   ["Plastik tabak", "Plastik"], ["Gazete kâğıdı", "Kâğıt"]]),
"tr-g05-fen-q0402": ("tablo", ["Bardak", "Sarıldığı malzeme", "Kalınlık"],
  [["Birinci", "Yün ip", "Aynı"], ["İkinci", "Alüminyum folyo", "Aynı"]]),
"tr-g05-fen-q0403": ("tablo", ["Kutu", "Tabanındaki yün kumaş"],
  [["Birinci", "Çift kat"], ["İkinci", "Tek kat"]]),
"tr-g05-fen-q0389": ("tablo", ["Model parçası", "Durumu"],
  [["Karton kutu", "İki özdeş"], ["İçine konan şişe", "Ilık su dolu"]]),
# ---- FB.5.6.1.1 devre elemanları ve sembolleri ----
"tr-g05-fen-q0405": ("devre", ["battery", "lamp", "switch", "wire"],
  "series"),
"tr-g05-fen-q0408": ("devre", ["battery", "switch", "lamp", "wire"],
  "series"),
"tr-g05-fen-q0411": ("devre", ["battery", "lamp", "switch", "wire"],
  "series"),
"tr-g05-fen-q0413": ("devre", ["battery", "switch", "lamp", "wire"],
  "series"),
"tr-g05-fen-q0415": ("devre", ["battery", "lamp", "switch", "wire"],
  "series"),
"tr-g05-fen-q0417": ("devre", ["battery", "switch", "lamp", "wire"],
  "series"),
"tr-g05-fen-q0421": ("devre", ["battery", "switch", "lamp", "wire"],
  "series"),
"tr-g05-fen-q0423": ("devre", ["battery", "switch", "lamp", "wire"],
  "series"),
# ---- FB.5.6.1.2 devre şeması ve deney ----
"tr-g05-fen-q0424": ("devre", ["battery", "switch", "lamp", "lamp", "wire"],
  "series"),
"tr-g05-fen-q0425": ("devre", ["battery", "switch", "lamp", "wire"],
  "series"),
"tr-g05-fen-q0427": ("devre", ["battery", "switch", "lamp", "wire"],
  "series"),
"tr-g05-fen-q0428": ("devre", ["battery", "switch", "lamp", "wire"],
  "series"),
"tr-g05-fen-q0431": ("devre", ["battery", "lamp", "switch", "wire"],
  "series"),
"tr-g05-fen-q0432": ("devre", ["battery", "switch", "lamp", "wire"],
  "series"),
"tr-g05-fen-q0435": ("devre", ["battery", "switch", "lamp", "wire"],
  "series"),
"tr-g05-fen-q0436": ("devre", ["battery", "switch", "lamp", "wire"],
  "series"),
"tr-g05-fen-q0438": ("devre", ["battery", "lamp", "wire"], "series"),
"tr-g05-fen-q0439": ("devre", ["battery", "lamp", "switch", "wire"],
  "series"),
"tr-g05-fen-q0441": ("devre", ["battery", "lamp", "switch"], "series"),
"tr-g05-fen-q0442": ("devre", ["battery", "lamp"], "series"),
# ---- FB.5.6.2.1 ampul parlaklığını etkileyen değişkenler ----
"tr-g05-fen-q0444": ("tablo", ["Devre", "Pil sayısı", "Ampul sayısı"],
  [["Birinci", "1", "1"], ["İkinci", "2", "1"]]),
"tr-g05-fen-q0446": ("tablo", ["Devre", "Pil sayısı", "Ampul sayısı"],
  [["Birinci", "1", "1"], ["İkinci", "2", "1"]]),
"tr-g05-fen-q0447": ("tablo", ["Devre", "Pil sayısı", "Ampul sayısı"],
  [["Birinci", "1", "1"], ["İkinci", "2", "1"]]),
"tr-g05-fen-q0448": ("tablo", ["Aşama", "Pil sayısı", "Ampul sayısı"],
  [["Başlangıç", "2", "1"], ["Sonra", "2", "3"]]),
# q0450 figür ALMAZ: pil/ampul sayıları yalnız ŞIKLARDA geçiyor, kökte yok;
# tabloya yazmak seçenekleri kökün içine taşımak olur.
"tr-g05-fen-q0453": ("tablo", ["Düzenek", "Pil sayısı", "Ampul sayısı"],
  [["1", "1", "1"], ["2", "2", "1"], ["3", "?", "?"]]),
"tr-g05-fen-q0455": ("tablo", ["Aşama", "Pil sayısı", "Ampul sayısı"],
  [["Başlangıç", "1", "1"], ["Sonra", "3", "1"]]),
"tr-g05-fen-q0457": ("tablo", ["Aşama", "Pil sayısı", "Ampul"],
  [["Başlangıç", "2", "Aynı"], ["Sonra", "4", "Aynı"]]),
"tr-g05-fen-q0458": ("tablo", ["Devre", "Pil", "Ampul"],
  [["Birinci", "İki özdeş pil", "İki özdeş ampul, seri"],
   ["İkinci", "Aynı iki pil", "Tek ampul"]]),
# q0459 figür ALMAZ: pil sayıları yalnız şıklarda geçiyor, kökte yok.
"tr-g05-fen-q0460": ("tablo", ["Grup", "Pil sayısı", "Ampul sayısı"],
  [["1", "2", "1"], ["2", "4", "1"]]),
"tr-g05-fen-q0462": ("tablo", ["Malzeme", "Adet"],
  [["Özdeş ampul", "İki"], ["Özdeş pil", "İki"]]),
"tr-g05-fen-q0463": ("tablo", ["Grup", "Pil sayısı", "Ampul sayısı"],
  [["A", "1", "2"], ["B", "2", "1"]]),
"tr-g05-fen-q0452": ("tablo", ["Aşama", "Pil", "Ampul"],
  [["Başlangıç", "İki özdeş pil", "Bir ampul"],
   ["Sonra", "Değiştirilmedi", "Bir ampul daha seri bağlandı"]]),
# ---- kural 42 eşiğini geçmek için hedefli ek figürler ----
# Bu dört kazanım %30 eşiğinin altındaydı: FB.5.2.3.2, FB.5.3.1.1,
# FB.5.3.2.2, FB.5.5.1.1. Aşağıdakiler yine yalnız kökteki veriyi gösterir.
"tr-g05-fen-q0155": ("tablo", ["Tasarım kararı", "Lastik yüzeyi"],
  [["Birinci", "Tamamen pürüzsüz"], ["İkinci", "Üzerine yağ sürülmüş"]]),
"tr-g05-fen-q0169": ("tablo", ["Zincirin durumu", "Pedal çevirme"],
  [["Paslanmış ve kurumuş", "Zorlaşıyor"], ["Yağlanmış", "?"]]),
"tr-g05-fen-q0172": ("tablo", ["Lastik", "Yol"],
  [["Zincir takılmadan", "Buzlu"], ["Zincir takıldıktan sonra", "Buzlu"]]),
"tr-g05-fen-q0242": ("tablo", ["Duruş özelliği", "Sınıfta oturma"],
  [["Sırt", "?"], ["Omuzlar", "?"], ["Ayaklar", "?"]]),
"tr-g05-fen-q0248": ("tablo", ["Vücut bölümü", "Ali'nin kaldırma biçimi"],
  [["Dizler", "Bükülü"], ["Sırt", "Dik"]]),
"tr-g05-fen-q0245": ("tablo", ["Alışkanlık alanı", "Günlük yaşamda"],
  [["Hareket", "?"], ["Beslenme", "?"], ["Duruş ve taşıma", "?"]]),
"tr-g05-fen-q0190": ("tablo", ["Hücrenin bölümü", "Gözlenen"],
  [["Dış kısım", "Kalın ve dayanıklı bir tabaka"],
   ["İç kısım", "Yeşil renkli küçük yapılar"]]),
"tr-g05-fen-q0310": ("tablo", ["Deney", "Suyun durumu", "Yayılma"],
  [["Birinci", "Oda sıcaklığında", "Tüm suya yayıldı"],
   ["İkinci", "Soğuk", "Daha yavaş"]]),
"tr-g05-fen-q0314": ("tablo", ["Öğrenci", "İddiası"],
  [["Birinci", "Katı taneciklerinin hiç hareket etmediği"],
   ["İkinci", "Sıcak suya konan metal kaşığın taneciklerinin sallandığı"]]),
"tr-g05-fen-q0308": ("tablo", ["Aşama", "Gözlenen"],
  [["Şeker eklenmeden önce", "Su seviyesi"],
   ["Şeker çözündükten sonra", "Su seviyesi neredeyse değişmedi"]]),
}


def slug_karsilastir(metin: str) -> str:
    s = unicodedata.normalize("NFKC", str(metin or "")).casefold()
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s)).strip()


def sayilar(metin: str) -> set:
    return set(re.findall(r"\d+", str(metin or "")))


def kok_dogrula(soru_id: str, kok: str, etiketler: list) -> None:
    """Figürdeki her sayı kökte geçmeli (§6.2)."""
    kok_sayilari = sayilar(kok)
    for e in etiketler:
        if e == "?":
            continue
        for s in sayilar(e):
            if s not in kok_sayilari:
                raise ValueError(
                    f"{soru_id}: '{e}' içindeki {s} soru kökünde yok; "
                    "figür kökte olmayan bilgi taşıyamaz")


def cevap_sizmasin(soru_id: str, dogru: str, etiketler: list) -> None:
    """Figür aranan değeri vermemeli (§6.2)."""
    d = slug_karsilastir(dogru)
    for e in etiketler:
        if e == "?":
            continue
        if slug_karsilastir(e) == d:
            raise ValueError(
                f"{soru_id}: figür doğru cevabı ('{dogru}') veriyor")


def anahtar(soru_id: str, metin: str) -> str:
    ozet = hashlib.sha256(metin.encode("utf-8")).hexdigest()[:12]
    return f"{soru_id}.visual.{ozet}"


def figur_kur(soru_id: str, tanim: tuple, etiketler: dict) -> tuple:
    """Figürü kurar; (figure, düz etiket listesi) döner."""
    duz: list = []

    def et(metin: str) -> str:
        duz.append(metin)
        a = anahtar(soru_id, metin)
        etiketler[a] = metin
        return a

    tip = tanim[0]
    if tip == "tablo":
        _, basliklar, satirlar = tanim
        for s in satirlar:
            assert len(s) == len(basliklar), f"{soru_id}: satır genişliği"
        return {"kind": "table",
                "headerKeys": [et(b) for b in basliklar],
                "rows": [[{"key": et(h)} for h in s] for s in satirlar]}, duz
    if tip == "grafik":
        _, stil, kategoriler, degerler, eksenler = tanim
        assert len(kategoriler) == len(degerler), f"{soru_id}: uzunluk"
        fig = {"kind": "chart", "style": stil,
               "categoryKeys": [et(k) for k in kategoriler],
               "values": list(degerler)}
        if eksenler:
            fig["axisKeys"] = {"x": et(eksenler[0]), "y": et(eksenler[1])}
        return fig, duz
    if tip == "akis":
        _, adimlar = tanim
        dugumler = [{"id": f"a{i+1}", "labelKey": et(a)}
                    for i, a in enumerate(adimlar)]
        kenarlar = [{"from": f"a{i+1}", "to": f"a{i+2}"}
                    for i in range(len(adimlar) - 1)]
        return {"kind": "flow", "nodes": dugumler, "edges": kenarlar,
                "direction": "right"}, duz
    if tip == "devre":
        _, elemanlar, duzen = tanim
        return ({"kind": "circuit", "elements": list(elemanlar),
                 "layout": duzen}, duz)
    raise ValueError(f"bilinmeyen kısayol: {tip}")


def alt_metin(tanim: tuple) -> str:
    """Görselin gösterdiğini betimler; çıkarımı değil (figure_spec 1.1.0)."""
    tip = tanim[0]
    if tip == "tablo":
        _, basliklar, satirlar = tanim
        sut = ", ".join(f"'{b}'" for b in basliklar)
        dolu = "; ".join(" — ".join(s) for s in satirlar)
        ek = (" Soru işaretli hücre boş bırakılmıştır."
              if any("?" in s for s in satirlar) else "")
        return (f"{len(satirlar)} satırlık tablo. Sütunlar: {sut}. "
                f"Satırlar: {dolu}.{ek}")
    if tip == "akis":
        _, adimlar = tanim
        ek = (" Soru işaretli halka boş bırakılmıştır."
              if "?" in adimlar else "")
        return (f"{len(adimlar)} halkalı soldan sağa akış şeması: "
                + " → ".join(adimlar) + f".{ek}")
    if tip == "grafik":
        _, stil, kategoriler, degerler, eksenler = tanim
        cift = ", ".join(f"{k}: {d}" for k, d in zip(kategoriler, degerler))
        tur = {"bar": "sütun", "line": "çizgi", "pie": "daire"}[stil]
        eksen = (f" Yatay eksen '{eksenler[0]}', düşey eksen '{eksenler[1]}'."
                 if eksenler else "")
        return f"{len(kategoriler)} değerli {tur} grafiği. {cift}.{eksen}"
    if tip == "devre":
        _, elemanlar, duzen = tanim
        ad = {"battery": "pil", "lamp": "ampul", "switch": "anahtar",
              "resistor": "direnç", "wire": "bağlantı kablosu"}
        sayim: dict = {}
        for e in elemanlar:
            sayim[e] = sayim.get(e, 0) + 1
        liste = ", ".join(f"{n} {ad[e]}" if n > 1 else ad[e]
                          for e, n in sayim.items())
        duzen_ad = {"series": "seri", "parallel": "paralel"}[duzen]
        return f"{duzen_ad.capitalize()} bağlı devre şeması: {liste}."
    raise ValueError(tip)


def kucult_ilk(metin: str) -> str:
    """Türkçe küçültme: Python'un lower()'ı I→ı, İ→i yaptığı için elle."""
    if not metin:
        return metin
    ilk = {"I": "ı", "İ": "i"}.get(metin[0], metin[0].lower())
    return ilk + metin[1:]


def uygula(kayitlar: list, figurler: dict) -> int:
    paket = kayitlar[0]
    etiketler = dict(paket.get("labels") or {})
    indeks = {k.get("id"): k for k in kayitlar}
    eklendi = 0
    for soru_id, tanim in figurler.items():
        q = indeks.get(soru_id)
        if q is None:
            raise ValueError(f"bulunamadı: {soru_id}")
        if q.get("figure"):
            continue
        fig, duz = figur_kur(soru_id, tanim, etiketler)
        kok_dogrula(soru_id, q["question"], duz)
        cevap_sizmasin(soru_id, q["choices"][q["correct"]], duz)
        metin = alt_metin(tanim)
        a = anahtar(soru_id, metin)
        etiketler[a] = metin
        fig["altTextKey"] = a
        q["figure"] = fig
        # §6.1: atıf figürle AYNI işlemde eklenir.
        onek = ATIF[fig["kind"]]
        if not q["question"].startswith(tuple(ATIF.values())):
            q["question"] = onek + kucult_ilk(q["question"])
        eklendi += 1
    paket["labels"] = etiketler
    return eklendi


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaz", action="store_true")
    ns = ap.parse_args(argv)

    kayitlar = [json.loads(s) for s in
                PAKET.read_text(encoding="utf-8").splitlines() if s.strip()]
    eklendi = uygula(kayitlar, FIGURLER)

    paket = kayitlar[0]
    sorular = [k for k in kayitlar if k.get("type") == "question"]
    figurlu = sum(1 for q in sorular if q.get("figure"))
    paket["contractPolicy"]["minFiguredQuestions"] = figurlu
    print(f"  eklenen figür       {eklendi}")
    print(f"  figürlü soru        {figurlu}/{len(sorular)}")

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
