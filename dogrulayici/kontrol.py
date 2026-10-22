#!/usr/bin/env python3
"""AliKa içerik deposu kalite kapısı.

Her turkiye/*/*/*.jsonl paketini uygulamanın doğrulayıcısıyla (dogrulayici/tools/pack_validate.py) denetler.
- HATA: bilinen-bulgular.json'da kayıtlı olmayan her HATA kapıyı düşürür (yeni hata yok kuralı).
  Bilinen bulgular uygulama ekibine raporlanmış yanlış alarmlardır; düzeldikçe listeden çıkar.
- ilkokul/*/*.jsonl görsel etkinlik paketleri ders paketi değildir (pack_validate kuralları uymaz); her sorusu
  uygulamanın visualChoice sözleşmesinden (dogrulayici/windows/visual_choice.py) geçmeli. Bilinen bulgu yoktur.
- KATALOG.json: paket listesi, soru sayıları ve sha256 değerleri dosyalarla birebir olmalı.

Kullanım:
  python dogrulayici/kontrol.py               # denetle (CI)
  python dogrulayici/kontrol.py --katalog-yaz # yeni/ değişen paketten sonra KATALOG.json'u yeniden üret
  python dogrulayici/kontrol.py --temel-yaz   # bilinen bulguları şimdiki duruma eşitle (yalnız onaylı yanlış alarmlar için)
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
TEMEL = KOK / "dogrulayici" / "bilinen-bulgular.json"
KATALOG = KOK / "KATALOG.json"

_spec = importlib.util.spec_from_file_location("pack_validate", KOK / "dogrulayici" / "tools" / "pack_validate.py")
pv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pv)
_vspec = importlib.util.spec_from_file_location("visual_choice", KOK / "dogrulayici" / "windows" / "visual_choice.py")
vc = importlib.util.module_from_spec(_vspec)
_vspec.loader.exec_module(vc)


def paketler() -> list[Path]:
    return sorted((KOK / "turkiye").glob("*/*/*.jsonl"))


def ilkokul_paketleri() -> list[Path]:
    return sorted((KOK / "ilkokul").glob("*/*.jsonl"))


def kayitlar(yol: Path) -> list[dict]:
    return [json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines() if s.strip()]


def gorsel_hatalari() -> list[str]:
    """İlkokul görsel paketleri: pack başlığı, tekil id ve her sorunun visualChoice sözleşmesi."""
    hatalar = []
    for yol in ilkokul_paketleri():
        rel = yol.relative_to(KOK).as_posix()
        satir = kayitlar(yol)
        if not satir or satir[0].get("type") != "pack":
            hatalar.append(f"{rel}|paket|ilk satır pack başlığı değil")
            continue
        labels = satir[0].get("labels") or {}
        sorular = [r for r in satir if r.get("type") == "question"]
        if not sorular:
            hatalar.append(f"{rel}|paket|soru yok")
        idler: set = set()
        for r in sorular:
            kid = r.get("id")
            if kid in idler:
                hatalar.append(f"{rel}|{kid}|id tekrarı")
            idler.add(kid)
            try:
                vc.validate_visual_choice(r.get("visualChoice"), r.get("choices"), r.get("correct"), labels)
            except ValueError as e:
                hatalar.append(f"{rel}|{kid}|{e}")
    return hatalar


def kayit_kimligi(yol: Path) -> dict[int, str]:
    kim = {}
    for i, s in enumerate(yol.read_text(encoding="utf-8").splitlines(), 1):
        if s.strip():
            try:
                kim[i] = json.loads(s).get("id", "")
            except json.JSONDecodeError:
                kim[i] = ""
    return kim


def bulgular() -> tuple[set, int]:
    """(HATA anahtarları, UYARI sayısı). Anahtar: yol|kayıt kimliği|kural|mesaj — satır kaymasından etkilenmez."""
    hatalar, uyari = set(), 0
    for yol in paketler():
        kim = kayit_kimligi(yol)
        for b in pv.validate_file(yol):
            if b.seviye == "HATA":
                hatalar.add(f"{yol.relative_to(KOK).as_posix()}|{kim.get(b.satir, 'paket')}|{b.kural}|{b.mesaj}")
            elif b.seviye == "UYARI":
                uyari += 1
    return hatalar, uyari


def katalog_uret() -> dict:
    eski = json.loads(KATALOG.read_text(encoding="utf-8")) if KATALOG.exists() else {}
    liste = []
    for yol in paketler():
        veri = yol.read_bytes()
        satir = [json.loads(s) for s in veri.decode("utf-8").splitlines() if s.strip()]
        bas = next((r for r in satir if r.get("type") == "pack"), {})
        rel = yol.relative_to(KOK)
        liste.append({
            "yol": rel.as_posix(), "paketId": bas.get("id"), "sinif": int(rel.parts[1].split("-")[0]),
            "ders": bas.get("subject"), "dersKlasoru": rel.parts[2], "lang": bas.get("lang"),
            "schemaVersion": bas.get("schemaVersion"), "curriculum": bas.get("curriculum"),
            "soru": sum(1 for r in satir if r.get("type") == "question"),
            "not": sum(1 for r in satir if r.get("type") == "note"),
            "reviewStatus": bas.get("reviewStatus"), "sha256": hashlib.sha256(veri).hexdigest()})
    liste.sort(key=lambda k: (k["sinif"], k["dersKlasoru"], k["yol"]))
    ilkokul = []
    for yol in ilkokul_paketleri():
        satir = kayitlar(yol)
        bas = next((r for r in satir if r.get("type") == "pack"), {})
        sorular = [r for r in satir if r.get("type") == "question"]
        yaslar = [r["ageBand"] for r in sorular if isinstance(r.get("ageBand"), list) and len(r["ageBand"]) == 2]
        rel = yol.relative_to(KOK)
        ilkokul.append({
            "yol": rel.as_posix(), "paketId": bas.get("id"), "tur": rel.parts[1], "lang": bas.get("lang"),
            "yas": [min(a for a, _ in yaslar), max(b for _, b in yaslar)] if yaslar else None,
            "soru": len(sorular), "reviewStatus": bas.get("reviewStatus"),
            "sha256": hashlib.sha256(yol.read_bytes()).hexdigest()})
    return {"ulke": eski.get("ulke", "Türkiye"), "kapsam": eski.get("kapsam", "ortaokul 5–8"),
            "ogretimYili": eski.get("ogretimYili", "2026–2027"), "paketSayisi": len(liste),
            "soruSayisi": sum(k["soru"] for k in liste), "paketler": liste, "ilkokul": ilkokul}


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if "--katalog-yaz" in argv:
        KATALOG.write_text(json.dumps(katalog_uret(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("KATALOG.json yazıldı")
        return 0
    hatalar, uyari = bulgular()
    if "--temel-yaz" in argv:
        TEMEL.write_text(json.dumps(sorted(hatalar), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"bilinen-bulgular.json: {len(hatalar)} kayıt")
        return 0
    temel = set(json.loads(TEMEL.read_text(encoding="utf-8"))) if TEMEL.exists() else set()
    yeni = sorted(hatalar - temel)
    duzelen = len(temel - hatalar)
    sorun = 0
    for h in yeni:
        print("YENİ HATA", h)
    sorun += len(yeni)
    gorsel = gorsel_hatalari()
    for h in gorsel:
        print("GÖRSEL HATA", h)
    sorun += len(gorsel)
    if KATALOG.exists():
        if json.loads(KATALOG.read_text(encoding="utf-8")) != katalog_uret():
            print("KATALOG.json dosyalarla uyuşmuyor: python dogrulayici/kontrol.py --katalog-yaz")
            sorun += 1
    else:
        print("KATALOG.json yok")
        sorun += 1
    print(f"paket {len(paketler())}, HATA {len(hatalar)} (bilinen {len(hatalar) - len(yeni)}, yeni {len(yeni)}), "
          f"düzelen bilinen {duzelen}, UYARI {uyari}")
    print(f"ilkokul görsel paket {len(ilkokul_paketleri())}, görsel HATA {len(gorsel)}")
    return 1 if sorun else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
