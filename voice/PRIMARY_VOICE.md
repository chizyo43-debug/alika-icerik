# AliKa ana kadın sesi

Türkiye içeriklerinde ses gerektiren bütün kayıtların kanonik konuşmacı profili
`alika-primary-woman-v1` değeridir. Profil, proje sahibinin eşine ait izinli bir
insan sesinden yerel olarak üretilir. Ham referans biyometrik veri olduğu için
Git'e ve dağıtım paketlerine girmez; yalnız SHA-256 özeti ve hak kaydı yayımlanır.

## Kanonik üretim rotası

- Motor/model: `openbmb/VoxCPM2`
- Model revizyonu: `32279effe8c19989596f05d353d1447f51d9e915`
- Model dosyası SHA-256: `f7f964cfa9da23653baec6e6f7750719977ad944ed9f95fe52fe3a620506891d`
- Model ve kod lisansı: Apache-2.0; model kartı ticari kullanıma açık olduğunu
  ayrıca belirtir.
- Klonlama modu: kısa referans ses + doğru referans transkriptiyle ultimate
  cloning.
- Parametreler: `cfg=2.0`, `inference_timesteps=10`, kayıt kimliğinden türetilen
  deterministik tohum, en çok 400 karakterlik parçalar ve parçalar arasında
  180 ms sessizlik.
- Çıktı: mono, PCM 16-bit, 48 kHz yerel WAV.
- Üretim: `tools/generate_primary_voice_audio.py`
- Uygulama: `tools/apply_primary_voice_audio.py`

Modelin resmî kaynakları:

- https://huggingface.co/openbmb/VoxCPM2
- https://github.com/OpenBMB/VoxCPM

OmniVoice bu üretim rotasında kullanılmaz. Kod lisansı Apache-2.0 olsa da
ön-eğitimli model kartı CC-BY-NC koşulu taşır; ürün paketlerinin ticari kullanım
kapısıyla uyumlu değildir.

## Özel referansın yerleşimi

Yerel referans varsayılan olarak şu Git dışı yolda tutulur:

`voice/private/alika-primary-woman-v1/prompt.wav`

Beklenen referans SHA-256 değeri:

`3ead7d03d36780933b0acb326e9a8eaf9ee443ad0a440e9b23ca8cccbdaa093e`

Üretici, farklı bir yolu yalnız `--reference` ile alabilir; dosya özeti beklenen
değerle eşleşmezse üretim başlamaz. Mutlak özel yol hiçbir manifest, rapor veya
pakete yazılmaz.

## Yayın kapısı

Her ses varlığı için WAV başlığı, dosya özeti, süre, örnekleme hızı, kanal,
bit derinliği, transkript, konuşmacı profili ve hak kaydı doğrulanır. Soru
bağlantısındaki `audio.contentSha256`, gerçek WAV SHA-256 değeriyle aynı olmalıdır.
Üretilen kayıtlarda kırpılma, sessiz/boş ses, beklenmeyen uzunluk ve ASR metin
uyuşmazlığı bulunamaz. Ham referans veya yerel mutlak yol içeren paket yayımlanmaz.
