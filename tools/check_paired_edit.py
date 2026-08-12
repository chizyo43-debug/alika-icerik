#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_paired_edit.py — bağlı alanların birlikte değişmesini zorunlu kılar.

Neden var: bir sorunun ``choices`` alanı değişip ``distractorWhy`` olduğu gibi
bırakılırsa, gerekçe artık ekranda olmayan bir şıkkı anlatır. Öğrenciye
doğrudan yanlış bilgi gider. Bu hata dosyanın kendisine bakarak güvenilir
biçimde bulunamaz (okuduğunu anlama sorularında gerekçe şıkkı meşru olarak
parafraz eder), ama DEĞİŞİMİ görerek kesin biçimde bulunur.

Kullanım:
    python tools/check_paired_edit.py --base origin/main
    python tools/check_paired_edit.py --base HEAD~1 --paths turkiye/...

Çıkış kodu: ihlal varsa 1.

Kurallar (soru satırları için, id eşleşmesiyle):
  1. ``choices`` değiştiyse ``distractorWhy`` de değişmeli.
  2. ``correct`` değiştiyse ``distractorWhy`` ve ``explanation`` da değişmeli.
  3. ``choices`` değiştiyse ve ``explanation`` eski doğru şıkkın metnini
     anıyorsa ``explanation`` da değişmeli.
Stdlib-only; git'i alt süreç olarak çağırır.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def git_goster(revizyon: str, yol: str) -> str | None:
    """Verilen revizyondaki dosya içeriğini döner; dosya yoksa None."""
    try:
        cikti = subprocess.run(
            ["git", "show", f"{revizyon}:{yol}"],
            capture_output=True, check=True,
        )
    except subprocess.CalledProcessError:
        return None
    return cikti.stdout.decode("utf-8")


def sorulari_ayikla(ham: str) -> dict:
    """JSONL metninden {id: soru} sözlüğü üretir; bozuk satırları atlar."""
    sorular = {}
    for satir in ham.splitlines():
        satir = satir.strip()
        if not satir:
            continue
        try:
            kayit = json.loads(satir)
        except json.JSONDecodeError:
            continue  # bozuk satır pack_validate.py'nin işi
        if isinstance(kayit, dict) and kayit.get("type") == "question":
            kimlik = kayit.get("id")
            if kimlik:
                sorular[kimlik] = kayit
    return sorular


def degisen_dosyalar(base: str) -> list:
    cikti = subprocess.run(
        ["git", "diff", "--name-only", base, "--", "*.jsonl"],
        capture_output=True, check=True,
    )
    return [s for s in cikti.stdout.decode("utf-8").splitlines() if s.strip()]


BAGLI_ALANLAR = ("choices", "correct", "distractorWhy", "explanation")


def secenekleri_karsilastirma_icin_normallestir(secenekler: object) -> object:
    """JSON sayılarını aynı görünen metin şıklarıyla eşdeğer kabul eder.

    AliKa şıkları boş olmayan metin olarak saklar. Eski paketlerdeki ``48``
    sayısının ``"48"`` metnine kayıpsız taşınması, öğrencinin gördüğü seçeneği
    değiştirmez. Bool ve bileşik JSON değerleri özellikle dönüştürülmez.
    """
    if not isinstance(secenekler, list):
        return secenekler
    return [
        str(secenek)
        if isinstance(secenek, (int, float)) and not isinstance(secenek, bool)
        else secenek
        for secenek in secenekler
    ]


