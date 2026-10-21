#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pack_validate.py — AliKa içerik paketi doğrulayıcısı (GOREV_ICERIK0 §1.5).

Kullanım:  python tools/pack_validate.py <yol.jsonl|yol.json>

Stdlib-only (bağımlılık kuralı: yalnız pytest geliştirme bağımlılığıdır, o da
burada kullanılmaz). Sürüm kapılı numaralı kuralları uygular; bulgular HATA /
UYARI / RAPOR olarak listelenir, en az bir HATA varsa çıkış kodu 1'dir.

Kural referansı: .claude/qoder/GOREV_ICERIK0.md §1.5 tablosu ve
.claude/skills/alika-icerik/SKILL.md. Şekil kataloğu: shared/figure_spec.json.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import re
import sys
import unicodedata
from fractions import Fraction
from pathlib import Path
from typing import NamedTuple


_FIGURE_CONTRACT_PATH = (
    Path(__file__).resolve().parents[1] / "windows" / "figure_contract.py"
)
_FIGURE_CONTRACT_SPEC = importlib.util.spec_from_file_location(
    "_alika_figure_contract", _FIGURE_CONTRACT_PATH,
)
if _FIGURE_CONTRACT_SPEC is None or _FIGURE_CONTRACT_SPEC.loader is None:
    raise ImportError("AliKa Figure doğrulama sözleşmesi yüklenemedi")
_FIGURE_CONTRACT = importlib.util.module_from_spec(_FIGURE_CONTRACT_SPEC)
_FIGURE_CONTRACT_SPEC.loader.exec_module(_FIGURE_CONTRACT)

_LGS_CORE_PATH = Path(__file__).resolve().parents[1] / "windows" / "lgs_exam_core.py"
_LGS_CORE_SPEC = importlib.util.spec_from_file_location("_alika_lgs_exam_core", _LGS_CORE_PATH)
if _LGS_CORE_SPEC is None or _LGS_CORE_SPEC.loader is None:
    raise ImportError("AliKa LGS deneme sözleşmesi yüklenemedi")
_LGS_CORE = importlib.util.module_from_spec(_LGS_CORE_SPEC)
_LGS_CORE_SPEC.loader.exec_module(_LGS_CORE)

KATALOG = _FIGURE_CONTRACT.KATALOG
CIRCUIT_ELEM = _FIGURE_CONTRACT.CIRCUIT_ELEM
DIAGRAM_STIL = _FIGURE_CONTRACT.DIAGRAM_STIL
DIAGRAM_RENK = _FIGURE_CONTRACT.DIAGRAM_RENK
MAP_TURLERI = _FIGURE_CONTRACT.MAP_TURLERI
MAP_NOKTA_SEMBOLLERI = _FIGURE_CONTRACT.MAP_NOKTA_SEMBOLLERI
MAP_ROTA_STILLERI = _FIGURE_CONTRACT.MAP_ROTA_STILLERI
FIGUR_GENEL_ZORUNLU = _FIGURE_CONTRACT.FIGUR_GENEL_ZORUNLU
FIGUR_GENEL_OPSIYONEL = _FIGURE_CONTRACT.FIGUR_GENEL_OPSIYONEL
_sayi_mi = _FIGURE_CONTRACT._sayi_mi
figur_kontrol = _FIGURE_CONTRACT.figur_kontrol


class Bulgu(NamedTuple):
    seviye: str  # "HATA" | "UYARI" | "RAPOR"
    kural: int
    satir: int  # 1-tabanlı satır no; paket geneli bulgularda 0
    mesaj: str


# ---------------------------------------------------------------- sabitler

DESTEKLENEN_DILLER = frozenset({"tr", "en", "de", "es", "fr", "ja", "ko", "pt", "ru"})

# Kural 2/3: tek başına "şekil", "tablo" veya "aşağıdaki" sözcüğü görsel
# bağımlılığı kanıtlamaz ("şekil örüntüsü", "tablo oluştur", "aşağıdaki
# ölçülerden" gibi). Yalnız dışarıdaki bir görsele açıkça işaret eden dil
# kalıpları eşleşir.
FIGUR_ATIF_RE = {
    "tr": (
        re.compile(
            r"\b(?:yukarıdaki|aşağıdaki)\s+"
            r"(?:şekilde|grafikte|tabloda|görselde|diyagramda|şemada|haritada|çizimde|zaman çizelgesinde)\b",
            re.I,
        ),
        re.compile(
            r"\b(?:(?:yukarıdaki|aşağıdaki|bu|verilen|gösterilen)\s+)?"
            r"(?:şekle|grafiğe|tabloya|görsele|diyagrama|şemaya|haritaya|çizime|zaman çizelgesine)\s+göre\b",
            re.I,
        ),
        re.compile(
            r"\b(?:şekli|grafiği|tabloyu|görseli|diyagramı|şemayı|haritayı|çizimi|zaman çizelgesini)\s+"
            r"(?:incele(?:yin|yiniz)?|kullan(?:ın|ınız)?|yorumla(?:yın|yınız)?|"
            r"karşılaştır(?:ın|ınız)?)\b",
            re.I,
        ),
    ),
    "ja": (
        re.compile(r"(?:上|下)の(?:図|グラフ|表|年表)"),
        re.compile(r"(?:図|グラフ|表|年表)(?:を見て|によると|に基づ)"),
    ),
    "ko": (
        re.compile(r"(?:위|아래)의?\s*(?:그림|그래프|표|연표|타임라인)"),
        re.compile(r"(?:그림|그래프|표|연표|타임라인)(?:을|를)?\s*(?:보고|참고|이용)"),
    ),
}

