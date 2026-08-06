#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fen notlarının eksik dört bölümünü ve görselini yazar; gövdeyi düzyazıya çevirir.

migrate_fen_22.py, 28 notun kaynakta bulunan beş bölümünü ayrıştırdı. Kalan
dördü (whatIWillLearn, priorKnowledge, summary, figureNote) kaynak metinde
yoktu ve otomatik türetilemez: "ne öğreneceğim" konunun vaadi, "ön bilgiler"
öğrencinin nereden geldiği, "özet" nelerin taşınacağı, "görselle çalışma" ise
figürün ne için bakılacağıdır. Bunlar konu anlatımının kendisidir; kavram
metninden kesip yapıştırmak dokuz bölümü doldurup hiçbirini öğretmez.

Görsel seçimi iki kurala bağlıdır:

  * Görsel, notun ANLATTIĞI ayrımı göstermeli. Bitki/hayvan hücresi bir
    karşılaştırma tablosudur çünkü not ortak ve ayırt edici yapıları
    karşılaştırır; hâl değişimi bir akıştır çünkü not geçişleri adlandırır;
    devre bir devre şemasıdır çünkü not sembolden düzeneğe geçmeyi öğretir.
  * Alt metin, görselin GÖSTERDİĞİNİ betimler, çıkarımı değil (figure_spec
    1.1.0 altTextRule). "Isı iletkenliği tablosu" demek yetmez; hangi
    kategorilerin hangi değerlerle karşılaştırıldığı yazılır.

Etiketler paket ``labels`` sözlüğüne, kimliği içerik hash'inden türetilen
anahtarlarla yazılır; böylece aynı metin iki kez farklı anahtar almaz.

Kullanım:
    python tools/finish_notes_fen.py --yaz
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from repair_turkce_release import render_lesson_body  # noqa: E402

KOK = Path(__file__).resolve().parent.parent
PAKET = KOK / "turkiye" / "5-sinif" / "fen-bilimleri" / "fen-bilimleri-tum.jsonl"

