# Diagnóstico isolado de qualidade das perguntas

Não é avaliação oficial. Seleção de campos herdada do mapeamento v6; sem gabaritos nas entradas.
Resultados estruturalmente válidos ainda exigem inspeção semântica. Sem retomada automática de falhas.
Modelo: llama3.1:8b. Tempo: 302.6s.

## 12 — formulation

Tempo: 73.97s; erro: nenhum.

- context_completeness: **pass** — A pergunta é clara e não requer contexto adicional.
- analytical_specificity: **pass** — A unidade contada é 'registros de vacinação', a medida é 'total' e o agrupamento é 'fabricante'. A seleção é implícita na pergunta.
- unambiguity: **fail** — Há duas interpretações plausíveis: 1) A pergunta está procurando por fabricantes que não tenham registros de vacinação, mas que tenham mais registros do que outros; 2) A pergunta está procurando por fabricantes que tenham mais registros de vacinação, independentemente de terem ou não registros. Para resolver essa ambiguidade, seria necessário definir claramente o que se entende por 'não vazio' em relação aos registros de vacinação.

## 12 — support

Tempo: 43.88s; erro: nenhum.

- data_availability: **pass** — COUNT conta registros sem coluna total; SUM precisa de campo quantitativo.
- implementation_support: **partial** — Falta de relação cadastrada permite suporte parcial, não prova impossibilidade; O inventário de relacionamentos é completo; a seleção de campos é parcial, herdada de um mapeamento automático anterior e pode estar errada.

## 65 — formulation

Tempo: 41.05s; erro: nenhum.

- context_completeness: **fail** — Falta de contexto necessário para determinar os estados com maior número de notificações de SRAG.
- analytical_specificity: **partial** — A unidade contada (leitos de UTI) e a medida (quantidade) estão definidas, mas a seleção (estados com maior número de notificações de SRAG) não é específica.
- unambiguity: **fail** — Há duas interpretações plausíveis: (1) a quantidade de leitos de UTI SUS nos estados com maior número de notificações de SRAG em um período específico, ou (2) a quantidade de leitos de UTI SUS nos estados que sempre têm o maior número de notificações de SRAG. Além disso, a definição de 'maior número de notificações' pode variar dependendo do período e da fonte de dados.

## 65 — support

Tempo: 29.75s; erro: Justificativa ausente..


## 68 — formulation

Tempo: 28.34s; erro: nenhum.

- context_completeness: **partial** — falta de informações sobre o período/local de referência
- analytical_specificity: **pass** — unidades de saúde (UBS) e leitos são definidos
- unambiguity: **fail** — duas interpretações plausíveis: (1) municípios com alto número de notificações e baixa disponibilidade de leitos em geral, ou (2) municípios com alto número de notificações de SRAG e baixa disponibilidade de leitos em UBS específicas

## 68 — support

Tempo: 30.59s; erro: nenhum.

- data_availability: **partial** — COUNT conta registros sem coluna total; SUM precisa de campo quantitativo.
- implementation_support: **partial** — Falta de relação cadastrada permite suporte parcial, não prova impossibilidade.

## control_explicit — formulation

Tempo: 28.61s; erro: nenhum.

- context_completeness: **pass** — O contexto fornece informações suficientes para realizar a consulta.
- analytical_specificity: **pass** — A unidade contada é a soma de vendas, a medida é maior que 1000 reais, o agrupamento é por loja e a seleção é todas as lojas.
- unambiguity: **pass** — A definição de 'vendas altas' como soma maior que 1000 reais resolve a ambiguidade.

Concordância no controle de ambiguidade: True.

## control_undefined — formulation

Tempo: 26.45s; erro: nenhum.

- context_completeness: **fail** — Falta de contexto necessário para identificar as lojas e as vendas.
- analytical_specificity: **fail** — Unidade contada, medida, agrupamento e seleção não estão definidos.
- unambiguity: **fail** — Pode haver duas interpretações plausíveis com resultados diferentes, como 'lojas' referindo-se a lojas físicas ou online, e 'vendas altas' referindo-se a um período específico ou a uma comparação com o ano anterior.

Concordância no controle de ambiguidade: True.
