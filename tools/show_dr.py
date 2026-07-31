"""difficultyReason ornekleri."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
f = ROOT / "turkiye" / "5-sinif" / "matematik" / "kesirler.jsonl"
lines = f.read_text(encoding="utf-8").strip().split("\n")
qs = [json.loads(l) for l in lines if json.loads(l).get("type") == "question"]

for q in [qs[0], qs[7], qs[27], qs[50], qs[80], qs[92]]:
    print(f"{q['id']} [L{q.get('level','?')}] {q.get('topic','?')}")
    print(f"  Q: {q['question'][:80]}")
    print(f"  DR: {q['difficultyReason']}")
    print()
