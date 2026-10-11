# Diagnóstico isolado de qualidade das perguntas

Não é avaliação oficial. Seleção de campos herdada do mapeamento v6; sem gabaritos nas entradas.
Resultados estruturalmente válidos ainda exigem inspeção semântica. Sem retomada automática de falhas.
Modelo: qwen2.5-coder:7b. Tempo: 277.1s.

## 12 — formulation

Tempo: 53.19s; erro: nenhum.

- context_completeness: **fail** — Falta contexto NECESSÁRIO. A consulta não especifica a fonte dos dados de vacinação.
- analytical_specificity: **partial** — A unidade contada (fabricante) e a medida (total de registros) estão definidos, mas não há especificação sobre o período ou local.
- unambiguity: **pass** — Não há duas interpretações plausíveis com resultados diferentes.

## 12 — support

Tempo: 45.81s; erro: nenhum.

- data_availability: **partial** — A seleção de campos é parcial e não inclui a coluna 'total' necessária para contar registros de vacinação por fabricante.
- implementation_support: **fail** — A relação 'vacinacao_leitos_uf' não é relevante para contar registros de vacinação por fabricante. A relação 'srag_ubs_municipio_notificacao' também não é relevante para esta consulta.

## 65 — formulation

Tempo: 25.09s; erro: nenhum.

- context_completeness: **fail** — Falta contexto necessário. É necessário informações sobre os estados, a quantidade de leitos de UTI SUS e os dados de notificações de SRAG.
- analytical_specificity: **not_assessable** — Não há informações suficientes para avaliar a especificidade analítica.
- unambiguity: **not_assessable** — Não há informações suficientes para avaliar a ambiguidade.

## 65 — support

Tempo: 36.91s; erro: nenhum.

- data_availability: **partial** — COUNT não pode ser usado para medir leitos. SUM precisa de campo quantitativo. Geocódigo agrupa, não mede leitos. Não presuma taxa per capita.
- implementation_support: **partial** — A relação 'srag_ubs_municipio_notificacao' não permite combinar os componentes necessários para obter a quantidade de leitos de UTI SUS nos estados com maior número de notificações de SRAG.

## 68 — formulation

Tempo: 27.62s; erro: nenhum.

- context_completeness: **fail** — Falta contexto NECESSÁRIO. Consulta irrestrita a uma base não exige período/local automaticamente.
- analytical_specificity: **partial** — Unidade contada e medida estão definidos, mas agrupamento e seleção não estão claramente definidos.
- unambiguity: **partial** — Há duas interpretações plausíveis com resultados diferentes. Uma interpretação considera todos os municípios, enquanto a outra considera apenas os que combinam todos os critérios.

## 68 — support

Tempo: 42.81s; erro: nenhum.

- data_availability: **partial** — A base de leitos não permite medir leitos disponíveis, apenas o código IBGE do município. A base de SRAG permite obter o número de notificações de SRAG por município, mas não há campo para contar registros sem coluna total.
- implementation_support: **partial** — A relação 'srag_ubs_municipio_notificacao' permite combinar os componentes de SRAG e UBS, mas não há relação para combinar leitos e municípios. A falta de relação cadastrada para leitos e municípios limita o suporte.

## control_explicit — formulation

Tempo: 26.19s; erro: nenhum.

- context_completeness: **pass** — O contexto fornece todas as informações necessárias para a pergunta.
- analytical_specificity: **pass** — A pergunta define claramente a unidade (lojas), a medida (vendas em reais), o agrupamento (por loja) e a seleção (vendas altas, soma maior que 1000 reais).
- unambiguity: **pass** — Não há ambiguidade na pergunta ou no contexto fornecido.

Concordância no controle de ambiguidade: True.

## control_undefined — formulation

Tempo: 19.47s; erro: nenhum.

- context_completeness: **fail** — Falta contexto NECESSÁRIO. Consulta irrestrita a uma base não exige período/local automaticamente.
- analytical_specificity: **not_assessable** — Não há informações suficientes para avaliar a especificidade analítica.
- unambiguity: **not_assessable** — Não há informações suficientes para avaliar a ambiguidade.

Concordância no controle de ambiguidade: False.
