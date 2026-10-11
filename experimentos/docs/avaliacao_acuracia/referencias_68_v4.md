# Referências propostas — protocolo v4

Q25 e Q58 tiveram os enunciados explicitados. SQLs e regras de comparação permanecem iguais ao v3. Revisão humana pendente.

## Q1

Quantas doses de vacina contra a COVID-19 foram registradas no conjunto de dados carregado?

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT count() AS total FROM vacinacao
```

## Q2

Qual UF de residência não vazia tem mais registros de primeira dose ('1ª Dose') no recorte? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

Colunas: uf, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT paciente_endereco_uf AS uf, count() AS total FROM vacinacao WHERE paciente_endereco_uf != '' AND vacina_descricao_dose = '1ª Dose' GROUP BY uf) SELECT uf,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q3

Quantos registros têm vacina_descricao_dose igual a '2ª Dose' na base carregada?

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT countIf(vacina_descricao_dose = '2ª Dose') AS total FROM vacinacao
```

## Q4

Por UF de residência não vazia, qual a diferença entre registros de '1ª Dose' e '2ª Dose'? Retorne UF e diferença, incluindo todas as UFs presentes.

Colunas: uf, diferenca

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT paciente_endereco_uf AS uf, toInt64(countIf(vacina_descricao_dose = '1ª Dose')) - toInt64(countIf(vacina_descricao_dose = '2ª Dose')) AS diferenca FROM vacinacao WHERE paciente_endereco_uf != '' GROUP BY uf
```

## Q5

Qual a razão entre o número de registros cuja descrição da dose contém 'reforço' (sem distinguir maiúsculas) e os de '1ª Dose'? Retorne apenas a razão, não percentual; nulo se denominador zero. Retorne a razão com pelo menos seis casas decimais.

Colunas: razao

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {"0": {"absolute_tolerance": 1e-06}}}`

```sql
SELECT countIf(positionCaseInsensitiveUTF8(ifNull(vacina_descricao_dose,''), 'reforço') > 0) / nullIf(countIf(vacina_descricao_dose = '1ª Dose'),0) AS razao FROM vacinacao
```

## Q6

Qual o percentual de registros F e de registros M no campo paciente_enumSexoBiologico, usando somente F e M no denominador? Retorne as duas categorias e percentuais, nulo se não houver F/M.

Colunas: sexo, percentual

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {"1": {"absolute_tolerance": 0.005}}}`

```sql
SELECT 'F' AS sexo, 100.0 * countIf(paciente_enumSexoBiologico = 'F') / nullIf(countIf(paciente_enumSexoBiologico IN ('F','M')),0) AS percentual FROM vacinacao UNION ALL SELECT 'M' AS sexo, 100.0 * countIf(paciente_enumSexoBiologico = 'M') / nullIf(countIf(paciente_enumSexoBiologico IN ('F','M')),0) AS percentual FROM vacinacao
```

## Q7

Entre faixas etárias presentes 0-18, 19-59 e 60+ anos, excluindo idades negativas, qual tem menos registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: faixa,total.

Colunas: faixa, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT multiIf(paciente_idade < 0, 'ignorada', paciente_idade <= 18, '0-18', paciente_idade <= 59, '19-59', '60+') AS faixa, count() AS total FROM vacinacao WHERE paciente_idade >= 0 GROUP BY faixa) SELECT faixa,total FROM grouped WHERE total = (SELECT min(total) FROM grouped)
```

## Q8

Quais municípios de residência (UF e código IBGE não vazios) têm a maior contagem de registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,municipio,total.

Colunas: uf, municipio, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT paciente_endereco_uf AS uf, paciente_endereco_coIbgeMunicipio AS municipio, count() AS total FROM vacinacao WHERE paciente_endereco_uf != '' AND notEmpty(ifNull(paciente_endereco_coIbgeMunicipio,'')) GROUP BY uf,municipio) SELECT uf,municipio,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q9

