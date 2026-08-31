#!/usr/bin/env python3
"""Append 100 independently authored Grade 6 English questions (batch 11)."""
from __future__ import annotations

from collections import Counter
import json

from author_grade6_bilisim_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade6_fen_batch07 import task
from author_grade6_fen_english_batch10 import ENGLISH_SOURCE, make_record
from author_grade6_mixed_batch03 import read_notes_only


def rows(note: str, values: list[tuple[str, str, str, str, str, str, str]]):
    return [task(note, mode, stem, correct, [w1, w2, w3], explanation)
            for mode, stem, correct, w1, w2, w3, explanation in values]


def mobile_health_tasks():
    n = "tr-g06-ingilizce-note-007"
    return rows(n, [
        ("comprehension", "Which of the following sentences gives advice about healthy phone use?", "You should take regular screen breaks.",
         "Phones help us send messages.", "My phone has a blue case.", "We used a phone yesterday.", "Should expresses advice, and the action limits continuous screen use."),
        ("comprehension", "What does 'screen time' refer to?", "The time spent looking at and using screens",
         "The time needed to clean a phone", "The date a phone was bought", "The size of a phone case", "Screen time measures duration of screen use."),
        ("comprehension", "Which connector introduces a reason?", "because", "so", "but", "then", "Because links an effect or opinion to its reason."),
        ("comprehension", "Which phrase describes direct communication in the same place?", "face-to-face communication",
         "battery level", "online storage", "screen brightness", "Face-to-face means people communicate while physically together."),
        ("application", "Complete the advice: 'Your eyes feel tired, so you ___ look away from the screen for a while.'", "should",
         "shouldn't", "did", "are", "Should recommends the helpful action."),
        ("application", "Eda checks messages during every family meal. Which of the following suggestions best supports social interaction?", "She should put her phone away and join the conversation.",
         "She should send messages to people at the table.", "She should wear headphones during the meal.", "She should increase the screen brightness.", "Putting the device away creates time for direct conversation."),
        ("application", "Choose the sentence that correctly links a cause and an effect.", "I stop using my phone early because I want to sleep well.",
         "I want to sleep well because so my phone.", "Because I stop my phone but early.", "I sleep phone and reason early.", "The because-clause gives a clear reason for the action."),
        ("application", "Your friend has used a phone continuously for two hours. What is suitable advice?", "You should rest your eyes and move for a few minutes.",
         "You should keep the same position for two more hours.", "You shouldn't take any break today.", "You should hold the screen closer to your eyes.", "A break and movement address prolonged use."),
        ("application", "Which option completes the dialogue: 'I cannot sleep after late-night videos.' — 'You ___ use your phone just before bed.'?", "shouldn't",
         "should", "can", "are", "Shouldn't advises against the habit connected to the sleep problem."),
        ("application", "A class wants a balanced phone-use rule. Which rule is most appropriate?", "Use phones for learning when permitted, but keep them away during discussion and rest time.",
         "Use phones without limits in every activity.", "Ban every digital tool for all purposes.", "Replace all face-to-face work with messages.", "The rule preserves useful use while limiting social and health costs."),
        ("analysis", "Read: 'Lina video-calls her grandmother weekly, but she also scrolls until 1 a.m.' Which evaluation is balanced?", "The phone supports communication, but late use may harm her sleep.",
         "The phone has only positive effects.", "The phone has only negative effects.", "Calling and sleep are unrelated to the text.", "The evaluation keeps both the communication benefit and sleep risk."),
        ("analysis", "Survey results are: before-bed phone use—8 hours average sleep: 7 students; no before-bed use—8 hours average sleep: 15 students. What can the class investigate next?", "Whether bedtime phone habits and sleep duration are related",
         "Whether phone colour changes the school timetable", "Whether every phone user has exactly the same sleep", "Whether sleep can be measured without any data", "The two recorded variables support a question about bedtime use and sleep."),
        ("analysis", "Aras says, 'Phones make communication easier.' Duru says, 'They can reduce conversation at dinner.' How are the statements related?", "They describe different possible social effects of phones.",
         "Only Aras gives an effect.", "The statements have exactly the same meaning.", "Both statements concern battery charging.", "One effect supports distant contact; the other concerns reduced direct talk."),
        ("analysis", "A poster says, 'Use night mode; then unlimited midnight use is harmless.' Which part needs correction?", "Night mode does not remove every effect of long or late use.",
         "Night mode always makes sleep unnecessary.", "The poster should recommend more midnight notifications.", "Screen duration can never affect rest.", "A display setting cannot justify an unlimited-use claim."),
        ("error-analysis", "A learner writes, 'You should to limit your screen time.' Which correction is grammatical?", "You should limit your screen time.",
         "You should limiting your screen time.", "You should limited your screen time.", "You to should limit your screen time.", "Should is followed directly by the base verb."),
        ("error-analysis", "A learner says, 'Because shows a result, and so shows a reason.' Which explanation is correct?", "Because introduces a reason, while so introduces a result.",
         "Because and so both mark only time.", "So always introduces a person.", "Because cannot join ideas.", "The two connectors have opposite cause-result functions."),
    ])


