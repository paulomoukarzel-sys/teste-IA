$ARGUMENTS contem o nome do cliente potencial para triagem de viabilidade.

---

## Execucao

### Passo 1 — Criar caso em modo triagem

Se a pasta do cliente NAO existe em `Clientes/`:
- Criar estrutura basica: `Clientes/<NOME_PASTA>/pipeline/` e `Clientes/<NOME_PASTA>/output_claude/`
- Criar caso.json minimo com `"status": "triagem"` (nao precisa de todos os campos obrigatorios)

Se a pasta ja existe:
- Ler caso.json existente
- Atualizar status para "triagem" se necessario

### Passo 2 — Analise de viabilidade

Invocar Agent `analista-viabilidade` (subagent_type: analista-viabilidade, model: opus) com prompt:

```
Voce e o Analista de Viabilidade do escritorio.

CASO:
[conteudo do caso.json]

PASTA DO CLIENTE: Clientes/<NOME_PASTA>/

Analise todos os documentos disponiveis na pasta do cliente e produza a analise de viabilidade completa.
Avalie: teses viaveis, riscos processuais, prescricao, qualidade da prova, complexidade.
Gere um score de viabilidade de 1 a 10.

Salve em: Clientes/<NOME_PASTA>/pipeline/analise_viabilidade_<prefixo>.txt
```

### Passo 3 — Pesquisa de precedentes

Invocar Agent `pesquisador-jurisprudencial` (subagent_type: pesquisador-jurisprudencial, model: sonnet) com prompt:

```
Pesquise jurisprudencia relevante para avaliar viabilidade deste caso:

Tipo de acao: [tipo_acao do caso.json]
Teses identificadas: [extrair do output do analista-viabilidade]

Foque em: precedentes favoraveis e desfavoraveis, tendencia dos tribunais, sumulas aplicaveis.
```

### Passo 4 — Validacao de citacoes

Para cada julgado retornado pelo pesquisador, verificar autenticidade basica (numero existe no tribunal).

### Passo 5 — Parecer formal

Invocar Agent `parecerista` (subagent_type: parecerista, model: opus) com prompt:

```
Voce e o Parecerista do escritorio.

CASO:
[conteudo do caso.json]

INSUMOS:
- Analise de viabilidade: Clientes/<NOME_PASTA>/pipeline/analise_viabilidade_<prefixo>.txt
- Pesquisa jurisprudencial: [output do pesquisador]

Gere parecer formal de viabilidade com score 1-10, recomendacao (ACEITAR/RECUSAR/NEGOCIAR),
justificativa detalhada e condicoes sugeridas.

Salve em: Clientes/<NOME_PASTA>/pipeline/parecer_viabilidade_<prefixo>.txt
```

### Passo 6 — Atualizar caso.json

Adicionar ao caso.json:
```json
{
  "viabilidade": {
    "score": [1-10],
    "recomendacao": "ACEITAR|RECUSAR|NEGOCIAR",
    "data_avaliacao": "YYYY-MM-DD",
    "parecer": "pipeline/parecer_viabilidade_<prefixo>.txt"
  }
}
```

### Passo 7 — Exibir resultado

```
TRIAGEM CONCLUIDA — [cliente]

RECOMENDACAO: [ACEITAR / RECUSAR / NEGOCIAR]
SCORE: [N]/10

Resumo:
  Teses viaveis: [N]
  Riscos criticos: [N]
  Prescricao: [status]
  
Arquivos gerados:
  - Analise: Clientes/<PASTA>/pipeline/analise_viabilidade_<prefixo>.txt
  - Parecer: Clientes/<PASTA>/pipeline/parecer_viabilidade_<prefixo>.txt

[Se ACEITAR: Proximo passo: /caso novo <cliente> para formalizar o caso]
[Se NEGOCIAR: Condicoes sugeridas: <resumo das condicoes>]
[Se RECUSAR: Motivo principal: <resumo>]
```

---

## Regras

- Sempre executar analise de viabilidade ANTES do parecer
- Score abaixo de 3: recomendacao automatica RECUSAR (o parecerista pode divergir com justificativa)
- Nao criar caso.json completo na triagem — apenas campos minimos
- Manter status "triagem" ate decisao final do Dr. Paulo
