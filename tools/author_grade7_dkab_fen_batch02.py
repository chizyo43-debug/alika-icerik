#!/usr/bin/env python3
"""Append Grade 7 batch 02: 91 Religion and Ethics, 9 Science questions."""
from __future__ import annotations

from collections import Counter
import json
from typing import Any

from build_unique_question_banks import ROOT
from author_grade6_mixed_batch03 import make_question, read_notes_only
from author_grade7_dkab_batch01 import CASES as DKAB_BASE, LABELS_OUTPUT, OUTPUT


DKAB_SOURCE = ROOT / "turkiye/7-sinif/din-kulturu-ve-ahlak-bilgisi/din-kulturu-ve-ahlak-bilgisi-tum.jsonl"
FEN_SOURCE = ROOT / "turkiye/7-sinif/fen-bilimleri/fen-bilimleri-tum.jsonl"


FEN_CASES = [
    ("tr-g07-fen-note-fb-7-5-2-4-q0385-q0388", "Bir öğrenci H2O ve CO2 formüllerindeki alt indisleri yorumluyor.", "H2O'da iki hidrojen ve bir oksijen, CO2'de bir karbon ve iki oksijen atomu bulunduğu modelle doğrulanıyor.", "Bileşik formülünde element sembolü atom türünü, alt indis ise o elementin bir birimdeki atom sayısını gösterir.", "Sembolleri büyük-küçük harfe dikkat ederek okuyup görünmeyen alt indisi bir kabul etmek gerekir.", "Modeldeki atom sayıları formülle aynıysa sembol ve alt indisler doğru yorumlanmıştır.", ["CO2 formülündeki 2, iki karbon atomu bulunduğunu gösterir.", "Alt indis bütün formülün önündeki katsayıyla aynı görevdedir.", "Element sembollerinde büyük ve küçük harf kullanımı anlamı değiştirmez."], "Kimyasal formül atom türü ve sayısını birlikte kodlar; sembol yazımı ile alt indis birbirine karıştırılmaz."),
    ("tr-g07-fen-note-fb-7-5-3-1-q0389-q0392", "Tuzlu su ile kumlu su karıştırılıp bekletiliyor.", "Tuzlu su tek görünümünü korurken kum tanecikleri bir süre sonra kabın dibinde birikiyor.", "Her yerinde aynı özellik gösteren karışım homojen, farklı kısımları ayırt edilebilen karışım heterojendir.", "Karışımları aynı kap, süre ve miktar koşullarında gözleyip görünüm ile çökelme kaydını birlikte değerlendirmek gerekir.", "Kumlu sudaki çökelme, dağılımın zamanla her yerde aynı kalmadığını ve heterojen olduğunu gösterir.", ["Tek görünümde olan her madde mutlaka saf maddedir.", "Kum dibe çöktüğü için kumlu su homojen karışımdır.", "Karışımı sınıflandırmak için gözlem ve bekleme süresi gereksizdir."], "Karışım sınıflandırması saf madde kararıyla karıştırılmaz; gözlenebilir dağılım ve zaman içindeki değişim kanıt olarak kullanılır."),
    ("tr-g07-fen-note-fb-7-5-3-2", "Eşit miktarda şeker, biri sıcak biri soğuk iki su kabına aynı anda ekleniyor.", "Aynı karıştırma koşulunda şeker sıcak suda daha kısa sürede görünmez hâle geliyor.", "Sıcaklığın çözünme hızına etkisini sınamak için diğer değişkenler sabit tutulup çözünme süresi karşılaştırılır.", "Su ve şeker miktarını, tanecik boyutunu ve karıştırmayı eşitleyip yalnız sıcaklığı değiştirmek gerekir.", "Yalnız sıcaklığın değiştiği düzende süre farkı, sıcaklığın çözünme hızına etkisiyle ilişkilendirilebilir.", ["Aynı deneyde sıcaklıkla birlikte şeker miktarı da değiştirilmelidir.", "Çözünme hızı ile bir sıvıda çözünebilecek en fazla madde miktarı aynı kavramdır.", "Kontrollü deneyde hangi değişkenlerin sabit kaldığı önemli değildir."], "Hipotez testi tek bağımsız değişken, ölçülebilir bağımlı değişken ve sabit tutulan koşullarla kurulmalıdır."),
    ("tr-g07-fen-note-fb-7-5-4-1", "Demir tozu, kum ve tuz içeren bir karışım ayrılacaktır.", "Mıknatıs demiri ayırıyor; su eklenince tuz çözünüyor, kum süzülüyor ve su uçurulunca tuz kalıyor.", "Karışım ayırma yöntemi bileşenlerin mıknatıslanma, çözünürlük, tanecik boyutu ve kaynama gibi fiziksel özellik farklarına dayanır.", "Önce mıknatısla demiri ayırıp sonra çözme-süzme ve güvenli buharlaştırma sırasını uygulamak gerekir.", "Her adımın farklı bir fiziksel özellikten yararlanması, tek yöntemin bütün bileşenleri ayıramayacağını gösterir.", ["Tuzu mıknatısla, demiri buharlaştırmayla ayırmak gerekir.", "Süzme işlemi suda çözünmüş tuzu filtre kâğıdında tamamen tutar.", "Ayırma sırasını bileşen özelliklerine göre planlamak gereksizdir."], "Ayırma basamakları karışım bileşenlerinin fiziksel özelliklerine göre sıralanır ve ısıtma işlemleri güvenlik kurallarıyla yapılır."),
    ("tr-g07-fen-note-fb-7-6-1-1", "Bir internet yazısı elektriklenmiş cismin her metal nesneyi kalıcı mıknatısa çevirdiğini iddia ediyor.", "Ders kitabı ve üniversite kaynağı, elektrik yükleri ile manyetik özelliklerin farklı kavramlar olduğunu ve iddianın deney kanıtı sunmadığını gösteriyor.", "Elektriklenme bilgisi yazarı, kurumu, tarihi, deney kanıtı ve başka güvenilir kaynaklarla tutarlılığı bakımından doğrulanmalıdır.", "İddiayı kaynaklar ve kontrollü gözlemle karşılaştırıp kanıtsız genellemeyi bilgi olarak paylaşmamak gerekir.", "Birden çok güvenilir kaynağın kavram ayrımında uyuşması, anonim iddianın güvenilir olmadığını gösterir.", ["İlk arama sonucu elektriklenme konusunda mutlaka doğrudur.", "Elektrik yükü ve mıknatıslık aynı kavramdır; kaynak kontrolü gerekmez.", "Deney kanıtı bulunmayan iddia daha kesin kabul edilmelidir."], "Bilgi toplama; kaynak güvenilirliği, kavramsal doğruluk ve yeniden sınanabilir kanıtın birlikte değerlendirilmesini gerektirir."),
    ("tr-g07-fen-note-fb-7-6-1-2", "Üç özdeş yalıtkan çubuk sürtünme, yüklü cisme dokundurma ve yaklaştırma yöntemleriyle inceleniyor.", "Sürtünmede iki cisim arasında yük aktarımı, dokunmada temasla paylaşım, etkide ise temas olmadan yüklerin yeniden dağılımı gözleniyor.", "Sürtünme, dokunma ve etki ile elektriklenme; temas durumu ve yüklerin davranışı ölçütleriyle ayırt edilir.", "Başlangıç yüklerini ve kullanılan malzemeyi kaydedip her yöntemi ayrı kontrollü düzende tekrarlamak gerekir.", "Etki düzeninde temas olmadan çekim oluşması, bu yöntemin dokunmayla elektriklenmeden ayrıldığını gösterir.", ["Etki ile elektriklenmede cisimlerin mutlaka birbirine dokunması gerekir.", "Sürtünmede yük aktarımı veya yeniden dağılımı gerçekleşmez.", "Üç elektriklenme yöntemi deneyde aynı temas koşuluna sahiptir."], "Elektriklenme yöntemleri gözlenebilir temas ve yük dağılımı kanıtlarıyla sınıflandırılır; tek gözlem bütün koşullara genellenmez."),
    ("tr-g07-fen-note-fb-7-6-1-3", "A, B ve C cisimlerinin yükleri elektroskop ve birbirleriyle etkileşimleri kullanılarak araştırılıyor.", "A ile B birbirini itiyor; A'nın pozitif olduğu biliniyor. C, nötr elektroskopa dokunduğunda yapraklar açılmıyor.", "Aynı işaretli yüklü cisimler iter; bir cismin pozitif, negatif veya nötr sınıflandırılması birden çok uygun kanıtla yapılır.", "Bilinen yükle itme-çekme ve elektroskop tepkisini ayrı ayrı sınayıp belirsiz durumda ek ölçüm yapmak gerekir.", "A'nın pozitif olup B'yi itmesi B'nin de pozitif olduğuna kanıt sağlar; tek bir çekim gözlemi ise yük işaretini her zaman belirlemez.", ["Pozitif A'nın ittiği B kesinlikle negatiftir.", "Yüklü cisimler işaretleri ne olursa olsun her zaman birbirini iter.", "Bir cismin başka cisme çekilmesi onun yük işaretini tek başına kesin belirler."], "Yük sınıflandırması itme gibi ayırt edici kanıtlara dayanır; çekim nötr cisimlerde kutuplanma nedeniyle de görülebilir."),
    ("tr-g07-fen-note-fb-7-7-1-1", "Bir gölde küçük balıklar planktonla, büyük balıklar küçük balıklarla besleniyor.", "Kirletici planktonda düşük, küçük balıkta daha yüksek, büyük balıkta en yüksek derişimde ölçülüyor.", "Besin zincirinde enerji üreticiden tüketicilere aktarılırken bazı kalıcı kirleticiler üst basamaklarda biyolojik birikim gösterebilir.", "Canlıların beslenme ilişkisini ve kirletici ölçümlerini aynı zincirde karşılaştırıp kirletici kaynağını azaltmak gerekir.", "Derişimin üst basamakta artması, kirleticinin yalnız ilk canlıda kalmadığını ve beslenme yoluyla taşındığını gösterir.", ["Besin zincirinde enerji üst tüketiciden üreticiye doğru akar.", "Kalıcı kirletici her basamakta mutlaka aynı derişimde kalır.", "Büyük balıktaki yüksek değer planktonla hiçbir ilişki kurulamayacağını gösterir."], "Enerji akışı ve madde birikimi aynı şey değildir; ölçümler beslenme ilişkileri ve kirleticinin kalıcılığıyla birlikte yorumlanır."),
    ("tr-g07-fen-note-fb-7-7-2-1", "Okulda musluklardan birinin dakikada yarım litre su sızdırdığı ölçülüyor.", "Conta değiştirildikten sonra sızıntı duruyor; sayaç kaydı haftalık tüketimde belirgin azalma gösteriyor.", "Kaynak tasarrufu sorunu ölçümle tanımlanır, uygulanabilir çözüm denenir ve sonuç aynı ölçütle yeniden değerlendirilir.", "Sızıntı miktarını kaydedip güvenli onarım istemek, ardından sayaç verisini önceki dönemle karşılaştırmak gerekir.", "Onarım sonrası aynı kullanım koşulunda tüketimin azalması, çözümün su kaybını azaltmada etkili olduğunu gösterir.", ["Tasarruf için ölçüm yapmadan bütün muslukları sürekli kapalı tutmak gerekir.", "Küçük sızıntılar zamanla kaynak tüketimini hiç etkilemez.", "Çözüm uygulandıktan sonra sonuç verisini kontrol etmek gereksizdir."], "Tasarruf çalışması problem, veri, çözüm ve etki değerlendirmesi zinciriyle yürütülür; güvenlik ve kullanıcı gereksinimleri korunur."),
]


