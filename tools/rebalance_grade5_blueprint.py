#!/usr/bin/env python3
"""Rebalance Grade 5 subject quotas with 21 newly authored Turkish questions.

Only note records are semantic authoring inputs.  Existing questions are used
solely to choose removable over-quota slots and preserve global distributions.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

from build_unique_question_banks import discover, objective_of, objective_quotas, subject_quotas


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "authoring/question-bank-blueprints/grade-5.jsonl"


def item(note: str, mode: str, stem: str, correct: str, wrongs: list[str], explanation: str) -> dict[str, Any]:
    return {"note": note, "mode": mode, "stem": stem, "correct": correct,
            "wrongs": wrongs, "explanation": explanation}


TASKS = [
    item("tr-g05-tur-to-5-21-n01", "comprehension", "'Neşeli' ve 'sevinçli' sözcükleri arasındaki ilişki hangisidir?", "Yakın anlamlıdır; benzer duyguları anlatırlar.", ["Zıt anlamlıdır; biri üzüntüyü anlatır.", "Eş seslidir; yazılışları aynıdır.", "Biri somut, biri özel addır."], "İki sözcük tam olarak aynı çağrışımı taşımayabilir; ancak bağlamda birbirine yakın bir sevinç durumunu belirtir."),
    item("tr-g05-tur-to-5-21-n01", "comprehension", "'Cesur' sözcüğünün anlamca karşıtı hangisidir?", "Korkak", ["Yürekli", "Kararlı", "Atılgan"], "Cesur, tehlike karşısında korkuya yenilmeyen kişiyi anlatır; korkak bunun karşıt anlamını taşır."),
    item("tr-g05-tur-to-5-21-n01", "application", "'İnce' sözcüğünün 'ince bir dal' ve 'ince bir davranış' kullanımları için hangi değerlendirme doğrudur?", "İlkinde kalınlık, ikincide özenli ve nazik davranış anlatılır.", ["İki kullanımda da yalnız dalın uzunluğu anlatılır.", "İlk kullanım mecaz, ikinci kullanım gerçek anlamdır.", "Sözcük iki cümlede de özel addır."], "Bağlam, aynı sözcüğün ilk cümlede ölçülebilen bir niteliği, ikinci cümlede ise mecaz bir tutumu anlattığını gösterir."),
    item("tr-g05-tur-to-5-21-n01", "application", "'Yaşlı çınar köyün geçmişine tanıklık etmişti.' cümlesinde 'tanıklık etmek' hangi anlamda kullanılmıştır?", "Uzun süre boyunca olayları görmüş olmak", ["Mahkemede ifade vermek", "Ağacın konuşarak bilgi vermesi", "Köyden uzaklaşmak"], "Cümlede ağaca insana özgü bir özellik aktarılmış; söz, yıllar içinde birçok olaya şahit olma anlamını kazanmıştır."),
    item("tr-g05-tur-to-5-21-n01", "error-analysis", "Bir öğrenci “Zıt anlamlı iki sözcük mutlaka aynı cümlede kullanılır.” diyor. Hangi düzeltme doğrudur?", "Zıtlık sözcüklerin anlam ilişkisidir; aynı cümlede bulunmaları zorunlu değildir.", ["Zıt sözcüklerin yazılışı aynı olmalıdır.", "Her sözcüğün yalnız bir zıt anlamlısı vardır.", "Zıtlık yalnız özel adlar arasında kurulur."], "Karşıt anlam, iki sözcüğün anlamları arasındaki ilişkiyi belirtir; kullanım yeri bu ilişkinin oluşması için koşul değildir."),
    item("tr-g05-tur-ty-5-1-n01", "comprehension", "Yazmaya başlamadan önce amaç ve hedef okur belirlemek hangi kararı kolaylaştırır?", "İçerik, tür ve anlatım biçimini seçmeyi", ["Her cümleyi aynı uzunlukta yazmayı", "Kaynakları metinden çıkarmayı", "Taslağı gözden geçirmeden yayımlamayı"], "Amaç ile okur, hangi bilginin ne kadar ayrıntılı ve hangi dil düzeyinde sunulacağını yönlendirir."),
    item("tr-g05-tur-ty-5-1-n01", "application", "Öğrenci okul kütüphanesinin kullanımını artırmak için öneri yazacaktır. İlk hazırlık adımı hangisidir?", "Kullanıcı gereksinimlerini gözleyip yazının amacını belirlemek", ["İlk akla gelen çözümü kanıtsız yazmak", "Yalnız kapak tasarımını tamamlamak", "Sonuç paragrafını kopyalamak"], "Öneri yazısı, gerçek gereksinime ve belirli bir amaca dayandığında uygulanabilir çözümler geliştirebilir."),
    item("tr-g05-tur-ty-5-1-n01", "application", "Taslakta iki paragraf aynı düşünceyi tekrarlıyor. Yazar ne yapmalıdır?", "Tekrarları birleştirip her paragrafa ayrı bir işlev vermelidir.", ["Aynı düşünceyi üçüncü kez yazmalıdır.", "Bütün örnekleri çıkarmalıdır.", "Yalnız yazı tipini değiştirmelidir."], "Gözden geçirmede paragraf işlevlerini ayırmak, düşüncenin gereksiz tekrar yerine adım adım ilerlemesini sağlar."),
    item("tr-g05-tur-ty-5-1-n01", "error-analysis", "Bir öğrenci “İlk taslağım bittiğinde yazım değiştirilemez.” diyor. Hangi düzeltme doğrudur?", "Taslak; içerik, yapı ve dil bakımından gözden geçirilip yeniden yazılabilir.", ["Düzeltme yalnız başlığı silmektir.", "Taslak doğrudan yayımlanmalıdır.", "Geri bildirim metni geliştirmez."], "İlk taslak düşüncelerin ilk düzenidir; yeniden okuma ve geri bildirim, anlatımın amaçla daha iyi uyuşmasını sağlar."),
    item("tr-g05-tur-tk-5-3-n01", "comprehension", "Konuşma içeriğinin amaca uygun olması ne demektir?", "Seçilen bilgi ve örneklerin konuşmanın hedefini desteklemesi", ["Konuyla ilgisiz her ayrıntının eklenmesi", "Konuşmanın mümkün olduğunca uzatılması", "Dinleyicinin ön bilgisinin yok sayılması"], "Amaca uygun içerik, dinleyiciyi gereksiz ayrıntıyla yormadan ana mesajın anlaşılmasını sağlar."),
    item("tr-g05-tur-tk-5-3-n01", "application", "Sınıfı su tasarrufuna ikna edecek konuşmada hangi içerik daha uygundur?", "Sınıftaki tüketim gözlemi, tasarruf adımları ve beklenen yarar", ["Konuyla ilgisiz bir tatil anısı", "Yalnız konuşmacının sevdiği renkler", "Kaynağı belirsiz abartılı iddialar"], "İkna amacı, sorunu gösteren kanıtın uygulanabilir çözüm ve sonuçla ilişkilendirilmesini gerektirir."),
    item("tr-g05-tur-tk-5-3-n01", "error-analysis", "Bir öğrenci “Dinleyici kim olursa olsun aynı terimleri açıklamadan kullanırım.” diyor. Hangi düzeltme doğrudur?", "Terim ve açıklama düzeyi dinleyicinin ön bilgisine göre uyarlanmalıdır.", ["Terimler her konuşmadan çıkarılmalıdır.", "Yalnız uzun sözcükler seçilmelidir.", "Dinleyici konuşma amacını etkilemez."], "Doğru terim korunabilir; ancak dinleyicinin kavramı anlayabilmesi için gerektiğinde kısa tanım ve örnek verilmelidir."),
    item("tr-g05-tur-tk-5-5-n01", "comprehension", "Bir tartışmada uzlaşma aramak neyi gerektirir?", "Tarafların ortak noktalarını ve kabul edilebilir çözümü belirlemeyi", ["Karşı görüşü dinlemeden reddetmeyi", "En yüksek sesle konuşanı haklı saymayı", "Sorunu değiştirmeden konuşmayı bitirmeyi"], "Uzlaşma, farklı ihtiyaçları dinleyerek ortak ölçütlere dayanan uygulanabilir bir çözüm üretme sürecidir."),
    item("tr-g05-tur-tk-5-5-n01", "application", "İki grup sınıf etkinliğinin günü konusunda anlaşamıyor. İlk yapıcı adım hangisidir?", "Her grubun gerekçesini sorup herkes için uygun zaman ölçütlerini belirlemek", ["Bir grubu konuşmadan dışlamak", "Tarihi rastgele seçmek", "Aynı görüşü sürekli tekrarlamak"], "Soru sormak ve etkin dinlemek, anlaşmazlığın altında bulunan ihtiyaçları görünür kılar ve ortak çözüm alanı açar."),
    item("tr-g05-tur-tk-5-5-n01", "error-analysis", "Bir öğrenci “Uzlaşmak, kendi düşüncemi açıklamadan karşı tarafı kabul etmektir.” diyor. Hangi düzeltme doğrudur?", "Uzlaşmada taraflar görüşlerini gerekçeleriyle açıklar ve ortak çözüm arar.", ["Uzlaşmada yalnız bir taraf konuşur.", "Gerekçe sunmak anlaşmayı bozar.", "Her anlaşmazlık oylamayla biter."], "Uzlaşma teslim olmak değil, karşılıklı dinleme ve gerekçeli değerlendirmeyle ortak bir karar geliştirmektir."),
    item("tr-g05-tur-ty-5-3-n01", "comprehension", "Bir paragraftaki destekleyici cümlelerin görevi nedir?", "Ana düşünceyi açıklamak, örneklemek veya gerekçelendirmek", ["Her biri yeni ve ilgisiz konu açmak", "Başlığı metinden bağımsızlaştırmak", "Sonucu anlaşılmaz kılmak"], "Destekleyici cümleler aynı merkez düşünceye bağlanarak paragrafın bütünlüğünü ve açıklığını güçlendirir."),
    item("tr-g05-tur-ty-5-3-n01", "application", "Bir bilgilendirici metnin sonucu yeni ve açıklanmamış bir iddia başlatıyor. Nasıl düzeltilmelidir?", "Yeni iddia gelişmede açıklanmalı ya da sonuçtan çıkarılmalıdır.", ["Sonuca daha çok yeni konu eklenmelidir.", "Giriş bütünüyle silinmelidir.", "Bütün kanıtlar sonuçta ilk kez verilmelidir."], "Sonuç bölümü daha önce geliştirilen düşünceleri bağlar; okurun hazırlıksız olduğu yeni bir savı başlatmaz."),
    item("tr-g05-tur-ty-5-21-n01", "comprehension", "Doğrudan soru bildiren cümlenin sonunda hangi işaret kullanılır?", "Soru işareti", ["İki nokta", "Noktalı virgül", "Kesme işareti"], "Soru işareti, yanıt bekleyen doğrudan soru cümlesinin tamamlandığını yazıda açıkça gösterir."),
    item("tr-g05-tur-ty-5-21-n01", "application", "Hangi cümlede özel ada gelen çekim eki doğru yazılmıştır?", "Bursa'ya baharda gideceğiz.", ["Ankaraya bu akşam varacağız.", "izmir'e hafta sonu gideceğiz.", "Edirne-ye trenle ulaşacağız."], "Şehir adı büyük harfle başlar; özel ada getirilen çekim eki kesme işaretiyle ayrılır."),
    item("tr-g05-tur-to-5-6-n01", "comprehension", "Bir metinde açıkça verilen bilgi nasıl belirlenir?", "Metindeki doğrudan ifadeler bulunup soruyla eşleştirilerek", ["Metinde olmayan ayrıntılar eklenerek", "Yalnız başlığa bakılarak", "Kişisel tahmin kanıt sayılarak"], "Açık bilgi için çıkarım yapmadan, metinde doğrudan belirtilen kişi, olay, yer veya neden ifadelerine dayanılır."),
    item("tr-g05-tur-to-5-6-n01", "error-analysis", "Bir öğrenci “Metinde açık bilgi sorulunca kendi deneyimimi cevap olarak yazabilirim.” diyor. Hangi düzeltme doğrudur?", "Yanıt kişisel deneyime değil metinde doğrudan verilen kanıta dayanmalıdır.", ["Her açık bilgi yoruma açıktır.", "Metni okumadan başlık yeterlidir.", "Yazarın söylemediği ayrıntılar eklenmelidir."], "Açıkça verilen bilgiyi bulma görevi, okurun tahminini değil metinde bulunan ve gösterilebilen ifadeyi ölçer."),
]


DROP_PLAN = {
    "Fen Bilimleri": Counter({"comprehension": 2, "application": 2, "error-analysis": 2}),
    "İngilizce": Counter({"comprehension": 2, "application": 2, "error-analysis": 1}),
    "Matematik": Counter({"comprehension": 2, "application": 2, "error-analysis": 1}),
    "Sosyal Bilgiler": Counter({"comprehension": 2, "application": 2, "error-analysis": 1}),
}


def rotate(correct: str, wrongs: list[str], position: int) -> list[str]:
    values = list(wrongs)
    values.insert(position, correct)
    return values


def main() -> int:
    rows = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    if len(rows) != 2000:
        raise RuntimeError(f"expected 2000 blueprints, found {len(rows)}")
    subjects = discover(5)
    by_subject = {subject.subject: subject for subject in subjects}
    quotas = subject_quotas(subjects)
    existing_rebalance = [row for row in rows if str(row.get("id", "")).startswith("tr-g05-bank-turkce-rb01-q")]
    selected: list[dict[str, Any]] = []
    if len(existing_rebalance) == len(TASKS):
        selected = sorted(existing_rebalance, key=lambda row: int(str(row["id"]).rsplit("q", 1)[1]))
    else:
        for subject_name, modes in DROP_PLAN.items():
            subject = by_subject[subject_name]
            objective_targets = objective_quotas(subject, quotas[subject_name])
            current = Counter(objective_of(row) for row in rows if row.get("subject") == subject_name)
            candidates = [row for row in rows if row.get("subject") == subject_name and row.get("figure") is None]
            for mode, needed in modes.items():
                eligible = [row for row in candidates if row.get("questionType") == mode and current[objective_of(row)] > objective_targets.get(objective_of(row), 2)]
                eligible.sort(key=lambda row: (-(current[objective_of(row)] - objective_targets.get(objective_of(row), 2)), int(row.get("questionNumber", 0))))
                if len(eligible) < needed:
                    raise RuntimeError(f"{subject_name}/{mode}: removable slot shortage")
                for row in eligible[:needed]:
                    selected.append(row)
                    candidates.remove(row)
                    current[objective_of(row)] -= 1
    if len(selected) != len(TASKS):
        raise AssertionError((len(selected), len(TASKS)))
    selected_by_mode: dict[str, list[dict[str, Any]]] = {}
    for row in selected:
        selected_by_mode.setdefault(str(row["questionType"]), []).append(row)
    notes = {str(note["id"]): note for note in by_subject["Türkçe"].notes}
    replacements: dict[str, dict[str, Any]] = {}
    mode_offsets = Counter()
    for local, task in enumerate(TASKS, 1):
        mode = task["mode"]
        slot = selected_by_mode[mode][mode_offsets[mode]]
        mode_offsets[mode] += 1
        note = notes[task["note"]]
        position = int(slot["correct"])
        choices = rotate(task["correct"], task["wrongs"], position)
        reason_map = {
            task["correct"]: f"Doğru gerekçe: {task['explanation']}",
            task["wrongs"][0]: f"Kavram yanılgısı: {task['wrongs'][0]} ifadesi ölçülen kavramın anlamını yanlış kurar.",
            task["wrongs"][1]: f"Koşul yanılgısı: {task['wrongs'][1]} ifadesi sorudaki bağlam ve koşulu birlikte karşılamaz.",
            task["wrongs"][2]: f"Kanıt dışı çıkarım: {task['wrongs'][2]} ifadesi verilen bilgi veya dil ölçütüyle desteklenmez.",
        }
        objective = str((note.get("objectives") or [note.get("objective")])[0])
        qid = f"tr-g05-bank-turkce-rb01-q{local:03d}"
        explanation = task["explanation"] + " Diğer seçenekler, soruda ölçülen anlam, yapı veya kanıt ilişkisini birlikte korumaz."
        replacements[str(slot["id"])] = {
            "type": "question", "id": qid, "questionId": qid,
            "questionNumber": slot["questionNumber"], "subject": "Türkçe", "grade": 5,
            "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
            "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
            "title": f"{note['title']} — kota dengeleme özgün üretimi",
            "objective": objective, "objectiveId": objective,
            "noteId": note["id"], "noteKey": note["id"],
            "question": task["stem"], "choices": choices,
            "correct": position, "correctIndex": position, "correctOption": choices[position],
            "distractorWhy": [reason_map[value] for value in choices],
            "explanation": explanation, "level": slot["level"],
            "difficultyReason": f"Düzey {slot['level']}; {note['title']} bilgisini {mode} görevinde kullanıp üç adlandırılmış yanılgıyı ayırmayı gerektirir.",
            "questionType": mode, "familyId": f"tr-g05-bank-turkce-rb01-family-{local:03d}",
            "authoringTemplateId": f"g5-turkce-rb01-{objective.lower().replace('.', '-')}-{mode}-v{local:03d}",
            "objectiveSource": note.get("objectiveSource"), "objectiveEvidenceId": note.get("objectiveEvidenceId"),
            "sourceRefs": note.get("sourceRefs") or [],
            "visualRequirement": "none",
            "visualNeed": {"level": "none", "role": "none", "rationale": "Çözüm için gerekli metin ve dil kanıtı soru kökünde eksiksiz verilmiştir.", "acceptableKinds": [], "evidenceDimensions": []},
            "figure": None, "hintsCount": 0, "hintsForbidden": True,
        }
    output = [replacements.get(str(row["id"]), row) for row in rows]
    counts = Counter(str(row["subject"]) for row in output)
    if counts != Counter(quotas):
        raise AssertionError((counts, quotas))
    if Counter(row["correct"] for row in output) != Counter({0: 500, 1: 500, 2: 500, 3: 500}):
        raise AssertionError("answer balance changed")
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in output) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"replaced": len(replacements), "subjects": dict(counts), "modes": dict(Counter(task["mode"] for task in TASKS)), "sourceQuestionReads": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
