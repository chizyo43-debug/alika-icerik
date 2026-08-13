"""Görünen ad biçimleri ve dile özgü soru kalıpları.

Wikidata etiketleri ham hâlde cümleye sokulduğunda "die Hauptstadt des Landes
Königreich der Niederlande" ya da "Brasil fica em América do Sul" gibi metinler
çıkıyordu: kimi resmî uzun ad, kimi artikelsiz. Burası iki işi yapar.

1. `display_name` — etiketi çocuğun duyduğu kısa ada indirger (`Hollanda
   Krallığı` → `Hollanda`, `スペイン王国` → `スペイン`, `베이징시` → `베이징`).
2. `country_forms` — her dilin cümlede istediği çekimli/edatlı biçimi üretir:
   Türkçe tamlayan eki, Almanca genitif, Fransızca/İspanyolca/Portekizce
   artikel kaynaşması, Rusça genitif, Korece ünsüz uyumlu ilgeç.

Kalıplar `TEMPLATES` içindedir; üreteç yalnız bu iki arayüzü çağırır.
Ad tabloları ISO 3166-1 alpha-2 koduna göre anahtarlanır, etiket metnine göre
değil: Wikidata etiketi değişirse kod bozulmasın diye.
"""
from __future__ import annotations


# --- Ülke adı düzeltmeleri -------------------------------------------------
# Yalnız resmî uzun ad, kayıt tutarsızlığı ya da bozuk etiket düzeltilir.
# "Kongo Demokratik Cumhuriyeti" gibi gerçekten kullanılan adlar korunur.
NAME_OVERRIDES: dict[str, dict[str, str]] = {
    "tr": {"NL": "Hollanda", "CN": "Çin", "NR": "Nauru"},
    "en": {
        "NL": "Netherlands", "CN": "China", "CZ": "Czechia", "NR": "Nauru",
        "BS": "Bahamas", "GM": "Gambia",
    },
    "de": {
        "NL": "Niederlande", "CN": "China", "TW": "Taiwan", "NR": "Nauru",
        "VC": "St. Vincent und Grenadinen",  # "von … und die Grenadinen" bozuktu
    },
    "es": {
        "NL": "Países Bajos", "CN": "China", "CZ": "Chequia", "TW": "Taiwán",
    },
    "fr": {
        "NL": "Pays-Bas", "CN": "Chine", "NR": "Nauru",
        "CD": "République démocratique du Congo",  # etikette küçük harfle geliyor
    },
    "pt": {
        "NL": "Países Baixos", "NR": "Nauru", "BF": "Burquina Faso",
        "KI": "Quiribáti",
    },
    "ru": {
        "NL": "Нидерланды", "KP": "Северная Корея", "KR": "Южная Корея",
        "TW": "Тайвань", "XK": "Косово",
    },
    "ja": {
        "NL": "オランダ", "ES": "スペイン", "NO": "ノルウェー", "TH": "タイ",
        "CZ": "チェコ", "ML": "マリ", "GW": "ギニアビサウ", "CN": "中国",
        "KP": "北朝鮮", "KR": "韓国", "XK": "コソボ", "MN": "モンゴル",
        "TW": "台湾", "US": "アメリカ",
    },
    "ko": {"NL": "네덜란드", "CN": "중국", "KP": "북한", "TW": "대만"},
}

# Başkent etiketlerindeki idari ekler ("北京市", "서울특별시"). Tablo açık
# tutulur: Korece "트빌리시" (Tiflis) adın kendisiyle biter, kesilmemeli.
CAPITAL_OVERRIDES: dict[str, dict[str, str]] = {
    "ja": {
        "BE": "ブリュッセル", "CN": "北京", "DJ": "ジブチ", "JP": "東京",
        "KP": "平壌", "KR": "ソウル", "KW": "クウェート", "LU": "ルクセンブルク",
        "PA": "パナマシティ", "SM": "サンマリノ", "TW": "台北",
    },
    "ko": {
        "CN": "베이징", "JP": "도쿄", "KP": "평양", "KR": "서울",
        "KW": "쿠웨이트시티", "TW": "타이베이", "VA": "바티칸",
    },
}

