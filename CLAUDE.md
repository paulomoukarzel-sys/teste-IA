# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Legal document generation system for attorney Paulo Ekke Moukarzel Junior. Built as a Claude Code skill that drafts Brazilian legal documents (petitions, appeals, writs, etc.) following the attorney's specific writing style, extracted from 60+ real legal documents.

## Architecture

```
.claude/
  skills/paulo-estilo-juridico/    # Main skill — legal writing engine
    SKILL.md                       # Workflow, checklists, document type guides
    references/perfil-estilo.md    # Detailed style profile (formulas, patterns, examples)
    scripts/gerar_peticao.py       # Word .docx generator (Python)
    scripts/requirements.txt       # python-docx>=0.8.11
    evals/test_cases.md            # 7 manual test scenarios
  skills/criar-agentes/            # Skill for creating specialized agents
  commands/doit_like_me.md         # Slash command: forces skill activation
  agents/                          # Multi-agent pipeline for legal documents
    analista-juridico-contestacao.md   # Step 1: Document analysis
    pesquisador-magistrado.md          # Step 1 (parallel): Judge research
    redator-contestacao.md             # Step 2: Draft writing (Opus)
    revisor-juridico-contestacao.md    # Step 3: Legal review
    revisor-linguistico-contestacao.md # Step 3 (parallel): Style review
    auditor-final-contestacao.md       # Step 4: Final audit (Opus)
Clientes/                          # Client folders with case documents
```

The skill follows a 5-step workflow: Collect info -> Consult style reference -> Draft -> Review (checklist) -> Generate .docx.

### Multi-Agent Pipeline (Contestação)

```
Step 1 (parallel):  analista-juridico-contestacao (Opus)   ─┐
                    pesquisador-magistrado (Sonnet)         ─┤
Step 2 (sequential): redator-contestacao (Opus)             ─┤
Step 3 (parallel):  revisor-juridico-contestacao (Sonnet)   ─┤
                    revisor-linguistico-contestacao (Sonnet) ─┤
Step 4 (sequential): auditor-final-contestacao (Opus)       ─┘→ .docx
```

Orchestrator launches Steps 1 in parallel, feeds outputs to Step 2, launches Step 3 in parallel, then Step 4 produces the final text for .docx generation.

### Multi-Agent Pipeline (Recursos — REsp/RE)

```
Step 1 (parallel):  pesquisador-jurisprudencial (Sonnet)   ─┐
                    redator-resp (Opus)                     ─┤
                    redator-re (Opus)                       ─┤
Step 2 (parallel):  revisor-prequestionamento (Sonnet)      ─┤
                    revisor-estilo-juridico (Sonnet)        ─┤
Step 3 (sequential): auditor-final (Opus)                   ─┤
Step 4 (sequential): gerador-docx (Sonnet)                  ─┘→ .docx
```

Orchestrator coordinates: Step 1 runs research + drafting in parallel, Step 2 runs dual review, Step 3 consolidates corrections, Step 4 generates .docx files.

## Workflow de Agentes

1. **Criar agentes primeiro** — Usar a skill `criar-agentes` para gerar os arquivos `.md` em `.claude/agents/` ANTES de invocar qualquer agente
2. **Paralelizar via Agent tool** — Tarefas independentes DEVEM ser lançadas em paralelo (múltiplas chamadas Agent no mesmo bloco)
3. **Modelo por papel** — Opus para redação e auditoria final; Sonnet para pesquisa, análise e revisão

## Commands

### Generate .docx from drafted text
```bash
python .claude/skills/paulo-estilo-juridico/scripts/gerar_peticao.py \
  --titulo "CONTESTACAO" --cliente "Nome do Cliente" \
  --conteudo /tmp/peticao.txt --cidade "Florianopolis" \
  --advogado "Paulo Ekke Moukarzel Junior" --oab "12345"
```

Output is always saved to: `<base-dir>/<NOME_CLIENTE>/output_claude/<TIPO>_<CLIENTE>_<DATA>.docx`
The client folder and `output_claude` subfolder are created automatically.

### Install dependencies
```bash
pip install -r .claude/skills/paulo-estilo-juridico/scripts/requirements.txt
```

## Key Conventions

