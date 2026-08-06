"""Question Contract 2.2 kuralları (47-56) ve sürüm ayrımı.

Bu testlerin asıl işi, 2.2'nin 2.0'ı BOZMADIĞINI güvence altına almak: iki
sözleşme tek dosyada yan yana yaşıyor ve hints kuralları birbirini iptal
ediyor. Sürüm kapısı kırılırsa yayımlanmış dört paket sessizce 500'er HATA
üretir; bunu ancak bir test yakalar.
"""
import copy
import importlib.util
import json
from pathlib import Path



ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location(
    "pack_validate_c22", ROOT / "tools" / "pack_validate.py"
)
pack_validate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pack_validate)


HIYERARSI = {
    "grade": 5,
    "subject": "Türkçe",
    "unitKey": "okuma",
    "topicKey": "metin-anlama",
    "subtopicKey": "ana-fikir",
    "noteKey": "ana-fikir-nedir",
}
DAMGA = {
    "reviewStatus": "pending",
    "humanReviewed": False,
    "provenance": "machine-generated:test:2026-08",
}
GEREKCELER = [
    "Doğru; metnin tamamını kapsayan tek yargı budur.",
    "Ayrıntıyı ana fikir sanmış: bu cümle yalnız bir örneği anlatır.",
    "Başlığı ana fikir sanmış: başlık konuyu verir, yargıyı değil.",
    "Kendi görüşünü metne yüklemiş: bu yargı metinde geçmez.",
]


def soru(sira: int, dogru: int = 0, aile: str = "ana-fikir-cikarim") -> dict:
    kayit = {
        "type": "question",
        "id": f"tr.g05.tur.ana-fikir.q{sira:03d}",
        "noteId": "tr.g05.tur.ana-fikir.n001",
        "familyId": aile,
        "level": 2,
        "difficultyReason": (
            "İki adım gerekir: yinelenen sözcükleri bulmak ve bunları tek bir "
            "yargıya bağlamak; çeldiriciler ayrıntı cümleleridir."
        ),
        "question": f"Aşağıdaki metnin ana fikri nedir? ({sira})",
        "choices": [f"A{sira}", f"B{sira}", f"C{sira}", f"D{sira}"],
        "correct": dogru,
        "distractorWhy": list(GEREKCELER),
        "explanation": "Her paragraf aynı yargıyı destekler; ana fikir budur.",
        "figure": None,
        "tags": ["ana fikir"],
        "topic": "Metin Anlama",
        "objective": "T.O.5.5.",
        "objectiveSource": "PENDING",
        "objectiveEvidenceId": "T.O.5.5.",
        "sourceRefs": ["PENDING"],
    }
    kayit.update(HIYERARSI)
    kayit.update(DAMGA)
    if dogru:
        kayit["distractorWhy"][0] = GEREKCELER[1]
        kayit["distractorWhy"][dogru] = GEREKCELER[0]
    return kayit


def paket_kaydi() -> dict:
    return {
        "type": "pack",
        "schemaVersion": "2.2",
        "id": "tr.g05.turkce.deneme",
        "version": 1,
        "lang": "tr",
        "country": "TR",
        "curriculum": "MEB-TYMM-2024",
        "subject": "Türkçe",
        "grade": 5,
        "license": "CC-BY-NC-4.0",
        "labels": {"tr.g05.tur.ana-fikir.n001.visual.a1":
                   "İki sütun ve iki satırlık kareli zemin."},
        "source": "deneme",
        "provenance": "machine-generated:test:2026-08",
        "sources": [{"sourceId": "s1", "title": "t",
                     "downloadUrl": "https://ornek.local/y.pdf"}],
        "disclosure": "ai-generated-and-ai-reviewed-no-human-review",
        "publishBlocked": True,
        "contractPolicy": {
            "questionCount": 4,
            "minFamilies": 2,
            "maxPerFamily": 8,
            "answerBalance": [1, 1, 1, 1],
            "minFiguredQuestions": 0,
        },
    }


