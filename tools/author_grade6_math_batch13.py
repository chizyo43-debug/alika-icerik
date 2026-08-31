#!/usr/bin/env python3
"""Append 100 independently authored Grade 6 mathematics questions (batch 13)."""
from __future__ import annotations

from collections import Counter
import json
from typing import Any

from author_grade6_bilisim_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade6_english_batch11 import rows
from author_grade6_english_math_batch12 import MATH_SOURCE
from author_grade6_fen_batch07 import task
from author_grade6_fen_english_batch10 import make_record
from author_grade6_mixed_batch03 import read_notes_only


def vrows(note: str, values: list[tuple[str, str, str, str, str, str, str, str | None]]):
    return [
        task(note, mode, stem, correct, [w1, w2, w3], explanation, figure_kind=tag)
        for mode, stem, correct, w1, w2, w3, explanation, tag in values
    ]


def _label(labels: dict[str, str], qid: str, suffix: str, value: str) -> str:
    key = f"figure.{qid}.{suffix}"
    labels[key] = value
    return key


def geometry_figure(qid: str, labels: dict[str, str], tag: str) -> dict[str, Any]:
    alt = _label(labels, qid, "alt", "Adlandırılmış doğrular ve noktalarla oluşturulmuş ölçek dışı geometri şeması; istenen açı veya uzunluk açıklanmamıştır.")
    if tag == "parallel-one":
        d1 = _label(labels, qid, "d1", "d₁")
        d2 = _label(labels, qid, "d2", "d₂")
        k = _label(labels, qid, "k", "k")
        p = _label(labels, qid, "p", "P")
        r = _label(labels, qid, "r", "R")
        elements = [
            {"type": "line", "style": "plain", "x1": 8, "y1": 18, "x2": 92, "y2": 18, "stroke": "blue", "labelKey": d1},
            {"type": "line", "style": "plain", "x1": 8, "y1": 45, "x2": 92, "y2": 45, "stroke": "blue", "labelKey": d2},
            {"type": "line", "style": "plain", "x1": 32, "y1": 5, "x2": 62, "y2": 56, "stroke": "ink", "labelKey": k},
            {"type": "circle", "style": "plain", "x": 40, "y": 18, "r": 2, "fill": "accent", "labelKey": p, "labelX": 35, "labelY": 12},
            {"type": "circle", "style": "plain", "x": 56, "y": 45, "r": 2, "fill": "accent", "labelKey": r, "labelX": 61, "labelY": 52},
        ]
    elif tag == "parallel-two":
        labels_local = {name: _label(labels, qid, name, name.upper()) for name in ("a", "b", "c", "d")}
        elements = [
            {"type": "line", "style": "plain", "x1": 8, "y1": 16, "x2": 92, "y2": 16, "stroke": "blue"},
            {"type": "line", "style": "plain", "x1": 8, "y1": 47, "x2": 92, "y2": 47, "stroke": "blue"},
            {"type": "line", "style": "plain", "x1": 25, "y1": 5, "x2": 40, "y2": 57, "stroke": "ink"},
            {"type": "line", "style": "plain", "x1": 75, "y1": 5, "x2": 62, "y2": 57, "stroke": "ink"},
            {"type": "circle", "style": "plain", "x": 28, "y": 16, "r": 2, "fill": "accent", "labelKey": labels_local["a"], "labelX": 23, "labelY": 10},
            {"type": "circle", "style": "plain", "x": 72, "y": 16, "r": 2, "fill": "accent", "labelKey": labels_local["b"], "labelX": 77, "labelY": 10},
            {"type": "circle", "style": "plain", "x": 37, "y": 47, "r": 2, "fill": "accent", "labelKey": labels_local["c"], "labelX": 32, "labelY": 54},
            {"type": "circle", "style": "plain", "x": 65, "y": 47, "r": 2, "fill": "accent", "labelKey": labels_local["d"], "labelX": 70, "labelY": 54},
        ]
    else:
        vertices = {name: _label(labels, qid, name.lower(), name) for name in "ABCD"}
        points = [[20, 45], [35, 12], [80, 12], [65, 45]]
        elements = [
            {"type": "polygon", "style": "plain", "points": points, "fill": "surface", "stroke": "blue"},
            {"type": "line", "style": "plain", "x1": 20, "y1": 45, "x2": 80, "y2": 12, "stroke": "muted"},
            {"type": "line", "style": "plain", "x1": 35, "y1": 12, "x2": 65, "y2": 45, "stroke": "muted"},
        ]
        for (x, y), name in zip(points, "ABCD"):
            elements.append({"type": "circle", "style": "plain", "x": x, "y": y, "r": 2, "fill": "accent", "labelKey": vertices[name]})
    return {"kind": "diagram", "viewBox": [0, 0, 100, 60], "elements": elements, "altTextKey": alt, "notToScale": True}


def apply_geometry_visual(row: dict[str, Any], item: dict[str, Any], labels: dict[str, str]) -> None:
    tag = item.get("figure_kind")
    if not tag:
        return
    row["figure"] = geometry_figure(str(row["id"]), labels, str(tag))
    row["visualRequirement"] = "required"
    row["visualNeed"] = {
        "level": "required", "role": "evidence",
        "rationale": "Doğru, kesen, köşe ve köşegenlerin uzamsal ilişkisi yalnız yapılandırılmış şemada eksiksiz gösterilmiştir.",
        "acceptableKinds": ["diagram"],
        "evidenceDimensions": ["doğru konumu", "köşe veya kesişim ilişkisi"],
    }


