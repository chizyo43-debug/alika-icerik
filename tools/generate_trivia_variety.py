"""Build mixed, localized general-knowledge pools from frozen AliKa sources.

Each 200-question pool contains geography, people/culture, mathematics/logic,
and science/technology.  The source files are committed, so generation is
deterministic and offline.
"""
from __future__ import annotations

import json
import random
import re
import tempfile
from pathlib import Path
from typing import Any

import generate_trivia_geography as geography
from build_trivia_games import BANDS, LANGUAGES, QUESTIONS, SUBJECTS


ROOT = Path(__file__).resolve().parents[1]
PEOPLE = ROOT / "games" / "who-is-it" / "identities"

TOPICS = {
    "tr": ("Coğrafya", "İnsanlar ve kültür", "Matematik ve mantık", "Bilim ve teknoloji"),
    "en": ("Geography", "People and culture", "Math and logic", "Science and technology"),
    "de": ("Geografie", "Menschen und Kultur", "Mathematik und Logik", "Wissenschaft und Technik"),
    "es": ("Geografía", "Personas y cultura", "Matemáticas y lógica", "Ciencia y tecnología"),
    "fr": ("Géographie", "Personnes et culture", "Mathématiques et logique", "Sciences et technologie"),
    "pt": ("Geografia", "Pessoas e cultura", "Matemática e lógica", "Ciência e tecnologia"),
    "ru": ("География", "Люди и культура", "Математика и логика", "Наука и техника"),
    "ja": ("地理", "人物と文化", "数学と論理", "科学と技術"),
    "ko": ("지리", "인물과 문화", "수학과 논리", "과학과 기술"),
}