def film_art_tasks():
    n = "tr-g06-ingilizce-note-008"
    return rows(n, [
        ("comprehension", "Which question asks about a type of film?", "What kind of films do you like?",
         "When does the cinema open?", "Where is the museum?", "How long is the film?", "What kind of asks for a category or genre."),
        ("comprehension", "Which adjective most naturally describes a comedy?", "funny", "scary", "silent", "crowded", "A comedy is commonly described as funny."),
        ("application", "Which option completes the preference statement 'I enjoy ___ photography exhibitions'?", "visiting",
         "visits", "visited", "visit", "Enjoy is followed by the -ing form visiting."),
        ("application", "Mert likes facts about nature. Which of the following films would best match his preference?", "A wildlife documentary",
         "A fictional horror film", "A romantic comedy", "An action film about car races", "A documentary offers factual content about nature."),
        ("application", "Ask your friend to explain a film preference.", "Why do you like science-fiction films?",
         "Where is the science-fiction film?", "How many films are on the shelf?", "When did the ticket arrive?", "Why requests the reason for a preference."),
        ("analysis", "Read: 'Nora dislikes horror films because they are scary, but she loves animations with clever stories.' Which film should Nora choose?", "An animated film with a thoughtful story",
         "A horror film with frightening scenes", "A film chosen only because it is long", "A documentary she says she hates", "The choice matches both her preferred form and stated reason."),
        ("analysis", "Ali says, 'The paintings are beautiful, but the exhibition is too crowded.' Which summary keeps both ideas?", "He likes the art but dislikes the crowded setting.",
         "He dislikes every painting.", "He thinks the exhibition is empty.", "He gives no opinion about the art.", "The summary preserves the positive art view and negative setting view."),
        ("error-analysis", "A learner writes, 'She enjoy watching cartoons.' Which sentence is correct?", "She enjoys watching cartoons.",
         "She enjoy to watching cartoons.", "She enjoying watches cartoons.", "She does enjoys watching cartoons.", "The singular subject needs enjoys, followed by watching."),
        ("error-analysis", "A learner says, 'I prefer documentaries than comedies.' Which correction follows the target structure?", "I prefer documentaries to comedies.",
         "I prefer documentaries from comedies.", "I prefers documentaries to comedies.", "I am prefer documentaries than comedies.", "Prefer A to B is the correct comparison pattern."),
    ])


