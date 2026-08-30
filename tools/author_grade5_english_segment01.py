#!/usr/bin/env python3
"""Author the first 30 Grade 5 English bank questions (grade rows 471–500)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from build_unique_question_banks import ROOT


SOURCE = ROOT / "turkiye/5-sinif/ingilizce/ingilizce-tum.jsonl"
OUTPUT = ROOT / "authoring/question-bank-blueprints/grade-5.jsonl"
LABELS_OUTPUT = ROOT / "authoring/question-bank-blueprints/grade-5-labels.json"


# note id, language input, task, correct option, distractors, explanation
ITEMS = [
    ("tr.g05.ingilizce.n001", "The art club meets in Room 8 after lunch on Tuesday.", "Dinleme notundaki yer ve zamanı birlikte koruyan bilgi hangisidir?", "It meets in Room 8 after lunch on Tuesday.", ["It meets in the gym before breakfast on Tuesday.", "The meeting starts before lunch in a different classroom.", "The students paint at home every evening."], "Room 8, after lunch ve Tuesday ayrıntılarının üçü de korunmalıdır."),
    ("tr.g05.ingilizce.n002", "Attention, students! The library is closed today, so return your books tomorrow.", "Bu okul iletisinin amacı ve yapılacak iş hangi seçenekte doğru sınıflandırılmıştır?", "Announcement — return the books tomorrow.", ["Invitation — buy new books today.", "Warning — never use the library again.", "Personal introduction — talk about a favourite book."], "İleti bugünkü kapanışı duyurur ve kitapların yarın iade edilmesini ister."),
    ("tr.g05.ingilizce.n003", "Our music lesson starts at ten, but the teacher asks us to arrive five minutes early.", "İletiyi kendi sözleriyle doğru aktaran öğrenci hangisini söylemelidir?", "We should be there at five to ten for the music lesson.", ["The music lesson finishes at five past ten.", "We can arrive at ten past ten.", "The teacher cancels the music lesson."], "Ten o'clock'tan beş dakika önce ifadesi five to ten biçiminde aktarılır."),
    ("tr.g05.ingilizce.n004", "Monday: Maths at 9, PE at 11. Tuesday: Science at 9, English at 11.", "Ders programındaki iki bilgiyi doğru birleştiren cümle hangisidir?", "Science is at nine on Tuesday, and PE is at eleven on Monday.", ["Science and PE are both at eleven on Tuesday.", "English is at nine on Monday.", "Maths is at eleven on Tuesday."], "Gün ve saat eşleşmeleri programdaki satırlardan değiştirilmeden alınmalıdır."),
    ("tr.g05.ingilizce.n005", "Class A has twenty students and two computers. Class B has eighteen students and four computers.", "Sınıfları karşılaştıran doğru çıkarım hangisidir?", "Class B has fewer students but more computers than Class A.", ["Class B has more students and fewer computers.", "Both classes have the same number of students.", "Class A has four computers and eighteen students."], "18 sayısı 20'den küçük, 4 sayısı 2'den büyüktür; iki karşılaştırma birlikte korunur."),
    ("tr.g05.ingilizce.n006", "A: May I borrow your ruler? B: Of course. Here you are.", "Diyaloğu doğal biçimde tamamlayan karşılık hangisidir?", "A: Thank you. B: You're welcome.", ["A: I am a ruler. B: It is Monday.", "A: Close the window. B: I don't like maths.", "A: How old is the ruler? B: At school."], "Bir eşya isteme ve kabul etme konuşması teşekkür ve uygun karşılıkla tamamlanır."),
    ("tr.g05.ingilizce.n007", "Mina has curly brown hair, wears glasses and enjoys solving puzzles.", "Kişisel betimlemedeki görünüş ve ilgi bilgisini birlikte veren seçenek hangisidir?", "She has curly brown hair and likes puzzles.", ["She has straight black hair and dislikes puzzles.", "She wears a hat and plays the drums every day.", "She has glasses, so she cannot solve puzzles."], "Curly brown hair ile enjoys solving puzzles bilgileri doğrudan metinde bulunur."),
    ("tr.g05.ingilizce.n008", "Eren gets up at seven, feeds the cat, and walks to school. At weekends, he gets up at nine.", "Bilgileri weekday ve weekend olarak doğru ayıran seçenek hangisidir?", "Weekdays: gets up at seven; weekends: gets up at nine.", ["Weekdays: gets up at nine; weekends: walks to school at seven.", "Every day: gets up at nine and never feeds the cat.", "Weekends: goes to school before feeding the cat."], "Metin hafta içi yedi, hafta sonu dokuz saatini açıkça ayırır."),
    ("tr.g05.ingilizce.n009", "Bir öğrenci kendisini ve rutinini kısa, anlaşılır cümlelerle tanıtacak.", "Bu amaca uygun ve dilbilgisel olarak tutarlı tanıtım hangisidir?", "I'm Deniz. I live in Ankara, and I usually read after dinner.", ["I'm Deniz. She live in Ankara and read yesterday every day.", "Deniz are Ankara. Usually dinner reading.", "I live after dinner because Ankara is a book."], "Kişi, yer ve rutin bilgisi I öznesiyle anlaşılır simple present cümlelerinde aktarılır."),
    ("tr.g05.ingilizce.n010", "My father makes breakfast, my sister sets the table, and we eat together at eight.", "Aile yaşamındaki görev ve zamanı doğru aktaran seçenek hangisidir?", "The sister sets the table, and the family eats at eight.", ["The father sets the table after eight at night.", "The family never has breakfast together.", "The sister makes breakfast while everyone sleeps."], "Sister–sets the table ve family–eight eşleşmeleri metinde açıkça verilir."),
    ("tr.g05.ingilizce.n011", "Mum usually works at the hospital, but she is working at home today.", "Rutin ile şu anki durumu doğru ayıran cümle hangisidir?", "She usually works at the hospital; today she is working at home.", ["She is usually working at home every day.", "She never works at the hospital.", "Today she works at the hospital because she is at home."], "Usually simple present rutini, today ile present continuous mevcut etkinliği gösterir."),
    ("tr.g05.ingilizce.n012", "We are preparing a surprise for Grandma. I feel excited, and my brother is making a card.", "Bilgi ve duyguyu birlikte aktaran doğru seçenek hangisidir?", "The speaker feels excited, and the brother is making a card.", ["The speaker feels bored, and the brother is buying a car.", "Grandma is making a card for the brother.", "They prepare the same surprise every morning."], "Excited duygusu ve is making a card etkinliği iki ayrı ayrıntı olarak korunur."),
    ("tr.g05.ingilizce.n013", "From the front door, go straight. The kitchen is on the left, opposite the living room.", "Ev içindeki konumu doğru gösteren yönerge hangisidir?", "The kitchen is on the left and the living room is opposite it.", ["The kitchen is behind the front door and next to no room.", "The living room is inside the kitchen.", "Turn right because both rooms are upstairs."], "On the left ve opposite ilişkileri ev haritasındaki iki konumu belirler."),
    ("tr.g05.ingilizce.n014", "Lara's neighbourhood is quiet and has a park. Tom's neighbourhood is busy and has a sports centre.", "İki mahalleyi değiştirmeden karşılaştıran seçenek hangisidir?", "Lara's area is quieter, while Tom's has a sports centre.", ["Tom's area is quiet and has the only park.", "Both neighbourhoods are busy and have no facilities.", "Lara lives in a sports centre, and Tom lives in a park."], "Quiet–park Lara'ya, busy–sports centre Tom'a aittir."),
    ("tr.g05.ingilizce.n015", "Bir öğrenci evini ve çevresini yön bildiren ifadelerle tanıtacak.", "Amaca uygun, anlaşılır tanıtım hangisidir?", "My flat is next to the bakery, and there is a bus stop across from it.", ["My flat next bakery bus across it there.", "The bakery is a bus because my flat stops.", "I next to live and across is bakery yesterday."], "There is ve next to/across from yapıları konumları açık ve doğru aktarır."),
    ("tr.g05.ingilizce.n016", "For the salad, we need two tomatoes, one cucumber and some cheese. We don't need onions.", "Ana bilgi ile ayrıntıları doğru koruyan alışveriş notu hangisidir?", "Buy two tomatoes, a cucumber and cheese; don't buy onions.", ["Buy two onions and no tomatoes.", "Buy only cheese because the salad has no vegetables.", "Buy a cucumber and onions, but leave the tomatoes."], "Miktarlar ve don't need onions olumsuz ayrıntısı birlikte korunur."),
    ("tr.g05.ingilizce.n017", "First wash the apples. Then cut them. Finally, put the pieces in a bowl.", "Tarif sırasını bozmayan yönerge hangisidir?", "Wash the apples, cut them, and then put the pieces in a bowl.", ["Put whole apples in the bowl before washing them.", "Cut the bowl and finally wash the pieces.", "First eat the apples, then buy a bowl."], "First–then–finally sırası yıkama, kesme ve kaba koyma işlemlerini belirler."),
    ("tr.g05.ingilizce.n018", "A: Would you like soup? B: No, thanks. I'd like some pasta, please.", "Müşterinin tercihini doğru aktaran cümle hangisidir?", "The customer doesn't want soup and asks for pasta.", ["The customer orders soup and refuses pasta.", "The waiter doesn't have any food.", "The customer asks how to cook soup at home."], "No, thanks soup'u reddeder; I'd like pasta tercihi nazikçe bildirir."),
    ("tr.g05.ingilizce.n019", "Penguins live in cold regions, have feathers and cannot fly, but they swim very well.", "Verilen hayvan bilgilerini doğru özetleyen sonuç hangisidir?", "Penguins are birds adapted to cold places and swimming.", ["Penguins are flying mammals from deserts.", "Penguins cannot swim because they have feathers.", "All birds live in cold regions and cannot fly."], "Cold regions, feathers, cannot fly ve swim well ayrıntıları penguenin yaşamına birlikte bağlanır."),
    ("tr.g05.ingilizce.n020", "A dolphin lives in water and breathes air. A shark lives in water and breathes through gills.", "İki hayvanın benzerlik ve farkını doğru yorumlayan seçenek hangisidir?", "Both live in water, but only the dolphin breathes air with lungs.", ["Both breathe through gills because both are fish.", "The shark lives on land, and the dolphin lives in water.", "Only the shark needs oxygen."], "İkisi de suda yaşar; dolphin memelidir ve akciğerle, shark solungaçla solunum yapar."),
    ("tr.g05.ingilizce.n021", "The rabbit needs fresh water, hay and a clean living area every day.", "Evcil hayvan bakımı hakkında uygun öneri hangisidir?", "Give it fresh water and hay, and keep its area clean.", ["Give it only sweets and never clean its area.", "Keep it without water during the day.", "Let it eat any unsafe plant it finds."], "Needs yapısı günlük bakım gereksinimlerini belirtir; öneri bu üç gereksinimi korur."),
    ("tr.g05.ingilizce.n022", "Next Saturday, our class is going to visit the planetarium to learn about Mars.", "Gelecek planının zaman, yer ve amacını doğru veren seçenek hangisidir?", "They are going to visit the planetarium next Saturday to learn about Mars.", ["They visited Mars at school last Saturday.", "They are going to play football at the planetarium every day.", "Mars is going to visit their class tonight."], "Be going to planı, next Saturday zamanı ve learn about Mars amacı birlikte aktarılır."),
    ("tr.g05.ingilizce.n023", "Plan A: We are going to watch the Moon on Friday. Plan B: We are going to build a model of Saturn on Saturday.", "İki gelecek planını doğru karşılaştıran seçenek hangisidir?", "The Moon observation is before the Saturn model activity.", ["Both activities are on Saturday.", "The Saturn model is before the Friday observation.", "Plan A is about Saturn, and Plan B is about the Moon."], "Friday Saturday'dan önce gelir; etkinlik konuları da Moon ve Saturn olarak ayrıdır."),
    ("tr.g05.ingilizce.n024", "I think people will travel farther in space, but they won't live on every planet.", "Geleceğe ilişkin tahmini anlamını değiştirmeden aktaran seçenek hangisidir?", "The speaker predicts more distant space travel but not life on all planets.", ["The speaker says people already live on every planet.", "The speaker refuses all future space travel.", "The speaker is describing yesterday's journey."], "Will/won't yapıları olumlu uzak yolculuk tahmini ile tüm gezegenlerde yaşama olumsuzluğunu ayırır."),
    ("tr.g05.ingilizce.n001", "Nora says, 'Our chess club is in the library at half past three.'", "İletideki etkinlik, yer ve saati doğru birleştiren seçenek hangisidir?", "Chess club — library — 3:30.", ["Art club — gym — 3:30.", "The library meeting starts one hour earlier.", "Library club — chess room — 4:30."], "Chess club, library ve half past three bilgileri aynı kayda aittir."),
    ("tr.g05.ingilizce.n002", "Student: 'The notice says the school trip is on Thursday.' Another student writes: 'The trip is on Tuesday.'", "İkinci öğrencinin bilgi değiştirme hatasını düzelten seçenek hangisidir?", "The school trip is on Thursday.", ["The notice moves the trip to an earlier weekday.", "The notice is a recipe for Thursday.", "There is no school trip in the notice."], "İletide Thursday açıkça verildiği için Tuesday yazmak zaman bilgisini değiştirir."),
    ("tr.g05.ingilizce.n003", "Message: 'Bring your science notebook tomorrow.' Student's report: 'We should bring our art books today.'", "Aktarma hatalarını bütünüyle düzelten cümle hangisidir?", "We should bring our science notebooks tomorrow.", ["We should bring our art books today.", "We brought science notebooks yesterday.", "Tomorrow's science lesson is cancelled."], "Science notebook ve tomorrow ayrıntılarının ikisi de aktarımda korunmalıdır."),
    ("tr.g05.ingilizce.n004", "Schedule: English at 10 on Wednesday. A student says, 'English is at 11 on Monday.'", "Program okuma yanılgısını düzelten seçenek hangisidir?", "English is at ten on Wednesday.", ["English is at eleven on Monday.", "A maths lesson follows English later in the day.", "Wednesday begins at eleven."], "Ders adı, saat ve gün program satırındaki gibi birlikte okunur."),
    ("tr.g05.ingilizce.n005", "Class X has 16 books; Class Y has 21 books. A student says, 'Class X has more books.'", "Karşılaştırma yanılgısını düzelten ifade hangisidir?", "Class Y has more books than Class X.", ["Class X has more books than Class Y.", "Both classes have sixteen books.", "Class Y has fewer than ten books."], "21 sayısı 16'dan büyük olduğu için more books karşılaştırması Class Y için kullanılır."),
    ("tr.g05.ingilizce.n006", "A: Can you help me carry these books? B: Yes, sure. A student answers next: 'I'm from Canada.'", "Konuşma işlevi yanılgısını düzelten doğal karşılık hangisidir?", "A: Thanks for your help.", ["A: I'm from Canada.", "A: The books are at seven o'clock.", "A: My favourite lesson can carry them."], "Yardım teklifinin kabulünden sonra teşekkür etmek konuşma akışına uygundur."),
]


MODES = ["comprehension"] * 7 + ["application"] * 11 + ["analysis"] * 7 + ["error-analysis"] * 5
LEVELS = [1] * 4 + [2] * 3 + [1] * 2 + [2] * 4 + [3] * 5 + [3] * 3 + [4] * 2 + [5] * 2 + [3] + [4] * 4


def notes() -> dict[str, dict[str, Any]]:
    rows = [json.loads(line) for line in SOURCE.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    return {str(row.get("id")): row for row in rows if row.get("type") == "note"}


def table(qid: str, language_input: str, labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.alt"
    labels[h1], labels[h2] = "Dinleme/okuma kaydı", "İleti"
    labels[alt] = "İngilizce iletiyi tek satırda gösteren tablo; doğru seçenek işaretlenmemiştir."
    return {"kind": "table", "headerKeys": [h1, h2], "rows": [[{"v": "Source"}, {"v": language_input}]], "altTextKey": alt}


def make(local: int, entry: tuple[Any, ...], note_map: dict[str, dict[str, Any]], labels: dict[str, str]) -> dict[str, Any]:
    note_id, language_input, task, correct_text, wrongs, explanation = entry
    note = note_map[note_id]
    objective = str((note.get("objectives") or [""])[0])
    global_number = 470 + local
    correct = (global_number - 1) % 4
    choices = [*wrongs[:correct], correct_text, *wrongs[correct:]]
    reason_map = {
        correct_text: f"Doğru iletişim çözümü: {explanation}",
        wrongs[0]: f"Bilgi değiştirme yanılgısı: Bu seçenek iletideki kişi, yer, zaman veya eylem ayrıntısını değiştirir. {explanation}",
        wrongs[1]: f"Dil işlevi yanılgısı: Bu seçenek sorunun istediği iletişim amacıyla uyuşmayan bir yapı kullanır. {explanation}",
        wrongs[2]: f"Dayanaksız çıkarım yanılgısı: Bu seçenekteki sonuç verilen iletiden çıkarılamaz. {explanation}",
    }
    mode, level = MODES[local - 1], LEVELS[local - 1]
    qid = f"tr-g05-bank-eng-s01-q{local:03d}"
    fig = table(qid, language_input, labels) if mode == "analysis" else None
    if mode == "analysis":
        stem = f"Aşağıdaki tabloda bir İngilizce ileti verilmiştir. {task}"
    else:
        stem = f"İleti: “{language_input}” {task}"
    visual_need = ({
        "level": "required", "role": "evidence", "rationale": "Çözümlenecek İngilizce ileti yalnız tabloda verilir.",
        "acceptableKinds": ["table"], "evidenceDimensions": ["ileti", "ayrıntı"],
    } if fig else {
        "level": "none", "role": "none", "rationale": "Çözümlenecek ileti soru metninde verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "İngilizce", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"), "subtopicKey": note.get("subtopicKey"),
        "topic": note.get("topic"), "title": f"{note['title']} — {mode}",
        "objective": objective, "objectiveId": objective, "noteId": note_id, "noteKey": note_id,
        "question": stem, "choices": choices, "correct": correct, "correctIndex": correct,
        "correctOption": choices[correct], "distractorWhy": [reason_map[choice] for choice in choices],
        "explanation": f"{explanation} Bu nedenle doğru yanıt “{correct_text}” seçeneğidir.",
        "level": level,
        "difficultyReason": f"Düzey {level}; İngilizce iletideki birden fazla ayrıntıyı {mode} biçiminde korumayı ve işlevsiz seçenekleri ayırmayı gerektirir.",
        "questionType": mode, "familyId": f"tr-g05-bank-eng-family-{local:03d}",
        "objectiveSource": note.get("objectiveSource"), "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [], "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 470:
        raise RuntimeError("the 470-question science quota must be regenerated first")
    label_map = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = notes()
    rows = [make(local, entry, note_map, label_map) for local, entry in enumerate(ITEMS, 1)]
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
                      encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(label_map, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
    print(json.dumps({"englishQuestions": len(rows), "gradeTotal": len(existing) + len(rows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
