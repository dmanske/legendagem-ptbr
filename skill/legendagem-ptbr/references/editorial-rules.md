# Regras editoriais consolidadas

## Hierarquia

1. Fidelidade ao que foi falado ou cantado na versão processada.
2. Sincronização adequada ao modo: musical ou audiovisual.
3. Fidelidade ao sentido e ao contexto da obra.
4. Naturalidade do português brasileiro.
5. Legibilidade e velocidade de leitura.
6. Integridade sintática, semântica e equilíbrio visual.

## Transcrição principal

- Usar ElevenLabs Scribe v2 como primeira opção quando a chave e a autorização estiverem disponíveis.
- Neste projeto, o pedido para legendar um clipe autoriza usar a chave ElevenLabs já configurada pelo proprietário.
- Não substituir silenciosamente o Scribe v2 por Whisper. Informar a indisponibilidade e usar Whisper somente como alternativa local ou conferência.
- Usar timestamps do Scribe como pontos de busca. Mesmo o Scribe v2 não determina sozinho a primeira sílaba nem o final de uma nota sustentada.
- Em música, separar os vocais antes da conferência acústica e enviar preferencialmente a faixa vocal ao Scribe quando o fluxo permitir. Em audiovisual falado, preservar a faixa que melhor mantenha o diálogo e usar diarização apenas como apoio interno.
- Verificar a saída por palavra antes de segmentar. Marcar duração nula ou negativa, palavras comprimidas, timestamps duplicados e sequências impossivelmente rápidas como anomalias.
- Quando houver anomalia forte, reprocessar somente uma janela local ao redor do trecho. Comparar o novo resultado com o original e substituir apenas quando a evidência melhorar; não retranscrever nem deslocar toda a música por causa de um erro local.
- Em finais de música, considerar anômala uma última palavra cuja duração reconhecida atravesse a reverberação, o instrumental ou chegue artificialmente ao fim da mídia. Reprocessar uma janela local com contexto, confirmar o último som vocal e distinguir cauda acústica de nota realmente sustentada antes de alterar o timestamp.

## Perfil calibrado pelo acervo final

- As regras deste perfil sobre primeira sílaba, ataque vocal, nota sustentada e tolerâncias de milissegundos são musicais. Em diálogo audiovisual, aplicar `audiovisual-dialogue-rules.md`.
- O acervo final aprovado serve como memória de tradução, fraseado e estilo. Não copiar automaticamente seus timestamps, quebras ou exceções técnicas.
- Ignorar como exemplo de layout qualquer cue do acervo que ultrapasse os limites rígidos. Esses casos são erros históricos, não preferências.
- Preferir uma linha em textos realmente curtos. Considerar 34 a 37 caracteres uma faixa confortável, mas permitir duas linhas mesmo abaixo de 42 caracteres quando uma divisão semântica limpa melhorar o aspecto visual. O limite rígido continua sendo 42 caracteres por linha.
- Buscar 15 CPS ou menos. De 15 a 17 CPS exige atenção editorial; acima de 17 CPS é erro e deve ser corrigido antes da exportação.
- Preferir duração aproximada de 1,2 a 4,7 segundos quando o fraseado permitir. Usar 5 segundos como teto editorial desejável e 7,5 segundos como limite normal. Uma única fala, palavra ou nota sustentada confirmada pode ultrapassar 7,5 segundos quando não houver divisão vocal legítima: preservar o início e o fim audíveis, registrar a exceção no validador e não duplicar, cortar nem apagar texto para forçar o limite. Abaixo de aproximadamente 0,8 segundo, conferir se há flash e condensar o texto antes de mexer em um limite vocal correto.
- Tratar 420 ms de pausa vocal como sinal forte de nova frase, não como limiar obrigatório. Pausas menores podem criar outro cue quando houver novo ataque, respiração, pontuação, célula melódica ou retomada de cadência.
- Uma margem automática após a última palavra reconhecida pode servir somente como aproximação de trabalho. Na saída final, removê-la e marcar o último som vocal audível; não acrescentar cauda para aumentar o tempo de leitura.
- Nunca aplicar antecipação automática. O padrão é `cue.start = primeira_silaba_audivel`.
- Aceitar UTF-8, UTF-8 com BOM e Windows-1252 ao ler SRTs aprovados. Exportar sempre em UTF-8.

