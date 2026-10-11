# Perguntas do experimento EasyDataSUS
## 68 questões para avaliação do sistema atual

Este documento contém o conjunto de perguntas utilizado pelo script `backend/tests/benchmark_68_questoes_seidig.py`. As perguntas foram estruturadas para avaliar o EasyDataSUS em cenários de apoio informacional à gestão em saúde pública, considerando bases do DataSUS, metadados semânticos, geração de SQL, validação estrutural e interoperabilidade controlada entre bases.

As perguntas estão alinhadas a cenários associados aos Objetivos Estratégicos do SEIDIG, mas devem ser interpretadas de acordo com a disponibilidade real dos dados carregados. Algumas perguntas exigem denominadores ou relações ainda não disponíveis, como população por território ou relacionamentos não cadastrados. Nesses casos, a resposta esperada pode ser a identificação da limitação analítica, e não necessariamente a execução de uma consulta SQL.

**Distribuição:**
- **OE 3.6.1 (Imunização)**: COVID-19 (15) + UBS (15) = 30 questões
- **OE 9.1 (Vigilância/Gestão)**: SRAG (15) + Leitos (15) = 30 questões  
- **Interoperabilidade**: 8 questões
- **TOTAL**: 68 questões

---

## OE 3.6.1 - IMUNIZAÇÃO: COVID-19 Vacinação (15 questões)

### Foco: Registros de vacinação, distribuição, equidade e tendências

#### Bloco 1: Monitoramento de registros vacinais (5 questões)

1. **Quantas doses de vacina contra a COVID-19 foram registradas no conjunto de dados carregado?**
   - Objetivo: Quantificar o volume de registros de vacinação disponíveis para análise
   - Campo: COUNT(*)
   - Complexidade: Simples

2. **Qual estado apresentou o maior número de registros de primeira dose de COVID-19?**
   - Objetivo: Identificar concentração estadual de registros de primeira dose
   - Campo: paciente_endereco_uf, vacina_descricao_dose = '1ª dose', COUNT(*)
   - Complexidade: Média

3. **Quantos registros de segunda dose contra a COVID-19 existem no conjunto de dados carregado?**
   - Objetivo: Monitorar registros associados ao esquema de segunda dose
   - Campo: vacina_descricao_dose = '2ª dose', COUNT(*)
   - Complexidade: Simples

4. **Qual é a diferença entre registros de primeira dose e segunda dose por estado?**
   - Objetivo: Comparar registros de etapas do esquema vacinal por UF, sem inferir cobertura populacional
   - Campo: paciente_endereco_uf, COUNT(1ª) - COUNT(2ª)
   - Complexidade: Complexa

5. **Quantos registros de doses de reforço existem em relação aos registros de primeira dose?**
   - Objetivo: Comparar registros de reforço com registros de primeira dose dentro do recorte carregado
   - Campo: vacina_descricao_dose (contém 'Reforço'), COUNT(*) / COUNT(vacina_descricao_dose = '1ª dose')
   - Complexidade: Média

#### Bloco 2: Equidade e Vulnerabilidade (5 questões)

6. **Qual é o percentual de mulheres em relação a homens na campanha de vacinação?**
   - Objetivo: Avaliar equidade de gênero na imunização
   - Campo: paciente_enumSexoBiologico, COUNT(*) / total
   - Complexidade: Média

7. **Qual faixa etária teve menor número de registros de vacinação?**
   - Objetivo: Identificar faixas etárias menos presentes no recorte carregado, sem calcular cobertura populacional
   - Campo: paciente_idade (agrupado em faixas), COUNT(*)
   - Complexidade: Complexa

8. **Quais municípios apresentam maior número de registros de vacinação contra a COVID-19?**
   - Objetivo: Identificar concentração municipal de registros de vacinação
   - Campo: paciente_endereco_nmMunicipio, COUNT(*)
   - Complexidade: Média

9. **Qual é a distribuição de vacinados por faixa etária e estado (análise de duas dimensões)?**
   - Objetivo: Identificar padrões demográficos por região
   - Campo: paciente_endereco_uf, paciente_idade (faixa), COUNT(*)
   - Complexidade: Complexa

10. **Qual é a distribuição de doses registradas por sistema de origem dos dados?**
    - Objetivo: Avaliar a origem sistêmica dos registros de vacinação disponíveis
    - Campo: sistema_origem, COUNT(*)
    - Complexidade: Média

#### Bloco 3: Eficiência Logística e Cadeia de Suprimento (5 questões)

