# Tradutor de Clipes

Skill pública para transcrever clipes musicais em inglês, traduzir para português brasileiro e gerar legendas SRT sincronizadas pelo fraseado.

O padrão editorial inclui entrada exatamente na primeira sílaba, separação por pausas vocais, refrões consistentes, até 2 linhas, 42 caracteres por linha, 17 CPS e validação sem sobreposições.

## Instalação em um comando

### macOS ou Linux

```bash
curl -fsSL https://raw.githubusercontent.com/dmanske/tradutor-de-clipes/main/install.sh | bash
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/dmanske/tradutor-de-clipes/main/install.ps1 | iex
```

Reinicie o Codex depois da instalação.

Para revisar o código antes de executar, clone o repositório e rode o instalador localmente. Consulte [docs/INSTALLATION.md](docs/INSTALLATION.md).

## O que é necessário

- Uma IA capaz de executar skills e comandos locais. Codex é o ambiente nativo e já fornece a IA de tradução.
- Python 3.9 ou superior.
- FFmpeg e FFprobe.
- Chave ElevenLabs com Speech to Text para o melhor fluxo recomendado.
- Opcionalmente, `faster-whisper` para transcrição totalmente local.

Sem ElevenLabs, a skill continua funcionando com Whisper local. Sem uma IA ativa, os scripts conseguem transcrever e validar, mas não realizam sozinhos a tradução editorial completa.

## Configuração rápida

Configure a chave fora do repositório:

```bash
export ELEVENLABS_API_KEY="sua-chave"
```

No Windows PowerShell:

```powershell
$env:ELEVENLABS_API_KEY = "sua-chave"
```

Nunca cole sua chave em uma conversa, issue ou commit. Veja [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

Execute o diagnóstico:

```bash
python3 ~/.codex/skills/tradutor-de-clipes/scripts/doctor.py
```

No Windows:

```powershell
py -3 "$HOME\.codex\skills\tradutor-de-clipes\scripts\doctor.py"
```

## Como usar

No Codex, anexe ou informe o caminho do vídeo e peça:

> Use $tradutor-de-clipes para criar uma legenda PT-BR profissional deste clipe. Use entrada exata na primeira sílaba e valide o SRT.

Consulte [docs/USAGE.md](docs/USAGE.md) para outros exemplos.

## Privacidade

Com ElevenLabs, a mídia é enviada ao serviço para transcrição. Com `faster-whisper`, a transcrição ocorre localmente. Chaves e arquivos de mídia são ignorados pelo Git.

## Licença

MIT © Daniel Manske.
