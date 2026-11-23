# Ressincronizar uma tradução pela legenda de referência

Pedido típico: "ressincronizar", "o texto em PT está bom mas o tempo está errado",
"usar o tempo do inglês com as falas do português".

## Quando usar

- Existe uma legenda de **referência com sincronia boa** para o vídeo que será
  assistido (em geral o inglês extraído do próprio arquivo, mesmo com SDH).
- Existe uma **tradução PT-BR com texto bom e tempo errado**, normalmente de outro
  lançamento (outra fonte, outra edição, outro corte de abertura).

Não usar ElevenLabs nem serviço pago: a referência já é a fonte de tempo.

## Regras

- **O texto da tradução não muda.** Não retraduzir, não condensar, não mover palavras
  entre cues. Erros de tradução evidentes vão para uma lista à parte, para o usuário
  decidir.
- Cada cue PT recebe o tempo do(s) cue(s) da referência que dizem a mesma coisa:
  - 1 PT : 1 referência → tempo da referência;
  - 1 PT : N referência → início do primeiro e fim do último;
  - N PT : 1 ou N referência → fronteiras internas mapeadas do tempo relativo do PT e
    encaixadas na borda de referência mais próxima (até 400 ms). Nunca repartir por
    quantidade de caracteres.
- Cues da referência que são só SDH (`(SIGHS)`, `[MUSIC]`, `♪`) não têm par e são
  ignorados. Rótulos de falante (`BARD:`) não contam como fala.
- Cue PT sem par (texto de tela, créditos da tradução) recebe só o deslocamento local.
- Não sobrescrever os originais; saída em arquivo novo, UTF-8.

## Passos

1. Mostrar ao usuário 2 ou 3 exemplos de partes diferentes do filme (tempo da
   referência, tempo PT atual, PT com o tempo novo) e o deslocamento medido.
2. Rodar:

   ```bash
   python3 scripts/resync_by_reference.py REFERENCIA.srt TRADUCAO.srt SAIDA.srt --relatorio rel.json
   ```

   O script lê a tradução em UTF-8 ou Windows-1252, mede o deslocamento local
   (mediana numa janela de 5 min), liga PT e referência por sobreposição e corrige
   sobreposições na saída.
3. Conferir: texto da saída idêntico ao da tradução (mesma quantidade e ordem),
   lista "sem par" do relatório (deve ser só texto de tela), `scripts/validate_srt.py`
   sem sobreposição nem erro de estrutura. Avisos de CPS que já existiam na tradução
   não são erro novo: comparar a contagem antes e depois.
4. Entregar com contagens (1:1, juntadas, divididas, sem par) e 7 a 10 pontos de
   conferência espalhados pelo filme (tempo + PT + referência).

## Caso de referência

The Odyssey (2026): referência EN com 2616 cues, PT com 1915 cues em Windows-1252,
PT adiantado de 0,75 a 0,83 s. Resultado: 1802 cues 1:1, 91 juntadas, 16 divididas
ou mistas, 6 sem par (títulos e créditos); avisos de CPS caíram de 587 para 295.
O usuário aprovou o resultado ("ficou perfeito").
