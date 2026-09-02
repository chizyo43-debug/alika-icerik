# AliKa İçerik Paketleri

AliKa uygulaması için indirilebilir **ders notu + soru bankası** paketleri.

## Ülke yayınları

- **Türkiye:** `turkiye/` altında 5–12. sınıf ders paketleri.
- **Japonya:** `library/releases/JP/2026-09-01/` altında 43 güvenli-kapsam
  paket; 20.460 soru ve 949 konu anlatımı.
- **Kore:** `library/releases/KR/2026-09-01/` altında 94 güvenli-kapsam
  paket; 47.000 soru ve 2.162 konu anlatımı.
- **İngiltere (England):** `library/releases/GB/2026-09-02/` altında 42
  güvenli-kapsam ders paketi ile derslerden bağımsız 42 soru bankası; derslerde
  20.700, bankalarda 84.000 soru. Canlı konuşma performansı gerektiren 6
  kazanım yayımdan açıkça bekletilmiştir.

Japonya, Kore ve İngiltere yayınlarının kanonik işaretçileri sırasıyla
`library/curriculum/JP/current-publish-release.json` ve
`library/curriculum/KR/current-publish-release.json` ile
`library/curriculum/GB/current-publish-release.json` dosyalarıdır. Yalnız
`publishable=true`, boş `releaseBlockers` ve hash-bağlı denetim sonucu taşıyan
ZIP'ler yayımlanır. Güvenli kapsam dışında bırakılan kazanımlar kataloglarda
`withheldObjectives` olarak açıkça belirtilir.

Türkiye sesli içeriklerinin kanonik konuşmacısı ve yerel üretim yöntemi
[`voice/PRIMARY_VOICE.md`](voice/PRIMARY_VOICE.md) içinde tanımlıdır. Ham insan
sesi referansı Git'e girmez; yayımlanan kayıtlarda yalnız izin, model lisansı ve
SHA-256 kanıtı tutulur.

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
| Türkiye | 7 | Sosyal Bilgiler | Tüm konular | 17 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 7 | Din Kültürü ve Ahlak Bilgisi | Tüm konular | 17 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 7 | Tüm Dersler | Altı dersin dengeli seçkisi | 267 | 2.000 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 8 | Türkçe | Tüm beceriler | 170 | 628 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 8 | Matematik | Tüm konular | 23 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 8 | Fen Bilimleri | Tüm konular | 37 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 8 | İngilizce | Tüm temalar | 192 | 1.536 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 8 | T.C. İnkılap Tarihi ve Atatürkçülük | Tüm konular | 15 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 8 | Din Kültürü ve Ahlak Bilgisi | Tüm konular | 19 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 8 | Tüm Dersler | Altı dersin dengeli seçkisi | 278 | 2.000 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Türk Dili ve Edebiyatı | Tüm temalar | 54 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Matematik | Tüm konular | 20 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Fizik | Tüm konular | 35 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Kimya | Tüm konular | 31 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Biyoloji | Tüm konular | 28 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Tarih | Tüm konular | 28 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Coğrafya | Tüm konular | 31 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | İngilizce | Tüm temalar | 192 | 1.536 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Din Kültürü ve Ahlak Bilgisi | Tüm konular | 29 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 9 | Tüm Dersler | Dokuz dersin dengeli seçkisi | 312 | 2.000 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 10 | Matematik | Tüm konular | 21 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 10 | Fizik | Tüm konular | 22 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 10 | Kimya | Tüm konular | 21 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 10 | Biyoloji | Tüm konular | 19 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 10 | Türk Dili ve Edebiyatı | Tüm konular | 20 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 10 | Tarih | Tüm konular | 20 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 10 | Coğrafya | Tüm konular | 20 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 10 | İngilizce | Tüm temalar | 20 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 10 | Felsefe | Tüm konular | 20 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 10 | Din Kültürü ve Ahlak Bilgisi | Tüm konular | 20 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 10 | Tüm Dersler | On dersin dengeli seçkisi | 203 | 2.000 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 11 | Matematik | Tüm konular | 20 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 11 | Fizik | Tüm konular | 31 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 11 | Kimya | Tüm konular | 25 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 11 | Biyoloji | Tüm konular | 22 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 11 | Türk Dili ve Edebiyatı | Tüm konular | 32 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 11 | Tarih | Tüm konular | 22 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 11 | Coğrafya | Tüm konular | 38 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 11 | İngilizce | Tüm temalar | 64 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 11 | Felsefe | Tüm konular | 24 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 11 | Din Kültürü ve Ahlak Bilgisi | Tüm konular | 50 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 11 | Tüm Dersler | On dersin dengeli seçkisi | 318 | 2.000 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 12 | Matematik | Tüm konular | 21 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 12 | Fizik | Tüm konular | 27 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 12 | Kimya | Tüm konular | 24 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 12 | Biyoloji | Tüm konular | 20 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 12 | Türk Dili ve Edebiyatı | Tüm beceriler | 16 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 12 | T.C. İnkılap Tarihi ve Atatürkçülük | Tüm konular | 16 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 12 | Coğrafya | Tüm konular | 20 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 12 | İngilizce | Tüm temalar | 24 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 12 | Felsefe Grubu | Psikoloji, Mantık ve Sosyoloji | 33 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 12 | Din Kültürü ve Ahlak Bilgisi | Tüm konular | 20 | 500 | ✅ AI-only doğrulandı; insan onayı yok |
| Türkiye | 12 | Tüm Dersler | On dersin dengeli seçkisi | 201 | 2.000 | ✅ AI-only doğrulandı; insan onayı yok |

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

On bağımsız 11. sınıf ders paketinde toplam **328 konu anlatımı ve 5.000 soru**
vardır. Her soru GPT-5.6 Sol tarafından AI-only modunda incelenmiş onarım
manifestine ve geçerli bir konu anlatımına bağlıdır; insan onayı yoktur.
Paketlerin tamamı Question Contract 2.2 sıkı doğrulamasından 0 hata ve 0
uyarıyla geçer.

On bağımsız 12. sınıf ders paketinde toplam **201 konu anlatımı ve 5.000 soru**
vardır. Dersler, MEB'in indirilebilir 2025-2026 öğretim programlarına dosya
özeti ve PDF sayfa çapasıyla bağlanır. 12. sınıfta genel Tarih yerine resmî
T.C. İnkılap Tarihi ve Atatürkçülük programı; ayrı bir 12. sınıf Felsefe
programı yerine Psikoloji, Mantık ve 12. sınıf Sosyoloji çıktılarından oluşan
Felsefe Grubu kullanılır. Bütün bağımsız paketler ve 2.000 soruluk derleme
Question Contract 2.2 denetiminden 100/100 skor, 0 hata ve 0 uyarıyla geçer;
inceleme AI-only'dir ve insan onayı yoktur.

7, 8, 9, 11 ve 12. sınıf ortak bankalarının her biri, kanonik ders paketlerinden
konu anlatımı ve doğru cevap konumu dengesi korunarak seçilmiş **2.000 soru**
içerir. Bu bankalar yeni soru üretmez; kaynak soruları yeniden paketler ve
doğru cevap dağılımını 500 / 500 / 500 / 500 olarak korur.

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
