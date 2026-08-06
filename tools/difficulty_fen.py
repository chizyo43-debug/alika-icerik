#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fen sorularının difficultyReason alanını sorunun kendi yapısından türetir.

Fen paketinde 500 sorunun 496'sı TEK şablonu taşıyordu:

    "<konu> konusunda <n>. düzeyde kavramı uygulama, kanıtı yorumlama veya
     seçenekleri karşılaştırma gerektirir."

Bu cümle hiçbir şey söylemez: üç beceriyi "veya" ile sıralayıp hepsini birden
iddia eder, ve konu adı dışında sorudan hiçbir iz taşımaz. Emirde istenen
ölçütler (adım sayısı, ön bilgi, kanıt yorumlama, çeldirici yakınlığı) bu
şablonda ölçülmüyor, yalnız adlandırılıyor.

Bu araç gerekçeyi SORUNUN KENDİ ÖLÇÜLEN YAPISINDAN kurar. Ölçülenler:

  * ``veri_sayisi``    kökte kaç ayrı ölçüm/değer verilmiş
  * ``karsilastirma``  kaç düzenek/deneme/örnek karşılaştırılıyor
  * ``kanit``          kök gözlem/deney/ölçüm anlatıyor mu
  * ``figur``          soruda okunacak bir görsel var mı
  * ``yakinlik``       doğru cevapla en yakın çeldiricinin sözcük örtüşmesi
  * ``ortak_govde``    bütün şıklar aynı sözcükle mi başlıyor
  * ``kavram``         bağlı notun alt konusu (ön bilgi çapası)

DÜRÜSTLÜK NOTU: bu cümleler tek tek elle yazılmadı; her birinin İÇERİĞİ o
sorunun ölçülen özelliklerinden geliyor ve o soru için doğrudur, ama cümle
KALIPLARI sınırlı bir kümeden seçiliyor. Elle yazılmış 500 gerekçenin yerini
tutmaz; şablonun yerini tutar. Bu ayrım pakette ve PR'da açıkça yazılıdır.

Aile ataması difficultyReason imzasından türediği için bu araçtan sonra
aileler yeniden atanır.

Kullanım:
    python tools/difficulty_fen.py --yaz
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pack_migrate_lib import AILE_TAVANI, slug  # noqa: E402


