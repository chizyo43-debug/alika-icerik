# -*- coding: utf-8 -*-
import io, json, sys
sys.stdout.reconfigure(encoding='utf-8')
u1 = [json.loads(l) for l in io.open('turkiye/5-sinif/fen-bilimleri/u1.jsonl', encoding='utf-8').read().split('\n') if l.strip()]
named = [json.loads(l) for l in io.open('turkiye/5-sinif/fen-bilimleri/gokyuzundeki-komsularimiz.jsonl', encoding='utf-8').read().split('\n') if l.strip()]
u1n = [o for o in u1 if o.get('type') == 'note']
nn = [o for o in named if o.get('type') == 'note']
print(f"u1 not body ort: {sum(len(o['body']) for o in u1n) // len(u1n)}")
print(f"named not body ort: {sum(len(o['body']) for o in nn) // len(nn)}")
u1q = [o for o in u1 if o.get('type') == 'question']
nq = [o for o in named if o.get('type') == 'question']
same = all(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True) for a, b in zip(u1q, nq))
print(f"Sorular birebir ayni mi: {same}")
# Notlar ayni mi?
same_n = all(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True) for a, b in zip(u1n, nn))
print(f"Notlar birebir ayni mi: {same_n}")
if not same_n:
    for i, (a, b) in enumerate(zip(u1n, nn)):
        if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
            print(f"  Farkli not {i}: u1 body={len(a['body'])} named body={len(b['body'])}")
