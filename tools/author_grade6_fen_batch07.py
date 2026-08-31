#!/usr/bin/env python3
"""Append 100 independently authored Grade 6 science questions (batch 07).

This batch completes the remaining quotas of objectives FB.6.1.1.1 through
FB.6.3.1.3 and adds two questions for FB.6.3.1.4.  Every task is authored from
the lesson-note concepts; lesson-package questions are never read.
"""
from __future__ import annotations

from collections import Counter
import json
from typing import Any

from author_grade6_bilisim_batch01 import LABELS_OUTPUT, OUTPUT, rotate
from author_grade6_mixed_batch03 import LEVEL_SEQUENCE, read_notes_only
from author_grade6_mixed_batch06 import FEN_SOURCE, _eclipse_figure, _prism_figure, _ray_figure


Task = dict[str, Any]


def task(note: str, mode: str, stem: str, correct: str, wrongs: list[str], explanation: str,
         *, figure_kind: str | None = None, figure_data: Any = None) -> Task:
    if len(wrongs) != 3 or len({correct, *wrongs}) != 4:
        raise ValueError(f"invalid choices for {note}: {stem[:50]}")
    return {
        "note": note, "mode": mode, "stem": stem, "correct": correct,
        "wrongs": wrongs, "explanation": explanation,
        "figure_kind": figure_kind, "figure_data": figure_data,
    }


def planet_tasks() -> list[Task]:
    n = "tr-g06-fen-bilimleri-note-001"
    return [
        task(n, "comprehension", "Merkür, Venüs, Dünya ve Mars'ın ortak yapısal özelliği hangisidir?",
             "Katı yüzeyli karasal gezegenler olmaları",
             ["Halkalarının belirgin olması", "Asteroit kuşağının dışında bulunmaları", "Tamamının çok sayıda uyduya sahip olması"],
             "İlk dört gezegen küçük ve kayalık yapıdadır; halka ve uydu sayısı bu grubun ortak ölçütü değildir."),
        task(n, "application", "Bir öğrenci gezegenleri asteroit kuşağına göre iki gruba ayıracaktır. Jüpiter hangi gruba yazılmalıdır?",
             "Asteroit kuşağının dışındaki dış gezegenler grubuna",
             ["Güneş ile asteroit kuşağı arasındaki iç gezegenler grubuna", "Karasal gezegenler grubuna", "Doğal uydusu olmayan gezegenler grubuna"],
             "Jüpiter asteroit kuşağının ötesindedir ve dış gezegenler arasında sınıflandırılır."),
        task(n, "analysis", "Bir katalogda K gezegeni 'kayalık, küçük ve Güneş'e yakın'; L gezegeni 'kalın gaz katmanlı, büyük ve halkalı' olarak tanıtılıyor. En uygun sınıflandırma hangisidir?",
             "K karasal-iç, L gazsal-dış gezegendir.",
             ["K gazsal-dış, L karasal-iç gezegendir.", "İkisi de yalnız halka durumuna göre karasal gezegendir.", "Güneş'e yakınlık yapısal sınıflandırmada hiçbir bilgi vermez."],
             "Kayalık ve yakın K iç-karasal; büyük, gaz katmanlı ve halkalı L dış-gazsal özellikler taşır."),
        task(n, "error-analysis", "Bir öğrenci 'Halkası bulunan her gezegen Güneş'e en yakın dört gezegenden biridir.' diyor. Bu yanılgıyı düzelten ifade hangisidir?",
             "Belirgin halkalar dış gezegenlerde görülür; Güneş'e en yakın dört gezegen karasaldır.",
             ["Halka durumu ile gezegen sınıflandırması arasında hiçbir ilişki yoktur.", "Yalnız Dünya'nın halkası vardır.", "Asteroit kuşağının içindeki bütün gezegenler gazsaldır."],
             "Halka özelliği yakınlıkla ters eşleştirilmiştir; belirgin halka sistemleri dış gezegenlerin özelliğidir."),
        task(n, "comprehension", "Güneş'e uzaklık sırası verilirken Dünya'nın iki komşusu hangi seçenekte doğru gösterilmiştir?",
             "Venüs – Dünya – Mars",
             ["Merkür – Dünya – Venüs", "Mars – Dünya – Jüpiter", "Venüs – Dünya – Jüpiter"],
             "Dünya Güneş'e yakınlıkta üçüncüdür; ikinci Venüs, dördüncü Mars'tır."),
        task(n, "application", "Bir sınıflandırma anahtarı önce 'katı yüzey var mı?', sonra 'asteroit kuşağının içinde mi?' sorularını soruyor. Dünya hangi yolu izler?",
             "Katı yüzey: evet; asteroit kuşağının içi: evet",
             ["Katı yüzey: hayır; asteroit kuşağının içi: evet", "Katı yüzey: evet; asteroit kuşağının içi: hayır", "Katı yüzey: hayır; asteroit kuşağının içi: hayır"],
             "Dünya karasal bir iç gezegendir; iki ölçüte de 'evet' yanıtı verir."),
        task(n, "analysis", "Uranüs ve Neptün aynı gruba alınırken yalnız renkleri değil, sistemdeki konum ve genel yapıları kullanılacaktır. Hangi gerekçe uygundur?",
             "İkisi de asteroit kuşağının dışında bulunan büyük dış gezegenlerdir.",
             ["İkisi de Güneş'e en yakın karasal gezegenlerdir.", "İkisinin de doğal uydusu bulunmaz.", "Renk benzerliği bilimsel sınıflandırma için tek başına yeterlidir."],
             "Bilimsel gruplama, yüzeydeki renk yerine yapısal özellik ve Güneş Sistemi'ndeki konuma dayanır."),
        task(n, "error-analysis", "Bir öğrenci “Gezegenleri yalnız adlarının ilk harfine göre gruplandırmak bilimsel bir sınıflandırmadır.” diyor. Hangi düzeltme yapılmalıdır?",
             "Halka, uydu, yapı ve Güneş'e göre konum gibi anlamlı nitelikler ölçüt seçilmelidir.",
             ["Gezegen adlarının uzunluğu tek ölçüt yapılmalıdır.", "Bütün gezegenler hiçbir ölçüt kullanmadan aynı gruba yazılmalıdır.", "Yalnız modelde kullanılan boya rengi ölçüt alınmalıdır."],
             "Sınıflandırma, incelenen varlıkların bilimsel olarak anlamlı benzerlik ve farklılıklarını kullanır."),
    ]


