# Mapeamento de Workflows

**DOCUMENTO 07 | ANALISE CRITICA**

Diagramas dos 10 Workflows Atuais + 10 Workflows Sugeridos com Validadores

---

Sistema de Workflow Juridico v2.0
Escritorio Gastao da Rosa & Moukarzel
Dr. Paulo Ekke Moukarzel Junior | OAB/SC

*Abril 2026 | Confidencial*

---

## Legenda dos Diagramas

| Elemento | Descricao |
|---|---|
| **TRIGGER** | Ponto de entrada / comando que inicia o workflow |
| **OPUS 4-6** | Agente Claude Opus — raciocinio profundo, redacao, auditoria |
| **SONNET 4-6** | Agente Claude Sonnet — pesquisa, revisao, verificacao |
| **SCRIPT** | Processamento via script Python ou ferramenta externa |
| **VALIDADOR** | Etapa de validacao/verificacao de qualidade (OBRIGATORIA) |
| **OUTPUT** | Resultado final entregue ao advogado |
| **GATE HUMANO** | Ponto de decisao que exige aprovacao humana antes de prosseguir |

> **Principio fundamental:** Todo workflow inclui pelo menos uma etapa de **VALIDACAO** antes de produzir output final. Nenhum conteudo e entregue sem verificacao.

---

# PARTE I — Workflows Atuais

## Workflow 1 — Skill: paulo-estilo-juridico

*Motor de redacao juridica no estilo do Dr. Paulo Moukarzel — 5 etapas*

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER                                                            │
│  Coletar informacoes — nome, tipo de peca, tribunal, processo,      │
│  documentos, bases legais...                          [Dados do caso]│
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 2 — CONSULTA                                                 │
│  Buscar pecas _vf do mesmo tipo em indice_vf.json para replicar     │
│  estrutura argumentativa...                         [indice_vf.json] │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 3 — ESTILO                                                   │
│  Ler perfil-estilo.md (conectivos, formulas, padroes extraidos de   │
│  292 pecas reais)                                [perfil-estilo.md]  │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 4 — REDACAO [OPUS]                                           │
│  Redigir aplicando 13 principios obrigatorios: fontes primarias,    │
│  cadeia documental, pr...                          [Texto da peca]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 5 — GERACAO                                                  │
│  gerar_peticao.py: Arial 12pt, espacamento 1.5, margens juridicas   │
│  3cm/2cm, timbre auto...                              [.docx final]  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Workflow 2 — Skill: criar-agentes

*Criar agentes especializados seguindo padroes Anthropic — 4 etapas*

```
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 1 — ESCOPO                                                   │
│  Entender: o que faz, o que nao faz, quem invoca,                   │
│  ferramentas disponiveis                              [Requisitos]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 2 — REFERENCIA                                               │
│  Consultar catalogo de ferramentas e padroes Anthropic de           │
│  agent design                                         [Ref tools]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 3 — RASCUNHO [OPUS]                                          │
│  Rascunhar .md com frontmatter YAML + responsabilidades +           │
│  processo + formato                                  [Rascunho .md]  │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 4 — REVISAO                                                  │
│  Validar contra checklist de qualidade e salvar em                  │
│  .claude/agents/                               [.claude/agents/*.md] │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Workflow 3 — Command: /novo-caso

*Criar caso novo com estrutura completa de pastas — 5 etapas*

```
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 1 — COLETA                                                   │
│  Coletar: nome MAIUSCULO, processo CNJ, vara, polo, parte adversa,  │
│  prazo fatal                                          [Dados brutos] │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 2 — CONFIRMACAO  [GATE HUMANO]                               │
│  Exibir resumo e aguardar confirmacao do usuario antes de criar     │
│  qualquer arquivo                                    [OK / Cancelar] │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 3 — ESTRUTURA                                                │
│  Criar pastas: Clientes/<CLIENTE>/pipeline/ + output_claude/        │
│                                                       [Diretorios]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 4 — CASO.JSON                                                │
│  Gerar caso.json com metadados completos e pipeline vazio           │
│                                                        [caso.json]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 5 — FEEDBACK                                                 │
│  Exibir confirmacao do caso criado + proximos passos sugeridos ao   │
│  usuario                                               [Resumo]      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Workflow 4 — Command: /caso (Hub de 8 Sub-Comandos)

| Sub-comando | Tipo | Descricao |
|---|---|---|
| /caso status | CONSULTA | Status detalhado — le caso.json, calcula dias ate prazo |
| /caso listar | CONSULTA | Painel de todos os casos ativos do escritorio |
| /caso prazos | CONSULTA | Casos ordenados: VENCIDO > URGENTE > OK > CONCLUIDO |
| /caso contestacao | PIPELINE | Dispara pipeline completo de contestacao (5 etapas) |
| /caso recurso | PIPELINE | Dispara pipeline de recursos REsp/RE (4 etapas) |
| /caso placeholders | CONSULTA | Lista [PLACEHOLDER] pendentes via placeholder_scan.py |
| /caso indexar | MANUTENCAO | Atualiza indice de arquivos _vf via indexar_vf.py |

---

## Workflow 5 — Command: /doit_like_me

