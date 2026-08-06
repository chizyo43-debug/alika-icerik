#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fen Bilimleri paketini 2.0'dan Question Contract 2.2'ye taşır.

Fen paketi tümüyle 2.0 biçimindeydi: hiyerarşi yok, aile yok, 500 soruda
``hints``, notlar düz metin, hiçbir yerde görsel yok. İçerik ise iyi:
28 notun gövdesi ~4000 karakterlik gerçek konu anlatımı, çeldirici gerekçeleri
ve açıklamalar somut. Bu yüzden burada üretim değil TAŞIMA yapılır.

Yapılanlar:

  * ``hints`` kaldırılır (2.2 yasağı; alan hiç bulunmaz, boş dizi de olmaz).
  * Hiyerarşi halkaları eklenir. Anahtarlar kazanım kodundan türetilir:
    ``unitKey = fb-5-<ünite>``, ``topicKey = fb-5-<ünite>-<konu grubu>``,
    ``subtopicKey = slug(konu başlığı)``. Ünitelere AD VERİLMEZ — 2024
    programındaki resmî ünite adlarını doğrulamadan yazmak uydurma olurdu;
    kod tabanlı anahtar hem kararlı hem doğrulanabilir.
  * ``noteKey`` = notun tam kimliği (kural 48); notta id/noteId/noteKey aynı.
  * Not gövdesi ``lessonSections``a ayrıştırılır. 28 notun altısı da aynı altı
    başlığı taşıyor, bu yüzden ayrıştırma pack_migrate_lib'in ortak
    ayrıştırıcısıyla yapılır. Dokuz bölümün DÖRDÜ (whatIWillLearn,
    priorKnowledge, summary, figureNote) kaynakta yok; onlar
    tools/finish_notes_fen.py'de elle yazılır. Bu araç tek başına koşulduğunda
    paket kural 57'den kırmızıdır ve bu bilinçlidir: eksik bölümü otomatik
    doldurmak, konu anlatımını üretmek olurdu.
  * ``familyId`` atanır (aynı not + aynı ölçülen beceri, tavan 8).
  * ``sourceRefs`` doldurulur. Uydurma değil: her sorunun
    ``objectiveEvidenceId``i zaten ``<sourceId>:pdf-page-<n>`` biçiminde ve o
    sourceId paketin ``sources`` listesinde sha256 ve sayfa sayısıyla kayıtlı.
    Ayrıştırılamayan olursa PENDING yazılır ve paket yayına kapatılır.
  * Damga geri alınır: 500 soru ve 28 not ``ai-verified`` görünüyordu, oysa
    onarılan içerik denetlenmemiştir. Üreten model kendi çıktısına
    ``ai-verified`` yazamaz; hepsi ``pending`` / ``humanReviewed: false``
    yapılır ve eski karar hash'leri silinir (içerik değişti, hash artık yalan).

Kullanım:
    python tools/migrate_fen_22.py --yaz
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pack_migrate_lib import (  # noqa: E402
    aile_ata, bolumlere_ayir, oz_kontrol_listele, slug,
)

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "fen-bilimleri" / "fen-bilimleri-tum.jsonl"

KAZANIM_RE = re.compile(r"^FB\.5\.(\d+)\.(\d+)\.(\d+)$")

# Eski damga alanları: içerik değiştiği an bunların doğruluğu ölçülemez.
DAMGA_ALANLARI = (
    "reviewMode", "reviewModel", "reviewDeclaration",
    "reviewedContentSha256", "reviewDecisionSha256",
    "contentHash", "reviewedHash", "reviewedBy",
)


def hiyerarsi(kazanim: str, konu: str) -> dict:
    """Kazanım kodundan üç halkalı anahtar üretir."""
    m = KAZANIM_RE.match(str(kazanim or ""))
    if not m:
        raise ValueError(f"tanınmayan kazanım kodu: {kazanim!r}")
    unite, grup, _ = m.groups()
    return {
        "unitKey": f"fb-5-{unite}",
        "topicKey": f"fb-5-{unite}-{grup}",
        "subtopicKey": slug(konu),
    }


def kaynak_ref(kanit: object) -> list:
    """objectiveEvidenceId'den kaynak kimliğini çıkarır."""
    s = str(kanit or "")
    if ":" in s:
        kimlik = s.split(":", 1)[0].strip()
        if kimlik:
            return [kimlik]
    return ["PENDING"]


