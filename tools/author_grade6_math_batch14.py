#!/usr/bin/env python3
"""Append 100 independently authored Grade 6 mathematics questions (batch 14)."""
from __future__ import annotations

from collections import Counter
import json
from typing import Any

from author_grade6_bilisim_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade6_english_batch11 import rows
from author_grade6_english_math_batch12 import MATH_SOURCE
from author_grade6_fen_batch07 import task
from author_grade6_fen_english_batch10 import make_record
from author_grade6_mixed_batch03 import read_notes_only


def vrows(note: str, values: list[tuple[str, str, str, str, str, str, str, str | None]]):
    return [task(note, mode, stem, correct, [w1, w2, w3], explanation, figure_kind=tag)
            for mode, stem, correct, w1, w2, w3, explanation, tag in values]


def angle_tasks():
    n = "tr-g06-matematik-note-015"
    return vrows(n, [
        ("comprehension", "Bir üçgenin iç açılarının ölçüleri toplamı kaç derecedir?", "180°", "90°", "270°", "360°", "Her üçgenin üç iç açısının toplamı 180°dir.", None),
        ("comprehension", "Bir paralelkenarın ardışık iki iç açısı arasında hangi ilişki vardır?", "Toplamları 180°dir.", "Her zaman eşittirler.", "Toplamları 90°dir.", "Aralarında sabit bir ilişki yoktur.", "Paralel kenarları kesen yan kenar nedeniyle ardışık açılar bütünlerdir.", None),
        ("application", "Bir üçgenin iki iç açısı 58° ve 73° olduğuna göre üçüncü iç açı kaç derecedir?", "49°", "131°", "59°", "229°", "180−58−73=49 bulunur.", "triangle"),
        ("application", "Bir paralelkenarın dar açısı 64° ise geniş açısı kaç derecedir?", "116°", "64°", "128°", "296°", "Ardışık açılar bütünlerdir; 180−64=116 olur.", "parallelogram"),
        ("application", "Bir üçgenin dış açısı 137°, komşu olmayan iç açılarından biri 61°dir. Diğer uzak iç açı kaç derecedir?", "76°", "198°", "104°", "43°", "Dış açı iki uzak iç açının toplamıdır; 137−61=76 olur.", "triangle"),
        ("analysis", "Bir eşkenar dörtgende ardışık açılar 2x ve 4x derecedir. Büyük açı kaç derecedir?", "120°", "60°", "90°", "240°", "2x+4x=180, x=30 ve 4x=120 olur.", "parallelogram"),
        ("analysis", "ABCD yamuğunda AB // CD, ∠A=74° ve ∠B=98°dir. ∠C ile ∠D sırasıyla kaç derecedir?", "82° ve 106°", "106° ve 82°", "74° ve 98°", "98° ve 74°", "Aynı yan kenardaki açılar bütünlerdir: C=180−98=82, D=180−74=106.", "trapezoid"),
        ("error-analysis", "Bir öğrenci “Bir dörtgenin iç açıları toplamı 180°dir.” diyor. Hangi düzeltme doğrudur?", "Bir köşegen dörtgeni iki üçgene ayırır; toplam 360°dir.", "Dörtgenin toplamı köşe sayısından bağımsızdır.", "Yalnız karede toplam 180°dir.", "Dörtgenin iç açı toplamı 540°dir.", "İki üçgenin açı toplamları 180+180=360° verir.", None),
        ("error-analysis", "Bir öğrenci “Eşkenar dörtgenin bütün açıları eşittir çünkü bütün kenarları eşittir.” diyor. Hangi değerlendirme doğrudur?", "Karşılıklı açılar eşittir; dört açının da eşit olması yalnız kare özel durumunda gerçekleşir.", "Kenar eşitliği bütün açıları 60° yapar.", "Eşkenar dörtgende karşılıklı açılar farklıdır.", "Bu şeklin iç açısı yoktur.", "Eş kenarlar tek başına dört dik açı gerektirmez.", "parallelogram"),
    ])