# --- Kıta -----------------------------------------------------------------
# Wikidata dil başına farklı bölümleme veriyordu: "Okyanusya" ile "Ada
# Okyanusyası" aynı soruda iki şık olarak çıkıyor, ikisi de savunulabilir
# doğru oluyordu. Altı kıtaya indiriyoruz. Avrasya bir kıta adı değil;
# hiçbir soruda doğru cevap olmadığı hâlde çeldirici olarak dolaşıyordu.
CONTINENT_KEYS = ("africa", "asia", "europe", "north_america", "south_america", "oceania")
CONTINENT_ALIASES: dict[str, str] = {
    "Africa": "africa", "Afrika": "africa", "Afrique": "africa", "África": "africa",
    "アフリカ": "africa", "아프리카": "africa", "Африка": "africa",
    "Asia": "asia", "Asien": "asia", "Asie": "asia", "Asya": "asia", "Ásia": "asia",
    "アジア": "asia", "아시아": "asia", "Азия": "asia",
    "Europe": "europe", "Europa": "europe", "Avrupa": "europe",
    "ヨーロッパ": "europe", "유럽": "europe", "Европа": "europe",
    "North America": "north_america", "Nordamerika": "north_america",
    "Amérique du Nord": "north_america", "América del Norte": "north_america",
    "América do Norte e América Central": "north_america",
    "Kuzey Amerika": "north_america", "北アメリカ": "north_america",
    "북아메리카": "north_america", "Северная Америка": "north_america",
    "South America": "south_america", "Südamerika": "south_america",
    "Amérique du Sud": "south_america", "América del Sur": "south_america",
    "América do Sul": "south_america", "Güney Amerika": "south_america",
    "南アメリカ": "south_america", "남아메리카": "south_america",
    "Южная Америка": "south_america",
    "Oceania": "oceania", "Ozeanien": "oceania", "Océanie": "oceania",
    "Oceanía": "oceania", "Oceanía insular": "oceania", "Okyanusya": "oceania",
    "Ada Okyanusyası": "oceania", "オセアニア": "oceania", "オセアニア島嶼部": "oceania",
    "오세아니아": "oceania", "Океания": "oceania", "Австралия и Океания": "oceania",
    # Avrasya bir kıta değil: eşlemesi yok, kıta kümesinden düşer.
}
CONTINENT_NAMES: dict[str, dict[str, str]] = {
    "tr": {"africa": "Afrika", "asia": "Asya", "europe": "Avrupa",
           "north_america": "Kuzey Amerika", "south_america": "Güney Amerika",
           "oceania": "Okyanusya"},
    "en": {"africa": "Africa", "asia": "Asia", "europe": "Europe",
           "north_america": "North America", "south_america": "South America",
           "oceania": "Oceania"},
    "de": {"africa": "Afrika", "asia": "Asien", "europe": "Europa",
           "north_america": "Nordamerika", "south_america": "Südamerika",
           "oceania": "Ozeanien"},
    "es": {"africa": "África", "asia": "Asia", "europe": "Europa",
           "north_america": "América del Norte", "south_america": "América del Sur",
           "oceania": "Oceanía"},
    "fr": {"africa": "Afrique", "asia": "Asie", "europe": "Europe",
           "north_america": "Amérique du Nord", "south_america": "Amérique du Sud",
           "oceania": "Océanie"},
    "pt": {"africa": "África", "asia": "Ásia", "europe": "Europa",
           "north_america": "América do Norte", "south_america": "América do Sul",
           "oceania": "Oceania"},
    "ru": {"africa": "Африка", "asia": "Азия", "europe": "Европа",
           "north_america": "Северная Америка", "south_america": "Южная Америка",
           "oceania": "Океания"},
    "ja": {"africa": "アフリカ", "asia": "アジア", "europe": "ヨーロッパ",
           "north_america": "北アメリカ", "south_america": "南アメリカ",
           "oceania": "オセアニア"},
    "ko": {"africa": "아프리카", "asia": "아시아", "europe": "유럽",
           "north_america": "북아메리카", "south_america": "남아메리카",
           "oceania": "오세아니아"},
}
# Rusça açıklama kıtayı edatlı hâlde ister.
RU_CONTINENT_PREPOSITIONAL = {
    "Африка": "Африке", "Азия": "Азии", "Европа": "Европе",
    "Северная Америка": "Северной Америке", "Южная Америка": "Южной Америке",
    "Океания": "Океании",
}

