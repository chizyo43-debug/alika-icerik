#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A4'te eklenen 49 soru figürüne alt metin yazar (2.2 zorunluluğu).

2.0 alt metin istemiyordu, 2.2 istiyor: alt metni olmayan figür, ekran
okuyucu kullanan çocuk için var olmayan figürdür.

Alt metin figürün PARAMETRELERİNDEN üretilir ve bu güvenlidir, çünkü A4
partisinde figür yalnız soru kökünde ZATEN yazılı olan ölçü için üretildi:
kökte iki derece geçen ya da iki dikdörtgen karşılaştırılan sorular atlandı.
Dolayısıyla alt metnin söylediği her şey metinde de yazıyor.

Alt metin ALGIYI anlatır, ÇIKARIMI yapmaz. Bir açının kaç derece olduğunu
yazmak, o derece kökte geçtiği için sızıntı değildir; ama "geniş açıdır"
demek sınıflandırmayı soran sorunun cevabını vermek olurdu.

Kullanım:
    python tools/add_alt_text_matematik.py --yaz
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "matematik" / "matematik-tum.jsonl"


def alt_metin(fig: dict) -> str:
    kind = fig.get("kind")
    if kind == "angle":
        d = fig.get("degrees")
        return (f"Ortak bir köşeden çıkan iki ışın; ikinci ışın yatay "
                f"başlangıç ışınından {d} derece döndürülmüş olarak "
                f"çizilmiştir.")
    if kind == "grid":
        s, r = fig.get("cols"), fig.get("rows")
        return (f"{s} sütun ve {r} satırdan oluşan birim kare ızgarası; "
                f"kareler eşit büyüklüktedir.")
    if kind == "shape" and fig.get("type") == "rect":
        d = fig.get("dims") or {}
        w, h = d.get("w"), d.get("h")
        return (f"Uzun kenarı {w} birim, kısa kenarı {h} birim olan bir "
                f"dikdörtgen.")
    if kind == "shape":
        return f"{fig.get('type')} türünde bir geometrik şekil."
    return ""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaz", action="store_true")
    ns = ap.parse_args(argv)

    kayitlar = [json.loads(s) for s in
                PAKET.read_text(encoding="utf-8").splitlines() if s.strip()]
    paket = next(k for k in kayitlar if k.get("type") == "pack")
    etiketler = dict(paket.get("labels") or {})

    eklenen = 0
    atlanan = []
    for k in kayitlar:
        if k.get("type") != "question":
            continue
        fig = k.get("figure")
        if not isinstance(fig, dict) or "altTextKey" in fig:
            continue
        metin = alt_metin(fig)
        if not metin:
            atlanan.append(k["id"])
            continue
        ozet = hashlib.sha256(metin.encode("utf-8")).hexdigest()[:12]
        anahtar = f"{k['id']}.visual.{ozet}"
        etiketler[anahtar] = metin
        fig["altTextKey"] = anahtar
        eklenen += 1

    paket["labels"] = etiketler
    print(f"  alt metin eklenen figür  {eklenen}")
    print(f"  etiket anahtarı          {len(etiketler)}")
    if atlanan:
        print(f"  ALT METİN ÜRETİLEMEYEN   {atlanan}")
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
