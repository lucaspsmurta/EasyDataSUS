"""Independent SQL reference candidates; require semantic review before use as gold."""
import re
from pathlib import Path

VERSION = "reference-v3"
ROOT = Path(__file__).resolve().parents[2]
V, U, S, B = "covid-19-vacinacao", "atencao-basica", "surtos-srag", "leitos"
LATEST = "COMP = (SELECT max(COMP) FROM leitos)"
VALID_UF = "notEmpty(trimBoth(uf))"
AGE_V = "multiIf(paciente_idade < 0, 'ignorada', paciente_idade <= 18, '0-18', paciente_idade <= 59, '19-59', '60+')"
# Q42 converts age magnitude and unit to years.
AGE_YEARS = "multiIf(tp_idade = 1, nu_idade_n / 365.25, tp_idade = 2, nu_idade_n / 12.0, toFloat64(nu_idade_n))"
AGE_S = f"multiIf(({AGE_YEARS}) < 19, '0-18', ({AGE_YEARS}) < 60, '19-59', '60+')"
GLOBAL = (
    "Avaliação restrita às tabelas carregadas, sem inferir cobertura nacional. "
    "Contagens de vacinação são registros, não pessoas. UBS são CNES distintos positivos. "
    "SRAG usa linhas de notificações, sem filtrar classi_fin; esta unidade deve ser revisada "
    "contra duplicatas antes de qualquer interpretação como casos únicos. "
    "Leitos são existentes na maior COMP global, nunca vagas livres. "
    "Indicadores SRAG = 1 significam presença; evolucao = 2 é o desfecho contado. "
    "Nulos/desconhecidos permanecem no denominador quando se pede todas as linhas. "
    "Os códigos e unidades da idade requerem revisão do dicionário da fonte."
)


