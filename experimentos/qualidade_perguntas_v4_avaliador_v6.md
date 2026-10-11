# Qualidade das perguntas

Rubrica adaptada da literatura; classificações automáticas são preliminares.
Disponibilidade e suporte são estimados por metadados, sem executar SQL ou consultar CSVs.
Não há nota global. Percentuais usam somente pass/partial/fail; veja pendências e denominadores.

Modelo: qwen2.5-coder:7b. Campo avaliado: question.

| Dimensão | Atende | Parcial | Não atende | Não aplicável | Não avaliável | Pendente | Revisadas | % atende / avaliadas |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| context_completeness | 0 | 3 | 0 | 0 | 0 | 65 | 0 | 0.0% / 3 |
| analytical_specificity | 2 | 1 | 0 | 0 | 0 | 65 | 0 | 66.7% / 3 |
| unambiguity | 2 | 1 | 0 | 0 | 0 | 65 | 0 | 66.7% / 3 |
| data_availability | 0 | 0 | 0 | 0 | 2 | 66 | 0 | Não avaliado |
| implementation_support | 0 | 1 | 0 | 0 | 2 | 65 | 0 | 0.0% / 1 |

## Q1

Quantas doses de vacina contra a COVID-19 foram registradas no conjunto de dados carregado?

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q2

Qual UF de residência não vazia tem mais registros de primeira dose ('1ª Dose') no recorte? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q3

Quantos registros têm vacina_descricao_dose igual a '2ª Dose' na base carregada?

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q4

Por UF de residência não vazia, qual a diferença entre registros de '1ª Dose' e '2ª Dose'? Retorne UF e diferença, incluindo todas as UFs presentes.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q5

Qual a razão entre o número de registros cuja descrição da dose contém 'reforço' (sem distinguir maiúsculas) e os de '1ª Dose'? Retorne apenas a razão, não percentual; nulo se denominador zero. Retorne a razão com pelo menos seis casas decimais.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q6

Qual o percentual de registros F e de registros M no campo paciente_enumSexoBiologico, usando somente F e M no denominador? Retorne as duas categorias e percentuais, nulo se não houver F/M.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q7

Entre faixas etárias presentes 0-18, 19-59 e 60+ anos, excluindo idades negativas, qual tem menos registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: faixa,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q8

Quais municípios de residência (UF e código IBGE não vazios) têm a maior contagem de registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,municipio,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q9

Qual a contagem de registros de vacinação por UF de residência não vazia e faixas 0-18, 19-59 e 60+ anos? Exclua idades negativas; retorne todos os grupos presentes, UF, faixa e total. Não conte pessoas distintas.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q10

Qual a contagem de registros de vacinação por sistema_origem? Retorne todos os grupos; mantenha nulos como nulos.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q11

Qual vacina_nome não vazio tem mais registros e qual o percentual desses registros sobre todas as linhas de vacinação? Retorne nome e percentual. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: vacina,percentual.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q12

Qual fabricante não vazio tem mais registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: fabricante,total.

Fatos extraídos: {"measure": "registros de vacinação?", "population": "fabricante", "time_scope": "", "place_scope": "", "filters": "", "grouping": "fabricante", "ties": "todos os empatados."}

Mapeamento de requisitos:
- Qual fabricante não vazio tem mais registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: fabricante,total. → field:covid-19-vacinacao:vacina_fabricante_nome, field:covid-19-vacinacao:vacina_fabricante_nome. O enunciado solicita a contagem de registros de vacinação por fabricante e incluir todos os empatados. O campo 'vacina_fabricante_nome' é o único que contém o f

Chamadas registradas: 4; tempo acumulado: 408.9s.

- **context_completeness: partial** (llm_preliminary). Falta período e local.
  Evidência: [{"source": "question", "quote": "Qual fabricante não vazio tem mais registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: fabricante,total."}]
  Sugestão: Especifique período e local para obter uma resposta completa e precisa. Por exemplo: 'Qual fabricante não vazio tem mais registros de vacinação em 2022 em São保罗
  Verificação: necessary_scope_missing — A falta de período e local limita a resposta, pois os dados podem variar significativamente entre diferentes períodos e locais.
  Problema indicado: Falta período e local para a consulta completa e precisa. Por exemplo: 'Qual fabricante não vazio tem mais registros de vacinação em 2022 em São Paulo?'.
  Interpretação alternativa: Se período e local não forem especificados, a consulta retornará os fabricantes com mais registros de vacinação em qualquer período e local disponíveis nos dados. No entanto, isso限

