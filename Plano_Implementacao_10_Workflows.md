# Implementacao dos 10 Novos Workflows — Plano Mestre

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementar 10 novos workflows juridicos que elevam a cobertura do sistema de ~15-20% para ~70-80% das atividades do escritorio.

**Architecture:** Sistema baseado em agentes Claude Code (.md) + commands + skills + scripts Python. Cada pipeline segue o padrao: coleta → analise → redacao (Opus) → revisao (Sonnet) → auditoria (Opus) → verificacao jurisprudencial → geracao .docx. O `caso.md` e o hub de roteamento; cada pipeline complexo (6+ etapas) tem orquestrador dedicado.

**Tech Stack:** Claude Code agents/commands/skills (.md), Python 3 (python-docx, regex), caso.json como fonte de verdade.

**Spec source:** `workflows/07_workflows_mapeamento.md` (Parte II)

---

## Agentes de Execucao

> 5 agentes especializados que CONSTROEM os artefatos do plano. Cada task e despachada para o agente com a competencia correta. Validadores rodam entre fases para garantir qualidade.

### AE-1: `python-scripter` — Desenvolvedor Python

**Tasks atribuidas:** 0.1, 1.1, 8.1 (step 2)
**Modelo:** Opus
**Competencias requeridas:**
- Python 3 (regex, json, argparse, pathlib, datetime)
- Calculo de dias uteis com feriados forenses (SC + federais + recessos)
- Padroes CNJ de numeracao processual (REsp, RE, HC, AREsp, etc.)
- Testes manuais via CLI com output JSON
- Encoding UTF-8 para textos juridicos com acentuacao

**Artefatos:** 3 scripts — `extrair_citacoes.py`, `prazos_monitor.py`, `legislacao_monitor.py`

### AE-2: `agent-architect` — Arquiteto de Agentes Claude Code

**Tasks atribuidas:** 3.1, 3.2, 3.3, 4.1, 5.1, 5.2, 5.3, 6.1, 7.2, 8.1 (step 1), 9.1 (steps 1-2)
**Modelo:** Opus
**Competencias requeridas:**
- Formato YAML frontmatter de agentes Claude Code (name, description, model, tools)
- Definicao precisa de tools por papel (Read/Write para redatores, Agent/TodoWrite para orquestradores)
- Processo juridico brasileiro: CPC, tipos de peca, estrutura de peticoes
- Estilo Paulo Moukarzel: 13 principios obrigatorios, formulas de abertura/encerramento
- Padrao de pipelines sequenciais e paralelos com Agent tool
- Consultar agentes existentes em `.claude/agents/` como referencia de formato
- Consultar `perfil-estilo.md` para regras de redacao

**Artefatos:** 13 agentes `.md`

### AE-3: `command-builder` — Construtor de Commands

**Tasks atribuidas:** 0.3, 1.2, 2.1, 3.4, 4.2, 5.4, 6.2, 7.1, 8.1 (step 3), 9.1 (step 3)
**Modelo:** Sonnet
**Competencias requeridas:**
- Formato de commands Claude Code (`$ARGUMENTS`, parsing de sub-comandos)
- Roteamento por sub-comando com fallback para help
- Invocacao de Agent tool dentro de commands (com model e subagent_type)
- Integracao com caso.json (leitura, atualizacao de campos)
- Flags e opcoes CLI (`--tribunal`, `--caso`, `--decisao`, `--prequestionamento`)
- Consultar commands existentes em `.claude/commands/` como referencia de formato

**Artefatos:** 6 commands `.md` novos + 5 sub-comandos em `caso.md`

### AE-4: `skill-designer` — Designer de Skills

**Tasks atribuidas:** 0.2
**Modelo:** Opus
**Competencias requeridas:**
- Formato SKILL.md com YAML frontmatter (name, description, triggers)
- Design de workflow multi-etapa com gates condicionais
- Integracao skill ↔ script Python (chamada via Bash)
- Padrao de GATE HUMANO (bloqueio condicional antes de prosseguir)
- Consultar `paulo-estilo-juridico/SKILL.md` como referencia estrutural

**Artefatos:** 1 skill — `verificador-jurisprudencia`

### AE-5: `pipeline-integrator` — Integrador de Pipelines Existentes

**Tasks atribuidas:** 0.4, 1.3, FINAL
**Modelo:** Opus
**Competencias requeridas:**
- Leitura e modificacao cirurgica de `.md` existentes (preservar tudo que nao muda)
- Insercao de etapas intermediarias em pipelines sem quebrar fluxo existente
- Atualizacao de schema caso.json (campos aditivos, backward-compatible)
- Documentacao tecnica (CLAUDE.md) — secoes novas seguindo formato existente
- Diff mental: saber exatamente o que mudou vs. o que permanece

**Artefatos:** 5 arquivos modificados

### VAL: `validator` — Agente Validador (Transversal)

**Tasks atribuidas:** V0, V1, V2, V3, V-FINAL
**Modelo:** Sonnet
**Competencias requeridas:**
- Leitura de todos os artefatos produzidos na fase
- Verificacao de formato YAML frontmatter (parse sem erro)
- Verificacao de coerencia de nomes: agentes referenciados em orquestradores existem?
- Verificacao de paths: scripts chamados nos commands existem?
- Execucao de scripts Python (`python script.py --help`) para confirmar que rodam
- Verificacao de integridade do caso.json schema
- Comparacao cruzada entre o plano e os artefatos produzidos

**Criterios de aprovacao por tipo:**
| Tipo | Criterio |
|------|----------|
| Script `.py` | Executa sem erro com `--help`; produz output esperado com input de teste |
| Agent `.md` | YAML parse OK; model valido; tools existem; description nao vazia |
| Command `.md` | Referencia agents que existem; paths de scripts corretos; sub-comandos documentados |
| Skill `.md` | YAML parse OK; triggers presentes; body com etapas numeradas |
| Modificacao | Diff mostra APENAS a mudanca esperada; nada removido indevidamente |

---

## Matriz de Despacho

```
FASE 0:  AE-1(0.1) → AE-4(0.2) → AE-3(0.3) → AE-5(0.4) → VAL(V0)
              ↕ paralelo
FASE 1:  AE-1(1.1) → AE-3(1.2) → AE-5(1.3) → VAL(V1)

FASE 2:  AE-3(2.1) ─────────────────────────────┐
         AE-2(3.1) ∥ AE-2(3.2) → AE-2(3.3) → AE-3(3.4) ─┤→ VAL(V2)
         AE-2(4.1) → AE-3(4.2) ─────────────────┘

FASE 3:  AE-2(5.1) ∥ AE-2(5.2) → AE-2(5.3) → AE-3(5.4) ─┐
         AE-2(6.1) → AE-3(6.2) ───────────────────────────┤
         AE-3(7.1) ∥ AE-2(7.2) ───────────────────────────┤→ VAL(V3)
         AE-2(8.1s1) ∥ AE-1(8.1s2) → AE-3(8.1s3) ────────┤
         AE-2(9.1s1) ∥ AE-2(9.1s2) → AE-3(9.1s3) ────────┘

FINAL:   AE-5(FINAL) → VAL(V-FINAL)
```

---

## Inventario de Arquivos

### Criar (23 arquivos)

