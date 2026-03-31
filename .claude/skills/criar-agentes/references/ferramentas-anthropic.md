# Ferramentas disponíveis para agentes no Claude Code

Use esta referência ao definir a lista `tools:` no frontmatter de um agente.
Princípio: **mínimo necessário**. Cada ferramenta adicionada amplia o espaço de comportamento
possível — menos ferramentas = agente mais previsível e seguro.

---

## Ferramentas de leitura/busca (somente leitura — baixo risco)

| Ferramenta | O que faz | Quando dar ao agente |
|---|---|---|
| `Read` | Lê conteúdo de um arquivo | Sempre que o agente precisar ler arquivos |
| `Glob` | Encontra arquivos por padrão de nome | Quando precisa descobrir arquivos por padrão |
| `Grep` | Busca conteúdo dentro de arquivos | Quando precisa encontrar texto em código/docs |

## Ferramentas de escrita (modificam estado — médio risco)

| Ferramenta | O que faz | Quando dar ao agente |
|---|---|---|
| `Write` | Cria ou sobrescreve um arquivo | Quando o agente produz arquivos como saída |
| `Edit` | Edição cirúrgica de arquivos existentes | Quando o agente faz modificações pontuais |
| `NotebookEdit` | Edita células de Jupyter notebooks | Apenas para agentes de ciência de dados |

## Ferramentas de execução (efeitos colaterais — alto risco)

| Ferramenta | O que faz | Quando dar ao agente |
|---|---|---|
| `Bash` | Executa comandos shell | Apenas quando imprescindível; especifique no prompt quais comandos são permitidos |

## Ferramentas de rede

| Ferramenta | O que faz | Quando dar ao agente |
|---|---|---|
| `WebSearch` | Pesquisa na web | Para agentes de pesquisa/jurisprudência |
| `WebFetch` | Busca conteúdo de URL específica | Para agentes que consultam fontes externas conhecidas |

## Ferramentas de orquestração

| Ferramenta | O que faz | Quando dar ao agente |
|---|---|---|
| `Agent` | Lança subagentes | Apenas para agentes orquestradores; subagentes leaf não precisam |
| `TodoWrite` | Gerencia lista de tarefas | Para agentes com fluxo multi-etapa que precisam rastrear progresso |

## Ferramentas de contexto do usuário

| Ferramenta | O que faz | Quando dar ao agente |
|---|---|---|
| `AskUserQuestion` | Faz pergunta ao usuário | Para agentes interativos que precisam de input humano |

---

## Combinações comuns por tipo de agente

**Agente de pesquisa/análise**
```yaml
tools: [Read, Grep, Glob, WebSearch]
```

**Agente de geração de documentos**
```yaml
tools: [Read, Write, Bash]
```

**Agente de refatoração de código**
```yaml
tools: [Read, Edit, Grep, Glob, Bash]
```

**Agente de revisão (somente leitura)**
```yaml
tools: [Read, Grep, Glob]
```

**Agente orquestrador**
```yaml
tools: [Agent, Read, TodoWrite]
```

**Agente de pesquisa jurídica**
```yaml
tools: [Read, Grep, Glob, WebSearch, WebFetch]
```