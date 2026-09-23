"""Conservative checks of explicit requests, not a semantic correctness oracle."""
import re
import unicodedata

from sqlglot import exp, parse_one


def normalize(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text.lower())
                   if not unicodedata.combining(c))


SQL_INSTRUCTIONS = """
Contrato analítico (prevalece sobre exemplos):
- Conte a entidade pedida: registros com COUNT(*), entidades distintas com COUNT(DISTINCT chave).
- Capacidade de leitos exige SUM, não COUNT de linhas nem MAX de uma linha.
- Preserve todos os filtros, indicadores, período e agrupamentos da pergunta.
- Aplique cada filtro à entidade mencionada. Código de município/CNES positivo
  significa código > 0; não acrescente filtro de teste laboratorial positivo.
- Ano/mês deve distinguir os anos; semana epidemiológica usa seu campo e ano.
- Para maior/menor, retorne somente os extremos, incluindo empates, usando uma CTE
  agregada e comparação com MAX/MIN da métrica. Não devolva o ranking inteiro.
- Não invente LIMIT. Use limite apenas quando solicitado; 'todos' inclui empates.
- Retorne somente as dimensões e métricas pedidas, sem contagens extras.
- Proteja denominadores com NULLIF(denominador, 0); resultado indefinido é NULL.
- Percentual/porcentagem deve estar na escala 0 a 100: 100.0 * numerador / denominador.
  Razão/proporção sem pedido de percentual permanece na escala de razão.
- Use parênteses para agrupar alternativas OR sob filtros comuns com AND.
- Indicadores simultâneos não são categorias exclusivas: não use CASE que perde sobreposições.
- Para 'ao menos um' indicador positivo, conte cada linha uma única vez:
  COUNTIF(indicador_a = 1 OR indicador_b = 1). Não some contagens individuais.
- Diferencie NULL de texto vazio. Respeite os rótulos literais e sua capitalização.
- Categoria literal exige igualdade exata. Use busca parcial (LIKE/position) apenas
  para a categoria cujo enunciado pede 'contém'; não estenda a busca às outras categorias.
- Dê às agregações aliases distintos dos campos físicos (ex.: total_febre, não febre),
  pois o ClickHouse pode substituir o alias no WHERE e rejeitar a consulta.
- IS NOT NULL não exclui ''. Para texto não vazio, use coluna != '' ou notEmpty(coluna).
- Coordenadas não zero exigem latitude != 0 E longitude != 0, além dos intervalos.
- positionCaseInsensitiveUTF8 recebe primeiro o texto/coluna e depois o trecho buscado.
- Percentuais por categoria sobre um total compartilhado exigem denominador global
  (subconsulta ou janela), não o total da própria categoria agrupada.
- Preserve formatos explicitados: AAAA-MM usa formatDateTime(data, '%Y-%m'),
  não um inteiro AAAAMM. Nomes de indicadores retornados como texto devem manter a grafia pedida.
- Idade exige magnitude e unidade; não suponha que todo valor esteja em anos.
- Aceite SELECT ou WITH. Se não puder atender à intenção, não substitua por outra consulta.
"""


def prepare_sql(sql, question):
    """Only a requested null-on-zero rewrite; never guess filters or grouping."""
    tree = parse_one(sql, read='clickhouse')
    q = normalize(question)
    if 'nulo' in q or 'null' in q:
        for division in tree.find_all(exp.Div):
            denominator = division.expression
            if not isinstance(denominator, exp.Nullif):
                division.set('expression', exp.Nullif(this=denominator.copy(), expression=exp.Literal.number(0)))
    return tree.sql(dialect='clickhouse')


