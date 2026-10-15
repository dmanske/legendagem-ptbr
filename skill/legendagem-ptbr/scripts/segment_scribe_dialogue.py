#!/usr/bin/env python3
"""Convert an ElevenLabs Scribe word stream into dialogue-sized JSON chunks."""

import argparse
import json
import re
from pathlib import Path


SENTENCE_END = re.compile(r"[.!?…][\"'»)]*$")


def join_words(words):
    return " ".join(word["text"].strip() for word in words).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript")
    parser.add_argument("output")
    parser.add_argument("--max-duration", type=float, default=5.8)
    parser.add_argument("--max-chars", type=int, default=78)
    parser.add_argument("--pause", type=float, default=0.75)
    args = parser.parse_args()

    data = json.loads(Path(args.transcript).read_text(encoding="utf-8"))
    words = [item for item in data["words"] if item.get("type") == "word"]
    chunks = []
    current = []

    def flush():
        nonlocal current
        if not current:
            return
        chunks.append({
            "id": len(chunks) + 1,
            "start": current[0]["start"],
            "end": current[-1]["end"],
            "speaker": current[0].get("speaker_id"),
            "text": join_words(current),
        })
        current = []

    for word in words:
        if current:
            speaker_changed = word.get("speaker_id") != current[-1].get("speaker_id")
            gap = max(0.0, word["start"] - current[-1]["end"])
            duration = word["end"] - current[0]["start"]
            candidate = join_words(current + [word])
            sentence_finished = bool(SENTENCE_END.search(current[-1]["text"]))
            if (
                speaker_changed
                or gap >= args.pause
                or sentence_finished
                or duration > args.max_duration
                or len(candidate) > args.max_chars
            ):
                flush()
        current.append(word)
    flush()

    Path(args.output).write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
