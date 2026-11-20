# AliKa Yeni İçerik Üretim Sistemi — Yerel PC Antigravity Devir ve Kurulum Planı

> **Amaç:** Mevcut canlı `chizyo43-debug/alika-icerik` kalite çıtasını (**Question/Note 2.2**, özgün pedagojik çeldiriciler, Şerit-A şekiller, `ai-verified` izlenebilirliği) koruyarak üretim maliyetini ve düzeltme turlarını ciddi biçimde düşürmek; tüm resmî kaynakları **Google Drive + ülke bazlı ayrı NotebookLM defterleri + Google ekosistemi araçları** üzerine taşımak.
>
> **Hedef Çalışma Ortamı:** Tüm resmî kaynak PDF'lerinin bulunduğu **Yerel PC** (Antigravity). Bu belge doğrudan Yerel PC'deki Antigravity'ye başlangıç görevi olarak verilebilir.

---

## 1. Kalite Sözleşmesi (Değişmez Çıta)

Yeni sistem aşağıdaki canlı `chizyo43-debug/alika-icerik` (`main`) kurallarından **asla** taviz vermez:

- **Format:** Question/Note 2.2 JSONL, paket başına en çok **500 soru** (dönem/ünite bölünmüş), `CC BY-NC 4.0`.
- **Gösterim & Biçim:** `alika-ami/1` (`__altı çizili__`), bağlam ayrı `context` alanında, öncüller `I. II. III.`, şekiller `dogrulayici/shared/figure_spec.json` uyumlu (Şerit-A katalog şekil varken raster yasak).
- **Pedagojik Kalite:** Her soru benzersiz bağlam/kök; 1–5 seviye dengesi; dengeli A/B/C/D dağılımı; her şık için **o sorunun özel hatasını teşhis eden** `distractorWhy` (kalıp/tekrarlı cümle yasak).
- **Zorunlu Kapılar:**
  1. `python dogrulayici/tools/pack_validate.py <paket.jsonl>` → **0 HATA**
  2. Mevcut paket değiştiyse başlıkta `version + 1`
  3. `python dogrulayici/kontrol.py --katalog-yaz`
  4. `python dogrulayici/kontrol.py` → **yeni HATA 0**
- **İnceleme:** `reviewStatus: "ai-verified"`, `humanReviewed: false`, karar belgesi SHA-256 (`reviewDecisionSha256`) ve ülke dilinde `disclosure`.

---

## 2. Google Aboneliğine Dahil Araçların Üretime Entegrasyonu

| Google Aracı | Üretim Sistemindeki Rolü | Neden Maliyeti Düşürür / Kaliteyi Artırır? |
|---|---|---|
| **NotebookLM** *(Pro: 300 kaynak/defter, 500 defter; Ultra: 500–600 kaynak/defter; tek dosya 200 MB / 500 bin kelime)* | **Ülke bazlı Resmî Müfredat & Kaynak Beyni.** Her ülke için ayrı defterde PDF'lerden sayfa atıflı ünite brifi, kazanım sınırları, kavram yanılgısı tablosu ve müfredat denetimi çıkarır. | 100+ sayfalık PDF'ler kodlama ajanlarına tekrar tekrar okutulmaz; abonelik dahilinde sıfıra yakın ek maliyetle halüsinasyon ve kapsam aşımı önlenir. |
| **Google Drive** | **Tek Merkezi Kaynak Havuzu.** Yerel PC'deki tüm resmî PDF'lerin ülke klasörlü arşivi (`AliKa-Kaynaklar/`). NotebookLM kaynakları doğrudan Drive'dan bağlanır. | Yerel PC ↔ Bulut PC ↔ NotebookLM senkronu sağlar; Google Docs olarak tutulan kurallar NotebookLM'de tek tıkla güncellenir. |
| **Gemini Özel Gem'ler** *(NotebookLM Defterine Bağlı)* | **Ülke Bazlı Uzman Asistanlar.** Her ülkenin NotebookLM defteri doğrudan ilgili Gem'e kaynak olarak bağlanır (normalde 10 dosya olan sınır defter üzerinden 300–600 kaynağa çıkar). | Tekrar kullanılabilir sabit sistem talimatıyla (Şema 2.2 + AMI + çeldirici kuralları) tutarlı taslak, not ve ön denetim üretir. |
| **Gemini Deep Research** | **Yeni Ülke Resmî Kaynak Keşfi.** Yeni ülkeye geçerken bakanlık müfredat PDF'lerini, yürürlük tarihlerini, sınıf karşılıklarını ve hassas konu kurallarını kaynak URL'li raporlar. | İstasyon 1 araştırma süresini saatlerden dakikalara indirir; yanlış/eski müfredat riskini azaltır. |
| **Google Sheets** | **Ortak Üretim ve Kalite Panosu.** `Ülke × Sınıf × Ders × Dönem × Paket Sürümü × Kaynak SHA-256 × Defter Adı × Durum` canlı matrisi. | Yerel PC ve Bulut PC aynı tabloyu görür; eksik ünite/sürüm/kapı takibi tek yerden yapılır. |
| **Google Docs** | **Canlı Standart Belgeleri.** Şema 2.2 özeti, Figure Spec kuralları, çeldirici yazım kılavuzu ve ülke hassas konu kuralları. | Drive → NotebookLM bağlantısıyla tek güncelleme tüm defterlere yansır. |
| **NotebookLM Studio** *(Veri Tablosu, Çalışma Rehberi, Audio/Video Overview)* | Kazanım–ünite karşılaştırma tabloları ve ders notu özet taslakları (bonus: `medya/` tanıtım/ders videosu senaryo hammaddesi). | Ekstra araç gerektirmeden yapılandırılmış özet çıktılar verir. |
| **Google AI Studio / Gemini API** *(Opsiyonel API katmanı)* | Yüksek hacimli otomatik JSONL üretimi ve bağımsız 2. göz hakemlik için **Context Caching + Batch API (%50 indirim) + Structured Outputs**. | Tekrarlanan şema/brif token maliyetini %75–90'a kadar düşürür; `alika_pipeline/providers.py` içine bağlanabilir. |

