---
name: legendagem-ptbr
description: Criar, transcrever, pesquisar, traduzir, revisar, sincronizar e validar legendas SRT profissionais em portugues brasileiro, sem SDH, para clipes, musicas, shows, filmes, series, documentarios, entrevistas e dialogos. Usar com audio, video ou SRT existente, inclusive para recomposicao audiovisual, dialogo seletivo e correcao precisa de entradas e saidas.
---

# Legendagem Profissional PT-BR

Criar legendas PT-BR limpas a partir de audio, video ou SRT existente. Aplicar
fraseado musical a canções e timing audiovisual a diálogos. Preservar versões
anteriores e entregar um SRT validado, sem elementos SDH.

Antes de agir, ler integralmente `references/editorial-rules.md`. Antes de qualquer
tradução ou revisão textual, ler também
`references/contextual-translation-workflow.md`. Ler ainda a referência do modo
escolhido:

- Obra identificável, com acesso a fontes externas: ler `references/source-verification-rules.md`.
- Clipe musical ou apresentação musical curta: ler `references/music-clean-rules.md`.
- Show longo: permanecer em `references/editorial-rules.md`; aplicar `references/music-clean-rules.md` somente às músicas quando o usuário pedir o perfil limpo.
- Filme, série, documentário, entrevista ou diálogo completo criado da mídia: ler `references/audiovisual-dialogue-rules.md`.
- Diálogo seletivo, inclusive conteúdo adulto: ler `references/dialogue-selective-rules.md`.
- Tradução ou revisão de SRT existente: ler `references/existing-srt-rules.md`.

As regras formam um conjunto: não aplicar apenas limites técnicos e ignorar contexto, fraseado, integridade estrutural ou revisão editorial.

Neste projeto, toda saída é legenda limpa. Não criar nem preservar SDH: omitir
nomes de falante, efeitos, música incidental, ruídos, vocalizações não verbais e
descrições entre colchetes ou parênteses. Texto visível na imagem pode ser
legendado somente quando for indispensável à narrativa; isso não é SDH.

## Fluxo obrigatório