TEXT = {
    "tr": {
        "identity": "Bu ipuçları kimi anlatıyor? {clues}",
        "occupation": "{person} en çok hangi alanla ilişkilidir?",
        "born": "{person} hangi yılda doğmuştur?",
        "add": "{a} ile {b} toplanırsa sonuç kaç olur?",
        "sub": "{a} sayısından {b} çıkarılırsa kaç kalır?",
        "mul": "{a} × {b} işleminin sonucu kaçtır?",
        "div": "{a} ÷ {b} işleminin sonucu kaçtır?",
        "sequence": "Sayı dizisinde sıradaki sayı hangisidir: {a}, {b}, {c}, ?",
        "atomic": "Simgesi {symbol} olan elementin atom numarası kaçtır?",
        "planet": "Güneş'e {order}. sırada bulunan gezegen hangisidir?",
        "unit": "{quantity} için kullanılan SI birim simgesi hangisidir?",
        "correct": "Doğru cevap: {answer}.",
    },
    "en": {
        "identity": "Who do these clues describe? {clues}", "occupation": "Which field is {person} best associated with?",
        "born": "In which year was {person} born?", "add": "What is {a} plus {b}?", "sub": "What is {a} minus {b}?",
        "mul": "What is {a} × {b}?", "div": "What is {a} ÷ {b}?", "sequence": "What comes next: {a}, {b}, {c}, ?",
        "atomic": "What is the atomic number of the element with symbol {symbol}?", "planet": "Which planet is number {order} from the Sun?",
        "unit": "Which SI unit symbol is used for {quantity}?", "correct": "Correct answer: {answer}.",
    },
    "de": {
        "identity": "Welche Person beschreiben diese Hinweise? {clues}", "occupation": "Mit welchem Gebiet wird {person} am stärksten verbunden?",
        "born": "In welchem Jahr wurde {person} geboren?", "add": "Wie viel ist {a} plus {b}?", "sub": "Wie viel ist {a} minus {b}?",
        "mul": "Wie viel ist {a} × {b}?", "div": "Wie viel ist {a} ÷ {b}?", "sequence": "Welche Zahl folgt: {a}, {b}, {c}, ?",
        "atomic": "Welche Ordnungszahl hat das Element mit dem Symbol {symbol}?", "planet": "Welcher Planet steht an {order}. Stelle von der Sonne?",
        "unit": "Welches SI-Einheitenzeichen wird für {quantity} verwendet?", "correct": "Richtige Antwort: {answer}.",
    },
    "es": {
        "identity": "¿A quién describen estas pistas? {clues}", "occupation": "¿Con qué campo se asocia principalmente a {person}?",
        "born": "¿En qué año nació {person}?", "add": "¿Cuánto es {a} más {b}?", "sub": "¿Cuánto es {a} menos {b}?",
        "mul": "¿Cuánto es {a} × {b}?", "div": "¿Cuánto es {a} ÷ {b}?", "sequence": "¿Qué número sigue: {a}, {b}, {c}, ?",
        "atomic": "¿Cuál es el número atómico del elemento cuyo símbolo es {symbol}?", "planet": "¿Qué planeta ocupa el lugar {order} desde el Sol?",
        "unit": "¿Qué símbolo de unidad SI se usa para {quantity}?", "correct": "Respuesta correcta: {answer}.",
    },
    "fr": {
        "identity": "Qui ces indices décrivent-ils ? {clues}", "occupation": "À quel domaine associe-t-on surtout {person} ?",
        "born": "En quelle année {person} est-il ou est-elle né(e) ?", "add": "Combien font {a} plus {b} ?", "sub": "Combien font {a} moins {b} ?",
        "mul": "Combien font {a} × {b} ?", "div": "Combien font {a} ÷ {b} ?", "sequence": "Quel nombre vient ensuite : {a}, {b}, {c}, ?",
        "atomic": "Quel est le numéro atomique de l’élément de symbole {symbol} ?", "planet": "Quelle planète est en position {order} à partir du Soleil ?",
        "unit": "Quel symbole d’unité SI utilise-t-on pour {quantity} ?", "correct": "Bonne réponse : {answer}.",
    },
    "pt": {
        "identity": "Quem estas pistas descrevem? {clues}", "occupation": "A que área {person} está mais associado(a)?",
        "born": "Em que ano nasceu {person}?", "add": "Quanto é {a} mais {b}?", "sub": "Quanto é {a} menos {b}?",
        "mul": "Quanto é {a} × {b}?", "div": "Quanto é {a} ÷ {b}?", "sequence": "Qual é o próximo número: {a}, {b}, {c}, ?",
        "atomic": "Qual é o número atómico do elemento de símbolo {symbol}?", "planet": "Qual planeta ocupa a posição {order} a partir do Sol?",
        "unit": "Qual símbolo de unidade SI é usado para {quantity}?", "correct": "Resposta correta: {answer}.",
    },
    "ru": {
        "identity": "Кого описывают эти подсказки? {clues}", "occupation": "С какой областью прежде всего связан или связана {person}?",
        "born": "В каком году родился или родилась {person}?", "add": "Сколько будет {a} плюс {b}?", "sub": "Сколько будет {a} минус {b}?",
        "mul": "Сколько будет {a} × {b}?", "div": "Сколько будет {a} ÷ {b}?", "sequence": "Какое число следующее: {a}, {b}, {c}, ?",
        "atomic": "Каков атомный номер элемента с символом {symbol}?", "planet": "Какая планета находится под номером {order} от Солнца?",
        "unit": "Какое обозначение единицы СИ используют для величины «{quantity}»?", "correct": "Правильный ответ: {answer}.",
    },
    "ja": {
        "identity": "この手がかりが表す人物は誰ですか？ {clues}", "occupation": "{person}と最も関係が深い分野はどれですか？",
        "born": "{person}が生まれた年はいつですか？", "add": "{a}と{b}を足すといくつですか？", "sub": "{a}から{b}を引くといくつですか？",
        "mul": "{a}×{b}はいくつですか？", "div": "{a}÷{b}はいくつですか？", "sequence": "次に入る数はどれですか：{a}、{b}、{c}、？",
        "atomic": "元素記号{symbol}の原子番号はいくつですか？", "planet": "太陽から{order}番目の惑星はどれですか？",
        "unit": "{quantity}に使うSI単位記号はどれですか？", "correct": "正解は{answer}です。",
    },
    "ko": {
        "identity": "이 단서들이 설명하는 인물은 누구인가요? {clues}", "occupation": "{person}와 가장 관련 깊은 분야는 무엇인가요?",
        "born": "{person}은(는) 몇 년에 태어났나요?", "add": "{a}와 {b}를 더하면 얼마인가요?", "sub": "{a}에서 {b}를 빼면 얼마인가요?",
        "mul": "{a} × {b}는 얼마인가요?", "div": "{a} ÷ {b}는 얼마인가요?", "sequence": "다음에 올 수는 무엇인가요: {a}, {b}, {c}, ?",
        "atomic": "원소 기호가 {symbol}인 원소의 원자 번호는 무엇인가요?", "planet": "태양에서 {order}번째 행성은 무엇인가요?",
        "unit": "{quantity}에 사용하는 SI 단위 기호는 무엇인가요?", "correct": "정답은 {answer}입니다.",
    },
}

