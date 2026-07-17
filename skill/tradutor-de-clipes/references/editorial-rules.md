# Regras editoriais consolidadas

## Hierarquia

1. Fidelidade ao sentido e ao contexto musical.
2. Sincronização com fraseado, respiração e pausas vocais.
3. Naturalidade do português brasileiro.
4. Legibilidade e velocidade de leitura.
5. Integridade sintática e semântica das linhas.
6. Equilíbrio visual.

## Tradução

- Traduzir sentido e emoção, não a ordem literal do inglês.
- Manter nomes próprios, marcas e lugares.
- Preservar intensidade de linguagem sem censura automática.
- Aplicar terminologia religiosa consistente: Lord → Senhor; grace → graça; mercy → misericórdia; praise → louvor; worship → adoração.
- Traduzir versos e refrões repetidos de forma idêntica, salvo mudança clara de contexto.
- Usar registro bíblico ou contemporâneo de forma consistente conforme a obra.
- Não inventar palavras em trechos incertos; sinalizar incerteza para revisão.

## Cues e sincronização musical

- Tratar cada frase cantada ou unidade respiratória como candidato a cue próprio.
- Dividir antes e depois de pausas vocais perceptíveis, mesmo com instrumental contínuo.
- Não reunir repetições executadas em momentos diferentes apenas para reduzir a quantidade de cues.
- Entrar exatamente na primeira sílaba detectada, sem antecipar a legenda. Usar `cue.start = primeira_palavra.start` como padrão.
- Antecipar a entrada somente quando o usuário pedir explicitamente; nunca aplicar lead-in negativo por padrão.
- Ao alinhar a entrada exata, encurtar a saída do cue anterior quando necessário e preservar pelo menos 80 ms entre cues.
- Sair próximo da última palavra, admitindo pequena folga de leitura que não invada o cue seguinte.
- Evitar cue superior a 7,5 segundos; versos sustentados podem exigir divisão editorial.
- Evitar flashes muito curtos; condensar tradução quando o original for cantado rapidamente.
- Não usar detector de silêncio como única evidência em música.

## Linhas

- Máximo de 2 linhas e 42 caracteres por linha.
- Meta máxima de 17 caracteres por segundo.
- Preferir uma linha quando a frase for curta.
- Nunca quebrar artigo + substantivo, preposição + complemento, negação + verbo, pronome + verbo, auxiliar + verbo, nome próprio ou expressão fixa.
- Preferir quebra em limite de oração, pausa, vírgula, conjunção ou bloco semântico.
- Evitar palavras fracas no fim da linha: de, do, da, e, que, um, uma.
- Usar pirâmide tradicional, linha superior igual ou maior, somente quando isso não prejudicar sintaxe ou ritmo.

## Limpeza

- Remover marcações CC não essenciais e símbolos musicais.
- Manter e traduzir sons indispensáveis à compreensão quando a legenda for inclusiva.
- Remover hesitações sem valor; traduzir confirmações com valor narrativo.
- Normalizar reticências e travessões sem apagar pausas dramáticas reais.

## Modos estruturais

- SRT existente: preservar IDs, tempos e quantidade por padrão; pedir autorização para retimar quando necessário.
- Legenda criada do áudio: criar, dividir, unir e retimar livremente em favor do fraseado musical.

## Validação final

- Conferir numeração sequencial, timestamps válidos e ausência de sobreposição.
- Conferir 2 linhas, 42 CPL, 17 CPS e 7,5 segundos.
- Conferir consistência dos refrões e do glossário.
- Revisar manualmente vozes sobrepostas, coros, ad-libs e trechos com baixa confiança.
