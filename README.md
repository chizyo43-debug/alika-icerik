# AliKa İçerik Paketleri

AliKa uygulaması için indirilebilir **ders notu + soru bankası** paketleri.

## Kullanım

AliKa uygulaması bu repodaki paketleri otomatik çeker. Elle indirmek için:

```
https://raw.githubusercontent.com/chizyo43-debug/alika-icerik/main/turkiye/5-sinif/matematik/matematik-tum.jsonl
```

## Dizin Yapısı

```
├── turkiye/                     ← ülke
│   └── 5-sinif/                ← sınıf
│       ├── matematik/          ← ders
│       │   └── matematik-tum.jsonl  ← final onaylı tüm konular
│       ├── fen-bilimleri/      ← ders
│       │   └── fen-bilimleri-tum.jsonl  ← final onaylı tüm konular
│       ├── turkce/             ← ders
│       │   └── turkce-tum.jsonl ← AI-only kalite kontrolü tamamlanan içerik
│       └── ingilizce/          ← ders
│           └── ingilizce-tum.jsonl ← final onaylı tüm konular
├── legal/                       ← yasal belgeler (Store gereksinimi)
└── README.md
```

## Paket Formatı (.jsonl)

Her satır bir JSON nesnesi:

| Tip | Açıklama |
|-----|----------|
| `pack` | Üst veri (id, müfredat, sınıf, tema, lisans) |
| `note` | Ders notu — tam konu anlatımı (Markdown) |
| `question` | Soru — seçenekler, çeldirici analizi, açıklama ve seviye 1-5 |

## Mevcut Paketler

| Ülke | Sınıf | Ders | Konu | Not | Soru | Durum |
|------|-------|------|------|-----|------|-------|
| Türkiye | 5 | Matematik | Tüm konular | 23 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 5 | Fen Bilimleri | Tüm konular | 28 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 5 | Türkçe | Tüm beceriler | 22 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 5 | İngilizce | Tüm temalar | 24 | 518 | ⚠️ Eski 2.0 sözleşmesi; 2.2 geçişi bekliyor |

## İndirme Katmanları

| Katman | Açıklama | Örnek |
|--------|----------|-------|
| **Ders paketi** | Dersin bütün konu ve kazanımları | `matematik/matematik-tum.jsonl` |
| **Birleşik** | Sınıftaki tüm dersler | `5-sinif-tum-dersler.jsonl` |

## İçerik üretimi ve kalite

İçerik üretecek veya düzeltecek herkes (insan ya da model) önce
**[AUTHORING_RULES.md](AUTHORING_RULES.md)** okur: bu depoda gerçekten yapılmış
hatalar ve tekrar etmemesi için uyulacak üretim disiplini.

```bash
python tools/pack_validate.py turkiye/5-sinif/matematik/matematik-tum.jsonl
```

```bash
python tools/pack_validate.py --skor turkiye/5-sinif --json reports/quality_score.json
```

```bash
python -m pytest tests/ -q
```

Kalite kapısı: her pakette **0 HATA** zorunlu; UYARI sayısı ve skor
`tests/quality_baseline.json` içindeki tabandan kötüleşemez. Hedef, tüm
paketlerde 0 uyarı ve skor ≥ 99. Şema: [SCHEMA_V2.md](SCHEMA_V2.md).

`tools/regen_*` ve `tools/migrate_*` dosyaları geçmiş onarımların
tekrarlanabilir kayıtlarıdır; yeni üretim girişi değildir. Yeni paketler
Question Contract 2.2 ile, `hints` alanı olmadan üretilir.

## Lisans

İçerikler: [CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/)
Yasal belgeler: `legal/` klasöründe (telif hakkı saklıdır).
