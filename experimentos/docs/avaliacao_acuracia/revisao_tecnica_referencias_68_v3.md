# Revisão técnica das 68 referências — protocolo v3

## Parecer

A revisão cobriu individualmente as 68 fichas: **64 consultas de referência e quatro comportamentos de limitação**, que não possuem SQL numérico. As 64 consultas executaram novamente, reproduziram os resultados congelados e coincidiram com um recálculo separado em Python. O esquema e o conteúdo das quatro tabelas coincidiram com o pacote v3 antes e depois da conferência.

**Não encontrei divergência numérica entre as referências e a interpretação operacional adotada no recálculo para os dados atuais.** A inspeção pergunta–SQL identificou duas diferenças pontuais de escopo, Q25 e Q58, que devem ser explicitadas antes da assinatura final do protocolo. Há também ressalvas sobre tipos, carga e significado dos indicadores, registradas em cada ficha. Correspondência numérica, isoladamente, não comprova validade semântica universal.

Esta é uma revisão técnica feita com assistência de IA, não uma declaração de que Lucas ou outro revisor humano assinou as referências. O autor deve conferir o parecer e registrar sua decisão com a data real. Não foram alterados SQLs do catálogo, enunciados, comparadores, status de revisão, pacote congelado, resultados das rodadas ou código de produção. Nenhuma avaliação foi reclassificada.

## Base da revisão

- Catálogo: `catalogo_68_v3.json`.
- Pacote utilizado: `../../referencias_68_catalogo_v3.json`.
- Código de carga e conversão: `../../backend/etl/load_csv.py`.
- Esquemas e relacionamentos locais: `../../backend/metadata/`.
- Conferência executável: [conferencia_referencias_v3.py](conferencia_referencias_v3.py).
- Evidência das 64 comparações: [conferencia_referencias_v3_resultado.json](conferencia_referencias_v3_resultado.json).
- Conferência das idades nos CSVs: [conferencia_idades_csv_v3.json](conferencia_idades_csv_v3.json).
- Parecer estruturado por ID: [parecer_referencias_v3.json](parecer_referencias_v3.json).

O recálculo usou operações Python de contagem, conjuntos, agrupamentos, somas e seleção de extremos, escritas separadamente das consultas SQL. Leu apenas os campos necessários, sem chamar a LLM e sem alterar tabelas. Não exportou linhas individuais de pacientes; as evidências preservadas são agregadas. A conferência numérica usa inteiros exatos e tolerância de ponto flutuante de 1e-9 absoluta/1e-12 relativa para acomodar diferenças aritméticas entre motores; não substitui as tolerâncias do experimento. Não utiliza o comparador do experimento para decidir a equivalência das tabelas.

A verificação é independente na implementação do cálculo, mas **não independente em autoria ou julgamento**: a mesma assistência de IA participou da referência e deste parecer. Ambas usam os dados já carregados, portanto não constituem uma auditoria integral CSV–banco. Houve uma conferência adicional específica das idades nos CSVs.

O dicionário oficial SIVEP-Gripe consultado descreve TP_IDADE como 1=dia, 2=mês e 3=ano, e distingue EVOLUCAO=2 de óbito por outras causas, código 3. Isso sustenta a leitura dos campos na revisão, mas é uma edição de 2022 e não uma certificação integral do esquema de 2026. As perguntas revisadas que usam códigos literais permanecem avaliadas segundo esses códigos explicitados. [Dicionário oficial SIVEP-Gripe, páginas 4 e 22](https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SRAG/pdfs/dicionario_de_dados_srag_hosp_17_02_2022.pdf).

## Pontos que merecem decisão antes da validação final

### Q25: filtro de município positivo não está explícito

A pergunta pede contagem por UF, município e bairro não vazio. O SQL acrescenta `ibge > 0` e uma condição de UF não vazia. A especificação global exige CNES positivos, mas não torna explícito que todos os agrupamentos municipais excluem município não positivo.

Recomendação: explicitar na pergunta “por UF não vazia, código de município positivo e bairro não vazio após remover espaços externos”. Se o objetivo for manter a pergunta literal sem essas exclusões, revisar os filtros do SQL. Não foi feita nenhuma dessas alterações nesta revisão.

No recorte atual não há linha com CNES positivo, bairro preenchido e município não positivo. Também não há UF não positiva entre CNES positivos. Por isso, essa diferença não muda os valores da rodada atual, mas poderia mudar em outros dados.

### Q58: denominador diferente de zero versus positivo

A pergunta diz excluir denominadores zero; o SQL usa `HAVING sum(LEITOS_EXISTENTES) > 0`, que exclui também negativos. Com capacidade não negativa, as duas condições coincidem. Não foi encontrado valor negativo de LEITOS_EXISTENTES ou LEITOS_SUS na competência atual.

Recomendação: se a regra desejada é rejeitar totais negativos como dados inválidos, explicitar “denominador positivo” na pergunta. Se o teste deve seguir literalmente “não zero” para qualquer valor, usar `!= 0`. Não é necessário mudar o número observado nesta rodada; a decisão é sobre o contrato geral.

### Idades: SQL aderente, mas a carga deve preservar a distinção entre ausência e zero

`paciente_idade` e `nu_idade_n` são Int32 não anuláveis. A carga transforma ausência ou valor inválido em zero, por isso um SQL não consegue recuperar a ausência original apenas com `IS NOT NULL`. Isso importa para Q7/Q9/Q42 em futuras cargas.

Nos CSVs atuais, foram lidas 390.911 linhas de vacinação e 92.156 de SRAG. Não foram encontradas magnitudes de idade ausentes/inválidas: os 1.438 zeros da vacinação e 698 de SRAG são zeros explícitos. Em SRAG, todas as unidades de idade carregadas pertencem a 1/2/3. Portanto, a ressalva não demonstrou erro no resultado atual da Q42. Sua conversão em anos é aproximada, mas foi explicitamente estipulada no enunciado; não deve ser apresentada como cálculo clínico exato da idade.

### UF, competência e unidade de contagem

- Em Q17/Q18/Q26/Q27, UF é Int32: `toString(uf) != ''` não exclui código zero. A pergunta diz não vazio, não código geográfico válido; registrar essa distinção. Não há UF não positiva no conjunto elegível atual.
- COMP é String, com valores atuais `202601` e `202602`. Ambos são AAAAMM válidos; MAX textual seleciona corretamente `202602`. A premissa precisará ser mantida em novas cargas.
- Não há CNES repetido na competência mais recente dos leitos. As somas dessa competência não sofrem repetição de estabelecimento por CNES no recorte conferido.
- Vacinação mede registros; SRAG mede linhas de notificação; UBS mede CNES distintos; leitos mede capacidade registrada. Nenhum desses resultados deve ser reinterpretado automaticamente como pessoas distintas, unidades ativas, ocupação ou vagas livres.

### Alcance das 68 fichas e comparação com o artigo

Os 68 IDs contêm 64 enunciados distintos. Entre as 64 perguntas analíticas, são 60 enunciados distintos: Q21 repete Q20, Q26 repete Q17, Q27 repete Q18 e Q64 repete Q63. Sessenta e três textos do catálogo diferem literalmente dos originais, inclusive por simples explicitação de contrato. Assim, a revisão confirma correspondência com os **enunciados atuais**, não equivalência automática com a formulação do artigo.

As quatro fichas Q65–Q68 testam a ausência de integração na implementação atual. Não têm referência numérica e não demonstram impossibilidade de responder com os dados após novas implementações. O relatório deve manter essa separação.

### Regras de comparação

As referências estão coerentes com as colunas e a ordem de colunas das fichas. Aliases SQL não precisam coincidir; o comparador usa posição. Q62 exige ordenação de linhas; as demais são comparadas sem ordem, mantendo multiplicidade. Percentuais e razão possuem tolerâncias por coluna. As únicas normalizações específicas são ano na Q32 e capitalização do nome do indicador na Q45.

Essas escolhas são decisões metodológicas, não verdades inerentes ao SQL. Como demonstrado pela Q6 da execução, colunas extras podem reprovar uma resposta que contém o valor correto. A aceitação dessas regras precisa constar do protocolo antes da avaliação final, sem flexibilização oportunista após observar resultados. Não foi feita auditoria completa da implementação do comparador neste parecer.

## Revisão individual

Cada ficha abaixo reproduz a pergunta atual e o SQL exato do pacote, com a análise correspondente. As amostras de resultado são limitadas a duas linhas para manter o documento legível; os resultados completos permanecem no pacote congelado. A amostra não implica ordenação obrigatória, exceto na Q62.

### Q01

