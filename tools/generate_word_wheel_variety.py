"""Generate familiar, mixed word-wheel pools from frozen reviewed sources.

The wheel is a word puzzle, not an exam.  Every pool deliberately mixes simple
emoji vocabulary, arithmetic written as words, space, familiar people and a
limited amount of geography.  People are an explicit familiarity allow-list;
obscure poets, ancient dates and specialist names cannot enter accidentally.
"""
from __future__ import annotations

import json
import random
import re
from pathlib import Path
from typing import Any

from build_word_wheel_games import BANDS, LANGUAGES, PUZZLES_PER_POOL, ROOT
from generate_trivia_geography import FOCUS, _age_ordered, _prepare
from generate_word_wheel_geography import (
    CATEGORIES as GEO_CATEGORIES,
    CONTINENT_CLUES,
    DATA_PATH,
)
from trivia_language import (
    CONTESTED_CAPITALS,
    CONTINENT_NAMES,
    SAME_NAME_CAPITALS,
    TEMPLATES,
    country_forms,
)


PEOPLE_PATH = ROOT / "games" / "who-is-it" / "data" / "wikidata_people.json"
LANGUAGE_INDEX = {language: index for index, language in enumerate(LANGUAGES)}

# Globally familiar figures with complete labels and descriptions in all nine
# languages.  Deliberately excludes niche poets and specialist historical names.
FAMILIAR_PEOPLE = (
    "Q935", "Q8023", "Q1001", "Q255", "Q307", "Q5593", "Q5582", "Q882",
    "Q5592", "Q5152", "Q8743", "Q8027", "Q8739", "Q5673", "Q19837",
    "Q1615", "Q34969", "Q9036", "Q303", "Q619", "Q8704", "Q529", "Q892",
    "Q7327", "Q8768", "Q17714", "Q30547", "Q5588", "Q91", "Q1339",
)

CATEGORIES = {
    "tr": {"people": "Tanınmış kişiler", "math": "Sayı bulmacası", "science": "Uzay",
           "animals": "Hayvanlar", "food": "Yiyecekler", "fun": "Spor ve nesneler"},
    "en": {"people": "Familiar people", "math": "Number puzzle", "science": "Space",
           "animals": "Animals", "food": "Food", "fun": "Sports and objects"},
    "de": {"people": "Bekannte Personen", "math": "Zahlenrätsel", "science": "Weltraum",
           "animals": "Tiere", "food": "Essen", "fun": "Sport und Gegenstände"},
    "es": {"people": "Personas conocidas", "math": "Acertijo numérico", "science": "Espacio",
           "animals": "Animales", "food": "Alimentos", "fun": "Deportes y objetos"},
    "fr": {"people": "Personnes connues", "math": "Énigme de nombres", "science": "Espace",
           "animals": "Animaux", "food": "Aliments", "fun": "Sports et objets"},
    "pt": {"people": "Pessoas conhecidas", "math": "Desafio numérico", "science": "Espaço",
           "animals": "Animais", "food": "Alimentos", "fun": "Esportes e objetos"},
    "ru": {"people": "Известные люди", "math": "Числовая загадка", "science": "Космос",
           "animals": "Животные", "food": "Еда", "fun": "Спорт и предметы"},
    "ja": {"people": "よく知られた人物", "math": "数字パズル", "science": "宇宙",
           "animals": "動物", "food": "食べ物", "fun": "スポーツと物"},
    "ko": {"people": "잘 알려진 인물", "math": "숫자 퍼즐", "science": "우주",
           "animals": "동물", "food": "음식", "fun": "스포츠와 사물"},
}

