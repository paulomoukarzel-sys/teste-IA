$ARGUMENTS contém o sub-comando e parâmetros. Detecte qual sub-comando foi chamado e execute as instruções correspondentes.

---

## Detecção do sub-comando

Leia os `$ARGUMENTS` e identifique o primeiro token como sub-comando. Os tokens seguintes são parâmetros.

Exemplos:
- `novo Le Motos` → sub-comando `novo`, cliente `Le Motos`
- `status Márcio Klaus` → sub-comando `status`, cliente `Márcio Klaus`
- `listar` → sub-comando `listar`, sem parâmetros
- `prazos` → sub-comando `prazos`, sem parâmetros
- `contestacao Le Motos` → sub-comando `contestacao`, cliente `Le Motos`
- `recurso Márcio Klaus` → sub-comando `recurso`, cliente `Márcio Klaus`
- `placeholders` → sub-comando `placeholders`, sem parâmetros
- `indexar` → sub-comando `indexar`, sem parâmetros

Se nenhum sub-comando reconhecido for passado, exiba o menu de ajuda (seção final deste arquivo).

---

## SUB-COMANDO: `novo`

**Propósito:** Criar um novo caso com estrutura de pastas e `caso.json`.

**Execução:** Delegue integralmente para o comando `/novo-caso`, passando os argumentos restantes (nome do cliente) como contexto inicial. O comando `/novo-caso` já sabe coletar as informações necessárias, confirmar com o usuário e criar a estrutura.

Instrua o usuário que o comando `/novo-caso` foi ativado e siga o workflow dele completamente.

---

## SUB-COMANDO: `status`

**Propósito:** Mostrar o estado atual de um caso específico.

**Parâmetro:** nome parcial do cliente (busca case-insensitive na pasta `Clientes/`).

**Execução:**

1. Use a ferramenta Bash para listar as pastas em `Clientes/` e encontrar a que corresponde ao argumento fornecido (busca parcial, case-insensitive). Se houver mais de uma correspondência, liste-as e peça ao usuário que especifique.

2. Leia o arquivo `Clientes/<PASTA_ENCONTRADA>/caso.json`.

3. Calcule os dias restantes até `prazo_fatal` (data de hoje: use `date +%Y-%m-%d` via Bash).

4. Exiba o relatório de status no seguinte formato:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CASO: [cliente]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DADOS DO CASO
  Processo:      [processo]
  Vara:          [vara]
  Polo:          [polo]
  Parte adversa: [parte_adversa]
  Tipo de peça:  [prazo_tipo]

PRAZO FATAL
  Data:          [prazo_fatal]
  Dias restantes: [N dias]   ← marcar URGENTE se <= 5 dias; VENCIDO se negativo

PIPELINE — ETAPAS
  [etapa]              [status]   [output ou "—"]
  analise              pendente   —
  pesquisa_magistrado  pendente   —
  redacao              concluido  Clientes/.../pipeline/redacao.txt
  ...

PLACEHOLDERS PENDENTES
  [lista de placeholders do campo "placeholders" do caso.json, ou "Nenhum pendente"]
```

5. Se `caso.json` não existir na pasta encontrada, informe o usuário e sugira executar `/caso novo <cliente>`.

---

## SUB-COMANDO: `listar`

**Propósito:** Exibir painel de todos os casos cadastrados com `caso.json`.

**Execução:**

1. Use a ferramenta Bash para encontrar todos os arquivos `caso.json` dentro de `Clientes/`:
   ```bash
   find Clientes -name "caso.json" 2>/dev/null
   ```

2. Leia cada `caso.json` encontrado.

3. Para cada caso, calcule os dias restantes até `prazo_fatal` (use `date +%Y-%m-%d` para obter a data atual via Bash).

4. Determine o status de exibição:
   - `CONCLUÍDO` → se todas as etapas do pipeline tiverem `status: "concluido"`
   - `VENCIDO` → se `prazo_fatal` já passou e não está concluído
   - `URGENTE` → se dias restantes <= 5 e não está concluído
   - `EM ANDAMENTO` → demais casos

5. Exiba a tabela formatada:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAINEL DE CASOS — [data de hoje]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cliente              | Tipo         | Etapa Atual          | Prazo      | Dias | Status
---------------------|--------------|----------------------|------------|------|-------------
Le Motos             | contestacao  | redacao              | 15/04/2026 |   12 | EM ANDAMENTO
Márcio Klaus         | resp         | concluido            |     —      |    — | CONCLUÍDO
[próximo caso...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: [N] casos  |  Em andamento: [N]  |  Concluídos: [N]  |  Urgentes: [N]
```

