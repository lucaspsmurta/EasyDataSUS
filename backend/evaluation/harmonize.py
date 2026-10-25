"""Apply an existing declared comparison protocol without running queries."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path

from .accuracy import compare_rows, digest, score, summarize, write_new


def read_bundle(path):
    bundle = json.loads(Path(path).read_text(encoding='utf-8'))
    content = {k: v for k, v in bundle.items() if k != 'integrity_sha256'}
    if digest(content) != bundle.get('integrity_sha256') or not bundle.get('ready'):
        raise ValueError('Invalid reference bundle')
    return bundle


def harmonize(source, protocol):
    if source['snapshot'] != protocol['snapshot']:
        raise ValueError('Reference data snapshots differ')
    cases = {c['id']: c for c in protocol['cases']}
    if set(cases) != {c['id'] for c in source['cases']}:
        raise ValueError('Case IDs differ')
    output = deepcopy(source)
    output.pop('integrity_sha256')
    for case in output['cases']:
        policy = cases[case['id']]
        for key in ('reference_sql', 'columns', 'expected_behavior', 'comparison'):
            if case.get(key) != policy.get(key):
                raise ValueError(f"Reference contract differs: {case['id']} / {key}")
        if case['expected_behavior'] == 'answer' and not compare_rows(
                case['expected_rows'], policy['expected_rows'], case['comparison']):
            raise ValueError(f"Reference values differ: {case['id']}")
        case.pop('result_alignment', None)
        if policy.get('result_alignment'):
            case['result_alignment'] = deepcopy(policy['result_alignment'])
    output['comparison_provenance'] = {
        'source_reference_sha256': source['integrity_sha256'],
        'protocol_reference_sha256': protocol['integrity_sha256'],
        'method': 'existing_declared_alignment_v1',
    }
    output['integrity_sha256'] = digest(output)
    return output


def rescore(run, source, unified):
    if run['reference_sha256'] != source['integrity_sha256']:
        raise ValueError('Run does not belong to source references')
    output = deepcopy(run)
    cases = {c['id']: c for c in unified['cases']}
    for result in output['results']:
        case = cases[result['id']]
        result['original_assessment'] = deepcopy(result['assessment'])
        result['assessment'] = score(case, result['response'])
        strict = deepcopy(case)
        strict.pop('result_alignment', None)
        result['strict_assessment'] = score(strict, result['response'])
    output['original_summary'] = deepcopy(run['summary'])
    output['summary'] = summarize(output['results'])
    strict_results = deepcopy(output['results'])
    for result in strict_results:
        result['assessment'] = result['strict_assessment']
    output['strict_summary'] = summarize(strict_results)
    output['reference_sha256'] = unified['integrity_sha256']
    output['rescoring'] = {
        'at': datetime.now(timezone.utc).isoformat(),
        'source_run_sha256': digest(run),
        'source_reference_sha256': source['integrity_sha256'],
        'queries_reexecuted': False,
        'protocol': unified['comparison_provenance'],
    }
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--references', required=True)
    parser.add_argument('--protocol', required=True)
    parser.add_argument('--run', required=True)
    parser.add_argument('--output-prefix', required=True)
    args = parser.parse_args()
    source, protocol = read_bundle(args.references), read_bundle(args.protocol)
    unified = harmonize(source, protocol)
    run = json.loads(Path(args.run).read_text(encoding='utf-8'))
    output = rescore(run, source, unified)
    paths = [args.output_prefix + '_references.json', args.output_prefix + '_results.json']
    if any(Path(p).exists() for p in paths):
        raise FileExistsError('Choose a new output prefix')
    write_new(paths[0], unified)
    write_new(paths[1], output)
    print(json.dumps({'summary': output['summary'], 'strict_summary': output['strict_summary']}))


if __name__ == '__main__':
    main()