# ---------------------------------------------------------------------------
# Her not için: ne öğreneceğim · ön bilgiler · özet · görselle çalışma · figür
#
# Figür kısayolları:
#   ("tablo", [başlık...], [[hücre...], ...])
#   ("akis",  [adım...])
#   ("grafik", stil, [kategori...], [değer...], (x ekseni, y ekseni) | None)
#   ("devre", [eleman...], düzen)
# ---------------------------------------------------------------------------
NOTLAR = {
"tr-g05-fen-fb-5-1-1-1": {
 "ogrenecegim":
   "Güneş'in nasıl bir gök cismi olduğunu ve döndüğünü nereden anladığımızı "
   "öğreneceksin. Gözlediğin bir şeyle o gözlemden çıkardığın sonucu "
   "birbirinden ayırmayı da alıştırma yapacaksın.",
 "onbilgi":
   "Gök cismi, yıldız ve gezegen sözcüklerini birbirinden ayırabilmen "
   "gerekiyor; çünkü Güneş'in yıldız oluşu, ışığı kendisinin üretmesiyle "
   "açıklanacak. Bir de dönme ile dolanmanın farklı hareketler olduğunu "
   "bilmelisin, yoksa lekelerin yer değiştirmesini yanlış harekete "
   "bağlarsın.",
 "ozet":
   "Güneş, ışığını ve ısısını kendi üreten, yaklaşık küresel ve çok sıcak "
   "gazlardan oluşan bir yıldızdır. Yüzeyindeki lekelerin farklı günlerde "
   "yer değiştirmesi, Güneş'in kendi ekseni çevresinde döndüğünün "
   "gözlenebilir kanıtıdır.",
 "gorsel":
   "Tabloda solda ne gördüğümüz, sağda o gözlemden çıkan sonuç var. Her "
   "satırı okurken şunu sor: sağdaki cümle gerçekten soldakinden mi "
   "çıkıyor, yoksa ben ezberden mi ekliyorum?",
 "fig": ("tablo", ["Gözlem", "Gözlemden çıkan sonuç"], [
   ["Her yönden yuvarlak görünür", "Yaklaşık küresel biçimdedir"],
   ["Kendi ışığını ve ısısını yayar", "Bir yıldızdır, gezegen değildir"],
   ["Yüzeydeki koyu lekeler gün gün yer değiştirir",
    "Kendi ekseni çevresinde döner"],
   ["Lekelerin sayısı ve biçimi zamanla değişir",
    "Lekeler kalıcı işaretler değildir"]]),
},
"tr-g05-fen-fb-5-1-2-1": {
 "ogrenecegim":
   "Ay'ın hangi özelliklerinin doğrudan gözlenebildiğini, hangilerinin "
   "gözlemden çıkarım yaparak bulunduğunu öğreneceksin. Ay'ın iki ayrı "
   "hareketini de birbirinden ayıracaksın.",
 "onbilgi":
   "Uydu kavramını ve bir cismin hem kendi çevresinde dönüp hem başka bir "
   "cismin çevresinde dolanabileceğini bilmelisin. Ay'ın hep aynı yüzünü "
   "görmemiz ancak bu ikisi birlikte düşünüldüğünde anlaşılır.",
 "ozet":
   "Ay, Dünya'nın doğal uydusudur; kendi ışığını üretmez, Güneş ışığını "
   "yansıtır. Hem kendi ekseni çevresinde döner hem Dünya çevresinde "
   "dolanır. Hep aynı yüzünü görmemiz Ay'ın dönmediğini değil, iki "
   "hareketinin birbirine denk sürelerde olduğunu gösterir.",
 "gorsel":
   "Tabloda sol sütun gözle görülebilen şeyler, sağ sütun ise bunlardan "
   "çıkan sonuçlar. Sol sütundaki hiçbir satırın 'Ay ışık üretmez' demediğine "
   "dikkat et; bu bir gözlem değil, çıkarımdır.",
 "fig": ("tablo", ["Gözlenen", "Çıkarılan"], [
   ["Geceleri parlak görünür", "Üzerine düşen ışığı yansıtır"],
   ["Yüzeyinde koyu ve açık bölgeler var", "Yüzeyi her yerde aynı değildir"],
   ["Yüzeyde geniş çukurlar var", "Çarpmalarla krater oluşmuştur"],
   ["Gökyüzündeki konumu gecelere göre değişir",
    "Dünya çevresinde dolanır"],
   ["Hep aynı yüzünü görürüz",
    "Dönme ve dolanma süreleri birbirine denktir"]]),
},
"tr-g05-fen-fb-5-1-2-2": {
 "ogrenecegim":
   "Ay'ın evrelerinin neden oluştuğunu ve dört ana evrenin nasıl "
   "adlandırıldığını öğreneceksin. Evre ile tutulmanın neden ayrı olaylar "
   "olduğunu da göreceksin.",
 "onbilgi":
   "Ay'ın Dünya çevresinde dolandığını ve ışığı yansıttığını bilmen gerekiyor. "
   "Bir topu ışık kaynağının çevresinde gezdirdiğinde aydınlık yarısının hep "
   "var olduğunu ama senin farklı miktarını gördüğünü fark etmek, bu konunun "
   "anahtarıdır.",
 "ozet":
   "Güneş, Ay'ın her zaman yaklaşık yarısını aydınlatır. Değişen şey "
   "aydınlanan miktar değil, o aydınlık yarının Dünya'dan görebildiğimiz "
   "bölümüdür. Bu yüzden evreler gölgeyle değil, konumla açıklanır.",
 "gorsel":
   "Tabloda her evrenin yanında Ay'ın Güneş'e göre nerede olduğu ve o konumda "
   "ne kadarını gördüğümüz yazıyor. Aydınlanan yarının hiçbir satırda "
   "değişmediğine dikkat et — değişen yalnız bizim görebildiğimiz.",
 "fig": ("tablo", ["Evre", "Ay'ın konumu", "Görünen aydınlık bölüm"], [
   ["Yeni ay", "Dünya ile Güneş arasına yakın", "Yok denecek kadar az"],
   ["İlk dördün", "Dolanmanın çeyreğinde", "Yarısı"],
   ["Dolunay", "Dünya'nın Güneş'e göre arka yanında", "Tamamı"],
   ["Son dördün", "Dolanmanın dörtte üçünde", "Yarısı, ters yandan"]]),
},
"tr-g05-fen-fb-5-1-3-1": {
 "ogrenecegim":
   "Güneş, Dünya ve Ay'ı gösteren bir modeli nasıl kuracağını ve bir modelin "
   "neyi başarıp neyi başaramayacağını öğreneceksin.",
 "onbilgi":
   "Üç gök cisminin türlerini (yıldız, gezegen, uydu) ve hareketlerini "
   "bilmelisin. Modelin amacına göre değerlendirileceğini anlamak için de "
   "'bu model neyi açıklamak için yapıldı?' sorusunu sormaya alışık olmalısın.",
 "ozet":
   "Model, gerçeğin seçilmiş özelliklerini gösteren bir temsildir. Güneş, "
   "Dünya ve Ay modelinde büyüklük sırası, biçim ve hareket ilişkileri "
   "gösterilebilir. Bir modelin başarısı gerçeğe ne kadar benzediğiyle değil, "
   "belirlenen amaca hizmet edip etmediğiyle ölçülür.",
 "gorsel":
   "Akış, bir model kurarken izlenen sırayı gösteriyor. En baştaki adımın "
   "'amacı belirle' olması rastlantı değil: amaç seçilmeden hangi malzemenin "
   "uygun olduğuna karar verilemez.",
 "fig": ("akis", [
   "Amacı belirle: büyüklük mü, hareket mi gösterilecek?",
   "Amaca uygun malzemeyi seç",
   "Her temsilin anlamını bir anahtarla yaz",
   "Hareketleri ok ile göster: dönme ekseni, dolanma yolu",
   "Modelin neyi gösteremediğini not et"]),
},
"tr-g05-fen-fb-5-2-1-1": {
 "ogrenecegim":
   "Kuvvetin ne olduğunu, dinamometreyle nasıl ölçüldüğünü ve neden newton "
   "birimiyle yazıldığını öğreneceksin.",
 "onbilgi":
   "İtme ve çekmenin birer etkileşim olduğunu bilmelisin. Ölçek okumayı, yani "
   "iki çizgi arasındaki aralığın kaç birim ettiğini bulmayı da bilmen "
   "gerekiyor; dinamometre okumak bunun aynısıdır.",
 "ozet":
   "Kuvvet, cisimler arasındaki itme ya da çekmedir; cismin hareketini veya "
   "şeklini değiştirebilir. Büyüklüğü dinamometreyle ölçülür ve newton (N) "
   "ile yazılır. Dinamometre, yayın kuvvet arttıkça belirli sınırlar içinde "
   "daha çok uzaması ilkesiyle çalışır.",
 "gorsel":
   "Tabloda aynı yayın farklı kuvvetler altındaki uzamaları var. Kuvvet iki "
   "katına çıkınca uzamanın nasıl değiştiğine bak; sonra son satıra dikkat et, "
   "orada yayın sınırı aşılmış.",
 "fig": ("tablo", ["Asılan kuvvet (N)", "Yayın uzaması (cm)", "Durum"], [
   ["1", "2", "Yay sınırı içinde"],
   ["2", "4", "Yay sınırı içinde"],
   ["3", "6", "Yay sınırı içinde"],
   ["8", "20", "Yay kalıcı biçimde uzamış, ölçüm geçersiz"]]),
},
"tr-g05-fen-fb-5-2-1-2": {
 "ogrenecegim":
   "Kendi dinamometreni nasıl tasarlayacağını ve ölçeğini nasıl "
   "işaretleyeceğini öğreneceksin.",
 "onbilgi":
   "Kuvvetin newton ile ölçüldüğünü ve yayın kuvvetle uzadığını bilmelisin. "
   "Bir de 'kalibrasyon' fikrine hazır olmalısın: bir aracın çizgileri, "
   "bilinen yüklerle karşılaştırılarak anlam kazanır.",
 "ozet":
   "Dinamometre tasarımı, kuvvet ile uzama arasındaki ilişkiyi bir ölçeğe "
   "çevirme işidir. Eşit aralıklı çizgiler tek başına doğru ölçüm sağlamaz; "
   "hangi çizginin hangi kuvvete karşılık geldiği bilinen yüklerle "
   "belirlenmelidir. Her yayın bir üst sınırı vardır.",
 "gorsel":
   "Akıştaki 'bilinen yüklerle işaretle' adımını atlarsan elinde çizgili ama "
   "hiçbir şey ölçmeyen bir araç kalır. Sırayı bu yüzden takip et.",
 "fig": ("akis", [
   "Kullanım amacını ve ölçülecek kuvvet aralığını yaz",
   "Amaca uygun yayı ve güvenli gövdeyi seç",
   "Yüksüz hâldeki gösterge konumunu sıfır olarak işaretle",
   "Bilinen yüklerle ölçeği işaretle (kalibrasyon)",
   "Yayın kalıcı uzadığı noktayı bul, üst sınır olarak yaz"]),
},
"tr-g05-fen-fb-5-2-2-1": {
 "ogrenecegim":
   "Kütle ile ağırlığın neden farklı büyüklükler olduğunu, hangi araçla "
   "ölçüldüklerini ve hangi birimle yazıldıklarını öğreneceksin.",
 "onbilgi":
   "Kuvvetin newton ile ölçüldüğünü ve dinamometreyle bulunduğunu bilmelisin. "
   "Yer çekiminin bir kuvvet olduğunu ve gök cismine göre değiştiğini de "
   "bilmen gerekiyor; ağırlığın Ay'da değişmesi buna dayanıyor.",
 "ozet":
   "Kütle, cismin madde miktarıyla ilgilidir; terazi ile ölçülür, birimi "
   "gram ve kilogramdır ve gittiğin yere göre değişmez. Ağırlık, gök cisminin "
   "uyguladığı çekim kuvvetidir; dinamometre ile ölçülür, birimi newtondur ve "
   "gök cismine göre değişir.",
 "gorsel":
   "Tablodaki dört satırı sütun sütun karşılaştır. Son satır işin can alıcı "
   "yeri: aynı cisim Ay'a götürüldüğünde hangi sütun değişiyor, hangisi "
   "değişmiyor?",
 "fig": ("tablo", ["Karşılaştırma", "Kütle", "Ağırlık"], [
   ["Ne ile ilgili", "Madde miktarı", "Yer çekimi kuvveti"],
   ["Ölçüm aracı", "Terazi", "Dinamometre"],
   ["Birimi", "Gram, kilogram", "Newton"],
   ["Ay'a götürülünce", "Değişmez", "Azalır"]]),
},
"tr-g05-fen-fb-5-2-3-1": {
 "ogrenecegim":
   "Sürtünme kuvvetinin harekete nasıl etki ettiğini ve bunu adil bir deneyle "
   "nasıl inceleyeceğini öğreneceksin.",
 "onbilgi":
   "Kuvvetin hareketi değiştirebildiğini bilmelisin. Adil deney fikrine de "
   "hazır olmalısın: yalnız bir değişkeni değiştirip geri kalanını sabit "
   "tutmak, sonucu neye bağlayacağını belirler.",
 "ozet":
   "Sürtünme, temas eden yüzeylerin göreli hareketine karşı koyan kuvvettir "
   "ve genellikle hareketin tersi yönde etki eder. Yüzeylerin pürüzlülüğü "
   "arttıkça etkisi büyür. Sürtünme varsa cisim hemen durmaz; yavaşlar.",
 "gorsel":
   "Grafikte aynı arabanın üç farklı yüzeyde kaç santimetre sonra durduğu "
   "var. Sütunların yüksekliğini karşılaştırırken şunu düşün: kısa sütun "
   "büyük sürtünme mi demek, küçük sürtünme mi?",
 "fig": ("grafik", "bar",
   ["Halı", "Ahşap zemin", "Buzlu yüzey"], [40, 120, 260],
   ("Yüzey türü", "Durma mesafesi (cm)")),
},
"tr-g05-fen-fb-5-2-3-2": {
 "ogrenecegim":
   "Günlük yaşamda sürtünmenin ne zaman artırılıp ne zaman azaltıldığını, "
   "hangi yöntemlerin kullanıldığını öğreneceksin.",
 "onbilgi":
   "Sürtünmenin temas eden yüzeyler arasında oluştuğunu ve pürüzlülükle "
   "ilgili olduğunu bilmelisin. Bir de problemi 'tutunmak mı, kolay hareket "
   "mi?' diye ayırt edebilmelisin; çözüm bu ayrımdan çıkıyor.",
 "ozet":
   "Tutunmak, durmak ya da kaymayı önlemek gerekiyorsa sürtünme artırılır; "
   "hareketi kolaylaştırmak ya da aşınmayı azaltmak gerekiyorsa azaltılır. "
   "Hiçbir yöntem sürtünmeyi sıfıra indirmez.",
 "gorsel":
   "Tabloda solda günlük bir sorun, ortada ne yapılması gerektiği, sağda "
   "yöntem var. Orta sütunu kapatıp kendin doldurmayı dene.",
 "fig": ("tablo", ["Durum", "Ne gerekir", "Yöntem"], [
   ["Ayakkabı ıslak zeminde kayıyor", "Sürtünmeyi artırmak",
    "Tabana girintili desen"],
   ["Ağır kutu zeminde zor ilerliyor", "Sürtünmeyi azaltmak",
    "Altına tekerlek takmak"],
   ["Bisiklet yokuşta durmuyor", "Sürtünmeyi artırmak",
    "Fren balatasını sıkmak"],
   ["Kapı menteşesi gıcırdıyor", "Sürtünmeyi azaltmak", "Yağlamak"]]),
},
"tr-g05-fen-fb-5-3-1-1": {
 "ogrenecegim":
   "Bitki ve hayvan hücrelerinin hangi yapıları ortak taşıdığını, hangilerinin "
   "ayırt edici olduğunu öğreneceksin.",
 "onbilgi":
   "Hücrenin canlıların temel yapı birimi olduğunu bilmelisin. Bir de "
   "'ortak yapı' ile 'ayırt edici yapı' arasındaki farkı kavramalısın: "
   "ikisini karıştırırsan tabloyu yanlış okursun.",
 "ozet":
   "Hücre zarı, sitoplazma ve çekirdek her iki hücrede de bulunur. Hücre "
   "duvarı ve kloroplast bitki hücresinin ayırt edici yapılarıdır. Hücrenin "
   "biçimi bulunduğu dokuya göre değişir; kitaplardaki düzenli şekiller "
   "öğretim amaçlı çizimlerdir.",
 "gorsel":
   "Tabloda her yapının iki hücrede bulunup bulunmadığı yazıyor. İki sütunun "
   "da 'var' dediği satırlar ortak yapıları, yalnız birinin 'var' dediği "
   "satırlar ayırt edici yapıları gösterir.",
 "fig": ("tablo", ["Yapı", "Bitki hücresi", "Hayvan hücresi"], [
   ["Hücre zarı", "Var", "Var"],
   ["Sitoplazma", "Var", "Var"],
   ["Çekirdek", "Var", "Var"],
   ["Hücre duvarı", "Var", "Yok"],
   ["Kloroplast", "Var", "Yok"]]),
},
"tr-g05-fen-fb-5-3-1-2": {
 "ogrenecegim":
   "Çok hücreli bir canlıda hücreden organizmaya kadar uzanan yapı "
   "düzeylerini sırayla öğreneceksin.",
 "onbilgi":
   "Hücrenin temel yapı birimi olduğunu bilmelisin. Zinciri kurarken hep aynı "
   "canlı üzerinden gitmen gerektiğini de aklında tut; örnekleri karıştırmak "
   "en sık yapılan hatadır.",
 "ozet":
   "Sıralama küçükten büyüğe hücre, doku, organ, sistem ve organizmadır. "
   "Benzer hücreler doku, farklı dokular organ, birlikte çalışan organlar "
   "sistem oluşturur. Organizma tek bir organın büyümüş hâli değil, "
   "sistemlerin uyumlu birlikteliğidir.",
 "gorsel":
   "Akıştaki her ok 'bir araya gelince' demek. Okları tersten okuyup "
   "büyükten küçüğe de inebilmelisin.",
 "fig": ("akis", ["Hücre", "Doku", "Organ", "Sistem", "Organizma"]),
},
"tr-g05-fen-fb-5-3-2-1": {
 "ogrenecegim":
   "Kemik, eklem ve kasın hareketi birlikte nasıl sağladığını öğreneceksin.",
 "onbilgi":
   "Kuvvetin hareketi başlatabildiğini bilmelisin, çünkü hareketi üreten "
   "kuvvet kaslardan gelir. Vücudunda dirsek ve diz gibi eklemlerin nerede "
   "olduğunu göstererek başlayabilirsin.",
 "ozet":
   "Kemikler destek sağlar, iç organları korur ve kaslara tutunma yüzeyi "
   "verir. Eklemler kemiklerin birleştiği ve hareketin gerçekleştiği "
   "bölgelerdir. Kaslar kasılıp gevşeyerek kemikleri çeker. Hareketi kemikler "
   "değil, kaslar üretir.",
 "gorsel":
   "Tabloda her yapının görevi yazıyor. Kolunu bükerken üç satırın da aynı "
   "anda çalıştığını fark et: hiçbiri tek başına hareket üretmiyor.",
 "fig": ("tablo", ["Yapı", "Görevi", "Kolu bükerken"], [
   ["Kemik", "Destek verir, organları korur", "Ön kol kemiği yer değiştirir"],
   ["Eklem", "İki kemiğin birleştiği yer", "Dirsek eklemi hareketi sağlar"],
   ["Kas", "Kasılıp gevşeyerek kemiği çeker",
    "Kol kası kasılır ve kemiği çeker"]]),
},
"tr-g05-fen-fb-5-3-2-2": {
 "ogrenecegim":
   "Destek ve hareket sistemini korumak için hangi alışkanlıkların işe "
   "yaradığını, tek bir besin ya da tek bir hareketin neden yetmediğini "
   "öğreneceksin.",
 "onbilgi":
   "Kemik, eklem ve kasın görevlerini bilmelisin. Bir de 'genel korunma "
   "önerisi' ile 'kişisel sağlık değerlendirmesi' arasındaki farkı ayırt "
   "edebilmelisin; ikincisi için uzmana gidilir.",
 "ozet":
   "Sağlık; dengeli beslenme, yaşa uygun düzenli hareket, doğru duruş, "
   "güvenlik önlemleri ve yeterli dinlenmenin birlikteliğine bağlıdır. Tek "
   "bir besine ya da tek bir egzersize aşırı anlam yüklemek yanlıştır.",
 "gorsel":
   "Tabloda solda alışkanlık, sağda neye katkı sağladığı var. Hiçbir satırın "
   "tek başına 'kemikler zarar görmez' demediğine dikkat et.",
 "fig": ("tablo", ["Alışkanlık", "Neye katkı sağlar"], [
   ["Dengeli beslenme", "Kemik ve kas gelişimi için gerekli besin ögeleri"],
   ["Yaşa uygun düzenli hareket", "Kas gücü, denge ve esneklik"],
   ["Çantayı iki omuza dengeli asmak", "Omurgaya binen yükün dağılması"],
   ["Etkinlik öncesi ısınma", "Ani zorlanmadan kaynaklanan yaralanma riski"],
   ["Yeterli dinlenme", "Yüklenen dokuların onarımı"]]),
},
"tr-g05-fen-fb-5-4-1-1": {
 "ogrenecegim":
   "Işığın doğrusal yayıldığını bir deneyle nasıl göstereceğini ve bu sözün "
   "tam olarak ne anlama geldiğini öğreneceksin.",
 "onbilgi":
   "Işık kaynağı kavramını bilmelisin. Bir de deneyde 'sabit tutulan' ile "
   "'değiştirilen' arasındaki farka dikkat etmelisin; kartların hizası burada "
   "değiştirilen değişkendir.",
 "ozet":
   "Işık kaynaktan her yöne yayılır; doğrusal olan, her bir yöndeki ışık "
   "yoludur. Üç kartondaki delikler aynı doğrultuya getirildiğinde ekranda "
   "ışık görülür, biri kaydırıldığında görülmez. Bu, ışığın köşe dönmediğini "
   "gösterir.",
 "gorsel":
   "Akış deneyin sırasını gösteriyor. Son iki adım birbirinin karşılaştırması: "
   "biri olmadan öbürü hiçbir şey kanıtlamaz.",
 "fig": ("akis", [
   "Üç kartona aynı yükseklikte delik aç",
   "Kartonları arka arkaya dik yerleştir",
   "El fenerini birinci deliğin önüne koy",
   "Delikler aynı doğrultudayken ekrana bak: ışık görünür",
   "Ortadaki kartonu kaydır ve tekrar bak: ışık görünmez"]),
},
"tr-g05-fen-fb-5-4-2-1": {
 "ogrenecegim":
   "Maddeleri ışığı geçirme durumlarına göre saydam, yarı saydam ve opak "
   "diye nasıl sınıflandıracağını öğreneceksin.",
 "onbilgi":
   "Işığın doğrusal yayıldığını bilmelisin. Adil karşılaştırma için aynı ışık "
   "kaynağını ve aynı uzaklığı kullanman gerektiğini de aklında tut.",
 "ozet":
   "Saydam madde ışığın büyük bölümünü geçirir ve arkası net görünür. Yarı "
   "saydam madde ışığı geçirir ama dağıttığı için görüntü bulanıklaşır. Opak "
   "madde ışığı geçirmez. Sınıflandırma renge göre değil, ışığın geçişine "
   "göre yapılır.",
 "gorsel":
   "Tabloda her maddenin ışığı ne kadar geçirdiği ve arkasının nasıl "
   "göründüğü var. Renkli ama saydam olan satırla renksiz ama yarı saydam "
   "olan satırı yan yana koy: renk sınıfı belirlemiyor.",
 "fig": ("tablo", ["Madde", "Işığı geçirme", "Arkasındaki cisim"], [
   ["Temiz pencere camı", "Büyük bölümünü geçirir", "Net görünür"],
   ["Renkli şeffaf plastik", "Büyük bölümünü geçirir", "Net görünür"],
   ["Buzlu cam", "Bir bölümünü geçirir", "Bulanık görünür"],
   ["Yağlı kâğıt", "Bir bölümünü geçirir", "Bulanık görünür"],
   ["Karton", "Geçirmez", "Görünmez"]]),
},
"tr-g05-fen-fb-5-4-3-1": {
 "ogrenecegim":
   "Tam gölgenin nasıl oluştuğunu ve boyutunun neye bağlı olarak "
   "değiştiğini öğreneceksin.",
 "onbilgi":
   "Işığın doğrusal yayıldığını ve opak cismin ışığı geçirmediğini bilmelisin. "
   "Bir de bir deneyde tek değişkeni değiştirmeyi: burada değişen, cismin "
   "kaynağa uzaklığıdır.",
 "ozet":
   "Tam gölge, opak bir cismin ışığı engellemesiyle yüzeyde oluşan "
   "aydınlanmamış bölgedir. Gölge cismin içinden çıkan bir görüntü değildir. "
   "Cisim ışık kaynağına yaklaştırıldığında gölge büyür.",
 "gorsel":
   "Grafikte cisim kaynağa yaklaştıkça gölge boyunun nasıl değiştiği var. "
   "Sol uçtaki değerle sağ uçtakini karşılaştır; aradaki fark cismin kendi "
   "boyundan büyük mü?",
 "fig": ("grafik", "line",
   ["10 cm", "20 cm", "30 cm", "40 cm"], [24, 14, 10, 8],
   ("Cismin kaynağa uzaklığı", "Gölge boyu (cm)")),
},
"tr-g05-fen-fb-5-5-1-1": {
 "ogrenecegim":
   "Maddenin taneciklerden oluştuğunu ve katı, sıvı, gaz hâllerinde bu "
   "taneciklerin nasıl farklı durduğunu öğreneceksin.",
 "onbilgi":
   "Maddenin üç hâlini ve gözlenebilir özelliklerini (şeklini koruma, kabın "
   "şeklini alma) bilmelisin. Bir de modelin gerçeğin kendisi olmadığını: "
   "çizdiğimiz noktalar tanecikleri temsil eder, tanecik değildir.",
 "ozet":
   "Bütün maddeler taneciklerden oluşur. Aynı madde için tanecik türü hâlden "
   "hâle değişmez; değişen, tanecikler arasındaki uzaklık, düzen ve hareket "
   "biçimidir. Katı tanecikleri de durmaz, yerinde titreşir.",
 "gorsel":
   "Tabloda üç hâlin tanecik düzeni karşılaştırılıyor. Katı satırındaki "
   "'titreşir' sözcüğüne dikkat et: hareketsiz demiyor.",
 "fig": ("tablo", ["Hâl", "Tanecikler arası uzaklık", "Düzen", "Hareket"], [
   ["Katı", "Çok yakın", "Düzenli", "Yerinde titreşir"],
   ["Sıvı", "Yakın", "Daha az düzenli", "Birbiri üzerinden kayar"],
   ["Gaz", "Çok uzak", "Düzensiz", "Her yöne serbestçe hareket eder"]]),
},
"tr-g05-fen-fb-5-5-2-1": {
 "ogrenecegim":
   "Isı ile sıcaklığın neden farklı kavramlar olduğunu, hangisinin neyle "
   "ölçüldüğünü öğreneceksin.",
 "onbilgi":
   "Termometre okumayı bilmelisin. Bir de enerjinin bir yerden başka bir yere "
   "aktarılabildiği fikrine hazır olmalısın; ısı tam olarak bu aktarımdır.",
 "ozet":
   "Sıcaklık, bir maddenin ne kadar sıcak olduğunu gösteren ölçülebilir "
   "büyüklüktür; termometreyle ölçülür, birimi °C'dir. Isı, sıcaklık farkı "
   "nedeniyle aktarılan enerjidir; birimi joule'dür. Bir cisimde 'ısı "
   "bulunmaz', ısı aktarılır.",
 "gorsel":
   "Tabloyu sütun sütun oku. Son satır ayrımın özü: sıcaklık cismin bir "
   "özelliği, ısı ise iki cisim arasında olan bir şey.",
 "fig": ("tablo", ["Karşılaştırma", "Sıcaklık", "Isı"], [
   ["Ne anlatır", "Ne kadar sıcak olduğunu", "Aktarılan enerjiyi"],
   ["Ölçüm aracı", "Termometre", "Doğrudan ölçülmez, hesaplanır"],
   ["Birimi", "Santigrat derece (°C)", "Joule (J)"],
   ["Nerede bulunur", "Cismin kendi özelliğidir",
    "İki cisim arasında aktarılır"]]),
},
"tr-g05-fen-fb-5-5-2-2": {
 "ogrenecegim":
   "Sıcaklıkları farklı iki madde temas ettiğinde ne olduğunu ve ısının hangi "
   "yöne aktığını öğreneceksin.",
 "onbilgi":
   "Isı ile sıcaklığın farkını bilmelisin. Bir de ortalama almanın her zaman "
   "geçerli olmadığını: eşit miktarda olmayan sıvılarda son sıcaklık iki "
   "değerin tam ortası çıkmaz.",
 "ozet":
   "Isı, sıcaklığı yüksek maddeden düşük olana aktarılır. Sıcak madde soğur, "
   "soğuk madde ısınır ve süreç sıcaklıklar eşitlenene kadar sürer. Son "
   "sıcaklık iki başlangıç değerinin arasındadır.",
 "gorsel":
   "Tabloda iki deneme var. Birincide miktarlar eşit, ikincide değil. Son "
   "sıcaklığın hangi denemede tam ortada çıktığına bak.",
 "fig": ("tablo",
   ["Deneme", "Sıcak su", "Soğuk su", "Son sıcaklık"], [
   ["1: eşit miktar", "100 mL, 40 °C", "100 mL, 20 °C", "Yaklaşık 30 °C"],
   ["2: farklı miktar", "50 mL, 40 °C", "150 mL, 20 °C", "Yaklaşık 25 °C"]]),
},
"tr-g05-fen-fb-5-5-3-1": {
 "ogrenecegim":
   "Maddenin hâlleri arasındaki geçişlerin adlarını ve her geçişte ısının "
   "hangi yöne gittiğini öğreneceksin.",
 "onbilgi":
   "Maddenin üç hâlini bilmelisin. Isının alınıp verilebildiğini de bilmen "
   "gerekiyor; geçişleri ayıran ölçüt tam olarak budur.",
 "ozet":
   "Hâl değişiminde maddenin kimliği değişmez, yalnız fiziksel hâli değişir. "
   "Erime ve buharlaşmada madde ısı alır; donma ve yoğuşmada ısı verir. "
   "Buharlaşma yalnız kaynama sıcaklığında olmaz.",
 "gorsel":
   "Akıştaki oklar iki yönlü okunmalı: sağa giderken madde ısı alıyor, sola "
   "dönerken ısı veriyor. Geçişin adını okun yönü belirliyor.",
 "fig": ("akis", [
   "Katı", "Erime: ısı alır", "Sıvı", "Buharlaşma: ısı alır", "Gaz",
   "Yoğuşma: ısı verir", "Sıvı (geri dönüş)", "Donma: ısı verir",
   "Katı (geri dönüş)"]),
},
"tr-g05-fen-fb-5-5-4-1": {
 "ogrenecegim":
   "Maddelerin ısıyı neden farklı hızlarda aktardığını ve iletken ile "
   "yalıtkanı nasıl ayırt edeceğini öğreneceksin.",
 "onbilgi":
   "Isının sıcaktan soğuğa aktarıldığını bilmelisin. Adil deney için "
   "çubukların aynı uzunlukta ve kalınlıkta olması gerektiğini de aklında tut.",
 "ozet":
   "Isı iletkenliği, maddenin ısı aktarımına ne ölçüde izin verdiğidir. "
   "Metaller genellikle iyi iletkendir; tahta, plastik ve durgun hava daha "
   "yavaş aktarır. 'Yalıtkan' sözcüğü 'hiç geçirmez' demek değildir.",
 "gorsel":
   "Grafikte aynı sürede üç çubuğun serbest ucunda ölçülen sıcaklık artışı "
   "var. En düşük sütunun sıfır olmadığına dikkat et: tahta da ısı aktarıyor, "
   "yalnız yavaş.",
 "fig": ("grafik", "bar",
   ["Metal çubuk", "Plastik çubuk", "Tahta çubuk"], [18, 6, 3],
   ("Çubuğun maddesi", "5 dakikada sıcaklık artışı (°C)")),
},
"tr-g05-fen-fb-5-5-4-2": {
 "ogrenecegim":
   "Isı yalıtımının ne işe yaradığını ve bir yalıtım tasarımını nasıl "
   "değerlendireceğini öğreneceksin.",
 "onbilgi":
   "İyi iletken ile yalıtkan maddeleri ayırt edebilmelisin. Bir de bir "
   "tasarımın başarısını ölçmek için önce başarı ölçütü yazman gerektiğini.",
 "ozet":
   "Yalıtım, iki ortam arasındaki ısı aktarımını yavaşlatır; durdurmaz. "
   "Hareketsiz hava tabakaları iyi yalıtım sağlar, çift cam bu yüzden "
   "kullanılır. Yalıtımlı kapta da sıcaklık zamanla değişir, yalnız daha "
   "yavaş.",
 "gorsel":
   "Grafikte iki kapta suyun sıcaklığı zamanla nasıl düşmüş, yan yana var. "
   "Yalıtımlı kabın çizgisinin de indiğine dikkat et — yalnız daha yavaş.",
 "fig": ("grafik", "line",
   ["0 dk", "10 dk", "20 dk", "30 dk"], [50, 44, 39, 35],
   ("Geçen süre", "Yalıtımlı kapta sıcaklık (°C)")),
},
"tr-g05-fen-fb-5-6-1-1": {
 "ogrenecegim":
   "Basit bir elektrik devresinin elemanlarını ve her elemanın sembolünü "
   "öğreneceksin.",
 "onbilgi":
   "Bir şeyin çalışması için kesintisiz bir yol gerektiği fikrine hazır "
   "olmalısın. Sembol kavramını da bilmelisin: sembol, nesnenin resmi değil, "
   "üzerinde anlaşılmış bir işaretidir.",
 "ozet":
   "Basit devrede pil enerji sağlar, ampul ışığa çevirir, kablolar iletken "
   "yolu kurar, anahtar yolu açıp kapatır. Devrenin çalışması için yolun "
   "kesintisiz olması gerekir. Şemadaki çizgi uzunluğu parlaklığı etkilemez.",
 "gorsel":
   "Şemada dört eleman seri bağlı. Pilin bir kutbundan çıkıp ampulden ve "
   "anahtardan geçerek öbür kutba dönen yolu parmağınla izle; yol kesilirse "
   "ampul yanmaz.",
 "fig": ("devre", ["battery", "lamp", "switch", "wire"], "series"),
},
"tr-g05-fen-fb-5-6-1-2": {
 "ogrenecegim":
   "Bir devre şemasından gerçek devreyi nasıl kuracağını ve kurduğun devreyi "
   "nasıl deneyeceğini öğreneceksin.",
 "onbilgi":
   "Devre elemanlarını ve sembollerini bilmelisin. Bir de açık devre ile "
   "kapalı devre arasındaki farkı; ampul yanmadığında ilk bakacağın yer "
   "budur.",
 "ozet":
   "Şemadan gerçeğe geçerken eleman sayısı, bağlantı sırası ve devrenin açık "
   "mı kapalı mı olduğu korunmalıdır. Ampul yanmıyorsa çözüm pil eklemek "
   "değil, yolun nerede kesildiğini bulmaktır.",
 "gorsel":
   "Şemada iki ampul ve bir anahtar seri bağlı. Anahtar açıkken yolun "
   "kesildiğini ve iki ampulün birden söndüğünü düşün; seri bağlamanın "
   "anlamı budur.",
 "fig": ("devre", ["battery", "lamp", "lamp", "switch", "wire"], "series"),
},
"tr-g05-fen-fb-5-6-2-1": {
 "ogrenecegim":
   "Bir ampulün parlaklığını hangi değişkenlerin etkilediğini ve bunu adil "
   "bir deneyle nasıl sınayacağını öğreneceksin.",
 "onbilgi":
   "Basit devre kurmayı ve seri bağlamayı bilmelisin. Adil deneyde tek "
   "değişkenin değiştirildiğini de bilmen gerekiyor; bu konunun asıl sınavı "
   "budur.",
 "ozet":
   "Ampul sayısı sabitken seri pil sayısı artarsa parlaklık genellikle artar. "
   "Pil sayısı sabitken seri ampul sayısı artarsa her ampulün parlaklığı "
   "azalır. İki değişken aynı anda değiştirilirse sonuç hiçbirine "
   "bağlanamaz.",
 "gorsel":
   "Tablodaki dört denemeden hangileri karşılaştırılabilir? Yalnız tek bir "
   "sütunu farklı olan satır çiftlerini bul; ötekiler adil deney değil.",
 "fig": ("tablo", ["Deneme", "Pil sayısı", "Ampul sayısı", "Parlaklık"], [
   ["1", "1", "1", "Orta"],
   ["2", "2", "1", "Yüksek"],
   ["3", "1", "2", "Düşük"],
   ["4", "2", "3", "Düşük"]]),
},
"tr-g05-fen-fb-5-7-1-1": {
 "ogrenecegim":
   "Evsel atıkları hangi sorulara bakarak sınıflandıracağını öğreneceksin.",
 "onbilgi":
   "Kâğıt, cam, metal ve plastiği görerek ayırt edebilmelisin. Bir de "
   "ambalajın birden çok malzemeden yapılabileceğini: bu, sınıflandırmayı "
   "zorlaştıran asıl durumdur.",
 "ozet":
   "Sınıflandırmada önce malzeme türüne, sonra temizlik durumuna, sonra "
   "ambalajın tek mi çok mu malzemeli olduğuna ve yerel toplama kurallarına "
   "bakılır. Yemekle kirlenmiş kâğıt geri dönüşüme uygun olmayabilir.",
 "gorsel":
   "Akış bir karar sırası. Her adımda 'evet' ya da 'hayır' diyerek ilerle; "
   "üstteki soruyu atlayıp alttan başlarsan yanlış kutuya atarsın.",
 "fig": ("akis", [
   "Bu ürün hangi temel malzemeden yapılmış?",
   "Tek malzemeden mi, birden çok malzemeden mi?",
   "Yemekle ya da yağla kirlenmiş mi?",
   "Yerel toplama kuralları bunu hangi kutuya yazıyor?",
   "Uygun kutuya at"]),
},
"tr-g05-fen-fb-5-7-1-2": {
 "ogrenecegim":
   "Geri dönüşümün ne olduğunu, neyi azalttığını ve neden tek başına yeterli "
   "olmadığını öğreneceksin.",
 "onbilgi":
   "Atıkların malzemeye göre ayrıldığını bilmelisin. Bir de bir işlemin "
   "kendisinin de kaynak harcadığı fikrine hazır olmalısın; geri dönüşümün "
   "sınırı buradan çıkıyor.",
 "ozet":
   "Geri dönüşüm, uygun atıkların işlenerek yeniden kullanılabilir malzemeye "
   "dönüştürülmesidir. Bazı kaynak ihtiyacını ve atık miktarını azaltabilir, "
   "ama kendisi de kaynak harcar. En etkili adım atığı hiç oluşturmamaktır.",
 "gorsel":
   "Akış en etkiliden en az etkiliye doğru sıralı. En üstteki adımın "
   "'gerekli mi?' olması boşuna değil: oluşmamış atık işlenmeyi de "
   "gerektirmez.",
 "fig": ("akis", [
   "Önle: bu ürün gerçekten gerekli mi?",
   "Yeniden kullan: eldeki ürün kullanılabilir mi?",
   "Ayrı topla: malzemesine göre doğru kutuya",
   "Geri dönüştür: işlenerek yeni malzemeye",
   "Uygun bertaraf: kalanı güvenli biçimde"]),
},
"tr-g05-fen-fb-5-7-1-3": {
 "ogrenecegim":
   "Bir atık yönetimi planının hangi adımlardan oluştuğunu ve başarısının "
   "nasıl ölçüleceğini öğreneceksin.",
 "onbilgi":
   "Atıkların sınıflandırılmasını ve geri dönüşüm basamaklarını bilmelisin. "
   "Bir de bir planın ölçülebilir bir hedefi olması gerektiğini: 'daha çok "
   "toplayalım' ölçülebilir bir hedef değildir.",
 "ozet":
   "Atık yönetimi, önleme ve azaltmadan başlayıp yeniden kullanım, kaynağında "
   "ayrı toplama, güvenli taşıma ve uygun bertarafa uzanan bir süreçtir. "
   "Toplanan miktarın artması tek başına başarı göstergesi değildir; "
   "tüketimin arttığını da gösterebilir.",
 "gorsel":
   "Akış bir plan kurma sırası. Son adımın 'ölç ve gözden geçir' olması "
   "önemli: ölçmediğin bir planın işe yarayıp yaramadığını bilemezsin.",
 "fig": ("akis", [
   "Mevcut durumu ölç: bir hafta boyunca say",
   "Sorunu kesinleştir: hangi atık nereye yanlış gidiyor?",
   "Ölçülebilir hedef yaz",
   "Uygulanabilir adımları belirle ve görev dağıt",
   "Ölç ve gözden geçir: hedefe ulaşıldı mı?"]),
},
}


