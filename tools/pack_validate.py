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
            r"(?:şekilde|grafikte|tabloda|görselde|diyagramda|şemada)\b",
            re.I,
        ),
        re.compile(
            r"\b(?:yukarıdaki|aşağıdaki|bu|verilen|gösterilen)\s+"
            r"(?:şekle|grafiğe|tabloya|görsele|diyagrama)\s+göre\b",
            re.I,
        ),
        # "şema" yalnız GÖSTERİLENE açıkça işaret eden kalıplarda sayılır.
        # "bu şemaya göre" güvenilir değildir: fen sorularında şema çoğu kez
        # senaryonun içindeki bir nesnedir ("öğrenci bir devre şeması çizer,
        # bu şemaya göre deney kurar") ve okura gösterilen bir figür değildir.
        re.compile(r"\b(?:yukarıdaki|aşağıdaki)\s+şemaya\s+göre\b", re.I),
        re.compile(
            r"\b(?:şekli|grafiği|tabloyu|görseli|diyagramı|şemayı)\s+"
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

# Kural 19/36: gerekçe ile şık arasındaki anlam bağı aranırken yok sayılan,
# her cümlede geçen sözcükler. Bunlar "gerekçe şıkkı anıyor" kanıtı sayılmaz.
DURAK_SOZCUK = {
    "seçenek", "seçeneği", "seçeneğinde", "şıkkı", "şıkta", "cevap", "cevabı",
    "yanlış", "yanlıştır", "doğru", "doğrudur", "değil", "değildir", "olduğu",
    "olduğundan", "için", "ancak", "fakat", "çünkü", "bunu", "bunun", "gibi",
    "daha", "göre", "yerine", "birlikte", "üzerinde", "arasında", "sorunun",
    "soruda", "sorusunda", "kökündeki", "metinde", "metnin", "ifade", "ifadesi",
    "option", "answer", "wrong", "correct", "because", "this", "that",
}

# Kural 18: ilk dört ipucu cevabı DUYURAMAZ. Doğru şıkkın metnini birebir
# içermese de "doğru cevap …dır" biçiminde parafrazla söylemek de sızıntıdır;
# öğrenci ipucu merdivenini tırmanmadan sonuca ulaşır.
# Not: yalın "doğrudur" ARANMAZ. Türkçede yön bildiren "gazdan sıvıya doğrudur"
# ile doğruluk bildiren "doğrudur" aynı yazılır; yalın biçimi aramak fen
# paketinde hâl değişimi sorularını yanlışlıkla yakalıyordu.
CEVAP_DUYURU_RE = re.compile(
    r"doğru\s+(?:cevap|seçenek|yanıt)|tam\s+çözüm|(?:cevap|yanıt)\s*[:=]",
    re.I,
)

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
    "circuit": {"zorunlu": {"elements"},
                "opsiyonel": {"layout", "labelKeys"}},
}
CIRCUIT_ELEM = {"battery", "lamp", "switch", "resistor", "wire"}

# Kural 42: görsel temsil olmadan öğretilemeyen kazanım alanları.
# MAT.5.3 geometri/çizim · MAT.5.4 alan-çevre · MAT.5.5 veri · MAT.5.6 olasılık
# FB.5.2 kuvvet-hareket · FB.5.3 canlı yapısı · FB.5.5 madde · FB.5.6 ışık/devre
FIGUR_ZORUNLU_KAZANIM_ONEKLERI = (
    "MAT.5.3", "MAT.5.4", "MAT.5.5",
    "FB.5.2", "FB.5.3", "FB.5.5", "FB.5.6",
)

# ---- Question Contract 2.2 ----
# 2.0 paketleri olduğu gibi çalışmaya devam eder: sürüm başına kural kümesi
# ayrılır ki tek dosyada iki sözleşme yan yana yaşayabilsin. 2.1 hiçbir zaman
# onaylanmadı (görsel pilotta tek taraflı açılmıştı) ve desteklenmez.
SEMA_22 = "2.2"
SEMA_DESTEKLENEN = frozenset({"2.0", SEMA_22})

# 2.2 hiyerarşisi: Sınıf → Ders → Ünite/Tema → Üst konu → Alt konu → Not → Soru.
# Halka atlanamaz; eksik halka, sorunun hangi kavramı ölçtüğünü kaybettirir.
HIYERARSI_ANAHTARLARI = ("unitKey", "topicKey", "subtopicKey", "noteKey")

# Anahtar makine kimliğidir: ASCII slug. Türkçe karakter ve büyük harf yasak —
# görünen metin labels sözlüğünden gelir, anahtardan değil.
ANAHTAR_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Kalıcı veriye bir iş turunun adını yazmak yasak: '.repaired' bir sonraki
# onarımda ne anlama geldiğini kaybeder ve yetim anahtar bırakır.
GECICI_ETIKET_RE = re.compile(r"\.(repaired|temp|fixed|new|old|v\d+)$")

# Her kind için geçerli ortak figür alanları (shared/figure_spec.json §common).
FIGUR_ORTAK_ZORUNLU = frozenset({"altTextKey"})
FIGUR_ORTAK_OPSIYONEL = frozenset({"captionKey"})

# Kural 41: yalnız SAYISAL bir şık geri dönüştürülemez.
# "7", "2/5", "0,45", "20 cm" bir kazanımda doğru cevap, başkasında çeldirici
# olabilir; bu kusur değildir. Çeldirici geri dönüşümünün zararı öğrencinin
# konuyu değil PAKETİ öğrenmesidir: bir sözcük ya da ifade pakette dolaşınca
# öğrenci "bu şık hep yanlış" diye ezberleyebilir. Çıplak bir sayıda
# ezberlenecek bir şey yoktur — doğruluğu tamamen sorunun kendisine bağlıdır.
# Matematikte ödünç çeldiricilerin %76'sı tam olarak budur.
# Bir ölçünün pakette dolgu olarak dolaşması ayrı bir kusurdur ve onu kural 39
# yakalar; bu istisna orayı gevşetmez.
SAYISAL_SIK_RE = re.compile(
    r"^[%\s]*[\d.,/\s]+\s*"
    r"(?:cm²|m²|cm|mm|km|m|tl|kg|gr|g|lt|l|derece|°|%|birim kare|birim|"
    r"saat|dakika|saniye)?\s*[.]?$",
    re.I,
)


def sik_sayisal_mi(metin: object) -> bool:
    """Şık yalnız bir sayı (isteğe bağlı birimle) mi?"""
    s = str(metin or "").strip()
    return bool(s) and bool(SAYISAL_SIK_RE.fullmatch(s)) and any(
        ch.isdigit() for ch in s)


# 2.2 konu anlatımının dokuz bölümü. Sıra öğretim sırasıdır: ne öğreneceğim →
# kavramlar → ön bilgiler → adım adım → örnekler → yanılgılar → öz kontrol →
# özet → görsel yönergesi.
NOT_BOLUMLERI = (
    "whatIWillLearn", "keyConcepts", "priorKnowledge", "steps",
    "workedExamples", "commonMistakes", "selfCheck", "summary", "figureNote",
)


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


def icerik_sozcukleri(metin: object) -> set:
    """Metnin ayırt edici sözcükleri: 3 harften uzun, durak sözcük olmayan."""
    sade = unicodedata.normalize("NFKC", str(metin or "")).casefold()
    return {
        s for s in re.findall(r"[^\W_]+", sade, flags=re.UNICODE)
        if len(s) > 3 and s not in DURAK_SOZCUK
    }


def gerekce_yabanci_sik_anlatiyor(w: object, secenek: object,
                                  soru_sozcukleri: set,
                                  havuz_sozcukleri: set) -> set:
    """Gerekçe, bu soruda bulunmayan bir şıkkın sözcüklerini anlatıyorsa döner.

    Şık metni değiştirilip gerekçesi güncellenmediğinde ortaya çıkan hatayı
    yakalar: şık ``şablon`` olurken gerekçe ``Açıölçer açı ölçer…`` kalmıştır.
    ``açıölçer`` pakette başka soruların şık sözlüğünde vardır ama bu sorunun
    ne kökünde ne şıklarında geçer — güçlü ve dar bir imzadır.

    Parafraz yapan meşru gerekçeleri elemek için üç koşul birlikte aranır:
    gerekçe kendi şıkkına hiç değinmiyor, şıkkın ayırt edici sözcüğü var
    (yani değinmediğini söyleyebiliyoruz) ve yabancı sözcük paketin şık
    sözlüğünden geliyor.
    """
    gerekce_sozcukler = icerik_sozcukleri(w)
    kendi = icerik_sozcukleri(secenek)
    if not gerekce_sozcukler or not kendi:
        return set()
    if kendi & gerekce_sozcukler:
        return set()  # kendi şıkkını anıyor
    return gerekce_sozcukler & havuz_sozcukleri - soru_sozcukleri


