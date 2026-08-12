"""Bağlı alan denetçisinin şık karşılaştırma regresyonları."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location(
    "check_paired_edit", ROOT / "tools" / "check_paired_edit.py"
)
check_paired_edit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_paired_edit)


def test_sayisal_sik_ayni_gorunen_metne_tasininca_esdeger():
    normalize = check_paired_edit.secenekleri_karsilastirma_icin_normallestir

    assert normalize([48, 24, 12.5, -3]) == ["48", "24", "12.5", "-3"]
    assert normalize([48, 24, 12.5, -3]) == normalize(
        ["48", "24", "12.5", "-3"]
    )


def test_gercek_sik_degisikligi_esdeger_sayilmaz():
    normalize = check_paired_edit.secenekleri_karsilastirma_icin_normallestir

    assert normalize([48, 24, 12, 14]) != normalize(["48", "25", "12", "14"])
    assert normalize([True, None, {"value": 1}]) == [True, None, {"value": 1}]