PLANETS = {
    "tr": "Merkür Venüs Dünya Mars Jüpiter Satürn Uranüs Neptün".split(),
    "en": "Mercury Venus Earth Mars Jupiter Saturn Uranus Neptune".split(),
    "de": "Merkur Venus Erde Mars Jupiter Saturn Uranus Neptun".split(),
    "es": "Mercurio Venus Tierra Marte Júpiter Saturno Urano Neptuno".split(),
    "fr": "Mercure Vénus Terre Mars Jupiter Saturne Uranus Neptune".split(),
    "pt": "Mercúrio Vénus Terra Marte Júpiter Saturno Urano Neptuno".split(),
    "ru": "Меркурий Венера Земля Марс Юпитер Сатурн Уран Нептун".split(),
    "ja": "水星 金星 地球 火星 木星 土星 天王星 海王星".split(),
    "ko": "수성 금성 지구 화성 목성 토성 천왕성 해왕성".split(),
}

QUANTITIES = {
    "tr": ["uzunluk", "kütle", "zaman", "elektrik akımı", "termodinamik sıcaklık", "madde miktarı", "ışık şiddeti", "frekans", "kuvvet", "basınç", "enerji", "güç"],
    "en": ["length", "mass", "time", "electric current", "thermodynamic temperature", "amount of substance", "luminous intensity", "frequency", "force", "pressure", "energy", "power"],
    "de": ["Länge", "Masse", "Zeit", "elektrische Stromstärke", "thermodynamische Temperatur", "Stoffmenge", "Lichtstärke", "Frequenz", "Kraft", "Druck", "Energie", "Leistung"],
    "es": ["longitud", "masa", "tiempo", "corriente eléctrica", "temperatura termodinámica", "cantidad de sustancia", "intensidad luminosa", "frecuencia", "fuerza", "presión", "energía", "potencia"],
    "fr": ["longueur", "masse", "temps", "courant électrique", "température thermodynamique", "quantité de matière", "intensité lumineuse", "fréquence", "force", "pression", "énergie", "puissance"],
    "pt": ["comprimento", "massa", "tempo", "corrente elétrica", "temperatura termodinâmica", "quantidade de matéria", "intensidade luminosa", "frequência", "força", "pressão", "energia", "potência"],
    "ru": ["длина", "масса", "время", "электрический ток", "термодинамическая температура", "количество вещества", "сила света", "частота", "сила", "давление", "энергия", "мощность"],
    "ja": ["長さ", "質量", "時間", "電流", "熱力学温度", "物質量", "光度", "周波数", "力", "圧力", "エネルギー", "仕事率"],
    "ko": ["길이", "질량", "시간", "전류", "열역학적 온도", "물질량", "광도", "주파수", "힘", "압력", "에너지", "일률"],
}
UNIT_SYMBOLS = ["m", "kg", "s", "A", "K", "mol", "cd", "Hz", "N", "Pa", "J", "W"]
ATOMS = [("H", 1), ("He", 2), ("Li", 3), ("B", 5), ("C", 6), ("N", 7), ("O", 8), ("F", 9), ("Ne", 10), ("Na", 11), ("Mg", 12), ("Al", 13), ("Si", 14), ("P", 15), ("S", 16), ("Cl", 17), ("Ar", 18), ("K", 19), ("Fe", 26), ("Au", 79)]