11. **Qual vacina foi mais utilizada na campanha (em % de doses totais)?**
    - Objetivo: Entender preferência/disponibilidade de tipos vacinais
    - Campo: vacina_nome, COUNT(*) / total
    - Complexidade: Simples

12. **Qual fabricante aparece com maior número de registros de doses aplicadas?**
    - Objetivo: Avaliar dependência da cadeia de suprimento
    - Campo: vacina_fabricante_nome, COUNT(*)
    - Complexidade: Média

13. **Qual é a evolução temporal de doses aplicadas por mês (tendência da campanha)?**
    - Objetivo: Identificar períodos de aceleração/desaceleração na vacinação
    - Campo: MONTH(vacina_dataAplicacao), COUNT(*)
    - Complexidade: Média

14. **Qual estado teve o maior pico de vacinação em um único mês?**
    - Objetivo: Avaliar capacidade operacional por região
    - Campo: paciente_endereco_uf, MONTH(vacina_dataAplicacao), MAX(COUNT(*))
    - Complexidade: Complexa

15. **Quantos registros existem para cada tipo de dose de reforço (Reforço 1, Reforço 2, etc.)?**
    - Objetivo: Monitorar cobertura de booster estratificada
    - Campo: vacina_descricao_dose (contém 'Reforço'), COUNT(*)
    - Complexidade: Média

---

## OE 3.6.1 / OE 7.2/7.3 - ATENÇÃO PRIMÁRIA: UBS (15 questões)

### Foco: Distribuição territorial e registros de Unidades Básicas de Saúde

#### Bloco 1: Mapeamento de Capacidade (5 questões)

16. **Quantas Unidades Básicas de Saúde (UBS) estão ativas no Brasil?**
    - Objetivo: Quantificar infraestrutura de atenção primária
    - Campo: COUNT(DISTINCT cnes)
    - Complexidade: Simples

17. **Qual é a distribuição de UBS por estado?**
    - Objetivo: Identificar disparidades estaduais de acesso
    - Campo: uf, COUNT(DISTINCT cnes)
    - Complexidade: Média

18. **Qual estado tem o maior número absoluto de UBS cadastradas?**
    - Objetivo: Identificar concentração estadual de unidades de atenção primária
    - Campo: uf, COUNT(DISTINCT cnes), ORDER BY DESC
    - Complexidade: Média

19. **Em quantos municípios há pelo menos uma UBS cadastrada?**
    - Objetivo: Medir abrangência municipal observada na base carregada
    - Campo: COUNT(DISTINCT ibge)
    - Complexidade: Simples

20. **Quais municípios possuem o maior número de UBS cadastradas?**
    - Objetivo: Identificar municípios com maior concentração de unidades básicas
    - Campo: ibge, COUNT(DISTINCT cnes), ORDER BY DESC
    - Complexidade: Média

#### Bloco 2: Análise Geográfica e Acesso (5 questões)

21. **Qual município tem o maior número de UBS cadastradas no recorte carregado?**
    - Objetivo: Identificar maior concentração municipal de UBS, sem usar denominador populacional
    - Campo: ibge, COUNT(DISTINCT cnes), ORDER BY DESC
    - Complexidade: Média

22. **Qual é o padrão de distribuição de UBS nos municípios da região Nordeste?**
    - Objetivo: Caracterizar acesso em região de menor cobertura
    - Campo: uf (Nordeste: AL, BA, CE, MA, PB, PE, PI, RN, SE), COUNT(cnes)
    - Complexidade: Média

23. **Quantas UBS possuem informações completas de localização (latitude/longitude)?**
    - Objetivo: Avaliar qualidade de dados geográficos para planejamento
    - Campo: COUNT(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL)
    - Complexidade: Simples

24. **Quais municípios possuem maior número de UBS com coordenadas geográficas registradas?**
    - Objetivo: Avaliar disponibilidade de localização geográfica por município
    - Campo: ibge, COUNT(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL)
    - Complexidade: Média

25. **Qual é a distribuição de UBS por bairro no conjunto de dados carregado?**
    - Objetivo: Avaliar concentração territorial segundo o campo de bairro disponível
    - Campo: bairro, COUNT(DISTINCT cnes)
    - Complexidade: Complexa

#### Bloco 3: Estrutura e Capacidade Operacional (5 questões)

26. **Qual é a distribuição de UBS por código de UF?**
    - Objetivo: Avaliar distribuição estadual usando o código de UF disponível na base
    - Campo: uf, COUNT(DISTINCT cnes)
    - Complexidade: Média

