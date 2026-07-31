"""Kesirler altın paket yükseltme aracı.

Her soruya özel difficultyReason üretir:
- Çözüm adımı sayısı
- İşlem türü (toplama, çıkarma, çarpma, bölme, karşılaştırma)
- Soyutlama seviyesi
- Çeldirici yakınlığı
- Ön bilgi gereksinimi

Ayrıca aritmetik doğrulama yapar (hesaplanabilir sorularda).

Kullanım:
    python tools/golden_kesirler.py [--dry-run]
"""
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KESIRLER = ROOT / "turkiye" / "5-sinif" / "matematik" / "kesirler.jsonl"


def parse_fraction(s: str):
    """'3/8' veya '2 tam 1/5' → Fraction."""
    s = s.strip()
    # Tam sayılı: "2 tam 1/5"
    m = re.match(r"(\d+)\s+tam\s+(\d+)/(\d+)", s)
    if m:
        return Fraction(int(m.group(1)) * int(m.group(3)) + int(m.group(2)), int(m.group(3)))
    # Basit kesir: "3/8"
    m = re.match(r"(\d+)/(\d+)", s)
    if m:
        return Fraction(int(m.group(1)), int(m.group(2)))
    # Tam sayı
    m = re.match(r"^(\d+)$", s)
    if m:
        return Fraction(int(m.group(1)))
    # Ondalık: "0.75"
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

    # Adım sayısı (explanation'dan tahmin)
    step_markers = re.findall(r"[→=÷×+\-]", explanation)
    steps = max(1, len(step_markers) // 2)
    if steps >= 4:
        parts.append(f"{steps} adım")
    elif steps >= 2:
        parts.append(f"{steps} adım")
    else:
        parts.append("tek adım")

    # İşlem türü
    ops = []
    if "topla" in explanation.lower() or "+" in explanation:
        ops.append("toplama")
    if "çıkar" in explanation.lower() or "-" in explanation:
        ops.append("çıkarma")
    if "×" in explanation or "çarp" in explanation.lower():
        ops.append("çarpma")
    if "÷" in explanation or "böl" in explanation.lower():
        ops.append("bölme")
    if "karşılaştır" in question.lower() or "sırala" in question.lower():
        ops.append("karşılaştırma")
    if "sadeleştir" in explanation.lower() or "EKOK" in explanation or "EBOB" in explanation:
        ops.append("sadeleştirme/EKOK")
    if ops:
        parts.append(" + ".join(ops[:3]))

    # Soyutlama
    if "model" in question.lower() or "şekil" in question.lower() or "görsel" in question.lower():
        parts.append("görsel yorumlama")
    elif "sayı doğrusu" in question.lower():
        parts.append("sayı doğrusu temsili")
    elif any(w in question.lower() for w in ["problem", "bir sınıfta", "bir pastan", "bir bahç"]):
        parts.append("gerçek yaşam problemi")

    # Çeldirici yakınlığı
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
    if prereqs:
        parts.append(f"ön bilgi: {', '.join(prereqs)}")

    reason = "; ".join(parts)
    # En az 20 karakter garantisi
    if len(reason) < 20:
        reason += f"; {topic} temel kavram uygulaması"
    return reason


def verify_arithmetic(q: dict) -> list:
    """Hesaplanabilir sorularda doğru cevabı bağımsız doğrula."""
    issues = []
    question = q.get("question", "")
    explanation = q.get("explanation", "")
    choices = q.get("choices", [])
    correct_idx = q.get("correct", 0)

    # "a/b + c/d" pattern
    m = re.search(r"(\d+/\d+)\s*([+\-])\s*(\d+/\d+)", question)
    if m:
        f1 = parse_fraction(m.group(1))
        f2 = parse_fraction(m.group(3))
        op = m.group(2)
        if f1 and f2:
            result = f1 + f2 if op == "+" else f1 - f2
            correct_choice = parse_fraction(choices[correct_idx])
            if correct_choice and correct_choice != result:
                issues.append(f"ARITMETIK HATA: {m.group(1)} {op} {m.group(3)} = {result}, ama correct={choices[correct_idx]}")

    # "a/b × c/d" pattern
    m = re.search(r"(\d+/\d+)\s*[×x]\s*(\d+/\d+)", question)
    if m:
        f1 = parse_fraction(m.group(1))
        f2 = parse_fraction(m.group(2))
        if f1 and f2:
            result = f1 * f2
            correct_choice = parse_fraction(choices[correct_idx])
            if correct_choice and correct_choice != result:
                issues.append(f"ARITMETIK HATA: {m.group(1)} × {m.group(2)} = {result}, ama correct={choices[correct_idx]}")

    # "N'nin a/b'i" pattern (sadece tek adımlı sorularda)
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
                            issues.append(f"ARITMETIK HATA: {n}×{pay}/{payda} = {result}, ama correct={choices[correct_idx]}")
                    except (ValueError, IndexError):
                        pass

    return issues


def main():
    dry_run = "--dry-run" in sys.argv
    lines = KESIRLER.read_text(encoding="utf-8").strip().split("\n")

    new_lines = []
    all_issues = []
    updated = 0

    for line in lines:
        obj = json.loads(line)
        if obj.get("type") != "question":
            new_lines.append(line)
            continue

        # Aritmetik doğrulama
        issues = verify_arithmetic(obj)
        if issues:
            all_issues.extend([(obj["id"], i) for i in issues])

        # Spesifik difficultyReason
        old_dr = obj.get("difficultyReason", "")
        new_dr = analyze_question(obj)
        if new_dr != old_dr:
            obj["difficultyReason"] = new_dr
            updated += 1

        new_lines.append(json.dumps(obj, ensure_ascii=False))

    # Rapor
    print(f"=== KESIRLER ALTIN PAKET YUKSELTME ===")
    print(f"difficultyReason güncellenen: {updated}/93 soru")
    print(f"Aritmetik sorun: {len(all_issues)}")
    for qid, issue in all_issues:
        print(f"  !! {qid}: {issue}")

    if not dry_run and not all_issues:
        KESIRLER.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        print("\nDosya güncellendi.")
    elif all_issues:
        print("\n!! Aritmetik hatalar var, dosya YAZILMADI. Elle düzeltin.")
    else:
        print("\n[KURU] Değişiklik yazılmadı.")


if __name__ == "__main__":
    main()
