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


def test_yuzeysel_sik_duzenlemeleri_anlamsal_olarak_esdeger():
    normalize = check_paired_edit.secenekleri_anlamsal_normallestir

    assert normalize(["A) 1.25", "B) daha daha yüksek"]) == normalize(
        ["1,25", "daha yüksek"]
    )


def test_degismeyen_gerekceler_yeni_dogruyu_acikca_kanitlayabilir():
    soru = {
        "choices": ["Sanal Gerçeklik", "Artırılmış Gerçeklik"],
        "correct": 1,
        "explanation": (
            "Artırılmış Gerçeklik, gerçek görüntü üzerine sanal öğe ekler."
        ),
        "distractorWhy": [
            "Sanal gerçeklik gerçek görüntünün yerini alır.",
            "Doğru seçenektir. Artırılmış Gerçeklik gerçek görüntüyü korur.",
        ],
    }

    assert check_paired_edit.dogru_baglami_acikca_tutarli(soru)


def test_eski_indekste_kalan_dogru_etiketi_kabul_edilmez():
    soru = {
        "choices": ["Sanal Gerçeklik", "Artırılmış Gerçeklik"],
        "correct": 1,
        "explanation": "Görüntüleme teknolojileri karşılaştırılır.",
        "distractorWhy": [
            "Doğru seçenektir. Sanal gerçeklik sayısal ortam kurar.",
            "Artırılmış gerçeklik gerçek görüntüyü korur.",
        ],
    }

    assert not check_paired_edit.dogru_baglami_acikca_tutarli(soru)


def test_yanlis_eslestirme_sorusunda_diger_dogrular_isaret_sayilmaz():
    soru = {
        "choices": ["Orman - Mobilya", "Toprak - Turizm"],
        "correct": 1,
        "explanation": "Toprak ile turizm doğrudan ilişkili değildir.",
        "distractorWhy": [
            "Orman mobilyanın ham maddesidir; eşleştirme doğrudur.",
            "Doğru seçenektir. Toprak ile turizm eşleştirmesi yanlıştır.",
        ],
    }

    assert check_paired_edit.dogru_baglami_acikca_tutarli(soru)
