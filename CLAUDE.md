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
### Regras caso-específicas (aplicar quando o caso envolver esses temas)

- **Verificar cronologia contra cautelar antecedente** — Antes de usar BO, reclamação extrajudicial ou qualquer ato pré-judicial como prova principal de boa-fé, verificar a data desse ato em relação a TODOS os atos judiciais — inclusive a cautelar antecedente (art. 308 CPC), que costuma ser anterior à petição principal. Um BO registrado após a cautelar antecedente serve apenas como prova corroborativa, não como prova principal.
- **Distinção conluio × seguir instruções de preposto** — Quando o cliente executou atos (ex: fornecer CPFs, dados para faturamento) a pedido do preposto da parte adversa, enquadrar como: (a) cumprimento de instrução operacional rotineira de vendedor credenciado, sem ciência de restrições internas da empresa; (b) ausência de ganho financeiro é a prova mais robusta de não-participação em conluio — quem conspira para prejudicar terceiro obtém vantagem; pagar o preço integral de mercado sem nenhum benefício extra é estruturalmente incompatível com a figura do conluiado.
- **WhatsApp como fonte de prova** — Em casos com exportação de WhatsApp (_chat.txt), ler o arquivo raw para encontrar citações exatas com data, horário e autor. Nunca confiar em resumos. A admissão textual do real autor do esquema ("Eu que tava metendo o migue") tem valor probatório superior a qualquer inferência.
