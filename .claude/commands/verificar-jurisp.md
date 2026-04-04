$ARGUMENTS contem o caminho do arquivo a verificar. Se vazio, verificar o ultimo arquivo _final.txt gerado no pipeline do caso ativo.

---

## Execucao

### Passo 1 — Identificar arquivo alvo

Se `$ARGUMENTS` contem um caminho de arquivo:
- Usar diretamente como arquivo alvo

Se `$ARGUMENTS` contem apenas o nome de um cliente:
- Buscar em `Clientes/<CLIENTE>/pipeline/` o arquivo mais recente com sufixo `_final.txt`
- Se nenhum encontrado, informar o usuario e sugerir caminhos possiveis

Se `$ARGUMENTS` esta vazio:
- Listar os ultimos 5 arquivos `*_final.txt` em qualquer `Clientes/*/pipeline/`
- Pedir ao usuario que selecione

### Passo 2 — Executar extracao de citacoes

Executar via Bash:

```bash
python .claude/skills/verificador-jurisprudencia/scripts/extrair_citacoes.py "<arquivo_alvo>" --output "<pasta_pipeline>/citacoes_<prefixo>.json"
```

Ler o JSON gerado. Exibir ao usuario:

```
Encontradas [N] citacoes para verificacao:
  - [N] recursos (REsp, RE, HC, etc.)
  - [N] sumulas
  - [N] temas de repercussao geral
  - [N] citacoes inline
```

Se `total == 0`:

```
Nenhuma citacao de jurisprudencia encontrada no arquivo.
Verificacao concluida — nada a validar.
```

### Passo 3 — Verificar cada citacao

Para CADA citacao extraida com `status: "pendente"`:

1. Invocar Agent `pesquisador-jurisprudencial` (subagent_type: pesquisador-jurisprudencial) com prompt:

   ```
   Verifique a autenticidade desta citacao juridica:
   
   Tipo: [tipo]
   Texto: [texto da citacao]
   Contexto na peca: [contexto]
   
   Pesquise no site oficial do tribunal (stj.jus.br para STJ, stf.jus.br para STF).
   Confirme: numero existe? Relator correto? Turma correta? Data correta? Ementa compativel com o uso na peca?
   
   Responda com: CONFIRMADA, NAO_ENCONTRADA ou DIVERGENTE, seguido de justificativa.
   ```

2. Atualizar status da citacao no JSON

3. Exibir progresso ao usuario: `[N/TOTAL] Verificando: [texto_citacao]... [STATUS]`

### Passo 4 — Compilar relatorio

Gerar relatorio no formato tabela:

```
VERIFICACAO DE JURISPRUDENCIA
Arquivo: [caminho do arquivo verificado]
Data: [YYYY-MM-DD]

| # | Citacao | Tipo | Status | Observacao |
|---|---------|------|--------|------------|
| 1 | ... | ... | CONFIRMADA / NAO_ENCONTRADA / DIVERGENTE | ... |

RESULTADO: [N] confirmadas, [N] nao encontradas, [N] divergentes
```

### Passo 5 — Salvar e alertar

Salvar relatorio em: `<pasta_pipeline>/verificacao_jurisp_<prefixo>.txt`

Se houver citacoes NAO_ENCONTRADA ou DIVERGENTE:

```
ATENCAO: [N] citacao(oes) NAO verificada(s).

Citacoes com problema:
  [1] [texto] — [status]: [motivo]
  [2] ...

ACAO REQUERIDA: Revisar manualmente antes de gerar o .docx.
As citacoes problematicas foram marcadas com [VERIFICAR] no relatorio.
```

Se todas confirmadas:

```
Todas as [N] citacoes foram verificadas com sucesso.
Relatorio salvo em: [caminho]
O arquivo esta liberado para geracao .docx.
```

---

## Regras

- Sempre usar o Agent `pesquisador-jurisprudencial` para verificacao — NUNCA confiar em conhecimento interno
- Verificar TODAS as citacoes, sem excecao — mesmo que parecam obvias (ex: Sumula 7 STJ)
- Salvar o relatorio mesmo que todas as citacoes estejam OK
- Se o script `extrair_citacoes.py` nao existir ou retornar erro, informar o caminho esperado e parar