Qual a contagem de registros de vacinação por UF de residência não vazia e faixas 0-18, 19-59 e 60+ anos? Exclua idades negativas; retorne todos os grupos presentes, UF, faixa e total. Não conte pessoas distintas.

Colunas: uf, faixa, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT paciente_endereco_uf AS uf, multiIf(paciente_idade < 0, 'ignorada', paciente_idade <= 18, '0-18', paciente_idade <= 59, '19-59', '60+') AS faixa, count() AS total FROM vacinacao WHERE paciente_endereco_uf != '' AND paciente_idade >= 0 GROUP BY uf,faixa
```

## Q10

Qual a contagem de registros de vacinação por sistema_origem? Retorne todos os grupos; mantenha nulos como nulos.

Colunas: sistema_origem, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT sistema_origem, count() AS total FROM vacinacao GROUP BY sistema_origem
```

## Q11

Qual vacina_nome não vazio tem mais registros e qual o percentual desses registros sobre todas as linhas de vacinação? Retorne nome e percentual. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: vacina,percentual.

Colunas: vacina, percentual

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {"1": {"absolute_tolerance": 0.005}}}`

```sql
WITH grouped AS (SELECT vacina_nome AS vacina, 100.0 * count() / nullIf((SELECT count() FROM vacinacao),0) AS percentual FROM vacinacao WHERE notEmpty(ifNull(vacina_nome,'')) GROUP BY vacina) SELECT vacina,percentual FROM grouped WHERE percentual = (SELECT max(percentual) FROM grouped)
```

## Q12

Qual fabricante não vazio tem mais registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: fabricante,total.

Colunas: fabricante, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT vacina_fabricante_nome AS fabricante, count() AS total FROM vacinacao WHERE notEmpty(ifNull(vacina_fabricante_nome,'')) GROUP BY fabricante) SELECT fabricante,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q13

Qual a contagem de registros de vacinação por ano e mês de aplicação? Retorne mes no formato AAAA-MM e total de todos os meses presentes; exclua datas nulas.

Colunas: mes, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT formatDateTime(vacina_dataAplicacao,'%Y-%m') AS mes, count() AS total FROM vacinacao WHERE vacina_dataAplicacao IS NOT NULL GROUP BY mes
```

## Q14

Qual combinação de UF de residência não vazia e mês de aplicação (AAAA-MM) tem mais registros de vacinação? Exclua datas nulas. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,mes,total.

Colunas: uf, mes, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT paciente_endereco_uf AS uf, formatDateTime(vacina_dataAplicacao,'%Y-%m') AS mes, count() AS total FROM vacinacao WHERE paciente_endereco_uf != '' AND vacina_dataAplicacao IS NOT NULL GROUP BY uf,mes) SELECT uf,mes,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q15

Quantos registros existem por descrição de dose que contenha 'reforço', sem distinguir maiúsculas? Preserve a descrição original e retorne todos os grupos.

Colunas: dose, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT vacina_descricao_dose AS dose, count() AS total FROM vacinacao WHERE positionCaseInsensitiveUTF8(ifNull(vacina_descricao_dose,''), 'reforço') > 0 GROUP BY dose
```

## Q16

Quantas UBS distintas estão cadastradas na base carregada, contando CNES positivos? Não inferir situação ativa.

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0
```

## Q17

Qual a contagem de CNES distintos positivos de UBS por código de UF não vazio? Retorne todos os grupos presentes.

Colunas: uf, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT uf, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND toString(uf) != '' GROUP BY uf
```

## Q26

Qual a contagem de CNES distintos positivos de UBS por código de UF não vazio? Retorne todos os grupos presentes.

Colunas: uf, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT uf, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND toString(uf) != '' GROUP BY uf
```

## Q18

Qual código de UF não vazio tem mais UBS distintas (CNES positivos)? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

Colunas: uf, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT uf, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND toString(uf) != '' GROUP BY uf) SELECT uf,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q27

Qual código de UF não vazio tem mais UBS distintas (CNES positivos)? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

Colunas: uf, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT uf, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND toString(uf) != '' GROUP BY uf) SELECT uf,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q19

