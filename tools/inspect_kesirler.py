"""Kesirler paketi inceleme."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
f = ROOT / "turkiye" / "5-sinif" / "matematik" / "kesirler.jsonl"
lines = f.read_text(encoding="utf-8").strip().split("\n")

print(f"Toplam satir: {len(lines)}")

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

print(f"Pack: {pack['id']} v{pack['version']} - {pack['theme']}")
print(f"Notlar: {len(notes)}, Sorular: {len(questions)}")

for n in notes:
    print(f"  NOT {n['id']}: {n.get('title', n.get('topic','?'))} ({len(n.get('body',''))} chars)")

levels = Counter(q.get("level", 0) for q in questions)
print(f"\nZorluk: {dict(sorted(levels.items()))}")
topics = Counter(q.get("topic", "?") for q in questions)
print(f"Konular: {dict(topics)}")

print("\n--- ILK 10 SORU ---")
for q in questions[:10]:
    print(f"\n  {q['id']} [L{q.get('level','?')}] {q.get('topic','?')}")
    print(f"  Q: {q['question'][:100]}")
    print(f"  C: {q['choices']}")
    print(f"  correct={q['correct']} | expl: {q.get('explanation','')[:80]}")
