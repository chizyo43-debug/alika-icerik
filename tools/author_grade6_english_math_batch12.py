#!/usr/bin/env python3
"""Append 60 English and 40 mathematics questions for Grade 6 batch 12."""
from __future__ import annotations

from collections import Counter
import json
import math
from pathlib import Path

from author_grade6_bilisim_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade6_english_batch11 import rows
from author_grade6_fen_english_batch10 import ENGLISH_SOURCE, make_record
from author_grade6_mixed_batch03 import read_notes_only


MATH_SOURCE = Path("turkiye/6-sinif/matematik/matematik-tum.jsonl")


def remaining_animal_disaster_tasks():
    n = "tr-g06-ingilizce-note-015"
    return rows(n, [
        ("comprehension", "Which action means moving an animal away from danger?", "rescue",
         "damage", "destroy", "flood", "Rescue means helping a person or animal reach safety."),
        ("application", "Which option completes the rule 'Visitors ___ feed displaced wild animals without expert advice'?", "mustn't",
         "must", "can always", "were", "Mustn't expresses the safety prohibition."),
        ("application", "A storm has broken branches near a nest. Which report is clear and safe?", "The nest may be at risk; inform the wildlife team and keep a safe distance.",
         "Climb the damaged tree alone.", "Move the nest without training.", "Ignore the broken branches.", "The report identifies the risk and directs it to trained help."),
        ("analysis", "Before a flood, 18 nests were recorded; after it, 11 usable nests remain. Which statement is supported?", "Seven recorded nesting sites became unusable during the observed period.",
         "Every animal in the area disappeared.", "The flood created seven new nests.", "The number of nests did not change.", "The before-after count supports a decrease of seven sites, not a total animal count."),
        ("error-analysis", "A learner writes, 'A forest fire can destroys habitats.' Which correction is grammatical?", "A forest fire can destroy habitats.",
         "A forest fire can destroying habitats.", "A forest fire cans destroy habitats.", "A forest fire can destroyed habitats.", "Can is followed by the base verb destroy."),
    ])


def disaster_people_tasks():
    n = "tr-g06-ingilizce-note-016"
    return rows(n, [
        ("comprehension", "Which word describes a person who has been physically harmed?", "injured",
         "crowded", "traditional", "interactive", "Injured describes someone hurt in an event."),
        ("comprehension", "Which sentence states a general effect of floods?", "Floods can damage homes.",
         "The flood damaged this bridge last year.", "People will visit the museum.", "A storm is a type of film.", "The Simple Present sentence gives a general possible effect."),
        ("comprehension", "Which response shows sympathy after hearing about a disaster?", "I'm sorry to hear that.",
         "That is your fault.", "The event is funny.", "I do not want any details because they are useless.", "The phrase acknowledges another person's difficult experience respectfully."),
        ("application", "Complete the result: 'The storm was very strong, ___ many trees fell.'", "so",
         "because", "before", "although", "So introduces the result of the strong storm."),
        ("application", "A report is about an earthquake that happened yesterday. Which verb form is suitable?", "The earthquake damaged several buildings.",
         "The earthquake damage several buildings yesterday.", "The earthquake will damaged buildings yesterday.", "The earthquake damaging every day yesterday.", "The Simple Past damaged matches the finished time yesterday."),
        ("application", "Choose the clearest emergency message after a landslide blocks a road.", "The road is blocked; use the official alternative route and follow local warnings.",
         "Drive through the blocked section without checking.", "Remove warning signs before help arrives.", "Assume every other road is also closed.", "The message states the condition and a safe verified action."),
        ("application", "Complete the advice: 'People ___ enter a damaged building until officials say it is safe.'", "mustn't",
         "must", "were", "are going", "Mustn't expresses the required prohibition."),
        ("application", "A family lost its home in a flood. Which sentence describes the effect respectfully?", "The family became homeless and needs safe shelter.",
         "The family chose a holiday outdoors.", "The flood improved their house.", "Their housing situation is unrelated to the flood.", "The sentence uses accurate effect vocabulary without blaming the family."),
        ("analysis", "Read: 'The tornado damaged roofs, but no injuries were reported.' Which summary is accurate?", "There was property damage, but the report records no injured people.",
         "No damage happened at all.", "Many injuries were confirmed.", "Only roads were damaged.", "The summary preserves both the roof damage and absence of reported injuries."),
        ("analysis", "Report A says 'may have damaged'; Report B says 'destroyed 24 homes.' Which statement is more specific?", "Report B, because it gives a confirmed action and a number.",
         "Report A, because may always proves certainty.", "Both reports give the same amount of evidence.", "Neither report contains an effect word.", "A counted confirmed outcome is more specific than an uncertain possibility."),
        ("analysis", "A chart shows injuries falling after an evacuation drill programme. Which conclusion stays within the evidence?", "The programme may have contributed to safer responses; other factors should also be checked.",
         "The programme is the only possible cause.", "Drills always prevent every injury.", "The falling numbers prove that no disaster occurred.", "The trend supports a possible contribution but not exclusive causation."),
        ("error-analysis", "A learner writes, 'The earthquake destroy many houses last night.' Which correction is grammatical?", "The earthquake destroyed many houses last night.",
         "The earthquake destroys many houses last night.", "The earthquake destroying many houses last night.", "The earthquake did destroyed many houses last night.", "The finished past event requires destroyed."),
        ("error-analysis", "A learner says, 'Because introduces the result in this sentence: The river rose, because homes flooded.' Which correction is appropriate?", "Use so before the result: The river rose, so homes flooded.",
         "Use because for every result without a reason.", "Remove both clauses and keep only flooded.", "Because and so have no role in cause and result.", "So links a preceding cause to its consequence."),
    ])


