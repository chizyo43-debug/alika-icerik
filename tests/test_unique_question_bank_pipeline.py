"""Regression tests for the fail-closed 5–12 unique-bank pipeline."""
from __future__ import annotations

import importlib
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys
import wave

import pytest


ROOT = Path(__file__).resolve().parent.parent


sys.path.insert(0, str(ROOT / "tools"))


def load_tool(name: str):
    return importlib.import_module(name)


build = load_tool("build_unique_question_banks")
audit = load_tool("audit_bank_source_readiness")
review = load_tool("review_unique_question_banks")
blueprint_audit = load_tool("audit_question_bank_blueprints")
pack_validate = load_tool("pack_validate")
audio_validate = load_tool("validate_audio_assets")


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


def test_active_current_curriculum_sources_are_unblocked() -> None:
    activation = json.loads(
        (build.ROOT / "curriculum/tr-2026-2027-activation.json").read_text(encoding="utf-8")
    )
    assert not build.CURRENT_CURRICULUM_BLOCKS
    for grade in (8, 12):
        assert activation["grades"][str(grade)]["repositorySourceStatus"] == "eligible"
        assert activation["grades"][str(grade)]["registry"]


def test_current_authored_blueprints_pass_strict_partial_audit() -> None:
    result = blueprint_audit.audit(5)
    assert result["questions"] >= 100
    assert result["status"] == "PASS", result["errors"][:5]


def test_grade6_note_only_batches_pass_strict_partial_audit() -> None:
    result = blueprint_audit.audit(6)
    assert result["questions"] == 2000
    assert result["questions"] % 100 == 0
    assert result["subjects"]["Bilişim Teknolojileri ve Yazılım"] == 293
    assert result["subjects"]["Din Kültürü ve Ahlak Bilgisi"] == 239
    assert result["subjects"]["Fen Bilimleri"] >= 381
    assert result["subjects"]["İngilizce"] >= 247
    assert result["subjects"]["Matematik"] == 285
    assert result["subjects"]["Sosyal Bilgiler"] == 239
    assert result["subjects"]["Türkçe"] == 316
    assert result["embeddedSourceRoots"] == 0
    assert result["status"] == "PASS", result["errors"][:5]


def test_published_grade5_bank_matches_current_canonical_objectives() -> None:
    rows, metrics = build.build_grade(5)
    assert len([row for row in rows if row.get("type") == "question"]) == 2000
    assert metrics["exactSourceIdOverlap"] == 0
    assert metrics["nearCopyAbove088"] == 0
    turkish = next(item for item in build.discover(5) if item.subject == "Türkçe")
    assert {"T.O.5.15.", "T.Y.5.20."} <= set(turkish.by_objective)


def test_choice_uniqueness_does_not_mask_numbers_or_proper_names() -> None:
    choices = ["Asya", "Avrupa", "Afrika", "Türkiye"]
    assert len({blueprint_audit.literal_choice_key(value) for value in choices}) == 4
    numeric = ["12", "18", "24", "30"]
    assert len({blueprint_audit.literal_choice_key(value) for value in numeric}) == 4


def test_mechanical_distractors_and_answer_coding_charts_are_rejected() -> None:
    assert blueprint_audit.mechanical_distractor(
        "Asya değildir; verilen koşullarda karşıt ilişki geçerlidir"
    )
    labels = {"c1": "Asya", "c2": "Avrupa", "c3": "Afrika", "c4": "Türkiye"}
    figure = {
        "kind": "chart", "style": "bar",
        "categoryKeys": ["c1", "c2", "c3", "c4"],
        "values": [100, 60, 50, 40], "altTextKey": "alt",
    }
    assert blueprint_audit.chart_encodes_choices(
        figure, ["Asya", "Avrupa", "Afrika", "Türkiye"], labels
    )


