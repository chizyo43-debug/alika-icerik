#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Türkçe konu anlatımlarını 2.2'nin dokuz bölümlü gövdesine ayrıştırır.

Mevcut notlar zaten dokuz bölümün ALTISINI taşıyor ve yirmi birinin hepsinde
aynı başlıklar var: Kavramlar · Adım adım öğrenelim · Çözümlü örnek 1 ·
Çözümlü örnek 2 · Sık yapılan hata · Öz kontrol · Görselle çalışma. Yani bu
bir yeniden yazım değil, AYRIŞTIRMA işidir; var olan metin korunur.

Eksik olan üç bölüm elle yazıldı: "Bu konuda ne öğreneceğim?", "Ön bilgiler"
ve "Özet". Üçü de nota özgüdür; ortak bir kalıptan üretilmedi, çünkü aynı
cümlenin yirmi bir kez tekrarlanması bölümü var etmez, yalnız alanı doldurur.

Bölümler düzyazı olarak saklanır. Çözümlü örneği "soru / çözüm / cevap" diye
üçe bölmek, metinde bulunmayan sınırları uydurmak olurdu.

Kullanım:
    python tools/restructure_notes_turkce.py           # yalnız rapor
    python tools/restructure_notes_turkce.py --yaz
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "turkce" / "turkce-tum.jsonl"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pack_migrate_lib import bolumlere_ayir, oz_kontrol_listele  # noqa: E402