def family_solution_tasks():
    n = "tr-g06-ingilizce-note-009"
    return rows(n, [
        ("comprehension", "Which expression makes a suggestion?", "Why don't we talk about it?",
         "We talked about it yesterday.", "The problem is in the kitchen.", "My brother has a new book.", "Why don't we...? is used to suggest a joint action."),
        ("comprehension", "Which verb means to say that you are sorry?", "apologize", "argue", "borrow", "decide", "Apologize names the action of saying sorry."),
        ("comprehension", "Which action supports a respectful family discussion?", "Listening without interrupting",
         "Shouting over every speaker", "Ignoring the problem", "Blaming a person before hearing them", "Listening allows family members to understand each other."),
        ("application", "Two siblings want the same desk at the same time. Which suggestion is fair?", "Let's make a timetable and take turns.",
         "Let's hide the desk from both siblings.", "One sibling must always use it without discussion.", "They should argue until one gives up.", "A timetable shares the resource through an agreed plan."),
        ("application", "Complete the suggestion: '___ about discussing the chores after dinner?'", "How",
         "Who", "Where", "Must", "How about plus -ing introduces a suggestion."),
        ("application", "Your sister says, 'You used my headphones without asking.' Which reply is most constructive?", "I'm sorry. I will ask before using them again.",
         "It is your fault for owning headphones.", "I will never listen to you.", "Let's pretend nothing happened.", "The reply apologizes and proposes a specific change."),
        ("application", "A family keeps forgetting shared chores. What solution is most practical?", "Create a visible weekly task list and review it together.",
         "Stop doing every household task.", "Change the tasks without telling anyone.", "Argue about the list each morning.", "A shared list clarifies roles and can be checked."),
        ("analysis", "Read: 'Mina is studying. Her brother plays loud music. Mina explains her need calmly, and he uses headphones.' What resolved the disagreement?", "Clear communication and a reasonable change",
         "Ignoring Mina's need", "Making the music louder", "Leaving the problem undefined", "Mina states the problem and her brother changes the source of disturbance."),
        ("analysis", "Parent: 'We must leave at eight.' Child: 'I need ten more minutes to finish.' Which response seeks agreement?", "Can we leave at 8:10 if I get ready immediately after this?",
         "I will ignore the departure time.", "You never understand anything.", "The trip must be cancelled forever.", "The response offers a specific compromise while recognizing both needs."),
        ("analysis", "A family solution works for one day but the same argument returns every week. What should they do next?", "Review the cause and improve the agreement together.",
         "Assume the problem is permanently solved.", "Stop listening to new information.", "Choose a random family member to blame.", "Repeated conflict is evidence that the first plan needs revision."),
        ("error-analysis", "A learner writes, 'Let's to share the chores.' Which correction is grammatical?", "Let's share the chores.",
         "Let's sharing the chores.", "Let's shared the chores.", "Let's to sharing the chores.", "Let's is followed by the base verb without to."),
        ("error-analysis", "A learner says, 'A solution means proving that one family member is always wrong.' Which correction is appropriate?", "A solution should address the problem and consider the people involved.",
         "A solution must increase every disagreement.", "Listening is unnecessary in family decisions.", "Blame is the only form of agreement.", "Problem solving focuses on needs, actions and workable agreements, not fixed blame."),
    ])


def family_home_tasks():
    n = "tr-g06-ingilizce-note-010"
    return rows(n, [
        ("comprehension", "Which sentence correctly uses 'has got'?", "My aunt has got two children.",
         "My aunt have got two children.", "My aunt has get two children.", "My aunt got has two children.", "A singular third-person subject takes has got."),
        ("comprehension", "Which phrase describes a home with parents and their children?", "a nuclear family home",
         "a sports hall", "a school office", "a city bus", "A nuclear family consists of parents and their children."),
        ("application", "Complete the description: 'There ___ three bedrooms in our house.'", "are",
         "is", "has", "am", "A plural noun phrase takes there are."),
        ("application", "A photo shows one garden behind the house. Which sentence describes it?", "There is a garden behind the house.",
         "There are a garden behind the house.", "The house have got behind a garden.", "There is three gardens behind the house.", "There is agrees with the single garden and gives its location."),
        ("application", "Complete the question to ask about a sibling: '___ she got a brother?'", "Has",
         "Have", "Does got", "Is", "Has she got...? is the question form for third-person possession."),
        ("analysis", "Read: 'Eren lives with his parents, sister, grandparents and uncle.' Which description fits?", "He lives in an extended family.",
         "He lives alone.", "He has no relatives at home.", "Only his classmates live there.", "Several generations and another relative indicate an extended family."),
        ("analysis", "House A has a garden and two bedrooms. House B has no garden and four bedrooms. Which statement is supported?", "House B has more bedrooms, but House A has a garden.",
         "Both houses have four bedrooms.", "House A has no outdoor space.", "House B has fewer bedrooms than House A.", "The comparison preserves both recorded differences."),
        ("error-analysis", "A learner writes, 'There is two bathrooms.' Which correction is grammatical?", "There are two bathrooms.",
         "There has two bathrooms.", "There are a bathroom.", "There is are two bathrooms.", "The plural noun bathrooms requires there are."),
        ("error-analysis", "A learner says, 'He have got a friendly cousin.' Which correction is needed?", "He has got a friendly cousin.",
         "He having got a friendly cousin.", "He do have got a friendly cousin.", "He has get a friendly cousin.", "He takes has got in the possession structure."),
    ])


