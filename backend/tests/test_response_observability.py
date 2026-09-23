import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from routes.query import ask, AskRequest


class ResponseObservabilityTests(unittest.TestCase):
    def test_success_and_failure_have_total_and_all_stage_times(self):
        for success in (True, False):
            def execute(req, timings):
                timings['stages'].update(dataset_selection=3.0, sql_generation=5.0)
                return {'success':success, 'data':[], 'dataset':'surtos-srag',
                        'sql_generation_mode':'llm' if success else 'llm_error'}
            output = io.StringIO()
            with patch('routes.query._ask', side_effect=execute), patch('routes.query.time.perf_counter', side_effect=[100.0,110.0]), contextlib.redirect_stdout(output):
                result = ask(AskRequest(question='Pergunta'))
            self.assertEqual(10.0, result['timing_s']['total'])
            self.assertEqual(10.0, result['evaluation_metrics']['automatic_metrics']['total_time_s'])
            self.assertEqual(2.0, result['timing_s']['other_processing'])
            self.assertIn('dataset_selection', output.getvalue())
            self.assertIn('3.00 s', output.getvalue())

    def test_actual_generation_failure_keeps_timing(self):
        with patch('routes.query.generate_sql', return_value=(None,'llm_error')), contextlib.redirect_stdout(io.StringIO()):
            result = ask(AskRequest(question='Mostre o resultado', dataset='surtos-srag'))
        self.assertFalse(result['success'])
        self.assertEqual('sql_generation', result['evaluation_metrics']['automatic_metrics']['failure_stage'])
        self.assertIsNotNone(result['evaluation_metrics']['automatic_metrics']['total_time_s'])

    def test_route_uses_explicit_interpretation_mode(self):
        summary = 'Consulte a tabela para visualizar os 10 registros.'
        for rows, expected in (([], 'deterministic_empty'), ([(10,)], 'llm_grounded')):
            llm = MagicMock()
            llm.generate.return_value = summary
            with patch('routes.query.generate_sql', return_value=('SELECT COUNT(*) AS total FROM srag','llm')), \
                 patch('routes.query.run_query', return_value=rows), \
                 patch('routes.query.build_factual_summary', return_value=summary), \
                 patch('routes.query.should_use_deterministic_interpretation', return_value=False), \
                 patch('services.interpretation_service.get_llm', return_value=llm), \
                 contextlib.redirect_stdout(io.StringIO()):
                result = ask(AskRequest(question='Mostre o resultado', dataset='surtos-srag'))
            self.assertTrue(result['success'])
            self.assertEqual(expected, result['interpretation_mode'])
            self.assertEqual(expected, result['evaluation_metrics']['generation']['interpretation_mode'])
            self.assertEqual(0 if not rows else 1, llm.generate.call_count)


if __name__ == '__main__':
    unittest.main()