def aile_ata_fen(sorular: list) -> dict:
    """Soru kimliği → familyId. Aile: aynı kazanım + aynı zorluk düzeyi."""
    kumeler: dict = {}
    for q in sorular:
        kumeler.setdefault((q.get("objective"), q.get("level")), []).append(
            q["id"])
    atama: dict = {}
    for (kazanim, duzey), kimlikler in sorted(
            kumeler.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
        temel = f"{slug(kazanim, 30)}-d{duzey}"
        for parca, bas in enumerate(range(0, len(kimlikler), AILE_TAVANI), 1):
            fid = temel if parca == 1 else f"{temel}-{parca}"
            for kimlik in kimlikler[bas:bas + AILE_TAVANI]:
                atama[kimlik] = fid
    return atama

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "fen-bilimleri" / "fen-bilimleri-tum.jsonl"

ESKI_KALIP = "düzeyde kavramı uygulama, kanıtı yorumlama veya seçenekleri"

KANIT_RE = re.compile(
    r"\b(gözleml|gözlem|deney|ölçüyor|ölçer|ölçüm|inceli|karşılaştır|"
    r"kaydedi|denem)", re.I)
DUZENEK_RE = re.compile(
    r"\b(düzenek|deneme|kap|bardak|rampa|devre|yay|kutu|zemin|yüzey|grup|"
    r"örnek|hücre|kaşık|çubuk)\w*", re.I)
OLCUM_RE = re.compile(
    r"\d+\s*(?:°C|N|cm|mm|m|kg|g|gram|mL|L|litre|dakika|saniye|saat|bilye)")


def sadelestir(metin: str) -> list:
    s = unicodedata.normalize("NFKC", str(metin or "")).casefold()
    return [k for k in re.findall(r"[^\W\d_]+", s, flags=re.UNICODE)
            if len(k) > 3]


def yakinlik(dogru: str, celdiriciler: list) -> float:
    a = set(sadelestir(dogru))
    if not a:
        return 0.0
    en = 0.0
    for c in celdiriciler:
        b = set(sadelestir(c))
        if not b:
            continue
        en = max(en, len(a & b) / len(a | b))
    return en


def ortak_govde(siklar: list) -> str:
    ilkler = [sadelestir(s)[:1] for s in siklar]
    if all(i and i == ilkler[0] for i in ilkler):
        return ilkler[0][0]
    return ""


def gerekce_kur(q: dict, kavram: str) -> str:
    kok = q.get("question") or ""
    siklar = list(q.get("choices") or [])
    dogru_i = q.get("correct")
    dogru = siklar[dogru_i] if isinstance(dogru_i, int) else ""
    celdiriciler = [s for i, s in enumerate(siklar) if i != dogru_i]

    olcumler = OLCUM_RE.findall(kok)
    veri = len(set(re.findall(OLCUM_RE, kok))) or len(olcumler)
    duzenek = len(set(m.group(0).casefold() for m in DUZENEK_RE.finditer(kok)))
    kanit = bool(KANIT_RE.search(kok))
    figur = bool(q.get("figure"))
    yak = yakinlik(dogru, celdiriciler)
    govde = ortak_govde(siklar)

    parcalar = []

    # 1) Adım: kaç bilgiyi birlikte tutmak gerekiyor.
    if veri >= 3:
        parcalar.append(
            f"Kökte verilen {veri} ölçümü aynı anda karşılaştırmayı gerektirir")
    elif veri == 2:
        parcalar.append(
            "İki ölçümü karşılaştırıp aradaki ilişkiyi kurmayı gerektirir")
    elif duzenek >= 3:
        parcalar.append(
            f"{duzenek} ayrı düzeneği tek ölçüte göre sıralamayı gerektirir")
    elif duzenek == 2:
        parcalar.append(
            "İki düzenek arasında yalnız neyin değiştiğini görmeyi gerektirir")
    else:
        parcalar.append(
            f"{kavram} kavramını tek adımda uygulamayı gerektirir")

    # 2) Kanıt / görsel: bilginin nereden okunacağı.
    if figur and kanit:
        parcalar.append(
            "veri görselden okunup kökteki gözlemle birlikte yorumlanmalıdır")
    elif figur:
        parcalar.append("veri metinden değil görselden okunmalıdır")
    elif kanit:
        parcalar.append(
            "gözlem ile gözlemden çıkan sonuç birbirinden ayrılmalıdır")
    else:
        parcalar.append(f"{kavram} tanımının doğrudan hatırlanması gerekir")

    # 3) Çeldirici yakınlığı: elemenin neden kolay olmadığı.
    if govde:
        parcalar.append(
            f"dört şık da '{govde}' ile başladığı için sözcüğe bakarak "
            "eleme yapılamaz")
    elif yak >= 0.34:
        parcalar.append(
            "çeldiriciler doğru cevapla büyük ölçüde aynı sözcükleri "
            "kullandığından ayrım anlamda aranmalıdır")
    elif yak >= 0.15:
        parcalar.append(
            "çeldiricilerin en az biri doğru cevabın yarısını tekrarlar")
    else:
        parcalar.append(
            "çeldiriciler farklı kavramlardan geldiği için her birinin neyi "
            "adlandırdığı bilinmelidir")

    return parcalar[0] + "; " + parcalar[1] + " ve " + parcalar[2] + "."


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaz", action="store_true")
    ns = ap.parse_args(argv)

    kayitlar = [json.loads(s) for s in
                PAKET.read_text(encoding="utf-8").splitlines() if s.strip()]
    notlar = {k["id"]: k for k in kayitlar if k.get("type") == "note"}
    sorular = [k for k in kayitlar if k.get("type") == "question"]

    degisen = 0
    for q in sorular:
        eski = q.get("difficultyReason") or ""
        if ESKI_KALIP not in eski:
            continue          # A3/regen'de elle yazılanlara dokunma
        n = notlar.get(q.get("noteId"))
        kavram = (n or {}).get("topic") or q.get("topic") or "Konu"
        q["difficultyReason"] = gerekce_kur(q, kavram)
        degisen += 1

    # Aile ataması difficultyReason imzasından türüyordu; gerekçeler soruya
    # özgüleştiği an imza her soruda ayrışıyor ve 292 ailenin 208'i tek
    # soruluk çıkıyor. Tek soruluk aile, aile değil; kimliğin başka adıdır.
    # Matematikte aynı ölçüm yapılmış ve 'kazanım + düzey'e geçilmişti;
    # fen de oraya hizalanır (bkz. tools/migrate_matematik_22.py).
    aileler = aile_ata_fen(sorular)
    for q in sorular:
        q["familyId"] = aileler[q["id"]]

    from pack_migrate_lib import iskelet
    imzalar = {iskelet(q["difficultyReason"]) for q in sorular}
    aile_sayisi = len(set(aileler.values()))
    en_kalabalik = max(
        sum(1 for v in aileler.values() if v == f) for f in set(aileler.values()))
    tekil = sum(1 for f in set(aileler.values())
                if sum(1 for v in aileler.values() if v == f) == 1)
    print(f"  yeniden yazılan gerekçe  {degisen}")
    print(f"  benzersiz iskelet        {len(imzalar)}/500 (önce 32)")
    print(f"  aile                     {aile_sayisi} "
          f"(en kalabalık {en_kalabalik}, tek soruluk {tekil})")

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
