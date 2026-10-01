import unittest

from backend.evaluation.question_quality_diagnostic import tasks, validate, schema


class DiagnosticTests(unittest.TestCase):
    def test_inputs_exclude_prior_judgments_and_control_answers(self):
        report = {'metadata': {'datasets': [{'nome_curto': 'sales', 'columns': {
            'amount': {'type': 'Int', 'description': 'Valor', 'private': 'SECRET'}}}]},
            'cases': [{'id': 1, 'question': 'Quantas vendas?', 'context': '',
                       'dimensions': {'secret': 'SECRET'}, 'expected_rows': ['SECRET'],
                       'preparation': {'map': {'support_map': [{'fields': ['field:sales:amount'] * 2}]}}}]}
        result = tasks(report, [1])
        self.assertEqual(4, len(result))
        for task in result:
            self.assertNotIn('SECRET', str(task['input']))
            self.assertNotIn('expected_unambiguity', task['input'])
        self.assertEqual(1, len(result[1]['input']['selected_fields']))
        self.assertEqual(result[2]['input']['question'], result[3]['input']['question'])
        self.assertNotEqual(result[2]['input']['context'], result[3]['input']['context'])

    def test_invalid_and_overlong_response_is_rejected_not_trimmed(self):
        names = schema('support')['properties']['dimensions']['required']
        value = {'dimensions': {name: {'status': 'pass', 'reason': 'Campo presente.'} for name in names}}
        validate(value, 'support')
        value['dimensions'][names[0]]['reason'] = 'x' * 601
        with self.assertRaises(ValueError):
            validate(value, 'support')
        self.assertEqual(601, len(value['dimensions'][names[0]]['reason']))


if __name__ == '__main__':
    unittest.main()
