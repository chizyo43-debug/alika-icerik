"""Localized garden settings and plants for AliKa Garden Masters."""
from __future__ import annotations


KITS = {
    "tr": [
        {"garden": "Anadolu avlu bahçesi", "style": "çini bordür"},
        {"garden": "Ege teras bahçesi", "style": "beyaz taş yol"},
        {"garden": "Karadeniz yağmur bahçesi", "style": "ahşap yükseltilmiş yatak"},
        {"garden": "İstanbul bostanı", "style": "tuğla patika"},
        {"garden": "Akdeniz güneş bahçesi", "style": "mozaik saksı"},
    ],
    "en": [
        {"garden": "cottage kitchen garden", "style": "woven willow edge"},
        {"garden": "coastal raised garden", "style": "pale stone path"},
        {"garden": "city community garden", "style": "reclaimed timber bed"},
        {"garden": "woodland edge garden", "style": "bark path"},
        {"garden": "sunny allotment", "style": "brick border"},
    ],
    "de": [
        {"garden": "Bauerngarten", "style": "Buchsbaumrand"},
        {"garden": "Alpenkräutergarten", "style": "Natursteinweg"},
        {"garden": "Stadtgemeinschaftsgarten", "style": "Holzhochbeet"},
        {"garden": "Rheinterrasse", "style": "Kiesweg"},
        {"garden": "Waldgarten", "style": "Rindenpfad"},
    ],
    "es": [
        {"garden": "huerto de patio", "style": "borde de azulejos"},
        {"garden": "terraza mediterránea", "style": "camino de piedra clara"},
        {"garden": "huerto comunitario", "style": "bancal de madera"},
        {"garden": "jardín andino", "style": "borde tejido"},
        {"garden": "jardín tropical", "style": "sendero de colores"},
    ],
    "fr": [
        {"garden": "potager de village", "style": "bordure tressée"},
        {"garden": "terrasse provençale", "style": "allée de pierre claire"},
        {"garden": "jardin partagé", "style": "bac en bois"},
        {"garden": "jardin de sous-bois", "style": "sentier d'écorce"},
        {"garden": "potager du littoral", "style": "bordure de galets"},
    ],
    "pt": [
        {"garden": "horta de quintal", "style": "borda de azulejos"},
        {"garden": "terraço atlântico", "style": "caminho de pedra"},
        {"garden": "horta comunitária", "style": "canteiro de madeira"},
        {"garden": "jardim tropical", "style": "trilha colorida"},
        {"garden": "horta serrana", "style": "borda trançada"},
    ],
    "ru": [
        {"garden": "деревенский огород", "style": "плетёный бордюр"},
        {"garden": "северный сад", "style": "деревянная грядка"},
        {"garden": "городской общий сад", "style": "кирпичная дорожка"},
        {"garden": "лесной огород", "style": "дорожка из коры"},
        {"garden": "солнечная дача", "style": "каменный бордюр"},
    ],
    "ja": [
        {"garden": "町家の菜園", "style": "竹の縁取り"},
        {"garden": "里山の畑", "style": "飛び石の小道"},
        {"garden": "地域の共同菜園", "style": "木の高床花壇"},
        {"garden": "海辺の庭", "style": "白砂の小道"},
        {"garden": "山の薬味畑", "style": "石組みの縁"},
    ],
    "ko": [
        {"garden": "한옥 텃밭", "style": "대나무 테두리"},
        {"garden": "산골 채소밭", "style": "돌길"},
        {"garden": "마을 공동정원", "style": "나무 화단"},
        {"garden": "바닷가 정원", "style": "밝은 자갈길"},
        {"garden": "도시 옥상 텃밭", "style": "벽돌 테두리"},
    ],
}


