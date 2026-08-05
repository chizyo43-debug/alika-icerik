# -*- coding: utf-8 -*-
"""MAT.5.3.1 'Temel geometrik çizimler' ailesinin yeniden üretimi (A3).

Neden: 21 soru 5 kalıbın sayı değiştirilmiş tekrarıydı; çeldiriciler her
soruda aynı dolgu havuzundan geliyordu ('yalnız silgi', 'hesap makinesi ve
gönye') ve 21 sorunun 9'unda doğru cevap 'cetvel ve pergel'di. Öğrenci
çizimi bilmeden eleyebiliyordu.

Yeni tasarım:
- 8 farklı çizim türü (orta dikme, açı, açıortay, çember, dik doğru,
  paralel doğru, uzunluk aktarma, eş açı aktarma).
- Çeldiriciler GERÇEK araç çiftleri; her biri o çizim için neden yetmediğini
  söyleyen bir gerekçeyle eşleşiyor. Silgi/hesap makinesi yok.
- Soru biçimleri değişken: araç seçme, adım sırası, gereksiz araç bulma,
  hata teşhisi, koşul gerekçelendirme.
- İpucu 1-4 cevabı vermez; 5. ipucu tam çözümdür.

choices/correct/distractorWhy/hints/explanation TEK birim olarak üretildi
(AUTHORING_RULES.md §1).
"""