def city_country_tasks():
    n = "tr-g06-ingilizce-note-011"
    return rows(n, [
        ("comprehension", "Which adjective means 'full of many people'?", "crowded", "peaceful", "empty", "quiet", "Crowded describes a place containing many people."),
        ("comprehension", "Which of the following sentences describes more than one facility?", "There are two hospitals in the town.",
         "There is a hospital in the town.", "The town has quiet.", "There are a hospital in town.", "There are agrees with the plural facility phrase."),
        ("comprehension", "Which comparative sentence is grammatical?", "The city is noisier than the village.",
         "The city is noisy than the village.", "The city noisier the village.", "The city is more noisy that village.", "Noisier than is the correct comparative pattern."),
        ("application", "A place has heavy traffic, many apartment blocks and frequent buses. How should it be described?", "It is an urban area.",
         "It is an isolated forest camp.", "It is an empty field.", "It is a mountain path with no transport.", "The facilities and traffic are typical urban clues."),
        ("application", "Complete the comparison: 'The village is ___ than the city at night.'", "quieter",
         "quiet", "quietest", "more quieter", "Quieter than is the comparative form of quiet."),
        ("application", "A visitor needs regular public transport and a large hospital. Which location profile best meets the needs?", "A town centre with bus lines and a regional hospital",
         "A remote farm with no bus service", "A forest cabin reached only on foot", "A small field outside every settlement", "The town-centre profile explicitly includes both required services."),
        ("application", "Describe a village with one school and three farms.", "There is one school and there are three farms.",
         "There are one school and one farms.", "There is three farms and schools.", "The village have one school are farms.", "Singular and plural facilities require different there structures."),
        ("application", "Which question can you ask someone about facilities in their neighbourhood?", "Are there any parks near your home?",
         "Is your home quieter than?", "How crowded parks do?", "Does any park are near?", "Are there any...? asks whether plural facilities exist."),
        ("analysis", "Profile K: quiet, one small shop, large gardens. Profile L: busy, many services, heavy traffic. Which conclusion is supported?", "K is more rural, while L is more urban.",
         "K has heavier traffic than L.", "L has fewer services than K.", "Both profiles describe exactly the same setting.", "The contrasting features align K with rural and L with urban life."),
        ("analysis", "A student says, 'The countryside is always better because it is quiet.' What makes the comparison incomplete?", "It ignores needs such as transport, work and health services.",
         "Quiet is not an English adjective.", "Every rural place has identical services.", "A comparison must use only one feature.", "A place can suit different needs; one advantage is not a complete evaluation."),
        ("analysis", "Data: City—bus every 10 minutes, air-quality score 55; village—bus twice daily, air-quality score 82. Which summary is balanced?", "The city has more frequent transport, while the village has the higher air-quality score.",
         "The village has more frequent buses.", "The city leads on both recorded measures.", "The two places have equal scores and schedules.", "The summary reports one advantage for each setting from the data."),
        ("error-analysis", "A learner writes, 'There is many shops in the city.' Which correction is grammatical?", "There are many shops in the city.",
         "There are much shop in the city.", "There is many shop are city.", "There have many shops in city.", "Plural shops takes there are."),
        ("error-analysis", "A learner says, 'The village is more quieter than the city.' Which form is correct?", "The village is quieter than the city.",
         "The village is more quietest than the city.", "The village quieter that the city.", "The village is quiet than the city.", "The comparative quieter does not take additional more."),
    ])


