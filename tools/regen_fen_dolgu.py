#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kural 39'un altı dolgu çeldiricisine ev açar; bir kural 19 hatasını kapatır.

Kural 39 şunları işaretledi: 'organizma'×7, 'termometre'×7, 'cetvel'×6,
'hücre zarı'×5, 'çekirdek'×5, 'sitoplazma'×4 — hepsi pakette dolaşıyor ve
HİÇBİR soruda doğru cevap değil. Zararı, kalıbı fark eden öğrencinin bu
seçenekleri okumadan eleyebilmesidir; etkin şık sayısı dörtten üçe düşer.

Kökü ölçüldü ve tek bir şeydi: KAPALI SEÇENEK HAVUZU.

  * q0173, q0187, q0192 aynı soruydu ("hangi yapı yalnız bitki hücresinde
    bulunur?"). Üçünde de doğru cevap ayırt edici yapı, çeldiriciler ise
    değişmez biçimde ortak yapılardı. Ortak yapılar hiç sorulmadığı için
    hem dolgu oldular hem de notun yarısı (ortak yapılar) hiç ölçülmedi.
  * q0096 dört kez tekrarlanan "kuvvet hangi araçla ölçülür?" kalıbındandı;
    cetvel ve termometre orada sürekli yanlış araçtı.
  * q0213, q0194'ün birebir tekrarıydı; 'organizma' zincirin son halkası
    olmasına rağmen hiç doğru cevap değildi.

Onarım değeri silmek değil, ona pakette bir ev bulmaktır (matematikte
öğrenilen ders, tools/regen_mat_dolgu.py). Burada ev açmak aynı zamanda
gerçek bir tekrarı da kaldırıyor: üç özdeş soru üç farklı şey soruyor artık.

Doğru cevabın KONUMU korunur; şık ve gerekçe birlikte yazılır (§1 atomiklik).

Ayrıca q0234'ün doğru gerekçesi 'doğru;' diye yarım kalmıştı (kural 19).

Kullanım:
    python tools/regen_fen_dolgu.py --yaz
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "fen-bilimleri" / "fen-bilimleri-tum.jsonl"

YENILER = {
"tr-g05-fen-q0173": {
 "kok": "Bitki ve hayvan hücrelerinin ikisinde de bulunan, hücreyi çevreleyen "
        "ve madde alışverişinin düzenlenmesine yardım eden yapı hangisidir?",
 "siklar": ["Hücre zarı", "Hücre duvarı", "Kloroplast", "Koful"],
 "dogru": "Hücre zarı",
 "gerekce": {
   "Hücre duvarı": "Hücre duvarı da hücreyi çevreler ama yalnız bitki "
                   "hücresinde bulunur; iki hücrede birden aranıyordu.",
   "Kloroplast": "Kloroplast besin üretimiyle ilgilidir ve yalnız bitki "
                 "hücresinde bulunur; hücreyi çevrelemez.",
   "Koful": "Koful hücre içinde madde depolar; hücreyi çevreleyen sınır "
            "değildir."},
 "aciklama": "Hücre zarı hem bitki hem hayvan hücresinde bulunur, hücreyi "
             "çevreler ve içeri girip çıkan maddelerin denetlenmesine "
             "yardım eder.",
 "zorluk": "İki ölçütü aynı anda tutmayı gerektirir: yapı hem ortak olmalı "
           "hem çevreleyici olmalı. Üç çeldiricinin her biri ölçütlerden "
           "yalnız birini karşılıyor, bu yüzden tek ölçüte bakan öğrenci "
           "yanılır.",
},
"tr-g05-fen-q0187": {
 "kok": "Hücrede yaşamsal olayların çoğunun gerçekleştiği, hücre içindeki "
        "yapıların bulunduğu bölüm hangisidir?",
 "siklar": ["Hücre duvarı", "Kloroplast", "Sitoplazma", "Hücre zarı"],
 "dogru": "Sitoplazma",
 "gerekce": {
   "Hücre duvarı": "Hücre duvarı dıştaki sert destek katmanıdır; içinde "
                   "hücresel yapılar bulunmaz.",
   "Kloroplast": "Kloroplast sitoplazma içinde bulunan bir yapıdır; "
                 "yapıları barındıran bölümün kendisi değildir.",
   "Hücre zarı": "Hücre zarı sınırı çizer; yaşamsal olayların geçtiği "
                 "bölüm onun içidir."},
 "aciklama": "Sitoplazma, hücre zarının içini dolduran ve hücresel "
             "yapıların bulunduğu bölümdür; birçok yaşamsal olay burada "
             "gerçekleşir.",
 "zorluk": "İçinde bulunan ile içine alan arasındaki ilişkiyi ayırmayı "
           "gerektirir. Kloroplast çeldiricisi tam bu karışıklığı temsil "
           "eder: doğru cevabın içinde yer alan bir yapıdır.",
},
"tr-g05-fen-q0192": {
 "kok": "Hem bitki hem hayvan hücresinde bulunan ve hücrenin yönetiminde "
        "görev alan yapı hangisidir?",
 "siklar": ["Kloroplast", "Hücre duvarı", "Koful", "Çekirdek"],
 "dogru": "Çekirdek",
 "gerekce": {
   "Kloroplast": "Kloroplast yalnız bitki hücresinde bulunur ve besin "
                 "üretimiyle ilgilidir; yönetim görevi yoktur.",
   "Hücre duvarı": "Hücre duvarı yalnız bitki hücresinde bulunur ve destek "
                   "sağlar.",
   "Koful": "Koful iki hücrede de bulunabilir ama görevi depolamadır, "
            "yönetim değildir."},
 "aciklama": "Çekirdek hem bitki hem hayvan hücresinde bulunur ve hücrenin "
             "yönetilmesinde görev alır.",
 "zorluk": "Üç çeldiricinin ikisi 'ortak olma' ölçütünde, biri 'görev' "
           "ölçütünde eleniyor; iki ölçütü birden uygulamayı gerektirdiği "
           "için tek bilgiyle çözülmez.",
},
"tr-g05-fen-q0213": {
 "kok": "Bir canlıda sindirim, dolaşım ve solunum sistemlerinin uyumlu "
        "biçimde birlikte çalışmasıyla ortaya çıkan yapı düzeyi hangisidir?",
 "siklar": ["Organizma", "Sistem", "Organ", "Doku"],
 "dogru": "Organizma",
 "gerekce": {
   "Sistem": "Sistem, birlikte çalışan organlardan oluşur; soruda "
             "sistemlerin kendisi birleşiyor, yani bir üst düzey aranıyor.",
   "Organ": "Organ, farklı dokuların bir araya gelmesiyle oluşur ve "
            "sistemden bir alt düzeydedir.",
   "Doku": "Doku, benzer hücrelerin bir araya gelmesidir ve zincirin en alt "
           "basamaklarındandır."},
 "aciklama": "Bütün sistemlerin uyumlu çalıştığı canlı bireye organizma "
             "denir; zincirin en üst basamağıdır.",
 "zorluk": "Zincirde bir basamak yukarı çıkmayı gerektirir. Çeldiricilerin "
           "üçü de zincirin gerçek basamakları olduğu için sıralamayı "
           "ezberlemek yetmez, hangi basamakta olunduğunu bilmek gerekir.",
 "fig": ("tablo", ["Canlıdaki sistem", "Durumu"],
   [["Sindirim sistemi", "Uyumlu çalışıyor"],
    ["Dolaşım sistemi", "Uyumlu çalışıyor"],
    ["Solunum sistemi", "Uyumlu çalışıyor"]]),
},
# q0213'ü değiştirmek 'Sistem'in TEK evini aldı ve uyarı yer değiştirdi —
# matematikte belgelenen tuzağın aynısı. Doğru yöntem: cevabı BAŞKA evi olan
# bir soruyu bağışçı seçmek. q0199'un cevabı 'Organ' idi ve 'Organ' q0208'de
# de doğru; bu yüzden 'Sistem'e ev q0199'da açıldı.
"tr-g05-fen-q0199": {
 "kok": "Belirli bir görevi birlikte yerine getiren organların oluşturduğu "
        "yapı düzeyi hangisidir?",
 "siklar": ["Hücre", "Doku", "Sistem", "Organizma"],
 "dogru": "Sistem",
 "gerekce": {
   "Hücre": "Hücre zincirin en küçük halkasıdır; organlardan değil, "
            "organlar ondan oluşur.",
   "Doku": "Doku benzer hücrelerin bir araya gelmesidir; organdan bir alt "
           "basamaktır.",
   "Organizma": "Organizma bütün sistemlerin uyumlu çalıştığı canlı "
                "bireydir; organlardan bir değil iki basamak yukarıdadır."},
 "aciklama": "Birlikte çalışan organlar bir sistemi oluşturur; sindirim "
             "sistemi mide, karaciğer ve pankreas gibi organlardan kurulur.",
 "zorluk": "Zincirde organdan tam bir basamak yukarı çıkmayı gerektirir. "
           "'Organizma' çeldiricisi iki basamak birden atlayan öğrenciyi, "
           "'doku' ise yönü ters çeviren öğrenciyi temsil eder.",
},
"tr-g05-fen-q0336": {
 "kok": "Bir öğrenci çayın ne kadar sıcak olduğunu sayı ile belirtmek "
        "istiyor. Bunun için hangi aracı kullanmalıdır?",
 "siklar": ["Dinamometre", "Eşit kollu terazi", "Kronometre", "Termometre"],
 "dogru": "Termometre",
 "gerekce": {
   "Dinamometre": "Dinamometre kuvvet ölçer ve newton gösterir; sıcaklıkla "
                  "ilgisi yoktur.",
   "Eşit kollu terazi": "Terazi kütle ölçer; sıcak bir çayın kütlesi "
                        "sıcaklığını söylemez.",
   "Kronometre": "Kronometre süre ölçer; çayın ne kadar beklediğini verir, "
                 "ne kadar sıcak olduğunu değil."},
 "aciklama": "Sıcaklık ölçülebilir bir büyüklüktür ve termometreyle "
             "ölçülür; sonuç santigrat derece ile yazılır.",
 "zorluk": "Dokunarak hissetmek ile sayı ile belirtmek arasındaki farkı "
           "görmeyi gerektirir. Üç çeldirici de gerçek ölçüm araçlarıdır, "
           "bu yüzden 'araç değil' diyerek elenemezler; her birinin hangi "
           "büyüklüğü ölçtüğü bilinmelidir.",
},
"tr-g05-fen-q0096": {
 "kok": "Bir öğrenci yaptığı dinamometrenin ölçeğini oluştururken yayın "
        "uzama miktarını santimetre cinsinden ölçmek istiyor. Bunun için "
        "hangi aracı kullanmalıdır?",
 "siklar": ["Dinamometre", "Termometre", "Kronometre", "Cetvel"],
 "dogru": "Cetvel",
 "gerekce": {
   "Dinamometre": "Dinamometre uygulanan kuvveti ölçer; burada ölçülmek "
                  "istenen yayın ne kadar uzadığıdır.",
   "Termometre": "Termometre sıcaklık ölçer; yayın uzamasıyla ilgisi "
                 "yoktur.",
   "Kronometre": "Kronometre süre ölçer; uzama bir uzunluktur, süre "
                 "değildir."},
 "aciklama": "Yayın uzaması bir uzunluktur ve cetvelle santimetre cinsinden "
             "ölçülür; ölçek bu uzunluklar işaretlenerek kurulur.",
 "zorluk": "Aracın kendisi ile aracın yapımında ölçülen büyüklüğü ayırmayı "
           "gerektirir. Dinamometre çeldiricisi tam bu karışıklığı temsil "
           "eder: soruda geçen araç odur ama ölçülen büyüklük onun değil.",
},
}

# Kural 19: doğru gerekçesi 'doğru;' diye yarım kalmıştı.
GEREKCE_ONARIMI = {
"tr-g05-fen-q0234":
  "Doğru; vücutta sert olan yapı kemik, yumuşak olup kasılıp gevşeyen yapı "
  "ise kastır. Öğrencinin hissettiği iki doku bu ikisidir.",
}


def anahtar_uret(soru_id: str, metin: str) -> str:
    import hashlib
    ozet = hashlib.sha256(metin.encode("utf-8")).hexdigest()[:12]
    return f"{soru_id}.visual.{ozet}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaz", action="store_true")
    ns = ap.parse_args(argv)

    kayitlar = [json.loads(s) for s in
                PAKET.read_text(encoding="utf-8").splitlines() if s.strip()]
    paket = kayitlar[0]
    etiketler = dict(paket.get("labels") or {})
    indeks = {k.get("id"): k for k in kayitlar}

    for kid, y in YENILER.items():
        q = indeks[kid]
        konum = q["correct"]
        siklar = list(y["siklar"])
        assert len(set(siklar)) == 4, f"{kid}: şık tekrarı"
        assert siklar[konum] == y["dogru"], (
            f"{kid}: doğru şık {konum}. konumda değil")
        gerekceler = []
        for i, s in enumerate(siklar):
            if i == konum:
                gerekceler.append(f"Doğru; {y['aciklama'][0].lower()}"
                                  f"{y['aciklama'][1:]}")
            else:
                assert s in y["gerekce"], f"{kid}: {s!r} gerekçesi yok"
                gerekceler.append(y["gerekce"][s])
        q.update(question=y["kok"], choices=siklar, distractorWhy=gerekceler,
                 explanation=y["aciklama"], difficultyReason=y["zorluk"],
                 reviewStatus="pending", humanReviewed=False,
                 provenance="machine-generated:claude-opus-5:2026-08; "
                            "contract=question-2.2; review=pending; "
                            "sebep=kural39-deger-evi")
        if "fig" in y:
            _, basliklar, satirlar = y["fig"]

            def et(metin: str) -> str:
                a = anahtar_uret(kid, metin)
                etiketler[a] = metin
                return a

            fig = {"kind": "table",
                   "headerKeys": [et(b) for b in basliklar],
                   "rows": [[{"key": et(h)} for h in s] for s in satirlar]}
            alt = (f"{len(satirlar)} satırlık tablo. Sütunlar: "
                   + ", ".join(f"'{b}'" for b in basliklar) + ". Satırlar: "
                   + "; ".join(" — ".join(s) for s in satirlar) + ".")
            a = anahtar_uret(kid, alt)
            etiketler[a] = alt
            fig["altTextKey"] = a
            q["figure"] = fig
            q["question"] = "Verilen tabloya göre, " + y["kok"][0].lower() + y["kok"][1:]

    for kid, metin in GEREKCE_ONARIMI.items():
        q = indeks[kid]
        q["distractorWhy"][q["correct"]] = metin

    # Yetim etiket bırakma (kural 25 / 51).
    kullanilan: set = set()

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
    dagilim = [0, 0, 0, 0]
    for q in sorular:
        dagilim[q["correct"]] += 1
    print(f"  yeniden üretilen soru  {len(YENILER)}")
    print(f"  gerekçe onarımı        {len(GEREKCE_ONARIMI)}")
    print(f"  silinen yetim etiket   {len(yetim)}")
    print(f"  cevap dağılımı         {dagilim}")
    if dagilim != [125, 125, 125, 125]:
        print("  ! dağılım bozuldu")
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
