# AliKa çalışma alanı — proje ve dosya indeksi

Bu dosya `AliKa_Projeleri` altındaki uygulama, içerik, web ve medya işlerinin nerede olduğunu gösterir. Harita 2026-09-29 tarihinde çıkarıldı; uygulama deposu, içerik junction'ları ve `worktrees/` bilgileri 2026-10-19'da yeniden ölçülerek güncellendi. Git dalı ve çalışma durumu değişebilir; güncel dal/commit tablosu [PROJE_BILGISI_VE_HEDEFLER](<atolye/AliKa atölye/PROJE_BILGISI_VE_HEDEFLER.md>) içindeki kopya haritasındadır. Aynı ürünün farklı klasörlerde duran kopyaları vardır: benzer `README.md` dosyaları bu kopyaların eşitlendiğini göstermez. Bir kopyada işe başlamadan önce kendi `AGENTS.md`, durum belgesi ve `git status -sb` çıktısını kontrol et.

## Bir işe nereden başlanır?

| Yapılacak iş | Başlangıç klasörü | Önce aç |
|---|---|---|
| Windows/Android AliKa uygulama kodu | [`urun/ebeveyn_kontrol`](<urun/ebeveyn_kontrol/>) (Git kökü) ve ona bağlı worktree'ler; önce `git fetch origin` ve `git worktree list` | [README](<urun/ebeveyn_kontrol/README.md>), [CODE_INDEX](<urun/ebeveyn_kontrol/CODE_INDEX.md>), [DURUM](<urun/ebeveyn_kontrol/DURUM.md>), [AGENTS](<urun/ebeveyn_kontrol/AGENTS.md>) |
| Eski uygulama klonu (yalnız tarihsel başvuru) | [`repolar/AliKa_release_candidate`](<repolar/AliKa_release_candidate/>) | 2026-08-22'de kalmış ayrı klon; yeni kod işine buradan başlama |
| Eğitim içeriği üretme ve kalite kontrolü | [`atolye/AliKa atölye`](<atolye/AliKa atölye/>) | [ATOLYE_KAPSAM](<atolye/AliKa atölye/ATOLYE_KAPSAM.md>), [STATUS](<atolye/AliKa atölye/STATUS.md>), [CONTENT_REPOSITORY](<atolye/AliKa atölye/CONTENT_REPOSITORY.md>), [library/README](<atolye/AliKa atölye/library/README.md>) |
| Uygulamaya yayınlanan ders/soru/oyun paketleri | [`icerik`](<icerik/>) | İlgili deponun [README](<icerik/alika-content-main/README.md>) ve [şeması](<icerik/alika-content-main/SCHEMA_V2.md>) |
| Ürün web sitesi | [`site/alika-site`](<site/alika-site/>) | [README](<site/alika-site/README.md>), `src/main.tsx` |
| TTS, seslendirme veya tanıtım videosu | [`ses`](<ses/>) | Aşağıdaki “Ses ve medya” haritası |
| Arşiv, yedek veya eski yayın | [`arsiv`](<arsiv/>) | Aşağıdaki “Arşiv ve referans dosyaları” bölümü; canlı kaynak kabul etme |

## Çalışma alanının üst haritası

| Klasör | Ne var? |
|---|---|
| `repolar/` | `alika-play-0.3.10` Play hotfix worktree'si ve 2026-08-22'de kalmış eski `AliKa_release_candidate` klonu. |
| `urun/` | AliKa uygulama deposunun Git kökü `ebeveyn_kontrol/` ve ona bağlı düzeltme/sürüm worktree'leri (`alika-kutuphane`, `alika-lgs`, `alika-kural15`, `alika-store-1.2.11`); ürün, servis, takip ve tanıtım çıktıları da bulunur. |
| `atolye/` | İçerik üretim/denetim atölyesi ve içerik, site, oyun, uygulama için ayrı alt çalışma kopyaları. |
| `icerik/` | İçerik paketleri için birden fazla ayrı depo/checkout. Bunların dal ve yayın durumları birbirinden bağımsız olabilir. |
| `site/` | Ürün sitesi, tarihli site kopyası ve Sites/Vinext deneme uygulaması. |
| `ses/` | Yerel TTS, ses/video üretim hattı, kareler ve tanıtım görselleri. |
| `arsiv/` | Eski uygulama/içerik kopyaları, cihaz yedeği, eski yayınlar ve atılmış build önbellekleri. |
| `dosyalar/` | Dağınık referans belgeleri, APK ve yama/yedek dosyaları; uygulama kaynak deposu değil. |
| `worktrees/` | Uygulama deposuna bağlı 5 özellik worktree'si (`ebeveyn_kontrol-*`), site deposuna bağlı `uk-screen-time-guide` ve `olu-video-fix`; `main-birlesim/` ve `tv-oyun/` 2026-10-19'da boş klasördü. |
| `web/` | Envanter sırasında boştu. |

