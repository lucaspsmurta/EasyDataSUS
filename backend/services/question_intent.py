"""Extract explicit analytical cues without supplying benchmark answers."""
import json
import re
import unicodedata


def analytical_intent(question):
    q = ''.join(c for c in unicodedata.normalize('NFKD', question.lower())
                if not unicodedata.combining(c))
    cues = []
    if re.search(r'por mes|cada mes|mes e ano|ano e mes', q):
        cues.append('Agrupamento mensal: distinguir mês e ano; não agrupar por dia.')
    if 'semana' in q and 'notifica' in q:
        cues.append('Agrupamento por ano de notificação e semana registrada, não por mês e semana.')
    if 'faixa' in q and ('etaria' in q or 'idade' in q):
        cues.append('Preservar as faixas etárias solicitadas, com todos os limites explícitos.')
    if re.search(r'porcentagem|percentual', q):
        cues.append('Medida percentual: escala 0 a 100; identificar o denominador na pergunta.')
    if re.search(r'para cada registro|registros.*por ubs|razao', q):
        cues.append('Medida de razão: numerador dividido pelo denominador indicado, não apenas uma contagem.')
    if 'hospitaliza' in q and re.search(r'entre as notificacoes|das notificacoes', q) and 'porcentagem' in q:
        cues.append('Se o universo pedido é o de hospitalizadas, denominador restrito a hospitalização; óbitos são subconjunto desse universo, não união OR.')
    if re.search(r'mais (?:registros|ubs|leitos|notificacoes)|maior|menor|menos (?:registros|leitos)', q):
        cues.append('Seleção de extremo da métrica: não devolver todos os grupos como ranking.')
    if 'empate' in q:
        cues.append('Preservar todos os empates do extremo solicitado.')
    if 'mais recente' in q:
        cues.append('Recorte temporal solicitado: levantamento mais recente da base correspondente.')
    if re.search(r'todo o periodo|todos os dados|toda a vacinacao', q):
        cues.append('Não inventar um filtro temporal adicional nas bases cujo período completo foi pedido.')
    requirements = []
    def require(kind, pattern, instruction):
        matches = list(re.finditer(pattern, q))
        if kind == 'distinct_entities':
            matches = [m for m in matches if not re.search(
                r'\b(?:nao|nem)\s+(?:(?:contando|conte|contar)\s+)?$', q[:m.start()])]
        if matches:
            requirements.append({'kind': kind, 'evidence': [m.group() for m in matches],
                                 'instruction': instruction})
    require('ratio', r'para cada (?:registro|dose|pessoa|unidade)|por ubs|\brazao\b',
            'Identificar numerador e denominador pela ordem e pelo sentido do pedido. '
            'Produzir uma divisão; agrupar categorias e devolver contagens não responde à razão.')
    require('percentage', r'porcentagem|percentual|percentagem',
            'Definir explicitamente o universo do denominador antes dos filtros do numerador. '
            'Aplicar filtros comuns aos dois; filtros do evento apenas ao numerador. '
            'Valores desconhecidos permanecem no denominador quando isso for solicitado.')
    require('monthly', r'por mes|cada mes|mes e ano|ano e mes',
            "Agrupar pela data transformada em ano-mês, não por dia. Usar formatDateTime(data, '%Y-%m') para apresentação mensal.")
    require('weekly', r'cada semana|por semana|semanas de notificacao',
            'Usar ano e semana registrada quando essa for a referência solicitada; não acrescentar mês ao agrupamento.')
    require('age_groups', r'faixas? etarias?|faixas? de .*?anos',
            'Construir idade em anos conforme unidade dos metadados antes de aplicar limites. '
            'Unidade da idade não é faixa etária. Usar CASE com limites da pergunta; projetar a faixa e incluí-la no GROUP BY junto das outras dimensões.')
    require('extreme', r'maior|menor|mais (?:registros|leitos|ubs|notificacoes)|menos (?:registros|leitos|ubs|notificacoes)',
            'Separar agregação e seleção: CTE com uma linha por grupo e métrica; '
            'consulta externa filtra métrica = (SELECT MAX(métrica) ou MIN(métrica) FROM CTE). '
            'ORDER BY apenas ordena, não seleciona o extremo. Não aninhar MAX(SUM(...)) no mesmo SELECT.')
    require('common_entities', r'(?:tanto|simultaneamente).*(?:quanto|e)|presentes (?:tanto|nas|em ambas)|que tem .* e ',
            'Se o pedido exige presença nas duas bases, usar interseção das chaves (INNER JOIN), '
            'agregando cada base na granularidade de junção antes de combinar. '
            'Não trocar por LEFT JOIN, que inclui entidades sem correspondência.')
    require('distinct_entities', r'(?:ubs|estabelecimentos|pessoas|municipios|unidades) (?:diferentes|distint[oa]s)|cada (?:ubs|unidade) uma vez',
            'Contar identificadores da entidade definidos nos metadados, não nomes nem linhas indiscriminadamente.')
    require('latest_snapshot', r'levantamento mais recente|competencia mais recente',
            'Calcular a competência máxima da base correspondente e filtrar todas as alternativas pelo mesmo período. '
            'Usar o campo físico documentado para competência; não criar uma coluna chamada competencia. '
            'O filtro desse período deve valer para todas as alternativas OR, agrupadas entre parênteses.')
    require('difference', r'\bdiferenca entre\b',
            'Quando forem categorias da mesma base, calcular as duas contagens condicionalmente por grupo e subtrair na ordem pedida; não perder grupos com contagem zero.')
    return {'question': question, 'explicit_cues': cues, 'requirements': requirements,
            'policy': 'Não inventar local, período, denominador ou unidade de contagem. '
                      'Preservar a pergunta inteira; os indícios não substituem sua leitura.'}


def intent_context(question):
    context = analytical_intent(question)
    # The surrounding generation prompt already contains the complete question.
    context.pop('question')
    context.pop('explicit_cues')
    return 'Intenção analítica identificada (indícios explícitos):\n' + json.dumps(
        context, ensure_ascii=False) + '''
Antes de emitir o SQL, confira internamente:
1. Qual entidade/medida foi solicitada? Qual campo ou expressão a representa nos metadados?
2. Quais dimensões precisam aparecer juntas no resultado? Não omitir nenhuma.
3. Quais filtros são do universo, do numerador e da seleção final de grupos?
4. Toda exigência explícita acima está representada no SQL?
As instruções são padrões de operação, não consultas prontas: substitua os nomes conceituais
somente pelos campos documentados. A pergunta e os metadados prevalecem sobre os indícios.
Não acrescente filtros territoriais ou temporais, nem complete ambiguidades com suposições.
Retorne apenas o SQL final, sem expor estas etapas de conferência.
'''
