#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matematik 5. sınıf paketini Question Contract 2.0 → 2.2'ye taşır.

Türkçe'den üç farkı var:

1. Notlarda `unit` ve `skill` alanı YOK. Hiyerarşinin üst iki halkası kazanım
   kodunun kendisinden türetilir (MAT.5.1 → sayılar, 5.3 → geometri …).
   Bu anahtarlar İÇ hiyerarşi anahtarlarıdır, resmî ünite adı iddiası değil;
   resmî kod `objective` alanında olduğu gibi durur.

2. Cevap dağılımı bozuk: 125/131/121/123. Altı soru başka konuma taşınır.
   Taşıma, şıkkı ve gerekçesini AYNI işlemde döndürür — ayrı döndürmek
   d133631'in hatasıdır (çocuk bir şıkkı seçer, başka şıkkın gerekçesi çıkar).
   Açıklamalarda konuma bağlı ifade taranıp sıfır olduğu doğrulandı, yoksa
   döndürme metni yalanlardı.

3. `objectiveEvidenceId` beş yüz kayıtta da BOŞ. objectiveSource doğru 2024
   program PDF'i ama sayfa çapası yok; kanıt PENDING olur ve paket yayına
   kapanır.

Kullanım:
    python tools/migrate_matematik_22.py            # yalnız rapor
    python tools/migrate_matematik_22.py --yaz
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "matematik" / "matematik-tum.jsonl"

from pack_migrate_lib import (  # noqa: E402
    AILE_TAVANI, dagilimi_esitle, slug,
)


