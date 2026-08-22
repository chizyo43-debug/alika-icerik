from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location(
    "finalize_ai_release_integrity",
    ROOT / "tools" / "finalize_ai_release.py",
)
finalizer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(finalizer)


class ReleaseAttestationIntegrityTests(unittest.TestCase):
    def test_local_script_cannot_fabricate_ai_review(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "apply_ai_review"):
            finalizer.apply_ai_review({"id": "q1"}, "test-producer")

    def test_legacy_finalizer_is_not_a_release_path(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "devre dışıdır"):
            finalizer.finalize_package("test", {})


if __name__ == "__main__":
    unittest.main()