# Not kimliği → (ne öğreneceğim, ön bilgiler, özet).
EK_BOLUMLER = {
"tr-g05-tur-td-5-1-n01": (
 "Bir oyunu doğru öğrenmek için hangi videoyu, sesi ya da anlatımı "
 "seçeceğine kendin karar vermeyi öğreneceksin. Eğlenceli olanla amacına "
 "uygun olanı ayırt edebileceksin.",
 "Dinlemek ile izlemek arasındaki farkı ve bir metnin amacının olduğunu "
 "biliyor olman yeterli.",
 "Materyal seçimi rastgele değildir: önce amacını belirlersin, sonra "
 "kaynağın süresini, düzeyini ve güvenilirliğini amacına göre tartarsın. "
 "Beğendiğin kaynak değil, işini gören kaynak doğru kaynaktır."),

"tr-g05-tur-td-5-5-n01": (
 "Dinlediğin ya da izlediğin bir içerikte açıkça söylenen bilgiyi eksiksiz "
 "yakalamayı öğreneceksin: kim, ne, nerede, ne zaman, nasıl.",
 "Bir olayın kişileri, yeri ve zamanı olduğunu biliyor olman gerekir.",
 "Yüzey anlam, içerikte doğrudan söylenendir. Onu bulmak için tahmin "
 "etmeye değil, dikkatle dinlemeye ve söylenen bilgiyi ayırmaya ihtiyaç "
 "vardır. Söylenmeyeni eklemek yüzey anlamı bozar."),

"tr-g05-tur-td-5-7-n01": (
 "İzlediğin bir görüntüde doğrudan söylenmeyen bilgiyi, elindeki "
 "ipuçlarına dayanarak çıkarmayı öğreneceksin.",
 "Yüzey anlamı, yani doğrudan söyleneni bulabiliyor olman gerekir.",
 "Çıkarım tahmin değildir: her çıkarımın izlediğin içerikte bir dayanağı "
 "olmalıdır. Dayanağını gösteremediğin sonuç, çıkarım değil varsayımdır."),

"tr-g05-tur-td-5-10-n01": (
 "Aynı konuyu anlatan iki konuşmayı yan yana koyup farklarını ölçütlerle "
 "karşılaştırmayı öğreneceksin.",
 "Tek bir konuşmanın amacını ve ana düşüncesini belirleyebiliyor olman "
 "gerekir.",
 "Karşılaştırma, hangisinin daha hoş olduğunu söylemek değildir. Amaç, "
 "kanıt ve dil gibi ölçütleri belirlersin, iki konuşmayı bu ölçütlerin "
 "her birinde ayrı ayrı tartarsın."),

"tr-g05-tur-td-5-22-n01": (
 "Bir reklamın, duyurunun ya da videonun sana ne yaptırmak istediğini "
 "fark etmeyi ve iletiyi tartarak değerlendirmeyi öğreneceksin.",
 "Gerçek ile görüşü ayırt edebiliyor ve bir metnin amacı olduğunu biliyor "
 "olman gerekir.",
 "Her medya iletisinin bir hazırlayanı, bir hedef kitlesi ve bir amacı "
 "vardır. Dört soru sorarsın: kim hazırladı, kime sesleniyor, hangi kanıtı "
 "sunuyor, benden ne istiyor."),

"tr-g05-tur-to-5-5-n01": (
 "Okurken karşılaştığın bilmediğin bir sözcüğün anlamını, cümlenin "
 "kendisinden ve sözcüğün yapısından bulmayı öğreneceksin.",
 "Kök ve ek kavramlarını tanıyor, sözlük kullanmayı biliyor olman gerekir.",
 "Bilmediğin sözcükte ilk adım sözlük değil bağlamdır: cümle çoğu zaman "
 "anlamı çevreler. Tahminini sözlükle doğrular, sonra kendi cümlende "
 "kullanarak sınarsın."),

"tr-g05-tur-to-5-6-n01": (
 "Okuduğun metinde doğrudan yazılan bilgiyi eksiksiz ve doğru biçimde "
 "bulmayı öğreneceksin.",
 "Cümlede özne, yer ve zaman bildiren sözcükleri ayırt edebiliyor olman "
 "gerekir.",
 "Yüzey anlam metinde yazılıdır; aranacak yer bellidir. Kim sorusunun "
 "cevabı kişilerin anıldığı cümlelerde, ne zaman sorusununki zaman "
 "bildiren sözcüklerdedir. Yorum eklemek cevabı bozar."),

"tr-g05-tur-to-5-8-n01": (
 "Metinde yazmayan ama yazılanlardan çıkan sonuçlara ulaşmayı ve bu "
 "sonucu metindeki kanıtla desteklemeyi öğreneceksin.",
 "Metnin yüzey anlamını, yani doğrudan yazılanı bulabiliyor olman "
 "gerekir; çıkarım her zaman bunun üzerine kurulur.",
 "Çıkarım, metinde dağınık duran bilgileri birbirine bağlamaktır. Ulaştığın "
 "her sonucu metne geri götürüp hangi cümleye dayandığını "
 "gösterebilmelisin; gösteremiyorsan sonuç metnin değil senindir."),

"tr-g05-tur-to-5-13-n01": (
 "Bir cümlenin doğrulanabilir bir gerçek mi yoksa kişisel bir görüş mü "
 "olduğunu ayırt etmeyi öğreneceksin.",
 "Metinde açıkça verilen bilgiyi bulabiliyor olman gerekir; bir cümleyi "
 "tartabilmek için önce ne dediğini doğru anlamalısın.",
 "Ölçüt tektir: doğrulanabilir mi? Gerçek ölçülür ya da kaynaktan bakılır; "
 "görüş kişiden kişiye değişir. Bence, en güzel, sıkıcı gibi sözcükler "
 "görüşün işaretidir ama tek başına kanıt değildir; asıl soru "
 "doğrulanabilirliktir."),

"tr-g05-tur-to-5-14-n01": (
 "Bir öyküde kişileri, yeri, zamanı ve olayların sırasını tanıyıp bunların "
 "nasıl bir bütün oluşturduğunu görmeyi öğreneceksin.",
 "Metinde açıkça verilen bilgiyi bulabiliyor olman gerekir; kişileri ve "
 "zamanı bulamadan olay örgüsünü izleyemezsin.",
 "Öykü rastgele olaylar dizisi değildir: serimde kişiler ve ortam "
 "tanıtılır, düğümde olay bir soruna dönüşür, çözümde sorun bir sonuca "
 "bağlanır. Bu sıra bozulursa öykü anlaşılmaz."),

"tr-g05-tur-to-5-15-n01": (
 "Bir metnin öyküleyici mi, bilgilendirici mi yoksa şiir mi olduğunu "
 "işaretlerinden tanımayı öğreneceksin.",
 "Öykü unsurlarını ve bir metnin amacı olduğunu biliyor olman gerekir.",
 "Tür, metnin amacından ve biçim işaretlerinden anlaşılır: olay örgüsü "
 "öyküleyiciyi, tanım ve sayı bilgilendiriciyi, dize ve yinelenen sesler "
 "şiiri gösterir. Konu değil, amaç ve biçim belirleyicidir."),

"tr-g05-tur-to-5-24-n01": (
 "Afiş, duyuru, haber gibi medya metinlerinin ögelerini tanıyıp bunları "
 "eleştirel gözle değerlendirmeyi öğreneceksin.",
 "Gerçek ile görüşü ayırt edebiliyor olman gerekir; medya metninde ikisi "
 "çoğu zaman yan yana durur.",
 "Medya metninde başlık dikkat çeker, görsel iletiyi destekler, kaynak "
 "bilginin nereden geldiğini gösterir, çağrı senden bir davranış ister. "
 "Kaynağı olmayan bir iddia, ne kadar büyük yazılırsa yazılsın kanıt "
 "değildir."),

"tr-g05-tur-tk-5-1-n01": (
 "Bir konuşmayı baştan sona planlamayı: amacını belirlemeyi, içeriğini "
 "sıralamayı, prova etmeyi ve sonrasında değerlendirmeyi öğreneceksin.",
 "Giriş, gelişme ve sonuç bölümlerini biliyor olman gerekir; konuşmanın "
 "planı da bu üç bölüm üzerine kurulur.",
 "Konuşma bir süreçtir, anlık bir iş değil. Dinleyicini ve amacını önce "
 "belirlersin; içeriği ona göre seçer, giriş-gelişme-sonuç olarak sıralar, "
 "prova edip süreni ölçersin. Geri bildirim sürecin sonu değil parçasıdır."),

"tr-g05-tur-tk-5-3-n01": (
 "Konuşmanın amacına göre hangi bilgiyi, hangi örneği ve hangi sırayı "
 "seçeceğine karar vermeyi öğreneceksin.",
 "Konuşma sürecinin adımlarını biliyor olman gerekir; içerik seçimi o "
 "sürecin planlama adımında yapılır.",
 "İçerik amaca göre seçilir: bilgilendirmek istiyorsan tanım ve sayı, ikna "
 "etmek istiyorsan gerekçe ve karşı görüşe yanıt, yönerge vermek "
 "istiyorsan sıralı adımlar gerekir. Amaç değişince içerik de değişmelidir."),

"tr-g05-tur-tk-5-5-n01": (
 "Bir konuşma sırasında soru sormayı, karşı görüş belirtmeyi ve uzlaşmayı "
 "uygun bir dille yapmayı öğreneceksin.",
 "Konuşma sırasında sıra almanın ve dinlemenin gereğini biliyor olman "
 "yeterli.",
 "Uygun tepki duruma göre değişir: anlaşılmayan yerde açıklayıcı soru "
 "sorulur, karşı görüşten önce katılınan yer söylenir, söz kesildiğinde "
 "sıra beklenir. Haklı olmak, kaba olmayı gerektirmez."),

"tr-g05-tur-tk-5-9-n01": (
 "Konuşurken vurgu, tonlama, hız ve ses düzeyini anlama uygun biçimde "
 "kullanmayı öğreneceksin.",
 "Cümlenin anlamının sözcük seçimiyle değiştiğini biliyor olman gerekir.",
 "Aynı cümle farklı vurgu ve tonlamayla farklı anlamlara gelir. Vurgu "
 "önemli sözcüğü öne çıkarır, tonlama duyguyu taşır, hız zor bilgide "
 "yavaşlar, ses düzeyi ortamın büyüklüğüne göre ayarlanır."),

"tr-g05-tur-tk-5-23-n01": (
 "Konuşurken duygunu ve tutumunu amacına uygun biçimde yansıtmayı "
 "öğreneceksin.",
 "Vurgu, tonlama ve hızın anlamı değiştirdiğini biliyor olman gerekir.",
 "Tutum sesle taşınır: kararlılık düşük ton ve ağır hızla, heyecan yüksek "
 "ton ve hızlı akışla, kibarlık yumuşak ton ve kısa duraklarla duyulur. "
 "Amacına uymayan bir ton, doğru sözü bile yanlış anlatır."),

"tr-g05-tur-ty-5-1-n01": (
 "Bir yazıyı hazırlıktan paylaşmaya kadar adım adım yönetmeyi "
 "öğreneceksin.",
 "Cümle kurabiliyor ve paragrafın ne olduğunu biliyor olman gerekir.",
 "Yazmak tek oturuşta bitmez: hazırlık, planlama, taslak, gözden geçirme, "
 "düzeltme ve paylaşma adımları vardır. Taslağı ilk hâlinde bırakmak, "
 "sürecin ortasında durmaktır."),

"tr-g05-tur-ty-5-3-n01": (
 "Yazının amacına göre içeriğini seçmeyi ve giriş, gelişme, sonuç olarak "
 "yapılandırmayı öğreneceksin.",
 "Yazma sürecinin adımlarını ve paragrafın ne olduğunu biliyor olman "
 "gerekir.",
 "Her bölümün bir görevi vardır: giriş konuyu tanıtır ve ilgi çeker, "
 "gelişme ana düşünceyi örnek ve gerekçeyle destekler, sonuç düşünceyi "
 "toparlar. Görevi olmayan paragraf yazıdan çıkar."),

"tr-g05-tur-ty-5-20-n01": (
 "Cümleler ve paragraflar arasında anlam bağı kurup yazını akıcı hâle "
 "getirmeyi öğreneceksin.",
 "Paragrafın ana düşüncesini bulabiliyor olman gerekir; bağlantıyı "
 "kurmak için önce neyin bağlanacağını bilmelisin.",
 "Bütünlük, her paragrafın tek bir ana düşünceye hizmet etmesi ve "
 "paragrafların bağlantı sözcükleriyle birbirine bağlanmasıyla kurulur. "
 "Konudan sapan cümle, ne kadar güzel olursa olsun yazıdan çıkarılır."),

"tr-g05-tur-ty-5-21-n01": (
 "Yazarken noktalama işaretlerini ve yazım kurallarını doğru "
 "uygulamayı öğreneceksin.",
 "Cümlenin nerede başlayıp nerede bittiğini ayırt edebiliyor olman "
 "gerekir.",
 "Noktalama süs değildir, anlamı taşır: nokta cümleyi bitirir, virgül "
 "sıralı ögeleri ayırır, kesme işareti özel ada gelen eki ayırır. Yanlış "
 "yerdeki bir virgül cümlenin anlamını değiştirebilir."),
}


