#!/usr/bin/env bash
# Separa a voz de um áudio ou vídeo com o Demucs (htdemucs, duas faixas).
# Na primeira vez, instala o Demucs num ambiente Python próprio, fora do
# Python do sistema. O PyTorch ocupa cerca de 1 GB: o agente deve pedir o "ok"
# do usuário antes de rodar este script num computador sem o Demucs.
#
# Uso:
#   separate_vocals.sh --check              # só diz se o Demucs já está instalado
#   separate_vocals.sh --install            # só instala
#   separate_vocals.sh <midia> <pasta-saida>
# Saída: <pasta-saida>/vocals.wav e <pasta-saida>/no_vocals.wav
set -eu

BASE="${LEGENDAGEM_HOME:-$HOME/.local/share/legendagem-ptbr}"
VENV="$BASE/demucs-venv"
PY="$VENV/bin/python"

installed() {
  [ -x "$PY" ] && "$PY" -c "import demucs, soundfile, numpy" >/dev/null 2>&1
}

install() {
  if installed; then
    echo "Demucs já instalado em $VENV"
    return 0
  fi
  echo "Instalando Demucs em $VENV (PyTorch, cerca de 1 GB)..."
  mkdir -p "$BASE"
  python3 -m venv "$VENV"
  "$PY" -m pip install -q --upgrade pip
  "$PY" -m pip install -q demucs soundfile numpy
  installed && echo "Demucs instalado."
}

case "${1:-}" in
  --check)
    if installed; then echo "DEMUCS: OK ($VENV)"; exit 0; else echo "DEMUCS: AUSENTE"; exit 1; fi
    ;;
  --install)
    install
    exit 0
    ;;
  ""|-h|--help)
    sed -n 2,12p "$0"
    exit 0
    ;;
esac

SRC="$1"
OUT="${2:?informe a pasta de saída}"
install
mkdir -p "$OUT"
TMP="$OUT/_stereo.wav"
ffmpeg -v error -y -i "$SRC" -vn -ac 2 -ar 44100 "$TMP"
"$PY" -m demucs --two-stems=vocals -n htdemucs -o "$OUT/_demucs" "$TMP" >/dev/null 2>&1
mv "$OUT/_demucs/htdemucs/_stereo/vocals.wav" "$OUT/vocals.wav"
mv "$OUT/_demucs/htdemucs/_stereo/no_vocals.wav" "$OUT/no_vocals.wav"
rm -rf "$OUT/_demucs" "$TMP"
echo "OK: $OUT/vocals.wav"