def unit_tasks():
    n = "tr-g06-matematik-note-016"
    return vrows(n, [
        ("comprehension", "Alan birimleri dönüştürülürken neden uzunluk birimlerinden farklı bir çarpan kullanılır?", "Alan iki boyutlu olduğu için dönüşüm çarpanı karesine alınır.", "Alan birimsiz olduğu için", "Bütün alan birimleri eşit olduğu için", "Yalnız çevre ölçüldüğü için", "1 m=100 cm iken 1 m²=100² cm²dir.", None),
        ("comprehension", "1 m² kaç cm²dir?", "10 000 cm²", "100 cm²", "1000 cm²", "1 000 000 cm²", "Bir metrenin iki kenarı da 100 cm olduğundan 100×100=10 000 cm²dir.", "unit-table"),
        ("comprehension", "Bir tarla alanı için en uygun birim hangisidir?", "metrekare", "milimetre", "santimetre", "litre", "Tarla yüzeyi iki boyutlu ve büyükçe olduğundan metrekare uygundur.", None),
        ("comprehension", "1 hektar ile 1 metrekare arasındaki ilişki hangisidir?", "1 ha = 10 000 m²", "1 ha = 100 m²", "1 ha = 1000 m²", "1 ha = 100 000 m²", "Hektar, kenarı 100 m olan karenin alanıdır.", "unit-table"),
        ("application", "Mozaik ustası 2,4 m²lik panoyu santimetrekare cinsinden sipariş formuna yazacaktır. Forma hangi değeri girmelidir?", "24 000 cm²", "240 cm²", "2400 cm²", "240 000 cm²", "Bir metrekare 10 000 santimetrekare olduğundan pano alanı 2,4×10 000=24 000 cm²dir.", None),
        ("application", "36 000 cm² kaç m²dir?", "3,6 m²", "36 m²", "0,36 m²", "360 m²", "Santimetrekareden metrekareye geçerken 10 000'e bölünür.", None),
        ("application", "0,75 hektarlık bahçenin alanı kaç metrekaredir?", "7500 m²", "750 m²", "75 000 m²", "75 m²", "0,75×10 000=7500 m²dir.", "unit-table"),
        ("application", "Kenarları 80 cm ve 1,5 m olan dikdörtgen masanın alanı kaç cm²dir?", "12 000 cm²", "120 cm²", "1200 cm²", "120 000 cm²", "1,5 m=150 cm; 80×150=12 000 cm² olur.", None),
        ("application", "4 km² kaç m²dir?", "4 000 000 m²", "4000 m²", "40 000 m²", "400 000 m²", "1 km²=1 000 000 m² olduğundan sonuç 4 000 000 m²dir.", "unit-table"),
        ("analysis", "A alanı 1,2 m², B alanı 11 500 cm²dir. Hangisi daha büyüktür ve fark kaç cm²dir?", "A, 500 cm² daha büyüktür.", "B, 500 cm² daha büyüktür.", "A, 6500 cm² daha büyüktür.", "İki alan eşittir.", "1,2 m²=12 000 cm²; fark 500 cm²dir.", None),
        ("analysis", "6000 m², 0,55 ha ve 58 000 000 cm² alanlarını büyükten küçüğe sıralayan seçenek hangisidir?", "6000 m² > 58 000 000 cm² > 0,55 ha", "0,55 ha > 6000 m² > 58 000 000 cm²", "58 000 000 cm² > 0,55 ha > 6000 m²", "Üçü eşittir.", "Değerler m² ile 6000, 5800 ve 5500'dür.", None),
        ("analysis", "Bir kare planın alanı 2 500 cm²dir. Kenar uzunluğu metre cinsinden kaçtır?", "0,5 m", "5 m", "0,25 m", "25 m", "Karenin kenarı √2500=50 cm=0,5 m'dir.", None),
        ("analysis", "Bir ölçüm kaydı 3 m² 4500 cm² biçimindedir. Tek birimle toplam alan kaç m²dir?", "3,45 m²", "7,5 m²", "3,045 m²", "345 m²", "4500 cm²=0,45 m²; toplam 3,45 m²dir.", None),
        ("error-analysis", "Bir öğrenci “1 m²=100 cm²dir; çünkü 1 m=100 cm.” diyor. Hangi düzeltme gerekir?", "İki boyut da dönüştürülür; 1 m²=100×100=10 000 cm²dir.", "Yalnız bir kenar dönüştürülmelidir.", "1 m²=10 cm²dir.", "Metrekare ile santimetrekare karşılaştırılamaz.", "Alan dönüşümünde doğrusal çarpanın karesi kullanılır.", None),
        ("error-analysis", "Bir öğrenci “25 000 cm²yi m²ye çevirirken 100'e bölerim.” diyor. Doğru sonuç ve işlem hangisidir?", "10 000'e bölünür ve 2,5 m² bulunur.", "100'e bölünür ve 250 m² bulunur.", "10'a bölünür ve 2500 m² bulunur.", "10 000 ile çarpılır ve 250 000 000 m² bulunur.", "1 m²=10 000 cm² ilişkisi bölme çarpanını belirler.", None),
    ])


def area_relation_tasks():
    n = "tr-g06-matematik-note-017"
    return vrows(n, [
        ("comprehension", "Paralelkenarın alan bağıntısı hangisidir?", "taban × o tabana ait yükseklik", "iki kenarın toplamı", "taban × yükseklik ÷ 2", "dört kenarın çarpımı", "Paralelkenar kesilip taşındığında aynı taban ve yükseklikte dikdörtgen oluşturur.", None),
        ("comprehension", "Üçgenin alanında neden taban ile yüksekliğin çarpısı ikiye bölünür?", "Aynı taban ve yükseklikte iki eş üçgen bir paralelkenar oluşturabilir.", "Üçgenin iki kenarı olduğu için", "Yükseklik her zaman yarım olduğu için", "Çevre alanın iki katı olduğu için", "Üçgen, karşılık gelen paralelkenarın yarı alanına sahiptir.", "triangle-area"),
        ("comprehension", "Bir yüksekliğin tabana göre temel özelliği nedir?", "Tabana dik olması", "Tabana paralel olması", "Tabanla aynı uzunlukta olması", "Üçgenin dışında olamaması", "Yükseklik, köşeden taban doğrusuna indirilen dik uzaklıktır.", None),
        ("application", "Tabanı 14 cm, bu tabana ait yüksekliği 9 cm olan paralelkenarın alanı kaç cm²dir?", "126 cm²", "46 cm²", "63 cm²", "252 cm²", "14×9=126 cm²dir.", "parallelogram-area"),
        ("application", "Bir parkta tabanı 18 m olan üçgen gölgelik, tabana dik 7 m yüksekliğe sahiptir. Kapladığı yüzey kaç m²dir?", "63 m²", "126 m²", "25 m²", "252 m²", "Aynı taban ve yükseklikteki paralelkenarın alanı 126 m² olur; üçgen bunun yarısını kapladığı için 63 m² elde edilir.", "triangle-area"),
        ("application", "Alanı 96 cm², tabanı 12 cm olan paralelkenarın yüksekliği kaç santimetredir?", "8 cm", "4 cm", "12 cm", "84 cm", "96÷12=8 cm olur.", None),
        ("application", "Alanı 60 dm² ve yüksekliği 10 dm olan üçgenin tabanı kaç desimetredir?", "12 dm", "6 dm", "30 dm", "120 dm", "60=taban×10÷2 olduğundan taban=12 dm'dir.", None),
        ("analysis", "Aynı tabana ve aynı yüksekliğe sahip bir paralelkenarla üçgenin alanları nasıl ilişkilidir?", "Paralelkenarın alanı üçgenin alanının iki katıdır.", "Alanları eşittir.", "Üçgenin alanı iki katıdır.", "Çevre bilinmeden karşılaştırılamaz.", "b×h ile b×h÷2 karşılaştırıldığında oran 2'dir.", "triangle-area"),
        ("analysis", "Bir paralelkenarın tabanı iki katına çıkarılıp aynı tabana ait yüksekliği yarıya indirilirse alan nasıl değişir?", "Değişmez.", "İki katına çıkar.", "Yarıya iner.", "Dört katına çıkar.", "(2b)×(h/2)=b×h olur.", None),
        ("analysis", "Alanları eşit iki üçgenden A'nın tabanı 10 cm, yüksekliği 12 cm; B'nin tabanı 15 cm'dir. B'nin yüksekliği kaç cm'dir?", "8 cm", "6 cm", "10 cm", "18 cm", "A alanı 60 cm²dir; 15×h÷2=60 olduğundan h=8.", "triangle-area"),
        ("error-analysis", "Bir öğrenci “Paralelkenarın eğik kenarı 11 cm olduğu için yüksekliği de 11 cm alırım.” diyor. Hangi düzeltme doğrudur?", "Yükseklik tabana dik uzaklıktır; eğik kenar ancak dikse yükseklik olabilir.", "Her kenar otomatik olarak yüksekliktir.", "Alan için yalnız çevre gerekir.", "Yükseklik tabana paralel olmalıdır.", "Kenar uzunluğu ile dik uzaklık farklı büyüklüklerdir.", "parallelogram-area"),
        ("error-analysis", "Bir öğrenci “Tabanı 16 cm, yüksekliği 5 cm olan üçgenin alanı 80 cm²dir.” diyor. Hangi düzeltme gerekir?", "Taban-yükseklik çarpısı ikiye bölünür; alan 40 cm²dir.", "16 ile 5 toplanır ve 21 cm² bulunur.", "Alan 160 cm²dir.", "Yalnız taban kullanılır ve 16 cm² bulunur.", "Üçgen, aynı taban ve yükseklikteki paralelkenarın yarısıdır.", None),
    ])