# Number-line method instructions are not external-figure references. These
# bounded patterns only flag questions asking for a value explicitly shown or
# marked on a supplied line.
SAYI_DOGRUSU_ATIF_RE = (
    re.compile(
        r"\bsayı\s+doğrusunda(?:ki)?\s+[A-ZÇĞİÖŞÜ]\s+noktasının\s+"
        r"(?:değeri|konumu|gösterdiği\s+sayı)\b"
        r"(?=[^?\n]{0,250}\b(?:kaçtır|nedir|hangisi|hangi)\b)", re.I),
    re.compile(
        r"\bsayı\s+doğrusunda(?:ki)?\b[^?\n]{0,300}?"
        r"\b(?:işaretli|gösterilen|verilen)\s+noktanın\s+"
        r"(?:değeri|konumu|gösterdiği\s+sayı)\b"
        r"(?=[^?\n]{0,250}\b(?:kaçtır|nedir|hangisi|hangi)\b)", re.I),
    re.compile(
        r"\b(?:which|what)\s+(?:value|number|point)\s+is\s+"
        r"(?:shown|marked|labelled|labeled)\s+on\s+the\s+number\s+line\b", re.I),
    re.compile(
        r"\bwelche\s+Zahl\s+ist\s+auf\s+dem\s+Zahlenstrahl\s+"
        r"(?:markiert|dargestellt)\b", re.I),
    re.compile(
        r"\bqué\s+(?:punto|número)\s+está\s+(?:marcado|señalado)\s+"
        r"en\s+la\s+recta\s+numérica\b", re.I),
    re.compile(
        r"\bquel\s+(?:point|nombre)\s+est\s+(?:placé|marqué|représenté)\s+"
        r"sur\s+la\s+droite\s+graduée\b", re.I),
    re.compile(r"数直線上の点[A-ZＡ-Ｚ]が表す数"),
    re.compile(r"数直線(?:上)?に示された点(?:[A-ZＡ-Ｚ])?が表す数"),
    re.compile(r"수직선에\s*표시된\s*수는\s*(?:얼마|무엇)"),
    re.compile(
        r"\bqual\s+(?:ponto|número)\s+está\s+(?:marcado|representado)\s+"
        r"na\s+reta\s+numérica\b", re.I),
    re.compile(
        r"\bкакое\s+число\s+(?:отмечено|изображено)\s+на\s+"
        r"(?:числовой|координатной)\s+прямой\b", re.I),
)

FIGUR_DOGRUDAN_TR_RE = re.compile(
    r"\b(?:şekildeki|grafikteki|tablodaki|görseldeki|diyagramdaki|şemadaki|"
    r"haritadaki|çizimdeki|zaman\s+çizelgesindeki)\b",
    re.I,
)

ID_KARAKTER_RE = re.compile(r"^[A-Za-z0-9._-]+$")

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

AI_REVIEW_SHA256 = re.compile(r"^[0-9a-f]{64}$")
# Damga inceleyen modeli adlandırmaz; reviewModel isteğe bağlıdır. Yazılırsa geçerli bir model kimliği
# olmalı ve provenance'taki reviewer-model ile aynı olmalıdır.
AI_REVIEW_MODEL_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{1,79}$")
AI_REVIEW_DECLARATION = "ai-generated-and-ai-reviewed-no-human-review"
GECICI_GORSEL_ANAHTARI_RE = re.compile(
    r"\.visual\.(?:repaired|fixed|new|temp|tmp)$",
    re.IGNORECASE,
)


# ---------------------------------------------------------------- yardımcılar

def normalize_metin(s: str) -> str:
    """Kural 13/14: boşluk/noktalama/büyük-küçük yok sayılarak normalize."""
    s = unicodedata.normalize("NFKC", s).casefold()
    return "".join(c for c in s if not unicodedata.category(c).startswith(("P", "Z", "C")))


def soru_tekrar_anahtari(k: dict) -> str:
    """Kural 14 anahtarı: öğrencinin gördüğü metnin tamamı ve şekli.

    AMI sunumunda ``question`` yalnız kök cümlesidir ("Buna göre aşağıdakilerden
    hangisi doğrudur?"); bağlam ``context``'te, öncüller ``premises``'te durur.
    Yalnız kökü karşılaştırmak farklı bağlamlı standart kökleri tekrar sayar.
    Anahtar: ``context`` + ``stemLead`` + ``premises.items`` + ``question`` +
    text/callout bloklarının metni; şekil (figure/figures) varsa kanonik JSON'u
    eklenir, farklı şekilli iki soru tekrar sayılmaz. Metin boşsa anahtar boş.
    """
    parcalar = [k.get("context"), k.get("stemLead")]
    oncul = k.get("premises")
    if isinstance(oncul, dict):
        oncul = oncul.get("items")
    parcalar += oncul if isinstance(oncul, list) else []
    parcalar.append(k.get("question"))
    for blok in k.get("blocks") or []:
        if isinstance(blok, dict) and blok.get("t") in ("text", "callout"):
            parcalar += [blok.get("title"), blok.get("v")]
    metin = normalize_metin(" ".join(p for p in parcalar if isinstance(p, str)))
    if not metin:
        return ""
    sekiller = [x for x in [k.get("figure")] + list(k.get("figures") or []) if x]
    if sekiller:
        metin += "\x00" + json.dumps(sekiller, ensure_ascii=False, sort_keys=True)
    return metin


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


GEREKCE_HUKUMLERI = frozenset((
    "doğru", "yanlış", "doğrudur", "yanlıştır", "doğru cevap", "doğru seçenek",
    "correct", "incorrect", "wrong", "right", "correct answer", "this is correct",
    "richtig", "falsch", "richtige antwort", "correcto", "incorrecto",
    "respuesta correcta", "réponse correcte", "正解", "不正解", "正しい",
    "正しいです", "間違い", "정답", "오답", "맞습니다", "correto", "incorreto",
    "resposta correta", "верно", "неверно", "правильно", "неправильно",
    "правильный ответ", "bu seçenek doğrudur", "bu cevap doğrudur",
    "bu şık doğrudur", "the answer is correct", "this answer is correct",
    "die antwort ist richtig", "la respuesta es correcta", "la réponse est correcte",
    "a resposta está correta", "これは正解です", "それは正解です",
    "この答えは正しいです", "정답입니다", "이 답은 맞습니다",
    "это правильный ответ", "этот ответ правильный",
))


def dogru_gerekcesi_jenerik(gerekce: str, secenek: object) -> bool:
    """True when a correct-choice rationale is only a verdict or repeats the choice."""
    sade = " ".join(unicodedata.normalize("NFKC", gerekce).casefold().split())
    sade = sade.rstrip(".!?;,:。！？」")
    if sade in GEREKCE_HUKUMLERI:
        return True
    _, cjk = latin_cjk_sayimi(gerekce)
    if cjk >= 4:
        return normalize_metin(gerekce) == normalize_metin(str(secenek))
    return distraktor_gerekcesi_jenerik(gerekce, secenek)


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
    if tip == "question" and any(desen.search(metin) for desen in SAYI_DOGRUSU_ATIF_RE):
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

_IFADE_RE = re.compile(r"[0-9" + USTSIMGE + r"+\-−×÷·⋅*/()\[\].,\s]+")
# İkili işlem: solunda işlenen (rakam, üs, kapanan parantez) olan + − × ÷ · ⋅ *.
# Baştaki ya da "(" sonrasındaki işaret ve kesir çizgisi "/" işlem sayılmaz.
_IKILI_ISLEM_RE = re.compile(r"[0-9" + USTSIMGE + r")\]]\s*[+\-−×÷·⋅*]")
# Bitişik a/b kesri (pay ondalık olabilir): × ÷ · işlemlerinden önce bağlanır.
_KESIR_RE = re.compile(r"(\d+(?:[.,]\d+)?)/(\d+)(?![" + USTSIMGE + r"])")


