#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matematik konu anlatımlarını tamamlar: 23 figür + dokuz bölümlü gövde.

Türkçe'de olduğu gibi notlar zaten altı bölümü taşıyor (Kavramlar, Adım adım
öğrenelim, Çözümlü örnek 1-2, Sık yapılan hata, Öz kontrol); bu yüzden iş
ayrıştırma. Eksik üç bölüm ("Ne öğreneceğim", "Ön bilgiler", "Özet") ve figür
elle yazıldı.

Matematikte figür seçimi Türkçe'den kolay: konuların çoğu zaten görsel. Yine
de kural aynı — figür notun ÖĞRETTİĞİ şeyi gösterir, süsleme değildir. Sayı
doğrusu, kesir modeli, açı, ızgara ve çokgen katalogda tam bu iş için var.

Figür ile metindeki atıf AYNI işlemde üretilir (AUTHORING_RULES §6.1).

Kullanım:
    python tools/finish_notes_matematik.py           # yalnız rapor
    python tools/finish_notes_matematik.py --yaz
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "matematik" / "matematik-tum.jsonl"

from pack_migrate_lib import bolumlere_ayir, oz_kontrol_listele  # noqa: E402


def _anahtar(not_id: str, metin: str) -> str:
    ozet = hashlib.sha256(metin.encode("utf-8")).hexdigest()[:12]
    return f"{not_id}.visual.{ozet}"