def fraction_decimal_tasks():
    n = "tr-g06-matematik-note-006"
    return rows(n, [
        ("comprehension", "3 ÷ 8 işlemi kesir olarak nasıl gösterilir?", "3/8",
         "8/3", "3/5", "8/11", "Bölünen paya, bölen paydaya yazılır."),
        ("comprehension", "Bir kesrin ondalık gösteriminin sonlu olması ne demektir?", "Virgülden sonra belirli sayıda basamakla bitmesi",
         "Aynı rakam grubunun sonsuza dek sürmesi", "Kesrin payının sıfır olması", "Ondalık kısmın yalnız bir rakam olması", "Sonlu ondalık gösterimde basamak dizisi bir noktada sona erer."),
        ("comprehension", "1/3 kesrinin 0,333… gösterimindeki çizgi neyi anlatır?", "3 rakamının düzenli olarak tekrar ettiğini",
         "Ondalık gösterimin 0,3'te bittiğini", "3'ün basamak değerinin sıfır olduğunu", "Kesrin 3 tam sayıya eşit olduğunu", "Tekrarlayan 3, devirli ondalık yapıyı gösterir."),
        ("application", "7 litre meyve suyu 20 eş şişeye paylaştırılıyor. Her şişedeki miktarın litre cinsinden ondalık gösterimi hangisidir?", "0,35 L",
         "0,7 L", "0,27 L", "3,5 L", "Paylaştırma 7÷20 işlemidir; 7/20=35/100=0,35 litre olur."),
        ("application", "5 ÷ 4 işleminin ondalık sonucu hangisidir?", "1,25",
         "0,8", "1,4", "2,5", "5/4=125/100=1,25 olur."),
        ("application", "0,125 ondalık gösteriminin sadeleşmiş kesir karşılığı hangisidir?", "1/8",
         "1/4", "5/8", "12/5", "0,125=125/1000 ve iki sayı 125'e bölününce 1/8 elde edilir."),
        ("application", "11 metre ip 6 eş parçaya ayrılıyor. Bir parçanın metre cinsinden devirli ondalık uzunluğu hangisidir?", "1,8333… m",
         "1,6 m", "1,1818… m", "0,8333… m", "11÷6 işleminde bölüm 1, kalan 5 olur; ondalık bölümde 8'den sonra 3 tekrar eder."),
        ("application", "Paydası 40 olan 13/40 kesri 1000 paydalı eş kesre çevrilirse pay kaç olur?", "325",
         "130", "520", "40", "40×25=1000 olduğundan pay da 13×25=325 olur."),
        ("analysis", "3/8 ve 5/12 kesirlerinin ondalık gösterimleri sırasıyla 0,375 ve 0,4166…'dır. Hangisi büyüktür?", "5/12",
         "3/8", "İkisi eşittir.", "Ondalıklar farklı türde olduğu için karşılaştırılamaz.", "0,4166… sayısı 0,375'ten büyüktür."),
        ("analysis", "Bir kesrin sadeleşmiş paydası 2³×5² biçimindedir. Ondalık gösterimi için hangi sonuç beklenir?", "Sonlu olur.",
         "Kesinlikle yalnız 3 tekrar eder.", "Ondalık gösterim oluşturulamaz.", "Her zaman tam sayıdır.", "Sade paydada yalnız 2 ve 5 asal çarpanları bulunması sonlu ondalık gösterim verir."),
        ("analysis", "0,272727… sayısında tekrar eden blok hangisidir ve kesir karşılığı nasıl kurulabilir?", "27 bloğu tekrar eder; sayı 27/99 olarak yazılabilir.",
         "2 bloğu tekrar eder; sayı 2/10'dur.", "272 bloğu tekrar eder; sayı 272/100'dür.", "Tekrar yoktur; sayı 27/100'dür.", "İki basamaklı 27 bloğu 99 paydalı kesirle temsil edilir."),
        ("error-analysis", "Bir öğrenci “2/5 kesri 2÷5 yerine 5÷2 yapılarak ondalığa çevrilir.” diyor. Hangi düzeltme doğrudur?", "Kesirde pay bölünendir; 2÷5=0,4 yapılmalıdır.",
         "Her kesir büyük sayı küçüğe bölünerek çevrilir.", "2/5 ondalık gösterime çevrilemez.", "Pay ve payda toplanarak 0,7 bulunur.", "Kesir çizgisi payın paydaya bölünmesini gösterir."),
        ("error-analysis", "Bir öğrenci “0,666… ile 0,6 eşittir çünkü ilk basamakları aynıdır.” diyor. Hangi değerlendirme doğrudur?", "0,666… sayısı 0,6'dan büyüktür; sonraki basamaklar da değere katkı yapar.",
         "İki sayı yalnız ilk basamakla karşılaştırılır.", "0,6 daha büyüktür çünkü daha kısadır.", "Devirli ondalıklar karşılaştırılamaz.", "Ondalık karşılaştırmada bütün devam eden basamaklar dikkate alınır."),
    ])


