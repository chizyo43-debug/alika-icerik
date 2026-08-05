import importlib.util
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location(
    "pack_validate_quality", ROOT / "tools" / "pack_validate.py"
)
pack_validate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pack_validate)

REPAIR_SPEC = importlib.util.spec_from_file_location(
    "repair_english_v3_test", ROOT / "tools" / "repair_english_v3.py"
)
repair_english_v3 = importlib.util.module_from_spec(REPAIR_SPEC)
REPAIR_SPEC.loader.exec_module(repair_english_v3)

ENGLISH_PACKAGE = (
    ROOT / "turkiye" / "5-sinif" / "ingilizce" / "ingilizce-tum.jsonl"
)


def load_english():
    rows = [
        json.loads(line)
        for line in ENGLISH_PACKAGE.read_text(encoding="utf-8").splitlines()
    ]
    pack = next(row for row in rows if row.get("type") == "pack")
    questions = [row for row in rows if row.get("type") == "question"]
    return pack, questions


def test_iskelet_imzasi_sablonu_kok_kopyasindan_ayirir():
    """Tırnak, sayı ve kökten kopyalanan sözcükler maskelenince şablon görünür.

    Eski sürüm sabit cümle listesi tutuyordu; yalnız o turda düzeltilen tam
    ifadeyi yakalıyordu. İmza yaklaşımı ifadeden bağımsızdır.
    """
    kok = "Boşluğu doğru tamamla: “He ___ a jumper.”"
    a = pack_validate.iskelet_imzasi(
        "Öğrencinin “He ___ a jumper.” görevi için jumper, tamamla "
        "kanıtlarını kullanarak seçenekleri karşılaştırmasını gerektirir.", kok)
    b = pack_validate.iskelet_imzasi(
        "Öğrencinin “She ___ a skirt.” görevi için skirt, tamamla "
        "kanıtlarını kullanarak seçenekleri karşılaştırmasını gerektirir.",
        "Boşluğu doğru tamamla: “She ___ a skirt.”")
    assert a == b, "aynı şablonun iki örneği aynı imzayı vermeli"

    farkli = pack_validate.iskelet_imzasi(
        "2 adım: payda eşitleme ve toplama; ön bilgi EKOK; çeldiriciler yakın.",
        kok)
    assert farkli != a, "somut gerekçe şablon imzasıyla çakışmamalı"


def test_difficulty_reason_yigilmasi_hata_verir(tmp_path):
    """Uzunluk kuralını (32) geçen ama tek iskelete yığılan gerekçe kural 37."""
    rows = _paket_iskeleti()
    for i in range(60):
        rows.append(_soru(
            i,
            difficultyReason=(
                "Öğrencinin görevi için kanıtları kullanarak seçenekleri "
                "karşılaştırmasını gerektirir; tema sözcüğü yetmez."
            ),
        ))
    yol = tmp_path / "yigilma.jsonl"
    yol.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8")
    bulgular = pack_validate.validate_file(yol)
    k37 = [b for b in bulgular if b.kural == 37 and b.seviye == "HATA"]
    assert k37, "tek iskelete yığılan difficultyReason HATA vermeli"


def test_cesitli_difficulty_reason_temiz_gecer(tmp_path):
    """Soruya özgü gerekçeler kural 37'yi tetiklememeli (yanlış pozitif yok)."""
    rows = _paket_iskeleti()
    adimlar = [
        "payda eşitleme", "basamak ayrımı", "birim çevirme", "oran kurma",
        "alan hesabı", "çevre toplama", "açı ölçme", "veri okuma",
        "olasılık kurma", "örüntü sürdürme", "sadeleştirme", "tahmin etme",
    ]
    onbilgiler = [
        "EKOK", "basamak değeri", "uzunluk birimleri", "kesir kavramı",
        "dikdörtgen özellikleri", "açı türleri", "sıklık tablosu",
        "eş olasılık", "kural bulma", "bölme", "çarpım tablosu", "yuvarlama",
    ]
    for i in range(60):
        rows.append(_soru(
            i,
            difficultyReason=(
                f"{i % 3 + 1} adım: {adimlar[i % 12]} ve kontrol; "
                f"ön bilgi {onbilgiler[(i + 5) % 12]}; "
                f"çeldiriciler {'yakın' if i % 2 else 'belirgin'}."
            ),
            distractorWhy=[
                "doğru",
                f"{adimlar[i % 12]} adımını atlamış",
                f"{onbilgiler[(i + 5) % 12]} bilgisini yanlış uygulamış",
                f"işlem sırasını {adimlar[(i + 3) % 12]} ile karıştırmış",
            ],
        ))
    yol = tmp_path / "cesitli.jsonl"
    yol.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8")
    bulgular = pack_validate.validate_file(yol)
    k37 = [b for b in bulgular if b.kural == 37 and b.seviye == "HATA"]
    assert not k37, f"çeşitli gerekçeler HATA vermemeli: {k37}"