def sports_place_tasks():
    n = "tr-g06-ingilizce-note-012"
    return rows(n, [
        ("comprehension", "Which activity normally takes the verb 'go'?", "go cycling", "play cycling", "do cycling ball", "make cycling", "Cycling is commonly used with go."),
        ("comprehension", "Where do people usually swim as a sport in a city?", "in a swimming pool",
         "on a tennis racket", "inside a football", "under a bicycle", "A swimming pool is the facility designed for swimming."),
        ("comprehension", "Which of the following questions asks about frequency?", "How often do you go hiking?",
         "Where do you go hiking?", "Who goes hiking with you?", "Why do you like hiking?", "How often asks how frequently an activity happens."),
        ("application", "Complete the routine: 'Selin usually ___ tennis at the sports centre.'", "plays",
         "goes", "does", "rides", "Tennis takes play, and Selin requires plays."),
        ("application", "A family wants an outdoor activity on a safe forest trail. Which option fits best?", "hiking",
         "indoor gymnastics", "swimming in a city pool", "basketball in a sports hall", "Hiking directly uses a forest trail outdoors."),
        ("application", "Which question can you ask a village resident about available sports facilities?", "Is there a sports field in your village?",
         "How often is your village?", "Does a sport field plays?", "Where many sports are village?", "Is there...? asks whether a singular facility exists."),
        ("application", "Read the notice: 'River path closed after heavy rain.' Which plan is safest?", "Choose another open route for cycling.",
         "Ignore the closure and enter the path.", "Cycle faster through the damaged section.", "Wait alone in the flooded area.", "An alternative open route respects the safety notice."),
        ("analysis", "Town A has a pool and sports hall. Village B has mountain trails and a river route. Which activity pair matches the places?", "Swimming in A and hiking in B",
         "Hiking inside A's pool and swimming on B's mountain", "Horse riding in A's sports hall and tennis in B's river", "Only the same indoor sport in both places", "Each activity uses a facility or landscape listed for its place."),
        ("analysis", "Ece says, 'I never go running, but I cycle every weekend.' Which statement is true?", "Cycling is part of her weekly routine.",
         "She runs every weekend.", "She never cycles.", "She does both activities every day.", "Every weekend identifies a recurring cycling habit."),
        ("analysis", "A survey records football 12, hiking 8, swimming 12 and cycling 5. Which conclusion is supported?", "Football and swimming are joint top choices.",
         "Cycling is the most popular activity.", "Nobody chose hiking.", "All activities have equal totals.", "Football and swimming share the largest count."),
        ("error-analysis", "A learner writes, 'I play swimming on Saturdays.' Which correction uses the natural verb?", "I go swimming on Saturdays.",
         "I do swimming ball on Saturdays.", "I plays swimming on Saturdays.", "I go swimmed on Saturdays.", "Swimming as an activity commonly takes go plus -ing."),
    ])