| # | Path | Workflow | Tipo |
|---|---|---|---|
| 1 | `.claude/skills/verificador-jurisprudencia/SKILL.md` | WF#10 | Skill |
| 2 | `.claude/skills/verificador-jurisprudencia/scripts/extrair_citacoes.py` | WF#10 | Script |
| 3 | `.claude/commands/verificar-jurisp.md` | WF#10 | Command |
| 4 | `.claude/commands/prazos.md` | WF#1 | Command |
| 5 | `.claude/skills/paulo-estilo-juridico/scripts/prazos_monitor.py` | WF#1 | Script |
| 6 | `.claude/commands/pesquisa.md` | WF#2 | Command |
| 7 | `.claude/agents/analista-vicios-decisorios.md` | WF#3 | Agent |
| 8 | `.claude/agents/redator-embargos.md` | WF#3 | Agent |
| 9 | `.claude/agents/orquestrador-embargos.md` | WF#3 | Orchestrator |
| 10 | `.claude/agents/comunicador-cliente.md` | WF#4 | Agent |
| 11 | `.claude/agents/analista-decisao-interlocutoria.md` | WF#5 | Agent |
| 12 | `.claude/agents/redator-agravo.md` | WF#5 | Agent |
| 13 | `.claude/agents/orquestrador-agravo.md` | WF#5 | Orchestrator |
| 14 | `.claude/agents/estrategista-audiencia.md` | WF#6 | Agent |
| 15 | `.claude/commands/triagem.md` | WF#7 | Command |
| 16 | `.claude/agents/analista-viabilidade.md` | WF#7 | Agent |
| 17 | `.claude/agents/parecerista.md` | WF#7 | Agent |
| 18 | `.claude/commands/legislacao.md` | WF#8 | Command |
| 19 | `.claude/agents/monitor-legislativo.md` | WF#8 | Agent |
| 20 | `.claude/skills/paulo-estilo-juridico/scripts/legislacao_monitor.py` | WF#8 | Script |
| 21 | `.claude/commands/parecer.md` | WF#9 | Command |
| 22 | `.claude/agents/analista-tematico.md` | WF#9 | Agent |
| 23 | `.claude/agents/redator-parecer.md` | WF#9 | Agent |

### Modificar (5 arquivos)

| # | Path | Mudanca |
|---|---|---|
| 1 | `.claude/commands/caso.md` | Adicionar sub-comandos: embargos, agravo, audiencia, relatorio, explicar |
| 2 | `.claude/commands/novo-caso.md` | Atualizar template caso.json com campos: prazos[], tipo_acao, status, comunicacoes[], audiencias[], decisao_recorrida, viabilidade |
| 3 | `.claude/agents/orquestrador-contestacao.md` | Inserir ETAPA 4.5 (verificacao jurisprudencial) antes do gerador-docx |
| 4 | `.claude/agents/orquestrador-recursos.md` | Inserir etapa de verificacao jurisprudencial antes do gerador-docx |
| 5 | `CLAUDE.md` | Documentar novos commands, agentes e workflows |

---

## Decisoes Arquiteturais

1. **Orquestrador por familia de pipeline** — pipelines complexos (6+ etapas) tem orquestrador dedicado; pipelines leves (4-5 etapas sequenciais) embutem orquestracao no command
2. **WF#10 como gate pre-docx** — verifica DEPOIS da auditoria final, ANTES da geracao .docx (custo-eficiente: so verifica o texto definitivo)
3. **caso.json aditivo** — novos campos sao opcionais, default null/[]. Nenhuma breaking change
4. **Todos os novos pipelines incluem WF#10 desde o dia 1** — sem retrofit
5. **`caso.md` como router** — continua sendo o hub central de despacho

---

## Grafo de Dependencias

```
FASE 0: WF#10 (Verificador Jurisp) ← IMPLEMENTAR PRIMEIRO
    ↓ modifica orquestrador-contestacao + orquestrador-recursos
    ↓ cria skill + script + command

FASE 1: WF#1 (Prazos) ← INDEPENDENTE, pode rodar paralelo com Fase 0

FASE 2: WF#2, #3, #4 ← DEPENDEM de WF#10 estar pronto (exceto #4)
    WF#2 (Pesquisa) — reutiliza pesquisador-jurisprudencial
    WF#3 (Embargos) — novo pipeline, inclui verificacao
    WF#4 (Comunicacao) — independente

FASE 3: WF#5, #6, #7, #8, #9 ← DEPENDEM de WF#10
    WF#5 (Agravo) — novo pipeline completo
    WF#6 (Audiencia) — pipeline leve, sem docx formal
    WF#7 (Triagem) — command independente
    WF#8 (Legislacao) — command + cron
    WF#9 (Pareceres) — pipeline leve
```

---

## FASE 0 — WF#10: Verificador de Jurisprudencia [CRITICO]

> Prioridade ABSOLUTA. Previne sancao OAB por citacao fabricada. Modifica todos os pipelines existentes.

### Task 0.1: Script extrair_citacoes.py

**Executor:** `AE-1: python-scripter` (Opus)
**Files:**
- Create: `.claude/skills/verificador-jurisprudencia/scripts/extrair_citacoes.py`

- [ ] **Step 1: Criar script de extracao de citacoes**

```python
#!/usr/bin/env python3
"""Extrai citacoes de jurisprudencia de textos juridicos."""
import re, json, sys, argparse
from pathlib import Path

# Padroes CNJ e tribunais
PATTERNS = [
    # REsp, RE, HC, RHC, AREsp, AgRg, AgInt, EDcl
    (r"((?:REsp|RE|HC|RHC|AREsp|AgRg|AgInt|EDcl)\s*(?:n[.ºo]*\s*)?[\d.,/\-]+)", "recurso"),
    # Sumula N ou Sumula Vinculante N
    (r"(S[uú]mula\s+(?:Vinculante\s+)?n?[.ºo]*\s*\d+)", "sumula"),
    # Tema N (repercussao geral)
    (r"(Tema\s+(?:n[.ºo]*\s*)?\d+)", "tema"),
    # Citacao inline com Min./Rel.
    (r"\(([^)]*(?:Min\.|Rel\.)[^)]*(?:julg|DJ|DJe)[^)]*)\)", "citacao_inline"),
]

def extrair(texto: str) -> list[dict]:
    citacoes = []
    seen = set()
    for linha_num, linha in enumerate(texto.splitlines(), 1):
        for pattern, tipo in PATTERNS:
            for match in re.finditer(pattern, linha, re.IGNORECASE):
                raw = match.group(1).strip()
                key = re.sub(r"\s+", " ", raw.lower())
                if key not in seen:
                    seen.add(key)
                    citacoes.append({
                        "tipo": tipo,
                        "texto": raw,
                        "linha": linha_num,
                        "contexto": linha.strip()[:200],
                        "status": "pendente"
                    })
    return citacoes

def main():
    parser = argparse.ArgumentParser(description="Extrai citacoes de jurisprudencia")
    parser.add_argument("arquivo", help="Caminho do arquivo .txt para analisar")
    parser.add_argument("--output", help="Caminho do JSON de saida (default: stdout)")
    args = parser.parse_args()

    texto = Path(args.arquivo).read_text(encoding="utf-8")
    resultado = extrair(texto)

    output = json.dumps({"total": len(resultado), "citacoes": resultado}, 
                        ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Extraidas {len(resultado)} citacoes -> {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
```

