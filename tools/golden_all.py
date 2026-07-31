"""Tüm paketlere spesifik difficultyReason uygular.

golden_kesirler.py'nin genelleştirilmiş hâli.
Matematik paketlerinde aritmetik doğrulama da yapar.

Kullanım:
    python tools/golden_all.py [--dry-run] [--subject Fen]
"""
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TURKIYE = ROOT / "turkiye" / "5-sinif"


def parse_fraction(s: str):
    """'3/8' veya '2 tam 1/5' → Fraction."""
    s = s.strip()
    m = re.match(r"(\d+)\s+tam\s+(\d+)/(\d+)", s)
    if m:
        return Fraction(int(m.group(1)) * int(m.group(3)) + int(m.group(2)), int(m.group(3)))
    m = re.match(r"(\d+)/(\d+)", s)
    if m:
        return Fraction(int(m.group(1)), int(m.group(2)))
    m = re.match(r"^(\d+)$", s)
    if m:
        return Fraction(int(m.group(1)))
    m = re.match(r"^(\d+)[.,](\d+)$", s)
    if m:
        return Fraction(f"{m.group(1)}.{m.group(2)}")
    return None


def analyze_question(q: dict) -> str:
    """Soru içeriğinden spesifik difficultyReason üret."""
    question = q.get("question", "")
    topic = q.get("topic", "")
    level = q.get("level", 1)
    choices = q.get("choices", [])
    explanation = q.get("explanation", "")

    parts = []

    # Adım sayısı
    step_markers = re.findall(r"[→=÷×+\-]", explanation)
    steps = max(1, len(step_markers) // 2)
    if steps >= 4:
        parts.append(f"{steps} adım")
    elif steps >= 2:
        parts.append(f"{steps} adım")
    else:
        parts.append("tek adım")

    # İşlem/bilişsel tür
    ops = []
    if any(w in explanation.lower() for w in ["topla", "+"]):
        ops.append("toplama")
    if any(w in explanation.lower() for w in ["çıkar", "-"]):
        ops.append("çıkarma")
    if "×" in explanation or "çarp" in explanation.lower():
        ops.append("çarpma")
    if "÷" in explanation or "böl" in explanation.lower():
        ops.append("bölme")
    if any(w in question.lower() for w in ["karşılaştır", "sırala", "hangisi daha"]):
        ops.append("karşılaştırma")
    if any(w in explanation.lower() for w in ["sadeleştir", "ekok", "ebob"]):
        ops.append("sadeleştirme")
    # Fen/Türkçe bilişsel süreçler
    if any(w in question.lower() for w in ["neden", "niçin", "açıkla"]):
        ops.append("nedensellik")
    if any(w in question.lower() for w in ["deney", "gözlem", "sonuç"]):
        ops.append("deneysel muhakeme")
    if any(w in question.lower() for w in ["anlam", "eş anlam", "zıt anlam"]):
        ops.append("anlam bilgisi")
    if any(w in question.lower() for w in ["paragraf", "metin", "yazar"]):
        ops.append("metin analizi")
    if ops:
        parts.append(" + ".join(ops[:3]))

    # Bağlam
    if any(w in question.lower() for w in ["model", "şekil", "görsel", "diyagram"]):
        parts.append("görsel yorumlama")
    elif "sayı doğrusu" in question.lower():
        parts.append("sayı doğrusu temsili")
    elif any(w in question.lower() for w in ["problem", "bir sınıfta", "bir pastan", "bir bahç", "bir market"]):
        parts.append("gerçek yaşam problemi")
    elif any(w in question.lower() for w in ["deney", "laboratuvar", "ölçüm"]):
        parts.append("deney bağlamı")

    # Çeldirici yakınlığı (Matematik)
    correct_idx = q.get("correct", 0)
    correct_val = parse_fraction(choices[correct_idx]) if correct_idx < len(choices) else None
    if correct_val:
        close_count = 0
        for i, c in enumerate(choices):
            if i == correct_idx:
                continue
            cv = parse_fraction(c)
            if cv and abs(cv - correct_val) <= Fraction(1, 4):
                close_count += 1
        if close_count >= 2:
            parts.append("çeldiriciler çok yakın")
        elif close_count == 1:
            parts.append("1 yakın çeldirici")

    # Ön bilgi
    prereqs = []
    if "EKOK" in explanation or "eşitle" in explanation.lower():
        prereqs.append("EKOK")
    if "EBOB" in explanation:
        prereqs.append("EBOB")
    if "ondalık" in topic.lower() and "kesir" in question.lower():
        prereqs.append("kesir-ondalık dönüşümü")
    if "yüzde" in question.lower():
        prereqs.append("yüzde kavramı")
    if any(w in question.lower() for w in ["fotosentez", "solunum"]):
        prereqs.append("hücre bilgisi")
    if any(w in question.lower() for w in ["devre", "ampul", "pil"]):
        prereqs.append("devre elemanları")
    if prereqs:
        parts.append(f"ön bilgi: {', '.join(prereqs)}")

    reason = "; ".join(parts)
    if len(reason) < 20:
        reason += f"; {topic} temel kavram uygulaması"
    return reason


def verify_arithmetic(q: dict) -> list:
    """Matematik sorularında aritmetik doğrulama."""
    issues = []
    question = q.get("question", "")
    choices = q.get("choices", [])
    correct_idx = q.get("correct", 0)

    # a/b + c/d veya a/b - c/d
    m = re.search(r"(\d+/\d+)\s*([+\-])\s*(\d+/\d+)", question)
    if m:
        f1 = parse_fraction(m.group(1))
        f2 = parse_fraction(m.group(3))
        op = m.group(2)
        if f1 and f2:
            result = f1 + f2 if op == "+" else f1 - f2
            correct_choice = parse_fraction(choices[correct_idx])
            if correct_choice and correct_choice != result:
                issues.append(f"ARITMETIK: {m.group(1)} {op} {m.group(3)} = {result}, correct={choices[correct_idx]}")

    # a/b × c/d
    m = re.search(r"(\d+/\d+)\s*[×x]\s*(\d+/\d+)", question)
    if m:
        f1 = parse_fraction(m.group(1))
        f2 = parse_fraction(m.group(2))
        if f1 and f2:
            result = f1 * f2
            correct_choice = parse_fraction(choices[correct_idx])
            if correct_choice and correct_choice != result:
                issues.append(f"ARITMETIK: {m.group(1)} × {m.group(2)} = {result}, correct={choices[correct_idx]}")

    # N'nin a/b'i (tek adımlı)
    multi_step = any(w in question.lower() for w in ["sonra", "kalan", "ardından", "daha sonra"])
    if not multi_step:
        m = re.search(r"(\d+)\D+(?:öğrenci|kişi|adet|tane)?\D*(\d+)/(\d+)['']?[iı]", question)
        if m:
            n = int(m.group(1))
            pay = int(m.group(2))
            payda = int(m.group(3))
            result = Fraction(n * pay, payda)
            correct_choice = parse_fraction(choices[correct_idx])
            if correct_choice and correct_choice != result:
                if result.denominator == 1:
                    try:
                        if int(choices[correct_idx]) != int(result):
                            issues.append(f"ARITMETIK: {n}×{pay}/{payda} = {result}, correct={choices[correct_idx]}")
                    except (ValueError, IndexError):
                        pass

    return issues


def process_file(path: Path, dry_run: bool, do_arithmetic: bool) -> dict:
    """Tek dosyayı işle."""
    lines = path.read_text(encoding="utf-8").strip().split("\n")
    new_lines = []
    stats = {"updated": 0, "issues": [], "total_q": 0}

    for line in lines:
        obj = json.loads(line)
        if obj.get("type") != "question":
            new_lines.append(line)
            continue

        stats["total_q"] += 1

        # Aritmetik doğrulama (sadece Matematik)
        if do_arithmetic:
            issues = verify_arithmetic(obj)
            if issues:
                stats["issues"].extend([(obj["id"], i) for i in issues])

        # Spesifik difficultyReason
        old_dr = obj.get("difficultyReason", "")
        new_dr = analyze_question(obj)
        if new_dr != old_dr:
            obj["difficultyReason"] = new_dr
            stats["updated"] += 1

        new_lines.append(json.dumps(obj, ensure_ascii=False))

    if not dry_run and not stats["issues"]:
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    return stats


def main():
    dry_run = "--dry-run" in sys.argv
    subject_filter = None
    for arg in sys.argv[1:]:
        if arg.startswith("--subject="):
            subject_filter = arg.split("=", 1)[1]

    if dry_run:
        print("=== KURU ÇALIŞTIRMA ===\n")

    total_updated = 0
    total_q = 0
    total_issues = []
    file_count = 0

    for jsonl in sorted(TURKIYE.rglob("*.jsonl")):
        if subject_filter and subject_filter.lower() not in str(jsonl).lower():
            continue

        do_arith = "matematik" in str(jsonl).lower()
        stats = process_file(jsonl, dry_run, do_arith)
        file_count += 1
        total_updated += stats["updated"]
        total_q += stats["total_q"]
        total_issues.extend(stats["issues"])

        status = "OK" if not stats["issues"] else f"!! {len(stats['issues'])} sorun"
        print(f"  {jsonl.relative_to(ROOT)}: {stats['updated']}/{stats['total_q']} DR güncellendi [{status}]")

    print(f"\n{'[KURU] ' if dry_run else ''}Toplam: {file_count} dosya, "
          f"{total_updated}/{total_q} difficultyReason güncellendi")
    if total_issues:
        print(f"\n!! ARITMETIK SORUNLAR ({len(total_issues)}):")
        for qid, issue in total_issues:
            print(f"  {qid}: {issue}")


if __name__ == "__main__":
    main()
