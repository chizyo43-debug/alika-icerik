#!/usr/bin/env python3
"""Append five 100-question Grade 7 English batches from lesson notes only."""
from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any

from author_grade6_fen_english_batch10 import make_record
from author_grade6_fen_batch07 import task
from author_grade6_mixed_batch03 import read_notes_only
from author_grade7_dkab_batch01 import LABELS_OUTPUT, OUTPUT


SOURCE = Path("turkiye/7-sinif/ingilizce/ingilizce-tum.jsonl")
MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15


CONTEXTS = {
    1: [
        ("Green School Fair", "The eco club meets beside the library at 14:40 on Tuesday. Members bring one reusable bottle and present a recycling idea.", "reusable", "eco club meeting", "14:40 on Tuesday"),
        ("Sports Team Notice", "Basketball practice moves to the small gym on Friday because the main hall hosts a concert. Players arrive at 16:10 with indoor shoes.", "practice", "basketball schedule change", "small gym at 16:10"),
        ("Book Exchange Day", "Students label two books at home, leave them at Desk 4 before lunch, and choose replacement books after the second lesson.", "exchange", "book exchange procedure", "Desk 4 before lunch"),
    ],
    2: [
        ("Testing Paper Strength", "Each group hangs equal masses from three paper strips. It records the greatest mass each strip holds and repeats every test twice.", "repeat", "a controlled classroom test", "every test is repeated twice"),
        ("Peer Feedback Routine", "First read your partner's paragraph silently. Next underline one clear detail, and finally suggest one question the reader still has.", "feedback", "peer review steps", "suggest one reader question"),
        ("Vocabulary Station", "Teams sort twelve word cards by meaning, check two uncertain cards in a dictionary, and explain one corrected choice to the class.", "sort", "a vocabulary learning task", "check uncertain cards in a dictionary"),
    ],
    3: [
        ("Balanced Evening", "Eda finishes her snack at 18:00, cycles for half an hour, prepares her school bag, and keeps screens outside the bedroom after 21:15.", "balanced", "an evening well-being routine", "screens stay outside after 21:15"),
        ("Hydration Plan", "Kerem fills a 750-millilitre bottle before school, drinks some at every break, and records whether any water remains at 15:30.", "hydration", "a daily water plan", "the bottle is checked at 15:30"),
        ("Managing a Busy Day", "Lina lists three important tasks, completes the shortest one first, takes a ten-minute movement break, and asks for help with the hardest task.", "priority", "a manageable task routine", "ask for help with the hardest task"),
    ],
    4: [
        ("Weekend Meal Plan", "The family checks what is already in the kitchen, chooses two seasonal vegetables, writes a shopping list, and cooks together on Saturday.", "seasonal", "a family meal plan", "cook together on Saturday"),
        ("Shared Home Tasks", "Aras waters the plants on Monday and Thursday. His sister loads the dishwasher after dinner, while both organise the living room on Sunday.", "shared", "a home responsibility schedule", "organise the living room on Sunday"),
        ("Grandmother's Story Box", "Every photograph has a date on the back. Family members select one photograph, ask two questions, and record the story with permission.", "permission", "a family history activity", "ask two questions about one photograph"),
    ],
    5: [
        ("Neighbourhood Repair Café", "Volunteers inspect broken small items at the community centre from 11:00 to 14:00. Visitors register online and carry their own replacement parts.", "volunteer", "a community repair event", "community centre from 11:00 to 14:00"),
        ("Safer Park Route", "The youth council compares lighting on three routes, marks two dark corners, and recommends the path with working lamps and a pedestrian crossing.", "route", "a neighbourhood safety study", "two dark corners are marked"),
        ("Library Culture Evening", "Guests hear a short local story, learn a traditional playground game, and share a word from a language spoken in their family.", "local", "a community culture evening", "share a family language word"),
    ],
    6: [
        ("Postcards Across Cultures", "Partner classes exchange postcards about a daily custom. Each card explains the custom, avoids stereotypes, and asks one respectful question.", "custom", "a cross-cultural postcard exchange", "ask one respectful question"),
        ("World Food Exhibit", "Groups research where one dish is eaten, identify two main ingredients, and cite the museum or cultural source used for the description.", "source", "a sourced cultural exhibit", "cite the description source"),
        ("Festival Calendar", "The class compares three public celebrations by season, common activities, and community meaning without calling one tradition better than another.", "compare", "a respectful festival comparison", "use three common criteria"),
    ],
    7: [
        ("Wetland Bird Count", "Observers stay on the marked path, count birds for fifteen minutes, record weather conditions, and avoid playing recorded bird calls.", "observe", "a low-impact bird survey", "count for fifteen minutes"),
        ("Forest Soil Check", "Students collect no plants. They compare soil moisture at two approved points, photograph the ground, and return every loose stone to its place.", "moisture", "a careful forest observation", "compare two approved points"),
        ("Pollinator Garden", "The garden team plants native flowers in three beds, counts visiting insects at the same hour each week, and uses no pesticide during the survey.", "native", "a pollinator monitoring plan", "count at the same hour weekly"),
    ],
    8: [
        ("Moon Base Water Brief", "A design team limits each model habitat to twenty litres per day, filters used water, and reports where water is lost from the cycle.", "filter", "a future habitat water system", "twenty litres per day"),
        ("Satellite Debris Alert", "The control team tracks two objects near a satellite, updates their predicted paths every hour, and changes course only if collision risk rises.", "collision", "a space safety procedure", "paths are updated hourly"),
        ("City of 2050 Forum", "Students propose one energy change, estimate its benefit, identify a possible drawback, and revise the proposal after public questions.", "drawback", "a future-city proposal", "revise after public questions"),
    ],
}


