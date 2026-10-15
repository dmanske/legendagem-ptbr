# Legendagem Profissional PT-BR

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

Versão pública atual: **2026.10.15.2**.

## Fonte oficial das regras

O comportamento da skill é definido por `skill/legendagem-ptbr/SKILL.md` e
pelos arquivos de `skill/legendagem-ptbr/references/`. O `README` é apenas uma
apresentação para pessoas; prompts e regras de aplicativos antigos não são
carregados pela skill.

O padrão foi calibrado a partir de um acervo aprovado com 67 legendas e 7.955
cues. Esse acervo serviu como evidência estatística e memória editorial, mas não
é um conjunto de milhares de regras e não precisa ser enviado ao agente. As
decisões reutilizáveis foram condensadas nas referências da skill.

## Como funciona

1. **Inspeção:** identifica faixas, idioma, duração, codecs, volume e legendas existentes com FFmpeg e FFprobe.
2. **Transcrição:** envia a mídia autorizada ao ElevenLabs Scribe v2 e salva a resposta original com timestamps por palavra. Em conteúdo com várias pessoas, a diarização pode ser usada apenas na análise interna.
3. **Verificação:** confronta a transcrição com o áudio executado e, quando a obra é identificável, com letras, roteiros, nomes e fontes confiáveis. O áudio final continua sendo a autoridade para o que foi realmente dito ou cantado.
4. **Tradução contextual:** reconstrói versos, falas ou microcenas completas antes de traduzir. Preserva agente, negação, tempo, lugar, intensidade, emoção, registro e imagens recorrentes.
5. **Segmentação e sincronização:** cria cues conforme o tipo de mídia. Música segue ataques, células vocais e notas sustentadas; diálogo segue frases, falantes, pausas e cortes de cena.
6. **Revisão editorial:** ajusta naturalidade, pontuação, capitalização, quebras de linha, repetições e velocidade de leitura, removendo todo conteúdo SDH.
7. **Validação e entrega:** verifica estrutura, sobreposição, duas linhas, 42 CPL, 17 CPS e duração. Depois salva o SRT sem sobrescrever silenciosamente uma versão existente.

## Modos principais

- **Vídeo ou áudio sem legenda:** transcreve toda a faixa útil, traduz e cria a segmentação PT-BR do zero.
- **Filme ou série com SRT original:** usa recomposição adaptativa; o SRT serve como texto e âncoras, enquanto áudio, falantes, leitura e cortes definem a estrutura final.
- **Somente SRT:** preserva IDs, timestamps, ordem e quantidade por padrão, traduzindo com contexto entre os cues.
- **Música e shows:** separa células cantadas, repetições, ad-libs e falas de palco; entra na primeira sílaba e sai no último som vocal audível.
- **Diálogo seletivo:** mantém falas com significado e remove vocalizações, ruídos e descrições sem conteúdo verbal.
- **Revisão de legenda pronta:** pode corrigir texto, quebras, entradas ou saídas de forma localizada, preservando os elementos já aprovados.

## Instalação em um comando

### macOS ou Linux

```bash
curl -fsSL https://raw.githubusercontent.com/dmanske/legendagem-ptbr/main/install.sh | bash
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/dmanske/legendagem-ptbr/main/install.ps1 | iex
```

O instalador preserva a versão anterior em `~/.codex/skill-backups/`, fora da
pasta indexada de skills. Abra uma nova sessão do Codex depois da instalação.

Ao migrar da antiga `$tradutor-de-clipes`, o instalador arquiva a pasta anterior
automaticamente para impedir que duas versões da mesma skill sejam carregadas.

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
python3 ~/.codex/skills/legendagem-ptbr/scripts/doctor.py
```

## Como usar

Anexe o arquivo ou informe seu caminho no Codex e peça:

> Use $legendagem-ptbr para criar uma legenda PT-BR profissional deste vídeo.

Para um filme ou uma série com SRT original:

> Use $legendagem-ptbr com este vídeo e o SRT original. Faça recomposição adaptativa e entregue uma legenda PT-BR limpa.

Para traduzir somente um SRT:

> Traduza este SRT para PT-BR, preservando IDs, timestamps, ordem e quantidade de cues.

Para corrigir apenas finais demorados:

> As entradas estão corretas. Preserve todos os inícios e corrija somente as saídas que permanecem depois do fim da voz.

Veja mais exemplos em [docs/USAGE.md](docs/USAGE.md).

## Política de transcrição

O ElevenLabs Scribe v2 é o transcritor deste fluxo. A skill não inclui nem usa
Whisper, Faster-Whisper ou outro transcritor local como fallback. Se a
ElevenLabs falhar, estiver sem credencial ou indisponível, o agente deve parar e
informar o problema antes de produzir qualquer legenda alternativa.

## Estrutura

```text
skill/legendagem-ptbr/
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