## Tradução

- Quando a legenda estiver sendo produzida interativamente pelo Codex, o próprio agente faz a tradução editorial usando todo o contexto disponível. Lovable não é o tradutor principal desse fluxo.
- Usar Lovable como motor do aplicativo automático, para lotes longos retomáveis ou quando o usuário solicitar explicitamente; toda saída automática continua sujeita à revisão editorial.
- Consultar primeiro o acervo final aprovado pelo usuário para recuperar voz, concisão, escolhas de tradução e tratamento de refrões. Não copiar timestamps, quebras defeituosas ou exceções técnicas do acervo.
- Traduzir sentido e emoção, não a ordem literal do inglês.
- Redigir primeiro a tradução semanticamente completa. Não resumir apenas para
  produzir uma frase mais curta, reduzir a quantidade de cues ou ficar abaixo
  da meta de 15 CPS. Entre 15 e 17 CPS, preferir fidelidade quando os limites
  rígidos e a composição de duas linhas forem respeitados.
- Antes de condensar, conferir agente, ação, objeto, tempo, lugar, modalidade,
  intensidade, escopo e imagem. Remover primeiro hesitações e redundâncias sem
  função; não apagar informação apenas porque ela pode ser inferida.
- Manter nomes próprios, marcas e lugares.
- Preservar intensidade de linguagem sem censura automática.
- Aplicar terminologia religiosa consistente: Lord → Senhor; grace → graça; mercy → misericórdia; praise → louvor; worship → adoração.
- Preferência editorial fixa do usuário: quando a fonte expressar um ato real de oração ou súplica religiosa, usar a família `orar`, `orava`, `orou` e `oração`; não usar `rezar`, `rezava`, `rezou` ou `reza`. Não forçar essa terminologia quando `pray` ou equivalente for idiomático e significar `esperar`, `pedir`, `implorar` ou `tomara`; traduzir a função real no contexto.
- Traduzir versos e refrões repetidos de forma idêntica, salvo mudança clara de contexto.
- Usar registro bíblico ou contemporâneo de forma consistente conforme a obra.
- Não inventar palavras em trechos incertos; sinalizar incerteza para revisão.

## Portão de tradução contextual

Executar integralmente `contextual-translation-workflow.md` antes de aprovar o
texto. A versão literal serve como controle de significado, não como padrão de
qualidade. Rejeitar qualquer forma que preserve palavras, mas altere a relação,
a intenção, a imagem ou o efeito emocional da unidade completa.

Quando duas leituras permanecerem igualmente defensáveis e produzirem tons
distintos, informar a incerteza ao usuário em vez de esconder a decisão.

## Hierarquia de referências

Quando a obra for identificável e houver acesso a fontes, executar
`source-verification-rules.md`. Manter separadas a hierarquia usada para
determinar o texto-fonte e a hierarquia usada para decidir a tradução. Uma
tradução aprovada orienta estilo e terminologia, mas não pode vencer a fala ou o
canto realmente executado em outra versão.

## Segmentação do original antes da tradução

- Reconstruir frases e versos semanticamente completos antes de traduzir.
- Evitar cues-fonte terminados em artigo, preposição, auxiliar, conjunção ou começo de oração quando a voz continuar.
- Se a tradução de um cue incluir palavras do próximo, tratar como erro de segmentação do original, não como simples problema de quebra de linha.
- Depois de corrigir limites semânticos, traduzir novamente o bloco afetado; não deslocar manualmente a tradução entre tempos errados.
- Em canto contínuo, separar células pela emissão e pelo fraseado. Em fala contínua, separar por oração, pontuação e legibilidade.

## Cues e sincronização musical

