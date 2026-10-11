# Qualidade das respostas por dimensão

Análise dos registros existentes, sem nova execução. A acurácia original não foi alterada.

Referências revisadas: False. Validade declarada na execução de origem: False.

## Critérios e denominadores

As dimensões podem se sobrepor. Não some seus percentuais nem use 100% menos uma categoria como qualidade global. Aprovação é calculada sobre avaliados (pass/partial/fail); cobertura é avaliados/aplicáveis. Pendências e casos sem resposta não são aprovações. Falhas técnicas reprovam a equivalência e o sucesso operacional, mas ficam sem avaliação de conteúdo final. Quantidades iguais de linhas/colunas não garantem valores ou significado corretos.

| Dimensão | Aplicáveis | Avaliados | Aprovados | Parciais | Reprovados | Pendentes | Sem avaliação possível | Aprovação/avaliados | Cobertura |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Seleção de bases | 68 | 68 | 68 | 0 | 0 | 0 | 0 | 100.00% | 100.00% |
| Seleção de relações | 4 | 4 | 4 | 0 | 0 | 0 | 0 | 100.00% | 100.00% |
| SQL aprovado | 64 | 64 | 56 | 0 | 8 | 0 | 0 | 87.50% | 100.00% |
| Sucesso operacional | 64 | 64 | 56 | 0 | 8 | 0 | 0 | 87.50% | 100.00% |
| Equivalência estrita | 64 | 64 | 52 | 0 | 12 | 0 | 0 | 81.25% | 100.00% |
| Quantidade de linhas | 64 | 56 | 56 | 0 | 0 | 0 | 8 | 100.00% | 87.50% |
| Quantidade de colunas | 64 | 56 | 56 | 0 | 0 | 0 | 8 | 100.00% | 87.50% |
| Limitação prevista | 4 | 4 | 4 | 0 | 0 | 0 | 0 | 100.00% | 100.00% |
| Filtros | 64 | 56 | 46 | 0 | 10 | 0 | 8 | 82.14% | 87.50% |
| Unidade e agregação | 64 | 56 | 53 | 1 | 2 | 0 | 8 | 94.64% | 87.50% |
| Dimensões e identificadores | 64 | 56 | 55 | 0 | 1 | 0 | 8 | 98.21% | 87.50% |
| Informação principal | 64 | 56 | 53 | 1 | 2 | 0 | 8 | 94.64% | 87.50% |
| Completude e escopo | 64 | 56 | 52 | 3 | 1 | 0 | 8 | 92.86% | 87.50% |
| Formato da saída | 64 | 56 | 47 | 7 | 2 | 0 | 8 | 83.93% | 87.50% |
| Fidelidade do texto | 64 | 56 | 47 | 4 | 5 | 0 | 8 | 83.93% | 87.50% |

Seleção nesta tabela significa igualdade de conjuntos por pergunta, não recall. Precisão/recall/F1 originais permanecem no JSON em original_summary.

- **Seleção de bases** (`dataset_selection`, automatic): Conjunto selecionado igual ao esperado.
- **Seleção de relações** (`relationship_selection`, automatic): Conjunto igual ao esperado nos casos com relação prevista.
- **SQL aprovado** (`sql_accepted`, automatic): SQL presente e aprovado pelo validador registrado.
- **Sucesso operacional** (`operational_success`, automatic): Resposta com success=true.
- **Equivalência estrita** (`result_equivalence`, automatic): Classificação original contra referência, incluindo contrato de saída.
- **Quantidade de linhas** (`row_count`, automatic): Mesma quantidade; não comprova completude semântica.
- **Quantidade de colunas** (`column_count`, automatic): Mesma quantidade; não comprova identidade ou ordem das colunas.
- **Limitação prevista** (`controlled_limitation`, automatic): Classificação original da limitação controlada.
- **Filtros** (`filters`, review): Período, localização, categorias e restrições correspondem ao pedido.
- **Unidade e agregação** (`aggregation`, review): Entidade contada, DISTINCT, grupos, denominadores e junções adequados.
- **Dimensões e identificadores** (`identification`, review): Campos, códigos, nomes e unidades solicitados são usados corretamente.
- **Informação principal** (`main_information`, review): Conteúdo principal solicitado está correto, independentemente de informação extra.
- **Completude e escopo** (`completeness`, review): Todos os elementos solicitados estão presentes, sem seleção indevida de grupos.
- **Formato da saída** (`output_contract`, review): Colunas, identificadores, ordem e informação adicional respeitam o pedido.
- **Fidelidade do texto** (`text_fidelity`, review): Texto corresponde à tabela e seus limites, sem extrapolações; não valida o SQL.

## Casos


### Q1 — correct

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Quantos registros de aplicação existem no total? Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Não há filtro de linha a aplicar além do escopo integral da base; o SQL não acrescenta recortes. Avaliado como atendimento ao escopo, não como dimensão não aplicável. Fonte: results[id=1].response e cases[id=1] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT(*) conta registros de aplicação; não deduplica pessoas. Fonte: results[id=1].response e cases[id=1] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['total'] representa as entidades e medidas solicitadas. Fonte: results[id=1].response e cases[id=1] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=1].response e cases[id=1] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=1].response e cases[id=1] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['total'], na ordem solicitada ['total']; representação compatível com o protocolo. Fonte: results[id=1].response e cases[id=1] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=1].response e cases[id=1] do pacote de referência vinculado. |

### Q2 — technical_failure

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Entre as UFs de residência com sigla não nula e diferente da string vazia, qual tem a maior contagem de registros cuja descrição de dose é exatamente '1ª Dose'? Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: uf,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | fail | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | fail | automatic | response.success |
| Equivalência estrita | fail | automatic | {"status": "technical_failure", "result_correct": false} |
| Quantidade de linhas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Quantidade de colunas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Unidade e agregação | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Dimensões e identificadores | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Informação principal | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Completude e escopo | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Formato da saída | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Fidelidade do texto | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |

### Q3 — correct

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Quantos registros têm descrição de dose exatamente igual a '2ª Dose'? Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | WHERE vacina_descricao_dose = '2ª Dose' preserva a igualdade exata. Fonte: results[id=3].response e cases[id=3] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT(*) nas linhas elegíveis equivale ao countIf da referência. Fonte: results[id=3].response e cases[id=3] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['total'] representa as entidades e medidas solicitadas. Fonte: results[id=3].response e cases[id=3] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=3].response e cases[id=3] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=3].response e cases[id=3] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['total'], na ordem solicitada ['total']; representação compatível com o protocolo. Fonte: results[id=3].response e cases[id=3] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=3].response e cases[id=3] do pacote de referência vinculado. |

### Q4 — correct

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Para cada UF de residência com sigla não nula e diferente da string vazia, calcule a contagem de registros de '1ª Dose' menos a contagem de '2ª Dose', usando essas descrições exatas. Inclua todas as UFs presentes, mesmo quando uma ou ambas as contagens forem zero. Retorne somente estas colunas, nesta ordem: uf,diferenca. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 28, "actual_row_count": 28} |
| Quantidade de linhas | pass | automatic | {"expected": 28, "actual": 28} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Exclui UF vazia/nula, sem excluir linhas de outras doses que mantêm UFs com diferenças zero. Fonte: results[id=4].response e cases[id=4] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | Conta por UF/dose e subtrai primeira menos segunda dose, mantendo todos os grupos. Fonte: results[id=4].response e cases[id=4] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['uf', 'diferenca'] representa as entidades e medidas solicitadas. Fonte: results[id=4].response e cases[id=4] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 28 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=4].response e cases[id=4] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (28 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=4].response e cases[id=4] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['uf', 'diferenca'], na ordem solicitada ['uf', 'diferenca']; representação compatível com o protocolo. Fonte: results[id=4].response e cases[id=4] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=4].response e cases[id=4] do pacote de referência vinculado. |

### Q5 — incorrect

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Qual é a razão entre a contagem de registros cuja descrição da dose contém 'reforço', sem distinguir maiúsculas de minúsculas, e a contagem com descrição exatamente '1ª Dose'? Retorne razão, não percentual, com pelo menos seis casas decimais; retorne nulo se o denominador for zero. Retorne somente estas colunas, nesta ordem: razao. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | fail | automatic | {"status": "incorrect", "result_correct": false, "mismatch_reasons": ["values_or_order_mismatch"], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Seleciona reforço com positionCaseInsensitiveUTF8 e primeira dose com igualdade exata. Fonte: results[id=5].response e cases[id=5] do pacote de referência vinculado. |
| Unidade e agregação | fail | ai_assisted | Divisão invertida: primeira_dose/reforco; pedido e referência exigem reforco/primeira_dose. Fonte: results[id=5].response e cases[id=5] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['razao'] representa as entidades e medidas solicitadas. Fonte: results[id=5].response e cases[id=5] do pacote de referência vinculado. |
| Informação principal | fail | ai_assisted | Retornou 1.5105337078651686; a razão solicitada e esperada é 0.6620176662017666. Numerador e denominador foram invertidos. Fonte: results[id=5].response e cases[id=5] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=5].response e cases[id=5] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['razao'], na ordem solicitada ['razao']; representação compatível com o protocolo. Fonte: results[id=5].response e cases[id=5] do pacote de referência vinculado. |
| Fidelidade do texto | fail | ai_assisted | O texto chama 1,510534 de reforços por primeira dose, mas o SQL calcula primeira dose por reforço. O resumo factual ainda reduz a precisão para 1,51; a explicação inverte o significado da razão. Fonte: results[id=5].response e cases[id=5] do pacote de referência vinculado. |

### Q6 — correct

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Qual é o percentual de registros com paciente_enumSexoBiologico igual a F e igual a M? Use como denominador somente a soma dos registros F e M, excluindo outras categorias. Retorne as duas categorias; se o denominador for zero, seus percentuais devem ser nulos. Retorne somente estas colunas, nesta ordem: sexo,percentual. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 2, "actual_row_count": 2} |
| Quantidade de linhas | pass | automatic | {"expected": 2, "actual": 2} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Restringe F e M antes de calcular o denominador compartilhado. Fonte: results[id=6].response e cases[id=6] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT por sexo e SUM(total) OVER() produzem percentuais de F/M, com NULLIF para zero. Fonte: results[id=6].response e cases[id=6] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['sexo', 'percentual'] representa as entidades e medidas solicitadas. Fonte: results[id=6].response e cases[id=6] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 2 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=6].response e cases[id=6] do pacote de referência vinculado. |
| Completude e escopo | partial | ai_assisted | No snapshot retornou F e M corretamente. Contudo, agrupa só categorias existentes: se uma faltar ou a base estiver vazia, não garante as duas categorias e seus nulos exigidos pelo enunciado. Fonte: results[id=6].response e cases[id=6] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['sexo', 'percentual'], na ordem solicitada ['sexo', 'percentual']; representação compatível com o protocolo. Fonte: results[id=6].response e cases[id=6] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=6].response e cases[id=6] do pacote de referência vinculado. |

