# Texto completo, junção, gênero e revisão geral (filmes e séries)

Regras aprovadas pelo usuário em 24/11/2026 depois de comparar a versão juntada com a
separada no mesmo filme.

Vale para diálogo falado (filme, série, documentário, entrevista), criado da mídia
ou traduzido de SRT. **Não vale para música**, que segue `music-clean-rules.md`, nem
para timing que o usuário mandou preservar 1:1. Em conflito com outra regra de CPS,
condensação ou segmentação de diálogo, **esta prevalece**.

A conferência de gênero (seção 4) e a revisão geral (seção 5) são **obrigatórias em toda
entrega**, sem esperar o usuário pedir. `scripts/dialogue_review.py` apoia as duas
(`genero`, `lado-a-lado`) e a junção (`juntar`); o que ele lista são candidatos a conferir.

## 1. Texto completo primeiro

- Não encurtar a tradução para caber em CPS. Preservar quem, o quê, onde, quando,
  intensidade, graça e palavrão.
- 17 CPS passa a ser alerta, não limite rígido. Continuam rígidos: 2 linhas,
  42 caracteres por linha, sem sobreposição.
- Fala rápida: primeiro juntar (seção 2), depois estender a saída no silêncio
  seguinte em até 1 segundo, sem invadir a próxima fala e respeitando corte de cena.
- Reescrever de forma mais direta só em último caso, quando ficar ilegível (referência:
  acima de 25 CPS depois das tentativas), sem perder informação. Informar esses casos.
- Uma correção da revisão não pode encurtar a fala sem necessidade.

## 2. Juntar pedaços da mesma frase

Juntar dois cues seguidos somente quando **todas** as condições valerem:

- mesma pessoa e mesma frase (o primeiro não termina em ponto, `?`, `!` nem `…`);
- intervalo menor que 150 ms e nenhum dos dois é diálogo duplo;
- pelo menos um dos pedaços passa de 17 CPS e a junção reduz esse pico;
- cabe em 2 linhas de 42 com quebra boa, sem apagar palavra, e em até 7 segundos.

O resto fica separado. Não juntar quando isso antecipar revelação, resposta ou piada.
Se não houver quebra boa sem perder texto, voltar a separar. Ao juntar, só o segundo
pedaço perde a inicial maiúscula (nome próprio e personagem mantêm).

## 3. Quebras de linha

- Reler todas as legendas de duas linhas, não só as marcadas por script.
- Nunca deixar no fim da linha palavra solta ("que o", "de", "a", "se na", "muito")
  nem separar substantivo e adjetivo ("pensamentos / sujos", "algumas / semanas").
- Exemplo: "Toda aquela água do rio nos pulmões / que o matou ou ao menos deu início
  a tudo." (35/42), e não "…nos pulmões que o / matou…" (41/41).

## 4. Gênero e falante

- O inglês não marca gênero. Antes de entregar, extrair do vídeo, se existirem, a
  faixa SDH (nomes de quem fala) e uma faixa de idioma que marca gênero (francês,
  espanhol, italiano) e cruzar por tempo com toda palavra portuguesa marcada.
- A faixa auxiliar é evidência, não verdade: conferir com a cena e com o texto.
  Nunca exibir rótulo de falante na legenda.
- Sem confirmação, usar forma neutra ("Valeu", "Muito prazer", "criança") e informar.
- Sem essas faixas, diarização do Scribe pelas regras já existentes da skill.

## 5. Revisão geral obrigatória

- Com a legenda montada, reler **todas** as falas (N/N) lado a lado com o original.
- Procurar: erro de sentido, calque ("navegar um casamento"), pergunta e resposta que
  não combinam, pedaço na fala errada, piada que depende de palavra repetida, gênero,
  concordância depois de substituição, detalhe perdido.
- Comparar o texto palavra por palavra antes e depois de mexer só em quebras.

## 6. Validação e entrega

- **Nome do arquivo** (vale sobre o item 15 do fluxo da `SKILL.md`): ao lado da mídia, a
  legenda em português fica com o nome exato do vídeo e `.srt`, para o player abrir
  sozinho. Se esse nome já estiver com a legenda de origem, confirmar o idioma pelo
  conteúdo e renomeá-la para `<nome>.en.srt` (ou o código do idioma dela) antes de
  gravar. Nunca apagar nem sobrescrever: se `<nome>.en.srt` já existir, usar
  `<nome>.en.2.srt`; se o `.srt` existente já for português, gravar `.v2.srt` e avisar.
  Informar os nomes finais.
- `validate_srt.py` acusa erro acima de 17 CPS. Rodar também com `--max-cps 99` para
  confirmar que o restante passa e informar quantas passam de 17 e de 23.
- Entregar relatório: falas revisadas (N/N), quantas corrigidas, exemplos antes e
  depois com o minuto, gênero não confirmado, falas reescritas e o que não foi
  conferido (áudio, cena). Não dizer que a sincronia foi conferida sem ouvir.