- [ ] **Step 2: Testar com um arquivo existente**

Run: `python .claude/skills/verificador-jurisprudencia/scripts/extrair_citacoes.py <qualquer_peca_existente>.txt`
Expected: JSON com lista de citacoes encontradas

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/verificador-jurisprudencia/scripts/extrair_citacoes.py
git commit -m "feat: script de extracao de citacoes jurisprudenciais para WF#10"
```

---

### Task 0.2: Skill verificador-jurisprudencia

**Executor:** `AE-4: skill-designer` (Opus)
**Files:**
- Create: `.claude/skills/verificador-jurisprudencia/SKILL.md`

- [ ] **Step 1: Criar SKILL.md**

O arquivo deve seguir a estrutura do `paulo-estilo-juridico/SKILL.md` com:

```yaml
---
name: verificador-jurisprudencia
description: >
  Verifica autenticidade de TODAS as citacoes de jurisprudencia em pecas juridicas
  antes da geracao .docx. Executa automaticamente em todos os pipelines ou 
  manualmente via /verificar-jurisp. NAO usar para redacao, revisao de estilo 
  ou analise de documentos.
triggers:
  - verificar jurisprudencia
  - checar citacoes
  - validar julgados
---
```

Body com 6 etapas:
1. EXTRACAO — executar `extrair_citacoes.py` no texto final
2. VALIDACAO EXISTENCIA — para cada citacao, `pesquisador-jurisprudencial` verifica se o processo/sumula existe no site oficial do tribunal
3. VALIDACAO HOLDING — a ementa real diz o que a peca afirma? Relator e data batem?
4. VALIDACAO VIGENCIA — jurisprudencia ainda vigente? Superada?
5. GATE HUMANO — se QUALQUER citacao nao verificada: marcar `[VERIFICAR]` e BLOQUEAR geracao .docx
6. RELATORIO — tabela: citacao | status (OK/VERIFICAR/REMOVIDA) | fonte

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/verificador-jurisprudencia/SKILL.md
git commit -m "feat: skill verificador-jurisprudencia (WF#10)"
```

---

### Task 0.3: Command verificar-jurisp

**Executor:** `AE-3: command-builder` (Sonnet)
**Files:**
- Create: `.claude/commands/verificar-jurisp.md`

- [ ] **Step 1: Criar command**

O command recebe `$ARGUMENTS` como path do arquivo. Deve:
1. Executar `extrair_citacoes.py` no arquivo via Bash
2. Para cada citacao extraida, invocar Agent `pesquisador-jurisprudencial` com a citacao como query
3. Compilar relatorio com status de cada citacao
4. Se houver citacoes nao verificadas, listar com `[VERIFICAR]` e alertar o usuario
5. Salvar relatorio em `pipeline/verificacao_jurisp_<nome>.txt`

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/verificar-jurisp.md
git commit -m "feat: command /verificar-jurisp para verificacao manual (WF#10)"
```

---

### Task 0.4: Integrar nos pipelines existentes

**Executor:** `AE-5: pipeline-integrator` (Opus)
**Files:**
- Modify: `.claude/agents/orquestrador-contestacao.md`
- Modify: `.claude/agents/orquestrador-recursos.md`

- [ ] **Step 1: Modificar orquestrador-contestacao.md**

Inserir entre a ETAPA 4 (auditor-final) e ETAPA 5 (gerador-docx):

```
### ETAPA 4.5 — VERIFICACAO DE JURISPRUDENCIA

1. Executar via Bash: `python .claude/skills/verificador-jurisprudencia/scripts/extrair_citacoes.py pipeline/contestacao_<prefixo>_final.txt --output pipeline/citacoes_<prefixo>.json`
2. Ler o JSON de citacoes
3. Para CADA citacao com status "pendente":
   - Invocar Agent pesquisador-jurisprudencial com a citacao
   - Atualizar status para "confirmada", "nao_encontrada" ou "divergente"
4. Se QUALQUER citacao nao confirmada:
   - Marcar no texto final com [VERIFICAR — citacao nao confirmada]
   - PARAR pipeline e reportar ao usuario
   - NAO prosseguir para ETAPA 5 ate resolucao
5. Salvar relatorio: pipeline/verificacao_jurisp_<prefixo>.txt
6. Atualizar caso.json: etapas.verificacao_jurisp.status = "concluido"
```

- [ ] **Step 2: Modificar orquestrador-recursos.md**

Mesma logica, inserida antes da etapa do gerador-docx. Adaptar para verificar ambos os arquivos (resp_final.txt e re_final.txt).

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/orquestrador-contestacao.md .claude/agents/orquestrador-recursos.md
git commit -m "feat: integrar verificacao jurisprudencial nos pipelines existentes (WF#10)"
```

---

### ✅ CHECKPOINT V0 — Validacao Fase 0

**Executor:** `VAL: validator` (Sonnet)

- [ ] **V0.1: Verificar script extrair_citacoes.py**

Run: `python .claude/skills/verificador-jurisprudencia/scripts/extrair_citacoes.py --help`
Expected: Help text sem erro de importacao

Run: Criar arquivo de teste com citacoes conhecidas (REsp 1.234.567/SP, Sumula 297 STJ) e executar o script
Expected: JSON com 2+ citacoes extraidas, tipos corretos

- [ ] **V0.2: Verificar SKILL.md**

Validar:
- YAML frontmatter parseia sem erro (name, description, triggers presentes)
- Body tem 6 etapas numeradas
- Referencia `extrair_citacoes.py` com path correto
- Referencia `pesquisador-jurisprudencial` (agente existente)

- [ ] **V0.3: Verificar command verificar-jurisp.md**

Validar:
- Referencia `extrair_citacoes.py` com path que existe
- Referencia Agent `pesquisador-jurisprudencial` (existe em `.claude/agents/`)
- Formato de output `pipeline/verificacao_jurisp_*.txt` documentado
- `$ARGUMENTS` parseado como path de arquivo

- [ ] **V0.4: Verificar modificacoes nos orquestradores**

Validar orquestrador-contestacao.md:
- ETAPA 4.5 existe entre ETAPA 4 e ETAPA 5
- Path do script `extrair_citacoes.py` correto
- Logica de GATE: "NAO prosseguir para ETAPA 5" presente
- Demais etapas INALTERADAS (diff limpo)

Validar orquestrador-recursos.md:
- Mesma logica presente
- Referencia resp_final.txt e re_final.txt

- [ ] **V0.5: Teste de integracao rapido**

Run: Criar texto ficticio com 3 citacoes (1 real, 1 inventada, 1 sumula) → executar `extrair_citacoes.py`
Expected: 3 citacoes extraidas com tipos corretos

**Criterio de aprovacao:** TODOS os V0.x passam. Se QUALQUER falhar → corrigir ANTES de prosseguir.

---

## FASE 1 — WF#1: Gestao de Prazos [CRITICO]

### Task 1.1: Script prazos_monitor.py

**Executor:** `AE-1: python-scripter` (Opus)
**Files:**
- Create: `.claude/skills/paulo-estilo-juridico/scripts/prazos_monitor.py`

- [ ] **Step 1: Criar script**