# Not kimliği → (figür üreticisi, alt metin, atıf cümlesi, ne öğreneceğim,
#                ön bilgiler, özet)
# Figür üreticisi: (kind, ek alanlar) ya da ("flow", adım listesi) /
#                  ("table", (başlıklar, satırlar))
TASARIM = {
"tr.g05.mat.5.1.1.note.01": (
 ("table", (["Bölük", "Basamaklar"],
            [["Milyonlar", "yüz milyonlar, on milyonlar, milyonlar"],
             ["Binler", "yüz binler, on binler, binler"],
             ["Birler", "yüzler, onlar, birler"]])),
 "Üç satırlı tablo: her satırda bir bölük ve o bölüğü oluşturan üç basamak.",
 "Aşağıdaki tabloyu inceleyin ve okuduğunuz sayının hangi bölükte kaç "
 "basamağı olduğunu belirleyin.",
 "Çok basamaklı doğal sayıları bölüklerine ayırmayı ve doğru okumayı "
 "öğreneceksin.",
 "Basamak ve basamak değeri kavramlarını biliyor olman gerekir.",
 "Sayı sağdan üçerli bölüklere ayrılır; her bölüğün adı vardır. Tamamı "
 "sıfır olan bölük okunmaz ve binler bölüğü 1 ise 'bir bin' değil yalnız "
 "'bin' denir."),

"tr.g05.mat.5.1.1.note.02": (
 ("numberline", {"min": 0, "max": 100000, "step": 25000,
                 "marks": [0, 25000, 50000, 75000, 100000]}),
 "Sıfırdan yüz bine kadar, yirmi beş binlik aralıklarla bölünmüş sayı "
 "doğrusu.",
 "Aşağıdaki şekli inceleyin ve yuvarlanacak sayının hangi iki işaret "
 "arasında durduğunu belirleyin.",
 "Büyük sayıları en yakın onluğa, yüzlüğe ve binliğe yuvarlamayı "
 "öğreneceksin.",
 "Sayıları büyüklüklerine göre sıralayabiliyor olman gerekir.",
 "Yuvarlama, sayıyı yakın bir tam değere taşımaktır. Hangi basamağa "
 "yuvarlanacaksa bir sağındaki rakama bakılır: 5 ve üzeriyse yukarı, "
 "altındaysa aşağı yuvarlanır."),

"tr.g05.mat.5.1.1.note.03": (
 ("table", (["Karşılaştırma", "Kural"],
            [["Basamak sayısı farklı", "Çok basamaklı olan büyüktür"],
             ["Basamak sayısı aynı", "Soldan ilk farklı rakama bakılır"],
             ["Rakamlar da aynı", "Sayılar eşittir"]])),
 "İki sütunlu tablo: sol sütunda üç karşılaştırma durumu, sağ sütunda her "
 "durumda uygulanan kural.",
 "Aşağıdaki tabloyu inceleyin ve karşılaştırdığınız iki sayının hangi "
 "satıra düştüğünü belirleyin.",
 "Çok basamaklı sayıları karşılaştırmayı ve sıralamayı öğreneceksin.",
 "Basamak değerini ve sayı okumayı biliyor olman gerekir.",
 "Karşılaştırmada önce basamak sayısına bakılır; eşitse soldan ilk farklı "
 "rakam belirleyicidir. Sağdan başlamak yaygın bir hatadır."),

"tr.g05.mat.5.1.2.note.01": (
 ("flow", ["Problemi kendi cümlelerinle yaz",
           "Verilenleri ve isteneni ayır",
           "Hangi işlemin gerektiğine karar ver",
           "İşlemi yap",
           "Sonucu problemin sorusuyla karşılaştır"]),
 "Problem çözmenin beş adımı yukarıdan aşağıya sıralanmış akış şeması.",
 "Aşağıdaki şemayı inceleyin ve çözdüğünüz problemde hangi adımda "
 "olduğunuzu izleyin.",
 "Doğal sayılarla kurulan problemleri adım adım çözmeyi öğreneceksin.",
 "Dört işlemi yapabiliyor olman gerekir.",
 "Problem çözmek işlem yapmak değildir: önce verilen ile istenen ayrılır, "
 "sonra işleme karar verilir. Sonucu soruyla karşılaştırmadan bırakmak en "
 "sık yapılan hatadır."),

"tr.g05.mat.5.1.2.note.02": (
 ("table", (["İfade", "İşlem"],
            [["toplamı, kadar arttı", "toplama"],
             ["farkı, kadar azaldı", "çıkarma"],
             ["katı, her birinde", "çarpma"],
             ["eşit paylaştırma, kaçar", "bölme"]])),
 "İki sütunlu tablo: sol sütunda problem metninde geçen ifadeler, sağ "
 "sütunda her ifadenin işaret ettiği işlem.",
 "Aşağıdaki tabloyu inceleyin ve problem metnindeki ifadenin hangi işleme "
 "karşılık geldiğini belirleyin.",
 "Problem metnindeki ifadelerden hangi işlemin gerektiğini anlamayı "
 "öğreneceksin.",
 "Dört işlemin ne yaptığını biliyor olman gerekir.",
 "İfadeler işleme ipucu verir ama tek başına yeterli değildir; anlamı "
 "denetlemeden anahtar sözcüğe göre işlem seçmek yanlış sonuca götürür."),

"tr.g05.mat.5.1.3.note.01": (
 ("fraction", {"style": "bar", "parts": 8, "filled": 3}),
 "Sekiz eşit parçaya bölünmüş bir çubuk; parçaların üçü boyalı.",
 "Aşağıdaki şekli inceleyin ve boyalı parçanın bütüne oranını kesirle "
 "yazın.",
 "Bir kesri model, sayı ve sözle gösterebilmeyi öğreneceksin.",
 "Bir bütünü eşit parçalara ayırabiliyor olman gerekir.",
 "Kesirde payda bütünün kaç eşit parçaya ayrıldığını, pay bu parçalardan "
 "kaçının alındığını gösterir. Parçalar eşit değilse kesir yazılamaz."),

"tr.g05.mat.5.1.4.note.01": (
 ("fraction", {"style": "pie", "parts": 4, "filled": 3}),
 "Dört eşit dilime bölünmüş bir daire; dilimlerin üçü boyalı.",
 "Aşağıdaki şekli inceleyin ve boyalı kısmın bütünden büyük mü küçük mü "
 "olduğunu belirleyin.",
 "Kesirleri birim kesir ve bütünle karşılaştırmayı öğreneceksin.",
 "Kesirde pay ve paydanın ne anlattığını biliyor olman gerekir.",
 "Payı paydasından küçük kesir bütünden küçüktür; eşitse bütüne eşittir. "
 "Payda büyüdükçe parçalar küçülür, bu yüzden büyük payda her zaman büyük "
 "kesir demek değildir."),

"tr.g05.mat.5.1.4.note.02": (
 ("numberline", {"min": 0, "max": 1, "step": 0.25,
                 "marks": [0, 0.25, 0.5, 0.75, 1]}),
 "Sıfır ile bir arasında, dörtte birlik aralıklarla işaretlenmiş sayı "
 "doğrusu.",
 "Aşağıdaki şekli inceleyin ve karşılaştırdığınız kesirlerin doğru üzerinde "
 "hangi sırada durduğunu belirleyin.",
 "Paydaları farklı kesirleri karşılaştırmayı öğreneceksin.",
 "Denk kesir kavramını ve kesirleri modelle gösterebilmeyi biliyor olman "
 "gerekir.",
 "Paydaları farklı kesirler doğrudan karşılaştırılamaz; ya paydalar "
 "eşitlenir ya sayı doğrusunda yerleri bulunur. Payları karşılaştırmak tek "
 "başına yanıltır."),

"tr.g05.mat.5.1.4.note.03": (
 ("table", (["Durum", "Nasıl karşılaştırılır?"],
            [["Paydalar eşit", "Payı büyük olan büyüktür"],
             ["Paylar eşit", "Paydası küçük olan büyüktür"],
             ["İkisi de farklı", "Paydalar eşitlenir"]])),
 "İki sütunlu tablo: sol sütunda üç karşılaştırma durumu, sağ sütunda her "
 "durumda uygulanan yol.",
 "Aşağıdaki tabloyu inceleyin ve elinizdeki iki kesrin hangi satıra "
 "düştüğünü belirleyin.",
 "Kesirleri karşılaştırmanın üç durumunu ayırt etmeyi öğreneceksin.",
 "Denk kesir bulmayı biliyor olman gerekir.",
 "Karşılaştırma yolu paylara ve paydalara göre değişir. Payı büyük olanın "
 "her zaman büyük olduğunu sanmak sık yapılan bir yanılgıdır."),

"tr.g05.mat.5.2.note.01": (
 ("table", (["Özellik", "Örnek"],
            [["Değişme", "7 + 5 = 5 + 7"],
             ["Birleşme", "(2 + 3) + 4 = 2 + (3 + 4)"],
             ["Etkisiz eleman", "9 + 0 = 9 ve 9 × 1 = 9"],
             ["Yutan eleman", "9 × 0 = 0"]])),
 "İki sütunlu tablo: sol sütunda dört işlem özelliği, sağ sütunda her "
 "özelliğin sayısal örneği.",
 "Aşağıdaki tabloyu inceleyin ve verilen eşitliğin hangi özelliğe örnek "
 "olduğunu belirleyin.",
 "Toplama ve çarpmanın özelliklerini tanımayı ve eşitliği korumayı "
 "öğreneceksin.",
 "Dört işlemi yapabiliyor olman gerekir.",
 "Eşitliğin iki yanı aynı değeri taşır. Değişme ve birleşme toplama ile "
 "çarpmada geçerlidir; çıkarma ve bölmede geçerli değildir."),

"tr.g05.mat.5.2.note.02": (
 ("flow", ["Parantez içi",
           "Çarpma ve bölme (soldan sağa)",
           "Toplama ve çıkarma (soldan sağa)"]),
 "İşlem önceliğinin üç basamağını yukarıdan aşağıya gösteren akış şeması.",
 "Aşağıdaki şemayı inceleyin ve işlemi hangi sırayla yapacağınızı "
 "belirleyin.",
 "Bir işlemde hangi adımın önce yapılacağını öğreneceksin.",
 "Dört işlemi yapabiliyor olman gerekir.",
 "İşlem önceliği soldan sağa yapmak değildir: önce parantez, sonra çarpma "
 "ve bölme, en son toplama ve çıkarma gelir. Aynı öncelikteki işlemler "
 "soldan sağa yapılır."),

"tr.g05.mat.5.2.note.03": (
 ("numberline", {"min": 3, "max": 23, "step": 5,
                 "marks": [3, 8, 13, 18, 23]}),
 "Üçten yirmi üçe kadar beşer artan sayıların işaretlendiği sayı doğrusu.",
 "Aşağıdaki şekli inceleyin ve işaretler arasındaki artışın kaç olduğunu "
 "belirleyin.",
 "Sayı ve şekil örüntülerindeki kuralı bulmayı öğreneceksin.",
 "Toplama ve çarpmayı biliyor olman gerekir.",
 "Örüntüde kural, ardışık terimler arasındaki ilişkidir. Kuralı bulmak için "
 "en az iki farklı adıma bakmak gerekir; tek adıma bakıp genelleme yapmak "
 "yanıltır."),

"tr.g05.mat.5.2.note.04": (
 ("flow", ["Başla", "Girdiyi al", "Koşulu denetle",
           "Uygun adımı uygula", "Sonucu yaz", "Bitir"]),
 "Bir algoritmanın altı adımını başlangıçtan bitişe gösteren akış şeması.",
 "Aşağıdaki şemayı inceleyin ve her adımın bir öncekine nasıl bağlandığını "
 "izleyin.",
 "Bir işi adım adım, sırası belli bir yönergeye dönüştürmeyi öğreneceksin.",
 "Bir problemi çözüm adımlarına ayırabiliyor olman gerekir.",
 "Algoritma, bir işin başı ve sonu belli, sırası değişmeyen adımlarıdır. "
 "Adımlardan biri atlanırsa ya da sırası değişirse sonuç değişir."),

"tr.g05.mat.5.3.note.01": (
 ("flow", ["Çizim hedefini belirle",
           "Uygun aracı seç: çizgeç, pergel, gönye, açıölçer",
           "Çizimi yap",
           "Sonucu hedefle karşılaştır"]),
 "Geometrik çizim yapmanın dört adımını sırayla gösteren akış şeması.",
 "Aşağıdaki şemayı inceleyin ve yapacağınız çizim için hangi aracın "
 "gerektiğini belirleyin.",
 "Temel geometrik çizimleri uygun araçla yapmayı öğreneceksin.",
 "Doğru, doğru parçası ve ışın kavramlarını biliyor olman gerekir.",
 "Her aracın bir işi vardır: çizgeç düz çizer, pergel eşit uzaklık taşır, "
 "gönye dik açı verir, açıölçer açı ölçer. Araç seçimi hedefe göre yapılır."),

"tr.g05.mat.5.3.note.02": (
 ("angle", {"degrees": 45}),
 "Ortak köşeden çıkan iki ışın; biri yatay, diğeri sağ üst yöne eğik.",
 "Aşağıdaki şekli inceleyin ve açının kollarının nereden çıktığını "
 "belirleyin.",
 "Açıyı tanımayı, adlandırmayı ve açıölçerle ölçmeyi öğreneceksin.",
 "Işın kavramını biliyor olman gerekir.",
 "Açı, ortak bir başlangıç noktasından çıkan iki ışının oluşturduğu "
 "şekildir. Açının ölçüsü kollarının uzunluğuna değil, aralarındaki "
 "açıklığa bağlıdır."),

"tr.g05.mat.5.3.note.03": (
 ("table", (["Açı türü", "Ölçüsü"],
            [["Dar", "0° ile 90° arasında"],
             ["Dik", "tam 90°"],
             ["Geniş", "90° ile 180° arasında"],
             ["Doğru", "tam 180°"]])),
 "İki sütunlu tablo: sol sütunda dört açı türü, sağ sütunda her türün ölçü "
 "aralığı.",
 "Aşağıdaki tabloyu inceleyin ve ölçtüğünüz açının hangi satıra düştüğünü "
 "belirleyin.",
 "Açıları ölçülerine göre sınıflandırmayı öğreneceksin.",
 "Açıölçerle açı ölçebiliyor olman gerekir.",
 "Sınıflandırma ölçüye dayanır: 90° ve 180° sınır değerlerdir ve kendi "
 "adları vardır. Sınır değeri komşu aralığa katmak sık yapılan hatadır."),

"tr.g05.mat.5.3.note.04": (
 ("shape", {"type": "polygon", "dims": {"a": 5, "b": 5, "c": 5}}),
 "Kenarları eşit uzunlukta kapalı bir çokgen.",
 "Aşağıdaki şekli inceleyin ve kenar ile köşe sayısını sayın.",
 "Çokgenleri kenar sayısına göre tanımayı ve adlandırmayı öğreneceksin.",
 "Doğru parçası kavramını biliyor olman gerekir.",
 "Çokgen, doğru parçalarından oluşan kapalı bir şekildir. Kenar sayısı köşe "
 "sayısına eşittir; şeklin kapalı olmaması onu çokgen olmaktan çıkarır."),

"tr.g05.mat.5.3.note.05": (
 ("shape", {"type": "triangle", "dims": {"a": 6, "b": 6, "c": 6}}),
 "Üç kenarı eşit uzunlukta bir üçgen.",
 "Aşağıdaki şekli inceleyin ve kenarların birbirine göre uzunluğunu "
 "karşılaştırın.",
 "Pergel ve çizgeçle üçgen çizmeyi öğreneceksin.",
 "Pergelin eşit uzaklık taşıdığını biliyor olman gerekir.",
 "Üçgen inşasında pergel kenar uzunluğunu taşır. Herhangi iki kenarın "
 "toplamı üçüncüden küçükse üçgen kapanmaz."),

"tr.g05.mat.5.4.note.01": (
 ("shape", {"type": "rect", "dims": {"w": 8, "h": 3}}),
 "Uzun kenarı sekiz, kısa kenarı üç birim olan bir dikdörtgen.",
 "Aşağıdaki şekli inceleyin ve çevreyi bulmak için hangi kenarları "
 "toplayacağınızı belirleyin.",
 "Dikdörtgenin çevresini hesaplamayı öğreneceksin.",
 "Toplama ve çarpmayı biliyor olman gerekir.",
 "Çevre, kenar uzunluklarının toplamıdır. Dikdörtgende karşılıklı kenarlar "
 "eşit olduğu için çevre iki kenarın toplamının iki katıdır."),

"tr.g05.mat.5.4.note.02": (
 ("grid", {"cols": 8, "rows": 3}),
 "Sekiz sütun ve üç satırdan oluşan birim kare ızgarası.",
 "Aşağıdaki şekli inceleyin ve toplam birim kare sayısını sütun ve satır "
 "sayısından bulun.",
 "Dikdörtgenin alanını birim karelerle ve çarpmayla bulmayı öğreneceksin.",
 "Çarpma işlemini biliyor olman gerekir.",
 "Alan, şeklin kapladığı birim kare sayısıdır. Dikdörtgende bu sayı "
 "sütun ile satırın çarpımına eşittir; alan çevreyle karıştırılmamalıdır."),

"tr.g05.mat.5.4.note.03": (
 ("table", (["Aranan", "Verilenler", "Yol"],
            [["Alan", "iki kenar", "kenarları çarp"],
             ["Çevre", "iki kenar", "toplamın iki katı"],
             ["Kenar", "alan ve bir kenar", "alanı kenara böl"]])),
 "Üç sütunlu tablo: satırlarda alan, çevre ve kenar; sütunlarda ne "
 "verildiği ve hangi yolun izleneceği.",
 "Aşağıdaki tabloyu inceleyin ve elinizdeki problemin hangi satıra "
 "düştüğünü belirleyin.",
 "Alan ve çevre problemlerinde hangi yolu izleyeceğine karar vermeyi "
 "öğreneceksin.",
 "Alan ve çevre hesabını ayrı ayrı biliyor olman gerekir.",
 "Problemde önce ne verildiği ve ne istendiği ayrılır. Alan ile çevreyi "
 "karıştırmak en sık yapılan hatadır: biri kapladığı yeri, diğeri "
 "kenarlarının toplamını anlatır."),

"tr.g05.mat.5.5.note.01": (
 ("chart", {"style": "bar",
            "categoryKeys": ["kirmizi", "mavi", "yesil", "sari"],
            "values": [7, 4, 6, 3]}),
 "Dört kategorili sütun grafiği: kırmızı 7, mavi 4, yeşil 6, sarı 3.",
 "Aşağıdaki grafiği inceleyin ve hangi kategorinin en çok, hangisinin en "
 "az olduğunu belirleyin.",
 "Kategorik veriyi toplamayı, tabloya ve sütun grafiğine dökmeyi "
 "öğreneceksin.",
 "Sayıları karşılaştırabiliyor ve toplama yapabiliyor olman gerekir.",
 "Sütun grafiğinde her sütunun yüksekliği o kategorinin sıklığıdır. "
 "Sıklıkların toplamı veri sayısına eşit olmalıdır; eşit değilse veri "
 "eksik ya da fazla sayılmıştır."),

"tr.g05.mat.5.6.note.01": (
 ("table", (["Durum", "Olasılık"],
            [["Kesin", "her zaman olur"],
             ["Mümkün", "olabilir de olmayabilir de"],
             ["İmkânsız", "hiçbir zaman olmaz"]])),
 "İki sütunlu tablo: sol sütunda üç olasılık durumu, sağ sütunda her "
 "durumun anlamı.",
 "Aşağıdaki tabloyu inceleyin ve verilen olayın hangi satıra düştüğünü "
 "belirleyin.",
 "Bir olayın kesin, mümkün ya da imkânsız olduğunu ayırt etmeyi "
 "öğreneceksin.",
 "Bir deneyin olası sonuçlarını sayabiliyor olman gerekir.",
 "Olasılık, bir olayın gerçekleşme ihtimalidir. Kesin olay her denemede "
 "olur, imkânsız olay hiç olmaz; ikisinin arasındaki her şey mümkündür."),
}