## 1. Ana AliKa uygulaması

Uygulamanın tek GitHub deposu `chizyo43-debug/alika` reposudur. Yerel Git kökü `urun/ebeveyn_kontrol/` klasörüdür; `urun/`, `repolar/` ve `worktrees/` altındaki güncel uygulama klasörlerinin çoğu bu köke bağlı worktree'lerdir. `C:\Users\Shadow\Desktop\ebeveyn_kontrol` ayrı bir kopya değil, `urun/ebeveyn_kontrol/` klasörüne giden junction'dır; aynı klasördür.

### `urun/ebeveyn_kontrol/` — uygulama deposunun Git kökü

Windows ve Android'de çalışan yerel-öncelikli ebeveyn kontrolü ve dijital iyi oluş uygulamasının yerel Git köküdür. 2026-10-19 ölçümünde dalı `wip/windows-maskot-saat-devam` (`07728bdf`, 2026-10-14) idi. GitHub `main` daha yeniydi (`3a506d5f`, 2026-10-19); yerel `main` referansı ise eskiydi (`6215d483`, 2026-10-15). İşe başlamadan `git fetch origin` ve `git worktree list` çalıştır, işin dalını ve worktree'sini seç. Kaynak ağacı:

- `windows/`: Python/Tkinter Windows istemcisi ve pytest testleri. Giriş noktaları `windows/main.py`, `windows/ui.py`.
- `android/`: Kotlin/Compose uygulaması; `android/app/` ve ortak protokol modelleri için `android/core-proto/`.
- `shared/`: Windows/Android sözleşmeleri, kurallar ve özellik envanteri. Atölyenin kanonik Figure Spec yolu bu klasördeki `figure_spec.json` dosyasıdır; o an açık dalın sürümünü gösterdiği için `origin/main` ile karşılaştırılır.
- `tools/`: doğrulama ve geliştirme yardımcıları.
- `docs/`: plan, mimari karar, tasarım, saha kanıtı, rapor ve yasal belgeler.
- `content/`: uygulamayla ilişkili izlenen içerik kaynakları.
- `site_repo/`: ürün deposundan ayrı site Git deposu bağlantısı; düz kaynak klasörü gibi taşımadan yerel durumunu kontrol et.
- `entitlement_service/`: lisans/cihaz yetkilendirme servisi.
- `output/tanitim-cizgi-film/`: tanıtım filmi üretim planı ve çıktıları.

İş yönlendirme belgeleri: [README](<urun/ebeveyn_kontrol/README.md>), [CODE_INDEX](<urun/ebeveyn_kontrol/CODE_INDEX.md>), [DURUM](<urun/ebeveyn_kontrol/DURUM.md>), [STATUS](<urun/ebeveyn_kontrol/STATUS.md>), [TAKIP](<urun/ebeveyn_kontrol/TAKIP.md>), [ECOSYSTEM](<urun/ebeveyn_kontrol/ECOSYSTEM.md>), [ANDROID_PLAN](<urun/ebeveyn_kontrol/ANDROID_PLAN.md>), [HANDOFF](<urun/ebeveyn_kontrol/HANDOFF.md>) ve [AGENTS](<urun/ebeveyn_kontrol/AGENTS.md>). Özellikten kaynak ve teste gitmek için önce CODE_INDEX'teki tabloya, tam eşleme için `shared/feature_inventory.json` dosyasına bak.

### Uygulama deposuna bağlı worktree'ler