**Pergunta avaliada:** Quantas doses de vacina contra a COVID-19 foram registradas no conjunto de dados carregado?

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

count() conta as linhas carregadas, correspondendo à convenção de registros de doses do protocolo. Não mede pessoas distintas nem elimina duplicatas. O resultado é aderente a essa unidade de observação.

**SQL de referência:**

```sql
SELECT count() AS total FROM vacinacao
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[390911]]
```

### Q02

**Pergunta avaliada:** Qual UF de residência não vazia tem mais registros de primeira dose ('1ª Dose') no recorte? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Filtra a descrição literal '1ª Dose' e UF de residência não vazia, conta por UF e seleciona todos os grupos cujo total coincide com o máximo. O uso de residência, e não estabelecimento, está explícito na pergunta.

**Formulação original, para rastreabilidade:** Qual estado apresentou o maior número de registros de primeira dose de COVID-19?

**SQL de referência:**

```sql
WITH grouped AS (SELECT paciente_endereco_uf AS uf, count() AS total FROM vacinacao WHERE paciente_endereco_uf != '' AND vacina_descricao_dose = '1ª Dose' GROUP BY uf) SELECT uf,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `uf, total`.

**Amostra do resultado:**

```json
[["AC", 137778]]
```

### Q03

**Pergunta avaliada:** Quantos registros têm vacina_descricao_dose igual a '2ª Dose' na base carregada?

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

countIf aplica igualdade exata com '2ª Dose', sem incluir descrições de reforço ou categorias semelhantes. O pedido é por registros, portanto não exige DISTINCT de pessoa.

**Formulação original, para rastreabilidade:** Quantos registros de segunda dose contra a COVID-19 existem no conjunto de dados carregado?

**SQL de referência:**

```sql
SELECT countIf(vacina_descricao_dose = '2ª Dose') AS total FROM vacinacao
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[120703]]
```

### Q04

**Pergunta avaliada:** Por UF de residência não vazia, qual a diferença entre registros de '1ª Dose' e '2ª Dose'? Retorne UF e diferença, incluindo todas as UFs presentes.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Agrupa todas as UFs de residência não vazias antes das contagens condicionais, preservando UFs sem primeira/segunda dose. Subtrai segunda de primeira; toInt64 evita subtração sem sinal. A ordem da diferença acompanha a ordem dos termos do enunciado.

**Formulação original, para rastreabilidade:** Qual é a diferença entre registros de primeira dose e segunda dose por estado?

**SQL de referência:**

```sql
SELECT paciente_endereco_uf AS uf, toInt64(countIf(vacina_descricao_dose = '1ª Dose')) - toInt64(countIf(vacina_descricao_dose = '2ª Dose')) AS diferenca FROM vacinacao WHERE paciente_endereco_uf != '' GROUP BY uf
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 28 linha(s), 2 coluna(s): `uf, diferenca`.

**Amostra do resultado:**

```json
[["RJ", 40], ["DF", 14]]
```

### Q05

**Pergunta avaliada:** Qual a razão entre o número de registros cuja descrição da dose contém 'reforço' (sem distinguir maiúsculas) e os de '1ª Dose'? Retorne apenas a razão, não percentual; nulo se denominador zero. Retorne a razão com pelo menos seis casas decimais.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Busca 'reforço' sem distinguir caixa apenas no numerador e usa igualdade exata de '1ª Dose' no denominador. NULLIF produz nulo quando não há primeiras doses. Não multiplica por 100; corresponde a razão, não percentual. A busca não ignora acentos, e isso não foi solicitado.

**Formulação original, para rastreabilidade:** Quantos registros de doses de reforço existem em relação aos registros de primeira dose?

**SQL de referência:**

```sql
SELECT countIf(positionCaseInsensitiveUTF8(ifNull(vacina_descricao_dose,''), 'reforço') > 0) / nullIf(countIf(vacina_descricao_dose = '1ª Dose'),0) AS razao FROM vacinacao
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `razao`.

**Amostra do resultado:**

```json
[[0.6620176662017666]]
```

### Q06

**Pergunta avaliada:** Qual o percentual de registros F e de registros M no campo paciente_enumSexoBiologico, usando somente F e M no denominador? Retorne as duas categorias e percentuais, nulo se não houver F/M.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Calcula F e M sobre o mesmo denominador restrito a F/M. UNION ALL materializa as duas categorias mesmo quando uma tem zero registros. Se não houver F/M, ambas permanecem com percentual nulo. Duas colunas, categoria e percentual, correspondem ao contrato atual.

**Formulação original, para rastreabilidade:** Qual é o percentual de mulheres em relação a homens na campanha de vacinação?

**SQL de referência:**

```sql
SELECT 'F' AS sexo, 100.0 * countIf(paciente_enumSexoBiologico = 'F') / nullIf(countIf(paciente_enumSexoBiologico IN ('F','M')),0) AS percentual FROM vacinacao UNION ALL SELECT 'M' AS sexo, 100.0 * countIf(paciente_enumSexoBiologico = 'M') / nullIf(countIf(paciente_enumSexoBiologico IN ('F','M')),0) AS percentual FROM vacinacao
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 2 linha(s), 2 coluna(s): `sexo, percentual`.

**Amostra do resultado:**

```json
[["M", 47.1490953183717], ["F", 52.8509046816283]]
```

### Q07

**Pergunta avaliada:** Entre faixas etárias presentes 0-18, 19-59 e 60+ anos, excluindo idades negativas, qual tem menos registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: faixa,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Exclui idades negativas, classifica a idade inteira em até 18, até 59 e 60+, conta e seleciona o mínimo entre grupos presentes. Não cria faixas ausentes com zero, em conformidade com 'presentes'. A carga usa Int32; a conferência dos CSVs não encontrou idade ausente/inválida nesse recorte.

**Formulação original, para rastreabilidade:** Qual faixa etária teve menor número de registros de vacinação?

**SQL de referência:**

```sql
WITH grouped AS (SELECT multiIf(paciente_idade < 0, 'ignorada', paciente_idade <= 18, '0-18', paciente_idade <= 59, '19-59', '60+') AS faixa, count() AS total FROM vacinacao WHERE paciente_idade >= 0 GROUP BY faixa) SELECT faixa,total FROM grouped WHERE total = (SELECT min(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `faixa, total`.

**Amostra do resultado:**

```json
[["60+", 53986]]
```

### Q08

**Pergunta avaliada:** Quais municípios de residência (UF e código IBGE não vazios) têm a maior contagem de registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,municipio,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Usa o código IBGE de residência e a UF, exclui código vazio/nulo e UF vazia, conta cada combinação e mantém todos os máximos. A referência não troca código por nome nem exige validação do cadastro IBGE além de não vazio.

**Formulação original, para rastreabilidade:** Quais municípios apresentam maior número de registros de vacinação contra a COVID-19?

**SQL de referência:**

```sql
WITH grouped AS (SELECT paciente_endereco_uf AS uf, paciente_endereco_coIbgeMunicipio AS municipio, count() AS total FROM vacinacao WHERE paciente_endereco_uf != '' AND notEmpty(ifNull(paciente_endereco_coIbgeMunicipio,'')) GROUP BY uf,municipio) SELECT uf,municipio,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 3 coluna(s): `uf, municipio, total`.

**Amostra do resultado:**

```json
[["AC", "120040", 187760]]
```

### Q09

**Pergunta avaliada:** Qual a contagem de registros de vacinação por UF de residência não vazia e faixas 0-18, 19-59 e 60+ anos? Exclua idades negativas; retorne todos os grupos presentes, UF, faixa e total. Não conte pessoas distintas.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Conta registros por UF de residência e faixa de idade, com limites compatíveis com idade inteira. Exclui UF vazia e idade negativa; mantém apenas grupos presentes. Não usa pessoa distinta, como solicitado.

**Formulação original, para rastreabilidade:** Qual é a distribuição de vacinados por faixa etária e estado (análise de duas dimensões)?

**SQL de referência:**

```sql
SELECT paciente_endereco_uf AS uf, multiIf(paciente_idade < 0, 'ignorada', paciente_idade <= 18, '0-18', paciente_idade <= 59, '19-59', '60+') AS faixa, count() AS total FROM vacinacao WHERE paciente_endereco_uf != '' AND paciente_idade >= 0 GROUP BY uf,faixa
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 83 linha(s), 3 coluna(s): `uf, faixa, total`.

**Amostra do resultado:**

```json
[["PE", "60+", 11], ["SC", "60+", 62]]
```

### Q10

**Pergunta avaliada:** Qual a contagem de registros de vacinação por sistema_origem? Retorne todos os grupos; mantenha nulos como nulos.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

GROUP BY sistema_origem preserva cada categoria e o grupo NULL. A soma dos totais deve recuperar todas as linhas de vacinação. Não há filtro indevido de preenchimento.

**Formulação original, para rastreabilidade:** Qual é a distribuição de doses registradas por sistema de origem dos dados?

**SQL de referência:**

```sql
SELECT sistema_origem, count() AS total FROM vacinacao GROUP BY sistema_origem
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 5 linha(s), 2 coluna(s): `sistema_origem, total`.

