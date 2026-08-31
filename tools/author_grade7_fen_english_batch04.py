#!/usr/bin/env python3
"""Append Grade 7 batch 04: 44 Science and 56 English questions.

Only lesson-note records are read.  The lesson-package question collection is
never loaded or used as an authoring source.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

from author_grade6_fen_english_batch10 import make_record
from author_grade6_fen_batch07 import task
from author_grade6_mixed_batch03 import LEVEL_SEQUENCE, make_question, read_notes_only
from author_grade7_dkab_batch01 import LABELS_OUTPUT, OUTPUT
from author_grade7_fen_batch03 import CASES


FEN_SOURCE = Path("turkiye/7-sinif/fen-bilimleri/fen-bilimleri-tum.jsonl")
ENGLISH_SOURCE = Path("turkiye/7-sinif/ingilizce/ingilizce-tum.jsonl")
MODES = ["comprehension"] * 25 + ["application"] * 35 + ["analysis"] * 25 + ["error-analysis"] * 15
ENGLISH_POSITIONS = set(range(1, 15)) | set(range(26, 46)) | set(range(61, 75)) | set(range(86, 94))
FOCI = (
    "calibration record", "controlled comparison", "evidence boundary",
    "repeat measurement", "safe procedure", "model limitation",
)


THEMES = {
    1: {
        "name": "school life and education",
        "event": "the school clubs fair",
        "detail": "The robotics club meets in Lab 2 on Thursday at 15:30, and students must bring a notebook.",
        "words": ("club", "timetable", "laboratory", "project"),
    },
    2: {
        "name": "classroom life and learning",
        "event": "a group science presentation",
        "detail": "First compare the two materials, then record one result, and finally explain it to your group.",
        "words": ("compare", "record", "evidence", "explain"),
    },
    3: {
        "name": "personal life and well-being",
        "event": "a healthy weekday routine",
        "detail": "Maya walks for twenty minutes after school, drinks water with dinner, and turns off her phone at 21:30.",
        "words": ("routine", "exercise", "water", "sleep"),
    },
}


def english_task(note: dict[str, Any], mode: str) -> dict[str, Any]:
    """Create a skill-specific English task for one canonical objective."""
    objective = str(note["objectiveId"])
    parts = objective.split(".")
    theme_no = int(parts[2])
    skill = parts[3]
    theme = THEMES[theme_no]
    name, event, detail = theme["name"], theme["event"], theme["detail"]
    w1, w2, w3, w4 = theme["words"]

    comprehension = {
        "G1": (f"In a notice about {event}, which sentence uses the verb form correctly?",
               f"Students are preparing for {event}.", [f"Students is preparing for {event}.", f"Students preparing for {event} yesterday.", f"Students prepares for {event}."],
               "The plural subject takes 'are', and the present continuous describes the current preparation."),
        "L1": (f"Before listening to an announcement titled '{event.title()}', which prediction is best supported by the title?",
               "The announcement will probably give practical event information.", ["It will certainly explain an unrelated space mission.", "It cannot include a time or place.", "The title proves that the event was cancelled."],
               "A prediction should use the title without inventing unsupported details."),
        "L2": (f"Listen to this transcript: '{detail}' What is one key detail?", detail.split(",")[0].strip() + ".",
               ["The speaker gives no action at all.", "The event takes place only at midnight.", "Every participant must ignore the instructions."],
               "The selected detail is stated directly in the short transcript."),
        "L3": (f"A speaker says: '{detail}' Which label best classifies the message?", f"Information about {name}",
               ["A weather warning with no daily action", "A fictional recipe with no instructions", "A historical date list unrelated to the speaker"],
               "The actions and setting place the message in the stated life theme."),
        "L4": (f"After listening to a message about {event}, which reflection gives useful evidence about comprehension?",
               "I identified the main event and noted the time or action that supported my answer.", ["I understood everything because the recording was short.", "I chose an answer before listening and kept it unchanged.", "I copied one word but did not connect it to the message."],
               "A useful reflection names what was understood and the evidence used."),
        "P1": (f"Which speaking choice makes the important information in '{detail}' easiest to follow?",
               "Stress the key action and pause between separate details.", ["Say every word at the same speed without pausing.", "Whisper the key information and stress only articles.", "Remove the final sounds from the key words."],
               "Meaningful stress and pauses help listeners distinguish the key details."),
        "R1": (f"A text has the heading '{event.title()}: What You Need to Know'. What can a reader reasonably predict?",
               "The text may explain the event and give preparation details.", ["The text must be a novel about an unknown planet.", "The heading shows that no preparation is needed.", "The text can contain only one isolated word."],
               "The heading supports a cautious prediction about purpose and content."),
        "R2": (f"Read: '{detail}' Which reading strategy finds the named action most efficiently?",
               f"Scan for the action word '{w2}' or its related phrase.", ["Read only the punctuation and ignore all words.", "Guess from the text length without reading.", "Search for a word unrelated to the question."],
               "Scanning for a relevant key word locates a specific detail efficiently."),
        "R3": (f"Read: '{detail}' What can be inferred from the sequence of information?",
               "The writer expects the reader to follow more than one connected step or habit.", ["The details have no relationship to one another.", "The writer forbids every activity mentioned.", "Only the final word matters for the meaning."],
               "The ordered details describe connected actions in one context."),
        "R4": (f"Which comment is a specific reflection after reading a text about {event}?",
               f"The heading helped me predict the topic, but I reread the sentence containing '{w3}' to confirm a detail.", ["The text was fine.", "I never checked whether my prediction matched the text.", "I understood it because I liked the page colour."],
               "The response identifies a strategy, a difficulty, and a verification step."),
        "S1": (f"Before giving a short talk about {event}, which plan is most useful?",
               "List the purpose, two key details, and a closing sentence for the audience.", ["Memorise unrelated words in alphabetical order.", "Begin speaking without deciding the topic.", "Plan only the colour of the title card."],
               "A speaking plan connects purpose, content, and audience."),
        "S2": (f"Which order makes a short talk about {event} easiest to follow?",
               "Introduce the event, explain the key details, then close with the required action.", ["Give the closing line first, hide the topic, and omit the action.", "Repeat one detail four times in random places.", "List unrelated words without connectors."],
               "A clear beginning, development, and closing organise spoken ideas."),
        "S3": (f"Which sentence is clearest in a spoken announcement about {event}?",
               f"Please note the time and bring the materials listed for {event}.", ["Things and stuff are somewhere later.", "Maybe it is that one, you know.", "Bring because event when place."],
               "The correct sentence gives a complete, precise instruction."),
        "S4": (f"During a conversation about {event}, you do not hear the meeting time. What should you say?",
               "Could you repeat the meeting time, please?", ["I will pretend I heard it.", "Your information is wrong because I missed it.", "Stop talking; clarification is never useful."],
               "A polite clarification request repairs the communication gap."),
    }

    application = {
        "S5": (f"After recording a talk about {event}, a learner notices that the key time is unclear. What is the best revision?",
               "Record it again, stressing the time and pausing before the required action.", ["Delete the time completely.", "Speak faster so the detail is harder to hear.", "Change the topic to an unrelated event."],
               "Monitoring should lead to a targeted improvement in clarity."),
        "S6": (f"Which speaking reflection about {event} includes both evidence and a next step?",
               "My examples were clear, but I spoke too quickly; next time I will mark two pauses in my notes.", ["My talk was perfect because I finished it.", "The audience should guess every missing detail.", "I will make no change because reflection has no purpose."],
               "The response evaluates a specific feature and sets an actionable improvement."),
        "V1": (f"In the sentence 'Please {w2} your findings before you {w4} them,' which meaning of '{w2}' fits the context?",
               "Write down or store information", ["Erase all evidence", "Celebrate without checking", "Move to a different building"],
               "The surrounding words show that the verb concerns preserving information."),
        "W1": (f"You will write a message about {event}. Which set of planning notes is most relevant?",
               "Audience, purpose, date or sequence, and the action readers should take", ["Only favourite colours", "Three unrelated song titles", "A list with no connection to the event"],
               "Relevant planning notes prepare the content and purpose of the message."),
        "W2": (f"Which outline best organises a paragraph about {event}?",
               "Topic sentence → supporting details → final reminder", ["Final reminder → unrelated joke → no topic", "Four details in random order → hidden purpose", "Title only → repeated title → repeated title"],
               "The selected outline gives the paragraph a logical information flow."),
        "W3": (f"Which draft communicates the details of {event} most clearly?",
               f"Our class is preparing for {event}. Check the schedule, bring the required material, and arrive on time.", [f"{event.title()} maybe things there.", "Bring it when because class.", "There is an event, but the reader needs no useful detail."],
               "The draft uses complete sentences and provides an explicit action."),
        "W4": (f"Choose the most precise word to complete: 'The notice gives a clear ___ for {event}.'",
               "schedule", ["thing", "nice", "somewhere"],
               "'Schedule' precisely names organised time information."),
        "W5": (f"Which sentence is correctly punctuated and capitalised for a message about {event}?",
               f"On Thursday, our class will prepare for {event}.", [f"On Thursday, our class preparing for {event}.", f"On Thursday, will our class prepare for {event}.", f"On Thursday, our classes prepares for {event}."],
               "The sentence begins with a capital, capitalises the day, uses the comma correctly, and ends with a full stop."),
        "W6": (f"Original: 'The group meet on Thursday it presents the project Friday.' Which revision is clearest?",
               "The group meets on Thursday, and it presents the project on Friday.", ["The group meet Thursday project Friday.", "The group meeting, it present Friday.", "Thursday and Friday because group."],
               "The revision fixes agreement, separates the two details, and adds the needed preposition."),
        "W7": (f"After writing about {event}, which reflection is most useful?",
               "I checked the sequence and corrected one missing time expression; next time I will also ask a peer to check clarity.", ["I finished, so the text cannot contain an error.", "I changed the font and ignored the content.", "I did not compare the draft with my plan."],
               "The reflection names a completed revision and a realistic next step."),
        "G1": (f"Complete the classroom report: 'Our team ___ the evidence before it gives an answer.'",
               "checks", ["check", "checking", "are check"],
               "The singular subject 'team' takes 'checks' in this present-tense routine."),
        "L1": (f"You see the audio title 'How Our Group Solved the Task'. What should you do before listening?",
               "Predict that the audio may describe steps and listen to verify the prediction.", ["Assume every detail without listening.", "Ignore the title and choose a random answer.", "Decide that the audio can only list school subjects."],
               "A useful prediction guides attention and remains open to verification."),
        "L2": (f"Audio transcript: '{detail}' Which detail should be written in a listening note?",
               detail.split(",")[1].strip().capitalize() + ".", ["The speaker refuses to give any instruction.", "The task has no sequence.", "The listener must invent an extra final step."],
               "The selected detail is explicitly stated in the middle of the transcript."),
        "L3": (f"Audio A says 'Compare first; then record.' Audio B says 'Record first; then compare.' What is the key difference?",
               "The order of the two actions", ["The number of speakers", "The language of the recordings", "Whether either recording contains an action"],
               "Both recordings contain the same actions but place them in a different order."),
        "L4": (f"A learner missed the final instruction in an audio about {event}. Which response shows effective reflection?",
               "I will replay the final section and note the signal word before the instruction.", ["I will invent an ending instead of listening again.", "I will say the recording has no final instruction.", "I will replay only the title and ignore the difficult section."],
               "The learner identifies the gap and chooses a focused listening strategy."),
        "P1": (f"You are reading the instruction 'Record the result, then explain it.' How should your voice mark the sequence?",
               "Stress 'record' and 'explain' and pause briefly after 'result'.", ["Stress only 'the' and remove the pause.", "Drop the final sounds of both action verbs.", "Use rising intonation on every word without grouping."],
               "Stress and a brief pause make the two steps audible."),
        "R1": (f"Before reading a text called 'Three Ways to Learn Together', which prediction is reasonable?",
               "The text may compare several group-learning strategies.", ["It must report tomorrow's weather.", "It cannot contain more than one idea.", "It certainly tells readers never to work together."],
               "The title supports a prediction about multiple collaborative strategies."),
        "R2": (f"Read: '{detail}' You need to find what happens last. What should you scan for?",
               "The sequence marker 'finally'", ["Only the first capital letter", "A word that does not occur in the text", "The length of the sentence rather than its meaning"],
               "The marker 'finally' signals the last step."),
        "R3": (f"Read two notes. A: 'Compare, record, explain.' B: 'Explain, compare, record.' Which conclusion is supported?",
               "The notes contain the same actions but organise them differently.", ["Only Note A contains action verbs.", "Both notes have exactly the same order.", "Note B contains no learning task."],
               "A comparison preserves the shared actions and identifies the order difference."),
        "R4": (f"Which response reflects on reading a classroom procedure with specific evidence?",
               "The sequence words helped me follow the steps, but I reread the second action to check its object.", ["I liked it because it was on paper.", "I understood every detail before I read it.", "I skipped the steps and judged the text by its length."],
               "The response links comprehension to a reading feature and a verification action."),
    }

    analysis = {
        "S1": (f"Two speaking plans for {event} are compared. Plan A lists purpose, audience and three ordered points. Plan B lists six unrelated words. Which evaluation is supported?",
               "Plan A is more usable because its content and order match the speaking purpose.", ["Plan B is better because unrelated words always improve coherence.", "Both plans are equally complete because they have text.", "Neither plan can guide a speaker under any condition."],
               "A usable plan connects purpose, audience, and ordered content."),
        "S2": (f"A speaker says: (1) final reminder, (2) event purpose, (3) supporting example. Which reordering improves coherence?",
               "Event purpose → supporting example → final reminder", ["Final reminder → final reminder → purpose", "Supporting example → unrelated fact → hidden purpose", "Keep the confusing order because sequence never matters"],
               "Listeners need the topic before its support and closing reminder."),
        "S3": (f"Which version conveys the classroom result without vague reference?",
               "Our group compared the samples and found that Sample B absorbed more water.", ["We did it and that one was more.", "The things made something somehow.", "It was good because this happened there."],
               "The correct version names the action, samples, result, and measured property."),
        "S4": (f"Speaker A says, 'It happens after the second task.' Speaker B is unsure which event 'it' means. Which turn best repairs the exchange?",
               "Do you mean the presentation happens after the second task?", ["I will answer without identifying 'it'.", "Your sentence must be false because I am unsure.", "Let us change the topic and keep the ambiguity."],
               "The repair checks the uncertain referent while preserving the proposed meaning."),
        "S5": (f"A recording is accurate but too fast at the evidence sentence. Which change directly improves comprehensibility?",
               "Slow down at the evidence sentence and add a pause before the conclusion.", ["Remove the evidence sentence.", "Speed up the entire recording.", "Replace the conclusion with an unrelated greeting."],
               "The revision targets the observed delivery problem without losing content."),
        "S6": (f"Feedback says a talk had a clear opening but weak evidence. Which reflection responds to both points?",
               "I will keep the opening and add one measured example before the conclusion.", ["I will remove the clear opening and add no evidence.", "The feedback has two points, so I will ignore both.", "I will change only the slide colour."],
               "The response preserves the strength and addresses the evidence gap."),
        "V1": (f"In 'The results support our claim,' which replacement keeps the meaning of 'support' in this context?",
               "provide evidence for", ["carry physically", "decorate", "remove all doubt without evidence"],
               "Here 'support' describes an evidential relationship, not physical carrying."),
        "W1": (f"A writer plans a classroom report using: purpose, method, result, conclusion. Which missing note would most improve the plan's reliability?",
               "The evidence or observation used for the result", ["The writer's favourite colour", "An unrelated weekend activity", "A decorative word with no link to the report"],
               "A report needs traceable evidence between its method and conclusion."),
        "W2": (f"Paragraph A orders claim→evidence→explanation. Paragraph B orders explanation→unrelated detail→claim and omits evidence. Which judgment is justified?",
               "Paragraph A has the more coherent evidence structure.", ["Paragraph B is stronger because it omits evidence.", "The paragraphs are identical in organisation.", "Organisation cannot affect written clarity."],
               "Claim, relevant evidence, and explanation form a traceable structure."),
        "W3": (f"Which draft best integrates a classroom observation and its interpretation?",
               "The paper towel absorbed 18 mL, whereas the cloth absorbed 11 mL; therefore, the towel absorbed more in this test.", ["The towel is always best everywhere because I like it.", "There were materials and numbers, so something happened.", "The cloth absorbed 11 mL; therefore, no measurement was made."],
               "The draft states comparable data and limits the conclusion to the test."),
        "W4": (f"A report calls a measured difference 'nice'. Which revision is more precise?",
               "The measured difference was 7 millilitres.", ["The difference was very thing-like.", "The result was nice and nice.", "The measurement was somewhere."],
               "The revised wording replaces a vague adjective with the measured quantity."),
        "W5": (f"Which sentence correctly joins a result and a contrast?",
               "Sample A dissolved, but Sample B remained visible.", ["Sample A dissolved but, Sample B was disappear.", "Sample A dissolving, But Sample B stayed.", "Sample A dissolve but Sample B remaining visible."],
               "The sentence uses correct capitals, verb forms, and comma placement before 'but'."),
        "W6": (f"Draft: 'We measured twice. The conclusion says four trials.' Which revision resolves the inconsistency?",
               "Change the conclusion to state two trials, unless two additional trials are actually performed.", ["Keep both numbers because consistency is optional.", "Delete the method and claim four trials anyway.", "Replace both numbers with 'many' to hide the record."],
               "Revision must make the conclusion agree with the documented procedure."),
        "W7": (f"A writer's checklist shows: organisation ✓, evidence ✓, unit labels ✗. Which reflection follows the evidence?",
               "The ideas and evidence are ready, but I must add unit labels before sharing the report.", ["Every feature is complete, including unit labels.", "I should delete the evidence because organisation passed.", "The checklist gives no information for revision."],
               "The reflection preserves completed work and identifies the unchecked requirement."),
    }

    errors = {
        "G1": (f"A learner writes, 'She drink water after exercise.' Which correction is needed?",
               "She drinks water after exercise.", ["She drinking water after exercise.", "She do drinks water after exercise.", "She drinked water after exercise every day."],
               "A third-person singular subject takes the present-tense form 'drinks'."),
        "L1": (f"Before an audio called 'A Better Bedtime Routine', a learner says, 'The title proves every detail, so I do not need to listen.' What is the best correction?",
               "Use the title to predict, then listen to confirm or revise the prediction.", ["Treat the prediction as the complete transcript.", "Ignore both the title and the recording.", "Choose details from an unrelated school event."],
               "Prediction prepares listening but must be checked against the audio."),
        "L2": (f"Audio: '{detail}' A learner reports, 'Maya uses her phone after 23:30.' What is wrong with the report?",
               "It contradicts the stated time and phone action.", ["It repeats every detail accurately.", "The transcript gives no information about a phone.", "A listener may replace stated times with any preferred time."],
               "The transcript says that Maya turns off her phone at 21:30."),
        "L3": (f"A learner classifies '{detail}' as a list of harmful habits. Which correction is supported?",
               "The details mainly describe health-supporting habits.", ["Every detail describes a school punishment.", "The message contains no actions to classify.", "Walking and drinking water are identified as harmful in the transcript."],
               "Walking, drinking water, and limiting late phone use support well-being."),
        "L4": (f"A learner says, 'I missed the exercise duration, but reflection means writing that the audio was good.' Which response improves the reflection?",
               "State the missing detail and replay the relevant section to verify it.", ["Praise the audio without addressing comprehension.", "Invent a duration and avoid replaying.", "Delete every listening note."],
               "Reflection should identify a comprehension gap and a strategy to resolve it."),
        "P1": (f"A learner stresses only the word 'for' in 'Walk for twenty minutes.' Why is this ineffective?",
               "The duration and action carry the key meaning and need clearer stress.", ["Function words must always receive all stress.", "Stress cannot affect listener understanding.", "The action word should be omitted completely."],
               "Content words such as the action and duration convey the essential message."),
        "R1": (f"A learner says, 'The title Three Healthy Evening Habits must describe a school timetable,' and refuses to revise the prediction. What should the learner do?",
               "Use the title to predict health habits and revise any prediction that the text does not support.", ["Keep the unrelated prediction regardless of evidence.", "Skip the text because prediction is always exact.", "Replace the title with an invented one."],
               "Reading predictions are provisional and should respond to title and text evidence."),
        "R2": (f"A learner needs Maya's phone time but scans only for the word 'walks'. Which correction is most efficient?",
               "Scan for 'phone' and the nearby time expression.", ["Count all letters without reading for meaning.", "Search only for exercise words.", "Guess the time from personal habits."],
               "Targeted scanning uses key words related to the requested detail."),
    }

    source = {"comprehension": comprehension, "application": application, "analysis": analysis, "error-analysis": errors}[mode]
    if skill not in source:
        raise KeyError(f"no {mode} English item for {objective}")
    stem, correct, wrongs, explanation = source[skill]
    return task(note["id"], mode, stem, correct, wrongs, explanation)


def derive_science(base: tuple[Any, ...], occurrence: int) -> tuple[Any, ...]:
    note, scenario, evidence, concept, action, inference, wrongs, rationale = base
    focus = FOCI[occurrence % len(FOCI)]
    return (
        note,
        f"A science team opens a new {focus} file. Instead of accepting an earlier label, it investigates this situation: {scenario}",
        f"The team records the following independent evidence: {evidence} It then tags which observation is direct and which statement is an interpretation.",
        f"{concept} In this file, the claim must also remain consistent with the {focus} record.",
        f"{action} The team must document the decision rule before comparing outcomes under the {focus} criterion.",
        f"{inference} This conclusion is limited to the recorded conditions and the {focus} evidence.",
        [
            f"{wrongs[0]} The {focus} file can therefore be ignored.",
            f"{wrongs[1]} A single label is enough even when the new observation conflicts with it.",
            f"{wrongs[2]} Direct observation and interpretation never need to be distinguished.",
        ],
        f"{rationale} The new decision is traceable because the {focus}, observation, and conclusion are connected without extending beyond the measured conditions.",
    )


def replace_grade(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace("tr-g06-bank-fen-b04", "tr-g07-bank-fen-b04").replace("tr.g06.bank.fen.b04", "tr.g07.bank.fen.b04").replace("tr-g06-bank-ingilizce-b04", "tr-g07-bank-ingilizce-b04").replace("g6-ingilizce-b04", "g7-ingilizce-b04")
    if isinstance(value, list):
        return [replace_grade(child) for child in value]
    if isinstance(value, dict):
        return {key: replace_grade(child) for key, child in value.items()}
    return value


def make_english_record(local: int, item: dict[str, Any], note: dict[str, Any]) -> dict[str, Any]:
    row = make_record(local, item, note, batch=4, number_base=300)
    row = replace_grade(row)
    row["grade"] = 7
    row["title"] = f"{note['title']} — Grade 7 original production batch 4"
    explanation = str(item["explanation"]).rstrip(". ") + "."
    row["explanation"] = explanation + " The other choices misuse the evidence, language feature, or requested strategy."
    reason_map = {
        item["correct"]: f"Doğru / correct reasoning: {explanation}",
        item["wrongs"][0]: f"Named misconception — meaning reversal: '{item['wrongs'][0]}' changes or contradicts the intended meaning.",
        item["wrongs"][1]: f"Named misconception — form or strategy mismatch: '{item['wrongs'][1]}' does not apply the target language skill.",
        item["wrongs"][2]: f"Named misconception — unsupported inference: '{item['wrongs'][2]}' is not supported by the prompt evidence.",
    }
    row["distractorWhy"] = [reason_map[value] for value in row["choices"]]
    row["difficultyReason"] = f"Level {row['level']}; the learner must use {note['objectiveId']} in a {item['mode']} task and distinguish three named misconceptions."
    return row


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 300:
        raise RuntimeError(f"batch 04 expects 300 records, found {len(existing)}")
    fen_notes = read_notes_only(FEN_SOURCE)
    english_notes = list(read_notes_only(ENGLISH_SOURCE).values())[:56]
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    science_occurrences: Counter[str] = Counter()
    english_index = 0
    records = []
    for local, mode in enumerate(MODES, 1):
        if local in ENGLISH_POSITIONS:
            note = english_notes[english_index]
            english_index += 1
            item = english_task(note, mode)
            row = make_english_record(local, item, note)
        else:
            base = CASES[(local + science_occurrences.total()) % len(CASES)]
            occurrence = science_occurrences[base[0]]
            science_occurrences[base[0]] += 1
            case = derive_science(base, occurrence)
            note = dict(fen_notes[case[0]])
            note["title"] = f"{note['title']} — {FOCI[occurrence % len(FOCI)]}"
            row = make_question(local, case, mode, LEVEL_SEQUENCE[local - 1], note, labels, "Fen Bilimleri", batch_number=4, number_base=300)
            row = replace_grade(row)
            row["grade"] = 7
            row["title"] = f"{note['title']} — 4. özgün üretim partisi"
        records.append(row)
    if english_index != 56:
        raise AssertionError(english_index)
    if Counter(row["subject"] for row in records) != Counter({"Fen Bilimleri": 44, "İngilizce": 56}):
        raise AssertionError(Counter(row["subject"] for row in records))
    if Counter(row["correctIndex"] for row in records) != Counter({0: 25, 1: 25, 2: 25, 3: 25}):
        raise AssertionError("answer balance")
    if Counter(row["questionType"] for row in records) != Counter({"comprehension": 25, "application": 35, "analysis": 25, "error-analysis": 15}):
        raise AssertionError("mode balance")
    labels = {replace_grade(key): replace_grade(value) for key, value in labels.items()}
    OUTPUT.write_text("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in existing + records) + "\n", encoding="utf-8", newline="\n")
    LABELS_OUTPUT.write_text(json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"grade": 7, "batch": 4, "questions": 100, "science": 44, "english": 56, "total": 400, "figures": sum(bool(row.get("figure")) for row in records), "sourceQuestionReads": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
