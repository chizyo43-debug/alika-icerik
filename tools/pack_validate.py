#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pack_validate.py — AliKa içerik paketi doğrulayıcısı (GOREV_ICERIK0 §1.5).

Kullanım:  python tools/pack_validate.py <yol.jsonl|yol.json>

Stdlib-only (bağımlılık kuralı: yalnız pytest geliştirme bağımlılığıdır, o da
burada kullanılmaz). 39 kural uygular; bulgular HATA / UYARI / RAPOR olarak
listelenir, en az bir HATA varsa çıkış kodu 1'dir.

Kural referansı: .claude/qoder/GOREV_ICERIK0.md §1.5 tablosu ve
.claude/skills/alika-icerik/SKILL.md. Şekil kataloğu: shared/figure_spec.json.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from fractions import Fraction
from pathlib import Path
from typing import NamedTuple


class Bulgu(NamedTuple):
    seviye: str  # "HATA" | "UYARI" | "RAPOR"
    kural: int
    satir: int  # 1-tabanlı satır no; paket geneli bulgularda 0
    mesaj: str


# ---------------------------------------------------------------- sabitler

# Kural 2/3: tek başına "şekil", "tablo" veya "aşağıdaki" sözcüğü görsel
# bağımlılığı kanıtlamaz ("şekil örüntüsü", "tablo oluştur", "aşağıdaki
# ölçülerden" gibi). Yalnız dışarıdaki bir görsele açıkça işaret eden dil
# kalıpları eşleşir.
FIGUR_ATIF_RE = {
    "tr": (
        re.compile(
            r"\b(?:yukarıdaki|aşağıdaki)\s+"
            r"(?:şekilde|grafikte|tabloda|görselde|diyagramda)\b",
            re.I,
        ),
        re.compile(
            r"\b(?:yukarıdaki|aşağıdaki|bu|verilen|gösterilen)\s+"
            r"(?:şekle|grafiğe|tabloya|görsele|diyagrama)\s+göre\b",
            re.I,
        ),
        re.compile(
            r"\b(?:şekli|grafiği|tabloyu|görseli|diyagramı)\s+"
            r"(?:incele(?:yin|yiniz)?|kullan(?:ın|ınız)?|yorumla(?:yın|yınız)?)\b",
            re.I,
        ),
    ),
    "ja": (
        re.compile(r"(?:上|下)の(?:図|グラフ|表)"),
        re.compile(r"(?:図|グラフ|表)(?:を見て|によると|に基づ)"),
    ),
    "ko": (
        re.compile(r"(?:위|아래)의?\s*(?:그림|그래프|표)"),
        re.compile(r"(?:그림|그래프|표)(?:을|를)?\s*(?:보고|참고|이용)"),
    ),
}

FIGUR_DOGRUDAN_TR_RE = re.compile(
    r"\b(?:şekildeki|grafikteki|tablodaki|görseldeki|diyagramdaki)\b",
    re.I,
)

ID_KARAKTER_RE = re.compile(r"^[A-Za-z0-9._-]+$")

# Paket boyunca dolaştığında gerçek çeldirici olmaktan çıkıp yalnız dolguya
# dönüşen, açıkça bozuk İngilizce biçimler. Yalnız bu yüksek güvenli küme uyarı
# üretir; alan terimlerinin sık görünmesi raporlanır ama otomatik kusur sayılmaz.
BARIZ_DIL_DOLGUSU = {
    "it are", "there am", "there be", "they is",
    "got has", "got have", "is got", "are go to",
}

# Kural 10: LaTeX izleri
LATEX_RE = re.compile(r"\$|\\frac|\\sqrt|\\begin")

# Kural 5-8: SVG beyaz listesi (shared/figure_spec.json ile birebir)
SVG_ETIKET = {"svg", "g", "circle", "ellipse", "rect", "line",
              "polyline", "polygon", "text", "tspan"}
SVG_TRANSFORM = {"translate", "rotate", "scale"}
RENK_TOKEN = {"ink", "muted", "accent", "gold", "success", "danger",
              "surface", "none"}
HEX_RENK_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")

# Kural 22: hazır kesir karakterleri
VULGAR = "½⅓⅔¼¾⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞"

USTSIMGE = "⁰¹²³⁴⁵⁶⁷⁸⁹"
UST2NORM = str.maketrans(USTSIMGE, "0123456789")

# Kural 15: sonuç soran kalıplar — yalnız bunlar varsa aritmetik değerlendirilir
SONUC_KALIP = ("sonucu", "sonuç", "kaçtır", "kaç olur", "eşittir", "değeri")

# Şekil kataloğu (shared/figure_spec.json ile birebir; doğrulayıcı kendi
# kopyasını taşır ki tek dosya halinde koşabilsin)
KATALOG = {
    "numberline": {"zorunlu": {"min", "max"},
                   "opsiyonel": {"step", "marks", "highlight"}},
    "fraction": {"zorunlu": {"style", "parts"}, "opsiyonel": {"filled"}},
    "shape": {"zorunlu": {"type"},
              "opsiyonel": {"dims", "sideLabels", "marks"}},
    "angle": {"zorunlu": {"degrees"}, "opsiyonel": {"rays", "labelKey"}},
    "grid": {"zorunlu": {"cols", "rows"}, "opsiyonel": {"shaded", "labels"}},
    "coordinate": {"zorunlu": {"xRange", "yRange"},
                   "opsiyonel": {"points", "segments", "labels"}},
    "chart": {"zorunlu": {"style", "categoryKeys", "values"},
              "opsiyonel": {"axisKeys"}},
    "table": {"zorunlu": {"headerKeys", "rows"}, "opsiyonel": {"highlight"}},
    "flow": {"zorunlu": {"nodes", "edges"}, "opsiyonel": {"direction"}},
    "circuit": {"zorunlu": {"elements"}, "opsiyonel": {"layout"}},
}
CIRCUIT_ELEM = {"battery", "lamp", "switch", "resistor", "wire"}


# ---------------------------------------------------------------- yardımcılar