**Amostra do resultado:**

```json
[[null, 399], ["Novo PNI", 385633]]
```

### Q11

**Pergunta avaliada:** Qual vacina_nome não vazio tem mais registros e qual o percentual desses registros sobre todas as linhas de vacinação? Retorne nome e percentual. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: vacina,percentual.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Agrupa nomes de vacina não vazios, mas divide pela contagem de todas as linhas, incluindo aquelas sem nome. Como o denominador é comum, maximizar percentual equivale a maximizar quantidade. Retorna todos os empates e apenas nome/percentual.

**Formulação original, para rastreabilidade:** Qual vacina foi mais utilizada na campanha (em % de doses totais)?

**SQL de referência:**

```sql
WITH grouped AS (SELECT vacina_nome AS vacina, 100.0 * count() / nullIf((SELECT count() FROM vacinacao),0) AS percentual FROM vacinacao WHERE notEmpty(ifNull(vacina_nome,'')) GROUP BY vacina) SELECT vacina,percentual FROM grouped WHERE percentual = (SELECT max(percentual) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `vacina, percentual`.

**Amostra do resultado:**

```json
[["COVID-19 PFIZER - COMIRNATY", 38.50237010470414]]
```

### Q12

**Pergunta avaliada:** Qual fabricante não vazio tem mais registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: fabricante,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Exclui fabricante vazio/nulo, agrupa pelo nome original, conta registros e seleciona todos os fabricantes com máximo. Não normaliza nomes, o que corresponde ao agrupamento literal do campo.

**Formulação original, para rastreabilidade:** Qual fabricante aparece com maior número de registros de doses aplicadas?

**SQL de referência:**

```sql
WITH grouped AS (SELECT vacina_fabricante_nome AS fabricante, count() AS total FROM vacinacao WHERE notEmpty(ifNull(vacina_fabricante_nome,'')) GROUP BY fabricante) SELECT fabricante,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `fabricante, total`.

**Amostra do resultado:**

```json
[["PFIZER", 166920]]
```

### Q13

**Pergunta avaliada:** Qual a contagem de registros de vacinação por ano e mês de aplicação? Retorne mes no formato AAAA-MM e total de todos os meses presentes; exclua datas nulas.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Exclui data de aplicação nula, formata ano e mês como AAAA-MM e conta todos os grupos existentes. Não mistura meses de anos diferentes e não exige ordenação não pedida.

**Formulação original, para rastreabilidade:** Qual é a evolução temporal de doses aplicadas por mês (tendência da campanha)?

**SQL de referência:**

```sql
SELECT formatDateTime(vacina_dataAplicacao,'%Y-%m') AS mes, count() AS total FROM vacinacao WHERE vacina_dataAplicacao IS NOT NULL GROUP BY mes
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 45 linha(s), 2 coluna(s): `mes, total`.

**Amostra do resultado:**

```json
[["2022-03", 12490], ["2023-06", 2661]]
```

### Q14

**Pergunta avaliada:** Qual combinação de UF de residência não vazia e mês de aplicação (AAAA-MM) tem mais registros de vacinação? Exclua datas nulas. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,mes,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Agrupa por residência e ano-mês de aplicação, excluindo UF vazia e datas nulas. O máximo é global entre as combinações, não um máximo separado por UF; essa leitura corresponde ao enunciado.

**Formulação original, para rastreabilidade:** Qual estado teve o maior pico de vacinação em um único mês?

**SQL de referência:**

```sql
WITH grouped AS (SELECT paciente_endereco_uf AS uf, formatDateTime(vacina_dataAplicacao,'%Y-%m') AS mes, count() AS total FROM vacinacao WHERE paciente_endereco_uf != '' AND vacina_dataAplicacao IS NOT NULL GROUP BY uf,mes) SELECT uf,mes,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 3 coluna(s): `uf, mes, total`.

**Amostra do resultado:**

```json
[["AC", "2021-08", 37844]]
```

### Q15

**Pergunta avaliada:** Quantos registros existem por descrição de dose que contenha 'reforço', sem distinguir maiúsculas? Preserve a descrição original e retorne todos os grupos.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Filtra descrições contendo 'reforço' sem distinção de caixa, mas agrupa pela descrição original. Portanto, variantes de caixa permanecem em grupos separados, como exige a preservação da descrição original.

**Formulação original, para rastreabilidade:** Quantos registros existem para cada tipo de dose de reforço (Reforço 1, Reforço 2, etc.)?

**SQL de referência:**

```sql
SELECT vacina_descricao_dose AS dose, count() AS total FROM vacinacao WHERE positionCaseInsensitiveUTF8(ifNull(vacina_descricao_dose,''), 'reforço') > 0 GROUP BY dose
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 4 linha(s), 2 coluna(s): `dose, total`.

**Amostra do resultado:**

```json
[["Reforço", 74868], ["2º Reforço", 19079]]
```

### Q16

**Pergunta avaliada:** Quantas UBS distintas estão cadastradas na base carregada, contando CNES positivos? Não inferir situação ativa.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

uniqExact(cnes) com cnes > 0 mede identificadores distintos cadastrados. A pergunta revisada explicitamente não pede situação ativa. A referência não serviria para afirmar unidades ativas usando a pergunta original.

**Formulação original, para rastreabilidade:** Quantas Unidades Básicas de Saúde (UBS) estão ativas no Brasil?

**SQL de referência:**

```sql
SELECT uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[47721]]
```

### Q17

**Pergunta avaliada:** Qual a contagem de CNES distintos positivos de UBS por código de UF não vazio? Retorne todos os grupos presentes.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Conta CNES positivos distintos dentro de cada UF. UF é Int32; toString(uf) != '' não exclui zero ou código inválido. Isso atende literalmente a 'não vazio' na tabela carregada, mas não é validação geográfica. Não há UF não positiva entre os CNES positivos atuais.

**Formulação original, para rastreabilidade:** Qual é a distribuição de UBS por estado?

**SQL de referência:**

```sql
SELECT uf, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND toString(uf) != '' GROUP BY uf
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 27 linha(s), 2 coluna(s): `uf, total`.

**Amostra do resultado:**

```json
[[41, 2366], [53, 211]]
```

### Q18

**Pergunta avaliada:** Qual código de UF não vazio tem mais UBS distintas (CNES positivos)? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Aplica a mesma contagem distinta por UF da Q17 e seleciona todos os máximos. A ressalva de UF numérica não vazia versus UF válida também se aplica, sem efeito no recorte atual.

**Formulação original, para rastreabilidade:** Qual estado tem o maior número absoluto de UBS cadastradas?

**SQL de referência:**

```sql
WITH grouped AS (SELECT uf, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND toString(uf) != '' GROUP BY uf) SELECT uf,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `uf, total`.

**Amostra do resultado:**

```json
[[31, 6137]]
```

### Q19

**Pergunta avaliada:** Quantos códigos de município positivos possuem pelo menos um CNES positivo na base de UBS?

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Conta códigos de município distintos positivos entre linhas com CNES positivo. Não conta UBS ou linhas como se fossem municípios e não precisa de uma tabela de população.

**Formulação original, para rastreabilidade:** Em quantos municípios há pelo menos uma UBS cadastrada?

**SQL de referência:**

```sql
SELECT uniqExact(ibge) AS total FROM atencao_basica WHERE cnes > 0 AND ibge > 0
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[5483]]
```

### Q20

**Pergunta avaliada:** Quais códigos de município positivos têm mais UBS distintas, contando CNES positivos nos municípios presentes na base? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: municipio,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Conta CNES distintos positivos por município positivo e seleciona todos os máximos. Município é identificado pelo código; nomes homônimos não são fundidos.

**Formulação original, para rastreabilidade:** Quais municípios possuem o maior número de UBS cadastradas?

**SQL de referência:**

```sql
WITH grouped AS (SELECT ibge AS municipio, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND ibge > 0 GROUP BY municipio) SELECT municipio,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `municipio, total`.

**Amostra do resultado:**

```json
[[355030, 645]]
```

### Q21

