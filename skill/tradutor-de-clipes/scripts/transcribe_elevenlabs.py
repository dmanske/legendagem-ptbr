#!/usr/bin/env python3
"""Transcribe media with ElevenLabs Scribe v2 and emit normalized word timestamps."""

from __future__ import annotations

import argparse
import http.client
import json
import mimetypes
import os
import sys
import uuid
from pathlib import Path


HOST = "api.elevenlabs.io"
PATH = "/v1/speech-to-text"


def field(boundary: str, name: str, value: str) -> bytes:
    return (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
        f"{value}\r\n"
    ).encode()


def transcribe(source: Path, api_key: str, language: str | None) -> dict:
    boundary = f"Boundary-{uuid.uuid4().hex}"
    fields = {
        "model_id": "scribe_v2",
        "tag_audio_events": "false",
        "timestamps_granularity": "word",
        "diarize": "false",
    }
    if language:
        fields["language_code"] = language

    prefix = b"".join(field(boundary, key, value) for key, value in fields.items())
    mime = mimetypes.guess_type(source.name)[0] or "application/octet-stream"
    file_header = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{source.name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode()
    suffix = f"\r\n--{boundary}--\r\n".encode()
    content_length = len(prefix) + len(file_header) + source.stat().st_size + len(suffix)

    connection = http.client.HTTPSConnection(HOST, timeout=180)
    connection.putrequest("POST", PATH)
    connection.putheader("xi-api-key", api_key)
    connection.putheader("Content-Type", f"multipart/form-data; boundary={boundary}")
    connection.putheader("Content-Length", str(content_length))
    connection.endheaders()
    connection.send(prefix)
    connection.send(file_header)
    with source.open("rb") as media:
        while chunk := media.read(1024 * 1024):
            connection.send(chunk)
    connection.send(suffix)

    response = connection.getresponse()
    data = response.read()
    connection.close()
    try:
        payload = json.loads(data)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"ElevenLabs retornou HTTP {response.status} sem JSON válido") from exc
    if not 200 <= response.status < 300:
        detail = payload.get("detail") or payload.get("message") or payload
        raise RuntimeError(f"ElevenLabs HTTP {response.status}: {detail}")
    return payload


def normalize(payload: dict) -> dict:
    words = []
    for item in payload.get("words", []):
        if item.get("type") != "word":
            continue
        if item.get("start") is None or item.get("end") is None:
            continue
        text = str(item.get("text", "")).strip()
        if text:
            words.append({"start": item["start"], "end": item["end"], "word": text})

    start = words[0]["start"] if words else 0
    end = words[-1]["end"] if words else 0
    text = str(payload.get("text", "")).strip()
    return {
        "provider": "elevenlabs",
        "model": "scribe_v2",
        "language": payload.get("language_code"),
        "duration": end,
        "segments": [{"start": start, "end": end, "text": text, "words": words}],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--language", default="en", help="ISO language code; use auto for detection")
    args = parser.parse_args()

    if not args.source.is_file():
        parser.error(f"arquivo não encontrado: {args.source}")
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        print("Configure ELEVENLABS_API_KEY no ambiente.", file=sys.stderr)
        return 2

    try:
        payload = transcribe(args.source, api_key, None if args.language == "auto" else args.language)
        normalized = normalize(payload)
        args.destination.parent.mkdir(parents=True, exist_ok=True)
        args.destination.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Transcrição salva em: {args.destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
