# Mapeamento Completo dos Workflows do Projeto

**Projeto:** teste-IA — Sistema de Documentos Juridicos  
**Autor:** Paulo Ekke Moukarzel Junior  
**Gerado em:** 03/04/2026  
**Totais:** 10 workflows | 15 agentes | 3 scripts | 2 pipelines multi-agente

---

## 1. SKILLS (2 workflows)

### 1.1 paulo-estilo-juridico

| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/skills/paulo-estilo-juridico/SKILL.md` |
| **Proposito** | Motor de redacao juridica no estilo do Dr. Paulo Moukarzel |
| **Input** | Info do cliente + documentos do caso |
| **Output** | `.docx` em `Clientes/<CLIENTE>/output_claude/` |

**5 etapas:**

1. **Coletar informacoes** — Nome, tipo de peca, tribunal, processo, documentos originais, bases legais
2. **Consultar pecas _vf** — Buscar documentos finalizados do mesmo tipo para replicar estrutura
3. **Consultar perfil de estilo** — Ler `perfil-estilo.md` (conectivos, formulas, padroes de 292 pecas reais)
4. **Redigir** — Aplicar 13 principios obrigatorios (fontes primarias, cadeia documental, precisao processual, etc.)
5. **Gerar .docx** — Executar `gerar_peticao.py` -> Arial 12pt, espacamento 1.5, margens juridicas

---

### 1.2 criar-agentes

| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/skills/criar-agentes/SKILL.md` |
| **Proposito** | Criar agentes especializados seguindo padroes Anthropic |

**4 etapas:**

1. **Entender escopo** — O que faz, o que nao faz, quem invoca, ferramentas necessarias
2. **Consultar referencia de ferramentas**
3. **Rascunhar .md** — Frontmatter + responsabilidades/processo/formato
4. **Revisar contra checklist** — Salvar em `.claude/agents/`

---

## 2. COMMANDS (3 workflows)

### 2.1 /novo-caso

| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/commands/novo-caso.md` |
| **Proposito** | Criar caso novo com estrutura de pastas |

**5 etapas:**

1. **Coletar dados** — Nome MAIUSCULO, processo CNJ, vara, polo, parte adversa, prazo fatal
2. **Confirmar com usuario** — Exibir resumo antes de criar
3. **Criar pastas** — `Clientes/<CLIENTE>/pipeline/` + `output_claude/`
4. **Gerar caso.json** — Metadados e pipeline vazio
5. **Exibir confirmacao** — Proximos passos disponiveis

---

### 2.2 /caso (hub de gestao)

| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/commands/caso.md` |

| Sub-comando | Funcao |
|---|---|
| `status <cliente>` | Status detalhado do caso (le caso.json, calcula dias ate prazo) |
| `listar` | Painel de todos os casos ativos |
| `prazos` | Casos ordenados por urgencia (VENCIDO > URGENTE > OK > CONCLUIDO) |
| `contestacao <cliente>` | Dispara pipeline completo de contestacao |
| `recurso <cliente>` | Dispara pipeline de recursos (REsp/RE) |
| `placeholders` | Lista placeholders pendentes via `placeholder_scan.py` |
| `indexar` | Atualiza indice de arquivos _vf via `indexar_vf.py` |

---

### 2.3 /doit_like_me

| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/commands/doit_like_me.md` |
| **Proposito** | Ativar a skill `paulo-estilo-juridico` imediatamente |

---

## 3. PIPELINES MULTI-AGENTE (2 workflows)

### 3.1 Pipeline de Contestacao

| Campo | Valor |
|---|---|
| **Orquestrador** | `orquestrador-contestacao` (Sonnet) |
| **Trigger** | `/caso contestacao <cliente>` |
| **Agentes/run** | ~7 agentes executados por run |

```
ETAPA 1 (paralelo):
    analista-juridico-contestacao (Opus)       -> analysis_<cliente>.txt
    pesquisador-magistrado (Sonnet)            -> perfil_magistrado_<cliente>.txt