- Tratar cada frase cantada ou unidade respiratória como candidato a cue próprio.
- Segmentar o original antes de acomodar o português: identificar ataques, células melódicas, retomadas e respirações no áudio; depois associar a cada célula o trecho correspondente da tradução.
- Dividir antes e depois de pausas vocais perceptíveis, mesmo com instrumental contínuo.
- Preferir um cue curto por célula cantada. Duas células sucessivas devem continuar em cues distintos mesmo quando, juntas, couberem em duas linhas.
- Não reunir repetições executadas em momentos diferentes apenas para reduzir a quantidade de cues.
- Entrar exatamente na primeira sílaba audível, sem antecipar a legenda. Usar o início da primeira palavra reconhecida apenas como ponto de busca e confirmar a entrada no vocal isolado.
- Aceitar como alvo de entrada de 0 a 80 ms depois do ataque vocal. Rejeitar qualquer cue que apareça antes da primeira sílaba.
- Antecipar a entrada somente quando o usuário pedir explicitamente; nunca aplicar lead-in negativo por padrão.
- Ajustar cada cue localmente; não aplicar deslocamento global quando a diferença entre reconhecimento e canto variar ao longo da música.
- Ao inserir limites internos em um cue, usar as sílabas e os ataques vocais como limites. Não distribuir a duração proporcionalmente à quantidade de caracteres da tradução.
- Depois de dividir, auditar novamente o início externo: se o texto traduz a frase inteira, ele deve entrar na primeira sílaba da frase, e não somente quando forem cantadas suas palavras finais.
- Usar intervalo adaptativo de 0 a 80 ms. Permitir cues encostados quando a voz for contínua e preservar a pausa real quando houver respiração; nunca criar sobreposição involuntária.
- Sair no fim audível da voz, acompanhando vogais e notas sustentadas. Não usar uma cauda fixa como substituto da revisão acústica.
- Marcar a saída no último som vocal audível. Não estender pelo instrumental, não acrescentar tempo para leitura e não cortar nota sustentada para cumprir duração máxima.
- Diagnosticar separadamente defeitos de entrada e de saída. Se o usuário aprovar as entradas e reclamar apenas de permanência excessiva, congelar IDs, texto, quebras e todos os inícios; revisar somente os finais e comprovar por comparação que `N/N entradas` permaneceram idênticas.
- Na revisão exclusiva de saída, usar o `end` da última palavra lexical do Scribe como ponto inicial de busca. Estender esse limite somente quando uma vogal ou nota vocal sustentada continuar audível. Piano, reverb, harmônicos, pratos e acompanhamento não justificam extensão; quando o mix completo mascarar a voz, preferir o limite do Scribe ou confirmar no vocal isolado. Um espectrograma do mix completo pode orientar a busca, mas não serve como prova única de cauda vocal.
- Dividir em unidades cantadas curtas quando houver nova emissão, retomada melódica ou bloco semântico, mesmo sem silêncio detectado pelo reconhecedor.
- Diferenciar quebra visual de novo cue: usar duas linhas dentro do mesmo cue somente quando a execução vocal for contínua; criar outro cue quando houver nova célula melódica, ataque vocal, retomada de cadência ou pausa perceptível.
- Ao dividir internamente uma frase cujo início e fim já foram aprovados, preservar esses limites externos e inserir apenas os novos limites internos confirmados no vocal.
- Usar os timestamps por palavra ou caractere para mapear cada célula do original ao bloco correspondente da tradução. Não distribuir o português apenas pelo tamanho visual das linhas.
- Permitir divisão musical dentro de uma expressão sintaticamente ligada quando a melodia separar claramente seus componentes. A integridade sintática continua sendo preferência, não motivo para ignorar a execução.
- Não transformar uma simples necessidade de quebra de linha em dois cues quando não houver mudança vocal ou melódica.
- Em repetições, preservar a mesma segmentação textual aprovada e realinhar cada ocorrência separadamente.
- Separar falas, comandos e ad-libs da letra principal; usar itálico quando ajudar a distingui-los.
- Em clipes, seguir `music-clean-rules.md`: omitir vocalizações isoladas sem conteúdo semântico por padrão. Preservar ad-libs, refrões e repetições quando carregarem informação, emoção narrativa ou função religiosa real.
- Em vocais simultâneos, priorizar a voz principal sem apagar automaticamente a secundária. Criar cue separado ou usar itálico quando houver conteúdo relevante; omitir a secundária somente se o usuário pedir uma legenda limpa ou se ela for uma interjeição sem conteúdo.
- Evitar cue superior a 7,5 segundos. Dividir somente quando houver nova emissão, célula ou limite vocal real; se uma única palavra ou nota sustentada exceder 7,5 segundos, preservar a duração audível inteira e registrar a exceção, sem repetir o texto nem cortar a voz.
- Evitar flashes muito curtos; condensar tradução quando o original for cantado rapidamente.
- Recalcular CPS depois de cada divisão. Se uma célula curta ultrapassar a meta, condensar a tradução primeiro; não antecipar a entrada, estender a saída sobre uma pausa nem reagrupar células diferentes para reduzir o CPS.
- Não usar detector de silêncio como única evidência em música.
- Examinar o vocal após o último cue até o fim da mídia para recuperar refrões e repetições omitidos pelo ASR.
- Nunca modificar um início ou término vocal correto para reduzir CPS. Condensar o texto.