| Klasör | Dal (2026-10-19) | Kullanım |
|---|---|---|
| [`urun/alika-kutuphane`](<urun/alika-kutuphane/>) | `duzeltme/kutuphane-test-1017` | Kütüphane düzeltmeleri. |
| [`urun/alika-lgs`](<urun/alika-lgs/>) | `duzeltme/lgs-kapsam-unite-sinif` | LGS kapsam/ünite/sınıf düzeltmesi. |
| [`urun/alika-kural15`](<urun/alika-kural15/>) | `duzeltme/distractor-why` | Çeldirici gerekçesi düzeltmesi. |
| [`urun/alika-store-1.2.11`](<urun/alika-store-1.2.11/>) | Detached HEAD `276c1784` | Microsoft Store 1.2.11 paket noktası. |
| [`repolar/alika-play-0.3.10`](<repolar/alika-play-0.3.10/>) | `hotfix/play-0.3.10-monitoring-flag` | Google Play 0.3.10 hotfix. |
| [`worktrees/ebeveyn_kontrol-*`](<worktrees/>) | `ozellik/android-panel-menu`, `cizici-2.3-aktarim`, `ozellik/cocuk-odak-halkasi`, `tv/eski-oyunlari-kaldir`, `windows/kaldirma-isareti` | Özellik dalları. |
| [`atolye/AliKa atölye/alika_figure_release_worktree`](<atolye/AliKa atölye/alika_figure_release_worktree/>) | `codex/figure-spec-2` | Figure Spec çalışma dalı. |