def anahtar(not_id: str, metin: str) -> str:
    ozet = hashlib.sha256(metin.encode("utf-8")).hexdigest()[:12]
    return f"{not_id}.visual.{ozet}"


def figur_kur(not_id: str, tanim: tuple, etiketler: dict) -> dict:
    """Kısayol tanımını katalog biçimine çevirir; etiketleri sözlüğe yazar."""
    def et(metin: str) -> str:
        a = anahtar(not_id, metin)
        etiketler[a] = metin
        return a

    tip = tanim[0]
    if tip == "tablo":
        _, basliklar, satirlar = tanim
        for s in satirlar:
            assert len(s) == len(basliklar), f"{not_id}: satır genişliği tutmuyor"
        return {
            "kind": "table",
            "headerKeys": [et(b) for b in basliklar],
            "rows": [[{"key": et(h)} for h in s] for s in satirlar],
        }
    if tip == "akis":
        _, adimlar = tanim
        dugumler = [{"id": f"a{i+1}", "labelKey": et(a)}
                    for i, a in enumerate(adimlar)]
        kenarlar = [{"from": f"a{i+1}", "to": f"a{i+2}"}
                    for i in range(len(adimlar) - 1)]
        return {"kind": "flow", "nodes": dugumler, "edges": kenarlar,
                "direction": "down"}
    if tip == "grafik":
        _, stil, kategoriler, degerler, eksenler = tanim
        assert len(kategoriler) == len(degerler), f"{not_id}: uzunluk tutmuyor"
        fig = {"kind": "chart", "style": stil,
               "categoryKeys": [et(k) for k in kategoriler],
               "values": list(degerler)}
        if eksenler:
            fig["axisKeys"] = {"x": et(eksenler[0]), "y": et(eksenler[1])}
        return fig
    if tip == "devre":
        _, elemanlar, duzen = tanim
        return {"kind": "circuit", "elements": list(elemanlar), "layout": duzen}
    raise ValueError(f"bilinmeyen figür kısayolu: {tip}")


