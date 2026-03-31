---
name: paulo-estilo-juridico
description: >
  Skill de escrita juridica no estilo de Paulo Moukarzel. Use SEMPRE que o usuario
  pedir para redigir, elaborar, revisar, corrigir, formatar ou automatizar peticoes,
  pecas juridicas, recursos, habeas corpus, contestacoes, alegacoes finais, memoriais,
  embargos, peticoes iniciais, replicas, agravos, mandados de seguranca, tutelas,
  contrarrazoes, impugnacoes ou qualquer outro documento juridico. Tambem ativar quando
  o usuario quiser gerar .docx de pecas ou revisar pecas existentes. Aplica o padrao de
  escrita, argumentacao e estrutura extraido das pecas reais do advogado Paulo Moukarzel
  Junior.
  Triggers: "elaborar peticao", "redigir peca", "fazer recurso", "escrever contestacao",
  "habeas corpus", "alegacoes finais", "memoriais", "embargos", "automatizar peticao",
  "no meu estilo", "meu padrao de escrita", "escreve como eu", "peticao juridica",
  "peticao inicial", "replica", "agravo", "mandado de seguranca", "tutela",
  "contrarrazoes", "impugnacao", "revisar peticao", "corrigir peca", "formatar peticao",
  "gerar docx", "documento juridico", "peca processual".
---

# Skill: Estilo Juridico de Paulo Moukarzel

Esta skill instrui como redigir pecas juridicas no estilo especifico do Dr. Paulo Ekke
Moukarzel Junior, com base na analise de 292 peticoes reais assinadas por ele (corpus de
3,1 milhoes de caracteres, atualizado em marco/2026).

Antes de redigir qualquer peca, leia o perfil de estilo detalhado em:
`./references/perfil-estilo.md`

---

## Principios Fundamentais

O estilo do Dr. Paulo Moukarzel e caracterizado por **sete marcas distintivas**:

1. **Fatos processuais em primeira mao (FONTES PRIMARIAS)**: NUNCA redigir com base em
   resumos, decisoes judiciais do processo atual ou alegacoes da parte contraria. Sempre
   ir aos documentos originais do processo (autos do processo de origem, peticoes, decisoes
   anteriores, certidoes, termos) e extrair fatos concretos com datas, numeros de evento
   e tipo de documento. Decisoes judiciais e peticoes adversarias podem estar desconexas,
   incompletas ou tendenciosas — o que importa sao os FATOS documentados nos autos.