- **Language**: All documents, skill files, and user interaction are in Brazilian Portuguese
- **Legal style**: Formal register, Latin expressions welcome, no bullet points in argumentative body, Roman numeral sections, extensive use of legal connectives ("Nesse sentido,", "Ocorre que,", "Com efeito,")
- **Document output**: Always .docx format, Arial 12pt, 1.5 line spacing, legal margins (3cm left/top, 2cm right/bottom), page numbering in footer
- **Client folders**: Documents organized by client name in UPPERCASE with underscores (e.g., `JOAO_DA_SILVA/output_claude/`)
- **No tempestividade**: Never include "tempestividade" boilerplate in any legal document
- **Skill activation**: Use `/doit_like_me` or any trigger keyword listed in SKILL.md frontmatter to activate the legal writing skill

## Workflow de Casos (Novo)

### Comandos de Gestão
- `/novo-caso` — cria caso.json + estrutura de pastas para um novo cliente
- `/caso listar` — painel de todos os casos ativos com prazo e etapa
- `/caso prazos` — casos ordenados por urgência
- `/caso status <cliente>` — status detalhado de um caso específico
- `/caso contestacao <cliente>` — dispara pipeline completo de contestação
- `/caso recurso <cliente>` — dispara pipeline de recursos (REsp/RE)
- `/caso embargos <cliente>` — dispara pipeline de Embargos de Declaração (WF#3)
- `/caso agravo <cliente>` — dispara pipeline de Agravo de Instrumento (WF#5)
- `/caso audiencia <cliente> <tipo>` — gera briefing estratégico para audiência (WF#6)
- `/caso relatorio <cliente>` — gera relatório de andamento para o cliente (WF#4)
- `/caso explicar <cliente>` — explica decisão em linguagem acessível (WF#4)
- `/caso placeholders` — lista placeholders não resolvidos em todas as peças
- `/caso indexar` — atualiza índice de arquivos _vf
- `/prazos [hoje|semana|criticos|todos]` — monitor de prazos processuais (WF#1)
- `/pesquisa <tema> [--tribunal] [--caso]` — pesquisa jurisprudencial sob demanda (WF#2)
- `/triagem <cliente>` — triagem de viabilidade para casos novos (WF#7)
- `/legislacao [semana|impacto <caso>]` — monitoramento legislativo (WF#8)
- `/parecer <tema> [--caso]` — pipeline de pareceres jurídicos internos (WF#9)
- `/verificar-jurisp <arquivo>` — verificação de citações jurisprudenciais (WF#10)

### Estrutura de Pastas por Cliente
```
Clientes/<NOME_CLIENTE>/
  caso.json              ← fonte única de verdade do caso
  pipeline/              ← arquivos intermediários (análise, rascunhos, revisões)
  output_claude/         ← .docx finais gerados
```

### Arquivos de Infraestrutura
- `data/indice_vf.json` — índice de 668 arquivos _vf por tipo de peça
- `data/placeholders.json` — placeholders pendentes por caso
- Scripts: `indexar_vf.py`, `placeholder_scan.py` em `.claude/skills/paulo-estilo-juridico/scripts/`

### Pipeline de Contestação (Automatizado)
O agente `orquestrador-contestacao` executa todo o pipeline automaticamente:
1. (Paralelo) Analista Jurídico + Pesquisador do Magistrado
2. Redator Principal
3. (Paralelo) Revisor Jurídico + Revisor Linguístico
4. Auditor Final
4.5. Verificação Jurisprudencial (WF#10)
5. Gerador .docx

Use `/caso contestacao <cliente>` para disparar ou chame o agente `orquestrador-contestacao` diretamente.

### Pipeline de Embargos de Declaração (WF#3)

```
1. analista-vicios-decisorios (Opus) → vicios_decisorios.txt
2. redator-embargos (Opus) → embargos_v1.txt
3. revisor-estilo-juridico (Sonnet) [REUTILIZADO]
4. auditor-final (Opus) [REUTILIZADO]
4.5. Verificação Jurisprudencial (WF#10)
5. GATE HUMANO
6. gerador-docx (Sonnet) [REUTILIZADO]
```

Use `/caso embargos <cliente>` — flags: `--decisao <path>`, `--prequestionamento`

### Pipeline de Agravo de Instrumento (WF#5)

```
1. (Paralelo) analista-decisao-interlocutoria (Opus) + pesquisador-jurisprudencial (Sonnet)
2. redator-agravo (Opus)
3. (Paralelo) revisor-estilo-juridico (Sonnet) + validação jurídica
4. auditor-final (Opus) [REUTILIZADO]
4.5. Verificação Jurisprudencial (WF#10)
5. GATE HUMANO
6. gerador-docx (Sonnet) [REUTILIZADO]
```

Use `/caso agravo <cliente>` — flag: `--decisao <path>`

### Pipeline de Pareceres (WF#9)

```
1. analista-tematico (Opus) → pesquisa_tema.txt
2. redator-parecer (Opus) → parecer_v1.txt
3. revisor-estilo-juridico (Sonnet) [REUTILIZADO]
4. auditor-final (Opus) [REUTILIZADO]
5. gerador-docx (Sonnet) [REUTILIZADO]
```

Use `/parecer <tema> [--caso NOME]`

### Novos Agentes (13 total)

| Agente | Workflow | Model | Papel |
|---|---|---|---|
| `analista-vicios-decisorios` | WF#3 | Opus | Identifica vícios decisórios (art. 1.022 CPC) |
| `redator-embargos` | WF#3 | Opus | Redige Embargos de Declaração |
| `orquestrador-embargos` | WF#3 | Sonnet | Coordena pipeline de embargos |
| `comunicador-cliente` | WF#4 | Sonnet | Relatórios e explicações para clientes leigos |
| `analista-decisao-interlocutoria` | WF#5 | Opus | Analisa decisões interlocutórias para agravo |
| `redator-agravo` | WF#5 | Opus | Redige Agravo de Instrumento |
| `orquestrador-agravo` | WF#5 | Sonnet | Coordena pipeline de agravo |
| `estrategista-audiencia` | WF#6 | Sonnet | Briefing estratégico para audiências |
| `analista-viabilidade` | WF#7 | Opus | Analisa viabilidade de casos novos |
| `parecerista` | WF#7 | Opus | Parecer formal de viabilidade |
| `monitor-legislativo` | WF#8 | Sonnet | Monitora mudanças legislativas |
| `analista-tematico` | WF#9 | Opus | Pesquisa jurídica aprofundada |
| `redator-parecer` | WF#9 | Opus | Redige pareceres internos |

### Nova Skill: verificador-jurisprudencia (WF#10)

Verifica autenticidade de TODAS as citações de jurisprudência antes da geração .docx. Integrado em todos os pipelines (contestação, recursos, embargos, agravo, pareceres).

Use `/verificar-jurisp <arquivo>` para verificação manual.

## Scripts Utilitários

| Script | Função | Executar com |
|---|---|---|
| `gerar_peticao.py` | Gera .docx formatado | `python ... --titulo ... --cliente ...` |
| `indexar_vf.py` | Indexa 668+ arquivos _vf | `python .claude/skills/.../indexar_vf.py` |
| `placeholder_scan.py` | Lista placeholders pendentes | `python .claude/skills/.../placeholder_scan.py` |
| `extrair_citacoes.py` | Extrai citações jurisprudenciais | `python .claude/skills/verificador-jurisprudencia/scripts/extrair_citacoes.py <arquivo>` |
| `prazos_monitor.py` | Monitor de prazos processuais | `python .claude/skills/.../prazos_monitor.py [hoje\|semana\|criticos\|todos]` |
| `legislacao_monitor.py` | Cruza legislação com casos | `python .claude/skills/.../legislacao_monitor.py --base .` |

### Regras caso-específicas (aplicar quando o caso envolver esses temas)

- **Verificar cronologia contra cautelar antecedente** — Antes de usar BO, reclamação extrajudicial ou qualquer ato pré-judicial como prova principal de boa-fé, verificar a data desse ato em relação a TODOS os atos judiciais — inclusive a cautelar antecedente (art. 308 CPC), que costuma ser anterior à petição principal. Um BO registrado após a cautelar antecedente serve apenas como prova corroborativa, não como prova principal.
- **Distinção conluio × seguir instruções de preposto** — Quando o cliente executou atos (ex: fornecer CPFs, dados para faturamento) a pedido do preposto da parte adversa, enquadrar como: (a) cumprimento de instrução operacional rotineira de vendedor credenciado, sem ciência de restrições internas da empresa; (b) ausência de ganho financeiro é a prova mais robusta de não-participação em conluio — quem conspira para prejudicar terceiro obtém vantagem; pagar o preço integral de mercado sem nenhum benefício extra é estruturalmente incompatível com a figura do conluiado.
- **WhatsApp como fonte de prova** — Em casos com exportação de WhatsApp (_chat.txt), ler o arquivo raw para encontrar citações exatas com data, horário e autor. Nunca confiar em resumos. A admissão textual do real autor do esquema ("Eu que tava metendo o migue") tem valor probatório superior a qualquer inferência.