def universe_life_tasks():
    n = "tr-g06-ingilizce-note-017"
    return rows(n, [
        ("comprehension", "Which sentence is a prediction about the future?", "People will discover more distant planets.",
         "Astronauts work in space.", "There are many stars in the sky.", "Earth has one Moon.", "Will plus the base verb marks a future prediction."),
        ("comprehension", "Which word names a person who travels and works in space?", "astronaut",
         "librarian", "counselor", "chef", "Astronaut is the space-travel profession."),
        ("comprehension", "Which of the following structures states that many objects exist?", "There are many galaxies.",
         "There is many galaxies.", "Many galaxies is there.", "There has many galaxies.", "There are agrees with the plural noun galaxies."),
        ("application", "Complete the prediction: 'Scientists ___ find signs of life on another world one day.'", "will",
         "are yesterday", "did tomorrow", "has", "Will forms a future prediction with find."),
        ("application", "Ask someone for a future prediction about Mars.", "Will people live on Mars in the future?",
         "Do people lived on Mars tomorrow?", "Where people will Mars?", "Are Mars live people?", "Will plus subject and base verb forms the future question."),
        ("application", "Which option completes the short answer: 'Will robots explore distant moons?' — 'Yes, they ___.'?", "will",
         "do", "are", "will be explore", "A will-question takes will in the short answer."),
        ("application", "Choose the sentence that separates a fact from an opinion.", "There are planets beyond Earth; I think some may support life.",
         "Every planet certainly has people.", "An opinion is always a measured fact.", "There are no questions about life in the universe.", "The first clause reports existence; the second is explicitly marked as a view."),
        ("application", "A poster needs a question about existence in space. Which one is suitable?", "Is there water on that planet?",
         "Will there water planet?", "Does water is there?", "Where many water are?", "Is there...? asks whether a singular or uncountable thing exists."),
        ("analysis", "Read: 'The telescope found a planet, but scientists have no evidence of life there.' Which conclusion is supported?", "A planet was found, but life on it is still unconfirmed.",
         "Living creatures were definitely found.", "The telescope found no planet.", "Every new planet must contain life.", "The conclusion keeps discovery and evidence limits separate."),
        ("analysis", "Sentence A: 'Stars produce light.' Sentence B: 'People will visit another star soon.' How do the sentences differ?", "A states a general fact; B makes a future prediction.",
         "Both report completed past events.", "A is a plan and B is a definition.", "Both use there are to show existence.", "The Simple Present and will serve different communication purposes."),
        ("analysis", "A survey asks, 'Will humans find life elsewhere?' Results: yes 18, no 7, unsure 5. Which summary is accurate?", "Most respondents predict yes, but the survey does not prove life exists.",
         "The survey proves extraterrestrial life.", "No is the most common answer.", "Nobody is unsure.", "Opinion counts show the leading prediction, not a scientific discovery."),
        ("error-analysis", "A learner writes, 'People will lives on another planet.' Which correction is grammatical?", "People will live on another planet.",
         "People will living on another planet.", "People wills live on another planet.", "People will lived on another planet.", "Will is followed by the base verb live."),
        ("error-analysis", "A learner says, 'There is many stars in the galaxy.' Which correction is needed?", "There are many stars in the galaxy.",
         "There is a many stars in the galaxy.", "There have many stars in the galaxy.", "There are much star in the galaxy.", "The plural noun stars requires there are."),
    ])


