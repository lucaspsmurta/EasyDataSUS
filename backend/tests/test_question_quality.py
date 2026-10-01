import unittest
import json
from copy import deepcopy
from unittest.mock import patch, Mock

from backend.evaluation.question_quality import (
    DIMENSIONS, OBSERVATIONS, GROUPS, inputs, evaluate, validate_rating, summarize, apply_review,
    evidence_sources, main, metadata, ROOT, validate_support, output_schema, validate_facts, validate_consistency, integration_check,
    data_requirements, validate_decision, support_choices,
)
from pathlib import Path
from tempfile import TemporaryDirectory


class QuestionQualityTests(unittest.TestCase):
    def test_decision_checks_prevent_contradictory_approval(self):
        for name, check in [('context_completeness', 'necessary_scope_missing'),
                            ('analytical_specificity', 'incomplete'), ('unambiguity', 'unresolved')]:
            rating = {'status': 'pass', 'decision_check': check,
                      'decision_detail': 'O corte de seleção altera quais entidades são retornadas.'}
            with self.assertRaises(ValueError):
                validate_decision(rating, name, [], {})
            rating['status'] = 'partial'
            validate_decision(rating, name, [], {})

    def test_support_choices_handle_single_and_disconnected_datasets(self):
        single = [{'fields': ['field:orders:amount']}]
        multiple = single + [{'fields': ['field:customers:id']}]
        self.assertIn(('pass', 'none'), support_choices('implementation_support', single, {}))
        self.assertNotIn(('partial', 'missing_relationship'),
                         support_choices('implementation_support', single, {}))
        self.assertNotIn(('pass', 'none'), support_choices('implementation_support', multiple, {}))
        self.assertIn(('partial', 'missing_relationship'),
                      support_choices('implementation_support', multiple, {}))
        self.assertIn(('pass', 'none'), support_choices('data_availability', multiple, {}))
        self.assertNotIn(('fail', 'missing_relationship'),
                         support_choices('implementation_support', multiple, {}))
        self.assertNotIn(('pass', 'none'), support_choices('data_availability', [{'fields': []}], {}))

    def test_question_alone_cannot_demonstrate_metadata_incompatibility(self):
        case = {'question': 'Quantos pedidos?', 'context': ''}
        mapping = [{'requirement': 'pedidos', 'fields': ['field:orders:id'], 'reason': 'Contagem'}]
        rating = {'status': 'fail', 'limitation': 'incompatible_metadata',
                  'evidence': [{'source': 'question', 'quote': 'pedidos'}]}
        with self.assertRaisesRegex(ValueError, 'campo mapeado'):
            validate_support(mapping, rating, 'data_availability', case,
                             {'question': case['question'], 'field:orders:id': 'Identificador'}, {})

    def setUp(self):
        self.case = {'id': 1, 'question': 'Quantos registros no conjunto carregado?', 'context': ''}
        self.ratings = {k: {'status': 'pass', 'justification': 'Escopo definido.',
                           'evidence': [{'source': 'question', 'quote': 'no conjunto carregado'}], 'suggestion': ''} for k in DIMENSIONS}
        for name in GROUPS['support']:
            self.ratings[name] = {'status': 'not_assessable', 'justification': 'Campos não fornecidos.',
                                  'evidence': [], 'suggestion': ''}

    def test_catalog_allowlist_excludes_answers_and_private_specification(self):
        source = {**self.case, 'reference_sql': 'SECRET', 'expected_rows': [[123]],
                  'specification': 'SECRET', 'expected_datasets': ['SECRET']}
        result = inputs({'global_specification': 'SECRET', 'cases': [source]}, 'question', '')
        self.assertEqual([self.case], result)

    def test_metadata_normalizes_both_formats_without_sql(self):
        meta = metadata(ROOT / 'backend/metadata')
        datasets = {d['nome_curto']: d for d in meta['datasets']}
        vaccine = datasets['covid-19-vacinacao']
        self.assertEqual('vacinacao', vaccine['tabela_clickhouse'])
        self.assertIn('fabricante', vaccine['columns']['vacina_fabricante_nome']['description'])
        self.assertIn('UTI_TOTAL_SUS', datasets['leitos']['columns'])
        self.assertIn('NU_NOTIFIC', datasets['surtos-srag']['columns'])
        self.assertNotIn('SELECT ', json.dumps(meta))
        sources = evidence_sources(self.case, meta, 'support')
        self.assertNotIn('context', sources)
        self.assertIn('field:leitos:UTI_TOTAL_SUS', sources)
        self.assertNotIn('columns', json.loads(sources['dataset:leitos']))

    def test_support_requires_fields_and_relevant_relationships(self):
        meta = metadata(ROOT / 'backend/metadata')
        case = {**self.case, 'question': 'fabricante e leitos'}
        sources = evidence_sources(case, meta, 'support')
        vaccine = 'field:covid-19-vacinacao:vacina_fabricante_nome'
        beds = 'field:leitos:UTI_TOTAL_SUS'
        mapping = [{'requirement': 'fabricante', 'fields': [vaccine], 'reason': 'Identifica fabricante.'}]
        rating = {'status': 'pass', 'evidence': [{'source': 'dataset:atencao-basica', 'quote': 'Dados'}]}
        with self.assertRaisesRegex(ValueError, 'campo field:'):
            validate_support(mapping, rating, 'data_availability', case, sources, meta)
        rating['evidence'] = [{'source': vaccine, 'quote': 'fabricante'}]
        validate_support(mapping, rating, 'implementation_support', case, sources, meta)
        mapping.append({'requirement': 'leitos', 'fields': [beds], 'reason': 'Leitos SUS.'})
        with self.assertRaisesRegex(ValueError, 'todas as bases'):
            validate_support(mapping, rating, 'implementation_support', case, sources, meta)
        rating['evidence'].append({'source': 'relationship:srag_ubs_municipio_notificacao', 'quote': 'SRAG'})
        with self.assertRaisesRegex(ValueError, 'não conecta'):
            validate_support(mapping, rating, 'implementation_support', case, sources, meta)
        rating['evidence'][-1]['source'] = 'relationship:vacinacao_leitos_uf'
        validate_support(mapping, rating, 'implementation_support', case, sources, meta)
        mapping[-1]['fields'] = []
        rating['evidence'].pop()
        with self.assertRaisesRegex(ValueError, 'faltam campos'):
            validate_support(mapping, rating, 'data_availability', case, sources, meta)

    def test_literal_extraction_and_contradictions(self):
        facts = {k: '' for k in OBSERVATIONS['formulation']}
        facts['measure'] = 'registros'
        validate_facts({'facts': facts}, self.case)
        invalid = {**facts, 'time_scope': 'último ano'}
        with self.assertRaisesRegex(ValueError, 'time_scope'):
            validate_facts({'facts': invalid}, self.case)
        rating = {**self.ratings['analytical_specificity'], 'status': 'fail',
                  'issue': 'Medida ausente.', 'alternative': '', 'missing_elements': ['measure']}
        with self.assertRaisesRegex(ValueError, 'explícitos'):
            validate_consistency(rating, 'analytical_specificity', facts, [], {})
        rating.update(missing_elements=[], issue='Critério relativo.', alternative='')
        with self.assertRaisesRegex(ValueError, 'outra interpretação'):
            validate_consistency(rating, 'unambiguity', facts, [], {})

    def test_extraction_and_mapping_schemas_only_offer_real_spans(self):
        sources = {'question': 'Qual fabricante? Inclua todos os empatados.'}
        schema = output_schema('extract', (), sources)
        values = schema['properties']['facts']['properties']['population']['enum']
        self.assertTrue(all(v in sources['question'] for v in values))
        self.assertNotIn('fabricantes', values)
        schema = output_schema('map', (), sources)
        values = schema['properties']['support_map']['items']['properties']['requirement']['enum']
        self.assertTrue(all(v and v in sources['question'] for v in values))
        self.assertNotIn('inclua todos os empatados', values)

    def test_data_requirements_exclude_presentation_and_evidence_is_literal(self):
        facts = {'measure': 'registros', 'population': 'fabricante', 'grouping': 'fabricante',
                 'ties': 'Inclua todos os empatados.'}
        self.assertEqual([self.case['question']], data_requirements(facts, self.case))
        incomplete = {'measure': 'notificações'}
        case = {'question': 'Quais municípios combinam notificações e baixa disponibilidade de leitos?', 'context': ''}
        self.assertIn(case['question'], data_requirements(incomplete, case))
        sources = {'question': self.case['question'], 'field:a:x': 'Descrição do campo. ' * 20}
        schema = output_schema('support', ('data_availability',), sources)
        choices = schema['properties']['dimensions']['properties']['data_availability']['properties']['evidence']['items']['anyOf']
        for choice in choices:
            source = choice['properties']['source']['enum'][0]
            self.assertTrue(all(q in sources[source] and len(q) <= 180
                                for q in choice['properties']['quote']['enum']))

    def test_nonpass_support_contradictions_are_rejected(self):
        mapping = [{'requirement': 'registros', 'fields': ['field:a:ID'], 'reason': 'Contagem.'}]
        rating = {'status': 'not_assessable', 'limitation': 'missing_fields', 'evidence': []}
        with self.assertRaisesRegex(ValueError, 'contradiz'):
            validate_consistency(rating, 'data_availability', {}, mapping, {})
        rating['limitation'] = 'missing_relationship'
        with self.assertRaisesRegex(ValueError, 'relacionamento'):
            validate_consistency(rating, 'data_availability', {}, mapping, {})
        rating['limitation'] = 'insufficient_metadata'
        with self.assertRaisesRegex(ValueError, 'Cite'):
            validate_consistency(rating, 'data_availability', {}, mapping, {})

    @patch('backend.evaluation.question_quality.requests.post')
    def test_stages_resume_cache_and_partial_preservation(self, post):
        self.case['dimensions'] = {k: {'status': 'pending'} for k in DIMENSIONS}
        meta = {'datasets': [{'nome_curto': 'a', 'columns': {'ID': {'type': 'INT', 'description': 'Registro'}}},
                             {'nome_curto': 'unrelated', 'columns': {'SECRET': {}}}]}
        facts = {k: '' for k in OBSERVATIONS['formulation']}
        facts['measure'] = 'registros'
        calls = []
        def reply(url, json, timeout):
            calls.append(json)
            properties = json['format']['properties']
            if 'facts' in properties:
                body = {'facts': facts}
            elif 'support_map' in properties:
                payload = __import__('json').loads(json['prompt'])
                body = {'support_map': [{'requirement': requirement, 'fields': ['field:a:ID'], 'reason': 'Contagem.'}
                                        for requirement in payload['requirements']]}
            else:
                ratings = {}
                for name in properties['dimensions']['properties']:
                    if name in GROUPS['formulation']:
                        rating = {**self.ratings[name], 'issue': '', 'alternative': '', 'missing_elements': []}
                        rating.update(decision_check={'context_completeness': 'sufficient',
                            'analytical_specificity': 'complete', 'unambiguity': 'resolved'}[name],
                            decision_detail='Contar todos os registros do conjunto explicitamente indicado.')
                    else:
                        rating = {'status': 'pass', 'justification': 'Campo de registros presente.', 'suggestion': '',
                                  'evidence': [{'source': 'field:a:ID', 'quote': 'Registro'}], 'limitation': 'none'}
                    if len(calls) == 2 and name == 'unambiguity':
                        rating['evidence'] = [{'source': 'question', 'quote': 'inventado'}]
                    ratings[name] = rating
                body = {'dimensions': ratings}
            return Mock(json=lambda: {'response': __import__('json').dumps(body), 'done_reason': 'stop', 'eval_count': 10})
        post.side_effect = reply
        evaluate(self.case, meta, 'm', 'http://local', 1)
        self.assertEqual(5, len(calls))
        self.assertNotIn('SECRET', calls[0]['prompt'])
        self.assertNotIn('SECRET', calls[1]['prompt'])
        self.assertIn('SECRET', calls[3]['prompt'])
        self.assertNotIn('SECRET', calls[4]['prompt'])
        self.assertEqual(['unambiguity'], list(calls[2]['format']['properties']['dimensions']['properties']))
        self.assertFalse(self.case['errors'])
        self.assertEqual(10, self.case['attempts'][0]['metrics']['eval_count'])
        self.case['dimensions']['unambiguity'] = {'status': 'pending'}
        evaluate(self.case, meta, 'm', 'http://local', 1)
        self.assertEqual(6, len(calls))  # Reuses extraction; does not repeat support.

    @patch('backend.evaluation.question_quality.requests.post')
    def test_truncated_preparation_never_becomes_a_rating(self, post):
        post.return_value = Mock(json=lambda: {'done_reason': 'length', 'response': '{}'})
        self.case['dimensions'] = {k: {'status': 'pending'} for k in DIMENSIONS}
        evaluate(self.case, {}, 'm', 'http://local', 1)
        self.assertEqual(4, post.call_count)
        self.assertFalse(self.case['preparation'])
        self.assertTrue(all(r['status'] == 'pending' for r in self.case['dimensions'].values()))

    def test_response_lengths_are_checked(self):
        rating = deepcopy(self.ratings['unambiguity'])
        rating['justification'] = 'x' * 241
        with self.assertRaisesRegex(ValueError, '240'):
            validate_rating({'dimensions': {'unambiguity': rating}}, self.case, ('unambiguity',))

    def test_prepare_resume_and_changed_protocol_protection(self):
        with TemporaryDirectory() as directory:
            prefix = str(Path(directory) / 'compact')
            args = ['question_quality', '--output-prefix', prefix, '--prepare-only']
            with patch('sys.argv', args):
                main()
            target = Path(prefix + '.json')
            before = target.read_bytes()
            report = json.loads(before)
            self.assertEqual('question-quality-v6', report['version'])
            self.assertEqual(2400, report['options']['num_predict'])
            with patch('sys.argv', args + ['--resume']):
                main()
            self.assertEqual(before, target.read_bytes())
            report['input_sha256'] = 'previous-protocol'
            target.write_text(json.dumps(report), encoding='utf-8')
            previous = target.read_bytes()
            with patch('sys.argv', args + ['--resume']):
                with self.assertRaisesRegex(ValueError, 'use outro prefixo'):
                    main()
            self.assertEqual(previous, target.read_bytes())

    def test_invalid_rating_and_invented_evidence_rejected(self):
        validate_rating({'dimensions': self.ratings}, self.case)
        self.ratings['unambiguity']['evidence'] = [{'source': 'question', 'quote': 'janeiro de 2026'}]
        with self.assertRaises(ValueError):
            validate_rating({'dimensions': self.ratings}, self.case)

    def test_pending_and_not_assessable_do_not_become_passes(self):
        cases = [{'dimensions': {k: {'status': status, 'method': 'llm_preliminary'} for k in DIMENSIONS}}
                 for status in ('pass', 'fail', 'pending', 'not_assessable')]
        stats = summarize(cases)['unambiguity']
        self.assertEqual(2, stats['evaluated'])
        self.assertEqual(.5, stats['pass_rate_evaluated'])
        self.assertEqual(0, stats['reviewed'])

    def test_review_bound_to_inputs_requires_provenance(self):
        report = {'input_sha256': 'abc', 'cases': [{**self.case, 'dimensions': self.ratings}]}
        review = {'input_sha256': 'wrong', 'ratings': []}
        with self.assertRaises(ValueError):
            apply_review(report, review)
        review = {'input_sha256': 'abc', 'ratings': [{'id': 1, 'dimension': 'unambiguity',
                   'status': 'partial', 'review_kind': 'ai_assisted', 'reviewer': 'Lucas',
                   'reviewed_at': '2026-09-25', 'justification': 'Duas interpretações.'}]}
        apply_review(report, review)
        self.assertEqual(1, report['summary']['unambiguity']['reviewed'])

    def test_metadata_evidence_has_its_own_source(self):
        rating = deepcopy(self.ratings['data_availability'])
        rating['evidence'] = [{'source': 'dataset:a', 'quote': 'field'}]
        validate_rating({'dimensions': {'data_availability': rating}}, self.case,
                        ('data_availability',), {'dataset:a': 'field'})
        with self.assertRaises(ValueError):
            validate_rating({'dimensions': {'data_availability': rating}}, self.case, ('data_availability',))

    def test_unnamed_metadata_sources_are_stable_unique_and_unchanged(self):
        meta = {'datasets': [{'descricao': 'Vacinação'}, {'nome_curto': ''},
                             {'nome_curto': 'unnamed:1'}, {'nome_curto': 'srag'}]}
        original = deepcopy(meta)
        sources = evidence_sources(self.case, meta, 'support')
        self.assertEqual(sources, evidence_sources(self.case, meta, 'support'))
        self.assertEqual(original, meta)
        self.assertEqual(5, len(sources))
        self.assertEqual(meta['datasets'][0], json.loads(sources['dataset:unnamed:1:']))
        self.assertIn('dataset:unnamed:2', sources)
        self.assertIn('dataset:srag', sources)



if __name__ == '__main__':
    unittest.main()