*Atalho rapido — ativa a skill paulo-estilo-juridico imediatamente, sem etapas intermediarias.*

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER: /DOIT_LIKE_ME                                             │
│  Usuario invoca comando de atalho                                   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ATIVACAO DIRETA                                                    │
│  Carrega skill paulo-estilo-juridico e inicia workflow de redacao   │
│  completo                                            [Skill ativa]   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Workflow 6 — Pipeline: Contestacao (5 Etapas)

*Orquestrador: Sonnet | 15 agentes disponiveis, ~7 executados por run*

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER                                                            │
│  /caso contestacao <cliente> — Orquestrador Sonnet inicia pipeline  │
│                                                        [caso.json]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  ETAPA 1A — ANALISTA [OPUS]          │  │         PARALELO         │
│  Le documentos, extrai fatos,        │  │                          │
│  argumentos adversos, dispositivos   │  │   [analysis_*.txt]       │
│  legais, cronologia                  │  │                          │
└──────────────────┬───────────────────┘  └──────────────────────────┘
                   ↓
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  ETAPA 1B — PESQ. MAGISTRADO [SONNET]│  │         PARALELO         │
│  Padrao decisorio do juiz,           │  │                          │
│  tendencias, sensibilidades,         │  │  [perfil_mag_*.txt]      │
│  precedentes                         │  │                          │
└──────────────────┬───────────────────┘  └──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 2 — REDATOR [OPUS]                                           │
│  Recebe analise + perfil magistrado. Redige no estilo Paulo com     │
│  13 principios                                    [contest_*_v1.txt] │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  ETAPA 3A — REV. JURIDICO [SONNET]   │  │         PARALELO         │
│  Cobertura de teses, artigos,        │  │                          │
│  jurisprudencia, cadeia documental   │  │  [review_jur_*.txt]      │
│  (doc. X)                            │  │                          │
└──────────────────┬───────────────────┘  └──────────────────────────┘
                   ↓
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  ETAPA 3B — REV. LINGUISTICO [SONNET]│  │         PARALELO         │
│  Aderencia ao estilo: vocabulario,   │  │                          │
│  conectivos, sem "Trata-se", sem     │  │  [review_ling_*.txt]     │
│  "v. acordao"                        │  │                          │
└──────────────────┬───────────────────┘  └──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 4 — AUDITOR FINAL [OPUS]                                     │
│  Consolida v1 + dois relatorios de revisao. Aplica correcoes        │
│  coerentes                                      [contest_*_final.txt] │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 5 — GERADOR .DOCX [SONNET]                                   │
│  gerar_peticao.py: timbre, Arial 12pt, margens juridicas,           │
│  numeracao                                    [CONTESTACAO_*.docx]   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Workflow 7 — Pipeline: Recursos REsp / RE (4 Etapas)

*Orquestrador: Opus | Gera dois documentos independentes simultaneamente*

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER                                                            │
│  /caso recurso <cliente> — Orquestrador Opus inicia pipeline        │
│                                                        [caso.json]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  ETAPA 1A — PESQ. JURISP. [SONNET]   │  │         PARALELO         │
│  Jurisprudencia autenticada STJ/STF  │  │                          │
│  com numero, relator, data, ementa   │  │    [jurisp_*.txt]        │
└──────────────────┬───────────────────┘  └──────────────────────────┘
                   ↓
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  ETAPA 1B — REDATOR RESP [OPUS]      │  │         PARALELO         │
│  Acordao como sujeito, violacao como │  │                          │
│  predicado. Prequestionamento        │  │      [resp_*.txt]        │
│  explicito                           │  │                          │
└──────────────────┬───────────────────┘  └──────────────────────────┘
                   ↓
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  ETAPA 1C — REDATOR RE [OPUS]        │  │         PARALELO         │
│  Repercussao geral, violacao direta  │  │                          │
│  CF. Teses subsidiarias incluidas    │  │       [re_*.txt]         │
└──────────────────┬───────────────────┘  └──────────────────────────┘
                   ↓
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  ETAPA 2A — REV. PREQUESTION.[SONNET]│  │         PARALELO         │
│  Todos os dispositivos foram debatidos│ │                          │
│  no acordao recorrido?               │  │  [review_preq.txt]       │
└──────────────────┬───────────────────┘  └──────────────────────────┘
                   ↓
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  ETAPA 2B — REV. ESTILO [SONNET]     │  │         PARALELO         │
│  Conectivos do corpus, abertura de   │  │                          │
│  secoes, sem alineas a/b/c no corpo  │  │  [review_estilo.txt]     │
└──────────────────┬───────────────────┘  └──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 3 — AUDITOR FINAL [OPUS]                                     │
│  Consolida correcoes de prequestionamento + estilo em ambos os      │
│  recursos                                              [*_final.txt] │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPA 4 — GERADOR .DOCX [SONNET]                                   │
│  Dois documentos .docx independentes: REsp + RE com formatacao      │
│  oficial                                                [2x .docx]   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Workflow 8 — Script: gerar_peticao.py

