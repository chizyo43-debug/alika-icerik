#!/usr/bin/env python3
"""Repair Grade 7 notes that fail the two-worked-example release gate."""
from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any

from author_grade7_dkab_batch01 import CASES as DKAB_CASES
from author_grade7_fen_batch03 import CASES as FEN_CASES
from author_grade7_math_batch11 import CASES as MATH_CASES
from author_grade7_math_social_batch13 import SOCIAL_CASES
from author_grade7_english_batches05_09 import CONTEXTS as ENGLISH_CONTEXTS


ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / "turkiye/7-sinif/din-kulturu-ve-ahlak-bilgisi/din-kulturu-ve-ahlak-bilgisi-tum.jsonl",
    ROOT / "turkiye/7-sinif/fen-bilimleri/fen-bilimleri-tum.jsonl",
    ROOT / "turkiye/7-sinif/ingilizce/ingilizce-tum.jsonl",
    ROOT / "turkiye/7-sinif/matematik/matematik-tum.jsonl",
    ROOT / "turkiye/7-sinif/sosyal-bilgiler/sosyal-bilgiler-tum.jsonl",
]
CASE_BY_NOTE = {case[0]: case for case in [*DKAB_CASES, *FEN_CASES, *MATH_CASES, *SOCIAL_CASES]}
SECTION_KEYS = ("whatIWillLearn", "keyConcepts", "priorKnowledge", "steps", "workedExamples", "commonMistakes", "selfCheck", "summary", "figureNote")
REVIEW_FIELDS = {
    "reviewStatus", "aiReviewStatus", "humanReviewed", "reviewMode", "reviewModel",
    "reviewDeclaration", "reviewedContentSha256", "reviewDecisionSha256",
    "reviewManifestSha256", "reviewRubricSha256", "reviewMethodVersion",
    "reviewAttestation", "contentHash", "reviewedHash", "provenance",
    "publishReady", "productionStatus", "disclosure",
}


SKILL_CONCEPTS = {
    "G1": "context clues, subject–verb agreement, time markers, tense choice, modal verbs and a final meaning check",
    "L1": "title and sound clues, prior knowledge, a provisional prediction and confirmation while listening",
    "L2": "listening topic, signal words, speaker purpose, stated detail and concise note-taking",
    "L3": "classification criteria, comparison, linked listening details and evidence-limited inference",
    "L4": "a specific listening success, a comprehension gap, cited evidence and an actionable next strategy",
    "P1": "content-word stress, complete final sounds, meaningful pauses, phrasing and intonation linked to purpose",
    "R1": "heading and layout clues, prior knowledge, a provisional reading prediction and later verification",
    "R2": "skimming for gist, scanning for a key word, close reading for detail and source-based confirmation",
    "R3": "classification criteria, comparison, linked textual clues and an inference that stays within the text",
    "R4": "a named reading strategy, the evidence it revealed, a remaining difficulty and a realistic next step",
    "S1": "audience, purpose, key content, supporting evidence, timing and a planned closing",
    "S2": "opening, logically ordered points, connectors, supporting evidence and a purposeful closing",
    "S3": "complete sentences, precise reference, relevant detail, understandable pace and audience awareness",
    "S4": "turn-taking, clarification, confirmation, polite disagreement and repair of misunderstanding",
    "S5": "recording or feedback evidence, a diagnosed speaking problem and a targeted revision",
    "S6": "a specific strength, evidence of a speaking difficulty and an actionable improvement target",
    "V1": "nearby words, topic, collocation, word family, contextual meaning and dictionary confirmation",
    "W1": "audience, purpose, relevant source evidence, text type, plan and success criteria",
    "W2": "topic sentence, logically grouped details, connectors and a closing related to purpose",
    "W3": "a complete draft with clear reference, source-based detail, coherent order and reader action",
    "W4": "precise nouns and verbs, suitable collocations, avoidance of vague words and context checking",
    "W5": "sentence agreement, tense consistency, capitals, punctuation and a final mechanics check",
    "W6": "content accuracy, organisation, sentence clarity, mechanics and revision against source evidence",
    "W7": "a documented revision, remaining writing need, peer feedback evidence and a next writing goal",
}


