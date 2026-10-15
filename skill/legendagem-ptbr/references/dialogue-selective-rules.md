# Diálogo seletivo, inclusive conteúdo adulto

## Objetivo

Criar uma legenda PT-BR limpa que preserve falas com significado e não trate vocalizações ou ruídos como diálogo.

Aplicar somente a material envolvendo adultos. Se a idade das pessoas for ambígua ou houver indicação de menores, interromper o processamento e pedir esclarecimento.

## O que manter

- Conversas, perguntas, respostas, acusações, explicações e comentários.
- Comandos e orientações que esclareçam ou mudem a ação.
- Falas em inglês, espanhol ou outro idioma com conteúdo semântico.
- Linguagem sexual explícita e palavrões com significado, preservando registro e intensidade sem censura automática.
- Consentimento, recusa, hesitação relevante, limites, dor, segurança, pedidos para parar ou continuar.
- Interrupções e repetições com função narrativa, emocional ou de consentimento.
- Nomes próprios, marcas e lugares sem tradução.

## O que omitir

- Gemidos, respiração, ofegos, beijos, gritos e vocalizações sem palavras.
- Música, efeitos, ruídos e qualquer descrição SDH, sem exceção neste projeto.
- Exclamações isoladas e repetitivas sem informação nova.
- Sequências redundantes de incentivo, confirmação ou reação.
- Reconhecimento incerto que não possa ser confirmado pelo contexto ou pelo áudio.
- Alucinações do ASR durante silêncio, ruído ou vocalizações.

Não inferir nem criar diálogo a partir de leitura labial, gestos, gemidos ou contexto visual.

## Seleção e tradução

- Selecionar pelo valor semântico, não pelo grau de explicitude.
- Não higienizar, suavizar ou moralizar a fala adulta.
- Traduzir naturalmente para PT-BR contemporâneo, mantendo o tratamento entre os falantes.
- Preservar o sentido de `no`, `stop`, `wait`, `slow down`, `yes` e outras falas ligadas a consentimento ou segurança, mesmo quando curtas.
- Omitir `yes`, `yeah`, `oh` e equivalentes somente quando forem reação repetitiva sem informação nova.
- Usar contexto anterior e posterior para resolver sujeito, intenção e referência, mas não deslocar texto entre tempos errados.

## Segmentação

- Iniciar exatamente na primeira palavra audível; nunca antecipar a entrada.
- Encerrar no fim da última palavra da fala selecionada. Admitir pequena permanência para leitura somente sem invadir a fala seguinte.
- Criar novo cue em troca de falante, frase completa, pausa relevante ou interrupção.
- Agrupar fragmentos do mesmo enunciado com `end_id`: o início vem do primeiro ID e o fim, do último.
- Remover cues independentes já cobertos por um grupo para impedir duplicação e sobreposição.
- Não fundir falas de pessoas diferentes apenas para reduzir a quantidade de cues.
- Quando houver fala simultânea, priorizar a fala inteligível e significativa; usar duas linhas com hífen simples somente se ambas forem necessárias e couberem.
- Usar hífen simples seguido de espaço (`- `), nunca travessão tipográfico, quando duas pessoas compartilharem o mesmo cue.
- Não exibir nomes, IDs ou rótulos de falantes. Voz fora de quadro também permanece sem identificação; usar apenas o texto falado e o contexto visual.

## Limites

- Máximo de 2 linhas.
- Máximo de 42 caracteres por linha.
- Meta de 17 caracteres por segundo.
- Duração máxima de 7,5 segundos.
- Sem sobreposição involuntária.
- Condensar com fidelidade antes de antecipar, prolongar artificialmente ou apagar informação importante.
- Descartar fragmentos subquadro sem janela útil somente quando forem redundantes ou não semânticos; não apagar consentimento, recusa ou segurança.

## Ferramentas

1. Gerar segmentos com `scripts/segment_scribe_dialogue.py`.
2. Revisar e selecionar IDs; usar `end_id` para falas que abrangem vários fragmentos.
3. Gerar o SRT com `scripts/build_selective_dialogue_srt.py`.
4. Usar `--audit-json` para conferir origem, IDs agrupados, duração e orçamento de caracteres.
5. Executar `scripts/validate_srt.py` e revisar no áudio todas as entradas e saídas selecionadas.

## Saída

- Preservar uma versão anterior.
- Informar que foi usado o modo de diálogo seletivo.
- Informar o que foi omitido por categoria, sem descrever conteúdo íntimo desnecessariamente.
- Confirmar que a saída não contém SDH, nomes de falante ou descrições sonoras.
- Não afirmar que a seleção está perfeita apenas porque o SRT passou na validação estrutural.
