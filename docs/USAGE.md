# Uso

## Criar uma legenda do vídeo

No Codex:

> Use $tradutor-de-clipes para transcrever este vídeo, traduzir para PT-BR e criar um SRT sincronizado. Inicie cada cue exatamente na primeira sílaba e valide o resultado.

## Usar uma letra de referência

> Use $tradutor-de-clipes neste vídeo. Considere a letra anexada como referência textual, mas obtenha os timestamps exclusivamente do áudio do vídeo final.

A letra pode estar sem repetições. A skill deve detectar as repetições no áudio e reutilizar a mesma tradução.

## Comparar com uma tradução aprovada

> Use $tradutor-de-clipes e mantenha a tradução dos versos equivalentes conforme o SRT aprovado anexado. Crie novos cues quando o fraseado desta versão for diferente.

## Transcrever diretamente com ElevenLabs

```bash
python3 skill/tradutor-de-clipes/scripts/transcribe_elevenlabs.py video.mp4 transcricao.json --language en
```

## Transcrever localmente

```bash
python3 skill/tradutor-de-clipes/scripts/transcribe_clip.py video.mp4 transcricao.json --language en
```

## Validar um SRT

```bash
python3 skill/tradutor-de-clipes/scripts/validate_srt.py legenda.pt-BR.srt
```

A saída válida deve informar `sem violações`.
