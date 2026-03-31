---
name: criar-agentes-especializados
description: >
  Use SEMPRE que o usuário quiser criar um agente especializado, subagente, agente autônomo,
  ou qualquer componente com escopo de tarefa bem definido. Também ativar quando o usuário
  descrever "preciso de um agente que faça X", "cria um agente para Y", "quero automatizar Z
  com um agente", ou quando apresentar o escopo/briefing de um agente novo.
  Esta skill garante que todos os agentes sejam criados dentro dos padrões ideais da Anthropic:
  escopo focado, ferramentas mínimas necessárias, descrição precisa de ativação, prompt de
  sistema bem estruturado e exemplos concretos.
---

# Skill: Criar Agentes Especializados

Esta skill guia a criação de agentes seguindo os padrões recomendados pela Anthropic para
o Claude Code. Um agente bem construído tem escopo único, ferramentas mínimas, descrição
que dispara no momento certo e sistema de prompt que o torna previsível e confiável.

---

## Princípios fundamentais (Anthropic)

Antes de escrever qualquer linha, tenha estes princípios na cabeça:

1. **Um agente = uma responsabilidade** — Se você precisar de "e também", crie dois agentes.
2. **Ferramentas mínimas** — Dê ao agente apenas as ferramentas que ele precisa. Menos ferramentas = comportamento mais previsível.
3. **Descrição como gatilho** — A `description` no frontmatter é o mecanismo primário de ativação. Ela precisa ser específica o suficiente para não disparar errado e abrangente o suficiente para não deixar de disparar.
4. **Prompt de sistema como contrato** — O corpo do agente define o que ele faz, o que NÃO faz, o formato de saída e como lidar com ambiguidade.
5. **Exemplos concretos valem mais que regras abstratas** — Sempre inclua pelo menos 2 exemplos de invocação no frontmatter.
6. **Falha controlada** — O agente deve saber quando parar e devolver o controle ao orquestrador, nunca tentar resolver sozinho algo fora do seu escopo.

---

## Workflow de criação

### Passo 1 — Entender o escopo

Se o usuário já trouxe o escopo, extraia as respostas às perguntas abaixo do que foi apresentado.
Se não, pergunte:

- **O que este agente faz?** (uma frase, verbo no infinitivo)
- **O que ele NÃO faz?** (limites explícitos evitam escopo creep)
- **Quem o invoca?** (Claude principal, outro agente, slash command)
- **Quais ferramentas precisa?** (Bash, Read, Write, Grep, Glob, WebSearch, WebFetch, Agent, Edit, etc.)
- **O que ele retorna?** (formato de saída: texto, arquivo, JSON, confirmação)
- **Quando NÃO deve ser ativado?** (casos limítrofes que poderiam confundir a descrição)

### Passo 2 — Consultar referência de ferramentas

Antes de listar as ferramentas do agente, leia `references/ferramentas-anthropic.md` para
verificar quais ferramentas estão disponíveis e qual o custo/benefício de cada uma.

### Passo 3 — Rascunhar o arquivo do agente

Estrutura obrigatória para agentes no Claude Code (arquivo `.md` em `.claude/agents/`):

```markdown
---
name: nome-do-agente
description: >
  [Quando usar — contextos específicos, gatilhos linguísticos, casos de uso primários]
  [Quando NÃO usar — casos limítrofes que devem ir para outro agente]
tools:
  - NomeExatoDaFerramenta1
  - NomeExatoDaFerramenta2
---

# [Nome do Agente]

[Uma frase descrevendo o papel deste agente]

## Responsabilidades

[Lista do que este agente faz]

## Fora do escopo

[Lista do que este agente NÃO faz — seja explícito]

## Processo

[Passo a passo de como o agente executa sua tarefa]

## Formato de saída

[Descreva exatamente o que o agente deve retornar ao orquestrador]

## Quando parar e devolver

[Condições em que o agente deve interromper, reportar um bloqueio ou escalar]

## Exemplos

[2-3 exemplos concretos de entrada → saída esperada]
```

### Passo 4 — Revisar com o checklist

Antes de salvar o arquivo final, verifique cada item:

- [ ] `name` em kebab-case, sem espaços, descritivo
- [ ] `description` cobre os gatilhos principais E os casos de não-ativação
- [ ] Ferramentas listadas são as **mínimas necessárias** (remova qualquer uma que não seja usada)
- [ ] O corpo define claramente o que está **dentro** e **fora** do escopo
- [ ] O formato de saída está especificado
- [ ] Há pelo menos um exemplo concreto
- [ ] Existe uma condição de parada/escalada documentada
- [ ] O agente não duplica responsabilidades de outro agente existente

### Passo 5 — Salvar e registrar

1. Salve em `.claude/agents/<nome-do-agente>.md` (ou no diretório indicado pelo usuário)
2. Se o projeto tiver `CLAUDE.md`, adicione uma linha documentando o agente e seu propósito
3. Se for parte de um sistema multi-agente, consulte `references/orquestracao.md` para garantir que os contratos entre agentes estejam alinhados

---

## Armadilhas comuns — evite

| Problema | Por quê é ruim | Solução |
|---|---|---|
| Description genérica ("Use when needed") | Nunca dispara ou dispara sempre | Especifique contextos concretos |
| Muitas ferramentas | Comportamento imprevisível, mais surface de erro | Só o que é necessário |
| Ausência de "fora do escopo" | O agente tenta resolver tudo | Seja explícito sobre limites |
| Formato de saída vago | Orquestrador não sabe o que esperar | Defina estrutura exata |
| Nenhum exemplo | Difícil de testar e de entender | Sempre 2+ exemplos |
| Lógica de negócio no agente | Quebra quando regra muda | Lógica fica no orquestrador ou skill |

---

## Nota sobre sistemas multi-agente

Se o usuário está criando múltiplos agentes que trabalham juntos:
1. Mapeie o fluxo antes de criar qualquer agente (quem chama quem, o quê passa entre eles)
2. Defina os contratos de entrada/saída entre agentes antes de escrever as instruções individuais
3. Leia `references/orquestracao.md` para padrões de composição recomendados pela Anthropic

---

## Onde salvar os agentes

| Contexto | Caminho |
|---|---|
| Projeto específico | `.claude/agents/<nome>.md` na raiz do projeto |
| Uso global (todos os projetos) | `~/.claude/agents/<nome>.md` |
| Dentro de plugin | `plugins/<plugin>/agents/<nome>.md` com entrada em `plugin.json` |