**Pergunta avaliada:** Quais códigos de município positivos têm mais UBS distintas, contando CNES positivos nos municípios presentes na base? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: municipio,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Mesmo enunciado e SQL da Q20. A referência é aderente, mas o caso repete a mesma tarefa e não acrescenta uma pergunta independente ao conjunto.

**Formulação original, para rastreabilidade:** Qual município tem o maior número de UBS cadastradas no recorte carregado?

**SQL de referência:**

```sql
WITH grouped AS (SELECT ibge AS municipio, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND ibge > 0 GROUP BY municipio) SELECT municipio,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `municipio, total`.

**Amostra do resultado:**

```json
[[355030, 645]]
```

### Q22

**Pergunta avaliada:** Na base de UBS, qual a contagem de CNES distintos positivos por município positivo nas UFs de códigos 21 a 29 (Nordeste)? Retorne todos os municípios, código e total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Filtra UFs 21 a 29, município positivo e CNES positivo; agrupa somente por código municipal e conta CNES distintos. O IN usa literais de texto contra UF numérica, aceitos pelo ClickHouse nesta execução; o conjunto selecionado coincide com o intervalo numérico 21–29 no recálculo.

**Formulação original, para rastreabilidade:** Qual é o padrão de distribuição de UBS nos municípios da região Nordeste?

**SQL de referência:**

```sql
SELECT ibge AS municipio, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND ibge > 0 AND uf IN ('21','22','23','24','25','26','27','28','29') GROUP BY municipio
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1783 linha(s), 2 coluna(s): `municipio, total`.

**Amostra do resultado:**

```json
[[250600, 16], [260030, 14]]
```

### Q23

**Pergunta avaliada:** Quantas UBS distintas (CNES positivos) têm latitude e longitude não zero e dentro de [-90,90] e [-180,180]?

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Filtra CNES positivo, ambas as coordenadas diferentes de zero e intervalos inclusivos de latitude/longitude, antes de contar identificadores distintos. Mede UBS com pelo menos uma linha que satisfaz os critérios, não prova precisão geográfica das coordenadas.

**Formulação original, para rastreabilidade:** Quantas UBS possuem informações completas de localização (latitude/longitude)?

**SQL de referência:**

```sql
SELECT uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND latitude != 0 AND longitude != 0 AND latitude BETWEEN -90 AND 90 AND longitude BETWEEN -180 AND 180
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[45792]]
```

### Q24

**Pergunta avaliada:** Quais municípios positivos têm mais UBS distintas com CNES positivo e coordenadas não zero nos intervalos latitude [-90,90] e longitude [-180,180]? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: municipio,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Aplica os mesmos critérios de coordenadas da Q23 e município positivo; conta CNES distintos por município e retorna todos os máximos. Não considera coordenada zero válida apenas por estar dentro do intervalo.

**Formulação original, para rastreabilidade:** Quais municípios possuem maior número de UBS com coordenadas geográficas registradas?

**SQL de referência:**

```sql
WITH grouped AS (SELECT ibge AS municipio, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND ibge > 0 AND latitude != 0 AND longitude != 0 AND latitude BETWEEN -90 AND 90 AND longitude BETWEEN -180 AND 180 GROUP BY municipio) SELECT municipio,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `municipio, total`.

**Amostra do resultado:**

```json
[[355030, 555]]
```

### Q25

**Pergunta avaliada:** Qual a contagem de CNES distintos positivos por UF, município e bairro não vazio da base UBS? Retorne todos os grupos; não una bairros homônimos de municípios diferentes.

**Parecer:** Aderente com ressalva de escopo a explicitar.

O agrupamento por UF, município e bairro evita fundir bairros homônimos. Entretanto, o SQL também impõe ibge > 0 e UF não vazia, condições não explicitadas com clareza no enunciado, que só qualifica bairro como não vazio. Recomenda-se explicitar esses filtros na pergunta antes de fechar o protocolo. O filtro de bairro usa trimBoth somente para excluir vazio; não une grafias diferentes. No recorte atual não existem linhas elegíveis com bairro preenchido e município não positivo, nem UF não positiva entre CNES positivos; a ressalva não muda o resultado observado.

**Formulação original, para rastreabilidade:** Qual é a distribuição de UBS por bairro no conjunto de dados carregado?

**SQL de referência:**

```sql
SELECT uf, ibge AS municipio, bairro, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND toString(uf) != '' AND ibge > 0 AND trimBoth(bairro) != '' GROUP BY uf,municipio,bairro
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 33696 linha(s), 4 coluna(s): `uf, municipio, bairro, total`.

**Amostra do resultado:**

```json
[[29, 291005, "GENARO", 1], [42, 420730, "VILA SANTO ANTONIO", 1]]
```

### Q26

**Pergunta avaliada:** Qual a contagem de CNES distintos positivos de UBS por código de UF não vazio? Retorne todos os grupos presentes.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Repete a Q17: CNES distintos positivos por UF. Aderente ao enunciado, com a ressalva do tipo numérico da UF. Registrar a duplicação ao descrever a diversidade do benchmark.

**Formulação original, para rastreabilidade:** Qual é a distribuição de UBS por código de UF?

**SQL de referência:**

```sql
SELECT uf, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND toString(uf) != '' GROUP BY uf
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 27 linha(s), 2 coluna(s): `uf, total`.

**Amostra do resultado:**

```json
[[41, 2366], [53, 211]]
```

### Q27

**Pergunta avaliada:** Qual código de UF não vazio tem mais UBS distintas (CNES positivos)? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Repete a Q18: máximo de CNES distintos positivos por UF. Aderente ao enunciado, mas não é um caso independente da Q18.

**Formulação original, para rastreabilidade:** Qual código de UF concentra o maior número de UBS cadastradas?

**SQL de referência:**

```sql
WITH grouped AS (SELECT uf, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND toString(uf) != '' GROUP BY uf) SELECT uf,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `uf, total`.

**Amostra do resultado:**

```json
[[31, 6137]]
```

### Q28

**Pergunta avaliada:** Quantas UBS distintas com CNES positivo possuem logradouro e bairro não vazios após remover espaços nas extremidades?

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Exige simultaneamente logradouro e bairro preenchidos após trimBoth, e conta CNES positivos distintos. Como campos de endereço são String, não há NULL persistido; ausências foram convertidas em vazio pela carga.

**Formulação original, para rastreabilidade:** Quantas UBS possuem logradouro e bairro registrados?

**SQL de referência:**

```sql
SELECT uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND trimBoth(logradouro) != '' AND trimBoth(bairro) != ''
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[47721]]
```

### Q29

**Pergunta avaliada:** Qual a contagem de UBS distintas com CNES positivo por bairro no município IBGE 355030? Inclua todos os grupos, inclusive bairro vazio.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Filtra município 355030 e CNES positivo; agrupa pelo bairro sem remover grupos vazios. Isso corresponde ao pedido explícito de incluir bairro vazio. A contagem distinta é por bairro, não uma distribuição necessariamente aditiva se um CNES aparecer em bairros diferentes.

**Formulação original, para rastreabilidade:** Qual é a distribuição de UBS por bairro no município com código IBGE 355030?

**SQL de referência:**