TEXT = {
    "tr": {"person": "Bu tanınmış kişiyi bul: {description}", "emoji": "{emoji} emojisi hangi kelimeyi anlatıyor?",
           "math": "{left} + {right} kaç eder? Cevabı yazıyla bul.", "planet": "Güneş'e {order}. sıradaki gezegeni bul.",
           "correct": "Doğru cevap: {answer}.", "emoji_explanation": "{emoji} emojisi {answer} kelimesini anlatır."},
    "en": {"person": "Find this familiar person: {description}", "emoji": "Which word does the {emoji} emoji show?",
           "math": "Write the result of {left} + {right} as a word.", "planet": "Find planet number {order} from the Sun.",
           "correct": "Correct answer: {answer}.", "emoji_explanation": "The {emoji} emoji represents {answer}."},
    "de": {"person": "Finde diese bekannte Person: {description}", "emoji": "Welches Wort passt zum Emoji {emoji}?",
           "math": "Schreibe das Ergebnis von {left} + {right} als Wort.", "planet": "Finde den {order}. Planeten von der Sonne.",
           "correct": "Richtige Antwort: {answer}.", "emoji_explanation": "Das Emoji {emoji} steht für {answer}."},
    "es": {"person": "Encuentra a esta persona conocida: {description}", "emoji": "¿Qué palabra muestra el emoji {emoji}?",
           "math": "Escribe con letras el resultado de {left} + {right}.", "planet": "Encuentra el planeta número {order} desde el Sol.",
           "correct": "Respuesta correcta: {answer}.", "emoji_explanation": "El emoji {emoji} representa {answer}."},
    "fr": {"person": "Trouve cette personne connue : {description}", "emoji": "Quel mot représente l’émoji {emoji} ?",
           "math": "Écris en lettres le résultat de {left} + {right}.", "planet": "Trouve la planète numéro {order} à partir du Soleil.",
           "correct": "Bonne réponse : {answer}.", "emoji_explanation": "L’émoji {emoji} représente {answer}."},
    "pt": {"person": "Encontre esta pessoa conhecida: {description}", "emoji": "Que palavra o emoji {emoji} mostra?",
           "math": "Escreva por extenso o resultado de {left} + {right}.", "planet": "Encontre o planeta número {order} a partir do Sol.",
           "correct": "Resposta correta: {answer}.", "emoji_explanation": "O emoji {emoji} representa {answer}."},
    "ru": {"person": "Узнайте этого известного человека: {description}", "emoji": "Какое слово показывает эмодзи {emoji}?",
           "math": "Запишите словами результат {left} + {right}.", "planet": "Найдите {order}-ю планету от Солнца.",
           "correct": "Правильный ответ: {answer}.", "emoji_explanation": "Эмодзи {emoji} означает «{answer}»."},
    "ja": {"person": "このよく知られた人物を当てましょう：{description}", "emoji": "絵文字{emoji}が表す言葉は何ですか？",
           "math": "{left}＋{right}の答えを言葉で書きましょう。", "planet": "太陽から{order}番目の惑星を当てましょう。",
           "correct": "正解は{answer}です。", "emoji_explanation": "絵文字{emoji}は{answer}を表します。"},
    "ko": {"person": "이 잘 알려진 인물을 맞혀 보세요: {description}", "emoji": "{emoji} 이모지는 어떤 낱말을 나타내나요?",
           "math": "{left} + {right}의 답을 글자로 써 보세요.", "planet": "태양에서 {order}번째 행성을 맞혀 보세요.",
           "correct": "정답은 {answer}입니다.", "emoji_explanation": "{emoji} 이모지는 {answer}을 나타냅니다."},
}