SPECIAL = {
    "tr": [("Suyun kimyasal formülü hangisidir?", "H₂O", ["CO₂", "O₂", "NaCl"]), ("Karbondioksitin kimyasal formülü hangisidir?", "CO₂", ["H₂O", "O₂", "N₂"]), ("İnsan kalbi kaç odacıktan oluşur?", "4", ["2", "3", "6"]), ("Bir böceğin kaç bacağı vardır?", "6", ["4", "8", "10"]), ("Bir örümceğin kaç bacağı vardır?", "8", ["4", "6", "10"]), ("Bir gün kaç saattir?", "24", ["12", "18", "36"]), ("Bir saat kaç dakikadır?", "60", ["30", "90", "100"]), ("Saf su deniz seviyesinde kaç °C'de donar?", "0", ["-10", "10", "100"]), ("Saf su deniz seviyesinde kaç °C'de kaynar?", "100", ["0", "50", "212"]), ("Kalıtsal bilgiyi taşıyan molekül hangisidir?", "DNA", ["ATP", "H₂O", "NaCl"])],
    "en": [("What is the chemical formula of water?", "H₂O", ["CO₂", "O₂", "NaCl"]), ("What is the chemical formula of carbon dioxide?", "CO₂", ["H₂O", "O₂", "N₂"]), ("How many chambers does the human heart have?", "4", ["2", "3", "6"]), ("How many legs does an insect have?", "6", ["4", "8", "10"]), ("How many legs does a spider have?", "8", ["4", "6", "10"]), ("How many hours are in a day?", "24", ["12", "18", "36"]), ("How many minutes are in an hour?", "60", ["30", "90", "100"]), ("At sea level, at what °C does pure water freeze?", "0", ["-10", "10", "100"]), ("At sea level, at what °C does pure water boil?", "100", ["0", "50", "212"]), ("Which molecule carries hereditary information?", "DNA", ["ATP", "H₂O", "NaCl"])],
    "de": [("Wie lautet die chemische Formel von Wasser?", "H₂O", ["CO₂", "O₂", "NaCl"]), ("Wie lautet die chemische Formel von Kohlendioxid?", "CO₂", ["H₂O", "O₂", "N₂"]), ("Wie viele Kammern hat das menschliche Herz?", "4", ["2", "3", "6"]), ("Wie viele Beine hat ein Insekt?", "6", ["4", "8", "10"]), ("Wie viele Beine hat eine Spinne?", "8", ["4", "6", "10"]), ("Wie viele Stunden hat ein Tag?", "24", ["12", "18", "36"]), ("Wie viele Minuten hat eine Stunde?", "60", ["30", "90", "100"]), ("Bei wie viel °C gefriert reines Wasser auf Meereshöhe?", "0", ["-10", "10", "100"]), ("Bei wie viel °C siedet reines Wasser auf Meereshöhe?", "100", ["0", "50", "212"]), ("Welches Molekül trägt die Erbinformation?", "DNA", ["ATP", "H₂O", "NaCl"])],
    "es": [("¿Cuál es la fórmula química del agua?", "H₂O", ["CO₂", "O₂", "NaCl"]), ("¿Cuál es la fórmula química del dióxido de carbono?", "CO₂", ["H₂O", "O₂", "N₂"]), ("¿Cuántas cavidades tiene el corazón humano?", "4", ["2", "3", "6"]), ("¿Cuántas patas tiene un insecto?", "6", ["4", "8", "10"]), ("¿Cuántas patas tiene una araña?", "8", ["4", "6", "10"]), ("¿Cuántas horas tiene un día?", "24", ["12", "18", "36"]), ("¿Cuántos minutos tiene una hora?", "60", ["30", "90", "100"]), ("Al nivel del mar, ¿a cuántos °C se congela el agua pura?", "0", ["-10", "10", "100"]), ("Al nivel del mar, ¿a cuántos °C hierve el agua pura?", "100", ["0", "50", "212"]), ("¿Qué molécula lleva la información hereditaria?", "ADN", ["ATP", "H₂O", "NaCl"])],
    "fr": [("Quelle est la formule chimique de l’eau ?", "H₂O", ["CO₂", "O₂", "NaCl"]), ("Quelle est la formule chimique du dioxyde de carbone ?", "CO₂", ["H₂O", "O₂", "N₂"]), ("Combien de cavités le cœur humain possède-t-il ?", "4", ["2", "3", "6"]), ("Combien de pattes un insecte a-t-il ?", "6", ["4", "8", "10"]), ("Combien de pattes une araignée a-t-elle ?", "8", ["4", "6", "10"]), ("Combien d’heures compte une journée ?", "24", ["12", "18", "36"]), ("Combien de minutes compte une heure ?", "60", ["30", "90", "100"]), ("Au niveau de la mer, à combien de °C l’eau pure gèle-t-elle ?", "0", ["-10", "10", "100"]), ("Au niveau de la mer, à combien de °C l’eau pure bout-elle ?", "100", ["0", "50", "212"]), ("Quelle molécule porte l’information héréditaire ?", "ADN", ["ATP", "H₂O", "NaCl"])],
    "pt": [("Qual é a fórmula química da água?", "H₂O", ["CO₂", "O₂", "NaCl"]), ("Qual é a fórmula química do dióxido de carbono?", "CO₂", ["H₂O", "O₂", "N₂"]), ("Quantas cavidades tem o coração humano?", "4", ["2", "3", "6"]), ("Quantas patas tem um inseto?", "6", ["4", "8", "10"]), ("Quantas patas tem uma aranha?", "8", ["4", "6", "10"]), ("Quantas horas tem um dia?", "24", ["12", "18", "36"]), ("Quantos minutos tem uma hora?", "60", ["30", "90", "100"]), ("Ao nível do mar, a quantos °C congela a água pura?", "0", ["-10", "10", "100"]), ("Ao nível do mar, a quantos °C ferve a água pura?", "100", ["0", "50", "212"]), ("Que molécula transporta a informação hereditária?", "ADN", ["ATP", "H₂O", "NaCl"])],
    "ru": [("Какова химическая формула воды?", "H₂O", ["CO₂", "O₂", "NaCl"]), ("Какова химическая формула углекислого газа?", "CO₂", ["H₂O", "O₂", "N₂"]), ("Сколько камер в сердце человека?", "4", ["2", "3", "6"]), ("Сколько ног у насекомого?", "6", ["4", "8", "10"]), ("Сколько ног у паука?", "8", ["4", "6", "10"]), ("Сколько часов в сутках?", "24", ["12", "18", "36"]), ("Сколько минут в часе?", "60", ["30", "90", "100"]), ("При скольких °C чистая вода замерзает на уровне моря?", "0", ["-10", "10", "100"]), ("При скольких °C чистая вода кипит на уровне моря?", "100", ["0", "50", "212"]), ("Какая молекула хранит наследственную информацию?", "ДНК", ["АТФ", "H₂O", "NaCl"])],
    "ja": [("水の化学式はどれですか？", "H₂O", ["CO₂", "O₂", "NaCl"]), ("二酸化炭素の化学式はどれですか？", "CO₂", ["H₂O", "O₂", "N₂"]), ("人の心臓にはいくつの部屋がありますか？", "4", ["2", "3", "6"]), ("昆虫の脚は何本ですか？", "6", ["4", "8", "10"]), ("クモの脚は何本ですか？", "8", ["4", "6", "10"]), ("1日は何時間ですか？", "24", ["12", "18", "36"]), ("1時間は何分ですか？", "60", ["30", "90", "100"]), ("海面気圧で純水が凍る温度は何°Cですか？", "0", ["-10", "10", "100"]), ("海面気圧で純水が沸騰する温度は何°Cですか？", "100", ["0", "50", "212"]), ("遺伝情報を担う分子はどれですか？", "DNA", ["ATP", "H₂O", "NaCl"])],
    "ko": [("물의 화학식은 무엇인가요?", "H₂O", ["CO₂", "O₂", "NaCl"]), ("이산화 탄소의 화학식은 무엇인가요?", "CO₂", ["H₂O", "O₂", "N₂"]), ("사람의 심장은 몇 개의 방으로 이루어져 있나요?", "4", ["2", "3", "6"]), ("곤충의 다리는 몇 개인가요?", "6", ["4", "8", "10"]), ("거미의 다리는 몇 개인가요?", "8", ["4", "6", "10"]), ("하루는 몇 시간인가요?", "24", ["12", "18", "36"]), ("한 시간은 몇 분인가요?", "60", ["30", "90", "100"]), ("해수면에서 순수한 물은 몇 °C에서 어나요?", "0", ["-10", "10", "100"]), ("해수면에서 순수한 물은 몇 °C에서 끓나요?", "100", ["0", "50", "212"]), ("유전 정보를 담는 분자는 무엇인가요?", "DNA", ["ATP", "H₂O", "NaCl"])],
}