2. **Cadeia documental robusta**: Cada alegacao factual deve ser respaldada por referencia
   a documento especifico. O formato PREFERENCIAL e por numero de evento do e-proc:
   "(evento N, TIPO)" ou "(evento N, TIPO — doc. 2)". Referencia a folhas ("fl. X" / "fls.
   X/Y") so deve ser usada de forma SUBSIDIARIA, quando nao houver informacao sobre o
   numero do evento correspondente. **Lista de documentos ao final da peca**: incluir
   "DOCUMENTOS QUE ACOMPANHAM ESTA [PECA]:" SOMENTE quando se tratar de peticao inicial
   ou quando os documentos juntados sejam NOVOS (i.e., ainda nao constam dos autos e nao
   possuem numeracao/evento no processo). Em recursos e pecas que se referem exclusivamente
   a documentos ja existentes nos autos, NAO incluir lista de documentos ao final — basta
   a referencia por evento ou folhas no corpo do texto. Em habeas corpus e RHCs, incluir
   "DOCUMENTOS QUE INSTRUEM ESTE MANDAMUS/RECURSO:" apenas quando houver documentos
   novos extraidos dos autos de origem que estejam sendo juntados pela primeira vez.

3. **Precisao Procedimental**: Sempre cita artigos de lei, numeros de evento dos autos
   (preferencialmente por evento do e-proc, subsidiariamente por folhas), timestamps de
   videos e documentos. Nunca e vago sobre fundamentos legais.

4. **Menos jurisprudencia, mais fatos**: Usar jurisprudencia apenas quando estritamente
   necessario (ex: 1 julgado para nulidade de clausula penal). O poder de convencimento
   vem dos FATOS processuais documentados, nao de citacoes doutrinarias ou jurisprudenciais
   em excesso. Fatos concretos e irrefutaveis valem mais que dezenas de ementas.

4A. **NUNCA incluir jurisprudencia sem confirmacao de autenticidade**: Antes de citar
   qualquer precedente (STJ, STF, TJSC ou outro tribunal), e OBRIGATORIO confirmar a sua
   existencia e autenticidade. O procedimento e:
   (a) se o precedente consta dos documentos fornecidos pelo Dr. Paulo ou das pecas dos
   autos, pode ser utilizado diretamente;
   (b) se o precedente foi encontrado via pesquisa (WebSearch), verificar numero, relator,
   data do julgamento e ementa no site oficial do tribunal antes de incluir na peca;
   (c) se nao for possivel confirmar a autenticidade do precedente por nenhuma dessas vias,
   NAO incluir na peca — em vez disso, perguntar ao Dr. Paulo se o julgado existe e se
   autoriza a sua utilizacao;
   (d) JAMAIS inventar, presumir ou "completar" dados de jurisprudencia (numero, relator,
   data, ementa). Se faltar qualquer dado, deixar em branco com marcador [PREENCHER] e
   alertar o Dr. Paulo.

5. **Exposicao de Contradicoes**: Estrategia retorica central: identificar inconsistencias
   da parte contraria ou da decisao recorrida e expo-las com precisao cirurgica.

6. **Formalidade Preservada**: Registro sempre formal e tecnico. Sem coloquialismos.
   Mantem formas de tratamento protocolar ("Vossa Excelencia", "Egregio", "Colendo", "Eminente").

6A. **Narrativa fatica OBJETIVA e CONCISA**: A secao de fatos deve ser narrada com maxima
   objetividade, sem floreios ou adjetivacao desnecessaria. Padrao:
   - **Crime/fato primeiro, processo depois**: "O paciente foi denunciado pela suposta
     pratica do crime de estupro de vulneravel (art. 217-A, caput, do Codigo Penal), com a
     causa de aumento do art. 226, inciso II, do Codigo Penal, em continuidade delitiva
     (art. 71, caput, do Codigo Penal) nos autos da acao penal n. XXXX" — e NAO:
     "O paciente RAFAEL DE MELO foi denunciado pelo Ministerio Publico do Estado de Santa
     Catarina, nos autos da acao penal n. XXXX, em tramite perante a Vara Criminal da
     Comarca de Florianopolis, pela suposta pratica..."
   - **Verbos no condicional** para fatos da acusacao: "teria praticado", "teria entrado",
     "supostamente cometeu" — marcando distanciamento da versao contraria.
   - **Formas IMPESSOAIS** para decisoes: "sobreveio decisao que indeferiu a liminar",
     "foi decretada a prisao preventiva", "sobreveio a sentenca ora recorrida" — NUNCA
     "o juiz decidiu", "o desembargador entendeu".
   - **Decisoes identificadas por evento**: "decisao proferida no evento 56", "evento 133,
     SENT1" — sem data, sem nome do magistrado.
   - **Transcricoes literais** de trechos da denuncia/decisao entre aspas, com referencia
     ao evento e pagina.
   - **Verbos de reporte para a parte contraria**: "argumentou", "aduziu", "sustenta",
     "narrou", "afirmou", "alega" — variacao lexical rica, sempre atribuindo a narrativa
     a parte adversa.

7. **Argumentacao incisiva, pro-cliente e baseada nos autos**: A argumentacao deve ser SEMPRE
   favoravel ao cliente e incisiva, com o objetivo de convencer o magistrado. Isso implica:
   (a) afastar as alegacoes da parte contraria com fatos e documentos dos autos que as derruam;
   (b) apontar contradicoes, omissoes e fragilidades das afirmacoes adversas;
   (c) fundamentar a posicao do cliente com referencias precisas aos autos (eventos, documentos,
   depoimentos, pericias); (d) nunca argumentar de forma abstrata ou generica — cada argumento
   deve ser ancorado em fato concreto extraido do processo; (e) reforcar a argumentacao com
   fundamentos legais (artigos de lei, codigos, legislacao especial) e jurisprudencia favoravel
   ao cliente (STJ, STF, TJSC), que confirmem a tese defendida e demonstrem que o direito
   ampara a posicao do cliente.

   **Tecnica de refutacao confirmada em 292 pecas**:
   - Abertura com formula de refutacao: "Sem razao, entretanto, [parte contraria]." (51x) /
     "Com a devida venia, Excelencia," (64x) / "Improcede [alegacao]" (28x)
   - Construcao pro-cliente: "E certo/evidente que" (104x) / "Como se sabe," (96x) /
     "Resta demonstrado/comprovado" (16x) / "Basta ver" (8x)
   - Escalada argumentativa (acumular golpes retoricos): "Mas nao e so." (118x) /
     "Nao fosse isso o suficiente," (46x) / "Nao bastasse," (25x) / "Alias," (202x)
   - Contraposicao direta: "Ocorre que," (82x) / "No entanto," (232x) / "Contudo," (167x)
   - Verbos no condicional para fatos da acusacao/parte contraria: "teria" (1.160x) /
     "supostamente" (80x)
   - Referencia direta ao juizo: "Como visto, Excelencia," / "Convem registrar, Excelencia, que"
   - Sequencia tipica: [Refuta tese adversa] → [Apresenta fato dos autos que a contraria] →
     [Fundamenta juridicamente] → [Conclui com "Portanto,"]

   **O que NAO fazer na argumentacao**:
   - NAO argumentar de forma abstrata, sem vincular a fatos concretos do processo
   - NAO usar teses genericas desconectadas dos autos — cada argumento = fato + documento
   - NAO usar jurisprudencia em excesso como substituto de fatos
   - NAO aceitar ou reproduzir acriticamente a narrativa da parte contraria
   - NAO ser tímido ou evasivo — a argumentacao e direta, incisiva e busca convencer

8. **Selecao estrategica de argumentos**: Priorizar argumentos FORTES e bem fundamentados
   no corpo principal da peca. Focar no argumento central e desenvolve-lo com profundidade
   factual. Argumentos menos eficazes NAO devem ser omitidos — devem ser incluidos ao final
   da peca, antes dos pedidos/requerimentos, sob o prefixo **"TESE SUBSIDIARIA"**, com breve
   descricao do argumento ou tese. Isso preserva a forca do argumento principal sem perder
   teses alternativas que o juiz possa acolher.

9. **NUNCA mencionar nomes de magistrados ou membros do MP que atuam no caso**: No corpo
   da peca, NAO referir pelo nome proprio juizes, desembargadores, ministros, promotores
   ou procuradores que atuam ou atuaram no processo em discussao. Referir-se SEMPRE pela
   funcao: "o Juiz sentenciante", "o Relator", "o Promotor de Justica", "o Desembargador
   Relator", "o Ministro Relator", "a autoridade coatora", "o orgao acusatorio". Isso
   torna o texto mais objetivo e com leitura mais fluida.
   **EXCECOES**: (a) no enderecamento formal da peca, quando o destinatario for ministro
   ou desembargador nomeado, pode-se usar o nome (exigencia protocolar); (b) em citacoes
   de jurisprudencia, SEMPRE incluir o nome do relator e a data do julgamento do
   precedente citado, pois sao de OUTROS processos e permitem conferencia de autenticidade.

9. **NUNCA mencionar o local de TRAMITACAO do processo**: NAO incluir comarca, vara, foro
   ou qualquer indicacao do juizo onde o processo tramita no corpo da peca. O processo deve
   ser identificado APENAS pelo numero (ex: "nos autos da acao penal n. XXXX"). NAO escrever
   "em tramite perante a Vara Criminal da Comarca de Florianopolis" ou similar.
   **EXCECOES**: (a) o enderecamento formal no cabecalho permanece obrigatorio; (b) o LOCAL
   DOS FATOS pode e deve ser mencionado — onde ocorreu o crime, onde se situava o imovel,
   onde aconteceram os eventos relevantes. Isso e essencial para detalhar a dinamica dos
   fatos apurados na demanda judicial. Ex: "na residencia da avo materna, no bairro Ribeirao
   da Ilha", "no terreno de heranca no bairro Jose Mendes, Florianopolis/SC".

10. **Evitar datas desnecessarias no corpo do texto**: Sentencas, acordaos e decisoes devem
    ser referenciados preferencialmente pela funcao e evento (ex: "a sentenca condenatoria",
    "o acordao recorrido", "a decisao do evento N"). **Datas DEVEM ser incluidas** quando: (a) forem
    importantes para explicar a dinamica dos fatos (ex: grande lapso temporal entre condutas);
    (b) forem utilizadas para fundamentar teses juridicas (prescricao, decadencia,
    intempestividade, contagem de prazos); (c) a cronologia for necessaria para demonstrar
    nulidade processual ou outra ilegalidade. Em resumo: datas sim quando contribuem para
    a argumentacao; datas nao quando sao meramente informativas e nao agregam.

11. **Sintese dos fundamentos da decisao recorrida na secao de fatos (OBRIGATORIO)**: Em
    TODOS os recursos (RHC, apelacao, agravo, RESE, AREsp/REsp, contrarrazoes, agravo
    interno) e em habeas corpus, a secao de fatos/sintese da demanda DEVE incluir um
    paragrafo que resuma, de forma objetiva e completa, os fundamentos da decisao recorrida
    ou do ato coator. O objetivo e permitir que o julgador compreenda, logo na leitura
    inicial, o que foi decidido e por que, para que a argumentacao subsequente faca sentido
    como contraposicao direta a esses fundamentos.
    **Formato**: O paragrafo deve iniciar com formula como "Em sintese, o acordao recorrido
    sustentou que" e desenvolver os fundamentos em TEXTO CORRIDO, conectados por expressoes
    como "No mesmo sentido,", "Quanto a [tema],", "Ademais,", "Por fim,", com referencia
    as folhas ou eventos correspondentes entre parenteses e transcricoes literais entre aspas.
    NUNCA enumerar os fundamentos com alineas (a/b/c), numerais romanos (i/ii/iii) ou
    qualquer outro marcador sequencial — a exposicao deve fluir em prosa continua.
    Encerrar com formula de transicao como "Como se demonstrara a seguir, nenhum desses
    fundamentos resiste ao confronto com os elementos dos autos."
    **EXCECAO**: Em embargos de declaracao, esta sintese NAO e necessaria — os EDs podem
    ser iniciados apontando diretamente os vicios (omissao, contradicao, obscuridade, erro
    material) da decisao embargada, sem necessidade de resumir previamente todos os seus
    fundamentos. Isso porque os EDs nao visam reformar a decisao, mas integra-la ou
    corrigi-la, de modo que a exposicao dos vicios ja contextualiza suficientemente o
    recurso. Em contestacoes e peticoes iniciais, esta regra tambem nao se aplica (nao
    ha decisao recorrida a sintetizar).

12. **NUNCA omitir argumentos de pecas anteriores do mesmo caso (OBRIGATORIO)**: Ao redigir
    recurso ou peca subsequente em caso que ja tenha pecas anteriores (_vf) na pasta de
    Clientes, TODOS os argumentos veiculados nas pecas anteriores devem ser mantidos e
    desenvolvidos na nova peca — SALVO se o argumento ja tiver sido expressamente restringido
    ou declarado prejudicado pela decisao do recurso imediatamente anterior (ex: tribunal que
    nao conheceu de determinada tese). Argumentos que foram rejeitados no merito, mas nao
    restringidos processualmente, devem ser reiterados e aprofundados. Em recursos sucessivos
    (ex: HC ao STJ → RHC ao STF), a nova peca deve: (a) manter todos os argumentos da peca
    anterior, adaptando-os ao novo destinatario e ao acrescimo de novos atos coatores;
    (b) acrescentar argumentos novos decorrentes dos vicios das decisoes posteriores;
    (c) incorporar argumentos auxiliares e reforcos retoricos que constam da peca anterior
    e que fortalecem a tese (ex: inversao do onus probatorio, exemplos hipoteticos, argumentos
    de senso comum). NUNCA reduzir o arsenal argumentativo em recurso subsequente — so ampliar.

13. **Demonstracao CONCRETA de fumus boni juris e periculum in mora em pedidos de liminar,
    tutela de urgencia, tutela de evidencia e tutela antecipada (OBRIGATORIO)**: Sempre que
    a peca contiver pedido liminar, tutela de urgencia (art. 300 CPC), tutela de evidencia
    (art. 311 CPC) ou tutela antecipada, a secao correspondente DEVE demonstrar, de forma
    CONCRETA e vinculada ao caso, os requisitos de fumus boni juris e periculum in mora.
    **O que e OBRIGATORIO**:
    (a) **Fumus boni juris**: Expor de forma resumida e REMISSIVA os argumentos centrais
    ja desenvolvidos no corpo da peca, vinculando-os aos fatos e documentos do caso concreto.
    Nao repetir a argumentacao, mas remeter as secoes onde foi desenvolvida (ex: "conforme
    demonstrado na secao II.1"). Incluir apenas os documentos-chave e trechos conclusivos.
    (b) **Periculum in mora**: Demonstrar CONCRETAMENTE o risco iminente ao cliente — tempo
    de prisao ja cumprido, dano irreversivel, cumprimento antecipado de pena, excesso de
    prazo, transito em julgado iminente. Fundamentar com dados concretos (datas, tempo de
    custodia, regime fixado vs. regime devido).
    (c) **Ausencia de periculum libertatis** (em HCs/RHCs): Demonstrar que o cliente nao
    oferece risco a ordem publica, a instrucao criminal ou a aplicacao da lei penal — citar
    primariedade, bons antecedentes, ausencia de vinculo com organizacao criminosa, instrucao
    ja encerrada, ausencia de elementos que indiquem reiteracao. Fundamentar com documentos
    concretos dos autos (certidao de antecedentes, por exemplo).
    **O que NUNCA fazer**: Paragrafos genericos ou abstratos que sirvam para qualquer caso.
    Cada argumento do fumus e cada fato do periculum devem ser especificos e ancorados nas
    circunstancias do caso.
    **Jurisprudencia e doutrina**: Podem acompanhar a fundamentacao do fumus/periculum,
    DESDE QUE: (i) a autenticidade seja confirmada (via site oficial do tribunal ou
    WebSearch); OU (ii) constem de peca anterior _vf ja elaborada e salva na pasta de
    Clientes. NUNCA inventar ou presumir precedentes para a secao de liminar.

> **APLICACAO UNIVERSAL**: Estes 7 principios se aplicam a TODOS os tipos de peca —
> habeas corpus, alegacoes finais, apelacao, agravo, replica, contestacao, memoriais,
> mandado de seguranca, RESE, contrarrazoes, peticao inicial e qualquer outra. As secoes
> "Por Tipo de Peca" abaixo detalham como cada principio se manifesta em cada tipo
> especifico, mas os principios NUNCA sao dispensados.

---

## Workflow Completo

### Passo 1 — Coletar Informacoes Minimas

Antes de redigir, certifique-se de ter:
- Nome completo do cliente (reu, apelante, paciente, autor, etc.)
- Tipo da peca e fase processual
- Tribunal/juizo destinatario (para o enderecamento formal — nome do magistrado destinatario
  APENAS se necessario para o cabecalho protocolar)
- Numero do processo (se disponivel)
- **Documentos originais do processo** — NAO resumos. Ler as pecas, decisoes e certidoes
  dos autos de origem para extrair fatos concretos com eventos e documentos
- Fundamentos juridicos ou tese pretendida
- Documentos/provas a mencionar (com eventos dos autos, se aplicavel)

> **LEMBRETE**: No corpo da peca, NUNCA incluir nomes de magistrados/promotores que atuam
> no caso (usar funcao: "o Juiz sentenciante", "o Relator") — mas SEMPRE incluir relator
> e data em citacoes de jurisprudencia. NUNCA incluir local de tramitacao (usar apenas
> numero do processo) — mas DEVE incluir local dos fatos (onde ocorreu o crime etc.).
> Evitar datas desnecessarias — mas incluir quando relevantes para dinamica dos fatos
> ou teses juridicas.

Se informacoes estiverem faltando, pergunte ao Dr. Paulo antes de comecar.

> **REGRA CRITICA**: Ao examinar documentos processuais, SEMPRE priorizar a leitura direta
> dos autos de origem (processo principal, inqueritos, PADs, inventarios etc.) em detrimento
> de resumos feitos pela parte contraria ou por decisoes do processo atual. A parte adversa
> pode omitir fatos relevantes ou distorce-los; decisoes judiciais de despachos iniciais
> podem reproduzir acriticamente alegacoes da parte autora. Ir ao DOCUMENTO ORIGINAL.

### Passo 1A — Consultar Pecas _vf Existentes do Mesmo Tipo (OBRIGATORIO)

Antes de redigir qualquer peca ou recurso, verificar se ja existe uma peca do MESMO
TIPO redigida pelo Dr. Paulo na pasta de Clientes:

```
C:\Users\paulo\OneDrive\Documentos\teste_IA\Clientes\
C:\Users\paulo\OneDrive\Documentos\M.Adv\Clientes\
```

Buscar arquivos com sufixo `_vf` (versao final) do mesmo tipo de peca (ex: `RHC_vf.docx`,
`Contestacao_vf.docx`, `Alegacoes_finais_vf.docx`, `HC_vf.docx`, `Apelacao_vf.docx` etc.).

**Se encontrar peca _vf do mesmo tipo**:
1. Ler o documento _vf na integra para extrair a **estrutura argumentativa** utilizada:
   secoes, ordem dos argumentos, forma de organizar a sintese da demanda, formato dos
   requerimentos/pedidos, forma de introduzir e encerrar cada secao.
2. **Replicar a estrutura argumentativa** na peca a ser redigida: mesma organizacao de
   secoes (ex: I – Sintese, II – Razoes com subsecoes, III – Tese adicional, TESE
   SUBSIDIARIA, IV – Liminar, V – Requerimentos), mesma forma de encadeamento dos
   argumentos, mesma tecnica de contrapor as decisoes recorridas.
3. O conteudo substantivo (fatos, provas, teses juridicas) sera evidentemente distinto
   para cada caso — o que deve ser identico e a ESTRUTURA e o PADRAO DE ORGANIZACAO
   da argumentacao.

**Se NAO encontrar peca _vf do mesmo tipo**: seguir os templates da secao "Por Tipo de
Peca" abaixo e o perfil de estilo em `./references/perfil-estilo.md`.

> **IMPORTANTE**: A consulta a pecas _vf existentes prevalece sobre os templates genericos
> da skill. Se o Dr. Paulo ja redigiu um RHC de determinada forma, todos os RHCs futuros
> devem seguir essa mesma estrutura argumentativa. Isso garante consistencia no padrao de
> trabalho do escritorio.

### Passo 2 — Consultar Referencia de Estilo

Leia `./references/perfil-estilo.md` para obter:
- Formulas de abertura por tipo de peca
- Frases de transicao mais usadas
- Formato de citacao de jurisprudencia
- Estrutura tipica de pedidos
- Templates detalhados por tipo de peca

### Passo 3 — Redigir no Estilo Correto

#### Enderecamento e Abertura

Para juizes e desembargadores (maiusculas):
```
EXCELENTISSIMO(A) SENHOR(A) JUIZ(A) DE DIREITO DA [VARA] COMARCA DE [CIDADE]
```
Para tribunais superiores:
```
EXCELENTISSIMO(A) SENHOR(A) MINISTRO(A) PRESIDENTE DO SUPERIOR TRIBUNAL DE JUSTICA
```
Para orgaos administrativos:
```
ILUSTRISSIMO(A) SENHOR(A) [CARGO]
```

#### Qualificacao das Partes (formula padrao)

```
[NOME DO CLIENTE], [qualificacao: ja qualificado nos autos / brasileiro, [estado civil],
[profissao], portador do CPF/RG n. XX], vem, respeitosamente, a elevada presenca de
Vossa Excelencia, por intermedio de seu advogado signatario, com fundamento no(s)
art(s). [ARTIGOS], apresentar [TIPO DA PECA], pelas razoes de fato e de direito a seguir
expostas.
```

Se ja qualificado nos autos: usar "ja qualificado nos autos em epigrafe"

#### Estrutura de Secoes

Usar algarismos romanos para secoes principais e arabicos para subsecoes:
```
I – DO CABIMENTO / DAS PRELIMINARES
II – DOS FATOS
III – DO DIREITO
  3.1 Da [tese principal]
  3.2 Da [tese secundaria]
IV – DOS PEDIDOS
```

#### Frases de Transicao e Conectivos (Top — extraidos de 292 pecas)

| Situacao | Frase | Contagem |
|----------|-------|----------|
| Introduzir argumento | "Ora," / "Pois bem." / "Com efeito," | 437x / 97x / 9x |
| Adicionar ponto | "Alem disso," / "Ademais," / "Alias," / "Outrossim," | 366x / 43x / 202x / 9x |
| Introduzir contradicao | "No entanto," / "Contudo," / "Ocorre que," / "Entretanto," | 232x / 167x / 82x / 51x |
| Concluir argumento | "Portanto," / "Desse modo," / "Logo," / "Assim," | 547x / 142x / 46x / 300x |
| Causa/explicacao | "Isso porque" / "E que" / "De fato," / "Em verdade," | 86x / 162x / 180x / 66x |
| Escalada (mais um argumento forte) | "Mas nao e so." / "Nao fosse isso o suficiente," / "Nao bastasse," | 118x / 46x / 25x |
| Reformulacao/sintese | "Ou seja," / "Em sintese," / "Em outras palavras," | 132x / 99x / 20x |
| Sequenciamento | "Em um primeiro momento," / "Em um segundo momento," / "Por fim," | 41x / 28x / 186x |
| Evidencia/confirmacao | "Como visto," / "Como se sabe," / "Diante desse contexto," | 105x / 32x / 59x |
| Registro | "Vale registrar," / "Vale frisar," / "Cumpre registrar," | 28x / 23x / 16x |
| Refutar argumento contrario | "Sem razao, entretanto," / "Com a devida venia," / "Improcede" | 51x / 64x / 28x |
| Concessiva | "Ainda que" / "Embora" / "Conquanto" / "Muito embora" | 73x / 152x / 3x / 2x |
| Introduzir jurisprudencia | "Nesse sentido," / "Sobre o assunto," / "No mesmo sentido," | 41x / 53x / 45x |

> Para lista completa de conectivos e expressoes, consulte `./references/perfil-estilo.md` secao 2.

#### Citacao de Jurisprudencia

**FORMATO INLINE (entre aspas, dentro do paragrafo)**: Citacoes de jurisprudencia e doutrina
NUNCA sao apresentadas em bloco recuado/indentado. Sempre fluem DENTRO do paragrafo, entre
aspas duplas, em italico, continuando na mesma formatacao do texto corrente.

Exemplo correto:
```
Nesse sentido, esse Colendo Tribunal de Justica sedimentou que, "[TRECHO DA EMENTA em
italico, com palavras-chave em negrito+italico]" (TJSC, HC n. XXXX, rel. Des. [Nome],
[Nª Camara Criminal], j. em DD.MM.AAAA).
```

Exemplo correto (com citacao aninhada):
```
A decisao afirmou que "sobressai da jurisprudencia que 'a periculosidade do agente pode
ser aferida por intermedio de diversos elementos concretos' (STF, HC 126501, rel. Min. p/
acordao Edson Fachin, j. 14.06.2016)" (grifos acrescentados).
```

Exemplo correto (doutrina):
```
Portanto, como explicam os insignes doutrinadores Eugenio Pacelli e Douglas Fischer
(Comentarios ao Codigo de Processo Penal e sua Jurisprudencia, 11 ed., Sao Paulo: Atlas,
2019, p. 736), "Havendo duvidas quanto a existencia de qualquer causa de justificacao
(excludentes da ilicitude), nao se determinara a prisao [preventiva] (art. 314 do CPP)"
(grifos acrescentados).
```

**REGRAS**:
- Texto citado entre aspas duplas (""), em italico; aspas simples ('') para citacoes aninhadas
- Palavras-chave dentro da citacao podem receber negrito+italico para enfase
- Referencia do julgado em parenteses IMEDIATAMENTE apos o fechamento das aspas
- Formato da referencia: ([Tribunal], [Tipo] n. [numero], rel. Min./Des. [nome], [orgao
  julgador], j. em DD.MM.AAAA)
- "(grifos acrescentados)" ou "(grifos nossos)" apos a referencia, quando houver enfase adicionada
- Colchetes [palavra] para termos acrescentados/esclarecidos pelo advogado dentro da citacao
- SEM quebra de linha antes ou depois da citacao — o texto continua no mesmo paragrafo
- NUNCA usar bloco recuado, fonte menor ou paragrafo separado para citacoes

> Para variacoes de introducao e citacao de artigos, consulte `./references/perfil-estilo.md` secoes 6.2 e 6.3.

#### Pedidos (formula tipica)

```
IV – DOS PEDIDOS

Ante todo o exposto, requer:

a) o conhecimento e provimento do presente [recurso/pedido];
b) [pedido especifico 1];
c) [pedido especifico 2];
d) o deferimento de [medida urgente, se cabivel].

Pede deferimento.

[Cidade], [data].

[Nome do advogado]
OAB/SC n. [numero]
```

### Passo 4 — Revisar (Checklist)

Antes de entregar a peca, execute a checklist de revisao abaixo (secao "Revisao e Checklist").

### Passo 5 — Gerar o Arquivo .docx (OBRIGATORIO)

Apos redigir, use o script `./scripts/gerar_peticao.py` para criar o arquivo Word.
O arquivo e **SEMPRE** salvo em uma pasta com o nome do cliente:

```
<diretorio-base>/<NOME_CLIENTE>/output_claude/<TIPO>_<CLIENTE>_<DATA>.docx
```

- A pasta do cliente e a subpasta `output_claude` sao criadas automaticamente
- `--cliente` e OBRIGATORIO (usado para criar a pasta e nomear o arquivo)
- `--base-dir` define onde criar a pasta do cliente (default: diretorio atual)

```bash
python ./scripts/gerar_peticao.py --titulo "CONTESTACAO" --cliente "Joao da Silva" \
  --advogado "Paulo Ekke Moukarzel Junior" --oab "12345" \
  --cidade "Florianopolis" --conteudo /tmp/peticao_redigida.txt
```

Resultado: `./JOAO_DA_SILVA/output_claude/CONTESTACAO_JOAO_DA_SILVA_2026-02-20.docx`

---

## Revisao e Checklist

### Checklist de Forma
- [ ] Enderecamento correto (juizo/tribunal, maiusculas)
- [ ] Qualificacao das partes completa
- [ ] Secoes numeradas com romanos (I, II, III, IV)
- [ ] Subsecoes com arabicos (3.1, 3.2)
- [ ] Pedidos em alineas (a, b, c, d)
- [ ] Encerramento: "Pede deferimento." + cidade/data + assinatura (417x no corpus)
- [ ] **NENHUM nome de magistrado/MP do caso** no corpo (usar funcao: "o Juiz sentenciante", "o Relator") — MAS nomes de relatores SIM em citacoes de jurisprudencia
- [ ] **NENHUM local de tramitacao** no corpo (identificar processo apenas pelo numero) — MAS local dos fatos SIM (onde ocorreu o crime etc.)
- [ ] **Datas apenas quando relevantes** para dinamica dos fatos ou teses juridicas (evitar datas meramente informativas)

### Checklist de Substancia
- [ ] Fatos extraidos de FONTES PRIMARIAS (autos de origem), nao de resumos ou peticao adversa
- [ ] Cadeia documental: cada alegacao factual com referencia por evento "(evento N, TIPO)" (preferencial) ou por folhas "(fl. X)" (subsidiario)
- [ ] Lista de documentos ao final da peca SOMENTE em peticoes iniciais ou quando os documentos sejam NOVOS (nao existentes nos autos). Em recursos sobre documentos ja nos autos, NAO incluir lista
- [ ] Fundamento legal citado para argumentos juridicos (artigo de lei)
- [ ] Jurisprudencia usada com parcimonia — apenas para pontos estritamente juridicos
- [ ] Citacoes de jurisprudencia COM nome do relator e data do julgamento (para conferencia de autenticidade)
- [ ] **TODA jurisprudencia citada teve autenticidade confirmada** (via documentos dos autos, pesquisa no site oficial do tribunal, ou validacao do Dr. Paulo). NENHUM precedente inventado ou presumido
- [ ] Citacoes INLINE entre aspas dentro do paragrafo (NUNCA em bloco recuado/indentado)
- [ ] Referencias aos autos PREFERENCIALMENTE por evento do e-proc; folhas apenas quando evento nao disponivel
- [ ] Preliminares no corpo principal APENAS se forem argumentos fortes
- [ ] Todos os pedidos correspondem aos argumentos desenvolvidos
- [ ] Argumentos menos robustos incluidos como TESE SUBSIDIARIA antes dos pedidos (nao omitidos)

### Checklist de Estilo
- [ ] Conectivos usados entre paragrafos (Nesse sentido, Ocorre que, Alem disso)
- [ ] Sem bullet points nem alineas (a/b/c) no corpo argumentativo — argumentos em paragrafos fluidos conectados por conectivos. Alineas (a, b, c) EXCLUSIVAMENTE na secao de pedidos/requerimentos
- [ ] Tratamento protocolar mantido (Vossa Excelencia, Colendo, Egregio)
- [ ] Nomes de clientes em MAIUSCULAS na primeira mencao
- [ ] Expressoes latinas usadas quando pertinentes
- [ ] Sentencas elaboradas, nao curtas e diretas
- [ ] **Narrativa fatica OBJETIVA**: crime/fato primeiro, processo depois; verbos no condicional para fatos da acusacao; formas impessoais para decisoes; decisoes por evento (sem data/nome); sem adjetivacao desnecessaria

---

## Modo de Revisao

Quando o usuario pedir para **revisar** ou **corrigir** uma peca existente, seguir este protocolo:

1. **Receber o documento** — Ler o texto integral fornecido
2. **Analise estrutural** — Verificar enderecamento, qualificacao, numeracao de secoes,
   pedidos, encerramento. Reportar ausencias.
3. **Analise de estilo** — Comparar com os padroes do Dr. Paulo (conectivos, formalidade,
   citacoes, expressoes latinas). Apontar desvios.
4. **Sugestoes categorizadas** — Organizar em:
   - **Criticas** (erros que comprometem a peca): fundamentacao ausente, pedido incompleto
   - **Importantes** (desvios significativos): estilo informal, falta de jurisprudencia
   - **Sugestoes** (melhorias opcionais): conectivos, expressoes mais precisas
5. **Reescrita** — Oferecer versao corrigida dos trechos problematicos, ou reescrever
   a peca inteira se solicitado.

---

## Modo Batch/Automacao

Para geracao de multiplas pecas em lote:

1. Preparar um arquivo CSV ou lista com: tipo_peca, cliente, tribunal, processo, fatos
2. Para cada entrada, executar o workflow completo (Passos 1-5)
3. Cada peca e salva automaticamente em `<CLIENTE>/output_claude/<TIPO>_<CLIENTE>_<DATA>.docx`
   - Exemplo: `JOAO_SILVA/output_claude/CONTESTACAO_JOAO_SILVA_2026-02-20.docx`
4. **Limitacoes**: cada peca requer revisao individual; nao pular o Passo 4 (checklist)

---

## Por Tipo de Peca

### Resposta a Acusacao (art. 396 CPP)

- Abre com fórmula padrão "já qualificado" + "apresentar RESPOSTA À ACUSAÇÃO"
- Variante completa: `I – BREVE ESCORÇO DA DENÚNCIA` + teses defensivas
- Variante minimalista: "Todas as questões relacionadas ao fato apurado serão devidamente tratadas ao longo da instrução criminal" + pedido de audiência
- Sempre incluir `ROL DE TESTEMUNHAS:` após assinaturas (máx. 8 por art. 401 CPP)
- Fundamento: art. 396 e seguintes do CPP
- **Fontes primarias**: Extrair os fatos da denuncia e do inquerito diretamente dos autos,
  nao de resumos. Identificar com precisao o evento da denuncia e as pecas do IP.
- **Argumentos selecionados**: Na variante completa, apresentar APENAS teses defensivas
  fortes nesta fase. Reservar teses mais complexas para alegacoes finais.

### Habeas Corpus / RHC

- **Quem se qualifica: os advogados**, não o cliente — `"BRUNO GASTÃO DA ROSA... e PAULO EKKE MOUKARZEL JUNIOR... advogados constituídos, vêm..."`
- Incluir cabeçalho de urgência: `URGENTE! / Paciente preso e / pedido de liminar`
- Paciente qualificado completamente (CPF + endereço prisional) no corpo
- Identificar o "ato coator" com precisão (decisão que decretou/manteve a prisão)
- Usar "paciente" para o réu/preso
- Fórmula de pedido: `"é este writ para requerer"` (TJSC) ou `"é este mandamus para requerer"` (STJ)
- Após assinaturas: `DOCUMENTOS QUE INSTRUEM ESTE MANDAMUS:` + lista numerada, SOMENTE quando houver documentos novos extraidos dos autos de origem que estejam sendo juntados pela primeira vez ao writ
- Pedir liminar quando houver urgência
- **Fontes primarias**: Ler diretamente os autos da acao penal/inquerito para identificar o
  ato coator e os fatos concretos de ilegalidade. NAO confiar em resumos da decisao atacada.
- **Cadeia documental**: Cada fato de ilegalidade respaldado por documento juntado ao writ.
  A lista "DOCUMENTOS QUE INSTRUEM ESTE MANDAMUS" so deve ser incluida quando houver
  documentos NOVOS sendo juntados pela primeira vez. Se todos os documentos ja constam dos
  autos com evento/numeracao, basta a referencia no corpo do texto.
- **Jurisprudencia minima**: Fatos concretos de ilegalidade convencem mais que ementas.
  Usar jurisprudencia apenas para pontos estritamente juridicos (ex: fundamentacao da prisao).
- **Pedido de liminar**: A secao de liminar deve ser CONCISA e REMISSIVA, evitando repetir
  a argumentacao ja desenvolvida no corpo do writ. Estrutura:
  - **Fumus boni juris**: Expor de forma resumida o argumento central (tese principal) com
    as referencias documentais e fundamentos legais essenciais, sem recontar a narrativa
    factual. Para os demais argumentos, remeter expressamente as secoes do corpo do writ
    onde foram desenvolvidos (ex: "conforme exposto na secao III.2 deste writ"), citando
    apenas os documentos-chave e trechos conclusivos.
  - **Periculum in mora**: Demonstrar CONCRETAMENTE o risco iminente ao paciente — tempo
    de prisao ja cumprido, cumprimento antecipado de pena em regime mais gravoso que o
    devido, excesso de prazo, transito em julgado iminente, dano irreversivel a liberdade.
    Fundamentar com dados concretos: datas, tempo de custodia, regime fixado vs. devido.
    Quando cabivel, registrar que o merito das teses nao foi apreciado pelos Tribunais
    Superiores por obstaculo processual, o que reforça a urgencia.
  - **Ausencia de periculum libertatis**: Demonstrar que o paciente nao oferece risco a
    ordem publica, a instrucao criminal ou a aplicacao da lei penal. Citar: primariedade,
    bons antecedentes, ausencia de vinculo com organizacao criminosa, instrucao ja
    encerrada, ausencia de elementos de reiteracao. Fundamentar com documentos concretos
    dos autos (certidao de antecedentes, por exemplo). Concluir que estao ausentes os
    requisitos do art. 312 do CPP para manutencao da prisao preventiva.
  - **Fechamento**: Concluir com pedido objetivo de suspensao da execucao da pena ou da
    decisao coatora ate o julgamento definitivo do writ, com fundamento no art. 660, §2º,
    do CPP.
  - **Regra geral**: A liminar NAO deve ser uma segunda peca dentro da peca. Deve ser
    enxuta (3-5 paragrafos), remetendo ao corpo do HC para a fundamentacao detalhada.
    O objetivo e demonstrar ao relator que ha plausibilidade juridica e urgencia, nao
    repetir todos os argumentos. NUNCA usar paragrafos genericos — cada fato do fumus e
    cada dado do periculum devem ser especificos do caso concreto.
  - **Jurisprudencia na liminar**: Pode acompanhar a fundamentacao, DESDE QUE a
    autenticidade seja confirmada (via site oficial do tribunal ou WebSearch) OU conste de
    peca anterior _vf ja elaborada na pasta de Clientes. NUNCA inventar precedentes.

### Embargos de Declaracao (EDs)

- Indicar o acordao/decisao embargada pelo numero do processo (SEM data, SEM nome do relator)
- Apontar especificamente: omissao / contradicao / obscuridade / erro material
- Estrutura: "O acordao embargado incorreu em [vicio], ao deixar de [apreciar/decidir/esclarecer]..."
- Pedir a integracao/correcao do julgado
- **Fontes primarias**: Citar trechos EXATOS do acordao embargado e confrontar com o que
  consta dos autos — apontar com precisao o evento, pagina ou trecho omitido/contraditorio.
- **Argumentos selecionados**: Focar APENAS nos vicios reais. Nao usar EDs como pretexto
  para rediscutir merito — apontar com cirurgica precisao a omissao, contradicao ou obscuridade.

### Contestacao

**Principio central**: O poder de convencimento vem dos FATOS documentados nos autos,
nao de teses juridicas abstratas. Ir evento a evento nos autos de origem e construir
uma narrativa factual irrefutavel.

> **REGRA CONCEITUAL — Arbitramento de honorarios**: Em acoes de arbitramento de
> honorarios (art. 22, §2o, Lei 8.906/94), o foco NAO e o contrato de honorarios em si,
> mas sim o TRABALHO EFETIVAMENTE REALIZADO pelo advogado no processo. O contrato serve,
> no maximo, como parametro. O que importa e: (i) qualidade/zelo do trabalho, (ii)
> complexidade da causa, (iii) quantidade de atos praticados, (iv) tempo dedicado. Logo,
> a contestacao deve focar em demonstrar — com provas documentais dos autos de origem —
> se o trabalho foi ou nao realizado com zelo, e nao em atacar clausulas contratuais
> abstratamente. Aplicar os criterios do art. 85, §2o, do CPC.

**Estrutura preferida (simples e focada)**:
- I – BREVE SÍNTESE DA DEMANDA (breve, sem "Trata-se")
- II – DO MÉRITO (seção única ou poucas subseções — preferir profundidade a amplitude)
  - II.1 – Título descritivo longo que antecipa a conclusão (ex: "Impossibilidade de
    cobrança de valores adicionais e falha na prestação dos serviços advocatícios, o que
    impõe improcedência da demanda ou, no mínimo, a fixação de quantum mínimo")
- III – TESE SUBSIDIÁRIA (se houver argumentos menos robustos — incluir aqui, antes dos
  pedidos, com breve descricao de cada tese alternativa que o juiz possa acolher)
- IV – DA PRODUÇÃO DE PROVAS
- V – REQUERIMENTOS (usar "Ante o exposto, os réus requerem:")

**Regras especificas**:
1. **Fatos em primeira mao**: Ler os autos do processo de ORIGEM (inventario, acao penal,
   PAD etc.) evento por evento. Extrair datas, decisoes, peticoes, certidoes com precisao.
   NAO se basear em resumos da parte contraria ou da decisao que recebeu a inicial.
2. **Cadeia documental**: Cada fato = "(doc. X)" referenciando documento juntado.
   Incluir "DOCUMENTOS QUE ACOMPANHAM ESTA CONTESTAÇÃO:" + lista ao final SOMENTE quando
   houver documentos NOVOS sendo juntados (nao existentes nos autos). Se todos os documentos
   ja constam dos autos com evento/numeracao, basta a referencia no corpo do texto.
3. **Atacar a forma da petição adversa** quando cabível: ex. "a petição inicial é confusa
   e não corresponde à fundamentação de ação de conhecimento."
4. **Preliminares**: Incluir no corpo principal APENAS se forem argumentos fortes e
   incontroversos. Preliminares menos robustas podem ser apresentadas como TESE SUBSIDIARIA.
5. **Jurisprudência mínima**: Usar apenas 1-2 julgados para pontos estritamente
   juridicos (ex: nulidade de clausula penal). O mérito deve ser sustentado pelos fatos.
6. **Qualificação simplificada**: Se partes já qualificadas nos autos, usar
   "já qualificados nos autos em epígrafe" (sem repetir CPF, profissão etc.)
7. **Endereçamento específico**: Usar o gênero correto do magistrado quando conhecido
   (ex: "EXCELENTÍSSIMA SENHORA DOUTORA JUÍZA DE DIREITO")
8. **"Sem razão, entretanto, os demandantes."** — fórmula de refutação direta.

### Alegacoes Finais

- Retomar os fatos provados na instrucao com referencia aos elementos de prova
- Confrontar a acusacao com as provas produzidas
- Em crimes dolosos: enfatizar ausencia de dolo ou de autoria
- Concluir pela absolvicao com fundamento no art. 386 do CPP (indicar inciso)
- Seção de fatos: `I – BREVE ESCORÇO DA DEMANDA`
- **Fontes primarias**: Cada fato relevante extraido diretamente dos depoimentos, pericias
  e documentos dos autos — citar evento e tipo de documento com precisao.
  NAO se basear em resumos da sentenca ou do MP sobre a prova produzida.
- **Jurisprudencia minima**: A forca das alegacoes finais esta nas PROVAS DOS AUTOS.
  Usar jurisprudencia apenas para pontos juridicos (ex: aplicacao do in dubio pro reo).
- **Argumentos selecionados**: Focar nas teses mais fortes com base na prova produzida.
  Teses menos robustas devem ser incluidas como TESE SUBSIDIARIA ao final da peca.

### Memoriais de Apelacao (TJSC)

- Estrutura SEM "vem, respeitosamente" — começa com bloco de metadados
- Formato de abertura: `Apelação Criminal n. [N]. / Apelante: [NOME] / Apelado: MP / Relator: [preencher] / Data do julgamento: [preencher] nº de pauta: [N]` (nomes de desembargadores e data preenchidos pelo Dr. Paulo)
- Depois: `MEMORIAIS PELO APELANTE` + `EMINENTE DESEMBARGADOR RELATOR / COLENDA [N]ª CÂMARA DE DIREITO CRIMINAL`
- Corpo narrativo puro — SEM seções numeradas
- Usar marcadores de escalada: `Mas não é só.`, `Não fosse isso tudo o suficiente,`, `Aliás,`
- Endereçar o juízo diretamente: `"Como visto, Excelência,"`, `"Convém registrar, Excelência, que"`
- Pedidos subsidiários com: `"Subsidiariamente, Excelência,"`
- Encerrar com frase retórica — SEM "Ante o exposto" e SEM "Pede deferimento"
- Frase final padrão: `"Como visto, Excelência, a absolvição do apelante é medida de Justiça, razão pela qual o recorrente reitera e confia no provimento da apelação, nos termos requeridos nas razões recursais."`
- **Fontes primarias**: O corpo narrativo deve ser construido com fatos CONCRETOS extraidos
  dos autos de instrucao — depoimentos, pericias, documentos — com referencia a eventos.
  O memorial e a oportunidade de mostrar ao desembargador os fatos que a sentenca ignorou.
- **Jurisprudencia minima**: Memoriais sao sobre FATOS e PROVAS, nao sobre teses abstratas.
  Usar no maximo 1-2 julgados e apenas quando estritamente necessario.

### RESE (Recurso em Sentido Estrito)

- Estrutura dupla: (1) petição de protocolo + (2) razões recursais separadas
- Petição de protocolo: "não se conformando com a r. decisão recorrida... vem... interpor RECURSO EM SENTIDO ESTRITO, a tempo e modo" + pedido de retratação (art. 589 CPP) ou remessa ao TJSC
- Corpo recursal: `RAZÕES DE RECURSO EM SENTIDO ESTRITO` + `EGRÉGIO TJSC / COLENDA CÂMARA / EXCELENTÍSSIMO DESEMBARGADOR RELATOR`
- Seção de fatos: `I – SÍNTESE DA DEMANDA`
- Pedidos: `"Diante do exposto, o recorrente requer o conhecimento e provimento do presente recurso em sentido estrito para..."`
- Hipóteses mais comuns: pronúncia (art. 581, IV CPP), rejeição da denúncia (I), prisão preventiva (V)
- **Fontes primarias**: Atacar a decisao recorrida com fatos concretos dos autos —
  depoimentos, documentos, pericias — citando evento e tipo de documento.
- **Jurisprudencia minima**: Fatos e provas em primeiro plano; jurisprudencia para pontos
  juridicos (ex: requisitos da pronuncia, fundamentacao da prisao).

### Apelacao Criminal

- Indicar a sentenca recorrida pelo numero do processo (SEM nome do juiz, SEM data, SEM local)
- Atacar os fundamentos da sentenca ponto a ponto
- Fundamento no art. 593 do CPP (absolvicao) ou art. 617 (reformatio in melius)
- Seção de fatos: `I – SÍNTESE DA DEMANDA`
- **Fontes primarias**: Confrontar cada fundamento da sentenca com a prova REAL dos autos —
  depoimentos (evento, tipo), pericias, documentos. Mostrar o que a sentenca ignorou ou
  distorceu, com referencia precisa ao evento e tipo de documento.
- **Jurisprudencia minima**: A apelacao deve ser sustentada pelas PROVAS e nao por teses
  abstratas. Jurisprudencia apenas para pontos estritamente juridicos.
- **Argumentos selecionados**: Focar nos pontos mais fortes de ataque a sentenca no corpo
  principal. Teses menos robustas podem ser incluidas como TESE SUBSIDIARIA ao final.

### AREsp / REsp (STJ)

- Demonstrar o prequestionamento
- Indicar a alinea do permissivo constitucional/legal
- Apresentar o dissidio jurisprudencial com "cotejo analitico" (se alinea "c")
- Transcrever a ementa do acordao recorrido
- **Fontes primarias**: Extrair fatos relevantes diretamente dos autos de origem e do
  acordao recorrido, com referencia precisa a eventos e documentos.
- **Argumentos selecionados**: Focar nos pontos com real chance de provimento no STJ.
  Nao sobrecarregar o recurso com teses marginais que diluem o argumento central.

### Peticao Inicial Civel

- Fundamento: arts. 319, 320 do CPC
- Requisitos obrigatorios: juizo competente, partes, causa de pedir, pedido, valor da causa
- Incluir pedido de tutela provisoria quando cabivel (art. 300 CPC)
- Juntar documentos indispensaveis (art. 320 CPC)
- **Cadeia documental**: Causa de pedir construida com fatos documentados — cada alegacao
  respaldada por "(doc. X)". Ao final: "DOCUMENTOS QUE ACOMPANHAM ESTA INICIAL:" + lista
  numerada. Na peticao inicial, a lista de documentos e SEMPRE obrigatoria (art. 320 CPC).
- **Fontes primarias**: Narrar fatos com base nos documentos concretos do cliente, nao em
  alegacoes genericas. Cada fato = data + documento + referencia.
- **Jurisprudencia minima**: Fatos bem documentados sao mais persuasivos que ementas.
  Jurisprudencia apenas para pontos juridicos controversos.

### Replica (Impugnacao a Contestacao)

- Fundamento: art. 351 do CPC
- Rebater preliminares arguidas na contestacao
- Impugnar documentos novos juntados pelo reu
- Reforcar os fundamentos da inicial com novos argumentos
- **Fontes primarias**: Refutar a contestacao ponto a ponto com fatos e documentos concretos
  dos autos, nao com teses abstratas. Cada refutacao = fato + "(doc. X)".
- **Atacar a forma da contestacao** quando cabivel (falta de impugnacao especifica, art. 341 CPC).
- **Argumentos selecionados**: Focar nos pontos que realmente comprometem a defesa.
  Nao rebater cada paragrafo — selecionar os pontos mais frageis da contestacao.

### Agravo de Instrumento

- Fundamento: art. 1.015 do CPC (hipoteses de cabimento — rol taxativo mitigado)
- Indicar a decisao interlocutoria agravada com precisao (evento — SEM data, SEM nome do juiz)
- Pedir efeito suspensivo ou tutela recursal quando cabivel (art. 1.019, I, CPC)
- Juntar copias obrigatorias (art. 1.017 CPC) ou indicar processo eletronico
- **Fontes primarias**: Demonstrar o erro da decisao com fatos concretos dos autos —
  citar eventos, documentos e provas que o juiz ignorou ou interpretou mal.
- **Jurisprudencia minima**: Fatos e provas sustentam o agravo; jurisprudencia apenas
  para pontos estritamente juridicos (ex: cabimento, periculum in mora).

### Agravo Interno

- Fundamento: art. 1.021 do CPC
- Impugnar especificamente os fundamentos da decisao monocratica
- Demonstrar por que a decisao merece reforma pelo colegiado
- Atencao ao prazo de 15 dias (art. 1.021 CPC)
- **Fontes primarias**: Confrontar a decisao monocratica com fatos concretos dos autos que
  demonstrem o erro, nao apenas com teses juridicas abstratas.
- **Argumentos selecionados**: Impugnar especificamente os fundamentos da decisao —
  nao repetir genericamente as razoes do recurso anterior.

### Mandado de Seguranca

- Fundamento: Lei n. 12.016/09, art. 5, LXIX da CF
- Demonstrar direito liquido e certo com prova pre-constituida
- Identificar a autoridade coatora e o ato ilegal/abusivo
- Pedir liminar (art. 7, III, Lei n. 12.016/09) quando houver periculum in mora
- **Cadeia documental essencial**: Direito liquido e certo = prova pre-constituida. Cada fato
  deve ser respaldado por "(doc. X)". Ao final: "DOCUMENTOS QUE ACOMPANHAM ESTE MANDAMUS:"
  + lista numerada (obrigatoria no MS, pois e prova pre-constituida juntada pela primeira vez).
- **Fontes primarias**: Demonstrar a ilegalidade com documentos concretos, nao com teses
  abstratas. Cada ato coator = referencia precisa ao documento que o comprova.

### Tutela de Urgencia / Evidencia

- Urgencia: art. 300 do CPC — probabilidade do direito + perigo de dano
- Evidencia: art. 311 do CPC — abuso de direito de defesa, prova documental suficiente
- Pode ser antecedente, incidental ou em carater antecedente (arts. 303-304 CPC)
- **Demonstracao OBRIGATORIA de fumus boni juris e periculum in mora**: Aplicar o
  Principio 13 integralmente. Fumus demonstrado com remissao concreta aos argumentos
  desenvolvidos na peca e aos documentos do caso. Periculum demonstrado com fatos
  concretos (datas, danos, prejuizos iminentes, irreversibilidade). NUNCA usar paragrafos
  genericos que sirvam para qualquer caso — cada fato deve ser especifico e ancorado nas
  circunstancias do caso concreto.
- **Fontes primarias e cadeia documental**: Periculum in mora e fumus boni iuris devem ser
  demonstrados com FATOS CONCRETOS e documentados — cada alegacao com "(doc. X)".
  Nao sustentar urgencia com teses abstratas.
- **Jurisprudencia na tutela**: Pode acompanhar a fundamentacao, DESDE QUE a autenticidade
  seja confirmada (via site oficial do tribunal ou WebSearch) OU conste de peca anterior
  _vf ja elaborada na pasta de Clientes.

### Contrarrazoes

- Procedimento geral: resposta ao recurso da parte contraria
- Defender a manutencao da decisao recorrida ponto a ponto
- Reforcar os fundamentos da decisao atacada
- Apontar eventuais questoes de inadmissibilidade do recurso (intempestividade, ausencia de preparo)
- **Fontes primarias**: Refutar cada argumento do recurso com fatos e provas dos autos —
  depoimentos, documentos, pericias — com referencia precisa a eventos.
- **Atacar a forma do recurso** quando cabivel: falta de dialeticidade, inovacao recursal,
  ausencia de impugnacao especifica dos fundamentos da sentenca.
- **Jurisprudencia minima**: As provas dos autos que sustentam a sentenca sao mais
  persuasivas que citacoes jurisprudenciais em excesso.

### Impugnacao ao Cumprimento de Sentenca

- Fundamento: art. 525 do CPC
- Materias arguiveis: falta/nulidade de citacao, ilegitimidade, inexequibilidade do titulo,
  excesso de execucao, pagamento, novacao, compensacao, prescricao
- Apresentar demonstrativo do debito correto quando alegar excesso
- Prazo: 15 dias (art. 525, caput, CPC)
- **Cadeia documental**: Demonstrar excesso de execucao, pagamento ou novacao com documentos
  concretos — cada alegacao com "(doc. X)". Demonstrativo do debito correto documentado.
- **Fontes primarias**: Confrontar os calculos do exequente com os termos exatos do titulo
  executivo judicial, nao com interpretacoes genericas.

---

## Dicas Avancadas de Estilo

- **Nomes de clientes** em MAIUSCULAS na primeira mencao, depois normal
- **Tribunais**: usar "Colendo STJ" (249x de "Colendo"), "Egregio Supremo Tribunal Federal" (NUNCA "Excelso" — 0x), "Egregio Tribunal de Justica"
- **Sentencas longas e complexas** sao preferidas a sentencas curtas e simples
- **Nunca abreviar** "Vossa Excelencia" para "V.Exa." no corpo do texto
- **Referenciar eventos dos autos** com precisao: "evento 76, OUT5" — referencia por evento do e-proc e o sistema PREFERENCIAL (3.561x no corpus). Referencia a folhas ("fl. X", "fls. X/Y") e SUBSIDIARIA, usada apenas quando nao houver informacao sobre o evento correspondente
- **Expressoes latinas** confirmadas (292 pecas): "bis in idem" (65x), "habeas corpus" (63x), "modus operandi" (37x), "in casu" (34x), "writ" (34x), "a quo" (33x), "in dubio pro reo" (26x), "periculum in mora" (19x), "fumus boni juris" (18x), "ex officio" (18x), "venire contra factum proprium" (18x), "reformatio in pejus" (17x), "ad argumentandum" (16x), "data maxima venia" (6x). NUNCA usar: "ad quem" (0x), "data venia" sem "maxima" (0x), "ex vi" (0x), "prima facie" (0x), "mutatis mutandis" (0x), "in verbis" (0x)
- **Negrito** e usado estrategicamente, nao em excesso — principalmente em trechos de jurisprudencia
- **Vocabulario incisivo confirmado** (adjetivos/adverbios mais usados): "manifesto" (289x), "ilegal" (223x), "absoluto" (121x), "irregular" (121x), "sequer" (93x), "proporcional" (66x), "incontroverso" (62x), "flagrante" (49x), "evidentemente" (44x), "manifestamente" (34x), "contundente" (29x), "desproporcional" (28x), "excessivo" (27x), "fragil" (24x), "elementar" (20x), "jamais" (14x), "tampouco" (14x)
- **Perguntas retoricas** — usadas com PARCIMONIA (apenas 17 em 292 pecas). Recurso pontual e estrategico, nao habitual
- **"No mais,"** (211x) como transicao para registro final ou pedido de intimacao
- **"Repita-se, Excelencia"** — enfase por repeticao (uso pontual em contestacoes)
- **Variacao lexical obrigatoria para "demonstrar"**: NAO repetir "demonstrar/demonstrou/demonstrado"
  em paragrafos proximos. Alternar com sinonimos: "comprovar/comprovou/comprovado",
  "provar/provou/provado", "evidenciar/evidenciou/evidenciado", "atestar/atestou/atestado",
  "confirmar/confirmou/confirmado", "restar demonstrado/comprovado/evidenciado". Manter variacao
  natural ao longo da peca — a mesma regra se aplica aos substantivos derivados ("demonstracao" →
  "comprovacao", "prova", "evidencia"). Exemplo: em vez de "demonstrou X ... demonstrou Y ...
  demonstrado Z", usar "demonstrou X ... comprovou Y ... restou evidenciado Z"

---

## Referencias

Para analise aprofundada do estilo com exemplos reais das pecas, consulte:
`./references/perfil-estilo.md`

Para gerar o arquivo .docx formatado apos redigir:
`./scripts/gerar_peticao.py`