def food_habit_tasks():
    n = "tr-g06-ingilizce-note-013"
    return rows(n, [
        ("comprehension", "Which meal is normally eaten in the morning?", "breakfast", "dinner", "dessert", "supper at midnight", "Breakfast names the morning meal."),
        ("comprehension", "Which adverb means an action happens zero times?", "never", "always", "usually", "sometimes", "Never expresses zero frequency."),
        ("comprehension", "Which question asks about a regular food habit?", "What do you usually eat for lunch?",
         "Where is the lunch box?", "Who cooked yesterday's soup?", "How much is the menu?", "Usually and the Simple Present target a recurring habit."),
        ("application", "Complete the sentence: 'My brother ___ milk with breakfast every day.'", "drinks",
         "drink", "drinking", "is drink", "The singular subject takes drinks in the Simple Present."),
        ("application", "Aylin eats fruit on Monday, Wednesday and Friday, but not every day. Which adverb best fits?", "sometimes",
         "never", "always", "once every year", "Sometimes matches a recurring but non-daily habit."),
        ("application", "Which question can you ask Bora to learn whether he likes vegetables?", "Do you like vegetables?",
         "Does you like vegetables?", "Are you like vegetables?", "Do vegetables likes you?", "Do you like...? is the correct preference question."),
        ("application", "Complete the reply: 'What does Ela have for breakfast?' — 'She ___ eggs and cheese.'", "has",
         "have", "having", "do have", "She takes has in the Simple Present."),
        ("analysis", "Read: 'I always eat breakfast, usually drink water with lunch and never have coffee.' Which drink is absent from the routine?", "coffee",
         "water", "a breakfast drink not named", "every possible drink", "Never directly excludes coffee."),
        ("analysis", "According to the food diary—Mon: soup, Tue: salad, Wed: soup, Thu: rice, Fri: soup—which lunch appears most often?", "soup",
         "salad", "rice", "All foods equally", "Soup appears on three days, more than the other entries."),
        ("analysis", "Mina says, 'I hate fish, but I eat it every Friday because it is our family meal.' Which summary is accurate?", "Her preference is negative, but her routine includes fish weekly.",
         "She loves fish and eats it daily.", "She never eats fish.", "The text gives no food preference.", "The summary separates what she likes from what she regularly does."),
        ("error-analysis", "A learner writes, 'He always eat breakfast.' Which correction is grammatical?", "He always eats breakfast.",
         "He eats always breakfast every.", "He always eating breakfast.", "He do always eats breakfast.", "The singular subject requires eats, with the frequency adverb before the main verb."),
    ])


def cooking_tasks():
    n = "tr-g06-ingilizce-note-014"
    return rows(n, [
        ("comprehension", "Which of the following cooking methods uses hot water?", "boil", "grill", "bake", "fry", "Boil means cooking food in hot or boiling water."),
        ("comprehension", "Which word introduces the last instruction in a recipe?", "Finally", "First", "Before", "Usually", "Finally marks the last step."),
        ("comprehension", "Which phrase gives a measured quantity?", "a cup of flour",
         "flour quickly", "a pan of cooking", "mix of an oven", "A cup of gives a container-based amount."),
        ("application", "Complete the instruction: '___ the onions into small pieces.'", "Cut",
         "Cuts", "Cutting", "To cut", "Recipe imperatives begin with the base verb."),
        ("application", "A recipe says, 'Cook the vegetables in steam above hot water.' Which method is described?", "steam",
         "fry", "grill", "roast", "Steam cooks food using water vapour."),
        ("application", "Choose the logical order for a simple salad.", "First wash the vegetables, then cut them, and finally mix them.",
         "First mix whole dirty vegetables, then wash the empty bowl.", "First serve the salad, then buy the ingredients.", "First cut nothing, then finish before washing.", "Washing precedes cutting, and mixing follows preparation."),
        ("application", "Complete the quantity: 'Add ___ olive oil to the mixture.'", "a spoon of",
         "a slice of", "a piece of", "an oven of", "A spoon of is a suitable measure for a small amount of liquid oil."),
        ("analysis", "Recipe card: 1 heat the oven, 2 mix flour and eggs, 3 pour into a tray, 4 bake. Which tool is essential in the final step?", "an oven",
         "a freezer", "a kettle only", "a grill rack without heat", "Bake explicitly requires an oven."),
        ("analysis", "Dish A is cooked in oil in a pan. Dish B is cooked on a rack over heat. Which methods are used?", "A is fried; B is grilled.",
         "A is boiled; B is steamed.", "A is baked; B is frozen.", "Both dishes are boiled.", "Oil in a pan indicates frying, while a rack over heat indicates grilling."),
        ("analysis", "A recipe lists ingredients and quantities but gives no sequence. What information is missing?", "The ordered preparation steps",
         "The names of the ingredients", "Every quantity", "The type of dish", "Without ordered steps, the cook does not know when or how to combine ingredients."),
        ("error-analysis", "A learner writes a recipe step as 'Cuts the tomatoes.' Which imperative is correct?", "Cut the tomatoes.",
         "Cutting the tomatoes.", "To cuts the tomatoes.", "You cuts the tomatoes.", "An imperative begins with the base form cut."),
    ])


