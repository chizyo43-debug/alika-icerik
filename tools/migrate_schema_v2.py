"""Şema V2 migrasyon aracı.

Mevcut v1 paketlere şema v2 alanlarını ekler:
- pack: schemaVersion, source, provenance, objectives, prerequisites
- question: objective, objectiveSource, difficultyReason, tags, reviewStatus, provenance
- note: objectives, band

Kullanım:
    python tools/migrate_schema_v2.py [--dry-run] [--subject Matematik]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TURKIYE = ROOT / "turkiye" / "5-sinif"

# MEB kazanım eşlemesi (konu bazlı)
KAZANIM_MAP = {
    "Matematik": {
        "kesirler": {"codes": ["M.5.1.4.1", "M.5.1.4.2", "M.5.1.4.3"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_matematik.pdf"},
        "ondalik-gosterim": {"codes": ["M.5.1.5.1", "M.5.1.5.2"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_matematik.pdf"},
        "yuzdeler": {"codes": ["M.5.1.6.1", "M.5.1.6.2"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_matematik.pdf"},
        "temel-geometrik-kavramlar": {"codes": ["M.5.2.1.1", "M.5.2.1.2"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_matematik.pdf"},
        "uzunluk-olcme": {"codes": ["M.5.3.1.1", "M.5.3.1.2"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_matematik.pdf"},
        "alan-olcme": {"codes": ["M.5.3.2.1", "M.5.3.2.2"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_matematik.pdf"},
        "veri-toplama-degerlendirme": {"codes": ["M.5.4.1.1", "M.5.4.1.2"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_matematik.pdf"},
    },
    "Fen Bilimleri": {
        "gunes-dunya-ay": {"codes": ["F.5.1.1.1", "F.5.1.1.2"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_fen_bilimleri.pdf"},
        "canlilarin-yapisina-yolculuk": {"codes": ["F.5.2.1.1", "F.5.2.1.2", "F.5.2.1.3"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_fen_bilimleri.pdf"},
        "kuvvetin-olculmesi": {"codes": ["F.5.3.1.1", "F.5.3.1.2"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_fen_bilimleri.pdf"},
        "madde-ve-degisim": {"codes": ["F.5.4.1.1", "F.5.4.1.2", "F.5.4.2.1"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_fen_bilimleri.pdf"},
        "isigin-yayilmasi": {"codes": ["F.5.5.1.1", "F.5.5.1.2"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_fen_bilimleri.pdf"},
        "insan-ve-cevre": {"codes": ["F.5.6.1.1", "F.5.6.1.2"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_fen_bilimleri.pdf"},
        "basit-elektrik-devreleri": {"codes": ["F.5.7.1.1", "F.5.7.1.2"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_fen_bilimleri.pdf"},
    },
    "Türkçe": {
        "sozcukte-anlam": {"codes": ["T.5.3.5", "T.5.3.6"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_turkce.pdf"},
        "cumlede-anlam": {"codes": ["T.5.3.14", "T.5.3.15"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_turkce.pdf"},
        "paragrafta-anlam": {"codes": ["T.5.3.19", "T.5.3.20", "T.5.3.21"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_turkce.pdf"},
        "ses-bilgisi": {"codes": ["T.5.4.1", "T.5.4.2"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_turkce.pdf"},
        "yazim-kurallari": {"codes": ["T.5.4.9", "T.5.4.10"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_turkce.pdf"},
        "noktalama-isaretleri": {"codes": ["T.5.4.11", "T.5.4.12"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_turkce.pdf"},
        "anlam-bilgisi": {"codes": ["T.5.3.5", "T.5.3.6", "T.5.3.14"], "source": "https://www.meb.gov.tr/meb_iys_dosyalar/2018_01/19/111743/dosyalar/2018_01/19/111743_5sinif_turkce.pdf"},
    },
}

# Zorluk gerekçesi şablonları
DIFFICULTY_TEMPLATES = {
    1: "{topic} konusunda temel kavram bilgisi; tek adım; doğrudan hatırlama; çeldiriciler belirgin",
    2: "{topic} konusunda 2-3 adım işlem; uygulama düzeyi; çeldiriciler yakın değerler içerir",
    3: "{topic} konusunda çok adımlı muhakeme; analiz/sentez; çeldiriciler yaygın hataları temsil eder",
}


def get_kazanim(subject: str, tema: str) -> dict:
    """Tema adından kazanım kodlarını bul."""
    tema_lower = tema.lower()
    subj_map = KAZANIM_MAP.get(subject, {})
    for key, val in subj_map.items():
        if key in tema_lower:
            return val
    # İlk kazanımı varsayılan olarak döndür
    if subj_map:
        return list(subj_map.values())[0]
    return {"codes": ["PENDING"], "source": "PENDING"}


def migrate_pack(obj: dict, subject: str) -> dict:
    """Pack satırına v2 alanları ekle."""
    obj["schemaVersion"] = "2.0"
    obj["source"] = "alika-atolye-v1-migrated"
    obj["provenance"] = "machine-generated:qwen3-4b:2026-07:human-pending"

    tema = obj.get("theme", "")
    kazanim = get_kazanim(subject, tema)
    obj["objectives"] = kazanim["codes"]
    obj["prerequisites"] = []

    # version +1
    obj["version"] = obj.get("version", 1) + 1
    return obj


def migrate_question(obj: dict, subject: str, tema: str) -> dict:
    """Soru satırına v2 alanları ekle."""
    kazanim = get_kazanim(subject, tema)
    level = obj.get("level", 1)

    obj["objective"] = kazanim["codes"][0] if kazanim["codes"] else "PENDING"
    obj["objectiveSource"] = kazanim["source"]
    obj["difficultyReason"] = DIFFICULTY_TEMPLATES.get(level, DIFFICULTY_TEMPLATES[2]).format(topic=obj.get("topic", tema))
    obj["tags"] = [obj.get("topic", "").lower().replace(" ", "-")] if obj.get("topic") else []
    obj["reviewStatus"] = "pending"
    obj["provenance"] = "machine-generated:qwen3-4b:2026-07:human-pending"
    return obj


def migrate_note(obj: dict, subject: str, tema: str) -> dict:
    """Not satırına v2 alanları ekle."""
    kazanim = get_kazanim(subject, tema)
    obj["objectives"] = kazanim["codes"][:2]  # İlk 2 kazanım
    obj["band"] = 2  # Varsayılan: 10-12 yaş bandı
    return obj


def migrate_file(path: Path, dry_run: bool = False) -> dict:
    """Tek dosyayı migrate et."""
    lines = path.read_text(encoding="utf-8").strip().split("\n")
    new_lines = []
    subject = ""
    tema = ""
    stats = {"pack": 0, "note": 0, "question": 0}

    for line in lines:
        obj = json.loads(line)
        t = obj.get("type", "")

        if t == "pack":
            subject = obj.get("subject", "")
            tema = obj.get("theme", "")
            obj = migrate_pack(obj, subject)
            stats["pack"] += 1
        elif t == "note":
            obj = migrate_note(obj, subject, tema)
            stats["note"] += 1
        elif t == "question":
            obj = migrate_question(obj, subject, tema)
            stats["question"] += 1

        new_lines.append(json.dumps(obj, ensure_ascii=False))

    if not dry_run:
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    return stats


def main():
    dry_run = "--dry-run" in sys.argv
    subject_filter = None
    for arg in sys.argv[1:]:
        if arg.startswith("--subject="):
            subject_filter = arg.split("=", 1)[1]

    if dry_run:
        print("=== KURU ÇALIŞTIRMA (değişiklik yazılmayacak) ===\n")

    total = {"pack": 0, "note": 0, "question": 0}
    file_count = 0

    for jsonl in sorted(TURKIYE.rglob("*.jsonl")):
        if subject_filter and subject_filter.lower() not in str(jsonl).lower():
            continue
        stats = migrate_file(jsonl, dry_run)
        file_count += 1
        for k in total:
            total[k] += stats[k]
        print(f"  {jsonl.relative_to(ROOT)}: {stats['question']} soru migrate edildi")

    print(f"\n{'[KURU] ' if dry_run else ''}Toplam: {file_count} dosya, "
          f"{total['pack']} paket, {total['note']} not, {total['question']} soru")


if __name__ == "__main__":
    main()