Quantos códigos de município positivos possuem pelo menos um CNES positivo na base de UBS?

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT uniqExact(ibge) AS total FROM atencao_basica WHERE cnes > 0 AND ibge > 0
```

## Q20

Quais códigos de município positivos têm mais UBS distintas, contando CNES positivos nos municípios presentes na base? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: municipio,total.

Colunas: municipio, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT ibge AS municipio, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND ibge > 0 GROUP BY municipio) SELECT municipio,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q21

Quais códigos de município positivos têm mais UBS distintas, contando CNES positivos nos municípios presentes na base? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: municipio,total.

Colunas: municipio, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT ibge AS municipio, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND ibge > 0 GROUP BY municipio) SELECT municipio,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q30

Quais códigos de município positivos têm menos UBS distintas, contando CNES positivos nos municípios presentes na base? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: municipio,total.

Colunas: municipio, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT ibge AS municipio, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND ibge > 0 GROUP BY municipio) SELECT municipio,total FROM grouped WHERE total = (SELECT min(total) FROM grouped)
```

## Q22

Na base de UBS, qual a contagem de CNES distintos positivos por município positivo nas UFs de códigos 21 a 29 (Nordeste)? Retorne todos os municípios, código e total.

Colunas: municipio, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT ibge AS municipio, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND ibge > 0 AND uf IN ('21','22','23','24','25','26','27','28','29') GROUP BY municipio
```

## Q23

Quantas UBS distintas (CNES positivos) têm latitude e longitude não zero e dentro de [-90,90] e [-180,180]?

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND latitude != 0 AND longitude != 0 AND latitude BETWEEN -90 AND 90 AND longitude BETWEEN -180 AND 180
```

## Q24

Quais municípios positivos têm mais UBS distintas com CNES positivo e coordenadas não zero nos intervalos latitude [-90,90] e longitude [-180,180]? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: municipio,total.

Colunas: municipio, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT ibge AS municipio, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND ibge > 0 AND latitude != 0 AND longitude != 0 AND latitude BETWEEN -90 AND 90 AND longitude BETWEEN -180 AND 180 GROUP BY municipio) SELECT municipio,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q25

Qual a contagem de CNES distintos positivos por UF não vazia, código de município positivo e bairro não vazio após remover espaços nas extremidades, na base UBS? Preserve o nome original do bairro no agrupamento. Retorne todos os grupos; não una bairros homônimos de municípios diferentes.

Colunas: uf, municipio, bairro, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT uf, ibge AS municipio, bairro, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND toString(uf) != '' AND ibge > 0 AND trimBoth(bairro) != '' GROUP BY uf,municipio,bairro
```

## Q28

Quantas UBS distintas com CNES positivo possuem logradouro e bairro não vazios após remover espaços nas extremidades?

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND trimBoth(logradouro) != '' AND trimBoth(bairro) != ''
```

## Q29

Qual a contagem de UBS distintas com CNES positivo por bairro no município IBGE 355030? Inclua todos os grupos, inclusive bairro vazio.

Colunas: bairro, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT bairro, uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0 AND ibge = 355030 GROUP BY bairro
```

## Q31

Quantas linhas de notificações existem na tabela SRAG carregada, sem filtrar classificação final?

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT count() AS total FROM srag
```

## Q32

Qual a contagem de linhas de SRAG por ano de dt_notific e sem_not, excluindo dt_notific = '1970-01-01'? Retorne todos os grupos.

Colunas: ano, semana, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {"0": {"normalization": "year"}}}`

```sql
SELECT toYear(dt_notific) AS ano, sem_not AS semana, count() AS total FROM srag WHERE dt_notific != toDate('1970-01-01') GROUP BY ano,semana
```

## Q33

Qual UF de notificação não vazia tem mais linhas de SRAG na base carregada? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

Colunas: uf, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT sg_uf_not AS uf, count() AS total FROM srag WHERE sg_uf_not != '' GROUP BY uf) SELECT uf,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q34

Qual a contagem de linhas de SRAG por UF de notificação não vazia? Retorne todas as UFs presentes.

Colunas: uf, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT sg_uf_not AS uf, count() AS total FROM srag WHERE sg_uf_not != '' GROUP BY uf
```