def compact(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def mark_pending(row: dict[str, Any]) -> None:
    for field in REVIEW_FIELDS:
        row.pop(field, None)
    row["reviewStatus"] = "pending"
    row["humanReviewed"] = False
    row["publishBlocked"] = True


def unwrap(value: Any) -> Any:
    if isinstance(value, dict) and "content" in value:
        return value["content"]
    return value


def clean_text(value: Any) -> str:
    return " ".join(str(unwrap(value) or "").split())


def case_examples(case: tuple[Any, ...]) -> list[str]:
    _, scenario, evidence, concept, action, inference, wrongs, rationale = case
    first = (
        f"Çözümlü örnek 1 — Durum: {scenario} Kanıt: {evidence} Soru: Bu kayıtlardan hangi sonuç çıkar? "
        f"Çözüm: {inference} Gerekçe: {rationale} Sonuç yalnız verilen koşullarla sınırlı tutulur; "
        "kayıtta bulunmayan kişi, dönem veya koşullara genellenmez."
    )
    second = (
        f"Çözümlü örnek 2 — Hatalı görüş: “{wrongs[0]}” Bu görüş nasıl düzeltilir? Çözüm: {concept} "
        f"Uygulama: {action} Gerekçe: {rationale} Böylece kavram, kanıt ve karar aynı çözüm zincirinde "
        "birleştirilir; karşıt seçeneğin hangi ölçütü dışarıda bıraktığı açıkça gösterilir."
    )
    return [first, second]


def english_examples(note: dict[str, Any]) -> list[str]:
    objective = str(note["objectiveId"])
    _, _, theme_text, skill = objective.split(".")
    contexts = ENGLISH_CONTEXTS[int(theme_text)]
    title1, text1, keyword1, topic1, detail1 = contexts[0]
    title2, text2, keyword2, topic2, detail2 = contexts[1]
    if skill == "G1":
        e1 = f"Worked example 1 — Context: {title1}. Source: '{text1}' Task: choose the grammatically accurate report. Solution: 'The group records the key detail before it presents the result.' The singular group takes records, and the time relationship remains consistent with the source."
        e2 = f"Worked example 2 — Context: {title2}. A learner writes, 'The students is preparing the activity.' Solution: 'The students are preparing the activity.' The plural subject requires are; the correction preserves the current preparation meaning rather than changing the tense."
    elif skill in {"L1", "R1"}:
        medium = "audio" if skill.startswith("L") else "text"
        e1 = f"Worked example 1 — Before using the {medium} titled '{title1}', predict that it may explain {topic1}. Solution: keep the prediction provisional, then use the source '{text1}' to confirm the topic and revise any unsupported detail."
        e2 = f"Worked example 2 — A learner predicts an unrelated weather report from the title '{title2}'. Solution: replace that guess with a prediction about {topic2}, then verify it against '{text2}'. A prediction guides attention but never replaces the source."
    elif skill in {"L2", "R2"}:
        action = "listen for signal words" if skill.startswith("L") else "scan for relevant key words"
        e1 = f"Worked example 1 — Source: '{text1}' Task: find one exact supporting detail. Solution: record '{detail1}'. Use this wording because it is explicitly stated; do not add a time, place or action that the source does not provide."
        e2 = f"Worked example 2 — Source: '{text2}' Strategy: {action}, then check the full sentence. Solution: note '{detail2}'. The nearby words confirm the detail and prevent a familiar but unrelated word from controlling the answer."
    elif skill in {"L3", "R3"}:
        e1 = f"Worked example 1 — Source: '{text1}' Solution: classify it as {topic1} and infer that the actions form one connected plan. The inference uses several linked details and does not claim that the plan applies to every setting."
        e2 = f"Worked example 2 — Compare the evidence in '{text2}'. Solution: identify the shared topic as {topic2}, then state which action or condition differs. Classification names a common criterion; inference explains a supported relationship rather than guessing a hidden fact."
    elif skill in {"L4", "R4", "S6", "W7"}:
        process = {"L4": "listening", "R4": "reading", "S6": "speaking", "W7": "writing"}[skill]
        e1 = f"Worked example 1 — After the {process} task on '{title1}', write: 'I identified {topic1} and verified {detail1}, but I need to check the section containing {keyword1} once more.' This reflection names evidence, a gap and a next action."
        e2 = f"Worked example 2 — Weak reflection: 'It was good.' Improved solution: 'In the {title2} task I used {detail2} accurately, but my explanation of {keyword2} was unclear; next time I will mark and rehearse that point.' The revision is specific and testable."
    elif skill == "P1":
        e1 = f"Worked example 1 — Read the detail '{detail1}'. Solution: stress the main action and the time or place, pronounce final sounds completely, and pause between information groups. This delivery makes the source meaning easier to follow without changing any words."
        e2 = f"Worked example 2 — A learner stresses only articles in '{detail2}'. Solution: shift stress to the content words, group related words and use intonation that matches the sentence purpose. The listener can then distinguish the key information from grammar words."
    elif skill == "V1":
        e1 = f"Worked example 1 — In '{text1}', infer the contextual meaning of '{keyword1}'. Solution: connect it with {topic1} and the nearby actions, propose a meaning, then confirm it in a dictionary. Context narrows meaning; it does not make every guess correct."
        e2 = f"Worked example 2 — In '{text2}', a learner selects an unrelated meaning for '{keyword2}'. Solution: examine its collocation and word family in the sentence, choose the meaning linked with {topic2}, and test whether that meaning keeps the whole sentence coherent."
    elif skill.startswith("S"):
        focus = SKILL_CONCEPTS[skill]
        e1 = f"Worked example 1 — Speaking task: present '{title1}'. Solution: use {focus}. Include the verified point '{detail1}', make its relationship to {topic1} explicit, and close with the action the audience should remember."
        e2 = f"Worked example 2 — A first attempt about '{title2}' is vague and the listener asks what '{keyword2}' refers to. Solution: name the referent, organise the points, request or give clarification when needed, and check that '{detail2}' remains audible and accurate."
    else:
        focus = SKILL_CONCEPTS[skill]
        e1 = f"Worked example 1 — Writing task: create a short text for '{title1}'. Solution: apply {focus}. Use the source detail '{detail1}', organise it for the intended reader, and check that every sentence supports {topic1} rather than adding an unrelated claim."
        e2 = f"Worked example 2 — Draft about '{title2}': one sentence is vague and a key condition is missing. Solution: replace the vague wording with '{keyword2}', restore '{detail2}', revise the order and mechanics, and compare the final text with the source before sharing."
    if min(len(e1), len(e2)) < 120:
        raise AssertionError((note["id"], len(e1), len(e2)))
    return [e1, e2]


def english_sections(note: dict[str, Any]) -> dict[str, Any]:
    objective = str(note["objectiveId"])
    _, _, theme_text, skill = objective.split(".")
    theme_name = ENGLISH_CONTEXTS[int(theme_text)][0][3]
    concepts = SKILL_CONCEPTS[skill]
    examples = english_examples(note)
    action = str(note["title"]).removeprefix("Students can ")
    return {
        "whatIWillLearn": f"You will learn to {action} through age-appropriate sources about {theme_name}. You will identify relevant evidence, apply the target English process and explain how the source supports your response.",
        "keyConcepts": f"Core concepts for {objective}: {concepts}. These concepts are used together; a familiar word or an attractive option cannot replace source meaning, audience, language form or task purpose.",
        "priorKnowledge": "Activate familiar English words and experiences, but keep every prediction provisional. Distinguish a source detail from your own idea, and use English word order, reference and punctuation when you communicate the result.",
        "steps": f"1. Identify the purpose and audience. 2. Preview the source. 3. Locate evidence relevant to {objective}. 4. Apply {concepts}. 5. Compare alternatives. 6. Check meaning and form. 7. Revise after feedback.",
        "workedExamples": examples,
        "commonMistakes": f"Common mistakes include ignoring the source, translating word for word, selecting an option because of one familiar word, confusing prediction with fact, omitting the audience, and failing to check the {skill} result against meaning and form.",
        "selfCheck": [f"Can I apply {objective} to a new source and cite the clue I used?", "Can I explain why one plausible alternative is unsupported?", "Can I revise my response after checking meaning, form, purpose and audience?"],
        "summary": f"Outcome {objective} develops the ability to {action}. A strong response uses source evidence, applies the specific {skill} process, communicates clearly in English and states any limit on the conclusion.",
        "figureNote": "All evidence needed for these examples is supplied in text. A future visual or audio stimulus must be bound to its exact task; no decorative image is used and no caption or alt text may reveal the answer.",
    }


def normalize_non_english(note: dict[str, Any], case: tuple[Any, ...]) -> dict[str, Any]:
    current = note.get("lessonSections") or {}
    result: dict[str, Any] = {}
    for key in SECTION_KEYS:
        value = unwrap(current.get(key)) if isinstance(current, dict) else None
        if key == "workedExamples":
            result[key] = case_examples(case)
        elif key == "selfCheck":
            if isinstance(value, list):
                result[key] = [clean_text(item) for item in value]
            else:
                questions = [part.strip() + "?" for part in re.split(r"\?+", clean_text(value)) if part.strip()]
                result[key] = questions[:5] or [f"{note['title']} kazanımında kullandığım kanıtı açıklayabiliyor muyum?"]
        else:
            result[key] = clean_text(value)
    return result


def render_body(sections: dict[str, Any]) -> str:
    chunks = []
    for key in SECTION_KEYS:
        value = sections[key]
        if isinstance(value, list):
            chunks.append("\n".join(f"- {item}" for item in value))
        else:
            chunks.append(str(value))
    return "\n\n".join(chunks)


def deficient(note: dict[str, Any]) -> bool:
    sections = note.get("lessonSections")
    examples = sections.get("workedExamples") if isinstance(sections, dict) else None
    return not isinstance(examples, list) or len(examples) < 2 or any(len(str(value)) < 120 for value in examples[:2])


def main() -> int:
    summaries = []
    for path in PATHS:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        pack = rows[0]
        changed = 0
        for note in rows:
            if note.get("type") != "note" and note.get("recordType") != "note":
                continue
            if not deficient(note):
                continue
            if note.get("subject") == "İngilizce":
                sections = english_sections(note)
            else:
                case = CASE_BY_NOTE.get(str(note.get("id")))
                if case is None:
                    raise KeyError(f"no authored case for deficient note {note.get('id')}")
                sections = normalize_non_english(note, case)
            note["lessonSections"] = sections
            note["body"] = render_body(sections)
            note["workedExamples"] = [
                {"title": f"Çözümlü örnek {index}", "problem": text.split("Çözüm:", 1)[0].strip(), "solution": (text.split("Çözüm:", 1)[1].strip() if "Çözüm:" in text else text)}
                for index, text in enumerate(sections["workedExamples"], 1)
            ]
            note["selfCheck"] = sections["selfCheck"]
            mark_pending(note)
            changed += 1
        if changed:
            version = pack.get("version", 1)
            pack["version"] = int(version) + 1 if isinstance(version, int) or str(version).isdigit() else "2.0.0"
            mark_pending(pack)
            path.write_text("\n".join(compact(row) for row in rows) + "\n", encoding="utf-8", newline="\n")
        summaries.append({"path": path.relative_to(ROOT).as_posix(), "notesRepaired": changed, "version": pack.get("version")})
    print(compact({"grade": 7, "packages": summaries, "humanReviewed": False, "status": "PENDING_INDEPENDENT_REVIEW"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
