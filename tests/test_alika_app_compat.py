"""Optional end-to-end gate against the real AliKa Windows importer.

Set ``ALIKA_APP_REPO`` to the AliKa application checkout. The test patches all
library paths into ``tmp_path`` and never touches the user's live catalogue.
"""
from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent.parent
EXPECTED = {
    "fen-bilimleri/fen-bilimleri-tum.jsonl": ("Fen Bilimleri", 28, 500),
    "ingilizce/ingilizce-tum.jsonl": ("İngilizce", 24, 500),
    "matematik/matematik-tum.jsonl": ("Matematik", 23, 500),
    "sosyal-bilgiler/sosyal-bilgiler-tum.jsonl": (
        "Sosyal Bilgiler", 19, 500,
    ),
    "turkce/turkce-tum.jsonl": ("Türkçe", 22, 500),
}

ALL_PACKAGES = sorted((ROOT / "turkiye").rglob("*.jsonl"))
ALL_PACKAGE_IDS = [
    path.relative_to(ROOT).with_suffix("").as_posix()
    for path in ALL_PACKAGES
]


def _load_app(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    raw = os.environ.get("ALIKA_APP_REPO", "").strip()
    if not raw:
        pytest.skip("ALIKA_APP_REPO verilmedi; gerçek uygulama kapısı atlandı.")
    windows = Path(raw).resolve() / "windows"
    if not (windows / "library" / "importer.py").is_file():
        pytest.fail(f"AliKa Windows kaynak yolu geçersiz: {windows}")
    monkeypatch.syspath_prepend(str(windows))

    library = importlib.import_module("library")
    values = {
        "LIBRARY_DIR": tmp_path / "library",
        "CATALOG_DB_PATH": tmp_path / "library" / "catalog.db",
        "BLOB_DIR": tmp_path / "library" / "blobs",
        "QUARANTINE_DIR": tmp_path / "library" / "quarantine",
        "WATCHED_FOLDER": tmp_path / "library" / "watched",
    }
    owners = {
        "library": values,
        "library.blob_repo": {
            key: values[key] for key in ("BLOB_DIR", "QUARANTINE_DIR")
        },
        "library.catalog_repo": {
            "CATALOG_DB_PATH": values["CATALOG_DB_PATH"],
        },
        "library.question_repo": {
            "CATALOG_DB_PATH": values["CATALOG_DB_PATH"],
        },
        "library.importer": {
            "QUARANTINE_DIR": values["QUARANTINE_DIR"],
        },
    }
    for module_name, replacements in owners.items():
        module = importlib.import_module(module_name)
        for name, value in replacements.items():
            monkeypatch.setattr(module, name, value, raising=False)
    return library


@pytest.mark.parametrize("path", ALL_PACKAGES, ids=ALL_PACKAGE_IDS)
def test_every_package_round_trips_through_alika(
    path: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """GitHub'daki her paket gerçek AliKa importer'ı ile kurulabilmeli."""
    _load_app(tmp_path, monkeypatch)
    from library import init_all
    from library.catalog_repo import connect
    from library.importer import ImportState, Importer

    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    expected_notes = sum(row.get("type") == "note" for row in records)
    expected_questions = sum(row.get("type") == "question" for row in records)

    init_all.init()
    importer = Importer()
    result = importer.import_file(path)
    relative = path.relative_to(ROOT).as_posix()
    assert result.success, (relative, result.error_code, result.error)
    assert result.state == ImportState.AWAITING_APPROVAL, relative
    assert result.preview["note_count"] == expected_notes, relative
    assert result.preview["question_count"] == expected_questions, relative
    assert importer.approve(result.content_id), relative

    with connect() as connection:
        active_notes = connection.execute(
            "SELECT COUNT(*) FROM content_items "
            "WHERE active=1 AND media_type='note'"
        ).fetchone()[0]
        active_questions = connection.execute(
            "SELECT COUNT(*) FROM question_items WHERE active=1"
        ).fetchone()[0]
        orphan_links = connection.execute(
            "SELECT COUNT(*) FROM question_items q "
            "LEFT JOIN content_items n "
            "ON n.content_id=q.note_content_id AND n.active=1 "
            "WHERE q.active=1 AND (q.note_content_id IS NULL OR n.content_id IS NULL)"
        ).fetchone()[0]
        invalid_answers = connection.execute(
            "SELECT COUNT(*) FROM question_items "
            "WHERE active=1 AND (correct < 0 OR correct > 3)"
        ).fetchone()[0]

    assert active_notes == expected_notes, relative
    assert active_questions == expected_questions, relative
    assert orphan_links == 0, relative
    assert invalid_answers == 0, relative


def test_grade5_packages_round_trip_through_alika(tmp_path, monkeypatch):
    _load_app(tmp_path, monkeypatch)
    from library import init_all
    from library.catalog_repo import connect
    from library.importer import ImportState, Importer

    init_all.init()
    importer = Importer()
    imported: dict[str, str] = {}
    for relative, (subject, note_count, question_count) in EXPECTED.items():
        path = ROOT / "turkiye" / "5-sinif" / relative
        result = importer.import_file(path)
        assert result.success, (relative, result.error_code, result.error)
        assert result.state == ImportState.AWAITING_APPROVAL
        assert result.preview["subject"] == subject
        assert result.preview["note_count"] == note_count
        assert result.preview["question_count"] == question_count
        assert importer.approve(result.content_id), relative
        imported[relative] = result.content_id

    with connect() as connection:
        question_rows = connection.execute(
            "SELECT choices, correct, metadata, note_content_id "
            "FROM question_items WHERE active=1"
        ).fetchall()
        note_rows = connection.execute(
            "SELECT description, provenance FROM content_items "
            "WHERE active=1 AND media_type='note'"
        ).fetchall()
        collection_count = connection.execute(
            "SELECT COUNT(*) FROM question_collections "
            "WHERE active=1 AND trust_state='approved'"
        ).fetchone()[0]

    assert collection_count == 5
    assert len(question_rows) == 2500
    assert len(note_rows) == 116
    for row in question_rows:
        metadata = json.loads(row["metadata"])
        assert len(json.loads(row["choices"])) == 4
        assert 0 <= int(row["correct"]) <= 3
        assert row["note_content_id"]
        assert metadata.get("noteId") == metadata.get("noteKey")
        assert metadata.get("objective")
        assert "hints" not in metadata
        if metadata.get("figure"):
            assert metadata["figure"].get("altTextKey")
    for row in note_rows:
        source = json.loads(row["provenance"])["source_record"]
        assert len(row["description"]) > 500
        assert source.get("noteKey")
        assert source.get("figure", {}).get("altTextKey")

    # Re-import is idempotent and returns the already activated package.
    for relative, content_id in imported.items():
        result = importer.import_file(ROOT / "turkiye" / "5-sinif" / relative)
        assert result.success
        assert result.state == ImportState.ACTIVATED
        assert result.content_id == content_id


def test_grade5_question_bank_round_trip_through_alika(tmp_path, monkeypatch):
    _load_app(tmp_path, monkeypatch)
    from library import init_all
    from library.catalog_repo import connect
    from library.importer import ImportState, Importer

    path = (
        ROOT
        / "turkiye"
        / "5-sinif"
        / "soru-bankasi"
        / "5-sinif-tum-dersler-2000-soru.jsonl"
    )
    init_all.init()
    importer = Importer()
    result = importer.import_file(path)
    assert result.success, (result.error_code, result.error)
    assert result.state == ImportState.AWAITING_APPROVAL
    assert result.preview["subject"] == "Tüm Dersler"
    assert result.preview["note_count"] == 116
    assert result.preview["question_count"] == 2000
    assert importer.approve(result.content_id)

    with connect() as connection:
        questions = connection.execute(
            "SELECT subject, metadata, note_content_id "
            "FROM question_items WHERE active=1"
        ).fetchall()
        notes = connection.execute(
            "SELECT COUNT(*) FROM content_items "
            "WHERE active=1 AND media_type='note'"
        ).fetchone()[0]
        collection = connection.execute(
            "SELECT subject, question_count, trust_state "
            "FROM question_collections WHERE active=1"
        ).fetchone()

    assert notes == 116
    assert len(questions) == 2000
    assert collection["subject"] == "Tüm Dersler"
    assert collection["question_count"] == 2000
    assert collection["trust_state"] == "approved"
    subject_counts: dict[str, int] = {}
    figured = 0
    for row in questions:
        subject_counts[row["subject"]] = subject_counts.get(row["subject"], 0) + 1
        metadata = json.loads(row["metadata"])
        assert row["note_content_id"]
        assert "hints" not in metadata
        if metadata.get("figure"):
            figured += 1
            assert metadata["figure"].get("altTextKey")
    assert subject_counts == {
        "Fen Bilimleri": 400,
        "Matematik": 400,
        "Sosyal Bilgiler": 400,
        "Türkçe": 400,
        "İngilizce": 400,
    }
    assert figured == 477

    # Aynı dosya ikinci kez yüklendiğinde kopya banka oluşturmamalı.
    second = importer.import_file(path)
    assert second.success
    assert second.state == ImportState.ACTIVATED
    assert second.content_id == result.content_id
