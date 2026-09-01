#!/usr/bin/env python3
"""Atomically apply reviewed primary-voice assets to Türkiye packages."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from build_unique_question_banks import REVIEW_FIELDS, canonical_bytes, read_jsonl
from validate_audio_assets import validate as validate_audio_assets


ROOT = Path(__file__).resolve().parent.parent
PROFILE_ID = "alika-authorized-woman-voice-v1"
RIGHTS_RECORD_ID = "tr-authorized-woman-voice-rights-20260901"
REVIEW_METHOD = "alika-primary-voice-audio-migration-review/1.0.0"
REVIEW_MODEL = "gpt-5.6-sol-codex-self-review"
DECLARATION = "ai-audio-migration-and-codex-self-review-no-human-review"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def digest_value(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def projection(row: dict[str, Any]) -> dict[str, Any]:
    return {key: copy.deepcopy(value) for key, value in row.items() if key not in REVIEW_FIELDS}


def bundle_name_for_package(package: Path) -> str:
    relative = package.resolve().relative_to(ROOT)
    if len(relative.parts) < 3:
        raise ValueError(f"package path lacks country/grade segments: {relative}")
    grade = relative.parts[1]
    stem = package.stem
    qualified_stem = stem if stem.startswith(f"{grade}-") else f"{grade}-{stem}"
    return f"{qualified_stem}-{PROFILE_ID}.alika.zip"


def stamp(row: dict[str, Any], review_sha: str, prior_manifest: str) -> dict[str, Any]:
    clean = projection(row)
    content_sha = digest_value(clean)
    decision_sha = digest_value({
        "recordId": clean.get("id"),
        "contentProjectionSha256": content_sha,
        "audioReviewReportSha256": review_sha,
        "decision": "PASS",
        "reviewerModel": REVIEW_MODEL,
        "method": REVIEW_METHOD,
    })
    clean.update({
        "reviewStatus": "ai-verified",
        "humanReviewed": False,
        "reviewMode": "ai-only",
        "reviewModel": REVIEW_MODEL,
        "reviewDeclaration": DECLARATION,
        "reviewMethodVersion": REVIEW_METHOD,
        "reviewedContentSha256": content_sha,
        "reviewDecisionSha256": decision_sha,
        "reviewManifestSha256": review_sha,
        "contentHash": f"sha256:{content_sha}",
        "reviewedHash": f"sha256:{content_sha}",
        "publishReady": True,
        "publishBlocked": False,
        "productionStatus": "primary-voice-migration-reviewed",
        "disclosure": DECLARATION,
        "provenance": (
            f"primary-voice-review:{decision_sha}; audio-review-report:{review_sha}; "
            f"prior-review-manifest:{prior_manifest or 'none'}; model:{REVIEW_MODEL}; "
            "mode:ai-only; human-review:false"
        ),
        "reviewAttestation": {
            "schema": "alika-primary-voice-record-decision/1.0.0",
            "decision": "PASS",
            "recordId": clean.get("id"),
            "contentProjectionSha256": content_sha,
            "reviewDecisionSha256": decision_sha,
            "reviewManifestSha256": review_sha,
            "reviewMethodVersion": REVIEW_METHOD,
            "model": REVIEW_MODEL,
            "mode": "ai-only",
            "humanReviewed": False,
            "declaration": DECLARATION,
            "changeScope": "audio-asset-and-hash-only",
            "priorReviewManifestSha256": prior_manifest or None,
        },
    })
    return clean


def write_jsonl_atomic(path: Path, rows: list[dict[str, Any]]) -> None:
    temporary = path.with_name(f".{path.name}.primary-voice.tmp")
    temporary.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n",
        encoding="utf-8", newline="\n",
    )
    os.replace(temporary, path)


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_name(f".{path.name}.primary-voice.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    os.replace(temporary, path)


def strict_validate(path: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "pack_validate.py"), "--strict", str(path)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode or "TOPLAM: 0 HATA, 0 UYARI" not in output:
        raise RuntimeError(output[-12000:])
    return "0 HATA / 0 UYARI"


def build_bundle(package: Path, manifest: Path, output: Path) -> dict[str, Any]:
    result = subprocess.run(
        [
            sys.executable, str(ROOT / "tools" / "build_audio_class_bundle.py"),
            "--package", str(package), "--audio-manifest", str(manifest),
            "--output", str(output),
        ],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode:
        raise RuntimeError((result.stdout or "") + (result.stderr or ""))
    payload = json.loads(result.stdout.strip().splitlines()[-1])
    payload["output"] = f"release/{output.name}"
    return payload


def apply_manifest(
    staged_manifest: Path, staging_root: Path, review_sha: str, release_root: Path,
) -> dict[str, Any]:
    relative = staged_manifest.relative_to(staging_root)
    source_manifest = ROOT / relative
    if not source_manifest.is_file():
        raise ValueError(f"source manifest missing: {relative}")
    staged = json.loads(staged_manifest.read_text(encoding="utf-8"))
    assets = staged.get("assets") if isinstance(staged.get("assets"), list) else []
    by_id = {str(asset["assetId"]): asset for asset in assets}
    if len(by_id) != len(assets) or staged.get("assetCount") != len(assets):
        raise ValueError(f"staged manifest invalid: {relative}")
    for asset in assets:
        source_wav = staged_manifest.parent / Path(str(asset["path"]))
        if not source_wav.is_file() or digest(source_wav) != asset.get("sha256"):
            raise ValueError(f"staged WAV invalid: {asset['assetId']}")
    source_manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest_next = source_manifest.with_name(f".{source_manifest.name}.primary-voice.tmp")
    shutil.copy2(staged_manifest, manifest_next)
    os.replace(manifest_next, source_manifest)
    for asset in assets:
        source_wav = staged_manifest.parent / Path(str(asset["path"]))
        target_wav = source_manifest.parent / Path(str(asset["path"]))
        target_wav.parent.mkdir(parents=True, exist_ok=True)
        target_next = target_wav.with_suffix(".wav.next")
        shutil.copy2(source_wav, target_next)
        os.replace(target_next, target_wav)

    package_candidates = []
    for candidate in sorted(source_manifest.parent.glob("*.jsonl")):
        if any(asset_id in candidate.read_text(encoding="utf-8") for asset_id in list(by_id)[:1]):
            package_candidates.append(candidate)
    if len(package_candidates) != 1:
        raise ValueError(f"expected one package beside {relative}, found {package_candidates}")
    package = package_candidates[0]
    rows = read_jsonl(package)
    if not rows or rows[0].get("type") != "pack":
        raise ValueError(f"pack header missing: {package}")
    old_package_sha = digest(package)
    manifest_sha = digest(source_manifest)
    changed_ids: list[str] = []
    for index, row in enumerate(rows):
        changed = False
        if index == 0:
            policy = dict(row.get("audioPolicy") or {})
            policy.update({
                "schemaVersion": "alika-local-audio-policy/1.1.0",
                "manifestPath": "audio-assets.json",
                "manifestSha256": manifest_sha,
                "assetCount": len(assets),
                "questionCount": len(assets),
                "storage": "local-offline-wav",
                "remoteAssetsAllowed": False,
                "voiceProfileId": PROFILE_ID,
                "rightsRecordId": RIGHTS_RECORD_ID,
            })
            row["audioPolicy"] = policy
            changed = True
        audio = row.get("audio") if isinstance(row.get("audio"), dict) else None
        if audio and str(audio.get("assetId") or "") in by_id:
            asset = by_id[str(audio["assetId"])]
            if audio.get("contentSha256") != asset["sha256"]:
                audio["contentSha256"] = asset["sha256"]
                row["audio"] = audio
            changed = True
        if changed:
            prior_manifest = str(row.get("reviewManifestSha256") or "")
            rows[index] = stamp(row, review_sha, prior_manifest)
            changed_ids.append(str(row.get("id") or f"line-{index + 1}"))
    linked = sum(
        1 for row in rows
        if isinstance(row.get("audio"), dict) and row["audio"].get("assetId") in by_id
    )
    if linked != len(assets):
        raise ValueError(f"audio coverage mismatch: {relative}: linked={linked} assets={len(assets)}")
    write_jsonl_atomic(package, rows)
    audio_report = validate_audio_assets(package, source_manifest, allow_runtime_pending=False)
    if audio_report["status"] != "PASS":
        raise ValueError(f"audio validation failed: {audio_report['errors'][:20]}")
    strict = strict_validate(package)
    release_root.mkdir(parents=True, exist_ok=True)
    bundle_name = bundle_name_for_package(package)
    bundle = build_bundle(package, source_manifest, release_root / bundle_name)
    receipts = sorted(source_manifest.parent.glob("*-release-receipt.json"))
    if len(receipts) != 1:
        raise ValueError(f"expected one release receipt beside {relative}, found {receipts}")
    receipt = json.loads(receipts[0].read_text(encoding="utf-8"))
    receipt.update({
        "decision": "PASS",
        "humanReviewed": False,
        "reviewedPackageSha256": digest(package),
        "strictValidation": strict,
        "audioValidation": audio_report,
        "androidClassBundle": bundle,
        "primaryVoiceRelease": {
            "schemaVersion": "alika-primary-voice-release/1.0.0",
            "voiceProfileId": PROFILE_ID,
            "rightsRecordId": RIGHTS_RECORD_ID,
            "audioManifestSha256": manifest_sha,
            "audioReviewReportSha256": review_sha,
            "modelId": "openbmb/VoxCPM2",
            "modelRevision": "32279effe8c19989596f05d353d1447f51d9e915",
            "modelLicense": "Apache-2.0",
            "commercialUseApproved": True,
        },
    })
    write_json_atomic(receipts[0], receipt)
    return {
        "manifest": relative.as_posix(), "package": package.relative_to(ROOT).as_posix(),
        "assets": len(assets), "changedRecords": len(changed_ids),
        "oldPackageSha256": old_package_sha, "newPackageSha256": digest(package),
        "manifestSha256": manifest_sha, "audioValidation": audio_report,
        "strictValidation": strict, "bundle": bundle,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staging-root", type=Path, default=ROOT / "build" / "primary-voice-audio")
    parser.add_argument("--review-report", type=Path, default=ROOT / "reports" / "primary-voice-audio-review.json")
    parser.add_argument("--release-root", type=Path, default=ROOT / "build" / "primary-voice-release")
    parser.add_argument("--manifest", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, default=ROOT / "reports" / "primary-voice-application.json")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    staging_root = args.staging_root.resolve()
    review_report = json.loads(args.review_report.read_text(encoding="utf-8"))
    if review_report.get("status") != "PASS" or review_report.get("voiceProfileId") != PROFILE_ID:
        raise SystemExit("primary-voice review report has not passed")
    manifests = args.manifest or sorted(staging_root.glob("turkiye/**/audio-assets.json"))
    expected_assets = sum(
        int(json.loads(path.read_text(encoding="utf-8")).get("assetCount") or 0)
        for path in manifests
    )
    if review_report.get("assetCount") != expected_assets:
        raise SystemExit("review report does not cover every staged asset")
    review_sha = digest(args.review_report)
    results = [
        apply_manifest(path.resolve(), staging_root, review_sha, args.release_root.resolve())
        for path in manifests
    ]
    expected_bundle_names = {Path(result["bundle"]["output"]).name for result in results}
    for stale in args.release_root.resolve().glob(f"*-{PROFILE_ID}.alika.zip"):
        if stale.name not in expected_bundle_names:
            stale.unlink()
    application = {
        "schemaVersion": "alika-primary-voice-application/1.0.0",
        "status": "PASS",
        "voiceProfileId": PROFILE_ID,
        "reviewReportSha256": review_sha,
        "assetCount": sum(result["assets"] for result in results),
        "packages": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_json_atomic(args.output, application)
    print(json.dumps({
        "status": "PASS", "assets": application["assetCount"],
        "packages": len(results), "report": str(args.output),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