def area_problem_tasks():
    n = "tr-g06-matematik-note-018"
    return vrows(n, [
        ("comprehension", "Bir alan probleminde işlemlere başlamadan önce hangi kontrol önceliklidir?", "Bütün uzunlukların aynı birimde olup olmadığı", "Şeklin renginin ne olduğu", "Çevrenin mutlaka alanla eşit olduğu", "Her ölçünün toplanması gerektiği", "Alan bağıntısı ortak uzunluk birimiyle uygulanmalıdır.", None),
        ("comprehension", "Bileşik bir bölgenin alanını bulmak için geçerli strateji hangisidir?", "Bölgeyi alanı bilinen şekillere ayırıp uygun biçimde toplamak veya çıkarmak", "Bütün kenarları gelişigüzel çarpmak", "Yalnız dış çevreyi hesaplamak", "Şeklin köşe sayısını ikiyle çarpmak", "Ayrıştırma, karmaşık alanı temel şekillere indirger.", None),
        ("application", "12 m × 8 m dikdörtgen bahçenin içine tabanı 6 m, yüksekliği 4 m olan üçgen çiçeklik yapılıyor. Geriye kaç m² kalır?", "84 m²", "72 m²", "90 m²", "108 m²", "Bahçe 96, üçgen 12 m²dir; 96−12=84.", "composite-area"),
        ("application", "Tabanı 9 m, yüksekliği 6 m olan paralelkenar biçimli zemine m² başına 3 karo kutusu gerekiyor. Kaç kutu gerekir?", "162", "54", "108", "324", "Alan 9×6=54 m²; 54×3=162 kutu gerekir.", None),
        ("application", "Bir üçgen pankartın tabanı 2,4 m, yüksekliği 150 cm'dir. Alanı kaç m²dir?", "1,8 m²", "180 m²", "3,6 m²", "0,18 m²", "150 cm=1,5 m; 2,4×1,5÷2=1,8 m².", "triangle-area"),
        ("application", "Alanı 72 m² olan paralelkenar arsada taban 12 m'dir. Aynı yüksekliğe sahip üçgen bölümün tabanı 8 m ise alanı kaç m²dir?", "24 m²", "36 m²", "48 m²", "96 m²", "Yükseklik 72÷12=6 m; üçgen alanı 8×6÷2=24 m².", None),
        ("analysis", "İki duvarın alanları eşittir. A duvarı 10 m×3 m dikdörtgen, B duvarı tabanı 12 m olan paralelkenardır. B'nin yüksekliği kaç metredir?", "2,5 m", "3 m", "4 m", "5 m", "A'nın alanı 30 m²; 30÷12=2,5 m olur.", None),
        ("analysis", "20 m×15 m dikdörtgen parktan, tabanı 10 m yüksekliği 8 m olan iki eş üçgen çıkarılıyor. Kalan alan kaç m²dir?", "220 m²", "260 m²", "140 m²", "180 m²", "Park 300; her üçgen 40, ikisi 80; kalan 220 m²dir.", "composite-area"),
        ("error-analysis", "Bir öğrenci “2 m ile 60 cm'yi doğrudan çarpıp 120 m² buldum.” diyor. Hangi düzeltme doğrudur?", "60 cm=0,6 m yapılmalı; dikdörtgen alanı 1,2 m²dir.", "120 sayısına yalnız cm² yazılmalıdır.", "2+60=62 m² alınmalıdır.", "Birimler alan hesabını etkilemez.", "Uzunluklar ortak birime çevrilmeden çarpılamaz.", None),
        ("error-analysis", "Bir öğrenci “Dikdörtgen alandan üçgen boşluk çıkarırken üçgen için taban×yükseklik kullandım.” diyor. Hangi düzeltme gerekir?", "Üçgen alanı taban×yükseklik÷2 ile bulunmalıdır.", "Üçgenin alanı yalnız tabandır.", "Boşluk alanı eklenmelidir.", "Dikdörtgen alanı da ikiye bölünmelidir.", "Üçgen, eş taban ve yükseklikteki paralelkenarın yarısıdır.", None),
    ])


