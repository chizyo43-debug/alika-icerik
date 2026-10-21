"""AliKa Figure Spec 1.7 için saf, kanonik Windows doğrulaması."""
from __future__ import annotations

import math


KATALOG = {
    "numberline": {"zorunlu": {"min", "max"},
                   "opsiyonel": {"step", "marks", "highlight", "intervals", "jumps"}},  # jumps 1.6
    "fraction": {"zorunlu": {"style", "parts"}, "opsiyonel": {"filled", "wholes", "rows", "rowsFilled"}},
    "shape": {"zorunlu": {"type"},
              "opsiyonel": {"dims", "sideLabels", "marks", "sides", "points", "vertexKeys", "cubes",  # cubes 1.6
                            "circleParts", "centerKey", "net",  # 1.6 çember öğeleri, cisim açınımı
                            "view", "projection"}},  # 1.6 küp yapısının görünümü, izometrik çizim
    "angle": {"zorunlu": {"degrees"}, "opsiyonel": {"rays", "labelKey",
                                                  "transversal", "angleKeys", "lineKeys",  # 1.6 paraleller ve kesen
                                                  "construction",  # 1.6 açıortay pergel izi
                                                  "protractor",  # 1.6 iletki
                                                  "adjacent", "rayKeys", "vertexKey"}},  # 1.6 komşu açılar
    "grid": {"zorunlu": {"cols", "rows"}, "opsiyonel": {"shaded", "labels"}},
    "coordinate": {"zorunlu": {"xRange", "yRange"},
                   "opsiyonel": {"points", "segments", "labels", "step", "grid", "axes",
                                 "equalScale", "axisKeys", "polygons", "lines", "vectors"}},
    "chart": {"zorunlu": {"style", "categoryKeys", "values"},
              "opsiyonel": {"axisKeys", "orientation", "seriesKeys", "showPercent", "binEdges",
                            "unit", "unitKey", "symbol",
                            "title", "titleStyle", "axisUnits"}},  # 1.8 başlık, eksen birimi
    "table": {"zorunlu": {"headerKeys", "rows"},
              "opsiyonel": {"highlight", "title", "titleStyle", "rowHeaderBold"}},  # 1.8
    "flow": {"zorunlu": {"nodes", "edges"}, "opsiyonel": {"direction", "numbered"}},  # node.shape 1.6
    "circuit": {"zorunlu": {"elements"}, "opsiyonel": {"layout", "labelKeys"}},
    "diagram": {"zorunlu": {"elements"}, "opsiyonel": {"viewBox"}},
    "map": {
        "zorunlu": {"mapType", "regions"},
        "opsiyonel": {
            "viewBox", "points", "routes", "legend", "northArrow", "scaleKey",
            "boundarySetId", "boundaryVersion", "territoryReview",
        },
    },
    "timeline": {"zorunlu": {"events"}, "opsiyonel": {"orientation", "periods"}},
    # 1.6 olasılık araçları: torba (items), çark (sectors, pointer), zar (faces).
    "chance": {"zorunlu": {"tool"}, "opsiyonel": {"items", "sectors", "pointer", "faces",
                                                  "coins", "cards"}},  # 1.6 madeni para, kartlar
    # 1.6 modelleme araçları: cebir karoları, sayma pulları (groups), eşit kollu terazi (left/right).
    "model": {"zorunlu": {"tool"}, "opsiyonel": {"groups", "operators", "variable", "left", "right", "tilt"}},
    # 1.6 fen ölçme araçları: termometre, dinamometre, dereceli silindir (terazi: model/balance).
    "instrument": {"zorunlu": {"tool", "min", "max", "step", "readings"}, "opsiyonel": {"minor", "unit"}},
    # 1.6 ışık: düz aynada yansıma, iki ortam sınırında kırılma.
    "light": {"zorunlu": {"surface", "incidence"},
              "opsiyonel": {"refracted", "denser", "reflected", "angleKeys", "rayKeys", "mediumKeys", "normalKey"}},
    # 1.6 tanecik modeli: katı/sıvı/gaz panelleri, aralarında hal değişimi okları.
    "particles": {"zorunlu": {"panels"}, "opsiyonel": {"arrows", "motion"}},
}
CIRCUIT_ELEM = {
    "battery", "lamp", "switch", "resistor", "wire",
    # 1.6: ölçü aletleri ve alıcılar.
    "ammeter", "voltmeter", "motor", "buzzer", "led", "fuse",
}
CIRCUIT_ANAHTAR = ("open", "closed")  # 1.6 switch.state
CIRCUIT_ALAN = {"type", "labelKey", "state", "branch", "across"}
CIRCUIT_KOL_EN_COK = 4  # 1.6 parallel: branch 0..3
CIRCUIT_KOL_ELEMAN_EN_COK = 3  # kol başına ve ana hatta
AKIS_SEKIL = ("process", "decision", "terminal", "io")  # 1.6 akış şeması düğüm simgeleri
# 1.4: dashed/dotted her türde düz çizimin kesik/noktalı kenarlı biçimidir.
DIAGRAM_CIZGI_DESENI = {"dashed", "dotted"}
DIAGRAM_STIL = {
    "circle": {"plain", "sun", "earth", "moon", "planet", "pulley"} | DIAGRAM_CIZGI_DESENI,
    "ellipse": {"plain", "orbit", "asteroid_belt"} | DIAGRAM_CIZGI_DESENI,
    "rect": {"plain", "block", "battery"} | DIAGRAM_CIZGI_DESENI,
    "line": {"plain", "ray", "rope", "force"} | DIAGRAM_CIZGI_DESENI,
    "polygon": {"plain", "shadow", "support", "incline"} | DIAGRAM_CIZGI_DESENI,
    "arc": {"plain", "orbit"} | DIAGRAM_CIZGI_DESENI,
}
# LGS Ek 2: çizgi ok ucu; force/ray yazılmazsa "last" (kuvvet ve ışının yönü), diğerleri "none".
DIAGRAM_OK_UCU = ("none", "first", "last", "both")
DIAGRAM_RENK = {
    "ink", "muted", "accent", "gold", "success", "danger", "surface",
    "blue", "teal", "purple", "orange", "earth", "land", "moon", "white",
    "none",
    # 1.4 yumuşak tonlar: koyu çizgi ve etiket altında sakin dolgular.
    "paper", "gold-soft", "success-soft", "blue-soft", "muted-soft",
    "danger-soft", "accent-soft",
}
# 1.4 tarama yalnız kapalı şekillere uygulanır; çizgiler şeklin içine kırpılır.
DIAGRAM_TARAMA = {"hatch", "crosshatch"}
DIAGRAM_TARAMALI_TURLER = {"rect", "polygon", "circle", "ellipse"}
# 1.4 gök cismi görünümleri yalnız circle içindir; renkleri sabittir.
DIAGRAM_IKON = {
    "sun", "mercury", "venus", "earth", "moon", "mars",
    "jupiter", "saturn", "uranus", "neptune",
}
SATURN_HALKA_ACIKLIGI = 1.9
MAP_TURLERI = {"schematic", "political", "physical", "thematic", "route", "hazard", "weather"}
MAP_NOKTA_SEMBOLLERI = {"dot", "city", "capital", "station", "mountain", "port"}
MAP_ROTA_STILLERI = {"route", "river", "border", "front", "wind"}
FIGUR_GENEL_ZORUNLU = {"altTextKey"}
FIGUR_GENEL_OPSIYONEL = {"captionKey", "notToScale"}
# 1.5: diyagram çokgeni yay/daire dilimi gibi eğrileri taşıyabilsin diye 128 noktaya
# kadar çıkar; öğe sınırı (40) değişmez.
DIAGRAM_COKGEN_NOKTA = (3, 128)
# 1.5: width viewBox birimidir (çizimde clamp(width*ölçek*0.55, 1.5, 8) px).
DIAGRAM_CIZGI_KALINLIGI = (0.1, 8.0)
# 1.5: kurgusal haritaların boş zeminli, 0..100 normalize koordinatlı biçimi.
# Gerçek coğrafya tabanları (world/turkiye) sürümlü sınır verisi olmadan reddedilir.
MAP_BOS_ZEMIN_ALANLARI = {"base", "polygons", "markers", "routes"}
MAP_SINIR_VERISI_GEREKEN_TABANLAR = {"world", "turkiye"}
MAP_BOS_ZEMIN_SINIR = {"polygons": 32, "markers": 64, "routes": 32}
# 1.6: dört bölgeli koordinat düzlemi; ızgara/noktalı kâğıt, çokgen ve sonsuz doğru.
KOORDINAT_IZGARA = {"none", "lines", "dots"}
KOORDINAT_EN_COK_ARALIK = 40
KOORDINAT_COKGEN = (8, 3, 24)  # en çok çokgen, köşe sayısı alt/üst sınırı
KOORDINAT_DOGRU = 4
KOORDINAT_DOGRU_STIL = ("line", "axis")  # 1.6 axis = simetri ekseni: kesik, oksuz
KOORDINAT_VEKTOR = 4  # 1.6 öteleme okları
# 1.6: sayı doğrusunda açık/kapalı uçlu aralık ve eşitsizlik ışını (uç yazılmazsa ışın).
SAYI_DOGRUSU_ARALIK = 4
# 1.6: sayı doğrusunda atlama okları (toplama/çıkarma, ardışık ekleme); yay yüksekliği sınırları px.
SAYI_DOGRUSU_SICRAMA = 6
SICRAMA_YAY = (16.0, 46.0, 0.35)  # en az, en çok, açıklığa oranı
# 1.6: grafik stilleri; nokta grafiği sıklık (0..20 tam sayı), histogram bitişik sütun,
# şekil grafiği satırda en çok 12 sembol (yarım sembol olur), çetele 0..30 tam sayı.
GRAFIK_STIL = ("bar", "line", "pie", "dot", "histogram", "pictograph", "tally")
GRAFIK_SERI = (2, 4)
GRAFIK_NOKTA_EN_COK = 20
GRAFIK_SEMBOL = ("circle", "square", "star")
GRAFIK_SEMBOL_EN_COK = 12
GRAFIK_CETELE_EN_COK = 30
# Çetele: grup içi çizgi aralığı step, grup adımı 5,5·step; çapraz çizgi -0,6..3,6·step.
CETELE_GRUP_ADIMI = 5.5
# 1.6: bileşik/tam sayılı kesir modeli en çok 4 bütünle çizilir.
KESIR_BUTUN_EN_COK = 4
KESIR_ALAN_EN_COK = 12  # 1.6 alan modeli: sütun (parts) ve satır (rows) en çok
# 1.6 olasılık araçları. Renkler iki platformda aynı onaltılık değerlerdir
# (Android FigureMath.CHANCE_COLORS).
SANS_ARAC = ("bag", "spinner", "dice", "coin", "cards")
SANS_ALAN = {"bag": "items", "spinner": "sectors", "dice": "faces", "coin": "coins", "cards": "cards"}
SANS_RENK = {
    "red": "#E5484D", "blue": "#3E7BFA", "green": "#2F9E57", "yellow": "#F5C518",
    "purple": "#8E5BD0", "orange": "#F2873A", "white": "#FFFFFF", "black": "#2A2F36",
}
SANS_TORBA = ("#EFD9B4", "#A8743A")  # torba gövdesi ve bağı
SANS_TOP_RENK_EN_COK = 6
SANS_TOP_EN_COK = 30
SANS_DILIM = (2, 12)
SANS_AGIRLIK_EN_COK = 12
SANS_ZAR_EN_COK = 3
SANS_PARA = ("#E9C46A", "#B8892E")  # madeni para yüzü; iç halka ve yüz simgesi
SANS_PARA_YUZ = ("heads", "tails")  # tura (yıldız amblem), yazı ("1" rakamı)
SANS_PARA_EN_COK = 4
SANS_KART_EN_COK = 12
SANS_KART_SIRA = 6  # bir sırada en çok kart
SANS_KART_DEGER = 99
SANS_KOYU = ("red", "blue", "green", "purple", "black")  # üstüne beyaz yazılan renkler
# Zar yüzü noktaları birim karede (0..1, y aşağı).
ZAR_NOKTA = {
    1: ((.5, .5),),
    2: ((.27, .27), (.73, .73)),
    3: ((.27, .27), (.5, .5), (.73, .73)),
    4: ((.27, .27), (.73, .27), (.27, .73), (.73, .73)),
    5: ((.27, .27), (.73, .27), (.5, .5), (.27, .73), (.73, .73)),
    6: ((.27, .25), (.73, .25), (.27, .5), (.73, .5), (.27, .75), (.73, .75)),
}
SAYI_DOGRUSU_ARALIK_ALANLARI = {"from", "to", "fromClosed", "toClosed", "labelKey", "color"}
SAYI_DOGRUSU_SICRAMA_ALANLARI = {"from", "to", "labelKey", "color"}