1. Confirmar o arquivo e inspecionar faixas de áudio e legenda, idiomas, duração, codec e volume com `ffprobe` e `ffmpeg`.
2. Se não houver áudio útil, solicitar letra, transcrição ou arquivo com áudio. Não inferir letra por leitura labial.
3. Identificar o modo: clipe musical, show longo com músicas e falas, audiovisual completo criado somente da mídia, filme ou série com SRT-fonte correspondente, diálogo seletivo ou tradução de SRT sem a mídia. Ler a referência específica e não aplicar automaticamente a estrutura de um modo a outro.
4. Detectar ferramentas de transcrição. Usar ElevenLabs Scribe v2 quando a chave estiver configurada e o usuário tiver autorizado esse fluxo. Neste projeto, o pedido para legendar uma mídia autoriza o uso da chave ElevenLabs já configurada pelo proprietário. Não usar Whisper, Faster-Whisper nem outro transcritor local como fallback automático: se a ElevenLabs falhar, estiver sem credencial ou indisponível, interromper o fluxo e avisar antes de produzir qualquer legenda alternativa. Em música solo, não usar diarização; em filmes, séries, entrevistas e falas com várias pessoas, ativá-la apenas para análise interna. Nunca exibir IDs ou nomes produzidos pela diarização.
5. Quando houver somente o vídeo, transcrever a faixa inteira e salvar a resposta bruta antes da edição. Em filme ou série, usar timestamps por palavra e diarização apenas internamente para mapear falas, pausas e trocas de interlocutor. Quando também houver um SRT original da mesma versão, confirmá-lo contra a faixa de áudio e tratá-lo como referência textual e conjunto de âncoras, sem retranscrever a obra inteira quando ele for confiável. Em música, não depender apenas de VAD ou silêncio, pois o instrumental continua durante pausas vocais. Em mídia longa, reutilizar resultados já salvos e dividir o trabalho em partes retomáveis quando necessário, sem perder o contexto nas bordas.
6. Auditar timestamps por palavra e reprocessar somente janelas com duração inválida, palavras comprimidas, timestamps duplicados ou sequências impossíveis. Em música, tratar como anomalia provável uma palavra final cuja duração se estenda de modo desproporcional pela reverberação, pelo instrumental ou até o fim da mídia; reprocessar uma janela local que inclua contexto antes e depois e separar o fim vocal da cauda sonora. Manter o resultado original quando a nova evidência não for melhor e nunca encurtar uma nota realmente sustentada.
7. Quando a obra for identificável e houver acesso a fontes, executar `references/source-verification-rules.md`. Revisar a transcrição contra letra, roteiro, legenda original, nomes, contexto e referências confirmadas. A execução audível determina o que foi dito ou cantado; ASR e fontes externas são evidências auxiliares.
8. Antes de traduzir, reconstruir unidades originais semanticamente completas e agrupá-las em blocos de contexto: estrofe, refrão ou ponte em música; troca completa, microcena ou tópico em diálogo. Um cue pode ser gramaticalmente completo e ainda depender do bloco para definir imagem, intenção e escolha verbal. Nunca decidir sua tradução isoladamente.
9. Em música, marcar primeiro as células cantadas no idioma original antes de distribuir a tradução. Em audiovisual falado, mapear falantes, frases, pausas e trocas de cena antes de criar cues. Diarização auxilia essa análise, mas não aparece no SRT.
10. Quando este fluxo for executado por um agente Codex, o próprio agente deve fazer a tradução editorial para PT-BR; não delegar automaticamente a tradução à Lovable ou a outro modelo. Executar integralmente `references/contextual-translation-workflow.md`: criar o briefing contextual, compreender e traduzir cada bloco antes de reencaixar seus cues, tratar expressões de risco com alternativas internas e aplicar a revisão de naturalidade e coerência do bloco. Preservar sentido, agente, tempo, lugar, intensidade, escopo, emoção, duplo sentido, registro religioso e motivos recorrentes. Não resumir apenas para produzir uma frase mais curta ou elegante. Usar Lovable somente no aplicativo automático, em lotes longos ou quando o usuário pedir explicitamente.
11. Antes da tradução editorial, consultar o acervo final aprovado pelo usuário como memória textual, de estilo e de escolhas recorrentes. Uma versão manual aprovada também calibra a densidade e o ritmo dos cues em conteúdo comparável. Descartar cortes dentro de palavras, antecipações, quebras artificiais e violações técnicas dos exemplos; aprender com as escolhas válidas sem universalizar um erro isolado. Uma tradução manual aprovada pelo usuário prevalece sobre qualquer alternativa automática.
12. Criar cues conforme o modo. Em música, iniciar na primeira sílaba e encerrar no fim audível da voz ou da nota sustentada. Em filme ou série com vídeo e SRT original, aplicar recomposição adaptativa por padrão: reconstruir falas completas, traduzir a unidade e somente depois unir, dividir, redistribuir ou retimar os cues conforme o áudio, a troca de falante, a leitura e os cortes. O SRT-fonte é âncora, não grade imutável. Em vídeo sem SRT, criar a segmentação natural a partir da transcrição e da imagem. Em trailer, clipe narrativo, entrevista curta ou conteúdo promocional misto, preservar mudanças reais de emissão, pausa, plano e ênfase; quando houver uma grade manual aprovada, manter sua quantidade e estratégia de divisão sempre que tecnicamente válidas e corrigir fronteiras com o menor deslocamento possível. Seguir `references/audiovisual-dialogue-rules.md` e não aplicar tolerâncias musicais mecanicamente a filmes e séries.
13. Adaptar a tradução a cada célula musical ou cue audiovisual já marcado. Depois de qualquer divisão, recalcular CPS em cada parte. Entre 15 e 17 CPS, revisar, mas preferir a versão semanticamente completa quando ela couber em até duas linhas de 42 caracteres. Condensar somente para resolver uma restrição real de leitura ou limite rígido, retirando primeiro redundâncias e hesitações sem valor; nunca apagar agente, negação, tempo, lugar, intensidade, escopo ou imagem, nem antecipar, prolongar artificialmente ou reagrupar unidades distintas apenas para passar na validação.
14. Em shows, tratar músicas e falas separadamente: músicas seguem fraseado; falas seguem unidades naturais de diálogo. Preservar conteúdo verbal significativo e omitir aplausos, ruídos, música incidental, vocalizações não verbais e alucinações do reconhecedor.
15. Salvar em `legendas/<nome-base-da-midia>.srt`: preservar exatamente o nome do arquivo de vídeo ou áudio — incluindo acentos, espaços, maiúsculas, pontuação e parênteses — e trocar somente a extensão final por `.srt`. Nunca acrescentar `.pt-BR`, código de idioma, `traduzido` ou qualquer outro sufixo. Se o destino exato já existir, não sobrescrever silenciosamente: criar uma versão segura, como `.v2.srt`, salvo quando o usuário autorizar expressamente a substituição.
16. Executar `scripts/validate_srt.py` e corrigir todas as violações antes da entrega. O validador também rejeita marcações SDH, símbolos musicais, rótulos de falante e estilos de cor ou posição. Escolher uma ou duas linhas pela melhor composição visual e pela leitura mais profissional, inclusive quando o texto couber inteiro em uma linha; preservar primeiro a sintaxe e os blocos semânticos. Aplicar meta de 15 CPS e limites rígidos de 42 CPL e 17 CPS. Usar 7,5 segundos como limite normal de duração, mas registrar com `--allow-long-cue` uma exceção confirmada quando uma única fala, palavra ou nota sustentada ultrapassar esse tempo e não puder ser dividida sem cortar conteúdo ainda audível.
17. Em legenda criada somente do áudio ou vídeo e em SRT recomposto com a mídia, revisar o início e o término de todos os cues, sem amostragem, e contabilizar `N/N entradas` e `N/N saídas`. Auditar também a cobertura do SRT-fonte para provar que nenhuma fala migrou, sumiu ou foi duplicada. Em SRT sem a mídia ou com timing expressamente preservado, conferir identidade estrutural e investigar somente anomalias objetivas. Em todos os modos, conferir fonte, tradução, nomes, continuidade, contexto e ausência de SDH. Validação estrutural não prova sincronização nem qualidade editorial.

