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
│       └── 5-sinif-tum-dersler.jsonl ← (ileride: tüm dersler birleşik)
├── legal/                       ← yasal belgeler (Store gereksinimi)
└── README.md
```

## Paket Formatı (.jsonl)

Her satır bir JSON nesnesi:

| Tip | Açıklama |
|-----|----------|
| `pack` | Üst veri (id, müfredat, sınıf, tema, lisans) |
| `note` | Ders notu — tam konu anlatımı (Markdown) |
| `question` | Soru — 4 şık, 5 ipucu, çeldirici analizi, seviye 1-5 |

## Mevcut Paketler

| Ülke | Sınıf | Ders | Konu | Not | Soru | Durum |
|------|-------|------|------|-----|------|-------|
| Türkiye | 5 | Matematik | Tüm konular | 23 | 500 | ✅ Final onaylı |

## İndirme Katmanları

| Katman | Açıklama | Örnek |
|--------|----------|-------|
| **Ders paketi** | Dersin bütün konu ve kazanımları | `matematik/matematik-tum.jsonl` |
| **Birleşik** | Sınıftaki tüm dersler | `5-sinif-tum-dersler.jsonl` |

## Lisans

İçerikler: [CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/)
Yasal belgeler: `legal/` klasöründe (telif hakkı saklıdır).