---

## 3. Ülke Bazlı İzolasyon Mimarisi (Karmaşayı Sıfırlama)

**Temel Kural:** Farklı ülkelerin müfredatları **asla** aynı NotebookLM defterine karıştırılmaz. Aynı ülke içinde yürürlükte iki farklı müfredat varsa (ör. Türkiye'de TYMM ile 2018 programı), kaynak sayısı veya karışma riski arttığında defter müfredata göre bölünür.

### 3.1 Google Drive Klasör Ağacı

```text
Google Drive/
└── AliKa-Kaynaklar/
    ├── 00-Ortak-Standartlar/              # Google Docs (Şema 2.2, AMI, Figure Spec, Çeldirici Kılavuzu)
    ├── 01-TR-Turkiye/
    │   ├── TYMM-5-6-7/                    # 5, 6, 7. sınıf TYMM resmî PDF'leri
    │   ├── MEB-2018-8-ve-Ing7/            # 8. sınıf ve 7. sınıf İngilizce 2018/2019 PDF'leri
    │   ├── LGS-2027-2028/                 # MEB Bağlam Temelli Soru Kılavuzu + LGS kapsam/örnekler
    │   └── Ders-Kitaplari-ve-Kilavuzlar/
    ├── 02-JP-Japonya/
    │   ├── Gakushu-Shido-Yoryo-H29/       # 中学校学習指導要領（平成29年告示）+ 해설 PDF'leri
    │   └── Sinif-Yerlestirme-Kararlari/   # 社会 vb. sınıf yerleştirme kuralları (Google Docs)
    ├── 03-KR-Guney-Kore/
    │   ├── 2022-Gaejeong-Program/         # 2022 개정 교육과정 PDF'leri (7–9. sınıf)
    │   ├── Pyonsujaryo-Hassas-Terimler/   # 편수자료 + hassas konu onay kuralları (독도, 동해 vb.)
    │   └── Yayinevi-Sinif-Esleme/         # 9. sınıf 2027 ön hazırlık & sınıf eşleme tabloları
    └── 99-Yeni-Ulkeler/                   # Gelecek ülkeler: 04-DE-Almanya/, 05-GB-Ingiltere/ vb.
```

### 3.2 NotebookLM Defter Yapısı (Başlangıçta 3 veya 4 Defter)

| Defter Adı | Drive Kaynak Klasörü | Kapsam & Not |
|---|---|---|
| **`AliKa-TR-TYMM-5-7`** | `01-TR-Turkiye/TYMM-5-6-7/` + `LGS-2027-2028/` + `00-Ortak-Standartlar/` | **Tavsiye:** Türkiye'de 5–7 (TYMM) ile 8. sınıf (2018) müfredatları farklı olduğu için iki ayrı TR defteri sıfır müfredat karışması sağlar. |
| **`AliKa-TR-2018-8-LGS`** | `01-TR-Turkiye/MEB-2018-8-ve-Ing7/` + `LGS-2027-2028/` + `00-Ortak-Standartlar/` | 8. sınıf tüm dersler + 7. sınıf İngilizce + LGS 2027. |
| **`AliKa-JP-Ortaokul-7-9`** | `02-JP-Japonya/` + `00-Ortak-Standartlar/` | Japonya ortaokul 7–9. sınıf (`sugaku`, `rika`, `kokugo`, `eigo`, `shakai-*`). |
| **`AliKa-KR-Ortaokul-7-9`** | `03-KR-Guney-Kore/` + `00-Ortak-Standartlar/` | Güney Kore ortaokul 7–9. sınıf (`suhak`, `gwahak`, `gugeo`, `yeongeo`, `sahoe`, `yeoksa`) + `편수자료` hassas konu kuralları. |
| **`AliKa-<ISO>-Ortaokul`** *(gelecek)* | `99-Yeni-Ulkeler/<ISO>/` + `00-Ortak-Standartlar/` | Her yeni ülke kendi izole defterini alır. |

### 3.3 Zorunlu PDF Dosya Adlandırma Kuralı

NotebookLM alıntılarının doğrudan `sourceRefs` ve `objectiveEvidenceId` alanlarıyla eşleşmesi için yüklemeden önce tüm dosyalar standart adlandırılır:

```text
<ULKE>_<PROGRAM>_<SINIF>_<DERS>_<BELGE_TURU>_<YIL>.pdf
Örnek:
TR_TYMM_7_FenBilimleri_Program_2024.pdf
TR_2018_8_Matematik_Program_2018.pdf
JP_H29_7-9_Sugaku_Kaisetsu_2017.pdf
KR_2022_7-9_Gwahak_Program_2022.pdf
```

---

## 4. Yeni 7 İstasyonlu Hibrit Üretim Akışı

1. **İstasyon 0 (Yeni Ülke):** Gemini Deep Research ile resmî bakanlık PDF'leri bulunur, Yerel PC'ye indirilir, SHA-256 kaydı `source-register.json` dosyasına yazılır ve Drive'a yüklenir.
2. **İstasyon 1–2 (NotebookLM → `unit-brief.json`):** Ülke defterinde her ders/ünite için standart istemle tek seferlik kompakt bir **Ünite Brifi** çıkarılır:
   - Resmî kazanım kodları + PDF sayfa numaraları (`objectiveEvidenceId`)
   - **Kapsam İçi / Kapsam Dışı (Yasaklı Üst Sınıf)** sınırları
   - Resmî tanımlar ve kritik terminoloji uyarıları
   - Her kazanım için **5–10 gerçek öğrenci kavram yanılgısı** *(doğrudan `distractorWhy` hammaddesi)*
   - Hassas konu kuralları
3. **İstasyon 3A (Deterministik Python — $0):** Matematik ve Fen'in hesaplamalı sorularında sayı üretimi, doğru cevap, hatalı işlem çeldiricileri ve `figure_spec.json` uyumlu Şerit-A şekil JSON'u Python ile üretilir.
4. **İstasyon 3B (Sözel/Bağlamsal Üretim):** Dev PDF yerine yalnızca kompakt `unit-brief.json` + Şema 2.2 kuralları modele verilir (50–100 soruluk partiler, paket başı en çok 500 soru). Toplu işlerde Gemini API **Context Caching + Batch API** kullanılır.
5. **İstasyon 4 (Yerel Doğrulayıcı — $0):** `python dogrulayici/tools/pack_validate.py` çalıştırılır; yalnızca hata veren satırlar onarılır.
6. **İstasyon 5 (Bağımsız Hakem + NotebookLM Denetimi):** Üreticiden farklı model ailesi soruları bağımsız çözer ve pedagojik/dil kontrolü yapar. Şüpheli veya hassas sorular ülke NotebookLM defterine sorulup *"resmî PDF sınırını aşan ifade var mı?"* kontrolüyle doğrulanır; `ai-verified` damga ve karar SHA-256'sı basılır.
7. **İstasyon 6 (Yayın):** Değişen paketlerde `version + 1`, `python dogrulayici/kontrol.py --katalog-yaz`, `python dogrulayici/kontrol.py`, PR ile `chizyo43-debug/alika-icerik` `main` dalına birleştirme.

---

## 5. Yerel PC Antigravity İçin Adım Adım Uygulama Planı

> **Yerel PC Antigravity'ye Talimat:** Aşağıdaki fazları sırayla uygula. Her faz sonunda kullanıcıya kısa, kanıtlı özet ver ve sonraki faza onay al.

### Faz 1 — Yerel Kaynak Envanteri ve Düzenleme (1. Oturum)
1. Yerel PC'deki tüm resmî müfredat, ders kitabı, kılavuz ve sınav PDF'lerini tara (`atolye/AliKa atölye/library/sources/` ve kullanıcıdaki diğer yerel klasörler).
2. Her dosya için `ülke`, `program`, `sınıf`, `ders`, `belge_türü`, `dosya_boyutu`, `sayfa_sayısı`, `sha256` ve `orijinal_yol` bilgilerini içeren **`kaynak-envanteri.json`** ve **`.csv`** oluştur.
3. Kopyaları temizle, 200 MB üstü PDF varsa (NotebookLM sınırı) bölüm bazlı bölünmesi gerekenleri işaretle.
4. Dosyaları §3.1'deki `TR/`, `JP/`, `KR/` klasör düzeni ve §3.3 adlandırma kuralıyla yerel bir aktarım klasöründe (`AliKa-Kaynaklar/`) hazırla (orijinal dosyaları silmeden kopyala/düzenle).

### Faz 2 — Google Drive + Ülke Bazlı NotebookLM Kurulumu (2. Oturum)
1. Hazırlanan `AliKa-Kaynaklar/` ağacını Google Drive'a yükle.
2. `00-Ortak-Standartlar/` altına canlı `alika-icerik` reposundan özetlenmiş 3 Google Docs belgesi oluştur:
   - `AliKa-Sema-2.2-ve-AMI-Kurallari`
   - `AliKa-Figure-Spec-Serit-A-Rehberi`
   - `AliKa-Celdirici-ve-Pedagoji-Standartlari`
3. Ülke bazlı ayrı NotebookLM defterlerini aç ve ilgili Drive klasörlerini bağla:
   - `AliKa-TR-TYMM-5-7`
   - `AliKa-TR-2018-8-LGS`
   - `AliKa-JP-Ortaokul-7-9`
   - `AliKa-KR-Ortaokul-7-9`
4. Her defterde standart **`unit-brief` çıkarma istemi**ni bir test ünitesiyle doğrula.

### Faz 3 — Özel Gem'ler + Google Sheets Takip Panosu + Pipeline Entegrasyonu (3. Oturum)
1. Her ülke defterine bağlı 1'er **Gemini Özel Gem** oluştur (`AliKa-TR-TYMM-Uretici`, `AliKa-TR-LGS-Uretici`, `AliKa-JP-Uretici`, `AliKa-KR-Uretici`).
2. `Google Sheets` üzerinde merkezi **`AliKa-Uretim-ve-Kalite-Panosu`** tablosunu oluştur ve canlı `KATALOG.json`'daki 170 paketi başlangıç satırları olarak içe aktar.
3. Atölye tarafındaki `library/alika_pipeline/` içine `unit-brief.json` girdi okuyucu ve istenirse `providers.py` içine **Gemini Context Caching + Batch API** sağlayıcısı ekle.

### Faz 4 — Pilot Test ve Maliyet/Kalite Kıyaslaması (4. Oturum)
1. Seçilecek **1 somut pilot paket** üzerinde yeni 7 istasyonlu akışı uçtan uca çalıştır.
2. Çıktıyı canlı doğrulayıcıdan geçir (`pack_validate.py` 0 HATA, `kontrol.py` yeni HATA 0).
3. Eski yöntemle kıyaslama raporu çıkar: **soru başına maliyet, toplam süre, doğrulayıcı ilk geçiş oranı, çeldirici özgünlüğü**.

---

## 6. NotebookLM'de Kullanılacak Standart `unit-brief` İstemi (Hazır Şablon)

Her yeni üniteye başlamadan önce ilgili ülkenin NotebookLM defterine aşağıdaki istem verilir ve çıktısı yerel `unit-brief.json` dosyasına kaydedilir:

```text
Yalnızca bu defterdeki resmî müfredat ve kılavuz kaynaklarına dayanarak
[SINIF] [DERS] — [ÜNİTE ADI] için ünite üretim brifi hazırla.
Kaynakta geçmeyen hiçbir bilgi ekleme; her maddenin yanına kaynak dosya adı ve sayfa numarasını yaz.

Çıktıyı şu 6 başlıkta ver:
1. Resmî Kazanım Listesi: Her kazanım için kod, tam metin, kaynak dosya + sayfa no.
2. Kapsam İçi (Kesin İşlenecek) Alt Başlıklar ve Resmî Tanımlar.
3. Kapsam Dışı / Yasaklı Sınırlar: Bu sınıfta VERİLMEYECEK kavram, formül veya üst sınıf konuları (resmî sınırlama notlarıyla).
4. Tipik Öğrenci Kavram Yanılgıları: Her kazanım için en az 4–6 somut hata/yanılgı (çoktan seçmeli çeldirici ve distractorWhy kaynağı olacak).
5. Hassas Konu / Resmî İfade Kuralları: Varsa kesin kullanılması gereken resmî terimler.
6. Görsel/Şekil Önerileri: Hangi kazanımlar tablo, grafik, sayı doğrusu, koordinat, diyagram veya geometri şekliyle daha iyi ölçülür?
```
