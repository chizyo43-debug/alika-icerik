#!/usr/bin/env python3
"""Build the curated Türkiye Grade 6 all-subject 2,000-question bank.

The bank is an aggregate, not 2,000 newly authored questions. It selects 380
questions from each of the five core subjects and 50 questions each from
Information Technologies and Religious Culture. Selection preserves every
note and objective, prioritizes visual questions, and balances answer positions.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRADE6 = ROOT / "turkiye" / "6-sinif"
OUTPUT = GRADE6 / "soru-bankasi" / "6-sinif-tum-dersler-2000-soru.jsonl"
CONTRACT_HASH = (
    "sha256:74b5ee649f01933fd50dfeb7e29706e7dc1ddf0fe3e014ead2fe5cd0896ae7a1"
)
SUBJECTS = (
    ("Matematik", GRADE6 / "matematik" / "matematik-tum.jsonl", (95, 95, 95, 95)),
    (
        "Fen Bilimleri",
        GRADE6 / "fen-bilimleri" / "fen-bilimleri-tum.jsonl",
        (95, 95, 95, 95),
    ),
    ("Türkçe", GRADE6 / "turkce" / "turkce-tum.jsonl", (95, 95, 95, 95)),
    ("İngilizce", GRADE6 / "ingilizce" / "ingilizce-tum.jsonl", (95, 95, 95, 95)),
    (
        "Sosyal Bilgiler",
        GRADE6 / "sosyal-bilgiler" / "sosyal-bilgiler-tum.jsonl",
        (95, 95, 95, 95),
    ),
    (
        "Bilişim Teknolojileri ve Yazılım",
        GRADE6 / "bilisim-teknolojileri" / "bilisim-teknolojileri-tum.jsonl",
        (13, 13, 12, 12),
    ),
    (
        "Din Kültürü ve Ahlak Bilgisi",
        GRADE6 / "din-kulturu" / "din-kulturu-tum.jsonl",
        (12, 12, 13, 13),
    ),
)
AUDIT_REASON_REWRITES = {
    "tr-g06-fen-bilimleri-q012": {
        0: "Bulut sayısı gezegenleri Güneş'e yakınlıklarına göre sıralamada kullanılan uzaklık ölçütünü vermez.",
    },
    "tr-g06-fen-bilimleri-q013": {
        3: "Deney yapmak bir değişkeni sınamayı gerektirir; burada öğrenci deney kurmuyor, gezegenleri halka özelliğine göre grupluyor.",
    },
    "tr-g06-fen-bilimleri-q026": {
        0: "Kâğıdın renginin değişmesi modelin açıkladığı bilimsel bilgiyi değiştirmez ve modeli geliştirmek için yeni kanıt sağlamaz.",
    },
    "tr-g06-fen-bilimleri-q061": {
        1: "Cismin rengi, kuvvetlerin yönünü, doğrultusunu veya büyüklüğünü belirlemediği için bileşke kuvvet hesabında kullanılmaz.",
        2: "Kuvveti uygulayan kişinin boyu, uygulanan kuvvetlerin vektörel özelliklerini göstermediği için bileşke kuvveti belirlemez.",
    },
    "tr-g06-fen-bilimleri-q177": {
        1: "Kalp kanı dolaşıma pompalayan organdır; devrede süreci başlatan anahtarın uyaran işlevini temsil etmez.",
        2: "Mide besinlerin sindiriminde görev yapar; devrede süreci başlatan anahtarın uyaran işlevini temsil etmez.",
        3: "Akciğer solunum ve gaz alışverişinde görev yapar; devrede süreci başlatan anahtarın uyaran işlevini temsil etmez.",
    },
    "tr-g06-matematik-q385": {
        3: "Çemberin alanı ile çevresini toplamak iki farklı niceliği birleştirir; çevre/çap oranını oluşturmadığı için değişmezliği sınamaz.",
    },
    "tr-g06-matematik-q395": {
        3: "İçteki karenin çevresi çember uzunluğu ile çap arasındaki oranı ölçmez ve farklı çaplı çemberlere ilişkin yeni kanıt sağlamaz.",
    },
    "tr-g06-matematik-q463": {
        1: "10 ile diğer iki grubun toplamı 14 arasındaki fark, sınıfın yarısını belirlemez; yorum için 10 sayısı 24 ÷ 2 = 12 ile karşılaştırılmalıdır.",
    },
    "tr-g06-turkce-q210": {
        1: "İnsanlar arasındaki yakınlık ve sevgi eksikliği, metindeki 'kapılar kapalı, yüzler gülmüyor' ifadeleriyle örtüşür; doğru cevap budur.",
    },
}
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
GENERIC_REASON_RE = re.compile(
    r"(?i)^(?:(?:bu|o)\s+)?(?:(?:şık|seçenek|cevap)\s+)?"
    r"(?:yanlış(?:tır)?|doğru\s+değil(?:dir)?|uygun\s+değil(?:dir)?|cevap\s+değil)"
    r"[.!?;,:]*$"
)
ANSWER_LETTER_RE = re.compile(
    r"(?i)\s*(?:bu nedenle\s+)?doğru\s+(?:cevap|yanıt)\s*[:\-]?\s*"
    r"[A-D]\s*(?:seçeneğidir|şıkkıdır|'dir|dır|dir|dur|dür|tır|tir|tur|tür)?[.!]?"
)
LETTER_OPTION_RE = re.compile(
    r"(?i)\s*[A-D]\s+(?:şıkkı|seçeneği)(?:dir|dır|dur|dür|tır|tir|tur|tür)?[.!]?"
)
OPTION_LETTER_RE = re.compile(
    r"(?i)\s*(?:bu nedenle\s+)?(?:doğru\s+)?(?:şık|seçenek)\s+"
    r"[A-D](?:'dir|'dır|'dur|'dür|dir|dır|dur|dür|tır|tir|tur|tür)?[.!]?"
)


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":"))
            for row in rows
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def canonical_sha256(value: object) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def insertion_order_sha256(value: object) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def assert_verified(record: dict) -> None:
    content = {
        key: copy.deepcopy(value)
        for key, value in record.items()
        if key not in REVIEW_FIELDS
    }
    expected_hashes = {
        f"sha256:{canonical_sha256(content)}",
        f"sha256:{insertion_order_sha256(content)}",
    }
    if (
        record.get("reviewStatus") != "ai-verified"
        or record.get("humanReviewed") is not False
        or record.get("reviewDeclaration")
        != "ai-generated-and-ai-reviewed-no-human-review"
        or record.get("contentHash") not in expected_hashes
        or record.get("reviewedHash") != record.get("contentHash")
        or not re.fullmatch(r"[0-9a-f]{64}", str(record.get("reviewedContentSha256") or ""))
    ):
        raise ValueError(f"{record.get('id')}: güncel AI inceleme damgası yok")


def stable_rank(subject: str, question: dict) -> str:
    return hashlib.sha256(
        f"grade6-bank-v1\0{subject}\0{question['id']}".encode("utf-8")
    ).hexdigest()


def normalize_option(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return re.sub(r"\s+", " ", text).strip(" \t\r\n.,;:!?\"'()[]{}")


def reason_is_generic(reason: object, choice: object) -> bool:
    text_value = " ".join(
        unicodedata.normalize("NFKC", str(reason or "")).casefold().split()
    )
    if not text_value or GENERIC_REASON_RE.fullmatch(text_value):
        return True
    reason_norm = "".join(
        char for char in unicodedata.normalize("NFKC", text_value)
        if not unicodedata.category(char).startswith(("P", "Z", "C"))
    )
    choice_norm = "".join(
        char
        for char in unicodedata.normalize(
            "NFKC", str(choice or "")
        ).casefold()
        if not unicodedata.category(char).startswith(("P", "Z", "C"))
    )
    if choice_norm and choice_norm in reason_norm:
        return len(reason_norm.replace(choice_norm, "", 1).strip()) < 4
    return len(reason_norm) < 12


def option_pool_debt(questions: list[dict]) -> tuple[int, int]:
    counts: Counter[str] = Counter()
    families: dict[str, set[str]] = defaultdict(set)
    correct_counts: Counter[str] = Counter()
    for question in questions:
        for option in question["choices"]:
            normalized = normalize_option(option)
            counts[normalized] += 1
            families[normalized].add(question["familyId"])
        correct_counts[
            normalize_option(question["choices"][question["correct"]])
        ] += 1
    homeless = [
        option for option, count in counts.items()
        if count >= 4 and len(families[option]) >= 2
        and correct_counts[option] == 0
    ]
    return len(homeless), sum(counts[option] - 3 for option in homeless)


def normalized_choice_set(question: dict) -> tuple[str, ...]:
    return tuple(sorted(normalize_option(v) for v in question["choices"]))


def choice_set_debt(questions: list[dict]) -> int:
    counts: Counter[tuple[str, ...]] = Counter()
    families: dict[tuple[str, ...], set[str]] = defaultdict(set)
    for question in questions:
        key = normalized_choice_set(question)
        counts[key] += 1
        families[key].add(question["familyId"])
    return sum(count for key, count in counts.items() if len(families[key]) > 1)


def select_subject(
    subject: str,
    notes: list[dict],
    questions: list[dict],
    target_positions: tuple[int, int, int, int],
) -> list[dict]:
    if len(questions) != 500:
        raise ValueError(f"{subject}: 500 kaynak soru bekleniyor")
    if Counter(question["correct"] for question in questions) != {
        0: 125,
        1: 125,
        2: 125,
        3: 125,
    }:
        raise ValueError(f"{subject}: kaynak cevap dağılımı 125'er değil")

    note_counts = Counter(question["noteId"] for question in questions)
    objective_counts = Counter(question["objective"] for question in questions)
    family_counts = Counter(question["familyId"] for question in questions)
    option_counts: Counter[str] = Counter()
    option_families: dict[str, set[str]] = defaultdict(set)
    for question in questions:
        for option in question["choices"]:
            normalized = normalize_option(option)
            option_counts[normalized] += 1
            option_families[normalized].add(question["familyId"])
    shared_options = {
        option
        for option, count in option_counts.items()
        if count >= 4 and len(option_families[option]) >= 2
    }
    # Derleme, kaynak pakette doğru cevap olarak bulunan ortak bir seçeneğin
    # bütün doğru örneklerini yanlışlıkla eleyip onu "sürekli yanlış dolgu"ya
    # dönüştürmemeli.
    protected_correct = {
        question["id"]
        for question in questions
        if normalize_option(question["choices"][question["correct"]])
        in shared_options
    }
    removed: set[str] = set()
    preserve_all_families = sum(target_positions) >= len(family_counts)

    for position in range(4):
        remove_target = 125 - target_positions[position]
        for allow_protected in (False, True):
            candidates = sorted(
                (
                    question
                    for question in questions
                    if question["correct"] == position
                    and question["id"] not in removed
                    and (allow_protected or question["id"] not in protected_correct)
                ),
                key=lambda question: (
                    bool(question.get("figure")),
                    -note_counts[question["noteId"]],
                    -objective_counts[question["objective"]],
                    -family_counts[question["familyId"]],
                    stable_rank(subject, question),
                ),
            )
            for question in candidates:
                removed_for_position = sum(
                    item["correct"] == position and item["id"] in removed
                    for item in questions
                )
                if removed_for_position >= remove_target:
                    break
                note_id = question["noteId"]
                objective = question["objective"]
                family = question["familyId"]
                if note_counts[note_id] <= 1 or objective_counts[objective] <= 1:
                    continue
                if preserve_all_families and family_counts[family] <= 1:
                    continue
                removed.add(question["id"])
                note_counts[note_id] -= 1
                objective_counts[objective] -= 1
                family_counts[family] -= 1
        removed_for_position = sum(
            item["correct"] == position and item["id"] in removed
            for item in questions
        )
        if removed_for_position != remove_target:
            raise ValueError(
                f"{subject}: {position}. cevap konumundan {remove_target} soru çıkarılamadı; "
                f"çıkarılan {removed_for_position}"
            )

    selected_ids = {
        question["id"] for question in questions if question["id"] not in removed
    }

    # Küçük ders kotalarında bir seçenek seçkide birkaç kez çeldirici olarak
    # kalırken onun doğru örneği dışarıda kalabilir. Aynı cevap konumunda
    # bire bir takas yaparak bu kapalı-havuz kusurunu mümkün olduğunca gider.
    for _ in range(32):
        current = [q for q in questions if q["id"] in selected_ids]
        current_option_counts: Counter[str] = Counter()
        current_option_families: dict[str, set[str]] = defaultdict(set)
        current_correct_counts: Counter[str] = Counter()
        for question in current:
            for option in question["choices"]:
                normalized = normalize_option(option)
                current_option_counts[normalized] += 1
                current_option_families[normalized].add(question["familyId"])
            current_correct_counts[
                normalize_option(question["choices"][question["correct"]])
            ] += 1
        homeless = sorted(
            option
            for option, count in current_option_counts.items()
            if count >= 4
            and len(current_option_families[option]) >= 2
            and current_correct_counts[option] == 0
        )
        if not homeless:
            break
        swapped = False
        current_note_counts = Counter(q["noteId"] for q in current)
        current_objective_counts = Counter(q["objective"] for q in current)
        current_family_counts = Counter(q["familyId"] for q in current)
        for option in homeless:
            additions = sorted(
                (
                    q for q in questions
                    if q["id"] not in selected_ids
                    and normalize_option(q["choices"][q["correct"]]) == option
                ),
                key=lambda q: (not bool(q.get("figure")), stable_rank(subject, q)),
            )
            for addition in additions:
                removals = sorted(
                    (
                        q for q in current
                        if q["correct"] == addition["correct"]
                        and current_note_counts[q["noteId"]] > 1
                        and current_objective_counts[q["objective"]] > 1
                        and (
                            not preserve_all_families
                            or current_family_counts[q["familyId"]] > 1
                        )
                        and (
                            current_option_counts[
                                normalize_option(q["choices"][q["correct"]])
                            ] < 4
                            or len(current_option_families[
                                normalize_option(q["choices"][q["correct"]])
                            ]) < 2
                            or current_correct_counts[
                                normalize_option(q["choices"][q["correct"]])
                            ] > 1
                        )
                    ),
                    key=lambda q: (
                        bool(q.get("figure")),
                        stable_rank(subject, q),
                    ),
                )
                if not removals:
                    continue
                selected_ids.remove(removals[0]["id"])
                selected_ids.add(addition["id"])
                swapped = True
                break
            if swapped:
                break
        if not swapped:
            base_debt = option_pool_debt(current)
            for option in homeless:
                victims = sorted(
                    (
                        q for q in current
                        if option in {normalize_option(v) for v in q["choices"]}
                        and current_note_counts[q["noteId"]] > 1
                        and current_objective_counts[q["objective"]] > 1
                        and (
                            not preserve_all_families
                            or current_family_counts[q["familyId"]] > 1
                        )
                    ),
                    key=lambda q: (bool(q.get("figure")), stable_rank(subject, q)),
                )
                for victim in victims:
                    additions = sorted(
                        (
                            q for q in questions
                            if q["id"] not in selected_ids
                            and q["correct"] == victim["correct"]
                            and option not in {
                                normalize_option(v) for v in q["choices"]
                            }
                        ),
                        key=lambda q: (
                            not bool(q.get("figure")),
                            stable_rank(subject, q),
                        ),
                    )
                    for addition in additions:
                        trial_ids = (
                            selected_ids - {victim["id"]}
                        ) | {addition["id"]}
                        trial = [
                            q for q in questions if q["id"] in trial_ids
                        ]
                        if option_pool_debt(trial) >= base_debt:
                            continue
                        selected_ids = trial_ids
                        swapped = True
                        break
                    if swapped:
                        break
                if swapped:
                    break
        if not swapped:
            break

    # Aynı dört seçenekten oluşan bir kümenin bağımsız ailelere yayılmasını
    # azalt. Bu da cevap konumu, not, kazanım ve (kota elveriyorsa) aile
    # kapsamını bozmayan bire bir takaslarla yapılır.
    for _ in range(64):
        current = [q for q in questions if q["id"] in selected_ids]
        base_debt = choice_set_debt(current)
        if base_debt == 0:
            break
        set_families: dict[tuple[str, ...], set[str]] = defaultdict(set)
        for question in current:
            set_families[normalized_choice_set(question)].add(
                question["familyId"]
            )
        current_note_counts = Counter(q["noteId"] for q in current)
        current_objective_counts = Counter(q["objective"] for q in current)
        current_family_counts = Counter(q["familyId"] for q in current)
        victims = sorted(
            (
                q for q in current
                if len(set_families[normalized_choice_set(q)]) > 1
                and current_note_counts[q["noteId"]] > 1
                and current_objective_counts[q["objective"]] > 1
                and (
                    not preserve_all_families
                    or current_family_counts[q["familyId"]] > 1
                )
            ),
            key=lambda q: (bool(q.get("figure")), stable_rank(subject, q)),
        )
        swapped = False
        for victim in victims:
            additions = sorted(
                (
                    q for q in questions
                    if q["id"] not in selected_ids
                    and q["correct"] == victim["correct"]
                    and normalized_choice_set(q) != normalized_choice_set(victim)
                ),
                key=lambda q: (
                    not bool(q.get("figure")),
                    stable_rank(subject, q),
                ),
            )
            for addition in additions:
                trial_ids = (selected_ids - {victim["id"]}) | {addition["id"]}
                trial = [q for q in questions if q["id"] in trial_ids]
                if option_pool_debt(trial) > option_pool_debt(current):
                    continue
                if choice_set_debt(trial) >= base_debt:
                    continue
                selected_ids = trial_ids
                swapped = True
                break
            if swapped:
                break
        if not swapped:
            break

    selected = [
        copy.deepcopy(question)
        for question in questions
        if question["id"] in selected_ids
    ]
    target_total = sum(target_positions)
    if len(selected) != target_total:
        raise ValueError(
            f"{subject}: {target_total} soru seçilemedi, bulunan {len(selected)}"
        )
    if Counter(question["correct"] for question in selected) != dict(enumerate(target_positions)):
        raise ValueError(f"{subject}: cevap konumları hedefle uyuşmuyor")
    selected_notes = {question["noteId"] for question in selected}
    if selected_notes != {note["id"] for note in notes}:
        missing = sorted({note["id"] for note in notes} - selected_notes)
        raise ValueError(f"{subject}: sorusuz kalan notlar: {missing}")
    if {question["objective"] for question in selected} != {
        question["objective"] for question in questions
    }:
        raise ValueError(f"{subject}: kazanım kapsamı kayboldu")
    if preserve_all_families and {question["familyId"] for question in selected} != {
        question["familyId"] for question in questions
    }:
        raise ValueError(f"{subject}: aile kapsamı kayboldu")
    return selected


def referenced_label_keys(value: object) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for name, child in value.items():
            if (
                isinstance(child, str)
                and (name == "key" or name.endswith("Key"))
            ):
                found.add(child)
            elif name.endswith("Keys") and isinstance(child, (list, dict)):
                if isinstance(child, list):
                    found.update(
                        item for item in child if isinstance(item, str)
                    )
                else:
                    found.update(
                        item for item in child.values()
                        if isinstance(item, str)
                    )
            found.update(referenced_label_keys(child))
    elif isinstance(value, list):
        for child in value:
            found.update(referenced_label_keys(child))
    return found


def namespace_label_keys(value: object, prefix: str) -> object:
    if isinstance(value, dict):
        rewritten: dict = {}
        for name, child in value.items():
            if isinstance(child, str) and (name == "key" or name.endswith("Key")):
                rewritten[name] = f"{prefix}.{child}"
            elif name.endswith("Keys") and isinstance(child, list):
                rewritten[name] = [
                    f"{prefix}.{item}" if isinstance(item, str) else item
                    for item in child
                ]
            elif name.endswith("Keys") and isinstance(child, dict):
                rewritten[name] = {
                    key: f"{prefix}.{item}" if isinstance(item, str) else item
                    for key, item in child.items()
                }
            else:
                rewritten[name] = namespace_label_keys(child, prefix)
        return rewritten
    if isinstance(value, list):
        return [namespace_label_keys(child, prefix) for child in value]
    return value


def build() -> tuple[list[dict], dict]:
    all_notes: list[dict] = []
    all_questions: list[dict] = []
    all_labels: dict[str, str] = {}
    all_sources: dict[str, dict] = {}
    source_packages = []
    visual_by_subject: dict[str, dict[str, int]] = {}

    target_by_subject: dict[str, int] = {}
    target_positions_by_subject: dict[str, list[int]] = {}
    family_by_subject: dict[str, dict[str, int]] = {}

    for subject, path, target_positions in SUBJECTS:
        rows = read_jsonl(path)
        pack = next(row for row in rows if row.get("type") == "pack")
        notes = [row for row in rows if row.get("type") == "note"]
        questions = [row for row in rows if row.get("type") == "question"]
        if pack.get("reviewStatus") != "ai-verified":
            raise ValueError(f"{subject}: kaynak paket AI doğrulanmış değil")
        for record in notes + questions:
            assert_verified(record)
        selected = select_subject(subject, notes, questions, target_positions)
        label_prefix = pack["id"]
        copied_notes = copy.deepcopy(notes)
        for record in copied_notes + selected:
            if record.get("figure") is not None:
                record["figure"] = namespace_label_keys(
                    record["figure"], label_prefix
                )
                if record.get("type") == "question":
                    stem = str(record.get("question") or "")
                    record["question"] = (
                        "Aşağıdaki görseli inceleyin. " + stem
                    )
                elif record.get("type") == "note":
                    body = str(record.get("body") or "")
                    record["body"] = (
                        body.rstrip()
                        + "\n\nAşağıdaki görseli inceleyin."
                    )
        for record in selected:
            explanation = str(record.get("explanation") or "")
            explanation = ANSWER_LETTER_RE.sub("", explanation)
            explanation = LETTER_OPTION_RE.sub("", explanation)
            explanation = OPTION_LETTER_RE.sub("", explanation).strip()
            if not explanation:
                explanation = str(
                    record["distractorWhy"][record["correct"]]
                )
            record["explanation"] = explanation
            for index, reason in enumerate(record.get("distractorWhy") or []):
                if index == record.get("correct"):
                    continue
                if reason_is_generic(reason, record["choices"][index]):
                    record["distractorWhy"][index] = (
                        f"{record['choices'][index]} seçeneği, şu çözüm "
                        f"ölçütünü karşılamaz: {explanation}"
                    )
            for index, reason in AUDIT_REASON_REWRITES.get(
                record["id"], {}
            ).items():
                record["distractorWhy"][index] = reason
        all_notes.extend(copied_notes)
        all_questions.extend(selected)
        source_packages.append(
            {
                "id": pack["id"],
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "questions": len(selected),
            }
        )
        visual_by_subject[subject] = {
            "source": sum(bool(question.get("figure")) for question in questions),
            "selected": sum(bool(question.get("figure")) for question in selected),
        }
        target_by_subject[subject] = len(selected)
        target_positions_by_subject[subject] = list(target_positions)
        family_by_subject[subject] = {
            "source": len({question["familyId"] for question in questions}),
            "selected": len({question["familyId"] for question in selected}),
        }
        for key, value in (pack.get("labels") or {}).items():
            all_labels[f"{label_prefix}.{key}"] = value
        for item in pack.get("sources") or []:
            source_id = item.get("sourceId")
            if not source_id:
                raise ValueError(f"{subject}: sourceId boş")
            normalized_item = copy.deepcopy(item)
            # ``reused`` yalnız kaynak paketin kendi üretim geçmişini anlatır;
            # aynı resmî belgenin kimliği veya doğrulama kanıtı değildir.
            normalized_item.pop("reused", None)
            previous = all_sources.get(source_id)
            if previous is not None and previous != normalized_item:
                raise ValueError(f"kaynak tanımı çakışması: {source_id}")
            all_sources[source_id] = normalized_item

    if len({note["id"] for note in all_notes}) != len(all_notes):
        raise ValueError("Dersler arasında not kimliği çakışıyor")
    if len({question["id"] for question in all_questions}) != len(all_questions):
        raise ValueError("Dersler arasında soru kimliği çakışıyor")

    note_ids_by_objective: defaultdict[str, set[str]] = defaultdict(set)
    for note in all_notes:
        for objective in note.get("objectives") or [note.get("objective")]:
            if objective:
                note_ids_by_objective[str(objective)].add(note["id"])
    question_counts = Counter(
        str(question["objective"]) for question in all_questions
    )
    linked_notes: defaultdict[str, set[str]] = defaultdict(set)
    for question in all_questions:
        linked_notes[str(question["objective"])].add(question["noteId"])
    coverage = {
        objective: {
            "notes": sorted(
                linked_notes[objective] or note_ids_by_objective[objective]
            ),
            "questions": question_counts[objective],
        }
        for objective in sorted(question_counts)
    }

    used_labels: set[str] = set()
    for record in all_notes + all_questions:
        used_labels.update(referenced_label_keys(record.get("figure")))
    labels = {
        key: all_labels[key]
        for key in sorted(used_labels)
        if key in all_labels
    }
    subject_counts = dict(
        sorted(Counter(question["subject"] for question in all_questions).items())
    )
    answer_balance = [
        sum(question["correct"] == position for question in all_questions)
        for position in range(4)
    ]
    figure_count = sum(bool(question.get("figure")) for question in all_questions)
    families = {question["familyId"] for question in all_questions}
    pack = {
        "type": "pack",
        "schemaVersion": "2.2",
        "id": "tr.g06.tum-dersler.soru-bankasi",
        "version": 1,
        "lang": "tr",
        "country": "TR",
        "curriculum": "MEB-TYMM-2024+2025+2026",
        "curricula": ["MEB-TYMM-2024", "MEB-TYMM-2025", "MEB-TYMM-2026"],
        "subject": "Tüm Dersler",
        "grade": 6,
        "theme": "Türkiye 6. Sınıf — 2.000 Soruluk Tüm Dersler Soru Bankası",
        "license": "CC-BY-NC-4.0",
        "source": "alika-grade6-ai-verified-course-packs",
        "sources": [all_sources[key] for key in sorted(all_sources)],
        "sourcePackages": source_packages,
        "selectionPolicy": {
            "version": "grade6-bank-v1",
            "mode": "curated-aggregate",
            "perSubject": target_by_subject,
            "perAnswerPositionBySubject": target_positions_by_subject,
            "prioritizeFigures": True,
            "preserveAllFigures": False,
            "preserveEveryNoteAndObjective": True,
            "preserveEveryFamilyWhereQuotaAllows": True,
        },
        "labels": labels,
        "objectives": sorted(question_counts),
        "coverage": coverage,
        "counts": {"notes": len(all_notes), "questions": len(all_questions)},
        "levelScale": [1, 5],
        "contentContractVersion": "2.2",
        "contentContractHash": CONTRACT_HASH,
        "visualPolicy": {
            "version": "1.0",
            "everyNote": True,
            "questionMinimumPercent": 0,
            "balancedByObjective": False,
            "preserveAllSourceFigures": False,
            "bySubject": visual_by_subject,
            "rationale": (
                "Her derste görselli sorular seçim sırasında önceliklendirilir. "
                "Bilişim ve Din için 50'şer soruluk kota ile diğer derslerdeki "
                "380 soruluk kota nedeniyle kaynak görsellerin tamamını korumak "
                "mümkün değildir; seçilen hiçbir sorunun kendi görseli çıkarılmaz."
            ),
        },
        "contractPolicy": {
            "questionCount": 2000,
            "perSubjectQuestionCount": subject_counts,
            "idScopeMode": "multi-subject",
            "minFamilies": len(families),
            "maxPerFamily": 8,
            "answerBalance": answer_balance,
            "minFiguredQuestions": figure_count,
            "everyNoteHasFigure": True,
            "objectiveBalanceMode": "coverage",
        },
        "reviewStatus": "pending",
        "humanReviewed": False,
        "publishBlocked": True,
        "disclosure": "ai-generated-and-ai-reviewed-no-human-review",
        "provenance": (
            "machine-compiled:codex-sol:2026-08; "
            "sources=grade6-ai-verified; review=pending"
        ),
    }
    rows = [
        pack,
        *sorted(all_notes, key=lambda row: (row["subject"], row["id"])),
        *sorted(all_questions, key=lambda row: (row["subject"], row["id"])),
    ]
    summary = {
        "notes": len(all_notes),
        "questions": len(all_questions),
        "subjects": subject_counts,
        "answers": answer_balance,
        "families": len(families),
        "figures": figure_count,
        "visualBySubject": visual_by_subject,
        "familiesBySubject": family_by_subject,
    }
    return rows, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    rows, summary = build()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.write:
        write_jsonl(OUTPUT, rows)
        print(OUTPUT.relative_to(ROOT).as_posix())
    else:
        print("(dosyayı yazmak için --write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