### Q7 — correct

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Entre as faixas de idade 0 a 18, 19 a 59 e 60 anos ou mais presentes nos registros, qual tem a menor contagem? Use paciente_idade em anos e exclua idades nulas ou negativas. Não inclua faixas sem registros; use os rótulos 0-18, 19-59 e 60+. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: faixa,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Cada ramo restringe a faixa, excluindo idades nulas/negativas. Fonte: results[id=7].response e cases[id=7] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT por três faixas e MIN(total); porém UNION de agregados escalares cria faixas de contagem zero mesmo quando ausentes. Fonte: results[id=7].response e cases[id=7] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['faixa', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=7].response e cases[id=7] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=7].response e cases[id=7] do pacote de referência vinculado. |
| Completude e escopo | partial | ai_assisted | A faixa mínima retornada está correta neste snapshot. Porém o UNION ALL constrói sempre três agregados, incluindo faixas de contagem zero, contrariando a exclusão explícita de faixas ausentes. Fonte: results[id=7].response e cases[id=7] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['faixa', 'total'], na ordem solicitada ['faixa', 'total']; representação compatível com o protocolo. Fonte: results[id=7].response e cases[id=7] do pacote de referência vinculado. |
| Fidelidade do texto | partial | ai_assisted | A tabela contém o mínimo solicitado (60+, 53.986), mas o resumo diz “maior total”. Embora seja o máximo do resultado unitário, não comunica o mínimo entre as faixas e induz leitura equivocada. Fonte: results[id=7].response e cases[id=7] do pacote de referência vinculado. |

### Q8 — incorrect

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Quais combinações de UF e código IBGE de residência têm a maior contagem de registros? Exclua UF ou código municipal nulo ou igual à string vazia; identifique o município pelo código acompanhado da UF. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: uf,municipio,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | fail | automatic | {"status": "incorrect", "result_correct": false, "mismatch_reasons": ["values_or_order_mismatch"], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 3, "actual_widths": [3]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | fail | ai_assisted | Filtra paciente_endereco_nmMunicipio; deveria excluir código paciente_endereco_coIbgeMunicipio ausente, além de UF ausente. A coincidência eventual dos resultados não implementa o filtro ausente. Fonte: results[id=8].response e cases[id=8] do pacote de referência vinculado. |
| Unidade e agregação | partial | ai_assisted | COUNT e máximo empatado estão presentes, mas o agrupamento usa nome municipal em vez do código IBGE; nomes homônimos podem unir entidades diferentes. Fonte: results[id=8].response e cases[id=8] do pacote de referência vinculado. |
| Dimensões e identificadores | fail | ai_assisted | Retorna RIO BRANCO em municipio; a pergunta pede o código IBGE e a referência retorna 120040. Nome não substitui o identificador solicitado. Fonte: results[id=8].response e cases[id=8] do pacote de referência vinculado. |
| Informação principal | partial | ai_assisted | Contagem 187.760 e UF AC coincidem, mas o identificador municipal pedido não foi fornecido. A revisão não presume equivalência nome/código para outros registros. Fonte: results[id=8].response e cases[id=8] do pacote de referência vinculado. |
| Completude e escopo | partial | ai_assisted | Seleciona máximo com empates e retorna UF/contagem, mas falta o código municipal solicitado e a chave de agrupamento foi trocada. Fonte: results[id=8].response e cases[id=8] do pacote de referência vinculado. |
| Formato da saída | fail | ai_assisted | Há três colunas na ordem pedida, porém municipio contém nome em vez de código IBGE: mesma largura não satisfaz o contrato. Fonte: results[id=8].response e cases[id=8] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=8].response e cases[id=8] do pacote de referência vinculado. |

### Q9 — correct

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Qual é a contagem por UF de residência e faixa etária de 0 a 18, 19 a 59 e 60 anos ou mais? Use paciente_idade em anos; exclua idades nulas ou negativas e UFs nulas ou iguais à string vazia. Inclua todos os grupos presentes e use os rótulos 0-18, 19-59 e 60+. Retorne somente estas colunas, nesta ordem: uf,faixa,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 83, "actual_row_count": 83} |
| Quantidade de linhas | pass | automatic | {"expected": 83, "actual": 83} |
| Quantidade de colunas | pass | automatic | {"expected": 3, "actual_widths": [3]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | WHERE idade >= 0 exclui negativos/nulos e UF <> vazio exclui UF vazia/nula. Fonte: results[id=9].response e cases[id=9] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | CASE forma faixas 0-18,19-59,60+; COUNT por UF/faixa e todos os grupos. Fonte: results[id=9].response e cases[id=9] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['uf', 'faixa', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=9].response e cases[id=9] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 83 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=9].response e cases[id=9] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (83 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=9].response e cases[id=9] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['uf', 'faixa', 'total'], na ordem solicitada ['uf', 'faixa', 'total']; representação compatível com o protocolo. Fonte: results[id=9].response e cases[id=9] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=9].response e cases[id=9] do pacote de referência vinculado. |

### Q10 — correct

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Qual é a contagem de registros por sistema_origem? Retorne todos os grupos, incluindo valores nulos como um grupo nulo e strings vazias como um grupo separado. Retorne somente estas colunas, nesta ordem: sistema_origem,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 5, "actual_row_count": 5} |
| Quantidade de linhas | pass | automatic | {"expected": 5, "actual": 5} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Não há filtro de linha a aplicar além do escopo integral da base; o SQL não acrescenta recortes. Avaliado como atendimento ao escopo, não como dimensão não aplicável. Fonte: results[id=10].response e cases[id=10] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | GROUP BY sistema_origem e COUNT de linhas preservam todos os grupos. Fonte: results[id=10].response e cases[id=10] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['sistema_origem', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=10].response e cases[id=10] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 5 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=10].response e cases[id=10] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (5 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=10].response e cases[id=10] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['sistema_origem', 'total'], na ordem solicitada ['sistema_origem', 'total']; representação compatível com o protocolo. Fonte: results[id=10].response e cases[id=10] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=10].response e cases[id=10] do pacote de referência vinculado. |

### Q11 — technical_failure

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Qual vacina_nome não nulo e diferente da string vazia tem a maior contagem de registros, e qual é o percentual desse grupo sobre todas as linhas da base, incluindo no denominador aquelas sem nome de vacina? Retorne o nome da vacina e o percentual. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: vacina,percentual. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | fail | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | fail | automatic | response.success |
| Equivalência estrita | fail | automatic | {"status": "technical_failure", "result_correct": false} |
| Quantidade de linhas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Quantidade de colunas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Unidade e agregação | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Dimensões e identificadores | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Informação principal | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Completude e escopo | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Formato da saída | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Fidelidade do texto | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |

### Q12 — correct

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Qual fabricante tem a maior contagem de registros? Agrupe por vacina_fabricante_nome, excluindo valores nulos e iguais à string vazia; preserve os demais nomes como estão armazenados. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: fabricante,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Exclui fabricante nulo/vazio, sem normalizar nomes indevidamente. Fonte: results[id=12].response e cases[id=12] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT por fabricante e igualdade com MAX(total) incluem todos os extremos empatados. Fonte: results[id=12].response e cases[id=12] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['fabricante', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=12].response e cases[id=12] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=12].response e cases[id=12] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=12].response e cases[id=12] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['fabricante', 'total'], na ordem solicitada ['fabricante', 'total']; representação compatível com o protocolo. Fonte: results[id=12].response e cases[id=12] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=12].response e cases[id=12] do pacote de referência vinculado. |

### Q13 — correct

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Qual é a contagem por ano e mês da data de aplicação vacina_dataAplicacao? Exclua datas nulas, inclua todos os meses presentes e identifique cada mês no formato AAAA-MM. Retorne somente estas colunas, nesta ordem: mes,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 45, "actual_row_count": 45} |
| Quantidade de linhas | pass | automatic | {"expected": 45, "actual": 45} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Exclui vacina_dataAplicacao nula, sem outro recorte. Fonte: results[id=13].response e cases[id=13] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | formatDateTime %Y-%m distingue anos; COUNT por mês, sem LIMIT. Fonte: results[id=13].response e cases[id=13] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['mes', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=13].response e cases[id=13] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 45 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=13].response e cases[id=13] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (45 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=13].response e cases[id=13] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['mes', 'total'], na ordem solicitada ['mes', 'total']; representação compatível com o protocolo. Fonte: results[id=13].response e cases[id=13] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=13].response e cases[id=13] do pacote de referência vinculado. |

### Q14 — correct

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Qual combinação de UF de residência e ano/mês de aplicação tem a maior contagem de registros? Exclua UFs nulas ou iguais à string vazia e datas de aplicação nulas. Identifique o mês no formato AAAA-MM. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: uf,mes,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 3, "actual_widths": [3]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Exclui UF vazia/nula e data nula. Fonte: results[id=14].response e cases[id=14] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT por UF/mês AAAA-MM; igualdade com MAX(total) seleciona empates. Fonte: results[id=14].response e cases[id=14] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['uf', 'mes', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=14].response e cases[id=14] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=14].response e cases[id=14] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=14].response e cases[id=14] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['uf', 'mes', 'total'], na ordem solicitada ['uf', 'mes', 'total']; representação compatível com o protocolo. Fonte: results[id=14].response e cases[id=14] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=14].response e cases[id=14] do pacote de referência vinculado. |

### Q15 — correct

Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. Qual é a contagem por descrição de dose que contenha 'reforço', sem distinguir maiúsculas de minúsculas na seleção? Preserve a descrição original no agrupamento e retorne todos os grupos encontrados. Retorne somente estas colunas, nesta ordem: dose,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao"], "actual": ["covid-19-vacinacao"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 4, "actual_row_count": 4} |
| Quantidade de linhas | pass | automatic | {"expected": 4, "actual": 4} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Busca reforço sem distinguir caixa e mantém descrição original. Fonte: results[id=15].response e cases[id=15] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | GROUP BY descrição e COUNT(*) preservam todas as descrições encontradas. Fonte: results[id=15].response e cases[id=15] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['dose', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=15].response e cases[id=15] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 4 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=15].response e cases[id=15] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (4 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=15].response e cases[id=15] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['dose', 'total'], na ordem solicitada ['dose', 'total']; representação compatível com o protocolo. Fonte: results[id=15].response e cases[id=15] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=15].response e cases[id=15] do pacote de referência vinculado. |