def dosyayi_denetle(base: str, yol: str, revert_of: str | None = None) -> list:
    ihlaller = []
    eski_ham = git_goster(base, yol)
    if eski_ham is None:
        return ihlaller  # yeni dosya; karşılaştırılacak taban yok
    yeni_yol = Path(yol)
    if not yeni_yol.exists():
        return ihlaller  # silinmiş dosya
    eski = sorulari_ayikla(eski_ham)
    yeni = sorulari_ayikla(yeni_yol.read_text(encoding="utf-8"))

    # Geri alma istisnası: bir düzenleme, bağlı alanları bilinen tutarlı bir
    # revizyondaki hâline birebir döndürüyorsa ihlal değildir. Bu bir bypass
    # değil, doğrulamadır — üçlü gerçekten o revizyonla aynı mı diye bakılır.
    hedef = {}
    if revert_of:
        hedef_ham = git_goster(revert_of, yol)
        if hedef_ham is not None:
            hedef = sorulari_ayikla(hedef_ham)

    for kimlik, y in yeni.items():
        e = eski.get(kimlik)
        if e is None:
            continue  # yeni soru
        h = hedef.get(kimlik)
        if h is not None and all(h.get(a) == y.get(a) for a in BAGLI_ALANLAR):
            continue  # bağlı alanlar bilinen tutarlı hâline geri döndürülmüş
        secenek_degisti = (
            secenekleri_karsilastirma_icin_normallestir(e.get("choices"))
            != secenekleri_karsilastirma_icin_normallestir(y.get("choices"))
        )
        dogru_degisti = e.get("correct") != y.get("correct")
        why_degisti = e.get("distractorWhy") != y.get("distractorWhy")
        exp_degisti = e.get("explanation") != y.get("explanation")

        if secenek_degisti and not why_degisti:
            ihlaller.append(
                f"{yol}:{kimlik}: choices değişti ama distractorWhy aynı kaldı; "
                "gerekçeler artık başka şıkları anlatıyor olabilir"
            )
        if dogru_degisti and not why_degisti:
            ihlaller.append(
                f"{yol}:{kimlik}: correct değişti ama distractorWhy aynı kaldı; "
                "'doğru' etiketi yanlış indekste"
            )
        if dogru_degisti and not exp_degisti:
            ihlaller.append(
                f"{yol}:{kimlik}: correct değişti ama explanation aynı kaldı"
            )
        if secenek_degisti and not exp_degisti:
            eski_secenekler = e.get("choices") or []
            eski_dogru = e.get("correct")
            aciklama = str(y.get("explanation") or "")
            if (
                isinstance(eski_dogru, int)
                and 0 <= eski_dogru < len(eski_secenekler)
                and str(eski_secenekler[eski_dogru]) in aciklama
                and str(eski_secenekler[eski_dogru])
                not in [str(c) for c in (y.get("choices") or [])]
            ):
                ihlaller.append(
                    f"{yol}:{kimlik}: choices değişti, explanation hâlâ artık "
                    f"bulunmayan {eski_secenekler[eski_dogru]!r} şıkkını anıyor"
                )
    return ihlaller


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(
        description="Bağlı alanların birlikte düzenlenmesini denetler")
    ap.add_argument("--base", default="origin/main",
                    help="karşılaştırma tabanı (varsayılan: origin/main)")
    ap.add_argument("--paths", nargs="*",
                    help="denetlenecek dosyalar; boşsa değişenler bulunur")
    ap.add_argument("--revert-of", dest="revert_of",
                    help="bağlı alanları bu revizyondaki hâline döndüren "
                         "düzenlemeler ihlal sayılmaz (birebir doğrulanır)")
    args = ap.parse_args(argv)

    yollar = args.paths or degisen_dosyalar(args.base)
    if not yollar:
        print("değişen .jsonl yok; denetim atlandı")
        return 0

    ihlaller = []
    for yol in yollar:
        ihlaller.extend(dosyayi_denetle(args.base, yol, args.revert_of))

    for ihlal in ihlaller:
        print(f"HATA {ihlal}")
    print(f"TOPLAM: {len(ihlaller)} bağlı-alan ihlali "
          f"({len(yollar)} dosya, taban {args.base})")
    return 1 if ihlaller else 0


if __name__ == "__main__":
    sys.exit(main())
