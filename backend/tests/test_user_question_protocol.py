import unittest
from backend.evaluation.accuracy import compare_rows, align_result, score
from backend.services.question_intent import analytical_intent


class UserQuestionProtocolTests(unittest.TestCase):
    def test_negated_people_do_not_request_distinct_count(self):
        for suffix in ('não pessoas diferentes', 'não contando pessoas diferentes', 'nem pessoas distintas'):
            intent = analytical_intent('Conte registros de doses, ' + suffix)
            self.assertNotIn('distinct_entities', [r['kind'] for r in intent['requirements']])
        intent = analytical_intent('Conte pessoas diferentes, não doses.')
        self.assertIn('distinct_entities', [r['kind'] for r in intent['requirements']])
        intent = analytical_intent('Conte UBS diferentes, não pessoas diferentes.')
        distinct = next(r for r in intent['requirements'] if r['kind'] == 'distinct_entities')
        self.assertEqual(['ubs diferentes'], distinct['evidence'])

    def test_natural_age_intervals_preserve_age_requirement(self):
        intent = analytical_intent('Separe nas faixas de até 18 anos e de 19 a 59 anos.')
        self.assertIn('age_groups', [r['kind'] for r in intent['requirements']])

    def test_domain_guidance_is_available_before_first_attempt(self):
        from backend.services.domain_requirements import domain_context
        self.assertIn('UNION ALL', domain_context('Quantas notificações com cada sintoma?', ['surtos-srag']))
        self.assertIn('UTI_*_EXIST', domain_context('Quantos leitos de UTI cadastrados?', ['leitos']))
        self.assertIn('não acrescente NOME', domain_context('Qual município tem mais UBS?', ['atencao-basica']))
        self.assertEqual('', domain_context('Quantas doses?', ['covid-19-vacinacao']))

    def test_repair_missing_ubs_name_does_not_invent_municipality_name(self):
        from backend.services.sql_repair import repair_prompt
        repaired = repair_prompt('UBS com código IBGE', [{'sql':'SELECT NOME FROM counts', 'errors':['UNKNOWN_IDENTIFIER NOME']}])
        self.assertIn('remova NOME', repaired)
        self.assertNotIn('remova NOME', repair_prompt('Outra fonte', [{'sql':'SELECT x', 'errors':['UNKNOWN_IDENTIFIER x']}]))

    def test_monthly_intent_and_no_invented_scope(self):
        result=analytical_intent('Quantos registros há por mês e ano?')
        self.assertTrue(any('mensal' in s for s in result['explicit_cues']))
        self.assertNotIn('2026',str(result))
        self.assertEqual([],analytical_intent('Quantos cidadãos foram vacinados?')['explicit_cues'])

    def test_large_reordered_columns_fail_quickly(self):
        a=[[i,'bairro',i+1] for i in range(33696)]
        b=[['bairro',i,i+1] for i in range(33696)]
        self.assertFalse(compare_rows(a,b,{}))
        self.assertTrue(compare_rows(a,list(reversed(a)),{}))

    def test_exact_numeric_and_identifier_types(self):
        self.assertTrue(compare_rows([[2]],[[2.0]],{}))
        self.assertFalse(compare_rows([['02']],[[2]],{}))
        self.assertFalse(compare_rows([[True]],[[1]],{}))

    def test_declared_projection_does_not_hide_wrong_values(self):
        policy={'aliases':{'sexo':['genero'],'percentual':['percentage']},'allow_extra_columns':True}
        case={'expected_behavior':'answer','expected_rows':[['F',52.0]],'columns':['sexo','percentual'],
              'comparison':{},'result_alignment':policy}
        response={'success':True,'columns':['percentage','genero','contagem'],'data':[[52.0,'F',100]]}
        self.assertTrue(score(case,response)['result_correct'])
        response['data'][0][0]=51.0
        self.assertFalse(score(case,response)['result_correct'])
        response['columns']=['x','y','z']
        self.assertFalse(score(case,response)['result_correct'])

    def test_duplicate_aliases_are_not_guessed(self):
        self.assertIsNone(align_result([[1,1]],['total','quantidade'],['total'],
                                      {'aliases':{'total':['quantidade']},'allow_extra_columns':True}))

    def test_value_aliases_explicit_only(self):
        p={'value_aliases':{'faixa':{'60 anos ou mais':'60+'}}}
        self.assertEqual([['60+']],align_result([['60 anos ou mais']],['faixa'],['faixa'],p))
        self.assertEqual([['59+']],align_result([['59+']],['faixa'],['faixa'],p))

    def test_scalar_join_is_not_arbitrary_join_permission(self):
        from backend.services.multibase_service import multibase_service
        from sqlglot import parse_one, exp
        sql='WITH latest AS (SELECT MAX(COMP) AS m FROM leitos) SELECT UF FROM leitos JOIN latest ON leitos.COMP = latest.m'
        tree=parse_one(sql,read='clickhouse')
        self.assertTrue(multibase_service._scalar_filter_join(tree,next(tree.find_all(exp.Join))))
        tree=parse_one(sql.replace('SELECT MAX(COMP) AS m','SELECT COMP AS m'),read='clickhouse')
        self.assertFalse(multibase_service._scalar_filter_join(tree,next(tree.find_all(exp.Join))))

    def test_extreme_membership_filter_and_unfiltered_ranking(self):
        from backend.services.analytical_contract import contract_errors
        sql='WITH counts AS (SELECT category, COUNT(*) AS n FROM source GROUP BY category) SELECT category, COUNT(*) FROM source WHERE category IN (SELECT category FROM counts WHERE n = (SELECT MAX(n) FROM counts)) GROUP BY category'
        question='Qual categoria tem mais registros? Mostre todos os empatados.'
        self.assertFalse(contract_errors(sql,question))
        self.assertTrue(contract_errors('SELECT category, COUNT(*) FROM source GROUP BY category',question))

    def test_group_key_deduplication_is_valid_preaggregation(self):
        from services.multibase_service import multibase_service
        from services.relationship_service import relationship_service
        datasets=['surtos-srag','atencao-basica']
        sql='WITH s AS (SELECT co_mun_not AS municipio FROM srag GROUP BY co_mun_not), u AS (SELECT ibge AS municipio FROM atencao_basica GROUP BY ibge) SELECT COUNT(*) FROM s JOIN u ON s.municipio=u.municipio'
        self.assertTrue(multibase_service.validate_sql(sql,datasets,relationship_service.find_relationships(datasets)).valid)

    def test_natural_ratio_requires_division(self):
        from backend.services.analytical_contract import contract_errors
        q='Quantos registros de reforço existem para cada registro de primeira dose?'
        self.assertTrue(contract_errors('SELECT COUNT(*) FROM vacinacao',q))
        self.assertFalse(contract_errors('SELECT countIf(a=1)/nullIf(countIf(a=2),0) FROM vacinacao',q))

    def test_latest_survey_scope_covers_or(self):
        from backend.services.analytical_contract import contract_errors
        q='Quantos leitos no levantamento mais recente disponível?'
        bad="SELECT SUM(LEITOS_SUS) FROM leitos WHERE COMP=(SELECT MAX(COMP) FROM leitos) AND NATUREZA_JURIDICA LIKE '2%' OR NATUREZA_JURIDICA LIKE '3%'"
        good="SELECT SUM(LEITOS_SUS) FROM leitos WHERE COMP=(SELECT MAX(COMP) FROM leitos) AND (NATUREZA_JURIDICA LIKE '2%' OR NATUREZA_JURIDICA LIKE '3%')"
        self.assertTrue(contract_errors(bad,q))
        self.assertFalse(contract_errors(good,q))

    def test_unresolved_alias_is_not_malformed_result(self):
        c={'expected_behavior':'answer','columns':['total'],'expected_rows':[[1]],'comparison':{},'result_alignment':{}}
        c['result_alignment']={'aliases':{'total':[]}}
        result=score(c,{'success':True,'columns':['desconhecido'],'data':[[2]]})
        self.assertIn('column_alignment_unresolved',result['mismatch_reasons'])
        self.assertNotIn('invalid_result_shape',result['mismatch_reasons'])

    def test_latest_period_inner_join_and_unsafe_variants(self):
        from backend.services.analytical_contract import contract_errors
        q='Quantos leitos por estado no levantamento mais recente?'
        sql='WITH latest AS (SELECT MAX(COMP) AS m FROM leitos) SELECT UF, SUM(LEITOS_EXISTENTES) FROM leitos JOIN latest ON leitos.COMP=latest.m GROUP BY UF'
        self.assertFalse(contract_errors(sql,q))
        self.assertTrue(contract_errors(sql.replace('JOIN latest','LEFT JOIN latest'),q))
        self.assertTrue(contract_errors(sql.replace('MAX(COMP)','MAX(LEITOS_EXISTENTES)'),q))
        self.assertTrue(contract_errors(sql.replace('leitos.COMP=latest.m','leitos.COMP>latest.m'),q))

    def test_natural_ratio_scale_and_zero_protection(self):
        from backend.services.analytical_contract import contract_errors, prepare_sql
        q='Quantos registros de A existem para cada registro de B?'
        self.assertTrue(contract_errors('SELECT 100.0 * countIf(a=1)/countIf(a=2) FROM source',q))
        sql=prepare_sql('SELECT countIf(a=1)/countIf(a=2) FROM source',q)
        self.assertIn('NULLIF',sql.upper())
        self.assertFalse(contract_errors(sql,q))

    def test_domain_measures_not_names_or_indicator_combinations(self):
        from services.domain_requirements import domain_errors
        self.assertTrue(domain_errors('SELECT COUNT(DISTINCT nome) FROM atencao_basica','Quantas UBS diferentes existem?',['atencao-basica']))
        self.assertFalse(domain_errors('SELECT COUNT(DISTINCT cnes) FROM atencao_basica','Quantas UBS diferentes existem?',['atencao-basica']))
        self.assertTrue(domain_errors('SELECT febre, COUNT(*) FROM srag GROUP BY febre','Quantas notificações registram cada sintoma?',['surtos-srag']))
        self.assertFalse(domain_errors('SELECT countIf(febre=1) FROM srag','Quantas notificações registram cada sintoma?',['surtos-srag']))
        self.assertTrue(domain_errors('SELECT SUM(LEITOS_SUS) FROM leitos','Quantos leitos de UTI em cada modalidade: adulto e neonatal?',['leitos']))
        self.assertFalse(domain_errors('SELECT SUM(UTI_ADULTO_EXIST), SUM(UTI_NEONATAL_EXIST) FROM leitos','Quantos leitos de UTI em cada modalidade: adulto e neonatal?',['leitos']))

    def test_alias_case_is_preserved_in_group_and_order(self):
        from services.multibase_service import multibase_service
        sql=multibase_service.canonicalize_sql_identifiers(
            'SELECT bairro AS bairro, COUNT(*) AS total FROM atencao_basica GROUP BY BAIRRO ORDER BY BAIRRO', ['atencao-basica'])
        self.assertIn('GROUP BY bairro',sql)
        self.assertIn('ORDER BY bairro',sql)

    def test_repair_has_history_and_specific_guidance(self):
        from services.sql_repair import repair_prompt, generation_attempts
        from unittest.mock import patch
        import os
        history=[{'sql':'SELECT SUM(countIf(x=1)) FROM t', 'errors':['ILLEGAL_AGGREGATION aggregate']}]
        prompt=repair_prompt('Pergunta original',history)
        self.assertIn('não envolva em SUM',prompt)
        self.assertIn('Pergunta original',prompt)
        self.assertIn(history[0]['sql'],prompt)
        with patch.dict(os.environ,{'SQL_GENERATION_MAX_ATTEMPTS':'100'}):
            self.assertEqual(4,generation_attempts())

    def test_second_repair_preserves_previous_validation_errors(self):
        import os
        from unittest.mock import patch, MagicMock
        from services.sql_service import generate_sql
        from metadata.loader import load_metadata
        llm=MagicMock()
        llm.generate.side_effect=['SELECT COUNT(*) AS n FROM srag']*3
        validator=MagicMock(side_effect=[['first planning error'],['second planning error'],[]])
        with patch.dict(os.environ,{'SQL_GENERATION_STRATEGY':'llm_first','SQL_GENERATION_MAX_ATTEMPTS':'3'}), patch('services.sql_service.get_llm',return_value=llm):
            sql,mode=generate_sql('Quantas notificações existem?',load_metadata('surtos-srag'),'test',
                                 'surtos-srag',return_mode=True,sql_validator=validator)
        self.assertEqual('llm',mode)
        self.assertEqual(3,validator.call_count)
        last_prompt=llm.generate.call_args.args[0]
        self.assertIn('first planning error',last_prompt)
        self.assertIn('second planning error',last_prompt)

    def test_provider_sends_context_and_output_limits(self):
        import os
        from unittest.mock import patch, MagicMock
        from llm.ollama_provider import OllamaProvider
        response=MagicMock()
        response.json.return_value={'response':'SELECT 1','done_reason':'stop'}
        with patch.dict(os.environ,{'OLLAMA_NUM_CTX':'8192'}), patch('llm.ollama_provider.requests.post',return_value=response) as post:
            self.assertEqual('SELECT 1',OllamaProvider('test').generate('prompt',num_predict=1024))
        options=post.call_args.kwargs['json']['options']
        self.assertEqual(8192,options['num_ctx'])
        self.assertEqual(1024,options['num_predict'])

    def test_units_and_dimensions_are_not_interchangeable(self):
        from services.domain_requirements import domain_errors
        q='Quantas UBS diferentes estão cadastradas em cada município do Sul?'
        self.assertTrue(domain_errors('SELECT ibge,nome,COUNT(DISTINCT cnes) FROM atencao_basica GROUP BY ibge,nome',q,['atencao-basica']))
        self.assertFalse(domain_errors('SELECT ibge,COUNT(DISTINCT cnes) FROM atencao_basica GROUP BY ibge',q,['atencao-basica']))
        q='Qual tipo de unidade reúne mais leitos?'
        self.assertTrue(domain_errors('SELECT TP_GESTAO,SUM(LEITOS_EXISTENTES) FROM leitos GROUP BY TP_GESTAO',q,['leitos']))
        self.assertFalse(domain_errors('SELECT DS_TIPO_UNIDADE,SUM(LEITOS_EXISTENTES) FROM leitos GROUP BY DS_TIPO_UNIDADE',q,['leitos']))
        self.assertTrue(domain_errors('SELECT COUNT(*) FROM leitos','Quantos leitos SUS estão cadastrados?',['leitos']))
        self.assertFalse(domain_errors('SELECT SUM(LEITOS_SUS) FROM leitos','Quantos leitos SUS estão cadastrados?',['leitos']))
        self.assertFalse(domain_errors('SELECT COUNT(*) FROM leitos','Quantos estabelecimentos têm leitos?',['leitos']))

    def test_text_state_cannot_be_compared_with_number(self):
        from backend.services.analytical_contract import contract_errors
        schema={'sg_uf_not':{'type':'String'},'ibge':{'type':'Int32'}}
        self.assertTrue(contract_errors('SELECT COUNT(*) FROM srag WHERE sg_uf_not>0','Quantas notificações?',schema))
        self.assertFalse(contract_errors("SELECT COUNT(*) FROM srag WHERE sg_uf_not!=''",'Quantas notificações?',schema))
        self.assertFalse(contract_errors('SELECT COUNT(*) FROM srag WHERE ibge>0','Quantos municípios?',schema))


if __name__=='__main__':
    unittest.main()