ETAPA 2 (sequencial):
    redator-contestacao (Opus)                 -> contestacao_<cliente>_v1.txt

ETAPA 3 (paralelo):
    revisor-juridico-contestacao (Sonnet)      -> review_juridico_<cliente>.txt
    revisor-linguistico-contestacao (Sonnet)   -> review_linguistico_<cliente>.txt

ETAPA 4 (sequencial):
    auditor-final-contestacao (Opus)           -> contestacao_<cliente>_final.txt

ETAPA 5 (sequencial):
    gerador-docx (Sonnet)                      -> CONTESTACAO_<CLIENTE>_<DATA>.docx
```

---

### 3.2 Pipeline de Recursos (REsp/RE/AREsp)

| Campo | Valor |
|---|---|
| **Orquestrador** | `orquestrador-recursos` (Opus) |
| **Trigger** | `/caso recurso <cliente>` |

```
ETAPA 1 (paralelo):
    pesquisador-jurisprudencial (Sonnet)       -> jurisprudencia_verificada.txt
    redator-resp (Opus)                        -> resp_<cliente>.txt
    redator-re (Opus)                          -> re_<cliente>.txt

ETAPA 2 (paralelo):
    revisor-prequestionamento (Sonnet)         -> relatorio de prequestionamento
    revisor-estilo-juridico (Sonnet)           -> relatorio de conformidade de estilo

ETAPA 3 (sequencial):
    auditor-final (Opus)                       -> *_final.txt

ETAPA 4 (sequencial):
    gerador-docx (Sonnet)                      -> .docx em output_claude/
```

---

## 4. SCRIPTS UTILITARIOS (3 workflows)

### 4.1 gerar_peticao.py

| Campo | Valor |
|---|---|
| **Proposito** | Gerar .docx formatado a partir de texto |
| **Etapas** | Carregar template .dotx -> Classificar paragrafos -> Formatar -> Salvar |
| **Params** | `--titulo`, `--cliente`, `--conteudo`, `--cidade`, `--advogado`, `--oab` |

---

### 4.2 indexar_vf.py

| Campo | Valor |
|---|---|
| **Proposito** | Indexar pecas finalizadas (_vf.docx) por tipo |
| **Etapas** | Escanear diretorios -> Classificar por tipo -> Gerar `data/indice_vf.json` |
| **Output** | JSON com 668+ arquivos organizados por tipo |

---

### 4.3 placeholder_scan.py

| Campo | Valor |
|---|---|
| **Proposito** | Encontrar placeholders nao resolvidos em pecas |
| **Etapas** | Buscar pastas pipeline/ -> Escanear .txt/.docx -> Extrair `[PLACEHOLDER]` -> Gerar `data/placeholders.json` |

---

## 5. RESUMO GERAL

| Tipo | Qtd | Workflows |
|---|---|---|
| Skills | 2 | paulo-estilo-juridico, criar-agentes |
| Commands | 3 | /novo-caso, /caso (8 sub-comandos), /doit_like_me |
| Pipelines | 2 | Contestacao (5 etapas), Recursos (4 etapas) |
| Scripts | 3 | gerar_peticao.py, indexar_vf.py, placeholder_scan.py |
| **TOTAL** | **10** | + 15 agentes especializados |

### Agentes por Funcao

| Funcao | Agentes | Modelo |
|---|---|---|
| Analise/Pesquisa | analista-juridico, pesquisador-magistrado, pesquisador-jurisprudencial | Opus/Sonnet |
| Redacao | redator-contestacao, redator-resp, redator-re | Opus |
| Revisao | revisor-juridico, revisor-linguistico, revisor-prequestionamento, revisor-estilo | Sonnet |
| Auditoria | auditor-final-contestacao, auditor-final | Opus |
| Geracao | gerador-docx | Sonnet |
| Orquestracao | orquestrador-contestacao, orquestrador-recursos | Sonnet/Opus |
