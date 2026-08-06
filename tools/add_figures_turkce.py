#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Türkçe paketinin 21 konu anlatımına birer Şerit A figürü ekler.

Soru figürü ÜRETMEZ ve bu bilinçlidir. Türkçe soruları metin anlamaya
dayanıyor; 39 sorunun kökünde geçen duyuru, çizelge ve afiş metnin kendisi.
Onları tabloya çevirmek bilgiyi önceden ayrıştırıp sunmak olur ve ölçülen
beceriyi — düzyazıdan bilgi çıkarmayı — ortadan kaldırır. Sayı tutturmak için
süs figür eklemek, metriği iyileştirip içeriği bozmaktır (AUTHORING_RULES §2).

Notlarda durum tersi: yirmi bir konunun tamamı ya bir SÜREÇ (yazma, konuşma,
dinleme materyali seçimi) ya da bir SINIFLANDIRMA (metin türleri, gerçek/görüş,
ses özellikleri). İkisi de görselin var olma nedenidir; akış şeması ve tablo
bunun için katalogda.

Alt metin kuralı: figürdeki kategori, ilişki ve değerler yazılır. Not
öğreticidir, bu yüzden alt metnin içeriği vermesi sızıntı değildir — sorularda
olsaydı olurdu.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "turkce" / "turkce-tum.jsonl"


def _anahtar(not_id: str, metin: str) -> str:
    """Etiket anahtarı: not kimliği + metnin kararlı özeti.

    Özet metinden türetilir ki aynı etiket iki kez yazıldığında aynı anahtarı
    alsın. Anahtar adına '.repaired' gibi bir iş turu adı ASLA yazılmaz.
    """
    ozet = hashlib.sha256(metin.encode("utf-8")).hexdigest()[:12]
    return f"{not_id}.visual.{ozet}"


def akis(not_id: str, adimlar: list, alt: str) -> tuple[dict, dict]:
    """Sıralı süreç figürü: her adım bir düğüm, ardışık adımlar bağlı."""
    etiketler = {}
    dugumler = []
    for i, metin in enumerate(adimlar):
        a = _anahtar(not_id, metin)
        etiketler[a] = metin
        dugumler.append({"id": f"a{i + 1}", "labelKey": a})
    kenarlar = [{"from": f"a{i + 1}", "to": f"a{i + 2}"}
                for i in range(len(adimlar) - 1)]
    alt_a = _anahtar(not_id, alt)
    etiketler[alt_a] = alt
    return ({"kind": "flow", "nodes": dugumler, "edges": kenarlar,
             "direction": "down", "altTextKey": alt_a}, etiketler)


def tablo(not_id: str, basliklar: list, satirlar: list, alt: str
          ) -> tuple[dict, dict]:
    """Sınıflandırma figürü: ölçüt sütunları ve karşılaştırılan satırlar."""
    etiketler = {}
    baslik_anahtarlari = []
    for metin in basliklar:
        a = _anahtar(not_id, metin)
        etiketler[a] = metin
        baslik_anahtarlari.append(a)
    tablo_satirlari = []
    for satir in satirlar:
        hucreler = []
        for metin in satir:
            a = _anahtar(not_id, metin)
            etiketler[a] = metin
            hucreler.append({"key": a})
        tablo_satirlari.append(hucreler)
    alt_a = _anahtar(not_id, alt)
    etiketler[alt_a] = alt
    return ({"kind": "table", "headerKeys": baslik_anahtarlari,
             "rows": tablo_satirlari, "altTextKey": alt_a}, etiketler)


