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
            "2026.11.22.1",
        )
        required = [
            "audiovisual-dialogue-rules.md",
            "contextual-translation-workflow.md",
            "dialogue-selective-rules.md",
            "editorial-rules.md",
            "existing-srt-rules.md",
            "resync-rules.md",
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


class ResyncTests(unittest.TestCase):
    def test_uses_reference_times_and_keeps_text(self):
        import tempfile
        ref = ("1\n00:00:10,000 --> 00:00:12,000\nHello there.\n\n"
               "2\n00:00:12,500 --> 00:00:13,000\n(SIGHS)\n\n"
               "3\n00:00:20,000 --> 00:00:21,000\nCome back.\n\n"
               "4\n00:00:21,100 --> 00:00:22,500\nPlease.\n")
        pt = ("1\n00:00:09,200 --> 00:00:11,100\nOlá, você aí.\n\n"
              "2\n00:00:19,200 --> 00:00:21,600\nVolte, por favor.\n")
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "ref.srt").write_text(ref, encoding="utf-8")
            (d / "pt.srt").write_bytes(pt.encode("cp1252"))
            subprocess.run([sys.executable, str(SKILL / "scripts" / "resync_by_reference.py"),
                            str(d / "ref.srt"), str(d / "pt.srt"), str(d / "out.srt")],
                           check=True, capture_output=True)
            out = (d / "out.srt").read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertIn("00:00:10,000 --> 00:00:12,000\nOlá, você aí.", out)
        self.assertIn("00:00:20,000 --> 00:00:22,500\nVolte, por favor.", out)
