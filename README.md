# AliKa İçerik Paketleri

AliKa uygulaması için indirilebilir **ders notu + soru bankası** paketleri.

Ayrıca AliKa'nın veri-only ortak ekran motoru için indirilebilir oyun
paketleri `games/` altında yayımlanır. Oyun paketleri uygulama kodu veya
eklenti taşımaz.

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
│       │   └── matematik-tum.jsonl  ← AI-only doğrulanmış paket
│       ├── fen-bilimleri/      ← ders
│       │   └── fen-bilimleri-tum.jsonl  ← AI-only doğrulanmış paket
│       ├── turkce/             ← ders
│       │   └── turkce-tum.jsonl ← AI-only kalite kontrolü tamamlanan içerik
│       ├── ingilizce/          ← ders
│       │   └── ingilizce-tum.jsonl ← AI-only doğrulanmış paket
│       ├── sosyal-bilgiler/    ← ders
│       │   └── sosyal-bilgiler-tum.jsonl ← AI-only doğrulanmış paket
│       └── soru-bankasi/
│           └── 5-sinif-tum-dersler-2000-soru.jsonl ← ortak seçki
│   └── 6-sinif/                ← sınıf
│       ├── matematik/matematik-tum.jsonl
│       ├── fen-bilimleri/fen-bilimleri-tum.jsonl
│       ├── turkce/turkce-tum.jsonl
│       ├── ingilizce/ingilizce-tum.jsonl
│       ├── sosyal-bilgiler/sosyal-bilgiler-tum.jsonl
│       ├── din-kulturu/din-kulturu-tum.jsonl
│       ├── bilisim-teknolojileri/bilisim-teknolojileri-tum.jsonl
│       └── soru-bankasi/
│           └── 6-sinif-tum-dersler-2000-soru.jsonl ← ortak seçki
├── legal/                       ← yasal belgeler (Store gereksinimi)
├── games/trivia/                ← yaş ve dile göre Bilgi Yarışması paketleri
├── games/memory/                ← yaş ve dile göre Ülke–Başkent Hafızası
├── games/word-wheel/            ← yaş ve dile göre Çarkıfelek kelimeleri
├── games/who-is-it/             ← yaş ve dile göre Bu Kim? kişi havuzları
├── games/taboo/                 ← yaş ve dile göre Tabu kartları
├── games/liar/                  ← yaş ve dile göre Yalancı kartları
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
| Türkiye | 5 | İngilizce | Tüm temalar | 24 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 5 | Sosyal Bilgiler | Tüm öğrenme alanları | 19 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 5 | Tüm Dersler | Beş dersin dengeli seçkisi | 116 | 2.000 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 6 | Matematik | Tüm konular | 24 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 6 | Fen Bilimleri | Tüm konular | 36 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 6 | Türkçe | Tüm beceriler | 28 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 6 | İngilizce | Tüm temalar | 19 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 6 | Sosyal Bilgiler | Tüm öğrenme alanları | 18 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 6 | Din Kültürü ve Ahlak Bilgisi | Tüm konular | 18 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 6 | Bilişim Teknolojileri ve Yazılım | Tüm konular | 25 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 6 | Tüm Dersler | Yedi dersin ağırlıklı seçkisi | 168 | 2.000 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 7 | Türkçe | Tüm beceriler | 152 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 7 | Matematik | Tüm konular | 30 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 7 | Fen Bilimleri | Tüm konular | 11 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 7 | İngilizce | Tüm temalar | 192 | 1.536 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 7 | Sosyal Bilgiler | Tüm konular | 17 | 136 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 7 | Din Kültürü ve Ahlak Bilgisi | Tüm konular | 17 | 136 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 8 | Türkçe | Tüm beceriler | 170 | 628 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 8 | Matematik | Tüm konular | 23 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 8 | Fen Bilimleri | Tüm konular | 37 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 8 | İngilizce | Tüm temalar | 192 | 1.536 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 8 | T.C. İnkılap Tarihi ve Atatürkçülük | Tüm konular | 15 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 8 | Din Kültürü ve Ahlak Bilgisi | Tüm konular | 19 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Türk Dili ve Edebiyatı | Tüm temalar | 54 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Matematik | Tüm konular | 20 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Fizik | Tüm konular | 24 | 192 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Kimya | Tüm konular | 31 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Biyoloji | Tüm konular | 14 | 112 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Tarih | Tüm konular | 13 | 104 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Coğrafya | Tüm konular | 19 | 152 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | İngilizce | Tüm temalar | 192 | 1.536 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Din Kültürü ve Ahlak Bilgisi | Tüm konular | 20 | 160 | ✅ AI-only doğrulandı; insan onayı yok |

Beş bağımsız ders paketinde toplam **116 konu anlatımı ve 2.500 soru** vardır.
Ortak soru bankası bunlardan ders başına 400 soru seçen bir derlemedir; 2.000
yeni soru olduğu iddia edilmez. Kaynak paketlerdeki 477 görselli sorunun tamamı
ortak bankada korunur. Altı paket de
Question Contract 2.2 kullanır; soru kayıtlarında `hints` alanı bulunmaz.
Her soru geçerli bir konu anlatımına bağlıdır.

Yedi bağımsız 6. sınıf ders paketinde toplam **168 konu anlatımı ve 3.500 soru**
vardır. Ortak 6. sınıf soru bankası yeni soru üretmez: Matematik, Fen, Türkçe,
İngilizce ve Sosyal Bilgilerden 380'er; Bilişim ile Din Kültüründen 50'şer
soru seçer. Bütün 168 konu anlatımı ve kazanım korunur; doğru cevap konumları
500 / 500 / 500 / 500'dür.

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

Güncel yayın kanıtı:
[5. Sınıf Yayın Hazırlık Raporu](reports/GRADE5_RELEASE_READINESS.md) ve
[5. Sınıf 2.000 Soruluk Banka Hazırlık Raporu](reports/GRADE5_QUESTION_BANK_READINESS.md),
[6. Sınıf 2.000 Soruluk Banka Hazırlık Raporu](reports/GRADE6_QUESTION_BANK_READINESS.md),
[7–9. Sınıf Tamamlanan Dersler Yayın Hazırlık Raporu](reports/GRADE7_9_COMPLETED_COURSES_READINESS.md).

`tools/regen_*` ve `tools/migrate_*` dosyaları geçmiş onarımların
tekrarlanabilir kayıtlarıdır; yeni üretim girişi değildir. Yeni paketler
Question Contract 2.2 ile, `hints` alanı olmadan üretilir.

## Oyun paketleri

Bilgi Yarışması, Ülke–Başkent Hafızası ve Çarkıfelek v1 katalogları ayrı ayrı
9 dil × 4 yaş bandında 36 `.alika-game` paketi sunar. Bilgi Yarışması
paketlerinde 200 soru, Hafıza paketlerinde 100 eşleştirme çifti, Çarkıfelek
paketlerinde sistemin otomatik seçtiği 200 kelime vardır. Kaynaklar, paket
karmaları ve inceleme durumu için [`games/README.md`](games/README.md) ve
[`reports/TRIVIA_V1_READINESS.md`](reports/TRIVIA_V1_READINESS.md) belgelerine
bakın. Bu ilk katalog insan kültürel incelemesi tamamlanana kadar
**AI-only taslak** durumundadır.

## Lisans

İçerikler: [CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/)
Yasal belgeler: `legal/` klasöründe (telif hakkı saklıdır).
