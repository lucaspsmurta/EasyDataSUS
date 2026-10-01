"""Reproducible, AI-assisted editorial revision of the 68-question v4 catalog.

This authors new questions; it is not a blind quality evaluation. Existing SQL
references inform wording for 1–64 and are preserved, not newly validated.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = 'reference-v5-questions'

SCOPES = {
    'vaccination': 'Considere todos os registros da base de vacinação contra COVID-19 carregada, sem recorte adicional de data ou local. Conte registros de aplicação, não pessoas distintas. ',
    'ubs': 'Considere o cadastro de UBS carregado, sem inferir situação ativa ou cobertura nacional. Conte UBS por CNES distinto e positivo. ',
    'srag': 'Considere todas as linhas da base SRAG carregada, em todo o período disponível, sem filtro de classificação final. Cada linha conta como uma notificação, sem deduplicação de pessoas ou episódios. ',
    'beds': 'Considere somente as linhas da base de leitos na maior competência COMP global disponível, a mesma para todos os grupos. As quantidades representam leitos cadastrados, não vagas livres. ',
}

# Each entry is deliberately authored; no LLM or SQL is executed by this module.
BODIES = {
1: 'Quantos registros de aplicação existem no total?',
2: "Entre as UFs de residência com sigla não nula e diferente da string vazia, qual tem a maior contagem de registros cuja descrição de dose é exatamente '1ª Dose'?",
3: "Quantos registros têm descrição de dose exatamente igual a '2ª Dose'?",
4: "Para cada UF de residência com sigla não nula e diferente da string vazia, calcule a contagem de registros de '1ª Dose' menos a contagem de '2ª Dose', usando essas descrições exatas. Inclua todas as UFs presentes, mesmo quando uma ou ambas as contagens forem zero.",
5: "Qual é a razão entre a contagem de registros cuja descrição da dose contém 'reforço', sem distinguir maiúsculas de minúsculas, e a contagem com descrição exatamente '1ª Dose'? Retorne razão, não percentual, com pelo menos seis casas decimais; retorne nulo se o denominador for zero.",
6: "Qual é o percentual de registros com paciente_enumSexoBiologico igual a F e igual a M? Use como denominador somente a soma dos registros F e M, excluindo outras categorias. Retorne as duas categorias; se o denominador for zero, seus percentuais devem ser nulos.",
7: "Entre as faixas de idade 0 a 18, 19 a 59 e 60 anos ou mais presentes nos registros, qual tem a menor contagem? Use paciente_idade em anos e exclua idades nulas ou negativas. Não inclua faixas sem registros; use os rótulos 0-18, 19-59 e 60+.",
8: 'Quais combinações de UF e código IBGE de residência têm a maior contagem de registros? Exclua UF ou código municipal nulo ou igual à string vazia; identifique o município pelo código acompanhado da UF.',
9: 'Qual é a contagem por UF de residência e faixa etária de 0 a 18, 19 a 59 e 60 anos ou mais? Use paciente_idade em anos; exclua idades nulas ou negativas e UFs nulas ou iguais à string vazia. Inclua todos os grupos presentes e use os rótulos 0-18, 19-59 e 60+.',
10: 'Qual é a contagem de registros por sistema_origem? Retorne todos os grupos, incluindo valores nulos como um grupo nulo e strings vazias como um grupo separado.',
11: 'Qual vacina_nome não nulo e diferente da string vazia tem a maior contagem de registros, e qual é o percentual desse grupo sobre todas as linhas da base, incluindo no denominador aquelas sem nome de vacina? Retorne o nome da vacina e o percentual.',
12: 'Qual fabricante tem a maior contagem de registros? Agrupe por vacina_fabricante_nome, excluindo valores nulos e iguais à string vazia; preserve os demais nomes como estão armazenados.',
13: 'Qual é a contagem por ano e mês da data de aplicação vacina_dataAplicacao? Exclua datas nulas, inclua todos os meses presentes e identifique cada mês no formato AAAA-MM.',
14: 'Qual combinação de UF de residência e ano/mês de aplicação tem a maior contagem de registros? Exclua UFs nulas ou iguais à string vazia e datas de aplicação nulas. Identifique o mês no formato AAAA-MM.',
15: "Qual é a contagem por descrição de dose que contenha 'reforço', sem distinguir maiúsculas de minúsculas na seleção? Preserve a descrição original no agrupamento e retorne todos os grupos encontrados.",
16: 'Quantas UBS distintas existem nesse cadastro?',
17: 'Qual é a contagem de UBS por código de UF? Exclua código de UF nulo ou cuja representação textual seja vazia e inclua todos os códigos presentes, sem convertê-los em siglas.',
18: 'Qual código de UF tem a maior contagem de UBS? Exclua código de UF nulo ou cuja representação textual seja vazia; retorne o código, sem convertê-lo em sigla.',
19: 'Quantos códigos IBGE de município distintos e positivos possuem pelo menos uma UBS com CNES positivo?',
20: 'Entre os municípios com código IBGE positivo e pelo menos uma UBS com CNES positivo, quais têm a maior contagem de UBS? Identifique cada município pelo código IBGE.',
21: 'Entre os municípios com código IBGE positivo e pelo menos uma UBS com CNES positivo, quais têm a maior contagem de UBS? Identifique cada município pelo código IBGE.',
22: 'Qual é a contagem de UBS por código IBGE positivo de município nas UFs de códigos 21, 22, 23, 24, 25, 26, 27, 28 e 29, correspondentes ao Nordeste? Inclua todos os municípios encontrados nesse recorte.',
23: 'Quantas UBS têm pelo menos um registro com latitude diferente de zero e entre -90 e 90, e longitude diferente de zero e entre -180 e 180, incluindo os limites? As duas condições devem ocorrer na mesma linha; essa regra é um critério operacional de preenchimento, não validação da localização real.',
24: 'Quais municípios de código IBGE positivo têm a maior contagem de UBS com pelo menos uma linha contendo latitude diferente de zero e entre -90 e 90 e longitude diferente de zero e entre -180 e 180, incluindo os limites? As condições devem ocorrer na mesma linha. Considere somente municípios com UBS que atendam ao filtro.',
25: 'Qual é a contagem de UBS por código de UF, código IBGE municipal e bairro? Exclua UF nula ou cuja representação textual seja vazia, município não positivo e bairro nulo ou vazio após remover espaços nas extremidades. Preserve o nome original do bairro no agrupamento; não una bairros homônimos de municípios diferentes. Retorne todos os grupos presentes.',
26: 'Qual é a contagem de UBS por código de UF? Exclua código de UF nulo ou cuja representação textual seja vazia e inclua todos os códigos presentes, sem convertê-los em siglas.',
27: 'Qual código de UF tem a maior contagem de UBS? Exclua código de UF nulo ou cuja representação textual seja vazia; retorne o código, sem convertê-lo em sigla.',
28: 'Quantas UBS têm pelo menos uma linha com logradouro e bairro ambos não nulos e não vazios após remover espaços nas extremidades? As duas condições devem ocorrer na mesma linha.',
29: 'Qual é a contagem de UBS por bairro no município cujo código IBGE armazenado é 355030? Preserve os bairros como armazenados e inclua todos os grupos, inclusive bairro vazio ou nulo, se presentes.',
30: 'Entre os municípios de código IBGE positivo com pelo menos uma UBS de CNES positivo, quais têm a menor contagem de UBS? Não inclua municípios ausentes do cadastro nem atribua zero a eles.',
31: 'Quantas linhas de notificações existem no total?',
32: "Qual é a contagem por ano da data de notificação dt_notific e valor da semana sem_not? Exclua dt_notific nula ou igual a '1970-01-01'. Use sem_not como armazenada, sem recalcular a semana; retorne todos os grupos presentes.",
33: 'Qual UF de notificação, identificada por sg_uf_not não nula e diferente da string vazia, tem a maior contagem de linhas? Não use a UF de residência.',
34: 'Qual é a contagem de linhas por UF de notificação sg_uf_not? Exclua UF nula ou igual à string vazia, retorne todas as UFs presentes e não use a UF de residência.',
35: 'Quantos códigos de município de notificação co_mun_not distintos e positivos aparecem na base? Não conte municípios de residência.',
36: 'Qual é o percentual de linhas com hospital = 1 sobre todas as linhas? Mantenha registros com hospital nulo ou desconhecido no denominador. Multiplique a razão por 100 e retorne nulo se não houver linhas.',
37: 'Quantas linhas têm evolucao = 2? Conte somente esse código, sem inferir desfechos para valores ausentes ou diferentes.',
38: 'Entre as linhas com hospital = 1, qual é o percentual que também tem evolucao = 2? O denominador inclui todas as linhas com hospital = 1, inclusive evolução nula ou desconhecida. Multiplique a razão por 100 e retorne nulo se o denominador for zero.',
39: 'Qual é o percentual de linhas com uti = 1 sobre todas as linhas? Mantenha uti nula ou desconhecida no denominador. Multiplique a razão por 100 e retorne nulo se não houver linhas.',
40: 'Qual UF de notificação sg_uf_not não nula e diferente da string vazia tem o maior percentual de linhas com evolucao = 2? Use todas as linhas de cada UF no respectivo denominador, inclusive evolução nula ou desconhecida, e multiplique a razão por 100.',
41: 'Quantas linhas têm valor 1 em cada indicador febre, tosse, garganta, dispneia, diarreia e vomito? Conte cada indicador separadamente; uma mesma linha pode contribuir para vários indicadores. Retorne uma única linha com as seis contagens.',
42: "Qual faixa etária presente tem a maior contagem de linhas: 0-18, 19-59 ou 60+? Para este teste, use nu_idade_n como magnitude e tp_idade 1=dias, 2=meses e 3=anos. Exclua magnitudes nulas ou negativas e unidades diferentes de 1, 2 ou 3. Converta dias dividindo por 365.25 e meses por 12; anos permanecem iguais. Classifique nos intervalos [0,19), [19,60) e [60,infinito), com rótulos '0-18', '19-59' e '60+'. Trata-se de conversão operacional aproximada.",
43: 'Qual é o percentual de linhas com pelo menos um dos indicadores cardiopati, hematologi, hepatica, asma, diabetes, neurologic, pneumopati, imunodepre, renal ou obesidade igual a 1? Conte cada linha uma vez no numerador e use todas as linhas no denominador, inclusive valores nulos ou desconhecidos. Multiplique a razão por 100 e retorne nulo se não houver linhas.',
44: 'Quantas linhas têm pcr_sars2 = 1 ou pos_pcrflu = 1? Conte uma linha apenas uma vez, mesmo quando os dois indicadores forem iguais a 1.',
45: 'Entre pcr_sars2, pos_pcrflu e pcr_vsr, qual indicador tem a maior contagem de linhas com valor 1? Compare os três indicadores, inclusive os que tenham contagem zero; uma linha pode contribuir para mais de um indicador. Retorne o nome do indicador e sua contagem.',
46: 'Qual é a soma de LEITOS_EXISTENTES em todas as linhas dessa competência?',
47: 'Qual é a soma de LEITOS_SUS em todas as linhas dessa competência?',
48: 'Qual é o percentual da soma de LEITOS_SUS sobre a soma de LEITOS_EXISTENTES nessa competência? Divida as somas, multiplique por 100 e retorne nulo se o denominador for zero.',
49: 'Qual UF não nula e diferente da string vazia tem a maior soma de LEITOS_EXISTENTES? Considere todas as UFs presentes nessa competência, inclusive aquelas com soma zero.',
50: 'Qual é a soma de LEITOS_EXISTENTES por UF não nula e diferente da string vazia? Inclua todas as UFs presentes nessa competência, inclusive aquelas com soma zero.',
51: 'Qual é a soma de UTI_TOTAL_EXIST em todas as linhas dessa competência?',
52: 'Qual é o percentual da soma de UTI_TOTAL_EXIST sobre a soma de LEITOS_EXISTENTES nessa competência? Divida as somas, multiplique por 100 e retorne nulo se o denominador for zero.',
53: 'Qual categoria DS_TIPO_UNIDADE não nula e diferente da string vazia tem a maior soma de LEITOS_EXISTENTES? Preserve a categoria como armazenada.',
54: 'Quais são as somas de UTI_ADULTO_EXIST, UTI_PEDIATRICO_EXIST, UTI_NEONATAL_EXIST, UTI_CORONARIANA_EXIST e UTI_QUEIMADO_EXIST? Retorne uma única linha, nessa ordem; não some competências diferentes.',
55: 'Qual UF não nula e diferente da string vazia tem a menor soma de UTI_NEONATAL_EXIST? Inclua UFs presentes com soma zero, mas não acrescente UFs ausentes dessa competência.',
56: 'Qual código TP_GESTAO não nulo e diferente da string vazia reúne a maior quantidade de CNES distintos não nulos e diferentes da string vazia? Retorne o código de gestão, sem interpretá-lo como natureza jurídica pública, privada ou filantrópica.',
57: "Qual é a soma de LEITOS_SUS nas linhas em que NATUREZA_JURIDICA, após remover espaços nas extremidades, começa com '2' ou '3'? Esse é um filtro por código; não substitua por TP_GESTAO nem infira classificação jurídica além dos códigos especificados.",
58: 'Qual UF não nula e diferente da string vazia tem o maior percentual da soma de LEITOS_SUS sobre a soma de LEITOS_EXISTENTES? Considere somente UFs cuja soma de LEITOS_EXISTENTES seja positiva e multiplique a razão por 100.',
59: 'Para cada REGIAO não nula e diferente da string vazia, quais são as somas de LEITOS_EXISTENTES e LEITOS_SUS? Preserve os nomes das regiões e inclua todos os grupos presentes.',
60: 'Qual combinação de UF e código municipal CO_IBGE tem a maior soma de LEITOS_EXISTENTES? Exclua UF ou código municipal nulo ou igual à string vazia. Identifique o município pelo código acompanhado da UF.',
61: 'Considere todas as linhas de SRAG e o cadastro de UBS carregados, sem recorte temporal adicional e sem filtro de classificação final da SRAG. Quantos códigos municipais positivos distintos aparecem simultaneamente em co_mun_not da SRAG e em ibge de UBS com CNES positivo? Use a igualdade de códigos prevista no relacionamento cadastrado. Conte municípios, não notificações ou UBS; não use município de residência.',
62: 'Considere todas as linhas de SRAG, sem filtro de classificação final, e o cadastro de UBS carregados, sem recorte temporal adicional. Para cada código municipal positivo presente tanto em co_mun_not da SRAG quanto em ibge de UBS com CNES positivo, retorne a contagem de linhas de notificações e a contagem de CNES distintos positivos. Agregue cada base antes de combinar pela igualdade dos códigos. Liste todos os municípios comuns, sem top N; ordene por notificações decrescentes e código municipal crescente.',
63: 'Considere todos os registros de vacinação carregados, agrupados por UF de residência, e as linhas de leitos da maior competência COMP global disponível. Para cada sigla de UF não nula e diferente da string vazia presente nas duas bases, retorne a contagem de registros de vacinação e a soma de UTI_TOTAL_EXIST. Inclua somente UFs cuja soma de UTI seja positiva. Agregue as bases separadamente antes de combinar pela sigla de UF. É uma comparação descritiva entre o acumulado de registros e o estoque cadastrado mais recente, não cobertura vacinal, ocupação ou comparação de períodos equivalentes.',
64: 'Considere todos os registros de vacinação carregados, agrupados por UF de residência, e as linhas de leitos da maior competência COMP global disponível. Para cada sigla de UF não nula e diferente da string vazia presente nas duas bases, retorne a contagem de registros de vacinação e a soma de UTI_TOTAL_EXIST. Inclua somente UFs cuja soma de UTI seja positiva. Agregue as bases separadamente antes de combinar pela sigla de UF. É uma comparação descritiva entre o acumulado de registros e o estoque cadastrado mais recente, não cobertura vacinal, ocupação ou comparação de períodos equivalentes.',
65: 'Na base SRAG carregada, conte todas as linhas por UF de notificação sg_uf_not não nula e não vazia, em todo o período disponível e sem filtro de classificação final. Selecione somente as UFs com a contagem máxima global, incluindo todas as empatadas. Para cada uma, retorne a contagem de notificações e a soma de UTI_TOTAL_SUS na maior competência COMP global da base de leitos, identificando também essa competência. Agregue as bases separadamente e combine pela sigla de UF usando correspondência validada. Se uma UF selecionada não tiver registros de leitos nessa competência, mantenha a UF e indique ausência de informação, sem atribuir zero. A comparação é descritiva: acumulado de notificações versus estoque cadastrado recente, não vagas livres nem oferta na época das notificações.',
66: 'Na base SRAG carregada, conte as linhas com hospital = 1 por UF de notificação sg_uf_not não nula e não vazia, em todo o período disponível e sem filtro de classificação final. Selecione somente as UFs com a maior contagem, incluindo todos os empates; se não houver linhas elegíveis, retorne lista vazia. Essa contagem representa notificações com hospitalização indicada, não internações únicas. Para cada UF selecionada, retorne essa contagem, a soma de LEITOS_EXISTENTES na maior competência COMP global da base de leitos e a competência. Agregue antes de combinar por correspondência validada de sigla de UF; mantenha UFs sem dados de leitos com informação ausente, não zero. Compare acumulado de notificações com estoque cadastrado recente, sem inferir capacidade disponível na data da hospitalização.',
67: 'Considere o cadastro de UBS e todos os registros de vacinação contra COVID-19 carregados, sem recorte temporal adicional. Para cada UF comum às duas bases, conte CNES distintos positivos das UBS e registros de vacinação por UF de residência. Use correspondência validada entre o código de UF das UBS e a sigla de UF da vacinação; exclua UFs não identificáveis. Agregue antes de combinar. Retorne os dois totais e a razão registros de vacinação por UBS, com pelo menos seis casas decimais; considere somente UFs com pelo menos uma UBS. A razão é descritiva, não mede cobertura, produtividade ou doses aplicadas pelas próprias UBS e não solicita correlação estatística.',
68: 'Considere todas as linhas de SRAG carregadas, sem filtro de classificação final, o cadastro de UBS carregado e os leitos da maior competência COMP global disponível. Use município de notificação co_mun_not na SRAG e correspondência municipal validada com ibge das UBS e CO_IBGE dos leitos. Agregue separadamente: contagem de linhas de SRAG, CNES distintos positivos das UBS e soma de LEITOS_EXISTENTES. O universo de comparação contém somente municípios identificáveis presentes nas três bases, com pelo menos uma UBS e total de leitos conhecido. Inclua total de leitos zero quando registrado; exclua ausência de informação, sem convertê-la em zero. Defina alto número de notificações como contagem estritamente acima da mediana das contagens desse universo e baixa oferta de leitos como soma estritamente abaixo da mediana dos totais de leitos do mesmo universo. Calcule ambas as medianas antes da seleção; com número par de municípios, use a média dos dois valores centrais. Retorne todos os municípios que cumpram simultaneamente os dois cortes, com código municipal harmonizado, notificações, UBS, leitos e competência; se nenhum cumprir, retorne lista vazia. São contagens absolutas, não taxas populacionais; a comparação do acumulado com estoque recente não representa vagas livres nem equivalência temporal.',
}

EXTREMA = {2, 7, 8, 11, 12, 14, 18, 20, 21, 24, 27, 30, 33, 40, 42, 45, 49, 53, 55, 56, 58, 60}
DECISIONS = {
    65: 'Maior número definido como máximo global com todos os empates; acumulado de SRAG versus última COMP; UF sem estoque fica ausente, não zero.',
    66: 'Hospitalizações operacionalizadas como linhas com hospital=1; máximo com empates; estoque da última COMP, sem inferir leitos na data do evento.',
    67: 'Relação operacionalizada como totais lado a lado e razão registros/UBS; não como correlação ou produção atribuída às UBS.',
    68: 'Alto/baixo operacionalizados por cortes estritos acima/abaixo da mediana no universo comum às três bases; leitos totais existentes, sem denominador populacional.',
}
PROPOSED_COLUMNS = {
    65: ['uf', 'notificacoes', 'uti_sus', 'competencia'],
    66: ['uf', 'notificacoes_hospitalizadas', 'leitos_existentes', 'competencia'],
    67: ['uf', 'ubs', 'registros_vacinacao', 'registros_por_ubs'],
    68: ['municipio', 'notificacoes', 'ubs', 'leitos_existentes', 'competencia'],
}


def revise(source):
    if len(source['cases']) != 68 or {c['id'] for c in source['cases']} != set(BODIES):
        raise ValueError('Esperado catálogo completo, com IDs 1–68.')
    result = deepcopy(source)
    result.update(version=VERSION, status='draft', review_kind='ai_assisted',
                  parent_version=source['version'],
                  revision_notes='Revisão editorial das 68 perguntas. Escopo e critérios incorporados em cada enunciado. '
                  'SQLs e comparações de Q1–Q64 preservados. Q65–Q68 têm decisões operacionais explícitas e continuam testes de limitação. '
                  'Sem revisão humana independente ou execução de novas referências.',
                  global_specification='Cada pergunta contém seu escopo. Resultados descrevem somente os dados carregados; '
                  'não implicam cobertura nacional, representatividade populacional ou equivalência temporal entre bases. '
                  'As convenções de campos/códigos são operacionais e não substituem validação do dicionário da fonte.')
    seen = {}
    for case in result['cases']:
        identifier = case['id']
        case['previous_question'] = case['question']
        prefix = (SCOPES['vaccination'] if identifier <= 15 else SCOPES['ubs'] if identifier <= 30
                  else SCOPES['srag'] if identifier <= 45 else SCOPES['beds'] if identifier <= 60 else '')
        question = prefix + BODIES[identifier]
        if identifier in EXTREMA:
            question += ' Inclua todos os grupos empatados no extremo solicitado; se não houver grupos elegíveis, retorne lista vazia.'
        if identifier <= 64:
            question += ' Retorne somente estas colunas, nesta ordem: ' + ','.join(case['columns']) + '.'
            if not case['comparison'].get('ordered'):
                question += ' A ordem das linhas é livre.'
        else:
            question += ' Retorne somente estas colunas, nesta ordem: ' + ','.join(PROPOSED_COLUMNS[identifier]) + '. A ordem das linhas é livre.'
            case['proposed_output_columns'] = PROPOSED_COLUMNS[identifier][:]
        case.update(question=question, review_status='draft', question_revision={
            'kind': 'ai_assisted', 'scope': 'wording_and_explicit_operational_definitions',
            'human_review': 'pending',
            'semantic_change': identifier >= 65,
            'decision': DECISIONS.get(identifier, 'Definições alinhadas ao SQL candidato existente, sem alterar sua lógica.'),
        })
        case.pop('repeat_of', None)
        if question in seen:
            case['repeat_of'] = seen[question]
        else:
            seen[question] = identifier
        if identifier >= 65:
            case['specification'] = DECISIONS[identifier] + ' Integração ainda não implementada; não é referência numérica validada.'
    return result


def render(spec):
    lines = ['# 68 perguntas revisadas — versão 5', '',
             'Revisão assistida por IA. Substitui os enunciados para novos experimentos, sem reclassificar resultados anteriores.',
             'Cada pergunta contém as definições necessárias ao seu escopo operacional; não depende de contexto oculto.', '',
             'Q1–Q64: SQLs e comparações da versão 4 preservados; não foram executados ou revalidados nesta revisão.',
             'Q65–Q68: novas definições propostas para resolver ambiguidades; integração segue não implementada.',
             'Melhorar o enunciado não comprova disponibilidade, cobertura real dos dados ou suporte de implementação.', '',
             '## Decisões explícitas da revisão', '']
    lines += [f'- Q{i}: {decision}' for i, decision in DECISIONS.items()]
    lines += ['', 'Repetições herdadas são mantidas para preservar os 68 IDs: Q20/Q21, Q17/Q26, Q18/Q27 e Q63/Q64. '
              'Não devem ser tratadas como evidências independentes de diversidade.', '',
              'Os cortes por mediana em Q68 são uma proposta operacional do experimento, não limiares de adequação assistencial. '
              'O orientador pode escolher outros critérios; isso exigirá nova versão.', '']
    for case in spec['cases']:
        lines += [f"## Q{case['id']}", '', case['question'], '']
        if case['id'] >= 65:
            lines += ['**Situação:** pergunta definida operacionalmente, mas integração ainda sem suporte implementado.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / 'docs/avaliacao_acuracia/catalogo_68_v4.json')
    parser.add_argument('--output-prefix', type=Path, default=ROOT / 'docs/avaliacao_acuracia/catalogo_68_v5')
    args = parser.parse_args()
    targets = [Path(str(args.output_prefix) + suffix) for suffix in ('.json', '.md')]
    if any(p.exists() or p.resolve() == args.source.resolve() for p in targets):
        parser.error('Use um prefixo novo para preservar os catálogos existentes.')
    spec = revise(json.loads(args.source.read_text(encoding='utf-8-sig')))
    targets[0].parent.mkdir(parents=True, exist_ok=True)
    targets[0].write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    targets[1].write_text(render(spec) + '\n', encoding='utf-8')
    print('68 perguntas revisadas em ' + str(args.output_prefix))


if __name__ == '__main__':
    main()
