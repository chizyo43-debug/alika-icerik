#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Türkçe 5. sınıf paketini Question Contract 2.0 → 2.2'ye taşır.

Bu araç YALNIZ yapısal taşıma yapar. İçerik metnine (soru kökü, şıklar,
gerekçeler, açıklama) dokunmaz: paket 2.0 altında 0 HATA veriyor, 500 kökün
tamamı benzersiz ve jenerik çeldirici gerekçesi yok. "Mevcut kaliteli içeriği
topluca yeniden üretme" kuralı gereği kusursuz kayıtlar olduğu gibi kalır.

Yaptıkları:
  1. hints alanını kaldırır (2.2'de alan yoktur, boş dizi de yazılmaz).
  2. Hiyerarşi anahtarlarını türetir: tema → beceri alanı → konu → not.
  3. familyId atar; aile, sorunun NE ÖLÇTÜĞÜNE göre kurulur.
  4. Damgayı düşürür: değiştirilen kayıt 'ai-verified' kalamaz.
  5. Kazanım kanıtını PENDING'e çeker ve paketi yayına kapatır.

Kazanım kodları neden PENDING: paket `MEB-TYMM-2024` diyor ve
objectiveSource gerçekten 2024 program PDF'i. Ama kodlar (`T.O.5.5.`) o
programın kodları değil ve provenance zincirinde eşlemenin bir AI tarafından
yapıldığı yazıyor (`curriculum-mapped:codex`). objectiveEvidenceId de sayfa
çapası değil, 'program-web'. Doğrulanmamış bir eşlemeyi doğrulanmış gibi
bırakmak, uydurulmuş kaynaktan daha tehlikelidir; çünkü denetlenmiş görünür.
Belge tutulur, kanıt PENDING olur, paket yayına kapanır.

Kullanım:
    python tools/migrate_turkce_22.py            # yalnız rapor
    python tools/migrate_turkce_22.py --yaz      # dosyaya yaz
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "turkce" / "turkce-tum.jsonl"

# Ortak yardımcılar tek yerde: kopyalanmış bir slug ya da döndürme işlevi,
# birinde düzeltilip diğerinde unutulan bir kural demektir.
from pack_migrate_lib import AILE_TAVANI, aile_ata, iskelet, slug  # noqa: E402


def hiyerarsi_uret(notlar: list) -> dict:
    """Her not için (unitKey, topicKey, subtopicKey, noteKey) üretir."""
    harita: dict = {}
    kullanilan: set = set()
    for n in notlar:
        birim = slug(n.get("unit"), 56) or "ortak-beceriler"
        # "5-sinif-turkce-ortak-beceriler" gibi uzun başlıkları kısalt.
        birim = re.sub(r"^\d+-sinif-turkce-", "", birim)
        birim = re.sub(r"^(\d+)-tema-", r"tema-\1-", birim)
        ust = slug(n.get("skill"), 24) or "genel"
        alt = slug(n.get("topic"), 44) or slug(n.get("title"), 44)
        # Aynı slug iki nota düşerse ayrıştır: anahtar tekil olmalıdır.
        temel = alt
        sayac = 2
        while alt in kullanilan:
            alt = f"{temel}-{sayac}"
            sayac += 1
        kullanilan.add(alt)
        harita[n["id"]] = {
            "unitKey": birim,
            "topicKey": ust,
            # Bugün her alt konuya tam bir not düşüyor, bu yüzden ikisi aynı
            # değeri alıyor. Kalabalık notlar alt konulara bölündüğünde
            # ayrışacaklar; anahtar henüz yayımlanmadığı için değişebilir.
            "subtopicKey": alt,
            "noteKey": alt,
        }
    return harita


def tasi(kayitlar: list) -> tuple[list, dict]:
    """Kayıtları 2.2'ye taşır; (yeni kayıtlar, özet) döner."""
    paket = next(k for k in kayitlar if k.get("type") == "pack")
    notlar = [k for k in kayitlar if k.get("type") == "note"]
    sorular = [k for k in kayitlar if k.get("type") == "question"]

    harita = hiyerarsi_uret(notlar)
    aileler = aile_ata(sorular)

    dagilim = [0, 0, 0, 0]
    for q in sorular:
        d = q.get("correct")
        if isinstance(d, int) and 0 <= d < 4:
            dagilim[d] += 1

    ipucu_silinen = 0
    for k in kayitlar:
        if k.get("type") == "pack":
            continue
        if "hints" in k:
            del k["hints"]
            ipucu_silinen += 1

        nid = k["id"] if k.get("type") == "note" else k.get("noteId")
        k.update(harita.get(nid, {}))

        if k.get("type") == "question":
            k["familyId"] = aileler[k["id"]]
            k.setdefault("tags", [
                t for t in (k.get("topic"), k.get("objective")) if t
            ])

        # Kanıt zinciri: belge doğru, eşleme doğrulanmamış.
        k["objectiveEvidenceId"] = "PENDING"
        k["sourceRefs"] = ["PENDING"]

        # Değiştirilen kayıt 'ai-verified' kalamaz; damgayı ayrı, salt-okunur
        # bir inceleme vurur ve üretici kendi çıktısını damgalayamaz.
        onceki = str(k.get("provenance") or "")
        k["reviewStatus"] = "pending"
        k["humanReviewed"] = False
        k["provenance"] = (
            "machine-migrated:claude-opus-5:2026-08:contract-2.2; "
            f"prior={onceki[:80]}"
        )
        for eski in ("contentHash", "reviewedHash", "reviewedBy"):
            k.pop(eski, None)

    paket["schemaVersion"] = "2.2"
    paket["disclosure"] = "ai-generated-and-ai-reviewed-no-human-review"
    paket["publishBlocked"] = True
    paket["contractPolicy"] = {
        "questionCount": len(sorular),
        "minFamilies": 80,
        "maxPerFamily": AILE_TAVANI,
        "answerBalance": dagilim,
        # Türkçe'de soru figürü 0'dır ve bu ölçülmüş bir karardır, taviz
        # değil: sorular metin anlamaya dayanıyor, kökteki duyuru ve çizelge
        # metnin kendisi. Onları tabloya çevirmek bilgiyi önceden ayrıştırıp
        # sunmak olur ve ölçülen beceriyi ortadan kaldırır. Gerekçe:
        # tools/add_figures_turkce.py modül açıklaması.
        "minFiguredQuestions": 0,
        "everyNoteHasFigure": True,
    }
    paket.setdefault("labels", {})

    ozet = {
        "soru": len(sorular),
        "not": len(notlar),
        "hints_silinen": ipucu_silinen,
        "aile": len(set(aileler.values())),
        "en_kalabalik_aile": max(
            (sum(1 for v in aileler.values() if v == f)
             for f in set(aileler.values())), default=0),
        "cevap_dagilimi": dagilim,
    }
    return kayitlar, ozet


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaz", action="store_true", help="dosyaya yaz")
    ns = ap.parse_args(argv)

    kayitlar = [json.loads(s) for s in
                PAKET.read_text(encoding="utf-8").splitlines() if s.strip()]
    kayitlar, ozet = tasi(kayitlar)

    for ad, deger in ozet.items():
        print(f"  {ad:20} {deger}")

    kalan = [k for k in kayitlar if "hints" in k]
    if kalan:
        print(f"UYARI: hâlâ hints taşıyan kayıt: {len(kalan)}")
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
