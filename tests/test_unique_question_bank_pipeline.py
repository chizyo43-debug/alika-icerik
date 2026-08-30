"""Regression tests for the fail-closed 5–12 unique-bank pipeline."""
from __future__ import annotations

import importlib
from collections import Counter
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parent.parent


sys.path.insert(0, str(ROOT / "tools"))


def load_tool(name: str):
    return importlib.import_module(name)


build = load_tool("build_unique_question_banks")
audit = load_tool("audit_bank_source_readiness")
review = load_tool("review_unique_question_banks")
blueprint_audit = load_tool("audit_question_bank_blueprints")


def rich_note(*, body: str | None = None) -> dict:
    sections = {
        "whatIWillLearn": "Kazanıma bağlı bilgiyi yeni bir durumda açıklayıp değerlendireceğim.",
        "priorKnowledge": "Önceki konuda öğrenilen temel kavramları ve aralarındaki ilişkiyi hatırlarım.",
        "keyConcepts": "Konuya özgü kavramlar, tanımlar, ayırt edici özellikler ve kanıt sınırları. " * 5,
        "steps": "Soruyu belirle, güvenilir kanıt topla, kanıtı ölçütlerle incele ve sonucu gerekçelendir.",
        "workedExamples": ["Ayrıntılı çözümlü örnek ve gerekçeli sonuç. " * 5, "İkinci ayrıntılı örnek ve çözüm. " * 6],
        "commonMistakes": "Yaygın hata, kanıtın desteklediğinden daha geniş bir sonuç çıkarmaktır. " * 2,
        "selfCheck": ["Birinci kontrol?", "İkinci kontrol?", "Üçüncü kontrol?"],
        "summary": "Kavram, kanıt ve sonuç arasındaki bağın kısa özeti burada verilir.",
        "figureNote": "Şekil yalnız süreci gösterir ve doğru cevabı açıklamaz.",
    }
    return {
        "body": body or ("Konuya özgü, açıklamalı ve örnekli ders içeriği. " * 30),
        "lessonSections": sections,
        "objectiveSource": "https://mufredat.meb.gov.tr/ornek.pdf",
        "objectiveEvidenceId": "meb:pdf-page-1",
    }


def test_difficulty_distribution_is_exact_and_deterministically_shuffled() -> None:
    expected = {
        5: {1: 400, 2: 500, 3: 600, 4: 400, 5: 100},
        8: {1: 300, 2: 500, 3: 600, 4: 400, 5: 200},
        11: {1: 200, 2: 400, 3: 600, 4: 500, 5: 300},
    }
    for grade, counts in expected.items():
        first = build.difficulty_schedule(grade)
        assert first == build.difficulty_schedule(grade)
        assert Counter(first) == counts
        assert max(
            sum(1 for _ in group)
            for _, group in __import__("itertools").groupby(first)
        ) < 30


def test_exact_schedule_keeps_duplicate_occurrences_distinct() -> None:
    schedule = build.exact_schedule(100, (0.5, 0.5), ("A", "B"), "regression")
    assert Counter(schedule) == {"A": 50, "B": 50}
    assert schedule != ["A"] * 50 + ["B"] * 50


def test_single_ordinary_phrase_is_not_a_generic_template_failure() -> None:
    note = rich_note(body=("Amaç, yöntem, kanıt ve sonuç ilişkisi konuya özgü örneklerle açıklanır. " * 20))
    assert "generic_template_language" not in audit.note_failures(note)


def test_multiple_high_specificity_template_markers_fail() -> None:
    note = rich_note(
        body=("Çalışma kaydı ve bağlam dizisi kullanılır. " * 25)
    )
    assert "generic_template_language" in audit.note_failures(note)


def test_review_manifest_must_be_bound_to_candidate_hash() -> None:
    with pytest.raises(ValueError, match="not bound"):
        review.verify_external_manifest(
            {
                "schemaVersion": "alika-independent-ai-batch-review/2.0.0",
                "candidateSha256": "stale",
            },
            [],
            "current",
        )


def test_review_manifest_covers_pack_and_notes_not_only_questions() -> None:
    questions = [{"type": "question", "id": f"q{index:04d}"} for index in range(2000)]
    manifest = {
        "schemaVersion": "alika-independent-ai-batch-review/2.0.0",
        "candidateSha256": "candidate",
        "humanReviewed": False,
        "reviewMode": "ai-only",
        "reviewerModel": "independent-reviewer",
        "producer": "producer",
        "batches": [],
    }
    for index in range(20):
        selected = questions[index * 100:(index + 1) * 100]
        manifest["batches"].append({
            "batch": index + 1,
            "decision": "PASS",
            "questionIds": [row["id"] for row in selected],
            "contentProjectionSha256": review.batch_digest(selected),
            "knownErrors": 0,
            "knownWarnings": 0,
        })
    with pytest.raises(ValueError, match="supporting record decisions"):
        review.verify_external_manifest(
            manifest,
            questions,
            "candidate",
            [{"type": "pack", "id": "pack-1"}],
        )


def test_future_curriculum_sources_fail_closed() -> None:
    assert {8, 12} <= set(build.CURRENT_CURRICULUM_BLOCKS)


def test_current_authored_blueprints_pass_strict_partial_audit() -> None:
    result = blueprint_audit.audit(5)
    assert result["questions"] >= 100
    assert result["status"] == "PASS", result["errors"][:5]


def test_complete_grade5_pack_declares_every_covered_objective() -> None:
    rows, _ = build.build_grade(5)
    pack = rows[0]
    assert pack["objectives"] == sorted(pack["coverage"])
    assert set(pack["objectives"]) == {
        build.objective_of(row) for row in rows if row.get("type") == "question"
    }
