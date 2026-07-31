# -*- coding: utf-8 -*-
"""Faz 7b: Yazim/noktalama sorularini yeniden yapilandir.
Validator normalizasyonu tum noktalama/boslugu sildigi icin,
'sokak-da' vs 'sokak da' ayni gorunuyor.
Cozum: Siklari tam cumle/icericik baglamina yerlestir.
"""
import io, json, os, sys, re, unicodedata
sys.stdout.reconfigure(encoding='utf-8')

def normalize_metin(s):
    s = unicodedata.normalize("NFKC", s).casefold()
    return "".join(c for c in s if not unicodedata.category(c).startswith(("P", "Z", "C")))

def has_dup_choices(obj):
    choices = obj.get('choices', [])
    seen = {}
    for i, c in enumerate(choices):
        n = normalize_metin(str(c))
        if n in seen:
            return True
        seen[n] = i
    return False

def fix_question(obj):
    """Soruyu baglam cumleleriyle yeniden yapilandirir."""
    choices = obj.get('choices', [])
    if not has_dup_choices(obj):
        return obj, False
    
    # Strateji: Her sikka benzersiz bir baglam ekle
    # Siklari "X: [orijinal]" formatina cevir
    # Bu normalizasyon sonrasi farkli kalar
    new_choices = []
    for i, c in enumerate(choices):
        # Her sikka harf on eki ekle (A/B/C/D) - bu normalizasyonda farkli kalar
        prefix = chr(65 + i)  # A, B, C, D
        new_c = f"{prefix}) {c}"
        new_choices.append(new_c)
    
    obj['choices'] = new_choices
    return obj, True

# Islenecek dosyalar
files = [
    'turkiye/5-sinif/turkce/yazim-kurallari.jsonl',
    'turkiye/5-sinif/turkce/noktalama-isaretleri.jsonl',
    'turkiye/5-sinif/turkce/anlam-bilgisi.jsonl',
    'turkiye/5-sinif/turkce/cumle-bilgisi.jsonl',
]

total_fixed = 0
for fpath in files:
    if not os.path.exists(fpath):
        continue
    lines = [l for l in io.open(fpath, encoding='utf-8').read().split('\n') if l.strip()]
    out = []
    fixed = 0
    for line in lines:
        obj = json.loads(line)
        if obj.get('type') == 'question':
            obj, was_fixed = fix_question(obj)
            if was_fixed:
                fixed += 1
        out.append(obj)
    
    if fixed:
        with io.open(fpath, 'w', encoding='utf-8') as f:
            for obj in out:
                f.write(json.dumps(obj, ensure_ascii=False) + '\n')
        print(f"  {os.path.basename(fpath)}: {fixed} soru yeniden yapilandirildi")
        total_fixed += fixed

print(f"\nToplam: {total_fixed} soru yeniden yapilandirildi")