def model_tasks() -> list[Task]:
    n = "tr-g06-fen-bilimleri-note-002"
    return [
        task(n, "comprehension", "Bir Güneş Sistemi modelinin bilimsel sayılmasını sağlayan temel özellik hangisidir?",
             "Seçilen sistem ilişkilerini açık ve tutarlı biçimde temsil etmesi",
             ["En pahalı malzemelerle yapılması", "Bütün gezegenlerin aynı renge boyanması", "Gerçek sistemin eksiksiz bir kopyası olması"],
             "Model, amaca göre seçilen özellikleri temsil eder; maliyet veya süsleme bilimsellik ölçütü değildir."),
        task(n, "application", "Gezegen sırasını öğretmek isteyen bir modelde ilk olarak hangi özellik doğrulanmalıdır?",
             "Gezegenlerin Güneş'ten uzaklaşma sırasının doğru olması",
             ["Kürelerin sınıftaki masaya sığması", "Bütün yörüngelerin aynı uzunlukta çizilmesi", "Gezegen adlarının alfabetik dizilmesi"],
             "Modelin amacı sıra öğretmekse öncelikli doğruluk ölçütü Güneş'e göre sıralamadır."),
        task(n, "application", "Model A gezegen sırasını, Model B yalnız göreli büyüklükleri doğru gösteriyor. 'Hangi gezegen Dünya'dan sonra gelir?' sorusu için hangisi kullanılmalıdır?",
             "Model A; çünkü soru konum sırasını gerektirir.",
             ["Model B; çünkü büyüklük her soruyu yanıtlar.", "İki model de kullanılamaz; model gerçeğin aynısı olmalıdır.", "Model B; çünkü büyük küreler Güneş'e daha yakındır."],
             "Model seçimi sorunun gerektirdiği özelliğe göre yapılır; bu soruda sıra bilgisi gerekir."),
        task(n, "error-analysis", "Bir öğrenci 'Modelde bütün uzaklıklar eşitse gerçek Güneş Sistemi'nde de eşittir.' sonucuna ulaşıyor. Doğru düzeltme hangisidir?",
             "Model ölçeksiz olabilir; eşit çizilen aralıklar gerçek uzaklıkların eşit olduğunu kanıtlamaz.",
             ["Her model gerçek uzaklıkları zorunlu olarak bire bir verir.", "Uzaklık bir modelde hiç gösterilemez.", "Gezegenlerin sırası uzaklıkla ilişkisizdir."],
             "Modelin temsil sınırı belirtilmeden çizim aralığı gerçek ölçü gibi yorumlanamaz."),
        task(n, "application", "Bir öğrenci hem gezegen büyüklüklerini hem uzaklıkları tek masa üzerinde aynı ölçekle göstermek istiyor. En bilimsel karar hangisidir?",
             "İki ayrı ölçek kullanıp her birini model üzerinde açıkça belirtmek",
             ["Uzaklıkları rastgele kısaltıp ölçek kullandığını söylememek", "Bütün gezegenleri eşit yapmak", "Modelin başlığını değiştirerek ölçek sorununu çözmek"],
             "Çok farklı büyüklük ve uzaklıklar tek küçük alana aynı ölçekle sığmayabilir; ayrı ölçekler dürüstçe belirtilir."),
        task(n, "analysis", "Yeni gözlem, bir gök cisminin yörüngesinin modeldekinden farklı olduğunu gösteriyor. Bilimsel süreç hangi davranışı gerektirir?",
             "Modeli yeni kanıtla uyumlu olacak biçimde gözden geçirmek",
             ["Kanıtı model bozulmasın diye yok saymak", "Modeli hiç değiştirmeden kesin gerçek ilan etmek", "Yalnız modelin rengini değiştirmek"],
             "Bilimsel modeller yeni ve güvenilir kanıtlar elde edildiğinde geliştirilebilir."),
        task(n, "comprehension", "Bir modelin altında 'Boyutlar ölçekli, uzaklıklar ölçeksizdir.' açıklaması bulunuyor. Bu notun işlevi nedir?",
             "Modelin hangi yönünün gerçeğe oranlı olduğunu ve sınırını belirtmek",
             ["Modeldeki bütün bilgilerin yanlış olduğunu göstermek", "Gezegen adlarını gizlemek", "Uzaklıkların gerçekte eşit olduğunu bildirmek"],
             "Ölçek notu, temsil edilen ve edilmeyen özellikleri kullanıcıya açıklar."),
        task(n, "application", "Dönme ve dolanma hareketlerini gösterecek bir model geliştiriliyor. Hangi ekleme amaca doğrudan hizmet eder?",
             "Dönme eksenlerini ve dolanma yönlerini ayırt eden oklar",
             ["Kürelerin altına fiyat etiketi", "Gezegenleri alfabetik sıraya dizme", "Bütün yörüngeleri kaldırma"],
             "Hareket modeli, eksen ve yön bilgisini görünür kılmalıdır."),
        task(n, "application", "Bir grup üç maketi bilimsel doğruluk bakımından karşılaştıracaktır. Hangi değerlendirme ölçütünü kullanmalıdır?",
             "Model doğruluğu fiziksel büyüklükle değil, amaçlanan ilişkileri doğru temsil etmesiyle değerlendirilir.",
             ["Büyük modeller hiçbir bilimsel bilgi gösteremez.", "Yalnız küçük modeller ölçek kullanabilir.", "Model seçiminde amaç ve kanıt dikkate alınmamalıdır."],
             "Maketi büyütmek temsil edilen ilişkinin doğruluğunu kendiliğinden artırmaz."),
        task(n, "analysis", "İki modelden biri gezegen sırasını doğru ama renkleri hayalî; diğeri renkleri gerçekçi fakat sırası yanlış gösteriyor. Sıra kazanımı için hangisi daha uygundur?",
             "Sırası doğru olan model; hayalî renklerin temsil sınırı ayrıca açıklanmalıdır.",
             ["Sırası yanlış olan model; renk her ölçütten önemlidir.", "İkisi eşittir; sıra doğruluğu değerlendirilmez.", "Hiçbiri; bilimsel modeller sınırlılık içeremez."],
             "Amaç sıra ilişkisini öğrenmek olduğundan bu ilişki doğru olmalı, diğer sınırlılıklar açıkça belirtilmelidir."),
        task(n, "comprehension", "Bilimsel model ile gerçek sistem arasındaki ilişkiyi en doğru açıklayan ifade hangisidir?",
             "Model, gerçeğin seçilmiş özelliklerini anlamayı kolaylaştıran bir temsildir.",
             ["Model, gerçek sistemin bütün ayrıntılarını zorunlu olarak taşır.", "Model yalnız süsleme amacıyla yapılır.", "Modelde gösterilmeyen özellik gerçekte de yoktur."],
             "Model gerçeğin kendisi değil, belirli amaçla sadeleştirilmiş temsilidir."),
        task(n, "application", "Asteroit kuşağını da göstermek isteyen öğrenci modelini nasıl geliştirmelidir?",
             "Kuşağı Mars ile Jüpiter yörüngeleri arasına, açıklayıcı bir anahtarla eklemelidir.",
             ["Kuşağı Dünya ile Ay arasına yerleştirmelidir.", "Kuşağı Güneş'in içine çizmelidir.", "Gezegen sırasını bozup kuşağı en dışa eklemelidir."],
             "Ana asteroit kuşağı Mars ile Jüpiter arasındadır; modelde konum ve açıklama birlikte doğru olmalıdır."),
        task(n, "analysis", "Bir model yalnız Güneş ve sekiz gezegeni içeriyor. Kuyruklu yıldızların hareketini araştırmak için kullanıldığında hangi değerlendirme yapılır?",
             "Model bu araştırma için eksiktir; kuyruklu yıldızın yörünge bilgisi eklenmelidir.",
             ["Model her araştırmayı eksiksiz yanıtlar.", "Kuyruklu yıldızlar modelle gösterilemez.", "Gezegenlerden birinin adı değiştirilirse eksik giderilir."],
             "Bir modelin yeterliliği kullanım amacına bağlıdır; araştırılan öğe ve ilişkisi modelde bulunmalıdır."),
    ]


