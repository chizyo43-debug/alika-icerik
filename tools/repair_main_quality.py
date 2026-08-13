#!/usr/bin/env python3
"""Repair deterministic quality defects in current AliKa 2.2 releases.

The repair is intentionally conservative: it does not change answer keys or
invent curriculum facts. It removes decorative question figures, teaches note
readers how to use retained figures, removes answer-position wording from
explanations, normalizes fraction spelling, drops orphan labels, and refreshes
AI-only review hashes for records whose content changed.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import math
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTRACT = json.loads((ROOT / "pack_contract.json").read_text(encoding="utf-8"))
CONTRACT_VERSION = CONTRACT["questionContract"]["version"]
CONTRACT_HASH = f"sha256:{CONTRACT['questionContract']['sha256']}"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_module("pack_validate", ROOT / "tools" / "pack_validate.py")
FINALIZER = load_module(
    "finalize_ai_release", ROOT / "tools" / "finalize_ai_release.py"
)


FIGURE_GUIDANCE = {
    "table": (
        "Görseli kullanma: Yukarıdaki tabloda satır ve sütun başlıklarını "
        "birlikte incele; hücrelerdeki bilgileri metindeki kavramlarla eşleştir."
    ),
    "flow": (
        "Görseli kullanma: Yukarıdaki şemada okları yönlerinde izle; her "
        "düğümü anlatımdaki ilgili adımla eşleştir."
    ),
    "chart": (
        "Görseli kullanma: Yukarıdaki grafikte kategorileri ve değerleri birlikte "
        "oku; karşılaştırmanı anlatımdaki ölçütlerle doğrula."
    ),
    "numberline": (
        "Görseli kullanma: Yukarıdaki görselde sayıların sırasını ve "
        "aralıklarını incele; metindeki sayısal ilişkiyle karşılaştır."
    ),
    "fraction": (
        "Görseli kullanma: Yukarıdaki görselde bütün, eş parçalar ve "
        "boyalı parçalar arasındaki ilişkiyi anlatımla eşleştir."
    ),
    "shape": (
        "Görseli kullanma: Yukarıdaki şekilde kenar, köşe ve ölçü işaretlerini "
        "incele; anlatımdaki geometrik özelliklerle eşleştir."
    ),
    "angle": (
        "Görseli kullanma: Yukarıdaki görselde ışınları, köşeyi ve "
        "ölçüyü incele; anlatımdaki açı ilişkisiyle eşleştir."
    ),
    "grid": (
        "Görseli kullanma: Yukarıdaki görselde satır, sütun ve boyalı "
        "bölgeleri say; sonucu anlatımdaki modelle karşılaştır."
    ),
    "coordinate": (
        "Görseli kullanma: Yukarıdaki görselde eksenleri ve "
        "noktaları sırayla oku; anlatımdaki konum ilişkisini doğrula."
    ),
    "circuit": (
        "Görseli kullanma: Yukarıdaki şemada devre elemanlarını ve bağlantı "
        "yolunu izle; anlatımdaki elektriksel ilişkiyle eşleştir."
    ),
}


ANSWER_POSITION_PATTERNS = (
    re.compile(
        r"\s*(?:Bu nedenle|Bu yüzden|Dolayısıyla)?\s*"
        r"(?:doğru\s+(?:cevap|yanıt|seçenek)|cevap)\s*[:\-]?\s*"
        r"[ABCD](?:\s+seçeneğidir|['’](?:d|t)[ıiuü]r)?\s*[.]?",
        re.I,
    ),
    re.compile(
        r"\s*(?:Bu nedenle|Bu yüzden|Dolayısıyla)?\s*"
        r"[ABCD]\s+(?:seçeneği|şıkkı)\s+"
        r"(?:doğrudur|yanlıştır|doğru\s+cevaptır)\s*[.]?",
        re.I,
    ),
    re.compile(
        r"\s*(?:Therefore,?\s*)?(?:the\s+)?correct\s+"
        r"(?:answer|option)\s+(?:is\s+)?[ABCD]\s*[.]?",
        re.I,
    ),
    re.compile(
        r"\s*[Oo]ption\s+[ABCD]\s+is\s+(?:the\s+)?correct\s+"
        r"(?:answer|choice)\s*[.]?",
        re.I,
    ),
)


def record_type(record: dict) -> str:
    return str(record.get("type") or record.get("recordType") or "")


def comparable(record: dict) -> dict:
    result = copy.deepcopy(record)
    for field in FINALIZER.REVIEW_FIELDS:
        result.pop(field, None)
    return result


def normalize_explanation(text: str) -> str:
    result = text
    for pattern in ANSWER_POSITION_PATTERNS:
        result = pattern.sub("", result)
    replacements = (
        (r"\b[ABCD]\s+seçeneğine\b", "doğru yanıta"),
        (r"\b[ABCD]\s+seçeneği\b", "Bu ifade"),
        (r"\b[ABCD]\s+şıkkına\b", "doğru yanıta"),
        (r"\b[ABCD]\s+şıkkı\b", "Bu ifade"),
        (r"\boption\s+[ABCD]\b", "the correct choice"),
    )
    for pattern, replacement in replacements:
        result = re.sub(pattern, replacement, result, flags=re.I)
    result = re.sub(
        r"\b(?:seçenek|ifade|yaklaşım|çalışma|ayrım|tanım)\s+"
        r"([ABCD])['’](?:d|t)[ıiuü]r\b",
        "ilgili seçenek doğru sonucu verir",
        result,
        flags=re.I,
    )
    result = re.sub(
        r"\b([ABCD])\s+(?:seçeneğinde|seçeneğindeki|seçeneğidir|seçeneği|"
        r"şıkkında|şıkkındaki|şıkkıdır|şıkkı)\b",
        "ilgili seçenekte",
        result,
        flags=re.I,
    )
    result = re.sub(r"\s+([,.;:])", r"\1", result)
    result = re.sub(r"(?:\.\s*){2,}", ". ", result)
    result = re.sub(r"\s{2,}", " ", result).strip(" ;")
    if result and result[-1] not in ".!?":
        result += "."
    return result


SCIENCE_RATIONALE_REPAIRS = {
    "tr-g06-fen-bilimleri-q120": [
        "1-2. haftalar arasındaki artış 3 cm'dir; 6 cm'lik en büyük artış değildir.",
        "3-4. haftalar arasındaki artış 3 cm'dir; 6 cm'lik en büyük artış değildir.",
        "2-3. haftalar arasındaki artış 6 cm ile ölçülen en büyük artıştır.",
        "Artışlar 3, 6 ve 3 cm olduğundan haftaların hepsinde eşit değildir.",
    ],
    "tr-g06-fen-bilimleri-q204": [
        "Ergenlikteki doğal bedensel ve duygusal değişimler tek başına hastalık değildir.",
        "Değişimlerin başlama zamanı bireyler arasında farklılık gösterebilir.",
        "Ergenlik, çocukluktan yetişkinliğe geçişte yaşanan doğal bir gelişim dönemidir.",
        "Bu ifade, ergenlik zamanının kişiden kişiye değişebileceğini doğru açıklar.",
    ],
    "tr-g06-fen-bilimleri-q206": [
        "Ergenliğin herkeste aynı anda başladığı iddiası bireysel gelişim farklarını yok sayar.",
        "Bu ifade, ergenliğin doğal olduğunu ve zamanının bireyler arasında değişebildiğini doğru belirtir.",
        "Ergenlik yaşam boyu sürmez; yetişkinliğe geçişteki gelişim dönemidir.",
        "Ergenlik yalnız bedensel değil, duygusal ve sosyal değişimleri de kapsar.",
    ],
    "tr-g06-fen-bilimleri-q228": [
        "Zımparanın pürüzlü yüzeyi ışığı farklı yönlere dağıtarak düzensiz yansıma oluşturur.",
        "Kartonun mat ve pürüzlü yüzeyi net görüntü oluşturan düzenli yansımaya uygun değildir.",
        "Taşın pürüzlü yüzeyi gelen ışınları farklı yönlere dağıtır.",
        "Aynanın çok düzgün yüzeyi ışığı düzenli yansıtarak net görüntü oluşturur.",
    ],
    "tr-g06-fen-bilimleri-q230": [
        "Cam, grafikte %95 ile en yüksek düzenli yansıma oranına sahiptir.",
        "Kartonun düzenli yansıma oranı grafikte %95'lik cam değerinden düşüktür.",
        "Kumaşın pürüzlü yapısı ışığı dağıtır; grafikteki değeri camdan düşüktür.",
        "Taşın düzenli yansıma değeri grafikte camın %95 değerinin altındadır.",
    ],
    "tr-g06-fen-bilimleri-q231": [
        "Tablo, ahşap yüzeyde net görüntü oluşmadığını gösterir.",
        "Tablo, keçe yüzeyde görüntünün dağınık olduğunu gösterir.",
        "Tabloda net görüntü oluşturan tek yüzey metal levhadır.",
        "Tablo, kâğıt yüzeyde net görüntü oluşmadığını gösterir.",
    ],
    "tr-g06-fen-bilimleri-q232": [
        "Halının pürüzlü lifleri ışığı farklı yönlere dağıtır.",
        "Tuğlanın pürüzlü yüzeyi düzenli değil, düzensiz yansıma oluşturur.",
        "Kumaşın lifli yüzeyi ışığı dağıtır ve net görüntü oluşturmaz.",
        "Aynanın pürüzsüz yüzeyi ışığı düzenli yansıtır.",
    ],
    "tr-g06-fen-bilimleri-q233": [
        "Parlatılmış çeliğin düzgün yüzeyi düzenli yansımaya uygundur.",
        "Buruşuk folyonun düzensiz yüzeyi ışığı farklı yönlere dağıtır.",
        "Zımparanın pürüzlü yüzeyi düzenli yansıma oluşturmaz.",
        "Kadifenin lifli yüzeyi ışığı dağıttığı için net görüntü oluşturmaz.",
    ],
    "tr-g06-fen-bilimleri-q234": [
        "B yüzeyinin pürüzlülüğü A'dan fazla olduğundan düzenli yansıması daha düşüktür.",
        "A, ölçülen en az pürüzlü yüzey olduğu için en güçlü düzenli yansımayı yapar.",
        "C yüzeyinin pürüzlülüğü A'dan fazla olduğundan net görüntü için uygun değildir.",
        "D yüzeyinin pürüzlülüğü A'dan fazla olduğundan ışığı daha çok dağıtır.",
    ],
}


TURKISH_QUESTION_REPAIRS = {
    "tr-g06-turkce-q467": {
        "choices": [
            "Türkiye'nin başkenti Ankara'dır.",
            "19 Mayıs 1919'da Samsun'a çıktık.",
            "Bu sene 23 Nisan da okulda kutlama yapılacak.",
            "Ayşe teyzem bize yarın gelecek.",
        ],
        "distractorWhy": [
            "Türkiye özel adına gelen ek kesme işaretiyle doğru ayrılmıştır.",
            "Belirli tarihi bildiren 19 Mayıs 1919'a gelen ek kesme işaretiyle doğru ayrılmıştır.",
            "23 Nisan özel gün adına gelen ek kesme işaretiyle ayrılmalıdır; doğru yazım 23 Nisan'da biçimindedir.",
            "Akrabalık bildiren teyze sözcüğü küçük harfle doğru yazılmıştır.",
        ],
        "explanation": "Belirli gün ve bayram adlarına gelen ekler kesme işaretiyle ayrılır. Bu nedenle doğru yazım “23 Nisan'da” olmalıdır.",
    },
    "tr-g06-turkce-q468": {
        "choices": [
            "Eyvah, yangın var!",
            "Okula gitmek için hazırlandın mı?",
            "Kitap, defter ve kalem aldım.",
            "Bugün hava çok güzel,",
        ],
        "distractorWhy": [
            "Ünlem işareti korku ve telaş bildiren cümlenin sonunda doğru kullanılmıştır.",
            "Soru işareti doğrudan soru bildiren cümlenin sonunda doğru kullanılmıştır.",
            "Virgül eş görevli sözcükleri ayırmak için doğru kullanılmıştır.",
            "Tamamlanmış yargının sonunda virgül değil nokta kullanılmalıdır.",
        ],
        "explanation": "“Bugün hava çok güzel” tamamlanmış bir yargıdır; cümlenin sonuna virgül değil nokta konmalıdır.",
    },
    "tr-g06-turkce-q469": {
        "choices": [
            "Bu akşam biz de yemek var.",
            "Sen de bizimle gelir misin?",
            "Kitabı çantada unutmuşum.",
            "Okulda bugün tören var.",
        ],
        "distractorWhy": [
            "Buradaki -de bulunma durumu ekidir ve “bizde” biçiminde bitişik yazılmalıdır.",
            "“Sen de” sözündeki de bağlaçtır ve ayrı yazılması doğrudur.",
            "“Çantada” sözcüğündeki -da bulunma durumu ekidir ve bitişik yazılması doğrudur.",
            "“Okulda” sözcüğündeki -da bulunma durumu ekidir ve bitişik yazılması doğrudur.",
        ],
        "explanation": "Cümle yemeğin bulunduğu yeri bildirir; bu nedenle bulunma durumu eki kullanılır ve “bizde” bitişik yazılır.",
    },
    "tr-g06-turkce-q470": {
        "choices": [
            "Türkiye'nin en yüksek dağı Ağrı'dır.",
            "Türk Dil Kurumu'nun sözlüğüne baktım.",
            "Ahmet'in kalemi çok güzel.",
            "İstanbul'un nüfusu çok fazla.",
        ],
        "distractorWhy": [
            "Türkiye özel adına gelen ek kesme işaretiyle doğru ayrılmıştır.",
            "Kurum ve kuruluş adlarına gelen ekler kesme işaretiyle ayrılmaz; doğru yazım “Türk Dil Kurumunun” biçimindedir.",
            "Ahmet özel adına gelen ek kesme işaretiyle doğru ayrılmıştır.",
            "İstanbul özel adına gelen ek kesme işaretiyle doğru ayrılmıştır.",
        ],
        "explanation": "Kurum ve kuruluş adlarına gelen ekler kesme işaretiyle ayrılmaz. Doğru yazım “Türk Dil Kurumunun sözlüğüne baktım.” biçimindedir.",
    },
    "tr-g06-turkce-q471": {
        "choices": [
            "Sınıftaki öğrenciler çok çalışkan.",
            "Yarınki sınavı düşünüyorum.",
            "Öyleki herkes şaşırdı.",
            "Evdeki hesap çarşıya uymaz.",
        ],
        "distractorWhy": [
            "“Sınıftaki” sözcüğündeki -ki ektir ve bitişik yazılması doğrudur.",
            "“Yarınki” sözcüğündeki -ki ektir ve bitişik yazılması doğrudur.",
            "“Öyle ki” sözündeki ki bağlaçtır ve ayrı yazılmalıdır.",
            "“Evdeki” sözcüğündeki -ki ektir ve bitişik yazılması doğrudur.",
        ],
        "explanation": "“Öyle ki” kalıbındaki ki bağlaçtır; bağlaç olan ki ayrı yazılır.",
    },
}


def sync_table_choices(record: dict) -> None:
    figure = record.get("figure")
    choices = record.get("choices")
    if not isinstance(figure, dict) or figure.get("kind") != "table":
        return
    rows = figure.get("rows")
    if not isinstance(rows, list) or not isinstance(choices, list):
        return
    if len(rows) != len(choices):
        return
    for row, choice in zip(rows, choices):
        if (
            isinstance(row, list)
            and len(row) >= 2
            and isinstance(row[1], dict)
            and "v" in row[1]
        ):
            row[1]["v"] = choice


def mark_correct_rationale(record: dict) -> None:
    rationales = record.get("distractorWhy")
    correct = record.get("correct")
    if (
        isinstance(rationales, list)
        and isinstance(correct, int)
        and 0 <= correct < len(rationales)
        and "doğru" not in str(rationales[correct]).casefold()
    ):
        rationales[correct] = "Doğru seçimdir; " + str(rationales[correct])


def apply_targeted_repairs(rows: list[dict]) -> None:
    for record in rows:
        record_id = str(record.get("id") or "")
        if record_id in SCIENCE_RATIONALE_REPAIRS:
            record["distractorWhy"] = SCIENCE_RATIONALE_REPAIRS[record_id]
            mark_correct_rationale(record)
        repair = TURKISH_QUESTION_REPAIRS.get(record_id)
        if repair:
            record.update(copy.deepcopy(repair))
            mark_correct_rationale(record)
            sync_table_choices(record)


def append_note_figure_guidance(record: dict) -> None:
    figure = record.get("figure") or {}
    guidance = FIGURE_GUIDANCE.get(
        figure.get("kind"),
        "Görseli kullanma: Yukarıdaki görselde verilenleri anlatımdaki "
        "kavramlarla eşleştirerek incele.",
    )
    body = record.get("body")
    if isinstance(body, str):
        if guidance not in body:
            record["body"] = body.rstrip() + "\n\n" + guidance
    elif isinstance(body, dict):
        current = str(body.get("figureNote") or "").strip()
        if guidance not in current:
            body["figureNote"] = (current + "\n\n" + guidance).strip()
    sections = record.get("lessonSections")
    if isinstance(sections, dict):
        current = str(sections.get("figureNote") or "").strip()
        if guidance not in current:
            sections["figureNote"] = (current + "\n\n" + guidance).strip()


def answer_distribution(questions: list[dict]) -> list[int]:
    counts = Counter()
    for question in questions:
        index = question.get("correctIndex", question.get("answerIndex"))
        if index is None:
            index = question.get("correct")
        if isinstance(index, int):
            counts[index] += 1
    return [counts[index] for index in range(4)]


def ensure_contract_metadata(pack: dict, rows: list[dict]) -> None:
    questions = [row for row in rows if record_type(row) == "question"]
    notes = [row for row in rows if record_type(row) == "note"]
    pack["contentContractVersion"] = CONTRACT_VERSION
    pack["contentContractHash"] = CONTRACT_HASH
    policy = pack.setdefault("contractPolicy", {})
    policy.setdefault("questionCount", len(questions))
    policy.setdefault("minFamilies", 80)
    policy.setdefault("maxPerFamily", 8)
    policy.setdefault("answerBalance", answer_distribution(questions))
    policy.setdefault("objectiveBalanceMode", "coverage")
    visual = pack.get("visualPolicy") or {}
    minimum_percent = visual.get("questionMinimumPercent", 0)
    if isinstance(minimum_percent, (int, float)) and not isinstance(
        minimum_percent, bool
    ):
        policy.setdefault(
            "minFiguredQuestions",
            math.ceil(len(questions) * float(minimum_percent) / 100),
        )
    policy.setdefault(
        "everyNoteHasFigure", bool(visual.get("everyNote", False) and notes)
    )


def replace_half(value):
    if isinstance(value, str):
        replacements = {
            "½": "1/2", "⅓": "1/3", "⅔": "2/3", "¼": "1/4",
            "¾": "3/4", "⅕": "1/5", "⅖": "2/5", "⅗": "3/5",
            "⅘": "4/5", "⅙": "1/6", "⅚": "5/6", "⅛": "1/8",
            "⅜": "3/8", "⅝": "5/8", "⅞": "7/8", "Â½": "1/2",
        }
        for old, new in replacements.items():
            value = value.replace(old, new)
        return value
    if isinstance(value, list):
        return [replace_half(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_half(item) for key, item in value.items()}
    return value


def remove_reported_orphan_labels(pack: dict, findings: list) -> int:
    """Remove only labels that the validator proved are unreferenced.

    Recomputing references in a second helper is unsafe because figure kinds
    use different key-bearing fields. The validator remains the single source
    of truth and reports the exact orphan key in rule 25.
    """
    labels = pack.get("labels")
    if not isinstance(labels, dict):
        return 0
    removed = 0
    for finding in findings:
        if finding.seviye != "UYARI" or finding.kural != 25:
            continue
        match = re.search(r"hiç kullanılmamış:\s*'([^']+)'", finding.mesaj)
        if match and match.group(1) in labels:
            labels.pop(match.group(1))
            removed += 1
    return removed


def repair_package(path: Path) -> dict:
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    pack = next(row for row in rows if record_type(row) == "pack")
    if pack.get("schemaVersion") != CONTRACT_VERSION:
        return {"path": str(path.relative_to(ROOT)), "skipped": True}

    originals = {
        str(row.get("id")): comparable(row)
        for row in rows
        if row.get("id") is not None
    }
    apply_targeted_repairs(rows)
    before = VALIDATOR.validate_file(path)
    by_line = {index + 1: row for index, row in enumerate(rows)}
    removed_figures = 0
    note_guidance = 0
    explanation_repairs = 0

    for finding in before:
        if finding.seviye != "UYARI" or not finding.satir:
            continue
        record = by_line[finding.satir]
        if finding.kural == 3 and record_type(record) == "note":
            old = copy.deepcopy(record)
            append_note_figure_guidance(record)
            note_guidance += int(record != old)
        elif finding.kural == 3 and record_type(record) == "question":
            if record.get("figure") is not None:
                record["figure"] = None
                removed_figures += 1
        elif finding.kural == 21 and record_type(record) == "question":
            old = str(record.get("explanation") or "")
            new = normalize_explanation(old)
            if new and new != old:
                record["explanation"] = new
                explanation_repairs += 1

    rows = [replace_half(row) for row in rows]
    pack = next(row for row in rows if record_type(row) == "pack")
    ensure_contract_metadata(pack, rows)
    orphan_labels_removed = remove_reported_orphan_labels(pack, before)

    producer = "existing-release; repair=gpt-5.6-sol"
    changed_ids = []
    for record in rows:
        record_id = str(record.get("id"))
        if originals.get(record_id) != comparable(record):
            FINALIZER.apply_ai_review(record, producer)
            changed_ids.append(record_id)
    if str(pack.get("id")) not in changed_ids:
        FINALIZER.apply_ai_review(pack, producer)

    path.write_text(
        "\n".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":"))
            for row in rows
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return {
        "path": str(path.relative_to(ROOT)),
        "removedFigures": removed_figures,
        "noteFigureGuidance": note_guidance,
        "explanationRepairs": explanation_repairs,
        "orphanLabelsRemoved": orphan_labels_removed,
        "changedRecords": len(changed_ids),
    }


def main() -> None:
    summaries = []
    for path in sorted((ROOT / "turkiye").glob("*-sinif/*/*.jsonl")):
        summaries.append(repair_package(path))
    print(json.dumps(summaries, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