O script deve:
1. Escanear todos os `caso.json` em `Clientes/*/caso.json`
2. Extrair `prazo_fatal` e `prazo_tipo` de cada caso
3. Calcular dias uteis restantes (descontando feriados forenses SC + recessos)
4. Classificar: CRITICO (<3 dias uteis), ATENCAO (3-7), OK (>7), VENCIDO (<0)
5. Gerar output formatado como tabela

Tabela de feriados deve incluir:
- Feriados federais BR (1/1, 21/4, 1/5, 7/9, 12/10, 2/11, 15/11, 25/12)
- Tiradentes, Corpus Christi (movel), Sexta-feira Santa (movel)
- Recesso forense: 20/12 a 20/01
- Feriados estaduais SC

CLI: `python prazos_monitor.py [hoje|semana|criticos|todos]`
Output: tabela formatada + JSON opcional com `--json`

- [ ] **Step 2: Testar script**

Run: `python .claude/skills/paulo-estilo-juridico/scripts/prazos_monitor.py todos`
Expected: Tabela vazia ou com casos encontrados

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/paulo-estilo-juridico/scripts/prazos_monitor.py
git commit -m "feat: script monitor de prazos processuais (WF#1)"
```

---

### Task 1.2: Command /prazos

**Executor:** `AE-3: command-builder` (Sonnet)
**Files:**
- Create: `.claude/commands/prazos.md`

- [ ] **Step 1: Criar command**

Sub-comandos baseados em `$ARGUMENTS`:
- `hoje` — prazos vencendo hoje
- `semana` — prazos dos proximos 7 dias uteis
- `criticos` — apenas CRITICO + VENCIDO
- (vazio) — todos os prazos ordenados por urgencia

Cada prazo exibido com: cliente, processo, tipo, prazo_fatal, dias restantes, semaforo, pipeline sugerido.

Se houver prazos CRITICOS ou VENCIDOS, exibir alerta em destaque.

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/prazos.md
git commit -m "feat: command /prazos para gestao de prazos (WF#1)"
```

---

### Task 1.3: Atualizar caso.json schema

**Executor:** `AE-5: pipeline-integrator` (Opus)
**Files:**
- Modify: `.claude/commands/novo-caso.md`

- [ ] **Step 1: Adicionar novos campos ao template caso.json**

Campos a adicionar (todos opcionais, default null ou []):
```json
{
  "status": "ativo",
  "tipo_acao": null,
  "prazos": [],
  "comunicacoes": [],
  "audiencias": [],
  "decisao_recorrida": null,
  "viabilidade": null
}
```

O campo `prazos` e um array de objetos: `{"data": "YYYY-MM-DD", "tipo": "contestacao|recurso|...", "descricao": "texto", "status": "pendente|cumprido"}`

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/novo-caso.md
git commit -m "feat: expandir schema caso.json com campos para novos workflows"
```

---

### ✅ CHECKPOINT V1 — Validacao Fase 1

**Executor:** `VAL: validator` (Sonnet)

- [ ] **V1.1: Verificar script prazos_monitor.py**

Run: `python .claude/skills/paulo-estilo-juridico/scripts/prazos_monitor.py --help`
Expected: Help text com sub-comandos (hoje, semana, criticos, todos)

Run: Criar caso.json ficticio em `Clientes/TESTE_PRAZOS/caso.json` com `prazos: [{"data": "2026-04-10", "tipo": "contestacao", "descricao": "teste", "status": "pendente"}]` e executar `prazos_monitor.py todos`
Expected: Tabela com 1 prazo classificado corretamente (CRITICO/ATENCAO/OK)

Run: `python prazos_monitor.py todos --json`
Expected: Output JSON valido

- [ ] **V1.2: Verificar command prazos.md**

Validar:
- Referencia script `prazos_monitor.py` com path correto
- Sub-comandos documentados: hoje, semana, criticos, vazio
- Alerta visual para CRITICO/VENCIDO presente

- [ ] **V1.3: Verificar novo-caso.md modificado**

Validar:
- Novos campos (status, tipo_acao, prazos, comunicacoes, audiencias, decisao_recorrida, viabilidade) presentes no template
- Todos com default null ou []
- Campos existentes INALTERADOS

- [ ] **V1.4: Limpar dados de teste**

Remover `Clientes/TESTE_PRAZOS/` se criado

**Criterio de aprovacao:** TODOS os V1.x passam.

---

## FASE 2 — Quick Wins (WF#2, #3, #4)

> Podem ser implementados em paralelo apos Fase 0 estar completa.

### Task 2.1: WF#2 — Command /pesquisa

**Executor:** `AE-3: command-builder` (Sonnet)
**Files:**
- Create: `.claude/commands/pesquisa.md`

- [ ] **Step 1: Criar command**

Recebe: `$ARGUMENTS` com tema e flags opcionais (`--tribunal STJ`, `--caso NOME`)

Workflow:
1. Parsear argumentos (tema obrigatorio, tribunal e caso opcionais)
2. Invocar Agent `pesquisador-jurisprudencial` com o tema como query
3. Para cada julgado encontrado, pesquisar a peticao originaria (OBRIGATORIO)
4. Marcar julgados sem peticao como `[VERIFICAR — PETICAO PENDENTE]`
5. Salvar output:
   - Se `--caso`: `Clientes/<CLIENTE>/pesquisas/pesquisa_YYYYMMDD.txt`
   - Senao: `pesquisas/pesquisa_YYYYMMDD_HHMMSS.txt`

- [ ] **Step 2: Criar pasta pesquisas/ se nao existir**

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/pesquisa.md
git commit -m "feat: command /pesquisa para jurisprudencia sob demanda (WF#2)"
```

---

### Task 3.1: WF#3 — Agente analista-vicios-decisorios

**Executor:** `AE-2: agent-architect` (Opus)
**Files:**
- Create: `.claude/agents/analista-vicios-decisorios.md`

- [ ] **Step 1: Criar agente**

Seguir padrao de `analista-juridico-contestacao.md`:

```yaml
---
name: analista-vicios-decisorios
description: >
  Analisa decisoes judiciais para identificar vicios embargaveis: omissao, 
  contradicao, obscuridade e erro material (art. 1.022 CPC). Usar ANTES do 
  redator-embargos. NAO usar para redacao, revisao ou geracao de documentos.
model: claude-opus-4-6
tools:
  - Read
  - Glob
---
```

Processo:
1. Ler a decisao judicial (path recebido do orquestrador)
2. Identificar e catalogar cada vicio encontrado:
   - OMISSAO: ponto levantado pela parte que a decisao nao analisou
   - CONTRADICAO: afirmacoes conflitantes no mesmo texto
   - OBSCURIDADE: trechos ambiguos ou incompreensiveis
   - ERRO MATERIAL: datas, valores, nomes incorretos
3. Se flag `--prequestionamento`: identificar dispositivos legais que precisam ser expressamente debatidos para viabilizar REsp/RE futuro
4. Output: `pipeline/vicios_decisorios_<prefixo>.txt` com secoes numeradas por vicio

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/analista-vicios-decisorios.md
git commit -m "feat: agente analista de vicios decisorios (WF#3)"
```

---

### Task 3.2: WF#3 — Agente redator-embargos

**Executor:** `AE-2: agent-architect` (Opus)
**Files:**
- Create: `.claude/agents/redator-embargos.md`

- [ ] **Step 1: Criar agente**

```yaml
---
name: redator-embargos
description: >
  Redige Embargos de Declaracao no estilo juridico de Paulo Ekke Moukarzel Junior,
  estruturados por vicio identificado pelo analista. Usar APOS o analista-vicios-decisorios 
  concluir. NAO usar para contestacoes, recursos ou outras pecas.