### Q16 — correct

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Quantas UBS distintas existem nesse cadastro? Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | WHERE cnes > 0 é explícito. Fonte: results[id=16].response e cases[id=16] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT(DISTINCT cnes) conta UBS distintas, não linhas. Fonte: results[id=16].response e cases[id=16] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['total'] representa as entidades e medidas solicitadas. Fonte: results[id=16].response e cases[id=16] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=16].response e cases[id=16] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=16].response e cases[id=16] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['total'], na ordem solicitada ['total']; representação compatível com o protocolo. Fonte: results[id=16].response e cases[id=16] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=16].response e cases[id=16] do pacote de referência vinculado. |

### Q17 — correct

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Qual é a contagem de UBS por código de UF? Exclua código de UF nulo ou cuja representação textual seja vazia e inclua todos os códigos presentes, sem convertê-los em siglas. Retorne somente estas colunas, nesta ordem: uf,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 27, "actual_row_count": 27} |
| Quantidade de linhas | pass | automatic | {"expected": 27, "actual": 27} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | fail | ai_assisted | Exclui UF nula/texto vazio com toString, mas omite cnes > 0. A coincidência eventual dos resultados não implementa o filtro ausente. Fonte: results[id=17].response e cases[id=17] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT(DISTINCT cnes) por UF é a operação pedida; omissão de elegibilidade é registrada em filtros. Fonte: results[id=17].response e cases[id=17] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['uf', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=17].response e cases[id=17] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 27 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=17].response e cases[id=17] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (27 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=17].response e cases[id=17] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['uf', 'total'], na ordem solicitada ['uf', 'total']; representação compatível com o protocolo. Fonte: results[id=17].response e cases[id=17] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=17].response e cases[id=17] do pacote de referência vinculado. |

### Q18 — correct

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Qual código de UF tem a maior contagem de UBS? Exclua código de UF nulo ou cuja representação textual seja vazia; retorne o código, sem convertê-lo em sigla. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: uf,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | cnes > 0 e UF textual não vazia/nula estão presentes. Fonte: results[id=18].response e cases[id=18] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT DISTINCT por UF; seleciona total = MAX(total), preservando empates. Fonte: results[id=18].response e cases[id=18] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['uf', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=18].response e cases[id=18] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=18].response e cases[id=18] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=18].response e cases[id=18] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['uf', 'total'], na ordem solicitada ['uf', 'total']; representação compatível com o protocolo. Fonte: results[id=18].response e cases[id=18] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=18].response e cases[id=18] do pacote de referência vinculado. |

### Q19 — correct

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Quantos códigos IBGE de município distintos e positivos possuem pelo menos uma UBS com CNES positivo? Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | fail | ai_assisted | WHERE cnes > 0 está presente, mas ibge > 0 foi omitido. A coincidência eventual dos resultados não implementa o filtro ausente. Fonte: results[id=19].response e cases[id=19] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT(DISTINCT ibge) conta municípios, não CNES. Fonte: results[id=19].response e cases[id=19] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['total'] representa as entidades e medidas solicitadas. Fonte: results[id=19].response e cases[id=19] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=19].response e cases[id=19] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=19].response e cases[id=19] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['total'], na ordem solicitada ['total']; representação compatível com o protocolo. Fonte: results[id=19].response e cases[id=19] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=19].response e cases[id=19] do pacote de referência vinculado. |

### Q20 — correct

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Entre os municípios com código IBGE positivo e pelo menos uma UBS com CNES positivo, quais têm a maior contagem de UBS? Identifique cada município pelo código IBGE. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: municipio,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | CNES e IBGE positivos estão explicitamente filtrados. Fonte: results[id=20].response e cases[id=20] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT DISTINCT CNES por IBGE, selecionando MAX(total_ubs) com empates. Fonte: results[id=20].response e cases[id=20] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['municipio', 'total_ubs'] representa as entidades e medidas solicitadas. Fonte: results[id=20].response e cases[id=20] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=20].response e cases[id=20] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=20].response e cases[id=20] do pacote de referência vinculado. |
| Formato da saída | partial | ai_assisted | Conteúdo, quantidade e ordem das colunas estão corretos, mas os nomes não seguem literalmente o pedido: recebido ['municipio', 'total_ubs']; solicitado ['municipio', 'total']. A métrica estrita de valores não verifica esses aliases. Fonte: results[id=20].response e cases[id=20] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=20].response e cases[id=20] do pacote de referência vinculado. |

### Q21 — correct

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Entre os municípios com código IBGE positivo e pelo menos uma UBS com CNES positivo, quais têm a maior contagem de UBS? Identifique cada município pelo código IBGE. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: municipio,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | CNES e IBGE positivos estão explicitamente filtrados. Fonte: results[id=21].response e cases[id=21] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT DISTINCT CNES por IBGE, selecionando MAX(total_ubs) com empates. Fonte: results[id=21].response e cases[id=21] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['municipio', 'total_ubs'] representa as entidades e medidas solicitadas. Fonte: results[id=21].response e cases[id=21] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=21].response e cases[id=21] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=21].response e cases[id=21] do pacote de referência vinculado. |
| Formato da saída | partial | ai_assisted | Conteúdo, quantidade e ordem das colunas estão corretos, mas os nomes não seguem literalmente o pedido: recebido ['municipio', 'total_ubs']; solicitado ['municipio', 'total']. A métrica estrita de valores não verifica esses aliases. Fonte: results[id=21].response e cases[id=21] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=21].response e cases[id=21] do pacote de referência vinculado. |

### Q22 — correct

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Qual é a contagem de UBS por código IBGE positivo de município nas UFs de códigos 21, 22, 23, 24, 25, 26, 27, 28 e 29, correspondentes ao Nordeste? Inclua todos os municípios encontrados nesse recorte. Retorne somente estas colunas, nesta ordem: municipio,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1783, "actual_row_count": 1783} |
| Quantidade de linhas | pass | automatic | {"expected": 1783, "actual": 1783} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | fail | ai_assisted | UF IN 21..29 e cnes > 0 presentes; falta ibge > 0. A coincidência eventual dos resultados não implementa o filtro ausente. Fonte: results[id=22].response e cases[id=22] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT DISTINCT CNES por município, sem limitar linhas. Fonte: results[id=22].response e cases[id=22] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['municipio', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=22].response e cases[id=22] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1783 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=22].response e cases[id=22] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1783 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=22].response e cases[id=22] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['municipio', 'total'], na ordem solicitada ['municipio', 'total']; representação compatível com o protocolo. Fonte: results[id=22].response e cases[id=22] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=22].response e cases[id=22] do pacote de referência vinculado. |

### Q23 — correct

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Quantas UBS têm pelo menos um registro com latitude diferente de zero e entre -90 e 90, e longitude diferente de zero e entre -180 e 180, incluindo os limites? As duas condições devem ocorrer na mesma linha; essa regra é um critério operacional de preenchimento, não validação da localização real. Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | CNES positivo, latitude/longitude não zero e intervalos inclusivos estão na mesma linha. Fonte: results[id=23].response e cases[id=23] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT DISTINCT CNES após filtros conta uma UBS mesmo com várias linhas elegíveis. Fonte: results[id=23].response e cases[id=23] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['total'] representa as entidades e medidas solicitadas. Fonte: results[id=23].response e cases[id=23] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=23].response e cases[id=23] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=23].response e cases[id=23] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['total'], na ordem solicitada ['total']; representação compatível com o protocolo. Fonte: results[id=23].response e cases[id=23] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=23].response e cases[id=23] do pacote de referência vinculado. |

### Q24 — correct

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Quais municípios de código IBGE positivo têm a maior contagem de UBS com pelo menos uma linha contendo latitude diferente de zero e entre -90 e 90 e longitude diferente de zero e entre -180 e 180, incluindo os limites? As condições devem ocorrer na mesma linha. Considere somente municípios com UBS que atendam ao filtro. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: municipio,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | fail | ai_assisted | CNES positivo e coordenadas válidas presentes; falta ibge > 0. A coincidência eventual dos resultados não implementa o filtro ausente. Fonte: results[id=24].response e cases[id=24] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT DISTINCT CNES por IBGE e máximo empatado, sem JOIN multiplicador. Fonte: results[id=24].response e cases[id=24] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['municipio', 'total_ubs'] representa as entidades e medidas solicitadas. Fonte: results[id=24].response e cases[id=24] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=24].response e cases[id=24] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=24].response e cases[id=24] do pacote de referência vinculado. |
| Formato da saída | partial | ai_assisted | Conteúdo, quantidade e ordem das colunas estão corretos, mas os nomes não seguem literalmente o pedido: recebido ['municipio', 'total_ubs']; solicitado ['municipio', 'total']. A métrica estrita de valores não verifica esses aliases. Fonte: results[id=24].response e cases[id=24] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=24].response e cases[id=24] do pacote de referência vinculado. |

### Q25 — incorrect

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Qual é a contagem de UBS por código de UF, código IBGE municipal e bairro? Exclua UF nula ou cuja representação textual seja vazia, município não positivo e bairro nulo ou vazio após remover espaços nas extremidades. Preserve o nome original do bairro no agrupamento; não una bairros homônimos de municípios diferentes. Retorne todos os grupos presentes. Retorne somente estas colunas, nesta ordem: uf,municipio,bairro,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | fail | automatic | {"status": "incorrect", "result_correct": false, "mismatch_reasons": ["values_or_order_mismatch"], "expected_row_count": 33696, "actual_row_count": 33696} |
| Quantidade de linhas | pass | automatic | {"expected": 33696, "actual": 33696} |
| Quantidade de colunas | pass | automatic | {"expected": 4, "actual_widths": [4]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | fail | ai_assisted | Faltam cnes > 0 e trim de bairro; bairro <> vazio não exclui só espaços. Acrescenta uf > 0, diferente da representação textual não vazia pedida. A coincidência eventual dos resultados não implementa o filtro ausente. Fonte: results[id=25].response e cases[id=25] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT DISTINCT CNES por UF/IBGE/bairro preserva nome original e separa bairros homônimos; filtros são analisados separadamente. Fonte: results[id=25].response e cases[id=25] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | UF e IBGE mantêm os códigos; toString muda seus tipos, mas todos os códigos correspondem aos esperados após conferência explícita de representação. Fonte: results[id=25].response e cases[id=25] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | As 33.696 linhas têm os mesmos códigos, bairros e contagens após converter identificadores para texto apenas nesta conferência. Isso não altera a reprovação estrita original nem aprova os filtros omitidos. Fonte: results[id=25].response e cases[id=25] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (33696 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=25].response e cases[id=25] do pacote de referência vinculado. |
| Formato da saída | fail | ai_assisted | UF/IBGE retornam strings por toString; a referência congela identificadores numéricos. Colunas e ordem coincidem, mas a representação difere. A comparação estrita original permanece incorreta. Fonte: results[id=25].response e cases[id=25] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=25].response e cases[id=25] do pacote de referência vinculado. |

