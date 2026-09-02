from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POINTER = ROOT / "library/registry/current-question-bank-release.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_independent_subject_question_bank_release_is_hash_bound_and_complete() -> None:
    pointer = json.loads(POINTER.read_text(encoding="utf-8"))
    catalog_path = ROOT / pointer["catalogPath"]
    audit_path = ROOT / pointer["auditPath"]
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))

    assert pointer["publishable"] is True
    assert pointer["releaseBlockers"] == []
    assert pointer["catalogSha256"] == sha256_file(catalog_path)
    assert pointer["auditSha256"] == sha256_file(audit_path)
    assert audit["status"] == "passed" and audit["errors"] == []
    assert audit["catalogSha256"] == pointer["catalogSha256"]
    assert catalog["publishable"] is True
    assert catalog["humanReviewed"] is False
    assert catalog["totals"] == {
        "packages": 137,
        "questions": 274000,
        "notes": 3151,
        "audioAssets": 940,
    }

    packages = catalog["packages"]
    japanese = [row for row in packages if row["country"] == "JP"]
    korean = [row for row in packages if row["country"] == "KR"]
    assert len(japanese) == 43
    assert len(korean) == 94
    assert {row["grade"] for row in japanese} == set(range(5, 13))
    assert {row["grade"] for row in korean} == {*range(5, 11), "11-12"}
    assert len({(row["country"], row["grade"], row["subjectCode"]) for row in packages}) == 137
    assert sum(row["counts"]["questions"] for row in japanese) == 86000
    assert sum(row["counts"]["questions"] for row in korean) == 188000
    assert sum(row["counts"]["audioAssets"] for row in japanese) == 640
    assert sum(row["counts"]["audioAssets"] for row in korean) == 300
    assert {row["grade"] for row in japanese if row["subjectCode"] == "eigo"} == set(range(5, 13))
    expected_audio = {
        **{f"jp-g{grade:02d}-eigo": 80 for grade in range(5, 13)},
        **{f"kr-g{grade:02d}-yeongeo": 60 for grade in range(5, 10)},
    }
    assert all(
        row["counts"]["audioAssets"] == expected_audio.get(row["cellId"], 0)
        for row in packages
    )
    for row in packages:
        bundle = ROOT / row["bundlePath"]
        assert bundle.is_file()
        assert bundle.stat().st_size == row["bundleBytes"]
        assert sha256_file(bundle) == row["bundleSha256"]
        assert row["publicationStatus"] == "publishable-independent-subject-question-bank"
        assert row["counts"]["questions"] == 2000
        assert row["counts"]["families"] == 400
        assert row["counts"]["notes"] == 23
        assert row["sourceQuestionReuse"] == "forbidden"
        assert row["questionsUsedAsSemanticInputs"] == 0

        with zipfile.ZipFile(bundle) as archive:
            manifest = json.loads(archive.read("MANIFEST.json"))
            assert manifest["schema"] == "alika-question-bank-bundle/v1"
            assert manifest["publishable"] is True
            assert manifest["productType"] == "independent-question-bank"
            assert manifest["recordReviewStatus"] == "pending"
            assert manifest["humanReviewed"] is False
            package = manifest["packages"][0]
            payload = archive.read(package["path"])
            assert hashlib.sha256(payload).hexdigest() == package["sha256"]
            rows = [json.loads(line) for line in payload.decode("utf-8").splitlines() if line]
            header = rows[0]
            notes = [item for item in rows[1:] if item.get("type") == "note"]
            questions = [item for item in rows[1:] if item.get("type") == "question"]
            assert header["type"] == "pack" and header["schemaVersion"] == "2.3"
            assert header["productType"] == "independent-question-bank"
            assert header["contractPolicy"]["questionCount"] == 2000
            assert header["contractPolicy"]["minFamilies"] == 400
            assert header["contractPolicy"]["maxPerFamily"] == 5
            assert header["generationPolicy"]["sourceQuestionReuse"] == "forbidden"
            assert header["generationPolicy"]["questionsUsedAsSemanticInputs"] == 0
            assert header["publishReady"] is True and header["publishBlocked"] is False
            assert len(notes) == 23 and len(questions) == 2000
            assert all(item["reviewStatus"] == "pending" for item in [*notes, *questions])
            assert all(item["humanReviewed"] is False for item in [*notes, *questions])
            assert len({item["id"] for item in questions}) == 2000
            assert [sum(item["correct"] == index for item in questions) for index in range(4)] == [500] * 4

            audio_assets = manifest.get("audioAssets") or []
            expected_audio_count = expected_audio.get(row["cellId"], 0)
            assert len(audio_assets) == expected_audio_count
            for asset in audio_assets:
                data = archive.read(asset["path"])
                assert len(data) == asset["bytes"]
                assert hashlib.sha256(data).hexdigest() == asset["sha256"]
