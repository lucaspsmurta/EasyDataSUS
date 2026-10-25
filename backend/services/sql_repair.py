"""Bounded repair instructions based on validation errors, never reference answers."""
import os


def generation_attempts():
    return max(1, min(4, int(os.getenv('SQL_GENERATION_MAX_ATTEMPTS', '3'))))


def repair_prompt(prompt, history):
    errors = '\n'.join(e for attempt in history for e in attempt['errors'])
    hints=[]
    if 'NOME' in errors and ('IBGE' in prompt or 'ibge' in prompt) and 'UBS' in prompt:
        hints.append('NOME identifica a UBS, não o município. Para totais municipais, remova NOME da projeção e do agrupamento; identifique o município pelo IBGE. Não junte a tabela novamente para obter NOME.')
    if 'cada sintoma' in errors:
        hints.append('Cada indicador solicitado precisa de sua própria contagem condicional com valor 1. Não projete o indicador bruto junto das agregações; se apresentar linhas, projete um rótulo literal em cada ramo UNION ALL.')
    if 'NO_COMMON_TYPE' in errors or 'é textual' in errors:
        hints.append('Há comparação ou junção entre tipos incompatíveis. Siglas de UF são texto: '
                     'para excluir ausência use IS NOT NULL e != string vazia, não > 0. '
                     'Códigos numéricos de UF exigem correspondência documentada antes de juntar com siglas; '
                     'converter ambos para texto não estabelece essa correspondência.')
    if any(term in errors.lower() for term in ('aggregate', 'agrega', 'countif')):
        hints.append('countIf(condição) já é uma agregação: não envolva em SUM. Para MAX de totais, '
                     'calcule os totais em uma CTE e MAX em outro nível. Use aliases distintos dos campos físicos.')
    if 'JOIN' in errors or 'join' in errors:
        hints.append('Projete a chave em cada CTE participante e dê aliases diferentes às fontes. '
                     'Se numerador e denominador vêm da mesma base, prefira agregações condicionais '
                     'em uma única CTE por grupo, evitando autojunções desnecessárias.')
    if 'Coluna não autorizada' in errors or 'UNKNOWN_IDENTIFIER' in errors:
        hints.append('Use apenas campos do esquema apresentado. Um nome conceitual não cria uma coluna física. '
                     'Valores de CTE escalar fora do FROM exigem (SELECT alias FROM cte).')
    if 'Modalidade de UTI' in errors:
        hints.append('Cada modalidade solicitada é uma medida própria: some diretamente a coluna indicada '
                     'na mensagem de validação. Não filtre tipo de estabelecimento para selecionar essas medidas.')
    if 'razão' in errors:
        hints.append('Calcule as contagens condicionais no mesmo universo e divida na ordem pedida, '
                     'sem GROUP BY da categoria que separaria numerador e denominador. Razão não é percentual.')
    tail=[]
    for i,attempt in enumerate(history,1):
        tail.append(f"Tentativa {i}:\n{attempt['sql']}\nErros: " + '; '.join(attempt['errors']))
    return (prompt + '\nReescreva a consulta completa preservando todos os requisitos da pergunta. '
            'Não repita as estruturas rejeitadas. Não remova uma medida ou filtro para eliminar o erro.\n'
            + '\n'.join(tail) + '\nOrientações de correção:\n' + '\n'.join(hints)
            + '\nRetorne somente SQL completo.')
