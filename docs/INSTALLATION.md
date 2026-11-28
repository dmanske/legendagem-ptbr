# Instalação

## Instalação rápida

### macOS ou Linux

```bash
curl -fsSL https://raw.githubusercontent.com/dmanske/legendagem-ptbr/main/install.sh | bash
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/dmanske/legendagem-ptbr/main/install.ps1 | iex
```

O instalador copia a pasta completa para `~/.codex/skills/legendagem-ptbr`
ou para `${CODEX_HOME}/skills/legendagem-ptbr`. Uma instalação anterior é
movida para `~/.codex/skill-backups/` ou `${CODEX_HOME}/skill-backups/`, fora
da pasta indexada de skills.

Se encontrar a antiga `tradutor-de-clipes`, o instalador também a move para a
pasta de backups, evitando duas skills equivalentes ativas ao mesmo tempo.

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

## Separação de voz (opcional, recomendada para música)

Para conferir entradas e saídas pela voz isolada, a skill usa o
[Demucs](https://github.com/facebookresearch/demucs) (modelo `htdemucs`). Ele
não vem com a skill: na primeira vez, o script instala o Demucs num ambiente
Python próprio, sem mexer no Python do sistema. O PyTorch ocupa cerca de 1 GB,
e o agente pede o "ok" antes de instalar.

```bash
# Já está instalado?
bash ~/.codex/skills/legendagem-ptbr/scripts/separate_vocals.sh --check
# Instalar agora (ou deixar o script instalar no primeiro uso)
bash ~/.codex/skills/legendagem-ptbr/scripts/separate_vocals.sh --install
```

O ambiente fica em `~/.local/share/legendagem-ptbr/demucs-venv` (ou em
`$LEGENDAGEM_HOME/demucs-venv`). Para remover, basta apagar essa pasta. A
separação de um show de 8 minutos leva uns 5 minutos num Mac com Apple Silicon.
Sem o Demucs a skill continua funcionando, com os tempos do Scribe.

## ElevenLabs

Crie uma chave com acesso a Speech to Text e configure a variável
`ELEVENLABS_API_KEY` conforme [CONFIGURATION.md](CONFIGURATION.md). Não coloque
a chave no comando de transcrição, no repositório ou no prompt enviado ao agente.

## Diagnóstico

macOS ou Linux:

```bash
python3 ~/.codex/skills/legendagem-ptbr/scripts/doctor.py
```

Windows:

```powershell
py -3 "$HOME\.codex\skills\legendagem-ptbr\scripts\doctor.py"
```

O diagnóstico mostra apenas se a chave está configurada; nunca imprime o valor.

## Instalação revisável

Para inspecionar o código antes da instalação:

```bash
git clone https://github.com/dmanske/legendagem-ptbr.git
cd legendagem-ptbr
bash install.sh
```

No Windows:

```powershell
git clone https://github.com/dmanske/legendagem-ptbr.git
Set-Location legendagem-ptbr
.\install.ps1
```

## Atualização

Execute novamente o instalador rápido. A instalação anterior será preservada
como backup. Quem mantém um clone também pode executar `git pull` antes do
instalador local.

Para conferir a versão instalada:

```bash
cat ~/.codex/skills/legendagem-ptbr/VERSION
```