## Diálogo seletivo

- Manter conversas, perguntas, respostas, comandos, explicações e comentários com significado.
- Em conteúdo adulto, preservar linguagem sexual explícita, palavrões, consentimento, recusa, limites e orientações com o mesmo sentido e intensidade, sem censura automática.
- Omitir gemidos, respiração, beijos, gritos não verbais, ruídos, música e reações repetitivas sem informação nova.
- Nunca transformar vocalização incerta em diálogo inventado.
- Iniciar na primeira palavra do primeiro fragmento selecionado e encerrar na última palavra do último fragmento agrupado.
- Usar `end_id` quando uma mesma fala abranger vários fragmentos do reconhecedor; remover duplicatas cobertas pelo grupo.
- Executar `scripts/segment_scribe_dialogue.py` para criar segmentos de diálogo a partir do Scribe e `scripts/build_selective_dialogue_srt.py` para gerar o SRT revisado.

## Decisões editoriais

- As regras abaixo sobre primeira sílaba, nota sustentada, ataques e células melódicas aplicam-se a música. Para filmes, séries, documentários e entrevistas, `references/audiovisual-dialogue-rules.md` prevalece no timing.
- Para SRT pronto sem acesso à mídia correspondente, preservar IDs e timing por padrão. Quando filme ou série e SRT original forem fornecidos juntos, usar recomposição adaptativa por padrão; preservar 1:1 somente quando o usuário pedir explicitamente.
- Para legenda criada do áudio, permitir criar, dividir, unir e retimar cues para acompanhar o cantor.
- Quando o usuário aprovar os inícios e fins e pedir somente tradução, pontuação ou quebra visual, preservar todos os timestamps. Não retimar sem pedido ou necessidade explicitamente informada.
- Quando o usuário aprovar as entradas e apontar somente saídas longas, tratar a revisão como correção exclusiva de saída: preservar IDs, texto, quebras e todos os `cue.start` exatamente; alterar apenas `cue.end`, salvo sobreposição ou timestamp inválido que precise ser informado. Comparar antes e depois e relatar `N/N entradas preservadas`, `N/N saídas revisadas` e quantas saídas mudaram.
- Ao revisar um SRT existente, nunca sobrescrever silenciosamente o original; criar versão identificável e informar exatamente o que mudou.
- Tratar o timestamp por palavra como ponto de busca, não como verdade final. Conferir no vocal isolado a primeira sílaba em uma janela local e ajustar cada cue individualmente; nunca corrigir uma música inteira com deslocamento global quando os erros variam.
- Usar entrada exata como padrão: `cue.start = primeira_silaba_audivel`. Não aplicar lead-in negativo nem antecipar a legenda, salvo pedido explícito do usuário.
- Buscar como alvo uma entrada entre 0 e 80 ms depois do ataque vocal detectado; qualquer valor anterior à primeira sílaba é falha de sincronização.
- Usar intervalo adaptativo de 0 a 80 ms. Permitir 0 ms quando o canto for contínuo; preservar a pausa real quando houver respiração. Nunca permitir sobreposição involuntária.
- Encerrar no fim audível da voz, incluindo vogais e notas sustentadas. Não depender de cauda fixa após o término lexical do reconhecedor.
- Preferência fixa do usuário: o cue deve desaparecer quando terminar o último som vocal audível. Nunca prolongar a saída para aumentar o tempo de leitura e nunca encurtá-la para satisfazer duração máxima enquanto ainda houver fala, sílaba ou nota sustentada. Uma tolerância técnica de medição não é uma cauda editorial.
- Buscar como alvo a saída no último som vocal audível. Não prolongar a legenda por causa do instrumental nem cortá-la no timestamp lexical do Scribe.
- Usar o término da última palavra no Scribe como ponto inicial da busca pela saída. Se piano, reverb, harmônicos ou acompanhamento mascararem o fim da voz no mix completo, preferir esse limite de base; estender além dele somente quando houver evidência auditiva de vogal ou nota vocal sustentada, idealmente no vocal isolado. Energia no espectrograma do mix completo não prova, sozinha, continuidade vocal.
- Dividir frases longas em unidades cantadas curtas quando a cadência indicar retomada, ainda que o reconhecedor não registre silêncio entre as palavras.
- Distinguir quebra visual de novo cue: usar duas linhas quando a voz for contínua; criar outro cue quando houver nova célula melódica, emissão, ataque vocal ou retomada de cadência.
- Preferir um cue curto por célula cantada. Não usar uma legenda de duas linhas para representar duas emissões vocais sucessivas apenas porque o texto cabe na tela.
- Ao separar um cue longo, mapear o começo de cada parte à primeira sílaba da célula correspondente e o fim ao último som dessa célula; não repartir o tempo proporcionalmente pelo tamanho do texto traduzido.
- Depois de qualquer divisão manual ou automática, verificar se o primeiro fragmento ainda começa na primeira palavra da frase original. Nunca atrasar uma tradução que representa a frase inteira para fazê-la coincidir apenas com suas palavras finais.
- Ao refinar apenas a segmentação de uma frase já aprovada, preservar o início externo e o fim externo; inserir somente os limites internos confirmados no vocal.
- Permitir que a divisão musical separe blocos sintaticamente ligados quando a execução os cantar em células diferentes; sincronização e fraseado prevalecem sobre a preferência de manter a expressão no mesmo cue.
- Reutilizar a mesma segmentação textual em versos e refrões repetidos, mas realinhar cada ocorrência à execução correspondente.
- Separar falas, comandos e ad-libs da letra principal; usar itálico quando essa distinção for editorialmente útil.
- Em qualquer perfil deste projeto, iniciar todo cue com letra maiúscula normal, mesmo quando ele continuar uma frase do cue anterior. Nunca converter toda a legenda para CAIXA ALTA.
- Não usar ponto e vírgula (`;`) no texto exibido. Preferir vírgula quando ela preservar o ritmo e o sentido; quando a vírgula produzir ambiguidade ou ligação inadequada, reescrever ou usar ponto ou dois-pontos.
- Em clipes musicais, aplicar também o perfil limpo: omitir vocalizações isoladas sem conteúdo semântico, sem omitir palavras ou repetições com sentido.
- No perfil de clipe aprovado, omitir pontuação terminal automática nas células cantadas comuns. Preservar somente a pontuação com função semântica ou prosódica real, como `?`, `!`, dois-pontos e vírgula interna ou terminal indispensável.
- Tratar vocais secundários de forma explícita: preservá-los quando tiverem conteúdo ou função musical relevante, separá-los da voz principal e usar itálico quando ajudar. Omiti-los somente em modo de legenda limpa solicitado pelo usuário ou quando forem interjeições sem conteúdo.
- Priorizar fraseado e sintaxe; usar equilíbrio visual apenas como desempate. Nunca copiar mecanicamente a quebra visual do inglês para o português.
- Quando houver duas linhas, preferir a linha inferior igual ou maior que a superior, sem sacrificar sintaxe, fraseado ou legibilidade. Em diálogo duplo, manter um falante por linha mesmo quando os comprimentos não obedecerem a essa forma visual.
- Não agrupar repetições cantadas em momentos diferentes dentro de um cue longo.
- Usar timestamps por palavra como evidência inicial; revisar no vocal isolado trechos com canto sustentado, vozes sobrepostas, respirações omitidas ou reconhecimento instável.
- Manter texto e pontuação idênticos em todas as repetições equivalentes depois que uma forma for aprovada.
- Não deixar a tradução migrar entre momentos da fala. No modo 1:1, se um bloco traduzido contém parte do cue seguinte, corrigir a segmentação e traduzir novamente. Na recomposição adaptativa, mover somente unidades semânticas completas dentro da mesma fala ou microcena e auditar a cobertura combinada da fonte.
- Não considerar um SRT pronto apenas porque passou no validador. Conferir letra, nomes próprios, cidades, ordem do repertório, refrões e amostras acústicas.
- Depois do último cue reconhecido, examinar o vocal até o final da mídia. Preservar refrões, repetições e despedidas audíveis omitidos pelo ASR.
- Não alterar um limite vocal correto para satisfazer CPS. Condensar o português; sincronização de entrada e saída prevalece.

