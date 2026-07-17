from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "tradutor-de-clipes"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class PublicPackageTests(unittest.TestCase):
    def test_skill_contains_exact_entry_rule(self):
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        rules = (SKILL / "references" / "editorial-rules.md").read_text(encoding="utf-8")
        self.assertIn("iniciar exatamente na primeira sílaba", skill)
        self.assertIn("cue.start = primeira_palavra.start", rules)

    def test_elevenlabs_response_is_normalized(self):
        module = load_module(
            "transcribe_elevenlabs",
            SKILL / "scripts" / "transcribe_elevenlabs.py",
        )
        payload = {
            "language_code": "en",
            "text": "Turn around",
            "words": [
                {"type": "word", "text": "Turn", "start": 1.0, "end": 1.4},
                {"type": "spacing", "text": " ", "start": 1.4, "end": 1.5},
                {"type": "word", "text": "around", "start": 1.5, "end": 2.1},
            ],
        }
        result = module.normalize(payload)
        self.assertEqual(result["provider"], "elevenlabs")
        self.assertEqual(result["segments"][0]["start"], 1.0)
        self.assertEqual(len(result["segments"][0]["words"]), 2)

    def test_validator_accepts_valid_fixture(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(SKILL / "scripts" / "validate_srt.py"),
                str(ROOT / "tests" / "fixtures" / "valid.srt"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("sem violações", completed.stdout)


if __name__ == "__main__":
    unittest.main()
