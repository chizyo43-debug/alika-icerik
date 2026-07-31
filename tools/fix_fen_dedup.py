# -*- coding: utf-8 -*-
"""Faz 3: Fen Bilimleri duplikasyon giderme.
u1-u7 (zengin notlar) kanonik -> aciklayici dosya adlarina tasi.
Eski u1-u7 dosyalarini sil.
"""
import io, json, os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

FEN = r'turkiye\5-sinif\fen-bilimleri'

# Esleme: u dosyasi -> aciklayici ad
ESLEME = {
    'u1.jsonl': 'gokyuzundeki-komsularimiz.jsonl',
    'u2.jsonl': 'kuvveti-taniyalim.jsonl',
    'u3.jsonl': 'canlilarin-yapisina-yolculuk.jsonl',
    'u4.jsonl': 'isigin-dunyasi.jsonl',
    'u5.jsonl': 'maddenin-dogasi.jsonl',
    'u6.jsonl': 'yasamimizdaki-elektrik.jsonl',
    'u7.jsonl': 'surdurulebilir-yasam.jsonl',
}

for u_file, named_file in ESLEME.items():
    u_path = os.path.join(FEN, u_file)
    named_path = os.path.join(FEN, named_file)
    
    if not os.path.exists(u_path):
        print(f"  ATLA: {u_file} yok")
        continue
    
    # u dosyasini oku (kanonik - zengin notlar)
    u_lines = [l for l in io.open(u_path, encoding='utf-8').read().split('\n') if l.strip()]
    
    # Dogrulama: 100 satir (1 pack + 9 not + 90 soru)
    assert len(u_lines) == 100, f"{u_file}: {len(u_lines)} satir (beklenen 100)"
    
    # Pack ID dogrula
    pack = json.loads(u_lines[0])
    assert pack['type'] == 'pack'
    
    # Named dosyaya yaz (u icerigi)
    with io.open(named_path, 'w', encoding='utf-8') as f:
        for line in u_lines:
            f.write(line + '\n')
    
    print(f"  {u_file} -> {named_file} (100 satir, pack={pack['id']})")

# Dogrulama: named dosyalar artik zengin icerige sahip
print("\nDogrulama:")
for u_file, named_file in ESLEME.items():
    named_path = os.path.join(FEN, named_file)
    lines = [l for l in io.open(named_path, encoding='utf-8').read().split('\n') if l.strip()]
    notes = [json.loads(l) for l in lines if json.loads(l).get('type') == 'note']
    avg_body = sum(len(n['body']) for n in notes) // len(notes)
    print(f"  {named_file}: {len(lines)} satir, not body ort: {avg_body}")

# u dosyalarini sil
print("\nEski u dosyalari siliniyor:")
for u_file in ESLEME.keys():
    u_path = os.path.join(FEN, u_file)
    if os.path.exists(u_path):
        os.remove(u_path)
        print(f"  SILINDI: {u_file}")

print("\nFaz 3 tamamlandi.")