def ifade_bul(metin: str):
    """Soru metnindeki tek ve tam aritmetik ifadeyi bulur; yoksa None.

    Birden çok sayılı parça (ifade tanınmayan bir karakterle bölünmüş olabilir),
    denklem (=) ya da harfe/değişkene bitişik ifade değerlendirilmez.
    """
    if any(c in metin for c in "√π%="):
        return None  # kök/pi/yüzde/denklem bu değerlendiricinin kapsamı dışında
    parcalar = []
    for m in _IFADE_RE.finditer(metin):
        p = m.group().strip(" .,\n\t")
        if not re.search(r"\d", p):
            continue
        bas = m.start() + m.group().index(p)
        parcalar.append((p, bas, bas + len(p)))
    if len(parcalar) != 1:
        return None
    aday, bas, son = parcalar[0]
    if (bas > 0 and metin[bas - 1].isalpha()) or (son < len(metin) and metin[son].isalpha()):
        return None  # değişkene bitişik: 0,25x − 0,5
    if not (_IKILI_ISLEM_RE.search(aday) or re.search(r"\d[" + USTSIMGE + r"]", aday)):
        return None  # tek sayı (−1/2) işlem değildir
    if len(re.findall(r"\d+", aday)) < 2:
        return None
    return aday


def ifade_degerlendir(ifade: str):
    """Küçük özyinelemeli ayrıştırıcı; Fraction döner, çözemezse None."""
    s = ifade.replace("[", "(").replace("]", ")")
    s = _KESIR_RE.sub(r"(\1/\2)", s)
    s = s.replace("×", "*").replace("·", "*").replace("⋅", "*").replace("÷", "/").replace("−", "-")
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



def figur_i18n_anahtarlari(fig) -> set:
    """Figürde geçen tüm i18n anahtarlarını toplar (kural 9/25)."""
    anahtarlar = set()

    def gez(v, ad=""):
        if isinstance(v, dict):
            for k, alt in v.items():
                if k == "key" and isinstance(alt, str):
                    anahtarlar.add(alt)
                # 1.6 shape marks.angles / marks.exterior, angle angleKeys / lineKeys: {"sıra": anahtar}.
                elif k in ("labels", "sideLabels", "axisKeys", "labelKeys", "angles", "exterior",
                           "angleKeys", "lineKeys") and isinstance(alt, dict):
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


def ai_review_claim_errors(kayit: dict) -> list[str]:
    """Question 2.2 AI-only güven damgasını insan onayından ayır."""

    status = kayit.get("reviewStatus")
    if status not in {"pending", "ai-verified"}:
        return ["reviewStatus yalnız pending veya ai-verified olabilir"]
    if kayit.get("humanReviewed") not in (None, False):
        return ["AI içeriği humanReviewed:false kalmalıdır"]
    approval_fields = (
        "reviewMode",
        "reviewModel",
        "reviewedContentSha256",
        "reviewDecisionSha256",
        "reviewDeclaration",
    )
    if status == "pending":
        unexpected = [alan for alan in approval_fields if alan in kayit]
        return (
            ["pending üretici kaydında onay alanı bulunamaz: " + ", ".join(unexpected)]
            if unexpected else []
        )

    hatalar = []
    beklenen = {
        "humanReviewed": False,
        "reviewMode": "ai-only",
        "reviewDeclaration": AI_REVIEW_DECLARATION,
    }
    for alan, deger in beklenen.items():
        if kayit.get(alan) != deger:
            hatalar.append(f"ai-verified kayıtta {alan}={deger!r} zorunludur")
    model = kayit.get("reviewModel")
    if model is not None and (not isinstance(model, str) or not AI_REVIEW_MODEL_RE.fullmatch(model)):
        hatalar.append("ai-verified kayıtta reviewModel yazılmışsa geçerli bir model kimliği olmalıdır")
    for alan in ("reviewedContentSha256", "reviewDecisionSha256"):
        deger = kayit.get(alan)
        if not isinstance(deger, str) or not AI_REVIEW_SHA256.fullmatch(deger):
            hatalar.append(f"ai-verified kayıtta geçerli {alan} zorunludur")
    provenance = str(kayit.get("provenance") or "")
    if (
        not provenance.startswith("ai-verified:sha256:")
        or "review-mode=ai-only" not in provenance
        or (isinstance(model, str) and f"reviewer-model={model}" not in provenance)
    ):
        hatalar.append("ai-verified provenance AI-only karar hash'ini taşımıyor")
    return hatalar


# ---------------------------------------------------------------- ana denetim

def lgs_kontrol(paket, sorular, ekle) -> None:
    """Kural 37: ``assessment`` (lgs-deneme) başlığı ve soruların ``lgs`` blokları.

    Kurallar Windows ve Android'in okuduğu ``windows/lgs_exam_core.py``'den gelir:
    form ∈ forms, geçerli oturum, (form, oturum, sıra) tekliği, ``requires`` kod
    biçimi, ders başına ``fullForm`` sınırı ve 1–5 seviye.
    """
    assessment = (paket or {}).get("assessment")
    lgs_sorulari = [(s, k) for s, k in sorular if "lgs" in k]
    if assessment is None:
        for satir_no, _ in lgs_sorulari:
            ekle("HATA", 37, satir_no, "soruda lgs bloğu var ama paket assessment taşımıyor")
        return
    for mesaj in _LGS_CORE.assessment_errors(assessment):
        ekle("HATA", 37, 0, mesaj)
    if not isinstance(assessment, dict):
        return
    for satir_no, k in sorular:
        if "lgs" not in k:
            ekle("HATA", 37, satir_no, "deneme paketinde lgs bloğu olmayan soru")
            continue
        for mesaj in _LGS_CORE.lgs_errors(k["lgs"], assessment, k.get("level")):
            ekle("HATA", 37, satir_no, mesaj)
    satirlar = {str(k.get("id") or ""): s for s, k in lgs_sorulari}
    for kid, mesaj in _LGS_CORE.pack_errors(assessment, [k for _, k in lgs_sorulari]):
        ekle("HATA", 37, satirlar.get(kid, 0), mesaj)