def eclipse_inference_tasks() -> list[Task]:
    n = "tr-g06-fen-bilimleri-note-003"
    return [
        task(n, "comprehension", "Aşağıdaki şemada gök cisimlerinin konumu verilmiştir. Hangi olay ve gerekçe şemayla uyumludur?",
             "Güneş tutulması; Ay, Güneş ile Dünya arasındadır.",
             ["Ay tutulması; Güneş, Dünya ile Ay arasındadır.", "Güneş tutulması; Dünya, Güneş ile Ay arasındadır.", "Ay tutulması; Ay'ın gölgesi Güneş'e düşer."],
             "Güneş-Ay-Dünya dizilişinde Ay'ın gölgesi Dünya'nın sınırlı bir bölümüne ulaşabilir.", figure_kind="solar"),
        task(n, "comprehension", "Aşağıdaki şemadaki diziliş için doğru çıkarım hangisidir?",
             "Ay tutulması gerçekleşebilir; Dünya'nın gölgesi Ay'a yönelir.",
             ["Güneş tutulması gerçekleşir; Ay'ın gölgesi Dünya'ya yönelir.", "Dünya tutulması gerçekleşir; Güneş gölgede kalır.", "Tutulma türü gök cisimlerinin sırasından bağımsızdır."],
             "Güneş-Dünya-Ay dizilişi Ay tutulmasının temel konum ilişkisidir.", figure_kind="lunar"),
        task(n, "comprehension", "Güneş tutulmasının Dünya'nın her yerinden aynı anda izlenememesinin temel nedeni hangisidir?",
             "Ay'ın gölgesinin Dünya üzerinde sınırlı bir bölgeye düşmesi",
             ["Dünya'nın Güneş ışığını hiç almaması", "Ay'ın kendi ışığını yalnız bazı ülkelere göndermesi", "Güneş tutulmasının yalnız gece gerçekleşmesi"],
             "Ay gölgesi Dünya yüzeyinin dar bir bölümünü örter; gözlem yeri bu nedenle önemlidir."),
        task(n, "comprehension", "Ay tutulması sırasında Ay'ın kararmasını açıklayan olay hangisidir?",
             "Ay'ın Dünya'nın gölge bölgesine girmesi",
             ["Ay'ın Güneş ile Dünya arasına girmesi", "Güneş'in ışık üretmeyi bırakması", "Ay'ın Dünya'dan bütünüyle uzaklaşması"],
             "Dünya Güneş ışığının Ay'a ulaşmasını bir süre engeller."),
        task(n, "application", "Bir gözlem kaydında gündüz Güneş'in küçük bir bölümü kısa süre görünmüyor. En uygun bilimsel yorum hangisidir?",
             "Gözlem yeri Güneş tutulmasının kısmi gölge alanında olabilir.",
             ["Bu kayıt kesinlikle Ay tutulmasını gösterir.", "Güneş kalıcı olarak ışık üretmeyi bırakmıştır.", "Dünya, Ay ile Güneş arasına girmiştir."],
             "Gündüz Güneş diskinin kısa süreli örtülmesi Güneş tutulmasıyla uyumludur; tek kayıt tutulmanın her yerde olduğunu göstermez."),
        task(n, "analysis", "İki gözlemci aynı anda farklı şehirlerdedir. Biri Güneş'in tümünü, diğeri yalnız bir bölümünü örtülü görüyor. Hangi çıkarım desteklenir?",
             "Gözlemciler Ay gölgesinin farklı bölgelerinde bulunmaktadır.",
             ["Ay tutulması iki şehirde farklı renkte gerçekleşmektedir.", "Güneş'in büyüklüğü şehirden şehre değişmektedir.", "Tutulma sırasında Ay'ın yörüngesi ortadan kalkmaktadır."],
             "Tam ve kısmi örtülme, gölgenin merkez ve çevre bölgelerinden gözlem yapılmasıyla açıklanır."),
        task(n, "error-analysis", "Bir öğrenci 'Her yeni ay evresinde mutlaka Güneş tutulması olur.' diyor. Hangi düzeltme doğrudur?",
             "Ay'ın yörünge düzlemi eğik olduğundan her yeni ayda üç cisim tam hizalanmaz.",
             ["Tutulma için Ay evresinin ve konumun hiçbir önemi yoktur.", "Güneş tutulması yalnız dolunayda olur.", "Her yeni ayda tutulma olur fakat Dünya'dan hiçbir zaman görülemez."],
             "Ay'ın yörünge düzlemi her ay Güneş-Dünya doğrultusuyla uygun biçimde kesişmediği için tutulma oluşmaz."),
        task(n, "application", "Güneş-Ay-Dünya sırasını gösteren bir çizime doğru olay etiketi eklenecektir. Hangi etiket seçilmelidir?",
             "Güneş tutulması olarak değiştirilmelidir.",
             ["Dünya tutulması olarak değiştirilmelidir.", "Etiket doğru bırakılmalıdır.", "Tutulma değil, Ay'ın evresi olarak yazılmalıdır."],
             "Ay, Güneş ile Dünya arasındaysa Ay gölgesi Dünya'ya yönelir ve Güneş tutulması modeli oluşur."),
        task(n, "application", "Ay tutulmasını gözlemek isteyen bir öğrenci hangi zaman ve yön bilgisini kullanmalıdır?",
             "Gece, Ay'ın gökyüzünde bulunduğu sırada gözlem yapmalıdır.",
             ["Öğle vakti Güneş'e çıplak gözle bakmalıdır.", "Ay gökyüzünde değilken yalnız yere bakmalıdır.", "Güneş tutulmasının dar gölge yolunu izlemelidir."],
             "Ay tutulması Ay'ın gözlenebildiği gece tarafında izlenir; Güneş'e bakmayı gerektirmez."),
        task(n, "application", "Güneş tutulmasını güvenli biçimde incelemek için hangi davranış uygundur?",
             "Onaylı Güneş gözlem filtresi kullanmak veya dolaylı izdüşüm yöntemi uygulamak",
             ["Güneş'e çıplak gözle uzun süre bakmak", "Sıradan güneş gözlüğünü tek başına yeterli saymak", "Teleskoba filtresiz bakmak"],
             "Yoğun Güneş ışığı göze zarar verebilir; yalnız uygun filtre veya dolaylı yöntem kullanılmalıdır."),
        task(n, "analysis", "Bir kayıtta Dünya'nın gece tarafındaki birçok bölgede Ay'ın karardığı belirtiliyor. Bu veri hangi olayı destekler?",
             "Ay tutulmasını; Ay, Dünya'nın gölgesine girmiştir.",
             ["Güneş tutulmasını; Ay gölgesi dar bir yol oluşturmuştur.", "Güneş lekesini; Dünya Ay'ı örtmüştür.", "Ay'ın kendi ışığının sönmesini"],
             "Ay tutulması gece tarafındaki geniş bir alandan izlenebilir ve Ay'ın Dünya gölgesine girmesiyle oluşur."),
        task(n, "comprehension", "Tutulma olaylarından bilimsel çıkarım yapılırken hangi iki bilgi birlikte kullanılmalıdır?",
             "Gök cisimlerinin dizilişi ile ışık ve gölge yönü",
             ["Yalnız gök cisimlerinin adları", "Yalnız gözlemcinin yaşı", "Gezegenlerin yüzey sıcaklıkları"],
             "Tutulmanın türünü sıra ve gölge ilişkisi belirler; ilgisiz özellikler çıkarımı desteklemez."),
        task(n, "error-analysis", "Bir öğrenci Ay'ın kendi ışığını ürettiği için tutulmada karardığını düşünüyor. Doğru açıklama hangisidir?",
             "Ay Güneş'ten gelen ışığı yansıtır; Dünya gölgesine girince aydınlanan bölümü azalır.",
             ["Ay ışık üretir ve istediğinde kapatır.", "Dünya tutulma sırasında Güneş'in ışığını kalıcı olarak söndürür.", "Ay'ın rengi yalnız bulutlar nedeniyle değişir; gölge etkili değildir."],
             "Ay bir ışık kaynağı değildir; görünürlüğü Güneş ışığını yansıtmasına bağlıdır."),
    ]


