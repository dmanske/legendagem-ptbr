#!/usr/bin/env python3
"""Transcribe audio with ElevenLabs Scribe v2 and save the complete JSON."""

from __future__ import annotations

import argparse
import http.client
import json
import mimetypes
import os
import ssl
import sys
import uuid
from pathlib import Path
from typing import Dict, Optional, Tuple


HOST = "api.elevenlabs.io"
ENDPOINT = "/v1/speech-to-text"
CHUNK_SIZE = 1024 * 1024


def tls_context() -> ssl.SSLContext:
    configured = os.environ.get("SSL_CERT_FILE", "").strip()
    if configured and Path(configured).is_file():
        return ssl.create_default_context(cafile=configured)

    defaults = ssl.get_default_verify_paths()
    if defaults.cafile and Path(defaults.cafile).is_file():
        return ssl.create_default_context()

    for candidate in ("/etc/ssl/cert.pem", "/private/etc/ssl/cert.pem"):
        if Path(candidate).is_file():
            return ssl.create_default_context(cafile=candidate)

    return ssl.create_default_context()


def multipart_parts(
    boundary: str,
    fields: Dict[str, str],
    source: Path,
) -> Tuple[bytes, bytes]:
    chunks = []
    for name, value in sorted(fields.items()):
        chunks.append(
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
                f"{value}\r\n"
            ).encode("utf-8")
        )

    content_type = mimetypes.guess_type(source.name)[0] or "application/octet-stream"
    chunks.append(
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; '
            f'filename="{source.name}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8")
    )
    prefix = b"".join(chunks)
    suffix = f"\r\n--{boundary}--\r\n".encode("utf-8")
    return prefix, suffix


def send_file(connection: http.client.HTTPSConnection, source: Path) -> None:
    with source.open("rb") as audio:
        while True:
            chunk = audio.read(CHUNK_SIZE)
            if not chunk:
                break
            connection.send(chunk)


def request_fields(
    language: str,
    diarize: bool,
    num_speakers: Optional[int],
) -> Dict[str, str]:
    fields = {
        "model_id": "scribe_v2",
        "tag_audio_events": "false",
        "timestamps_granularity": "word",
        "diarize": "true" if diarize else "false",
    }
    normalized_language = language.strip().lower()
    if normalized_language and normalized_language != "auto":
        fields["language_code"] = normalized_language
    if num_speakers is not None:
        fields["num_speakers"] = str(num_speakers)
    return fields


def transcribe(
    source: Path,
    api_key: str,
    language: str,
    diarize: bool,
    num_speakers: Optional[int],
) -> dict:
    boundary = f"Boundary-{uuid.uuid4().hex}"
    fields = request_fields(language, diarize, num_speakers)

    prefix, suffix = multipart_parts(boundary, fields, source)
    content_length = len(prefix) + source.stat().st_size + len(suffix)

    connection = http.client.HTTPSConnection(
        HOST,
        timeout=600,
        context=tls_context(),
    )
    try:
        connection.putrequest("POST", ENDPOINT)
        connection.putheader("xi-api-key", api_key)
        connection.putheader(
            "Content-Type",
            f"multipart/form-data; boundary={boundary}",
        )
        connection.putheader("Content-Length", str(content_length))
        connection.endheaders()
        connection.send(prefix)
        send_file(connection, source)
        connection.send(suffix)

        response = connection.getresponse()
        payload = response.read()
    finally:
        connection.close()

    try:
        parsed = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(
            f"ElevenLabs retornou HTTP {response.status} sem JSON válido."
        ) from error

    if not 200 <= response.status < 300:
        detail = parsed.get("detail", parsed)
        raise RuntimeError(
            f"ElevenLabs retornou HTTP {response.status}: "
            f"{json.dumps(detail, ensure_ascii=False)}"
        )

    words = parsed.get("words")
    if not isinstance(words, list):
        raise RuntimeError("A resposta do Scribe v2 não contém a lista 'words'.")
    lexical_words = [
        item
        for item in words
        if isinstance(item, dict)
        and item.get("type") == "word"
        and isinstance(item.get("start"), (int, float))
        and isinstance(item.get("end"), (int, float))
    ]
    if not lexical_words:
        raise RuntimeError("O Scribe v2 não retornou palavras com timestamps.")

    return parsed


def write_json(destination: Path, payload: dict) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(
        f".{destination.name}.{uuid.uuid4().hex}.tmp"
    )
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(destination)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Transcreve áudio com ElevenLabs Scribe v2."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument(
        "--language",
        default="auto",
        help=(
            "Código ISO-639-1/3 do áudio; use 'auto' para detecção automática "
            "(padrão)."
        ),
    )
    parser.add_argument(
        "--diarize",
        action="store_true",
        help=(
            "Identifica falantes no JSON para análise interna. "
            "Os identificadores nunca devem aparecer na legenda."
        ),
    )
    parser.add_argument(
        "--num-speakers",
        type=int,
        help="Quantidade máxima esperada de falantes, entre 1 e 32.",
    )
    args = parser.parse_args()

    if not args.source.is_file():
        parser.error(f"Arquivo não encontrado: {args.source}")
    if args.num_speakers is not None and not 1 <= args.num_speakers <= 32:
        parser.error("--num-speakers deve estar entre 1 e 32")
    if args.num_speakers is not None:
        args.diarize = True

    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        parser.error(
            "Defina ELEVENLABS_API_KEY no ambiente; não informe a chave no comando."
        )

    try:
        payload = transcribe(
            args.source,
            api_key,
            args.language,
            args.diarize,
            args.num_speakers,
        )
        write_json(args.destination, payload)
    except Exception as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1

    word_count = sum(
        1 for item in payload["words"] if item.get("type") == "word"
    )
    mode = "com diarização interna" if args.diarize else "sem diarização"
    print(
        f"OK: Scribe v2 salvou {word_count} palavras em "
        f"{args.destination} ({mode})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
