#!/usr/bin/env python3
"""Add local audio links to the preserved Grade 11 English lesson questions."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from build_unique_question_banks import ROOT, read_jsonl


PACK = ROOT / "build/grade11-enriched-subjects/ingilizce/ingilizce-tum.jsonl"
MANIFEST = PACK.parent / "audio-assets.json"


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()
    rows = read_jsonl(PACK)
    questions = [row for row in rows if row.get("type") == "question"]
    audio_questions = []
    for position, question in enumerate(questions, 1):
        match = re.search(r"\.([LSP])\d+$", str(question.get("objective") or ""))
        if not match:
            question.pop("mediaRequirement", None)
            question.pop("audio", None)
            question.pop("spokenResponse", None)
            continue
        skill = match.group(1)
        asset_id = f"tr.g11.ingilizce.lesson.a{position:04d}"
        question["mediaRequirement"] = (
            "audio-required" if skill == "L" else "audio-response-required"
        )
        question["audio"] = {
            "assetId": asset_id,
            "role": "prompt" if skill == "L" else "reference",
            "playbackRequired": True,
        }
        if skill != "L":
            question["spokenResponse"] = {
                "mode": "repeat-after-model",
                "recordingRequired": True,
                "referenceAssetId": asset_id,
                "assessmentStatus": "runtime-supported",
            }
        else:
            question.pop("spokenResponse", None)
        audio_questions.append(question)
    if len(audio_questions) != 216:
        raise SystemExit(f"expected 216 L/S/P questions, found {len(audio_questions)}")
    pack = rows[0]
    if args.finalize:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        assets = {
            str(asset.get("assetId") or ""): asset
            for asset in manifest.get("assets") or []
        }
        for question in audio_questions:
            asset_id = question["audio"]["assetId"]
            asset = assets.get(asset_id)
            if asset is None:
                raise SystemExit(f"missing asset {asset_id}")
            question["audio"]["contentSha256"] = asset["sha256"]
        manifest_sha = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
        pack["audioPolicy"] = {
            "schemaVersion": "alika-local-audio-policy/1.0.0",
            "manifestPath": "audio-assets.json",
            "manifestSha256": manifest_sha,
            "assetCount": len(assets),
            "questionCount": len(audio_questions),
            "storage": "local-offline-wav",
            "remoteAssetsAllowed": False,
            "recordingStorage": "local-temporary-only",
        }
    else:
        pack.pop("audioPolicy", None)
    write_rows(PACK, rows)
    print(json.dumps({
        "pack": str(PACK), "audioQuestions": len(audio_questions),
        "finalized": args.finalize,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