def eclipse_model_tasks() -> list[Task]:
    n = "tr-g06-fen-bilimleri-note-004"
    return [
        task(n, "application", "Üç küreyle kurulan tutulma modelinde olayın nedenini göstermek için hangi öğe mutlaka eklenmelidir?",
             "Işık kaynağı ile ışığın geliş ve gölge yönleri",
             ["Kürelerin fiyat etiketleri", "Rastgele yıldız süsleri", "Gök cisimlerinin alfabetik sırası"],
             "Tutulma modeli yalnız cisimleri değil, ışık kaynağı ve gölge ilişkisini göstermelidir."),
        task(n, "analysis", "Bir modelde lamba-Ay küresi-Dünya küresi aynı doğrultudadır. Ay'ın arkasındaki dar gölge Dünya'ya ulaşıyor. Model neyi temsil eder?",
             "Güneş tutulmasını",
             ["Ay tutulmasını", "Mevsimlerin oluşumunu", "Dünya'nın günlük hareketini"],
             "Lamba Güneş'i temsil eder; Ay aradaysa gölgesi Dünya üzerine düşer."),
        task(n, "analysis", "Lamba-Dünya küresi-Ay küresi dizilişinde Dünya'nın gölgesi Ay'a düşüyor. Hangi model kurulmuştur?",
             "Ay tutulması modeli",
             ["Güneş tutulması modeli", "Güneş Sistemi büyüklük modeli", "Ay'ın evreleriyle ilgisiz bir model"],
             "Dünya ışık kaynağı ile Ay arasındadır; bu konum Ay tutulmasını temsil eder."),
        task(n, "application", "Tutulma modelindeki gölge hiç görünmüyor. İlk denetlenecek düzenek özelliği hangisidir?",
             "Lamba ile kürelerin doğrultusu ve aralarındaki konum",
             ["Kürelerin boya markası", "Masanın rengi", "Öğrencilerin oturma sırası"],
             "Gölgenin oluşması ışık kaynağı, engel ve ekran görevi gören cismin hizasına bağlıdır."),
        task(n, "comprehension", "Bilimsel tutulma modelinin sınırlılığı hangi ifadeyle doğru belirtilir?",
             "Kürelerin boyut ve uzaklıkları gerçek oranlarda olmayabilir.",
             ["Model gök cisimlerinin konum ilişkisini hiçbir zaman gösteremez.", "Modelde ışık kullanılmaz.", "Model gerçeğin bütün ayrıntılarını zorunlu olarak içerir."],
             "Sınıf modeli konum ve gölgeyi açıklayabilir; gerçek ölçekleri aynı anda vermesi beklenmeyebilir."),
        task(n, "application", "Güneş tutulması modeli kuran öğrenci üç küreyi hangi konum ilişkisiyle yerleştirmelidir?",
             "Ay, Güneş ile Dünya arasına alınmalıdır.",
             ["Güneş, Dünya ile Ay arasına alınmalıdır.", "Bütün cisimler farklı doğrultulara dağıtılmalıdır.", "Işık kaynağı modelden çıkarılmalıdır."],
             "Güneş tutulmasında Ay'ın gölgesinin Dünya'ya düşebilmesi için Ay arada olmalıdır."),
        task(n, "application", "Modelin Ay tutulmasını yalnız belirli hizalanmada göstermesi için hangi işlem uygundur?",
             "Dünya küresini lamba ile Ay küresi arasına getirip gölgeyi Ay üzerinde gözlemek",
             ["Ay küresini lambanın arkasına saklamak", "Dünya küresini modelden çıkarmak", "Lambayı kapatıp kürelerin rengini karşılaştırmak"],
             "Ay tutulması modeli Güneş-Dünya-Ay doğrultusu ve Dünya gölgesini gerektirir."),
        task(n, "analysis", "İlk taslak yalnız cisimlerin sırasını, ikinci taslak buna gölge konisini de gösteriyor. Hangisi tutulmanın nedenini daha iyi açıklar?",
             "İkinci taslak; çünkü sıra ile ışık-gölge ilişkisini birlikte gösterir.",
             ["İlk taslak; çünkü gölge bilimsel modelde gereksizdir.", "İkisi eşittir; açıklayıcılık değerlendirilmez.", "İlk taslak; çünkü daha az kanıt her zaman daha doğrudur."],
             "Tutulma, konumun ışık yolunu nasıl değiştirdiğiyle açıklanır; gölge gösterimi modeli geliştirir."),
        task(n, "comprehension", "Bir tutulma modeli yeni gözlemle uyuşmadığında bilimsel olarak ne yapılmalıdır?",
             "Modelin konum, ölçek veya ışık varsayımları yeniden incelenip model geliştirilmelidir.",
             ["Gözlem otomatik olarak yanlış sayılmalıdır.", "Model değişmez gerçek kabul edilmelidir.", "Yalnız modelin adı değiştirilmelidir."],
             "Model kanıtı açıklamak için kullanılır ve güvenilir yeni kanıta göre geliştirilebilir."),
        task(n, "application", "Güneş tutulmasındaki tam ve kısmi gölge bölgelerini ayırt etmek isteyen grup modele ne eklemelidir?",
             "Ay'ın arkasında dar tam gölge ve çevresindeki kısmi gölge alanlarını gösteren ışınlar",
             ["Dünya'nın içine rastgele renkler", "Ay'ın önüne ikinci bir Güneş", "Yörünge bilgisini gizleyen tek bir etiket"],
             "Farklı gözlem bölgeleri, ışın sınırları ve oluşan gölge alanlarıyla modellenir."),
        task(n, "error-analysis", "Bir öğrenci “Küreler doğru sıradaysa lamba Dünya'nın arkasında olsa da tutulma modeli doğrudur.” diyor. Bu yargıdaki eksik nedir?",
             "Işık kaynağının yönü de tutulma olayına uygun olmalıdır.",
             ["Işık kaynağının konumu hiçbir modeli etkilemez.", "Yalnız kürelerin rengi doğruluğu belirler.", "Tutulma modeli gölge içeremez."],
             "Doğru sıra tek başına yeterli değildir; ışık-gölge yönü fiziksel olayla uyumlu olmalıdır."),
        task(n, "analysis", "İki model aynı dizilişi gösteriyor; yalnız biri cisimlerin yörünge düzlemlerinin her ay tam çakışmadığını belirtiyor. Hangisi tutulmaların neden her ay olmadığını açıklar?",
             "Yörünge düzlemi bilgisini içeren model",
             ["Bu bilgiyi içermeyen model; çünkü yalnız küre sayısı önemlidir.", "İkisi de açıklayamaz; yörünge tutulmayla ilgisizdir.", "Küreleri daha parlak olan model"],
             "Her ay tutulma olmamasını açıklamak için dizilişin yanında yörünge düzlemlerinin uygun kesişmesi gerekir."),
        task(n, "application", "Bir model sunumunda izleyici hangi kürenin hangi gök cismini temsil ettiğini karıştırıyor. En uygun geliştirme hangisidir?",
             "Görünür fakat cevabı söylemeyen Güneş, Dünya ve Ay etiketleri eklemek",
             ["Küreleri etiketsiz bırakmak", "Üç küreye aynı adı vermek", "Işık kaynağını gizlemek"],
             "Model anahtarı öğelerin neyi temsil ettiğini açıklar; konum ilişkisini izleyicinin yerine çözmez."),
    ]


def force_tasks() -> list[Task]:
    n = "tr-g06-fen-bilimleri-note-005"
    return [
        task(n, "application", "Bir sandığa doğuya 18 N, batıya 11 N kuvvet uygulanıyor. Bileşke kuvvet nedir?",
             "7 N doğu", ["29 N doğu", "7 N batı", "29 N batı"],
             "Zıt yönlü kuvvetler çıkarılır; 18−11=7 N ve yön büyük kuvvetin yönü olan doğudur."),
        task(n, "application", "Aynı doğrultuda batıya 6 N ve 9 N uygulanan iki kuvvetin bileşkesi hangisidir?",
             "15 N batı", ["3 N batı", "15 N doğu", "3 N doğu"],
             "Aynı yönlü kuvvetler toplanır ve yön korunur: 6+9=15 N batı."),
        task(n, "analysis", "Bir cisimde sağa doğru bileşke 4 N'dir. Sola 5 N kuvvet biliniyorsa sağa uygulanan kuvvet kaç N'dir?",
             "9 N", ["1 N", "4 N", "20 N"],
             "Sağ kuvvet−5 N=4 N olduğundan sağ kuvvet 9 N'dir."),
        task(n, "comprehension", "Eşit büyüklükte ve zıt yönlü iki kuvvet için hangi sonuç doğrudur?",
             "Bileşke kuvvet 0 N olur.", ["Kuvvetler aynı yönlüymüş gibi toplanır.", "Bileşke küçük kuvvet yönünde olur.", "Kuvvetlerin doğrultusu yok olur."],
             "Eşit ve zıt kuvvetler vektörel olarak birbirini dengeler."),
        task(n, "application", "Bir kontrol kartında 14 N doğu ve 8 N batı kuvvetlerinin bileşkesi soruluyor. Hangi sonuç yazılmalıdır?",
             "Zıt yönlü oldukları için çıkarılmalı; sonuç 6 N doğu olmalıdır.",
             ["Toplama doğrudur fakat yön batı olmalıdır.", "İki kuvvet de yok sayılmalıdır.", "14 ile 8 çarpılıp 112 N bulunmalıdır."],
             "Zıt yönlü kuvvetlerde büyüklük farkı alınır; büyük olan doğu yönünü belirler."),
    ]