def _sayi_mi(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _diagram_14_hatalari(i, tur, eleman, diagram_inside) -> list:
    """Figure Spec 1.4 tarama ve gök cismi alanlarını denetler."""
    h = []
    desen = eleman.get("pattern")
    if "pattern" in eleman and (
        tur not in DIAGRAM_TARAMALI_TURLER
        or not isinstance(desen, str) or desen not in DIAGRAM_TARAMA
    ):
        h.append(f"diagram: elements[{i}].pattern yalnız rect/polygon/circle/ellipse için hatch|crosshatch olur")
    desen_rengi = eleman.get("patternColor")
    if "patternColor" in eleman and (
        "pattern" not in eleman or not isinstance(desen_rengi, str)
        or desen_rengi not in DIAGRAM_RENK or desen_rengi == "none"
    ):
        h.append(f"diagram: elements[{i}].patternColor pattern ve görünür renk ister")
    if "icon" in eleman:
        ikon = eleman["icon"]
        if tur != "circle" or not isinstance(ikon, str) or ikon not in DIAGRAM_IKON:
            h.append(f"diagram: elements[{i}].icon yalnız circle için beyaz listeden olur")
        elif eleman.get("style", "plain") not in {"plain"} | DIAGRAM_CIZGI_DESENI:
            # Gök cismi kendi görünümünü çizer; sun/earth gibi eski stillerle karışmaz.
            h.append(f"diagram: elements[{i}].icon anlamsal stil ile birlikte yazılmaz")
        elif ikon == "saturn":
            x, y, r = eleman.get("x"), eleman.get("y"), eleman.get("r")
            if not all(_sayi_mi(v) and math.isfinite(float(v)) for v in (x, y, r)) or not (
                diagram_inside([x - SATURN_HALKA_ACIKLIGI * r, y])
                and diagram_inside([x + SATURN_HALKA_ACIKLIGI * r, y])
            ):
                h.append(f"diagram: elements[{i}] Satürn halkası viewBox içinde olmalı")
    return h


def _bos_zemin_harita_hatalari(fig: dict) -> list:
    """1.5 base=blank haritası: kapalı alan listesi, 0..100 normalize koordinat."""
    h = []
    izinli = MAP_BOS_ZEMIN_ALANLARI | FIGUR_GENEL_ZORUNLU | FIGUR_GENEL_OPSIYONEL | {"kind"}
    for alan in sorted(FIGUR_GENEL_ZORUNLU):
        if alan not in fig:
            h.append(f"map: zorunlu alan eksik: {alan}")
    for alan in fig:
        if alan not in izinli:
            h.append(f"map: base biçiminde olmayan alan: {alan}")
    if h:
        return h
    taban = fig.get("base")
    if taban in MAP_SINIR_VERISI_GEREKEN_TABANLAR:
        return [f"map: base={taban} için sürümlü sınır verisi yok; yalnız blank kabul edilir"]
    if taban != "blank":
        return ["map: base yalnız blank olabilir"]

    def _nokta(pair):
        return (
            isinstance(pair, list) and len(pair) == 2
            and all(_sayi_mi(v) and math.isfinite(float(v)) and 0 <= float(v) <= 100 for v in pair)
        )

    def _etiket(oge, i, ad):
        if "labelKey" in oge and (not isinstance(oge["labelKey"], str) or not oge["labelKey"].strip()):
            h.append(f"map: {ad}[{i}].labelKey boş olamaz")

    toplam = 0
    for ad in ("polygons", "markers", "routes"):
        liste = fig.get(ad, [])
        if not isinstance(liste, list) or len(liste) > MAP_BOS_ZEMIN_SINIR[ad]:
            h.append(f"map: {ad} 0..{MAP_BOS_ZEMIN_SINIR[ad]} öğeli liste değil")
            return h
        toplam += len(liste)
    if toplam == 0:
        h.append("map: en az bir çokgen, işaret veya rota gerekir")
    kimlikler: set = set()
    for i, oge in enumerate(fig.get("polygons", [])):
        if not isinstance(oge, dict) or set(oge) - {"id", "points", "labelKey", "colorToken"}:
            h.append(f"map: polygons[{i}] yalnız id/points/labelKey/colorToken içerebilir")
            continue
        kimlik, noktalar = oge.get("id"), oge.get("points")
        if not isinstance(kimlik, str) or not kimlik.strip() or kimlik in kimlikler:
            h.append(f"map: polygons[{i}].id boş veya tekrarlı")
        kimlikler.add(kimlik)
        if (not isinstance(noktalar, list) or not 3 <= len(noktalar) <= 128
                or not all(_nokta(p) for p in noktalar)):
            h.append(f"map: polygons[{i}].points 3..128 nokta ve 0..100 içinde olmalı")
        if "colorToken" in oge and (oge["colorToken"] not in DIAGRAM_RENK or oge["colorToken"] == "none"):
            h.append(f"map: polygons[{i}].colorToken beyaz liste dışı")
        _etiket(oge, i, "polygons")
    for i, oge in enumerate(fig.get("markers", [])):
        if not isinstance(oge, dict) or set(oge) - {"id", "x", "y", "labelKey"}:
            h.append(f"map: markers[{i}] yalnız id/x/y/labelKey içerebilir")
            continue
        if "id" in oge and (not isinstance(oge["id"], str) or not oge["id"].strip()):
            h.append(f"map: markers[{i}].id boş olamaz")
        if not _nokta([oge.get("x"), oge.get("y")]):
            h.append(f"map: markers[{i}] x/y 0..100 içinde olmalı")
        _etiket(oge, i, "markers")
    for i, oge in enumerate(fig.get("routes", [])):
        if not isinstance(oge, dict) or set(oge) - {"points", "labelKey"}:
            h.append(f"map: routes[{i}] yalnız points/labelKey içerebilir")
            continue
        noktalar = oge.get("points")
        if (not isinstance(noktalar, list) or not 2 <= len(noktalar) <= 64
                or not all(_nokta(p) for p in noktalar)):
            h.append(f"map: routes[{i}].points 2..64 nokta ve 0..100 içinde olmalı")
        _etiket(oge, i, "routes")
    return h


SEKIL_KOSE = (3, 12)  # 1.6 polygon köşe sayısı alt/üst sınırı
SEKIL_ESIT_GRUP = 3  # eş kenar grubu; grup k (0'dan) k+1 çentikle çizilir
SEKIL_ACI_TOLERANS = 1.0  # derece; dik açı işareti gerçek 90°'ye bu kadar yakın olmalı
SEKIL_ESIT_TOLERANS = 0.01  # eş kenar işareti: göreli uzunluk farkı
SEKIL_ACI_YAY = 22.0  # px; şekil içi/dış açı yayının en büyük yarıçapı
SEKIL_DIS_UZATMA = 40.0  # px; dış açıda kenarın köşeden öteye uzatılan boyu
SEKIL_PARALEL_GRUP = 3  # paralel kenar grubu; grup k (0'dan) k+1 ok başıyla çizilir
SEKIL_ISARET_ALANLARI = {"equal", "parallel", "right", "angles", "exterior", "height", "median", "bisector"}


def shape_vertices(fig: dict) -> list:
    """1.6 square/rect/triangle/polygon köşeleri: birim uzunlukta, y yukarı.

    Hazır şekillerde v0 sol alt köşedir ve köşeler saat yönü tersine sıralanır;
    kenar i, köşe i ile köşe i+1 arasındadır. Üçgende kenar 0 = c (taban),
    kenar 1 = a, kenar 2 = b. polygon `points` yazarın sırasını korur; `sides`
    tabanı yatay düzgün çokgendir. Çizilemeyen üçgende ValueError.
    """
    tur, dims = fig.get("type"), fig.get("dims") or {}
    if tur in ("square", "rect"):
        dw = float(dims.get("w", 1))
        dh = dw if tur == "square" else float(dims.get("h", 1))
        return [(0.0, 0.0), (dw, 0.0), (dw, dh), (0.0, dh)]
    if tur == "triangle":
        # Eksik kenarlar şematik tamamlanır; tahmin edilen değer etiketlenmez.
        yedek = max((float(dims[k]) for k in ("a", "b", "c") if k in dims), default=1.0)
        a, b, taban = (float(dims.get(k, yedek)) for k in ("a", "b", "c"))
        if not abs(a - b) < taban < a + b:
            raise ValueError("Üçgen kenarları üçgen eşitsizliğini sağlamıyor.")
        x = (b * b + taban * taban - a * a) / (2 * taban)
        return [(0.0, 0.0), (taban, 0.0), (x, math.sqrt(max(0.0, b * b - x * x)))]
    if tur == "polygon":
        if fig.get("points"):
            return [(float(x), float(y)) for x, y in fig["points"]]
        n = int(fig.get("sides", 6))
        return [
            (math.cos(a), math.sin(a))
            for a in (-math.pi / 2 - math.pi / n + 2 * math.pi * k / n for k in range(n))
        ]
    return []


def shape_parallel_marks(points: list, groups: list, equal_groups: list = ()) -> list:
    """1.6 paralel kenar okları (ekran, y aşağı). Grup k (0'dan) k+1 iç içe ok başıyla işaretlenir;
    gruptaki bütün oklar grubun ilk kenarının yönünü gösterir. Ok başı kenarın ortasındadır; kenar eş
    çentik de taşıyorsa oklar çentiklerin ötesine, ok yönünde kayar. Her ok başı [kol, uç, kol] üç
    noktadır (derinlik 6, yarı açıklık 5, ardışık uçlar 6 aralıklı). Android `FigureMath.shapeParallelMarks`."""
    n = len(points)
    esit = {kenar: g for g, grup in enumerate(equal_groups) for kenar in grup}
    oklar = []
    for k, grup in enumerate(groups):
        (ax, ay), (bx, by) = points[grup[0]], points[(grup[0] + 1) % n]
        for kenar in grup:
            (x1, y1), (x2, y2) = points[kenar], points[(kenar + 1) % n]
            boy = math.hypot(x2 - x1, y2 - y1) or 1.0
            ux, uy = (x2 - x1) / boy, (y2 - y1) / boy
            if ux * (bx - ax) + uy * (by - ay) < 0:
                ux, uy = -ux, -uy
            # Çentik yarı yayılımı + 2 + 8 boşluk + ok kümesinin yarısı (3 + 3k).
            kay = esit[kenar] * 2.5 + 13 + 3 * k if kenar in esit else 0.0
            mx, my = (x1 + x2) / 2 + ux * kay, (y1 + y2) / 2 + uy * kay
            for j in range(k + 1):
                t = 3 + (j - k / 2) * 6
                tx, ty = mx + ux * t, my + uy * t
                oklar.append([(tx - ux * 6 - uy * 5, ty - uy * 6 + ux * 5), (tx, ty),
                              (tx - ux * 6 + uy * 5, ty - uy * 6 - ux * 5)])
    return oklar


def _kesisir(p1, p2, p3, p4) -> bool:
    """İki doğru parçası (uçlar dahil) kesişir mi."""
    def yon(a, b, c):
        v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        return 0 if abs(v) < 1e-12 else (1 if v > 0 else -1)

    def ustunde(a, b, c):
        return min(a[0], b[0]) - 1e-12 <= c[0] <= max(a[0], b[0]) + 1e-12 and \
            min(a[1], b[1]) - 1e-12 <= c[1] <= max(a[1], b[1]) + 1e-12

    d1, d2, d3, d4 = yon(p3, p4, p1), yon(p3, p4, p2), yon(p1, p2, p3), yon(p1, p2, p4)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    return any(d == 0 and ustunde(a, b, c) for d, a, b, c in (
        (d1, p3, p4, p1), (d2, p3, p4, p2), (d3, p1, p2, p3), (d4, p1, p2, p4)))


def polygon_simple(points: list) -> bool:
    """Alanı sıfır olmayan, kendini kesmeyen kapalı çokgen mi."""
    n = len(points)
    alan = sum(points[i][0] * points[(i + 1) % n][1] - points[(i + 1) % n][0] * points[i][1] for i in range(n)) / 2
    olcek = max(max(abs(v) for p in points for v in p), 1e-9)
    if abs(alan) <= 1e-9 * olcek * olcek:
        return False
    kenarlar = [(points[i], points[(i + 1) % n]) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                continue
            if _kesisir(*kenarlar[i], *kenarlar[j]):
                return False
    return all(points[i] != points[(i + 1) % n] for i in range(n))


def shape_cevian(points: list, kind: str, frm: int) -> dict:
    """1.6 üçgende kenarortay (median) ya da iç açıortay (bisector): köşe frm'den karşı kenara
    (kenar frm+1). foot ayak; t ayağın kenardaki konumu (0 = köşe frm+1, 1 = köşe frm+2).
    Açıortay ayağı karşı kenarı komşu kenarların oranında böler. Android `FigureMath.shapeCevian` aynası."""
    v, a, b = points[frm], points[(frm + 1) % 3], points[(frm + 2) % 3]
    t = 0.5 if kind == "median" else math.dist(v, a) / ((math.dist(v, a) + math.dist(v, b)) or 1.0)
    return {"foot": (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), "t": t}


def shape_angle(points: list, index: int) -> float:
    """Köşedeki iç açının ölçüsü (derece, 0..180 arası geometrik açı)."""
    n = len(points)
    v, p, q = points[index], points[index - 1], points[(index + 1) % n]
    a = math.atan2(p[1] - v[1], p[0] - v[0]) - math.atan2(q[1] - v[1], q[0] - v[0])
    a = abs(math.degrees(a)) % 360
    return 360 - a if a > 180 else a


CEMBER_PARCA = {  # 1.6 circleParts türü -> gerekli açı alanları (derece, 0 sağ, saat yönü tersi)
    "radius": ("at",), "diameter": ("at",), "point": ("at",),
    "chord": ("from", "to"), "arc": ("from", "to"), "sector": ("from", "to"),
}
CEMBER_PARCA_EN_COK = 8


def circle_parts(fig: dict) -> list:
    """1.6 çember öğeleri; eski dims.r / sideLabels.r yarıçap öğesi yoksa 0°'de yarıçap olur."""
    parts = [dict(p) for p in fig.get("circleParts") or []]
    dims, keys = fig.get("dims") or {}, fig.get("sideLabels") or {}
    if (keys.get("r") or dims.get("r")) and not any(p.get("kind") == "radius" for p in parts):
        legacy = {"kind": "radius", "at": 0.0}
        if keys.get("r"):
            legacy["labelKey"] = keys["r"]
        else:
            legacy["labelValue"] = dims["r"]
        parts.insert(0, legacy)
    return parts


def _ekran_yonu(derece: float) -> tuple:
    a = math.radians(derece)
    return math.cos(a), -math.sin(a)


def _yukari_dik(u: tuple) -> tuple:
    """Yönün iki dikinden ekranda yukarı (yoksa sağa) bakanı."""
    if abs(u[0]) < 1e-9:
        return 1.0, 0.0
    return (u[1], -u[0]) if -u[0] < 0 else (-u[1], u[0])


def circle_layout(fig: dict, w: float, h: float, size) -> dict:
    """1.6 çember yerleşimi (Android `FigureMath.circleLayout` aynası).

    size(öğe) yazının (yarı genişlik, yarı yükseklik) ölçüsünü verir; öğe labelKey ya da
    labelValue taşır. Dışarıdaki adlar (nokta, yay, sığmayan dilim açısı) tuvale sığana
    kadar çember küçülür, yazı küçülmez. Dönüş ekran koordinatıdır (y aşağı); açılar
    matematik yönünde derece (Tk create_arc ile aynı).
    """
    parts = circle_parts(fig)
    cx, cy = w / 2, h / 2
    base = max(24.0, min(w, h) / 2 - 12)

    def uzanim(n, hw, hh, gap):
        return gap + abs(n[0]) * hw + abs(n[1]) * hh

    def sigdir(disari):
        r = base
        for (ux, uy), rc, hw, hh in disari:
            for d, half, centre, boy in ((ux, hw, cx, w), (uy, hh, cy, h)):
                if d > 1e-9:
                    r = min(r, (boy - 4 - half - centre) / d - rc)
                elif d < -1e-9:
                    r = min(r, (centre - 4 - half) / -d - rc)
        return max(r, 24.0)

    sweep = lambda p: (p["to"] - p["from"]) % 360
    disari, dilim_disari = [], set()
    for p in parts:
        if p["kind"] in ("point", "arc") and ("labelKey" in p or "labelValue" in p):
            u = _ekran_yonu(p["at"] if p["kind"] == "point" else p["from"] + sweep(p) / 2)
            hw, hh = size(p)
            disari.append((u, uzanim(u, hw, hh, 6 if p["kind"] == "point" else 8), hw, hh))
    r = sigdir(disari)
    ark = lambda r: min(SEKIL_ACI_YAY, 0.3 * r)

    def dilim_uzaklik(p, r):
        hw, hh = size(p)
        rho = math.hypot(hw, hh)
        yarim = math.radians(sweep(p) / 2)
        d = ark(r) + rho + 4
        if yarim < math.pi / 2:
            d = max(d, (rho + 4) / max(math.sin(yarim), 1e-3))
        return d, rho

    for _ in range(2):
        # Merkez açı adı dilimin içine sığmazsa yayın dışına, açıortay yönünde geçer.
        for i, p in enumerate(parts):
            if p["kind"] == "sector" and "labelKey" in p and i not in dilim_disari:
                d, rho = dilim_uzaklik(p, r)
                if d + rho + 4 > r:
                    dilim_disari.add(i)
                    u = _ekran_yonu(p["from"] + sweep(p) / 2)
                    hw, hh = size(p)
                    disari.append((u, uzanim(u, hw, hh, 6), hw, hh))
        r = sigdir(disari)

    nokta = lambda derece, uzak=None: (cx + (r if uzak is None else uzak) * _ekran_yonu(derece)[0],
                                       cy + (r if uzak is None else uzak) * _ekran_yonu(derece)[1])
    lines, sectors, arcs, angle_arcs, dots, labels, yonler = [], [], [], [], [], [], []

    def ad(p, x, y):
        labels.append((p, (x, y)))

    for i, p in enumerate(parts):
        k, adli = p["kind"], "labelKey" in p or "labelValue" in p
        if k in ("radius", "diameter"):
            a = p["at"]
            lines.append((nokta(a + 180) if k == "diameter" else (cx, cy), nokta(a), k))
            yonler += [a % 360] + ([(a + 180) % 360] if k == "diameter" else [])
            if adli:
                u, (hw, hh) = _ekran_yonu(a), size(p)
                n = _yukari_dik(u)
                rc = uzanim(n, hw, hh, 6)
                ad(p, cx + u[0] * r / 2 + n[0] * rc, cy + u[1] * r / 2 + n[1] * rc)
        elif k == "chord":
            (ax, ay), (bx, by) = nokta(p["from"]), nokta(p["to"])
            lines.append(((ax, ay), (bx, by), k))
            if adli:
                mx, my = (ax + bx) / 2, (ay + by) / 2
                boy = math.hypot(cx - mx, cy - my)
                if boy > 1:
                    n = ((cx - mx) / boy, (cy - my) / boy)
                else:
                    kb = math.hypot(bx - ax, by - ay) or 1.0
                    n = _yukari_dik(((bx - ax) / kb, (by - ay) / kb))
                hw, hh = size(p)
                rc = uzanim(n, hw, hh, 6)
                ad(p, mx + n[0] * rc, my + n[1] * rc)
        elif k == "sector":
            s = sweep(p)
            sectors.append((p["from"] % 360, s, p.get("shaded", True)))
            lines += [((cx, cy), nokta(p["from"]), k), ((cx, cy), nokta(p["to"]), k)]
            yonler += [p["from"] % 360, p["to"] % 360]
            if "labelKey" in p:
                orta = p["from"] + s / 2
                angle_arcs.append((p["from"] % 360, s, ark(r)))
                if i in dilim_disari:
                    u, (hw, hh) = _ekran_yonu(orta), size(p)
                    rc = uzanim(u, hw, hh, 6)
                    ad(p, *nokta(orta, r + rc))
                else:
                    yonler.append(orta % 360)
                    ad(p, *nokta(orta, dilim_uzaklik(p, r)[0]))
        elif k == "arc":
            s = sweep(p)
            arcs.append((p["from"] % 360, s))
            if adli:
                orta = p["from"] + s / 2
                u, (hw, hh) = _ekran_yonu(orta), size(p)
                ad(p, *nokta(orta, r + uzanim(u, hw, hh, 8)))
        elif k == "point":
            dots.append(nokta(p["at"]))
            if adli:
                u, (hw, hh) = _ekran_yonu(p["at"]), size(p)
                ad(p, *nokta(p["at"], r + uzanim(u, hw, hh, 6)))
    merkez = fig.get("centerKey")
    if merkez or yonler:
        dots.append((cx, cy))
    if merkez:
        # Merkez adı merkezden çıkan çizgiler arasındaki en geniş boşluğun ortasına yazılır.
        if yonler:
            sirali = sorted(set(round(a, 6) for a in yonler))
            bosluk = [((sirali[(j + 1) % len(sirali)] - a) % 360 or 360, a) for j, a in enumerate(sirali)]
            genis, bas = max(bosluk)
            yon = bas + genis / 2
        else:
            yon = 225.0
        oge = {"kind": "centre", "labelKey": merkez}
        u, (hw, hh) = _ekran_yonu(yon), size(oge)
        ad(oge, *nokta(yon, uzanim(u, hw, hh, 5)))
    return {"centre": (cx, cy), "radius": r, "lines": lines, "sectors": sectors, "arcs": arcs,
            "angle_arcs": angle_arcs, "dots": dots, "labels": labels}


def _cember_hatalari(fig: dict) -> list:
    """1.6 circle: centerKey ve circleParts öğeleri."""
    h = []
    if "centerKey" in fig and not (isinstance(fig["centerKey"], str) and fig["centerKey"].strip()):
        h.append("shape: centerKey boş olmayan anahtar olmalı")
    if "circleParts" not in fig:
        return h
    parcalar = fig["circleParts"]
    if not isinstance(parcalar, list) or not 1 <= len(parcalar) <= CEMBER_PARCA_EN_COK:
        return h + [f"shape: circleParts 1..{CEMBER_PARCA_EN_COK} öğeli liste olmalı"]
    aci = lambda v: _sayi_mi(v) and math.isfinite(float(v)) and 0 <= v < 360
    dolu = lambda v: isinstance(v, str) and bool(v.strip())
    for i, p in enumerate(parcalar):
        tur = p.get("kind") if isinstance(p, dict) else None
        if tur not in CEMBER_PARCA:
            h.append(f"shape: circleParts[{i}].kind radius|diameter|chord|arc|sector|point olmalı")
            continue
        gerekli = set(CEMBER_PARCA[tur])
        izinli = gerekli | {"kind", "labelKey"} | ({"shaded"} if tur == "sector" else set())
        if not gerekli <= set(p) or set(p) - izinli:
            h.append(f"shape: circleParts[{i}] ({tur}) yalnız {sorted(izinli)} içerir; gerekli {sorted(gerekli)}")
        elif not all(aci(p[k]) for k in gerekli):
            h.append(f"shape: circleParts[{i}] açıları 0 ≤ derece < 360 sayı olmalı")
        elif "from" in gerekli and p["from"] == p["to"]:
            h.append(f"shape: circleParts[{i}] from ve to aynı olamaz")
        elif ("labelKey" in p and not dolu(p["labelKey"])) or (tur == "point" and "labelKey" not in p):
            h.append(f"shape: circleParts[{i}] labelKey boş olmayan anahtar olmalı (point için zorunlu)")
        elif "shaded" in p and not isinstance(p["shaded"], bool):
            h.append(f"shape: circleParts[{i}] shaded true/false olmalı")
    return h


def _kesen_hatalari(fig: dict) -> list:
    """1.6 angle.transversal: paralel iki doğru ve kesen; angleKeys / lineKeys adları."""
    h = []
    kesen = fig.get("transversal", False)
    if not isinstance(kesen, bool):
        return ["angle: transversal true/false olmalı"]
    if not kesen:
        if "lineKeys" in fig or ("angleKeys" in fig and "adjacent" not in fig):
            h.append("angle: angleKeys yalnız transversal=true ya da adjacent ile, lineKeys yalnız transversal=true ile yazılır")
        return h
    d = fig.get("degrees")
    if _sayi_mi(d) and not KESEN_ACI[0] <= d <= KESEN_ACI[1]:
        h.append(f"angle: transversal açısı {KESEN_ACI[0]} ≤ degrees ≤ {KESEN_ACI[1]} olmalı")
    if "rays" in fig or "labelKey" in fig:
        h.append("angle: transversal ile rays ve labelKey yazılmaz (açı adları angleKeys ile)")
    dolu = lambda v: isinstance(v, str) and bool(v.strip())
    for alan, izinli in (("angleKeys", {str(i) for i in range(1, 9)}), ("lineKeys", {"0", "1", "2"})):
        if alan not in fig:
            continue
        v = fig[alan]
        if not isinstance(v, dict) or not v or set(v) - izinli or not all(dolu(x) for x in v.values()):
            h.append(f"angle: {alan} {{sıra: anahtar}} olmalı; sıra {'1..8' if alan == 'angleKeys' else '0, 1, 2'}, anahtar boş olmaz")
    return h


KOMSU_EN_AZ = 15  # 1.6 adjacent: her komşu açı en az bu kadar derece (ad ışınlar arasına sığsın)
KOMSU_EN_COK = 6
# Yan yana yaylar karışmasın: sırayla küçük/büyük yarıçap ve iki renk; 360'ta tek sayılı son açı üçüncü biçimde.
KOMSU_YAY = ((28.0, "accent"), (44.0, "purple"), (36.0, "success"))


def _komsu_hatalari(fig: dict) -> list:
    """1.6 angle.adjacent: tek köşede yan yana açılar (komşu, tümler, bütünler; 360'ta ters açılar)."""
    h = []
    parcalar = fig["adjacent"]
    if (not isinstance(parcalar, list) or not 1 <= len(parcalar) <= KOMSU_EN_COK
            or not all(_sayi_mi(p) and p >= KOMSU_EN_AZ for p in parcalar)):
        return [f"angle: adjacent 1..{KOMSU_EN_COK} adet, her biri ≥ {KOMSU_EN_AZ} derece olmalı"]
    d = fig.get("degrees")
    if _sayi_mi(d) and abs(sum(parcalar) - d) > 1e-6:
        h.append("angle: adjacent toplamı degrees olmalı")
    if "rays" in fig or "labelKey" in fig or any(fig.get(a) is True for a in ("transversal", "construction", "protractor")):
        h.append("angle: adjacent ile rays/labelKey/transversal/construction/protractor yazılmaz (adlar angleKeys ile)")
    dolu = lambda v: isinstance(v, str) and bool(v.strip())
    n = len(parcalar)
    if "angleKeys" in fig:
        v = fig["angleKeys"]
        if not isinstance(v, dict) or not v or set(v) - {str(i) for i in range(1, n + 1)} or not all(dolu(x) for x in v.values()):
            h.append(f"angle: adjacent ile angleKeys {{sıra: anahtar}} olmalı; sıra 1..{n}, anahtar boş olmaz")
    isin = n if abs(sum(parcalar) - 360) < 1e-6 else n + 1
    if "rayKeys" in fig:
        v = fig["rayKeys"]
        if not isinstance(v, list) or len(v) != isin or not all(dolu(x) for x in v):
            h.append(f"angle: rayKeys ışın sayısı ({isin}) kadar boş olmayan anahtar olmalı")
    if "vertexKey" in fig and not dolu(fig["vertexKey"]):
        h.append("angle: vertexKey boş olmayan anahtar olmalı")
    return h


def shape_convex_at(points: list, index: int) -> bool:
    """Köşe dışbükey mi: iç açı 180°'den küçük ve köşe düz (≈180°) değil."""
    n = len(points)
    alan = sum(points[i][0] * points[(i + 1) % n][1] - points[(i + 1) % n][0] * points[i][1] for i in range(n))
    p, v, q = points[index - 1], points[index], points[(index + 1) % n]
    capraz = (v[0] - p[0]) * (q[1] - v[1]) - (v[1] - p[1]) * (q[0] - v[0])
    boy = (math.dist(p, v) * math.dist(v, q)) or 1.0
    return capraz * alan > 0 and abs(capraz) / boy > math.sin(math.radians(1))


def shape_height(points: list, frm: int, to: int) -> dict:
    """1.6 yükseklik: köşe `frm`'den kenar `to`'nun doğrusuna dikme (y yukarı birimde).

    foot dikme ayağı; t ayağın kenar üzerindeki konumu (0 = köşe to, 1 = köşe to+1).
    Ayak kenarın dışındaysa extension (yakın uç, ayak) kenarın kesik uzantısıdır.
    arm dik açı işaretinin kenar boyunca kolu: ayak içerideyse uzak uca, dışarıdaysa
    kenara doğru. Android `FigureMath.shapeHeight` aynası.
    """
    n = len(points)
    v, p, q = points[frm], points[to], points[(to + 1) % n]
    dx, dy = q[0] - p[0], q[1] - p[1]
    boy = math.hypot(dx, dy) or 1.0
    ux, uy = dx / boy, dy / boy
    t = ((v[0] - p[0]) * ux + (v[1] - p[1]) * uy) / boy
    foot = (p[0] + t * dx, p[1] + t * dy)
    if t < 0:
        extension, yon = (p, foot), 1
    elif t > 1:
        extension, yon = (q, foot), -1
    else:
        extension, yon = None, 1 if t < 0.5 else -1
    return {"foot": foot, "t": t, "extension": extension, "arm": (ux * yon, uy * yon)}


def shape_angle_mark(points: list, index: int, exterior: bool, half_w: float, half_h: float,
                     split: tuple | None = None) -> dict:
    """1.6 şekil açısı yerleşimi; points ekran yönünde (y aşağı), herhangi düzgün ölçekte.

    arms yayın iki kolu (birim): iç açıda köşeden önceki ve sonraki köşeye, dış açıda
    gelen kenarın uzantısı ve sonraki köşe. label yazı merkezinin köşeye göre px ötelemesi:
    kolların ortaortayında, yayın dışında ve kollara değmeden (ölçekten bağımsız). split
    (birim, ekran yönü) köşeden çıkan yükseklik gibi açıyı bölen bir çizgidir: yazı onun
    ayırdığı büyük parçanın ortaortayına geçer. Android `FigureMath.shapeAngleMark` aynası.
    """
    n = len(points)
    p, v, q = points[index - 1], points[index], points[(index + 1) % n]

    def birim(a, b):
        d = math.dist(a, b) or 1.0
        return (b[0] - a[0]) / d, (b[1] - a[1]) / d

    def aci(a, b):
        return math.acos(max(-1.0, min(1.0, a[0] * b[0] + a[1] * b[1])))

    first, second = (birim(p, v) if exterior else birim(v, p)), birim(v, q)
    sol, sag = first, second
    if split and abs(aci(first, split) + aci(split, second) - aci(first, second)) < 1e-6:
        sol, sag = (first, split) if aci(first, split) >= aci(split, second) else (split, second)
    bx, by = sol[0] + sag[0], sol[1] + sag[1]
    boy = math.hypot(bx, by) or 1.0
    yarim = aci(sol, sag) / 2
    rho = math.hypot(half_w, half_h)
    uzaklik = max(SEKIL_ACI_YAY + rho + 4, (rho + 4) / max(math.sin(yarim), 1e-3))
    return {"arms": (first, second), "label": (bx / boy * uzaklik, by / boy * uzaklik),
            "extension": first if exterior else None}


def angle_layout(degrees: float, rays: int, w: float, h: float, half_w: float, half_h: float) -> dict:
    """1.6 açı yerleşimi (Android `FigureMath.angleLayout` aynası). Köşe tuval ortasında,
    ilk ışın sağa; yay ışınların arasında. Ölçü yazısı yayın dışında ve ışınlara değmeden
    yazılır: rays=2'de açının ortaortayında, rays=3'te (açıortay) ilk yarının ortasında.
    Işınlar arasına sığmayan yazı ışın uçlarının ötesine geçer; tuvale sığmazsa ışınlar kısalır."""
    a = math.radians(degrees)
    direction = a / 4 if rays == 3 else a / 2
    clearance = direction  # yazının iki yanındaki ışına açısal uzaklık
    rho = math.hypot(half_w, half_h)
    radius = max(24.0, min(w, h) / 2 - 24)
    cx, cy = w / 2, h / 2
    while True:
        arc = min(42.0, radius * 0.55)
        distance = arc + rho + 4
        if clearance < math.pi / 2:
            # Işınlardan (ρ + 4) uzak kalacak kadar dışarı; ışın uçlarının ötesi her zaman boştur.
            distance = max(distance, min((rho + 4) / math.sin(clearance), radius + rho + 8))
        x, y = cx + distance * math.cos(direction), cy - distance * math.sin(direction)
        fits = half_w + 4 <= x <= w - half_w - 4 and half_h + 4 <= y <= h - half_h - 4
        if fits or radius <= 24:
            break
        radius = max(24.0, radius * 0.9)
    # Sığmayan çok dar açıda yazı tuvalin içine çekilir (yazı küçültülmez).
    x = min(max(x, half_w + 4), w - half_w - 4)
    y = min(max(y, half_h + 4), h - half_h - 4)
    angles = [0.0, a] + ([a / 2] if rays == 3 else [])
    return {"centre": (cx, cy), "radius": radius, "arc": arc, "inner": arc * 0.6 if rays == 3 else None,
            "rays": angles, "label": (x, y)}


def protractor_layout(degrees: float, w: float, h: float, half_w: float, half_h: float,
                      label_gap: float = 30.0) -> dict:
    """1.6 iletki (ekran, y aşağı): köşe tabanın ortasında, ilk ışın 0 çizgisinde (sağ), ölçek saat
    yönünün tersine 0..180. Çentikler 10° uzun (12), 5° orta (8), yarıçap ≥ 200,5 ise 1° kısa (5);
    sayılar R - 22'de (0/180 tabanın 10 px üstünde), aralıkları en az label_gap olacak biçimde 10/20/30 derecede bir. Işınlar R + 16
    uzunluğunda; adı verilen ölçü yazısı açının ortaortayında, iletkinin boş iç bölgesinde (en çok .6R)."""
    radius = max(60.0, min((w - 72) / 2, h - 56))
    cx, cy = w / 2, min(h - 20, max(36 + radius, (h + radius + 6) / 2))
    ticks = []
    for derece in range(181):
        if derece % 10 == 0:
            boy, tur = 12.0, 10
        elif derece % 5 == 0:
            boy, tur = 8.0, 5
        elif radius * math.radians(1) >= 3.5:
            boy, tur = 5.0, 1
        else:
            continue
        a = math.radians(derece)
        ticks.append({"degrees": derece, "kind": tur,
                      "outer": (cx + radius * math.cos(a), cy - radius * math.sin(a)),
                      "inner": (cx + (radius - boy) * math.cos(a), cy - (radius - boy) * math.sin(a))})
    adim = next((s for s in (10, 20, 30) if (radius - 22) * math.radians(s) >= label_gap), 30)
    labels = [(derece, (cx + (radius - 22) * math.cos(math.radians(derece)),
                        min(cy - 10, cy - (radius - 22) * math.sin(math.radians(derece)))))
              for derece in range(0, 181, adim)]
    a = math.radians(degrees)
    arc = min(28.0, .2 * radius)
    rho = math.hypot(half_w, half_h)
    yarim = a / 2
    uzaklik = arc + rho + 4
    if yarim < math.pi / 2:
        uzaklik = max(uzaklik, (rho + 4) / math.sin(yarim))
    uzaklik = min(uzaklik, .6 * radius)
    x = min(max(cx + uzaklik * math.cos(yarim), half_w + 4), w - half_w - 4)
    y = min(max(cy - uzaklik * math.sin(yarim), half_h + 4), cy - half_h - 4)
    return {"centre": (cx, cy), "radius": radius, "ticks": ticks, "labels": labels, "rays": [0.0, a],
            "rayLength": radius + 16, "arc": arc, "label": (x, y)}


def adjacent_layout(adjacent: list, w: float, h: float, size) -> dict:
    """1.6 komşu açılar (ekran, y aşağı; Android `FigureMath.adjacentLayout` aynası).

    İlk ışın sağa; açılar saat yönünün tersine yan yana. Toplam 360 ise son ışın ilkine düşer
    (ters açılar, bir nokta etrafındaki açılar). size(item) -> (yarı genişlik, yarı yükseklik) ya da
    None (yazı yok); item ("angle", 1..n), ("ray", sıra), ("vertex",). Yaylar sırayla KOMSU_YAY
    biçimlerinde (yan yana iki yay karışmasın), 90°'de kare. Açı adı kendi ortaortayında, yaydan ve ışınlardan
    uzakta; ışın adı ucun ötesinde; köşe adı en geniş boşlukta (açının içindeyse o açının yayı dışarı
    alınır). Işın boyu her şey tuvale sığacak en büyük değer (40..220), şekil tuvalde ortalanır.
    """
    n = len(adjacent)
    sinir = [0.0]
    for parca in adjacent:
        sinir.append(sinir[-1] + float(parca))
    tam = abs(sinir[-1] - 360) < 1e-6
    isinlar = sinir[:-1] if tam else sinir
    bicim = [2 if tam and n % 2 and i == n - 1 and n > 1 else i % 2 for i in range(n)]
    yay = [KOMSU_YAY[b][0] for b in bicim]
    sabit = []  # (öğe, ox, oy, yarı genişlik, yarı yükseklik): köşeye göre sabit ötelemeli yazılar
    tepe = size(("vertex",))
    if tepe:
        hw, hh = tepe
        rho = math.hypot(hw, hh)
        bosluk = [(sinir[i], float(adjacent[i]), i) for i in range(n)]
        if not tam:
            bosluk.append((sinir[-1], 360 - sinir[-1], None))
        bas, aciklik, icinde = max(bosluk, key=lambda b: (b[1], b[2] is None))
        yarim = math.radians(aciklik / 2)
        d = rho + 6 if yarim >= math.pi / 2 else max(rho + 6, (rho + 4) / math.sin(yarim))
        if icinde is not None:
            yay[icinde] = max(yay[icinde], d + rho + 6)
        orta = math.radians(bas + aciklik / 2)
        sabit.append((("vertex",), d * math.cos(orta), -d * math.sin(orta), hw, hh))
    for i, parca in enumerate(adjacent):
        hw, hh = size(("angle", i + 1))
        rho = math.hypot(hw, hh)
        yarim = math.radians(parca / 2)
        d = yay[i] + rho + 4
        if yarim < math.pi / 2:
            d = max(d, (rho + 4) / math.sin(yarim))
        orta = math.radians(sinir[i] + parca / 2)
        sabit.append((("angle", i + 1), d * math.cos(orta), -d * math.sin(orta), hw, hh))
    uclar = []
    for j, a in enumerate(isinlar):
        boyut = size(("ray", j))
        uclar.append((math.cos(math.radians(a)), -math.sin(math.radians(a)), boyut))

    def kutu(r):
        xs, ys = [0.0], [0.0]
        for _, ox, oy, hw, hh in sabit:
            xs += [ox - hw, ox + hw]; ys += [oy - hh, oy + hh]
        for ux, uy, boyut in uclar:
            xs.append(r * ux); ys.append(r * uy)
            if boyut:
                hw, hh = boyut
                e = r + math.hypot(hw, hh) + 6
                xs += [e * ux - hw, e * ux + hw]; ys += [e * uy - hh, e * uy + hh]
        return min(xs), min(ys), max(xs), max(ys)

    kenar = 8.0
    alt, ust = 40.0, 220.0
    for _ in range(40):
        orta_r = (alt + ust) / 2
        x0, y0, x1, y1 = kutu(orta_r)
        if x1 - x0 <= w - 2 * kenar and y1 - y0 <= h - 2 * kenar:
            alt = orta_r
        else:
            ust = orta_r
    r = alt
    x0, y0, x1, y1 = kutu(r)
    cx, cy = w / 2 - (x0 + x1) / 2, h / 2 - (y0 + y1) / 2
    etiketler = [(item, (cx + ox, cy + oy)) for item, ox, oy, _, _ in sabit]
    for j, (ux, uy, boyut) in enumerate(uclar):
        if boyut:
            e = r + math.hypot(*boyut) + 6
            etiketler.append((("ray", j), (cx + e * ux, cy + e * uy)))
    yaylar = [(sinir[i], float(adjacent[i]), yay[i], abs(adjacent[i] - 90) < 0.5, KOMSU_YAY[bicim[i]][1])
              for i in range(n)]
    return {"centre": (cx, cy), "radius": r, "rays": isinlar, "arcs": yaylar, "labels": etiketler}


KESEN_ACI = (30, 150)  # 1.6 transversal: kesenin paralellerle yaptığı açı (derece) aralığı
KESEN_YAY = 22.0


def transversal_angles(fig: dict) -> dict:
    """Adı yazılacak açılar {sıra 1..8: anahtar ya da None}; angleKeys yoksa 1. açıya ölçü yazılır."""
    keys = fig.get("angleKeys")
    if isinstance(keys, dict) and keys:
        return {int(k): keys[k] for k in sorted(keys, key=int)}
    return {1: None}


def _kutu_ust_uste(a: tuple, b: tuple, pay: float = 2.0) -> bool:
    return a[0] - pay < b[2] and b[0] - pay < a[2] and a[1] - pay < b[3] and b[1] - pay < a[3]


def transversal_layout(fig: dict, w: float, h: float, size) -> dict:
    """1.6 paralel iki doğru ve kesen (Android `FigureMath.transversalLayout` aynası).

    Paraleller yataydır (doğru 0 üstte, 1 altta); kesen (doğru 2) onları sağa doğru `degrees`
    açıyla keser. Açı sırası üst kesişimde 1 sağ üst, 2 sol üst, 3 sol alt, 4 sağ alt; alt
    kesişimde aynı sırayla 5..8. size(item) -> (yarı genişlik, yarı yükseklik); item
    ("angle", sıra) ya da ("line", sıra). Açı adı kolların ortaortayında yaydan ve kollardan
    uzakta; paralel adları kesenin üst ucunun karşı yanındaki uçta çizginin üstünde, paralellik
    oku ad ile kesişimdeki ilk yazı/yay arasının ortasında; kesenin adı üst ucunun yanında.
    Sığmazsa paraleller yaklaşır, yazı küçülmez.
    """
    t = math.radians(float(fig["degrees"]))
    names = transversal_angles(fig)
    line_keys = {int(k): v for k, v in (fig.get("lineKeys") or {}).items()}
    kenar = 8.0
    baslangic = [0.0, t, math.pi, math.pi + t]
    aciklik = [t, math.pi - t, t, math.pi - t]
    ofset = {}
    for k in names:
        i = (k - 1) % 4
        hw, hh = size(("angle", k))
        rho = math.hypot(hw, hh)
        yarim = aciklik[i] / 2
        d = max(KESEN_YAY + rho + 4, (rho + 4) / math.sin(yarim))
        orta = baslangic[i] + yarim
        ofset[k] = (d * math.cos(orta), -d * math.sin(orta), hw, hh)
    ad = {i: size(("line", i)) for i in line_keys}
    ust = max([KESEN_YAY + 14] + [hh + 4 - oy for k, (ox, oy, hw, hh) in ofset.items() if k in (1, 2)]
              + ([2 * ad[0][1] + 6] if 0 in ad else []))
    alt = max([KESEN_YAY + 14] + [oy + hh + 4 for k, (ox, oy, hw, hh) in ofset.items() if k in (7, 8)])
    g_min = max([2 * KESEN_YAY + 8] + [oy + hh + 4 for k, (ox, oy, hw, hh) in ofset.items() if k in (3, 4)]
                + [hh + 4 - oy for k, (ox, oy, hw, hh) in ofset.items() if k in (5, 6)]
                + ([2 * ad[1][1] + 6] if 1 in ad else []))
    g = max(g_min, min(h - ust - alt - 2 * kenar, 170.0))
    sol_ad = math.cos(t) >= -1e-9  # kesenin üst ucu sağa yatıksa adlar sol uçta
    while True:
        y0 = kenar + ust + (h - 2 * kenar - ust - alt - g) / 2
        y1 = y0 + g
        dx = g * math.cos(t) / math.sin(t)
        goreli = []
        for k, (ox, oy, hw, hh) in ofset.items():
            vx = dx / 2 if k <= 4 else -dx / 2
            goreli += [vx + ox - hw, vx + ox + hw]
        goreli += [dx / 2 - KESEN_YAY, dx / 2 + KESEN_YAY, -dx / 2 - KESEN_YAY, -dx / 2 + KESEN_YAY]
        xc = w / 2 - (min(goreli) + max(goreli)) / 2
        tepe, dip = (xc + dx / 2, y0), (xc - dx / 2, y1)
        yon = (math.cos(t), -math.sin(t))

        def uc(nokta, isaret):
            sx, sy = yon[0] * isaret, yon[1] * isaret
            s = min(((kenar / 2 - nokta[1]) / sy) if sy < -1e-9 else ((h - kenar / 2 - nokta[1]) / sy),
                    ((w - kenar / 2 - nokta[0]) / sx) if sx > 1e-9 else ((kenar / 2 - nokta[0]) / sx) if sx < -1e-9 else math.inf)
            return nokta[0] + sx * s, nokta[1] + sy * s

        ust_uc, alt_uc = uc(tepe, 1), uc(dip, -1)
        etiketler, kutular, oklar_kutu = [], [], []
        for k, (ox, oy, hw, hh) in ofset.items():
            v = tepe if k <= 4 else dip
            x, y = v[0] + ox, v[1] + oy
            etiketler.append((("angle", k), (x, y)))
            kutular.append((x - hw, y - hh, x + hw, y + hh))
        aci_kutulari = dict(zip(ofset, kutular))
        oklar = []
        for i, y in ((0, y0), (1, y1)):
            # Paralellik oku adın (ya da çizgi ucunun oku) ile kesişim tarafındaki ilk yazı/yay arasının ortasında.
            v = tepe if i == 0 else dip
            yakin = [b for k, b in aci_kutulari.items() if (k <= 4) == (i == 0)]
            if sol_ad:
                bas = kenar + 14
                son = min([v[0] - KESEN_YAY] + [b[0] for b in yakin if b[2] <= v[0]]) - 6
            else:
                bas = w - kenar - 14
                son = max([v[0] + KESEN_YAY] + [b[2] for b in yakin if b[0] >= v[0]]) + 6
            if i in ad:
                hw, hh = ad[i]
                x = kenar + hw if sol_ad else w - kenar - hw
                etiketler.append((("line", i), (x, y - hh - 4)))
                kutular.append((x - hw, y - 2 * hh - 4, x + hw, y - 4))
                bas = x + hw + 8 if sol_ad else x - hw - 8
            ok_x = (bas + son) / 2 if abs(son - bas) > 14 else bas + (7 if sol_ad else -7)
            oklar.append((ok_x, y))
            oklar_kutu.append((ok_x - 6, y - 7, ok_x + 6, y + 7))
        if 2 in ad:
            hw, hh = ad[2]
            x = min(max(ust_uc[0] + hw + 8, hw + 2), w - hw - 2)
            y = min(max(ust_uc[1] + hh + 2, hh + 2), h - hh - 2)
            if abs((x - tepe[0]) * yon[1] - (y - tepe[1]) * yon[0]) < math.hypot(hw, hh) + 2:
                x = min(max(ust_uc[0] - hw - 8, hw + 2), w - hw - 2)
            etiketler.append((("line", 2), (x, y)))
            kutular.append((x - hw, y - hh, x + hw, y + hh))
        hepsi = kutular + oklar_kutu
        sigar = all(0 <= b[0] and b[2] <= w and 0 <= b[1] and b[3] <= h for b in hepsi)
        sigar = sigar and not any(_kutu_ust_uste(a, b) for i, a in enumerate(hepsi) for b in hepsi[i + 1:])
        # Ad kutusu kesene değmemeli (açı adları kesenden yapı gereği uzaktır).
        for (item, (x, y)), b in zip(etiketler, kutular):
            if item[0] == "line" and item[1] < 2:
                rho = math.hypot((b[2] - b[0]) / 2, (b[3] - b[1]) / 2)
                sigar = sigar and abs((x - tepe[0]) * yon[1] - (y - tepe[1]) * yon[0]) > rho + 2
        if sigar or g <= g_min:
            break
        g = max(g_min, g * 0.92)
    yaylar = []
    for k in names:
        i = (k - 1) % 4
        yaylar.append((0 if k <= 4 else 1, math.degrees(baslangic[i]), math.degrees(aciklik[i]),
                       abs(math.degrees(aciklik[i]) - 90) < 0.5))
    return {"lines": [((kenar / 2, y0), (w - kenar / 2, y0)), ((kenar / 2, y1), (w - kenar / 2, y1)), (ust_uc, alt_uc)],
            "vertices": [tepe, dip], "arcs": yaylar, "chevrons": oklar, "labels": etiketler}


def angle_construction(lay: dict, degrees: float, half_w: float, half_h: float, w: float, h: float) -> dict:
    """1.6 açıortay pergel izi (rays=3, construction=true). Köşe merkezli r1 yayı iki ışını
    P (0°) ve Q (degrees) noktasında keser; P ve Q merkezli r2 yayları açıortay üstünde R'de
    (köşeden d uzakta) kesişir. Üç yay da ölçü yazısına değmez, R yazıdan uzak durur. R ışın
    boyuna sığmazsa yalnız açıortay ışını tuval içinde uzatılır (bisector). Android
    `FigureMath.angleConstruction` aynası."""
    a = math.radians(degrees)
    (cx, cy), radius, arc = lay["centre"], lay["radius"], lay["arc"]
    lx, ly = lay["label"]
    rho = math.hypot(half_w, half_h)
    uzak = math.hypot(lx - cx, ly - cy)
    ux, uy = math.cos(a / 2), -math.sin(a / 2)
    # Açıortay ışınının tuvalde (ok ucu payıyla) en çok uzayabileceği boy.
    sinir = min((w - 8 - cx) / ux if ux > 1e-9 else (cx - 8) / -ux if ux < -1e-9 else math.inf,
                (cy - 8) / -uy if uy < -1e-9 else math.inf)

    def yazida(x: float, y: float) -> bool:
        return abs(x - lx) < half_w + 3 and abs(y - ly) < half_h + 3

    def yay_carpar(ox: float, oy: float, r: float, bas: float, son: float) -> bool:
        return any(yazida(ox + r * math.cos(bas + (son - bas) * k / 60), oy - r * math.sin(bas + (son - bas) * k / 60))
                   for k in range(61))

    adaylar = [arc + 12, uzak - rho - 8, uzak + rho + 8, radius * 0.45, radius * 0.6, radius * 0.3]
    secim = None
    for uzun in (radius, sinir):
        for r1 in adaylar:
            if r1 < (lay["inner"] or arc) + 8:
                continue
            # R köşeden 1,6·r1 uzakta: yaylar ölçü yayından ve birbirinden ayrık kalır (180°'de de).
            d = 1.6 * r1
            r2 = math.hypot(d - r1 * math.cos(a / 2), r1 * math.sin(a / 2))
            rx, ry = cx + d * ux, cy + d * uy
            boy = max(radius, d + 24)
            # Çizilen üç yay: köşede -8°..a+8°, P ve Q'da R yönünün ±14°'si; uzayan ışın da yazıya değmez.
            carpar = yay_carpar(cx, cy, r1, -math.radians(8), a + math.radians(8))
            for taban in (0.0, a):
                px, py = cx + r1 * math.cos(taban), cy - r1 * math.sin(taban)
                yon = math.atan2(py - ry, rx - px)
                carpar = carpar or yay_carpar(px, py, r2, yon - math.radians(14), yon + math.radians(14))
            carpar = carpar or any(yazida(cx + (radius + (boy - radius) * k / 40) * ux, cy + (radius + (boy - radius) * k / 40) * uy)
                                   for k in range(41))
            aday = {"r1": r1, "r2": r2, "d": d, "bisector": boy}
            if d + 24 <= uzun and not carpar and math.hypot(rx - lx, ry - ly) > rho + 12:
                return aday
            secim = secim or aday
    return secim


def circuit_parts(fig: dict) -> list[dict]:
    """1.6 devre elemanlarının tek okuması: dize (eski biçim) ya da
    {"type","labelKey"?,"state"?,"branch"?,"across"?}. labelKey yazılmazsa
    labelKeys[type] kullanılır. Çiziciler ve doğrulayıcı aynı okumayı kullanır;
    Android FigureMath.circuitParts aynası."""
    keys = fig.get("labelKeys") if isinstance(fig.get("labelKeys"), dict) else {}
    parts = []
    for i, e in enumerate(fig.get("elements") or []):
        item = e if isinstance(e, dict) else {"type": e}
        kind = item.get("type")
        parts.append({
            "index": i,
            "type": kind,
            "labelKey": item.get("labelKey") or (keys.get(kind) if isinstance(kind, str) else None),
            "state": item.get("state", "open"),
            "branch": item.get("branch"),
            "across": item.get("across"),
        })
    return parts


def circuit_parallel_groups(parts: list[dict]) -> tuple[list[dict], list[list[dict]]]:
    """Paralel devrede ana hat ve kollar. branch yazılmışsa yazılmayanlar ana hattadır;
    eski biçimde pil ana hatta, her alıcı kendi kolundadır. Tel çizilmez.
    Android FigureMath.circuitParallelGroups aynası."""
    devices = [p for p in parts if p["type"] != "wire"]
    if any(p["branch"] is not None for p in devices):
        count = max(p["branch"] for p in devices if p["branch"] is not None) + 1
        return ([p for p in devices if p["branch"] is None],
                [[p for p in devices if p["branch"] == b] for b in range(count)])
    return ([p for p in devices if p["type"] == "battery"],
            [[p] for p in devices if p["type"] != "battery"])


def _devre_hatalari(fig: dict) -> list[str]:
    """1.6 devre elemanı nesneleri: anahtar durumu, paralel kollar, voltmetre köprüsü."""
    h: list[str] = []
    elemanlar = fig["elements"]
    paralel = fig.get("layout") == "parallel"
    tam = lambda v: isinstance(v, int) and not isinstance(v, bool)
    for i, e in enumerate(elemanlar):
        if isinstance(e, str):
            if e not in CIRCUIT_ELEM:
                h.append(f"circuit: eleman beyaz liste dışı: {e!r}")
            continue
        if not (isinstance(e, dict) and set(e) <= CIRCUIT_ALAN and e.get("type") in CIRCUIT_ELEM):
            h.append(f"circuit: elements[{i}] dize ya da {{'type','labelKey'?,'state'?,'branch'?,'across'?}} değil: {e!r}")
            continue
        if "labelKey" in e and not (isinstance(e["labelKey"], str) and e["labelKey"].strip()):
            h.append(f"circuit: elements[{i}].labelKey boş")
        if "state" in e and (e["type"] != "switch" or e["state"] not in CIRCUIT_ANAHTAR):
            h.append(f"circuit: elements[{i}].state yalnız switch için open|closed")
        if "branch" in e and (
            not paralel or e["type"] in ("battery", "wire") or not tam(e["branch"])
            or not 0 <= e["branch"] < CIRCUIT_KOL_EN_COK
        ):
            h.append(f"circuit: elements[{i}].branch yalnız parallel düzende pil/tel dışı elemana 0..{CIRCUIT_KOL_EN_COK - 1}")
        if "across" in e:
            hedef = e["across"]
            hedef_tur = None
            if tam(hedef) and 0 <= hedef < len(elemanlar) and hedef != i:
                o = elemanlar[hedef]
                hedef_tur = o.get("type") if isinstance(o, dict) else o
            if paralel or e["type"] != "voltmeter" or hedef_tur in (None, "voltmeter", "wire"):
                h.append(f"circuit: elements[{i}].across yalnız seri düzende voltmetreye, ölçülen elemanın sırası")
    if h:
        return h
    parts = circuit_parts(fig)
    if paralel:
        ana, kollar = circuit_parallel_groups(parts)
        if any(p["branch"] is not None for p in parts):
            if len(kollar) < 2 or any(not kol for kol in kollar):
                h.append("circuit: branch numaraları 0'dan ardışık ve en az iki kol olmalı")
            elif len(ana) > CIRCUIT_KOL_ELEMAN_EN_COK or any(len(kol) > CIRCUIT_KOL_ELEMAN_EN_COK for kol in kollar):
                h.append(f"circuit: ana hatta ve her kolda en çok {CIRCUIT_KOL_ELEMAN_EN_COK} eleman")
    else:
        hedefler = [p["across"] for p in parts if p["across"] is not None]
        if len(hedefler) != len(set(hedefler)):
            h.append("circuit: bir elemana tek voltmetre bağlanır")
    return h


def _akis_semasi_hatalari(fig: dict) -> list[str]:
    """1.6 algoritma akış şeması: bir düğüm shape taşıyınca (yazılmayan process sayılır)."""
    h: list[str] = []
    sekil = {n["id"]: n.get("shape", "process") for n in fig["nodes"]}
    if len(sekil) != len(fig["nodes"]):
        h.append("flow: shape'li akışta node id'leri benzersiz olmalı")
    if fig.get("direction") not in (None, "horizontal", "vertical", "down", "right"):
        h.append("flow: shape'li akışta direction horizontal|vertical olur")
    cikis: dict = {i: [] for i in sekil}
    giris: dict = {i: 0 for i in sekil}
    for e in fig["edges"]:
        if e["from"] == e["to"]:
            h.append(f"flow: shape'li akışta düğüm kendine bağlanamaz: {e!r}")
        cikis[e["from"]].append(e)
        giris[e["to"]] += 1
    for i, tur in sekil.items():
        if tur == "decision":
            if len(cikis[i]) < 2 or any(not e.get("labelKey") for e in cikis[i]):
                h.append(f"flow: decision {i!r} en az iki etiketli çıkış (ör. Evet/Hayır) ister")
        elif len(cikis[i]) > 1:
            h.append(f"flow: {tur} {i!r} en çok bir çıkış alır; dallanma decision ile yapılır")
        if tur == "terminal" and giris[i] and cikis[i]:
            h.append(f"flow: terminal {i!r} ya başla (girişsiz) ya bitir (çıkışsız) olmalı")
    return h


# 1.6 hazır cisimler (shape.type): eğik izdüşüm, gizli kenar kesik çizgi.
KATI_TURLER = ("cuboid", "prism", "pyramid", "cylinder", "cone", "cubes")
KATI_OLCU = {
    "cuboid": ("w", "h", "d"), "prism": ("a", "h"), "pyramid": ("a", "h"),
    "cylinder": ("r", "h"), "cone": ("r", "h"), "cubes": (),
}
KATI_TABAN = (3, 8)  # prism/pyramid sides
KATI_KUP_EN_COK = 40
KATI_KUP_SINIR = 8  # birim küp konumu 0..7
KATI_KUP_BIRIM = 4  # küp yapısında birim en çok çizim alanının 1/4'ü: şıklardaki görünümler aynı ölçekte
KATI_ORAN_EN_COK = 8.0  # çizilen ölçülerin en büyüğü / en küçüğü
# Derinlik ekseni yarım ölçekte, 40° yukarı sağa (eğik/kabine izdüşüm).
KATI_DERINLIK = (0.5 * math.cos(math.radians(40)), 0.5 * math.sin(math.radians(40)))
KATI_ELIPS = 0.3  # silindir/koni tabanı: yatay yarıçapın bu katı dikey yarı eksen
KATI_GORUNUM = ("front", "top", "right", "left")  # 1.6 birim küp yapısının dik görünümü
KATI_IZDUSUM = ("oblique", "isometric")  # 1.6 birim küp yapısının çizim biçimi
KATI_IZO = math.cos(math.radians(30))  # izometrik: x sağa aşağı, z sağa yukarı 30°, kenarlar birim
_KATI_ELIPS_ADIM = 48


def solid_dims(fig: dict) -> dict:
    """Cismin çizilen ölçüleri. Eksik ölçü verilenden şematik tamamlanır
    (kutuda küp, prizma/piramitte h = 1,5a, silindir/konide h = 2r)."""
    tur, dims = fig.get("type"), fig.get("dims") or {}
    if tur == "cuboid":
        yedek = max((float(dims[k]) for k in ("w", "h", "d") if k in dims), default=1.0)
        return {k: float(dims.get(k, yedek)) for k in ("w", "h", "d")}
    if tur in ("prism", "pyramid"):
        a = float(dims["a"]) if "a" in dims else (float(dims["h"]) / 1.5 if "h" in dims else 1.0)
        return {"a": a, "h": float(dims.get("h", 1.5 * a))}
    if tur in ("cylinder", "cone"):
        r = float(dims["r"]) if "r" in dims else (float(dims["h"]) / 2 if "h" in dims else 1.0)
        return {"r": r, "h": float(dims.get("h", 2 * r))}
    return {}


def _taban(n: int, a: float) -> list:
    """Tabanı önde yatay kenarlı düzgün n-gen (x, z); kenar 0 → 1 en öndedir."""
    r = a / (2 * math.sin(math.pi / n))
    return [(r * math.cos(t), r * math.sin(t))
            for t in (-math.pi / 2 - math.pi / n + 2 * math.pi * k / n for k in range(n))]


def _cokyuzlu(koseler: list, yuzler: list) -> tuple:
    """Dışbükey çokyüzlü: görünen yüzler (izdüşüm, dolgu) ve kenarlar (izdüşüm, gizli mi)."""
    c, s = KATI_DERINLIK
    iz = [(x + c * z, y + s * z) for x, y, z in koseler]
    merkez = [sum(p[i] for p in koseler) / len(koseler) for i in range(3)]
    gorunur, ust = [], []
    for yuz in yuzler:
        p0, p1, p2 = (koseler[i] for i in yuz[:3])
        u = [p1[i] - p0[i] for i in range(3)]
        v = [p2[i] - p0[i] for i in range(3)]
        n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
        orta = [sum(koseler[i][k] for i in yuz) / len(yuz) for k in range(3)]
        if sum(n[k] * (orta[k] - merkez[k]) for k in range(3)) < 0:
            n = [-q for q in n]
        boy = math.sqrt(sum(q * q for q in n)) or 1
        # Bakış yönü (c, s, -1): ön, üst ve sağ yüzler görünür.
        gorunur.append(n[0] * c + n[1] * s - n[2] > 1e-9)
        ust.append(n[1] / boy > 0.7)
    yuz_cizim = [([iz[i] for i in yuz], "paper" if ust[k] else "surface")
                 for k, yuz in enumerate(yuzler) if gorunur[k]]
    kenarlar: dict = {}
    for k, yuz in enumerate(yuzler):
        for i in range(len(yuz)):
            anahtar = tuple(sorted((yuz[i], yuz[(i + 1) % len(yuz)])))
            kenarlar.setdefault(anahtar, []).append(gorunur[k])
    cizgi = [([iz[a], iz[b]], not any(g)) for (a, b), g in kenarlar.items()]
    return iz, yuz_cizim, cizgi


def _elips(r: float, y0: float, bas: float, son: float) -> list:
    adim = max(2, round(_KATI_ELIPS_ADIM * (son - bas) / (2 * math.pi)))
    return [(r * math.cos(t), y0 + KATI_ELIPS * r * math.sin(t))
            for t in (bas + (son - bas) * i / adim for i in range(adim + 1))]


def _kenarda_cokgen(p: tuple, q: tuple, n: int) -> list:
    """p→q kenarının solunda (y yukarı) duran düzgün n-gen; köşeler p, q'dan başlayarak sırayla."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    t = 2 * math.pi / n
    pts = [p, q]
    for _ in range(n - 2):
        dx, dy = dx * math.cos(t) - dy * math.sin(t), dx * math.sin(t) + dy * math.cos(t)
        pts.append((pts[-1][0] + dx, pts[-1][1] + dy))
    return pts


def _cember_noktalari(cx: float, cy: float, r: float) -> list:
    return [(cx + r * math.cos(2 * math.pi * k / _KATI_ELIPS_ADIM), cy + r * math.sin(2 * math.pi * k / _KATI_ELIPS_ADIM))
            for k in range(_KATI_ELIPS_ADIM)]


def solid_net(tur: str, olcu: dict, adli: set) -> dict:
    """1.6 cisim açınımı (net=true), birim uzunlukta ve y yukarı; solid_drawing ile aynı biçim.
    Yan yüzler surface, tabanlar paper dolgulu; ölçü adı açınımın dış kenarında, piramit
    taban kenarı adı tabanın içinde. Piramit/koni yüksekliği açınımda görünmez, adlanmaz.
    Android FigureMath.solidNet aynası."""
    yuzler: list = []
    cizgiler: list = []
    adlar: list = []
    dikdortgen = lambda x0, y0, x1, y1: [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    if tur == "cuboid":
        # Haç açınım: sol, ön, sağ, arka yan yana; üst ve alt ön yüze bağlı.
        w, h, d = olcu["w"], olcu["h"], olcu["d"]
        for x0, x1 in ((0, d), (d, d + w), (d + w, 2 * d + w), (2 * d + w, 2 * d + 2 * w)):
            yuzler.append((dikdortgen(x0, 0.0, x1, h), "surface"))
        yuzler.append((dikdortgen(d, h, d + w, h + d), "paper"))
        yuzler.append((dikdortgen(d, -d, d + w, 0.0), "paper"))
        yerler = {"w": ((d + w / 2, -d), (0.0, -1.0)), "h": ((0.0, h / 2), (-1.0, 0.0)), "d": ((d / 2, 0.0), (0.0, -1.0))}
        adlar = [(k, *yerler[k]) for k in ("w", "h", "d") if k in adli]
    elif tur == "prism":
        # Yan dikdörtgenler yan yana; iki taban ortadaki dikdörtgenin üst ve alt kenarına bağlı.
        n, a, h = olcu["n"], olcu["a"], olcu["h"]
        for k in range(n):
            yuzler.append((dikdortgen(k * a, 0.0, (k + 1) * a, h), "surface"))
        m = n // 2
        yuzler.append((_kenarda_cokgen((m * a, h), ((m + 1) * a, h), n), "paper"))
        yuzler.append((_kenarda_cokgen(((m + 1) * a, 0.0), (m * a, 0.0), n), "paper"))
        yerler = {"a": ((a / 2, 0.0), (0.0, -1.0)), "h": ((0.0, h / 2), (-1.0, 0.0))}
        adlar = [(k, *yerler[k]) for k in ("a", "h") if k in adli]
    elif tur == "pyramid":
        # Taban ortada; her kenara yan yüz yüksekliği kadar dışa açılan üçgen.
        n, a, h = olcu["n"], olcu["a"], olcu["h"]
        taban = _taban(n, a)
        yan = math.hypot(h, a / (2 * math.tan(math.pi / n)))
        yuzler.append((taban, "paper"))
        for k in range(n):
            (x1, y1), (x2, y2) = taban[k], taban[(k + 1) % n]
            boy = math.hypot(x2 - x1, y2 - y1) or 1
            tepe = ((x1 + x2) / 2 + (y2 - y1) / boy * yan, (y1 + y2) / 2 - (x2 - x1) / boy * yan)
            yuzler.append(([(x1, y1), (x2, y2), tepe], "surface"))
        if "a" in adli:
            adlar.append(("a", ((taban[0][0] + taban[1][0]) / 2, taban[0][1]), (0.0, 1.0)))
    elif tur == "cylinder":
        # Yanal yüz 2πr × h dikdörtgen; tabanlar ortada üstte ve altta.
        r, h = olcu["r"], olcu["h"]
        yuzler.append((dikdortgen(0.0, 0.0, 2 * math.pi * r, h), "surface"))
        yuzler.append((_cember_noktalari(math.pi * r, h + r, r), "paper"))
        yuzler.append((_cember_noktalari(math.pi * r, -r, r), "paper"))
        if "r" in adli:
            cizgiler.append(([(math.pi * r, h + r), (math.pi * r + r, h + r)], False))
            adlar.append(("r", (math.pi * r + r, h + r), (1.0, 0.0)))
        if "h" in adli:
            adlar.append(("h", (0.0, h / 2), (-1.0, 0.0)))
    elif tur == "cone":
        # Yanal yüz ana doğru l yarıçaplı, 360·r/l derecelik daire dilimi; taban yayın ortasına değer.
        r, h = olcu["r"], olcu["h"]
        l = math.hypot(r, h)
        aci = 2 * math.pi * r / l
        adim = max(2, round(_KATI_ELIPS_ADIM * aci / (2 * math.pi)))
        yay = [(l * math.cos(-math.pi / 2 - aci / 2 + aci * i / adim), l * math.sin(-math.pi / 2 - aci / 2 + aci * i / adim))
               for i in range(adim + 1)]
        yuzler.append(([(0.0, 0.0), *yay], "surface"))
        yuzler.append((_cember_noktalari(0.0, -l - r, r), "paper"))
        if "r" in adli:
            cizgiler.append(([(0.0, -l - r), (r, -l - r)], False))
            adlar.append(("r", (r, -l - r), (1.0, 0.0)))
    return {"faces": yuzler, "lines": cizgiler, "labels": adlar}


def solid_drawing(fig: dict) -> dict:
    """1.6 cisim çizimi, birim uzunlukta ve y yukarı:
    faces [(noktalar, dolgu)] çizim sırasıyla, lines [(noktalar, kesik mi)],
    labels [(ölçü adı, çapa, dış yön)]. Yalnız dims ya da sideLabels'ta yazılan
    ölçü adlanır. Android FigureMath.solidDrawing aynası."""
    tur = fig.get("type")
    adli = set(fig.get("dims") or {}) | set(fig.get("sideLabels") or {})
    olcu = solid_dims(fig)
    if fig.get("net") is True and tur != "cubes":
        olcu["n"] = int(fig.get("sides", 3 if tur == "prism" else 4))
        return solid_net(tur, olcu, adli)
    c, s = KATI_DERINLIK
    yuzler: list = []
    cizgiler: list = []
    adlar: list = []
    orta = lambda p, q: ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    if tur == "cubes":
        kupler = {tuple(k) for k in fig.get("cubes") or []}
        gorunum = fig.get("view")
        if gorunum in KATI_GORUNUM:
            # 1.6 dik görünüm: o yönden görülen birim kareler; derinlik birleşir. Sağdan bakınca
            # ön (z=0) sağda, soldan bakınca solda; üstten bakınca ön aşağıdadır.
            hucre = {"front": lambda x, y, z: (x, y), "top": lambda x, y, z: (x, z),
                     "right": lambda x, y, z: (-z - 1, y), "left": lambda x, y, z: (z, y)}[gorunum]
            for u, v in sorted({hucre(*k) for k in kupler}, key=lambda q: (q[1], q[0])):
                yuzler.append(([(u, v), (u + 1, v), (u + 1, v + 1), (u, v + 1)], "blue-soft"))
            return {"faces": yuzler, "lines": [], "labels": [], "dots": []}
        renk = {"front": "blue-soft", "top": "paper", "right": "muted-soft"}
        izometrik = fig.get("projection") == "isometric"
        if izometrik:
            # Bakış (1, 1, -1) yönünden: yakınlık x + y - z büyüdükçe artar, uzaktan yakına boyanır.
            iz = lambda x, y, z: ((x + z) * KATI_IZO, y + (z - x) / 2)
            sira = lambda k: (k[0] + k[1] - k[2], k[1], k[0])
        else:
            iz = lambda x, y, z: (x + c * z, y + s * z)
            sira = lambda k: (-k[2], k[1], k[0])
        for x, y, z in sorted(kupler, key=sira):
            if (x, y, z - 1) not in kupler:
                yuzler.append(([iz(x, y, z), iz(x + 1, y, z), iz(x + 1, y + 1, z), iz(x, y + 1, z)], renk["front"]))
            if (x, y + 1, z) not in kupler:
                yuzler.append(([iz(x, y + 1, z), iz(x + 1, y + 1, z), iz(x + 1, y + 1, z + 1), iz(x, y + 1, z + 1)], renk["top"]))
            if (x + 1, y, z) not in kupler:
                yuzler.append(([iz(x + 1, y, z), iz(x + 1, y, z + 1), iz(x + 1, y + 1, z + 1), iz(x + 1, y + 1, z)], renk["right"]))
        return {"faces": yuzler, "lines": [], "labels": [], "dots": isometric_dots(yuzler) if izometrik else []}
    if tur == "cuboid":
        w, h, d = olcu["w"], olcu["h"], olcu["d"]
        koseler = [(x * w, y * h, z * d) for z in (0, 1) for y in (0, 1) for x in (0, 1)]
        yuzler_idx = [[0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5]]
        iz, yuzler, cizgiler = _cokyuzlu(koseler, yuzler_idx)
        boy = math.hypot(s, c)
        yerler = {"w": (orta(iz[0], iz[1]), (0.0, -1.0)), "h": (orta(iz[0], iz[2]), (-1.0, 0.0)),
                  "d": (orta(iz[1], iz[5]), (s / boy, -c / boy))}
        adlar = [(k, *yerler[k]) for k in ("w", "h", "d") if k in adli]
    elif tur in ("prism", "pyramid"):
        n = int(fig.get("sides", 3 if tur == "prism" else 4))
        a, h = olcu["a"], olcu["h"]
        taban = _taban(n, a)
        koseler = [(x, 0.0, z) for x, z in taban]
        if tur == "prism":
            koseler += [(x, h, z) for x, z in taban]
            yuzler_idx = [list(range(n)), list(range(n, 2 * n))] + [
                [k, (k + 1) % n, n + (k + 1) % n, n + k] for k in range(n)]
        else:
            koseler.append((0.0, h, 0.0))
            yuzler_idx = [list(range(n))] + [[k, (k + 1) % n, n] for k in range(n)]
        iz, yuzler, cizgiler = _cokyuzlu(koseler, yuzler_idx)
        if "a" in adli:
            adlar.append(("a", orta(iz[0], iz[1]), (0.0, -1.0)))
        if "h" in adli:
            if tur == "prism":
                k = max(range(n), key=lambda i: iz[i][0])
                adlar.append(("h", orta(iz[k], iz[n + k]), (1.0, 0.0)))
            else:
                # Piramit yüksekliği tepeden taban merkezine kesik çizgi.
                cizgiler.append(([iz[n], (0.0, 0.0)], True))
                adlar.append(("h", orta(iz[n], (0.0, 0.0)), (-1.0, 0.0)))
    elif tur in ("cylinder", "cone"):
        r, h = olcu["r"], olcu["h"]
        on = _elips(r, 0.0, math.pi, 2 * math.pi)  # tabanın ön (alt) yarısı
        arka = _elips(r, 0.0, 0.0, math.pi)
        if tur == "cylinder":
            ust_on = _elips(r, h, math.pi, 2 * math.pi)
            yuzler = [([(-r, h), *on, (r, h), *reversed(ust_on)], "surface"),
                      (_elips(r, h, 0.0, 2 * math.pi)[:-1], "paper")]
            cizgiler = [(arka, True), (on, False), ([(-r, 0.0), (-r, h)], False), ([(r, 0.0), (r, h)], False),
                        (_elips(r, h, 0.0, 2 * math.pi), False)]
            if "r" in adli:
                # Üst elips ince; ad yarıçapın ucunda, elipsin dışında sağ üstte durur.
                cizgiler.append(([(0.0, h), (r, h)], False))
                adlar.append(("r", (r, h), (0.6, 0.8)))
            if "h" in adli:
                adlar.append(("h", (r, h / 2), (1.0, 0.0)))
        else:
            yuzler = [([(0.0, h), *on], "surface")]
            cizgiler = [(arka, True), (on, False), ([(-r, 0.0), (0.0, h)], False), ([(0.0, h), (r, 0.0)], False)]
            if "r" in adli:
                # Taban koninin içinde kalır; yarıçap gizli çizgidir.
                cizgiler.append(([(0.0, 0.0), (r, 0.0)], True))
                adlar.append(("r", (r / 2, 0.0), (0.0, 1.0)))
            if "h" in adli:
                cizgiler.append(([(0.0, h), (0.0, 0.0)], True))
                adlar.append(("h", (0.0, h / 2), (-1.0, 0.0)))
    return {"faces": yuzler, "lines": cizgiler, "labels": adlar}


def isometric_dots(faces: list) -> list:
    """1.6 izometrik nokta kağıdı: küp köşelerinin düştüğü kafes (sütun a: x = a·cos30°,
    y ∈ a/2 + ℤ), çizimin çevresinde bir aralık payla; sütun sütun, aşağıdan yukarı.
    Android `FigureMath.isometricDots`."""
    xs = [p[0] for pts, _ in faces for p in pts]
    ys = [p[1] for pts, _ in faces for p in pts]
    a0, a1 = round(min(xs) / KATI_IZO) - 1, round(max(xs) / KATI_IZO) + 1
    v0, v1 = round(2 * min(ys)) - 2, round(2 * max(ys)) + 2
    return [(a * KATI_IZO, v / 2) for a in range(a0, a1 + 1) for v in range(v0, v1 + 1) if (v - a) % 2 == 0]


def _kati_hatalari(fig: dict) -> list:
    """1.6 hazır cisim alanları: ölçü adları, taban kenar sayısı, birim küpler, okunur oran."""
    h = []
    tur = fig["type"]
    for alan in ("points", "vertexKeys", "marks", "circleParts", "centerKey"):
        if alan in fig:
            h.append(f"shape: {alan} cisimde (type={tur}) yazılmaz")
    if "sides" in fig and tur not in ("prism", "pyramid"):
        h.append("shape: sides yalnız polygon, prism ve pyramid ile yazılır")
    elif "sides" in fig:
        s = fig["sides"]
        if not isinstance(s, int) or isinstance(s, bool) or not KATI_TABAN[0] <= s <= KATI_TABAN[1]:
            h.append(f"shape: {tur} sides {KATI_TABAN[0]}..{KATI_TABAN[1]} tam sayı olmalı")
    izinli = set(KATI_OLCU[tur])
    dims = fig.get("dims") or {}
    if set(dims) - izinli:
        h.append(f"shape: {tur} dims yalnız {sorted(izinli)}")
    adlar = fig.get("sideLabels")
    if adlar is not None and (not isinstance(adlar, dict) or not all(
        k in izinli and isinstance(v, str) and v.strip() for k, v in adlar.items()
    )):
        h.append(f"shape: {tur} sideLabels anahtarları {sorted(izinli)}, değerleri boş olmayan anahtar olmalı")
    if tur == "cubes":
        kupler = fig.get("cubes")
        tam = lambda v: isinstance(v, int) and not isinstance(v, bool) and 0 <= v < KATI_KUP_SINIR
        if (not isinstance(kupler, list) or not 1 <= len(kupler) <= KATI_KUP_EN_COK or not all(
            isinstance(k, list) and len(k) == 3 and all(tam(v) for v in k) for k in kupler
        )):
            h.append(f"shape: cubes 1..{KATI_KUP_EN_COK} adet [x, y, z] (0..{KATI_KUP_SINIR - 1} tam sayı) olmalı")
        else:
            konum = {tuple(k) for k in kupler}
            if len(konum) != len(kupler):
                h.append("shape: cubes aynı konumu iki kez içeremez")
            elif any(y > 0 and (x, y - 1, z) not in konum for x, y, z in konum):
                h.append("shape: cubes yerde (y=0) ya da altındaki küpün üstünde durmalı")
    elif "cubes" in fig:
        h.append("shape: cubes yalnız type=cubes ile yazılır")
    for alan, degerler in (("view", KATI_GORUNUM), ("projection", KATI_IZDUSUM)):
        if alan in fig and (tur != "cubes" or not isinstance(fig[alan], str) or fig[alan] not in degerler):
            h.append(f"shape: {alan} yalnız type=cubes ile {'/'.join(degerler)} olur")
    if "view" in fig and "projection" in fig:
        h.append("shape: view (dik görünüm) ile projection birlikte yazılmaz")
    if "net" in fig:
        # 1.6 açınım: piramit ve koninin yüksekliği açınımda görünmez.
        if not isinstance(fig["net"], bool) or tur == "cubes":
            h.append("shape: net true/false olmalı ve yalnız cuboid, prism, pyramid, cylinder, cone ile yazılır")
        elif fig["net"] and tur in ("pyramid", "cone") and isinstance(adlar, dict) and "h" in adlar:
            h.append(f"shape: {tur} açınımında (net) yükseklik görünmez; sideLabels.h yazılmaz")
    if not h and tur != "cubes":
        olcu = list(solid_dims(fig).values())
        if max(olcu) / min(olcu) > KATI_ORAN_EN_COK:
            h.append(f"shape: {tur} ölçüleri çizimde okunmaz (en büyük / en küçük > {KATI_ORAN_EN_COK:g})")
    return h


def _sekil_16_hatalari(fig: dict) -> list:
    """1.6 shape: polygon sides/points, vertexKeys, polygon sideLabels, marks."""
    h = []
    tur = fig.get("type")
    for alan in ("sides", "points"):
        if alan in fig and tur != "polygon":
            h.append(f"shape: {alan} yalnız type=polygon ile yazılır")
    for alan in ("circleParts", "centerKey"):
        if alan in fig and tur != "circle":
            h.append(f"shape: {alan} yalnız type=circle ile yazılır")
    if tur == "circle":
        h.extend(_cember_hatalari(fig))
    if tur == "polygon":
        en_az, en_cok = SEKIL_KOSE
        if "sides" in fig and "points" in fig:
            h.append("shape: sides ve points birlikte yazılmaz")
        elif "sides" in fig:
            s = fig["sides"]
            if not isinstance(s, int) or isinstance(s, bool) or not en_az <= s <= en_cok:
                h.append(f"shape: sides {en_az}..{en_cok} tam sayı olmalı")
        elif "points" in fig:
            pts = fig["points"]
            if (not isinstance(pts, list) or not en_az <= len(pts) <= en_cok or not all(
                isinstance(p, list) and len(p) == 2 and all(_sayi_mi(v) and math.isfinite(float(v)) for v in p)
                for p in pts
            )):
                h.append(f"shape: points {en_az}..{en_cok} adet [x, y] sonlu sayı çifti olmalı")
            elif not polygon_simple([(float(x), float(y)) for x, y in pts]):
                h.append("shape: points kendini kesmeyen, alanı sıfır olmayan bir çokgen olmalı")
    if h:
        return h
    try:
        koseler = shape_vertices(fig)
    except (ValueError, TypeError):
        return ["shape: üçgen kenarları üçgen eşitsizliğini sağlamıyor"]
    n = len(koseler)
    if "vertexKeys" in fig:
        anahtarlar = fig["vertexKeys"]
        if tur == "circle" or not isinstance(anahtarlar, list) or len(anahtarlar) != n or not all(
            isinstance(k, str) and k.strip() for k in anahtarlar
        ):
            h.append("shape: vertexKeys köşe sayısı kadar boş olmayan anahtar olmalı (circle hariç)")
    if tur == "polygon" and "sideLabels" in fig:
        adlar = fig["sideLabels"]
        if not isinstance(adlar, dict) or not all(
            k in {str(i) for i in range(n)} and isinstance(v, str) and v.strip() for k, v in adlar.items()
        ):
            h.append("shape: polygon sideLabels anahtarları kenar sırası (\"0\".."
                     "\"n-1\"), değerleri boş olmayan anahtar olmalı")
    if "marks" in fig:
        h.extend(_sekil_isaret_hatalari(fig["marks"], tur, koseler))
    return h


def _sekil_isaret_hatalari(isaret, tur, koseler) -> list:
    n = len(koseler)
    if tur == "circle" or not isinstance(isaret, dict) or not set(isaret) <= SEKIL_ISARET_ALANLARI:
        return ["shape: marks yalnız {equal?, parallel?, right?, angles?, exterior?, height?, median?, bisector?} "
                "sözlüğü olur (circle hariç)"]
    h = []
    tam = lambda v: isinstance(v, int) and not isinstance(v, bool) and 0 <= v < n
    uzunluk = lambda i: math.dist(koseler[i], koseler[(i + 1) % n])
    if "equal" in isaret:
        gruplar = isaret["equal"]
        if (not isinstance(gruplar, list) or not 1 <= len(gruplar) <= SEKIL_ESIT_GRUP
                or not all(isinstance(g, list) and len(g) >= 2 and all(tam(v) for v in g) for g in gruplar)):
            h.append(f"shape: marks.equal 1..{SEKIL_ESIT_GRUP} grup, her grup ≥ 2 kenar sırası olmalı")
        else:
            hepsi = [v for g in gruplar for v in g]
            if len(hepsi) != len(set(hepsi)):
                h.append("shape: marks.equal bir kenarı birden çok kez içeremez")
            for g in gruplar:
                boylar = [uzunluk(i) for i in g]
                if max(boylar) - min(boylar) > SEKIL_ESIT_TOLERANS * max(boylar):
                    h.append(f"shape: marks.equal {g} kenarları çizimde eşit değil")
    if "parallel" in isaret:
        gruplar = isaret["parallel"]
        if (not isinstance(gruplar, list) or not 1 <= len(gruplar) <= SEKIL_PARALEL_GRUP
                or not all(isinstance(g, list) and len(g) >= 2 and all(tam(v) for v in g) for g in gruplar)):
            h.append(f"shape: marks.parallel 1..{SEKIL_PARALEL_GRUP} grup, her grup ≥ 2 kenar sırası olmalı")
        else:
            hepsi = [v for g in gruplar for v in g]
            if len(hepsi) != len(set(hepsi)):
                h.append("shape: marks.parallel bir kenarı birden çok kez içeremez")
            yon = lambda i: math.degrees(math.atan2(koseler[(i + 1) % n][1] - koseler[i][1],
                                                    koseler[(i + 1) % n][0] - koseler[i][0]))
            for g in gruplar:
                # Yön farkı 180° kipinde; ters yönlü karşı kenar da paraleldir.
                if any(abs((yon(i) - yon(g[0]) + 90) % 180 - 90) > SEKIL_ACI_TOLERANS for i in g):
                    h.append(f"shape: marks.parallel {g} kenarları çizimde paralel değil")
    if "right" in isaret:
        dik = isaret["right"]
        if not isinstance(dik, list) or not all(tam(v) for v in dik) or len(dik) != len(set(dik)):
            h.append("shape: marks.right farklı köşe sıraları listesi olmalı")
        else:
            for i in dik:
                if abs(shape_angle(koseler, i) - 90) > SEKIL_ACI_TOLERANS:
                    h.append(f"shape: marks.right köşe {i} çizimde dik açı değil")
    for alan in ("angles", "exterior"):
        # Köşe açısı adı {"köşe sırası": anahtar}; yay yalnız dışbükey köşede anlamlı.
        if alan not in isaret:
            continue
        adlar = isaret[alan]
        if not isinstance(adlar, dict) or not adlar or not all(
                str(k).isdigit() and int(k) < n and isinstance(v, str) and v.strip() for k, v in adlar.items()):
            h.append(f"shape: marks.{alan} {{\"köşe sırası\": anahtar}} olmalı; sıra köşe sayısından küçük")
            continue
        for k in adlar:
            if not shape_convex_at(koseler, int(k)):
                h.append(f"shape: marks.{alan} köşe {k} dışbükey değil (iç açı 180°'den küçük olmalı)")
    if "height" in isaret:
        y = isaret["height"]
        if (not isinstance(y, dict) or not {"from", "to"} <= set(y) <= {"from", "to", "labelKey"}
                or not tam(y["from"]) or not tam(y["to"]) or y["from"] in (y["to"], (y["to"] + 1) % n)
                or ("labelKey" in y and not (isinstance(y["labelKey"], str) and y["labelKey"].strip()))):
            h.append("shape: marks.height {from, to, labelKey?} olmalı; from köşe, to o köşeye değmeyen kenar sırası")
        else:
            dik = shape_height(koseler, y["from"], y["to"])
            kenar = math.dist(koseler[y["to"]], koseler[(y["to"] + 1) % n])
            # Ayak komşu köşeye oturuyorsa dikme o köşedeki kenarın ta kendisidir.
            komsu = (abs(dik["t"]) < SEKIL_ESIT_TOLERANS and y["from"] == (y["to"] - 1) % n) or \
                (abs(dik["t"] - 1) < SEKIL_ESIT_TOLERANS and y["from"] == (y["to"] + 2) % n)
            if math.dist(koseler[y["from"]], dik["foot"]) < 1e-6 * kenar:
                h.append("shape: marks.height köşe kenarın doğrusu üzerinde")
            elif komsu:
                h.append("shape: marks.height bir kenarla çakışıyor (dik kenar zaten yüksekliktir)")
    for alan in ("median", "bisector"):
        # 1.6 üçgende kenarortay / açıortay: köşe from'dan karşı kenara.
        if alan not in isaret:
            continue
        y = isaret[alan]
        if n != 3:
            h.append(f"shape: marks.{alan} yalnız üçgende (3 köşe) yazılır")
        elif (not isinstance(y, dict) or not {"from"} <= set(y) <= {"from", "labelKey"} or not tam(y["from"])
              or ("labelKey" in y and not (isinstance(y["labelKey"], str) and y["labelKey"].strip()))):
            h.append(f"shape: marks.{alan} {{from, labelKey?}} olmalı; from köşe sırası")
        elif alan == "median" and any(isinstance(g, list) and (y["from"] + 1) % 3 in g
                                      for g in (isaret.get("equal") if isinstance(isaret.get("equal"), list) else [])):
            h.append("shape: marks.median karşı kenarı marks.equal içinde olamaz (yarı çentikleri karışır)")
        elif alan == "bisector" and (
                any(isinstance(isaret.get(k), dict) and str(y["from"]) in isaret[k] for k in ("angles", "exterior"))
                or (isinstance(isaret.get("right"), list) and y["from"] in isaret["right"])):
            h.append("shape: marks.bisector köşesine angles/exterior/right yazılmaz (eş yarı yaylar çizilir)")
    return h


def _sayi_dogrusu_aralik_hatalari(fig: dict) -> list:
    """1.6 intervals: [from, to] aralığı; from/to yoksa o yöne ışın."""
    h = []
    mn, mx = fig["min"], fig["max"]
    araliklar = fig.get("intervals", [])
    if not isinstance(araliklar, list) or len(araliklar) > SAYI_DOGRUSU_ARALIK:
        return [f"numberline: intervals 0..{SAYI_DOGRUSU_ARALIK} öğeli liste değil"]
    for i, oge in enumerate(araliklar):
        if not isinstance(oge, dict) or set(oge) - SAYI_DOGRUSU_ARALIK_ALANLARI:
            h.append(f"numberline: intervals[{i}] yalnız from/to/fromClosed/toClosed/labelKey/color içerebilir")
            continue
        uclar = [oge.get(alan) for alan in ("from", "to") if alan in oge]
        if not uclar:
            h.append(f"numberline: intervals[{i}] en az bir uç (from/to) içermeli")
        elif not all(_sayi_mi(v) and math.isfinite(float(v)) and mn <= v <= mx for v in uclar):
            h.append(f"numberline: intervals[{i}] uçları [min, max] içinde olmalı")
        elif len(uclar) == 2 and not uclar[0] < uclar[1]:
            h.append(f"numberline: intervals[{i}] from < to olmalı")
        for uc, alan in (("from", "fromClosed"), ("to", "toClosed")):
            if alan in oge and (not isinstance(oge[alan], bool) or uc not in oge):
                h.append(f"numberline: intervals[{i}].{alan} yalnız {uc} varken true/false olur")
        if "labelKey" in oge and (not isinstance(oge["labelKey"], str) or not oge["labelKey"].strip()):
            h.append(f"numberline: intervals[{i}].labelKey boş olamaz")
        if "color" in oge and (oge["color"] not in DIAGRAM_RENK or oge["color"] == "none"):
            h.append(f"numberline: intervals[{i}].color beyaz liste dışı")
    return h


def _sayi_dogrusu_sicrama_hatalari(fig: dict) -> list:
    """1.6 jumps: from'dan to'ya eksen üstünde yay ve ok; adı yoksa işaretli fark (+5, −3)."""
    mn, mx = fig["min"], fig["max"]
    sicramalar = fig["jumps"]
    if not isinstance(sicramalar, list) or not 1 <= len(sicramalar) <= SAYI_DOGRUSU_SICRAMA:
        return [f"numberline: jumps 1..{SAYI_DOGRUSU_SICRAMA} öğeli liste olmalı"]
    h = []
    if "intervals" in fig or "marks" in fig:
        h.append("numberline: jumps ile intervals/marks birlikte yazılmaz (başlangıç highlight ile)")
    for i, oge in enumerate(sicramalar):
        if not isinstance(oge, dict) or set(oge) - SAYI_DOGRUSU_SICRAMA_ALANLARI:
            h.append(f"numberline: jumps[{i}] yalnız from/to/labelKey/color içerebilir")
            continue
        uclar = [oge.get("from"), oge.get("to")]
        if not all(_sayi_mi(v) and math.isfinite(float(v)) and mn <= v <= mx for v in uclar):
            h.append(f"numberline: jumps[{i}] from ve to [min, max] içinde sayı olmalı")
        elif uclar[0] == uclar[1]:
            h.append(f"numberline: jumps[{i}] from ≠ to olmalı")
        if "labelKey" in oge and (not isinstance(oge["labelKey"], str) or not oge["labelKey"].strip()):
            h.append(f"numberline: jumps[{i}].labelKey boş olamaz")
        if "color" in oge and (oge["color"] not in DIAGRAM_RENK or oge["color"] == "none"):
            h.append(f"numberline: jumps[{i}].color beyaz liste dışı")
    return h


def numberline_jumps_layout(jumps: list, conv, size, samples: int = 24) -> dict:
    """1.6 atlama okları (eksenden yukarı yükseklik, px; Android `FigureMath.numberlineJumps` aynası).

    Her atlama from'dan to'ya yarım elips yaydır; yükseklik açıklığın 0,35'i (16..46). Önceki bir
    yay ya da ad bu yayın üstünde kalıyorsa (geri dönüş, iç içe binme) atlama bir kata çıkar: taban,
    açıklık içindeki önceki çizimlerin 10 px üstüne alınır, uçlar eksene kesik çizgiyle iner. Ad tepenin
    4 px üstünde ortalanır; önceki ad ya da yaya binerse taban yükselir. size(sıra) -> (yarı genişlik,
    yarı yükseklik). Dönen "top": en üst ad + 6 px.
    """
    en_az, en_cok, oran = SICRAMA_YAY
    yay_noktalari: list = []  # (x, yükseklik) önceki yaylar
    adlar: list = []  # (x0, x1, alt, üst) önceki ad kutuları
    sonuc = []
    for i, oge in enumerate(jumps):
        a, b = float(conv(oge["from"])), float(conv(oge["to"]))
        sol, sag = min(a, b), max(a, b)
        orta, yari = (sol + sag) / 2, max((sag - sol) / 2, 1e-9)
        hw, hh = size(i)
        yuk = min(max(oran * (sag - sol), en_az), en_cok)

        def kendi(x):  # tabanı 0 olan yayın x'teki yüksekliği
            t = min(abs(x - orta) / yari, 1.0)
            return yuk * math.sqrt(1 - t * t)

        cakisma = any(sol + 1 < x < sag - 1 and ust >= 2 and ust + 6 > kendi(x) for x, ust in yay_noktalari)
        for x0, x1, _, ust in adlar:
            k0, k1 = max(x0, sol - 8), min(x1, sag + 8)  # ok ucu yarı genişliği payı
            if k0 <= k1 and ust + 6 > min(kendi(k0), kendi(k1)):
                cakisma = True
        taban = 0.0
        if cakisma:
            ustler = [ust for x, ust in yay_noktalari if sol - 2 <= x <= sag + 2]
            ustler += [ust for x0, x1, _, ust in adlar if x0 <= sag + 8 and sol - 8 <= x1]
            taban = max(ustler) + 10
        for _ in range(len(adlar) + len(yay_noktalari) + 1):
            once = taban
            alt = taban + yuk + 4
            for x0, x1, a_alt, a_ust in adlar:
                if x0 < orta + hw + 2 and orta - hw - 2 < x1 and a_alt < alt + 2 * hh + 4 and alt < a_ust + 4:
                    taban = max(taban, a_ust + 4 - yuk)
            for x, ust in yay_noktalari:
                if orta - hw - 2 < x < orta + hw + 2 and ust + 4 > alt:
                    taban = max(taban, ust - yuk)
            if taban == once:
                break
        noktalar = []
        for k in range(samples + 1):
            fi = math.pi * k / samples
            noktalar.append((a + (b - a) * (1 - math.cos(fi)) / 2, taban + yuk * math.sin(fi)))
        sonuc.append({"points": noktalar, "label": (orta, taban + yuk + 4 + hh), "rise": yuk, "base": taban})
        yay_noktalari.extend(noktalar)
        adlar.append((orta - hw, orta + hw, taban + yuk + 4, taban + yuk + 4 + 2 * hh))
    top = max((ad[3] for ad in adlar), default=0.0) + 6
    return {"jumps": sonuc, "top": top}


def rounded_rect(x0: float, y0: float, x1: float, y1: float, r: float, steps: int = 6) -> list:
    """Köşeleri r yarıçaplı yuvarlatılmış dikdörtgen çokgeni (ekran, y aşağı), saat yönünde."""
    r = max(0.0, min(r, (x1 - x0) / 2, (y1 - y0) / 2))
    points = []
    for cx, cy, bas in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for k in range(steps + 1):
            a = math.radians(bas + 90 * k / steps)
            points.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return points


def _bezier(p0: tuple, p1: tuple, p2: tuple, steps: int = 12) -> list:
    return [((1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * p1[1] + t * t * p2[1])
            for t in (k / steps for k in range(1, steps + 1))]


def chance_ball_colors(items: list) -> list:
    """Torbadaki top renkleri dizilme sırasıyla: renkler birer birer dönüşümlü alınır (karışık görünüm)."""
    kalan = [int(item["count"]) for item in items]
    sira = []
    while any(kalan):
        for j, item in enumerate(items):
            if kalan[j]:
                sira.append(item["color"])
                kalan[j] -= 1
    return sira


def chance_bag_layout(n: int, x0: float, y0: float, x1: float, y1: float) -> dict:
    """1.6 torba (ekran, y aşağı): gövde çokgeni, ağız fırfırı, bağ kutusu ve n topun merkezleri.
    Torba kutuya sığan en büyük boydadır (yükseklik = .95·genişlik); toplar gövdenin alt kısmına,
    alttan yukarı ve satır ortalı dizilir. Top yarıçapı en çok 22."""
    w, h = x1 - x0, y1 - y0
    bw = min(w, h / .95)
    bh = .95 * bw
    cx = (x0 + x1) / 2
    top = y0 + (h - bh) / 2
    bottom = top + bh
    kose = .3 * bw
    boyun = (cx - .12 * bw, top + .16 * bh)
    sol = [boyun] + _bezier(boyun, (cx - .5 * bw, top + .2 * bh), (cx - .5 * bw, top + .55 * bh))
    sol += [(cx - .5 * bw + kose - kose * math.cos(math.radians(90 * k / 8)),
             bottom - kose + kose * math.sin(math.radians(90 * k / 8))) for k in range(9)]
    govde = sol + [(2 * cx - x, y) for x, y in reversed(sol)]
    # Ağız fırfırı: boyundan açılan, üst kenarı dalgalı kumaş.
    agiz = [boyun, (cx - .24 * bw, top + .03 * bh), (cx - .12 * bw, top), (cx, top + .04 * bh),
            (cx + .12 * bw, top), (cx + .24 * bw, top + .03 * bh), (cx + .12 * bw, top + .16 * bh)]
    bag = (cx - .15 * bw, top + .12 * bh, cx + .15 * bw, top + .18 * bh)
    ic_x0, ic_x1, ic_y0, ic_y1 = cx - .36 * bw, cx + .36 * bw, top + .45 * bh, bottom - .05 * bh
    d, k = -1.0, 1
    for aday in range(1, max(1, n) + 1):
        u = min((ic_x1 - ic_x0) / aday, (ic_y1 - ic_y0) / math.ceil(max(1, n) / aday))
        if u > d + 1e-9:
            d, k = u, aday
    r = min(.42 * d, 22.0)
    adim = 2.3 * r
    toplar = []
    for b in range(n):
        satir, sira = divmod(b, k)
        say = min(k, n - satir * k)
        toplar.append((cx + (sira - (say - 1) / 2) * adim, ic_y1 - r - satir * adim))
    return {"body": govde, "mouth": agiz, "tie": bag, "balls": toplar, "r": r}


def _cark_noktasi(cx: float, cy: float, r: float, derece: float) -> tuple:
    a = math.radians(derece)
    return (cx + r * math.sin(a), cy - r * math.cos(a))


def chance_spinner_layout(weights: list, pointer, w: float, h: float) -> dict:
    """1.6 çark: dilimler tepeden saat yönünde ağırlıkla orantılı (start/sweep derece), ad noktası
    .68r'de; pointer verilmişse ok merkezden o dilimin ortasına .5r uzanır."""
    r = max(20.0, min(w - 40, h - 30) / 2)
    cx, cy = w / 2, h / 2
    toplam = float(sum(weights))
    bas, dilimler = 0.0, []
    for agirlik in weights:
        sweep = 360 * agirlik / toplam
        dilimler.append({"start": bas, "sweep": sweep, "label": _cark_noktasi(cx, cy, .68 * r, bas + sweep / 2)})
        bas += sweep
    ok = None
    if pointer is not None:
        hedef = dilimler[pointer]
        ok = _cark_noktasi(cx, cy, .5 * r, hedef["start"] + hedef["sweep"] / 2)
    return {"center": (cx, cy), "r": r, "sectors": dilimler, "pointer": ok}


def chance_dice_layout(faces: list, w: float, h: float) -> list:
    """1.6 zarlar yan yana, ortalı; kenar en çok 110, aralık 24. Her zar kutu, köşe yarıçapı ve noktalar."""
    n, ara = len(faces), 24.0
    s = max(20.0, min(110.0, (w - 40 - ara * (n - 1)) / n, h - 40))
    sol, ust = (w - n * s - ara * (n - 1)) / 2, (h - s) / 2
    zarlar = []
    for i, yuz in enumerate(faces):
        x = sol + i * (s + ara)
        zarlar.append({"box": (x, ust, x + s, ust + s), "corner": .16 * s, "pipR": .085 * s,
                       "pips": [(x + u * s, ust + v * s) for u, v in ZAR_NOKTA[int(yuz)]]})
    return zarlar


def chance_coin_layout(sides: list, w: float, h: float, label_h: float) -> list:
    """1.6 madeni paralar yan yana, ortalı; yarıçap en çok 60, aralık 24. Ad varsa label_h paranın
    altına ayrılır, ad yazısının üst ortası "label"dır. Tura (heads) ortada beş köşeli yıldız amblem
    (pictograph_symbol star, .5r), yazı (tails) çizgilerle "1" rakamı: bayrak, gövde ve taban
    parçaları (kalınlık .12r). İç halka .8r. Android `FigureMath.chanceCoinLayout`."""
    n, ara = len(sides), 24.0
    r = max(16.0, min(60.0, (w - 40 - ara * (n - 1)) / (2 * n), (h - 30 - label_h) / 2))
    sol, cy = (w - 2 * n * r - ara * (n - 1)) / 2, (h - label_h) / 2
    paralar = []
    for i, yuz in enumerate(sides):
        cx = sol + r + i * (2 * r + ara)
        bir = [((cx - .2 * r, cy - .28 * r), (cx + .06 * r, cy - .5 * r)),
               ((cx + .06 * r, cy - .5 * r), (cx + .06 * r, cy + .5 * r)),
               ((cx - .2 * r, cy + .5 * r), (cx + .32 * r, cy + .5 * r))]
        paralar.append({"center": (cx, cy), "r": r, "rim": .8 * r,
                        "star": pictograph_symbol("star", cx, cy, .5 * r) if yuz == "heads" else None,
                        "one": bir if yuz == "tails" else [], "label": (cx, cy + r + 6)})
    return paralar


def chance_cards_layout(n: int, w: float, h: float, text_w: float) -> list:
    """1.6 kartlar sıra sıra (bir sırada en çok 6), her sıra ortalı; en/boy 2:3, en en çok 80,
    aralık 12. En geniş yazı + 16 karta sığmazsa sırada daha az kart olur; yazı küçülmez.
    Kart kutusu, köşe; kapalı kart sırtı için iç çerçeve ve ortada eşkenar dörtgen.
    Android `FigureMath.chanceCardsLayout`."""
    ara = 12.0
    adaylar = []
    for sutun in range(min(n, SANS_KART_SIRA), 0, -1):
        satir = -(-n // sutun)
        adaylar.append((sutun, satir, min(80.0, (w - 40 - ara * (sutun - 1)) / sutun,
                                          (h - 30 - ara * (satir - 1)) / satir / 1.5)))
    sutun, satir, en = next((a for a in adaylar if a[2] >= text_w + 16), max(adaylar, key=lambda a: a[2]))
    en = max(20.0, en)
    boy = 1.5 * en
    ust = (h - satir * boy - ara * (satir - 1)) / 2
    kartlar = []
    for i in range(n):
        s, k = divmod(i, sutun)
        sirada = min(sutun, n - s * sutun)
        x = (w - sirada * en - ara * (sirada - 1)) / 2 + k * (en + ara)
        y = ust + s * (boy + ara)
        cx, cy = x + en / 2, y + boy / 2
        kartlar.append({"box": (x, y, x + en, y + boy), "corner": .12 * en,
                        "inner": (x + .1 * en, y + .1 * en, x + .9 * en, y + boy - .1 * en),
                        "diamond": [(cx, cy - .25 * en), (cx + .18 * en, cy), (cx, cy + .25 * en), (cx - .18 * en, cy)]})
    return kartlar


def _sans_hatalari(fig: dict) -> list:
    """chance: 1.6 torba, çark, zar, madeni para ve kartlar."""
    arac = fig.get("tool")
    if arac not in SANS_ARAC:
        return ["chance: tool ∈ " + "|".join(SANS_ARAC) + " değil"]
    h = []
    sahip = {"items": "bag", "sectors": "spinner", "pointer": "spinner", "faces": "dice", "coins": "coin",
             "cards": "cards"}
    for alan, tur in sahip.items():
        if alan in fig and tur != arac:
            h.append(f"chance: {alan} yalnız tool={tur} ile yazılır")
    gerekli = SANS_ALAN[arac]
    if gerekli not in fig:
        h.append(f"chance: tool={arac} için {gerekli} zorunlu")
    if h:
        return h
    tam = lambda v, a, b: isinstance(v, int) and not isinstance(v, bool) and a <= v <= b
    anahtar = lambda oge: "labelKey" not in oge or (isinstance(oge["labelKey"], str) and oge["labelKey"].strip())
    if arac == "bag":
        ogeler = fig["items"]
        if not isinstance(ogeler, list) or not 1 <= len(ogeler) <= SANS_TOP_RENK_EN_COK:
            return [f"chance: items 1..{SANS_TOP_RENK_EN_COK} öğeli liste değil"]
        renkler, toplam = [], 0
        for i, oge in enumerate(ogeler):
            if (not isinstance(oge, dict) or set(oge) - {"color", "count", "labelKey"}
                    or not isinstance(oge.get("color"), str) or oge["color"] not in SANS_RENK
                    or not tam(oge.get("count"), 1, SANS_TOP_EN_COK)
                    or not anahtar(oge)):
                h.append(f"chance: items[{i}] geçersiz (color, 1..{SANS_TOP_EN_COK} count, labelKey)")
                continue
            renkler.append(oge["color"])
            toplam += oge["count"]
        if len(set(renkler)) != len(renkler):
            h.append("chance: items renkleri farklı olmalı")
        if toplam > SANS_TOP_EN_COK:
            h.append(f"chance: torbada en çok {SANS_TOP_EN_COK} top olur")
    elif arac == "spinner":
        dilimler = fig["sectors"]
        en_az, en_cok = SANS_DILIM
        if not isinstance(dilimler, list) or not en_az <= len(dilimler) <= en_cok:
            return [f"chance: sectors {en_az}..{en_cok} öğeli liste değil"]
        for i, oge in enumerate(dilimler):
            if (not isinstance(oge, dict) or set(oge) - {"color", "labelKey", "weight"}
                    or not isinstance(oge.get("color"), str) or oge["color"] not in SANS_RENK
                    or ("weight" in oge and not tam(oge["weight"], 1, SANS_AGIRLIK_EN_COK)) or not anahtar(oge)):
                h.append(f"chance: sectors[{i}] geçersiz (color, 1..{SANS_AGIRLIK_EN_COK} weight, labelKey)")
        if "pointer" in fig and not tam(fig["pointer"], 0, len(dilimler) - 1):
            h.append("chance: pointer dilim sırası (0'dan) olmalı")
    elif arac == "coin":
        paralar = fig["coins"]
        if not isinstance(paralar, list) or not 1 <= len(paralar) <= SANS_PARA_EN_COK:
            return [f"chance: coins 1..{SANS_PARA_EN_COK} öğeli liste değil"]
        for i, oge in enumerate(paralar):
            if (not isinstance(oge, dict) or set(oge) - {"side", "labelKey"}
                    or not isinstance(oge.get("side"), str) or oge["side"] not in SANS_PARA_YUZ or not anahtar(oge)):
                h.append(f"chance: coins[{i}] geçersiz (side {'|'.join(SANS_PARA_YUZ)}, labelKey)")
    elif arac == "cards":
        kartlar = fig["cards"]
        if not isinstance(kartlar, list) or not 1 <= len(kartlar) <= SANS_KART_EN_COK:
            return [f"chance: cards 1..{SANS_KART_EN_COK} öğeli liste değil"]
        for i, oge in enumerate(kartlar):
            kapali = isinstance(oge, dict) and oge.get("faceDown") is True
            if (not isinstance(oge, dict) or set(oge) - {"value", "labelKey", "color", "faceDown"}
                    or ("faceDown" in oge and not isinstance(oge["faceDown"], bool))
                    or ("color" in oge and (not isinstance(oge["color"], str) or oge["color"] not in SANS_RENK))
                    or ("value" in oge and not tam(oge["value"], 0, SANS_KART_DEGER)) or not anahtar(oge)
                    or (("value" in oge or "labelKey" in oge) if kapali else ("value" in oge) == ("labelKey" in oge))):
                h.append(f"chance: cards[{i}] geçersiz (açık kartta value 0..{SANS_KART_DEGER} ya da labelKey, "
                         "kapalı kartta (faceDown) ikisi de yok; color)")
    else:
        yuzler = fig["faces"]
        if (not isinstance(yuzler, list) or not 1 <= len(yuzler) <= SANS_ZAR_EN_COK
                or not all(tam(v, 1, 6) for v in yuzler)):
            h.append(f"chance: faces 1..{SANS_ZAR_EN_COK} öğeli, her biri 1..6 tam sayı olmalı")
    return h


def _kesir_alan_hatalari(fig: dict) -> list:
    """1.6 kesirlerde çarpma alan modeli: parts sütun, rows satır; filled sütun ve rowsFilled satır taranır."""
    tam = lambda v, a, b: isinstance(v, int) and not isinstance(v, bool) and a <= v <= b
    h = []
    if "wholes" in fig:
        h.append("fraction: area modeli tek bütündür, wholes yazılmaz")
    if not tam(fig.get("parts"), 2, KESIR_ALAN_EN_COK) or not tam(fig.get("rows"), 2, KESIR_ALAN_EN_COK):
        return h + [f"fraction: area için parts ve rows 2..{KESIR_ALAN_EN_COK} tam sayı olmalı"]
    if not tam(fig.get("filled", 0), 0, fig["parts"]):
        h.append("fraction: area filled 0..parts (taralı sütun) olmalı")
    if not tam(fig.get("rowsFilled", 0), 0, fig["rows"]):
        h.append("fraction: area rowsFilled 0..rows (taralı satır) olmalı")
    return h


def fraction_area_layout(parts: int, rows: int, filled: int, rows_filled: int, w: float, h: float, olc) -> dict:
    """1.6 kesirlerde çarpma alan modeli (ekran, y aşağı). Birim kare parts sütun × rows satıra bölünür;
    soldan filled sütun ve üstten rows_filled satır taranır, kesişim (çarpım) koyu. Sütun kesri karenin
    üstünde, satır kesri solunda köşeli ayraçla yazılır. olc(yazı) -> (genişlik, satır yüksekliği).
    Hücre durumu: both | col | row | empty; hücreler satır satır."""
    th = olc("Ag")[1]
    ust_yazi = f"{filled}/{parts}" if filled else ""
    sol_yazi = f"{rows_filled}/{rows}" if rows_filled else ""
    mt = th + 18 if ust_yazi else 16
    ml = olc(sol_yazi)[0] + 22 if sol_yazi else 16
    kenar = max(60.0, min(w - 2 * ml, h - 2 * mt))
    x0, y0 = (w - kenar) / 2, (h - kenar) / 2
    cw, rh = kenar / parts, kenar / rows
    hucreler = []
    for r in range(rows):
        for k in range(parts):
            durum = ("both" if r < rows_filled else "col") if k < filled else ("row" if r < rows_filled else "empty")
            hucreler.append({"box": (x0 + k * cw, y0 + r * rh, x0 + (k + 1) * cw, y0 + (r + 1) * rh), "state": durum})
    yazilar = []
    if ust_yazi:
        x1 = x0 + filled * cw
        yazilar.append({"text": ust_yazi, "pos": ((x0 + x1) / 2, y0 - 12 - th / 2),
                        "bracket": [x0 + 1, y0 - 3, x0 + 1, y0 - 8, x1 - 1, y0 - 8, x1 - 1, y0 - 3]})
    if sol_yazi:
        y1 = y0 + rows_filled * rh
        yazilar.append({"text": sol_yazi, "pos": (x0 - 14 - olc(sol_yazi)[0] / 2, (y0 + y1) / 2),
                        "bracket": [x0 - 3, y0 + 1, x0 - 8, y0 + 1, x0 - 8, y1 - 1, x0 - 3, y1 - 1]})
    return {"cells": hucreler, "labels": yazilar, "side": kenar}


def fraction_layout(style: str, parts: int, wholes: int, w: float, h: float) -> list:
    """1.6 kesir modeli parçaları (ekran, y aşağı), doldurma sırasıyla: önce birinci bütün.
    Daire dilimi {"box", "start", "sweep"} (start tepeden saat yönünde derece), diğerleri {"box"}.
    bar bütünleri alt alta; pie ve grid bütünleri parçayı en büyük yapan sütun sayısıyla
    (eşitlikte yan yana) dizilir. Tek bütün 1.5 yerleşimiyle aynıdır."""
    if style == "pie":
        bw, bh, alan_w, alan_h, ara, adaylar = 1, 1, w - 35, h - 35, 16, range(wholes, 0, -1)
    elif style == "bar":
        bw, bh, alan_w, alan_h, ara, adaylar = parts, 1, w - 40, h - 30, 12, (1,)
    else:
        kolon = min(parts, 6)
        bw, bh, alan_w, alan_h, ara, adaylar = kolon, math.ceil(parts / kolon), w - 40, h - 30, 16, range(wholes, 0, -1)
    birim, k = -1.0, 1
    for aday in adaylar:
        satir = math.ceil(wholes / aday)
        u = min((alan_w - ara * (aday - 1)) / (aday * bw), (alan_h - ara * (satir - 1)) / (satir * bh))
        if u > birim + 1e-9:
            birim, k = u, aday
    satir = math.ceil(wholes / k)
    sol = (w - k * bw * birim - ara * (k - 1)) / 2
    ust = (h - satir * bh * birim - ara * (satir - 1)) / 2
    hucreler = []
    for b in range(wholes):
        # Eksik son satır ortalanır.
        kayma = (k - min(k, wholes - b // k * k)) * (bw * birim + ara) / 2
        bx, by = sol + kayma + (b % k) * (bw * birim + ara), ust + (b // k) * (bh * birim + ara)
        if style == "pie":
            hucreler.extend({"box": (bx, by, bx + birim, by + birim), "start": 360 * i / parts, "sweep": 360 / parts}
                            for i in range(parts))
            continue
        for i in range(parts):
            x, y = bx + (i % bw) * birim, by + (i // bw) * birim
            hucreler.append({"box": (x, y, x + birim, y + birim)})
    return hucreler


def pictograph_symbol(symbol: str, cx: float, cy: float, r: float, half: bool = False) -> list:
    """1.6 şekil grafiği sembolü çokgeni (ekran, y aşağı); yarım sembol sol yarıdır."""
    if symbol == "square":
        s = r * .86
        noktalar = [(cx - s, cy - s), (cx + s, cy - s), (cx + s, cy + s), (cx - s, cy + s)]
    elif symbol == "star":
        noktalar = [(cx + (r if k % 2 == 0 else r * .45) * math.cos(-math.pi / 2 + k * math.pi / 5),
                     cy + (r if k % 2 == 0 else r * .45) * math.sin(-math.pi / 2 + k * math.pi / 5))
                    for k in range(10)]
    else:
        noktalar = [(cx + r * math.cos(2 * math.pi * k / 32), cy + r * math.sin(2 * math.pi * k / 32))
                    for k in range(32)]
    if not half:
        return noktalar
    # Sutherland-Hodgman: x ≤ cx yarı düzlemi.
    yarim = []
    for (x1, y1), (x2, y2) in zip(noktalar, noktalar[1:] + noktalar[:1]):
        ic1, ic2 = x1 <= cx + 1e-9, x2 <= cx + 1e-9
        if ic1:
            yarim.append((x1, y1))
        if ic1 != ic2:
            t = (cx - x1) / (x2 - x1)
            yarim.append((cx, y1 + t * (y2 - y1)))
    return yarim


def tally_strokes(count: int, x: float, cy: float, height: float, step: float) -> list:
    """1.6 çetele çizgileri (ekran, y aşağı): dört dik çizgi, beşincisi onları çapraz keser."""
    cizgiler = []
    for k in range(count):
        grup, sira = divmod(k, 5)
        gx = x + grup * CETELE_GRUP_ADIMI * step
        if sira < 4:
            cizgiler.append(((gx + sira * step, cy - height / 2), (gx + sira * step, cy + height / 2)))
        else:
            cizgiler.append(((gx - step * .6, cy + height * .3), (gx + step * 3.6, cy - height * .3)))
    return cizgiler


def tally_step(most: int, room: float, height: float) -> float:
    """En uzun çetelenin (most) room genişliğine sığdığı çizgi aralığı; en çok 0,3·height."""
    gruplar = max(1, math.ceil(most / 5))
    return min(height * .3, room / ((gruplar - 1) * CETELE_GRUP_ADIMI + 4.2))


def _grafik_hatalari(fig: dict) -> list:
    """chart: 1.5 bar/line/pie + 1.6 dot, histogram, pictograph, tally, yatay, gruplu seri, yüzde."""
    h = []
    stil = fig.get("style")
    if stil not in GRAFIK_STIL:
        return ["chart: style ∈ " + "|".join(GRAFIK_STIL) + " değil"]
    cats, vals = fig.get("categoryKeys"), fig.get("values")
    if not isinstance(cats, list) or not isinstance(vals, list) or len(cats) != len(vals):
        return ["chart: len(categoryKeys) == len(values) değil"]
    if not cats:
        h.append("chart: en az bir kategori olmalı")
    sonlu = lambda v: _sayi_mi(v) and math.isfinite(float(v))
    seriler = fig.get("seriesKeys")
    if "seriesKeys" in fig:
        en_az, en_cok = GRAFIK_SERI
        if stil not in ("bar", "line"):
            h.append("chart: seriesKeys yalnız bar/line ile yazılır")
        elif (not isinstance(seriler, list) or not en_az <= len(seriler) <= en_cok
              or not all(isinstance(k, str) and k.strip() for k in seriler)):
            h.append(f"chart: seriesKeys {en_az}..{en_cok} boş olmayan anahtar olmalı")
        elif not all(isinstance(v, list) and len(v) == len(seriler) and all(sonlu(x) for x in v) for v in vals):
            h.append("chart: seriesKeys varken her values öğesi seri sayısı kadar sayı listesi olmalı")
    elif not all(sonlu(v) for v in vals):
        h.append("chart: values sayısal değil")
        return h
    elif stil == "pie" and (any(v < 0 for v in vals) or sum(vals) <= 0):
        h.append("chart: style=pie değerleri ≥ 0 ve toplamı > 0 olmalı")
    elif stil == "dot" and not all(
        isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= GRAFIK_NOKTA_EN_COK for v in vals
    ):
        h.append(f"chart: style=dot değerleri 0..{GRAFIK_NOKTA_EN_COK} tam sayı (sıklık) olmalı")
    elif stil == "histogram" and any(v < 0 for v in vals):
        h.append("chart: style=histogram değerleri ≥ 0 olmalı")
    elif stil == "tally" and not all(
        isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= GRAFIK_CETELE_EN_COK for v in vals
    ):
        h.append(f"chart: style=tally değerleri 0..{GRAFIK_CETELE_EN_COK} tam sayı (çetele) olmalı")
    elif stil == "pictograph":
        birim = fig.get("unit", 1)
        if not sonlu(birim) or birim <= 0:
            h.append("chart: style=pictograph unit pozitif sayı olmalı")
        elif any(v < 0 or abs(v / birim * 2 - round(v / birim * 2)) > 1e-9
                 or v / birim > GRAFIK_SEMBOL_EN_COK for v in vals):
            h.append("chart: style=pictograph değerleri unit'in yarım katları olmalı; satırda en çok "
                     f"{GRAFIK_SEMBOL_EN_COK} sembol olur")
    if stil in ("pie", "pictograph", "tally") and "axisKeys" in fig:
        h.append(f"chart: style={stil} iken axisKeys yazılmaz")
    for alan in ("unit", "unitKey", "symbol"):
        if alan in fig and stil != "pictograph":
            h.append(f"chart: {alan} yalnız style=pictograph ile yazılır")
    if stil == "pictograph" and "unitKey" in fig and not (
        isinstance(fig["unitKey"], str) and fig["unitKey"].strip()
    ):
        h.append("chart: unitKey boş olmayan anahtar olmalı")
    if stil == "pictograph" and "symbol" in fig and fig["symbol"] not in GRAFIK_SEMBOL:
        h.append("chart: symbol ∈ " + "|".join(GRAFIK_SEMBOL) + " olmalı")
    if "orientation" in fig and (stil != "bar" or fig["orientation"] not in ("vertical", "horizontal")):
        h.append("chart: orientation yalnız style=bar ile vertical|horizontal olur")
    if "showPercent" in fig and (stil != "pie" or not isinstance(fig["showPercent"], bool)):
        h.append("chart: showPercent yalnız style=pie ile true/false olur")
    if "binEdges" in fig:
        sinirlar = fig["binEdges"]
        if stil != "histogram":
            h.append("chart: binEdges yalnız style=histogram ile yazılır")
        elif (not isinstance(sinirlar, list) or len(sinirlar) != len(vals) + 1
              or not all(sonlu(v) for v in sinirlar)
              or any(a >= b for a, b in zip(sinirlar, sinirlar[1:]))):
            h.append("chart: binEdges kategori sayısı + 1 adet kesin artan sayı olmalı")
    return h


def _koordinat_16_hatalari(fig: dict) -> list:
    """1.6 koordinat alanları: adım, ızgara, eksen adları, çokgen ve doğru."""
    h = []
    (x0, x1), (y0, y1) = fig["xRange"], fig["yRange"]

    def _icinde(pair):
        return (
            isinstance(pair, list) and len(pair) == 2
            and all(_sayi_mi(v) and math.isfinite(float(v)) for v in pair)
            and x0 <= pair[0] <= x1 and y0 <= pair[1] <= y1
        )

    def _etiket_ve_renk(oge, ad, i):
        if "labelKey" in oge and (not isinstance(oge["labelKey"], str) or not oge["labelKey"].strip()):
            h.append(f"coordinate: {ad}[{i}].labelKey boş olamaz")
        if "color" in oge and (oge["color"] not in DIAGRAM_RENK or oge["color"] == "none"):
            h.append(f"coordinate: {ad}[{i}].color beyaz liste dışı")

    if "step" in fig:
        adim = fig["step"]
        if not _sayi_mi(adim) or not math.isfinite(float(adim)) or adim <= 0:
            h.append("coordinate: step > 0 olmalı")
        elif max(x1 - x0, y1 - y0) / adim > KOORDINAT_EN_COK_ARALIK:
            h.append(f"coordinate: step ile eksende en çok {KOORDINAT_EN_COK_ARALIK} aralık olur")
    if "grid" in fig and fig["grid"] not in KOORDINAT_IZGARA:
        h.append("coordinate: grid ∈ none|lines|dots değil")
    for alan in ("axes", "equalScale"):
        if alan in fig and not isinstance(fig[alan], bool):
            h.append(f"coordinate: {alan} true/false olmalı")
    if "axisKeys" in fig:
        eksen = fig["axisKeys"]
        if (not isinstance(eksen, dict) or set(eksen) != {"x", "y"}
                or not all(isinstance(v, str) and v.strip() for v in eksen.values())):
            h.append("coordinate: axisKeys {x, y} anahtarlı olmalı")
        elif fig.get("axes") is False:
            h.append("coordinate: axes=false iken axisKeys yazılmaz")
    en_cok, en_az_kose, en_cok_kose = KOORDINAT_COKGEN
    cokgenler = fig.get("polygons", [])
    if not isinstance(cokgenler, list) or len(cokgenler) > en_cok:
        h.append(f"coordinate: polygons 0..{en_cok} öğeli liste değil")
        cokgenler = []
    for i, oge in enumerate(cokgenler):
        if not isinstance(oge, dict) or set(oge) - {"points", "labelKey", "color"}:
            h.append(f"coordinate: polygons[{i}] yalnız points/labelKey/color içerebilir")
            continue
        noktalar = oge.get("points")
        if (not isinstance(noktalar, list) or not en_az_kose <= len(noktalar) <= en_cok_kose
                or not all(_icinde(p) for p in noktalar)):
            h.append(f"coordinate: polygons[{i}].points {en_az_kose}..{en_cok_kose} nokta ve aralık içinde olmalı")
        _etiket_ve_renk(oge, "polygons", i)
    dogrular = fig.get("lines", [])
    if not isinstance(dogrular, list) or len(dogrular) > KOORDINAT_DOGRU:
        h.append(f"coordinate: lines 0..{KOORDINAT_DOGRU} öğeli liste değil")
        dogrular = []
    for i, oge in enumerate(dogrular):
        if not isinstance(oge, dict) or set(oge) - {"through", "labelKey", "color", "style"}:
            h.append(f"coordinate: lines[{i}] yalnız through/labelKey/color/style içerebilir")
            continue
        iki = oge.get("through")
        if (not isinstance(iki, list) or len(iki) != 2 or not all(_icinde(p) for p in iki)
                or iki[0] == iki[1]):
            h.append(f"coordinate: lines[{i}].through aralık içinde iki farklı nokta olmalı")
        if "style" in oge and oge["style"] not in KOORDINAT_DOGRU_STIL:
            h.append(f"coordinate: lines[{i}].style ∈ line|axis olmalı")
        _etiket_ve_renk(oge, "lines", i)
    vektorler = fig.get("vectors", [])
    if not isinstance(vektorler, list) or len(vektorler) > KOORDINAT_VEKTOR:
        h.append(f"coordinate: vectors 0..{KOORDINAT_VEKTOR} öğeli liste değil")
        vektorler = []
    for i, oge in enumerate(vektorler):
        if not isinstance(oge, dict) or set(oge) - {"from", "to", "labelKey", "color"}:
            h.append(f"coordinate: vectors[{i}] yalnız from/to/labelKey/color içerebilir")
            continue
        if not _icinde(oge.get("from")) or not _icinde(oge.get("to")) or oge["from"] == oge["to"]:
            h.append(f"coordinate: vectors[{i}] from ve to aralık içinde iki farklı nokta olmalı")
        _etiket_ve_renk(oge, "vectors", i)
    return h


def _parca_kutuya_girer(x1, y1, x2, y2, sol, ust, sag, alt) -> bool:
    """Doğru parçası kutunun içinden geçer mi (Liang–Barsky; kenara değmek geçmek sayılmaz)."""
    t0, t1 = 0.0, 1.0
    for p, q in ((x1 - x2, x1 - sol), (x2 - x1, sag - x1), (y1 - y2, y1 - ust), (y2 - y1, alt - y1)):
        if p == 0:
            if q <= 0:
                return False
        elif p < 0:
            t0 = max(t0, q / p)
        else:
            t1 = min(t1, q / p)
    return t0 < t1


def coordinate_vector_label(ax, ay, bx, by, tw, th, w, h, obstacles=(), segments=(), gap=8.0) -> tuple:
    """1.6 öteleme oku adının merkezi (ekran, y aşağı). Ad okun ortasından, sonra %30, %70, %15, %85
    noktasından dik yönde (önce sol yan) açılır; bunlar binerse bir satır daha uzakta denenir. Tuvale
    sığan, engellere (eksen bantları, öteki adlar: (sol, üst, sağ, alt)) binmeyen ve çizgilerin
    (çokgen kenarı, ok, doğru: (x1, y1, x2, y2)) geçmediği ilk aday seçilir; yoksa yalnız engellere
    binmeyen, o da yoksa tuvale sığan ilk aday kullanılır."""
    uzun = math.hypot(bx - ax, by - ay) or 1.0
    nx, ny = (by - ay) / uzun, -(bx - ax) / uzun
    d = gap + abs(nx) * tw / 2 + abs(ny) * th / 2
    adaylar = [(ax + t * (bx - ax) + isaret * nx * u, ay + t * (by - ay) + isaret * ny * u)
               for u in (d, d + th) for t in (0.5, 0.3, 0.7, 0.15, 0.85) for isaret in (1, -1)]
    sigan = [(cx, cy) for cx, cy in adaylar if tw / 2 <= cx <= w - tw / 2 and th / 2 <= cy <= h - th / 2]
    bos = [(cx, cy) for cx, cy in sigan
           if not any(cx - tw / 2 < sag and sol < cx + tw / 2 and cy - th / 2 < alt and ust < cy + th / 2
                      for sol, ust, sag, alt in obstacles)]
    for cx, cy in bos:
        if not any(_parca_kutuya_girer(*s, cx - tw / 2, cy - th / 2, cx + tw / 2, cy + th / 2) for s in segments):
            return cx, cy
    return (bos or sigan or adaylar)[0]


MODEL_ARAC = ("tiles", "counters", "balance")  # 1.6 modelleme araçları
MODEL_GRUP = 3
MODEL_KARO = {"x2": 4, "x": 10, "1": 10}  # grup başına en çok |adet|
MODEL_KARO_TOPLAM = 30
MODEL_PUL = 15  # grup başına en çok + ya da − pul
MODEL_PUL_TOPLAM = 40
MODEL_KEFE_OGE = 4
MODEL_KEFE_TOPLAM = 12
MODEL_ISLEM = {"+": "+", "-": "\u2212", "=": "="}
MODEL_EGIM = {"level": 0.0, "left": 7.0, "right": -7.0}  # derece; artı = sol kefe aşağıda
OLCU_ARAC = {"thermometer": ("°C", "°F"), "dynamometer": ("N",), "cylinder": ("mL", "cm³")}  # ilk birim varsayılan
OLCU_OKUMA_ALAN = {"value", "objectKey", "labelKey"}
OLCU_OKUMA = 3  # yan yana en çok araç
OLCU_ARALIK = 10  # ana aralık sayısı 2..10
OLCU_ALT = 10  # ana aralık başına en çok alt bölme
OLCU_CENTIK = 100
OLCU_SINIR = 10000
OLCU_ALT_ARALIK = 5.0  # alt çentikler arası en az px/dp
ISIK_YUZEY = ("mirror", "boundary")
ISIK_ACI = ("incidence", "reflection", "refraction")  # angleKeys
ISIK_ISIN = ("incident", "reflected", "refracted")  # rayKeys; sırası ISIK_ACI ile eş
ISIK_YOGUN = ("top", "bottom")
ISIK_GELME = 80
ISIK_KIRILMA = 85
ISIK_AD_EN_AZ = 15  # adlı açı en az bu kadar derece: ad iki kola değmeden yaya yakın durur
TANECIK_HAL = ("solid", "liquid", "gas")
TANECIK_PANEL = 3
TANECIK_KUTU = 150.0  # panel kutusu en çok bu kadar geniş
TANECIK_ARA = 28.0  # paneller arası
TANECIK_YAY = 18.0  # hal değişimi yayının yüksekliği
# Sıvı: dipten satır satır tanecik x konumları (d biriminde, kutu ortasına göre); satır arası d.
TANECIK_SIVI = ((-2.0, -1.0, 0.0, 1.0, 2.0), (-1.7, -0.4, 0.7, 1.8), (-1.3, 0.1, 1.2))
# Gaz: iç alanda (0..1) seyrek konumlar ve motion okunun yönü (derece, ekran ekseni).
TANECIK_GAZ = ((0.18, 0.22), (0.62, 0.14), (0.86, 0.42), (0.40, 0.48), (0.14, 0.70), (0.66, 0.76), (0.38, 0.88))
TANECIK_GAZ_YON = (230, 340, 80, 335, 110, 20, 315)


def _tam_mi(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _model_hatalari(fig: dict) -> list:
    """1.6 model: cebir karoları, sayma pulları (+/−, sıfır çifti), eşit kollu terazi."""
    arac = fig.get("tool")
    if arac not in MODEL_ARAC:
        return [f"model: tool ∈ {'|'.join(MODEL_ARAC)} olmalı"]
    h = []
    dolu = lambda v: isinstance(v, str) and bool(v.strip())
    if "variable" in fig and not (isinstance(fig["variable"], str) and len(fig["variable"]) == 1
                                  and "a" <= fig["variable"] <= "z"):
        h.append("model: variable tek küçük harf (a-z) olmalı")
    if arac == "balance":
        if "groups" in fig or "operators" in fig:
            h.append("model: balance ile groups/operators yazılmaz (kefeler left/right)")
        if fig.get("tilt", "level") not in MODEL_EGIM:
            h.append("model: tilt ∈ level|left|right olmalı")
        for taraf in ("left", "right"):
            kefe = fig.get(taraf)
            if not isinstance(kefe, list) or not 1 <= len(kefe) <= MODEL_KEFE_OGE:
                h.append(f"model: {taraf} 1..{MODEL_KEFE_OGE} öğeli liste olmalı")
                continue
            toplam = 0
            for i, oge in enumerate(kefe):
                if not isinstance(oge, dict) or set(oge) - {"item", "count", "labelKey", "color"}:
                    h.append(f"model: {taraf}[{i}] yalnız item/count/labelKey/color içerebilir")
                    continue
                tur = oge.get("item")
                if tur not in ("x", "unit", "weight", "object"):
                    h.append(f"model: {taraf}[{i}].item ∈ x|unit|weight|object olmalı")
                    continue
                ust = 12 if tur in ("x", "unit") else 4
                adet = oge.get("count", 1)
                if not _tam_mi(adet) or not 1 <= adet <= ust:
                    h.append(f"model: {taraf}[{i}].count 1..{ust} tam sayı olmalı")
                else:
                    toplam += adet
                if tur in ("weight", "object") and not dolu(oge.get("labelKey")):
                    h.append(f"model: {taraf}[{i}] {tur} için labelKey zorunlu")
                if tur in ("x", "unit") and "labelKey" in oge:
                    h.append(f"model: {taraf}[{i}] x/unit adsızdır (harf variable, birim 1)")
                if "color" in oge and (tur != "object" or oge["color"] not in DIAGRAM_RENK or oge["color"] == "none"):
                    h.append(f"model: {taraf}[{i}].color yalnız object için, beyaz listeden")
            if toplam > MODEL_KEFE_TOPLAM:
                h.append(f"model: {taraf} kefesinde en çok {MODEL_KEFE_TOPLAM} nesne")
        return h
    if any(a in fig for a in ("left", "right", "tilt")):
        h.append("model: left/right/tilt yalnız balance ile yazılır")
    gruplar = fig.get("groups")
    if not isinstance(gruplar, list) or not 1 <= len(gruplar) <= MODEL_GRUP:
        return h + [f"model: groups 1..{MODEL_GRUP} öğeli liste olmalı"]
    islemler = fig.get("operators", [""] * (len(gruplar) - 1))
    if not isinstance(islemler, list) or len(islemler) != len(gruplar) - 1 or any(
            i not in MODEL_ISLEM and i != "" for i in islemler):
        h.append("model: operators grup sayısı − 1 öğe, her biri + | - | = | \"\" olmalı")
    toplam = 0
    for i, gr in enumerate(gruplar):
        alanlar = set(MODEL_KARO) if arac == "tiles" else {"positive", "negative", "zeroPairs"}
        if not isinstance(gr, dict) or set(gr) - alanlar - {"labelKey"}:
            h.append(f"model: groups[{i}] yalnız {'/'.join(sorted(alanlar))}/labelKey içerebilir")
            continue
        if "labelKey" in gr and not dolu(gr["labelKey"]):
            h.append(f"model: groups[{i}].labelKey boş olamaz")
        if arac == "tiles":
            sayilar = {k: gr.get(k, 0) for k in MODEL_KARO}
            if not all(_tam_mi(v) and abs(v) <= MODEL_KARO[k] for k, v in sayilar.items()):
                h.append(f"model: groups[{i}] karo sayıları tam sayı; |x2| ≤ 4, |x| ≤ 10, |1| ≤ 10")
                continue
            if not any(sayilar.values()):
                h.append(f"model: groups[{i}] en az bir karo içermeli")
            toplam += sum(abs(v) for v in sayilar.values())
        else:
            p, n, z = gr.get("positive", 0), gr.get("negative", 0), gr.get("zeroPairs", 0)
            if not all(_tam_mi(v) and 0 <= v <= MODEL_PUL for v in (p, n)) or not _tam_mi(z):
                h.append(f"model: groups[{i}] positive/negative 0..{MODEL_PUL} tam sayı olmalı")
                continue
            if p + n == 0:
                h.append(f"model: groups[{i}] en az bir pul içermeli")
            if not 0 <= z <= min(p, n):
                h.append(f"model: groups[{i}].zeroPairs 0..min(positive, negative) olmalı")
            toplam += p + n
    ust = MODEL_KARO_TOPLAM if arac == "tiles" else MODEL_PUL_TOPLAM
    if toplam > ust:
        h.append(f"model: toplam en çok {ust} {'karo' if arac == 'tiles' else 'pul'}")
    return h


def _sekil(t, role, pts, fill=None, stroke=None, text=None, r=0.0, dash=False, width=1.5):
    return {"t": t, "role": role, "pts": [float(v) for v in pts], "fill": fill, "stroke": stroke,
            "text": text, "r": float(r), "dash": dash, "width": float(width)}


def _model_kolonlar(fig: dict, s: float, olc) -> tuple:
    """tiles/counters: grup başına kolon listesi [(genişlik, tür, işaret, adet)], kolon boyu, aralık."""
    karo = fig["tool"] == "tiles"
    g = 4.0 if karo else 8.0
    gruplar = fig["groups"]
    if karo:
        L = 2.5 * s
        H = L if any(gr.get("x2") or gr.get("x") for gr in gruplar) else 2 * s + g
    else:
        H = 2 * s + g
    sonuc = []
    for gr in gruplar:
        kol = []
        if karo:
            for tur, gen in (("x2", 2.5 * s), ("x", s)):
                n = gr.get(tur, 0)
                kol += [(gen, tur, -1 if n < 0 else 1, 1)] * abs(n)
            n = gr.get("1", 0)
            kol += [(s, "1", -1 if n < 0 else 1, min(2, abs(n) - k)) for k in range(0, abs(n), 2)]
        else:
            p, n, z = gr.get("positive", 0), gr.get("negative", 0), gr.get("zeroPairs", 0)
            kol += [(s, "pair", 0, 2)] * z
            kol += [(s, "pos", 1, min(2, p - z - k)) for k in range(0, p - z, 2)]
            kol += [(s, "neg", -1, min(2, n - z - k)) for k in range(0, n - z, 2)]
        sonuc.append(kol)
    return sonuc, H, g


def _model_dizilim(fig: dict, s: float, w: float, label, olc) -> dict:
    """Kolonları satırlara böler: grup içi satır kaydırma, gruplar ve işlemler satır satır."""
    kolonlar, H, g = _model_kolonlar(fig, s, olc)
    wmax = w - 32
    _, lh = olc("Ag")
    n = len(kolonlar)
    islemler = fig.get("operators") or [""] * (n - 1)
    bloklar = []
    for i, kol in enumerate(kolonlar):
        satirlar, sat, gen = [], [], 0.0
        for k in kol:
            ek = k[0] if not sat else gen + g + k[0]
            if sat and ek > wmax:
                satirlar.append((sat, gen)); sat, gen = [k], k[0]
            else:
                sat.append(k); gen = ek
        if sat:
            satirlar.append((sat, gen))
        ad = label(fig["groups"][i]["labelKey"]) if fig["groups"][i].get("labelKey") else ""
        bw = max([sg for _, sg in satirlar] + [olc(ad)[0] if ad else 0.0])
        bh = len(satirlar) * H + (len(satirlar) - 1) * 8 + (lh + 6 if ad else 0)
        bloklar.append({"lines": satirlar, "w": bw, "h": bh, "label": ad})
    ara = [olc(MODEL_ISLEM[o])[0] + 24 if o else 24.0 for o in islemler]
    # Satır kırılınca işlem işareti yeni satırın başına geçer; işlemsiz boşluk satır başında düşer.
    sira, sat, gen = [], [], 0.0
    for i, b in enumerate(bloklar):
        on = ara[i - 1] if i else 0.0
        if sat and gen + on + b["w"] > wmax:
            sira.append((sat, gen)); sat, gen = [], 0.0
            on = ara[i - 1] if islemler[i - 1] else 0.0
        sat.append(i)
        gen += on + b["w"]
    if sat:
        sira.append((sat, gen))
    satirlar = [(blok_idx, gen, max(bloklar[i]["h"] for i in blok_idx)) for blok_idx, gen in sira]
    toplam = sum(r[2] for r in satirlar) + 12 * (len(satirlar) - 1)
    return {"blocks": bloklar, "rows": satirlar, "H": H, "g": g, "ops": islemler, "gaps": ara,
            "height": toplam, "widest": max(k[0] for kol in kolonlar for k in kol),
            "split": any(len(b["lines"]) > 1 for b in bloklar)}


def _model_karo_kolon(fig, k, x0, y0, s, g, H) -> list:
    """Tek kolonun şekilleri: karo (x², x, 1) ya da pul (+, −, sıfır çifti)."""
    gen, tur, isaret, adet = k
    v = fig.get("variable") or "x"
    eksi = "\u2212" if isaret < 0 else ""
    out = []
    if tur in ("x2", "x"):
        boy = 2.5 * s
        dolgu = "danger-soft" if isaret < 0 else ("blue-soft" if tur == "x2" else "success-soft")
        out.append(_sekil("rect", "tile-" + tur, (x0, y0, x0 + gen, y0 + boy), dolgu, "ink"))
        out.append(_sekil("text", "tile-text", (x0 + gen / 2, y0 + boy / 2), text=eksi + v + ("\u00b2" if tur == "x2" else ""), fill="ink"))
    elif tur == "1":
        for j in range(adet):
            y = y0 + j * (s + g)
            out.append(_sekil("rect", "tile-1", (x0, y, x0 + s, y + s), "danger-soft" if isaret < 0 else "gold-soft", "ink"))
            out.append(_sekil("text", "tile-text", (x0 + s / 2, y + s / 2), text=eksi + "1", fill="ink"))
    else:
        if tur == "pair":
            out.append(_sekil("rect", "zero-pair", (x0 - 3, y0 - 3, x0 + s + 3, y0 + 2 * s + g + 3), None, "muted", dash=True, width=1.0))
        for j in range(adet):
            arti = tur == "pos" or (tur == "pair" and j == 0)
            cy = y0 + j * (s + g) + s / 2
            out.append(_sekil("circle", "counter-pos" if arti else "counter-neg", (x0 + s / 2, cy),
                              "gold" if arti else "danger", "ink", r=s / 2))
            out.append(_sekil("text", "counter-text", (x0 + s / 2, cy), text="+" if arti else "\u2212",
                              fill="ink" if arti else "white"))
    return out


def _model_gruplu(fig: dict, w: float, h: float, label, olc) -> dict:
    v = fig.get("variable") or "x"
    tw, th = olc("Ag")
    if fig["tool"] == "tiles":
        smin = max(olc("\u22121")[0], olc("\u2212" + v)[0], th) + 8
    else:
        smin = max(olc("+")[0], olc("\u2212")[0], th) + 8
    smax = max(smin, 44.0)

    def sigar(s, kat):
        d = _model_dizilim(fig, s, w, label, olc)
        return (d["height"] <= h - 32 and d["widest"] <= w - 32 and not (kat < 2 and d["split"])
                and not (kat == 0 and len(d["rows"]) > 1))

    # Önce tek satır ve bölünmemiş gruplarla en büyük birim; olmazsa gruplar alt satıra geçer;
    # o da olmazsa grup kendi içinde bölünür; hiçbiri sığmazsa en küçük birim (Android uzar).
    s = smin
    for kat in (0, 1, 2):
        if sigar(smax, kat):
            s = smax
            break
        if sigar(smin, kat):
            alt, ust = smin, smax
            for _ in range(30):
                orta = (alt + ust) / 2
                alt, ust = (orta, ust) if sigar(orta, kat) else (alt, orta)
            s = alt
            break
    d = _model_dizilim(fig, s, w, label, olc)
    H, g = d["H"], d["g"]
    out = []
    y = max(16.0, (h - d["height"]) / 2)
    for blok_idx, gen, rh in d["rows"]:
        x = (w - gen) / 2
        for i in blok_idx:
            b = d["blocks"][i]
            if i and (i != blok_idx[0] or d["ops"][i - 1]):
                if d["ops"][i - 1]:
                    out.append(_sekil("text", "operator", (x + d["gaps"][i - 1] / 2, y + H / 2),
                                      text=MODEL_ISLEM[d["ops"][i - 1]], fill="ink"))
                x += d["gaps"][i - 1]
            for li, (sat, sg) in enumerate(b["lines"]):
                kx = x + (b["w"] - sg) / 2
                ly = y + li * (H + 8)
                for k in sat:
                    out += _model_karo_kolon(fig, k, kx, ly, s, g, H)
                    kx += k[0] + g
            if b["label"]:
                out.append(_sekil("text", "group-label", (x + b["w"] / 2, y + b["h"] - th / 2), text=b["label"], fill="ink"))
            x += b["w"]
        y += rh + 12
    return {"shapes": out, "height": d["height"] + 32, "unit": s}


def _model_terazi(fig: dict, w: float, h: float, label, olc) -> dict:
    """Eşit kollu terazi: kefeler kol uçlarında üstte; nesneler kefede alttan yukarı dizilir."""
    v = fig.get("variable") or "x"
    _, th = olc("Ag")
    s = max(olc("1")[0], th) + 8
    sx = max(1.6 * s, olc(v)[0] + 12)
    P = min((w - 48) / 2, 180.0)
    D = P / 2 + 8
    cx = w / 2

    def ogeler(kefe):
        liste = []
        for oge in kefe:
            tur, adet = oge["item"], oge.get("count", 1)
            for _ in range(adet):
                if tur == "x":
                    liste.append((tur, sx, sx, v, "success-soft"))
                elif tur == "unit":
                    liste.append((tur, s, s, "1", "gold-soft"))
                else:
                    yazi = label(oge["labelKey"])
                    dolgu = "muted-soft" if tur == "weight" else oge.get("color", "blue-soft")
                    liste.append((tur, olc(yazi)[0] + (18 if tur == "weight" else 14), th + 10, yazi, dolgu))
        satirlar, sat, gen = [], [], 0.0
        for o in liste:
            ek = o[1] if not sat else gen + 3 + o[1]
            if sat and ek > P - 8:
                satirlar.append((sat, gen)); sat, gen = [o], o[1]
            else:
                sat.append(o); gen = ek
        if sat:
            satirlar.append((sat, gen))
        return satirlar, sum(max(o[2] for o in r) for r, _ in satirlar) + 3 * (len(satirlar) - 1)

    sol, sag = ogeler(fig["left"]), ogeler(fig["right"])
    aci = math.radians(MODEL_EGIM[fig.get("tilt", "level")])
    dl, dr = D * math.sin(aci), -D * math.sin(aci)  # kol ucunun pivota göre aşağı inişi
    pivot = 16 + max(sol[1] + 22 - dl, sag[1] + 22 - dr)
    taban = pivot + max(dl, dr, 0.0) + 60
    gerek = taban + 10 + 16
    kay = max(0.0, (h - gerek) / 2)
    pivot += kay; taban += kay
    out = [
        _sekil("rect", "stand", (cx - 50, taban, cx + 50, taban + 10), "muted-soft", "ink"),
        _sekil("line", "stand", (cx, pivot, cx, taban), stroke="ink", width=5.0),
    ]
    for isaret, (satirlar, _), dy in ((-1, sol, dl), (1, sag, dr)):
        ex, ey = cx + isaret * D, pivot + dy
        tabla = ey - 14
        out.append(_sekil("line", "pan-post", (ex, ey, ex, tabla), stroke="ink", width=3.0))
        out.append(_sekil("poly", "pan", (ex - P / 2, tabla - 8, ex + P / 2, tabla - 8, ex + P / 2 - 10, tabla,
                                          ex - P / 2 + 10, tabla), "muted-soft", "ink"))
        y = tabla - 8
        for sat, gen in satirlar:
            rh = max(o[2] for o in sat)
            x = ex - gen / 2
            for tur, ow, oh, yazi, dolgu in sat:
                y0 = y - oh
                if tur == "weight":
                    out.append(_sekil("poly", "item-weight", (x + 5, y0, x + ow - 5, y0, x + ow, y, x, y), dolgu, "ink"))
                else:
                    out.append(_sekil("rect", "item-" + tur, (x, y0, x + ow, y), dolgu, "ink"))
                out.append(_sekil("text", "item-text", (x + ow / 2, y0 + oh / 2), text=yazi, fill="ink"))
                x += ow + 3
            y -= rh + 3
    out.append(_sekil("line", "beam", (cx - D, pivot + dl, cx + D, pivot + dr), stroke="ink", width=5.0))
    out.append(_sekil("circle", "pivot", (cx, pivot), "gold", "ink", r=6))
    return {"shapes": out, "height": gerek, "unit": s}


def model_layout(fig: dict, w: float, h: float, label, olc) -> dict:
    """1.6 model ortak tarifi (Android `FigureMath.modelLayout` aynası).

    label(anahtar) -> yazı, olc(yazı) -> (genişlik, satır yüksekliği). Dönen "shapes" sırayla boyanır:
    t ∈ rect (pts x0,y0,x1,y1) | circle (pts cx,cy; r) | poly | line (pts düz liste) | text (pts merkez).
    "height": yazı küçültülmeden gereken tuval yüksekliği. Karo/pul birimi sığana dek küçülür
    (yazı sığacak en küçük değere kadar); sığmayan gruplar ve kolonlar alt satıra geçer.
    """
    if fig["tool"] == "balance":
        return _model_terazi(fig, w, h, label, olc)
    return _model_gruplu(fig, w, h, label, olc)


def _olcu_hatalari(fig: dict) -> list:
    """1.6 instrument: termometre, dinamometre, dereceli silindir (eşit kollu terazi model/balance)."""
    arac = fig.get("tool")
    if arac not in OLCU_ARAC:
        return [f"instrument: tool ∈ {'|'.join(OLCU_ARAC)} olmalı"]
    lo, hi, adim = fig.get("min"), fig.get("max"), fig.get("step")
    if not all(_sayi_mi(v) and abs(v) <= OLCU_SINIR for v in (lo, hi, adim)) or not lo < hi or adim <= 0:
        return [f"instrument: min < max ve step > 0 sayı olmalı (|değer| ≤ {OLCU_SINIR})"]
    h = []
    n = (hi - lo) / adim
    if abs(n - round(n)) > 1e-6 or not 2 <= round(n) <= OLCU_ARALIK:
        h.append(f"instrument: (max − min) / step 2..{OLCU_ARALIK} tam sayı olmalı")
    alt = fig.get("minor", 1)
    if not _tam_mi(alt) or not 1 <= alt <= OLCU_ALT or round(n) * alt > OLCU_CENTIK:
        h.append(f"instrument: minor 1..{OLCU_ALT} tam sayı, toplam çentik ≤ {OLCU_CENTIK} olmalı")
        alt = 1
    if arac != "thermometer" and lo < 0:
        h.append("instrument: dynamometer ve cylinder için min ≥ 0 olmalı")
    if fig.get("unit", OLCU_ARAC[arac][0]) not in OLCU_ARAC[arac]:
        h.append(f"instrument: {arac} birimi {'|'.join(OLCU_ARAC[arac])} olmalı")
    okumalar = fig.get("readings")
    if not isinstance(okumalar, list) or not 1 <= len(okumalar) <= OLCU_OKUMA:
        return h + [f"instrument: readings 1..{OLCU_OKUMA} öğeli liste olmalı"]
    birim = adim / alt
    for i, o in enumerate(okumalar):
        if not isinstance(o, dict) or not set(o) <= OLCU_OKUMA_ALAN or "value" not in o:
            h.append(f"instrument: readings[{i}] yalnız value/objectKey/labelKey içerir (value zorunlu)")
            continue
        v = o["value"]
        if not _sayi_mi(v) or not lo - 1e-9 <= v <= hi + 1e-9:
            h.append(f"instrument: readings[{i}].value min..max aralığında sayı olmalı")
        elif abs((v - lo) / birim - round((v - lo) / birim)) > 1e-6:
            h.append(f"instrument: readings[{i}].value bir çentiğe denk gelmeli (step/minor katı)")
        elif "objectKey" in o and arac == "cylinder" and v - lo < (hi - lo) / 4 - 1e-9:
            h.append(f"instrument: readings[{i}] cismi sıvıda kalmalı: value ≥ min + (max − min)/4")
        for alan in ("objectKey", "labelKey"):
            if alan in o and (not isinstance(o[alan], str) or not o[alan].strip()):
                h.append(f"instrument: readings[{i}].{alan} boş olamaz")
        if "objectKey" in o and arac == "thermometer":
            h.append(f"instrument: readings[{i}].objectKey yalnız dynamometer/cylinder ile yazılır")
    return h


def instrument_layout(fig: dict, w: float, h: float, label, olc, sayi) -> dict:
    """1.6 instrument ortak tarifi (Android `FigureMath.instrumentLayout` aynası).

    label(anahtar) -> yazı, olc(yazı) -> (genişlik, satır yüksekliği), sayi(değer) -> dilin ondalık
    yazısı. Ölçek boyu L ana aralık başına en az bir satır + 4, alt çentik başına en az 5 px olur; yer
    varsa en çok 300'e uzar. Termometre ve silindirde değer yukarı, dinamometrede aşağı artar. Araçlar
    yan yana dizilir, sığmayan alt satıra geçer; "height" yazı küçültülmeden gereken yükseklik.
    Şekiller model_layout ile aynı biçimdedir.
    """
    arac = fig["tool"]
    lo, hi, adim = float(fig["min"]), float(fig["max"]), float(fig["step"])
    n = round((hi - lo) / adim)
    alt = fig.get("minor", 1)
    birim = fig.get("unit") or OLCU_ARAC[arac][0]
    _, th = olc("Ag")
    sayilar = [(lo + k * adim, sayi(lo + k * adim)) for k in range(n + 1)]
    nw = max(olc(t)[0] for t in [s for _, s in sayilar] + [birim])
    okumalar = fig["readings"]
    nesne = [label(o["objectKey"]) if "objectKey" in o else "" for o in okumalar]
    adlar = [label(o["labelKey"]) if "labelKey" in o else "" for o in okumalar]
    ow = [olc(t)[0] + 16 if t else 0.0 for t in nesne]
    oh = th + 10
    ust = 8 + max(1.5 * th + 6, {"thermometer": 19.0, "cylinder": 20.0, "dynamometer": 50.0}[arac])
    L = max(n * (th + 4), n * alt * OLCU_ALT_ARALIK)
    if arac == "thermometer":
        govde = 35.0
        uclar = [(-13.0, 31 + nw) for _ in okumalar]
    elif arac == "cylinder":
        govde = 8.0
        gw = [max(48.0, o + 36) for o in ow]
        uclar = [(-g / 2 - 16 - nw, g / 2 + 12) for g in gw]  # sayılar taban ucunun solunda
        for o, t in zip(okumalar, nesne):
            if t:
                L = max(L, (oh + 6) * (hi - lo) / (o["value"] - lo))
    else:
        govde = 41.0 + (6 + oh if any(nesne) else 0.0)
        uclar = [(min(-21 - nw, 2 - o / 2), max(15.0, 2 + o / 2)) for o in ow]
    uclar = [(min(a, -olc(t)[0] / 2), max(b, olc(t)[0] / 2)) if t else (a, b) for (a, b), t in zip(uclar, adlar)]
    alt_pay = govde + (6 + th if any(adlar) else 0.0) + 8
    genis = [b - a for a, b in uclar]
    satirlar, sat, gen = [], [], 0.0
    for i, cw in enumerate(genis):
        ek = cw if not sat else gen + 28 + cw
        if sat and ek > w - 16:
            satirlar.append((sat, gen)); sat, gen = [i], cw
        else:
            sat.append(i); gen = ek
    satirlar.append((sat, gen))
    r = len(satirlar)
    L = max(L, min(300.0, (h - 16 * (r - 1)) / r - ust - alt_pay))
    sat_h = ust + L + alt_pay
    gerek = r * sat_h + 16 * (r - 1)
    y_sat = max(0.0, (h - gerek) / 2)
    out = []
    for sat, gen in satirlar:
        x = (w - gen) / 2
        ys = y_sat + ust
        for i in sat:
            cx = x - uclar[i][0]
            x += genis[i] + 28
            v = float(okumalar[i]["value"])
            oran = lambda d: (d - lo) / (hi - lo) * L
            yv = (lambda d: ys + oran(d)) if arac == "dynamometer" else (lambda d: ys + L - oran(d))
            if arac == "thermometer":
                ty, by = ys - 12, ys + L + 22
                tup = [cx - 7, by]
                for k in range(9):
                    a = math.pi * (1 - k / 8)
                    tup += [cx + 7 * math.cos(a), ty - 7 * math.sin(a)]
                out.append(_sekil("poly", "tube", tup + [cx + 7, by], "paper", "ink", width=2.0))
                out.append(_sekil("circle", "bulb", (cx, by), "danger", "ink", r=13, width=2.0))
                out.append(_sekil("rect", "liquid", (cx - 3, yv(v), cx + 3, by), "danger"))
                cizgi_x, sayi_x = cx + 7, cx + 24
                alt_y = by + 13
            elif arac == "cylinder":
                g = gw[i]
                gx0, gx1, bot, top = cx - g / 2, cx + g / 2, ys + L, ys - 14
                out.append(_sekil("rect", "glass-back", (gx0, top, gx1, bot), "paper"))
                if v > lo:
                    egri = []
                    for k in range(13):
                        egri += [gx0 + g * k / 12, yv(v) - 4 * (k / 6 - 1) ** 2]
                    out.append(_sekil("poly", "liquid", egri + [gx1, bot, gx0, bot], "blue-soft"))
                    out.append(_sekil("line", "meniscus", egri, stroke="blue", width=2.0))
                if nesne[i]:
                    x0, x1, y0, y1 = cx - ow[i] / 2, cx + ow[i] / 2, bot - 2 - oh, bot - 2
                    out.append(_sekil("poly", "object", (x0 + 5, y0, x1 - 5, y0, x1, y0 + 5, x1, y1 - 5, x1 - 5, y1,
                                                         x0 + 5, y1, x0, y1 - 5, x0, y0 + 5), "muted-soft", "ink"))
                    out.append(_sekil("text", "object-text", (cx, y0 + oh / 2), text=nesne[i], fill="ink"))
                cizgi_x, sayi_x = gx0, gx0 - 16 - nw
                alt_y = bot + 8
            else:
                y0, y1, yp = ys, ys + L, yv(v)
                out.append(_sekil("circle", "ring", (cx, y0 - 43), None, "ink", r=7, width=2.0))
                out.append(_sekil("rect", "body", (cx - 15, y0 - 36, cx + 15, y1 + 14), "paper", "ink", width=2.0))
                yay = [cx + 6, y0 - 36]
                for k in range(1, 12):
                    yay += [cx + 6 + (5 if k % 2 else -5), y0 - 36 + (yp - y0 + 36) * k / 12]
                out.append(_sekil("line", "spring", yay + [cx + 6, yp], stroke="muted", width=1.5))
                hy = y1 + 32
                out.append(_sekil("line", "rod", (cx + 6, yp, cx + 6, hy), stroke="ink", width=2.0))
                kanca = [cx + 6, hy]
                for k in range(9):
                    a = (math.pi + 0.6) * k / 8
                    kanca += [cx + 2 + 4 * math.cos(a), hy + 5 + 4 * math.sin(a)]
                out.append(_sekil("line", "hook", kanca, stroke="ink", width=2.0))
                alt_y = hy + 9
                if nesne[i]:
                    out.append(_sekil("line", "hook", (cx + 2, hy + 9, cx + 2, hy + 15), stroke="ink", width=1.5))
                    x0, x1 = cx + 2 - ow[i] / 2, cx + 2 + ow[i] / 2
                    out.append(_sekil("rect", "object", (x0, hy + 15, x1, hy + 15 + oh), "gold-soft", "ink"))
                    out.append(_sekil("text", "object-text", (cx + 2, hy + 15 + oh / 2), text=nesne[i], fill="ink"))
                    alt_y = hy + 15 + oh
                cizgi_x, sayi_x = cx - 15, cx - 21 - nw
            for k in range(n * alt + 1):
                yk = yv(lo + k * (hi - lo) / (n * alt))
                ana = k % alt == 0
                boy = (14 if arac == "cylinder" else 12) if ana else (7 if arac == "cylinder" else 6)
                out.append(_sekil("line", "tick-major" if ana else "tick-minor", (cizgi_x, yk, cizgi_x + boy, yk),
                                  stroke="ink", width=2.0 if ana else 1.0))
            # Sayı sütunu [sayi_x, sayi_x + nw]: termometrede sola, ötekilerde sağa yaslı.
            for d, t in sayilar:
                tw = olc(t)[0]
                sx = sayi_x + tw / 2 if arac == "thermometer" else sayi_x + nw - tw / 2
                out.append(_sekil("text", "number", (sx, yv(d)), text=t, fill="ink"))
            out.append(_sekil("text", "unit", (sayi_x + nw / 2, ys - th - 6), text=birim, fill="ink"))
            if arac == "cylinder":
                out.append(_sekil("line", "glass", (gx0 - 5, top - 4, gx0, top, gx0, bot, gx1, bot, gx1, top, gx1 + 5, top - 4),
                                  stroke="ink", width=2.0))
                out.append(_sekil("rect", "base", (gx0 - 12, bot, gx1 + 12, bot + 8), "muted-soft", "ink"))
            if arac == "dynamometer":
                out.append(_sekil("line", "pointer", (cx - 15, yv(v), cx + 13, yv(v)), stroke="danger", width=3.0))
            if adlar[i]:
                out.append(_sekil("text", "label", (cx, alt_y + 6 + th / 2), text=adlar[i], fill="ink"))
        y_sat += sat_h + 16
    return {"shapes": out, "height": gerek, "unit": L}


def _isik_hatalari(fig: dict) -> list:
    """1.6 light: düz aynada yansıma (mirror), iki ortam sınırında kırılma (boundary)."""
    yuzey = fig.get("surface")
    if yuzey not in ISIK_YUZEY:
        return [f"light: surface ∈ {'|'.join(ISIK_YUZEY)} olmalı"]
    gelme = fig.get("incidence")
    if not _sayi_mi(gelme) or not 0 <= gelme <= ISIK_GELME:
        return [f"light: incidence 0..{ISIK_GELME} derece olmalı"]
    h = []
    sinir = yuzey == "boundary"
    kirilma = None
    if sinir:
        kirilma = fig.get("refracted")
        if not _sayi_mi(kirilma) or not 0 <= kirilma <= ISIK_KIRILMA:
            h.append(f"light: boundary için refracted 0..{ISIK_KIRILMA} derece zorunlu")
            kirilma = None
        yogun = fig.get("denser")
        if "denser" in fig and yogun not in ISIK_YOGUN:
            h.append("light: denser top|bottom olmalı")
        elif gelme == 0:
            if kirilma not in (None, 0):
                h.append("light: incidence 0 iken refracted 0 olmalı (dik gelen ışın kırılmaz)")
        elif yogun is None:
            h.append("light: boundary için denser top|bottom zorunlu")
        elif kirilma is not None and (kirilma >= gelme if yogun == "bottom" else kirilma <= gelme):
            h.append("light: yoğun ortama geçen ışın normale yaklaşır (refracted < incidence), "
                     "az yoğun ortama geçen uzaklaşır")
        if "reflected" in fig and not isinstance(fig["reflected"], bool):
            h.append("light: reflected true|false olmalı")
        ortam = fig.get("mediumKeys")
        if "mediumKeys" in fig and (not isinstance(ortam, list) or len(ortam) != 2
                                    or not all(isinstance(k, str) and k.strip() for k in ortam)):
            h.append("light: mediumKeys [üst, alt] iki dolu ad olmalı")
    else:
        for alan in ("refracted", "denser", "reflected", "mediumKeys"):
            if alan in fig:
                h.append(f"light: {alan} yalnız surface=boundary ile yazılır")
    var = {"incidence": True, "reflection": not sinir or fig.get("reflected") is True, "refraction": sinir}
    olcu = {"incidence": gelme, "reflection": gelme, "refraction": kirilma}
    for alan, adlar in (("angleKeys", ISIK_ACI), ("rayKeys", ISIK_ISIN)):
        if alan not in fig:
            continue
        d = fig[alan]
        if (not isinstance(d, dict) or not d or not set(d) <= set(adlar)
                or not all(isinstance(v, str) and v.strip() for v in d.values())):
            h.append(f"light: {alan} yalnız {'/'.join(adlar)} anahtarlı dolu adlar içerir")
            continue
        for k in d:
            aci = ISIK_ACI[ISIK_ISIN.index(k)] if alan == "rayKeys" else k
            if not var[aci]:
                h.append(f"light: {alan}.{k} çizilmeyen ışın/açı için yazılamaz")
            elif alan == "angleKeys" and olcu[aci] is not None and olcu[aci] < ISIK_AD_EN_AZ:
                h.append(f"light: angleKeys.{k} için açı en az {ISIK_AD_EN_AZ}° olmalı (ad yayın içine sığar)")
    if "normalKey" in fig and (not isinstance(fig["normalKey"], str) or not fig["normalKey"].strip()):
        h.append("light: normalKey boş olamaz")
    return h


def _kutu_kesisir(kutu, a, b) -> bool:
    """ab doğru parçası (x0, y0, x1, y1) kutusuna değiyor mu (Liang-Barsky)."""
    x0, y0, x1, y1 = kutu
    dx, dy = b[0] - a[0], b[1] - a[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
        if abs(p) < 1e-12:
            if q < 0:
                return False
        else:
            t = q / p
            if p < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def light_layout(fig: dict, w: float, h: float, label, olc) -> dict:
    """1.6 light ortak tarifi (Android `FigureMath.lightLayout` aynası).

    Işınlar çarpma noktası P'den R uzunlukta; gelen ışın sol üstten gelir, yansıyan sağ üste,
    kırılan sağ alta gider. Açı adı açıortay üzerinde iki kola da değmeyene dek dışarı itilir;
    ışın adı ışının ucunda, ortam adları yüzeyin hemen üstü/altında ışınlara değmeyen ilk köşede.
    R ışın adları genişliğe sığacak kadar kısalır (en az 60); yazı küçülmez, görünüm uzar.
    Şekiller model_layout ile aynı biçimdedir.
    """
    sinir = fig["surface"] == "boundary"
    gelme = math.radians(fig["incidence"])
    kirilma = math.radians(fig.get("refracted", 0)) if sinir else 0.0
    yansiyan = not sinir or fig.get("reflected") is True
    _, th = olc("Ag")

    def boyut(key):
        return olc(label(key))[0] / 2 + 3, th / 2 + 1

    yon = {"incident": (-math.sin(gelme), -math.cos(gelme)), "reflected": (math.sin(gelme), -math.cos(gelme)),
           "refracted": (math.sin(kirilma), math.cos(kirilma))}
    isinlar = ["incident"] + (["reflected"] if yansiyan else []) + (["refracted"] if sinir else [])
    # Işın adları sabit sırada (Android JSONObject anahtar sırası tutmaz).
    isin_ad = {k: fig["rayKeys"][k] for k in ISIK_ISIN if k in fig.get("rayKeys", {})}
    R = min(w / 2 - 24, (h - 48) / 2 if sinir else h - 60)
    yari = h / 2 - 8 if sinir else h - 33  # yüzeyden üst (ve sınırda alt) kenara yer
    for k, key in isin_ad.items():
        ux, uy = yon[k]
        hw, hh = boyut(key)
        ek = hw * abs(ux) + hh * abs(uy) + 6
        if abs(ux) > 1e-6:
            R = min(R, (w / 2 - 8 - hw) / abs(ux) - ek)
        if abs(uy) > 1e-6:
            R = min(R, (yari - hh) / abs(uy) - ek)
    if fig.get("normalKey"):
        R = min(R, yari - 14 - 2 * boyut(fig["normalKey"])[1])
    R = max(R, 60.0)
    ra = min(36.0, R * 0.35)
    yukari, asagi = (0.0, -1.0), (0.0, 1.0)
    out, yazilar, kutular = [], [], []
    sol, sag = -w / 2 + 16, w / 2 - 16
    segler = [((0.0, 0.0), (R * ux, R * uy)) for ux, uy in (yon[k] for k in isinlar)]
    segler.append(((0.0, -R - 10), (0.0, R + 10 if sinir else 0.0)))
    # Açılar: (ad anahtarı, normal yönü, ışın yönü, derece)
    acilar = [("incidence", yukari, yon["incident"], fig["incidence"])]
    if yansiyan:
        acilar.append(("reflection", yukari, yon["reflected"], fig["incidence"]))
    if sinir:
        acilar.append(("refraction", asagi, yon["refracted"], fig.get("refracted", 0)))
    yaylar = []
    for ad, n, u, derece in acilar:
        if derece <= 0:
            continue
        a0, a1 = math.atan2(n[1], n[0]), math.atan2(u[1], u[0])
        fark = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        pts = []
        for k in range(13):
            a = a0 + fark * k / 12
            pts += [ra * math.cos(a), ra * math.sin(a)]
        yaylar.append(_sekil("line", "arc", pts, stroke="ink", width=1.5))
        key = fig.get("angleKeys", {}).get(ad)
        if key:
            hw, hh = boyut(key)
            bx, by = n[0] + u[0], n[1] + u[1]
            bl = math.hypot(bx, by)
            bx, by = bx / bl, by / bl
            d = ra + 4
            while d < 2000:
                kutu = (d * bx - hw, d * by - hh, d * bx + hw, d * by + hh)
                if not any(_kutu_kesisir(kutu, (0.0, 0.0), (5000 * v[0], 5000 * v[1])) for v in (n, u)):
                    break
                d += 2
            kutular.append(kutu)
            yazilar.append(("angle-label", d * bx, d * by, label(key)))
    for k, key in isin_ad.items():
        ux, uy = yon[k]
        hw, hh = boyut(key)
        e = R + hw * abs(ux) + hh * abs(uy) + 6
        kutular.append((e * ux - hw, e * uy - hh, e * ux + hw, e * uy + hh))
        yazilar.append(("ray-label", e * ux, e * uy, label(key)))
    if fig.get("normalKey"):
        hw, hh = boyut(fig["normalKey"])
        cy = -R - 10 - hh - 4
        kutular.append((-hw, cy - hh, hw, cy + hh))
        yazilar.append(("normal-label", 0.0, cy, label(fig["normalKey"])))
    if sinir and fig.get("mediumKeys"):
        for isaret, key in zip((-1, 1), fig["mediumKeys"]):
            hw, hh = boyut(key)
            adaylar = [(x, isaret * y) for y in (hh + 6, R / 2, R + 10) for x in (sol + 6 + hw, sag - 6 - hw)]
            secim = adaylar[0]
            for cx, cy in adaylar:
                kutu = (cx - hw, cy - hh, cx + hw, cy + hh)
                if (not any(_kutu_kesisir(kutu, a, b) for a, b in segler)
                        and not any(kutu[0] < k[2] + 2 and k[0] < kutu[2] + 2 and kutu[1] < k[3] + 2 and k[1] < kutu[3] + 2
                                    for k in kutular)):
                    secim = (cx, cy)
                    break
            kutular.append((secim[0] - hw, secim[1] - hh, secim[0] + hw, secim[1] + hh))
            yazilar.append(("medium-label", secim[0], secim[1], label(key)))
    ust = max([R + 10] + [-k[1] for k in kutular])
    alt = max([R + 10 if sinir else 9.0] + [k[3] for k in kutular])
    gerek = ust + alt + 16
    y0 = ust + 8 + max(0.0, (h - gerek) / 2)
    if sinir and fig.get("denser") in ISIK_YOGUN:
        uzun = R + 10
        out.append(_sekil("rect", "medium", (sol, 0.0, sag, uzun) if fig["denser"] == "bottom" else (sol, -uzun, sag, 0.0),
                          "blue-soft"))
    out.append(_sekil("line", "surface", (sol, 0.0, sag, 0.0), stroke="ink", width=2.0 if sinir else 3.0))
    if not sinir:
        x = sol + 8
        while x <= sag:
            out.append(_sekil("line", "hatch", (x, 0.0, x - 7, 9.0), stroke="muted", width=1.0))
            x += 10
    out.append(_sekil("line", "normal", (0.0, -R - 10, 0.0, R + 10 if sinir else 0.0), stroke="muted", dash=True, width=1.5))
    out.extend(yaylar)
    for k in isinlar:
        ux, uy = yon[k]
        out.append(_sekil("line", "ray-" + k, (0.0, 0.0, R * ux, R * uy), stroke="danger", width=2.5))
        dx, dy = (-ux, -uy) if k == "incident" else (ux, uy)
        mx, my = 0.55 * R * ux, 0.55 * R * uy
        out.append(_sekil("poly", "arrow", (mx + 7 * dx, my + 7 * dy, mx - 5 * dx - 5 * dy, my - 5 * dy + 5 * dx,
                                            mx - 5 * dx + 5 * dy, my - 5 * dy - 5 * dx), "danger"))
    for rol, x, y, yazi in yazilar:
        out.append(_sekil("text", rol, (x, y), text=yazi, fill="ink"))
    for s in out:
        s["pts"] = [v + (w / 2 if j % 2 == 0 else y0) for j, v in enumerate(s["pts"])]
    return {"shapes": out, "height": gerek, "unit": R}


def _tanecik_hatalari(fig: dict) -> list:
    """1.6 particles: katı/sıvı/gaz tanecik modeli panelleri ve aralarında hal değişimi okları."""
    paneller = fig.get("panels")
    if not isinstance(paneller, list) or not 1 <= len(paneller) <= TANECIK_PANEL:
        return [f"particles: panels 1..{TANECIK_PANEL} öğeli liste olmalı"]
    h = []
    for i, panel in enumerate(paneller):
        if not isinstance(panel, dict) or not set(panel) <= {"state", "labelKey"}:
            h.append(f"particles: panels[{i}] yalnız {{state, labelKey?}} içerir")
            continue
        if panel.get("state") not in TANECIK_HAL:
            h.append(f"particles: panels[{i}].state ∈ {'|'.join(TANECIK_HAL)} olmalı")
        if "labelKey" in panel and (not isinstance(panel["labelKey"], str) or not panel["labelKey"].strip()):
            h.append(f"particles: panels[{i}].labelKey boş olamaz")
    if "arrows" in fig:
        oklar = fig["arrows"]
        if not isinstance(oklar, list) or not 1 <= len(oklar) <= 2 * (len(paneller) - 1):
            h.append("particles: arrows 1..2·(panel − 1) öğeli liste olmalı")
            oklar = []
        gorulen = set()
        for i, ok in enumerate(oklar):
            if not isinstance(ok, dict) or not set(ok) <= {"from", "to", "labelKey"}:
                h.append(f"particles: arrows[{i}] yalnız {{from, to, labelKey?}} içerir")
                continue
            a, b = ok.get("from"), ok.get("to")
            if not (_tam_mi(a) and _tam_mi(b) and 0 <= a < len(paneller) and 0 <= b < len(paneller)
                    and abs(a - b) == 1):
                h.append(f"particles: arrows[{i}] from/to yan yana iki panelin sırası olmalı")
            elif (a, b) in gorulen:
                h.append(f"particles: arrows[{i}] aynı ok iki kez yazılamaz")
            gorulen.add((a, b))
            if "labelKey" in ok and (not isinstance(ok["labelKey"], str) or not ok["labelKey"].strip()):
                h.append(f"particles: arrows[{i}].labelKey boş olamaz")
    if "motion" in fig:
        if not isinstance(fig["motion"], bool):
            h.append("particles: motion true|false olmalı")
        elif fig["motion"] and not any(isinstance(p, dict) and p.get("state") == "gas" for p in paneller):
            h.append("particles: motion yalnız gas paneli varken yazılır")
    return h


def particles_layout(fig: dict, w: float, h: float, label, olc) -> dict:
    """1.6 particles ortak tarifi (Android `FigureMath.particlesLayout` aynası).

    Paneller yan yana kapalı kutulardır. Katıda 4×4 tanecik düzenli ve bitişik; sıvıda 5-4-3
    tanecik dipte, bitişik ama düzensiz sıralı; gazda 7 tanecik kutuya seyrek yayılır. Tanecik
    aralığı d (merkezden merkeze, 2r + 1) her satırda en az d olduğundan tanecikler örtüşmez.
    Hal değişimi okları ileri (from < to) kutuların üstünde, geri altta yaydır; adı yayın
    tepesinde, sığmazsa bir satır dışarı itilir. Kutu boyu genişlikten gelir; yazı küçülmez,
    görünüm uzar.
    """
    paneller = fig["panels"]
    n = len(paneller)
    _, th = olc("Ag")

    def boyut(key):
        return olc(label(key))[0] / 2 + 3, th / 2 + 1

    ara = TANECIK_ARA
    bw = min(TANECIK_KUTU, (w - 16 - ara * (n - 1)) / n)
    bh = bw * 0.8
    d = min(22.0, (bw - 12) / 5.4, (bh - 12) / 4.2)
    r = (d - 1) / 2
    x0 = (w - (n * bw + ara * (n - 1))) / 2
    merkez = [x0 + i * (bw + ara) + bw / 2 for i in range(n)]
    out, yazilar = [], []
    for i, panel in enumerate(paneller):
        sol, cx = merkez[i] - bw / 2, merkez[i]
        out.append(_sekil("rect", "box", (sol, 0.0, sol + bw, bh), "paper", "ink", width=2.0))
        taban = bh - 6 - r
        if panel["state"] == "solid":
            noktalar = [(cx + (k - 1.5) * d, taban - s * d) for s in range(4) for k in range(4)]
        elif panel["state"] == "liquid":
            noktalar = [(cx + x * d, taban - s * d) for s, satir in enumerate(TANECIK_SIVI) for x in satir]
        else:
            ic_w, ic_h = bw - 12 - 2 * r, bh - 12 - 2 * r
            noktalar = [(sol + 6 + r + u * ic_w, 6 + r + v * ic_h) for u, v in TANECIK_GAZ]
        for x, y in noktalar:
            out.append(_sekil("circle", "particle-" + panel["state"], (x, y), "blue", "ink", r=r, width=1.0))
        if panel["state"] == "gas" and fig.get("motion"):
            for (x, y), aci in zip(noktalar, TANECIK_GAZ_YON):
                ux, uy = math.cos(math.radians(aci)), math.sin(math.radians(aci))
                a, b = r + 2, r + 2 + 0.7 * d
                out.append(_sekil("line", "motion", (x + a * ux, y + a * uy, x + b * ux, y + b * uy),
                                  stroke="muted", width=1.5))
                tx, ty = x + (b + 3) * ux, y + (b + 3) * uy
                out.append(_sekil("poly", "motion-head", (tx, ty, tx - 6 * ux - 3 * uy, ty - 6 * uy + 3 * ux,
                                                          tx - 6 * ux + 3 * uy, ty - 6 * uy - 3 * ux), "muted"))
        if panel.get("labelKey"):
            hw, hh = boyut(panel["labelKey"])
            yazilar.append(("state-label", cx, bh + 4 + hh, hw, hh, label(panel["labelKey"])))
    alt_cizgi = bh + (4 + th + 4 if any(p.get("labelKey") for p in paneller) else 4)
    kutular = {-1: [], 1: []}
    for ok in sorted(fig.get("arrows", []), key=lambda o: (o["from"] > o["to"], min(o["from"], o["to"]))):
        a, b = ok["from"], ok["to"]
        yon = -1 if a < b else 1  # ileri üstte, geri altta
        y = -4.0 if yon < 0 else alt_cizgi
        p0 = (merkez[a] + (1 if b > a else -1) * bw * 0.2, y)
        p1 = (merkez[b] - (1 if b > a else -1) * bw * 0.2, y)
        cx_, cy_ = (p0[0] + p1[0]) / 2, y + yon * 2 * TANECIK_YAY
        pts = []
        for k in range(13):
            t = k / 12
            pts += [(1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * cx_ + t * t * p1[0],
                    (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * cy_ + t * t * p1[1]]
        out.append(_sekil("line", "change", pts, stroke="ink", width=2.0))
        ux, uy = p1[0] - cx_, p1[1] - cy_
        ul = math.hypot(ux, uy)
        ux, uy = ux / ul, uy / ul
        out.append(_sekil("poly", "change-head", (p1[0], p1[1], p1[0] - 9 * ux - 4.5 * uy, p1[1] - 9 * uy + 4.5 * ux,
                                                  p1[0] - 9 * ux + 4.5 * uy, p1[1] - 9 * uy - 4.5 * ux), "ink"))
        if ok.get("labelKey"):
            hw, hh = boyut(ok["labelKey"])
            tepe = y + yon * TANECIK_YAY
            ly = tepe + yon * (4 + hh)
            while any(abs(ly - k[1]) < hh + k[3] and abs(cx_ - k[0]) < hw + k[2] for k in kutular[yon]):
                ly += yon * (th + 2)
            kutular[yon].append((cx_, ly, hw, hh))
            yazilar.append(("change-label", cx_, ly, hw, hh, label(ok["labelKey"])))
    ust = max([0.0] + [-(y - hh) for _, _, y, _, hh, _ in yazilar] + [TANECIK_YAY + 4 for o in fig.get("arrows", [])
                                                                       if o["from"] < o["to"]])
    alt = max([bh] + [y + hh for _, _, y, _, hh, _ in yazilar] + [alt_cizgi + TANECIK_YAY for o in fig.get("arrows", [])
                                                                   if o["from"] > o["to"]])
    gerek = ust + alt + 16
    y0 = ust + 8 + max(0.0, (h - gerek) / 2)
    for rol, x, y, _, _, yazi in yazilar:
        out.append(_sekil("text", rol, (x, y), text=yazi, fill="ink"))
    for s in out:
        s["pts"] = [v + (0.0 if j % 2 == 0 else y0) for j, v in enumerate(s["pts"])]
    return {"shapes": out, "height": gerek, "unit": d}


def _baslik_hatalari(fig: dict, stiller: tuple[str, ...]) -> list:
    """1.8 ``title`` (AMI metni, «Tablo: …») ve ``titleStyle`` denetimi."""
    h = []
    kind = fig.get("kind")
    if "title" in fig and not (isinstance(fig["title"], str) and fig["title"].strip()):
        h.append(f"{kind}: title boş olmayan metin olmalı")
    if "titleStyle" in fig:
        if "title" not in fig:
            h.append(f"{kind}: titleStyle yalnız title ile yazılır")
        elif fig["titleStyle"] not in stiller:
            h.append(f"{kind}: titleStyle {' | '.join(stiller)} olmalı")
    return h


def figur_kontrol(fig: dict) -> list:
    """Şerit A figürünü katalog kısıtlarına göre denetler; hata listesi döner."""
    h = []
    kind = fig.get("kind")
    if kind not in KATALOG:
        return [f"bilinmeyen kind: {kind!r}"]
    if kind == "map" and "base" in fig:
        return _bos_zemin_harita_hatalari(fig)
    spec = KATALOG[kind]
    izinli = (
        spec["zorunlu"] | spec["opsiyonel"] |
        FIGUR_GENEL_ZORUNLU | FIGUR_GENEL_OPSIYONEL | {"kind"}
    )
    for alan in spec["zorunlu"] | FIGUR_GENEL_ZORUNLU:
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
            h.extend(_sayi_dogrusu_aralik_hatalari(fig))
            if "jumps" in fig:
                h.extend(_sayi_dogrusu_sicrama_hatalari(fig))
    elif kind == "fraction":
        if fig.get("style") not in ("bar", "pie", "grid", "area"):
            h.append("fraction: style ∈ bar|pie|grid|area değil")
        if fig.get("style") == "area":
            h.extend(_kesir_alan_hatalari(fig))
        elif "rows" in fig or "rowsFilled" in fig:
            h.append("fraction: rows/rowsFilled yalnız style area ile yazılır")
        p = fig.get("parts")
        if not isinstance(p, int) or not 2 <= p <= 24:
            h.append("fraction: 2 ≤ parts ≤ 24 değil")
        b = fig.get("wholes", 1)
        if not isinstance(b, int) or isinstance(b, bool) or not 1 <= b <= KESIR_BUTUN_EN_COK:
            h.append(f"fraction: wholes 1..{KESIR_BUTUN_EN_COK} tam sayı olmalı")
            b = 1
        f = fig.get("filled")
        if f is not None and (not isinstance(f, int) or isinstance(p, int) and not 0 <= f <= p * b):
            h.append("fraction: 0 ≤ filled ≤ parts·wholes değil")
    elif kind == "shape":
        if fig.get("type") not in ("square", "rect", "triangle", "circle", "polygon", *KATI_TURLER):
            h.append("shape: type beyaz liste dışı")
        dims = fig.get("dims", {})
        if not isinstance(dims, dict):
            h.append("shape: dims sözlük değil")
        else:
            for k, v in dims.items():
                if k not in ("w", "h", "r", "a", "b", "c", "d") or (k == "d" and fig.get("type") != "cuboid"):
                    h.append(f"shape: dims alanı tanımsız: {k}")
                elif not _sayi_mi(v) or v <= 0:
                    h.append(f"shape: dims.{k} > 0 değil")
        if "net" in fig and fig.get("type") not in KATI_TURLER:
            h.append("shape: net yalnız cisimle (cuboid, prism, pyramid, cylinder, cone) yazılır")
        if ("view" in fig or "projection" in fig) and fig.get("type") not in KATI_TURLER:
            h.append("shape: view ve projection yalnız type=cubes ile yazılır")
        if not h:
            h.extend(_kati_hatalari(fig) if fig["type"] in KATI_TURLER else _sekil_16_hatalari(fig))
    elif kind == "angle":
        d = fig.get("degrees")
        if not _sayi_mi(d) or not 0 < d <= 360:
            h.append("angle: 0 < degrees ≤ 360 değil")
        rays = fig.get("rays", 2)
        if isinstance(rays, bool) or rays not in (2, 3):
            h.append("angle: rays yalnız 2 ya da 3 (3 = açıortay ışını)")
        h.extend(_kesen_hatalari(fig))
        if "construction" in fig:
            if not isinstance(fig["construction"], bool):
                h.append("angle: construction true/false olmalı")
            elif fig["construction"] and (rays != 3 or not (_sayi_mi(d) and d <= 180)):
                h.append("angle: construction yalnız rays=3 ve degrees ≤ 180 ile (açıortay pergel izi)")
        if "adjacent" in fig:
            h.extend(_komsu_hatalari(fig))
        elif "rayKeys" in fig or "vertexKey" in fig:
            h.append("angle: rayKeys/vertexKey yalnız adjacent ile yazılır")
        if "protractor" in fig:
            if not isinstance(fig["protractor"], bool):
                h.append("angle: protractor true/false olmalı")
            elif fig["protractor"] and (rays != 2 or not (_sayi_mi(d) and d <= 180)
                                        or fig.get("transversal") is True or fig.get("construction") is True):
                h.append("angle: protractor yalnız rays=2 ve degrees ≤ 180 ile (transversal/construction olmadan)")
    elif kind == "grid":
        c, r = fig.get("cols"), fig.get("rows")
        if not isinstance(c, int) or not isinstance(r, int) or not (1 <= c <= 20 and 1 <= r <= 20):
            h.append("grid: 1 ≤ cols,rows ≤ 20 değil")
        else:
            for i in fig.get("shaded", []) or []:
                if not isinstance(i, int) or not 0 <= i < c * r:
                    h.append(f"grid: shaded indeksi cols*rows dışı: {i!r}")
            # Hücre adı {"hücre sırası": anahtar}; eski paketlerdeki boş liste de geçerli.
            names = fig.get("labels", {})
            if names != [] and (not isinstance(names, dict) or any(
                    not str(k).isdigit() or not 0 <= int(k) < c * r or not isinstance(v, str) or not v.strip()
                    for k, v in names.items())):
                h.append("grid: labels {\"hücre sırası\": anahtar} olmalı; sıra cols*rows içinde")
    elif kind == "coordinate":
        for alan in ("xRange", "yRange"):
            rng = fig.get(alan)
            if (not isinstance(rng, list) or len(rng) != 2
                    or not all(_sayi_mi(v) and math.isfinite(float(v)) for v in rng)
                    or not rng[0] < rng[1]):
                h.append(f"coordinate: {alan} [min,max] ve min<max değil")
        for p in fig.get("points", []) or []:
            if not (isinstance(p, list) and len(p) == 2 and all(_sayi_mi(v) for v in p)):
                h.append(f"coordinate: point [x,y] değil: {p!r}")
        # Nokta adı {"nokta sırası": anahtar} (grid kuralı); liste biçimi çizicide sessizce
        # kayboluyor ya da çöküyordu (LGS Ek 1). Eski paketlerdeki boş liste geçerli.
        points = fig.get("points") if isinstance(fig.get("points"), list) else []
        names = fig.get("labels", {})
        if names != [] and (not isinstance(names, dict) or any(
                not str(k).isdigit() or not 0 <= int(k) < len(points) or not isinstance(v, str) or not v.strip()
                for k, v in names.items())):
            h.append("coordinate: labels {\"nokta sırası\": anahtar} olmalı; sıra points içinde")
        if not h:
            h.extend(_koordinat_16_hatalari(fig))
    elif kind == "chart":
        h.extend(_grafik_hatalari(fig))
        h.extend(_baslik_hatalari(fig, ("prefix-above",)))
        if "axisUnits" in fig:
            birim = fig["axisUnits"]
            if not (isinstance(birim, dict) and birim and set(birim) <= {"x", "y"}
                    and all(isinstance(v, str) and v.strip() for v in birim.values())):
                h.append("chart: axisUnits {x?, y?} boş olmayan metin olmalı")
            elif "axisKeys" not in fig:
                h.append("chart: axisUnits yalnız axisKeys ile yazılır")
    elif kind == "chance":
        h.extend(_sans_hatalari(fig))
    elif kind == "model":
        h.extend(_model_hatalari(fig))
    elif kind == "instrument":
        h.extend(_olcu_hatalari(fig))
    elif kind == "light":
        h.extend(_isik_hatalari(fig))
    elif kind == "particles":
        h.extend(_tanecik_hatalari(fig))
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
                    # 1.8: düz dize hücre {"v": dize} kısaltmasıdır (AMI alabilir).
                    if isinstance(hucre, str):
                        continue
                    if not (isinstance(hucre, dict) and len(hucre) == 1
                            and next(iter(hucre)) in ("key", "v")):
                        h.append(f"table: hücre {{'key':…}}, {{'v':…}} veya metin değil: {hucre!r}")
        if "rowHeaderBold" in fig and not isinstance(fig["rowHeaderBold"], bool):
            h.append("table: rowHeaderBold true/false olmalı")
        h.extend(_baslik_hatalari(fig, ("prefix-above", "header-row")))
    elif kind == "flow":
        dugumler, kenarlar = fig.get("nodes"), fig.get("edges")
        onceki = len(h)
        idler = set()
        if not isinstance(dugumler, list):
            h.append("flow: nodes liste değil")
        else:
            for n in dugumler:
                if not (isinstance(n, dict) and {"id", "labelKey"} <= set(n) <= {"id", "labelKey", "shape"}):
                    h.append(f"flow: node {{'id','labelKey','shape'?}} değil: {n!r}")
                else:
                    idler.add(n["id"])
                    if "shape" in n and n["shape"] not in AKIS_SEKIL:
                        h.append(f"flow: node shape ∈ {'|'.join(AKIS_SEKIL)} değil: {n!r}")
        if "numbered" in fig and not isinstance(fig["numbered"], bool):
            h.append("flow: numbered true|false olmalı")
        if not isinstance(kenarlar, list):
            h.append("flow: edges liste değil")
        else:
            for e in kenarlar:
                if not (isinstance(e, dict) and {"from", "to"} <= set(e)
                        and set(e) <= {"from", "to", "labelKey"}):
                    h.append(f"flow: edge {{'from','to','labelKey'?}} değil: {e!r}")
                elif idler and (e["from"] not in idler or e["to"] not in idler):
                    h.append(f"flow: edge tanımsız node'a bağlanıyor: {e!r}")
        if len(h) == onceki and any("shape" in n for n in dugumler):
            h.extend(_akis_semasi_hatalari(fig))
    elif kind == "circuit":
        elemanlar = fig.get("elements")
        if not isinstance(elemanlar, list) or not elemanlar:
            h.append("circuit: elements liste değil/boş")
            elemanlar = []
        if "layout" in fig and fig["layout"] not in ("series", "parallel"):
            h.append("circuit: layout ∈ series|parallel değil")
        elif elemanlar:
            h.extend(_devre_hatalari(fig))
        etiketler = fig.get("labelKeys")
        # Kendi labelKey'i olmayan her eleman türü ve düzen labelKeys'ten adlanır.
        gereken = {e for e in elemanlar if isinstance(e, str)} | {
            e.get("type") for e in elemanlar
            if isinstance(e, dict) and isinstance(e.get("type"), str) and not e.get("labelKey")
        }
        if fig.get("layout") in ("series", "parallel"):
            gereken.add(fig["layout"])
        if not isinstance(etiketler, dict):
            if gereken or "labelKeys" in fig:
                h.append("circuit: labelKeys sözlük olmalı")
        else:
            eksik = gereken - set(etiketler)
            if eksik:
                h.append(f"circuit: labelKeys eksik: {sorted(eksik)}")
    elif kind == "diagram":
        view = fig.get("viewBox", [0, 0, 100, 60])
        if (
            not isinstance(view, list) or len(view) != 4
            or not all(_sayi_mi(v) and math.isfinite(float(v)) for v in view)
            or float(view[2]) <= 0 or float(view[3]) <= 0
        ):
            h.append("diagram: viewBox [x,y,w,h] ve w,h>0 değil")
            view = [0, 0, 100, 60]
        vx, vy, vw, vh = map(float, view)

        def diagram_inside(pair):
            return (isinstance(pair, (list, tuple)) and len(pair) == 2
                    and all(_sayi_mi(v) and math.isfinite(float(v)) for v in pair)
                    and vx <= float(pair[0]) <= vx + vw
                    and vy <= float(pair[1]) <= vy + vh)
        elemanlar = fig.get("elements")
        if not isinstance(elemanlar, list) or not 1 <= len(elemanlar) <= 40:
            h.append("diagram: elements 1..40 öğeli liste değil")
        else:
            for i, eleman in enumerate(elemanlar):
                if not isinstance(eleman, dict):
                    h.append(f"diagram: elements[{i}] nesne değil")
                    continue
                tur = eleman.get("type")
                if tur not in DIAGRAM_STIL:
                    h.append(f"diagram: elements[{i}].type beyaz liste dışı")
                    continue
                if eleman.get("style", "plain") not in DIAGRAM_STIL[tur]:
                    h.append(f"diagram: elements[{i}].style beyaz liste dışı")
                for renk_alani in ("fill", "stroke"):
                    if renk_alani in eleman and eleman[renk_alani] not in DIAGRAM_RENK:
                        h.append(f"diagram: elements[{i}].{renk_alani} beyaz liste dışı")
                h.extend(_diagram_14_hatalari(i, tur, eleman, diagram_inside))
                if "width" in eleman:
                    kalinlik = eleman["width"]
                    en_ince, en_kalin = DIAGRAM_CIZGI_KALINLIGI
                    if (isinstance(kalinlik, bool) or not isinstance(kalinlik, (int, float))
                            or not en_ince <= kalinlik <= en_kalin):
                        h.append(f"diagram: elements[{i}].width 0.1..8 olmalı")
                if tur == "polygon":
                    points = eleman.get("points")
                    en_az, en_cok = DIAGRAM_COKGEN_NOKTA
                    if (not isinstance(points, list) or not en_az <= len(points) <= en_cok
                            or not all(diagram_inside(point) for point in points)):
                        h.append(f"diagram: elements[{i}].points 3..128 ve viewBox içinde olmalı")
                elif tur == "line":
                    start = [eleman.get("x1"), eleman.get("y1")]
                    end = [eleman.get("x2"), eleman.get("y2")]
                    if not diagram_inside(start) or not diagram_inside(end) or start == end:
                        h.append(f"diagram: elements[{i}] çizgi uçları farklı ve viewBox içinde olmalı")
                    if "arrow" in eleman and eleman["arrow"] not in DIAGRAM_OK_UCU:
                        h.append(f"diagram: elements[{i}].arrow none|first|last|both olmalı")
    elif kind == "map":
        map_turu = fig.get("mapType")
        if map_turu not in MAP_TURLERI:
            h.append("map: mapType beyaz liste dışı")
        view = fig.get("viewBox", [0, 0, 100, 60])
        if (
            not isinstance(view, list) or len(view) != 4
            or not all(_sayi_mi(v) and math.isfinite(float(v)) for v in view)
            or float(view[2]) <= 0 or float(view[3]) <= 0
        ):
            h.append("map: viewBox [x,y,w,h] ve w,h>0 değil")
            view = [0, 0, 100, 60]
        vx, vy, vw, vh = (float(value) for value in view)

        def _icinde(pair):
            return (
                isinstance(pair, list) and len(pair) == 2
                and all(_sayi_mi(value) and math.isfinite(float(value)) for value in pair)
                and vx <= float(pair[0]) <= vx + vw
                and vy <= float(pair[1]) <= vy + vh
            )

        bolgeler = fig.get("regions")
        if not isinstance(bolgeler, list) or not 1 <= len(bolgeler) <= 64:
            h.append("map: regions 1..64 öğeli liste değil")
        else:
            for i, bolge in enumerate(bolgeler):
                noktalar = bolge.get("points") if isinstance(bolge, dict) else None
                if (
                    not isinstance(bolge, dict) or not isinstance(bolge.get("id"), str)
                    or not bolge["id"].strip() or not isinstance(noktalar, list)
                    or not 3 <= len(noktalar) <= 512 or not all(_icinde(p) for p in noktalar)
                ):
                    h.append(f"map: regions[{i}] geçersiz")
                    continue
                for renk_alani in ("fill", "stroke"):
                    if renk_alani in bolge and bolge[renk_alani] not in DIAGRAM_RENK:
                        h.append(f"map: regions[{i}].{renk_alani} beyaz liste dışı")
        noktalar = fig.get("points", []) or []
        if not isinstance(noktalar, list) or len(noktalar) > 64:
            h.append("map: points 0..64 öğeli liste değil")
        else:
            for i, nokta in enumerate(noktalar):
                if (
                    not isinstance(nokta, dict) or not _icinde([nokta.get("x"), nokta.get("y")])
                    or nokta.get("symbol", "dot") not in MAP_NOKTA_SEMBOLLERI
                ):
                    h.append(f"map: points[{i}] geçersiz")
        rotalar = fig.get("routes", []) or []
        if not isinstance(rotalar, list) or len(rotalar) > 32:
            h.append("map: routes 0..32 öğeli liste değil")
        else:
            for i, rota in enumerate(rotalar):
                rota_noktalari = rota.get("points") if isinstance(rota, dict) else None
                if (
                    not isinstance(rota, dict) or not isinstance(rota_noktalari, list)
                    or not 2 <= len(rota_noktalari) <= 256
                    or not all(_icinde(p) for p in rota_noktalari)
                    or rota.get("style", "route") not in MAP_ROTA_STILLERI
                ):
                    h.append(f"map: routes[{i}] geçersiz")
        lejant = fig.get("legend", []) or []
        if not isinstance(lejant, list) or len(lejant) > 12:
            h.append("map: legend 0..12 öğeli liste değil")
        else:
            for i, oge in enumerate(lejant):
                if (
                    not isinstance(oge, dict) or not isinstance(oge.get("labelKey"), str)
                    or not oge["labelKey"].strip() or oge.get("color") not in DIAGRAM_RENK
                ):
                    h.append(f"map: legend[{i}] geçersiz")
        if map_turu != "schematic" and (
            not str(fig.get("boundarySetId") or "").strip()
            or not str(fig.get("boundaryVersion") or "").strip()
        ):
            h.append("map: doğrulanmış sınır veri kimliği/sürümü eksik")
        if map_turu == "political" and fig.get("territoryReview") != "passed-human":
            h.append("map: siyasi harita passed-human bölge incelemesi olmadan yayımlanamaz")
    elif kind == "timeline":
        if fig.get("orientation", "horizontal") not in {"horizontal", "vertical"}:
            h.append("timeline: orientation horizontal|vertical değil")
        olaylar = fig.get("events")
        onceki = -1.0
        if not isinstance(olaylar, list) or not 2 <= len(olaylar) <= 40:
            h.append("timeline: events 2..40 öğeli liste değil")
        else:
            for i, olay in enumerate(olaylar):
                konum = olay.get("position") if isinstance(olay, dict) else None
                if (
                    not isinstance(olay, dict) or not str(olay.get("id") or "").strip()
                    or not str(olay.get("labelKey") or "").strip()
                    or not _sayi_mi(konum) or not math.isfinite(float(konum))
                    or not 0 <= float(konum) <= 1 or float(konum) <= onceki
                    or ("color" in olay and olay["color"] not in DIAGRAM_RENK)
                ):
                    h.append(f"timeline: events[{i}] geçersiz veya sırasız")
                if _sayi_mi(konum):
                    onceki = float(konum)
        donemler = fig.get("periods", []) or []
        if not isinstance(donemler, list) or len(donemler) > 12:
            h.append("timeline: periods 0..12 öğeli liste değil")
        else:
            for i, donem in enumerate(donemler):
                bas = donem.get("start") if isinstance(donem, dict) else None
                son = donem.get("end") if isinstance(donem, dict) else None
                if (
                    not isinstance(donem, dict) or not str(donem.get("labelKey") or "").strip()
                    or not _sayi_mi(bas) or not _sayi_mi(son)
                    or not 0 <= float(bas) < float(son) <= 1
                    or ("color" in donem and donem["color"] not in DIAGRAM_RENK)
                ):
                    h.append(f"timeline: periods[{i}] geçersiz")
    return h


__all__ = [
    "CIRCUIT_ANAHTAR", "CIRCUIT_ELEM", "DIAGRAM_CIZGI_DESENI", "DIAGRAM_IKON", "DIAGRAM_RENK",
    "DIAGRAM_STIL", "DIAGRAM_TARAMA", "DIAGRAM_TARAMALI_TURLER",
    "SATURN_HALKA_ACIKLIGI", "DIAGRAM_COKGEN_NOKTA", "DIAGRAM_CIZGI_KALINLIGI",
    "MAP_BOS_ZEMIN_ALANLARI", "MAP_SINIR_VERISI_GEREKEN_TABANLAR",
    "FIGUR_GENEL_OPSIYONEL", "FIGUR_GENEL_ZORUNLU", "KATALOG",
    "MAP_NOKTA_SEMBOLLERI", "MAP_ROTA_STILLERI", "MAP_TURLERI",
    "_sayi_mi", "figur_kontrol",
]