def length_unit_tasks():
    n = "tr-g06-matematik-note-007"
    return rows(n, [
        ("comprehension", "Bir sınıfın uzunluğunu ölçmek için en uygun standart birim hangisidir?", "metre",
         "milimetre", "kilometre", "santimetrekare", "Sınıf boyutu metre ölçeğine uygundur."),
        ("comprehension", "1 kilometre kaç metredir?", "1000 metre",
         "100 metre", "10 000 metre", "1000 santimetre", "Kilo ön eki temel birimin bin katını gösterir."),
        ("application", "3,6 metre kaç santimetredir?", "360 santimetre",
         "36 santimetre", "3600 santimetre", "0,36 santimetre", "1 m=100 cm olduğundan 3,6×100=360 cm'dir."),
        ("application", "Bir kalemin uzunluğu 145 mm'dir. Bu uzunluk kaç santimetredir?", "14,5 cm",
         "1,45 cm", "1450 cm", "0,145 cm", "10 mm=1 cm olduğundan 145÷10=14,5 cm olur."),
        ("application", "Bir yürüyüş rotası 2 km 350 m'dir. Tamamı metre cinsinden kaçtır?", "2350 m",
         "2500 m", "2035 m", "23 500 m", "2 km=2000 m; 2000+350=2350 m'dir."),
        ("analysis", "Bir masa 1,2 m, bir dolap 135 cm uzunluğundadır. Hangisi daha uzundur ve fark kaç santimetredir?", "Dolap 15 cm daha uzundur.",
         "Masa 15 cm daha uzundur.", "Dolap 135 cm daha uzundur.", "İkisi eşit uzunluktadır.", "1,2 m=120 cm; 135−120=15 cm olur."),
        ("analysis", "0,75 km, 720 m ve 74 000 cm uzunlukları büyükten küçüğe nasıl sıralanır?", "0,75 km > 74 000 cm > 720 m",
         "720 m > 0,75 km > 74 000 cm", "74 000 cm > 720 m > 0,75 km", "Üçü eşittir.", "Değerler metreyle 750 m, 740 m ve 720 m'dir."),
        ("error-analysis", "Bir öğrenci “4,2 m=42 cm'dir; çünkü virgülü bir basamak kaydırdım.” diyor. Hangi düzeltme gerekir?", "Metreden santimetreye geçerken 100 ile çarpılır; 4,2 m=420 cm'dir.",
         "Metre ile santimetre arasında 10 kat vardır.", "4,2 m=0,42 cm'dir.", "Birim dönüşümünde sayı değişmez.", "Metre-santimetre ilişkisi iki basamaklı, yani 100 katlıdır."),
    ])


def mixed_representation_tasks():
    n = "tr-g06-matematik-note-008"
    return rows(n, [
        ("comprehension", "%25'in kesir ve ondalık gösterimleri hangileridir?", "1/4 ve 0,25",
         "1/25 ve 0,4", "25/10 ve 2,5", "3/4 ve 0,75", "%25=25/100=1/4 ve 0,25'tir."),
        ("application", "240 TL'nin %15'i kaç TL'dir?", "36 TL",
         "24 TL", "15 TL", "204 TL", "240×15/100=36 TL olur."),
        ("analysis", "Bir ürün önce %20 indirimle 400 TL'den düşüyor, sonra kasada 30 TL kupon uygulanıyor. Son fiyat kaç TL'dir?", "290 TL",
         "310 TL", "320 TL", "350 TL", "%20 indirim 80 TL'dir; 400−80−30=290 TL olur."),
    ])


def algebra_expression_tasks():
    n = "tr-g06-matematik-note-009"
    return rows(n, [
        ("comprehension", "Bir sayının 7 fazlasını gösteren cebirsel ifade hangisidir?", "x + 7",
         "x'in 7 katını gösteren 7x", "x'in 7 eksiğini gösteren x − 7", "7'nin x eksiğini gösteren 7 − x", "Fazlası sözcüğü değişkene toplama yapılmasını gerektirir."),
        ("comprehension", "5a ifadesinde 5 sayısının görevi nedir?", "a değişkeninin katsayısıdır.",
         "Sabit terimdir ve a'dan bağımsızdır.", "Değişkenin değeridir.", "İşlem işaretidir.", "Değişkenle çarpılan sayı katsayıdır."),
        ("application", "Bir otoparkta başlangıç ücreti 20 TL, her saat için 8 TL alınıyor. h saatlik ücret hangi ifadeyle gösterilir?", "20 + 8h",
         "28h", "20h + 8", "8 + h", "Sabit başlangıç ücretine saat başına ücretin h katı eklenir."),
        ("application", "Kenar uzunluğu a cm olan karenin çevresi hangi ifadeyle gösterilir?", "4a",
         "a + 4", "a²", "2a", "Karenin dört eş kenarı olduğundan çevre 4×a'dır."),
        ("analysis", "Bir taksinin ücreti 15+6k biçimindedir. k=4 için ücret kaçtır ve 15 neyi temsil eder?", "39 TL; açılış ücretini",
         "84 TL; kilometreyi", "24 TL; toplam yolu", "21 TL; saat ücretini", "15+6×4=39; k'den bağımsız 15 sabit açılış ücretidir."),
        ("error-analysis", "Bir öğrenci “Bir sayının üç katının 5 eksiği 3(x−5) ile gösterilir.” diyor. Hangi düzeltme doğrudur?", "Önce üç kat alınır, sonra 5 çıkarılır; ifade 3x−5'tir.",
         "İfade x−15 olmalıdır.", "Üç katı x+3 ile gösterilir.", "Eksik sözcüğü çarpma gerektirir.", "3(x−5), sayının ve 5'in farkının üç katıdır; işlem sırası farklıdır."),
    ])


def pattern_tasks():
    n = "tr-g06-matematik-note-010"
    return rows(n, [
        ("comprehension", "4, 7, 10, 13, ... sayı örüntüsünün artış kuralı nedir?", "Her adımda 3 eklenir.",
         "Her adımda 4 eklenir.", "Her adımda 2 ile çarpılır.", "Her adımda 3 çıkarılır.", "Ardışık terimler arasındaki fark sürekli 3'tür."),
        ("application", "İlk terimi 5, artışı 4 olan örüntünün 6. terimi kaçtır?", "25",
         "24", "29", "20", "6. terim 5+(6−1)×4=25 olur."),
        ("application", "n. terimi 2n+3 olan örüntünün ilk dört terimi hangileridir?", "5, 7, 9, 11",
         "3, 5, 7, 9", "2, 5, 8, 11", "5, 8, 11, 14", "n=1,2,3,4 değerleri sırasıyla 5,7,9,11 verir."),
        ("analysis", "Bir tabloda adım 1,2,3,4 için değerler 6,10,14,18'dir. Hangi cebirsel kural tabloyu açıklar?", "4n + 2",
         "6n", "2n + 4", "3n + 3", "n=1 için 6 veren ve her adımda 4 artan kural 4n+2'dir."),
        ("analysis", "A örüntüsü 3n+1, B örüntüsü 2n+5 ile veriliyor. Hangi adımda değerleri eşittir?", "4. adımda",
         "2. adımda", "3. adımda", "5. adımda", "3n+1=2n+5 eşitliğinden n=4 bulunur."),
        ("error-analysis", "Bir öğrenci “2, 5, 8, 11 örüntüsünün kuralı 2n+1'dir.” diyor. Hangi düzeltme doğrudur?", "Artış 3 olduğundan kural 3n−1 olmalıdır.",
         "Kural 2n+1 doğrudur çünkü ilk terim 2'dir.", "Kural n+3 olmalıdır.", "Örüntünün cebirsel kuralı yazılamaz.", "3n−1, n=1 için 2 verir ve her adımda 3 artar."),
    ])


