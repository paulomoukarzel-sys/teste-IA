$ARGUMENTS contem o tema do parecer e flags opcionais. Formato: <tema> [--caso NOME_CLIENTE]

---

## Execucao

### Passo 1 — Parsear argumentos

Extrair:
- **tema** (obrigatorio): assunto do parecer
- **--caso** (opcional): vincular a caso existente

Se tema vazio:
```
Uso: /parecer <tema> [--caso NOME_CLIENTE]

Exemplos:
  /parecer "prescricao intercorrente no CPC 2015"
  /parecer "responsabilidade do empregador por ato de preposto" --caso Le Motos
```

### Passo 2 — Pesquisa tematica

Invocar Agent `analista-tematico` (subagent_type: analista-tematico, model: opus) com prompt:

```
Pesquise aprofundadamente sobre o tema: [tema]

Cubra:
1. Legislacao aplicavel (artigos especificos)
2. Jurisprudencia STJ e STF (julgados relevantes com numero)
3. Doutrina (autores e obras de referencia)
4. Correntes interpretativas (majoritaria vs minoritaria)
5. Tendencias recentes dos tribunais

[Se --caso: Contextualize a pesquisa para o caso [cliente] — leia caso.json em Clientes/<PASTA>/]

Salve em: [Se --caso: Clientes/<PASTA>/pipeline/pesquisa_tema_<prefixo>.txt]
          [Senao: pipeline/pesquisa_tema_<tema_resumido>.txt]
```

### Passo 3 — Redacao do parecer

Invocar Agent `redator-parecer` (subagent_type: redator-parecer, model: opus) com prompt:

```
Redija parecer juridico interno sobre: [tema]

INSUMO:
- Pesquisa tematica: [path do output anterior]
- Perfil de estilo: .claude/skills/paulo-estilo-juridico/references/perfil-estilo.md

Estrutura obrigatoria:
I — QUESTAO
II — FUNDAMENTACAO (Legislacao, Jurisprudencia, Doutrina, Analise critica)
III — CONCLUSAO

Salve em: [Se --caso: Clientes/<PASTA>/pipeline/parecer_<prefixo>_v1.txt]
          [Senao: pipeline/parecer_<tema_resumido>_v1.txt]
```

### Passo 4 — Revisao de estilo

Invocar Agent `revisor-estilo-juridico` (subagent_type: revisor-estilo-juridico, model: sonnet) para revisar o parecer.

### Passo 5 — Auditoria final

Invocar Agent `auditor-final` (subagent_type: auditor-final, model: opus) para produzir versao final.

### Passo 6 — Geracao .docx

Invocar Agent `gerador-docx` (subagent_type: gerador-docx, model: sonnet) com titulo "PARECER".

### Passo 7 — Exibir resultado

```
PARECER CONCLUIDO — [tema]

Arquivos gerados:
  - Pesquisa: [path]
  - Parecer v1: [path]
  - Parecer final: [path]
  - DOCX: [path]

[Se --caso: Vinculado ao caso de [cliente]]
```

---

## Regras

- Pipeline completo: pesquisa → redacao → revisao estilo → auditoria → docx
- Sempre verificar citacoes de jurisprudencia no parecer antes do docx
- Se --caso especificado, salvar tudo na pasta do cliente
- Se nao, usar pasta pipeline/ na raiz do projeto