def aile_ata_matematik(sorular: list) -> dict:
    """Soru kimliği → familyId. Aile: aynı kazanım + aynı zorluk düzeyi.

    Türkçe'de aile (not + difficultyReason imzası) ile kuruldu ve orada
    işledi. Matematikte İŞLEMEZ: difficultyReason'lar A3 turunda soruya özgü
    yeniden yazıldığı için imza neredeyse her soruda ayrışıyor ve 380 ailenin
    310'u tek soruluk çıkıyor. Tek soruluk aile, aile değil; kimliğin başka
    adıdır ve ölçüyü anlamsızlaştırır.

    Ölçülen dört seçenek arasından bu seçildi:

        kök imzası              350 aile, 295'i tek soruluk
        not + kök imzası        352 aile, 299'u tek soruluk
        not                      74 aile, sözleşme tabanının altında
        kazanım + düzey         115 aile, yalnız 1'i tek soruluk   ← seçilen

    Aynı kazanımı aynı zorluk düzeyinde ölçen sorular gerçekten aynı ailedir
    ve en kalabalık küme zaten 8; tavan bölme gerektirmiyor.
    """
    kumeler: dict = {}
    for q in sorular:
        kumeler.setdefault((q.get("objective"), q.get("level")), []).append(q["id"])
    atama: dict = {}
    for (kazanim, duzey), kimlikler in sorted(
            kumeler.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
        temel = f"{slug(kazanim, 30)}-d{duzey}"
        for parca, bas in enumerate(range(0, len(kimlikler), AILE_TAVANI), 1):
            fid = temel if parca == 1 else f"{temel}-{parca}"
            for kimlik in kimlikler[bas:bas + AILE_TAVANI]:
                atama[kimlik] = fid
    return atama

# Kazanım kodunun ikinci basamağı → öğrenme alanı anahtarı.
# Bunlar iç hiyerarşi anahtarlarıdır; programın resmî ünite adı olduğu
# iddiasında değildir. Resmî kod `objective` alanında korunur.
ALAN_ANAHTARI = {
    "1": "sayilar-ve-nicelikler",
    "2": "islemler-ve-cebirsel-dusunme",
    "3": "geometrik-sekiller",
    "4": "geometrik-nicelikler",
    "5": "veri-isleme",
    "6": "olasilik",
}


def alan_kodu(objective: object) -> str:
    """MAT.5.3.2 → '3'. Kod okunamazsa boş döner ve çağıran karar verir."""
    m = re.match(r"^MAT\.\d+\.(\d+)", str(objective or ""))
    return m.group(1) if m else ""


def hiyerarsi_uret(notlar: list, sorular: list) -> dict:
    """Not kimliği → dört hiyerarşi anahtarı.

    Notların kendi `objective` alanı olmadığı için öğrenme alanı, o nota bağlı
    soruların kazanımından okunur. Not birden çok kazanıma hizmet ediyorsa en
    çok soruyu veren kazanım belirleyicidir.
    """
    not_kazanimlari: dict = {}
    for q in sorular:
        not_kazanimlari.setdefault(q.get("noteId"), []).append(q.get("objective"))

    harita: dict = {}
    kullanilan: set = set()
    for n in notlar:
        kazanimlar = not_kazanimlari.get(n["id"], [])
        baskin = max(set(kazanimlar), key=kazanimlar.count) if kazanimlar else ""
        alan = ALAN_ANAHTARI.get(alan_kodu(baskin), "genel")
        # Üst konu = kazanımın kendisi (MAT.5.3.2 → mat-5-3-2); alt konu =
        # notun konu başlığı. Böylece zincirin her halkası ayrı bilgi taşır.
        ust = slug(baskin, 24) or "genel"
        alt = slug(n.get("topic"), 44) or slug(n.get("title"), 44)
        temel = alt
        sayac = 2
        while alt in kullanilan:
            alt = f"{temel}-{sayac}"
            sayac += 1
        kullanilan.add(alt)
        harita[n["id"]] = {
            "unitKey": alan,
            "topicKey": ust,
            "subtopicKey": alt,
            "noteKey": alt,
        }
    return harita


def tasi(kayitlar: list) -> tuple[list, dict]:
    paket = next(k for k in kayitlar if k.get("type") == "pack")
    notlar = [k for k in kayitlar if k.get("type") == "note"]
    sorular = [k for k in kayitlar if k.get("type") == "question"]

    hedef = [len(sorular) // 4] * 4
    for i in range(len(sorular) - sum(hedef)):
        hedef[i] += 1
    tasinan = dagilimi_esitle(sorular, hedef)

    harita = hiyerarsi_uret(notlar, sorular)
    aileler = aile_ata_matematik(sorular)

    ipucu_silinen = 0
    for k in kayitlar:
        if k.get("type") == "pack":
            continue
        if "hints" in k:
            del k["hints"]
            ipucu_silinen += 1

        nid = k["id"] if k.get("type") == "note" else k.get("noteId")
        k.update(harita.get(nid, {}))
        k.setdefault("grade", paket.get("grade"))
        k.setdefault("subject", paket.get("subject"))

        if k.get("type") == "question":
            k["familyId"] = aileler[k["id"]]
            k.setdefault("tags", [
                t for t in (k.get("topic"), k.get("objective")) if t
            ])

        k["objectiveEvidenceId"] = "PENDING"
        k["sourceRefs"] = ["PENDING"]

        onceki = str(k.get("provenance") or "")
        k["reviewStatus"] = "pending"
        k["humanReviewed"] = False
        k["provenance"] = (
            "machine-migrated:claude-opus-5:2026-08:contract-2.2; "
            f"prior={onceki[:80]}"
        )
        for eski in ("contentHash", "reviewedHash", "reviewedBy"):
            k.pop(eski, None)

    dagilim = [0, 0, 0, 0]
    for q in sorular:
        dagilim[q["correct"]] += 1

    paket["schemaVersion"] = "2.2"
    paket["disclosure"] = "ai-generated-and-ai-reviewed-no-human-review"
    paket["publishBlocked"] = True
    paket["contractPolicy"] = {
        "questionCount": len(sorular),
        "minFamilies": 80,
        "maxPerFamily": AILE_TAVANI,
        "answerBalance": dagilim,
        "minFiguredQuestions": sum(1 for q in sorular if q.get("figure")),
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
        "dagilim_icin_tasinan": len(tasinan),
        "cevap_dagilimi": dagilim,
        "figurlu_soru": sum(1 for q in sorular if q.get("figure")),
    }
    return kayitlar, ozet


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaz", action="store_true")
    ns = ap.parse_args(argv)

    kayitlar = [json.loads(s) for s in
                PAKET.read_text(encoding="utf-8").splitlines() if s.strip()]
    kayitlar, ozet = tasi(kayitlar)
    for ad, deger in ozet.items():
        print(f"  {ad:22} {deger}")

    if [k for k in kayitlar if "hints" in k]:
        print("UYARI: hâlâ hints taşıyan kayıt var")
        return 1
    if ozet["cevap_dagilimi"] != [125, 125, 125, 125]:
        print(f"UYARI: dağılım hedefi tutmadı: {ozet['cevap_dagilimi']}")
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
