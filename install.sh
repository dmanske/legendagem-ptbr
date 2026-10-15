#!/usr/bin/env bash
set -eu

REPO="${LEGENDAGEM_REPO:-${TRADUTOR_REPO:-dmanske/legendagem-ptbr}}"
REF="${LEGENDAGEM_REF:-${TRADUTOR_REF:-main}}"
SKILL_NAME="legendagem-ptbr"
LEGACY_SKILL_NAME="tradutor-de-clipes"
CODEX_ROOT="${CODEX_HOME:-$HOME/.codex}"
DESTINATION="$CODEX_ROOT/skills/$SKILL_NAME"
LEGACY_DESTINATION="$CODEX_ROOT/skills/$LEGACY_SKILL_NAME"
BACKUP_ROOT="$CODEX_ROOT/skill-backups"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || pwd)"
TEMP_DIR=""

cleanup() {
  if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
  fi
}
trap cleanup EXIT

if [ -f "$SCRIPT_DIR/skill/$SKILL_NAME/SKILL.md" ]; then
  SOURCE="$SCRIPT_DIR/skill/$SKILL_NAME"
else
  TEMP_DIR="$(mktemp -d)"
  ARCHIVE="$TEMP_DIR/repository.tar.gz"
  URL="https://github.com/$REPO/archive/refs/heads/$REF.tar.gz"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$URL" -o "$ARCHIVE"
  elif command -v wget >/dev/null 2>&1; then
    wget -q "$URL" -O "$ARCHIVE"
  else
    echo "Instale curl ou wget e tente novamente." >&2
    exit 1
  fi
  tar -xzf "$ARCHIVE" -C "$TEMP_DIR"
  REPO_NAME="${REPO##*/}"
  SOURCE="$TEMP_DIR/$REPO_NAME-$REF/skill/$SKILL_NAME"
fi

if [ ! -f "$SOURCE/SKILL.md" ]; then
  echo "A skill não foi encontrada no pacote baixado." >&2
  exit 1
fi

mkdir -p "$CODEX_ROOT/skills" "$BACKUP_ROOT"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)-$$"
if [ -e "$DESTINATION" ]; then
  BACKUP="$BACKUP_ROOT/$SKILL_NAME.backup-$TIMESTAMP"
  mv "$DESTINATION" "$BACKUP"
  echo "Versão anterior preservada em: $BACKUP"
fi
if [ -e "$LEGACY_DESTINATION" ]; then
  LEGACY_BACKUP="$BACKUP_ROOT/$LEGACY_SKILL_NAME.backup-$TIMESTAMP"
  mv "$LEGACY_DESTINATION" "$LEGACY_BACKUP"
  echo "Nome antigo preservado em: $LEGACY_BACKUP"
fi

cp -R "$SOURCE" "$DESTINATION"
chmod +x "$DESTINATION"/scripts/*.py 2>/dev/null || true

echo "Skill instalada em: $DESTINATION"
echo "Reinicie o Codex e execute: python3 $DESTINATION/scripts/doctor.py"