### Q26 — correct

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Qual é a contagem de UBS por código de UF? Exclua código de UF nulo ou cuja representação textual seja vazia e inclua todos os códigos presentes, sem convertê-los em siglas. Retorne somente estas colunas, nesta ordem: uf,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 27, "actual_row_count": 27} |
| Quantidade de linhas | pass | automatic | {"expected": 27, "actual": 27} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | fail | ai_assisted | Exclui UF nula/texto vazio com toString, mas omite cnes > 0. A coincidência eventual dos resultados não implementa o filtro ausente. Fonte: results[id=26].response e cases[id=26] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT DISTINCT CNES por UF correto como operação; não corrige a omissão do filtro. Fonte: results[id=26].response e cases[id=26] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['uf', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=26].response e cases[id=26] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 27 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=26].response e cases[id=26] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (27 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=26].response e cases[id=26] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['uf', 'total'], na ordem solicitada ['uf', 'total']; representação compatível com o protocolo. Fonte: results[id=26].response e cases[id=26] do pacote de referência vinculado. |
| Fidelidade do texto | fail | ai_assisted | A explicação associa código 31 ao Rio de Janeiro e depois a Minas Gerais; inventa código 91 e mínimo 1.021 para Roraima. A tabela não contém 91/1.021 e seu mínimo é 162 no código 16. O resumo factual correto não anula a explicação incorreta. Fonte: results[id=26].response e cases[id=26] do pacote de referência vinculado. |

### Q27 — correct

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Qual código de UF tem a maior contagem de UBS? Exclua código de UF nulo ou cuja representação textual seja vazia; retorne o código, sem convertê-lo em sigla. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: uf,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | CNES positivo e UF textual não vazia/nula estão presentes. Fonte: results[id=27].response e cases[id=27] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT DISTINCT por UF com MAX(total) inclui todos os empates. Fonte: results[id=27].response e cases[id=27] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['uf', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=27].response e cases[id=27] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=27].response e cases[id=27] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=27].response e cases[id=27] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['uf', 'total'], na ordem solicitada ['uf', 'total']; representação compatível com o protocolo. Fonte: results[id=27].response e cases[id=27] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=27].response e cases[id=27] do pacote de referência vinculado. |

### Q28 — correct

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Quantas UBS têm pelo menos uma linha com logradouro e bairro ambos não nulos e não vazios após remover espaços nas extremidades? As duas condições devem ocorrer na mesma linha. Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | CNES positivo e TRIM(logradouro)/TRIM(bairro) não vazios exigidos na mesma linha. Fonte: results[id=28].response e cases[id=28] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT DISTINCT CNES conta UBS com ao menos uma linha elegível. Fonte: results[id=28].response e cases[id=28] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['total'] representa as entidades e medidas solicitadas. Fonte: results[id=28].response e cases[id=28] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=28].response e cases[id=28] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=28].response e cases[id=28] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['total'], na ordem solicitada ['total']; representação compatível com o protocolo. Fonte: results[id=28].response e cases[id=28] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=28].response e cases[id=28] do pacote de referência vinculado. |

### Q29 — correct

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Qual é a contagem de UBS por bairro no município cujo código IBGE armazenado é 355030? Preserve os bairros como armazenados e inclua todos os grupos, inclusive bairro vazio ou nulo, se presentes. Retorne somente estas colunas, nesta ordem: bairro,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 449, "actual_row_count": 449} |
| Quantidade de linhas | pass | automatic | {"expected": 449, "actual": 449} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | fail | ai_assisted | ibge = 355030 presente e bairro não é filtrado; falta cnes > 0. A coincidência eventual dos resultados não implementa o filtro ausente. Fonte: results[id=29].response e cases[id=29] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT DISTINCT CNES por bairro mantém bairros vazios/nulos presentes. Fonte: results[id=29].response e cases[id=29] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['bairro', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=29].response e cases[id=29] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 449 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=29].response e cases[id=29] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (449 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=29].response e cases[id=29] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['bairro', 'total'], na ordem solicitada ['bairro', 'total']; representação compatível com o protocolo. Fonte: results[id=29].response e cases[id=29] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=29].response e cases[id=29] do pacote de referência vinculado. |

### Q30 — correct

Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. Entre os municípios de código IBGE positivo com pelo menos uma UBS de CNES positivo, quais têm a menor contagem de UBS? Não inclua municípios ausentes do cadastro nem atribua zero a eles. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: municipio,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica"], "actual": ["atencao-basica"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 720, "actual_row_count": 720} |
| Quantidade de linhas | pass | automatic | {"expected": 720, "actual": 720} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | CNES e IBGE positivos estão filtrados. Fonte: results[id=30].response e cases[id=30] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | Agrupa municípios existentes e seleciona MIN(total_ubs), com todos os 720 empates retornados. Fonte: results[id=30].response e cases[id=30] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['municipio', 'total_ubs'] representa as entidades e medidas solicitadas. Fonte: results[id=30].response e cases[id=30] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 720 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=30].response e cases[id=30] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (720 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=30].response e cases[id=30] do pacote de referência vinculado. |
| Formato da saída | partial | ai_assisted | Conteúdo, quantidade e ordem das colunas estão corretos, mas os nomes não seguem literalmente o pedido: recebido ['municipio', 'total_ubs']; solicitado ['municipio', 'total']. A métrica estrita de valores não verifica esses aliases. Fonte: results[id=30].response e cases[id=30] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=30].response e cases[id=30] do pacote de referência vinculado. |

### Q31 — correct

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Quantas linhas de notificações existem no total? Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Não há filtro de linha a aplicar além do escopo integral da base; o SQL não acrescenta recortes. Avaliado como atendimento ao escopo, não como dimensão não aplicável. Fonte: results[id=31].response e cases[id=31] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT(*) conta linhas, sem deduplicar pessoas/episódios. Fonte: results[id=31].response e cases[id=31] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['total'] representa as entidades e medidas solicitadas. Fonte: results[id=31].response e cases[id=31] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=31].response e cases[id=31] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=31].response e cases[id=31] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['total'], na ordem solicitada ['total']; representação compatível com o protocolo. Fonte: results[id=31].response e cases[id=31] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=31].response e cases[id=31] do pacote de referência vinculado. |

### Q32 — correct

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Qual é a contagem por ano da data de notificação dt_notific e valor da semana sem_not? Exclua dt_notific nula ou igual a '1970-01-01'. Use sem_not como armazenada, sem recalcular a semana; retorne todos os grupos presentes. Retorne somente estas colunas, nesta ordem: ano,semana,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 20, "actual_row_count": 20} |
| Quantidade de linhas | pass | automatic | {"expected": 20, "actual": 20} |
| Quantidade de colunas | pass | automatic | {"expected": 3, "actual_widths": [3]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Exclui data nula e 1970-01-01. Fonte: results[id=32].response e cases[id=32] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | Agrupa ano %Y e sem_not armazenada, sem recalcular semana; ano textual é permitido pela normalização da referência. Fonte: results[id=32].response e cases[id=32] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['ano', 'semana', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=32].response e cases[id=32] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 20 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=32].response e cases[id=32] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (20 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=32].response e cases[id=32] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['ano', 'semana', 'total'], na ordem solicitada ['ano', 'semana', 'total']; representação compatível com o protocolo. Fonte: results[id=32].response e cases[id=32] do pacote de referência vinculado. |
| Fidelidade do texto | partial | ai_assisted | Os valores 21 e 7.131 aparecem na tabela, mas o destaque do maior total informa apenas o ano 2026; omite a semana 16 que identifica esse grupo. Trata a semana como métrica de máximo, embora seja dimensão temporal. Fonte: results[id=32].response e cases[id=32] do pacote de referência vinculado. |

### Q33 — correct

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Qual UF de notificação, identificada por sg_uf_not não nula e diferente da string vazia, tem a maior contagem de linhas? Não use a UF de residência. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: uf,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | sg_uf_not não vazia/nula; não usa residência. Fonte: results[id=33].response e cases[id=33] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT por UF de notificação e seleção pelo máximo com empates. Fonte: results[id=33].response e cases[id=33] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['uf', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=33].response e cases[id=33] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=33].response e cases[id=33] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=33].response e cases[id=33] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['uf', 'total'], na ordem solicitada ['uf', 'total']; representação compatível com o protocolo. Fonte: results[id=33].response e cases[id=33] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=33].response e cases[id=33] do pacote de referência vinculado. |

### Q34 — correct

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Qual é a contagem de linhas por UF de notificação sg_uf_not? Exclua UF nula ou igual à string vazia, retorne todas as UFs presentes e não use a UF de residência. Retorne somente estas colunas, nesta ordem: uf,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 27, "actual_row_count": 27} |
| Quantidade de linhas | pass | automatic | {"expected": 27, "actual": 27} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | sg_uf_not não vazia/nula, sem recorte adicional. Fonte: results[id=34].response e cases[id=34] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT por UF de notificação, todos os grupos presentes. Fonte: results[id=34].response e cases[id=34] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['uf', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=34].response e cases[id=34] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 27 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=34].response e cases[id=34] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (27 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=34].response e cases[id=34] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['uf', 'total'], na ordem solicitada ['uf', 'total']; representação compatível com o protocolo. Fonte: results[id=34].response e cases[id=34] do pacote de referência vinculado. |
| Fidelidade do texto | partial | ai_assisted | Valores e UFs citados conferem, mas rotula contagens de linhas sem deduplicação/classificação final como “casos de SRAG”. O pedido define notificações; a redação amplia o significado da unidade. Fonte: results[id=34].response e cases[id=34] do pacote de referência vinculado. |

### Q35 — correct

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Quantos códigos de município de notificação co_mun_not distintos e positivos aparecem na base? Não conte municípios de residência. Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | co_mun_not > 0 está presente. Fonte: results[id=35].response e cases[id=35] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT DISTINCT códigos municipais de notificação, sem contar municípios de residência. Fonte: results[id=35].response e cases[id=35] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['total'] representa as entidades e medidas solicitadas. Fonte: results[id=35].response e cases[id=35] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=35].response e cases[id=35] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=35].response e cases[id=35] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['total'], na ordem solicitada ['total']; representação compatível com o protocolo. Fonte: results[id=35].response e cases[id=35] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=35].response e cases[id=35] do pacote de referência vinculado. |

