# Tradutor de Clipes

Skill pública para criar, traduzir, revisar e sincronizar legendas SRT limpas
em português brasileiro. Funciona com clipes, músicas, shows, filmes, séries,
documentários, entrevistas, diálogos e SRTs existentes.

A skill usa o ElevenLabs Scribe v2 para transcrição e timestamps por palavra. A
tradução editorial é feita pelo próprio agente, considerando contexto, sentido,
fraseado, leitura e sincronização — não por tradução automática palavra a palavra.

## O que está incluído

- Transcrição de vídeo ou áudio com ElevenLabs Scribe v2.
- Tradução contextual para PT-BR.
- Sincronização musical na primeira sílaba e no último som vocal audível.
- Saídas sem cauda artificial de piano, reverb ou acompanhamento.
- Recomposição adaptativa de filmes e séries quando o vídeo e o SRT original são fornecidos juntos.
- Preservação de IDs e timestamps ao traduzir somente um SRT, salvo pedido diferente.
- Diálogo seletivo e limpeza completa de elementos SDH.
- Até duas linhas, 42 caracteres por linha e máximo rígido de 17 CPS.
- Validação determinística do SRT antes da entrega.

Versão pública atual: **2026.10.14.1**.

## Instalação em um comando

### macOS ou Linux

```bash
curl -fsSL https://raw.githubusercontent.com/dmanske/tradutor-de-clipes/main/install.sh | bash
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/dmanske/tradutor-de-clipes/main/install.ps1 | iex
```

O instalador preserva a versão anterior como backup. Abra uma nova sessão do
Codex depois da instalação.

Se preferir revisar o código antes de executá-lo, consulte
[docs/INSTALLATION.md](docs/INSTALLATION.md).

## Requisitos

- Codex ou outro agente compatível com skills no formato `SKILL.md`.
- Python 3.9 ou superior.
- FFmpeg e FFprobe disponíveis no `PATH`.
- Chave ElevenLabs com acesso a Speech to Text.

Configure `ELEVENLABS_API_KEY` fora do repositório. Nunca publique a chave em
commits, issues, conversas ou capturas de tela.

Execute o diagnóstico depois da instalação:

```bash
python3 ~/.codex/skills/tradutor-de-clipes/scripts/doctor.py
```

## Como usar

Anexe o arquivo ou informe seu caminho no Codex e peça:

> Use $tradutor-de-clipes para criar uma legenda PT-BR profissional deste vídeo.

Para um filme ou uma série com SRT original:

> Use $tradutor-de-clipes com este vídeo e o SRT original. Faça recomposição adaptativa e entregue uma legenda PT-BR limpa.

Para traduzir somente um SRT:

> Traduza este SRT para PT-BR, preservando IDs, timestamps, ordem e quantidade de cues.

Para corrigir apenas finais demorados:

> As entradas estão corretas. Preserve todos os inícios e corrija somente as saídas que permanecem depois do fim da voz.

Veja mais exemplos em [docs/USAGE.md](docs/USAGE.md).

## Política de transcrição

O ElevenLabs Scribe v2 é o transcritor principal. A skill não troca
silenciosamente para Whisper: se a ElevenLabs falhar ou a credencial estiver
ausente, o agente deve informar o problema antes de usar qualquer alternativa.
O script local permanece disponível somente para uso explicitamente escolhido.

## Estrutura

```text
skill/tradutor-de-clipes/
├── SKILL.md
├── VERSION
├── agents/
├── references/
└── scripts/
```

Copie sempre a pasta completa: `SKILL.md` depende das referências e dos scripts.

## Documentação

- [Instalação](docs/INSTALLATION.md)
- [Configuração e ElevenLabs](docs/CONFIGURATION.md)
- [Exemplos de uso](docs/USAGE.md)
- [Segurança](SECURITY.md)
- [Como contribuir](CONTRIBUTING.md)

## Privacidade

Ao usar ElevenLabs, a mídia é enviada ao serviço para transcrição. A chave fica
no ambiente local e não deve ser gravada no repositório. Arquivos de mídia,
transcrições e `.env` são ignorados pelo Git.

## Licença

MIT © Daniel Manske.