# --- gösterim kuralları (G-, içerik isteği K9) --------------------------------
#
# MEB 5-8. sınıf yazım biçimi: binlik, yüzde, ondalık, çarpma/bölme işareti,
# saat, derece, tırnak, olumsuz kök vurgusu, öncül şık sırası ve AMI sözdizimi.
# Kural kimlikleri içerik tarafının doğrulayıcı kopyasıyla aynıdır; bulgunun
# ``kural`` alanı sayı değil "G-..." metnidir. Uygulamanın içe aktarma kapısı
# yalnız AMI sözdizimini reddeder; biçim kuralları burada kalır.

_AMI_PATH = Path(__file__).resolve().parents[1] / "windows" / "ami.py"
_AMI_SPEC = importlib.util.spec_from_file_location("_alika_ami", _AMI_PATH)
if _AMI_SPEC is None or _AMI_SPEC.loader is None:
    raise ImportError("AliKa AMI ayrıştırıcısı yüklenemedi")
_AMI = importlib.util.module_from_spec(_AMI_SPEC)
sys.modules.setdefault("_alika_ami", _AMI)
_AMI_SPEC.loader.exec_module(_AMI)

_SAAT_BAGLAMI_RE = re.compile(r"\bsaat|\bdakika|\bsa\.", re.IGNORECASE)
_ORAN_BAGLAMI_RE = re.compile(r"\boran", re.IGNORECASE)
#: G-EKSI-BOSLUKLU: "−" öncesindeki cebirsel terim (sayı/üs/AMI atomu, ")" ya da "|" ile biten;
#: 2x, x², AB gibi en çok iki harfli değişken). U+FFFC: _ami_parcala'nın atom yer tutucusu.
_CEBIR_TERIM_RE = re.compile(
    r".*[0-9⁰¹²³⁴-⁹)|\ufffc]|\d*[a-zA-Z]{1,2}[⁰¹²³⁴-⁹\ufffc]*")
_OLUMSUZ_KOK = ("değildir|değil|yanlıştır|söylenemez|olamaz|yoktur|olmayan|olmadığı|"
                "yapılamaz|ulaşılamaz|çıkarılamaz|kullanılamaz|gösterilemez|bulunmaz|"
                "değinilmemiştir")
_OLUMSUZ_RE = re.compile(rf"(?<!\w)(?:{_OLUMSUZ_KOK})(?!\w)")
_OLUMSUZ_BUYUK_RE = re.compile(
    r"(?<!\w)(?:" + _OLUMSUZ_KOK.replace("i", "İ").upper() + r")(?!\w)")
#: İçerik deposunun MEB denetimiyle aynı ek kalıpları ("kullanılmamıştır", "bilmeyen",
#: "çelişmeyen"). Yalnız soru kökünde (``question``'ın "?" ile biten son cümlesi) aranır:
#: eski paketlerde bağlam da ``question``'dadır ("nefesi yetmediği için ...") ve MEB
#: kuralı kökteki olumsuzluğu ister. Ekten önce en az 3 harf ("bil|meyen" eşleşir,
#: "namaz", "Ramazan" eşleşmez); sözcük ekleriyle bütün alınır ("bilmeyenler").
_OLUMSUZ_EK = "amaz|emez|mayan|meyen|madığı|mediği|mamıştır|memiştir"
_OLUMSUZ_EK_RE = re.compile(rf"(?<!\w)[^\W\d_]{{3,}}(?:{_OLUMSUZ_EK})[^\W\d_]*")
_OLUMSUZ_EK_BUYUK_RE = re.compile(
    r"(?<!\w)[A-ZÇĞIİÖŞÜ]{3,}(?:" + _OLUMSUZ_EK.replace("i", "İ").upper() + r")[A-ZÇĞIİÖŞÜ]*")


def _soru_koku(yazi: str) -> str:
    """Metnin "?" ile biten son cümlesi (soru kökü); yoksa boş."""
    cumleler = [c for c in re.split(r"(?<=[.!?…:])\s+", yazi.strip()) if c.strip()]
    return cumleler[-1] if cumleler and cumleler[-1].rstrip().endswith("?") else ""
_SIK_HEPSI_RE = re.compile(
    r"^(?:yukarıdakilerin\s+)?(?:hepsi|hiçbiri)(?:\s+doğru(?:dur)?)?$"
    r"|^(?:her\s+ikisi|ikisi\s+de)$|^[a-e]\s+ve\s+[a-e]$")
_ROMA = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}
_ONCUL_SIK_RE = re.compile(r"^(?:yalnız\s+)?(?:I{1,3}|IV|V)(?:\s*(?:,|ve)\s*(?:I{1,3}|IV|V))*\.?$")
_NESNE = "\ufffc"  # AMI etiketinin yerini tutar (kesir, üs...)


def _tr_kucuk(metin: str) -> str:
    return metin.replace("I", "ı").replace("İ", "i").lower()


def _ami_parcala(metin: str):
    """(görünen metin, altı çizili metinler) ya da AMI hatası.

    Etiketler tek bir nesne karakterine iner: ``{{frac|3|4}}`` yazım
    kurallarında «3/4» gibi görünmesin.
    """
    dugumler = _AMI.parse(metin)
    gorunen: list[str] = []
    alti: list[str] = []

    def gez(items, cizili: bool) -> None:
        for d in items:
            if isinstance(d, _AMI.Text):
                gorunen.append(d.value)
                if cizili:
                    alti.append(d.value)
            elif isinstance(d, _AMI.Styled):
                gez(d.children, cizili or d.kind == "u")
            else:
                gorunen.append(_NESNE)
    gez(dugumler, False)
    return "".join(gorunen), alti


def _gosterim_alanlari(k: dict) -> list[tuple[str, str]]:
    """(alan, metin) — URL ve kimlik alanları dışında okunan tüm metinler."""
    alanlar: list[tuple[str, str]] = []

    def ekle(alan, deger) -> None:
        if isinstance(deger, str):
            alanlar.append((alan, deger))
        elif isinstance(deger, list):
            for x in deger:
                ekle(alan, x)

    for alan in ("question", "context", "stemLead", "premises", "choices",
                 "choiceCells", "explanation", "distractorWhy"):
        ekle(alan, k.get(alan))
    sekiller = [k.get("figure")] + list(k.get("figures") or [])
    for sekil in sekiller:
        if isinstance(sekil, dict) and (sekil.get("kind") or sekil.get("type")) == "table":
            ekle("table", sekil.get("title"))
            ekle("table", sekil.get("rows"))
    # K15a: blok metni ve bilgi kutusu başlığı da K9 gösterim kurallarından geçer.
    for blok in k.get("blocks") or []:
        if isinstance(blok, dict):
            ekle("blocks", blok.get("v"))
            ekle("blocks", blok.get("title"))
    return alanlar