SOURCES = {
    "math": {"title": "Khan Academy mathematics", "url": "https://www.khanacademy.org/math"},
    "atom": {"title": "IUPAC periodic table", "url": "https://iupac.org/what-we-do/periodic-table-of-elements/"},
    "planet": {"title": "NASA Solar System Exploration", "url": "https://science.nasa.gov/solar-system/planets/"},
    "unit": {"title": "BIPM SI Brochure", "url": "https://www.bipm.org/en/publications/si-brochure"},
    "science": {"title": "Smithsonian Science Education Center", "url": "https://ssec.si.edu/"},
}


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _draft(question: str, answer: str, candidates: list[str], topic: str,
           source: dict[str, str], tags: list[str]) -> dict[str, Any]:
    wrong = []
    for value in candidates:
        value = str(value)
        if value != answer and value not in wrong:
            wrong.append(value)
    if len(wrong) < 3:
        raise ValueError(f"not enough unique distractors for {question!r}")
    return {"question": question, "answer": answer, "wrong": wrong[:3], "topic": topic,
            "source": source, "culture_tags": tags}


def _geo_drafts(language: str, band: str, generated: Path) -> list[dict[str, Any]]:
    rows = _rows(generated / language / f"{band}.jsonl")
    local = [row for row in rows if f"culture:{language}" in row["culture_tags"]]
    # Geography is capped at 20% of the final pool.  Using the first forty
    # local rows also guarantees a meaningful culture-specific foundation.
    selected = local[:40]
    if len(selected) != 40:
        raise ValueError(f"expected 40 local geography rows for {language}/{band}")
    topic = TOPICS[language][0]
    return [_draft(row["question"], row["choices"][row["correct"]], row["choices"], topic,
                   row["source"], row["culture_tags"]) for row in selected]