# Başkenti geçişte/yerelleştirilmemiş ya da siyasi olarak tartışmalı olan
# devletler. Kıta sorusuna girerler; başkent sorusuna girmezler. Ekvator
# Ginesi, Ciudad de la Paz'ı 2 Ocak 2026'da başkent ilan etti ve kurumların
# taşınması için bir yıllık geçiş öngördü; dondurulmuş etiket dokuz dilde de
# İspanyolca kaldığından bu sürümde sorulmuyor. Kudüs ise dokuz dile dağıtılan
# bir çocuk oyunu için siyasi olarak tartışmalıdır.
CONTESTED_CAPITALS = frozenset({"GQ", "IL"})

# Ülke ve başkent görünen adları bazı dillerde birebir eşit değildir
# (ör. Yibuti/Ciudad de Yibuti, 바티칸 시국/바티칸). Bu devletleri yalnız metin
# eşitliğiyle elemek diller arasında farklı sonuç verir.
SAME_NAME_CAPITALS = frozenset({"MC", "LU", "DJ", "VA"})


# --- Türkçe ---------------------------------------------------------------
_TR_VOWELS = "aeıioöuü"
_TR_HARMONY = {"a": "ı", "ı": "ı", "o": "u", "u": "u",
               "e": "i", "i": "i", "ö": "ü", "ü": "ü"}


def _tr_lower(char: str) -> str:
    # Python'un .lower()'ı Türkçe için yanlış: I → ı, İ → i elle yapılır.
    if char == "I":
        return "ı"
    if char == "İ":
        return "i"
    return char.lower()


# Yazılışta kalın ünlü var ama söyleyişte ince "l" ile bitiyor: ek incelir.
_TR_GENITIVE_EXCEPTIONS = {"Nepal": "Nepal'in", "Senegal": "Senegal'in"}


def _tr_genitive(name: str) -> str:
    """Özel ada kesme işaretiyle tamlayan eki getirir: İran → İran'ın."""
    if name in _TR_GENITIVE_EXCEPTIONS:
        return _TR_GENITIVE_EXCEPTIONS[name]
    vowel = next((_tr_lower(char) for char in reversed(name)
                  if _tr_lower(char) in _TR_VOWELS), "e")
    suffix = _TR_HARMONY[vowel]
    if _tr_lower(name[-1]) in _TR_VOWELS:
        return f"{name}'n{suffix}n"
    return f"{name}'{suffix}n"


# --- Korece ---------------------------------------------------------------
def _ko_topic(word: str) -> str:
    """Son hecede ünsüz varsa 은, yoksa 는."""
    code = ord(word.strip()[-1])
    if 0xAC00 <= code <= 0xD7A3:
        return "은" if (code - 0xAC00) % 28 else "는"
    return "는"


# --- Almanca --------------------------------------------------------------
# "die Hauptstadt {of}" — artikelsiz ülkeler "von X", artikelliler genitif.
_DE_ARTICLED = {
    "CH": ("der Schweiz", "die Schweiz", False),
    "TR": ("der Türkei", "die Türkei", False),
    "UA": ("der Ukraine", "die Ukraine", False),
    "SK": ("der Slowakei", "die Slowakei", False),
    "MN": ("der Mongolei", "die Mongolei", False),
    "CI": ("der Elfenbeinküste", "die Elfenbeinküste", False),
    "DO": ("der Dominikanischen Republik", "die Dominikanische Republik", False),
    "CF": ("der Zentralafrikanischen Republik", "die Zentralafrikanische Republik", False),
    "CD": ("der Demokratischen Republik Kongo", "die Demokratische Republik Kongo", False),
    "CG": ("der Republik Kongo", "die Republik Kongo", False),
    "IR": ("des Iran", "der Iran", False),
    "IQ": ("des Irak", "der Irak", False),
    "LB": ("des Libanon", "der Libanon", False),
    "SD": ("des Sudan", "der Sudan", False),
    "SS": ("des Südsudan", "der Südsudan", False),
    "TD": ("des Tschad", "der Tschad", False),
    "NE": ("des Niger", "der Niger", False),
    "XK": ("des Kosovo", "der Kosovo", False),
    "GB": ("des Vereinigten Königreichs", "das Vereinigte Königreich", False),
    "NL": ("der Niederlande", "die Niederlande", True),
    "US": ("der Vereinigten Staaten", "die Vereinigten Staaten", True),
    "PH": ("der Philippinen", "die Philippinen", True),
    "AE": ("der Vereinigten Arabischen Emirate", "die Vereinigten Arabischen Emirate", True),
    "MV": ("der Malediven", "die Malediven", True),
    "SC": ("der Seychellen", "die Seychellen", True),
    "KM": ("der Komoren", "die Komoren", True),
    "BS": ("der Bahamas", "die Bahamas", True),
    "SB": ("der Salomonen", "die Salomonen", True),
    "MH": ("der Marshallinseln", "die Marshallinseln", True),
    "FM": ("der Föderierten Staaten von Mikronesien",
           "die Föderierten Staaten von Mikronesien", True),
}


