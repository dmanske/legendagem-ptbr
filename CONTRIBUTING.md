# Contribuindo

Contribuições devem preservar o objetivo principal: legendas PT-BR fiéis,
naturais, limpas e sincronizadas conforme o tipo de mídia. Regras musicais não
devem ser aplicadas mecanicamente a filmes, séries ou entrevistas.

Antes de enviar uma alteração:

```bash
python3 -m unittest discover -s tests -v
python3 skill/tradutor-de-clipes/scripts/validate_srt.py tests/fixtures/valid.srt
```

Ao alterar o conteúdo da skill, atualize também `VERSION` e mantenha README,
documentação e testes coerentes com o comportamento publicado.

Não inclua arquivos de mídia, transcrições protegidas, chaves de API ou `.env` em commits e issues.