27. **Qual código de UF concentra o maior número de UBS cadastradas?**
    - Objetivo: Identificar a maior concentração estadual de UBS
    - Campo: uf, COUNT(DISTINCT cnes), ORDER BY DESC
    - Complexidade: Média

28. **Quantas UBS possuem logradouro e bairro registrados?**
    - Objetivo: Avaliar completude de informações de endereço
    - Campo: COUNT(CASE WHEN logradouro IS NOT NULL AND bairro IS NOT NULL)
    - Complexidade: Simples

29. **Qual é a distribuição de UBS por bairro no município com código IBGE 355030?**
    - Objetivo: Analisar equidade intraurbanana de acesso
    - Campo: ibge = 355030, bairro, COUNT(DISTINCT cnes)
    - Complexidade: Média

30. **Quais municípios possuem menor número de UBS cadastradas entre os municípios presentes na base?**
    - Objetivo: Identificar municípios com baixa presença de UBS no recorte carregado
    - Campo: ibge, COUNT(DISTINCT cnes), ORDER BY ASC
    - Complexidade: Média

---

## OE 9.1 - VIGILÂNCIA EPIDEMIOLÓGICA: SRAG (15 questões)

### Foco: Detecção de Surtos, Gravidade Clínica e Mortalidade

#### Bloco 1: Monitoramento de Casos (5 questões)

31. **Quantos casos de SRAG foram notificados no período analisado?**
    - Objetivo: Conhecer escala da onda epidemiológica
    - Campo: COUNT(DISTINCT nu_notific)
    - Complexidade: Simples

32. **Qual é a evolução semanal de notificações de SRAG?**
    - Objetivo: Identificar tendência ascendente/descendente de surto
    - Campo: sem_not, COUNT(DISTINCT nu_notific)
    - Complexidade: Média

33. **Qual estado apresentou o maior número de casos de SRAG no período?**
    - Objetivo: Identificar epicentro da onda epidemiológica
    - Campo: sg_uf_not, COUNT(DISTINCT nu_notific), ORDER BY DESC
    - Complexidade: Média

34. **Qual é a distribuição de notificações de SRAG por estado?**
    - Objetivo: Comparar volume de notificações entre UFs no recorte carregado
    - Campo: sg_uf_not, COUNT(DISTINCT nu_notific), ORDER BY DESC
    - Complexidade: Média

35. **Em quantos municípios foram registrados casos de SRAG?**
    - Objetivo: Medir dispersão geográfica do surto
    - Campo: COUNT(DISTINCT co_mun_not)
    - Complexidade: Simples

#### Bloco 2: Gravidade Clínica e Internação (5 questões)

36. **Qual é a taxa de hospitalização entre os casos notificados de SRAG?**
    - Objetivo: Avaliar proporção de casos graves
    - Campo: COUNT(CASE WHEN hospital = 1) / COUNT(*) × 100
    - Complexidade: Média

37. **Quantos casos evoluíram para morte?**
    - Objetivo: Monitorar mortalidade e impacto da onda
    - Campo: COUNT(CASE WHEN evolucao = 2)
    - Complexidade: Simples

38. **Qual é a taxa de mortalidade entre os casos hospitalizados?**
    - Objetivo: Avaliar gravidade clínica (CFR = Case Fatality Rate)
    - Campo: COUNT(CASE WHEN evolucao = 2 AND hospital = 1) / COUNT(CASE WHEN hospital = 1) × 100
    - Complexidade: Média

39. **Qual é a taxa de internação em UTI entre todos os casos?**
    - Objetivo: Avaliar necessidade de cuidados intensivos
    - Campo: COUNT(CASE WHEN uti = 1) / COUNT(*) × 100
    - Complexidade: Média

40. **Qual estado teve a maior taxa de mortalidade (por casos)?**
    - Objetivo: Identificar regiões com pior desfecho clínico
    - Campo: sg_uf_not, COUNT(CASE WHEN evolucao = 2) / COUNT(*) × 100, ORDER BY DESC
    - Complexidade: Complexa

#### Bloco 3: Caracterização Clínico-Epidemiológica (5 questões)

41. **Qual é a distribuição de sintomas primários entre os casos (febre, tosse, dispneia, etc)?**
    - Objetivo: Caracterizar apresentação clínica do surto
    - Campo: febre, tosse, garganta, dispneia, diarreia, vomito (COUNT cada)
    - Complexidade: Complexa