```
┌─────────────────────────────────────────────────────────────────────┐
│  INPUT                                                              │
│  Parametros: --titulo, --cliente, --conteudo, --cidade,             │
│  --advogado, --oab                                     [Args CLI]    │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  CARREGAR TEMPLATE                                                  │
│  Template .dotx com identidade visual do escritorio (timbre,        │
│  fontes, margens)                                         [.dotx]    │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  FORMATAR                                                           │
│  Classificar paragrafos e aplicar: Arial 12pt, espacamento 1.5,    │
│  margens 3cm/2cm                                      [Formatado]    │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  OUTPUT                                                             │
│  Salvar em output_claude/ com nome padronizado                      │
│  TIPO_CLIENTE_DATA.docx                                   [.docx]    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Workflow 9 — Script: indexar_vf.py

```
┌─────────────────────────────────────────────────────────────────────┐
│  ESCANEAR                                                           │
│  Varrer diretorios de Clientes/ buscando sufixo _vf.docx           │
│                                                        [Pastas]      │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  CLASSIFICAR                                                        │
│  Organizar por tipo: REsp, RE, HC, Contestacao, Apelacao, etc.     │
│                                                        [Tipos]       │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  OUTPUT                                                             │
│  Gerar data/indice_vf.json com 668+ arquivos indexados              │
│                                                  [indice_vf.json]    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Workflow 10 — Script: placeholder_scan.py

```
┌─────────────────────────────────────────────────────────────────────┐
│  ESCANEAR                                                           │
│  Buscar pastas pipeline/ de todos os casos ativos                   │
│                                                        [Pastas]      │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  DETECTAR                                                           │
│  Escanear .txt e .docx por padroes [PLACEHOLDER] e [VERIFICAR]     │
│                                                        [Matches]     │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  OUTPUT                                                             │
│  Gerar data/placeholders.json com relatorio por caso                │
│                                               [placeholders.json]    │
└─────────────────────────────────────────────────────────────────────┘
```

---

# PARTE II — 10 Workflows Sugeridos

> **Principio de design:** Todo workflow sugerido inclui etapa(s) de **VALIDACAO** obrigatoria(s) antes de entregar qualquer output. Nenhum conteudo gerado por IA sai do sistema sem ser verificado. Workflows criticos incluem **GATE HUMANO** que bloqueia a geracao final ate aprovacao do advogado.

## Tabela Geral

| # | Workflow | Tipo | Prioridade | Esforco |
|---|---|---|---|---|
| 1 | Gestao de Prazos | Cmd + Cron | [CRITICO] | 3-5 dias |
| 2 | Pesquisa Jurisprudencial | Command | [QUICK WIN] | 2-3 dias |
| 3 | Embargos de Declaracao | Pipeline | [QUICK WIN] | 5-7 dias |
| 4 | Comunicacao com Clientes | Command | [QUICK WIN] | 2-3 dias |
| 5 | Agravo de Instrumento | Pipeline | [MEDIO] | 1 semana |
| 6 | Preparacao Audiencias | Pipeline | [MEDIO] | 4-5 dias |
| 7 | Triagem Novos Casos | Pipeline | [MEDIO] | 1 semana |
| 8 | Monitoramento Legislativo | Cmd + Cron | [MEDIO] | 1 semana |
| 9 | Pareceres Internos | Pipeline | [MEDIO] | 3-4 dias |
| 10 | Verificador Jurisprudencia | Skill Global | [CRITICO] | 3-5 dias |

---

## Workflow Sugerido #1 — Gestao de Prazos Processuais [CRITICO]