def circumference_relation_tasks():
    n = "tr-g06-matematik-note-019"
    return vrows(n, [
        ("comprehension", "Bir çemberde çap ile yarıçap arasındaki ilişki hangisidir?", "Çap yarıçapın iki katıdır.", "Yarıçap çapın iki katıdır.", "Çap ile yarıçapın toplamı sıfırdır.", "Aralarında sabit ilişki yoktur.", "Çap merkezden geçerek iki yarıçapı uç uca birleştirir.", "circle"),
        ("comprehension", "Pi sayısı çemberde hangi oranın sabit değeridir?", "Çevre uzunluğunun çap uzunluğuna oranı", "Çapın yarıçapa oranı", "Alanın çevreye oranı", "Yayın merkez açıya oranı", "C/d oranı bütün çemberlerde π'ye eşittir.", "circle"),
        ("comprehension", "Çember uzunluğu için doğru bağıntı hangisidir?", "C = πd", "C = d/π", "C = π+r", "C = 2d", "Çevrenin çapa oranı π olduğundan C=πd'dir.", None),
        ("comprehension", "Aynı çember için 2πr ve πd ifadeleri neden eşittir?", "d=2r olduğu için", "π=2 olduğu için", "r=d olduğu için", "Çevre yarıçaptan bağımsız olduğu için", "πd=π(2r)=2πr olur.", None),
        ("comprehension", "Pi sayısını deneysel tahmin etmek için hangi ölçümler gerekir?", "Aynı dairesel nesnenin çevresi ve çapı", "Yalnız yarıçapı", "Karenin çevresi ve alanı", "İki farklı doğrunun eğimi", "Çevre çapa bölünerek π için yaklaşık değer elde edilir.", "measure-table"),
        ("application", "Çapı 14 cm olan çemberin uzunluğu π=22/7 alınırsa kaç cm'dir?", "44 cm", "22 cm", "88 cm", "154 cm", "C=πd=(22/7)×14=44 cm.", "circle"),
        ("application", "Bir seramik tabağın merkezinden kenarına uzaklık 8 cm ölçülüyor. Kenarına çekilecek ince şeridin uzunluğu π=3,14 ile kaç cm olur?", "50,24 cm", "25,12 cm", "100,48 cm", "11,14 cm", "Ölçülen 8 cm yarıçaptır. Tam kenar şeridi iki yarıçaplı çapa göre 3,14×16=50,24 cm uzunluğundadır.", None),
        ("application", "Çevresi 62,8 cm olan çemberin çapı π=3,14 ile kaç cm'dir?", "20 cm", "10 cm", "31,4 cm", "197,192 cm", "d=C/π=62,8/3,14=20 cm.", None),
        ("application", "Bir tekerleğin çapı 70 cm'dir. π=22/7 ile bir tam turda aldığı yol kaç santimetredir?", "220 cm", "110 cm", "440 cm", "1540 cm", "Bir turdaki yol çevreye eşittir: (22/7)×70=220 cm.", "circle"),
        ("application", "Çapı 1,2 m olan yuvarlak masanın kenarına şerit çekilecektir. π=3 alınırsa en az kaç metre şerit gerekir?", "3,6 m", "1,8 m", "4,2 m", "7,2 m", "C=πd=3×1,2=3,6 m.", None),
        ("application", "Yarıçapı 21 m olan dairesel pistin çevresi π=22/7 ile kaç metredir?", "132 m", "66 m", "462 m", "84 m", "C=2×(22/7)×21=132 m.", None),
        ("application", "Çevresi 31,4 m olan dairesel havuzun yarıçapı π=3,14 ile kaç metredir?", "5 m", "10 m", "15,7 m", "2,5 m", "r=C/(2π)=31,4/6,28=5 m.", None),
        ("analysis", "A çemberinin çapı B'ninkinin 3 katıdır. Çevre uzunlukları nasıl ilişkilidir?", "A'nın çevresi B'nin çevresinin 3 katıdır.", "Çevreleri eşittir.", "A'nın çevresi 9 katıdır.", "B'nin çevresi 3 katıdır.", "C=πd doğrusal orantı verdiği için çap oranı çevreye aynen taşınır.", "circle"),
        ("analysis", "Ölçüm tablosunda çevre/çap oranları 3,12; 3,15; 3,14 çıkıyor. En uygun yorum hangisidir?", "Ölçüm hataları olsa da oranlar π'nin yaklaşık sabit değerinin çevresinde toplanmıştır.", "Pi her nesnede bütünüyle farklıdır.", "Çap çevreden büyüktür.", "Yalnız 3,12 doğru olabilir.", "Yakın oranlar sabit ilişkiyi, küçük farklar ölçüm belirsizliğini gösterir.", "measure-table"),
        ("analysis", "Çevreleri 94,2 cm ve 62,8 cm olan iki çember için π=3,14 alınırsa çap farkı kaç cm'dir?", "10 cm", "31,4 cm", "20 cm", "5 cm", "Çaplar 30 ve 20 cm; fark 10 cm'dir.", None),
        ("analysis", "Bir tekerlek 4400 cm yol alırken 20 tam tur atıyor. π=22/7 ise çapı kaç cm'dir?", "70 cm", "35 cm", "140 cm", "220 cm", "Bir tur 4400/20=220 cm; d=220÷(22/7)=70 cm.", None),
        ("analysis", "Yarıçapı %25 artırılan bir çemberin çevresi nasıl değişir?", "%25 artar.", "%50 artar.", "%56,25 artar.", "Değişmez.", "C=2πr olduğundan çevre yarıçapla aynı oranda değişir.", None),
        ("error-analysis", "Bir öğrenci “Çapı 10 cm olan çemberin uzunluğu 2π×10'dur.” diyor. Hangi düzeltme doğrudur?", "10 çap olduğundan C=π×10 kullanılmalıdır.", "Çap önce karesi alınmalıdır.", "Çevre yalnız 2×10'dur.", "Pi kullanılmaz.", "2πr bağıntısındaki 10 yarıçap değil çaptır.", None),
        ("error-analysis", "Bir öğrenci “Çevreyi çapa böldüğümde her zaman tam 3 çıkar.” diyor. Hangi değerlendirme doğrudur?", "Oran π'dir; 3 yaklaşık alınabilir ama daha duyarlı ölçümlerde 3,14'e yaklaşır.", "Oran her zaman 2'dir.", "Pi yalnız karelerde kullanılır.", "Çevre çap oranı nesneye göre rastgele değişir.", "π irrasyoneldir ve hesapta seçilen yaklaşıma göre temsil edilir.", "measure-table"),
        ("error-analysis", "Bir öğrenci “Tekerlek iki tur atınca yalnız bir çevre kadar yol gider.” diyor. Hangi düzeltme gerekir?", "Alınan yol tur sayısı×çevredir; iki turda iki çevre kadar yol alınır.", "Tur sayısı çevreyi yarıya indirir.", "Yol çap×yarıçaptır.", "Tekerlek dönünce ilerlemez.", "Kaymadan dönmede her tam tur bir çevre uzunluğu kadar ilerletir.", None),
    ])