def figur_uret(not_id: str, tasarim, alt: str) -> tuple[dict, dict]:
    tur, veri = tasarim
    etiketler = {}
    alt_a = _anahtar(not_id, alt)
    etiketler[alt_a] = alt

    if tur == "flow":
        dugumler = []
        for i, metin in enumerate(veri):
            a = _anahtar(not_id, metin)
            etiketler[a] = metin
            dugumler.append({"id": f"a{i + 1}", "labelKey": a})
        fig = {"kind": "flow", "nodes": dugumler,
               "edges": [{"from": f"a{i + 1}", "to": f"a{i + 2}"}
                         for i in range(len(veri) - 1)],
               "direction": "down", "altTextKey": alt_a}
    elif tur == "table":
        basliklar, satirlar = veri
        bas_a = []
        for metin in basliklar:
            a = _anahtar(not_id, metin)
            etiketler[a] = metin
            bas_a.append(a)
        satir_a = []
        for satir in satirlar:
            hucre = []
            for metin in satir:
                a = _anahtar(not_id, metin)
                etiketler[a] = metin
                hucre.append({"key": a})
            satir_a.append(hucre)
        fig = {"kind": "table", "headerKeys": bas_a, "rows": satir_a,
               "altTextKey": alt_a}
    elif tur == "chart":
        veri = dict(veri)
        kat_a = []
        for metin in veri["categoryKeys"]:
            a = _anahtar(not_id, metin)
            etiketler[a] = metin
            kat_a.append(a)
        fig = {"kind": "chart", "style": veri["style"], "categoryKeys": kat_a,
               "values": veri["values"], "altTextKey": alt_a}
    else:
        fig = {"kind": tur, **veri, "altTextKey": alt_a}
    return fig, etiketler


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaz", action="store_true")
    ns = ap.parse_args(argv)

    kayitlar = [json.loads(s) for s in
                PAKET.read_text(encoding="utf-8").splitlines() if s.strip()]
    paket = next(k for k in kayitlar if k.get("type") == "pack")
    etiketler = dict(paket.get("labels") or {})

    eksik = [k["id"] for k in kayitlar
             if k.get("type") == "note" and k["id"] not in TASARIM]
    if eksik:
        print(f"tasarımı olmayan not: {eksik}")
        return 1

    donusen = 0
    for k in kayitlar:
        if k.get("type") != "note":
            continue
        fig_t, alt, atif, ogren, on, ozet = TASARIM[k["id"]]
        fig, yeni = figur_uret(k["id"], fig_t, alt)
        etiketler.update(yeni)
        k["figure"] = fig

        parcalar = bolumlere_ayir(str(k.get("body") or ""))
        ornekler = [parcalar.get("Çözümlü örnek 1", ""),
                    parcalar.get("Çözümlü örnek 2", "")]
        ornekler = [o for o in ornekler if o]
        oz = oz_kontrol_listele(parcalar.get("Öz kontrol", ""))
        if len(ornekler) < 2 or len(oz) < 3:
            print(f"AYRIŞTIRILAMADI: {k['id']} örnek={len(ornekler)} öz={len(oz)}")
            return 1
        k["body"] = {
            "whatIWillLearn": ogren,
            "keyConcepts": parcalar.get("Kavramlar", ""),
            "priorKnowledge": on,
            "steps": parcalar.get("Adım adım öğrenelim", ""),
            "workedExamples": ornekler,
            "commonMistakes": parcalar.get("Sık yapılan hata", ""),
            "selfCheck": oz,
            "summary": ozet,
            "figureNote": atif,
        }
        donusen += 1

    paket["labels"] = etiketler
    print(f"  dokuz bölüme ayrılan not  {donusen}")
    print(f"  not figürü                {donusen}")
    print(f"  etiket anahtarı           {len(etiketler)}")

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
