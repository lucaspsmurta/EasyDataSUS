"""Small closed grammar: unmatched requests must go to the LLM or fail explicitly."""
import re
from services.analytical_contract import normalize


def fallback_sql(question, dataset='covid-19-vacinacao'):
    q = normalize(question).strip(' ?.').strip()
    if dataset == 'leitos':
        latest = 'COMP = (SELECT MAX(COMP) FROM leitos)'
        period = r'(?: na competencia mais recente)?'
        match = re.fullmatch(r'quais (?:cidades|municipios) (?:tem|possuem) (?:leitos de )?uti neonatal' + period, q)
        if match:
            return f'SELECT DISTINCT MUNICIPIO, UF FROM leitos WHERE UTI_NEONATAL_EXIST > 0 AND {latest} ORDER BY UF, MUNICIPIO'
        match = re.fullmatch(r'qual (?:e )?a quantidade de leitos de uti por (estado|regiao)' + period, q)
        if match:
            column = 'UF' if match.group(1) == 'estado' else 'REGIAO'
            return f'SELECT {column}, SUM(UTI_TOTAL_EXIST) AS total_uti_beds FROM leitos WHERE {latest} GROUP BY {column} ORDER BY total_uti_beds DESC, {column}'
        match = re.fullmatch(r'qual (?:e )?a proporcao de leitos sus em relacao ao total de leitos existentes por (estado|regiao)' + period, q)
        if match:
            column = 'UF' if match.group(1) == 'estado' else 'REGIAO'
            return f'SELECT {column}, SUM(LEITOS_SUS) AS leitos_sus, SUM(LEITOS_EXISTENTES) AS leitos_totais, 100.0 * SUM(LEITOS_SUS) / NULLIF(SUM(LEITOS_EXISTENTES), 0) AS percentual_sus FROM leitos WHERE {latest} GROUP BY {column} ORDER BY {column}'
        return None
    # Only these complete noun phrases are accepted. Unknown filters cannot be discarded.
    nouns = {
        'surtos-srag': (r'(?:casos|notificacoes|registros)(?: de srag)?', 'srag', 'SG_UF_NOT', 'co_mun_not', 'COUNT(*)'),
        'covid-19-vacinacao': (r'(?:doses|vacinas|registros de vacinacao)(?: de vacina)?(?: contra (?:a )?covid-19)?', 'vacinacao', 'paciente_endereco_uf', 'paciente_endereco_coIbgeMunicipio', 'COUNT(*)'),
        'atencao-basica': (r'(?:ubs|unidades basicas de saude)', 'atencao_basica', 'uf', 'ibge', 'COUNT(DISTINCT cnes)'),
    }
    if dataset not in nouns:
        return None
    noun, table, state, municipality, metric = nouns[dataset]
    extrema_noun = noun
    if dataset == 'covid-19-vacinacao':
        extrema_noun = r'doses(?: registradas)?(?: contra (?:a )?covid-19)?'
    extreme = re.fullmatch(r'quais (estados|municipios) (?:possuem|tem) (?:o )?(maior|menor) numero de ' + extrema_noun, q)
    if extreme:
        column = state if extreme.group(1) == 'estados' else municipality
        if dataset == 'atencao-basica':
            column, metric = column.upper(), 'COUNT(DISTINCT CNES)'
        alias = {'atencao-basica':'total_ubs', 'covid-19-vacinacao':'total_doses', 'surtos-srag':'total_srag'}[dataset]
        function = 'MAX' if extreme.group(2) == 'maior' else 'MIN'
        return f'WITH grouped AS (SELECT {column}, {metric} AS {alias} FROM {table} GROUP BY {column}) SELECT {column}, {alias} FROM grouped WHERE {alias} = (SELECT {function}({alias}) FROM grouped) ORDER BY {column}'
    prefix = r'(?:quant[ao]s |qual (?:e )?(?:o total|a quantidade|o numero) de |qual (?:e )?a distribuicao de )'
    suffix = r'(?: foram (?:registrad[ao]s|aplicad[ao]s|notificad[ao]s)| existem)?(?: no conjunto de dados carregado| na base carregada)?'
    if dataset == 'covid-19-vacinacao':
        state_match = re.fullmatch(prefix + noun + suffix + r' em ([a-z]{2})', q)
        if state_match and state_match.group(1).upper() in {'AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO'}:
            return f"SELECT COUNT(*) AS total_registros FROM vacinacao WHERE paciente_endereco_uf = '{state_match.group(1).upper()}'"
    match = re.fullmatch(prefix + noun + suffix + r'(?: por (estado|uf|municipio))?', q)
    if match:
        dimension = match.group(1)
        if "distribuicao" in q and not dimension:
            return None
        if dimension:
            column = municipality if dimension == 'municipio' else state
            return f'SELECT {column}, {metric} AS total FROM {table} GROUP BY {column} ORDER BY total DESC, {column} ASC'
        return f'SELECT {metric} AS total_registros FROM {table}'
    # Distinct municipalities are different from rows; no additional filters accepted.
    if re.fullmatch(r'quantos municipios (?:possuem|tem|registram) ' + noun, q):
        return f"SELECT COUNT(DISTINCT {municipality}) AS total_municipios FROM {table} WHERE toString({municipality}) NOT IN ('', '0')"
    return None