### Q36 — correct

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Qual é o percentual de linhas com hospital = 1 sobre todas as linhas? Mantenha registros com hospital nulo ou desconhecido no denominador. Multiplique a razão por 100 e retorne nulo se não houver linhas. Retorne somente estas colunas, nesta ordem: percentual. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Nenhum filtro global exclui hospital nulo/desconhecido do denominador. Fonte: results[id=36].response e cases[id=36] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | SUM CASE hospital=1 / COUNT(*) *100; ELSE 0 e NULLIF respeitam numerador e denominador. Fonte: results[id=36].response e cases[id=36] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['percentual'] representa as entidades e medidas solicitadas. Fonte: results[id=36].response e cases[id=36] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=36].response e cases[id=36] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=36].response e cases[id=36] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['percentual'], na ordem solicitada ['percentual']; representação compatível com o protocolo. Fonte: results[id=36].response e cases[id=36] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=36].response e cases[id=36] do pacote de referência vinculado. |

### Q37 — correct

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Quantas linhas têm evolucao = 2? Conte somente esse código, sem inferir desfechos para valores ausentes ou diferentes. Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | WHERE evolucao=2 limita exatamente ao código solicitado. Fonte: results[id=37].response e cases[id=37] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT(*) conta linhas com esse código, sem inferir outros desfechos. Fonte: results[id=37].response e cases[id=37] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['total'] representa as entidades e medidas solicitadas. Fonte: results[id=37].response e cases[id=37] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=37].response e cases[id=37] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=37].response e cases[id=37] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['total'], na ordem solicitada ['total']; representação compatível com o protocolo. Fonte: results[id=37].response e cases[id=37] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=37].response e cases[id=37] do pacote de referência vinculado. |

### Q38 — correct

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Entre as linhas com hospital = 1, qual é o percentual que também tem evolucao = 2? O denominador inclui todas as linhas com hospital = 1, inclusive evolução nula ou desconhecida. Multiplique a razão por 100 e retorne nulo se o denominador for zero. Retorne somente estas colunas, nesta ordem: percentual. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | hospital=1 no denominador; hospital=1 AND evolucao=2 no numerador. Fonte: results[id=38].response e cases[id=38] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | Divide contagens escalares, multiplica por 100 e protege denominador zero; CROSS JOIN de duas linhas agregadas não multiplica casos. Fonte: results[id=38].response e cases[id=38] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['percentual'] representa as entidades e medidas solicitadas. Fonte: results[id=38].response e cases[id=38] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=38].response e cases[id=38] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=38].response e cases[id=38] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['percentual'], na ordem solicitada ['percentual']; representação compatível com o protocolo. Fonte: results[id=38].response e cases[id=38] do pacote de referência vinculado. |
| Fidelidade do texto | fail | ai_assisted | O texto interpreta evolucao=2 como evolução positiva/melhoria. O metadado SRAG EVOLUCAO define 2=Óbito. O percentual 4,44 está correto, mas a interpretação do desfecho foi invertida. Fonte: results[id=38].response e cases[id=38] do pacote de referência vinculado. |

### Q39 — correct

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Qual é o percentual de linhas com uti = 1 sobre todas as linhas? Mantenha uti nula ou desconhecida no denominador. Multiplique a razão por 100 e retorne nulo se não houver linhas. Retorne somente estas colunas, nesta ordem: percentual. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | COUNT total mantém uti nula/desconhecida; numerador uti=1. Fonte: results[id=39].response e cases[id=39] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | 100*contagem uti=1/total; CASE e NULLIF protegem denominador zero. Fonte: results[id=39].response e cases[id=39] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['percentual'] representa as entidades e medidas solicitadas. Fonte: results[id=39].response e cases[id=39] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=39].response e cases[id=39] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=39].response e cases[id=39] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['percentual'], na ordem solicitada ['percentual']; representação compatível com o protocolo. Fonte: results[id=39].response e cases[id=39] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=39].response e cases[id=39] do pacote de referência vinculado. |

### Q40 — incorrect

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Qual UF de notificação sg_uf_not não nula e diferente da string vazia tem o maior percentual de linhas com evolucao = 2? Use todas as linhas de cada UF no respectivo denominador, inclusive evolução nula ou desconhecida, e multiplique a razão por 100. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: uf,percentual. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | fail | automatic | {"status": "incorrect", "result_correct": false, "mismatch_reasons": ["values_or_order_mismatch"], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Exclui sg_uf_not vazia/nula e mantém todas as linhas de cada UF no denominador. Fonte: results[id=40].response e cases[id=40] do pacote de referência vinculado. |
| Unidade e agregação | fail | ai_assisted | Percentual por UF calculado corretamente, mas seleciona MAX(TotalObitos), não MAX(percentual): maximiza contagem absoluta. Fonte: results[id=40].response e cases[id=40] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['uf', 'percentual'] representa as entidades e medidas solicitadas. Fonte: results[id=40].response e cases[id=40] do pacote de referência vinculado. |
| Informação principal | fail | ai_assisted | Retorna SP com 4.438280166435506%, enquanto a maior proporção pedida é PI com 13.16793893129771%. Fonte: results[id=40].response e cases[id=40] do pacote de referência vinculado. |
| Completude e escopo | fail | ai_assisted | Seleciona o extremo de contagem absoluta de óbitos, não o extremo percentual solicitado, omitindo a UF vencedora correta. Fonte: results[id=40].response e cases[id=40] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['uf', 'percentual'], na ordem solicitada ['uf', 'percentual']; representação compatível com o protocolo. Fonte: results[id=40].response e cases[id=40] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | O resumo “nos dados retornados, maior percentual: SP (4,44)” coincide com a única linha retornada. Esta aprovação é de fidelidade à tabela, não de correção da seleção, reprovada em agregação, informação principal e escopo. Fonte: results[id=40].response e cases[id=40] do pacote de referência vinculado. |

### Q41 — correct

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Quantas linhas têm valor 1 em cada indicador febre, tosse, garganta, dispneia, diarreia e vomito? Conte cada indicador separadamente; uma mesma linha pode contribuir para vários indicadores. Retorne uma única linha com as seis contagens. Retorne somente estas colunas, nesta ordem: febre,tosse,garganta,dispneia,diarreia,vomito. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 6, "actual_widths": [6]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Cada countIf testa seu indicador =1, sem exigir exclusividade. Fonte: results[id=41].response e cases[id=41] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | Seis countIf independentes permitem que uma notificação contribua para vários sintomas. Fonte: results[id=41].response e cases[id=41] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['febre', 'tosse', 'garganta', 'dispneia', 'diarreia', 'vomito'] representa as entidades e medidas solicitadas. Fonte: results[id=41].response e cases[id=41] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=41].response e cases[id=41] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=41].response e cases[id=41] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['febre', 'tosse', 'garganta', 'dispneia', 'diarreia', 'vomito'], na ordem solicitada ['febre', 'tosse', 'garganta', 'dispneia', 'diarreia', 'vomito']; representação compatível com o protocolo. Fonte: results[id=41].response e cases[id=41] do pacote de referência vinculado. |
| Fidelidade do texto | partial | ai_assisted | Tosse é de fato o indicador mais frequente, mas a ordem posterior é falsa: vomito=11.283 supera garganta=10.769 e diarreia=7.973; o texto coloca vômito por último. As seis contagens da tabela permanecem corretas. Fonte: results[id=41].response e cases[id=41] do pacote de referência vinculado. |

### Q42 — technical_failure

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Qual faixa etária presente tem a maior contagem de linhas: 0-18, 19-59 ou 60+? Para este teste, use nu_idade_n como magnitude e tp_idade 1=dias, 2=meses e 3=anos. Exclua magnitudes nulas ou negativas e unidades diferentes de 1, 2 ou 3. Converta dias dividindo por 365.25 e meses por 12; anos permanecem iguais. Classifique nos intervalos [0,19), [19,60) e [60,infinito), com rótulos '0-18', '19-59' e '60+'. Trata-se de conversão operacional aproximada. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: faixa,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | fail | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | fail | automatic | response.success |
| Equivalência estrita | fail | automatic | {"status": "technical_failure", "result_correct": false} |
| Quantidade de linhas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Quantidade de colunas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Unidade e agregação | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Dimensões e identificadores | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Informação principal | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Completude e escopo | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Formato da saída | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Fidelidade do texto | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |

### Q43 — correct

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Qual é o percentual de linhas com pelo menos um dos indicadores cardiopati, hematologi, hepatica, asma, diabetes, neurologic, pneumopati, imunodepre, renal ou obesidade igual a 1? Conte cada linha uma vez no numerador e use todas as linhas no denominador, inclusive valores nulos ou desconhecidos. Multiplique a razão por 100 e retorne nulo se não houver linhas. Retorne somente estas colunas, nesta ordem: percentual. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | OR entre os dez indicadores =1; total de linhas fica sem filtros. Fonte: results[id=43].response e cases[id=43] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT de linhas que satisfazem OR, não soma contagens sobrepostas; razão *100 e proteção de zero. Fonte: results[id=43].response e cases[id=43] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['percentual'] representa as entidades e medidas solicitadas. Fonte: results[id=43].response e cases[id=43] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=43].response e cases[id=43] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=43].response e cases[id=43] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['percentual'], na ordem solicitada ['percentual']; representação compatível com o protocolo. Fonte: results[id=43].response e cases[id=43] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=43].response e cases[id=43] do pacote de referência vinculado. |

### Q44 — correct

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Quantas linhas têm pcr_sars2 = 1 ou pos_pcrflu = 1? Conte uma linha apenas uma vez, mesmo quando os dois indicadores forem iguais a 1. Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | pcr_sars2=1 OR pos_pcrflu=1 está explícito. Fonte: results[id=44].response e cases[id=44] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | countIf do OR conta cada linha uma vez, mesmo com ambos positivos. Fonte: results[id=44].response e cases[id=44] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['total'] representa as entidades e medidas solicitadas. Fonte: results[id=44].response e cases[id=44] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=44].response e cases[id=44] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=44].response e cases[id=44] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['total'], na ordem solicitada ['total']; representação compatível com o protocolo. Fonte: results[id=44].response e cases[id=44] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=44].response e cases[id=44] do pacote de referência vinculado. |