```sql
SELECT bairro, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND ibge = 355030 GROUP BY bairro
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 449 linha(s), 2 coluna(s): `bairro, total`.

**Amostra do resultado:**

```json
[["CAMBUCI", 1], ["IGUATEMI", 1]]
```

### Q30

**Pergunta avaliada:** Quais códigos de município positivos têm menos UBS distintas, contando CNES positivos nos municípios presentes na base? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: municipio,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Seleciona o mínimo de CNES distintos entre municípios positivos presentes. Não inclui municípios sem linha na base como zero, conforme a restrição do enunciado.

**Formulação original, para rastreabilidade:** Quais municípios possuem menor número de UBS cadastradas entre os municípios presentes na base?

**SQL de referência:**

```sql
WITH grouped AS (SELECT ibge AS municipio, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND ibge > 0 GROUP BY municipio) SELECT municipio,total FROM grouped WHERE total = (SELECT min(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 720 linha(s), 2 coluna(s): `municipio, total`.

**Amostra do resultado:**

```json
[[411325, 1], [314660, 1]]
```

### Q31

**Pergunta avaliada:** Quantas linhas de notificações existem na tabela SRAG carregada, sem filtrar classificação final?

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Conta todas as linhas da tabela SRAG, sem filtro de classificação final e sem deduplicação. Responde à pergunta revisada sobre linhas de notificações, não a um total de pessoas ou casos únicos.

**Formulação original, para rastreabilidade:** Quantos casos de SRAG foram notificados no período analisado?

**SQL de referência:**

```sql
SELECT count() AS total FROM srag
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[92156]]
```

### Q32

**Pergunta avaliada:** Qual a contagem de linhas de SRAG por ano de dt_notific e sem_not, excluindo dt_notific = '1970-01-01'? Retorne todos os grupos.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Agrupa pelo ano civil extraído de dt_notific e pelo valor armazenado em sem_not, excluindo a sentinela 1970-01-01. Responde literalmente ao pedido. Não deve ser apresentado como cálculo validado de ano epidemiológico, que pode diferir do ano civil nas fronteiras do ano.

**Formulação original, para rastreabilidade:** Qual é a evolução semanal de notificações de SRAG?

**SQL de referência:**

```sql
SELECT toYear(dt_notific) AS ano, sem_not AS semana, count() AS total FROM srag WHERE dt_notific != toDate('1970-01-01') GROUP BY ano,semana
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 20 linha(s), 3 coluna(s): `ano, semana, total`.

**Amostra do resultado:**

```json
[[2026, 6, 2736], [2026, 7, 3302]]
```

### Q33

**Pergunta avaliada:** Qual UF de notificação não vazia tem mais linhas de SRAG na base carregada? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Conta linhas por UF de notificação não vazia e seleciona todos os máximos. A referência usa sg_uf_not, não a UF de residência sg_uf.

**Formulação original, para rastreabilidade:** Qual estado apresentou o maior número de casos de SRAG no período?

**SQL de referência:**

```sql
WITH grouped AS (SELECT sg_uf_not AS uf, count() AS total FROM srag WHERE sg_uf_not != '' GROUP BY uf) SELECT uf,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `uf, total`.

**Amostra do resultado:**

```json
[["SP", 19467]]
```

### Q34

**Pergunta avaliada:** Qual a contagem de linhas de SRAG por UF de notificação não vazia? Retorne todas as UFs presentes.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Retorna todas as UFs de notificação não vazias com contagens de linhas. Não aplica filtros clínicos ou deduplicação não solicitados.

**Formulação original, para rastreabilidade:** Qual é a distribuição de notificações de SRAG por estado?

**SQL de referência:**

```sql
SELECT sg_uf_not AS uf, count() AS total FROM srag WHERE sg_uf_not != '' GROUP BY uf
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 27 linha(s), 2 coluna(s): `uf, total`.

**Amostra do resultado:**

```json
[["RJ", 5871], ["DF", 3976]]
```

### Q35

**Pergunta avaliada:** Quantos códigos de município de notificação positivos distintos existem nas linhas de SRAG?

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Conta municípios de notificação distintos com código positivo. Não exige que estejam em UBS ou tenham casos confirmados, pois isso não faz parte da pergunta.

**Formulação original, para rastreabilidade:** Em quantos municípios foram registrados casos de SRAG?

**SQL de referência:**

```sql
SELECT uniqExact(co_mun_not) AS total FROM srag WHERE co_mun_not > 0
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[1213]]
```

### Q36

**Pergunta avaliada:** Qual o percentual de linhas de SRAG com hospital = 1 entre todas as linhas? Retorne nulo se o denominador for zero.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Numerador hospital = 1; denominador todas as linhas. Ausentes/ignorados não entram no numerador, mas permanecem no denominador. Isso corresponde ao enunciado operacional, não à proporção entre somente respostas conhecidas.

**Formulação original, para rastreabilidade:** Qual é a taxa de hospitalização entre os casos notificados de SRAG?

**SQL de referência:**

```sql
SELECT 100.0 * countIf(hospital = 1) / nullIf(count(),0) AS percentual FROM srag
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `percentual`.

**Amostra do resultado:**

```json
[[94.27709536004167]]
```

### Q37

**Pergunta avaliada:** Quantas linhas de SRAG possuem evolucao = 2?

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Conta exatamente evolucao = 2. Não inclui código 3, que o dicionário consultado distingue como óbito por outras causas. A pergunta revisada cita o código explicitamente, evitando ambiguidade sobre todos os óbitos.

**Formulação original, para rastreabilidade:** Quantos casos evoluíram para morte?

**SQL de referência:**

```sql
SELECT countIf(evolucao = 2) AS total FROM srag
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[4151]]
```

### Q38

**Pergunta avaliada:** Qual o percentual de linhas de SRAG com evolucao = 2 entre as linhas com hospital = 1? Retorne nulo se o denominador for zero.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Numerador evolucao = 2 e hospital = 1; denominador somente hospital = 1. NULLIF trata ausência de hospitalizados. Não divide pelo total de SRAG nem restringe o denominador a evolução conhecida.

**Formulação original, para rastreabilidade:** Qual é a taxa de mortalidade entre os casos hospitalizados?

**SQL de referência:**

```sql
SELECT 100.0 * countIf(evolucao = 2 AND hospital = 1) / nullIf(countIf(hospital = 1),0) AS percentual FROM srag
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `percentual`.

**Amostra do resultado:**

```json
[[4.439354526829493]]
```

### Q39

**Pergunta avaliada:** Qual o percentual de linhas de SRAG com uti = 1 entre todas as linhas? Retorne nulo se o denominador for zero.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Conta uti = 1 sobre todas as linhas, com proteção contra denominador zero. Não usa apenas hospitalizados no denominador, pois a pergunta não pede essa restrição.

**Formulação original, para rastreabilidade:** Qual é a taxa de internação em UTI entre todos os casos?

**SQL de referência:**

```sql
SELECT 100.0 * countIf(uti = 1) / nullIf(count(),0) AS percentual FROM srag
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `percentual`.

**Amostra do resultado:**

```json
[[24.383653804418593]]
```

### Q40

**Pergunta avaliada:** Qual UF de notificação não vazia tem maior percentual de linhas com evolucao = 2, usando todas as linhas daquela UF no denominador? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,percentual.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Calcula evolucao = 2 sobre todas as linhas da mesma UF de notificação. O denominador local está correto; seleciona o maior percentual e todos os empates. Os grupos existentes têm contagem positiva.

**Formulação original, para rastreabilidade:** Qual estado teve a maior taxa de mortalidade (por casos)?

**SQL de referência:**

```sql
WITH grouped AS (SELECT sg_uf_not AS uf, 100.0 * countIf(evolucao = 2) / count() AS percentual FROM srag WHERE sg_uf_not != '' GROUP BY uf) SELECT uf,percentual FROM grouped WHERE percentual = (SELECT max(percentual) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `uf, percentual`.

**Amostra do resultado:**

```json
[["PI", 13.16793893129771]]
```

### Q41

**Pergunta avaliada:** Retorne uma linha com as contagens de SRAG em que cada indicador vale 1, na ordem febre, tosse, garganta, dispneia, diarreia e vomito. Uma notificação pode contribuir para vários sintomas.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Uma contagem condicional independente por sintoma, na ordem solicitada. Uma linha pode contribuir para vários indicadores; o SQL não força exclusividade e não soma os indicadores como pessoas distintas.

**Formulação original, para rastreabilidade:** Qual é a distribuição de sintomas primários entre os casos (febre, tosse, dispneia, etc)?

**SQL de referência:**

```sql
SELECT countIf(febre = 1) AS febre, countIf(tosse = 1) AS tosse, countIf(garganta = 1) AS garganta, countIf(dispneia = 1) AS dispneia, countIf(diarreia = 1) AS diarreia, countIf(vomito = 1) AS vomito FROM srag
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 6 coluna(s): `febre, tosse, garganta, dispneia, diarreia, vomito`.

**Amostra do resultado:**

```json
[[61089, 73263, 10769, 61264, 7973, 11283]]
```

### Q42

**Pergunta avaliada:** Qual faixa tem mais linhas de SRAG: 0-18, 19-59 ou 60+ anos? Use nu_idade_n como magnitude da idade e tp_idade 1=dias, 2=meses e 3=anos; exclua idade nula, negativa e unidades desconhecidas. Para este teste, converta dias dividindo por 365.25 e meses por 12; anos permanecem iguais. Use os intervalos [0,19), [19,60) e [60,infinito), com rótulos '0-18', '19-59' e '60+'. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: faixa,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Converte magnitude de idade conforme tp_idade 1/2/3, exclui unidade desconhecida e magnitude nula/negativa, usa limites <19 e <60 e seleciona todos os máximos. A conversão aproximada está explícita na pergunta. NU_IDADE_N é Int32 não anulável no banco, portanto IS NOT NULL sozinho não identificaria ausências já convertidas em zero. Nos CSVs atuais todas as magnitudes são numéricas; os 698 zeros são explícitos, não ausências detectadas. A proteção para futuras cargas requer preservar nulos ou validar a entrada.

**Formulação original, para rastreabilidade:** Qual é a faixa etária mais acometida por SRAG no período?

**SQL de referência:**

```sql
WITH grouped AS (SELECT multiIf((multiIf(tp_idade = 1, nu_idade_n / 365.25, tp_idade = 2, nu_idade_n / 12.0, toFloat64(nu_idade_n))) < 19, '0-18', (multiIf(tp_idade = 1, nu_idade_n / 365.25, tp_idade = 2, nu_idade_n / 12.0, toFloat64(nu_idade_n))) < 60, '19-59', '60+') AS faixa, count() AS total FROM srag WHERE tp_idade IN (1,2,3) AND nu_idade_n IS NOT NULL AND nu_idade_n >= 0 GROUP BY faixa) SELECT faixa,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `faixa, total`.

**Amostra do resultado:**

```json
[["0-18", 56766]]
```

### Q43

**Pergunta avaliada:** Qual o percentual de linhas de SRAG com ao menos um dos indicadores cardiopati, hematologi, hepatica, asma, diabetes, neurologic, pneumopati, imunodepre, renal ou obesidade igual a 1, sobre todas as linhas? Nulo se não houver linhas.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Usa OR dentro de countIf para que uma linha com vários indicadores seja contada uma única vez. Denominador todas as linhas, incluindo desconhecidos. A lista dos dez indicadores coincide com a pergunta.

**Formulação original, para rastreabilidade:** Qual é a proporção de casos com comorbidades (diabetes, asma, cardiopatia, etc) entre os notificados?

**SQL de referência:**

```sql
SELECT 100.0 * countIf(cardiopati = 1 OR hematologi = 1 OR hepatica = 1 OR asma = 1 OR diabetes = 1 OR neurologic = 1 OR pneumopati = 1 OR imunodepre = 1 OR renal = 1 OR obesidade = 1) / nullIf(count(),0) AS percentual FROM srag
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `percentual`.

**Amostra do resultado:**

```json
[[31.818872346890057]]
```

### Q44

**Pergunta avaliada:** Quantas linhas de SRAG têm pcr_sars2 = 1 ou pos_pcrflu = 1? Conte cada linha apenas uma vez.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

OR entre pcr_sars2 = 1 e pos_pcrflu = 1 conta cada linha uma vez, inclusive quando ambos estão marcados. Não equivale à soma de duas contagens nem à classificação final do caso.

**Formulação original, para rastreabilidade:** Quantos casos tiveram confirmação laboratorial (PCR positivo)?

**SQL de referência:**

```sql
SELECT countIf(pcr_sars2 = 1 OR pos_pcrflu = 1) AS total FROM srag
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[10154]]
```

### Q45

**Pergunta avaliada:** Entre os indicadores pcr_sars2, pos_pcrflu e pcr_vsr, qual possui mais linhas de SRAG com valor 1? Retorne o nome do indicador e a contagem. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: agente,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Monta uma linha de contagem para cada um dos três indicadores e seleciona todos os máximos. Os nomes retornados são os nomes dos campos. Mede marcação igual a 1, não um diagnóstico clínico independente. Se todos fossem zero, retornaria os três empatados.

**Formulação original, para rastreabilidade:** Qual agente etiológico foi mais frequentemente identificado (SARS-CoV-2, Influenza, VSR, etc)?

**SQL de referência:**

```sql
WITH grouped AS (SELECT 'pcr_sars2' AS agente, countIf(pcr_sars2 = 1) AS total FROM srag UNION ALL SELECT 'pos_pcrflu' AS agente, countIf(pos_pcrflu = 1) AS total FROM srag UNION ALL SELECT 'pcr_vsr' AS agente, countIf(pcr_vsr = 1) AS total FROM srag) SELECT agente,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `agente, total`.

**Amostra do resultado:**

```json
[["pos_pcrflu", 8190]]
```

### Q46

**Pergunta avaliada:** Qual a soma de LEITOS_EXISTENTES na tabela leitos na maior competência COMP global disponível? Conte leitos registrados, não vagas livres.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Soma LEITOS_EXISTENTES apenas na maior COMP global. COMP é texto, mas os valores atuais são AAAAMM válidos e de tamanho fixo; nesse domínio MAX textual coincide com a competência mais recente. Não soma competências diferentes nem mede vagas livres.

**Formulação original, para rastreabilidade:** Quantos leitos totais de internação estão disponíveis no Brasil?

**SQL de referência:**

```sql
SELECT sum(LEITOS_EXISTENTES) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[520569]]
```

### Q47

**Pergunta avaliada:** Qual a soma de LEITOS_SUS na tabela leitos na maior competência COMP global disponível? Conte leitos registrados, não vagas livres.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Mesmo recorte temporal da Q46, somando LEITOS_SUS. A unidade é capacidade registrada, não ocupação nem disponibilidade em tempo real.

**Formulação original, para rastreabilidade:** Quantos desses são leitos SUS?

**SQL de referência:**

```sql
SELECT sum(LEITOS_SUS) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[352171]]
```

### Q48

**Pergunta avaliada:** Qual o percentual da soma de LEITOS_SUS sobre a soma de LEITOS_EXISTENTES na maior COMP global de leitos? Nulo se denominador zero.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Razão das somas LEITOS_SUS/LEITOS_EXISTENTES na mesma competência, multiplicada por 100, com NULLIF. Não é média simples de percentuais por estabelecimento.

**Formulação original, para rastreabilidade:** Qual é a proporção de leitos SUS em relação ao total (% de cobertura pública)?

**SQL de referência:**

```sql
SELECT 100.0 * sum(LEITOS_SUS) / nullIf(sum(LEITOS_EXISTENTES),0) AS percentual FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `percentual`.