def circumference_problem_tasks():
    n = "tr-g06-matematik-note-020"
    return vrows(n, [
        ("comprehension", "Çember uzunluğu probleminde çap verilmişse en kısa doğrudan işlem hangisidir?", "Çapı π ile çarpmak", "Çapı ikiye bölüp işlemi bitirmek", "Çapın karesini almak", "Çapa π eklemek", "C=πd bağıntısı çapı doğrudan kullanır.", None),
        ("comprehension", "Dairesel bir pistte tur sayısı ve toplam yol ilişkisi hangisidir?", "Toplam yol = tur sayısı × pist çevresi", "Toplam yol = çevre ÷ tur sayısı", "Toplam yol = çap + tur sayısı", "Toplam yol yarıçapa eşittir", "Her tam tur bir çevre uzunluğu kadar yol verir.", None),
        ("application", "Yarıçapı 14 m olan dairesel parkın çevresine üç sıra tel çekiliyor. π=22/7 ile kaç metre tel gerekir?", "264 m", "88 m", "132 m", "616 m", "Bir sıra 88 m; üç sıra 264 m'dir.", "circle"),
        ("application", "Çapı 50 cm olan bisiklet tekerleği 30 tam tur atıyor. π=3,14 ile kaç metre yol alır?", "47,1 m", "4,71 m", "471 m", "15,7 m", "Çevre 157 cm; 30 tur 4710 cm=47,1 m.", "circle"),
        ("analysis", "Aynı 314 m yolu çapı 1 m ve 2 m olan iki tekerlek alıyor. π=3,14 ile tur sayıları nasıl karşılaştırılır?", "Küçük tekerlek 100, büyük tekerlek 50 tur atar.", "İkisi 100 tur atar.", "Küçük 50, büyük 100 tur atar.", "İkisi 314 tur atar.", "Çevreler 3,14 ve 6,28 m olduğundan tur sayıları 100 ve 50'dir.", None),
        ("analysis", "Bir çemberin çevresine 5 m aralıklarla 44 direk, boşluk kalmadan yerleştiriliyor. π=22/7 ise çap kaç metredir?", "70 m", "35 m", "140 m", "220 m", "Çevre 44×5=220 m; çap 220÷(22/7)=70 m.", None),
        ("error-analysis", "Bir öğrenci “Çapı 28 m olan pistte 4 tur için π×28÷4 yaparım.” diyor. Hangi düzeltme doğrudur?", "Bir turun çevresi π×28, dört turun yolu bunun 4 katıdır.", "Tur arttıkça toplam yol bölünür.", "Çap yerine alan kullanılmalıdır.", "Dört tur her zaman 28 m'dir.", "Toplam yol tur sayısıyla doğru orantılıdır.", None),
    ])


def arc_tasks():
    n = "tr-g06-matematik-note-021"
    return vrows(n, [
        ("comprehension", "Bir çemberde 90°lik merkez açının gördüğü yay, çevrenin hangi bölümüdür?", "Dörtte biri", "Yarısı", "Üçte biri", "Tamamı", "90/360=1/4'tür.", "arc"),
        ("application", "Çevresi 72 cm olan çemberde 120°lik merkez açının gördüğü yay kaç cm'dir?", "24 cm", "12 cm", "36 cm", "48 cm", "120/360=1/3; 72÷3=24 cm.", "arc"),
        ("application", "Yarıçapı 7 cm olan çemberde 180°lik yayın uzunluğu π=22/7 ile kaç cm'dir?", "22 cm", "44 cm", "11 cm", "154 cm", "Tam çevre 44 cm, 180°lik yay bunun yarısı 22 cm'dir.", "arc"),
        ("analysis", "Aynı çemberde A yayı 60°, B yayı 150° merkez açı görüyor. B yayının uzunluğu A'nın kaç katıdır?", "2,5 katı", "1,5 katı", "3 katı", "90 katı", "Aynı çevrede yay uzunluklarının oranı merkez açıların oranıdır: 150/60=2,5.", "arc"),
        ("analysis", "Çevresi 96 cm olan çemberde bir yay 20 cm'dir. Bu yayı gören merkez açı kaç derecedir?", "75°", "60°", "80°", "120°", "20/96=θ/360; θ=75° bulunur.", None),
        ("error-analysis", "Bir öğrenci “Merkez açısı 45° olan yayın uzunluğu çevrenin 45'te biridir.” diyor. Hangi düzeltme gerekir?", "Pay 45, bütün 360 alınır; yay çevrenin 45/360=1/8'idir.", "Yay çevrenin 45 katıdır.", "Her yay çevrenin yarısıdır.", "Merkez açı yayla ilişkili değildir.", "Oran merkez açının tam açıya, yani 360°ye oranıdır.", None),
    ])