| Campo | Detalhe |
|---|---|
| **Tipo / Prioridade** | Command + Cron Diario | [CRITICO] |
| **Trigger** | `/prazos hoje` | `/prazos semana` | `/prazos criticos` | Cron diario 8h |
| **Problema** | Perda de prazo = responsabilidade civil + sancao OAB. Gestao manual e fragil e falha sob pressao. |

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER                                                            │
│  /prazos (manual) ou cron diario 8h (automatico)                    │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VARREDURA [SCRIPT]                                                 │
│  Script Python varre todos os caso.json e extrai array prazos[]     │
│                                                    [Lista prazos]    │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  CALCULO [SCRIPT]                                                   │
│  Calcular dias uteis descontando feriados forenses e recessos       │
│  (tabela local)                                   [Dias restantes]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VALIDADOR [SONNET]                                                 │
│  Verificar consistencia: prazo nao pode ser anterior a intimacao,   │
│  datas fazem sentido?                             [Dados validados]  │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  CLASSIFICACAO                                                      │
│  CRITICO (<3d) | ATENCAO (3-7d) | OK (>7d) + sugestao de pipeline  │
│  por prazo                                            [Semaforo]     │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  OUTPUT                                                             │
│  Painel formatado com semaforo + acao sugerida para cada caso       │
│                                                   [Painel prazos]   │
└─────────────────────────────────────────────────────────────────────┘
```

**ROI:** Risco ZERO de perder prazo. Eliminacao de planilhas manuais. Priorizacao automatica da carga.

### Como Usar

| Mecanismo | Descricao |
|-----------|-----------|
| **Tipo** | **Command** (`.claude/commands/prazos.md`) + **Cron Job** (execucao automatica) |
| **Uso manual** | Digitar `/prazos hoje`, `/prazos semana` ou `/prazos criticos` no Claude Code |
| **Uso automatico** | Configurar cron job diario as 8h que executa o script de varredura e envia o painel para o terminal ou Telegram |
| **Implementacao** | Criar command `/prazos` em `.claude/commands/prazos.md` + script Python `scripts/prazos_monitor.py` com tabela de feriados forenses |
| **Integracao** | Le o campo `prazos[]` do caso.json de cada caso ativo. Nao depende de nenhum outro workflow |

---

## Workflow Sugerido #2 — Pesquisa Jurisprudencial Sob Demanda [QUICK WIN]

| Campo | Detalhe |
|---|---|
| **Tipo / Prioridade** | Command (agente reutilizado) | [QUICK WIN] |
| **Trigger** | `/pesquisa "tema" [--tribunal STJ] [--caso NOME]` |
| **Problema** | Pesquisa manual em sites de tribunais consome 30-60 min por consulta. Resultado incompleto. |

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER                                                            │
│  /pesquisa "clausula de nao concorrencia em contratos de franquia"  │
│                                                        [Query]       │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  PESQUISA [SONNET]                                                  │
│  Pesquisador Jurisprudencial (REUTILIZADO) faz web search em sites  │
│  de tribunais                                    [Resultados brutos] │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VALIDADOR [SONNET]                                                 │
│  Verificar CADA citacao: numero existe? Relator correto? Data       │
│  confere? Ementa bate?                           [Citacoes validadas]│
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  FILTRAGEM                                                          │
│  Remover citacoes nao verificaveis. Marcar incertas com [VERIFICAR] │
│                                                     [Lista limpa]    │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ANEXAR PETICAO [SONNET]  *** OBRIGATORIO ***                       │
│  Para cada jurisprudencia encontrada, localizar e anexar a peticao  │
│  que originou aquele julgado. Sem peticao originaria = sem entrega. │
│                                                   [Peticao anexada]  │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  OUTPUT                                                             │
│  5-10 precedentes verificados com tendencia + peticao originaria    │
│  anexada a cada um                                 [pesquisa_*.txt]  │
└─────────────────────────────────────────────────────────────────────┘
```

> **REGRA OBRIGATORIA — ANEXAR PETICAO:** Sempre que uma jurisprudencia for encontrada e validada, e OBRIGATORIO localizar e anexar a peticao que originou aquele julgado. Esta etapa nao pode ser pulada. Jurisprudencias sem peticao originaria identificada devem ser marcadas como [VERIFICAR — PETICAO PENDENTE] e nao compoe o output final aprovado.

**ROI:** Economia 30-60 min/consulta. Agente ja existe — menor esforco de implementacao.

### Como Usar

| Mecanismo | Descricao |
|-----------|-----------|
| **Tipo** | **Command** (`.claude/commands/pesquisa.md`) — reutiliza agente existente |
| **Uso** | Digitar `/pesquisa "tema"` no Claude Code. Flags opcionais: `--tribunal STJ`, `--caso NOME` |
| **Exemplos** | `/pesquisa "dano moral em relacao de consumo"` ou `/pesquisa "prescricao intercorrente" --tribunal STJ --caso SILVA` |
| **Implementacao** | Criar command `/pesquisa` que invoca o agente `pesquisador-jurisprudencial` (ja existe no pipeline de recursos) como servico autonomo |
| **Output** | Salva em `pesquisas/pesquisa_YYYYMMDD_HHMMSS.txt`. Se `--caso` informado, salva na pasta do caso |

---

## Workflow Sugerido #3 — Pipeline de Embargos de Declaracao [QUICK WIN]

