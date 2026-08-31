#!/usr/bin/env python3
"""Build an Android-installable v2 class bundle with local WAV assets."""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--audio-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    package = args.package.resolve()
    audio_manifest_path = args.audio_manifest.resolve()
    audio_manifest = json.loads(audio_manifest_path.read_text(encoding="utf-8"))
    assets = audio_manifest.get("assets") if isinstance(audio_manifest.get("assets"), list) else []
    if int(audio_manifest.get("assetCount") or -1) != len(assets):
        raise SystemExit("audio manifest count mismatch")
    package_member = f"packages/{package.name}"
    declared_assets = []
    paths: list[tuple[Path, str]] = []
    for asset in assets:
        relative = PurePosixPath(str(asset.get("path") or ""))
        if relative.parts[:2] != ("assets", "audio") or ".." in relative.parts:
            raise SystemExit(f"unsafe asset path: {relative}")
        source = audio_manifest_path.parent / Path(*relative.parts)
        if not source.is_file() or digest(source) != asset.get("sha256"):
            raise SystemExit(f"asset hash mismatch: {relative}")
        declared_assets.append({
            "assetId": asset["assetId"],
            "path": relative.as_posix(),
            "sha256": asset["sha256"],
            "bytes": source.stat().st_size,
            "mimeType": "audio/wav",
        })
        paths.append((source, relative.as_posix()))
    pack_header = json.loads(package.read_text(encoding="utf-8").splitlines()[0])
    manifest = {
        "schema": "alika-class-bundle/v2",
        "id": f"{pack_header.get('id', package.stem)}.audio-bundle",
        "country": pack_header.get("country", "TR"),
        "grade": pack_header.get("grade"),
        "lang": pack_header.get("lang", "tr"),
        "packages": [{
            "path": package_member,
            "sha256": digest(package),
            "bytes": package.stat().st_size,
        }],
        "audioManifestSha256": digest(audio_manifest_path),
        "audioAssets": declared_assets,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        archive.writestr(
            "MANIFEST.json",
            json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        )
        archive.write(package, package_member)
        for source, member in paths:
            archive.write(source, member)
    print(json.dumps({
        "output": str(args.output), "sha256": digest(args.output),
        "bytes": args.output.stat().st_size, "audioAssets": len(declared_assets),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