def statistics_tasks():
    n = "tr-g06-matematik-note-022"
    return vrows(n, [
        ("comprehension", "'Öğrencilerin okula geliş biçimi' değişkeni hangi veri türündedir?", "Kategorik", "Nicel kesikli", "Sürekli ölçüm", "Oran", "Cevaplar servis, yürüyüş gibi kategori adlarıdır.", None),
        ("comprehension", "'Bir haftada okunan kitap sayısı' hangi veri türündedir?", "Nicel kesikli", "Kategorik", "Sürekli nicel", "Metinsel olmayan veri değildir", "Kitap adedi saymayla 0,1,2 gibi değerler alır.", None),
        ("comprehension", "Ortanca bulunmadan önce hangi işlem yapılmalıdır?", "Veriler büyüklük sırasına konmalıdır.", "En büyük değer silinmelidir.", "Bütün değerler ikiyle çarpılmalıdır.", "Kategori adları toplanmalıdır.", "Ortanca sıralı listenin orta konumuna dayanır.", None),
        ("comprehension", "Tepe değer neyi gösterir?", "En sık görülen değeri veya kategoriyi", "En büyük sayıyı", "Bütün değerlerin toplamını", "Dağılımın açıklığını", "Tepe değer sıklığı en yüksek gözlemdir.", None),
        ("comprehension", "Tarafsız bir araştırma sorusunun özelliği hangisidir?", "Beklenen cevabı ima etmeden değişkeni açıkça sorması", "Katılımcıyı belirli seçeneğe yönlendirmesi", "İki farklı özelliği tek cevapta istemesi", "Zaman aralığını gizlemesi", "Tarafsız soru, cevaplayanın seçimini yönlendirmez.", None),
        ("application", "Veri seti 3, 4, 4, 6, 8 için aritmetik ortalama kaçtır?", "5", "4", "6", "25", "Toplam 25, veri sayısı 5; 25÷5=5.", "data-table"),
        ("application", "Veriler 2, 5, 5, 7, 9, 12 biçimindedir. Ortanca kaçtır?", "6", "5", "7", "6,5", "Çift sayıda veride ortadaki 5 ve 7'nin ortalaması 6'dır.", "data-table"),
        ("application", "Kulüp tercihleri Robotik 9, Spor 7, Müzik 4, Resim 6'dır. Tepe kategori hangisidir?", "Robotik", "Spor", "Müzik", "Resim", "En yüksek sıklık 9 ile Robotiktir.", "bar-chart"),
        ("application", "Bir sınıfta günlük çözülen soru sayıları 10, 12, 12, 14, 17'dir. Açıklık kaçtır?", "7", "12", "27", "5", "Açıklık en büyük−en küçük=17−10=7.", "data-table"),
        ("application", "Bir okul iki sınıfın haftalık okuma sürelerini karşılaştırmak istiyor. En uygun araştırma sorusu hangisidir?", "6-A ve 6-B öğrencilerinin son yedi gündeki okuma süreleri nasıl farklılaşır?", "Kitap okumak çok yararlı değil mi?", "Okulumuzdaki en iyi sınıf hangisidir?", "Öğrenciler ne düşünür?", "İki grup, ortak süre ve ölçülen değişken açıkça belirtilmiştir.", None),
        ("application", "Kategorik sıklıkları karşılaştırmak için uygun gösterim hangisidir?", "Sütun grafiği", "Yalnız sayı doğrusu", "Açıölçer", "Cebirsel eşitlik", "Sütun yükseklikleri kategorilerin sıklıklarını karşılaştırır.", "bar-chart"),
        ("application", "Son yedi günde spor yapılan gün sayısını toplamak için en açık soru hangisidir?", "Son yedi günde en az 20 dakika spor yaptığın kaç gün oldu?", "Çok spor yapıyor musun?", "Spor iyi midir ve hangi takımı seversin?", "Geçmişte hiç hareket ettin mi?", "Zaman, ölçüt ve sayılacak birim açıkça verilmiştir.", None),
        ("application", "5, 6, 6, 7, 16 verisinde tipik değeri uç değerden daha az etkilenen ölçü hangisidir?", "Ortanca 6", "Aritmetik ortalama 8", "Açıklık 11", "En büyük değer 16", "Ortanca sıralamadaki merkezdir ve 16'dan ortalamaya göre daha az etkilenir.", "data-table"),
        ("analysis", "A ve B gruplarının ortalaması 10'dur. A'nın açıklığı 2, B'nin açıklığı 12'dir. Hangi yorum desteklenir?", "Merkezleri eşit olsa da B grubunun değişebilirliği daha fazladır.", "Dağılımları kesinlikle aynıdır.", "A grubunun ortalaması daha büyüktür.", "Açıklık merkez ölçüsüdür.", "Eş ortalama, yayılımın da eşit olmasını gerektirmez.", "data-table"),
        ("analysis", "Bir ankette yalnız robotik kulübündeki 12 öğrenciye 'en sevdiğin kulüp' soruluyor. Sonuç bütün okul için neden zayıftır?", "Seçilen grup hedef topluluğu temsil etmeyebilir.", "12 bir sayı olduğu için kategorik veri toplanamaz.", "Kulüp adı hiçbir zaman sorulamaz.", "Her örneklem bütün okulu kesin temsil eder.", "Tek kulüpten seçim, tercih dağılımını robotik lehine yanlılaştırabilir.", None),
        ("analysis", "Grafikte Pazartesi 18, Salı 24, Çarşamba 21, Perşembe 27 katılım vardır. En az 25 koşulunu hangi gün sağlar?", "Yalnız Perşembe", "Salı ve Perşembe", "Pazartesi ve Çarşamba", "Dört günün tamamı", "Değerler ayrı karşılaştırılır; yalnız 27 en az 25'tir.", "bar-chart"),
        ("analysis", "2, 3, 3, 4, 20 verisi için hangi değerlendirme en uygundur?", "20 ortalamayı yükseltir; ortanca ve tepe değer 3'tür.", "Bütün merkez ölçüleri 20'dir.", "20 kanıtsız biçimde silinmelidir.", "Ortanca 4, tepe değer yoktur.", "Sıralı merkez 3, en sık değer 3; uç değer ortalamayı etkiler.", "data-table"),
        ("analysis", "Bir grafikte sütunlar 3 boyutlu çizildiği için 8 değeri 6'nın iki katı gibi görünüyor. Hangi iyileştirme gerekir?", "Eksen ölçeği açık, iki boyutlu ve ortak tabanlı sütunlar kullanılmalıdır.", "Değer etiketleri kaldırılmalıdır.", "Sütun genişlikleri rastgele değiştirilmelidir.", "Grafik yalnız resimle süslenmelidir.", "Ortak ölçek ve 2B gösterim görsel yanıltmayı azaltır.", "bar-chart"),
        ("error-analysis", "Bir öğrenci “Meyve türlerinin aritmetik ortalamasını bulacağım.” diyor. Hangi düzeltme doğrudur?", "Kategori adlarının ortalaması alınmaz; sıklıklar sayılıp tepe kategori belirlenebilir.", "Meyve adları harf sayılarına göre toplanır.", "Her kategoriye rastgele sayı verilir.", "Kategorik veri analiz edilemez.", "Aritmetik ortalama nicel değerlere uygulanır, adlara değil.", None),
        ("error-analysis", "Bir öğrenci “Altı veride ortanca soldan üçüncü değerdir.” diyor. Hangi düzeltme gerekir?", "Sıralı altı veride üçüncü ve dördüncü değerlerin ortalaması alınır.", "Her zaman ilk değer seçilir.", "En büyük iki değer toplanır.", "Ortanca yalnız tek sayıda veride vardır.", "Çift veri sayısında iki merkez konum birlikte kullanılır.", None),
    ])


