import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from services.interpretation_service import _fallback_interpretation, interpret_result


class InterpretationServiceTests(unittest.TestCase):
    def test_empty_result_does_not_call_llm_and_reports_its_mode(self):
        with patch('services.interpretation_service.get_llm') as llm:
            text, mode = interpret_result('Pergunta', [], return_mode=True)
        llm.assert_not_called()
        self.assertEqual('deterministic_empty', mode)
        self.assertIn('Não encontrei registros', text)

    def test_identical_llm_text_is_not_misclassified_as_fallback(self):
        summary = 'São Paulo possui 10 registros.'
        llm = MagicMock()
        llm.generate.return_value = summary
        with patch('services.interpretation_service.get_llm', return_value=llm):
            self.assertEqual((summary, 'llm_grounded'), interpret_result('Pergunta', [(10,)], factual_summary=summary, return_mode=True))

    def test_timeout_and_blank_response_report_fallback(self):
        for value in ('', TimeoutError('timeout')):
            llm = MagicMock()
            if isinstance(value, Exception):
                llm.generate.side_effect = value
            else:
                llm.generate.return_value = value
            with patch('services.interpretation_service.get_llm', return_value=llm):
                self.assertEqual(('10 registros.', 'deterministic_fallback'), interpret_result('Pergunta', [(10,)], factual_summary='10 registros.', return_mode=True))

    def test_empty_llm_response_uses_factual_summary(self):
        llm = MagicMock()
        llm.generate.return_value = ""
        with patch("services.interpretation_service.get_llm", return_value=llm):
            response = interpret_result(
                "Apresente os resultados",
                [("SP", 10)],
                factual_summary="São Paulo possui 10 registros.",
            )
        self.assertEqual("São Paulo possui 10 registros.", response)

    def test_generic_fallback_does_not_expose_python_tuple(self):
        response = _fallback_interpretation(
            [("SP", 10, 20), ("RJ", 8, 15)],
            "Compare os resultados",
        )
        self.assertNotIn("('SP'", response)
        self.assertIn("Consulte a tabela", response)


if __name__ == "__main__":
    unittest.main()
