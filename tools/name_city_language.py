"""Localized alphabets and category labels for AliKa Name–City."""
from __future__ import annotations


ALPHABETS = {
    "tr": tuple("ABCÇDEFGHIİKLMNOPRSŞTUYZ"),
    "en": tuple("ABCDEFGHIJKLMNOPRSTW"),
    "de": tuple("ABCDEFGHIJKLMNOPRSTUW"),
    "es": tuple("ABCDEFGHIJKLMNOPRSTUV"),
    "fr": tuple("ABCDEFGHIJKLMNOPRSTV"),
    "pt": tuple("ABCDEFGHIJKLMNOPRSTV"),
    "ru": tuple("АБВГДЕЖЗИКЛМНОПРСТУФХЧШЯ"),
    "ja": ("あ", "か", "さ", "た", "な", "は", "ま", "や", "ら", "わ"),
    "ko": ("ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"),
}

INITIAL_MODES = {**{language: "letter" for language in ("tr", "en", "de", "es", "fr", "pt", "ru")},
                 "ja": "kana_row", "ko": "choseong"}

CATEGORY_IDS = ("person", "city", "animal", "plant", "object", "food", "country",
                "profession", "place", "sport", "artist", "tradition")

CATEGORIES = {
    "tr": ("İsim", "Şehir", "Hayvan", "Bitki", "Eşya", "Yemek", "Ülke", "Meslek", "Gezilecek yer", "Spor", "Sanatçı", "Gelenek"),
    "en": ("Name", "City", "Animal", "Plant", "Object", "Food", "Country", "Profession", "Place to visit", "Sport", "Artist", "Tradition"),
    "de": ("Name", "Stadt", "Tier", "Pflanze", "Gegenstand", "Essen", "Land", "Beruf", "Ausflugsziel", "Sport", "Künstler", "Tradition"),
    "es": ("Nombre", "Ciudad", "Animal", "Planta", "Objeto", "Comida", "País", "Profesión", "Lugar para visitar", "Deporte", "Artista", "Tradición"),
    "fr": ("Prénom", "Ville", "Animal", "Plante", "Objet", "Plat", "Pays", "Métier", "Lieu à visiter", "Sport", "Artiste", "Tradition"),
    "pt": ("Nome", "Cidade", "Animal", "Planta", "Objeto", "Comida", "País", "Profissão", "Lugar para visitar", "Esporte", "Artista", "Tradição"),
    "ru": ("Имя", "Город", "Животное", "Растение", "Предмет", "Блюдо", "Страна", "Профессия", "Место", "Спорт", "Артист", "Традиция"),
    "ja": ("名前", "都市", "動物", "植物", "物", "食べ物", "国", "仕事", "名所", "スポーツ", "芸術家", "伝統"),
    "ko": ("이름", "도시", "동물", "식물", "물건", "음식", "나라", "직업", "명소", "운동", "예술가", "전통"),
}

CULTURE_FOCUS = {
    "tr": ("yerel yemek", "Türkiye'den şehir", "Anadolu bitkisi", "yerel sanatçı", "aile geleneği"),
    "en": ("regional food", "local city", "native plant", "local artist", "family tradition"),
    "de": ("regionales Essen", "deutsche Stadt", "heimische Pflanze", "lokaler Künstler", "Familientradition"),
    "es": ("comida regional", "ciudad local", "planta autóctona", "artista local", "tradición familiar"),
    "fr": ("plat régional", "ville locale", "plante locale", "artiste local", "tradition familiale"),
    "pt": ("comida regional", "cidade local", "planta nativa", "artista local", "tradição familiar"),
    "ru": ("местное блюдо", "родной город", "местное растение", "местный артист", "семейная традиция"),
    "ja": ("郷土料理", "日本の都市", "身近な植物", "地域の芸術家", "家族の伝統"),
    "ko": ("향토 음식", "한국의 도시", "우리 식물", "지역 예술가", "가족 전통"),
}
