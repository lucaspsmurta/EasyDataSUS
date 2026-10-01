import unittest

from backend.services.analytical_contract import contract_errors


class RevisedWordingContractTests(unittest.TestCase):
    def test_negated_substitution_is_not_a_requested_field(self):
        for question in ('Use NATUREZA_JURIDICA; não substitua por TP_GESTAO.',
                         'Não substitua NATUREZA_JURIDICA por TP_GESTAO.'):
            self.assertEqual([], contract_errors('SELECT NATUREZA_JURIDICA FROM leitos', question,
                                                 ['NATUREZA_JURIDICA', 'TP_GESTAO']))
            self.assertIn('Campo explicitamente excluído: TP_GESTAO', contract_errors(
                'SELECT NATUREZA_JURIDICA, TP_GESTAO FROM leitos', question,
                ['NATUREZA_JURIDICA', 'TP_GESTAO']))

    def test_municipality_alias_does_not_require_name_column(self):
        self.assertEqual([], contract_errors('SELECT CO_IBGE AS municipio FROM leitos',
            'Identifique o município pelo código CO_IBGE. Retorne municipio.', ['CO_IBGE', 'MUNICIPIO']))
        for wording in ('Retorne o campo municipio', 'Retorne MUNICIPIO', 'Retorne `municipio`'):
            self.assertIn('Campo solicitado ausente: MUNICIPIO', contract_errors(
                'SELECT CO_IBGE FROM leitos', wording, ['MUNICIPIO']))

    def test_numeric_empty_string_error_has_actionable_correction(self):
        metadata = {'uf': {'tipo': 'Int32'}, 'bairro': {'type': 'String'}}
        for predicate in ("uf != ''", "'' = uf"):
            self.assertTrue(any('toString' in error for error in contract_errors(
                'SELECT uf FROM places WHERE ' + predicate, 'Código não vazio', metadata)))
        for predicate in ("toString(uf) != ''", "bairro != ''", 'uf > 0'):
            self.assertEqual([], contract_errors('SELECT uf FROM places WHERE ' + predicate,
                                                 'Código não vazio', metadata))

    def test_removing_limit_does_not_fix_maximum_with_ties(self):
        question = 'Qual categoria tem a maior soma? Inclua todos os empatados.'
        prefix = 'WITH a AS (SELECT categoria, SUM(valor) AS total FROM vendas GROUP BY categoria) '
        self.assertTrue(any('ORDER BY' in error for error in contract_errors(
            prefix + 'SELECT categoria,total FROM a ORDER BY total DESC', question)))
        self.assertEqual([], contract_errors(prefix +
            'SELECT categoria,total FROM a WHERE total=(SELECT MAX(total) FROM a) ORDER BY total DESC', question))
        self.assertEqual([], contract_errors(prefix +
            'SELECT categoria,total FROM a ORDER BY total DESC', 'Liste todas as categorias por total decrescente.'))


if __name__ == '__main__':
    unittest.main()