def _people_drafts(language: str, band: str, rng: random.Random) -> list[dict[str, Any]]:
    rows = _rows(PEOPLE / language / f"{band}.jsonl")
    rng.shuffle(rows)
    text = TEXT[language]
    topic = TOPICS[language][1]
    labels = [row["answer"] for row in rows]
    categories = list(dict.fromkeys(row["category"] for row in rows))
    years = []
    for row in rows:
        match = re.search(r"-?\d{1,4}", row["clues"][1])
        if match and not match.group().startswith("-") and match.group() not in years:
            years.append(match.group())
    result = []
    seen_identity_questions = set()
    for row in rows:
        birth_match = re.search(r"-?\d{1,4}", row["clues"][1])
        if birth_match and birth_match.group().startswith("-"):
            continue
        clue = " ".join((row["clues"][1], row["clues"][2], row["clues"][3]))
        question = text["identity"].format(clues=clue)
        key = " ".join(question.casefold().split())
        if key in seen_identity_questions:
            continue
        seen_identity_questions.add(key)
        result.append(_draft(question, row["answer"], labels, topic, row["source"], row["culture_tags"]))
        if len(result) == 30:
            break
    occupation_rows = []
    seen_categories = set()
    for row in rows[30:]:
        if row["category"] not in seen_categories:
            occupation_rows.append(row)
            seen_categories.add(row["category"])
        if len(occupation_rows) == 15:
            break
    for row in occupation_rows:
        result.append(_draft(text["occupation"].format(person=row["answer"]), row["category"], categories,
                             topic, row["source"], row["culture_tags"]))
    born_count = 0
    for row in rows[45:]:
        match = re.search(r"-?\d{1,4}", row["clues"][1])
        if not match or match.group().startswith("-"):
            continue
        result.append(_draft(text["born"].format(person=row["answer"]), match.group(), years, topic,
                             row["source"], row["culture_tags"]))
        born_count += 1
        if born_count == 15:
            break
    if len(result) != 60:
        raise ValueError(f"expected 60 people rows for {language}/{band}")
    return result


def _number_wrongs(answer: int) -> list[str]:
    values = [answer - 2, answer - 1, answer + 1, answer + 2, answer + 5]
    return [str(value) for value in values if value >= 0 and value != answer][:3]


