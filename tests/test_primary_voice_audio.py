from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))


def load_tool(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


generator = load_tool("generate_primary_voice_audio")
application = load_tool("apply_primary_voice_audio")


def test_primary_voice_rights_and_model_license_are_public_but_reference_is_private() -> None:
    rights = json.loads(
        (ROOT / "voice" / "rights" / "alika-authorized-woman-voice-v1.json").read_text(encoding="utf-8")
    )
    model = json.loads(
        (ROOT / "voice" / "model-licenses" / "voxcpm2.json").read_text(encoding="utf-8")
    )
    assert rights["speakerKind"] == "consented-human-voice-clone"
    assert rights["licenseStatus"] == "voice-owner-authorized-commercial-use"
    assert rights["redistributionReviewStatus"] == "approved-project-owner-attestation"
    assert rights["privacy"]["publishReferenceAudio"] is False
    assert model["license"] == "Apache-2.0"
    assert model["commercialUseApproved"] is True
    tracked = subprocess.check_output(
        ["git", "ls-files", "voice/**/*.wav"], cwd=ROOT, text=True,
    ).strip()
    assert not tracked


def test_primary_voice_seed_and_text_splitting_are_deterministic() -> None:
    assert generator.GENERATOR_VERSION == "alika-primary-voice-generator/1.3.0"
    first = generator.stable_seed("tr.g11.ingilizce.bank.a0807", 20260901)
    assert first == generator.stable_seed("tr.g11.ingilizce.bank.a0807", 20260901)
    assert first != generator.stable_seed("tr.g11.ingilizce.bank.a0808", 20260901)
    chunks = generator.split_text("First sentence. Second sentence is longer.", 24)
    assert " ".join(chunks) == "First sentence. Second sentence is longer."
    assert all(len(chunk) <= 24 for chunk in chunks)
    assert generator.transcript_shard("Same transcript.", 2) == generator.transcript_shard(
        "Same transcript.", 2,
    )
    assert generator.transcript_shard("Same transcript.", 1) == 0


def test_resumed_duplicate_reuse_is_owned_even_when_source_was_already_checkpointed() -> None:
    transcript = "A source checkpoint from an earlier run."
    shard = generator.transcript_shard(transcript, 4)
    assert generator.transcript_owned_by_shard(transcript, 4, shard)
    assert all(
        not generator.transcript_owned_by_shard(transcript, 4, other)
        for other in range(4)
        if other != shard
    )
    assert generator.transcript_owned_by_shard(transcript, 1, 0)


def test_checkpoint_seed_is_bound_to_recorded_retry_attempt() -> None:
    base = 12345
    assert generator.checkpoint_seed_valid({"attempt": 1, "seed": base}, base)
    assert generator.checkpoint_seed_valid({"attempt": 4, "seed": base + 30_000}, base)
    assert not generator.checkpoint_seed_valid({"attempt": 4, "seed": base}, base)
    assert not generator.checkpoint_seed_valid({"attempt": 0, "seed": base - 10_000}, base)


def test_generated_asset_records_consented_voice_and_real_wave_hash(tmp_path: Path) -> None:
    wav_path = tmp_path / "assets" / "audio" / "prompt.wav"
    wav_path.parent.mkdir(parents=True)
    with wave.open(str(wav_path), "wb") as target:
        target.setnchannels(1)
        target.setsampwidth(2)
        target.setframerate(48000)
        target.writeframes(b"\x01\x00" * 4800)
    actual_sha = hashlib.sha256(wav_path.read_bytes()).hexdigest()
    metadata_path = wav_path.with_suffix(".wav.meta.json")
    metadata_path.write_text(json.dumps({
        "generationParameters": {
            "seed": 1, "cfg": 2.0, "inferenceTimesteps": 10,
            "maxChars": 400, "chunkGapMs": 180, "attempt": 1,
        },
    }), encoding="utf-8")
    asset = {
        "assetId": "prompt.one", "path": "assets/audio/prompt.wav",
        "transcript": "A neutral prompt.",
    }
    job = generator.Job(
        ROOT / "turkiye" / "11-sinif" / "soru-bankasi" / "audio-assets.json",
        Path("turkiye/11-sinif/soru-bankasi/audio-assets.json"),
        asset, wav_path, metadata_path,
    )
    updated = generator.updated_asset(asset, job)
    assert updated["sha256"] == actual_sha
    assert updated["sampleRate"] == 48000
    assert updated["speaker"]["voiceProfileId"] == "alika-authorized-woman-voice-v1"
    assert updated["rightsRecordId"] == "tr-authorized-woman-voice-rights-20260901"
    assert updated["referenceAudio"]["sha256"] == generator.REFERENCE_SHA256
    assert updated["referenceAudio"]["packaged"] is False
    assert updated["voiceModel"]["revision"] == generator.MODEL_REVISION
    assert updated["generationMethod"] == "local-voxcpm2-authorized-woman-voice-clone"
    assert updated["licenseStatus"] == "voice-owner-authorized-commercial-use"


def test_audio_migration_stamp_is_hash_bound_and_discloses_self_review() -> None:
    row = {
        "type": "question", "id": "q1", "audio": {"contentSha256": "a" * 64},
        "reviewManifestSha256": "b" * 64,
    }
    stamped = application.stamp(row, "c" * 64, "b" * 64)
    assert stamped["contentHash"] == stamped["reviewedHash"]
    assert stamped["reviewManifestSha256"] == "c" * 64
    assert stamped["reviewAttestation"]["changeScope"] == "audio-asset-and-hash-only"
    assert stamped["humanReviewed"] is False


def test_audio_bundle_names_are_grade_qualified_and_collision_free() -> None:
    grade11 = ROOT / "turkiye" / "11-sinif" / "ingilizce" / "ingilizce-tum.jsonl"
    grade12 = ROOT / "turkiye" / "12-sinif" / "ingilizce" / "ingilizce-tum.jsonl"
    bank11 = (
        ROOT / "turkiye" / "11-sinif" / "soru-bankasi"
        / "11-sinif-tum-dersler-2000-soru.jsonl"
    )
    names = {
        application.bundle_name_for_package(grade11),
        application.bundle_name_for_package(grade12),
        application.bundle_name_for_package(bank11),
    }
    assert len(names) == 3
    assert application.bundle_name_for_package(grade11).startswith("11-sinif-")
    assert application.bundle_name_for_package(grade12).startswith("12-sinif-")
    assert not application.bundle_name_for_package(bank11).startswith("11-sinif-11-sinif-")
