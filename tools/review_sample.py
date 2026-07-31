"""İnsan incelemesi örneklem raporu üretir.

Her paketten rastgele (deterministik) %10 soru seçer ve
inceleme formu formatında raporlar.

Kullanım:
    python tools/review_sample.py > reports/REVIEW_SAMPLE.md
"""
import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TURKIYE = ROOT / "turkiye" / "5-sinif"
SEED = 2026


def select_sample(questions: list, pct: float = 0.10) -> list:
    """Deterministik örnekleme."""
    n = max(1, int(len(questions) * pct))
    rng = random.Random(SEED)
    indices = sorted(rng.sample(range(len(questions)), min(n, len(questions))))
    return [questions[i] for i in indices]


def main():
    print("# İnsan İncelemesi Örneklem Raporu")
    print(f"\n**Tarih:** 2026-07-29  ")
    print(f"**Örnekleme oranı:** %10 (deterministik, seed={SEED})  ")
    print(f"**Amaç:** Makine üretimi içeriğin pedagojik doğrulaması\n")
    print("---\n")

    total_sampled = 0
    total_questions = 0

    for jsonl in sorted(TURKIYE.rglob("*.jsonl")):
        lines = jsonl.read_text(encoding="utf-8").strip().split("\n")
        pack = None
        questions = []
        for l in lines:
            obj = json.loads(l)
            if obj.get("type") == "pack":
                pack = obj
            elif obj.get("type") == "question":
                questions.append(obj)

        if not pack or not questions:
            continue

        sample = select_sample(questions)
        total_sampled += len(sample)
        total_questions += len(questions)

        rel = jsonl.relative_to(ROOT)
        print(f"## {pack.get('subject', '?')} — {pack.get('theme', rel.stem)}")
        print(f"**Dosya:** `{rel}`  ")
        print(f"**Örneklem:** {len(sample)}/{len(questions)} soru\n")

        for q in sample:
            print(f"### {q['id']}")
            print(f"- **Konu:** {q.get('topic', '?')}")
            print(f"- **Zorluk:** L{q.get('level', '?')} — {q.get('difficultyReason', '')[:60]}")
            print(f"- **Kazanım:** {q.get('objective', '?')}")
            print(f"- **Soru:** {q['question']}")
            print(f"- **Seçenekler:**")
            for i, c in enumerate(q["choices"]):
                marker = "✓" if i == q["correct"] else "✗"
                print(f"  - {marker} {c}")
            print(f"- **Açıklama:** {q.get('explanation', '')}")
            print(f"- **İnceleme durumu:** {q.get('reviewStatus', 'pending')}")
            print(f"- [ ] Doğru cevap onaylandı")
            print(f"- [ ] Çeldiriciler pedagojik olarak uygun")
            print(f"- [ ] Açıklama yeterli")
            print(f"- [ ] Zorluk seviyesi doğru")
            print()

        print("---\n")

    print(f"## Özet")
    print(f"- Toplam soru: {total_questions}")
    print(f"- Örneklenen: {total_sampled} (%{total_sampled/total_questions*100:.1f})")
    print(f"- Paket sayısı: {len(list(TURKIYE.rglob('*.jsonl')))}")


if __name__ == "__main__":
    main()