def alt_metin(tanim: tuple, gorsel_notu: str) -> str:
    """Görselin GÖSTERDİĞİNİ betimler; çıkarımı değil (figure_spec 1.1.0)."""
    tip = tanim[0]
    if tip == "tablo":
        _, basliklar, satirlar = tanim
        sutunlar = ", ".join(f"'{b}'" for b in basliklar)
        ilk = "; ".join(" — ".join(s) for s in satirlar[:2])
        return (f"{len(satirlar)} satırlık tablo. Sütunlar: {sutunlar}. "
                f"İlk satırlar: {ilk}.")
    if tip == "akis":
        _, adimlar = tanim
        return (f"{len(adimlar)} adımlı yukarıdan aşağı akış şeması: "
                + " → ".join(adimlar) + ".")
    if tip == "grafik":
        _, stil, kategoriler, degerler, eksenler = tanim
        cift = ", ".join(f"{k}: {d}" for k, d in zip(kategoriler, degerler))
        eksen = (f" Yatay eksen '{eksenler[0]}', düşey eksen '{eksenler[1]}'."
                 if eksenler else "")
        tur = {"bar": "sütun", "line": "çizgi", "pie": "daire"}[stil]
        return f"{len(kategoriler)} değerli {tur} grafiği. {cift}.{eksen}"
    if tip == "devre":
        _, elemanlar, duzen = tanim
        ad = {"battery": "pil", "lamp": "ampul", "switch": "anahtar",
              "resistor": "direnç", "wire": "bağlantı kablosu"}
        sayim: dict = {}
        for e in elemanlar:
            sayim[e] = sayim.get(e, 0) + 1
        liste = ", ".join(
            f"{n} {ad[e]}" if n > 1 else ad[e] for e, n in sayim.items())
        duzen_ad = {"series": "seri", "parallel": "paralel"}[duzen]
        return f"{duzen_ad.capitalize()} bağlı devre şeması: {liste}."
    raise ValueError(tip)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaz", action="store_true")
    ns = ap.parse_args(argv)

    kayitlar = [json.loads(s) for s in
                PAKET.read_text(encoding="utf-8").splitlines() if s.strip()]
    paket = kayitlar[0]
    etiketler = dict(paket.get("labels") or {})
    notlar = [k for k in kayitlar if k.get("type") == "note"]

    eksik = sorted({n["id"] for n in notlar} - set(NOTLAR))
    if eksik:
        print(f"tanımı yazılmamış not: {eksik}")
        return 1

    tur_sayimi: dict = {}
    for n in notlar:
        y = NOTLAR[n["id"]]
        b = n["lessonSections"]
        b["whatIWillLearn"] = y["ogrenecegim"]
        b["priorKnowledge"] = y["onbilgi"]
        b["summary"] = y["ozet"]
        b["figureNote"] = y["gorsel"]
        # Dokuz bölüm, kaynaktaki beşle birlikte NOT_BOLUMLERI sırasına konur.
        n["lessonSections"] = {
            "whatIWillLearn": b["whatIWillLearn"],
            "keyConcepts": b["keyConcepts"],
            "priorKnowledge": b["priorKnowledge"],
            "steps": b["steps"],
            "workedExamples": b["workedExamples"],
            "commonMistakes": b["commonMistakes"],
            "selfCheck": b["selfCheck"],
            "summary": b["summary"],
            "figureNote": b["figureNote"],
        }
        n["body"] = render_lesson_body(n["lessonSections"])

        fig = figur_kur(n["id"], y["fig"], etiketler)
        a = anahtar(n["id"], alt_metin(y["fig"], y["gorsel"]))
        etiketler[a] = alt_metin(y["fig"], y["gorsel"])
        fig["altTextKey"] = a
        n["figure"] = fig
        tur_sayimi[fig["kind"]] = tur_sayimi.get(fig["kind"], 0) + 1

    paket["labels"] = etiketler
    print(f"  tamamlanan not      {len(notlar)}")
    print(f"  figür türleri       {tur_sayimi}")
    print(f"  etiket              {len(etiketler)}")

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
