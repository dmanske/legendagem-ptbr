# Provedores e credenciais

## IA de tradução

A própria IA que executa esta skill deve traduzir e revisar os cues. Codex é o ambiente nativo. Outro agente pode usar as regras, desde que consiga ler `SKILL.md`, executar comandos locais e acessar os arquivos de mídia.

Para automação externa, aceitar um provedor compatível com Chat Completions e manter endpoint, modelo e chave fora do repositório. Nunca registrar ou imprimir credenciais.

## ElevenLabs Scribe v2

Preferir ElevenLabs quando `ELEVENLABS_API_KEY` estiver disponível. Executar:

```bash
python scripts/transcribe_elevenlabs.py entrada.mp4 transcricao.json --language en
```

O script envia a mídia para `POST https://api.elevenlabs.io/v1/speech-to-text`, solicita timestamps por palavra e normaliza a resposta para o formato usado pela skill.

Se a API responder `401` ou `403`, explicar que a chave precisa permitir Speech to Text. Não solicitar a chave na conversa.

## Transcrição local

Usar `scripts/transcribe_clip.py` quando não houver ElevenLabs ou quando o usuário não quiser enviar mídia a um serviço externo. Requer FFmpeg, Python e `faster-whisper`. O primeiro uso pode baixar um modelo grande.

## Ordem recomendada

1. ElevenLabs Scribe v2 para reconhecimento e timestamps.
2. Letra oficial ou fornecida pelo usuário como referência textual.
3. Áudio do vídeo final como fonte de sincronização.
4. IA ativa para tradução, consistência e regras editoriais.
5. `validate_srt.py` para validação determinística.
