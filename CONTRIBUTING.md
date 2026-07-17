# Contribuindo

Contribuições devem preservar o objetivo principal: legendas musicais PT-BR fiéis, naturais e sincronizadas exatamente com a primeira sílaba.

Antes de enviar uma alteração:

```bash
python3 -m unittest discover -s tests -v
python3 skill/tradutor-de-clipes/scripts/validate_srt.py tests/fixtures/valid.srt
```

Não inclua arquivos de mídia, transcrições protegidas, chaves de API ou `.env` em commits e issues.