# Not kimliği → (tür, veri). Her figür notun ÖĞRETTİĞİ şeyi gösterir;
# süsleme değildir ve notun metninde anlatılanı görünür kılar.
TASARIM = {
    "tr-g05-tur-td-5-1-n01": ("akis", [
        "Amacı belirle: ne öğrenmek istiyorum?",
        "Kaynakları tara: konuşma, video, belgesel, ses kaydı",
        "Uygunluğu denetle: süre, düzey, güvenilirlik",
        "Seç ve hazırlan: not defterini ve soruları hazırla",
        "Dinledikten sonra seçimi gözden geçir",
    ], "Dinleme materyali seçiminin beş adımı yukarıdan aşağıya sıralanmıştır: "
       "amaç belirleme, kaynak tarama, uygunluk denetimi, seçim ve hazırlık, "
       "seçimi gözden geçirme."),

    "tr-g05-tur-td-5-5-n01": ("tablo",
        ["Soru", "Ne aranır?"],
        [["Kim?", "Konuşmadaki kişiler"],
         ["Ne?", "Anlatılan olay ya da bilgi"],
         ["Nerede?", "Geçtiği yer"],
         ["Ne zaman?", "Zaman bilgisi"],
         ["Nasıl?", "Olayın gerçekleşme biçimi"]],
        "İki sütunlu tablo: sol sütunda beş soru sözcüğü, sağ sütunda her "
        "sorunun dinlenen içerikte neyi aradığı yazılıdır."),

    "tr-g05-tur-td-5-7-n01": ("akis", [
        "İzlerken kanıtı topla: söz, davranış, görüntü",
        "Kanıtları birbiriyle karşılaştır",
        "Doğrudan söylenmeyeni tahmin et",
        "Tahmini kanıta geri götürerek sına",
    ], "Çıkarım yapmanın dört adımı sıralanmıştır: kanıt toplama, kanıtları "
       "karşılaştırma, söylenmeyeni tahmin etme, tahmini kanıtla sınama."),

    "tr-g05-tur-td-5-10-n01": ("tablo",
        ["Ölçüt", "Birinci konuşma", "İkinci konuşma"],
        [["Amaç", "Bilgilendirmek", "İkna etmek"],
         ["Kanıt", "Sayı ve kaynak verir", "Kişisel deneyim anlatır"],
         ["Dil", "Tarafsız", "Duygu yüklü"]],
        "Üç sütunlu tablo: satırlarda amaç, kanıt ve dil ölçütleri; "
        "sütunlarda iki konuşmanın bu ölçütlerdeki farkı gösterilmiştir."),

    "tr-g05-tur-td-5-22-n01": ("tablo",
        ["Sorulacak soru", "Neden önemli?"],
        [["Bu iletiyi kim hazırladı?", "Kaynağın amacını gösterir"],
         ["Kime sesleniyor?", "Hedef kitleyi belirler"],
         ["Hangi kanıtı sunuyor?", "İddia ile kanıtı ayırır"],
         ["Ne yapmamı istiyor?", "Yönlendirmeyi görünür kılar"]],
        "İki sütunlu tablo: sol sütunda medya iletisine sorulacak dört soru, "
        "sağ sütunda her sorunun neyi ortaya çıkardığı yazılıdır."),

    "tr-g05-tur-to-5-5-n01": ("akis", [
        "Bilmediğin sözcüğün geçtiği cümleyi yeniden oku",
        "Bağlamdan anlamını tahmin et",
        "Sözcüğün kökünü ve eklerini ayır",
        "Sözlükten doğrula",
        "Anlamı kendi cümlende kullanarak sına",
    ], "Bilinmeyen sözcüğün anlamını bulmanın beş adımı sıralanmıştır: "
       "cümleyi yeniden okuma, bağlamdan tahmin, kök ve ek ayırma, sözlükten "
       "doğrulama, kendi cümlesinde kullanarak sınama."),

    "tr-g05-tur-to-5-6-n01": ("tablo",
        ["Yüzey anlam sorusu", "Metinde nerede aranır?"],
        [["Kim?", "Kişilerin anıldığı cümleler"],
         ["Nerede?", "Yer bildiren sözcükler"],
         ["Ne zaman?", "Zaman bildiren sözcükler"],
         ["Ne oldu?", "Olayı anlatan cümleler"]],
        "İki sütunlu tablo: sol sütunda dört yüzey anlam sorusu, sağ sütunda "
        "her sorunun cevabının metinde hangi tür cümlelerde arandığı."),

    "tr-g05-tur-to-5-8-n01": ("akis", [
        "Metinde doğrudan yazılanı işaretle",
        "İşaretlerin arasındaki ilişkiyi kur",
        "Doğrudan yazılmayan sonuca ulaş",
        "Sonucu metindeki kanıtla eşleştir",
    ], "Okuduğundan çıkarım yapmanın dört adımı sıralanmıştır: doğrudan "
       "yazılanı işaretleme, ilişki kurma, sonuca ulaşma, sonucu kanıtla "
       "eşleştirme."),

    "tr-g05-tur-to-5-13-n01": ("tablo",
        ["Ölçüt", "Gerçek", "Görüş"],
        [["Doğrulanabilir mi?", "Evet, ölçülür ya da kaynaktan bakılır",
          "Hayır, kişiden kişiye değişir"],
         ["Örnek", "Kitap 120 sayfadır", "Kitap çok sürükleyicidir"],
         ["İşaret sözcükler", "Sayı, tarih, ölçü",
          "Bence, en güzel, sıkıcı"]],
        "Üç sütunlu tablo: satırlarda doğrulanabilirlik, örnek ve işaret "
        "sözcükler; sütunlarda gerçek ile görüşün bu ölçütlerdeki farkı."),

    "tr-g05-tur-to-5-14-n01": ("akis", [
        "Serim: kişiler, yer ve zaman tanıtılır",
        "Düğüm: olay bir soruna dönüşür",
        "Çözüm: sorun bir sonuca bağlanır",
    ], "Öyküleyici metnin üç bölümü sırayla gösterilmiştir: serimde kişi, yer "
       "ve zaman tanıtılır; düğümde olay soruna dönüşür; çözümde sorun "
       "sonuca bağlanır."),

    "tr-g05-tur-to-5-15-n01": ("tablo",
        ["Metin türü", "Amacı", "Tanınma işareti"],
        [["Öyküleyici", "Olay anlatmak", "Kişi, zaman, yer ve olay örgüsü"],
         ["Bilgilendirici", "Bilgi vermek", "Tanım, örnek, sayı"],
         ["Şiir", "Duygu ve izlenim aktarmak", "Dize, ölçü, yinelenen sesler"]],
        "Üç sütunlu tablo: satırlarda öyküleyici, bilgilendirici ve şiir "
        "türleri; sütunlarda her türün amacı ve tanınma işareti."),

    "tr-g05-tur-to-5-24-n01": ("tablo",
        ["Medya metni ögesi", "Ne işe yarar?"],
        [["Başlık", "Dikkati çeker ve konuyu duyurur"],
         ["Görsel", "İletiyi destekler ya da duyguyu güçlendirir"],
         ["Kaynak", "Bilginin nereden geldiğini gösterir"],
         ["Çağrı", "Okuyucudan bir davranış ister"]],
        "İki sütunlu tablo: sol sütunda medya metninin dört ögesi, sağ "
        "sütunda her ögenin işlevi."),

    "tr-g05-tur-tk-5-1-n01": ("akis", [
        "Amacı ve dinleyiciyi belirle",
        "Ana düşünceyi ve örnekleri seç",
        "Konuşmayı giriş, gelişme, sonuç olarak sırala",
        "Prova et ve süreyi ölç",
        "Konuşma sonrası geri bildirimi değerlendir",
    ], "Konuşma sürecinin beş adımı sıralanmıştır: amaç ve dinleyici "
       "belirleme, içerik seçme, giriş-gelişme-sonuç sıralaması, prova ve "
       "süre ölçümü, geri bildirim değerlendirmesi."),

    "tr-g05-tur-tk-5-3-n01": ("tablo",
        ["Amaç", "Uygun içerik seçimi"],
        [["Bilgilendirmek", "Tanım, sayı ve kaynak"],
         ["İkna etmek", "Gerekçe ve karşı görüşe yanıt"],
         ["Anlatmak", "Olay sırası ve ayrıntı"],
         ["Yönerge vermek", "Sıralı adımlar ve uyarılar"]],
        "İki sütunlu tablo: sol sütunda dört konuşma amacı, sağ sütunda her "
        "amaca uygun içerik seçimi."),

    "tr-g05-tur-tk-5-5-n01": ("tablo",
        ["Durum", "Uygun tepki"],
        [["Anlaşılmayan bir yer var", "Açıklayıcı soru sor"],
         ["Karşı görüş belirtilecek", "Önce katıldığın yeri söyle"],
         ["Söz kesildi", "Sırayı bekle ve konuya dön"],
         ["Bilgi eksik", "Kaynağını sor"]],
        "İki sütunlu tablo: sol sütunda dört sözlü etkileşim durumu, sağ "
        "sütunda her duruma uygun tepki."),

    "tr-g05-tur-tk-5-9-n01": ("tablo",
        ["Ses özelliği", "Ne zaman değişir?"],
        [["Vurgu", "Önemli sözcüğü öne çıkarırken"],
         ["Tonlama", "Soru, şaşkınlık ya da üzüntü aktarırken"],
         ["Hız", "Zor bir bilgi verirken yavaşlar"],
         ["Ses düzeyi", "Salonun büyüklüğüne göre ayarlanır"]],
        "İki sütunlu tablo: sol sütunda vurgu, tonlama, hız ve ses düzeyi; "
        "sağ sütunda her birinin hangi durumda değiştiği."),

    "tr-g05-tur-tk-5-23-n01": ("tablo",
        ["Aktarılacak tutum", "Sesteki karşılığı"],
        [["Kararlılık", "Düşük ton, ağır hız"],
         ["Heyecan", "Yüksek ton, hızlı akış"],
         ["Kibarlık", "Yumuşak ton, kısa duraklar"],
         ["Merak", "Cümle sonunda yükselen ton"]],
        "İki sütunlu tablo: sol sütunda dört tutum, sağ sütunda her tutumun "
        "ses tonu ve hız olarak karşılığı."),

    "tr-g05-tur-ty-5-1-n01": ("akis", [
        "Hazırlık: konuyu, amacı ve okuyucuyu belirle",
        "Planlama: ana düşünce ve yardımcı düşünceleri sırala",
        "Taslak: planı cümlelere dök",
        "Gözden geçirme: anlam ve sıralamayı düzelt",
        "Düzeltme: yazım ve noktalamayı denetle",
        "Paylaşma: yazıyı okuyucuya ulaştır",
    ], "Yazma sürecinin altı adımı yukarıdan aşağıya sıralanmıştır: hazırlık, "
       "planlama, taslak, gözden geçirme, düzeltme, paylaşma."),

    "tr-g05-tur-ty-5-3-n01": ("tablo",
        ["Yazı bölümü", "Görevi"],
        [["Giriş", "Konuyu tanıtır ve ilgi çeker"],
         ["Gelişme", "Ana düşünceyi örnek ve gerekçeyle destekler"],
         ["Sonuç", "Düşünceyi toparlar ve bağlar"]],
        "İki sütunlu tablo: sol sütunda giriş, gelişme ve sonuç bölümleri, "
        "sağ sütunda her bölümün yazıdaki görevi."),

    "tr-g05-tur-ty-5-20-n01": ("akis", [
        "Her paragrafın ana düşüncesini tek cümlede yaz",
        "Paragraflar arasında bağlantı sözcüğü kur",
        "Konudan sapan cümleleri çıkar",
        "Sıralamayı okuyucunun izleyebileceği biçime getir",
    ], "Paragraflar arası anlam bütünlüğünü kurmanın dört adımı sıralanmıştır: "
       "ana düşünceyi yazma, bağlantı kurma, sapan cümleleri çıkarma, "
       "sıralamayı düzenleme."),

    "tr-g05-tur-ty-5-21-n01": ("tablo",
        ["İşaret", "Nerede kullanılır?"],
        [["Nokta", "Tamamlanmış cümlenin sonunda"],
         ["Virgül", "Sıralı ögeler arasında"],
         ["Soru işareti", "Soru bildiren cümlenin sonunda"],
         ["İki nokta", "Açıklama ya da örnek sıralamadan önce"],
         ["Kesme işareti", "Özel adlara gelen ekleri ayırırken"]],
        "İki sütunlu tablo: sol sütunda beş noktalama işareti, sağ sütunda "
        "her işaretin hangi durumda kullanıldığı."),
}