- **analytical_specificity: pass** (llm_preliminary). A consulta especifica a unidade contada (registros de vacinação), a medida (total), o agrupamento (fabricante) e a comparação (todos os empatados).
  Evidência: [{"source": "question", "quote": "Qual fabricante não vazio tem mais registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: fabricante,total."}]
  Verificação: complete — A consulta é específica em relação à unidade contada, medida, agrupamento e comparação solicitados.

- **unambiguity: pass** (llm_preliminary). Não há interpretações plausíveis que alterem o resultado, pois a tarefa é clara e não depende de termos relativos ou rankings sem limites.
  Evidência: [{"source": "question", "quote": "Qual fabricante não vazio tem mais registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: fabricante,total."}]
  Verificação: resolved — A tarefa é clara e não depende de termos relativos ou rankings sem limites.

- **data_availability: not_assessable** (llm_preliminary). A evidência não fornece detalhes suficientes para avaliar a disponibilidade dos dados necessários para responder à pergunta. A ausência de campos específicos ou metadados relevantes impede uma avaliação precisa.
  Evidência: [{"source": "question", "quote": "Qual fabricante não vazio tem mais registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: fabricante,total."}, {"source": "dataset:covid-19-vacinacao", "quote": "{\"descricao\": \"Dados de vacinação COVID-19 no Brasil - DataSUS\", \"nome_curto\": \"covid-19-vacinacao\", \"tabela_clickhouse\": \"vacinacao\"}"}, {"source": "field:covid-19-vacinacao:vacina_fabricante_nome", "quote": "String | Nome da fabricante da vacina"}]
  Sugestão: Forneça mais detalhes sobre os campos disponíveis e a estrutura dos dados para uma avaliação precisa. Se os campos necessários estão ausentes, considere a possí

- **implementation_support: not_assessable** (llm_preliminary). A evidência não fornece detalhes suficientes para avaliar o suporte descrito nos metadados de bases e relacionamentos cadastrados. A ausência de campos específicos ou metadados relevantes impede uma avaliação precisa.
  Evidência: [{"source": "question", "quote": "Qual fabricante não vazio tem mais registros de vacinação? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: fabricante,total."}, {"source": "dataset:covid-19-vacinacao", "quote": "{\"descricao\": \"Dados de vacinação COVID-19 no Brasil - DataSUS\", \"nome_curto\": \"covid-19-vacinacao\", \"tabela_clickhouse\": \"vacinacao\"}"}, {"source": "field:covid-19-vacinacao:vacina_fabricante_nome", "quote": "String | Nome da fabricante da vacina"}]
  Sugestão: Forneça mais detalhes sobre os campos disponíveis e a estrutura dos dados para uma avaliação precisa. Se os campos necessários estão ausentes, considere a possí

## Q13

Qual a contagem de registros de vacinação por ano e mês de aplicação? Retorne mes no formato AAAA-MM e total de todos os meses presentes; exclua datas nulas.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q14

Qual combinação de UF de residência não vazia e mês de aplicação (AAAA-MM) tem mais registros de vacinação? Exclua datas nulas. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,mes,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q15

Quantos registros existem por descrição de dose que contenha 'reforço', sem distinguir maiúsculas? Preserve a descrição original e retorne todos os grupos.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q16

Quantas UBS distintas estão cadastradas na base carregada, contando CNES positivos? Não inferir situação ativa.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q17

Qual a contagem de CNES distintos positivos de UBS por código de UF não vazio? Retorne todos os grupos presentes.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q26

Qual a contagem de CNES distintos positivos de UBS por código de UF não vazio? Retorne todos os grupos presentes.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q18

Qual código de UF não vazio tem mais UBS distintas (CNES positivos)? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q27

Qual código de UF não vazio tem mais UBS distintas (CNES positivos)? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q19

Quantos códigos de município positivos possuem pelo menos um CNES positivo na base de UBS?

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q20

