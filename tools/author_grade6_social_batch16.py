#!/usr/bin/env python3
"""Append 100 independently authored Grade 6 social studies questions (batch 16)."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

from author_grade6_bilisim_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade6_fen_batch07 import task
from author_grade6_fen_english_batch10 import make_record
from author_grade6_mixed_batch03 import read_notes_only

SOCIAL_SOURCE = Path("turkiye/6-sinif/sosyal-bilgiler/sosyal-bilgiler-tum.jsonl")


def vrows(note: str, values: list[tuple[str, str, str, str, str, str, str, str | None]]):
    result = []
    for mode, stem, correct, w1, w2, w3, explanation, visual in values:
        item = task(note, mode, stem, correct, [w1, w2, w3], explanation,
                    figure_kind=(visual.split(":", 1)[0] if visual else None))
        if visual:
            item["visual_payload"] = visual
        result.append(item)
    return result


def environment_tasks():
    n = "tr-g06-sosyal-bilgiler-note-005"
    return vrows(n, [
        ("comprehension", "Doğal çevre unsuru hangisidir?", "Akarsu", "Baraj", "Liman", "Karayolu", "Akarsu insan yapımı olmayan doğal bir unsurdur.", None),
        ("comprehension", "Beşerî çevre neyi kapsar?", "İnsanların oluşturduğu veya değiştirdiği yerleşme, ulaşım ve üretim unsurlarını", "Yalnız iklim olaylarını", "Sadece yer şekillerini", "İnsan etkisi görmemiş bütün alanları", "Beşerî çevre insan etkinliklerinin mekândaki izlerini içerir.", None),
        ("comprehension", "Nüfusun dağılışını etkileyen doğal etkenlerden biri hangisidir?", "İklim", "Belediye logosu", "Sokak adı", "Okul forması", "İklim yaşam ve üretim koşullarını etkileyerek yerleşme tercihlerini değiştirebilir.", None),
        ("application", "Yağışın bol, eğimin fazla olduğu bir bölgede heyelan riskini azaltmak için hangi uygulama uygundur?", "Bitki örtüsünü korumak ve riskli yamaçlarda yapılaşmayı sınırlamak", "Yamaçtaki bütün ağaçları kesmek", "Akarsu yataklarını daraltmak", "Eğim bilgisini yok saymak", "Kökler toprağı tutar; yer seçimi de tehlikeye maruz kalmayı azaltır.", "flow:Yoğun yağış>Eğimli yamaç>Heyelan riski>Koruyucu önlem"),
        ("application", "Geniş ve verimli bir ovada hangi ekonomik faaliyet daha elverişli olabilir?", "Tarım", "Açık deniz balıkçılığı", "Yüksek dağ kayak işletmesi", "Kutup araştırması", "Düz arazi ve verimli toprak tarımsal üretimi destekler.", None),
        ("application", "Bir kıyı kentinde doğal liman ve ulaşım bağlantıları gelişmiştir. Hangi faaliyet güçlenebilir?", "Deniz ticareti", "Yalnız yaylacılık", "Çöl tarımı", "Buzul madenciliği", "Korunaklı liman ve bağlantılar yük ve yolcu taşımacılığını kolaylaştırır.", "table:Doğal özellik|Korunaklı koy;Beşerî özellik|Kara yolu bağlantısı;Olası faaliyet|Deniz ticareti"),
        ("application", "Akarsu yatağının taşkın alanına konut yapılmasının temel sakıncası nedir?", "Taşkın sırasında can ve mal kaybı riskini artırması", "Yağışı tamamen durdurması", "Akarsuyun kaynağını değiştirmesi", "Dağların yükseltisini azaltması", "Taşkın ovası suyun dönemsel olarak yayılabildiği alandır.", None),
        ("application", "Bir bölgede maden çıkarılması planlanıyor. Sürdürülebilir karar için hangisi birlikte incelenmelidir?", "Ekonomik yarar, su-toprak etkisi ve rehabilitasyon planı", "Yalnız cevherin rengi", "Sadece ilk yıl geliri", "Çevresel etkileri gizleyen reklam", "Doğal kaynak kullanımı ekonomik ve çevresel sonuçlarla birlikte değerlendirilir.", None),
        ("analysis", "Bir vadiye yol yapılınca pazara erişim kolaylaşıyor fakat orman parçalanıyor. Hangi yorum dengelidir?", "Ulaşım yararı ile ekosistem üzerindeki parçalanma etkisi birlikte değerlendirilmelidir.", "Yolun yalnız olumlu etkisi vardır.", "Orman parçalanması ulaşım planıyla ilgisizdir.", "Ekonomik yarar bütün çevresel etkileri önemsiz yapar.", "Beşerî müdahale birden çok sonuç doğurabilir.", "table:Yarar|Pazara erişim;Risk|Orman parçalanması;Karar ölçütü|İki etkiyi birlikte değerlendirme"),
        ("analysis", "Dağlık bölgede yerleşmeler seyrek, vadilerde daha yoğundur. Hangi açıklama en uygundur?", "Eğim, ulaşım ve tarıma elverişli alanların dağılışı yerleşmeyi etkilemiştir.", "Dağlık alanlarda insan yaşayamaz.", "Nüfus yalnız şehir adlarına göre dağılır.", "Vadilerde hiçbir doğal kaynak yoktur.", "Daha düz ve erişilebilir alanlar yerleşme için görece elverişli olabilir.", None),
        ("analysis", "Kuraklık sonrası tarımsal üretim azalıyor ve bazı aileler kente göç ediyor. Bu örnek hangi ilişkiyi gösterir?", "Doğal koşulların ekonomik faaliyet ve nüfus hareketini etkileyebildiğini", "Göçün iklimle hiçbir ilişkisi olmadığını", "Tarımın yalnız kentlerde yapıldığını", "Kuraklığın ulaşımı doğrudan artırdığını", "Su azalması üretimi, üretim kaybı da geçim kararlarını etkileyebilir.", "flow:Kuraklık>Su azalması>Üretim kaybı>Göç kararı"),
        ("error-analysis", "Bir öğrenci “İnsan eli değen her yer artık doğal çevreyle ilişkisizdir.” diyor. Hangi düzeltme doğrudur?", "Doğal ve beşerî çevre sürekli etkileşir; insan yapıları doğal süreçlerden etkilenmeye devam eder.", "Kentlerde iklim oluşmaz.", "Yollar yer şekillerinden bağımsızdır.", "Beşerî çevre doğayı tamamen ortadan kaldırır.", "Yerleşmeler su, iklim, zemin ve afet gibi doğal koşullarla ilişkilidir.", None),
        ("error-analysis", "Bir öğrenci “Verimli ovaya kurulan her fabrika çevre için kesinlikle uygundur.” diyor. Hangi değerlendirme gerekir?", "Arazi kaybı, su kullanımı, kirlilik ve ekonomik gereksinim birlikte incelenmeden uygunluk söylenemez.", "Fabrika türü ve yer seçimi önemli değildir.", "Verimli toprak yalnız sanayi içindir.", "Çevresel etki ölçülemez.", "Tek bir özellik yer seçiminin bütün sonuçlarını belirlemez.", None),
    ])


def turkic_world_tasks():
    n = "tr-g06-sosyal-bilgiler-note-006"
    return vrows(n, [
        ("comprehension", "Türk dünyasıyla kültürel iş birliğinin temel alanlarından biri hangisidir?", "Dil, sanat ve eğitim", "Yalnız sınır çizimi", "Sadece hava durumu", "Tek taraflı ürün satışı", "Ortak kültürel bağlar eğitim, sanat ve dil çalışmalarında iş birliğini destekler.", None),
        ("comprehension", "Ortak alfabe veya terim çalışmaları hangi amaca katkı sağlayabilir?", "Topluluklar arası yazılı iletişimi kolaylaştırmaya", "Bütün dilleri ortadan kaldırmaya", "Coğrafi uzaklığı sıfırlamaya", "Kültürel çeşitliliği yasaklamaya", "Ortak gösterimler karşılıklı anlaşılabilirliği artırabilir.", None),
        ("comprehension", "Kardeş okul projesinin kültürel işlevi nedir?", "Öğrencilerin karşılıklı yaşam ve gelenekleri doğrudan tanımasına ortam sağlamak", "Yalnız sınav notlarını gizlemek", "Tek bir kültürü üstün ilan etmek", "İletişimi kesmek", "Düzenli öğrenci etkileşimi kültürler arası öğrenmeyi güçlendirir.", None),
        ("application", "Türkiye ve Kazakistan'daki öğrenciler ortak destan motiflerini karşılaştırıyor. Hangi ürün uygundur?", "Kaynakları belirtilmiş iki dilli dijital sergi", "Kaynağı gizlenmiş kopya metin", "Yalnız tek görüşü doğru ilan eden afiş", "Katılımcıları dışlayan liste", "İki dilli, kaynaklı sunum karşılıklı erişim ve akademik dürüstlük sağlar.", None),
        ("application", "Ortak müzik festivalinde kültürel saygıyı artıran uygulama hangisidir?", "Eserlerin yöresini, icracısını ve bağlamını tanıtmak", "Eser adlarını değiştirmek", "Sanatçı katkısını gizlemek", "Bir grubun sahneye çıkmasını engellemek", "Köken ve emeği görünür kılmak temsilin doğruluğunu güçlendirir.", None),
        ("application", "Türk dünyası ülkeleri kuraklık deneyimlerini paylaşacaktır. En verimli iş birliği hangisidir?", "Ortak araştırma, veri paylaşımı ve uyarlanabilir su yönetimi çalışması", "Verileri gizlemek", "Yalnız tören düzenlemek", "Her ülkenin aynı çözümü kanıtsız uygulaması", "Benzer sorunlarda karşılaştırmalı veri ve ortak araştırma çözüm kapasitesini artırır.", "flow:Ortak sorun>Veri paylaşımı>Karşılaştırmalı araştırma>Uyarlanmış çözüm"),
        ("application", "Bir öğrenci değişim programı için sunum hazırlıyor. Hangi yaklaşım genelleme riskini azaltır?", "Farklı bölgelerden güvenilir kaynaklar kullanıp çeşitliliği belirtmek", "Tek bir kişiyi bütün ülke adına konuşturmak", "Sosyal medya söylentisini doğrulamadan aktarmak", "Bütün toplulukları aynı saymak", "Çoklu kaynak kültür içindeki çeşitliliği görünür kılar.", None),
        ("analysis", "İki ülke ortak film yapıyor; senaryoda her iki toplumdan danışmanlar bulunuyor. Bunun katkısı nedir?", "Temsil hatalarını azaltıp ortak üretim duygusunu güçlendirebilir.", "Bütün kültürel farkları siler.", "Filmin kaynağa ihtiyacını ortadan kaldırır.", "Yalnız maliyeti artırır.", "Karşılıklı danışmanlık doğruluk ve katılım sağlar.", None),
        ("analysis", "Dil benzerliği iletişimi kolaylaştırsa da bazı sözcüklerin anlamı farklıdır. Hangi sonuç çıkar?", "Benzerlikten yararlanırken anlam farklılıklarını araştırmak gerekir.", "Bütün sözcükler kesin aynı anlama gelir.", "İletişim mümkün değildir.", "Çeviri çalışması gereksizdir.", "Akraba dillerde ortaklıklar kadar farklılaşmalar da bulunur.", "table:Ortaklık|Benzer kökler;Farklılık|Değişen anlamlar;Gereken|Bağlamı kontrol etme"),
        ("analysis", "Kültürel proje yalnız başkentlerde düzenleniyor ve kırsal katılımcılara ulaşmıyor. Hangi iyileştirme uygundur?", "Çevrim içi erişim ve farklı bölgelerde yerel ortaklıklar kurmak", "Katılımı daha da sınırlamak", "Yalnız davetli listesini gizlemek", "Yerel dilleri kaldırmak", "Erişim kanallarını çeşitlendirmek kapsayıcılığı artırır.", None),
        ("analysis", "Ortak miras etkinliği sonunda katılımcılar kendi kültürlerini de yeniden araştırıyor. Bu sonuç neyi gösterir?", "Kültürel etkileşim karşı tarafı tanırken öz farkındalığı da güçlendirebilir.", "Etkileşim kimliği mutlaka yok eder.", "Araştırma kültürle ilgisizdir.", "Ortak etkinlik tek yönlü öğrenmedir.", "Karşılaştırma kişinin kendi kültürel unsurlarını yeniden düşünmesini sağlayabilir.", None),
        ("error-analysis", "Bir öğrenci “Türk dünyasındaki bütün toplumların kültürü bütünüyle aynıdır.” diyor. Hangi düzeltme doğrudur?", "Ortak tarihî ve dilsel bağlar bulunabilir; her toplumun özgün deneyim ve kültürel çeşitliliği de vardır.", "Ortak bağ bulunması bütün farkları yok eder.", "Farklılık varsa iş birliği yapılamaz.", "Kültür yalnız coğrafyayla belirlenir.", "Ortaklık ve çeşitlilik aynı anda bulunabilir.", None),
        ("error-analysis", "Bir öğrenci “Kültürel iş birliği tek ülkenin ürünlerini diğerlerine öğretmesidir.” diyor. Hangi değerlendirme uygundur?", "İş birliği karşılıklı paylaşım, ortak karar ve iki yönlü öğrenme gerektirir.", "Tek yönlü aktarım her zaman eşitliktir.", "Ortak projede danışma gerekmez.", "Katılımcıların görüşü önemsizdir.", "İş birliğinde taraflar üretime ve karara birlikte katılır.", None),
    ])


def first_turkic_states_tasks():
    n = "tr-g06-sosyal-bilgiler-note-007"
    return vrows(n, [
        ("comprehension", "İlk Türk devletlerinde kurultay hangi işleve sahipti?", "Devlet işlerinin görüşüldüğü danışma meclisi olmaya", "Yalnız ticaret malı depolamaya", "Dinî yapı inşa etmeye", "Tarım ürünü ölçmeye", "Kurultay yönetim meselelerinin görüşüldüğü siyasi bir organdı.", None),
        ("comprehension", "Kut anlayışı yönetimde neyi ifade ederdi?", "Yönetme yetkisinin ilahî kaynaklı kabul edilmesini", "Her kararın tüccarlarca verilmesini", "Ülkenin yönetimsiz kalmasını", "Yalnız askerî rütbeyi", "Kut, hükümdarlık yetkisinin meşruiyet açıklamalarından biriydi.", None),
        ("comprehension", "Onlu sistemin askerî katkısı hangisidir?", "Birlikleri düzenli kademelere ayırarak sevk ve yönetimi kolaylaştırması", "Ordunun sayısını gizlemesi", "At kullanımını yasaklaması", "Bütün askerleri tek birime toplaması", "On, yüz, bin gibi kademeler örgütlenmeyi kolaylaştırdı.", None),
        ("application", "Bir tarihçi yazıt, Çin kroniği ve arkeolojik bulguyu karşılaştırıyor. Bu yöntem neden değerlidir?", "Farklı kaynakların eksik ve yanlı yönlerini karşılıklı denetlemeyi sağlar.", "Tek kaynağı mutlak doğru yapar.", "Arkeolojiyi gereksiz kılar.", "Olayların tarihini değiştirir.", "Çoklu kaynak kullanımı kanıt gücünü artırır.", None),
        ("application", "Göçebe yaşam koşullarında atlı birliklerin yaygın olması hangi gereksinimle ilişkilidir?", "Geniş alanlarda hızlı hareket ve savunma", "Denizaltı taşımacılığı", "Sabit fabrika üretimi", "Kutup tarımı", "Atlı hareketlilik bozkır coğrafyasında ulaşım ve askerlik avantajı sağladı.", None),
        ("application", "İpek Yolu üzerindeki denetim neden devletler için önemliydi?", "Ticaret geliri ve kültürel-siyasi etkileşim sağlaması", "Yalnız yağışı artırması", "Bütün savaşları bitirmesi", "Tarım alanını otomatik genişletmesi", "Ticaret yolları ekonomik kaynak ve diplomatik ilişki oluşturdu.", "flow:Ticaret yolu>Mal ve insan hareketi>Gelir ve etkileşim>Siyasi önem"),
        ("application", "Orhun Yazıtları hangi tür tarihsel bilgi sağlayabilir?", "Yönetim anlayışı, toplum ve dönemin olaylarına ilişkin birincil anlatı", "Gelecekteki hava tahmini", "Yalnız modern nüfus sayımı", "Roma hukukunun tam metni", "Döneminde yazılmış metinler siyasi ve toplumsal düşünceyi yansıtır.", None),
        ("application", "Hayvancılığın yaygın olduğu bozkır ekonomisinde hangi ürünün ticareti beklenebilir?", "Deri ve yün", "Tropikal kauçuk", "Okyanus mercanı", "Çay plantasyonu ürünü", "Hayvan yetiştiriciliği deri, yün ve hayvansal ürün sağlar.", None),
        ("analysis", "Kurultayın bulunması hükümdarın yetkisinin sınırsız olmadığına tek başına kesin kanıt mıdır?", "Hayır; danışmanın karar üzerindeki gerçek etkisi başka kanıtlarla da incelenmelidir.", "Evet; her kurultay modern parlamento ile aynıdır.", "Hayır; kurultay hiç toplanmamıştır.", "Evet; hükümdar karar veremezdi.", "Kurumun varlığı kadar uygulamadaki yetkisi önemlidir.", None),
        ("analysis", "Yazıtlarda halka karşı sorumluluk vurgusu bulunması hangi yönetim düşüncesini destekler?", "Hükümdarın toplumun düzen ve refahını gözetmesi beklentisini", "Halkın hiçbir önem taşımadığını", "Yönetimin yalnız ticaretle ilgilendiğini", "Devletin askerî yapısının olmadığını", "Metindeki hesap verme ve koruma dili yöneticilik sorumluluğuna işaret eder.", None),
        ("analysis", "Bozkır yaşamı, hayvancılık ve atlı askerlik birlikte değerlendirildiğinde hangi ilişki kurulur?", "Coğrafya ekonomik üretim ve askerî örgütlenmeyi birlikte etkilemiştir.", "Üç unsur birbirinden bağımsızdır.", "Hayvancılık yalnız kıyıda yapılır.", "Atlı birlikler tarımı ortadan kaldırmıştır.", "Hareketli yaşam hayvan yetiştiriciliği ve süvari becerilerini destekledi.", "table:Coğrafya|Bozkır;Ekonomi|Hayvancılık;Askerlik|Atlı birlik"),
        ("error-analysis", "Bir öğrenci “Kut anlayışı hükümdarın her kararının doğru olduğunu kanıtlar.” diyor. Hangi düzeltme gerekir?", "Kut meşruiyet anlayışıdır; kararların sonuçları ve yönetim uygulamaları ayrıca değerlendirilir.", "Kut bilimsel deney sonucudur.", "Kut yalnız ticaret vergisidir.", "Hükümdar hiçbir karar vermezdi.", "Yetki kaynağına ilişkin inanç, her uygulamanın doğruluğunu garanti etmez.", None),
        ("error-analysis", "Bir öğrenci “İpek Yolu yalnız mal taşır, kültürel etkileşim oluşturmaz.” diyor. Hangi değerlendirme doğrudur?", "Tüccarlar, yolcular ve elçiler mallarla birlikte bilgi, inanç ve teknikleri de taşıyabilir.", "Yollar insan hareketini engeller.", "Ticaret yalnız tek yönde olur.", "Kültür coğrafya boyunca değişmez.", "Ticaret ağları çok yönlü insan ve fikir dolaşımına aracılık eder.", None),
    ])


def islamic_civilization_tasks():
    n = "tr-g06-sosyal-bilgiler-note-008"
    return vrows(n, [
        ("comprehension", "Beytülhikme'nin tarihsel işlevlerinden biri hangisidir?", "Çeviri ve bilim çalışmalarını destekleyen bir merkez olmak", "Yalnız askerî eğitim vermek", "Ticaret yollarını kapatmak", "Tarım vergisi toplamak", "Bağdat'taki merkez farklı dillerdeki eserlerin çevrilmesi ve incelenmesine katkı sağladı.", None),
        ("comprehension", "İslam medeniyetinde vakıflar hangi toplumsal alana katkı sağlayabiliyordu?", "Eğitim, sağlık ve sosyal yardıma", "Yalnız saray eğlencesine", "Sadece sınır çizimine", "Bilimsel eserleri yasaklamaya", "Vakıflar kalıcı gelirle kamu yararına hizmetleri destekleyebiliyordu.", None),
        ("comprehension", "Çeviri faaliyetlerinin bilimsel gelişime katkısı hangisidir?", "Önceki bilgi birikimini erişilebilir kılıp eleştiri ve yeni çalışmalar için temel oluşturması", "Bütün eski bilgiyi değişmeden doğru kabul ettirmesi", "Yeni araştırmayı gereksiz kılması", "Tek dili zorunlu kılması", "Çeviri, bilgiyi dolaşıma sokar; bilim insanları bunu geliştirip sınayabilir.", "flow:Eski eser>Çeviri>Karşılaştırma ve eleştiri>Yeni çalışma"),
        ("application", "Bir öğrenci İbn Sina'nın tıp katkısını araştırıyor. En güvenilir yöntem hangisidir?", "Eser çevirilerini, bilim tarihi çalışmalarını ve kaynak bağlamını karşılaştırmak", "Kaynağı belirsiz tek alıntıyı kullanmak", "Modern bir söylentiyi tarihsel kanıt saymak", "Yalnız portreye bakmak", "Kaynak çeşitliliği katkının içeriğini ve dönemini doğrulamaya yardım eder.", None),
        ("application", "Harezmi'nin çalışmalarının sonraki toplumlara aktarılmasında hangi süreç önemlidir?", "Eserlerin çevrilmesi, öğretilmesi ve farklı problemlerde kullanılması", "Metinlerin saklanıp okunmaması", "Sayı kullanımının yasaklanması", "Ticaretin durdurulması", "Bilgi aktarımı metin, eğitim ve uygulama ağlarıyla gerçekleşir.", "timeline:Çalışmanın yazılması;Çeviri;Eğitimde kullanım;Yeni uygulamalar"),
        ("application", "Bir hastane vakıf gelirleriyle ücretsiz hizmet sunuyor. Bu durum hangi ilişkiyi örnekler?", "Ekonomik kaynağın toplumsal sağlık hizmetine dönüştürülmesini", "Bilimin toplumdan ayrılmasını", "Yalnız askerî örgütlenmeyi", "Ticaretin yasaklanmasını", "Vakıf geliri süreklilik sağlayarak kamusal hizmeti destekler.", None),
        ("application", "Bir astronom gözlemlerini tablo hâline getirip başkalarının hesaplarıyla karşılaştırıyor. Hangi bilimsel tutumu gösterir?", "Sistemli kayıt ve doğrulama", "Kanıtsız kabul", "Bilgiyi gizleme", "Sonucu ölçmeden ilan etme", "Kayıt ve karşılaştırma sonuçların sınanabilirliğini artırır.", "table:Yöntem|Gözlem kaydı;Kontrol|Başka hesaplarla karşılaştırma;Sonuç|Sınanabilir bilgi"),
        ("analysis", "Antik bir eser Arapçaya, sonra Latinceye çevriliyor ve Avrupa'da inceleniyor. Hangi çıkarım uygundur?", "Medeniyetler arası çeviri ağları bilginin korunup dönüşmesine aracılık etmiştir.", "Bilgi yalnız tek toplumda kalmıştır.", "Çeviri hiçbir yeni yorum oluşturmaz.", "Eserin ilk dili önemini yitirmiştir.", "Birden çok aktarım aşaması ortak bilim mirasını genişletir.", "timeline:İlk metin;Arapça çeviri;Bilimsel yorum;Latince çeviri"),
        ("analysis", "Bir bilim insanının önceki görüşü eleştirip ölçümle yeni sonuç önermesi neyi gösterir?", "Bilimsel mirasın yalnız korunmadığını, sorgulanarak geliştirildiğini", "Önceki bilginin tümden değersiz olduğunu", "Ölçümün bilimle ilgisiz olduğunu", "Eleştirinin çeviriyi engellediğini", "Bilimsel ilerleme aktarım, sınama ve düzeltme süreçlerini içerir.", None),
        ("analysis", "Bağdat, Kurtuba ve Semerkant'ta bilim merkezlerinin bulunması hangi durumu destekler?", "Bilimsel üretimin farklı bölgelerde ağlar kurarak geliştiğini", "Bilimin yalnız tek kentte yapıldığını", "Şehirler arasında iletişim olmadığını", "Coğrafyanın bilgi dolaşımını engellediğini", "Çok merkezli üretim seyahat, eğitim ve eser dolaşımıyla birbirine bağlanabilir.", None),
        ("analysis", "Bir katkının 'insanlığın ortak mirası' sayılması neyi vurgular?", "Farklı toplumların ürettiği bilginin sonraki kuşaklarca paylaşılması ve geliştirilmesini", "Bilginin yalnız üretildiği yerde kalmasını", "Bütün buluşların tek kişiye ait olmasını", "Geçmiş çalışmaların kullanılmamasını", "Bilgi kültürler arası aktarım ve birikimle ortaklaşır.", None),
        ("error-analysis", "Bir öğrenci “Çeviri yapan bilim insanları yalnız sözcükleri değiştirdi, bilgiye katkı sunmadı.” diyor. Hangi düzeltme doğrudur?", "Çevirmenler terim geliştirme, açıklama, karşılaştırma ve yeni araştırmaya zemin hazırlama rolleri de üstlenmiştir.", "Çeviri hiçbir uzmanlık gerektirmez.", "Çevrilen eserler okunmamıştır.", "Bilimsel terimler kendiliğinden oluşur.", "Bilginin doğru aktarımı ve yorumlanması bilimsel emeğin parçasıdır.", None),
        ("error-analysis", "Bir öğrenci “İslam medeniyetindeki bütün bilimsel çalışmalar tek bir millete aittir.” diyor. Hangi değerlendirme uygundur?", "Farklı dil, bölge ve topluluklardan bilim insanları ortak kurum ve ağlarda üretime katılmıştır.", "Medeniyetler yalnız tek kökenden oluşur.", "Bilim insanlarının seyahati olmamıştır.", "Ortak dil çeşitliliği ortadan kaldırır.", "Medeniyet havzası çok sayıda topluluğun katkısını içerebilir.", None),
    ])


def change_after_islam_tasks():
    n = "tr-g06-sosyal-bilgiler-note-009"
    return vrows(n, [
        ("comprehension", "Türklerin İslamiyet'i kabulünden sonra görülen kültürel değişimlerden biri hangisidir?", "İslamî eğitim ve mimari kurumların yaygınlaşması", "Bütün eski geleneklerin bir anda yok olması", "Yazının tamamen terk edilmesi", "Şehir yaşamının sona ermesi", "Yeni din eğitim, sanat ve kurumlara etki ederken bazı eski unsurlar da sürdü.", None),
        ("comprehension", "Kültürel sentez neyi ifade eder?", "Farklı kültürel unsurların etkileşerek yeni biçimler oluşturmasını", "Geçmişin bütünüyle silinmesini", "Yalnız tek unsurun değişmeden kalmasını", "Toplumlar arası iletişimin kesilmesini", "Sentez süreklilik ve değişim öğelerini birlikte taşır.", None),
        ("comprehension", "Karahanlı eserlerinde Türkçe kullanımının sürmesi neyi gösterir?", "Dinî değişime rağmen dilsel sürekliliğin korunabildiğini", "Türkçenin hemen unutulduğunu", "Hiç yeni kavram oluşmadığını", "Yalnız sözlü kültür bulunduğunu", "Kültürel değişim bütün eski unsurları aynı anda ortadan kaldırmaz.", None),
        ("application", "Kutadgu Bilig'i incelerken hangi iki boyut birlikte ele alınmalıdır?", "Türk yönetim geleneği ile İslamî ahlak ve düşünce", "Yalnız kâğıdın rengi ile sayfa sayısı", "Sadece modern yorumlar", "Eserin adı ile baskı fiyatı", "Eser iki kültürel birikimin etkileşimini yansıtır.", None),
        ("application", "Bir yapıda kubbe, geometrik süsleme ve yerel taş işçiliği birlikte görülüyor. En uygun yorum hangisidir?", "Mimari, yeni dinî ihtiyaçlarla yerel sanat birikimini birleştirmiş olabilir.", "Yapı hiçbir kültürel etki taşımaz.", "Yerel malzeme dinî işlevi yok eder.", "Her kubbeli yapı aynı dönemdendir.", "Biçim, işlev ve malzeme farklı geleneklerin birleşimini gösterebilir.", "table:Yeni unsur|Dinî işlev ve kubbe;Süren unsur|Yerel taş işçiliği;Sonuç|Kültürel sentez"),
        ("application", "Yeni kabul edilen dinin kavramları Türkçeye aktarılırken hangi süreç beklenir?", "Bazı yeni sözcüklerin alınması ve Türkçe karşılıkların geliştirilmesi", "Dilin iletişim işlevini yitirmesi", "Bütün sözcüklerin aynı anda değişmesi", "Yazılı eserin ortadan kalkması", "Dil temasla yeni kavramları karşılayacak biçimde zenginleşebilir.", None),
        ("application", "Ahilikte meslek eğitimi ile ahlak kurallarının birlikte verilmesi neyi gösterir?", "Ekonomik yaşam ile toplumsal değerlerin kurumsal biçimde birleşmesini", "Mesleklerin kuralsız olduğunu", "Ticaretin eğitimle ilişkisiz olduğunu", "Yalnız askerî eğitim yapıldığını", "Ahilik üretim, dayanışma ve meslek ahlakını birlikte düzenledi.", "flow:Meslek eğitimi>Ahlak ilkeleri>Kaliteli üretim>Toplumsal güven"),
        ("application", "Bir tarihçi değişimi incelerken İslamiyet öncesi ve sonrası cenaze uygulamalarını karşılaştırıyor. Hangi yöntem uygundur?", "Arkeolojik bulgularla yazılı kaynakları dönemlerine göre karşılaştırmak", "Tek bulguyu bütün yüzyıllara genellemek", "Kaynak tarihlerini yok saymak", "Sadece günümüz uygulamasını geçmiş saymak", "Dönemlendirilmiş çoklu kanıt süreklilik ve değişimi ayırır.", None),
        ("analysis", "Yeni din kabul edildiği hâlde bazı bayram ve müzik unsurlarının sürmesi hangi sonucu destekler?", "Kültürel değişimin seçici ve zaman içinde gerçekleştiğini", "Hiçbir değişim olmadığını", "Eski kültürün tamamının yok olduğunu", "Din ile kültürün ilişkisiz olduğunu", "Toplumlar yeni unsurları önceki birikimleriyle uyarlayabilir.", "timeline:Önceki gelenek;Yeni dinin kabulü;Uyarlama;Yeni kültürel biçim"),
        ("analysis", "Devlet unvanlarında hem eski Türkçe hem İslamî terimler görülüyor. Bu durum neyi gösterir?", "Yönetim dilinde süreklilik ve yeni meşruiyet unsurlarının birlikte bulunduğunu", "Eski yönetimin hiç etkisi kalmadığını", "İki terimin aynı anlama geldiğini", "Devlet kurumlarının ortadan kalktığını", "Karma terminoloji geçiş ve sentez sürecine işaret eder.", None),
        ("analysis", "Kentlerde medrese ve kervansarayların yaygınlaşması hangi iki alanı etkileyebilir?", "Eğitim ile ticaret ve konaklama ağlarını", "Yalnız deniz savaşlarını", "Sadece göçebe hayvancılığı", "Kutup araştırmasını", "Yeni kurumlar bilgi dolaşımı ve yol güvenliği-ekonomi bağlantısını destekler.", None),
        ("error-analysis", "Bir öğrenci “İslamiyet'in kabulüyle Türk kültürünün bütün eski unsurları aynı gün sona ermiştir.” diyor. Hangi düzeltme gerekir?", "Değişim uzun sürede gerçekleşmiş; bazı unsurlar dönüşmüş, bazıları sürmüş, yenileri eklenmiştir.", "Kültürel değişim anlıktır.", "Eski geleneklerin sürmesi imkânsızdır.", "Yeni din hiçbir değişim oluşturmaz.", "Tarihsel kültür değişimi süreklilik ve dönüşümü birlikte içerir.", None),
        ("error-analysis", "Bir öğrenci “Yeni bir sözcüğün dile girmesi dilin tamamen yok olduğu anlamına gelir.” diyor. Hangi değerlendirme doğrudur?", "Diller etkileşimle sözcük alabilir; temel yapı ve üretkenlik sürerken söz varlığı değişebilir.", "Her alıntı sözcük dili bitirir.", "Diller hiç değişmez.", "Sözcük alışverişi iletişimi imkânsız yapar.", "Söz varlığı değişimi dilsel yok oluşla aynı değildir.", None),
    ])


def anatolia_tasks():
    n = "tr-g06-sosyal-bilgiler-note-010"
    return vrows(n, [
        ("comprehension", "Malazgirt Savaşı'nın Anadolu tarihi açısından önemi hangisidir?", "Türk yerleşme ve siyasi hâkimiyet sürecini hızlandırması", "Anadolu'daki bütün şehirleri aynı gün kurması", "Ticareti tamamen durdurması", "Haçlı Seferlerini sona erdirmesi", "1071 sonrası yerleşme ve beylikleşme süreci hız kazandı.", "timeline:Malazgirt 1071;Yerleşmelerin artması;Beylikler;Türkiye Selçukluları"),
        ("comprehension", "Kervansarayların temel işlevlerinden biri hangisidir?", "Tüccar ve yolculara güvenli konaklama sağlamak", "Tarım alanlarını küçültmek", "Yalnız dinî tören yapmak", "Sınırları çizmek", "Kervansaraylar ticaret yollarındaki güvenlik ve hizmet ağının parçasıydı.", None),
        ("comprehension", "Anadolu'nun Türkleşmesi neyi kapsar?", "Yerleşme, siyasi örgütlenme, dil ve kültürün zamanla yaygınlaşmasını", "Yalnız tek bir savaşın sonucunu", "Bütün halkların bir anda yer değiştirmesini", "Sadece mimari biçim değişimini", "Süreç askerî, demografik, siyasi ve kültürel boyutlar taşır.", None),
        ("application", "Bir şehirde cami, medrese, han ve çarşı birlikte kuruluyor. Bu yapılaşma hangi sonucu destekler?", "Yerleşik yaşam, eğitim, din ve ticaretin birlikte örgütlendiğini", "Şehrin boşaldığını", "Yalnız askerî üs kurulduğunu", "Ticaretin yasaklandığını", "Farklı kurumlar kentsel ve toplumsal hayatın bütünleşmesini gösterir.", "flow:Yerleşme>Cami ve medrese>Han ve çarşı>Kentsel yaşam"),
        ("application", "Bir vakfiye, köprünün bakımına ve yolcuların barınmasına gelir ayırıyor. Hangi işleve işaret eder?", "Ulaşım ve sosyal hizmetlerin sürekliliğine", "Yalnız saray harcamasına", "Toprakların boş bırakılmasına", "Bilginin gizlenmesine", "Vakıf geliri altyapı ve yolcu hizmetini uzun süre destekleyebilir.", None),
        ("application", "Anadolu'daki bir yapının tarihini araştırırken hangisi birlikte kullanılmalıdır?", "Kitabe, mimari özellik, vakfiye ve arkeolojik bulgu", "Yalnız güncel turizm broşürü", "Kaynağı belirsiz söylenti", "Sadece yapının rengi", "Farklı kanıtlar yapının tarihini ve işlevini karşılıklı doğrular.", None),
        ("application", "Ticaret yolu üzerindeki şehrin büyümesini açıklayan en uygun ilişki hangisidir?", "Güvenli yol, pazar ve konaklama hizmetleri tüccar hareketini artırmıştır.", "Yol şehrin bütün bağlantılarını kesmiştir.", "Pazar nüfusu zorunlu olarak azaltır.", "Konaklama ticaretle ilgisizdir.", "Ulaşım ve hizmet altyapısı ekonomik canlılığı destekler.", "table:Altyapı|Yol ve kervansaray;Etkinlik|Ticaret;Olası sonuç|Şehir büyümesi"),
        ("analysis", "Bir bölgede Türkçe yer adları artarken farklı mimari gelenekler birlikte sürüyor. Hangi yorum uygundur?", "Türkleşme yerleşme ve dil değişimini içerirken kültürel etkileşim de devam etmiştir.", "Bütün eski kültürler tamamen yok olmuştur.", "Yer adı değişimi tek başına bütün nüfusu kanıtlar.", "Mimari tarihsel kanıt değildir.", "Demografik ve kültürel süreçler tek biçimli olmayabilir.", None),
        ("analysis", "Haçlı Seferleri ticaret yollarında güvenlik sorunları oluştururken bazı liman ticaretlerini de canlandırmıştır. Bu neyi gösterir?", "Aynı tarihsel olayın bölge ve alana göre farklı sonuçlar doğurabildiğini", "Bütün sonuçların yalnız olumsuz olduğunu", "Ticaretin savaşlardan etkilenmediğini", "Her limanın aynı oranda büyüdüğünü", "Çok boyutlu olaylarda sonuçlar mekâna ve koşullara göre değişebilir.", None),
        ("analysis", "Danişmentliler, Saltuklular ve Mengüceklilere ait eserlerin farklı bölgelerde bulunması hangi çıkarımı destekler?", "Türk beyliklerinin Anadolu'nun çeşitli bölgelerinde siyasi ve kültürel iz bıraktığını", "Yalnız tek merkezde devlet kurulduğunu", "Beyliklerin mimari eser üretmediğini", "Anadolu'da yerleşme olmadığını", "Dağılan eserler bölgesel hâkimiyet ve yerleşme ağlarına kanıt sağlar.", "timeline:İlk yerleşmeler;Bölgesel beylikler;Mimari eserler;Siyasi bütünleşme"),
        ("analysis", "Bir tarihçi yalnız savaş tarihlerini kullanarak Türkleşmeyi açıklıyor. Hangi kanıtlar anlatımı tamamlar?", "Nüfus hareketleri, vakıflar, dil, mimari ve ekonomik ağlar", "Yalnız hükümdar portreleri", "Sadece hava durumu", "Modern sınav sonuçları", "Türkleşme tek askerî olay değil çok boyutlu toplumsal süreçtir.", None),
        ("error-analysis", "Bir öğrenci “1071'de Anadolu'nun tamamı aynı anda Türkleşti.” diyor. Hangi düzeltme doğrudur?", "1071 önemli bir dönüm noktasıdır; yerleşme ve kültürel dönüşüm yüzyıllara yayılan bir süreçtir.", "Bütün tarihsel süreçler bir günde biter.", "Malazgirt'in yerleşmeyle ilgisi yoktur.", "Anadolu'da daha sonra hiçbir siyasi değişim olmamıştır.", "Dönüm noktası ile uzun süreli süreç birbirinden ayrılmalıdır.", None),
        ("error-analysis", "Bir öğrenci “Kervansaraylar yalnız süs amaçlı yapılmıştır.” diyor. Hangi değerlendirme gerekir?", "Kervansaraylar konaklama, güvenlik, bakım ve ticaret hizmetleri sunan işlevsel yapılardı.", "Tüccarlar yapılara giremezdi.", "Yollarla bağlantıları yoktu.", "Ekonomiye hiçbir etkileri olmadı.", "Mimari değerlerinin yanında ulaşım ve ekonomi işlevleri bulunuyordu.", None),
    ])


def participation_tasks():
    n = "tr-g06-sosyal-bilgiler-note-011"
    return vrows(n, [
        ("comprehension", "Kamuoyu neyi ifade eder?", "Toplumu ilgilendiren konularda oluşan yaygın görüş ve tutumları", "Yalnız bir kişinin özel düşüncesini", "Resmî kanunun tam metnini", "Sadece seçim sonucunu", "Kamuoyu çok sayıda bireyin ortak meseleler hakkındaki görüş eğilimidir.", None),
        ("comprehension", "Sivil toplum kuruluşlarının temel özelliklerinden biri hangisidir?", "Kamu yararına bir amaç çevresinde gönüllü katılım örgütlemeleri", "Devletin bütün yetkilerini kullanmaları", "Yalnız seçimlere aday göstermeleri", "Mahkeme kararı vermeleri", "STK'lar devlet dışı gönüllü örgütlenmeler olarak savunuculuk ve hizmet üretebilir.", None),
        ("comprehension", "Siyasi partiler demokratik sistemde hangi işlevi üstlenir?", "Farklı politika önerileri geliştirip seçmen desteği aramak", "Bütün medya organlarını yönetmek", "Mahkemelerin yerine geçmek", "Vatandaş görüşünü yasaklamak", "Partiler programlarıyla yönetime talip olur ve siyasi temsil sunar.", None),
        ("comprehension", "Medyanın yönetim kararlarına etkisi hangi yolla olabilir?", "Sorunları görünür kılma, bilgi sunma ve tartışma ortamı oluşturma", "Kararları tek başına kanunlaştırma", "Seçimleri iptal etme", "Yargı kararı verme", "Medya gündem ve bilgi akışı üzerinden kamuoyu oluşumunu etkileyebilir.", None),
        ("application", "Mahalle sakinleri güvenli yaya geçidi istiyor. Demokratik ve kanıta dayalı yol hangisidir?", "Kaza ve trafik verilerini toplayıp dilekçe ile belediyeye sunmak ve süreci izlemek", "Yolu izinsiz kapatmak", "Yanlış bilgi yaymak", "Başka mahalleleri suçlamak", "Dilekçe, veri ve takip katılımı yasal ve etkili kılar.", "flow:Sorun>Veri toplama>Dilekçe ve görüşme>Kararın izlenmesi"),
        ("application", "Bir çevre derneği yasa taslağı hakkında görüş bildirecek. En güvenilir yaklaşım hangisidir?", "Araştırma sonuçlarını ve etkilenen grupların görüşlerini kaynaklarıyla sunmak", "Kaynağı olmayan korkutucu içerik paylaşmak", "Karşı görüşü tehdit etmek", "Verileri seçici biçimde gizlemek", "Kanıta dayalı savunuculuk karar vericilerin seçenekleri değerlendirmesine katkı sağlar.", None),
        ("application", "Bir haber yönetim kararını eleştiriyor. Okuyucunun ilk yapması gereken nedir?", "Haberdeki iddiaları birden çok güvenilir kaynak ve resmî belgeyle karşılaştırmak", "Başlığı kanıt saymak", "Haberi okumadan paylaşmak", "Karşıt bütün bilgileri reddetmek", "Kaynak doğrulama yanlış yönlendirilmiş kamuoyu riskini azaltır.", None),
        ("application", "Gençler belediye bütçesinde spor alanı öneriyor. Katılımlarını güçlendiren yöntem hangisidir?", "İhtiyaç anketi, maliyet tahmini ve açık toplantıda gerekçeli sunum", "Yalnız slogan yazmak", "Diğer ihtiyaçları yok saymak", "Bütçe verisini gizlemek", "İhtiyaç ve kaynak kanıtı öneriyi uygulanabilir hâle getirir.", "table:Kanıt|İhtiyaç anketi;Kaynak|Maliyet tahmini;Katılım|Açık toplantı"),
        ("application", "Bir siyasi parti programındaki eğitim vaadi nasıl değerlendirilebilir?", "Amaç, kaynak, uygulanabilirlik ve ölçülebilir sonuçlar karşılaştırılarak", "Yalnız afiş rengine bakılarak", "Parti adı yeterli sayılarak", "Diğer programlar okunmadan", "Politika önerisi somut plan ve olası sonuçlarıyla incelenir.", None),
        ("analysis", "Sosyal medyada çok paylaşılan bir talep ile bilimsel araştırma farklı sonuç veriyor. Yönetim ne yapmalıdır?", "Temsil düzeyi, yöntem ve kanıt kalitesini inceleyip iki bilgi kaynağını birlikte değerlendirmelidir.", "Yalnız paylaşım sayısını gerçek kabul etmelidir.", "Araştırmayı otomatik reddetmelidir.", "Hiçbir görüşü dinlememelidir.", "Popülerlik ve güvenilir kanıt aynı ölçüt değildir.", None),
        ("analysis", "Bir STK kampanyası sonrası konu meclis gündemine alınıyor fakat karar henüz çıkmıyor. Hangi yorum doğrudur?", "STK gündemi etkilemiş olabilir; nihai karar yetkili kurumların sürecine bağlıdır.", "STK kanunu tek başına çıkarmıştır.", "Kampanyanın hiçbir etkisi olmamıştır.", "Meclis gündemi kamuoyuyla ilişkisizdir.", "Gündeme gelme etki göstergesidir fakat karar yetkisiyle aynı değildir.", None),
        ("analysis", "Medya bir sorunu yalnız tek grubun bakışıyla veriyor. Demokratik tartışma için hangi eksiklik oluşur?", "Farklı kanıt ve görüşlerin görünürlüğü azalır.", "Haber otomatik olarak kanun olur.", "Tek bakış bütün toplumu kesin temsil eder.", "Kaynak çeşitliliği gereksizdir.", "Çoğulcu tartışma ilgili tarafların görüş ve kanıtlarına erişim gerektirir.", None),
        ("error-analysis", "Bir öğrenci “Kamuoyu ne isterse yönetim hiçbir hukuk kuralına bakmadan onu yapmalıdır.” diyor. Hangi düzeltme doğrudur?", "Kamuoyu önemlidir; kararlar hukuk, temel haklar, kaynaklar ve kamu yararıyla birlikte değerlendirilir.", "Kamuoyu bütün hakları kaldırır.", "Yönetim vatandaş görüşünü hiç dikkate almamalıdır.", "Çoğunluk her kararı otomatik meşru yapar.", "Demokratik yönetim katılımı hukuk devleti ilkeleriyle dengeler.", None),
    ])


def fundamental_rights_tasks():
    n = "tr-g06-sosyal-bilgiler-note-012"
    return vrows(n, [
        ("comprehension", "Temel hakların ortak özelliği hangisidir?", "İnsan onurunu korumaya yönelik ve herkese ait olmaları", "Yalnız yetişkinlere verilmesi", "İstenildiğinde keyfî kaldırılması", "Sadece başarılı öğrencilere tanınması", "Temel haklar ayrım gözetmeden insan olmaktan kaynaklanır.", None),
        ("comprehension", "Hakların sınırlandırılmasında hangi ilke önemlidir?", "Kanunilik, meşru amaç ve ölçülülük", "Keyfîlik", "Belirsiz söylenti", "Süresiz ve gerekçesiz yasak", "Sınırlama hukukla öngörülmeli ve amaçla orantılı olmalıdır.", None),
        ("comprehension", "Düşünceyi açıklama özgürlüğü hangi sorumlulukla birlikte kullanılır?", "Başkalarının hak ve itibarına saygı göstermekle", "Doğrulanmamış iftira yaymakla", "Şiddeti teşvik etmekle", "Özel bilgileri izinsiz paylaşmakla", "İfade özgürlüğü başkalarının haklarını ihlal etme yetkisi vermez.", None),
        ("application", "Bir okul etkinliğine engelli öğrencinin erişememesi hâlinde hangi düzenleme hak eşitliğini destekler?", "Fiziksel erişim ve uygun katılım desteği sağlamak", "Öğrenciyi etkinlikten çıkarmak", "İhtiyacı görmezden gelmek", "Yalnız arkadaşından yardım istemesini söylemek", "Makul düzenleme eşit katılım önündeki engeli azaltır.", None),
        ("application", "Bir öğrenci arkadaşının fotoğrafını izinsiz paylaşıyor. Hangi hak etkilenir?", "Özel hayatın ve kişisel verilerin korunması", "Yalnız seyahat hakkı", "Seçme hakkı", "Mülkiyetin devri", "Fotoğraf kişisel veri ve özel yaşamla ilişkilidir; paylaşım için uygun izin gerekir.", None),
        ("application", "Barışçıl bir toplantıda güvenliği sağlamak için en uygun yaklaşım hangisidir?", "Toplantı hakkını korurken somut güvenlik risklerine ölçülü önlem almak", "Bütün toplantıları gerekçesiz yasaklamak", "Katılımcıların görüşünü suç saymak", "Şiddet uygulamayanları cezalandırmak", "Hak ile güvenlik ölçülü ve kanuni tedbirlerle dengelenir.", "flow:Temel hak>Somut risk değerlendirmesi>Ölçülü önlem>Hakkın korunması"),
        ("analysis", "Bir kural yalnız belirli kökenden öğrencilere daha ağır uygulanıyor. Hangi temel ilke ihlal edilir?", "Eşitlik ve ayrımcılık yasağı", "Trafik güvenliği", "Bütçe denkliği", "Bilimsel yöntem", "Benzer durumdaki kişilere köken temelinde farklı muamele ayrımcılık oluşturabilir.", None),
        ("error-analysis", "Bir öğrenci “Özgürlük istediğim her şeyi sonuçlarına bakmadan yapabilmektir.” diyor. Hangi düzeltme doğrudur?", "Özgürlük başkalarının hakları ve hukuk düzeniyle birlikte kullanılır.", "Özgürlük bütün sorumlulukları kaldırır.", "Haklar yalnız tek kişiye aittir.", "Kurallar temel haklarla ilişkisizdir.", "Hakların birlikte yaşanabilmesi karşılıklı sınırlara saygı gerektirir.", None),
        ("error-analysis", "Bir öğrenci “Güvenlik gerekçesi söylenirse her hak süresiz ve sınırsız biçimde durdurulabilir.” diyor. Hangi değerlendirme gerekir?", "Sınırlama somut, kanuni, gerekli ve ölçülü olmalı; keyfî ve süresiz olmamalıdır.", "Güvenlik sözü tek başına yeterlidir.", "Haklar hiçbir durumda dikkate alınmaz.", "Süre ve kapsam açıklanmak zorunda değildir.", "Hukuk devleti sınırlamaları gerekçe, kapsam ve denetime bağlar.", None),
    ])


TASK_BUILDERS = [environment_tasks, turkic_world_tasks, first_turkic_states_tasks,
                 islamic_civilization_tasks, change_after_islam_tasks, anatolia_tasks,
                 participation_tasks, fundamental_rights_tasks]


def _label(labels: dict[str, str], qid: str, suffix: str, value: str) -> str:
    key = f"figure.{qid}.{suffix}"
    labels[key] = value
    return key


def table_figure(qid: str, labels: dict[str, str], payload: str) -> dict[str, Any]:
    raw_rows = [segment.split("|") for segment in payload.split(":", 1)[1].split(";")]
    width = max(len(row) for row in raw_rows)
    headers = [_label(labels, qid, f"h{i}", f"Alan {i+1}") for i in range(width)]
    rows_out = [[{"v": value} for value in row + ["—"] * (width - len(row))] for row in raw_rows]
    alt = _label(labels, qid, "alt", "Soruda verilen ilişkileri karşılaştırmalı satırlar hâlinde gösteren tablo; doğru cevap veya yorum içermez.")
    return {"kind": "table", "headerKeys": headers, "rows": rows_out, "altTextKey": alt}


def flow_figure(qid: str, labels: dict[str, str], payload: str) -> dict[str, Any]:
    names = payload.split(":", 1)[1].split(">")
    nodes = [{"id": f"n{i}", "labelKey": _label(labels, qid, f"n{i}", name)}
             for i, name in enumerate(names)]
    edges = [{"from": f"n{i}", "to": f"n{i+1}"} for i in range(len(names) - 1)]
    alt = _label(labels, qid, "alt", "Sorudaki neden, süreç veya sonuç ilişkisini soldan sağa gösteren akış şeması; doğru seçenek belirtilmemiştir.")
    return {"kind": "flow", "nodes": nodes, "edges": edges, "altTextKey": alt}


def timeline_figure(qid: str, labels: dict[str, str], payload: str) -> dict[str, Any]:
    names = payload.split(":", 1)[1].split(";")
    step = 1 / (len(names) + 1)
    events = [{"id": f"e{i}", "position": round(step * (i + 1), 6),
               "labelKey": _label(labels, qid, f"e{i}", name)} for i, name in enumerate(names)]
    alt = _label(labels, qid, "alt", "Soruda kullanılan tarihsel aşamaları soldan sağa kronolojik sırada gösteren zaman çizelgesi; doğru cevap açıklanmamıştır.")
    return {"kind": "timeline", "orientation": "horizontal", "events": events, "altTextKey": alt}


def apply_visual(row: dict[str, Any], item: dict[str, Any], labels: dict[str, str]) -> None:
    payload = item.get("visual_payload")
    if not payload:
        return
    qid = str(row["id"])
    kind = payload.split(":", 1)[0]
    if kind == "table":
        figure, word = table_figure(qid, labels, payload), "tabloyu"
    elif kind == "flow":
        figure, word = flow_figure(qid, labels, payload), "akış şemasını"
    elif kind == "timeline":
        figure, word = timeline_figure(qid, labels, payload), "zaman çizelgesini"
    else:
        raise AssertionError(f"unsupported visual payload: {payload}")
    row["figure"] = figure
    row["question"] = f"Aşağıdaki görseli inceleyiniz. Görseldeki {word} kullanarak cevaplayınız. {row['question']}"
    row["visualRequirement"] = "required"
    row["visualNeed"] = {"level": "required", "role": "evidence",
                         "rationale": "Kronolojik, nedensel veya karşılaştırmalı kanıt yapılandırılmış görsel üzerinden okunur.",
                         "acceptableKinds": [figure["kind"]],
                         "evidenceDimensions": ["süreç veya dönem", "neden-sonuç veya karşılaştırma"]}


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1500:
        raise RuntimeError("validated first fifteen batches must exist before batch 16")
    notes = read_notes_only(SOCIAL_SOURCE)
    tasks = [item for builder in TASK_BUILDERS for item in builder()]
    if len(tasks) != 100:
        raise AssertionError(f"batch 16 must contain 100 tasks, got {len(tasks)}")
    expected_modes = {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
    if Counter(item["mode"] for item in tasks) != expected_modes:
        raise AssertionError(Counter(item["mode"] for item in tasks))
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    rows_out = []
    for local, item in enumerate(tasks, 1):
        row = make_record(local, item, notes[item["note"]], batch=16, number_base=1500)
        apply_visual(row, item, labels)
        rows_out.append(row)
    if Counter(row["subject"] for row in rows_out) != Counter({"Sosyal Bilgiler": 100}):
        raise AssertionError(Counter(row["subject"] for row in rows_out))
    if Counter(row["correctIndex"] for row in rows_out) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer positions are not exactly balanced")
    figure_count = sum(bool(row.get("figure")) for row in rows_out)
    expected_figures = sum(bool(item.get("visual_payload")) for item in tasks)
    if figure_count != expected_figures:
        raise AssertionError((figure_count, expected_figures))
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":"))
                                 for row in existing + rows_out) + "\n", encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
    print(json.dumps({"batch": 16, "questions": 100, "socialStudies": 100,
                      "figures": figure_count, "total": 1600,
                      "modes": dict(Counter(item["mode"] for item in tasks)),
                      "sourceQuestionReads": 0, "figureSpec": "1.3.0"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