def future_life_tasks():
    n = "tr-g06-ingilizce-note-018"
    return rows(n, [
        ("comprehension", "Which structure usually describes a prior plan?", "be going to",
         "the Simple Past", "there were", "mustn't", "Be going to commonly communicates an intention arranged before speaking."),
        ("comprehension", "Which sentence is a negative future prediction?", "Homes won't use as much energy.",
         "Homes will use smart sensors.", "Homes use energy today.", "Homes are going to install a sensor tomorrow.", "Won't plus the base verb forms a negative prediction."),
        ("comprehension", "Which short answer correctly replies to 'Will you have a robot?'?", "Yes, I will.",
         "Yes, I do will.", "Yes, I am have.", "Yes, I going to.", "A will-question takes will in its short answer."),
        ("comprehension", "Which sentence describes an arranged intention?", "We are going to visit the technology fair on Saturday.",
         "Robots will probably become smaller.", "The fair opened last year.", "Smart homes use sensors.", "The stated Saturday arrangement is expressed with be going to."),
        ("application", "Which option completes the prediction 'I think public transport ___ become cleaner'?", "will",
         "is going without to", "did", "has", "I think commonly introduces a will prediction."),
        ("application", "Deniz bought a ticket for tomorrow's robotics exhibition. Which sentence reports the plan?", "Deniz is going to visit the robotics exhibition tomorrow.",
         "Deniz will perhaps visited the exhibition.", "Deniz visits the exhibition yesterday.", "Deniz going visit without a plan.", "The ticket is evidence of a prior plan, so is going to fits."),
        ("application", "Complete the question: '___ your family going to use solar energy?'", "Is",
         "Will be", "Does", "Are", "Family is treated as singular here, so Is begins the question."),
        ("application", "Your friend says, 'I forgot my water bottle.' Which of the following replies gives a natural immediate decision?", "I'll lend you mine.",
         "I lent you mine yesterday.", "I am going to buy one next month.", "You should bring two bottles tomorrow.", "Will can express a decision made at the moment of speaking."),
        ("application", "Which of the following is a grammatically correct future sentence?", "They aren't going to buy a new car this year.",
         "They isn't going to buy a new car.", "They aren't going buy a new car.", "They not going to bought a car.", "Plural they takes aren't going to plus the base verb."),
        ("analysis", "Read: 'The city has approved the project and signed the contract. It ___ build a smart-energy centre next year.' Which form fits the evidence?", "is going to",
         "did", "will have yesterday", "is building every past year", "Approval and a contract indicate a prior plan."),
        ("analysis", "Arda says, 'Robots will do every job.' Ela says, 'Robots may help with some tasks.' Which claim is more cautious?", "Ela's claim, because it avoids an absolute prediction.",
         "Arda's claim, because every always proves certainty.", "Both claims are identical.", "Neither sentence refers to technology.", "May and some preserve uncertainty and scope."),
        ("analysis", "According to the plan list—Monday: book tickets; Friday: travel—which sentence best describes Friday?", "We are going to travel on Friday.",
         "We travelled on Friday yesterday.", "We will booking tickets Friday.", "We are travel every Friday.", "The list records a planned future trip."),
        ("analysis", "A prediction from five years ago did not happen. What is the best evaluation?", "Predictions are not guarantees and should be updated with new evidence.",
         "Every prediction is a permanent fact.", "New evidence must be ignored.", "The grammar of will makes events certain.", "Future language expresses expectations, not proof."),
        ("error-analysis", "A learner writes, 'She will to live in a smart home.' Which correction is grammatical?", "She will live in a smart home.",
         "She will living in a smart home.", "She wills live in a smart home.", "She will lived in a smart home.", "Will takes the base verb without to."),
        ("error-analysis", "A learner writes, 'They is going to travel.' Which correction is needed?", "They are going to travel.",
         "They am going to travel.", "They are going travel.", "They is going travel.", "They takes are in the be going to structure."),
        ("error-analysis", "A learner says, 'Will and be going to always have exactly the same use.' Which correction is appropriate?", "Will often gives predictions or immediate decisions; be going to often gives prior plans.",
         "Will can only describe the past.", "Be going to cannot express future meaning.", "Both structures are nouns, not future forms.", "The forms overlap but have typical differences in prediction and intention."),
    ])