# emoji, category, then answers in LANGUAGES order: tr,en,de,es,fr,pt,ru,ja,ko
EMOJI_WORDS = (
    ("🐶", "animals", "köpek", "dog", "Hund", "perro", "chien", "cão", "собака", "犬", "개"),
    ("🐱", "animals", "kedi", "cat", "Katze", "gato", "chat", "gato", "кошка", "猫", "고양이"),
    ("🦁", "animals", "aslan", "lion", "Löwe", "león", "lion", "leão", "лев", "ライオン", "사자"),
    ("🐘", "animals", "fil", "elephant", "Elefant", "elefante", "éléphant", "elefante", "слон", "ゾウ", "코끼리"),
    ("🦒", "animals", "zürafa", "giraffe", "Giraffe", "jirafa", "girafe", "girafa", "жираф", "キリン", "기린"),
    ("🦓", "animals", "zebra", "zebra", "Zebra", "cebra", "zèbre", "zebra", "зебра", "シマウマ", "얼룩말"),
    ("🐒", "animals", "maymun", "monkey", "Affe", "mono", "singe", "macaco", "обезьяна", "サル", "원숭이"),
    ("🐼", "animals", "panda", "panda", "Panda", "panda", "panda", "panda", "панда", "パンダ", "판다"),
    ("🐨", "animals", "koala", "koala", "Koala", "koala", "koala", "coala", "коала", "コアラ", "코알라"),
    ("🐯", "animals", "kaplan", "tiger", "Tiger", "tigre", "tigre", "tigre", "тигр", "トラ", "호랑이"),
    ("🐻", "animals", "ayı", "bear", "Bär", "oso", "ours", "urso", "медведь", "クマ", "곰"),
    ("🦊", "animals", "tilki", "fox", "Fuchs", "zorro", "renard", "raposa", "лиса", "キツネ", "여우"),
    ("🐰", "animals", "tavşan", "rabbit", "Kaninchen", "conejo", "lapin", "coelho", "кролик", "ウサギ", "토끼"),
    ("🐢", "animals", "kaplumbağa", "turtle", "Schildkröte", "tortuga", "tortue", "tartaruga", "черепаха", "カメ", "거북이"),
    ("🐬", "animals", "yunus", "dolphin", "Delfin", "delfín", "dauphin", "golfinho", "дельфин", "イルカ", "돌고래"),
    ("🐋", "animals", "balina", "whale", "Wal", "ballena", "baleine", "baleia", "кит", "クジラ", "고래"),
    ("🐙", "animals", "ahtapot", "octopus", "Oktopus", "pulpo", "pieuvre", "polvo", "осьминог", "タコ", "문어"),
    ("🐧", "animals", "penguen", "penguin", "Pinguin", "pingüino", "pingouin", "pinguim", "пингвин", "ペンギン", "펭귄"),
    ("🦉", "animals", "baykuş", "owl", "Eule", "búho", "hibou", "coruja", "сова", "フクロウ", "부엉이"),
    ("🐝", "animals", "arı", "bee", "Biene", "abeja", "abeille", "abelha", "пчела", "ミツバチ", "벌"),
    ("🍎", "food", "elma", "apple", "Apfel", "manzana", "pomme", "maçã", "яблоко", "りんご", "사과"),
    ("🍌", "food", "muz", "banana", "Banane", "plátano", "banane", "banana", "банан", "バナナ", "바나나"),
    ("🍓", "food", "çilek", "strawberry", "Erdbeere", "fresa", "fraise", "morango", "клубника", "いちご", "딸기"),
    ("🍉", "food", "karpuz", "watermelon", "Wassermelone", "sandía", "pastèque", "melancia", "арбуз", "スイカ", "수박"),
    ("🥕", "food", "havuç", "carrot", "Karotte", "zanahoria", "carotte", "cenoura", "морковь", "ニンジン", "당근"),
    ("🌽", "food", "mısır", "corn", "Mais", "maíz", "maïs", "milho", "кукуруза", "トウモロコシ", "옥수수"),
    ("🍞", "food", "ekmek", "bread", "Brot", "pan", "pain", "pão", "хлеб", "パン", "빵"),
    ("🧀", "food", "peynir", "cheese", "Käse", "queso", "fromage", "queijo", "сыр", "チーズ", "치즈"),
    ("🍕", "food", "pizza", "pizza", "Pizza", "pizza", "pizza", "pizza", "пицца", "ピザ", "피자"),
    ("🍔", "food", "hamburger", "hamburger", "Hamburger", "hamburguesa", "hamburger", "hambúrguer", "гамбургер", "ハンバーガー", "햄버거"),
    ("🍨", "food", "dondurma", "ice cream", "Eis", "helado", "glace", "sorvete", "мороженое", "アイスクリーム", "아이스크림"),
    ("🎂", "food", "pasta", "cake", "Kuchen", "pastel", "gâteau", "bolo", "торт", "ケーキ", "케이크"),
    ("🍯", "food", "bal", "honey", "Honig", "miel", "miel", "mel", "мёд", "はちみつ", "꿀"),
    ("🥚", "food", "yumurta", "egg", "Ei", "huevo", "œuf", "ovo", "яйцо", "卵", "달걀"),
    ("🍄", "food", "mantar", "mushroom", "Pilz", "champiñón", "champignon", "cogumelo", "гриб", "キノコ", "버섯"),
    ("⚽", "fun", "futbol", "football", "Fußball", "fútbol", "football", "futebol", "футбол", "サッカー", "축구"),
    ("🏀", "fun", "basketbol", "basketball", "Basketball", "baloncesto", "basketball", "basquete", "баскетбол", "バスケットボール", "농구"),
    ("🚲", "fun", "bisiklet", "bicycle", "Fahrrad", "bicicleta", "vélo", "bicicleta", "велосипед", "自転車", "자전거"),
    ("✈️", "fun", "uçak", "airplane", "Flugzeug", "avión", "avion", "avião", "самолёт", "飛行機", "비행기"),
    ("🚆", "fun", "tren", "train", "Zug", "tren", "train", "trem", "поезд", "電車", "기차"),
    ("🚀", "fun", "roket", "rocket", "Rakete", "cohete", "fusée", "foguete", "ракета", "ロケット", "로켓"),
    ("🌈", "fun", "gökkuşağı", "rainbow", "Regenbogen", "arcoíris", "arc-en-ciel", "arco-íris", "радуга", "虹", "무지개"),
    ("☀️", "fun", "güneş", "sun", "Sonne", "sol", "soleil", "sol", "солнце", "太陽", "태양"),
    ("🌙", "fun", "ay", "moon", "Mond", "luna", "lune", "lua", "луна", "月", "달"),
    ("⭐", "fun", "yıldız", "star", "Stern", "estrella", "étoile", "estrela", "звезда", "星", "별"),
    ("☂️", "fun", "şemsiye", "umbrella", "Regenschirm", "paraguas", "parapluie", "guarda-chuva", "зонт", "傘", "우산"),
    ("📷", "fun", "kamera", "camera", "Kamera", "cámara", "appareil photo", "câmera", "камера", "カメラ", "카메라"),
    ("🎸", "fun", "gitar", "guitar", "Gitarre", "guitarra", "guitare", "violão", "гитара", "ギター", "기타"),
    ("📖", "fun", "kitap", "book", "Buch", "libro", "livre", "livro", "книга", "本", "책"),
    ("🕰️", "fun", "saat", "clock", "Uhr", "reloj", "horloge", "relógio", "часы", "時計", "시계"),
)