def algorithm_expression_tasks():
    n = "tr-g06-matematik-note-011"
    return rows(n, [
        ("comprehension", "Bir algoritmada 'sayının iki katını al, sonra 3 ekle' adımları hangi ifadeyi oluşturur?", "2x + 3",
         "2(x+3)", "x+5", "3x+2", "Önce 2 ile çarpılır, oluşan sonuca 3 eklenir."),
        ("comprehension", "4(x+2) ifadesi hangi işlem sırasını anlatır?", "Önce x'e 2 ekleyip sonucu 4 ile çarpmayı",
         "Önce x'i 4 ile çarpıp yalnız x'e 2 eklemeyi", "x'e 8 eklemeyi", "x'i 6 ile çarpmayı", "Parantez içi işlem çarpmadan önce yapılır."),
        ("comprehension", "Bir algoritmanın çıktısı 5x−1 ise x=3 için çıktı kaçtır?", "14",
         "12", "15", "16", "5×3−1=14 olur."),
        ("application", "Girdi n için '3 ekle, sonucu 2 ile çarp' algoritmasının çıktısı hangisidir?", "2(n+3)",
         "2n+3", "n+6", "3(n+2)", "Toplama önce yapıldığı için parantez gerekir."),
        ("application", "Bir makine girdiyi önce 4 ile çarpıyor, sonra 7 çıkarıyor. Girdi x ile gösterilirse makinenin kuralı hangisidir?", "Dört katın 7 eksiği olan 4x − 7",
         "Önce 7 çıkarıp dörtle çarpmayı gösteren 4(x − 7)", "Yedi katın 4 eksiği olan 7x − 4", "Dört katın 7 fazlası olan 4x + 7", "İlk adım 4x sonucunu verir; ikinci adımda bu sonuçtan 7 çıkarılır."),
        ("application", "Çıktısı 3x+5 olan makinede çıktı 26 ise girdi kaçtır?", "7",
         "5", "8", "9", "3x+5=26, 3x=21 ve x=7'dir."),
        ("analysis", "A algoritması 2(x+4), B algoritması 2x+4 çıktısı veriyor. x=3 için çıktılar nasıl karşılaştırılır?", "A=14, B=10; A daha büyüktür.",
         "İkisi de 10'dur.", "A=10, B=14'tür.", "İkisi de 14'tür.", "A'da 3+4 önce ikiyle çarpılır; B'de yalnız x'in iki katına 4 eklenir."),
        ("analysis", "Bir akışın adımları 'x'ten 5 çıkar; sonucu 3 ile çarp; 2 ekle'dir. Hangi ifade doğrudur?", "3(x−5)+2",
         "3x−5+2", "3(x−3)", "x−15+2", "İlk farkın tamamı 3 ile çarpıldıktan sonra 2 eklenir."),
        ("error-analysis", "Bir öğrenci “2(x+6)=2x+6'dır.” diyor. Hangi düzeltme doğrudur?", "2 parantezdeki iki terime de dağılır; sonuç 2x+12'dir.",
         "2 yalnız 6'ya dağıtılır ve x+12 olur.", "Parantez sonucu değiştirmez.", "2(x+6)=x+8 olur.", "Dağılma özelliğinde dış çarpan her terimle çarpılır."),
        ("error-analysis", "Bir öğrenci 'önce 2 ekle, sonra karesini değil üç katını al' adımını x+6 yazıyor. Hangi ifade doğrudur?", "3(x+2)",
         "3x+2", "x+3+2", "2(x+3)", "Önce x+2 oluşur; bu sonucun tamamı 3 ile çarpılır."),
    ])


