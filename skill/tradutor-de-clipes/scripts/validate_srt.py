#!/usr/bin/env python3
"""Validate structural and readability constraints of an SRT file."""

import argparse
import re
from pathlib import Path


TIMESTAMP = re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})$")
HTML_TAG = re.compile(r"<[^>]+>")
SDH_BRACKET = re.compile(r"\[[^\]]+\]")
SDH_PARENTHETICAL_LINE = re.compile(r"^\s*\([^()]+\)\s*$")
SDH_SPEAKER_LABEL = re.compile(
    r"^\s*[A-ZÀ-ÖØ-Ý][A-ZÀ-ÖØ-Ý0-9 .'-]{1,30}:\s*"
)
MUSIC_SYMBOL = re.compile(r"[♪♫♬]")
SDH_STYLE_TAG = re.compile(r"<\s*font\b|\{\\[^}]+\}", re.IGNORECASE)


def read_subtitle(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ("utf-8-sig", "cp1252", "iso-8859-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"não foi possível identificar a codificação de {path.name}")


def seconds(value: str) -> float:
    match = TIMESTAMP.match(value)
    if not match:
        raise ValueError(f"invalid timestamp: {value}")
    hours, minutes, secs, millis = map(int, match.groups())
    return hours * 3600 + minutes * 60 + secs + millis / 1000


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("srt")
    parser.add_argument("--max-lines", type=int, default=2)
    parser.add_argument("--max-cpl", type=int, default=42)
    parser.add_argument("--target-cps", type=float, default=15.0)
    parser.add_argument("--max-cps", type=float, default=17.0)
    parser.add_argument("--preferred-max-duration", type=float, default=4.7)
    parser.add_argument("--max-duration", type=float, default=7.5)
    parser.add_argument(
        "--allow-long-cue",
        type=int,
        action="append",
        default=[],
        help="ID de cue vocal indivisível autorizado a ultrapassar --max-duration",
    )
    args = parser.parse_args()

    content = read_subtitle(Path(args.srt)).strip()
    blocks = re.split(r"\n\s*\n", content) if content else []
    errors = []
    warnings = []
    previous_end = -1.0

    for expected, block in enumerate(blocks, 1):
        lines = block.splitlines()
        if len(lines) < 3:
            errors.append(f"cue {expected}: bloco incompleto")
            continue
        try:
            cue_id = int(lines[0])
            start_text, end_text = lines[1].split(" --> ")
            start, end = seconds(start_text), seconds(end_text)
        except (ValueError, TypeError) as exc:
            errors.append(f"cue {expected}: {exc}")
            continue

        text_lines = lines[2:]
        duration = end - start
        visible_lines = [HTML_TAG.sub("", line) for line in text_lines]
        text = " ".join(visible_lines)
        cps = len(text) / duration if duration > 0 else float("inf")

        if cue_id != expected:
            errors.append(f"cue {expected}: ID encontrado {cue_id}")
        if start < previous_end:
            errors.append(f"cue {cue_id}: sobreposição com cue anterior")
        if duration <= 0:
            errors.append(f"cue {cue_id}: duração inválida")
        if duration > args.max_duration and cue_id in args.allow_long_cue:
            warnings.append(
                f"cue {cue_id}: duração {duration:.2f}s autorizada para unidade vocal indivisível"
            )
        elif duration > args.max_duration:
            errors.append(f"cue {cue_id}: duração {duration:.2f}s > {args.max_duration:.2f}s")
        elif duration > args.preferred_max_duration:
            warnings.append(
                f"cue {cue_id}: duração {duration:.2f}s acima da faixa preferida"
            )
        if len(text_lines) > args.max_lines:
            errors.append(f"cue {cue_id}: {len(text_lines)} linhas > {args.max_lines}")
        for number, line in enumerate(visible_lines, 1):
            if len(line) > args.max_cpl:
                errors.append(
                    f"cue {cue_id}, linha {number}: {len(line)} caracteres > {args.max_cpl}"
                )
            original_line = text_lines[number - 1]
            if SDH_BRACKET.search(line):
                errors.append(
                    f"cue {cue_id}, linha {number}: marcação SDH entre colchetes"
                )
            if SDH_PARENTHETICAL_LINE.match(line):
                errors.append(
                    f"cue {cue_id}, linha {number}: descrição SDH entre parênteses"
                )
            if SDH_SPEAKER_LABEL.match(line):
                errors.append(
                    f"cue {cue_id}, linha {number}: provável rótulo de falante"
                )
            if MUSIC_SYMBOL.search(line):
                errors.append(
                    f"cue {cue_id}, linha {number}: símbolo musical não permitido"
                )
            if SDH_STYLE_TAG.search(original_line):
                errors.append(
                    f"cue {cue_id}, linha {number}: estilo de cor ou posição não permitido"
                )
        if cps > args.max_cps:
            errors.append(f"cue {cue_id}: {cps:.1f} CPS > {args.max_cps:.1f}")
        elif cps > args.target_cps:
            warnings.append(
                f"cue {cue_id}: {cps:.1f} CPS acima da meta de {args.target_cps:.1f}"
            )
        previous_end = end

    if errors:
        print("FALHOU")
        for error in errors:
            print(f"- {error}")
        return 1

    if warnings:
        print(f"OK: {len(blocks)} cues; sem violações rígidas")
        print("ATENÇÃO EDITORIAL")
        for warning in warnings:
            print(f"- {warning}")
        return 0

    print(f"OK: {len(blocks)} cues; sem violações ou alertas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
