#!/usr/bin/env python3
"""Repair the misaligned structured sections of SB.5.6.2 without touching questions."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from build_unique_question_banks import ROOT, pending


TARGET = ROOT / "turkiye" / "5-sinif" / "sosyal-bilgiler" / "sosyal-bilgiler-tum.jsonl"
NOTE_ID = "tr-g05-sosyal-sb-5-6-2-note"


SECTIONS: dict[str, Any] = {
    "whatIWillLearn": (
        "Teknolojik bir ürünü yalnızca kullanıp kullanmama açısından değil; amaç, süre, güvenlik, "
        "mahremiyet, sağlık, çevre ve kaynak tasarrufu ölçütleriyle değerlendirmeyi öğreneceğim. "
        "Topladığım kanıtlardan hareketle bilinçli kullanımı destekleyen bir ürün veya öneri oluşturacağım."
    ),
    "priorKnowledge": (
        "Teknoloji, insanların bir ihtiyacı karşılamak ya da bir sorunu çözmek için geliştirdiği araç, "
        "yöntem ve sistemlerin bütünüdür. Bir ürünün yararlı olması, her koşulda ve sınırsız kullanılmasının "
        "doğru olduğu anlamına gelmez. Güvenli parola, kişisel bilgi, ekran süresi, enerji tasarrufu, geri "
        "dönüşüm ve kullanım kılavuzu kavramları bu konuyu anlamak için başlangıç bilgisidir."
    ),
    "keyConcepts": (
        "Bilinçli kullanım; ürünü gerçek ihtiyaca uygun seçmek, kullanım amacını önceden belirlemek, süreyi "
        "planlamak, güvenlik kurallarına uymak ve sonuçlarını izlemektir. Dijital mahremiyet; ad, adres, "
        "konum, parola ve fotoğraf gibi kişisel verileri izinsiz paylaşmamayı gerektirir. Dijital ayak izi, "
        "çevrim içi işlemlerin geride bıraktığı kayıtlardır. Kanıt; ekran süresi kaydı, elektrik faturası, "
        "kullanım kılavuzu, gözlem çizelgesi veya güvenilir kurum açıklaması gibi denetlenebilir bilgidir. "
        "Yorum ise bu kanıta dayanarak ulaşılan sonuçtur; yorum kanıtın söylediğinden daha geniş olmamalıdır. "
        "Sağlık açısından uygun duruş, aydınlatma, mola ve ses düzeyi; çevre açısından cihazı gereksiz açık "
        "bırakmama, onarım ve elektronik atığı doğru toplama önemlidir. Oluşturulan afiş, kontrol listesi veya "
        "kullanım planı; açık bir hedef, uygulanabilir kurallar ve bu kuralların gerekçelerini içermelidir."
    ),
    "steps": (
        "KANIT basamakları kullanılır: (1) Konuyu ve hedefi belirle: Hangi ürün, kim tarafından, hangi amaçla "
        "kullanılıyor? (2) Araştırılabilir bir soru yaz: Örneğin 'Bildirimleri kapatmak ödev süresindeki "
        "dikkat dağılmasını azaltıyor mu?' (3) Nesnel kanıt topla: Aynı süre boyunca kullanım kaydı, gözlem "
        "çizelgesi veya güvenilir kurum bilgisi kullan; özel verileri kaydetme. (4) Kanıtı ölçütlerle incele: "
        "Amaç, süre, sağlık, güvenlik, mahremiyet, maliyet ve çevre sonuçlarını ayrı ayrı değerlendir. (5) "
        "Kanıt ile yorumu ayır: Gözlenen sonucu yaz, sonra yalnız bu sonucun desteklediği çıkarımı kur. (6) "
        "Uygulanabilir çözüm geliştir: Zamanlayıcı, bildirim ayarı, ortak şarj noktası, güvenlik kontrol listesi "
        "gibi somut bir öneri seç. (7) Ürünü oluştur ve gerekçelendir: Her kuralın hangi riski azalttığını veya "
        "hangi yararı güçlendirdiğini belirt. (8) Geri bildirimle düzelt: Önerinin uygulanabilirliğini bir "
        "kontrol listesiyle sınayıp eksik ölçütleri tamamla."
    ),
    "workedExamples": [
        (
            "Örnek 1 — Tabletle ödev: Elif üç gün boyunca tablet kullanımını kaydeder. Birinci gün bildirimler "
            "açıkken 40 dakikalık ödev sırasında 9 kez uygulama değiştirir ve ödevi 65 dakikada bitirir. İkinci "
            "ve üçüncü gün bildirimleri kapatıp 25 dakikalık çalışma ve 5 dakikalık mola planı uygular; uygulama "
            "değiştirme sayısı 2 ve 1, bitirme süresi 48 ve 46 dakika olur. Kanıt, bu üç denemede planlı kullanımın "
            "dikkat dağılmasını azalttığını destekler; 'tablet kullanan herkes başarısız olur' sonucunu desteklemez. "
            "Elif'in ürünü, bildirimleri kapatma, çalışma süresini belirleme, mola verme ve iş bitince cihazı "
            "kapatma adımlarını içeren bir ödev kontrol listesidir."
        ),
        (
            "Örnek 2 — Fotoğraf paylaşımı: Bir sınıf etkinliğinde öğrenciler afiş hazırlamak için fotoğraf "
            "kullanacaktır. Fotoğrafta öğrencilerin yüzleri, okul adı ve konum bilgisi görünmektedir. 'Fotoğrafı "
            "hemen paylaşmak' hızlı olsa da mahremiyet ve güvenlik ölçütlerini karşılamaz. Bilinçli çözüm; fotoğrafta "
            "yer alan kişilerden ve gerekli yetişkinden izin almak, okul ve konum bilgisini kaldırmak, paylaşım "
            "kitlesini sınırlandırmak ve mümkünse kişileri tanınmaz gösteren başka bir görsel seçmektir. Hazırlanan "
            "ürün, 'izin al — kişisel veriyi denetle — hedef kitleyi seç — paylaşmadan önce yeniden kontrol et' "
            "basamaklarından oluşan bir paylaşım kartıdır."
        ),
    ],
    "commonMistakes": (
        "'Bilinçli kullanım yalnız ekran süresini azaltmaktır' yanlıştır; güvenlik, mahremiyet, sağlık, amaç ve "
        "çevre de değerlendirilir. 'İnternette bulunan ilk bilgi kanıttır' yanlıştır; yazar, kurum, tarih ve başka "
        "güvenilir kaynaklarla doğrulama gerekir. 'Parolayı yakın arkadaşa vermek güvenlidir' yanlıştır; parola "
        "kişiye özeldir. 'Bir gözlem herkes için aynı sonucu kanıtlar' aşırı genellemedir. 'Cihazı hiç kullanmamak "
        "bilinçli kullanımdır' da doğru değildir; amaç yararlı kullanımı güvenli ve ölçülü hâle getirmektir. Bir "
        "afişte yalnız yasakları sıralamak yerine her önerinin gerekçesi ve uygulanabilir bir davranış bulunmalıdır."
    ),
    "selfCheck": [
        "Bir teknolojik ürünü seçerken ihtiyaç ile istek arasındaki farkı açıklayabiliyor muyum?",
        "Kullanımın amaç, süre, sağlık, güvenlik, mahremiyet ve çevre etkilerini ayrı ayrı değerlendirdim mi?",
        "Kullandığım bilgi veya gözlemin denetlenebilir bir kanıt olduğunu gösterebiliyor muyum?",
        "Kanıtın söylediği ile benim yorumumu birbirinden ayırdım mı?",
        "Kişisel verileri ve başkalarının mahremiyetini korudum mu?",
        "Önerdiğim her kuralın gerekçesini yazdım mı?",
        "Oluşturduğum ürün uygulanabilir mi ve geri bildirimle düzeltilmiş mi?",
    ],
    "summary": (
        "Teknolojik ürünlerin bilinçli kullanımı; doğru amacı seçme, süreyi planlama, güvenlik ve mahremiyeti "
        "koruma, sağlık ve çevre etkilerini gözetme davranışlarının birlikte uygulanmasıdır. Sağlam bir karar, "
        "güvenilir kanıtı yorumdan ayırır ve kanıtın sınırını aşan genellemelerden kaçınır. Bilinçli kullanımı "
        "destekleyen ürün; hedef kitlesi belli, kuralları uygulanabilir, gerekçeleri açık ve geri bildirimle "
        "iyileştirilmiş bir afiş, plan ya da kontrol listesi olabilir."
    ),
    "figureNote": (
        "Yukarıdaki şemada bilinçli kullanım kararı; amaç belirleme, kanıt toplama, ölçütlerle değerlendirme ve "
        "uygulanabilir ürün oluşturma sırasıyla gösterir. Şema örnek bir süreci açıklar; herhangi bir sorunun "
        "doğru seçeneğini veya sonucunu göstermez."
    ),
}


def build_body(sections: dict[str, Any]) -> str:
    blocks = [
        ("NE ÖĞRENECEĞİM?", sections["whatIWillLearn"]),
        ("ÖN BİLGİLER", sections["priorKnowledge"]),
        ("TEMEL KAVRAMLAR", sections["keyConcepts"]),
        ("KANITA DAYALI ÇALIŞMA BASAMAKLARI", sections["steps"]),
        ("ÇÖZÜMLÜ ÖRNEKLER", "\n\n".join(sections["workedExamples"])),
        ("YAYGIN HATALAR", sections["commonMistakes"]),
        ("ÖZ KONTROL", "\n".join(f"- {item}" for item in sections["selfCheck"])),
        ("ÖZET", sections["summary"]),
        ("GÖRSEL NOTU", sections["figureNote"]),
    ]
    return "\n\n".join(f"{heading}\n{text}" for heading, text in blocks)


def main() -> int:
    rows = [json.loads(line) for line in TARGET.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    matches = [row for row in rows if row.get("id") == NOTE_ID]
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one {NOTE_ID}, found {len(matches)}")

    for index, row in enumerate(rows):
        if row.get("type") == "pack":
            updated = pending(row)
            updated["version"] = max(int(row.get("version") or 0), 3)
            updated["releaseNotes"] = (
                "SB.5.6.2 konu anlatımının karışmış bölüm alanları düzeltildi; soru kayıtları değiştirilmedi."
            )
            rows[index] = updated
        elif row.get("id") == NOTE_ID:
            updated = pending(row)
            updated["lessonSections"] = SECTIONS
            updated["body"] = build_body(SECTIONS)
            rows[index] = updated

    payload = "\n".join(
        json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows
    ) + "\n"
    TARGET.write_text(payload, encoding="utf-8", newline="\n")
    print(f"repaired {NOTE_ID}; pack version={rows[0].get('version')}; questions unchanged=500")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