def _math_drafts(language: str, band: str, rng: random.Random) -> list[dict[str, Any]]:
    text = TEXT[language]
    topic = TOPICS[language][2]
    level = list(BANDS).index(band) + 1
    result = []
    for index in range(10):
        a, b = 4 + level * 5 + index * 2, 2 + index
        answer = a + b
        result.append(_draft(text["add"].format(a=a, b=b), str(answer), _number_wrongs(answer), topic, SOURCES["math"], ["global"]))
    for index in range(10):
        b = 2 + index
        a = b + 7 + level * 4 + index
        answer = a - b
        result.append(_draft(text["sub"].format(a=a, b=b), str(answer), _number_wrongs(answer), topic, SOURCES["math"], ["global"]))
    for index in range(10):
        a, b = 2 + level + index % 5, 2 + index
        answer = a * b
        result.append(_draft(text["mul"].format(a=a, b=b), str(answer), _number_wrongs(answer), topic, SOURCES["math"], ["global"]))
    for index in range(10):
        b = 2 + index % 7
        answer = 3 + level + index
        a = b * answer
        result.append(_draft(text["div"].format(a=a, b=b), str(answer), _number_wrongs(answer), topic, SOURCES["math"], ["global"]))
    for index in range(10):
        start, step = 1 + index + level, 2 + index % (level + 2)
        answer = start + step * 3
        result.append(_draft(text["sequence"].format(a=start, b=start + step, c=start + step * 2),
                             str(answer), _number_wrongs(answer), topic, SOURCES["math"], ["global"]))
    rng.shuffle(result)
    return result


def _science_drafts(language: str) -> list[dict[str, Any]]:
    text = TEXT[language]
    topic = TOPICS[language][3]
    result = []
    atomic_numbers = [str(number) for _, number in ATOMS]
    for symbol, number in ATOMS:
        result.append(_draft(text["atomic"].format(symbol=symbol), str(number), atomic_numbers, topic, SOURCES["atom"], ["global"]))
    planets = PLANETS[language]
    for index, planet in enumerate(planets, 1):
        result.append(_draft(text["planet"].format(order=index), planet, planets, topic, SOURCES["planet"], ["global"]))
    for quantity, symbol in zip(QUANTITIES[language], UNIT_SYMBOLS):
        result.append(_draft(text["unit"].format(quantity=quantity), symbol, UNIT_SYMBOLS, topic, SOURCES["unit"], ["global"]))
    for question, answer, wrong in SPECIAL[language]:
        result.append(_draft(question, answer, wrong, topic, SOURCES["science"], ["global"]))
    if len(result) != 50:
        raise AssertionError(len(result))
    return result


def _interleave(groups: list[list[dict[str, Any]]], rng: random.Random) -> list[dict[str, Any]]:
    """Mix topic families without allowing a same-topic question streak."""
    for group in groups:
        rng.shuffle(group)
    mixed = []
    last_topic = None
    while any(groups):
        candidates = [group for group in groups if group and group[-1]["topic"] != last_topic]
        if not candidates:
            candidates = [group for group in groups if group]
        largest = max(len(group) for group in candidates)
        near_largest = [group for group in candidates if len(group) >= largest - 3]
        chosen = rng.choice(near_largest)
        item = chosen.pop()
        mixed.append(item)
        last_topic = item["topic"]
    return mixed


def generate() -> None:
    snapshot = json.loads(geography.DATA_PATH.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="alika-trivia-geography-") as raw:
        generated = Path(raw)
        original = geography.QUESTIONS
        try:
            geography.QUESTIONS = generated
            geography.generate(snapshot)
        finally:
            geography.QUESTIONS = original
        for language in LANGUAGES:
            for band in BANDS:
                rng = random.Random(f"alika-trivia-variety-v2:{language}:{band}")
                drafts = _interleave([
                    _geo_drafts(language, band, generated),
                    _people_drafts(language, band, rng),
                    _math_drafts(language, band, rng),
                    _science_drafts(language),
                ], rng)
                if len(drafts) != 200:
                    raise AssertionError(len(drafts))
                rows = []
                for number, draft in enumerate(drafts, 1):
                    correct = (number - 1) % 4
                    choices = draft["wrong"][:]
                    choices.insert(correct, draft["answer"])
                    rows.append({
                        "question_id": f"gk-{language}-{band}-{number:03d}",
                        "question": draft["question"], "choices": choices, "correct": correct,
                        "subject": SUBJECTS[language], "topic": draft["topic"],
                        "explanation": TEXT[language]["correct"].format(answer=draft["answer"]),
                        "source": draft["source"], "culture_tags": draft["culture_tags"],
                        "review_status": "ai-draft",
                    })
                path = QUESTIONS / language / f"{band}.jsonl"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


if __name__ == "__main__":
    generate()