### Q45 — correct

Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. Entre pcr_sars2, pos_pcrflu e pcr_vsr, qual indicador tem a maior contagem de linhas com valor 1? Compare os três indicadores, inclusive os que tenham contagem zero; uma linha pode contribuir para mais de um indicador. Retorne o nome do indicador e sua contagem. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: agente,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["surtos-srag"], "actual": ["surtos-srag"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Cada ramo testa um dos três indicadores =1. Fonte: results[id=45].response e cases[id=45] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | UNION ALL de contagens escalares inclui zero e seleciona MAX com empates; rótulos em maiúsculas são aceitos pelo casefold do protocolo. Fonte: results[id=45].response e cases[id=45] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | POS_PCRFLU identifica o mesmo indicador de pos_pcrflu; o protocolo da Q45 admite normalização casefold. Não se interpretou como outro agente. Fonte: results[id=45].response e cases[id=45] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=45].response e cases[id=45] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=45].response e cases[id=45] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['agente', 'total'], na ordem solicitada ['agente', 'total']; representação compatível com o protocolo. Fonte: results[id=45].response e cases[id=45] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=45].response e cases[id=45] do pacote de referência vinculado. |

### Q46 — correct

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Qual é a soma de LEITOS_EXISTENTES em todas as linhas dessa competência? Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | COMP=(SELECT MAX(COMP) FROM leitos) aplica última competência global. Fonte: results[id=46].response e cases[id=46] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | SUM LEITOS_EXISTENTES soma estoque cadastrado, não linhas/vagas livres. Fonte: results[id=46].response e cases[id=46] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['total'] representa as entidades e medidas solicitadas. Fonte: results[id=46].response e cases[id=46] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=46].response e cases[id=46] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=46].response e cases[id=46] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['total'], na ordem solicitada ['total']; representação compatível com o protocolo. Fonte: results[id=46].response e cases[id=46] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=46].response e cases[id=46] do pacote de referência vinculado. |

### Q47 — correct

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Qual é a soma de LEITOS_SUS em todas as linhas dessa competência? Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Última COMP global sem filtro adicional. Fonte: results[id=47].response e cases[id=47] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | SUM LEITOS_SUS corresponde ao total solicitado. Fonte: results[id=47].response e cases[id=47] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['total'] representa as entidades e medidas solicitadas. Fonte: results[id=47].response e cases[id=47] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=47].response e cases[id=47] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=47].response e cases[id=47] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['total'], na ordem solicitada ['total']; representação compatível com o protocolo. Fonte: results[id=47].response e cases[id=47] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=47].response e cases[id=47] do pacote de referência vinculado. |

### Q48 — correct

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Qual é o percentual da soma de LEITOS_SUS sobre a soma de LEITOS_EXISTENTES nessa competência? Divida as somas, multiplique por 100 e retorne nulo se o denominador for zero. Retorne somente estas colunas, nesta ordem: percentual. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Última COMP global aplicada às duas somas. Fonte: results[id=48].response e cases[id=48] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | 100*SUM(LEITOS_SUS)/NULLIF(SUM(LEITOS_EXISTENTES),0), razão de somas e não média de percentuais. Fonte: results[id=48].response e cases[id=48] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['percentual'] representa as entidades e medidas solicitadas. Fonte: results[id=48].response e cases[id=48] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=48].response e cases[id=48] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=48].response e cases[id=48] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['percentual'], na ordem solicitada ['percentual']; representação compatível com o protocolo. Fonte: results[id=48].response e cases[id=48] do pacote de referência vinculado. |
| Fidelidade do texto | fail | ai_assisted | O valor 67,65% confere, porém a frase “há um uso de 67,65%” infere utilização/ocupação a partir da composição SUS do estoque cadastrado. A consulta não mede uso nem vagas livres. Fonte: results[id=48].response e cases[id=48] do pacote de referência vinculado. |

### Q49 — technical_failure

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Qual UF não nula e diferente da string vazia tem a maior soma de LEITOS_EXISTENTES? Considere todas as UFs presentes nessa competência, inclusive aquelas com soma zero. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: uf,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | fail | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | fail | automatic | response.success |
| Equivalência estrita | fail | automatic | {"status": "technical_failure", "result_correct": false} |
| Quantidade de linhas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Quantidade de colunas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Unidade e agregação | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Dimensões e identificadores | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Informação principal | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Completude e escopo | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Formato da saída | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Fidelidade do texto | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |

### Q50 — correct

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Qual é a soma de LEITOS_EXISTENTES por UF não nula e diferente da string vazia? Inclua todas as UFs presentes nessa competência, inclusive aquelas com soma zero. Retorne somente estas colunas, nesta ordem: uf,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 27, "actual_row_count": 27} |
| Quantidade de linhas | pass | automatic | {"expected": 27, "actual": 27} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | fail | ai_assisted | Última COMP global presente, mas falta excluir UF nula/vazia. A coincidência eventual dos resultados não implementa o filtro ausente. Fonte: results[id=50].response e cases[id=50] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | SUM LEITOS_EXISTENTES por UF, sem LIMIT ou exclusão de totais zero. Fonte: results[id=50].response e cases[id=50] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['UF', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=50].response e cases[id=50] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 27 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=50].response e cases[id=50] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (27 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=50].response e cases[id=50] do pacote de referência vinculado. |
| Formato da saída | partial | ai_assisted | Conteúdo, quantidade e ordem das colunas estão corretos, mas os nomes não seguem literalmente o pedido: recebido ['UF', 'total']; solicitado ['uf', 'total']. A métrica estrita de valores não verifica esses aliases. Fonte: results[id=50].response e cases[id=50] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=50].response e cases[id=50] do pacote de referência vinculado. |

### Q51 — correct

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Qual é a soma de UTI_TOTAL_EXIST em todas as linhas dessa competência? Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Última COMP global aplicada. Fonte: results[id=51].response e cases[id=51] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | SUM UTI_TOTAL_EXIST corresponde ao estoque de UTI solicitado. Fonte: results[id=51].response e cases[id=51] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['total'] representa as entidades e medidas solicitadas. Fonte: results[id=51].response e cases[id=51] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=51].response e cases[id=51] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=51].response e cases[id=51] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['total'], na ordem solicitada ['total']; representação compatível com o protocolo. Fonte: results[id=51].response e cases[id=51] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=51].response e cases[id=51] do pacote de referência vinculado. |

### Q52 — correct

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Qual é o percentual da soma de UTI_TOTAL_EXIST sobre a soma de LEITOS_EXISTENTES nessa competência? Divida as somas, multiplique por 100 e retorne nulo se o denominador for zero. Retorne somente estas colunas, nesta ordem: percentual. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Última COMP global aplicada. Fonte: results[id=52].response e cases[id=52] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | 100*SUM(UTI_TOTAL_EXIST)/NULLIF(SUM(LEITOS_EXISTENTES),0) calcula composição percentual do estoque. Fonte: results[id=52].response e cases[id=52] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['percentual'] representa as entidades e medidas solicitadas. Fonte: results[id=52].response e cases[id=52] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=52].response e cases[id=52] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=52].response e cases[id=52] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['percentual'], na ordem solicitada ['percentual']; representação compatível com o protocolo. Fonte: results[id=52].response e cases[id=52] do pacote de referência vinculado. |
| Fidelidade do texto | fail | ai_assisted | 12,29% está correto, mas o texto o converte em “12,29 leitos de UTI por cada leito geral”: erro de escala por fator 100. O denominador é todo o estoque existente, não somente leitos gerais. Fonte: results[id=52].response e cases[id=52] do pacote de referência vinculado. |

### Q53 — correct

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Qual categoria DS_TIPO_UNIDADE não nula e diferente da string vazia tem a maior soma de LEITOS_EXISTENTES? Preserve a categoria como armazenada. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: tipo,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Última COMP global e tipo não vazio/nulo tanto na consulta principal como na subconsulta. Fonte: results[id=53].response e cases[id=53] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | SUM por tipo; HAVING compara com máximo dos totais agrupados, incluindo empates. Fonte: results[id=53].response e cases[id=53] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['tipo', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=53].response e cases[id=53] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=53].response e cases[id=53] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=53].response e cases[id=53] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['tipo', 'total'], na ordem solicitada ['tipo', 'total']; representação compatível com o protocolo. Fonte: results[id=53].response e cases[id=53] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=53].response e cases[id=53] do pacote de referência vinculado. |

### Q54 — correct

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Quais são as somas de UTI_ADULTO_EXIST, UTI_PEDIATRICO_EXIST, UTI_NEONATAL_EXIST, UTI_CORONARIANA_EXIST e UTI_QUEIMADO_EXIST? Retorne uma única linha, nessa ordem; não some competências diferentes. Retorne somente estas colunas, nesta ordem: UTI_ADULTO_EXIST,UTI_PEDIATRICO_EXIST,UTI_NEONATAL_EXIST,UTI_CORONARIANA_EXIST,UTI_QUEIMADO_EXIST. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 5, "actual_widths": [5]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Última COMP global aplicada às cinco somas. Fonte: results[id=54].response e cases[id=54] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | Somas dos cinco tipos de UTI em uma única linha e ordem solicitada. Fonte: results[id=54].response e cases[id=54] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['UTI_ADULTO_EXIST', 'UTI_PEDIATRICO_EXIST', 'UTI_NEONATAL_EXIST', 'UTI_CORONARIANA_EXIST', 'UTI_QUEIMADO_EXIST'] representa as entidades e medidas solicitadas. Fonte: results[id=54].response e cases[id=54] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=54].response e cases[id=54] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=54].response e cases[id=54] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['UTI_ADULTO_EXIST', 'UTI_PEDIATRICO_EXIST', 'UTI_NEONATAL_EXIST', 'UTI_CORONARIANA_EXIST', 'UTI_QUEIMADO_EXIST'], na ordem solicitada ['UTI_ADULTO_EXIST', 'UTI_PEDIATRICO_EXIST', 'UTI_NEONATAL_EXIST', 'UTI_CORONARIANA_EXIST', 'UTI_QUEIMADO_EXIST']; representação compatível com o protocolo. Fonte: results[id=54].response e cases[id=54] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=54].response e cases[id=54] do pacote de referência vinculado. |

### Q55 — technical_failure

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Qual UF não nula e diferente da string vazia tem a menor soma de UTI_NEONATAL_EXIST? Inclua UFs presentes com soma zero, mas não acrescente UFs ausentes dessa competência. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: uf,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | fail | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | fail | automatic | response.success |
| Equivalência estrita | fail | automatic | {"status": "technical_failure", "result_correct": false} |
| Quantidade de linhas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Quantidade de colunas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Unidade e agregação | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Dimensões e identificadores | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Informação principal | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Completude e escopo | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Formato da saída | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Fidelidade do texto | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |

