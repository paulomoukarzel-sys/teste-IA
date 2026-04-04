---
name: verificador-jurisprudencia
description: >
  Verifica autenticidade de TODAS as citacoes de jurisprudencia em pecas juridicas
  antes da geracao .docx. Executa automaticamente em todos os pipelines ou
  manualmente via /verificar-jurisp. NAO usar para redacao, revisao de estilo
  ou analise de documentos.
  Triggers: "verificar jurisprudencia", "checar citacoes", "validar julgados",
  "verificar julgados", "conferir citacoes"
---

# Skill: Verificador de Jurisprudencia

Verifica a autenticidade e vigencia de TODAS as citacoes de jurisprudencia presentes em pecas juridicas antes da geracao do .docx final. Previne sancao OAB por citacao fabricada ou superada.

Referencia tecnica: `./scripts/extrair_citacoes.py`

---

## Workflow de Verificacao

### ETAPA 1 — EXTRACAO

Executar o script de extracao no texto final da peca:

```bash
python .claude/skills/verificador-jurisprudencia/scripts/extrair_citacoes.py <arquivo_final.txt> --output <pasta_pipeline>/citacoes_<prefixo>.json
```

Ler o JSON gerado. Se `total == 0`, informar que nenhuma citacao foi encontrada e encerrar com status OK.

### ETAPA 2 — VALIDACAO DE EXISTENCIA

Para CADA citacao com `status: "pendente"`:

1. Invocar Agent `pesquisador-jurisprudencial` com a citacao como query
2. O pesquisador deve verificar no site oficial do tribunal (stj.jus.br, stf.jus.br) se:
   - O numero do processo/sumula existe
   - O relator citado e correto
   - A turma/secao e correta
   - A data de julgamento e correta
3. Atualizar status: `"confirmada"`, `"nao_encontrada"` ou `"divergente"`

### ETAPA 3 — VALIDACAO DE HOLDING

Para cada citacao `"confirmada"` na Etapa 2:

1. Comparar a ementa REAL do julgado com o que a peca afirma
2. Se a peca distorce o holding (cita para sustentar tese oposta ao decidido): marcar como `"holding_divergente"`
3. Se a peca usa corretamente: manter `"confirmada"`

### ETAPA 4 — VALIDACAO DE VIGENCIA

Para cada citacao ainda `"confirmada"`:

1. Verificar se o entendimento foi superado por julgado posterior (overruling)
2. Verificar se a sumula foi cancelada ou revisada
3. Verificar se o tema de repercussao geral foi redefinido
4. Se superada: marcar como `"superada"` com referencia ao julgado que superou

### ETAPA 5 — GATE HUMANO

Compilar resultado final:

- Se TODAS as citacoes estao `"confirmada"`: status APROVADO — prosseguir para geracao .docx
- Se QUALQUER citacao estiver `"nao_encontrada"`, `"divergente"`, `"holding_divergente"` ou `"superada"`:
  - Marcar no texto final com `[VERIFICAR — <motivo>]` ao lado da citacao
  - BLOQUEAR geracao .docx
  - Reportar ao Dr. Paulo com detalhes de cada citacao problematica
  - NAO prosseguir ate que o Dr. Paulo resolva (removendo, substituindo ou confirmando manualmente)

### ETAPA 6 — RELATORIO

Gerar relatorio final em formato tabela:

```
VERIFICACAO DE JURISPRUDENCIA — [nome da peca]
Data: [YYYY-MM-DD]

| # | Citacao | Tipo | Status | Fonte | Observacao |
|---|---------|------|--------|-------|------------|
| 1 | REsp 1.234.567/SP | recurso | CONFIRMADA | stj.jus.br | — |
| 2 | Sumula 297 STJ | sumula | NAO ENCONTRADA | — | Numero inexistente |
| 3 | Tema 1.023 STF | tema | SUPERADA | stf.jus.br | Superado pelo Tema 1.200 |

RESULTADO: APROVADO / BLOQUEADO (N citacoes com problema)
```

Salvar em: `<pasta_pipeline>/verificacao_jurisp_<prefixo>.txt`

---

## Regras

1. **Executar SEMPRE antes do gerador-docx** — nenhuma peca vai para .docx sem passar por esta verificacao
2. **Zero tolerancia** — uma unica citacao nao verificada bloqueia o pipeline inteiro
3. **Pesquisador-jurisprudencial e o unico verificador** — nao confiar em conhecimento interno do modelo para confirmar existencia de julgados
4. **Sumulas e temas tambem verificam** — nao apenas recursos nominados
5. **Citacoes inline contam** — citacoes entre parenteses com Min./Rel. tambem devem ser verificadas
6. **Relatorio e obrigatorio** — mesmo que todas as citacoes estejam OK, gerar o relatorio
