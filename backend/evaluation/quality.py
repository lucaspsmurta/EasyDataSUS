"""Avaliação dimensional de execuções salvas, sem consultas ao banco ou à LLM."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from .accuracy import digest


DIMENSIONS = {
    'dataset_selection': ('Seleção de bases', 'Conjunto selecionado igual ao esperado.', 'automatic'),
    'relationship_selection': ('Seleção de relações', 'Conjunto igual ao esperado nos casos com relação prevista.', 'automatic'),
    'sql_accepted': ('SQL aprovado', 'SQL presente e aprovado pelo validador registrado.', 'automatic'),
    'operational_success': ('Sucesso operacional', 'Resposta com success=true.', 'automatic'),
    'result_equivalence': ('Equivalência estrita', 'Classificação original contra referência, incluindo contrato de saída.', 'automatic'),
    'row_count': ('Quantidade de linhas', 'Mesma quantidade; não comprova completude semântica.', 'automatic'),
    'column_count': ('Quantidade de colunas', 'Mesma quantidade; não comprova identidade ou ordem das colunas.', 'automatic'),
    'controlled_limitation': ('Limitação prevista', 'Classificação original da limitação controlada.', 'automatic'),
    'filters': ('Filtros', 'Período, localização, categorias e restrições correspondem ao pedido.', 'review'),
    'aggregation': ('Unidade e agregação', 'Entidade contada, DISTINCT, grupos, denominadores e junções adequados.', 'review'),
    'identification': ('Dimensões e identificadores', 'Campos, códigos, nomes e unidades solicitados são usados corretamente.', 'review'),
    'main_information': ('Informação principal', 'Conteúdo principal solicitado está correto, independentemente de informação extra.', 'review'),
    'completeness': ('Completude e escopo', 'Todos os elementos solicitados estão presentes, sem seleção indevida de grupos.', 'review'),
    'output_contract': ('Formato da saída', 'Colunas, identificadores, ordem e informação adicional respeitam o pedido.', 'review'),
    'text_fidelity': ('Fidelidade do texto', 'Texto corresponde à tabela e seus limites, sem extrapolações; não valida o SQL.', 'review'),
}
STATUSES = ('pass', 'partial', 'fail', 'pending', 'not_assessable', 'not_applicable')


def item(status, evidence, method='automatic'):
    return dict(status=status, evidence=evidence, method=method)


def assess(case, result):
    response = result.get('response') or {}
    assessment = result['assessment']
    answer = case['expected_behavior'] == 'answer'
    limitation = case['expected_behavior'] == 'limitation'
    available = response.get('success') is True and isinstance(response.get('data'), list)
    values = {}
    for key, expected in [('datasets', 'expected_datasets'), ('relationships', 'expected_relationships')]:
        dimension = 'dataset_selection' if key == 'datasets' else 'relationship_selection'
        if not case.get(expected):
            values[dimension] = item('not_applicable', 'Sem conjunto positivo esperado para esta dimensão.')
        elif key not in response:
            values[dimension] = item('not_assessable', 'Seleção ausente do registro.')
        else:
            actual = set(response.get(key) or [])
            target = set(case[expected])
            values[dimension] = item('pass' if actual == target else 'fail',
                                    dict(expected=sorted(target), actual=sorted(actual),
                                         tp=len(actual & target), fp=len(actual-target), fn=len(target-actual)))
    for name in ('sql_accepted', 'operational_success', 'result_equivalence', 'row_count', 'column_count'):
        if not answer:
            values[name] = item('not_applicable', 'Caso sem referência analítica.')
    if answer:
        sql_ok = bool(response.get('sql')) and (response.get('validation') or {}).get('valid') is True
        values['sql_accepted'] = item('pass' if sql_ok else 'fail', 'SQL final e validation.valid registrados.')
        values['operational_success'] = item('pass' if response.get('success') is True else 'fail', 'response.success')
        correct = assessment.get('result_correct')
        values['result_equivalence'] = item('pass' if correct is True else 'fail' if correct is False else 'pending', assessment)
        if not available:
            for name in ('row_count', 'column_count'):
                values[name] = item('not_assessable', 'Não há tabela final executada com sucesso.')
        else:
            rows = response['data']
            values['row_count'] = item('pass' if len(rows) == len(case['expected_rows']) else 'fail',
                                       dict(expected=len(case['expected_rows']), actual=len(rows)))
            widths = [len(row) for row in rows if isinstance(row, (list, tuple))]
            if len(widths) != len(rows):
                values['column_count'] = item('fail', 'Estrutura de linha inválida.')
            elif rows or response.get('columns'):
                if not rows:
                    widths = [len(response['columns'])]
                values['column_count'] = item('pass' if all(w == len(case['columns']) for w in widths) else 'fail',
                                              dict(expected=len(case['columns']), actual_widths=sorted(set(widths))))
            else:
                values['column_count'] = item('not_assessable', 'Tabela vazia sem metadados de colunas.')
    values['controlled_limitation'] = item(
        ('pass' if assessment.get('limitation_correct') is True else 'fail') if limitation else 'not_applicable',
        assessment if limitation else 'Não é uma limitação prevista.')
    for name, (_, _, mode) in DIMENSIONS.items():
        if mode != 'review':
            continue
        if not answer:
            status, reason = 'not_applicable', 'Rubrica qualitativa restrita às respostas analíticas.'
        elif not available:
            status, reason = 'not_assessable', 'Não há resposta analítica final; falha contabilizada nas dimensões operacionais.'
        elif name == 'text_fidelity' and not (response.get('insight') or response.get('factual_summary')):
            status, reason = 'not_assessable', 'Sem texto explicativo registrado.'
        else:
            status, reason = 'pending', 'Exige inspeção da pergunta, referência e resposta; não inferido da equivalência.'
        values[name] = item(status, reason, 'review')
    return dict(id=case['id'], question=case['question'], expected_behavior=case['expected_behavior'],
                original_status=assessment['status'], dimensions=values,
                diagnostics=[d for d in response.get('generation_diagnostics', [])
                             if d.get('stage') == 'sql_validation' and d.get('errors')])


def summarize(cases):
    summary = {}
    for dimension in DIMENSIONS:
        ratings = [c['dimensions'][dimension] for c in cases]
        counts = Counter(v['status'] for v in ratings)
        applicable = len(cases)-counts['not_applicable']
        evaluated = sum(counts[k] for k in ('pass', 'partial', 'fail'))
        summary[dimension] = dict(
            counts={k: counts[k] for k in STATUSES}, applicable=applicable, evaluated=evaluated,
            coverage=evaluated/applicable if applicable else None,
            pass_rate_evaluated=counts['pass']/evaluated if evaluated else None,
            partial_rate_evaluated=counts['partial']/evaluated if evaluated else None,
            fail_rate_evaluated=counts['fail']/evaluated if evaluated else None,
            methods=dict(Counter(v['method'] for v in ratings if v['status'] in ('pass', 'partial', 'fail'))))
    return summary


def apply_review(cases, review, results_hash, reference_hash):
    if review.get('results_sha256') != results_hash or review.get('reference_sha256') != reference_hash:
        raise ValueError('A revisão pertence a outro resultado ou referência.')
    by_id = {c['id']: c for c in cases}
    seen = set()
    for entry in review.get('ratings', []):
        key = (entry['id'], entry['dimension'])
        if key in seen or entry['id'] not in by_id or entry['dimension'] not in DIMENSIONS:
            raise ValueError(f'Entrada inválida/duplicada: {key}')
        seen.add(key)
        name = entry['dimension']
        if DIMENSIONS[name][2] != 'review':
            raise ValueError('Revisão não pode sobrescrever dimensão automática.')
        if entry.get('status') == 'pending':
            continue
        target = by_id[entry['id']]['dimensions'][name]
        if target['status'] != 'pending':
            raise ValueError(f'Dimensão sem resposta elegível: {key}')
        if entry.get('status') not in ('pass', 'partial', 'fail', 'not_applicable'):
            raise ValueError(f'Status de revisão inválido: {key}')
        if not all(isinstance(entry.get(k), str) and entry[k].strip()
                   for k in ('evidence', 'reviewer', 'reviewed_at')):
            raise ValueError(f'Revisão exige evidência, responsável e data: {key}')
        if entry.get('review_kind') not in ('human', 'ai_assisted'):
            raise ValueError('review_kind deve ser human ou ai_assisted.')
        datetime.fromisoformat(entry['reviewed_at'])
        by_id[entry['id']]['dimensions'][name] = dict(
            status=entry['status'], evidence=entry['evidence'], method=entry['review_kind'],
            reviewer=entry['reviewer'], reviewed_at=entry['reviewed_at'])


def build(results, bundle, results_hash, review=None):
    reference_hash = bundle.get('integrity_sha256')
    payload = {k: v for k, v in bundle.items() if k != 'integrity_sha256'}
    if not reference_hash or digest(payload) != reference_hash or not bundle.get('ready'):
        raise ValueError('Pacote de referência inválido.')
    if results.get('reference_sha256') != reference_hash:
        raise ValueError('Execução e referência não correspondem.')
    if not results.get('summary') or results.get('snapshot_unchanged') is not True:
        raise ValueError('Use uma execução finalizada com dados inalterados.')
    refs = {c['id']: c for c in bundle['cases']}
    seen, cases = set(), []
    for result in results['results']:
        i = result['id']
        if i in seen or i not in refs:
            raise ValueError('IDs duplicados ou sem referência.')
        seen.add(i)
        if result['question'] != refs[i]['question'] or result['expected_behavior'] != refs[i]['expected_behavior']:
            raise ValueError('Enunciado/comportamento diferente da referência.')
        cases.append(assess(refs[i], result))
    if not cases:
        raise ValueError('Execução sem casos.')
    cases.sort(key=lambda c: c['id'])
    if review is not None:
        apply_review(cases, review, results_hash, reference_hash)
    return dict(version='response-quality-v1', created_at=datetime.now(timezone.utc).isoformat(),
                results_sha256=results_hash, reference_sha256=reference_hash,
                reference_reviewed=results.get('reference_reviewed', False),
                source_valid_for_claims=results.get('valid_for_claims', False),
                original_summary=results['summary'], dimensions=DIMENSIONS,
                summary=summarize(cases), cases=cases)


def markdown(report):
    def percent(value):
        return '—' if value is None else f'{100*value:.2f}%'
    lines = ['# Qualidade das respostas por dimensão\n',
             'Análise dos registros existentes, sem nova execução. A acurácia original não foi alterada.\n',
             f'Referências revisadas: {report["reference_reviewed"]}. Validade declarada na execução de origem: {report["source_valid_for_claims"]}.\n',
             '## Critérios e denominadores\n',
             'As dimensões podem se sobrepor. Não some seus percentuais nem use 100% menos uma categoria como qualidade global. '
             'Aprovação é calculada sobre avaliados (pass/partial/fail); cobertura é avaliados/aplicáveis. '
             'Pendências e casos sem resposta não são aprovações. Falhas técnicas reprovam a equivalência e o sucesso operacional, '
             'mas ficam sem avaliação de conteúdo final. Quantidades iguais de linhas/colunas não garantem valores ou significado corretos.\n',
             '| Dimensão | Aplicáveis | Avaliados | Aprovados | Parciais | Reprovados | Pendentes | Sem avaliação possível | Aprovação/avaliados | Cobertura |',
             '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for name, (label, criterion, mode) in DIMENSIONS.items():
        s = report['summary'][name]
        c = s['counts']
        lines.append(f'| {label} | {s["applicable"]} | {s["evaluated"]} | {c["pass"]} | {c["partial"]} | {c["fail"]} | {c["pending"]} | {c["not_assessable"]} | {percent(s["pass_rate_evaluated"])} | {percent(s["coverage"])} |')
    lines.append('\nSeleção nesta tabela significa igualdade de conjuntos por pergunta, não recall. Precisão/recall/F1 originais permanecem no JSON em original_summary.\n')
    for name, (label, criterion, mode) in DIMENSIONS.items():
        lines.append(f'- **{label}** (`{name}`, {mode}): {criterion}')
    lines.append('\n## Casos\n')
    for case in report['cases']:
        lines += [f'\n### Q{case["id"]} — {case["original_status"]}\n', case['question'],
                  '\n| Dimensão | Classificação | Método | Evidência |', '|---|---|---|---|']
        for name, rating in case['dimensions'].items():
            evidence = rating['evidence'] if isinstance(rating['evidence'], str) else json.dumps(rating['evidence'], ensure_ascii=False)
            evidence = evidence.replace('|', '\\|').replace('\n', ' ')
            lines.append(f'| {DIMENSIONS[name][0]} | {rating["status"]} | {rating["method"]} | {evidence} |')
    return '\n'.join(lines)+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', required=True)
    parser.add_argument('--references', required=True)
    parser.add_argument('--output-prefix', required=True)
    parser.add_argument('--review', help='Ficha preenchida de revisão qualitativa')
    args = parser.parse_args()
    paths = [Path(args.output_prefix+suffix) for suffix in ('.json', '.md', '.review.json')]
    for path in paths:
        if path.exists():
            raise FileExistsError(path)
    raw = Path(args.results).read_bytes()
    results = json.loads(raw)
    bundle = json.loads(Path(args.references).read_text(encoding='utf-8'))
    review = json.loads(Path(args.review).read_text(encoding='utf-8')) if args.review else None
    report = build(results, bundle, hashlib.sha256(raw).hexdigest(), review)
    report['source_results'] = str(Path(args.results).resolve())
    report['source_references'] = str(Path(args.references).resolve())
    template = dict(results_sha256=report['results_sha256'], reference_sha256=report['reference_sha256'], ratings=[])
    for case in report['cases']:
        for name, rating in case['dimensions'].items():
            if rating['status'] == 'pending' and DIMENSIONS[name][2] == 'review':
                template['ratings'].append(dict(id=case['id'], dimension=name, status='pending',
                    evidence='', reviewer='', reviewed_at='', review_kind=''))
    for path, data in zip(paths, (json.dumps(report, ensure_ascii=False, indent=2), markdown(report),
                                  json.dumps(template, ensure_ascii=False, indent=2))):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('x', encoding='utf-8') as handle:
            handle.write(data)
        print(path)


if __name__ == '__main__':
    main()