def _paket_iskeleti() -> list:
    return [
        {
            "type": "pack", "schemaVersion": "2.0", "id": "tr.g05.test",
            "lang": "tr", "country": "TR", "curriculum": "MEB-TYMM-2024",
            "subject": "Test", "grade": 5, "theme": "Test", "labels": {},
            "license": "CC-BY-NC-4.0", "source": "quality-test",
            "provenance": "machine-generated:test:2026-08",
            "objectives": ["OBJ"],
            "coverage": {"OBJ": {"notes": ["tr.g05.test.n001"]}},
        },
        {
            "type": "note", "id": "tr.g05.test.n001", "subject": "Test",
            "topic": "Konu", "title": "Not", "body": "Gövde.", "figure": None,
            "objectives": ["OBJ"],
        },
    ]


def _soru(i: int, **ustyaz) -> dict:
    kayit = {
        "type": "question", "id": f"tr.g05.test.q{i:03d}", "subject": "Test",
        "topic": "Konu", "noteId": "tr.g05.test.n001", "objective": "OBJ",
        "objectiveSource": "https://tymm.meb.gov.tr/program.pdf",
        "level": 2,
        "difficultyReason": "2 adım; ön bilgi: temel kavram; çeldirici yakın.",
        "question": f"{i} sayısının bir fazlası kaçtır?",
        "choices": [f"{i + 1}", f"{i + 2}", f"{i - 1}", f"{i + 10}"],
        "correct": 0,
        "distractorWhy": ["doğru", f"iki fazlası {i + 2}",
                          f"bir eksiği {i - 1}", f"on fazlası {i + 10}"],
        "explanation": f"{i} sayısına 1 eklenir.",
        "figure": None,
        "hints": [f"{i} sayısını bul.", "Bir ekle.", "Sonucu kontrol et.",
                  "Seçenekleri karşılaştır.", "Toplamayı tekrar yap."],
        "reviewStatus": "pending",
        "provenance": "machine-generated:test:2026-08",
    }
    kayit.update(ustyaz)
    return kayit


def test_dominant_hints_and_closed_choice_pool_are_reported(tmp_path):
    rows = [
        {
            "type": "pack",
            "schemaVersion": "2.0",
            "id": "tr.g05.test",
            "lang": "tr",
            "source": "quality-test",
            "provenance": "machine-generated:test:2026-08",
            "coverage": {"OBJ": {"notes": ["tr.g05.test.n001"]}},
            "labels": {},
        },
        {
            "type": "note",
            "id": "tr.g05.test.n001",
            "topic": "Test",
            "body": "Deneme notu.",
            "figure": None,
        },
    ]
    for index in range(20):
        rows.append(
            {
                "type": "question",
                "id": f"tr.g05.test.q{index + 1:03d}",
                "topic": "Test",
                "question": f"{index + 1}. bağlama göre doğru sınıf hangisidir?",
                "choices": ["doğru sınıf", "yanlış yer", "yanlış zaman", "It are"],
                "correct": 0,
                "distractorWhy": [
                    "Doğrudur; bağlamdaki sınıf bilgisiyle eşleşir.",
                    "Yanlıştır; sınıf yerine yer bilgisi verir.",
                    "Yanlıştır; sınıf yerine zaman bilgisi verir.",
                    "Yanlıştır; özne ile be fiili kişi ve sayı bakımından uyuşmaz.",
                ],
                "explanation": "Bağlam sınıf bilgisini açıkça verir.",
                "difficultyReason": (
                    "2 adım gerekir: bağlam kanıtı bulunur ve yakın "
                    "çeldiriciler bilgi türüne göre karşılaştırılır."
                ),
                "figure": None,
                "hints": [
                    f"{index + 1}. soruda istenen bilgi türünü belirle.",
                    "Yer ve zaman bilgilerini ayır.",
                    "Seçenekleri kökle karşılaştır.",
                    "Aynı genel dördüncü ipucu.",
                    "Aynı genel beşinci ipucu.",
                ],
                "objective": "OBJ",
                "objectiveSource": "https://example.test/program",
                "noteId": "tr.g05.test.n001",
                "reviewStatus": "pending",
                "provenance": "machine-generated:test:2026-08",
            }
        )
    package = tmp_path / "quality.jsonl"
    package.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )

    findings = pack_validate.validate_file(package)
    rules = {(finding.seviye, finding.kural) for finding in findings}
    assert ("UYARI", 38) in rules
    assert ("RAPOR", 39) in rules
    assert ("UYARI", 39) in rules


def test_english_v3_has_open_choice_pools_and_no_legacy_fillers():
    pack, questions = load_english()
    assert pack["version"] == 3
    assert len(questions) == 518

    choice_sets = Counter(
        tuple(
            sorted(
                repair_english_v3.normalize(choice)
                for choice in question["choices"]
            )
        )
        for question in questions
    )
    assert max(choice_sets.values()) == 1

    legacy = {
        repair_english_v3.normalize(choice)
        for question in questions
        for choice in question["choices"]
        if repair_english_v3.normalize(choice)
        in repair_english_v3.LEGACY_FILLERS
    }
    assert legacy == set()