def space_technology_tasks():
    n = "tr-g06-ingilizce-note-019"
    return rows(n, [
        ("comprehension", "Which verb means to create a device or method for the first time?", "invent",
         "travel", "observe", "borrow", "Invent means creating something new."),
        ("comprehension", "Which of the following sentences expresses ability?", "Robots can explore dangerous places.",
         "Robots will explore Mars next year.", "Robots are going to enter the lab tomorrow.", "Robots explored the area yesterday.", "Can communicates present or general ability."),
        ("comprehension", "Which question word asks about a reason?", "Why", "Where", "When", "Who", "Why requests a reason or explanation."),
        ("comprehension", "Which vehicle is designed to travel beyond Earth's atmosphere?", "a spacecraft",
         "a city bus", "a fishing boat", "a bicycle", "A spacecraft is built for travel in space."),
        ("application", "Which option completes the possibility statement 'New sensors ___ help astronauts detect danger earlier'?", "could",
         "did yesterday", "are to helped", "has", "Could expresses a possible ability or outcome."),
        ("application", "Ask how a robot can support a space mission.", "How can a robot help astronauts?",
         "Where robot can is astronauts?", "When helps a robot why?", "Who astronaut does robot space?", "How can plus subject and base verb asks about method or ability."),
        ("application", "A mission has a confirmed launch schedule for next month. Which sentence reports the plan?", "The team is going to launch the spacecraft next month.",
         "The team launched it next month yesterday.", "The team will to launches the spacecraft.", "The spacecraft going launch itself.", "The confirmed schedule supports be going to for a plan."),
        ("application", "Choose a suitable caption for a robot testing rocks on another planet.", "The robot can collect samples where conditions are dangerous for people.",
         "The robot is a natural planet.", "Samples can drive the spacecraft alone.", "Danger makes all technology unnecessary.", "The caption links robot capability to a mission need."),
        ("analysis", "Read: 'The rover can take photos, but it cannot repair its own wheel.' Which evaluation is accurate?", "It has a useful ability and a stated limitation.",
         "It can perform every possible task.", "It cannot take any photos.", "A wheel is unrelated to rover movement.", "The evaluation preserves both clauses."),
        ("analysis", "Question: 'Where will astronauts live?' Answer: 'Because the station is safe.' What is wrong with the answer?", "It gives a reason instead of a place.",
         "It correctly gives a location.", "Where always asks for a person.", "Because introduces a time.", "Where requires location information, while because introduces a reason."),
        ("analysis", "Technology A reduces communication delay; Technology B uses less energy. Which conclusion is balanced?", "Each technology has a different recorded advantage.",
         "A is better on every measure.", "B reduces delay more, although no delay data are given.", "The technologies are identical.", "The evidence supports one distinct benefit for each option."),
        ("analysis", "A headline says, 'Scientists could find a new planet.' Which interpretation is correct?", "Finding a planet is presented as a possibility, not a confirmed event.",
         "A planet has definitely been found.", "Scientists are unable to search.", "Could describes only a past habit here.", "Could keeps the claim uncertain."),
        ("error-analysis", "A learner writes, 'Robots can to carry equipment.' Which correction is grammatical?", "Robots can carry equipment.",
         "Robots can carrying equipment.", "Robots cans carry equipment.", "Robots can carried equipment.", "Can takes the base verb without to."),
    ])


def factor_multiple_tasks():
    n = "tr-g06-matematik-note-001"
    return rows(n, [
        ("comprehension", "Bir doğal sayının çarpanı neyi ifade eder?", "Sayıyı kalansız bölen doğal sayıyı",
         "Sayıdan her zaman büyük olan değeri", "Yalnız sayının on katını", "Bölmede kalan veren sayıyı", "Çarpanla bölmede kalan sıfırdır."),
        ("comprehension", "24 sayısının katları için hangi ifade doğrudur?", "24, 48, 72 biçiminde sürer ve sonlu bir liste değildir.",
         "Yalnız 1 ve 24'ten oluşur.", "24'ten küçük sayılardır.", "Her kat 24'ü kalansız böler.", "Katlar 24'ün doğal sayılarla çarpılmasıyla sınırsız biçimde üretilir."),
        ("application", "36 sayısının eksiksiz çarpan listesi hangisidir?", "1, 2, 3, 4, 6, 9, 12, 18, 36",
         "1, 2, 3, 6, 12, 36", "2, 4, 6, 8, 12, 18, 36", "1, 3, 4, 9, 18, 36", "Çarpan çiftleri 1×36, 2×18, 3×12 ve 4×9'dur."),
        ("application", "24 kare taş, hiç artmadan eş satırlı bir dikdörtgen oluşturacak. Hangisi mümkün bir satır×sütun düzenidir?", "4 × 6",
         "5 × 5", "3 × 7", "2 × 13", "4 ve 6, 24'ün bir çarpan çiftidir."),
        ("analysis", "Bir öğrenci 30'un çarpanlarını 1, 2, 3, 5, 6, 10, 15, 30 yazıyor. Liste nasıl değerlendirilir?", "Liste eksiksizdir; her sayı 30'u kalansız böler.",
         "20 eksik olduğu için liste yanlıştır.", "30 yazılmamalıdır çünkü sayı kendisinin çarpanı olamaz.", "Katlar yazıldığı için listenin tamamı yanlıştır.", "Çarpan çiftleri 1×30, 2×15, 3×10 ve 5×6 bütün listeyi verir."),
        ("analysis", "K dizisi 7, 14, 21, 28; L listesi 1, 2, 4, 7, 14, 28'dir. Hangi sınıflandırma doğrudur?", "K, 7'nin katlarını; L, 28'in çarpanlarını gösterir.",
         "İki liste de yalnız 28'in katlarını gösterir.", "K, 7'nin çarpanlarını; L, 28'in katlarını gösterir.", "İki liste de sınırsız çarpan listeleridir.", "K eşit artan kat örüntüsü, L ise sonlu kalansız bölen listesidir."),
        ("error-analysis", "Bir öğrenci “Bir sayının katları, o sayıyı kalansız bölen sayılardır.” diyor. Hangi düzeltme doğrudur?", "Kalansız bölenler çarpandır; katlar sayının doğal sayılarla çarpılmasıyla oluşur.",
         "Çarpanlar ve katlar her zaman aynı sonlu listedir.", "Katlar yalnız sayıdan küçüktür.", "Bir sayının kendisi ne çarpanı ne katıdır.", "Tanımda çarpan ile kat kavramları yer değiştirmiştir."),
    ])


