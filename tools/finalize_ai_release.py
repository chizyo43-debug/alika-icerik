#!/usr/bin/env python3
"""Legacy Grade 5 migration helpers; local AI release stamping is disabled.

This module historically fabricated ``ai-verified`` fields locally without an
actual GPT-5.6 Sol review run. That path is intentionally blocked. Educational
content may be approved only by the worker's hash-bound, full-coverage,
read-only Sol review manifest and post-stamp verifier.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTRACT_VERSION = "2.2"
CONTRACT_SHA256 = (
    "74b5ee649f01933fd50dfeb7e29706e7dc1ddf0fe3e014ead2fe5cd0896ae7a1"
)
REVIEW_MODEL = "gpt-5.6-sol"
REVIEW_DECLARATION = "ai-generated-and-ai-reviewed-no-human-review"

REVIEW_FIELDS = {
    "reviewStatus",
    "humanReviewed",
    "reviewMode",
    "reviewModel",
    "reviewDeclaration",
    "reviewedContentSha256",
    "reviewDecisionSha256",
    "contentHash",
    "reviewedHash",
    "reviewedBy",
    "provenance",
}

PACKAGES = {
    "matematik": {
        "path": ROOT
        / "turkiye"
        / "5-sinif"
        / "matematik"
        / "matematik-tum.jsonl",
        "source_id": "tr-meb-mat-g05-g08-program-2024",
        "source_url": (
            "https://tymm.meb.gov.tr/upload/program/"
            "2024programmat5678Onayli.pdf"
        ),
        "producer": "claude-opus-5",
        "schema_version": "2.2",
        "visual_minimum_percent": 20,
        "visual_rationale": (
            "Matematikte görsel yalnız çözüm için anlamlı olduğunda kullanılır; "
            "uygulamanın kapalı şekil kataloğunda bulunmayan çizimler metinleştirilir."
        ),
    },
    "fen-bilimleri": {
        "path": ROOT
        / "turkiye"
        / "5-sinif"
        / "fen-bilimleri"
        / "fen-bilimleri-tum.jsonl",
        "source_id": "tr-meb-fen-g05-g08-program-2024",
        "source_url": (
            "https://tymm.meb.gov.tr/upload/program/"
            "2024programfen345678Onayli.pdf"
        ),
        "producer": "minimax-m3; repair=claude-opus-5",
        "schema_version": "2.2",
        "visual_minimum_percent": 30,
        "visual_rationale": (
            "Fen Bilimleri sorularında deney verisi, devre, grafik ve süreç "
            "görselleri çözümün kanıtını taşıdığı ölçüde kullanılır."
        ),
    },
    "turkce": {
        "path": ROOT
        / "turkiye"
        / "5-sinif"
        / "turkce"
        / "turkce-tum.jsonl",
        "producer": "chatgpt-pro; repair=codex-sol",
        "schema_version": "2.2",
        "visual_minimum_percent": 0,
        "visual_rationale": (
            "Türkçe sorularında görsel yalnız metin yapısı veya olay akışı "
            "ölçüldüğünde kullanılır; sözcük ve anlam sorularına süs görseli "
            "eklenmez. Bütün konu anlatımlarının kendi öğretici görseli vardır."
        ),
    },
    "ingilizce": {
        "path": ROOT
        / "turkiye"
        / "5-sinif"
        / "ingilizce"
        / "ingilizce-tum.jsonl",
        "producer": "chatgpt-pro; repair=codex-sol",
        "schema_version": "2.2",
        "visual_minimum_percent": 20,
        "visual_rationale": (
            "İngilizce görselleri program, sınıflandırma ve bağlam "
            "kanıtlarını erişilebilir biçimde düzenler; süs amaçlı kullanılmaz."
        ),
    },
    "sosyal-bilgiler": {
        "path": ROOT
        / "turkiye"
        / "5-sinif"
        / "sosyal-bilgiler"
        / "sosyal-bilgiler-tum.jsonl",
        "producer": "chatgpt-pro; repair=codex-sol",
        "schema_version": "2.2",
        "visual_minimum_percent": 20,
        "visual_rationale": (
            "Sosyal Bilgiler görselleri olay sırası, kurum ilişkisi ve veri "
            "kanıtlarını erişilebilir tablo veya akış olarak düzenler."
        ),
    },
    "soru-bankasi": {
        "path": ROOT
        / "turkiye"
        / "5-sinif"
        / "soru-bankasi"
        / "5-sinif-tum-dersler-2000-soru.jsonl",
        "producer": "compiled-from-ai-verified-grade5-packs; curator=codex-sol",
        "schema_version": "2.2",
        "visual_minimum_percent": 0,
        "visual_rationale": (
            "Ortak banka kaynak beş ders paketindeki görselli soruların "
            "tamamını korur; derslerin farklı görsel politikaları değiştirilmez."
        ),
        "preserve_record_reviews": True,
        "preserve_visual_policy": True,
    },
    "soru-bankasi-6": {
        "path": ROOT
        / "turkiye"
        / "6-sinif"
        / "soru-bankasi"
        / "6-sinif-tum-dersler-2000-soru.jsonl",
        "producer": "compiled-from-ai-verified-grade6-packs; curator=codex-sol",
        "schema_version": "2.2",
        "visual_minimum_percent": 0,
        "visual_rationale": (
            "Ortak banka kaynak yedi ders paketinden seçilir; görselli sorular "
            "önceliklendirilir ve seçilen soruların görsel yapıları korunur."
        ),
        "preserve_record_reviews": False,
        "preserve_visual_policy": True,
    },
}

MATH_POLYGON_TABLE_REWRITES = {
    "tr.g05.mat.5-3-5.q003": {
        "question": "Aşağıdaki tabloya göre, bu çokgenin adı nedir?",
        "rows": [("sides", "7")],
        "alt": "Çokgenin kenar sayısının 7 olduğunu gösteren tablo.",
    },
    "tr.g05.mat.5-3-5.q004": {
        "question": (
            "Aşağıdaki tabloya göre, çokgenin köşe sayısı bir dörtgeninkinden "
            "kaç fazladır?"
        ),
        "rows": [("sides", "9")],
        "alt": "Çokgenin kenar sayısının 9 olduğunu gösteren tablo.",
    },
    "tr.g05.mat.5-3-5.q008": {
        "question": (
            "Aşağıdaki tabloya göre, çokgene belirtilen sayıda kenar daha "
            "eklenirse yeni şeklin adı ne olur?"
        ),
        "rows": [("sides", "5"), ("added", "1")],
        "alt": "Başlangıçta 5 kenar bulunduğunu ve 1 kenar ekleneceğini gösteren tablo.",
    },
    "tr.g05.mat.5-3-5.q014": {
        "question": (
            "Aşağıdaki tabloya göre, düzgün çokgenin çevresi kaç santimetredir?"
        ),
        "rows": [("sides", "7"), ("side_length", "3 cm")],
        "alt": "Düzgün çokgenin 7 kenarlı ve bir kenarının 3 santimetre olduğunu gösteren tablo.",
    },
    "tr.g05.mat.5-3-5.q018": {
        "question": (
            "Tablodaki düzgün çokgenin toplam kenar uzunluğu kaç santimetredir?"
        ),
        "rows": [("sides", "5"), ("side_length", "4 cm")],
        "alt": "Düzgün çokgenin 5 kenarlı ve bir kenarının 4 santimetre olduğunu gösteren tablo.",
    },
    "tr.g05.mat.5-3-6.q008": {
        "question": (
            "Aşağıdaki tabloya göre, düzgün çokgenin bir kenarı kaç santimetredir?"
        ),
        "rows": [("sides", "9"), ("perimeter", "36 cm")],
        "alt": "Düzgün çokgenin 9 kenarlı ve çevresinin 36 santimetre olduğunu gösteren tablo.",
    },
    "tr.g05.mat.5-3-6.q010": {
        "question": "Aşağıdaki tabloya göre, düzgün çokgenin adı nedir?",
        "rows": [("sides", "10")],
        "alt": "Düzgün çokgenin kenar sayısının 10 olduğunu gösteren tablo.",
    },
    "tr.g05.mat.5-3-6.q012": {
        "question": (
            "Aşağıdaki tabloya göre, çokgene belirtilen sayıda kenar daha "
            "eklenirse kenar sayısı kaç olur?"
        ),
        "rows": [("sides", "5"), ("added", "2")],
        "alt": "Başlangıçta 5 kenar bulunduğunu ve 2 kenar ekleneceğini gösteren tablo.",
    },
    "tr.g05.mat.5-3-6.q013": {
        "question": (
            "Aşağıdaki tabloya göre, çokgenin kenar sayısı ile köşe sayısının "
            "toplamı kaçtır?"
        ),
        "rows": [("sides", "8")],
        "alt": "Çokgenin kenar sayısının 8 olduğunu gösteren tablo.",
    },
    "tr.g05.mat.5-3-6.q017": {
        "question": (
            "Tablodaki çevre uzunluğunu kenar sayısına bölünce bir kenar "
            "kaç santimetre bulunur?"
        ),
        "rows": [("sides", "8"), ("perimeter", "40 cm")],
        "alt": "Düzgün çokgenin 8 kenarlı ve çevresinin 40 santimetre olduğunu gösteren tablo.",
    },
}

MATH_TABLE_LABELS = {
    "property": ("math.figure.property", "Özellik"),
    "value": ("math.figure.value", "Değer"),
    "sides": ("math.figure.sides", "Kenar sayısı"),
    "added": ("math.figure.added", "Eklenecek kenar sayısı"),
    "side_length": ("math.figure.side_length", "Bir kenarın uzunluğu"),
    "perimeter": ("math.figure.perimeter", "Çevre"),
}

ENGLISH_TABLE_ALT_TEXT = {
    "tr.g05.ingilizce.q505": (
        "İki satırlı gezi planı: Monday günü valley bölgesinde hike, "
        "Tuesday günü island bölgesinde boat trip."
    ),
    "tr.g05.ingilizce.q506": (
        "İki satırlı gezi planı: Friday günü coast bölgesinde walk by the sea, "
        "Saturday günü museum içinde see a space exhibition."
    ),
    "tr.g05.ingilizce.q507": (
        "Üç gök cismini sınıflandıran tablo: Sun bir star, Earth bir planet, "
        "Moon ise Earth çevresinde hareket eder."
    ),
    "tr.g05.ingilizce.q508": (
        "Hareket ilişkileri tablosu: Earth, Sun çevresinde; Moon, Earth "
        "çevresinde hareket eder."
    ),
    "tr.g05.ingilizce.q515": (
        "Üç gezi hazırlığı: sunny coast için hat, rainy forest için waterproof "
        "boots, snowy mountain için warm coat."
    ),
}

FEN_CIRCUIT_LABELS = {
    "battery": ("fen.figure.circuit.battery", "Pil"),
    "lamp": ("fen.figure.circuit.lamp", "Ampul"),
    "switch": ("fen.figure.circuit.switch", "Anahtar"),
    "resistor": ("fen.figure.circuit.resistor", "Direnç"),
    "wire": ("fen.figure.circuit.wire", "Bağlantı kablosu"),
    "series": ("fen.figure.circuit.series", "Seri devre"),
    "parallel": ("fen.figure.circuit.parallel", "Paralel devre"),
}


def canonical_sha256(value: object) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def strip_review_fields(record: dict) -> dict:
    return {
        key: copy.deepcopy(value)
        for key, value in record.items()
        if key not in REVIEW_FIELDS
    }


def apply_ai_review(record: dict, producer: str) -> None:
    del record, producer
    raise RuntimeError(
        "Yerel apply_ai_review yasaktır. Hash-bağlı tam kapsamlı GPT-5.6 Sol "
        "inceleme manifesti olmadan ai-verified üretilemez."
    )


def assert_current_ai_review(record: dict) -> None:
    content_sha = canonical_sha256(strip_review_fields(record))
    expected = f"sha256:{content_sha}"
    if (
        record.get("reviewStatus") != "ai-verified"
        or record.get("humanReviewed") is not False
        or record.get("reviewDeclaration") != REVIEW_DECLARATION
        or record.get("contentHash") != expected
        or record.get("reviewedHash") != expected
        or record.get("reviewedContentSha256") != content_sha
    ):
        raise ValueError(
            f"{record.get('id')}: kaynak AI inceleme damgası güncel değil"
        )


def evidence_id(source_id: str, objectives: list[str]) -> str:
    codes = "+".join(sorted(dict.fromkeys(objectives)))
    return f"{source_id}#{codes}"


def assert_page_evidence(record: dict, source_id: str) -> None:
    evidence = str(record.get("objectiveEvidenceId") or "")
    if re.fullmatch(
        rf"{re.escape(source_id)}(?::pdf-page-|#p)\d+",
        evidence,
        flags=re.I,
    ) is None:
        raise ValueError(
            f"{record.get('id')}: exact PDF page evidence is required"
        )


def finalize_math(rows: list[dict], config: dict) -> None:
    source_id = config["source_id"]
    source_url = config["source_url"]
    pack = next(record for record in rows if record.get("type") == "pack")
    labels = pack.setdefault("labels", {})
    for key, value in MATH_TABLE_LABELS.values():
        labels[key] = value
    note_objectives: defaultdict[str, set[str]] = defaultdict(set)
    for record in rows:
        if record.get("type") != "question":
            continue
        objective = str(record.get("objective") or "").strip()
        if not objective.startswith("MAT.5."):
            raise ValueError(f"{record.get('id')}: unexpected objective {objective!r}")
        note_objectives[str(record.get("noteId"))].add(objective)
        record["objectiveSource"] = source_url
        record["sourceRefs"] = [source_id]
        assert_page_evidence(record, source_id)

    for record in rows:
        figure = record.get("figure")
        if (
            record.get("type") != "question"
            or not isinstance(figure, dict)
            or figure.get("kind") != "shape"
            or figure.get("type") != "polygon"
            or "sides" not in figure
        ):
            continue
        sides = figure.pop("sides")
        if sides == 6:
            # AliKa's catalogued generic polygon is rendered as a hexagon.
            continue
        if sides == 4:
            figure["type"] = "square"
            continue
        replacement = MATH_POLYGON_TABLE_REWRITES.get(str(record.get("id")))
        if replacement is None:
            raise ValueError(
                f"{record.get('id')}: unsupported polygon needs an explicit rewrite"
            )
        # Replaced below with an AliKa-native table whose data is required to
        # solve the question.

    for record in rows:
        replacement = MATH_POLYGON_TABLE_REWRITES.get(str(record.get("id")))
        if replacement is None:
            continue
        old_figure = record.get("figure")
        alt_key = (
            old_figure.get("altTextKey")
            if isinstance(old_figure, dict)
            else f"{record['id']}.visual.alt"
        )
        labels[alt_key] = replacement["alt"]
        record["question"] = replacement["question"]
        record["figure"] = {
            "kind": "table",
            "headerKeys": [
                MATH_TABLE_LABELS["property"][0],
                MATH_TABLE_LABELS["value"][0],
            ],
            "rows": [
                [
                    {"key": MATH_TABLE_LABELS[name][0]},
                    {"v": value},
                ]
                for name, value in replacement["rows"]
            ],
            "altTextKey": alt_key,
        }

    for record in rows:
        if record.get("type") != "note":
            continue
        objectives = sorted(note_objectives.get(str(record.get("id")), set()))
        if not objectives:
            raise ValueError(f"{record.get('id')}: linked outcome not found")
        record["objectives"] = objectives
        record["objectiveSource"] = source_url
        record["sourceRefs"] = [source_id]
        assert_page_evidence(record, source_id)


def finalize_science(rows: list[dict]) -> None:
    pack = next(record for record in rows if record.get("type") == "pack")
    labels = pack.setdefault("labels", {})
    for key, value in FEN_CIRCUIT_LABELS.values():
        labels[key] = value

    for record in rows:
        figure = record.get("figure")
        if isinstance(figure, dict) and figure.get("kind") == "circuit":
            needed = set(figure.get("elements") or [])
            if figure.get("layout"):
                needed.add(figure["layout"])
            figure["labelKeys"] = {
                name: FEN_CIRCUIT_LABELS[name][0] for name in sorted(needed)
            }

        # The canonical validator intentionally ignores inline textual tables.
        # These lessons refer to an actual structured figure, so use the
        # unambiguous word "görsel" throughout instead of triggering that
        # inline-table exception.
        if record.get("type") == "note" and figure:
            body = str(record.get("body") or "")
            record["body"] = re.sub(
                r"tablo", lambda match: "Görsel" if match.group(0)[0].isupper() else "görsel",
                body, flags=re.IGNORECASE,
            )

        question = str(record.get("question") or "")
        prefix = "Verilen tabloya göre, "
        if record.get("type") == "question" and figure and question.startswith(prefix):
            remainder = question[len(prefix):]
            record["question"] = (
                "Görseli inceleyin. " + remainder[:1].upper() + remainder[1:]
            )

    hierarchy_fix = next(
        record for record in rows if record.get("id") == "tr-g05-fen-q0370"
    )
    hierarchy_fix["subtopicKey"] = "hal-degisimi"
    hierarchy_fix["topic"] = "Hâl değişimi"

    missing_figure_fix = next(
        record for record in rows if record.get("id") == "tr-g05-fen-q0434"
    )
    missing_figure_fix["question"] = missing_figure_fix["question"].replace(
        "Çizdiği şemaya göre pil, anahtar, ampul ve kabloları bağlar. ",
        "Pil, anahtar, ampul ve kabloları bağlar. ",
    )


def finalize_english(rows: list[dict]) -> None:
    pack = next(record for record in rows if record.get("type") == "pack")
    labels = pack.setdefault("labels", {})
    for record in rows:
        alt_text = ENGLISH_TABLE_ALT_TEXT.get(str(record.get("id")))
        if alt_text is None:
            continue
        figure = record.get("figure")
        if not isinstance(figure, dict) or figure.get("kind") != "table":
            raise ValueError(f"{record.get('id')}: expected a table figure")
        key = f"{record['id']}.visual.alt"
        figure["altTextKey"] = key
        labels[key] = alt_text


def referenced_label_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for name, child in value.items():
            if (
                isinstance(child, str)
                and (name == "key" or name.endswith("Key"))
            ):
                keys.add(child)
            elif name.endswith("Keys") and isinstance(child, (list, dict)):
                if isinstance(child, list):
                    keys.update(item for item in child if isinstance(item, str))
                else:
                    keys.update(
                        item for item in child.values() if isinstance(item, str)
                    )
            keys.update(referenced_label_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(referenced_label_keys(child))
    return keys


def remove_orphan_labels(rows: list[dict]) -> None:
    pack = next(record for record in rows if record.get("type") == "pack")
    referenced: set[str] = set()
    for record in rows:
        referenced.update(referenced_label_keys(record.get("figure")))
    labels = pack.get("labels")
    if isinstance(labels, dict):
        pack["labels"] = {
            key: value for key, value in labels.items() if key in referenced
        }


def finalize_package(name: str, config: dict) -> None:
    raise RuntimeError(
        "finalize_ai_release yayın yolu devre dışıdır. İçeriği pending olarak "
        "hazırlayın ve worker'ın tam kapsamlı GPT-5.6 Sol "
        "denetim/onarım/yayın akışını kullanın."
    )

    # Aşağıdaki eski taşıma kodu yalnız tarihsel referans olarak tutulmaktadır;
    # yukarıdaki güvenlik kapısı kaldırılmamalıdır.
    path: Path = config["path"]
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    pack = next(record for record in rows if record.get("type") == "pack")
    if pack.get("schemaVersion") != config["schema_version"]:
        raise ValueError(
            f"{name}: expected schema {config['schema_version']}"
        )

    if name == "matematik":
        finalize_math(rows, config)
    elif name == "fen-bilimleri":
        finalize_science(rows)
    elif name == "ingilizce":
        finalize_english(rows)

    remove_orphan_labels(rows)

    preserve_reviews = bool(config.get("preserve_record_reviews"))
    for record in rows:
        if record.get("type") in {"note", "question"}:
            if (
                record.get("objectiveSource") == "PENDING"
                or record.get("objectiveEvidenceId") == "PENDING"
                or "PENDING" in (record.get("sourceRefs") or [])
            ):
                raise ValueError(f"{record.get('id')}: PENDING evidence remains")
            if preserve_reviews:
                assert_current_ai_review(record)
            else:
                apply_ai_review(record, config["producer"])

    pack_update = {
        "reviewStatus": "ai-verified",
        "humanReviewed": False,
        "reviewMode": "ai-only",
        "reviewModel": REVIEW_MODEL,
        "reviewDeclaration": REVIEW_DECLARATION,
        "disclosure": REVIEW_DECLARATION,
        "publishBlocked": False,
    }
    if config["schema_version"] == CONTRACT_VERSION:
        questions = [r for r in rows if r.get("type") == "question"]
        figured_questions = sum(bool(r.get("figure")) for r in questions)
        visual_policy = (
            pack.get("visualPolicy")
            if config.get("preserve_visual_policy")
            else {
                "version": "1.0",
                "everyNote": True,
                "questionMinimumPercent": config["visual_minimum_percent"],
                "balancedByObjective": False,
                "rationale": config["visual_rationale"],
            }
        )
        pack_update.update(
            {
                "contentContractVersion": CONTRACT_VERSION,
                "contentContractHash": f"sha256:{CONTRACT_SHA256}",
                "visualPolicy": visual_policy,
            }
        )
        contract_policy = pack.setdefault("contractPolicy", {})
        contract_policy["minFiguredQuestions"] = figured_questions
        contract_policy["everyNoteHasFigure"] = True
    pack.update(pack_update)
    pack.pop("publishBlockReasons", None)
    apply_ai_review(pack, config["producer"])

    path.write_text(
        "\n".join(
            json.dumps(record, ensure_ascii=False, separators=(",", ":"))
            for record in rows
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"{name}: {len(rows)} records finalized")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "packages",
        nargs="*",
        choices=sorted(PACKAGES),
        help="Boş bırakılırsa tüm paketler sonlandırılır.",
    )
    args = parser.parse_args(argv)
    targets = args.packages or list(PACKAGES)
    for name in targets:
        config = PACKAGES[name]
        finalize_package(name, config)


if __name__ == "__main__":
    main()
