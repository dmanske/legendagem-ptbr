# Uso

## Criar uma legenda a partir de vídeo ou áudio

Anexe o arquivo ou informe o caminho no Codex:

> Use $tradutor-de-clipes para transcrever este vídeo com ElevenLabs Scribe v2, traduzir editorialmente para PT-BR, sincronizar e validar o SRT.

A skill inspeciona a mídia, salva a transcrição bruta, traduz por blocos de
contexto e cria uma segmentação adequada ao tipo de conteúdo.

## Clipe musical

> Legende este videoclipe em PT-BR. Entre na primeira sílaba, saia no último som vocal audível e não prolongue os cues por causa do instrumental.

Quando uma palavra ou nota vocal for realmente sustentada, ela pode ultrapassar
o limite normal de duração sem ser cortada artificialmente.

## Filme ou série com SRT original

> Use este vídeo e o SRT original para criar uma legenda PT-BR com recomposição adaptativa. Trate o SRT como referência textual e âncoras, não como grade rígida.

A skill reconstrói falas e microcenas antes de traduzir e pode unir, dividir ou
retimar cues quando o áudio, a troca de falante, a leitura ou os cortes exigirem.

## Traduzir somente um SRT

> Traduza este SRT para PT-BR preservando IDs, timestamps, ordem e quantidade. Não retime.

Sem a mídia correspondente, a estrutura é preservada por padrão.

## Usar tradução ou legenda aprovada como referência

> Use $tradutor-de-clipes e considere o SRT aprovado como memória de estilo e tradução. Não copie os timestamps nem as quebras defeituosas.

## Corrigir somente as saídas

> As entradas estão corretas. Preserve todos os IDs, textos, quebras e inícios exatamente. Revise somente as saídas que permanecem depois do fim da voz.

Nessa revisão, piano, reverb, harmônicos e acompanhamento não contam como
continuidade vocal. Uma extensão além do fim lexical do Scribe exige evidência
de voz ou nota sustentada realmente audível.

## Transcrever diretamente com ElevenLabs

```bash
python3 skill/tradutor-de-clipes/scripts/transcribe_scribe_v2.py \
  video.mp4 transcricao.json --language auto
```

Use `--diarize` apenas quando vários falantes precisarem ser distinguidos para
análise interna. Os identificadores não aparecem no SRT.

## Validar um SRT

```bash
python3 skill/tradutor-de-clipes/scripts/validate_srt.py legenda.srt
```

Uma unidade vocal indivisível confirmada pode ser autorizada explicitamente:

```bash
python3 skill/tradutor-de-clipes/scripts/validate_srt.py \
  legenda.srt --allow-long-cue 36
```

O validador confirma estrutura e legibilidade. A qualidade final ainda exige
revisão editorial e sincronização audiovisual de todos os cues.
