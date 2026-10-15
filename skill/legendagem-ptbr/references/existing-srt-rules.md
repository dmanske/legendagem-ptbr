# Tradução e revisão de SRT existente

## Escolha do modo estrutural

- Com somente o SRT, preservar IDs, início, fim, ordem e quantidade de cues.
- Com filme ou série e SRT original da mesma versão, usar recomposição adaptativa por padrão: o SRT fornece texto e âncoras, mas a unidade de trabalho é a fala completa ou microcena.
- No modo adaptativo, permitir unir, dividir, criar, excluir limites internos e retimar cues quando áudio, interlocutor, pausa, leitura ou corte justificarem. Não apagar conteúdo verbal para reduzir a quantidade de cues.
- Preservar a estrutura 1:1 mesmo com a mídia quando o usuário pedir explicitamente para manter os tempos ou a grade original.
- Criar uma nova versão do arquivo; não sobrescrever silenciosamente o original.
- Se o usuário aprovar os tempos e pedir somente tradução ou quebra visual, os timestamps são imutáveis.

## Recomposição adaptativa com a mídia

- Confirmar que o SRT corresponde à versão, corte e faixa de áudio do arquivo. Comparar também com a faixa de legenda interna limpa quando existir.
- Reconstruir sentenças e turnos completos antes de traduzir. Traduzir a intenção completa e só depois desenhar os cues em PT-BR.
- Usar os timestamps originais como pontos de busca. Decidir limites finais pelo começo e fim audível da fala, troca de pessoa, pausa, interrupção, leitura e corte de cena.
- Ao unir cues, usar como intervalo externo o começo do primeiro e o fim do último, ajustando-os somente com evidência audiovisual.
- Ao separar ou deslocar uma fronteira interna, usar timestamps por palavra, fala audível ou pausa confirmada. Nunca repartir o tempo proporcionalmente pela quantidade de caracteres traduzidos.
- Não reunir falantes diferentes. Duas falas curtas podem compartilhar um cue apenas segundo as regras de diálogo duplo.
- Auditar todos os IDs-fonte como cobertura: cada trecho verbal precisa aparecer exatamente uma vez na sequência recomposta, ainda que a numeração e a quantidade finais sejam diferentes.
- Comparar a versão recomposta com a preservada por indicadores objetivos: fragmentos sintáticos, flashes, CPS, duração, quebras, continuidade e ausência de texto inventado.

## Tradução em lotes

- Traduzir em lotes de aproximadamente 10 a 20 cues.
- Enviar até 3 cues anteriores e 3 posteriores como contexto quando isso ajudar.
- Traduzir somente os IDs-alvo; contexto não deve reaparecer na saída.
- No modo 1:1, exigir os mesmos IDs, na mesma ordem e sem duplicatas. No modo adaptativo, manter internamente o vínculo com todos os IDs-fonte, embora a numeração final possa mudar.
- Rejeitar respostas malformadas, tentar novamente e reduzir o lote se necessário.
- Manter memória de tradução para frases repetidas, mas permitir mudança quando o contexto realmente alterar o sentido.
- Usar glossário como orientação contextual, não como substituição mecânica que produza português errado.

## Continuidade entre cues

- Detectar frases que continuam em cues vizinhos por pontuação, conectores, palavras funcionais e intervalo curto.
- Usar a continuidade para compreender a sentença inteira.
- No modo 1:1, manter a saída por ID e não mover palavras automaticamente entre cues.
- No modo adaptativo, redistribuir somente unidades semânticas completas dentro da mesma fala ou microcena, apoiando cada nova fronteira no áudio e na imagem.

## Smart Rebalance sem a mídia

Tratar Smart Rebalance como modo opcional quando não houver acesso ao áudio ou vídeo. Ele melhora a composição textual, mas não substitui a recomposição audiovisual.

Quando explicitamente solicitado:

- Preservar IDs, tempos, ordem, quantidade e conteúdo lexical combinado.
- Mover somente blocos semânticos completos entre cues da mesma sentença.
- Não acrescentar, apagar, resumir ou parafrasear.
- Recalcular as quebras internas depois da redistribuição.
- Rejeitar o resultado se a melhoria não for clara ou se qualquer restrição falhar.

## Contexto de filme ou série

Executar `source-verification-rules.md` quando a obra puder ser identificada.
Quando disponíveis, usar título, título original, ano, gênero, sinopse, personagens e relações como contexto interpretativo.

- O texto explícito do SRT e o diálogo local têm prioridade.
- Contexto externo resolve ambiguidades, mas não autoriza invenção.
- Confirmar nomes próprios, cargos, lugares e termos recorrentes.

## Limpeza e estilo

- Produzir PT-BR natural e contemporâneo.
- Iniciar todo cue com letra maiúscula normal, mesmo quando ele continuar uma frase do cue anterior. Não converter o texto inteiro para CAIXA ALTA.
- Preservar intensidade, palavrões e linguagem explícita sem censura automática.
- Produzir somente legenda limpa neste projeto. Remover marcações CC/SDH, nomes de falante, música, efeitos, ruídos, símbolos musicais e descrições entre colchetes ou parênteses.
- Quando um cue misturar fala e marcação SDH, preservar e traduzir a fala; remover apenas a marcação.
- Preservar texto visível na imagem somente quando for indispensável à narrativa e não estiver repetido no diálogo.
- Remover hesitações vazias; manter hesitação com função dramática ou narrativa.
- Usar hífen simples seguido de espaço (`- `) em diálogo duplo no mesmo cue.
- Não copiar as quebras do inglês; recalcular com sintaxe portuguesa.
- Remover ponto e vírgula (`;`) do texto final. Preferir vírgula quando natural; caso contrário, reescrever ou usar ponto ou dois-pontos.

## Quebras visuais

- Máximo de 2 linhas e 42 caracteres por linha.
- Permitir duas linhas mesmo quando o texto inteiro couber em uma, desde que a divisão semântica melhore claramente o equilíbrio e a apresentação profissional.
- Meta de 15 CPS, máximo rígido de 17 CPS e duração máxima de 7,5 segundos, sem alterar tempos já aprovados.
- Não separar artigo e substantivo, preposição e complemento, negação e verbo, pronome clítico e verbo, auxiliar e verbo, nome próprio ou expressão fixa.
- Preferir oração, vírgula, conjunção, pausa e bloco semântico.
- Evitar palavras fracas no fim da linha.
- Quando houver duas linhas, preferir a linha inferior igual ou maior que a superior apenas depois de preservar sintaxe e unidades semânticas. Em diálogo duplo, manter cada falante em sua própria linha mesmo quando essa proporção não for possível.
- Sintaxe e naturalidade têm prioridade sobre a forma visual.
- Não alterar palavras quando a tarefa for somente refazer quebras de linha.

## Validação

- No modo 1:1, conferir que IDs, tempos, ordem e quantidade permanecem idênticos ao original.
- No modo adaptativo, conferir que todo conteúdo verbal dos IDs-fonte aparece exatamente uma vez, na ordem narrativa correta, e que a saída tem numeração sequencial, tempos válidos e nenhum limite sem sustentação audiovisual.
- Conferir 2 linhas, 42 CPL, CPS, duração e ausência de sobreposição.
- Conferir pontuação, nomes, contexto, coerência entre falantes e consistência terminológica.
- Conferir que não restaram elementos SDH ou nomes de falante.
- Validação estrutural não comprova qualidade de tradução; revisar o texto inteiro. Se os tempos forem preexistentes e imutáveis, investigar acusticamente somente anomalias objetivas.