42. **Qual é a faixa etária mais acometida por SRAG no período?**
    - Objetivo: Identificar grupos de risco
    - Campo: idade (agrupado: 0-18, 19-59, 60+), COUNT(*), ORDER BY DESC
    - Complexidade: Média

43. **Qual é a proporção de casos com comorbidades (diabetes, asma, cardiopatia, etc) entre os notificados?**
    - Objetivo: Avaliar perfil de risco dos casos
    - Campo: COUNT(CASE WHEN diabetes = 1 OR asma = 1 OR cardiopati = 1...) / COUNT(*) × 100
    - Complexidade: Complexa

44. **Quantos casos tiveram confirmação laboratorial (PCR positivo)?**
    - Objetivo: Avaliar taxa de confirmação diagnóstica
    - Campo: COUNT(CASE WHEN pcr_sars2 = 1 OR pos_pcrflu = 1)
    - Complexidade: Simples

45. **Qual agente etiológico foi mais frequentemente identificado (SARS-CoV-2, Influenza, VSR, etc)?**
    - Objetivo: Caracterizar etiologia do surto
    - Campo: pcr_sars2, pos_pcrflu, pcr_vsr (COUNT cada), ORDER BY DESC
    - Complexidade: Média

---

## OE 9.1 - GESTÃO ASSISTENCIAL: Leitos (15 questões)

### Foco: Capacidade de Internação e Resposta a Emergências

#### Bloco 1: Mapeamento de Capacidade (5 questões)

46. **Quantos leitos totais de internação estão disponíveis no Brasil?**
    - Objetivo: Quantificar capacidade máxima do sistema
    - Campo: SUM(LEITOS_EXISTENTES)
    - Complexidade: Simples

47. **Quantos desses são leitos SUS?**
    - Objetivo: Quantificar leitos registrados como disponíveis ao SUS
    - Campo: SUM(LEITOS_SUS)
    - Complexidade: Simples

48. **Qual é a proporção de leitos SUS em relação ao total (% de cobertura pública)?**
    - Objetivo: Avaliar equidade de acesso hospitalar
    - Campo: SUM(LEITOS_SUS) / SUM(LEITOS_EXISTENTES) × 100
    - Complexidade: Média

49. **Qual estado possui maior capacidade absoluta de leitos?**
    - Objetivo: Identificar polos de concentração de recursos
    - Campo: UF, SUM(LEITOS_EXISTENTES), ORDER BY DESC
    - Complexidade: Média

50. **Qual é a quantidade de leitos existentes por estado na competência mais recente?**
    - Objetivo: Comparar capacidade assistencial estadual no período mais recente disponível
    - Campo: UF, SUM(LEITOS_EXISTENTES), COMP = MAX(COMP)
    - Complexidade: Média

#### Bloco 2: Distribuição por Tipo de Unidade e Especialidade (5 questões)

51. **Quantos leitos de UTI estão disponíveis no Brasil no total?**
    - Objetivo: Avaliar capacidade de cuidados intensivos
    - Campo: SUM(UTI_TOTAL_EXIST)
    - Complexidade: Simples

52. **Qual é a proporção de leitos de UTI em relação aos leitos totais?**
    - Objetivo: Avaliar disponibilidade de cuidados críticos
    - Campo: SUM(UTI_TOTAL_EXIST) / SUM(LEITOS_EXISTENTES) × 100
    - Complexidade: Média

53. **Qual tipo de unidade (Hospital Geral, Pronto Socorro, etc) possui maior volume de leitos?**
    - Objetivo: Entender modelo de organização da rede
    - Campo: DS_TIPO_UNIDADE, SUM(LEITOS_EXISTENTES), ORDER BY DESC
    - Complexidade: Média

54. **Qual é a distribuição de especialidades de UTI (Adulto, Pediátrica, Neonatal, Coronariana, Queimados)?**
    - Objetivo: Avaliar preparo para diferentes grupos etários/patologias
    - Campo: SUM(UTI_ADULTO_EXIST), SUM(UTI_PEDIATRICO_EXIST), SUM(UTI_NEONATAL_EXIST), SUM(UTI_CORONARIANA_EXIST), SUM(UTI_QUEIMADO_EXIST)
    - Complexidade: Média

55. **Qual estado tem a menor quantidade absoluta de leitos de UTI neonatal na competência mais recente?**
    - Objetivo: Identificar menor disponibilidade absoluta de UTI neonatal no recorte carregado
    - Campo: UF, SUM(UTI_NEONATAL_EXIST), COMP = MAX(COMP), ORDER BY ASC
    - Complexidade: Média