def not_kaydi() -> dict:
    kayit = {
        "type": "note",
        "id": "tr.g05.tur.ana-fikir.n001",
        "noteId": "tr.g05.tur.ana-fikir.n001",
        "title": "Ana Fikir",
        "body": "Ana fikir, metnin tamamını kapsayan tek yargıdır.",
        "figure": {"kind": "grid", "cols": 2, "rows": 2,
                   "altTextKey": "tr.g05.tur.ana-fikir.n001.visual.a1"},
        "topic": "Metin Anlama",
        "objective": "T.O.5.5.",
        "objectiveSource": "PENDING",
        "objectiveEvidenceId": "T.O.5.5.",
        "sourceRefs": ["PENDING"],
    }
    kayit.update(HIYERARSI)
    kayit.update(DAMGA)
    return kayit


def temiz_paket() -> list:
    return [paket_kaydi(), not_kaydi(),
            soru(1, 0), soru(2, 1),
            soru(3, 2, "ana-fikir-baslik"), soru(4, 3, "ana-fikir-baslik")]


def kosu(tmp_path, kayitlar) -> set:
    """Paketi doğrular ve tetiklenen HATA kural numaralarını döner."""
    yol = tmp_path / "paket.jsonl"
    yol.write_text(
        "\n".join(json.dumps(k, ensure_ascii=False) for k in kayitlar) + "\n",
        encoding="utf-8",
    )
    return {b.kural for b in pack_validate.validate_file(yol)
            if b.seviye == "HATA"}


def test_temiz_22_paketi_hatasiz(tmp_path):
    assert kosu(tmp_path, temiz_paket()) == set()


def test_hints_alani_hata_uretir(tmp_path):
    k = temiz_paket()
    k[2]["hints"] = ["a", "b", "c", "d", "e"]
    assert 56 in kosu(tmp_path, k)


def test_bos_hints_dizisi_de_hata_uretir(tmp_path):
    """Boş dizi 'bu alan var, doldurulmayı bekliyor' der; 2.2'de alan yoktur."""
    k = temiz_paket()
    k[2]["hints"] = []
    assert 56 in kosu(tmp_path, k)


def test_iki_sifir_paketinde_hints_hala_zorunlu(tmp_path):
    """Sürüm kapısı: 2.0'da beş dolu ipucu şarttır ve 46 hiç çalışmaz."""
    k = temiz_paket()
    k[0]["schemaVersion"] = "2.0"
    kurallar = kosu(tmp_path, k)
    assert 17 in kurallar
    assert 56 not in kurallar


def test_hiyerarsi_halkasi_eksikse_hata(tmp_path):
    k = temiz_paket()
    del k[2]["subtopicKey"]
    assert 47 in kosu(tmp_path, k)


def test_anahtar_slug_degilse_hata(tmp_path):
    """Anahtar makine kimliğidir: büyük harf ve alt çizgi kabul edilmez."""
    k = temiz_paket()
    k[2]["topicKey"] = "Metin_Anlama"
    assert 47 in kosu(tmp_path, k)


def test_notekey_noteid_celisirse_hata(tmp_path):
    k = temiz_paket()
    k[2]["noteKey"] = "bambaska-not"
    assert 48 in kosu(tmp_path, k)


def test_familyid_yoksa_hata(tmp_path):
    k = temiz_paket()
    del k[2]["familyId"]
    assert 49 in kosu(tmp_path, k)


def test_aile_tavani_asilirsa_hata(tmp_path):
    k = temiz_paket()
    k[0]["contractPolicy"]["maxPerFamily"] = 1
    assert 49 in kosu(tmp_path, k)


def test_aile_sayisi_yetersizse_hata(tmp_path):
    k = temiz_paket()
    k[0]["contractPolicy"]["minFamilies"] = 99
    assert 50 in kosu(tmp_path, k)


def test_gecici_etiket_soneki_hata(tmp_path):
    """'.repaired' kalıcı veriye bir iş turunun adını yazmaktır."""
    k = temiz_paket()
    k[0]["labels"]["tr.g05.tur.ana-fikir.q001.visual.repaired"] = "x"
    assert 51 in kosu(tmp_path, k)


def test_cevap_dagilimi_bildirileni_tutmuyorsa_hata(tmp_path):
    k = temiz_paket()
    k[3]["correct"] = 0
    k[3]["distractorWhy"] = list(GEREKCELER)
    assert 52 in kosu(tmp_path, k)