def parallel_angle_tasks():
    n = "tr-g06-matematik-note-012"
    return vrows(n, [
        ("comprehension", "Aynı düzlemde kesişmeyen iki doğru nasıl adlandırılır?", "Paralel doğrular",
         "Dik doğrular", "Kesişen doğrular", "Çakışık olmayan ışınlar", "Paralel doğrular aynı düzlemde ortak nokta oluşturmaz.", None),
        ("comprehension", "Şemada d₁ ve d₂ paralel, k bu doğruları P ve R noktalarında kesmektedir. P ve R'de aynı konumda bulunan açılar hangi türdür?", "Yöndeş açılar",
         "Ters açılar", "Komşu bütünler açılar", "Merkez açılar", "İki kesişimde aynı göreli konumdaki açılar yöndeştir.", "parallel-one"),
        ("comprehension", "İki doğruyu farklı noktalarda kesen üçüncü doğruya ne denir?", "Kesen doğru",
         "Açıortay", "Köşegen", "Yarıçap", "Kesen, iki doğruyla ayrı kesişim noktaları oluşturur.", None),
        ("application", "Paralel iki doğruyu kesen bir doğrunun oluşturduğu yöndeş açılardan biri 68° ise diğeri kaç derecedir?", "68°",
         "112°", "34°", "136°", "Paralel doğrularda yöndeş açılar eş ölçülüdür.", None),
        ("application", "Şemada d₁ // d₂ ve k kesenidir. P noktasındaki iç açı 124° ise R noktasındaki aynı yandaki iç açı kaç derecedir?", "56°",
         "124°", "62°", "248°", "Paralel doğrularda aynı yandaki iç açılar bütünlerdir; 180−124=56 olur.", "parallel-one"),
        ("application", "Paralel doğrularda iç ters açılardan biri 47° olduğuna göre diğeri kaç derecedir?", "47°",
         "133°", "94°", "23,5°", "İç ters açılar eş ölçülüdür.", None),
        ("application", "Şemadaki P kesişiminde bir açı 75°'dir. Bu açının ters açısı kaç derecedir?", "75°",
         "105°", "37,5°", "150°", "Bir kesişimde ters açılar birbirine eşittir.", "parallel-one"),
        ("application", "Bir kesenle oluşan komşu iki doğrusal açının ölçülerinden biri 109° ise diğeri kaç derecedir?", "71°",
         "109°", "54,5°", "251°", "Doğrusal açı çifti 180° olduğundan 180−109=71 bulunur.", None),
        ("analysis", "Şemada d₁ // d₂ iken P'deki bir açı 82°, onunla yöndeş R açısı 98° yazılmıştır. Hangi değerlendirme doğrudur?", "Ölçülerden biri hatalıdır; yöndeş açılar eşit olmalıdır.",
         "İki ölçü doğrudur çünkü toplamları 180°'dir.", "Paralellik yöndeş açıları etkilemez.", "Yöndeş açılar her zaman bütünlerdir.", "Paralellik koşulunda aynı konumdaki iki açı aynı ölçüyü taşımalıdır.", "parallel-one"),
        ("analysis", "İki doğruyu kesen bir doğruyla oluşan iç ters açılar eşit ölçülüyor. Bu bilgi hangi çıkarımı destekler?", "İki doğrunun paralel olabileceğini gösteren bir ölçüttür.",
         "Doğruların kesinlikle dik olduğunu gösterir.", "Kesenin açıortay olduğunu kanıtlar.", "Bütün açıların 90° olduğunu gösterir.", "İç ters açı eşitliği paralellik için kullanılan ters yöndeki ölçütlerden biridir.", None),
        ("analysis", "Şemada P'deki dar açı 3x+5°, R'deki yöndeş açı 5x−25°'dir. x kaçtır?", "15",
         "10", "20", "30", "Yöndeş açılar eşit olduğundan 3x+5=5x−25 ve x=15 olur.", "parallel-one"),
        ("analysis", "Aynı yandaki iç açılar 2x+10° ve 4x+20° olarak verilmiştir. Doğrular paralelse x kaçtır?", "25",
         "20", "30", "35", "Toplam 180°: 6x+30=180 ve x=25 olur.", None),
        ("error-analysis", "Bir öğrenci “Paralel doğrularda aynı yandaki iç açılar eşittir.” diyor. Hangi düzeltme doğrudur?", "Aynı yandaki iç açılar bütünlerdir; toplamları 180°'dir.",
         "Bu açılar her zaman 90°'dir.", "İç açılar arasında hiçbir ilişki yoktur.", "Yalnız ters açılar 180° toplam verir.", "Öğrenci eşitlik ile bütünlerlik ilişkisini karıştırmıştır.", None),
        ("error-analysis", "Bir öğrenci “Şemadaki P açısının ters açısı R kesişimindedir.” diyor. Hangi düzeltme gerekir?", "Ters açılar aynı kesişimde karşılıklı bulunur; R'deki açı farklı bir ilişki taşır.",
         "Ters açılar yalnız farklı kesişimlerde olur.", "P ile R aynı nokta sayılmalıdır.", "Her iki kesişimdeki bütün açılar ters açıdır.", "Ters açı tanımı tek kesişim noktasındaki karşılıklı ışınlara dayanır.", "parallel-one"),
    ])