| Campo | Detalhe |
|---|---|
| **Tipo / Prioridade** | Pipeline Multi-Agente (6 etapas) | [QUICK WIN] |
| **Trigger** | `/caso embargos [--decisao arquivo.pdf] [--prequestionamento]` |
| **Problema** | Peca intermediaria mais frequente. 2-4h manual. Essencial para prequestionamento pre-recurso. |

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER                                                            │
│  /caso embargos — identifica ultima decisao no caso.json            │
│  automaticamente                                       [caso.json]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ANALISTA VICIOS [OPUS]                                             │
│  Identifica omissoes, obscuridades e contradicoes na decisao        │
│  judicial                                        [vicios_decisao.txt]│
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  REDATOR EMBARGOS [OPUS]                                            │
│  Redige embargos estruturados por vicio, com prequestionamento      │
│  quando aplicavel                                   [embargos_v1.txt]│
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VALIDADOR ESTILO [SONNET]                                          │
│  Verifica aderencia ao perfil-estilo.md: conectivos, vocabulario,   │
│  ausencia de anti-padroes...                    [review_estilo.txt]  │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VALIDADOR JURIDICO [SONNET]                                        │
│  Verifica: todos os vicios cobertos? Artigos corretos? Citacoes     │
│  existem? Prequestionam...                        [review_jur.txt]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  AUDITOR FINAL [OPUS]                                               │
│  Consolida v1 + reviews. Aplica correcoes sem novos erros. Texto    │
│  definitivo                                      [embargos_final.txt]│
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  GATE HUMANO                                                        │
│  Advogado revisa texto final antes de gerar .docx.                  │
│  Pode editar ou aprovar                               [GO / EDITAR]  │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  GERADOR .DOCX                                                      │
│  gerar_peticao.py com identidade visual do escritorio               │
│                                                  [EMBARGOS_*.docx]   │
└─────────────────────────────────────────────────────────────────────┘
```

**ROI:** R$400-800 economizados por peca. Custo API ~R$6. ROI >60x.

### Como Usar

| Mecanismo | Descricao |
|-----------|-----------|
| **Tipo** | **Pipeline Multi-Agente** disparado por **sub-comando do /caso** |
| **Uso** | Digitar `/caso embargos` no Claude Code. O sistema identifica automaticamente a ultima decisao no caso.json |
| **Flags** | `--decisao arquivo.pdf` (especificar decisao manualmente) / `--prequestionamento` (forcar prequestionamento explicito para preparo de REsp/RE) |
| **Implementacao** | Adicionar sub-comando `embargos` ao hub `/caso` em `.claude/commands/caso.md`. Criar 2 agentes novos em `.claude/agents/`: `analista-vicios-decisorios.md` e `redator-embargos.md`. Reutiliza revisor-estilo e gerador-docx |
| **Fluxo** | O orquestrador-contestacao (Sonnet) pode ser reutilizado como orquestrador, adicionando rota para embargos |

---

## Workflow Sugerido #4 — Comunicacao com Clientes [QUICK WIN]

| Campo | Detalhe |
|---|---|
| **Tipo / Prioridade** | Command | [QUICK WIN] |
| **Trigger** | `/caso relatorio CLIENTE` | `/caso explicar "texto da decisao"` |
| **Problema** | Traduzir juridiques para linguagem simples consome tempo. Falta de comunicacao perde clientes. |

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER                                                            │
│  /caso relatorio SILVA ou /caso explicar "texto da decisao"         │
│                                                       [Dados caso]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ANALISE [SONNET]                                                   │
│  Le caso.json + ultimos artefatos do pipeline. Contextualiza o      │
│  andamento                                            [Contexto]     │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  GERACAO [SONNET]                                                   │
│  Gera dois textos: resumo tecnico (arquivo) + resumo cliente        │
│  (linguagem simples)                                  [2 textos]     │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VALIDADOR [SONNET]                                                 │
│  Verifica: dados sigilosos expostos? Informacao incorreta? Tom      │
│  adequado para leigo?                             [Texto validado]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  GATE HUMANO                                                        │
│  Advogado revisa antes de enviar ao cliente. Pode ajustar tom ou    │
│  conteudo                                             [Aprovado]     │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  OUTPUT                                                             │
│  Texto pronto para enviar por e-mail/WhatsApp ao cliente            │
│                                                  [relatorio_*.txt]   │
└─────────────────────────────────────────────────────────────────────┘
```

**ROI:** Economia 30-60 min/comunicacao. Cliente informado = cliente retido.

### Como Usar

| Mecanismo | Descricao |
|-----------|-----------|
| **Tipo** | **Sub-comandos do /caso** (agente unico, sem pipeline complexo) |
| **Uso** | `/caso relatorio SILVA` (gera relatorio de andamento) ou `/caso explicar "texto da decisao"` (traduz decisao para linguagem leiga) |
| **Implementacao** | Adicionar sub-comandos `relatorio` e `explicar` ao hub `/caso`. Criar 1 agente: `comunicador-cliente.md` (Sonnet) com instrucoes de linguagem acessivel |
| **Output** | Dois arquivos: resumo tecnico (arquivo interno) + resumo cliente (para envio). Salvos em `Clientes/<CLIENTE>/comunicacoes/` |
| **GATE HUMANO** | O advogado SEMPRE revisa antes de enviar ao cliente. O texto gerado e rascunho ate aprovacao |

---

## Workflow Sugerido #5 — Pipeline de Agravo de Instrumento [MEDIO]