# --- Fransızca ------------------------------------------------------------
_FR_PLURAL = frozenset({"NL", "US", "AE", "FM", "PH", "MV", "SC", "KM", "BS",
                        "SB", "MH", "FJ", "PW"})
_FR_NO_ARTICLE = frozenset({"CU", "CY", "DJ", "HT", "IL", "KI", "MG", "MT",
                            "MU", "MC", "NR", "OM", "KN", "LC", "SM", "VC",
                            "WS", "ST", "SG", "TW", "TO", "TT", "TV", "VU",
                            "BH", "AG"})
_FR_MASCULINE_E = frozenset({"MX", "MZ", "ZW", "KH", "BZ", "SR"})
_FR_FEMININE = frozenset({"KP", "KR", "MK", "CD", "CG", "GW"})


def _fr_article(iso: str, name: str) -> str:
    if iso in _FR_PLURAL:
        return "les"
    if iso in _FR_NO_ARTICLE:
        return ""
    if name[0] in "AEIOUYÀÂÉÈÊÎÔÖÛÜaeiouy":
        return "l'"
    if iso in _FR_FEMININE:
        return "la"
    if iso in _FR_MASCULINE_E:
        return "le"
    return "la" if name.endswith("e") else "le"


# --- İspanyolca -----------------------------------------------------------
_ES_ARTICLE = {
    "NL": "los", "US": "los", "AE": "los", "FM": "los", "GB": "el", "CG": "el",
    "DO": "la", "CF": "la", "CD": "la", "IN": "la", "VA": "la",
    "MV": "las", "SC": "las", "KM": "las", "SB": "las", "MH": "las", "BS": "las",
}


# --- Portekizce -----------------------------------------------------------
_PT_PLURAL = {"NL": "os", "US": "os", "AE": "os", "PH": "as", "MV": "as",
              "SC": "as", "KM": "as", "SB": "as", "MH": "as", "BS": "as",
              "CM": "os"}
_PT_NO_ARTICLE = frozenset({"PT", "AO", "MZ", "CV", "ST", "TL", "IL", "CU",
                            "AD", "MT", "SG", "SV", "NR", "KI", "TV", "VU",
                            "PW", "FJ", "WS", "TO", "BZ", "GD", "DM", "LC",
                            "SM", "AG", "KN", "VC", "TT", "MA", "HN", "MC",
                            "BB", "MG", "TW"})
_PT_FEMININE = frozenset({"GN", "GW", "GQ", "KP", "KR", "MK", "CI", "CD",
                          "CG", "PG"})
_PT_MASCULINE_A = frozenset({"KE", "UG", "BW", "RW", "GH", "KH"})


def _pt_article(iso: str, name: str) -> str:
    if iso in _PT_PLURAL:
        return _PT_PLURAL[iso]
    if iso in _PT_NO_ARTICLE:
        return ""
    if iso in _PT_FEMININE:
        return "a"
    if iso in _PT_MASCULINE_A:
        return "o"
    return "a" if name.endswith("a") else "o"


_PT_DE = {"o": "do", "a": "da", "os": "dos", "as": "das", "": "de"}
_ES_DE = {"el": "del", "la": "de la", "los": "de los", "las": "de las", "": "de"}