def divisibility_tasks():
    n = "tr-g06-matematik-note-002"
    return rows(n, [
        ("comprehension", "Bir doğal sayının 10 ile tam bölünmesi için birler basamağı nasıl olmalıdır?", "0 olmalıdır.",
         "5 olmalıdır.", "Çift olan herhangi bir rakam olmalıdır.", "Rakamlar toplamı 10 olmalıdır.", "10'un bütün doğal sayı katları 0 ile biter."),
        ("comprehension", "9 ile bölünebilme ölçütünde hangi bilgi kullanılır?", "Rakamlar toplamının 9'un katı olması",
         "Yalnız son iki basamağın çift olması", "Birler basamağının 5 olması", "İlk rakamın 9 olması", "Bir sayının 9'a göre kalanı rakamlar toplamıyla aynı kalanı verir."),
        ("comprehension", "6 ile tam bölünebilmek için hangi iki koşul birlikte sağlanmalıdır?", "2 ve 3 ile tam bölünebilme",
         "2 ve 5 ile tam bölünebilme", "3 ve 9 ile tam bölünebilme", "4 ve 10 ile tam bölünebilme", "6=2×3 ve bu iki çarpan aralarında asal olduğundan iki ölçüt birlikte kullanılır."),
        ("application", "4 576 sayısı aşağıdakilerden hangisiyle tam bölünür?", "4",
         "5", "9", "10", "Son iki basamak 76, 4'ün katıdır; diğer ölçütler sağlanmaz."),
        ("application", "Rakamları toplamı 27 ve birler basamağı 8 olan sayı hangi sayılarla kesin tam bölünür?", "2, 3, 6 ve 9",
         "Yalnız 2 ve 5", "4 ve 10", "Yalnız 9", "Çiftlik 2'yi, rakam toplamı 3 ve 9'u, iki koşul birlikte 6'yı garanti eder."),
        ("application", "54□ sayısının 5 ve 9 ile tam bölünmesi için □ yerine hangi rakam gelmelidir?", "0",
         "1", "5", "9", "Son basamak 0 olduğunda 5 ölçütü sağlanır; 5+4+0=9 olduğu için sayı 9'a da tam bölünür."),
        ("application", "Son iki basamağı 00 olan bir doğal sayı için hangi sonuç kesin doğrudur?", "2, 4, 5 ve 10 ile tam bölünür.",
         "9 ile kesin tam bölünür.", "3 ile kesin tam bölünmez.", "6 ile kesin tam bölünür.", "00 çift, 4'ün katı ve 0 ile bittiği için 2, 4, 5 ve 10 ölçütlerini sağlar."),
        ("analysis", "2 346 sayısı için bir öğrenci '6 ile bölünür' diyor. Gerekçesi nasıl doğrulanır?", "Sayı çift ve rakamları toplamı 15 olduğu için 2 ve 3 ile tam bölünür.",
         "Son basamağı 6 olduğu için tek başına yeterlidir.", "Son iki basamağı 46 olduğu için 6'ya bölünür.", "İlk rakamı 2 olduğu için 6'ya bölünür.", "6 ölçütü çiftlik ile 3'e bölünebilmenin birlikte sınanmasını gerektirir."),
        ("analysis", "A sayısı 3 ile, B sayısı 2 ile tam bölünüyor. A+B'nin 6 ile bölünmesi hakkında ne söylenebilir?", "Kesin karar verilemez; toplam ayrıca 2 ve 3 ölçütleriyle sınanmalıdır.",
         "Kesinlikle 6 ile bölünür.", "Kesinlikle 6 ile bölünmez.", "Yalnız A'nın son basamağı yeterlidir.", "A ve B hakkında verilen ayrı bilgiler toplamın iki koşulu birden sağlamasını garanti etmez."),
        ("analysis", "Bir sayı hem 4 hem 9 ile tam bölünüyor. Hangisi bu özelliğe sahiptir?", "1 044",
         "1 026", "1 035", "1 050", "1 044'ün son iki basamağı 44 ve rakam toplamı 9'dur."),
        ("error-analysis", "Bir öğrenci “Son basamağı çift olan her sayı 4 ile tam bölünür.” diyor. Hangi düzeltme gerekir?", "4 için sayının son iki basamağının 4'ün katı olması gerekir.",
         "4 için yalnız rakamlar toplamına bakılır.", "Çift sayılar hiçbir zaman 4'e bölünmez.", "Son basamağın 0 olması zorunludur.", "Çiftlik yalnız 2 ölçütünü garanti eder; 4 için son iki basamak incelenir."),
        ("error-analysis", "Bir öğrenci “3 510 sayısı 6 ile bölünmez çünkü son basamağı 0'dur.” diyor. Hangi değerlendirme doğrudur?", "Sayı çift ve rakamları toplamı 9 olduğu için 6 ile tam bölünür.",
         "0 tek rakam olduğu için sayı 6'ya bölünmez.", "6 ile bölünmede yalnız son iki basamak kullanılır.", "Rakamlar toplamı 6 olmalı, 9 olamaz.", "Birler basamağı 0 çiftlik sağlar; rakam toplamı da 3'ün katıdır."),
    ])