**Amostra do resultado:**

```json
[[67.6511663199307]]
```

### Q49

**Pergunta avaliada:** Qual UF não vazia tem a maior soma de LEITOS_EXISTENTES na maior COMP global de leitos? Inclua UFs com total zero. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Agrega LEITOS_EXISTENTES por UF não vazia na maior COMP global, incluindo totais zero, e retorna todos os máximos. A busca do máximo ocorre depois da soma por UF.

**Formulação original, para rastreabilidade:** Qual estado possui maior capacidade absoluta de leitos?

**SQL de referência:**

```sql
WITH grouped AS (SELECT UF AS uf, sum(LEITOS_EXISTENTES) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND UF != '' GROUP BY UF) SELECT uf,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `uf, total`.

**Amostra do resultado:**

```json
[["SP", 109724]]
```

### Q50

**Pergunta avaliada:** Qual a soma de LEITOS_EXISTENTES por UF não vazia na maior COMP global? Retorne todas as UFs presentes.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Soma por UF não vazia na maior COMP global e mantém todos os grupos presentes. Não seleciona somente um ranking parcial.

**Formulação original, para rastreabilidade:** Qual é a quantidade de leitos existentes por estado na competência mais recente?

**SQL de referência:**

```sql
SELECT UF AS uf, sum(LEITOS_EXISTENTES) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND UF != '' GROUP BY UF
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 27 linha(s), 2 coluna(s): `uf, total`.

**Amostra do resultado:**

```json
[["RJ", 44013], ["DF", 10222]]
```

### Q51

**Pergunta avaliada:** Qual a soma de UTI_TOTAL_EXIST na tabela leitos na maior competência COMP global disponível? Conte leitos registrados, não vagas livres.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Soma UTI_TOTAL_EXIST na maior COMP global. Não reconstrói o total somando subtipos, evitando presumir que a lista de subtipos seja completa ou disjunta.

**Formulação original, para rastreabilidade:** Quantos leitos de UTI estão disponíveis no Brasil no total?

**SQL de referência:**

```sql
SELECT sum(UTI_TOTAL_EXIST) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[63986]]
```

### Q52

**Pergunta avaliada:** Qual o percentual da soma de UTI_TOTAL_EXIST sobre a soma de LEITOS_EXISTENTES na maior COMP global de leitos? Nulo se denominador zero.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Percentual da soma de UTI_TOTAL_EXIST sobre LEITOS_EXISTENTES na mesma competência, com denominador protegido. Responde ao indicador literal solicitado; a interpretação de que UTI seja subconjunto do total exige o dicionário da fonte.

**Formulação original, para rastreabilidade:** Qual é a proporção de leitos de UTI em relação aos leitos totais?

**SQL de referência:**

