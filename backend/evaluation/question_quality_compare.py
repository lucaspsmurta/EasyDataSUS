"""Compare saved evaluator labels with an explicit assisted reference; no inference."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def indexed(cases):
    result = {}
    for case in cases:
        if case['id'] in result:
            raise ValueError('ID duplicado.')
        result[case['id']] = case
    return result


def compare(reference, report):
    for key in ('metadata', 'rubric'):
        if digest(report[key]) != reference[key + '_sha256']:
            raise ValueError(f'{key}: conteúdo diferente da referência; revise antes de comparar.')
    expected = indexed(reference['cases'])
    actual = indexed(report['cases'])
    rows = []
    valid = {'pass', 'partial', 'fail', 'not_applicable', 'not_assessable'}
    for identifier, case in expected.items():
        candidate = actual.get(identifier)
        if candidate is None or any(candidate.get(k, '') != case.get(k, '') for k in ('question', 'context')):
            raise ValueError(f'Q{identifier}: pergunta/contexto ausente ou diferente.')
        if set(case['dimensions']) != set(report['rubric']):
            raise ValueError('Referência deve conter todas as dimensões da rubrica.')
        for dimension, rating in case['dimensions'].items():
            observed = candidate['dimensions'][dimension]
            if rating['status'] not in valid or observed['status'] not in valid | {'pending'}:
                raise ValueError('Classificação inválida.')
            if observed.get('method') in {'human', 'ai_assisted'}:
                raise ValueError('Compare o relatório automático, sem sobreposição de revisão.')
            outcome = ('pending' if observed['status'] == 'pending' else
                       'agreement' if observed['status'] == rating['status'] else 'disagreement')
            rows.append({'id': identifier, 'dimension': dimension, 'reference': rating['status'],
                         'observed': observed['status'], 'outcome': outcome})
    counts = Counter(row['outcome'] for row in rows)
    evaluated = len(rows) - counts['pending']
    return {'reference_kind': reference['review_kind'], 'reference_status': reference['status'],
            'report_sha256': digest(report), 'reference_sha256': digest(reference),
            'total': len(rows), 'evaluated': evaluated, 'pending': counts['pending'],
            'agreements': counts['agreement'], 'disagreements': counts['disagreement'],
            'coverage': evaluated / len(rows) if rows else None,
            'agreement_among_evaluated': counts['agreement'] / evaluated if evaluated else None,
            'rows': rows}


def render(result):
    lines = ['# Comparação com referência assistida', '',
             'Referência provisória, assistida por IA; não constitui validação humana independente.',
             'Casos diagnósticos já conhecidos. Concordância de rótulos não mede correção das justificativas nem acurácia geral.', '',
             f"Cobertura: {result['evaluated']}/{result['total']}. Pendentes: {result['pending']}.",
             f"Concordâncias: {result['agreements']}/{result['evaluated']} classificações concluídas; "
             f"{result['agreements']}/{result['total']} células totais. Divergências: {result['disagreements']}.", '',
             '| Pergunta | Dimensão | Referência | Avaliador | Resultado |',
             '|---|---|---|---|---|']
    for row in result['rows']:
        lines.append(f"| Q{row['id']} | {row['dimension']} | {row['reference']} | {row['observed']} | {row['outcome']} |")
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--output-prefix', type=Path, required=True)
    args = parser.parse_args()
    outputs = [Path(str(args.output_prefix) + suffix) for suffix in ('.json', '.md')]
    if any(path.resolve() in {args.reference.resolve(), args.report.resolve()} for path in outputs):
        parser.error('A saída não pode sobrescrever as entradas.')
    result = compare(json.loads(args.reference.read_text(encoding='utf-8')),
                     json.loads(args.report.read_text(encoding='utf-8')))
    outputs[0].parent.mkdir(parents=True, exist_ok=True)
    outputs[0].write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    outputs[1].write_text(render(result), encoding='utf-8')
    print(render(result))


if __name__ == '__main__':
    main()