def test_audio_assets_may_vary_inside_family_but_not_cross_families(tmp_path: Path) -> None:
    audio_dir = tmp_path / "assets" / "audio"
    audio_dir.mkdir(parents=True)
    assets = []
    for index in (1, 2):
        path = audio_dir / f"prompt-{index}.wav"
        with wave.open(str(path), "wb") as output:
            output.setnchannels(1)
            output.setsampwidth(2)
            output.setframerate(8000)
            output.writeframes(b"\x00\x00" * 800)
        assets.append({
            "assetId": f"prompt.{index}",
            "path": f"assets/audio/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "mimeType": "audio/wav",
            "bytes": path.stat().st_size,
            "durationMs": 100,
            "sampleRate": 8000,
            "channels": 1,
            "sampleWidthBits": 16,
            "language": "en-US",
            "speaker": "synthetic-test",
            "redistributionReviewStatus": "approved",
            "transcript": f"Neutral prompt number {index}",
        })
    questions = [
        {
            "type": "question", "id": f"q{index}", "familyId": "family.one",
            "mediaRequirement": "audio-required", "correctOption": "Supported answer",
            "choices": ["Supported answer", "Wrong one", "Wrong two", "Wrong three"],
            "audio": {
                "assetId": f"prompt.{index}", "role": "prompt", "playbackRequired": True,
                "contentSha256": assets[index - 1]["sha256"],
            },
        }
        for index in (1, 2)
    ]
    questions_path = tmp_path / "questions.jsonl"
    manifest_path = tmp_path / "audio-assets.json"
    questions_path.write_text(
        "\n".join(json.dumps(row) for row in questions) + "\n", encoding="utf-8"
    )
    manifest_path.write_text(
        json.dumps({"assetCount": 2, "assets": assets}), encoding="utf-8"
    )
    assert audio_validate.validate(questions_path, manifest_path)["status"] == "PASS"

    questions[1]["familyId"] = "family.two"
    questions[1]["audio"]["assetId"] = "prompt.1"
    questions[1]["audio"]["contentSha256"] = assets[0]["sha256"]
    questions_path.write_text(
        "\n".join(json.dumps(row) for row in questions) + "\n", encoding="utf-8"
    )
    manifest_path.write_text(
        json.dumps({"assetCount": 1, "assets": assets[:1]}), encoding="utf-8"
    )
    report = audio_validate.validate(questions_path, manifest_path)
    assert report["status"] == "FAIL"
    assert any("audio-asset-reused-across-question-families" in error for error in report["errors"])