| Campo | Detalhe |
|---|---|
| **Tipo / Prioridade** | Pipeline Multi-Agente (7 etapas) | [MEDIO] |
| **Trigger** | `/caso agravo [--decisao arquivo.pdf]` |
| **Problema** | Decisoes interlocutorias prejudiciais exigem resposta rapida com fundamentacao solida. |

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER                                                            │
│  /caso agravo — identifica decisao interlocutoria no caso.json      │
│                                                        [caso.json]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  ANALISTA DECISAO [OPUS]             │  │         PARALELO         │
│  Identifica error in judicando/      │  │                          │
│  procedendo, prejuizo concreto,      │  │  [analise_dec.txt]       │
│  urgencia                            │  │                          │
└──────────────────┬───────────────────┘  └──────────────────────────┘
                   ↓
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  PESQ. JURISP. [SONNET]              │  │         PARALELO         │
│  Jurisprudencia para fumus boni iuris│  │                          │
│  e periculum in mora                 │  │    [jurisp.txt]          │
└──────────────────┬───────────────────┘  └──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VALIDADOR CITACOES [SONNET]                                        │
│  Verificar CADA citacao: numero, relator, data, holding. Remover    │
│  nao-verificaveis                              [jurisp_validada.txt] │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  REDATOR AGRAVO [OPUS]                                              │
│  Redige agravo com pedido de efeito suspensivo/ativo quando         │
│  cabivel                                          [agravo_v1.txt]    │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VALIDADOR ESTILO+JUR [SONNET]                                      │
│  Revisao dupla: aderencia ao estilo + completude juridica +         │
│  prequestionamento                                  [reviews.txt]    │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  AUDITOR FINAL [OPUS]                                               │
│  Consolida correcoes. Texto definitivo do agravo                    │
│                                                  [agravo_final.txt]  │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  GATE HUMANO                                                        │
│  Advogado revisa antes de gerar .docx. Ponto critico: pedido de     │
│  tutela correto?                                     [GO / EDITAR]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  GERADOR .DOCX                                                      │
│  Documento final pronto para protocolo com identidade visual        │
│                                                   [AGRAVO_*.docx]    │
└─────────────────────────────────────────────────────────────────────┘
```

**ROI:** R$600-1200 economizados por peca. Custo API ~R$10. Prazo curto = velocidade critica.

### Como Usar

| Mecanismo | Descricao |
|-----------|-----------|
| **Tipo** | **Pipeline Multi-Agente** disparado por **sub-comando do /caso** |
| **Uso** | Digitar `/caso agravo` no Claude Code. Flag: `--decisao arquivo.pdf` para especificar decisao |
| **Implementacao** | Adicionar sub-comando `agravo` ao hub `/caso`. Criar 2 agentes novos: `analista-decisao-interlocutoria.md` e `redator-agravo.md`. Reutiliza pesquisador-jurisprudencial, revisor-estilo e gerador-docx |
| **Orquestrador** | Usar orquestrador-contestacao (Sonnet) com rota adicional para agravo |
| **GATE HUMANO** | Obrigatorio antes de gerar .docx — advogado valida pedido de efeito suspensivo/ativo |

---

## Workflow Sugerido #6 — Preparacao para Audiencias [MEDIO]

| Campo | Detalhe |
|---|---|
| **Tipo / Prioridade** | Pipeline Leve (5 etapas) | [MEDIO] |
| **Trigger** | `/caso audiencia instrucao\|conciliacao\|julgamento` |
| **Problema** | 3-6h de preparacao manual na vespera, sob pressao. Risco de esquecer pontos relevantes. |

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER                                                            │
│  /caso audiencia instrucao — le caso.json + todos os artefatos do   │
│  pipeline                                              [caso.json]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  ANALISTA [OPUS]                     │  │         PARALELO         │
│  Resumo do caso, pontos-chave,       │  │                          │
│  cronologia, contradicoes da parte   │  │    [resumo.txt]          │
│  adversa                             │  │                          │
└──────────────────┬───────────────────┘  └──────────────────────────┘
                   ↓
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  ESTRATEGISTA [SONNET]               │  │         PARALELO         │
│  Roteiro de perguntas, argumentos    │  │                          │
│  orais, pontos de atencao por tipo   │  │   [estrategia.txt]       │
│  de audiencia                        │  │                          │
└──────────────────┬───────────────────┘  └──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VALIDADOR [SONNET]                                                 │
│  Cruzar briefing com caso.json: todos os fatos cobertos? Provas     │
│  mencionadas? Testemunhas...                          [Validado]     │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  CONSOLIDADOR [SONNET]                                              │
│  Monta briefing de 2-3 paginas: resumo + perguntas + argumentos +   │
│  riscos                                            [briefing.txt]    │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  OUTPUT .DOCX                                                       │
│  Briefing compacto e imprimivel para levar na audiencia             │
│                                                  [BRIEFING_*.docx]   │
└─────────────────────────────────────────────────────────────────────┘
```

**ROI:** Preparacao em 30 min ao inves de 4h. Zero pontos esquecidos.

### Como Usar

| Mecanismo | Descricao |
|-----------|-----------|
| **Tipo** | **Pipeline Leve** disparado por **sub-comando do /caso** |
| **Uso** | `/caso audiencia instrucao` ou `/caso audiencia conciliacao` ou `/caso audiencia julgamento` |
| **Implementacao** | Adicionar sub-comando `audiencia` ao hub `/caso` com argumento obrigatorio do tipo. Criar 1 agente novo: `estrategista-audiencia.md` (Sonnet). Reutiliza analista-juridico (Opus) |
| **Output** | Briefing .docx de 2-3 paginas salvo em `Clientes/<CLIENTE>/audiencias/` — imprimivel para levar ao forum |
| **Dica** | Rodar na vespera da audiencia. O caso.json ja tem todos os dados necessarios |

---

## Workflow Sugerido #7 — Triagem de Novos Casos [MEDIO]

