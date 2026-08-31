#!/usr/bin/env python3
"""Append Grade 7 batch 10: 44 English and 56 Mathematics questions."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

from author_grade6_fen_english_batch10 import make_record
from author_grade6_fen_batch07 import task
from author_grade6_mixed_batch03 import read_notes_only
from author_grade7_dkab_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade7_english_batches05_09 import make_item as english_item, record as english_record


ENGLISH_SOURCE = Path("turkiye/7-sinif/ingilizce/ingilizce-tum.jsonl")
MATH_SOURCE = Path("turkiye/7-sinif/matematik/matematik-tum.jsonl")
MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
ENGLISH_POSITIONS = set(range(1, 12)) | set(range(26, 41)) | set(range(61, 72)) | set(range(86, 93))


# Each pair is an independently worded, solved item for the corresponding note.
# prompt, correct, distractors, explanation
MATH_CASES: list[list[tuple[str, str, list[str], str]]] = [
    [("Bir istasyonda zemin kat 0, üçüncü bodrum -3 ile gösteriliyor. -3 hangi sayı kümesine kesinlikle aittir?", "Tam sayılar kümesine", ["Yalnız doğal sayılar kümesine", "İrrasyonel sayılar kümesine", "Pozitif sayılar kümesine"], "-3 negatif bir tam sayıdır; doğal veya pozitif değildir."),
     ("Bir ölçüm sonucu 7/4 litre olarak yazılıyor. Bu değer sayı doğrusu üzerinde hangi iki tam sayı arasındadır?", "1 ile 2 arasında", ["-2 ile -1 arasında", "0 ile 1 arasında", "2 ile 3 arasında"], "7/4=1,75 olduğundan 1 ile 2 arasındadır.")],
    [("5/8 kesrinin sonlu ondalık gösterimi hangisidir?", "0,625", ["0,58", "0,8", "0,0625"], "5'i 8'e bölmek 0,625 sonucunu verir."),
     ("0,3\u0305 gösterimindeki çizgi 3 rakamının tekrar ettiğini belirtiyor. Bu sayı hangi kesre eşittir?", "1/3", ["3/10", "3/100", "10/3"], "0,333... geometrik olarak 1/3'e eşittir.")],
    [("-2/3, -0,6 ve -3/4 sayıları küçükten büyüğe nasıl sıralanır?", "-3/4 < -2/3 < -0,6", ["-0,6 < -2/3 < -3/4", "-2/3 < -3/4 < -0,6", "-3/4 < -0,6 < -2/3"], "Ondalık karşılıklar -0,75, yaklaşık -0,667 ve -0,6'dır."),
     ("7/10, 2/3 ve 0,68 sayılarından en büyüğü hangisidir?", "7/10", ["2/3", "0,68", "Üçü eşittir"], "7/10=0,70; 2/3 yaklaşık 0,667 ve diğer sayı 0,68'dir.")],
    [("Bir depoda sabah 3/4 ton ürün vardı. 2/5 tonu satıldı. Kaç ton ürün kaldı?", "7/20 ton", ["1/20 ton", "5/9 ton", "23/20 ton"], "3/4-2/5=15/20-8/20=7/20'dir."),
     ("Bir yürüyüşçü parkurun önce 2/7'sini, sonra 3/14'ünü tamamlıyor. Toplam ne kadarını tamamlamıştır?", "1/2'sini", ["5/21'ini", "5/14'ünü", "1/7'sini"], "2/7+3/14=4/14+3/14=7/14=1/2'dir.")],
    [("A kutusunda 6, B kutusunda 18 bilye vardır. B'nin sayısı A'ya göre nasıl karşılaştırılır?", "B, A'nın 3 katıdır ve A'dan 12 fazladır.", ["B, A'nın 12 katıdır.", "B, A'dan 3 fazladır.", "A, B'nin 3 katıdır."], "Çarpımsal karşılaştırma 18/6=3, toplamsal fark 18-6=12'dir."),
     ("K kitaplığında 15, L kitaplığında 25 kitap vardır. İki karşılaştırmayı birlikte doğru veren ifade hangisidir?", "L, K'den 10 fazladır ve K'nin 5/3 katıdır.", ["L, K'den 5 fazladır ve 10 katıdır.", "K, L'den 10 fazladır.", "L, K'nin 3/5 katıdır."], "Fark 10, oran 25/15=5/3'tür.")],
    [("Bir tarifte 2 bardak pirince 3 bardak su kullanılıyor. Pirinç 6 bardağa çıkarılırsa aynı oran için kaç bardak su gerekir?", "9 bardak", ["6 bardak", "7 bardak", "12 bardak"], "Pirinç 3 katına çıkınca su da 3 katına, 9 bardağa çıkar."),
     ("Bir araç sabit hızla 4 saatte 280 km gidiyor. Aynı hızla 7 saatte kaç kilometre gider?", "490 km", ["400 km", "420 km", "560 km"], "Birim hız 70 km/sa, yedi saatte 490 km'dir.")],
    [("Doğru orantılı bir tabloda x=3 iken y=12'dir. x=8 iken y kaçtır?", "32", ["17", "24", "96"], "Orantı sabiti 12/3=4 olduğundan y=4x ve y=32'dir."),
     ("Bir grafikte doğru orantı doğrusu orijinden geçiyor ve (5,20) noktasını içeriyor. (9,y) noktası için y kaçtır?", "36", ["24", "40", "45"], "y/x=20/5=4 sabittir; y=4·9=36.")],
    [("3x+2x-4 ifadesinin sadeleşmiş biçimi hangisidir?", "5x eksi 4", ["5x artı 4", "6x eksi 4", "x eksi 4"], "Benzer terimlerin katsayıları 3+2=5 olarak toplanır."),
     ("2(a-3)+a ifadesi sadeleştirildiğinde ne olur?", "3a eksi 6", ["3a eksi 3", "2a eksi 6", "3a artı 6"], "Dağıtma ile 2a-6+a=3a-6 elde edilir.")],
    [("4x-7=21 denkleminin çözümü nedir?", "x=7", ["x=3,5", "x=14", "x=28"], "Her iki yana 7 eklenir ve 4'e bölünür: x=7."),
     ("Bir etkinlik bütçesi için 35+8n≤99 eşitsizliği kuruluyor. n en fazla kaç doğal sayı olabilir?", "8", ["7", "9", "16"], "8n≤64 olduğundan n≤8'dir.")],
    [("'İki tek sayının toplamı tektir.' iddiasını çürüten karşı örnek hangisidir?", "3+5=8", ["2+4=6", "3+4=7", "5+6=11"], "3 ve 5 tek olduğu hâlde toplamları 8 çifttir."),
     ("n çift ise n+6'nın çift olduğunu gösteren cebirsel ifade hangisidir?", "n=2k ise n+6=2(k+3)", ["n=2k ise n+6=2k+3", "n=k ise n+6=6k", "n=2k+1 ise n+6=2k+6"], "2(k+3) biçimi sonucun 2'nin katı olduğunu kanıtlar.")],
    [("Bir algoritma x sayısını 3 ile çarpıp 5 çıkarıyor. x=4 için çıktı nedir?", "7", ["9", "12", "17"], "3·4-5=12-5=7'dir."),
     ("Çıktısı 2x+1 olan algoritma 15 çıktısını verdiyse girdi kaçtır?", "7", ["6", "8", "14"], "2x+1=15 denkleminden x=7 bulunur.")],
    [("A(2,-1) noktası y eksenine göre yansıtılıyor. Görüntüsü hangisidir?", "A': x eksi 2, y eksi 1", ["A': x artı 2, y artı 1", "A': x eksi 2, y artı 1", "A': x artı 1, y eksi 2"], "y eksenine yansımada x işaret değiştirir, y aynı kalır."),
     ("B(-3,4) noktası x eksenine göre yansıtılıyor. Yeni koordinatlar nedir?", "B': x eksi 3, y eksi 4", ["B': x artı 3, y artı 4", "B': x artı 3, y eksi 4", "B': x eksi 4, y eksi 3"], "x eksenine yansımada y işaret değiştirir.")],
    [("P ve Q noktalarına eşit uzaklıktaki noktaların geometrik yeri nedir?", "PQ doğru parçasının orta dikmesi", ["P merkezli herhangi bir çember", "PQ doğrusuna paralel bir doğru", "Yalnız P noktası"], "Orta dikme üzerindeki her nokta P ve Q'ya eşit uzaklıktadır."),
     ("Bir açının iki kenarına eşit uzaklıktaki noktalar hangi doğru üzerinde bulunur?", "Açıortay üzerinde", ["Kenarortay üzerinde", "Açıya paralel bir doğru üzerinde", "Yalnız köşe noktasında"], "Açıortayın noktaları iki açı kenarına eşit uzaklıktadır.")],
    [("Eş küplerden yapılmış bir yapının üstten görünüşünde 4 dolu kare vardır. Bu bilgi tek başına küp sayısını belirler mi?", "Hayır; her karedeki yükseklikler bilinmelidir.", ["Evet; yapı kesin 4 küptür.", "Evet; yapı kesin 8 küptür.", "Hayır; üstten görünüş hiçbir bilgi vermez."], "Üst görünüş taban konumlarını gösterir, sütun yüksekliklerini göstermez."),
     ("Bir küp yapısının üç taban konumundaki yükseklikleri 2, 1 ve 4'tür. Toplam kaç küp vardır?", "7", ["3", "8", "12"], "Sütun yükseklikleri 2+1+4=7 küp verir.")],
    [("Yarıçapı 6 cm olan dairenin alanı π=3 alınırsa kaç cm²'dir?", "108 cm²", ["18 cm²", "36 cm²", "216 cm²"], "Alan πr²=3·36=108 cm²'dir."),
     ("Tabanları 8 cm ve 14 cm, yüksekliği 5 cm olan yamuğun alanı kaç cm²'dir?", "55 cm²", ["44 cm²", "70 cm²", "110 cm²"], "Alan (8+14)·5/2=55 cm²'dir.")],
    [("Ayrıtları 3 cm, 4 cm ve 5 cm olan dikdörtgenler prizmasının yüzey alanı kaç cm²'dir?", "94 cm²", ["47 cm²", "60 cm²", "120 cm²"], "2·(3·4+3·5+4·5)=94'tür."),
     ("Kare tabanlı bir prizmanın taban ayrıtı 4 cm, yüksekliği 7 cm'dir. Yüzey alanı kaç cm²'dir?", "144 cm²", ["112 cm²", "128 cm²", "196 cm²"], "İki taban 32, dört yan yüz 112; toplam 144 cm²'dir.")],
    [("Bir kutu 4×3×2 birim küple tamamen dolduruluyor. Kaç birim küp gerekir?", "24", ["9", "12", "18"], "Katman başına 12, iki katmanda 24 küp vardır."),
     ("Her katmanda 15 birim küp bulunan bir prizma 4 katmandan oluşuyor. Hacmi kaç birimküptür?", "60 birimküp", ["19 birimküp", "45 birimküp", "75 birimküp"], "15·4=60 birimküp elde edilir.")],
    [("Boyutları 2 cm, 6 cm ve 9 cm olan prizmanın hacmi kaç cm³'tür?", "108 cm³", ["17 cm³", "54 cm³", "216 cm³"], "Hacim 2·6·9=108 cm³'tür."),
     ("Hacmi 180 cm³, taban alanı 30 cm² olan prizmanın yüksekliği kaç cm'dir?", "6 cm", ["5 cm", "30 cm", "150 cm"], "V=taban alanı·yükseklik olduğundan 180/30=6 cm'dir.")],
    [("2,5 dm³ kaç cm³'tür?", "2500 cm³", ["25 cm³", "250 cm³", "25000 cm³"], "1 dm³=1000 cm³ olduğundan 2,5 dm³=2500 cm³'tür."),
     ("4800 mL kaç litredir?", "4,8 L", ["0,48 L", "48 L", "480 L"], "1000 mL=1 L olduğundan 4800 mL=4,8 L'dir.")],
    [("Kapalı bir akvaryum 50×30×40 cm boyutlarındadır. Cam alanı hesaplanırken hangi büyüklük kullanılmalıdır?", "Dikdörtgenler prizmasının yüzey alanı", ["Yalnız hacim", "Yalnız taban çevresi", "Boyutların toplamı"], "Cam gereksinimi altı yüzün alanlarının toplamıdır."),
     ("60×40×30 cm bir kutunun içine sığabilecek madde miktarı için hangi hesap yapılır?", "60·40·30 ile hacim", ["2·(60+40) ile çevre", "60·40 ile yalnız taban alanı", "60+40+30 ile ayrıt toplamı"], "Kapasite üç boyutun çarpımı olan hacimle belirlenir.")],
    [("Çapı 10 cm olan yuvarlak okul ambleminin kapladığı yüzey, π=3,14 alınarak hesaplanıyor. Sonuç ve gerekçesi hangisidir?", "78,5 cm²; çünkü yarıçap 5 cm alınır", ["31,4 cm²; çünkü çap doğrudan π ile çarpılır", "157 cm²; çünkü yarıçap yerine çap kullanılır", "314 cm²; çünkü çapın karesi kullanılır"], "Yarıçap 5 cm; alan 3,14·25=78,5 cm²'dir."),
     ("Alanı 154 cm² olan dairede π=22/7 alınırsa yarıçap kaç cm'dir?", "7 cm", ["5 cm", "11 cm", "14 cm"], "154=(22/7)r² eşitliğinden r²=49 ve r=7'dir.")],
    [("Yarıçapı 8 cm, merkez açısı 90° olan daire diliminin alanı π=3 alınırsa kaç cm²'dir?", "48 cm²", ["24 cm²", "96 cm²", "192 cm²"], "90° tam dairenin dörtte biridir; 3·64/4=48'dir."),
     ("Aynı dairede 60°'lik dilimin alanı 30 cm² ise 120°'lik dilimin alanı kaç cm²'dir?", "60 cm²", ["15 cm²", "30 cm²", "90 cm²"], "Merkez açı iki katına çıktığı için dilim alanı da iki katına çıkar.")],
    [("Köşegenleri 10 cm ve 14 cm olan eşkenar dörtgenin alanı kaç cm²'dir?", "70 cm²", ["24 cm²", "140 cm²", "280 cm²"], "Alan köşegenler çarpımının yarısıdır: 10·14/2=70."),
     ("Alanı 96 cm², yüksekliği 8 cm ve tabanlarından biri 10 cm olan yamuğun diğer tabanı kaç cm'dir?", "14 cm", ["2 cm", "12 cm", "24 cm"], "96=(10+b)·8/2 eşitliğinden 10+b=24, b=14 bulunur.")],
    [("Bir üçgende köşeden karşı kenarın orta noktasına çizilen doğru parçası nedir?", "Kenarortay", ["Yükseklik", "Açıortay", "Orta dikme"], "Kenarortay köşeyi karşı kenarın orta noktasıyla birleştirir."),
     ("Bir köşeden karşı kenara dik çizilen doğru parçası nedir?", "Yükseklik", ["Kenarortay", "Açıortay", "Kenar orta dikmesi"], "Yükseklik karşı kenara veya uzantısına diktir.")],
    [("AB kenarının orta dikmesi pergel-cetvelle çizildikten sonra C köşesi bu orta noktayla birleştiriliyor. Oluşan doğru parçası nedir?", "C köşesinden AB'ye ait kenarortay", ["C açısının dış açıortayı", "AB'ye paralel doğru", "Üçgenin çevrel çemberi"], "Orta dikme AB'nin orta noktasını verir; C ile bu noktanın birleşimi kenarortaydır."),
     ("Bir kenarortay inşasında ilk olarak karşı kenarın orta noktasını güvenilir biçimde bulmak için hangi çizim kullanılır?", "Karşı kenarın orta dikme inşası", ["Köşeden rastgele ışın", "Kenara paralel herhangi bir doğru", "Yalnız açı ölçümü"], "Orta dikme, kenarın iki ucuna eşit uzaklıktaki kesişimlerle orta noktayı belirler.")],
    [("'Okula geliş süresi ile kullanılan ulaşım türü ilişkili midir?' sorusu için hangi veri çifti gerekir?", "Her öğrencinin ulaşım türü ve geliş süresi", ["Yalnız öğrencilerin adları", "Sadece sınıfın duvar rengi", "Yalnız bir öğrencinin sevdiği ders"], "Araştırma sorusundaki kategorik ve nicel iki değişken birlikte toplanmalıdır."),
     ("Bir okul kantini araştırmasında tüm öğrenciler yerine yalnız spor kulübü üyeleri inceleniyor. Temsil sorunu nedir?", "Örneklem okulun bütün öğrencilerini temsil etmeyebilir.", ["Örneklem her zaman evrenden daha doğrudur.", "Kategorik veri toplanamaz.", "Üye sayısı bilinmese de kesin genelleme yapılır."], "Tek bir kulüp, okul nüfusunun tercihlerini yanlı temsil edebilir.")],
    [("İki sınıfın ortalama puanı 72'dir; A'da değerler 70–74, B'de 40–100 arasındadır. Hangi yorum doğrudur?", "Ortalamalar eşit olsa da B sınıfında değişkenlik daha büyüktür.", ["İki dağılım tamamen aynıdır.", "A sınıfında değişkenlik daha büyüktür.", "Aralık bilgisi karşılaştırmada kullanılamaz."], "B'nin değer aralığı çok daha geniştir."),
     ("Bir ankette 20 kişiden 14'ü parkı güvenli buluyor. 'Şehirde herkes parkı güvenli bulur.' sonucu neden zayıftır?", "Küçük örneklem ve kapsam, bütün şehre kesin genellemeyi desteklemez.", ["14 sayısı 20'den küçük olduğu için veri yoktur.", "Anketler hiçbir zaman bilgi vermez.", "Çoğunluk her zaman evrenin tamamı demektir."], "Sonuç örneklemin kimleri ve kaç kişiyi temsil ettiğiyle sınırlıdır.")],
    [("Bir olayın gerçekleşme olasılığı 0,35 ise tümleyeninin olasılığı kaçtır?", "0,65", ["0,35", "1,35", "0,75"], "Bir olay ile tümleyeninin olasılıkları toplamı 1'dir."),
     ("Yağmur yağmama olasılığı 3/5 ise yağmur yağma olasılığı nedir?", "2/5", ["3/5", "1/5", "8/5"], "Tümleyen olasılık 1-3/5=2/5'tir.")],
    [("Bir torbada 5 kırmızı, 3 mavi top vardır. Rastgele seçilen topun kırmızı olma olasılığı nedir?", "5/8", ["3/8", "1/2", "5/3"], "Sekiz eş olasılıklı topun beşi kırmızıdır."),
     ("1'den 10'a kadar numaralı eş kartlardan biri çekiliyor. Asal sayı gelme olasılığı nedir?", "2/5", ["1/5", "1/2", "3/5"], "Asal kartlar 2,3,5,7 olmak üzere 4 tanedir; 4/10=2/5.")],
    [("Bir zar atışında 'çift gelme' ile '4'ten büyük gelme' olayları ayrık mıdır?", "Hayır; 6 sonucu iki olayın ortak elemanıdır.", ["Evet; hiçbir ortak sonuç yoktur.", "Evet; yalnız 2 ortaktır.", "Hayır; bütün sonuçlar ortaktır."], "Çift sonuçlar {2,4,6}, 4'ten büyükler {5,6}; kesişim {6}'dır."),
     ("Bir kart 1–8 arasından seçiliyor. 'Tek gelme' ile 'çift gelme' olayları için doğru yorum hangisidir?", "Ayrıktırlar ve birlikte tüm örnek uzayı kapsarlar.", ["Ayrık değildirler; 3 ortaktır.", "İki olay da yalnız 8'i içerir.", "Birlikte hiçbir sonucu kapsamazlar."], "Bir sayı aynı anda tek ve çift olamaz; her sayı bu iki gruptan birindedir.")],
]


def math_item(note: dict[str, Any], note_index: int, variant: int, mode: str) -> dict[str, Any]:
    prompt, correct, wrongs, explanation = MATH_CASES[note_index][variant]
    if mode == "error-analysis":
        stem = f"Bir öğrenci “{wrongs[0]}” yanıtını veriyor. Aşağıdaki özgün problemde bu yanılgıyı düzelten seçenek hangisidir? {prompt}"
    elif mode == "analysis":
        stem = f"Verilenleri ve işlem ilişkisini birlikte çözümleyiniz: {prompt}"
    elif mode == "application":
        stem = f"Konu anlatımındaki bağıntıyı bu yeni duruma uygulayınız: {prompt}"
    else:
        stem = prompt
    return task(note["id"], mode, stem, correct, wrongs, explanation)


def math_record(local: int, item: dict[str, Any], note: dict[str, Any]) -> dict[str, Any]:
    row = make_record(local, item, note, batch=10, number_base=900)
    row["id"] = row["id"].replace("tr-g06-", "tr-g07-")
    row["questionId"] = row["id"]
    row["familyId"] = row["familyId"].replace("tr-g06-", "tr-g07-")
    row["authoringTemplateId"] = row["authoringTemplateId"].replace("g6-", "g7-")
    row["grade"] = 7
    row["title"] = f"{note['title']} — 10. özgün üretim partisi"
    explanation = str(item["explanation"]).rstrip(". ") + "."
    row["explanation"] = explanation + " Diğer seçenekler işlem sırasını, birimi, bağıntıyı veya veri sınırını yanlış uygular."
    reasons = {
        item["correct"]: f"Doğru çözüm: {explanation} Sonuç, problemde verilen bütün nicelik ve birimlerle denetlenmiştir.",
        item["wrongs"][0]: f"Adlandırılmış yanılgı — ilk işlem hatası: {item['wrongs'][0]} sonucu verilen bağıntıyı doğru uygulamaz.",
        item["wrongs"][1]: f"Adlandırılmış yanılgı — kavram karışıklığı: {item['wrongs'][1]} sonucu istenen büyüklüğü başka bir büyüklükle karıştırır.",
        item["wrongs"][2]: f"Adlandırılmış yanılgı — kanıt dışı sonuç: {item['wrongs'][2]} seçeneği problemdeki bütün koşulları birlikte sağlamaz.",
    }
    row["distractorWhy"] = [reasons[value] for value in row["choices"]]
    return row


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 900:
        raise RuntimeError(f"batch 10 expects 900 records, found {len(existing)}")
    english_notes = list(read_notes_only(ENGLISH_SOURCE).values())[116:160]
    math_notes = list(read_notes_only(MATH_SOURCE).values())
    math_assignments = [(i, 0) for i in range(30)] + [(i, 1) for i in range(26)]
    english_index = math_index = 0
    rows = []
    for local, mode in enumerate(MODES, 1):
        if local in ENGLISH_POSITIONS:
            note = english_notes[english_index]
            english_index += 1
            item = english_item(note, mode, 2)
            row = english_record(local, 10, item, note, 2)
        else:
            note_index, variant = math_assignments[math_index]
            math_index += 1
            note = math_notes[note_index]
            item = math_item(note, note_index, variant, mode)
            row = math_record(local, item, note)
        rows.append(row)
    if (english_index, math_index) != (44, 56):
        raise AssertionError((english_index, math_index))
    if Counter(row["correctIndex"] for row in rows) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer balance")
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + rows) + "\n", encoding="utf-8", newline="\n")
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"grade": 7, "batch": 10, "questions": 100, "english": 44, "mathematics": 56, "total": 1000, "sourceQuestionReads": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
