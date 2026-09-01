#!/usr/bin/env python3
"""Generate every Türkiye audio catalog with the consented AliKa woman voice.

Run this script with the dedicated VoxCPM virtual environment.  WAV files and
checkpoints are written below ``build/`` first; source manifests are untouched
until ``apply_primary_voice_audio.py`` is run after QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import re
import shutil
import sys
import time
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
PROFILE_ID = "alika-primary-woman-v1"
RIGHTS_RECORD_ID = "voice-rights-alika-primary-woman-v1"
REFERENCE_SHA256 = "3ead7d03d36780933b0acb326e9a8eaf9ee443ad0a440e9b23ca8cccbdaa093e"
REFERENCE_TEXT = (
    "İsterseniz daha sonra kuralları istediğiniz zaman değiştirebilir, "
    "yeni uygulamalar ekleyebilir veya tatil günleri için özel takvimler "
    "oluşturabilirsiniz. Şimdi sırasıyla kurulumu, kural belirlemeyi ve "
    "günlük kullanım adım adım gösteriyorum."
)
MODEL_ID = "openbmb/VoxCPM2"
MODEL_REVISION = "32279effe8c19989596f05d353d1447f51d9e915"
MODEL_FILE_SHA256 = "f7f964cfa9da23653baec6e6f7750719977ad944ed9f95fe52fe3a620506891d"
GENERATOR_VERSION = "alika-primary-voice-generator/1.3.0"
GENERATED_AT = "2026-09-01T00:00:00+03:00"


@dataclass(frozen=True)
class Job:
    manifest_path: Path
    manifest_relative: Path
    asset: dict[str, Any]
    wav_path: Path
    metadata_path: Path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def text_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_seed(asset_id: str, seed_base: int) -> int:
    value = int(hashlib.sha256(asset_id.encode("utf-8")).hexdigest()[:8], 16)
    return seed_base + value % 1_000_000_000


def transcript_shard(transcript: str, shard_count: int) -> int:
    """Return a stable worker shard; identical transcripts always stay together."""
    return int(text_digest(transcript.strip())[:16], 16) % shard_count


def split_text(text: str, max_chars: int) -> list[str]:
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]
    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        if len(sentence) <= max_chars:
            combined = f"{current} {sentence}".strip()
            if current and len(combined) > max_chars:
                chunks.append(current)
                current = sentence
            else:
                current = combined
            continue
        if current:
            chunks.append(current)
            current = ""
        candidates = [part.strip() for part in re.split(r"(?<=[,;:])\s+", sentence) if part.strip()]
        for candidate in candidates:
            words = candidate.split()
            piece = ""
            for word in words:
                combined = f"{piece} {word}".strip()
                if piece and len(combined) > max_chars:
                    chunks.append(piece)
                    piece = word
                else:
                    piece = combined
            if piece:
                chunks.append(piece)
    if current:
        chunks.append(current)
    return chunks or [text.strip()]


def active_bounds(audio: Any, sample_rate: int) -> tuple[int, int]:
    import numpy as np

    frame = max(1, round(sample_rate * 0.01))
    usable = len(audio) - len(audio) % frame
    if usable <= 0:
        return 0, len(audio)
    frames = audio[:usable].reshape(-1, frame)
    rms = np.sqrt(np.mean(np.square(frames, dtype=np.float64), axis=1))
    threshold = max(0.004, float(np.max(rms)) * 0.055)
    active = np.flatnonzero(rms >= threshold)
    if not len(active):
        return 0, len(audio)
    pad = max(1, round(0.04 * sample_rate / frame))
    return max(0, int(active[0]) - pad) * frame, min(len(frames), int(active[-1]) + 1 + pad) * frame


def basic_audio_qa(audio: Any, sample_rate: int, transcript: str) -> dict[str, Any]:
    import numpy as np

    values = np.asarray(audio, dtype=np.float32).reshape(-1)
    duration = len(values) / sample_rate if sample_rate else 0.0
    peak = float(np.max(np.abs(values))) if len(values) else 0.0
    rms = float(np.sqrt(np.mean(np.square(values, dtype=np.float64)))) if len(values) else 0.0
    minimum = max(1.0, len(transcript) / 32.0)
    maximum = max(8.0, len(transcript) / 3.2)
    checks = {
        "finite": bool(len(values) and np.isfinite(values).all()),
        "sampleRate48k": sample_rate == 48000,
        "peakBelowClipping": 0.02 <= peak < 0.9999,
        "audibleRms": rms >= 0.004,
        "durationPlausible": minimum <= duration <= maximum,
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "durationSeconds": round(duration, 3),
        "peak": round(peak, 6),
        "rms": round(rms, 6),
        "expectedDurationRangeSeconds": [round(minimum, 3), round(maximum, 3)],
    }


def wave_metadata(path: Path) -> dict[str, int | str]:
    with wave.open(str(path), "rb") as source:
        rate = source.getframerate()
        channels = source.getnchannels()
        width = source.getsampwidth() * 8
        frames = source.getnframes()
    return {
        "sha256": digest(path),
        "bytes": path.stat().st_size,
        "durationMs": round(frames * 1000 / rate),
        "sampleRate": rate,
        "channels": channels,
        "sampleWidthBits": width,
    }


def checkpoint_valid(
    job: Job, *, cfg: float = 2.0, steps: int = 10,
    max_chars: int = 400, seed_base: int = 20260901,
) -> bool:
    if not job.wav_path.is_file() or not job.metadata_path.is_file():
        return False
    try:
        metadata = json.loads(job.metadata_path.read_text(encoding="utf-8"))
        actual = wave_metadata(job.wav_path)
    except (OSError, ValueError, json.JSONDecodeError, wave.Error, EOFError):
        return False
    parameters = metadata.get("generationParameters") if isinstance(metadata.get("generationParameters"), dict) else {}
    expected_seed = stable_seed(text_digest(str(job.asset.get("transcript") or "").strip()), seed_base)
    return (
        metadata.get("assetId") == job.asset.get("assetId")
        and metadata.get("transcriptSha256") == text_digest(str(job.asset.get("transcript") or ""))
        and metadata.get("referenceSha256") == REFERENCE_SHA256
        and metadata.get("modelRevision") == MODEL_REVISION
        and metadata.get("generatorVersion") == GENERATOR_VERSION
        and metadata.get("wavSha256") == actual["sha256"]
        and metadata.get("basicQa", {}).get("passed") is True
        and parameters.get("cfg") == cfg
        and parameters.get("inferenceTimesteps") == steps
        and parameters.get("maxChars") == max_chars
        and parameters.get("seed") in {expected_seed, expected_seed + 10_000, expected_seed + 20_000}
    )


def updated_asset(asset: dict[str, Any], job: Job) -> dict[str, Any]:
    metadata = json.loads(job.metadata_path.read_text(encoding="utf-8"))
    actual = wave_metadata(job.wav_path)
    result = dict(asset)
    result.update(actual)
    result.update({
        "mimeType": "audio/wav",
        "language": "en-US",
        "speaker": {
            "kind": "consented-human-voice-clone",
            "voiceProfileId": PROFILE_ID,
            "rightsRecordId": RIGHTS_RECORD_ID,
            "referenceSha256": REFERENCE_SHA256,
        },
        "generationMethod": "local-offline-voxcpm2-ultimate-cloning",
        "generationToolVersion": GENERATOR_VERSION,
        "generationParameters": metadata["generationParameters"],
        "generatedAt": GENERATED_AT,
        "licenseStatus": "voice-owner-authorized-commercial-use",
        "redistributionReviewStatus": "approved-project-owner-attestation",
        "sourceModelId": MODEL_ID,
        "sourceModelRevision": MODEL_REVISION,
        "sourceModelSha256": MODEL_FILE_SHA256,
    })
    result.pop("sourceModelCardSha256", None)
    return result


def build_jobs(manifest_paths: list[Path], staging_root: Path) -> tuple[list[Job], dict[Path, dict[str, Any]]]:
    jobs: list[Job] = []
    manifests: dict[Path, dict[str, Any]] = {}
    seen: set[str] = set()
    for manifest_path in manifest_paths:
        manifest_path = manifest_path.resolve()
        relative = manifest_path.relative_to(ROOT)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assets = manifest.get("assets") if isinstance(manifest.get("assets"), list) else []
        if manifest.get("assetCount") != len(assets):
            raise ValueError(f"{relative}: asset count mismatch")
        manifests[manifest_path] = manifest
        for asset in assets:
            asset_id = str(asset.get("assetId") or "")
            if not asset_id or asset_id in seen:
                raise ValueError(f"duplicate or empty asset id: {asset_id!r}")
            seen.add(asset_id)
            transcript = str(asset.get("transcript") or "").strip()
            if not transcript:
                raise ValueError(f"{asset_id}: transcript missing")
            relative_wav = Path(str(asset.get("path") or ""))
            if relative_wav.is_absolute() or relative_wav.parts[:2] != ("assets", "audio") or ".." in relative_wav.parts:
                raise ValueError(f"{asset_id}: unsafe path")
            wav_path = staging_root / relative.parent / relative_wav
            jobs.append(Job(manifest_path, relative, asset, wav_path, wav_path.with_suffix(".wav.meta.json")))
    return jobs, manifests


def write_staged_manifests(
    manifests: dict[Path, dict[str, Any]], jobs: list[Job], staging_root: Path,
) -> list[Path]:
    by_manifest: dict[Path, list[Job]] = {}
    for job in jobs:
        by_manifest.setdefault(job.manifest_path, []).append(job)
    written: list[Path] = []
    for source, manifest in manifests.items():
        related = by_manifest[source]
        payload = dict(manifest)
        payload.update({
            "schemaVersion": "alika-audio-assets/1.1.0",
            "assetCount": len(related),
            "generationTool": GENERATOR_VERSION,
            "voiceProfileId": PROFILE_ID,
            "rightsRecordId": RIGHTS_RECORD_ID,
            "voiceModel": MODEL_ID,
            "voiceModelRevision": MODEL_REVISION,
            "voiceModelSha256": MODEL_FILE_SHA256,
            "licenseEvidence": {
                "modelUrl": "https://huggingface.co/openbmb/VoxCPM2",
                "repositoryUrl": "https://github.com/OpenBMB/VoxCPM",
                "modelLicense": "Apache-2.0",
                "commercialUseApproved": True,
                "rightsRecordId": RIGHTS_RECORD_ID,
                "redistributionReviewStatus": "approved-project-owner-attestation",
            },
            "assets": [updated_asset(job.asset, job) for job in related],
        })
        target = staging_root / related[0].manifest_relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8", newline="\n",
        )
        written.append(target)
    return written


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, action="append", default=[])
    parser.add_argument("--staging-root", type=Path, default=ROOT / "build" / "primary-voice-audio")
    parser.add_argument("--reference", type=Path, default=ROOT / "voice" / "private" / PROFILE_ID / "prompt.wav")
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--cfg", type=float, default=2.0)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--max-chars", type=int, default=400)
    parser.add_argument("--seed-base", type=int, default=20260901)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if args.shard_count < 1 or not 0 <= args.shard_index < args.shard_count:
        raise SystemExit("shard-index must be in [0, shard-count)")
    manifests = args.manifest or sorted(ROOT.glob("turkiye/**/audio-assets.json"))
    staging_root = args.staging_root.resolve()
    reference = args.reference.resolve()
    if not reference.is_file() or digest(reference) != REFERENCE_SHA256:
        raise SystemExit("Primary voice reference is missing or has the wrong SHA-256")
    jobs, source_manifests = build_jobs(manifests, staging_root)
    incomplete_jobs = [
        job for job in jobs
        if args.force or not checkpoint_valid(
            job, cfg=args.cfg, steps=args.steps, max_chars=args.max_chars,
            seed_base=args.seed_base,
        )
    ]
    valid_by_transcript = {
        str(job.asset["transcript"]).strip(): job for job in jobs
        if not args.force and checkpoint_valid(
            job, cfg=args.cfg, steps=args.steps, max_chars=args.max_chars,
            seed_base=args.seed_base,
        )
    }
    pending = []
    planned_transcripts = set(valid_by_transcript)
    for job in incomplete_jobs:
        transcript = str(job.asset["transcript"]).strip()
        if transcript not in planned_transcripts:
            pending.append(job)
            planned_transcripts.add(transcript)
    all_pending = pending
    pending = [
        job for job in all_pending
        if transcript_shard(str(job.asset["transcript"]), args.shard_count) == args.shard_index
    ]
    if args.limit is not None:
        pending = pending[:args.limit]
    owned_transcripts = {str(job.asset["transcript"]).strip() for job in pending}
    print(json.dumps({
        "phase": "plan", "assets": len(jobs), "pendingGeneration": len(pending),
        "pendingOtherShards": len(all_pending) - len(pending),
        "shard": [args.shard_index, args.shard_count],
        "stagingRoot": str(staging_root),
    }, ensure_ascii=False), flush=True)
    if pending:
        os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
        import numpy as np
        import soundfile as sf
        import torch
        from voxcpm import VoxCPM

        model = VoxCPM.from_pretrained(
            args.model_path,
            load_denoiser=False,
            optimize=True,
            device=args.device,
        )
        sample_rate = int(model.tts_model.sample_rate)
        # Encoding the consented reference is deterministic and expensive. Keep
        # one immutable cache for the whole run instead of re-encoding the same
        # WAV for every asset. VoxCPM's cached path is the same generation path
        # used by ``VoxCPM.generate`` after reference preparation.
        prompt_cache = model.tts_model.build_prompt_cache(
            prompt_text=REFERENCE_TEXT,
            prompt_wav_path=str(reference),
            reference_wav_path=str(reference),
        )
        for index, job in enumerate(pending, start=1):
            transcript = str(job.asset["transcript"]).strip()
            chunks = split_text(transcript, args.max_chars)
            base_seed = stable_seed(text_digest(transcript), args.seed_base)
            started = time.time()
            last_error = ""
            for attempt in range(3):
                try:
                    generated = []
                    for chunk_index, chunk in enumerate(chunks):
                        seed = base_seed + attempt * 10_000 + chunk_index
                        random.seed(seed)
                        np.random.seed(seed % (2**32 - 1))
                        torch.manual_seed(seed)
                        if torch.cuda.is_available():
                            torch.cuda.manual_seed_all(seed)
                        waveform, _, _ = model.tts_model.generate_with_prompt_cache(
                            target_text=chunk,
                            prompt_cache=prompt_cache,
                            min_len=2,
                            max_len=4096,
                            cfg_value=args.cfg,
                            inference_timesteps=args.steps,
                            retry_badcase=True,
                            retry_badcase_max_times=3,
                            retry_badcase_ratio_threshold=6.0,
                        )
                        values = np.asarray(waveform.squeeze(0).cpu(), dtype=np.float32).reshape(-1)
                        start, end = active_bounds(values, sample_rate)
                        generated.append(values[start:end])
                    silence = np.zeros(round(sample_rate * 0.18), dtype=np.float32)
                    combined = generated[0]
                    for waveform in generated[1:]:
                        combined = np.concatenate((combined, silence, waveform))
                    peak = float(np.max(np.abs(combined)))
                    if peak >= 0.98:
                        combined = combined * (0.96 / peak)
                    qa = basic_audio_qa(combined, sample_rate, transcript)
                    if not qa["passed"]:
                        raise ValueError(f"basic QA failed: {qa}")
                    job.wav_path.parent.mkdir(parents=True, exist_ok=True)
                    sf.write(job.wav_path, combined, sample_rate, subtype="PCM_16")
                    actual = wave_metadata(job.wav_path)
                    metadata = {
                        "schemaVersion": "alika-primary-voice-checkpoint/1.0.0",
                        "assetId": job.asset["assetId"],
                        "transcriptSha256": text_digest(transcript),
                        "referenceSha256": REFERENCE_SHA256,
                        "modelId": MODEL_ID,
                        "modelRevision": MODEL_REVISION,
                        "generatorVersion": GENERATOR_VERSION,
                        "wavSha256": actual["sha256"],
                        "generationParameters": {
                            "seed": base_seed + attempt * 10_000,
                            "cfg": args.cfg,
                            "inferenceTimesteps": args.steps,
                            "maxChars": args.max_chars,
                            "chunkGapMs": 180,
                            "attempt": attempt + 1,
                        },
                        "basicQa": qa,
                    }
                    job.metadata_path.write_text(
                        json.dumps(metadata, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                        encoding="utf-8", newline="\n",
                    )
                    print(json.dumps({
                        "phase": "asset", "index": index, "pending": len(pending),
                        "assetId": job.asset["assetId"], "durationMs": actual["durationMs"],
                        "elapsedSeconds": round(time.time() - started, 2), "status": "PASS",
                    }, ensure_ascii=False), flush=True)
                    break
                except Exception as exc:  # checkpointed retry; final failure is fatal
                    last_error = f"{type(exc).__name__}: {exc}"
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
            else:
                raise RuntimeError(f"{job.asset['assetId']}: generation failed after 3 attempts: {last_error}")
    # Exact duplicate transcripts reuse the already generated, hash-bound WAV.
    # Each destination keeps its own checkpoint/asset identity while recording
    # the source asset used for byte-for-byte reuse.
    valid_by_transcript = {
        str(job.asset["transcript"]).strip(): job for job in jobs
        if checkpoint_valid(
            job, cfg=args.cfg, steps=args.steps, max_chars=args.max_chars,
            seed_base=args.seed_base,
        )
    }
    reused = 0
    for job in jobs:
        if checkpoint_valid(
            job, cfg=args.cfg, steps=args.steps, max_chars=args.max_chars,
            seed_base=args.seed_base,
        ):
            continue
        transcript = str(job.asset["transcript"]).strip()
        if transcript not in owned_transcripts:
            continue
        source = valid_by_transcript.get(transcript)
        if source is None:
            continue
        job.wav_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source.wav_path, job.wav_path)
        metadata = json.loads(source.metadata_path.read_text(encoding="utf-8"))
        metadata["assetId"] = job.asset["assetId"]
        metadata["wavSha256"] = digest(job.wav_path)
        metadata["reusedFromAssetId"] = source.asset["assetId"]
        job.metadata_path.write_text(
            json.dumps(metadata, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8", newline="\n",
        )
        if not checkpoint_valid(
            job, cfg=args.cfg, steps=args.steps, max_chars=args.max_chars,
            seed_base=args.seed_base,
        ):
            raise RuntimeError(f"{job.asset['assetId']}: duplicate transcript reuse checkpoint failed")
        reused += 1
    if reused:
        print(json.dumps({"phase": "duplicate-reuse", "assets": reused}, ensure_ascii=False), flush=True)
    incomplete = [
        job.asset["assetId"] for job in jobs
        if not checkpoint_valid(
            job, cfg=args.cfg, steps=args.steps, max_chars=args.max_chars,
            seed_base=args.seed_base,
        )
    ]
    if incomplete:
        print(json.dumps({"phase": "partial", "remaining": len(incomplete), "first": incomplete[:10]}, ensure_ascii=False), flush=True)
        return 2
    written = write_staged_manifests(source_manifests, jobs, staging_root)
    report = {
        "schemaVersion": "alika-primary-voice-generation/1.0.0",
        "status": "PASS",
        "assetCount": len(jobs),
        "manifestCount": len(written),
        "voiceProfileId": PROFILE_ID,
        "rightsRecordId": RIGHTS_RECORD_ID,
        "referenceSha256": REFERENCE_SHA256,
        "modelId": MODEL_ID,
        "modelRevision": MODEL_REVISION,
        "manifests": [path.relative_to(staging_root).as_posix() for path in written],
    }
    report_path = staging_root / "generation-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"phase": "complete", **report, "report": str(report_path)}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
