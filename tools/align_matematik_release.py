#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matematik paketini Türkçe yayın onarımının sıkılaştırdığı 2.2 biçimine taşır.

Matematik dalı, Türkçe'nin son yayın onarımından (8b56eca) ÖNCE dallandığı için
sözleşmenin eski biçimine göre üretildi. Onarım üç kuralı sıkılaştırdı ve
matematik birleşme sonrası 1038 HATA verdi:

  kural 57 (46)  not gövdesi artık dokuz bölümlü NESNE değil: ``body`` uygulamanın
                 doğrudan gösterdiği düz metin, dokuz bölüm ``lessonSections``
                 altında durur. Uygulama ham JSON gösteremez, denetleyici de
                 pedagojik bölümleri kaybetmemeli; ikisi bir arada tutulur.
  kural 48 (523) ``noteKey`` artık ayrı bir slug değil, uygulamanın açacağı notun
                 tam kimliği: notta id == noteId == noteKey, soruda
                 noteId == noteKey. Ayrıştıklarında uygulama doğru notu yanlış
                 ekranda arar.
  kural 19 (469) 2.2'de doğru seçeneğin gerekçesi yalnız sonuç etiketi olamaz.
                 Matematikte 469 soruda gerekçe tek sözcüktü: "doğru". Bu, neden
                 doğru olduğunu söylemez; çocuk cevabı görür, çözümü görmez.

Bu araç İÇERİK ÜRETMEZ, mevcut içeriği taşır:

  * dokuz bölüm olduğu gibi ``lessonSections``a taşınır, ``body`` Türkçe ile AYNI
    işlevle (``repair_turkce_release.render_lesson_body``) üretilir — biçim iki
    ders arasında elle kopyalanırsa kaçınılmaz olarak birbirinden ayrılır.
  * ``noteKey`` kimliğe eşitlenir. Kimlikler KORUNUR: nokta ayraçlı eski not
    kimlikleri (``tr.g05.mat.5.1.1.note.01``) ID_KARAKTER_RE'ye uyuyor, bu yüzden
    yeniden adlandırmaya gerek yok. Eski slug ``subtopicKey``te zaten duruyor.
  * doğru seçenek gerekçesi sorunun kendi ``explanation`` alanından kurulur.
    Bu uydurma değil: explanation her soruda o sorunun somut çözümüdür ve
    Türkçe paketinde de gerekçe aynı biçimde ("Doğru seçenektir; …") kurulmuş.
    Zaten somut gerekçe taşıyan 31 soruya (A3/A4'te yeniden üretilenler)
    dokunulmaz.

reviewStatus DEĞİŞTİRİLMEZ: matematik ``pending`` kalır. Üreten model kendi
çıktısına ``ai-verified`` yazamaz; damgayı bağımsız denetçi süreç vurur.

Kullanım:
    python tools/align_matematik_release.py --yaz
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from repair_turkce_release import render_lesson_body  # noqa: E402

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "matematik" / "matematik-tum.jsonl"

ETIKET_GEREKCE = {"doğru", "doğrudur", "doğru cevap", "doğru seçenek"}


def gerekce_kur(aciklama: str) -> str:
    """Doğru seçeneğin gerekçesini sorunun kendi çözümünden kurar."""
    metin = str(aciklama or "").strip()
    if not metin:
        raise ValueError("explanation boş; gerekçe uydurulamaz")
    return f"Doğru seçenektir; {metin}"


def etiket_mi(gerekce: object) -> bool:
    s = str(gerekce or "").strip()
    return len(s) < 8 or s.casefold() in ETIKET_GEREKCE


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaz", action="store_true")
    ns = ap.parse_args(argv)

    kayitlar = [json.loads(s) for s in
                PAKET.read_text(encoding="utf-8").splitlines() if s.strip()]

    not_sayaci = govde_sayaci = anahtar_sayaci = gerekce_sayaci = 0

    for k in kayitlar:
        tip = k.get("type")

        if tip == "note":
            not_sayaci += 1
            govde = k.get("body")
            if isinstance(govde, dict):
                k["lessonSections"] = govde
                k["body"] = render_lesson_body(govde)
                govde_sayaci += 1
            kimlik = k.get("id")
            if k.get("noteId") != kimlik or k.get("noteKey") != kimlik:
                k["noteId"] = kimlik
                k["noteKey"] = kimlik
                anahtar_sayaci += 1

        elif tip == "question":
            nid = k.get("noteId")
            if k.get("noteKey") != nid:
                k["noteKey"] = nid
                anahtar_sayaci += 1
            why = k.get("distractorWhy") or []
            dogru = k.get("correct")
            if isinstance(dogru, int) and 0 <= dogru < len(why):
                if etiket_mi(why[dogru]):
                    why[dogru] = gerekce_kur(k.get("explanation"))
                    gerekce_sayaci += 1

    print(f"  not                         {not_sayaci}")
    print(f"  gövde → lessonSections      {govde_sayaci}")
    print(f"  noteKey hizalanan kayıt     {anahtar_sayaci}")
    print(f"  somutlaştırılan gerekçe     {gerekce_sayaci}")

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