def _sayi_mi(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def normalize_metin(s: str) -> str:
    """Kural 13/14: boşluk/noktalama/büyük-küçük yok sayılarak normalize."""
    s = unicodedata.normalize("NFKC", s).casefold()
    return "".join(c for c in s if not unicodedata.category(c).startswith(("P", "Z", "C")))


def normalize_secim_metin(s: str) -> str:
    """Şık tekrarı için öğrencinin ekranda gördüğü yazımı aynen korur.

    Büyük/küçük harf, noktalama ve sözcükler arasındaki boşluk yazım
    sorularında ölçülen özellik olabilir. Bu nedenle yalnız dış boşluklar ve
    Unicode'un kanonik kodlama farkları yok sayılır.
    """
    return unicodedata.normalize("NFC", s).strip()


def cevap_metin_sizintisi(ipucu: str, cevap: str) -> bool:
    """Doğru şık metnini ipucunda bağımsız sözcük dizisi olarak ara.

    Noktalama ve büyük/küçük harf farkını yok sayar; ancak kısa İngilizce
    cevapların (``is``, ``in``, ``a`` gibi) başka bir sözcüğün içinde
    geçmesini cevap sızıntısı saymaz.
    """
    cevap_sozcukleri = re.findall(
        r"[^\W_]+",
        unicodedata.normalize("NFKC", str(cevap)).casefold(),
        flags=re.UNICODE,
    )
    ipucu_sozcukleri = re.findall(
        r"[^\W_]+",
        unicodedata.normalize("NFKC", str(ipucu)).casefold(),
        flags=re.UNICODE,
    )
    if not cevap_sozcukleri or len(cevap_sozcukleri) > len(ipucu_sozcukleri):
        return False
    uzunluk = len(cevap_sozcukleri)
    return any(
        ipucu_sozcukleri[i:i + uzunluk] == cevap_sozcukleri
        for i in range(len(ipucu_sozcukleri) - uzunluk + 1)
    )


def distraktor_gerekcesi_jenerik(w: object, secenek: object) -> bool:
    """Yanlış şık gerekçesinin yalnız boş/genel bir etiket olup olmadığını bulur."""
    metin = str(w or "").strip()
    sade = " ".join(unicodedata.normalize("NFKC", metin).casefold().split())
    if not sade:
        return True
    kalip = re.sub(r"[.!?;,:]+$", "", sade).strip()
    if re.fullmatch(
            r"(?:(?:bu|o)\s+)?(?:(?:şık|seçenek|cevap)\s+)?"
            r"(?:yanlış(?:tır)?|doğru\s+değil(?:dir)?|uygun\s+değil(?:dir)?|cevap\s+değil)",
            kalip):
        return True

    # Kısa bir gerekçe, şıkkın kendisini adlandırıp ayırt edici bir özellik
    # söylüyorsa izlenebilirdir ("3 tektir", "Bakır iletkendir" gibi).
    secenek_norm = normalize_metin(str(secenek or ""))
    metin_norm = normalize_metin(metin)
    if secenek_norm and secenek_norm in metin_norm:
        kalan = metin_norm.replace(secenek_norm, "", 1)
        return len(kalan) < 4
    return len(metin_norm) < 12


def distraktor_gerekcesi_sablon(w: object) -> bool:
    """Uzun görünmesine karşın öğrencinin hatasını adlandırmayan kalıpları bulur."""
    sade = " ".join(
        unicodedata.normalize("NFKC", str(w or "")).casefold().split()
    )
    genel_kaliplar = (
        "kişi, yer, zaman, eylem veya dil bilgisi ilişkilerinden en az birini karşılamaz",
        "kökün istediği kişi, yer, zaman, eylem veya dil bilgisi",
    )
    if any(kalip in sade for kalip in genel_kaliplar):
        return True
    return (
        "kökündeki" in sade
        and "ipuçları bu seçeneği desteklemez" in sade
        and "yanlıştır" in sade
    )


def zorluk_gerekcesi_sablon(w: object) -> bool:
    """Şema §4 ölçütleri yerine soru kökünü yapıştıran gerekçeleri bulur."""
    sade = " ".join(
        unicodedata.normalize("NFKC", str(w or "")).casefold().split()
    )
    yasak = (
        "yalnız tema sözcüğünü tanımak yeterli değildir",
        "kökten kopyalanan",
    )
    return any(kalip in sade for kalip in yasak)


def figur_atfi_var(metin: str, dil: str, tip: str = "question") -> bool:
    """Metnin paket dışındaki bir görsele açıkça bağlı olup olmadığını söyler."""
    if not isinstance(metin, str) or not metin.strip():
        return False
    kucuk = metin.casefold()
    # Tablo/listenin hücreleri soru metnine erişilebilir düz metin olarak
    # gömülmüşse figure eksik değildir.
    satirici_tablo = (
        "tablo" in kucuk
        and (
            "\n" in metin
            or "\t" in metin
            or re.search(r"\bI\.\s.+\bII\.\s", metin) is not None
            or re.search(r"\b1[-.)]\s*.+\b2[-.)]\s*", metin) is not None
        )
    )
    if satirici_tablo:
        return False
    # Paket dilinin yanlış yazılması eksik görseli saklamamalı. Önce bildirilen
    # dil, ardından diğer desteklenen diller taranır.
    diller = [dil] if dil in FIGUR_ATIF_RE else []
    diller.extend(d for d in FIGUR_ATIF_RE if d not in diller)
    desenler = tuple(desen for d in diller for desen in FIGUR_ATIF_RE[d])
    if any(desen.search(metin) for desen in desenler):
        return True
    # "Şekildeki..." soru kökünde cevap için dış görsel gerektiğini gösterir;
    # konu anlatımındaki "şekildeki ilişkiyi belirle" gibi genel yöntem
    # cümlelerinde ise tek başına yeterli kanıt değildir.
    return tip == "question" and FIGUR_DOGRUDAN_TR_RE.search(metin) is not None


def _id_parcalari(kimlik: str) -> list[str]:
    return [p.casefold() for p in re.split(r"[._-]+", kimlik) if p]


def id_semasi_gecerli(
        kid: object,
        tip: str,
        paket_id: object,
        coverage_note_ids: set[str],
) -> bool:
    """Eski ve yapılandırılmış kimlik ailelerini paket kapsamıyla doğrular.

    Eski ``<paketId>.q001/n001`` ailesi geriye dönük uyumludur. Yeni ailede
    ayraçlar değişebilir; ancak ülke, sınıf ve ders kapsamı paketle uyuşmalı,
    soru/not türü de kimlikten veya paket coverage ilişkisinden kanıtlanmalıdır.
    """
    if not isinstance(kid, str) or not isinstance(paket_id, str):
        return False
    if not ID_KARAKTER_RE.fullmatch(kid):
        return False

    eski = re.fullmatch(re.escape(paket_id) + r"\.(q|n)\d+", kid, re.I)
    if eski:
        return eski.group(1).casefold() == ("n" if tip == "note" else "q")

    paket_parca = _id_parcalari(paket_id)
    kayit_parca = _id_parcalari(kid)
    if len(paket_parca) < 3 or len(kayit_parca) < 3:
        return False
    if kayit_parca[:2] != paket_parca[:2]:
        return False

    paket_ders = paket_parca[2]
    kayit_ders = kayit_parca[2]
    if not (paket_ders.startswith(kayit_ders) or kayit_ders.startswith(paket_ders)):
        return False

    if tip == "question":
        return re.search(r"(?:^|[._-])q\d+$", kid, re.I) is not None
    if tip == "note":
        isaretli_not = (
            re.search(r"(?:^|[._-])note(?:[._-]?\d+)$", kid, re.I) is not None
            or re.search(r"(?:^|[._-])n\d+$", kid, re.I) is not None
        )
        return isaretli_not or kid in coverage_note_ids
    return False


def sayi_ayristir(metin: str):
    """Şık metnini Fraction'a çevirmeyi dener; olmazsa None (kural 13/15)."""
    if not isinstance(metin, str):
        return None
    s = metin.strip().replace("−", "-")
    # üslü biçim: 2⁵
    m = re.fullmatch(r"([+-]?\d+)([" + USTSIMGE + r"]+)", s)
    if m:
        return Fraction(int(m.group(1))) ** int(m.group(2).translate(UST2NORM))
    # tam sayılı kesir: 1 1/2
    m = re.fullmatch(r"([+-]?\d+) (\d+)/(\d+)", s)
    if m:
        tam, pay, payda = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if payda == 0:
            return None
        kesir = Fraction(pay, payda)
        return Fraction(tam) + (kesir if tam >= 0 else -kesir)
    # düz kesir: 3/8
    m = re.fullmatch(r"([+-]?\d+)/(\d+)", s)
    if m:
        if int(m.group(2)) == 0:
            return None
        return Fraction(int(m.group(1)), int(m.group(2)))
    # düz sayı (ondalık nokta veya virgül)
    if re.fullmatch(r"[+-]?\d+(?:[.,]\d+)?", s):
        return Fraction(s.replace(",", "."))
    return None


# --- kural 15: güvenli aritmetik değerlendirici (eval YOK) -----------------

_IFADE_RE = re.compile(r"[0-9" + USTSIMGE + r"+\-−×÷/().,\s]+")


def ifade_bul(metin: str):
    """Soru metnindeki en uzun saf aritmetik ifadeyi bulur; yoksa None."""
    if any(c in metin for c in "√π%"):
        return None  # kök/pi/yüzde bu değerlendiricinin kapsamı dışında
    aday = ""
    for m in _IFADE_RE.finditer(metin):
        p = m.group().strip(" .,\n\t")
        if len(p) > len(aday):
            aday = p
    if not re.search(r"[+\-−×÷]|\d[" + USTSIMGE + r"]", aday):
        return None
    if len(re.findall(r"\d+", aday)) < 2:
        return None
    return aday or None


def ifade_degerlendir(ifade: str):
    """Küçük özyinelemeli ayrıştırıcı; Fraction döner, çözemezse None."""
    s = ifade.replace("×", "*").replace("÷", "/").replace("−", "-")
    s = re.sub(r"([0-9)])([" + USTSIMGE + r"]+)",
               lambda m: m.group(1) + "**" + m.group(2).translate(UST2NORM), s)
    s = re.sub(r"(\d),(\d)", r"\1.\2", s)  # ondalık virgül
    tokenlar = re.findall(r"\d+\.\d+|\d+|\*\*|[+\-*/()]", s)
    if "".join(tokenlar) != re.sub(r"\s+", "", s):
        return None  # tanınmayan artık karakter → değerlendirme yapma
    poz = 0

    def bak():
        return tokenlar[poz] if poz < len(tokenlar) else None

    def al():
        nonlocal poz
        t = tokenlar[poz]
        poz += 1
        return t

    def atom():
        t = bak()
        if t == "(":
            al()
            v = toplam()
            if bak() != ")":
                raise ValueError("paren")
            al()
            return v
        if t is None or not re.fullmatch(r"\d+(\.\d+)?", t):
            raise ValueError("sayı bekleniyor")
        al()
        return Fraction(t)

    def carpan():
        neg = False
        while bak() == "-":
            al()
            neg = not neg
        v = atom()
        if bak() == "**":
            al()
            us = carpan()
            if us.denominator != 1:
                raise ValueError("kesirli üs")
            v = v ** us.numerator
        return -v if neg else v

    def carpim():
        v = carpan()
        while bak() in ("*", "/"):
            op = al()
            sag = carpan()
            if op == "/":
                if sag == 0:
                    raise ValueError("sıfıra bölme")
                v = v / sag
            else:
                v = v * sag
        return v

    def toplam():
        v = carpim()
        while bak() in ("+", "-"):
            op = al()
            sag = carpim()
            v = v + sag if op == "+" else v - sag
        return v

    try:
        sonuc = toplam()
    except (ValueError, ZeroDivisionError):
        return None
    if poz != len(tokenlar):
        return None
    return sonuc


# --- şekil kataloğu denetimi (kural 4) --------------------------------------

def figur_kontrol(fig: dict) -> list:
    """Şerit A figürünü katalog kısıtlarına göre denetler; hata listesi döner."""
    h = []
    kind = fig.get("kind")
    if kind not in KATALOG:
        return [f"bilinmeyen kind: {kind!r}"]
    spec = KATALOG[kind]
    izinli = spec["zorunlu"] | spec["opsiyonel"] | {"kind", "notToScale"}
    for alan in spec["zorunlu"]:
        if alan not in fig:
            h.append(f"{kind}: zorunlu alan eksik: {alan}")
    for alan in fig:
        if alan not in izinli:
            h.append(f"{kind}: katalogda olmayan alan: {alan}")
    if h:
        return h

    def _num(alan):
        return fig.get(alan) if _sayi_mi(fig.get(alan)) else None

    if kind == "numberline":
        mn, mx = _num("min"), _num("max")
        if mn is None or mx is None or not mn < mx:
            h.append("numberline: min < max sağlanmıyor")
        else:
            for alan in ("marks", "highlight"):
                for v in fig.get(alan, []) or []:
                    if not _sayi_mi(v) or not (mn <= v <= mx):
                        h.append(f"numberline: {alan} elemanı aralık dışı: {v!r}")
            step = fig.get("step")
            if step is not None and (not _sayi_mi(step) or step <= 0):
                h.append("numberline: step > 0 olmalı")
    elif kind == "fraction":
        if fig.get("style") not in ("bar", "pie", "grid"):
            h.append("fraction: style ∈ bar|pie|grid değil")
        p = fig.get("parts")
        if not isinstance(p, int) or not 2 <= p <= 24:
            h.append("fraction: 2 ≤ parts ≤ 24 değil")
        f = fig.get("filled")
        if f is not None and (not isinstance(f, int) or isinstance(p, int) and not 0 <= f <= p):
            h.append("fraction: 0 ≤ filled ≤ parts değil")
    elif kind == "shape":
        if fig.get("type") not in ("square", "rect", "triangle", "circle", "polygon"):
            h.append("shape: type beyaz liste dışı")
        dims = fig.get("dims", {})
        if not isinstance(dims, dict):
            h.append("shape: dims sözlük değil")
        else:
            for k, v in dims.items():
                if k not in ("w", "h", "r", "a", "b", "c"):
                    h.append(f"shape: dims alanı tanımsız: {k}")
                elif not _sayi_mi(v) or v <= 0:
                    h.append(f"shape: dims.{k} > 0 değil")
    elif kind == "angle":
        d = fig.get("degrees")
        if not _sayi_mi(d) or not 0 < d <= 360:
            h.append("angle: 0 < degrees ≤ 360 değil")
    elif kind == "grid":
        c, r = fig.get("cols"), fig.get("rows")
        if not isinstance(c, int) or not isinstance(r, int) or not (1 <= c <= 20 and 1 <= r <= 20):
            h.append("grid: 1 ≤ cols,rows ≤ 20 değil")
        else:
            for i in fig.get("shaded", []) or []:
                if not isinstance(i, int) or not 0 <= i < c * r:
                    h.append(f"grid: shaded indeksi cols*rows dışı: {i!r}")
    elif kind == "coordinate":
        for alan in ("xRange", "yRange"):
            rng = fig.get(alan)
            if (not isinstance(rng, list) or len(rng) != 2
                    or not all(_sayi_mi(v) for v in rng) or not rng[0] < rng[1]):
                h.append(f"coordinate: {alan} [min,max] ve min<max değil")
        for p in fig.get("points", []) or []:
            if not (isinstance(p, list) and len(p) == 2 and all(_sayi_mi(v) for v in p)):
                h.append(f"coordinate: point [x,y] değil: {p!r}")
    elif kind == "chart":
        stil = fig.get("style")
        if stil not in ("bar", "line", "pie"):
            h.append("chart: style ∈ bar|line|pie değil")
        cats, vals = fig.get("categoryKeys"), fig.get("values")
        if not isinstance(cats, list) or not isinstance(vals, list) or len(cats) != len(vals):
            h.append("chart: len(categoryKeys) == len(values) değil")
        elif not all(_sayi_mi(v) for v in vals):
            h.append("chart: values sayısal değil")
        if stil == "pie" and "axisKeys" in fig:
            h.append("chart: style=pie iken axisKeys yazılmaz")
    elif kind == "table":
        basliklar, satirlar = fig.get("headerKeys"), fig.get("rows")
        if not isinstance(basliklar, list) or not basliklar:
            h.append("table: headerKeys liste değil/boş")
        elif not isinstance(satirlar, list):
            h.append("table: rows liste değil")
        else:
            for i, satir in enumerate(satirlar):
                if not isinstance(satir, list) or len(satir) != len(basliklar):
                    h.append(f"table: satır {i} hücre sayısı headerKeys ile eşit değil")
                    continue
                for hucre in satir:
                    if not (isinstance(hucre, dict) and len(hucre) == 1
                            and next(iter(hucre)) in ("key", "v")):
                        h.append(f"table: hücre {{'key':…}} veya {{'v':…}} değil: {hucre!r}")
    elif kind == "flow":
        dugumler, kenarlar = fig.get("nodes"), fig.get("edges")
        idler = set()
        if not isinstance(dugumler, list):
            h.append("flow: nodes liste değil")
        else:
            for n in dugumler:
                if not (isinstance(n, dict) and set(n) == {"id", "labelKey"}):
                    h.append(f"flow: node {{'id','labelKey'}} değil: {n!r}")
                else:
                    idler.add(n["id"])
        if not isinstance(kenarlar, list):
            h.append("flow: edges liste değil")
        else:
            for e in kenarlar:
                if not (isinstance(e, dict) and {"from", "to"} <= set(e)
                        and set(e) <= {"from", "to", "labelKey"}):
                    h.append(f"flow: edge {{'from','to','labelKey'?}} değil: {e!r}")
                elif idler and (e["from"] not in idler or e["to"] not in idler):
                    h.append(f"flow: edge tanımsız node'a bağlanıyor: {e!r}")
    elif kind == "circuit":
        elemanlar = fig.get("elements")
        if not isinstance(elemanlar, list) or not elemanlar:
            h.append("circuit: elements liste değil/boş")
        else:
            for e in elemanlar:
                if e not in CIRCUIT_ELEM:
                    h.append(f"circuit: eleman beyaz liste dışı: {e!r}")
        if "layout" in fig and fig["layout"] not in ("series", "parallel"):
            h.append("circuit: layout ∈ series|parallel değil")
    return h


def figur_i18n_anahtarlari(fig) -> set:
    """Figürde geçen tüm i18n anahtarlarını toplar (kural 9/25)."""
    anahtarlar = set()

    def gez(v, ad=""):
        if isinstance(v, dict):
            for k, alt in v.items():
                if k == "key" and isinstance(alt, str):
                    anahtarlar.add(alt)
                elif k in ("labels", "sideLabels", "axisKeys") and isinstance(alt, dict):
                    for x in alt.values():
                        if isinstance(x, str):
                            anahtarlar.add(x)
                else:
                    gez(alt, k)
        elif isinstance(v, list):
            for x in v:
                gez(x, ad)
        elif isinstance(v, str) and (ad.endswith("Key") or ad.endswith("Keys")):
            anahtarlar.add(v)

    gez(fig)
    return anahtarlar


# --- SVG denetimi (kural 5-9) ------------------------------------------------

_ATTR_RE = re.compile(r"([\w:-]+)\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>/]+)")


def svg_kontrol(svg: str, labels: dict, ekle, kullanilan: set):
    """Şerit B SVG metnini beyaz listeye göre denetler.

    ekle(kural, mesaj) geri çağrısıyla bulgu üretir; data-i18n anahtarlarını
    kullanilan kümesine yazar.
    """
    if re.search(r"<!\s*(DOCTYPE|ENTITY)", svg, re.I):
        ekle(5, "SVG içinde <!DOCTYPE> / <!ENTITY>")
    if re.search(r"(xlink:)?href\s*=", svg, re.I):
        ekle(5, "SVG içinde href/xlink:href")
    for m in HEX_RENK_RE.finditer(svg):
        ekle(8, f"SVG'de hex renk: {m.group()}")

    yigin = []
    ilk_etiket = True
    for m in re.finditer(r"<[^>]*>", svg):
        tok = m.group()
        if tok.startswith("<!"):
            continue  # yukarıda raporlandı
        kapanis = tok.startswith("</")
        ad_m = re.match(r"</?\s*([A-Za-z][\w:-]*)", tok)
        if not ad_m:
            ekle(6, f"çözümlenemeyen etiket: {tok[:40]}")
            continue
        ad = ad_m.group(1)
        if ad not in SVG_ETIKET:
            ekle(5, f"beyaz liste dışı etiket: <{ad}>")
        if kapanis:
            if yigin and yigin[-1] == ad:
                yigin.pop()
            else:
                ekle(6, f"eşleşmeyen kapanış etiketi: </{ad}>")
            continue
        kendinden_kapali = tok.rstrip(">").rstrip().endswith("/")
        # öznitelikler
        govde = tok[len(ad_m.group(0)):].rstrip(">").rstrip("/")
        attrlar = {}
        for am in _ATTR_RE.finditer(govde):
            anahtar, deger = am.group(1), am.group(2)
            if deger.startswith('"'):
                ekle(6, f"<{ad}> özniteliği çift tırnaklı: {anahtar}")
                deger = deger.strip('"')
            elif deger.startswith("'"):
                deger = deger.strip("'")
            else:
                ekle(6, f"<{ad}> özniteliği tırnaksız: {anahtar}")
            attrlar[anahtar] = deger
        if ilk_etiket and ad == "svg":
            for anahtar in attrlar:
                if anahtar in ("style", "background"):
                    ekle(8, f"kök <svg> üzerinde {anahtar}")
                elif anahtar not in ("viewBox", "xmlns"):
                    ekle(5, f"kök <svg> üzerinde izinsiz öznitelik: {anahtar}")
        ilk_etiket = False
        if "style" in attrlar and ad != "svg":
            ekle(5, f"<{ad}> üzerinde style özniteliği")
        tr = attrlar.get("transform")
        if tr:
            for fn in re.findall(r"([A-Za-z]+)\s*\(", tr):
                if fn not in SVG_TRANSFORM:
                    ekle(5, f"izinsiz transform: {fn}")
        for renk_alani in ("fill", "stroke"):
            deger = attrlar.get(renk_alani)
            if deger and deger not in RENK_TOKEN and not deger.startswith("#"):
                ekle(5, f"<{ad}> {renk_alani}='{deger}' token değil")
        if ad == "text":
            if "data-i18n" not in attrlar or "text-anchor" not in attrlar:
                ekle(7, "<text> üzerinde data-i18n / text-anchor eksik")
        anahtar = attrlar.get("data-i18n")
        if anahtar:
            kullanilan.add(anahtar)
            if anahtar not in labels:
                ekle(9, f"data-i18n anahtarı labels'ta yok: {anahtar!r}")
        if not kendinden_kapali:
            yigin.append(ad)
    for ad in yigin:
        ekle(6, f"kapatılmamış etiket: <{ad}>")
    # düz metin düğümleri (kural 7): etiketler arasında boşluk dışı içerik
    for parca in re.split(r"<[^>]*>", svg):
        if parca.strip():
            ekle(7, f"etiket içinde düz metin: {parca.strip()[:40]!r}")


# --- metin toplayıcılar -------------------------------------------------------

def kayit_metinleri(k: dict) -> list:
    """Kural 10/22/23 taraması için kaydın insan-okur metin alanları."""
    m = []
    for alan in ("question", "explanation", "title", "body", "topic", "subject"):
        v = k.get(alan)
        if isinstance(v, str):
            m.append(v)
    for alan in ("choices", "hints", "distractorWhy"):
        v = k.get(alan)
        if isinstance(v, list):
            m.extend(x for x in v if isinstance(x, str))
    return m


def latin_cjk_sayimi(metin: str):
    latin = len(re.findall(r"[A-Za-z]", metin))
    cjk = len(re.findall(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]", metin))
    return latin, cjk


# ---------------------------------------------------------------- ana denetim

def validate_file(yol) -> list:
    """Dosyayı doğrular, Bulgu listesi döner (testler bunu import eder)."""
    yol = Path(yol)
    bulgular: list = []

    def ekle(seviye, kural, satir, mesaj):
        bulgular.append(Bulgu(seviye, kural, satir, mesaj))

    ham = yol.read_text(encoding="utf-8")
    kayitlar = []  # (satir_no, dict)
    if yol.suffix == ".json":
        try:
            veri = json.loads(ham)
        except json.JSONDecodeError as e:
            ekle("HATA", 1, 1, f"geçerli JSON değil: {e}")
            return bulgular
        for i, k in enumerate(veri if isinstance(veri, list) else [veri], 1):
            kayitlar.append((i, k))
    else:
        for i, satir in enumerate(ham.splitlines(), 1):
            if not satir.strip():
                continue
            try:
                k = json.loads(satir)
            except json.JSONDecodeError as e:
                ekle("HATA", 1, i, f"satır geçerli JSON değil: {e}")
                continue
            if not isinstance(k, dict):
                ekle("HATA", 1, i, "satır JSON nesnesi değil")
                continue
            kayitlar.append((i, k))

    paket = next((k for _, k in kayitlar if k.get("type") == "pack"), None)
    paket_id = paket.get("id") if paket else None
    labels = (paket or {}).get("labels") or {}
    dil = (paket or {}).get("lang", "")
    if paket is None:
        ekle("HATA", 11, 0, "paket satırı (type=pack) yok; id şeması doğrulanamaz")

    # ---- Şema V2 paket kuralları ----
    if paket:
        sv = paket.get("schemaVersion", "")
        if sv and sv != "2.0":
            ekle("HATA", 27, 0, f"desteklenmeyen schemaVersion: {sv!r}")
        src = paket.get("source", "")
        if sv == "2.0" and (not src or src == "unknown"):
            ekle("HATA", 28, 0, "source boş veya 'unknown'")
        prov = paket.get("provenance", "")
        if sv == "2.0" and prov:
            if prov.count(":") < 2:
                ekle("HATA", 29, 0, f"provenance format hatası: {prov!r}")

    notlar = {k.get("id"): k for _, k in kayitlar if k.get("type") == "note"}
    sorular = [(s, k) for s, k in kayitlar if k.get("type") == "question"]
    coverage = (paket or {}).get("coverage")
    coverage_note_ids: set[str] = set()
    if coverage is not None and not isinstance(coverage, dict):
        ekle("HATA", 16, 0, "coverage nesne/sözlük değil")
        coverage = {}
    elif coverage is None:
        coverage = {}
    for objective, kapsam in coverage.items():
        if not isinstance(kapsam, dict):
            ekle("HATA", 16, 0, f"coverage[{objective!r}] nesne değil")
            continue
        kapsam_notlari = kapsam.get("notes")
        if not isinstance(kapsam_notlari, list):
            ekle("HATA", 16, 0, f"coverage[{objective!r}].notes liste değil")
            continue
        for nid in kapsam_notlari:
            if not isinstance(nid, str):
                ekle("HATA", 16, 0,
                     f"coverage[{objective!r}].notes içinde metin olmayan id: {nid!r}")
                continue
            coverage_note_ids.add(nid)
            if nid not in notlar:
                ekle("HATA", 16, 0,
                     f"coverage[{objective!r}] bulunmayan nota bağlı: {nid!r}")

    idler: dict = {}
    norm_sorular: dict = {}
    kullanilan_anahtarlar: set = set()
    konu_sayac: dict = {}
    kazanim_sayac: dict = {}
    objektifsiz = 0
    kind_kume: set = set()
    secenek_kume_kayitlari: dict = {}
    secenek_gorunum: dict = {}
    secenek_dogru: dict = {}
    secenek_kumeleri: dict = {}
    ipucu_konum_sayaclari = [dict() for _ in range(5)]

    for satir_no, k in kayitlar:
        tip = k.get("type")
        if tip not in ("note", "question"):
            continue
        metinler = kayit_metinleri(k)
        birlesik = " ".join(metinler)

        # kural 10 — LaTeX
        m10 = LATEX_RE.search(birlesik)
        if m10:
            ekle("HATA", 10, satir_no, f"LaTeX izi: {m10.group()!r}")

        # kural 11 — id şeması ve teklik
        kid = k.get("id")
        if kid in idler:
            ekle("HATA", 11, satir_no, f"id tekrarı: {kid!r} (ilk: satır {idler[kid]})")
        else:
            idler[kid] = satir_no
        if paket_id is not None and not id_semasi_gecerli(
                kid, tip, paket_id, coverage_note_ids):
            beklenen = "not" if tip == "note" else "soru"
            ekle("HATA", 11, satir_no,
                 f"{beklenen} id'si paket ülke/sınıf/ders kapsamı veya türüyle "
                 f"uyuşmuyor: {kid!r}")

        # kural 2/3 — şekil atfı ↔ figure alanı
        fig = k.get("figure")
        ana_metin = k.get("question") if tip == "question" else (k.get("body") or "")
        atif_var = figur_atfi_var(ana_metin or "", dil, tip)
        if atif_var and not fig:
            ekle("HATA", 2, satir_no, "metin şekle atıf yapıyor ama figure boş")
        if fig and not atif_var:
            ekle("UYARI", 3, satir_no, "figure dolu ama metin ondan bahsetmiyor")

        # kural 4/5-9 — figür denetimi
        if isinstance(fig, dict):
            if "svg" in fig:
                svg_kontrol(fig.get("svg") or "", labels,
                            lambda kural, mesaj, s=satir_no: ekle("HATA", kural, s, mesaj),
                            kullanilan_anahtarlar)
            elif "kind" in fig:
                kind_kume.add(fig.get("kind"))
                for hata in figur_kontrol(fig):
                    ekle("HATA", 4, satir_no, hata)
                anahtarlar = figur_i18n_anahtarlari(fig)
                kullanilan_anahtarlar |= anahtarlar
                for a in sorted(anahtarlar):
                    if a not in labels:
                        ekle("HATA", 9, satir_no, f"figür anahtarı labels'ta yok: {a!r}")
            else:
                ekle("HATA", 4, satir_no, "figure ne 'kind' ne 'svg' içeriyor")
        elif fig is not None and fig != {}:
            ekle("HATA", 4, satir_no, f"figure nesne değil: {type(fig).__name__}")

        if tip == "note":
            continue

        # ---- yalnız sorular ----
        soru = k.get("question") or ""
        secenekler = k.get("choices") if isinstance(k.get("choices"), list) else []
        dogru = k.get("correct")

        # kural 12 — correct aralığı, şık sayısı, aynı metin
        if not 2 <= len(secenekler) <= 5:
            ekle("HATA", 12, satir_no, f"şık sayısı 2-5 dışında: {len(secenekler)}")
        if not isinstance(dogru, int) or not 0 <= dogru < max(len(secenekler), 1):
            ekle("HATA", 12, satir_no, f"correct aralık dışı: {dogru!r}")
            dogru = None
        gorulen = {}
        for i, c in enumerate(secenekler):
            # Noktalama sorularında noktalama işaretleri şıkkın ölçülen
            # parçasıdır; soru tekrarı için kullanılan noktalama-silen
            # normalizasyon burada kullanılamaz.
            n = normalize_secim_metin(str(c))
            if n in gorulen:
                ekle("HATA", 12, satir_no,
                     f"iki şık metni aynı: {gorulen[n]} ve {i} ({c!r})")
            else:
                gorulen[n] = i

        # Paket-geneli kapalı seçenek havuzu ölçümleri. Aynı seçenek kümesinin
        # birden çok soruda görünmesi tek başına hata değildir; aşağıdaki
        # sayaçlar yüksek tekrar ve sürekli yanlış dolgu birleşimini ayırır.
        secenek_normlari = tuple(
            sorted(
                " ".join(
                    unicodedata.normalize("NFKC", str(c)).casefold().split()
                )
                for c in secenekler
            )
        )
        secenek_kume_kayitlari.setdefault(secenek_normlari, []).append(satir_no)
        for c in secenekler:
            c_norm = " ".join(
                unicodedata.normalize("NFKC", str(c)).casefold().split()
            )
            secenek_gorunum[c_norm] = secenek_gorunum.get(c_norm, 0) + 1
            secenek_kumeleri.setdefault(c_norm, set()).add(secenek_normlari)
        if dogru is not None and dogru < len(secenekler):
            dogru_norm = " ".join(
                unicodedata.normalize(
                    "NFKC", str(secenekler[dogru])
                ).casefold().split()
            )
            secenek_dogru[dogru_norm] = secenek_dogru.get(dogru_norm, 0) + 1

        # kural 13 — iki şık aynı sayıya eşit
        degerler = [(i, sayi_ayristir(str(c))) for i, c in enumerate(secenekler)]
        for a in range(len(degerler)):
            for b in range(a + 1, len(degerler)):
                va, vb = degerler[a][1], degerler[b][1]
                if va is not None and vb is not None and va == vb \
                        and normalize_metin(str(secenekler[a])) != normalize_metin(str(secenekler[b])):
                    ekle("HATA", 13, satir_no,
                         f"şık {a} ({secenekler[a]!r}) ile şık {b} ({secenekler[b]!r}) aynı sayı")

        # kural 14 — normalize soru tekrarı
        n_soru = normalize_metin(soru)
        if n_soru:
            if n_soru in norm_sorular:
                ekle("HATA", 14, satir_no,
                     f"soru metni tekrar (ilk: satır {norm_sorular[n_soru]})")
            else:
                norm_sorular[n_soru] = satir_no

        # kural 15 — hesaplanabilir aritmetik
        if dogru is not None and dogru < len(secenekler) \
                and any(kal in soru.casefold() for kal in SONUC_KALIP):
            ifade = ifade_bul(soru)
            if ifade:
                hesap = ifade_degerlendir(ifade)
                secenek_deger = sayi_ayristir(str(secenekler[dogru]))
                if hesap is not None and secenek_deger is not None and hesap != secenek_deger:
                    ekle("HATA", 15, satir_no,
                         f"aritmetik tutmuyor: {ifade!r} = {hesap} ama doğru şık {secenekler[dogru]!r}")

        # kural 16 — noteId ↔ topic eşleşmesi
        nid = k.get("noteId")
        if nid:
            hedef = notlar.get(nid)
            if hedef is None:
                ekle("HATA", 16, satir_no, f"noteId bulunamadı: {nid!r}")
            else:
                objective = k.get("objective")
                kapsam = coverage.get(objective) if objective else None
                if isinstance(kapsam, dict) and isinstance(kapsam.get("notes"), list):
                    if nid not in kapsam["notes"]:
                        ekle("HATA", 16, satir_no,
                             f"noteId, {objective!r} coverage.notes içinde değil: {nid!r}")
                elif hedef.get("topic") != k.get("topic"):
                    ekle("HATA", 16, satir_no,
                         "noteId ilişkisini coverage doğrulamıyor ve topic uyuşmuyor: "
                         f"soru={k.get('topic')!r} not={hedef.get('topic')!r}")

        # kural 17 — hints 5 basamak, boşsuz
        ipuclari = k.get("hints") if isinstance(k.get("hints"), list) else []
        if len(ipuclari) != 5 or any(not str(x or "").strip() for x in ipuclari):
            ekle("HATA", 17, satir_no,
                 f"hints 5 dolu basamak değil (uzunluk {len(ipuclari)})")
        if len(ipuclari) == 5:
            for konum, ipucu in enumerate(ipuclari):
                ipucu_norm = " ".join(
                    unicodedata.normalize(
                        "NFKC", str(ipucu)
                    ).casefold().split()
                )
                sayac = ipucu_konum_sayaclari[konum]
                sayac[ipucu_norm] = sayac.get(ipucu_norm, 0) + 1

        # kural 18 — ilk dört ipucunda cevap sızıntısı
        if dogru is not None and dogru < len(secenekler):
            cevap = str(secenekler[dogru]).strip()
            n_cevap = normalize_metin(cevap)
            for i, ip in enumerate(ipuclari[:4]):
                ip_s = str(ip)
                sizinti = False
                if re.fullmatch(r"[+-]?[\d.,/ ]+", cevap):
                    if re.search(r"(?<![\d.,/])" + re.escape(cevap) + r"(?![\d.,/])", ip_s):
                        sizinti = True
                elif n_cevap and cevap_metin_sizintisi(ip_s, cevap):
                    sizinti = True
                if sizinti:
                    ekle("HATA", 18, satir_no,
                         f"ipucu {i + 1} doğru şık metnini içeriyor ({cevap!r})")

        # kural 19/20 — distractorWhy
        why = k.get("distractorWhy") if isinstance(k.get("distractorWhy"), list) else []
        if len(why) != len(secenekler):
            ekle("HATA", 19, satir_no,
                 f"distractorWhy uzunluğu şık sayısına eşit değil ({len(why)}≠{len(secenekler)})")
        elif dogru is not None:
            if "doğru" not in str(why[dogru]).casefold():
                ekle("HATA", 19, satir_no, "doğru indekste 'doğru' yazmıyor")
            jenerik = [
                i for i, w in enumerate(why)
                if i != dogru
                and distraktor_gerekcesi_jenerik(w, secenekler[i])
            ]
            if jenerik:
                ekle("UYARI", 20, satir_no,
                     f"distractorWhy boş veya yalnız jenerik hüküm içeriyor: şık {jenerik}")
            sablon = [
                i for i, w in enumerate(why)
                if i != dogru and distraktor_gerekcesi_sablon(w)
            ]
            if sablon:
                ekle(
                    "HATA", 36, satir_no,
                    "distractorWhy öğrencinin somut hatasını adlandırmayan "
                    f"uzun şablon içeriyor: şık {sablon}",
                )

        # kural 21 — açıklamada şık harfi
        if dogru is not None and isinstance(k.get("explanation"), str):
            harf = "ABCDE"[dogru]
            if re.search(r"(?i)(cevap|yanıt|şık|seçenek)\s*[:\-]?\s*" + harf + r"\b", k["explanation"]) \
                    or re.search(harf + r"\s+(şıkkı|seçeneği)", k["explanation"]):
                ekle("UYARI", 21, satir_no, f"explanation şık harfi veriyor ({harf})")

        # kural 24 — objective ↔ objectiveSource
        if k.get("objective") and not k.get("objectiveSource"):
            ekle("HATA", 24, satir_no, "objective dolu ama objectiveSource boş")

        # ---- Şema V2 soru kuralları ----
        sv = (paket or {}).get("schemaVersion", "")
        if sv == "2.0":
            obj_val = k.get("objective", "")
            if not obj_val or obj_val == "PENDING":
                ekle("UYARI", 30, satir_no, "objective boş veya PENDING")
            obj_src = k.get("objectiveSource", "")
            if not obj_src or obj_src == "PENDING":
                ekle("UYARI", 31, satir_no, "objectiveSource boş veya PENDING")
            elif not obj_src.startswith(("http://", "https://")):
                ekle("UYARI", 31, satir_no, f"objectiveSource geçerli URL değil: {obj_src[:40]}")
            dr = k.get("difficultyReason", "")
            if len(dr) < 20:
                ekle("HATA", 32, satir_no, f"difficultyReason çok kısa ({len(dr)} karakter)")
            elif zorluk_gerekcesi_sablon(dr):
                ekle(
                    "HATA", 37, satir_no,
                    "difficultyReason soru kökünü uzatan jenerik şablon; "
                    "adım, ön bilgi veya çeldirici yakınlığı somutlaştırılmalı",
                )
            rs = k.get("reviewStatus", "")
            if rs and rs not in ("pending", "reviewed", "ai-verified", "rejected"):
                ekle("HATA", 33, satir_no, f"reviewStatus geçersiz: {rs!r}")
            if rs == "reviewed":
                q_prov = k.get("provenance", "")
                if "human-reviewed" not in q_prov:
                    ekle("HATA", 34, satir_no, "reviewStatus=reviewed ama provenance'da human-reviewed yok")
            if rs == "ai-verified":
                q_prov = k.get("provenance", "")
                if not q_prov.startswith("ai-verified:"):
                    ekle("HATA", 34, satir_no, "reviewStatus=ai-verified ama provenance AI karar hash'i taşımıyor")

        # kural 26 sayaçları
        konu_sayac[k.get("topic")] = konu_sayac.get(k.get("topic"), 0) + 1
        if k.get("objective"):
            kazanim_sayac[k["objective"]] = kazanim_sayac.get(k["objective"], 0) + 1
        else:
            objektifsiz += 1

    # ---- paket geneli kurallar ----
    tum_metin = " ".join(m for _, k in kayitlar for m in kayit_metinleri(k))

    # kural 22 — karışık kesir yazımı
    if re.search(r"\d/\d", tum_metin) and any(c in tum_metin for c in VULGAR):
        ekle("UYARI", 22, 0, "pakette hem 1/2 hem ½ biçimi var")

    # kural 23 — dil ↔ alfabe
    if dil in ("ja", "ko"):
        latin, cjk = latin_cjk_sayimi(tum_metin)
        if latin > cjk:
            ekle("HATA", 23, 0,
                 f"paket dili {dil!r} ama metin ağırlıklı Latin ({latin} Latin / {cjk} CJK)")

    # kural 25 — kullanılmayan labels anahtarları
    for a in sorted(set(labels) - kullanilan_anahtarlar):
        ekle("UYARI", 25, 0, f"labels anahtarı hiç kullanılmamış: {a!r}")

    # kural 26 — kapsama raporu
    for konu, adet in sorted(konu_sayac.items(), key=lambda x: str(x[0])):
        ekle("RAPOR", 26, 0, f"konu {konu!r}: {adet} soru")
    for kod, adet in sorted(kazanim_sayac.items()):
        ekle("RAPOR", 26, 0, f"kazanım {kod!r}: {adet} soru")
    ekle("RAPOR", 26, 0, f"objective boş: {objektifsiz} soru")
    bagsiz = [nid for nid in notlar
              if not any(k.get("noteId") == nid for _, k in sorular)]
    if bagsiz:
        ekle("RAPOR", 26, 0, f"hiç sorusu olmayan not: {', '.join(map(str, bagsiz))}")
    ekle("RAPOR", 26, 0,
         f"kullanılan farklı kind: {len(kind_kume)} ({', '.join(sorted(map(str, kind_kume))) or '-'})")

    # kural 38 — ipucu merdiveninin son iki basamağı dolguya dönüşmemeli.
    if len(sorular) >= 20:
        for konum in (3, 4):
            sayac = ipucu_konum_sayaclari[konum]
            if not sayac:
                continue
            ipucu, adet = max(sayac.items(), key=lambda item: item[1])
            oran = adet / len(sorular)
            if oran >= 0.70:
                ekle(
                    "UYARI", 38, 0,
                    f"ipucu {konum + 1} tek kalıba yığılmış: "
                    f"{adet}/{len(sorular)} (%{oran * 100:.1f}); "
                    f"örnek={ipucu[:70]!r}",
                )

    # kural 39 — kapalı seçenek havuzu ve sürekli yanlış dolgu.
    tekrarli_kumeler = [
        (kume, satirlar)
        for kume, satirlar in secenek_kume_kayitlari.items()
        if kume and len(satirlar) > 1
    ]
    if tekrarli_kumeler:
        etkilenen = sum(len(satirlar) for _, satirlar in tekrarli_kumeler)
        en_yuksek = max(len(satirlar) for _, satirlar in tekrarli_kumeler)
        ekle(
            "RAPOR", 39, 0,
            f"aynı seçenek kümesi: {len(tekrarli_kumeler)} küme / "
            f"{etkilenen} soru; en yüksek tekrar={en_yuksek}",
        )

    dolgu = []
    for secenek, adet in secenek_gorunum.items():
        if (
            adet >= 4
            and secenek_dogru.get(secenek, 0) == 0
            and len(secenek_kumeleri.get(secenek, ())) >= 2
            and re.search(r"[^\W\d_]", secenek, flags=re.UNICODE)
        ):
            dolgu.append((secenek, adet))
    if dolgu:
        ornekler = ", ".join(
            f"{secenek!r}×{adet}"
            for secenek, adet in sorted(
                dolgu, key=lambda item: (-item[1], item[0])
            )[:8]
        )
        ekle(
            "RAPOR", 39, 0,
            "birden çok soru ailesinde dolaşan ve hiç doğru olmayan "
            f"seçenekler var: {ornekler}",
        )

    bariz_dolgu = [
        (secenek, adet)
        for secenek, adet in secenek_gorunum.items()
        if (
            adet >= 4
            and secenek_dogru.get(secenek, 0) == 0
            and secenek in BARIZ_DIL_DOLGUSU
        )
    ]
    if bariz_dolgu:
        ornekler = ", ".join(
            f"{secenek!r}×{adet}"
            for secenek, adet in sorted(
                bariz_dolgu, key=lambda item: (-item[1], item[0])
            )
        )
        ekle(
            "UYARI", 39, 0,
            "açıkça bozuk dil biçimleri sürekli yanlış dolgu olarak "
            f"tekrarlanıyor: {ornekler}",
        )

    # ---- Şema V2 paket-genel kurallar ----
    if len(sorular) >= 10:
        from collections import Counter as _C
        cevap_konum = _C(k.get("correct", 0) for _, k in sorular)
        toplam_q = len(sorular)
        for konum, adet in cevap_konum.items():
            pct = adet / toplam_q * 100
            if pct > 35:
                ekle("UYARI", 35, 0,
                     f"doğru cevap konumu {konum}: %{pct:.1f} (>{35}% eşiği)")

    return bulgular


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="AliKa içerik paketi doğrulayıcısı")
    ap.add_argument("paket", help="doğrulanacak .jsonl veya .json dosyası")
    args = ap.parse_args(argv)
    yol = Path(args.paket)
    if not yol.exists():
        print(f"HATA  dosya yok: {yol}")
        return 1
    bulgular = validate_file(yol)
    hata = uyari = 0
    for b in bulgular:
        yer = f"[satır {b.satir}]" if b.satir else "[paket]"
        print(f"{b.seviye:<5} {yer} kural {b.kural}: {b.mesaj}")
        if b.seviye == "HATA":
            hata += 1
        elif b.seviye == "UYARI":
            uyari += 1
    print(f"TOPLAM: {hata} HATA, {uyari} UYARI")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