model: claude-opus-4-6
tools:
  - Read
  - Write
---
```

Processo:
1. Ler `pipeline/vicios_decisorios_<prefixo>.txt` + `perfil-estilo.md`
2. Consultar pecas _vf de embargos em `data/indice_vf.json` (tipo "Embargos")
3. Redigir embargos com estrutura:
   - Enderecamento
   - Qualificacao ("ja qualificado nos autos")
   - I — DOS FATOS (breve, remissivo a peca anterior)
   - II — DA OMISSAO (se aplicavel)
   - III — DA CONTRADICAO (se aplicavel)
   - IV — DA OBSCURIDADE (se aplicavel)
   - V — DO PREQUESTIONAMENTO (se flag ativa)
   - VI — DOS REQUERIMENTOS
   - Encerramento padrao
4. Aplicar 13 principios obrigatorios do estilo Paulo
5. Output: `pipeline/embargos_<prefixo>_v1.txt`

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/redator-embargos.md
git commit -m "feat: agente redator de embargos de declaracao (WF#3)"
```

---

### Task 3.3: WF#3 — Orquestrador de embargos

**Executor:** `AE-2: agent-architect` (Opus)
**Files:**
- Create: `.claude/agents/orquestrador-embargos.md`

- [ ] **Step 1: Criar orquestrador**

```yaml
---
name: orquestrador-embargos
description: >
  Condutor central do pipeline de Embargos de Declaracao. Coordena 6 etapas sequenciais
  desde analise de vicios ate geracao .docx. Usar quando /caso embargos for invocado.
  NAO usar para contestacoes ou recursos.
model: claude-sonnet-4-6
tools:
  - Agent
  - Read
  - Write
  - Glob
  - TodoWrite
---
```