def balanced_force_tasks() -> list[Task]:
    n = "tr-g06-fen-bilimleri-note-006"
    return [
        task(n, "comprehension", "Dengelenmiş kuvvetlerin ortak özelliği hangisidir?",
             "Cisme etki eden bileşke kuvvetin sıfır olması",
             ["Cismin mutlaka hareketsiz olması", "Bütün kuvvetlerin aynı yönde olması", "Cismin süratinin her saniye artması"],
             "Dengelenme hareket durumuyla değil net kuvvetin sıfır olmasıyla tanımlanır."),
        task(n, "analysis", "Düz yolda sabit süratle ilerleyen araca motor 300 N ileri, dirençler 300 N geri kuvvet uyguluyor. Hangi yorum doğrudur?",
             "Kuvvetler dengelenmiştir; araç hareketini sabit süratle sürdürebilir.",
             ["Araç mutlaka durur.", "Net kuvvet 600 N ileridir.", "Kuvvetler dengelenmemiştir çünkü araç hareketlidir."],
             "Eşit zıt kuvvetlerin bileşkesi sıfırdır; hareketli cisim sabit hız durumunu koruyabilir."),
        task(n, "application", "Başlangıçta duran bir arabaya sağa 5 N, sola 2 N uygulanıyor. Hareket için en uygun öngörü hangisidir?",
             "Net 3 N sağa olduğundan araba sağa doğru hızlanabilir.",
             ["Net kuvvet sıfır olduğundan kesinlikle hareketsiz kalır.", "Net 7 N sola olduğundan sola hızlanır.", "Kuvvet yönleri hareketi etkilemez."],
             "Bileşke 5−2=3 N sağdır; dengelenmemiş kuvvet hareket durumunu değiştirebilir."),
        task(n, "error-analysis", "Bir öğrenci 'Hareket eden her cisimde kuvvetler dengelenmemiştir.' diyor. Doğru düzeltme hangisidir?",
             "Sabit hızla doğrusal hareket eden cisimde net kuvvet sıfır olabilir.",
             ["Hareketli cisimlere hiçbir kuvvet etki etmez.", "Dengelenmiş kuvvet yalnız düşen cisimlerde görülür.", "Net kuvvet sıfırsa cisim mutlaka geçmişte de hiç hareket etmemiştir."],
             "Dengelenmiş kuvvet hareketi değil, hareket durumundaki değişimin olmamasını açıklar."),
        task(n, "analysis", "Bir topun doğuya sürati her saniye artıyor. Kuvvetler için hangi çıkarım yapılabilir?",
             "Doğu yönünde sıfırdan farklı bir bileşke kuvvet vardır.",
             ["Kuvvetler kesinlikle dengelenmiştir.", "Bileşke batı yönündedir.", "Topa hiçbir kuvvet etki etmemektedir."],
             "Doğu yönündeki hız artışı aynı yönde net kuvvet bulunduğunu gösterir."),
        task(n, "application", "Bir asansör sabit hızla yukarı çıkarken kuvvet modeli nasıl olmalıdır?",
             "Yukarı taşıma kuvveti ile aşağı ağırlık etkisi dengelenmiş gösterilmelidir.",
             ["Yalnız yukarı kuvvet çizilmelidir.", "Aşağı kuvvet daha büyük çizilmelidir.", "Hareket ettiği için net kuvvet zorunlu olarak yukarı çizilmelidir."],
             "Sabit hız, hız değişimi olmadığını ve basitleştirilmiş modelde net kuvvetin sıfır olabileceğini gösterir."),
        task(n, "comprehension", "Dengelenmemiş kuvvet bir cismin hangi özelliğini değiştirebilir?",
             "Hızının büyüklüğünü veya yönünü",
             ["Maddenin kimyasal türünü zorunlu olarak", "Kütlesini her durumda", "Gezegen üzerindeki konumundan bağımsız ağırlığını sıfıra"],
             "Net kuvvet cismin hareket durumunu, yani sürat veya yönünü değiştirebilir."),
        task(n, "application", "Sağa 12 N ve sola 12 N kuvvet uygulanan düzenek için hareket tahmini yapılacaktır. Hangi net kuvvet kullanılmalıdır?",
             "Kuvvetler zıt ve eşit olduğundan net kuvvet 0 N'dir.",
             ["Net kuvvet 24 N sola olmalıdır.", "Net kuvvet 12 N sağ olmalıdır.", "Yönler göz ardı edilip kuvvetler çarpılmalıdır."],
             "Vektörel yönler dikkate alındığında eşit zıt kuvvetler birbirini dengeler."),
    ]


def speed_velocity_tasks() -> list[Task]:
    n = "tr-g06-fen-bilimleri-note-007"
    return [
        task(n, "comprehension", "Sürat ile hız arasındaki temel fark hangisidir?",
             "Hız yön içerirken sürat yalnız büyüklük bildirir.",
             ["Sürat yön içerir, hız içermez.", "İkisi de yalnız alınan yola bağlıdır.", "Hızın birimi yoktur."],
             "Sürat skaler, hız yönlü bir büyüklüktür."),
        task(n, "application", "Bir bisikletli 180 metre yolu 30 saniyede alıyor. Ortalama sürati kaç m/s'dir?",
             "6 m/s", ["5 m/s", "30 m/s", "210 m/s"],
             "Ortalama sürat alınan yol/zaman=180/30=6 m/s'dir."),
        task(n, "analysis", "Koşucu 200 metrelik parkuru gidip aynı yoldan başlangıca dönüyor. Toplam süre 100 saniyedir. Hangisi doğrudur?",
             "Ortalama sürati 4 m/s, ortalama hızı 0 m/s'dir.",
             ["Ortalama sürati ve hızı 0 m/s'dir.", "Ortalama sürati 2 m/s, hızı 4 m/s'dir.", "Yer değiştirmesi 400 metredir."],
             "Toplam yol 400 m olduğundan sürat 4 m/s; başlangıca dönüşte yer değiştirme sıfır olduğundan ortalama hız sıfırdır."),
        task(n, "application", "Bir araç kuzeye doğru 12 m/s hareket ediyor. Bu ifade hangi büyüklüğü verir?",
             "Hızı; çünkü büyüklükle birlikte yön de verilmiştir.",
             ["Yalnız sürati; yön bilgisi önemsizdir.", "Kütleyi", "Bileşke kuvveti doğrudan"],
             "Yön içeren hareket oranı hızdır."),
        task(n, "error-analysis", "Bir öğrenci “Bir turda alınan yol 300 m ise yer değiştirme de 300 m'dir.” diyor. Hangi düzeltme gerekir?",
             "Başlangıç noktasına dönüldüğünden yer değiştirme 0 m'dir.",
             ["Alınan yol da 0 m'dir.", "Yer değiştirme 600 m'dir.", "Yol ve yer değiştirme her durumda aynıdır."],
             "Yer değiştirme başlangıçtan bitişe yönlü konum farkıdır; kapalı turda sıfırdır."),
        task(n, "analysis", "Aynı sürede K 100 m, L 140 m yol alıyor. Yalnız bu verilere göre hangi sonuç desteklenir?",
             "L'nin ortalama sürati K'den büyüktür.",
             ["K'nin ortalama sürati daha büyüktür.", "İkisinin yönlü hızları kesinlikle aynıdır.", "L'nin yer değiştirmesi mutlaka 140 m'dir."],
             "Süreler eşitken daha çok yol alanın ortalama sürati daha büyüktür; yön ve yer değiştirme verilmemiştir."),
        task(n, "comprehension", "Ortalama hız hesabında paya hangi büyüklük yazılır?",
             "Yer değiştirme", ["Toplam alınan yol", "Cismin kütlesi", "Bileşke kuvvet"],
             "Ortalama hız yer değiştirme/zaman; ortalama sürat toplam yol/zaman bağıntısıyla bulunur."),
    ]