FEN_POSITIONS = {5: 0, 15: 1, 28: 2, 42: 3, 55: 4, 64: 5, 72: 6, 88: 7, 97: 8}
MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
LEVELS = [1] * 20 + [2] * 25 + [3] * 30 + [4] * 20 + [5] * 5
FOCI = (
    "kaynak güvenilirliği", "ortak ilke ile uygulama ayrımı", "neden-sonuç ilişkisi",
    "bireysel sorumluluk", "tarihsel bağlam", "kanıtın sınırı",
)


def derive_dkab(base: tuple[Any, ...], occurrence: int) -> tuple[Any, ...]:
    note, scenario, evidence, concept, action, inference, wrongs, rationale = base
    focus = FOCI[occurrence % len(FOCI)]
    tag = f"{focus} odaklı kaynak incelemesi"
    return (
        note,
        f"Bir {tag} sırasında şu örneğin hangi ölçütlerle açıklanacağı tartışılıyor: {scenario}",
        f"İnceleme sonucunda şu gerekçe ve kayıt birlikte doğrulanıyor: {rationale} Ayrıca {evidence}",
        f"{inference} Bu sonuç, temel kavram ile kanıtı {focus} bakımından birbirine bağlar.",
        f"{action} Kararın dayanağı {focus} bakımından da açıkça belirtilmelidir.",
        f"{concept} İkinci kayıt, bu temel ayrımın {focus} bakımından korunması gerektiğini gösterir.",
        [
            f"{wrongs[0]} Üstelik bu iddia için kaynak denetimine ihtiyaç yoktur.",
            f"{wrongs[1]} Bu sonuç bütün durumlara koşulsuz uygulanabilir.",
            f"{wrongs[2]} Kanıtın kapsamı bu kararı hiçbir biçimde etkilemez.",
        ],
        f"{rationale} Karşılaştırmalı görevde kavram, kanıt ve {focus} ölçütü ayrı ayrı denetlenir.",
    )