def iskelet_imzasi(metin: object, kok: object = "") -> str:
    """Tırnaklı alanları, sayıları ve kökten kopyalanan sözcükleri maskeler.

    Geriye kalan dizge gerekçenin "iskeleti"dir; aynı iskeletin pakette
    yığılması, uzunluğuna bakılmaksızın şablon üretimin işaretidir.
    """
    sade = unicodedata.normalize("NFKC", str(metin or "")).casefold()
    sade = re.sub(r"[“\"'«»][^“\"'«»]*[”\"'«»]", " <X> ", sade)
    sade = re.sub(r"\d+(?:[.,/]\d+)*", "#", sade)
    kok_sozcukler = icerik_sozcukleri(kok)
    if kok_sozcukler:
        sade = " ".join(
            "<K>" if s in kok_sozcukler else s
            for s in re.split(r"(\W+)", sade)
        )
    return " ".join(sade.split())


def sozlesmeyi_yukle(paket_yolu) -> dict:
    """pack_contract.json'u paketin bulunduğu depo kökünden arar.

    Bulunamazsa boş sözlük döner ve kural 46 sessizce atlanır; doğrulayıcı
    sözleşme dosyası olmayan tek başına bir paket için de çalışabilmelidir.
    """
    for dizin in [Path(paket_yolu).resolve()] + list(
            Path(paket_yolu).resolve().parents):
        aday = dizin / "pack_contract.json"
        if aday.is_file():
            try:
                return json.loads(aday.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                return {}
    return {}


def figur_zorunlu_kazanim(objective: object) -> bool:
    """Görsel temsil olmadan öğretilemeyen kazanım kodlarını tanır.

    Liste bilinçli olarak dardır: yalnız geometri/ölçme, veri-grafik ve fen'in
    yapı/devre/ışık öğrenme alanları. Genişletmek insan yargısı gerektirir.
    """
    kod = str(objective or "").upper()
    return kod.startswith(FIGUR_ZORUNLU_KAZANIM_ONEKLERI)


def figur_atfi_var(metin: str, dil: str, tip: str = "question",
                   satirici_kacis: bool = True) -> bool:
    """Metnin paket dışındaki bir görsele açıkça bağlı olup olmadığını söyler.

    ``satirici_kacis`` iki farklı sorunun aynı işlevle sorulmasını ayırır:

    * Kural 2 "figür eksik mi?" — satır içi tablo gömülüyse figür gerekmez,
      kaçış açıktır.
    * Kural 3 "dolu figür anılmış mı?" — burada kaçış KAPALI olmalıdır. Aksi
      hâlde gövdesinde tablo bulunan bir konu anlatımı, figürüne açıkça atıf
      yapsa bile "metin ondan bahsetmiyor" uyarısı alır; kaçış geçerli atfı
      bastırır ve yazarı atfı düzeltmek yerine silmeye iter.
    """
    if not isinstance(metin, str) or not metin.strip():
        return False
    kucuk = metin.casefold()
    # Tablo/listenin hücreleri soru metnine erişilebilir düz metin olarak
    # gömülmüşse figure eksik değildir.
    satirici_tablo = (
        satirici_kacis
        and "tablo" in kucuk
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
        cok_dersli: bool = False,
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

    if not cok_dersli:
        paket_ders = paket_parca[2]
        kayit_ders = kayit_parca[2]
        if not (
            paket_ders.startswith(kayit_ders)
            or kayit_ders.startswith(paket_ders)
        ):
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
    # Türkçe yazımda "." binlik ayracı, "," ondalık ayracıdır. Binlik noktaları
    # ÖNCE atılır: sonra atılırsa ondalık virgülden dönüşen nokta ("1,234" →
    # "1.234") üç basamaklı bir binlik grubuna benzer ve yanlışlıkla silinir.
    s = re.sub(r"(?<=\d)\.(?=\d{3}(?!\d))", "", s)
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

def figur_kontrol(fig: dict, sema: str = "2.0") -> list:
    """Şerit A figürünü katalog kısıtlarına göre denetler; hata listesi döner.

    ``altTextKey`` / ``captionKey`` her kind için geçerli ortak alanlardır ve
    kind başına tekrarlanmaz; tekrarlanan tanım birinde güncellenip diğerinde
    unutulur. 2.2'de alt metin ZORUNLUDUR: alt metni olmayan bir figür, ekran
    okuyucu kullanan çocuk için var olmayan figürdür.
    """
    h = []
    kind = fig.get("kind")
    if kind not in KATALOG:
        return [f"bilinmeyen kind: {kind!r}"]
    spec = KATALOG[kind]
    izinli = (spec["zorunlu"] | spec["opsiyonel"] | {"kind", "notToScale"}
              | FIGUR_ORTAK_ZORUNLU | FIGUR_ORTAK_OPSIYONEL)
    zorunlu = set(spec["zorunlu"])
    if sema == SEMA_22:
        zorunlu |= set(FIGUR_ORTAK_ZORUNLU)
    for alan in zorunlu:
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
        if "sides" in fig:
            kenar = fig.get("sides")
            if fig.get("type") != "polygon":
                h.append("shape: sides yalnız type='polygon' ile kullanılır")
            elif not isinstance(kenar, int) or not 3 <= kenar <= 12:
                h.append(f"shape: sides 3-12 aralığında tam sayı değil: {kenar!r}")
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
        etiketler = fig.get("labelKeys")
        if not isinstance(etiketler, dict):
            h.append("circuit: labelKeys sözlük olmalı")
        else:
            gereken = set(elemanlar or [])
            if fig.get("layout"):
                gereken.add(fig["layout"])
            eksik = gereken - set(etiketler)
            if eksik:
                h.append(f"circuit: labelKeys eksik: {sorted(eksik)}")
    return h


def figur_i18n_anahtarlari(fig) -> set:
    """Figürde geçen tüm i18n anahtarlarını toplar (kural 9/25)."""
    anahtarlar = set()

    def gez(v, ad=""):
        if isinstance(v, dict):
            for k, alt in v.items():
                if k == "key" and isinstance(alt, str):
                    anahtarlar.add(alt)
                elif k in ("labels", "sideLabels", "axisKeys", "labelKeys") and isinstance(alt, dict):
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

def kural_22(kayitlar, paket, labels, kullanilan, ekle, olcum) -> None:
    """Question Contract 2.2 kuralları (47-58).

    Şema (shared/question-2.2.schema.json) kayıt biçimini denetler; buradaki
    kurallar şemanın YAPAMADIĞI şeyleri ölçer: iki alanın birbiriyle
    tutarlılığı, paket geneli sayımlar ve bildirilen hedefle ölçülen değerin
    karşılaştırılması. Şemayı tekrarlamazlar.
    """
    sorular = [(s, k) for s, k in kayitlar if k.get("type") == "question"]
    notlar = {k.get("noteId") or k.get("id"): k
              for _, k in kayitlar if k.get("type") == "note"}
    politika = (paket or {}).get("contractPolicy") or {}
    beklenen_soru_sayisi = politika.get("questionCount")
    if beklenen_soru_sayisi is not None and len(sorular) != beklenen_soru_sayisi:
        ekle(
            "HATA",
            52,
            0,
            f"soru sayısı bildirileni tutmuyor: ölçülen {len(sorular)}, "
            f"bildirilen {beklenen_soru_sayisi}",
        )
    ders_hedefleri = politika.get("perSubjectQuestionCount")
    if isinstance(ders_hedefleri, dict):
        ders_sayaci: dict[str, int] = {}
        for _, soru in sorular:
            ders = str(soru.get("subject") or "")
            ders_sayaci[ders] = ders_sayaci.get(ders, 0) + 1
        if ders_sayaci != ders_hedefleri:
            ekle(
                "HATA",
                52,
                0,
                "ders soru dağılımı bildirileni tutmuyor: "
                f"ölçülen {ders_sayaci}, bildirilen {ders_hedefleri}",
            )

    # kural 58 — resmî kaynak zinciri dosyaya ve sayfaya kadar çözülmeli.
    # URL'nin çalışıyor görünmesi kanıt değildir: indirilen belgenin hash'i,
    # sayfa sayısı ve her kaydın o belgedeki sayfa çapası birlikte saklanır.
    kaynaklar = (paket or {}).get("sources")
    kaynak_haritasi: dict[str, dict] = {}
    if not isinstance(kaynaklar, list) or not kaynaklar:
        ekle("HATA", 58, 0, "2.2 paketinde sources listesi boş veya eksik")
    else:
        for item in kaynaklar:
            if not isinstance(item, dict):
                ekle("HATA", 58, 0, "sources girdisi nesne değil")
                continue
            source_id = item.get("sourceId")
            if not isinstance(source_id, str) or not source_id.strip():
                ekle("HATA", 58, 0, "sources girdisinde sourceId boş")
                continue
            if source_id in kaynak_haritasi:
                ekle("HATA", 58, 0, f"sourceId tekrar ediyor: {source_id!r}")
            kaynak_haritasi[source_id] = item
            url = item.get("downloadUrl")
            if (
                not isinstance(url, str)
                or not re.match(r"^https?://", url, flags=re.I)
                or not url.lower().split("?", 1)[0].endswith(
                    (".pdf", ".doc", ".docx")
                )
            ):
                ekle(
                    "HATA", 58, 0,
                    f"{source_id}: indirilebilir belge URL'si yok: {url!r}",
                )
            sha = item.get("sha256")
            if (
                not isinstance(sha, str)
                or re.fullmatch(r"[0-9a-fA-F]{64}", sha) is None
            ):
                ekle("HATA", 58, 0, f"{source_id}: sha256 eksik/bozuk")
            page_count = item.get("pageCount")
            if not isinstance(page_count, int) or page_count < 1:
                ekle("HATA", 58, 0, f"{source_id}: pageCount eksik/bozuk")

    evidence_re = re.compile(r"^(.+?)(?::pdf-page-|#p)(\d+)$", re.I)
    for satir_no, record in kayitlar:
        if record.get("type") not in {"note", "question"}:
            continue
        refs = record.get("sourceRefs")
        if not isinstance(refs, list) or not refs:
            ekle("HATA", 58, satir_no, "sourceRefs boş veya eksik")
            ref_ids: set[str] = set()
        else:
            ref_ids = {
                str(ref).split("#", 1)[0]
                for ref in refs
                if isinstance(ref, str)
            }
            eksik_refs = sorted(ref_ids - set(kaynak_haritasi))
            if eksik_refs:
                ekle(
                    "HATA", 58, satir_no,
                    f"sourceRefs pakette tanımlı değil: {eksik_refs}",
                )
        evidence = record.get("objectiveEvidenceId")
        match = evidence_re.fullmatch(str(evidence or ""))
        if not match:
            ekle(
                "HATA", 58, satir_no,
                f"objectiveEvidenceId sayfa çapası değil: {evidence!r}",
            )
            continue
        source_id, page_text = match.groups()
        source_item = kaynak_haritasi.get(source_id)
        if source_item is None:
            ekle(
                "HATA", 58, satir_no,
                f"objectiveEvidenceId kaynağı pakette yok: {source_id!r}",
            )
            continue
        if source_id not in ref_ids:
            ekle(
                "HATA", 58, satir_no,
                f"objectiveEvidenceId kaynağı sourceRefs içinde yok: {source_id!r}",
            )
        page = int(page_text)
        page_count = source_item.get("pageCount")
        if isinstance(page_count, int) and not 1 <= page <= page_count:
            ekle(
                "HATA", 58, satir_no,
                f"kanıt sayfası belge dışında: {page}/{page_count}",
            )
        if record.get("objectiveSource") != source_item.get("downloadUrl"):
            ekle(
                "HATA", 58, satir_no,
                "objectiveSource, objectiveEvidenceId belgesiyle uyuşmuyor",
            )

    # kural 56 — hints alanı bulunmamalı.
    # Boş dizi de ihlaldir: boş dizi "bu alan var, doldurulmayı bekliyor" der.
    for satir_no, k in kayitlar:
        if "hints" in k:
            ekle("HATA", 56, satir_no,
                 f"2.2'de hints alanı yoktur (tür={type(k['hints']).__name__})")

    # kural 47 — hiyerarşi halkaları. Sınıf → Ders → Ünite → Üst konu →
    # Alt konu → Not zincirinde atlanan halka, sorunun hangi kavramı ölçtüğünü
    # kaybettirir. unit/topic/subtopic ASCII slug, noteKey ise AliKa'nın
    # açtığı tam not kimliğidir.
    for satir_no, k in kayitlar:
        if k.get("type") not in ("question", "note"):
            continue
        for alan in HIYERARSI_ANAHTARLARI:
            deger = k.get(alan)
            if not deger:
                ekle("HATA", 47, satir_no, f"hiyerarşi halkası eksik: {alan}")
            elif alan == "noteKey" and not ID_KARAKTER_RE.fullmatch(str(deger)):
                ekle("HATA", 47, satir_no,
                     f"noteKey geçerli kayıt kimliği değil: {deger!r}")
            elif alan != "noteKey" and not ANAHTAR_RE.fullmatch(str(deger)):
                ekle("HATA", 47, satir_no,
                     f"{alan} kararlı slug değil: {deger!r} "
                     "(yalnız ASCII küçük harf, rakam, tek tire)")

    # kural 48 — noteKey uygulamanın açacağı notun kararlı kimliğidir.
    # AliKa 2.2'de ayrı bir slug değildir: notta id/noteId/noteKey, soruda ise
    # noteId/noteKey aynı değeri taşır. Aksi durumda uygulama yanlış ekranda
    # doğru notu bulamaz.
    for satir_no, k in kayitlar:
        if k.get("type") != "note":
            continue
        nid = k.get("noteId") or k.get("id")
        if k.get("id") != nid or k.get("noteKey") != nid:
            ekle("HATA", 48, satir_no,
                 "not id/noteId/noteKey değerleri aynı olmalı")
    for satir_no, k in sorular:
        nid = k.get("noteId")
        nkey = k.get("noteKey")
        hedef = notlar.get(nid)
        if hedef is None:
            ekle("HATA", 48, satir_no, f"noteId hiçbir nota karşılık gelmiyor: {nid!r}")
        elif nkey != nid:
            ekle("HATA", 48, satir_no,
                 f"soru noteKey ile noteId aynı değil: {nkey!r} != {nid!r}")
        elif hedef.get("noteKey") != nid:
            ekle("HATA", 48, satir_no,
                 f"bağlı notun noteKey değeri noteId ile aynı değil: {nid!r}")

    # kural 49 — soru ailesi ve aile tavanı.
    aileler: dict = {}
    for satir_no, k in sorular:
        fid = k.get("familyId")
        if not fid:
            ekle("HATA", 49, satir_no, "familyId yok")
        else:
            aileler.setdefault(str(fid), []).append(satir_no)
    tavan = politika.get("maxPerFamily")
    if tavan:
        for fid, satirlar in sorted(aileler.items()):
            if len(satirlar) > tavan:
                ekle("HATA", 49, satirlar[0],
                     f"aile tavanı aşıldı: {fid!r} {len(satirlar)} soru (tavan {tavan})")

    # kural 50 — en az N gerçek aile. Az aile, kökü isim/sayı değiştirerek
    # çoğaltmanın işaretidir.
    asgari_aile = politika.get("minFamilies")
    if asgari_aile and aileler and len(aileler) < asgari_aile:
        ekle("HATA", 50, 0,
             f"soru ailesi sayısı yetersiz: {len(aileler)} (asgari {asgari_aile})")
    if aileler:
        ekle("RAPOR", 50, 0,
             f"soru ailesi: {len(aileler)}, en kalabalık aile "
             f"{max(len(v) for v in aileler.values())} soru")

    # kural 51 — geçici etiket adı. '.repaired' kalıcı veriye bir iş turunun
    # adını yazmaktır ve bir sonraki onarımda anlamını kaybeder.
    for a in sorted(labels):
        if GECICI_ETIKET_RE.search(a):
            ekle("HATA", 51, 0, f"labels anahtarında geçici sonek: {a!r}")

    # kural 52 — bildirilen cevap dağılımı ile ölçülen dağılım.
    hedef_dagilim = politika.get("answerBalance")
    if hedef_dagilim and sorular:
        olculen = [0, 0, 0, 0]
        for _, k in sorular:
            d = k.get("correct")
            if isinstance(d, int) and 0 <= d < 4:
                olculen[d] += 1
        if olculen != list(hedef_dagilim):
            ekle("HATA", 52, 0,
                 f"doğru cevap dağılımı bildirileni tutmuyor: "
                 f"ölçülen {olculen}, bildirilen {list(hedef_dagilim)}")

    # kural 53 — asgari görselli soru sayısı ve her notta görsel.
    figurlu = sum(1 for _, k in sorular if k.get("figure"))
    asgari_figur = politika.get("minFiguredQuestions")
    if asgari_figur and figurlu < asgari_figur:
        ekle("HATA", 53, 0,
             f"görselli soru sayısı yetersiz: {figurlu} (asgari {asgari_figur})")
    if politika.get("everyNoteHasFigure"):
        for satir_no, k in kayitlar:
            if k.get("type") == "note" and not (k.get("figure") or k.get("svg")):
                ekle("HATA", 53, satir_no, "notta görsel yok")
    if sorular:
        ekle("RAPOR", 53, 0,
             f"görselli soru: {figurlu}/{len(sorular)} "
             f"(%{100 * figurlu / len(sorular):.1f})")

    # kural 54 — damga bütünlüğü.
    # Şema alanların varlığını denetler ama iki alanı KARŞILAŞTIRAMAZ: bayat
    # damga (içerik değişmiş, inceleme hash'i eski) ancak burada yakalanır.
    for satir_no, k in kayitlar:
        if k.get("type") not in ("question", "note"):
            continue
        durum = k.get("reviewStatus")
        if durum == "ai-verified":
            ich, inch = k.get("contentHash"), k.get("reviewedHash")
            if not inch or not ich:
                ekle("HATA", 54, satir_no,
                     "ai-verified ama contentHash/reviewedHash eksik")
            elif ich != inch:
                ekle("HATA", 54, satir_no,
                     "damga bayat: içerik hash'i inceleme hash'inden farklı")
            uretici = str(k.get("provenance") or "")
            inceleyen = str(k.get("reviewedBy") or "")
            if inceleyen and inceleyen in uretici:
                ekle("HATA", 54, satir_no,
                     f"üretici kendi çıktısını incelemiş: {inceleyen!r}")
        if k.get("humanReviewed") and durum != "human-verified":
            ekle("HATA", 54, satir_no,
                 "humanReviewed true ama reviewStatus human-verified değil")

    # kural 57 — konu anlatımının dokuz bölümü.
    # ``body`` uygulamanın doğrudan gösterebildiği UTF-8 metindir;
    # ``lessonSections`` ise üretim/denetim için yapılandırılmış kaynaktır.
    # İkisi bir arada tutulur: uygulama ham JSON göstermez, denetleyici de
    # pedagojik bölümleri kaybetmez.
    for satir_no, k in kayitlar:
        if k.get("type") != "note":
            continue
        govde = k.get("body")
        if not isinstance(govde, str) or not govde.strip():
            ekle("HATA", 57, satir_no,
                 "2.2'de body uygulamada gösterilecek dolu metin olmalı")
        bolumler = k.get("lessonSections")
        if not isinstance(bolumler, dict):
            ekle("HATA", 57, satir_no,
                 "2.2'de lessonSections dokuz bölümlü nesne olmalı")
            continue
        for bolum in NOT_BOLUMLERI:
            deger = bolumler.get(bolum)
            if not deger:
                ekle("HATA", 57, satir_no, f"konu anlatımı bölümü eksik: {bolum}")
        ornekler = bolumler.get("workedExamples")
        if isinstance(ornekler, list) and len(ornekler) < 2:
            ekle("HATA", 57, satir_no,
                 f"en az iki çözümlü örnek gerekir (var: {len(ornekler)})")
        oz = bolumler.get("selfCheck")
        if isinstance(oz, list) and len(oz) < 3:
            ekle("HATA", 57, satir_no,
                 f"öz kontrol listesi çok kısa (madde: {len(oz)})")

    # kural 55 — paket beyanı ve yayın kilidi.
    if paket is not None:
        if not paket.get("disclosure"):
            ekle("HATA", 55, 0, "paket beyanı (disclosure) yok")
        bekleyen = sum(
            1 for _, k in kayitlar
            if k.get("objectiveSource") == "PENDING"
            or "PENDING" in (k.get("sourceRefs") or [])
        )
        if bekleyen and not paket.get("publishBlocked"):
            ekle("HATA", 55, 0,
                 f"{bekleyen} kayıtta PENDING kaynak var ama publishBlocked açık değil")
        if bekleyen:
            ekle("RAPOR", 55, 0,
                 f"PENDING kaynaklı kayıt: {bekleyen} (paket yayına kapalı)")

    # 2.2 skoru: hints kalktığı için S1 (ipucu sızıntısı) ölçülemez. Yerine
    # aynı ağırlıkla gerekçe özgüllüğü ölçülür — sözleşmenin asıl derdi budur.
    if sorular:
        jenerik = 0
        toplam_gerekce = 0
        for _, k in sorular:
            why = k.get("distractorWhy") or []
            secenekler = k.get("choices") or []
            dogru = k.get("correct")
            if len(why) != len(secenekler):
                continue
            for i, w in enumerate(why):
                if i == dogru:
                    continue
                toplam_gerekce += 1
                if distraktor_gerekcesi_jenerik(w, secenekler[i]):
                    jenerik += 1
        olcum["S1_gerekce_ozgullugu"] = (
            1 - jenerik / toplam_gerekce if toplam_gerekce else 1.0
        )


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

def validate_file(yol, metrikler: dict | None = None) -> list:
    """Dosyayı doğrular, Bulgu listesi döner (testler bunu import eder).

    ``metrikler`` verilirse kalite skorunun alt ölçütleri bu sözlüğe yazılır;
    böylece skor, kuralların saydığı aynı sayaçlardan türetilir ve ikinci bir
    ölçüm koduyla ayrışamaz.
    """
    yol = Path(yol)
    bulgular: list = []
    olcum: dict = metrikler if metrikler is not None else {}

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
    sema = (paket or {}).get("schemaVersion", "") or "2.0"
    ikibucuk = sema == SEMA_22
    if paket is None:
        ekle("HATA", 11, 0, "paket satırı (type=pack) yok; id şeması doğrulanamaz")

    # ---- Şema V2 paket kuralları ----
    if paket:
        sv = paket.get("schemaVersion", "")
        if sv and sv not in SEMA_DESTEKLENEN:
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
    secenek_kume_aileleri: dict = {}
    secenek_gorunum: dict = {}
    secenek_dogru: dict = {}
    secenek_kumeleri: dict = {}
    secenek_gorunum_ders: dict[str, dict] = {}
    secenek_dogru_ders: dict[str, dict] = {}
    secenek_kumeleri_ders: dict[str, dict] = {}
    ipucu_konum_sayaclari = [dict() for _ in range(5)]
    dw_bag_toplam = [0, 0]             # kural 36: (ölçülen, kendi şıkkına bağlı)
    dw_iskeletleri: list = []          # kural 37 kardeşi: distractorWhy imzaları
    dr_iskeletleri: list = []          # kural 37: difficultyReason imzaları
    govde_imzalari: list = []          # kural 40: soru kalıbı imzaları
    # Kural 41: geri dönüşüm KAZANIM üzerinden ölçülür, konu üzerinden değil.
    # Aynı kazanım içinde cevap havuzunun paylaşılması kusur değil, ölçmenin
    # kendisidir: sıklık zarfları (always/often/never) ya da bir ünitenin giysi
    # sözcükleri kapalı bir kümedir ve her sorunun çeldiricisi zorunlu olarak
    # başka bir sorunun doğru cevabıdır. Ünite dışından sözcük koymak soruyu
    # kolaylaştırır. Asıl kusur, çeldiricinin BAŞKA bir kazanımdan ödünç
    # alınmasıdır; ölçülen budur.
    metin_kazanimlari: dict = {}       # kural 41: doğru cevap metni → kazanım kümesi
    kazanim_celdiricileri: list = []   # kural 41: (kazanım, çeldirici metni)
    kazanim_figur: dict = {}           # kural 42: kazanım → (figürlü, toplam)
    objective_kaynaklari: dict = {}    # kural 43: objectiveSource → kazanım kümesi
    ipucu5_gorunum: dict = {}          # RAPOR 44: son ipucu çeşitliliği

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
        cok_dersli = (
            ((paket or {}).get("contractPolicy") or {}).get("idScopeMode")
            == "multi-subject"
        )
        if paket_id is not None and not id_semasi_gecerli(
                kid, tip, paket_id, coverage_note_ids, cok_dersli):
            beklenen = "not" if tip == "note" else "soru"
            ekle("HATA", 11, satir_no,
                 f"{beklenen} id'si paket ülke/sınıf/ders kapsamı veya türüyle "
                 f"uyuşmuyor: {kid!r}")

        # kural 2/3 — şekil atfı ↔ figure alanı
        fig = k.get("figure")
        if tip == "question":
            ana_metin = k.get("question")
        else:
            # 2.2'de not gövdesi dokuz bölümlü bir nesnedir; figüre yapılan
            # atıf figureNote bölümünde durur. 2.0'da gövde düz metindir.
            govde = k.get("body") or ""
            ana_metin = ("\n".join(
                str(v) for v in govde.values() if isinstance(v, str))
                if isinstance(govde, dict) else govde)
        if figur_atfi_var(ana_metin or "", dil, tip) and not fig:
            ekle("HATA", 2, satir_no, "metin şekle atıf yapıyor ama figure boş")
        if fig and not figur_atfi_var(ana_metin or "", dil, tip,
                                      satirici_kacis=False):
            ekle("UYARI", 3, satir_no, "figure dolu ama metin ondan bahsetmiyor")

        # kural 4/5-9 — figür denetimi
        if isinstance(fig, dict):
            if "svg" in fig:
                svg_kontrol(fig.get("svg") or "", labels,
                            lambda kural, mesaj, s=satir_no: ekle("HATA", kural, s, mesaj),
                            kullanilan_anahtarlar)
            elif "kind" in fig:
                kind_kume.add(fig.get("kind"))
                for hata in figur_kontrol(fig, sema):
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
        secenek_kume_aileleri.setdefault(secenek_normlari, set()).add(
            k.get("familyId") or f"satir-{satir_no}"
        )
        for c in secenekler:
            c_norm = " ".join(
                unicodedata.normalize("NFKC", str(c)).casefold().split()
            )
            secenek_gorunum[c_norm] = secenek_gorunum.get(c_norm, 0) + 1
            secenek_kumeleri.setdefault(c_norm, set()).add(secenek_normlari)
            ders_adi = str(k.get("subject") or "")
            ders_gorunum = secenek_gorunum_ders.setdefault(ders_adi, {})
            ders_kumeleri = secenek_kumeleri_ders.setdefault(ders_adi, {})
            ders_gorunum[c_norm] = ders_gorunum.get(c_norm, 0) + 1
            ders_kumeleri.setdefault(c_norm, set()).add(secenek_normlari)
        if dogru is not None and dogru < len(secenekler):
            dogru_norm = " ".join(
                unicodedata.normalize(
                    "NFKC", str(secenekler[dogru])
                ).casefold().split()
            )
            secenek_dogru[dogru_norm] = secenek_dogru.get(dogru_norm, 0) + 1
            ders_adi = str(k.get("subject") or "")
            ders_dogru = secenek_dogru_ders.setdefault(ders_adi, {})
            ders_dogru[dogru_norm] = ders_dogru.get(dogru_norm, 0) + 1

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

        # kural 17 — hints 5 basamak, boşsuz (yalnız 2.0).
        # 2.2'de hints alanı yoktur; kural 56 varlığını HATA sayar. İki sürümün
        # kuralı birbirini iptal ettiği için ikisi de koşulsuz çalışamaz.
        ipuclari = k.get("hints") if isinstance(k.get("hints"), list) else []
        if not ikibucuk and (
                len(ipuclari) != 5
                or any(not str(x or "").strip() for x in ipuclari)):
            ekle("HATA", 17, satir_no,
                 f"hints 5 dolu basamak değil (uzunluk {len(ipuclari)})")
        if not ikibucuk and len(ipuclari) == 5:
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
                elif CEVAP_DUYURU_RE.search(ip_s):
                    # Parafrazla duyuru: şık metni birebir geçmese de ipucu
                    # "doğru cevap …dır" diyerek merdiveni atlatıyor.
                    ekle("HATA", 18, satir_no,
                         f"ipucu {i + 1} cevabı duyuruyor: {ip_s[:70]!r}")

        # kural 19/20 — distractorWhy
        why = k.get("distractorWhy") if isinstance(k.get("distractorWhy"), list) else []
        if len(why) != len(secenekler):
            ekle("HATA", 19, satir_no,
                 f"distractorWhy uzunluğu şık sayısına eşit değil ({len(why)}≠{len(secenekler)})")
        elif dogru is not None:
            dogru_gerekce = str(why[dogru]).strip()
            if "doğru" not in dogru_gerekce.casefold():
                ekle("HATA", 19, satir_no, "doğru indekste 'doğru' yazmıyor")
            elif ikibucuk and (
                    len(dogru_gerekce) < 8 or dogru_gerekce.casefold() in {
                        "doğru", "doğrudur", "doğru cevap"
                    }
            ):
                ekle("HATA", 19, satir_no,
                     "doğru seçenek gerekçesi yalnız sonuç etiketi; "
                     "somut çözüm doğrulaması gerekli")
            jenerik = [
                i for i, w in enumerate(why)
                if i != dogru
                and distraktor_gerekcesi_jenerik(w, secenekler[i])
            ]
            if jenerik:
                ekle("UYARI", 20, satir_no,
                     f"distractorWhy boş veya yalnız jenerik hüküm içeriyor: şık {jenerik}")
            # kural 36 — gerekçe kendi şıkkına bağlı olmalı.
            # (a) Gerekçe, anlattığı şıkkın hiçbir ayırt edici sözcüğünü
            #     anmıyorsa izlenebilir değildir.
            # (b) Gerekçe BAŞKA bir şıkkın tamamını anlatıyorsa şık metni
            #     değiştirilip gerekçe güncellenmemiş demektir — bu, öğrenciye
            #     doğrudan yanlış bilgi gösterir.
            # kural 36 sayacı — gerekçenin kendi şıkkıyla sözcük bağı.
            # Bu bir ihlal ölçütü DEĞİLDİR: okuduğunu anlama sorularında
            # gerekçe şıkkı parafraz eder ("… metinde belirtilmemiştir").
            # Yalnız paket profili olarak raporlanır; şık değiştirilip
            # gerekçenin güncellenmemesini yakalayan gerçek kapı
            # tools/check_paired_edit.py'dir (fark zamanı denetimi).
            for i, w in enumerate(why):
                if i == dogru or not icerik_sozcukleri(secenekler[i]):
                    continue
                dw_bag_toplam[0] += 1
                if icerik_sozcukleri(secenekler[i]) & icerik_sozcukleri(w):
                    dw_bag_toplam[1] += 1
            # Paket geneli iskelet yığılması için imza topla.
            for i, w in enumerate(why):
                if i != dogru:
                    dw_iskeletleri.append(iskelet_imzasi(w, soru))

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
            else:
                # kural 37 imzası: yığılma paket düzeyinde değerlendirilir.
                dr_iskeletleri.append((satir_no, iskelet_imzasi(dr, soru)))
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

        # kural 40/41/42/43/44 sayaçları
        govde_imzalari.append(iskelet_imzasi(soru))
        obj = k.get("objective")
        kazanim = obj if obj else k.get("topic")
        if dogru is not None and dogru < len(secenekler):
            metin_kazanimlari.setdefault(
                normalize_metin(str(secenekler[dogru])), set()).add(kazanim)
        for i, c in enumerate(secenekler):
            # Sayısal şık geri dönüşüm ölçümüne girmez: ezberlenecek bir
            # anlamı yoktur (bkz. SAYISAL_SIK_RE açıklaması).
            if i != dogru and not sik_sayisal_mi(c):
                kazanim_celdiricileri.append((kazanim, normalize_metin(str(c))))
        if obj:
            figurlu, toplam = kazanim_figur.get(obj, (0, 0))
            kazanim_figur[obj] = (figurlu + (1 if k.get("figure") else 0),
                                  toplam + 1)
            kaynak = k.get("objectiveSource")
            if kaynak:
                objective_kaynaklari.setdefault(kaynak, set()).add(obj)
        if len(ipuclari) == 5:
            son = " ".join(
                unicodedata.normalize("NFKC", str(ipuclari[4])).casefold().split()
            )
            ipucu5_gorunum[son] = ipucu5_gorunum.get(son, 0) + 1

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

    # ---- Question Contract 2.2 kuralları (47-56) ----
    if ikibucuk:
        kural_22(kayitlar, paket, labels, kullanilan_anahtarlar, ekle, olcum)

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

    cok_dersli_paket = (
        ((paket or {}).get("contractPolicy") or {}).get("idScopeMode")
        == "multi-subject"
    )
    dolgu = []
    dolgu_kapsamlari = (
        (
            (
                ders,
                secenek_gorunum_ders.get(ders, {}),
                secenek_dogru_ders.get(ders, {}),
                secenek_kumeleri_ders.get(ders, {}),
            )
            for ders in secenek_gorunum_ders
        )
        if cok_dersli_paket
        else (("", secenek_gorunum, secenek_dogru, secenek_kumeleri),)
    )
    for ders, gorunum, dogrular, kumeler in dolgu_kapsamlari:
        for secenek, adet in gorunum.items():
            if (
                adet >= 4
                and dogrular.get(secenek, 0) == 0
                and len(kumeler.get(secenek, ())) >= 2
                and re.search(r"[^\W\d_]", secenek, flags=re.UNICODE)
            ):
                etiket = f"{ders}: {secenek}" if ders else secenek
                dolgu.append((etiket, adet))
    if dolgu:
        ornekler = ", ".join(
            f"{secenek!r}×{adet}"
            for secenek, adet in sorted(
                dolgu, key=lambda item: (-item[1], item[0])
            )[:8]
        )
        # Dolgu çeldirici, kalıbı fark eden öğrencinin eleyebildiği seçenektir;
        # etkin şık sayısını düşürerek ölçmeyi zayıflatır. UYARI seviyesi:
        # birim/tarih gibi meşru tekrarlar olabildiği için HATA değil.
        ekle(
            "UYARI", 39, 0,
            f"{len(dolgu)} seçenek birden çok soru ailesinde dolaşıyor ve "
            f"hiçbirinde doğru değil: {ornekler}",
        )

    bariz_dolgu = []
    bariz_kapsamlari = (
        (
            (
                ders,
                secenek_gorunum_ders.get(ders, {}),
                secenek_dogru_ders.get(ders, {}),
            )
            for ders in secenek_gorunum_ders
        )
        if cok_dersli_paket
        else (("", secenek_gorunum, secenek_dogru),)
    )
    for ders, gorunum, dogrular in bariz_kapsamlari:
        for secenek, adet in gorunum.items():
            if (
                adet >= 4
                and dogrular.get(secenek, 0) == 0
                and secenek in BARIZ_DIL_DOLGUSU
            ):
                etiket = f"{ders}: {secenek}" if ders else secenek
                bariz_dolgu.append((etiket, adet))
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

    # kural 36 — gerekçe/şık sözcük bağı profili (yalnız rapor).
    if dw_bag_toplam[0]:
        ekle("RAPOR", 36, 0,
             f"kendi şıkkına sözcük bağı olan gerekçe: "
             f"{dw_bag_toplam[1]}/{dw_bag_toplam[0]}")

    # kural 37 — gerekçelerin iskelet yığılması.
    # Tırnaklı alan, sayı ve soru kökünden kopyalanan sözcükler maskelendikten
    # sonra kalan iskelet pakette yığılıyorsa gerekçe uzun olsa da şablondur.
    for alan, imzalar, esik in (
        ("difficultyReason", [imza for _, imza in dr_iskeletleri], 0.20),
        ("distractorWhy", dw_iskeletleri, 0.20),
    ):
        if len(imzalar) < 40:
            continue
        sayac: dict = {}
        for imza in imzalar:
            sayac[imza] = sayac.get(imza, 0) + 1
        imza, adet = max(sayac.items(), key=lambda item: item[1])
        oran = adet / len(imzalar)
        if oran > esik:
            ekle(
                "HATA", 37, 0,
                f"{alan} tek iskelete yığılmış: {adet}/{len(imzalar)} "
                f"(%{oran * 100:.1f} > %{esik * 100:.0f}); "
                f"iskelet={imza[:70]!r}",
            )
        ekle("RAPOR", 37, 0,
             f"{alan} benzersiz iskelet: {len(sayac)}/{len(imzalar)}")

    # kural 40 — soru kalıbı çeşitliliği.
    if len(govde_imzalari) >= 40:
        sayac = {}
        for imza in govde_imzalari:
            sayac[imza] = sayac.get(imza, 0) + 1
        benzersiz_oran = len(sayac) / len(govde_imzalari)
        imza, adet = max(sayac.items(), key=lambda item: item[1])
        # Dil paketlerinde "Boşluğu doğru tamamla" gibi meşru soru aileleri
        # tek kalıp altında toplanır; eşik bu yüzden gevşek tutulur. Asıl
        # ölçüt aşağıdaki genel çeşitlilik oranıdır.
        if adet / len(govde_imzalari) > 0.10:
            ekle("UYARI", 40, 0,
                 f"aynı soru kalıbı {adet}/{len(govde_imzalari)} kez "
                 f"(%{adet / len(govde_imzalari) * 100:.1f} > %10): {imza[:70]!r}")
        if benzersiz_oran < 0.60:
            ekle("UYARI", 40, 0,
                 f"soru kalıbı çeşitliliği düşük: {len(sayac)}/"
                 f"{len(govde_imzalari)} (%{benzersiz_oran * 100:.1f} < %60)")
        ekle("RAPOR", 40, 0,
             f"benzersiz soru kalıbı: {len(sayac)}/{len(govde_imzalari)}")

    # kural 41 — çeldirici geri dönüşümü: çeldirici, BAŞKA bir kazanıma ait
    # sorunun doğru cevabıysa o şık konu dışından ödünç alınmıştır ve dikkatli
    # öğrenci tarafından elenebilir. Aynı kazanım içindeki paylaşım sayılmaz.
    if kazanim_celdiricileri:
        geri_donen = sum(
            1 for kazanim, metin in kazanim_celdiricileri
            if metin and (metin_kazanimlari.get(metin, set()) - {kazanim})
        )
        oran = geri_donen / len(kazanim_celdiricileri)
        if oran > 0.15:
            ekle("UYARI", 41, 0,
                 f"çeldiricilerin %{oran * 100:.1f}'i BAŞKA bir kazanımdaki "
                 f"sorunun doğru cevabı ({geri_donen}/"
                 f"{len(kazanim_celdiricileri)}, eşik %15)")
        ekle("RAPOR", 41, 0,
             "kazanım dışından ödünç çeldirici: "
             f"{geri_donen}/{len(kazanim_celdiricileri)}")

    # kural 42 — şekil gerektiren kazanımlar.
    figur_gereken = [
        (obj, figurlu, toplam)
        for obj, (figurlu, toplam) in sorted(kazanim_figur.items())
        if figur_zorunlu_kazanim(obj) and toplam >= 5
    ]
    eksik_figur = [
        (obj, figurlu, toplam) for obj, figurlu, toplam in figur_gereken
        if figurlu / toplam < 0.30
    ]
    if eksik_figur:
        ornek = ", ".join(f"{obj} {f}/{t}" for obj, f, t in eksik_figur[:6])
        ekle("UYARI", 42, 0,
             f"görsel gerektiren {len(eksik_figur)}/{len(figur_gereken)} "
             f"kazanımda figure oranı %30 altında: {ornek}"
             + (" …" if len(eksik_figur) > 6 else ""))

    # kural 43 — objectiveSource belge çapası olmalı.
    # Bir dersin bütün kazanımlarının aynı program PDF'ine bağlanması normaldir;
    # sorun, kaynağın belge değil gezinilebilir bir açılış sayfası olmasıdır.
    for kaynak, kazanimlar in objective_kaynaklari.items():
        if len(kazanimlar) < 5:
            continue
        belge_mi = (
            kaynak.lower().endswith((".pdf", ".doc", ".docx"))
            or "#" in kaynak
        )
        if not belge_mi:
            ekle("UYARI", 43, 0,
                 f"{len(kazanimlar)} kazanım belge olmayan bir objectiveSource'a "
                 f"bağlı (program PDF'i veya sayfa çapası bekleniyor): {kaynak[:70]}")

    # kural 46 — dersler arası paket sözleşmesi.
    sozlesme = sozlesmeyi_yukle(yol)
    if sozlesme and paket:
        olcek = sozlesme.get("levelScale", {})
        alt, ust = olcek.get("min", 1), olcek.get("max", 5)
        bildirilen = paket.get("levelScale")
        if bildirilen is not None:
            if (not isinstance(bildirilen, list) or len(bildirilen) != 2
                    or not (alt <= bildirilen[0] <= bildirilen[1] <= ust)):
                ekle("HATA", 46, 0,
                     f"levelScale sözleşme aralığının ({alt}-{ust}) dışında "
                     f"veya biçimsiz: {bildirilen!r}")
            else:
                alt, ust = bildirilen
        kullanilan = sorted({
            k.get("level") for _, k in sorular if isinstance(k.get("level"), int)
        })
        disarida = [s for s in kullanilan if not alt <= s <= ust]
        if disarida:
            ekle("HATA", 46, 0,
                 f"level değerleri bildirilen ölçek dışında ({alt}-{ust}): "
                 f"{disarida}")

        izinli_mufredat = sozlesme.get("curriculum", {}).get("izinli", [])
        if izinli_mufredat and paket.get("curriculum") not in izinli_mufredat:
            ekle("HATA", 46, 0,
                 f"curriculum sözleşmede yok: {paket.get('curriculum')!r} "
                 f"(izinli: {izinli_mufredat})")

        alan = sozlesme.get("notKazanimAlani", {}).get("ad", "objectives")
        yanlis_alanli = [
            k.get("id") for _, k in kayitlar
            if k.get("type") == "note" and not k.get(alan)
            and any(k.get(a) for a in ("objective", "objectives"))
        ]
        if yanlis_alanli:
            ekle("HATA", 46, 0,
                 f"{len(yanlis_alanli)} not sözleşmedeki {alan!r} alanını "
                 f"kullanmıyor: {yanlis_alanli[:3]}")

    # kural 45 — kazanım yükü dengesi.
    # Bazı derslerde kazanımların kapsamı eşit değildir. Paket açıkça
    # objectiveBalanceMode=coverage diyorsa oranı keyfî biçimde eşitlemek
    # yerine her kazanımın not ve soru kapsamının doğru beyan edildiğini ölç.
    denge_modu = ((paket or {}).get("contractPolicy") or {}).get(
        "objectiveBalanceMode", "ratio")
    kapsam_dengeli = True
    if denge_modu == "coverage":
        for objective, adet in kazanim_sayac.items():
            kapsam = coverage.get(objective)
            if (
                not isinstance(kapsam, dict)
                or kapsam.get("questions") != adet
                or not kapsam.get("notes")
            ):
                kapsam_dengeli = False
                ekle("HATA", 45, 0,
                     f"kazanım kapsam beyanı eksik/tutarsız: {objective!r}")
        eksik_kazanim = sorted(set(coverage) - set(kazanim_sayac))
        if eksik_kazanim:
            kapsam_dengeli = False
            ekle("HATA", 45, 0,
                 f"sorusu olmayan coverage kazanımı: {eksik_kazanim}")
        ekle("RAPOR", 45, 0,
             f"kazanım dengesi kapsam modunda; {len(kazanim_sayac)} kazanımın "
             "not ve soru beyanı doğrulandı")
    elif denge_modu != "ratio":
        kapsam_dengeli = False
        ekle("HATA", 45, 0,
             f"objectiveBalanceMode tanınmıyor: {denge_modu!r}")

    if len(kazanim_sayac) >= 5:
        en_cok = max(kazanim_sayac.values())
        en_az = min(kazanim_sayac.values())
        if denge_modu == "ratio" and en_az and en_cok / en_az > 6:
            yuklu = max(kazanim_sayac.items(), key=lambda x: x[1])
            zayif = min(kazanim_sayac.items(), key=lambda x: x[1])
            ekle("UYARI", 45, 0,
                 f"kazanım yükü dengesiz: {yuklu[0]}={yuklu[1]} soru, "
                 f"{zayif[0]}={zayif[1]} soru (oran {en_cok / en_az:.1f} > 6)")
        ekle("RAPOR", 45, 0,
             f"kazanım başına soru: en az {en_az}, en çok {en_cok}, "
             f"kazanım sayısı {len(kazanim_sayac)}")

    # kural 44 — son ipucu çeşitliliği (RAPOR).
    # SKILL.md yalnız ilk dört ipucunun cevabı vermemesini şart koşar; 5. ipucu
    # tam çözüm verebilir. Burada yalnız çeşitlilik ölçülür, ihlal üretilmez.
    if ipucu5_gorunum:
        toplam5 = sum(ipucu5_gorunum.values())
        ekle("RAPOR", 44, 0,
             f"son ipucu benzersizliği: {len(ipucu5_gorunum)}/{toplam5}")

    # ---- kalite skoru alt ölçütleri ----
    # Hepsi yukarıdaki kuralların saydığı sayaçlardan türer; ayrı bir ölçüm
    # kodu yoktur ki skor ile kural birbirinden ayrışmasın.
    soru_sayisi = len(sorular)
    if soru_sayisi:
        sizintili = len({b.satir for b in bulgular if b.kural == 18})
        # Aynı soru ailesinde sınıflandırma seçeneklerinin tekrar kullanılması
        # ölçme kusuru değildir (ör. dar/dik/geniş/doğru açı). Kapalı havuz
        # yalnız aynı küme birden fazla bağımsız aileye yayıldığında oluşur.
        paylasilan = sum(
            len(satirlar)
            for kume, satirlar in secenek_kume_kayitlari.items()
            if len(secenek_kume_aileleri.get(kume, ())) > 1
        )
        secenek_ornegi = sum(secenek_gorunum.values()) or 1
        # Uyarı ile skor aynı kapsamı ölçer. Çok dersli derlemede ``dolgu``
        # yukarıda ders bazında hesaplanmıştır; farklı derslerdeki doğal ortak
        # ölçü/sözcükler skoru yapay biçimde düşürmemelidir.
        dolgu_ornegi = sum(adet for _, adet in dolgu)
        imza_sayaci: dict = {}
        for imza in govde_imzalari:
            imza_sayaci[imza] = imza_sayaci.get(imza, 0) + 1
        # Kural 42'nin kabul ölçütü her görsel-zorunlu kazanımda en az %30'dur.
        # Eski hesap ham görsel yüzdesini doğrudan puanlıyor ve %30'u geçen
        # doğru paketleri %30 puanda bırakıyordu. Kapsama puanı artık her
        # kazanımın %30 hedefini ne ölçüde karşıladığını ölçer ve hedefte doyar.
        figur_hedef_toplam = 0
        figur_hedef_karsilanan = 0
        for o, (f, t) in kazanim_figur.items():
            if not figur_zorunlu_kazanim(o):
                continue
            hedef = max(1, (3 * t + 9) // 10)
            figur_hedef_toplam += hedef
            figur_hedef_karsilanan += min(f, hedef)
        if denge_modu == "coverage":
            denge = 1.0 if kapsam_dengeli else 0.0
        elif len(kazanim_sayac) >= 2:
            _oran = max(kazanim_sayac.values()) / max(min(kazanim_sayac.values()), 1)
            denge = min(1.0, 6 / _oran) if _oran > 6 else 1.0
        else:
            denge = 1.0
        geri_donen = sum(
            1 for kazanim, metin in kazanim_celdiricileri
            if metin and (metin_kazanimlari.get(metin, set()) - {kazanim})
        )
        # Alan bütünlüğü sürüme bağlıdır: 2.0'da beş dolu ipucu zorunlu alandır,
        # 2.2'de hints hiç yoktur ve yerine hiyerarşi zinciri zorunludur.
        def _alanlari_tam(k) -> bool:
            temel = (
                str(k.get("explanation") or "").strip()
                and str(k.get("difficultyReason") or "").strip()
                and str(k.get("objective") or "").strip()
            )
            if not temel:
                return False
            if ikibucuk:
                return all(k.get(a) for a in HIYERARSI_ANAHTARLARI) and bool(
                    k.get("familyId"))
            return isinstance(k.get("hints"), list) and len(k["hints"]) == 5

        tam_alan = sum(1 for _, k in sorular if _alanlari_tam(k))
        olcum.update({
            "soru": soru_sayisi,
            "S1_sizinti_yok": 1 - sizintili / soru_sayisi,
            "S2_havuz_acikligi": 1 - paylasilan / soru_sayisi,
            "S3_dolgu_yok": 1 - dolgu_ornegi / secenek_ornegi,
            "S4_kalip_cesitliligi": len(imza_sayaci) / soru_sayisi,
            "S5_sekil_kapsamasi": (
                figur_hedef_karsilanan / figur_hedef_toplam
                if figur_hedef_toplam else 1.0
            ),
            "S6_kazanim_dengesi": denge,
            "S7_geri_donusum_yok": (
                1 - geri_donen / len(kazanim_celdiricileri)
                if kazanim_celdiricileri else 1.0
            ),
            "S8_alan_butunlugu": tam_alan / soru_sayisi,
        })

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


# 2.2'de S1 yer değiştirir: ipucu kalktığı için "sızıntı yok" ölçütü her zaman
# 1.0 döner ve skoru sahte biçimde şişirirdi. Aynı ağırlık, sözleşmenin asıl
# derdi olan gerekçe özgüllüğüne verilir.
SKOR_AGIRLIK_22 = {"S1_gerekce_ozgullugu": "S1_sizinti_yok"}

SKOR_AGIRLIK = {
    "S1_sizinti_yok": 0.20,       # ilk dört ipucunda cevap sızıntısı (kural 18)
    "S2_havuz_acikligi": 0.15,    # tekrarlı seçenek kümesi (kural 39)
    "S3_dolgu_yok": 0.15,         # sürekli yanlış dolgu çeldirici (kural 39)
    "S4_kalip_cesitliligi": 0.15,  # soru kalıbı çeşitliliği (kural 40)
    "S5_sekil_kapsamasi": 0.10,   # görsel gerektiren kazanımlar (kural 42)
    "S6_kazanim_dengesi": 0.10,   # kazanım yükü dengesi (kural 45)
    "S7_geri_donusum_yok": 0.10,  # çeldirici geri dönüşümü (kural 41)
    "S8_alan_butunlugu": 0.05,    # zorunlu alanların doluluğu
}
SKOR_ESIK = 99.0

# Kural eşiklerini geçen ham ölçüler tam puan alır. Aksi yaklaşım, örneğin
# kural 40'ın açıkça kabul ettiği %60 kalıp çeşitliliğini yalnız 60 puan sayıp
# 0 HATA / 0 UYARI paketini yayın eşiğinin altında bırakıyordu. Ham değerler
# raporda ayrıca korunur; böylece iyileştirme alanları görünmez olmaz.
SKOR_KABUL_TABANI = {
    "S4_kalip_cesitliligi": 0.60,
    "S7_geri_donusum_yok": 0.85,
}


def skor_uygunluk_degeri(ad: str, ham: float) -> float:
    taban = SKOR_KABUL_TABANI.get(ad)
    if taban:
        return min(1.0, ham / taban)
    return ham


def paket_skoru(yol) -> dict:
    """Bir paketin alt ölçütlerini, skorunu ve bulgu sayımını döner."""
    olcum: dict = {}
    bulgular = validate_file(yol, metrikler=olcum)
    hata = sum(1 for b in bulgular if b.seviye == "HATA")
    uyari = sum(1 for b in bulgular if b.seviye == "UYARI")
    # 2.2 paketinde S1 yerine gerekçe özgüllüğü konur; ağırlık aynı kalır.
    for yeni_ad, eski_ad in SKOR_AGIRLIK_22.items():
        if yeni_ad in olcum:
            olcum[eski_ad] = olcum[yeni_ad]
    ham_olcutler = {
        ad: max(0.0, min(1.0, olcum.get(ad, 0.0)))
        for ad in SKOR_AGIRLIK
    }
    uygunluk_olcutleri = {
        ad: skor_uygunluk_degeri(ad, ham)
        for ad, ham in ham_olcutler.items()
    }
    skor = 100.0 * sum(
        SKOR_AGIRLIK[ad] * uygunluk_olcutleri[ad]
        for ad in SKOR_AGIRLIK
    )
    return {
        "paket": str(yol).replace("\\", "/"),
        "soru": olcum.get("soru", 0),
        "hata": hata,
        "uyari": uyari,
        "skor": round(skor, 2),
        "olcutler": {
            ad: round(100.0 * uygunluk_olcutleri[ad], 1)
            for ad in SKOR_AGIRLIK
        },
        "hamOlcutler": {
            ad: round(100.0 * ham_olcutler[ad], 1)
            for ad in SKOR_AGIRLIK
        },
        "gecti": bool(skor >= SKOR_ESIK and hata == 0 and uyari == 0),
    }


def _skor_modu(hedefler: list, json_yolu: str | None) -> int:
    yollar: list = []
    for hedef in hedefler:
        p = Path(hedef)
        if p.is_dir():
            yollar.extend(sorted(p.rglob("*.jsonl")))
        elif p.exists():
            yollar.append(p)
        else:
            print(f"HATA  dosya yok: {p}")
            return 1
    if not yollar:
        print("HATA  doğrulanacak paket bulunamadı")
        return 1

    sonuclar = [paket_skoru(y) for y in yollar]
    olcut_adlari = list(SKOR_AGIRLIK)
    basliklar = [ad.split("_", 1)[0] for ad in olcut_adlari]
    print(f"{'paket':28s} {'soru':>5s} {'skor':>7s}  "
          + " ".join(f"{b:>5s}" for b in basliklar) + "  HATA UYARI")
    for s in sonuclar:
        ad = Path(s["paket"]).stem[:28]
        print(f"{ad:28s} {s['soru']:5d} {s['skor']:7.2f}  "
              + " ".join(f"{s['olcutler'][o]:5.1f}" for o in olcut_adlari)
              + f"  {s['hata']:4d} {s['uyari']:5d}")
    gecen = sum(1 for s in sonuclar if s["gecti"])
    print(f"TOPLAM: {gecen}/{len(sonuclar)} paket eşiği geçti "
          f"(skor ≥ {SKOR_ESIK:.0f}, 0 HATA, 0 UYARI)")

    if json_yolu:
        Path(json_yolu).parent.mkdir(parents=True, exist_ok=True)
        Path(json_yolu).write_text(
            json.dumps({"esik": SKOR_ESIK,
                        "agirliklar": SKOR_AGIRLIK,
                        "paketler": sonuclar},
                       ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"skor dosyası yazıldı: {json_yolu}")
    return 0 if gecen == len(sonuclar) else 1


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="AliKa içerik paketi doğrulayıcısı")
    ap.add_argument("paket", nargs="+",
                    help="doğrulanacak .jsonl/.json dosyası (--skor ile dizin)")
    ap.add_argument("--skor", action="store_true",
                    help="kalite skorunu hesapla ve tablo bas")
    ap.add_argument("--json", dest="json_yolu",
                    help="--skor ile: sonucu bu JSON dosyasına yaz")
    args = ap.parse_args(argv)
    if args.skor:
        return _skor_modu(args.paket, args.json_yolu)
    if len(args.paket) != 1:
        print("HATA  tek paket bekleniyor (çoklu kullanım için --skor)")
        return 1
    yol = Path(args.paket[0])
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