def parallel_shape_tasks():
    n = "tr-g06-matematik-note-013"
    return vrows(n, [
        ("comprehension", "İki paralel doğru ile bunları kesen iki doğrunun arasında kalan dört kenarlı kapalı bölge hangi genel sınıfa girer?", "Dörtgen",
         "Üçgen", "Çember", "Doğru parçası", "Dört doğru parçasıyla çevrili kapalı bölge dörtgendir.", None),
        ("comprehension", "Şemadaki A, B, C ve D kesişim noktaları birleştirildiğinde oluşan kapalı şeklin kaç köşesi vardır?", "4",
         "2", "3", "6", "Dört farklı kesişim noktası dört köşe oluşturur.", "parallel-two"),
        ("comprehension", "Bir dörtgende karşılıklı kenar ne demektir?", "Ortak köşesi bulunmayan iki kenar",
         "Aynı köşede birleşen iki kenar", "Yalnız eş uzunlukta olan kenarlar", "Birbirini kesen köşegenler", "Karşılıklı kenarlar birbirine komşu değildir.", None),
        ("comprehension", "İki paralel doğru arasında oluşan dörtgende bu doğrular üzerindeki iki kenarın ortak özelliği nedir?", "Birbirlerine paraleldirler.",
         "Zorunlu olarak eş uzunluktadırlar.", "Birbirlerine diktirler.", "Aynı doğru üzerinde bulunurlar.", "Kenarlar başlangıçtaki iki paralel doğrunun parçalarıdır.", None),
        ("application", "Şemada AB // CD'dir. AB=9 cm ve CD=13 cm ise şekil için hangi bilgi doğrudan söylenebilir?", "Bir çift karşılıklı kenarı paralel olan bir dörtgendir.",
         "Bütün kenarları eşit bir eşkenar dörtgendir.", "AB ve CD birbirine diktir.", "Şekil zorunlu olarak karedir.", "Veri yalnız bir karşılıklı kenar çiftinin paralelliğini garanti eder.", "parallel-two"),
        ("application", "Paralel iki doğruyu kesen iki kesen birbirine de paralelse arada oluşan dörtgen hangi temel özelliğe sahiptir?", "İki çift karşılıklı kenarı paraleldir.",
         "Yalnız üç kenarı vardır.", "Bütün açıları zorunlu 60°'dir.", "Köşegenleri bulunmaz.", "Her iki doğru çifti karşılıklı paralel kenarlar oluşturur.", None),
        ("application", "Şemadaki A-B-C-D kapalı bölgesinin sınırını saat yönünde veren sıra hangisidir?", "A-B-D-C-A",
         "A-D-B-C-A", "A-C-B-D-A", "A-B-C-A", "Üstte A-B, sağda B-D, altta D-C ve solda C-A kenarları izlenir.", "parallel-two"),
        ("application", "Bir kesen iki paralel doğruyu kesiyor; ikinci kesen ilk kesenle paraleller arasında kesişiyor. Kapalı bölgelerden biri hangi şekil olabilir?", "Üçgen",
         "Yalnız çember", "Beş kenarsız bölge", "Tek nokta", "İki kesen ve paralel doğrulardan birinin parçaları üç kenarlı bölge oluşturabilir.", None),
        ("application", "Şemada üst ve alt doğrular paraleldir. Sol kesen sağa, sağ kesen sola eğimlidir. Aşağıdaki AB ve CD kenarları için hangi ilişki geçerlidir?", "AB ile CD birbirine paraleldir.",
         "AB ile CD birbirine diktir.", "AB ve CD aynı doğru üzerindedir.", "AB ile CD'nin ortak ucu vardır.", "AB ve CD paralel doğruların üzerinde yer alan karşılıklı kenarlardır.", "parallel-two"),
        ("application", "Bir dörtgenin yalnız bir çift karşılıklı kenarı paralel, diğer çifti paralel değildir. Bu bilgi hangi sınıflandırmayı destekler?", "Yamuk",
         "Kare", "Eşkenar üçgen", "Çember", "Yamukta bir çift karşılıklı kenar paraleldir.", None),
        ("application", "İki paralel doğru ve bunlara dik iki kesen arasında oluşan dörtgenin bütün iç açıları kaç derecedir?", "90°",
         "45°", "60°", "120°", "Dik kesenler paralel doğrularla dört dik açı oluşturur.", None),
        ("analysis", "Şemadaki A-B-D-C dörtgeninde AB // CD, AC ile BD ise paralel değildir. Hangi sonuç kesin değildir?", "Köşegenlerin birbirini ortalaması",
         "Şeklin dört köşeli olması", "AB ve CD'nin karşılıklı kenar olması", "En az bir paralel kenar çiftinin bulunması", "Tek paralel kenar çifti köşegenlerin ortalanmasını garanti etmez.", "parallel-two"),
        ("analysis", "Bir çizimde iki paralel doğruyu kesen doğrular kesişmeden ilerliyor. Oluşan dörtgende hangi özellik beklenir?", "İkinci karşılıklı kenar çifti de paraleldir.",
         "Şeklin üç kenarı olur.", "Paralel kenarlar kesişir.", "Bütün kenarlar zorunlu farklıdır.", "Kesenlerin de paralel olması ikinci paralel kenar çiftini oluşturur.", None),
        ("analysis", "Aynı iki paralel doğru üzerinde A-B ve C-D kenarları var. A-B uzunluğu 12 cm, C-D uzunluğu 12 cm ve yan kenarlar paralel. Hangi sınıf desteklenir?", "Paralelkenar",
         "Yalnız üçgen", "Çember", "Paralel kenarı olmayan dörtgen", "İki çift karşılıklı kenarın paralelliği paralelkenarı tanımlar.", None),
        ("analysis", "Şemada AB // CD ve ∠A=70°'dir. AC keseni boyunca aynı yandaki iç açı olan ∠C kaç derecedir?", "110°",
         "70°", "35°", "140°", "Aynı yandaki iç açılar bütünlerdir; 180−70=110 olur.", "parallel-two"),
        ("error-analysis", "Bir öğrenci “İki paralel doğru ve iki kesen her zaman kare oluşturur.” diyor. Hangi düzeltme doğrudur?", "Kare için paralelliğe ek olarak dik açı ve eş kenar koşulları gerekir.",
         "Her dörtgen zaten karedir.", "Paralel doğrular hiçbir kapalı şekil oluşturmaz.", "Karede paralel kenar bulunmaz.", "Verilen doğrular farklı eğim ve uzaklıklarda çeşitli üçgen ve dörtgenler oluşturabilir.", None),
        ("error-analysis", "Bir öğrenci “Şemadaki A-B-D-C bölgesi bir üçgendir.” diyor. Hangi düzeltme gerekir?", "Bölgenin dört köşesi ve dört kenarı olduğu için dörtgendir.",
         "Her kapalı bölge üçgendir.", "A ve C aynı köşedir.", "Kenar sayısı sınıflandırmada kullanılmaz.", "Şekil sınıfı kapalı sınırdaki kenar ve köşe sayısıyla belirlenir.", "parallel-two"),
        ("error-analysis", "Bir öğrenci “Karşılıklı kenarlar aynı köşede birleşir.” diyor. Hangi açıklama doğrudur?", "Aynı köşede birleşenler komşu, ortak köşesi olmayanlar karşılıklı kenarlardır.",
         "Bütün kenarlar karşılıklıdır.", "Karşılıklı kenar yalnız eş uzunluk demektir.", "Dörtgende komşu kenar bulunmaz.", "Öğrenci komşuluk ile karşılıklılık kavramlarını karıştırmıştır.", None),
    ])


