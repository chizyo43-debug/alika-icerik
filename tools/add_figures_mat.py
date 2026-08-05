# -*- coding: utf-8 -*-
"""A4 birinci parti — matematik geometri ailelerine Şerit A figürü ekler.

İlke: figür yalnız soru kökünde ZATEN yazılı olan ölçüyü görselleştirir.
Metinde bulunmayan bir bilgiyi (özellikle aranan değeri) figüre koymak
soruyu çözer; bu yüzden yalnız kökten okunabilen ölçüler kullanılır ve
aranan büyüklüğü açığa vuracak eşleşmeler atlanır.

Kapsam:
  angle  — 5-3-3 / 5-3-4: kökte geçen derece değeri
  grid   — 5-4-2: "# sütun ve # satır birim kare" ifadesi
  shape  — 5-4-1 / 5-4-3: "# cm ve # cm kenarlı" ya da "# cm × # cm"

Katalog kısıtları (shared/figure_spec.json ile birebir):
  angle: 0 < degrees <= 360
  grid : 1 <= cols, rows <= 20
  shape: dims degerleri > 0
Bu figürlerin hiçbiri labels sözlüğüne anahtar eklemez; etiket taşımazlar.
"""
import json
import re
import sys

YOL = (r"C:\Users\Shadow\AppData\Local\Temp\claude"
       r"\C--Users-Shadow-Desktop-ebeveyn-kontrol--claude-worktrees-chat-session-49102a"
       r"\eed40a9b-0979-4702-bf19-b8be4c2c09a5\scratchpad\repo"
       r"\turkiye\5-sinif\matematik\matematik-tum.jsonl")

DERECE = re.compile(r"(\d+)\s*°")
IZGARA = re.compile(r"(\d+)\s*sütun\s+ve\s+(\d+)\s*satır")
KENAR_VE = re.compile(r"[Kk]enarları\s+(\d+)\s*cm\s+ve\s+(\d+)\s*cm")
CARPIM_CM = re.compile(r"(\d+)\s*cm\s*×\s*(\d+)\s*cm")
CARPIM_BIRIM = re.compile(r"(\d+)\s*×\s*(\d+)\s*birim")


def figur_uret(q):
    """Sorunun kökünden okunabilen ölçüyle bir figür üretir; yoksa None."""
    qid = q["id"]
    kok = q["question"]

    if ".5-3-3." in qid or ".5-3-4." in qid:
        # Kökte tek bir derece geçiyorsa onu çiz. Birden çok derece varsa
        # hangisinin çizileceği belirsizdir ve eksik çizim yanıltır: atla.
        dereceler = [int(d) for d in DERECE.findall(kok)]
        dereceler = [d for d in dereceler if 0 < d <= 360]
        if len(dereceler) == 1:
            return {"kind": "angle", "degrees": dereceler[0]}
        return None

    if ".5-4-2." in qid:
        m = IZGARA.search(kok)
        if m:
            sutun, satir = int(m.group(1)), int(m.group(2))
            if 1 <= sutun <= 20 and 1 <= satir <= 20:
                return {"kind": "grid", "cols": sutun, "rows": satir}
        m = CARPIM_BIRIM.search(kok)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            # Iki dikdortgenin karsilastirildigi sorularda tek izgara
            # hangisinin cizildigini belirsiz birakir: atla.
            if len(CARPIM_BIRIM.findall(kok)) == 1 and 1 <= a <= 20 and 1 <= b <= 20:
                return {"kind": "grid", "cols": a, "rows": b}
        return None

    if ".5-4-1." in qid or ".5-4-3." in qid:
        m = KENAR_VE.search(kok) or CARPIM_CM.search(kok)
        if m and len(CARPIM_CM.findall(kok)) <= 1:
            a, b = int(m.group(1)), int(m.group(2))
            if a > 0 and b > 0:
                return {"kind": "shape", "type": "rect",
                        "dims": {"w": max(a, b), "h": min(a, b)}}
        return None

    return None


ATIF_ONEKI = "Verilen şekle göre, "


def _kucult_ilk(harf: str) -> str:
    """Türkçe küçültme: I → ı, İ → i. Python'un lower()'ı bunu yapmaz."""
    if harf == "I":
        return "ı"
    if harf == "İ":
        return "i"
    return harf.lower()


def atif_ekle(kok: str) -> str:
    """Soru köküne figüre açık atıf ekler (kural 3).

    Figür ile atıf AYNI işlemde üretilir: metnin hiç anmadığı bir figür
    süstür ve doğrulayıcı bunu kural 3 ile yakalar.
    """
    if not kok:
        return kok
    return ATIF_ONEKI + _kucult_ilk(kok[0]) + kok[1:]


def main():
    with open(YOL, encoding="utf-8") as f:
        satirlar = [json.loads(s) for s in f]

    eklenen = 0
    ozet = {}
    for r in satirlar:
        if r.get("type") != "question" or r.get("figure"):
            continue
        fig = figur_uret(r)
        if fig:
            r["figure"] = fig
            r["question"] = atif_ekle(r["question"])
            eklenen += 1
            aile = r["id"].rsplit(".", 1)[0]
            ozet[aile] = ozet.get(aile, 0) + 1

    for aile in sorted(ozet):
        print(f"  {aile}: {ozet[aile]} figür")
    print(f"TOPLAM eklenen figür: {eklenen}")

    if "--yaz" not in sys.argv:
        return
    with open(YOL, "w", encoding="utf-8", newline="\n") as f:
        for r in satirlar:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("yazildi")


if __name__ == "__main__":
    main()