PLANTS = {
    "tr": [
        ("domates", "fruiting", 3, 2), ("biber", "fruiting", 3, 2),
        ("fesleğen", "herb", 2, 2), ("kekik", "herb", 3, 1),
        ("kadife çiçeği", "flower", 3, 2), ("marul", "leafy", 2, 2),
        ("maydanoz", "herb", 2, 2), ("çilek", "fruiting", 3, 2),
        ("havuç", "root", 3, 2), ("fasulye", "fruiting", 3, 2),
    ],
    "en": [
        ("tomato", "fruiting", 3, 2), ("pea", "fruiting", 2, 2),
        ("lavender", "flower", 3, 1), ("rosemary", "herb", 3, 1),
        ("marigold", "flower", 3, 2), ("lettuce", "leafy", 2, 2),
        ("parsley", "herb", 2, 2), ("strawberry", "fruiting", 3, 2),
        ("carrot", "root", 3, 2), ("bean", "fruiting", 3, 2),
    ],
    "de": [
        ("Tomate", "fruiting", 3, 2), ("Erbse", "fruiting", 2, 2),
        ("Lavendel", "flower", 3, 1), ("Schnittlauch", "herb", 2, 2),
        ("Ringelblume", "flower", 3, 2), ("Kopfsalat", "leafy", 2, 2),
        ("Petersilie", "herb", 2, 2), ("Erdbeere", "fruiting", 3, 2),
        ("Möhre", "root", 3, 2), ("Buschbohne", "fruiting", 3, 2),
    ],
    "es": [
        ("tomate", "fruiting", 3, 2), ("pimiento", "fruiting", 3, 2),
        ("lavanda", "flower", 3, 1), ("romero", "herb", 3, 1),
        ("caléndula", "flower", 3, 2), ("lechuga", "leafy", 2, 2),
        ("perejil", "herb", 2, 2), ("fresa", "fruiting", 3, 2),
        ("zanahoria", "root", 3, 2), ("frijol", "fruiting", 3, 2),
    ],
    "fr": [
        ("tomate", "fruiting", 3, 2), ("petit pois", "fruiting", 2, 2),
        ("lavande", "flower", 3, 1), ("thym", "herb", 3, 1),
        ("souci", "flower", 3, 2), ("laitue", "leafy", 2, 2),
        ("persil", "herb", 2, 2), ("fraise", "fruiting", 3, 2),
        ("carotte", "root", 3, 2), ("haricot", "fruiting", 3, 2),
    ],
    "pt": [
        ("tomate", "fruiting", 3, 2), ("pimentão", "fruiting", 3, 2),
        ("lavanda", "flower", 3, 1), ("alecrim", "herb", 3, 1),
        ("calêndula", "flower", 3, 2), ("alface", "leafy", 2, 2),
        ("salsa", "herb", 2, 2), ("morango", "fruiting", 3, 2),
        ("cenoura", "root", 3, 2), ("feijão", "fruiting", 3, 2),
    ],
    "ru": [
        ("помидор", "fruiting", 3, 2), ("горох", "fruiting", 2, 2),
        ("лаванда", "flower", 3, 1), ("укроп", "herb", 2, 2),
        ("календула", "flower", 3, 2), ("салат", "leafy", 2, 2),
        ("петрушка", "herb", 2, 2), ("клубника", "fruiting", 3, 2),
        ("морковь", "root", 3, 2), ("фасоль", "fruiting", 3, 2),
    ],
    "ja": [
        ("トマト", "fruiting", 3, 2), ("エンドウ", "fruiting", 2, 2),
        ("シソ", "herb", 2, 2), ("ローズマリー", "herb", 3, 1),
        ("マリーゴールド", "flower", 3, 2), ("コマツナ", "leafy", 2, 2),
        ("ミツバ", "herb", 2, 2), ("イチゴ", "fruiting", 3, 2),
        ("ニンジン", "root", 3, 2), ("インゲン", "fruiting", 3, 2),
    ],
    "ko": [
        ("토마토", "fruiting", 3, 2), ("완두콩", "fruiting", 2, 2),
        ("들깨", "herb", 2, 2), ("로즈메리", "herb", 3, 1),
        ("금잔화", "flower", 3, 2), ("상추", "leafy", 2, 2),
        ("미나리", "herb", 2, 3), ("딸기", "fruiting", 3, 2),
        ("당근", "root", 3, 2), ("강낭콩", "fruiting", 3, 2),
    ],
}
