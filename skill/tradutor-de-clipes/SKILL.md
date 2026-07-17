---
name: tradutor-de-clipes
description: Transcrever clipes musicais em ingles, traduzir as letras para portugues brasileiro e criar legendas SRT profissionais sincronizadas pelo fraseado musical. Usar quando o usuario pedir para legendar, traduzir ou sincronizar um videoclipe, musica, apresentacao de louvor ou arquivo de audio/video em MP4, MKV, MOV, WEBM, MP3, WAV, M4A, FLAC ou OGG.
---

# Tradutor de Clipes

Criar legendas PT-BR a partir do audio, orientadas pelas frases cantadas e pausas vocais. Preservar versões anteriores e entregar um SRT validado.

## Fluxo obrigatório

1. Confirmar o arquivo e inspecionar faixas, duração, codec e volume com `ffprobe` e `ffmpeg`.
2. Se não houver áudio útil, solicitar letra, transcrição ou arquivo com áudio. Não inferir letra por leitura labial.
3. Escolher o transcritor. Se `ELEVENLABS_API_KEY` estiver configurada, preferir ElevenLabs Scribe v2 por `scripts/transcribe_elevenlabs.py`. Caso contrário, usar `faster-whisper` por `scripts/transcribe_clip.py`. Instalar dependências apenas com autorização quando necessário.
4. Transcrever a faixa inteira. Em música, não depender apenas de VAD ou silêncio, pois o instrumental continua durante pausas vocais.
5. Revisar a transcrição contra repetições, refrões e contexto musical. Corrigir alucinações evidentes sem inventar conteúdo incerto.
6. Traduzir para PT-BR natural. Preservar sentido, emoção, registro religioso quando aplicável e consistência absoluta dos refrões.
7. Criar cues pelo fraseado: iniciar exatamente na primeira sílaba detectada, sem antecipação; encerrar perto da última palavra; dividir em cada pausa vocal ou nova unidade cantada, mesmo quando o texto couber em um só cue.
8. Aplicar as regras de `references/editorial-rules.md`.
9. Salvar em `legendas/<titulo>.pt-BR.srt`. Se já existir, criar uma nova versão sem sobrescrever a anterior.
10. Executar `scripts/validate_srt.py` e corrigir todas as violações antes da entrega.

## Decisões editoriais

- Para tradução de SRT pronto, preservar IDs e timing por padrão.
- Para legenda criada do áudio, permitir criar, dividir, unir e retimar cues para acompanhar o cantor.
- Usar entrada exata como padrão: `cue.start = primeira_palavra.start`. Não aplicar lead-in negativo nem antecipar a legenda, salvo pedido explícito do usuário.
- Ao remover antecipação, encurtar a saída do cue anterior quando necessário para preservar pelo menos 80 ms sem sobreposição.
- Priorizar fraseado e sintaxe; usar equilíbrio visual apenas como desempate.
- Preferir pirâmide tradicional quando houver duas linhas: linha superior igual ou maior que a inferior.
- Não agrupar repetições cantadas em momentos diferentes dentro de um cue longo.
- Usar timestamps por palavra como evidência; revisar manualmente trechos com vozes sobrepostas ou reconhecimento instável.
- Nunca pedir que o usuário cole chaves de API na conversa. Orientar o uso de variável de ambiente, cofre do sistema ou campo seguro do aplicativo.

## Recursos

- `scripts/transcribe_clip.py`: transcrição JSON com timestamps por palavra.
- `scripts/transcribe_elevenlabs.py`: transcrição Scribe v2 por API, usando `ELEVENLABS_API_KEY`.
- `scripts/doctor.py`: diagnóstico multiplataforma da instalação e das dependências.
- `scripts/validate_srt.py`: valida estrutura, sobreposição, CPL, CPS e duração.
- `references/editorial-rules.md`: padrão consolidado de tradução e sincronização.
- `references/providers.md`: escolha entre IA ativa, ElevenLabs e transcrição local. Ler ao configurar o ambiente ou quando um provedor falhar.

## Entrega

Informar o arquivo criado, quantidade de cues, validações executadas e incertezas relevantes. Fornecer link local clicável para o SRT.