## Linhas

- Máximo de 2 linhas e 42 caracteres por linha.
- Meta de 15 caracteres por segundo; máximo rígido de 17.
- Iniciar todo cue com letra maiúscula normal, inclusive quando ele continuar uma frase do cue anterior. Não confundir inicial maiúscula com CAIXA ALTA.
- Escolher uma ou duas linhas pela melhor leitura e composição visual. Uma frase curta pode usar duas linhas quando houver uma divisão semântica limpa e o resultado ficar mais profissional; não quebrar apenas para preencher a tela.
- Nunca quebrar artigo + substantivo, preposição + complemento, negação + verbo, pronome + verbo, auxiliar + verbo, nome próprio ou expressão fixa.
- Preferir quebra em limite de oração, pausa, vírgula, conjunção ou bloco semântico.
- Evitar palavras fracas no fim da linha: de, do, da, e, que, um, uma.
- Preferir a linha inferior igual ou maior que a superior somente depois de preservar sintaxe, unidades semânticas e ritmo. Nunca forçar essa forma separando auxiliar + verbo, preposição + complemento, artigo + substantivo ou expressão fixa. Em diálogo duplo, preservar um falante por linha.
- Em diálogo duplo, usar hífen seguido de espaço, no máximo um falante por linha e uma fala autossuficiente por linha. Não deixar a fala do mesmo personagem continuar no cue vizinho apenas para acomodar duas pessoas no cue atual.

## Pontuação e continuidade

- Usar sempre o caractere único de reticências (`…`), nunca três pontos (`...`).
- Não usar reticências apenas porque uma frase continua no cue seguinte. Em continuidade normal, encerrar sem pontuação ou com vírgula, dois-pontos ou ponto, conforme a estrutura do português.
- Usar reticências quando houver pausa audível longa, de aproximadamente 2 segundos ou mais, hesitação relevante, pensamento que se apaga, falso começo, interrupção abrupta ou fala deliberadamente deixada em suspenso.
- Quando a fala retomar no cue seguinte após uma pausa, não iniciar o novo cue com reticências. Usá-las no início somente quando o cue realmente começar no meio de uma frase por causa de conteúdo interveniente, sobreposição ou retomada parcial.
- Em canções, usar reticências no fim quando a letra continuar audivelmente, mas deixar de ser legendada por causa de diálogo ou outro conteúdo prioritário. Não usá-las para simples troca de cue entre versos contínuos.
- No perfil de clipe aprovado, omitir pontuação terminal nas células cantadas comuns; não inserir ponto ou vírgula apenas para marcar o fim de uma frase. Preservar `?`, `!`, dois-pontos e vírgula interna ou terminal quando tiverem função semântica, prosódica ou de clareza. Em conteúdo falado, aplicar pontuação normal do PT-BR.
- Em citação distribuída entre vários cues, abrir aspas no primeiro e fechar somente no último, sem repetir aspas em cada cue.

## Números

- Escrever de um a dez por extenso em texto corrido e usar algarismos acima de dez, salvo restrição de leitura, dado técnico, placar, endereço, medida, moeda, porcentagem ou grafia oficial.
- No início de uma frase, preferir o número por extenso. Manter idades em algarismos e preservar consistência quando números da mesma categoria forem comparados.
- Aplicar estas convenções sem sacrificar 42 CPL, 17 CPS, naturalidade ou fidelidade a nomes e títulos oficiais.

## Limpeza

- Produzir somente legenda limpa; não criar nem preservar SDH neste projeto.
- Remover marcações CC, nomes de falante, efeitos, descrições sonoras, símbolos musicais e indicações de música incidental.
- Preservar texto visível na imagem somente quando for indispensável à narrativa; isso não é SDH.
- Remover hesitações sem valor; traduzir confirmações com valor narrativo.
- Normalizar reticências e travessões conforme a seção `Pontuação e continuidade`, sem apagar pausas dramáticas reais.
- Não exportar ponto e vírgula (`;`) nas legendas deste perfil. Preferir vírgula; se ela prejudicar a clareza ou a gramática, reescrever a frase ou usar ponto ou dois-pontos.

