# Filmes, séries, documentários e entrevistas

Usar este modo para criar legenda a partir de uma mídia audiovisual com diálogo
contínuo. Para traduzir um SRT pronto, aplicar também `existing-srt-rules.md`.
Toda saída deste projeto é legenda limpa, nunca SDH.

## Preparação

- Inspecionar todas as faixas de áudio e legenda. Confirmar idioma, versão,
  dublagem, canais e faixa realmente escolhida.
- Preferir uma legenda ou roteiro no idioma original como evidência textual
  quando pertencer à mesma versão. Confirmar sua correspondência contra o
  áudio e, quando existir, contra a faixa interna limpa. Usá-la como transcrição
  de referência e âncoras temporais, não como grade obrigatória de cues.
- Executar `source-verification-rules.md` e criar um mapa curto de personagens,
  relações, termos, lugares e formas de tratamento.
- Em séries, carregar decisões aprovadas de episódios anteriores e atualizá-las
  somente quando o episódio atual justificar a mudança.

## Transcrição e falantes

- Quando houver somente o vídeo, transcrever toda a faixa falada antes da tradução. Salvar a resposta bruta e construir a segmentação a partir de palavras, pausas, turnos e imagem.
- Quando houver um SRT original confiável da mesma versão, evitar retranscrição integral desnecessária. Usar transcrição por palavra somente para limites novos, trechos ambíguos ou anomalias.
- Usar Scribe v2 com diarização em mídias com várias pessoas. Deixar a detecção
  de idioma automática em conteúdo multilíngue; fixar o idioma quando ele for
  conhecido e isso melhorar a precisão.
- Usar `speaker_id` apenas para separar turnos, acompanhar continuidade e evitar
  fundir falas de pessoas diferentes. Nunca exibir `speaker_0`, nomes, cargos ou
  rótulos de voz no SRT.
- Manter `tag_audio_events=false`. Ignorar eventos não verbais mesmo que apareçam
  na resposta bruta.
- Conferir nomes, termos raros, fala abafada, sobreposição, voz ao telefone e
  trechos de baixa confiança contra áudio, imagem e fontes.
- Em conteúdo longo, salvar a transcrição bruta e trabalhar em partes retomáveis
  com contexto de borda. Não retranscrever mídia paga quando um resultado bruto
  utilizável já estiver salvo.

## Conteúdo da legenda limpa

Manter:

- diálogo falado, narração e voz em off com conteúdo;
- fala ao telefone, rádio ou televisão quando for narrativamente relevante;
- canto somente quando a letra tiver função narrativa real;
- texto visível na imagem somente quando for indispensável à compreensão e não
  for repetido no diálogo. Texto narrativo na tela não é SDH.

Omitir sempre:

- efeitos sonoros, música incidental, ruídos e descrições de ambiente;
- marcações como `[risos]`, `(porta bate)`, `♪`, `MÚSICA TENSA` e equivalentes;
- nomes, cores ou identificadores de falante;
- vocalizações sem palavras e reações repetitivas sem informação;
- descrições de tom, emoção, sotaque ou posição da voz.

Se um SRT-fonte for CC ou SDH, extrair e traduzir apenas o conteúdo verbal e o
texto narrativo indispensável. Remover as marcações sem apagar palavras faladas
que estejam no mesmo cue.

## Segmentação e diálogo

- Com vídeo e SRT-fonte, reconstruir primeiro cada fala completa e permitir que a segmentação final em PT-BR tenha quantidade e limites diferentes. Preservar 1:1 somente por pedido explícito.
- Criar novo cue em troca de falante, oração completa, pausa relevante,
  interrupção ou mudança de cena que torne a permanência inadequada.
- Quando uma fala contiver frases ou afirmações independentes com pausa, ataque
  novo ou corte sustentando a separação, preferir cues distintos se cada parte
  continuar natural e legível. Não manter várias emissões independentes em um
  cue longo apenas porque cabem em duas linhas ou porque a união reduz o CPS.
- Em trailer, clipe narrativo, entrevista curta ou conteúdo promocional misto,
  aceitar uma segmentação moderadamente mais densa quando mudança de emissão,
  pausa, plano, enquadramento ou ênfase sustentar o novo cue. Não fundir apenas
  para reduzir a quantidade de cues ou tornar cada cue gramaticalmente isolado.
