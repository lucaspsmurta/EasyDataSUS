# Referência assistida — Q12, Q65 e Q68

Revisão provisória por Codex. Requer validação humana antes de uso como referência independente.

- Referência assistida por IA, não revisão humana independente.
- Casos escolhidos após observar falhas; não são amostra independente nem permitem estimar acurácia geral.
- Apenas pergunta, contexto e metadados congelados; sem gabaritos SQL, execução ou comprovação de cobertura.
- Suporte parcial é a convenção quando componentes existem mas falta integração cadastrada; not_assessable é alternativa discutível que exige decisão humana.
- Disponibilidade considera medidas brutas viáveis nos metadados, separando ambiguidade de formulação; não valida toda interpretação possível.

## Q12

Qual fabricante não vazio tem mais registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: fabricante,total.

- **context_completeness: pass** — A consulta irrestrita ao conjunto de vacinação é suficiente para este agregado. Não há necessidade demonstrada de impor período ou local. Esta é uma convenção da rubrica, não um contexto literalmente declarado.
- **analytical_specificity: pass** — A unidade contada é o registro de vacinação; fabricante é o agrupamento. Há filtro de fabricante não vazio, máximo, todos os empates e ordem de colunas explícitos.
- **unambiguity: pass** — A comparação pelo máximo e o tratamento de empates estão explícitos. Não se identificou ambiguidade central que altere a operação solicitada.
- **data_availability: pass** — vacina_fabricante_nome permite filtrar e agrupar; o total é COUNT dos registros. Não é necessário um campo total nem dados de município ou período.
- **implementation_support: pass** — A operação usa uma única base de vacinação; não requer relacionamento cadastrado. Suporte de metadados não comprova execução nem cobertura real.

## Q65

Qual é a quantidade de leitos de UTI SUS nos estados com maior número de notificações de SRAG?

- **context_completeness: partial** — Falta alinhar período das notificações com competência do estoque de leitos. Estados já define a granularidade; não é necessário exigir um estado específico.
- **analytical_specificity: partial** — Medida de UTI SUS e agrupamento por estado estão definidos, mas falta delimitar quais posições ou corte compõem os estados com maior número.
- **unambiguity: fail** — Maior número pode selecionar somente o máximo com empates ou os cinco primeiros estados. Município/UF de notificação e de residência também não são equivalentes. As escolhas mudam o resultado.
- **data_availability: pass** — NU_NOTIFIC e SG_UF_NOT permitem contar notificações por UF; UTI_TOTAL_SUS e UF permitem agregar leitos. COMP identifica competência. A nota considera medidas brutas, sem comprovar cobertura histórica.
- **implementation_support: partial** — Os componentes têm campos, mas o inventário não registra integração SRAG–leitos. Suporte parcial não significa impossibilidade de SQL. Seria necessário validar chaves, competências e agregação antes da combinação.

## Q68

Quais municípios combinam alto número de notificações de SRAG, UBS cadastradas e baixa disponibilidade de leitos?

- **context_completeness: partial** — Municípios define a granularidade. Falta período das notificações e referência temporal dos estoques/cadastros para tornar a comparação interpretável.
- **analytical_specificity: partial** — Há entidades e medidas identificáveis, mas alto/baixa não definem cortes e disponibilidade de leitos não especifica tipo ou unidade de comparação.
- **unambiguity: fail** — Alto pode significar maior contagem absoluta ou taxa; baixa pode significar poucos leitos totais ou por habitante. Faltam critérios para escolher interpretações que produzem seleções distintas.
- **data_availability: pass** — Há campos para contagens brutas de notificações e UBS, quantidades de leitos e códigos municipais. Esta nota não presume taxa por habitante: tal interpretação precisaria de denominador adicional e nova análise.
- **implementation_support: partial** — SRAG–UBS tem relação municipal cadastrada com pré-agregação obrigatória. Falta ponte cadastrada com leitos; é preciso validar códigos e competência. A ausência não demonstra impossibilidade técnica.

## Auditoria das justificativas do relatório v5.1

Mesmo nas cinco concordâncias de rótulos, a justificativa precisa de revisão. Em Q12, especificidade confunde fabricante (agrupamento) com registro (unidade contada). Em Q65, contexto exige local sem justificar por que um estado específico seria necessário. Em Q68, disponibilidade não cita a quantidade de leitos necessária; ausência de evidência contrária não substitui evidência positiva.

As aprovações de ausência de ambiguidade em Q65 e Q68 são os erros mais relevantes: deixam passar critérios que alteram a seleção. As quatro pendências representam ausência de julgamento válido, não reprovação das perguntas.

Próximo passo: validar estas convenções com uma pessoa revisora e então calibrar o avaliador. Não executar nova rodada extensa apenas para repetir os mesmos erros. A comparação automática abaixo mede somente rótulos.
