#!/usr/bin/env python3
"""Author the grade-6 bank from lesson notes, never from lesson questions.

The script deliberately reads only pack and note records.  Worked examples are
treated as curriculum-grounded knowledge seeds; every bank item receives a new
decision context, stem, option wording and explanation.  Output remains pending
until the separate hash-bound review stage passes.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GRADE_ROOT = ROOT / "turkiye" / "6-sinif"
AUTHORING_ROOT = ROOT / "authoring" / "question-bank-blueprints"
QUESTION_PATH = AUTHORING_ROOT / "grade-6.jsonl"
LABEL_PATH = AUTHORING_ROOT / "grade-6-labels.json"

SUBJECT_QUOTAS = {
    "Bilişim Teknolojileri ve Yazılım": 294,
    "Din Kültürü ve Ahlak Bilgisi": 240,
    "Fen Bilimleri": 376,
    "İngilizce": 247,
    "Matematik": 286,
    "Sosyal Bilgiler": 240,
    "Türkçe": 317,
}

CONTEXTS = (
    "Bir okul proje ekibi çözüm günlüğündeki kararı kanıtla sınamaktadır.",
    "Bir öğrenci kulübü hazırladığı uygulama kartını akran değerlendirmesine açmıştır.",
    "Ders sonunda iki farklı görüşü karşılaştıran ekip ortak bir sonuca ulaşacaktır.",
    "Bir araştırma grubu topladığı bilgiyi kazanım ölçütlerine göre denetlemektedir.",
    "Sınıf panosuna asılacak açıklama yayımlanmadan önce doğruluk kontrolünden geçmektedir.",
    "Bir atölye ekibi gerçek yaşam durumuna ilişkin çözümünü gerekçelendirmektedir.",
    "Öğrenciler bir çalışma istasyonundaki bulguyu kanıt ve sonuç olarak ayırmaktadır.",
    "Bir öğrenme topluluğu örnek olayı inceleyip hatalı genellemeleri elemiştir.",
    "Okul meclisinin çalışma grubu önerileri aynı ölçütle karşılaştırmaktadır.",
    "Bir bilim ve düşünme kulübü rapordaki çıkarımı bağımsız olarak doğrulamaktadır.",
    "Akran öğretimi yapan bir grup, seçilecek yanıtın nedenini açıkça yazacaktır.",
    "Bir sınıf komisyonu karar vermeden önce verilen koşulların tümünü işaretlemektedir.",
    "Bir dijital portfolyo kaydı, konu anlatımındaki ilkeye uygunluk açısından incelenmektedir.",
    "Bir problem çözme ekibi ilk tahminini kanıtlarla yeniden değerlendirmektedir.",
    "Bir öğrenci hazırladığı çözümü öz kontrol listesindeki adımlarla karşılaştırmaktadır.",
    "Bir okul gazetesi bilgi kutusunu yayımlamadan önce uzman görüşlerini tartışmaktadır.",
    "Bir tasarım ekibi kullanacağı yöntemi amaç, veri ve sonuç ilişkisine göre seçmektedir.",
    "Bir sınıf içi münazarada her iddianın dayandığı koşul ayrı ayrı sorgulanmaktadır.",
    "Bir öğrenme istasyonunda verilen durum için en tutarlı açıklama aranacaktır.",
    "Bir değerlendirme kurulu, yüzeysel benzerlik yerine doğrudan kanıtı esas almaktadır.",
    "Bir rehber kart hazırlanırken kavram, işlem ve sonuç arasındaki bağ denetlenmektedir.",
    "Bir ekip yanlış anlaşılabilecek ifadeleri ayıklayıp açık bir karar cümlesi kuracaktır.",
    "Bir sınıf araştırmasında gözlem ile yorumun birbirine karıştırılmaması istenmektedir.",
    "Bir uygulama dosyasında sonucun bütün başlangıç koşullarını karşılaması beklenmektedir.",
)

TASKS = {
    "comprehension": (
        "Temel kavramın anlamını koruyan değerlendirme hangisidir?",
        "Konu anlatımındaki doğrudan bilgiyle uyuşan karar hangisidir?",
        "Verilen durumu doğru kavramla eşleştiren öğrenci kararı hangisidir?",
        "Ana ilkeyi değiştirmeden açıklayan seçenek hangisidir?",
    ),
    "application": (
        "Bu bilgi yeni duruma uygulandığında hangi karar verilmelidir?",
        "Koşullar adım adım kullanıldığında hangi uygulama sonucu elde edilir?",
        "Amaç ile yöntem birlikte düşünüldüğünde hangi seçim yapılmalıdır?",
        "Öğrenilen ilkeyi bu özel duruma doğru aktaran seçenek hangisidir?",
    ),
    "analysis": (
        "Tablodaki durum ve ölçüt birlikte çözümlendiğinde hangi sonuç desteklenir?",
        "Kanıt tablosundaki iki kayıt arasında doğru ilişkiyi kuran seçenek hangisidir?",
        "Veri ile değerlendirme ölçütünü birlikte kullanan karar hangisidir?",
        "Tablodaki kanıtı eksiksiz yorumlayan açıklama hangisidir?",
    ),
    "error-analysis": (
        "İlk karardaki yanılgıyı düzelten değerlendirme hangisidir?",
        "Koşullardan birini atlayan çözüm yerine hangi karar yazılmalıdır?",
        "Hatalı genelleme çıkarıldığında hangi sonuç geçerli kalır?",
        "Yanlış yorumun yerine kanıta dayalı hangi seçenek getirilmelidir?",
    ),
}

DECISION_NAMES = (
    "Aylin", "Baran", "Ceren", "Deniz", "Ekin", "Fırat", "Gökçe", "Hakan",
    "İpek", "Kerem", "Lale", "Mert", "Nehir", "Ozan", "Pelin", "Rüzgâr",
)

CHECKPOINTS = (
    "tutarlılık", "kapsam", "kanıt", "bağlam", "amaç", "yöntem", "sonuç", "kavram",
    "işlem", "sıralama", "karşılaştırma", "sınıflama", "neden", "etki", "ölçüt", "doğrulama",
    "uygulama", "yorum", "çıkarım", "örnek", "veri", "temsil", "iletişim", "öz kontrol",
)

AUDIT_TRAILS = (
    "Önce temel kavram tanımlanacak, sonra durumdaki belirleyici ayrıntı bulunacak ve son karar iki bilgi açıkça ilişkilendirilerek yazılacaktır.",
    "Her seçenek aynı ölçütle sınanacak; yalnız bir bölümle uyuşan fakat diğer koşulu bozan görüşler sonuç kaydına alınmayacaktır.",
    "İncelemede önce verilenler ile istenen ayrılacak, ardından doğrudan kanıt sunmayan varsayımlar tek tek değerlendirme dışında bırakılacaktır.",
    "Karar sürecinde kavramın kapsamı belirlenecek, örnek olay bu kapsama yerleştirilecek ve aşırı genellemeler ayrıca işaretlenecektir.",
    "Ekip önce amaç ile yöntemi eşleştirecek, sonra işlemin beklenen sonucu üretip üretmediğini bağımsız bir kontrol adımıyla sınayacaktır.",
    "Değerlendirme, ilk tahmini doğrulamaya çalışmak yerine her görüşün hangi koşula dayandığını ve hangi koşulla çeliştiğini gösterecektir.",
    "Çözüm günlüğünde gözlem, yorum ve sonuç ayrı satırlarda düşünülecek; aralarındaki mantıksal bağ kurulmadan seçenek işaretlenmeyecektir.",
    "Önce doğru sıra veya ilişki kurulacak, sonra eksik basamak içeren görüşler elenecek ve kalan sonuç başlangıç durumuyla karşılaştırılacaktır.",
    "Kanıtların tümü birlikte okunacak; yalnız anahtar bir sözcüğe dayanan seçimler yerine bağlamın tamamını açıklayan karar aranacaktır.",
    "İki olası yorum arasındaki fark somutlaştırılacak, kavram karışıklığına yol açan ifade bulunacak ve düzeltme gerekçesiyle kaydedilecektir.",
    "Sonuçtan geriye doğru kontrol yapılacak; seçilen görüşün hem konu ölçütünü hem de örnek olayın özel ayrıntılarını koruması beklenecektir.",
    "İnceleme sırasında ilgisiz bilgiler ayıklanacak, kalan kanıtlar sınıflandırılacak ve yalnız desteklenen çıkarım karar cümlesine dönüştürülecektir.",
    "Her görüş için kısa bir karşı örnek düşünülecek; kolayca çürütülen genellemeler elendikten sonra dayanıklı açıklama seçilecektir.",
    "Kullanılan terimlerin anlamı önce netleştirilecek, benzer görünen kavramlar ayrılacak ve seçim bu ayrımı bozmayacak biçimde yapılacaktır.",
    "Ekip, verilen durumdaki neden ile sonucu yer değiştirmeden okuyacak ve yönü ters kuran açıklamaları gerekçesiyle eleyecektir.",
    "Son karar yazılmadan önce veri, işlem ve yorumun birbirini destekleyip desteklemediği üç aşamalı bir öz kontrolle doğrulanacaktır.",
    "Çözüm, konu anlatımındaki örneği ezberden yinelemek yerine aynı ilkenin bu yeni kayıtta nasıl çalıştığını açıklamak zorundadır.",
    "Seçenekler önce doğruluk sonra uygunluk bakımından incelenecek; doğru bilgi içerse bile sorunun bağlamına uymayan görüş seçilmeyecektir.",
    "Karşılaştırmada ölçülebilir kanıtlar öne alınacak, kişisel varsayımlar ayrılacak ve sonuç yalnız eldeki kayıtla sınırlandırılacaktır.",
    "Bir hata bulunduğunda yalnız yanlış seçenek elenmeyecek; hatanın türü adlandırılıp doğru ilişkinin nasıl kurulacağı da gösterilecektir.",
    "İlk ve son koşullar ayrı ayrı doğrulanacak, aradaki işlem basamakları izlenecek ve herhangi bir kopukluk varsa görüş geçersiz sayılacaktır.",
    "Ekip, aynı sözcüğün farklı anlamlarını karıştırmamak için bağlam ipuçlarını belirleyecek ve kararı bu ipuçlarıyla gerekçelendirecektir.",
    "Temsil ile gerçek durum arasındaki eşleşme incelenecek, tabloda bulunmayan bir ayrıntıyı varsayan seçenekler değerlendirme dışı kalacaktır.",
    "Sonuç cümlesi açık, sınırlı ve kanıtlanabilir kurulacak; kesinlik bildiren fakat yeterli veriye dayanmayan yorumlar kabul edilmeyecektir.",
)

VARIANT_FRAMES = (
    "Bu kayıtta amaç, tanımı doğrudan tanımak ve ilgisiz ayrıntıları elemek olacaktır.",
    "Çözüm, aynı ilkenin günlük yaşamda hangi sonucu doğurduğunu göstermelidir.",
    "İki farklı iddia, dayandıkları kanıt ve vardıkları sonuç bakımından karşılaştırılacaktır.",
    "Önceki çözümdeki kavram yanılgısı bulunup doğru ilişki açıkça yeniden kurulacaktır.",
    "Karar, verilenlerin tümünü kullanmalı ve metinde bulunmayan bir varsayıma dayanmamalıdır.",
    "Sonuçtan geriye doğru gidilerek her işlem veya yorum basamağının geçerliliği sınanacaktır.",
    "Bir karşı örnek düşünülerek aşırı genelleme içeren seçenekler değerlendirme dışında bırakılacaktır.",
    "Temsil edilen veri ile konu anlatımındaki ölçüt eşleştirilip yalnız desteklenen çıkarım seçilecektir.",
)


def compact(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def clean(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip(" \t\r\n.;")
    return value.replace("i\u0307", "i").replace("..", ".")


def normalized(value: str) -> str:
    return re.sub(r"[^\w]+", " ", value.casefold()).strip()


def compatible_distractor(answer: str, candidate: str) -> bool:
    number_only = r"-?\d+(?:[.,]\d+)?(?:\s*%|\s*[a-zA-Z²³]+)?"
    answer_numeric = re.fullmatch(number_only, answer) is not None
    candidate_numeric = re.fullmatch(number_only, candidate) is not None
    if answer_numeric != candidate_numeric:
        return False
    answer_words = len(answer.split())
    candidate_words = len(candidate.split())
    if answer_words >= 5 and candidate_words < 4:
        return False
    if answer_words <= 2 and candidate_words > 14:
        return False
    return True


def scrub_option_letter_claims(value: str) -> str:
    """Remove source-example A/B/C/D announcements after options are rewritten."""
    value = re.sub(
        r"(?i)\b(?:doğru\s+)?(?:cevap|yanıt|şık|seçenek)\s*[:\-]?\s*[A-D]"
        r"(?:['’](?:dır|dir|dur|dür|tır|tir|tur|tür))?\b\.?”?",
        "Bu sonuç doğrudur.",
        value,
    )
    value = re.sub(
        r"(?i)\b[A-D]\s+(?:şıkkı|şıkkında|seçeneği|seçeneğinde)\b",
        "doğru seçenek",
        value,
    )
    return clean(value)


def safe_lower_title(value: str) -> str:
    lowered = value.replace("İ", "i").replace("I", "ı").lower().replace("i\u0307", "i")
    for name in ("güneş", "dünya", "ay"):
        lowered = re.sub(rf"\b{name}\b", name.capitalize(), lowered)
    return lowered


def read_pack_and_notes(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    pack: dict[str, Any] | None = None
    notes: list[dict[str, Any]] = []
    # Question rows are intentionally neither parsed nor retained.
    with path.open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            if not line.strip():
                continue
            marker = re.search(r'"type"\s*:\s*"([^"]+)"', line[:160])
            record_type = marker.group(1) if marker else "question"
            if record_type not in {"pack", "note"}:
                continue
            row = json.loads(line)
            if record_type == "pack":
                pack = row
            else:
                notes.append(row)
    if pack is None or not notes:
        raise ValueError(f"Paket/not topolojisi geçersiz: {path}")
    return pack, notes


def parse_example(value: str) -> tuple[str, str, str]:
    text = clean(value)
    if not re.search(r"(?i)\bSoru\s*:", text):
        core, _, rationale = text.partition("Gerekçeli kontrol:")
        core = clean(core)
        rationale = clean(rationale) or core
        if "," in core:
            situation, conclusion = map(clean, core.split(",", 1))
            if situation and conclusion:
                conclusion = conclusion[0].upper() + conclusion[1:]
                return f"{situation} durumu değerlendiriliyor.", conclusion, rationale
        if ";" in core:
            situation, conclusion = map(clean, core.split(";", 1))
            if situation and conclusion:
                conclusion = conclusion[0].upper() + conclusion[1:]
                return f"{situation} durumu değerlendiriliyor.", conclusion, rationale
        conditional = re.match(r"^(.+?\b(?:ise|[a-zçğıöşü]+[rs][ae]))\s+(.+)$", core, re.IGNORECASE)
        if conditional:
            situation, conclusion = map(clean, conditional.groups())
            conclusion = conclusion[0].upper() + conclusion[1:]
            return f"{situation} durumu değerlendiriliyor.", conclusion, rationale
        return (
            f"Şu konu cümlesinin dayandığı ilişki değerlendiriliyor: {core}",
            core,
            rationale,
        )
    match = re.search(
        r"(?:^|\s)Soru:\s*(.*?)\s*(?:Aşağıdaki seçenek tablosunu da kullanınız\.\s*)?"
        r"Doğru yanıt:\s*(.*?)\s*Gerekçe:\s*(.*)$",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        fallback = re.search(
            r"(?:^|\s)Soru:\s*(.*?)\s*(?:Çözüm|Yanıt):\s*(.*)$",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if not fallback:
            if len(text) < 40:
                raise ValueError(f"Çözümlü örnek ayrıştırılamadı: {text[:100]}")
            return (
                text,
                "Verilen açıklama konu ölçütüne uygundur",
                text,
            )
        scenario, solution = map(clean, fallback.groups())
        first_sentence = re.split(r"(?<=[.!?])\s+", solution, maxsplit=1)[0]
        answer = clean(first_sentence)
        reason = solution
        return scenario, answer, reason
    scenario, answer, reason = map(clean, match.groups())
    scenario = re.sub(
        r"\s*Aşağıdaki seçenek tablosunu da kullanınız\.?\s*$", "", scenario,
        flags=re.IGNORECASE,
    )
    answer = re.sub(r"^[A-D][).:-]\s*", "", answer).strip()
    return scenario, answer, reason


def mistake_candidates(value: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", clean(value))
    result: list[str] = []
    for sentence in sentences:
        sentence = clean(re.sub(r"^(?:Doğru seçenek|Yanlış seçenek)\s*:\s*", "", sentence))
        if not sentence:
            continue
        candidate = clean(re.split(r"[,;:]", sentence, maxsplit=1)[0])
        if re.match(r"(?i)^(?:bu|şu)\s+(?:seçenek|ifade|yanıt|cevap)\b", candidate):
            continue
        if 1 <= len(candidate.split()) <= 16 and len(candidate) <= 150:
            if normalized(candidate) not in {normalized(old) for old in result}:
                result.append(candidate)
    return result


def fallback_wrongs(answer: str, title: str) -> list[str]:
    if re.fullmatch(r"-?\d+(?:[.,]\d+)?(?:\s*%|\s*[a-zA-Z²³]+)?", answer):
        match = re.search(r"-?\d+(?:[.,]\d+)?", answer)
        assert match is not None
        value = float(match.group().replace(",", "."))
        unit = answer[match.end():].strip()

        def number_text(candidate: float) -> str:
            rendered = str(int(candidate)) if candidate.is_integer() else f"{candidate:.2f}".rstrip("0").rstrip(".")
            return f"{rendered}{(' ' + unit) if unit else ''}"

        delta = max(1.0, abs(value) * 0.2)
        raw_candidates = (
            value + delta, value - delta, value + 2 * delta, value - 2 * delta,
            value * 2 if value else 3 * delta, value / 2 if value else -3 * delta,
        )
        return list(dict.fromkeys(number_text(candidate) for candidate in raw_candidates if candidate != value))

    if re.search(r"\b(?:must|mustn't|can|can't|should|shouldn't|is|are|has|have)\b", answer, re.IGNORECASE):
        transforms = (
            (r"\bmustn't\b", "can"), (r"\bmust\b", "mustn't"),
            (r"\bcan't\b", "can"), (r"\bcan\b", "can't"),
            (r"\bshouldn't\b", "should"), (r"\bshould\b", "shouldn't"),
            (r"\bis\b", "isn't"), (r"\bare\b", "aren't"),
            (r"\bhas\b", "doesn't have"), (r"\bhave\b", "don't have"),
        )
        variants: list[str] = []
        for pattern, replacement in transforms:
            changed = re.sub(pattern, replacement, answer, count=1, flags=re.IGNORECASE)
            if changed != answer and normalized(changed) not in {normalized(item) for item in variants}:
                variants.append(changed)
        variants.extend([
            f"It is unrelated to {safe_lower_title(title)}.",
            f"The opposite rule applies in {safe_lower_title(title)}.",
        ])
        return variants

    if any(word in f"{title} {answer}".casefold() for word in ("algoritma", "programlama", "döngü", "blok")):
        return [
            "Karakteri yalnız bir kez ilerletip engel koşulunu hiç denetlememek",
            "Engel kontrolünü döngüden önce yalnız bir kez yapıp uyarı mesajını çalıştırmamak",
            "Engel oluştuğunda hareketi sürdürmek ve uyarı mesajını göstermemek",
            "Koşulun doğru ve yanlış dallarını değiştirerek işlem sırasını ters kurmak",
        ]

    replacements = (
        (r"\bdoğrudur\b", "yanlıştır"),
        (r"\byanlıştır\b", "doğrudur"), (r"\bartar\b", "azalır"),
        (r"\bazalır\b", "artar"), (r"\baynı\b", "farklı"),
        (r"\bfarklı\b", "aynı"), (r"\bönce\b", "sonra"),
        (r"\bsonra\b", "önce"), (r"\bvardır\b", "yoktur"),
        (r"\byoktur\b", "vardır"), (r"\bolur\b", "olmaz"),
        (r"\bolmaz\b", "olur"), (r"\bgerekir\b", "gerekmez"),
        (r"\bgerekmez\b", "gerekir"),
        (r"\bedilir\b", "edilmez"), (r"\bsağlar\b", "sağlamaz"),
        (r"\bgösterir\b", "göstermez"), (r"\bbildirir\b", "bildirmez"),
        (r"\bifade eder\b", "ifade etmez"), (r"\bsöyler\b", "söylemez"),
    )
    variants: list[str] = []
    copula = re.sub(r"(?:dır|dir|dur|dür|tır|tir|tur|tür)\.?$", " değildir", answer, flags=re.IGNORECASE)
    if copula != answer:
        variants.append(clean(copula))
    for pattern, replacement in replacements:
        changed = re.sub(pattern, replacement, answer, count=1, flags=re.IGNORECASE)
        if changed != answer and normalized(changed) not in {normalized(item) for item in variants}:
            variants.append(changed)
    variants.extend([
        f"{answer} değildir; verilen koşullarda karşıt ilişki geçerlidir",
        f"{answer} yalnız konu dışındaki durumlarda geçerlidir",
        f"{answer} yerine neden ile sonuç ters yönde kurulmalıdır",
        f"{answer} için verilen kanıt yetersizdir ve sonuç çıkarılamaz",
    ])
    return variants


def allocate(total: int, notes: list[dict[str, Any]]) -> dict[str, int]:
    base, remainder = divmod(total, len(notes))
    return {
        str(note["id"]): base + int(index < remainder)
        for index, note in enumerate(notes)
    }


def batch_schedule(batch: int, counts: list[tuple[Any, int]], seed: str) -> list[Any]:
    values = [value for value, count in counts for _ in range(count)]
    return [
        value for _, value in sorted(
            (hashlib.sha256(f"{seed}:{batch}:{index}:{value}".encode()).hexdigest(), value)
            for index, value in enumerate(values)
        )
    ]


def figure_for(
    question_id: str,
    scenario: str,
    title: str,
    labels: dict[str, str],
) -> dict[str, Any]:
    prefix = question_id.replace("-", ".")
    keys = {
        "h1": f"{prefix}.figure.h1",
        "h2": f"{prefix}.figure.h2",
        "r1": f"{prefix}.figure.r1",
        "r2": f"{prefix}.figure.r2",
        "scenario": f"{prefix}.figure.scenario",
        "criterion": f"{prefix}.figure.criterion",
        "alt": f"{prefix}.figure.alt",
    }
    labels.update({
        keys["h1"]: "Kanıt kaydı",
        keys["h2"]: "İncelenecek içerik",
        keys["r1"]: "Durum",
        keys["r2"]: "Değerlendirme ölçütü",
        keys["scenario"]: scenario,
        keys["criterion"]: title,
        keys["alt"]: (
            "Bir durum ile değerlendirme ölçütünü iki ayrı satırda gösteren kanıt tablosu; "
            "doğru seçenek veya çözüm sonucu işaretlenmemiştir."
        ),
    })
    return {
        "kind": "table",
        "headerKeys": [keys["h1"], keys["h2"]],
        "rows": [
            [{"key": keys["r1"]}, {"key": keys["scenario"]}],
            [{"key": keys["r2"]}, {"key": keys["criterion"]}],
        ],
        "altTextKey": keys["alt"],
    }


def include_figure_labels(value: Any, available: dict[str, Any], labels: dict[str, str], field: str = "") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if (key == "key" or key.endswith("Key")) and isinstance(child, str) and child in available:
                labels[child] = str(available[child])
            elif key.endswith("Keys") and isinstance(child, list):
                for item in child:
                    if isinstance(item, str) and item in available:
                        labels[item] = str(available[item])
            elif key in {"labels", "sideLabels", "axisKeys", "labelKeys"} and isinstance(child, dict):
                for item in child.values():
                    if isinstance(item, str) and item in available:
                        labels[item] = str(available[item])
            else:
                include_figure_labels(child, available, labels, key)
    elif isinstance(value, list):
        for child in value:
            include_figure_labels(child, available, labels, field)


def keyed_label(question_id: str, suffix: str, text: str, labels: dict[str, str]) -> str:
    key = f"{question_id.replace('-', '.')}.figure.{suffix}"
    labels[key] = text
    return key


def map_figure(
    question_id: str, title: str, scenario: str, answer: str, labels: dict[str, str]
) -> dict[str, Any]:
    turkiye = keyed_label(question_id, "turkiye", "Türkiye", labels)
    alt = keyed_label(
        question_id,
        "alt",
        "Soruda incelenen yerlerin göreli konumlarını etiketli işaretçilerle gösteren sade harita; seçenek numarası işaretlenmemiştir.",
        labels,
    )
    world = any(word in title.casefold() for word in ("dünya", "kıta", "okyanus", "türk dünyası"))
    if world and any(word in f"{scenario} {answer}".casefold() for word in ("asya", "avrupa", "okyanus")):
        avrupa = keyed_label(question_id, "europe", "Avrupa", labels)
        asya = keyed_label(question_id, "asia", "Asya", labels)
        markers = [
            {"x": 43, "y": 34, "labelKey": avrupa},
            {"x": 53, "y": 41, "labelKey": turkiye},
            {"x": 68, "y": 36, "labelKey": asya},
        ]
    else:
        names = [clean(item) for item in answer.split(",") if clean(item)][:4]
        if len(names) >= 2:
            positions = ((72, 28), (45, 30), (58, 47), (29, 61))
            markers = [
                {"x": positions[index][0], "y": positions[index][1],
                 "labelKey": keyed_label(question_id, f"place{index + 1}", name, labels)}
                for index, name in enumerate(names)
            ]
        else:
            region = keyed_label(question_id, "region", "İncelenen bölge", labels)
            markers = [
                {"x": 55, "y": 42, "labelKey": turkiye},
                {"x": 68 if world else 38, "y": 34 if world else 58, "labelKey": region},
            ]
    return {
        "kind": "map",
        "base": "world" if world else "turkiye",
        "markers": markers,
        "altTextKey": alt,
    }


def diagram_figure(question_id: str, labels: dict[str, str], answer: str = "") -> dict[str, Any]:
    relation = [clean(part) for part in re.split(r"\s*(?:-|→|=>)\s*", answer, maxsplit=1)]
    if len(relation) == 2 and all(relation):
        names = (relation[0], relation[1])
    else:
        names = ("Girdi", "İşlem", "Koşul kontrolü", "Çıktı")
    node_keys = [keyed_label(question_id, f"node{index + 1}", name, labels) for index, name in enumerate(names)]
    alt = keyed_label(
        question_id,
        "alt",
        "Kavramlar veya işlem basamakları arasındaki yönlü ilişkiyi gösteren güvenli süreç diyagramı; seçenek numarası belirtilmemiştir.",
        labels,
    )
    return {
        "kind": "diagram",
        "nodes": [
            {"id": f"n{index + 1}", "labelKey": node_keys[index], "shape": "diamond" if index == 2 else "rect",
             "x": 12 + index * (76 // max(1, len(names) - 1)), "y": 50}
            for index in range(len(names))
        ],
        "edges": [
            {"from": f"n{index + 1}", "to": f"n{index + 2}", "directed": True}
            for index in range(len(names) - 1)
        ],
        "direction": "horizontal",
        "altTextKey": alt,
    }


def experiment_figure(question_id: str, title: str, scenario: str, labels: dict[str, str]) -> dict[str, Any]:
    lowered = f"{title} {scenario}".casefold()
    if any(word in lowered for word in ("elektrik", "ampul", "direnç", "reosta", "iletken")):
        apparatus_types = ("battery", "switch", "resistor", "lamp")
        kind = "wire"
        description = "Pil, anahtar, direnç ve lambanın iletken tellerle seri bağlandığı deney düzeneği"
    elif any(word in lowered for word in ("ışık", "ayna", "yansıma", "soğur")):
        apparatus_types = ("lightSource", "mirror", "screen")
        kind = "beam"
        description = "Işık kaynağı, ayna ve ekrandan oluşan ışık deney düzeneği"
    elif any(word in lowered for word in ("bitki", "tohum", "çimlen", "çiçek", "tozlaş")):
        apparatus_types = ("plant", "plant")
        kind = "support"
        description = "Aynı tür iki bitkinin farklı deney koşullarında karşılaştırıldığı kontrollü düzenek"
    else:
        apparatus_types = ("beaker", "thermometer", "burner")
        kind = "support"
        description = "Beher, termometre ve ısı kaynağından oluşan ölçüm düzeneği"
    apparatus = []
    for index, apparatus_type in enumerate(apparatus_types):
        if apparatus_type == "plant" and "tül" in lowered:
            label_text = "Tülle kapatılan çiçek" if index == 0 else "Açık bırakılan çiçek"
        elif apparatus_type == "plant":
            label_text = f"Bitki {index + 1}"
        else:
            label_text = apparatus_type
        label = keyed_label(question_id, f"apparatus{index + 1}", label_text, labels)
        apparatus.append({
            "id": f"a{index + 1}", "type": apparatus_type,
            "x": 18 + index * (64 // max(1, len(apparatus_types) - 1)), "y": 55,
            "labelKey": label,
        })
    alt = keyed_label(
        question_id,
        "alt",
        f"{description}; ölçüm sonucu ve doğru seçenek görselde verilmemiştir.",
        labels,
    )
    return {
        "kind": "experiment",
        "apparatus": apparatus,
        "connections": ([] if apparatus_types == ("plant", "plant") else [
            {"from": apparatus[index]["id"], "to": apparatus[index + 1]["id"], "kind": kind}
            for index in range(len(apparatus) - 1)
        ]),
        "altTextKey": alt,
    }


def chart_figure(
    question_id: str,
    scenario: str,
    labels: dict[str, str],
    candidates: list[str] | None = None,
    answer: str = "",
) -> dict[str, Any] | None:
    numbers = [float(value.replace(",", ".")) for value in re.findall(r"(?<![\w.])\d+(?:[.,]\d+)?", scenario)]
    lowered = scenario.casefold()
    if "sürat-zaman" in lowered or "hız-zaman" in lowered:
        interval = re.search(r"(\d+)\s*[-–]\s*(\d+)\s*saniye", answer, re.IGNORECASE)
        start, end = (int(interval.group(1)), int(interval.group(2))) if interval else (2, 4)
        category_names = ["0 s", f"{start} s", f"{end} s", f"{end + 2} s"]
        values = [5.0, 10.0, 10.0, 15.0]
    elif "kıta" in lowered and candidates:
        known = {"asya": 44.6, "afrika": 30.4, "kuzey amerika": 24.7, "güney amerika": 17.8,
                 "antarktika": 14.0, "avrupa": 10.2, "avustralya": 8.6, "türkiye": 0.78}
        category_names = [clean(item) for item in candidates[:4]]
        values = [known.get(normalized(item), 5.0) for item in category_names]
    else:
        values = numbers[:4]
        category_names = [f"Veri {index + 1}" for index in range(len(values))]
    if len(values) == 1 and "%" in scenario:
        values.append(max(0.0, 100.0 - values[0]))
    if len(values) < 2 and candidates and answer in candidates:
        category_names = [clean(item) for item in candidates[:4]]
        values = [70.0 - index * 10.0 for index in range(len(category_names))]
        values[category_names.index(answer)] = 100.0
    if len(values) < 2:
        return None
    category_keys = [keyed_label(question_id, f"category{index + 1}", name, labels) for index, name in enumerate(category_names)]
    alt = keyed_label(
        question_id,
        "alt",
        "Soruda verilen sayısal kayıtları sütunlar hâlinde karşılaştıran grafik; doğru seçenek veya sonuç vurgulanmamıştır.",
        labels,
    )
    return {
        "kind": "chart", "style": "bar",
        "categoryKeys": category_keys, "values": values,
        "altTextKey": alt,
    }


def choose_figure(
    question_id: str,
    subject: str,
    title: str,
    scenario: str,
    note: dict[str, Any],
    available_labels: dict[str, Any],
    labels: dict[str, str],
    candidates: list[str],
    answer: str,
) -> dict[str, Any]:
    lowered = f"{title} {scenario}".casefold()
    if any(word in scenario.casefold() for word in ("grafik", "chart", "yüzde", "istatistik", "olasılık")):
        chart = chart_figure(question_id, scenario, labels, candidates, answer)
        if chart is not None:
            return chart
    if any(word in scenario.casefold() for word in ("akış şeması", "diyagram", "şema")):
        return diagram_figure(question_id, labels, answer)
    if subject == "Sosyal Bilgiler" and "harita" in scenario.casefold():
        return map_figure(question_id, title, scenario, answer, labels)
    if "tablo" in scenario.casefold():
        return figure_for(question_id, scenario, title, labels)
    if subject == "Sosyal Bilgiler" and any(word in lowered for word in ("harita", "konum", "kıta", "okyanus", "anadolu", "türk dünyası")):
        return map_figure(question_id, title, scenario, answer, labels)
    if subject == "Fen Bilimleri" and any(word in lowered for word in (
        "deney", "çimlen", "erime", "donma", "kaynama", "yoğunluk", "iletken",
        "elektrik", "ampul", "direnç", "reosta", "yansıma", "soğur", "ışın",
    )):
        return experiment_figure(question_id, title, scenario, labels)
    if subject == "Bilişim Teknolojileri ve Yazılım" and any(word in lowered for word in ("algoritma", "blok", "programlama", "döngü", "koşul")):
        return diagram_figure(question_id, labels, answer)
    if any(word in lowered for word in ("grafik", "chart", "yüzde", "istatistik", "olasılık")):
        chart = chart_figure(question_id, scenario, labels, candidates, answer)
        if chart is not None:
            return chart
    source_figure = note.get("figure")
    if isinstance(source_figure, dict):
        cloned = copy.deepcopy(source_figure)
        include_figure_labels(cloned, available_labels, labels)
        replacement = keyed_label(
            question_id,
            "alt",
            f"{str(cloned.get('kind') or 'Görsel').capitalize()} türündeki temsil, soruda karşılaştırılan "
            "kayıt, konum veya ilişkileri yapısal olarak gösterir; doğru seçenek ayrıca işaretlenmemiştir.",
            labels,
        )
        cloned["altTextKey"] = replacement
        return cloned
    return figure_for(question_id, scenario, title, labels)


def question_record(
    *,
    note: dict[str, Any],
    subject: str,
    number: int,
    local_index: int,
    mode: str,
    level: int,
    correct_index: int,
    available_labels: dict[str, Any],
    labels: dict[str, str],
) -> dict[str, Any]:
    sections = note.get("lessonSections") or {}
    examples = [str(value) for value in sections.get("workedExamples") or []]
    if len(examples) < 2:
        raise ValueError(f"{note.get('id')}: en az iki çözümlü örnek yok")
    example_index = local_index % len(examples)
    parsed_examples = [parse_example(value) for value in examples]
    scenario, answer, reason = parsed_examples[example_index]
    reason = scrub_option_letter_claims(reason)
    title = clean(str(note.get("title") or note.get("topic") or note.get("objective")))
    errors = mistake_candidates(str(sections.get("commonMistakes") or ""))
    grouped = errors[example_index * 3: example_index * 3 + 3]
    sibling_answers = [item[1] for index, item in enumerate(parsed_examples) if index != example_index]
    pool = [*grouped, *sibling_answers, *errors, *fallback_wrongs(answer, title)]
    wrongs: list[str] = []
    for candidate in pool:
        if normalized(candidate) == normalized(answer):
            continue
        if not compatible_distractor(answer, candidate):
            continue
        if normalized(candidate) in {normalized(old) for old in wrongs}:
            continue
        wrongs.append(candidate)
        if len(wrongs) == 3:
            break
    if len(wrongs) != 3:
        raise ValueError(f"{note.get('id')}: üç benzersiz çeldirici üretilemedi")

    question_id = f"tr-g06-bank-q{number:04d}"
    variant = local_index // len(examples)
    candidates = [answer, *wrongs]
    semantic_options = candidates
    correct_option = semantic_options[0]
    wrong_options = semantic_options[1:]
    choices = list(wrong_options)
    choices.insert(correct_index, correct_option)

    context = CONTEXTS[(number + local_index * 5) % len(CONTEXTS)]
    task = TASKS[mode][variant % len(TASKS[mode])]
    checkpoint = CHECKPOINTS[local_index % len(CHECKPOINTS)]
    reasoning_path = AUDIT_TRAILS[local_index % len(AUDIT_TRAILS)]
    variant_frame = VARIANT_FRAMES[variant % len(VARIANT_FRAMES)]
    comparison_frame = VARIANT_FRAMES[(variant + 3) % len(VARIANT_FRAMES)]
    explicit_visual = re.search(
        r"(?i)\b(?:grafik|harita|şekil|görsel|diyagram|şema|tablo|deney|düzenek|devre|chart|map|diagram|picture|visual|image|graph|table|figure)\w*\b",
        scenario,
    ) is not None
    use_figure = local_index % 3 == 0 or explicit_visual
    if not use_figure:
        task = (
            task.replace("Tablodaki durum ve ölçüt", "Verilen durum ve ölçüt")
            .replace("Kanıt tablosundaki iki kayıt", "Verilen iki kanıt")
            .replace("Tablodaki kanıtı", "Verilen kanıtı")
        )
    topic_focus = safe_lower_title(title)
    if use_figure:
        figure = (
            choose_figure(
                question_id, subject, title, scenario, note, available_labels, labels,
                candidates, answer,
            )
            if explicit_visual
            else figure_for(question_id, scenario, title, labels)
        )
        kind = str(figure.get("kind"))
        if kind != "table":
            task = (
                task.replace("Tablodaki durum ve ölçüt", "Görseldeki durum ve ölçüt")
                .replace("Kanıt tablosundaki iki kayıt", "Görseldeki iki kanıt")
                .replace("Tablodaki kanıtı", "Görseldeki kanıtı")
            )
        reference = {
            "map": "harita", "experiment": "deney düzeneği", "diagram": "diyagram",
            "chart": "grafik", "table": "tablo", "flow": "akış şeması",
            "circuit": "devre şeması", "coordinate": "koordinat çizimi",
            "shape": "şekil", "angle": "açı çizimi", "grid": "kareli model",
            "numberline": "sayı doğrusu", "fraction": "kesir modeli",
        }.get(kind, "görsel")
        if kind == "table" and figure.get("altTextKey", "").startswith(question_id.replace("-", ".")):
            situation = "Çözülecek durum tablonun içerik satırında verilmiştir."
        else:
            display_scenario = scenario
            if kind != "table":
                display_scenario = re.sub(
                    r"(?i)\s*Yukarıdaki tablo[^.]*\.?", "", display_scenario,
                )
            situation = f"İncelenen durum şöyledir: {clean(display_scenario)}"
        stem = (
            f"{context} Aşağıda sunulan {reference} çözüm için gerekli kanıtı taşımaktadır. {situation} "
            f"{task} Karar verilirken görseldeki bilgi ile {topic_focus} konusu birlikte kullanılmalıdır. "
            f"Çözüm özellikle {checkpoint} ölçütüyle gerekçelendirilmelidir. {variant_frame} "
            f"{comparison_frame} {reasoning_path}"
        )
        visual_need = {
            "level": "required",
            "role": "evidence",
            "rationale": f"{kind} temsili, soruda karşılaştırılan durumun yapı veya veri ilişkisini taşımaktadır.",
            "acceptableKinds": [kind],
            "evidenceDimensions": ["durum", "ilişki", "ölçüt"],
        }
    else:
        figure = None
        if mode == "error-analysis":
            mistaken = wrongs[(variant + local_index) % len(wrongs)]
            if subject == "Matematik" and re.search(r"[×÷=]", mistaken):
                mistaken = "ara işlemde kullanılan sayı ve işlemleri yanlış eşleştiren bir sonuç"
            stem = (
                f"{context} İncelenen durum şöyledir: {scenario} Bir öğrenci bu durum için “{mistaken}” "
                f"yorumunu yapmıştır. {task} Düzeltme {checkpoint} ölçütüyle gerekçelendirilmelidir. "
                f"{variant_frame} {comparison_frame} {reasoning_path}"
            )
        else:
            stem = (
                f"{context} İncelenen durum şöyledir: {scenario} {task} "
                f"Çözüm özellikle {checkpoint} ölçütüyle gerekçelendirilmelidir. {variant_frame} "
                f"{comparison_frame} {reasoning_path}"
            )
        visual_need = {
            "level": "none",
            "role": "none",
            "rationale": "Durum, ölçüt ve karar için gerekli bütün bilgiler soru metninde eksiksizdir.",
            "acceptableKinds": [],
            "evidenceDimensions": [],
        }

    why = []
    misconception_names = (
        "Kavramı ters yorumlama", "Bağlam koşulunu atlama", "Kanıtı aşırı genelleme"
    )
    wrong_cursor = 0
    for index, choice in enumerate(choices):
        if index == correct_index:
            why.append(
                f"Doğru ilişki: {reason} Bu seçenek durum, kazanım ölçütü ve sonucu tutarlı biçimde ilişkilendirir."
            )
        else:
            why.append(
                f"{misconception_names[wrong_cursor]}: ‘{choice}’ ifadesi verilen koşullardan en az birini "
                "dışarıda bırakır veya yanlış bir kavram ilişkisi kurar."
            )
            wrong_cursor += 1

    objective = str(note.get("objective") or note.get("objectiveId"))
    note_id = str(note.get("id"))
    return {
        "type": "question",
        "id": question_id,
        "questionId": question_id,
        "questionNumber": number,
        "subject": subject,
        "grade": 6,
        "unitKey": note.get("unitKey"),
        "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"),
        "topic": note.get("topic") or title,
        "title": f"{title} — {mode}",
        "objective": objective,
        "objectiveId": objective,
        "noteId": note_id,
        "noteKey": note_id,
        "question": stem,
        "choices": choices,
        "correct": correct_index,
        "correctIndex": correct_index,
        "correctOption": choices[correct_index],
        "distractorWhy": why,
        "explanation": f"Doğru sonuç: ‘{answer}’. {reason} Diğer seçenekler koşullardan en az birini karşılamaz.",
        "level": level,
        "difficultyReason": (
            f"Düzey {level}; {title} bilgisini {mode} türünde yeni bir karar bağlamına aktarmayı, "
            "dört gerekçeli görüşü karşılaştırmayı ve kanıtla sonuç arasındaki ilişkiyi denetlemeyi gerektirir."
        ),
        "questionType": mode,
        "familyId": f"tr-g06-bank-family-{number:04d}",
        "objectiveSource": note.get("objectiveSource"),
        "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": list(note.get("sourceRefs") or []),
        "visualNeed": visual_need,
        "figure": figure,
        "hintsCount": 0,
        "hintsForbidden": True,
    }


def main() -> int:
    subject_data: dict[str, tuple[list[dict[str, Any]], dict[str, Any]]] = {}
    for path in sorted(GRADE_ROOT.glob("*/*-tum.jsonl")):
        if path.parent.name == "soru-bankasi":
            continue
        pack, notes = read_pack_and_notes(path)
        subject = str(pack.get("subject"))
        if subject not in SUBJECT_QUOTAS:
            raise ValueError(f"Beklenmeyen ders: {subject}")
        subject_data[subject] = (notes, dict(pack.get("labels") or {}))
    if set(subject_data) != set(SUBJECT_QUOTAS):
        raise ValueError("6. sınıf ders kapsamı eksik")

    labels: dict[str, str] = {}
    questions: list[dict[str, Any]] = []
    number = 0
    mode_schedules = [
        batch_schedule(batch, [
            ("comprehension", 25), ("application", 35),
            ("analysis", 25), ("error-analysis", 15),
        ], "grade6-mode")
        for batch in range(20)
    ]
    level_schedules = [
        batch_schedule(batch, [(1, 20), (2, 25), (3, 30), (4, 20), (5, 5)], "grade6-level")
        for batch in range(20)
    ]

    for subject in SUBJECT_QUOTAS:
        notes, available_labels = subject_data[subject]
        allocation = allocate(SUBJECT_QUOTAS[subject], notes)
        for note in notes:
            for local_index in range(allocation[str(note["id"])]):
                batch = number // 100
                offset = number % 100
                questions.append(question_record(
                    note=note,
                    subject=subject,
                    number=number + 1,
                    local_index=local_index,
                    mode=mode_schedules[batch][offset],
                    level=level_schedules[batch][offset],
                    correct_index=offset % 4,
                    available_labels=available_labels,
                    labels=labels,
                ))
                number += 1

    if number != 2000:
        raise AssertionError(f"Soru sayısı 2000 değil: {number}")
    AUTHORING_ROOT.mkdir(parents=True, exist_ok=True)
    QUESTION_PATH.write_text(
        "\n".join(compact(row) for row in questions) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    LABEL_PATH.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(compact({
        "grade": 6,
        "questions": len(questions),
        "labels": len(labels),
        "subjects": SUBJECT_QUOTAS,
        "sourceQuestionRecordsRead": 0,
        "status": "PENDING_REVIEW",
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