def base_data(note: dict[str, Any], variant: int) -> tuple[str, str, str, str, str, str]:
    objective = str(note["objectiveId"])
    _, _, theme_text, skill = objective.split(".")
    title, text, keyword, topic, detail = CONTEXTS[int(theme_text)][variant % 3]
    return skill, title, text, keyword, topic, detail


def make_item(note: dict[str, Any], mode: str, variant: int) -> dict[str, Any]:
    skill, title, text, keyword, topic, detail = base_data(note, variant)
    channel = skill[0]
    number = int(skill[1:]) if skill[1:].isdigit() else 1

    if skill == "G1":
        forms = [
            ("The group records each result before it compares the samples.", ["The group record each result before it compares the samples.", "The group recording each result before compare the samples.", "The group records each result before it comparing the samples."]),
            ("Yesterday, the students moved the activity to the small gym.", ["Yesterday, the students move the activity to the small gym.", "Yesterday, the students are moved the activity to the small gym.", "Yesterday, the students moving the activity to the small gym."]),
            ("Participants should cite the source they use.", ["Participants should cited the source they use.", "Participants should to cite the source they use.", "Participants should cites the source they use."]),
        ]
        correct, wrongs = forms[variant % 3]
        if mode == "error-analysis":
            stem = f"A learner writes, '{wrongs[0]}' in a report about {title}. Which correction is accurate?"
        elif mode == "analysis":
            stem = f"A report about {title} needs a grammatically complete sentence. Which option keeps the time and subject relationship accurate?"
        elif mode == "application":
            stem = f"Choose the sentence that correctly reports one action connected with {title}."
        else:
            stem = "Which sentence has correct subject–verb or tense agreement?"
        return task(note["id"], mode, stem, correct, wrongs, "The correct sentence matches the subject, time marker, and required verb form.")

    if skill == "V1":
        correct = f"a word connected with {topic} in this passage"
        wrongs = ["a command to erase the whole record", "a name for an unrelated musical instrument", "a signal that the event has no purpose"]
        if mode == "error-analysis":
            stem = f"A learner says, 'In this text, {keyword} means an unrelated instrument.' Read: '{text}' Which correction is supported?"
        elif mode == "analysis":
            stem = f"Read: '{text}' How does the context help a reader interpret the word '{keyword}'?"
        elif mode == "application":
            stem = f"Use the passage to choose the contextual meaning of '{keyword}': '{text}'"
        else:
            stem = f"In the passage about {title}, what kind of meaning does '{keyword}' carry?"
        return task(note["id"], mode, stem, correct, wrongs, "The surrounding actions and topic establish the word's contextual meaning.")

    if skill == "P1":
        correct = f"Stress the key action and '{detail}', grouping the remaining words around them."
        wrongs = ["Stress only articles and remove every pause.", "Drop the final sounds of the key words.", "Use the same flat emphasis on every syllable and hide the detail."]
        if mode == "error-analysis":
            stem = f"A learner says, 'I should stress only the word the when reading this detail: {detail}.' Which correction improves pronunciation?"
        elif mode == "analysis":
            stem = f"Two speakers read the key detail '{detail}'. One marks the action and time; the other stresses only function words. Which delivery is clearer?"
            correct = "The speaker who marks the action and time with meaningful stress and phrasing."
        else:
            stem = f"How should a speaker make this information from {title} easy to follow: '{detail}'?"
        return task(note["id"], mode, stem, correct, wrongs, "Meaningful stress, complete sounds, and phrasing make important content easier to understand.")

    if channel in {"L", "R"}:
        medium = "audio transcript" if channel == "L" else "text"
        action = "listen" if channel == "L" else "read"
        if number == 1:
            correct = f"Predict that it may explain {topic}, then {action} to confirm or revise the prediction."
            wrongs = ["Treat the heading as proof of every detail and skip the source.", "Predict an unrelated topic and refuse to revise it.", "Ignore both the heading and the source content."]
            if mode == "error-analysis":
                stem = f"A learner says, 'The title {title} proves every detail, so I do not need to {action}.' Which correction is needed?"
            elif mode == "analysis":
                stem = f"The title is '{title}', but the first sentence adds an unexpected condition. Which prediction strategy handles both pieces of evidence?"
            else:
                stem = f"Before using a {medium} titled '{title}', which preparation is most effective?"
            explanation = "A prediction uses available clues but remains open to confirmation and revision."
        elif number == 2:
            correct = detail
            wrongs = ["The source gives no practical detail.", "Every action happens at midnight in an unnamed place.", "The participants are told to do the opposite of the stated action."]
            if mode == "error-analysis":
                stem = f"A learner says, 'This {medium} gives no usable detail.' Use the source to correct the claim: '{text}'"
            elif mode == "analysis":
                stem = f"Use the {medium} to separate the main topic from a supporting detail: '{text}' Which detail is stated?"
            elif mode == "application":
                stem = f"You need one exact detail from this {medium}: '{text}' What should your note contain?"
            else:
                stem = f"According to this {medium}, which detail is correct? '{text}'"
            explanation = "The answer is explicitly supported by the source and does not add an unstated condition."
        elif number == 3:
            correct = f"The source describes {topic} through connected actions and evidence."
            wrongs = ["The details are unrelated and cannot be classified.", "The source proves that the opposite action is always required.", "One isolated word cancels every other detail."]
            if mode == "error-analysis":
                stem = f"A learner says, 'The details in this {medium} are unrelated.' Which correction follows from the source? '{text}'"
            elif mode == "analysis":
                stem = f"Classify the message and infer its purpose from the linked details: '{text}'"
            else:
                stem = f"What is the most accurate classification of this {medium}? '{text}'"
            explanation = "The classification and inference account for the linked actions without overgeneralising."
        else:
            correct = f"I identified {topic}, verified '{detail}', and will review the section containing '{keyword}' once more."
            wrongs = ["I understood it because the page or recording looked short.", "I kept my first guess even when the source contradicted it.", "I copied one word but did not connect it to meaning."]
            if mode == "error-analysis":
                stem = f"A learner says, 'Reflection means writing that {title} was nice.' Which response is a useful correction?"
            elif mode == "analysis":
                stem = f"Which reflection on the {medium} names evidence, comprehension, and a next step?"
            else:
                stem = f"After you {action} about {title}, which reflection is specific and useful?"
            explanation = "Effective reflection identifies what was understood, cites evidence, and selects a next step."
        return task(note["id"], mode, stem, correct, wrongs, explanation)

    if channel == "S":
        if number == 1:
            correct = f"Plan the purpose, audience, two details about {topic}, and a closing request."
            wrongs = ["List unrelated words without deciding the purpose.", "Plan only the colour of a visual.", "Begin speaking before selecting any relevant information."]
            focus = "planning"
        elif number == 2:
            correct = f"Introduce {topic}, present the details in a logical order, then give the final action."
            wrongs = ["Start with an unexplained ending and hide the topic.", "Repeat one detail randomly and omit the purpose.", "Mix unrelated points without connectors."]
            focus = "organisation"
        elif number == 3:
            correct = f"The {title} information is clear: {detail}."
            wrongs = ["It is that thing somewhere later.", "Maybe stuff happens because there.", "The information detail thing is good." ]
            focus = "clear spoken language"
        elif number == 4:
            correct = f"Could you clarify whether you mean '{detail}'?"
            wrongs = ["I will pretend I understood the unclear detail.", "Your message is wrong because I missed one word.", "Let us ignore the misunderstanding and change topics."]
            focus = "interaction repair"
        elif number == 5:
            correct = f"Record the talk again, slowing down and stressing the phrase '{detail}'."
            wrongs = ["Remove the important detail.", "Speak faster at the unclear section.", "Replace the topic with an unrelated story."]
            focus = "monitoring and improvement"
        else:
            correct = f"My explanation of {topic} was organised, but I rushed the key detail; next time I will mark a pause before it."
            wrongs = ["My talk was perfect because it ended.", "The listeners should repair every missing detail themselves.", "I will change nothing because reflection cannot improve speaking."]
            focus = "speaking reflection"
        if mode == "error-analysis":
            stem = f"A learner says, 'For {title}, {wrongs[0]}' Which correction applies {focus}?"
        elif mode == "analysis":
            stem = f"Two speakers prepare information about {title}. Which option best applies {focus} and preserves the key evidence?"
        elif mode == "application":
            stem = f"You will speak about {title}. Which action best applies {focus}?"
        else:
            stem = f"Which option demonstrates effective {focus} in a talk about {title}?"
        return task(note["id"], mode, stem, correct, wrongs, f"The selected response directly applies {focus} to the stated audience, content, and evidence.")

    if channel == "W":
        if number == 1:
            correct = f"Note the audience, purpose, '{detail}', and the response expected from readers."
            wrongs = ["Plan only decorative colours.", "Collect unrelated song titles.", "Begin a final draft without selecting a purpose or evidence."]
            focus = "writing preparation"
        elif number == 2:
            correct = f"Topic and purpose → evidence about {topic} → final reminder"
            wrongs = ["Unrelated joke → hidden topic → no conclusion", "Final reminder → random detail → repeated title", "Evidence removed → claim repeated without support"]
            focus = "organisation"
        elif number == 3:
            correct = f"The {title} focuses on {topic}. One verified detail is {detail}. Readers should use this information before acting."
            wrongs = [f"{title} is things and stuff.", "It happens because somewhere then.", "A detail exists, but readers need no clear information."]
            focus = "clear drafting"
        elif number == 4:
            correct = f"The report gives the precise detail: {detail}."
            wrongs = ["The report gives a nice thing.", "The result is stuff-like.", "The detail is somewhere and good."]
            focus = "precise vocabulary"
        elif number == 5:
            correct = f"On Friday, the group will present its findings about {topic}."
            wrongs = [f"on friday the group present its findings about {topic}", f"On Friday the group, will presents findings about {topic}.", f"On friday, the groups presents it finding about {topic}." ]
            focus = "grammar and mechanics"
        elif number == 6:
            correct = f"Revise the draft so its sequence, evidence, and statement '{detail}' agree with the source."
            wrongs = ["Keep conflicting details because consistency is optional.", "Delete the source and preserve an unsupported claim.", "Replace every exact detail with vague words."]
            focus = "revision and editing"
        else:
            correct = f"I checked the structure and verified '{detail}'; next time I will ask a peer whether the final request is clear."
            wrongs = ["I finished, so the draft cannot contain an error.", "I changed the font and ignored meaning.", "I did not compare the draft with its plan or source."]
            focus = "writing reflection"
        if mode == "error-analysis":
            stem = f"A learner writes, 'For {title}, {wrongs[0]}' Which correction applies {focus}?"
        elif mode == "analysis":
            stem = f"Which option best preserves the evidence from {title} while applying {focus}? Read: '{text}'"
        elif mode == "application":
            stem = f"You are writing about {title}. Which choice correctly applies {focus}?"
        else:
            stem = f"Which choice demonstrates effective {focus} for a text about {title}?"
        return task(note["id"], mode, stem, correct, wrongs, f"The correct choice applies {focus} while keeping the purpose and source evidence traceable.")

    raise KeyError(note["objectiveId"])


