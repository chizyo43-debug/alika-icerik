#!/usr/bin/env python3
"""Validate AliKa local WAV manifests and question-to-audio links."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
import wave
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from build_unique_question_banks import ROOT, read_jsonl


def normalized(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).casefold()
    text = re.sub(r"[^\w]+", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid_sha256(value: Any) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{64}", str(value or "")))


def validate_speaker_provenance(asset_id: str, asset: dict[str, Any]) -> list[str]:
    """Accept legacy synthetic voices and the consented AliKa voice contract."""
    errors: list[str] = []
    speaker = asset.get("speaker")
    if isinstance(speaker, str):
        if not speaker.startswith("synthetic-"):
            errors.append(f"{asset_id}: speaker-provenance-missing")
        return errors
    if not isinstance(speaker, dict):
        return [f"{asset_id}: speaker-provenance-missing"]
    if speaker.get("kind") != "consented-human-voice-clone":
        errors.append(f"{asset_id}: speaker-kind-invalid")
    for field in ("voiceProfileId", "rightsRecordId"):
        if not str(speaker.get(field) or "").strip():
            errors.append(f"{asset_id}: speaker-{field}-missing")
    if not valid_sha256(speaker.get("referenceSha256")):
        errors.append(f"{asset_id}: speaker-reference-hash-invalid")
    if asset.get("licenseStatus") != "voice-owner-authorized-commercial-use":
        errors.append(f"{asset_id}: voice-owner-license-missing")
    if asset.get("redistributionReviewStatus") != "approved-project-owner-attestation":
        errors.append(f"{asset_id}: audio-license-review-pending")
    rights_record_id = str(asset.get("rightsRecordId") or "").strip()
    if not rights_record_id or rights_record_id != speaker.get("rightsRecordId"):
        errors.append(f"{asset_id}: rights-record-binding-invalid")
    reference = asset.get("referenceAudio")
    if not isinstance(reference, dict):
        errors.append(f"{asset_id}: reference-audio-evidence-missing")
    else:
        if reference.get("sha256") != speaker.get("referenceSha256"):
            errors.append(f"{asset_id}: reference-audio-hash-mismatch")
        if reference.get("packaged") is not False:
            errors.append(f"{asset_id}: private-reference-packaging-invalid")
    voice_model = asset.get("voiceModel")
    if not isinstance(voice_model, dict):
        errors.append(f"{asset_id}: voice-model-evidence-missing")
    else:
        for field in ("modelId", "revision", "modelFileSha256", "license"):
            if not str(voice_model.get(field) or "").strip():
                errors.append(f"{asset_id}: voice-model-{field}-missing")
        if not valid_sha256(voice_model.get("modelFileSha256")):
            errors.append(f"{asset_id}: voice-model-hash-invalid")
    return errors


def validate(
    questions_path: Path, manifest_path: Path, allow_runtime_pending: bool = False,
) -> dict[str, Any]:
    errors: list[str] = []
    questions = [row for row in read_jsonl(questions_path) if row.get("type") == "question"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assets = manifest.get("assets") if isinstance(manifest.get("assets"), list) else []
    by_id: dict[str, dict[str, Any]] = {}
    for asset in assets:
        asset_id = str(asset.get("assetId") or "")
        if not asset_id or asset_id in by_id:
            errors.append(f"{asset_id or '<empty>'}: duplicate-or-empty-asset-id")
            continue
        by_id[asset_id] = asset
    links: Counter[str] = Counter()
    asset_families: defaultdict[str, set[str]] = defaultdict(set)
    requirements: Counter[str] = Counter()
    for question in questions:
        qid = str(question.get("id") or "")
        requirement = str(question.get("mediaRequirement") or "none")
        requirements[requirement] += 1
        if not requirement.startswith("audio"):
            if question.get("audio") or question.get("spokenResponse"):
                errors.append(f"{qid}: unexpected-audio-payload")
            continue
        audio = question.get("audio") if isinstance(question.get("audio"), dict) else {}
        asset_id = str(audio.get("assetId") or "")
        if asset_id not in by_id:
            errors.append(f"{qid}: audio-reference-unresolved:{asset_id}")
            continue
        links[asset_id] += 1
        asset_families[asset_id].add(str(question.get("familyId") or qid))
        if audio.get("role") not in {"prompt", "reference"} or audio.get("playbackRequired") is not True:
            errors.append(f"{qid}: invalid-audio-link")
        if audio.get("contentSha256") != by_id[asset_id].get("sha256"):
            errors.append(f"{qid}: audio-content-hash-mismatch")
        response = question.get("spokenResponse")
        if requirement == "audio-response-required":
            if not isinstance(response, dict):
                errors.append(f"{qid}: spoken-response-missing")
            else:
                if response.get("mode") != "repeat-after-model" or response.get("recordingRequired") is not True:
                    errors.append(f"{qid}: spoken-response-contract")
                if response.get("referenceAssetId") != asset_id:
                    errors.append(f"{qid}: spoken-response-reference")
                status = response.get("assessmentStatus")
                if status != "runtime-supported" and not (allow_runtime_pending and status == "runtime-integration-pending"):
                    errors.append(f"{qid}: spoken-response-runtime-missing")
        elif response is not None:
            errors.append(f"{qid}: unexpected-spoken-response")
        transcript = normalized(by_id[asset_id].get("transcript"))
        correct = normalized(question.get("correctOption"))
        if not transcript:
            errors.append(f"{qid}: transcript-missing")
        if correct and (correct in transcript or transcript in correct or SequenceMatcher(None, correct, transcript, autojunk=False).ratio() > 0.88):
            errors.append(f"{qid}: audio-answer-leak")
        for choice in question.get("choices") or []:
            if normalized(choice) == transcript:
                errors.append(f"{qid}: audio-choice-transcript-leak")
    for asset_id, families in asset_families.items():
        if len(families) > 1:
            errors.append(
                f"{asset_id}: audio-asset-reused-across-question-families:{len(families)}"
            )
    if set(links) != set(by_id):
        errors.append(f"audio-coverage-mismatch:linked={len(links)}:assets={len(by_id)}")

    package_root = manifest_path.parent.resolve()
    valid_files = 0
    duration_ms = 0
    byte_count = 0
    for asset_id, asset in by_id.items():
        relative = Path(str(asset.get("path") or ""))
        if relative.is_absolute() or relative.parts[:2] != ("assets", "audio") or ".." in relative.parts:
            errors.append(f"{asset_id}: unsafe-audio-path")
            continue
        path = (package_root / relative).resolve()
        try:
            path.relative_to(package_root)
        except ValueError:
            errors.append(f"{asset_id}: audio-path-escape")
            continue
        if not path.is_file():
            errors.append(f"{asset_id}: audio-file-missing")
            continue
        try:
            with wave.open(str(path), "rb") as wav_file:
                rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                width = wav_file.getsampwidth() * 8
                frames = wav_file.getnframes()
        except (wave.Error, EOFError):
            errors.append(f"{asset_id}: invalid-wave")
            continue
        actual = {
            "sha256": sha256(path), "bytes": path.stat().st_size,
            "durationMs": round(frames * 1000 / rate), "sampleRate": rate,
            "channels": channels, "sampleWidthBits": width,
        }
        for field, value in actual.items():
            if asset.get(field) != value:
                errors.append(f"{asset_id}: audio-metadata-mismatch:{field}")
        if asset.get("mimeType") != "audio/wav" or asset.get("language") != "en-US":
            errors.append(f"{asset_id}: audio-format-language")
        errors.extend(validate_speaker_provenance(asset_id, asset))
        if (
            isinstance(asset.get("speaker"), str)
            and asset.get("redistributionReviewStatus") != "approved"
        ):
            errors.append(f"{asset_id}: audio-license-review-pending")
        valid_files += 1
        duration_ms += actual["durationMs"]
        byte_count += actual["bytes"]
    if manifest.get("assetCount") != len(by_id):
        errors.append("audio-manifest-count")
    return {
        "status": "PASS" if not errors else "FAIL",
        "questions": len(questions),
        "requirements": dict(sorted(requirements.items())),
        "assets": len(by_id),
        "validFiles": valid_files,
        "bytes": byte_count,
        "durationMs": duration_ms,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--allow-runtime-pending", action="store_true")
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    report = validate(args.questions, args.manifest, args.allow_runtime_pending)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
