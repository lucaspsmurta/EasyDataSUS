"""Check explicit domain measures without consulting evaluation references."""
import re
from sqlglot import exp, parse_one
from services.analytical_contract import normalize


def domain_context(question, datasets):
    q=normalize(question)
    instructions=[]
    if 'atencao-basica' in datasets and 'municipio' in q:
        instructions.append('Município das UBS: IBGE. NOME identifica a unidade de saúde; não deve ser usado como nome de município nem dividir um total municipal.')
        instructions.append('Identifique o município pelo IBGE disponível; não acrescente NOME à projeção ou faça uma junção para recuperar o nome municipal, pois esse campo nomeia a UBS.')
    if 'leitos' in datasets:
        if 'uti' in q:
            instructions.append('Leitos de UTI cadastrados correspondem às medidas UTI_*_EXIST. Use UTI_*_SUS somente quando a pergunta restringir explicitamente aos leitos SUS; o fato de a fonte ser DataSUS não implica essa restrição.')
        if re.search(r'tipo (?:de|da) unidade',q):
            instructions.append('Dimensão solicitada: DS_TIPO_UNIDADE. Não substituir por TP_GESTAO ou NATUREZA_JURIDICA.')
        if re.search(r'quantos leitos|quantidade de leitos|total de leitos',q):
            instructions.append('Medida solicitada: somar capacidade. COUNT de linhas mede registros, não leitos. Usar a coluna de leitos correspondente ao tipo e ao vínculo SUS pedidos.')
    if 'surtos-srag' in datasets and re.search(r'estado|\buf\b',q):
        instructions.append("SG_UF_NOT contém siglas textuais. Não comparar com 0 nem converter a inteiro. Valores ausentes são tratados por IS NOT NULL e != '', quando a análise exige local identificado.")
    if 'surtos-srag' in datasets and re.search(r'cada um destes sintomas|cada sintoma',q):
        instructions.append('Sintomas são indicadores independentes: agregue cada indicador solicitado com countIf(campo=1). Não agrupe pelos valores dos indicadores nem filtre a base por um único sintoma. Na apresentação em linhas, use rótulo literal por sintoma e UNION ALL; na apresentação em colunas, use uma agregação por indicador.')
    return 'Vinculação da intenção ao domínio:\n'+'\n'.join(instructions) if instructions else ''


def domain_errors(sql, question, datasets):
    tree=parse_one(sql,read='clickhouse')
    q=normalize(question)
    used={c.name.lower() for c in tree.find_all(exp.Column)}
    errors=[]
    if datasets == ['atencao-basica'] and re.search(r'(?:por|cada) municipio',q) and not re.search(r'\bnome\b|por unidade|cada unidade',q):
        for group in tree.find_all(exp.Group):
            if any(c.name.lower()=='nome' for c in group.find_all(exp.Column)):
                errors.append('NOME identifica a UBS, não o município. Para totais por município, agrupe pelo código IBGE; não subdivida pelo nome da unidade.')
                break
    if 'leitos' in datasets:
        if re.search(r'tipo (?:de|da) unidade',q) and 'ds_tipo_unidade' not in used:
            errors.append('Tipo de unidade corresponde a DS_TIPO_UNIDADE; TP_GESTAO representa gestão, não tipo de unidade.')
        if re.search(r'quantos leitos|quantidade de leitos|total de leitos',q) and not any(
                c.name.lower().startswith(('leitos_', 'uti_')) for agg in tree.find_all(exp.Sum)
                for c in agg.find_all(exp.Column)):
            errors.append('Quantidade de leitos exige SUM da medida de capacidade solicitada, não COUNT de registros ou estabelecimentos.')
    if 'atencao-basica' in datasets and re.search(r'ubs (?:diferentes|distintas)|cada (?:ubs|unidade) uma vez',q):
        for count in tree.find_all(exp.Count, exp.Anonymous):
            if isinstance(count,exp.Anonymous) and count.name.lower() not in ('uniqexact','countdistinct'):
                continue
            if any(c.name.lower()=='nome' for c in count.find_all(exp.Column)):
                errors.append('UBS distintas devem ser contadas pelo CNES; nomes de unidades podem se repetir.')
                break
    if 'leitos' in datasets and 'uti' in q and re.search(r'cada modalidade|modalidades de uti',q):
        modalities={'adult':'UTI_ADULTO','pediatric':'UTI_PEDIATRICO','neonatal':'UTI_NEONATAL',
                    'coronarian':'UTI_CORONARIANA','queimad':'UTI_QUEIMADO'}
        suffix='_SUS' if re.search(r'uti (?:destinad\w+ ao |do )?sus',q) else '_EXIST'
        for term,column in modalities.items():
            if term in q and (column+suffix).lower() not in used:
                errors.append('Modalidade de UTI solicitada exige soma de '+column+suffix+'; não filtre DS_TIPO_UNIDADE por nomes de UTI.')
    if 'surtos-srag' in datasets and re.search(r'cada um destes sintomas|cada sintoma',q):
        symptoms={'febre','tosse','garganta','dispneia','diarreia','vomito'}
        for group in tree.find_all(exp.Group):
            if any(c.name.lower() in symptoms for c in group.find_all(exp.Column)):
                errors.append('Conte cada sintoma separadamente com countIf(indicador=1); GROUP BY dos indicadores produz combinações, não os totais por sintoma.')
                break
    return errors