def replace_grade(value: Any, subject_slug: str) -> Any:
    if isinstance(value, str):
        return (value.replace(f"tr-g06-bank-{subject_slug}-b02", f"tr-g07-bank-{subject_slug}-b02")
                .replace(f"tr.g06.bank.{subject_slug}.b02", f"tr.g07.bank.{subject_slug}.b02"))
    if isinstance(value, list):
        return [replace_grade(child, subject_slug) for child in value]
    if isinstance(value, dict):
        return {key: replace_grade(child, subject_slug) for key, child in value.items()}
    return value


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 100:
        raise RuntimeError(f"batch 02 expects batch 01 only, found {len(existing)}")
    dkab_notes, fen_notes = read_notes_only(DKAB_SOURCE), read_notes_only(FEN_SOURCE)
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    records, dkab_cursor = [], 0
    occurrences: Counter[str] = Counter()
    for local, (mode, level) in enumerate(zip(MODES, LEVELS), 1):
        if local in FEN_POSITIONS:
            case = FEN_CASES[FEN_POSITIONS[local]]
            note, subject, slug = fen_notes[case[0]], "Fen Bilimleri", "fen"
        else:
            base = DKAB_BASE[dkab_cursor % len(DKAB_BASE)]
            occurrence = occurrences[base[0]]
            occurrences[base[0]] += 1
            case = derive_dkab(base, occurrence)
            dkab_cursor += 1
            note = dict(dkab_notes[case[0]])
            note["title"] = f"{note['title']} — {FOCI[occurrence % len(FOCI)]}"
            subject, slug = "Din Kültürü ve Ahlak Bilgisi", "dkab"
        row = make_question(local, case, mode, level, note, labels, subject, batch_number=2, number_base=100)
        row = replace_grade(row, slug)
        row["grade"] = 7
        row["title"] = f"{note['title']} — 2. özgün üretim partisi"
        records.append(row)
    labels = {replace_grade(key, "dkab"): replace_grade(value, "dkab") for key, value in labels.items()}
    labels = {replace_grade(key, "fen"): replace_grade(value, "fen") for key, value in labels.items()}
    if Counter(row["subject"] for row in records) != Counter({"Din Kültürü ve Ahlak Bilgisi": 91, "Fen Bilimleri": 9}):
        raise AssertionError(Counter(row["subject"] for row in records))
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + records) + "\n", encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"grade": 7, "batch": 2, "questions": 100, "dkab": 91, "science": 9, "total": 200, "figures": sum(bool(row.get("figure")) for row in records), "sourceQuestionReads": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
