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
| Filtros | 64 | 0 | 0 | 0 | 0 | 56 | 8 | — | 0.00% |
| Unidade e agregação | 64 | 0 | 0 | 0 | 0 | 56 | 8 | — | 0.00% |
| Dimensões e identificadores | 64 | 0 | 0 | 0 | 0 | 56 | 8 | — | 0.00% |
| Informação principal | 64 | 0 | 0 | 0 | 0 | 56 | 8 | — | 0.00% |
| Completude e escopo | 64 | 0 | 0 | 0 | 0 | 56 | 8 | — | 0.00% |
| Formato da saída | 64 | 0 | 0 | 0 | 0 | 56 | 8 | — | 0.00% |
| Fidelidade do texto | 64 | 0 | 0 | 0 | 0 | 56 | 8 | — | 0.00% |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
| Filtros | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Unidade e agregação | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Dimensões e identificadores | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Informação principal | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Completude e escopo | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Formato da saída | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |
| Fidelidade do texto | pending | review | Exige inspeção da pergunta, referência e resposta; não inferido da equivalência. |

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