```sql
SELECT 100.0 * sum(UTI_TOTAL_EXIST) / nullIf(sum(LEITOS_EXISTENTES),0) AS percentual FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `percentual`.

**Amostra do resultado:**

```json
[[12.291550207561341]]
```

### Q53

**Pergunta avaliada:** Qual DS_TIPO_UNIDADE não vazio tem maior soma de LEITOS_EXISTENTES na maior COMP global? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: tipo,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Soma capacidade por DS_TIPO_UNIDADE não vazio na competência mais recente e seleciona todos os máximos. Não confunde maior número de estabelecimentos com maior número de leitos.

**Formulação original, para rastreabilidade:** Qual tipo de unidade (Hospital Geral, Pronto Socorro, etc) possui maior volume de leitos?

**SQL de referência:**

```sql
WITH grouped AS (SELECT DS_TIPO_UNIDADE AS tipo, sum(LEITOS_EXISTENTES) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND DS_TIPO_UNIDADE != '' GROUP BY tipo) SELECT tipo,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `tipo, total`.

**Amostra do resultado:**

```json
[["HOSPITAL GERAL", 439673]]
```

### Q54

**Pergunta avaliada:** Retorne uma linha com as somas de UTI_ADULTO_EXIST, UTI_PEDIATRICO_EXIST, UTI_NEONATAL_EXIST, UTI_CORONARIANA_EXIST e UTI_QUEIMADO_EXIST nessa ordem, na maior COMP global de leitos.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Retorna uma única linha com as cinco somas na ordem exigida: adulto, pediátrico, neonatal, coronariana e queimado. Todas usam a mesma maior COMP global.

**Formulação original, para rastreabilidade:** Qual é a distribuição de especialidades de UTI (Adulto, Pediátrica, Neonatal, Coronariana, Queimados)?

**SQL de referência:**

