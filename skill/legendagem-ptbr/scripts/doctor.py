#!/usr/bin/env python3
"""Verifica requisitos locais sem ler nem revelar credenciais."""

from __future__ import annotations

import argparse
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
    skill_path = codex_home / "skills" / "legendagem-ptbr"
    version_path = skill_path / "VERSION"
    checks = {
        "system": platform.system(),
        "python": platform.python_version(),
        "python_supported": sys.version_info >= (3, 9),
        "ffmpeg": shutil.which("ffmpeg"),
        "ffprobe": shutil.which("ffprobe"),
        "elevenlabs_key": bool(os.environ.get("ELEVENLABS_API_KEY", "").strip()),
        "skill_installed": (skill_path / "SKILL.md").is_file(),
        "version": version_path.read_text(encoding="utf-8").strip()
        if version_path.is_file()
        else None,
    }
    checks["ready"] = bool(
        checks["python_supported"]
        and checks["ffmpeg"]
        and checks["ffprobe"]
        and checks["elevenlabs_key"]
        and checks["skill_installed"]
    )

    if args.json:
        print(json.dumps(checks, ensure_ascii=False, indent=2))
    else:
        print("Legendagem Profissional PT-BR — diagnóstico")
        print(f"Sistema: {checks['system']} | Python: {checks['python']}")
        print(f"Skill: {'OK' if checks['skill_installed'] else 'AUSENTE'}")
        print(f"Versão: {checks['version'] or 'NÃO IDENTIFICADA'}")
        print(f"FFmpeg: {'OK' if checks['ffmpeg'] else 'AUSENTE'}")
        print(f"FFprobe: {'OK' if checks['ffprobe'] else 'AUSENTE'}")
        print(f"ElevenLabs: {'CONFIGURADA' if checks['elevenlabs_key'] else 'SEM CHAVE'}")
        result = "pronto para usar" if checks["ready"] else "configuração incompleta"
        print(f"Resultado: {result}.")
    return 0 if checks["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
