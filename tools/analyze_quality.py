# -*- coding: utf-8 -*-
"""AliKa icerik deposu kapsamli kalite analizi - Faz 1"""
import io, json, os, re, sys, hashlib
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'c:\Users\Shadow\Desktop\ebeveyn_kontrol\icerik'
files = []
for dirpath, _, filenames in os.walk(ROOT):
    for fn in sorted(filenames):
        if fn.endswith('.jsonl'):
            files.append(os.path.join(dirpath, fn))

print(f"Toplam JSONL dosyasi: {len(files)}\n")

# Global collectors
all_packs = []
all_notes = []
all_questions = []
pack_ids = Counter()
line_ids = Counter()
question_texts = Counter()
correct_dist = Counter()  # A/B/C/D
level_dist = Counter()
figure_count = 0
placeholder_pat = re.compile(r'\(yaz[iı]m fark[iı]|\(farkl[iı] [oö]rnek\)|\(farkli ornek\)')
turkish_char_pat = re.compile(r'[ğĞıİşŞçÇöÖüÜ]')
mojibake_pat = re.compile(r'[Ã¢Ã¤Ã§Ã¶Ã¼ÃğÃıÃş]|â€|Ã©')
objective_empty = 0
objective_source_empty = 0
hint_answer_leak = 0

per_subject = defaultdict(lambda: {"packs":0,"notes":0,"questions":0,"files":[],"correct":Counter(),"levels":Counter(),"figures":0,"placeholders":0,"mojibake":0,"no_turkish_chars":0})

def normalize(s):
    return re.sub(r'[^a-z0-9\u00e0-\u024f\u011f\u0131\u015f\u00e7]', '', s.lower().strip())

for fpath in files:
    rel = os.path.relpath(fpath, ROOT)
    lines = [l for l in io.open(fpath, encoding='utf-8').read().split('\n') if l.strip()]
    
    subj = None
    file_packs = []
    file_notes = []
    file_questions = []
    
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"  JSON HATA: {rel} satir {i+1}: {e}")
            continue
        
        t = obj.get('type')
        if t == 'pack':
            pid = obj.get('id','?')
            pack_ids[pid] += 1
            file_packs.append(obj)
            all_packs.append(obj)
            subj = obj.get('subject','?')
        elif t == 'note':
            nid = obj.get('id','?')
            line_ids[nid] += 1
            file_notes.append(obj)
            all_notes.append(obj)
        elif t == 'question':
            qid = obj.get('id','?')
            line_ids[qid] += 1
            file_questions.append(obj)
            all_questions.append(obj)
            
            # Correct answer distribution
            ci = obj.get('correct', 0)
            correct_dist[ci] += 1
            
            # Level distribution
            lv = obj.get('level', 0)
            level_dist[lv] += 1
            
            # Figure
            if obj.get('figure'):
                figure_count += 1
            
            # Objective
            if not obj.get('objective'):
                objective_empty += 1
            if not obj.get('objectiveSource'):
                objective_source_empty += 1
            
            # Question text duplicates (normalized)
            qt = normalize(obj.get('question',''))
            question_texts[qt] += 1
            
            # Placeholder check
            full_text = json.dumps(obj, ensure_ascii=False)
            if placeholder_pat.search(full_text):
                per_subject[subj]["placeholders"] += 1 if subj else 0
            
            # Mojibake check
            if mojibake_pat.search(full_text):
                per_subject[subj]["mojibake"] += 1 if subj else 0
            
            # Turkish char check (notes)
            if not turkish_char_pat.search(obj.get('question','') + obj.get('explanation','')):
                per_subject[subj]["no_turkish_chars"] += 1 if subj else 0
            
            # Hint leaks correct answer
            choices = obj.get('choices', [])
            hints = obj.get('hints', [])
            if ci < len(choices):
                norm_c = normalize(choices[ci])
                if norm_c and len(norm_c) > 3:
                    for h in hints:
                        if norm_c in normalize(h):
                            hint_answer_leak += 1
                            break
    
    if subj:
        s = per_subject[subj]
        s["packs"] += len(file_packs)
        s["notes"] += len(file_notes)
        s["questions"] += len(file_questions)
        s["files"].append(rel)
        for q in file_questions:
            s["correct"][q.get('correct',0)] += 1
            s["levels"][q.get('level',0)] += 1
            if q.get('figure'):
                s["figures"] += 1

# === REPORT ===
print("=" * 70)
print("ALIKA ICERIK DEPOSU - FAZ 1 KALITE ANALIZI")
print("=" * 70)

print(f"\n## GENEL ISTASTISTIKLER")
print(f"  JSONL dosyalari: {len(files)}")
print(f"  Paketler: {len(all_packs)}")
print(f"  Notlar: {len(all_notes)}")
print(f"  Sorular: {len(all_questions)}")
print(f"  Toplam satir: {len(all_packs)+len(all_notes)+len(all_questions)}")

print(f"\n## PAKET KIMLIGI DUPLIKASYONU")
dup_packs = {k:v for k,v in pack_ids.items() if v > 1}
if dup_packs:
    for k,v in sorted(dup_packs.items()):
        print(f"  DUPLIKE: {k} -> {v} kez")
else:
    print("  Yok")