def reproduction_tasks() -> list[Task]:
    n = "tr-g06-fen-bilimleri-note-008"
    return [
        task(n, "comprehension", "Eşeyli üremenin ayırt edici olayı hangisidir?", "Üreme hücrelerinin birleşmesi ve döllenme",
             ["Tek ana canlıdan tomurcuk oluşması", "Sürünücü gövdeden yeni bitki gelişmesi", "Canlının yalnız büyümesi"],
             "Eşeyli üremede dişi ve erkek üreme hücreleri birleşir."),
        task(n, "application", "Patates yumrusundan yeni bitki yetişmesi nasıl sınıflandırılır?", "Eşeysiz üreme",
             ["Eşeyli üreme", "Döllenme", "Yalnız büyüme"],
             "Yumruyla vejetatif çoğalmada üreme hücreleri birleşmez."),
        task(n, "analysis", "İki yavrunun özellikleri karşılaştırılıyor: K ana canlıyla neredeyse aynı, L iki ebeveynden farklı özellikler taşıyor. En uygun yorum hangisidir?",
             "K eşeysiz, L eşeyli üremeyle oluşmuş olabilir.",
             ["K kesinlikle eşeyli, L kesinlikle eşeysizdir.", "Benzerlik üreme biçimi hakkında hiçbir ipucu vermez.", "İki yavru da yalnız büyüme sonucu oluşmuştur."],
             "Eşeysiz üreme genetik benzerliği korurken eşeyli üreme çeşitliliğe katkı sağlar; ifade olasılık sınırında tutulur."),
        task(n, "error-analysis", "Bir öğrenci 'Tek ebeveyn görülüyorsa mutlaka eşeysiz üreme vardır.' diyor. Hangi ölçüt daha güvenilirdir?",
             "Üreme hücrelerinin birleşip birleşmediğini incelemek",
             ["Yalnız ebeveynin dış görünüşüne bakmak", "Yavrunun yaşını ölçmek", "Canlının yaşadığı ortamın rengini seçmek"],
             "Gözlenen ebeveyn sayısı tek başına yeterli değildir; döllenme ayırt edici ölçüttür."),
        task(n, "application", "Çileğin sürünücü gövdesinden oluşan yeni bitki için hangisi doğrudur?",
             "Döllenme olmadan oluştuğu için eşeysiz üreme örneğidir.",
             ["Tohum oluştuğu için zorunlu olarak eşeylidir.", "Üreme değildir; yalnız fotosentezdir.", "İki üreme hücresi birleşmiştir."],
             "Sürünücü gövde vejetatif eşeysiz üreme sağlar."),
        task(n, "comprehension", "Eşeysiz üremenin bir avantajı hangisidir?",
             "Uygun koşullarda kısa sürede çok sayıda birey oluşturabilmesi",
             ["Her zaman yüksek genetik çeşitlilik oluşturması", "Mutlaka iki ebeveyn gerektirmesi", "Döllenme olmadan gerçekleşememesi"],
             "Eşeysiz üreme hızlı çoğalma sağlayabilir; çeşitlilik genellikle sınırlıdır."),
        task(n, "analysis", "Bir maya hücresinin yüzeyinde küçük bir çıkıntı büyüyüp ayrılıyor. Bu gözlem hangi süreci destekler?",
             "Tomurcuklanmayla eşeysiz üremeyi",
             ["Döllenmeyle eşeyli üremeyi", "Tohumla çoğalmayı", "Yalnız hücrenin beslenmesini"],
             "Tomurcuk ana canlı üzerinde gelişip ayrılan yeni bireydir ve eşeysiz üreme biçimidir."),
        task(n, "error-analysis", "Bir öğrenci “Eşeysiz üremede yavrular her zaman birbirinden çok farklıdır.” diyor. Doğru düzeltme hangisidir?",
             "Eşeysiz üremede yavrular genellikle ana canlıya ve birbirine çok benzer.",
             ["Eşeysiz üremede kalıtsal madde bulunmaz.", "Eşeyli üremede yavrular mutlaka özdeştir.", "Üreme biçimi benzerliği hiçbir zaman etkilemez."],
             "Tek ana canlıdan döllenmesiz oluşum genetik çeşitliliği sınırlı tutar."),
        task(n, "application", "Bir üretici hastalığa dayanıklı bitkinin aynı özelliklerini koruyarak çoğaltmak istiyor. Hangi yöntem amaca daha uygundur?",
             "Bitkiden çelik alarak vejetatif çoğaltma",
             ["Farklı iki çeşidi rastgele tozlaştırma", "Yalnız çiçek rengini gözleme", "Tohumların tamamını farklı türlerle karıştırma"],
             "Vejetatif eşeysiz çoğaltma seçilen bitkinin özelliklerini büyük ölçüde korur."),
        task(n, "analysis", "Döllenme sonucu zigot oluşan bir olay için hangi sınıflandırma kesinlikle yapılabilir?",
             "Eşeyli üreme sürecidir.", ["Eşeysiz üremedir.", "Tomurcuklanmadır.", "Vejetatif üremedir."],
             "Zigot, üreme hücrelerinin birleşmesiyle oluşur ve eşeyli üremenin kanıtıdır."),
    ]