| Campo | Detalhe |
|---|---|
| **Tipo / Prioridade** | Pipeline (5 etapas) | [MEDIO] |
| **Trigger** | `/triagem NOME_CLIENTE` |
| **Problema** | 1-3h para avaliar viabilidade. Muitas vezes resulta em declinar — tempo sem retorno. |

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER                                                            │
│  /triagem SILVA — cria caso.json com status "triagem"               │
│                                                        [caso.json]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ANALISTA VIABILIDADE [OPUS]                                        │
│  Analisa documentos, identifica teses viaveis, pontos fracos,       │
│  riscos processuais                              [analise_viab.txt]  │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  PESQ. JURISP. [SONNET]                                             │
│  Busca precedentes para cada tese. Calcula taxa de sucesso          │
│  aproximada                                      [precedentes.txt]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VALIDADOR [SONNET]                                                 │
│  Verificar citacoes de precedentes. Score faz sentido? Riscos       │
│  identificados sao reais?                        [Dados validados]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  PARECERISTA [OPUS]                                                 │
│  Gera parecer: ACEITAR / RECUSAR / NEGOCIAR com score, justificativa│
│  e condicoes                                    [parecer_viab.txt]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  OUTPUT                                                             │
│  Parecer de 1 pagina com score, teses, riscos e recomendacao        │
│  objetiva                                             [Parecer]      │
└─────────────────────────────────────────────────────────────────────┘
```

**ROI:** Triagem em 15 min ao inves de 2h. Decisoes baseadas em dados, nao intuicao.

### Como Usar

| Mecanismo | Descricao |
|-----------|-----------|
| **Tipo** | **Command proprio** (`.claude/commands/triagem.md`) com pipeline de 5 etapas |
| **Uso** | Digitar `/triagem NOME_CLIENTE` no Claude Code. Jogar os documentos do caso potencial na pasta antes de rodar |
| **Implementacao** | Criar command `/triagem` separado do `/caso`. Criar 2 agentes novos: `analista-viabilidade.md` (Opus) e `parecerista.md` (Opus). Reutiliza pesquisador-jurisprudencial |
| **Output** | Parecer de viabilidade salvo em `Clientes/<CLIENTE>/parecer_viabilidade.txt`. Atualiza caso.json com score e recomendacao |
| **Fluxo pos-triagem** | Se aceitar: `/novo-caso` cria a estrutura completa. Se recusar: pasta fica como registro de declinio |

---

## Workflow Sugerido #8 — Monitoramento Legislativo Semanal [MEDIO]

| Campo | Detalhe |
|---|---|
| **Tipo / Prioridade** | Command + Cron Semanal | [MEDIO] |
| **Trigger** | `/legislacao semana` | `/legislacao impacto CASO` | Cron semanal (segunda 8h) |
| **Problema** | Mudancas legislativas impactam casos ativos. Acompanhamento manual e falho e inconsistente. |

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER                                                            │
│  Cron semanal (segunda 8h) ou /legislacao semana                    │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  PESQUISA [SONNET]                                                  │
│  Web search em DOU, informativos STJ/STF, sites legislativos por    │
│  area de atuacao                                    [mudancas.txt]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VALIDADOR [SONNET]                                                 │
│  Verificar: lei/sumula citada existe? Data correta? Texto do        │
│  dispositivo confere?                           [Mudancas validadas] │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  CRUZAMENTO [SCRIPT]                                                │
│  Cruzar mudancas com tipo_acao dos casos ativos em caso.json        │
│                                                    [impactos.txt]    │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  OUTPUT                                                             │
│  Relatorio: "Mudancas que impactam seus casos" com referencia       │
│  cruzada                                       [legislacao_sem.txt]  │
└─────────────────────────────────────────────────────────────────────┘
```

**ROI:** Escritorio sempre atualizado. Zero argumentos com legislacao revogada.

### Como Usar

| Mecanismo | Descricao |
|-----------|-----------|
| **Tipo** | **Command** (`.claude/commands/legislacao.md`) + **Cron Job semanal** |
| **Uso manual** | `/legislacao semana` (relatorio geral) ou `/legislacao impacto SILVA` (impacto em caso especifico) |
| **Uso automatico** | Configurar cron semanal (segunda 8h) que executa o agente e salva relatorio em `relatorios/legislacao_semana_YYYYMMDD.txt` |
| **Implementacao** | Criar command `/legislacao` + agente `monitor-legislativo.md` (Sonnet com web search). Script auxiliar cruza mudancas com caso.json de cada caso ativo |
| **Integracao** | Le o campo `tipo_acao` de cada caso.json para filtrar mudancas relevantes |

---

## Workflow Sugerido #9 — Pareceres Internos [MEDIO]