Quais códigos de município positivos têm mais UBS distintas, contando CNES positivos nos municípios presentes na base? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: municipio,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q21

Quais códigos de município positivos têm mais UBS distintas, contando CNES positivos nos municípios presentes na base? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: municipio,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q30

Quais códigos de município positivos têm menos UBS distintas, contando CNES positivos nos municípios presentes na base? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: municipio,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q22

Na base de UBS, qual a contagem de CNES distintos positivos por município positivo nas UFs de códigos 21 a 29 (Nordeste)? Retorne todos os municípios, código e total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q23

Quantas UBS distintas (CNES positivos) têm latitude e longitude não zero e dentro de [-90,90] e [-180,180]?

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q24

Quais municípios positivos têm mais UBS distintas com CNES positivo e coordenadas não zero nos intervalos latitude [-90,90] e longitude [-180,180]? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: municipio,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q25

Qual a contagem de CNES distintos positivos por UF não vazia, código de município positivo e bairro não vazio após remover espaços nas extremidades, na base UBS? Preserve o nome original do bairro no agrupamento. Retorne todos os grupos; não una bairros homônimos de municípios diferentes.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q28

Quantas UBS distintas com CNES positivo possuem logradouro e bairro não vazios após remover espaços nas extremidades?

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q29

Qual a contagem de UBS distintas com CNES positivo por bairro no município IBGE 355030? Inclua todos os grupos, inclusive bairro vazio.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q31

Quantas linhas de notificações existem na tabela SRAG carregada, sem filtrar classificação final?

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q32

Qual a contagem de linhas de SRAG por ano de dt_notific e sem_not, excluindo dt_notific = '1970-01-01'? Retorne todos os grupos.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q33

Qual UF de notificação não vazia tem mais linhas de SRAG na base carregada? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q34

Qual a contagem de linhas de SRAG por UF de notificação não vazia? Retorne todas as UFs presentes.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q35

Quantos códigos de município de notificação positivos distintos existem nas linhas de SRAG?

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q36

Qual o percentual de linhas de SRAG com hospital = 1 entre todas as linhas? Retorne nulo se o denominador for zero.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q38

Qual o percentual de linhas de SRAG com evolucao = 2 entre as linhas com hospital = 1? Retorne nulo se o denominador for zero.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q39

Qual o percentual de linhas de SRAG com uti = 1 entre todas as linhas? Retorne nulo se o denominador for zero.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q37

Quantas linhas de SRAG possuem evolucao = 2?

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q40

Qual UF de notificação não vazia tem maior percentual de linhas com evolucao = 2, usando todas as linhas daquela UF no denominador? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,percentual.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q41

Retorne uma linha com as contagens de SRAG em que cada indicador vale 1, na ordem febre, tosse, garganta, dispneia, diarreia e vomito. Uma notificação pode contribuir para vários sintomas.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q42

Qual faixa tem mais linhas de SRAG: 0-18, 19-59 ou 60+ anos? Use nu_idade_n como magnitude da idade e tp_idade 1=dias, 2=meses e 3=anos; exclua idade nula, negativa e unidades desconhecidas. Para este teste, converta dias dividindo por 365.25 e meses por 12; anos permanecem iguais. Use os intervalos [0,19), [19,60) e [60,infinito), com rótulos '0-18', '19-59' e '60+'. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: faixa,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q43

Qual o percentual de linhas de SRAG com ao menos um dos indicadores cardiopati, hematologi, hepatica, asma, diabetes, neurologic, pneumopati, imunodepre, renal ou obesidade igual a 1, sobre todas as linhas? Nulo se não houver linhas.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q44

Quantas linhas de SRAG têm pcr_sars2 = 1 ou pos_pcrflu = 1? Conte cada linha apenas uma vez.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q45

Entre os indicadores pcr_sars2, pos_pcrflu e pcr_vsr, qual possui mais linhas de SRAG com valor 1? Retorne o nome do indicador e a contagem. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: agente,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q46

Qual a soma de LEITOS_EXISTENTES na tabela leitos na maior competência COMP global disponível? Conte leitos registrados, não vagas livres.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q47

Qual a soma de LEITOS_SUS na tabela leitos na maior competência COMP global disponível? Conte leitos registrados, não vagas livres.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q51