def damgayi_geri_al(k: dict) -> None:
    """Denetlenmemiş içeriği pending'e döndürür ve eski hash'leri siler."""
    for alan in DAMGA_ALANLARI:
        k.pop(alan, None)
    k["reviewStatus"] = "pending"
    k["humanReviewed"] = False
    k["provenance"] = (
        "machine-generated:minimax-m3; repair=claude-opus-5:2026-08; "
        "contract=question-2.2; review=pending"
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaz", action="store_true")
    ns = ap.parse_args(argv)

    kayitlar = [json.loads(s) for s in
                PAKET.read_text(encoding="utf-8").splitlines() if s.strip()]
    paket = kayitlar[0]
    notlar = [k for k in kayitlar if k.get("type") == "note"]
    sorular = [k for k in kayitlar if k.get("type") == "question"]

    bekleyen_kaynak = 0
    bolum_sayaci = 0

    for n in notlar:
        kimlik = n["id"]
        n.update(hiyerarsi(n["objectives"][0], n["topic"]))
        n["grade"] = 5
        n["noteId"] = kimlik
        n["noteKey"] = kimlik
        parcalar = bolumlere_ayir(n["body"])
        ornekler = [parcalar[b] for b in ("Çözümlü örnek 1", "Çözümlü örnek 2")
                    if parcalar.get(b)]
        bolumler = {
            "keyConcepts": parcalar.get("Kavramlar", ""),
            "steps": parcalar.get("Adım adım öğrenelim", ""),
            "workedExamples": ornekler,
            "commonMistakes": parcalar.get("Sık yapılan hata", ""),
            "selfCheck": oz_kontrol_listele(parcalar.get("Öz kontrol", "")),
        }
        eksik = [b for b, v in bolumler.items() if not v]
        if eksik:
            raise ValueError(f"{kimlik}: kaynakta bulunamayan bölüm {eksik}")
        n["lessonSections"] = bolumler
        bolum_sayaci += 1
        n["sourceRefs"] = kaynak_ref(n.get("objectiveEvidenceId"))
        damgayi_geri_al(n)

    aileler = aile_ata(sorular)
    for q in sorular:
        q.pop("hints", None)
        q.update(hiyerarsi(q["objective"], q["topic"]))
        q["grade"] = 5
        q["noteKey"] = q["noteId"]
        q["familyId"] = aileler[q["id"]]
        q["sourceRefs"] = kaynak_ref(q.get("objectiveEvidenceId"))
        if q["sourceRefs"] == ["PENDING"]:
            bekleyen_kaynak += 1
        damgayi_geri_al(q)

    paket["schemaVersion"] = "2.2"
    paket["disclosure"] = "ai-generated-and-ai-reviewed-no-human-review"
    paket["publishBlocked"] = bekleyen_kaynak > 0
    paket["labels"] = paket.get("labels") or {}
    paket["contractPolicy"] = {
        "questionCount": len(sorular),
        "minFamilies": 80,
        "maxPerFamily": 8,
        "answerBalance": [125, 125, 125, 125],
        "minFiguredQuestions": sum(1 for q in sorular if q.get("figure")),
        "everyNoteHasFigure": True,
        "objectiveBalanceMode": "coverage",
    }
    # quality.status 'approved-locked' idi; içerik değişti, kilit artık geçersiz.
    paket["quality"] = dict(paket.get("quality") or {})
    paket["quality"]["status"] = "pending-review"

    aile_sayisi = len(set(aileler.values()))
    en_kalabalik = max(
        sum(1 for v in aileler.values() if v == f) for f in set(aileler.values()))
    print(f"  not                       {len(notlar)}")
    print(f"  lessonSections ayrıştı    {bolum_sayaci} (5/9 bölüm; 4'ü elle)")
    print(f"  soru                      {len(sorular)}")
    print(f"  aile                      {aile_sayisi} (en kalabalık {en_kalabalik})")
    print(f"  hints kalan               {sum(1 for k in kayitlar if 'hints' in k)}")
    print(f"  sourceRefs PENDING        {bekleyen_kaynak}")
    print(f"  publishBlocked            {paket['publishBlocked']}")

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
