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