PLANETS = {
    "tr": ("Merkür", "Venüs", "Dünya", "Mars", "Jüpiter", "Satürn", "Uranüs", "Neptün"),
    "en": ("Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"),
    "de": ("Merkur", "Venus", "Erde", "Mars", "Jupiter", "Saturn", "Uranus", "Neptun"),
    "es": ("Mercurio", "Venus", "Tierra", "Marte", "Júpiter", "Saturno", "Urano", "Neptuno"),
    "fr": ("Mercure", "Vénus", "Terre", "Mars", "Jupiter", "Saturne", "Uranus", "Neptune"),
    "pt": ("Mercúrio", "Vénus", "Terra", "Marte", "Júpiter", "Saturno", "Urano", "Neptuno"),
    "ru": ("Меркурий", "Венера", "Земля", "Марс", "Юпитер", "Сатурн", "Уран", "Нептун"),
    "ja": ("水星", "金星", "地球", "火星", "木星", "土星", "天王星", "海王星"),
    "ko": ("수성", "금성", "지구", "화성", "목성", "토성", "천왕성", "해왕성"),
}


def _key(value: str) -> str:
    return " ".join(value.casefold().split())


def _number_word(language: str, number: int) -> str:
    small = {
        "tr": ("", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz",
               "on", "on bir", "on iki", "on üç", "on dört", "on beş", "on altı", "on yedi", "on sekiz", "on dokuz"),
        "en": ("", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
               "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"),
        "de": ("", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun",
               "zehn", "elf", "zwölf", "dreizehn", "vierzehn", "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn"),
        "es": ("", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
               "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve"),
        "fr": ("", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf",
               "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"),
        "pt": ("", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove",
               "dez", "onze", "doze", "treze", "catorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"),
        "ru": ("", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять",
               "десять", "одиннадцать", "двенадцать", "тринадцать", "четырнадцать", "пятнадцать", "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать"),
    }
    if language in ("ja", "ko"):
        digits = ("", "一", "二", "三", "四", "五", "六", "七", "八", "九") if language == "ja" else ("", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구")
        ten = "十" if language == "ja" else "십"
        return (digits[number // 10] if number // 10 > 1 else "") + ten + digits[number % 10] if number >= 10 else digits[number]
    if number < 20:
        return small[language][number]
    tens = {
        "tr": ("", "", "yirmi", "otuz", "kırk"), "en": ("", "", "twenty", "thirty", "forty"),
        "de": ("", "", "zwanzig", "dreißig", "vierzig"), "es": ("", "", "veinte", "treinta", "cuarenta"),
        "fr": ("", "", "vingt", "trente", "quarante"), "pt": ("", "", "vinte", "trinta", "quarenta"),
        "ru": ("", "", "двадцать", "тридцать", "сорок"),
    }[language][number // 10]
    unit = number % 10
    if not unit:
        return tens
    if language == "de":
        return ("ein" if unit == 1 else small[language][unit]) + "und" + tens
    if language in ("es", "fr", "pt"):
        joiner = (" et " if unit == 1 else "-") if language == "fr" else (" e " if language == "pt" else " y ")
        if language == "es" and number < 30:
            special = {21: "veintiuno", 22: "veintidós", 23: "veintitrés", 24: "veinticuatro", 25: "veinticinco",
                       26: "veintiséis", 27: "veintisiete", 28: "veintiocho", 29: "veintinueve"}
            return special[number]
        return tens + joiner + small[language][unit]
    return tens + " " + small[language][unit]


def _geography_rows(language: str, band: str, snapshot: dict[str, list[dict[str, str]]]) -> list[dict[str, Any]]:
    prepared = _prepare(snapshot)
    rng = random.Random(f"alika-word-wheel-variety-v2:{language}:{band}")
    ordered = _age_ordered(prepared[language], FOCUS[language], band, rng)
    eligible = [item for item in ordered
                if item["iso2"] not in CONTESTED_CAPITALS
                and item["iso2"] not in SAME_NAME_CAPITALS
                and item["country"].casefold() != item["capital"].casefold()
                and len(item["continents"]) == 1]
    rows: list[dict[str, Any]] = []
    used: set[str] = set()
    local = set(FOCUS[language])
    for kind in ("country", "capital"):
        added = 0
        for item in eligible:
            answer = item["country"] if kind == "country" else item["capital"]
            forms = country_forms(language, item["iso2"], item["country"])
            continent = CONTINENT_NAMES[language][item["continents"][0]]
            context = {**forms, "capital": item["capital"], "continent": continent}
            clue = (CONTINENT_CLUES[language].format(**context) if kind == "country"
                    else TEMPLATES[language]["capital"].format(**context))
            if _key(answer) in used or _key(answer) in _key(clue):
                continue
            rows.append({
                "answer": answer,
                "category": GEO_CATEGORIES[language][0 if kind == "country" else 1],
                "category_key": kind,
                "clue": clue,
                "explanation": TEMPLATES[language]["capital_explanation"].format(**context),
                "source": {"title": f"Wikidata {item['country_qid']}",
                           "url": f"https://www.wikidata.org/wiki/{item['country_qid']}"},
                "culture_tags": ([f"culture:{language}", item["iso2"]]
                                 if item["iso2"] in local else ["global"]),
            })
            used.add(_key(answer))
            added += 1
            if added == 35:
                break
        if added != 35:
            raise ValueError(f"{language}/{band}: geography quota is {added}, expected 35")
    return rows


def _mixed_rows(language: str, people: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for qid in FAMILIAR_PEOPLE:
        person = people[qid]
        answer = person["labels"][language]
        description = person["descriptions"][language]
        description = re.sub(re.escape(answer), "…", description, flags=re.IGNORECASE)
        rows.append({
            "answer": answer, "category": CATEGORIES[language]["people"], "category_key": "people",
            "clue": TEXT[language]["person"].format(description=description),
            "explanation": f"{answer}: {description}",
            "source": {"title": f"Wikidata {qid}", "url": f"https://www.wikidata.org/wiki/{qid}"},
            "culture_tags": ["global"],
        })
    for number in range(1, 43):
        answer = _number_word(language, number)
        left = max(0, number - (number % 4 + 1))
        right = number - left
        rows.append({
            "answer": answer, "category": CATEGORIES[language]["math"], "category_key": "math",
            "clue": TEXT[language]["math"].format(left=left, right=right),
            "explanation": TEXT[language]["correct"].format(answer=answer),
            "source": {"title": "Khan Academy arithmetic", "url": "https://www.khanacademy.org/math/arithmetic"},
            "culture_tags": [f"culture:{language}"],
        })
    for order, answer in enumerate(PLANETS[language], 1):
        rows.append({
            "answer": answer, "category": CATEGORIES[language]["science"], "category_key": "science",
            "clue": TEXT[language]["planet"].format(order=order),
            "explanation": TEXT[language]["correct"].format(answer=answer),
            "source": {"title": "NASA Solar System Exploration", "url": "https://science.nasa.gov/solar-system/planets/"},
            "culture_tags": ["global"],
        })
    for entry in EMOJI_WORDS:
        emoji, category_key = entry[:2]
        answer = entry[2 + LANGUAGE_INDEX[language]]
        rows.append({
            "answer": answer, "category": CATEGORIES[language][category_key], "category_key": category_key,
            "clue": TEXT[language]["emoji"].format(emoji=emoji),
            "explanation": TEXT[language]["emoji_explanation"].format(emoji=emoji, answer=answer),
            "source": {"title": "Unicode Emoji Charts", "url": "https://unicode.org/emoji/charts/full-emoji-list.html"},
            "culture_tags": [f"culture:{language}"],
        })
    return rows


def _interleave(rows: list[dict[str, Any]], language: str, band: str) -> list[dict[str, Any]]:
    rng = random.Random(f"alika-word-wheel-interleave-v2:{language}:{band}")
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row["category_key"], []).append(row)
    for values in grouped.values():
        rng.shuffle(values)
    result: list[dict[str, Any]] = []
    while grouped:
        for key in list(grouped):
            values = grouped[key]
            result.append(values.pop())
            if not values:
                del grouped[key]
    return result


def generate() -> None:
    snapshot = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    people_data = json.loads(PEOPLE_PATH.read_text(encoding="utf-8"))["people"]
    people = {row["qid"]: row for row in people_data if row["qid"] in FAMILIAR_PEOPLE}
    if set(people) != set(FAMILIAR_PEOPLE):
        raise ValueError("familiar people source is incomplete")
    if len(EMOJI_WORDS) != 50:
        raise ValueError("expected 50 emoji words")

    for language in LANGUAGES:
        for band in BANDS:
            rows = _geography_rows(language, band, snapshot) + _mixed_rows(language, people)
            rows = _interleave(rows, language, band)
            if len(rows) != PUZZLES_PER_POOL:
                raise ValueError(f"{language}/{band}: expected {PUZZLES_PER_POOL}, got {len(rows)}")
            answers = [_key(row["answer"]) for row in rows]
            if len(answers) != len(set(answers)):
                raise ValueError(f"{language}/{band}: duplicate answer")
            output = []
            for number, source in enumerate(rows, 1):
                row = {key: value for key, value in source.items() if key != "category_key"}
                row.update({"puzzle_id": f"wheel-{language}-{band}-{number:03d}", "review_status": "ai-draft"})
                if _key(row["answer"]) in _key(row["clue"]):
                    raise ValueError(f"{language}/{band}:{number}: answer appears in clue")
                output.append(row)
            path = ROOT / "games" / "word-wheel" / "words" / language / f"{band}.jsonl"
            path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in output), encoding="utf-8")


def main() -> int:
    generate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
