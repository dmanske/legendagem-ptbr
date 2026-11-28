#!/usr/bin/env python3
"""Refina entradas e saídas de um SRT musical pela energia da voz isolada.

Rodar com o Python do ambiente do Demucs (tem numpy e soundfile):
  ~/.local/share/legendagem-ptbr/demucs-venv/bin/python refine_by_vocals.py \
      entrada.srt vocals.wav saida.srt [--sustained "amém,amen"]

O que faz, por cue:
- entrada: se já há voz no início marcado, recua até o ataque (no máximo 0,3 s;
  até 3,5 s em palavras sustentadas com melisma, como "amém"); se não há voz,
  avança até o primeiro som (no máximo 0,3 s). Nunca entra antes do fim do cue
  anterior.
- saída: se a voz continua, estende até ela parar (no máximo +1,5 s; +4 s em
  palavras sustentadas), sem encostar no próximo cue; se a voz já parou, recua
  até o último som (no máximo 0,4 s).

É uma medição de energia, não escuta: coral, ad-libs ("yeah", "oh") e falas
fora da legenda também têm energia. Conferir o log e corrigir à mão os cues que
estenderam por cima de algo que não é a letra legendada.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import soundfile as sf


def parse_srt(text: str):
    cues = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", lines[1])
        if not m:
            continue
        g = list(map(int, m.groups()))
        start = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        end = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        cues.append([start, end, "\n".join(lines[2:])])
    return cues


def ts(x: float) -> str:
    ms = int(round(x * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("srt")
    ap.add_argument("vocals")
    ap.add_argument("output")
    ap.add_argument("--sustained", default="amém,amen,aleluia,hallelujah")
    args = ap.parse_args()

    audio, sr = sf.read(args.vocals)
    if audio.ndim > 1:
        audio = audio.mean(1)
    hop = int(sr * 0.01)
    n = len(audio) // hop
    frames = audio[: n * hop].reshape(n, hop)
    db = 20 * np.log10(np.sqrt((frames**2).mean(1)) + 1e-9)

    def v(t: float) -> float:
        return db[min(max(int(round(t * 100)), 0), n - 1)]

    sustained = tuple(w.strip().lower() for w in args.sustained.split(",") if w.strip())
    cues = parse_srt(Path(args.srt).read_text(encoding="utf-8-sig"))
    out, log = [], []
    for i, (s0, e0, txt) in enumerate(cues):
        long_word = any(w in txt.lower() for w in sustained)
        seg = db[int(s0 * 100) : int(e0 * 100) + 1]
        thr = max(np.percentile(seg, 95) - 14, -40) if len(seg) else -40
        prev_end = out[-1][1] if out else 0.0
        nxt = cues[i + 1][0] if i + 1 < len(cues) else None

        lim = max(prev_end + 0.04, s0 - (3.5 if long_word else 0.3))
        t = s0
        if v(t) > thr:
            while t - 0.01 > lim and any(v(t - k) > thr for k in (0.01, 0.02, 0.03)):
                t -= 0.01
        else:
            u = s0
            while u < s0 + 0.3 and v(u) <= thr:
                u += 0.01
            t = u if u < s0 + 0.3 else s0
        start = round(t, 2)

        cap = e0 + (4.0 if long_word else 1.5)
        if nxt is not None:
            cap = min(cap, nxt - 0.04)
        t = e0
        if v(t) > thr:
            gap, last = 0.0, t
            while t + 0.01 < cap:
                t += 0.01
                if v(t) > thr:
                    gap, last = 0.0, t
                else:
                    gap += 0.01
                    if gap > 0.08:
                        break
            t = last
        else:
            u = e0
            while u > max(e0 - 0.4, start + 0.5) and v(u) <= thr:
                u -= 0.01
            t = u
        end = round(t, 2)
        if nxt is not None:
            end = min(end, round(nxt - 0.04, 2))
        if end <= start:
            end = e0
        out.append([start, end, txt])
        if abs(start - s0) > 0.05 or abs(end - e0) > 0.05:
            log.append(
                f"{i + 1:4d} {s0:8.2f}->{start:8.2f} ({start - s0:+.2f})  "
                f"{e0:8.2f}->{end:8.2f} ({end - e0:+.2f})  {txt.splitlines()[0][:40]}"
            )

    with open(args.output, "w", encoding="utf-8") as f:
        for i, (a, b, t) in enumerate(out, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n")
    print("\n".join(log))
    print(f"{len(log)} de {len(out)} cues mudaram. Revisar o log antes de entregar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
