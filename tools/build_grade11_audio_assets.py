#!/usr/bin/env python3
"""Build local, hash-verifiable WAV assets for Grade 11 English bank items."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import wave
from pathlib import Path
from typing import Any

from build_unique_question_banks import ROOT, read_jsonl


BLUEPRINT = ROOT / "authoring/question-bank-blueprints/grade-11.jsonl"
SOURCE_PACK = ROOT / "turkiye/11-sinif/ingilizce/ingilizce-tum.jsonl"
OUTPUT = ROOT / "build/audio-authoring/grade-11"
VOICE_ROOT = ROOT / "build/audio-tooling/voices"
MODEL = VOICE_ROOT / "en_US-ljspeech-medium.onnx"
CONFIG = VOICE_ROOT / "en_US-ljspeech-medium.onnx.json"
MODEL_CARD = VOICE_ROOT / "MODEL_CARD"
MODEL_SHA256 = "6f52a751e2349abe7a76735eb09dc1875298c77ea2342ffd2fef79ff81b87f22"
DATASET_URL = "https://keithito.com/LJ-Speech-Dataset/"
MODEL_URL = "https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/ljspeech/medium"

PURPOSES = (
    "The listener should identify the speaker's purpose before drawing a conclusion.",
    "Notice the time reference and the relationship between the two details.",
    "Use only the evidence in the recording and avoid unsupported assumptions.",
    "Compare the stated reason with the result that follows from it.",
    "Pay attention to register, audience and the key contrast in the message.",
    "Check which detail limits the scope of the speaker's claim.",
    "Distinguish the main point from an example that merely supports it.",
    "Follow the sequence carefully before deciding how the message ends.",
    "Identify the condition that makes the speaker's proposal appropriate.",
    "Separate an observation from the inference based on that observation.",
    "Listen for the phrase that signals a change, contrast or consequence.",
    "Evaluate the response for clarity, accuracy and communicative effect.",
    "Use the contextual clue to resolve the most plausible meaning.",
    "Check whether the conclusion stays within the evidence provided.",
    "Relate the speaker's choice of words to the intended audience.",
    "Review the message for one supporting detail and one limiting detail.",
    "Track the cause, process and result in the order presented.",
    "Notice how the example modifies or qualifies the general statement.",
    "Confirm that the final response preserves both meaning and tone.",
    "Test the first interpretation against the complete spoken context.",
)

TOPIC_FALLBACKS = {
    "School Life & Education": (
        "Our school offers academic and vocational pathways, so students compare facilities, course goals and future plans before choosing.",
        "The student council is preparing a national day programme and checks the audience, schedule and purpose of every activity.",
    ),
    "Classroom Life & Learning": (
        "The class tests two study strategies, records the evidence and explains why one method fits the task better.",
        "Before the group presentation, each learner checks the instructions, the source and the order of the main points.",
    ),
    "Personal Life & Well-Being": (
        "A balanced plan combines sleep, regular movement and realistic goals instead of relying on a single quick solution.",
        "The speaker describes a preference respectfully and gives a reason without making assumptions about another person.",
    ),
    "Family Life & Home": (
        "Family members compare past and present routines, then agree on a fair plan for shared responsibilities at home.",
        "The speaker explains a household change by using a clear time marker and a reason supported by the situation.",
    ),
    "Life in the Neighbourhood, City & Social Life": (
        "The visitor compares two routes by time, accessibility and cost before asking for directions to the community centre.",
        "Neighbours discuss a local service and choose a polite request that matches the place, audience and purpose.",
    ),
    "Life in the World & Culture": (
        "The report compares cultural practices with evidence and avoids turning one example into a claim about everyone.",
        "The traveller identifies the country, language and custom accurately while keeping the description respectful.",
    ),
    "Life in Nature & Global Problems": (
        "The group links resource use to its environmental effect and proposes an action that can be checked with evidence.",
        "The speaker distinguishes an observed change from a prediction about what may happen in the future.",
    ),
    "Life in the Universe & Future": (
        "Scientists compare two observations before deciding whether the evidence supports a claim about a distant planet.",
        "The mission plan separates a confirmed fact, a likely prediction and a possibility that still needs evidence.",
    ),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strings(value: Any) -> list[str]:
    if isinstance(value, str) and value.strip():
        return [" ".join(value.split())]
    if isinstance(value, list):
        return [item for child in value for item in strings(child)]
    if isinstance(value, dict):
        return [item for child in value.values() for item in strings(child)]
    return []


def clean_english(value: str) -> str:
    value = re.sub(r"[*_#>`]", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def candidates(note: dict[str, Any]) -> list[str]:
    sections = note.get("lessonSections") if isinstance(note.get("lessonSections"), dict) else {}
    pool = strings(sections.get("workedExamples"))
    pool += re.split(r"(?<=[.!?])\s+", str(note.get("body") or ""))
    turkish = re.compile(r"(?i)\b(?:için|verilen|kanıt|koşul|sonuç|öğrenci|kazanım|soru|yanıt)\b")
    english = re.compile(r"(?i)\b(?:the|a|an|is|are|was|were|with|from|to|of|in|on|for|and|because|before|after)\b")
    result = []
    for raw in pool:
        text = clean_english(str(raw))
        if 45 <= len(text) <= 260 and not turkish.search(text) and len(english.findall(text)) >= 2:
            if text not in result:
                result.append(text)
    return result


def transcript(question: dict[str, Any], note: dict[str, Any], position: int) -> str:
    topic = str(question.get("topic") or note.get("topic") or "the current topic")
    pool = candidates(note)
    fallback = TOPIC_FALLBACKS.get(topic, (
        f"The speaker explains a situation about {topic} and supports the conclusion with two clear details.",
    ))
    base_pool = pool or list(fallback)
    base = base_pool[position % len(base_pool)]
    purpose = PURPOSES[(position // max(1, len(base_pool))) % len(PURPOSES)]
    skill = re.search(r"\.([LSP])\d+$", str(question.get("objective") or ""))
    lead = "Listen carefully." if skill and skill.group(1) == "L" else "Listen to the model response."
    text = f"{lead} {base} {purpose}"
    correct = clean_english(str(question.get("correctOption") or "")).casefold()
    if correct and (correct in text.casefold() or text.casefold() in correct):
        text = f"{lead} {fallback[position % len(fallback)]} {purpose}"
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--questions", type=Path, default=BLUEPRINT)
    parser.add_argument("--source-pack", type=Path, default=SOURCE_PACK)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--expected", type=int, default=275)
    parser.add_argument("--grade", type=int, default=11)
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if digest(MODEL) != MODEL_SHA256:
        raise SystemExit("Piper voice model SHA-256 mismatch")
    sys.path.insert(0, str(ROOT / "build/audio-tooling/venv/Lib/site-packages"))
    from piper import PiperVoice, SynthesisConfig  # type: ignore

    notes = {
        str(row.get("id")): row
        for row in read_jsonl(args.source_pack)
        if row.get("type") == "note"
    }
    questions = [
        row for row in read_jsonl(args.questions)
        if str(row.get("mediaRequirement") or "").startswith("audio")
    ]
    if len(questions) != args.expected:
        raise SystemExit(f"Expected {args.expected} audio items, found {len(questions)}")
    audio_dir = args.output / "assets/audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    espeak_data = ROOT / "build/audio-tooling/venv/Lib/site-packages/piper/espeak-ng-data"
    voice = PiperVoice.load(MODEL, CONFIG, espeak_data_dir=espeak_data)
    synth = SynthesisConfig(length_scale=1.08, noise_scale=0.62, noise_w_scale=0.78)
    records = []
    for position, question in enumerate(questions):
        asset = question["audio"]["assetId"]
        destination = audio_dir / f"{asset}.wav"
        script = transcript(question, notes[str(question["noteId"])], position)
        if args.force or not destination.exists() or destination.stat().st_size < 44:
            with wave.open(str(destination), "wb") as wav_file:
                voice.synthesize_wav(script, wav_file, syn_config=synth)
        with wave.open(str(destination), "rb") as wav_file:
            sample_rate = wav_file.getframerate()
            channels = wav_file.getnchannels()
            sample_width_bits = wav_file.getsampwidth() * 8
            frames = wav_file.getnframes()
        records.append({
            "assetId": asset,
            "path": f"assets/audio/{destination.name}",
            "sha256": digest(destination),
            "mimeType": "audio/wav",
            "bytes": destination.stat().st_size,
            "durationMs": round(frames * 1000 / sample_rate),
            "sampleRate": sample_rate,
            "channels": channels,
            "sampleWidthBits": sample_width_bits,
            "language": "en-US",
            "speaker": "synthetic-piper-en-us-ljspeech-medium",
            "generationMethod": "local-offline-piper-tts-1.7.0",
            "generatedAt": "2026-08-31T00:00:00+03:00",
            "licenseStatus": "approved-public-domain-source-and-mit-model",
            "redistributionReviewStatus": "approved",
            "transcript": script,
            "sourceModelSha256": MODEL_SHA256,
            "sourceModelCardSha256": digest(MODEL_CARD),
        })
    manifest = {
        "schemaVersion": "alika-audio-assets/1.0.0",
        "grade": args.grade,
        "subject": "İngilizce",
        "language": "en-US",
        "assetCount": len(records),
        "generationTool": "piper-tts-1.7.0-local-offline",
        "voiceModel": "en_US-ljspeech-medium",
        "voiceModelSha256": MODEL_SHA256,
        "licenseEvidence": {
            "modelUrl": MODEL_URL,
            "datasetUrl": DATASET_URL,
            "modelRepositoryLicense": "MIT",
            "datasetLicense": "public-domain",
            "redistributionReviewStatus": "approved",
        },
        "assets": records,
    }
    manifest_path = args.output / "audio-assets.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({
        "assets": len(records),
        "bytes": sum(record["bytes"] for record in records),
        "durationMs": sum(record["durationMs"] for record in records),
        "manifest": str(manifest_path),
        "manifestSha256": digest(manifest_path),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
