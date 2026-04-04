$ARGUMENTS contem o filtro de exibicao. Opcoes: hoje, semana, criticos, ou vazio (= todos).

---

## Execucao

### Passo 1 — Executar monitor de prazos

Execute o script via Bash:

```bash
python .claude/skills/paulo-estilo-juridico/scripts/prazos_monitor.py $ARGUMENTS --base .
```

Se `$ARGUMENTS` esta vazio, usar filtro `todos` (default do script).

### Passo 2 — Exibir resultado

Exiba a saida do script diretamente ao usuario.

Se o script retornar erro, informar:

```
Erro ao executar prazos_monitor.py: [mensagem de erro]
Verifique se o arquivo existe em: .claude/skills/paulo-estilo-juridico/scripts/prazos_monitor.py
```

### Passo 3 — Alertas criticos

Apos exibir a tabela, verificar se ha prazos VENCIDO ou CRITICO na saida.

Se houver prazos VENCIDOS:

```
ATENCAO: Existem prazos VENCIDOS! Acao imediata necessaria.
```

Se houver prazos CRITICOS (<=2 dias uteis):

```
Prazos CRITICOS detectados — menos de 3 dias uteis restantes.
```

### Passo 4 — Sugestao de pipeline

Para cada prazo VENCIDO ou CRITICO, sugerir o pipeline adequado:

- Se tipo = `contestacao`: sugerir `/caso contestacao <cliente>`
- Se tipo = `resp` ou `re` ou `aresp`: sugerir `/caso recurso <cliente>`
- Se tipo = `embargos`: sugerir `/caso embargos <cliente>`
- Se tipo = `agravo`: sugerir `/caso agravo <cliente>`
- Outros tipos: sugerir `/doit_like_me` com contexto do caso

---

## Sub-comandos

| Filtro | Descricao |
|--------|-----------|
| `hoje` | Prazos vencendo hoje |
| `semana` | Proximos 7 dias uteis |
| `criticos` | Apenas CRITICO + VENCIDO |
| (vazio) | Todos os prazos ordenados por urgencia |

---

## Regras

- Sempre executar o script com `--base .` para usar o diretorio atual
- Nao modificar nenhum caso.json — apenas leitura
- Datas exibidas no formato DD/MM/YYYY
- Semaforo visual: [!!!] vencido, [!! ] critico, [!  ] atencao, [   ] ok
