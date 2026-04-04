$ARGUMENTS contem o sub-comando. Opcoes: semana, impacto <CASO>.

---

## Deteccao do sub-comando

Leia os $ARGUMENTS e identifique:
- `semana` → relatorio geral da semana
- `impacto <CASO>` → impacto em caso especifico
- (vazio) → mesmo que `semana`

---

## SUB-COMANDO: `semana`

**Proposito:** Gerar relatorio de mudancas legislativas da ultima semana.

**Execucao:**

1. Invocar Agent `monitor-legislativo` (subagent_type: monitor-legislativo, model: sonnet) com prompt:
   ```
   Pesquise mudancas legislativas relevantes dos ultimos 7 dias:
   - Novas leis, MPs, decretos publicados no DOU
   - Informativos STJ e STF
   - Alteracoes em sumulas ou teses de repercussao geral
   
   Foque em areas relevantes para o escritorio: direito civil, consumidor,
   responsabilidade civil, processual civil, constitucional.
   
   Salve o relatorio em: data/legislacao_semanal_YYYYMMDD.txt
   ```

2. Executar via Bash o cruzamento com casos ativos:
   ```bash
   python .claude/skills/paulo-estilo-juridico/scripts/legislacao_monitor.py --base .
   ```

3. Se o script nao existir, fazer o cruzamento manualmente:
   - Ler todos os caso.json ativos
   - Para cada mudanca legislativa, verificar se o campo tipo_acao corresponde

4. Exibir relatorio ao usuario com alertas por caso impactado.

---

## SUB-COMANDO: `impacto`

**Proposito:** Verificar impacto de mudancas legislativas em caso especifico.

**Parametro:** nome parcial do cliente.

**Execucao:**

1. Localizar pasta do cliente e ler caso.json.

2. Invocar Agent `monitor-legislativo` com prompt focado no tipo_acao do caso.

3. Exibir mudancas relevantes e impacto no caso especifico.

---

## Regras

- Pesquisas legislativas sao informativas — nao modificam caso.json
- Alertas de impacto devem ser claros sobre se a mudanca e favoravel ou desfavoravel
- Se nenhuma mudanca relevante encontrada, informar claramente