#### Bloco 3: Resposta a Emergências e Resiliência (5 questões)

56. **Qual é o tipo de gestão predominante (Pública, Privada, Filantrópica) nas unidades de saúde?**
    - Objetivo: Avaliar composição público-privada da rede
    - Campo: TP_GESTAO, COUNT(*), SUM(LEITOS_EXISTENTES)
    - Complexidade: Média

57. **Quantos leitos SUS existem em estabelecimentos da iniciativa privada (parcerias)?**
    - Objetivo: Avaliar disponibilidade de leitos públicos em rede privada
    - Campo: TP_GESTAO = 'Privada', SUM(LEITOS_SUS)
    - Complexidade: Média

58. **Qual estado tem o maior percentual de leitos SUS em relação ao total (maior compromisso público)?**
    - Objetivo: Avaliar modelos de oferta pública por estado
    - Campo: UF, SUM(LEITOS_SUS) / SUM(LEITOS_EXISTENTES) × 100, ORDER BY DESC
    - Complexidade: Complexa

59. **Qual é a distribuição de capacidade de leitos entre regiões (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)?**
    - Objetivo: Avaliar equidade regional
    - Campo: REGIAO, SUM(LEITOS_EXISTENTES), SUM(LEITOS_SUS)
    - Complexidade: Média

60. **Qual município possui maior quantidade absoluta de leitos existentes na competência mais recente?**
    - Objetivo: Identificar centros com maior capacidade absoluta de internação
    - Campo: MUNICIPIO, UF, SUM(LEITOS_EXISTENTES), COMP = MAX(COMP), ORDER BY DESC
    - Complexidade: Média

---

##  INTEROPERABILIDADE: Análises Integradas (8 questões)

### Foco: Relações suportadas e limites analíticos interdomínio

#### Análises Cruzadas Entre Datasets

61. **Em quantos municípios há notificações de SRAG e também UBS cadastradas?**
    - Objetivo: Avaliar capacidade de resposta comunitária a surtos
    - Datasets: SRAG × UBS
    - Campos: SRAG.co_mun_not (INNER JOIN) UBS.ibge
    - Complexidade: Média

62. **Quais municípios possuem maior número de notificações de SRAG e quantas UBS existem em cada um?**
    - Objetivo: Comparar volume de notificações de SRAG com disponibilidade territorial de UBS
    - Datasets: SRAG × UBS
    - Campos: TOP municípios por SRAG, COUNT(DISTINCT UBS)
    - Complexidade: Média

63. **Quais estados possuem simultaneamente registros de vacinação contra a COVID-19 e leitos de UTI na competência mais recente, e quais são os respectivos totais?**
    - Objetivo: Demonstrar consulta interdomínio entre imunização e capacidade assistencial por UF
    - Datasets: COVID-19 × Leitos
    - Campos: vacinacao.paciente_endereco_uf, leitos.UF, COUNT(*), SUM(UTI_TOTAL_EXIST)
    - Complexidade: Média

64. **Compare o número de doses registradas contra a COVID-19 com a quantidade de leitos de UTI por estado.**
    - Objetivo: Avaliar a geração de consulta multibase por UF com pré-agregação nos dois lados
    - Datasets: COVID-19 × Leitos
    - Campos: COUNT(vacinacao), SUM(UTI_TOTAL_EXIST), JOIN por UF
    - Complexidade: Média

65. **Qual é a quantidade de leitos de UTI SUS nos estados com maior número de notificações de SRAG?**
    - Objetivo: Avaliar limite atual para relacionamento SRAG–Leitos ainda não cadastrado
    - Datasets: SRAG × Leitos
    - Campos: SRAG por estado, SUM(UTI_TOTAL_SUS), relacionamento ainda não cadastrado
    - Complexidade: Complexa

66. **Qual estado teve mais hospitalizações por SRAG e qual era sua quantidade de leitos existentes na competência mais recente?**
    - Objetivo: Avaliar limite atual para integração entre demanda epidemiológica e capacidade hospitalar
    - Datasets: SRAG × Leitos
    - Campos: SRAG hospitalizados por estado, SUM(LEITOS_EXISTENTES), relacionamento ainda não cadastrado
    - Complexidade: Complexa

67. **Qual é a relação entre quantidade de UBS e número de registros de vacinação contra a COVID-19 por estado?**
    - Objetivo: Avaliar limite atual para relação UBS–Vacinação ainda não cadastrada
    - Datasets: UBS × COVID-19
    - Campos: COUNT(UBS), COUNT(vacinacao), relacionamento ainda não cadastrado
    - Complexidade: Complexa