def quadrilateral_diagonal_tasks():
    n = "tr-g06-matematik-note-014"
    return vrows(n, [
        ("comprehension", "Bir dörtgende komşu olmayan iki köşeyi birleştiren doğru parçasına ne denir?", "Köşegen",
         "Kenar", "Açıortay", "Yarıçap", "Köşegen karşılıklı iki köşeyi birleştirir.", None),
        ("comprehension", "Şemadaki ABCD dörtgeninde çizilmiş iki iç doğru parçası hangileridir?", "AC ve BD köşegenleri",
         "AB ve CD kenarları", "AD ve BC kenarları", "A ve C açıları", "AC ile BD karşılıklı köşeleri birleştirir.", "quad-diag"),
        ("comprehension", "Köşegenlerin birbirini ortalaması ne demektir?", "Kesişim noktasının her köşegeni iki eş parçaya ayırması",
         "Köşegenlerin zorunlu olarak dik olması", "Bütün kenarların eş olması", "Köşegenlerin kesişmemesi", "Ortalama, her köşegen üzerindeki iki parçanın eşliğidir.", None),
        ("comprehension", "Hangi dörtgen ailesinde köşegenler her zaman birbirini ortalar?", "Paralelkenarlar",
         "Bütün yamuklar", "Bütün deltoidler", "Herhangi dört noktanın oluşturduğu şekiller", "Paralelkenarın temel özelliklerinden biri köşegenlerin birbirini ortalamasıdır.", None),
        ("comprehension", "Dikdörtgenin köşegenleri için hangi ifade doğrudur?", "Birbirini ortalar ve uzunlukları eşittir.",
         "Birbirini hiç kesmez.", "Yalnız biri ortalanır.", "Her zaman birbirine diktir.", "Dikdörtgen paralelkenar ailesindedir ve eş köşegen özelliği taşır.", None),
        ("comprehension", "Eşkenar dörtgenin köşegenleri için hangi ek özellik geçerlidir?", "Birbirlerine diktirler.",
         "Birbirlerini ortalamazlar.", "Kesişim noktaları iki tanedir.", "Zorunlu olarak eş uzunluktadırlar.", "Eşkenar dörtgende köşegenler birbirini dik keserek ortalar.", None),
        ("application", "Şemada ABCD paralelkenarının köşegenleri O'da kesişiyor. AO=7 cm ise OC kaç santimetredir?", "7 cm",
         "3,5 cm", "14 cm", "21 cm", "Köşegenler birbirini ortaladığı için AO=OC'dir.", "quad-diag"),
        ("application", "Bir dikdörtgende AC köşegeni 18 cm ise BD köşegeni kaç santimetredir?", "18 cm",
         "9 cm", "36 cm", "12 cm", "Dikdörtgenin iki köşegeni eş uzunluktadır.", None),
        ("application", "Şemadaki eşkenar dörtgende AO=5 cm ve BO=8 cm'dir. AC ve BD köşegenlerinin toplamı kaç santimetredir?", "26 cm",
         "13 cm", "18 cm", "40 cm", "O orta nokta olduğundan AC=10 ve BD=16; toplam 26 cm'dir.", "quad-diag"),
        ("application", "Köşegenleri birbirini ortalayan bir dörtgen çizmek için hangi işlem uygundur?", "Ortak orta noktada kesişen iki doğru parçasının uçlarını sırayla birleştirmek",
         "Birbirini kesmeyen iki doğru parçası çizmek", "Üç rastgele noktayı birleştirmek", "Yalnız bir çember çizmek", "Ortak orta nokta koşulu kurulduğunda uçların sıralı birleşimi paralelkenar oluşturur.", None),
        ("application", "Şemada AO=x+3, OC=2x−4 ve köşegenler birbirini ortalıyor. x kaçtır?", "7",
         "5", "9", "11", "AO=OC olduğundan x+3=2x−4 ve x=7 olur.", "quad-diag"),
        ("application", "Bir paralelkenarda BO=3y−2, OD=y+6'dır. y kaçtır?", "4",
         "2", "6", "8", "BO=OD: 3y−2=y+6, 2y=8 ve y=4 olur.", None),
        ("application", "Köşegenleri eş, birbirini ortalayan fakat dik olmak zorunda olmayan dörtgen hangisidir?", "Dikdörtgen",
         "Genel eşkenar dörtgen", "Her yamuk", "Deltoid", "Eş ve birbirini ortalayan köşegenler dikdörtgen özelliğidir; diklik yalnız özel durumda gerekir.", None),
        ("analysis", "Şemadaki ABCD dörtgeninde AO=OC ve BO=OD ölçülüyor. Hangi sonuç en güçlü biçimde desteklenir?", "Köşegenler birbirini ortaladığı için ABCD bir paralelkenardır.",
         "ABCD kesinlikle karedir.", "Bütün kenarlar zorunlu eşittir.", "Köşegenler kesinlikle diktir.", "İki köşegenin karşılıklı parçalarının eşliği paralelkenar ölçütüdür.", "quad-diag"),
        ("analysis", "Bir dörtgende köşegenler birbirini ortalıyor ve diktir; ancak uzunlukları eş değil. Hangi sınıflandırma uygundur?", "Eşkenar dörtgen olabilir, kare değildir.",
         "Dikdörtgen olmak zorundadır.", "Yamuk olmak zorundadır.", "Hiçbir dörtgen bu özellikleri taşımaz.", "Diklik eşkenar dörtgeni, eş olmama ise kareyi dışlar.", None),
        ("analysis", "Köşegenleri eş ve birbirini dik ortalayan dörtgen için hangi sonuç desteklenir?", "Kare özelliklerini taşır.",
         "Yalnız genel paralelkenardır, başka sonuç çıkmaz.", "Kesinlikle yamuktur.", "Köşegenleri kesişmez.", "Eşlik, diklik ve karşılıklı ortalama birlikte kareyi belirler.", None),
        ("analysis", "Şemada AO=6, OC=6, BO=4 ve OD=5 ölçülmüştür. Dörtgen neden paralelkenar ölçütünü sağlamaz?", "BD köşegeni O'da iki eş parçaya ayrılmamıştır.",
         "AC köşegeni iki eş parçaya ayrılmıştır.", "Köşegenler kesiştiği için", "AO ile BO farklı olduğu için", "Her köşegen kendi iki parçasıyla karşılaştırılır; BO≠OD koşulu bozar.", "quad-diag"),
        ("analysis", "Bir dikdörtgenin köşegenleri O'da kesişiyor. AO=9 cm ise dört köşenin O'ya uzaklıkları için ne söylenir?", "AO=BO=CO=DO=9 cm",
         "Yalnız AO=CO, diğerleri bilinmez.", "BO ve DO 18 cm'dir.", "Bütün uzaklıklar farklıdır.", "Eş köşegenler ve ortak orta nokta dört yarı köşegeni eş yapar.", None),
        ("analysis", "Aynı orta noktada kesişen 12 cm ve 20 cm uzunluklu iki köşegenin uçları birleştiriliyor. Oluşan paralelkenarda yarı köşegenler hangileridir?", "6 cm ve 10 cm",
         "12 cm ve 20 cm", "4 cm ve 8 cm", "16 cm ve 32 cm", "Orta nokta her köşegeni iki eş parçaya böler.", None),
        ("error-analysis", "Bir öğrenci “Köşegenler birbirini ortalıyorsa dörtgen mutlaka karedir.” diyor. Hangi düzeltme doğrudur?", "Bu özellik paralelkenarı gösterir; kare için ek olarak eş kenar ve dik açı koşulları gerekir.",
         "Köşegenler hiçbir paralelkenarda ortalanmaz.", "Her paralelkenarın bütün kenarları eşittir.", "Karede köşegen bulunmaz.", "Öğrenci genel paralelkenar ölçütünü özel kare koşullarıyla karıştırmıştır.", None),
        ("error-analysis", "Bir öğrenci şemada AO=OC olduğuna bakıp 'köşegenler birbirini ortalıyor' sonucunu veriyor. Hangi eksik kontrol vardır?", "BO ile OD'nin de eş olup olmadığı denetlenmelidir.",
         "AB ile AC'nin aynı doğru olup olmadığı", "Yalnız açıların adları", "Dörtgenin renginin eş olup olmadığı", "Birbirini ortalama için iki köşegenin de kendi parçaları eş olmalıdır.", "quad-diag"),
        ("error-analysis", "Bir öğrenci “Dik kesişen her iki doğru parçası bir karenin köşegenidir.” diyor. Hangi düzeltme gerekir?", "Kare için doğru parçaları aynı orta noktada birbirini ortalamalı ve eş uzunlukta olmalıdır.",
         "Diklik tek başına bütün kare özelliklerini verir.", "Kare köşegenleri hiçbir zaman dik değildir.", "Doğru parçalarının uçları birleştirilemez.", "Diklik gerekli özelliklerden yalnız biridir; eşlik ve orta nokta da aranır.", None),
    ])


