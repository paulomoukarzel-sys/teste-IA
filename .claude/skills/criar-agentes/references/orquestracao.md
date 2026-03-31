# Padrões de orquestração multi-agente (Anthropic)

Use esta referência quando o usuário está criando múltiplos agentes que trabalham juntos.

---

## Padrões principais

### 1. Orquestrador → Subagentes leaf

O padrão mais comum. Um agente central decide o que fazer e delega tarefas atômicas
para agentes especializados. Os subagentes não conhecem uns aos outros.

```
Orquestrador
├── Agente A (pesquisa)
├── Agente B (geração)
└── Agente C (revisão)
```

**Regras:**
- O orquestrador tem a ferramenta `Agent`; os leaf não precisam
- Cada leaf recebe apenas as informações necessárias para sua tarefa
- O leaf retorna resultado estruturado; o orquestrador decide o que fazer com ele

### 2. Pipeline sequencial

Cada agente processa a saída do anterior. Útil para transformações em etapas.

```
Input → Agente A → Agente B → Agente C → Output
```

**Regras:**
- Defina o formato de saída de cada agente explicitamente
- O próximo agente na cadeia não deve precisar reprocessar o que o anterior já fez
- Se um elo falhar, o pipeline inteiro para — projete para falha controlada

### 3. Agentes paralelos + agregação

Tarefas independentes rodam em paralelo; os resultados são agregados pelo orquestrador.

```
          ┌─ Agente A ─┐
Input ────┤─ Agente B ─├──→ Agregador → Output
          └─ Agente C ─┘
```

**Quando usar:** Pesquisa em múltiplas fontes, análise de múltiplos documentos, 
verificações independentes que precisam de resultado conjunto.

---

## Contratos entre agentes

Todo par orquestrador/subagente precisa de um contrato explícito:

```markdown
## Contrato do Agente X

**Recebe:**
- [campo]: [tipo] — [descrição]

**Retorna:**
- [campo]: [tipo] — [descrição]

**Erros possíveis:**
- [condição]: o agente retorna [mensagem de erro padrão]
```

---

## Princípio de isolamento

Subagentes não devem ter estado compartilhado. Se dois agentes precisam da mesma
informação, o orquestrador passa para ambos — os agentes não se comunicam diretamente.

**Ruim:**
```
Agente A → escreve arquivo X → Agente B lê arquivo X
```

**Bom:**
```
Agente A → retorna dado → Orquestrador → passa dado → Agente B
```

---

## Quando usar cada padrão para fluxos jurídicos

| Tarefa | Padrão recomendado |
|---|---|
| Redigir peça (pesquisa + redação + revisão) | Orquestrador → 3 leaf em sequência |
| Verificar autenticidade de múltiplos julgados | Orquestrador → leaf em paralelo |
| Analisar WhatsApp + BO + decisão | Pipeline sequencial |
| Gerar peça + .docx | Pipeline sequencial |