def bias_intro_task():
    return rows("tr-g06-matematik-note-023", [
        ("comprehension", "Bir istatistiksel yorumda yalnız sonucu destekleyen verileri seçip diğerlerini gizlemek hangi soruna yol açar?", "Yanlı bir sonuca", "Daha temsil edici bir örnekleme", "Kesin bir nedensellik kanıtına", "Ölçüm birimlerinin eşitlenmesine", "Seçici raporlama dağılımın bütününü çarpıtır."),
    ])


TASK_BUILDERS = [angle_tasks, unit_tasks, area_relation_tasks, area_problem_tasks,
                 circumference_relation_tasks, circumference_problem_tasks, arc_tasks,
                 statistics_tasks, bias_intro_task]


def _label(labels: dict[str, str], qid: str, suffix: str, value: str) -> str:
    key = f"figure.{qid}.{suffix}"
    labels[key] = value
    return key


def diagram_figure(qid: str, labels: dict[str, str], tag: str) -> dict[str, Any]:
    alt = _label(labels, qid, "alt", "Soruda kullanılan ölçü ve ilişkileri gösteren, ölçek dışı ve cevabı açıklamayan matematik şeması.")
    if tag in {"circle", "arc"}:
        o = _label(labels, qid, "o", "O")
        a = _label(labels, qid, "a", "A")
        b = _label(labels, qid, "b", "B")
        elements = [
            {"type": "circle", "style": "plain", "x": 50, "y": 30, "r": 23, "stroke": "blue", "fill": "surface"},
            {"type": "line", "style": "plain", "x1": 50, "y1": 30, "x2": 73, "y2": 30, "stroke": "ink"},
            {"type": "line", "style": "plain", "x1": 50, "y1": 30, "x2": 50, "y2": 7, "stroke": "ink"},
            {"type": "circle", "style": "plain", "x": 50, "y": 30, "r": 1.5, "fill": "accent", "labelKey": o},
            {"type": "circle", "style": "plain", "x": 73, "y": 30, "r": 1.5, "fill": "accent", "labelKey": a},
            {"type": "circle", "style": "plain", "x": 50, "y": 7, "r": 1.5, "fill": "accent", "labelKey": b},
        ]
    elif tag in {"triangle", "triangle-area"}:
        a = _label(labels, qid, "a", "A")
        b = _label(labels, qid, "b", "B")
        c = _label(labels, qid, "c", "C")
        h = _label(labels, qid, "h", "h")
        elements = [
            {"type": "polygon", "style": "plain", "points": [[15, 50], [82, 50], [58, 8]], "stroke": "blue", "fill": "surface"},
            {"type": "line", "style": "plain", "x1": 58, "y1": 8, "x2": 58, "y2": 50, "stroke": "muted", "labelKey": h},
            {"type": "circle", "style": "plain", "x": 15, "y": 50, "r": 1.5, "fill": "accent", "labelKey": a},
            {"type": "circle", "style": "plain", "x": 82, "y": 50, "r": 1.5, "fill": "accent", "labelKey": b},
            {"type": "circle", "style": "plain", "x": 58, "y": 8, "r": 1.5, "fill": "accent", "labelKey": c},
        ]
    else:
        names = {x: _label(labels, qid, x.lower(), x) for x in "ABCD"}
        points = [[18, 48], [35, 10], [82, 10], [67, 48]]
        elements = [{"type": "polygon", "style": "plain", "points": points, "stroke": "blue", "fill": "surface"}]
        for (x, y), name in zip(points, "ABCD"):
            elements.append({"type": "circle", "style": "plain", "x": x, "y": y, "r": 1.5, "fill": "accent", "labelKey": names[name]})
    return {"kind": "diagram", "viewBox": [0, 0, 100, 60], "elements": elements,
            "altTextKey": alt, "notToScale": True}