TASK_BUILDERS = [
    fraction_decimal_tasks, length_unit_tasks, mixed_representation_tasks,
    algebra_expression_tasks, pattern_tasks, algorithm_expression_tasks,
    parallel_angle_tasks, parallel_shape_tasks, quadrilateral_diagonal_tasks,
]


def verify_math_facts() -> None:
    assert abs(7 / 20 - 0.35) < 1e-12 and abs(5 / 4 - 1.25) < 1e-12
    assert 125 / 1000 == 1 / 8 and 13 * 25 == 325
    assert 5 / 12 > 3 / 8 and 27 / 99 == 0.2727272727272727
    assert 3.6 * 100 == 360 and 145 / 10 == 14.5 and 2 * 1000 + 350 == 2350
    assert [0.75 * 1000, 74000 / 100, 720] == [750, 740, 720]
    assert 240 * 15 / 100 == 36 and 400 * 0.8 - 30 == 290
    assert 15 + 6 * 4 == 39 and 5 + (6 - 1) * 4 == 25
    assert [2 * n + 3 for n in range(1, 5)] == [5, 7, 9, 11]
    assert 3 * 4 + 1 == 2 * 4 + 5 and 4 * 6 - 7 == 17
    assert 3 * 7 + 5 == 26 and 3 * (15 - 5) + 2 == 32
    assert 180 - 124 == 56 and 180 - 109 == 71 and 3 * 15 + 5 == 5 * 15 - 25
    assert 2 * 25 + 10 + 4 * 25 + 20 == 180 and 180 - 70 == 110
    assert 2 * (5 + 8) == 26 and 7 + 3 == 2 * 7 - 4 and 3 * 4 - 2 == 4 + 6


def main() -> int:
    verify_math_facts()
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1200:
        raise RuntimeError("validated first twelve batches must exist before batch 13")
    notes = read_notes_only(MATH_SOURCE)
    tasks = [item for builder in TASK_BUILDERS for item in builder()]
    if len(tasks) != 100:
        raise AssertionError(f"batch 13 must contain 100 tasks, got {len(tasks)}")
    expected_modes = {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
    if Counter(item["mode"] for item in tasks) != expected_modes:
        raise AssertionError(Counter(item["mode"] for item in tasks))
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    rows_out = []
    for local, item in enumerate(tasks, 1):
        row = make_record(local, item, notes[item["note"]], batch=13, number_base=1200)
        apply_geometry_visual(row, item, labels)
        rows_out.append(row)
    if Counter(row["correctIndex"] for row in rows_out) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer positions are not exactly balanced")
    if sum(bool(row.get("figure")) for row in rows_out) != 20:
        raise AssertionError("batch 13 must contain exactly 20 required geometry diagrams")
    OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + rows_out) + "\n",
        encoding="utf-8", newline="\n",
    )
    LABELS_OUTPUT.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({
        "batch": 13, "questions": 100, "mathematics": 100, "figures": 20,
        "total": 1300, "modes": dict(Counter(item["mode"] for item in tasks)),
        "sourceQuestionReads": 0, "figureSpec": "1.3.0",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
