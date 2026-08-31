#!/usr/bin/env python3
"""Append 13 science and 87 English questions for Grade 6 batch 10.

The authoring source is lesson notes only. Lesson-package questions are never
read, transformed, or used as prompt roots.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

from author_grade6_bilisim_batch01 import LABELS_OUTPUT, OUTPUT, rotate
from author_grade6_fen_batch07 import task
from author_grade6_mixed_batch03 import LEVEL_SEQUENCE, read_notes_only
from author_grade6_mixed_batch06 import FEN_SOURCE


ENGLISH_SOURCE = Path("turkiye/6-sinif/ingilizce/ingilizce-tum.jsonl")


def science_tasks():
    fuel = "tr-g06-fen-bilimleri-note-035"
    environment = "tr-g06-fen-bilimleri-note-036"
    return [
        task(fuel, "comprehension", "Isınma amaçlı bir yakıt değerlendirilirken hangi iki etki birlikte ele alınmalıdır?",
             "İnsan sağlığı ve çevre üzerindeki etkiler", ["Yalnız ambalajın rengi", "Sadece yakıtın adı", "Yalnız satış yerinin uzaklığı"],
             "Dengeli değerlendirme ısınma yararının yanında sağlık ve çevre sonuçlarını da kapsar."),
        task(fuel, "analysis", "K sobası odayı aynı sürede ısıtırken L'ye göre daha fazla duman ve parçacık çıkarıyor. Hangi yorum veriye uygundur?",
             "Isıtma yararı benzer olsa da K'nın hava kalitesi etkisi daha olumsuz olabilir.",
             ["K her ölçüte göre kesinlikle daha iyidir.", "Duman verisi sağlık ve çevre değerlendirmesinde kullanılamaz.", "İki yakıtın bütün özellikleri zorunlu aynıdır."],
             "Karar yalnız ısı miktarına değil, ölçülen salım farkına da dayanmalıdır."),
        task(fuel, "error-analysis", "Bir öğrenci “Yakıt evi ısıtıyorsa insan sağlığına etkisini araştırmaya gerek yoktur.” diyor. Hangi düzeltme doğrudur?",
             "Isınma yararı ile solunan havaya ve çevreye olası etkiler birlikte araştırılmalıdır.",
             ["Isı üreten bütün yakıtlar sıfır salım yapar.", "Sağlık yalnız dış ortam sıcaklığına bağlıdır.", "Kanıt yerine kişisel beğeni yeterlidir."],
             "Bilimsel tartışma yarar ve risk kanıtlarını aynı değerlendirmede karşılaştırır."),
        task(environment, "comprehension", "Çevre sorununa çözüm üretme sürecinin ilk basamağı hangisidir?",
             "Problemi nerede ve nasıl görüldüğüyle açık biçimde tanımlamak",
             ["Kanıt toplamadan ilk fikri uygulamak", "Sonucu ölçmeden başarı ilan etmek", "Bütün seçenekleri tek cümlede reddetmek"],
             "Açık problem tanımı kanıt, neden ve çözüm seçeneklerinin doğru kapsamda kurulmasını sağlar."),
        task(environment, "application", "Okul bahçesinde belirli noktada sürekli çöp birikiyor. İlk araştırma için en uygun işlem hangisidir?",
             "Birikmenin yeri, zamanı, çöp türü ve mevcut kutuların kullanımını kaydetmek",
             ["Bahçeyi gözlemeden bütün öğrencileri suçlamak", "Yalnız bir afiş asıp ölçüm yapmamak", "Çöpleri saymadan sorunun bittiğini varsaymak"],
             "Çözümden önce sorunun örüntüsü ve olası nedenleri izlenebilir verilerle belirlenmelidir."),
        task(environment, "analysis", "Parkta günlük su tüketimi 900 L'dir. Zaman ayarlı sulama 620 L, kaçak onarımı 700 L öngörüyor; iki çözümün maliyetleri de uygulanabilir. Hangi seçim beklenen yarara göre daha güçlüdür?",
             "Tüketimi daha fazla azaltması beklenen zaman ayarlı sulama",
             ["Hiç ölçüm yapılmayan mevcut düzen", "Daha az azaltım sağlayan seçeneği yalnız adı kısa diye seçmek", "İki seçeneğin verisini yok saymak"],
             "Uygulanabilirlik eşitken beklenen su tasarrufu ölçütü 620 L seçeneğini destekler."),
        task(environment, "application", "Bir dere temizliği projesinin işe yarayıp yaramadığını görmek için hangi izleme planı uygundur?",
             "Aynı noktalarda temizlik öncesi ve sonrası atık miktarı ile su kalitesi verilerini karşılaştırmak",
             ["Yalnız proje logosunu değerlendirmek", "Temizlikten önce veri toplamamak", "Her ölçümde farklı ve kayıtsız bir yöntem kullanmak"],
             "Önce-sonra karşılaştırması çözümün beklenen değişimle ilişkisini sınar."),
        task(environment, "error-analysis", "Bir öğrenci “Çevre sorunu için aklıma gelen ilk çözüm mutlaka en iyisidir.” diyor. Hangi düzeltme gerekir?",
             "Birden fazla seçenek uygulanabilirlik, yarar ve sürdürülebilirlik ölçütleriyle karşılaştırılmalıdır.",
             ["Çözüm seçenekleri için kanıt gerekmez.", "En pahalı çözüm her zaman en etkilidir.", "Sonuçları izlemek çözüm sürecine zarar verir."],
             "Karar verme, seçenekleri açık ölçütlerle sınamayı gerektirir."),
        task(environment, "application", "Gürültü sorunu için iki öneri var: A yalnız bir gün uyarı yapıyor, B yoğun saatleri belirleyip kalıcı sessiz alan düzenliyor. Sürdürülebilirlik ölçütüne göre hangisi seçilmelidir?",
             "Uzun süre uygulanabilecek düzen kurduğu için B",
             ["Bir günlük olduğu için A", "Ölçüt kullanmadan rastgele biri", "Sorunu tanımlamadığı için ikisi de aynı derecede başarılı"],
             "Sürdürülebilir çözüm tek seferlik tepki yerine kalıcı ve izlenebilir bir düzen oluşturur."),
        task(environment, "analysis", "Fidanların kuruması için yalnız 'az sulama' nedeni öne sürülüyor; ancak toprak, hastalık ve sıcaklık verileri yok. Hangi değerlendirme uygundur?",
             "Tek nedeni kesinleştirmeden farklı olasılıklar için kanıt toplanmalıdır.",
             ["İlk tahmin kanıtsız da kesin sonuçtur.", "Toprak ve sıcaklık fidanları hiçbir zaman etkilemez.", "Neden araştırması yerine yalnız fidan sayısı gizlenmelidir."],
             "Çevre sorunları birden çok etkene bağlı olabilir; neden kanıtla sınanır."),
        task(environment, "application", "Mahallede hava kirliliğini azaltma önerileri karşılaştırılacak. Hangi ölçüt seti karar için uygundur?",
             "Beklenen salım azalması, uygulanabilirlik, maliyet ve süreklilik",
             ["Önerinin adındaki harf sayısı", "Sunumu yapan kişinin yaşı", "Afişte kullanılan renk sayısı"],
             "Çözüm ölçütleri sorunun etkisi ve uygulama koşullarıyla doğrudan ilgili olmalıdır."),
        task(environment, "comprehension", "Bir çevre çözümü uygulandıktan sonra sonuç neden izlenmelidir?",
             "Beklenen gelişmenin gerçekleşip gerçekleşmediğini görüp gerekirse çözümü güncellemek için",
             ["İlk kararın değişmesini yasaklamak için", "Yeni kanıtları yok saymak için", "Problemin tanımını gizlemek için"],
             "İzleme, çözümün etkisini kanıtlar ve iyileştirme gereksinimini gösterir."),
        task(environment, "analysis", "Atık kutularının yeri değiştirildikten sonra koridordaki günlük atık 40 parçadan 12'ye düşüyor. Hangi sonuç kanıt sınırını korur?",
             "Bu dönemde yer değişikliği atık azalmasına katkı sağlamış olabilir; izleme sürdürülmelidir.",
             ["Okuldaki atık sorunu sonsuza kadar kesin bitmiştir.", "Kutuların yeri ile sonuç arasında hiçbir ilişki olamaz.", "Tek veri bütün okullar için aynı sonucu kanıtlar."],
             "Ölçüm olumlu değişimi destekler; kalıcılık ve başka etkenler için izleme gerekir."),
    ]


def school_rule_tasks():
    n = "tr-g06-ingilizce-note-001"
    return [
        task(n, "comprehension", "Which sentence expresses an obligation at school?", "Students must arrive on time.",
             ["Students can use the art room.", "Students may play outside.", "Students like the school garden."], "Must expresses an obligation."),
        task(n, "comprehension", "What does 'mustn't' show in a school rule?", "A prohibition",
             ["A past event", "A personal hobby", "A future prediction"], "Mustn't tells learners that an action is forbidden."),
        task(n, "comprehension", "Which phrase asks for permission politely?", "May I open the window?",
             ["You must open the window.", "Could you close the window?", "The window was open."], "May I ...? is a polite permission question."),
        task(n, "comprehension", "Choose the rule that is suitable for a library.", "You must be quiet.",
             ["You must shout across the room.", "You can damage the books.", "You must run between the shelves."], "Quiet behaviour supports reading and study in a library."),
        task(n, "comprehension", "In the sentence 'Students are allowed to use the lab with a teacher,' what is permitted?", "Using the lab with a teacher",
             ["Entering the lab alone", "Skipping every science lesson", "Taking equipment home"], "Allowed to identifies the permitted action and its condition."),
        task(n, "comprehension", "Which English sentence has the meaning 'Koridorlarda koşamazsın'?", "You can't run in the corridors.",
             ["You can run in the corridors.", "You must run in the corridors.", "You run in the playground."], "Can't gives the required negative permission meaning."),
        task(n, "comprehension", "Which word completes a rule about respectful behaviour: 'You ___ listen when others speak.'?", "must",
             ["can", "mustn't", "might"], "Must is followed by the base verb and marks a duty."),

        task(n, "application", "A sign says: 'SCIENCE LAB — goggles are required.' Which rule matches it?", "You must wear goggles in the science lab.",
             ["You can leave your goggles at home.", "You mustn't enter any classroom.", "You are allowed to break equipment."], "The sign states a required safety action."),
        task(n, "application", "Complete the notice: 'Keep food outside. You ___ eat in the computer room.'", "mustn't",
             ["must", "are", "did"], "The notice prohibits eating in that room."),
        task(n, "application", "Teacher: 'The floor is wet.' Student: 'What should I tell my friends?' Choose the best warning.", "You mustn't run here.",
             ["You can slide on the floor.", "You must bring more water.", "You are allowed to push others."], "A no-running rule directly addresses the wet-floor risk."),
        task(n, "application", "Your school permits phones only during lunch break. Which sentence reports the rule correctly?", "We can use our phones during lunch break.",
             ["We must use phones in every lesson.", "We can't use phones at lunch.", "We used phones before the school opened."], "Can expresses permission limited to the stated time."),
        task(n, "application", "Complete the dialogue: '___ I borrow this dictionary?' — 'Yes, but return it today.'", "Can",
             ["Mustn't", "Did", "Never"], "Can I ...? asks for permission in this classroom dialogue."),
        task(n, "application", "The art room rule is 'Clean your desk after the activity.' Which student follows it?", "Mina puts the materials away and wipes her desk.",
             ["Efe leaves paint on the table.", "Lara hides the cleaning cloth.", "Can throws paper on the floor."], "Mina performs the required clean-up action."),
        task(n, "application", "Choose the clearest English rule for a staircase safety poster.", "Hold the handrail and don't push.",
             ["Draw on the steps.", "Run faster near the stairs.", "Leave your bag on a step."], "The selected wording gives two relevant safety actions."),
        task(n, "application", "A new student asks, 'Is chewing gum permitted in class?' The rule says it is forbidden. What should you answer?", "No, you aren't allowed to chew gum in class.",
             ["Yes, you are allowed to chew gum in class.", "No, but you must chew gum in class.", "Yes, chewing gum is required in class."], "Not allowed to communicates the stated prohibition."),
        task(n, "application", "Two rules are needed for an emergency exit. Which pair is most appropriate?", "Keep the exit clear; follow the teacher's instructions.",
             ["Block the door; ignore all instructions.", "Store bags at the exit; run back alone.", "Lock the route; wait without telling anyone."], "A clear route and following instructions support safe evacuation."),
        task(n, "application", "Rewrite 'It is necessary to submit homework on Friday' as a school rule.", "You must submit your homework on Friday.",
             ["You don't have to submit your homework.", "You can submit your homework whenever you want.", "You must submit your homework on Monday."], "Must accurately converts necessity into a rule."),

        task(n, "analysis", "Read the notice: 'Students may enter the music room at break, but food is not allowed.' Which action follows both conditions?", "Deniz enters at break without food.",
             ["Arda eats a sandwich inside.", "Selin enters during a lesson without permission.", "Mert brings juice and cake at break."], "Deniz respects the permitted time and the food prohibition."),
        task(n, "analysis", "Rule A: 'You must wear sports shoes in the gym.' Rule B: 'You can choose any T-shirt.' What is the difference?", "Rule A is an obligation; Rule B is permission.",
             ["Both rules are prohibitions.", "Rule A is permission; Rule B is an obligation.", "Both rules give optional advice."], "Must and can have different functions in the two rules."),
        task(n, "analysis", "A poster reads 'NO RUNNING', but its explanation says 'Students may run near the stairs.' What should be corrected?", "The explanation should say students mustn't run there.",
             ["The poster should give permission to run.", "No change is needed because the messages agree.", "Only the location phrase should be removed."], "The verbal explanation must match the prohibition on the sign."),
        task(n, "analysis", "The rules are: (1) arrive by 8:30, (2) bring your ID, (3) no drinks in the hall. Who follows all rules?", "Ada arrives at 8:20 with her ID and no drink.",
             ["Bora arrives at 8:40 with his ID.", "Cem arrives at 8:10 with juice.", "Duru arrives at 8:20 without her ID."], "Ada meets each of the three conditions."),
        task(n, "analysis", "A student says, 'Can I leave early?' The teacher answers, 'No, you must finish the safety check first.' What is required before leaving?", "Finishing the safety check",
             ["Opening every window", "Skipping the check", "Calling the cafeteria"], "The must-clause states the required prior action."),

        task(n, "error-analysis", "A learner writes, 'You must to raise your hand.' Which correction is grammatical?", "You must raise your hand.",
             ["You must raising your hand.", "You must raised your hand.", "You to must raise your hand."], "A modal verb is followed by the base form without to."),
        task(n, "error-analysis", "A learner translates a ban as 'You can eat in the lab.' Which sentence fixes the meaning?", "You can't eat in the lab.",
             ["You can eating in the lab.", "You ate in the lab tomorrow.", "You must food in the lab."], "Can't changes permission to prohibition."),
        task(n, "error-analysis", "A learner says, 'Mustn't means an activity is optional.' What is the correct explanation?", "Mustn't means the activity is forbidden.",
             ["Mustn't describes a completed activity.", "Mustn't means everyone likes the activity.", "Mustn't asks what time it is."], "The negative modal marks a ban, not a choice."),
        task(n, "error-analysis", "A learner answers 'Yes, you can't' to 'Can I use the library?' when permission is given. Which answer is correct?", "Yes, you can.",
             ["Yes, you mustn't.", "No, you can permission.", "Yes, you did can."], "The short answer must use can and agree with the positive permission."),
    ]


def school_people_tasks():
    n = "tr-g06-ingilizce-note-002"
    return [
        task(n, "comprehension", "Who manages a school and coordinates its general work?", "The principal",
             ["The librarian", "The school nurse", "The class teacher"], "Principal names the person responsible for managing the school."),
        task(n, "comprehension", "Which school worker organizes books and helps readers find them?", "The librarian",
             ["The principal", "The school nurse", "The secretary"], "A librarian manages library resources and assists readers."),
        task(n, "comprehension", "What does a school counselor usually do?", "Listens to students and guides them",
             ["Repairs every classroom window", "Cooks all cafeteria meals", "Writes every student's homework"], "Counselors support students by listening and guiding."),
        task(n, "comprehension", "Choose the correct Simple Present sentence about a teacher.", "A teacher explains lessons.",
             ["A teacher explain lessons.", "A teacher explaining lessons every day.", "A teacher are explain lessons."], "A third-person singular subject takes explains."),

        task(n, "application", "You feel ill during a lesson. Who is the most appropriate person to visit first at school?", "The school nurse",
             ["The librarian", "The school counselor", "The secretary"], "The school nurse deals with health concerns and first aid."),
        task(n, "application", "Complete the question: '___ helps you choose a suitable book?'", "Who",
             ["What", "Where", "When"], "Who asks about a person performing the role."),
        task(n, "application", "The office needs someone to organize documents and answer calls. Which role matches the need?", "The secretary",
             ["The school nurse", "The librarian", "The counselor"], "These duties belong to the secretary."),
        task(n, "application", "Complete the reply: 'What does the janitor do?' — 'He ___ the school clean.'", "keeps",
             ["keep", "keeping", "is keep"], "He requires the third-person singular form keeps."),
        task(n, "application", "A new student cannot find the science room. Which request is most suitable?", "Could you show me where the science room is?",
             ["Who teaches science this year?", "Can you help me with my science homework?", "Is science your favourite subject?"], "The request clearly asks a school person for directions."),

        task(n, "analysis", "Read: 'Ms Lee checks students' health. Mr Can arranges books. Ms Aylin manages school records.' Who is the librarian?", "Mr Can",
             ["Ms Lee", "Ms Aylin", "All three people"], "Arranging books is the librarian clue."),
        task(n, "analysis", "Ece says, 'I attend lessons, complete assignments and respect classroom rules.' Which role is she describing?", "A student's responsibilities",
             ["A principal's management duties", "A nurse's medical duties", "A librarian's cataloguing duties"], "The listed actions are learner responsibilities."),
        task(n, "analysis", "A profile says: 'He listens to personal problems, gives guidance and keeps appointments private.' Which title fits best?", "School counselor",
             ["School nurse", "Librarian", "Principal"], "Listening and guidance identify the counselor role."),

        task(n, "error-analysis", "A learner writes, 'The principal manage the school.' Which correction is needed?", "The principal manages the school.",
             ["The principal managing the school.", "The principal manage schools yesterday every day.", "The principal are manage the school."], "The singular subject needs the -s form manages."),
        task(n, "error-analysis", "A learner says, 'A librarian treats injured students.' Which correction matches school roles?", "A school nurse treats injured students.",
             ["A library treats injured books.", "A student manages every school.", "A secretary gives medical treatment in every case."], "Health care is the nurse's role, not the librarian's."),
    ]


def routine_tasks():
    n = "tr-g06-ingilizce-note-003"
    return [
        task(n, "comprehension", "Which tense is commonly used to describe a school routine?", "The Simple Present",
             ["The Past Perfect", "The Future Perfect", "The Past Continuous only"], "Repeated daily actions are normally expressed with the Simple Present."),
        task(n, "comprehension", "Which sequence word introduces the last step?", "Finally",
             ["First", "Usually", "Before"], "Finally marks the closing action in an ordered routine."),
        task(n, "application", "Complete the sentence: 'Mert ___ classes at half past eight every day.'", "starts",
             ["start", "starting", "is start"], "Mert is third-person singular, so start takes -s."),
        task(n, "application", "Choose the natural order for a weekday morning.", "First I get up, then I have breakfast, and after that I go to school.",
             ["First I go to school, then I wake up, and finally I get dressed.", "First I have lunch, then I get up, and after that I have breakfast.", "First I start classes, then I leave home, and finally I pack my bag."], "The selected sequence uses logical actions and correct linking words."),
        task(n, "application", "Ask Ela about the frequency of her library visits.", "How often do you go to the library?",
             ["When do you go to the library?", "Where is the library?", "Do you go to the library on Monday?"], "How often plus do asks about frequency."),
        task(n, "analysis", "Read: 'I finish school at three. I usually do homework at four, but I never watch TV on weekdays.' Which statement is true?", "The speaker does not watch TV on weekdays.",
             ["The speaker finishes school at four.", "The speaker never does homework.", "The speaker watches TV every weekday."], "Never directly rules out weekday TV viewing."),
        task(n, "analysis", "Bora's list is: 07:00 get up, 08:30 start classes, 12:20 have lunch, 15:10 finish school. What happens before lunch?", "He starts classes.",
             ["He finishes school.", "He goes to bed.", "He has dinner."], "08:30 occurs before the 12:20 lunch entry."),
        task(n, "error-analysis", "A learner writes, 'She usually do her homework.' Which sentence is correct?", "She usually does her homework.",
             ["She does usually her homework always yesterday.", "She usually doing her homework.", "She do usually her homework."], "The third-person singular verb is does; the frequency adverb precedes it."),
        task(n, "error-analysis", "A learner uses 'never' but says the action happens every day. Which explanation fixes the contradiction?", "Never means the action happens zero times.",
             ["Never means every day.", "Never gives a clock time.", "Never changes the subject to plural."], "Never is the zero-frequency adverb."),
    ]


def celebration_tasks():
    n = "tr-g06-ingilizce-note-004"
    return [
        task(n, "comprehension", "Which question asks for the date of a celebration?", "When is the celebration?",
             ["Where is the celebration?", "Who joins the celebration?", "What do people wear?"], "When asks about time or date."),
        task(n, "comprehension", "Which of the following words means 'kutlamak'?", "celebrate",
             ["borrow", "repair", "measure"], "Celebrate is the verb for marking a special day."),
        task(n, "comprehension", "Choose the phrase that describes a national day.", "a national celebration",
             ["a classroom accident", "a daily homework tool", "a weather measurement"], "National celebration is the relevant category phrase."),
        task(n, "application", "Complete the sentence: 'We ___ Republic Day on October 29.'", "celebrate",
             ["celebrates", "celebrating", "is celebrate"], "The plural subject we takes the base verb celebrate."),
        task(n, "application", "An invitation says 'Sunday, 2 p.m.; school garden; traditional games.' Which question is answered by 'school garden'?", "Where is the celebration?",
             ["When is the celebration?", "What activities are planned?", "Who is invited?"], "School garden gives the location."),
        task(n, "application", "Choose the best sentence for a festival poster showing families visiting relatives.", "Families visit their relatives during the holiday.",
             ["Families stay apart during every holiday.", "Only one person celebrates all national days.", "People spend the holiday doing ordinary schoolwork."], "The sentence correctly describes a repeated celebration activity."),
        task(n, "application", "Your friend asks what people do on a special day. Which reply is suitable?", "They decorate the streets and share traditional food.",
             ["It takes place in May.", "It is held in the town square.", "My sister thinks it is exciting."], "The reply gives two clear celebration activities."),
        task(n, "analysis", "Read: 'The event is on April 23. Children perform dances and read poems at school.' What is the text mainly about?", "A children's national celebration",
             ["A routine maths lesson", "A library prohibition", "A phone repair guide"], "The date and school performances identify a national celebration for children."),
        task(n, "analysis", "Two cards say: A—'October 29, parade and flags'; B—'family visits, sweets and holiday wishes.' What do both cards describe?", "Ways people celebrate special days",
             ["Rules for a science lab", "Jobs in a school office", "Daily bus times"], "Though the occasions differ, both cards list celebration practices."),
        task(n, "analysis", "The invitation lists a date and food but not a place. Which information should be added so guests know where to go?", "The venue",
             ["The dress code", "The guest list", "A photo of the food"], "A venue supplies the missing location information."),
        task(n, "error-analysis", "A learner writes, 'People celebrates the festival every year.' Which correction is grammatical?", "People celebrate the festival every year.",
             ["People is celebrate the festival.", "People celebrating every festival year.", "People does celebrates the festival."], "The plural subject people takes the base verb celebrate."),
    ]


def learning_preference_tasks():
    n = "tr-g06-ingilizce-note-005"
    return [
        task(n, "comprehension", "Which sentence expresses a learning preference?", "I prefer pair work to individual work.",
             ["Pair work begins after lunch.", "Our class completes two projects.", "Individual work takes thirty minutes."], "Prefer ... to ... compares two choices."),
        task(n, "comprehension", "Which verb form correctly completes the preference statement 'I ___ solving puzzles'?", "enjoy",
             ["enjoys", "enjoyed", "enjoying"], "Enjoy is the form that agrees with I and is followed by the gerund solving."),
        task(n, "comprehension", "What does 'I'd rather read than watch a video' mean?", "Reading is the speaker's preferred activity.",
             ["The speaker dislikes both activities equally.", "The speaker watched a video yesterday.", "Reading is forbidden."], "Would rather ... than ... gives the stronger choice."),
        task(n, "application", "Complete the reply: 'Do you like group projects?' — 'Yes, I ___ working with classmates.'", "enjoy",
             ["enjoys", "am enjoy", "doesn't enjoys"], "I takes enjoy, followed by working."),
        task(n, "application", "Ayşe likes speaking activities more than writing. Which of the following sentences reports her preference?", "Ayşe prefers speaking to writing.",
             ["Ayşe prefers writing to speaking.", "Ayşe likes speaking and writing equally.", "Ayşe dislikes both speaking and writing."], "Prefers ... to ... correctly compares the two activities."),
        task(n, "application", "Ask a classmate to choose between a project and a game.", "Which do you prefer, doing a project or playing a game?",
             ["When do you finish the project?", "Do you play games after school?", "Why is this project difficult?"], "Which do you prefer...? presents two clear alternatives."),
        task(n, "application", "Which option completes the sentence 'Kerem doesn't like ___ long texts'?", "reading",
             ["reads", "readed", "is read"], "Like/dislike can be followed by the -ing form reading."),
        task(n, "analysis", "Survey: Elif—group work; Can—pair work; Nisa—group work; Ali—individual work. Which activity is chosen most often?", "Group work",
             ["Pair work", "Individual work", "All activities equally"], "Group work has two choices, while the others have one each."),
        task(n, "analysis", "Read: 'I love experiments because I learn by doing, but I dislike copying long notes.' Which activity best fits the learner?", "A hands-on science task",
             ["Reading a long chapter without a task", "Listening to a lecture without practising", "Copying a full page of definitions"], "The stated reason supports an activity based on doing."),
        task(n, "analysis", "Teacher: 'We can debate or write alone.' Lina: 'I feel more confident when I share ideas with others.' What will Lina probably prefer?", "The debate",
             ["Writing alone", "Skipping the lesson", "A task with no communication"], "Sharing ideas with others aligns with the interactive debate."),
        task(n, "error-analysis", "A learner writes, 'She prefer group work.' Which correction is needed?", "She prefers group work.",
             ["She preferring group work.", "She do prefers group work.", "She is prefer group work."], "The third-person singular subject requires prefers."),
        task(n, "error-analysis", "A learner says 'I prefer maths than science.' Which form matches the target structure?", "I prefer maths to science.",
             ["I prefer maths from science.", "I prefers maths to science.", "I am prefer maths than science."], "The standard comparison is prefer A to B."),
    ]


def learning_technology_tasks():
    n = "tr-g06-ingilizce-note-006"
    return [
        task(n, "comprehension", "Which item is an interactive learning technology?", "An educational app",
             ["A printed worksheet", "A paper dictionary", "A set of cardboard flashcards"], "An educational app can present and respond to learning activities."),
        task(n, "comprehension", "What does 'offline' mean in a technology description?", "Not connected to the internet",
             ["Connected to a live website", "Saved only in cloud storage", "Synchronised through the internet"], "Offline describes use without an internet connection."),
        task(n, "comprehension", "Which question asks someone to choose a device?", "Which one do you prefer, a tablet or a laptop?",
             ["Do you use a tablet at school?", "Where is your laptop?", "When do you study online?"], "The question presents two devices and asks for a preference."),
        task(n, "application", "Complete the sentence: 'I prefer ___ e-books on a tablet.'", "reading",
             ["readed", "am read", "reads"], "Prefer can be followed by the -ing form reading."),
        task(n, "application", "A student has no internet at home but wants digital practice. Which option best fits?", "An app with downloadable offline exercises",
             ["A live stream that never works offline", "A link with no saved content", "An online-only meeting at all times"], "Downloadable exercises match the stated offline need."),
        task(n, "application", "Which question can you ask to learn whether your partner likes using a smart board?", "Do you like using a smart board?",
             ["Which smart board is in the classroom?", "When do you use the smart board?", "How many smart boards are there?"], "Do you like using...? is the correct present-tense preference question."),
        task(n, "application", "Mira learns new words best by listening. Which digital resource is most suitable?", "An audio vocabulary activity",
             ["A text-only grammar page", "A labelled diagram without sound", "A silent reading quiz"], "Audio practice directly supports the stated listening preference."),
        task(n, "application", "Complete the dialogue: 'Do you prefer printed books or e-books?' — 'I ___ e-books because I can change the text size.'", "prefer",
             ["prefers", "am prefer", "prefering"], "I takes the base form prefer."),
        task(n, "analysis", "Tool A works offline and has audio; Tool B needs internet and has video only. A learner lacks internet and prefers listening. Which tool fits both conditions?", "Tool A",
             ["Tool B", "Both tools fail both conditions", "Neither tool has audio"], "Tool A matches both the connection limit and learning preference."),
        task(n, "analysis", "Read: 'Eren likes quick feedback after each answer. Selin prefers taking notes on paper.' Who is more likely to choose an interactive quiz app?", "Eren",
             ["Selin", "Both for the same stated reason", "Neither because apps cannot give feedback"], "Immediate feedback is the feature Eren explicitly values."),
        task(n, "analysis", "A class survey shows: tablet 9, laptop 6, smart board 9, e-book reader 3. Which conclusion is supported?", "Tablet and smart board are joint top choices.",
             ["Laptop is the only top choice.", "Nobody chose an e-book reader.", "All tools received nine votes."], "Tablet and smart board share the largest count, nine."),
        task(n, "analysis", "A review says, 'The app has useful videos, but its buttons do not work with a screen reader.' Which evaluation is balanced?", "It offers learning content but has an accessibility limitation.",
             ["It is perfect in every way.", "It has no useful content at all.", "Accessibility never affects tool choice."], "The conclusion preserves both the benefit and the stated limitation."),
        task(n, "error-analysis", "A learner writes, 'I like use tablets.' Which sentence is correct?", "I like using tablets.",
             ["I likes use tablets.", "I am like tablets use.", "I like used tablets tomorrow."], "Like is followed naturally by the -ing activity using."),
        task(n, "error-analysis", "A learner answers a preference question with 'Yes, I tablet.' Which complete response is suitable?", "I prefer the tablet.",
             ["I am tablet prefer.", "I prefers the tablet do.", "The tablet yes I."], "A preference response needs a subject, preference verb and object."),
    ]


def mobile_effect_task():
    n = "tr-g06-ingilizce-note-007"
    return [
        task(n, "analysis", "Read: 'Arda uses his phone until midnight. He feels tired in class and rarely talks to family at dinner.' Which advice addresses both effects?",
             "He should stop using the phone before bed and keep it away during family meals.",
             ["He should increase screen time at midnight.", "He should replace every conversation with messages.", "He shouldn't sleep or meet his family."],
             "The advice responds to the sleep and face-to-face communication problems in the text."),
    ]


TASK_BUILDERS = [
    science_tasks, school_rule_tasks, school_people_tasks, routine_tasks,
    celebration_tasks, learning_preference_tasks, learning_technology_tasks,
    mobile_effect_task,
]


def make_record(
    local: int, item: dict[str, Any], note: dict[str, Any],
    *, batch: int = 10, number_base: int = 900,
) -> dict[str, Any]:
    subject = str(note["subject"])
    subject_slug = {
        "Fen Bilimleri": "fen", "İngilizce": "ingilizce", "Matematik": "matematik",
        "Sosyal Bilgiler": "sosyal-bilgiler", "Türkçe": "turkce",
        "Bilişim Teknolojileri ve Yazılım": "bilisim", "Din Kültürü ve Ahlak Bilgisi": "dkab",
    }.get(subject)
    if subject_slug is None:
        raise ValueError(f"unsupported subject for authored record: {subject}")
    qid = f"tr-g06-bank-{subject_slug}-b{batch:02d}-q{local:03d}"
    correct_position = (local - 1) % 4
    choices = rotate(item["correct"], item["wrongs"], correct_position)
    explanation = str(item["explanation"]).rstrip()
    if explanation[-1:] not in ".!?…":
        explanation += "."
    if subject == "İngilizce":
        explanation += " The other options either change the intended meaning, break the target structure, or contradict the prompt."
    elif subject == "Matematik":
        explanation += " Diğer seçenekler işlem ilişkisini, sayı özelliğini veya soruda verilen koşulları birlikte sağlamaz."
    else:
        explanation += " Diğer seçenekler ölçülen veriyi, belirtilen koşulu veya bilimsel neden-sonuç ilişkisini birlikte korumaz."
    correct_reason = f"Doğru gerekçe: {explanation}"
    wrong_reasons = [
        f"Kavram veya dil işlevi karışıklığı: {item['wrongs'][0]} seçeneği hedeflenen anlamı ya da yapıyı karşılamaz.",
        f"Koşul ve yapı hatası: {item['wrongs'][1]} seçeneği sorudaki bağlamı veya dil kuralını korumaz.",
        f"Kanıt dışı ya da ilgisiz çıkarım: {item['wrongs'][2]} seçeneği verilen bilgiyle desteklenmez.",
    ]
    reason_map = {item["correct"]: correct_reason, **dict(zip(item["wrongs"], wrong_reasons))}
    objective = str((note.get("objectives") or [note.get("objective")])[0])
    level = LEVEL_SEQUENCE[local - 1]
    return {
        "type": "question", "id": qid, "questionId": qid,
        "questionNumber": number_base + local, "subject": subject, "grade": 6,
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
            f"Düzey {level}; {note['title']} içeriğini {item['mode']} görevinde kullanmayı "
            "ve üç ayrı yanılgıyı ayırmayı gerektirir."
        ),
        "questionType": item["mode"],
        "familyId": f"tr-g06-bank-{subject_slug}-b{batch:02d}-family-{local:03d}",
        "authoringTemplateId": f"g6-{subject_slug}-b{batch:02d}-{objective.lower().replace('.', '-')}-{item['mode']}-v{local:03d}",
        "objectiveSource": note.get("objectiveSource"),
        "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [],
        "visualRequirement": "none",
        "visualNeed": {
            "level": "none", "role": "none",
            "rationale": "Çözüm için gerekli metin, veri ve koşullar soru kökünde eksiksiz verilmiştir.",
            "acceptableKinds": [], "evidenceDimensions": [],
        },
        "figure": None, "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    existing = [json.loads(x) for x in OUTPUT.read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(existing) != 900:
        raise RuntimeError("validated first nine batches must exist before batch 10")
    notes = read_notes_only(FEN_SOURCE)
    notes.update(read_notes_only(ENGLISH_SOURCE))
    tasks = [item for builder in TASK_BUILDERS for item in builder()]
    if len(tasks) != 100:
        raise AssertionError(f"batch 10 must contain 100 tasks, got {len(tasks)}")
    expected_modes = {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
    if Counter(item["mode"] for item in tasks) != expected_modes:
        raise AssertionError(Counter(item["mode"] for item in tasks))
    rows = [make_record(local, item, notes[item["note"]]) for local, item in enumerate(tasks, 1)]
    if Counter(row["subject"] for row in rows) != Counter({"Fen Bilimleri": 13, "İngilizce": 87}):
        raise AssertionError(Counter(row["subject"] for row in rows))
    if Counter(row["correctIndex"] for row in rows) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer positions are not exactly balanced")
    OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + rows) + "\n",
        encoding="utf-8", newline="\n",
    )
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    LABELS_OUTPUT.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({
        "batch": 10, "questions": 100, "science": 13, "english": 87,
        "total": len(existing) + len(rows), "modes": dict(Counter(x["mode"] for x in tasks)),
        "sourceQuestionReads": 0,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
