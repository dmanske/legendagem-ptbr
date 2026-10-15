from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "legendagem-ptbr"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class PublicPackageTests(unittest.TestCase):
    def test_package_contains_current_complete_skill(self):
        self.assertEqual(
            (SKILL / "VERSION").read_text(encoding="utf-8").strip(),
            "2026.10.15.2",
        )
        required = [
            "audiovisual-dialogue-rules.md",
            "contextual-translation-workflow.md",
            "dialogue-selective-rules.md",
            "editorial-rules.md",
            "existing-srt-rules.md",
            "music-clean-rules.md",
            "source-verification-rules.md",
        ]
        for filename in required:
            self.assertTrue((SKILL / "references" / filename).is_file(), filename)
        self.assertFalse((SKILL / "scripts" / "transcribe_clip.py").exists())

    def test_skill_contains_entry_and_exit_rules(self):
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        metadata = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("name: legendagem-ptbr", skill)
        self.assertIn("$legendagem-ptbr", metadata)
        self.assertIn("cue.start = primeira_silaba_audivel", skill)
        self.assertIn("correção exclusiva de saída", skill)
        self.assertIn("piano, reverb ou acompanhamento", readme)
        self.assertIn("meta de 15 CPS", skill)
        self.assertNotIn("alternativa local com Faster-Whisper", skill)

    def test_scribe_request_fields(self):
        module = load_module(
            "transcribe_scribe_v2",
            SKILL / "scripts" / "transcribe_scribe_v2.py",
        )
        fields = module.request_fields("en", False, None)
        self.assertEqual(fields["model_id"], "scribe_v2")
        self.assertEqual(fields["timestamps_granularity"], "word")
        self.assertEqual(fields["language_code"], "en")
        self.assertEqual(fields["diarize"], "false")

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