68. **Quais municípios combinam alto número de notificações de SRAG, UBS cadastradas e baixa disponibilidade de leitos?**
    - Objetivo: Avaliar limite de consulta multibase envolvendo três domínios e regras analíticas adicionais
    - Datasets: SRAG × Leitos × UBS
    - Campos: SRAG por município, UBS por município, leitos por município, relações e critérios ainda parciais
    - Complexidade: Complexa

---

##  Distribuição e Alinhamento

### Por Dataset
| Dataset | OE | Questões | % |
|---------|-----|----------|---|
| COVID-19 | 3.6.1 | 1-15 | 22% |
| UBS | 3.6.1/7.2/7.3 | 16-30 | 22% |
| SRAG | 9.1 | 31-45 | 22% |
| Leitos | 9.1 | 46-60 | 22% |
| Interoperabilidade | Multi | 61-68 | 12% |
| **TOTAL** | | **68** | **100%** |

### Por Objetivo Estratégico
| OE | Foco | Questões | Total |
|----|------|----------|-------|
| **OE 3.6.1** | Imunização + Atenção Primária | 1-30 | 30 (44%) |
| **OE 9.1** | Vigilância + Gestão Assistencial | 31-60 | 30 (44%) |
| **Multi-OE** | Interoperabilidade | 61-68 | 8 (12%) |

### Por complexidade

Cada pergunta traz uma classificação de complexidade estimada. Essa classificação é usada para separar consultas simples de agregação, consultas intermediárias com agrupamentos/filtros e consultas mais complexas envolvendo múltiplas dimensões, relações entre bases ou limites analíticos.

---

## Alinhamento com Decisão de Gestores

Essas 68 questões habilitam gestores a responder:

### Gestor de Imunização (OE 3.6.1)
- Qual é o volume de registros de vacinação disponível? (Q1-5)
- Como os registros se distribuem por sexo, idade, município e sistema de origem? (Q6-10)
- Como os registros se distribuem por vacina, fabricante e período? (Q11-15)

### Gestor de Atenção Primária (OE 3.6.1/7.2)
- Qual é a distribuição territorial de UBS no recorte carregado? (Q16-20)
- Quais municípios concentram ou apresentam menor número de UBS? (Q21-25)
- Como está a completude geográfica e de endereço das UBS? (Q26-30)

### Gestor de Vigilância (OE 9.1)
- Qual é a escala do surto? (Q31-35)
- Qual é a gravidade clínica? (Q36-40)
- Como está a etiologia? (Q41-45)

###  Gestor de Internação (OE 9.1)
- Qual é minha capacidade total? (Q46-50)
- Tenho capacidade crítica (UTI)? (Q51-55)
- Como está minha rede público-privada? (Q56-60)

###  Decisões Integradas
- Quais relações interdomínio o sistema executa automaticamente e quais ainda são limites analíticos? (Q61-68)

---

##  Critérios de avaliação

Essas 68 questões permitem avaliar:

- **Respondibilidade**: se a pergunta pode ou não ser respondida com os dados carregados.
- **Seleção de datasets**: se a base ou conjunto de bases selecionado é compatível com a pergunta.
- **Seleção de relacionamento**: se o relacionamento interdomínio correto é recuperado quando aplicável.
- **Validação SQL**: se a consulta gerada é somente leitura e respeita tabelas, colunas e joins permitidos.
- **Execução analítica**: se a consulta é executada com sucesso no ClickHouse.
- **Fidelidade factual**: se a resposta textual permanece ancorada nos dados retornados.
- **Desempenho**: tempo total e tempos por etapa registrados em `timing_s` e `evaluation_metrics`.

---

## Uso em experimentos

Cada questão pode ser executada pelo script:

```powershell
python backend/tests/benchmark_68_questoes_seidig.py
```

Também é possível executar intervalos ou datasets específicos:

```powershell
python backend/tests/benchmark_68_questoes_seidig.py --start 61 --end 68
python backend/tests/benchmark_68_questoes_seidig.py --dataset leitos
```

Cada resposta da rota `/api/ask` inclui o bloco `evaluation_metrics`, que registra métricas automáticas e campos pendentes de gabarito. As métricas dependentes de referência, como Exact Match, Execution Accuracy e fidelidade da resposta, devem ser preenchidas ou calculadas posteriormente a partir de gabarito/resultado esperado.

O resultado agregado é salvo em `test_results_68_questoes.json` na raiz do projeto.

---