def test_english_v3_reasons_name_the_measured_error():
    _, questions = load_english()
    banned = (
        "kişi, yer, zaman, eylem veya dil bilgisi ilişkilerinden en az birini karşılamaz",
        "yalnız tema sözcüğünü tanımak yeterli değildir",
    )
    for question in questions:
        reason = question["difficultyReason"]
        assert "adım gerektirir" in reason
        assert "Ön bilgi" in reason
        assert "Çeldiriciler" in reason
        assert not any(phrase in reason for phrase in banned)
        for index, distractor_reason in enumerate(question["distractorWhy"]):
            assert f"“{question['choices'][index]}”" in distractor_reason
            if index != question["correct"]:
                assert "yanlıştır" in distractor_reason
                assert not any(
                    phrase in distractor_reason for phrase in banned
                )


def test_english_v3_final_hints_are_question_specific():
    _, questions = load_english()
    for position in (3, 4):
        counts = Counter(question["hints"][position] for question in questions)
        assert counts.most_common(1)[0][1] / len(questions) < 0.10


def test_binlik_ayraci_ondalik_sanilmaz():
    """Kural 15: Türkçe yazımda "." binlik ayracıdır, ondalık ayracı değildir.

    Bu ayrım yapılmazsa "4.812 + 3.196" ifadesi 4,812 + 3,196 diye okunur ve
    doğrulayıcı, doğru içeriğe yanlış aritmetik hatası verir (ya da daha
    kötüsü, yanlış bir toplamı doğru sayar).
    """
    from fractions import Fraction

    hesapla = pack_validate.ifade_degerlendir

    assert hesapla("4.812 + 3.196") == 8008
    assert hesapla("10.000 ÷ 8") == 1250
    # ondalık virgül bozulmamalı
    assert hesapla("2,5 × 2") == 5
    assert hesapla("1,234 + 1") == Fraction(1117, 500)


def _kapali_kume_paketi():
    """Bir ünitenin kapalı sözcük kümesi: her sorunun çeldiricisi zorunlu
    olarak aynı kazanımdaki başka bir sorunun doğru cevabıdır."""
    kelimeler = ["always", "usually", "often", "sometimes", "rarely", "never"]
    rows = [{"type": "pack", "schemaVersion": "2.0", "id": "t", "version": 1,
             "lang": "en", "country": "TR", "curriculum": "MEB-TYMM-2025",
             "subject": "Test", "grade": 5, "levelScale": [1, 3]}]
    for i, dogru in enumerate(kelimeler):
        secenekler = [dogru] + [w for w in kelimeler if w != dogru][:3]
        rows.append({
            "type": "question", "id": f"t.q{i:03d}", "objective": "ENG.5.1.L1",
            "topic": "Frequency", "level": 1, "question": f"Soru {i} icin bosluk",
            "choices": secenekler, "correct": 0,
        })
    return rows


def test_kural41_ayni_kazanim_icindeki_cevap_havuzunu_geri_donusum_saymaz():
    """Kural 41 kazanim disindan odunc alinan celdiriciyi olcer.

    Sikliḳ zarflari ya da bir unitenin giysi sozcukleri kapali bir kumedir;
    her sorunun celdiricisi zorunlu olarak baska bir sorunun dogru cevabidir.
    Bunu kusur saymak, unite disindan sozcuk konmasini odullendirir ve
    soruyu kolaylastirir.
    """
    kazanim_celdiricileri = []
    metin_kazanimlari = {}
    for satir in _kapali_kume_paketi():
        if satir.get("type") != "question":
            continue
        kazanim = satir["objective"]
        secenekler = satir["choices"]
        dogru = satir["correct"]
        metin_kazanimlari.setdefault(
            pack_validate.normalize_metin(secenekler[dogru]), set()).add(kazanim)
        for i, c in enumerate(secenekler):
            if i != dogru:
                kazanim_celdiricileri.append(
                    (kazanim, pack_validate.normalize_metin(c)))

    geri_donen = sum(
        1 for kazanim, metin in kazanim_celdiricileri
        if metin and (metin_kazanimlari.get(metin, set()) - {kazanim})
    )
    assert kazanim_celdiricileri, "test paketi celdirici uretmedi"
    assert geri_donen == 0, (
        "ayni kazanim icindeki kapali cevap havuzu geri donusum sayilmamali; "
        f"{geri_donen} celdirici yanlislikla isaretlendi"
    )


def test_kural41_kazanim_disindan_odunc_celdiriciyi_yakalar():
    """Baska bir kazanimin dogru cevabini celdirici yapmak kusurdur."""
    metin_kazanimlari = {
        pack_validate.normalize_metin("20 cm"): {"MAT.5.3.7"},
    }
    kazanim_celdiricileri = [("MAT.5.4.1", pack_validate.normalize_metin("20 cm"))]
    geri_donen = sum(
        1 for kazanim, metin in kazanim_celdiricileri
        if metin and (metin_kazanimlari.get(metin, set()) - {kazanim})
    )
    assert geri_donen == 1