def catalog():
    original = dict((int(i), q) for i, q in re.findall(
        r"(?m)^(\d+)\. \*\*(.*?)\*\*", (ROOT / "docs/PERGUNTAS_SEIDIG_68.md").read_text(encoding="utf-8")))
    cases = {}

    def add(i, question, sql, columns, *, datasets=None, relations=None, note="", ordered=False):
        ds = datasets or ([V] if i <= 15 else [U] if i <= 30 else [S] if i <= 45 else [B])
        cases[i] = dict(id=i, original_question=original[i], question=question,
                        reference_sql=sql, columns=columns.split(","), expected_datasets=ds,
                        expected_relationships=relations or [], expected_behavior="answer",
                        implementation_supported=i < 65, review_status="draft",
                        specification=note, comparison=dict(ordered=ordered, absolute_tolerance=0.0,
                                                          relative_tolerance=0.0))

    def extrema(i, question, inner, cols, metric="total", low=False, **kw):
        op = "min" if low else "max"
        add(i, question + " Inclua todos os empatados. Retorne somente estas colunas, nesta ordem: " + cols + ".",
            f"WITH grouped AS ({inner}) SELECT {cols} FROM grouped WHERE {metric} = (SELECT {op}({metric}) FROM grouped)",
            cols, **kw)

    add(1, original[1], "SELECT count() AS total FROM vacinacao", "total")
    extrema(2, "Qual UF de residência não vazia tem mais registros de primeira dose ('1ª Dose') no recorte?",
            "SELECT paciente_endereco_uf AS uf, count() AS total FROM vacinacao WHERE paciente_endereco_uf != '' AND vacina_descricao_dose = '1ª Dose' GROUP BY uf", "uf,total")
    add(3, "Quantos registros têm vacina_descricao_dose igual a '2ª Dose' na base carregada?",
        "SELECT countIf(vacina_descricao_dose = '2ª Dose') AS total FROM vacinacao", "total")
    add(4, "Por UF de residência não vazia, qual a diferença entre registros de '1ª Dose' e '2ª Dose'? Retorne UF e diferença, incluindo todas as UFs presentes.",
        "SELECT paciente_endereco_uf AS uf, toInt64(countIf(vacina_descricao_dose = '1ª Dose')) - toInt64(countIf(vacina_descricao_dose = '2ª Dose')) AS diferenca FROM vacinacao WHERE paciente_endereco_uf != '' GROUP BY uf", "uf,diferenca")
    booster = "positionCaseInsensitiveUTF8(ifNull(vacina_descricao_dose,''), 'reforço') > 0"
    add(5, "Qual a razão entre o número de registros cuja descrição da dose contém 'reforço' (sem distinguir maiúsculas) e os de '1ª Dose'? Retorne apenas a razão, não percentual; nulo se denominador zero.",
        f"SELECT countIf({booster}) / nullIf(countIf(vacina_descricao_dose = '1ª Dose'),0) AS razao FROM vacinacao", "razao")
    add(6, "Qual o percentual de registros F e de registros M no campo paciente_enumSexoBiologico, usando somente F e M no denominador? Retorne as duas categorias e percentuais, nulo se não houver F/M.",
        " UNION ALL ".join(f"SELECT '{sexo}' AS sexo, 100.0 * countIf(paciente_enumSexoBiologico = '{sexo}') / nullIf(countIf(paciente_enumSexoBiologico IN ('F','M')),0) AS percentual FROM vacinacao" for sexo in ['F','M']), "sexo,percentual")
    extrema(7, "Entre faixas etárias presentes 0-18, 19-59 e 60+ anos, excluindo idades negativas, qual tem menos registros de vacinação?",
            f"SELECT {AGE_V} AS faixa, count() AS total FROM vacinacao WHERE paciente_idade >= 0 GROUP BY faixa", "faixa,total", low=True)
    extrema(8, "Quais municípios de residência (UF e código IBGE não vazios) têm a maior contagem de registros de vacinação?",
            "SELECT paciente_endereco_uf AS uf, paciente_endereco_coIbgeMunicipio AS municipio, count() AS total FROM vacinacao WHERE paciente_endereco_uf != '' AND notEmpty(ifNull(paciente_endereco_coIbgeMunicipio,'')) GROUP BY uf,municipio", "uf,municipio,total")
    add(9, "Qual a contagem de registros de vacinação por UF de residência não vazia e faixas 0-18, 19-59 e 60+ anos? Exclua idades negativas; retorne todos os grupos presentes, UF, faixa e total. Não conte pessoas distintas.",
        f"SELECT paciente_endereco_uf AS uf, {AGE_V} AS faixa, count() AS total FROM vacinacao WHERE paciente_endereco_uf != '' AND paciente_idade >= 0 GROUP BY uf,faixa", "uf,faixa,total")
    add(10, "Qual a contagem de registros de vacinação por sistema_origem? Retorne todos os grupos; mantenha nulos como nulos.",
        "SELECT sistema_origem, count() AS total FROM vacinacao GROUP BY sistema_origem", "sistema_origem,total")
    extrema(11, "Qual vacina_nome não vazio tem mais registros e qual o percentual desses registros sobre todas as linhas de vacinação? Retorne nome e percentual.",
            "SELECT vacina_nome AS vacina, 100.0 * count() / nullIf((SELECT count() FROM vacinacao),0) AS percentual FROM vacinacao WHERE notEmpty(ifNull(vacina_nome,'')) GROUP BY vacina", "vacina,percentual", metric="percentual")
    extrema(12, "Qual fabricante não vazio tem mais registros de vacinação?",
            "SELECT vacina_fabricante_nome AS fabricante, count() AS total FROM vacinacao WHERE notEmpty(ifNull(vacina_fabricante_nome,'')) GROUP BY fabricante", "fabricante,total")
    add(13, "Qual a contagem de registros de vacinação por ano e mês de aplicação? Retorne mes no formato AAAA-MM e total de todos os meses presentes; exclua datas nulas.",
        "SELECT formatDateTime(vacina_dataAplicacao,'%Y-%m') AS mes, count() AS total FROM vacinacao WHERE vacina_dataAplicacao IS NOT NULL GROUP BY mes", "mes,total")
    extrema(14, "Qual combinação de UF de residência não vazia e mês de aplicação (AAAA-MM) tem mais registros de vacinação? Exclua datas nulas.",
            "SELECT paciente_endereco_uf AS uf, formatDateTime(vacina_dataAplicacao,'%Y-%m') AS mes, count() AS total FROM vacinacao WHERE paciente_endereco_uf != '' AND vacina_dataAplicacao IS NOT NULL GROUP BY uf,mes", "uf,mes,total")
    add(15, "Quantos registros existem por descrição de dose que contenha 'reforço', sem distinguir maiúsculas? Preserve a descrição original e retorne todos os grupos.",
        f"SELECT vacina_descricao_dose AS dose, count() AS total FROM vacinacao WHERE {booster} GROUP BY dose", "dose,total")
    add(16, "Quantas UBS distintas estão cadastradas na base carregada, contando CNES positivos? Não inferir situação ativa.",
        "SELECT uniqExact(cnes) AS total FROM atencao_basica WHERE cnes > 0", "total",
        note="Original pede ativas; schema não possui situação. Versão revisada mede cadastradas.")
    ubase = "FROM atencao_basica WHERE cnes > 0"
    for i in (17,26):
        add(i, "Qual a contagem de CNES distintos positivos de UBS por código de UF não vazio? Retorne todos os grupos presentes.",
            f"SELECT uf, uniqExact(cnes) AS total {ubase} AND toString(uf) != '' GROUP BY uf", "uf,total")
    for i in (18,27):
        extrema(i, "Qual código de UF não vazio tem mais UBS distintas (CNES positivos)?",
                f"SELECT uf, uniqExact(cnes) AS total {ubase} AND toString(uf) != '' GROUP BY uf", "uf,total")
    add(19, "Quantos códigos de município positivos possuem pelo menos um CNES positivo na base de UBS?",
        f"SELECT uniqExact(ibge) AS total {ubase} AND ibge > 0", "total")
    for i in (20,21,30):
        extrema(i, "Quais códigos de município positivos têm " + ("menos" if i==30 else "mais") + " UBS distintas, contando CNES positivos nos municípios presentes na base?",
                f"SELECT ibge AS municipio, uniqExact(cnes) AS total {ubase} AND ibge > 0 GROUP BY municipio", "municipio,total", low=i==30)
    add(22, "Na base de UBS, qual a contagem de CNES distintos positivos por município positivo nas UFs de códigos 21 a 29 (Nordeste)? Retorne todos os municípios, código e total.",
        f"SELECT ibge AS municipio, uniqExact(cnes) AS total {ubase} AND ibge > 0 AND uf IN ('21','22','23','24','25','26','27','28','29') GROUP BY municipio", "municipio,total")
    coords = "latitude != 0 AND longitude != 0 AND latitude BETWEEN -90 AND 90 AND longitude BETWEEN -180 AND 180"
    add(23, "Quantas UBS distintas (CNES positivos) têm latitude e longitude não zero e dentro de [-90,90] e [-180,180]?",
        f"SELECT uniqExact(cnes) AS total {ubase} AND {coords}", "total",
        note="ETL converte coordenadas ausentes/inválidas em zero; não basta IS NOT NULL.")
    extrema(24, "Quais municípios positivos têm mais UBS distintas com CNES positivo e coordenadas não zero nos intervalos latitude [-90,90] e longitude [-180,180]?",
            f"SELECT ibge AS municipio, uniqExact(cnes) AS total {ubase} AND ibge > 0 AND {coords} GROUP BY municipio", "municipio,total")
    add(25, "Qual a contagem de CNES distintos positivos por UF, município e bairro não vazio da base UBS? Retorne todos os grupos; não una bairros homônimos de municípios diferentes.",
        f"SELECT uf, ibge AS municipio, bairro, uniqExact(cnes) AS total {ubase} AND toString(uf) != '' AND ibge > 0 AND trimBoth(bairro) != '' GROUP BY uf,municipio,bairro", "uf,municipio,bairro,total")
    add(28, "Quantas UBS distintas com CNES positivo possuem logradouro e bairro não vazios após remover espaços nas extremidades?",
        f"SELECT uniqExact(cnes) AS total {ubase} AND trimBoth(logradouro) != '' AND trimBoth(bairro) != ''", "total")
    add(29, "Qual a contagem de UBS distintas com CNES positivo por bairro no município IBGE 355030? Inclua todos os grupos, inclusive bairro vazio.",
        f"SELECT bairro, uniqExact(cnes) AS total {ubase} AND ibge = 355030 GROUP BY bairro", "bairro,total")
    add(31, "Quantas linhas de notificações existem na tabela SRAG carregada, sem filtrar classificação final?", "SELECT count() AS total FROM srag", "total")
    add(32, "Qual a contagem de linhas de SRAG por ano de dt_notific e sem_not, excluindo dt_notific = '1970-01-01'? Retorne todos os grupos.",
        "SELECT toYear(dt_notific) AS ano, sem_not AS semana, count() AS total FROM srag WHERE dt_notific != toDate('1970-01-01') GROUP BY ano,semana", "ano,semana,total")
    extrema(33, "Qual UF de notificação não vazia tem mais linhas de SRAG na base carregada?",
            "SELECT sg_uf_not AS uf, count() AS total FROM srag WHERE sg_uf_not != '' GROUP BY uf", "uf,total")
    add(34, "Qual a contagem de linhas de SRAG por UF de notificação não vazia? Retorne todas as UFs presentes.",
        "SELECT sg_uf_not AS uf, count() AS total FROM srag WHERE sg_uf_not != '' GROUP BY uf", "uf,total")
    add(35, "Quantos códigos de município de notificação positivos distintos existem nas linhas de SRAG?",
        "SELECT uniqExact(co_mun_not) AS total FROM srag WHERE co_mun_not > 0", "total")
    for i, condition, denom, desc in [(36,"hospital = 1","count()","hospital = 1 entre todas as linhas"),
                                     (38,"evolucao = 2 AND hospital = 1","countIf(hospital = 1)","evolucao = 2 entre as linhas com hospital = 1"),
                                     (39,"uti = 1","count()","uti = 1 entre todas as linhas")]:
        add(i,f"Qual o percentual de linhas de SRAG com {desc}? Retorne nulo se o denominador for zero.",
            f"SELECT 100.0 * countIf({condition}) / nullIf({denom},0) AS percentual FROM srag", "percentual")
    add(37,"Quantas linhas de SRAG possuem evolucao = 2?", "SELECT countIf(evolucao = 2) AS total FROM srag", "total")
    extrema(40,"Qual UF de notificação não vazia tem maior percentual de linhas com evolucao = 2, usando todas as linhas daquela UF no denominador?",
            "SELECT sg_uf_not AS uf, 100.0 * countIf(evolucao = 2) / count() AS percentual FROM srag WHERE sg_uf_not != '' GROUP BY uf", "uf,percentual", metric="percentual")
    symptoms=["febre","tosse","garganta","dispneia","diarreia","vomito"]
    add(41,"Retorne uma linha com as contagens de SRAG em que cada indicador vale 1, na ordem febre, tosse, garganta, dispneia, diarreia e vomito. Uma notificação pode contribuir para vários sintomas.",
        "SELECT " + ", ".join(f"countIf({c} = 1) AS {c}" for c in symptoms) + " FROM srag", ",".join(symptoms))
    extrema(42,"Qual faixa tem mais linhas de SRAG: 0-18, 19-59 ou 60+ anos? Use nu_idade_n como magnitude da idade e tp_idade 1=dias, 2=meses e 3=anos; exclua idade nula, negativa e unidades desconhecidas. Para este teste, converta dias dividindo por 365.25 e meses por 12; anos permanecem iguais. Use os intervalos [0,19), [19,60) e [60,infinito), com rótulos '0-18', '19-59' e '60+'.",
            f"SELECT {AGE_S} AS faixa, count() AS total FROM srag WHERE tp_idade IN (1,2,3) AND nu_idade_n IS NOT NULL AND nu_idade_n >= 0 GROUP BY faixa", "faixa,total",
            note="Conversão operacional aproximada explicitada na pergunta, não cálculo clínico de idade completa. Revisar codificação na fonte antes da validação científica.")
    conditions=["cardiopati","hematologi","hepatica","asma","diabetes","neurologic","pneumopati","imunodepre","renal","obesidade"]
    add(43,"Qual o percentual de linhas de SRAG com ao menos um dos indicadores cardiopati, hematologi, hepatica, asma, diabetes, neurologic, pneumopati, imunodepre, renal ou obesidade igual a 1, sobre todas as linhas? Nulo se não houver linhas.",
        "SELECT 100.0 * countIf(" + " OR ".join(f"{c} = 1" for c in conditions) + ") / nullIf(count(),0) AS percentual FROM srag", "percentual")
    add(44,"Quantas linhas de SRAG têm pcr_sars2 = 1 ou pos_pcrflu = 1? Conte cada linha apenas uma vez.",
        "SELECT countIf(pcr_sars2 = 1 OR pos_pcrflu = 1) AS total FROM srag", "total")
    extrema(45,"Entre os indicadores pcr_sars2, pos_pcrflu e pcr_vsr, qual possui mais linhas de SRAG com valor 1? Retorne o nome do indicador e a contagem.",
            " UNION ALL ".join(f"SELECT '{c}' AS agente, countIf({c} = 1) AS total FROM srag" for c in ["pcr_sars2","pos_pcrflu","pcr_vsr"]), "agente,total")
    for i,col in [(46,"LEITOS_EXISTENTES"),(47,"LEITOS_SUS"),(51,"UTI_TOTAL_EXIST")]:
        add(i,f"Qual a soma de {col} na tabela leitos na maior competência COMP global disponível? Conte leitos registrados, não vagas livres.",
            f"SELECT sum({col}) AS total FROM leitos WHERE {LATEST}", "total")
    for i,col in [(48,"LEITOS_SUS"),(52,"UTI_TOTAL_EXIST")]:
        add(i,f"Qual o percentual da soma de {col} sobre a soma de LEITOS_EXISTENTES na maior COMP global de leitos? Nulo se denominador zero.",
            f"SELECT 100.0 * sum({col}) / nullIf(sum(LEITOS_EXISTENTES),0) AS percentual FROM leitos WHERE {LATEST}", "percentual")
    for i,col,low in [(49,"LEITOS_EXISTENTES",False),(55,"UTI_NEONATAL_EXIST",True)]:
        extrema(i,f"Qual UF não vazia tem a {'menor' if low else 'maior'} soma de {col} na maior COMP global de leitos? Inclua UFs com total zero.",
                f"SELECT UF AS uf, sum({col}) AS total FROM leitos WHERE {LATEST} AND UF != '' GROUP BY UF", "uf,total",low=low)
    add(50,"Qual a soma de LEITOS_EXISTENTES por UF não vazia na maior COMP global? Retorne todas as UFs presentes.",
        f"SELECT UF AS uf, sum(LEITOS_EXISTENTES) AS total FROM leitos WHERE {LATEST} AND UF != '' GROUP BY UF", "uf,total")
    extrema(53,"Qual DS_TIPO_UNIDADE não vazio tem maior soma de LEITOS_EXISTENTES na maior COMP global?",
            f"SELECT DS_TIPO_UNIDADE AS tipo, sum(LEITOS_EXISTENTES) AS total FROM leitos WHERE {LATEST} AND DS_TIPO_UNIDADE != '' GROUP BY tipo", "tipo,total")
    beds=["UTI_ADULTO_EXIST","UTI_PEDIATRICO_EXIST","UTI_NEONATAL_EXIST","UTI_CORONARIANA_EXIST","UTI_QUEIMADO_EXIST"]
    add(54,"Retorne uma linha com as somas de UTI_ADULTO_EXIST, UTI_PEDIATRICO_EXIST, UTI_NEONATAL_EXIST, UTI_CORONARIANA_EXIST e UTI_QUEIMADO_EXIST nessa ordem, na maior COMP global de leitos.",
        "SELECT " + ", ".join(f"sum({c}) AS {c}" for c in beds) + f" FROM leitos WHERE {LATEST}", ",".join(beds))
    extrema(56,"Qual código TP_GESTAO não vazio reúne mais CNES distintos não vazios na maior COMP global de leitos? Retorne o código, sem classificá-lo como público, privado ou filantrópico.",
            f"SELECT TP_GESTAO AS gestao, uniqExact(CNES) AS total FROM leitos WHERE {LATEST} AND TP_GESTAO != '' AND CNES != '' GROUP BY gestao", "gestao,total",
            note="TP_GESTAO não é classificação de natureza jurídica. Pergunta revisada para códigos reais.")
    add(57,"Qual a soma de LEITOS_SUS, na maior COMP global de leitos, em linhas cujo código NATUREZA_JURIDICA, após remover espaços externos, começa com '2' ou '3'? Não use TP_GESTAO para esse filtro.",
        f"SELECT sum(LEITOS_SUS) AS total FROM leitos WHERE {LATEST} AND (startsWith(trimBoth(NATUREZA_JURIDICA),'2') OR startsWith(trimBoth(NATUREZA_JURIDICA),'3'))", "total",
        note="Pergunta revisada para filtro explícito de códigos. Não equivale automaticamente à formulação original sobre iniciativa privada; revisar classificação jurídica da fonte antes de interpretar como setor privado.")
    extrema(58,"Qual UF não vazia tem maior percentual da soma de LEITOS_SUS sobre LEITOS_EXISTENTES na maior COMP global? Exclua denominadores zero.",
            f"SELECT UF AS uf, 100.0 * sum(LEITOS_SUS) / sum(LEITOS_EXISTENTES) AS percentual FROM leitos WHERE {LATEST} AND UF != '' GROUP BY UF HAVING sum(LEITOS_EXISTENTES) > 0", "uf,percentual", metric="percentual")
    add(59,"Retorne REGIAO, soma de LEITOS_EXISTENTES e soma de LEITOS_SUS para todas as regiões não vazias na maior COMP global de leitos.",
        f"SELECT REGIAO AS regiao, sum(LEITOS_EXISTENTES) AS existentes, sum(LEITOS_SUS) AS sus FROM leitos WHERE {LATEST} AND REGIAO != '' GROUP BY REGIAO", "regiao,existentes,sus")
    extrema(60,"Qual combinação de UF e código CO_IBGE não vazios tem maior soma de LEITOS_EXISTENTES na maior COMP global?",
            f"SELECT UF AS uf, CO_IBGE AS municipio, sum(LEITOS_EXISTENTES) AS total FROM leitos WHERE {LATEST} AND UF != '' AND CO_IBGE != '' GROUP BY UF,CO_IBGE", "uf,municipio,total")
    add(61,"Quantos códigos positivos de município de notificação de SRAG também aparecem na base UBS com CNES positivo? Conte municípios distintos por igualdade dos códigos.",
        "SELECT count() AS total FROM (SELECT DISTINCT co_mun_not AS municipio FROM srag WHERE co_mun_not > 0) s INNER JOIN (SELECT DISTINCT ibge AS municipio FROM atencao_basica WHERE ibge > 0 AND cnes > 0) u ON s.municipio = u.municipio", "total",datasets=[S,U],relations=["srag_ubs_municipio_notificacao"])
    add(62,"Liste todos os municípios positivos presentes em SRAG e UBS, com número de linhas de notificações e número de CNES distintos positivos. Ordene por notificações decrescentes e código municipal crescente, sem limitar a quantidade de linhas.",
        "WITH s AS (SELECT co_mun_not AS municipio, count() AS notificacoes FROM srag WHERE co_mun_not > 0 GROUP BY municipio), u AS (SELECT ibge AS municipio, uniqExact(cnes) AS ubs FROM atencao_basica WHERE ibge > 0 AND cnes > 0 GROUP BY municipio) SELECT s.municipio, s.notificacoes, u.ubs FROM s INNER JOIN u ON s.municipio=u.municipio ORDER BY s.notificacoes DESC,s.municipio ASC", "municipio,notificacoes,ubs",datasets=[S,U],relations=["srag_ubs_municipio_notificacao"],ordered=True)
    for i in (63,64):
        add(i,"Para todas as UFs não vazias comuns à vacinação e aos leitos, retorne UF, contagem de registros por UF de residência em toda a vacinação carregada e soma de UTI_TOTAL_EXIST na maior COMP global dos leitos. Inclua somente UFs com soma de UTI positiva; agregue antes de juntar.",
            f"WITH v AS (SELECT paciente_endereco_uf AS uf, count() AS doses FROM vacinacao WHERE paciente_endereco_uf != '' GROUP BY uf), b AS (SELECT UF AS uf, sum(UTI_TOTAL_EXIST) AS leitos FROM leitos WHERE {LATEST} AND UF != '' GROUP BY UF HAVING sum(UTI_TOTAL_EXIST)>0) SELECT v.uf,v.doses,b.leitos FROM v INNER JOIN b ON v.uf=b.uf", "uf,doses,leitos", datasets=[V,B],relations=["vacinacao_leitos_uf"])
    for i, ds in [(65,[S,B]),(66,[S,B]),(67,[U,V]),(68,[S,U,B])]:
        add(i,original[i],None,"",datasets=ds,note="Relacionamento não implementado; teste de limitação, não acurácia numérica. Q68 também exige limiares de alto/baixo e harmonização municipal.")
        cases[i].update(expected_behavior="limitation",implementation_supported=False)
        cases[i]["expected_missing_data"]=["relacionamento semântico validado entre as bases selecionadas"]
    assert set(cases)==set(range(1,69))
    for c in cases.values():
        if not c["reference_sql"]:
            c["columns"]=[]
    seen = {}
    for c in cases.values():
        rules = {}
        for index, name in enumerate(c['columns']):
            if name == 'percentual':
                rules[str(index)] = dict(absolute_tolerance=0.005)
            elif name == 'razao':
                rules[str(index)] = dict(absolute_tolerance=0.000001)
                c['question'] += ' Retorne a razão com pelo menos seis casas decimais.'
        if c['id'] == 32:
            rules['0'] = dict(normalization='year')
        if c['id'] == 45:
            rules['0'] = dict(normalization='casefold')
        c['comparison']['columns'] = rules
        if c['question'] in seen:
            c['repeat_of'] = seen[c['question']]
        else:
            seen[c['question']] = c['id']
    return dict(version=VERSION, revision_notes="Contrato de saída explícito; tolerâncias por coluna; normalização restrita a ano e nome de indicador; conversão de idade explicitada; duplicatas marcadas. Protocolo novo, sem reclassificação das rodadas v2; revisão humana pendente.", status="draft", global_specification=GLOBAL, cases=list(cases.values()))
