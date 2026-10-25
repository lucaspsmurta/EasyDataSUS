import unittest
from copy import deepcopy
from backend.evaluation.harmonize import harmonize


class HarmonizeTests(unittest.TestCase):
    def setUp(self):
        self.bundle = {'integrity_sha256': 'source', 'snapshot': {}, 'cases': [
            {'id': 1, 'expected_behavior': 'answer', 'reference_sql': 'SELECT x',
             'expected_rows': [[1], [2]], 'columns': ['x'], 'comparison': {'ordered': False}}]}

    def test_order_only_difference_and_source_preservation(self):
        protocol = deepcopy(self.bundle)
        protocol['cases'][0]['expected_rows'].reverse()
        protocol['cases'][0]['result_alignment'] = {'aliases': {'x': ['value']}}
        result = harmonize(self.bundle, protocol)
        self.assertEqual(result['cases'][0]['expected_rows'], [[1], [2]])
        self.assertNotIn('result_alignment', self.bundle['cases'][0])
        self.assertEqual(result['cases'][0]['result_alignment'], protocol['cases'][0]['result_alignment'])

    def test_different_values_or_contract_rejected(self):
        for key, value in [('expected_rows', [[3]]), ('reference_sql', 'SELECT y')]:
            protocol = deepcopy(self.bundle)
            protocol['cases'][0][key] = value
            with self.assertRaises(ValueError):
                harmonize(self.bundle, protocol)
