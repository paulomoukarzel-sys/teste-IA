$ARGUMENTS contem o tema de pesquisa e flags opcionais. Formato: <tema> [--tribunal STJ|STF|TST|TJSC] [--caso NOME_CLIENTE]

---

## Execucao

### Passo 1 — Parsear argumentos

Extrair dos $ARGUMENTS:
- **tema** (obrigatorio): tudo que nao e flag
- **--tribunal** (opcional): filtrar por tribunal especifico (default: todos)
- **--caso** (opcional): vincular pesquisa a um caso existente

Se tema estiver vazio, exibir:

```
Uso: /pesquisa <tema> [--tribunal STJ|STF|TST|TJSC] [--caso NOME_CLIENTE]

Exemplos:
  /pesquisa "dano moral consumo"
  /pesquisa "responsabilidade civil empregador" --tribunal STJ
  /pesquisa "fraude automotiva" --caso Le Motos
```

### Passo 2 — Executar pesquisa

Invocar Agent `pesquisador-jurisprudencial` (subagent_type: pesquisador-jurisprudencial) com prompt:

```
Pesquise jurisprudencia sobre o tema: [tema]
[Se --tribunal: Foque no tribunal: [tribunal]]

Para cada julgado encontrado:
1. Confirme que o numero do processo existe no site oficial do tribunal
2. Extraia: numero, relator, turma/secao, data de julgamento, ementa resumida
3. Pesquise a peticao originaria que deu origem ao julgado (OBRIGATORIO)
4. Se nao encontrar a peticao originaria, marque como [VERIFICAR — PETICAO PENDENTE]

Retorne no formato:
JULGADO 1:
  Numero: REsp X.XXX.XXX/UF
  Relator: Min. Nome
  Turma: X Turma
  Data: DD/MM/YYYY
  Ementa: [resumo]
  Peticao originaria: [encontrada/VERIFICAR]
  Tese: [tese extraida relevante ao tema]
```

### Passo 3 — Compilar resultado

Organizar os julgados encontrados em formato estruturado:

```
PESQUISA JURISPRUDENCIAL
Tema: [tema]
Tribunal: [tribunal ou "todos"]
Data: [YYYY-MM-DD]

JULGADOS ENCONTRADOS: [N]

[lista de julgados formatados]

ALERTAS:
- [N] julgados sem peticao originaria confirmada [VERIFICAR]
```

### Passo 4 — Salvar resultado

Se `--caso` foi especificado:
- Criar pasta se nao existir: `Clientes/<CLIENTE>/pesquisas/`
- Salvar em: `Clientes/<CLIENTE>/pesquisas/pesquisa_YYYYMMDD.txt`

Se `--caso` NAO foi especificado:
- Criar pasta se nao existir: `pesquisas/`
- Salvar em: `pesquisas/pesquisa_YYYYMMDD_HHMMSS.txt`

Exibir ao usuario o caminho do arquivo salvo.

---

## Regras

- Sempre usar o Agent `pesquisador-jurisprudencial` — NUNCA confiar em conhecimento interno para dados de julgados
- Pesquisar peticao originaria e OBRIGATORIO para cada julgado
- Marcar julgados sem peticao como [VERIFICAR — PETICAO PENDENTE]
- Se nenhum julgado encontrado, informar claramente e sugerir termos alternativos