def transform(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace("tr-g06-bank-ingilizce", "tr-g07-bank-ingilizce").replace("g6-ingilizce", "g7-ingilizce")
    if isinstance(value, list):
        return [transform(child) for child in value]
    if isinstance(value, dict):
        return {key: transform(child) for key, child in value.items()}
    return value


def record(local: int, batch: int, item: dict[str, Any], note: dict[str, Any], variant: int) -> dict[str, Any]:
    row = transform(make_record(local, item, note, batch=batch, number_base=(batch - 1) * 100))
    row["grade"] = 7
    row["title"] = f"{note['title']} — Grade 7 original production batch {batch}"
    skill, context_title, context_text, _, _, decisive_detail = base_data(note, variant)
    skill_phrase = str(note["title"]).removeprefix("Students can ")
    row["question"] = (
        f"{row['question']} Source for this item: \"{context_text}\" "
        f"Use the source while focusing on how learners {skill_phrase}."
    )
    explanation = str(item["explanation"]).rstrip(". ") + "."
    explanation += (
        f" In the {context_title} source, the decisive detail is '{decisive_detail}'; "
        f"the {skill} decision keeps that evidence connected to the requested language action."
    )
    row["explanation"] = explanation + " The remaining choices contradict the source, misuse the target skill, or make an unsupported inference."
    reasons = {
        item["correct"]: f"Doğru / correct reasoning: {explanation}",
        item["wrongs"][0]: f"Named misconception — source reversal: '{item['wrongs'][0]}' contradicts or removes the relevant evidence.",
        item["wrongs"][1]: f"Named misconception — skill mismatch: '{item['wrongs'][1]}' does not perform the requested language action.",
        item["wrongs"][2]: f"Named misconception — unsupported inference: '{item['wrongs'][2]}' adds a conclusion the prompt cannot support.",
    }
    row["distractorWhy"] = [reasons[value] for value in row["choices"]]
    row["difficultyReason"] = f"Level {row['level']}; the task applies {note['objectiveId']} to new source evidence and requires three named misconceptions to be distinguished."
    return row


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 400:
        raise RuntimeError(f"batches 05–09 expect 400 records, found {len(existing)}")
    notes = list(read_notes_only(SOURCE).values())
    if len(notes) != 192:
        raise RuntimeError(f"expected 192 English notes, found {len(notes)}")
    assignments = (notes + notes + notes[:116])[:500]
    seen: defaultdict[str, int] = defaultdict(int)
    rows = []
    for offset, note in enumerate(assignments):
        batch = 5 + offset // 100
        local = offset % 100 + 1
        mode = MODES[local - 1]
        variant = seen[note["id"]]
        seen[note["id"]] += 1
        item = make_item(note, mode, variant)
        rows.append(record(local, batch, item, note, variant))
    for batch in range(5, 10):
        batch_rows = rows[(batch - 5) * 100:(batch - 4) * 100]
        if Counter(row["correctIndex"] for row in batch_rows) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
            raise AssertionError(f"batch {batch} answer balance")
        if Counter(row["questionType"] for row in batch_rows) != Counter({"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}):
            raise AssertionError(f"batch {batch} mode balance")
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + rows) + "\n", encoding="utf-8", newline="\n")
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"grade": 7, "batches": "05-09", "questions": 500, "english": 500, "total": 900, "objectives": len(seen), "sourceQuestionReads": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
