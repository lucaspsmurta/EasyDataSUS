import json
from copy import deepcopy
from pathlib import Path
import unittest

from backend.evaluation.revise_questions import revise, VERSION, BODIES


class RevisedQuestionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((Path(__file__).resolve().parents[2] /
            'docs/avaliacao_acuracia/catalogo_68_v4.json').read_text(encoding='utf-8'))

    def test_preserves_references_and_history_without_mutating_source(self):
        before = deepcopy(self.source)
        revised = revise(self.source)
        self.assertEqual(before, self.source)
        self.assertEqual(VERSION, revised['version'])
        self.assertEqual(set(range(1, 69)), set(BODIES))
        self.assertEqual(68, len(revised['cases']))
        for old, new in zip(self.source['cases'], revised['cases']):
            for key in ('id', 'original_question', 'reference_sql', 'columns', 'comparison',
                        'expected_behavior', 'implementation_supported', 'expected_datasets',
                        'expected_relationships'):
                self.assertEqual(old[key], new[key], (old['id'], key))
            self.assertEqual(old['question'], new['previous_question'])
            self.assertNotEqual(old['question'], new['question'])
            self.assertEqual('pending', new['question_revision']['human_review'])

    def test_limitation_cases_are_not_promoted_to_numeric_references(self):
        for case in revise(self.source)['cases'][64:]:
            self.assertIsNone(case['reference_sql'])
            self.assertEqual('limitation', case['expected_behavior'])
            self.assertFalse(case['implementation_supported'])
            self.assertTrue(case['question_revision']['semantic_change'])
            self.assertTrue(case['proposed_output_columns'])

    def test_incomplete_catalog_is_rejected(self):
        source = deepcopy(self.source)
        source['cases'].pop()
        with self.assertRaises(ValueError):
            revise(source)

    def test_repeated_cases_are_still_disclosed(self):
        cases = {c['id']: c for c in revise(self.source)['cases']}
        for duplicate, original in ((21, 20), (26, 17), (27, 18), (64, 63)):
            self.assertEqual(original, cases[duplicate]['repeat_of'])


if __name__ == '__main__':
    unittest.main()