ATIF = {
    "akis": ("\n\nGörselle çalışma\nAşağıdaki şemada bu sürecin adımları "
             "sırasıyla gösterilmiştir. Şemayı inceleyin ve kendi "
             "çalışmanızda hangi adımda olduğunuzu izleyin."),
    "tablo": ("\n\nGörselle çalışma\nAşağıdaki tabloda ölçütler ve "
              "karşılıkları yan yana verilmiştir. Tabloyu inceleyin ve bir "
              "örnekle karşılaştığınızda hangi satıra düştüğünü belirleyin."),
}


def uygula(kayitlar: list) -> tuple[int, dict]:
    """Figürü ve metindeki atfı AYNI işlemde üretir.

    Metnin hiç anmadığı figür süstür: çocuk ona bakmayı bilmez ve doğrulayıcı
    bunu kural 3 ile yakalar. Bu, atomiklik ilkesinin şekil hâlidir
    (AUTHORING_RULES §1 ve §6.1).
    """
    paket = next(k for k in kayitlar if k.get("type") == "pack")
    etiketler = dict(paket.get("labels") or {})
    eklenen = 0
    for k in kayitlar:
        if k.get("type") != "note":
            continue
        tasarim = TASARIM.get(k["id"])
        if not tasarim:
            continue
        if tasarim[0] == "akis":
            fig, yeni = akis(k["id"], tasarim[1], tasarim[2])
        else:
            fig, yeni = tablo(k["id"], tasarim[1], tasarim[2], tasarim[3])
        k["figure"] = fig
        govde = str(k.get("body") or "")
        if "Görselle çalışma" not in govde:
            k["body"] = govde.rstrip() + ATIF[tasarim[0]]
        etiketler.update(yeni)
        eklenen += 1
    paket["labels"] = etiketler
    return eklenen, etiketler


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaz", action="store_true")
    ns = ap.parse_args(argv)

    kayitlar = [json.loads(s) for s in
                PAKET.read_text(encoding="utf-8").splitlines() if s.strip()]
    notlar = [k for k in kayitlar if k.get("type") == "note"]
    eksik = [n["id"] for n in notlar if n["id"] not in TASARIM]
    if eksik:
        print(f"tasarımı olmayan not: {eksik}")
        return 1

    eklenen, etiketler = uygula(kayitlar)
    print(f"  not figürü      {eklenen}")
    print(f"  etiket anahtarı {len(etiketler)}")
    print(f"  soru figürü     0 (bilinçli: Türkçe soruları metin anlamaya "
          f"dayanıyor)")

    if not ns.yaz:
        print("(yazmak için --yaz)")
        return 0
    PAKET.write_text(
        "\n".join(json.dumps(k, ensure_ascii=False) for k in kayitlar) + "\n",
        encoding="utf-8", newline="\n")
    print(f"yazıldı: {PAKET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
