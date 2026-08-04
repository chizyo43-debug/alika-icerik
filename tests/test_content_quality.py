"""AliKa içerik deposu kalite testleri.

Çalıştırma:
    cd icerik
    python -m pytest tests/ -q

Testler:
1. Tüm paketler doğrulayıcıdan geçer (0 HATA)
2. Şema V2 alanları mevcut
3. Cevap dağılımı dengeli (%35 eşiği)
4. difficultyReason spesifik (≥20 karakter)
5. Duplikasyon yok (pack ID tekil)
6. Soru sayısı tutarlı (≥90/paket)
7. Zorluk dağılımı makul (her seviyede ≥%15)
"""
import json
import sys
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TURKIYE = ROOT / "turkiye" / "5-sinif"

# Depoyla birlikte sürümlenen doğrulayıcıyı yükle. Testler temiz bir klonda,
# çalışma alanının dışında başka bir repoya ihtiyaç duymadan çalışmalıdır.
sys.path.insert(0, str(ROOT / "tools"))
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "pack_validate", ROOT / "tools" / "pack_validate.py")
pack_validate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pack_validate)


def get_all_packages():
    """Tüm .jsonl dosyalarını bul."""
    return sorted(TURKIYE.rglob("*.jsonl"))


def load_package(path):
    """Paketi yükle: (pack, notes, questions)."""
    lines = path.read_text(encoding="utf-8").strip().split("\n")
    pack = None
    notes = []
    questions = []
    for l in lines:
        obj = json.loads(l)
        t = obj.get("type", "")
        if t == "pack":
            pack = obj
        elif t == "note":
            notes.append(obj)
        elif t == "question":
            questions.append(obj)
    return pack, notes, questions


PACKAGES = get_all_packages()
PACKAGE_IDS = [p.stem for p in PACKAGES]


class TestValidator:
    """Doğrulayıcı tabanlı testler."""

    @pytest.mark.parametrize("path", PACKAGES, ids=PACKAGE_IDS)
    def test_sifir_hata(self, path):
        """Her paket 0 HATA ile doğrulayıcıdan geçmeli."""
        bulgular = pack_validate.validate_file(path)
        hatalar = [b for b in bulgular if b.seviye == "HATA"]
        assert hatalar == [], f"HATA: {hatalar}"


class TestSchemaV2:
    """Şema V2 alan testleri."""

    @pytest.mark.parametrize("path", PACKAGES, ids=PACKAGE_IDS)
    def test_pack_v2_alanlari(self, path):
        pack, _, _ = load_package(path)
        assert pack is not None
        assert pack.get("schemaVersion") == "2.0"
        assert pack.get("source"), "source boş"
        assert pack.get("provenance"), "provenance boş"
        assert pack.get("objectives"), "objectives boş"

    @pytest.mark.parametrize("path", PACKAGES, ids=PACKAGE_IDS)
    def test_soru_v2_alanlari(self, path):
        _, _, questions = load_package(path)
        for q in questions:
            assert q.get("difficultyReason"), f"{q['id']}: difficultyReason yok"
            assert len(q["difficultyReason"]) >= 20, f"{q['id']}: DR çok kısa"
            assert q.get("reviewStatus") in (
                "pending", "reviewed", "ai-verified", "rejected"
            ), \
                f"{q['id']}: reviewStatus geçersiz"
            assert q.get("provenance"), f"{q['id']}: provenance yok"


class TestQuality:
    """Kalite metrik testleri."""

    @pytest.mark.parametrize("path", PACKAGES, ids=PACKAGE_IDS)
    def test_cevap_dagilimi(self, path):
        """Doğru cevap konumu %35'i aşmamalı."""
        _, _, questions = load_package(path)
        if len(questions) < 10:
            pytest.skip("Yetersiz soru")
        konumlar = Counter(q["correct"] for q in questions)
        for konum, adet in konumlar.items():
            pct = adet / len(questions) * 100
            assert pct <= 35, f"Konum {konum}: %{pct:.1f} > %35"

    @pytest.mark.parametrize("path", PACKAGES, ids=PACKAGE_IDS)
    def test_zorluk_dagilimi(self, path):
        """Her zorluk seviyesi en az %15 olmalı."""
        _, _, questions = load_package(path)
        levels = Counter(q.get("level", 0) for q in questions)
        for lvl in (1, 2, 3):
            pct = levels.get(lvl, 0) / len(questions) * 100
            assert pct >= 15, f"L{lvl}: %{pct:.1f} < %15"

    @pytest.mark.parametrize("path", PACKAGES, ids=PACKAGE_IDS)
    def test_min_soru_sayisi(self, path):
        """Her pakette en az 90 soru olmalı."""
        _, _, questions = load_package(path)
        assert len(questions) >= 90, f"Soru sayısı: {len(questions)}"

    @pytest.mark.parametrize("path", PACKAGES, ids=PACKAGE_IDS)
    def test_min_not_sayisi(self, path):
        """Her pakette en az 9 not olmalı."""
        _, notes, _ = load_package(path)
        assert len(notes) >= 9, f"Not sayısı: {len(notes)}"


class TestIntegrity:
    """Bütünlük testleri."""

    def test_pack_id_tekil(self):
        """Aynı pack ID birden fazla dosyada olmamalı."""
        ids = []
        for path in PACKAGES:
            pack, _, _ = load_package(path)
            if pack:
                ids.append(pack["id"])
        dupes = [i for i, c in Counter(ids).items() if c > 1]
        assert dupes == [], f"Duplikat pack ID: {dupes}"

    def test_soru_id_tekil(self):
        """Tüm soru ID'leri depo genelinde tekil olmalı."""
        all_ids = []
        for path in PACKAGES:
            _, _, questions = load_package(path)
            all_ids.extend(q["id"] for q in questions)
        dupes = [i for i, c in Counter(all_ids).items() if c > 1]
        assert dupes == [], f"Duplikat soru ID ({len(dupes)}): {dupes[:5]}"

    @pytest.mark.parametrize("path", PACKAGES, ids=PACKAGE_IDS)
    def test_noteid_baglanti(self, path):
        """Her sorunun noteId'si paketteki bir nota işaret etmeli."""
        _, notes, questions = load_package(path)
        note_ids = {n["id"] for n in notes}
        for q in questions:
            nid = q.get("noteId")
            if nid:
                assert nid in note_ids, f"{q['id']}: noteId={nid} bulunamadı"