Qual a soma de UTI_TOTAL_EXIST na tabela leitos na maior competência COMP global disponível? Conte leitos registrados, não vagas livres.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q48

Qual o percentual da soma de LEITOS_SUS sobre a soma de LEITOS_EXISTENTES na maior COMP global de leitos? Nulo se denominador zero.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q52

Qual o percentual da soma de UTI_TOTAL_EXIST sobre a soma de LEITOS_EXISTENTES na maior COMP global de leitos? Nulo se denominador zero.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q49

Qual UF não vazia tem a maior soma de LEITOS_EXISTENTES na maior COMP global de leitos? Inclua UFs com total zero. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q55

Qual UF não vazia tem a menor soma de UTI_NEONATAL_EXIST na maior COMP global de leitos? Inclua UFs com total zero. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q50

Qual a soma de LEITOS_EXISTENTES por UF não vazia na maior COMP global? Retorne todas as UFs presentes.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q53

Qual DS_TIPO_UNIDADE não vazio tem maior soma de LEITOS_EXISTENTES na maior COMP global? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: tipo,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q54

Retorne uma linha com as somas de UTI_ADULTO_EXIST, UTI_PEDIATRICO_EXIST, UTI_NEONATAL_EXIST, UTI_CORONARIANA_EXIST e UTI_QUEIMADO_EXIST nessa ordem, na maior COMP global de leitos.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q56

Qual código TP_GESTAO não vazio reúne mais CNES distintos não vazios na maior COMP global de leitos? Retorne o código, sem classificá-lo como público, privado ou filantrópico. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: gestao,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q57

Qual a soma de LEITOS_SUS, na maior COMP global de leitos, em linhas cujo código NATUREZA_JURIDICA, após remover espaços externos, começa com '2' ou '3'? Não use TP_GESTAO para esse filtro.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q58

Qual UF não vazia tem maior percentual da soma de LEITOS_SUS sobre LEITOS_EXISTENTES na maior COMP global? Considere somente UFs cuja soma de LEITOS_EXISTENTES seja positiva. Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,percentual.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q59

Retorne REGIAO, soma de LEITOS_EXISTENTES e soma de LEITOS_SUS para todas as regiões não vazias na maior COMP global de leitos.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q60

Qual combinação de UF e código CO_IBGE não vazios tem maior soma de LEITOS_EXISTENTES na maior COMP global? Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: uf,municipio,total.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q61

Quantos códigos positivos de município de notificação de SRAG também aparecem na base UBS com CNES positivo? Conte municípios distintos por igualdade dos códigos.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q62

Liste todos os municípios positivos presentes em SRAG e UBS, com número de linhas de notificações e número de CNES distintos positivos. Ordene por notificações decrescentes e código municipal crescente, sem limitar a quantidade de linhas.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q63

Para todas as UFs não vazias comuns à vacinação e aos leitos, retorne UF, contagem de registros por UF de residência em toda a vacinação carregada e soma de UTI_TOTAL_EXIST na maior COMP global dos leitos. Inclua somente UFs com soma de UTI positiva; agregue antes de juntar.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q64

Para todas as UFs não vazias comuns à vacinação e aos leitos, retorne UF, contagem de registros por UF de residência em toda a vacinação carregada e soma de UTI_TOTAL_EXIST na maior COMP global dos leitos. Inclua somente UFs com soma de UTI positiva; agregue antes de juntar.

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q65

Qual é a quantidade de leitos de UTI SUS nos estados com maior número de notificações de SRAG?

Fatos extraídos: {"measure": "quantidade de leitos de UTI SUS", "population": "estados", "time_scope": "", "place_scope": "", "filters": "maior número de notificações de SRAG?", "grouping": "", "ties": ""}

Mapeamento de requisitos:
- Qual é a quantidade de leitos de UTI SUS nos estados com maior número de notificações de SRAG? → field:surtos-srag:SG_UF_NOT, field:leitos:UF, field:leitos:UTI_TOTAL_SUS. Esses campos são necessários para identificar o estado de notificação, o estado dos leitos e a quantidade de leitos de UTI SUS disponíveis.

Chamadas registradas: 5; tempo acumulado: 388.9s.

