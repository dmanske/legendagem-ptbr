# Instalação

## Instalação rápida

### macOS ou Linux

```bash
curl -fsSL https://raw.githubusercontent.com/dmanske/tradutor-de-clipes/main/install.sh | bash
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/dmanske/tradutor-de-clipes/main/install.ps1 | iex
```

O instalador copia a pasta completa para `~/.codex/skills/tradutor-de-clipes`
ou para `${CODEX_HOME}/skills/tradutor-de-clipes`. Uma instalação anterior é
renomeada como backup.

Abra uma nova sessão do Codex depois da instalação.

## Dependências

São necessários Python 3.9+, FFmpeg e FFprobe.

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
sudo apt install -y ffmpeg python3 git
```

## ElevenLabs

Crie uma chave com acesso a Speech to Text e configure a variável
`ELEVENLABS_API_KEY` conforme [CONFIGURATION.md](CONFIGURATION.md). Não coloque
a chave no comando de transcrição, no repositório ou no prompt enviado ao agente.

## Diagnóstico

macOS ou Linux:

```bash
python3 ~/.codex/skills/tradutor-de-clipes/scripts/doctor.py
```

Windows:

```powershell
py -3 "$HOME\.codex\skills\tradutor-de-clipes\scripts\doctor.py"
```

O diagnóstico mostra apenas se a chave está configurada; nunca imprime o valor.

## Instalação revisável

Para inspecionar o código antes da instalação:

```bash
git clone https://github.com/dmanske/tradutor-de-clipes.git
cd tradutor-de-clipes
bash install.sh
```

No Windows:

```powershell
git clone https://github.com/dmanske/tradutor-de-clipes.git
Set-Location tradutor-de-clipes
.\install.ps1
```

## Atualização

Execute novamente o instalador rápido. A instalação anterior será preservada
como backup. Quem mantém um clone também pode executar `git pull` antes do
instalador local.

Para conferir a versão instalada:

```bash
cat ~/.codex/skills/tradutor-de-clipes/VERSION
```