def plant_growth_tasks() -> list[Task]:
    n = "tr-g06-fen-bilimleri-note-009"
    return [
        task(n, "analysis", "Özdeş iki bitkiden biri aydınlıkta, diğeri karanlıkta eşit sulanıyor. Karanlıktaki bitki soluk ve zayıf gelişiyor. Hangi çıkarım desteklenir?",
             "Işık, bitkinin sağlıklı büyüme ve gelişmesini etkileyen faktörlerden biridir.",
             ["Işık bitki gelişimini hiçbir biçimde etkilemez.", "Karanlık bütün bitkilerin büyümesini daima hızlandırır.", "Deney suyun etkisini ölçmektedir."],
             "Su eşitken değişen ışık koşulu ile gelişim farkının birlikte görülmesi ışığın etkisini destekler."),
        task(n, "application", "Suyun bitki büyümesine etkisini adil biçimde sınamak için hangi düzenek uygundur?",
             "Özdeş bitkileri aynı ışık ve sıcaklıkta tutup yalnız su miktarını değiştirmek",
             ["Bitki türü, ışık ve suyu birlikte değiştirmek", "Bir bitkiyi ölçüp karşılaştırma yapmamak", "Saksıları farklı haftalarda rastgele sulamak"],
             "Neden çıkarımı için bağımsız değişken su olmalı, diğer temel koşullar sabit tutulmalıdır."),
        task(n, "comprehension", "Bitkinin büyümesi ile gelişmesi arasındaki ilişkiyi doğru açıklayan ifade hangisidir?",
             "Büyüme boyut ve kütle artışını, gelişme yapı ve işlevlerde olgunlaşmayı içerir.",
             ["İki kavram her durumda yalnız boy uzaması demektir.", "Gelişme yalnız su miktarını ölçer.", "Büyüme canlılarda gözlenemez."],
             "Büyüme nicel artış, gelişme ise yapı ve işlevlerin değişip olgunlaşmasıdır."),
        task(n, "error-analysis", "Bir öğrenci “Bir bitkiye ne kadar çok su verilirse bitki o kadar sağlıklı büyür.” diyor. Hangi düzeltme doğrudur?",
             "Bitkinin gereksiniminden fazla su köklere zarar verebilir; uygun miktar tür ve koşula bağlıdır.",
             ["Su miktarı bitkileri hiçbir zaman etkilemez.", "Bitkiler yalnız karanlıkta su kullanır.", "En az su her tür için daima en iyidir."],
             "Büyümede kaynakların yalnız varlığı değil, uygun düzeyde olması önemlidir."),
        task(n, "analysis", "Bir çiçeğin böcek girişini engelleyen ince ağla kapatılması sonrası meyve oluşumu azalıyor; açık çiçeklerde sürüyor. Hangi sonuç uygundur?",
             "Tozlaşmanın engellenmesi döllenme, tohum ve meyve oluşumunu azaltmış olabilir.",
             ["Ağ kesinlikle toprağın mineralini artırmıştır.", "Meyve oluşumu tozlaşmadan bütünüyle bağımsızdır.", "Açık çiçeklerde üreme gerçekleşmemiştir."],
             "İki grup arasındaki belirgin fark tozlaştırıcı erişimidir; sonuç olasılık sınırında yorumlanır."),
        task(n, "application", "Mineral eksikliğinin etkisini araştıran deneyde hangi ölçüm anlamlıdır?",
             "Aynı süre sonunda yaprak rengi, yaprak sayısı ve boy değişimini karşılaştırmak",
             ["Yalnız saksıların dış rengini karşılaştırmak", "Her bitkiye farklı ışık ve su vermek", "Başlangıç ölçümü almadan yalnız tahmin yazmak"],
             "Büyüme-gelişme etkisi gözlenebilir göstergeler ve kontrollü koşullarla izlenir."),
        task(n, "comprehension", "Çiçekli bitkide döllenmeden sonra tohumun oluşmasına katkı sağlayan yapı hangisidir?",
             "Tohum taslağı", ["Kök tüyü", "Yaprak damarı", "Gövde kabuğu"],
             "Döllenmiş tohum taslağı gelişerek tohumu oluşturur."),
        task(n, "error-analysis", "Bir öğrenci “Farklı tür ve yaştaki iki bitkinin boy farkı yalnız ışık miktarından kaynaklanır.” diyor. Temel hata nedir?",
             "Bitki türü ve başlangıç yaşı kontrol edilmediği için ışığın tek etkisi ayrıştırılamaz.",
             ["Işık deneylerde hiç değişken olamaz.", "Boy ölçümü bitkilerde kullanılamaz.", "Karşılaştırma için daha çok değişkeni aynı anda değiştirmek gerekir."],
             "Adil karşılaştırmada incelenmeyen özellikler olabildiğince eşit tutulur."),
        task(n, "application", "Seradaki bitkilerin bir grubunda ışık süresi azaltılacak. Önceden hangi hipotez uygun biçimde kurulabilir?",
             "Diğer koşullar eşitse daha az ışık alan grubun gelişim göstergeleri azalabilir.",
             ["Işık süresi azalınca bütün bitkiler kesinlikle iki kat büyür.", "Işık ile gelişim arasında hiçbir hipotez kurulamaz.", "Sonuç ölçülmeden hipotez kesin kanun sayılır."],
             "Hipotez değişkenler arasında sınanabilir ve kesinlik taşımayan bir ilişki önerir."),
    ]


def germination_tasks() -> list[Task]:
    n = "tr-g06-fen-bilimleri-note-010"
    return [
        task(n, "comprehension", "Tohumun çimlenmesi için temel çevre koşulları hangi seçenekte birlikte verilmiştir?",
             "Uygun sıcaklık, yeterli su ve oksijen",
             ["Yalnız yoğun ışık ve gübre", "Toprak, çiçek ve meyve", "Sınırsız su ve oksijensiz ortam"],
             "Çimlenmede uygun sıcaklık, nem ve solunum için oksijen gerekir; ışık her tohum için zorunlu değildir."),
        task(n, "application", "Suyun çimlenmeye etkisini sınamak için hangi iki kap karşılaştırılmalıdır?",
             "Aynı sıcaklık ve oksijende tutulan, yalnız su miktarı farklı iki kap",
             ["Suyu, sıcaklığı ve tohumu farklı iki kap", "Biri tohumlu biri tohumsuz iki kap", "Bütün koşulları farklı iki kap"],
             "Yalnız su değişirse gözlenen fark suyla ilişkilendirilebilir."),
        task(n, "analysis", "Nemli pamuktaki tohumlar 22°C'de çimleniyor, aynı nemde 2°C'dekiler çimlenmiyor. Hangi çıkarım desteklenir?",
             "Uygun sıcaklık çimlenmeyi etkileyen bir koşuldur.",
             ["Su çimlenmeyi engeller.", "Tohumlar yalnız karanlıkta çimlenir.", "Sıcaklık etkisini ölçmek için nem de değiştirilmelidir."],
             "Nem eşitken sıcaklıkla birlikte sonuç değişmiştir; uygun sıcaklığın etkisi desteklenir."),
        task(n, "error-analysis", "Bir öğrenci su dolu kapta tamamen batırdığı tohumların çimlenmemesini 'su hiç gerekmiyor' diye yorumluyor. Doğru düzeltme hangisidir?",
             "Aşırı su oksijen erişimini azaltmış olabilir; çimlenme yeterli su ile birlikte oksijen de gerektirir.",
             ["Tohumlar oksijensiz ortamda her zaman daha hızlı çimlenir.", "Su miktarı ile oksijen arasında hiçbir ilişki kurulamaz.", "Çimlenme yalnız tohumun rengine bağlıdır."],
             "Tek koşulun aşırı düzeyi o koşulun gereksiz olduğunu göstermez; diğer gereksinimler de değerlendirilir."),
        task(n, "application", "Oksijenin etkisini araştıran güvenli düzende hangi değişken değiştirilmelidir?",
             "Tohumların hava ile temas durumu",
             ["Tohum türü, sıcaklık ve su birlikte", "Yalnız kapların rengi", "Ölçüm süresi her kapta farklı"],
             "Bağımsız değişken oksijen erişimi, bağımlı değişken çimlenen tohum sayısı olmalıdır."),
        task(n, "comprehension", "Çimlenme deneyinde 'bağımlı değişken' ne olabilir?",
             "Belirli süre sonunda çimlenen tohum sayısı",
             ["Araştırmacının adı", "Kapların masa üzerindeki sıra numarası", "Sabit tutulan tohum türü"],
             "Bağımlı değişken, değiştirilen koşulun etkisiyle ölçülen sonuçtur."),
        task(n, "analysis", "Dört kaptan yalnız nemli, hava alan ve ılık ortamda bulunan tohumlar çimleniyor. En kapsamlı çıkarım hangisidir?",
             "Bu düzende su, oksijen ve uygun sıcaklığın birlikte bulunması çimlenmeyi desteklemiştir.",
             ["Yalnız ışık çimlenmeyi belirlemiştir.", "Tek bir tohum bütün türler için kesin kanıt sağlar.", "Oksijen çimlenmeyi engellemiştir."],
             "Karşılaştırılan kaplar üç temel koşulun birlikte önemini destekler; sonuç tüm türlere sınırsız genellenmez."),
        task(n, "error-analysis", "Bir öğrenci “İki kapta hem sıcaklık hem su farklı olsa da sonuç yalnız sıcaklığın etkisini gösterir.” diyor. Hangi hata yapılmıştır?",
             "Birden fazla değişken aynı anda değiştiği için sıcaklığın etkisi ayrıştırılamaz.",
             ["Deneylerde sıcaklık ölçülemez.", "Su çimlenmeyi hiçbir zaman etkilemez.", "Değişken sayısı arttıkça neden sonucu kesinleşir."],
             "Kontrollü deneyde incelenen etken dışında diğer koşullar sabit tutulur."),
        task(n, "application", "Işığın fasulye tohumlarının çimlenmesine etkisi sınanacak. En uygun plan hangisidir?",
             "Özdeş tohumları aynı su, sıcaklık ve oksijende tutup yalnız ışık koşulunu değiştirmek",
             ["Işıklı grubu sıcak, karanlık grubu soğuk tutmak", "Gruplara farklı miktarda su vermek", "Sonuçları ölçmeden ışığın zorunlu olduğunu ilan etmek"],
             "Işığın etkisini ayırmak için yalnız ışık bağımsız değişken olmalıdır."),
        task(n, "comprehension", "Hipotezin bilimsel olarak sınanabilir olması ne demektir?",
             "Değişkenler ve beklenen sonuç gözlem veya ölçümle karşılaştırılabilir olmalıdır.",
             ["Sonuç deneyden önce kesin doğru ilan edilmelidir.", "Hipotez hiçbir koşulda değiştirilememelidir.", "Ölçülemeyen kişisel beğeni yeterlidir."],
             "Sınanabilir hipotez, değişkenler arasında ölçülebilir bir beklenti kurar."),
        task(n, "analysis", "Bir deneyde 20 tohumdan 18'i uygun nem ve sıcaklıkta, 4'ü çok soğuk ortamda çimleniyor. Hangi rapor cümlesi uygundur?",
             "Veriler, bu tohumlarda uygun sıcaklığın çimlenme oranını artırdığı görüşünü destekler.",
             ["Soğuk ortam bütün tohumlarda çimlenmeyi kesinlikle yok eder.", "Nem sonuçla ilgisizdir çünkü iki grupta eşittir.", "Tek deney evrendeki bütün bitkiler için değişmez yasa kurar."],
             "Sonuç verilen tohum ve koşullarla sınırlı, verinin desteklediği biçimde yazılır."),
        task(n, "error-analysis", "Bir öğrenci “Çimlenme ile büyüme aynı süreçtir; aralarında fark yoktur.” diyor. Doğru ayrım hangisidir?",
             "Çimlenme embriyonun gelişmeye başlamasıdır; büyüme çimlenme sonrasında da süren boyut ve kütle artışıdır.",
             ["Çimlenme yalnız meyve oluşumudur.", "Büyüme tohumun su almadan önceki hâlidir.", "İki süreç canlılıkla ilişkili değildir."],
             "Çimlenme yaşam döngüsünün başlangıç geçişidir; büyüme daha uzun süren nicel artıştır."),
    ]


