#!/usr/bin/env python3
"""Transcribe an audio/video file to JSON with word-level timestamps."""

import argparse
import json

from faster_whisper import WhisperModel


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("--model", default="large-v3-turbo")
    parser.add_argument("--language", default="en")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--compute-type", default="int8")
    args = parser.parse_args()

    model = WhisperModel(
        args.model,
        device=args.device,
        compute_type=args.compute_type,
    )
    segments, info = model.transcribe(
        args.source,
        language=args.language or None,
        beam_size=5,
        vad_filter=False,
        word_timestamps=True,
        condition_on_previous_text=False,
        initial_prompt=args.prompt or None,
    )

    payload = {
        "language": info.language,
        "language_probability": info.language_probability,
        "duration": info.duration,
        "segments": [],
    }
    for segment in segments:
        payload["segments"].append(
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
                "words": [
                    {"start": word.start, "end": word.end, "word": word.word}
                    for word in (segment.words or [])
                ],
            }
        )

    with open(args.destination, "w", encoding="utf-8") as output:
        json.dump(payload, output, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
