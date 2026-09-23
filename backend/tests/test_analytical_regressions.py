import json
import os
import sys
import sqlite3
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from services.analytical_contract import contract_errors, prepare_sql
from services.multibase_service import multibase_service as service
from services.relationship_service import relationship_service
from services.sql_service import fallback_sql, generate_sql, validate_sql_syntax, extract_sql
from metadata.loader import load_metadata
from routes.query import ask, AskRequest, sanitize_sql, _error_response


class AnalyticalRegressions(unittest.TestCase):
    def test_same_base_group_keys_can_join_without_relationship_catalog(self):
        sql = 'WITH a AS (SELECT sg_uf_not AS uf, COUNT(*) AS n FROM srag WHERE evolucao=2 GROUP BY sg_uf_not), b AS (SELECT sg_uf_not AS uf, COUNT(*) AS n FROM srag GROUP BY sg_uf_not) SELECT a.uf, 100.0*a.n/b.n FROM a JOIN b ON a.uf=b.uf'
        self.assertTrue(service.validate_sql(sql, ['surtos-srag'], []).valid)
        unsafe = sql.replace('GROUP BY sg_uf_not)', 'GROUP BY sg_uf_not, cs_sexo)')
        self.assertFalse(service.validate_sql(unsafe, ['surtos-srag'], []).valid)
        self.assertFalse(service.validate_sql(sql.replace('a.uf=b.uf','a.n=b.n'), ['surtos-srag'], []).valid)

    def test_diagnostics_are_opt_in_and_isolated(self):
        from services.generation_diagnostics import capture, record
        record('outside')
        with capture() as first:
            record('first')
            with capture() as second:
                record('second')
            record('last')
        self.assertEqual(['first','last'],[r['stage'] for r in first])
        self.assertEqual(['second'],[r['stage'] for r in second])

    def test_positive_codes_are_grounded_in_numeric_relationship_fields(self):
        datasets = ['surtos-srag', 'atencao-basica']
        relationships = relationship_service.find_relationships(datasets)
        for question in ['Códigos positivos de município de SRAG com CNES positivo em UBS',
                         'Municípios positivos com CNES distintos positivos, sem limitar a quantidade']:
            hints = service._positive_code_filter_hints(question, datasets, relationships)
            self.assertEqual({'srag.co_mun_not > 0', 'atencao_basica.ibge > 0', 'atencao_basica.cnes > 0'}, set(hints))
        self.assertEqual([], service._positive_code_filter_hints('Testes laboratoriais positivos', datasets, relationships))
        self.assertEqual([], service._positive_code_filter_hints('Exclua municípios positivos', datasets, relationships))
        self.assertEqual([], service._positive_code_filter_hints('CNES positivos', ['leitos'], []))

    def test_negated_percentage_does_not_require_scaling(self):
        question = 'Qual a razão, não percentual, entre doses de reforço e primeiras doses?'
        ratio = 'SELECT countIf(paciente_id = 1) / count() FROM vacinacao'
        self.assertEqual([], contract_errors(ratio, question))
        self.assertTrue(contract_errors(ratio.replace('SELECT ', 'SELECT 100.0 * '), question))

    def test_case_insensitive_search_argument_order(self):
        wrong = "SELECT countIf(positionCaseInsensitiveUTF8('reforço', vacina_descricao_dose)>0) FROM vacinacao"
        right = "SELECT countIf(positionCaseInsensitiveUTF8(vacina_descricao_dose, 'reforço')>0) FROM vacinacao"
        self.assertTrue(contract_errors(wrong, 'Conte reforços'))
        self.assertEqual([], contract_errors(right, 'Conte reforços'))

    def test_derived_column_case_preserves_aliases_and_scope(self):
        sql = 'WITH s AS (SELECT CO_MUN_NOT FROM srag), u AS (SELECT IBGE AS Codigo FROM atencao_basica) SELECT s.CO_MUN_NOT,u.codigo FROM s JOIN u ON s.CO_MUN_NOT=u.codigo'
        actual = service.canonicalize_sql_identifiers(sql, ['surtos-srag','atencao-basica'])
        self.assertIn('s.co_mun_not', actual)
        self.assertIn('u.Codigo', actual)
        self.assertIn('ibge AS Codigo', actual)
        nested = 'WITH a AS (SELECT x.CO_MUN_NOT FROM srag x), b AS (SELECT x.IBGE FROM atencao_basica x) SELECT a.CO_MUN_NOT FROM a'
        actual = service.canonicalize_sql_identifiers(nested, ['surtos-srag','atencao-basica'])
        self.assertIn('x.co_mun_not', actual)
        self.assertIn('x.ibge', actual)

    def test_aggregate_alias_does_not_replace_where_column(self):
        sql = 'SELECT SUM(FEBRE=1) AS febre FROM srag WHERE FEBRE=1'
        actual = service.canonicalize_sql_identifiers(sql, ['surtos-srag'])
        self.assertIn('SUM(febre = 1) AS febre', actual)
        self.assertIn('WHERE srag.febre = 1', actual)
        aliased = service.canonicalize_sql_identifiers(sql.replace('FROM srag', 'FROM srag AS X'), ['surtos-srag'])
        self.assertIn('WHERE X.febre = 1', aliased)
        sql = 'SELECT SUM(FEBRE) AS total FROM srag HAVING total > 10'
        self.assertIn('HAVING total > 10', service.canonicalize_sql_identifiers(sql, ['surtos-srag']))

    def test_engine_error_is_used_for_sql_repair(self):
        llm = MagicMock()
        llm.generate.side_effect = ['SELECT SUM(febre=1) AS febre FROM srag WHERE febre=1',
                                    'SELECT SUM(febre=1) AS total_febre FROM srag WHERE febre=1']
        validator = MagicMock(side_effect=[['ClickHouse: aggregate function in WHERE'], []])
        with patch.dict(os.environ, {'SQL_GENERATION_STRATEGY':'llm_first'}), patch('services.sql_service.get_llm',return_value=llm):
            sql, mode = generate_sql('Quantos registros com febre?', load_metadata('surtos-srag'), 'test',
                'surtos-srag', return_mode=True, sql_validator=validator)
        self.assertEqual('llm', mode)
        self.assertIn('total_febre', sql)
        self.assertEqual(2, validator.call_count)
        self.assertIn('aggregate function in WHERE', llm.generate.call_args.args[0])

    def test_unauthorized_sql_is_not_sent_to_engine(self):
        llm = MagicMock()
        llm.generate.return_value = 'SELECT COUNT(*) FROM secret_table'
        validator = MagicMock(return_value=[])
        with patch.dict(os.environ, {'SQL_GENERATION_STRATEGY':'llm_first'}), patch('services.sql_service.get_llm',return_value=llm):
            generate_sql('Consulta fora do catálogo', load_metadata('surtos-srag'), 'test',
                'surtos-srag', sql_validator=validator)
        validator.assert_not_called()

    def test_multibase_engine_error_triggers_retry(self):
        sql = 'WITH s AS (SELECT co_mun_not AS ibge,COUNT(*) AS n FROM srag GROUP BY co_mun_not), u AS (SELECT ibge,COUNT(DISTINCT cnes) AS m FROM atencao_basica GROUP BY ibge) SELECT s.ibge,s.n,u.m FROM s JOIN u ON s.ibge=u.ibge'
        llm = MagicMock()
        llm.generate.return_value = sql
        validator = MagicMock(side_effect=[['ClickHouse: test planning error'], []])
        datasets = ['surtos-srag','atencao-basica']
        with patch.dict(os.environ, {'SQL_GENERATION_STRATEGY':'llm_first'}), patch('services.multibase_service.get_llm',return_value=llm):
            result, mode = service.generate_sql('Liste notificações e CNES distintos por município', 'test', datasets,
                relationship_service.find_relationships(datasets), sql_validator=validator)
        self.assertEqual('llm', mode)
        self.assertIsNotNone(result)
        self.assertEqual(2, validator.call_count)
        self.assertIn('test planning error', llm.generate.call_args.args[0])

    def test_engine_validation_only_explains_and_keeps_diagnostic(self):
        from db.clickhouse import validate_query, run_query
        from clickhouse_connect.driver.exceptions import DatabaseError
        with patch('db.clickhouse.get_client') as factory:
            self.assertEqual([], validate_query('SELECT count() FROM srag'))
            self.assertEqual('EXPLAIN PLAN SELECT count() FROM srag', factory.return_value.query.call_args.args[0])
            factory.return_value.query.side_effect = DatabaseError('Invalid aggregate in WHERE')
            factory.return_value.query.reset_mock()
            result = run_query('SELECT bad FROM srag')
            self.assertEqual(1, factory.return_value.query.call_count)
            self.assertIn('Invalid aggregate', result['message'])

    def test_llm_failure_metrics_do_not_claim_no_attempt(self):
        response = _error_response('Pergunta', ['surtos-srag'], 'Falha', 'SQL não gerado', sql_generation_mode='llm_error')
        metrics = response['evaluation_metrics']['automatic_metrics']
        self.assertTrue(metrics['llm_sql_attempted'])
        self.assertEqual('sql_generation', metrics['failure_stage'])

    def test_union_of_read_queries_is_valid(self):
        sql = "SELECT 'A' AS grupo, COUNT(*) AS total FROM srag WHERE hospital=1 UNION ALL SELECT 'B' AS grupo, COUNT(*) AS total FROM srag WHERE hospital=2"
        validation = service.validate_sql(sql, ['surtos-srag'], [])
        self.assertTrue(validation.valid, validation.errors)

    def test_cross_join_allowed_only_for_scalar_monobase_aggregates(self):
        sql = 'WITH a AS (SELECT COUNT(*) AS n FROM srag), b AS (SELECT COUNT(*) AS m FROM srag WHERE hospital=1) SELECT 100.0*m/n FROM a CROSS JOIN b'
        self.assertTrue(service.validate_sql(sql, ['surtos-srag'], []).valid)
        unsafe = sql.replace('SELECT COUNT(*) AS m FROM srag WHERE hospital=1', 'SELECT hospital AS m FROM srag').replace('SELECT COUNT(*) AS n FROM srag', 'SELECT hospital AS n FROM srag')
        self.assertFalse(service.validate_sql(unsafe, ['surtos-srag'], []).valid)
        window = unsafe.replace('SELECT hospital AS m FROM srag', 'SELECT SUM(hospital) OVER () AS m FROM srag')
        self.assertFalse(service.validate_sql(window, ['surtos-srag'], []).valid)
        grouped = 'WITH a AS (SELECT hospital, COUNT(*) AS n FROM srag GROUP BY hospital), b AS (SELECT COUNT(*) AS m FROM srag) SELECT a.hospital, 100.0*a.n/b.m FROM a, b'
        self.assertTrue(service.validate_sql(grouped, ['surtos-srag'], []).valid)

    def test_preaggregation_in_derived_tables_is_valid(self):
        sql = 'SELECT s.ibge,s.n,u.m FROM (SELECT co_mun_not AS ibge,COUNT(*) AS n FROM srag GROUP BY co_mun_not) s INNER JOIN (SELECT ibge,COUNT(DISTINCT cnes) AS m FROM atencao_basica GROUP BY ibge) u ON s.ibge=u.ibge'
        datasets = ['surtos-srag','atencao-basica']
        validation = service.validate_sql(sql, datasets, relationship_service.find_relationships(datasets))
        self.assertTrue(validation.valid, validation.errors)

    def test_multibase_missing_requested_field_triggers_correction(self):
        sql = 'WITH s AS (SELECT co_mun_not AS ibge,COUNT(*) AS n FROM srag GROUP BY co_mun_not), u AS (SELECT ibge,COUNT(*) AS m FROM atencao_basica GROUP BY ibge) SELECT s.ibge,s.n,u.m FROM s JOIN u ON s.ibge=u.ibge'
        corrected = sql.replace('COUNT(*) AS m', 'COUNT(DISTINCT cnes) AS m')
        llm = MagicMock()
        llm.generate.side_effect = [sql, corrected]
        datasets = ['surtos-srag','atencao-basica']
        with patch.dict(os.environ, {'SQL_GENERATION_STRATEGY':'llm_first'}), patch('services.multibase_service.get_llm',return_value=llm):
            result, mode = service.generate_sql('Liste CNES distintos por município em SRAG e UBS', 'test', datasets, relationship_service.find_relationships(datasets))
        self.assertEqual('llm', mode)
        self.assertIn('CNES', result.upper())
        self.assertEqual(2, llm.generate.call_count)
        self.assertIn('Campo solicitado ausente', llm.generate.call_args.args[0])

    def test_extractor_preserves_full_cte_and_null_predicates(self):
        sql = "WITH totals AS (SELECT uf, COUNT(*) AS n FROM atencao_basica GROUP BY uf)\n\nSELECT uf,n FROM totals WHERE n=(SELECT MAX(n) FROM totals)"
        self.assertEqual(sql, extract_sql('```sql\n' + sql + '\n```'))
        self.assertEqual('SELECT uf FROM atencao_basica WHERE uf IS NOT NULL',
            extract_sql('SELECT uf FROM atencao_basica WHERE uf IS NOT NULL'))
        self.assertIsNone(extract_sql('SELECT uf FROM atencao_basica; SELECT 2'))
        self.assertIsNone(extract_sql('WITH totals AS (SELECT uf FROM atencao_basica)'))

    def test_exact_distinct_aggregate_is_accepted(self):
        self.assertTrue(validate_sql_syntax('SELECT ibge, uniqExact(cnes) AS total FROM atencao_basica GROUP BY ibge',
            'atencao-basica', 'Quais municípios têm mais UBS?'))

    def test_percentage_scale_and_overlapping_indicators(self):
        self.assertTrue(contract_errors('SELECT SUM(hospital) / COUNT(*) FROM srag', 'Qual o percentual?'))
        self.assertEqual([], contract_errors('SELECT 100.0 * SUM(hospital) / COUNT(*) FROM srag', 'Qual o percentual?'))
        self.assertEqual([], contract_errors('SELECT SUM(hospital) / COUNT(*) FROM srag', 'Qual a razão?'))
        wrong = 'SELECT 100.0 * (COUNTIF(asma=1) + COUNTIF(diabetes=1)) / COUNT(*) FROM srag'
        right = 'SELECT 100.0 * COUNTIF(asma=1 OR diabetes=1) / COUNT(*) FROM srag'
        question = 'Qual percentual com ao menos um indicador positivo?'
        self.assertTrue(contract_errors(wrong, question))
        self.assertEqual([], contract_errors(right, question))

    def test_scalar_percentage_does_not_add_helper_columns(self):
        question = 'Qual o percentual de linhas com indicador positivo sobre todas as linhas?'
        self.assertTrue(contract_errors('SELECT COUNT(*), 100.0 * countIf(asma=1)/COUNT(*) FROM srag', question))
        self.assertEqual([], contract_errors('SELECT 100.0 * countIf(asma=1)/COUNT(*) FROM srag', question))

    def test_fields_do_not_introduce_extra_datasets(self):
        cases = [
            ('Municípios de vacinação por código IBGE', ['covid-19-vacinacao']),
            ('Percentual de SRAG com hospital = 1', ['surtos-srag']),
            ('Percentual de SRAG com uti = 1', ['surtos-srag']),
            ('Leitos por CNES e CO_IBGE', ['leitos']),
            ('SRAG e quantidade de leitos de UTI', ['leitos', 'surtos-srag']),
            ('Notificações de SRAG e UBS por município', ['surtos-srag', 'atencao-basica']),
        ]
        for question, expected in cases:
            with self.subTest(question=question), patch('services.multibase_service.get_llm') as llm:
                actual = service.select_datasets(question, 'test', ['covid-19-vacinacao','leitos','surtos-srag','atencao-basica'])
                self.assertEqual(actual.datasets, expected)
                llm.assert_not_called()

    def test_partial_graph_is_controlled_limitation_before_llm(self):
        with patch('routes.query.run_query') as db, patch('services.multibase_service.get_llm') as llm:
            response = ask(AskRequest(question='Municípios com SRAG, UBS e leitos'))
        db.assert_not_called()
        llm.assert_not_called()
        self.assertFalse(response['answerability']['answerable'])
        self.assertEqual('none', response['sql_generation_mode'])

    def test_fallback_does_not_discard_filters_or_units(self):
        for q, ds in [
            ('Quantos casos de SRAG foram notificados em janeiro de 2026?', 'surtos-srag'),
            ('Quantas UBS por município no Nordeste?', 'atencao-basica'),
            ('Quantas doses por ano e mês?', 'covid-19-vacinacao'),
            ('Quantas doses foram aplicadas em SP em 2026?', 'covid-19-vacinacao'),
            ('Quantas pessoas distintas foram vacinadas?', 'covid-19-vacinacao'),
            ('Qual a soma de leitos com natureza jurídica 2 ou 3?', 'leitos'),
        ]:
            with self.subTest(question=q):
                self.assertIsNone(fallback_sql(q, ds))

    def test_fallback_groups_and_distinct_counts(self):
        sql = fallback_sql('Qual é a distribuição de UBS por estado?', 'atencao-basica')
        self.assertIn('GROUP BY uf', sql)
        self.assertNotIn('LIMIT', sql)
        sql = fallback_sql('Quantos municípios possuem notificações de SRAG?', 'surtos-srag')
        self.assertIn('COUNT(DISTINCT co_mun_not)', sql)

    def test_multibase_filters_cannot_be_ignored(self):
        ds = ['surtos-srag','atencao-basica']
        rels = relationship_service.find_relationships(ds)
        q = 'Em quantos municípios há notificações de SRAG e também UBS cadastradas?'
        sql = service.build_deterministic_fallback_sql(ds, rels, q)
        self.assertIn('COUNT(*) AS total_municipios', sql)
        self.assertIsNone(service.build_deterministic_fallback_sql(ds, rels, q.rstrip('?') + ' no RJ?'))
        sql = service.build_deterministic_fallback_sql(ds, rels, 'Liste todos os municípios com registros de SRAG e UBS')
        self.assertNotIn('LIMIT', sql)
        self.assertIn('s.ibge ASC', sql)

    def test_generic_beds_are_not_replaced_by_icu_beds(self):
        datasets = ['covid-19-vacinacao','leitos']
        sql = service.build_deterministic_fallback_sql(datasets,
            relationship_service.find_relationships(datasets), 'Liste doses e leitos por estado')
        self.assertIn('SUM(LEITOS_EXISTENTES)', sql)
        self.assertNotIn('UTI_TOTAL_EXIST', sql)

    def test_null_zero_and_no_hidden_truncation(self):
        sql = prepare_sql('SELECT SUM(hospital) / COUNT(*) FROM srag', 'Retorne nulo se denominador zero')
        self.assertIn('NULLIF', sql.upper())
        self.assertEqual(sql, prepare_sql(sql, 'Retorne nulo'))
        self.assertNotIn('LIMIT', sanitize_sql('SELECT uf FROM atencao_basica'))

    def test_complete_results_and_missing_indicators_rejected(self):
        errors = contract_errors('SELECT cardiopati FROM srag LIMIT 100',
            'Liste todos os registros com cardiopati e hematologi', ['cardiopati','hematologi'])
        self.assertEqual(2, len(errors))
        errors = contract_errors('SELECT NATUREZA_JURIDICA FROM leitos',
            'Use NATUREZA_JURIDICA; não use TP_GESTAO', ['NATUREZA_JURIDICA','TP_GESTAO'])
        self.assertEqual([], errors)

    def test_corrective_llm_retry_preserves_mode(self):
        llm = MagicMock()
        llm.generate.side_effect = [
            'SELECT cardiopati FROM srag',
            'SELECT cardiopati, hematologi FROM srag',
        ]
        with patch.dict(os.environ, {'SQL_GENERATION_STRATEGY':'llm_first'}), patch('services.sql_service.get_llm', return_value=llm):
            sql, mode = generate_sql('Liste cardiopati e hematologi', load_metadata('surtos-srag'), 'test', 'surtos-srag', return_mode=True)
        self.assertEqual('llm', mode)
        self.assertIn('hematologi', sql)
        self.assertEqual(2, llm.generate.call_count)
        self.assertIn('Campo solicitado ausente', llm.generate.call_args.args[0])

    def test_srag_metadata_exposes_loaded_indicators_and_age_unit(self):
        columns = json.loads(load_metadata('surtos-srag'))['columns']
        self.assertTrue({'HEMATOLOGI','HEPATICA','NEUROLOGIC','TP_IDADE'} <= columns.keys())
        self.assertIn('3=anos', columns['TP_IDADE']['description'])

    def test_valid_laboratory_union_is_not_forced_to_include_vsr(self):
        self.assertTrue(validate_sql_syntax('SELECT COUNT(*) FROM srag WHERE pcr_sars2 = 1 OR pos_pcrflu = 1',
            'surtos-srag', 'Quantos registros positivos para SARS ou influenza?'))

    def test_or_cannot_escape_requested_competence(self):
        prefix = 'SELECT SUM(LEITOS_SUS) FROM leitos WHERE COMP = (SELECT MAX(COMP) FROM leitos) AND '
        alternatives = "NATUREZA_JURIDICA LIKE '2%' OR NATUREZA_JURIDICA LIKE '3%'"
        question = 'Soma na maior COMP com natureza 2 ou 3'
        self.assertTrue(contract_errors(prefix + alternatives, question))
        self.assertEqual([], contract_errors(prefix + '(' + alternatives + ')', question))

    def test_extrema_keep_all_ties_on_independent_fixture(self):
        with sqlite3.connect(':memory:') as db:
            db.execute('CREATE TABLE atencao_basica (ibge INT, cnes INT)')
            db.executemany('INSERT INTO atencao_basica VALUES (?,?)', [(1,10),(1,11),(2,20),(2,21),(3,30),(1,10)])
            sql = fallback_sql('Quais municípios possuem o maior número de UBS?', 'atencao-basica')
            self.assertEqual([(1,2),(2,2)], db.execute(sql).fetchall())

    def test_bed_ratio_uses_sum_and_only_latest_period(self):
        with sqlite3.connect(':memory:') as db:
            db.execute('CREATE TABLE leitos (COMP TEXT, UF TEXT, LEITOS_SUS INT, LEITOS_EXISTENTES INT)')
            db.executemany('INSERT INTO leitos VALUES (?,?,?,?)',
                [('202501','RJ',100,100),('202502','RJ',3,10),('202502','RJ',2,10),('202502','SP',0,0)])
            sql = fallback_sql('Qual é a proporção de leitos SUS em relação ao total de leitos existentes por estado na competência mais recente?', 'leitos')
            self.assertEqual([('RJ',5,20,25.0),('SP',0,0,None)], db.execute(sql).fetchall())


if __name__ == '__main__':
    unittest.main()
