import hashlib
import copy
import json
from pathlib import Path

from tools.build_unique_question_banks import REVIEW_FIELDS, canonical_bytes


ROOT = Path(__file__).resolve().parents[1]
TARGETS = (
    ROOT / "turkiye/5-sinif/sosyal-bilgiler/sosyal-bilgiler-tum.jsonl",
    ROOT / "turkiye/6-sinif/fen-bilimleri/fen-bilimleri-tum.jsonl",
    ROOT / "turkiye/6-sinif/sosyal-bilgiler/sosyal-bilgiler-tum.jsonl",
)


def projection(row):
    return {key: copy.deepcopy(value) for key, value in row.items() if key not in REVIEW_FIELDS}


def digest(row):
    return hashlib.sha256(canonical_bytes(row)).hexdigest()


def test_three_previously_blocked_subject_packs_are_hash_bound_and_ready():
    for path in TARGETS:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
        pack = rows[0]
        assert pack["publishReady"] is True
        assert pack["publishBlocked"] is False
        assert pack["reviewStatus"] == "ai-verified"
        assert pack["humanReviewed"] is False
        assert pack["reviewDeclaration"] == "ai-generated-and-codex-self-reviewed-no-human-review"
        assert len([row for row in rows if row.get("type") == "question"]) == 500
        manifest_path = ROOT / "reports/tr-pending-subject-reviews" / f"{pack['id']}.json"
        manifest_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["decision"] == "PASS"
        assert manifest["knownErrors"] == manifest["knownWarnings"] == 0
        decisions = {row["recordId"]: row for row in manifest["records"]}
        for row in rows:
            assert row["reviewManifestSha256"] == manifest_sha
            assert row["reviewedContentSha256"] == digest(projection(row))
            assert decisions[row["id"]]["contentProjectionSha256"] == digest(projection(row))
        receipt_path = path.with_name(path.stem.replace("-tum", "-release-receipt") + ".json")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        assert receipt["decision"] == "PASS"
        assert receipt["humanReviewed"] is False
        assert receipt["reviewedPackageSha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