### Q56 — correct

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Qual código TP_GESTAO não nulo e diferente da string vazia reúne a maior quantidade de CNES distintos não nulos e diferentes da string vazia? Retorne o código de gestão, sem interpretá-lo como natureza jurídica pública, privada ou filantrópica. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: gestao,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 2, "actual_widths": [2]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Última COMP global, TP_GESTAO e CNES não nulos/vazios em ambas as agregações. Fonte: results[id=56].response e cases[id=56] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT DISTINCT CNES por gestão; HAVING com máximo dos totais preserva empates e não infere natureza jurídica. Fonte: results[id=56].response e cases[id=56] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['TP_GESTAO', 'total'] representa as entidades e medidas solicitadas. Fonte: results[id=56].response e cases[id=56] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=56].response e cases[id=56] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=56].response e cases[id=56] do pacote de referência vinculado. |
| Formato da saída | partial | ai_assisted | Conteúdo, quantidade e ordem das colunas estão corretos, mas os nomes não seguem literalmente o pedido: recebido ['TP_GESTAO', 'total']; solicitado ['gestao', 'total']. A métrica estrita de valores não verifica esses aliases. Fonte: results[id=56].response e cases[id=56] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=56].response e cases[id=56] do pacote de referência vinculado. |

### Q57 — correct

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Qual é a soma de LEITOS_SUS nas linhas em que NATUREZA_JURIDICA, após remover espaços nas extremidades, começa com '2' ou '3'? Esse é um filtro por código; não substitua por TP_GESTAO nem infira classificação jurídica além dos códigos especificados. Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1, "actual_row_count": 1} |
| Quantidade de linhas | pass | automatic | {"expected": 1, "actual": 1} |
| Quantidade de colunas | pass | automatic | {"expected": 1, "actual_widths": [1]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | Última COMP global e alternativas TRIM(NATUREZA_JURIDICA) LIKE 2%/3% agrupadas; não usa TP_GESTAO. Fonte: results[id=57].response e cases[id=57] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | SUM LEITOS_SUS nas linhas elegíveis, sem multiplicação por JOIN. Fonte: results[id=57].response e cases[id=57] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['total'] representa as entidades e medidas solicitadas. Fonte: results[id=57].response e cases[id=57] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=57].response e cases[id=57] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=57].response e cases[id=57] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['total'], na ordem solicitada ['total']; representação compatível com o protocolo. Fonte: results[id=57].response e cases[id=57] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=57].response e cases[id=57] do pacote de referência vinculado. |

### Q58 — technical_failure

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Qual UF não nula e diferente da string vazia tem o maior percentual da soma de LEITOS_SUS sobre a soma de LEITOS_EXISTENTES? Considere somente UFs cuja soma de LEITOS_EXISTENTES seja positiva e multiplique a razão por 100. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: uf,percentual. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | fail | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | fail | automatic | response.success |
| Equivalência estrita | fail | automatic | {"status": "technical_failure", "result_correct": false} |
| Quantidade de linhas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Quantidade de colunas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Unidade e agregação | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Dimensões e identificadores | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Informação principal | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Completude e escopo | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Formato da saída | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Fidelidade do texto | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |

### Q59 — correct

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Para cada REGIAO não nula e diferente da string vazia, quais são as somas de LEITOS_EXISTENTES e LEITOS_SUS? Preserve os nomes das regiões e inclua todos os grupos presentes. Retorne somente estas colunas, nesta ordem: regiao,existentes,sus. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 5, "actual_row_count": 5} |
| Quantidade de linhas | pass | automatic | {"expected": 5, "actual": 5} |
| Quantidade de colunas | pass | automatic | {"expected": 3, "actual_widths": [3]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | fail | ai_assisted | Última COMP global presente, mas falta excluir REGIAO nula/vazia. A coincidência eventual dos resultados não implementa o filtro ausente. Fonte: results[id=59].response e cases[id=59] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | SUM existentes e SUS por REGIAO, com todos os grupos presentes. Fonte: results[id=59].response e cases[id=59] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['REGIAO', 'existentes', 'sus'] representa as entidades e medidas solicitadas. Fonte: results[id=59].response e cases[id=59] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 5 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=59].response e cases[id=59] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (5 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=59].response e cases[id=59] do pacote de referência vinculado. |
| Formato da saída | partial | ai_assisted | Conteúdo, quantidade e ordem das colunas estão corretos, mas os nomes não seguem literalmente o pedido: recebido ['REGIAO', 'existentes', 'sus']; solicitado ['regiao', 'existentes', 'sus']. A métrica estrita de valores não verifica esses aliases. Fonte: results[id=59].response e cases[id=59] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=59].response e cases[id=59] do pacote de referência vinculado. |

### Q60 — technical_failure

Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. Qual combinação de UF e código municipal CO_IBGE tem a maior soma de LEITOS_EXISTENTES? Exclua UF ou código municipal nulo ou igual à string vazia. Identifique o município pelo código acompanhado da UF. Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia. Retorne somente estas colunas, nesta ordem: uf,municipio,total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos"], "actual": ["leitos"], "tp": 1, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | fail | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | fail | automatic | response.success |
| Equivalência estrita | fail | automatic | {"status": "technical_failure", "result_correct": false} |
| Quantidade de linhas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Quantidade de colunas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Unidade e agregação | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Dimensões e identificadores | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Informação principal | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Completude e escopo | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Formato da saída | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Fidelidade do texto | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |

### Q61 — technical_failure

Considere todas as linhas de SRAG e o cadastro de UBS carregados, sem recorte temporal adicional e sem filtro de classificação final da SRAG. Quantos códigos municipais positivos distintos aparecem simultaneamente em co_mun_not da SRAG e em ibge de UBS com CNES positivo? Use a igualdade de códigos prevista no relacionamento cadastrado. Conte municípios, não notificações ou UBS; não use município de residência. Retorne somente estas colunas, nesta ordem: total. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica", "surtos-srag"], "actual": ["atencao-basica", "surtos-srag"], "tp": 2, "fp": 0, "fn": 0} |
| Seleção de relações | pass | automatic | {"expected": ["srag_ubs_municipio_notificacao"], "actual": ["srag_ubs_municipio_notificacao"], "tp": 1, "fp": 0, "fn": 0} |
| SQL aprovado | fail | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | fail | automatic | response.success |
| Equivalência estrita | fail | automatic | {"status": "technical_failure", "result_correct": false} |
| Quantidade de linhas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Quantidade de colunas | not_assessable | automatic | Não há tabela final executada com sucesso. |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Unidade e agregação | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Dimensões e identificadores | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Informação principal | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Completude e escopo | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Formato da saída | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |
| Fidelidade do texto | not_assessable | review | Não há resposta analítica final; falha contabilizada nas dimensões operacionais. |

### Q62 — correct

Considere todas as linhas de SRAG, sem filtro de classificação final, e o cadastro de UBS carregados, sem recorte temporal adicional. Para cada código municipal positivo presente tanto em co_mun_not da SRAG quanto em ibge de UBS com CNES positivo, retorne a contagem de linhas de notificações e a contagem de CNES distintos positivos. Agregue cada base antes de combinar pela igualdade dos códigos. Liste todos os municípios comuns, sem top N; ordene por notificações decrescentes e código municipal crescente. Retorne somente estas colunas, nesta ordem: municipio,notificacoes,ubs.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica", "surtos-srag"], "actual": ["atencao-basica", "surtos-srag"], "tp": 2, "fp": 0, "fn": 0} |
| Seleção de relações | pass | automatic | {"expected": ["srag_ubs_municipio_notificacao"], "actual": ["srag_ubs_municipio_notificacao"], "tp": 1, "fp": 0, "fn": 0} |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 1198, "actual_row_count": 1198} |
| Quantidade de linhas | pass | automatic | {"expected": 1198, "actual": 1198} |
| Quantidade de colunas | pass | automatic | {"expected": 3, "actual_widths": [3]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | CNES positivo na UBS e município positivo na SRAG; INNER JOIN por igualdade com co_mun_not > 0 exclui também ibge não positivo, mesmo sem repetir esse filtro na CTE UBS. Fonte: results[id=62].response e cases[id=62] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | Pré-agregações independentes: COUNT SRAG e COUNT DISTINCT CNES; INNER JOIN por município evita multiplicar notificações; ordenação pedida presente. Fonte: results[id=62].response e cases[id=62] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['municipio', 'notificacoes', 'ubs'] representa as entidades e medidas solicitadas. Fonte: results[id=62].response e cases[id=62] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 1198 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=62].response e cases[id=62] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (1198 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=62].response e cases[id=62] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['municipio', 'notificacoes', 'ubs'], na ordem solicitada ['municipio', 'notificacoes', 'ubs']; representação compatível com o protocolo. Fonte: results[id=62].response e cases[id=62] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=62].response e cases[id=62] do pacote de referência vinculado. |

### Q63 — correct

Considere todos os registros de vacinação carregados, agrupados por UF de residência, e as linhas de leitos da maior competência COMP global disponível. Para cada sigla de UF não nula e diferente da string vazia presente nas duas bases, retorne a contagem de registros de vacinação e a soma de UTI_TOTAL_EXIST. Inclua somente UFs cuja soma de UTI seja positiva. Agregue as bases separadamente antes de combinar pela sigla de UF. É uma comparação descritiva entre o acumulado de registros e o estoque cadastrado mais recente, não cobertura vacinal, ocupação ou comparação de períodos equivalentes. Retorne somente estas colunas, nesta ordem: uf,doses,leitos. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao", "leitos"], "actual": ["covid-19-vacinacao", "leitos"], "tp": 2, "fp": 0, "fn": 0} |
| Seleção de relações | pass | automatic | {"expected": ["vacinacao_leitos_uf"], "actual": ["vacinacao_leitos_uf"], "tp": 1, "fp": 0, "fn": 0} |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 27, "actual_row_count": 27} |
| Quantidade de linhas | pass | automatic | {"expected": 27, "actual": 27} |
| Quantidade de colunas | pass | automatic | {"expected": 3, "actual_widths": [3]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | UFs não vazias/nulas nas duas bases; maior COMP global; filtro leitos>0 depois da soma é equivalente a HAVING. Fonte: results[id=63].response e cases[id=63] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT vacinação por residência e SUM UTI por UF em CTEs separadas; JOIN de agregados, sem multiplicação. Fonte: results[id=63].response e cases[id=63] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['uf', 'doses', 'leitos'] representa as entidades e medidas solicitadas. Fonte: results[id=63].response e cases[id=63] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 27 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=63].response e cases[id=63] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (27 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=63].response e cases[id=63] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['uf', 'doses', 'leitos'], na ordem solicitada ['uf', 'doses', 'leitos']; representação compatível com o protocolo. Fonte: results[id=63].response e cases[id=63] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=63].response e cases[id=63] do pacote de referência vinculado. |

### Q64 — correct