## Q35

Quantos códigos de município de notificação positivos distintos existem nas linhas de SRAG?

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT uniqExact(co_mun_not) AS total FROM srag WHERE co_mun_not > 0
```

## Q36

Qual o percentual de linhas de SRAG com hospital = 1 entre todas as linhas? Retorne nulo se o denominador for zero.

Colunas: percentual

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {"0": {"absolute_tolerance": 0.005}}}`

```sql
SELECT 100.0 * countIf(hospital = 1) / nullIf(count(),0) AS percentual FROM srag
```

## Q38

Qual o percentual de linhas de SRAG com evolucao = 2 entre as linhas com hospital = 1? Retorne nulo se o denominador for zero.

Colunas: percentual

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {"0": {"absolute_tolerance": 0.005}}}`

```sql
SELECT 100.0 * countIf(evolucao = 2 AND hospital = 1) / nullIf(countIf(hospital = 1),0) AS percentual FROM srag
```

## Q39

Qual o percentual de linhas de SRAG com uti = 1 entre todas as linhas? Retorne nulo se o denominador for zero.

Colunas: percentual

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {"0": {"absolute_tolerance": 0.005}}}`

```sql
SELECT 100.0 * countIf(uti = 1) / nullIf(count(),0) AS percentual FROM srag
```

## Q37

Quantas linhas de SRAG possuem evolucao = 2?

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT countIf(evolucao = 2) AS total FROM srag
```

## Q40

Qual UF de notificação não vazia tem maior percentual de linhas com evolucao = 2, usando todas as linhas daquela UF no denominador? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,percentual.

Colunas: uf, percentual

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {"1": {"absolute_tolerance": 0.005}}}`

```sql
WITH grouped AS (SELECT sg_uf_not AS uf, 100.0 * countIf(evolucao = 2) / count() AS percentual FROM srag WHERE sg_uf_not != '' GROUP BY uf) SELECT uf,percentual FROM grouped WHERE percentual = (SELECT max(percentual) FROM grouped)
```

## Q41

Retorne uma linha com as contagens de SRAG em que cada indicador vale 1, na ordem febre, tosse, garganta, dispneia, diarreia e vomito. Uma notificação pode contribuir para vários sintomas.

Colunas: febre, tosse, garganta, dispneia, diarreia, vomito

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT countIf(febre = 1) AS febre, countIf(tosse = 1) AS tosse, countIf(garganta = 1) AS garganta, countIf(dispneia = 1) AS dispneia, countIf(diarreia = 1) AS diarreia, countIf(vomito = 1) AS vomito FROM srag
```

## Q42

Qual faixa tem mais linhas de SRAG: 0-18, 19-59 ou 60+ anos? Use nu_idade_n como magnitude da idade e tp_idade 1=dias, 2=meses e 3=anos; exclua idade nula, negativa e unidades desconhecidas. Para este teste, converta dias dividindo por 365.25 e meses por 12; anos permanecem iguais. Use os intervalos [0,19), [19,60) e [60,infinito), com rótulos '0-18', '19-59' e '60+'. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: faixa,total.

Colunas: faixa, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT multiIf((multiIf(tp_idade = 1, nu_idade_n / 365.25, tp_idade = 2, nu_idade_n / 12.0, toFloat64(nu_idade_n))) < 19, '0-18', (multiIf(tp_idade = 1, nu_idade_n / 365.25, tp_idade = 2, nu_idade_n / 12.0, toFloat64(nu_idade_n))) < 60, '19-59', '60+') AS faixa, count() AS total FROM srag WHERE tp_idade IN (1,2,3) AND nu_idade_n IS NOT NULL AND nu_idade_n >= 0 GROUP BY faixa) SELECT faixa,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q43

Qual o percentual de linhas de SRAG com ao menos um dos indicadores cardiopati, hematologi, hepatica, asma, diabetes, neurologic, pneumopati, imunodepre, renal ou obesidade igual a 1, sobre todas as linhas? Nulo se não houver linhas.

Colunas: percentual

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {"0": {"absolute_tolerance": 0.005}}}`