Pipeline de 6 etapas (todas sequenciais):
1. `analista-vicios-decisorios` (Opus) → vicios_decisorios.txt
2. `redator-embargos` (Opus) → embargos_v1.txt
3. `revisor-estilo-juridico` (Sonnet) → review_estilo.txt [REUTILIZADO]
4. `auditor-final` (Opus) → embargos_final.txt [REUTILIZADO]
5. Verificacao jurisprudencial (skill WF#10)
6. GATE HUMANO → aguardar aprovacao
7. `gerador-docx` (Sonnet) → EMBARGOS_*.docx [REUTILIZADO]

Atualizar caso.json a cada etapa concluida.

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/orquestrador-embargos.md
git commit -m "feat: orquestrador pipeline embargos de declaracao (WF#3)"
```

---

### Task 3.4: WF#3 — Adicionar sub-comando embargos ao caso.md

**Executor:** `AE-3: command-builder` (Sonnet)
**Files:**
- Modify: `.claude/commands/caso.md`

- [ ] **Step 1: Adicionar rota `embargos` ao hub /caso**

Na secao de deteccao de sub-comandos, adicionar:
- `embargos <cliente>` → ler caso.json → invocar Agent `orquestrador-embargos`
- Flags: `--decisao <path>` (especificar decisao manualmente), `--prequestionamento` (forcar prequestionamento)

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/caso.md
git commit -m "feat: sub-comando /caso embargos (WF#3)"
```

---

### Task 4.1: WF#4 — Agente comunicador-cliente

**Executor:** `AE-2: agent-architect` (Opus)
**Files:**
- Create: `.claude/agents/comunicador-cliente.md`

- [ ] **Step 1: Criar agente**

```yaml
---
name: comunicador-cliente
description: >
  Gera relatorios de andamento e explicacoes de decisoes em linguagem acessivel
  para clientes leigos. Produz dois textos: resumo tecnico (arquivo interno) e 
  resumo cliente (para envio). Usar via /caso relatorio ou /caso explicar.
  NAO usar para redacao de pecas juridicas ou comunicacoes internas.
model: claude-sonnet-4-6
tools:
  - Read
  - Write
---
```

Processo:
1. Ler caso.json + ultimos artefatos do pipeline
2. Gerar resumo tecnico (registro interno, linguagem juridica)
3. Gerar resumo cliente (linguagem simples, sem jargao, tom empatico)
4. VALIDADOR interno: verificar que nao expoe dados sigilosos, informacao esta correta, tom adequado para leigo
5. Output: `Clientes/<CLIENTE>/comunicacoes/relatorio_YYYYMMDD.txt` + `explicacao_YYYYMMDD.txt`

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/comunicador-cliente.md
git commit -m "feat: agente comunicador-cliente (WF#4)"
```

---

### Task 4.2: WF#4 — Sub-comandos relatorio e explicar no caso.md

**Executor:** `AE-3: command-builder` (Sonnet)
**Files:**
- Modify: `.claude/commands/caso.md`

- [ ] **Step 1: Adicionar rotas**

- `relatorio <cliente>` → invocar Agent `comunicador-cliente` com modo "relatorio"
- `explicar <texto>` → invocar Agent `comunicador-cliente` com modo "explicar" + texto fornecido
- Ambos incluem GATE HUMANO: exibir texto gerado e pedir aprovacao antes de considerar "pronto para envio"

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/caso.md
git commit -m "feat: sub-comandos /caso relatorio e /caso explicar (WF#4)"
```

---

### ✅ CHECKPOINT V2 — Validacao Fase 2

**Executor:** `VAL: validator` (Sonnet)

- [ ] **V2.1: Verificar command pesquisa.md (WF#2)**

Validar:
- Referencia Agent `pesquisador-jurisprudencial` (existe)
- Parsing de `$ARGUMENTS` com tema + flags opcionais
- Paths de output corretos (com e sem `--caso`)
- Obrigatoriedade de pesquisar peticao originaria documentada

- [ ] **V2.2: Verificar pipeline embargos completo (WF#3)**

Validar agentes criados (3 arquivos):
- `analista-vicios-decisorios.md`: YAML OK, model opus, tools [Read, Glob], art. 1.022 CPC mencionado
- `redator-embargos.md`: YAML OK, model opus, tools [Read, Write], referencia perfil-estilo.md
- `orquestrador-embargos.md`: YAML OK, model sonnet, tools incluem Agent+TodoWrite

Validar coerencia do orquestrador:
- Referencia `analista-vicios-decisorios` → existe em `.claude/agents/`?
- Referencia `redator-embargos` → existe em `.claude/agents/`?
- Referencia `revisor-estilo-juridico` → existe em `.claude/agents/`? (REUTILIZADO)
- Referencia `auditor-final` → existe em `.claude/agents/`? (REUTILIZADO)
- Referencia `gerador-docx` → existe em `.claude/agents/`? (REUTILIZADO)
- Etapa de verificacao jurisprudencial (WF#10) presente?

Validar sub-comando em caso.md:
- Rota `embargos` adicionada
- Invoca `orquestrador-embargos`
- Flags `--decisao` e `--prequestionamento` documentadas

- [ ] **V2.3: Verificar comunicador-cliente (WF#4)**

Validar:
- `comunicador-cliente.md`: YAML OK, model sonnet, tools [Read, Write]
- Dois modos documentados (relatorio + explicar)
- Validador interno de dados sigilosos mencionado
- Sub-comandos `relatorio` e `explicar` adicionados ao caso.md
- GATE HUMANO presente em ambos

- [ ] **V2.4: Verificar integridade do caso.md**

Run: Contar quantos sub-comandos o caso.md reconhece agora
Expected: Sub-comandos originais + embargos + relatorio + explicar (minimo 3 novos)
Validar: Nenhum sub-comando original foi removido ou quebrado

**Criterio de aprovacao:** TODOS os V2.x passam.

---

## FASE 3 — Workflows Medios (WF#5, #6, #7, #8, #9)

### Task 5.1: WF#5 — Agente analista-decisao-interlocutoria

**Executor:** `AE-2: agent-architect` (Opus)
**Files:**
- Create: `.claude/agents/analista-decisao-interlocutoria.md`

- [ ] **Step 1: Criar agente**

```yaml
---
name: analista-decisao-interlocutoria
description: >
  Analisa decisoes interlocutorias para identificar error in judicando/procedendo,
  prejuizo concreto e urgencia para agravo de instrumento. Usar ANTES do redator-agravo.
  NAO usar para decisoes finais (sentencas/acordaos) — usar analista-juridico para esses.
model: claude-opus-4-6
tools:
  - Read
  - Glob
---
```

Output: `pipeline/analise_interlocutoria_<prefixo>.txt` com: erro identificado, prejuizo concreto, urgencia, fumus boni iuris, periculum in mora.

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/analista-decisao-interlocutoria.md
git commit -m "feat: agente analista de decisao interlocutoria (WF#5)"
```

---

### Task 5.2: WF#5 — Agente redator-agravo

**Executor:** `AE-2: agent-architect` (Opus)
**Files:**
- Create: `.claude/agents/redator-agravo.md`

- [ ] **Step 1: Criar agente**

```yaml
---
name: redator-agravo
description: >
  Redige Agravo de Instrumento no estilo juridico de Paulo Ekke Moukarzel Junior,
  com pedido de efeito suspensivo/ativo quando cabivel. Usar APOS analista-decisao-interlocutoria
  e pesquisador-jurisprudencial concluirem. NAO usar para outros recursos.
model: claude-opus-4-6
tools:
  - Read
  - Write
---
```

Estrutura: Enderecamento ao TJ → Qualificacao → I SINTESE DA DEMANDA → II DO CABIMENTO → III DO FUMUS BONI IURIS → IV DO PERICULUM IN MORA → V DO PEDIDO DE EFEITO SUSPENSIVO/ATIVO → VI DOS REQUERIMENTOS

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/redator-agravo.md
git commit -m "feat: agente redator de agravo de instrumento (WF#5)"
```

---

### Task 5.3: WF#5 — Orquestrador agravo

**Executor:** `AE-2: agent-architect` (Opus)
**Files:**
- Create: `.claude/agents/orquestrador-agravo.md`

- [ ] **Step 1: Criar orquestrador**

7 etapas:
1. PARALELO: analista-decisao-interlocutoria (Opus) + pesquisador-jurisprudencial (Sonnet)
2. Validacao de citacoes (Sonnet) — verificar cada citacao encontrada
3. redator-agravo (Opus)
4. PARALELO: revisor-estilo-juridico (Sonnet) + revisao juridica (validacao completude)
5. auditor-final (Opus)
6. Verificacao jurisprudencial (WF#10)
7. GATE HUMANO → gerador-docx (Sonnet)

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/orquestrador-agravo.md
git commit -m "feat: orquestrador pipeline agravo de instrumento (WF#5)"
```

---

### Task 5.4: WF#5 — Sub-comando agravo no caso.md

**Executor:** `AE-3: command-builder` (Sonnet)
**Files:**
- Modify: `.claude/commands/caso.md`

- [ ] **Step 1: Adicionar rota `agravo`**

- `agravo <cliente>` → ler caso.json → invocar Agent `orquestrador-agravo`
- Flag: `--decisao <path>` para especificar decisao interlocutoria

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/caso.md
git commit -m "feat: sub-comando /caso agravo (WF#5)"
```

---

### Task 6.1: WF#6 — Agente estrategista-audiencia

**Executor:** `AE-2: agent-architect` (Opus)
**Files:**
- Create: `.claude/agents/estrategista-audiencia.md`

- [ ] **Step 1: Criar agente**

```yaml
---
name: estrategista-audiencia
description: >
  Prepara briefing estrategico para audiencias (instrucao, conciliacao, julgamento).
  Gera roteiro de perguntas, argumentos orais e pontos de atencao. Usar via /caso audiencia.
  NAO usar para redacao de pecas escritas.
model: claude-sonnet-4-6
tools:
  - Read
  - Write
  - WebSearch
---
```

Output: briefing de 2-3 paginas com: resumo do caso, pontos-chave, perguntas sugeridas, argumentos orais, riscos, jurisprudencia relevante.

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/estrategista-audiencia.md
git commit -m "feat: agente estrategista de audiencia (WF#6)"
```

---

### Task 6.2: WF#6 — Sub-comando audiencia no caso.md

**Executor:** `AE-3: command-builder` (Sonnet)
**Files:**
- Modify: `.claude/commands/caso.md`

- [ ] **Step 1: Adicionar rota `audiencia`**

Pipeline leve embutido no command (sem orquestrador separado):
1. Ler caso.json + artefatos do pipeline
2. Invocar Agent `analista-juridico-contestacao` (reutilizado) para resumo
3. Invocar Agent `estrategista-audiencia` em paralelo para estrategia
4. Consolidar briefing
5. Gerar .docx via `gerar_peticao.py` com titulo "BRIEFING_AUDIENCIA"
6. Salvar em `Clientes/<CLIENTE>/audiencias/`

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/caso.md
git commit -m "feat: sub-comando /caso audiencia (WF#6)"
```

---

### Task 7.1: WF#7 — Command /triagem

**Executor:** `AE-3: command-builder` (Sonnet)
**Files:**
- Create: `.claude/commands/triagem.md`

- [ ] **Step 1: Criar command**

Recebe `$ARGUMENTS` como nome do cliente potencial. Workflow:
1. Criar caso.json com `status: "triagem"` (via /novo-caso adaptado)
2. Invocar Agent `analista-viabilidade` (Opus) para avaliar documentos
3. Invocar Agent `pesquisador-jurisprudencial` (Sonnet) para precedentes [REUTILIZADO]
4. Validacao: verificar citacoes e coerencia do score
5. Invocar Agent `parecerista` (Opus) para parecer formal
6. Atualizar caso.json com score e recomendacao
7. Exibir resultado: ACEITAR / RECUSAR / NEGOCIAR

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/triagem.md
git commit -m "feat: command /triagem para novos casos (WF#7)"
```

---

### Task 7.2: WF#7 — Agentes analista-viabilidade e parecerista

**Executor:** `AE-2: agent-architect` (Opus)
**Files:**
- Create: `.claude/agents/analista-viabilidade.md`
- Create: `.claude/agents/parecerista.md`

- [ ] **Step 1: Criar analista-viabilidade**

Model: claude-opus-4-6, Tools: Read, Glob. Analisa documentos do caso potencial e identifica: teses viaveis, pontos fracos, riscos processuais, prescricao, qualidade da prova.

- [ ] **Step 2: Criar parecerista**

Model: claude-opus-4-6, Tools: Read, Write. Gera parecer formal com: score 1-10, recomendacao (ACEITAR/RECUSAR/NEGOCIAR), justificativa, condicoes sugeridas (honorarios, probabilidade de exito).

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/analista-viabilidade.md .claude/agents/parecerista.md
git commit -m "feat: agentes analista-viabilidade e parecerista (WF#7)"
```

---

### Task 8.1: WF#8 — Command /legislacao + agente + script

**Executores:** `AE-2: agent-architect` (Step 1) + `AE-1: python-scripter` (Step 2) + `AE-3: command-builder` (Step 3) — Steps 1 e 2 em PARALELO, Step 3 sequencial
**Files:**
- Create: `.claude/commands/legislacao.md`
- Create: `.claude/agents/monitor-legislativo.md`
- Create: `.claude/skills/paulo-estilo-juridico/scripts/legislacao_monitor.py`

- [ ] **Step 1: Criar agente monitor-legislativo** `[AE-2]`

```yaml
---
name: monitor-legislativo
description: >
  Monitora mudancas legislativas relevantes para os casos ativos do escritorio.
  Pesquisa DOU, informativos STJ/STF e sites legislativos. Usar via /legislacao.
  NAO usar para pesquisa jurisprudencial (usar pesquisador-jurisprudencial).
model: claude-sonnet-4-6
tools:
  - WebSearch
  - WebFetch
  - Read
  - Write
---
```

- [ ] **Step 2: Criar script legislacao_monitor.py** `[AE-1]`

Funcao: cruzar mudancas legislativas encontradas com campo `tipo_acao` dos caso.json ativos. Output: relatorio de impacto por caso.

- [ ] **Step 3: Criar command /legislacao** `[AE-3]`

Sub-comandos: `semana` (relatorio geral), `impacto <CASO>` (impacto em caso especifico).

- [ ] **Step 4: Commit**

```bash
git add .claude/commands/legislacao.md .claude/agents/monitor-legislativo.md .claude/skills/paulo-estilo-juridico/scripts/legislacao_monitor.py
git commit -m "feat: monitoramento legislativo semanal (WF#8)"
```

---

### Task 9.1: WF#9 — Command /parecer + agentes

**Executores:** `AE-2: agent-architect` (Steps 1-2) + `AE-3: command-builder` (Step 3) — Steps 1 e 2 em PARALELO, Step 3 sequencial
**Files:**
- Create: `.claude/commands/parecer.md`
- Create: `.claude/agents/analista-tematico.md`
- Create: `.claude/agents/redator-parecer.md`

- [ ] **Step 1: Criar agente analista-tematico** `[AE-2]`

Model: claude-opus-4-6, Tools: Read, WebSearch, WebFetch. Pesquisa aprofundada sobre tema juridico especifico com jurisprudencia + doutrina.

- [ ] **Step 2: Criar agente redator-parecer** `[AE-2]`

Model: claude-opus-4-6, Tools: Read, Write. Redige parecer interno no estilo do escritorio. Estrutura: I QUESTAO, II FUNDAMENTACAO, III CONCLUSAO.

- [ ] **Step 3: Criar command /parecer** `[AE-3]`

Pipeline leve de 4 etapas inline:
1. analista-tematico (Opus) → pesquisa_tema.txt
2. redator-parecer (Opus) → parecer_v1.txt
3. revisor-estilo-juridico (Sonnet) → review.txt [REUTILIZADO]
4. auditor-final (Opus) → parecer_final.txt [REUTILIZADO]
5. gerador-docx → PARECER_*.docx [REUTILIZADO]

Flag: `--caso NOME` para vincular a um caso existente.

- [ ] **Step 4: Commit**

```bash
git add .claude/commands/parecer.md .claude/agents/analista-tematico.md .claude/agents/redator-parecer.md
git commit -m "feat: pipeline de pareceres internos (WF#9)"
```

---

### ✅ CHECKPOINT V3 — Validacao Fase 3

**Executor:** `VAL: validator` (Sonnet)

- [ ] **V3.1: Verificar pipeline agravo completo (WF#5)**

Validar agentes (3 arquivos):
- `analista-decisao-interlocutoria.md`: YAML OK, model opus, tools [Read, Glob], menciona error in judicando/procedendo
- `redator-agravo.md`: YAML OK, model opus, tools [Read, Write], referencia perfil-estilo.md, estrutura de agravo presente
- `orquestrador-agravo.md`: YAML OK, model sonnet, 7 etapas, etapas paralelas marcadas, WF#10 integrado

Validar coerencia do orquestrador-agravo:
- Todos os agentes referenciados existem em `.claude/agents/`?
- Etapa de verificacao jurisprudencial presente?
- GATE HUMANO antes do gerador-docx?

Validar sub-comando `agravo` no caso.md

- [ ] **V3.2: Verificar estrategista-audiencia (WF#6)**

Validar:
- `estrategista-audiencia.md`: YAML OK, model sonnet, tools incluem WebSearch
- Sub-comando `audiencia` no caso.md: pipeline leve inline (sem orquestrador)
- Reutiliza `analista-juridico-contestacao` (existe?)
- Output em `Clientes/<CLIENTE>/audiencias/`

- [ ] **V3.3: Verificar triagem completa (WF#7)**

Validar:
- `analista-viabilidade.md`: YAML OK, model opus
- `parecerista.md`: YAML OK, model opus, score 1-10 documentado
- `triagem.md`: referencia ambos os agentes + pesquisador-jurisprudencial (reutilizado)
- Output ACEITAR/RECUSAR/NEGOCIAR documentado
- Atualiza caso.json com score

- [ ] **V3.4: Verificar legislacao (WF#8)**

Validar:
- `monitor-legislativo.md`: YAML OK, model sonnet, tools incluem WebSearch+WebFetch
- `legislacao_monitor.py`: executa com `--help` sem erro
- `legislacao.md`: sub-comandos `semana` e `impacto` documentados
- Script cruzar mudancas com `tipo_acao` dos caso.json

- [ ] **V3.5: Verificar pareceres (WF#9)**

Validar:
- `analista-tematico.md`: YAML OK, model opus, tools incluem WebSearch
- `redator-parecer.md`: YAML OK, model opus, estrutura QUESTAO/FUNDAMENTACAO/CONCLUSAO
- `parecer.md`: pipeline 5 etapas, reutiliza revisor-estilo-juridico + auditor-final + gerador-docx
- Flag `--caso` documentada

- [ ] **V3.6: Verificar integridade GLOBAL do caso.md**

Run: Listar TODOS os sub-comandos reconhecidos pelo caso.md
Expected: listar, prazos, status, contestacao, recurso, placeholders, indexar + embargos, agravo, audiencia, relatorio, explicar (11+ sub-comandos)
Validar: Nenhum sub-comando original removido

- [ ] **V3.7: Contagem total de agentes**

Run: `ls .claude/agents/*.md | wc -l`
Expected: 28 agentes (15 existentes + 13 novos)
Validar: Nenhum agente existente foi sobrescrito ou removido

**Criterio de aprovacao:** TODOS os V3.x passam.

---

### Task FINAL: Atualizar CLAUDE.md

**Executor:** `AE-5: pipeline-integrator` (Opus)
**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Documentar novos workflows**

Adicionar secoes para:
- Novos commands: `/prazos`, `/pesquisa`, `/triagem`, `/legislacao`, `/parecer`, `/verificar-jurisp`
- Novos sub-comandos do `/caso`: embargos, agravo, audiencia, relatorio, explicar
- Nova skill: `verificador-jurisprudencia`
- 13 novos agentes
- Novos scripts: extrair_citacoes.py, prazos_monitor.py, legislacao_monitor.py

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: documentar 10 novos workflows no CLAUDE.md"
```

---

### ✅ CHECKPOINT V-FINAL — Validacao Completa

**Executor:** `VAL: validator` (Sonnet)

- [ ] **VF.1: Inventario de arquivos**

Validar que TODOS os 23 arquivos novos existem nos paths especificados no Inventario:

```bash
# Scripts (3)
test -f .claude/skills/verificador-jurisprudencia/scripts/extrair_citacoes.py
test -f .claude/skills/paulo-estilo-juridico/scripts/prazos_monitor.py
test -f .claude/skills/paulo-estilo-juridico/scripts/legislacao_monitor.py

# Skill (1)
test -f .claude/skills/verificador-jurisprudencia/SKILL.md

# Commands (6)
test -f .claude/commands/verificar-jurisp.md
test -f .claude/commands/prazos.md
test -f .claude/commands/pesquisa.md
test -f .claude/commands/triagem.md
test -f .claude/commands/legislacao.md
test -f .claude/commands/parecer.md

# Agents (13)
test -f .claude/agents/analista-vicios-decisorios.md
test -f .claude/agents/redator-embargos.md
test -f .claude/agents/orquestrador-embargos.md
test -f .claude/agents/comunicador-cliente.md
test -f .claude/agents/analista-decisao-interlocutoria.md
test -f .claude/agents/redator-agravo.md
test -f .claude/agents/orquestrador-agravo.md
test -f .claude/agents/estrategista-audiencia.md
test -f .claude/agents/analista-viabilidade.md
test -f .claude/agents/parecerista.md
test -f .claude/agents/monitor-legislativo.md
test -f .claude/agents/analista-tematico.md
test -f .claude/agents/redator-parecer.md
```

Expected: 23/23 arquivos existem

- [ ] **VF.2: Verificar modificacoes nos 5 arquivos existentes**

Para cada arquivo modificado, confirmar que:
- `caso.md`: 5 novos sub-comandos adicionados, nenhum original removido
- `novo-caso.md`: 7 novos campos no template, campos originais intactos
- `orquestrador-contestacao.md`: ETAPA 4.5 presente, demais etapas inalteradas
- `orquestrador-recursos.md`: verificacao jurisprudencial presente, demais inalteradas
- `CLAUDE.md`: secoes novas documentando todos os workflows

- [ ] **VF.3: Todos os scripts executam**

```bash
python .claude/skills/verificador-jurisprudencia/scripts/extrair_citacoes.py --help
python .claude/skills/paulo-estilo-juridico/scripts/prazos_monitor.py --help
python .claude/skills/paulo-estilo-juridico/scripts/legislacao_monitor.py --help
```

Expected: 3/3 executam sem erro

- [ ] **VF.4: Coerencia de referencias cruzadas**

Para CADA orquestrador, verificar que TODOS os agentes que ele referencia existem:
- `orquestrador-embargos` → analista-vicios-decisorios, redator-embargos, revisor-estilo-juridico, auditor-final, gerador-docx
- `orquestrador-agravo` → analista-decisao-interlocutoria, pesquisador-jurisprudencial, redator-agravo, revisor-estilo-juridico, auditor-final, gerador-docx

Para CADA command, verificar que os agents/scripts referenciados existem.

- [ ] **VF.5: Zero regressao**

Validar que os 15 agentes originais ainda existem e nao foram modificados (exceto os 2 orquestradores intencionalmente alterados):
```bash
git diff --name-only .claude/agents/
```
Expected: apenas orquestrador-contestacao.md e orquestrador-recursos.md aparecem como modified

**Criterio de aprovacao:** TODOS os VF.x passam. Se QUALQUER falhar → localizar task responsavel e corrigir.

---

## Verificacao End-to-End

Para validar cada workflow implementado:

| Workflow | Teste |
|---|---|
| WF#10 | Rodar `/verificar-jurisp` em uma peca existente com citacoes conhecidas |
| WF#1 | Rodar `/prazos todos` com pelo menos 1 caso.json com prazo_fatal |
| WF#2 | Rodar `/pesquisa "dano moral consumo" --tribunal STJ` |
| WF#3 | Rodar `/caso embargos <cliente>` com caso que tenha decisao |
| WF#4 | Rodar `/caso relatorio <cliente>` e `/caso explicar "texto"` |
| WF#5 | Rodar `/caso agravo <cliente>` com caso que tenha decisao interlocutoria |
| WF#6 | Rodar `/caso audiencia instrucao` com caso ativo |
| WF#7 | Rodar `/triagem TESTE_CLIENTE` com documentos na pasta |
| WF#8 | Rodar `/legislacao semana` |
| WF#9 | Rodar `/parecer "prescricao intercorrente"` |

---

## Resumo

| Fase | Workflows | Arquivos Novos | Arquivos Modificados | Tasks | Validador |
|---|---|---|---|---|---|
| 0 | WF#10 | 3 | 2 | 4 | V0 (5 checks) |
| 1 | WF#1 | 2 | 1 | 3 | V1 (4 checks) |
| 2 | WF#2, #3, #4 | 5 | 1 | 6 | V2 (4 checks) |
| 3 | WF#5, #6, #7, #8, #9 | 13 | 1 | 7 | V3 (7 checks) |
| Final | CLAUDE.md | 0 | 1 | 1 | VF (5 checks) |
| **Total** | **10 workflows** | **23** | **5** | **21 tasks** | **25 checks** |

## Agentes de Execucao — Resumo

| Agente | Codigo | Modelo | Tasks | Artefatos |
|---|---|---|---|---|
| Python Scripter | AE-1 | Opus | 0.1, 1.1, 8.1(s2) | 3 scripts .py |
| Agent Architect | AE-2 | Opus | 3.1-3.3, 4.1, 5.1-5.3, 6.1, 7.2, 8.1(s1), 9.1(s1-2) | 13 agentes .md |
| Command Builder | AE-3 | Sonnet | 0.3, 1.2, 2.1, 3.4, 4.2, 5.4, 6.2, 7.1, 8.1(s3), 9.1(s3) | 6 commands + 5 sub-cmd |
| Skill Designer | AE-4 | Opus | 0.2 | 1 skill .md |
| Pipeline Integrator | AE-5 | Opus | 0.4, 1.3, FINAL | 5 arquivos modificados |
| Validator | VAL | Sonnet | V0, V1, V2, V3, VF | 25 verificacoes |

**Total de despachos estimado:** ~18 (com paralelizacao maxima entre fases e dentro de fases)