def animal_tasks() -> list[Task]:
    n = "tr-g06-fen-bilimleri-note-011"
    return [
        task(n, "analysis", "Bir canlı yumurtalarını suya bırakıyor; yavru önce solungaçla yaşıyor, sonra akciğerli ergin hâle geliyor. Hangi çıkarım uygundur?",
             "Canlı dış gelişim ve başkalaşım gösteren bir kurbağa olabilir.",
             ["Canlı kesinlikle doğurarak çoğalan bir memelidir.", "Yavru hiçbir gelişim evresi geçirmemiştir.", "Yumurta bırakmak yalnız bitkilere özgüdür."],
             "Su ortamındaki yumurta, iribaş ve ergin geçişi kurbağanın başkalaşım döngüsüyle uyumludur."),
        task(n, "comprehension", "Doğurarak çoğalan bir memelide yavrunun gelişimi için hangisi genel olarak doğrudur?",
             "Embriyonun gelişimi anne vücudunda sürer ve doğumdan sonra bakım görülebilir.",
             ["Yavru mutlaka yumurta içinde dış ortamda gelişir.", "Bütün memeliler başkalaşım geçirir.", "Üreme ile büyüme arasında hiçbir ilişki yoktur."],
             "Memelilerin çoğunda iç gelişim ve doğum sonrası yavru bakımı görülür."),
    ]


TASK_BUILDERS = [
    planet_tasks, model_tasks, eclipse_inference_tasks, eclipse_model_tasks,
    force_tasks, balanced_force_tasks, speed_velocity_tasks, reproduction_tasks,
    plant_growth_tasks, germination_tasks, animal_tasks,
]


def make_record(
    local: int, item: Task, note: dict[str, Any], labels: dict[str, str],
    *, batch: int = 7, number_base: int = 600,
) -> dict[str, Any]:
    qid = f"tr-g06-bank-fen-b{batch:02d}-q{local:03d}"
    correct_position = (local - 1) % 4
    choices = rotate(item["correct"], item["wrongs"], correct_position)
    figure = None
    if item["figure_kind"] in {"solar", "lunar"}:
        figure = _eclipse_figure(qid, labels, lunar=item["figure_kind"] == "lunar")
    elif item["figure_kind"] == "ray":
        figure = _ray_figure(qid, labels)
    elif item["figure_kind"] == "prism":
        figure = _prism_figure(qid, labels)
    explanation = str(item["explanation"]).rstrip()
    if explanation[-1:] not in ".!?…":
        explanation += "."
    explanation += " Bu nedenle doğru seçenek, verilen koşul ile bilimsel ilişkiyi aynı kapsamda tutar."
    correct_reason = f"Doğru gerekçe: {explanation}"
    wrong_reasons = [
        f"Kavram karışıklığı: {item['wrongs'][0]} ifadesi ilgili kavramların görevini veya sınıfını birbiriyle karıştırır.",
        f"Koşul ve yön hatası: {item['wrongs'][1]} ifadesi soruda verilen yön, değişken ya da karşılaştırma koşulunu korumaz.",
        f"Kanıt dışı genelleme: {item['wrongs'][2]} ifadesi verilen durumun desteklemediği kesin veya ilgisiz bir sonuç kurar.",
    ]
    reason_map = {item["correct"]: correct_reason, **dict(zip(item["wrongs"], wrong_reasons))}
    objective = str((note.get("objectives") or [note.get("objective")])[0])
    visual_need = (
        {
            "level": "required", "role": "evidence",
            "rationale": "Çözüm için gereken uzamsal sıra, ışın veya gölge kanıtı yalnız yapılandırılmış şemada verilmiştir.",
            "acceptableKinds": ["diagram"], "evidenceDimensions": ["gök cismi sırası", "gölge yönü"],
        }
        if figure else
        {
            "level": "none", "role": "none",
            "rationale": "Çözüm için gerekli bütün bilgi soru metninde açıkça verilmiştir.",
            "acceptableKinds": [], "evidenceDimensions": [],
        }
    )
    level = LEVEL_SEQUENCE[local - 1]
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": number_base + local,
        "subject": "Fen Bilimleri", "grade": 6,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — {batch}. özgün üretim partisi",
        "objective": objective, "objectiveId": objective,
        "noteId": note["id"], "noteKey": note["id"],
        "question": item["stem"], "choices": choices,
        "correct": correct_position, "correctIndex": correct_position,
        "correctOption": choices[correct_position],
        "distractorWhy": [reason_map[value] for value in choices],
        "explanation": explanation, "level": level,
        "difficultyReason": (
            f"Düzey {level}; {note['title']} bilgisini {item['mode']} görevinde kullanmayı, "
            "koşulları korumayı ve üç adlandırılmış yanılgıyı ayırmayı gerektirir."
        ),
        "questionType": item["mode"],
        "familyId": f"tr-g06-bank-fen-b{batch:02d}-family-{local:03d}",
        "authoringTemplateId": f"g6-fen-b{batch:02d}-{objective.lower().replace('.', '-')}-{item['mode']}-v{local:03d}",
        "objectiveSource": note.get("objectiveSource"),
        "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [],
        "visualRequirement": "required" if figure else "none",
        "visualNeed": visual_need, "figure": figure,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    existing = [json.loads(x) for x in OUTPUT.read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(existing) != 600:
        raise RuntimeError("validated first six batches must exist before batch 07")
    notes = read_notes_only(FEN_SOURCE)
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    tasks = [item for builder in TASK_BUILDERS for item in builder()]
    if len(tasks) != 100:
        raise AssertionError(f"batch 07 must contain 100 tasks, got {len(tasks)}")
    expected_modes = {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
    if Counter(item["mode"] for item in tasks) != expected_modes:
        raise AssertionError(Counter(item["mode"] for item in tasks))
    rows = [make_record(local, item, notes[item["note"]], labels) for local, item in enumerate(tasks, 1)]
    if Counter(row["correctIndex"] for row in rows) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer positions are not exactly balanced")
    OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + rows) + "\n",
        encoding="utf-8", newline="\n",
    )
    LABELS_OUTPUT.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({
        "batch": 7, "questions": 100, "science": 100, "total": 700,
        "modes": expected_modes, "labels": len(labels), "sourceQuestionReads": 0,
        "figureSpec": "1.3.0",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