```sql
SELECT 100.0 * countIf(cardiopati = 1 OR hematologi = 1 OR hepatica = 1 OR asma = 1 OR diabetes = 1 OR neurologic = 1 OR pneumopati = 1 OR imunodepre = 1 OR renal = 1 OR obesidade = 1) / nullIf(count(),0) AS percentual FROM srag
```

## Q44

Quantas linhas de SRAG têm pcr_sars2 = 1 ou pos_pcrflu = 1? Conte cada linha apenas uma vez.

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT countIf(pcr_sars2 = 1 OR pos_pcrflu = 1) AS total FROM srag
```

## Q45

Entre os indicadores pcr_sars2, pos_pcrflu e pcr_vsr, qual possui mais linhas de SRAG com valor 1? Retorne o nome do indicador e a contagem. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: agente,total.

Colunas: agente, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {"0": {"normalization": "casefold"}}}`

```sql
WITH grouped AS (SELECT 'pcr_sars2' AS agente, countIf(pcr_sars2 = 1) AS total FROM srag UNION ALL SELECT 'pos_pcrflu' AS agente, countIf(pos_pcrflu = 1) AS total FROM srag UNION ALL SELECT 'pcr_vsr' AS agente, countIf(pcr_vsr = 1) AS total FROM srag) SELECT agente,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q46

Qual a soma de LEITOS_EXISTENTES na tabela leitos na maior competência COMP global disponível? Conte leitos registrados, não vagas livres.

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT sum(LEITOS_EXISTENTES) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos)
```

## Q47

Qual a soma de LEITOS_SUS na tabela leitos na maior competência COMP global disponível? Conte leitos registrados, não vagas livres.

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT sum(LEITOS_SUS) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos)
```

## Q51

Qual a soma de UTI_TOTAL_EXIST na tabela leitos na maior competência COMP global disponível? Conte leitos registrados, não vagas livres.

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT sum(UTI_TOTAL_EXIST) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos)
```

## Q48

Qual o percentual da soma de LEITOS_SUS sobre a soma de LEITOS_EXISTENTES na maior COMP global de leitos? Nulo se denominador zero.

Colunas: percentual

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {"0": {"absolute_tolerance": 0.005}}}`

```sql
SELECT 100.0 * sum(LEITOS_SUS) / nullIf(sum(LEITOS_EXISTENTES),0) AS percentual FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos)
```

## Q52

Qual o percentual da soma de UTI_TOTAL_EXIST sobre a soma de LEITOS_EXISTENTES na maior COMP global de leitos? Nulo se denominador zero.

Colunas: percentual

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {"0": {"absolute_tolerance": 0.005}}}`

```sql
SELECT 100.0 * sum(UTI_TOTAL_EXIST) / nullIf(sum(LEITOS_EXISTENTES),0) AS percentual FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos)
```

## Q49

Qual UF não vazia tem a maior soma de LEITOS_EXISTENTES na maior COMP global de leitos? Inclua UFs com total zero. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

Colunas: uf, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT UF AS uf, sum(LEITOS_EXISTENTES) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND UF != '' GROUP BY UF) SELECT uf,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q55

Qual UF não vazia tem a menor soma de UTI_NEONATAL_EXIST na maior COMP global de leitos? Inclua UFs com total zero. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

Colunas: uf, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT UF AS uf, sum(UTI_NEONATAL_EXIST) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND UF != '' GROUP BY UF) SELECT uf,total FROM grouped WHERE total = (SELECT min(total) FROM grouped)
```

## Q50

Qual a soma de LEITOS_EXISTENTES por UF não vazia na maior COMP global? Retorne todas as UFs presentes.

Colunas: uf, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT UF AS uf, sum(LEITOS_EXISTENTES) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND UF != '' GROUP BY UF
```