```sql
SELECT sum(UTI_ADULTO_EXIST) AS UTI_ADULTO_EXIST, sum(UTI_PEDIATRICO_EXIST) AS UTI_PEDIATRICO_EXIST, sum(UTI_NEONATAL_EXIST) AS UTI_NEONATAL_EXIST, sum(UTI_CORONARIANA_EXIST) AS UTI_CORONARIANA_EXIST, sum(UTI_QUEIMADO_EXIST) AS UTI_QUEIMADO_EXIST FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 5 coluna(s): `UTI_ADULTO_EXIST, UTI_PEDIATRICO_EXIST, UTI_NEONATAL_EXIST, UTI_CORONARIANA_EXIST, UTI_QUEIMADO_EXIST`.

**Amostra do resultado:**

```json
[[44079, 7554, 9962, 2141, 250]]
```

### Q55

**Pergunta avaliada:** Qual UF não vazia tem a menor soma de UTI_NEONATAL_EXIST na maior COMP global de leitos? Inclua UFs com total zero. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Soma UTI neonatal por UF não vazia e seleciona todos os mínimos, preservando UFs com total zero. Considera UFs presentes nessa competência, não uma lista externa de estados ausentes da base.

**Formulação original, para rastreabilidade:** Qual estado tem a menor quantidade absoluta de leitos de UTI neonatal na competência mais recente?

**SQL de referência:**

```sql
WITH grouped AS (SELECT UF AS uf, sum(UTI_NEONATAL_EXIST) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND UF != '' GROUP BY UF) SELECT uf,total FROM grouped WHERE total = (SELECT min(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `uf, total`.

**Amostra do resultado:**

```json
[["RR", 25]]
```

### Q56

**Pergunta avaliada:** Qual código TP_GESTAO não vazio reúne mais CNES distintos não vazios na maior COMP global de leitos? Retorne o código, sem classificá-lo como público, privado ou filantrópico. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: gestao,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Conta CNES distintos não vazios por TP_GESTAO não vazio na maior COMP e retorna todos os máximos. Não trata gestão como natureza jurídica. A referência responde ao enunciado revisado sobre códigos, não à formulação original público/privado/filantrópico.

**Formulação original, para rastreabilidade:** Qual é o tipo de gestão predominante (Pública, Privada, Filantrópica) nas unidades de saúde?

**SQL de referência:**

```sql
WITH grouped AS (SELECT TP_GESTAO AS gestao, uniqExact(CNES) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND TP_GESTAO != '' AND CNES != '' GROUP BY gestao) SELECT gestao,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `gestao, total`.

**Amostra do resultado:**

```json
[["M", 5243]]
```

### Q57

**Pergunta avaliada:** Qual a soma de LEITOS_SUS, na maior COMP global de leitos, em linhas cujo código NATUREZA_JURIDICA, após remover espaços externos, começa com '2' ou '3'? Não use TP_GESTAO para esse filtro.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Aplica trimBoth e prefixo 2 ou 3 em NATUREZA_JURIDICA, sob o filtro da maior COMP global, e soma LEITOS_SUS. O OR está agrupado, portanto o filtro temporal vale para ambos os prefixos. Aderente ao filtro técnico explícito; não certifica por si só a interpretação institucional de setor privado.

**Formulação original, para rastreabilidade:** Quantos leitos SUS existem em estabelecimentos da iniciativa privada (parcerias)?

**SQL de referência:**

```sql
SELECT sum(LEITOS_SUS) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND (startsWith(trimBoth(NATUREZA_JURIDICA),'2') OR startsWith(trimBoth(NATUREZA_JURIDICA),'3'))
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[158775]]
```

### Q58

**Pergunta avaliada:** Qual UF não vazia tem maior percentual da soma de LEITOS_SUS sobre LEITOS_EXISTENTES na maior COMP global? Exclua denominadores zero. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,percentual.

**Parecer:** Aderente com ressalva de escopo a explicitar.

Calcula a razão das somas por UF e seleciona os maiores percentuais. A ressalva é HAVING sum(LEITOS_EXISTENTES) > 0: o enunciado diz excluir denominadores zero, o que literalmente permitiria negativos. Nos dados atuais não há leitos negativos, portanto o resultado coincide. Para um contrato geral, explicitar denominadores positivos ou usar != 0, conforme a política de qualidade adotada.

**Formulação original, para rastreabilidade:** Qual estado tem o maior percentual de leitos SUS em relação ao total (maior compromisso público)?

**SQL de referência:**

```sql
WITH grouped AS (SELECT UF AS uf, 100.0 * sum(LEITOS_SUS) / sum(LEITOS_EXISTENTES) AS percentual FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND UF != '' GROUP BY UF HAVING sum(LEITOS_EXISTENTES) > 0) SELECT uf,percentual FROM grouped WHERE percentual = (SELECT max(percentual) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 2 coluna(s): `uf, percentual`.

**Amostra do resultado:**

```json
[["AC", 89.92999461497038]]
```

### Q59

**Pergunta avaliada:** Retorne REGIAO, soma de LEITOS_EXISTENTES e soma de LEITOS_SUS para todas as regiões não vazias na maior COMP global de leitos.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Agrupa REGIAO não vazia na maior COMP e retorna as duas somas, existentes e SUS, na ordem contratada. Não converte região em UF nem calcula percentuais adicionais.

**Formulação original, para rastreabilidade:** Qual é a distribuição de capacidade de leitos entre regiões (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)?

**SQL de referência:**

```sql
SELECT REGIAO AS regiao, sum(LEITOS_EXISTENTES) AS existentes, sum(LEITOS_SUS) AS sus FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND REGIAO != '' GROUP BY REGIAO
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 5 linha(s), 3 coluna(s): `regiao, existentes, sus`.

**Amostra do resultado:**

```json
[["NORDESTE", 137529, 106772], ["NORTE", 40336, 31307]]
```

### Q60

**Pergunta avaliada:** Qual combinação de UF e código CO_IBGE não vazios tem maior soma de LEITOS_EXISTENTES na maior COMP global? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,municipio,total.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Agrupa UF e código CO_IBGE não vazios antes de somar leitos e selecionar o máximo. Inclui empates e não substitui o código por nome de município. A filtragem temporal é global.

**Formulação original, para rastreabilidade:** Qual município possui maior quantidade absoluta de leitos existentes na competência mais recente?

**SQL de referência:**

```sql
WITH grouped AS (SELECT UF AS uf, CO_IBGE AS municipio, sum(LEITOS_EXISTENTES) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND UF != '' AND CO_IBGE != '' GROUP BY UF,CO_IBGE) SELECT uf,municipio,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 3 coluna(s): `uf, municipio, total`.

**Amostra do resultado:**

```json
[["SP", "355030", 36872]]
```

### Q61

**Pergunta avaliada:** Quantos códigos positivos de município de notificação de SRAG também aparecem na base UBS com CNES positivo? Conte municípios distintos por igualdade dos códigos.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Forma dois conjuntos de municípios positivos distintos, exigindo CNES positivo em UBS, e conta sua interseção. Cada município entra uma vez, sem multiplicação por notificações ou unidades. Ambos os códigos são inteiros no banco, e a pergunta define igualdade de códigos.

**Formulação original, para rastreabilidade:** Em quantos municípios há notificações de SRAG e também UBS cadastradas?

**SQL de referência:**

```sql
SELECT count() AS total FROM (SELECT DISTINCT co_mun_not AS municipio FROM srag WHERE co_mun_not > 0) s INNER JOIN (SELECT DISTINCT ibge AS municipio FROM atencao_basica WHERE ibge > 0 AND cnes > 0) u ON s.municipio = u.municipio
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1 linha(s), 1 coluna(s): `total`.

**Amostra do resultado:**

```json
[[1198]]
```

### Q62

**Pergunta avaliada:** Liste todos os municípios positivos presentes em SRAG e UBS, com número de linhas de notificações e número de CNES distintos positivos. Ordene por notificações decrescentes e código municipal crescente, sem limitar a quantidade de linhas.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Conta notificações por município e CNES distintos positivos por município separadamente antes do INNER JOIN. Retorna somente municípios comuns; ordena notificações decrescentes e código crescente, sem LIMIT. A ordem é parte explícita da pergunta e do comparador.

**Formulação original, para rastreabilidade:** Quais municípios possuem maior número de notificações de SRAG e quantas UBS existem em cada um?

**SQL de referência:**

```sql
WITH s AS (SELECT co_mun_not AS municipio, count() AS notificacoes FROM srag WHERE co_mun_not > 0 GROUP BY municipio), u AS (SELECT ibge AS municipio, uniqExact(cnes) AS ubs FROM atencao_basica WHERE ibge > 0 AND cnes > 0 GROUP BY municipio) SELECT s.municipio, s.notificacoes, u.ubs FROM s INNER JOIN u ON s.municipio=u.municipio ORDER BY s.notificacoes DESC,s.municipio ASC
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 1198 linha(s), 3 coluna(s): `municipio, notificacoes, ubs`.

**Amostra do resultado:**

```json
[[355030, 4517, 645], [530010, 3976, 210]]
```

### Q63

**Pergunta avaliada:** Para todas as UFs não vazias comuns à vacinação e aos leitos, retorne UF, contagem de registros por UF de residência em toda a vacinação carregada e soma de UTI_TOTAL_EXIST na maior COMP global dos leitos. Inclua somente UFs com soma de UTI positiva; agregue antes de juntar.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Agrega vacinação inteira por UF de residência; agrega leitos na maior COMP global, excluindo UFs vazias e soma de UTI não positiva; junta os resultados por UF. Evita multiplicação de registros. Responde a uma comparação descritiva entre recortes, não a cobertura vacinal, correlação causal ou períodos harmonizados.

**Formulação original, para rastreabilidade:** Quais estados possuem simultaneamente registros de vacinação contra a COVID-19 e leitos de UTI na competência mais recente, e quais são os respectivos totais?

**SQL de referência:**

```sql
WITH v AS (SELECT paciente_endereco_uf AS uf, count() AS doses FROM vacinacao WHERE paciente_endereco_uf != '' GROUP BY uf), b AS (SELECT UF AS uf, sum(UTI_TOTAL_EXIST) AS leitos FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND UF != '' GROUP BY UF HAVING sum(UTI_TOTAL_EXIST)>0) SELECT v.uf,v.doses,b.leitos FROM v INNER JOIN b ON v.uf=b.uf
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 27 linha(s), 3 coluna(s): `uf, doses, leitos`.

**Amostra do resultado:**

```json
[["RJ", 424, 8319], ["DF", 184, 2051]]
```

### Q64

**Pergunta avaliada:** Para todas as UFs não vazias comuns à vacinação e aos leitos, retorne UF, contagem de registros por UF de residência em toda a vacinação carregada e soma de UTI_TOTAL_EXIST na maior COMP global dos leitos. Inclua somente UFs com soma de UTI positiva; agregue antes de juntar.

**Parecer:** Aderente ao enunciado operacional atual; observar notas.

Idêntica à Q63 em enunciado e SQL. A referência é aderente à tarefa explicitada, mas a repetição não constitui uma segunda tarefa independente.

**Formulação original, para rastreabilidade:** Compare o número de doses registradas contra a COVID-19 com a quantidade de leitos de UTI por estado.

**SQL de referência:**

```sql
WITH v AS (SELECT paciente_endereco_uf AS uf, count() AS doses FROM vacinacao WHERE paciente_endereco_uf != '' GROUP BY uf), b AS (SELECT UF AS uf, sum(UTI_TOTAL_EXIST) AS leitos FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND UF != '' GROUP BY UF HAVING sum(UTI_TOTAL_EXIST)>0) SELECT v.uf,v.doses,b.leitos FROM v INNER JOIN b ON v.uf=b.uf
```

**Conferência:** consulta executada; resultado preservado e recálculo Python coincidentes. 27 linha(s), 3 coluna(s): `uf, doses, leitos`.

**Amostra do resultado:**

```json
[["RJ", 424, 8319], ["DF", 184, 2051]]
```

### Q65

**Pergunta avaliada:** Qual é a quantidade de leitos de UTI SUS nos estados com maior número de notificações de SRAG?

**Parecer:** Limitação de implementação; sem gabarito numérico.

Não existe SQL de referência. O comportamento esperado é informar ausência de relacionamento SRAG–leitos na configuração atual. As bases podem permitir construir uma análise após implementação e definição de período; isto é limitação do sistema, não impossibilidade intrínseca dos dados.

**Bases esperadas:** surtos-srag, leitos. **SQL:** ausente por definição. A configuração de relacionamentos foi inspecionada; não houve nova chamada à LLM para essas quatro fichas nesta revisão.

### Q66

**Pergunta avaliada:** Qual estado teve mais hospitalizações por SRAG e qual era sua quantidade de leitos existentes na competência mais recente?

**Parecer:** Limitação de implementação; sem gabarito numérico.

Não existe SQL de referência. A consulta exigiria agregar hospitalizações SRAG por estado e associar capacidade na competência mais recente; essa relação não está cadastrada. A recusa prevista é um teste operacional, não um gabarito numérico.

**Bases esperadas:** surtos-srag, leitos. **SQL:** ausente por definição. A configuração de relacionamentos foi inspecionada; não houve nova chamada à LLM para essas quatro fichas nesta revisão.

### Q67

**Pergunta avaliada:** Qual é a relação entre quantidade de UBS e número de registros de vacinação contra a COVID-19 por estado?

**Parecer:** Limitação de implementação; sem gabarito numérico.

Não existe SQL de referência. A relação UBS–vacinação por UF não está cadastrada; a UF de UBS é numérica e a de vacinação é sigla, exigindo harmonização. O termo 'relação' também precisaria definir o indicador pretendido para uma referência numérica.

**Bases esperadas:** atencao-basica, covid-19-vacinacao. **SQL:** ausente por definição. A configuração de relacionamentos foi inspecionada; não houve nova chamada à LLM para essas quatro fichas nesta revisão.

### Q68

**Pergunta avaliada:** Quais municípios combinam alto número de notificações de SRAG, UBS cadastradas e baixa disponibilidade de leitos?

**Parecer:** Limitação de implementação; sem gabarito numérico.

Não existe SQL de referência. SRAG–UBS tem relação cadastrada, mas não há caminho autorizado que integre leitos aos outros dois nesse conjunto. Além disso, 'alto' e 'baixo' precisam de limiares, e 'disponibilidade' não pode ser presumida como vagas livres. A limitação controlada é apropriada à implementação atual.

**Bases esperadas:** surtos-srag, atencao-basica, leitos. **SQL:** ausente por definição. A configuração de relacionamentos foi inspecionada; não houve nova chamada à LLM para essas quatro fichas nesta revisão.

## Encaminhamento

O autor pode usar estas fichas para conferir e assumir a especificação de cada referência. Antes de registrar a revisão humana, resolver as redações de Q25/Q58, aceitar explicitamente as regras de comparação e documentar as limitações indicadas. Uma mudança de pergunta, SQL ou política de comparação deve produzir uma versão nova do catálogo e um novo pacote preparado, preservando a história. Se o texto enviado ao modelo mudar, a execução anterior não deve ser renomeada como se tivesse usado a nova pergunta.

Não há evidência nesta conferência para atribuir os erros da última rodada a valores numéricos incorretos dos gabaritos nos dados atuais. Isso não equivale a garantia de que o catálogo não possui outras ambiguidades, nem a validação de utilidade em saúde pública. O parecer é uma revisão técnica de correspondência pergunta–consulta e de cálculo, com as ressalvas identificadas acima.
