import copy
import unittest

from backend.evaluation.accuracy import digest
from backend.evaluation.quality import assess, apply_review, build, summarize


class ResponseQualityTests(unittest.TestCase):
    def setUp(self):
        self.case = dict(id=1, question='Conte registros', expected_behavior='answer',
                         expected_datasets=['a'], expected_relationships=[],
                         columns=['total'], expected_rows=[[10]])
        self.result = dict(id=1, question='Conte registros', expected_behavior='answer',
                           assessment=dict(status='correct', result_correct=True),
                           response=dict(success=True, sql='SELECT count(*) FROM a',
                                         validation=dict(valid=True), data=[[10]], datasets=['a'],
                                         insight='Há 10 registros.'))

    def test_equivalence_does_not_certify_semantic_dimensions(self):
        c = assess(self.case, self.result)
        self.assertEqual('pass', c['dimensions']['result_equivalence']['status'])
        for name in ('filters', 'aggregation', 'main_information', 'text_fidelity'):
            self.assertEqual('pending', c['dimensions'][name]['status'])

    def test_failure_is_not_quality_pass_and_denominators_are_explicit(self):
        failure = copy.deepcopy(self.result)
        failure['assessment'] = dict(status='technical_failure', result_correct=False)
        failure['response'] = dict(success=False)
        a = assess(self.case, self.result)
        b = assess(dict(self.case, id=2), failure)
        s = summarize([a, b])
        self.assertEqual(0.5, s['result_equivalence']['pass_rate_evaluated'])
        self.assertEqual(1, s['main_information']['counts']['pending'])
        self.assertEqual(1, s['main_information']['counts']['not_assessable'])
        self.assertIsNone(s['main_information']['pass_rate_evaluated'])
        self.assertEqual(0, s['main_information']['coverage'])

    def test_extra_columns_and_empty_result_are_distinguished(self):
        r = copy.deepcopy(self.result)
        r['response']['data'] = [[10, 2]]
        c = assess(self.case, r)
        self.assertEqual('pass', c['dimensions']['row_count']['status'])
        self.assertEqual('fail', c['dimensions']['column_count']['status'])
        r['response']['data'] = []
        c = assess(self.case, r)
        self.assertEqual('fail', c['dimensions']['row_count']['status'])
        self.assertEqual('not_assessable', c['dimensions']['column_count']['status'])

    def test_limitation_does_not_enter_analytical_denominator(self):
        case = dict(self.case, expected_behavior='limitation')
        result = dict(self.result, assessment=dict(status='expected_limitation', limitation_correct=True),
                      response=dict(success=False, datasets=['a']))
        s = summarize([assess(case, result)])
        self.assertEqual(0, s['result_equivalence']['applicable'])
        self.assertEqual(1, s['controlled_limitation']['evaluated'])
        self.assertEqual(1.0, s['controlled_limitation']['pass_rate_evaluated'])

    def test_review_requires_evidence_provenance_and_matching_files(self):
        cases = [assess(self.case, self.result)]
        entry = dict(id=1, dimension='main_information', status='pass', evidence='Valor 10 corresponde à referência.',
                     reviewer='Revisor de teste', reviewed_at='2026-09-24', review_kind='ai_assisted')
        review = dict(results_sha256='r', reference_sha256='f', ratings=[entry])
        with self.assertRaises(ValueError):
            apply_review(cases, review, 'outro', 'f')
        invalid = copy.deepcopy(review)
        invalid['ratings'][0]['evidence'] = ''
        with self.assertRaises(ValueError):
            apply_review(cases, invalid, 'r', 'f')
        apply_review(cases, review, 'r', 'f')
        self.assertEqual({'ai_assisted': 1}, summarize(cases)['main_information']['methods'])
        self.assertEqual('pending', cases[0]['dimensions']['filters']['status'])

    def test_bundle_integrity_and_question_identity(self):
        bundle = dict(ready=True, cases=[self.case])
        bundle['integrity_sha256'] = digest(bundle)
        result = dict(reference_sha256=bundle['integrity_sha256'], snapshot_unchanged=True,
                      summary={'total': 1}, results=[self.result])
        self.assertEqual(1, len(build(result, bundle, 'hash')['cases']))
        altered = copy.deepcopy(result)
        altered['results'][0]['question'] = 'Outra pergunta'
        with self.assertRaises(ValueError):
            build(altered, bundle, 'hash')
        altered = copy.deepcopy(bundle)
        altered['cases'][0]['expected_rows'] = [[20]]
        with self.assertRaises(ValueError):
            build(result, altered, 'hash')


if __name__ == '__main__':
    unittest.main()