def test_consented_primary_voice_contract_is_accepted(tmp_path: Path) -> None:
    audio_dir = tmp_path / "assets" / "audio"
    audio_dir.mkdir(parents=True)
    path = audio_dir / "prompt.wav"
    with wave.open(str(path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(48000)
        output.writeframes(b"\x01\x00" * 4800)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    asset = {
        "assetId": "primary.prompt",
        "path": "assets/audio/prompt.wav",
        "sha256": digest,
        "mimeType": "audio/wav",
        "bytes": path.stat().st_size,
        "durationMs": 100,
        "sampleRate": 48000,
        "channels": 1,
        "sampleWidthBits": 16,
        "language": "en-US",
        "speaker": {
            "kind": "consented-human-voice-clone",
            "voiceProfileId": "alika-primary-woman-v1",
            "rightsRecordId": "voice-rights-alika-primary-woman-v1",
            "referenceSha256": "3ead7d03d36780933b0acb326e9a8eaf9ee443ad0a440e9b23ca8cccbdaa093e",
        },
        "licenseStatus": "voice-owner-authorized-commercial-use",
        "redistributionReviewStatus": "approved-project-owner-attestation",
        "transcript": "A neutral listening prompt.",
    }
    question = {
        "type": "question", "id": "q-primary", "familyId": "family.primary",
        "mediaRequirement": "audio-required", "correctOption": "Supported answer",
        "choices": ["Supported answer", "Wrong one", "Wrong two", "Wrong three"],
        "audio": {
            "assetId": "primary.prompt", "role": "prompt", "playbackRequired": True,
            "contentSha256": digest,
        },
    }
    questions_path = tmp_path / "questions.jsonl"
    manifest_path = tmp_path / "audio-assets.json"
    questions_path.write_text(json.dumps(question) + "\n", encoding="utf-8")
    manifest_path.write_text(
        json.dumps({"assetCount": 1, "assets": [asset]}), encoding="utf-8"
    )
    assert audio_validate.validate(questions_path, manifest_path)["status"] == "PASS"

    asset["speaker"].pop("rightsRecordId")
    manifest_path.write_text(
        json.dumps({"assetCount": 1, "assets": [asset]}), encoding="utf-8"
    )
    report = audio_validate.validate(questions_path, manifest_path)
    assert report["status"] == "FAIL"
    assert any("speaker-rightsRecordId-missing" in error for error in report["errors"])


def test_source_root_copy_inside_a_longer_composite_is_rejected() -> None:
    source = (
        "Bir akıllı saat sensörle ölçtüğü adım sayısını internet üzerinden "
        "telefondaki sağlık uygulamasına aktarıyor. Bu teknoloji hangisidir?"
    )
    composite = f"I. problem: {source} Önerilen yanıt: Nesnelerin interneti. II. problem: başka durum."
    assert blueprint_audit.source_stem_embedded(source, composite)
    assert not blueprint_audit.source_stem_embedded("Bu nedir?", composite)


def test_two_card_truth_table_is_one_cognitive_archetype() -> None:
    row = {
        "question": "I. problem için bir yanıt, II. problem için başka bir yanıt verilmiştir.",
        "choices": [
            "I. kart onaylanmalı, II. kart düzeltilmelidir.",
            "I. kart ve II. kart onaylanmalıdır.",
            "I. kart ve II. kart düzeltilmelidir.",
            "II. kart onaylanmalı, I. kart düzeltilmelidir.",
        ],
    }
    assert blueprint_audit.cognitive_archetype(row) == "two-source-answer-audit"


def test_required_table_must_not_duplicate_the_question_evidence() -> None:
    labels = {
        "cell": "Deney grubunda sıcaklık 20 °C'den 35 °C'ye çıkınca çözünme hızı arttı."
    }
    figure = {"kind": "table", "rows": [[{"key": "cell"}]]}
    root = "Tabloyu inceleyiniz. Deney grubunda sıcaklık 20 °C'den 35 °C'ye çıkınca çözünme hızı arttı."
    assert blueprint_audit.required_table_duplicates_question(figure, root, labels)


def test_source_answer_index_leak_and_turkish_english_wrapper_are_rejected() -> None:
    assert blueprint_audit.explanation_leaks_numeric_answer_position(
        "Kaynak çözümde doğru seçenek 3 olarak verilmiştir."
    )
    assert blueprint_audit.english_root_is_turkish_meta_wrapper(
        "İki kartı inceleyiniz. Hangi değerlendirme doğrudur?"
    )
    assert not blueprint_audit.english_root_is_turkish_meta_wrapper(
        "Which sentence correctly completes the dialogue and explains why?"
    )


def test_grade6_batch_declares_multiple_capped_authoring_templates() -> None:
    result = blueprint_audit.audit(6)
    assert result["authoringTemplates"]
    assert max(result["authoringTemplates"].values()) <= 10


def test_reusable_mixed_batch_builder_scopes_ids_to_the_requested_batch() -> None:
    module = load_tool("author_grade6_mixed_batch03")
    note = {
        "id": "note", "title": "Doğru Sözlülük", "objectives": ["DKAB.6.3.1"],
        "unitKey": "u", "topicKey": "t", "subtopicKey": "s", "topic": "ahlak",
        "objectiveSource": "meb", "objectiveEvidenceId": "page", "sourceRefs": [],
    }
    case = (
        "note", "Bir öğrenci bulduğu eşyayı sahibine veriyor.",
        "Eşyanın sahibi doğru bilgi sayesinde bulunuyor.",
        "Doğru sözlülük güven oluşturur.", "Gerçeği açıkça söylemek gerekir.",
        "Güvenin doğru bilgiyle kurulduğu görülür.",
        ["Gerçek saklanmalıdır.", "Yalan güveni artırır.", "Doğruluk yalnız ödül varsa gerekir."],
        "Doğru söz ve davranış güven ilişkisini korur.",
    )
    row = module.make_question(
        1, case, "comprehension", 1, note, {}, "Din Kültürü ve Ahlak Bilgisi",
        batch_number=4, number_base=300,
    )
    assert row["id"] == "tr-g06-bank-dkab-b04-q001"
    assert row["questionNumber"] == 301
    assert row["authoringTemplateId"].startswith("g6-b04-")


def test_note_only_canonical_objective_is_not_dropped_from_quota_universe() -> None:
    science = next(item for item in build.discover(6) if item.subject == "Fen Bilimleri")
    assert "FB.6.4.1.2" in science.by_objective
    assert science.by_objective["FB.6.4.1.2"] == []
    quotas = build.objective_quotas(science, build.subject_quotas(build.discover(6))[science.subject])
    assert quotas["FB.6.4.1.2"] >= 2


def test_grade6_science_case_library_covers_all_canonical_note_objectives() -> None:
    cases = load_tool("author_grade6_fen_case_library").FEN_CASES
    science = next(item for item in build.discover(6) if item.subject == "Fen Bilimleri")
    case_notes = {case[0] for case in cases}
    assert len(cases) == 36
    assert case_notes == {str(note["id"]) for note in science.notes}


def test_grade6_batch12_recomputes_all_authored_math_facts() -> None:
    load_tool("author_grade6_english_math_batch12").verify_math_facts()


def test_grade6_batch13_recomputes_math_facts_and_routes_twenty_diagrams() -> None:
    module = load_tool("author_grade6_math_batch13")
    module.verify_math_facts()
    tasks = [item for builder in module.TASK_BUILDERS for item in builder()]
    assert sum(bool(item.get("figure_kind")) for item in tasks) == 20


def test_grade6_batch14_recomputes_math_facts_and_uses_canonical_figures() -> None:
    module = load_tool("author_grade6_math_batch14")
    module.verify_math_facts()
    tasks = [item for builder in module.TASK_BUILDERS for item in builder()]
    assert len(tasks) == 100
    assert sum(bool(item.get("figure_kind")) for item in tasks) == 43
    assert {"diagram", "table", "chart"}.issubset({
        module.diagram_figure("tr-g06-bank-matematik-b14-q003", {}, "triangle")["kind"],
        module.tabular_figure("tr-g06-bank-matematik-b14-q085", {}, "data-table")["kind"],
        module.tabular_figure("tr-g06-bank-matematik-b14-q096", {}, "bar-chart")["kind"],
    })


def test_grade6_batch15_finishes_math_quota_and_avoids_unreviewed_real_maps() -> None:
    module = load_tool("author_grade6_math_social_batch15")
    module.verify_math_facts()
    tasks = [item for builder in module.TASK_BUILDERS for item in builder()]
    assert len(tasks) == 100
    assert sum(item["note"].startswith("tr-g06-matematik") for item in tasks) == 45
    assert sum(item["note"].startswith("tr-g06-sosyal-bilgiler") for item in tasks) == 55
    assert not any(item.get("figure_kind") == "map" for item in tasks)
    assert {item.get("figure_kind") for item in tasks if item.get("figure_kind")} <= {
        "table", "chart", "coordinate",
    }


def test_grade6_batch16_uses_timeline_flow_table_without_unreviewed_maps() -> None:
    module = load_tool("author_grade6_social_batch16")
    tasks = [item for builder in module.TASK_BUILDERS for item in builder()]
    assert len(tasks) == 100
    assert {item.get("figure_kind") for item in tasks if item.get("figure_kind")} <= {
        "table", "flow", "timeline",
    }
    assert sum(bool(item.get("visual_payload")) for item in tasks) == 22
    assert not any(item.get("figure_kind") == "map" for item in tasks)


def test_grade6_batch17_finishes_social_quota_and_starts_turkish() -> None:
    module = load_tool("author_grade6_social_turkish_batch17")
    tasks = [item for builder in module.TASK_BUILDERS for item in builder()]
    assert len(tasks) == 100
    assert sum(item["note"].startswith("tr-g06-sosyal-bilgiler") for item in tasks) == 84
    assert sum(item["note"].startswith("tr-g06-turkce") for item in tasks) == 16
    assert not any(item.get("figure_kind") == "map" for item in tasks)


def test_grade6_batch18_adds_one_hundred_non_decorative_turkish_questions() -> None:
    module = load_tool("author_grade6_turkish_batch18")
    tasks = [item for builder in module.TASK_BUILDERS for item in builder()]
    assert len(tasks) == 100
    assert all(item["note"].startswith("tr-g06-turkce") for item in tasks)
    assert all(not item.get("figure_kind") for item in tasks)


def test_grade6_batch19_adds_one_hundred_more_turkish_questions() -> None:
    module = load_tool("author_grade6_turkish_batch19")
    tasks = [item for builder in module.TASK_BUILDERS for item in builder()]
    assert len(tasks) == 100
    assert all(item["note"].startswith("tr-g06-turkce") for item in tasks)
    assert all(not item.get("figure_kind") for item in tasks)


def test_grade6_batch20_completes_bank_with_balanced_non_decorative_turkish_questions() -> None:
    module = load_tool("author_grade6_turkish_batch20")
    tasks = [item for builder in module.TASK_BUILDERS for item in builder()]
    assert len(tasks) == 100
    assert all(item["note"].startswith("tr-g06-turkce") for item in tasks)
    assert all(not item.get("figure_kind") for item in tasks)
    assert Counter(item["mode"] for item in tasks) == {
        "comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15,
    }


def test_figure_spec_13_diagram_and_timeline_validate_with_legacy_support() -> None:
    diagram = {
        "kind": "diagram", "viewBox": [0, 0, 100, 60],
        "elements": [
            {"type": "circle", "style": "sun", "x": 12, "y": 30, "r": 8},
            {"type": "line", "style": "ray", "x1": 20, "y1": 30, "x2": 80, "y2": 30},
        ],
        "altTextKey": "alt",
    }
    timeline = {
        "kind": "timeline", "orientation": "horizontal",
        "events": [
            {"id": "e1", "position": 0.2, "labelKey": "event.1"},
            {"id": "e2", "position": 0.8, "labelKey": "event.2"},
        ],
        "altTextKey": "alt",
    }
    legacy = {
        "kind": "diagram",
        "nodes": [{"id": "n1", "labelKey": "n1", "shape": "rect", "x": 20, "y": 20}],
        "edges": [], "altTextKey": "alt",
    }
    assert pack_validate.figur_kontrol(diagram, "2.0") == []
    assert pack_validate.figur_kontrol(timeline, "2.0") == []
    assert pack_validate.figur_kontrol(legacy, "2.0") == []


def test_figure_spec_13_map_release_guards_fail_closed() -> None:
    schematic = {
        "kind": "map", "mapType": "schematic",
        "regions": [{"id": "r1", "points": [[5, 5], [80, 5], [50, 50]]}],
        "altTextKey": "alt", "notToScale": True,
    }
    assert pack_validate.figur_kontrol(schematic, "2.0") == []
    political = {**schematic, "mapType": "political"}
    findings = pack_validate.figur_kontrol(political, "2.0")
    assert any("sınır veri" in finding for finding in findings)
    assert any("passed-human" in finding for finding in findings)