- **context_completeness: partial** (llm_preliminary). Falta de período e local.
  Evidência: [{"source": "question", "quote": "Qual é a quantidade de leitos de UTI SUS nos estados com maior número de notificações de SRAG?"}]
  Sugestão: Especifique período e local para obter uma resposta completa e precisa. Por exemplo: 'Qual é a quantidade de leitos de UTI SUS nos estados com maior número de n
  Verificação: necessary_scope_missing — A falta de período e local limita a resposta, pois não é possível determinar a quantidade de leitos de UTI SUS em um determinado período ou local específico.
  Problema indicado: Falta de período e local para a consulta completa e precisa. Por exemplo: 'Qual é a quantidade de leitos de UTI SUS nos estados com maior número de notificações de SRAG em 2022?'
  Interpretação alternativa: Especificar um período específico, como 2022, ou um local específico, como Brasil, para obter uma resposta mais precisa e contextualizada.

- **analytical_specificity: pass** (llm_preliminary). A medida, entidade e agrupamento solicitados estão claros.
  Evidência: [{"source": "question", "quote": "Qual é a quantidade de leitos de UTI SUS nos estados com maior número de notificações de SRAG?"}]
  Verificação: complete — A medida, entidade e agrupamento solicitados estão claros e não requerem alterações.

- **unambiguity: pass** (llm_preliminary). Não há interpretações plausíveis que alterem o resultado.
  Evidência: [{"source": "question", "quote": "Qual é a quantidade de leitos de UTI SUS nos estados com maior número de notificações de SRAG?"}]
  Verificação: resolved — Não há interpretações plausíveis que alterem o resultado.

- **data_availability: not_assessable** (llm_preliminary). Evidência insuficiente para avaliar a disponibilidade dos dados necessários.
  Evidência: [{"source": "question", "quote": "Qual é a quantidade de leitos de UTI SUS nos estados com maior número de notificações de SRAG?"}]
  Sugestão: Verifique a disponibilidade dos dados em fontes oficiais e atualize os metadados se necessário.

- **implementation_support: not_assessable** (llm_preliminary). Evidência insuficiente para avaliar o suporte de implementação.
  Evidência: [{"source": "question", "quote": "Qual é a quantidade de leitos de UTI SUS nos estados com maior número de notificações de SRAG?"}]
  Sugestão: Verifique se os campos necessários estão mapeados corretamente e se há relacionamentos cadastrados entre as bases.

## Q66

Qual estado teve mais hospitalizações por SRAG e qual era sua quantidade de leitos existentes na competência mais recente?

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q67

Qual é a relação entre quantidade de UBS e número de registros de vacinação contra a COVID-19 por estado?

- **context_completeness: pending** (pending). Aguardando avaliação.

- **analytical_specificity: pending** (pending). Aguardando avaliação.

- **unambiguity: pending** (pending). Aguardando avaliação.

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: pending** (pending). Aguardando avaliação.

## Q68

Quais municípios combinam alto número de notificações de SRAG, UBS cadastradas e baixa disponibilidade de leitos?

Fatos extraídos: {"measure": "número de notificações de SRAG, UBS cadastradas", "population": "municípios", "time_scope": "", "place_scope": "", "filters": "baixa disponibilidade de leitos?", "grouping": "", "ties": ""}

Mapeamento de requisitos:
- Quais municípios combinam alto número de notificações de SRAG, UBS cadastradas e baixa disponibilidade de leitos? → field:surtos-srag:CO_MUN_NOT, field:atencao-basica:IBGE, field:leitos:CO_IBGE, field:leitos:LEITOS_SUS. Esses campos são necessários para identificar municípios com alto número de notificações de SRAG, UBS cadastradas e baixa disponibilidade de leitos.

Chamadas registradas: 5; tempo acumulado: 495.8s.

Erros da avaliação: {"data_availability": "Incompatibilidade exige citar campo mapeado; a pergunta não demonstra conflito de metadados."}