## Q53

Qual DS_TIPO_UNIDADE não vazio tem maior soma de LEITOS_EXISTENTES na maior COMP global? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: tipo,total.

Colunas: tipo, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT DS_TIPO_UNIDADE AS tipo, sum(LEITOS_EXISTENTES) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND DS_TIPO_UNIDADE != '' GROUP BY tipo) SELECT tipo,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q54

Retorne uma linha com as somas de UTI_ADULTO_EXIST, UTI_PEDIATRICO_EXIST, UTI_NEONATAL_EXIST, UTI_CORONARIANA_EXIST e UTI_QUEIMADO_EXIST nessa ordem, na maior COMP global de leitos.

Colunas: UTI_ADULTO_EXIST, UTI_PEDIATRICO_EXIST, UTI_NEONATAL_EXIST, UTI_CORONARIANA_EXIST, UTI_QUEIMADO_EXIST

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT sum(UTI_ADULTO_EXIST) AS UTI_ADULTO_EXIST, sum(UTI_PEDIATRICO_EXIST) AS UTI_PEDIATRICO_EXIST, sum(UTI_NEONATAL_EXIST) AS UTI_NEONATAL_EXIST, sum(UTI_CORONARIANA_EXIST) AS UTI_CORONARIANA_EXIST, sum(UTI_QUEIMADO_EXIST) AS UTI_QUEIMADO_EXIST FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos)
```

## Q56

Qual código TP_GESTAO não vazio reúne mais CNES distintos não vazios na maior COMP global de leitos? Retorne o código, sem classificá-lo como público, privado ou filantrópico. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: gestao,total.

Colunas: gestao, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT TP_GESTAO AS gestao, uniqExact(CNES) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND TP_GESTAO != '' AND CNES != '' GROUP BY gestao) SELECT gestao,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q57

Qual a soma de LEITOS_SUS, na maior COMP global de leitos, em linhas cujo código NATUREZA_JURIDICA, após remover espaços externos, começa com '2' ou '3'? Não use TP_GESTAO para esse filtro.

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT sum(LEITOS_SUS) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND (startsWith(trimBoth(NATUREZA_JURIDICA),'2') OR startsWith(trimBoth(NATUREZA_JURIDICA),'3'))
```

## Q58

Qual UF não vazia tem maior percentual da soma de LEITOS_SUS sobre LEITOS_EXISTENTES na maior COMP global? Considere somente UFs cuja soma de LEITOS_EXISTENTES seja positiva. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,percentual.

Colunas: uf, percentual

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {"1": {"absolute_tolerance": 0.005}}}`

```sql
WITH grouped AS (SELECT UF AS uf, 100.0 * sum(LEITOS_SUS) / sum(LEITOS_EXISTENTES) AS percentual FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND UF != '' GROUP BY UF HAVING sum(LEITOS_EXISTENTES) > 0) SELECT uf,percentual FROM grouped WHERE percentual = (SELECT max(percentual) FROM grouped)
```

## Q59

Retorne REGIAO, soma de LEITOS_EXISTENTES e soma de LEITOS_SUS para todas as regiões não vazias na maior COMP global de leitos.

Colunas: regiao, existentes, sus

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT REGIAO AS regiao, sum(LEITOS_EXISTENTES) AS existentes, sum(LEITOS_SUS) AS sus FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND REGIAO != '' GROUP BY REGIAO
```

## Q60

Qual combinação de UF e código CO_IBGE não vazios tem maior soma de LEITOS_EXISTENTES na maior COMP global? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,municipio,total.

