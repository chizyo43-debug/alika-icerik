#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2.0 → 2.2 taşımasının derse bağlı olmayan yardımcıları.

Türkçe ve Matematik taşıyıcıları bu modülü paylaşır. Kopyalanmış bir yardımcı,
birinde düzeltilip diğerinde unutulan bir kural demektir; slug üretimi ve
seçenek döndürme gibi işlerde bu sessiz bir veri bozulmasına dönüşür.
"""
from __future__ import annotations

import re
import unicodedata

AILE_TAVANI = 8

TURKCE_HARF = {
    "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u",
    "â": "a", "î": "i", "û": "u", "Ç": "c", "Ğ": "g", "İ": "i",
    "I": "i", "Ö": "o", "Ş": "s", "Ü": "u",
}


def slug(metin: object, uzunluk: int = 48) -> str:
    """Türkçe metni kararlı ASCII slug'a çevirir.

    Python'un lower()'ı Türkçe için yanlıştır (I→ı, İ→i) ve NFKD ayrıştırması
    'ı' harfini boşa düşürür; harf eşlemesi bu yüzden elle yapılır. Kesme
    işareti ayraca DÖNÜŞMEZ, silinir: "Atatürk'ü" → "ataturku", yoksa anahtar
    "ataturk-u" olup sözcük ortadan bölünür.
    """
    s = re.sub(r"['’‘`]", "", str(metin or ""))
    s = "".join(TURKCE_HARF.get(ch, ch) for ch in s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    if len(s) > uzunluk:
        s = s[:uzunluk].rstrip("-")
    return s


def iskelet(metin: object) -> str:
    """Metnin sayı ve noktalamadan arındırılmış imzası.

    Aynı imzayı taşıyan difficultyReason'lar aynı beceriyi ölçer; soru ailesi
    bu imzadan kurulur. Aile, kökü isim/sayı değiştirerek çoğaltmanın kabı
    değil, neyin ölçüldüğünün görünür hâlidir.
    """
    s = unicodedata.normalize("NFKC", str(metin or "")).casefold()
    s = re.sub(r"\d+", "#", s)
    s = re.sub(r"[^\w\s#]", " ", s, flags=re.UNICODE)
    return " ".join(s.split())


def aile_ata(sorular: list, taban_alan: str = "noteId") -> dict:
    """Soru kimliği → familyId. Aile: aynı not + aynı ölçülen beceri."""
    kumeler: dict = {}
    for q in sorular:
        anahtar = (q.get(taban_alan), iskelet(q.get("difficultyReason")))
        kumeler.setdefault(anahtar, []).append(q["id"])
    atama: dict = {}
    sayaclar: dict = {}
    for (nid, _imza), kimlikler in sorted(
            kumeler.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
        temel = slug(nid, 34)
        # Tavanı aşan küme parçalara bölünür; tek bir aile 8'i geçemez.
        for bas in range(0, len(kimlikler), AILE_TAVANI):
            sayaclar[temel] = sayaclar.get(temel, 0) + 1
            fid = f"{temel}-f{sayaclar[temel]:02d}"
            for kimlik in kimlikler[bas:bas + AILE_TAVANI]:
                atama[kimlik] = fid
    return atama


def dondur(soru: dict, hedef: int) -> bool:
    """Doğru cevabı ``hedef`` konuma taşır; şık ve gerekçeyi BİRLİKTE döndürür.

    Ayrı döndürmek d133631'in hatasıdır: çocuk bir şıkkı seçer, ekranda başka
    bir şıkkın gerekçesi çıkar. Bu yüzden iki dizi tek işlemde kaydırılır ve
    sonuç ``assert`` ile denetlenir.
    """
    secenekler = soru.get("choices")
    gerekceler = soru.get("distractorWhy")
    dogru = soru.get("correct")
    if not isinstance(secenekler, list) or len(secenekler) != 4:
        return False
    if not isinstance(gerekceler, list) or len(gerekceler) != 4:
        return False
    if not isinstance(dogru, int) or dogru == hedef:
        return False

    kaydir = (hedef - dogru) % 4
    yeni_s = [secenekler[(i - kaydir) % 4] for i in range(4)]
    yeni_g = [gerekceler[(i - kaydir) % 4] for i in range(4)]

    assert yeni_s[hedef] == secenekler[dogru], "doğru şık kaymadı"
    assert yeni_g[hedef] == gerekceler[dogru], "doğru gerekçe kaymadı"
    assert sorted(yeni_s) == sorted(secenekler), "şık kümesi değişti"
    assert sorted(yeni_g) == sorted(gerekceler), "gerekçe kümesi değişti"
    for eski_sik, eski_ger in zip(secenekler, gerekceler):
        i = yeni_s.index(eski_sik)
        assert yeni_g[i] == eski_ger, "şık ile gerekçe ayrıştı"

    soru["choices"] = yeni_s
    soru["distractorWhy"] = yeni_g
    soru["correct"] = hedef
    return True


def dagilimi_esitle(sorular: list, hedef: list) -> list:
    """Doğru cevap dağılımını hedefe çeker; taşınan soruları döner.

    Seçim belirlenimcidir (kimliğe göre sıralı) ki aynı girdi hep aynı çıktıyı
    versin ve bir sonraki koşumda başka sorular oynamasın.
    """
    dagilim = [0, 0, 0, 0]
    for q in sorular:
        if isinstance(q.get("correct"), int) and 0 <= q["correct"] < 4:
            dagilim[q["correct"]] += 1

    fazla = [i for i in range(4) for _ in range(max(0, dagilim[i] - hedef[i]))]
    eksik = [i for i in range(4) for _ in range(max(0, hedef[i] - dagilim[i]))]
    if len(fazla) != len(eksik):
        raise ValueError(f"hedef toplamı tutmuyor: {dagilim} → {hedef}")

    tasinan = []
    sirali = sorted(sorular, key=lambda q: str(q.get("id")))
    for kaynak, varis in zip(fazla, eksik):
        for q in sirali:
            if q.get("correct") != kaynak or q.get("id") in tasinan:
                continue
            if dondur(q, varis):
                tasinan.append(q["id"])
                break
        else:
            raise ValueError(f"{kaynak} konumundan taşınacak soru bulunamadı")
    return tasinan


# ---- konu anlatımı ayrıştırıcısı ----

NOT_BASLIKLARI = [
    "Kavramlar",
    "Adım adım öğrenelim",
    "Çözümlü örnek 1",
    "Çözümlü örnek 2",
    "Sık yapılan hata",
    "Öz kontrol",
    "Görselle çalışma",
]


def bolumlere_ayir(govde: str) -> dict:
    """Düzyazı not gövdesini bilinen başlıklara göre parçalara ayırır."""
    parcalar: dict = {}
    su_an = None
    for satir in str(govde or "").splitlines():
        temiz = satir.strip()
        if not temiz:
            continue
        if temiz in NOT_BASLIKLARI:
            su_an = temiz
            parcalar[su_an] = []
            continue
        if su_an:
            parcalar[su_an].append(temiz)
    return {k: "\n".join(v).strip() for k, v in parcalar.items()}


def oz_kontrol_listele(metin: str) -> list:
    """Öz kontrol düzyazısını tek tek denetlenebilir maddelere böler.

    Metin kimi notta madde imli, kimi notta akan cümlelerdir; ikisi de tek bir
    cümle sonu kuralıyla ayrılabilir.
    """
    ham = re.sub(r"^\s*[-•]\s*", "", str(metin or ""), flags=re.M)
    maddeler = [p.strip() for p in re.split(r"(?<=[.!?])\s+", ham) if p.strip()]
    return [m for m in maddeler if len(m) >= 15]
