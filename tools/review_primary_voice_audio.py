#!/usr/bin/env python3
"""Codex QA for staged AliKa primary-voice WAV assets."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import wave
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
PROFILE_ID = "alika-authorized-woman-voice-v1"
REFERENCE_SHA256 = "3ead7d03d36780933b0acb326e9a8eaf9ee443ad0a440e9b23ca8cccbdaa093e"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def normalized(text: str) -> str:
    return " ".join(re.sub(r"[^\w]+", " ", text.casefold(), flags=re.UNICODE).split())


def longest_quiet_seconds(audio: Any, sample_rate: int) -> float:
    import numpy as np

    frame = max(1, round(sample_rate * 0.01))
    usable = len(audio) - len(audio) % frame
    if usable <= 0:
        return 0.0
    frames = audio[:usable].reshape(-1, frame)
    rms = np.sqrt(np.mean(np.square(frames, dtype=np.float64), axis=1))
    quiet = rms < max(0.003, float(np.max(rms)) * 0.025)
    longest = current = 0
    for value in quiet:
        current = current + 1 if value else 0
        longest = max(longest, current)
    return longest * frame / sample_rate


def waveform_review(path: Path, asset: dict[str, Any]) -> dict[str, Any]:
    import soundfile as sf
    import numpy as np

    errors: list[str] = []
    try:
        with wave.open(str(path), "rb") as source:
            rate = source.getframerate()
            channels = source.getnchannels()
            width = source.getsampwidth() * 8
            frames = source.getnframes()
    except (wave.Error, EOFError, OSError) as exc:
        return {"status": "FAIL", "errors": [f"invalid-wave:{exc}"]}
    audio, read_rate = sf.read(path, dtype="float32", always_2d=False)
    if getattr(audio, "ndim", 1) > 1:
        audio = np.mean(audio, axis=1)
    peak = float(np.max(np.abs(audio))) if len(audio) else 0.0
    rms = float(np.sqrt(np.mean(np.square(audio, dtype=np.float64)))) if len(audio) else 0.0
    quiet = longest_quiet_seconds(audio, rate)
    actual = {
        "sha256": digest(path), "bytes": path.stat().st_size,
        "durationMs": round(frames * 1000 / rate), "sampleRate": rate,
        "channels": channels, "sampleWidthBits": width,
    }
    for field, value in actual.items():
        if asset.get(field) != value:
            errors.append(f"metadata:{field}")
    if read_rate != 48000 or rate != 48000 or channels != 1 or width != 16:
        errors.append("format")
    if not len(audio) or not np.isfinite(audio).all() or rms < 0.004:
        errors.append("silent-or-invalid")
    if peak >= 0.9999 or peak < 0.02:
        errors.append("peak")
    if quiet > 0.9:
        errors.append("long-silence")
    speaker = asset.get("speaker") if isinstance(asset.get("speaker"), dict) else {}
    if (
        speaker.get("kind") != "consented-human-voice-clone"
        or speaker.get("voiceProfileId") != PROFILE_ID
        or speaker.get("referenceSha256") != REFERENCE_SHA256
    ):
        errors.append("speaker-contract")
    return {
        "status": "PASS" if not errors else "FAIL", "errors": errors,
        "durationMs": actual["durationMs"], "peak": round(peak, 6),
        "rms": round(rms, 6), "longestQuietSeconds": round(quiet, 3),
    }


def discover_assets(staging_root: Path, manifests: list[Path]) -> list[tuple[Path, dict[str, Any], Path]]:
    records: list[tuple[Path, dict[str, Any], Path]] = []
    seen: set[str] = set()
    for manifest_path in manifests:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        assets = payload.get("assets") if isinstance(payload.get("assets"), list) else []
        if payload.get("assetCount") != len(assets):
            raise ValueError(f"{manifest_path}: asset count mismatch")
        for asset in assets:
            asset_id = str(asset.get("assetId") or "")
            if not asset_id or asset_id in seen:
                raise ValueError(f"duplicate or empty asset id: {asset_id!r}")
            seen.add(asset_id)
            path = manifest_path.parent / Path(str(asset.get("path") or ""))
            records.append((manifest_path.relative_to(staging_root), asset, path))
    return records


def run_asr(records: list[tuple[Path, dict[str, Any], Path]], checkpoint: Path, batch_size: int) -> dict[str, dict[str, Any]]:
    import librosa
    import torch
    from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

    completed: dict[str, dict[str, Any]] = {}
    if checkpoint.is_file():
        for line in checkpoint.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            completed[row["assetId"]] = row
    current = {
        str(asset["assetId"]): {
            "wavSha256": str(asset["sha256"]),
            "transcriptSha256": hashlib.sha256(str(asset["transcript"]).encode("utf-8")).hexdigest(),
        }
        for _, asset, _ in records
    }
    completed = {
        asset_id: row for asset_id, row in completed.items()
        if asset_id in current
        and row.get("wavSha256") == current[asset_id]["wavSha256"]
        and row.get("transcriptSha256") == current[asset_id]["transcriptSha256"]
    }
    pending = [record for record in records if str(record[1]["assetId"]) not in completed]
    if not pending:
        return completed
    model_id = "openai/whisper-large-v3-turbo"
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    device = "cuda" if torch.cuda.is_available() else "cpu"
    processor = AutoProcessor.from_pretrained(model_id)
    recognizer = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, dtype=dtype, low_cpu_mem_usage=True, use_safetensors=True,
    )
    recognizer.to(device)
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    for offset in range(0, len(pending), batch_size):
        batch = pending[offset:offset + batch_size]
        arrays = []
        for _, _, path in batch:
            audio, _ = librosa.load(path, sr=16000, mono=True)
            arrays.append(audio)
        inputs = processor(
            arrays, sampling_rate=16000, return_tensors="pt", padding=True,
        )
        input_features = inputs.input_features.to(device=device, dtype=dtype)
        attention_mask = getattr(inputs, "attention_mask", None)
        if attention_mask is not None:
            attention_mask = attention_mask.to(device)
        with torch.inference_mode():
            token_ids = recognizer.generate(
                input_features,
                attention_mask=attention_mask,
                language="english",
                task="transcribe",
            )
        outputs = processor.batch_decode(token_ids, skip_special_tokens=True)
        with checkpoint.open("a", encoding="utf-8", newline="\n") as stream:
            for (_, asset, _), recognized_text in zip(batch, outputs):
                expected = normalized(str(asset["transcript"]))
                recognized = normalized(str(recognized_text or ""))
                similarity = SequenceMatcher(None, expected, recognized, autojunk=False).ratio()
                row = {
                    "assetId": asset["assetId"],
                    "wavSha256": asset["sha256"],
                    "transcriptSha256": hashlib.sha256(str(asset["transcript"]).encode("utf-8")).hexdigest(),
                    "recognized": str(recognized_text or "").strip(),
                    "normalizedCharacterSimilarity": round(similarity, 6),
                    "status": "PASS" if similarity >= 0.9 else "FAIL",
                }
                completed[row["assetId"]] = row
                stream.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
                print(json.dumps({"phase": "asr", **row}, ensure_ascii=False), flush=True)
    return completed


def run_speaker_sample(
    records: list[tuple[Path, dict[str, Any], Path]], reference: Path, sample_size: int,
) -> list[dict[str, Any]]:
    import librosa
    import numpy as np
    import torch
    from speechbrain.inference.speaker import EncoderClassifier
    from speechbrain.utils.fetching import LocalStrategy

    if digest(reference) != REFERENCE_SHA256:
        raise ValueError("speaker reference hash mismatch")
    selected = [records[round(index * (len(records) - 1) / max(1, sample_size - 1))] for index in range(min(sample_size, len(records)))]
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_dir = Path.home() / ".cache" / "alika-models" / "spkrec-ecapa-voxceleb"
    classifier = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb", savedir=str(model_dir),
        run_opts={"device": device}, local_strategy=LocalStrategy.COPY,
    )

    def embedding(path: Path) -> Any:
        audio = librosa.load(path, sr=16000, mono=True)[0]
        tensor = torch.from_numpy(audio).float().unsqueeze(0).to(device)
        with torch.inference_mode():
            return classifier.encode_batch(tensor, normalize=True).squeeze().detach().cpu().numpy()

    reference_embedding = embedding(reference)
    results = []
    for _, asset, path in selected:
        value = embedding(path)
        similarity = float(np.dot(value, reference_embedding) / (np.linalg.norm(value) * np.linalg.norm(reference_embedding)))
        results.append({
            "assetId": asset["assetId"], "similarityToPrivateReference": round(similarity, 6),
            "status": "PASS" if similarity >= 0.6 else "FAIL",
        })
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staging-root", type=Path, default=ROOT / "build" / "primary-voice-audio")
    parser.add_argument("--manifest", type=Path, action="append", default=[])
    parser.add_argument("--reference", type=Path, default=ROOT / "voice" / "private" / PROFILE_ID / "prompt.wav")
    parser.add_argument("--without-asr", action="store_true")
    parser.add_argument("--without-speaker-sample", action="store_true")
    parser.add_argument("--speaker-sample-size", type=int, default=24)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--output", type=Path, default=ROOT / "reports" / "primary-voice-audio-review.json")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    staging_root = args.staging_root.resolve()
    manifests = args.manifest or sorted(staging_root.glob("turkiye/**/audio-assets.json"))
    records = discover_assets(staging_root, manifests)
    waveform_results = []
    for manifest, asset, path in records:
        result = waveform_review(path, asset)
        waveform_results.append({"manifest": manifest.as_posix(), "assetId": asset["assetId"], **result})
    asr = {} if args.without_asr else run_asr(records, staging_root / "asr-checkpoint.jsonl", args.batch_size)
    speaker = [] if args.without_speaker_sample else run_speaker_sample(records, args.reference.resolve(), args.speaker_sample_size)
    failures = [row for row in waveform_results if row["status"] != "PASS"]
    failures.extend({"assetId": key, "errors": ["asr"]} for key, row in asr.items() if row["status"] != "PASS")
    failures.extend({"assetId": row["assetId"], "errors": ["speaker-similarity"]} for row in speaker if row["status"] != "PASS")
    report = {
        "schemaVersion": "alika-primary-voice-codex-review/1.0.0",
        "status": "PASS" if not failures and len(records) > 0 else "FAIL",
        "reviewer": "gpt-5.6-sol-codex-self-review",
        "humanReviewed": False,
        "voiceProfileId": PROFILE_ID,
        "referenceSha256": REFERENCE_SHA256,
        "assetCount": len(records),
        "manifestCount": len(manifests),
        "waveformPassed": sum(row["status"] == "PASS" for row in waveform_results),
        "asrPassed": sum(row["status"] == "PASS" for row in asr.values()),
        "asrMinimumSimilarity": min((row["normalizedCharacterSimilarity"] for row in asr.values()), default=None),
        "speakerSamplePassed": sum(row["status"] == "PASS" for row in speaker),
        "speakerSampleMinimumSimilarity": min((row["similarityToPrivateReference"] for row in speaker), default=None),
        "failures": failures,
        "asrResults": [asr[key] for key in sorted(asr)],
        "speakerSample": speaker,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: report[key] for key in report if key not in {"asrResults", "speakerSample", "failures"}}, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