Bunlara ek olarak `C:\Users\Shadow\Desktop\ebeveyn_kontrol\.claude\worktrees\` altında oturum worktree'leri ve `C:\cb\...\worktree` (`codex-bridge-bulut-pc`) bulunur. Dallar değiştikçe tablo eskir; kesin liste `git worktree list` çıktısıdır.

### `repolar/AliKa_release_candidate/` — eski ayrı klon

Aynı GitHub deposunun worktree olmayan ayrı bir klonudur. 2026-10-19'da `codex/sol-flow-runtime-repair-2026-08-22` dalında (`71483c5`, 2026-08-22) duruyordu. Çalışma ağacında görsel etkinlik (`visualChoice`) kodu yoktu ve `shared/figure_spec.json` 1.1.0 sürümündeydi (`main`: 1.8.0). Yeni kod işi, sözleşme okuması veya durum takibi için kullanma; yalnız tarihsel başvuru içindir.

## 2. Eğitim içeriği: üretim ile yayın ayrıdır

### `atolye/AliKa atölye/` — üretim ve kalite atölyesi

AliKa için ders anlatımı, soru bankası, oyun ve çok ülkeli müfredat içeriğini üretme, denetleme ve hazırlama çalışma alanıdır; uygulamanın kendisi veya yayın deposu değildir. [ATOLYE_KAPSAM](<atolye/AliKa atölye/ATOLYE_KAPSAM.md>) ülke/sınıf kapsamını; [ATOLYE_PLAN](<atolye/AliKa atölye/ATOLYE_PLAN.md>) üretim planını; [STATUS](<atolye/AliKa atölye/STATUS.md>) iş ve kabul durumunu; [CONTENT_REPOSITORY](<atolye/AliKa atölye/CONTENT_REPOSITORY.md>) yayın deposu ile çalışma kopyalarının ayrımını açıklar. Python proje ayarları `pyproject.toml` içindedir.

- `library/`: ana üretim kütüphanesi. `sources/` ve `curriculum/` kaynak/müfredat; `prompts/` ve `skills/` üretim yöntemleri; `schemas/` ve `tools/` biçim/doğrulama; `tests/`, `reviews/`, `audit/`, `reports/`, `releases/` kalite kanıtı ve teslimler.
- `analysis/`, `audit/`, `kaynak kitap/`: araştırma, kalite denetimi ve kaynak kitaplıkları.
- `games/`: oyun çalışma alanı. 2026-09-29 envanterindeki `ebeveyn_kontrol_games/` ve `ebeveyn_kontrol_premium_games_v2/` 2026-10-19'da yoktu.
- İçerik çalışma kopyaları: `alika_icerik_current/`, `alika_icerik_games/`, `alika_icerik_premium_v2_rights/`, `alika-content-gb-publish/`.
- Site çalışma kopyaları: `alika-site/`, `alika-site-gb-publish/`, `alika-site-codex-marketing/`.
- AliKa uygulama worktree'si: `alika_figure_release_worktree/` (`codex/figure-spec-2`, uygulama deposuna bağlı). 2026-09-29 envanterindeki `ebeveyn_kontrol_memory/` 2026-10-19'da yoktu.

Bu iç içe dizinler aynı atölye ana deposunun sıradan alt klasörleri olmayabilir; kendi README/AGENTS ve Git durumları bulunan ayrı iş kopyalarıdır. Özellikle içerik yayınında atölyenin [CONTENT_REPOSITORY](<atolye/AliKa atölye/CONTENT_REPOSITORY.md>) belgesi temiz yayın ağacı olarak `C:\Users\Shadow\Desktop\alika-content-main` yolunu işaret eder. Bu yol `icerik/alika-content-main/` klasörüne giden junction'dır (2026-10-19'da doğrulandı); ikisi aynı klasördür. Diğer `icerik/` checkout'ları ve atölye içindeki içerik kopyaları bu yol ile aynı değildir. Atölye içindeki `.venv*`, `.pytest_cache`, `.tmp` ve `.qualitydeps` ortam/araç alanlarıdır; ürün kaynağı veya yayımlanacak içerik değildir.

### `icerik/alika-content-main/` — Türkiye paketleri ve ana içerik deposu kopyası

AliKa uygulamasının indirdiği ders notu, soru bankası ve veri-only oyun paketlerinin deposudur. Bu çalışma alanındaki checkout `main` dalındadır (`bb2b1e8`, 2026-09-01). Atölye belgesinin işaret ettiği `C:\Users\Shadow\Desktop\alika-content-main` yolu bu klasöre giden junction'dır; ikisi aynı fiziksel klasördür (2026-10-19).

- `turkiye/`: ülke/sınıf/ders paketleri.
- `games/`: uygulama kodu veya eklenti içermeyen oyun veri paketleri.
- `authoring/`, `curriculum/`, `staging/`, `tools/`, `tests/`: yazım, müfredat, hazırlık, doğrulama ve test.
- `docs/`, `reports/`, `voice/`: belgeler, kalite raporları ve ses kuralları.
- İlk başvuru: [README](<icerik/alika-content-main/README.md>), [SCHEMA_V2](<icerik/alika-content-main/SCHEMA_V2.md>), [AUTHORING_RULES](<icerik/alika-content-main/AUTHORING_RULES.md>), `voice/PRIMARY_VOICE.md`.

### `icerik/alika-content-jp-kr-20260901/` — tarihli Japonya/Kore içerik checkout'u

2026-09-01 tarihli Japonya/Kore yayın paketi ve kanıtlarını içeren ayrı Git checkout'udur; kendi README'si JP/KR kataloglarını `library/releases/JP/2026-09-01/` ve `library/releases/KR/2026-09-01/` altında gösterir. Türkiye içerikleri ve oyun paketleri de bulunabilir; JP/KR işi için `library/curriculum/JP/` veya `KR/` içindeki `current-publish-release.json` işaretçilerini ve ilgili `publishable`/bloklayıcı/karma kanıtlarını kontrol et. [README](<icerik/alika-content-jp-kr-20260901/README.md>), [SCHEMA_V2](<icerik/alika-content-jp-kr-20260901/SCHEMA_V2.md>).

### `icerik/alika-icerik-catalog/` — katalog checkout'u

İçerik paketleri için daha dar checkout: `turkiye/`, `games/`, `tools/`, `tests/`, `reports/`. [README](<icerik/alika-icerik-catalog/README.md>) ve [SCHEMA_V2](<icerik/alika-icerik-catalog/SCHEMA_V2.md>) paket kullanımını/şemasını açıklar; `reports/` hazır olma ve kalite incelemelerini tutar. `alika-content-main` ile içerik bakımından örtüşür; hangi kopyanın hedef olduğunu Git dalını ve iş isteğini kontrol ederek seç.

## 3. Web ve Site işleri

### `site/alika-site/` — ürünün çok dilli statik web sitesi

`www.alika.tr` için React/Vite tabanlı ürün ve mağaza sitesi; uygulama arayüzü değildir. `src/main.tsx` giriş, `src/data/` site verileri, `src/styles/` tasarım stilleri, `legal/` yasal sayfalar, `assistant-service/` isteğe bağlı site asistanıdır. [README](<site/alika-site/README.md>) build ve yayın davranışını; [package.json](<site/alika-site/package.json>) komutları ve bağımlılıkları açıklar. `dist/` build çıktısı, `node_modules/` bağımlılık alanıdır.

### `site/alika-site-jp-kr-20260901/` — tarihli site kopyası

Ürün sitesinin 2026-09-01 tarihli ayrı checkout/kopyasıdır. `src/`, `public/`, `legal/`, `tools/` ve `assistant-service/` yapısı ana siteyle örtüşür. Kendiliğinden `site/alika-site/` ile eşit veya güncel kabul etme; [README](<site/alika-site-jp-kr-20260901/README.md>) ve Git durumunu kontrol et.

### `worktrees/uk-screen-time-guide/` — siteye bağlı UK rehber dalı

Ürün sitesinin `codex/uk-screen-time-guide` adlı Git worktree dalıdır; `site/alika-site` deposunun worktree listesinde görünür. UK ekran-süresi rehberi işi açıkça bu dala aitse burayı kullan. README, `src/`, `public/`, `legal/` ve `tools/` site düzenini izler. Site ana kopyasına doğrudan taşımadan önce hedef dalı teyit et. Aynı site deposuna bağlı ikinci worktree `worktrees/olu-video-fix/` (`codex/olu-video-baglantilari`) klasörüdür.

### `site/alika-sites-preview/` — Sites/Vinext deneme uygulaması

Diğer statik ürün sitesiyle karıştırılmaması gereken ayrı preview/prototip uygulaması. `package.json` Next/React, Vinext ve Cloudflare araçlarını gösterir; `app/page.tsx`, `app/layout.tsx` ve `app/book-experience.tsx` sayfa girişleridir. `.openai/hosting.json` Sites proje kimliğini, `vite.config.ts` Vite ayarını taşır. `dist/`, `.next/`, `.wrangler/` ve `node_modules/` üretilmiş/bağımlılık çıktılarıdır.

## 4. Ses, TTS ve tanıtım medyası

### `ses/alika_tts_v2/` — yerel çok dilli TTS sistemi

Metinden yerel WAV üreten TTS CLI'si. [README](<ses/alika_tts_v2/README.md>) ana kullanım ve dilleri; `alika_tts.py` CLI'yi; `config/routing.json` dil/motor seçimini; `scripts/`, `reports/`, `ref/`, `out/` yardımcıları, seçim kanıtını, referansları ve örnek çıktıları gösterir. `models/`, `models_qwen/`, `.venv_*`, `bench/` ve `out/` büyük yerel model, ortam ve üretilmiş çalışma alanlarıdır; dosya haritasında tek tek dökülmez.

### `ses/alika ses/` — seslendirme ve video üretim çalışma alanı

`AliKa_Seslendirme_Plani.md` ses sisteminin amacını; `video-production/README.md` güncel Windows V2 video hattını tarif eder. `video-production/tr/` ve diğer dil klasörleri senaryo/yerelleştirme; `tools/` TTS, hizalama, render ve doğrulama; `assets/`, `samples/`, `work/`, `artifact-work/`, `out/`, `upload-ready/` kaynak/ara/final medya alanlarıdır. Ham WAV ve ASR JSON'ları da klasör kökünde bulunur. İçindeki `alika-site/` aynı ürün sitesi türünden ayrı bir kopyadır; ana `site/alika-site/` ile senkron kabul etme.

### Diğer medya alanları

- `ses/alika_tts/`: kök envanterinde yalnız `models/` görüldü; çalıştırılabilir CLI veya açıklayıcı README bulunmadı. Model dosyası arşivi/önceki TTS alanı olması olasıdır; etkin TTS kodu olarak varsayma.
- `ses/AliKa_Veo_Denemeleri/`: iki tarihli maskot hareketi video denemesi. Kabul edilen alfa kanallı sonuç örneği `mascot-wave-20260907-02/transparent-v1/README.md` içindedir.
- `ses/alika_video_kareler/`: tanıtım videosu ekran kareleri; `ham/`, `aday/`, `klip/`, `kontak/`, `montaj/`, `tumkare/` görsel seçim ve kurgu aşamalarıdır.
- `ses/alika-social-card/`: tek sosyal paylaşım görseli `alika-social-card-1200x630.png`.

## 5. Arşiv ve dağınık referans dosyaları

### `arsiv/` — eski sürüm, yedek ve emekliye ayrılmış işler

- `alika/ebeveyn_kontrol/`: tam uygulama deposunun eski arşiv kopyası ve tarihsel plan/kanıtları; aktif ürün kökü değildir.
- `alika/AliKa atölye/`: atölyenin arşiv kopyası.
- `alika_cihaz_yedek_20260808/`: cihaz yedeği (`databases/`, `files/`, `shared_prefs/`).
- `alika-content-retired-bundles-20260901/`: emekliye ayrılmış içerik ZIP paketleri; canlı paket seçmek için kullanma.
- `AliKa-Play-0.3.0/`: eski oyun sürümü AAB'si ve `release-manifest.json`.
- `alika-quality-worktrees/`: eski kalite/Android/içerik çalışma ağaçları; bazıları kendi `AGENTS.md` dosyalarını taşır.
- `alika-retired-build-cache-20260901/`: KSP/Kotlin/build/test ara çıktıları; kaynak kod değildir.

### `dosyalar/` — kökteki tekil belgeler ve paketler

- `AliKa_BrainCore.txt`: `repolar/.../docs/plan/brain_core.md` kaynaklı, açıkça “fikir yürütme kopyası” denmiş not; kanonik mimari belgesi yerine kullanma.
- `AliKa_Tanitim_Videosu.md`: ilk tanıtım videosu senaryo/çekim planı.
- `AliKa-test.apk`: test APK paketi; kaynak değildir.
- `ebeveyn_kontrol_untracked_20260731.txt` ve `ebeveyn_kontrol_yedek_20260731.patch`: tarihli takip/yama dosyaları; uygulamadan önce hangi koda ait olduklarını doğrula.

## Yarım ve açık işler

Bu bölüm mevcut durum dosyalarında açık kalan işleri özetler; tamamlanmış kod ile cihaz, insan incelemesi, mağaza veya yayın kabulini ayrı tutar. Tarih, her kaydın ne kadar güncel olduğunu gösterir.

### Ürün ve yayın işleri

| İş | Son kayıt / kalan adım | Kaynak |
|---|---|---|
| Android Öğrenme Stüdyosu 3B | **Sıradaki kod dilimi.** 3A yerel ders devam kaydı inceleme ve hedefli testleri geçti. 3B gerçek çocuk kimliği, içerik sürümü ve kararlı okuyucu adımını bağlamalı; sahte bağlam kullanmamalı. Android/TV cihaz kabulü ve Windows ile eşitleme ayrıca açık. | 2026-09-29 [DURUM](<urun/ebeveyn_kontrol/DURUM.md>), [2.0 planı](<urun/ebeveyn_kontrol/docs/plan/ALIKA_2_0_PLAN.md>) |
| Windows Öğrenme Stüdyosu 5A–5E | Kod/test kabulü tamamlandı. **Kurulu paket ve insan görsel/saha kabulü henüz yok.** | 2026-09-29 [DURUM](<urun/ebeveyn_kontrol/DURUM.md>), [yürütme kaydı](<urun/ebeveyn_kontrol/docs/plan/LEARNING_STUDIO_EXECUTION.md>) |
| Android tam test paketi | 2026-09-29 kaydında `:app:testDebugUnitTest` 1.416 test tamamladı; Almanca kaynak anahtarı parity kontrolü başarısız, 1 test atlandı. 3A kaydına göre hata bu dilimdeki koddan bağımsız; genel test paketi bütünüyle yeşil değil. | [DURUM](<urun/ebeveyn_kontrol/DURUM.md>), [2.0 planı](<urun/ebeveyn_kontrol/docs/plan/ALIKA_2_0_PLAN.md>) |
| Play lisansının güvenli yeniden kurulumu | 2026-09-15 takip kaydı açık: uygulama kaldırılıp yeniden kurulunca değişen cihaz kimliği aynı Play alımında `409 root_device_changed` üretiyor ve hata kullanıcıya yanlış gösteriliyor. Güvenli kurtarma, kod/deploy ve gerçek cihaz kabulü için **daha yeni kapanış kaydı bulunmadı**. | [STATUS](<urun/ebeveyn_kontrol/STATUS.md>), [TAKIP](<urun/ebeveyn_kontrol/TAKIP.md>) |
| 1.2.10 Store paketi | 2026-09-26 kaydı Submission 10'u “Update in certification” olarak gösteriyor; otomatik yayın açık, ancak sertifika/onay ve canlı yayın sonucu daha yeni kayıtta doğrulanmamış. Sonucu ürünün `DURUM.md` dosyasından teyit et. | [DURUM](<urun/ebeveyn_kontrol/DURUM.md>) |
| Tanıtım çizgi filmi, bölüm 1 | 35 sn yatay/dikey senkronlu adaylar ve teknik kontroller hazır. **Kare kare insan görsel/ses kabuli bekliyor; yayımlanmadı/yüklenmedi.** | 2026-09-29 [STATUS](<urun/ebeveyn_kontrol/STATUS.md>), çıktı alanı `urun/ebeveyn_kontrol/output/tanitim-cizgi-film/` |
| Japonya/Kore bilinirlik dalgası 2 | 2026-09-28'de iki editoryal e-posta gönderildi; yanıt bekleniyor. Yeni yerel Shorts taslağı ve 7 günlük ölçüm turu planda, henüz yayımlanmış değil. | [Durum özeti](<urun/ebeveyn_kontrol/DURUM.md>), [dalga 2 planı](<urun/ebeveyn_kontrol/docs/marketing/japan-korea-awareness-wave-2-2026-09-28.md>) |

### İçerik ve kalite işleri

| İş | Son kayıt / kalan adım | Kaynak |
|---|---|---|
| Türkiye 5. sınıf Sosyal Bilgiler | **Son atölye kaydı 2026-09-12.** 19 kazanım kaynak programa bağlanmış, 345 soruluk adayda gerçek `semanticCase`/`semanticFamilyKey` denetimi ve bir siyasi haritanın Figure Spec uyumu açık kalmıştı; son tam strict kabul kaydedilmemiş. Durumu ilerletmeden önce atölye kaydını yenile. | [Atölye STATUS](<atolye/AliKa atölye/STATUS.md>), [GLOBAL-REPAIR-QUEUE](<atolye/AliKa atölye/library/reviews/quality-program-20260905/GLOBAL-REPAIR-QUEUE.md>) |
| Türkiye 5. sınıf Matematik | 2026 müfredat kontrolünde yayın/kazanım kabulü yeniden açılmış: üç örüntü sorusu ve paylaşılan konu notu güncel kaynak sınırını aşıyor; bir olasılık sorusu ayrıca eşleştirme incelemesinde. Önceki teknik/cihaz testleri müfredat kabulinin yerine geçmiyor. | [2026-09-07 müfredat raporu](<atolye/AliKa atölye/library/reviews/quality-program-20260905/curriculum-check-20260907/REPORT.md>) |
| Türkiye 5. sınıf Türkçe yayını | 263 soru onarımı tamamlandı; 384 soruluk yerel aday strict kontrolden geçti. **`publishReady=false`:** insan editoryal incelemesi, yeni hash için Windows/Android kabulü, ses/ASR kabulü ve yayın onayı ayrı açık kapılar. | 2026-09-12 [Atölye STATUS](<atolye/AliKa atölye/STATUS.md>) |
| Diğer ülke ve sınıfların içerik kuyruğu | Repair queue'nin son güncellemesi 2026-09-07; çok sayıda ders/sınıf sırada. ABD kapsamı `blocked-scope-not-defined`. Bu kuyruk, atölye STATUS dosyasından daha eski olduğundan yeni işe başlamadan önce kuyruk ve manifesti tazele. | [GLOBAL-REPAIR-QUEUE](<atolye/AliKa atölye/library/reviews/quality-program-20260905/GLOBAL-REPAIR-QUEUE.md>), [Atölye STATUS](<atolye/AliKa atölye/STATUS.md>) |
| 7–9. sınıf Matematik paketleri | Hazır olma raporunun gövdesi (2026-08-11) 7. sınıfı 456/500, 8. sınıfı 25/500 soru olarak gösterip yayın kapsamı dışında bırakıyor. Daha yeni bir hazır olma raporu bulunmadı; güncel dosya sayımıyla yeniden teyit edilmeli. | [7–9 hazır olma raporu](<icerik/alika-content-main/reports/GRADE7_9_COMPLETED_COURSES_READINESS.md>) |

### Planlanan, fakat tamamlanma kaydı bulunmayan işler

- **AliKa.tr iyileştirmeleri:** 2026-09-07 planı A0 kaynak/yayın doğrulamasından başlayıp A1 edinme akışı, A2 ana sayfa, A3 eğitim/mahremiyet kanıtı ve A4 dokuz dil/erişilebilirlik/yayın kabuline gidiyor. Son somut adım A0; site deposunda bu aşamaların durumunu kaydeden bir durum dosyası yok. Önce dal ve canlı kaynak eşleşmesini kontrol et. [Plan](<urun/ebeveyn_kontrol/docs/plan/ALIKA_SITE_IYILESTIRME_PLANI_2026_09_07.md>)
- **AliKa 2.0 uzun dönem kuyruğu:** Sıradaki 3B'den sonra Android/TV Stüdyo devamı; sonraki kapılı işler dil üniteleri ve çocuk pilotu, Yerel AI, AliKa Birlikte/aile oyunları, gelişmiş TV, uzak bağlantı ve tam A1. Bunlar plan/bağımlılık durumlarıdır, hepsi başlanmış iş demek değildir. [Tek yürütme sırası](<urun/ebeveyn_kontrol/docs/plan/ALIKA_2_0_PLAN.md>)
- **Ürün sitesi çalışma dalları:** `site/alika-site` üzerinde `codex/warm-video-home` ve aynı repo ile ilişkili `worktrees/uk-screen-time-guide` dalı var; bu dallar için tamamlanma/teslim durumu indekste bulunan belgelerde kayıtlı değil. Yalnız dal adıyla açık iş sayma; branch, diff ve PR/teslim kaydını kontrol et.

### Eski veya çelişebilen durum kayıtları

- `repolar/AliKa_release_candidate/DURUM.md` son olarak 2026-08-22'de değişmiş ve bazı entegrasyonları açık gösteriyor. Daha yeni `urun/ebeveyn_kontrol/TAKIP.md`, 2026-09-24 saha teyidinden sonra paylaşım, mesaj, sayaç ve eşleştirme maddelerini kapatıyor. Eski açık maddeleri güncel kabul etme. `release_candidate` klonu 2026-10-19 itibarıyla eski kabul edilir; güncel kayıt `urun/ebeveyn_kontrol/DURUM.md` dosyasıdır (son değişiklik 2026-10-13).
- `atolye/AliKa atölye/STATUS.md` son olarak 2026-09-12'de güncellenmiş; içindeki daha eski “263 soru kaldı” notu, aynı dosyanın sonraki 2026-09-12 tamamlanma kaydıyla geçersiz kılınmış. Onarım tamamlandı; dış yayın/insan/platform/ses kapıları açık.
- Atölye içindeki `alika_figure_release_worktree/` (2026-08-30) durum dosyaları bu haritada eski kopya kayıtlarıdır; yeni ürün durumunu temsil ettiklerini varsayma. `ebeveyn_kontrol_premium_games_v2/` 2026-10-19'da artık yoktu.

## Hızlı dosya arama

Önce ilgili kökü seç; sonra dosya adını veya kavramı o kapsam içinde ara. Geniş `.git`, bağımlılık, model, build ve cache klasörlerini tarama:

```powershell
rg --files --hidden <proje-koku> -g '!**/.git/**' -g '!**/node_modules/**' -g '!**/.venv*/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.cache/**'
rg -n "aranan özellik veya terim" <proje-koku>
```

Kod işi için uygulama deposundaki [CODE_INDEX](<urun/ebeveyn_kontrol/CODE_INDEX.md>), içerik işi için ilgili `README.md`/`SCHEMA_V2.md`, atölye işi için [STATUS](<atolye/AliKa atölye/STATUS.md>) ve `CONTENT_REPOSITORY.md` başlangıç noktasıdır. Birbirine benzeyen klasörlerde düzenleme yapmadan önce Git kökü/dalı ve yerel `AGENTS.md` dosyasını doğrula.

## Haritanın kapsamı

Bu indeks 10 kök klasörün tamamını ve bunların proje kimliğini belirleyen üst düzey alt klasör/dosyalarını kapsar. Her resim, soru satırı, video karesi, model ağırlığı, ZIP içeriği veya build dosyası tek tek listelenmez; büyük medya/model/bağımlılık/cache ve tarihsel build içerikleri bulundukları proje altında sınıflandırılır.