## Shows longos

- Extrair uma faixa de trabalho compacta, mono, preservando o áudio original intacto.
- Produzir transcrição incremental em JSONL ou em partes, para que o progresso sobreviva a falhas e possa ser auditado.
- Mapear repertório, convidados, falas e transições antes da tradução. Usar fontes oficiais ou referências fornecidas pelo usuário quando disponíveis.
- Criar cues-fonte em pontuação, pausas e limites semânticos. Um corte mecânico por quantidade de caracteres pode antecipar a oração seguinte.
- Traduzir em lotes com contexto anterior e posterior, mas exigir correspondência exata de IDs. Rejeitar e refazer lotes com IDs ausentes, duplicados ou conteúdo deslocado.
- Condensar somente os cues que excederem o tempo real de leitura. Não compensar fala rápida antecipando a entrada.
- Revisar manualmente músicas conhecidas contra traduções aprovadas e revisar falas longas por amostragem distribuída.
- Encerrar no último conteúdo significativo. Não manter alucinações de ASR geradas sobre aplausos, créditos ou silêncio.

## Segurança e serviços externos

- Nunca gravar chaves de API, tokens ou senhas no repositório, nos prompts, nas legendas ou nos logs.
- Antes de enviar áudio ou vídeo a um serviço externo, confirmar que o usuário autorizou esse envio. A seleção explícita de ElevenLabs ou a regra permanente já aprovada neste projeto conta como autorização. Transcrição local deve permanecer local.
- No trabalho interativo do Codex, traduzir editorialmente no próprio contexto do agente. Não enviar o texto à Lovable por padrão.
- Quando a Lovable for usada pelo aplicativo, por lote longo ou por pedido explícito, informar essa diferença com clareza e fazer revisão editorial antes da entrega.
- As chaves Lovable e ElevenLabs devem ser configuradas localmente em cada computador, preferencialmente no gerenciador de credenciais do sistema ou em variáveis de ambiente ignoradas pelo Git.