def test_gorselli_soru_sayisi_yetersizse_hata(tmp_path):
    k = temiz_paket()
    k[0]["contractPolicy"]["minFiguredQuestions"] = 3
    assert 53 in kosu(tmp_path, k)


def test_notta_gorsel_yoksa_hata(tmp_path):
    k = temiz_paket()
    k[0]["contractPolicy"]["everyNoteHasFigure"] = True
    k[1]["figure"] = None
    assert 53 in kosu(tmp_path, k)


def test_bayat_damga_hata(tmp_path):
    """Şemanın yapamadığı iş: iki hash alanını karşılaştırmak."""
    k = temiz_paket()
    k[2].update(reviewStatus="ai-verified", reviewedBy="gpt-5.6-sol",
                contentHash="sha256:" + "a" * 64,
                reviewedHash="sha256:" + "b" * 64)
    assert 54 in kosu(tmp_path, k)


def test_guncel_damga_gecerli(tmp_path):
    k = temiz_paket()
    for kayit in k[2:]:
        kayit.update(reviewStatus="ai-verified", reviewedBy="gpt-5.6-sol",
                     contentHash="sha256:" + "a" * 64,
                     reviewedHash="sha256:" + "a" * 64)
    assert 54 not in kosu(tmp_path, k)


def test_uretici_kendini_inceleyemez(tmp_path):
    k = temiz_paket()
    k[2].update(reviewStatus="ai-verified", reviewedBy="test",
                contentHash="sha256:" + "a" * 64,
                reviewedHash="sha256:" + "a" * 64)
    assert 54 in kosu(tmp_path, k)


def test_insan_incelemesi_taklit_edilemez(tmp_path):
    k = temiz_paket()
    k[2]["humanReviewed"] = True
    assert 54 in kosu(tmp_path, k)


def test_pending_kaynak_yayini_kilitler(tmp_path):
    """PENDING kaynak varken publishBlocked kapalıysa paket yayına çıkabilirdi."""
    k = temiz_paket()
    k[0]["publishBlocked"] = False
    assert 55 in kosu(tmp_path, k)


def test_beyan_yoksa_hata(tmp_path):
    k = temiz_paket()
    del k[0]["disclosure"]
    assert 55 in kosu(tmp_path, k)


def test_dolu_figurde_alt_metin_zorunlu(tmp_path):
    k = temiz_paket()
    del k[1]["figure"]["altTextKey"]
    assert 4 in kosu(tmp_path, k)


def _paket_surumu(yol: Path) -> str:
    for satir in yol.read_text(encoding="utf-8").splitlines():
        kayit = json.loads(satir)
        if kayit.get("type") == "pack":
            return kayit.get("schemaVersion", "")
    return ""


def test_iki_sifir_paketleri_bozulmadi():
    """2.2 eklemesi 2.0'da kalan paketleri etkilememeli."""
    for ad in ("turkce", "matematik", "fen-bilimleri", "ingilizce"):
        yol = ROOT / "turkiye" / "5-sinif" / ad / f"{ad}-tum.jsonl"
        if _paket_surumu(yol) != "2.0":
            continue
        hatalar = [b for b in pack_validate.validate_file(yol)
                   if b.seviye == "HATA"]
        assert hatalar == [], f"{ad}: {hatalar[:3]}"


def test_turkce_22_borcu_yalniz_gorselde():
    """Türkçe 2.2'ye taşındı; kalan tek borç bildirilen görsel açığıdır.

    Bu test kapıyı açık tutmaz, DARALTIR: görsel dışında herhangi bir kural
    kırmızıya dönerse taşıma bir şeyi bozmuş demektir ve derhâl görünür olur.
    """
    yol = ROOT / "turkiye" / "5-sinif" / "turkce" / "turkce-tum.jsonl"
    if _paket_surumu(yol) != "2.2":
        return
    baska = sorted({b.kural for b in pack_validate.validate_file(yol)
                    if b.seviye == "HATA" and b.kural != 53})
    assert baska == [], f"görsel dışı HATA kuralları: {baska}"
