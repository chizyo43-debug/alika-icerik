# AliKa Projesi: Bilgi, Klasör Yolları ve Hedefler

Güncelleme: 19 Ekim 2026 — kopya haritası, Figure Spec kanonik yolu ve ölçülebilir hedef tablosu eklendi.

## Proje özeti

AliKa; ailelerin çocukların dijital yaşamını desteklemesi için geliştirilen, Windows ve Android uygulamaları bulunan bir ebeveyn kontrolü ve dijital iyi oluş ürünüdür. Eğitim içerikleri AliKa Atölye’de hazırlanır; atölye verileri uygulama kodundan ve yayınlanmış içerik depolarından ayrı tutulur.

Uzun vadeli eğitim hedefi, desteklenen ülkelerin müfredatlarına uygun, farklı dillere yerelleştirilebilen ders anlatımları, alıştırmalar, soru bankaları ve oyunlar üretmektir. Atölye kapsam belgesi 11 ülke/bölge ve okul sınıflarını tarif eder. Ülke, sınıf veya ders içeriğini yayıma hazır saymak için güncel resmî müfredat, kaynak, kalite ve yayın kontrolleri gerekir.

## Çalışma alanı ve ana klasörler

Ana çalışma alanı:

`C:\Users\Shadow\Desktop\AliKa_Projeleri\`

| Klasör | Görevi |
|---|---|
| `atolye\AliKa atölye\` | İçerik üretimi, müfredat araştırması, doğrulayıcılar, kalite testleri ve inceleme kanıtları. Bu belge bu klasördedir. |
| `urun\ebeveyn_kontrol\` | Windows ve Android uygulama deposunun (`alika`) ana Git köküdür. `urun\` ve `repolar\` altındaki güncel uygulama worktree'leri bu köke bağlıdır. Ayrıntı aşağıdaki kopya haritasındadır. |
| `repolar\` | `alika-play-0.3.10` hotfix worktree'si ile eski, ayrı `AliKa_release_candidate` klonu. Release candidate klonu 22 Ağustos 2026'da kalmıştır; yeni kod işi buradan başlatılmaz. |
| `icerik\` | Uygulamaya sunulan içerik paketlerinin ve bunlara ait ayrı checkout’ların bulunduğu alan. Hangi kopyanın yayın deposu olduğu ilgili indeks ve depo belgelerinden doğrulanır. |
| `site\` | AliKa ürün sitesi ve site prototiplerinin çalışma kopyaları. |
| `ses\` | Yerel metin-ses üretimi, seslendirme ve tanıtım medyası çalışma alanları. |
| `arsiv\` | Eski sürümler, yedekler ve tarihsel kanıtlar. Canlı kaynak depo olarak kullanılmaz. |

Klasörlerin görev yönlendirmesi için [AliKa çalışma alanı indeksi](<C:\Users\Shadow\Desktop\AliKa_Projeleri\PROJECT_INDEX.md>) temel başvuru noktasıdır. İndeksin uygulama deposu, içerik junction'ları ve `worktrees\` bölümleri 19 Ekim 2026'da bu belgedeki kopya haritasına göre güncellendi; dal ve commit ayrıntısı için aşağıdaki kopya haritası esas alınır. Farklı çalışma kopyaları aynı dosya adına veya benzer içeriğe sahip olabilir; eşit veya güncel oldukları varsayılmamalıdır.

## Kopya haritası

Ölçüm tarihi: 19 Ekim 2026. Dal ve commit bilgisi her işte değişebilir; işe başlamadan aşağıdaki kontrol komutlarıyla yenilenir.

### Uygulama deposu (`chizyo43-debug/alika`)

| Klasör | Bağlantı türü | Dal | Son commit | Kullanım |
|---|---|---|---|---|
| `urun\ebeveyn_kontrol\` | Ana Git kökü | `wip/windows-maskot-saat-devam` | `07728bdf` (2026-10-14) | Uygulama deposunun yerel kökü. Worktree listesi bu klasörden alınır. |
| `C:\Users\Shadow\Desktop\ebeveyn_kontrol\` | Junction → `urun\ebeveyn_kontrol\` | Aynı klasör | Aynı | Ayrı kopya değildir; AGENTS.md'deki Figure Spec yolu bu bağlantıyı kullanır. |
| GitHub `origin/main` | Uzak dal | `main` | `3a506d5f` (2026-10-19) | Güncel ana dal. Android `0.3.11` / `2026101601`. Görsel etkinlik (`visualChoice`) kodu bu dalda 18 dosyada bulunur. Yerel `main` referansı eskidir (`6215d483`, 2026-10-15); karşılaştırmadan önce `fetch` yapılır. |
| `urun\alika-kutuphane\` | Worktree | `duzeltme/kutuphane-test-1017` | `3a506d5f` (2026-10-19) | Kütüphane düzeltmeleri; ölçüm anında `origin/main` ile aynı commit. |
| `urun\alika-lgs\` | Worktree | `duzeltme/lgs-kapsam-unite-sinif` | `871b65aa` (2026-10-16) | LGS kapsam/ünite/sınıf düzeltmesi. |
| `urun\alika-kural15\` | Worktree | `duzeltme/distractor-why` | `de3c30d8` (2026-10-14) | Çeldirici gerekçesi düzeltmesi. |
| `urun\alika-store-1.2.11\` | Worktree | Detached HEAD | `276c1784` (2026-10-13) | Microsoft Store 1.2.11 paket noktası. |
| `repolar\alika-play-0.3.10\` | Worktree | `hotfix/play-0.3.10-monitoring-flag` | `d32a30f4` (2026-10-06) | Google Play 0.3.10 hotfix. |
| `worktrees\ebeveyn_kontrol-*` | 5 worktree | `ozellik/android-panel-menu`, `cizici-2.3-aktarim`, `ozellik/cocuk-odak-halkasi`, `tv/eski-oyunlari-kaldir`, `windows/kaldirma-isareti` | Değişken | Özellik dalları. |
| `repolar\AliKa_release_candidate\` | Ayrı klon | `codex/sol-flow-runtime-repair-2026-08-22` | `71483c5` (2026-08-22) | **Eski.** Çalışma ağacında `visualChoice` kodu yok, Figure Spec 1.1.0. Yeni kod işi ve sözleşme okuması için kullanılmaz. |

Bu tabloya ek olarak aynı köke bağlı başka worktree'ler de vardır: atölye içindeki `alika_figure_release_worktree\` (`codex/figure-spec-2`), `C:\Users\Shadow\Desktop\ebeveyn_kontrol\.claude\worktrees\` altındaki oturum worktree'leri ve `C:\cb\...\worktree` (`codex-bridge-bulut-pc`). Tam liste için aşağıdaki `worktree list` komutu çalıştırılır.

### İçerik, site ve atölye

| Klasör | Depo | Dal | Son commit | Kullanım |
|---|---|---|---|---|
| `icerik\alika-content-main\` | `alika-icerik` | `main` | `bb2b1e8` (2026-09-01) | İçerik yayın deposu. `C:\Users\Shadow\Desktop\alika-content-main` bu klasöre giden junction'dır; CONTENT_REPOSITORY.md'deki yol bu klasörün kendisidir. |
| `icerik\alika-content-jp-kr-20260901\` | `alika-icerik` | `codex/publish-jp-complete-question-banks-20260902` | `bb7c5b1` (2026-09-02) | Japonya/Kore tarihli yayın dalı. |
| `icerik\alika-icerik-catalog\` | `alika-icerik` | `main` | `be53d53` (2026-08-13) | Dar katalog kopyası; `alika-content-main` kopyasından eski. |
| `site\alika-site\` | `alika-site` | `codex/yeni-tasarim-ugur-stili` | `9b9053e` (2026-10-17) | alika.tr ürün sitesi. |
| `atolye\AliKa atölye\` | Yerel depo (uzak bağlantı yok) | `main` | `0ee0eb2` (2026-09-12) | İçerik atölyesi. Çalışma ağacında commit edilmemiş değişiklikler var; bu belge Git'te henüz izlenmiyor. |

### Kontrol komutları

```powershell
git -C "C:\Users\Shadow\Desktop\AliKa_Projeleri\urun\ebeveyn_kontrol" fetch origin
git -C "C:\Users\Shadow\Desktop\AliKa_Projeleri\urun\ebeveyn_kontrol" worktree list
git -C "<kopya klasörü>" status -sb
```

## Figure Spec kanonik yolu

AGENTS.md'ye göre görsel sözleşmenin kanonik dosyası:

`C:\Users\Shadow\Desktop\ebeveyn_kontrol\shared\figure_spec.json`

Bu yol `urun\ebeveyn_kontrol\` klasörüne giden bir junction'dır. Bu nedenle sabit bir sürümü değil, o klasörde **o an açık olan dalın** dosyasını gösterir. 19 Ekim 2026 ölçümünde bu dosya GitHub ana dalının bir sürüm gerisindeydi:

| Kaynak | Sürüm | `kind` sayısı | SHA-256 (ilk 12) | Durum |
|---|---|---|---|---|
| `origin/main` (`3a506d5f`) | 1.8.0 | 18 | `35fa897ea37a` | En güncel. 1.8.0; chart için `title`, `titleStyle`, `axisUnits`, table için `title`, `titleStyle`, `rowHeaderBold` ekledi. |
| AGENTS.md yolu = `urun\ebeveyn_kontrol\` (`07728bdf`) | 1.7.0 | 18 | `adb04b514af9` | Main'in bir sürüm gerisinde. |
| `repolar\alika-play-0.3.10\` | 1.3.0 | 13 | `4726ed8d8f75` | Hotfix dalı; üretim için kullanılmaz. |
| `repolar\AliKa_release_candidate\` | 1.1.0 | 10 | `3f776cb92cea` | Eski; üretim için kullanılmaz. |

Üretim veya doğrulamaya başlamadan önce kanonik yoldaki dosya ana dalla karşılaştırılır:

```powershell
git -C "C:\Users\Shadow\Desktop\AliKa_Projeleri\urun\ebeveyn_kontrol" fetch origin
git -C "C:\Users\Shadow\Desktop\AliKa_Projeleri\urun\ebeveyn_kontrol" diff --stat origin/main -- shared/figure_spec.json
```

Çıktı boşsa dosya ana dalla aynıdır. Çıktı varsa üretimin hangi Figure Spec sürümüne göre yapıldığı iş kaydına sürüm ve hash ile yazılır. Kanonik yolun eski bir sürümde kalması, yeni sürümde eklenen alanların kullanılamaması anlamına gelir. `release_candidate` ve hotfix kopyalarındaki eski sürümler sözleşme kaynağı sayılmaz.

## Atölye içindeki önemli yollar

Atölye kökü: `C:\Users\Shadow\Desktop\AliKa_Projeleri\atolye\AliKa atölye\`

- `ATOLYE_KAPSAM.md`: Ülke, sınıf, yaş ve ders kapsamı.
- `ATOLYE_PLAN.md`: İçerik üretim hattının tasarımı ve aşamaları.
- `STATUS.md`: Atölye görevlerinin kaydedilmiş son durumu.
- `CONTENT_REPOSITORY.md`: Üretim çalışma alanı ile içerik yayın depolarının ayrımı.
- `library\curriculum\`: Ülke ve bölge müfredat kayıtları.
- `library\sources\`: Kaynak araştırması ve referans kayıtları.
- `library\schemas\`, `library\tools\`, `library\tests\`: Veri biçimleri, üretim/doğrulama araçları ve testler.
- `library\registry\question-bank-worklist.json`: Sınıf soru bankalarının kanonik çalışma listesi.
- `library\reviews\`: İnceleme ve kabul kanıtları.
- `library\releases\`: Hazırlanmış içerik sürümleri ve yayın kayıtları.
- `library\work\supplemental\global-visual-u9-500\`: 9 yaş altına yönelik 500 dil bağımsız görsel etkinliğin kaynak ve çalışma dosyaları.
- `library\work\supplemental\global-visual-u9-500\runtime\global-visual-u9-500-runtime.zip`: AliKa içe aktarma biçimine dönüştürülmüş runtime paketi.
- `library\reviews\global-visual-u9-integration-2026-09-08\`: Bu 500 etkinliğin Android/Windows entegrasyonu ve cihaz testine dair son belgelenmiş kabul kanıtları.

## Şu an odaklandığımız görsel etkinlik çalışması

Amaç, okuma yazma gerektirmeyen ve çocukların yalnızca görsellere bakarak çözebileceği 500 kısa etkinliği AliKa’ya uyumlu biçimde kullanmaktır. Etkinlikler bir dile bağlı yönerge veya yazılı şık gerektirmeyen örüntü, eşleştirme, yansıtma, döndürme ve şekil ilişkileri gibi görsel görevlerden oluşur.

Uygulamadaki hedef akış, iki örnek görseli ve bir görsel soruyu gösterir; çocuk dört resimli seçenekten birini seçer. Etkinlikte sayaç zaman aşımı ve yanlış cevaba bağlı süre kaybı uygulanmaz. Doğru cevap, ebeveynin belirlediği ödül ayarlarına göre süre kazandırır. Aynı etkinliğin tekrar çözülmesi ikinci bir ödül oluşturmamalıdır.

Son belgelenmiş teknik kabul 8 Eylül 2026 tarihli rapordadır. Bu rapora göre runtime paketinde 500 kayıt bulunmuş; Android’de 79 birim testi, Windows’ta ilgili test grubu ve X8 cihazında bir uçtan uca deneme başarıyla tamamlanmıştır. X8 denemesinde içe aktarma, doğru/yanlış seçim, zaman aşımı uygulanmaması ve tekrar ödülün engellenmesi kontrol edilmiştir. Cihaz denemesi ana uygulamada değil, ayrı `com.alika.parental.fentest` paketinde yapılmıştır. 19 Ekim 2026 itibarıyla görsel etkinlik kodu uygulama deposunun `main` dalındadır.

Bu teknik kabul, etkinliklerin müfredat onayı, pedagojik uzman incelemesi veya yayın izni aldığı anlamına gelmez. Belgelenmiş içerik durumu insan incelemesi bekliyor. Ürünün ana Android uygulamasının Google Play’deki kapalı test sürümüne dağıtımı ayrı bir sürüm/yayın adımıdır; test amaçlı APK kurulumu yayın yerine geçmez. Windows tarafında kod ve test kanıtı mevcut olsa da son rapor kurulu Windows uygulamasında saha kabulinin yapılmadığını belirtir.

Veri yapısına dair 19 Ekim 2026 ölçümü: 500 kaydın tamamı 3×3 ızgara kullanır. 491 kayıtta en az bir yanlış seçenek doğru cevaptan yalnız bir hücre farklıdır. Beş adımlı ipucu dizisi 500 kayıtta aynıdır. Doğru seçenek konumu dengelidir (her konumda 125).

## Hedefler

Her hedef, bitti sayılması için ölçülebilir bir ölçüt ve kanıt yeri taşır. Durum sütunu, belirtilen tarihteki son kanıta dayanır. Hedef tarihleri ürün sahibi belirler; “Belirlenmedi” yazan hedef henüz takvime bağlanmamıştır.

### Şimdi: 500 görsel etkinlik

| # | Hedef | Bitti sayılma ölçütü | Durum (kanıt tarihi) | Kanıt yeri | Hedef tarih |
|---|---|---|---|---|---|
| H1 | Ana Android uygulamasında kabul | Yayın imzalı `com.alika.parental` sürümünde veri koruyan yükseltme yapılır. 500 kaydın içe aktarılması, doğru/yanlış seçim, zaman aşımı olmaması ve tekrar ödülün reddedilmesi cihazda geçer. | Kod `main` dalında (2026-10-19). Cihaz kabulü yalnız `fentest` paketinde (X8, 2026-09-08). Ana paket imza uyuşmazlığı nedeniyle kurulmadı. Android APK'sı Android işleri tamamlandığında derlenir. | `library\reviews\global-visual-u9-integration-2026-09-08\ACCEPTANCE.md` ve yeni kabul klasörü | Belirlenmedi |
| H2 | Windows saha kabulü | Kurulu Windows uygulamasında H1'deki dört kontrol geçer ve kanıt klasörüne yazılır. | Görev test grubu 95 geçti, 1 atlandı. Kurulu uygulamada saha turu yok (2026-09-08). | Aynı rapor ve yeni kabul klasörü | Belirlenmedi |
| H3 | İnsan ve çocuk incelemesi | 500/500 kayıtta `humanReviewed=true` olur ve `reviewStatus` artık `pending` değildir. Yaş bantları çocuk denemesiyle doğrulanır; `agePlacement` artık `editorial-not-child-validated` değildir. | 0/500 incelendi; 500/500 yaş bandı yalnız editoryal (2026-10-19). | `global-visual-u9-500\questions.jsonl` | Belirlenmedi |
| H4 | Yayına açma | Runtime `audit.json` içinde `publishable=true` olur ve `nativeRuntimeAcceptance` artık `pending` değildir. H1–H3 tamamlanmadan açılmaz. | `publishable=false`, `nativeRuntimeAcceptance=pending` (2026-10-19). | `global-visual-u9-500\runtime\audit.json` | Belirlenmedi |

### Sonraki: Türkiye 5. sınıf ilk tam dikey dilim

| # | Hedef | Bitti sayılma ölçütü | Durum (kanıt tarihi) | Kanıt yeri | Hedef tarih |
|---|---|---|---|---|---|
| H5 | TR 5. sınıfın uçtan uca yayın kabulü | Yayımlanabilir bütün TR 5 dersleri ders paketi kabulünü geçer. Bu dersleri kapsayan tam 2.000 soruluk karma sınıf bankası üretilir. TR 5, `question-bank-worklist.json` içinde `release-ready` olarak yer alır. | Yerel ders kapsamı 3: Fen Bilimleri, Matematik, Türkçe. Sosyal Bilgiler onarımda. TR 5 çalışma listesinde yok; sınıf bankası kabulü yok (2026-09-12). | `STATUS.md`, `library\registry\question-bank-worklist.json` | Belirlenmedi |
| H6 | TR 5 Türkçe bankasını yayına hazırlamak | SHA-256 `8c9f6127…` adayı için insan editoryal incelemesi, Windows kabulü, Android kabulü, ses/ASR kabulü ve yayın onayı tamamlanır; `publishReady=true` olur. | İçerik onarımı 263/263; strict 0 hata/0 uyarı. Dört dış kapı açık (2026-09-12). | `STATUS.md`, `staging\turkce-local\turkce-bank-final-candidate.jsonl` | Belirlenmedi |
| H7 | TR 5 Sosyal Bilgiler yerel adayı | 345 banka sorusunda gerçek `semanticCase`/`semanticFamilyKey` denetimi biter. Siyasi harita kaydı AGENTS.md harita kapılarıyla Figure Spec'e uyar. Strict sonuç 0 hata olur. | İki madde açık; daha yeni kayıt yok (2026-09-12). | `STATUS.md`, Sosyal Bilgiler iş kartı worktree'si | Belirlenmedi |

### Uzun vade: ülke kapsamı

| # | Hedef | Bitti sayılma ölçütü | Durum (kanıt tarihi) | Kanıt yeri | Hedef tarih |
|---|---|---|---|---|---|
| H8 | 11 ülke/bölgenin sınıf bankaları | Kapsamdaki her yayımlanabilir ülke × sınıf, `question-bank-worklist.json` içinde `release-ready` olur. | 31 sınıf `release-ready`: GB 8, JP 8, KR 8, RU 7. TR, US, BR, DE, FR, ES ve PT listede yok; US kapsamı `blocked-scope-not-defined` (2026-10-19). | `library\registry\question-bank-worklist.json`, `ATOLYE_KAPSAM.md`, `library\reviews\quality-program-20260905\GLOBAL-REPAIR-QUEUE.md` | Belirlenmedi |

### Süreklilik: belge ve çalışma alanı

| # | Hedef | Bitti sayılma ölçütü | Durum (kanıt tarihi) | Kanıt yeri | Hedef tarih |
|---|---|---|---|---|---|
| H9 | Güncel durum kaydı | Her iş kartı kapandığında `STATUS.md` dosyasına tarihli bir kayıt eklenir. Bu belgedeki kopya haritası ve Figure Spec tablosu ölçüm tarihiyle yenilenir. | `STATUS.md` son kaydı 2026-09-12; Sosyal Bilgiler kartının sonucu kayıtlı değil. Kopya haritası 2026-10-19. | `STATUS.md`, bu belge | Sürekli |
| H10 | Figure Spec eşitliği | Kanonik yoldaki dosya `origin/main` ile aynıdır; yukarıdaki `diff --stat` komutu boş çıktı verir. | Kanonik yol 1.7.0, `main` 1.8.0 (2026-10-19). | Bu belgedeki Figure Spec tablosu | Belirlenmedi |

## Çalışma ve yayın ilkeleri

1. Uygulama kodu ana ürün deposunda, eğitim verisi atölye/içerik depolarında tutulur. Eğitim paketi uygulama kodu veya çalıştırılabilir eklenti içermez.
2. Her işe başlamadan önce hedef depo ve klasör belirlenir; o kopyanın talimat, durum ve Git kayıtları kontrol edilir. Uygulama kodu için hedef kopya yukarıdaki kopya haritasından seçilir; `repolar\AliKa_release_candidate` kullanılmaz.
3. İçerik üretimi güncel ve resmî kaynaklarla temellendirilir. Kaynak, kapsam ve kalite kanıtı saklanır.
4. Görsel soru biçimi paylaşılan Figure Spec ve yönlendirme kayıtlarına uyar; desteklenmeyen şekil türleri üretilmez. Kullanılan Figure Spec sürümü ve hash'i iş kaydına yazılır.
5. Teknik test başarısı tek başına pedagojik veya yayın kabulü sayılmaz. İnsan incelemesi ve içerik yayın kapıları ayrıca tamamlanır.
6. Sonuçlar ölçülebilir test, cihaz veya paket kanıtıyla raporlanır; tamamlanmamış doğrulamalar açıkça belirtilir.

## Başvuru belgeleri

- Atölye kapsamı: [ATOLYE_KAPSAM.md](ATOLYE_KAPSAM.md)
- Atölye üretim planı: [ATOLYE_PLAN.md](ATOLYE_PLAN.md)
- Atölye kayıtlı durumu: [STATUS.md](STATUS.md)
- Atölye içerik deposu ayrımı: [CONTENT_REPOSITORY.md](CONTENT_REPOSITORY.md)
- Ortak üretim kuralları: [AGENTS.md](AGENTS.md)
- Sınıf soru bankası çalışma listesi: [question-bank-worklist.json](library/registry/question-bank-worklist.json)
- Ana çalışma alanı indeksi: [PROJECT_INDEX.md](<C:\Users\Shadow\Desktop\AliKa_Projeleri\PROJECT_INDEX.md>) — uygulama bölümü 2026-10-19'da güncellendi.
- 500 görsel etkinlik teknik kabul raporu: [ACCEPTANCE.md](library/reviews/global-visual-u9-integration-2026-09-08/ACCEPTANCE.md)