# (id, level, soru, şıklar, doğru indeks, gerekçeler, açıklama, ipuçları, zorluk)
YENI = [
    (
        "tr.g05.mat.5-3-1.q001", 1,
        "Bir doğru parçasının orta dikmesini pergelle çizerken pergel açıklığı "
        "neden parçanın yarısından büyük seçilir?",
        ["İki uçtan çizilen yaylar ancak o zaman kesişir",
         "Pergel açıklığı büyüdükçe çizgi daha ince olur",
         "Açıklık büyüdükçe doğru parçası da uzar",
         "Küçük açıklıkta gönye kullanmak zorunlu olur"],
        0,
        ["doğru",
         "Açıklık çizginin kalınlığını değil, yayların kesişip kesişmediğini belirler.",
         "Pergel açıklığı çizilmiş doğru parçasının uzunluğunu değiştirmez.",
         "Orta dikme pergelle çizilir; açıklık küçükse gönyeye geçilmez, açıklık büyütülür."],
        "Yaylar iki uçtan eşit açıklıkla çizilir. Açıklık parçanın yarısından "
        "küçükse yaylar birbirine ulaşamaz ve kesişme noktası oluşmaz; orta "
        "dikme bu kesişim noktalarından geçtiği için çizim tamamlanamaz.",
        ["İki uçtan çizilen yayların birbirine ulaşması gerektiğini düşün.",
         "Açıklık parçanın yarısı kadar olsaydı yaylar nerede buluşurdu?",
         "Orta dikmenin hangi noktalardan geçtiğini hatırla.",
         "Kesişme noktası oluşmazsa çizimin hangi adımı yapılamaz?",
         "Tam çözüm: yaylar iki uçtan eşit açıklıkla çizilir; açıklık parçanın "
         "yarısından küçükse yaylar kesişmez, orta dikme geçireceğimiz nokta "
         "oluşmaz. Bu yüzden açıklık yarıdan büyük seçilir."],
        "2 adım; ön bilgi: orta dikme tanımı ve pergel açıklığının yay yarıçapı "
        "olduğu; çeldiriciler yakın; beceri: gerekçelendirme",
    ),
    (
        "tr.g05.mat.5-3-1.q002", 2,
        "Bir ışının başlangıç noktasında 45°'lik açı çizilecektir. Açıölçer "
        "doğru yerleştirildikten sonra hangi adım gelir?",
        ["Açıölçerin merkezini ışının başlangıç noktasına oturtmak",
         "45° işaretini bulup noktalamak ve bu noktayla köşeyi birleştirmek",
         "Pergelle 45°'lik yay çizmek",
         "Gönyeyi ışının üstüne koyup 45°'yi okumak"],
        1,
        ["Bu, açıölçerin yerleştirilmesi adımıdır; soru ondan sonrasını istiyor.",
         "doğru",
         "Pergel yay çizer ama derece ölçüsünü işaretleyemez; 45° pergelle bulunamaz.",
         "Gönyenin açıları sabittir (90°, 45°, 30°, 60°); ölçü okumak için kullanılmaz."],
        "Açıölçer yerleştirildikten sonra ölçeğinde 45° işareti bulunur, bir "
        "nokta konur ve bu nokta ışının başlangıç noktasıyla birleştirilerek "
        "ikinci ışın oluşturulur.",
        ["Açıölçer yerine oturduktan sonra sırada ne kaldığını düşün.",
         "Açının ikinci kolunu oluşturmak için neye ihtiyaç var?",
         "Ölçek üzerindeki işaretin ne işe yaradığını hatırla.",
         "İşaretlenen noktanın hangi noktayla birleştirileceğine karar ver.",
         "Tam çözüm: ölçekte 45° işareti bulunup noktalanır; bu nokta köşeyle "
         "birleştirilince açının ikinci kolu oluşur."],
        "2 adım; ön bilgi: açıölçer ölçeğini okuma ve açının kolları; "
        "çeldiriciler adım sırası üzerinden yakın; beceri: işlem sırası",
    ),
    (
        "tr.g05.mat.5-3-1.q003", 3,
        "Yarıçapı 8 cm olan bir çember çizilecektir. Pergel açıklığı nasıl "
        "ayarlanmalıdır?",
        ["Cetvelde 0 ile 8 cm arası kadar açılmalıdır",
         "Cetvelde 0 ile 16 cm arası kadar açılmalıdır",
         "Açıölçerde 8° kadar açılmalıdır",
         "Gönyenin 8 cm'lik kenarına eşitlenmelidir"],
        0,
        ["doğru",
         "16 cm çapa karşılık gelir; pergel açıklığı yarıçap kadar olmalıdır.",
         "Pergel açıklığı uzunluktur, derece değildir; açıölçerle ayarlanmaz.",
         "Gönye sabit kenarlıdır; istenen her uzunluğu veremez, ölçü cetvelden alınır."],
        "Pergelin iğnesi ile kalemi arasındaki açıklık çemberin yarıçapıdır. "
        "Cetvelde 0 ile 8 cm arası kadar açılan pergel, iğne merkezdeyken 8 cm "
        "yarıçaplı çemberi çizer.",
        ["Pergel açıklığının çemberin hangi ölçüsüne karşılık geldiğini düşün.",
         "Yarıçap ile çap arasındaki ilişkiyi hatırla.",
         "Açıklığı hangi araçla ölçebileceğine karar ver.",
         "8 cm'nin yarıçap mı çap mı olduğunu soru kökünde kontrol et.",
         "Tam çözüm: açıklık yarıçapa eşittir; cetvelde 0-8 cm arası kadar "
         "açılan pergel 8 cm yarıçaplı çemberi verir."],
        "2 adım; ön bilgi: yarıçap-çap ilişkisi ve pergel açıklığının yarıçap "
        "olduğu; çeldiriciler yakın (çap hatası); beceri: ölçü aktarma",
    ),
    (
        "tr.g05.mat.5-3-1.q004", 4,
        "Bir doğruya, doğru üzerinde olmayan P noktasından dik doğru çizilecek. "
        "Öğrencinin elinde yalnız cetvel ve gönye var. Bu çizim yapılabilir mi?",
        ["Yapılamaz; dik çizim yalnız pergelle mümkündür",
         "Yapılamaz; önce açıölçerle 90° işaretlenmelidir",
         "Yapılabilir; gönyenin dik kenarı doğruya dayanır, diğer kenar P'den geçirilir",
         "Yapılabilir; gönye P noktasına konup çember çizilir"],
        2,
        ["Dik çizim pergelle de yapılabilir ama gönye ile de yapılır; tek yol pergel değildir.",
         "Gönyenin kendisi 90° taşır; ayrıca açıölçerle işaretlemeye gerek yoktur.",
         "doğru",
         "Gönye çember çizmez; çember pergelin işidir."],
        "Gönyenin bir dik kenarı verilen doğru üzerine yerleştirilir, gönye "
        "doğru boyunca P noktası diğer dik kenarın üzerine gelene kadar "
        "kaydırılır. Cetvelle bu kenar boyunca çizilen doğru P'den geçer ve "
        "verilen doğruya diktir.",
        ["Gönyenin üzerinde hazır bulunan açıyı hatırla.",
         "Gönyeyi doğru üzerinde kaydırmanın ne işe yarayacağını düşün.",
         "P noktasının gönyenin hangi kenarına gelmesi gerektiğine karar ver.",
         "Çizimin hem P'den geçmesi hem dik olması koşullarını birlikte kontrol et.",
         "Tam çözüm: gönyenin dik kenarı doğruya dayanır, gönye P diğer kenara "
         "gelene kadar kaydırılır, cetvelle o kenar boyunca çizilir."],
        "3 adım; ön bilgi: gönyenin sabit 90° açısı ve dik doğru tanımı; "
        "çeldiriciler hem 'yapılamaz' hem yanlış yöntem içeriyor; beceri: "
        "yöntem doğrulama",
    ),
    (
        "tr.g05.mat.5-3-1.q005", 5,
        "Bir doğru parçasının uzunluğu, ölçüsü okunmadan başka bir doğru "
        "üzerine aynen aktarılacaktır. Bu iş için hangi araç şarttır?",
        ["Açıölçer", "Gönye", "Pergel", "Yalnız cetvel"],
        2,
        ["Açıölçer derece ölçer; uzunluk taşıyamaz.",
         "Gönyenin kenarları sabittir; verilen her uzunluğu taşıyamaz.",
         "doğru",
         "Cetvelle taşımak için önce ölçüyü okumak gerekir; soru okumadan aktarmayı istiyor."],
        "Pergel, iki uç arasındaki açıklığı değiştirmeden koruyabildiği için "
        "uzunluğu sayıya çevirmeden taşır. Açıklık parçanın uçlarına ayarlanır, "
        "sonra yeni doğru üzerinde aynı açıklıkla işaretlenir.",
        ["Uzunluğu okumadan taşımanın ne demek olduğunu düşün.",
         "Hangi aracın açıklığını sabit tutabildiğini hatırla.",
         "Ölçüyü sayıya çevirmek gerekiyor mu, kontrol et.",
         "Sabit kenarlı araçların istenen her uzunluğu veremeyeceğini göz önüne al.",
         "Tam çözüm: pergel açıklığı parçanın uçlarına ayarlanır ve "
         "değiştirilmeden yeni doğruya taşınır; ölçü okunmaz."],
        "2 adım; ön bilgi: pergelin açıklığı koruma özelliği; çeldiriciler "
        "'cetvelle de olur' yanılgısını hedefliyor; beceri: araç seçimi gerekçelendirme",
    ),
    (
        "tr.g05.mat.5-3-1.q006", 1,
        "Aşağıdaki çizimlerden hangisi pergel kullanılmadan yapılabilir?",
        ["Bir açının açıortayını çizmek",
         "Verilen bir uzunluğu ölçü okumadan aktarmak",
         "Merkezi belli bir çember çizmek",
         "Verilen bir doğruya gönyeyle dik doğru çizmek"],
        3,
        ["Açıortay eş yaylar gerektirir; yaylar pergelle çizilir.",
         "Ölçü okumadan aktarma pergelin açıklığını korumasıyla olur.",
         "Çember pergelin temel işidir.",
         "doğru"],
        "Gönyenin üzerinde hazır 90°'lik açı bulunur; dik doğru bu açı "
        "kullanılarak cetvelle çizilir, pergele gerek kalmaz. Diğer üç çizim "
        "yay çizmeyi veya açıklık korumayı gerektirdiği için pergelsiz yapılamaz.",
        ["Her seçeneğin yay çizmeyi gerektirip gerektirmediğine bak.",
         "Hangi araçta hazır bir dik açı bulunduğunu hatırla.",
         "Açıklık korumanın hangi araca ait olduğunu düşün.",
         "Yay gerektirmeyen tek çizimi ayır.",
         "Tam çözüm: gönyede hazır 90° vardır; dik doğru gönye ve cetvelle "
         "çizilir. Açıortay, uzunluk aktarma ve çember yay ya da sabit açıklık "
         "gerektirdiği için pergelsiz olmaz."],
        "2 adım; ön bilgi: dört çizimin de yöntemi; çeldiriciler ayırt edici "
        "(hepsi gerçek çizim); beceri: sınıflandırma",
    ),
    (
        "tr.g05.mat.5-3-1.q007", 2,
        "Bir açının açıortayı çizilirken köşeye pergel batırılıp bir yay "
        "çizilir. Bu yayın amacı nedir?",
        ["Açının ölçüsünü derece cinsinden vermek",
         "Açının iki kolu üzerinde köşeye eşit uzaklıkta iki nokta belirlemek",
         "Açıyı iki eş parçaya doğrudan bölmek",
         "Açının kollarını uzatmak"],
        1,
        ["Derece ölçüsü açıölçerle okunur; yay ölçü vermez.",
         "doğru",
         "Bu yay tek başına bölmez; bölme, bu iki noktadan çizilen yayların "
         "kesişimiyle tamamlanır.",
         "Kolların uzunluğu açıortay çiziminde değişmez, uzatma gerekmez."],
        "Köşe merkezli yay, açının iki kolunu keserek köşeye eşit uzaklıkta iki "
        "nokta verir. Açıortay çizimi bu iki noktadan eş yarıçaplı yaylar "
        "çizilip kesişimlerinin köşeyle birleştirilmesiyle tamamlanır.",
        ["Yayın açının kollarını nerede kestiğine dikkat et.",
         "Kesişen noktaların köşeye uzaklıklarını karşılaştır.",
         "Bu iki noktanın sonraki adımda ne işe yarayacağını düşün.",
         "Açıortayın tek bir yayla mı yoksa birkaç adımla mı tamamlandığını hatırla.",
         "Tam çözüm: köşe merkezli yay, kollar üzerinde köşeye eşit uzaklıkta "
         "iki nokta verir; sonraki yaylar bu noktalardan çizilir."],
        "2 adım; ön bilgi: açıortay çizim basamakları; çeldiriciler adımın "
        "amacını kaydırıyor; beceri: adımın işlevini açıklama",
    ),
    (
        "tr.g05.mat.5-3-1.q008", 3,
        "Bir öğrenci 6 cm yarıçaplı çember çizerken pergeli 6 cm açtı, iğneyi "
        "merkeze batırdı ama çizim sırasında açıklığın 5 cm'ye düştüğünü fark "
        "etti. Çizimde ne olur?",
        ["Çember kapanmaz ve iki ucu birbirini tutmaz",
         "Çember daha kalın çizilir",
         "Çemberin merkezi kayar",
         "Çember çizilir ama çapı 5 cm olur"],
        0,
        ["doğru",
         "Açıklık değişmesi kalemin bastırma gücüyle ilgili değildir; çizgi kalınlaşmaz.",
         "İğne merkezde durduğu sürece merkez kaymaz; değişen yarıçaptır.",
         "5 cm yarıçap olurdu, çap değil; ayrıca yarıçap çizim ortasında "
         "değiştiği için tek bir çember oluşmaz."],
        "Çemberin her noktası merkeze eşit uzaklıktadır. Çizim ortasında açıklık "
        "değişirse ilk yay 6 cm, sonraki yay 5 cm uzaklıkta kalır; iki yay aynı "
        "noktada buluşamaz ve çember kapanmaz.",
        ["Çemberin tanımındaki 'eşit uzaklık' koşulunu hatırla.",
         "Açıklık değişince yayın merkeze uzaklığına ne olur, düşün.",
         "İki farklı uzaklıkta çizilen yayların buluşup buluşamayacağını sorgula.",
         "İğnenin yerinden oynamadığına dikkat et; değişen tek şey ne?",
         "Tam çözüm: çemberde her nokta merkeze eşit uzaktadır; açıklık ortada "
         "değişince 6 cm'lik yay ile 5 cm'lik yay buluşamaz, çember kapanmaz."],
        "3 adım; ön bilgi: çember tanımı ve yarıçap sabitliği; çeldiriciler "
        "yakın (çap/yarıçap, merkez kayması); beceri: hata teşhisi",
    ),
    (
        "tr.g05.mat.5-3-1.q009", 4,
        "Verilen bir doğruya paralel bir doğru çizmek için gönye nasıl kullanılır?",
        ["Gönye doğruya dik konur ve yerinden hiç oynatılmadan çizim yapılır",
         "Gönyenin bir kenarı doğruya dayanır, cetvel gönyeye dayanır ve gönye "
         "cetvel boyunca kaydırılır",
         "Gönyenin dik açısı doğrunun ortasına konur ve çevresinde döndürülür",
         "Gönye açıölçerle 180°'ye ayarlanıp doğruya yaslanır"],
        1,
        ["Gönye oynatılmazsa yalnız tek bir doğru çizilir; paralel için kaydırma gerekir.",
         "doğru",
         "Gönyeyi döndürmek açıyı değiştirir; paralellik bozulur.",
         "Gönye ayarlanabilir bir araç değildir; açıları sabittir."],
        "Gönyenin bir kenarı verilen doğruya dayanır. Cetvel gönyenin diğer "
        "kenarına sabit tutulur ve gönye cetvel boyunca kaydırılır. Gönyenin "
        "doğruya dayanan kenarı yönünü koruduğu için çizilen yeni doğru verilen "
        "doğruya paraleldir.",
        ["Paralel doğruların yönünün aynı kalması gerektiğini hatırla.",
         "Gönyeyi kaydırırken yönünü neyin sabit tuttuğunu düşün.",
         "Cetvelin bu çizimdeki görevini belirle.",
         "Döndürme ile kaydırma arasındaki farkın açıya etkisini karşılaştır.",
         "Tam çözüm: gönyenin bir kenarı doğruya dayanır, cetvel diğer kenara "
         "sabitlenir, gönye cetvel boyunca kaydırılır; yön korunduğu için yeni "
         "doğru paraleldir."],
        "3 adım; ön bilgi: paralellik ve gönyenin yön koruması; çeldiriciler "
        "kaydırma/döndürme ayrımını hedefliyor; beceri: yöntem kurma",
    ),
    (
        "tr.g05.mat.5-3-1.q010", 5,
        "Bir açının eşi, ölçüsü hiç okunmadan başka bir ışının üzerine "
        "aktarılacaktır. Aşağıdakilerden hangisi bu çizimde kullanılmaz?",
        ["Pergel", "Cetvel", "Açıölçer", "Kalem"],
        2,
        ["Pergel hem yayları çizer hem açıklığı korur; şarttır.",
         "Cetvel ışınları çizmek için gereklidir.",
         "doğru",
         "Kalem her çizimde kullanılır."],
        "Eş açı aktarımında köşeden yay çizilir, aynı yay yeni ışında "
        "tekrarlanır ve kolların arasındaki açıklık pergelle taşınır. Ölçü "
        "okunmadığı için açıölçere hiç ihtiyaç duyulmaz.",
        ["'Ölçüsü okunmadan' ifadesinin hangi aracı devre dışı bıraktığını düşün.",
         "Açıklığı taşıyan aracın hangisi olduğunu hatırla.",
         "Işınları çizmek için neye ihtiyaç olduğuna bak.",
         "Kalan araçlardan hangisinin görevi yalnız derece okumak, belirle.",
         "Tam çözüm: eş açı aktarımı yay ve açıklık taşımayla yapılır; ölçü "
         "okunmadığı için açıölçer kullanılmaz."],
        "2 adım; ön bilgi: eş açı aktarım yöntemi; çeldiriciler gerçekten "
        "kullanılan araçlar; beceri: gereksiz aracı ayırt etme",
    ),
    (
        "tr.g05.mat.5-3-1.q011", 1,
        "Orta dikme çizimi tamamlandığında elde edilen doğru, verilen doğru "
        "parçasıyla nasıl bir ilişki içindedir?",
        ["Parçayı iki eş parçaya böler ve parçaya diktir",
         "Parçayı iki eş parçaya böler ama dik değildir",
         "Parçaya diktir ama ortasından geçmez",
         "Parçanın bir ucundan geçer ve ona paraleldir"],
        0,
        ["doğru",
         "Orta dikme adındaki 'dik' sözcüğü diklik koşulunu da taşır.",
         "'Orta' sözcüğü parçanın orta noktasından geçmeyi gerektirir.",
         "Bir doğru, kestiği parçaya paralel olamaz."],
        "Orta dikme, doğru parçasının orta noktasından geçen ve parçaya dik olan "
        "doğrudur. Adındaki iki sözcük iki koşulu birden söyler: 'orta' orta "
        "noktadan geçmeyi, 'dikme' 90°'lik açıyı.",
        ["Çizimin adındaki iki sözcüğü ayrı ayrı düşün.",
         "'Orta' sözcüğünün hangi koşulu getirdiğini belirle.",
         "'Dikme' sözcüğünün hangi açıyı gerektirdiğini hatırla.",
         "İki koşulun birlikte sağlanması gerektiğini kontrol et.",
         "Tam çözüm: orta dikme hem parçanın orta noktasından geçer hem de "
         "parçaya diktir; iki koşul birlikte sağlanır."],
        "1 adım; ön bilgi: orta dikme tanımı; çeldiriciler koşullardan birini "
        "eksik bırakıyor; beceri: tanım hatırlama",
    ),
    (
        "tr.g05.mat.5-3-1.q012", 2,
        "Açıölçerle 120°'lik açı çizen bir öğrenci, açıölçerin iki ölçeğini "
        "karıştırıp 60° çizmiştir. Bu hatayı çizimine bakarak nasıl fark eder?",
        ["Açının dar mı geniş mi göründüğünü kontrol ederek",
         "Kolların uzunluklarını ölçerek",
         "Açının köşesini silip yeniden çizerek",
         "Pergelle açının içine yay çizerek"],
        0,
        ["doğru",
         "Açının ölçüsü kolların uzunluğuna bağlı değildir; uzunluk ölçmek hatayı göstermez.",
         "Silip yeniden çizmek aynı ölçek hatasını tekrarlamaya açıktır; kontrol sağlamaz.",
         "Yay çizmek açının ölçüsünü değiştirmez ve okumayı doğrulamaz."],
        "120° geniş açı, 60° ise dar açıdır. Öğrenci çizdiği açının 90°'den "
        "büyük mü küçük mü göründüğüne bakarsa, dar bir açı çizmiş olduğunu "
        "hemen görür ve yanlış ölçeği okuduğunu anlar.",
        ["120° ile 60°'nin açı türlerini karşılaştır.",
         "Çizilen açının 90°'den büyük mü küçük mü olduğuna bakmanın ne "
         "söyleyeceğini düşün.",
         "Kol uzunluğunun açı ölçüsünü değiştirip değiştirmediğini hatırla.",
         "Bir kontrolün hatayı gerçekten yakalayabilmesi için neye bakması "
         "gerektiğine karar ver.",
         "Tam çözüm: 120° geniş, 60° dardır; çizilen açının dar göründüğünü "
         "gören öğrenci yanlış ölçeği okuduğunu anlar."],
        "3 adım; ön bilgi: dar/geniş açı ayrımı ve açıölçerin çift ölçeği; "
        "çeldiriciler işe yaramayan kontroller; beceri: hata teşhisi",
    ),
    (
        "tr.g05.mat.5-3-1.q013", 3,
        "Merkezi O olan bir çember çizildikten sonra çemberin üzerinde bir A "
        "noktası işaretlendi. |OA| uzunluğu neye eşittir?",
        ["Çemberin çapına", "Çemberin yarıçapına",
         "Çemberin çevresine", "Pergelin toplam boyuna"],
        1,
        ["Çap merkezden geçen ve iki ucu çember üzerinde olan uzunluktur; "
         "|OA| bunun yarısıdır.",
         "doğru",
         "Çevre, çemberin etrafını dolaşan uzunluktur; bir doğru parçası değildir.",
         "Pergelin boyu çizimle ilgisizdir; belirleyici olan iğne-kalem açıklığıdır."],
        "Çember üzerindeki her nokta merkeze eşit uzaklıktadır ve bu uzaklık "
        "yarıçaptır. A noktası çember üzerinde olduğuna göre |OA| yarıçaptır; "
        "aynı zamanda çizimde kullanılan pergel açıklığına eşittir.",
        ["Çemberin tanımındaki merkeze uzaklık koşulunu hatırla.",
         "A noktasının çember üzerinde olmasının ne anlama geldiğini düşün.",
         "Çap ile yarıçap arasındaki ilişkiyi karşılaştır.",
         "Bir uzunluk mu yoksa bir eğri boyu mu arandığına dikkat et.",
         "Tam çözüm: çember üzerindeki her nokta merkeze yarıçap kadar uzaktır; "
         "A çember üzerinde olduğu için |OA| yarıçaptır."],
        "1 adım; ön bilgi: çember tanımı, yarıçap ve çap; çeldiriciler yakın "
        "(çap/çevre karışması); beceri: kavram ilişkilendirme",
    ),
    (
        "tr.g05.mat.5-3-1.q014", 4,
        "Bir öğrenci P noktasından geçen dik doğruyu gönyeyle çizdi ama gönyeyi "
        "doğru üzerinde kaydırmadan, göz kararı yerleştirdi. Bu çizimin en "
        "olası kusuru nedir?",
        ["Doğru P'den geçer ama verilen doğruya tam dik olmayabilir",
         "Doğru dik olur ama P'den geçmeyebilir",
         "Doğrunun uzunluğu yanlış olur",
         "Doğru verilen doğruya paralel çıkar"],
        1,
        ["Gönyenin dik kenarı doğruya dayandığı sürece diklik korunur; "
         "kaymayan şey diklik değildir.",
         "doğru",
         "Bir doğrunun uzunluğu yoktur; doğru iki yönde sınırsızdır.",
         "Gönye kullanıldığı sürece çizim dik olur; paralel çıkması beklenmez."],
        "Gönyenin dik kenarı verilen doğruya dayandığı için diklik zaten "
        "sağlanır. Kaydırma işleminin amacı P noktasını gönyenin diğer kenarına "
        "getirmektir; kaydırmadan yerleştirilirse çizilen dik doğru P'nin "
        "yanından geçer.",
        ["Gönyenin hangi özelliğinin dikliği güvenceye aldığını düşün.",
         "Kaydırma adımının hangi koşulu sağladığını belirle.",
         "İki koşuldan (dik olma, P'den geçme) hangisinin araçtan geldiğine bak.",
         "Kaydırma yapılmazsa hangi koşulun boşta kaldığını sorgula.",
         "Tam çözüm: diklik gönyenin sabit açısından gelir, korunur; kaydırma "
         "P'den geçme koşulunu sağlar. Kaydırma yapılmazsa doğru P'den geçmez."],
        "3 adım; ön bilgi: gönyeyle dik çizim adımları ve iki koşulun ayrılması; "
        "çeldiriciler koşulları takas ediyor; beceri: hata teşhisi",
    ),
    (
        "tr.g05.mat.5-3-1.q015", 5,
        "Aşağıdaki adımlar hangi çizimi anlatır?\n"
        "1) Köşeye pergel batırılıp kolları kesen bir yay çizilir.\n"
        "2) Yayın kolları kestiği iki noktadan eş açıklıkla yaylar çizilir.\n"
        "3) Bu yayların kesişimi köşeyle birleştirilir.",
        ["Orta dikme çizimi", "Açıortay çizimi",
         "Paralel doğru çizimi", "Eş uzunluk aktarma"],
        1,
        ["Orta dikme bir doğru parçasının uçlarından başlar; burada başlangıç "
         "bir köşe ve iki koldur.",
         "doğru",
         "Paralel çizimde yay kullanılmaz; gönye kaydırılır.",
         "Uzunluk aktarmada tek bir açıklık taşınır; kesişen yaylar oluşturulmaz."],
        "Adımlar bir açının köşesinden başlıyor ve kolları kesen yayla iki eşit "
        "uzaklıkta nokta üretiyor. Bu noktalardan çizilen eş yayların kesişimi "
        "köşeyle birleştirildiğinde açıyı iki eş parçaya bölen açıortay elde "
        "edilir.",
        ["Adımların bir doğru parçasından mı yoksa bir açıdan mı başladığına bak.",
         "Birinci adımda yayın neyi kestiğine dikkat et.",
         "Son adımda kesişimin hangi noktayla birleştirildiğini düşün.",
         "Sonuçta ortaya çıkan doğrunun açıyı nasıl ayırdığını hayal et.",
         "Tam çözüm: köşeden başlayıp kolları kesen yay, ardından eş yayların "
         "kesişimi ve köşeyle birleştirme — bu açıortay çizimidir."],
        "3 adım; ön bilgi: dört çizimin adım dizileri; çeldiriciler gerçek "
        "çizimler; beceri: adım dizisinden çizimi tanıma",
    ),
    (
        "tr.g05.mat.5-3-1.q016", 1,
        "Aşağıdaki araçlardan hangisi üzerinde hazır açı ölçüleri bulunur ve "
        "bu yüzden 90°'lik çizimlerde ölçmeden kullanılabilir?",
        ["Pergel", "Cetvel", "Gönye", "Silgi"],
        2,
        ["Pergel yay çizer; üzerinde açı ölçüsü yoktur.",
         "Cetvelde uzunluk ölçeği vardır, açı ölçeği yoktur.",
         "doğru",
         "Silgi bir çizim aracı değildir."],
        "Gönyenin köşelerindeki açılar sabittir ve içlerinden biri 90°'dir. Bu "
        "yüzden dik çizimlerde açıölçerle ölçmeye gerek kalmadan doğrudan "
        "kullanılabilir.",
        ["Araçların üzerinde ne tür ölçek bulunduğunu karşılaştır.",
         "Hangi aracın kenarları arasındaki açının değişmediğini düşün.",
         "90°'yi ölçmeden elde etmenin yolunu ara.",
         "Uzunluk ölçeği ile açı ölçeğini birbirinden ayır.",
         "Tam çözüm: gönyenin açıları sabittir ve biri 90°'dir; dik çizimde "
         "ölçmeden kullanılır."],
        "1 adım; ön bilgi: çizim araçlarının özellikleri; çeldiriciler diğer "
        "araçlar; beceri: araç tanıma",
    ),
    (
        "tr.g05.mat.5-3-1.q017", 2,
        "Açıölçer bir açının köşesine yerleştirilirken hangi iki koşul birlikte "
        "sağlanmalıdır?",
        ["Merkez köşeye gelmeli ve sıfır çizgisi bir kolun üstüne oturmalı",
         "Merkez köşeye gelmeli ve açıölçer kolların dışında kalmalı",
         "Sıfır çizgisi köşeye gelmeli ve merkez bir kolun üstüne oturmalı",
         "Açıölçer kolların ortasına konmalı ve iki ölçek birden okunmalı"],
        0,
        ["doğru",
         "Açıölçerin kolların dışında kalması ölçümü imkânsızlaştırır; "
         "ölçek kolların üzerine gelmelidir.",
         "Merkez ile sıfır çizgisinin görevleri yer değiştirmiş; merkez köşeye gelir.",
         "İki ölçek aynı anda okunmaz; hangisinin okunacağı sıfır çizgisinin "
         "hangi kolda olduğuna bağlıdır."],
        "Açıölçerin merkez işareti açının köşesine oturtulur, sıfır çizgisi de "
        "kollardan birinin üzerine getirilir. İki koşul birlikte sağlanmazsa "
        "ölçek yanlış yerden okunur.",
        ["Açıölçerin üzerindeki merkez işaretinin nereye geldiğini düşün.",
         "Sıfır çizgisinin görevinin ne olduğunu hatırla.",
         "İki koşulun birbirinin yerine geçip geçemeyeceğini sorgula.",
         "Koşullardan biri eksik kalırsa okumaya ne olacağını düşün.",
         "Tam çözüm: merkez köşeye oturur, sıfır çizgisi bir kolun üstüne "
         "gelir; ölçü diğer kolun geçtiği yerden okunur."],
        "2 adım; ön bilgi: açıölçerin merkez ve sıfır çizgisi; çeldiriciler "
        "koşulları takas ediyor; beceri: araç kullanımı",
    ),
    (
        "tr.g05.mat.5-3-1.q018", 3,
        "Aynı merkezli, yarıçapları 3 cm ve 5 cm olan iki çember çizilecektir. "
        "Çizim sırasında hangi işlem yapılmaz?",
        ["Pergelin iğnesi aynı noktada tutulur",
         "Pergel açıklığı iki çizim arasında değiştirilir",
         "İki çember arasında merkez yeni bir yere taşınır",
         "Her çizimde açıklık cetvelle ayarlanır"],
        2,
        ["Aynı merkezli çemberlerde iğne yerinden oynatılmaz.",
         "Yarıçaplar farklı olduğu için açıklık mutlaka değiştirilir.",
         "doğru",
         "Her yarıçap cetvelle ayarlanır; bu gerekli bir adımdır."],
        "'Aynı merkezli' ifadesi iki çemberin merkezinin ortak olduğunu söyler. "
        "Bu yüzden iğne yerinden oynatılmaz; değişen tek şey pergel açıklığıdır: "
        "önce 3 cm, sonra 5 cm.",
        ["'Aynı merkezli' ifadesinin neyi sabitlediğini belirle.",
         "İki çemberin farklı olan özelliğinin ne olduğunu düşün.",
         "Hangi büyüklüğün değişmesi, hangisinin sabit kalması gerektiğini ayır.",
         "Soru 'yapılmaz' dediği için sabit kalması gereken şeyi ara.",
         "Tam çözüm: merkez ortaktır, iğne oynatılmaz; yalnız açıklık 3 cm'den "
         "5 cm'ye değiştirilir."],
        "2 adım; ön bilgi: aynı merkezli çember kavramı; çeldiriciler gerekli "
        "adımları içeriyor; beceri: olumsuz soru kökünü çözme",
    ),
    (
        "tr.g05.mat.5-3-1.q019", 4,
        "Bir doğru parçasının orta dikmesi çizildi. Bu doğru üzerinde alınan "
        "herhangi bir noktanın, parçanın iki ucuna uzaklıkları için ne söylenebilir?",
        ["Uzaklıklar birbirine eşittir",
         "Uca yakın olan uzaklık her zaman daha kısadır",
         "Uzaklıklar parçanın uzunluğuna eşittir",
         "Uzaklıklar yalnız orta noktada eşittir"],
        0,
        ["doğru",
         "Orta dikme üzerindeki her nokta iki uca eşit uzaktadır; bir uca "
         "daha yakın olmaz.",
         "Uzaklıkların parça uzunluğuyla eşit olması için özel bir neden yoktur.",
         "Eşitlik yalnız orta noktada değil, orta dikmenin bütün noktalarında geçerlidir."],
        "Orta dikme, doğru parçasının uçlarına eşit uzaklıktaki noktaların "
        "oluşturduğu doğrudur. Bu yüzden üzerinde alınan her nokta için iki uca "
        "olan uzaklıklar eşittir; çizim de zaten bu özellikten yararlanılarak "
        "eş yaylarla yapılır.",
        ["Orta dikmenin nasıl çizildiğini, hangi yayların kullanıldığını hatırla.",
         "Eş yarıçaplı yayların kesişim noktasının iki uca uzaklığını düşün.",
         "Bu özelliğin yalnız kesişim noktasında mı geçerli olduğunu sorgula.",
         "Orta noktanın da bu doğru üzerinde olduğunu göz önüne al.",
         "Tam çözüm: orta dikme, uçlara eşit uzaklıktaki noktaların doğrusudur; "
         "üzerindeki her nokta için iki uzaklık eşittir."],
        "3 adım; ön bilgi: orta dikmenin eş uzaklık özelliği ve çizim yöntemiyle "
        "bağı; çeldiriciler kısmi doğrular; beceri: özellik genelleme",
    ),
    (
        "tr.g05.mat.5-3-1.q020", 5,
        "Elinde yalnız pergel ve cetvel bulunan bir öğrenci, aşağıdakilerden "
        "hangisini yapamaz?",
        ["Bir doğru parçasının orta dikmesini çizmek",
         "Bir açının açıortayını çizmek",
         "Ölçüsü 37° olan bir açı çizmek",
         "Verilen bir uzunluğu başka bir doğruya aktarmak"],
        2,
        ["Orta dikme eş yaylarla, yani pergel ve cetvelle çizilir.",
         "Açıortay da eş yaylarla çizilir; pergel ve cetvel yeter.",
         "doğru",
         "Uzunluk aktarma pergelin açıklığını korumasıyla yapılır."],
        "Pergel ve cetvel yay çizmeye ve uzunluk taşımaya yarar; belirli bir "
        "derece ölçüsünü işaretleyemez. 37° gibi verilen bir ölçüyü çizmek için "
        "açıölçer gerekir. Diğer üç çizim eş yaylara dayandığı için bu iki "
        "araçla yapılabilir.",
        ["Her seçeneğin derece ölçüsü gerektirip gerektirmediğine bak.",
         "Pergelin ve cetvelin ne ölçebildiğini hatırla.",
         "Eş yaylarla yapılabilen çizimleri bir kenara ayır.",
         "Geriye kalan tek çizimin neden farklı olduğunu düşün.",
         "Tam çözüm: pergel ve cetvel derece ölçemez; 37°'lik açı açıölçer "
         "ister. Orta dikme, açıortay ve uzunluk aktarma eş yaylarla yapılır."],
        "3 adım; ön bilgi: dört çizimin araç gereksinimi; çeldiriciler gerçek "
        "çizimler; beceri: araç-yöntem eşleştirme ve eleme",
    ),
    (
        "tr.g05.mat.5-3-1.q021", 1,
        "Pergelin çizim sırasındaki temel görevi nedir?",
        ["Uzunluk ölçüsünü santimetre cinsinden okumak",
         "Sabit bir açıklıkla yay ve çember çizmek",
         "Doğruları birbirine dik hâle getirmek",
         "Açıların derece ölçüsünü belirlemek"],
        1,
        ["Santimetre okuma cetvelin görevidir.",
         "doğru",
         "Diklik gönyenin sabit açısıyla ya da orta dikme çizimiyle sağlanır; "
         "pergel tek başına dik yapmaz.",
         "Derece ölçüsünü açıölçer belirler."],
        "Pergel, iğnesi ile kalemi arasındaki açıklığı koruyarak yay ve çember "
        "çizer. Bu özellik sayesinde eş uzunluklar taşınabilir ve orta dikme, "
        "açıortay gibi çizimlerin temeli olan eş yaylar oluşturulabilir.",
        ["Pergelin iki ucu arasındaki açıklığın ne işe yaradığını düşün.",
         "Pergelle çizilen şeklin biçimini hatırla.",
         "Diğer araçların görevlerini pergelinkinden ayır.",
         "Ölçü okuma ile ölçü taşıma arasındaki farkı karşılaştır.",
         "Tam çözüm: pergel sabit açıklıkla yay ve çember çizer; bu sayede eş "
         "uzunluklar taşınır ve eş yaylar oluşturulur."],
        "1 adım; ön bilgi: pergelin işlevi; çeldiriciler diğer araçların "
        "görevleri; beceri: araç-işlev eşleştirme",
    ),
]
