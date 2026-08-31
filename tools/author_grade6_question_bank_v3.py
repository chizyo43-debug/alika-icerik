#!/usr/bin/env python3
"""REJECTED grade-6 experiment retained only as an audit regression fixture.

Each bank item combines two independently authored lesson exercises from the
same note into one new verification task.  The learner must solve both cases
and audit the proposed answers.  The source answer position is never copied;
bank answer positions are scheduled independently.  A source visual is used
only when it is the primary evidence for the new task.

Independent review proved that this approach embeds lesson-question roots and
collapses all items into one cognitive archetype.  It must never generate a
candidate again; ``main`` fails closed before reading or writing content.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from author_grade6_question_bank import (
    AUTHORING_ROOT,
    GRADE_ROOT,
    LABEL_PATH,
    QUESTION_PATH,
    SUBJECT_QUOTAS,
    allocate,
    batch_schedule,
    clean,
)


PAIR_WORDINGS = (
    ("Yalnız I. yanıt doğrudur.", "Yalnız II. yanıt doğrudur.",
     "I ve II. yanıtların ikisi de doğrudur.", "I ve II. yanıtların ikisi de yanlıştır."),
    ("Sadece birinci öğrencinin sonucu geçerlidir.",
     "Sadece ikinci öğrencinin sonucu geçerlidir.",
     "Her iki öğrencinin sonucu da geçerlidir.",
     "İki öğrencinin sonucu da geçerli değildir."),
    ("I. kart onaylanır, II. kart düzeltilir.",
     "II. kart onaylanır, I. kart düzeltilir.",
     "Her iki kart da değiştirilmeden onaylanır.",
     "Her iki kartta da yanıt düzeltilmelidir."),
    ("Birinci çözüm doğru, ikinci çözüm yanlıştır.",
     "İkinci çözüm doğru, birinci çözüm yanlıştır.",
     "Her iki çözüm de doğrudur.", "Her iki çözüm de yanlıştır."),
)

REASON_PREFIXES = (
    ("Birinci kartı koşulsuz onaylama yanılgısı", "I. durumun doğruluğunu varsayma hatası",
     "İlk çözümü kanıtsız kabul etme yanılgısı", "Birinci yanıta öncelik verme hatası"),
    ("İkinci kartı koşulsuz onaylama yanılgısı", "II. durumun doğruluğunu varsayma hatası",
     "İkinci çözümü kanıtsız kabul etme yanılgısı", "Son yanıta öncelik verme hatası"),
    ("İki yanıtı da doğru sayma yanılgısı", "Çifte onay genellemesi",
     "Kartlar arası farkı gözden kaçırma hatası", "Her iki sonucu kanıtsız kabul etme yanılgısı"),
    ("İki yanıtı da yanlış sayma yanılgısı", "Çifte ret genellemesi",
     "Geçerli kartı da eleme hatası", "Her iki sonucu kanıtsız reddetme yanılgısı"),
)

OPENERS = (
    "Bir çalışma grubunun iki ayrı problem için hazırladığı yanıtlar denetleniyor.",
    "Konu anlatımından sonra iki öğrenci farklı alıştırmaları çözüyor.",
    "Bir öğretmen, iki çözüm kartındaki problem–yanıt uyumunu inceliyor.",
    "Aynı kazanıma ait iki durum için verilen sonuçlar karşılaştırılıyor.",
    "Bir akran değerlendirmesinde iki ayrı çözümün doğruluğu gerekçeleriyle sınanıyor.",
    "Ders sonunda hazırlanan iki kontrol kartı konu bilgisinin doğruluğuna göre inceleniyor.",
)

SPECIAL_SCIENCE_NOTES = {
    "tr-g06-fen-bilimleri-note-021",
    "tr-g06-fen-bilimleri-note-027",
    "tr-g06-fen-bilimleri-note-029",
    "tr-g06-fen-bilimleri-note-030",
    "tr-g06-fen-bilimleri-note-031",
    "tr-g06-fen-bilimleri-note-034",
}

# Curated pair reselections for source exercises whose wording is intentionally
# very similar within one objective.  Offsets choose a different substantive
# pair; they do not alter names or numbers in an existing pair.
PAIR_SHIFTS = {
    "tr-g06-bank-q0629": 17, "tr-g06-bank-q0641": 541,
    "tr-g06-bank-q0644": 601, "tr-g06-bank-q0673": 19,
    "tr-g06-bank-q0674": 239, "tr-g06-bank-q0676": 659,
    "tr-g06-bank-q0710": 911,
    "tr-g06-bank-q0730": 23, "tr-g06-bank-q0736": 251,
    "tr-g06-bank-q0755": 31, "tr-g06-bank-q0756": 37,
    "tr-g06-bank-q0757": 41, "tr-g06-bank-q0758": 43,
    "tr-g06-bank-q0760": 137, "tr-g06-bank-q0775": 919,
    "tr-g06-bank-q0796": 929,
    "tr-g06-bank-q0799": 263, "tr-g06-bank-q0800": 757,
    "tr-g06-bank-q0819": 197,
    "tr-g06-bank-q0834": 271, "tr-g06-bank-q0836": 59, "tr-g06-bank-q0840": 211,
    "tr-g06-bank-q0876": 937, "tr-g06-bank-q0878": 277, "tr-g06-bank-q0880": 809,
    "tr-g06-bank-q1180": 857, "tr-g06-bank-q1371": 293,
    "tr-g06-bank-q1249": 941, "tr-g06-bank-q1407": 947,
    "tr-g06-bank-q1577": 307,
}


def synthetic_science_question(note_id: str, seed: int) -> dict[str, Any]:
    """Create self-contained, solver-checkable evidence for four visual-heavy notes."""
    if note_id in {"tr-g06-fen-bilimleri-note-027", "tr-g06-fen-bilimleri-note-029"}:
        materials = ["cam", "mermer", "porselen", "alüminyum", "tuğla", "granit", "bakır", "çelik"]
        material = materials[seed % len(materials)]
        volume = 10 + seed % 8
        density = 2 + seed % 5
        mass = volume * density
        variant = seed % 5
        correct = 0
        if variant == 0:
            choices = [f"{density} g/cm³", f"{density + 1} g/cm³",
                       f"{mass} g/cm³", f"{volume} g/cm³"]
            stem_text = (f"Bir {material} örneğinin kütlesi {mass} g, hacmi {volume} cm³ ölçülüyor. "
                         "Kütle/hacim oranına göre maddenin yoğunluğu kaçtır?")
            explanation = (f"Bu {material} örneğinin yoğunluğu kütlenin hacme bölünmesiyle bulunur: "
                           f"{mass} ÷ {volume} = {density} g/cm³.")
        elif variant == 1:
            choices = [f"{mass} g", f"{density + volume} g", f"{volume} g", f"{mass + volume} g"]
            stem_text = (f"Yoğunluğu {density} g/cm³ olan bir {material} parçası {volume} cm³ hacim kaplıyor. "
                         "Bu parçanın kütlesi kaç gramdır?")
            explanation = (f"Bu {material} parçasının kütlesi yoğunluk ile hacmin çarpımıdır: "
                           f"{density} × {volume} = {mass} g.")
        elif variant == 2:
            choices = [f"{volume} cm³", f"{density} cm³", f"{mass} cm³", f"{volume + density} cm³"]
            stem_text = (f"Kütlesi {mass} g ve yoğunluğu {density} g/cm³ olan bir {material} örneğinin "
                         "hacmi kaç santimetreküp olur?")
            explanation = (f"Bu {material} örneğinin hacmi kütlenin yoğunluğa bölünmesiyle bulunur: "
                           f"{mass} ÷ {density} = {volume} cm³.")
        elif variant == 3:
            liquid_density = density - 1
            choices = ["batar", "yüzer", "askıda kalır", "verilerle belirlenemez"]
            stem_text = (f"Yoğunluğu {density} g/cm³ olan bir {material} parçası, yoğunluğu "
                         f"{liquid_density} g/cm³ olan ve onunla tepkimeye girmeyen bir sıvıya bırakılıyor. "
                         "Parça için hangi gözlem beklenir?")
            explanation = (f"Bu {material} parçasının yoğunluğu sıvınınkinden büyüktür "
                           f"({density} > {liquid_density}); bu nedenle parça sıvıda batar.")
        else:
            other = materials[(seed + 3) % len(materials)]
            other_density = density + 1
            choices = [f"{other} daha yoğundur", f"{material} daha yoğundur",
                       "yoğunlukları eşittir", "hacim verilmeden karşılaştırılamaz"]
            stem_text = (f"Eşit hacimli {material} ve {other} örneklerinin kütleleri karşılaştırılıyor. "
                         f"{material} için yoğunluk {density} g/cm³, {other} için {other_density} g/cm³ bulunuyor. "
                         "Hangi sonuç doğrudur?")
            explanation = (f"Eşit hacimde yoğunluğu daha büyük olan madde daha fazla kütlelidir; "
                           f"{other_density} > {density} olduğu için {other}, {material} örneğinden daha yoğundur.")
    elif note_id == "tr-g06-fen-bilimleri-note-021":
        objects = ["kâğıt", "ekran", "kumaş", "duvar", "karton", "perde"]
        obj = objects[seed % len(objects)]
        variant = seed % 5
        correct = 0
        if variant == 0:
            choices = ["beyaz", "siyah", "sarı", "mor"]
            stem_text = (f"Karanlık bir odada {obj} üzerine eşit şiddette kırmızı, yeşil ve mavi ışık "
                         "aynı anda düşürülüyor. Işıkların örtüştüğü bölge hangi renkte görünür?")
            explanation = (f"Bu {obj} üzerinde kırmızı, yeşil ve mavi ana ışık renkleri eşit şiddette "
                           "birleştiğinde beyaz ışık algılanır.")
        elif variant == 1:
            choices = ["sarı", "camgöbeği", "mor", "siyah"]
            stem_text = (f"Beyaz bir {obj} üzerine yalnız kırmızı ve yeşil ışık eşit şiddette yansıtılıyor. "
                         "Işıkların kesiştiği alan hangi renkte görünür?")
            explanation = (f"Bu {obj} üzerinde kırmızı ve yeşil ışığın toplamsal karışımı sarı ışık oluşturur.")
        elif variant == 2:
            colors = ["kırmızı", "yeşil", "mavi"]
            color = colors[seed % 3]
            choices = [color, colors[(seed + 1) % 3], colors[(seed + 2) % 3], "beyaz"]
            stem_text = (f"Beyaz ışık, ideal bir {color} filtreden geçirilerek beyaz {obj} üzerine düşürülüyor. "
                         "Filtreyi geçen ışık hangi renktir?")
            explanation = (f"İdeal {color} filtre kendi rengindeki ışığı geçirip diğer renklerin büyük bölümünü "
                           f"soğurduğu için {obj} {color} ışıkla aydınlanır.")
        elif variant == 3:
            choices = ["siyah", "mavi", "yeşil", "beyaz"]
            stem_text = (f"Yalnız mavi ışıkla aydınlatılan odada kırmızı bir {obj} inceleniyor. "
                         "Cisim mavi ışığı belirgin biçimde yansıtmıyorsa nasıl görünür?")
            explanation = (f"Kırmızı {obj} mavi ışığı yansıtamadığından göze yeterli ışık ulaşmaz ve cisim siyaha "
                           "yakın görünür.")
        else:
            choices = ["kırmızıdan mora uzanan renk bandı", "yalnız yeşil bir leke",
                       "yalnız siyah bir gölge", "iki renkten oluşan sabit desen"]
            stem_text = (f"Dar bir beyaz ışık demeti prizmadan geçirilip beyaz {obj} üzerine düşürülüyor. "
                         "Ekranda hangi gözlem beyaz ışığın bileşenlerini kanıtlar?")
            explanation = (f"Prizma beyaz ışığı farklı oranlarda kırar; bu {obj} üzerinde kırmızıdan mora uzanan "
                           "bir renk bandı oluşturur.")
    elif note_id == "tr-g06-fen-bilimleri-note-030":
        conductors = ["bakır tel", "alüminyum folyo", "demir çivi", "çelik kaşık"]
        insulators = ["plastik cetvel", "cam çubuk", "kuru tahta", "kauçuk silgi"]
        answer = conductors[seed % len(conductors)]
        choices = [answer, insulators[seed % 4], insulators[(seed + 1) % 4], insulators[(seed + 2) % 4]]
        correct = 0
        contexts = ["masa lambası", "oyuncak motor", "uyarı zili", "model ev", "el feneri", "mini fan"]
        context = contexts[seed % len(contexts)]
        stem_text = (f"Bir {context} için pil, alıcı ve bağlantı kablolarıyla kurulan test devresinde boşluğa "
                     "aşağıdaki maddelerden hangisi yerleştirildiğinde lamba yanar?")
        explanation = (f"Bu {context} testinde {answer} elektrik akımını iletir ve devreyi tamamlar; plastik, cam, "
                       "kuru tahta ve kauçuk gibi maddeler bu koşullarda yalıtkandır.")
    elif note_id == "tr-g06-fen-bilimleri-note-031":
        short = 5 + (seed % 5) * 2
        long = short + 10
        metals = ["bakır", "alüminyum", "demir", "nikel", "çelik", "krom"]
        metal = metals[seed % len(metals)]
        choices = [f"{short} cm uzun, kalın {metal} tel", f"{long} cm uzun, kalın {metal} tel",
                   f"{short} cm uzun, ince {metal} tel", f"{long} cm uzun, ince {metal} tel"]
        correct = 0
        stem_text = (f"Aynı pil ve lambayla kurulan devrelerde yalnız {metal} telin uzunluğu ve kalınlığı "
                     "değiştiriliyor. Hangi tel kullanıldığında elektriksel direnç en az, lamba parlaklığı en fazla olur?")
        explanation = (f"Aynı cins {metal} tellerde kısa ve kalın telin direnci daha azdır; bu nedenle {short} cm "
                       f"uzunluğundaki kalın {metal} telle lamba en parlak yanar.")
    elif note_id == "tr-g06-fen-bilimleri-note-034":
        threats = ["sulak alanın kurutulması", "tarım ilacının aşırı kullanılması",
                   "ormanın parçalanması", "göle arıtılmamış atık bırakılması"]
        protections = ["yerli türlerin yaşam alanını korumak", "kaçak avcılığı denetlemek",
                       "atık suyu arıtmak", "doğal koridorlar oluşturmak"]
        answer = threats[seed % 4]
        choices = [answer, protections[seed % 4], protections[(seed + 1) % 4], protections[(seed + 2) % 4]]
        correct = 0
        stem_text = ("Bir bölgede tür sayısının azalmasını önlemeye yönelik çalışmalar planlanıyor. "
                     "Aşağıdakilerden hangisi biyoçeşitliliği koruyan bir uygulama değil, doğrudan tehdit eden bir etkendir?")
        explanation = (f"Bu durumda {answer} yaşam alanını veya canlıları olumsuz etkileyerek tür ve "
                       "birey sayısını azaltabilir; diğer uygulamalar koruma amacı taşır.")
    else:
        raise KeyError(note_id)
    reasons = []
    for index, choice in enumerate(choices):
        if index == correct:
            reasons.append(f"Bilimsel hesap veya sınıflandırma doğru: {explanation}")
        else:
            reasons.append(f"Değişken karıştırma yanılgısı: “{choice}” verilen deney koşulu ve bilimsel ilişkiyle uyuşmaz. {explanation}")
    return {"id": f"synthetic-{note_id}-{seed}", "question": stem_text,
            "choices": choices, "correct": correct, "distractorWhy": reasons,
            "explanation": explanation, "figure": None}


def read_subject(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines()
            if line.strip()]
    pack = next(row for row in rows if row.get("type") == "pack")
    notes = [row for row in rows if row.get("type") == "note"]
    questions = [row for row in rows if row.get("type") == "question"]
    if len(questions) != 500:
        raise ValueError(f"{path}: 500 ders sorusu bekleniyor, {len(questions)} bulundu")
    return pack, notes, questions


def stable(values: list[dict[str, Any]], salt: str) -> list[dict[str, Any]]:
    return sorted(values, key=lambda row: hashlib.sha256(
        f"{salt}\0{row.get('id')}".encode("utf-8")
    ).hexdigest())


def polish(value: str) -> str:
    value = clean(value)
    value = re.sub(r"\b0['’]dır\b", "0'dur", value, flags=re.I)
    value = re.sub(r"\bdünya(['’](?:da|de|dan|den|nın|ya|ye))", r"Dünya\1", value, flags=re.I)
    value = re.sub(r"\bay(['’](?:da|de|dan|den|ın|a|e))", r"Ay\1", value, flags=re.I)
    value = re.sub(r"\bgüneş(['’](?:ta|te|tan|ten|in|e))", r"Güneş\1", value, flags=re.I)
    value = re.sub(r"\b[A-D]\s+seçeneği\b", "Bu seçenek", value)
    for letter, ordinal in (("A", "birinci"), ("B", "ikinci"), ("C", "üçüncü"), ("D", "dördüncü")):
        value = re.sub(
            rf"(?i)bu\s+seçenek\s+{letter}['’]nin\b",
            f"Bu ifade {ordinal} konuşmacının",
            value,
        )
    value = re.sub(r"(?i)doğru\s+çıkarım\s+[A-D]['’]dir", "doğru çıkarım bu anlamdır", value)
    value = re.sub(r"(?i)doğru\s+cevap", "bu anlamı veren ifade", value)
    value = re.sub(
        r"(?i)\s*(?:bu nedenle\s+)?doğru\s+(?:cevap|yanıt)\s*[:\-]?\s*[A-D]"
        r"(?:\s+(?:seçeneği|seçenekleri|sıkkı))?[^.!?]*[.!?]?",
        " ", value,
    )
    return value


def answer_at(question: dict[str, Any], wanted_true: bool, salt: int) -> tuple[str, int]:
    correct = int(question["correct"])
    if wanted_true:
        return str(question["choices"][correct]), correct
    index = (correct + 1 + salt % 3) % 4
    if index == correct:
        index = (index + 1) % 4
    return str(question["choices"][index]), index


def truth_index(first: bool, second: bool) -> int:
    if first and not second:
        return 0
    if second and not first:
        return 1
    if first and second:
        return 2
    return 3


def case_text(label: str, question: dict[str, Any], proposed: str) -> str:
    stem = polish(str(question.get("question") or "")).rstrip()
    return f"{label}. problem: {stem} Önerilen yanıt: “{proposed}”."


def clone_source_labels(figure: dict[str, Any], source_labels: dict[str, str],
                        labels: dict[str, str], qid: str) -> None:
    """Copy only label values that the canonical figure actually references."""
    mapping: dict[str, str] = {}

    def remap(old_key: str) -> str:
        if old_key not in source_labels:
            raise ValueError(f"figure etiketi kaynak pakette yok: {old_key}")
        if old_key not in mapping:
            mapping[old_key] = f"{qid.replace('-', '.')}.source.{len(mapping) + 1}"
            labels[mapping[old_key]] = source_labels[old_key]
        return mapping[old_key]

    def walk(value: Any, field: str = "") -> Any:
        if isinstance(value, dict):
            for key, child in value.items():
                if key.endswith("Keys") and isinstance(child, list):
                    value[key] = [remap(item) if isinstance(item, str) else item for item in child]
                elif key in {"labels", "sideLabels", "axisKeys", "labelKeys"} and isinstance(child, dict):
                    value[key] = {name: remap(item) if isinstance(item, str) else item
                                  for name, item in child.items()}
                else:
                    value[key] = walk(child, key)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                value[index] = walk(child, field)
        elif isinstance(value, str) and (field == "key" or field.endswith("Key")):
            return remap(value)
        return value
    walk(figure)


def audit_table(qid: str, first_case: str, second_case: str,
                labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    keys = {name: f"{prefix}.{name}" for name in ("h1", "h2", "r1", "r2", "c1", "c2", "alt")}
    labels.update({
        keys["h1"]: "Kontrol kartı", keys["h2"]: "Problem ve önerilen yanıt",
        keys["r1"]: "I", keys["r2"]: "II", keys["c1"]: first_case,
        keys["c2"]: second_case,
        keys["alt"]: "İki ayrı problem ile her problem için önerilen yanıtı gösteren tablo; yanıtların doğru olup olmadığı belirtilmemiştir.",
    })
    return {"kind": "table", "headerKeys": [keys["h1"], keys["h2"]],
            "rows": [[{"key": keys["r1"]}, {"key": keys["c1"]}],
                     [{"key": keys["r2"]}, {"key": keys["c2"]}]],
            "altTextKey": keys["alt"]}


def case_reason(question: dict[str, Any], proposed_index: int, is_true: bool) -> str:
    correct = str(question["choices"][int(question["correct"])])
    proposed = str(question["choices"][proposed_index])
    explanation = polish(str(question.get("explanation") or "")).rstrip(".!? ")
    if is_true:
        return (f"Önerilen “{proposed}” yanıtı konu bilgisiyle uyuşur. {explanation}.")
    why = polish(str((question.get("distractorWhy") or [""] * 4)[proposed_index])).rstrip(".!? ")
    return (f"Önerilen “{proposed}” yanıtı “{correct}” yerine seçilmiştir. "
            f"{why}. Doğru düzeltme şu bilgiye dayanır: {explanation}.")


def make_question(*, number: int, local: int, note: dict[str, Any],
                  first: dict[str, Any], second: dict[str, Any], mode: str,
                  level: int, correct_position: int, truth_pair: tuple[bool, bool],
                  source_labels: dict[str, str], labels: dict[str, str]) -> dict[str, Any]:
    qid = f"tr-g06-bank-q{number:04d}"
    first_answer, first_index = answer_at(first, truth_pair[0], number)
    second_answer, second_index = answer_at(second, truth_pair[1], number + 1)
    first_case = case_text("I", first, first_answer)
    second_case = case_text("II", second, second_answer)

    source_figure = copy.deepcopy(first.get("figure")) if first.get("figure") else None
    if source_figure:
        clone_source_labels(source_figure, source_labels, labels, qid)
        figure = source_figure
        if mode == "error-analysis":
            question_text = (
                f"Aşağıdaki görseli inceleyiniz. Bir öğrenci “{first_answer}” ve “{second_answer}” "
                f"yanıtlarını yazmıştır; en az biri hatalıdır. {first_case} {second_case} "
                "Hatalı yanıt veya yanıtları doğru belirleyen seçenek hangisidir?"
            )
        elif mode == "application":
            question_text = (
                f"Aşağıdaki görseli ve iki uygulama kartını birlikte inceleyiniz. {first_case} "
                f"{second_case} Her problem kendi koşullarında çözüldüğünde hangi sonuca ulaşılır?"
            )
        elif mode == "comprehension":
            question_text = (
                f"Aşağıdaki görsel I. problem için kanıt sunmaktadır. {first_case} {second_case} "
                "Konu anlatımındaki temel bilgiye göre hangi değerlendirme doğrudur?"
            )
        else:
            question_text = (
                f"Aşağıdaki görseli ve iki problem kartını birlikte inceleyiniz. {first_case} "
                f"{second_case} Kanıtlar çözümlendiğinde hangi değerlendirme doğrudur?"
            )
    elif mode == "analysis":
        figure = audit_table(qid, first_case, second_case, labels)
        question_text = (
            f"Aşağıdaki tabloyu inceleyiniz. {OPENERS[number % len(OPENERS)]} "
            f"I. kart “{first_answer}”, II. kart “{second_answer}” "
            f"yanıtını önermektedir. {first_case} {second_case} "
            "Aynı bilgiler karşılaştırma tablosunda da düzenlenmiştir. "
            "Konu anlatımına göre hangi değerlendirme doğrudur?"
        )
    elif mode == "error-analysis":
        figure = None
        question_text = (
            f"Bir öğrenci “{first_answer}” ve “{second_answer}” yanıtlarını iki ayrı problem için "
            "yazmıştır; en az bir yanıtı hatalıdır. "
            f"{first_case} {second_case} Hatalı yanıt veya yanıtları doğru belirleyen seçenek hangisidir?"
        )
    elif mode == "application":
        figure = None
        question_text = (
            f"{OPENERS[number % len(OPENERS)]} {first_case} {second_case} "
            "Her problem kendi koşulları içinde çözüldüğünde hangi sonuca ulaşılır?"
        )
    else:
        figure = None
        question_text = (
            f"{OPENERS[number % len(OPENERS)]} {first_case} {second_case} "
            "Konu anlatımındaki temel bilgiye göre hangi değerlendirme doğrudur?"
        )

    first_correct = str(first["choices"][int(first["correct"])])
    second_correct = str(second["choices"][int(second["correct"])])
    semantic_options = [
        f"I. karttaki “{first_answer}” yanıtı onaylanmalı, II. karttaki “{second_answer}” yanıtı düzeltilmelidir.",
        f"II. karttaki “{second_answer}” yanıtı onaylanmalı, I. karttaki “{first_answer}” yanıtı düzeltilmelidir.",
        f"I. karttaki “{first_answer}” ve II. karttaki “{second_answer}” yanıtlarının ikisi de onaylanmalıdır.",
        f"I. karttaki “{first_answer}” ve II. karttaki “{second_answer}” yanıtlarının ikisi de düzeltilmelidir.",
    ]
    semantic_correct = truth_index(*truth_pair)
    correct_option = semantic_options[semantic_correct]
    wrong_options = [value for index, value in enumerate(semantic_options) if index != semantic_correct]
    choices = wrong_options[:correct_position] + [correct_option] + wrong_options[correct_position:]
    reasons = []
    actual = semantic_correct
    for choice in choices:
        candidate = semantic_options.index(choice)
        if candidate == actual:
            reasons.append(
                f"Kanıta uygun çift denetim: I. kartın doğru yanıtı “{first_correct}”, "
                f"II. kartın doğru yanıtı “{second_correct}”dır; bu seçenek iki sonucu da eksiksiz ifade eder."
            )
        else:
            prefix = REASON_PREFIXES[candidate][number % len(REASON_PREFIXES[candidate])]
            candidate_pair = ((True, False), (False, True), (True, True), (False, False))[candidate]
            reasons.append(
                f"{prefix}: Seçenek I. kartı {'doğru' if candidate_pair[0] else 'yanlış'}, II. kartı "
                f"{'doğru' if candidate_pair[1] else 'yanlış'} sayar. Oysa I. kartta doğru yanıt "
                f"“{first_correct}”, II. kartta “{second_correct}” olmalıdır."
            )

    first_reason = case_reason(first, first_index, truth_pair[0])
    second_reason = case_reason(second, second_index, truth_pair[1])
    explanation = (
        f"I. kartın denetimi: {first_reason} II. kartın denetimi: {second_reason} "
        f"Bu iki denetim birlikte ele alındığında “{correct_option}” sonucuna ulaşılır."
    )
    objective = str(note.get("objective") or (note.get("objectives") or [""])[0])
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "Birinci problemdeki veri ve iki kartın karşılaştırması görsel kanıtla çözülür.",
        "acceptableKinds": [str(figure["kind"])], "evidenceDimensions": ["I. kart", "II. kart"],
    } if figure else {
        "level": "none", "role": "none",
        "rationale": "Her iki problem ve önerilen yanıt soru metninde eksiksiz verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": number,
        "subject": note.get("subject"), "grade": 6, "unitKey": note.get("unitKey"),
        "topicKey": note.get("topicKey"), "subtopicKey": note.get("subtopicKey"),
        "topic": note.get("topic"), "title": f"{note.get('title')} — {mode}",
        "objective": objective, "objectiveId": objective, "noteId": note.get("id"),
        "noteKey": note.get("id"), "question": question_text, "choices": choices,
        "correct": correct_position, "correctIndex": correct_position,
        "correctOption": choices[correct_position], "distractorWhy": reasons,
        "explanation": explanation, "level": level,
        "difficultyReason": (
            f"Düzey {level}; {note.get('title')} kazanımında iki bağımsız problem–yanıt "
            f"eşleşmesini {mode} biçiminde çözüp sonuçları birleştirmeyi gerektirir."
        ),
        "questionType": mode, "familyId": f"tr-g06-bank-family-{number:04d}",
        "objectiveSource": note.get("objectiveSource"),
        "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": list(note.get("sourceRefs") or []), "visualNeed": visual_need,
        "visualRequirement": "required" if figure else "none",
        "figure": figure, "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    raise RuntimeError(
        "REJECTED producer: embeds source-question roots and uses one cognitive archetype; "
        "use subject-specific note-only authoring batches"
    )
    labels: dict[str, str] = {}
    questions: list[dict[str, Any]] = []
    number = 0
    source_records_used: set[str] = set()
    for subject, quota in SUBJECT_QUOTAS.items():
        path = next(path for path in sorted(GRADE_ROOT.glob("*/*-tum.jsonl"))
                    if path.parent.name != "soru-bankasi"
                    and json.loads(path.read_text(encoding="utf-8-sig").splitlines()[0]).get("subject") == subject)
        pack, notes, source_questions = read_subject(path)
        by_note: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for question in source_questions:
            by_note[str(question["noteId"])].append(question)
        allocations = allocate(quota, notes)
        source_labels = dict(pack.get("labels") or {})
        for note in notes:
            note_id = str(note["id"])
            pool = stable(by_note[note_id], f"g6-v3:{note_id}")
            if note_id in SPECIAL_SCIENCE_NOTES:
                pool = [synthetic_science_question(note_id, seed) for seed in range(64)]
            nonvisual = [row for row in pool if not row.get("figure")]
            visual = [row for row in pool if row.get("figure")]
            if len(pool) < 2:
                raise ValueError(f"{note_id}: iki ayrı ders sorusu bulunamadı")
            ordinary_left = pool
            secondary_base = nonvisual if nonvisual else pool
            ordinary_pairs = stable(
                [{"id": f"{left['id']}::{right['id']}", "left": left, "right": right}
                 for left in ordinary_left for right in secondary_base
                 if left["id"] != right["id"]],
                f"g6-v3-pairs:{note_id}",
            )
            analysis_pairs = stable(
                [{"id": f"{left['id']}::{right['id']}", "left": left, "right": right}
                 for left in (visual or ordinary_left) for right in secondary_base
                 if left["id"] != right["id"]],
                f"g6-v3-analysis-pairs:{note_id}",
            )
            ordinary_cursor = 0
            analysis_cursor = 0
            for local in range(allocations[note_id]):
                number += 1
                batch, offset = (number - 1) // 100, (number - 1) % 100
                modes = batch_schedule(batch, [("comprehension", 25), ("application", 35),
                                                ("analysis", 25), ("error-analysis", 15)], "g6-v3-mode")
                levels = batch_schedule(batch, [(1, 20), (2, 25), (3, 30), (4, 20), (5, 5)],
                                         "g6-v3-level")
                answers = batch_schedule(batch, [(0, 25), (1, 25), (2, 25), (3, 25)],
                                          "g6-v3-answer")
                mode = modes[offset]
                if mode == "analysis":
                    shift = PAIR_SHIFTS.get(f"tr-g06-bank-q{number:04d}", 0)
                    pair = analysis_pairs[(analysis_cursor + shift) % len(analysis_pairs)]
                    analysis_cursor += 1
                else:
                    shift = PAIR_SHIFTS.get(f"tr-g06-bank-q{number:04d}", 0)
                    pair = ordinary_pairs[(ordinary_cursor + shift) % len(ordinary_pairs)]
                    ordinary_cursor += 1
                first, second = pair["left"], pair["right"]
                pattern = (local + number // 7) % 4
                truth_pair = ((True, False), (False, True), (True, True), (False, False))[pattern]
                if mode == "error-analysis" and truth_pair == (True, True):
                    truth_pair = (False, True)
                source_records_used.update((str(first["id"]), str(second["id"])))
                questions.append(make_question(
                    number=number, local=local, note=note, first=first, second=second,
                    mode=mode, level=levels[offset], correct_position=answers[offset],
                    truth_pair=truth_pair, source_labels=source_labels, labels=labels,
                ))
    if number != 2000:
        raise AssertionError(number)
    AUTHORING_ROOT.mkdir(parents=True, exist_ok=True)
    QUESTION_PATH.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":"))
                                       for row in questions) + "\n", encoding="utf-8", newline="\n")
    LABEL_PATH.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                          encoding="utf-8", newline="\n")
    print(json.dumps({"grade": 6, "questions": len(questions), "labels": len(labels),
                      "status": "PENDING_REVIEW", "sourceQuestionRecordsRead": 3500,
                      "distinctSourceQuestionRecordsUsed": len(source_records_used),
                      "composition": "two-case-solution-audit"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