def prime_factor_tasks():
    n = "tr-g06-matematik-note-003"
    return rows(n, [
        ("comprehension", "Asal sayının doğru tanımı hangisidir?", "1'den büyük ve yalnız 1 ile kendisine bölünen doğal sayı",
         "Yalnız çift olan doğal sayı", "Tam olarak üç çarpanı olan sayı", "1 dahil bütün tek sayılar", "Asal sayının iki farklı doğal sayı çarpanı vardır."),
        ("comprehension", "1 sayısı neden asal değildir?", "Yalnız bir farklı doğal sayı çarpanı vardır.",
         "Çift sayı olduğu için", "10'dan küçük olduğu için", "Hiç çarpanı olmadığı için", "Asallık iki farklı çarpan gerektirir; 1'in yalnız kendisi vardır."),
        ("comprehension", "Bir doğal sayıyı asal çarpanlarına ayırmak ne anlama gelir?", "Sayıyı asal sayıların çarpımı biçiminde yazmak",
         "Sayıya kadar bütün asalları toplamak", "Sayının yalnız en büyük çarpanını yazmak", "Sayıyı ondalık gösterime çevirmek", "Asal çarpanlara ayırmada bütün çarpanlar asal olana kadar ayrıştırılır."),
        ("application", "84 sayısının asal çarpanlarına ayrılmış biçimi hangisidir?", "2² × 3 × 7",
         "2 × 42", "4 × 3 × 7", "2 × 3 × 14", "84=2×2×3×7 olduğundan bütün çarpanlar asal biçimde 2²×3×7 yazılır."),
        ("application", "Aşağıdaki sayılardan hangisi asaldır?", "47",
         "39", "51", "57", "47, 2, 3, 5 ve 7 ile bölünmez; diğerleri 3'ün katıdır."),
        ("application", "Bir kodun sayısal değeri 2² × 3² × 5 çarpımıyla oluşturuluyor. Bu kodu oluşturan farklı asal çarpanların kümesi hangisidir?", "2, 3 ve 5",
         "2, 5 ve 9", "3, 6 ve 10", "2, 3 ve 15", "Üslü yazımdaki asal tabanlar 2, 3 ve 5'tir; üsler bu farklı asal sayıların tekrar sayısını gösterir."),
        ("application", "2³ × 5 çarpımının değeri kaçtır?", "40",
         "30", "50", "80", "2³=8 ve 8×5=40'tır."),
        ("application", "Bir çarpan ağacında 72 önce 8×9, sonra 8=2×4, 4=2×2 ve 9=3×3 ayrılıyor. Sonuç hangisidir?", "2³ × 3²",
         "2² × 3³", "8 × 3²", "2 × 4 × 9", "Uçlardaki asal sayılar üç tane 2 ve iki tane 3'tür."),
        ("analysis", "91 sayısının asal olup olmadığını sınamak için hangi bölme yeterli bir karşı örnek verir?", "91 ÷ 7 = 13",
         "91 ÷ 2 kalan 1", "91 ÷ 3 kalan 1", "91 ÷ 5 kalan 1", "7 ve 13, 1 ile sayı dışında bir çarpan çifti verdiğinden 91 asal değildir."),
        ("analysis", "İki farklı çarpan ağacı 60 için sırasıyla 6×10 ve 4×15 ile başlıyor. Son asal çarpan sonuçları nasıl olmalıdır?", "İkisi de 2² × 3 × 5 sonucuna ulaşmalıdır.",
         "Başlangıç farklıysa asal çarpanlar zorunlu farklıdır.", "Biri 6×10'da bırakılmalıdır.", "Yalnız 4×15 doğru ayrıştırmadır.", "Farklı ara çarpanlar aynı sayının tek asal çarpan yapısına ulaşır."),
        ("analysis", "Bir çözümde 126=2×3×21 yazılıp işlem bitiriliyor. Eksik nedir?", "21 asal olmadığı için 3×7 biçiminde ayrıştırılmalıdır.",
         "2 asal olmadığı için 1×2 yazılmalıdır.", "126 asal sayı ilan edilmelidir.", "3 çarpanı silinmelidir.", "Asal çarpanlara ayırma bütün uçlar asal olana kadar sürer."),
        ("error-analysis", "Bir öğrenci “1 asaldır çünkü yalnız 1'e bölünür.” diyor. Hangi düzeltme doğrudur?", "Asal sayı iki farklı çarpana sahip olmalıdır; 1'in yalnız bir çarpanı vardır.",
         "1 asaldır çünkü bütün sayıları böler.", "1 bileşik sayıdır çünkü dört çarpanı vardır.", "Asallık yalnız çift sayılar için tanımlanır.", "Öğrenci asallığın iki farklı çarpan koşulunu gözden kaçırmıştır."),
        ("error-analysis", "Bir öğrenci “45=5×9 olduğuna göre asal çarpanlarına ayrılmıştır.” diyor. Hangi düzeltme gerekir?", "9 asal değildir; 45=3²×5 biçiminde yazılmalıdır.",
         "5 asal değildir, bu yüzden yalnız 9 yazılmalıdır.", "45 zaten asal olduğu için ayrıştırılamaz.", "9 yerine 1 yazılmalıdır.", "Son çarpanların tamamı asal olmalıdır; 9 yeniden 3×3 ayrılır."),
    ])