## Recursos

- `scripts/transcribe_scribe_v2.py`: transcrição principal pelo ElevenLabs Scribe v2 usando `ELEVENLABS_API_KEY`.
- `scripts/segment_scribe_dialogue.py`: transforma palavras do ElevenLabs Scribe em fragmentos de diálogo.
- `scripts/build_selective_dialogue_srt.py`: monta o SRT seletivo com suporte a `end_id`, edições e auditoria.
- `scripts/validate_srt.py`: valida estrutura, sobreposição, CPL, CPS, duração e ausência de SDH.
- `references/editorial-rules.md`: padrão consolidado de tradução e sincronização.
- `references/contextual-translation-workflow.md`: briefing, tradução por unidades semânticas e revisão contextual em PT-BR.
- `references/source-verification-rules.md`: pesquisa de letra, versão, obra, personagens e hierarquia de evidências.
- `references/music-clean-rules.md`: capitalização, fidelidade, layout e remoção de vocalizações em clipes.
- `references/audiovisual-dialogue-rules.md`: filmes, séries, documentários e entrevistas sem SDH.
- `references/dialogue-selective-rules.md`: seleção editorial para diálogos, inclusive vídeos adultos.
- `references/existing-srt-rules.md`: tradução, contexto e reformatação segura de SRT existente.

## Entrega

Informar o arquivo criado, quantidade de cues, validações executadas e incertezas relevantes. Fornecer link local clicável para o SRT.