A coluna "Etapa Atual" deve mostrar a última etapa com `status != "pendente"`, ou `"pendente"` se nenhuma etapa foi iniciada.

6. Se nenhum `caso.json` for encontrado, informe que não há casos cadastrados e sugira `/caso novo <cliente>`.

---

## SUB-COMANDO: `prazos`

**Propósito:** Mostrar casos ordenados por urgência (prazo mais próximo primeiro).

**Execução:**

1. Execute a mesma coleta de dados do sub-comando `listar` (leia todos os `caso.json`).

2. Ordene os casos da seguinte forma:
   - Primeiro: casos VENCIDOS (prazo já passou), do mais recente ao mais antigo
   - Segundo: casos com prazo nos próximos 5 dias (URGENTE), do mais próximo ao mais distante
   - Terceiro: demais casos em andamento, do mais próximo ao mais distante
   - Por último: casos CONCLUÍDOS (sem prazo relevante)

3. Exiba no formato:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRAZOS — [data de hoje]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[VENCIDO]  Le Motos         contestacao   venceu há 3 dias   (prazo: 31/03/2026)
[URGENTE]  Outro Cliente    apelacao      3 dias restantes   (prazo: 06/04/2026)
           Mais um Cliente  resp          15 dias restantes  (prazo: 18/04/2026)
