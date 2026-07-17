#!/usr/bin/env python3
"""Check the local requirements used by the music subtitle skill."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import shutil
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    checks = {
        "system": platform.system(),
        "python": platform.python_version(),
        "python_supported": sys.version_info >= (3, 9),
        "ffmpeg": shutil.which("ffmpeg"),
        "ffprobe": shutil.which("ffprobe"),
        "elevenlabs_key": bool(os.environ.get("ELEVENLABS_API_KEY", "").strip()),
        "faster_whisper": importlib.util.find_spec("faster_whisper") is not None,
        "skill_installed": (codex_home / "skills" / "tradutor-de-clipes" / "SKILL.md").is_file(),
    }
    ready_remote = checks["python_supported"] and checks["ffmpeg"] and checks["elevenlabs_key"]
    ready_local = checks["python_supported"] and checks["ffmpeg"] and checks["faster_whisper"]
    checks["ready_with_elevenlabs"] = bool(ready_remote)
    checks["ready_with_local_whisper"] = bool(ready_local)

    if args.json:
        print(json.dumps(checks, ensure_ascii=False, indent=2))
    else:
        print("Tradutor de Clipes — diagnóstico")
        print(f"Sistema: {checks['system']} | Python: {checks['python']}")
        print(f"Skill global: {'OK' if checks['skill_installed'] else 'AUSENTE'}")
        print(f"FFmpeg: {'OK' if checks['ffmpeg'] else 'AUSENTE'}")
        print(f"FFprobe: {'OK' if checks['ffprobe'] else 'AUSENTE'}")
        print(f"ElevenLabs: {'CONFIGURADA' if checks['elevenlabs_key'] else 'SEM CHAVE'}")
        print(f"faster-whisper local: {'OK' if checks['faster_whisper'] else 'OPCIONAL/AUSENTE'}")
        if ready_remote:
            print("Resultado: pronto para usar ElevenLabs Scribe v2.")
        elif ready_local:
            print("Resultado: pronto para transcrição local.")
        else:
            print("Resultado: consulte docs/INSTALLATION.md para concluir a configuração.")
    return 0 if checks["skill_installed"] and (ready_remote or ready_local) else 1


if __name__ == "__main__":
    raise SystemExit(main())