# --- Rusça ----------------------------------------------------------------
_RU_GENITIVE_EXCEPTIONS = {
    "Беларусь": "Беларуси",
    "Египет": "Египта",
    "Маврикий": "Маврикия",
    "Никарагуа": "Никарагуа",
    "Самоа": "Самоа",
    "Тонга": "Тонга",
    "Гвинея-Бисау": "Гвинеи-Бисау",
    "Коморы": "Комор",
    "Мальдивы": "Мальдив",
    "Филиппины": "Филиппин",
    "Нидерланды": "Нидерландов",
    "США": "США",
    "Босния и Герцеговина": "Боснии и Герцеговины",
    "Антигуа и Барбуда": "Антигуа и Барбуды",
    "Тринидад и Тобаго": "Тринидада и Тобаго",
    "Сент-Китс и Невис": "Сент-Китса и Невиса",
    "Сент-Винсент и Гренадины": "Сент-Винсента и Гренадин",
    "Сан-Томе и Принсипи": "Сан-Томе и Принсипи",
    "Папуа — Новая Гвинея": "Папуа — Новой Гвинеи",
    "Северная Македония": "Северной Македонии",
    "Новая Зеландия": "Новой Зеландии",
    "Саудовская Аравия": "Саудовской Аравии",
    "Южный Судан": "Южного Судана",
    "Восточный Тимор": "Восточного Тимора",
    "Экваториальная Гвинея": "Экваториальной Гвинеи",
    "Северная Корея": "Северной Кореи",
    "Южная Корея": "Южной Кореи",
    "Демократическая Республика Конго": "Демократической Республики Конго",
    "Центральноафриканская Республика": "Центральноафриканской Республики",
    "Республика Конго": "Республики Конго",
    "Доминиканская Республика": "Доминиканской Республики",
    "Федеративные Штаты Микронезии": "Федеративных Штатов Микронезии",
    "Объединённые Арабские Эмираты": "Объединённых Арабских Эмиратов",
    "Багамские Острова": "Багамских Островов",
    "Соломоновы Острова": "Соломоновых Островов",
    "Маршалловы Острова": "Маршалловых Островов",
    "Сейшельские Острова": "Сейшельских Островов",
}
_RU_PLURAL = frozenset({"NL", "US", "AE", "PH", "MV", "SC", "KM", "BS", "SB",
                        "MH", "FM"})


def _ru_genitive(name: str) -> str:
    if name in _RU_GENITIVE_EXCEPTIONS:
        return _RU_GENITIVE_EXCEPTIONS[name]
    if name.endswith("ия"):
        return name[:-2] + "ии"
    if name.endswith("я"):
        return name[:-1] + "и"
    if name.endswith("а"):
        return name[:-1] + ("и" if name[-2] in "кгхжчшщ" else "ы")
    if name.endswith("ь") or name.endswith("й"):
        return name[:-1] + "я"
    if name[-1] in "оуеэию":
        return name  # çekimsiz: Чили, Перу, Конго, Зимбабве
    return name + "а"


# --- Kalıplar -------------------------------------------------------------
# Her dil için üç soru ve üç açıklama. Biçimlendirme anahtarları
# `country_forms` çıktısından gelir.
TEMPLATES: dict[str, dict[str, str]] = {
    "tr": {
        "capital": "{gen} başkenti neresidir?",
        "country": "{capital} hangi ülkenin başkentidir?",
        "continent": "{name} hangi kıtada yer alır?",
        "capital_explanation": "{capital}, {gen} başkentidir.",
        "country_explanation": "{capital}, {gen} başkentidir.",
        "continent_explanation": "{name}, {continent} kıtasında yer alır.",
    },
    "en": {
        "capital": "What is the capital of {of}?",
        "country": "{capital} is the capital of which country?",
        "continent": "Which continent is {of} in?",
        "capital_explanation": "{capital} is the capital of {of}.",
        "country_explanation": "{capital} is the capital of {of}.",
        "continent_explanation": "{Subj} is in {continent}.",
    },
    "de": {
        "capital": "Wie heißt die Hauptstadt {of}?",
        "country": "{capital} ist die Hauptstadt welches Landes?",
        "continent": "Auf welchem Kontinent {verb} {subj}?",
        "capital_explanation": "{capital} ist die Hauptstadt {of}.",
        "country_explanation": "{capital} ist die Hauptstadt {of}.",
        "continent_explanation": "{Subj} {verb} in {continent}.",
    },
    "es": {
        "capital": "¿Cuál es la capital {of}?",
        "country": "¿De qué país es capital {capital}?",
        "continent": "¿En qué continente {verb} {subj}?",
        "capital_explanation": "{capital} es la capital {of}.",
        "country_explanation": "{capital} es la capital {of}.",
        "continent_explanation": "{Subj} {verb} en {continent}.",
    },
    "fr": {
        "capital": "Quelle est la capitale {of} ?",
        "country": "{capital} est la capitale de quel pays ?",
        "continent": "Sur quel continent {verb} {subj} ?",
        "capital_explanation": "{capital} est la capitale {of}.",
        "country_explanation": "{capital} est la capitale {of}.",
        "continent_explanation": "{Subj} {verb} en {continent}.",
    },
    "pt": {
        "capital": "Qual é a capital {of}?",
        "country": "{capital} é a capital de que país?",
        "continent": "Em que continente {verb} {subj}?",
        "capital_explanation": "{capital} é a capital {of}.",
        "country_explanation": "{capital} é a capital {of}.",
        "continent_explanation": "{Subj} {verb} na {continent}.",
    },
    "ru": {
        "capital": "Какой город является столицей {gen}?",
        "country": "Столицей какой страны является {capital}?",
        "continent": "На каком континенте {verb} {name}?",
        "capital_explanation": "{capital} — столица {gen}.",
        "country_explanation": "{capital} — столица {gen}.",
        "continent_explanation": "{name} {verb} в {continent_prep}.",
    },
    "ja": {
        "capital": "{name}の首都はどこですか？",
        "country": "{capital}はどの国の首都ですか？",
        "continent": "{name}はどの大陸にありますか？",
        "capital_explanation": "{name}の首都は{capital}です。",
        "country_explanation": "{capital}は{name}の首都です。",
        "continent_explanation": "{name}は{continent}にあります。",
    },
    "ko": {
        "capital": "{name}의 수도는 어디인가요?",
        "country": "수도가 {capital}인 나라는 어디인가요?",
        "continent": "{name}{topic} 어느 대륙에 있나요?",
        "capital_explanation": "{name}의 수도는 {capital}입니다.",
        "country_explanation": "{name}의 수도는 {capital}입니다.",
        "continent_explanation": "{name}{topic} {continent}에 있습니다.",
    },
}


