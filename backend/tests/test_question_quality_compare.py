import unittest
from copy import deepcopy

from backend.evaluation.question_quality_compare import compare, digest


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.report = {'metadata': {}, 'rubric': {'a': 'A', 'b': 'B', 'c': 'C'},
                       'cases': [{'id': 12, 'question': 'Pergunta?', 'context': '',
                                  'dimensions': {'a': {'status': 'pass'}, 'b': {'status': 'fail'},
                                                 'c': {'status': 'pending'}}}]}
        self.reference = {'review_kind': 'ai_assisted', 'status': 'provisional',
                          'metadata_sha256': digest({}), 'rubric_sha256': digest(self.report['rubric']),
                          'cases': deepcopy(self.report['cases'])}
        for rating in self.reference['cases'][0]['dimensions'].values():
            rating['status'] = 'pass'

    def test_pending_is_separate_and_rejected_attempts_do_not_count(self):
        self.report['cases'][0]['attempts'] = [{'dimensions': {'c': {'status': 'pass'}}}]
        result = compare(self.reference, self.report)
        self.assertEqual((3, 2, 1, 1, 1), tuple(result[k] for k in
                         ('total', 'evaluated', 'pending', 'agreements', 'disagreements')))
        self.assertEqual(.5, result['agreement_among_evaluated'])

    def test_changed_inputs_are_rejected(self):
        for key in ('metadata', 'rubric'):
            report = deepcopy(self.report)
            report[key]['changed'] = True
            with self.assertRaises(ValueError):
                compare(self.reference, report)
        self.report['cases'][0]['question'] = 'Outra pergunta'
        with self.assertRaises(ValueError):
            compare(self.reference, self.report)

    def test_duplicates_and_reviewed_outputs_are_rejected(self):
        reference = deepcopy(self.reference)
        reference['cases'] *= 2
        with self.assertRaises(ValueError):
            compare(reference, self.report)
        self.report['cases'][0]['dimensions']['a']['method'] = 'ai_assisted'
        with self.assertRaises(ValueError):
            compare(self.reference, self.report)

    def test_all_pending_has_no_agreement_rate(self):
        for rating in self.report['cases'][0]['dimensions'].values():
            rating['status'] = 'pending'
        self.assertIsNone(compare(self.reference, self.report)['agreement_among_evaluated'])


if __name__ == '__main__':
    unittest.main()