Considere todos os registros de vacinação carregados, agrupados por UF de residência, e as linhas de leitos da maior competência COMP global disponível. Para cada sigla de UF não nula e diferente da string vazia presente nas duas bases, retorne a contagem de registros de vacinação e a soma de UTI_TOTAL_EXIST. Inclua somente UFs cuja soma de UTI seja positiva. Agregue as bases separadamente antes de combinar pela sigla de UF. É uma comparação descritiva entre o acumulado de registros e o estoque cadastrado mais recente, não cobertura vacinal, ocupação ou comparação de períodos equivalentes. Retorne somente estas colunas, nesta ordem: uf,doses,leitos. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["covid-19-vacinacao", "leitos"], "actual": ["covid-19-vacinacao", "leitos"], "tp": 2, "fp": 0, "fn": 0} |
| Seleção de relações | pass | automatic | {"expected": ["vacinacao_leitos_uf"], "actual": ["vacinacao_leitos_uf"], "tp": 1, "fp": 0, "fn": 0} |
| SQL aprovado | pass | automatic | SQL final e validation.valid registrados. |
| Sucesso operacional | pass | automatic | response.success |
| Equivalência estrita | pass | automatic | {"status": "correct", "result_correct": true, "mismatch_reasons": [], "expected_row_count": 27, "actual_row_count": 27} |
| Quantidade de linhas | pass | automatic | {"expected": 27, "actual": 27} |
| Quantidade de colunas | pass | automatic | {"expected": 3, "actual_widths": [3]} |
| Limitação prevista | not_applicable | automatic | Não é uma limitação prevista. |
| Filtros | pass | ai_assisted | UFs não vazias/nulas nas duas bases; maior COMP global; filtro leitos>0 depois da soma é equivalente a HAVING. Fonte: results[id=64].response e cases[id=64] do pacote de referência vinculado. |
| Unidade e agregação | pass | ai_assisted | COUNT vacinação por residência e SUM UTI por UF em CTEs separadas; JOIN de agregados, sem multiplicação. Fonte: results[id=64].response e cases[id=64] do pacote de referência vinculado. |
| Dimensões e identificadores | pass | ai_assisted | Campos selecionados e unidade inspecionados no SQL; saída ['uf', 'doses', 'leitos'] representa as entidades e medidas solicitadas. Fonte: results[id=64].response e cases[id=64] do pacote de referência vinculado. |
| Informação principal | pass | ai_assisted | Conteúdo central da tabela conferido contra a referência no snapshot: 27 linha(s). A classificação não aprova automaticamente os filtros ou o texto. Fonte: results[id=64].response e cases[id=64] do pacote de referência vinculado. |
| Completude e escopo | pass | ai_assisted | A tabela contém os grupos e medidas solicitados no snapshot (27 linha(s)); não há LIMIT indevido. A inspeção de seleção/empates consta na análise de agregação. Fonte: results[id=64].response e cases[id=64] do pacote de referência vinculado. |
| Formato da saída | pass | ai_assisted | Colunas retornadas ['uf', 'doses', 'leitos'], na ordem solicitada ['uf', 'doses', 'leitos']; representação compatível com o protocolo. Fonte: results[id=64].response e cases[id=64] do pacote de referência vinculado. |
| Fidelidade do texto | pass | ai_assisted | Explicação e resumo conferidos com a tabela: números e destaque são compatíveis, sem afirmação adicional incompatível identificada. Resumo de destaques é aceito quando a tabela completa acompanha a resposta. Fonte: results[id=64].response e cases[id=64] do pacote de referência vinculado. |

### Q65 — expected_limitation

Na base SRAG carregada, conte todas as linhas por UF de notificação sg_uf_not não nula e não vazia, em todo o período disponível e sem filtro de classificação final. Selecione somente as UFs com a contagem máxima global, incluindo todas as empatadas. Para cada uma, retorne a contagem de notificações e a soma de UTI_TOTAL_SUS na maior competência COMP global da base de leitos, identificando também essa competência. Agregue as bases separadamente e combine pela sigla de UF usando correspondência validada. Se uma UF selecionada não tiver registros de leitos nessa competência, mantenha a UF e indique ausência de informação, sem atribuir zero. A comparação é descritiva: acumulado de notificações versus estoque cadastrado recente, não vagas livres nem oferta na época das notificações. Retorne somente estas colunas, nesta ordem: uf,notificacoes,uti_sus,competencia. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos", "surtos-srag"], "actual": ["leitos", "surtos-srag"], "tp": 2, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | not_applicable | automatic | Caso sem referência analítica. |
| Sucesso operacional | not_applicable | automatic | Caso sem referência analítica. |
| Equivalência estrita | not_applicable | automatic | Caso sem referência analítica. |
| Quantidade de linhas | not_applicable | automatic | Caso sem referência analítica. |
| Quantidade de colunas | not_applicable | automatic | Caso sem referência analítica. |
| Limitação prevista | pass | automatic | {"status": "expected_limitation", "result_correct": null, "limitation_correct": true} |
| Filtros | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Unidade e agregação | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Dimensões e identificadores | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Informação principal | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Completude e escopo | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Formato da saída | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Fidelidade do texto | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |

### Q66 — expected_limitation

Na base SRAG carregada, conte as linhas com hospital = 1 por UF de notificação sg_uf_not não nula e não vazia, em todo o período disponível e sem filtro de classificação final. Selecione somente as UFs com a maior contagem, incluindo todos os empates; se não houver linhas elegíveis, retorne lista vazia. Essa contagem representa notificações com hospitalização indicada, não internações únicas. Para cada UF selecionada, retorne essa contagem, a soma de LEITOS_EXISTENTES na maior competência COMP global da base de leitos e a competência. Agregue antes de combinar por correspondência validada de sigla de UF; mantenha UFs sem dados de leitos com informação ausente, não zero. Compare acumulado de notificações com estoque cadastrado recente, sem inferir capacidade disponível na data da hospitalização. Retorne somente estas colunas, nesta ordem: uf,notificacoes_hospitalizadas,leitos_existentes,competencia. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["leitos", "surtos-srag"], "actual": ["leitos", "surtos-srag"], "tp": 2, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | not_applicable | automatic | Caso sem referência analítica. |
| Sucesso operacional | not_applicable | automatic | Caso sem referência analítica. |
| Equivalência estrita | not_applicable | automatic | Caso sem referência analítica. |
| Quantidade de linhas | not_applicable | automatic | Caso sem referência analítica. |
| Quantidade de colunas | not_applicable | automatic | Caso sem referência analítica. |
| Limitação prevista | pass | automatic | {"status": "expected_limitation", "result_correct": null, "limitation_correct": true} |
| Filtros | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Unidade e agregação | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Dimensões e identificadores | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Informação principal | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Completude e escopo | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Formato da saída | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Fidelidade do texto | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |

### Q67 — expected_limitation

Considere o cadastro de UBS e todos os registros de vacinação contra COVID-19 carregados, sem recorte temporal adicional. Para cada UF comum às duas bases, conte CNES distintos positivos das UBS e registros de vacinação por UF de residência. Use correspondência validada entre o código de UF das UBS e a sigla de UF da vacinação; exclua UFs não identificáveis. Agregue antes de combinar. Retorne os dois totais e a razão registros de vacinação por UBS, com pelo menos seis casas decimais; considere somente UFs com pelo menos uma UBS. A razão é descritiva, não mede cobertura, produtividade ou doses aplicadas pelas próprias UBS e não solicita correlação estatística. Retorne somente estas colunas, nesta ordem: uf,ubs,registros_vacinacao,registros_por_ubs. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica", "covid-19-vacinacao"], "actual": ["atencao-basica", "covid-19-vacinacao"], "tp": 2, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | not_applicable | automatic | Caso sem referência analítica. |
| Sucesso operacional | not_applicable | automatic | Caso sem referência analítica. |
| Equivalência estrita | not_applicable | automatic | Caso sem referência analítica. |
| Quantidade de linhas | not_applicable | automatic | Caso sem referência analítica. |
| Quantidade de colunas | not_applicable | automatic | Caso sem referência analítica. |
| Limitação prevista | pass | automatic | {"status": "expected_limitation", "result_correct": null, "limitation_correct": true} |
| Filtros | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Unidade e agregação | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Dimensões e identificadores | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Informação principal | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Completude e escopo | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Formato da saída | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Fidelidade do texto | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |

### Q68 — expected_limitation

Considere todas as linhas de SRAG carregadas, sem filtro de classificação final, o cadastro de UBS carregado e os leitos da maior competência COMP global disponível. Use município de notificação co_mun_not na SRAG e correspondência municipal validada com ibge das UBS e CO_IBGE dos leitos. Agregue separadamente: contagem de linhas de SRAG, CNES distintos positivos das UBS e soma de LEITOS_EXISTENTES. O universo de comparação contém somente municípios identificáveis presentes nas três bases, com pelo menos uma UBS e total de leitos conhecido. Inclua total de leitos zero quando registrado; exclua ausência de informação, sem convertê-la em zero. Defina alto número de notificações como contagem estritamente acima da mediana das contagens desse universo e baixa oferta de leitos como soma estritamente abaixo da mediana dos totais de leitos do mesmo universo. Calcule ambas as medianas antes da seleção; com número par de municípios, use a média dos dois valores centrais. Retorne todos os municípios que cumpram simultaneamente os dois cortes, com código municipal harmonizado, notificações, UBS, leitos e competência; se nenhum cumprir, retorne lista vazia. São contagens absolutas, não taxas populacionais; a comparação do acumulado com estoque recente não representa vagas livres nem equivalência temporal. Retorne somente estas colunas, nesta ordem: municipio,notificacoes,ubs,leitos_existentes,competencia. A ordem das linhas é livre.

| Dimensão | Classificação | Método | Evidência |
|---|---|---|---|
| Seleção de bases | pass | automatic | {"expected": ["atencao-basica", "leitos", "surtos-srag"], "actual": ["atencao-basica", "leitos", "surtos-srag"], "tp": 3, "fp": 0, "fn": 0} |
| Seleção de relações | not_applicable | automatic | Sem conjunto positivo esperado para esta dimensão. |
| SQL aprovado | not_applicable | automatic | Caso sem referência analítica. |
| Sucesso operacional | not_applicable | automatic | Caso sem referência analítica. |
| Equivalência estrita | not_applicable | automatic | Caso sem referência analítica. |
| Quantidade de linhas | not_applicable | automatic | Caso sem referência analítica. |
| Quantidade de colunas | not_applicable | automatic | Caso sem referência analítica. |
| Limitação prevista | pass | automatic | {"status": "expected_limitation", "result_correct": null, "limitation_correct": true} |
| Filtros | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Unidade e agregação | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Dimensões e identificadores | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Informação principal | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Completude e escopo | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Formato da saída | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
| Fidelidade do texto | not_applicable | review | Rubrica qualitativa restrita às respostas analíticas. |