#: K15a bilgi kutusu (`blocks` öğesi `{"t": "callout", "title"?, "v"}`).
_KUTU_ALANLARI = {"t", "title", "v"}
_KUTU_BASLIK_EN_COK = 60
_KUTU_METIN_EN_COK = 1500


_duz = _AMI.plain  # bozuk işaretlemede metnin kendisi


def _kutu_bulgulari(k: dict) -> list[tuple[str, str, str]]:
    """G-CALLOUT-BOS / -ALAN (hata), G-CALLOUT-UZUN (uyarı)."""
    bulgular: list[tuple[str, str, str]] = []
    if "callout" in k:
        bulgular.append(("HATA", "G-CALLOUT-ALAN",
                         "callout soru kaydının üst düzeyinde olmaz; blocks öğesidir"))
    bloklar = k.get("blocks")
    for i, blok in enumerate(bloklar if isinstance(bloklar, list) else []):
        if not isinstance(blok, dict) or blok.get("t") != "callout":
            continue
        fazla = sorted(set(blok) - _KUTU_ALANLARI)
        if fazla:
            bulgular.append(("HATA", "G-CALLOUT-ALAN",
                             f"blocks[{i}]: tanımsız alan {', '.join(fazla)}; renk/ton temadan gelir"))
        baslik = blok.get("title")
        if "title" in blok and (not isinstance(baslik, str) or not baslik.strip()):
            bulgular.append(("HATA", "G-CALLOUT-ALAN",
                             f"blocks[{i}]: boş title yazılmaz; başlık yoksa alan hiç olmaz"))
        metin = blok.get("v")
        if not isinstance(metin, str) or not _duz(metin).strip():
            bulgular.append(("HATA", "G-CALLOUT-BOS", f"blocks[{i}]: bilgi kutusunun v metni boş"))
            continue
        if (isinstance(baslik, str) and len(_duz(baslik)) > _KUTU_BASLIK_EN_COK) \
                or len(_duz(metin)) > _KUTU_METIN_EN_COK:
            bulgular.append(("UYARI", "G-CALLOUT-UZUN",
                             f"blocks[{i}]: kutu uzun (başlık ≤ {_KUTU_BASLIK_EN_COK}, metin ≤ "
                             f"{_KUTU_METIN_EN_COK} karakter); uzun metin text bloğuna"))
    return bulgular


def _oncul_anahtari(sik: str):
    sayilar = [_ROMA[p] for p in re.findall(r"IV|V|I{1,3}", sik)]
    return len(sayilar), sorted(sayilar)