def tabular_figure(qid: str, labels: dict[str, str], tag: str) -> dict[str, Any]:
    alt = _label(labels, qid, "alt", "Soruda karşılaştırılan değerleri açık satır ve sütunlarla gösteren veri tablosu; doğru seçenek belirtilmemiştir.")
    h1 = _label(labels, qid, "h1", "Kayıt")
    h2 = _label(labels, qid, "h2", "Değer")
    local = int(qid.rsplit("q", 1)[1])
    if tag == "bar-chart":
        cats = ["Pzt", "Sal", "Çar", "Per"]
        values = [18, 24, 21, 27]
        category_keys = [_label(labels, qid, f"c{i}", value) for i, value in enumerate(cats)]
        x = _label(labels, qid, "x", "Kategori")
        y = _label(labels, qid, "y", "Sıklık")
        return {"kind": "chart", "style": "bar", "categoryKeys": category_keys,
                "values": values, "axisKeys": {"x": x, "y": y}, "altTextKey": alt}
    data_rows = {
        85: ["Gözlemler", "3, 4, 4, 6, 8"],
        86: ["Sıralı gözlemler", "2, 5, 5, 7, 9, 12"],
        88: ["Günlük soru sayıları", "10, 12, 12, 14, 17"],
        90: ["Okunan kitap sayıları", "5, 6, 6, 7, 16"],
        93: ["Açıklıklar", "A: 2, B: 12"],
    }
    values = (data_rows.get(local) or (["1 m²", "10 000 cm²"] if tag == "unit-table" else
              ["Çevre / çap", "π'ye yakın"] if tag == "measure-table" else
              ["Sıralı veri", "Merkez ve yayılım"]))
    return {"kind": "table", "headerKeys": [h1, h2],
            "rows": [[{"v": values[0]}, {"v": values[1]}]], "altTextKey": alt}


def apply_visual(row: dict[str, Any], item: dict[str, Any], labels: dict[str, str]) -> None:
    tag = item.get("figure_kind")
    if not tag:
        return
    qid = str(row["id"])
    local = int(qid.rsplit("q", 1)[1])
    allowed = {3, 4, 5, 6, 7, 9, 26, 28, 29, 32, 34, 35, 39, 41, 44,
               47, 48, 51, 52, 55, 59, 65, 69, 70, 74, 75, 76, 77,
               85, 86, 88, 90, 93, 96}
    if local not in allowed:
        return
    if tag in {"unit-table", "measure-table", "data-table", "bar-chart"}:
        figure = tabular_figure(qid, labels, str(tag))
    else:
        figure = diagram_figure(qid, labels, str(tag))
    row["figure"] = figure
    visual_word = "grafiği" if figure["kind"] == "chart" else "tabloyu" if figure["kind"] == "table" else "şemayı"
    row["question"] = f"Aşağıdaki {visual_word} inceleyiniz. {row['question']}"
    row["visualRequirement"] = "required"
    row["visualNeed"] = {"level": "required", "role": "evidence",
                         "rationale": "Soru verisinin uzamsal veya nicel ilişkisi yapılandırılmış görsel üzerinden denetlenir.",
                         "acceptableKinds": [figure["kind"]],
                         "evidenceDimensions": ["ölçü veya veri", "ilişki veya karşılaştırma"]}


def verify_math_facts() -> None:
    assert 180 - 58 - 73 == 49 and 180 - 64 == 116 and 137 - 61 == 76
    assert 4 * 30 == 120 and 180 - 98 == 82 and 180 - 74 == 106
    assert 2.4 * 10000 == 24000 and 36000 / 10000 == 3.6 and .75 * 10000 == 7500
    assert 80 * 150 == 12000 and 4 * 1000000 == 4000000
    assert 12000 - 11500 == 500 and [6000, 58000000 / 10000, .55 * 10000] == [6000, 5800, 5500]
    assert 14 * 9 == 126 and 18 * 7 / 2 == 63 and 60 * 2 / 10 == 12
    assert 12 * 8 - 6 * 4 / 2 == 84 and 9 * 6 * 3 == 162 and abs(2.4 * 1.5 / 2 - 1.8) < 1e-12
    assert (22 / 7) * 14 == 44 and 2 * 3.14 * 8 == 50.24 and 62.8 / 3.14 == 20
    assert (22 / 7) * 70 == 220 and 2 * (22 / 7) * 21 == 132 and 31.4 / 6.28 == 5
    assert 4400 / 20 / (22 / 7) == 70 and 3 * 2 * (22 / 7) * 14 == 264
    assert 30 * 3.14 * 50 / 100 == 47.1 and 44 * 5 / (22 / 7) == 70
    assert 72 * 120 / 360 == 24 and 2 * (22 / 7) * 7 / 2 == 22 and 96 * 75 / 360 == 20
    assert sum([3, 4, 4, 6, 8]) / 5 == 5 and (5 + 7) / 2 == 6 and 17 - 10 == 7


def main() -> int:
    verify_math_facts()
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1300:
        raise RuntimeError("validated first thirteen batches must exist before batch 14")
    notes = read_notes_only(MATH_SOURCE)
    tasks = [item for builder in TASK_BUILDERS for item in builder()]
    if len(tasks) != 100:
        raise AssertionError(f"batch 14 must contain 100 tasks, got {len(tasks)}")
    expected_modes = {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
    if Counter(item["mode"] for item in tasks) != expected_modes:
        raise AssertionError(Counter(item["mode"] for item in tasks))
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    rows_out = []
    for local, item in enumerate(tasks, 1):
        row = make_record(local, item, notes[item["note"]], batch=14, number_base=1300)
        apply_visual(row, item, labels)
        rows_out.append(row)
    if Counter(row["correctIndex"] for row in rows_out) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer positions are not exactly balanced")
    if sum(bool(row.get("figure")) for row in rows_out) != 34:
        raise AssertionError("batch 14 must contain exactly 34 required figures")
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":"))
                                 for row in existing + rows_out) + "\n", encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
    print(json.dumps({"batch": 14, "questions": 100, "mathematics": 100, "figures": 34,
                      "total": 1400, "modes": dict(Counter(item["mode"] for item in tasks)),
                      "sourceQuestionReads": 0, "figureSpec": "1.3.0"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