| Campo | Detalhe |
|---|---|
| **Tipo / Prioridade** | Pipeline Leve (4 etapas) | [MEDIO] |
| **Trigger** | `/parecer "tema ou questao juridica"` |
| **Problema** | Pareceres consomem 2-3h. Raciocinio estrategico fica sem registro formal. |

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER                                                            │
│  /parecer "prescricao intercorrente em execucao fiscal"             │
│                                                        [Tema]        │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ANALISTA TEMATICO [OPUS]                                           │
│  Pesquisa aprofundada com web search + jurisprudencia relevante      │
│  sobre o tema                                   [pesquisa_tema.txt]  │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  REDATOR PARECER [OPUS]                                             │
│  Redacao no estilo do escritorio com fundamentacao juridica         │
│  estruturada                                      [parecer_w1.txt]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VALIDADOR [SONNET]                                                 │
│  Verificar citacoes, coerencia argumentativa, completude, aderencia │
│  ao estilo                                          [review.txt]     │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  AUDITOR [OPUS]                                                     │
│  Aplica correcoes do validador. Texto definitivo do parecer         │
│                                                 [parecer_final.txt]  │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  OUTPUT .DOCX                                                       │
│  Parecer formatado pronto para arquivo interno                      │
│                                                   [PARECER_*.docx]   │
└─────────────────────────────────────────────────────────────────────┘
```

**ROI:** Pareceres em 15 min ao inves de 2-3h. Conhecimento documentado.

### Como Usar

| Mecanismo | Descricao |
|-----------|-----------|
| **Tipo** | **Command proprio** (`.claude/commands/parecer.md`) com pipeline leve de 4 etapas |
| **Uso** | Digitar `/parecer "tema ou questao"` no Claude Code. Ex: `/parecer "prescricao intercorrente em execucao fiscal"` |
| **Implementacao** | Criar command `/parecer` + 2 agentes novos: `analista-tematico.md` (Opus) e `redator-parecer.md` (Opus). Reutiliza revisor-estilo como validador |
| **Output** | Parecer .docx salvo em `pareceres/PARECER_TEMA_DATA.docx` — pronto para arquivo interno |
| **Vinculacao a caso** | Flag opcional `--caso NOME` para salvar o parecer dentro da pasta do caso em vez de `pareceres/` |

---

## Workflow Sugerido #10 — Verificador de Jurisprudencia (Pre-Protocolo) [CRITICO]

| Campo | Detalhe |
|---|---|
| **Tipo / Prioridade** | Skill Global — integravel a TODOS os pipelines | [CRITICO] |
| **Trigger** | Automatico antes de gerar .docx em qualquer pipeline (OBRIGATORIO) |
| **Problema** | Citacao fabricada por IA = sancao OAB + responsabilidade civil. Risco numero 1 do sistema. |

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER (AUTOMATICO)                                               │
│  Executado antes da etapa Gerador .docx em TODOS os pipelines do   │
│  sistema                                          [Texto da peca]    │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  EXTRACAO [SCRIPT]                                                  │
│  Regex + LLM identifica todos os numeros de processo, sumulas e     │
│  teses citados no texto                           [Lista citacoes]   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VALIDADOR 1 — EXISTENCIA [SONNET]                                  │
│  Web search CADA numero no STJ/STF/TJ. O processo existe? A decisao │
│  existe?                                            [Existe: S/N]    │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VALIDADOR 2 — HOLDING [SONNET]                                     │
│  A ementa REAL diz o que a peca afirma? Relator e data batem?       │
│  Tese correta?                                    [Holding: OK/NOK]  │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  VALIDADOR 3 — VIGENCIA [SONNET]                                    │
│  A jurisprudencia ainda esta vigente? Foi superada? Houve mudanca   │
│  de entendimento?                                  [Vigente: S/N]    │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  GATE HUMANO OBRIGATORIO                                            │
│  Se QUALQUER citacao nao verificada: marca [VERIFICAR] e BLOQUEIA   │
│  geracao .docx                                      [GO / BLOQUEIO]  │
└─────────────────────────────┬───────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  RELATORIO                                                          │
│  Lista completa: citacao | status (OK/VERIFICAR/REMOVIDA) | fonte   │
│  de verificacao                                  [verif_jurisp.txt]  │
└─────────────────────────────────────────────────────────────────────┘
```

**ROI:** PREVINE SANCAO OAB. Elimina risco #1. Deve ser implementado ANTES de qualquer outra melhoria.

### Como Usar

| Mecanismo | Descricao |
|-----------|-----------|
| **Tipo** | **Skill global** (`.claude/skills/verificador-jurisprudencia/SKILL.md`) — se integra a TODOS os pipelines |
| **Uso automatico** | NAO e um command que o Paulo digita. E uma etapa que roda AUTOMATICAMENTE dentro de todos os pipelines antes do Gerador .docx |
| **Uso manual** | Pode ser invocado diretamente com `/verificar-jurisp ARQUIVO.txt` para checar citacoes de qualquer texto |
| **Implementacao** | Criar skill `verificador-jurisprudencia` + script `scripts/extrair_citacoes.py` (regex para numeros de processo CNJ). Modificar TODOS os pipelines existentes (contestacao + recursos) para incluir esta etapa antes do gerador-docx |
| **GATE** | Se qualquer citacao falhar na verificacao, o pipeline PARA e marca [VERIFICAR] no texto. Nao gera .docx ate o advogado resolver |
| **Prioridade** | Implementar PRIMEIRO — antes de qualquer outro workflow sugerido. Protege o Paulo de sancao OAB |

---

## Resumo Final

10 workflows atuais documentados com diagramas visuais.
10 workflows sugeridos, TODOS com etapas de **VALIDACAO** obrigatorias.
Workflows criticos incluem **GATE HUMANO** pre-protocolo.

**Prioridade absoluta:** Workflow #10 (Verificador de Jurisprudencia) deve ser implementado ANTES de qualquer outro — elimina o risco #1 do sistema (sancao OAB por citacao fabricada).

O sistema v2.0 cobre ~15-20% das atividades. Com os 10 workflows sugeridos: **70-80%**.

---

*Documento 07 | Abril 2026 | Analise Critica — Sistema de Workflow Juridico | Gastao da Rosa & Moukarzel | Confidencial*