def common_factor_multiple_tasks():
    n = "tr-g06-matematik-note-004"
    return rows(n, [
        ("comprehension", "İki farklı aralıkla tekrarlanan olayın yeniden aynı anda gerçekleşmesi hangi ilişkiyle incelenir?", "Ortak kat ilişkisiyle",
         "Yalnız tek sayının çarpanlarıyla", "Ondalık basamak değeriyle", "Asal sayı tanımıyla", "Tekrar aralıklarının ortak katları birlikte gerçekleşme zamanlarını verir."),
        ("application", "Biri 6, diğeri 8 dakikada bir çalan iki zil şimdi birlikte çaldı. En erken kaç dakika sonra yine birlikte çalar?", "24 dakika",
         "14 dakika", "32 dakika", "48 dakika", "6 ve 8'in en küçük ortak katı 24'tür."),
        ("analysis", "24 m ve 36 m uzunluğundaki iki ip artmayacak biçimde eş ve en uzun parçalara ayrılacak. Neden ortak bölen kullanılır?", "Parça uzunluğu iki toplam uzunluğu da kalansız bölmelidir.",
         "Parça uzunluğu iki sayının ortak katı olmalıdır.", "İplerin toplamı asal olmalıdır.", "Her parça 36 metreden uzun olmalıdır.", "Eş parçanın uzunluğu her iki ölçünün ortak böleni olmak zorundadır."),
        ("error-analysis", "Bir öğrenci “Her 9 ve 12 dakikada bir yapılan iki iş için ilk ortak zamanı bulurken ortak bölen kullanırım.” diyor. Hangi düzeltme doğrudur?", "Tekrarlanan olayların ilk ortak zamanı için en küçük ortak kat kullanılır.",
         "Ortak bölen yalnız tekrar zamanlarında kullanılır.", "İki aralık toplanarak her zaman doğru zaman bulunur.", "Küçük aralık tek başına ortak zamanı verir.", "Zamanlar 9'un ve 12'nin katlarında tekrar eder; ortak olan ilk kat aranır."),
    ])


