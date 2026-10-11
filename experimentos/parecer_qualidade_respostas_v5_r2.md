# Parecer assistido sobre a qualidade das respostas — v5, rodada 2

Revisão realizada por Codex, assistida por IA. Não é revisão humana independente nem validação científica das referências.

## Material e procedimento

Foram inspecionadas as perguntas, os SQLs finais, os SQLs candidatos de referência, as tabelas e os textos insight/factual_summary da execução acuracia_qwen_catalogo_v5_r2.json. As comparações completas de tabelas já registradas foram conferidas; a Q25 recebeu conferência adicional de todos os 33.696 registros após normalização de representação dos identificadores, exclusivamente para distinguir conteúdo de formato. Não houve nova execução do Ollama nem consulta ao banco.

Escopo: 68 casos. Há 56 respostas analíticas finais disponíveis; oito falhas técnicas (Q2, Q11, Q42, Q49, Q55, Q58, Q60, Q61) não fornecem conteúdo final avaliável; Q65–Q68 são limitações previstas, tratadas separadamente. Foram registrados 392 julgamentos qualitativos, cada um com evidência, responsável, data e método. Nenhum caso elegível ficou pendente. A cobertura qualitativa é 56/64 = 87,5%.

Os 52/64 acertos estritos (81,25%) da execução original foram preservados. Uma aprovação de conteúdo ou fidelidade não substitui a acurácia nem valida toda a consulta.

## Resultados por dimensão

| Dimensão | Atende | Parcial | Não atende | Avaliados | Sem resposta avaliável |
|---|---:|---:|---:|---:|---:|
| Filtros | 46 | 0 | 10 | 56/64 | 8 |
| Unidade e agregação | 53 | 1 | 2 | 56/64 | 8 |
| Dimensões e identificadores | 55 | 0 | 1 | 56/64 | 8 |
| Informação principal | 53 | 1 | 2 | 56/64 | 8 |
| Completude e escopo | 52 | 3 | 1 | 56/64 | 8 |
| Formato da saída | 47 | 7 | 2 | 56/64 | 8 |
| Fidelidade do texto | 47 | 4 | 5 | 56/64 | 8 |

As contagens se sobrepõem. Não somar falhas entre dimensões e não interpretar percentuais entre os 56 avaliados como aprovação sobre todos os 64. Os quatro casos de limitação não integram esse denominador. Há pares de perguntas repetidas no catálogo; as observações não são todas independentes.

## Achados principais

1. **Acerto numérico pode ocultar SQL incompleto.** Q17/Q26/Q29 omitem CNES > 0; Q19/Q22/Q24 omitem município positivo; Q50 e Q59 omitem exclusão de UF/região vazia. Q25 também omite CNES positivo e remoção de espaços do bairro, além de acrescentar filtro de UF positiva. Q8 filtra nome em lugar de código municipal. São dez reprovações em filtros, sem reclassificar a acurácia original.
2. **Q5 calcula a razão inversa.** Retorna 1,510534 em vez de aproximadamente 0,662018. A explicação ainda descreve a razão invertida como se fosse a solicitada.
3. **Q40 seleciona a UF errada.** Calcula percentuais, mas escolhe o maior número absoluto de óbitos (SP), em vez do maior percentual (PI).
4. **Q26 inventa conteúdo na explicação.** A tabela está correta, mas o texto fornece associações contraditórias de UF e inventa código 91 e mínimo 1.021.
5. **Q38 inverte o significado do desfecho.** O percentual está correto; a explicação chama evolucao=2 de melhoria. O metadado local define esse código como óbito.
6. **Q48 e Q52 extrapolam os números.** Q48 sugere uso/ocupação a partir da parcela SUS do estoque; Q52 transforma 12,29% em 12,29 leitos por cada leito, erro de escala.
7. **Q41 descreve ordem incorreta.** Tosse é corretamente apontada como mais frequente, mas vômito é colocado por último apesar de superar garganta e diarreia.
8. **Formato pode divergir mesmo com valores certos.** Q20/Q21/Q24/Q30/Q50/Q56/Q59 não usam literalmente os aliases pedidos. Q25 retorna códigos numéricos como texto: todos os conteúdos conferem após normalização, mas a reprovação estrita original continua válida. Q8 substitui código IBGE por nome municipal.
9. **Limites do SQL em cenários explicitamente previstos.** Q6 não garante ambas as categorias se uma estiver ausente; Q7 cria faixas com zero apesar do pedido de excluir faixas ausentes. Ambos acertaram neste snapshot; a completude recebeu parcial.

## Convenções utilizadas

- Informação principal: conteúdo da tabela no snapshot. Texto é avaliado separadamente em fidelidade, evitando confundir acerto numérico com explicação correta.
- Filtros: inclui escopo sem restrição; não acrescentar filtro indevido também é atendimento. Condições garantidas pela lógica do JOIN são aceitas, como município positivo em Q62.
- Agregação: contagem, DISTINCT, denominador e chave de agrupamento; erros de seleção de extremo também podem afetar escopo.
- Formato: nomes exatos de colunas são considerados quando o enunciado os pede; divergências apenas de alias recebem parcial. Normalizações já previstas no protocolo, como ano em Q32 e casefold em Q45, são respeitadas.
- Fidelidade: uma explicação pode resumir destaques sem repetir a tabela inteira. Deve preservar valores, unidades e significado. Em Q40, o texto é fiel à tabela errada; essa dimensão não valida o SQL.
- Q7, Q32, Q34 e Q41 receberam parcial em fidelidade; Q5, Q26, Q38, Q48 e Q52 receberam fail. A classificação parcial descreve a parcela atendida e a deficiência.

## Arquivos

- [Relatório dimensional completo](qualidade_respostas_v5_r2_revisada_ia.md)
- [Julgamentos, evidências e autoria](qualidade_respostas_v5_r2.revisao_ia.json)
- [Relatório estruturado consolidado](qualidade_respostas_v5_r2_revisada_ia.json)
- [Relatório automático preservado](qualidade_respostas_v5_r2.md)

A revisão está completa no escopo das respostas disponíveis, mas permanece assistida por IA e sujeita à conferência humana. As referências numéricas ainda são rascunhos. Não foi atribuída uma nota global de qualidade.