def contract_errors(sql, question, columns=()):
    """Detect a few explicit violations; passing does not establish correctness."""
    try:
        tree = parse_one(sql, read='clickhouse')
    except Exception:
        return ['SQL não pôde ser analisado']
    q = normalize(question)
    errors = []
    # Technical field names explicitly requested must not disappear.
    used = {c.name.lower() for c in tree.find_all(exp.Column)}
    if (re.match(r'qual (?:e )?o percentual de linhas\b', q)
            and not re.search(r'\bpor\b|retorne (?:tambem|a contagem)|e (?:o total|a contagem)', q)
            and len(tree.expressions) != 1):
        errors.append('A pergunta pede somente um percentual: projete apenas essa métrica, sem contagens auxiliares')
    scale_question = re.sub(r'nao (?:em )?(?:percentual|porcentagem|percentagem)', '', q)
    if re.search(r'percentual|porcentagem|percentagem|%', scale_question) and next(tree.find_all(exp.Div), None):
        scalars = {literal.this for literal in tree.find_all(exp.Literal) if not literal.is_string}
        if not scalars.intersection({'100', '100.0', '0.01'}):
            errors.append('Percentual exige escala 0 a 100, não apenas a razão; multiplique o numerador por 100.0')
    if re.search(r'nao (?:em )?percentual', q) and re.search(r'\brazao\b', q):
        for multiplication in tree.find_all(exp.Mul):
            if any(isinstance(value, exp.Literal) and value.this in {'100','100.0'}
                   for value in (multiplication.this, multiplication.expression)):
                errors.append('Foi pedida razão, não percentual: não multiplique por 100')
                break
    if 'sem distinguir maiusculas' in q:
        for like in tree.find_all(exp.Like):
            if not isinstance(like, exp.ILike) and 'lower' not in like.sql().lower():
                errors.append('LIKE distingue maiúsculas: use busca sem distinção de caixa')
    for function in tree.find_all(exp.Anonymous):
        if function.name.lower() == 'positioncaseinsensitiveutf8':
            args = function.expressions
            if len(args) == 2 and isinstance(args[0], exp.Literal) and list(args[1].find_all(exp.Column)):
                errors.append('positionCaseInsensitiveUTF8: coluna/texto primeiro, trecho buscado depois')
    if re.search(r'ao menos um|pelo menos um|qualquer um', q):
        conditional_counts = [agg for agg in tree.find_all(exp.AggFunc)
            if isinstance(agg, (exp.Sum, exp.CountIf)) and list(agg.find_all(exp.Column))]
        if len(conditional_counts) > 1 and next(tree.find_all(exp.Add), None):
            errors.append('Não some contagens de indicadores sobrepostos; conte linhas com OR entre os indicadores, uma vez por linha')
    for column in columns:
        if re.search(r'nao (?:use|utilize)\s+' + re.escape(column.lower()) + r'\b', q):
            if column.lower() in used:
                errors.append('Campo explicitamente excluído: ' + column)
            continue
        if re.search(r'\b' + re.escape(column.lower()) + r'\b', question.lower()) and column.lower() not in used:
            errors.append('Campo solicitado ausente: ' + column)
    if re.search(r'sem limit|todos os|todas as|inclua todos', q) and tree.args.get('limit'):
        errors.append('LIMIT externo contradiz pedido de resultado completo/empates')
    if ('ano/mes' in q or 'ano e mes' in q) and 'year' not in sql.lower() and not re.search(r'%[Yy]|YYYY|toStartOfMonth', sql):
        errors.append('Agrupamento mensal deve preservar o ano')
    if 'empatad' in q and tree.args.get('group') and not tree.args.get('having') and not tree.args.get('qualify'):
        errors.append('Agregação simples não seleciona somente extremos empatados; use CTE e MAX/MIN')
    if re.search(r'maior (?:competencia|comp)\b|competencia mais recente', q):
        def constrains_period(node):
            if isinstance(node, exp.Paren):
                return constrains_period(node.this)
            if isinstance(node, exp.And):
                return constrains_period(node.this) or constrains_period(node.expression)
            if isinstance(node, exp.Or):
                return constrains_period(node.this) and constrains_period(node.expression)
            return any(c.name.lower() == 'comp' for c in node.find_all(exp.Column))
        # Check physical bed scans, including scans inside CTEs, but not MAX(COMP) subqueries.
        for select in tree.find_all(exp.Select):
            source = select.args.get('from_') or select.args.get('from')
            if not source or not isinstance(source.this, exp.Table) or source.this.name.lower() != 'leitos':
                continue
            if len(select.expressions) == 1 and isinstance(select.expressions[0].unalias(), exp.Max):
                continue
            where = select.args.get('where')
            if not where or not constrains_period(where.this):
                errors.append('Filtro de competência ausente em uma alternativa OR; agrupe as alternativas sob o filtro temporal')
    return errors