def govdeyi_kur(not_kaydi: dict) -> dict | None:
    parcalar = bolumlere_ayir(str(not_kaydi.get("body") or ""))
    ek = EK_BOLUMLER.get(not_kaydi["id"])
    if not ek:
        return None
    ornekler = [parcalar.get("Çözümlü örnek 1", ""),
                parcalar.get("Çözümlü örnek 2", "")]
    ornekler = [o for o in ornekler if o]
    oz = oz_kontrol_listele(parcalar.get("Öz kontrol", ""))
    if len(ornekler) < 2 or len(oz) < 3:
        return None
    return {
        "whatIWillLearn": ek[0],
        "keyConcepts": parcalar.get("Kavramlar", ""),
        "priorKnowledge": ek[1],
        "steps": parcalar.get("Adım adım öğrenelim", ""),
        "workedExamples": ornekler,
        "commonMistakes": parcalar.get("Sık yapılan hata", ""),
        "selfCheck": oz,
        "summary": ek[2],
        "figureNote": parcalar.get("Görselle çalışma", ""),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaz", action="store_true")
    ns = ap.parse_args(argv)

    kayitlar = [json.loads(s) for s in
                PAKET.read_text(encoding="utf-8").splitlines() if s.strip()]
    donusen = 0
    basarisiz = []
    for k in kayitlar:
        if k.get("type") != "note":
            continue
        if isinstance(k.get("body"), dict):
            donusen += 1
            continue
        govde = govdeyi_kur(k)
        if govde is None:
            basarisiz.append(k["id"])
            continue
        k["body"] = govde
        donusen += 1

    print(f"  dokuz bölüme ayrılan not  {donusen}")
    if basarisiz:
        print(f"  AYRIŞTIRILAMAYAN          {basarisiz}")
        return 1
    ornek = next(k for k in kayitlar if k.get("type") == "note")
    print(f"  örnek öz kontrol maddesi  {len(ornek['body']['selfCheck'])}")

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