- **context_completeness: partial** (llm_preliminary). Falta período e local.
  Evidência: [{"source": "question", "quote": "Quais municípios combinam alto número de notificações de SRAG, UBS cadastradas e baixa disponibilidade de leitos?"}]
  Sugestão: Especifique período e local para obter uma resposta precisa e contextualizada. Por exemplo: 'Quais municípios no estado de São Paulo combinam alto número de not
  Verificação: necessary_scope_missing — A falta de período e local limita a relevância e a precisão da resposta, pois não é possível identificar municípios específicos que atendam aos critérios solicitados.
  Problema indicado: Falta período e local para a consulta completa e precisa.
  Interpretação alternativa: Se o período e local não forem especificados, a consulta retornará uma lista de municípios em geral, sem contexto geográfico ou temporal específico.

- **analytical_specificity: partial** (llm_preliminary). A medida e os filtros estão definidos, mas falta o agrupamento e a comparação solicitados.
  Evidência: [{"source": "question", "quote": "Quais municípios combinam alto número de notificações de SRAG, UBS cadastradas e baixa disponibilidade de leitos?"}]
  Sugestão: Especifique como deseja agrupar os resultados e como deseja compará-los. Por exemplo: 'Quais municípios no estado de São Paulo combinam alto número de notifica
  Verificação: incomplete — A falta de agrupamento e comparação limita a profundidade e a utilidade da resposta, pois não é possível identificar padrões ou tendências nos dados solicitados.
  Problema indicado: Falta agrupamento e comparação para a análise completa e precisa.
  Interpretação alternativa: Se o agrupamento e a comparação não forem especificados, a consulta retornará uma lista de municípios que atendem aos critérios solicitados, sem uma análise mais detalhada.

- **unambiguity: partial** (llm_preliminary). A interpretação da pergunta é ambígua, pois não está claro se deseja identificar municípios com alto número de notificações de SRAG e UBS cadastradas e baixa disponibilidade de leitos, ou se deseja identificar municípios com alto número de 
  Evidência: [{"source": "question", "quote": "Quais municípios combinam alto número de notificações de SRAG, UBS cadastradas e baixa disponibilidade de leitos?"}]
  Sugestão: Especifique se deseja identificar municípios com alto número de notificações de SRAG e UBS cadastradas e baixa disponibilidade de leitos, ou se deseja identific
  Verificação: unresolved — A interpretação da pergunta é ambígua, pois não está claro se deseja identificar municípios com alto número de notificações de SRAG e UBS cadastradas e baixa disponibilidade de le
  Problema indicado: A interpretação da pergunta é ambígua, pois não está claro se deseja identificar municípios com alto número de notificações de SRAG e UBS cadastradas e baixa disponibilidade de le
  Interpretação alternativa: Se a interpretação da pergunta for alterada para identificar municípios com alto número de notificações de SRAG e UBS cadastradas e baixa disponibilidade de leitos, a consulta ret

- **data_availability: pending** (pending). Aguardando avaliação.

- **implementation_support: partial** (llm_preliminary). A integração entre as bases de dados não está cadastrada, o que limita a capacidade de responder à pergunta.
  Evidência: [{"source": "relationship:srag_ubs_municipio_notificacao", "quote": "{\"id\":\"srag_ubs_municipio_notificacao\",\"description\":\"Relaciona notificações de SRAG às UBS do município\",\"source_dataset\":\"surtos-srag\",\"source_table\":\"srag\",\"source_column\":\"co_m"}, {"source": "dataset:atencao-basica", "quote": "ao-basica\", \"tabela_clickhouse\": \"atencao_basica\"}"}, {"source": "dataset:leitos", "quote": "{\"descricao\": \"Dados de leitos disponíveis em hospitais e estabelecimentos de saúde no Brasil - DataSUS\", \"nome_curto\": \"leitos\", \"tabela_clickhouse\": \"leitos\"}"}]
  Sugestão: Cadastre a integração entre as bases de dados e entre os campos necessários para responder à pergunta.

## Referências

- [Wang e Strong (1996), Beyond Accuracy](https://courses.washington.edu/geog482/resource/14_Beyond_Accuracy.pdf)
- [Pipino, Lee e Wang (2002), Data Quality Assessment](https://web.mit.edu/tdqm/www/tdqmpub/PipinoLeeWangCACMApr02.pdf)
- [Bhaskar et al. (2023), Text-to-SQL under Ambiguity](https://aclanthology.org/2023.emnlp-main.436/)
- [Wang et al. (2023), Know What I don’t Know](https://aclanthology.org/2023.findings-acl.352/)