Colunas: uf, municipio, total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH grouped AS (SELECT UF AS uf, CO_IBGE AS municipio, sum(LEITOS_EXISTENTES) AS total FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND UF != '' AND CO_IBGE != '' GROUP BY UF,CO_IBGE) SELECT uf,municipio,total FROM grouped WHERE total = (SELECT max(total) FROM grouped)
```

## Q61

Quantos códigos positivos de município de notificação de SRAG também aparecem na base UBS com CNES positivo? Conte municípios distintos por igualdade dos códigos.

Colunas: total

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
SELECT count() AS total FROM (SELECT DISTINCT co_mun_not AS municipio FROM srag WHERE co_mun_not > 0) s INNER JOIN (SELECT DISTINCT ibge AS municipio FROM atencao_basica WHERE ibge > 0 AND cnes > 0) u ON s.municipio = u.municipio
```

## Q62

Liste todos os municípios positivos presentes em SRAG e UBS, com número de linhas de notificações e número de CNES distintos positivos. Ordene por notificações decrescentes e código municipal crescente, sem limitar a quantidade de linhas.

Colunas: municipio, notificacoes, ubs

Revisão: draft

Comparação: `{"ordered": true, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH s AS (SELECT co_mun_not AS municipio, count() AS notificacoes FROM srag WHERE co_mun_not > 0 GROUP BY municipio), u AS (SELECT ibge AS municipio, uniqExact(cnes) AS ubs FROM atencao_basica WHERE ibge > 0 AND cnes > 0 GROUP BY municipio) SELECT s.municipio, s.notificacoes, u.ubs FROM s INNER JOIN u ON s.municipio=u.municipio ORDER BY s.notificacoes DESC,s.municipio ASC
```

## Q63

Para todas as UFs não vazias comuns à vacinação e aos leitos, retorne UF, contagem de registros por UF de residência em toda a vacinação carregada e soma de UTI_TOTAL_EXIST na maior COMP global dos leitos. Inclua somente UFs com soma de UTI positiva; agregue antes de juntar.

Colunas: uf, doses, leitos

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH v AS (SELECT paciente_endereco_uf AS uf, count() AS doses FROM vacinacao WHERE paciente_endereco_uf != '' GROUP BY uf), b AS (SELECT UF AS uf, sum(UTI_TOTAL_EXIST) AS leitos FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND UF != '' GROUP BY UF HAVING sum(UTI_TOTAL_EXIST)>0) SELECT v.uf,v.doses,b.leitos FROM v INNER JOIN b ON v.uf=b.uf
```

## Q64

Para todas as UFs não vazias comuns à vacinação e aos leitos, retorne UF, contagem de registros por UF de residência em toda a vacinação carregada e soma de UTI_TOTAL_EXIST na maior COMP global dos leitos. Inclua somente UFs com soma de UTI positiva; agregue antes de juntar.

Colunas: uf, doses, leitos

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

```sql
WITH v AS (SELECT paciente_endereco_uf AS uf, count() AS doses FROM vacinacao WHERE paciente_endereco_uf != '' GROUP BY uf), b AS (SELECT UF AS uf, sum(UTI_TOTAL_EXIST) AS leitos FROM leitos WHERE COMP = (SELECT max(COMP) FROM leitos) AND UF != '' GROUP BY UF HAVING sum(UTI_TOTAL_EXIST)>0) SELECT v.uf,v.doses,b.leitos FROM v INNER JOIN b ON v.uf=b.uf
```

## Q65

Qual é a quantidade de leitos de UTI SUS nos estados com maior número de notificações de SRAG?

Colunas: 

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

Limitação prevista da implementação; sem SQL numérico.

## Q66

Qual estado teve mais hospitalizações por SRAG e qual era sua quantidade de leitos existentes na competência mais recente?

Colunas: 

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

Limitação prevista da implementação; sem SQL numérico.

## Q67

Qual é a relação entre quantidade de UBS e número de registros de vacinação contra a COVID-19 por estado?

Colunas: 

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

Limitação prevista da implementação; sem SQL numérico.

## Q68

Quais municípios combinam alto número de notificações de SRAG, UBS cadastradas e baixa disponibilidade de leitos?

Colunas: 

Revisão: draft

Comparação: `{"ordered": false, "absolute_tolerance": 0.0, "relative_tolerance": 0.0, "columns": {}}`

Limitação prevista da implementação; sem SQL numérico.