def display_name(language: str, iso2: str, label: str) -> str:
    return NAME_OVERRIDES.get(language, {}).get(iso2, label)


def display_capital(language: str, iso2: str, label: str) -> str:
    return CAPITAL_OVERRIDES.get(language, {}).get(iso2, label)


def country_forms(language: str, iso2: str, name: str) -> dict[str, str]:
    """Kalıpların istediği bütün ad biçimlerini üretir."""
    forms = {"name": name}
    if language == "tr":
        forms["gen"] = _tr_genitive(name)
    elif language == "en":
        article = iso2 in {
            "US", "GB", "NL", "PH", "AE", "DO", "CD", "CG", "CF", "MV", "SC",
            "KM", "SB", "MH", "FM", "BS", "GM",
        }
        forms["of"] = f"the {name}" if article else name
        forms["Subj"] = f"The {name}" if article else name
    elif language == "de":
        of, subj, plural = _DE_ARTICLED.get(iso2, (f"von {name}", name, False))
        forms["of"] = of
        forms["subj"] = subj
        forms["Subj"] = subj[0].upper() + subj[1:]
        forms["verb"] = "liegen" if plural else "liegt"
    elif language == "fr":
        article = _fr_article(iso2, name)
        subj = f"{article}{name}" if article == "l'" else (
            f"{article} {name}" if article else name)
        of = {"le": f"du {name}", "les": f"des {name}", "la": f"de la {name}",
              "l'": f"de l'{name}", "": f"de {name}"}[article]
        if not article and name[0] in "AEIOUYHÀÂÉÈÊÎÔÖÛÜaeiouyh":
            of = f"d'{name}"
        forms["of"] = of
        forms["subj"] = subj
        forms["Subj"] = subj[0].upper() + subj[1:]
        forms["verb"] = "se trouvent" if article == "les" else "se trouve"
    elif language == "es":
        article = _ES_ARTICLE.get(iso2, "")
        subj = f"{article} {name}" if article else name
        forms["of"] = f"{_ES_DE[article]} {name}"
        forms["subj"] = subj
        forms["Subj"] = subj[0].upper() + subj[1:]
        forms["verb"] = "están" if article in {"los", "las"} else "está"
    elif language == "pt":
        article = _pt_article(iso2, name)
        subj = f"{article} {name}" if article else name
        forms["of"] = f"{_PT_DE[article]} {name}"
        forms["subj"] = subj
        forms["Subj"] = subj[0].upper() + subj[1:]
        forms["verb"] = "ficam" if article in {"os", "as"} else "fica"
    elif language == "ru":
        forms["gen"] = _ru_genitive(name)
        forms["verb"] = "находятся" if iso2 in _RU_PLURAL else "находится"
    elif language == "ko":
        forms["topic"] = _ko_topic(name)
    return forms