## Shows, apresentações e conteúdo misto

- Tratar músicas, falas de palco, orações, testemunhos e transições como tipos editoriais diferentes dentro do mesmo arquivo.
- No perfil aprovado deste projeto, todo cue começa com letra maiúscula normal: canto, fala, entrevista, oração, testemunho ou bastidor. Nunca converter toda a música para CAIXA ALTA.
- Legendar falas, perguntas, comandos e comentários com significado.
- Omitir aplausos, gritos indistintos, ruído, contagens técnicas e agradecimentos automáticos repetidos sem valor novo.
- Em orações e linguagem religiosa, preservar intenção, pessoa verbal e registro; não tornar a fala artificialmente formal.
- Mapear repertório e convidados antes de corrigir letras reconhecidas incorretamente.
- Em arquivos longos, salvar transcrição e tradução incrementalmente ou em lotes retomáveis.
- Durante o trabalho, usar amostras distribuídas para detectar problemas sistêmicos. Antes da entrega final criada do áudio ou vídeo, conferir todos os cues e seus limites.
- Encerrar no último conteúdo significativo, evitando legendas inventadas sobre silêncio, créditos ou plateia.

## Modos estruturais

- Somente SRT, sem a mídia correspondente: preservar IDs, tempos e quantidade por padrão; pedir autorização antes de redistribuir ou retimar.
- Filme ou série com vídeo e SRT original correspondente: usar recomposição adaptativa por padrão, tratando o SRT como texto e âncoras; preservar a grade 1:1 somente quando o usuário pedir.
- Legenda musical criada do áudio: criar, dividir, unir e retimar em favor do fraseado musical.
- Filme, série, documentário ou entrevista criado da mídia: seguir `audiovisual-dialogue-rules.md`; não aplicar timing musical.

## Validação final

- Conferir numeração sequencial, timestamps válidos e ausência de sobreposição.
- Conferir 2 linhas, 42 CPL, 17 CPS e o limite normal de 7,5 segundos. Em fala ou canto muito rápido, priorizar sincronização e condensar o texto antes de prolongar artificialmente o cue. Aceitar duração maior somente para unidade vocal indivisível confirmada, validada com `--allow-long-cue` e informada como exceção editorial.
- Conferir consistência dos refrões e do glossário.
- Conferir também pontuação e capitalização idênticas em repetições equivalentes.
- Conferir se toda reticência corresponde a pausa, hesitação, interrupção, falso começo ou continuidade deliberadamente omitida; remover reticências usadas apenas como cola entre cues.
- Revisar manualmente vozes sobrepostas, coros, ad-libs e trechos com baixa confiança.
- Em legenda criada da mídia, conferir individualmente `N/N entradas` e `N/N saídas`; usar vocal isolado em música e áudio mais imagem em audiovisual. Em SRT existente com timing preservado, investigar acusticamente as anomalias e manter os tempos aprovados.
- Em correção exclusiva de saída, informar `N/N entradas preservadas`, `N/N saídas revisadas` e a quantidade de saídas alteradas; qualquer mudança de entrada exige justificativa objetiva e comunicação explícita.
- Quando houver uma versão manual aprovada pelo usuário, comparar cue por cue e extrair padrões reutilizáveis de fidelidade, fraseado, densidade, ritmo e apresentação. Preservar suas fronteiras válidas em conteúdo comparável, mas não transformar em regra um corte dentro de palavra, uma antecipação ou um erro isolado de timing, tradução ou CPS.
- Conferir nomes próprios, cidades, convidados, títulos de músicas e termos religiosos.
- Conferir se algum cue contém palavras pertencentes ao cue anterior ou seguinte.
- Conferir que não restaram elementos SDH, nomes de falante, descrições sonoras ou símbolos musicais.
- O validador comprova estrutura e legibilidade, não a correção da letra ou da tradução. A entrega exige também revisão editorial e acústica.
- Informar na entrega o provedor usado e a contagem de limites conferidos. Não declarar sincronização concluída sem revisar todos os cues.
