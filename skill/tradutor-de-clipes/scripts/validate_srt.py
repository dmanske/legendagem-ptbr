#!/usr/bin/env python3
"""Validate structural and readability constraints of an SRT file."""

import argparse
import re
from pathlib import Path


TIMESTAMP = re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})$")


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
    parser.add_argument("--max-cps", type=float, default=17.0)
    parser.add_argument("--max-duration", type=float, default=7.5)
    args = parser.parse_args()

    content = Path(args.srt).read_text(encoding="utf-8-sig").strip()
    blocks = re.split(r"\n\s*\n", content) if content else []
    errors = []
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
        text = " ".join(text_lines)
        cps = len(text) / duration if duration > 0 else float("inf")

        if cue_id != expected:
            errors.append(f"cue {expected}: ID encontrado {cue_id}")
        if start < previous_end:
            errors.append(f"cue {cue_id}: sobreposição com cue anterior")
        if duration <= 0:
            errors.append(f"cue {cue_id}: duração inválida")
        if duration > args.max_duration:
            errors.append(f"cue {cue_id}: duração {duration:.2f}s > {args.max_duration:.2f}s")
        if len(text_lines) > args.max_lines:
            errors.append(f"cue {cue_id}: {len(text_lines)} linhas > {args.max_lines}")
        for number, line in enumerate(text_lines, 1):
            if len(line) > args.max_cpl:
                errors.append(
                    f"cue {cue_id}, linha {number}: {len(line)} caracteres > {args.max_cpl}"
                )
        if cps > args.max_cps:
            errors.append(f"cue {cue_id}: {cps:.1f} CPS > {args.max_cps:.1f}")
        previous_end = end

    if errors:
        print("FALHOU")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OK: {len(blocks)} cues; sem violações")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
