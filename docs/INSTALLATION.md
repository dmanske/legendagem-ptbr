# Instalação

## 1. Instalar a skill

### macOS ou Linux

```bash
curl -fsSL https://raw.githubusercontent.com/dmanske/tradutor-de-clipes/main/install.sh | bash
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/dmanske/tradutor-de-clipes/main/install.ps1 | iex
```

O instalador copia a pasta completa para `${CODEX_HOME}/skills/tradutor-de-clipes` ou, por padrão, `~/.codex/skills/tradutor-de-clipes`. Uma instalação anterior é preservada como backup.

## 2. Instalar FFmpeg e Python

### macOS com Homebrew

```bash
brew install ffmpeg python@3.11 git
```

### Windows com winget

```powershell
winget install --id Gyan.FFmpeg --exact
winget install --id Python.Python.3.11 --exact
winget install --id Git.Git --exact
```

### Ubuntu ou Debian

```bash
sudo apt update
sudo apt install -y ffmpeg python3 python3-venv git
```

Feche e reabra o terminal depois da instalação no Windows.

## 3. Escolher a transcrição

### ElevenLabs recomendado

Crie uma chave com permissão Speech to Text e configure `ELEVENLABS_API_KEY` conforme [CONFIGURATION.md](CONFIGURATION.md).

### Whisper local opcional

```bash
python3 -m venv .venv
```

macOS ou Linux:

```bash
source .venv/bin/activate
pip install --upgrade pip faster-whisper
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip faster-whisper
```

O primeiro uso do Whisper pode baixar vários gigabytes de modelo.

## 4. Diagnosticar

macOS ou Linux:

```bash
python3 ~/.codex/skills/tradutor-de-clipes/scripts/doctor.py
```

Windows:

```powershell
py -3 "$HOME\.codex\skills\tradutor-de-clipes\scripts\doctor.py"
```

## Instalação revisável

Se preferir não executar código diretamente da internet:

```bash
git clone https://github.com/dmanske/tradutor-de-clipes.git
cd tradutor-de-clipes
bash install.sh
```
