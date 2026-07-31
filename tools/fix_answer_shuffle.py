# -*- coding: utf-8 -*-
"""Faz 4: Cevap konumu karistirma.
Deterministik seed ile her sorunun seceneklerini karistirir.
correctIndex, distractorWhy ve hints yeni sirayla eslesir.
Hedef: A/B/C/D dagilimi ~%25 (hicbiri %35'i gecmez).
"""
import io, json, os, sys, random, hashlib
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'turkiye\5-sinif'
SEED_BASE = 42  # Deterministik temel seed

def get_files():
    files = []
    for dirpath, _, filenames in os.walk(ROOT):
        for fn in sorted(filenames):
            if fn.endswith('.jsonl'):
                files.append(os.path.join(dirpath, fn))
    return files

def shuffle_question(obj, seed):
    """Bir sorunun seceneklerini deterministik olarak karistirir."""
    choices = obj.get('choices', [])
    correct = obj.get('correct', 0)
    dw = obj.get('distractorWhy', [])
    
    if len(choices) < 2:
        return obj
    
    # Mevcut indeksler
    indices = list(range(len(choices)))
    
    # Deterministik karistirma (soru ID + seed)
    qid = obj.get('id', '')
    rng = random.Random(hashlib.md5(f"{SEED_BASE}:{qid}".encode()).hexdigest())
    rng.shuffle(indices)
    
    # Yeni siralama
    new_choices = [choices[i] for i in indices]
    new_dw = [dw[i] for i in indices] if len(dw) == len(choices) else dw
    new_correct = indices.index(correct)
    
    obj['choices'] = new_choices
    obj['correct'] = new_correct
    if len(new_dw) == len(new_choices):
        obj['distractorWhy'] = new_dw
    
    # Hints: cevap metni iceren ipuclarini duzelt
    # (Karistirma sonrasi ipucu-cevap sizintisi kontrolu)
    correct_text = new_choices[new_correct].lower().strip()
    hints = obj.get('hints', [])
    for i, h in enumerate(hints[:4]):  # Ilk 4 ipucu
        h_lower = h.lower().strip()
        # Tam eslesme veya uzun alt metin kontrolu
        if len(correct_text) > 3 and correct_text in h_lower:
            hints[i] = 'Dogru secenegi dusun.'
    obj['hints'] = hints
    
    return obj

def process_file(fpath):
    lines = [l for l in io.open(fpath, encoding='utf-8').read().split('\n') if l.strip()]
    out = []
    q_count = 0
    
    for line in lines:
        obj = json.loads(line)
        if obj.get('type') == 'question':
            obj = shuffle_question(obj, SEED_BASE)
            q_count += 1
        out.append(obj)
    
    with io.open(fpath, 'w', encoding='utf-8') as f:
        for obj in out:
            f.write(json.dumps(obj, ensure_ascii=False) + '\n')
    
    return q_count

# Ana calisma
files = get_files()
print(f"Islenecek dosya: {len(files)}")

total_q = 0
for fpath in files:
    n = process_file(fpath)
    total_q += n
    print(f"  {os.path.basename(fpath)}: {n} soru karistirildi")

print(f"\nToplam: {total_q} soru karistirildi")

# Dagilim kontrolu
print("\nDogru cevap dagilimi (sonrasi):")
dist = Counter()
for fpath in files:
    lines = [l for l in io.open(fpath, encoding='utf-8').read().split('\n') if l.strip()]
    for line in lines:
        obj = json.loads(line)
        if obj.get('type') == 'question':
            dist[obj.get('correct', 0)] += 1

total = sum(dist.values())
for ci in range(4):
    cnt = dist.get(ci, 0)
    pct = cnt / total * 100 if total else 0
    label = chr(65 + ci)
    bar = '#' * int(pct / 2)
    flag = " !!!" if pct > 35 else ""
    print(f"  {label}: {cnt:5d} ({pct:5.1f}%) {bar}{flag}")

# Paket bazinda kontrol
print("\nPaket bazinda maks sapma:")
for fpath in files:
    lines = [l for l in io.open(fpath, encoding='utf-8').read().split('\n') if l.strip()]
    pdist = Counter()
    for line in lines:
        obj = json.loads(line)
        if obj.get('type') == 'question':
            pdist[obj.get('correct', 0)] += 1
    pt = sum(pdist.values())
    if pt == 0:
        continue
    max_pct = max(pdist.get(ci, 0) / pt * 100 for ci in range(4))
    fname = os.path.basename(fpath)
    flag = " GECERSIZ" if max_pct > 35 else " OK"
    print(f"  {fname}: maks %{max_pct:.1f}{flag}")