def decimal_place_tasks():
    n = "tr-g06-matematik-note-005"
    return rows(n, [
        ("comprehension", "7,483 sayısında 8 rakamının basamak değeri hangisidir?", "8/100",
         "8/10", "8/1000", "80/10", "Virgülden sonraki ikinci basamak yüzde birlerdir."),
        ("application", "3 + 4/10 + 6/100 + 2/1000 toplamının ondalık gösterimi hangisidir?", "3,462",
         "3,642", "3,426", "34,62", "Kesirler sırasıyla onda, yüzde ve binde birler basamaklarını verir."),
        ("application", "5,307 sayısında 3 ve 7 rakamlarının basamak değerleri hangileridir?", "3/10 ve 7/1000",
         "3/100 ve 7/10", "3 ve 7/100", "30/10 ve 7/100", "3 onda birler, 7 binde birler basamağındadır."),
        ("analysis", "0,6 ve 0,06 sayılarındaki 6 rakamlarının değerleri nasıl karşılaştırılır?", "0,6'daki değer, 0,06'dakinin 10 katıdır.",
         "İki rakamın basamak değeri eşittir.", "0,06'daki değer, 0,6'dakinin 10 katıdır.", "Karşılaştırma yapılamaz çünkü rakamlar aynıdır.", "6/10, 6/100 değerinin 10 katıdır."),
    ])


TASK_BUILDERS = [
    remaining_animal_disaster_tasks, disaster_people_tasks,
    universe_life_tasks, future_life_tasks, space_technology_tasks,
    factor_multiple_tasks, divisibility_tasks, prime_factor_tasks,
    common_factor_multiple_tasks, decimal_place_tasks,
]


def verify_math_facts() -> None:
    """Recompute the numerical claims used by this batch."""
    assert [value for value in range(1, 37) if 36 % value == 0] == [1, 2, 3, 4, 6, 9, 12, 18, 36]
    assert 4 * 6 == 24
    assert [value for value in range(1, 31) if 30 % value == 0] == [1, 2, 3, 5, 6, 10, 15, 30]
    assert 4576 % 4 == 0 and all(4576 % value for value in (5, 9, 10))
    assert 540 % 5 == 0 and 540 % 9 == 0
    assert 3510 % 6 == 0 and 2346 % 6 == 0 and 1044 % 4 == 0 and 1044 % 9 == 0
    assert 84 == 2**2 * 3 * 7 and 180 == 2**2 * 3**2 * 5 and 72 == 2**3 * 3**2
    assert all(47 % value for value in range(2, math.isqrt(47) + 1))
    assert 91 == 7 * 13 and 60 == 2**2 * 3 * 5 and 126 == 2 * 3**2 * 7 and 45 == 3**2 * 5
    assert math.lcm(6, 8) == 24 and math.gcd(24, 36) == 12
    assert abs((3 + 4 / 10 + 6 / 100 + 2 / 1000) - 3.462) < 1e-12


def main() -> int:
    verify_math_facts()
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1100:
        raise RuntimeError("validated first eleven batches must exist before batch 12")
    notes = read_notes_only(ENGLISH_SOURCE)
    notes.update(read_notes_only(MATH_SOURCE))
    tasks = [item for builder in TASK_BUILDERS for item in builder()]
    if len(tasks) != 100:
        raise AssertionError(f"batch 12 must contain 100 tasks, got {len(tasks)}")
    expected_modes = {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
    if Counter(item["mode"] for item in tasks) != expected_modes:
        raise AssertionError(Counter(item["mode"] for item in tasks))
    rows_out = [
        make_record(local, item, notes[item["note"]], batch=12, number_base=1100)
        for local, item in enumerate(tasks, 1)
    ]
    if Counter(row["subject"] for row in rows_out) != Counter({"İngilizce": 60, "Matematik": 40}):
        raise AssertionError(Counter(row["subject"] for row in rows_out))
    if Counter(row["correctIndex"] for row in rows_out) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer positions are not exactly balanced")
    OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + rows_out) + "\n",
        encoding="utf-8", newline="\n",
    )
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    LABELS_OUTPUT.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({
        "batch": 12, "questions": 100, "english": 60, "mathematics": 40,
        "total": 1200, "modes": dict(Counter(item["mode"] for item in tasks)),
        "sourceQuestionReads": 0,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
