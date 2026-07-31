"""Kesirler distractorWhy ve difficultyReason kalite kontrolu."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
f = ROOT / "turkiye" / "5-sinif" / "matematik" / "kesirler.jsonl"
lines = f.read_text(encoding="utf-8").strip().split("\n")

qs = [json.loads(l) for l in lines if json.loads(l).get("type") == "question"]

print("=== DISTRACTORWHY KALITESI (ornek 10 soru) ===\n")
for q in qs[5:15]:
    print(f"{q['id']} [L{q.get('level','?')}] {q.get('topic','?')}")
    print(f"  Q: {q['question'][:90]}")
    dw = q.get("distractorWhy", [])
    for i, d in enumerate(dw):
        marker = "OK" if i == q["correct"] else "XX"
        print(f"  [{marker}] {q['choices'][i][:30]:30s} -> {d[:60]}")
    print(f"  DR: {q.get('difficultyReason','')[:80]}")
    print()