print(f"\n## SATIR KIMLIGI DUPLIKASYONU")
dup_lines = {k:v for k,v in line_ids.items() if v > 1}
if dup_lines:
    print(f"  Toplam duplike kimlik: {len(dup_lines)}")
    for k,v in sorted(dup_lines.items())[:20]:
        print(f"    {k} -> {v} kez")
    if len(dup_lines) > 20:
        print(f"    ... ve {len(dup_lines)-20} daha")
else:
    print("  Yok")

print(f"\n## SORU METNI DUPLIKASYONU (normalize)")
dup_q = {k:v for k,v in question_texts.items() if v > 1}
print(f"  Duplike soru metni: {len(dup_q)}")
if dup_q:
    for k,v in sorted(dup_q.items(), key=lambda x:-x[1])[:10]:
        print(f"    [{v}x] {k[:60]}...")

print(f"\n## DOGRU CEVAP KONUMU DAGILIMI")
total_q = len(all_questions)
for ci in range(4):
    cnt = correct_dist.get(ci, 0)
    pct = cnt/total_q*100 if total_q else 0
    label = chr(65+ci)
    bar = '#' * int(pct/2)
    print(f"  {label}: {cnt:5d} ({pct:5.1f}%) {bar}")

print(f"\n## ZORLUK SEVIYESI DAGILIMI")
for lv in sorted(level_dist.keys()):
    cnt = level_dist[lv]
    pct = cnt/total_q*100 if total_q else 0
    print(f"  Seviye {lv}: {cnt:5d} ({pct:5.1f}%)")

print(f"\n## SEKIL/GORSEL KULLANIMI")
print(f"  Sekilli soru: {figure_count} / {total_q} ({figure_count/total_q*100:.1f}%)")

print(f"\n## KAZANIM (OBJECTIVE) DURUMU")
print(f"  objective bos: {objective_empty} / {total_q} ({objective_empty/total_q*100:.1f}%)")
print(f"  objectiveSource bos: {objective_source_empty} / {total_q} ({objective_source_empty/total_q*100:.1f}%)")

print(f"\n## IPUCU-CEVAP SIZINTISI")
print(f"  Ipucu dogru cevabi iceriyor: {hint_answer_leak}")

print(f"\n## DERS BAZINDA PROFIL")
for subj in sorted(per_subject.keys()):
    s = per_subject[subj]
    print(f"\n  ### {subj}")
    print(f"    Dosyalar: {len(s['files'])}")
    print(f"    Paket: {s['packs']}, Not: {s['notes']}, Soru: {s['questions']}")
    print(f"    Dogru cevap dagilimi:")
    tq = s['questions']
    for ci in range(4):
        cnt = s['correct'].get(ci, 0)
        pct = cnt/tq*100 if tq else 0
        print(f"      {chr(65+ci)}: {cnt:4d} ({pct:5.1f}%)")
    print(f"    Seviye dagilimi: {dict(s['levels'])}")
    print(f"    Sekilli soru: {s['figures']}")
    print(f"    Yer tutucu: {s['placeholders']}")
    print(f"    Mojibake: {s['mojibake']}")
    print(f"    Turkce karaktersiz: {s['no_turkish_chars']}")

# Fen duplikasyon analizi
print(f"\n## FEN BILIMLERI DUPLIKASYON ANALIZI")
fen_dir = os.path.join(ROOT, 'turkiye', '5-sinif', 'fen-bilimleri')
named_files = sorted([f for f in os.listdir(fen_dir) if f.endswith('.jsonl') and not f.startswith('u')])
u_files = sorted([f for f in os.listdir(fen_dir) if f.endswith('.jsonl') and f.startswith('u')])
print(f"  Aciklayici dosyalar: {named_files}")
print(f"  u1-u7 dosyalari: {u_files}")

for uf in u_files:
    upath = os.path.join(fen_dir, uf)
    ulines = [l for l in io.open(upath, encoding='utf-8').read().split('\n') if l.strip()]
    upack = json.loads(ulines[0])
    upid = upack.get('id','?')
    utheme = upack.get('theme','?')
    uhash = hashlib.md5(io.open(upath,'rb').read()).hexdigest()[:12]
    
    # Find matching named file
    match = None
    for nf in named_files:
        npath = os.path.join(fen_dir, nf)
        nlines = [l for l in io.open(npath, encoding='utf-8').read().split('\n') if l.strip()]
        npack = json.loads(nlines[0])
        npid = npack.get('id','?')
        if npid == upid:
            nhash = hashlib.md5(io.open(npath,'rb').read()).hexdigest()[:12]
            match = (nf, npid, nhash, len(nlines))
            break
    
    if match:
        same = "AYNI" if match[2] == uhash else "FARKLI"
        print(f"  {uf} (pid={upid}, {len(ulines)} satir, hash={uhash}) <-> {match[0]} (hash={match[2]}, {match[3]} satir) [{same}]")
    else:
        print(f"  {uf} (pid={upid}, {len(ulines)} satir, hash={uhash}) <-> ESLESME YOK")

print(f"\n## DOSYA BOYUTLARI")
total_size = 0
for fpath in files:
    sz = os.path.getsize(fpath)
    total_size += sz
print(f"  Toplam: {total_size/1024:.1f} KB ({total_size/1024/1024:.2f} MB)")

print("\n=== ANALIZ TAMAMLANDI ===")