def disaster_animal_tasks():
    n = "tr-g06-ingilizce-note-015"
    return rows(n, [
        ("comprehension", "Which word means the natural home of an animal?", "habitat", "shelter worker", "storm warning", "rescue team", "Habitat is the place and conditions where a species lives."),
        ("comprehension", "Which disaster can burn a woodland habitat?", "a forest fire", "an earthquake drill", "a light breeze", "a cloudy morning", "A forest fire directly burns vegetation and animal shelter."),
        ("application", "Complete the safety rule: 'During a wildlife rescue, people ___ follow trained responders' instructions.'", "must",
         "mustn't", "were", "might not always", "Must expresses the required safety behaviour."),
        ("application", "A flood has covered an animal shelter's entrance. Which message is appropriate?", "Do not enter the water; call trained rescue services.",
         "Walk into moving water alone.", "Move every animal without equipment.", "Ignore the flooded entrance.", "The message avoids hazardous water and directs the situation to trained responders."),
        ("analysis", "Read: 'After the drought, the pond dried up and birds left the area.' Which chain is supported?", "Drought reduced water habitat, so birds lost a needed resource.",
         "Birds caused the drought by leaving.", "The pond gained more water after the drought.", "The text shows no change in habitat.", "The text links water loss to a change in animal use of the area."),
        ("analysis", "A fire report records fewer nesting sites but does not count animals. Which conclusion stays within the evidence?", "The fire damaged nesting habitat; animal population change needs separate data.",
         "Every animal certainly died.", "The animal population certainly increased.", "Nesting sites are unrelated to habitat.", "The report supports habitat damage but not an exact population outcome."),
        ("error-analysis", "A learner writes, 'Animals must to leave the damaged area.' Which correction is grammatical?", "Animals must leave the damaged area.",
         "Animals must leaving the damaged area.", "Animals must left the damaged area.", "Animals to must leave the damaged area.", "Must takes the base verb without to."),
        ("error-analysis", "A learner says, 'A flood and a drought always damage habitats in exactly the same way.' Which correction is appropriate?", "Different disasters can damage habitats through different processes.",
         "All disasters have identical causes and effects.", "Habitat evidence is unnecessary after a disaster.", "Only the disaster name matters, not the observed damage.", "Flooding and water shortage can create different forms of habitat harm."),
    ])


TASK_BUILDERS = [
    mobile_health_tasks, film_art_tasks, family_solution_tasks,
    family_home_tasks, city_country_tasks, sports_place_tasks,
    food_habit_tasks, cooking_tasks, disaster_animal_tasks,
]


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 1000:
        raise RuntimeError("validated first ten batches must exist before batch 11")
    notes = read_notes_only(ENGLISH_SOURCE)
    tasks = [item for builder in TASK_BUILDERS for item in builder()]
    if len(tasks) != 100:
        raise AssertionError(f"batch 11 must contain 100 tasks, got {len(tasks)}")
    expected_modes = {"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}
    if Counter(item["mode"] for item in tasks) != expected_modes:
        raise AssertionError(Counter(item["mode"] for item in tasks))
    rows_out = [
        make_record(local, item, notes[item["note"]], batch=11, number_base=1000)
        for local, item in enumerate(tasks, 1)
    ]
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
        "batch": 11, "questions": 100, "english": 100, "total": 1100,
        "modes": dict(Counter(item["mode"] for item in tasks)), "sourceQuestionReads": 0,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
