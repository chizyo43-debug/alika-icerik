#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometri ve veri ailelerine, soru kökünden okunabilen figürleri ekler.

İlke A4'ten devam ediyor: figür yalnız kökte ZATEN yazılı olan ölçüyü
görselleştirir. Metinde bulunmayan bir bilgiyi — özellikle aranan değeri —
figüre koymak soruyu çözer; ölçme biter, resme bakma başlar.

Belirsizse üretilmez, atlanır:
  * kökte iki derece geçiyorsa hangisinin çizildiği belli değildir
  * iki dikdörtgen karşılaştırılıyorsa tek şekil yanıltır
  * çokgenin kenar sayısı katalogda ifade edilemiyor (aşağıya bakınız)

KATALOG SINIRI: shape/polygon kenar sayısı taşımıyor; yalnız dims a,b,c var.
Bu yüzden MAT.5.3.5 ve MAT.5.3.6'nın çokgen sayma soruları sadık biçimde
çizilemiyor ve bu araç onlara figür ÜRETMİYOR. Yanlış kenar sayılı bir şekil,
figürsüz sorudan kötüdür: çocuk şekli sayar ve yanlış cevaba varır.

Figür ile kökteki atıf aynı işlemde üretilir (AUTHORING_RULES §6.1).

Kullanım:
    python tools/add_figures_mat_geo.py            # yalnız rapor
    python tools/add_figures_mat_geo.py --yaz
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "matematik" / "matematik-tum.jsonl"

DERECE = re.compile(r"(\d+)\s*°")
YARICAP = re.compile(r"[Yy]arıçap\w*\s+(\d+)\s*cm")
CARPIM = re.compile(r"(\d+)\s*(?:m|cm)\s*×\s*(\d+)\s*(?:m|cm)")
ESKENAR = re.compile(r"kenarı\s+(\d+)\s*cm")
KATEGORI = re.compile(r"([A-Za-zÇĞİÖŞÜçğıöşü]{3,})\s+(\d+)")

ATIF_ONEKI = "Verilen şekle göre, "


def _kucult_ilk(harf: str) -> str:
    """Türkçe küçültme: I → ı, İ → i. Python'un lower()'ı bunu yapmaz."""
    if harf == "I":
        return "ı"
    if harf == "İ":
        return "i"
    return harf.lower()


def atif_ekle(kok: str) -> str:
    if not kok or kok.startswith(ATIF_ONEKI):
        return kok
    return ATIF_ONEKI + _kucult_ilk(kok[0]) + kok[1:]


def figur_ve_alt(q: dict):
    """(figür, alt metin) döner; üretilemiyorsa (None, None)."""
    kok = q["question"]
    obj = q.get("objective", "")

    dereceler = [int(d) for d in DERECE.findall(kok)]
    dereceler = [d for d in dereceler if 0 < d <= 360]
    if len(dereceler) == 1:
        d = dereceler[0]
        return ({"kind": "angle", "degrees": d},
                f"Ortak bir köşeden çıkan iki ışın; ikinci ışın yatay "
                f"başlangıç ışınından {d} derece döndürülmüş olarak "
                f"çizilmiştir.")

    m = YARICAP.search(kok)
    if m and len(YARICAP.findall(kok)) == 1:
        r = int(m.group(1))
        return ({"kind": "shape", "type": "circle", "dims": {"r": r}},
                f"Yarıçapı {r} santimetre olan bir çember.")

    carpimlar = CARPIM.findall(kok)
    if len(carpimlar) == 1:
        a, b = int(carpimlar[0][0]), int(carpimlar[0][1])
        if a > 0 and b > 0:
            return ({"kind": "shape", "type": "rect",
                     "dims": {"w": max(a, b), "h": min(a, b)}},
                    f"Uzun kenarı {max(a, b)} birim, kısa kenarı {min(a, b)} "
                    f"birim olan bir dikdörtgen.")

    if "eşkenar üçgen" in kok:
        kenarlar = [int(x) for x in ESKENAR.findall(kok)]
        if len(kenarlar) == 1:
            k = kenarlar[0]
            return ({"kind": "shape", "type": "triangle",
                     "dims": {"a": k, "b": k, "c": k}},
                    f"Üç kenarı da {k} santimetre olan bir eşkenar üçgen.")

    # Kategorik veri: "futbol 12, basketbol 9, voleybol 5, yüzme 4"
    if obj.startswith("MAT.5.5"):
        ciftler = KATEGORI.findall(kok)
        # Aynı kategori iki kez geçmemeli ve en az üç kategori olmalı.
        adlar = [a.lower() for a, _ in ciftler]
        if len(ciftler) >= 3 and len(set(adlar)) == len(adlar):
            adlar = [a for a, _ in ciftler]
            degerler = [int(v) for _, v in ciftler]
            if all(0 < v <= 1000 for v in degerler):
                ozet = ", ".join(f"{a} {v}" for a, v in zip(adlar, degerler))
                return ({"kind": "chart", "style": "bar",
                         "categoryKeys": adlar, "values": degerler},
                        f"Sütun grafiği; kategoriler ve sıklıkları: {ozet}.")
    return (None, None)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaz", action="store_true")
    ns = ap.parse_args(argv)

    kayitlar = [json.loads(s) for s in
                PAKET.read_text(encoding="utf-8").splitlines() if s.strip()]
    paket = next(k for k in kayitlar if k.get("type") == "pack")
    etiketler = dict(paket.get("labels") or {})

    eklenen = collections.Counter()
    for k in kayitlar:
        if k.get("type") != "question" or k.get("figure"):
            continue
        if not str(k.get("objective", "")).startswith(("MAT.5.3", "MAT.5.4",
                                                       "MAT.5.5")):
            continue
        fig, alt = figur_ve_alt(k)
        if not fig:
            continue
        if fig["kind"] == "chart":
            kat = []
            for ad in fig["categoryKeys"]:
                a = f"{k['id']}.visual.{hashlib.sha256(ad.encode()).hexdigest()[:12]}"
                etiketler[a] = ad
                kat.append(a)
            fig["categoryKeys"] = kat
        ozet = hashlib.sha256(alt.encode("utf-8")).hexdigest()[:12]
        anahtar = f"{k['id']}.visual.{ozet}"
        etiketler[anahtar] = alt
        fig["altTextKey"] = anahtar
        k["figure"] = fig
        k["question"] = atif_ekle(k["question"])
        eklenen[k["objective"]] += 1

    paket["labels"] = etiketler
    for obj in sorted(eklenen):
        print(f"  {obj}: {eklenen[obj]} figür")
    print(f"TOPLAM eklenen: {sum(eklenen.values())}")

    sorular = [k for k in kayitlar if k.get("type") == "question"]
    paket["contractPolicy"]["minFiguredQuestions"] = sum(
        1 for q in sorular if q.get("figure"))

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