def gosterim_kontrol(k: dict) -> list[tuple[str, str, str]]:
    """Soru kaydının G- bulguları: ``(seviye, kural, mesaj)``.

    Sınıf ``grade`` alanından okunur; 5-8 dışı kayıtta yalnız AMI ve
    figure/figures kuralları çalışır. Türkçe dışı (``lang`` != tr) kayıtta
    sayı/tırnak/olumsuz kök kuralları uygulanmaz (İngilizce «3.5» doğrudur).
    """
    bulgular: list[tuple[str, str, str]] = []
    gorulen: set[str] = set()

    def bul(seviye: str, kural: str, mesaj: str) -> None:
        if kural not in gorulen:  # aynı kural kayıtta bir kez raporlanır
            gorulen.add(kural)
            bulgular.append((seviye, kural, mesaj))

    if k.get("figure") and k.get("figures"):
        bul("HATA", "G-FIGURE-FIGURES", "figure ile figures birlikte kullanılamaz")

    gorunur: list[tuple[str, str]] = []
    altlar: dict[str, list[str]] = {}
    for alan, metin in _gosterim_alanlari(k):
        try:
            yazi, alti = _ami_parcala(metin)
        except _AMI.AmiError as hata:
            kural = "G-AMI-BILINMEYEN" if hata.code == "ami_unknown_tag" else "G-AMI-KAPANMAMIS"
            bul("HATA", kural, f"{alan}: AMI sözdizimi hatası {hata.code} ({metin[:40]!r})")
            yazi, alti = metin, []
        gorunur.append((alan, yazi))
        altlar.setdefault(alan, []).extend(alti)

    sinif = k.get("grade")
    if type(sinif) is not int or not 5 <= sinif <= 8:
        return bulgular
    for seviye, kural, mesaj in _kutu_bulgulari(k):
        bul(seviye, kural, mesaj)
    if str(k.get("lang") or "tr") != "tr":
        return bulgular

    tum = " ".join(yazi for _, yazi in gorunur)
    saat_baglami = bool(_SAAT_BAGLAMI_RE.search(tum))
    oran_baglami = bool(_ORAN_BAGLAMI_RE.search(tum))
    matematik = "mat" in _tr_kucuk(str(k.get("subject") or ""))

    for alan, yazi in gorunur:
        def ara(desen: str):
            return re.search(desen, yazi)

        if m := ara(r"(?<![\d.,])\d{1,3}(?:\.\d{3})+(?![\d.,])"):
            if len(re.sub(r"\D", "", m.group())) >= 5:
                bul("HATA", "G-BINLIK", f"{alan}: binlik nokta {m.group()!r}; doğrusu «12 500»")
        if m := ara(r"(?<!\d)(?<!\d )\d \d{3}(?!\d)(?! \d{3})"):
            bul("UYARI", "G-BINLIK-4", f"{alan}: 4 basamakta boşluk {m.group()!r}; doğrusu «3500»")
        if m := ara(r"\d\s*%"):
            bul("HATA", "G-YUZDE", f"{alan}: yüzde işareti sonda {m.group()!r}; doğrusu «%25»")
        if m := ara(r"%\s+\d"):
            bul("HATA", "G-YUZDE-BOSLUK", f"{alan}: yüzde ile sayı arası boşluk {m.group()!r}")
        for m in re.finditer(r"(?<![\d.,])\d+\.\d{1,2}(?![\d.,]*\d)", yazi):
            saat = re.fullmatch(r"(?:[01]?\d|2[0-3])\.[0-5]\d", m.group())
            if not (saat and saat_baglami):
                bul("HATA", "G-ONDALIK-NOKTA", f"{alan}: ondalık nokta {m.group()!r}; doğrusu «3,5»")
                break
        if m := ara(r"\d\s*[xX]\s*\d"):
            bul("HATA", "G-CARPMA-X", f"{alan}: çarpma için x {m.group()!r}")
        if sinif >= 6 and (m := ara(r"\S\s*[·∙]\s*\S")):
            bul("HATA", "G-CARPMA-B7", f"{alan}: çarpma için U+00B7/U+2219; doğrusu «⋅» (U+22C5)")
        if m := ara(r"\d\s*\*\s*\d"):
            bul("HATA", "G-CARPMA-YILDIZ", f"{alan}: çarpma için * {m.group()!r}")
        for m in re.finditer(r"(?<![\d.,])(\d+)(\s*):(\s*)(\d+)(?![\d])", yazi):
            saat = (not m.group(2) and not m.group(3)
                    and re.fullmatch(r"(?:[01]?\d|2[0-3]):[0-5]\d", m.group()))
            if saat:
                bul("HATA", "G-SAAT-IKINOKTA", f"{alan}: saat {m.group()!r}; doğrusu «10.30»")
            elif sinif <= 7 and not oran_baglami:
                bul("HATA", "G-BOLME-IKINOKTA", f"{alan}: bölme için «:» {m.group()!r}; doğrusu «÷»")
        if matematik and (m := ara(r"(?<![\d/])\d+/\d+(?![\d/])")) and "http" not in yazi:
            bul("UYARI", "G-KESIR-EGIK", f"{alan}: düz kesir {m.group()!r}; {{{{frac|p|q}}}} kullanın")
        if "^" in yazi:
            bul("HATA", "G-US-SAPKA", f"{alan}: üs için ^; ² ya da {{{{sup|…}}}} kullanın")
        if m := ara(r"\d°C"):
            bul("HATA", "G-SICAKLIK-BITISIK", f"{alan}: {m.group()!r}; doğrusu «60 °C»")
        if m := ara(r"\d\s+°(?!\s*C)"):
            bul("HATA", "G-DERECE-BOSLUK", f"{alan}: açıda boşluk {m.group()!r}; doğrusu «45°»")
        if ara(r"[«»]"):
            bul("HATA", "G-TIRNAK-FRANSIZ", f"{alan}: « » tırnak; doğrusu “ ”")
        if '"' in yazi:
            bul("UYARI", "G-TIRNAK-DUZ", f'{alan}: düz " tırnak; doğrusu “ ”')
        if sinif >= 7:
            for m in re.finditer(r"−\s+\d", yazi):
                once = yazi[:m.start()].rstrip()
                if not once or once[-1] in "(=,;:[":
                    isaret = True
                else:
                    # "2x − 5", "x² − 16", "(a + 3)(a − 3)", "|AB| − 2": cebirsel terimden
                    # sonra ikili çıkarmadır (MEB yazımı). Sözel bağlamda ("Sıcaklık − 5")
                    # işaret eksi sayılır.
                    terim = re.search(r"[^\s(=,;:\[]+$", once).group()
                    isaret = not _CEBIR_TERIM_RE.fullmatch(terim) and bool(
                        re.search(r"[^\W\d_]{2,}$", terim))
                if isaret:
                    bul("UYARI", "G-EKSI-BOSLUKLU", f"{alan}: negatif sayıda boşluk {m.group()!r}")
                    break
        if alan in ("question", "stemLead"):
            kok = _soru_koku(yazi) if alan == "question" else ""
            if m := (_OLUMSUZ_BUYUK_RE.search(yazi) or _OLUMSUZ_EK_BUYUK_RE.search(kok)):
                bul("HATA", "G-OLUMSUZ-BUYUKHARF",
                    f"{alan}: {m.group()!r} büyük harfle; __{_tr_kucuk(m.group())}__ yazın")
            vurgulu = " ".join(altlar.get(alan, ()))
            for m in [*_OLUMSUZ_RE.finditer(yazi), *_OLUMSUZ_EK_RE.finditer(kok)]:
                if not re.search(rf"(?<!\w){m.group()}(?!\w)", vurgulu):
                    bul("HATA", "G-OLUMSUZ-VURGUSUZ",
                        f"{alan}: olumsuz sözcük {m.group()!r} altı çizili değil")
                    break

    siklar = [_AMI.plain(s).strip() for s in k.get("choices") or [] if isinstance(s, str)]
    for sik in siklar:
        if _SIK_HEPSI_RE.match(_tr_kucuk(sik).rstrip(".")):
            bul("HATA", "G-SIK-HEPSI", f"choices: {sik!r} (Hepsi/Hiçbiri/A ve B kullanılmaz)")
            break
    if len(siklar) >= 3 and all(_ONCUL_SIK_RE.match(s.replace("Yalnız", "yalnız"))
                                for s in siklar):
        anahtarlar = [_oncul_anahtari(s) for s in siklar]
        if k.get("choiceOrder") != "fixed" or anahtarlar != sorted(anahtarlar):
            bul("HATA", "G-ONCUL-KARISIK",
                "öncül kombinasyonlu şıklar choiceOrder=fixed ve kanonik sırada olmalı")
    return bulgular


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
    if not isinstance(dil, str) or dil not in DESTEKLENEN_DILLER:
        ekle("HATA", 23, 0, f"paket lang eksik veya desteklenmiyor: {dil!r}")
        dil = ""
    if paket is None:
        ekle("HATA", 11, 0, "paket satırı (type=pack) yok; id şeması doğrulanamaz")

    # ---- Şema V2 paket kuralları ----
    if paket:
        sv = paket.get("schemaVersion", "")
        if sv and sv not in ("2.0", "2.1", "2.2", "2.3"):
            ekle("HATA", 27, 0, f"desteklenmeyen schemaVersion: {sv!r}")
        src = paket.get("source", "")
        if sv in ("2.0", "2.1") and (not src or src == "unknown"):
            ekle("HATA", 28, 0, "source boş veya 'unknown'")
        prov = paket.get("provenance", "")
        if sv in ("2.0", "2.1") and prov:
            if prov.count(":") < 2:
                ekle("HATA", 29, 0, f"provenance format hatası: {prov!r}")
        if sv == "2.2":
            for satir_no, kayit in kayitlar:
                if kayit.get("type") not in {"pack", "note", "question"}:
                    continue
                for mesaj in ai_review_claim_errors(kayit):
                    ekle("HATA", 34, satir_no, mesaj)

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
    gorsel_soru_sayisi = 0
    kazanim_gorsel_sayac: dict = {}

    for satir_no, k in kayitlar:
        tip = k.get("type")
        if tip not in ("note", "question"):
            continue
        if "lang" in k and k["lang"] != dil:
            ekle("HATA", 23, satir_no, "kayıt lang değeri paket lang değeriyle uyuşmuyor")
        metinler = kayit_metinleri(k)
        birlesik = " ".join(metinler)

        # kural 10 — LaTeX
        m10 = LATEX_RE.search(birlesik)
        if m10:
            ekle("HATA", 10, satir_no, f"LaTeX izi: {m10.group()!r}")

        # G- gösterim kuralları (K9): MEB 5-8 yazım biçimi ve AMI sözdizimi
        if tip == "question":
            for seviye, kural, mesaj in gosterim_kontrol(k):
                ekle(seviye, kural, satir_no, mesaj)

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
        need = k.get("visualNeed")
        requirement = k.get("visualRequirement")
        if requirement not in ("required", "optional", "none") and isinstance(need, dict):
            requirement = need.get("level")
        if requirement in ("required", "optional", "none"):
            atif_var = requirement == "required" or (requirement == "optional" and bool(fig))
        if atif_var and not fig:
            ekle("HATA", 2, satir_no, "metin şekle atıf yapıyor ama figure boş")
        if fig and not atif_var:
            ekle("UYARI", 3, satir_no, "figure dolu ama metin ondan bahsetmiyor")

        # kural 4/5-9 — figür denetimi
        if isinstance(fig, dict):
            for genel_alan in FIGUR_GENEL_ZORUNLU:
                deger = fig.get(genel_alan)
                if not isinstance(deger, str) or not deger.strip():
                    ekle("HATA", 4, satir_no,
                         f"figure zorunlu erişilebilirlik alanı eksik/boş: {genel_alan}")
            for genel_alan in FIGUR_GENEL_ZORUNLU | {"captionKey"}:
                deger = fig.get(genel_alan)
                if isinstance(deger, str):
                    kullanilan_anahtarlar.add(deger)
                    if deger not in labels:
                        ekle("HATA", 9, satir_no,
                             f"figure {genel_alan} labels'ta yok: {deger!r}")
                    if GECICI_GORSEL_ANAHTARI_RE.search(deger):
                        ekle("HATA", 9, satir_no,
                             f"geçici görsel anahtarı kanonik hash değil: {deger!r}")
            if "svg" in fig:
                if tip != "note":
                    ekle("HATA", 5, satir_no,
                         "SVG yalnız konu anlatımı/not kaydında kullanılabilir")
                izinli_svg = {"svg"} | FIGUR_GENEL_ZORUNLU | FIGUR_GENEL_OPSIYONEL
                for alan in fig:
                    if alan not in izinli_svg:
                        ekle("HATA", 5, satir_no, f"SVG figure alanı izinsiz: {alan}")
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
                    if GECICI_GORSEL_ANAHTARI_RE.search(a):
                        ekle("HATA", 9, satir_no,
                             f"geçici görsel anahtarı kanonik hash değil: {a!r}")
            else:
                ekle("HATA", 4, satir_no, "figure ne 'kind' ne 'svg' içeriyor")
        elif fig is not None and fig != {}:
            ekle("HATA", 4, satir_no, f"figure nesne değil: {type(fig).__name__}")

        if tip == "note":
            continue

        if fig:
            gorsel_soru_sayisi += 1
            if k.get("objective"):
                kazanim_gorsel_sayac[k["objective"]] = (
                    kazanim_gorsel_sayac.get(k["objective"], 0) + 1
                )

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
        elif dogru >= len(secenekler):
            dogru = None  # şık yok; şık sayısı hatası yukarıda bildirildi
        # K2 (17 Eki): uygulama okuyucusu (read_atolye_package) boş ya da yalnız
        # boşluk şıkkı reddeder; doğrulayıcı aynı ölçütle HATA verir.
        for i, c in enumerate(secenekler):
            if not isinstance(c, str) or not c.strip():
                ekle("HATA", 12, satir_no, f"şık {i} boş ya da yalnız boşluk: {c!r}")
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

        # kural 13 — iki şık aynı sayıya eşit
        degerler = [(i, sayi_ayristir(str(c))) for i, c in enumerate(secenekler)]
        for a in range(len(degerler)):
            for b in range(a + 1, len(degerler)):
                va, vb = degerler[a][1], degerler[b][1]
                if va is not None and vb is not None and va == vb \
                        and normalize_metin(str(secenekler[a])) != normalize_metin(str(secenekler[b])):
                    ekle("HATA", 13, satir_no,
                         f"şık {a} ({secenekler[a]!r}) ile şık {b} ({secenekler[b]!r}) aynı sayı")

        # kural 14 — normalize soru tekrarı (öğrencinin gördüğü metnin tamamı + şekil)
        n_soru = soru_tekrar_anahtari(k)
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
        sv = (paket or {}).get("schemaVersion", "")
        nid = k.get("noteId")
        if sv == "2.2" and (not isinstance(nid, str) or not nid.strip()):
            ekle("HATA", 16, satir_no,
                 "schemaVersion=2.2 soru kaydında dolu noteId zorunlu")
        if sv == "2.2":
            for alan in ("topicKey", "subtopicKey", "noteKey"):
                if not isinstance(k.get(alan), str) or not k[alan].strip():
                    ekle("HATA", 16, satir_no,
                         f"schemaVersion=2.2 soru kaydında dolu {alan} zorunlu")
            if isinstance(nid, str) and nid.strip() and k.get("noteKey") != nid:
                ekle("HATA", 16, satir_no,
                     "noteKey, noteId ile aynı olmalı")
        if nid:
            hedef = notlar.get(nid)
            if hedef is None:
                ekle("HATA", 16, satir_no, f"noteId bulunamadı: {nid!r}")
            else:
                if sv == "2.2":
                    for alan in ("topicKey", "subtopicKey", "noteKey"):
                        if not isinstance(hedef.get(alan), str) or not hedef[alan].strip():
                            ekle("HATA", 16, satir_no,
                                 f"bağlı notta dolu {alan} zorunlu: {nid!r}")
                    if hedef.get("noteKey") != nid:
                        ekle("HATA", 16, satir_no,
                             f"bağlı notun noteKey değeri noteId ile uyuşmuyor: {nid!r}")
                    if any(k.get(alan) != hedef.get(alan)
                           for alan in ("topicKey", "subtopicKey", "noteKey")):
                        ekle("HATA", 16, satir_no,
                             "soru topicKey/subtopicKey/noteKey hiyerarşisi "
                             f"bağlı notla uyuşmuyor: {nid!r}")
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

        # kural 17/18 — 2.2'de ipucu sistemi yoktur. Eski 2.0/2.1
        # paketleri geriye uyumlu doğrulanmaya devam eder.
        ipuclari = k.get("hints") if isinstance(k.get("hints"), list) else []
        if sv == "2.2":
            if "hints" in k:
                ekle("HATA", 17, satir_no,
                     "schemaVersion=2.2 soru kaydında hints alanı yasaktır")
            ipuclari = []
        elif len(ipuclari) != 5 or any(not str(x or "").strip() for x in ipuclari):
            ekle("HATA", 17, satir_no,
                 f"hints 5 dolu basamak değil (uzunluk {len(ipuclari)})")

        # kural 18 — yalnız eski sözleşmelerde cevap sızıntısı
        if sv != "2.2" and dogru is not None and dogru < len(secenekler):
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
            if sv != "2.3" and "doğru" not in str(why[dogru]).casefold():
                ekle("HATA", 19, satir_no, "doğru indekste 'doğru' yazmıyor")
            elif sv == "2.3" and dogru_gerekcesi_jenerik(
                    str(why[dogru] or ""), secenekler[dogru]):
                ekle("HATA", 19, satir_no,
                     "doğru şık gerekçesi yalnız genel hüküm veya şık tekrarı içeriyor")
        if sv == "2.3":
            gorsel_gereksinimi = k.get("visualRequirement")
            if gorsel_gereksinimi not in {"required", "optional", "none"}:
                ekle("HATA", 36, satir_no,
                     "visualRequirement required|optional|none olmalı")
            elif gorsel_gereksinimi == "required" and not k.get("figure"):
                ekle("HATA", 36, satir_no, "zorunlu görsel eksik")
        jenerik = [
            i for i, w in enumerate(why[:len(secenekler)])
            if i != dogru
            and distraktor_gerekcesi_jenerik(w, secenekler[i])
        ]
        if jenerik:
            ekle("UYARI", 20, satir_no,
                 f"distractorWhy boş veya yalnız jenerik hüküm içeriyor: şık {jenerik}")

        # kural 21 — açıklamada şık harfi
        if dogru is not None and dogru < len("ABCDE") and isinstance(k.get("explanation"), str):
            harf = "ABCDE"[dogru]
            if re.search(r"(?i)(cevap|yanıt|şık|seçenek)\s*[:\-]?\s*" + harf + r"\b", k["explanation"]) \
                    or re.search(harf + r"\s+(şıkkı|seçeneği)", k["explanation"]):
                ekle("UYARI", 21, satir_no, f"explanation şık harfi veriyor ({harf})")

        # kural 24 — objective ↔ objectiveSource
        if k.get("objective") and not k.get("objectiveSource"):
            ekle("HATA", 24, satir_no, "objective dolu ama objectiveSource boş")

        # ---- Şema V2 soru kuralları ----
        if sv in ("2.0", "2.1", "2.2", "2.3"):
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
            if sv != "2.2":
                rs = k.get("reviewStatus", "")
                allowed_statuses = {
                    "pending", "reviewed", "ai-verified", "rejected"
                }
                if rs and rs not in allowed_statuses:
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
        if ".visual." in a:
            ekle("HATA", 9, 0,
                 f"pack labels içinde kullanılmayan görsel anahtarı var: {a!r}")
        else:
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

    # Şema 2.1/2.2 görsel politika kapısı. Eski 2.0 paketleri geriye uyumlu kalır;
    # yeni üretim sistemi visualPolicy olmadan yayın adımına geçemez.
    if paket and paket.get("schemaVersion") in {"2.1", "2.2", "2.3"}:
        politika = paket.get("visualPolicy")
        if not isinstance(politika, dict):
            ekle("HATA", 36, 0,
                 f"schemaVersion={paket.get('schemaVersion')} için visualPolicy nesnesi zorunlu")
        else:
            minimum = politika.get("questionMinimumPercent")
            if not _sayi_mi(minimum) or not 0 <= minimum <= 100:
                ekle("HATA", 36, 0,
                     "visualPolicy.questionMinimumPercent 0-100 olmalı")
            elif sorular:
                oran = gorsel_soru_sayisi / len(sorular) * 100
                if oran + 1e-9 < minimum:
                    ekle("HATA", 36, 0,
                         f"görsel soru oranı %{oran:.1f}; hedef en az %{minimum:g}")
            if politika.get("everyNote", False):
                for nid, not_kaydi in notlar.items():
                    if not not_kaydi.get("figure"):
                        ekle("HATA", 36, 0,
                             f"konu anlatımında figure zorunlu: {nid!r}")
            if politika.get("balancedByObjective", True):
                for objective, toplam in kazanim_sayac.items():
                    if toplam >= 5 and kazanim_gorsel_sayac.get(objective, 0) == 0:
                        ekle("HATA", 36, 0,
                             f"kazanımda hiç görsel soru yok: {objective!r} ({toplam} soru)")

    # kural 37 — LGS deneme paketi: assessment başlığı ve soru başına lgs bloğu
    lgs_kontrol(paket, sorular, ekle)

    # kural 38 — konu kartı tutarlılığı (17 Eki K9). Ders Arşivi konu kartlarını
    # (sınıf, ders) içinde topicKey ile gruplar ve adı MIN(topic) ile koyar:
    # bir anahtar birden çok konu adı taşırsa konular tek kartta toplanır, aynı
    # adı taşıyan iki anahtar ise aynı başlıklı iki kart olur.
    konu_adlari: dict = {}
    mufredat = (paket or {}).get("curriculum")
    paket_sinifi = (paket or {}).get("grade", mufredat.get("grade") if isinstance(mufredat, dict) else None)
    for _, k in kayitlar:
        if k.get("type") not in ("note", "question"):
            continue
        anahtar, ad = k.get("topicKey"), k.get("topic")
        if not (isinstance(anahtar, str) and anahtar.strip() and isinstance(ad, str) and ad.strip()):
            continue
        kapsam = (k.get("grade", paket_sinifi), k.get("subject", (paket or {}).get("subject")))
        konu_adlari.setdefault(kapsam, {}).setdefault(anahtar.strip(), set()).add(ad.strip())
    for (sinif, ders), anahtarlar in sorted(konu_adlari.items(), key=lambda x: str(x[0])):
        yer = f"{sinif}. sınıf {ders}" if sinif is not None else str(ders)
        for anahtar, adlar in sorted(anahtarlar.items()):
            if len(adlar) > 1:
                ekle("UYARI", 38, 0,
                     f"{yer}: topicKey {anahtar!r} birden çok konu adı taşıyor "
                     f"({', '.join(sorted(adlar))}); bunlar tek konu kartında toplanır")
        sahipler: dict = {}
        for anahtar, adlar in anahtarlar.items():
            for ad in adlar:
                sahipler.setdefault(normalize_metin(ad), (ad, set()))[1].add(anahtar)
        for ad, ortak in sorted(sahipler.values()):
            if len(ortak) > 1:
                ekle("UYARI", 38, 0,
                     f"{yer}: farklı topicKey'ler ({', '.join(sorted(ortak))}) aynı konu "
                     f"adını taşıyor ({ad!r}); aynı başlıklı iki kart görünür")

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