- Quando o usuário fornecer ou aprovar uma grade manual, preservar sua quantidade,
  seu ritmo e suas separações válidas em conteúdo comparável. Se uma fronteira
  cortar palavra, antecipar fala, produzir flash ou ultrapassar 17 CPS, movê-la
  para o limite lexical ou a pausa mais próxima e reencaixar o texto. Manter a
  quantidade de cues quando isso puder ser feito sem migração de conteúdo;
  fundir somente quando nenhuma solução válida preservar a divisão.
- Não aceitar uma divisão que deixe apenas sujeito, negação, auxiliar,
  preposição ou começo de oração em um cue, salvo quando a interpretação ou o
  corte impuser essa suspensão e ambos os lados continuarem compreensíveis. Uma
  continuação sintática curta pode atravessar cues quando a mudança audiovisual
  for real, a leitura combinada for imediata e a forma tiver sido aprovada pelo
  usuário; isso nunca autoriza cortar uma palavra.
- Não fundir pessoas diferentes para economizar cues.
- Quando duas falas curtas precisarem compartilhar o mesmo cue, usar uma linha
  por pessoa com hífen simples e espaço (`- `), sem nomes. Não colocar mais de
  duas pessoas no mesmo cue.
- Em sobreposição, preservar as falas inteligíveis e narrativamente necessárias.
  Se todas não couberem, priorizar a fala que conduz a ação ou a resposta.
- Usar contexto anterior e posterior para resolver pronomes, elipses e intenção,
  sem antecipar informação nem mover fala para o tempo errado.

## Timing audiovisual

- Em legenda criada do vídeo, entrar junto ou muito próximo do início da fala,
  sem revelar o diálogo antecipadamente.
- Encerrar no fim natural da fala e permitir permanência curta para leitura
  quando não houver outra fala, sobreposição ou corte incompatível.
- Respeitar trocas de plano e cortes de cena quando forem visualmente relevantes;
  evitar deixar uma legenda da cena anterior atravessar um corte forte.
- Evitar flashes e intervalos imperceptíveis. Priorizar uma experiência contínua
  de leitura sem esconder mudança de falante.
- Depois de inserir qualquer fronteira, conferir que ela esteja numa pausa,
  troca de falante ou limite lexical confirmado. A fronteira não pode cortar o
  intervalo temporal de uma palavra. Se o timestamp por palavra for duvidoso,
  decidir pelo áudio e pela forma de onda, não por divisão proporcional.
- Ao adaptar uma grade manual, auditar cada fronteira contra os timestamps por
  palavra ou o áudio. O validador estrutural de SRT não detecta sozinho um corte
  dentro da palavra; exigir cobertura integral `N/N` e zero limites internos.
- Auditar cobertura integral: toda palavra-fonte deve pertencer por inteiro a um
  intervalo final, exatamente uma vez. Sobreposição parcial com um cue não conta
  como cobertura. Recalcular CPS e duração de cada lado; se a divisão criar
  flash, ultrapassar 17 CPS ou produzir fragmentos artificiais, condensar o
  texto ou preservar uma unidade maior.
- Não aplicar automaticamente a tolerância de primeira sílaba, nota sustentada
  ou célula melódica usada em canções.
- Em SRT existente sem a mídia ou com timing expressamente aprovado, preservar todos os tempos. Com a mídia e sem pedido de preservação 1:1, ajustar a grade para o PT-BR e revisar cada novo limite contra o áudio e a imagem.
- Nunca criar um novo limite dividindo proporcionalmente a duração pelo tamanho do texto. Usar fala, timestamps por palavra, pausa ou fronteira original confirmada.

## Tradução e continuidade

- Traduzir cenas e sentenças completas em lotes com contexto anterior e posterior.
- Preservar personalidade, registro, humor, ironia, palavrões, intimidade e
  relações de poder sem suavização automática.
- Manter um mapa de nomes, tratamentos, termos da obra e decisões recorrentes.
- Não tornar explícito um subtexto que o original apenas sugere.
- Fazer a leitura final ocultando o original e conferir coerência de personagem,
  continuidade entre cenas e naturalidade do PT-BR.

## Validação

- Máximo de 2 linhas e 42 caracteres por linha.
- Meta de 15 CPS e máximo rígido de 17 CPS.
- Máximo de 7,5 segundos por cue, salvo timing preexistente e imutável.
- Sem sobreposição involuntária.
- Conferir todos os cues criados da mídia contra o áudio e o vídeo.
- Conferir o texto inteiro, nomes, termos, relações e continuidade.
- Fazer uma busca final por colchetes, parênteses descritivos, símbolos musicais,
  rótulos e outros vestígios SDH. Entregar somente depois de removê-los.
