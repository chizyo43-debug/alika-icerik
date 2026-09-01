from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


EXPECTED = {
    "JP": {
        "release_id": "jp-2026-09-01-safe-scope",
        "packages": 43,
        "questions": 20_460,
        "notes": 949,
        "audio_assets": 160,
        "withheld": 36,
    },
    "KR": {
        "release_id": "kr-2026-09-01-safe-scope",
        "packages": 94,
        "questions": 47_000,
        "notes": 2_162,
        "audio_assets": 135,
        "withheld": 289,
    },
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_frozen_country_releases_are_publishable_hash_bound_and_self_contained() -> None:
    for country, expected in EXPECTED.items():
        current_path = ROOT / "library" / "curriculum" / country / "current-publish-release.json"
        current = load(current_path)
        catalog_path = ROOT / current["catalogPath"]
        audit_path = ROOT / current["auditPath"]
        catalog = load(catalog_path)
        audit = load(audit_path)

        assert current["releaseId"] == expected["release_id"]
        assert current["publishable"] is True
        assert current["releaseBlockers"] == []
        assert digest(catalog_path.read_bytes()) == current["catalogSha256"]
        assert digest(audit_path.read_bytes()) == current["auditSha256"]
        assert catalog["publishable"] is True
        assert catalog["releaseBlockers"] == []
        assert audit["publishable"] is True
        assert audit["status"] == "passed"
        assert audit["errors"] == []
        assert audit["catalogSha256"] == current["catalogSha256"]
        assert catalog["totals"]["packages"] == expected["packages"]
        assert catalog["totals"]["questions"] == expected["questions"]
        assert catalog["totals"]["notes"] == expected["notes"]
        assert catalog["totals"]["audioAssets"] == expected["audio_assets"]
        assert catalog["totals"]["withheldObjectives"] == expected["withheld"]
        assert len(catalog["packages"]) == expected["packages"]

        rights = ROOT / catalog["audioRights"]["rightsRecordPath"]
        assert digest(rights.read_bytes()) == catalog["audioRights"]["rightsRecordSha256"]

        totals = {"questions": 0, "notes": 0, "audio_assets": 0}
        for entry in catalog["packages"]:
            bundle = ROOT / entry["bundlePath"]
            assert bundle.stat().st_size == entry["bundleBytes"]
            assert digest(bundle.read_bytes()) == entry["bundleSha256"]
            assert entry["publicationStatus"] == "publishable-produced-safe-scope"
            assert entry["releaseBlockers"] == []

            with zipfile.ZipFile(bundle) as archive:
                manifest = json.loads(archive.read("MANIFEST.json"))
                assert manifest["publishable"] is True
                assert manifest["releaseId"] == expected["release_id"]
                assert manifest["withheldObjectives"] == entry["withheldObjectives"]
                package = manifest["packages"][0]
                payload = archive.read(package["path"])
                assert digest(payload) == package["sha256"]
                rows = [json.loads(line) for line in payload.decode("utf-8").splitlines()]
                header = rows[0]
                records = rows[1:]
                questions = [row for row in records if row["type"] == "question"]
                notes = [row for row in records if row["type"] == "note"]
                assert header["schemaVersion"] == "2.3"
                assert header["publishable"] is True
                assert len(questions) == entry["counts"]["questions"]
                assert len(notes) == entry["counts"]["notes"]
                assert all(row["reviewStatus"] == "pending" for row in records)
                assert all(row["humanReviewed"] is False for row in records)
                assert all(
                    row.get("visualRequirement") != "required" or isinstance(row.get("figure"), dict)
                    for row in records
                )

                assets = manifest.get("audioAssets") or []
                for asset in assets:
                    assert digest(archive.read(asset["path"])) == asset["sha256"]
                totals["questions"] += len(questions)
                totals["notes"] += len(notes)
                totals["audio_assets"] += len(assets)

        assert totals == {
            "questions": expected["questions"],
            "notes": expected["notes"],
            "audio_assets": expected["audio_assets"],
        }
