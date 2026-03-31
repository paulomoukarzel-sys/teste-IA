# Casos de Teste — Skill paulo-estilo-juridico

## Teste 1: Habeas Corpus basico

**Input**: "Elabore um habeas corpus para o paciente Joao da Silva, preso preventivamente no evento 45 dos autos n. 0001234-56.2025.8.24.0001, por suposto furto qualificado (art. 155, § 4, CP). A prisao foi decretada sem fundamentacao idonea."
**Esperado**: Peca com enderecamento ao TJ/SC, qualificacao do paciente, identificacao do constrangimento ilegal, fundamentacao (art. 312 CPP, ausencia de fundamentacao), jurisprudencia STJ/STF sobre fundamentacao de preventiva, pedido de liminar com alvara de soltura.
**Checklist**: enderecamento maiusculo, "paciente", "constrangimento ilegal", referencia ao evento 45, pedido de liminar, encerramento padrao.

## Teste 2: Contestacao civel

**Input**: "Escreva uma contestacao para a empresa ABC Ltda contra acao de indenizacao por danos morais movida por Maria Souza. O autor alega defeito em produto, mas nao ha prova do nexo causal."
**Esperado**: Peca com preliminares (se cabivel), impugnacao especifica dos fatos, negativa peremptoria, fundamentacao em ausencia de nexo causal, jurisprudencia sobre onus da prova (art. 373 CPC), pedidos.
**Checklist**: "Nega-se, peremptoriamente", secoes com romanos, subsecoes arabes, conectivos entre paragrafos, encerramento padrao.

## Teste 3: Revisao de peca existente

**Input**: [Fornecer peca mal formatada, sem conectivos, com bullets no corpo, sem jurisprudencia]
**Esperado**: Analise estrutural + estilo + sugestoes categorizadas (criticas/importantes/sugestoes). Reescrita oferecida.
**Checklist**: modo de revisao ativado, sugestoes categorizadas, correcoes de estilo apontadas.

## Teste 4: Geracao de .docx

**Input**: "Gere o docx da peticao acima"
**Esperado**: Execucao do script gerar_peticao.py com parametros corretos, arquivo .docx gerado com Arial 12, espacamento 1.5, margens forense, numeracao de paginas.
**Checklist**: script executado, arquivo criado, formatacao correta ao abrir no Word.

## Teste 5: Trigger de ativacao

**Positivos** (devem ativar a skill):
- "Elabore uma peticao inicial civel"
- "Faca um agravo de instrumento"
- "Revise essa peca juridica"
- "Gere o docx dessa contestacao"
- "Escreve como eu faria"
- "Redigir mandado de seguranca"

**Negativos** (NAO devem ativar a skill):
- "O que e um habeas corpus?" (pergunta generica, nao pedido de redacao)
- "Resuma esse artigo sobre direito penal" (resumo, nao peca juridica)

## Teste 6: Peticao Inicial Civel (tipo novo)

**Input**: "Elabore uma peticao inicial de acao de obrigacao de fazer contra a empresa XYZ S.A., que se recusa a entregar produto comprado pelo autor Carlos Mendes. Valor da causa: R$ 15.000,00. Pedir tutela de urgencia."
**Esperado**: Peca com qualificacao completa do autor, enderecamento ao juizo civel, secoes (Fatos, Direito, Tutela Provisoria, Pedidos, Provas, Valor da Causa), fundamentacao nos arts. 319/320 CPC e art. 300 CPC (tutela), pedido de citacao do reu.
**Checklist**: arts. 319, 320 CPC mencionados, tutela de urgencia fundamentada no art. 300, valor da causa indicado, secao de provas.

## Teste 7: Agravo de Instrumento (tipo novo)

**Input**: "Faca um agravo de instrumento contra decisao que indeferiu tutela de urgencia no evento 30 do processo n. 0005678-90.2025.8.24.0023. O juiz nao analisou o periculum in mora."
**Esperado**: Peca com enderecamento ao TJ, qualificacao do agravante, indicacao da decisao agravada (evento 30), cabimento (art. 1.015 CPC), razoes para reforma (omissao quanto ao periculum), pedido de efeito suspensivo/tutela recursal (art. 1.019, I, CPC).
**Checklist**: art. 1.015 CPC, referencia ao evento 30, pedido de efeito suspensivo, fundamentacao sobre periculum in mora, encerramento padrao.