[OK]       ...
```

Destacar visualmente as linhas VENCIDO e URGENTE com prefixo entre colchetes.

---

## SUB-COMANDO: `contestacao`

**Propósito:** Disparar o pipeline de agentes para elaboração de contestação.

**Parâmetro:** nome parcial do cliente.

**Execução:**

1. Localize a pasta do cliente em `Clientes/` (busca parcial, case-insensitive) e leia o `caso.json`.

2. Verifique se o `prazo_tipo` é `contestacao`. Se não for, alerte o usuário:
   ```
   ATENÇÃO: O caso de [cliente] está registrado como tipo "[prazo_tipo]", não "contestacao".
   O orquestrador de contestação pode não ser o pipeline adequado.
   Deseja continuar mesmo assim? (s/n)
   ```

3. Verifique se o agente `orquestrador-contestacao` existe em `.claude/agents/orquestrador-contestacao.md`. Se não existir, instrua o usuário a criá-lo primeiro:
   ```
   O agente orquestrador-contestacao não foi encontrado em .claude/agents/.
   Crie-o usando a skill criar-agentes antes de continuar.
   ```

4. Se tudo estiver em ordem, exiba o contexto completo para o orquestrador e instrua o Claude a invocar o agente `orquestrador-contestacao` via Agent tool, passando como contexto:
   - O conteúdo completo do `caso.json`
   - O caminho da pasta do cliente: `Clientes/<PASTA>/`
   - A instrução: "Elabore a contestação completa para este caso seguindo o pipeline de agentes."

5. Exiba ao usuário:
   ```
   Iniciando pipeline de contestação para [cliente].
   Caso: [processo]
   Prazo fatal: [prazo_fatal] ([N] dias restantes)
   
   O orquestrador-contestacao foi ativado. Acompanhe o progresso nas mensagens seguintes.
   ```

---

## SUB-COMANDO: `recurso`

**Propósito:** Disparar o pipeline de agentes para elaboração de REsp/RE ou outros recursos.

**Parâmetro:** nome parcial do cliente.

**Execução:**

1. Localize a pasta do cliente em `Clientes/` (busca parcial, case-insensitive) e leia o `caso.json`.

2. Verifique se o `prazo_tipo` é compatível com recursos (`resp`, `re`, `apelacao`, `hc`, `rhc`, `aresp`, `embargos`). Se for `contestacao`, alerte:
   ```
   ATENÇÃO: O caso de [cliente] está registrado como tipo "contestacao".
   Para contestações, use: /caso contestacao <cliente>
   Deseja continuar com o orquestrador de recursos mesmo assim? (s/n)
   ```

3. Verifique se o agente `orquestrador-recursos` existe em `.claude/agents/orquestrador-recursos.md`. Se não existir, instrua o usuário a criá-lo primeiro:
   ```
   O agente orquestrador-recursos não foi encontrado em .claude/agents/.
   Crie-o usando a skill criar-agentes antes de continuar.
   ```

4. Se tudo estiver em ordem, invoque o agente `orquestrador-recursos` via Agent tool, passando como contexto:
   - O conteúdo completo do `caso.json`
   - O caminho da pasta do cliente: `Clientes/<PASTA>/`
   - A instrução: "Elabore o(s) recurso(s) completo(s) para este caso seguindo o pipeline de agentes."

5. Exiba ao usuário:
   ```
   Iniciando pipeline de recursos para [cliente].
   Tipo de peça: [prazo_tipo]
   Caso: [processo]
   Prazo fatal: [prazo_fatal] ([N] dias restantes)
   
   O orquestrador-recursos foi ativado. Acompanhe o progresso nas mensagens seguintes.
   ```

---

## SUB-COMANDO: `placeholders`

**Propósito:** Listar todos os `[PLACEHOLDERS]` não resolvidos nos documentos dos clientes.

**Execução:**

1. Execute o script de varredura via Bash:
   ```bash
   python .claude/skills/paulo-estilo-juridico/scripts/placeholder_scan.py
   ```

2. Exiba a saída do script diretamente ao usuário.

3. Se o script não existir ou retornar erro, informe:
   ```
   Erro ao executar placeholder_scan.py: [mensagem de erro]
   Verifique se o arquivo existe em: .claude/skills/paulo-estilo-juridico/scripts/placeholder_scan.py
   ```

4. Se nenhum placeholder for encontrado, informe:
   ```
   Nenhum [PLACEHOLDER] pendente encontrado nos documentos dos clientes.
   ```

---

## SUB-COMANDO: `indexar`

**Propósito:** Re-executar a indexação das peças _vf para atualizar o índice de referências.

**Execução:**

1. Execute o script de indexação via Bash:
   ```bash
   python .claude/skills/paulo-estilo-juridico/scripts/indexar_vf.py
   ```

2. Exiba a saída do script diretamente ao usuário.

3. Se o script não existir ou retornar erro, informe:
   ```
   Erro ao executar indexar_vf.py: [mensagem de erro]
   Verifique se o arquivo existe em: .claude/skills/paulo-estilo-juridico/scripts/indexar_vf.py
   ```

4. Após execução bem-sucedida, confirme:
   ```
   Índice atualizado com sucesso.
   Arquivo gerado: data/indice_vf.json
   ```

---

## Menu de ajuda (sub-comando não reconhecido ou sem argumentos)

Se os `$ARGUMENTS` estiverem vazios ou contiverem um sub-comando não reconhecido, exiba:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GERENCIADOR DE CASOS — Gastão da Rosa & Moukarzel Advogados
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Uso:  /caso <sub-comando> [parâmetros]

Sub-comandos disponíveis:

  novo <cliente>          Cria novo caso (pasta + caso.json)
  status <cliente>        Exibe etapa atual, prazo e placeholders pendentes
  listar                  Painel de todos os casos cadastrados
  prazos                  Casos ordenados por urgência do prazo
  contestacao <cliente>   Dispara o pipeline de contestação
  recurso <cliente>       Dispara o pipeline de recursos (REsp/RE/apelação)
  placeholders            Lista todos [PLACEHOLDERS] não resolvidos
  indexar                 Reindexar peças _vf (atualiza data/indice_vf.json)

Exemplos:
  /caso novo Le Motos
  /caso status Márcio Klaus
  /caso listar
  /caso prazos
  /caso contestacao Le Motos
  /caso recurso Márcio Klaus
  /caso placeholders
  /caso indexar
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Regras gerais de execução

- Sempre usar caminhos relativos a partir do diretório de trabalho do projeto (`Clientes/`, `.claude/`, etc.)
- Busca de cliente em `Clientes/` é sempre parcial e case-insensitive: "le motos", "Le Motos" e "LE_MOTOS" devem todos encontrar a pasta `Leonardo - Le Motos/` ou `LE_MOTOS/`
- Para calcular dias restantes, use sempre a data atual via Bash: `date +%Y-%m-%d`
- Datas no `caso.json` estão no formato `YYYY-MM-DD`; exibir ao usuário no formato `DD/MM/YYYY`
- Nunca modificar `caso.json` neste comando — apenas ler. Modificações no `caso.json` são responsabilidade dos agentes do pipeline
- Se um `caso.json` estiver malformado ou ausente, reportar o erro com clareza e sugerir `/caso novo <cliente>` para recriar
